#!/usr/bin/env python3
"""
Google SEO + AI-agent (agentic commerce) improvements for Sheffield Pottery's
Cone Art kilns, applied reproducibly and reversibly through the Shopify Admin
GraphQL API.

Usage:
    export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
    export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx
    python3 scripts/cone_art_seo.py snapshot            # save current state
    python3 scripts/cone_art_seo.py plan                # build cone_art/plan.json (offline)
    python3 scripts/cone_art_seo.py apply               # dry run: list every change
    python3 scripts/cone_art_seo.py apply --execute     # write to the store
    python3 scripts/cone_art_seo.py rollback --execute  # put the snapshot back
    python3 scripts/cone_art_seo.py export              # GraphQL ops apply would run

What `apply` changes (all content lives in scripts/cone_art_content.py):
    * SEO title + meta description on the 40 storefront Cone Art products and
      the Cone Art collections (unique, accurate, within Google's limits).
    * Shopify product category / product type fixes (packages filed as
      "Pottery & Sculpting Materials", a glass kiln filed as kiln furniture...).
    * Factual fixes: wrong model numbers and copy-pasted specs in descriptions,
      spec-table typos, the BX119D voltage filter, mis-tagged pottery kilns
      showing up in the Cone Art Glass Kilns collection.
    * Product FAQs: visible on the page (theme "ABZ Faq" section reads
      custom.product_faqs) and emitted as FAQPage JSON-LD by Booster SEO
      (custom.faqs), for Google and AI answer engines.
    * Shopify standard category attributes (kiln features, loading style,
      firing atmosphere, element type, power source, shape) - the structured
      fields Shopify Catalog exposes to AI shopping agents.
    * seo.hidden=1 on the hidden option products (furniture kits, vents,
      "$0" shelf options...) so they stop being indexed or surfacing in
      storefront/agent search, plus on two empty Cone Art collections.

Safety:
    * `apply` is a dry run unless --execute is passed.
    * `snapshot` records every field this tool can touch; `rollback` restores
      them and deletes the FAQ metaobjects it created. The standard attribute
      definitions/values it enables are left in place (harmless, shared).
    * `plan` refuses to build if a description fix no longer matches the live
      text exactly once, so stale edits can't clobber newer copy.

Admin API scopes: read_products, write_products, read_metaobjects,
write_metaobjects, read_metaobject_definitions, write_metaobject_definitions.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cone_art_content as content  # noqa: E402

API_VERSION = "2025-07"
VENDOR = "Cone Art Kilns"
HIDDEN_TAG = "HideOnStorefront"
FAQ_TYPE = "product_faq"
# userError codes/messages meaning "this standard definition is already enabled"
ALREADY_ENABLED = ["TAKEN", "ALREADY_EXISTS", "already"]

DEFAULT_SNAPSHOT = "cone_art/snapshot.json"
DEFAULT_PLAN = "cone_art/plan.json"
DEFAULT_OPS = "cone_art/ops.json"

# Every metafield this tool may write. The snapshot keeps their prior values.
PRODUCT_METAFIELDS = {
    ("custom", "voltage"),
    ("custom", "kiln_style"),
    ("custom", "kiln_type"),
    ("custom", "gas_or_electric"),
    ("custom", "pdp_under_price_short_desc"),
    ("custom", "pdp_product_short_desc"),
    ("custom", "specifications"),
    ("custom", "product_faqs"),
    ("custom", "faqs"),
    ("seo", "hidden"),
} | {("shopify", key) for key in content.ATTRIBUTE_METAFIELD_KEYS.values()}
COLLECTION_METAFIELDS = {("custom", "faqs"), ("seo", "hidden")}

PRODUCTS_QUERY = """
query ConeArtProducts($cursor: String, $q: String!) {
  products(first: 25, after: $cursor, query: $q) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id title handle productType tags descriptionHtml
      seo { title description }
      category { id }
      metafields(first: 100) { nodes { namespace key type value } }
    }
  }
}
"""

COLLECTIONS_QUERY = """
query ConeArtCollections($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on Collection {
      id handle title descriptionHtml
      seo { title description }
      ruleSet { appliedDisjunctively rules { column relation condition } }
      metafields(first: 100) { nodes { namespace key type value } }
    }
  }
}
"""

METAOBJECT_BY_HANDLE_QUERY = """
query MetaobjectByHandle($h: MetaobjectHandleInput!) {
  metaobjectByHandle(handle: $h) { id handle type }
}
"""


# --------------------------------------------------------------------------
# Admin API
# --------------------------------------------------------------------------
def shopify_graphql(domain, token, query, variables=None):
    url = f"https://{domain}/admin/api/{API_VERSION}/graphql.json"
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Shopify API error {e.code}: {e.read().decode()}")
    if "errors" in payload:
        raise SystemExit(f"Shopify GraphQL errors: {payload['errors']}")
    return payload["data"]


def credentials():
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not domain or not token:
        raise SystemExit(
            "Set SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN environment variables first."
        )
    return domain, token


def user_errors(data):
    """Collect userErrors from every aliased mutation field in a response."""
    errors = []
    for alias, payload in (data or {}).items():
        for err in (payload or {}).get("userErrors") or []:
            errors.append(f"{alias}: {err}")
    return errors


# --------------------------------------------------------------------------
# Snapshot
# --------------------------------------------------------------------------
def _metafield_map(node, allowed):
    return {
        f"{m['namespace']}.{m['key']}": {"type": m["type"], "value": m["value"]}
        for m in node["metafields"]["nodes"]
        if (m["namespace"], m["key"]) in allowed
    }


def trim_product(node):
    return {
        "title": node["title"],
        "handle": node["handle"],
        "productType": node["productType"],
        "tags": sorted(node["tags"]),
        "seo": {"title": node["seo"]["title"], "description": node["seo"]["description"]},
        "category": (node.get("category") or {}).get("id"),
        "descriptionHtml": node["descriptionHtml"],
        "metafields": _metafield_map(node, PRODUCT_METAFIELDS),
    }


def trim_collection(node):
    rule_set = node.get("ruleSet")
    return {
        "handle": node["handle"],
        "title": node["title"],
        "seo": {"title": node["seo"]["title"], "description": node["seo"]["description"]},
        "descriptionHtml": node["descriptionHtml"],
        "ruleSet": {
            "appliedDisjunctively": rule_set["appliedDisjunctively"],
            "rules": [
                {k: r[k] for k in ("column", "relation", "condition")} for r in rule_set["rules"]
            ],
        } if rule_set else None,
        "metafields": _metafield_map(node, COLLECTION_METAFIELDS),
    }


def _nodes(export):
    """Accept a raw GraphQL response, a connection, or a plain list of nodes."""
    if isinstance(export, list):
        return export
    for key in ("data", "products", "collections", "nodes"):
        if isinstance(export, dict) and key in export:
            return _nodes(export[key])
    raise SystemExit("Unrecognised export format")


def fetch_snapshot(domain, token):
    products, cursor = [], None
    while True:
        data = shopify_graphql(
            domain, token, PRODUCTS_QUERY, {"cursor": cursor, "q": f"vendor:'{VENDOR}'"}
        )
        conn = data["products"]
        products.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    data = shopify_graphql(domain, token, COLLECTIONS_QUERY, {"ids": list(content.COLLECTIONS)})
    collections = [n for n in data["nodes"] if n]
    return products, collections


def build_snapshot(product_nodes, collection_nodes):
    return {
        "taken_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "vendor": VENDOR,
        "products": {n["id"]: trim_product(n) for n in product_nodes},
        "collections": {n["id"]: trim_collection(n) for n in collection_nodes},
    }


# --------------------------------------------------------------------------
# Plan
# --------------------------------------------------------------------------
def rich_text(text):
    return json.dumps({
        "type": "root",
        "children": [{"type": "paragraph", "children": [{"type": "text", "value": text}]}],
    })


def apply_text_fixes(text, fixes, where):
    """Apply (old, new[, expected_count]) replacements; expected_count defaults to 1."""
    for fix in fixes:
        old, new = fix[0], fix[1]
        expected = fix[2] if len(fix) > 2 else 1
        count = text.count(old)
        if count != expected:
            raise SystemExit(
                f"{where}: expected {expected} occurrence(s) of {old!r}, found {count}. "
                "The live text changed since this fix was written; update cone_art_content.py."
            )
        text = text.replace(old, new)
    return text


def _mf_value(snap_item, ns, key):
    entry = snap_item["metafields"].get(f"{ns}.{key}")
    return entry["value"] if entry else None


def plan_product(gid, snap, facts, warnings):
    legacy_id = gid.rsplit("/", 1)[-1]
    item = {"id": gid, "title": snap["title"], "handle": snap["handle"], "update": {},
            "tags_add": [], "tags_remove": [], "metafields": [], "faqs": [], "attributes": {}}

    seo = {"title": facts["seo_title"], "description": facts["seo_desc"]}
    if seo != snap["seo"]:
        item["update"]["seo"] = seo
    if facts.get("category") and facts["category"] != snap["category"]:
        item["update"]["category"] = facts["category"]
    if facts.get("product_type") and facts["product_type"] != snap["productType"]:
        item["update"]["productType"] = facts["product_type"]
    fixes = content.DESCRIPTION_FIXES.get(legacy_id, [])
    if fixes:
        desc = apply_text_fixes(snap["descriptionHtml"], fixes, f"{snap['title']} description")
        if desc != snap["descriptionHtml"]:
            item["update"]["descriptionHtml"] = desc

    if facts["family"] != "glass" and content.GLASS_COLLECTION_TAG in snap["tags"]:
        item["tags_remove"].append(content.GLASS_COLLECTION_TAG)
    item["tags_add"] = [t for t in facts.get("add_tags", []) if t not in snap["tags"]]

    def want(ns, key, mtype, value, only_if_missing=False):
        current = _mf_value(snap, ns, key)
        if current == value or (only_if_missing and current is not None):
            return
        item["metafields"].append({"namespace": ns, "key": key, "type": mtype, "value": value})

    if facts["family"] != "part":
        volts = "120 Volt" if facts["volts"] == "120" else "240 or 208"
        want("custom", "voltage", "single_line_text_field", facts.get("voltage", volts))
        want("custom", "kiln_style", "single_line_text_field", "Top Loading")
        want("custom", "gas_or_electric", "single_line_text_field", "Electric")
        kiln_type = "Glass" if facts["family"] == "glass" else facts.get("kiln_type", "Pottery")
        want("custom", "kiln_type", "single_line_text_field", kiln_type, only_if_missing=True)
    if facts.get("item_class"):
        want("custom", "pdp_under_price_short_desc", "single_line_text_field", facts["item_class"])
    if facts.get("short_desc"):
        want("custom", "pdp_product_short_desc", "rich_text_field", rich_text(facts["short_desc"]))
    spec_fixes = content.SPEC_FIXES.get(legacy_id, [])
    if spec_fixes:
        spec = _mf_value(snap, "custom", "specifications")
        if spec is None:
            warnings.append(f"{snap['title']}: spec fixes listed but no custom.specifications")
        else:
            fixed = apply_text_fixes(spec, spec_fixes, f"{snap['title']} specifications")
            want("custom", "specifications", "multi_line_text_field", fixed)

    base = content.faq_handle(facts)
    item["faqs"] = [
        {"handle": f"{base}-{i}", "question": q, "answer": a}
        for i, (q, a) in enumerate(content.product_faqs(facts), start=1)
    ]
    item["attributes"] = content.product_attributes(facts)
    return item


def plan_collection(gid, snap, spec):
    item = {"id": gid, "handle": snap["handle"], "title": snap["title"], "update": {},
            "metafields": []}
    if "seo_title" in spec:
        seo = {"title": spec["seo_title"], "description": spec["seo_desc"]}
        if seo != snap["seo"]:
            item["update"]["seo"] = seo
    desc = snap["descriptionHtml"]
    if spec.get("description_html"):
        desc = spec["description_html"]
    if spec.get("description_replace"):
        desc = apply_text_fixes(desc, spec["description_replace"], f"{snap['handle']} description")
    if desc != snap["descriptionHtml"]:
        item["update"]["descriptionHtml"] = desc
    rule = spec.get("add_rule")
    if rule and snap["ruleSet"] and rule not in snap["ruleSet"]["rules"]:
        item["update"]["ruleSet"] = {
            "appliedDisjunctively": snap["ruleSet"]["appliedDisjunctively"],
            "rules": snap["ruleSet"]["rules"] + [rule],
        }
    if spec.get("faqs"):
        faqs = json.dumps([{"question": q, "answer": a} for q, a in spec["faqs"]])
        if _mf_value(snap, "custom", "faqs") != faqs:
            item["metafields"].append(
                {"namespace": "custom", "key": "faqs", "type": "json", "value": faqs})
    if spec.get("seo_hidden") and _mf_value(snap, "seo", "hidden") != "1":
        item["metafields"].append(
            {"namespace": "seo", "key": "hidden", "type": "number_integer", "value": "1"})
    return item


def build_plan(snapshot, snapshot_path):
    warnings = []
    products, hidden = [], []
    for gid, snap in sorted(snapshot["products"].items(), key=lambda kv: kv[1]["title"]):
        if HIDDEN_TAG in snap["tags"]:
            if _mf_value(snap, "seo", "hidden") != "1":
                hidden.append({"id": gid, "title": snap["title"]})
            continue
        facts = content.PRODUCTS.get(gid.rsplit("/", 1)[-1])
        if not facts:
            warnings.append(f"Storefront product without curated content, skipped: {snap['title']}")
            continue
        products.append(plan_product(gid, snap, facts, warnings))

    collections = []
    for gid, spec in content.COLLECTIONS.items():
        snap = snapshot["collections"].get(gid)
        if not snap:
            warnings.append(f"Collection {spec['handle']} ({gid}) missing from snapshot, skipped")
            continue
        collections.append(plan_collection(gid, snap, spec))

    used = {(t, h) for p in products for t, hs in p["attributes"].items() for h in hs}
    attribute_values = [
        {"type": t, "handle": h, "label": label, "taxonomy_value": tv}
        for t, values in content.ATTRIBUTE_VALUES.items()
        for h, (label, tv) in values.items() if (t, h) in used
    ]
    plan = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot": snapshot_path,
        "snapshot_taken_at": snapshot["taken_at"],
        "attribute_definitions": [
            {"metaobject_type": t, "metafield_key": k}
            for t, k in content.ATTRIBUTE_METAFIELD_KEYS.items()
        ],
        "attribute_values": attribute_values,
        "products": products,
        "hidden_products": hidden,
        "collections": collections,
        "warnings": warnings,
    }
    plan["summary"] = summarize(plan)
    return plan


def summarize(plan):
    ps = plan["products"]
    return {
        "products_with_changes": sum(1 for p in ps if p["update"] or p["metafields"]
                                     or p["tags_add"] or p["tags_remove"]),
        "seo_rewrites": sum(1 for p in ps if "seo" in p["update"]),
        "category_fixes": sum(1 for p in ps if "category" in p["update"]),
        "product_type_fixes": sum(1 for p in ps if "productType" in p["update"]),
        "description_fixes": sum(1 for p in ps if "descriptionHtml" in p["update"]),
        "tag_changes": sum(len(p["tags_add"]) + len(p["tags_remove"]) for p in ps),
        "metafield_fixes": sum(len(p["metafields"]) for p in ps),
        "faq_entries": sum(len(p["faqs"]) for p in ps),
        "products_with_attributes": sum(1 for p in ps if p["attributes"]),
        "hidden_products_to_noindex": len(plan["hidden_products"]),
        "collections_with_changes": sum(1 for c in plan["collections"]
                                        if c["update"] or c["metafields"]),
    }


def render_review(plan, snapshot):
    """Human-readable before/after of everything in the plan (cone_art/plan.md)."""
    def cell(text):
        return (text or "—").replace("|", "\\|").replace("\n", " ")

    out = ["# Cone Art SEO / agentic plan — review", "",
           f"Generated {plan['generated_at']} from the snapshot taken {plan['snapshot_taken_at']}.",
           "Nothing here is live until `python3 scripts/cone_art_seo.py apply --execute` runs.", "",
           "## Summary", ""]
    out += [f"- {k.replace('_', ' ')}: **{v}**" for k, v in plan["summary"].items()]
    out += ["", "## Product SEO titles and meta descriptions", "",
            "| Product | Before | After |", "|---|---|---|"]
    for p in plan["products"]:
        before = snapshot["products"][p["id"]]["seo"]
        after = p["update"].get("seo")
        if after:
            out.append(f"| {cell(p['title'])} | **{cell(before['title'])}**<br>{cell(before['description'])} "
                       f"| **{cell(after['title'])}** ({len(after['title'])})<br>{cell(after['description'])} "
                       f"({len(after['description'])}) |")
    out += ["", "## Other product changes", ""]
    for p in plan["products"]:
        before = snapshot["products"][p["id"]]
        lines = []
        if "category" in p["update"]:
            lines.append(f"category `{before['category']}` → `{p['update']['category']}`")
        if "productType" in p["update"]:
            lines.append(f"product type `{before['productType']}` → `{p['update']['productType']}`")
        if "descriptionHtml" in p["update"]:
            legacy = p["id"].rsplit("/", 1)[-1]
            for fix in content.DESCRIPTION_FIXES.get(legacy, []):
                lines.append(f"description: `{cell(fix[0])}` → `{cell(fix[1])}`")
        for t in p["tags_remove"]:
            lines.append(f"remove tag `{t}`")
        for t in p["tags_add"]:
            lines.append(f"add tag `{t}`")
        for m in p["metafields"]:
            old = (before["metafields"].get(f"{m['namespace']}.{m['key']}") or {}).get("value")
            if m["key"] == "specifications":
                legacy = p["id"].rsplit("/", 1)[-1]
                fixes = "; ".join(f"`{cell(f[0])}` → `{cell(f[1])}`" for f in content.SPEC_FIXES[legacy])
                lines.append(f"spec table: {fixes}")
            else:
                lines.append(f"`{m['namespace']}.{m['key']}`: `{cell(old)}` → `{cell(m['value'])}`")
        if lines:
            out.append(f"**{p['title']}**")
            out += [f"- {line}" for line in lines]
            out.append("")
    out += ["## Product FAQs (visible on the page + FAQPage structured data)", ""]
    for p in plan["products"]:
        out.append(f"<details><summary>{p['title']} — {len(p['faqs'])} questions</summary>")
        out.append("")
        for f in p["faqs"]:
            out += [f"- **{f['question']}**  ", f"  {f['answer']}"]
        out += ["", "</details>", ""]
    out += ["## Category attributes (Shopify standard taxonomy)", "",
            "| Product | Shape | Kiln features |", "|---|---|---|"]
    for p in plan["products"]:
        if p["attributes"]:
            out.append(f"| {cell(p['title'])} | {', '.join(p['attributes']['shopify--shape'])} | "
                       f"{', '.join(p['attributes']['shopify--kiln-features'])} |")
    out += ["", "All kilns also get: loading style `top-loading`, firing atmosphere `oxidation`, "
            "heating element `kanthal-fecral-wire`, power source `ac-powered`.", "",
            f"## Hidden option products set to `seo.hidden = 1` ({len(plan['hidden_products'])})", ""]
    out += [f"- {h['title']}" for h in plan["hidden_products"]]
    out += ["", "## Collections", ""]
    for c in plan["collections"]:
        before = snapshot["collections"][c["id"]]
        out.append(f"**{c['title']}** (`/collections/{c['handle']}`)")
        if "seo" in c["update"]:
            out.append(f"- SEO title: `{cell(before['seo']['title'])}` → `{cell(c['update']['seo']['title'])}`")
            out.append(f"- Meta description: `{cell(before['seo']['description'])}` → "
                       f"`{cell(c['update']['seo']['description'])}`")
        if "descriptionHtml" in c["update"]:
            out.append("- Description rewritten (see `plan.json` for the full HTML)")
        if "ruleSet" in c["update"]:
            new_rules = [r for r in c["update"]["ruleSet"]["rules"] if r not in before["ruleSet"]["rules"]]
            out += [f"- Add smart-collection condition: {r['column']} {r['relation']} `{r['condition']}`"
                    for r in new_rules]
        for m in c["metafields"]:
            out.append(f"- Set `{m['namespace']}.{m['key']}`")
        out.append("")
    if plan["warnings"]:
        out += ["## Warnings", ""] + [f"- {w}" for w in plan["warnings"]]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# GraphQL operations
# --------------------------------------------------------------------------
def _batched(op_name, var_type, call, selection, values, size):
    """Yield (query, variables) with up to `size` aliased calls per request."""
    for start in range(0, len(values), size):
        chunk = values[start:start + size]
        defs = ", ".join(f"$v{i}: {var_type}" for i in range(len(chunk)))
        body = "\n".join(
            f"  m{i}: {call.format(v=f'$v{i}')} {selection}" for i in range(len(chunk)))
        yield (f"mutation {op_name}({defs}) {{\n{body}\n}}",
               {f"v{i}": v for i, v in enumerate(chunk)})


def metafields_set_ops(metafields, label):
    chunks = [metafields[i:i + 25] for i in range(0, len(metafields), 25)]
    for query, variables in _batched(
            "MetafieldsSet", "[MetafieldsSetInput!]!", "metafieldsSet(metafields: {v})",
            "{ metafields { id } userErrors { field message code } }", chunks, 4):
        yield {"label": label, "query": query, "variables": variables}


def metafields_delete_ops(identifiers, label):
    chunks = [identifiers[i:i + 25] for i in range(0, len(identifiers), 25)]
    for query, variables in _batched(
            "MetafieldsDelete", "[MetafieldIdentifierInput!]!",
            "metafieldsDelete(metafields: {v})",
            "{ deletedMetafields { key } userErrors { field message } }", chunks, 4):
        yield {"label": label, "query": query, "variables": variables}


def upsert_ops(entries, label):
    """entries: [(type, handle, fields_dict, publishable_bool)]"""
    values = []
    for mtype, handle, fields, publishable in entries:
        mo = {"fields": [{"key": k, "value": v} for k, v in fields.items()]}
        if publishable:
            mo["capabilities"] = {"publishable": {"status": "ACTIVE"}}
        values.append({"handle": {"type": mtype, "handle": handle}, "metaobject": mo})
    for start in range(0, len(values), 25):
        chunk = values[start:start + 25]
        defs = ", ".join(f"$h{i}: MetaobjectHandleInput!, $m{i}: MetaobjectUpsertInput!"
                         for i in range(len(chunk)))
        body = "\n".join(
            f"  u{i}: metaobjectUpsert(handle: $h{i}, metaobject: $m{i}) "
            "{ metaobject { id handle type } userErrors { field message code } }"
            for i in range(len(chunk)))
        variables = {}
        for i, v in enumerate(chunk):
            variables[f"h{i}"] = v["handle"]
            variables[f"m{i}"] = v["metaobject"]
        yield {"label": label, "query": f"mutation MetaobjectUpsert({defs}) {{\n{body}\n}}",
               "variables": variables}


def ref(mtype, handle):
    """Placeholder for a metaobject GID that is only known after upsert."""
    return f"$ref:{mtype}/{handle}"


def apply_ops(plan):
    """Every write `apply` performs, in order. Metaobject GIDs appear as $ref placeholders."""
    ops = []
    # 1. standard category attributes: definitions + values
    for d in plan["attribute_definitions"]:
        ops.append({"label": f"enable metaobject type {d['metaobject_type']}",
                    "query": "mutation EnableType($type: String!) { standardMetaobjectDefinitionEnable(type: $type) "
                             "{ metaobjectDefinition { id } userErrors { field message code } } }",
                    "variables": {"type": d["metaobject_type"]}, "tolerate": ALREADY_ENABLED})
        ops.append({"label": f"enable metafield shopify.{d['metafield_key']}",
                    "query": "mutation EnableMetafield($key: String!) { standardMetafieldDefinitionEnable("
                             "ownerType: PRODUCT, namespace: \"shopify\", key: $key, pin: false) "
                             "{ createdDefinition { id } userErrors { field message code } } }",
                    "variables": {"key": d["metafield_key"]}, "tolerate": ALREADY_ENABLED})
    ops.extend(upsert_ops(
        [(v["type"], v["handle"], {"label": v["label"], "taxonomy_reference": v["taxonomy_value"]}, False)
         for v in plan["attribute_values"]], "attribute values"))

    # 2. product fields
    updates = [dict(p["update"], id=p["id"]) for p in plan["products"] if p["update"]]
    for query, variables in _batched(
            "ProductUpdate", "ProductUpdateInput!", "productUpdate(product: {v})",
            "{ product { id } userErrors { field message } }", updates, 10):
        ops.append({"label": "product SEO/category/type/description", "query": query,
                    "variables": variables})
    for p in plan["products"]:
        if p["tags_remove"]:
            ops.append({"label": f"tags remove: {p['title']}",
                        "query": "mutation TagsRemove($id: ID!, $tags: [String!]!) { m: tagsRemove(id: $id, tags: $tags) "
                                 "{ userErrors { field message } } }",
                        "variables": {"id": p["id"], "tags": p["tags_remove"]}})
        if p["tags_add"]:
            ops.append({"label": f"tags add: {p['title']}",
                        "query": "mutation TagsAdd($id: ID!, $tags: [String!]!) { m: tagsAdd(id: $id, tags: $tags) "
                                 "{ userErrors { field message } } }",
                        "variables": {"id": p["id"], "tags": p["tags_add"]}})
    fixes = [dict(m, ownerId=p["id"]) for p in plan["products"] for m in p["metafields"]]
    ops.extend(metafields_set_ops(fixes, "product metafield fixes"))

    # 3. FAQs: metaobjects, then the two product metafields that point at them
    ops.extend(upsert_ops(
        [(FAQ_TYPE, f["handle"], {"question": f["question"], "answer": rich_text(f["answer"]),
                                  "open_by_default": "false"}, True)
         for p in plan["products"] for f in p["faqs"]], "FAQ metaobjects"))
    faq_mfs = []
    for p in plan["products"]:
        if not p["faqs"]:
            continue
        faq_mfs.append({"ownerId": p["id"], "namespace": "custom", "key": "product_faqs",
                        "type": "list.metaobject_reference",
                        "value": json.dumps([ref(FAQ_TYPE, f["handle"]) for f in p["faqs"]])})
        faq_mfs.append({"ownerId": p["id"], "namespace": "custom", "key": "faqs", "type": "json",
                        "value": json.dumps([{"question": f["question"], "answer": f["answer"]}
                                             for f in p["faqs"]])})
    ops.extend(metafields_set_ops(faq_mfs, "product FAQ metafields"))

    # 4. category attribute metafields
    attr_mfs = [
        {"ownerId": p["id"], "namespace": "shopify",
         "key": content.ATTRIBUTE_METAFIELD_KEYS[mtype], "type": "list.metaobject_reference",
         "value": json.dumps([ref(mtype, h) for h in handles])}
        for p in plan["products"] for mtype, handles in p["attributes"].items()
    ]
    ops.extend(metafields_set_ops(attr_mfs, "product category attributes"))

    # 5. keep hidden option products out of search engines and search
    ops.extend(metafields_set_ops(
        [{"ownerId": h["id"], "namespace": "seo", "key": "hidden", "type": "number_integer",
          "value": "1"} for h in plan["hidden_products"]], "seo.hidden on option products"))

    # 6. collections
    for c in plan["collections"]:
        if c["update"]:
            ops.append({"label": f"collection {c['handle']}",
                        "query": "mutation CollectionUpdate($input: CollectionInput!) { m: collectionUpdate(input: $input) "
                                 "{ collection { id } userErrors { field message } } }",
                        "variables": {"input": dict(c["update"], id=c["id"])}})
    ops.extend(metafields_set_ops(
        [dict(m, ownerId=c["id"]) for c in plan["collections"] for m in c["metafields"]],
        "collection metafields"))
    return ops


def resolve_refs(variables, resolver):
    """Replace $ref placeholders (also inside JSON-encoded metafield values)."""
    text = json.dumps(variables)
    if "$ref:" not in text:
        return variables

    def swap(value):
        if isinstance(value, str) and value.startswith("["):
            try:
                items = json.loads(value)
            except ValueError:
                return value
            if isinstance(items, list) and any(isinstance(i, str) and i.startswith("$ref:") for i in items):
                return json.dumps([resolver(i[5:]) if isinstance(i, str) and i.startswith("$ref:") else i
                                   for i in items])
        if isinstance(value, dict):
            return {k: swap(v) for k, v in value.items()}
        if isinstance(value, list):
            return [swap(v) for v in value]
        return value

    return swap(variables)


def execute(domain, token, ops):
    known = {}

    def resolver(key):
        if key not in known:
            mtype, handle = key.split("/", 1)
            data = shopify_graphql(domain, token, METAOBJECT_BY_HANDLE_QUERY,
                                   {"h": {"type": mtype, "handle": handle}})
            if not data["metaobjectByHandle"]:
                raise SystemExit(f"Metaobject {key} not found; run the earlier upsert step first.")
            known[key] = data["metaobjectByHandle"]["id"]
        return known[key]

    for n, op in enumerate(ops, start=1):
        variables = resolve_refs(op["variables"], resolver)
        data = shopify_graphql(domain, token, op["query"], variables)
        for alias, payload in (data or {}).items():
            for key in ("metaobject",):
                mo = (payload or {}).get(key)
                if mo:
                    known[f"{mo['type']}/{mo['handle']}"] = mo["id"]
        errors = user_errors(data)
        tolerated = [e for e in errors if any(code in e for code in op.get("tolerate", []))]
        errors = [e for e in errors if e not in tolerated]
        status = "ok" if not errors else "ERRORS"
        print(f"[{n}/{len(ops)}] {op['label']}: {status}")
        for e in errors:
            print(f"    {e}", file=sys.stderr)
        if errors:
            raise SystemExit("Stopping on first error; fix it and re-run (every step is idempotent).")


# --------------------------------------------------------------------------
# Rollback
# --------------------------------------------------------------------------
def rollback_ops(plan, snapshot):
    ops = []
    restore_mfs, delete_mfs = [], []

    def restore(owner, before, ns, key):
        entry = before["metafields"].get(f"{ns}.{key}")
        if entry:
            restore_mfs.append({"ownerId": owner, "namespace": ns, "key": key,
                                "type": entry["type"], "value": entry["value"]})
        else:
            delete_mfs.append({"ownerId": owner, "namespace": ns, "key": key})

    updates = []
    for p in plan["products"]:
        before = snapshot["products"][p["id"]]
        if p["update"]:
            update = {"id": p["id"]}
            for field in p["update"]:
                update[field] = before[field] if field != "category" else before["category"]
            updates.append(update)
        if p["tags_remove"]:
            ops.append({"label": f"restore tags: {p['title']}",
                        "query": "mutation TagsAdd($id: ID!, $tags: [String!]!) { m: tagsAdd(id: $id, tags: $tags) "
                                 "{ userErrors { field message } } }",
                        "variables": {"id": p["id"], "tags": p["tags_remove"]}})
        if p["tags_add"]:
            ops.append({"label": f"remove added tags: {p['title']}",
                        "query": "mutation TagsRemove($id: ID!, $tags: [String!]!) { m: tagsRemove(id: $id, tags: $tags) "
                                 "{ userErrors { field message } } }",
                        "variables": {"id": p["id"], "tags": p["tags_add"]}})
        touched = {(m["namespace"], m["key"]) for m in p["metafields"]}
        if p["faqs"]:
            touched |= {("custom", "product_faqs"), ("custom", "faqs")}
        touched |= {("shopify", content.ATTRIBUTE_METAFIELD_KEYS[t]) for t in p["attributes"]}
        for ns, key in sorted(touched):
            restore(p["id"], before, ns, key)
    for query, variables in _batched(
            "ProductUpdate", "ProductUpdateInput!", "productUpdate(product: {v})",
            "{ product { id } userErrors { field message } }", updates, 10):
        ops.insert(0, {"label": "restore product fields", "query": query, "variables": variables})
    for h in plan["hidden_products"]:
        restore(h["id"], snapshot["products"][h["id"]], "seo", "hidden")
    for c in plan["collections"]:
        before = snapshot["collections"][c["id"]]
        if c["update"]:
            update = {"id": c["id"]}
            for field in c["update"]:
                update[field] = before[field]
            ops.append({"label": f"restore collection {c['handle']}",
                        "query": "mutation CollectionUpdate($input: CollectionInput!) { m: collectionUpdate(input: $input) "
                                 "{ collection { id } userErrors { field message } } }",
                        "variables": {"input": update}})
        for m in c["metafields"]:
            restore(c["id"], before, m["namespace"], m["key"])
    ops.extend(metafields_set_ops(restore_mfs, "restore metafields"))
    ops.extend(metafields_delete_ops(delete_mfs, "delete added metafields"))
    for p in plan["products"]:
        for f in p["faqs"]:
            ops.append({"label": f"delete FAQ {f['handle']}", "delete_metaobject": [FAQ_TYPE, f["handle"]]})
    return ops


def execute_rollback(domain, token, ops):
    for n, op in enumerate(ops, start=1):
        if "delete_metaobject" in op:
            mtype, handle = op["delete_metaobject"]
            data = shopify_graphql(domain, token, METAOBJECT_BY_HANDLE_QUERY,
                                   {"h": {"type": mtype, "handle": handle}})
            if not data["metaobjectByHandle"]:
                print(f"[{n}/{len(ops)}] {op['label']}: already gone")
                continue
            data = shopify_graphql(
                domain, token,
                "mutation Del($id: ID!) { m: metaobjectDelete(id: $id) { deletedId userErrors { field message } } }",
                {"id": data["metaobjectByHandle"]["id"]})
        else:
            data = shopify_graphql(domain, token, op["query"], op["variables"])
        errors = user_errors(data)
        print(f"[{n}/{len(ops)}] {op['label']}: {'ok' if not errors else 'ERRORS'}")
        for e in errors:
            print(f"    {e}", file=sys.stderr)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(obj, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")


def describe(ops):
    for n, op in enumerate(ops, start=1):
        count = len([k for k in op.get("variables", {}) if k.startswith(("v", "m"))]) or 1
        print(f"[{n}/{len(ops)}] {op['label']} ({count} call{'s' if count > 1 else ''})")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_snap = sub.add_parser("snapshot", help="save the current state of every field this tool touches")
    p_snap.add_argument("--out", default=DEFAULT_SNAPSHOT)
    p_snap.add_argument("--from-export", nargs=2, metavar=("PRODUCTS_JSON", "COLLECTIONS_JSON"),
                        help="build the snapshot from saved GraphQL output instead of the API")

    p_plan = sub.add_parser("plan", help="build the change plan from a snapshot (offline)")
    p_plan.add_argument("--snapshot", default=DEFAULT_SNAPSHOT)
    p_plan.add_argument("--out", default=DEFAULT_PLAN)

    p_apply = sub.add_parser("apply", help="apply the plan (dry run unless --execute)")
    p_apply.add_argument("--plan", default=DEFAULT_PLAN)
    p_apply.add_argument("--execute", action="store_true")

    p_rb = sub.add_parser("rollback", help="restore the snapshot (dry run unless --execute)")
    p_rb.add_argument("--plan", default=DEFAULT_PLAN)
    p_rb.add_argument("--snapshot", default=DEFAULT_SNAPSHOT)
    p_rb.add_argument("--execute", action="store_true")

    p_exp = sub.add_parser("export", help="write the GraphQL operations apply would run")
    p_exp.add_argument("--plan", default=DEFAULT_PLAN)
    p_exp.add_argument("--out", default=DEFAULT_OPS)

    args = parser.parse_args()

    if args.command == "snapshot":
        if args.from_export:
            products = _nodes(load(args.from_export[0]))
            wanted = set(content.COLLECTIONS)
            collections = [c for c in _nodes(load(args.from_export[1])) if c["id"] in wanted]
        else:
            products, collections = fetch_snapshot(*credentials())
        snapshot = build_snapshot(products, collections)
        save(snapshot, args.out)
        print(f"Saved {len(snapshot['products'])} products and {len(snapshot['collections'])} "
              f"collections to {args.out}")
    elif args.command == "plan":
        snapshot = load(args.snapshot)
        plan = build_plan(snapshot, args.snapshot)
        save(plan, args.out)
        review = os.path.splitext(args.out)[0] + ".md"
        with open(review, "w", encoding="utf-8") as f:
            f.write(render_review(plan, snapshot))
        print(f"Wrote {args.out} and {review}")
        for k, v in plan["summary"].items():
            print(f"  {k}: {v}")
        for w in plan["warnings"]:
            print(f"WARNING: {w}", file=sys.stderr)
    elif args.command == "apply":
        ops = apply_ops(load(args.plan))
        if not args.execute:
            describe(ops)
            print("\nDry run only. Re-run with --execute to write these changes.")
            return
        execute(*credentials(), ops)
    elif args.command == "rollback":
        ops = rollback_ops(load(args.plan), load(args.snapshot))
        if not args.execute:
            describe(ops)
            print("\nDry run only. Re-run with --execute to restore the snapshot.")
            return
        execute_rollback(*credentials(), ops)
    elif args.command == "export":
        ops = apply_ops(load(args.plan))
        save(ops, args.out)
        print(f"Wrote {len(ops)} operations to {args.out}")


if __name__ == "__main__":
    main()
