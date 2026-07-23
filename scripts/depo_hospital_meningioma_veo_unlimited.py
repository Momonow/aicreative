"""Produce the 45-50s hospital meningioma UGC ad on free Veo 3.1 Lite.

Generate and QA one clip at a time so every output can be shown before inspection.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elevenlabs_client import scribe
from googleflow_client import download, generate_veo, upload_asset


ROOT = Path("outputs/depo_hospital_meningioma_veo_unlimited")
BASE_ANCHOR = Path("outputs/depo_meningioma_openers_omni/white_woman_post_op_scar_anchor.png")
MODEL = "veo-3.1-lite-low-priority"
LINES = [
    (8, "If you used Depo-Provera and were diagnosed with brain meningioma, you may qualify for significant financial compensation."),
    (8, "I'm still in the hospital trying to take everything in. My sister sent me this page because I used Depo for years."),
    (6, "I learned the diagnosis in your records matters. It needs to say brain meningioma."),
    (6, "This isn't about headaches or guessing. It's about that specific diagnosis in your medical records."),
    (8, "They ask whether you used Depo for a year or more and whether you were diagnosed afterward."),
    (8, "Even if this happened years ago, or you can't find every shot record, it may still be worth checking."),
    (6, "The questions are free and private. Tap the page below and see where you stand."),
]


def prompt_for(line):
    return f"""Use the supplied first frame as the sole visual source of truth. Continue that exact frame as a fixed-camera video. Do not redesign, restage, beautify, age-shift, or reinterpret any visible detail. Identity, face geometry, hair, eyes, skin texture, wardrobe, setting, lighting, framing, and camera position must remain unchanged from the supplied frame. No zoom, pan, reframing, cuts, or camera drift.

ACTION: She looks into the phone lens, blinks naturally, and speaks with restrained head and facial movement. Her mouth remains visible. No touching the incision and no dramatic gestures.

VOICE: Tired, plain-spoken adult American voice. Serious and steady, slightly fatigued, not theatrical, not an announcer, and not polished. Natural conversational pace around 2.3 words per second. Clear close phone-mic audio. Pronounce "meningioma" as "men-in-jee-OH-muh" and "Depo" as "DEP-oh."

She says ONLY the supplied spoken dialogue verbatim, with no extra, repeated, or improvised words, and then stops. No screen text, captions, subtitles, labels, logo, watermark, music, or added hospital sound effects.

SPOKEN DIALOGUE: "{line}"""


def tokens(text):
    return re.findall(r"[a-z0-9']+", text.lower().replace("depo-provera", "depo provera"))


def full_line_spoken(transcript, intended):
    heard = tokens(transcript)
    wanted = tokens(intended)
    pos = 0
    for word in heard:
        if pos < len(wanted) and word == wanted[pos]:
            pos += 1
    return pos == len(wanted)


def clip_path(number):
    return ROOT / f"clip{number:02d}.mp4"


def metadata_path(number):
    return ROOT / f"clip{number:02d}_generation.json"


def anchor_for(number):
    if number == 1:
        return BASE_ANCHOR
    anchor = ROOT / "anchors" / f"hospital_anchor_{number - 2}.jpg"
    if not anchor.exists():
        raise RuntimeError(f"Missing rotated clip-1 anchor: {anchor}")
    return anchor


def generate(number):
    ROOT.mkdir(parents=True, exist_ok=True)
    duration, line = LINES[number - 1]
    out = clip_path(number)
    meta = metadata_path(number)
    if out.exists() and meta.exists():
        saved = json.loads(meta.read_text())
        if saved.get("intended") == line and saved.get("model") == MODEL:
            print(f"[reuse] {out}")
            return

    anchor = anchor_for(number)
    image_mgid = upload_asset(str(anchor), "image/png" if anchor.suffix.lower() == ".png" else "image/jpeg")
    prompt = prompt_for(line)
    result = generate_veo(
        prompt=prompt,
        image_mgid=image_mgid,
        duration=duration,
        aspect_ratio="portrait",
        model=MODEL,
        attempts=3,
        ref_param="startImage",
    )
    if result.get("status") != "success" or not result.get("urls"):
        raise RuntimeError(f"clip {number} failed: {result.get('raw')}")
    download(result["urls"][0], str(out))
    meta.write_text(json.dumps({
        "model": MODEL,
        "duration": duration,
        "intended": line,
        "prompt": prompt,
        "anchor": str(anchor),
        "raw": result.get("raw"),
    }, indent=2))
    print(out)


def qa(number):
    duration, line = LINES[number - 1]
    video = clip_path(number)
    if not video.exists():
        raise RuntimeError(f"Missing {video}")
    raw = scribe(
        str(video), biased_keywords=["meningioma", "Depo-Provera", "Depo"], language_code="en"
    )
    transcript = raw.get("text", "")
    passed = full_line_spoken(transcript, line)
    keep_start = 0.0
    keep_end = None
    wanted = tokens(line)
    heard = []
    for item in raw.get("words", []):
        if item.get("type") != "word":
            continue
        for token in tokens(item.get("text", "")):
            heard.append((token, item.get("start"), item.get("end")))
    pos = 0
    first_start = None
    last_end = None
    first_match_index = None
    last_match_index = None
    for index, (word, start, end) in enumerate(heard):
        if pos < len(wanted) and word == wanted[pos]:
            if first_start is None:
                first_start = start
                first_match_index = index
            last_end = end
            last_match_index = index
            pos += 1
    if pos == len(wanted) and first_start is not None and last_end is not None:
        leading_extra = first_match_index not in (None, 0)
        trailing_extra = last_match_index is not None and last_match_index < len(heard) - 1
        keep_start = max(0.0, first_start - 0.04) if leading_extra else 0.0
        keep_end = last_end + (0.12 if trailing_extra else 0.40)
    out = ROOT / f"clip{number:02d}_qa.json"
    out.write_text(json.dumps({
        "intended": line,
        "transcript": transcript,
        "full_line_spoken": passed,
        "requested_duration": duration,
        "keep_start": keep_start,
        "keep_end": keep_end,
    }, indent=2))
    print(f"transcript: {transcript}")
    print("PASS" if passed else "FAIL")
    if not passed:
        raise RuntimeError(f"clip {number} transcript did not contain the full intended line")


def pick_anchors():
    out_dir = ROOT / "anchors"
    subprocess.run([
        sys.executable, "scripts/pick_clean_anchors.py", str(clip_path(1)),
        "--out-dir", str(out_dir), "--n", "6", "--prefix", "hospital_anchor",
    ], check=True)


def static_level(src, out):
    measured = subprocess.run([
        "ffmpeg", "-i", str(src), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ], check=True, capture_output=True, text=True)
    match = re.search(r"\{\s*\"input_i\".*?\n\}", measured.stderr, re.S)
    if not match:
        raise RuntimeError(f"Could not measure loudness for {src}")
    input_i = float(json.loads(match.group(0))["input_i"])
    gain = -16.0 - input_i
    subprocess.run([
        "ffmpeg", "-y", "-i", str(src),
        "-af", f"volume={gain:.2f}dB,alimiter=limit=0.891:level=disabled",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out),
    ], check=True, capture_output=True)


def assemble():
    trimmed = []
    for number in range(1, len(LINES) + 1):
        if not clip_path(number).exists():
            raise RuntimeError(f"Missing {clip_path(number)}")
        qa_file = ROOT / f"clip{number:02d}_qa.json"
        if not qa_file.exists():
            raise RuntimeError(f"Clip {number} has not passed transcript QA")
        qa_data = json.loads(qa_file.read_text())
        if not qa_data.get("full_line_spoken") or qa_data.get("keep_end") is None:
            raise RuntimeError(f"Clip {number} has not passed timestamped transcript QA")
        trim = ROOT / f"clip{number:02d}_trimmed.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{qa_data['keep_start']:.3f}", "-i", str(clip_path(number)),
            "-t", f"{max(0.2, qa_data['keep_end'] - qa_data['keep_start']):.3f}",
            "-vf", "scale=720:1280,fps=24,setsar=1", "-af", "aresample=44100",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", str(trim),
        ], check=True, capture_output=True)
        trimmed.append(trim)
    source_list = ROOT / "concat.txt"
    source_list.write_text("".join(f"file '{path.resolve()}'\n" for path in trimmed))
    raw = ROOT / "hospital_brain_meningioma_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(source_list),
        "-vf", "scale=720:1280,fps=24,setsar=1", "-af", "aresample=44100",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", str(raw),
    ], check=True, capture_output=True)
    final = ROOT / "hospital_brain_meningioma_veo_unlimited_clean.mp4"
    static_level(raw, final)
    print(final)


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--generate", type=int, choices=range(1, len(LINES) + 1))
    action.add_argument("--qa", type=int, choices=range(1, len(LINES) + 1))
    action.add_argument("--pick-anchors", action="store_true")
    action.add_argument("--assemble", action="store_true")
    args = parser.parse_args()
    if args.generate:
        generate(args.generate)
    elif args.qa:
        qa(args.qa)
    elif args.pick_anchors:
        pick_anchors()
    else:
        assemble()


if __name__ == "__main__":
    main()
