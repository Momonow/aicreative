#!/usr/bin/env python3
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import kie_client


OUT_DIR = Path("outputs/adswipe_1564/host/gpt_anchor_candidates")
IDENTITY = Path("outputs/adswipe_1564/host/host_nyc_summer_identity_locked_01.png")

ANCHORS = [
    {
        "slug": "anchor02_same_block_progressed",
        "pose": Path(
            "outputs/adswipe_1564/host/gpt_anchor_sources/clip01_f054_2.2s.jpg"
        ),
        "prompt": """Use the first supplied image as the exact identity, clothing, season, lighting, and phone-camera reference. Use the second supplied image as the walking pose and framing reference. Create a photorealistic vertical smartphone selfie frame a few yards farther along the same New York City summer sidewalk. Preserve the woman exactly: same face, apparent age, facial proportions, skin texture, curls, eyes, body, sage short-sleeve T-shirt, and arm-held phone perspective. Do not beautify, rejuvenate, or reinterpret her. Keep the same block, architecture, leafy trees, warm summer conditions, camera character, and direction of daylight, but update the background naturally as though she continued walking: different pedestrians in ordinary summer clothing, changed traffic positions, and the yellow taxi farther down the street. The frame must feel like a later moment from the same walk, not a new neighborhood or recreated set. Natural phone exposure, consistent shadows, detailed background, no artificial blur, no text, no logos, no readable signs, no duplicated people, and no malformed hands or faces.""",
    },
    {
        "slug": "anchor03_same_block_farther",
        "pose": Path(
            "outputs/adswipe_1564/host/gpt_anchor_sources/clip01_f139_5.75s.jpg"
        ),
        "prompt": """Use the first supplied image as the exact identity, clothing, season, lighting, and phone-camera reference. Use the second supplied image as the walking pose and framing reference. Create a photorealistic vertical smartphone selfie frame slightly farther down the same New York City summer block. Preserve the woman exactly: same face, apparent age, facial proportions, skin texture, curls, eyes, body, sage short-sleeve T-shirt, and arm-held phone perspective. Do not beautify, rejuvenate, or reinterpret her. Keep the same nearby buildings, leafy street character, sidewalk width, warm season, and natural daylight direction. Shift the viewpoint only enough to show that she has walked forward: a different street tree position, a new group of pedestrians behind her, and different cars moving through the background. Maintain believable geographic continuity and the same ordinary smartphone look. No new neighborhood, no dramatic relighting, no artificial blur, no text, no logos, no readable signs, no duplicated people, and no malformed hands or faces.""",
    },
    {
        "slug": "anchor04_same_block_near_corner",
        "pose": Path(
            "outputs/adswipe_1564/host/gpt_anchor_sources/clip01_f163_6.75s.jpg"
        ),
        "prompt": """Use the first supplied image as the exact identity, clothing, season, lighting, and phone-camera reference. Use the second supplied image as the walking pose and framing reference. Create a photorealistic vertical smartphone selfie frame later in the same walk, near the next part of the same New York City summer street. Preserve the woman exactly: same face, apparent age, facial proportions, skin texture, curls, eyes, body, sage short-sleeve T-shirt, and arm-held phone perspective. Do not beautify, rejuvenate, or reinterpret her. The block must remain recognizably continuous, with compatible buildings, leafy trees, sidewalk materials, summer daylight, and camera exposure. Show subtle forward progress through a slightly changed building and tree alignment, entirely different background pedestrians, and updated traffic positions. Keep the change modest and geographically plausible. No abrupt location change, no dramatic relighting, no artificial blur, no text, no logos, no readable signs, no duplicated people, and no malformed hands or faces.""",
    },
]


def generate(anchor: dict, identity_url: str) -> dict:
    pose_url = kie_client.upload_file(str(anchor["pose"]), "image/jpeg")
    result = kie_client.generate_gpt_image(
        anchor["prompt"],
        image_urls=[identity_url, pose_url],
        aspect_ratio="9:16",
        resolution="2K",
    )
    if result["status"] != "success" or not result.get("urls"):
        raise RuntimeError(f"{anchor['slug']} failed: {result.get('raw')}")
    output_path = OUT_DIR / f"{anchor['slug']}.png"
    kie_client.download(result["urls"][0], str(output_path))
    metadata = {
        "provider": "KIE",
        "model": "gpt-image-2-image-to-image",
        "resolution": "2K",
        "aspect_ratio": "9:16",
        "identity_reference": str(IDENTITY),
        "pose_reference": str(anchor["pose"]),
        "prompt": anchor["prompt"],
        "source_url": result["urls"][0],
        "output_path": str(output_path),
    }
    (OUT_DIR / f"{anchor['slug']}.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    return metadata


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    identity_url = kie_client.upload_file(str(IDENTITY), "image/png")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(generate, anchor, identity_url): anchor["slug"]
            for anchor in ANCHORS
        }
        for future in as_completed(futures):
            slug = futures[future]
            metadata = future.result()
            print(f"{slug}: {metadata['output_path']}", flush=True)


if __name__ == "__main__":
    main()
