#!/usr/bin/env python3
"""Silent listening clips on Grok Imagine (KIE) — the ONLY model that keeps the mouth closed
with natural motion (Veo always talks). 10s each so we can trim to any beat with no looping.
"""
import sys, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie
REF=Path("outputs/depo_interview/reference"); OUT=Path("outputs/depo_interview/clips_grok"); OUT.mkdir(parents=True,exist_ok=True)
def prompt(side):
    return (f"The woman sits calmly in the armchair, listening quietly to someone off to her {side}. "
        "She nods gently now and then, blinks naturally, makes small attentive head movements, and "
        "keeps a warm, empathetic expression. She stays quiet with her lips closed. Calm and still. "
        "Faint room ambience.")
JOBS=[("doc_listen_grok_1",REF/"doc_alone_v1_L.png","left"),
      ("doc_listen_grok_2",REF/"doc_alone_v1_L.png","left"),
      ("surv_listen_grok_1",REF/"surv_face_v1.png","right"),
      ("surv_listen_grok_2",REF/"surv_face_v1.png","right")]
def gen(name, anchor, side):
    out=OUT/f"{name}.mp4"
    if out.exists(): print("skip",name); return
    url=kie.upload_file(str(anchor))
    payload={"model":"grok-imagine/image-to-video","input":{"image_urls":[url],"prompt":prompt(side),
             "mode":"normal","duration":"10","resolution":"720p","aspect_ratio":"9:16"}}
    r=requests.post(kie.JOBS_CREATE, headers=kie.HEADERS, json=payload)
    tid=(r.json().get("data") or {}).get("taskId")
    if not tid: print("FAIL create",name,r.json()); return
    res=kie._poll_jobs(tid,"Grok")
    if res.get("status")=="success" and res.get("urls"):
        kie.download(res["urls"][0],out); print("done",name)
    else: print("FAIL",name,str(res.get("raw"))[:160])
for j in JOBS: gen(*j)
print("ALL DONE")
