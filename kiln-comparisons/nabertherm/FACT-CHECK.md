# Nabertherm kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/nabertherm-kilns
Metafield: `custom.abz_collection_below_descrption` on collection
`gid://shopify/Collection/446611652930`. The page has no heading anchor inside
the below block: the top description's "Read More!" link points at
`#abz_below_richtxt_id` (the block itself), so the section is inserted at the
**start** of the metafield value, before `<h3>Helpful Resources</h3>`.
Preview with:
`node tools/preview_shot.js <url> '#sp-nabertherm-compare' preview draft.html '#abz_below_richtxt_id .rich-text__text' afterbegin`

## Sources (read 2026-11-19)

Nabertherm's US arm (Nabertherm Inc., New Castle, DE) uses the main site,
nabertherm.com. There is no separate US website; US specs are published there.

1. **US catalog (primary source for every number on the page):**
   Nabertherm *Arts & Crafts* catalog, US edition, 48 pp., PDF dated 2025-11-17:
   https://nabertherm.com/sites/default/files/2025-03/artscrafts-english-US.pdf
   (linked from https://nabertherm.com/en/products/arts-crafts/top-loaders/top-loaders)
   Top loaders p. 16–17, Top ../R p. 18–19, chamber kilns N p. 24–25,
   N ../H p. 26–27, AC590 controller p. 37–41, MyNabertherm app p. 42.
2. **US/Canada top-loader manual** M01.9089, 2026-06:
   https://nabertherm.com/sites/default/files/noindex/2026-06/M01.9089_Toplader_USA%20Canada_English_2026-06.pdf
   Section 2.2 specifications (incl. **max. charge weight**) and the model-name
   explanation ("Top = Top loader, round/oval; 60 = 2.1 cft kiln chamber; R = rapid").
3. **US/Canada chamber-kiln manual** M01.9038, 2025-03:
   https://nabertherm.com/sites/default/files/noindex/2025-04/M01.9038_N_USA_Canada_English_2025-03_0.pdf
   Section 2.2 (N 200 max. charge weight) and model names ("N = Chamber kiln;
   200 = 7.06 cft; H = High temperature").
4. **nabertherm.com product pages, "Technical Specifications U.S. models" tables:**
   - https://nabertherm.com/en/products/arts-crafts/top-loaders/top-loaders
   - https://nabertherm.com/en/products/arts-crafts/top-loaders/top-loaders-increased-connected-load
   - https://nabertherm.com/en/products/arts-crafts/chamber-kilns/chamber-kilns-1300-degc-heated-five-sides
   These match the US catalog for every model on the page.
5. International (metric) catalog, used only to confirm that the model number =
   chamber liters and to explain where the store's metric figures came from:
   https://nabertherm.com/sites/default/files/2024-04/artscrafts_english_0.pdf

## Where each number on the page came from

All rows: 240V single-phase ("2/PE") except the N 200 (240V three-phase, "3/PE").

| Model | Interior (in) | cu ft | Max load | Tmax | Amps @240V | Breaker / plug | Source |
|---|---|---|---|---|---|---|---|
| Top 60 | Ø 16.0 × 17.8 | 2.11 | 66 lb | 2408°F, cone 10 | 15.2 | 20 A / NEMA 6-20 | Catalog p. 17 (load: manual 2.2) |
| Top 60/R | Ø 16 × 17.8 | 2.11 | 66 lb | 2408°F, cone 10 | 23.2 | 30 A / NEMA 6-30 | Catalog p. 19 (load: manual 2.2) |
| Top 160 | Ø 23.0 × 22.4 | 5.65 | 176 lb | 2408°F, cone 10 | 37.7 | 50 A / NEMA 6-50 | Catalog p. 17 (load: manual 2.2) |
| Top 190 | Ø 23.0 × 26.7 | 6.70 | 176 lb | 2408°F, cone 10 | 41.5 | 60 A / fixed | Catalog p. 17 (load: manual 2.2) |
| Top 220 | 36.6 × 23.0 × 17.7 (oval) | 7.76 | 150 lb | 2408°F, cone 10 | 62.7 | 80 A / fixed | Catalog p. 17 (load: manual 2.2) |
| N 200 | 18.5 W × 20.9 D × 30.7 H | 7.06 | 220 lb | 2372°F, cone 10 | 37.0 (3-phase) | 50 A / fixed | Catalog p. 25 + web page (load: N manual 2.2) |

- Liters in the Capacity column: the international catalog's "Volume in l"
  (Top 60 = 60 l … Top 220 = 220 l, N 200 = 200 l); they equal the cu ft × 28.3.
- 208V footnote (Top 60 6-30/30 A, Top 60/R 6-50/50 A, Top 160 fixed): catalog p. 17/19.
- "Every model except the Top 60 comes in three-phase": catalog p. 17/19 (the Top 60
  is listed only at 208/240V 2/PE).
- 5.6 kW vs 3.7 kW (/R text): catalog p. 17/19.
- Made in Germany, UL 499 / CSA C22.2#221, 36-month warranty: catalog p. 2.
- AC590 standard on all of them; 50 programs; cone firing assistant; USB data;
  Wi-Fi + free MyNabertherm app: catalog p. 16, 24, 37–42.
- /R "heat up much faster … frequent use … Cone 10": catalog p. 18.
- /H = cone 13 (2444°F): catalog p. 26.
- Bottom heating + manual zone control, Top 160–Top 220: catalog p. 15.
- N 300 10.59 cu ft, N 440 15.53 cu ft: catalog p. 25.

## Nabertherm's own sources disagree

- **N 200 power and amps:** US catalog (Nov 2025) and web page: 15.2 kW,
  42.7 A @208V / 37.0 A @240V. Older US/Canada manual (Mar 2025): 15 kW,
  41.6 A / 36.1 A. **The page uses the catalog** (it's newer and matches the web page).
- **Top 60/R plug on 208V three-phase:** catalog and web page say NEMA 15-30 on a
  50 A breaker; the June 2026 manual says 15-50 (which matches a 50 A breaker).
  Not shown on the page.
- Top 190 connected load: catalog 10.0 kW, manual 9.96 kW. Top 190/R weight:
  catalog 298 lb, manual 297 lb. Not on the page.
- Max temp wording: tables give Tmax 2408°F "to fire cone 10"; the Top ../R text
  says "up to 2354 °F/Cone 10"; the manual says top loaders suit firing "up to
  2300 °F and can be fired up to 2408 °F". The page shows "Cone 10, 2408°F max"
  (2372°F for the N 200), matching the spec tables.
- International (metric) models differ from US models (e.g. Top 60 3.6 kW,
  Top 190 11.0 kW three-phase, Top 190/R 13.5 kW). The page uses US models only.

## What matched in the store's data

The spec tables in the product descriptions of the Top 60, Top 60/R, Top 160,
Top 190 and Top 220 are copies of Nabertherm's US tables and match the catalog
exactly (including the catalog's 15-30 plug for the Top 60/R on 208V 3-phase).
The finder `facts` capacities (2.11, 5.65, 6.7, 7.76 cu ft) are correct.

## Errors in the store's product data (not fixed; for the user)

| Product | Field | Store says | Nabertherm says |
|---|---|---|---|
| Top 60R | SEO meta description | "Buy the Nabertherm **Top 190** … 190L capacity" (copied) | Should describe the Top 60/R (60 L, 2.11 cu ft) |
| Top 60R | description intro | Tmax 1300 °C | **1320 °C / 2408 °F** |
| Top 60R | description intro | "Incl. NEMA-plug 60-50P" | **NEMA 6-30** at 240V (6-50 at 208V) |
| Top 60R | description intro | 5,5 kW; inner 410 × 460 mm; outer 580 × 870 × 870 mm (metric/international) | US: **5.6 kW; Ø 16 × 17.8 in; 23.6 × 35.0 × 35.4 in** |
| Top 160 | handle / part no. | handle `nabertherm-top-190`, `pdp_vendor_part_no` TOP190 | It's the Top 160. (Changing the handle needs a URL redirect.) |
| Top 160 | Yotpo metafields | `preloaded_product_filters` productId 8304889004354 | That is the **N200's** product ID (listing was duplicated) |
| Top 190 | "Specifications" list | Power 13.5 kW | **10.0 kW** (13.5 kW is the international Top 190/R) |
| Top 190 | "Specifications" list | Interior Ø 600 × 670 mm (23.6" × 26.4") | **Ø 23.0 × 26.7 in** (intl Ø 590 × 680 mm) |
| Top 190 | "Specifications" list | Exterior 35.43 × 35.43 × 41.34 in; weight 441 lb (200 kg) | **30.7 × 42.5 × 45.6 in; 298 lb** |
| Top 190, Top 220 | "Specifications" list | Controller: B 400 (standard) | **AC590** touch controller is standard |
| Top 190, Top 220 | "Specifications" list | "High-quality ceramic fiber insulation" | Light-weight refractory brick + microporous back-up insulation; Nabertherm says it uses **no ceramic fiber (RCF)** |
| Top 190, Top 220 | "Specifications" list | Elements "on all sides including floor" | Floor (bottom) heating is an **option** for Top 160–220 |
| N200 | description / metafields | No spec table; `custom.voltage` "240 or 208"; never says three-phase | **Three-phase only** (208V or 240V 3-phase), 15.2 kW, 42.7 / 37.0 A, hardwired; 7.06 cu ft; 18.5 × 20.9 × 30.7 in |
| N200 | description | Mentions models N 100/G … N 660/H and °C temperature advice (international copy) | US lineup is N 200, N 300, N 440 (and /H) |
| Top 160, Top 190, N200 | `custom.kiln_top_cone` | missing | Cone 10 (all three) |
| N300 (unlisted) | SEO title | "480V 3PH" (but `custom.voltage` says 240 or 208) | US catalog lists N 300 at 208/240V 3-phase only |
| Collection page (existing text) | below block | "Bottom heating for **Top 140**, Top 190, and Top 220" | US catalog: **Top 160 – Top 220** (no Top 140 in the US lineup). Left unchanged. |

## Notes

- No Nabertherm sales are recorded in Shopify (last 5 years), so the table has
  no "Best seller" badge.
- Linked only ACTIVE products with an Online Store URL. The N440 (ACTIVE but not
  on the Online Store) and N300 (UNLISTED) are mentioned in text, not linked.
  Furniture kits are UNLISTED and not linked.
