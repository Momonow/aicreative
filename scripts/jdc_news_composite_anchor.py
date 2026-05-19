"""Composite reporter_4 + interviewee_1 into one Chicago L-tracks two-shot
(the Veo IMAGE_2_VIDEO scene anchor).

Uses gpt-image-2 image-edit (multi-input) — feeds both persona refs and prompts
gpt-image to merge them into a single 9:16 scene that matches the source ad's
two-shot framing: reporter LEFT-profile mic-forward, interviewee RIGHT 3/4 to camera.

Generates 3 framing variants — user picks the best as the Veo anchor.

Output: outputs/illinois_jdc_news_eltracks/anchor/composite_v{1..3}.png
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

REF_DIR = Path("outputs/illinois_jdc_news_eltracks/reference")
OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/anchor")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORTER = REF_DIR / "reporter_4.png"
INTERVIEWEE = REF_DIR / "interviewee_1.png"

COMMON = (
    "Photoreal news b-roll two-shot photograph, real daylight under the Chicago "
    "Loop elevated train tracks ('the L'). Massive black-painted riveted steel "
    "girders and lattice beams overhead, large steel support columns visible "
    "behind the figures. Polished brick/concrete sidewalk under foot, granite-clad "
    "Loop-era buildings + faint yellow taxi at the curb in the deep background. "
    "Late-afternoon overcast lighting, subtle pattern shadows from the El "
    "structure on the ground. Documentary handheld feel, NOT studio. "
    "Visible pores, fine lines, slight asymmetry on both faces, no makeup, no "
    "beauty mode, no retouching, no filter, no skin smoothing. "
    "Both characters must EXACTLY match the reference faces and wardrobe: "
    "the OLDER MAN (reporter) preserves the black overcoat over charcoal blazer "
    "and white shirt, close-cropped hair, full neat short beard, medium-dark "
    "skin tone, and his black handheld stick microphone with a WHITE square "
    "mic-flag. The YOUNGER MAN (interviewee) preserves the short freeform "
    "twists with high temple-fade taper, gold stud earring in his left ear, "
    "tan-camel corduroy trucker jacket with cream sherpa-collar lining over a "
    "charcoal-grey zip hoodie, medium-dark skin tone, faint chin-strap goatee. "
    "NO on-screen text, NO captions, NO watermarks, NO logos, NO chyrons."
)

VARIATIONS = {
    "composite_v1": (
        "TWO-SHOT, both subjects framed from mid-chest up. "
        "Reporter on the LEFT of the frame, in strong LEFT-profile — viewer sees "
        "the back of his head, ear, cheekbone, jaw line, full short beard. He is "
        "leaning slightly forward, his right hand holding the black stick microphone "
        "with the white square mic-flag extended forward at chest height, the mic "
        "head pointed toward the younger man's mouth. "
        "Interviewee on the RIGHT of the frame, body angled 3/4 toward the camera, "
        "face fully visible to the viewer, mid-thought expression, mouth slightly "
        "open as if about to answer. Hands at his sides. "
        "The two figures are about 3 feet apart, the reporter's mic naturally "
        "occupying the middle-low foreground between them. " + COMMON
    ),
    "composite_v2": (
        "TWO-SHOT, slightly wider framing — both subjects from chest up but with "
        "more headroom and more of the El track structure visible above them. "
        "Reporter on the LEFT, strong LEFT-profile, mic extended forward at chest "
        "height with white square mic-flag clearly visible, head turned to the "
        "right toward the interviewee. "
        "Interviewee on the RIGHT, body 3/4 to camera, hands relaxed at sides, "
        "looking slightly down then back up at the reporter — listening energy. "
        "Slightly more space between the two subjects. The riveted black El "
        "girders overhead frame the top of the shot like a ceiling. " + COMMON
    ),
    "composite_v3": (
        "TWO-SHOT, tighter framing — both subjects from upper-chest up. "
        "Reporter on the LEFT in LEFT-profile, mic held forward at chest height, "
        "white square mic-flag visible. Reporter's posture closer in toward the "
        "interviewee. "
        "Interviewee on the RIGHT, 3/4 toward camera, head slightly tilted, more "
        "intimate two-shot feel. The El track structure visible only at the very "
        "top edge of the frame and the steel column at the far right of frame. "
        "Background deep brick Loop buildings clearly recognizable. " + COMMON
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
        image_paths=[str(REPORTER), str(INTERVIEWEE)],
        size="1024x1536",
        quality="high",
        n=1,
    )
    if r["status"] != "success":
        return slug, "failed", r["raw"].get("error", "unknown")
    return slug, "success", r["paths"][0]


def main():
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(gen, s, p): s for s, p in VARIATIONS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                _, status, info = f.result()
                print(f"[{s}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
