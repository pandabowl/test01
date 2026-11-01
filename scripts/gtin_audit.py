#!/usr/bin/env python3
"""
Audit GTINs (UPC / EAN / ISBN barcodes) across every Shopify product variant
and say what to do about each gap.

Usage:
    export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
    export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx   # read_products scope
    python3 scripts/gtin_audit.py [--include-inactive]

Outputs (in feeds/ by default):
    gtin_audit.csv          one row per variant: sku, product, vendor, current
                            barcode, status, and the recommended action
    gtin_vendor_summary.csv one row per vendor: how many variants are missing
                            GTINs, so you can request barcode sheets vendor by
                            vendor

Why this doesn't "generate" GTINs:
    A GTIN is only valid if it was assigned by the brand owner under a GS1
    company prefix. Made-up or check-digit-correct-but-unlicensed numbers are
    rejected by Google Merchant Center (they're checked against GS1's
    registry) and can get the whole account flagged. So the script sorts
    variants into what each one actually needs:

      ok                 valid GTIN already on file
      fix_format         barcode present but wrong length / bad check digit
                         (often a UPC that lost its leading zero; the script
                         suggests the corrected value when padding fixes it)
      get_from_vendor    resold product with no barcode: the manufacturer
                         already has a GTIN; get it from their price list /
                         barcode sheet or the product packaging
      own_brand          a product Sheffield Pottery makes itself (clay,
                         glazes, slips...). Either license GTINs from GS1 US
                         and assign them, or submit to Google without one
                         (identifier_exists = no, with brand + MPN), which is
                         allowed when no GTIN was ever assigned
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict

API_VERSION = "2026-10"
OWN_BRAND_VENDORS = {"sheffield pottery", "sheffield pottery inc.", "sheffield pottery inc"}
GTIN_LENGTHS = {8, 12, 13, 14}

VARIANTS_QUERY = """
query Variants($cursor: String, $q: String) {
  productVariants(first: 250, after: $cursor, query: $q) {
    nodes {
      id
      sku
      title
      barcodes(first: 5) { nodes { type value } }
      product { id title vendor status handle }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def gtin_check_digit_ok(code):
    """GS1 mod-10 check digit, valid for GTIN-8/12/13/14."""
    if not code.isdigit() or len(code) not in GTIN_LENGTHS:
        return False
    digits = [int(c) for c in code]
    body, check = digits[:-1], digits[-1]
    total = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(body)))
    return (10 - total % 10) % 10 == check


def classify(barcode, vendor):
    """Return (status, suggested_gtin, action)."""
    code = (barcode or "").strip().replace(" ", "").replace("-", "")
    if code:
        if gtin_check_digit_ok(code):
            return "ok", code, ""
        # Commonly a UPC-A typed into a spreadsheet that dropped leading zeros.
        if code.isdigit() and len(code) >= 10:
            for length in (12, 13, 14):
                padded = code.zfill(length)
                if len(code) < length and gtin_check_digit_ok(padded):
                    return ("fix_format", padded,
                            f"Barcode '{code}' is invalid; '{padded}' passes the check digit. "
                            "Confirm against the packaging, then update.")
        return ("fix_format", "",
                f"Barcode '{code}' is not a valid GTIN. Replace it with the real one or clear it.")
    if (vendor or "").strip().lower() in OWN_BRAND_VENDORS:
        return ("own_brand", "",
                "Own product: license GTINs from GS1 US and assign one, "
                "or submit to Google with identifier_exists=no (brand + MPN).")
    return ("get_from_vendor", "",
            f"Get the GTIN from {vendor or 'the manufacturer'} (barcode sheet / packaging).")


def shopify_graphql(domain, token, query, variables):
    req = urllib.request.Request(
        f"https://{domain}/admin/api/{API_VERSION}/graphql.json",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"Shopify API error {e.code}: {e.read().decode(errors='replace')}")
    if payload.get("errors"):
        sys.exit(f"Shopify GraphQL errors: {payload['errors']}")
    return payload["data"]


def fetch_variants(domain, token, include_inactive):
    q = None if include_inactive else "product_status:active"
    cursor = None
    while True:
        data = shopify_graphql(domain, token, VARIANTS_QUERY, {"cursor": cursor, "q": q})
        conn = data["productVariants"]
        for v in conn["nodes"]:
            # Filter client-side too, in case the search filter is ignored.
            if include_inactive or v["product"]["status"] == "ACTIVE":
                yield v
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="feeds/gtin_audit.csv")
    ap.add_argument("--out-vendors", default="feeds/gtin_vendor_summary.csv")
    ap.add_argument("--include-inactive", action="store_true",
                    help="also audit draft/archived products (default: active only)")
    args = ap.parse_args()

    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not domain or not token:
        sys.exit("Set SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN.")

    rows = []
    for v in fetch_variants(domain, token, args.include_inactive):
        barcodes = v["barcodes"]["nodes"]
        current = barcodes[0]["value"] if barcodes else ""
        vendor = v["product"]["vendor"] or ""
        status, suggested, action = classify(current, vendor)
        rows.append({
            "status": status,
            "vendor": vendor,
            "sku": v["sku"] or "",
            "product_title": v["product"]["title"],
            "variant_title": "" if v["title"] == "Default Title" else v["title"],
            "current_barcode": current,
            "suggested_gtin": suggested,
            "action": action,
            "product_status": v["product"]["status"],
            "variant_id": v["id"],
            "product_url_handle": v["product"]["handle"],
        })

    rows.sort(key=lambda r: (r["status"] == "ok", r["vendor"].lower(), r["product_title"].lower()))
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["status"])
        w.writeheader()
        w.writerows(rows)

    by_vendor = defaultdict(Counter)
    for r in rows:
        by_vendor[r["vendor"]][r["status"]] += 1
    statuses = ["ok", "fix_format", "get_from_vendor", "own_brand"]
    with open(args.out_vendors, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vendor", "variants", "missing_or_invalid"] + statuses)
        for vendor, c in sorted(by_vendor.items(), key=lambda kv: -(sum(kv[1].values()) - kv[1]["ok"])):
            total = sum(c.values())
            w.writerow([vendor, total, total - c["ok"]] + [c[s] for s in statuses])

    totals = Counter(r["status"] for r in rows)
    print(f"Audited {len(rows)} variants")
    for s in statuses:
        print(f"  {s:16} {totals[s]}")
    print(f"Wrote {args.out} and {args.out_vendors}")


if __name__ == "__main__":
    main()
