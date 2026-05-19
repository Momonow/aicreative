"""Re-roll JUST the interviewee no-mic test (reporter already passed).

Same prompt + anchor. Will retry on transient 500 errors up to 3 times.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_catbox, generate_veo as kie_generate_veo, download as kie_download
from jdc_news_solo_pair_nomic import INTERVIEWEE_PROMPT, INTERVIEWEE_ANCHOR

OUT = Path("outputs/illinois_jdc_news_eltracks/solo/interviewee_nomic_test.mp4")

print(f"Uploading anchor: {INTERVIEWEE_ANCHOR.name}", flush=True)
url = upload_catbox(str(INTERVIEWEE_ANCHOR))
print(f"  catbox: {url}", flush=True)

for attempt in range(1, 4):
    print(f"\n=== Attempt {attempt} (Veo 3.1 Fast 1080p) ===", flush=True)
    r = kie_generate_veo(
        prompt=INTERVIEWEE_PROMPT,
        aspect_ratio="9:16",
        image_urls=[url, url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_fast",
        resolution="1080p",
    )
    if r["status"] == "success" and r.get("urls"):
        print(f"DOWNLOADING: {r['urls'][0]}", flush=True)
        kie_download(r["urls"][0], str(OUT))
        print(f"DONE → {OUT}", flush=True)
        break
    err = str(r.get("raw"))[:400]
    print(f"FAIL attempt {attempt}: {err}", flush=True)
    if attempt < 3:
        print(f"Sleeping 30s before next attempt…", flush=True)
        time.sleep(30)
