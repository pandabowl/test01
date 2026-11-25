# Category Header Banners

Remakes of the old Volusion-era category header images (the glossy
orange-red lettering with a cream rim, set over product photos on a warm
textured background). The two surviving originals are in `originals/`:
`tools-21.jpg` (still live on *Clay Tools / Trimming Tools*) and
`mixers-pugmills-3.jpg`. Both are only 235×75 px.

The new banners are 2000×640 px, close to the originals' 3.13:1 shape, so
they're sharp on retina screens. Every product in them is a real Sheffield
Pottery product photo, cut out of its white studio background.

## Contents

- `out/*.jpg`: the finished banners, ready to upload.
- `banners.json`: one entry per banner: title, target collection handle,
  background colours, optional generated pattern (firebrick wall or stain
  colour chips), title position/size, and where each product sits
  (`x`/`y` = centre as a fraction of width/height, `h` = height as a fraction
  of banner height, `rot` in degrees, `z` for stacking).
- `cutouts/`: the product cutouts (WebP with transparency) and the clay/glaze
  swatch photos the layouts use.
- `scripts/cutout.py`: removes a white studio backdrop from a product photo.
- `scripts/render.cjs`: renders banners from `banners.json` with headless
  Chromium.
- `originals/`: the two surviving old banners, for reference.

## Regenerating

```bash
node banners/scripts/render.cjs            # all banners
node banners/scripts/render.cjs tools kilns  # just these
```

This needs Playwright with Chromium, plus network access to Google Fonts for
the **Ribeye** typeface.

## Adding a banner

1. Find a product photo with a plain white background (the storefront's
   `/collections/<handle>/products.json` lists every product's image URLs).
2. Cut it out:
   ```bash
   python3 banners/scripts/cutout.py "<image url>" banners/cutouts/new-thing.png
   ```
   If it leaves a grey halo from a studio shadow, add `--shadow 50`. If parts
   of the product are missing, lower `--tol`. White products on white
   backgrounds (white wheels, white stilts) won't cut out cleanly, so skip
   them. Convert the result to `.webp` if you like; the renderer accepts both.
3. Add an entry to `banners.json` and render. Long titles shrink
   automatically to `text.maxWidth`.

Requires `numpy`, `scipy` and `Pillow`.

## Putting them on the store

On the old site the banner sat at the very top of the collection
description, as an `<img>` inside a `<p>`. Only *Clay Tools / Trimming Tools*
still has one (`files/21_480x480.jpg`). To install a banner:

1. Upload `out/<key>.jpg` to **Content → Files** in Shopify admin.
2. In the collection's description, replace the old `<img>` (or add one at
   the top) with:
   ```html
   <p><img src="<uploaded file URL>" alt="<Title>" width="2000" height="640" style="width:100%;height:auto;"></p>
   ```
