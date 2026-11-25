#!/usr/bin/env python3
"""
Cut a product photo out of its white studio background.

Usage:
    python3 cutout.py <image-url-or-path> <out.png> [--tol 18] [--shadow 0] [--feather 0.8]

The backdrop colour is sampled from the image border. Pixels close to it AND
connected to the border are background (a flood fill from the edges), as are
enclosed pockets that match it closely (the hole in a rib). White parts of the
product itself survive unless they touch the backdrop. Edge pixels get a soft
alpha and have the backdrop colour un-mixed out of them, so there is no white
halo when the cutout sits on a dark banner. Raise --tol for photos with a soft
grey halo, or pass --shadow N to strip a neutral grey studio shadow that is
up to N levels darker than the backdrop. Output is cropped to the product.
"""
import argparse, io, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def load(src):
    if src.startswith("http"):
        sep = "&" if "?" in src else "?"
        data = subprocess.run(["curl", "-sL", src + sep + "width=1400"],
                              capture_output=True, check=True).stdout
        return Image.open(io.BytesIO(data))
    return Image.open(src)


def cutout(im, tol=18, feather=0.8, holes=True, shadow=0):
    im = im.convert("RGBA")
    rgb = np.asarray(im.convert("RGB")).astype(np.float32)
    a0 = np.asarray(im)[..., 3].astype(np.float32) / 255
    # reference background colour = median of the outermost pixels (handles
    # slightly grey or cream "white" studio backdrops)
    edge = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    ref = np.median(edge, axis=0)
    dist = np.abs(rgb - ref).max(axis=2)          # 0 = exactly background
    near_bg = (dist <= tol) | (a0 < 0.03)
    if shadow:
        # soft grey studio shadow: neutral (unsaturated) and only somewhat
        # darker than the backdrop. Bristles/cream glaze are warmer than this.
        chroma = rgb.max(axis=2) - rgb.min(axis=2)
        darker = ref.mean() - rgb.mean(axis=2)
        near_bg |= (chroma <= 9) & (darker > 0) & (darker <= shadow)
    # background = near-background regions that touch the border ...
    lab, n = ndimage.label(near_bg)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0])
    # ... plus enclosed pockets of background (the hole in a rib)
    if holes and n:
        idx = np.arange(1, n + 1)
        area = ndimage.sum(near_bg, lab, idx)
        mean_d = ndimage.mean(dist, lab, idx)
        pocket = (area > near_bg.size * 0.0004) & (mean_d < max(tol, shadow) * 0.6)
        bg |= np.isin(lab, idx[pocket])
    fg = ~bg
    # drop specks (dust, stray dimension-label text away from the product)
    flab, fn = ndimage.label(fg)
    if fn > 1:
        sizes = ndimage.sum(fg, flab, range(1, fn + 1))
        keep = np.zeros(fn + 1, bool)
        keep[1:] = sizes >= sizes.max() * 0.04
        fg = keep[flab]
    # soft alpha in a thin band around the edge, from distance to background
    inner = ndimage.binary_erosion(fg, iterations=2)
    outer = ndimage.binary_dilation(fg, iterations=1)
    soft = np.clip((dist - tol * 0.5) / 40.0, 0, 1)
    if shadow:
        soft = np.where((rgb.max(axis=2) - rgb.min(axis=2)) <= 9, np.clip((dist - shadow) / 40.0, 0, 1), soft)
    alpha = np.where(inner, 1.0, np.where(outer, soft, 0.0))
    alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(feather))).astype(np.float32) / 255
    alpha = np.minimum(alpha, a0)
    # un-mix the backdrop colour out of semi-transparent edge pixels
    a = np.maximum(alpha, 1e-3)[..., None]
    dec = np.clip((rgb - (1 - a) * ref) / a, 0, 255)
    col = np.where(((alpha > 0.02) & (alpha < 0.98))[..., None], dec, rgb)
    out = Image.fromarray(np.dstack([col, alpha * 255]).astype(np.uint8), "RGBA")
    bbox = out.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    return out.crop(bbox) if bbox else out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--tol", type=int, default=18)
    ap.add_argument("--feather", type=float, default=0.8)
    ap.add_argument("--shadow", type=int, default=0,
                    help="also strip a neutral grey studio shadow up to N levels darker than the backdrop")
    a = ap.parse_args()
    res = cutout(load(a.src), a.tol, a.feather, shadow=a.shadow)
    res.save(a.out)
    print(a.out, res.size)
