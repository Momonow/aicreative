"""3 distinct survivor anchors for the 'It Was Never Consent' street-interview series — reverse-shot
(looking screen-LEFT at the interviewer), small podcast mic, courthouse steps, matching the Nice One
set + interviewer. Explicit per-persona anthropometry so gpt-image-2 doesn't mode-collapse to one face.
gpt-image-2 t2i, 2K 9:16.
"""
import pathlib, concurrent.futures as cf, requests
from kie_client import generate_gpt_image

OUT = pathlib.Path("outputs/wp_series2/reference"); OUT.mkdir(parents=True, exist_ok=True)
REAL = ("Photoreal candid documentary photo (NOT glamour, NOT fashion, NOT a celebrity portrait) — "
        "an ordinary weathered real person, plain average features, natural skin with visible pores, "
        "fine lines, uneven tone, no makeup, no beauty retouching, no filter. Overcast natural daylight "
        "outside a courthouse: worn stone steps and columns of a civic government building softly out of "
        "focus behind. Waist-up documentary framing.")
MIC = ("She holds a small black podcast microphone — short black cylindrical handle, round black foam "
       "windscreen ball on top, a tiny blue LED on the handle — up near her mouth. ")
LOOK = ("Looking to HER LEFT at an off-camera interviewer, mid-conversation, serious and candid. ")

SURV = {
 # Latina, ~50, heavyset, round face
 "surv1_maria": ("A Latina woman, about 50, heavyset build, round full face, olive-tan weathered skin, "
   "faint penciled eyebrows, tired dark-brown eyes, dark brown hair with grey streaks pulled into a low "
   "bun, small silver stud earrings, plain maroon top under a grey zip hoodie. " + LOOK + MIC + REAL),
 # Black, ~55, thin/angular
 "surv2_denise": ("A Black woman, about 55, thin angular build, deep-brown skin, sharp cheekbones, short "
   "greying natural locs, a small mole near her lip, thin reading glasses hanging on a beaded chain on "
   "her chest, plain navy blouse under a tan cardigan. " + LOOK + MIC + REAL),
 # White, ~48, gaunt, hard-lived
 "surv3_kathy": ("A white woman, about 48, gaunt hard-lived build, pale freckled lined skin, thin lips, "
   "sandy-grey hair in a messy low ponytail, a small faded tattoo on her forearm, plain olive t-shirt "
   "under a worn denim jacket. " + LOOK + MIC + REAL),
}

def gen(name, prompt):
    r = generate_gpt_image(prompt, aspect_ratio="9:16", resolution="2K")
    if r.get("status") == "success" and r.get("urls"):
        dst = OUT / f"{name}.png"; dst.write_bytes(requests.get(r["urls"][0], timeout=120).content)
        return name, str(dst)
    return name, f"FAIL {str(r.get('raw'))[:120]}"

if __name__ == "__main__":
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for name, res in ex.map(lambda kv: gen(*kv), SURV.items()):
            print(f"[done] {name} -> {res}")
    print("SERIES2 PERSONAS DONE")
