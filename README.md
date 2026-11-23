# Google Merchant Center Promotions Feed

Generates and maintains Sheffield Pottery's [Google Merchant Center Promotions
feed](https://support.google.com/merchants/answer/2906014) from live Shopify
discount data.

## Contents

- `feeds/google_merchant_promotions.xlsx` — the filled-in Google Promotions
  template (same 9 columns as Google's official template), ready to review
  and upload via Google Sheets.
- `feeds/google_merchant_promotions.txt` — the same feed as a tab-separated
  file, for a scheduled fetch or manual upload in Merchant Center.
- `scripts/generate_promotions_feed.py` — regenerates both files from the
  Shopify Admin API.

## What's in the feed, and why

The feed currently lists Sheffield Pottery's two **active, automatic
(no-code)** Shopify discounts:

| Promotion | What it is |
|---|---|
| `TALISMAN_SIEVE_SCREEN` | Free replacement mesh screen with a Talisman Rotary Sieve purchase |
| `BTH_WHEEL_CLAY_DISCOUNT` | $45 off clay (4 bags at $11.25 off each) with a BTH Andromeda D3 Pottery Wheel purchase |

The store also has dozens of other "active" Shopify discount codes, but
almost all of them are individual customer-service courtesy codes (named
after specific customers, e.g. `adamfehr`, `angieriley`) or long-expired
seasonal codes. Those are **not public storefront promotions** and must
never be published to a public Google Shopping feed — so the generator
excludes code-based discounts by default and only picks up automatic
discounts, which by definition apply to every shopper at checkout.

If a real, publicly-advertised promo code should be added to the feed later,
add it explicitly — don't flip the generator to include all codes.

## Before you upload

1. **`specific_products` mapping.** Both current promotions target specific
   products/collections, so Google requires the matching products in your
   Shopify product feed to carry the same `promotion_id` (via the
   `promotion_ids` / custom label mapping Google's product feed spec
   expects). Un-mapped `specific_products` promotions get disapproved. See
   the green note cell in the xlsx for Google's own explanation.
2. **Effective/display end dates.** Neither Shopify discount has an end
   date configured, so the generator assigns a synthetic 90-day
   `promotion_effective_dates` end (see script docstring). Confirm these
   dates make sense, or shorten/extend them, before uploading.

## Regenerating the feed

```bash
export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx   # Admin API access token, read_discounts scope
python3 scripts/generate_promotions_feed.py
```

This overwrites both files in `feeds/` with the current set of active
automatic Shopify discounts. Re-run it periodically (e.g. before a
promotion's synthetic end date passes) to keep the feed current.

Options:

```
--out-tsv PATH              (default: feeds/google_merchant_promotions.txt)
--out-xlsx PATH             (default: feeds/google_merchant_promotions.xlsx)
--default-duration-days N   (default: 90)
--destination VALUE         (default: Shopping_ads)
```

Requires `openpyxl` (`pip install openpyxl`).

---

# Skutt Kiln Full Set of Replacement Elements

`scripts/build_skutt_element_sets.py` holds the Element tables from Skutt's
2026 Parts Price List (effective January 10, 2026) and builds the Shopify
product **Skutt Kiln Full Set of Replacement Elements**
(`skutt-kiln-full-set-of-replacement-elements`). It follows the Cone Art
element-set product:

- One dropdown, **Kiln Model and Voltage**, with each model + voltage/phase
  listed twice: "... – Standard" and "... – APM (Long-Life)". Element type
  is folded in, not a second option: a separate Element Type dropdown let
  shoppers pick APM for kilns that have no APM set, which the theme shows
  as "Unavailable".
- Price = Skutt list price × every element in the kiln. Sets whose list
  total is $252 or less sell for $20 over list (`SMALL_SET_MAX` /
  `SMALL_SET_SURCHARGE` in the script).
- APM variants are left out where Skutt lists APM as "Call For Pricing".
- Wired-ring kilns (WR / -27) get their own variants with the 2 extra
  elements (1 extra for the 145 WR), per footnote 1 of the price list.
- SKUs: `SK<model>FSE-<voltage>[-<phase>][-APM]`, e.g. `SK12273FSE-208-3-APM`.
- Weight: 1 lb per element. Inventory not tracked; continue selling when
  out of stock.

```bash
python3 scripts/build_skutt_element_sets.py
```

writes:

- `data/skutt_element_sets_2026.csv`: one row per variant with its Skutt
  part numbers, for checking against the price list.
- `data/skutt_element_sets_2026.json`: the `productSet` input used to create
  the product.

When Skutt issues a new price list, update the prices in `KILNS`, re-run, and
update the variant prices from the CSV.
