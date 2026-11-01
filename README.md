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

# GTIN audit

`scripts/gtin_audit.py` checks every active Shopify variant for a valid GTIN
(UPC/EAN/ISBN) and writes:

- `feeds/gtin_audit.csv`: one row per variant, with its status and what to do
- `feeds/gtin_vendor_summary.csv`: missing GTINs counted per vendor, so you
  can request barcode lists one vendor at a time

```bash
export SHOPIFY_STORE_DOMAIN=sheffield-pottery.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx   # read_products scope
python3 scripts/gtin_audit.py                 # --include-inactive for drafts/archived
```

GTINs can't be generated. A valid one has to be assigned by the brand owner
under a GS1 company prefix, and Google checks them against GS1, so made-up
numbers get disapproved. Each variant gets one of these statuses:

| Status | Meaning | What to do |
|---|---|---|
| `ok` | Valid GTIN on file | Nothing |
| `fix_format` | Barcode fails the GS1 check digit (often a UPC missing its leading 0) | Use the suggested value after checking it against the packaging, or clear it |
| `get_from_vendor` | Resold product with no barcode | Ask the manufacturer for their UPC list, or read it off the packaging |
| `own_brand` | Sheffield Pottery's own product (clay, glazes, slips) | License GTINs from GS1 US and assign them, **or** submit to Google with `identifier_exists = no` plus brand + MPN (allowed when no GTIN was ever assigned) |
