# Laguna front-loading gas kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/laguna-front-loading-gas-kilns
Metafield: `custom.abz_collection_below_descrption` on collection
`gid://shopify/Collection/441037422914`. The section is inserted right after
`<h3 id="Laguna-Front-Guide">` (the "Learn more" link in the top description
points there).

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
| LE-200-40C | Not in the store | Laguna's standard 40 cu ft car kiln. Shown in the table without a link, with "call us". |
