"""Submit clip 2a + 2b via KIE Veo 3.1 Lite (Poyo Fast is in outage).

Per provider-match rule: KIE gen → KIE storage upload.
Reuses anchors already extracted (1.5s, 4.5s from clip 1) but re-uploads
via kie_client.upload_file.

Prompts imported from jdc_ugc_p08_clip2_split (same dialogue, same pace lock).
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download
from jdc_ugc_p08_clip2_split import CLIP2A_PROMPT, CLIP2B_PROMPT

ANCHOR_DIR = Path("outputs/illinois_jdc_ugc/anchors")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")

CLIPS = [
    ("clip2a", ANCHOR_DIR / "clip2a_anchor_at_1.5s.jpg", CLIP2A_PROMPT, OUT_DIR / "p08_clip2a.mp4"),
    ("clip2b", ANCHOR_DIR / "clip2b_anchor_at_4.5s.jpg", CLIP2B_PROMPT, OUT_DIR / "p08_clip2b.mp4"),
]


def submit_one(slug, anchor_jpg, prompt, out_path):
    print(f"[{slug}] uploading to KIE storage", flush=True)
    url = kie_upload(str(anchor_jpg))
    print(f"[{slug}] url: {url}", flush=True)
    print(f"[{slug}] submitting (prompt {len(prompt)} chars)", flush=True)
    r = kie_generate_veo(
        prompt=prompt,
        aspect_ratio="9:16",
        image_urls=[url, url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_fast",
        resolution="1080p",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    kie_download(r["urls"][0], str(out_path))
    return slug, "success", str(out_path)


def main():
    with ThreadPoolExecutor(max_workers=2) as ex:
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
