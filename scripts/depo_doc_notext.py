#!/usr/bin/env python3
"""Text-free reverse backdrop -> composite doc looking RIGHT -> flip to clean screen-LEFT
(no backwards text, since the backdrop has no readable letters). Chest-up 3/4, iPhone look.
"""
import concurrent.futures as cf, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, upload_file, download
REF = Path("outputs/depo_interview/reference")
DOC = REF / "doc_B_woman_gray.png"
IPHONE = ("candid vertical iPhone video frame, deep focus, flat even indoor exposure, realistic "
    "smartphone color, slight sensor grain, no bokeh, no cinematic grade. 9:16 vertical.")
ROOM_PROMPT = ("Empty warm home living room, reverse-angle side opposite a family-photo wall: one "
    "cream fabric armchair facing camera; behind it a tall wooden bookshelf full of books whose "
    "spines are PLAIN and softly BLURRED with NO readable titles, a framed soft landscape "
    "painting, a window with warm daylight, a leafy houseplant. Warm beige walls, wood tones, "
    "cozy. Absolutely NO readable text or letters anywhere in the frame. NO people. " + IPHONE)
DOC_PROMPT = ("Put the woman from the first image into the room from the second image, sitting in "
    "the cream armchair. Tight CHEST-UP close-up, podcast/documentary 3/4 angle: she looks toward "
    "the RIGHT side of the frame at someone off the right edge, relaxed conversational gaze angled "
    "right, not dead into the lens, not full profile. Keep second image's camera look. " + IPHONE)

def t2i(name):
    out = REF / f"{name}.png"
    if out.exists(): return out
    res = generate_gpt_image(ROOM_PROMPT, aspect_ratio="9:16", resolution="2K")
    if res.get("status") == "success" and res.get("urls"):
        download(res["urls"][0], out); print(f"[room] {out}"); return out
    print(f"[FAIL room] {res.get('raw')}"); return None

def comp_and_flip(name, room):
    out = REF / f"{name}.png"; flip = REF / f"{name}_L.png"
    if flip.exists(): print(f"[skip] {flip}"); return
    fu, ru = upload_file(str(DOC)), upload_file(str(room))
    res = generate_gpt_image(DOC_PROMPT, image_urls=[fu, ru], aspect_ratio="9:16", resolution="2K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}"); return
    download(res["urls"][0], out)
    Image.open(out).transpose(Image.FLIP_LEFT_RIGHT).save(flip)
    print(f"[done] {flip} (flipped -> screen-left)")

room = t2i("rev_room_notext")
if room:
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        list(ex.map(lambda n: comp_and_flip(n, room), ["doc_nt_v1", "doc_nt_v2"]))
print("ALL DONE")
