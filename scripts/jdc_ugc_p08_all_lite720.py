"""Regenerate ALL 5 clips on KIE Veo 3.1 Lite at 720p for uniform UGC aesthetic.

Lite 720p delivers: natural softness (no over-sharpening), broadcast audio,
exact transcripts, smaller files. Matches "real phone capture" UGC vibe.

Anchors used (reuse existing — character consistency holds across resolutions):
  clip 1: persona_08 original
  clip 2a: clip2a_anchor_at_1.5s.jpg (extracted from prior clip 1)
  clip 2b: clip2b_anchor_at_4.5s.jpg
  clip 3:  clip3_anchor_at_3.0s.jpg
  clip 4:  clip4_anchor_at_6.0s.jpg

All submitted in parallel via ThreadPoolExecutor (different anchor URLs = no
per-URL rate-limit hit).

Output: outputs/illinois_jdc_ugc/clips/p08_clip{N}_lite720.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download

# Pull prompts that worked
from jdc_ugc_p08_clip1 import PROMPT as CLIP1_PROMPT
from jdc_ugc_p08_clips234 import CLIP3_PROMPT, CLIP4_PROMPT
from jdc_ugc_p08_clip2_split import CLIP2A_PROMPT, CLIP2B_PROMPT

ANCHOR_DIR = Path("outputs/illinois_jdc_ugc/anchors")
PERSONA_ANCHOR = Path("outputs/illinois_jdc_ugc/personas/persona_08_chicago_bus_stop.png")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")

CLIPS = [
    ("clip1",  PERSONA_ANCHOR,                              CLIP1_PROMPT,  OUT_DIR / "p08_clip1_lite720.mp4"),
    ("clip2a", ANCHOR_DIR / "clip2a_anchor_at_1.5s.jpg",    CLIP2A_PROMPT, OUT_DIR / "p08_clip2a_lite720.mp4"),
    ("clip2b", ANCHOR_DIR / "clip2b_anchor_at_4.5s.jpg",    CLIP2B_PROMPT, OUT_DIR / "p08_clip2b_lite720.mp4"),
    ("clip3",  ANCHOR_DIR / "clip3_anchor_at_3.0s.jpg",     CLIP3_PROMPT,  OUT_DIR / "p08_clip3_lite720.mp4"),
    ("clip4",  ANCHOR_DIR / "clip4_anchor_at_6.0s.jpg",     CLIP4_PROMPT,  OUT_DIR / "p08_clip4_lite720.mp4"),
]


def submit_one(slug, anchor_path, prompt, out_path):
    print(f"[{slug}] uploading to KIE storage", flush=True)
    url = kie_upload(str(anchor_path))
    print(f"[{slug}] url: {url}", flush=True)
    print(f"[{slug}] submitting (prompt {len(prompt)} chars)", flush=True)
    r = kie_generate_veo(
        prompt=prompt,
        aspect_ratio="9:16",
        image_urls=[url, url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_lite",
        resolution="720p",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    kie_download(r["urls"][0], str(out_path))
    return slug, "success", str(out_path)


def main():
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(submit_one, s, a, p, o): s for s, a, p, o in CLIPS}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
