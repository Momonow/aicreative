"""Generate 10 Black male UGC persona refs in Chicago via gpt-image-2.

For IL JDC sexual abuse compensation campaign. Young men in their late teens
to early 20s — old enough to have aged out of juvenile detention recently
enough that the lawsuit window applies, young enough to feel "current."

UGC selfie / handheld-doc framing — 9:16 portrait, photoreal, real Chicago
neighborhoods + natural daylight. NOT studio, NOT polished. Each persona
varies by age, neighborhood, wardrobe, hair, accessories, energy.

Output: outputs/illinois_jdc_ugc/personas/persona_{01..10}.png (1024x1536)
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

OUT_DIR = Path("outputs/illinois_jdc_ugc/personas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COMMON = (
    "Photoreal UGC selfie / handheld-doc portrait, 9:16 vertical mobile-phone "
    "framing, eye-level, head-and-upper-chest framing. Real natural daylight, "
    "NOT studio, NOT cinematic, NOT polished. Visible pores, fine skin texture, "
    "slight asymmetry, no makeup, no beauty mode, no retouching, no filter, "
    "no skin smoothing. Looks like an actual phone selfie or handheld iPhone "
    "video frame. NO on-screen text, NO captions, NO watermarks, NO logos."
)

PROMPTS = {
    "persona_01_southside_porch": (
        "Photoreal portrait of a young Black man, early 20s, sitting on the "
        "concrete front steps of a brick two-flat house in a South Side Chicago "
        "residential neighborhood. He has short freeform twists with a high "
        "temple-fade taper, faint chin-strap goatee, small gold stud earring in "
        "his left ear. Wearing a tan corduroy trucker jacket with cream sherpa "
        "collar over a charcoal-grey zip hoodie. Looking directly at the camera, "
        "calm, reserved expression. Late-afternoon overcast daylight. Background: "
        "out-of-focus brick row houses, parked cars on the residential street. "
        + COMMON
    ),
    "persona_02_westside_alley": (
        "Photoreal portrait of a young Black man, late teens / 19, standing in a "
        "narrow alley between brick buildings on the West Side of Chicago. Short "
        "box braids pulled back, faint mustache stubble. Wearing a black quilted "
        "puffer jacket over a grey hoodie. Looking off-camera-left, contemplative "
        "expression. Cool overcast late-afternoon light. Background: brick walls, "
        "dumpster, soft natural fall-off. " + COMMON
    ),
    "persona_03_downtown_loop_under_el": (
        "Photoreal portrait of a young Black man, early 20s, standing on a "
        "sidewalk under the Chicago Loop elevated train tracks ('the L'). High "
        "temple-fade taper with short waves on top, neat thin goatee, small "
        "silver chain visible at collar. Wearing a navy bomber jacket with "
        "ribbed cuffs over a white tee. Looking directly at camera, serious "
        "attentive expression. Late-afternoon daylight, steel girders of the "
        "L visible overhead in shallow soft-focus. Background: Loop-era brick "
        "buildings + faint yellow taxi at curb. " + COMMON
    ),
    "persona_04_lakeshore_path": (
        "Photoreal portrait of a young Black man, early 20s, on a Chicago "
        "lakeshore pedestrian path, Lake Michigan visible behind him soft-focus. "
        "Short twists, faint chin-strap goatee, gold chain at neck. Wearing a "
        "dark olive military-style canvas jacket over a cream waffle henley. "
        "Looking slightly off-camera-right with a quiet thoughtful expression. "
        "Late afternoon, overcast cool grey-blue light, gentle wind in his hair. "
        + COMMON
    ),
    "persona_05_southside_corner_store": (
        "Photoreal portrait of a young Black man, late teens / 19, standing on "
        "the corner of a South Side Chicago residential block. Plain front of a "
        "small convenience store visible behind him (no signs, no text). Short "
        "low fade with hair on top in tight curls, light beard stubble. Wearing "
        "a heavy grey hoodie under an unzipped black bubble jacket. Hands in "
        "hoodie pocket. Looking at camera, slightly guarded expression. Overcast "
        "afternoon. Soft-focus brick + chain-link fence behind. " + COMMON
    ),
    "persona_06_residential_block_porch": (
        "Photoreal portrait of a young Black man, mid 20s, sitting on the wooden "
        "porch railing of a frame house on a Chicago residential block. Locs "
        "(thick dreadlocks) pulled into a low ponytail, faint goatee. Wearing a "
        "rust-orange knit beanie + cream cable-knit sweater + dark blue jeans. "
        "Looking off-camera at someone unseen, calm reflective expression. "
        "Golden-hour late-afternoon sun softly raking across his face. " + COMMON
    ),
    "persona_07_park_bench_humboldt": (
        "Photoreal portrait of a young Black man, early 20s, sitting on a "
        "concrete park bench in a Chicago neighborhood park (Humboldt Park-style "
        "wide open green space). Bald fade haircut, full short beard, small gold "
        "hoop in left ear. Wearing a dark grey Champion-style hoodie under a "
        "denim trucker jacket. Looking directly at camera, deadpan honest "
        "expression. Cool overcast daylight. Background: bare-branched trees, "
        "soft-focus grass. " + COMMON
    ),
    "persona_08_chicago_bus_stop": (
        "Photoreal portrait of a young Black man, late teens / 19, standing at "
        "a Chicago CTA bus stop. Short freeform twists, faint mustache stubble, "
        "no facial hair beyond. Wearing a faded brown carhartt-style work jacket "
        "over a heather grey crewneck sweatshirt. Backpack strap visible on "
        "shoulder. Looking slightly off-camera-left, thoughtful expression. "
        "Overcast afternoon light. Background: out-of-focus blue bus stop sign + "
        "street with parked cars. " + COMMON
    ),
    "persona_09_chicago_basketball_court": (
        "Photoreal portrait of a young Black man, early 20s, standing on an "
        "outdoor concrete basketball court in a Chicago neighborhood, chain-link "
        "fence behind him soft-focus, faded painted court lines on the ground. "
        "Short twists with a high taper fade, faint goatee. Wearing a grey "
        "hooded sweatshirt with the hood up, gold chain visible at collar. "
        "Looking directly at camera, calm steady expression. Late-afternoon "
        "overcast daylight. " + COMMON
    ),
    "persona_10_chicago_apartment_window": (
        "Photoreal portrait of a young Black man, mid 20s, standing near a "
        "window inside a small Chicago apartment, soft late-afternoon daylight "
        "streaming through the window onto his face. Short fade haircut, full "
        "short beard, neutral plain white tee. Looking directly at camera, "
        "serious quiet expression. Background: out-of-focus interior — "
        "blinds, painted wall, hint of a kitchen counter. Intimate, "
        "documentary-still feel. " + COMMON
    ),
}


def gen(slug, prompt):
    out = OUT_DIR / f"{slug}.png"
    if out.exists():
        return slug, "exists", str(out)
    print(f"[{slug}] generating...", flush=True)
    r = generate_image(
        prompt=prompt,
        out_path=str(out),
        size="1024x1536",
        quality="medium",
        n=1,
    )
    if r["status"] != "success":
        return slug, "failed", r["raw"].get("error", "unknown")
    return slug, "success", r["paths"][0]


def main():
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(gen, s, p): s for s, p in PROMPTS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                _, status, info = f.result()
                print(f"[{s}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
