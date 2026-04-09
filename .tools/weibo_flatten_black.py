"""Unify dark areas to #000; remove gray seam column (e.g. x=74). Keep bright logo."""
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
            kill = False
            if x == 74:
                kill = True
            elif r == 17 and g == 17 and b == 17:
                kill = True
            elif r == 30 and g == 30 and b == 30:
                kill = True
            if kill:
                a[y, x, 0] = 0
                a[y, x, 1] = 0
                a[y, x, 2] = 0
                a[y, x, 3] = 255
                n += 1
    Image.fromarray(a, "RGBA").save(path, optimize=True)
    print(path, "flattened", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
