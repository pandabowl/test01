# Amaco Excel: shared comparison blocks (live 2026-11-19)

| Page | `custom.comparison_blocks` |
|---|---|
| `/collections/amaco-kilns` (`gid://shopify/Collection/443935228226`) | `amaco-excel` (`gid://shopify/Metaobject/685600178547`), `kiln-compare-cta` (`gid://shopify/Metaobject/685569474931`) |
| `/collections/amaco-excel-kilns` | none (user chose not to show the table on this duplicate page) |

- Block repo copy: `amaco-excel.html` (verified byte-for-byte on the live page).
- The old embedded copy in `custom.abz_collection_below_descrption` on
  `amaco-kilns` was **deleted** in the same request that set the list (the whole
  value was the comparison, so nothing else was on it). Backup:
  `../backup_abz_collection_below_descrption_before_move_2026-11-19.html`.
- Added to the shared `kiln-compare-styles` entry (appended at the end, everything
  else kept, including another chat's `.spc-was` rules from 06:18 UTC):
  `.spc-sub` (small grey sub-line in a cell; wraps on phones). Previous value:
  `backup_kiln-compare-styles_before_amaco_2026-11-19.html`.
- Phone layout: Interior column moved before Sides so the half-width card cells
  pair up ("Inside" spans the full card width).
