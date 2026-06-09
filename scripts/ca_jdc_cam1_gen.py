"""
CA JDC — Script B1 "The Files Are Finally Open"
Persona: CA_M1_v4 — Venice Beach boardwalk, 31yo, medium-dark skin
9 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority

Moderation split (CLAUDE.md hard rule):
  Minor refs ("children", "juvenile", "minor") only in clips 1, 3, 7 — NO sexual abuse language
  Sexual abuse language only in clip 4 — NO minor/kid reference
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
# CA_M1_v4 — Venice Beach boardwalk, 31yo, taper fade, stubble, white tee (refreshed 2026-06-09)
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:cc46a60f-5e9e-45c3-80e3-7610f89043e1"
OUT = Path("outputs/ca_jdc_cam1")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked directly into the lens. Steady. Like sharing something that was not supposed to come out.\n"
            "BODY LANGUAGE: Standing completely still. Head level. No movement. A slight set to the jaw.\n"
            "VOICE STYLE: Low, early 30s, plain California. NOT announcer-voiced. Like telling one person something they were never supposed to know.\n"
            "TONE: Quiet revelation. Conspiratorial weight. Each word chosen carefully.\n"
            "SPEED: ~1.6 wps. Slow and deliberate. Long pause after 'juvenile facilities.'\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full quiet projection. NOT whispered. Every word distinct.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout. Never close. Never drift.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Nobody was supposed to find out what happened inside California\'s juvenile facilities."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Same steady weight. Letting the reveal land.\n"
            "BODY LANGUAGE: Standing still. Head level. Absolutely no movement. A very slight exhale between the two sentences.\n"
            "VOICE STYLE: Same low plain voice. 'They didn't.' delivered flat and final — its own complete sentence.\n"
            "TONE: Quiet finality. The second sentence lands like a door closing.\n"
            "SPEED: ~1.5 wps. Very slow. 1.5-second silence between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL quiet projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The records were supposed to stay buried. They didn\'t."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Head lifts very slightly. The pivot from secret to scale.\n"
            "BODY LANGUAGE: Standing still. The smallest lift of the chin as the facts arrive.\n"
            "VOICE STYLE: Same low plain voice. Factual. Momentum picking up slightly.\n"
            "TONE: Quiet disclosure. Naming numbers and people — plain, not triumphant.\n"
            "SPEED: ~2.0 wps. Even throughout. Short natural pause after 'right now.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Hundreds of cases are being filed right now by people who were children in those centers."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. Jaw set. Naming what happened — plain, steady, not dramatic.\n"
            "BODY LANGUAGE: Standing still. Head level. Slight tension in the jaw. Arms at sides.\n"
            "VOICE STYLE: Same low plain voice. 'The claim is the same in case after case.' delivered flat. 'Sexually abuse' spoken plainly — not emphasized, just named.\n"
            "TONE: Quiet indictment. Not angry. Just stating a documented pattern as fact.\n"
            "SPEED: ~2.5 wps. Even throughout. Brief pause after 'case after case.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The claim is the same in case after case. Staff used their power to sexually abuse the people in their care."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Naming institutional failure — plain and final.\n"
            "BODY LANGUAGE: Standing still. Head level. Arms at sides. No movement.\n"
            "VOICE STYLE: Same low plain voice. Each sentence its own beat. 'They did nothing.' flat, unhurried.\n"
            "TONE: Quiet accountability. Not outrage — just fact. The last sentence picks up very slightly.\n"
            "SPEED: ~1.8 wps. Each sentence separated by a natural pause.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "They knew. And they did nothing. That is why this is moving so fast."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Calm certainty. Evidence established. Letting it land.\n"
            "BODY LANGUAGE: Standing still. Head level. Completely still. No movement.\n"
            "VOICE STYLE: Same low plain voice. 'On the record.' delivered flat and final.\n"
            "TONE: Quiet authority. The two sentences are the same fact said two ways — repetition gives it weight.\n"
            "SPEED: ~1.8 wps. Even. Long pause between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "It is not one person\'s word anymore. It is a pattern, on the record."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. The softest the clip has been. Direct but with quiet empathy.\n"
            "BODY LANGUAGE: Standing still. Head level. A very slight lean toward camera on 'you are not alone.'\n"
            "VOICE STYLE: Same low plain voice. Slightly quieter. This is personal address — not a fact, a statement to one person.\n"
            "TONE: Quiet empathy. 'You are not too late.' and 'you are not alone.' each get their own space.\n"
            "SPEED: ~1.8 wps. Slower on the final two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT whispered. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "If this happened to you in one of these facilities, you are not too late. You are not alone."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Direct and calm. Removing every obstacle one at a time.\n"
            "BODY LANGUAGE: Standing still. Head level. Arms at sides. Completely still.\n"
            "VOICE STYLE: Same low plain voice. 'Free.' 'Confidential.' each delivered flat — one at a time.\n"
            "TONE: Plain removal of barriers. NOT a sales pitch. Just stating what is and isn't required.\n"
            "SPEED: ~2.0 wps. Even. Natural pause before 'completely confidential' and 'less than a minute.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You may qualify for significant potential compensation. The check is free, completely confidential, and takes less than a minute."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Quiet closing urgency — NOT salesy, NOT hype.\n"
            "BODY LANGUAGE: Standing still. Head level. Arms at sides. The slightest forward settle on 'Tap below.'\n"
            "VOICE STYLE: Same low plain voice. Unhurried but weighted. 'Before it closes.' its own final beat.\n"
            "TONE: Quiet inevitability. The window is real. Not a trick — just a fact.\n"
            "SPEED: ~2.0 wps. Even. Slight natural pause before 'Tap below.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The window does not stay open forever. Tap below and find out where you stand before it closes."\n\n'
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
            raise RuntimeError(f"clip{n} FAILED: {data.get('error', data)}")
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
        "endImage": ANCHOR,
        "aspectRatio": "portrait",
        "duration": 8,
        "async": True,
        "captchaRetry": 5,
    }
    r = requests.post(
        "https://api.useapi.net/v1/google-flow/videos",
        headers=HEADERS, json=payload, timeout=120,
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
    print(f"CA JDC B1 — CA_M1_v4 (Venice Beach) | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
