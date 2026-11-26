#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png (make.fun news-image-20261125 v4).

Stdlib only, deterministic, no external dependencies. Reads entry.png
from the same directory as this script (not the current working
directory), so `python3 main.py` works from anywhere.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"

# Honor MAKEFUN_BOT_DIR if set, but the output is always /output/entry.png.
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_BOT_DIR", "/output"))
DST = OUTPUT_DIR / "entry.png"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    size = DST.stat().st_size
    print(f"OK entry.png copied ({size} bytes)")


if __name__ == "__main__":
    main()
