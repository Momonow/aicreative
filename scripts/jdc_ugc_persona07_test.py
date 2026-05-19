"""Persona 07 test — Humboldt Park bench UGC, safe neutral line, KIE Veo 3.1 Lite.

Sentence is intentionally generic (no JDC / abuse / Illinois mentions) so we
isolate whether Veo can generate this character cleanly before adding the
real campaign dialogue.

Anchor: outputs/illinois_jdc_ugc/personas/persona_07_park_bench_humboldt.png
Upload via Poyo storage (publicly accessible, no rate-limit issues).

Output: outputs/illinois_jdc_ugc/clips/persona07_test.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import upload_file as poyo_upload
from kie_client import generate_veo as kie_generate_veo, download as kie_download

ANCHOR = Path("outputs/illinois_jdc_ugc/personas/persona_07_park_bench_humboldt.png")
OUT = Path("outputs/illinois_jdc_ugc/clips/persona07_test.mp4")
OUT.parent.mkdir(parents=True, exist_ok=True)


PROMPT = """\
A young man, early 20s, sits on a concrete park bench in a Chicago
neighborhood park. He has a bald fade haircut, full short beard, and a small
gold hoop in his left ear. He's wearing a dark grey Champion-style hooded
sweatshirt under an unbuttoned denim trucker jacket. Bare-branched trees and
soft-focus grass behind him. Cool overcast afternoon daylight.

Tight head-and-upper-chest UGC selfie / handheld phone framing, eye-level,
9:16 vertical. He looks directly at the camera (the phone he's holding) and
speaks naturally to the lens. Photoreal, NOT studio, NOT cinematic. Visible
pores, fine skin texture, no makeup, no retouching. Single continuous locked
phone-camera take, very subtle breathing-only float, NO cuts, NO zoom.

His face stays IDENTICAL throughout the 8 seconds — same fade, beard,
jawline, eye position. No morphing, no identity drift.

VOICE: mid-20s adult male, casual conversational register, mature, calm tone.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational projection,
like he's speaking right into the phone's microphone. NOT whispered, NOT
muttered, NOT soft. Clean clear broadcast-quality audio that fills the
foreground.

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know). NO trailing
words. NO additions. NO repetition. STOP after final word "alright".

SPOKEN DIALOGUE (verbatim, stop after final word):
"It's been a long day, but I'm doing alright."

After "alright" he holds his expression with a small natural breath, looking
at the camera. NO further words.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""


def main():
    print(f"Uploading anchor via Poyo storage: {ANCHOR.name}", flush=True)
    url = poyo_upload(str(ANCHOR))
    print(f"  url: {url}", flush=True)
    print(f"Prompt length: {len(PROMPT)} chars", flush=True)
    print(f"Submitting to KIE Veo 3.1 Lite (1080p, FIRST_AND_LAST_FRAMES anchor)…", flush=True)
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
