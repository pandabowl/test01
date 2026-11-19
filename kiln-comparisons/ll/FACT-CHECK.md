# L&L kilns: fact-check

Pages: https://www.sheffield-pottery.com/collections/l-l-kilns (all series) and
the L&L series collections. The comparison is built from shared blocks (see
`../SHARED-BLOCKS.md`); the block HTML is in `blocks/`.

## Sources (read 2026-11-19)

- L&L *Potters Catalog 2026* (rev 6/24/26):
  https://hotkilns.com/sites/default/files/2026-06/Potters%20Catalog-2026-P7_0.pdf
- L&L *School Catalog 2026*: https://hotkilns.com/sites/default/files/2026-06/SCHOOL_%20Catalog_2026%20P4.pdf
  (bowl counts per load, School-Master ratings)
- L&L *Industry Catalog 2026*: https://hotkilns.com/sites/default/files/2026-06/Industry%20Catalog-2026%20P5.pdf
- Catalog page: https://hotkilns.com/kiln-catalog-downloads
- Series pages: https://hotkilns.com/kiln-series/easy-fire-kilns, `/equad-pro-kilns`,
  `/efl-kiln-series`, `/school-master-kilns`, `/jh-crystalline-kilns`,
  `/davinci-kilns`, `/doll-test-kilns`
- Model pages (electrical tab per voltage), e.g.
  https://hotkilns.com/kilns/e23t-3-pottery-kiln. All 25 active models read:
  e14S-3, e18S/M/T-3, e23S/M/T-3, e28S/M/T-3, eQ2327-3, eQ2827-3, eFL1626,
  eFL2626, eFL2635, SM23T-3, JD18-JH, e23S-JH, JD230-JH, X3227, T3427,
  DL11-D, DLH11-D, DLH11-DX, Plug-n-Fire.
- Spec sheets: eFL1626, Doll/test (DL11/DLH11), e14S-3, Plug-n-Fire
  (linked from each model page).

Basis: 240V single-phase unless noted (test kilns: their own voltage).

## What the section uses (all matched L&L)

Inside diameter/size and height, cubic feet, max cone and °F at 240V/1Ph,
amps at 240V/1Ph, plug or direct wire, brick, zones, and L&L's naming
(e = Easy-Fire, 14/18/23/28 diameter, S/M/T = 18"/22.5"/27", -3 = 3" brick).
Bowl counts (6" × 3" bowls) are from the School catalog: e23T-3 and SM23T-3 38,
eQ2827-3 74, eFL2635 128, X3227 108.

Best-seller badges are from store sales over the last two years (ShopifyQL,
net items sold): e23T-3 (51 packages + 18 kilns), Plug-n-Fire (111),
eQ2827-3 (11 + 11, vs 5 for the eQ2327-3).

## Where L&L's own sources disagree (what the page uses)

| Item | Sources | Page uses |
|---|---|---|
| eFL1626 hookup on 240V/1Ph | Catalog: NEMA 6-50 plug. Model page and spec sheet: direct wire | Direct wire |
| DL11-D plug | Catalog and spec sheet: 1,800 W, 15 A, NEMA 5-15. Model page electrical tab: 1,847 W, 15.4 A, 5-20P | 15 A, NEMA 5-15 |
| DLH11-DX plug | Catalog: 14-30. Model page and spec sheet: NEMA 6-20 | NEMA 6-20 |
| Plug-n-Fire loading | Catalog says "door"; spec sheet diagram shows "Top / Lid" and "power shuts off when the lid is opened"; series page says Top-Loading | Top-loading |
| e28T-3 cone | Model page key specs show cone 5 (the 208V/1Ph rating); electrical tab and catalog: cone 8 at 240V/1Ph, cone 5 at 208V/1Ph, cone 10 on 3-phase | Cone 8 (2280°F) at 240V/1Ph |
| School-Master cone | Model page: "Cone 1, 2080F"; catalog: "Designed for Low Fire (Cone 1), Max Cone 6 (2232°F)"; series page: "rated for Cone 6 but recommended for up to Cone 1" | "Cone 6 max (made for cone 1)" |
| X3227 capacity | Key specs and catalogs: 14.5 cu ft; model-page description: 15 cu ft | 14.5 |
| JD230-JH capacity | Key specs and catalog: 7.0; description: 6.7 | 7.0 |
| e23S-JH capacity / zones | Key specs: 4.7; description: 4.6 and "Three-Zoned" but "two Type S thermocouples" | 4.7; two zones |
| e23 diameter | Spec tables 22.3"; descriptions 22-3/8" | 22.3" |

## Errors in the store's product data (not fixed; for the owner)

| Product | Field | Store says | L&L says |
|---|---|---|---|
| Plug-n-Fire | finder facts / note | "Front-loading", "A small front-door kiln" | **Top-loading** (lid) |
| Plug-n-Fire | spec table | extra row "27 in / 28 in / 28 in / 9.9 / 50" (looks copied from Skutt KM1227-3: 9.9 cu ft, 50 bowls) | 8" × 8" × 9", **0.33 cu ft** |
| DL11-D | finder eyebrow, note, `kiln_top_cone` | Cone 6; "5-20 plug" | **Cone 5** (2170°F); **NEMA 5-15** |
| e18S-3 | spec table | no 240V or 208V single-phase rows; the row labeled 240/3P has the 208V/3Ph part number (K-E-18S3/22) and watts (4,980) | 240/1P: 5,740 W, 23.9 A, 30 A fuse, 6-50 · 208/1P: 4,980 W, 23.9 A · 240/3P: 5,740 W, 20.7 A |
| e23S-3 | spec table, 208V/3Ph amps | 24.6 | **34.6** |
| e23M-3 | spec table, 240V/1Ph fuse | 50 A | **60 A** |
| e28M-3 | spec table, USA part numbers | K-E-23MX/.. (an e23 prefix) | K-E-28M3/.. |
| e28S-3, e28T-3 | spec table part numbers | K-E-28SX/.., K-E-28TX/.. | L&L now lists K-E-28S3/.., K-E-28T3/.. |
| e28T-3 | spec table, 220V row | "48.0/td>" (broken HTML) | 48.0 |
| e14S-3 | spec table, 208V row model name | "e14S-3-240 (USA)" | e14S-3-208 |
| eQ2327-3 | spec table, 208V watts | 11,684 | 11,648 |
| eFL1626 | spec table, power connection | 6-50 and 15-50 cordsets | **Direct wired** (spec sheet and model page; see disagreement above) |
| eFL2626 | spec table, 3-phase power connection | 15-50 cordset | **Direct wire** |
| SM23T-3 | spec table | 240V/3Ph row named "e28M-240-3P / e28M-3-240-3P" (copied from e28M-3); 208V/1Ph fuse 40 A; 208V/3Ph amps 47.9 | SM23T-3-A-3Ph; **60 A** fuse; **27.9 A** |
| JD18-JH, e23S-JH | spec table, power cord | "Cord with NEMA 6-50 / 15-50 plug" | **Direct wire** |
| JD18-JH | spec table, 208V/3Ph row | volts "240/3P" | 208/3P |
| JD230-JH | spec table, 3-phase power cord | "Cord with NEMA 15-50 plug" | **Direct wire** |
| X3227D | finder facts | 15 cu ft | **14.5 cu ft** |

Collections and page text (not product data):
- `l-l-easy-fire-m-kilns` (Easy-Fire M kilns) includes the e14S-3, a short model.
- JH collection text, spec table: JD18-JH "240 Volt K.W." shows 40" (should be
  8.8); JD18-JH amps 36.1 (L&L 36.7).
- eFL collection text: "available in five sizes ranging from 4 cubic feet" (L&L
  now lists three: 6.6, 10.2, 13.7) and "except the eFL1626 208/single phase
  which is cone 5" (only the special eFL1626-208-X is cone 5).
- All 10 products on `l-l-jupiter-series-kilns` are archived.
