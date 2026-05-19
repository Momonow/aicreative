"""Re-roll clip 4 on KIE Lite 720p with same-tone prompt (not commercial).

Issue: previous clip 4 read as a CTA / ad. Fix: explicit "same quiet tone
as rest of video, NOT commercial, NOT pitching" direction.

Anchor: outputs/illinois_jdc_ugc/anchors_lite720/clip4_anchor_at_6.0s.jpg

Output: outputs/illinois_jdc_ugc/clips/p08_clip4_lite720.mp4 (overwrites)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download
from jdc_ugc_p08_clips234 import CLIP4_PROMPT

ANCHOR = Path("outputs/illinois_jdc_ugc/anchors_lite720/clip4_anchor_at_6.0s.jpg")
OUT = Path("outputs/illinois_jdc_ugc/clips/p08_clip4_lite720.mp4")

print(f"Uploading anchor to KIE storage: {ANCHOR.name}", flush=True)
url = kie_upload(str(ANCHOR))
print(f"url: {url}", flush=True)
print(f"Prompt length: {len(CLIP4_PROMPT)} chars", flush=True)
print(f"Submitting KIE Veo 3.1 Lite 720p…", flush=True)
r = kie_generate_veo(
    prompt=CLIP4_PROMPT,
    aspect_ratio="9:16",
    image_urls=[url, url],
    mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
    model="veo3_lite",
    resolution="720p",
)
if r["status"] != "success" or not r.get("urls"):
    print(f"FAILED: {str(r.get('raw'))[:500]}", flush=True)
else:
    print(f"Downloading: {r['urls'][0]}", flush=True)
    kie_download(r["urls"][0], str(OUT))
    print(f"DONE → {OUT}", flush=True)
