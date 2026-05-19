"""MAXIMALLY SAFE prompt — to test if Veo failures are moderation-related.

Strips out EVERYTHING potentially sensitive:
- No skin tone / race / age / character demographics
- No location specifics (Chicago, Illinois, Loop, juvenile detention)
- No serious topic (no abuse, guard, lawsuit, compensation, "I didn't know")
- Generic person, generic greeting, generic urban setting

If THIS passes → original prompt is hitting Veo moderation, soften.
If THIS fails → infrastructure / capacity issue, retry later.

Tries both anchors (reporter + interviewee) so we know if face/identity
matters too. Submitted on Poyo Veo 3.1 Fast (working provider).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import generate_veo as poyo_generate_veo, download as poyo_download, upload_file as poyo_upload

OUT = Path("outputs/illinois_jdc_news_eltracks/safe_test")
OUT.mkdir(parents=True, exist_ok=True)

SAFE_PROMPT = """\
A person stands outside on a downtown sidewalk in the afternoon. Tight
head-and-shoulders portrait, framed from mid-chest up. The person speaks
clearly and audibly, looking slightly off-camera. Documentary handheld
camera, eye-level, locked frame with very subtle breathing-only float.
NO cuts, NO zoom, NO sudden movement. Photoreal natural daylight.

The person speaks one short greeting line then pauses naturally.

SPOKEN DIALOGUE (verbatim, stop after final word):
"Hello, it's a beautiful afternoon downtown today."

NO on-screen text, NO captions, NO watermarks.
"""


def submit_one(label, anchor_path, out_path):
    print(f"\n=== {label} ===", flush=True)
    print(f"Uploading to Poyo storage: {anchor_path.name}…", flush=True)
    url = poyo_upload(str(anchor_path))
    print(f"  url: {url}", flush=True)
    print(f"Prompt length: {len(SAFE_PROMPT)} chars", flush=True)
    print(f"Submitting Poyo Veo 3.1 Fast…", flush=True)
    r = poyo_generate_veo(
        prompt=SAFE_PROMPT,
        image_urls=[url, url],
        aspect_ratio="9:16",
        resolution="720p",
        generation_type="frame",
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"FAILED: {str(r.get('raw'))[:400]}", flush=True)
        return False
    print(f"Downloading: {r['urls'][0]}", flush=True)
    poyo_download(r["urls"][0], str(out_path))
    print(f"DONE → {out_path}", flush=True)
    return True


def main():
    # Reporter anchor first
    ok = submit_one(
        "SAFE / REPORTER ANCHOR",
        Path("outputs/illinois_jdc_news_eltracks/wide/reporter_nomic.png"),
        OUT / "safe_reporter.mp4",
    )
    if not ok:
        print("\nFirst safe submit failed — likely infra/capacity. Stopping.")
        return
    print("\n=== Sleep 30s ===")
    time.sleep(30)
    submit_one(
        "SAFE / INTERVIEWEE ANCHOR",
        Path("outputs/illinois_jdc_news_eltracks/wide/interviewee_nomic.png"),
        OUT / "safe_interviewee.mp4",
    )


if __name__ == "__main__":
    main()
