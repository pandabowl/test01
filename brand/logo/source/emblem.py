"""Emblem geometry for the Sheffield Pottery logo refresh.

The evolved emblem keeps the original idea (a triangle holding three icons:
mining / raw & moist clay / supplies) but redraws it as a single solid
shape with the icons cut out, so it stays crisp at small sizes and in one color.
"""

# Triangle (rounded via a fat round-join stroke), viewBox 0 0 120 108
TRI = "M60,6 L116,103 L4,103 Z"
TRI_STROKE = 8

# --- Icon 1: excavator bucket on its stick (Mining) — local box ~39 x 32 -------
# Side view, opening toward the right, tooth biting forward; one heavy stick
# rises toward the apex so it reads as machinery, not a face.
BUCKET = "M7.5,13 H27 L31.6,25.2 L38.6,26.8 L32.4,30.6 L31.2,31.6 H19 C11.5,31.6 6,27.4 5.6,21.4 Z"
BUCKET_ARM = "M17,14 L8,0"

# --- Icon 2: block of moist clay mid-cut by a wire tool — local box ~30 x 30 --
CLAY_BLOCK = "M3,13 H27 a3,3 0 0 1 3,3 V27 a3,3 0 0 1 -3,3 H3 a3,3 0 0 1 -3,-3 V16 a3,3 0 0 1 3,-3 Z"
CLAY_CUT = "M18.5,13 L14.5,30"        # seam the wire has cut (drawn back in brand color)
WIRE = "M5.5,4.2 L18.5,12 L27.5,3.2"  # wire running from toggle to toggle through the cut
TOGGLES = (
    "M2.6,1.2 h5.8 a1.6,1.6 0 0 1 0,3.2 h-5.8 a1.6,1.6 0 0 1 0,-3.2 Z"
    " M24.6,0.2 h5.8 a1.6,1.6 0 0 1 0,3.2 h-5.8 a1.6,1.6 0 0 1 0,-3.2 Z"
)

# --- Icon 3: pot on a potter's wheel (Supplies) — local box ~30 x 30 ----------
POT = (
    "M9.2,0 H20.8 C20.8,1.5 18.4,2.1 18.4,3.5 C18.4,4.7 26.2,6.1 26.2,10.5"
    " C26.2,13.6 23.8,15.6 20.8,15.6 H9.2 C6.2,15.6 3.8,13.6 3.8,10.5"
    " C3.8,6.1 11.6,4.7 11.6,3.5 C11.6,2.1 9.2,1.5 9.2,0 Z"
)
WHEEL_HEAD = "M1.4,17.2 H28.6 a1.4,1.4 0 0 1 0,2.8 H1.4 a1.4,1.4 0 0 1 0,-2.8 Z"
WHEEL_BODY = "M12.4,20 H17.6 V22.6 H25.4 L27.6,29.6 H2.4 L4.6,22.6 H12.4 Z"

# Icon placement inside the 120 x 108 triangle
P_BUCKET = (40, 28)
P_CLAY = (16, 66)
P_WHEEL = (73, 66)


def emblem_group(color="#DF422C", uid="e", x=0, y=0, scale=1.0):
    """Return SVG <defs>+<g> for the emblem, icons truly knocked out via a mask."""
    m = f"m-{uid}"
    return f"""
  <defs>
    <mask id="{m}" maskUnits="userSpaceOnUse" x="-10" y="-10" width="140" height="130">
      <path d="{TRI}" fill="#fff" stroke="#fff" stroke-width="{TRI_STROKE}" stroke-linejoin="round"/>
      <g transform="translate({P_BUCKET[0]},{P_BUCKET[1]})" fill="#000">
        <path d="{BUCKET}"/>
        <path d="{BUCKET_ARM}" stroke="#000" stroke-width="6.5" stroke-linecap="round" fill="none"/>
      </g>
      <g transform="translate({P_CLAY[0]},{P_CLAY[1]})" fill="#000">
        <path d="{CLAY_BLOCK}"/>
        <path d="{CLAY_CUT}" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
        <path d="{WIRE}" fill="none" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>
        <path d="{TOGGLES}"/>
      </g>
      <g transform="translate({P_WHEEL[0]},{P_WHEEL[1]})" fill="#000">
        <path d="{POT}"/><path d="{WHEEL_HEAD}"/><path d="{WHEEL_BODY}"/>
      </g>
    </mask>
  </defs>
  <g transform="translate({x},{y}) scale({scale})">
    <rect x="-10" y="-10" width="140" height="130" fill="{color}" mask="url(#{m})"/>
  </g>"""


def emblem_svg(color="#DF422C"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 108">{emblem_group(color)}\n</svg>\n'


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(emblem_svg())
