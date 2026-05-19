"""Step 1: regenerate CLIP 1 only on KIE Veo 3.1 Lite at 720p.

Once landed, run jdc_ugc_p08_others_from_clip1.py to extract fresh anchors
from this new clip 1 and generate clips 2a/2b/3/4.

Anchor: persona_08_chicago_bus_stop.png (original persona ref)
Output: outputs/illinois_jdc_ugc/clips/p08_clip1_lite720.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download
from jdc_ugc_p08_clip1 import PROMPT

ANCHOR = Path("outputs/illinois_jdc_ugc/personas/persona_08_chicago_bus_stop.png")
OUT = Path("outputs/illinois_jdc_ugc/clips/p08_clip1_lite720.mp4")

print(f"Uploading to KIE storage: {ANCHOR.name}", flush=True)
url = kie_upload(str(ANCHOR))
print(f"url: {url}", flush=True)
print(f"Prompt length: {len(PROMPT)} chars", flush=True)
print(f"Submitting KIE Veo 3.1 Lite 720p…", flush=True)
r = kie_generate_veo(
    prompt=PROMPT,
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
