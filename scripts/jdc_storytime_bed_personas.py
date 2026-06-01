"""Storytime-confession personas, IN BED selfie style (matches reference media.1780116952093).
Ordinary/relatable survivors in their 30s, lying back in bed filming a front-camera confession.
Mix of women + men so we have anchors across V1 (young woman), V2/V3 (men).
t2i via KIE gpt-image-2, 9:16, 2K. Output: outputs/illinois_jdc_storytime_bed/reference/bed_*.png
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_gpt_image, download as kie_download

OUT = Path("outputs/illinois_jdc_storytime_bed/reference")
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    " Photoreal candid selfie shot on a front-facing phone camera held just above the face at a slight "
    "high angle, the person lying back in bed with their head resting on a pillow against a fabric "
    "headboard, soft cream and white bedding. Tight vertical close-up, the face filling most of the "
    "frame, intimate and unstaged like a real TikTok storytime video. Warm dim bedroom lamp light in "
    "the evening, the room soft and out of focus behind them. NOT a glamour or fashion shoot, NOT a "
    "celebrity portrait — an ordinary, everyday, relatable person with plain average features. Natural "
    "skin with visible pores, blemishes, uneven tone, slight under-eye shadows, imperfect teeth, no "
    "makeup, no beauty retouching, no filter, no skin smoothing. Calm, vulnerable, reflective "
    "expression, eyes open looking softly toward the phone. Shallow depth of field. 9:16 vertical. "
    "NO on-screen text, NO captions, NO watermarks."
)

PERSONAS = [
    ("bed_f1", "A woman, age 31, with slightly messy wavy shoulder-length blonde hair, fair skin and "
     "faint freckles, wearing a cozy cream cable-knit sweater. Tired and emotionally open."),
    ("bed_f2", "A Latina woman, age 35, dark brown hair loosely tied back with a few strands loose, "
     "plain heather-grey long-sleeve top. Quiet and reflective, a little guarded."),
    ("bed_f3", "A woman, age 38, short auburn hair, slightly fuller face, plain navy crew-neck "
     "t-shirt. Weary, heavy eyes, on the edge of tears but composed."),
    ("bed_m1", "A Black man, age 33, short fade with light stubble, wearing a plain charcoal hoodie "
     "with the hood down. Somber and guarded, looking down slightly then up."),
    ("bed_m2", "A white man, age 36, buzzcut with a short beard flecked with grey, wearing a plain "
     "olive t-shirt. Heavy and reflective, carrying something he buried a long time."),
    ("bed_m3", "A Latino man, age 30, short dark curls and light stubble, wearing a plain "
     "heather-grey crew-neck sweatshirt. Uneasy and vulnerable, hesitant."),
    # --- Black men, late 20s + mid 30s (storytime-confession anchors) ---
    ("bed_b1", "A Black man, age 28, short fade with light stubble, wearing a plain black "
     "t-shirt. Vulnerable and open, eyes a little glassy."),
    ("bed_b2", "A Black man, age 27, short twists and a thin patchy beard, wearing a grey "
     "hoodie with the hood down. Uneasy and hesitant, on guard."),
    ("bed_b3", "A Black man, age 29, short afro and clean-shaven with a small gap in his "
     "front teeth, wearing a plain heather-grey t-shirt. Quiet and nervous, sincere."),
    ("bed_b4", "A Black man, age 35, short hair with a slightly receding hairline and a full "
     "beard flecked with grey, wearing a plain dark flannel shirt. Weathered and heavy, tired eyes."),
    ("bed_b5", "A Black man, age 34, bald with light stubble, a bit heavyset, wearing a "
     "charcoal hoodie. Quiet and reflective, looking down then up."),
    ("bed_b6", "A Black man, age 36, shoulder-length locs tied back with some grey and a short "
     "beard, wearing a dark hoodie. Somber and grounded, carrying something old."),
    # --- 10 more in the b1/b2/b5 direction (ordinary, real, vulnerable; fades/twists/bald, hoodies+tees) ---
    ("bed_b7", "A Black man, age 29, short fade with a crisp line-up and a thin mustache, medium-brown "
     "skin, wearing a plain white t-shirt. Tired and vulnerable, eyes a little glassy."),
    ("bed_b8", "A Black man, age 31, bald with a full short beard, deep-brown skin, average build, "
     "wearing a black hoodie with the hood down. Heavy and weathered, weary eyes."),
    ("bed_b9", "A Black man, age 27, short twists and clean-shaven, a bit heavyset with round cheeks, "
     "wearing a heather-grey hoodie. Nervous and hesitant, looking down then up."),
    ("bed_b10", "A Black man, age 33, short 360 waves and a neat goatee, medium-brown skin, wearing a "
     "plain navy t-shirt. Somber and quiet, every word costing him something."),
    ("bed_b11", "A Black man, age 28, a high-top short afro and light stubble, lean face, wearing a "
     "dark green hoodie. Guarded and uneasy, jaw tight."),
    ("bed_b12", "A Black man, age 35, bald with a beard flecked with grey, deep-brown skin, wearing a "
     "plain charcoal t-shirt. Reflective and worn down, on the edge of tears but holding it."),
    ("bed_b13", "A Black man, age 30, cornrows braided straight back and a thin beard, wearing a black "
     "hoodie. Uneasy and vulnerable, swallowing hard."),
    ("bed_b14", "A Black man, age 27, short fade with a chin-strap beard, medium-brown skin, lean, "
     "wearing a plain grey t-shirt. Glassy-eyed and raw, voice about to crack."),
    ("bed_b15", "A Black man, age 36, short hair with a slightly receding hairline and a full beard, "
     "wearing a plain dark flannel shirt over a tee. Weary and grounded, heavy tired eyes."),
    ("bed_b16", "A Black man, age 32, low bald fade going thin on top with a mustache and soul patch, "
     "average build, wearing a plain black t-shirt. Quiet and contained, distant look."),
]


def gen(slug, desc):
    dst = OUT / f"{slug}.png"
    if dst.exists() and dst.stat().st_size > 50000:
        return slug, "cached", str(dst)
    full = desc + STYLE
    print(f"[{slug}] submit ({len(full)} chars)", flush=True)
    r = generate_gpt_image(prompt=full, aspect_ratio="9:16", resolution="2K")
    if r["status"] != "success" or not r.get("urls"):
        return slug, "FAILED", str(r.get("raw"))[:300]
    kie_download(r["urls"][0], str(dst))
    return slug, "success", str(dst)


def main():
    only = sys.argv[1:]
    items = [(s, d) for s, d in PERSONAS if not only or s in only]
    with ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(gen, s, d): s for s, d in items}
        for f in as_completed(futs):
            slug, status, info = f.result()
            print(f"[{slug}] {status}: {info}", flush=True)


if __name__ == "__main__":
    main()
