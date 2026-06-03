"""
IL JDC — Persona M1 (Living Room / Couch) | "You saw this and kept scrolling" script
9 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:60c8beb2-0bd9-4438-a160-0a8609b55a5f"
OUT = Path("outputs/il_jdc_m1")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked straight into the lens. Slightly narrowed — knowing. Like he watched you do it.\n"
            "BODY LANGUAGE: Seated on couch, slight forward lean, elbows on knees. Head level. Very still.\n"
            "VOICE STYLE: Low, early-30s. Measured. Slight weight on 'scrolling' and 'you.'\n"
            "TONE: Quiet recognition. Not accusing — naming. He sees through the scroll.\n"
            "SPEED: ~2.0 wps. Unhurried. Short pause after 'scrolling.'\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. NOT whispered. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking DIRECTLY into the lens the entire clip. Never close. Never drift.\n\n"
            "CRITICAL — NO SMILE: Mouth flat and neutral. ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You saw this and kept scrolling. Maybe you thought it wasn\'t for you."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Softer now. He understands those thoughts.\n"
            "BODY LANGUAGE: Seated on couch. Head level, slight tilt down on 'blow up your life.' Arms relaxed.\n"
            "VOICE STYLE: Same low voice. Slightly gentler. Each 'Maybe' gets its own weight.\n"
            "TONE: Empathetic naming. He's been there. Not pitying — recognizing.\n"
            "SPEED: ~2.0 wps. Each fear gets its own beat.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Maybe you thought it was too late, or nobody would believe you, or it would blow up your life."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Flat and certain. The pivot.\n"
            "BODY LANGUAGE: Seated on couch. Completely still. Head level. Jaw set.\n"
            "VOICE STYLE: Same low voice. 'None of that is true' delivered flat and final. Then plain on the second sentence.\n"
            "TONE: Definitive. No softness. A plain correction, then a plain fact.\n"
            "SPEED: ~2.0 wps. Slight pause after 'true.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY. juvie = JOO-vee.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "None of that is true. A guard or staff abused you as a kid in Illinois juvie."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. Steady. Information mode.\n"
            "BODY LANGUAGE: Seated on couch. Head level. Still. Arms relaxed at sides.\n"
            "VOICE STYLE: Same low voice. Factual and plain. No emotional inflection.\n"
            "TONE: Matter-of-fact. Laying out what is simply true.\n"
            "SPEED: ~2.2 wps. Even throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Significant compensation is still open. Illinois is not going to announce this on the news."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Quiet weight. Naming what the state is doing.\n"
            "BODY LANGUAGE: Seated on couch. Slight forward lean. Head level. Jaw set.\n"
            "VOICE STYLE: Same low voice. Each word carries weight. 'Banking' delivered with quiet contempt.\n"
            "TONE: Quiet accusation. Controlled. He knows how the math works.\n"
            "SPEED: ~1.8 wps. Deliberate. Each word its own space.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "They are banking on survivors not coming forward."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Blunt. The math.\n"
            "BODY LANGUAGE: Seated on couch. Head level. Still. Slight nod on 'math.'\n"
            "VOICE STYLE: Same low voice. 'They don't have to pay' flat and plain. 'That's the math' almost offhand.\n"
            "TONE: Plain and blunt. No emotion — just arithmetic.\n"
            "SPEED: ~2.2 wps. Slightly harder on 'pay.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Every person who stays quiet is a person they don\'t have to pay. That\'s the math."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. Steady. The reassurance pivot.\n"
            "BODY LANGUAGE: Seated on couch. Head level. Arms slightly more relaxed. Energy fractionally warmer.\n"
            "VOICE STYLE: Same low voice. 'Hasn't passed yet' has quiet urgency. 'Nobody finds out' delivered softly.\n"
            "TONE: Reassurance. Three plain facts that remove barriers. No sales inflection.\n"
            "SPEED: ~2.1 wps. Each phrase its own beat.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The deadline hasn\'t passed yet. Completely private, nobody in your life finds out. Free to check."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Calm. Walking them through the steps.\n"
            "BODY LANGUAGE: Seated on couch. Head level. Slight lean back — relaxed certainty.\n"
            "VOICE STYLE: Same low voice. 'Two minutes' plain and unhurried. 'Legal team tells you if you qualify' matter-of-fact.\n"
            "TONE: Simple and clear. The process is easy. No excitement, no urgency — just plain truth.\n"
            "SPEED: ~2.2 wps. Even and clear.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Two minutes. You fill out one form and a legal team tells you if you qualify."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Eyes on camera. Direct and final. Talking to one person.\n"
            "BODY LANGUAGE: Seated on couch. Head level. Still. One small nod on 'Go look.'\n"
            "VOICE STYLE: Same low voice. 'No cost unless they win' plain. 'Go look' delivered like a quiet instruction.\n"
            "TONE: Calm command. Not urgent, not salesy. Like telling a friend what to do next.\n"
            "SPEED: ~2.0 wps. Even and unhurried. NO commercial inflection on any word.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "No cost unless they win. Go look. That\'s it. Tap below."\n\n'
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
    print(f"IL JDC — Persona M1 | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
