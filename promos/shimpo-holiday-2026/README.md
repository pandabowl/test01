# Shimpo Holiday Promotion: Nov 1 to Dec 31, 2026

Buy a Shimpo pottery wheel, get a free Sheffield Pottery gift certificate:

| Wheel | Gift certificate |
|---|---|
| Shimpo RK-Whisper | $40 |
| Shimpo VL-Whisper | $40 |
| Shimpo VL-Lite | $30 |

## What is live in Shopify (set Oct 31, 2026)

Each change is a `<div class="shimpo-holiday-promo-2026">` block placed at the
very top of a description. To take the promo down, delete that block, or
restore the matching file in `originals/`.

- **Landing page:** the `/collections/shimpo-pottery-wheels` description, with
  `collection-banner.html` added above the original text.
- **Product pages:** `product-banner-40.html` / `product-banner-30.html` added
  above the original description on:
  - `nidec-shimpo-vl-whisper-pottery-wheel-svlw` ($40)
  - `shimpo-rk-whisper-potters-wheel-srkw` ($40)
  - `shimpo-vl-lite-wheel-with-splash-pan-svll` ($30)
  - `shimpo-vl-whisper-pottery-wheel-in-store-pickup` ($40)
  - `shimpo-rk-whisper-pottery-wheel-special` ($40)
- The two "Educational Promo" (5-wheel school) listings were left unchanged.

## Home page strip (live theme, set in the theme editor)

The connection used here cannot edit the live theme, so change the
"Shimpo holiday" promo strip section by hand:

- Heading: `Holiday promo on now!`, with the highlighted part reading `Free gift certificates`
- Body: `Buy a Shimpo pottery wheel by Dec 31 and get a free $40 Sheffield Pottery gift certificate (RK-Whisper or VL-Whisper) or $30 (VL-Lite).`
- Image: `shimpo-holiday-promo-red-bow.jpg` (same artwork with red bows)
- Button: unchanged, `Shop Shimpo wheels` linking to `/collections/shimpo-pottery-wheels`

## Image

`shimpo-holiday-promo-red-bow.jpg` is the original `Shimpo-holiday-promo.jpg`
with the gift bows recolored red by `recolor_bow.py`:

    python3 recolor_bow.py shimpo-holiday-promo-original.jpg shimpo-holiday-promo-red-bow.jpg
