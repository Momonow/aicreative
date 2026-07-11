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

BASE = ("Combine these two women into ONE candid documentary street-interview photo, wide 16:9 "
        "horizontal framing, sunny urban sidewalk, natural daylight, softly out-of-focus "
        "storefronts behind. The FIRST image is the interviewer (light-blue denim jacket, holding "
        "a black foam microphone). The SECOND image is the woman being interviewed (grey hoodie, "
        "dark hair in a low bun, weathered face). Keep each woman's EXACT face, skin tone, hair and "
        "clothing — do not beautify or change their identity. Photoreal, real skin texture, no "
        "makeup, no beauty retouching, no filter. No on-screen text, no captions.")

VARIANTS = {
 "v1_ots": BASE + " Over-the-shoulder: the interviewer stands at the LEFT edge seen from behind at "
   "a three-quarter angle (back and shoulder to camera), extending the mic toward the other woman "
   "on the RIGHT, who faces toward camera mid-answer. She is the main subject.",
 "v2_profile": BASE + " Balanced two-shot: interviewer on the LEFT in three-quarter profile facing "
   "right, the woman on the RIGHT in three-quarter profile facing left, the microphone held "
   "between them near center. Both faces clearly visible so either can be the focus.",
 "v3_foreground": BASE + " The interviewer's shoulder, arm and the microphone are in soft "
   "foreground at the LEFT, the interviewed woman is centered and sharp, facing the mic, waist-up.",
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
