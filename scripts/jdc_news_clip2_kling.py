"""IL JDC news-interview CLIP 2 — Kling 3.0 std with element-refs.

INTERVIEWEE speaks (5s). Reporter silent in frame.
Dialogue: "Yeah, I did."

Same Kling std setup as clip 1 (which user approved):
  image_urls=[setting_1]  (empty bg first-frame)
  @element_reporter   (silent this clip)
  @element_interviewee (speaks this clip)

Output: outputs/illinois_jdc_news_eltracks/clip2.mp4
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_kling, download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks")
REF_URLS_CACHE = OUT_DIR / "kling_ref_urls.json"
OUTPUT_CLIP = OUT_DIR / "clip2.mp4"

PROMPT = """\
SHOT: ENG handheld two-shot, eye-level, 24mm wide. Both subjects mid-chest
up, ~3 feet apart. Shallow DOF, subjects sharp, background soft. SLOW gentle
breathing float (~±5px), NO jitter, NO shake spikes. Single continuous take,
NO cuts, NO zoom. Photoreal local-news b-roll, genuine field-news camera
feel, NOT polished broadcast, NOT cinematic.

SETTING: sidewalk under Chicago Loop elevated train tracks ('the L'). Black
steel girders overhead, steel support column at frame edge, brick/concrete
sidewalk, Loop-era brick buildings + faint yellow taxi in soft-focus
background. Late-afternoon overcast daylight.

POSITIONING:
@element_reporter on LEFT in STRONG LEFT-PROFILE to camera (viewer sees back
of head, ear, cheekbone, beard). RIGHT hand holds black stick mic with BLANK
WHITE square mic-flag (NO text, NO logo) extended forward at chest height,
mic head toward the younger man. Leans slightly forward, professional.

@element_interviewee on RIGHT, body 3/4 toward camera (face clearly visible).
Hands at sides. Mouth slightly opens to answer.

ACTION — ONLY @element_interviewee SPEAKS the entire clip:
@element_interviewee gives a brief honest answer to a question. His mouth
moves, jaw articulates the two words. Brief, direct, slightly downcast eye
flicker on the admission, then back to the reporter.

@element_reporter is COMPLETELY SILENT the entire 5 seconds. Mouth STAYS
CLOSED in a soft neutral line. Does NOT speak, does NOT mouth-move, not one
syllable. LISTENS attentively, holds mic-forward posture. May blink naturally
but lips stay sealed.

ABSOLUTE: only ONE voice in the clip = @element_interviewee's voice. NO sound
from @element_reporter. After @element_interviewee finishes "did", brief
silence — both characters holding their positions.

@element_interviewee voice: younger adult male, mid-20s, casual conversational
register, slightly higher pitch than a 40-year-old reporter, honest brief
delivery. Sounds like a real young guy on the street, not an actor.

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like). NO trailing words.
NO repetition. STOP after final word "did".

@element_interviewee SPOKEN (verbatim, stop after final word):
"Yeah, I did."

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks. Mic-flag stays BLANK WHITE.
"""


def main():
    urls = json.loads(REF_URLS_CACHE.read_text())
    print(f"Loaded element refs from {REF_URLS_CACHE}", flush=True)

    kling_elements = [
        {
            "name": "element_reporter",
            "description": "older Black male field news reporter in black wool overcoat over charcoal blazer and white shirt, late 30s, full short beard, holding black stick mic with blank white mic-flag",
            "element_input_urls": [urls["reporter_4"], urls["reporter_4_alt"]],
        },
        {
            "name": "element_interviewee",
            "description": "younger Black male in tan corduroy trucker jacket with cream sherpa collar over grey hoodie, mid 20s, short freeform twists with high temple-fade taper, gold stud earring in left ear, faint chin-strap goatee",
            "element_input_urls": [urls["interviewee_1"], urls["interviewee_1_alt"]],
        },
    ]

    print(f"Prompt length: {len(PROMPT)} chars (cap 2500)", flush=True)
    print("Submitting CLIP 2 to KIE Kling 3.0 (std, 5s, 9:16, sound=True)...", flush=True)
    r = generate_kling(
        prompt=PROMPT,
        duration=5,
        aspect_ratio="9:16",
        image_urls=[urls["setting_1"]],
        sound=True,
        mode="std",
        kling_elements=kling_elements,
        multi_shots=False,
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"\nKLING FAILED: {str(r.get('raw'))[:600]}", flush=True)
        return
    print(f"Downloading: {r['urls'][0]}", flush=True)
    download(r["urls"][0], str(OUTPUT_CLIP))
    print(f"DONE → {OUTPUT_CLIP}", flush=True)


if __name__ == "__main__":
    main()
