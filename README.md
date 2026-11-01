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

# Homepage hero: Shimpo holiday promo (live text)

`theme/shimpo-holiday-hero.liquid` replaces the homepage "Shimpo holiday hero"
Custom liquid section, which used to be a single 1900×560 JPG with all the
words drawn into the picture.

In the new version, every word is real HTML: the headline (an `<h2>`), the offer
details, the button, the dates and the gift cards. Search engines can index
it, it stays sharp at any screen size, and the page loads faster. The only
images are the three wheel photos, pulled from the products at about 300px
(about 29 KB in total, compared with 134 KB for the old desktop JPG). Each photo
links to its product page. The background, snow and gift cards are CSS. It uses
the theme's own Jost and Marcellus fonts, so it loads no extra fonts.

To install it, paste the file into that Custom liquid section in the theme
editor, replacing the old code. The wording is set at the top of the file.
The section hides itself after `promo_ends` (Dec 31, 2026).

# Homepage slideshow (live text)

`theme/sections/live-text-slideshow.liquid` replaces the homepage slideshow,
whose four active slides (BTH D3, kiln packages, schools, glaze discounts)
were 1900×190 pictures with every word drawn into them.

In the new section, each slide is a small photo with no words in it, next to
real HTML text: the label, the headline (an `<h2>`), the details and the
button. All four slides are in the page HTML, so search engines index every
slide, not only the first one. The words are edited in the theme editor, so
changing them doesn't require a new image.

- **Photos:** `theme/slide-photos/` holds photo-only crops of the old slides,
  6–11 KB each. Phones get their own sharper crop (`*-mobile.webp`).
- **The BTH slide** uses the wheel's own product photo. Its price, compare-at
  price and "Save $X" come live from the product, so the slide can't show an
  out-of-date price. The $50 gift certificate is drawn with CSS.
- Swiping, the dots and autoplay use a small built-in script. Autoplay pauses
  while a shopper hovers over or taps the slideshow, and it is off for people
  who have reduced motion turned on.

To install it:
1. Upload the six images in `theme/slide-photos/` to Content → Files.
2. Add `live-text-slideshow.liquid` to the theme's `sections/` folder.
3. Add the entry in `theme/live-text-slideshow.index.json` to
   `templates/index.json` in place of the old slideshow, or add the section in
   the theme editor. It comes pre-filled with the four slides' text.
