"""
CA JDC — Persona M6 (Basketball Court / Longer Beard) | "Count the Hours" script
8 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
# persona_M6_v4 — basketball court, 38yo, longer beard, dark navy sweatshirt
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:2313a613-a74f-4218-ac5c-9f49eaac5537"
OUT = Path("outputs/ca_jdc_m6")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked directly into the lens. Still. Heavy. Like carrying a weight the viewer can feel.\n"
            "BODY LANGUAGE: Standing completely still. Head level. Arms at sides. No movement.\n"
            "VOICE STYLE: Low, late 30s, plain and controlled. NOT a narrator. Like quietly telling one person something serious.\n"
            "TONE: Quiet dread. Each short phrase lands separately — 'Certain nights.' 'Certain guards.' each get their own beat.\n"
            "SPEED: ~2.0 wps. Deliberate. No rushing. Each phrase its own moment.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full quiet projection. NOT whispered. NOT announcer-voiced.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking DIRECTLY into the lens throughout. Never close. Never drift.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You used to count the hours until morning. Because you knew. Certain nights. Certain guards. You knew what was coming."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Still and direct. Recalling something specific.\n"
            "BODY LANGUAGE: Standing still. Head level. Arms at sides. Very still.\n"
            "VOICE STYLE: Same low plain voice. The two 'You knew' lines delivered flat — repetition gives them weight, not emphasis.\n"
            "TONE: Quiet recognition. Naming details from memory. No emotion, just facts.\n"
            "SPEED: ~1.8 wps. Slow and deliberate. Short natural pause between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "In a California juvenile facility, you knew their shift schedule. You knew their footsteps."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Jaw set. Naming what happened — plain, not dramatic.\n"
            "BODY LANGUAGE: Standing still. Head level. Slight tension in the jaw. Arms at sides.\n"
            "VOICE STYLE: Same low plain voice. 'A check. A routine. Their job.' delivered flat — each word its own weight.\n"
            "TONE: Quiet indictment. Not angry. Just naming what they called it versus what it was.\n"
            "SPEED: ~2.0 wps. Even throughout. Short pause after 'abused you.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "And when they abused you, they called it a check. A routine. Their job."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. Calm certainty. The pivot — naming the truth plainly.\n"
            "BODY LANGUAGE: Standing still. Very slight forward settle on 'But you were a child.' Head level. Arms still.\n"
            "VOICE STYLE: Same low plain voice. 'Not their job' delivered flat, firm — NOT triumphant, NOT emotional.\n"
            "TONE: Plain truth. Not a speech. Just two facts stated directly.\n"
            "SPEED: ~2.0 wps. Even throughout. Small natural pause between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "But you were a child in a California juvenile facility. And what they did to you was not their job."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Head lifts slightly. Factual pivot to present.\n"
            "BODY LANGUAGE: Standing still. Very slight head lift on 'Right now.' Arms at sides.\n"
            "VOICE STYLE: Same low plain voice. 'Survivors are coming forward' delivered plain — NOT triumphant.\n"
            "TONE: Factual present tense. What is happening right now — stated without drama.\n"
            "SPEED: ~2.0 wps. Even. Short natural pause between the two sentences.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Right now, survivors are coming forward. California is facing active legal claims."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Direct and calm. Removing barriers one by one.\n"
            "BODY LANGUAGE: Standing still. Head level. Arms at sides. Completely still.\n"
            "VOICE STYLE: Same low plain voice. 'No proof.' 'No police report.' each delivered flat — one at a time, letting each land.\n"
            "TONE: Plain removal of obstacles. NOT a pitch. Just stating facts about what is and isn't required.\n"
            "SPEED: ~1.8 wps. Slow. Brief natural pause before 'No proof.' and 'No police report.'\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "And you may be owed significant potential compensation. No proof. No police report."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. Steady. Delivering the privacy guarantee plainly.\n"
            "BODY LANGUAGE: Standing still. Head level. Still. Arms at sides.\n"
            "VOICE STYLE: Same low plain voice. 'Not one person.' — flat, final, unhurried.\n"
            "TONE: Plain safety guarantee. NOT reassuring in a salesy way — just stating what is true.\n"
            "SPEED: ~2.0 wps. Even throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "This is completely private and confidential. No one in your life finds out. Not one person."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Direct and calm. Quiet closing — NOT urgent, NOT salesy.\n"
            "BODY LANGUAGE: Standing still. Head level. Arms at sides. Very slight exhale on 'Tap below.'\n"
            "VOICE STYLE: Same low plain voice. 'Tap below.' plain. '60 seconds.' plain. Unhurried throughout.\n"
            "TONE: Quiet instruction. NOT a call-to-action voice. Just telling them the next plain step.\n"
            "SPEED: ~2.0 wps. Even. No acceleration.\n\n"
            "AUDIO CRITICAL: FULL projection. NOT announcer-voiced. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Tap below. The form takes 60 seconds. Find out what you qualify for. Before the window closes."\n\n'
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
    print(f"CA JDC — Persona M6 (Basketball Court) | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
