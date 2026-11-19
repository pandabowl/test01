# Paragon glass, jewelry and metal clay kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/paragon-glass-kilns
(collection `gid://shopify/Collection/441785975106`, "Paragon Glass Kilns and PMC Kilns").

Published 2026-11-19 as a shared block (see `../SHARED-BLOCKS.md`), not in
`custom.abz_collection_below_descrption` (left unchanged):

- Block `paragon-glass` (`gid://shopify/Metaobject/685600080243`), repo copy
  `blocks/paragon-glass.html`: glass-fusing table plus jewelry/metal
  clay/enameling table.
- Page list `custom.comparison_blocks` = `[paragon-glass, kiln-compare-cta]`
  (it was empty before).
- The top description's "Learn more" link now points at `#paragon-glass`
  (was `#abz_below_richtxt_id`, the below-text section). Before/after:
  `backup_descriptionHtml_before_2026-11-19.html`, `live_descriptionHtml_2026-11-19.html`.

Verified on the live page with `tools/verify_live.py` (block, shared styles,
CTA and description all exact), all section links return 200, and the
"Learn more" link scrolls to the block.

## Sources (read 2026-11-19)

Paragon's site, **paragonkilns.com** (paragonweb.com redirects there). Each
product page's "Specifications" tab is a spec-sheet image; every number comes
from these:

| Model (our name) | Paragon product page | Spec sheet |
|---|---|---|
| Fusion 14 | https://paragonkilns.com/products/fusion14-glass-fusing-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/Fusion14-specs.png |
| CS-14D | https://paragonkilns.com/products/cs14d-dual-clamshell-glass-fusing-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CS14D.png |
| CS19S | https://paragonkilns.com/products/cs19s-clamshell-glass-fusing-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CS19S.png |
| CS19D | https://paragonkilns.com/products/cs19d-dual-clamshell-glass-fusing-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CS19D.png |
| Fusion 10 | https://paragonkilns.com/products/fusion10-glass-fusing-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/Fusion10-specs.png |
| Janus 1613 (CT81713 Janus) | https://paragonkilns.com/products/ct81713-janus-ceramic-and-glass-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT81713Janus-specs.png |
| Janus 23 (CT102322 Janus) | https://paragonkilns.com/products/ct102322-janus-ceramic-and-glass-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT102322Janus-specs.png |
| Janus 27 (CT122822 Janus) | https://paragonkilns.com/products/ct122822-janus-ceramic-and-glass-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT122822Janus.png |
| QuikFire 6 (QuikFire VI) | https://paragonkilns.com/products/quikfire-test-kiln | spec image returns 404; numbers from the product description |
| Caldera | https://paragonkilns.com/products/caldera-multipurpose-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/Caldera-specs.png |
| Caldera XL | https://paragonkilns.com/products/caldera-xl-multipurpose-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CalderaXL-specs.png |
| Xpress Q-11 | https://paragonkilns.com/products/q11-multipurpose-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/Q11-specs.png |
| SC-2 | https://paragonkilns.com/products/sc2-jewelry-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/SC2-specs.png |
| SC-3 | https://paragonkilns.com/products/sc3-jewelry-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/SC3-specs.png |
| Xpress E-9 | https://paragonkilns.com/products/e9-enameling-and-china-painting-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/E9-specs.png |
| Xpress E-10 | https://paragonkilns.com/products/e10-enameling-and-china-painting-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/E10-specs.png |
| Xpress E-12T | https://paragonkilns.com/products/e12t-enameling-and-china-painting-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/E12T-specs.png |
| Xpress E-14 | https://paragonkilns.com/products/e14-enameling-and-china-painting-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/E14-specs.png |
| F-120 (linked only) | https://paragonkilns.com/products/f120-glass-annealing-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/F120-specs.png |

Descriptions on the same pages were used for: CS = Clamshell, S = single
opening (walls and lid lift together), D = dual opening (lid can also lift
alone); element placement (Fusion 14 and CS lids; Fusion 10 lid plus a wall
element; Janus glass mode = top + middle wall elements, pottery mode = wall
elements only); the CS-14D's "nine 4" x 4" tiles"; the E-12T's room for
bronze-clay containers; QuikFire VI (6" × 6" × 6", 2000°F, 120 V, 1,560 W, on/off
switch and pyrometer, "fire and cool glass projects in as little as 30–40
minutes"); option lists (Fusion 10/14 window variants, SC window and bead door,
Caldera bead collar); 240V variants of the Fusion 14, Caldera, Caldera XL and E-12T.

"Best seller" on the QuikFire 6: Shopify analytics, net items sold over the last
730 days: QuikFire 6 6, Caldera 5, SC-3 5. No fusing kiln stood out, so that
table has no badge.

## What's on the page (from the spec sheets)

| Model | Inside | Cu ft | Max temp | Power |
|---|---|---|---|---|
| Fusion 14 | 14" × 14" × 6.5" | 0.73 | 1700°F | 120 V, 15 A, 5-15 |
| CS-14D | 14" × 14" × 6.7" | 0.76 | 1700°F | 120 V, 15 A, 5-15 |
| CS19S | 19" × 19" × 6.7" | 1.4 | 1700°F | 240 V, 16 A, 6-20 |
| CS19D | 19" × 19" × 6.7" | 1.4 | 1700°F | 240 V, 16 A, 6-20 |
| Fusion 10 | 23.5" round × 11" | 2.86 | 1700°F | 240 V, 29 A, 6-30 |
| Janus 1613 | 16.5" × 13.25" | 1.75 | 2350°F | 240 V, 30 A, 6-30 |
| Janus 23 | 22.5" × 22.25" | 5.1 | 2350°F | 240 V, 42 A, 6-50 |
| Janus 27 | 28" × 22.25" | 8.11 | 2350°F | 240 V, 48 A, 6-50 |
| QuikFire 6 | 6" × 6" × 6" | | 2000°F | 120 V, 1,560 W (description) |
| Caldera | 8" × 8" × 6.7" | 0.25 | 2350°F | 120 V, 14 A, 5-15 |
| Caldera XL | 7.5" × 7.5" × 9" | 0.29 | 2350°F | 120 V, 15 A, 5-15 |
| Xpress Q-11 | 6" × 6" × 6.25" H | 0.13 | 2350°F | 120 V, 12 A, 5-15 |
| SC-2 | 8" × 7.75" × 5.75" H | 0.21 | 2000°F | 120 V, 14 A, 5-15 |
| SC-3 | 7.75" × 8" × 7.75" H | 0.28 | 2000°F | 120 V, 15 A, 5-15 |
| Xpress E-9 | 8.5" × 9" × 4.5" H | 0.19 | 2000°F | 120 V, 11 A, 5-15 |
| Xpress E-10 | 8.5" × 9" × 8.7" H | 0.39 | 2000°F | 120 V, 15 A, 5-15 |
| Xpress E-12T | 8.5" × 12" × 8.7" H | 0.53 | 2000°F | 120 V, 20 A, 5-20 |
| Xpress E-14 | 13" × 13.5" × 8.75" H | 0.89 | 2000°F | 240 V, 13 A, 6-20 |

## Paragon's own sources disagree (the page uses the spec sheets)

- Caldera XL description: 7.5" × 5.5" × 8.75"; spec sheet 7.5" × 7.5" × 9".
- Fusion 14 description: 6.75" deep; spec sheet 6.5".
- E-12T description: 9" high; spec sheet 8.7". E-10 description 8.75"; sheet 8.7".
- F-120 description: 10.75" × 11" × 7"; spec sheet 11" × 11" × 7".
- CT81713 Janus description: 6,400 W; spec sheet 6,240 W.

## Errors in the store's product data (not fixed; for the user)

| Product | Field | Store says | Paragon says |
|---|---|---|---|
| Fusion 10 | spec table | 2.53 cu ft, 22.5" diameter, 30 A, 7,200 W | **2.86 cu ft, 23.5", 29 A, 6,850 W** |
| CS-14D | spec table | 0.73 cu ft | **0.76 cu ft** |
| CS19S, CS19D | spec table | 1.35 cu ft | **1.4 cu ft** |
| SC-2 | spec table | 12 A, 1,440 W | **14 A, 1,680 W** |
| SC-3 | spec table | 1,800 W | **1,750 W** (15 A matches) |
| F-120 | spec table | 240 V, 13 A, 3,073 W, NEMA 6-20, 11" × 18" × 4.25" | **120 V, 14 A, 1,680 W, NEMA 5-15, 11" × 11" × 7"**. Left out of the table until it's clear which version Sheffield sells |
| Janus 1613, Janus 23 | see `../paragon-pottery/FACT-CHECK.md` | | |
| Fusion 10, Fusion 14 | product type | "Kiln Furniture" | should be a glass kiln type |
| Caldera XL | product type | "Kiln Accessories" | should be a glass kiln type |
| Fusion 10, Fusion 14, Caldera XL | finder metafields | empty | (no finder card data) |
