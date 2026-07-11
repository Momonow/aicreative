#!/usr/bin/env python3
"""Shot-reverse-shot coverage: same room, chairs facing each other, so each person's
camera sees the OPPOSITE wall (different backdrop). Both CHEST-UP close-ups.

- Survivor: her existing backdrop (bg_room_iph = family-photo wall), chest-up, screen-RIGHT.
- Doc: NEW reverse-angle backdrop (opposite wall of same room), chest-up, screen-LEFT.

Minimal i2i prompts (NO appearance description — the face image drives likeness). i2i uses
input_urls under the hood (kie_client handles that).

Run: .venv/bin/python scripts/depo_interview_reverse.py
"""
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, upload_file, download

REF = Path("outputs/depo_interview/reference")
SURV = REF / "survivor_A_twistout.png"
DOC = REF / "doc_B_woman_gray.png"
SURV_ROOM = REF / "bg_room_iph.png"   # survivor's side (family-photo wall)

IPHONE = (
    "candid vertical iPhone video frame, deep focus with the background in focus, flat even "
    "indoor exposure, realistic smartphone color, slight sensor grain, no bokeh, no cinematic "
    "grade. 9:16 vertical."
)

# Reverse-angle backdrop: opposite wall of the SAME warm home, empty, one cream armchair.
REVERSE_ROOM_PROMPT = (
    "Empty warm home living room, the reverse-angle side of the room opposite a family-photo "
    "wall: one cream fabric armchair facing the camera; behind it a tall wooden bookshelf full "
    "of books, a framed landscape painting on a warm beige wall, a window with soft warm "
    "daylight, and a leafy houseplant. Same cozy warm beige palette and wood tones as a family "
    "living room. NO people. " + IPHONE
)

SURV_PROMPT = (
    "Put the woman from the first image into the room from the second image, sitting in the "
    "cream armchair. Tight CHEST-UP close-up: her head and chest fill the frame, do not show her "
    "arms, hands or lap. She looks toward the RIGHT edge of the frame at someone off-camera, not "
    "into the lens. Keep the second image's exact camera look. " + IPHONE
)
DOC_PROMPT = (
    "Put the woman from the first image into the room from the second image, sitting in the "
    "cream armchair. Tight CHEST-UP close-up: her head and chest fill the frame, do not show her "
    "arms, hands or lap. She looks toward the LEFT edge of the frame at someone off-camera, not "
    "into the lens. Keep the second image's exact camera look. " + IPHONE
)


def t2i(name, prompt):
    out = REF / f"{name}.png"
    if out.exists():
        print(f"[skip] {out}"); return out
    print(f"[room] {name} …")
    res = generate_gpt_image(prompt, aspect_ratio="9:16", resolution="2K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}"); return None
    download(res["urls"][0], out); print(f"[done] {out}"); return out


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


# Stage 1: two reverse-angle backdrop options
with cf.ThreadPoolExecutor(max_workers=2) as ex:
    list(ex.map(lambda n: t2i(n, REVERSE_ROOM_PROMPT), ["rev_room_v1", "rev_room_v2"]))

rev = REF / "rev_room_v1.png"
# Stage 2: survivor chest-up (her backdrop) + doc chest-up (reverse backdrop)
jobs = [
    ("surv_cu_v1", SURV, SURV_ROOM, SURV_PROMPT),
    ("surv_cu_v2", SURV, SURV_ROOM, SURV_PROMPT),
    ("doc_rev_v1", DOC, rev, DOC_PROMPT),
    ("doc_rev_v2", DOC, rev, DOC_PROMPT),
]
with cf.ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(lambda j: compose(*j), jobs))
print("ALL DONE")
