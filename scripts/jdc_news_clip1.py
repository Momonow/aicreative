"""IL JDC news-interview ad — CLIP 1 of 3 via KIE Veo 3.1 Lite.

Two-person Chicago L-tracks news interview, both characters in frame,
but ONLY the REPORTER speaks. Interviewee stays silent (mouth closed) the
entire clip. This avoids the Veo voice-attribution problem from earlier
(ΔF0 1.4Hz on v2: both "speakers" sounded like the same person).

Strengthened prompt with explicit FACE IDENTITY HOLD + MOTION SMOOTHNESS locks
to address Lite's known weaknesses (face drift mid-clip + occasional jitter).

Dialogue (REPORTER only):
  "Did you ever spend time at the Audy Home, Saint Charles, or another Illinois
  juvie growing up?"

Anchor: outputs/illinois_jdc_news_eltracks/anchor/composite_v2.png
        (URL cached in clip1_anchor_url.txt)

Output: outputs/illinois_jdc_news_eltracks/clip1.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file, generate_veo as kie_generate_veo, download as kie_download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks")
ANCHOR_LOCAL = OUT_DIR / "anchor" / "composite_v2.png"
ANCHOR_URL_CACHE = OUT_DIR / "clip1_anchor_url.txt"
OUTPUT_CLIP = OUT_DIR / "clip1.mp4"

PROMPT = """\
CHARACTERS (TWO PEOPLE IN FRAME, ONLY ONE SPEAKS):

REPORTER (LEFT side of frame, mid-foreground, STRONG LEFT-PROFILE to camera):
A man with medium-dark skin tone, late 30s. Close-cropped short black hair,
full neatly trimmed short beard, clean jawline. Wearing an unbuttoned black
wool overcoat over a charcoal-grey blazer and crisp white open-collar shirt.
His RIGHT hand holds a classic black handheld stick microphone with a thick
foam windscreen and a WHITE square mic-flag (COMPLETELY BLANK — no text, no
letters, no station logo, no symbols). Mic extended forward at chest height,
head pointed toward the younger man. He is slightly leaning forward, calm,
attentive, professional. NOT theatrical. NOT smiling.

INTERVIEWEE (RIGHT side of frame, body 3/4 toward camera):
A younger man with medium-dark skin tone, mid 20s. Short freeform twists with
high temple-fade taper on the sides. Small gold stud earring in his LEFT ear.
Faint chin-strap goatee, light mustache stubble. Wearing a tan-camel corduroy
trucker jacket with cream sherpa-collar lining over a charcoal-grey zip
hoodie, top hoodie zip-pull visible at chest. Hands at his sides. He does NOT
gesture. All expression is in his face — listening, processing.

SETTING:
Real daylight under the Chicago Loop elevated train tracks ('the L'). Massive
black-painted riveted steel girders and lattice beams overhead. Large steel
support column visible to the side. Polished brick and concrete sidewalk under
foot. Granite-clad and red-brick Loop-era buildings in soft-focus deep
background, faint yellow taxi at the curb. Late-afternoon overcast daylight,
cool urban palette, subtle El-pattern shadows on the ground.

CAMERA + MOTION (CRITICAL — must be smooth throughout):
Locked TWO-SHOT, both subjects framed from mid-chest up. ~24mm equivalent.
Single continuous handheld take with VERY SUBTLE breathing-only float (~±5
pixels of drift, slow and gentle). NO cuts. NO zoom. NO rack focus. NO sudden
movements. NO jitter. NO shake spikes. Motion is smooth and slow, like a
seasoned documentary cameraperson holding the camera steady. Slight shallow
depth-of-field — subjects sharp, background softly blurred. Documentary
handheld realism, NOT polished broadcast smoothness, but DEFINITELY NOT
jittery or shaky.

CRITICAL — FACE IDENTITY MUST HOLD FOR THE ENTIRE 8 SECONDS:
Both characters' faces must remain IDENTICAL from second 0 through second 8.
The REPORTER's face at second 0 (beard shape, hairline, jaw, eye position,
skin tone, age) must be the SAME face at second 4 and the SAME face at
second 8 — no morphing, no drift, no shift to a different person.
Same applies to the INTERVIEWEE — his twists, taper fade, goatee, gold stud
earring, jaw, eye position, skin tone must all be IDENTICAL throughout. Each
character is the SAME PERSON for the full 8 seconds. NO face drift. NO
identity blur. NO morphing between frames.

CRITICAL — ONLY THE REPORTER SPEAKS THIS ENTIRE CLIP:
The REPORTER's mouth opens and articulates each word. His jaw moves, his lips
form the syllables. His head turns slightly toward the interviewee as he asks.

The INTERVIEWEE's mouth STAYS CLOSED in a soft neutral line the ENTIRE 8
seconds. His lips DO NOT move. Not even one syllable. Not a single twitch.
He LISTENS and watches the reporter. He may blink naturally and his eyes may
shift expression, but his MOUTH IS SEALED throughout. He makes NO SOUND.

PHASE 1 (~0.0s – ~5.5s) — the reporter asks the question. Reporter mouth
moves, interviewee mouth sealed, both eyes engaged.

PHASE 2 (~5.5s – ~8.0s) — reporter finishes the question. Both mouths closed.
Reporter holds his mic-forward posture. Interviewee continues to LISTEN
quietly. The clip continues in silence.

ABSOLUTE RULES:
- Only ONE voice is heard in this entire clip: the REPORTER's voice.
- The interviewee makes NO SOUND, NO mouth movement, NO syllables.
- NO on-screen text, NO captions, NO subtitles, NO chyrons, NO lower-thirds,
  NO station bug, NO watermarks. The white mic-flag STAYS COMPLETELY BLANK.

REPORTER's voice: MATURE adult male, calm, even-tempo, slightly lower
register, careful broadcast-trained articulation. Late-30s local-news field
reporter.

PRONUNCIATION LOCK:
- "Audy Home" → pronounce as "AW-dee Home" (rhymes with the car brand Audi)
- "Saint Charles" → pronounce the full word "Saint" (NOT abbreviated)
- "juvie" → pronounce as "JOO-vee" (short for juvenile)
- "Illinois" → pronounce as "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers ("uh", "um", "like", "you know",
"so"). NO trailing words at the end. NO words beyond what is listed below.
NO repetition. STOP all speech after the final word "up?".

SPOKEN DIALOGUE (REPORTER only, verbatim, stop after final word):
"Did you ever spend time at the Audy Home, Saint Charles, or another Illinois juvie growing up?"

(After "up?", NO further words from anyone. Hold the two-shot in respectful
silence with both characters in their established positions.)
"""


def try_kie(anchor_url):
    """KIE Veo 3.1 Lite. FIRST_AND_LAST_FRAMES anchor pattern."""
    print("Submitting to KIE (veo3_lite, Veo 3.1 Lite)...", flush=True)
    try:
        r = kie_generate_veo(
            prompt=PROMPT,
            aspect_ratio="9:16",
            image_urls=[anchor_url, anchor_url],
            mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
            model="veo3_lite",
        )
        if r["status"] == "success" and r["urls"]:
            return r["urls"][0], "kie_veo3_lite"
        print(f"KIE failed: {str(r.get('raw'))[:500]}", flush=True)
    except Exception as e:
        print(f"KIE exception: {e}", flush=True)
    return None, None


def main():
    if ANCHOR_URL_CACHE.exists():
        anchor_url = ANCHOR_URL_CACHE.read_text().strip()
        print(f"Using cached anchor URL: {anchor_url}", flush=True)
    else:
        print(f"Uploading anchor: {ANCHOR_LOCAL}", flush=True)
        anchor_url = upload_file(str(ANCHOR_LOCAL))
        ANCHOR_URL_CACHE.write_text(anchor_url)

    url, provider = try_kie(anchor_url)
    if not url:
        print("KIE FAILED — abort", flush=True)
        return
    print(f"Downloading from {provider}: {url}", flush=True)
    kie_download(url, str(OUTPUT_CLIP))
    print(f"DONE → {OUTPUT_CLIP} (via {provider})", flush=True)


if __name__ == "__main__":
    main()
