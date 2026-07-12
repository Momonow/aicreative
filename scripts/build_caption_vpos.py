#!/usr/bin/env python3
"""Build a layout-aware caption vpos-map for a STACKED interview video: full-frame stretches
(b-roll tails after the 2s intro, and the full-frame CTA) get bottom position; the two-pane
stretches keep the default seam position. Emits JSON [[start,end,vpos],...] of the FULL ranges.

Usage: build_caption_vpos.py <insider|figured> <out.json> [--full-vpos 0.82]
"""
import sys, json, subprocess, argparse, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",str(p)],capture_output=True,text=True).stdout.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("which"); ap.add_argument("out"); ap.add_argument("--full-vpos", type=float, default=0.82)
    a = ap.parse_args()
    mod = importlib.import_module(f"{a.which}_assemble")
    BEATS, BB, INTRO, S = mod.BEATS, mod.BEAT_BROLL, mod.BROLL_INTRO, mod.S
    ranges, t = [], 0.0
    for idx, (talk, persona, listener, line) in enumerate(BEATS):
        seg = S / (f"beat_{idx}_stack.mp4" if idx in BB else f"seg_{idx:02d}.mp4")
        d = dur(seg)
        if idx in BB:                      # b-roll beat: 2s two-pane intro, then full-frame tail
            ranges.append([round(t + INTRO, 2), round(t + d, 2), a.full_vpos])
        elif listener is None:             # CTA: full-frame
            ranges.append([round(t, 2), round(t + d, 2), a.full_vpos])
        t += d
    json.dump(ranges, open(a.out, "w"))
    print(f"{a.which}: {len(ranges)} full-frame ranges -> {a.out}")
    for r in ranges: print("  ", r)

if __name__ == "__main__":
    main()
