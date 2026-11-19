# Laguna front-loading gas kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/laguna-front-loading-gas-kilns
(collection `gid://shopify/Collection/441037422914`).

Published 2026-11-19 as a **shared block** (see `../SHARED-BLOCKS.md`), not in
`custom.abz_collection_below_descrption` (that value was not changed):
- Block entry `laguna-gas` (`gid://shopify/Metaobject/685585957235`, type
  `kiln_comparison_block`); repo copy `blocks/laguna-gas.html`.
- The collection's `custom.comparison_blocks` = `[laguna-gas, kiln-compare-cta]`
  (`live_comparison_blocks_2026-11-19.json`). It renders above the existing
  "below text", which starts with `<h3 id="Laguna-Front-Guide">`.
- The top description's "Learn more" link now points at `#laguna-gas` (was
  `#Laguna-Front-Guide`); nothing else in it changed. Backup:
  `backup_descriptionHtml_before_2026-11-19.html`; new value:
  `live_descriptionHtml_2026-11-19.html`.
- Shared `kiln-compare-cta` wording changed at the user's request from "fits your
  space and electrical service?" to "fits your space and your electrical or gas
  service?" (backup: `backup_kiln-compare-cta_before_2026-11-19.html`).
- Verified on the live page: styles, block and CTA each an exact match
  (`tools/verify_live.py`); all 7 links return 200; no sideways scroll at 1280 px
  or on an iPhone 13.

## Sources (read 2026-11-19)

- Laguna kilns page: https://www.lagunaclay.com/collections/kilns
  (model list with inner volume, standard and optional features)
- Laguna *Gas Kilns* flyer (PDF dated 2025-10-09), linked from
  https://www.lagunaclay.com/pages/catalogs-flyers:
  https://cdn.shopify.com/s/files/1/0664/2050/6866/files/gas_kilns_flyer_lagunaclay.pdf?v=1760367634
- Laguna *Fiber Kilns* flyer, same page:
  https://cdn.shopify.com/s/files/1/0664/2050/6866/files/fiber_kilns_flyer_lagunaclay_compressed.pdf?v=1761851429
- Laguna *Gas Kilns Users' Manual* (PDF dated 2023-12-05), linked from the kilns page:
  https://cdn.shopify.com/s/files/1/0664/2050/6866/files/Laguna_Gas_Kiln_Manual.pdf?v=1745524520

lagunaclay.com and www.lagunaclay.com were added to the environment's allowed hosts.

## What Laguna publishes, and what's on the page

| Item | Laguna source | On the page |
|---|---|---|
| Models and inner volume | Kilns page + both flyers: LE-200-9 9.2, LE-200-12 12, LE-200-18 18, LE-200-24 23.9, LE-200-40 40, LE-200-40C 40 cu ft ("inner firing chamber volume") | Same |
| Loading | Flyer: "standard front-load, optional car kiln"; "Car-Kiln configuration available"; LE-200-40C listed | Front door; LE-200-40C = roll-out car |
| Fuel | Flyer/kilns page: "specify natural gas or propane"; manual: orifices can be swapped between fuels | Natural gas or propane |
| Draft | Flyer: "Choice of up-draft or down-draft airflow design"; manual describes both damper/flue layouts | Updraft or downdraft |
| Max temp | Manual: high limit "pre-set at the factory to 2350° F assuming a maximum firing temperature of 2350° F"; programmable controller ships with a "P4 Cone 10 Glaze" program | Cone 10 (2350°F) |
| Brick lining | Flyer: "1½" fiber board back up insulation on brick kilns" | Same |
| Fiber lining | Fiber flyer: ceramic fiber with ITC coating; "Up to 30% savings on annual fuel costs", "Faster heating and cooling cycles", "Less kiln wall cracking issues" | Same, attributed to Laguna |
| Standard equipment | Flyer: natural-draft ceramic-tip venturi burners, direct-spark electronic ignition, digital high-limit/safety shut-off, manual burner valves, water column gauge | Same |
| Programmable controller | Flyer: optional, "8 programs, 16 segments each (combinable)" | Same |
| ETL listing | Flyer: "All Laguna Clay Company Gas Kilns are ETL Listed" (Intertek) | Same |
| Gas pressure | Manual: natural gas minimum 6 in. WC; propane two-stage regulator, ~5 PSI then ~15 in. WC | Same |
| Gas line sizing | Manual: BTU rating (on the spec plate), distance from meter, number of elbows | Same |
| Clearance | Manual: 4 ft from combustible walls, 3 ft from noncombustible | Same |
| Venting | Manual: indoor kilns must be vented, usually a hood, stainless ideal; outdoors a noncombustible roof 6-8 ft above the flue | Same |
| Delivery | Manual: crated; forklift or pallet jack needed to unload | Same |
| Model name | Not explained by Laguna. The last number matches the volume (9 = 9.2, 24 = 23.9, ...) | Stated as "approximate inner volume" |

## Not on the page, and why

Laguna's current literature does **not** publish per-model BTU ratings, burner
counts, interior/stacking dimensions or exterior dimensions. Those figures
appear only in an older spec table (the image already on the collection page,
and the LE-200-40 product description), and they don't match Laguna's current
volumes (see below). So the table has no BTU, burner or dimension columns. The
footnote asks buyers to call for the BTU rating and outside dimensions of the
configuration they want.

## Laguna's own sources disagree

- Wind skirt: the kilns page lists it as a standard feature; the gas flyer lists
  it under optional features. The page doesn't mention it.
- High-limit preset: the manual says 2350°F in one paragraph and 2400°F in the
  next. The page uses 2350°F, which the manual calls the maximum firing temperature.

## Errors and stale data in the store (not fixed; for the user)

| Where | Store says | Laguna says |
|---|---|---|
| Collection top description and below-grid text | "Sizes range from 7.9 to over 54 cubic feet" | Standard models are 9.2 to 40 cu ft (custom sizes on request). 7.9 is the gross interior of the old LE-200-4, which Laguna no longer lists; 54.1 is the old gross interior of the LE-200-40. |
| Below-grid spec image (`Laguna-gas-kiln-specs...jpg`) | Older table: LE-200-4 listed; stacking volumes 10.0 / 12.7 / 19.8 / 25.0 / 40.7 cu ft; gross interior 16.3 / 20.65 / 30.9 / 40.1 / 54.1 | LE-200-4 not offered; volumes 9.2 / 12 / 18 / 23.9 / 40 cu ft. BTU/burner figures in the image can't be confirmed from current Laguna literature. |
| LE-200-40 product description, spec table | 54.1 cu ft inside, 42x41x54 in., 36x36x54 setting area, 541,000 BTU/hr, 10 burners | Laguna lists 40 cu ft only; dimensions, BTU and burners aren't published now |
| Below-grid text | Propane minimum "14" WC" | Manual: second-stage regulator reduces propane to "approximately 15 in. of WC" (natural gas minimum 6" WC matches) |
| Below-grid text | Crating fee $240 per kiln; LE-200-40 description says $565 | Laguna: "Crating charges vary. Request a quote." (the two store figures also disagree with each other) |
| Below-grid text, standard features | K-23 brick walls / K-26 floor, 6" fiber panels, detachable wind apron | Laguna's current lists don't mention brick grades or panel thickness; they list 1½" fiber board backup on brick kilns, ITC-coated fiber, a wind skirt, and ETL listing |
| LE-200-9 `finder.note` | "Downdraft gas kiln for reduction and cone 10 firing" | Every model is offered updraft or downdraft |
| LE-200-12/-18/-24/-40 | `custom.kiln_top_cone` empty (only the LE-200-9 has "10"), so these may be missing from cone filters | Cone 10 (2350°F) for all |

## LE-200-40C quote page (added 2026-11-19, at the user's request)

- New product `gid://shopify/Product/15679542362483`,
  `/products/laguna-gas-kiln-le-200-40c-40-cubic-feet-car-kiln-le20040c`, SKU `LE20040C`.
  Published to the Online Store channel only (not Google & YouTube, Facebook, Shop or POS).
- Uses the new `templates/product.quote.json` (file in `kiln-comparisons/theme/`), which the
  user pasted into the live theme because theme writes on the live theme are blocked for the
  API. It's the live `product.json` with the variant picker, inventory counter, quantity
  selector, infinite-options app block and buy buttons removed, the price hidden with section
  CSS, and a "Request a quote" form (Shopify contact form, `form_type=contact`) where the
  buy buttons were. Submissions go to the store's contact email with the product title and SKU.
- Not purchasable: inventory tracked at 0, policy DENY, price 0.00 (hidden by the template).
  No "Laguna Front Loading Gas Kilns" tag, so the collection's smart rules leave it out of the grid.
- Description uses only Laguna-published facts (gas flyer, fiber flyer, manual); image is the
  store's existing Laguna car kiln photo.
- Known limits: the theme's structured data and `og:price` still output 0.00 / out of stock
  (theme-level, needs a theme code change). Shopify's storefront hCaptcha covers this form, so
  it can't be test-submitted from the cloud sandbox (hCaptcha hosts are blocked there); the
  user tests it from a browser.

## Old spec image removed (2026-11-19, at the user's request)

The below text (`custom.abz_collection_below_descrption`) ended with an older Laguna
spec table image (`Laguna-gas-kiln-specs_f484ae11-...jpg`). Its last paragraph
(only that `<p><img ...></p>`) was removed with `metafieldsSet` + `compareDigest`; the
rest of the text is unchanged. Backup: `backup_abz_collection_below_descrption_before_2026-11-19.html`
(proved exact against the live page first); new value:
`live_abz_collection_below_descrption_2026-11-19.html` (exact match on the live page).
The image file itself was not deleted from Shopify Files.

How the image compared with Laguna's current published volumes:

| Model | Image: stacking vol. | Image: gross interior | Image: stacking area | Image: BTU/hr / burners | Laguna now: inner volume |
|---|---|---|---|---|---|
| LE-200-4 | 4.3 | 7.9 | 16x16x29 | 79,000 / 4 | not offered |
| LE-200-9 | 10.0 | 16.3 | 24x24x30 | 163,000 / 6 | 9.2 |
| LE-200-12 | 12.7 | 20.65 | 24x24x38 | 206,500 / 6 | 12 |
| LE-200-18 | 19.8 | 30.9 | 30x30x38 | 309,000 / 8 | 18 |
| LE-200-24 | 25.0 | 40.1 | 32x32x42.3 | 401,000 / 8 | 23.9 |
| LE-200-40 | 40.7 | 54.1 | 36x36x54 | 541,000 / 10 | 40 |
| LE-200-24C (car) | 25.0 | 40.1 | 32x32x42.3 | 401,000 / 8 | not offered |
| LE-200-40C (car) | 40.7 | 54.1 | 36x36x54 | 541,000 / 10 | 40 |

Laguna's current figures sit 2-9% below the image's stacking volumes and far below its
gross interior volumes. BTU, burners, stacking dimensions and weights can't be checked
against anything Laguna publishes now. The text that remains still says "7.9 to over 54
cubic feet" (the image's LE-200-4 and LE-200-40 gross figures), in both the top
description and the below text.
