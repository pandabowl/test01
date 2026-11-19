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

Two kinds of active *automatic* discounts are also left out, and the
generator lists each one it skips on stderr (`SKIPPED: ...`):

- **App discounts** (`DiscountAutomaticApp`), e.g. the UpsellKoala volume /
  quantity-break discounts. Their real terms (tiers, eligible products) live
  in the app; the Shopify API only exposes a title and dates. The generator
  can't tell what the offer is, so it can't write an accurate promotion row
  for one. If one should be advertised, add it to the feed by hand.
- **Automatic discounts limited to specific customers, customer segments or
  markets.** Like the courtesy codes, they don't apply to every shopper.

## Shopify API notes

- **API version:** the generator calls Admin GraphQL API version `2026-10`
  (`SHOPIFY_API_VERSION` near the top of the script). Shopify supports each
  version for about 12 months; `2026-10` is supported until 16 October 2027.
  After that, Shopify quietly serves requests with the oldest version it
  still supports. If that happens, the generator prints
  `WARNING: requested Shopify API ... but Shopify served ...`. Move the
  constant to the latest stable version before then, and check that the
  query still runs without deprecated fields.
- **Query:** `discountNodes` with `query: "method:automatic status:active"`,
  sorted by ID. This replaces `automaticDiscountNodes`, which is deprecated
  as of `2026-10`. The `method:automatic` filter is what keeps code discounts
  out. The generator also checks the type of every discount that comes back,
  so a code discount still can't reach the feed if Shopify ever ignores the
  filter.
- **Eligibility (`context`):** since API version `2025-10`, automatic
  discounts can be limited to specific customers, customer segments or
  markets, and queries return those discounts too. Older versions, including
  the `2024-10` this generator used to request, filtered them out. To keep
  the same behavior, the generator only uses automatic discounts whose
  `context` is all customers (`DiscountBuyerSelectionAll`).
- **Access scope:** still just `read_discounts`.

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
