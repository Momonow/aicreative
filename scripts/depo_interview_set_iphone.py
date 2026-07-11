#!/usr/bin/env python3
"""Rebuild the interview set with an iPhone-VIDEO aesthetic (not polished photo):
deep focus, flat even exposure, phone-camera color, slight sensor grain, no bokeh.
Room t2i -> composite each real face (survivor right-gaze, doc left-gaze).

Run: .venv/bin/python scripts/depo_interview_set_iphone.py
"""
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, upload_file, download

REF = Path("outputs/depo_interview/reference")
SURV = REF / "survivor_A_twistout.png"
DOC = REF / "doc_B_woman_gray.png"

IPHONE = (
    "Make the whole image look like a candid VERTICAL iPhone VIDEO FRAME grabbed from a phone "
    "recording: shot on an iPhone, DEEP focus with the background also in focus, flat even natural "
    "indoor exposure, realistic smartphone camera color, slight digital sensor grain/noise, mild "
    "phone-camera softness — NOT a professional photo, NO shallow depth of field, NO creamy bokeh, "
    "NO cinematic color grade, no studio lighting. 9:16 vertical."
)

ROOM_PROMPT = (
    "Vertical smartphone video still, shot on an iPhone, of an EMPTY warm home living room set up "
    "for a sit-down interview: one cream-beige upholstered armchair in the center; behind it a warm "
    "beige wall with framed family photographs, a wooden cabinet with books and a small lamp, a "
    "leafy houseplant, and a window with soft daylight. Ordinary natural indoor lighting. NO "
    "people. " + IPHONE
)

SURV_PROMPT = (
    "Place the woman from the FIRST image seated in the cream armchair in the room from the SECOND "
    "image. Keep her EXACT face, gray natural twist-out hair, gray t-shirt and clip-on lav mic — do "
    "NOT change her appearance or clothing. She sits back, turned slightly to look toward the RIGHT "
    "side of the frame (screen-right) at an off-camera interviewer, not into the lens. " + IPHONE
)

DOC_PROMPT = (
    "Place the woman from the FIRST image seated in the cream armchair in the room from the SECOND "
    "image. Keep her EXACT face, short gray hair, thin wire glasses and light chambray shirt — do "
    "NOT change her appearance or clothing. She is the interviewer holding a small notepad, turned "
    "slightly to look toward the LEFT side of the frame (screen-left) at an off-camera subject, not "
    "into the lens, warm attentive expression. " + IPHONE
)


def gen_room():
    out = REF / "bg_room_iph.png"
    if out.exists():
        print(f"[skip] {out}")
        return out
    print("[room] bg_room_iph …")
    res = generate_gpt_image(ROOM_PROMPT, aspect_ratio="9:16", resolution="4K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] room: {res.get('raw')}")
        return None
    download(res["urls"][0], out)
    print(f"[done] {out}")
    return out


def composite(name, face, prompt, room):
    out = REF / f"{name}.png"
    if out.exists():
        print(f"[skip] {out}")
        return
    face_url = upload_file(str(face))
    room_url = upload_file(str(room))
    print(f"[comp] {name} …")
    res = generate_gpt_image(prompt, image_urls=[face_url, room_url], aspect_ratio="9:16", resolution="4K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}")
        return
    download(res["urls"][0], out)
    print(f"[done] {out}")


room = gen_room()
if room:
    jobs = [
        ("surv_iph", SURV, SURV_PROMPT, room),
        ("doc_iph", DOC, DOC_PROMPT, room),
    ]
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        list(ex.map(lambda j: composite(*j), jobs))
print("ALL DONE")
