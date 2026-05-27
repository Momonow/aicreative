"""
Script 05-B v3 — Fix two issues from v2:
  1. Clip 2: persona smiled during "I know you never told nobody. I didn't either, for 15 years."
             → Re-roll with hard NO SMILE / heavy somber expression lock
  2. Clip 7: 30 words in 8s = 3.75 wps (too fast)
             → Split into:
               clip7_new: "The window on this is not open forever. Illinois set a deadline. I almost missed it. Don't miss it."  (~16 words, ~2.0 wps)
               clip8_new: "Tap below. Two minutes. Free. Private. You've carried this long enough."  (~11 words, slow pauses)

Uses Google Flow Veo 3.1 Lite via useapi.net.
"""
import os, sys, json, time, requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

USEAPI_TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {USEAPI_TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/il_jdc_script05_b_v2")
OUT.mkdir(exist_ok=True)

ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:a08d887a-711c-4256-bc8e-28d159ce34b6"

# ── Clip definitions ────────────────────────────────────────────────────────
CLIPS = [
    {
        "n": "2_v2",
        "duration": 8,
        "dialogue": "I know you never told nobody. I didn't either, for 15 years.",
        "prompt": """GAZE: Starts briefly downcast — weighted memory — then slowly lifts back to lens, soft and still.
BODY LANGUAGE: Heavy exhale before speaking, shoulders drop with the weight of it. Slight brow furrow. Absolutely NO smile at any point. Expression is grief-heavy, somber, the kind of stillness that comes from 15 years of carried silence.
VOICE STYLE: Quieter, intimate — same voice, lower register, almost private. Subdued.
TONE: Vulnerable, heavy confession. He is WITH the viewer — not above them, not lighter than them.
SPEED: ~1.8 words per second, unhurried — each phrase breathes. Pause between sentences.

AUDIO CRITICAL: Voice clear and audible despite soft tone. NOT inaudible — still fills the foreground.

PRONUNCIATION LOCK: "nobody" = NO-buh-dee (natural, not clipped).

CRITICAL — NO SMILE EVER: His mouth stays in a HEAVY, SAD, DOWNCAST NEUTRAL LINE throughout the entire clip. ZERO upturned corners. ZERO smile. ZERO teeth visible. ZERO warmth or lightness in the expression. This is 15 years of carried silence — pure weight, not warmth.

CRITICAL — DIALOGUE LOCK: English only, no fillers, no extra words. Speak ONLY these words in order. Stop after the final word.

SPOKEN DIALOGUE: "I know you never told nobody. I didn't either, for 15 years."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": "7_new",
        "duration": 8,
        "dialogue": "The window on this is not open forever. Illinois set a deadline. I almost missed it. Don't miss it.",
        "prompt": """GAZE: Eyes on lens throughout. Direct, focused — the look of someone who knows the clock is ticking.
BODY LANGUAGE: Very slight forward lean as urgency builds through "Don't miss it." Then holds still. Jaw set. Subdued gravity.
VOICE STYLE: Low urgency — NOT salesy, NOT energetic. Subdued gravitas. The quiet warning of someone who nearly lost their own chance.
TONE: Quiet urgency. Somber weight. Each sentence lands separately.
SPEED: ~2.0 words per second, deliberate. Each sentence has a beat of silence after it.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY at FULL conversational projection. NOT whispered. Clean foreground audio.

PRONUNCIATION LOCK: "Illinois" = ILL-ih-noy. "deadline" = DEAD-line (natural).

CRITICAL — NO SMILE EVER: Mouth stays in a firm, flat neutral line. ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only, no fillers, no extra words, no trailing words. Speak ONLY these words in order. Stop after the final word.

SPOKEN DIALOGUE: "The window on this is not open forever. Illinois set a deadline. I almost missed it. Don't miss it."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": "8_new",
        "duration": 8,
        "dialogue": "Tap below. Two minutes. Free. Private. You've carried this long enough.",
        "prompt": """GAZE: Eyes on lens, soft and still. The gentlest look in the entire video — like he is talking directly to one person.
BODY LANGUAGE: Completely still, no lean. The stillness of someone who has said everything that needed to be said. Face is calm, open, compassionate.
VOICE STYLE: Warm, low, private. The quietest clip. Like he is speaking to one person in the room, not to an audience.
TONE: Compassion. Relief. A personal favor from someone who made it through.
SPEED: ~1.5 words per second. Very slow. Each phrase has a FULL pause after it. "You've carried this long enough" — even slower, each word given its own weight.

AUDIO CRITICAL: He speaks CLEARLY AUDIBLY despite soft tone. NOT inaudible. Clean foreground audio.

CRITICAL — NO SMILE EVER: Mouth stays in a soft neutral line. ZERO upturned corners. ZERO smile. Compassion lives in the eyes, not the mouth.

CRITICAL — DIALOGUE LOCK: English only, no fillers, no extra words, no trailing words. Speak ONLY these words in order. Stop after the final word.

SPOKEN DIALOGUE: "Tap below. Two minutes. Free. Private. You've carried this long enough."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
]


# ── Generation helpers ───────────────────────────────────────────────────────
def submit_clip(clip):
    n = clip["n"]
    out_path = OUT / f"clip{n}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        print(f"  clip{n}: already exists ({out_path.stat().st_size//1024}KB), skipping")
        return n, str(out_path), "skipped"

    payload = {
        "prompt": clip["prompt"],
        "model": "veo-3.1-lite",
        "startImage": ANCHOR,
        "aspectRatio": "portrait",
        "duration": clip["duration"],
        "async": True,
        "captchaRetry": 5,
    }
    r = requests.post("https://api.useapi.net/v1/google-flow/videos",
                      headers=HEADERS, json=payload, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Submit clip{n} failed: {r.status_code} {r.text[:300]}")
    job_id = r.json().get("jobid")
    if not job_id:
        raise RuntimeError(f"clip{n} no jobid: {r.text[:300]}")
    print(f"  clip{n}: submitted → job {job_id}")
    return n, job_id, "submitted"


def poll_job(job_id, n, timeout=600, interval=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"https://api.useapi.net/v1/google-flow/jobs/{job_id}",
                         headers=HEADERS, timeout=30)
        if r.status_code != 200:
            time.sleep(interval)
            continue
        data = r.json()
        status = data.get("status", "")
        resp = data.get("response", {})

        if status == "completed":
            media = (resp.get("media") or [{}])
            video_url = media[0].get("videoUrl", "") if media else ""
            if video_url:
                return video_url
            raise RuntimeError(f"clip{n} completed but no videoUrl: {data}")
        elif status == "failed":
            raise RuntimeError(f"clip{n} FAILED: {data.get('error', data)}")
        else:
            pct = data.get("progressRatio", "?")
            eta = data.get("estimatedTimeToStartSeconds", "?")
            print(f"    clip{n}: {status} ({pct}) eta={eta}s …", flush=True)
            time.sleep(interval)
    raise TimeoutError(f"clip{n} timed out after {timeout}s")


def download_clip(url, n):
    out_path = OUT / f"clip{n}.mp4"
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(65536):
            f.write(chunk)
    size = out_path.stat().st_size
    print(f"  clip{n}: downloaded → {size//1024}KB")
    return str(out_path)


def generate_clip(clip):
    n = clip["n"]
    out_path = OUT / f"clip{n}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        print(f"  clip{n}: already exists, skipping")
        return n, str(out_path)

    _, job_id, status = submit_clip(clip)
    if status == "skipped":
        return n, str(out_path)

    video_url = poll_job(job_id, n)
    path = download_clip(video_url, n)
    return n, path


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Generating {len(CLIPS)} fix clips → {OUT}")
    print(f"  clip2_v2: re-roll (no smile lock)")
    print(f"  clip7_new: 16 words, slow urgency")
    print(f"  clip8_new: 11 words, compassionate CTA\n")

    results = {}
    # Generate sequentially to avoid rate limits (only 3 clips)
    for clip in CLIPS:
        n = clip["n"]
        try:
            n, path = generate_clip(clip)
            results[n] = path
            print(f"✓ clip{n} done: {path}")
        except Exception as e:
            print(f"✗ clip{n} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/{len(CLIPS)} fix clips")
    for n in sorted(results):
        print(f"  clip{n}: {results[n]}")
