#!/usr/bin/env python3
"""Build the "Skutt Kiln Full Set of Replacement Elements" Shopify product.

Source: Skutt Kilns Parts Price List, prices effective January 10, 2026
(revised 12/19/2025), "Elements" tables on pages 1-3.

Modeled on the existing "Cone Art Kiln Full Set of Replacement Elements"
product: one product, one variant per kiln model + voltage, priced as the
sum of Skutt's list price for every element in the kiln. Skutt also sells
APM (long-life) elements, so this product has a second option, Element
Type, with Standard and APM variants. APM variants are left out where
Skutt lists APM as "Call For Pricing".

Wired-ring (WR / -27) kilns: footnote 1 of the price list says they hold
2 more elements than the "Qty in Kiln" column shows (145 WR holds 1 more),
so they get their own variants with the extra elements counted.

Small-set surcharge: sets whose list total is $252 or less sell for $20
over list (SMALL_SET_MAX / SMALL_SET_SURCHARGE). The rule was "under $250",
widened to take in the $252 818-family sets. The CSV shows both the list
total and the selling price.

Outputs (both overwritten):
  data/skutt_element_sets_2026.csv      one row per variant, with the parts
  data/skutt_element_sets_2026.json     productSet input for the Admin API

Usage:
  python3 scripts/build_skutt_element_sets.py
"""

import csv
import json
import os
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CSV = os.path.join(ROOT, "data", "skutt_element_sets_2026.csv")
OUT_JSON = os.path.join(ROOT, "data", "skutt_element_sets_2026.json")

OPT_MODEL = "Kiln Model and Voltage"
OPT_TYPE = "Element Type"
STANDARD = "Standard"
APM = "APM (Long-Life)"

LB_PER_ELEMENT = Decimal("1.0")  # matches the store's single Skutt element weight

SMALL_SET_MAX = Decimal("252")       # list totals at or below this...
SMALL_SET_SURCHARGE = Decimal("20")  # ...sell for this much over list


def sell_price(list_total):
    if list_total <= SMALL_SET_MAX:
        return list_total + SMALL_SET_SURCHARGE
    return list_total

# Element locations as printed on the price list.
TB, INT, CTR, ALL = "top/bottom", "intermediate", "center", "all"


def e(loc, qty, std_part, std_price, apm_part=None, apm_price=None):
    return {
        "loc": loc,
        "qty": qty,
        "std_part": std_part,
        "std_price": Decimal(std_price),
        "apm_part": apm_part,
        "apm_price": Decimal(apm_price) if apm_price else None,
    }


def cfg(voltage, sku_suffix, elements):
    return {"voltage": voltage, "sku_suffix": sku_suffix, "elements": elements}


# Voltage labels shown to shoppers.
V240_1 = "240V 1-Phase"
V240_3 = "240V 3-Phase"
V240_13 = "240V 1 or 3-Phase"
V208_1 = "208V 1-Phase"
V208_3 = "208V 3-Phase"
V208_13 = "208V 1 or 3-Phase"
V208_240 = "208V or 240V 1-Phase"
V240 = "240V"
V208 = "208V"
V120 = "120V"

GROUP_PK = "Skutt PK production kilns"
GROUP_TEN_TWELVE = "Skutt 12-sided and 10-sided kilns"
GROUP_EIGHT = "Skutt 8-sided and smaller kilns"
GROUP_OLD = "Older KilnSitter and wired-ring (WR) kilns"
GROUP_OTHER = "Skutt GlazeTech and FireBox kilns"

# fmt: off
KILNS = [
    # ---------------- Page 1 ----------------
    {"model": "KMT/KM1627-3 PK", "code": "16273PK", "group": GROUP_PK, "configs": [
        cfg(V240_3, "240-3", [e(TB, 4, "0409", "65", "1692", "168"), e(INT, 4, "0410", "65", "1693", "168"), e(CTR, 4, "0411", "65", "1694", "168")]),
        cfg(V208_3, "208-3", [e(TB, 4, "0406", "65", "1695", "168"), e(INT, 4, "0407", "65", "1696", "168"), e(CTR, 4, "0408", "65", "1697", "168")]),
    ]},
    {"model": "KMT/KM1627-3 PK-LF", "code": "16273PKLF", "group": GROUP_PK, "configs": [
        cfg(V240_13, "240", [e(TB, 4, "2540", "65", "1698", "168"), e(INT, 4, "2541", "65", "1699", "168"), e(CTR, 4, "2542", "65", "1700", "168")]),
        cfg(V208_13, "208", [e(TB, 4, "2543", "65", "1661", "168"), e(INT, 4, "2544", "65", "1662", "168"), e(CTR, 4, "2545", "65", "1663", "168")]),
    ]},
    {"model": "KMT/KM1231-3 PK", "code": "12313PK", "group": GROUP_PK, "configs": [
        cfg(V240_1, "240-1", [e(TB, 2, "1429", "74", "1664", "185"), e(INT, 2, "1430", "74", "1665", "185"), e(CTR, 3, "1431", "74", "1666", "185")]),
        cfg(V208_1, "208-1", [e(TB, 2, "1432", "74", "1667", "185"), e(INT, 2, "1433", "74", "1669", "185"), e(CTR, 3, "1434", "74", "1668", "185")]),
        cfg(V240_3, "240-3", [e(TB, 2, "1435", "74", "1664", "185"), e(INT, 2, "1436", "74", "1665", "185"), e(CTR, 3, "1437", "74", "1666", "185")]),
        cfg(V208_3, "208-3", [e(TB, 2, "1438", "74", "1667", "185"), e(INT, 2, "1439", "74", "1669", "185"), e(CTR, 3, "1440", "74", "1668", "185")]),
    ]},
    # ---------------- Page 2 ----------------
    {"model": "KMT/KM1227-3 PK", "code": "12273PK", "group": GROUP_PK, "configs": [
        cfg(V240_1, "240-1", [e(TB, 2, "1441", "74", "1640", "185"), e(INT, 2, "1442", "74", "1641", "185"), e(CTR, 2, "1443", "74", "1642", "185")]),
        cfg(V208_1, "208-1", [e(TB, 2, "1548", "74", "1658", "185"), e(INT, 2, "1549", "74", "1659", "185"), e(CTR, 2, "1550", "74", "1660", "185")]),
        cfg(V240_3, "240-3", [e(TB, 2, "1444", "74", "1640", "185"), e(INT, 2, "1445", "74", "1641", "185"), e(CTR, 2, "1446", "74", "1642", "185")]),
        cfg(V208_3, "208-3", [e(TB, 2, "1447", "74", "1658", "185"), e(INT, 2, "1448", "74", "1659", "185"), e(CTR, 2, "1449", "74", "1660", "185")]),
    ]},
    {"model": "KMT/KM1227-3, KS1227-3, 280-3", "code": "12273", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "1368", "74", "1654", "185"), e(CTR, 4, "1370", "74", "1655", "185")]),
        cfg(V208_1, "208-1", [e(TB, 2, "1369", "74", "1650", "185"), e(CTR, 4, "1371", "74", "1651", "185")]),
        cfg(V208_3, "208-3", [e(TB, 2, "1369", "74", "1650", "185"), e(CTR, 4, "1391", "74", "1687", "185")]),
    ]},
    {"model": "KMT/KM1027, KS1027, 230, 231, 235", "code": "1027", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "0171", "74", "1656", "185"), e(CTR, 4, "0172", "74", "1657", "185")]),
        cfg(V208_1, "208-1", [e(TB, 2, "1372", "74", "1671", "185"), e(CTR, 4, "1375", "74", "2742", "185")]),
        cfg(V208_3, "208-3", [e(TB, 2, "1372", "74", "1671", "185"), e(CTR, 4, "1392", "74", "1672", "185")]),
    ]},
    {"model": "KMT/KM1027-3, KS1027-3", "code": "10273", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "1373", "74", "1684", "185"), e(CTR, 4, "1376", "74", "1685", "185")]),
        cfg(V208_1, "208-1", [e(TB, 2, "1374", "74", "1649", "185"), e(CTR, 4, "1377", "74", "2743", "185")]),
        cfg(V208_3, "208-3", [e(TB, 2, "1374", "74", "1649", "185"), e(CTR, 4, "1393", "74", "2744", "185")]),
    ]},
    {"model": "KMT/KM1222-3", "code": "12223", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "3266", "74", "3271", "185"), e(CTR, 3, "3267", "74", "3272", "185")]),
        cfg(V208_1, "208-1", [e(TB, 2, "3268", "74", "3273", "185"), e(CTR, 3, "3269", "74", "3274", "185")]),
        cfg(V208_3, "208-3", [e(TB, 2, "3270", "74", "3275", "185"), e(CTR, 3, "3249", "74", "3349", "185")]),
    ]},
    {"model": "KMT/KM1022", "code": "1022", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "3258", "74", "3276", "185"), e(CTR, 3, "3259", "74", "3277", "185")]),
        cfg(V208_13, "208", [e(TB, 2, "3260", "74", "3278", "185"), e(CTR, 3, "3261", "74", "3279", "185")]),
    ]},
    {"model": "KMT/KM1022-3", "code": "10223", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "3262", "74", "3280", "185"), e(CTR, 3, "3263", "74", "3281", "185")]),
        cfg(V208_13, "208", [e(TB, 2, "3264", "74", "3282", "185"), e(CTR, 3, "3265", "74", "3283", "185")]),
    ]},
    {"model": "KMT/KM822", "code": "822", "group": GROUP_EIGHT, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "3250", "63", "3284", "150"), e(CTR, 3, "3251", "63", "3285", "150")]),
        cfg(V208_1, "208", [e(TB, 2, "3252", "63", "3286", "150"), e(CTR, 3, "3253", "63", "3287", "150")]),
    ]},
    {"model": "KMT/KM822-3", "code": "8223", "group": GROUP_EIGHT, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "3254", "63", "3288", "150"), e(CTR, 3, "3255", "63", "3289", "150")]),
        cfg(V208_1, "208", [e(TB, 2, "3256", "63", "3290", "150"), e(CTR, 3, "3257", "63", "3291", "150")]),
    ]},
    # ---------------- Page 3 ----------------
    # Note: APM #2721 is printed at $170.00; every other 12/10-sided APM is $185.00.
    {"model": "KMT/KM1218-3", "code": "12183", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_13, "240", [e(TB, 2, "2550", "74", "2719", "185"), e(CTR, 2, "2551", "74", "2720", "185")]),
        cfg(V208_13, "208", [e(TB, 2, "2552", "74", "2721", "170"), e(CTR, 2, "2553", "74", "2722", "185")]),
    ]},
    {"model": "KMT/KM1018, KS1018, 231-18", "code": "1018", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "0176", "74", "2725", "185"), e(CTR, 2, "0177", "74", "2726", "185")]),
        cfg(V208_1, "208", [e(TB, 2, "0295", "74", "1673", "185"), e(CTR, 2, "0296", "74", "1674", "185")]),
    ]},
    {"model": "KMT/KM1018-3, KS1018-3", "code": "10183", "group": GROUP_TEN_TWELVE, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "1378", "74", "2727", "185"), e(CTR, 2, "1380", "74", "2728", "185")]),
        cfg(V208_1, "208", [e(TB, 2, "1379", "74", "1675", "185"), e(CTR, 2, "1381", "74", "1676", "185")]),
    ]},
    {"model": "KMT/KM818, KS818", "code": "818", "group": GROUP_EIGHT, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "1540", "63", "2700", "150"), e(CTR, 2, "1541", "63", "2701", "150")]),
        cfg(V208_1, "208", [e(TB, 2, "1542", "63", "1678", "150"), e(CTR, 2, "1543", "63", "1679", "150")]),
    ]},
    {"model": "KMT/KM818-3, KS818-3", "code": "8183", "group": GROUP_EIGHT, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "1544", "63", "2723", "150"), e(CTR, 2, "1545", "63", "2724", "150")]),
        cfg(V208_1, "208", [e(TB, 2, "1546", "63", "1689", "150"), e(CTR, 2, "1547", "63", "1690", "150")]),
    ]},
    # APM: Call For Pricing -> standard only.
    {"model": "KMT/KM818-3 30 Amp, KS818P-3", "code": "8183P", "group": GROUP_EIGHT, "configs": [
        cfg(V240_1, "240", [e(TB, 2, "1552", "63"), e(CTR, 2, "1553", "63")]),
        cfg(V208_1, "208", [e(TB, 2, "1554", "63"), e(CTR, 2, "1555", "63")]),
    ]},
    {"model": "818, 185 (old style)", "code": "818OS", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 4, "0269", "63")]),
        cfg(V208_1, "208", [e(ALL, 4, "0318", "63")]),
    ]},
    {"model": "KS818WR, 181-27 (wired ring)", "code": "818WR", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 6, "0269", "63")]),
        cfg(V208_1, "208", [e(ALL, 6, "0318", "63")]),
    ]},
    {"model": "818-3 (old style)", "code": "8183OS", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 4, "1386", "63")]),
        cfg(V208_1, "208", [e(ALL, 4, "1387", "63")]),
    ]},
    {"model": "KS818-3 WR (wired ring)", "code": "8183WR", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 6, "1386", "63")]),
        cfg(V208_1, "208", [e(ALL, 6, "1387", "63")]),
    ]},
    {"model": "KS818P, 183", "code": "818P", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 4, "0272", "63")]),
        cfg(V208_1, "208", [e(ALL, 4, "1382", "63")]),
    ]},
    {"model": "KS818P WR, 183-27 (wired ring)", "code": "818PWR", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 6, "0272", "63")]),
        cfg(V208_1, "208", [e(ALL, 6, "1382", "63")]),
    ]},
    {"model": "KS818P-3 WR (wired ring)", "code": "8183PWR", "group": GROUP_OLD, "configs": [
        cfg(V240_1, "240", [e(ALL, 6, "1388", "63")]),
        cfg(V208_1, "208", [e(ALL, 6, "1389", "63")]),
    ]},
    {"model": "181, 180", "code": "181", "group": GROUP_OLD, "configs": [
        cfg(V208_240, "208240", [e(ALL, 4, "1383", "63")]),
    ]},
    {"model": "KMT/KM714, KS714, 145", "code": "714", "group": GROUP_EIGHT, "configs": [
        cfg(V208_240, "208240", [e(ALL, 3, "0472", "52", "1677", "130")]),
    ]},
    {"model": "145 WR (wired ring)", "code": "145WR", "group": GROUP_OLD, "configs": [
        cfg(V208_240, "208240", [e(ALL, 4, "0472", "52", "1677", "130")]),
    ]},
    {"model": "KMT/KM614-3, KS614-3", "code": "6143", "group": GROUP_EIGHT, "configs": [
        cfg(V120, "120", [e(ALL, 3, "1029", "52", "2642", "130")]),
    ]},
    {"model": "KS609", "code": "609", "group": GROUP_EIGHT, "configs": [
        cfg(V120, "120", [e(ALL, 2, "0340", "52", "1688", "130")]),
    ]},
    {"model": "GlazeTech", "code": "GT", "group": GROUP_OTHER, "configs": [
        cfg(V240, "240", [e(ALL, 4, "3021", "41", "3186", "80")]),
        cfg(V208, "208", [e(ALL, 4, "3022", "41", "3187", "80")]),
    ]},
    {"model": "FireBox 8x4, FireBox 8x6", "code": "FB8", "group": GROUP_OTHER, "configs": [
        cfg(V120, "120", [e(ALL, 2, "0910", "41")]),
    ]},
]
# fmt: on

GROUP_ORDER = [GROUP_PK, GROUP_TEN_TWELVE, GROUP_EIGHT, GROUP_OLD, GROUP_OTHER]


def option_value(kiln, c):
    return f"{kiln['model']} – {c['voltage']}"


def describe(elements, part_key):
    """'2 top/bottom #1429, 2 intermediate #1430, 3 center #1431'."""
    bits = []
    for el in elements:
        loc = "elements" if el["loc"] == ALL else el["loc"]
        bits.append(f"{el['qty']} {loc} #{el[part_key]}")
    return ", ".join(bits)


def build_variants():
    rows = []
    for kiln in KILNS:
        for c in kiln["configs"]:
            els = c["elements"]
            qty = sum(el["qty"] for el in els)
            base_sku = f"SK{kiln['code']}FSE-{c['sku_suffix']}"
            std_total = sum(el["qty"] * el["std_price"] for el in els)
            rows.append({
                "model": kiln["model"], "group": kiln["group"], "voltage": c["voltage"],
                "option_value": option_value(kiln, c), "element_type": STANDARD,
                "sku": base_sku, "elements": qty,
                "list_total": std_total, "price": sell_price(std_total),
                "parts": describe(els, "std_part"),
            })
            if all(el["apm_part"] for el in els):
                apm_total = sum(el["qty"] * el["apm_price"] for el in els)
                rows.append({
                    "model": kiln["model"], "group": kiln["group"], "voltage": c["voltage"],
                    "option_value": option_value(kiln, c), "element_type": APM,
                    "sku": f"{base_sku}-APM", "elements": qty,
                    "list_total": apm_total, "price": sell_price(apm_total),
                    "parts": describe(els, "apm_part"),
                })
    return rows


def description_html():
    out = [
        '<h2 class="abz-seo-product">Skutt Kiln Full Set of Replacement Elements</h2>',
        "<p>A complete set of replacement heating elements for Skutt KM, KMT and KS "
        "(KilnSitter) pottery kilns. Choose your kiln model, voltage and phase to get "
        "every element your kiln needs in one order, in Skutt's standard elements or "
        "long-life APM elements.</p>",
        "<p><strong>Before you order:</strong></p>",
        "<ul>",
        "<li>Match the model, voltage and phase on your kiln's serial plate (on the "
        "control box). If you're not sure, send us the serial plate info or a photo "
        "with your order.</li>",
        "<li><strong>APM elements</strong> are engineered to last longer in kilns that "
        "fire to high temperatures with long hold times.</li>",
        "<li><strong>Wired-ring kilns</strong> (WR, and -27 on older models) have 2 extra "
        "elements, and the 145 WR has 1 extra. Those sets are listed separately and "
        "include the extra elements.</li>",
        "<li><strong>KS818, KS818-3 and KS818P-3:</strong> since October 1, 2017 these "
        "kilns use the same elements as the matching KM818 models. If your kiln was "
        "built before then and you're replacing ALL the elements, Skutt suggests the "
        "KM818 set. WR kilns and single-element replacements must use the old design.</li>",
        "</ul>",
    ]
    for group in GROUP_ORDER:
        out.append(f"<h3>{group}</h3>")
        out.append("<table>")
        out.append("<thead><tr><th>Kiln Model</th><th>Voltage</th>"
                   "<th>Elements in Set (Standard Part #)</th><th>APM Part #</th></tr></thead>")
        out.append("<tbody>")
        for kiln in KILNS:
            if kiln["group"] != group:
                continue
            for c in kiln["configs"]:
                els = c["elements"]
                apm = (describe(els, "apm_part") if all(el["apm_part"] for el in els)
                       else "Call for pricing")
                out.append(
                    f"<tr><td>{kiln['model']}</td><td>{c['voltage']}</td>"
                    f"<td>{describe(els, 'std_part')}</td><td>{apm}</td></tr>"
                )
        out.append("</tbody>")
        out.append("</table>")
    out.append('<h4 style="text-align: center;">Need a single element instead of a full set, '
               "or don't see your kiln model?<br>Call us toll free (888) 774-2529.</h4>")
    return "\n".join(out)


def compact(obj):
    """JSON the way Shopify stores rich-text metafields: compact, UTF-8."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def rich_text(text):
    return compact({"type": "root", "children": [
        {"type": "paragraph", "children": [{"type": "text", "value": text}]}]})


SEO_TITLE = "Skutt Kiln Replacement Element Sets | Sheffield Pottery"
SEO_DESC = ("Full replacement element sets for Skutt KM, KMT and KS kilns. Standard or "
            "long-life APM, every model, voltage and phase. Free shipping.")


def product_set_input(rows):
    option_values = []
    for r in rows:
        if r["option_value"] not in option_values:
            option_values.append(r["option_value"])
    type_values = [STANDARD, APM]

    # Copied from the Cone Art element-set product (shared help-desk widgets etc).
    metafields = [
        {"namespace": "global", "key": "SHIPPING_GROUPS", "type": "single_line_text_field", "value": "Free Shipping Item"},
        {"namespace": "custom", "key": "pdp_freeshippingitem", "type": "boolean", "value": "true"},
        {"namespace": "global", "key": "ORIGINS", "type": "single_line_text_field", "value": "Sheffield Pottery Inc"},
        {"namespace": "custom", "key": "pdp_under_price_short_desc", "type": "single_line_text_field", "value": "Kiln Parts"},
        {"namespace": "custom", "key": "pdp_categorytree", "type": "single_line_text_field", "value": "Equipment > Kiln and Pottery Wheel Replacements Parts"},
        {"namespace": "custom", "key": "pdp_product_short_desc", "type": "rich_text_field",
         "value": rich_text("Full replacement element sets for Skutt KM, KMT and KS kilns, in standard or long-life APM elements")},
        {"namespace": "custom", "key": "help_desk_meta", "type": "metaobject_reference", "value": "gid://shopify/Metaobject/252827992435"},
        {"namespace": "custom", "key": "helpdesk_img", "type": "file_reference", "value": "gid://shopify/MediaImage/54053224153459"},
        {"namespace": "custom", "key": "show_expert", "type": "rich_text_field",
         "value": compact({"type": "root", "children": [
             {"type": "heading", "children": [{"type": "text", "value": "Get questions answered fast & free. I'm here for you!", "bold": True}], "level": 4},
             {"type": "paragraph", "children": [{"type": "text", "value": "Expert Help | 400+ hours training | USA Based (EST)"}]}]})},
        {"namespace": "custom", "key": "show_expert_contact", "type": "rich_text_field",
         "value": compact({"type": "root", "children": [{"type": "paragraph", "children": [
             {"type": "text", "value": "📞"},
             {"url": "tel:1-888-774-2529", "type": "link", "children": [{"type": "text", "value": " 1-888-774-2529"}]},
             {"type": "text", "value": "    💬 Tim  ext. 220"}]}]})},
        {"namespace": "custom", "key": "pdp_availability", "type": "single_line_text_field", "value": "1-2 Weeks"},
        {"namespace": "shopify--discovery--product_recommendation", "key": "complementary_products",
         "type": "list.product_reference", "value": compact(["gid://shopify/Product/8312981455170"])},
    ]

    variants = []
    for i, r in enumerate(rows, start=1):
        variants.append({
            "optionValues": [
                {"optionName": OPT_MODEL, "name": r["option_value"]},
                {"optionName": OPT_TYPE, "name": r["element_type"]},
            ],
            "price": f"{r['price']:.2f}",
            "sku": r["sku"],
            "taxable": True,
            "inventoryPolicy": "CONTINUE",
            "position": i,
            "inventoryItem": {
                "tracked": False,
                "requiresShipping": True,
                "measurement": {"weight": {"value": float(r["elements"] * LB_PER_ELEMENT), "unit": "POUNDS"}},
            },
        })

    return {
        "title": "Skutt Kiln Full Set of Replacement Elements",
        "handle": "skutt-kiln-full-set-of-replacement-elements",
        "vendor": "Skutt",
        "productType": "Kiln Parts",
        "status": "DRAFT",
        "tags": ["Kiln and Pottery Wheel Replacements Parts", "Kiln Elements"],
        "category": "gid://shopify/TaxonomyCategory/ae-2-1-4-20",
        "descriptionHtml": description_html(),
        "seo": {"title": SEO_TITLE, "description": SEO_DESC},
        "metafields": metafields,
        "files": [{
            "originalSource": "https://cdn.shopify.com/s/files/1/0677/5508/2050/files/SK10273FSE-1_31564285-2b5f-4205-92e9-f711d03878b8.jpg?v=1791876098",
            "alt": "Skutt kiln full set of replacement heating elements",
            "contentType": "IMAGE",
        }],
        "productOptions": [
            {"name": OPT_MODEL, "position": 1, "values": [{"name": v} for v in option_values]},
            {"name": OPT_TYPE, "position": 2, "values": [{"name": v} for v in type_values]},
        ],
        "variants": variants,
    }


def main():
    rows = build_variants()
    skus = [r["sku"] for r in rows]
    assert len(skus) == len(set(skus)), "duplicate SKU"
    combos = [(r["option_value"], r["element_type"]) for r in rows]
    assert len(combos) == len(set(combos)), "duplicate option combination"

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Group", "Kiln Model", "Voltage", "Element Type", "SKU",
                    "Elements in Set", "Parts", "List Total", "Price"])
        for r in rows:
            w.writerow([r["group"], r["model"], r["voltage"], r["element_type"], r["sku"],
                        r["elements"], r["parts"], f"{r['list_total']:.2f}", f"{r['price']:.2f}"])
    with open(OUT_JSON, "w") as f:
        json.dump(product_set_input(rows), f, indent=2, ensure_ascii=False)
        f.write("\n")

    n_models = len({r["option_value"] for r in rows})
    n_apm = sum(r["element_type"] == APM for r in rows)
    print(f"{len(rows)} variants ({len(rows) - n_apm} standard, {n_apm} APM) "
          f"across {n_models} model/voltage choices")
    print(f"wrote {os.path.relpath(OUT_CSV, ROOT)} and {os.path.relpath(OUT_JSON, ROOT)}")


if __name__ == "__main__":
    main()
