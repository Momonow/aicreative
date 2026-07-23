#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import kie_client


OUT_DIR = Path("outputs/adswipe_1564/host")
REFERENCE_PATH = OUT_DIR / "host_living_room_candidate_01.png"
OUT_PATH = OUT_DIR / "host_nyc_street_candidate_01.png"
META_PATH = OUT_DIR / "host_nyc_street_candidate_01.json"

PROMPT = """Using the supplied woman as the exact identity reference, create a photorealistic vertical smartphone selfie frame from an authentic UGC video. Preserve her face, age, complexion, natural curls, eye appearance, and realistic skin texture. She is now outdoors, walking along a busy New York City sidewalk in daytime while holding the phone at arm's length and talking directly to it. Frame her from mid-torso upward with an eye-level front-facing phone-camera perspective. Her expression is concerned, alert, and ready to explain something important. Keep the same forest-green top and charcoal cardigan for identity continuity. Behind her, show a lively but believable Manhattan street with pedestrians moving in both directions, traffic, yellow taxis, crosswalk activity, storefronts, and mid-rise city buildings. The background should feel busy and energetic while remaining secondary to her face, with natural depth and slight motion character but no artificial portrait blur. Overcast-bright daylight, realistic phone exposure, ordinary handheld asymmetry, documentary realism. Leave usable space in the upper third for a comment card and below center for captions. No bed, no indoor room, no hospital, no glamour styling, no studio lighting, no beauty retouching, no text, no captions, no logos, no readable storefront signs, no medical props, and no duplicated or malformed people."""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    reference_url = kie_client.upload_file(str(REFERENCE_PATH), "image/png")
    result = kie_client.generate_gpt_image(
        PROMPT,
        image_urls=[reference_url],
        aspect_ratio="9:16",
        resolution="2K",
    )
    source_url = result["urls"][0]
    kie_client.download(source_url, str(OUT_PATH))
    META_PATH.write_text(
        json.dumps(
            {
                "provider": "KIE",
                "model": "generate_gpt_image",
                "mode": "image-to-image",
                "resolution": "2K",
                "aspect_ratio": "9:16",
                "identity_reference": str(REFERENCE_PATH),
                "prompt": PROMPT,
                "source_url": source_url,
                "output_path": str(OUT_PATH),
            },
            indent=2,
        )
        + "\n"
    )
    print(OUT_PATH)


if __name__ == "__main__":
    main()
