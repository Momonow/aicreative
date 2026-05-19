"""Reporter + interviewee solo test pair — NO MIC visible in either clip.

User flagged mic-holding rendering as visually odd. Removing mic entirely:
- Tighter head/shoulders crop (mic out of frame)
- Prompt drops all mic mentions
- Reads as intimate documentary-style cutaway (Frontline/60 Minutes
  closeup), not man-on-the-street with mic
- Wardrobe (overcoat/blazer + sherpa/corduroy) + off-camera gaze still
  convey the news interview format

Veo 3.1 Fast 1080p, anchors via catbox.moe, serial submission.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_catbox, generate_veo as kie_generate_veo, download as kie_download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/solo")
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTER_ANCHOR = Path("outputs/illinois_jdc_news_eltracks/wide/reporter_nomic.png")
INTERVIEWEE_ANCHOR = Path("outputs/illinois_jdc_news_eltracks/wide/interviewee_nomic.png")


REPORTER_PROMPT = """\
CHARACTER (ONE PERSON IN FRAME — REPORTER):

Man, medium-dark skin tone, late 30s. Close-cropped short black hair, full
neatly trimmed short beard, clean jawline. Wearing an unbuttoned black wool
overcoat over a charcoal-grey blazer and a crisp white open-collar shirt.
STRONG LEFT-PROFILE to camera (viewer sees the back of his head, ear,
cheekbone, jaw, beard). Tight head-and-shoulders framing. He is slightly
leaning forward, professional, attentive — interviewing an UNSEEN OFF-CAMERA
subject to the right of frame.

NO microphone in this shot. NO mic, NO mic flag, NO equipment visible. His
hands are NOT visible in the frame. Just his head and upper shoulders, with
the cool overcoat collar and white shirt at the bottom of frame.

SETTING: under the Chicago Loop elevated train tracks ('the L'). Granite-clad
and red-brick Loop-era building columns visible behind him in soft focus.
Steel girder elements faintly visible. Late-afternoon overcast daylight,
cool urban palette. Shallow DOF — reporter sharp, background blurred.

CAMERA: ENG handheld documentary close-up, eye-level, ~85mm equivalent tight
portrait framing. Single continuous locked-camera take with very subtle
~±5px breathing float. NO cuts, NO zoom, NO sudden movement, NO jitter.
Smooth and steady.

FACE IDENTITY LOCK: Reporter's face remains IDENTICAL for the entire 8
seconds. Same beard, jaw, hairline, skin tone, eye position.

ACTION: The REPORTER asks the question, looking off-camera-right. His mouth
moves and articulates each word, jaw forms the syllables. His head turns
very slightly as he asks. Serious, calm tone.

REPORTER's voice: MATURE adult male, calm, even tempo, slightly lower
register, careful broadcast articulation. Late-30s field reporter.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational broadcast
projection — like he's miked for a TV news segment. NOT whispered. NOT
muttered. NOT soft. NOT distant. Clean clear loud broadcast-recording audio,
the kind you'd hear on a Frontline / 20-20 / local-news interview segment.
Voice fills the foreground audio mix.

PRONUNCIATION LOCK:
- "Audy Home" = "AW-dee Home" (rhymes with Audi)
- "Saint Charles" = full word "Saint" (NOT abbreviated)
- "juvie" = "JOO-vee"
- "Illinois" = "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know, so). NO
trailing words. NO additions. NO repetition. STOP after final word "up?".

SPOKEN DIALOGUE (verbatim, stop after final word):
"Did you ever spend time at the Audy Home, Saint Charles, or another Illinois juvie growing up?"

After "up?", clip continues in complete silence with the reporter holding
his attentive listening posture.

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks, NO microphone, NO equipment.
"""


INTERVIEWEE_PROMPT = """\
CHARACTER (ONE PERSON IN FRAME — INTERVIEWEE):

Younger man, medium-dark skin tone, mid 20s. Short freeform twists with
high temple-fade taper on the sides. Small gold stud earring in his LEFT
ear. Faint chin-strap goatee, light mustache stubble. Wearing a tan-camel
corduroy trucker jacket with cream sherpa-collar lining over a charcoal-
grey zip hoodie. Body angled 3/4 toward camera, face clearly visible.
Tight head-and-shoulders framing.

NO microphone in this shot. NO mic, NO mic flag, NO equipment visible.
His hands are NOT in frame. Just his head and upper shoulders, with the
corduroy collar + sherpa lining at the bottom of frame.

SETTING: under the Chicago Loop elevated train tracks ('the L'). Granite-clad
and red-brick Loop-era buildings visible behind him in soft focus. Steel
girder elements faintly visible. Late-afternoon overcast daylight, cool
urban palette. Shallow DOF — interviewee sharp, background blurred.

CAMERA: ENG handheld documentary close-up, eye-level, ~85mm equivalent tight
portrait framing. Single continuous locked-camera take with very subtle
~±5px breathing float. NO cuts, NO zoom, NO sudden movement, NO jitter.

FACE IDENTITY LOCK: Interviewee's face remains IDENTICAL for the entire
8 seconds. Same twists, taper fade, goatee, gold stud, jaw, eye position.

ACTION: The INTERVIEWEE gives an honest brief reaction. Mouth moves and
articulates each word. Slight eyebrow raise on "even an option" — small
beat of genuine surprise. NOT performative — honest, real. Looking slightly
off-camera-left (toward the unseen reporter).

INTERVIEWEE's voice: YOUNGER adult male, mid-20s, casual conversational
register, slightly higher pitch than a 40yo reporter. Honest unrehearsed
delivery, like a real young guy on the street, not an actor.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational broadcast
projection — like he's miked for a TV news segment. NOT whispered. NOT
muttered. NOT soft. NOT distant. Clean clear loud broadcast-recording audio,
the kind you'd hear on a Frontline / 20-20 / local-news interview segment.
Voice fills the foreground audio mix.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "option".

SPOKEN DIALOGUE (verbatim, stop after final word):
"I didn't know that was even an option."

After "option", clip continues in silence with the interviewee holding his
position, blinking naturally.

ABSOLUTELY NO on-screen text, NO captions, NO chyrons, NO station bug, NO
watermarks, NO microphone, NO equipment.
"""


def submit_one(label, anchor_path, prompt, out_path):
    print(f"\n=== {label} ===", flush=True)
    print(f"Uploading anchor to catbox.moe: {anchor_path.name}…", flush=True)
    anchor_url = upload_catbox(str(anchor_path))
    print(f"  URL: {anchor_url}", flush=True)
    print(f"Prompt length: {len(prompt)} chars", flush=True)
    print(f"Submitting to Veo 3.1 Fast (1080p)…", flush=True)
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
    ok_r = submit_one(
        "REPORTER (no-mic) TEST",
        REPORTER_ANCHOR, REPORTER_PROMPT,
        OUT_DIR / "reporter_nomic_test.mp4",
    )
    if not ok_r:
        print("Reporter test failed — stopping before interviewee submission.")
        return
    print("\n=== Sleeping 30s ===")
    time.sleep(30)
    submit_one(
        "INTERVIEWEE (no-mic) TEST",
        INTERVIEWEE_ANCHOR, INTERVIEWEE_PROMPT,
        OUT_DIR / "interviewee_nomic_test.mp4",
    )


if __name__ == "__main__":
    main()
