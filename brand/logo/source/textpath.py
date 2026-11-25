"""Shape text with HarfBuzz and emit SVG path outlines (no font dependency in output)."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

import os
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep
_cache = {}


def _load(name):
    if name not in _cache:
        path = FONT_DIR + name
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        font = hb.Font(face)
        tt = TTFont(path)
        _cache[name] = (font, tt, tt["head"].unitsPerEm)
    return _cache[name]


def text_path(text, font_name, size, x=0.0, y=0.0, tracking=0.0, features=None, extra=None):
    """Return (d, advance_width, (xmin, ymin, xmax, ymax)) for text with baseline at y.

    tracking is in em units (e.g. 0.2 = 20% of size added after every glyph but the last).
    """
    font, tt, upem = _load(font_name)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    bpen = BoundsPen(gs)
    cx = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        gname = order[info.codepoint]
        ox = x + (cx + pos.x_offset) * scale
        oy = y - pos.y_offset * scale
        t = (scale, 0, 0, -scale, ox, oy)
        gs[gname].draw(TransformPen(pen, t))
        gs[gname].draw(TransformPen(bpen, t))
        cx += pos.x_advance
        if i < n - 1:
            cx += tracking * upem
        if extra and i in extra:
            cx += extra[i] * upem
    return pen.getCommands(), cx * scale, bpen.bounds
