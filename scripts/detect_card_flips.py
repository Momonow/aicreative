"""Detect caption CARD-FLIP timestamps in a (Submagic) captioned video by diffing a binary
text mask of the caption band. A full card change flips many text pixels; an active-word
color change or face motion barely moves the luminance mask. Output: flip start-times.

  python scripts/detect_card_flips.py <video.mp4> [--fps 12] [--thresh 0.04] [--min-gap 0.35]
"""
import sys, subprocess, argparse
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--fps", type=float, default=12)
    ap.add_argument("--thresh", type=float, default=0.045)  # fraction of mask pixels that changed
    ap.add_argument("--min-gap", type=float, default=0.35)
    a = ap.parse_args()
    # decode caption band as raw gray frames at fps
    W, H = 360, 260   # downscaled caption band
    cmd = ["ffmpeg", "-v", "error", "-i", a.video,
           "-vf", f"crop=720:540:0:650,scale={W}:{H},fps={a.fps},format=gray",
           "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H)
    frames = np.frombuffer(raw[:n * W * H], dtype=np.uint8).reshape(n, H, W)
    masks = frames > 180          # bright text pixels (white/yellow/green caption glyphs)
    flips = [0.0]
    prev_t = 0.0
    for i in range(1, n):
        changed = np.mean(masks[i] ^ masks[i - 1])   # fraction of mask pixels that flipped
        t = i / a.fps
        if changed > a.thresh and (t - prev_t) >= a.min_gap:
            flips.append(round(t, 2)); prev_t = t
    print(f"frames={n} fps={a.fps} -> {len(flips)} card flips")
    print(" ".join(f"{x:.2f}" for x in flips))
    # also write to a sidecar for downstream use
    import json, pathlib
    out = pathlib.Path(a.video).with_suffix(".flips.json")
    out.write_text(json.dumps(flips))
    print("wrote", out)


if __name__ == "__main__":
    main()
