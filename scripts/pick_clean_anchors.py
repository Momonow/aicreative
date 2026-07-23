#!/usr/bin/env python3
"""Pick clean, eyes-open anchor frames for multi-clip image-to-video generation.

Repeatedly seeding from one generated frame can compound transient defects and make later clips
look progressively less like the approved person. This tool samples clip 1, keeps frontal frames
with two detected eyes, and exports either a well-spaced or deterministic-random anchor set plus
a manifest.

Usage:
  .venv/bin/python scripts/pick_clean_anchors.py clip01.mp4 \
    --out-dir outputs/anchors --n 6 --strategy random --seed 17
"""

import argparse
import json
import random
import subprocess
from pathlib import Path

import cv2


FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
EYE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)


def probe_duration(video):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def eyes_open_score(image):
    """Return (accepted, face_area) using frontal-face and eye cascades."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.1, 5, minSize=(120, 120))
    if len(faces) == 0:
        return False, 0
    x, y, width, height = max(faces, key=lambda face: face[2] * face[3])
    eye_region = gray[y:y + int(height * 0.6), x:x + width]
    eyes = EYE_CASCADE.detectMultiScale(eye_region, 1.1, 6, minSize=(25, 25))
    return len(eyes) >= 2, int(width * height)


def sample_candidates(video, duration, step):
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise RuntimeError(f"could not open video: {video}")
    candidates = []
    timestamp = 0.3
    try:
        while timestamp < duration - 0.2:
            capture.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            ok, image = capture.read()
            if ok and image is not None:
                accepted, face_area = eyes_open_score(image)
                if accepted:
                    candidates.append({"time": timestamp, "face_area": face_area})
            timestamp += step
    finally:
        capture.release()
    return candidates


def spaced_pick(candidates, count):
    if count <= 0:
        return []
    if count == 1:
        return [candidates[len(candidates) // 2]]
    return [
        candidates[round(index * (len(candidates) - 1) / (count - 1))]
        for index in range(count)
    ]


def random_pick(candidates, count, seed, min_gap):
    """Choose a reproducible random subset while avoiding near-duplicate moments."""
    rng = random.Random(seed)
    pool = candidates[:]
    rng.shuffle(pool)
    chosen = []
    for candidate in pool:
        if all(abs(candidate["time"] - prior["time"]) >= min_gap for prior in chosen):
            chosen.append(candidate)
            if len(chosen) == count:
                break
    if len(chosen) < count:
        for candidate in spaced_pick(candidates, min(count, len(candidates))):
            if candidate not in chosen:
                chosen.append(candidate)
            if len(chosen) == count:
                break
    return sorted(chosen, key=lambda candidate: candidate["time"])


def extract_frame(video, timestamp, output):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("clip")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--prefix", default="_anchor")
    parser.add_argument("--step", type=float, default=0.15, help="sample interval in seconds")
    parser.add_argument(
        "--strategy",
        choices=["spaced", "random"],
        default="spaced",
        help="selection method; random is deterministic with --seed",
    )
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument(
        "--min-gap",
        type=float,
        default=0.45,
        help="minimum seconds between random anchors",
    )
    args = parser.parse_args()

    clip = Path(args.clip).resolve()
    if not clip.exists():
        parser.error(f"clip not found: {clip}")
    if args.n < 1:
        parser.error("--n must be at least 1")
    if args.step <= 0 or args.min_gap < 0:
        parser.error("--step must be positive and --min-gap cannot be negative")

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = probe_duration(clip)
    candidates = sample_candidates(clip, duration, args.step)
    used_fallback = False
    if not candidates:
        used_fallback = True
        fallback_times = [0.5, 1.8, 3.0, 4.2, 5.5, 6.8]
        candidates = [
            {"time": timestamp, "face_area": 0}
            for timestamp in fallback_times
            if timestamp < duration - 0.1
        ]
    if not candidates:
        raise RuntimeError("clip is too short to extract an anchor")

    count = min(args.n, len(candidates))
    if args.strategy == "random":
        picks = random_pick(candidates, count, args.seed, args.min_gap)
    else:
        picks = spaced_pick(candidates, count)

    selected = []
    for index, candidate in enumerate(picks):
        output = out_dir / f"{args.prefix}_{index}.jpg"
        extract_frame(clip, candidate["time"], output)
        selected.append(
            {
                "index": index,
                "time": round(candidate["time"], 3),
                "face_area": candidate["face_area"],
                "file": str(output),
            }
        )

    manifest_name = f"{args.prefix.strip('_') or 'anchor'}_manifest.json"
    manifest_path = out_dir / manifest_name
    manifest = {
        "source": str(clip),
        "duration": round(duration, 3),
        "requested_count": args.n,
        "strategy": args.strategy,
        "seed": args.seed if args.strategy == "random" else None,
        "sample_step": args.step,
        "min_gap": args.min_gap if args.strategy == "random" else None,
        "eyes_open_candidate_count": len(candidates),
        "used_fixed_timestamp_fallback": used_fallback,
        "partial_selection": len(selected) < args.n,
        "selected": selected,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    print(
        f"eyes-open candidates: {len(candidates)} | picked {len(selected)} "
        f"| strategy: {args.strategy}",
        flush=True,
    )
    for item in selected:
        print(
            f"  {args.prefix}_{item['index']}  t={item['time']:.3f}s  {item['file']}",
            flush=True,
        )
    print(f"manifest: {manifest_path}", flush=True)
    if len(selected) < args.n:
        print(
            f"WARN: requested {args.n} anchors but only {len(selected)} clean candidates "
            "were available; review the clip or lower --step",
            flush=True,
        )


if __name__ == "__main__":
    main()
