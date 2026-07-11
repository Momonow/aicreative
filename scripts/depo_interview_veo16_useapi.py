#!/usr/bin/env python3
"""Same 4 first-16s clips but on the FREE useapi google-flow tier (Veo 3.1 Lite, $0).
Reuses the exact prompts/anchors from depo_interview_veo16.py. Output -> clips_useapi/.
Slow ultra-low-priority queue; skip-if-exists so re-runs resume.
"""
import concurrent.futures as cf, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import googleflow_client as gf
from depo_interview_veo16 import CLIPS  # reuse anchors + prompts

OUT = Path("outputs/depo_interview/clips_useapi"); OUT.mkdir(parents=True, exist_ok=True)

def gen(name):
    out = OUT / f"{name}.mp4"
    if out.exists(): print(f"[skip] {out}"); return
    anchor, prompt = CLIPS[name]
    print(f"[gen ] {name} (anchor {anchor.name}) — free google-flow queue")
    res = gf.generate_veo(prompt, image_path=str(anchor), duration=8, aspect_ratio="portrait")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {str(res.get('raw'))[:160]}"); return
    gf.download(res["urls"][0], out); print(f"[done] {out}")

with cf.ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(gen, CLIPS.keys()))
print("ALL DONE")
