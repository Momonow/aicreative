"""Test personas 02, 06, 08, 09 with the same safe line via KIE Veo 3.1 Lite.

Each persona uses its OWN anchor URL (different upload), submitted in parallel
(safe — different URLs don't trip per-URL rate limits like same-URL parallel
hits did).

Audio prompt clause included (proven on p07 test — got -17.6 LUFS vs prior
clips at -25.5 LUFS).

Sentence: "It's been a long day, but I'm doing alright." (safe, neutral)

Output: outputs/illinois_jdc_ugc/clips/persona{NN}_test.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from poyo_client import upload_file as poyo_upload
from kie_client import generate_veo as kie_generate_veo, download as kie_download

PERSONAS_DIR = Path("outputs/illinois_jdc_ugc/personas")
OUT_DIR = Path("outputs/illinois_jdc_ugc/clips")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PERSONAS = {
    "persona_02": (
        PERSONAS_DIR / "persona_02_westside_alley.png",
        "A young man, late teens / 19, standing in a narrow alley between brick "
        "buildings on the West Side of Chicago. Short box braids pulled back, "
        "faint mustache stubble. Wearing a black quilted puffer jacket over a "
        "grey hoodie. Cool overcast late-afternoon light. Background: brick walls, "
        "dumpster, soft natural fall-off.",
    ),
    "persona_06": (
        PERSONAS_DIR / "persona_06_residential_block_porch.png",
        "A young man, mid 20s, sitting on the wooden porch railing of a frame "
        "house on a Chicago residential block. Locs pulled into a low ponytail, "
        "faint goatee. Wearing a rust-orange knit beanie + cream cable-knit "
        "sweater + dark blue jeans. Golden-hour late-afternoon sun softly raking "
        "across his face.",
    ),
    "persona_08": (
        PERSONAS_DIR / "persona_08_chicago_bus_stop.png",
        "A young man, late teens / 19, standing at a Chicago CTA bus stop. Short "
        "freeform twists, faint mustache stubble. Wearing a faded brown "
        "carhartt-style work jacket over a heather grey crewneck sweatshirt. "
        "Backpack strap visible on shoulder. Overcast afternoon light. "
        "Background: out-of-focus blue bus stop sign + street with parked cars.",
    ),
    "persona_09": (
        PERSONAS_DIR / "persona_09_chicago_basketball_court.png",
        "A young man, early 20s, standing on an outdoor concrete basketball court "
        "in a Chicago neighborhood, chain-link fence behind him soft-focus, "
        "faded painted court lines on the ground. Short twists with a high taper "
        "fade, faint goatee. Wearing a grey hooded sweatshirt with the hood up, "
        "gold chain visible at collar. Late-afternoon overcast daylight.",
    ),
}

DIALOGUE = "It's been a long day, but I'm doing alright."

PROMPT_TEMPLATE = """\
{character_setting}

Tight head-and-upper-chest UGC selfie / handheld phone framing, eye-level,
9:16 vertical. He looks directly at the camera (the phone he's holding) and
speaks naturally to the lens. Photoreal, NOT studio, NOT cinematic. Visible
pores, fine skin texture, no makeup, no retouching. Single continuous locked
phone-camera take, very subtle breathing-only float, NO cuts, NO zoom.

His face stays IDENTICAL throughout the 8 seconds. No morphing, no identity
drift.

VOICE: mid-20s adult male, casual conversational register, calm tone.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational projection,
like he's speaking right into the phone's microphone. NOT whispered, NOT
muttered, NOT soft. Clean clear broadcast-quality audio that fills the
foreground.

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know). NO trailing
words. NO additions. NO repetition. STOP after final word "alright".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{dialogue}"

After "alright" he holds his expression with a small natural breath. NO
further words.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""


def submit_one(slug, anchor_path, char_setting):
    out = OUT_DIR / f"{slug}_test.mp4"
    print(f"[{slug}] uploading anchor", flush=True)
    url = poyo_upload(str(anchor_path))
    print(f"[{slug}] url: {url}", flush=True)
    prompt = PROMPT_TEMPLATE.format(character_setting=char_setting, dialogue=DIALOGUE)
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
    kie_download(r["urls"][0], str(out))
    return slug, "success", str(out)


def main():
    # Parallel with max_workers=2 (safer for KIE rate-limit)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(submit_one, s, a, c): s for s, (a, c) in PERSONAS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
