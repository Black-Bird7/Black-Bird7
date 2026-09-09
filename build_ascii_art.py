"""
build_ascii_art.py

Converts a portrait photo into blocky, neofetch-style ASCII art:
  1. GrabCut removes the background (so trees/walls/etc. don't turn into noise)
  2. The largest remaining blob (you) is kept, everything else is dropped
  3. Contrast is stretched + CLAHE-enhanced so hair/face/shirt read clearly
  4. The result is downsampled into a character grid using a density ramp

Usage:
    python build_ascii_art.py your_photo.jpg --cols 60 > ascii_lines.txt

Tune --cols for width (60 is a good match for a ~1000px-wide SVG panel).
If the cutout looks wrong (grabbed the wrong region, or clipped your
shoulders), adjust RECT_MARGIN below or pass a tighter/looser photo crop.
"""

import argparse
import numpy as np
import cv2
from PIL import Image

RAMP = " .'`^:;lI!><~+-_?][}{)(|\\/tfjnuvczYXUJCLQ0OZmwqdbkha*8%$@#&"
RECT_MARGIN = 0.02  # fraction of width/height to inset the GrabCut init rectangle


def remove_background(bgr_img):
    h, w = bgr_img.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (
        int(w * RECT_MARGIN), int(h * RECT_MARGIN),
        int(w * (1 - 2 * RECT_MARGIN)), int(h * (1 - 2 * RECT_MARGIN)),
    )
    cv2.grabCut(bgr_img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    fg_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype("uint8")

    kernel = np.ones((7, 7), np.uint8)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    n, labels, stats, _ = cv2.connectedComponentsWithStats(fg_mask, connectivity=8)
    if n > 1:
        largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        fg_mask = np.where(labels == largest, 255, 0).astype("uint8")
    return fg_mask


def enhance_foreground(bgr_img, fg_mask):
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    mask_bool = fg_mask > 0

    vals = gray[mask_bool]
    lo, hi = np.percentile(vals, 1), np.percentile(vals, 99)
    stretched = (gray.astype(np.float32) - lo) / max(1.0, (hi - lo)) * 255
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)
    stretched[~mask_bool] = 255

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(stretched)
    enhanced[~mask_bool] = 255
    return enhanced


def to_ascii(gray_array, cols=60, char_aspect=0.50, levels=13, bg_thresh=248):
    img = Image.fromarray(gray_array)
    w, h = img.size
    rows = max(1, int(cols * (h / w) * char_aspect))
    img = img.resize((cols, rows), Image.LANCZOS)
    pixels = list(img.getdata())

    n_bands = min(levels, len(RAMP))
    lines = []
    for r in range(rows):
        row = pixels[r * cols:(r + 1) * cols]
        chars = []
        for p in row:
            if p >= bg_thresh:
                chars.append(" ")
                continue
            band = int((1 - p / 255) * (n_bands - 1))
            idx = int(band * (len(RAMP) - 1) / (n_bands - 1)) if n_bands > 1 else 0
            chars.append(RAMP[idx])
        lines.append("".join(chars).rstrip())

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("--cols", type=int, default=60)
    args = ap.parse_args()

    bgr = cv2.imread(args.photo)
    fg_mask = remove_background(bgr)
    enhanced = enhance_foreground(bgr, fg_mask)
    for line in to_ascii(enhanced, cols=args.cols):
        print(line)


if __name__ == "__main__":
    main()
