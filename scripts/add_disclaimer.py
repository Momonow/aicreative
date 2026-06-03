#!/usr/bin/env python3
"""Overlay the verbatim Pulaski/Jones legal disclaimer onto a video at its
calmest ("most boring") 6-second window — no captions, audio untouched.

Usage:
  .venv/bin/python scripts/add_disclaimer.py <in.mp4> [--out out.mp4] [--secs 6]
                                             [--start <sec>]   # force a window
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.caption_styled import render_disclaimer, DEFAULT_DISCLAIMER


def probe(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True)
    w, h, dur = r.stdout.strip().split(",")
    return int(w), int(h), float(dur)


def find_boring_window(path, total_dur, secs):
    """Lowest frame-to-frame motion window, avoiding first/last 4s."""
    r = subprocess.run(
        ["ffmpeg", "-i", path, "-vf", "fps=4,scale=64:64",
         "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"],
        capture_output=True)
    frames = r.stdout
    fw = fh = 64
    n = len(frames) // (fw * fh)
    diffs = []
    for i in range(1, n):
        a = frames[(i-1)*fw*fh : i*fw*fh]
        b = frames[i*fw*fh : (i+1)*fw*fh]
        diffs.append(sum(abs(x-y) for x, y in zip(a, b)))

    fps_m = 4
    win = int(secs * fps_m)
    lo = int(4 * fps_m)
    hi = int((total_dur - 4 - secs) * fps_m)
    if hi <= lo:                      # too short to avoid edges — center it
        return max(0.0, (total_dur - secs) / 2)
    best_start, best_score = lo / fps_m, float("inf")
    for s in range(lo, hi):
        score = sum(diffs[s:s+win])
        if score < best_score:
            best_score, best_start = score, s / fps_m
    return best_start


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=None)
    ap.add_argument("--secs", type=float, default=6.0)
    ap.add_argument("--start", type=float, default=None)
    args = ap.parse_args()

    inp = args.video
    out = args.out or str(Path("outputs") / (Path(inp).stem + "_disclaimer.mp4"))
    Path("outputs").mkdir(exist_ok=True)

    w, h, dur = probe(inp)
    start = args.start if args.start is not None else find_boring_window(inp, dur, args.secs)
    end = start + args.secs
    print(f"  {w}x{h} {dur:.1f}s — disclaimer {start:.1f}s → {end:.1f}s")

    font = "assets/fonts/Montserrat-Black.ttf"
    if not Path(font).exists():
        font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    tmp = tempfile.mkdtemp()
    png = Path(tmp) / "disclaimer.png"
    render_disclaimer(DEFAULT_DISCLAIMER, w, h, font, png)

    subprocess.run([
        "ffmpeg", "-y", "-i", inp, "-i", str(png),
        "-filter_complex",
        f"[0:v][1:v]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})'[v]",
        "-map", "[v]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        "-c:a", "copy", out], check=True, capture_output=True)
    print(f"  saved → {out} ({Path(out).stat().st_size//1024}KB)")


if __name__ == "__main__":
    main()
