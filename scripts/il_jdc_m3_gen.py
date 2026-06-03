"""
IL JDC — Persona M3 (Bedroom / Clean Shaven) | "Most people who qualify" script
8 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:f8294f93-bb45-442d-b9a8-0cd8c45229ac"
OUT = Path("outputs/il_jdc_m3")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked into lens. Still and knowing. He's stating a fact most people don't know.\n"
            "BODY LANGUAGE: Seated on bed edge, slight forward lean, arms relaxed on knees. Head level. Very still.\n"
            "VOICE STYLE: Low, early-30s. Measured and plain. Weight on 'deadline' and 'exists.'\n"
            "TONE: Quiet insider knowledge. He knows how this works. Not alarming — just stating what's real.\n"
            "SPEED: ~2.2 wps. Even. Short pause after 'file.'\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. NOT whispered. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking DIRECTLY into the lens the entire clip. Never close. Never drift.\n\n"
            "CRITICAL — NO SMILE: Mouth flat and neutral. ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Most people who qualify for this don\'t file because they don\'t know the deadline exists."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Heavier now. Naming what the state is doing.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Completely still. Jaw set.\n"
            "VOICE STYLE: Same low voice. 'Counting on' delivered with quiet certainty. 'They owe you nothing' flat and final.\n"
            "TONE: Quiet accusation. Not angry — just naming the calculation plainly.\n"
            "SPEED: ~2.0 wps. Deliberate pause after 'counting on.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "That\'s exactly what Illinois is counting on. After it passes, they owe you nothing."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Talking to one person now.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Still. Arms relaxed.\n"
            "VOICE STYLE: Same low voice. Plain on 'If you were.' Weight on 'sexually abused.'\n"
            "TONE: Direct identification. Not sensational — plain and factual. Naming a real thing.\n"
            "SPEED: ~2.1 wps. Steady throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "If you were in an Illinois juvenile facility as a kid and a guard or staff member sexually abused you,"\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. Steady. Delivering the key fact.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Slight lean forward. Arms still.\n"
            "VOICE STYLE: Same low voice. 'Right now' has slight quiet emphasis. 'File a claim' plain.\n"
            "TONE: Factual urgency. Not alarm — just the plain truth of the window.\n"
            "SPEED: ~2.2 wps. Even and clear.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "there is a legal window open right now to file a claim."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Steady. Normalizing — this is not their fault.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Arms relaxed. Very still.\n"
            "VOICE STYLE: Same low voice. 'No idea' delivered with quiet weight. Plain and even.\n"
            "TONE: Validating. Not pitying — just stating what's normal so they don't feel alone.\n"
            "SPEED: ~2.2 wps. Even throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Most people who were in those facilities have no idea this is happening."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Two plain facts.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Completely still.\n"
            "VOICE STYLE: Same low voice. 'Not been loud about it' delivered flat. 'Significant compensation' plain, no commercial inflection.\n"
            "TONE: Matter-of-fact. Two truths stated simply.\n"
            "SPEED: ~2.2 wps. Short pause between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Illinois has not been loud about it. You may qualify for significant compensation."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. Fractionally warmer. Removing the barriers one by one.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Arms slightly more relaxed. Each phrase its own beat.\n"
            "VOICE STYLE: Same low voice. Each barrier removed plainly. 'Private and confidential' quietly firm.\n"
            "TONE: Reassurance. No pressure. Just killing every reason not to check.\n"
            "SPEED: ~2.1 wps. Each phrase gets its own space.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You don\'t have to come in. No phone calls. Private and confidential. Free to check."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Direct and final. One person, one instruction.\n"
            "BODY LANGUAGE: Seated on bed. Head level. Still. One small nod on 'Go look now.'\n"
            "VOICE STYLE: Same low voice. 'Two minutes' plain. 'Window is still open' has slight quiet urgency. 'Tap below' unhurried.\n"
            "TONE: Calm command. Not urgent, not salesy. Like telling a friend the last thing they need to do.\n"
            "SPEED: ~2.2 wps. Even. NO commercial inflection on 'qualify' or 'tap below.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Two minutes to check if you qualify. Go look now while the window is still open. Tap below."\n\n'
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
    print(f"IL JDC — Persona M3 | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
