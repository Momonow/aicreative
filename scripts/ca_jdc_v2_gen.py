"""
CA JDC V2b — "People hear lawsuit"
Persona C v4 (Black male 27, painted exterior wall)
5 clips × 8s via useapi.net Google Flow veo-3.1-lite
v2b: no crossed arms; natural selfie hold; gaze never leaves lens
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:2b26477d-07dd-438e-aa22-4a2cd3769a6a"
OUT = Path("outputs/ca_jdc_v2_c_b")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Heavy and locked onto the lens from frame one — NEVER leaves the lens for the "
            "ENTIRE clip. The look of someone correcting a wrong assumption. Eyes stay on camera always.\n"
            "BODY LANGUAGE: Natural selfie stance — one arm extended forward holding the phone, "
            "other arm relaxed at side. Shoulder leaning slightly into the wall. Head level. "
            "NO crossed arms. One slow blink after 'bucks' — eyes reopen immediately back on the lens.\n"
            "VOICE STYLE: Low, measured, early-to-mid 20s. Quiet authority. Not performing — stating.\n"
            "TONE: Quiet correction. Naming a misunderstanding everyone has. No drama — just weight.\n"
            "SPEED: ~1.6 wps. Full pause after 'bucks.' 'This is not that.' lands as three separate beats.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. "
            "NOT whispered. NO filler sounds. ONLY the exact scripted words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Warm dark-brown eyes stay OPEN looking DIRECTLY "
            "into the camera lens for the COMPLETE duration. Does NOT look away, does NOT look down, "
            "does NOT look to the side. Eyes are ALWAYS on the lens.\n\n"
            "CRITICAL — NO SMILE EVER: Mouth stays in a flat controlled neutral line. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No filler words. No extra words inserted. "
            "No trailing words. Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "People hear lawsuit and think a couple hundred bucks. This is not that."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes locked forward on the lens for the ENTIRE clip — NEVER looks away, "
            "NEVER glances down or to the side. Holding the camera with steady eye contact throughout.\n"
            "BODY LANGUAGE: Natural selfie stance — one arm forward holding the phone, "
            "other arm relaxed at side or in hoodie pocket. NO crossed arms. "
            "Very still. Shoulder against wall. No head movement. No nodding.\n"
            "VOICE STYLE: Same low voice, half a register flatter. Factual. Reading a verdict.\n"
            "TONE: The weight of what this actually is. Not drama — just naming it plainly.\n"
            "SPEED: ~2.1 wps. Even and steady through the full sentence. 'So-called' lands with mild emphasis.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY the exact words.\n\n"
            "PRONUNCIATION LOCK: California = Cal-ih-FOR-nee-uh. juvenile = JOO-ven-ile. "
            "facilities = fuh-SIL-ih-teez. pat-downs = PAT-downz.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN and LOCKED on the lens throughout "
            "the ENTIRE clip. Does NOT look away at any point.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No extra words. No trailing word. "
            "Speak ONLY the EXACT words below and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "California juvenile facilities are being sued over staff sexually abusing kids during so-called searches and pat-downs."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on the lens the ENTIRE time — direct, steady, NEVER breaking contact. "
            "Slight forward presence making sure this lands. Eyes do NOT drift, do NOT look away.\n"
            "BODY LANGUAGE: Natural selfie posture — one arm extended holding phone toward camera, "
            "other hand relaxed at side. NO crossed arms. Very small weight shift forward on 'significant.' "
            "Then completely still. Head level. NO nodding.\n"
            "VOICE STYLE: Same low voice. Slight uptick of presence — not salesy, just present.\n"
            "TONE: A door opening. Quiet delivery of important news. Calm certainty.\n"
            "SPEED: ~2.1 wps. Steady through the first sentence. "
            "'Six figures, in some cases.' delivered slower with space around it.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO non-verbal sounds between sentences. ONLY the exact words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN and LOCKED directly on the camera "
            "lens for the ENTIRE clip. Does NOT look away for even a moment.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO upturned corners. ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No added words. "
            "Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "And the people coming forward could be looking at significant potential compensation. Six figures, in some cases."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eye contact deepens and HOLDS. Eyes locked on the lens the ENTIRE clip. "
            "Talking to one specific person. NEVER breaks eye contact, NEVER looks away.\n"
            "BODY LANGUAGE: Natural selfie stance — one arm forward holding phone, "
            "other arm relaxed at side. NO crossed arms. Head level and completely still. "
            "ONE small forward lean on 'you owe it to yourself.' Otherwise still.\n"
            "VOICE STYLE: Same low voice, slightly warmer but grounded. Not pitching — insisting.\n"
            "TONE: Direct and personal. Quiet urgency. The kind of thing a trusted friend says once.\n"
            "SPEED: ~2.6 wps. 'It costs nothing.' and 'It stays private.' land flat and final with brief pauses between.\n\n"
            "AUDIO CRITICAL: FULL projection. ABSOLUTELY NO non-verbal sounds between sentences. ONLY the exact words.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN and LOCKED on the lens for the "
            "ENTIRE clip. Does NOT close eyes, does NOT look away at any moment.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO smile in face or voice. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. "
            "Each sentence spoken ONCE only. "
            "Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "If that was you in there, you owe it to yourself to just check. It costs nothing. It stays private."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Softest, most direct look in the video — eyes quietly locked on the lens. "
            "NEVER looks away. This is the final offer, delivered straight into the camera.\n"
            "BODY LANGUAGE: Natural selfie posture — one arm forward holding phone toward camera, "
            "other hand relaxed at side or in pocket. NO crossed arms. Completely still. "
            "Everything has been said.\n"
            "VOICE STYLE: Same voice, even and practical. A friend making it simple. No enthusiasm.\n"
            "TONE: Removing every barrier. Each phrase is a door opening. Plain and final.\n"
            "SPEED: ~1.4 wps. Each phrase has space around it. 'See your number.' lands clean and flat.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY despite quiet tone. NOT inaudible. "
            "NO fillers. ONLY the exact words.\n\n"
            "PRONUNCIATION LOCK: 30-second = THIR-tee SEK-und.\n\n"
            "CRITICAL — EYES ON LENS AT ALL TIMES: Eyes stay OPEN looking DIRECTLY into the lens "
            "for the COMPLETE clip. Does NOT look away at any point.\n\n"
            "CRITICAL — NO SMILE EVER: ZERO smile in face or voice.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. "
            "Do NOT add anything after 'your number.' "
            "Speak ONLY the EXACT words below in order and STOP after the final word.\n\n"
            'SPOKEN DIALOGUE: "Tap the link, take the 30-second quiz, and see your number."\n\n'
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
    print(f"CA JDC V2b — 'People hear lawsuit'")
    print(f"Persona: C_v4 | Model: veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
