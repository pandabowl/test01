"""Turn the green gift bows in the Shimpo promo image red (card panels stay green)."""
import colorsys, sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
px = im.load()
# Bow areas on the two gift certificates, left of the green "$40"/"$30" panels.
boxes = [(405, 50, 527, 185), (405, 262, 527, 395)]
for x0, y0, x1, y1 in boxes:
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.20 < h < 0.48 and s > 0.25 and v > 0.08:
                nr, ng, nb = colorsys.hsv_to_rgb(0.995, min(1.0, s * 1.05), min(1.0, v * 1.08))
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255))
im.save(dst, quality=92)
