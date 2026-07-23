#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from googleflow_client import download, generate_veo


MODEL = "veo-3.1-lite-low-priority"
ANCHOR = Path("outputs/adswipe_1564/host/host_nyc_summer_identity_locked_01.png")
OUT_DIR = Path("outputs/adswipe_1564/host_clips")
OUT_PATH = OUT_DIR / "clip01_nyc_summer_hook.mp4"
META_PATH = OUT_DIR / "clip01_nyc_summer_hook.json"

PROMPT = """Native-speed handheld front-facing phone video. She walks forward at a relaxed, steady pace while holding the camera at arm's length. Keep her gaze mostly on the lens with natural brief glances toward the sidewalk ahead. Her shoulders and the camera have subtle authentic walking movement; the people, traffic, and street behind her move consistently with her forward motion. She speaks clearly in conversational American English with a serious, personal, slightly urgent tone. Keep the delivery natural and continuous, with ordinary breathing and no theatrical pauses.

Dialogue: "I used Depo-Provera years ago, then I was diagnosed with a brain meningioma. But I don't remember my shot dates."

Preserve the supplied first frame as the exact identity and scene source. No change to her identity, face, hair, clothing, or the established location. No cuts, no zoom, no reframing jump, no slow motion, no speed changes, no freeze frames, no duplicated pedestrians, no music, no captions, and no generated on-screen text. Keep natural city ambience quiet beneath the voice."""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Submitting {OUT_PATH.name} on {MODEL}", flush=True)
    result = generate_veo(
        PROMPT,
        image_path=str(ANCHOR),
        duration=8,
        seed=156401,
        aspect_ratio="portrait",
        model=MODEL,
        attempts=3,
    )
    META_PATH.write_text(
        json.dumps(
            {
                "provider": "useapi Google Flow unlimited",
                "model": MODEL,
                "duration": 8,
                "seed": 156401,
                "aspect_ratio": "portrait",
                "anchor": str(ANCHOR),
                "prompt": PROMPT,
                "result": result,
            },
            indent=2,
        )
        + "\n"
    )
    if result["status"] != "success" or not result["urls"]:
        raise RuntimeError(f"Generation failed: {result['raw']}")
    download(result["urls"][0], str(OUT_PATH))
    print(OUT_PATH, flush=True)


if __name__ == "__main__":
    main()
