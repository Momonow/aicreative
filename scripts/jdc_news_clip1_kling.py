"""IL JDC news-interview ad — CLIP 1 via KIE Kling 3.0 with element-refs.

Kling 3.0 "Omni" approach: 2 character element-refs (@reporter + @interviewee) +
composite scene baseline. Each character locked by its persona reference image
so identity doesn't drift mid-clip the way Veo Lite/Fast did.

Reporter-only dialogue (single voice — avoids the Veo ΔF0 1.4Hz "both
speakers sound the same" failure mode we hit on v2).

Dialogue (REPORTER only):
  "Did you ever spend time at the Audy Home, Saint Charles, or another Illinois
  juvie growing up?"

Element refs:
  @element_reporter   = outputs/illinois_jdc_news_eltracks/reference/reporter_4.png
  @element_interviewee = outputs/illinois_jdc_news_eltracks/reference/interviewee_1.png
  Scene baseline (image_urls): composite_v2.png

Output: outputs/illinois_jdc_news_eltracks/clip1.mp4
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_kling, download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks")
REF_URLS_CACHE = OUT_DIR / "kling_ref_urls.json"
OUTPUT_CLIP = OUT_DIR / "clip1.mp4"

PROMPT = """\
Photoreal news b-roll handheld two-shot under Chicago Loop elevated train
tracks ('the L'). Black-painted riveted steel girders + lattice beams overhead,
steel support column visible. Granite-clad red-brick Loop buildings in soft
deep background, yellow taxi at curb. Late-afternoon overcast daylight, cool
urban palette, El-pattern shadows. Documentary realism, NOT polished broadcast.

TWO-SHOT, both subjects mid-chest up. @element_reporter on LEFT in strong
LEFT-profile (back of head, ear, cheekbone, short beard visible). Black wool
overcoat over charcoal blazer + white shirt. Holds black stick mic with BLANK
WHITE square mic-flag (no text, no logo) extended forward at chest height in
his RIGHT hand, mic head pointed toward the younger man. Slightly leaning in.

@element_interviewee on RIGHT, body 3/4 toward camera. Tan corduroy trucker
jacket with cream sherpa collar over grey hoodie. Hands at sides.

ACTION — ONLY @element_reporter SPEAKS this entire clip:
@element_reporter asks the question. His mouth moves, jaw articulates each word.
@element_interviewee is COMPLETELY SILENT the ENTIRE 10 seconds. His mouth
STAYS CLOSED in a soft neutral line — does NOT speak, does NOT mouth-move,
not one syllable. He LISTENS and watches @element_reporter. He may blink
naturally but his lips remain sealed throughout.

ABSOLUTE: only ONE voice in this clip = @element_reporter's. NO sound from
@element_interviewee. After @element_reporter finishes the question, clip
continues in SILENCE for ~3s — reporter holds mic-forward posture, interviewee
continues to listen quietly with mouth sealed.

@element_reporter's voice: mature adult male, calm, even-tempo, slightly lower
register, broadcast articulation. Late-30s local-news field reporter.

PRONUNCIATION:
- "Audy Home" = "AW-dee Home" (rhymes with Audi)
- "Saint Charles" = full word "Saint"
- "juvie" = "JOO-vee"
- "Illinois" = "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like). NO trailing words. NO
repetition. STOP after final word "up?".

@element_reporter SPOKEN DIALOGUE (verbatim, stop after final word):
"Did you ever spend time at the Audy Home, Saint Charles, or another Illinois juvie growing up?"

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks. The white mic-flag stays COMPLETELY BLANK.
"""


def main():
    urls = json.loads(REF_URLS_CACHE.read_text())
    print(f"Loaded element refs from {REF_URLS_CACHE}", flush=True)
    for k, v in urls.items():
        print(f"  {k}: {v}", flush=True)

    kling_elements = [
        {
            "name": "element_reporter",
            "description": "older Black male field news reporter in black wool overcoat over charcoal blazer and white shirt, late 30s, full short beard, holding black stick mic with blank white mic-flag",
            "element_input_urls": [urls["reporter_4"], urls["reporter_4_alt"]],
        },
        {
            "name": "element_interviewee",
            "description": "younger Black male in tan-camel corduroy trucker jacket with cream sherpa collar over grey hoodie, mid 20s, short freeform twists with high temple-fade taper, gold stud earring in left ear, faint chin-strap goatee",
            "element_input_urls": [urls["interviewee_1"], urls["interviewee_1_alt"]],
        },
    ]

    print("\nSubmitting to KIE Kling 3.0 (pro mode, 10s, 9:16, sound=True, 2 element-refs)...", flush=True)
    r = generate_kling(
        prompt=PROMPT,
        duration=10,
        aspect_ratio="9:16",
        image_urls=[urls["composite_v2"]],
        sound=True,
        mode="pro",
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
