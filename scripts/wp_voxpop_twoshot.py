"""Vox-pop two-shot composite anchor — merge interviewer + respondent A into ONE
wide 16:9 street-interview frame via gpt-image-2 image-edit (KIE). Render 3 framings.
That composite becomes the Veo anchor; punch-in to the active speaker in post.
"""
import pathlib, concurrent.futures as cf, requests
from kie_client import generate_gpt_image, upload_file

REF = pathlib.Path("outputs/wp_voxpop/reference")
OUT = pathlib.Path("outputs/wp_voxpop/twoshot"); OUT.mkdir(parents=True, exist_ok=True)

print("[upload] interviewer + respondent_a to KIE ...")
iv = upload_file(str(REF / "interviewer.png"))
ra = upload_file(str(REF / "respondent_a.png"))

# MINIMAL prompt — describe ONLY the scene/composition, NOT the people (per input_urls i2i rule).
# Describing appearance fights the reference faces and drifts identity.
BASE = ("Put these two exact people together in ONE candid documentary street-interview photo, "
        "wide 16:9 horizontal framing on a sunny sidewalk. FIRST person = the interviewer holding "
        "the microphone. SECOND person = the woman being interviewed. No on-screen text.")

VARIANTS = {
 "v1_ots": BASE + " Over-the-shoulder: the interviewer at the LEFT edge seen from behind (back and "
   "shoulder to camera), extending the mic toward the second woman on the RIGHT, who faces camera "
   "mid-answer as the main subject.",
 "v2_profile": BASE + " Balanced two-shot: interviewer on the LEFT facing right, the second woman "
   "on the RIGHT facing left, microphone between them near center, both faces clearly visible.",
 "v3_foreground": BASE + " The interviewer's shoulder, arm and microphone soft in the LEFT "
   "foreground, the second woman centered and sharp, facing the mic, waist-up.",
}

def gen(name, prompt):
    print(f"[gen] {name} — gpt-image-2 i2i 16:9 2K")
    r = generate_gpt_image(prompt, image_urls=[iv, ra], aspect_ratio="16:9", resolution="2K")
    if r.get("status") != "success" or not r.get("urls"):
        return name, None, r
    dst = OUT / f"{name}.png"
    dst.write_bytes(requests.get(r["urls"][0], timeout=120).content)
    return name, str(dst), None

with cf.ThreadPoolExecutor(max_workers=3) as ex:
    for name, path, err in ex.map(lambda kv: gen(*kv), VARIANTS.items()):
        print(f"[done] {name} -> {path or 'FAIL: '+str(err)[:150]}")
print("ALL DONE")
