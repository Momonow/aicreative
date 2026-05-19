"""IL JDC UGC ad — CLIPS 2, 3, 4 (Script B, persona 08).

Anchor rotation: extract 3 clean frames from clip 1 at varied pause moments
(0.7s, 3.0s, 6.0s) and use a different one for each clip 2-4. Per CLAUDE.md
anchor rotation rule — avoids templated identical-anchor look.

Provider rule (NEW memory): KIE generators must fetch KIE-hosted URLs.
Uploads via kie_client.upload_file (timestamped tempfile.redpandaai.co).

Dialogue:
  CLIP 2: "A guard sexually abused me. I held it in for years. Just found out
          Illinois is paying out significant potential compensation to people
          who went through it."
  CLIP 3: "Lawyers come to you. Whole thing's confidential. They don't blast
          your business."
  CLIP 4: "Free two-minute quiz to see if you qualify. Y'all gotta know about
          this."

KIE Veo 3.1 Lite, 1080p, 9:16, FIRST_AND_LAST_FRAMES_2_VIDEO.
Parallel submission (different anchor URLs per clip = no per-URL rate-limit).

Output: outputs/illinois_jdc_ugc/clips/p08_clip{2,3,4}.mp4
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file as kie_upload, generate_veo as kie_generate_veo, download as kie_download

CLIP1 = Path("outputs/illinois_jdc_ugc/clips/p08_clip1.mp4")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")
ANCHOR_DIR = Path("outputs/illinois_jdc_ugc/anchors")
ANCHOR_DIR.mkdir(parents=True, exist_ok=True)

# Common framing/voice/audio cues — shared across clips 2/3/4
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
slightly soft and tentative — but NOT mumbled. Honest unrehearsed delivery,
like a real young guy on the street, NOT an actor.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational projection,
like he's speaking right into the phone's microphone. NOT whispered, NOT
muttered, NOT soft. Clean clear broadcast-quality audio that fills the
foreground.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""

CLIP2_DIALOGUE = (
    "A guard sexually abused me. I held it in for years. Just found out "
    "Illinois is paying out significant potential compensation to people "
    "who went through it."
)
CLIP2_PROMPT = COMMON + f"""
EMOTIONAL REGISTER: He delivers the heaviest line. Quiet, honest, almost
flat affect — like he's said it out loud for the first time. Slight pause
between "years" and "Just found out" — the shift from disclosure to
information. Eyes hold camera, slight downward flicker on "sexually abused
me", then return.

PRONUNCIATION:
- "Illinois" = "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know). NO
trailing words. NO additions. NO repetition. STOP after final word "it".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{CLIP2_DIALOGUE}"

After "it" he holds his expression, small natural breath. NO further words.
"""

CLIP3_DIALOGUE = (
    "Lawyers come to you. Whole thing's confidential. They don't blast "
    "your business."
)
CLIP3_PROMPT = COMMON + f"""
EMOTIONAL REGISTER: Slightly more steady — practical informational mode.
He's reassuring the viewer. Eyebrows neutral, eyes hold camera.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "business".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{CLIP3_DIALOGUE}"

After "business" he holds his expression, small natural breath. NO further
words.
"""

CLIP4_DIALOGUE = (
    "Free two-minute quiz to see if you qualify. Y'all gotta know about this."
)
CLIP4_PROMPT = COMMON + f"""
EMOTIONAL REGISTER — CRITICAL: NEVER COMMERCIAL. SAME QUIET TONE AS THE
DISCLOSURE BEATS.

THE OPENING WORDS "Free two-minute quiz" MUST NOT be delivered with any
commercial inflection. Specifically:
- NO emphasis on the word "Free" — say it flat, like any other word
- NO enthusiasm on "two-minute quiz" — say it like a quiet aside
- NO rising inflection / upbeat / pitch lift on the opening
- NO "spokesperson clarity" / NO TV-ad voice
- NO smile in the voice

He sounds EXACTLY the same here as he did when he said "A guard sexually
abused me" — same soft, subdued, heavy voice. Same volume. Same vulnerable
register. Same slow deliberate pace.

Think of it this way: he's NOT urging anyone, NOT selling, NOT pitching.
He's just CONTINUING to share quietly. A friend telling another friend
"hey, there's this thing you can do — y'all gotta know." Almost
muttered. Almost reluctant. Heavy and personal.

The line should feel like a SAD AFTERTHOUGHT, not a call-to-action. Imagine
him having just told the prior heavy disclosure — and now adding this last
quiet piece of info before he stops talking. NO LIFT INTO ENTHUSIASM.

"Y'all gotta know about this" is the same — quiet, matter-of-fact, almost
under his breath. NOT pleading, NOT pitching, NOT urging. Just saying it
because it's true.

ABSOLUTELY AVOID:
- ANY commercial / advertising inflection on opening words
- Emphasis on "Free", "two-minute", "quiz", "qualify"
- Pitch lift on the CTA line
- Volume increase anywhere in this clip
- Upbeat closing
- Sales delivery / spokesperson voice
- Smile in the voice
- "Tap the button" energy

He sounds the same at the FINAL word "this" as he did at the FIRST word
"Free" — same subdued heavy honest register. As quiet as everything else
he's said.

PACE LOCK: ~2.4 words per second. Slow, deliberate, each word given equal
weight. NO acceleration through CTA words.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "this".

SPOKEN DIALOGUE (verbatim, stop after final word — delivered quietly,
flatly, without commercial inflection):
"{CLIP4_DIALOGUE}"

After "this" he holds his expression briefly, small natural breath. Eyes
still on camera with the same quiet honesty. NO further words.
"""

CLIPS = [
    ("clip2", 0.7, CLIP2_PROMPT, OUT_DIR / "p08_clip2.mp4"),
    ("clip3", 3.0, CLIP3_PROMPT, OUT_DIR / "p08_clip3.mp4"),
    ("clip4", 6.0, CLIP4_PROMPT, OUT_DIR / "p08_clip4.mp4"),
]


def extract_frame(timestamp, dst):
    cmd = ["ffmpeg", "-y", "-ss", str(timestamp), "-i", str(CLIP1),
           "-frames:v", "1", "-q:v", "2", str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Frame extract failed: {r.stderr[-200:]}")


def submit_one(slug, ts, prompt, out_path):
    anchor_jpg = ANCHOR_DIR / f"{slug}_anchor_at_{ts}s.jpg"
    print(f"[{slug}] extracting frame at {ts}s from clip 1", flush=True)
    extract_frame(ts, anchor_jpg)
    print(f"[{slug}] uploading to KIE storage", flush=True)
    url = kie_upload(str(anchor_jpg))
    print(f"[{slug}] url: {url}", flush=True)
    print(f"[{slug}] submitting (prompt {len(prompt)} chars)", flush=True)
    r = kie_generate_veo(
        prompt=prompt,
        aspect_ratio="9:16",
        image_urls=[url, url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_lite",
        resolution="1080p",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    kie_download(r["urls"][0], str(out_path))
    return slug, "success", str(out_path)


def main():
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(submit_one, s, ts, p, o): s for s, ts, p, o in CLIPS}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
