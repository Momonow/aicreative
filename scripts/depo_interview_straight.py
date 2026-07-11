#!/usr/bin/env python3
"""Front-on talking-head coverage: both speakers CHEST-UP, looking nearly straight into the
lens (natural interview eyeline beside the camera), NOT turned to the side. Same room,
opposite-wall backdrops. Minimal i2i prompts (no appearance description; i2i via input_urls).

Run: .venv/bin/python scripts/depo_interview_straight.py
"""
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, upload_file, download

REF = Path("outputs/depo_interview/reference")
SURV = REF / "survivor_A_twistout.png"
DOC = REF / "doc_B_woman_gray.png"
SURV_ROOM = REF / "bg_room_iph.png"   # family-photo wall
DOC_ROOM = REF / "rev_room_v1.png"    # opposite wall (bookshelf/window)

IPHONE = (
    "candid vertical iPhone video frame, deep focus with the background in focus, flat even "
    "indoor exposure, realistic smartphone color, slight sensor grain, no bokeh, no cinematic "
    "grade. 9:16 vertical."
)

STRAIGHT = (
    "Tight CHEST-UP close-up: head and chest fill the frame, no arms, hands or lap visible. "
    "The camera is straight in front of her and she looks nearly straight INTO the lens (natural "
    "interview eyeline, as if talking to an interviewer right beside the camera) — face front-on, "
    "NOT turned to the side, NOT in profile. Keep the second image's exact camera look. "
)

SURV_PROMPT = "Put the woman from the first image into the room from the second image, sitting in the cream armchair. " + STRAIGHT + IPHONE
DOC_PROMPT = "Put the woman from the first image into the room from the second image, sitting in the cream armchair. " + STRAIGHT + IPHONE


def compose(name, face, room, prompt):
    out = REF / f"{name}.png"
    if out.exists():
        print(f"[skip] {out}"); return
    face_url = upload_file(str(face)); room_url = upload_file(str(room))
    print(f"[comp] {name} …")
    res = generate_gpt_image(prompt, image_urls=[face_url, room_url], aspect_ratio="9:16", resolution="2K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}"); return
    download(res["urls"][0], out); print(f"[done] {out}")


jobs = [
    ("surv_str_v1", SURV, SURV_ROOM, SURV_PROMPT),
    ("surv_str_v2", SURV, SURV_ROOM, SURV_PROMPT),
    ("doc_str_v1", DOC, DOC_ROOM, DOC_PROMPT),
    ("doc_str_v2", DOC, DOC_ROOM, DOC_PROMPT),
]
with cf.ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(lambda j: compose(*j), jobs))
print("ALL DONE")
