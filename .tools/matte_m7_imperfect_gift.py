"""White-background removal with soft alpha for m7 imperfect-finish gift PNG."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("numpy required: pip install numpy", file=sys.stderr)
    sys.exit(1)

from PIL import Image


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path_in = root / "照片素材" / "m7-imperfect-mystery-box-src.png"
    path_out = root / "照片素材" / "m7-imperfect-mystery-box.png"

    img = Image.open(path_in).convert("RGBA")
    arr = np.asarray(img, dtype=np.float32)
    r, g, b, a_orig = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    sat = np.divide(max_c - min_c, max_c, out=np.zeros_like(max_c), where=max_c > 1e-3)
    dist = np.sqrt((255.0 - r) ** 2 + (255.0 - g) ** 2 + (255.0 - b) ** 2)

    bg_score = np.clip(1.0 - dist / 100.0, 0.0, 1.0) * np.clip(1.0 - sat / 0.22, 0.0, 1.0)
    inner, outer = 0.62, 0.22
    t = (bg_score - outer) / (inner - outer + 1e-6)
    t = np.clip(t, 0.0, 1.0)
    smooth = t * t * (3.0 - 2.0 * t)
    new_a = (1.0 - smooth) * (a_orig / 255.0) * 255.0
    new_a = np.clip(new_a, 0, 255).astype(np.uint8)

    out = np.dstack([arr[:, :, :3].astype(np.uint8), new_a])
    Image.fromarray(out, "RGBA").save(path_out, optimize=True)
    print(path_out, img.size)


if __name__ == "__main__":
    main()
