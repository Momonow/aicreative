"""Emotion audition for b14: 3 takes of the hook clip with different sad/sobbing voice.
KIE veo3_lite, FIRST_AND_LAST_FRAMES from the bed_b14 host image.
Output: outputs/illinois_jdc_storytime_e_b14/emotion_test/hook_<emo>.mp4
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
GAZE: {gaze} Warm dark-brown eyes, OPEN, staying the SAME color throughout.
BODY: {body}
VOICE: {voice}
TONE: {tone}
SPEED: {speed}
AUDIO CRITICAL: he speaks THROUGH the emotion but stays clearly audible and intelligible at a close intimate volume right into the phone mic. The crying does NOT make him inaudible or mumbled.
PRONUNCIATION: say "SA'ed" as the spoken letters "ess-ay-d" (S then A then a d), NOT "sad", NOT "essayed". "juvie" = "JOO-vee". "Illinois" = "ill-uh-NOY".
DIALOGUE LOCK: English only. Say ONLY the words in SPOKEN DIALOGUE, in order. No fillers, no extra or trailing words, no repetition. Crying sounds (a sniffle, a shaky breath, a catch in the throat) are allowed BETWEEN words but add NO words. Stop after the final word "it".
NO on-screen text, NO captions, NO subtitles, NO watermark.
SPOKEN DIALOGUE (verbatim, stop after final word): "{LINE}\""""

TAKES = {
    "sob": P(
        "glassy eyes brimming with tears, looking into the phone then down as it overwhelms him, then back.",
        "tears spilling over, sniffles, lips trembling, jaw tight, a shaky breath before he starts.",
        "choked and breaking, actively crying — a catch in the throat, words wavering and pushed out through tears, sniffling between phrases.",
        "raw open grief, barely holding himself together.",
        "slow and halting, about 2 words per second with small broken pauses."),
    "sad": P(
        "heavy wet eyes, mostly cast down, lifting to the lens now and then.",
        "slow heavy blinks, one tear sliding down, swallowing hard, very still.",
        "low, heavy and trembling, thick with held-back tears, quiet and weary, almost a whisper but still audible.",
        "deep quiet sadness, right on the verge of crying but holding it in.",
        "slow and deliberate, about 2.2 words per second."),
    "break": P(
        "starts steady on the lens, eyes welling up and drifting away as his voice breaks, then back.",
        "composed at first, then the chin quivers, a tear falls, his breath catches mid-sentence.",
        "starts quiet and composed, then the voice cracks and tightens partway through and wells up by the end.",
        "composure giving way to emotion as he speaks.",
        "starts about 2.4 words per second, slowing as it breaks."),
}


def gen(emo, prompt, url):
    out = OUT / f"hook_{emo}.mp4"
    r = generate_veo(prompt=prompt, aspect_ratio="9:16", image_urls=[url, url],
                     mode="FIRST_AND_LAST_FRAMES_2_VIDEO", model="veo3_lite", resolution="720p")
    if r.get("status") != "success" or not r.get("urls"):
        return emo, "FAILED", str(r.get("raw"))[:200]
    download(r["urls"][0], str(out))
    return emo, "success", str(out)


def main():
    url = upload_file(HOST)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(gen, e, p, url): e for e, p in TAKES.items()}
        for f in as_completed(futs):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
