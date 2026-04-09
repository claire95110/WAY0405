"""Extract Weibo mark: white glyph on transparent background (no outer frame)."""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def flood_mask_dark(a: np.ndarray, sx: int, sy: int) -> np.ndarray:
    h, w = a.shape[:2]
    seen = np.zeros((h, w), dtype=bool)
    q = deque([(sx, sy)])
    seen[sy, sx] = True

    def dark(px: np.ndarray) -> bool:
        return bool(px[0] < 55 and px[1] < 50 and px[2] < 45)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= w or ny >= h or seen[ny, nx]:
                continue
            if dark(a[ny, nx]):
                seen[ny, nx] = True
                q.append((nx, ny))
    return seen


def flood_non_dark(sub: np.ndarray, dark: np.ndarray, sx: int, sy: int) -> np.ndarray:
    """4-connect fill through non-dark cells (stays inside enclosed hole)."""
    h, w = sub.shape[:2]
    seen = np.zeros((h, w), dtype=bool)
    if dark[sy, sx]:
        return seen
    q = deque([(sx, sy)])
    seen[sy, sx] = True
    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= w or ny >= h or seen[ny, nx] or dark[ny, nx]:
                continue
            seen[ny, nx] = True
            q.append((nx, ny))
    return seen


def trim_solid_white_frame(rgba: np.ndarray) -> np.ndarray:
    """Remove rows/cols that are fully opaque near-white (export artifacts)."""
    h, w = rgba.shape[:2]
    y0, y1, x0, x1 = 0, h - 1, 0, w - 1

    def row_is_frame(y: int) -> bool:
        row = rgba[y, :, :]
        op = row[:, 3] > 200
        if not op.all():
            return False
        return bool(np.all(row[:, :3] > 248))

    def col_is_frame(x: int) -> bool:
        col = rgba[:, x, :]
        op = col[:, 3] > 200
        if not op.all():
            return False
        return bool(np.all(col[:, :3] > 248))

    while y0 <= y1 and row_is_frame(y0):
        y0 += 1
    while y1 >= y0 and row_is_frame(y1):
        y1 -= 1
    while x0 <= x1 and col_is_frame(x0):
        x0 += 1
    while x1 >= x0 and col_is_frame(x1):
        x1 -= 1
    if y0 > y1 or x0 > x1:
        return rgba
    return rgba[y0 : y1 + 1, x0 : x1 + 1]


def main() -> int:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    im = Image.open(src).convert("RGB")
    a = np.array(im, dtype=np.uint8)
    h, w = a.shape[:2]

    sx, sy = w // 2, int(h * 0.42)
    while sy < h - 1 and not (
        a[sy, sx, 0] < 50 and a[sy, sx, 1] < 45 and a[sy, sx, 2] < 40
    ):
        sy += 1

    inner_dark = flood_mask_dark(a, sx, sy)
    ys, xs = np.where(inner_dark)
    if len(xs) == 0:
        print("flood failed", file=sys.stderr)
        return 1

    pad = 8
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, w - 1)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, h - 1)
    sub = a[y0 : y1 + 1, x0 : x1 + 1]

    r = sub[:, :, 0].astype(np.float32)
    g = sub[:, :, 1].astype(np.float32)
    b = sub[:, :, 2].astype(np.float32)
    lum = (r + g + b) / 3.0
    dark = (r < 60) & (g < 55) & (b < 50)
    tan = (r > 175) & (g > 145) & (b > 110) & (r - b > 35)

    sh, sw = sub.shape[:2]
    scx, scy = sw // 2, sh // 2
    if dark[scy, scx]:
        nd = np.where(~dark)
        if len(nd[0]) == 0:
            print("no hole", file=sys.stderr)
            return 1
        d2 = (nd[0] - scy) ** 2 + (nd[1] - scx) ** 2
        k = int(np.argmin(d2))
        scy, scx = int(nd[0][k]), int(nd[1][k])

    inside = flood_non_dark(sub, dark, scx, scy)
    logo = inside & (lum > 88) & ~tan

    out_a = np.zeros(sub.shape[:2], dtype=np.uint8)
    out_a[logo] = 255
    rgba = np.dstack(
        [
            np.full(sub.shape[:2], 255, dtype=np.uint8),
            np.full(sub.shape[:2], 255, dtype=np.uint8),
            np.full(sub.shape[:2], 255, dtype=np.uint8),
            out_a,
        ]
    )

    ys2, xs2 = np.where(out_a > 0)
    if len(xs2) == 0:
        print("empty logo", file=sys.stderr)
        return 1
    p = 2
    x0b = max(xs2.min() - p, 0)
    x1b = min(xs2.max() + p, rgba.shape[1] - 1)
    y0b = max(ys2.min() - p, 0)
    y1b = min(ys2.max() + p, rgba.shape[0] - 1)
    rgba = rgba[y0b : y1b + 1, x0b : x1b + 1]
    rgba = trim_solid_white_frame(rgba)

    Image.fromarray(rgba, "RGBA").save(dst, optimize=True)
    print(dst, rgba.shape[1], rgba.shape[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
