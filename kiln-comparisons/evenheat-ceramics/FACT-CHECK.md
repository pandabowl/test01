# Evenheat ceramic kilns: fact-check

**Status: live since 2026-11-19 06:33 UTC.** Entry `evenheat-ceramic` (`gid://shopify/Metaobject/685607649651`); the page's
`custom.comparison_blocks` = [`evenheat-ceramic`, `kiln-compare-cta` (`gid://shopify/Metaobject/685569474931`)].
The top description's "Learn more" link now points to `#evenheat-ceramic` (it was `#EvenheatCeramicsKilns-guide`); before/after copies:
`../evenheat-store-fixes/fixed_2026-11-19/collection_evenheat-ceramics-kilns.description.html` and
`collection_description_after_2026-11-19.html`. Verified on the live page with `tools/verify_live.py`: the shared
styles, `blocks/evenheat-ceramic.html` and `kiln-compare-cta` render exactly, in that order, directly above the
below-grid text (whose value is unchanged), with the same left/right edges (42/1238 px desktop, 18/372 px phone) and
no sideways scroll. All links in the block return 200. Store-data errors below were fixed the same day (see note).

Page: https://www.sheffield-pottery.com/collections/evenheat-ceramics-kilns
Published as shared blocks (see `../SHARED-BLOCKS.md`): entry `evenheat-ceramic`
(`blocks/evenheat-ceramic.html`, h2 `#evenheat-ceramic-kiln-model-comparison`), then the
shared `kiln-compare-cta`, listed in `custom.comparison_blocks` on collection
`gid://shopify/Collection/441127928130`. The theme renders them directly above the
below-grid text. (First drafted as an embedded section for
`custom.abz_collection_below_descrption`; switched to blocks on 2026-11-19 when the site
moved to shared blocks.) The main `evenheat-kilns` page was left
alone (the user chose the sub-pages; it already has its own series overview table).

## Sources (read 2026-11-19)

- Evenheat model pages (each has a Specifications block: chamber size and cu ft,
  max temperature, volts/amps/watts, plug or direct wire, voltage options):
  https://www.evenheat-kiln.com/rm-810-2024, /rm-1210-2024, /rm-1210b-2024, /rm-1413,
  /rm-1813-2024, /rm-1822-2024, /rm-2322-2024, /rm-2329-2024, /rm-2922-2024,
  /rm-2929-2024, /rm-2522-2024, /rm-2541-2024, /hf-810-2024, /hf-1210-b-2024,
  /hf-1413-2024, /hf-1813-2024, /hf-1818-2024, /hf-2318-2024, /hf-2327-2024,
  /hf-2918-2024, /hf-2927-2024
- Category pages: https://www.evenheat-kiln.com/ceramic-pottery-personal,
  /ceramic-pottery-studio, /ceramic-pottery-production, /china-porcelain
- Controls: https://www.evenheat-kiln.com/controls
- RMII and HF Ceramic Kilns manual:
  https://www.evenheat-kiln.com/_files/ugd/3a9418_762419806b4a40bab4d69f1d860e1c74.pdf
- Ceramic published list price, March 1, 2026 (used only to confirm the current
  model and controller lineup; no prices on the page):
  https://www.evenheat-kiln.com/_files/ugd/3a9418_75e6b7a8e7ba42ebbbd2d154c00e17cc.pdf

## What's on the page, and where each claim comes from

- Interior, cu ft, max cone/°F, amps, plug/direct wire: model-page Specifications
  blocks, standard 240V single-phase build (120V for RM 810, HF 810, RM 1210).
- 120V kilns need a fully rated 20A breaker: model pages and manual p.3
  ("Models RM2 810, HF 810 and RM2 1210 ... must use 'Fully Rated' 20A circuit breakers").
- HF = 3" firebrick, same chamber as the RM, larger outside: every HF page
  ("3" Firebrick with No Loss of Chamber Volume"); HF 1413 page: "our 3" brick
  version of the RM 1413".
- Multi-zone control on HF 1818, 2318, 2327, 2918, 2927 and Dyna-Lift standard on
  HF 2318, 2327, 2918, 2927: those model pages.
- Rim height 33" (RM 2322, RM 2922): model pages.
- Badges quote Evenheat: RM 1822 "by far the most popular personal-sized ceramic kiln";
  HF 1818 "by far the most popular cone 10, personal-sized"; RM 2329 "our most popular
  studio model"; HF 2327 "our best selling High Fire model"; RM 1413 "our most popular
  porcelain and china painting kiln"; HF 2927 "Our Largest cone 10 Kiln"; RM 2541
  "our largest ceramic kiln".
- Controllers: Icon, Icon+, TAP II, Rampmaster II (TAP I / Icon+ / Rampmaster II on
  multi-zone HF); Rampmaster II "features dedicated buttons" (controls page).
  Quiet Drive solid-state relays are an option on the ceramic kilns.
- Voltage note: Evenheat builds HF 2318/2327/2918/2927 in 200/208/220/230V and RM
  2322 and up in 220/230V by request; 3-phase on the 23" and 29" models.

Derived by us, not stated by Evenheat: the "first two digits ≈ width, last two ≈
depth" reading. It holds for every round kiln from the 1413 up (1413 = 14.5" × 13.5",
2329 = 23.5" × 29", etc.). It doesn't hold for the 810/1210 or the oval 2541
(41" wide), so the page limits it to "the round kilns from the 1413 up".

## Evenheat's own sources disagree

- Nothing that affects the page. (RM 2522 weight is listed as "370lb. (118Kg)";
  370 lb is about 168 kg. Weight isn't on the page.)

## Errors found in the store's data

Fixed on 2026-11-19 at the user's request (details and backups in
`../evenheat-store-fixes/README.md`): the RM II 810 description (it was the HF 810's text) and
title, the 240/208 V finder labels on the 14 kilns below (`custom.kiln_power` is a fixed-choice
filter, so it was left as "240 or 208 V"), the collection text (five families, controllers,
"Eveheat"), the main-page 20A note, and the HF 1210B SEO description, which described the
RM II 810. Still open: the HF 2918 and RM II 1210 descriptions are missing some specs, and the
RM II 1210B handle.

| Product / place | Field | Store says | Evenheat says |
|---|---|---|---|
| RM II 810 | description spec block, max temp | 2300°F / Cone 8 | **2200°F / Cone 5-1/2** |
| RM II 810 | title, `custom.kiln_top_cone`, finder eyebrow | Cone 5 | Cone 5-1/2 (minor) |
| 14 ceramic products: RM II 1210B, 1413, 1813, 1822, 2322, 2329, 2922, 2929, 2522, 2541 and HF 1210B, 1413, 1813, 1818 | finder eyebrow "240/208 V", `custom.kiln_power` "240 or 208 V" | 208V available | Their Evenheat model pages don't list 208V (RM 2322 and up: 220V/230V by request; the small ones: no other voltages). Only HF 2318, 2327, 2918, 2927 list 208V. Confirm with Evenheat before promising 208V. |
| HF 2918 | description | no electrical spec | 240V, 48A, 11,520W, NEMA 6-50 (missing, not wrong) |
| RM II 1210 (china paint) | description | no chamber or electrical spec | 11.25" × 13.5", 0.86 cu ft; 120V, 19A, 2280W, NEMA 5-20 (missing) |
| Collection below text | "five families ... Evolution Series Square Kilns ... Classic Series: manual kiln sitter cone 8" | | Neither series is in Evenheat's current ceramic lineup (RM and HF only). |
| Collection below text | controllers "Set-Pro, RM3, Genesis, TAP" | | Current ceramic controls: Icon, Icon+, TAP II, Rampmaster II (TAP I on multi-zone HF). |
| Collection top + below text | "Eveheat" | typo | Evenheat |
| Main `evenheat-kilns` overview table | "120V Small Kilns ... (the 810s need a 20A circuit)" | | The RM 1210 also needs a fully rated 20A breaker (NEMA 5-20). |

Cosmetic: the RM II 1210B handle is `evenheat-rm-ii-1210-120v-china-paininting-kiln-everm1210b`
("120v", "paininting") but it's a 240V cone 8 kiln. Changing a handle changes the URL,
so leave it unless a redirect is added.
