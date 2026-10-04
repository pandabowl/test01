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

# Cone Art kilns: Google SEO + AI-agent readiness

`scripts/cone_art_seo.py` fixes and enriches the Cone Art kiln listings (vendor
**Cone Art Kilns**) so Google and AI shopping agents (Shopify Catalog / ChatGPT,
Copilot, Perplexity, Google AI Mode) describe them correctly. It does this by writing to
Shopify product and collection data; the theme is not changed.

- `cone_art/AUDIT.md` — what was wrong, what the tool fixes, and the items that need a
  human decision (structured-data duplication, identifiers, availability, weights…).
- `cone_art/plan.md` — before/after review of every change (SEO titles and
  descriptions, fixes, FAQs, attributes, collections).
- `cone_art/plan.json` — the same plan, machine-readable; `apply` executes it.
- `cone_art/snapshot.json` — the store state the plan was built from; `rollback`
  restores it.
- `scripts/cone_art_content.py` — the curated copy and per-model facts. Every value
  comes from the store's own spec tables and descriptions; disputed specs are listed
  in `DISPUTED_FACTS` and left out.
- `cone_art/theme/product-jsonld.liquid` — the single Product JSON-LD block for the
  theme. It is installed on an unpublished theme copy for testing, not on the live theme;
  `cone_art/theme/theme-changes.patch` holds the exact edits made to that copy.

```bash
export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx   # products + metaobjects (+ definitions) read/write
python3 scripts/cone_art_seo.py snapshot             # back up current state
python3 scripts/cone_art_seo.py plan                 # rebuild plan.json + plan.md (offline)
python3 scripts/cone_art_seo.py apply                # dry run
python3 scripts/cone_art_seo.py apply --execute      # write to the store
python3 scripts/cone_art_seo.py rollback --execute   # restore the snapshot
```

`apply` is idempotent and stops on the first Shopify error. `plan` refuses to run if a
description fix no longer matches the live text exactly, so re-run `snapshot` before
`plan` whenever the listings may have been edited.

The current plan was applied to the live store on 2026-10-04 and verified field by field.
The committed `snapshot.json` is the pre-apply state, which is what `rollback` restores.
Running `snapshot` again overwrites it with the post-apply state.
