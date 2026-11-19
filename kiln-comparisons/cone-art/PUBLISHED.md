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
