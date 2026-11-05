# Shimpo Holiday Promotion: Nov 1 to Dec 31, 2026

Buy a Shimpo pottery wheel, get a free Sheffield Pottery gift certificate:

| Wheel | Gift certificate |
|---|---|
| Shimpo RK-Whisper | $40 |
| Shimpo VL-Whisper | $40 |
| Shimpo VL-Lite | $30 |

## Launched 12:01am Eastern, Nov 1, 2026

Landing page and product banners were re-applied at launch and verified live.
The live theme at launch was "PREVIEW - Hide Halloween (01-11-26)", which
already had the updated Shimpo strip.

## What went live in Shopify

The banners were taken back down on Oct 31 so nothing shows before the
start. They are re-applied at 12:01am Nov 1 (each banner + its original).

Each change is a `<div class="shimpo-holiday-promo-2026">` block placed at the
very top of a description. To take the promo down, delete that block, or
restore the matching file in `originals/`.

- **Landing page:** the `/collections/shimpo-pottery-wheels` description, with
  `collection-banner.html` (with the red-bow image) added above the original text.
- **Product pages:** `product-banner-40.html` / `product-banner-30.html` added
  (with the red-bow image) above the original description on:
  - `nidec-shimpo-vl-whisper-pottery-wheel-svlw` ($40)
  - `shimpo-rk-whisper-potters-wheel-srkw` ($40)
  - `shimpo-vl-lite-wheel-with-splash-pan-svll` ($30)
  - `shimpo-vl-whisper-pottery-wheel-in-store-pickup` ($40)
  - `shimpo-rk-whisper-pottery-wheel-special` ($40)
- The two "Educational Promo" (5-wheel school) listings were left unchanged.

## Home page strip: publish the theme copy at 12:01am

Theme **"SHIMPO HOLIDAY PROMO - publish Nov 1 12:01am"** is a copy of the live
theme ("PREVIEW - Equipment finder hidden v3 (28-10-26)") made Oct 31. The only
change is the Shimpo strip in `templates/index.json` (saved here as
`theme/index.json`):

- Image: `shimpo-holiday-promo-red-bow.jpg`
- Heading: "Holiday promo on now!", with the highlighted part reading "Free gift certificates"
- Body: "Buy a Shimpo pottery wheel by Dec 31 and get a free $40 Sheffield
  Pottery gift certificate (RK-Whisper or VL-Whisper) or $30 (VL-Lite)."

Preview: https://www.sheffield-pottery.com/?preview_theme_id=197006229875

Theme edits made to the live theme after Oct 31 are not in this copy.

## Image

`shimpo-holiday-promo-red-bow.jpg` is the original `Shimpo-holiday-promo.jpg`
with the gift bows recolored red by `recolor_bow.py`:

    python3 recolor_bow.py shimpo-holiday-promo-original.jpg shimpo-holiday-promo-red-bow.jpg

## Home page big slide (live Nov 1, 2026)

Theme "SHIMPO BIG SLIDE - copy of live (01-11-26)" was published Nov 1. Its
home page (`theme/index-big-slide.json`) adds the `shimpo_holiday_hero` section
(the code in `home-slide/custom-liquid-section.liquid`) above the
four-card block. The slideshow comes after that block. The old `shimpo_holiday`
promo strip is hidden, and the Brent slide stays hidden.

To end the promo after Dec 31: hide the "Shimpo holiday hero" section in the
theme editor, and remove the `shimpo-holiday-promo-2026` banner block from the
landing page and the five product descriptions (originals are in `originals/`).

## Hero restyle (live Nov 5, 2026)

Theme "PREVIEW - Shimpo hero snowflakes (05-11-26)" was published Nov 5. It
restyles the live-text Shimpo hero to match the social ad: crystal snowflakes,
a navy gradient and string lights. The code is in
`home-slide/shimpo-hero-live-text-snowflakes.liquid`, and the full home page
template is `theme/index-snowflakes.json`. The hero hides itself after Dec 31
(`promo_ends`).
