#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png (make.fun news-image-20261125 v4).

Stdlib only, deterministic, no external dependencies. Reads entry.png
from the same directory as this script (not the current working
directory), so `python3 main.py` works from anywhere.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"

# The output is always /output/entry.png. MAKEFUN_BOT_DIR is the bot
# directory (/bot) where the repo lives, NOT the output directory —
# writing there fails when /bot is read-only in the grader.
OUTPUT_DIR = Path("/output")
DST = OUTPUT_DIR / "entry.png"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not SRC.exists():
        raise FileNotFoundError(
            f"entry.png not found at {SRC} — entry.png must be present "
            "in the same directory as main.py"
        )
    shutil.copyfile(SRC, DST)
    size = DST.stat().st_size
    print(f"OK entry.png copied ({size} bytes)")


if __name__ == "__main__":
    main()
