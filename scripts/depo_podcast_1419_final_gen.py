"""Generate the approved Depo podcast host read on useapi Google Flow unlimited.

The runner is intentionally sequential: generate one clip, inspect it, then continue.
Clips 2-N use rotated, eyes-open frames selected from clip 1.
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


ROOT = Path("outputs/depo_podcast_1419_clone/final")
BASE_ANCHOR = Path("outputs/depo_podcast_1419_clone/podcast_host_anchor.png")
MODEL = "veo-3.1-lite-low-priority"
LINES = [
    (8, "Can I tell you the part about the Depo shot that bothered me most? It wasn't the headlines."),
    (4, "It was realizing how specific this actually is."),
    (8, "Women who used the Depo shot for a year or more and were later diagnosed with brain meningioma."),
    (4, "They may qualify for significant potential compensation."),
    (6, "And I know the questions people have. What if it was years ago?"),
    (4, "It may still be worth having your case reviewed."),
    (8, "What if your old shot records are incomplete? Start with the medical information you do have."),
    (8, "Look through your records for the words brain meningioma. Not headaches. Not just feeling off. An actual diagnosis."),
    (8, "If you see that diagnosis, answer a few private questions below. The review is free and only takes a couple of minutes."),
]


def prompt_for(line):
    return f"""Continue the supplied first frame as one fixed-camera shot. Treat the supplied frame as the sole visual truth and preserve every visible person and scene detail exactly. Do not redesign, restage, beautify, age-shift, or reinterpret anything visible.

ACTION: She delivers a private single-speaker monologue while looking slightly past the camera, with natural blinks, restrained facial expression, and small conversational head movements. Her mouth remains visible. Keep the performance continuous and understated.

VOICE: Calm, serious, ordinary independent-podcast delivery, never a newscaster, announcer, or commercial voice. Natural adult American woman's voice at roughly 2.3 to 2.5 words per second. Dry, isolated, clear close-microphone audio. Pronounce "Depo" as "DEH-poh," two syllables ending in a clear long OH sound, with absolutely no final T sound. Pronounce "meningioma" as "men-in-jee-OH-muh."

CAMERA AND SCENE: Keep the camera fixed. No cuts, zooms, pans, reframing, camera drift, added people, added objects, screen text, captions, graphics, music, sound effects, logo, or watermark.

Exactly one voice is audible: hers. Generate no listener, interviewer, second voice, backchannel noise, acknowledgement, "mm-hmm," filler sound, or response. Keep silence around her words. She says ONLY the supplied spoken dialogue verbatim, with no extra, repeated, or improvised words, and then stops.

SPOKEN DIALOGUE: "{line}\""""


def tokens(text):
    parsed = re.findall(r"[a-z0-9']+", text.lower().replace("depo-provera", "depo provera"))
    # Scribe commonly spells the brand's /dee-poh/ audio as the homophone "depot".
    return ["depo" if token == "depot" else token for token in parsed]


def full_line_spoken(transcript, intended):
    heard = tokens(transcript)
    wanted = tokens(intended)
    position = 0
    for word in heard:
        if position < len(wanted) and word == wanted[position]:
            position += 1
    return position == len(wanted)


def clip_path(number):
    return ROOT / f"clip{number:02d}.mp4"


def metadata_path(number):
    return ROOT / f"clip{number:02d}_generation.json"


def qa_path(number):
    return ROOT / f"clip{number:02d}_qa.json"


def anchor_for(number):
    if number == 1:
        return BASE_ANCHOR
    anchor = ROOT / "anchors" / f"podcast_anchor_{number - 2}.jpg"
    if not anchor.exists():
        raise RuntimeError(f"Missing rotated clip-1 anchor: {anchor}")
    return anchor


def generate(number):
    ROOT.mkdir(parents=True, exist_ok=True)
    duration, line = LINES[number - 1]
    output = clip_path(number)
    metadata = metadata_path(number)
    prompt = prompt_for(line)

    if output.exists() and metadata.exists():
        saved = json.loads(metadata.read_text())
        if (
            saved.get("intended") == line
            and saved.get("model") == MODEL
            and saved.get("duration") == duration
        ):
            print(f"[reuse] {output}", flush=True)
            return

    anchor = anchor_for(number)
    content_type = "image/png" if anchor.suffix.lower() == ".png" else "image/jpeg"
    print(f"provider=useapi google-flow model={MODEL}", flush=True)
    print(f"anchor={anchor}", flush=True)
    print(f"prompt:\n{prompt}", flush=True)
    image_mgid = upload_asset(str(anchor), content_type)
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

    download(result["urls"][0], str(output))
    metadata.write_text(
        json.dumps(
            {
                "provider": "useapi google-flow unlimited",
                "model": MODEL,
                "duration": duration,
                "intended": line,
                "prompt": prompt,
                "anchor": str(anchor),
                "raw": result.get("raw"),
            },
            indent=2,
        )
    )
    print(output, flush=True)


def word_timing(raw, intended):
    wanted = tokens(intended)
    heard = []
    for item in raw.get("words", []):
        if item.get("type") != "word":
            continue
        for token in tokens(item.get("text", "")):
            heard.append((token, item.get("start"), item.get("end")))

    position = 0
    first_start = None
    last_end = None
    first_match_index = None
    last_match_index = None
    for index, (word, start, end) in enumerate(heard):
        if position < len(wanted) and word == wanted[position]:
            if first_start is None:
                first_start = start
                first_match_index = index
            last_end = end
            last_match_index = index
            position += 1

    if position != len(wanted) or first_start is None or last_end is None:
        return None, None

    leading_extra = first_match_index not in (None, 0)
    trailing_extra = last_match_index is not None and last_match_index < len(heard) - 1
    keep_start = max(0.0, first_start - 0.04) if leading_extra else 0.0
    keep_end = last_end + (0.12 if trailing_extra else 0.32)
    return keep_start, keep_end


def qa(number):
    duration, line = LINES[number - 1]
    video = clip_path(number)
    if not video.exists():
        raise RuntimeError(f"Missing {video}")

    raw = scribe(
        str(video),
        biased_keywords=[
            "meningioma",
            "Depo",
            "Depo-Provera",
            "significant potential compensation",
        ],
        language_code="en",
    )
    transcript = raw.get("text", "")
    passed = full_line_spoken(transcript, line)
    keep_start, keep_end = word_timing(raw, line)
    output = qa_path(number)
    output.write_text(
        json.dumps(
            {
                "intended": line,
                "transcript": transcript,
                "full_line_spoken": passed,
                "requested_duration": duration,
                "keep_start": keep_start,
                "keep_end": keep_end,
                "scribe": raw,
            },
            indent=2,
        )
    )
    print(f"transcript: {transcript}", flush=True)
    print("PASS" if passed and keep_end is not None else "FAIL", flush=True)
    if not passed or keep_end is None:
        raise RuntimeError(f"clip {number} transcript did not contain the full intended line")


def pick_anchors():
    output_dir = ROOT / "anchors"
    subprocess.run(
        [
            sys.executable,
            "scripts/pick_clean_anchors.py",
            str(clip_path(1)),
            "--out-dir",
            str(output_dir),
            "--n",
            str(len(LINES) - 1),
            "--prefix",
            "podcast_anchor",
        ],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--generate", type=int, choices=range(1, len(LINES) + 1))
    action.add_argument("--qa", type=int, choices=range(1, len(LINES) + 1))
    action.add_argument("--pick-anchors", action="store_true")
    args = parser.parse_args()

    if args.generate:
        generate(args.generate)
    elif args.qa:
        qa(args.qa)
    else:
        pick_anchors()


if __name__ == "__main__":
    main()
