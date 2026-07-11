#!/usr/bin/env python3
"""Regenerate the documentarian into the SAME room (bg_room_v1) but looking clearly
SCREEN-LEFT, so she faces the survivor (who looks screen-right). Keeps exact face.

Run: .venv/bin/python scripts/depo_interview_doc_left.py
"""
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, upload_file, download

REF = Path("outputs/depo_interview/reference")
DOC = REF / "doc_B_woman_gray.png"
ROOM = REF / "bg_room_v1.png"

PROMPT = (
    "Place the woman from the FIRST image seated in the cream armchair in the room shown in the "
    "SECOND image. Keep her EXACT face, short gray hair, thin wire glasses and light chambray "
    "button shirt — do NOT change her appearance or clothing. She is the interviewer. Turn her "
    "head and eyes clearly to look toward the LEFT side of the frame (the viewer's left / "
    "screen-left) at an off-camera subject sitting just off the left edge of the frame, with a "
    "warm attentive listening expression. She must NOT look toward the right and must NOT look "
    "into the lens. Match the room's warm window light. Natural candid documentary photo, natural "
    "skin texture, no beauty retouching, no filter, no smile, muted realistic warm color. Medium "
    "chest-up framing. 9:16 vertical."
)


def gen(name):
    out = REF / f"{name}.png"
    if out.exists():
        print(f"[skip] {out}")
        return
    doc_url = upload_file(str(DOC))
    room_url = upload_file(str(ROOM))
    print(f"[gen ] {name} …")
    res = generate_gpt_image(PROMPT, image_urls=[doc_url, room_url], aspect_ratio="9:16", resolution="4K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}")
        return
    download(res["urls"][0], out)
    print(f"[done] {out}")


with cf.ThreadPoolExecutor(max_workers=2) as ex:
    list(ex.map(gen, ["doc_setL_v1", "doc_setL_v2"]))
print("ALL DONE")
