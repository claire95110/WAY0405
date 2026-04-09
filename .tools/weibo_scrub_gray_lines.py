"""Remove residual gray frame lines (anti-alias) on fixed rows/cols in weibo-mark.png."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image


def main() -> int:
    path = Path(sys.argv[1])
    a = np.array(Image.open(path).convert("RGBA"), dtype=np.uint8)
    h, w = a.shape[:2]
    n = 0
    for y in range(h):
        for x in range(w):
            if a[y, x, 3] < 128:
                continue
            r, g, b = int(a[y, x, 0]), int(a[y, x, 1]), int(a[y, x, 2])
            lum = (r + g + b) / 3.0
            kill = False
            if x == 75 and lum > 100:
                kill = True
            elif y == 75 and lum > 100:
                kill = True
            elif x == 7 and lum > 150:
                kill = True
            elif y == 7 and lum > 150:
                kill = True
            if kill:
                a[y, x, 0] = 0
                a[y, x, 1] = 0
                a[y, x, 2] = 0
                n += 1
    Image.fromarray(a, "RGBA").save(path, optimize=True)
    print(path, "zeroed", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
