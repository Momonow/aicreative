#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from googleflow_client import download, generate_veo


MODEL = "veo-3.1-lite-low-priority"
ANCHOR = Path(
    "outputs/adswipe_1564/host/gpt_anchor_candidates/"
    "anchor04_strict_single_frame.png"
)
OUT_DIR = Path("outputs/adswipe_1564/host_clips")
OUT_PATH = OUT_DIR / "clip04_nyc_summer_private_review.mp4"
META_PATH = OUT_DIR / "clip04_nyc_summer_private_review.json"

PROMPT = """Native-speed handheld front-facing phone video beginning exactly from the supplied frame. She walks forward naturally while holding the phone at arm's length. Keep realistic step movement, direct eye contact, ordinary breathing, and consistent background motion. Her expression softens slightly as she reassures the viewer, with one small open-palm gesture and no exaggerated performance. Her conversational American English remains clear, personal, and steady.

Dialogue: "A private claim review can look at what you remember and help determine what information may still be available. You don't have to figure it out alone."

Preserve the supplied first frame as the exact identity and scene source. No cuts, zoom, reframing jump, slow motion, speed changes, freeze frames, music, captions, or generated text. Keep natural city ambience quiet beneath the voice."""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Submitting {OUT_PATH.name} on {MODEL}", flush=True)
    result = generate_veo(
        PROMPT,
        image_path=str(ANCHOR),
        duration=8,
        seed=156404,
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
                "seed": 156404,
                "aspect_ratio": "portrait",
                "anchor": str(ANCHOR),
                "anchor_source": "approved strict single-frame GPT anchor 4",
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
