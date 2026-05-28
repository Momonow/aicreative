"""
IL JDC Variation 5 — Persona J Forward — 8 clips × 8s
Phase 1: Generate nano-banana-pro anchor → save Google Flow mediaId
Phase 2: Generate 8 clips via useapi.net Veo 3.1 Fast, startImage = anchor mediaId
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

USEAPI_TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {USEAPI_TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/il_jdc_v5_a")
OUT.mkdir(exist_ok=True)

ANCHOR_ID_PATH = OUT / "anchor_mediaId.txt"

ANCHOR_PROMPT = """RAW phone selfie photo. Man, deep dark-brown complexion, mid-30s, lean build, short natural coils with a taper fade, clean-shaved, angular jawline. Facing directly into the front camera, body squared to the lens. Close framing — head and upper chest. Chicago suburban residential street behind him: brick ranch-style houses, a dark sedan parked at the curb, bare winter trees, dry dead autumn leaves scattered on the sidewalk, flat grey overcast sky. Heather-brown waffle-knit thermal long-sleeve, no phone in hands. Direct gaze into the lens, still serious unsmiling expression.

REALISM CRITICAL: visible skin pores on nose and cheeks, natural under-eye darkness, slight uneven skin tone, fine lines at eye corners, natural lip texture slightly dry, subtle facial asymmetry, visible follicle texture from clean shave. Front-facing camera slight wide-angle lens distortion. Slightly noisy image from phone sensor. NOT smooth, NOT retouched, NOT studio-lit.
9:16 vertical portrait."""

CLIPS = [
    {
        "n": 1,
        "prompt": """GAZE: Locked into camera from first frame. Heavy-eyed, weight of knowing behind them. Stays steady throughout.
BODY LANGUAGE: Completely still at open. Slight lean forward mid-clip on "nobody tells you." Jaw set.
VOICE STYLE: Mid-30s man, warm deep voice, Chicago cadence. Measured and deliberate.
TONE: Quiet urgency. Opening a door on something real that most people never say out loud.
SPEED: ~1.9 wps, each phrase given a breath.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection into the phone mic. NOT whispered. Clean foreground audio.

PRONUNCIATION LOCK: "Illinois" = ILL-ih-noy. "juvenile" = JOO-veh-nile.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout. Does NOT close eyes during dialogue.

CRITICAL — NO SMILE EVER: Mouth stays in a flat heavy neutral line. ZERO upturned corners.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "Here's the part nobody tells you about what happened in them Illinois juvenile spots."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 2,
        "prompt": """GAZE: Direct into lens, steady and heavy. Eyes carry weight, not anger.
BODY LANGUAGE: Near-still throughout. Jaw tightens very slightly on "put hands on you." Small breath before "as a kid."
VOICE STYLE: Same deep Chicago voice, drops half a register. This is naming something painful directly.
TONE: Grave and personal. Calling out something that happened. Not accusing, not dramatic. Just truth.
SPEED: ~2.0 wps. "In any kinda way" lands slowly, deliberate.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. Clean foreground audio.

PRONUNCIATION LOCK: "Illinois" = ILL-ih-noy.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "If a staff member, guard, counselor put hands on you in any kinda way when you was in there as a kid."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 3,
        "prompt": """GAZE: Eyes on lens, steady, slightly forward. The look of someone about to deliver important information.
BODY LANGUAGE: Very small nod on "right now." Posture settled and grounded.
VOICE STYLE: Same voice, lifts slightly. Informational but still intimate, not a sales tone.
TONE: Important news delivered quietly. Something is happening and he wants this person to know.
SPEED: ~2.0 wps, even pacing.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. Clean foreground audio.

PRONUNCIATION LOCK: "Illinois" = ILL-ih-noy. "compensation" = com-pen-SAY-shun.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "There is a process happening right now where Illinois is paying out significant potential compensation."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 4,
        "prompt": """GAZE: Direct into lens, sharp and focused. Eyes stay level.
BODY LANGUAGE: Small deliberate head shake on "they missing it." Still and grounded on "It ain't."
VOICE STYLE: Slightly more forward and direct. Mild street-level frankness, not anger.
TONE: Straight talk to a brother. Mild frustration with the situation, not the viewer. "It ain't" lands flat and final.
SPEED: ~2.0 wps. Natural pause after "They missing it." Brief staccato on final two sentences.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. Clean foreground audio.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "And the men who keep waiting? They missing it. Cause they think it's complicated. It ain't."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 5,
        "prompt": """GAZE: Eyes steady on lens throughout, calm and reassuring.
BODY LANGUAGE: Near-still. Each short phrase lands with a small stillness after it. The pause IS the message.
VOICE STYLE: Even, matter-of-fact, unhurried. Listing the barriers that don't exist.
TONE: Relief. Stripping away the fear one item at a time. This is the list of things that will NOT happen.
SPEED: ~2.2 wps. Each phrase separated by a natural breath.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. Clean foreground audio.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "No police report. No paperwork. No court date right now. No phone calls to your house."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 6,
        "prompt": """GAZE: Direct into lens. Eyes stay steady, practical and present.
BODY LANGUAGE: Minimal, grounded. Very subtle forward presence, engaged.
VOICE STYLE: Same voice, slightly more open and clear. Walking someone through something simple.
TONE: Simple and easy. This is not a big thing. He is making it small and approachable.
SPEED: ~2.2 wps. "A few private questions" gets slight emphasis on "private."

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. Clean foreground audio.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "You go on your phone, you answer a few private questions, and it tells you if you qualify."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 7,
        "prompt": """GAZE: Direct into camera. Eyes soften slightly, reassuring.
BODY LANGUAGE: Very small nod on "That's it." Completely still otherwise. The stillness of "I mean it."
VOICE STYLE: Quieter, warm, private. The closest register in the video.
TONE: Reassurance. Taking the last remaining hesitation and setting it down gently.
SPEED: ~1.8 wps. Very deliberate. "That's it." gets a full stop with silence after.

AUDIO CRITICAL: Voice clear and audible despite soft tone. NOT inaudible. Fills the foreground.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "Less than a minute. Nobody finds out you even looked. That's it."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
    {
        "n": 8,
        "prompt": """GAZE: Eyes directly into lens. Soft, still, completely present. The quietest most direct moment in the video.
BODY LANGUAGE: Completely still. No lean. Face open and settled. Everything has been said. This is the only thing left.
VOICE STYLE: Warm, low, private. The softest clip. Not commercial. Not energetic.
TONE: Compassion. A personal favor to one person. "Tap below" is NOT an ad read. It is a quiet invitation.
SPEED: ~1.5 wps. Very slow. A full breath between each sentence. NOT upbeat, NOT rising inflection.

AUDIO CRITICAL: Speaks CLEARLY AUDIBLY despite soft tone. NOT inaudible. Clean foreground audio. Zero rising inflection. Zero smile in the voice.

CRITICAL — EYES OPEN AND ON CAMERA: Eyes stay OPEN and looking DIRECTLY at the lens throughout.

CRITICAL — NO SMILE EVER: ZERO smile. Eyes carry warmth, not the mouth.

CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. No trailing words. Speak ONLY the words below in order and STOP after the final word.

SPOKEN DIALOGUE: "The hardest part is tapping the button. Tap below. See what comes back."

No on-screen text, no captions, no subtitles, no watermarks.""",
    },
]


# ── Phase 1: Generate anchor via nano-banana-pro ─────────────────────────────

def generate_anchor():
    if ANCHOR_ID_PATH.exists():
        media_id = ANCHOR_ID_PATH.read_text().strip()
        print(f"Anchor already exists: {media_id[:60]}…")
        return media_id

    print("Phase 1: Generating nano-banana-pro anchor …", flush=True)
    payload = {
        "prompt": ANCHOR_PROMPT,
        "model": "nano-banana-pro",
        "aspectRatio": "9:16",
    }
    r = requests.post("https://api.useapi.net/v1/google-flow/images",
                      headers=HEADERS, json=payload, timeout=120)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Anchor generate failed: {r.status_code} {r.text[:400]}")

    data = r.json()
    media_list = data.get("media", [])
    if not media_list:
        raise RuntimeError(f"Anchor: no media in response. Keys: {list(data.keys())}")

    m = media_list[0]
    fife_url = m.get("image", {}).get("generatedImage", {}).get("fifeUrl", "")
    media_id = m.get("image", {}).get("generatedImage", {}).get("mediaGenerationId", "")
    if not media_id:
        raise RuntimeError(f"Anchor: no mediaGenerationId in response")

    # Save anchor image + mediaId
    if fife_url:
        r2 = requests.get(fife_url, timeout=60)
        r2.raise_for_status()
        img_path = OUT / "anchor.jpg"
        img_path.write_bytes(r2.content)
        print(f"Anchor image saved → {img_path} ({img_path.stat().st_size // 1024}KB)")

    ANCHOR_ID_PATH.write_text(media_id)
    print(f"Anchor mediaId saved: {media_id[:60]}…")
    return media_id


# ── Phase 2: Generate video clips ───────────────────────────────────────────

def submit_clip(clip, anchor):
    n = clip["n"]
    out_path = OUT / f"clip{n}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        print(f"  clip{n}: already exists ({out_path.stat().st_size // 1024}KB), skipping")
        return n, out_path, "skipped"

    payload = {
        "prompt": clip["prompt"],
        "model": "veo-3.1-fast",
        "startImage": anchor,
        "aspectRatio": "portrait",
        "duration": 8,
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
    print(f"  clip{n}: submitted → {job_id[:55]}…", flush=True)
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
            media = resp.get("media") or [{}]
            video_url = (media[0].get("videoUrl", "") if media else "")
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
    print(f"  clip{n}: downloaded → {size // 1024}KB")
    return str(out_path)


def generate_clip(clip, anchor):
    n = clip["n"]
    out_path = OUT / f"clip{n}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        print(f"  clip{n}: already exists, skipping")
        return n, str(out_path)
    _, job_id, status = submit_clip(clip, anchor)
    if status == "skipped":
        return n, str(out_path)
    video_url = poll_job(job_id, n)
    path = download_clip(video_url, n)
    return n, path


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Phase 1
    anchor = generate_anchor()
    print(f"\nPhase 2: Generating {len(CLIPS)} clips → {OUT}")
    print(f"Model: veo-3.1-fast | Anchor: {anchor[:60]}…\n")

    # Phase 2
    results = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(generate_clip, c, anchor): c["n"] for c in CLIPS}
        for fut in as_completed(futs):
            n = futs[fut]
            try:
                n, path = fut.result()
                results[n] = path
                print(f"✓ clip{n} done: {path}")
            except Exception as e:
                print(f"✗ clip{n} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/{len(CLIPS)} clips")
    for n in sorted(results):
        print(f"  clip{n}: {results[n]}")
