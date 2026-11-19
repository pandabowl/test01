Page: https://www.sheffield-pottery.com/collections/olympic-kilns
(collection `gid://shopify/Collection/441036341570`).

**Live since 2026-11-19 06:33 UTC as a shared comparison block** (see
`SHARED-BLOCKS.md`), not in `custom.abz_collection_below_descrption`:

- Block entry `olympic-stackable` (`gid://shopify/Metaobject/685607616883`,
  type `kiln_comparison_block`). Repo copy: `blocks/olympic-stackable.html`.
- The page's `custom.comparison_blocks` = `olympic-stackable`, then the shared
  `kiln-compare-cta` (`gid://shopify/Metaobject/685569474931`). It was empty
  before. Value: `live_comparison_blocks_2026-11-19.json`.
- The top description's "Learn more" link now points at `#olympic-stackable`
  (was `#abz_below_richtxt_id`), at the user's request. Backup and new value:
  `backup_descriptionHtml_before_2026-11-19.html`, `live_descriptionHtml_2026-11-19.html`.
- `custom.abz_collection_below_descrption` was not changed; it still renders
  below the block.
- Verified on the live page: the block, `kiln-compare-cta`, the new description
  and the untouched below text are exact matches (`tools/verify_live.py`); the
  block sits in `.sp-compare` directly above the below-text section; all 23
  page links return 200; no sideways scroll at 1280 px or 390 px; clicking
  "Learn more" scrolls to the block. The shared `kiln-compare-styles` entry had
  gained a `.spc-sub` rule from another chat since the preview; it doesn't
  affect this block.
- 2026-11-19 07:43 UTC: another chat moved the "Which Olympic kiln should I
  buy?" picks above the model-number box and table (same wording; the
  site-wide order now, as on Skutt). `blocks/olympic-stackable.html` is synced
  to that version. The shared `kiln-compare-cta` was reworded at 06:43 UTC
  ("Not sure which model fits your needs? Call our kiln experts at (888)
  774-2529."), with no claim about how long Sheffield has sold kilns.
- 2026-11-19 07:46 UTC: also on `olympic-multi-sided-electric-kilns`
  (list `olympic-stackable` + `kiln-compare-cta`, user's OK). Verified exact.
- `draft_section_2026-11-19.html` is the first draft in the old
  (below-text) format, kept for reference; it was never published.

Scope (chosen by the user 2026-11-19): the 18", 23" and 28" stackable electric
pottery kilns we sell, plus short pointers to Medallion, Freedom, oval, 120V,
FL front-loading and Dual Media pages. No best-seller badge (online order counts
are too low to call one).

## Sources

- **Olympic Kilns & Accessories Price List** (`WEB-KILNS-AND-ACCESSORIES-PRICE-LIST-1-1.pdf`,
  created 2026-10-23, modified 2026-10-30). Its spec sheets are the source for
  every number in the table: inside dims, cu ft, max temp, amps 1-phase at
  240/208V, 3-phase availability, plug/direct wire, brick thickness. Supplied by
  the user (downloaded from olympickilns.com).
- **Olympic Electric & Gas Kilns catalog 2023** (`gas.electric.catalog.2023.lowres.pdf`,
  https://www.olympickilns.com/wp-content/uploads/2023/02/gas.electric.catalog.2023.lowres.pdf).
  Used for wording only: founded 1971, Flowery Branch GA, "built in sections …
  without having to remove the entire electrical box", H models "tough and can
  handle continuous firings", Medallion green electrical box, Freedom package
  contents, HotBox cone 10 on 120V. Supplied by the user.
- **Olympic electric kiln operating manual** (June 2024):
  https://cdn.shopify.com/s/files/1/0694/7461/5526/files/Olympic_Kilns_Electric_Manual.pdf
  Model designation (width/depth digits, H = 3" brick cone 10, E = electronic
  controller, DM, FL = cubic feet), NEMA 5-15 on standard 120V outlets, breaker
  at 125% of load.

olympickilns.com is the manufacturer's domain (the manual says so on every
page; greatkilns.com is not Olympic's). It's on the allowed-hosts list, but
Cloudflare's bot check blocks all automated requests to it, PDFs included,
so the user downloaded the two PDFs in a browser.

## Table values (all from the 2026 price list)

| Model | Inside (w × d) | cu ft | Max temp | Brick | Amps 240/208 1-ph | Plug |
|---|---|---|---|---|---|---|
| 1818E / 1818HE | 17.5 × 18 | 2.63 | cone 8 / cone 10 | 2.5" / 3" | 21/24 | NEMA 6-30 |
| 1823E / 1823HE | 17.5 × 22.5 | 3.29 | cone 8 / cone 10 | 2.5" / 3" | 26.25/30 | NEMA 6-50 |
| 1827E / 1827HE | 17.5 × 27 | 3.95 | cone 8 / cone 10 | 2.5" / 3" | 31/36 | NEMA 6-50 |
| 2318E / 2318HE | 23 3/8 × 18 | 4.7 | cone 8 / cone 10 | 2.5" / 3" | 36/41 | NEMA 6-50 |
| 2323HE | 23 3/8 × 22.5 | 5.83 | cone 10 | 3" | 44/46 | NEMA 6-50 |
| 2327HE | 23 3/8 × 27 | 7 | cone 10 | 3" | 47/48 | NEMA 6-50 |
| 2331HE | 23 3/8 × 31.5 | 8.17 | cone 10 | 3" | 54/62 | Direct wired |
| 2818HE | 28.25 × 18 | 6.67 | cone 10 | 3" | 40/46 | NEMA 6-50 |
| 2823HE | 28.25 × 22.5 | 8.34 | cone 10 | 3" | 48/55 | "NEMA 6-50/Direct Wired" |
| 2827HE | 28.25 × 27 | 10 | cone 10 | 3" | 56/64 | Direct wired |
| 2831HE | 28.25 × 31.5 | 11.67 | cone 10 | 3" | 64/73 | Direct wired |

Cross-checks: amps × 240 V match Olympic's watts (e.g. 2827HE 13,440 W / 240 =
56 A). Three-phase is listed for every model except the 1818E/1818HE ("na").
The page shows the 2823HE's hookup as "NEMA 6-50 plug or direct wire" because
Olympic doesn't say which applies when; the footnote asks buyers to call.

Picks and notes: 1818HE runs on a 30-amp breaker (Olympic: breaker 30, NEMA
6-30). Medallion (MAS1818HE–MAS2827HE) inside dims and amps equal the HE models
and the price list shows it costs less. Ovals top out at 20.5 cu ft (3031HE).
1414HE: 1.4 cu ft, cone 10, NEMA 6-30.

## Olympic's own sources disagree

- Freedom 1414HE: the 2026 price list shows it at 17.5 × 18, 2.63 cu ft (the
  1818HE's numbers); the 2023 catalog says 14.5" wide × 13.5" deep. The page only
  says Freedom sizes "run from the Freedom 1414HE to the oval Freedom 2527HE".
- Freedom vent: the 2023 catalog says VentMaster; the 2026 price list says
  "Freedom Vent". The page just says "a kiln vent".
- Controllers: the 2023 catalog lists 3 Key, V6-CF, RTC-1000 and Genesis; the
  2026 price list offers KilnStar or Genesis only. The page doesn't name controllers.

## Store data fixed 2026-11-19 (at the user's request)

Spec tables inside the product descriptions (`descriptionHtml`) that didn't
match Olympic's 2026 price list. Each description was backed up first
(`product-fixes/backup_<handle>_2026-11-19.html`), only the values below were
changed, every description was read back and matched the intended HTML byte
for byte, and the live product pages show the new values.

| Product | Field | Was | Now (Olympic 2026) |
|---|---|---|---|
| 2818H | spec table, inside dims (2818 and 2818H rows) | 28 1/4 x 22.5 | 28 1/4 x 18 |
| 2827H | spec table, 2827 row max temp | Cone 8 – 23000°F | Cone 8 – 2300°F |
| 2331H | spec table, 2331H 3-phase breaker | P3= 63/41 | P3= 50/60 |
| 2323H | spec table, 2323H watts | 9600 | 10560 |
| 2323H | spec table, 2323H 1-phase breaker | P1= 50/60 | P1= 60 |
| 2318 and 2318H | spec table, 2318H watts | 8400 | 8600 |
| 2318 and 2318H | furniture kit table, row labels | 2323 / 2323H | 2318 / 2318H |

## Other store-data issues (not fixed; for the user)

| Product | Field | Store says | Olympic says |
|---|---|---|---|
| 2323H, 2331H, 2818H | spec tables | still list cone 8/cone 4 2323, 2331, 2818 | Olympic now lists these sizes as HE (cone 10) only |
| Stackable products + `olympic-multi-sided-electric-kilns` page | boilerplate text | "models 2323 and 2331 fire to cone 4" and "Every size kiln is available in a regular … or H version" | 2323, 2331, 2818, 2823 and 2831 are HE only now |
| Most stackables | spec table outside dims | 2 numbers from an older sheet (e.g. 2827H 42 x 41) | 3 numbers now (2827HE 42 x 53 x 47) |
| 1827 (cone 8) | URL handle | `…-3-29-cuft-ol1827` | 3.95 cu ft (title and finder facts are right; changing the handle needs a redirect) |
| MAS2827HE | URL handle | `…-mas28237he-…` | typo (same redirect caveat) |
| 1414HE, HB64, 1214-120 | product titles | "3 Key" controller | the 2026 price list offers KilnStar or Genesis (Spark on small HotBoxes) |
| `olympic-kilns` page | existing below-grid text | "lead times … up to 28 weeks" (2023 notice) | check with Olympic; left as is |
