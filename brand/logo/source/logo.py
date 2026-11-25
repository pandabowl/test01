"""Build the Sheffield Pottery logo-refresh SVG suite (all text outlined to paths)."""
import math
import os
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

from emblem import emblem_group
from textpath import _load, text_path

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)

# Palette: the two original brand colors are kept exactly; cream added for reverses.
KILN = "#DF422C"      # original brand red-orange
CHAR = "#231F20"      # original charcoal
SLATE = "#5E5856"     # warm gray for the tagline (original used a cool #6D6F71)
CREAM = "#F6EFE6"     # reverse / on-dark text

WORD_FONT = "BarlowCondensed-BlackItalic.ttf"
TAG_FONT = "Barlow-SemiBold.ttf"
RING_FONT = "BarlowCondensed-Bold.ttf"
WORD = "Sheffıeld Pottery"   # dotless i: the dot is replaced by a brand triangle


def i_dot_box(size):
    """Bounds of the dot of 'i' in the wordmark font, at `size`, glyph origin at 0,0 (y up)."""
    _, tt, upem = _load(WORD_FONT)
    rec = RecordingPen()
    tt.getGlyphSet()["i"].draw(rec)
    # split into contours, keep the highest one (the dot)
    contours, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op == "closePath":
            contours.append(cur)
            cur = []
    best = None
    for c in contours:
        bp = BoundsPen(None)
        for op, args in c:
            getattr(bp, op)(*args)
        if best is None or bp.bounds[1] > best[1]:
            best = bp.bounds
    s = size / upem
    return tuple(v * s for v in best)


I_GAP = {4: 0.035}   # a little air between the second f and the dotless i (glyph index 4 = 2nd f)


def wordmark(x, baseline, size, color, accent):
    d, adv, bounds = text_path(WORD, WORD_FONT, size, x, baseline, tracking=-0.005, extra=I_GAP)
    # pen position of the dotless i = advance of "Sheff" + the extra gap
    _, pre_adv, _ = text_path("Sheff", WORD_FONT, size, 0, 0, tracking=-0.005)
    pre_adv += -0.005 * size + I_GAP[4] * size
    x0, y0, x1, y1 = i_dot_box(size)
    w = (x1 - x0) * 1.18
    h = w * 0.9
    cx = x + pre_adv + (x0 + x1) / 2 + w * 0.06
    base = baseline - y0
    slant = h * math.tan(math.radians(7))   # lean the apex with the italic
    tri = (f"M{cx - w/2:.2f},{base:.2f} L{cx + w/2:.2f},{base:.2f} "
           f"L{cx + slant*0.5:.2f},{base - h:.2f} Z")
    svg = (f'<path fill="{color}" d="{d}"/>'
           f'<path fill="{accent}" stroke="{accent}" stroke-width="{size*0.02:.2f}" stroke-linejoin="round" d="{tri}"/>')
    return svg, adv, bounds


def tagline(x, baseline, size, color, accent, target_width=None):
    parts = ["MINING", "RAW & MOIST CLAY", "SUPPLIES"]
    track = 0.16
    sep_gap = size * 0.95          # space each side of a separator triangle
    def natural(tr):
        ws = [text_path(p, TAG_FONT, size, 0, 0, tracking=tr)[1] for p in parts]
        return ws, sum(ws) + 2 * (2 * sep_gap)
    ws, total = natural(track)
    if target_width:
        # solve tracking so the line spans exactly target_width
        letters = sum(len(p) - 1 for p in parts)
        track += (target_width - total) / (letters * size)
        ws, total = natural(track)
    out, cx = [], x
    tri_h = size * 0.62
    for i, p in enumerate(parts):
        d, adv, _ = text_path(p, TAG_FONT, size, cx, baseline, tracking=track)
        out.append(f'<path fill="{color}" d="{d}"/>')
        cx += adv
        if i < len(parts) - 1:
            mx = cx + sep_gap
            top = baseline - size * 0.7 + (size * 0.7 - tri_h) / 2
            out.append(f'<path fill="{accent}" d="M{mx - tri_h*0.58:.2f},{top + tri_h:.2f} '
                       f'L{mx + tri_h*0.58:.2f},{top + tri_h:.2f} L{mx:.2f},{top:.2f} Z"/>')
            cx = mx + sep_gap
    return "".join(out), total


def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n{body}\n</svg>\n')


def write(name, w, h, body, title="Sheffield Pottery"):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg_doc(w, h, body, title))


# ---------------------------------------------------------------- horizontal
def horizontal(emblem_color, word_color, tag_color, accent, uid):
    pad = 8
    ex, ey = pad, pad
    wx = ex + 120 + 20
    size = 84
    wm, wadv, wb = wordmark(wx, ey + 71, size, word_color, accent)
    # italic overhang: align tagline to the visual left/right of the wordmark
    left, right = wb[0], wb[2]
    tg, tw = tagline(left + 2, ey + 106, 17, tag_color, accent, target_width=(right - left) - 6)
    body = emblem_group(emblem_color, uid=uid, x=ex, y=ey) + "\n" + wm + "\n" + tg
    return body, right + pad, 108 + 2 * pad


def stacked(emblem_color, word_color, tag_color, accent, uid):
    size = 86
    _, wadv, wb = wordmark(0, 0, size, word_color, accent)
    ww = wb[2] - wb[0]
    pad = 10
    W = ww + 2 * pad
    es = 1.5
    ex = W / 2 - 60 * es
    body = emblem_group(emblem_color, uid=uid, x=ex, y=pad, scale=es)
    base = pad + 108 * es + 84
    wm, _, wb2 = wordmark(pad - wb[0], base, size, word_color, accent)
    tg, tw = tagline(pad + 2, base + 38, 17, tag_color, accent, target_width=ww - 6)
    return body + "\n" + wm + "\n" + tg, W, base + 38 + pad + 2


# ---------------------------------------------------------------- seal
def arc_text(text, font, size, cx, cy, r, center_deg, tracking, color, bottom=False):
    """Set outlined text along a circle. Angles: 0 = top, clockwise. bottom=True reads left-to-right along the bottom."""
    _, total, _ = text_path(text, font, size, 0, 0, tracking=tracking)
    out = []
    # per-glyph placement using cumulative advances from the shaped run
    pen = 0.0
    for i, ch in enumerate(text):
        d, adv, _ = text_path(ch, font, size, 0, 0)
        if ch != " ":
            mid = pen + adv / 2
            if not bottom:
                ang = center_deg + math.degrees((mid - total / 2) / r)
                rad = math.radians(ang)
                px, py = cx + r * math.sin(rad), cy - r * math.cos(rad)
                out.append(f'<path fill="{color}" transform="translate({px:.2f},{py:.2f}) rotate({ang:.2f}) '
                           f'translate({-adv/2:.2f},0)" d="{d}"/>')
            else:
                ang = center_deg - math.degrees((mid - total / 2) / r)
                rad = math.radians(ang)
                px, py = cx + r * math.sin(rad), cy - r * math.cos(rad)
                out.append(f'<path fill="{color}" transform="translate({px:.2f},{py:.2f}) rotate({ang - 180:.2f}) '
                           f'translate({-adv/2:.2f},{size*0.7:.2f})" d="{d}"/>')
        pen += adv + tracking * size
    return "".join(out)


def seal(ring, ink, center, uid):
    R = 150
    cx = cy = R + 4
    teeth = 72
    pts = []
    for k in range(teeth * 2):
        a = math.pi * 2 * k / (teeth * 2)
        rr = R if k % 2 == 0 else R - 5
        pts.append(f"{cx + rr*math.sin(a):.2f},{cy - rr*math.cos(a):.2f}")
    body = [f'<path fill="{ring}" stroke="{ring}" stroke-width="1.2" stroke-linejoin="round" d="M{" L".join(pts)} Z"/>']
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{R-15}" fill="none" stroke="{ink}" stroke-width="1.6"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{R-58}" fill="{center}"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{R-64}" fill="none" stroke="{ring}" stroke-width="1.4"/>')
    body.append(arc_text("SHEFFIELD POTTERY", RING_FONT, 30, cx, cy, R - 47, 0, 0.16, ink))
    body.append(arc_text("SHEFFIELD, MASS.", RING_FONT, 27, cx, cy, R - 46.3, 180, 0.16, ink, bottom=True))
    for side in (-1, 1):  # triangle stars at 9 and 3 o'clock
        x = cx + side * (R - 36.5)
        body.append(f'<path fill="{ink}" d="M{x-6:.2f},{cy+4.5:.2f} L{x+6:.2f},{cy+4.5:.2f} L{x:.2f},{cy-6:.2f} Z"/>')
    s = 0.92
    body.append(emblem_group(ring, uid=uid, x=cx - 60 * s, y=cy - 64 * s, scale=s))
    d, adv, _ = text_path("SINCE 1946", RING_FONT, 17, 0, 0, tracking=0.26)
    body.append(f'<path fill="{ring}" transform="translate({cx - adv/2:.2f},{cy + 58:.2f})" d="{d}"/>')
    return "\n".join(body), 2 * cx, 2 * cy


# ---------------------------------------------------------------- app icon / favicon
def app_icon(bg, tri, uid, rounded=True):
    """Simplified mark for tiny sizes: the triangle with just the pot on the wheel."""
    from emblem import TRI, TRI_STROKE, POT, WHEEL_HEAD, WHEEL_BODY
    S = 512
    s = 2.85                    # triangle scale inside the tile
    tx, ty = S / 2 - 60 * s, S / 2 - 58 * s
    bgel = (f'<rect width="{S}" height="{S}" rx="{112 if rounded else 0}" fill="{bg}"/>' if bg else "")
    return f"""{bgel}
  <defs><mask id="m-{uid}" maskUnits="userSpaceOnUse" x="-10" y="-10" width="140" height="130">
    <path d="{TRI}" fill="#fff" stroke="#fff" stroke-width="{TRI_STROKE + 4}" stroke-linejoin="round"/>
    <g transform="translate(60,72) scale(1.75) translate(-15,-15)" fill="#000">
      <path d="{POT}"/><path d="{WHEEL_HEAD}"/><path d="{WHEEL_BODY}"/>
    </g></mask></defs>
  <g transform="translate({tx:.2f},{ty:.2f}) scale({s})"><rect x="-10" y="-10" width="140" height="130" fill="{tri}" mask="url(#m-{uid})"/></g>""", S, S


if __name__ == "__main__":
    b, w, h = app_icon(CHAR, KILN, "app")
    write("sheffield-pottery-app-icon.svg", w, h, b)
    b, w, h = app_icon(None, KILN, "fav")
    write("sheffield-pottery-favicon.svg", w, h, b)
    b, w, h = horizontal(KILN, CHAR, SLATE, KILN, "h")
    write("sheffield-pottery-logo-horizontal.svg", w, h, b)
    b, w, h = horizontal(KILN, CREAM, "#CFC6BD", KILN, "hr")
    write("sheffield-pottery-logo-horizontal-reverse.svg", w, h, b)
    b, w, h = horizontal(CHAR, CHAR, CHAR, CHAR, "hk")
    write("sheffield-pottery-logo-horizontal-black.svg", w, h, b)
    b, w, h = horizontal("#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "hw")
    write("sheffield-pottery-logo-horizontal-white.svg", w, h, b)
    b, w, h = stacked(KILN, CHAR, SLATE, KILN, "s")
    write("sheffield-pottery-logo-stacked.svg", w, h, b)
    b, w, h = stacked(KILN, CREAM, "#CFC6BD", KILN, "sr")
    write("sheffield-pottery-logo-stacked-reverse.svg", w, h, b)
    write("sheffield-pottery-emblem.svg", 120, 108, emblem_group(KILN, uid="em"))
    write("sheffield-pottery-emblem-white.svg", 120, 108, emblem_group("#FFFFFF", uid="emw"))
    b, w, h = seal(KILN, CREAM, CREAM, "seal")
    write("sheffield-pottery-seal.svg", w, h, b, "Sheffield Pottery — Since 1946")
    print("ok")
