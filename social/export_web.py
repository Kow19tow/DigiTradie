#!/usr/bin/env python3
"""Converts every post's @2x exports into web-optimised JPGs in /images.
Run after render.sh:  python3 social/export_web.py
Names: images/<post>-1200x630.jpg, <post>-square-1080.jpg, <post>-portrait-1080x1350.jpg"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "images"
OUT.mkdir(exist_ok=True)
SIZES = {"landscape": ("1200x630", (1200, 630)), "square": ("square-1080", (1080, 1080)), "portrait": ("portrait-1080x1350", (1080, 1350))}

for post in sorted(p for p in ROOT.iterdir() if (p / "exports").is_dir()):
    for layout, (suffix, size) in SIZES.items():
        src = post / "exports" / f"{layout}@2x.png"
        if not src.exists():
            continue
        dst = OUT / f"{post.name}-{suffix}.jpg"
        Image.open(src).convert("RGB").resize(size, Image.LANCZOS).save(dst, "JPEG", quality=90, optimize=True, progressive=True)
        print(f"{dst.name}  {dst.stat().st_size // 1024} KB")
