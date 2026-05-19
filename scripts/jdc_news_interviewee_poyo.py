"""Test interviewee no-mic via Poyo Veo 3.1 Fast ($0.10/clip flat).

Switching providers from KIE Fast (3 consecutive Internal Error 500s on
this prompt+anchor) to Poyo Fast. Same model (veo3.1-fast), different infra.

Anchor: catbox URL (KIE host is rate-limited, catbox is reliable).
Poyo frame mode requires EXACTLY 2 image URLs — pass same URL twice.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import generate_veo as poyo_generate_veo, download as poyo_download, upload_file as poyo_upload
from jdc_news_solo_pair_nomic import INTERVIEWEE_ANCHOR

OUT = Path("outputs/illinois_jdc_news_eltracks/solo/interviewee_yeah_poyo.mp4")

# SHORTER dialogue ("Yeah, I did") + minimal prompt — softened to pass moderation
# after 4 fails on "I didn't know that was even an option" line.
INTERVIEWEE_PROMPT = """\
CHARACTER (ONE PERSON IN FRAME):

Younger man, medium-dark skin tone, mid 20s. Short freeform twists with
high temple-fade taper. Small gold stud earring in left ear. Faint chin-strap
goatee. Wearing a tan-camel corduroy trucker jacket with cream sherpa-collar
lining over a charcoal-grey zip hoodie. Body angled 3/4 toward camera, face
clearly visible. Tight head-and-shoulders framing. Hands not in frame. NO
microphone, NO equipment visible.

SETTING: under elevated train tracks downtown. Steel girder elements faintly
visible. Brick buildings in soft-focus deep background. Overcast daylight,
cool palette. Shallow DOF — subject sharp, background blurred.

CAMERA: ENG handheld documentary close-up, eye-level, locked camera with
subtle breathing float. NO cuts, NO zoom, NO shake. Smooth.

ACTION: He gives a brief honest answer. Mouth moves, jaw articulates the
two words. Calm, direct delivery. Looking slightly off-camera-left.

VOICE: Mid-20s adult male, casual conversational register, slightly higher
pitch than a middle-aged voice.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO repetition.
STOP after final word "did".

SPOKEN DIALOGUE (verbatim, stop after final word):
"Yeah, I did."

After "did", clip continues in silence with him holding position.

NO on-screen text, NO captions, NO chyrons, NO watermarks.
"""

print(f"Uploading anchor to Poyo storage: {INTERVIEWEE_ANCHOR.name}", flush=True)
url = poyo_upload(str(INTERVIEWEE_ANCHOR))
print(f"  poyo: {url}", flush=True)
print(f"Prompt length: {len(INTERVIEWEE_PROMPT)} chars", flush=True)

print("Submitting to Poyo Veo 3.1 Fast (veo3.1-fast, 720p)...", flush=True)
r = poyo_generate_veo(
    prompt=INTERVIEWEE_PROMPT,
    image_urls=[url, url],
    aspect_ratio="9:16",
    resolution="720p",
    generation_type="frame",
)

if r["status"] != "success" or not r.get("urls"):
    print(f"FAILED: {str(r.get('raw'))[:500]}", flush=True)
else:
    print(f"Downloading: {r['urls'][0]}", flush=True)
    poyo_download(r["urls"][0], str(OUT))
    print(f"DONE → {OUT}", flush=True)
