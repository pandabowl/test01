# Home page slide: $50 gift certificate with the BTH Andromeda D3

Slide for the home page slideshow (`abz_slide_show` section) promoting the
offer on the [BTH – Andromeda D3 Pottery Wheel](https://www.sheffield-pottery.com/products/bth-dd03-pottery-wheel):

> Special Offer: BUY NOW AND GET A $50 GIFT CERTIFICATE TOWARDS YOUR NEXT ORDER at Sheffield Pottery!

| File | Size | Use for |
|---|---|---|
| `bth-d3-gift-certificate-desktop.jpg` | 3800 × 1100 | Slide **Image** |
| `bth-d3-gift-certificate-mobile.jpg` | 1234 × 1600 | Slide **Mobile image** |
| `assets/bth-d3-wheel.png` | 875 × 935 | Cut-out of the product's main photo, used in both |

These are 2× the size of the other slides (1900 × 550 desktop, 617 × 800
mobile). The proportions are the same, so the slideshow height doesn't change,
and the text stays sharp on retina screens. The slideshow uses
**Image aspect: Original**, so keep these proportions if the images are ever
re-exported.

The headline, offer, and button are part of the image, the same way the old
4th of July sale slide worked. The whole slide links to the product.

## Status (2026-10-07)

- Both images are in **Content → Files** as `bth-d3-gift-certificate-desktop.jpg`
  and `bth-d3-gift-certificate-mobile.jpg`, with the alt text below. They were
  replaced in place with the version that includes the wheel photo, so the
  filenames (and anything pointing at them) didn't change.
- **Ready to publish (2026-10-08): "ABZ Stiletto - D3 gift cert slide (08-10-26)".**
  This is a fresh copy of the live theme, made 2026-10-08 18:10 UTC, with the
  slide **turned on** as slide 2 (after Kiln Packages). Checked file by file,
  it differs from the live theme only in `templates/index.json`, which is the
  live template plus one block, `slide_bthD3g`.
- The first preview copy, made 2026-10-07, is out of date and has been renamed
  **"OLD - D3 slide preview (don't publish)"**. Publishing it would undo a
  header text change made on the live theme at 17:43 UTC on 2026-10-07
  ("SHOWROOM BY APPOINTMENT" became "TOOL ROOM SHOPPING BY APPOINTMENT").
  Delete it. The Shopify connector can't delete themes.
- The live theme is **"ABZ Stiletto - D3 gift cert badge (preview)"**,
  published 2026-10-07 15:15 UTC despite the name. It hasn't been changed by
  this work. The Shopify connector can't edit or publish the live theme.
- `preview-theme/templates/index.json` is the home page template that was
  written to the copies.

## Going live

Pick one:

1. **Publish "ABZ Stiletto - D3 gift cert slide (08-10-26)"**: go to
   **Online Store → Themes**, find it in the theme library, open its **…**
   menu, and choose **Publish**. The slide goes live immediately. This is only
   safe while the live theme is unchanged since the copy was made
   (2026-10-08 18:10 UTC). Any edit to the live theme after that, including
   apps editing theme files or settings changes in the theme editor, would be
   undone by publishing, so compare the two themes again first if in doubt.
   To roll back, republish "ABZ Stiletto - D3 gift cert badge (preview)".
2. **Add the slide in the live theme editor** (steps below). This works
   whatever has changed on the live theme in the meantime.

## Adding it to the slideshow

In **Online Store → Themes → Customize → Home page → abz slideshow**:

1. Click **Add slide**. A new slide comes pre-filled with a **Heading**
   ("Slideshow") and **Text** ("Use this section to make a bold statement").
   **Delete both**, or they'll be drawn on top of the image.
2. Set these:

   | Setting | Value |
   |---|---|
   | Image | `bth-d3-gift-certificate-desktop.jpg` |
   | Mobile image | `bth-d3-gift-certificate-mobile.jpg` |
   | Link (media link) | the *BTH - Andromeda D3 Pottery Wheel* product |
   | Heading, Subheading, Text, Buttons | empty |
   | Overlay opacity | 0 |

3. Drag the new slide up so it sits directly below **SHEFFIELD POTTERY KILN
   PACKAGES**. New slides are added at the end of the list.
4. Check the editor preview: nothing should be drawn over the image. If you're
   not ready for it to go live, hide it with the eye icon, then save.

Image alt text (already set on both uploaded files in **Content → Files**):

> Special offer: get a $50 gift certificate toward your next order when you buy the BTH Andromeda D3 Pottery Wheel. Shop now.

Placement: the first enabled slide's heading becomes the home page `<h1>`.
That heading is currently "SHEFFIELD POTTERY KILN PACKAGES". This slide has
no text heading, so if it's moved to the first position, the home page will
have no `<h1>` while it's there. Second place avoids that.

When the offer ends, disable the slide. The product description, the product
image badge (`custom.image_offer_badge` metafield) and this slide all state the
offer, so update them together.

## Safe zones

Because the button is part of the image, the layout has to stay clear of
the theme's slideshow controls. The geometry below comes from the live theme's
`assets/theme.css`:

- **Dots:** the slideshow dots sit over the image's bottom-left corner,
  32px above the bottom, one 24px tap target per slide. Keep text and the
  button out of that corner. Otherwise taps meant for the button switch slides.
- **Link area:** the slide's link only covers the centred content strip
  (1400px plus side gutters). On very wide screens, the outer edges of the
  image aren't clickable, so keep the button in the middle of the banner.
- **Mobile switch:** the theme shows the mobile image below 720px wide. At
  768px (iPad portrait), the desktop image is drawn at 40% size, so text in it
  needs to be about 30px or bigger to stay readable.

`npm run check` tests the text and button positions in `slide.html` against
all three rules at every screen width from 320 to 2560px.

## Editing and re-rendering

`slide.html` is the source for both images. Each image is an artboard in that
file (`#desktop` and `#mobile`), and the colors are taken from the live
theme's settings (cream `#fdf9f5`, clay `#efe7db`, button red `#f40000`).
The theme's own fonts (ITC Stepp, Neuzeit S, ITC Clearface) are licensed for
the storefront only. The slide uses open-source stand-ins from Fontsource:
Barlow / Barlow Condensed for the headline and copy, and Playfair Display for
the certificate.

```bash
npm install          # fonts + Playwright
npm run render       # rewrites both JPGs
npm run check        # dots / link-area check at 320-2560px
```

To preview while editing, open `slide.html` in a browser after
`npm install`. If Playwright can't find a browser, run
`npx playwright install chromium` once.

The wheel is the product's main photo (`BTH-D32.jpg`) with the background
removed by `make-cutout.py`, which uses rembg's IS-Net model. In the photo,
the pedal cable runs off the right edge and the pedal is clipped at the
bottom. `slide.html` puts those two edges on the edge of each artboard
(`--wx`, `--wy`, `--ws`), so neither cut is visible. Keep that if you move
the wheel.
