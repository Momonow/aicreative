"""
IL JDC — Persona M4 (Basement/Den / Box Fade / Hoodie) | "Major legal breakthrough" script
8 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:6450a645-c3c8-43e1-bd44-f7eea9509b1a"
OUT = Path("outputs/il_jdc_m4")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked into lens. Steady and serious. Delivering weight on 'sexual abuse' and 'detention centers.'\n"
            "BODY LANGUAGE: Standing still, head level. Arms at sides. No movement.\n"
            "VOICE STYLE: Low, mid-30s, controlled. NOT a news anchor. Plain and direct like a person, not a broadcast.\n"
            "TONE: Quiet gravity. NOT newscaster, NOT attorney-ad voice. Conversational weight — like telling a friend something serious.\n"
            "SPEED: ~2.0 wps. Slow and deliberate. Each phrase lands.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. NOT whispered. NOT announcer-voiced. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking DIRECTLY into the lens the entire clip. Never close. Never drift.\n\n"
            "CRITICAL — NO SMILE: Mouth flat and neutral. ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "A major legal breakthrough is unfolding for survivors of sexual abuse in Illinois juvenile detention centers."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Heavier. Letting the number land.\n"
            "BODY LANGUAGE: Standing. Head level. Completely still. Jaw set.\n"
            "VOICE STYLE: Same low plain voice. NOT news anchor. 'Finally breaks down' delivered quietly, not triumphantly.\n"
            "TONE: Plain statement of fact. Quiet gravity. NOT energetic or dramatic.\n"
            "SPEED: ~2.0 wps. Short pause after 'filed.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Hundreds of new lawsuits have been filed as the wall of silence finally breaks down."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Still and serious. Naming what happened.\n"
            "BODY LANGUAGE: Standing. Head level. Very still. Arms at sides.\n"
            "VOICE STYLE: Same low plain voice. 'Threats' and 'children quiet' delivered with controlled weight. NOT dramatic.\n"
            "TONE: Quiet indictment. Not angry — just stating a documented reality.\n"
            "SPEED: ~2.0 wps. Even throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "For decades, staff allegedly used threats of extended sentences to keep children quiet,"\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. The pivot — 'But the law has changed' lands with weight.\n"
            "BODY LANGUAGE: Standing. Head level. Slight nod on 'changed.' Arms still.\n"
            "VOICE STYLE: Same low plain voice. 'Turned a blind eye' flat. 'Changed' delivered as a plain fact, NOT triumphant.\n"
            "TONE: Factual pivot. Not hopeful or rousing — just two plain facts.\n"
            "SPEED: ~2.0 wps. Short pause before 'But the law has changed.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "while facilities turned a blind eye to the trauma. But the law has changed."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Talking to one person.\n"
            "BODY LANGUAGE: Standing. Slight forward lean. Head level. Arms relaxed.\n"
            "VOICE STYLE: Same low plain voice. 'Up to 30 years ago' delivered matter-of-fact. NOT emphatic.\n"
            "TONE: Plain and direct. No urgency, no drama — just a fact about time.\n"
            "SPEED: ~1.8 wps. Very deliberate. Each word its own space.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Even if your abuse happened up to 30 years ago,"\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Steady. Delivering the offer plainly.\n"
            "BODY LANGUAGE: Standing. Head level. Still. Arms at sides.\n"
            "VOICE STYLE: Same low plain voice. 'Life-changing compensation' delivered flat — NOT salesy, NOT excited.\n"
            "TONE: Plain possibility. Not a pitch — just what the law now allows. NO commercial inflection.\n"
            "SPEED: ~2.0 wps. Even throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "you may finally be eligible to hold these institutions accountable and seek life-changing compensation."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. Direct and calm. The window, the step.\n"
            "BODY LANGUAGE: Standing. Head level. Completely still.\n"
            "VOICE STYLE: Same low plain voice. 'Open now' plain. 'Tap below' unhurried. NO rising inflection. NO commercial energy.\n"
            "TONE: Plain instruction. NOT urgent, NOT a call-to-action voice — just telling them what to do next.\n"
            "SPEED: ~2.0 wps. Even. No acceleration on 'Tap below.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The window to join this is open now. Tap below to take your private eligibility check."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Final. Direct. Talking to one person.\n"
            "BODY LANGUAGE: Standing. Head level. Arms at sides. Still.\n"
            "VOICE STYLE: Same low plain voice. 'Your voice matters' plain and even — NOT motivational. 'Time to act is now' same low flat register.\n"
            "TONE: Quiet closing. NOT rousing, NOT attorney-ad close. Just two plain facts. Same subdued energy as the rest.\n"
            "SPEED: ~2.0 wps. Even and unhurried. No emphasis spike on any word.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Join the fight for justice. Your voice matters, and the time to act is now."\n\n'
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
    print(f"IL JDC — Persona M4 | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
