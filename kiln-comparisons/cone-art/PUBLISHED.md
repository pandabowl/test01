# Cone Art comparison: what is live

Published 2026-11-19 06:14 UTC as shared comparison blocks (see
`../SHARED-BLOCKS.md`). Research and store-data errors:
`../cone-art-pottery/FACT-CHECK.md` and `../cone-art-glass/FACT-CHECK.md`.

## Blocks (metaobject type `kiln_comparison_block`)

| Handle | Metaobject | Repo copy |
|---|---|---|
| `cone-art-overview` | `gid://shopify/Metaobject/685585432947` | `blocks/cone-art-overview.html` |
| `cone-art-pottery` | `gid://shopify/Metaobject/685593297267` | `blocks/cone-art-pottery.html` |
| `cone-art-glass` | `gid://shopify/Metaobject/685586022771` | `blocks/cone-art-glass.html` |
| `kiln-compare-cta` (shared) | `gid://shopify/Metaobject/685569474931` | `../shared/kiln-compare-cta.html` |

## Pages (`custom.comparison_blocks`)

| Collection | Blocks, in order | compareDigest after write |
|---|---|---|
| `tucker-s-cone-art-kilns` (`…/Collection/441037128002`, main Cone Art page) | overview, pottery, glass, cta | `b2f6bd2a…` |
| `cone-art-glass-fusing-kilns` (`…/Collection/443938341186`) | glass, cta | `d1f7a5bd…` |
| `cone-art-cone-10-double-wall-automatic-electric-kilns` (`…/Collection/443939520834`) | pottery, cta | `c5c878a7…` |

## Backups

Nothing was overwritten: `custom.comparison_blocks` was empty on all three
collections before (written with `compareDigest: null`), and
`custom.abz_collection_below_descrption` was not touched on any page. The
existing below-grid text and the "Learn more about Cone Art kilns" link are
unchanged (the link still points at `#abz_below_richtxt_id`, which now sits
below the comparison; left as is, per the user).

## Verification (2026-11-19 06:19 UTC)

- Each block entry read back from Shopify and diffed against its repo file:
  exact.
- `tools/verify_live.py` on each live page (cache-busted): every Cone Art block
  and the current `kiln-compare-styles` and `kiln-compare-cta` values are exact
  matches on all three pages.
- Note: other brand chats edited the shared entries during this work (CTA now
  says "electrical or gas service", 06:04 UTC; styles gained `span.spc-was`
  rules, 06:18 UTC). `../shared/` holds the values as of 06:19 UTC.
- All 34 product/collection links in the sections return 200; the two jump
  links (`#cone-art-pottery`, `#cone-art-glass`) have targets on the main page.
- No sideways scroll on desktop (1280) or phone (390) on any of the three pages.

## Old spec tables removed (2026-11-19 06:31 UTC, user's request)

`custom.abz_collection_below_descrption` was edited on two pages, with
`compareDigest`, to remove only the old spec listings that now sat under the
new tables:

| Page | Removed | Backup / new value |
|---|---|---|
| `cone-art-cone-10-double-wall-automatic-electric-kilns` | caption "Cone Art Pottery Kilns Models & Specifications", the HTML spec table (errors in 8 rows) and its breaker footnote; 22,152 → 4,773 chars | `../cone-art-pottery/backup_…_before_2026-11-19.html` / `../cone-art-pottery/live_…_2026-11-19.html` |
| `cone-art-glass-fusing-kilns` | caption "Cone Art Glass Kilns - Models & Specifications" and the spec image (240V/208V amps swapped); 1,276 → 1,012 chars | `../cone-art-glass/backup_…_before_2026-11-19.html` / `../cone-art-glass/live_…_2026-11-19.html` |

The backups are exact copies read three times from the Admin API. (The
storefront was briefly blocking automated requests, so they could not be
checked against the live page before the edit.) After the edit:
`verify_live.py` gives exact matches for both new values and for the Cone Art
blocks on both pages; each page now has only one table (the new block). The
packages page spec image was left as is (it's correct and that page has no
comparison block).

## Capacity sentences fixed (2026-11-19 06:36 UTC, user's request)

- `cone-art-cone-10-double-wall-automatic-electric-kilns`, below text: "ranges
  from 3.3 up to 16.5 cubic feet" → "0.57 up to 16.5" (metafieldsSet with
  compareDigest).
- `cone-art-glass-fusing-kilns`, below text (metafieldsSet with compareDigest)
  and top description (`collectionUpdate`, `descriptionHtml`; backup
  `../cone-art-glass/backup_descriptionHtml_…_before_2026-11-19.html`, checked
  exact against the live page first): "ranges from 0.69 up to 8.25 cubic feet"
  → "ranges from under 1 cubic foot up to 8.25 cubic feet".

`verify_live.py` after the edit: exact matches for all three new values and for
the Cone Art blocks on both pages; no old figures left on either page. The
`live_…_2026-11-19.html` files in `../cone-art-pottery/` and `../cone-art-glass/`
hold the current values.

## Duplicate heading removed (2026-11-19 06:58 UTC, user's request)

`cone-art-glass-fusing-kilns` top description started with
`<h2>Cone Art Glass Kilns <br>\n</h2>`, which repeated the page title (H1)
word for word. Removed with `collectionUpdate`; the rest of the description is
unchanged. Previous value: the capacity-fix version in git history
(`../cone-art-glass/live_descriptionHtml_…_2026-11-19.html` at commit 865946e);
current value: same file now. Checked live: exact match; headings are now
H1 "Cone Art Glass Kilns" then H2 "Cone Art Glass Kiln Comparison". The other
two Cone Art pages have no heading that repeats their title.

## Buying-guide cards moved up (2026-11-19 07:34/07:46 UTC, by the shared-blocks chat)

The shared-blocks chat reordered `cone-art-glass` and `cone-art-pottery` on
Shopify so the "Which … kiln should I buy?" heading and cards come right after
the intro, above the model-number box and the table. Checked 2026-11-20: a pure
reorder (same lines, same length, no wording changes). `blocks/` now holds the
live values.
