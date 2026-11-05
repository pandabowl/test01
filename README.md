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
- `feeds/promotions_config.json` — maps each Shopify discount to the
  `promotion_id` and `long_title` used in the feed.
- `scripts/generate_promotions_feed.py` — updates both feed files from the
  Shopify Admin API.
- `tests/` — unit tests for the generator (`python3 -m unittest discover tests`).

## What's in the feed, and why

The feed lists Sheffield Pottery's two **active, automatic (no-code)**
Shopify discounts:

| Promotion | What it is |
|---|---|
| `TALISMAN_SIEVE_SCREEN` | Free replacement mesh screen with a Talisman Rotary Sieve purchase |
| `BTH_WHEEL_CLAY_DISCOUNT` | $45 off clay (4 bags at $11.25 off each) with a BTH Andromeda D3 Pottery Wheel purchase |

Each promotion has one row per period it runs. As of 2026-11-05:

| promotion_id | Shows from | Until |
|---|---|---|
| `TALISMAN_SIEVE_SCREEN`, `BTH_WHEEL_CLAY_DISCOUNT` | 2026-09-06 | 2026-12-02 |
| `TALISMAN_SIEVE_SCREEN_20261203`, `BTH_WHEEL_CLAY_DISCOUNT_20261203` | 2026-12-03 | 2027-03-02 |

The store also has dozens of other "active" Shopify discount codes, but
almost all of them are individual customer-service courtesy codes (named
after specific customers, e.g. `adamfehr`, `angieriley`) or long-expired
seasonal codes. Those are **not public storefront promotions** and must
never be published to a public Google Shopping feed — so the generator
excludes code-based discounts and only picks up automatic discounts, which
by definition apply to every shopper at checkout. It also skips automatic
discounts created by apps (upsell and bundle tools).

If a real, publicly-advertised promo code should be added to the feed later,
add its row to the `.txt` file by hand. The generator keeps rows it doesn't
manage until their end date passes.

## How renewal works

Google doesn't let a promotions feed edit a promotion once it's approved,
and a promotion's start date can't change. Promotions also can't run longer
than 183 days. So the generator never edits a row Google may have approved:

1. Rows that haven't ended are kept exactly as they are.
2. When a promotion's latest row ends within 30 days (`--renew-days`), it adds
   a new row with a new ID: the base ID plus the date the row starts
   displaying, e.g. `TALISMAN_SIEVE_SCREEN_20261203`.
3. The new row's `promotion_effective_dates` starts today, so Google reviews
   it in advance. Its `promotion_display_dates` starts the second after the
   old row ends, so shoppers see no gap.
4. Rows that have ended, and rows whose Shopify discount is no longer active,
   are removed.

Shopify has no end date on either discount, so each new row runs 90 days
(`--default-duration-days`) from its display start. Re-run the generator in
the last 30 days of a row to renew it. The next renewal is due between
2027-02-01 and 2027-03-02.

## Before you upload

1. **Map every new `promotion_id` to its products.** Both promotions are
   `specific_products`, so Google only shows them on products whose product
   feed entry carries the same `promotion_id`. Un-mapped promotions get
   disapproved (see the green note cell in the xlsx). The generator prints
   each new ID it adds. Add it next to the existing ID on the same products,
   since products can carry several. The current `*_20261203` IDs need adding
   before they start showing on 2026-12-03.
2. **Upload the whole file.** Keep the current rows in the upload, so the
   promotions that are showing now keep running until their end date.

## Regenerating the feed

```bash
export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx   # Admin API access token, read_discounts scope
python3 scripts/generate_promotions_feed.py
```

This reads the current `feeds/google_merchant_promotions.txt`, applies the
renewal rules above, and rewrites both files. The xlsx is updated in place, so
its formatting and Google's notes are kept. Running it again with nothing due
changes nothing.

To preview what a future run would do, add `--as-of YYYY-MM-DD` and point
`--out-tsv`/`--out-xlsx` at copies.

Options:

```
--out-tsv PATH              feed to read and update (default: feeds/google_merchant_promotions.txt)
--out-xlsx PATH             (default: feeds/google_merchant_promotions.xlsx)
--config PATH               (default: feeds/promotions_config.json)
--default-duration-days N   display length when Shopify has no end date (default: 90, max 183)
--renew-days N              renew when the current row ends within N days (default: 30)
--review-lead-days N        review time before a brand-new promotion shows (default: 3)
--timezone TZ               time zone for promotion dates (default: America/New_York)
--as-of YYYY-MM-DD          treat this date as today
--destination VALUE         (default: Shopping_ads)
--api-version VERSION       Shopify Admin API version (default: 2026-10, or $SHOPIFY_API_VERSION)
```

A new automatic discount with no entry in `feeds/promotions_config.json` gets
an ID built from its Shopify title. To choose its ID and title, add its
Shopify discount ID to the config before the first run. Never change a
`promotion_id` there once Google has seen it.

Shopify supports each Admin API version for about a year, so update
`API_VERSION` in the script when Shopify retires 2026-10 (expected around
October 2027).

Requires Python 3.9+ and `openpyxl` (`pip install openpyxl`). On Windows, also
`pip install tzdata`.
