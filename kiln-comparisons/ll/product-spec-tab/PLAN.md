# L&L product pages: move spec tables into the Specifications tab

Task relayed from the "Shared blocks for specs" chat (2026-11-20). The owner's
rule: on kiln product pages the specs belong in the Specifications tab
(`custom.specifications`, then the brand comparison block). The theme copy
"Product spec tab + comparison (20-11-26)" (`197922586995`, unpublished) adds the
tab layout and a "See full specifications" button; nothing here adds a link.

**Status: drafted and previewed only. Nothing has been written to Shopify.**
Waiting for the owner's yes.

- `backup-2026-11-20/`: `descriptionHtml` and `custom.specifications` for each
  product, read 2026-11-20 ~17:05 UTC. Re-read right before writing; another
  chat may have edited a description since.
- `drafts/`: the proposed new values (`build_spec_drafts.py` makes them from the
  backups). Each new description is the old one with one block cut out; nothing
  else in it changes.
- `spec_preview.js`: injects a draft into the theme copy in the browser only
  (`?preview_theme_id=197922586995`) and screenshots both tabs, desktop + phone.

## What changes

**B. Ten packages: table in the description, no Specifications tab.** Each
description ends with `<p><meta …></p>`, a ~6.5 KB `<style>` with **unscoped page-wide
rules** (`* { margin:0; padding:0 }`, `body {…}`), and a `div.container` with the
electrical table. That whole block is cut out (the rest of the description is
unchanged), which also stops that CSS leaking onto the page.
The new `custom.specifications`:

| Package | New Specifications tab |
|---|---|
| e18M-3, e18T-3, e23M-3, e23S-3, e23T-3, e28M-3, e28S-3, e28T-3 packages, eQ2827-3 package | exact copy of the matching kiln-only product's existing tab (same rows; the e18M-3 package differed only by a missing space) |
| e18S-3 package | its own table (more complete than the kiln-only tab), in the same standard wrapper |

**A. Two products: Specifications tab AND tables in the description.**
- `e23T-3` (kiln only): the description's "Specifications" heading and 33-row
  table (temperature, dimensions, construction, controls…) move into the tab,
  above the electrical table, which is retitled "Electrical specifications". Three
  scoped CSS rules are added so the two-column table wraps text.
  **Owner's call:** the "Ordering & Shipping" table (weights, class, crate size)
  is left in the description for now.
- `e23S-JH`: the electrical table in the description is identical to the existing
  tab, so it (and its unscoped CSS) is just removed from the description.
  **Owner's call:** the description also has a JH-series table (JD18-JH,
  e23S-JH, JD230-JH, JD2927-JH) with errors (below). Move it to the tab as-is,
  or drop it (the L&L JH comparison block will cover the series)?

Previews checked: e28M-3 package, e18S-3 package, e23T-3 kiln. Desktop and phone,
no sideways scrolling. The spec tables scroll sideways inside their box on phones,
as the existing tabs already do.

## Store-data errors found (not fixed)

- e18S-3 package table: row labeled "e18S-3-208-3P / 208/3P" (K-E-18S3/21, 4,980 W,
  23.9 A, 6-50 cord) is L&L's **208V single-phase** row; row labeled
  "e18S-3-240-3P / 240/3P" (K-E-18S3/22, 4,980 W, 20.7 A) is L&L's **208V
  three-phase** row.
- e18S-3 kiln-only tab: missing the 240V and 208V single-phase rows (see `../FACT-CHECK.md`).
- e28M-3 tab (and so the e28M-3 package copy): USA part numbers K-E-23MX/..
  (an e23 prefix); L&L lists K-E-28M3/.. Copying it carries the error to the
  package unless the owner wants both fixed.
- e28M-3 package description "Specifications and Features" list: "Power Hook Up:
  Single phase only" (L&L offers three-phase with a 15-50 plug).
- e23T-3 kiln description table: outside dimensions "32" wide by 40" high by 45"
  deep" (L&L: 30" W × 68" H × 40" D); "c-UL-us listed" (L&L: c-ETL-us listed to
  UL 499); shipping weight 365 lb (L&L catalog: 380 lb kiln, 470 lb with kit).
- e23S-JH description JH-series table: JD18-JH "240 Volt K.W." = 40" (8.8 kW);
  JD18-JH 240V/1Ph 36.1 A (L&L 36.7); e23S-JH 240V three-phase "n/a" (L&L lists
  41.5 A); JD230-JH inside diameter 23-2/3" (L&L 23.3"); JD2927-JH "29'" and the
  JD2927-JH is archived; "Fule" typo.
- `custom.comparison_blocks` on the SM23T-3 School-Master product is `ll-easy-fire`
  (set by the shared-blocks chat); the School-Master isn't in that table. It
  should be `ll-school-master` once that block exists, or empty until then.
- Product descriptions carry a callout box ending "Sheffield Pottery · Since 1946"
  (seen on the e28M-3 package). The owner's rule bans claims about how long
  Sheffield has sold kilns; check whether this counts.
