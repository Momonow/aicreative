"""Trim leading/trailing silence from a clip using word-level transcript timing.

Default: keep one continuous window from first-word-start (- lead) to last-word-end (+ tail).
Internal pauses (between sentences, dramatic beats) are preserved.

Optional --max-gap: also cut internal silences longer than the threshold (jump-cut mode).

Usage:
    .venv/bin/python scripts/trim_silence.py <clip.mp4> <transcript.json>
    .venv/bin/python scripts/trim_silence.py <clip.mp4> <transcript.json> --lead 0.2 --tail 0.3
    .venv/bin/python scripts/trim_silence.py <clip.mp4> <transcript.json> --max-gap 0.4
"""
import argparse, json, subprocess, sys
from pathlib import Path


def collect_words(transcript):
    words = []
    for seg in transcript.get("segments", []):
        words.extend(seg.get("words", []))
    return words


def keep_windows(words, lead, tail, max_gap=None):
    if not words:
        return []
    if max_gap is None:
        # one continuous window: speech start (- lead) to speech end (+ tail)
        s = max(0.0, words[0]["start"] - lead)
        e = words[-1]["end"] + tail
        return [(round(s, 3), round(e, 3))]
    # jump-cut mode: split at any silence > max_gap
    windows = [[max(0.0, words[0]["start"] - lead), words[0]["end"]]]
    for i, w in enumerate(words[1:], start=1):
        gap = w["start"] - words[i - 1]["end"]
        if gap > max_gap:
            windows[-1][1] = words[i - 1]["end"] + tail
            windows.append([max(0.0, w["start"] - lead), w["end"]])
        else:
            windows[-1][1] = w["end"]
    windows[-1][1] = windows[-1][1] + tail
    return [(round(s, 3), round(e, 3)) for s, e in windows]


def build_filter(windows):
    parts = []
    for i, (s, e) in enumerate(windows):
        parts.append(f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS[a{i}]")
    n = len(windows)
    streams = "".join(f"[v{i}][a{i}]" for i in range(n))
    parts.append(f"{streams}concat=n={n}:v=1:a=1[vout][aout]")
    return ";".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("transcript")
    ap.add_argument("--lead", type=float, default=0.15, help="padding before first word")
    ap.add_argument("--tail", type=float, default=0.25, help="padding after last word")
    ap.add_argument("--max-gap", type=float, default=None, help="if set, also cut internal silences longer than this")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    clip = Path(args.clip)
    out = Path(args.out) if args.out else clip.with_name(clip.stem + "_trimmed" + clip.suffix)

    with open(args.transcript) as f:
        t = json.load(f)
    words = collect_words(t)
    if not words:
        print("no words found", file=sys.stderr)
        sys.exit(1)

    windows = keep_windows(words, args.lead, args.tail, args.max_gap)
    total = sum(e - s for s, e in windows)
    print(f"keeping {len(windows)} window(s), total {total:.2f}s:")
    for s, e in windows:
        print(f"  {s:5.2f} - {e:5.2f}  ({e-s:.2f}s)")

    fc = build_filter(windows)
    cmd = [
        "ffmpeg", "-y", "-i", str(clip),
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    print(f"\nDONE → {out}")


if __name__ == "__main__":
    main()
