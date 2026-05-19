"""Generate 2nd-angle variant per persona so Kling 3.0's element-ref
has the required 2-4 images per element.

Inputs (the picked persona refs):
  reference/reporter_4.png      → reference/reporter_4_alt.png
  reference/interviewee_1.png   → reference/interviewee_1_alt.png

Strategy: gpt-image-2 image-edit, same identity, different camera angle.
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

REF_DIR = Path("outputs/illinois_jdc_news_eltracks/reference")

VARIATIONS = {
    "reporter_4_alt": (
        REF_DIR / "reporter_4.png",
        "Same exact man as in the reference image — preserve face, beard, "
        "hair, skin tone, age, identity perfectly. Change the angle: he is "
        "now turned 3/4 toward camera (instead of strict left-profile). His "
        "full face is visible. He still wears the same unbuttoned black wool "
        "overcoat over the charcoal blazer and white shirt. Holding the same "
        "black handheld stick microphone with the BLANK WHITE square mic-flag "
        "at chest height. Same Chicago L-tracks setting in soft-focus deep "
        "background. Photoreal, visible pores, fine lines, no makeup, no "
        "retouching, no filter. NO on-screen text, NO captions, NO watermarks."
    ),
    "interviewee_1_alt": (
        REF_DIR / "interviewee_1.png",
        "Same exact younger man as in the reference image — preserve face, "
        "freeform twists, taper fade, gold stud earring, chin-strap goatee, "
        "skin tone, age, identity perfectly. Change the angle: head turned "
        "slightly more to the left (toward an unseen interviewer), 3/4 view, "
        "expression slightly more contemplative. Same tan-camel corduroy "
        "trucker jacket with cream sherpa-collar lining over the charcoal-grey "
        "zip hoodie. Same Chicago L-tracks setting in soft-focus deep "
        "background. Photoreal, visible pores, fine lines, no makeup, no "
        "retouching, no filter. NO on-screen text, NO captions, NO watermarks."
    ),
}


def gen(slug, src, prompt):
    out = REF_DIR / f"{slug}.png"
    if out.exists():
        return slug, "exists", str(out)
    print(f"[{slug}] generating from {src.name}...", flush=True)
    r = generate_image(
        prompt=prompt,
        out_path=str(out),
        image_paths=[str(src)],
        size="1024x1536",
        quality="medium",
        n=1,
    )
    if r["status"] != "success":
        return slug, "failed", r["raw"].get("error", "unknown")
    return slug, "success", r["paths"][0]


def main():
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(gen, s, src, p): s for s, (src, p) in VARIATIONS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                _, status, info = f.result()
                print(f"[{s}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
