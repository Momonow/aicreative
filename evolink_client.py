"""EvoLink.AI client — Veo 3.1 Fast.

Endpoint: POST https://api.evolink.ai/v1/videos/generations
Polling:  GET  https://api.evolink.ai/v1/tasks/{task_id}
Auth:     Bearer sk-...

Models:
  veo-3.1-fast-generate-preview  — Veo 3.1 Fast (4/6/8s, T2V + I2V first-frame)
  veo-3.1-pro-beta               — Veo 3.1 Pro (T2V + first-AND-last-frame I2V)
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("EVOLINK_API_KEY")
if not KEY:
    raise RuntimeError("EVOLINK_API_KEY not set in .env")

BASE = "https://api.evolink.ai"
HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def generate_veo(
    prompt,
    image_urls=None,
    model="veo-3.1-fast-generate-preview",
    aspect_ratio="9:16",
    resolution="720p",
    duration=8,
    generation_type=None,
    generate_audio=True,
    seed=None,
):
    """Submit Veo generation, poll until done, return {status, urls, raw}."""
    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "quality": resolution,
        "duration": duration,
        "generate_audio": generate_audio,
    }
    if image_urls:
        payload["image_urls"] = image_urls
    if generation_type:
        payload["generation_type"] = generation_type
    if seed is not None:
        payload["seed"] = seed

    r = requests.post(f"{BASE}/v1/videos/generations", headers=HEADERS, json=payload, timeout=60)
    body = r.json()
    task_id = body.get("id")
    if not task_id:
        return {"status": "failed", "urls": [], "raw": body}
    print(f"  EvoLink taskId: {task_id}", flush=True)

    return _poll(task_id)


def _poll(task_id, interval=8, timeout=900):
    start = time.time()
    while True:
        time.sleep(interval)
        if time.time() - start > timeout:
            return {"status": "failed", "urls": [], "raw": {"error": "poll timeout"}}
        r = requests.get(f"{BASE}/v1/tasks/{task_id}", headers=HEADERS, timeout=30)
        d = r.json()
        status = d.get("status")
        progress = d.get("progress", 0)
        print(f"  {time.strftime('%H:%M:%S')} EvoLink: {status} ({progress}%)", flush=True)
        if status == "completed":
            urls = d.get("results", [])
            return {"status": "success", "urls": urls, "raw": d}
        if status == "failed":
            return {"status": "failed", "urls": [], "raw": d}


def download(url, dest):
    from pathlib import Path
    r = requests.get(url, stream=True)
    r.raise_for_status()
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 16):
            f.write(chunk)
    print(f"  Saved: {dest} ({os.path.getsize(dest) // 1024}KB)", flush=True)
    return dest
