# Nabertherm kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/nabertherm-kilns
(collection `gid://shopify/Collection/446611652930`).

**Since 2026-11-19 06:14 UTC the comparison is shared blocks** (see
`../SHARED-BLOCKS.md`). The page's `custom.comparison_blocks` lists, in order:

| Order | Handle | Metaobject | Repo copy |
|---|---|---|---|
| 1 | `nabertherm-overview` | `gid://shopify/Metaobject/685593624947` | `blocks/nabertherm-overview.html` |
| 2 | `nabertherm-top` | `gid://shopify/Metaobject/685593657715` | `blocks/nabertherm-top.html` |
| 3 | `nabertherm-n` | `gid://shopify/Metaobject/685593690483` | `blocks/nabertherm-n.html` |
| 4 | `kiln-compare-cta` (shared) | `gid://shopify/Metaobject/685569474931` | `../shared/kiln-compare-cta.html` |

The same write removed the embedded section from
`custom.abz_collection_below_descrption`; the rest of that text is unchanged
(`live_abz_collection_below_descrption_2026-11-19.html`). The value with the
embedded section is `backup_abz_collection_below_descrption_before_blocks_2026-11-19.html`;
the original value from before any of this work is
`backup_abz_collection_below_descrption_before_2026-11-19.html`.
Verified on the live page: shared styles, all three blocks, the CTA and the
below text are exact matches; the table appears once; every link returns 200
(the existing Kiln Buying Guide link is a 301 to a 200); left edge aligned with
the below text on desktop and phone; no sideways scroll.

The top description's "Read More!" link pointed at `#abz_below_richtxt_id`,
which comes *after* the blocks. At the user's request (2026-11-19 06:19 UTC) it now
points at `#nabertherm-kiln-model-comparison`, the overview block's heading;
clicking it lands on that heading on desktop and phone. Backup:
`backup_collection_descriptionHtml_before_2026-11-19.html`; live value:
`live_collection_descriptionHtml_2026-11-19.html` (exact match on the live page).

History: the comparison was first published embedded at the start of the
below-text value (2026-11-19 04:50 UTC, units restyled 05:39 UTC), then moved
to blocks at 06:14 UTC.

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

## Units (user request, 2026-11-19)

Every Nabertherm spec shows **standard (US) units first** at normal size, with the
metric value kept next to it in `<small>` (smaller; in the comparison section also
grey via `#sp-nabertherm-compare small{font-size:.8em;color:#666}`). Example:
`2408°F <small>(1320°C)</small>`. Metric values are Nabertherm's own published
metric figures for the same model (international catalog / web page), e.g. Top 60
inner Ø 410 × 450 mm, Top 190 Ø 590 × 680 mm, 780 × 1080 × 1160 mm, 135 kg; N range
1300 °C, N ../H 1340 °C. Nabertherm's US inch figures are rounded conversions of
these (e.g. 590 mm is printed as 23.0"), so the pairs can differ by ~1%.
Insulation thicknesses converted: 15 mm = 0.59", 20 mm = 0.79", 80 mm = 3.15".
The US spec tables were already all-standard and were left as they are.

## What matched in the store's data

The spec tables in the product descriptions of the Top 60, Top 60/R, Top 160,
Top 190 and Top 220 are copies of Nabertherm's US tables and match the catalog
exactly (including the catalog's 15-30 plug for the Top 60/R on 208V 3-phase).
The finder `facts` capacities (2.11, 5.65, 6.7, 7.76 cu ft) are correct.

## Store-data errors: fixed on 2026-11-19 (at the user's request)

Backups of every changed field are in `products/backup_*.json` (taken right
before the changes); the values now live are in `products/live_description_*.html`.
Each product description was checked against the Admin API after writing: exact
for Top 60, Top 60/R, Top 160 and N200; Top 190 and Top 220 differ only by
newlines Shopify's formatter inserts before `</li>` (no visible change). Product
pages also get `loading="lazy"` added to images by the theme, so verify product
descriptions through the API, not the live page.

| Product | Field | Was | Now |
|---|---|---|---|
| Top 60R | SEO meta description | copied from the Top 190 ("190L capacity") | Top 60/R text: 2.11 cu ft (60 L), cone 10 (2408°F), AC590 |
| Top 60R | description intro | Tmax 1300 °C; "NEMA-plug 60-50P"; 5,5 kW; 410 × 460 / 580 × 870 × 870 mm; 240 V only | Tmax 2408 °F (1320 °C); NEMA 6-30P at 240 V, 6-50P at 208 V; 5.6 kW; 16.0" × 17.8" (410 × 450 mm); 23.6" × 35.0" × 35.4" (600 × 890 × 900 mm); 240 V or 208 V |
| Top 160 | handle | `nabertherm-top-190` | `nabertherm-top-160-kiln` (Shopify redirect from the old URL, checked: 301 → 200) |
| Top 160 | `custom.pdp_vendor_part_no` | TOP190 | TOP160 |
| Top 160 | description | "160-liter chamber capacity" | "5.65 cu ft (160-liter)" |
| Top 160 | SEO meta description | "160-liter …" | "5.65 cu ft (160 L) … cone 10 … AC590" |
| Top 190 | Specifications list | 13.5 kW; Ø 600 × 670 mm (23.6" × 26.4"); 35.43 × 35.43 × 41.34 in; 200 kg (441 lbs); 190 liters; 1320°C (2408°F) | 10.0 kW; Ø 23.0" × 26.7" (Ø 590 × 680 mm); 30.7" × 42.5" × 45.6" (780 × 1080 × 1160 mm); 298 lbs (135 kg); 6.70 cu ft (190 liters); 2408°F (1320°C) |
| Top 190 | SEO meta description | "190L capacity, 1320°C max temp" | "6.70 cu ft (190 L) chamber, 2408°F (1320°C) max temp" |
| Top 190, Top 220 | Specifications / Features | B 400 controller; "ceramic fiber insulation"; elements "including floor" | AC590 touch controller; refractory brick + microporous, no ceramic fiber; wall elements, bottom heating optional |
| Top 220 | Specifications | 1320°C (2408°F) | 2408°F (1320°C) |
| N200 | description | no spec table; never said three-phase; N 100/G–N 660/H and °C advice (international copy); "N 100.. – N 300.." ranges; stainless side panels; "See page 22" | added US spec table and "three-phase only, hard-wired" note; US lineup N 200–N 440/H with °F (°C); ranges removed (standard on all US N models); galvanized side panels + stainless door cover (US catalog p. 28); AC590 |
| Top 160, Top 190, N200 | `custom.kiln_top_cone` | missing | 10 |
| Top 160, Top 190 | `finder.eyebrow` | Pottery · 240/208 V | Cone 10 · 240/208 V (matches the other top loaders) |
| N200 | `finder.eyebrow` / `custom.kiln_power` | Pottery / missing | Cone 10 · 240/208 V 3-phase / "240 or 208 V" (the field only accepts "120 V", "240 or 208 V", "Gas or propane") |
| All six | venting / insulation text | "3.15\" (80 mm)", "15 mm", "20 mm" | metric in `<small>`, inches first |
| Top 60R | description | stray "x" before the features image | removed (06:30 UTC; backup `products/backup_top60r_before_x_and_title_fix_2026-11-19.json`) |
| Top 60R | SEO title | "Nabertherm Top 60R Kiln  Top-Loading Electric Kiln \| Sheffield Pottery" (double space) | "Nabertherm Top 60R Kiln – Top-Loading Electric Kiln \| Sheffield Pottery" |
| Top 60, 60R, 160, 190, 220 | description CSS | two copies of a page-wide `<style>` (`body{margin:20px;font-family:Arial;color:#222}`, `:root` variables, unscoped `table`/`th`/`td`/`.note`/`.table-wrap` rules); the `.note` box wrapped the whole venting section (12 px grey text) | one `<style>` scoped to `.sp-spec-table` / `.sp-spec-note` (same table look as intended by the old CSS); footnote box closes after the footnotes. Live: page margin 0 (was 20 px), venting text 16 px (was 12 px). 07:17–07:47 UTC; backup `products/backup_toploaders_before_css_cleanup_2026-11-19.json` |
| Collection page (existing text) | below block | "Bottom heating for Top 140 …"; "80 mm diameter"; "300 liters" / "440 liters" | "Top 160 …"; 3.15" (80 mm); 10.59 cu ft (300 liters) / 15.53 cu ft (440 liters) |

## Not changed (for the user to decide)

- **Top 160 Yotpo data** (`yotpo.preloaded_product_filters`) still carries the
  N200's product ID. `metafieldsSet` returned no error but did not change it; the
  Yotpo app owns that field. Fix it from Yotpo (re-sync) if reviews look wrong.
- **N300** (unlisted, not on the Online Store): SEO title says "480V 3PH" and the
  part number is N300N480, so it may really be a 480V unit; `custom.voltage` says
  "240 or 208". Its description (and the N440's) still has the international
  N 100/G–N 660/H copy and °C-only advice. Neither product is on the website.
- Top loader descriptions still contain two stray `<meta>` tags
  (`<meta charset>` / `<meta viewport>`) inside a `<p>`. Left as is.
- The "Kiln Buying Guide" link in the existing page text 301-redirects to
  /blogs/ceramic-arts-blog/kiln-buying-guide (200).

## Notes

- No Nabertherm sales are recorded in Shopify (last 5 years), so the table has
  no "Best seller" badge.
- Linked only ACTIVE products with an Online Store URL. The N440 (ACTIVE but not
  on the Online Store) and N300 (UNLISTED) are mentioned in text, not linked.
  Furniture kits are UNLISTED and not linked.
