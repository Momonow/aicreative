"""3 variants of clip 2b with more dynamic emotion + natural facial movement.

User wants the v2 base (gradient lift energy) but with LIVELIER face — less
static, more micro-expressions, more natural human movement.

Three different direction angles:
  A — VULNERABLE DRIFT: eyes flick down on "sexually... I mean... compensation",
      slight throat-clearing breath, small lip purse before "significant",
      brief return to camera at "people who went through it"
  B — CONTEMPLATIVE BUILD: slight head tilt, eyebrows raise faintly on
      "significant potential compensation" (small hopeful surprise),
      slight nod on "to people who went through it"
  C — MICRO-EXPRESSIVE: small glance away then back at "Illinois", soft
      half-smile flicker on "compensation" (not joy — disbelief), eyes
      water-glisten slightly without crying

Same dialogue + pace lock. Same anchor (already in KIE storage).
All on KIE Veo 3.1 Lite 720p, parallel.

Output: outputs/illinois_jdc_ugc/clips/p08_clip2b_dyn_{a,b,c}.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download

ANCHOR = Path("outputs/illinois_jdc_ugc/anchors_lite720/clip2b_anchor_at_4.5s.jpg")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")

DIALOGUE = "Just found out Illinois is paying out significant potential compensation to people who went through it."

COMMON = """\
Tight head-and-upper-chest UGC selfie / handheld phone framing, eye-level,
9:16 vertical. He looks directly at the camera (the phone he's holding) and
speaks naturally to the lens. Photoreal, NOT studio, NOT cinematic. Visible
pores, fine skin texture, no makeup, no retouching, no filter. Single
continuous locked phone-camera take, very subtle breathing-only float, NO
cuts, NO zoom.

Same young man as before — late teens / 19, short freeform twists, faint
mustache stubble, faded brown carhartt-style work jacket over heather grey
crewneck. His face stays IDENTICAL throughout the 8 seconds. No morphing,
no drift.

VOICE PROFILE: Late-teens male voice (~19-20), light tenor (~140-160 Hz),
slightly soft. Honest unrehearsed delivery, like a real young guy.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection,
NOT whispered, NOT muttered. Broadcast-quality audio.

PACE LOCK: ~2.4 words per second. Slow, deliberate, each word given weight.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""

DLG_BLOCK = f"""
DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "it".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{DIALOGUE}"

After "it" he holds his expression, small natural breath. NO further words.
"""

PROMPT_A = COMMON + """
EMOTIONAL REGISTER — VULNERABLE DRIFT:

He's still processing what he just said. As he delivers this line, his face
shows quiet vulnerability. Specifically:
- On the opening "Just found out" his eyes flick briefly DOWNWARD then
  return to camera — a small "still can't believe it" beat.
- A soft throat-clearing breath happens naturally between "out" and
  "Illinois" (tiny pause).
- His lips press together briefly before "significant" — a small lip-purse
  conveying the weight of the word.
- On "to people who went through it" his eyes return to camera and hold
  steady — gentle eye contact, small subtle blink.
- Throughout: quiet voice, soft delivery, gradual very-slight energy lift.
  Honest natural micro-expressions, NOT performed.
""" + DLG_BLOCK

PROMPT_B = COMMON + """
EMOTIONAL REGISTER — CONTEMPLATIVE BUILD:

He's sharing news that's slowly sinking in for him. As he delivers this
line, his face shows quiet contemplative emotion. Specifically:
- A slight head tilt to the right on "Just found out" — like he's still
  taking it in himself.
- His eyebrows raise faintly (not surprised, just acknowledging weight)
  on "significant potential compensation" — small hopeful awareness beat.
- A small barely-perceptible nod on "to people who went through it" — a
  silent affirmation, like "yeah, people like me."
- Throughout: quiet voice, gradual very-slight energy lift. Eyebrows and
  head do soft natural micro-motion. Lips slightly mobile.
""" + DLG_BLOCK

PROMPT_C = COMMON + """
EMOTIONAL REGISTER — MICRO-EXPRESSIVE:

He's processing complex emotion as he speaks. As he delivers this line,
his face shows subtle natural micro-expressions. Specifically:
- A small glance off-camera-left then back to camera on "Illinois" — like
  recalling something.
- A soft half-smile flicker (not joy — disbelief / "can you believe it")
  on "compensation" — barely there, gone in a half-second.
- His eyes get a faint glassy quality on "people who went through it" —
  emotion without crying.
- A natural slow blink between "people" and "who".
- Throughout: quiet voice, gradual very-slight energy lift. Face has small
  natural motion — NOT static, NOT stiff. Reads as a real person
  emotionally engaged with what he's saying.
""" + DLG_BLOCK

CLIPS = [
    ("dyn_a", PROMPT_A, OUT_DIR / "p08_clip2b_dyn_a.mp4"),
    ("dyn_b", PROMPT_B, OUT_DIR / "p08_clip2b_dyn_b.mp4"),
    ("dyn_c", PROMPT_C, OUT_DIR / "p08_clip2b_dyn_c.mp4"),
]


def submit_one(slug, prompt, out_path):
    print(f"[{slug}] uploading to KIE storage", flush=True)
    url = kie_upload(str(ANCHOR))
    print(f"[{slug}] url: {url}", flush=True)
    print(f"[{slug}] submitting (prompt {len(prompt)} chars)", flush=True)
    r = kie_generate_veo(
        prompt=prompt,
        aspect_ratio="9:16",
        image_urls=[url, url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_lite",
        resolution="720p",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    kie_download(r["urls"][0], str(out_path))
    return slug, "success", str(out_path)


def main():
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(submit_one, s, p, o): s for s, p, o in CLIPS}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
