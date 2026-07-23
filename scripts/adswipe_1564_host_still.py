#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import kie_client


OUT_DIR = Path("outputs/adswipe_1564/host")
OUT_PATH = OUT_DIR / "host_living_room_candidate_01.png"
META_PATH = OUT_DIR / "host_living_room_candidate_01.json"

PROMPT = """Create a photorealistic vertical smartphone selfie frame for an authentic UGC video. A Black woman around 50 sits upright in a bright living-room armchair beside a window during daytime. She has a warm medium-dark complexion, shoulder-length natural curls, clearly open brown eyes looking directly into the phone camera, and a calm but concerned, ready-to-explain expression. She wears a simple forest-green crewneck top with a casual charcoal cardigan. Frame her from mid-torso upward at arm's length, eye-level, with natural handheld phone perspective and a little ordinary asymmetry. The room feels real and lived-in: soft daylight, a side table, a neutral sofa edge, and modest home details in the background, all secondary and slightly out of focus. No bed, no bedroom, no hospital, no glamour styling, no studio lighting, no beauty retouching, no text, no captions, no logos, no medical props. Natural skin texture, realistic hands, believable phone-camera exposure, documentary realism. Vertical 9:16 composition with enough clean space in the upper third for a comment card and enough clear space below center for captions."""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = kie_client.generate_gpt_image(
        PROMPT,
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
                "resolution": "2K",
                "aspect_ratio": "9:16",
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
