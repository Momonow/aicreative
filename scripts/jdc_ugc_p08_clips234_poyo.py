"""Regenerate clips 2/3/4 on POYO Veo 3.1 Fast (different infra, same prompts).

Uses Poyo storage for uploads (per provider-match rule: Poyo gen → Poyo upload).
Re-uploads the rotated anchor JPGs from outputs/illinois_jdc_ugc/anchors/.

Output: outputs/illinois_jdc_ugc/clips/p08_clip{2,3,4}_poyo.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import upload_file as poyo_upload, generate_veo as poyo_generate_veo, download as poyo_download

# Import the prompts that worked
from jdc_ugc_p08_clips234 import CLIP2_PROMPT, CLIP3_PROMPT, CLIP4_PROMPT

ANCHOR_DIR = Path("outputs/illinois_jdc_ugc/anchors")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")

CLIPS = [
    ("clip2", ANCHOR_DIR / "clip2_anchor_at_0.7s.jpg", CLIP2_PROMPT, OUT_DIR / "p08_clip2_poyo.mp4"),
    ("clip3", ANCHOR_DIR / "clip3_anchor_at_3.0s.jpg", CLIP3_PROMPT, OUT_DIR / "p08_clip3_poyo.mp4"),
    ("clip4", ANCHOR_DIR / "clip4_anchor_at_6.0s.jpg", CLIP4_PROMPT, OUT_DIR / "p08_clip4_poyo.mp4"),
]


def submit_one(slug, anchor_jpg, prompt, out_path):
    print(f"[{slug}] uploading anchor to Poyo storage", flush=True)
    url = poyo_upload(str(anchor_jpg))
    print(f"[{slug}] url: {url}", flush=True)
    print(f"[{slug}] submitting (prompt {len(prompt)} chars)", flush=True)
    r = poyo_generate_veo(
        prompt=prompt,
        image_urls=[url, url],
        aspect_ratio="9:16",
        resolution="720p",
        generation_type="frame",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    poyo_download(r["urls"][0], str(out_path))
    return slug, "success", str(out_path)


def main():
    with ThreadPoolExecutor(max_workers=3) as ex:
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
