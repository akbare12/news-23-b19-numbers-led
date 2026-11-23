#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with a read-only /bot and
MAKEFUN_OUTPUT_DIR=/output, so it writes only to that directory,
never next to this file. Stdlib only: no third-party imports.
"""
import hashlib
import os
import shutil
import struct
import sys


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        src_sha = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_sha = hashlib.sha256(f.read()).hexdigest()
    if src_sha != dst_sha:
        print("sha256 mismatch", file=sys.stderr)
        return 1
    w, h = png_size(dst)
    if (w, h) != (1024, 1024):
        print(f"bad size {w}x{h}", file=sys.stderr)
        return 1
    if os.path.getsize(dst) > 1048576:
        print("entry.png over 1 MiB", file=sys.stderr)
        return 1
    print("OK", dst, os.path.getsize(dst), "bytes", f"{w}x{h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
