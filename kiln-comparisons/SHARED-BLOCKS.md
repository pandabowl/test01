# Shared comparison blocks: method

How kiln comparison tables are stored once and shown on any number of
collection pages. Fix a spec in one place and every page that shows that block
updates. This replaces pasting a whole section into each page's
`custom.abz_collection_below_descrption` (the old method in `PLAYBOOK.md`).

Research and fact-checking don't change: `PLAYBOOK.md` steps 1–3 still apply.
This file replaces its steps 4–8 (draft, preview, publish, verify, save).

## How it works

- Each block is one Shopify **metaobject** entry of type
  `kiln_comparison_block`. A block is usually one series table (e.g. L&L
  Easy-Fire), a brand overview, or the shared call-to-action.
- Each collection has a list field, **`custom.comparison_blocks`**, that
  names the blocks it shows, in order. A brand page lists all its blocks; a
  series page lists only its own.
- One section in the theme renders that list on every collection page, directly
  above the "ABZ Collection Below text" section. On a page with an empty list
  it outputs nothing (0 px tall).
- The blocks are rendered by Liquid on the server, so search engines see them as
  normal page text.
- One entry, `kiln-compare-styles`, holds the CSS for all blocks. It is output
  once per page, before the blocks.

## The pieces

| Piece | Where | Details |
|---|---|---|
| Block type | Content > Metaobjects > "Kiln comparison block" | Type `kiln_comparison_block` (`gid://shopify/MetaobjectDefinition/48391291251`). Fields `title` (admin label) and `html` (raw HTML, multi-line text). Storefront access: public read (Liquid needs it). Not "publishable": an entry shows wherever a list includes it. |
| Shared entries | entries of that type | `kiln-compare-styles` (all CSS) and `kiln-compare-cta` (the phone call-to-action). Repo copies: `shared/`. |
| Brand blocks | entries of that type | Handle `<brand>-<series>`, e.g. `ll-easy-fire`, `ll-overview`. Repo copies: `<brand>/blocks/<handle>.html`. |
| Page list | collection metafield `custom.comparison_blocks` | Type `list.metaobject_reference`, limited to `kiln_comparison_block`; pinned on the collection admin page. Order = display order. |
| Renderer | theme `templates/collection.json`, section `sp_comparison_blocks` | An "ABZ Custom Liquid" section, padding none, placed directly above `4ab91e11-…` ("ABZ Collection Below text"). Liquid: `theme/comparison-blocks.liquid`. |
| Product list | product metafield `custom.comparison_blocks` | Same type and limit as the collection field (`gid://shopify/MetafieldDefinition/729818464627`). Shown in the product's Specifications tab; see "Product pages: Specifications tab". |
| Product renderer | theme `sections/hk-tab-section.liquid` + `snippets/sp-spec-jump.liquid` | Specifications tab content and the "See full specifications" button. Repo copies: `theme/hk-tab-section.liquid.with-spec-tab`, `theme/sp-spec-jump.liquid`. |

```liquid
{%- assign sp_blocks = collection.metafields.custom.comparison_blocks.value -%}
{%- if sp_blocks != blank -%}
<div class="sp-compare">
{{ shop.metaobjects.kiln_comparison_block['kiln-compare-styles'].html.value }}
{%- for b in sp_blocks -%}{{ b.html.value }}{%- endfor -%}
</div>
{%- endif -%}
```

Every kiln brand and series collection uses the default `collection.json`
(checked 2026-11-19: all have an empty template suffix). If a page ever uses
another collection template (`collection.abz_brand.json`, `…holiday.json`,
etc.), that template needs the same section too.

## Theme status

**Placement: reverting (owner, 2026-11-19 ~07:35 UTC: "we went too far, products need to be here").** Final placement = title and description, then products, then the comparison: the original spot directly above the below-text section. To get it, the owner publishes the backup "Comparison blocks (19-11-26)" again (checked: the live theme had no edits after 07:17, and the backup has the same product.quote.json). History: **comparison at the top was live 07:20 UTC** (the owner published "Comparison at top (19-11-26)", now the live theme; "Comparison blocks (19-11-26)" is the unpublished backup; no live-theme edits were lost, the old theme's newest file change was 05:49). Checked live: Paragon pottery and Skutt pottery show the comparison right under the title and description, with products after it; Fredrickson (no list) shows nothing extra.

Original note: the user asked for the
comparison at the top of collection pages, directly under the title and
description. Theme copy "Comparison at top (19-11-26)"
(`gid://shopify/OnlineStoreTheme/197858328947`, copied from the live theme at
07:15 UTC) moves `sp_comparison_blocks` to directly after `d445fd78-…`
(abz-main-collection-banner: title + description). Nothing else changed:
`theme/collection.json.comparison-at-top`, read back and checked. Preview:
Paragon pottery shows the comparison at 499 px and products after it. The theme
hides the description on phones, so there the comparison follows the title.
Publishing it needs the owner. Once published, the placement paragraph below
("directly above the below-text section") is out of date.

**Live since 2026-11-19 05:50 UTC.** The live theme is "Comparison blocks
(19-11-26)", `gid://shopify/OnlineStoreTheme/197853249907`. The previous live
theme, "Collection heading fixes (17-11-26)" (`…/197790761331`), is kept
unpublished as the backup. Checked after publishing:
- The home, collection and product pages all return 200 on the new theme.
- On collection pages the section sits directly before the below-text section,
  0 px tall while no list is set.
- The below-text section is at the same position as before (Fredrickson desktop
  2303 px), with no sideways scroll.
- The Skutt page still renders its below-text value exactly.

Any future theme that becomes live must keep the `sp_comparison_blocks`
section in `templates/collection.json`, or the blocks disappear from every page.
A theme copied from the live theme after 2026-11-19 05:50 already has it.

How it got there: the tools can't write to the live theme (`theme_bash` is
refused on this store, and `themeFilesUpsert` only works on unpublished themes).
So the section was added to a copy, which the owner then published:

- **Copy:** "Comparison blocks (19-11-26)" (first named "PREVIEW - …"),
  `gid://shopify/OnlineStoreTheme/197853249907`, taken 2026-11-19 04:54 UTC
  from the live theme "Collection heading fixes (17-11-26)" (`…/197790761331`).
  Its `collection.json` is the live file plus the one section (checked by
  reading it back). Another chat added `templates/product.quote.json` (a
  request-a-quote form) to the live theme at 05:17, after the copy was taken;
  that file was copied into the copy too (`theme/product.quote.json.live-2026-11-19`;
  checked equal). Every other file matched the live theme: same file
  list, and no live file edited after the copy was taken.
- **Publishing is blocked for the tools too** (`theme_publish` is refused on
  this store), so the owner clicks Publish.
- **Preview:** add `?preview_theme_id=197853249907` to any collection URL. With
  curl, use `-L` and a cookie jar; the first response is a redirect.
- `theme/collection.json.live-2026-11-19` is the live file before the change;
  `theme/collection.json.with-comparison-blocks` is the copy's file.

**To add the section to a theme by hand** (only needed if a live theme ever
lacks it; owner, about 2 minutes, in the theme editor):

1. Online Store > Themes > live theme > **Customize**.
2. Top drop-down: **Collections > Default collection**.
3. **Add section > ABZ Custom Liquid.** Paste the Liquid above (or
   `theme/comparison-blocks.liquid`) into Custom Liquid. Set Section padding to
   **None** and Divider to **None**.
4. Drag it so it sits **directly above "ABZ Collection Below text"**. Save.

Or add it to a copy and have the owner publish the copy (Online Store > Themes
> the copy > **…** > **Publish**). That's the no-code route, but first check
that nobody has edited the live theme since the copy was taken: compare the
live theme's `updatedAt` and file list with the copy's, and bring any newer
files across. Publishing throws away live-theme edits the copy doesn't have.

**Now that the section is live, setting `custom.comparison_blocks` on a
collection publishes those blocks immediately.** Don't set a list until the
blocks have been through preview and the user has said yes.

The store has about 100 themes, which is at or near Shopify's limit. Delete old
`PREVIEW -` copies before the next `themeDuplicate`.

## Block HTML rules

- **Order inside a block (owner, 2026-11-19):** `<h2>` heading, intro paragraph
  (plus `ul.spc-jump` on overview blocks), then **"Which ___ kiln should I buy?"**
  (`<h3>` + `ul.spc-picks`), then the model-number box, tables, notes and the rest.
  All 12 live blocks with picks were reordered this way on 2026-11-19/20.
- One block = one `<div class="spc-block" id="<handle>">`. The id lets
  "Learn more" links and jump lists point at it.
- **No `<style>` in brand blocks.** All CSS lives in `kiln-compare-styles`,
  scoped to `.sp-compare`. If a block needs a style that isn't there, add it to
  `kiln-compare-styles` (and `shared/`) so it works for every brand.
- Same classes as `template/comparison-section.html`: `spc-table-wrap`,
  `spc-model` (model cell; `<span>` badge inside), `spc-pop` (best-seller row),
  `spc-num` (no-wrap numbers), `spc-note`, `spc-decode` (model-number box),
  `ul.spc-picks` (buying picks), `ul.spc-jump` (pill links to other blocks),
  `spc-cta`.
- Every `<td>` except the model cell needs `data-label`. On phones each row
  becomes a two-column card; cells labelled `Inside` or `Best for` span the full
  width, so use those exact labels for the long cells.
- Specs are fact-checked against the manufacturer (`PLAYBOOK.md` step 3,
  `<brand>/FACT-CHECK.md`). No prices.
- End a page's list with `kiln-compare-cta` rather than writing the phone
  line into each block.

## How to...

**Add a brand (new tables)**

1. Research and fact-check (`PLAYBOOK.md` steps 1–3).
2. Write each block to `<brand>/blocks/<handle>.html`.
3. Preview without publishing. The draft is injected into the live page in
   the browser only, in the same wrapper and spot the theme section uses:

   ```bash
   python3 tools/build_preview.py draft.html <brand>/blocks/<a>.html <brand>/blocks/<b>.html shared/kiln-compare-cta.html
   node tools/preview_shot.js <collection-url> '.sp-compare' preview draft.html abz_below_richtxt_id before
   ```

   Look at both PNGs; `scrollWidth` must equal `innerWidth`. Send desktop +
   phone previews and the store-data errors; wait for a yes. (Before the theme
   section is live you can also set the list and view the theme copy with
   `?preview_theme_id=`; after that, setting the list publishes.)
4. Create each entry with `metaobjectCreate` (or `metaobjectUpsert`). Pass the
   HTML as a GraphQL **variable**, not inline: it avoids escaping mistakes and
   the 16,384-character limit on the query text.
5. Set `custom.comparison_blocks` on each page with `metafieldsSet`
   (type `list.metaobject_reference`, value a JSON array of metaobject GIDs).
6. Verify (below).

**Move a brand that is already embedded** (e.g. Skutt), only after the theme
section is live:

1. Read the page's `custom.abz_collection_below_descrption` exactly, with its
   `compareDigest`, and save it as a backup (`PLAYBOOK.md` step 6.1–6.2).
2. Turn the comparison part into blocks: drop the outer
   `<div id="sp-<brand>-compare">` and its `<style>`, split the rest into
   `spc-block` divs, and switch the phone labels to the conventions above.
   Check the brand's old CSS for anything `kiln-compare-styles` lacks.
3. Create the entries (step 4 above).
4. In **one** `metafieldsSet` call, set the page's `custom.comparison_blocks`
   **and** write `abz_collection_below_descrption` without the comparison (with
   `compareDigest`). The page then never shows the table twice or not at all.
   Leave the rest of the below text as it was.
5. If the top description's "Learn more" link pointed at a heading inside the
   old section (Skutt: `#SkuttPoetry-guide`), it now has no target. Ask the user
   whether to point it at the first block's id.
6. Verify, then save the blocks, the backup and the new below-text value in
   `<brand>/`.

**Fix a spec:** edit the block's `html` in Content > Metaobjects (or
`metaobjectUpdate`). Then update the repo copy and the brand's `FACT-CHECK.md`.

**Show a block on another page:** add its entry to that collection's
`custom.comparison_blocks`.

**Verify:** fetch the page with a cache-buster and run
`python3 tools/verify_live.py live.html <file>` for `shared/kiln-compare-styles.html`
and each block file: each must be an exact match. Check every link returns 200.
Screenshot with `tools/preview_shot.js` (selector `.sp-compare`); the section's
left and right edges should match the "below text" section's, with no sideways
scrolling.

## Gotchas

- `collectionByHandle` and `productByHandle` are deprecated: use
  `collectionByIdentifier` / `productByIdentifier`.
- A metaobject definition's description is limited to 255 characters.
- A big query result is saved to a file instead of shown. To get an exact copy
  of a long value, request it under several aliases to force that, then pull it
  out with `jq -j`.
- `metafieldsSet` takes at most 50 metafields per call.
- Screenshots: `preview_shot.js` hides fixed and sticky elements (headers,
  popups) but not table cells; the store's spec tables pin their first column
  with `position: sticky`, and hiding it made the model column look blank.
  `tools/spec_tab_shot.js <handle> <theme-id|live> <out>` screenshots a product's
  Description and Specifications tabs.

## Product pages: Specifications tab

Owner's request (2026-11-20): on every kiln product where it applies, the specs
live in the **Specifications tab**, and the description has a clear link that
jumps straight to them. Choices the owner made: the tab shows the product's own
spec table, then its brand comparison; spec tables move out of descriptions into
the tab (backups first); the link is added automatically by the theme at the top
of the description; each brand chat does the per-product work for its brand.

**How the theme does it** (`sections/hk-tab-section.liquid`, the product tabs):

- The Specifications tab shows when the product has `custom.specifications`
  (its own table, as before) **or** a `custom.comparison_blocks` list. Inside the
  tab: the spec table first (wrapped in `<div class="rte hk-specs-table-wrap">`),
  then the comparison blocks (in `<div class="sp-compare sp-compare--product">`,
  with the shared styles entry).
- Whenever the tab shows, the Product Description tab starts with a navy
  **"☰ See full specifications ↓"** button (`snippets/sp-spec-jump.liquid`).
  Clicking it opens the Specifications tab and scrolls to it. A link to
  `<product-url>#specifications` does the same on page load.
- The snippet also marks the current product's row in the comparison table
  (`tr.spc-current`: pale orange with a red left edge), by matching the
  `td.spc-model` link to the page URL.
- Don't add a link or button to descriptions by hand: the theme adds it.
- Don't put the comparison inside an `.rte` element: the theme's
  `.rte table th` rule outranks the block styles and turns the header row pale.
  That's why `rte` sits on the spec-table wrapper only.

**Which block each product gets** (set 2026-11-20 on 231 products; list in
`product-spec-tab/product-comparison-blocks-2026-11-20.json`):

1. The block whose table links to the product from a `td.spc-model` cell
   (164 products, plus 5 whose product type isn't a kiln type: Janus, Caldera XL,
   RM II 1210). No product is linked from two blocks.
2. Otherwise, the block of the product's family collection, e.g.
   `skutt-ceramic-kilns` → `skutt-pottery`, `l-l-easy-fire-kilns` →
   `ll-easy-fire` (62 products: packages, touchscreen versions, small kilns).
   Brand-wide collections (`olympic-kilns`, `paragon-kilns`, `evenheat-kilns`,
   `tucker-s-cone-art-kilns`, `nabertherm-kilns`) are not used for this.
3. Never the CTA, the styles entry, overview blocks or `skutt-glass-picks`.

Not covered yet (no block fits): Olympic outside the stackable line (75),
L&L outside Easy-Fire and eQuad-Pro (14), Fredrickson (11), 9 Skutt, 1 Nabertherm.
These still get the tab and button once they have `custom.specifications`.

When a brand adds a block, attach it to its products the same way (rule 1, then
rule 2) with `metafieldsSet` (50 per call at most; `type` can be left out
because the definition exists). The live theme ignores the product list until the
new theme is published; after that, setting it publishes immediately.

**Per-product work (brand chats):** `product-spec-tab/WORKLIST-2026-11-20.md`
lists each brand's kilns in three groups: A) has a tab and tables in the
description (merge, then remove), B) tables in the description only (move),
C) no spec table anywhere (build one from the manufacturer's specs). For each
product:

1. Re-read `descriptionHtml` and `custom.specifications` right before writing;
   other chats edit kiln descriptions too. Save both as the backup.
2. Move the spec section (heading, its `<style>`, the table(s), weight and
   footnotes) into `custom.specifications` (multi-line text, raw HTML). Use the
   existing format as the model (e.g. Skutt KM1027-3,
   `skutt-kiln-km1027-3-skkm10273`: `<div id="custom-specifications-section">`
   with a heading, the table and notes). Remove empty layout tables instead of
   moving them.
3. Remove that section from the description and leave the rest alone.
4. Fact-check numbers as in `PLAYBOOK.md`; list store-data errors for the
   owner instead of silently changing them.
5. Preview, get the owner's yes, write, then check the live page.

**Theme status (2026-11-20):** built on the copy "Product spec tab + comparison
(20-11-26)" (`gid://shopify/OnlineStoreTheme/197922586995`), duplicated from the
live theme "Glaze mix-and-match cart message (19-11-26)" (`…/197880349043`;
it still has `sp_comparison_blocks` after the products). Only
`sections/hk-tab-section.liquid` changed and `snippets/sp-spec-jump.liquid` was
added; both read back with matching checksums. Previewed on 17 products (one per
block, desktop and phone): tab and button show, the button opens and scrolls to
the tab, the comparison styles match the collection pages exactly (0 computed
differences), the right row is highlighted, no sideways scroll. Waiting for the
owner to publish; check the live theme for newer edits first.

## Note for the brand chats

Paste this into a brand chat that is drafting a comparison:

> The site is moving kiln comparison tables to shared blocks. Read
> `kiln-comparisons/SHARED-BLOCKS.md` on branch `claude/hopeful-meitner-1d7l0w`
> (`git fetch origin claude/hopeful-meitner-1d7l0w && git checkout FETCH_HEAD -- kiln-comparisons`).
> Keep the research and fact-check as they are. Write the section as blocks:
> one `<div class="spc-block" id="<brand>-<series>">` per series, no `<style>`
> (the shared `kiln-compare-styles` entry has the CSS), `data-label` on every
> non-model cell, with "Inside" and "Best for" for the long cells. Save them in
> `<brand>/blocks/`. Preview and wait for my yes as usual. Don't write into
> `custom.abz_collection_below_descrption`. The theme section is live, so after
> my yes, publish by creating the entries and setting `custom.comparison_blocks`
> (that makes them visible immediately).

## Status (2026-11-19)

Done:
- Block type `kiln_comparison_block` (created by the L&L chat).
- Collection list field `custom.comparison_blocks`.
- Shared entries `kiln-compare-styles` and `kiln-compare-cta`, created by the
  L&L chat. Repo copies in `shared/`, taken 2026-11-19 05:33 UTC.
- Theme copy with the renderer section. Tested on `fredrickson-kilns` with two
  L&L blocks: rendered in the right place, aligned with the page, no sideways
  scroll on desktop or phone. The test list was removed afterwards. With no
  list, the section is 0 px tall and the page matches live.
- The owner published that theme on 2026-11-19 at 05:50 UTC; checked on the
  live site (see Theme status).

- **First page on shared blocks: Laguna** (`laguna-front-loading-gas-kilns`,
  list `laguna-gas` + `kiln-compare-cta`), live 2026-11-19 06:12 UTC, published
  by the Laguna chat. Checked here: the styles and both blocks render exactly,
  in order, directly above the below-text section.
- `kiln-compare-cta` wording changed 06:04 UTC (Laguna chat, with the user's OK):
  "your space and your electrical or gas service", so it fits gas kilns too.
  `shared/kiln-compare-cta.html` updated to match.
- All ten brand chats were told about the new method on 2026-11-19 (drafts:
  publish as blocks; live tables: move when the user says go).

Not done:
- Skutt pottery moved to blocks at about 06:55 UTC (Skutt chat, with the user's OK):
  `skutt-ceramic-kilns` lists `skutt-pottery` + `kiln-compare-cta`; the embedded table was
  removed in the same save; "Learn more" points to `#skutt-pottery`. Current files are on
  branch `claude/elegant-bohr-1e5ynt` (`skutt-ceramic/`). The `..._0649_before_move.html` file
  here is only the in-between value after the 1946 sentence was removed.
- Other brands: L&L, Cone Art and Nabertherm have entries in progress. Paragon,
  Olympic and Evenheat still have drafts. Skutt, Skutt glass, Amaco and
  Nabertherm are still embedded the old way until each one moves. L&L is being drafted in its own chat
  (`ll/`, branch `claude/zealous-ptolemy-711aho`).
- Skutt and any other brands published the old way can move over afterwards.
