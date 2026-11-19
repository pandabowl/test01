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

# GTINs (product barcodes)

Google Shopping reads each variant's GTIN from Shopify's **Barcode** field.
As of 2026-11-18 only 44 of ~3,000 active products had one, so most
listings went to Google without a GTIN.

`feeds/gtin/` holds the results of a GTIN audit of the public catalog
(6,001 variants):

- `gtin_found.csv` — 310 variants with a GTIN that passes the GS1
  check digit. All 310 were written to Shopify's Barcode field on
  2026-11-19 and checked against the live storefront (`action` column
  shows what changed):
  - 222 come from the variant metafield `custom.pdp_upc_number`, which
    already held UPCs (mostly Xiem and Speedball) that never reached the
    Barcode field.
  - 45 are existing barcodes; 34 of them were stored as 11 digits (the
    leading `0` was dropped, likely by a spreadsheet) and are restored to 12.
  - 43 Amaco/Brent items are derived from Amaco's item number
    (`custom.pdp_vendor_part_no`): Amaco UPCs are `039672` + the 5 digits of
    the item number + a check digit. This matched all 27 Amaco/Brent
    barcodes already in the store and 5 independent retailer listings.
- `gtin_data_problems.csv` — junk or conflicting values to clean up.
- `gtin_missing.csv` — the 5,691 variants still without a GTIN, bucketed:
  - `ask vendor`: retail-packaged brands that normally carry UPCs; request
    a UPC list from the vendor.
  - `probably none`: own-brand, repackaged bulk materials, made-to-order
    kilns/equipment and refractories. Send brand + MPN to Google and leave
    GTIN empty; don't invent one.
  - `check`: unclear; confirm with the vendor.

Never make up or reuse a GTIN: a wrong one is worse for Google than none.
