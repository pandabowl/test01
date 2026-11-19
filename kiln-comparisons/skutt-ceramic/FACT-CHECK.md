# Skutt pottery kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/skutt-ceramic-kilns
Since 2026-11-19 06:50 UTC the comparison is the shared block `skutt-pottery`
(`gid://shopify/Metaobject/685613220211`, repo copy `blocks/skutt-pottery.html`),
listed with `kiln-compare-cta` in the collection's `custom.comparison_blocks`.
Before that it was embedded in `custom.abz_collection_below_descrption`
(backups in this folder). The top description's "Learn more" points at
`#skutt-pottery`. In the block, the Interior column comes before Sides so the
phone cards pair up (Inside is full width).

## Sources (read 2026-11-19)

- Skutt *Ceramic Kiln and Wheel Catalog 2023*:
  https://skutt.com/images/Ceramic-Kiln-and-Wheel-Catalog-2023-web.pdf
  (embedded on https://skutt.com/skutt-resources/catalogs/ceramic-kilns/)
- Skutt model pages, e.g. https://skutt.com/products-page/ceramic-kilns/km-1027-3/
  (they list interior size, cubic feet and "tea bowls" per load)

## What matched Skutt

Sides, depths, tea bowls per load, cone ratings at 240V single-phase, amps,
NEMA 6-50 plugs, PK direct wire, KM1627-3PK three-phase only, and the
model-number explanation (KM / KMT, first digits = bricks around / sides,
last two = depth, -3 = 3" brick vs. standard 2-1/2", PK = Production Kiln).

## Corrected on the page (2026-11-19)

- KM818 capacity is 2.6 cu ft (only the KM818-3 is 2.3).
- KM614-3 runs on 115 volts (we had 120).
- Buying-advice cards: Shopify sales since Jan 2023 show the KMT1027-3 package is the
  best-selling Skutt kiln (222 units; KM1027-3 kiln only: 76) and the KMT822-3 package
  is second (122). The "Most popular" card now names the KMT1027-3 package, and the
  "First kiln" card mentions the KMT822-3 package.

## Skutt's own sources disagree

- 8-sided interior width: catalog says 17.5" (16.5" with 3" brick); model pages
  say 18" (17"). The page uses the model pages.
- KM822-3 capacity: catalog 2.8, model page 2.9. KM1022-3: catalog 5.2, model
  page 5.25. KM1627-3PK width: catalog 30.75", model page 31". The page uses the
  model pages.

## Product spec tables fixed (2026-11-19)

Every product in `skutt-ceramic-kilns` was checked row by row against Skutt's
figures with `spec_check.py` (run it on a saved GraphQL export of the
collection's products with their `custom.specifications` metafield). 14
products had errors in `custom.specifications`; all were corrected, read back
byte for byte, and re-checked (0 errors left). Originals are in
`backup_product_specifications_before_2026-11-19.json`.

| Product(s) | Was | Now (Skutt) |
|---|---|---|
| KM1027-3, KMT1027-3 | 208V 1-phase: Cone 6, 2250°F; cu ft 7 | Cone 10, 2350°F; 6.4 cu ft |
| KM818 | 2.3 cu ft (spec and capacity tables) | 2.6 cu ft |
| KMT818 | capacity table 17" × 17", 2.3 cu ft | 18" × 18", 2.6 cu ft |
| KM818-3, KM818-30A-3, KMT818-3, KMT818-30A-3 | 30-amp rows: Cone 10, 2300°F (KMT: 208V 21.7 A) | Cone 8, 2300°F; 208V 24.0 A |
| KM1227-3PK | 240V 3-phase 640 A; one row with blank phase | 40 A; phase 3 |
| KMT1227-3PK | two duplicate rows with swapped amps (240V 69 A, 208V 60 A); 3-phase rows "Cone 1" | duplicates removed; Cone 10 |
| KM1022, KM1022-3 | 3-phase 208V row labeled 240V | 208V |
| KM1627-3PK | 26,300 W; capacity table copied from KM818 | 23,600 W; 27" deep, 46" × 31", 18.5 cu ft, 99 bowls |
| KM1627-3PK-LF | cone 10 rows 26,300 W | 23,600 W |

## Still open (not changed)

- KM1427-3PK has no spec table. Skutt lists the model (12.75 cu ft, 27" deep).
- KMT1227-3PK: the two single-phase rows show ship dims "0x0x0" and 425 lb
  (the 3-phase rows say 42x45x44, 410 lb).
- Descriptions (`descriptionHtml`) weren't audited, only the spec tables.
