"""IL JDC UGC ad — CLIP 1 (Script B, persona 08).

Dialogue (REPORTER would be wrong term — this is persona 08 himself, a young
guy doing UGC selfie disclosure):
  "I was at Saint Charles when I was fifteen. Never told nobody what
  happened up there."

8s, KIE Veo 3.1 Lite, 1080p, 9:16. Persona 08 anchor (CTA bus stop, twists,
carhartt, light tenor voice).

Output: outputs/illinois_jdc_ugc/clips/p08_clip1.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import upload_file as poyo_upload
from kie_client import generate_veo as kie_generate_veo, download as kie_download

ANCHOR = Path("outputs/illinois_jdc_ugc/personas/persona_08_chicago_bus_stop.png")
OUT = Path("outputs/illinois_jdc_ugc/clips/p08_clip1.mp4")

PROMPT = """\
A young man, late teens / 19, standing at a Chicago CTA bus stop. Short
freeform twists, faint mustache stubble. Wearing a faded brown carhartt-
style work jacket over a heather grey crewneck sweatshirt. Backpack strap
visible on shoulder. Overcast afternoon light. Background: out-of-focus
blue bus stop sign + street with parked cars.

Tight head-and-upper-chest UGC selfie / handheld phone framing, eye-level,
9:16 vertical. He looks directly at the camera (the phone he's holding) and
speaks naturally to the lens. Photoreal, NOT studio, NOT cinematic. Visible
pores, fine skin texture, no makeup, no retouching, no filter. Single
continuous locked phone-camera take, very subtle breathing-only float, NO
cuts, NO zoom.

His face stays IDENTICAL throughout the 8 seconds — same twists, jawline,
eye position, skin tone. No morphing, no drift.

EMOTIONAL REGISTER: Quiet, honest, slightly vulnerable. He's not
performing. He's sharing something heavy in a private moment to the
camera. Mouth softer, eyes more downcast on "never told nobody". Pace is
slow and deliberate — like he's choosing every word.

VOICE PROFILE: Late-teens male voice (~19-20), light tenor (~140-160 Hz),
slightly soft and tentative — but NOT mumbled. Honest unrehearsed
delivery, like a real young guy on the street, NOT an actor.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational
projection, like he's speaking right into the phone's microphone. NOT
whispered, NOT muttered, NOT distant. Clean clear broadcast-quality audio
that fills the foreground.

PRONUNCIATION LOCK:
- "Saint Charles" = full word "Saint" (NOT abbreviated).
- "fifteen" = clean "fif-teen" (NOT "fiteen", NOT "fivteen").

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know, so). NO
trailing words. NO additions. NO repetition. STOP after final word "there".

SPOKEN DIALOGUE (verbatim, stop after final word):
"I was at Saint Charles when I was fifteen. Never told nobody what happened up there."

After "there" he holds his expression — natural small breath, eyes still
on camera, slight head tilt down. NO further words.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""


def main():
    print(f"Uploading anchor: {ANCHOR.name}", flush=True)
    url = poyo_upload(str(ANCHOR))
    print(f"  url: {url}", flush=True)
    print(f"Prompt length: {len(PROMPT)} chars", flush=True)
    print(f"Submitting to KIE Veo 3.1 Lite (1080p, FIRST_AND_LAST_FRAMES)…", flush=True)
    r = kie_generate_veo(
        prompt=PROMPT,
        aspect_ratio="9:16",
        image_urls=[url, url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_lite",
        resolution="1080p",
    )
    if r["status"] != "success" or not r.get("urls"):
        print(f"FAILED: {str(r.get('raw'))[:500]}", flush=True)
        return
    print(f"Downloading: {r['urls'][0]}", flush=True)
    kie_download(r["urls"][0], str(OUT))
    print(f"DONE → {OUT}", flush=True)


if __name__ == "__main__":
    main()
