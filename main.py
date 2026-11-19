#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Copies the pre-built front-page image (entry.png, sitting next to this
file) into the output directory as entry.png. Deterministic: a plain
byte-for-byte copy, identical on every run. Python 3.13, standard
library only, no network access.
"""

import hashlib
import os
import shutil

MAX_BYTES = 1_048_576  # 1 MiB

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    # Create the output directory only if it does not exist.
    # Never delete or remove the output directory itself.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    src_size = os.path.getsize(SRC)
    if src_size > MAX_BYTES:
        raise SystemExit(f"Refusing to copy: entry.png is {src_size} bytes (> 1 MiB)")
    dest = os.path.join(OUTPUT_DIR, "entry.png")
    shutil.copyfile(SRC, dest)
    size = os.path.getsize(dest)
    print(f"Copied entry.png ({size} bytes, sha256 {sha256_of(dest)}) to {dest}")


if __name__ == "__main__":
    main()
