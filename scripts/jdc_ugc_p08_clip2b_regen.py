"""Re-roll clip 2b on KIE Lite 720p with stronger energy-gradient prompt.

Issue: previous 2b had abrupt energy shift from quiet 2a → too informational.
Fix: explicit gradient direction in prompt — START quiet (matching 2a end),
LIFT GRADUALLY over duration, END slightly more informational (but still
quiet) to bridge into clip 3's practical tone.

Anchor: outputs/illinois_jdc_ugc/anchors_lite720/clip2b_anchor_at_4.5s.jpg
        (same one used in previous gen — fresh frame from new clip 1)

Output: outputs/illinois_jdc_ugc/clips/p08_clip2b_lite720.mp4 (overwrites)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download
from jdc_ugc_p08_clip2_split import CLIP2B_PROMPT

ANCHOR = Path("outputs/illinois_jdc_ugc/anchors_lite720/clip2b_anchor_at_4.5s.jpg")
OUT = Path("outputs/illinois_jdc_ugc/clips/p08_clip2b_lite720.mp4")

print(f"Uploading anchor to KIE storage: {ANCHOR.name}", flush=True)
url = kie_upload(str(ANCHOR))
print(f"url: {url}", flush=True)
print(f"Prompt length: {len(CLIP2B_PROMPT)} chars", flush=True)
print(f"Submitting KIE Veo 3.1 Lite 720p…", flush=True)
r = kie_generate_veo(
    prompt=CLIP2B_PROMPT,
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
