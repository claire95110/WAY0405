"""Turn outer light square frame on weibo-mark.png to black; keep inner white logo."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image


def outer_band_mask(
    op: np.ndarray, y0: int, y1: int, x0: int, x1: int, band: int
) -> np.ndarray:
    h, w = op.shape
    m = np.zeros((h, w), dtype=bool)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not op[y, x]:
                continue
            if (
                x - x0 < band
                or x1 - x < band
                or y - y0 < band
                or y1 - y < band
            ):
                m[y, x] = True
    return m


def main() -> int:
    path = Path(sys.argv[1])
    im = Image.open(path).convert("RGBA")
    a = np.array(im, dtype=np.uint8)
    h, w = a.shape[:2]
    op = a[:, :, 3] > 128
    if not op.any():
        print("no opaque pixels", file=sys.stderr)
        return 1
    ys, xs = np.where(op)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    r = a[:, :, 0].astype(np.float32)
    g = a[:, :, 1].astype(np.float32)
    b = a[:, :, 2].astype(np.float32)
    lum = (r + g + b) / 3.0
    # Pass 1: bright white in the outer 5px ring (thick frame).
    in5 = outer_band_mask(op, y0, y1, x0, x1, 5)
    light = (lum > 135) & op & in5
    # Pass 2: anti-aliased inner frame line (gray), slightly deeper than 5px.
    in9 = outer_band_mask(op, y0, y1, x0, x1, 9)
    gray_frame = (lum >= 110) & (lum <= 220) & op & in9
    hit = light | gray_frame
    a[hit, 0] = 0
    a[hit, 1] = 0
    a[hit, 2] = 0
    Image.fromarray(a, "RGBA").save(path, optimize=True)
    print(path, "recolored", int(hit.sum()), "pixels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
