"""Rebuild assets/bth-d3-wheel.png from the product's main photo.

    pip install "rembg[cpu]==2.0.67"
    curl -o BTH-D32.jpg "https://cdn.shopify.com/s/files/1/0677/5508/2050/files/BTH-D32.jpg?v=1739975323"
    python3 make-cutout.py BTH-D32.jpg assets/bth-d3-wheel.png

Uses rembg's IS-Net model (isnet-general-use, Apache-2.0); it downloads
~180 MB of model weights on first run. The wheel body is white plastic on a
light-grey backdrop, so a colour threshold can't separate them.

The crop box keeps the photo's right and bottom edges: that's where the
pedal cable leaves the frame and the pedal is clipped. slide.html places
those two edges on the artboard edges so neither cut shows.
"""
import sys

from PIL import Image
from rembg import new_session, remove

CROP = (125, 65, 1000, 1000)  # alpha bounding box of the 1000x1000 photo

src, dst = sys.argv[1], sys.argv[2]
cut = remove(Image.open(src).convert("RGB"), session=new_session("isnet-general-use")).crop(CROP)
cut.putalpha(cut.getchannel("A").point(lambda v: 0 if v < 8 else v))  # drop matting speckle
cut.save(dst, optimize=True)
print(f"wrote {dst} {cut.size}")
