"""Voice consistency detector — catches what audio_match.py misses.

Per-clip metrics:
  - Speaker embedding (resemblyzer / GE2E)  → cosine similarity to reference clip
  - Mean F0 (pitch) via librosa pyin       → Hz delta from reference clip
  - Mean F0 std (pitch variability)        → indicator of monotone vs animated

Thresholds (tuned for short UGC ads):
  - Speaker similarity     ≥ 0.85   (anything lower = audible voice character change)
  - Mean F0 delta          ≤ 8 Hz   (humans detect ~5-10 Hz shifts in male voice)
  - F0 std ratio           0.5x..2x (animation level should be in same ballpark)

Usage:
  .venv/bin/python scripts/voice_consistency.py <reference.mp4> <clip2.mp4> <clip3.mp4> ...
  .venv/bin/python scripts/voice_consistency.py <ref.mp4> <c2.mp4> --sim-min 0.80 --f0-tol 10
"""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import librosa


def extract_wav(video_path: Path) -> Path:
    """Extract mono 16kHz wav from a video into a temp file. Returns path."""
    tmp = Path(tempfile.mkstemp(suffix=".wav")[1])
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path),
         "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", str(tmp)],
        check=True, capture_output=True,
    )
    return tmp


def compute_f0(wav_path: Path):
    """Return (mean_f0_hz, std_f0_hz) using librosa pyin. Voiced frames only."""
    y, sr = librosa.load(str(wav_path), sr=16000, mono=True)
    f0, voiced, _ = librosa.pyin(
        y, fmin=70, fmax=400, sr=sr, frame_length=2048,
    )
    voiced_f0 = f0[voiced & ~np.isnan(f0)]
    if len(voiced_f0) == 0:
        return 0.0, 0.0
    return float(np.mean(voiced_f0)), float(np.std(voiced_f0))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="+", help="reference first, then candidates")
    ap.add_argument("--sim-min", type=float, default=0.85, help="min speaker similarity (default 0.85)")
    ap.add_argument("--f0-tol", type=float, default=8.0, help="max |delta Hz| in mean F0 (default 8)")
    args = ap.parse_args()

    if len(args.videos) < 2:
        sys.exit("need at least 2 videos: reference + 1 or more candidates")

    enc = VoiceEncoder(verbose=False)

    # process reference
    ref_path = Path(args.videos[0]).resolve()
    ref_wav = extract_wav(ref_path)
    ref_emb = enc.embed_utterance(preprocess_wav(ref_wav))
    ref_f0_mean, ref_f0_std = compute_f0(ref_wav)

    print(f"REFERENCE: {ref_path.name}")
    print(f"  speaker-embed (256-d, unit-norm)   mean F0 {ref_f0_mean:6.1f}Hz   F0 std {ref_f0_std:5.1f}Hz")
    print()
    print(f"TOLERANCES: similarity ≥ {args.sim_min:.2f}   |Δ mean F0| ≤ {args.f0_tol:.0f}Hz")
    print()

    fails = []
    for vpath in args.videos[1:]:
        path = Path(vpath).resolve()
        wav = extract_wav(path)
        emb = enc.embed_utterance(preprocess_wav(wav))
        sim = float(np.dot(ref_emb, emb))   # both unit-norm already
        f0_mean, f0_std = compute_f0(wav)
        d_f0 = f0_mean - ref_f0_mean
        d_f0_std_ratio = f0_std / ref_f0_std if ref_f0_std > 0 else float("nan")

        flags = []
        if sim < args.sim_min:
            flags.append(f"sim {sim:.3f}")
        if abs(d_f0) > args.f0_tol:
            flags.append(f"ΔF0 {d_f0:+.1f}Hz")
        status = "✗ FAIL" if flags else "✓ OK  "
        flag_txt = "   [" + " | ".join(flags) + "]" if flags else ""
        print(f"  {status} {path.name:34s}  sim {sim:.3f}   mean F0 {f0_mean:6.1f}Hz  ({d_f0:+.1f})   F0 std {f0_std:5.1f}Hz  ({d_f0_std_ratio:.2f}x){flag_txt}")
        if flags:
            fails.append(path.name)
        try:
            wav.unlink()
        except OSError:
            pass
    try:
        ref_wav.unlink()
    except OSError:
        pass

    if fails:
        print(f"\n{len(fails)} clip(s) flagged: {fails}")
        sys.exit(1)
    print("\nall clips within tolerance")


if __name__ == "__main__":
    main()
