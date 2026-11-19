"""Assemble shared comparison blocks into one draft file for preview_shot.js.

Wraps the blocks exactly as the theme section does (SHARED-BLOCKS.md): the ABZ
Custom Liquid section's padding-free wrapper, then <div class="sp-compare">,
the shared styles, and the blocks in the order given.

    python3 tools/build_preview.py draft.html ll/blocks/ll-overview.html ll/blocks/ll-easy-fire.html shared/kiln-compare-cta.html
    node tools/preview_shot.js <collection-url> '.sp-compare' preview draft.html abz_below_richtxt_id before

Styles come from shared/kiln-compare-styles.html unless --styles <file> is given
(use that to preview a change to the shared CSS).
"""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
styles = os.path.join(here, '..', 'shared', 'kiln-compare-styles.html')
if '--styles' in args:
    i = args.index('--styles')
    styles = args[i + 1]
    del args[i:i + 2]
if len(args) < 2:
    sys.exit(__doc__)
out, blocks = args[0], args[1:]

read = lambda p: open(p, encoding='utf-8').read()
html = ('<div class="section section--divider-none section--vertical-padding-none">\n'
        '<div class="sp-compare">\n' + read(styles) + '\n'
        + ''.join(read(b) for b in blocks) + '\n</div>\n</div>\n')
open(out, 'w', encoding='utf-8').write(html)
print(f'wrote {out}: styles + {len(blocks)} block(s)')
