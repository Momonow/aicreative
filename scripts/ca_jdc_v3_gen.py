"""
CA JDC V3 — "Give me two minutes"
Persona G v4 (Black male 31, concrete steps, golden hour sunshine)
6 clips × 8s via useapi.net Google Flow veo-3.1-lite
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:2d01cdb1-aa32-431e-b84a-708dcec8ed2e"
OUT = Path("outputs/ca_jdc_v3_g")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Locked on the lens from the first frame — NEVER leaves it. The look of "
            "someone stopping you before you scroll. Urgent but controlled.\n"
            "BODY LANGUAGE: Natural selfie stance — one arm extended forward holding the phone, "
            "other arm relaxed at side. Slight forward lean toward the camera on 'two minutes.' "
            "Head level. NO crossed arms.\n"
            "VOICE STYLE: Low, direct, early 30s. Controlled urgency. Not shouting — cutting through.\n"
            "TONE: Stopping the scroll. Talking to one specific person. This matters and he knows it.\n"
            "SPEED: ~2.25 wps. Brief pause after 'life.' 'Scroll right past it.' lands flat.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. "
            "NOT whispered. NO filler sounds. ONLY the exact scripted words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Warm dark-brown eyes OPEN and LOCKED on "
            "the lens for the COMPLETE clip. Does NOT look away for even a moment.\n\n"
            "CRITICAL — NO SMILE EVER: Mouth stays flat and neutral. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No filler words. No extra words. "
            "No trailing words. Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "Give me two minutes, because this could change your life and most people scroll right past it."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes LOCKED on the lens — steady, heavy, NEVER leaving. He is naming a "
            "specific condition and making sure it lands. No looking away.\n"
            "BODY LANGUAGE: Natural selfie stance — one arm forward holding phone, other relaxed. "
            "NO crossed arms. Very still throughout. Head level and grounded.\n"
            "VOICE STYLE: Same low voice, slightly heavier. Factual. Naming each element clearly.\n"
            "TONE: Heavy and plain. Not dramatic — just stating what happened. Every word has weight.\n"
            "SPEED: ~3.0 wps. Even delivery — no internal pauses. The full clause delivered as one unit.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY the exact words. "
            "The sentence trails with a natural comma pause at the end — not a full stop.\n\n"
            "PRONUNCIATION LOCK: California = Cal-ih-FOR-nee-uh. juvenile = JOO-ven-ile. "
            "facility = fuh-SIL-ih-tee. pat-down = PAT-down.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN and LOCKED on the lens "
            "for the ENTIRE clip. Does NOT look away at any point.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No extra words. No trailing word. "
            "Speak ONLY the EXACT words below and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "If you spent time in a California juvenile facility and a staff member used a pat-down or a search to sexually abuse you,"\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes still LOCKED on the lens — this is the payoff of what he just said. "
            "Forward presence deepens slightly. Making sure this next part lands.\n"
            "BODY LANGUAGE: Natural selfie hold — one arm forward, other relaxed. NO crossed arms. "
            "Very small forward weight shift on 'active lawsuit.' Then completely still.\n"
            "VOICE STYLE: Same low voice. Slows and opens slightly — important news delivered calmly.\n"
            "TONE: A door opening. Quiet gravity. The most important thing in the video.\n"
            "SPEED: ~1.75 wps. 'Active lawsuit right now' lands with space around it. "
            "'Significant potential compensation' is even and clear — not rushed.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO non-verbal sounds. ONLY the exact words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes OPEN and LOCKED on the camera lens "
            "throughout the COMPLETE clip. Does NOT look away.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No added words. "
            "Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "there is an active lawsuit right now, and you could receive significant potential compensation."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes LOCKED on the lens — steady and certain. Talking directly to one person. "
            "NEVER breaks contact, NEVER looks away.\n"
            "BODY LANGUAGE: Natural selfie stance — one arm forward holding phone, other at side. "
            "NO crossed arms. Completely still. Head level.\n"
            "VOICE STYLE: Same voice, practical and flat. Removing every objection one by one.\n"
            "TONE: Quiet reassurance. Each phrase closes a door that was stopping the viewer. Plain.\n"
            "SPEED: ~2.1 wps. Each phrase has a brief pause after it — 'No cost to find out.' pause. "
            "'No win, no fee.' pause. '100% confidential.' pause. 'Nobody finds out you even looked.' final.\n\n"
            "AUDIO CRITICAL: FULL projection. ABSOLUTELY NO non-verbal sounds between phrases. ONLY the exact words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN looking DIRECTLY into the lens "
            "for the ENTIRE clip. Does NOT look away at any point.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO smile in face or voice. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. "
            "Each phrase spoken ONCE. Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "No cost to find out. No win, no fee. 100% confidential. Nobody finds out you even looked."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes LOCKED on the lens — practical and direct. NEVER looks away. "
            "He's making it simple and easy.\n"
            "BODY LANGUAGE: Natural selfie hold — one arm extended forward with phone, other relaxed. "
            "NO crossed arms. Relaxed but focused. Head level and still.\n"
            "VOICE STYLE: Same low voice, slightly warmer. A friend explaining something straightforward.\n"
            "TONE: Removing intimidation. Making the process feel effortless. Calm and practical.\n"
            "SPEED: ~2.25 wps. Even delivery. 'You just list where you were and what happened.' "
            "lands simply — no buildup, no drama.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY the exact words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN and LOCKED directly on the lens "
            "for the COMPLETE clip. Does NOT look away for even a moment.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO smile. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. "
            "Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "Tap below. There\'s a form you fill out online. You just list where you were and what happened."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: The quietest, most direct look in the video — eyes locked, soft but certain. "
            "NEVER breaks eye contact. This is the close.\n"
            "BODY LANGUAGE: Natural selfie hold — one arm forward, other relaxed or in pocket. "
            "NO crossed arms. Completely still. Posture slightly opens — everything has been said.\n"
            "VOICE STYLE: Same voice, slightly lower, gravely practical. Not selling — closing.\n"
            "TONE: Final. Gravity without pressure. 'Before this window closes' lands heavy and real.\n"
            "SPEED: ~1.75 wps. 'That's the whole process.' short and flat. "
            "Then space before 'See what you could qualify for before this window closes.'\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY despite quiet tone. NOT inaudible. "
            "NO fillers. ONLY the exact words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN and LOCKED on the lens for "
            "the COMPLETE clip. Does NOT look away.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO smile in face or voice.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. "
            "Do NOT add anything after 'window closes.' "
            "Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "That\'s the whole process. See what you could qualify for before this window closes."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
]


def poll(job_id, n, timeout=600, interval=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(
            f"https://api.useapi.net/v1/google-flow/jobs/{job_id}",
            headers=HEADERS, timeout=30,
        )
        if r.status_code != 200:
            time.sleep(interval)
            continue
        data = r.json()
        status = data.get("status", "")
        if status == "completed":
            media = data.get("response", {}).get("media") or [{}]
            url = media[0].get("videoUrl", "") if media else ""
            if url:
                return url
            raise RuntimeError(f"clip{n}: completed but no videoUrl — {data}")
        elif status == "failed":
            raise RuntimeError(f"clip{n} FAILED: {data}")
        pct = data.get("progressRatio", "?")
        print(f"    clip{n}: {status} ({pct}) …", flush=True)
        time.sleep(interval)
    raise TimeoutError(f"clip{n} timeout after {timeout}s")


def gen(clip):
    n = clip["n"]
    out_path = OUT / f"clip{n}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        print(f"  clip{n}: exists ({out_path.stat().st_size // 1024}KB), skipping")
        return n, str(out_path)

    payload = {
        "prompt": clip["prompt"],
        "model": "veo-3.1-lite",
        "startImage": ANCHOR,
        "aspectRatio": "portrait",
        "duration": 8,
        "async": True,
        "captchaRetry": 5,
    }
    r = requests.post(
        "https://api.useapi.net/v1/google-flow/videos",
        headers=HEADERS, json=payload, timeout=60,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Submit clip{n}: {r.status_code} {r.text[:300]}")
    job_id = r.json().get("jobid")
    print(f"  clip{n}: submitted {job_id[:55]}…", flush=True)

    url = poll(job_id, n)
    r2 = requests.get(url, timeout=120, stream=True)
    r2.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in r2.iter_content(65536):
            f.write(chunk)
    print(f"  clip{n}: saved {out_path.stat().st_size // 1024}KB")
    return n, str(out_path)


if __name__ == "__main__":
    print(f"CA JDC V3 — 'Give me two minutes'")
    print(f"Persona: G_v4 | Model: veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(gen, c): c["n"] for c in CLIPS}
        for fut in as_completed(futs):
            n = futs[fut]
            try:
                n, path = fut.result()
                results[n] = path
                print(f"✓ clip{n} done")
            except Exception as e:
                print(f"✗ clip{n} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/{len(CLIPS)}")
    for n in sorted(results):
        print(f"  clip{n}: {results[n]}")
