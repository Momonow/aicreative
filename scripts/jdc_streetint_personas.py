"""Generate persona reference candidates for the IL JDC street-interview clone.

Two roles, 4 candidates each (parallel via OpenAI gpt-image-2 medium quality):

- INTERVIEWER: Black man 50s, salt-and-pepper goatee, olive bomber over black hoodie,
  holding a stick mic. Community-elder energy, NOT broadcast reporter.
- INTERVIEWEE: Black man mid-20s, freeform short twists w/ high taper fade, gold stud,
  tan corduroy trucker w/ cream sherpa collar over grey hoodie.

Moderation safety: descriptors say "medium-dark skin tone" instead of "Black man" since
dialogue context is sexual-abuse-compensation (per CLAUDE.md Veo moderation triggers,
the same rule applies to GPT-Image less aggressively but stays consistent).

Output: outputs/illinois_jdc_streetint/reference/{interviewer,interviewee}_{1..4}.png
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

OUT_DIR = Path("outputs/illinois_jdc_streetint/reference")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COMMON = (
    "Photoreal portrait, daylight overcast natural lighting, NOT studio. "
    "Visible pores, fine lines, faint skin texture, slight asymmetry, no makeup, "
    "no beauty mode, no retouching, no filter, no skin smoothing. "
    "Documentary handheld photograph feel, shot on a phone or small mirrorless, "
    "shallow background blur. Urban street setting: older red-brick warehouse-loft "
    "buildings out of focus in deep background, sidewalk, parked cars faintly visible. "
    "Looks like Chicago west-side / loft district / Fulton-Market type block. "
    "Late fall jacket weather, mild cool overcast tint. "
    "NO on-screen text, NO captions, NO watermarks, NO logos."
)

INTERVIEWER_VARIATIONS = {
    "interviewer_1": (
        "Medium-chest-up portrait of a man, medium-dark skin tone, late 40s to early 50s. "
        "Short greying buzz-cut hair, neatly trimmed salt-and-pepper goatee. "
        "Wearing a zipped-down olive-green nylon bomber jacket with a black zip hoodie "
        "underneath and a plain white crew-neck tee peeking out at the collar. "
        "Silver chain bracelet on his right wrist, visible holding a black handheld "
        "stick microphone with a thick black foam windscreen at chest height. "
        "Body angled in strong LEFT profile to the camera — viewer sees the back of his "
        "head, ear, cheekbone, salt-pepper goatee. Relaxed, slightly leaning forward, "
        "approachable community-elder energy, NOT a polished TV reporter. "
        + COMMON
    ),
    "interviewer_2": (
        "Medium-chest-up portrait of a man, medium-dark skin tone, mid 50s. "
        "Short close-cropped greying hair, fuller salt-and-pepper goatee with more beard. "
        "Wearing a faded army-green canvas field jacket over a charcoal grey hoodie, "
        "white tee at the collar. Silver wristwatch on right wrist visible holding a "
        "matte black stick microphone with thick foam windscreen at chest height. "
        "Body angled in strong LEFT profile to camera. Calm, slightly weathered, looks "
        "like a longtime neighborhood organizer or pastor. "
        + COMMON
    ),
    "interviewer_3": (
        "Medium-chest-up portrait of a man, medium-dark skin tone, late 40s. "
        "Short faded buzz cut with slight grey at the temples, neatly trimmed black "
        "goatee with faint grey flecks. Wearing a darker olive bomber jacket fully "
        "zipped up, no hoodie visible underneath. Plain black handheld stick microphone "
        "with foam windscreen held at chest height in his right hand. "
        "Body in strong LEFT profile to camera. Slightly more serious expression, "
        "investigative energy without being adversarial. "
        + COMMON
    ),
    "interviewer_4": (
        "Medium-chest-up portrait of a man, medium-dark skin tone, early 50s. "
        "Short greying hair faded on the sides, full salt-and-pepper goatee. "
        "Wearing a zipped olive bomber jacket over a heather-grey hoodie with a thin "
        "white tee peeking at the collar. Beaded leather wristband on right wrist "
        "holding a classic black handheld stick microphone with foam windscreen, "
        "extended slightly forward at chest height as if interviewing someone off-frame. "
        "Body in strong LEFT profile to camera. Warm, open expression, the energy of a "
        "trusted older brother. "
        + COMMON
    ),
}

INTERVIEWEE_VARIATIONS = {
    "interviewee_1": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Hair styled in short freeform twists with a high temple-fade taper on the sides. "
        "Small gold stud earring in his left ear. Faint chin-strap goatee, light "
        "mustache stubble. Wearing a tan-camel corduroy trucker jacket with cream "
        "sherpa-collar lining over a charcoal-grey zip hoodie underneath, top hoodie "
        "zip-pull visible. Body angled 3/4 toward camera, head slightly tilted, "
        "curious-but-cautious expression. Hands at his sides, no gesturing. "
        + COMMON
    ),
    "interviewee_2": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Hair in short freeform twists, medium length, high taper fade on sides. "
        "Small silver stud earring in his left ear. Light beard stubble around the jaw. "
        "Wearing a brown corduroy sherpa-collar trucker jacket over a dark grey hoodie. "
        "Body angled 3/4 toward camera. Slightly more guarded expression, hint of "
        "skepticism. Hands relaxed at sides. "
        + COMMON
    ),
    "interviewee_3": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Hair styled in longer freeform short twists with a high fade taper. "
        "Single small gold hoop earring in his left ear. Sparse chinstrap beard. "
        "Wearing a tan suede / corduroy sherpa-collar jacket over a navy-grey "
        "zip hoodie. Body angled 3/4 toward camera. Open, almost surprised expression — "
        "like he just heard something he didn't know. Hands at his sides. "
        + COMMON
    ),
    "interviewee_4": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Hair in short freeform twists pulled up slightly at the crown, high taper "
        "fade on sides. Gold stud earring in his left ear. Faint mustache stubble, "
        "soft chin-strap. Wearing a camel-tan corduroy trucker with off-white sherpa "
        "collar and lining, over a slate-grey hoodie. Body 3/4 toward camera, mouth "
        "slightly open as if mid-thought. Hands at sides. "
        + COMMON
    ),
}

ALL_PROMPTS = {**INTERVIEWER_VARIATIONS, **INTERVIEWEE_VARIATIONS}


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
        futures = {ex.submit(gen, s, p): s for s, p in ALL_PROMPTS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                _, status, info = f.result()
                print(f"[{s}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
