"""Audit every extracted frame for flashes, blanks, freezes, and short visual runs."""

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def small_gray(frame):
    return cv2.resize(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
        (90, 160),
        interpolation=cv2.INTER_AREA,
    )


def mean_diff(first, second):
    return float(np.mean(cv2.absdiff(first, second)))


def audit(frames_dir, scenes_file, fps, output_dir):
    paths = sorted(frames_dir.glob("frame_*.jpg"))
    if not paths:
        raise RuntimeError(f"No extracted frames in {frames_dir}")

    frames = []
    gray = []
    black_frames = []
    for index, path in enumerate(paths):
        frame = cv2.imread(str(path))
        if frame is None:
            raise RuntimeError(f"Unreadable frame: {path}")
        frames.append(frame)
        reduced = small_gray(frame)
        gray.append(reduced)
        if float(np.mean(reduced)) < 5.0 and float(np.std(reduced)) < 5.0:
            black_frames.append(index)

    consecutive_diffs = [
        mean_diff(gray[index - 1], gray[index])
        for index in range(1, len(gray))
    ]
    frozen_runs = []
    run_start = None
    for index, difference in enumerate(consecutive_diffs, 1):
        if difference < 0.08:
            if run_start is None:
                run_start = index - 1
        elif run_start is not None:
            if index - run_start >= 5:
                frozen_runs.append((run_start, index - 1))
            run_start = None
    if run_start is not None and len(gray) - run_start >= 5:
        frozen_runs.append((run_start, len(gray) - 1))

    isolated_flashes = []
    for index in range(1, len(gray) - 1):
        previous = mean_diff(gray[index - 1], gray[index])
        following = mean_diff(gray[index], gray[index + 1])
        skipped = mean_diff(gray[index - 1], gray[index + 1])
        if previous > 20.0 and following > 20.0 and skipped < 8.0:
            isolated_flashes.append(
                {
                    "frame": index,
                    "time": index / fps,
                    "previous_diff": previous,
                    "following_diff": following,
                    "skipped_diff": skipped,
                }
            )

    scenes = json.loads(scenes_file.read_text())
    cut_frames = sorted(
        {max(1, min(len(frames) - 1, round(cut * fps))) for cut in scenes["cuts"]}
    )
    boundaries = [0, *cut_frames, len(frames)]
    scene_runs = [
        {
            "start_frame": boundaries[index],
            "end_frame": boundaries[index + 1],
            "frames": boundaries[index + 1] - boundaries[index],
            "seconds": (boundaries[index + 1] - boundaries[index]) / fps,
        }
        for index in range(len(boundaries) - 1)
    ]
    short_runs = [run for run in scene_runs if run["frames"] < 12]

    thumb_width = 180
    thumb_height = 320
    label_height = 24
    samples = []
    for cut_frame in cut_frames:
        for frame_index, label in (
            (cut_frame - 1, "before"),
            (cut_frame, "at"),
            (cut_frame + 1, "after"),
        ):
            frame_index = max(0, min(len(frames) - 1, frame_index))
            rgb = cv2.cvtColor(frames[frame_index], cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb).resize(
                (thumb_width, thumb_height),
                Image.Resampling.LANCZOS,
            )
            samples.append((image, frame_index, label))

    columns = 6
    rows = math.ceil(len(samples) / columns)
    sheet = Image.new(
        "RGB",
        (columns * thumb_width, rows * (thumb_height + label_height)),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for sample_index, (image, frame_index, label) in enumerate(samples):
        column = sample_index % columns
        row = sample_index // columns
        x = column * thumb_width
        y = row * (thumb_height + label_height)
        sheet.paste(image, (x, y + label_height))
        draw.rectangle((x, y, x + thumb_width, y + label_height), fill="black")
        draw.text(
            (x + 5, y + 6),
            f"f{frame_index:04d} {frame_index / fps:06.3f}s {label}",
            fill="white",
            font=font,
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    contact_path = output_dir / "transition_before_at_after.jpg"
    sheet.save(contact_path, quality=92)
    report = {
        "frames_audited": len(frames),
        "fps": fps,
        "duration_seconds": len(frames) / fps,
        "detected_cut_frames": cut_frames,
        "scene_runs": scene_runs,
        "minimum_scene_run_frames": min(run["frames"] for run in scene_runs),
        "minimum_scene_run_seconds": min(run["seconds"] for run in scene_runs),
        "black_frames": black_frames,
        "frozen_runs_5_frames_or_longer": frozen_runs,
        "isolated_single_frame_flashes": isolated_flashes,
        "short_scene_runs_under_12_frames": short_runs,
        "passed": not (
            black_frames
            or frozen_runs
            or isolated_flashes
            or short_runs
        ),
        "transition_contact_sheet": str(contact_path),
    }
    report_path = output_dir / "framewise_qa.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_dir", type=Path)
    parser.add_argument("scenes_file", type=Path)
    parser.add_argument("--fps", type=float, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    audit(args.frames_dir, args.scenes_file, args.fps, args.output_dir)


if __name__ == "__main__":
    main()
