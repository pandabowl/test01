# Cone Art pottery kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/tucker-s-cone-art-kilns
(the "Cone Art" menu link; `cone-art-kilns` is the everything-incl.-parts page
and points visitors here). Metafield: `custom.abz_collection_below_descrption`
on collection `gid://shopify/Collection/441037128002`. The section goes after
the "Cone Art Kiln Models" overview list, right before
`<h3>Do Cone Art pottery kilns really fire to cone 10?</h3>`; the top
description's "Learn more about Cone Art kilns" button jumps to that block.

## Sources (read 2026-11-19)

- *Cone Art Kilns 2025 Product Catalog* (PDF, dated 2025-03-22, supplied by
  the user): specs pp. 10, 12, 14, 16, 18; capacity guide pp. 20-22; cut sheet
  p. 23; electrical specs p. 25.
- *Tucker's Cone Art Kilns Pottery Kiln Retail Pricelist - USD*, effective
  2026-02-15 (PDF, supplied by the user). Same specs as the catalog, plus the
  standard-feature notes used below.
- Cone Art's website could not be read: coneartkilns.com 301-redirects to
  countonconeart.com, which serves a Cloudflare bot check ("Just a moment...",
  HTTP 403) to automated fetches. Both hosts are on the allowed-hosts list.

## What matched Cone Art

Every number in the section (interior size, cu ft, cups per load, amps at
240V/208V, breaker sizes, 3-phase availability, 120V 119D with NEMA 5-20P,
hardwired 8' SOOW cord on all 240/208V models) is from the catalog and
price list, which agree with each other on every pottery spec. 17 of the
store's product spec tables match exactly (script check, all 16 sizes).

Best seller: the 2327D (store sales, last 3 years: 18 GX2327D packages,
5 GX2327D, 1 BX2327D; next is the GX2322D-SQ package at 9). Cone Art's catalog
also calls the 2327D "our most popular kiln".

## Cone Art's own sources disagree

- Floor elements: the catalog's test-kiln page says "the 1822D comes with a
  floor heating element", implying the 119D/1813D/1818D don't. The newer
  price list says "ALL Cone Art Pottery Kilns ... feature ... a heating element
  in the floor." The section follows the price list.
- Catalog text says "Model 2327's interior is 23" across"; its spec tables say
  23.5". The section uses the spec tables.

## Errors in the store's product data (not fixed; for the user)

| Product | Field | Store says | Cone Art says |
|---|---|---|---|
| BX2327D, GX2327D | spec table, inside | 23.4 x 27 | **23.5 x 27** |
| BX2318D | spec table, ship weight | 370 lb | **270 lb** |
| BX4222D | spec table, inside | 41 x 32 x 22.5 | **41 x 31 x 22.5** |
| BX4222D | spec table, ship weight | 325 lb | **625 lb** |
| BX2822D | spec table, 3-phase amps at 240V | 36.6 | **36.3** |
| BX2336D | spec table, 1-phase amps at 208V | 79.9 | **79.5** |
| GX119D | finder facts | 0.49 cu ft | **0.57 cu ft** (its own spec table says 0.57) |
| BX1813D, GX1813D | finder facts | 1.7 cu ft | **1.98 cu ft** (spec tables say 1.98) |
| BX2818D | finder facts | 6.5 cu ft | 6.66 cu ft (rounding) |
| BX1818D, BX1822D, BX2318D, BX2818D | `custom.kiln_top_cone` / finder eyebrow | blank / "Pottery" | Cone 10 |
| GX2322D, GX2327D, GX2827D, GX2322D-SQ, GX4227D packages | spec table | missing | (the GX2327D-SQ package has one) |
| BX1818D | handle | `cone-art-bx1822d-kiln` | works, but names the wrong model |

## Errors in existing page content (not changed; for the user)

`cone-art-cone-10-double-wall-automatic-electric-kilns`, spec table in the
below-grid block:

| Row | Store says | Cone Art says |
|---|---|---|
| 119D | 208V amps "19 / 21", breaker 30A | 120V only: 18 A, **20A** breaker |
| 1813D | 28 / 32 A, 40A breaker, #8 wire (the 1822D's values) | **19 / 21 A, 30A, #10** |
| 1822D | #6 wire | **#8** |
| 2818D | 3 sections | **2** |
| 4227D | 3-phase wire "4/6" | **6** |
| 2318D SQ | ship weight 350 | **310** |
| 2322D SQ | inside 23 x 23.5 x 22.5 | **23 x 23 x 22.5** |
| 2322D SQ, 2327D SQ | breaker/wire 50A, #6 | 40A/50A, #8/#6 (3-phase); #6/#4 (1-phase) |
| 2327D SQ | 8 cu ft | **8.4** |
| (missing) | no 1818D or 4222D rows | both are current models |

`tucker-s-cone-art-kilns` FAQ text: "a floor element on most models" (the
price list says all models); "roughly 30% lower electricity use" (the catalog
says 32%).

The pottery spec image on `cone-art-kilns-energy-efficient-kiln-packages`
matches Cone Art (it just leaves out the 1818D and 4222D).
