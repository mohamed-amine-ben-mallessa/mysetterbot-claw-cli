#!/usr/bin/env python3
"""
fixups.py — re-apply the instagrapi DM-media guard after any (re)install of instagrapi.

The DM-thread read in instagrapi crashes (`list index out of range`) when a thread
contains media with an empty version list (voice notes, video-call events, some
shared media). This is an upstream bug (present in 2.9.9 and 2.9.11). We guard the
two `sorted(...)[-1]` calls in `extract_direct_media`.

Idempotent: running it twice is safe. Re-run after `pip install/upgrade instagrapi`.

    python fixups.py            # apply
    python fixups.py --check    # report only, exit 1 if patch missing
"""
from __future__ import annotations
import sys

MARKER = "# msbc-patch: guard empty media version lists"

BEFORE = '''def extract_direct_media(data):
    media = deepcopy(data)
    if "video_versions" in media:
        # Select Best Quality by Resolutiuon
        media["video_url"] = sorted(media["video_versions"], key=lambda o: o["height"] * o["width"])[-1]["url"]
    if "image_versions2" in media:
        media["thumbnail_url"] = sorted(
            media["image_versions2"]["candidates"],
            key=lambda o: o["height"] * o["width"],
        )[-1]["url"]'''

AFTER = '''def extract_direct_media(data):
    media = deepcopy(data)
    ''' + MARKER + '''
    if "video_versions" in media:
        _versions = media.get("video_versions") or []
        if _versions:
            media["video_url"] = sorted(_versions, key=lambda o: o["height"] * o["width"])[-1]["url"]
    if "image_versions2" in media:
        _candidates = (media.get("image_versions2") or {}).get("candidates") or []
        if _candidates:
            media["thumbnail_url"] = sorted(
                _candidates,
                key=lambda o: o["height"] * o["width"],
            )[-1]["url"]'''


def _extractors_path() -> str:
    import instagrapi.extractors as e
    return e.__file__


def main() -> int:
    check_only = "--check" in sys.argv
    path = _extractors_path()
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    if MARKER in src:
        print(f"[ok] patch already present: {path}")
        return 0

    if BEFORE not in src:
        print(f"[warn] expected code block not found in {path} — instagrapi changed. "
              f"Apply patches/instagrapi-empty-media-versions.patch by hand.")
        return 1

    if check_only:
        print(f"[missing] patch not applied: {path} (run without --check to fix)")
        return 1

    src = src.replace(BEFORE, AFTER, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"[patched] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
