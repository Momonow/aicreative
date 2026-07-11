#!/usr/bin/env python3
"""Re-anchor survivor A + documentarian B into ONE shared interview room (matched light)
so the stacked two-shot reads as the same space. i2i on the picked faces (KIE gpt-image-2).

Survivor gaze = camera-RIGHT; documentarian gaze = camera-LEFT (they 'face' across the stack).
Run: .venv/bin/python scripts/depo_interview_room_anchors.py
"""
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, upload_file, download

REF = Path("outputs/depo_interview/reference")
OUT = REF
SURV_SRC = REF / "survivor_A_twistout.png"
DOC_SRC = REF / "doc_B_woman_gray.png"

ROOM = (
    "a warm, lived-in home living room set up for a sit-down documentary interview: soft warm "
    "daylight coming from a window to camera-left, background softly out of focus showing a "
    "wooden cabinet, framed family photographs on a beige wall and a leafy houseplant, cozy "
    "muted warm earth tones"
)
REAL = (
    "Natural real skin texture with visible pores and fine lines, no beauty retouching, no "
    "filter, no smile. Documentary camera, shallow depth of field, muted realistic warm color. "
    "Medium chest-up framing. 9:16 vertical."
)

SURV_PROMPT = (
    "Edit this photo. Keep this EXACT woman — identical face, identical short natural twist-out "
    "hair with a little gray, same age, same features, same deep-brown skin, same small lav mic. "
    f"Place her seated for a documentary interview in {ROOM}. Her body is angled so she looks "
    "slightly to camera-RIGHT at an off-camera interviewer (NOT into the lens). Tired eyes, plain "
    f"everyday look. {REAL}"
)
DOC_PROMPT = (
    "Edit this photo. Keep this EXACT woman — identical face, identical short gray hair, identical "
    "thin glasses, identical light chambray button shirt, same age. Place her seated across the "
    f"same interview in {ROOM} (reverse camera angle, SAME room and SAME warm window light). Her "
    "body is angled so she looks slightly to camera-LEFT toward the subject, warm attentive "
    f"listening expression (NOT into the lens). {REAL}"
)

JOBS = [
    ("survivor_room_v1", SURV_SRC, SURV_PROMPT),
    ("survivor_room_v2", SURV_SRC, SURV_PROMPT),
    ("doc_room_v1", DOC_SRC, DOC_PROMPT),
    ("doc_room_v2", DOC_SRC, DOC_PROMPT),
]


def gen(name, src, prompt):
    out = OUT / f"{name}.png"
    if out.exists():
        print(f"[skip] {out}")
        return
    url = upload_file(str(src))
    print(f"[gen ] {name} (i2i from {src.name}) …")
    res = generate_gpt_image(prompt, image_urls=[url], aspect_ratio="9:16", resolution="2K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}")
        return
    download(res["urls"][0], out)
    print(f"[done] {out}")


with cf.ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(lambda j: gen(*j), JOBS))
print("ALL DONE")
