# Paragon pottery kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/paragon-pottery-and-ceramics-kilns
(collection `gid://shopify/Collection/441785844034`).

Published 2026-11-19 as a shared block (see `../SHARED-BLOCKS.md`), not in
`custom.abz_collection_below_descrption` (left unchanged):

- Block `paragon-pottery` (`gid://shopify/Metaobject/685599162739`), repo copy
  `blocks/paragon-pottery.html`.
- Page list `custom.comparison_blocks` = `[paragon-pottery, kiln-compare-cta]`
  (it was empty before).
- The top description's "learn more" link now points at `#paragon-pottery`
  (was `#pargon-guide`). Before/after: `backup_descriptionHtml_before_2026-11-19.html`,
  `live_descriptionHtml_2026-11-19.html`.
- The main Paragon page (`paragon-kilns`) lists `[paragon-compare-links,
  kiln-compare-cta]`: a link box pointing here and to the glass page
  (`../paragon-main/blocks/paragon-compare-links.html`).
- Added `.sp-compare td.spc-model span.spc-was` (grey "was TnF-…" line, light on
  phones) to the end of the shared `kiln-compare-styles` entry.

Verified on the live page with `tools/verify_live.py` (block, shared styles,
CTA and description all exact), all 36 section links return 200, and the
"learn more" link scrolls to the block.

## Sources (read 2026-11-19)

Paragon's site is now **paragonkilns.com** (paragonweb.com 301-redirects there;
both are on the allowed-hosts list). Each product page has a "Specifications"
tab whose content is a spec-sheet image. Every number in the table comes from
these spec sheets (240V single-phase versions):

| Model (our name) | Paragon product page | Spec sheet |
|---|---|---|
| CT81713 (TnF-16-13-3) | https://paragonkilns.com/products/ct81713-ceramic-and-pottery-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT81713-specs.png |
| CT81722 (TnF-82-3) | https://paragonkilns.com/products/ct81722-ceramic-and-pottery-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT81722-specs.png |
| CT102322 (TnF-23-3) | https://paragonkilns.com/products/ct102322-ceramic-and-pottery-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT102322-specs.png |
| CT102329 (TnF-24-3) | https://paragonkilns.com/products/ct102329-ceramic-and-pottery-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT102329-specs.png |
| CT122822 (TnF-27-3) | https://paragonkilns.com/products/ct122822-ceramic-and-pottery-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT122822-specs.png |
| CT122829 (TnF-28-3) | https://paragonkilns.com/products/ct122829-ceramic-and-pottery-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT122829-specs.png |
| Viking 24 (CT102329 Heavy Duty) | https://paragonkilns.com/products/ct102329-viking-ceramic-and-pottery-heavy-duty-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT102329Viking-specs.png |
| Viking 27 (CT122822 Heavy Duty) | https://paragonkilns.com/products/ct122822-viking-ceramic-and-pottery-heavy-duty-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT122822Viking-specs.png |
| Viking 28 (CT122829 Heavy Duty) | https://paragonkilns.com/products/ct122829-viking-ceramic-and-pottery-heavy-duty-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/CT122829Viking-specs.png |
| Iguana | https://paragonkilns.com/products/iguana-ceramic-and-pottery-front-loading-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/Iguana-specs.png |
| Dragon 24 | https://paragonkilns.com/products/dragon24-ceramic-and-pottery-front-loading-kiln | https://cdn.shopify.com/s/files/1/0700/2288/9700/files/Dragon24-specs.png |
| Caldera, Xpress Q-11 (mentioned) | see `../paragon-glass/FACT-CHECK.md` | |

The descriptions on the same pages were used for: "CT Series—short for Ceramic
Top", 3" firebrick, SSR, AOP vent outlet and pre-drilled vent hole, pinless
element grooves (every CT); LiteLid (10- and 12-sided); sectional construction
(CT102329, CT122822, CT122829); Viking upgrades ("higher amperage-rated
electrical components", "industrial-grade relays and wiring"); Janus glass and
pottery modes. The spec-sheet alt text gives the old model names (e.g. CT102322 =
"Kiln model TNF233" = TnF-23-3).

"Best seller" on the CT122822: Shopify analytics, net items sold over the last
730 days. It is the top Paragon pottery kiln (4 sold); small numbers.

## What's on the page (from the spec sheets)

| Model | Inside (W × depth) | Cu ft | Max temp | Amps | Hookup |
|---|---|---|---|---|---|
| CT81713 | 16.5" × 13.25" | 1.75 | 2350°F | 27 | 6-30 |
| CT81722 | 16.5" × 22.25" | 2.95 | 2350°F | 30 | 6-50 |
| CT102322 | 22.5" × 22.25" | 5.1 | 2350°F | 40 | 6-50 |
| CT102329 / Viking 24 | 22.5" × 29" | 7.1 | 2350°F | 48 / 60 | 6-50 / direct wire |
| CT122822 / Viking 27 | 28" × 22.25" | 8.11 | 2350°F | 48 / 60 | 6-50 / direct wire |
| CT122829 / Viking 28 | 28" × 29" | 10.57 | 2350°F | 48 / 60 | 6-50 / direct wire |
| Iguana | 18" × 18" × 22.5" H | 4.2 | 2350°F | 45 | 6-50 |
| Dragon 24 | 24" × 24" × 27" H | 9.0 | 2350°F | 68 | direct wire |

Viking wattage 14,400 on all three sheets. All sheets list the Sentinel
SmartTouch controller.

## Paragon's own sources disagree (the page uses the spec sheets)

- CT interior widths: descriptions say 17" and 23"; spec sheets 16.5" and 22.5".
  The model numbers use the rounded figures, so the page calls them "approximate".
- Viking 28 (CT122829 Heavy Duty) description: "48-amp upgrade"; spec sheet 60 A,
  14,400 W (same as the other Vikings).
- Dragon 24 description: 16,500 W; spec sheet 16,225 W, 68 A.
- Iguana description: 4.1 cu ft; spec sheet 4.2 cu ft.
- CT81713 description: 6,400 W; spec sheet 6,408 W (not on the page).

## Errors in the store's product data (not fixed; for the user)

| Product | Field | Store says | Paragon says |
|---|---|---|---|
| CT102322 (was TnF-23-3) | description spec block | 43 A, 10,270 W | **40 A, 9,600 W** |
| CT102329 (was TnF-24-3) | spec table + finder facts | 6.70 / 6.7 cu ft | **7.1 cu ft** (its headline already says 7.1) |
| Viking 24 | spec table | 6.70 cu ft | **7.1 cu ft** |
| CT122829 (was TnF-28-3) | spec table | 45 A, 10,800 W, 60 A breaker | **48 A, 11,500 W** (its own text says 48 A) |
| CT122829 (was TnF-28-3) | finder note | "rated to 2150°F" | **2350°F, cone 10** (`kiln_top_cone` is empty) |
| Janus 1613 | description | 20 A, 4,800 W | **30 A, 6,240 W** (CT81713 Janus sheet) |
| Janus 23 | description + chamber table | 37 A, 8,918 W; 20.25" deep | **42 A, 10,007 W; 22.25" deep** |
| Dragon (kiln and package) | spec table | 69 A, 16,500 W | spec sheet 68 A, 16,225 W (matches Paragon's own description, so low priority) |

Other notes:
- The existing below-text block on this page promises a free upgrade to the
  Bartlett Genesis Mini controller for kilns with a 3-key controller. Paragon now
  ships these kilns with its Sentinel SmartTouch. Possibly out of date; left alone.
- The Sheffield Pottery Bull Elk (Studio and Pro packages) is not on Paragon's
  site, so it is mentioned without specs.
- Paragon also sells a "TNF Standard" line (mechanical relays, Paragon Blue,
  sold only by Paragon). Sheffield doesn't list it; not included.
