"""Finalize the approved Depo podcast ad without changing native playback speed.

Steps:
1. Trim each host clip to scripted speech and remove timestamped internal backchannels.
2. Normalize cross-clip voice drift with an ElevenLabs clone of the clean host takes.
3. Concatenate the host read and add only the approved B-roll slate.
"""

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elevenlabs_client import clone_voice, voice_changer


ROOT = Path("outputs/depo_podcast_1419_clone/final")
BROLL_ROOT = Path("outputs/depo_podcast_1419_clone/broll")
TRIM_CONFIG = {
    1: {"start": 0.559, "end": 7.259, "remove": [(4.55, 4.70)]},
    2: {"start": 0.060, "end": 3.319, "remove": [(0.26, 0.33)]},
    3: {"start": 0.439, "end": 6.639, "remove": [(3.76, 4.04)]},
    4: {"start": 0.000, "end": 3.510, "remove": []},
    5: {"start": 0.579, "end": 4.679, "remove": []},
    6: {"start": 0.480, "end": 3.320, "remove": []},
    7: {"start": 0.579, "end": 6.839, "remove": []},
    8: {"start": 0.159, "end": 7.920, "remove": [(4.20, 4.52), (5.59, 5.80)]},
    9: {"start": 0.260, "end": 7.920, "remove": []},
}
CTA_PATH = BROLL_ROOT / "17_mobile_eligibility_screenshot_sequence.mp4"
OUTPUT_FPS = 24
# Frame-quantized edit. Adjacent B-roll cuts share one exact boundary; later
# proof clips have deliberate host breathing room between them.
EDIT_SEGMENTS = [
    {"slug": "hospital_bed", "kind": "broll", "start": 0, "end": 38,
     "path": BROLL_ROOT / "09_hospital_bed_bandaged_white.mp4", "source_start": 0.30},
    {"slug": "recovery_selfie", "kind": "broll", "start": 38, "end": 63,
     "path": BROLL_ROOT / "10_recovery_selfie_white.mp4", "source_start": 0.50},
    {"slug": "host_open", "kind": "host", "start": 63, "end": 90},
    {"slug": "healing_incision", "kind": "broll", "start": 90, "end": 135,
     "path": BROLL_ROOT / "11_healing_incision_white.mp4", "source_start": 0.50},
    {"slug": "host_specificity", "kind": "host", "start": 135, "end": 231},
    {"slug": "depo_packaging", "kind": "broll", "start": 231, "end": 321,
     "path": BROLL_ROOT / "01_depo_real.mp4", "source_start": 0.40},
    {"slug": "host_claim_bridge", "kind": "host", "start": 321, "end": 354},
    {"slug": "doctor_scan_impact", "kind": "broll", "start": 354, "end": 411,
     "path": BROLL_ROOT / "12_doctor_scan_reaction.mp4", "source_start": 0.40},
    {"slug": "host_objections", "kind": "host", "start": 411, "end": 615},
    {"slug": "recovery_corridor", "kind": "broll", "start": 615, "end": 671,
     "path": BROLL_ROOT / "14_recovery_corridor_black.mp4", "source_start": 0.40},
    {"slug": "host_diagnosis_setup", "kind": "host", "start": 671, "end": 806},
    {"slug": "mri_comparison", "kind": "broll", "start": 806, "end": 925,
     "path": BROLL_ROOT / "02_mri.mp4", "source_start": 0.40},
    {"slug": "host_cta_setup", "kind": "host", "start": 925, "end": 968},
    {"slug": "mobile_eligibility", "kind": "broll", "start": 968, "end": 1139,
     "path": CTA_PATH, "source_start": 0.00},
]


def run(command, **kwargs):
    return subprocess.run(command, check=True, **kwargs)


def probe_duration(path):
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def measure_lufs(path):
    measured = run(
        [
            "ffmpeg",
            "-i",
            str(path),
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    match = re.search(r"\{\s*\"input_i\".*?\n\}", measured.stderr, re.S)
    if not match:
        raise RuntimeError(f"Could not measure loudness for {path}")
    return float(json.loads(match.group(0))["input_i"])


def kept_segments(config):
    cursor = config["start"]
    segments = []
    for remove_start, remove_end in config["remove"]:
        if remove_start > cursor:
            segments.append((cursor, remove_start))
        cursor = max(cursor, remove_end)
    if cursor < config["end"]:
        segments.append((cursor, config["end"]))
    return segments


def trim_clip(number):
    source = ROOT / f"clip{number:02d}.mp4"
    output = ROOT / "trimmed" / f"clip{number:02d}_trimmed.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        return output

    segments = kept_segments(TRIM_CONFIG[number])
    filters = []
    concat_inputs = []
    for index, (start, end) in enumerate(segments):
        filters.extend(
            [
                (
                    f"[0:v]trim=start={start:.3f}:end={end:.3f},"
                    f"setpts=PTS-STARTPTS,scale=720:1280,fps=24,setsar=1[v{index}]"
                ),
                (
                    f"[0:a]atrim=start={start:.3f}:end={end:.3f},"
                    f"asetpts=PTS-STARTPTS,aresample=44100[a{index}]"
                ),
            ]
        )
        concat_inputs.append(f"[v{index}][a{index}]")
    filters.append(
        "".join(concat_inputs)
        + f"concat=n={len(segments)}:v=1:a=1[vout][aout]"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[vout]",
            "-map",
            "[aout]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output),
        ],
        capture_output=True,
    )
    return output


def trim_all():
    outputs = [trim_clip(number) for number in range(1, 10)]
    manifest = {
        f"clip{number:02d}": {
            "source": str(ROOT / f"clip{number:02d}.mp4"),
            "output": str(outputs[number - 1]),
            "config": TRIM_CONFIG[number],
            "duration": probe_duration(outputs[number - 1]),
            "speed_change": False,
        }
        for number in range(1, 10)
    }
    (ROOT / "native_speed_trim_manifest.json").write_text(json.dumps(manifest, indent=2))
    for output in outputs:
        print(output, flush=True)


def extract_audio(video, output):
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-vn",
            "-ar",
            "44100",
            "-ac",
            "1",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(output),
        ],
        capture_output=True,
    )


def make_voice_id():
    work = ROOT / "voice_consistency"
    work.mkdir(parents=True, exist_ok=True)
    cache = work / "voice_id.txt"
    if cache.exists() and cache.read_text().strip():
        return cache.read_text().strip()

    samples = []
    for number in (1, 5, 8):
        source = ROOT / "trimmed" / f"clip{number:02d}_trimmed.mp4"
        audio = work / f"clone_clip{number:02d}.mp3"
        extract_audio(source, audio)
        samples.append(audio)
    voice_id = clone_voice(
        "depo_podcast_1419_host_v1",
        [str(path) for path in samples],
        description="Approved Depo meningioma independent-podcast host",
    )
    cache.write_text(voice_id)
    return voice_id


def remux_voice(video, changed_audio, output):
    duration = probe_duration(video)
    input_lufs = measure_lufs(changed_audio)
    gain = -18.0 - input_lufs
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-i",
            str(changed_audio),
            "-filter_complex",
            (
                f"[1:a]volume={gain:.2f}dB,alimiter=limit=0.891:level=disabled,"
                f"apad=pad_dur={duration:.3f}[a]"
            ),
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-t",
            f"{duration:.3f}",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-ar",
            "44100",
            "-b:a",
            "192k",
            str(output),
        ],
        capture_output=True,
    )


def voice_normalize():
    trim_all()
    voice_id = make_voice_id()
    work = ROOT / "voice_consistency"

    def convert(number):
        source_video = ROOT / "trimmed" / f"clip{number:02d}_trimmed.mp4"
        source_audio = work / f"clip{number:02d}_source.mp3"
        changed_audio = work / f"clip{number:02d}_voice.mp3"
        output = work / f"clip{number:02d}_voice.mp4"
        if output.exists():
            return number, output
        extract_audio(source_video, source_audio)
        if not changed_audio.exists():
            voice_changer(
                str(source_audio),
                voice_id,
                str(changed_audio),
                model_id="eleven_english_sts_v2",
                stability=0.5,
                similarity_boost=0.70,
                output_format="mp3_44100_192",
                remove_background_noise=True,
                use_speaker_boost=False,
            )
        remux_voice(source_video, changed_audio, output)
        return number, output

    outputs = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(convert, number) for number in range(1, 10)]
        for future in as_completed(futures):
            number, output = future.result()
            outputs[number] = output
            print(output, flush=True)
    return [outputs[number] for number in range(1, 10)]


def concat_host():
    clips = voice_normalize()
    concat_file = ROOT / "voice_consistency" / "concat.txt"
    concat_file.write_text(
        "".join(f"file '{clip.resolve()}'\n" for clip in clips)
    )
    stitched = ROOT / "depo_podcast_1419_host_voice_consistent_raw.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(stitched),
        ],
        capture_output=True,
    )
    measured = measure_lufs(stitched)
    output = ROOT / "depo_podcast_1419_host_voice_consistent.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(stitched),
            "-af",
            f"volume={-16.0 - measured:.2f}dB,alimiter=limit=0.841:level=disabled",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output),
        ],
        capture_output=True,
    )
    print(output, flush=True)
    return output


def add_broll():
    host = concat_host()
    host_frames = 1139
    command = ["ffmpeg", "-y", "-i", str(host)]
    input_indexes = {}
    next_input = 1
    for item in EDIT_SEGMENTS:
        if item["kind"] != "broll":
            continue
        path = item["path"]
        if path not in input_indexes:
            input_indexes[path] = next_input
            command.extend(["-i", str(path)])
            next_input += 1

    filters = []
    segment_labels = []
    for index, item in enumerate(EDIT_SEGMENTS):
        label = f"s{index}"
        frame_count = item["end"] - item["start"]
        if item["kind"] == "host":
            filters.append(
                (
                    f"[0:v]trim=start_frame={item['start']}:end_frame={item['end']},"
                    f"setpts=PTS-STARTPTS,scale=720:1280,fps={OUTPUT_FPS},setsar=1[{label}]"
                )
            )
        else:
            input_index = input_indexes[item["path"]]
            source_start_frame = round(item["source_start"] * OUTPUT_FPS)
            source_end_frame = source_start_frame + frame_count
            filters.append(
                (
                    f"[{input_index}:v]fps={OUTPUT_FPS},"
                    f"trim=start_frame={source_start_frame}:end_frame={source_end_frame},"
                    "setpts=PTS-STARTPTS,"
                    "scale=720:1280:force_original_aspect_ratio=increase,"
                    f"crop=720:1280,setsar=1[{label}]"
                )
            )
        segment_labels.append(f"[{label}]")
    filters.append(
        "".join(segment_labels)
        + f"concat=n={len(segment_labels)}:v=1:a=0[vout]"
    )

    output = ROOT / "depo_podcast_1419_combined_clean.mp4"
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[vout]",
            "-map",
            "0:a:0",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    run(command, capture_output=True)
    (ROOT / "broll_timeline.json").write_text(
        json.dumps(
            {
                "duration": host_frames / OUTPUT_FPS,
                "total_frames": host_frames,
                "fps": OUTPUT_FPS,
                "native_speed_only": True,
                "timeline": [
                    {
                        **item,
                        "path": str(item["path"]) if item.get("path") else None,
                        "start_seconds": item["start"] / OUTPUT_FPS,
                        "end_seconds": item["end"] / OUTPUT_FPS,
                    }
                    for item in EDIT_SEGMENTS
                ],
            },
            indent=2,
        )
    )
    print(output, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=["trim", "voice", "host", "combined"],
    )
    args = parser.parse_args()
    if args.action == "trim":
        trim_all()
    elif args.action == "voice":
        voice_normalize()
    elif args.action == "host":
        concat_host()
    else:
        add_broll()


if __name__ == "__main__":
    main()
