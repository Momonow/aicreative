"""Submit ONE reporter solo clip + ONE interviewee solo clip (serial test pair).

Approach validated: single-character per clip, no two-person confusion,
news-style cutaway grammar. Veo only renders ONE person per shot.

Anchors:
  reporter_solo.png    → reporter test clip (8s, asks the full question)
  interviewee_solo.png → interviewee test clip (8s, says "I didn't know
                         that was even an option" — richer than "Yeah I did")

Veo 3.1 Fast 1080p, serial submission (one waits for the other) to avoid
KIE Cloudflare rate-limit. Each ~3-4min.

Output:
  outputs/illinois_jdc_news_eltracks/solo/reporter_test.mp4
  outputs/illinois_jdc_news_eltracks/solo/interviewee_test.mp4
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_catbox, generate_veo as kie_generate_veo, download as kie_download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/solo")
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTER_ANCHOR = Path("outputs/illinois_jdc_news_eltracks/wide/reporter_solo.png")
INTERVIEWEE_ANCHOR = Path("outputs/illinois_jdc_news_eltracks/wide/interviewee_solo.png")


REPORTER_PROMPT = """\
CHARACTER (ONE PERSON IN FRAME — REPORTER):

Man, medium-dark skin tone, late 30s. Close-cropped short black hair, full
neatly trimmed short beard, clean jawline. Wearing an unbuttoned black wool
overcoat over a charcoal-grey blazer and crisp white open-collar shirt.
STRONG LEFT-PROFILE (viewer sees back of his head, ear, cheekbone, jaw,
beard). His RIGHT hand holds a classic black handheld stick microphone
with thick foam windscreen and a BLANK WHITE square mic-flag (NO text, NO
letters, NO logo) extended forward at chest height — mic head pointed
toward an UNSEEN OFF-CAMERA INTERVIEWEE to the right of frame. He is
slightly leaning forward, professional, calm, attentive.

SETTING: under the Chicago Loop elevated train tracks ('the L'). Massive
black-painted riveted steel girders and lattice beams overhead. Large steel
support column visible. Polished brick and concrete sidewalk. Granite-clad
and red-brick Loop-era buildings in soft-focus deep background. Late-
afternoon overcast daylight, cool urban palette.

CAMERA: ENG handheld single-character shot, eye-level, ~35mm equivalent.
Reporter framed from mid-chest up, occupying the LEFT 2/3 of the frame.
Empty space on the RIGHT side of frame (where the off-camera interviewee
is). Shallow DOF — reporter sharp, background soft. Single continuous
locked-camera take with very subtle ~±5px breathing float. NO cuts, NO
zoom, NO sudden movement, NO jitter. Smooth, like a real documentary
cameraperson holding the camera steady.

FACE IDENTITY LOCK: Reporter's face remains IDENTICAL for the entire 8
seconds. Same beard, jaw, hairline, skin tone, eye position. No morphing,
no drift.

ACTION: The REPORTER asks the question, looking off-camera-right toward
the (unseen) interviewee. His mouth moves and articulates each word, jaw
forms the syllables. His head turns slightly as he asks.

REPORTER's voice: MATURE adult male, calm, even tempo, slightly lower
register, careful broadcast articulation. Late-30s field reporter.

PRONUNCIATION LOCK:
- "Audy Home" = "AW-dee Home" (rhymes with Audi)
- "Saint Charles" = full word "Saint" (NOT abbreviated)
- "juvie" = "JOO-vee"
- "Illinois" = "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know, so). NO
trailing words. NO additions. NO repetition. STOP after final word "up?".

SPOKEN DIALOGUE (verbatim, stop after final word):
"Did you ever spend time at the Audy Home, Saint Charles, or another Illinois juvie growing up?"

After "up?", clip continues in complete silence for ~1.5s with the reporter
holding his mic-forward posture.

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks. The white mic-flag stays COMPLETELY BLANK.
"""


INTERVIEWEE_PROMPT = """\
CHARACTER (ONE PERSON IN FRAME — INTERVIEWEE):

Younger man, medium-dark skin tone, mid 20s. Short freeform twists with
high temple-fade taper on the sides. Small gold stud earring in his LEFT
ear. Faint chin-strap goatee, light mustache stubble. Wearing a tan-camel
corduroy trucker jacket with cream sherpa-collar lining over a charcoal-
grey zip hoodie. Body angled 3/4 toward camera, face clearly visible.
Hands at his sides — he does NOT gesture.

A black handheld stick microphone with a BLANK WHITE square mic-flag (NO
text, NO letters, NO logo) enters from the BOTTOM-LEFT edge of frame,
held by an UNSEEN OFF-CAMERA reporter — the mic head is held just below
the interviewee's mouth, pointing up at him.

SETTING: under the Chicago Loop elevated train tracks ('the L'). Black-
painted riveted steel girders and lattice beams overhead. Polished brick
and concrete sidewalk. Granite-clad and red-brick Loop-era buildings in
soft-focus deep background, faint yellow taxi at the curb. Late-afternoon
overcast daylight.

CAMERA: ENG handheld single-character cutaway shot, eye-level, ~35mm
equivalent. Interviewee framed from mid-chest up, occupying the RIGHT 2/3
of the frame (LEFT 1/3 shows the mic + empty space toward off-camera
reporter). Shallow DOF — interviewee sharp, background soft. Single
continuous locked-camera take, very subtle ~±5px breathing float. NO cuts,
NO zoom, NO sudden movement, NO jitter.

FACE IDENTITY LOCK: Interviewee's face remains IDENTICAL for the entire
8 seconds. Same twists, taper fade, goatee, gold stud, jaw, eye position.
No morphing, no drift.

ACTION: The INTERVIEWEE gives an honest brief reaction. Mouth moves and
articulates each word. Slight eyebrow raise on "even an option" — small
beat of genuine surprise. NOT performative, NOT acted — honest, real.
Looking slightly off-camera-left (toward the unseen reporter).

INTERVIEWEE's voice: YOUNGER adult male, mid-20s, casual conversational
register, slightly higher pitch than a 40yo reporter. Honest unrehearsed
delivery, like a real young guy on the street, not an actor.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "option".

SPOKEN DIALOGUE (verbatim, stop after final word):
"I didn't know that was even an option."

After "option", clip continues in silence with the interviewee holding his
position, blinking naturally.

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks. The white mic-flag stays COMPLETELY BLANK.
"""


def submit_one(label, anchor_path, prompt, out_path):
    print(f"\n=== {label} ===", flush=True)
    print(f"Uploading anchor to catbox.moe: {anchor_path.name}…", flush=True)
    anchor_url = upload_catbox(str(anchor_path))
    print(f"  URL: {anchor_url}", flush=True)
    print(f"Prompt length: {len(prompt)} chars", flush=True)
    print(f"Submitting to Veo 3.1 Fast (veo3_fast, 1080p, 9:16)…", flush=True)
    r = kie_generate_veo(
        prompt=prompt,
        aspect_ratio="9:16",
        image_urls=[anchor_url, anchor_url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_fast",
        resolution="1080p",
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"FAILED: {str(r.get('raw'))[:500]}", flush=True)
        return False
    print(f"Downloading: {r['urls'][0]}", flush=True)
    kie_download(r["urls"][0], str(out_path))
    print(f"DONE → {out_path}", flush=True)
    return True


def main():
    # SERIAL — reporter first, then interviewee
    ok_r = submit_one(
        "REPORTER TEST (asks question)",
        REPORTER_ANCHOR, REPORTER_PROMPT,
        OUT_DIR / "reporter_test.mp4",
    )
    if not ok_r:
        print("Reporter test failed — stopping before interviewee submission.", flush=True)
        return
    print("\n=== Sleeping 60s before interviewee submission (rate-limit safety) ===")
    time.sleep(60)
    submit_one(
        "INTERVIEWEE TEST (I didn't know that was even an option)",
        INTERVIEWEE_ANCHOR, INTERVIEWEE_PROMPT,
        OUT_DIR / "interviewee_test.mp4",
    )


if __name__ == "__main__":
    main()
