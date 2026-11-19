# Shared comparison blocks: handoff

How kiln comparison tables are shared between a brand's main collection page and
its series pages, so one edit updates every page that shows the block. Started
for L&L (2026-11-19). Skutt still uses the older per-page method in
`PLAYBOOK.md` and can be moved over later.

## Why it works this way

- One table per **series** (e.g. L&L Easy-Fire). The brand page lists all of a
  brand's series blocks; each series page lists only its own.
- One copy of each block, stored as a Shopify **metaobject**. Fix a spec once
  and every page that lists that block shows the fix.
- The blocks are rendered by Liquid on the server, so search engines see them as
  normal page text (not injected by JavaScript).
- The old method (pasting HTML into `custom.abz_collection_below_descrption`)
  can't share: one collection's metafield can't include another's.

## The pieces

| Piece | Where | Details |
|---|---|---|
| Block type | Shopify admin > Content > Metaobjects | Definition `kiln_comparison_block` ("Kiln comparison block", `gid://shopify/MetaobjectDefinition/48391291251`). Fields: `title` (single line, the admin label) and `html` (multi-line text, the block's raw HTML). Storefront access: public read (Liquid needs it). |
| Blocks | entries of that type | Shared by all brands: `kiln-compare-styles` (the CSS, output once per page by the section) and `kiln-compare-cta` (phone call-to-action, listed last on every page). L&L: `ll-overview` (main page only: decoder, jump links, buying picks), `ll-easy-fire`, `ll-equad-pro`, `ll-efl`, `ll-school-master`, `ll-jh-crystalline`, `ll-davinci`, `ll-test-kilns`. |
| Which blocks a page shows | collection metafield `custom.comparison_blocks` | Type `list.metaobject_reference` (limited to `kiln_comparison_block`). Order = display order. Empty = nothing shown. |
| Renderer | theme `templates/collection.json` | One `abz-custom-liquid` section ("ABZ Custom Liquid"), placed directly **above** the "below rich text" section (`4ab91e11-...`). Padding: none. Every collection uses this one template, so the section shows nothing on collections without `custom.comparison_blocks`. |

The Liquid in that section:

```liquid
{%- assign sp_blocks = collection.metafields.custom.comparison_blocks.value -%}
{%- if sp_blocks != blank -%}
<div class="sp-compare">
{{ shop.metaobjects.kiln_comparison_block['kiln-compare-styles'].html.value }}
{%- for b in sp_blocks -%}{{ b.html.value }}{%- endfor -%}
</div>
{%- endif -%}
```

## Block HTML rules

- Same look as `template/comparison-section.html`, but CSS is scoped to
  `.sp-compare` (shared by all brands) instead of a per-brand id, and lives only
  in `kiln-compare-styles`. Class prefix stays `spc-`.
- Each block is one `<div class="spc-block" id="<handle>">` with its own `<h2>`,
  short intro, table (`data-label` on every non-model `<td>`), and footnote.
- Specs are fact-checked against the manufacturer (see `PLAYBOOK.md` step 3 and
  `<brand>/FACT-CHECK.md`). No prices.
- The repo keeps a copy of each block in `<brand>/blocks/<handle>.html`. After
  any edit made in Shopify admin, pull the entry back into the repo.

## Theme access (important)

- The tools may **not** write to the live (MAIN) theme. Theme writes are only
  allowed on unpublished themes, and publishing a theme is blocked.
- So the section is added to a **copy** of the live theme
  (`themeDuplicate`; the store has a 20-theme limit, so the owner frees a slot
  first). Preview with `?preview_theme_id=<copy id>` on any collection URL.
- To go live, the owner either adds the same section to the live theme in the
  theme editor (safer), or publishes the copy. Publishing the copy throws away
  any live-theme edits made after the copy was taken, so only do that if
  nobody has touched the live theme since.

## How to...

- **Fix a spec:** edit the block's `html` in Content > Metaobjects (or with
  `metaobjectUpdate`). Then update `<brand>/blocks/` and the fact-check notes.
- **Show a block on another page:** add the entry to that collection's
  `custom.comparison_blocks` list.
- **Preview before a block is in Shopify:** `python3 tools/render_blocks.py
  <brand>/blocks <handle> ... > rendered.html` reproduces the section's output;
  inject it with `tools/preview_shot.js <url> '.sp-compare' <out> rendered.html
  shopify-section-template--29972624277875__abz_collection_description_67jKkK`.
- **Verify:** fetch the live page with a cache-buster and run
  `tools/verify_live.py live.html <brand>/blocks/<handle>.html` for each block
  (and for `kiln-compare-styles`): each must be an exact match. Check every
  link returns 200. Screenshot with `tools/preview_shot.js` (selector
  `.sp-compare`).

## Status (2026-11-19)

Done:
- hotkilns.com is on the network allowlist.
- L&L store data pulled (31 active kilns; all Jupiter kilns are archived).
- `ll/FACT-CHECK.md` written (sources, L&L's own disagreements, store-data
  errors for the owner). All 10 blocks drafted in `ll/blocks/`; all 28 links
  return 200; local desktop/phone previews checked (no sideways scroll).
- Shopify: block type `kiln_comparison_block` created. Entries created (5 of
  10): `kiln-compare-cta`, `kiln-compare-styles`, `ll-overview`,
  `ll-easy-fire`, `ll-equad-pro`.

Not done yet:
1. Create the other 5 entries: `ll-efl`, `ll-school-master`,
   `ll-jh-crystalline`, `ll-davinci`, `ll-test-kilns`. Pass each file's exact
   text as a GraphQL variable (`json.dumps` of the file). Check with
   `metaobjects(type: "kiln_comparison_block")` before re-running a create:
   a call that was cut off may or may not have run. Later, verify each stored
   `html` equals its file byte for byte.
2. Create the collection metafield definition and set
   `custom.comparison_blocks` on: `l-l-kilns` (overview, all series blocks,
   CTA), and on each series page its block + CTA: `l-l-easy-fire-kilns`,
   `l-l-easy-fire-m-kilns`,
   `l-l-equad-pro-production-kiln`, `l-l-efl-series-front-loading-kilns`,
   `l-l-school-master-kilns`, `l-l-jh-series-kilns-cone-12-crystalline-glaze-kilns`,
   `l-l-davinci-series-kilns` (and test kilns on `l-l-kilns-doll-baby-series-test-kilns`).
3. Duplicate the live theme once the owner has freed a slot; add the section to
   the copy's `templates/collection.json`; send desktop + phone previews and the
   store-data errors; wait for a yes.
4. Owner puts the section on the live theme; verify, screenshot, commit
   `ll/` (blocks, FACT-CHECK.md, the copy's original `collection.json`), and
   update the Brands table in `PLAYBOOK.md`.

Update 2026-11-19 07:15 UTC (from the "Shared blocks for specs" chat; checked
against Shopify):
- The theme section `sp_comparison_blocks` is **live** (theme "Comparison
  blocks (19-11-26)"), and the `custom.comparison_blocks` definition exists. No
  theme copy is needed any more. **Setting a list now publishes immediately**,
  so lists are set only after the user's yes on the previews.
- The brand-neutral method doc and tools are on branch
  `claude/hopeful-meitner-1d7l0w` (`SHARED-BLOCKS.md`, `shared/`,
  `tools/build_preview.py`, `preview_shot.js ... before`).
- User rules: never state how long Sheffield has sold kilns (the shared CTA now
  reads "Not sure which model fits your needs? Call our kiln experts at (888)
  774-2529."). Every brand and series page lists its blocks, ending with
  `kiln-compare-cta`; once a block is approved, adding it to more pages needs no
  new approval.
- `kiln-compare-styles` is shared by every brand and others append rules: re-read
  it before any edit and keep everything in it. Repo copies in `ll/blocks/`
  were synced to Shopify at 07:15 UTC.
- L&L pages to list blocks on after approval: `l-l-kilns` (all), `l-l-easy-fire-kilns`,
  `l-l-easy-fire-kiln-packages`, `l-l-easy-fire-m-kilns`,
  `l-l-equad-pro-production-kiln`, `l-l-efl-series-front-loading-kilns`,
  `l-l-school-master-kilns`, `l-l-davinci-series-kilns`,
  `l-l-jh-series-kilns-cone-12-crystalline-glaze-kilns`,
  `l-l-kilns-doll-baby-series-test-kilns`, `craft-test-kilns-1`. Ask the user
  about `l-l-jupiter-series-kilns` (all products archived) and `l-l` (139
  products).

Open question: the L&L description's "Learn more" link jumps to
`#abz_below_richtxt_id`, which will sit just below the comparison blocks.
