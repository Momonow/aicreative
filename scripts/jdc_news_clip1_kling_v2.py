"""IL JDC news-interview CLIP 1 — Kling 3.0 STD with 3 element-refs, NO first-frame.

Approach: pure element-ref composition (no image_urls / no first-frame anchor).
Kling generates the scene composition itself from 3 element references:
  @element_setting     (Chicago L-tracks location, 2 background imgs)
  @element_reporter    (older reporter, 2 angle imgs)
  @element_interviewee (younger interviewee, 2 angle imgs)

Reporter-only dialogue. Interviewee silent in frame the entire clip.

Specific camera-shot language for realism:
  ENG handheld two-shot, 24mm equivalent, eye-level, shallow DOF, lateral
  positioning (reporter LEFT-profile, interviewee 3/4 to camera).

Mode: std (720p, cheaper than pro).
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
mic head toward the younger man. Leans slightly forward, calm, professional.

@element_interviewee on RIGHT, body 3/4 toward camera (face clearly visible).
Hands at sides. LISTENS — eyes on the reporter.

ACTION — ONLY @element_reporter SPEAKS the entire clip:
@element_reporter asks the question. Mouth moves, jaw articulates each word.
@element_interviewee is COMPLETELY SILENT the entire 10 seconds. Mouth STAYS
CLOSED in a soft neutral line. Does NOT speak, does NOT mouth-move, not one
syllable, not one twitch. LISTENS, may blink naturally, lips stay sealed.

ABSOLUTE: only ONE voice in the clip = @element_reporter's voice. NO sound
from @element_interviewee. After @element_reporter finishes "up?", clip
continues in SILENCE — reporter holds mic-forward, interviewee keeps
listening with mouth sealed.

@element_reporter voice: mature adult male, calm, even tempo, slightly lower
register, broadcast articulation. Late-30s field reporter.

PRONUNCIATION:
- "Audy Home" = "AW-dee Home" (rhymes with Audi)
- "Saint Charles" = full word "Saint"
- "juvie" = "JOO-vee"
- "Illinois" = "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO repetition.
STOP after final word "up?".

@element_reporter SPOKEN (verbatim, stop after final word):
"Did you ever spend time at the Audy Home, Saint Charles, or another Illinois juvie growing up?"

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks. Mic-flag stays BLANK WHITE.
"""


def main():
    urls = json.loads(REF_URLS_CACHE.read_text())
    print(f"Loaded element refs from {REF_URLS_CACHE}", flush=True)

    # Element refs only define the 2 characters.
    # Setting comes via image_urls=[setting_1] as Kling-required first frame
    # (empty background — characters get composed in from element refs).
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
    print("Submitting to KIE Kling 3.0 (std, 10s, 9:16, sound=True, 2 element-refs + empty-bg first-frame)...", flush=True)
    r = generate_kling(
        prompt=PROMPT,
        duration=10,
        aspect_ratio="9:16",
        image_urls=[urls["setting_1"]],    # empty bg — characters injected from elements
        sound=True,
        mode="std",                         # 720p cheaper tier
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
