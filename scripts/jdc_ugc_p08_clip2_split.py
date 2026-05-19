"""Split clip 2 into 2 pieces with overlapping 'Just found out' for smooth pace.

Clip 2a (15 words, ~6s slow pace):
  "A guard sexually abused me. I held it in for years. Just found out."

Clip 2b (16 words, ~6.5s slow pace):
  "Just found out Illinois is paying out significant potential compensation
   to people who went through it."

Overlap = "Just found out" (3 words). At stitch time: keep clip 2a fully,
splice clip 2b starting AFTER its "Just found out" → final delivers all 28
words at consistent slow ~2.4 words/sec pace.

Anchors: 2 fresh frames from clip 1 (1.5s, 4.5s — unused timestamps).
Poyo Veo Fast 720p, Poyo storage upload.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import upload_file as poyo_upload, generate_veo as poyo_generate_veo, download as poyo_download

CLIP1 = Path("outputs/illinois_jdc_ugc/clips/p08_clip1.mp4")
ANCHOR_DIR = Path("outputs/illinois_jdc_ugc/anchors")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")

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
slightly soft and tentative. Honest unrehearsed delivery, like a real young
guy on the street.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational projection,
like he's speaking right into the phone's microphone. NOT whispered, NOT
muttered, NOT soft. Clean clear broadcast-quality audio that fills the
foreground.

PACE LOCK: Speaks SLOWLY and DELIBERATELY at approximately 2.4 words per
second. Pauses naturally between clauses. Each sentence is given weight.
NOT rushed. Matches the slow heavy pace of someone disclosing something
personal in a quiet moment.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""

CLIP2A_DIALOGUE = "A guard sexually abused me. I held it in for years. Just found out."
CLIP2A_PROMPT = COMMON + f"""
EMOTIONAL REGISTER: Heavy disclosure. Quiet, honest, almost flat. He says
the first sentence then a slight pause. The "Just found out." at the end is
him beginning to pivot toward giving information — voice lifts slightly
into the next thought (which will be the next clip).

PRONUNCIATION:
- "Illinois" not used here — clip 2b only.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "out".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{CLIP2A_DIALOGUE}"

After "out" he holds his expression, small natural breath. NO further words.
"""

CLIP2B_DIALOGUE = (
    "Just found out Illinois is paying out significant potential "
    "compensation to people who went through it."
)
CLIP2B_PROMPT = COMMON + f"""
EMOTIONAL REGISTER — CRITICAL: SAME ENERGY AS THE PREVIOUS CLIP, NO LIFT.

This clip MUST sound like it's a direct continuation of the prior heavy
disclosure beat ("A guard sexually abused me. I held it in for years.
Just found out."). Same quiet vulnerable subdued tone from START to FINISH.
NO energy increase. NO mood shift. NO informational pivot. Same person,
same moment, same weight, same volume, same soft voice — throughout the
entire clip.

He's STILL processing what he just disclosed. He's sharing this
information in the same quiet honest way he just admitted what happened.
NO "now I'm telling you the good news" energy. NO dawning hope. NO upbeat
turn. NO news-anchor delivery. NO salesy register.

Think of the entire sentence as if it's delivered as a quiet exhale —
heavy, slow, almost flat affect. Like he's saying it because he has to,
not because he's excited about it. Eyes still downcast or focused away,
NOT lit up. Voice STAYS soft throughout — same volume as the previous
clip's "Just found out."

ABSOLUTELY AVOID:
- Any volume increase mid-sentence
- Any pitch lift / brightness
- Informational announcement tone
- Excited / hopeful / salesy energy
- Faster pace toward end of sentence
- News-anchor delivery

He sounds the same at the FINAL word "it" as he did at the FIRST word
"Just" — same subdued register, same heavy quiet tone.

PRONUNCIATION:
- "Illinois" = "ill-i-NOY" (silent final 's')

PACE LOCK: ~2.4 words per second (matches clip 1 and clip 2a). Slow,
deliberate, each word given weight. NO acceleration.

DIALOGUE LOCK: ENGLISH only. NO fillers. NO trailing words. NO additions.
NO repetition. STOP after final word "it".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{CLIP2B_DIALOGUE}"

After "it" he holds his expression, small natural breath, eyes still
downcast/heavy. NO further words.
"""

CLIPS = [
    ("clip2a", 1.5, CLIP2A_PROMPT, OUT_DIR / "p08_clip2a_poyo.mp4"),
    ("clip2b", 4.5, CLIP2B_PROMPT, OUT_DIR / "p08_clip2b_poyo.mp4"),
]


def extract_frame(timestamp, dst):
    cmd = ["ffmpeg", "-y", "-ss", str(timestamp), "-i", str(CLIP1),
           "-frames:v", "1", "-q:v", "2", str(dst)]
    subprocess.run(cmd, capture_output=True, text=True, check=True)


def submit_one(slug, ts, prompt, out_path):
    anchor_jpg = ANCHOR_DIR / f"{slug}_anchor_at_{ts}s.jpg"
    print(f"[{slug}] extracting frame at {ts}s from clip 1", flush=True)
    extract_frame(ts, anchor_jpg)
    print(f"[{slug}] uploading to Poyo storage", flush=True)
    url = poyo_upload(str(anchor_jpg))
    print(f"[{slug}] url: {url}", flush=True)
    print(f"[{slug}] submitting (prompt {len(prompt)} chars)", flush=True)
    r = poyo_generate_veo(
        prompt=prompt,
        image_urls=[url, url],
        aspect_ratio="9:16",
        resolution="720p",
        generation_type="frame",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    poyo_download(r["urls"][0], str(out_path))
    return slug, "success", str(out_path)


def main():
    with ThreadPoolExecutor(max_workers=2) as ex:
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
