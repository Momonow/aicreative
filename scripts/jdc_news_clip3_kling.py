"""IL JDC news-interview CLIP 3 — Kling 3.0 std with element-refs.

REPORTER speaks (15s). Interviewee silent in frame.
Dialogue: abuse trigger + "millions paid out" social-proof beat.

Camera STARTS LOCKED with both characters already in frame from t=0.
Very subtle slow push-in over duration. No camera entry, no zoom-in reveal.

Output: outputs/illinois_jdc_news_eltracks/clip3.mp4
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_kling, download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks")
REF_URLS_CACHE = OUT_DIR / "kling_ref_urls.json"
OUTPUT_CLIP = OUT_DIR / "clip3.mp4"

PROMPT = """\
SHOT: ENG handheld two-shot, eye-level, 24mm wide. Both subjects mid-chest
up, ~3 feet apart, BOTH ALREADY IN FRAME FROM FRAME 1 (camera STARTS LOCKED,
no entry, no zoom-in reveal). Shallow DOF. Camera essentially LOCKED with
~±3px breathing float, optional VERY slow push-in (max 1.00→1.05). NO jitter,
NO shake spikes. Single continuous take, NO cuts. Photoreal local-news b-roll
feel, NOT polished broadcast.

SETTING: sidewalk under Chicago Loop elevated train tracks ('the L'). Black
steel girders overhead, steel column at frame edge, brick/concrete sidewalk,
Loop-era brick buildings + faint yellow taxi in soft-focus background.
Late-afternoon overcast daylight.

POSITIONING (from frame 1):
@element_reporter on LEFT in STRONG LEFT-PROFILE (viewer sees back of head,
ear, cheekbone, beard). RIGHT hand holds black stick mic with BLANK WHITE
square mic-flag (NO text, NO logo) extended forward at chest height, mic head
toward the younger man. Slight forward lean.

@element_interviewee on RIGHT, body 3/4 to camera (face clearly visible).
Hands at sides. LISTENS — eyes on reporter, mouth in soft neutral line.

ACTION — ONLY @element_reporter SPEAKS this entire clip:
@element_reporter delivers the heavier question. Mouth moves, jaw articulates
each word. Calm, even tempo, slightly serious — appropriate gravity.

@element_interviewee is COMPLETELY SILENT all 15 seconds. Mouth STAYS CLOSED.
Does NOT speak, does NOT mouth-move, not one syllable. LISTENS gravely, eyes
may shift slightly down then back up on heavier beats — lips stay sealed.

ABSOLUTE: only ONE voice = @element_reporter's. NO sound from interviewee.

@element_reporter voice: mature adult male, calm, even tempo, slightly lower
register, broadcast articulation. Late-30s field reporter delivering with
appropriate gravity.

PRONUNCIATION: "Illinois" = "ill-i-NOY" (silent final 's').

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions. NO
repetition. STOP after final word "forward".

@element_reporter SPOKEN (verbatim, stop after final word):
"If a guard or staff member ever touched you inappropriately, Illinois has already paid out millions to people who came forward."

NO on-screen text, NO captions, NO chyrons, NO station bug, NO watermarks.
Mic-flag stays BLANK WHITE.
"""


def main():
    urls = json.loads(REF_URLS_CACHE.read_text())

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
    print("Submitting CLIP 3 to KIE Kling 3.0 (std, 15s, 9:16, sound=True)...", flush=True)
    r = generate_kling(
        prompt=PROMPT,
        duration=15,
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
