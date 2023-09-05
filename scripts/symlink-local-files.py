#!/usr/bin/env python3
import os

BLOG_ROOT = os.path.expanduser(
    os.path.join("~", "gdrive", "docs", "blog")
)

DIRS_TO_LINK = [
    "_posts",
    "pages",
    os.path.join("assets", "images")
]

for d in DIRS_TO_LINK:
    src = os.path.join(BLOG_ROOT, d)
    target = os.path.join(os.curdir, d)
    if os.path.islink(target):
        continue
    if os.path.exists(target):
        os.path.rmdir(target)
    print(f"symlinking {src} to {dir}")
    os.symlink(src, target)

