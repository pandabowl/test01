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

Not done:
- No collection lists any blocks yet. L&L is being drafted in its own chat
  (`ll/`, branch `claude/zealous-ptolemy-711aho`).
- Skutt and any other brands published the old way can move over afterwards.
