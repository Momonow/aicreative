"""Generate persona refs for the IL JDC NEWS INTERVIEW clone (under Chicago El tracks).

Format: field reporter (polished, station-branded mic flag) interviewing a passerby
under elevated train infrastructure in the Chicago Loop. Reads as local-affiliate
news b-roll — CBS Chicago / WGN field segment energy.

Two roles, 4 candidates each (parallel via OpenAI gpt-image-2 medium quality):

- REPORTER: man, late 30s to 40s, blazer/suit jacket, holds a station-branded
  stick microphone with a colored mic flag. Pro broadcast reporter look.
- INTERVIEWEE: man, medium-dark skin tone, mid-20s, casual Chicago streetwear.

Moderation safety: descriptors say "medium-dark skin tone" instead of "Black man"
since dialogue context is sexual-abuse-compensation (per CLAUDE.md Veo moderation
triggers — same rule kept consistent for GPT-Image).

Output: outputs/illinois_jdc_news_eltracks/reference/{reporter,interviewee}_{1..4}.png
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/reference")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COMMON_STYLE = (
    "Photoreal portrait, real-world daylight, NOT studio. Visible pores, fine lines, "
    "skin texture, slight asymmetry, no makeup, no beauty mode, no retouching, no "
    "filter, no skin smoothing. Documentary handheld photograph feel, shot on a phone "
    "or small mirrorless, shallow background blur. "
    "NO on-screen text, NO captions, NO watermarks, NO logos, NO chyrons."
)

COMMON_SETTING = (
    "Setting: under the Chicago Loop elevated train tracks ('the L'). Massive black "
    "and dark-green painted steel girders and lattice beams overhead, large riveted "
    "steel support columns visible to the side, polished brick/concrete sidewalk under "
    "foot. Distinctive Chicago downtown street: older granite-clad and red-brick "
    "Loop-era buildings line the far side of the street, faintly visible parked cars "
    "and yellow taxi at the curb, daylight diffused through the steel structure overhead "
    "casting subtle pattern shadows on the ground. Late afternoon or overcast daytime "
    "lighting, cool urban palette, slight haze. Iconic 'this is Chicago' read."
)

REPORTER_VARIATIONS = {
    "reporter_1": (
        "Medium-chest-up portrait of a male field news reporter, white, late 30s. "
        "Short well-groomed dark brown hair, clean-shaven. Wearing a charcoal-grey "
        "wool blazer over a crisp light blue button-down shirt, no tie, top button "
        "undone. Holding a black handheld stick microphone with a square red "
        "station-branded mic flag (blank colored flag, no text or logo visible), "
        "extended forward at chest height in his right hand. "
        "Body angled in strong LEFT profile to the camera — viewer sees the back of "
        "his head, ear, cheekbone, jaw line. Professional, engaged, calm broadcast "
        "energy. " + COMMON_SETTING + " " + COMMON_STYLE
    ),
    "reporter_2": (
        "Medium-chest-up portrait of a male field news reporter, medium-dark skin "
        "tone, early 40s. Short black hair with neat side-part fade, clean-shaven "
        "with light goatee. Wearing a navy-blue blazer over a white open-collar "
        "button-down shirt. Holding a black handheld stick microphone with a "
        "rectangular blue station-branded mic flag (blank colored flag, no text or "
        "logo visible), extended forward at chest height. "
        "Body angled in strong LEFT profile to the camera. Warm, attentive, the "
        "energy of a seasoned local-news anchor in the field. "
        + COMMON_SETTING + " " + COMMON_STYLE
    ),
    "reporter_3": (
        "Medium-chest-up portrait of a male field news reporter, white, mid 40s. "
        "Short greying hair at the temples, neatly trimmed peppered stubble. "
        "Wearing a dark grey single-breasted suit jacket over a pale grey shirt, no "
        "tie. Holding a matte black handheld stick microphone with a black "
        "rectangular mic flag (blank, no text), extended forward at chest height. "
        "Body angled in strong LEFT profile to the camera. Slightly more serious, "
        "investigative news-anchor energy. "
        + COMMON_SETTING + " " + COMMON_STYLE
    ),
    "reporter_4": (
        "Medium-chest-up portrait of a male field news reporter, medium-dark skin "
        "tone, late 30s. Short close-cropped hair, full but neat short beard. "
        "Wearing a black wool overcoat unbuttoned over a charcoal blazer and a "
        "white shirt. Holding a classic black handheld stick microphone with a "
        "white square station-branded mic flag (blank, no text or logo), extended "
        "forward at chest height. "
        "Body angled in strong LEFT profile to the camera. Modern-news, "
        "polished-but-real energy. " + COMMON_SETTING + " " + COMMON_STYLE
    ),
}

INTERVIEWEE_VARIATIONS = {
    "interviewee_1": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Hair styled in short freeform twists with a high temple-fade taper on the "
        "sides. Small gold stud earring in his left ear. Faint chin-strap goatee, "
        "light mustache stubble. Wearing a tan-camel corduroy trucker jacket with "
        "cream sherpa-collar lining over a charcoal-grey zip hoodie underneath, top "
        "hoodie zip-pull visible. Body angled 3/4 toward camera, slight head tilt, "
        "curious-but-cautious expression. Hands at his sides. "
        + COMMON_SETTING + " " + COMMON_STYLE
    ),
    "interviewee_2": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Short faded buzz cut on the sides, slightly longer black curls on top. "
        "Single small silver stud earring in left ear. Light beard stubble. "
        "Wearing a black puffer vest over a heather-grey crew-neck sweatshirt and "
        "a black thermal henley shirt visible at the collar. Body angled 3/4 toward "
        "camera. Skeptical, slightly guarded expression. Hands relaxed at sides. "
        + COMMON_SETTING + " " + COMMON_STYLE
    ),
    "interviewee_3": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Short box braids pulled into a small bun at the back, neat taper at the "
        "sides. Gold chain visible at the collar, no earring. Faint mustache stubble, "
        "sparse chin goatee. Wearing a dark olive utility canvas jacket over a "
        "cream waffle-knit henley. Body angled 3/4 toward camera. Open, almost "
        "surprised expression — like he just heard something he didn't know. "
        "Hands at his sides. " + COMMON_SETTING + " " + COMMON_STYLE
    ),
    "interviewee_4": (
        "Medium-chest-up portrait of a younger man, medium-dark skin tone, mid 20s. "
        "Short waves with a sharp temple-fade taper. Single small gold hoop in the "
        "left ear. Clean-shaven with light jawline shadow. Wearing a heavy quilted "
        "black bomber jacket over a white tee with a thin gold chain visible. Body "
        "angled 3/4 toward camera, head slightly tilted down then up — listening "
        "energy. Hands at his sides. " + COMMON_SETTING + " " + COMMON_STYLE
    ),
}

ALL_PROMPTS = {**REPORTER_VARIATIONS, **INTERVIEWEE_VARIATIONS}


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
