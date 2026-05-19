"""Submit ONE Veo Lite 1080p clip 1 candidate. Serial submission to avoid
KIE host rate-limit (HTTP 429) hit by 3 parallel image fetches.

Strategy: submit one, wait for completion, audit, decide whether to re-roll.

Same strengthened single-speaker prompt as jdc_news_clip1_rerolls.py.

Output: outputs/illinois_jdc_news_eltracks/clip1_v5.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file, generate_veo as kie_generate_veo, download as kie_download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks")
ANCHOR_LOCAL = OUT_DIR / "anchor" / "composite_v2.jpg"
ANCHOR_URL_CACHE = OUT_DIR / "clip1_anchor_url.txt"
OUTPUT_CLIP = OUT_DIR / "clip1_v5.mp4"

# Import the prompt from the rerolls script
from jdc_news_clip1_rerolls import PROMPT


def main():
    if ANCHOR_URL_CACHE.exists():
        anchor_url = ANCHOR_URL_CACHE.read_text().strip()
    else:
        anchor_url = upload_file(str(ANCHOR_LOCAL))
        ANCHOR_URL_CACHE.write_text(anchor_url)
    print(f"Anchor URL: {anchor_url}")
    print(f"Prompt length: {len(PROMPT)} chars")
    print("Submitting ONE Veo Lite 1080p candidate (serial)...")

    r = kie_generate_veo(
        prompt=PROMPT,
        aspect_ratio="9:16",
        image_urls=[anchor_url, anchor_url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_fast",
        resolution="1080p",
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"FAILED: {str(r.get('raw'))[:500]}")
        return
    print(f"Downloading: {r['urls'][0]}")
    kie_download(r["urls"][0], str(OUTPUT_CLIP))
    print(f"DONE → {OUTPUT_CLIP}")


if __name__ == "__main__":
    main()
