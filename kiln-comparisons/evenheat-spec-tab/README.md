# Evenheat: product Specifications tab (draft, 2026-11-20)

Task from the shared-blocks chat (owner's request, per `SHARED-BLOCKS.md` "Product pages:
Specifications tab" and `product-spec-tab/WORKLIST-2026-11-20.md` on branch
`claude/hopeful-meitner-1d7l0w`): give every Evenheat kiln a `custom.specifications` table, in the
same format as Skutt KM1027-3 (`div#custom-specifications-section`), and move the spec lists out of
the descriptions. **Nothing has been written to the store.**

- `evenheat_specs.json`: per-product specs parsed from Evenheat's model pages (sources in each
  entry's `page`).
- `tables/<handle>.html`: the proposed `custom.specifications` value for each product (Skutt's CSS
  wrapper, one row for Evenheat's standard build, and a note with Evenheat's other voltages by
  request and the 20A-breaker requirement for the 120V kilns). No links, buttons or founding-year
  claims.
- `backup_before/raw_products_2026-11-20.json`: every Evenheat ceramic and glass product's
  description, `custom.specifications` and `custom.comparison_blocks` as of 2026-11-20 ~17:20 UTC.

Coverage: 33 tables = the worklist's 34 kilns minus 3 + 1:
- not built: **Copper** (Evenheat publishes no specs) and **Studio Pro 14 : 240 Volt** (Evenheat
  publishes only the 120V figures); STP added (Evenheat page exists).
- added: **RM II 1210 China Painting** (missing from the worklist, probably because its product type is
  "China Paint Kiln").

Still to do after the owner's yes: per-product removal of the description spec lists (each
description lays them out differently), re-reading each description right before writing.
