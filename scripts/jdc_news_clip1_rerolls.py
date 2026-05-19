"""Re-roll clip 1 on Veo 3.1 Lite, 3 candidates in parallel.

The v3 we had passed Whisper but at ~7.0-7.5s the interviewee's mouth started
to part (likely the start of an unrendered "Yeah") + faint audio energy
(-30dBFS). Need stronger lock: interviewee mouth STAYS SEALED for ALL 8s,
ZERO audible sound from him, full silence after reporter's "up?".

Submitting 3 candidates so user can pick the cleanest.

Output: outputs/illinois_jdc_news_eltracks/clip1_v4{a,b,c}.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import upload_file, generate_veo as kie_generate_veo, download as kie_download

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks")
ANCHOR_LOCAL = OUT_DIR / "anchor" / "composite_v2.png"
ANCHOR_URL_CACHE = OUT_DIR / "clip1_anchor_url.txt"

PROMPT = """\
CHARACTERS (TWO PEOPLE IN FRAME, ONLY THE REPORTER MAKES ANY SOUND):

REPORTER (LEFT, strong LEFT-PROFILE, mid-foreground):
Man, medium-dark skin tone, late 30s. Close-cropped short black hair, full
neatly trimmed short beard, clean jawline. Unbuttoned black wool overcoat
over a charcoal-grey blazer and crisp white open-collar shirt. His RIGHT
hand holds a black handheld stick mic with thick foam windscreen and a
COMPLETELY BLANK WHITE square mic-flag (no text, no letters, no logo, no
symbols). Mic extended forward at chest height, head pointed toward the
younger man. Slightly leaning in, calm, attentive.

INTERVIEWEE (RIGHT, body 3/4 toward camera):
Younger man, medium-dark skin tone, mid 20s. Short freeform twists with high
temple-fade taper. Small gold stud earring in his LEFT ear. Faint chin-strap
goatee, light mustache stubble. Tan-camel corduroy trucker jacket with
cream sherpa-collar lining over a charcoal-grey zip hoodie. Hands at his
sides. He does NOT gesture.

SETTING:
Real daylight under the Chicago Loop elevated train tracks ('the L'). Massive
black-painted riveted steel girders and lattice beams overhead. Large steel
support column visible to the side. Polished brick and concrete sidewalk.
Granite-clad and red-brick Loop-era buildings in soft-focus deep background,
faint yellow taxi at the curb. Late-afternoon overcast daylight, cool urban
palette.

CAMERA + MOTION:
Locked TWO-SHOT, both subjects from mid-chest up. ~24mm equivalent. Single
continuous handheld take with VERY SUBTLE ~±5px breathing-only float. NO
cuts, NO zoom, NO rack focus, NO sudden movements, NO jitter, NO shake
spikes. Smooth and slow, like a real documentary cameraperson.

FACE IDENTITY LOCK:
Both characters' faces remain IDENTICAL from second 0 through second 8. Same
beard, jaw, hairline, skin tone, eye position. No morphing, no drift.

═══════════════════════════════════════════════════════════════════
CRITICAL — INTERVIEWEE MUST BE TOTALLY SILENT AND MOUTH-SEALED:

The INTERVIEWEE makes ABSOLUTELY ZERO sound for the entire 8-second clip.
- He does NOT speak. Not one word. Not one syllable.
- He does NOT breathe audibly. NO breath sounds, NO exhales, NO inhales
  through the mouth.
- His MOUTH STAYS COMPLETELY CLOSED in a soft neutral line for ALL 8
  seconds. From frame 1 to frame 192 (the final frame at 24fps × 8s),
  his lips DO NOT PART, DO NOT OPEN, DO NOT MOVE, NOT EVEN A MILLIMETER.
- He does NOT begin to say "Yeah". He does NOT begin to say "Yes". He does
  NOT begin to say anything. His mouth is COMPLETELY SEALED throughout.
- He LISTENS attentively, eyes on the reporter. He may blink naturally and
  his eyebrows may move subtly, but his MOUTH IS ABSOLUTELY MOTIONLESS.

Only ONE source of audio in this clip = the REPORTER's voice asking the
question. After "up?" the clip continues in COMPLETE SILENCE (-40dBFS or
lower) for the remaining ~1.5 seconds. NO whispers, NO breath, NO secondary
voice, NO mouth sounds from anyone.

═══════════════════════════════════════════════════════════════════

CRITICAL — ONLY THE REPORTER SPEAKS, AND ONLY THE LINE BELOW:
The REPORTER's mouth moves and articulates each word of the line. His head
turns slightly toward the interviewee as he asks. He stops speaking after
the final word "up?".

REPORTER's voice: MATURE adult male, calm, even tempo, slightly lower
register, careful broadcast articulation. Late-30s field reporter.

PRONUNCIATION:
- "Audy Home" = "AW-dee Home" (rhymes with Audi)
- "Saint Charles" = full word "Saint" (NOT abbreviated)
- "juvie" = "JOO-vee"
- "Illinois" = "ill-i-NOY" (silent final 's')

DIALOGUE LOCK: ENGLISH only. NO fillers (uh, um, like). NO trailing words.
NO additions. NO repetition. STOP after final word "up?".

SPOKEN DIALOGUE (REPORTER only, verbatim, stop after final word):
"Did you ever spend time at the Audy Home, Saint Charles, or another Illinois juvie growing up?"

After "up?", ABSOLUTE SILENCE for ~1.5s — no breath, no whisper, no second
voice. Both characters hold their positions.

ABSOLUTELY NO on-screen text, NO captions, NO subtitles, NO chyrons, NO
lower-thirds, NO station bug, NO watermarks. White mic-flag stays
COMPLETELY BLANK.
"""


def submit(slug, anchor_url):
    out = OUT_DIR / f"clip1_{slug}.mp4"
    print(f"[{slug}] Submitting (1080p)…", flush=True)
    r = kie_generate_veo(
        prompt=PROMPT,
        aspect_ratio="9:16",
        image_urls=[anchor_url, anchor_url],
        mode="FIRST_AND_LAST_FRAMES_2_VIDEO",
        model="veo3_lite",
        resolution="1080p",
    )
    if r["status"] != "success" or not r.get("urls"):
        return slug, "failed", str(r.get("raw"))[:300]
    kie_download(r["urls"][0], str(out))
    return slug, "success", str(out)


def main():
    if ANCHOR_URL_CACHE.exists():
        anchor_url = ANCHOR_URL_CACHE.read_text().strip()
    else:
        anchor_url = upload_file(str(ANCHOR_LOCAL))
        ANCHOR_URL_CACHE.write_text(anchor_url)
    print(f"Anchor URL: {anchor_url}")
    print(f"Prompt length: {len(PROMPT)} chars\n")

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(submit, s, anchor_url): s for s in ["v4a", "v4b", "v4c"]}
        for f in as_completed(futures):
            s = futures[f]
            try:
                slug, status, info = f.result()
                print(f"[{slug}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
