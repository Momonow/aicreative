#!/usr/bin/env python3
"""Burn the exact Pulaski/Jones campaign disclaimer without captions."""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.caption_hormozi3 import find_boring_window
from scripts.caption_styled import find_font, probe_size, render_disclaimer

DEFAULT_TEXT_PATH = REPO / "config/campaigns/pulaski-jones/disclaimer.txt"


def burn_disclaimer(src, out, secs=6.0, start=None, text=None):
    text = text or DEFAULT_TEXT_PATH.read_text().strip()
    width, height = probe_size(src)
    if start is None:
        start, _ = find_boring_window(src, length=secs)
    end = start + secs
    with tempfile.TemporaryDirectory() as tmp:
        disclaimer_png = Path(tmp) / "disclaimer.png"
        render_disclaimer(
            text,
            width,
            height,
            find_font(),
            disclaimer_png,
            fontsize_ratio=0.013,
            vertical_pos=0.99,
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(src), "-i", str(disclaimer_png),
            "-filter_complex",
            f"[0:v][1:v]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})':format=auto[out]",
            "-map", "[out]", "-map", "0:a", "-c:a", "copy",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19",
            "-pix_fmt", "yuv420p", str(out),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed:\n{result.stderr[-2000:]}")
    print(f"{Path(out).name}: Pulaski/Jones disclaimer {start:.1f}-{end:.1f}s", flush=True)
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Burn only the exact Pulaski/Jones legal disclaimer."
    )
    parser.add_argument("video")
    parser.add_argument("out")
    parser.add_argument("--secs", type=float, default=6.0)
    parser.add_argument("--start", type=float, default=None)
    parser.add_argument("--text", default=None, help="explicit approved override")
    args = parser.parse_args()
    burn_disclaimer(args.video, args.out, secs=args.secs, start=args.start, text=args.text)


if __name__ == "__main__":
    main()
