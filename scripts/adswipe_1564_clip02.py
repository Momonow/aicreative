#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from googleflow_client import download, generate_veo


MODEL = "veo-3.1-lite-low-priority"
ANCHOR = Path(
    "outputs/adswipe_1564/host/gpt_anchor_candidates/"
    "anchor02_strict_single_frame.png"
)
OUT_DIR = Path("outputs/adswipe_1564/host_clips")
OUT_PATH = OUT_DIR / "clip02_nyc_summer_records_reassurance.mp4"
META_PATH = OUT_DIR / "clip02_nyc_summer_records_reassurance.json"

PROMPT = """Native-speed handheld front-facing phone video beginning exactly from the supplied frame. She walks forward at a relaxed, steady pace while holding the camera at arm's length. Keep her gaze mostly on the lens with brief natural checks of the sidewalk ahead. The camera, her shoulders, pedestrians, traffic, and street background all move consistently with forward walking. She gives a small matter-of-fact head shake on the first sentence and one restrained open-palm gesture with her free hand. Her delivery is clear conversational American English, serious and reassuring, with natural breathing and no theatrical pauses.

Dialogue: "Do not count yourself out just because the dates are fuzzy. You should not have to reconstruct the whole timeline before asking for a review."

Preserve the supplied first frame as the exact identity and scene source. No cuts, zoom, reframing jump, slow motion, speed changes, freeze frames, music, captions, or generated text. Keep natural city ambience quiet beneath the voice."""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Submitting {OUT_PATH.name} on {MODEL}", flush=True)
    result = generate_veo(
        PROMPT,
        image_path=str(ANCHOR),
        duration=8,
        seed=156402,
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
                "seed": 156402,
                "aspect_ratio": "portrait",
                "anchor": str(ANCHOR),
                "anchor_source": "approved strict single-frame GPT anchor 2",
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
