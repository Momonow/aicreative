"""Women's-Prison vox-pop — street-casual persona references (gpt-image-2 via KIE, 2K 9:16).
1 interviewer (holds mic, silent-on-camera) + 3 distinct respondents.
Explicit per-persona anthropometry to defeat gpt-image-2 mode-collapse.
"""
import os, pathlib, concurrent.futures as cf, requests
from kie_client import generate_gpt_image

OUT = pathlib.Path("outputs/wp_voxpop/reference"); OUT.mkdir(parents=True, exist_ok=True)

REAL = ("Photoreal candid documentary street photo (NOT glamour, NOT fashion, NOT a celebrity "
        "portrait) — an ordinary hard-lived working-class woman who looks like life has been rough "
        "on her, like someone who has done time. Weathered sun-worn skin with visible pores, deep "
        "lines, uneven tone, heavy under-eye shadows, no makeup, no beauty retouching, no filter. "
        "Tired, guarded eyes. Bright natural daylight on a plain urban sidewalk with softly "
        "out-of-focus storefronts behind (no readable signage). Waist-up vox-pop framing, a black "
        "foam-windscreen handheld microphone held into frame from the side toward her. NO tattoos "
        "on the neck.")

PERSONAS = {
 # interviewer already approved — regenerate respondents only (rough, been-to-prison, Black/Latina, ~45)
 "respondent_a": (
   "A Latina woman, about 42, hard-lived and weary. Long oval face, medium-brown skin, sun-worn "
   "and lined, sharp cheekbones, thin lips, dark deep-set eyes with heavy under-eye shadows, "
   "penciled-thin eyebrows, dark hair with grey streaks scraped back into a tight low bun, a small "
   "faded fine-line tattoo on her forearm. Plain worn grey zip hoodie. Guarded, tired, mid-answer "
   "expression. " + REAL),
 "respondent_b": (
   "A Black woman, about 46, heavyset and weathered. Round full face, deep-brown skin with uneven "
   "tone and visible pores, tired puffy eyes, short natural hair with grey at the temples, a small "
   "gold hoop earring, a faded fine-line tattoo on the back of one hand. Plain oversized dark tee "
   "under a worn flannel shirt. Hard, no-nonsense, been-through-it expression. " + REAL),
 "respondent_c": (
   "A Latina woman, about 48, gaunt and hard-lived. Long angular face, olive skin deeply sun-"
   "damaged and creased, hollow cheeks, a faint old scar through one eyebrow, imperfect uneven "
   "teeth, thin lips, dark tired eyes, dark-grey hair loose and slightly unkempt. Plain faded tank "
   "under an open worn cardigan, a small faded tattoo on her forearm. Wary, subdued, weary "
   "expression. " + REAL),
}

def gen(name, prompt):
    print(f"[gen] {name}\n  gpt-image-2 (t2i, 2K, 9:16): {prompt[:110]}...")
    r = generate_gpt_image(prompt, aspect_ratio="9:16", resolution="2K")
    if r.get("status") != "success" or not r.get("urls"):
        return name, None, r
    url = r["urls"][0]
    dst = OUT / f"{name}.png"
    dst.write_bytes(requests.get(url, timeout=120).content)
    return name, str(dst), url

with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for name, path, extra in ex.map(lambda kv: gen(*kv), PERSONAS.items()):
        print(f"[done] {name} -> {path if path else 'FAILED: '+str(extra)[:160]}")
print("ALL DONE")
