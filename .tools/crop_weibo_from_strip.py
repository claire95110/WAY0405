"""Crop Weibo glyph (white on black) from the 3-column reference strip; square canvas for circular CSS."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image


def main() -> int:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    im = Image.open(src).convert("RGB")
    a = np.array(im)
    h, w = a.shape[:2]
    cw = w // 3
    # Icon only: strip row has label under each square; exclude bottom text band.
    h_icon = min(h, max(int(h * 0.62), 1))
    col = a[0:h_icon, 0:cw, :]
    r, g, b = col[:, :, 0], col[:, :, 1], col[:, :, 2]
    lum = (r.astype(np.float32) + g + b) / 3.0
    blk = (lum < 48) & (r < 52) & (g < 52) & (b < 52)
    ys, xs = np.where(blk)
    if len(xs) == 0:
        print("no black region", file=sys.stderr)
        return 1
    pad = 6
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, cw - 1)
    ch = col.shape[0]
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, ch - 1)
    patch = col[y0 : y1 + 1, x0 : x1 + 1].copy()
    ph, pw = patch.shape[:2]
    side = max(pw, ph) + 4
    out = np.zeros((side, side, 3), dtype=np.uint8)
    ox = (side - pw) // 2
    oy = (side - ph) // 2
    out[oy : oy + ph, ox : ox + pw] = patch
    Image.fromarray(out, "RGB").save(dst, optimize=True)
    print(dst, side, side)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
