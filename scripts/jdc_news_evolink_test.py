"""Test EvoLink Veo 3.1 Fast — reporter + interviewee solo pair.

Uses Poyo's storage.poyo.ai URLs (already uploaded, publicly accessible).
EvoLink Veo's fetcher should reach them.

Output:
  outputs/illinois_jdc_news_eltracks/solo/reporter_evolink.mp4
  outputs/illinois_jdc_news_eltracks/solo/interviewee_evolink.mp4
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import upload_file as poyo_upload
from evolink_client import generate_veo as evo_generate_veo, download as evo_download
from jdc_news_solo_pair_nomic import REPORTER_PROMPT, INTERVIEWEE_PROMPT, REPORTER_ANCHOR, INTERVIEWEE_ANCHOR

OUT = Path("outputs/illinois_jdc_news_eltracks/solo")
OUT.mkdir(parents=True, exist_ok=True)


def submit_one(label, anchor_path, prompt, out_path):
    print(f"\n=== {label} ===", flush=True)
    print(f"Uploading anchor to Poyo storage: {anchor_path.name}", flush=True)
    url = poyo_upload(str(anchor_path))
    print(f"  url: {url}", flush=True)
    print(f"Prompt length: {len(prompt)} chars", flush=True)
    print(f"Submitting to EvoLink Veo 3.1 Fast (1080p)...", flush=True)
    r = evo_generate_veo(
        prompt=prompt,
        image_urls=[url],
        aspect_ratio="9:16",
        resolution="1080p",
        duration=8,
        generation_type="FIRST&LAST",
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"FAILED: {str(r.get('raw'))[:500]}", flush=True)
        return False
    print(f"Downloading: {r['urls'][0]}", flush=True)
    evo_download(r["urls"][0], str(out_path))
    print(f"DONE → {out_path}", flush=True)
    return True


def main():
    ok = submit_one("REPORTER EVOLINK", REPORTER_ANCHOR, REPORTER_PROMPT,
                    OUT / "reporter_evolink.mp4")
    if not ok:
        print("\nReporter failed — stopping.")
        return
    print("\n=== Sleep 20s ===")
    time.sleep(20)
    submit_one("INTERVIEWEE EVOLINK", INTERVIEWEE_ANCHOR, INTERVIEWEE_PROMPT,
               OUT / "interviewee_evolink.mp4")


if __name__ == "__main__":
    main()
