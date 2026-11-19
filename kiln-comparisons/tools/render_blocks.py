"""Render shared comparison blocks the way the theme's Liquid section does.

The ABZ Custom Liquid section (see SHARED-BLOCKS.md) outputs:
    <div class="sp-compare">\n + kiln-compare-styles + each listed block + </div>
inside the section's own wrapper div. Use the output for browser previews
(tools/preview_shot.js) before the blocks exist in Shopify.

    python3 render_blocks.py <blocks-dir> <handle> [<handle> ...] > rendered.html
"""
import os
import sys

blocks_dir, handles = sys.argv[1], sys.argv[2:]


def read(handle):
    with open(os.path.join(blocks_dir, handle + '.html'), encoding='utf-8') as f:
        return f.read()


out = ('<div class="section section--divider-none section--vertical-padding-none">'
       '<div class="sp-compare">\n' + read('kiln-compare-styles')
       + ''.join(read(h) for h in handles) + '</div></div>')
sys.stdout.write(out)
