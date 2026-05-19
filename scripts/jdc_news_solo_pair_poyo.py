"""Regen both solo clips on POYO Veo 3.1 Fast w/ Poyo's own storage host.

KIE Fast has been hitting consistent 500 Internal Errors. Switching to Poyo:
  - Upload via api.poyo.ai/common/upload/stream (storage.poyo.ai URL)
  - Generate via api.poyo.ai/generate/submit (veo3.1-fast model)
  - $0.10/clip flat (cheaper than KIE Fast)
  - Same model under the hood, different infra
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import generate_veo as poyo_generate_veo, download as poyo_download, upload_file as poyo_upload
from jdc_news_solo_pair_nomic import REPORTER_PROMPT, INTERVIEWEE_PROMPT, REPORTER_ANCHOR, INTERVIEWEE_ANCHOR

OUT = Path("outputs/illinois_jdc_news_eltracks/solo")
OUT.mkdir(parents=True, exist_ok=True)


def submit_one(label, anchor_path, prompt, out_path):
    print(f"\n=== {label} ===", flush=True)
    print(f"Uploading anchor to Poyo storage: {anchor_path.name}…", flush=True)
    url = poyo_upload(str(anchor_path))
    print(f"  poyo: {url}", flush=True)
    print(f"Prompt length: {len(prompt)} chars", flush=True)
    print(f"Submitting to Poyo Veo 3.1 Fast (720p, frame mode)…", flush=True)
    r = poyo_generate_veo(
        prompt=prompt,
        image_urls=[url, url],
        aspect_ratio="9:16",
        resolution="720p",
        generation_type="frame",
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"FAILED: {str(r.get('raw'))[:500]}", flush=True)
        return False
    print(f"Downloading: {r['urls'][0]}", flush=True)
    poyo_download(r["urls"][0], str(out_path))
    print(f"DONE → {out_path}", flush=True)
    return True


def main():
    ok = submit_one("REPORTER (no-mic, audio-v2)", REPORTER_ANCHOR, REPORTER_PROMPT,
                    OUT / "reporter_audio_v2_poyo.mp4")
    if not ok:
        print("Reporter failed — stopping.")
        return
    print("\n=== Sleep 30s before interviewee ===")
    time.sleep(30)
    submit_one("INTERVIEWEE (no-mic, audio-v2)", INTERVIEWEE_ANCHOR, INTERVIEWEE_PROMPT,
               OUT / "interviewee_audio_v2_poyo.mp4")


if __name__ == "__main__":
    main()
