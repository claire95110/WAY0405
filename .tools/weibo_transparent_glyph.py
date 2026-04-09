"""Weibo: remove outer black square only; keep white logo + enclosed black (pupil). Output RGBA."""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def main() -> int:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    im = Image.open(src).convert("RGB")
    a = np.array(im, dtype=np.uint8)
    h, w = a.shape[:2]

    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = (r.astype(np.float32) + g + b) / 3.0
    dark = (lum < 58) & (r < 72) & (g < 72) & (b < 72)

    outer = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        if dark[0, x]:
            q.append((x, 0))
            outer[0, x] = True
        if h > 1 and dark[h - 1, x]:
            q.append((x, h - 1))
            outer[h - 1, x] = True
    for y in range(h):
        if dark[y, 0]:
            if not outer[y, 0]:
                q.append((0, y))
                outer[y, 0] = True
        if w > 1 and dark[y, w - 1]:
            if not outer[y, w - 1]:
                q.append((w - 1, y))
                outer[y, w - 1] = True

    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= w or ny >= h or outer[ny, nx]:
                continue
            if dark[ny, nx]:
                outer[ny, nx] = True
                q.append((nx, ny))

    alpha = np.where(outer, 0, 255).astype(np.uint8)
    rgba = np.dstack([a[:, :, 0], a[:, :, 1], a[:, :, 2], alpha])

    ys, xs = np.where(alpha > 0)
    if len(xs) == 0:
        print("empty after mask", file=sys.stderr)
        return 1
    p = 2
    x0, x1 = max(xs.min() - p, 0), min(xs.max() + p, w - 1)
    y0, y1 = max(ys.min() - p, 0), min(ys.max() + p, h - 1)
    rgba = rgba[y0 : y1 + 1, x0 : x1 + 1]

    Image.fromarray(rgba, "RGBA").save(dst, optimize=True)
    print(dst, rgba.shape[1], rgba.shape[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
