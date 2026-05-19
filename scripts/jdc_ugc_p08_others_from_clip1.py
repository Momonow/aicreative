"""Step 2+3: Extract fresh anchors from new clip 1 (Lite 720p) and submit
clips 2a/2b/3/4 in parallel.

Source clip 1: outputs/illinois_jdc_ugc/clips/p08_clip1_lite720.mp4

Anchors extracted (different timestamps per clip):
  clip 2a → 1.5s
  clip 2b → 4.5s
  clip 3  → 3.0s
  clip 4  → 6.0s

All submitted on KIE Veo 3.1 Lite 720p, parallel via ThreadPoolExecutor.

Output: outputs/illinois_jdc_ugc/clips/p08_clip{N}_lite720.mp4
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download
from jdc_ugc_p08_clips234 import CLIP3_PROMPT, CLIP4_PROMPT
from jdc_ugc_p08_clip2_split import CLIP2A_PROMPT, CLIP2B_PROMPT

CLIP1 = Path("outputs/illinois_jdc_ugc/clips/p08_clip1_lite720.mp4")
ANCHOR_DIR = Path("outputs/illinois_jdc_ugc/anchors_lite720")
ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")

CLIPS = [
    ("clip2a", 1.5, CLIP2A_PROMPT, OUT_DIR / "p08_clip2a_lite720.mp4"),
    ("clip2b", 4.5, CLIP2B_PROMPT, OUT_DIR / "p08_clip2b_lite720.mp4"),
    ("clip3",  3.0, CLIP3_PROMPT,  OUT_DIR / "p08_clip3_lite720.mp4"),
    ("clip4",  6.0, CLIP4_PROMPT,  OUT_DIR / "p08_clip4_lite720.mp4"),
]


def extract_frame(timestamp, dst):
    cmd = ["ffmpeg", "-y", "-ss", str(timestamp), "-i", str(CLIP1),
           "-frames:v", "1", "-q:v", "2", str(dst)]
    subprocess.run(cmd, capture_output=True, text=True, check=True)


def submit_one(slug, ts, prompt, out_path):
    anchor_jpg = ANCHOR_DIR / f"{slug}_anchor_at_{ts}s.jpg"
    print(f"[{slug}] extracting frame at {ts}s", flush=True)
    extract_frame(ts, anchor_jpg)
    print(f"[{slug}] uploading to KIE storage", flush=True)
    url = kie_upload(str(anchor_jpg))
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
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(submit_one, s, ts, p, o): s for s, ts, p, o in CLIPS}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
