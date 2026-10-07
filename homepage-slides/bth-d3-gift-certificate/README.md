# Home page slide: $50 gift certificate with the BTH Andromeda D3

Slide for the home page slideshow (`abz_slide_show` section) promoting the
offer on the [BTH – Andromeda D3 Pottery Wheel](https://www.sheffield-pottery.com/products/bth-dd03-pottery-wheel):

> Special Offer: BUY NOW AND GET A $50 GIFT CERTIFICATE TOWARDS YOUR NEXT ORDER at Sheffield Pottery!

| File | Size | Use for |
|---|---|---|
| `bth-d3-gift-certificate-desktop.jpg` | 3800 × 1100 | Slide **Image** |
| `bth-d3-gift-certificate-mobile.jpg` | 1234 × 1600 | Slide **Mobile image** |

These are 2× the size of the other slides (1900 × 550 desktop, 617 × 800
mobile). The proportions are the same, so the slideshow height doesn't change,
and the text stays sharp on retina screens. The slideshow uses
**Image aspect: Original**, so keep these proportions if the images are ever
re-exported.

The headline, offer, and button are part of the image, the same way the old
4th of July sale slide worked. Leave the slide's own text fields empty.

## Adding it to the slideshow

In **Online Store → Themes → Customize → Home page → abz slideshow → Add slide**:

| Setting | Value |
|---|---|
| Image | `bth-d3-gift-certificate-desktop.jpg` |
| Mobile image | `bth-d3-gift-certificate-mobile.jpg` |
| Link (media link) | the *BTH - Andromeda D3 Pottery Wheel* product (`/products/bth-dd03-pottery-wheel`) |
| Heading / Subheading / Text / Buttons | leave empty |
| Overlay opacity | 0 |

Image alt text (set it on both files in **Content → Files**):

> Special offer: get a $50 gift certificate toward your next order when you buy the BTH Andromeda D3 Pottery Wheel. Shop the Andromeda D3.

Placement: the first enabled slide's heading becomes the home page `<h1>`.
That heading is currently "SHEFFIELD POTTERY KILN PACKAGES". This slide has
no text heading, so if you move it to the first position, the home page will
have no `<h1>` while it's there. Putting it second avoids that.

When the offer ends, disable the slide. The product description and the
slide both state the offer, so update them together.

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
```

To preview while editing, open `slide.html` in a browser after
`npm install`. If Playwright can't find a browser, run
`npx playwright install chromium` once.
