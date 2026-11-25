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

# Kiln package "What's in the package" boxes

`kiln-packages/` adds a "What's in the package" box to each kiln package
description. The box lists the kiln, everything in its furniture kit and
everything that comes with its vent.

- `kiln-packages/build_package_boxes.py`: the per-package contents (with
  sources noted in the docstring) and the code that builds the box and puts
  it in the description. Running it again replaces the box rather than
  adding a second one.
- `kiln-packages/originals/`: every package description as it was before
  this change (pulled 2026-11-19), so any of them can be restored.
- `kiln-packages/updated/`: the new descriptions, ready to send to Shopify.
- `kiln-packages/preview.html`: all the boxes on one page for review.
- `kiln-packages/verify_live.py`: checks a saved `nodes(ids:)` response
  (`{ ... on Product { id descriptionHtml } }`) against `updated/`. It
  prints OK or MISMATCH for each product and exits 1 on any mismatch.
- `kiln-packages/merge_live.py`: for any product in that saved response
  whose live description has lost its box, puts the box back into the
  live text and writes the result to `updated/`. Edits made since the
  push, such as a new banner, are kept.
- `kiln-packages/check_base.py`: run just before pushing one product. It
  prints PUSH only if nobody has changed that product's description text
  since its file in `updated/` was prepared. Unlike comparing `updatedAt`,
  it ignores the scheduled job that updates other product fields several
  times a day.

Note: `originals/` predates the 2026-11-19 "Free Lift-Gate Service"
banner, so restoring an original also removes that banner.

```bash
python3 kiln-packages/build_package_boxes.py
python3 kiln-packages/verify_live.py <saved nodes response>.json
python3 kiln-packages/merge_live.py <saved nodes response>.json
```
