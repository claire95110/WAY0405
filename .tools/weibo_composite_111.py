"""Composite weibo-mark.png onto solid background (default #000) to reduce scale halos."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

# Match #m6 .social-icon__mark background
BG = (0, 0, 0, 255)


def main() -> int:
    path = Path(sys.argv[1])
    im = Image.open(path).convert("RGBA")
    base = Image.new("RGBA", im.size, BG)
    out = Image.alpha_composite(base, im)
    out.save(path, optimize=True)
    print(path, im.size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
