"""Re-roll all 5 persona tests with per-persona DISTINCT voice descriptions.

Original batch had uniform VOICE clause → all 4 personas sounded similar.
This batch uses a unique voice profile per persona to give Veo's TTS a
different target for each.

Same safe line + same audio-loud prompt clause as before.

Output: outputs/illinois_jdc_ugc/clips/persona{NN}_v2.mp4
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

# (anchor_path, character_setting, voice_profile)
PERSONAS = {
    "persona_02": (
        PERSONAS_DIR / "persona_02_westside_alley.png",
        "A young man, late teens / 19, standing in a narrow alley between brick "
        "buildings on the West Side of Chicago. Short box braids pulled back, "
        "faint mustache stubble. Wearing a black quilted puffer jacket over a "
        "grey hoodie. Cool overcast late-afternoon light. Background: brick walls, "
        "dumpster, soft natural fall-off.",
        # Voice: younger, rougher edge, slightly faster
        "YOUNGER late-teens male voice (~19), light tenor / slightly higher pitch "
        "(~145-160 Hz), faster casual cadence, slightly rougher edge, hint of "
        "Chicago AAVE inflection, NOT polished, NOT mature. Sounds like an actual "
        "19-year-old, almost street-casual delivery.",
    ),
    "persona_06": (
        PERSONAS_DIR / "persona_06_residential_block_porch.png",
        "A young man, mid 20s, sitting on the wooden porch railing of a frame "
        "house on a Chicago residential block. Locs pulled into a low ponytail, "
        "faint goatee. Wearing a rust-orange knit beanie + cream cable-knit "
        "sweater + dark blue jeans. Golden-hour late-afternoon sun softly raking "
        "across his face.",
        # Voice: warmer mid-range, steady, slightly melodic
        "WARMER mid-range male voice (~25), smooth steady cadence, slightly "
        "melodic / musical inflection, low-medium pitch (~125-140 Hz). Sounds "
        "like a reflective, soft-spoken neighborhood guy who's seen some things. "
        "Calm, deliberate, almost gentle.",
    ),
    "persona_07": (
        PERSONAS_DIR / "persona_07_park_bench_humboldt.png",
        "A young man, early 20s, sitting on a concrete park bench in a Chicago "
        "neighborhood park. Bald fade haircut, full short beard, small gold hoop "
        "in his left ear. Wearing a dark grey Champion-style hooded sweatshirt "
        "under an unbuttoned denim trucker jacket. Bare-branched trees and "
        "soft-focus grass behind him. Cool overcast afternoon daylight.",
        # Voice: deeper baritone, slower deliberate
        "DEEPER baritone male voice (~24), slower more deliberate cadence, "
        "lower pitch (~100-115 Hz), measured weighted delivery. Sounds mature "
        "for his age, like he chooses his words carefully. Gravelly low register.",
    ),
    "persona_08": (
        PERSONAS_DIR / "persona_08_chicago_bus_stop.png",
        "A young man, late teens / 19, standing at a Chicago CTA bus stop. Short "
        "freeform twists, faint mustache stubble. Wearing a faded brown "
        "carhartt-style work jacket over a heather grey crewneck sweatshirt. "
        "Backpack strap visible on shoulder. Overcast afternoon light. "
        "Background: out-of-focus blue bus stop sign + street with parked cars.",
        # Voice: lighter tenor, slightly higher pitch, more tentative
        "LIGHT tenor male voice (~20), higher pitch (~150-165 Hz), slightly "
        "tentative / softer delivery, more polite student-y cadence. Sounds "
        "younger and less weathered than the others — like a community-college "
        "kid riding the bus.",
    ),
    "persona_09": (
        PERSONAS_DIR / "persona_09_chicago_basketball_court.png",
        "A young man, early 20s, standing on an outdoor concrete basketball court "
        "in a Chicago neighborhood, chain-link fence behind him soft-focus, "
        "faded painted court lines on the ground. Short twists with a high taper "
        "fade, faint goatee. Wearing a grey hooded sweatshirt with the hood up, "
        "gold chain visible at collar. Late-afternoon overcast daylight.",
        # Voice: calm low monotone, almost flat
        "CALM low-pitched male voice (~23), slower monotone delivery, almost "
        "flat affect, low pitch (~105-120 Hz). Sounds guarded, like he's keeping "
        "his cards close. Slight hood-effect — voice slightly muffled as if "
        "hood is up around his ears.",
    ),
}

DIALOGUE = "It's been a long day, but I'm doing alright."


def build_prompt(char_setting, voice_profile):
    return f"""\
{char_setting}

Tight head-and-upper-chest UGC selfie / handheld phone framing, eye-level,
9:16 vertical. He looks directly at the camera (the phone he's holding) and
speaks naturally to the lens. Photoreal, NOT studio, NOT cinematic. Visible
pores, fine skin texture, no makeup, no retouching. Single continuous locked
phone-camera take, very subtle breathing-only float, NO cuts, NO zoom.

His face stays IDENTICAL throughout the 8 seconds. No morphing, no drift.

VOICE PROFILE (critical — Veo TTS must match this specific voice):
{voice_profile}

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational projection,
like he's speaking right into the phone's microphone. NOT whispered, NOT
muttered, NOT soft. Clean clear broadcast-quality audio that fills the
foreground.

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like, you know). NO trailing
words. NO additions. NO repetition. STOP after final word "alright".

SPOKEN DIALOGUE (verbatim, stop after final word):
"{DIALOGUE}"

After "alright" he holds his expression with a small natural breath. NO
further words.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO watermarks.
"""


def submit_one(slug, anchor_path, char_setting, voice_profile):
    out = OUT_DIR / f"{slug}_v2.mp4"
    print(f"[{slug}] uploading anchor", flush=True)
    url = poyo_upload(str(anchor_path))
    prompt = build_prompt(char_setting, voice_profile)
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
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(submit_one, s, a, c, v): s for s, (a, c, v) in PERSONAS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
