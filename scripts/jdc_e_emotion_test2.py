"""Emotion audition v2 for b14 hook: 5 LOW-PITCHED takes (sobbing was too high).
All force a deep chest-voice register while varying the emotional delivery.
KIE veo3_lite, FIRST_AND_LAST_FRAMES from bed_b14. Output: emotion_test/hook_<name>.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_veo, upload_file, download

OUT = Path("outputs/illinois_jdc_storytime_e_b14/emotion_test"); OUT.mkdir(parents=True, exist_ok=True)
HOST = "outputs/illinois_jdc_storytime_bed/reference/bed_b14.png"
LINE = "A guard SA'ed me at Illinois juvie. This is my story, and how I might finally be getting compensated for it."

def P(gaze, body, voice, tone, speed):
    return f"""He is lying back in bed talking into his phone, filming a raw selfie confession.
GAZE: {gaze} Warm dark-brown eyes, OPEN, staying the SAME color throughout (no red, no bloodshot tint).
BODY: {body}
VOICE: {voice}
PITCH LOCK: keep his voice LOW, deep and masculine the whole time — a grown man's chest voice. It must NOT rise into a high or whiny pitch, even while crying or emotional. The grief comes out LOW and heavy, never high.
TONE: {tone}
SPEED: {speed}
AUDIO CRITICAL: he speaks THROUGH the emotion but stays clearly audible and intelligible at a close intimate volume into the phone mic. The crying does NOT make him inaudible or mumbled.
PRONUNCIATION: say "SA'ed" as the spoken letters "ess-ay-d" (S then A then a d), NOT "sad", NOT "essayed". "juvie" = "JOO-vee". "Illinois" = "ill-uh-NOY".
DIALOGUE LOCK: English only. Say ONLY the words in SPOKEN DIALOGUE, in order. No fillers, no extra/trailing words, no repetition. Crying sounds (a low sniffle, a shaky breath, a catch in the throat) are allowed BETWEEN words but add NO words. Stop after the final word "it".
NO on-screen text, NO captions, NO subtitles, NO watermark.
SPOKEN DIALOGUE (verbatim, stop after final word): "{LINE}\""""

TAKES = {
    "lowsob": P(
        "glassy eyes brimming, looking into the phone, dropping down as it hits him then back.",
        "tears spilling, the chest rising and falling with heavy sobs, jaw tight, a deep shaky breath first.",
        "deep, low, chest-heavy sobbing — broken and wet but staying in a LOW masculine register, heavy sobs from the chest, NOT a high whimper, sniffles and a catch in the throat between words.",
        "raw grief that comes out low and heavy.",
        "slow and halting, about 2 words per second with small broken pauses."),
    "choked": P(
        "wet eyes fixed low then flicking to the lens, blinking hard.",
        "jaw clenched, swallowing hard between phrases, a single tear, throat working.",
        "low and tight, choked up, swallowing his sobs, fighting to push each word out in a deep voice that keeps catching.",
        "barely holding it together, a man trying not to break.",
        "slow, about 2.2 words per second, words pushed out in low bursts."),
    "tremble": P(
        "heavy wet eyes mostly down, lifting slowly to the lens.",
        "lower lip quivering, slow heavy blinks, a tear sliding, very still.",
        "low and trembling, a deep voice wavering and thick with held-back tears, quiet and unsteady.",
        "deep sadness right on the edge, the voice shaking but staying low.",
        "slow and deliberate, about 2.2 words per second."),
    "numb": P(
        "flat, distant stare into the phone, eyes wet but unfocused.",
        "almost no movement, one slow tear, a blank exhausted face.",
        "low, flat and hollow, exhausted — grief gone numb, nearly monotone, heavy and quiet, deep in the chest.",
        "emptied-out, defeated, like he's said it in his head a thousand times.",
        "slow and even, about 2 words per second."),
    "whisper": P(
        "looking down and inward, glancing up to the lens, intimate.",
        "shoulders drawn in, a tear, a slow swallow, leaning slightly toward the phone.",
        "a very quiet LOW whisper, deep and intimate, broken at the edges, almost talking to himself, but still audible.",
        "fragile and private, on the verge of tears, kept low.",
        "slow and hushed, about 2 words per second."),
}


def gen(name, prompt, url):
    out = OUT / f"hook_{name}.mp4"
    r = generate_veo(prompt=prompt, aspect_ratio="9:16", image_urls=[url, url],
                     mode="FIRST_AND_LAST_FRAMES_2_VIDEO", model="veo3_lite", resolution="720p")
    if r.get("status") != "success" or not r.get("urls"):
        return name, "FAILED", str(r.get("raw"))[:200]
    download(r["urls"][0], str(out))
    return name, "success", str(out)


def main():
    only = set(sys.argv[1:])
    items = [(n, p) for n, p in TAKES.items() if not only or n in only]
    url = upload_file(HOST)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(gen, n, p, url): n for n, p in items}
        for f in as_completed(futs):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
