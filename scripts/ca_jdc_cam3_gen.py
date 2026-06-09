"""
CA JDC — "California is paying out" (A-series)
Persona: CA_M3_v1 — Modest apartment living room, 29yo, medium-dark skin
10 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority

Moderation split (CLAUDE.md hard rule):
  Minor refs ("kids", "juvenile", "minor") only in clips 2, 5 — NO sexual abuse language
  Sexual abuse language only in clip 3 — NO minor/kid reference
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
# CA_M3_v1 — Apartment living room, 29yo, medium-dark skin, navy tee (refreshed 2026-06-09)
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:fbfb77e0-329a-4ec5-8102-7519c4d1d0fb"
OUT = Path("outputs/ca_jdc_cam3")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked into the lens from the first frame. Breaking news to a close friend.\n"
            "BODY LANGUAGE: Completely still. Head level. Jaw set. A slow exhale before speaking.\n"
            "VOICE STYLE: Low, late 20s, plain California. Quiet but carrying weight.\n"
            "TONE: Controlled urgency. Like telling someone something they need to hear right now.\n"
            "SPEED: ~2.2 wps. Even. Slight drop in pace on 'still don't know exists.'\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full quiet projection. NOT whispered. Every word distinct.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Right now, today, California is paying out on a wave of cases most survivors still don\'t know exists."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Leaning into the facts. Momentum building.\n"
            "BODY LANGUAGE: Completely still. Head level. Very slight forward settle on 'juvenile facilities.'\n"
            "VOICE STYLE: Same low plain voice. 'Here is what's happening.' as a short sharp pivot.\n"
            "TONE: Quiet disclosure. Naming facts plain — not outrage, just the record.\n"
            "SPEED: ~2.3 wps. Even, clipped. Brief pause after 'what's happening.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Here is what\'s happening. For decades, kids locked in California juvenile facilities were kept quiet by the people running them."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Jaw set. Stating the fact plainly — not dramatized, just named.\n"
            "BODY LANGUAGE: Completely still. Head level. Slight tension in the jaw. No movement.\n"
            "VOICE STYLE: Same low plain voice. 'Sexually abused' spoken plainly — not whispered, not emphasized.\n"
            "TONE: Quiet indictment. Not angry. Just stating a documented pattern as cold fact.\n"
            "SPEED: ~1.3 wps. Very slow. Long pause between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Those staff members sexually abused them. Those facilities covered it up."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. A very slight lift of the head — the turn has come.\n"
            "BODY LANGUAGE: Completely still. The faintest release of jaw tension as the pivot arrives.\n"
            "VOICE STYLE: Same low plain voice. 'Now the law has caught up.' delivered with quiet finality.\n"
            "TONE: Quiet arrival. The facts have changed. This is the turn.\n"
            "SPEED: ~1.9 wps. Even. Natural pause after 'caught up.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Now the law has caught up, and hundreds of former detainees have already stepped forward."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Direct but with the softest weight. This is for one person.\n"
            "BODY LANGUAGE: Completely still. A very slight slow blink on 'Locked up.' — then eyes return, locked.\n"
            "VOICE STYLE: Same low plain voice. Each phrase its own breath. 'A minor.' flat and separate.\n"
            "TONE: Quiet recognition. Not pity — acknowledgment. 'I know what that was.'\n"
            "SPEED: ~2.3 wps with long pauses between 'once.' and 'A minor.' and 'Locked up.' and 'Told to stay quiet.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT whispered. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Every one of them was where you were once. A minor. Locked up. Told to stay quiet."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Direct. A quiet empowerment — speaking for them.\n"
            "BODY LANGUAGE: Completely still. Head level. A slight forward steadiness — grounded.\n"
            "VOICE STYLE: Same low plain voice. 'Anymore.' and 'from back then.' each land flat and final.\n"
            "TONE: Quiet release. Not a pep talk. Just stating what's true and what's different now.\n"
            "SPEED: ~2.0 wps. Even. Short pause after 'anymore.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You don\'t have to stay quiet anymore. You don\'t have to prove anything from back then."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Removing every barrier one at a time.\n"
            "BODY LANGUAGE: Completely still. Head level. Arms at sides. No movement.\n"
            "VOICE STYLE: Same low plain voice. 'No report.' and 'No records.' each delivered flat — one at a time.\n"
            "TONE: Plain removal of obstacles. Not a sales pitch. Just naming what is not required.\n"
            "SPEED: ~2.0 wps. Even. Natural pause after 'No records.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "No report. No records. If you remember the facility and you can describe who did it."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Direct and calm. The offer lands, then the stakes land.\n"
            "BODY LANGUAGE: Completely still. Head level. Arms at sides. Completely still.\n"
            "VOICE STYLE: Same low plain voice. 'But these claims run on a deadline.' flat and weighted.\n"
            "TONE: Quiet gravity. First the possibility, then the clock — unhurried but real.\n"
            "SPEED: ~1.6 wps. Slow. Long pause after 'compensation.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You may qualify for significant potential compensation. But these claims run on a deadline."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Urgency without hype — just fact.\n"
            "BODY LANGUAGE: Completely still. Head level. The slightest forward steadiness on 'moving now.'\n"
            "VOICE STYLE: Same low plain voice. 'The check is free.' delivered flat. 'Under a minute.' the same.\n"
            "TONE: Quiet urgency. The stakes are real. The barrier to entry is not.\n"
            "SPEED: ~2.2 wps. Even. Brief pause after 'moving now.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The people moving first are moving now. The check is free, it\'s confidential, and it\'s under a minute."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 10,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Quiet closing weight. NOT salesy — final and real.\n"
            "BODY LANGUAGE: Completely still. Head level. The slightest forward settle on 'Tap below.'\n"
            "VOICE STYLE: Same low plain voice. 'Don't let this be one more thing they took from you.' its own final beat.\n"
            "TONE: Quiet inevitability mixed with quiet empathy. The last line is for them, not at them.\n"
            "SPEED: ~2.1 wps. Slight natural pause before 'Don't let this.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Tap below before your window closes. Don\'t let this be one more thing they took from you."\n\n'
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
    print(f"CA JDC cam3 — CA_M3_v1 (Apartment) | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
