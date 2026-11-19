# Evenheat glass kilns: fact-check

**Status (2026-11-19): drafted and previewed, waiting for the go-ahead to publish.**

Page: https://www.sheffield-pottery.com/collections/evenheat-glass-kilns
Metafield: `custom.abz_collection_below_descrption` on collection
`gid://shopify/Collection/441128943938`. The section (`#sp-evenheat-glass-compare`,
h2 `#evenheat-glass-kiln-model-comparison`) is inserted at the very top of the value,
before the old `<h3 ... id="#abz_below_richtxt_id">` tagline. The top description's
"Learn more" link points to `#abz_below_richtxt_id`, which is the theme's wrapper div
(the h3's id has a stray `#`, so it never matched), so the link lands on the new section.

## Sources (read 2026-11-19)

- Evenheat model pages (Specifications block: chamber L × W × D and cu ft, max temp,
  volts/amps/watts, plug, voltage options; furniture kit shelf sizes; features):
  https://www.evenheat-kiln.com/studio-pro-14, /sp17-2024, /sp24-glass-kiln,
  /sp28-glass-kiln, /sp41-glass-kiln, /studio-pro-stp, /gts-18-2024, /gts-23-2024,
  /gts-2541-2024, /gts-41-2024, /v8-vitrigraph
  (also read, not sold here: /gts-17-2024, /gts-24-2024, /gts-28-2024)
- Category pages: https://www.evenheat-kiln.com/glass-kilns, /studio-pro-personal-size,
  /studio-pro-studio-size, /gts-top-load-personal, /gts-top-load-studio
- Controls: https://www.evenheat-kiln.com/controls
- Glass published list price, March 1, 2026 (used only to confirm the current lineup,
  the 120V/240V versions of the Studio Pro 14 and 17, and that the Copper is still
  made; no prices on the page):
  https://www.evenheat-kiln.com/_files/ugd/3a9418_25d1faa5f62741288e3a8deba1f1dd21.pdf

## What's on the page, and where each claim comes from

- Interior, cu ft, max temp, volts/amps, plug: model-page Specifications blocks.
- Loading: Studio Pro pages ("Dual Access Design ... front and top loading ...
  Simply lift the chamber to expose the entire floor. It's wall-free"); GTS pages
  ("top loading design").
- Shelf: the full shelf Evenheat sells for each model (SP14 13"×13", SP17 16"×16",
  SP24 20"×20", SP28 24"×24", SP41/GTS 2541/GTS 41 38"×22-5/8", GTS 18 15.5",
  GTS 23 21"). GTS 2541, GTS 41 and SP41 also take a two-piece half-shelf set.
- Badges/claims quote Evenheat: SP17 "our largest, and best selling personal design";
  SP41 "our largest model in the Studio Pro line"; GTS 41 "our largest top-loading
  glass kiln ... fiber lid"; GTS 23 "the original studio kiln ... Built entirely of
  firebrick"; GTS 2541 "the original oval shaped kiln ... all-firebrick ...
  Dyna-Lift"; GTS 18 "constructed completely of firebrick ... fusing, slumping,
  draping, painting and kiln-casting"; SP24/SP28 "spring lift assist"; SP28
  "4 square feet"; firebrick "stores heat in the beginning of the firing ... then
  releases heat slowly ... very calm annealing".
- Quiet Drive solid-state relays standard: SP14, SP17, SP24, SP28, SP41, GTS 18,
  GTS 23, GTS 2541, GTS 41 pages.
- Controllers: Icon, Icon+, TAP II, Rampmaster 3 (glass); Rampmaster 3 "features
  dedicated buttons" (controls page). SP24/28/41 are offered with Icon+ and TAP II only
  (price list), hence "depending on the model".
- Voltage note: SP14 and SP17 default 120V, built for 200–240V by request (and listed
  at 240V in the price list); SP24/28/41 and the GTS kilns offer 208V and 3-phase by
  request.
- STP: 8"×8"×4.5", 1800°F, 120V 12A NEMA 5-15 (standard household plug); "perfect
  for one-off projects, jewelry and creating design elements to be used in larger
  designs". V8: 8"×8"×6.5", 2300°F, 120V 12A NEMA 5-15, "designed specifically as a
  vitrigraph kiln", pots "up to 7-1/2" diameter".
- Copper: in Evenheat's 2026 glass price list (120V and 240V) but Evenheat has no spec
  page for it, so the section names it with no numbers.

## Evenheat's own sources disagree

- The 38" × 22-5/8" full shelf (SP41, GTS 2541, GTS 41) is labelled "5.2 square feet";
  38 × 22.625 = 860 sq in, about 6.0 sq ft. The SP41 half shelves (19-1/8" × 23-1/4",
  two of them) are labelled "5.44 square feet combined"; that's about 6.2 sq ft. The
  page shows shelf dimensions only, not square feet.

## Errors in the store's data (not fixed; for the user)

| Product / place | Field | Store says | Evenheat says |
|---|---|---|---|
| Studio Pro 14 : 120 Volt | description plug | NEMA 5-15P | **NEMA 5-20** (the same description says a 20A breaker is required) |
| Studio Pro 14 : 120 Volt | finder facts | "Top-loading · Test size" | Dual Access: front + top loading |
| V8 (both products) | description max temp | 2350°F (1260°C) | **2300°F (1260°C)** |
| V8 (both products) | description 120V electrical | 14A, 1680W | **12A, 1440W** |
| GTS 41 | description outer dimensions | 30.25" L × 56" W × 29.5" H (that's the GTS 2541's footprint) | **35.5" L × 45.5" W × 37" H** |
| Studio Pro 41 | description and finder note | optional shelf "884 square inches (6.14 sq. ft.)", "39.3" at its widest" | Evenheat's current SP41 full shelf is 38" × 22-5/8" (half shelves 19-1/8" × 23-1/4") |
| GTS 18-13 | description watts | 6460W | 6480W (minor) |
| GTS 18-13, GTS 23 | finder note | "top and side elements" / "top and side fire" | Evenheat's pages don't say where the elements are; verify before keeping |
| Studio Pro 14 and 17 | description, 240V version | 10A, 2400W | Not on Evenheat's pages (unverified) |
| Copper | all specs | 0.34 cu ft, 2200°F, 120V 12A / 240V 13A | No Evenheat spec page (unverified) |
| Glass descriptions and collection text | controllers | Set-Pro, RM3, Genesis, TAP | Current: Icon, Icon+, TAP II, Rampmaster 3 |
| Collection below text | "Studio Pro 15 ... runs on a 15 amp standard household outlet" | | No Studio Pro 15 in Evenheat's lineup. The Studio Pro 14 draws 15A but has a NEMA 5-20 (20A) plug. |
| Collection below text | V8 "can hold a 7.25" crucible pot" | | Pots up to **7-1/2"** diameter |
| Collection below text | "Fishbone Lampwork and Bead Annealing kiln" | | Not in Evenheat's current lineup or this collection |
| Collection top + below text; PMC collection top text | "Eveheat" | typo | Evenheat. (The PMC page's top text also says "Here you will find Eveheat glass kilns".) |
| Main `evenheat-kilns` overview table | "Small & Specialty ... 1800–2350°F" | | STP 1800°F, V8 2300°F; Copper unpublished. Should be 1800–2300°F. |

Also: a DRAFT duplicate product `evenheat-glass-kiln-gts-23` sits in this collection
(not linked). The GTS 18-13 title/handle and the GTS 2541 handle
(`...-gts-2541-9-and-2541-13-...`) carry older names; Evenheat now calls them GTS 18 and
GTS 2541, each 13.5" deep. Changing a handle changes the URL, so leave the handles alone.
