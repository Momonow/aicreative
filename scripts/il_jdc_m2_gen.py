"""
IL JDC — Persona M2 (Kitchen / Longer Beard) | "Illinois settled quietly" script
9 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:1a45fe55-9968-46e9-85cf-4b8a8aac69b2"
OUT = Path("outputs/il_jdc_m2")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes locked straight into the lens from the first frame. Calm authority. Like he's about to expose something real.\n"
            "BODY LANGUAGE: Standing in kitchen, slight forward lean, arms relaxed at sides. Head level. Very still. Jaw set.\n"
            "VOICE STYLE: Low, controlled, early-to-mid 30s. Deliberate weight on 'simple' and 'money'.\n"
            "TONE: Quiet insider knowledge. The tone of someone who has figured out the game.\n"
            "SPEED: ~2.4 wps. Even and measured. Short pause after 'simple.'\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at FULL conversational projection. NOT whispered. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking DIRECTLY into the lens the entire clip. Never close. Never drift.\n\n"
            "CRITICAL — NO SMILE: Mouth flat and neutral. ZERO upturned corners throughout.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The reason Illinois settled these cases without telling anybody is simple. '
            'Every survivor who doesn\'t know is money they keep."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on camera. Heavier now. Naming the viewer directly.\n"
            "BODY LANGUAGE: Standing in kitchen. Completely still. Head level. Slight tilt down on 'abused.'\n"
            "VOICE STYLE: Same low controlled voice. Slower on 'juvie' and 'abused.'\n"
            "TONE: Direct and plain. The weight of naming a real thing.\n"
            "SPEED: ~2.2 wps. Deliberate pause after 'minor.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY. juvie = JOO-vee.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "If you were in Illinois juvie as a minor and you were abused."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on camera. Direct. Pointing the finger at the system.\n"
            "BODY LANGUAGE: Standing in kitchen. Head level. Jaw tight. Arms still.\n"
            "VOICE STYLE: Same low voice. Slightly harder on 'hoping doesn't come forward.'\n"
            "TONE: Quiet accusation. Controlled anger at the institution, not the viewer.\n"
            "SPEED: ~2.2 wps. Slight pause after 'people.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN on the lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "You are one of the people they\'re hoping doesn\'t come forward."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes on camera. Explaining mode. Still and direct.\n"
            "BODY LANGUAGE: Standing in kitchen. Slight forward lean. Head level. One hand may gesture briefly on 'legal duty' then return still.\n"
            "VOICE STYLE: Same low voice. Plain and factual. 'Legal duty' delivered flat.\n"
            "TONE: Matter-of-fact explanation. No emotion — just laying out the mechanism.\n"
            "SPEED: ~2.3 wps. Even throughout.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "PRONUNCIATION LOCK: Illinois = Ill-ih-NOY.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Here\'s how this works. Illinois had a legal duty to protect kids in their custody."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes on camera. Heavier. The weight of 'liable' and 'jury.'\n"
            "BODY LANGUAGE: Standing in kitchen. Very still. Head level. Jaw set. Slight nod on 'liable.'\n"
            "VOICE STYLE: Same low voice. 'Liable' lands flat and final. 'Jury' delivered with quiet certainty.\n"
            "TONE: Accountability. Plain and certain. Not angry — just stating facts.\n"
            "SPEED: ~2.3 wps. Slight pause after 'liable.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "When staff abused those kids, the state became liable. '
            'They know a jury would not be kind to them."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes on camera. Still and direct. The pivot from explanation to action.\n"
            "BODY LANGUAGE: Standing in kitchen. Head level. Completely still. Arms at sides.\n"
            "VOICE STYLE: Same low voice. 'Right now' has slight emphasis. 'Dots' delivered flat.\n"
            "TONE: Transitional — closing the explanation, opening the urgency.\n"
            "SPEED: ~2.4 wps. Even delivery.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "So they\'ve been settling quietly, hoping survivors never connect the dots. '
            'Active claims are moving right now."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes on camera. Heaviest look of the ad. Delivering the two stakes.\n"
            "BODY LANGUAGE: Standing in kitchen. Leans forward slightly. Head level. Jaw set.\n"
            "VOICE STYLE: Same low voice. Fractionally heavier. 'Not flexible' delivered flat and final.\n"
            "TONE: Real urgency without panic. Two plain facts, both with weight.\n"
            "SPEED: ~2.2 wps. Pause after 'table.'\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Significant compensation is on the table. '
            'There is a deadline and it is not flexible."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes on camera. Reassuring. Killing each barrier plainly.\n"
            "BODY LANGUAGE: Standing in kitchen. Head level. Arms relaxed. Fractionally softer energy.\n"
            "VOICE STYLE: Same low voice. Each phrase its own beat. 'Nobody finds out' delivered quietly.\n"
            "TONE: Barrier removal. Plain and reassuring. No sales inflection.\n"
            "SPEED: ~2.1 wps. Each phrase has its own beat and space.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "It\'s private. Nobody in your life finds out. No cost unless they win."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Eyes on camera. Direct and final. Talking to one person.\n"
            "BODY LANGUAGE: Standing in kitchen. Head level. Still. Head may give one small nod on 'qualify.'\n"
            "VOICE STYLE: Same low voice. 'Tap below' plain and unhurried. No commercial inflection.\n"
            "TONE: Calm command. Not urgent, not salesy — just inevitable.\n"
            "SPEED: ~2.2 wps. Even and clear.\n\n"
            "AUDIO CRITICAL: FULL projection. ZERO fillers. ONLY exact words.\n\n"
            "EYES LOCK: Dark-brown eyes stay OPEN and on the lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO smile. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No trailing words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Two minutes to check. Tap below to see if you qualify."\n\n'
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
    print(f"IL JDC — Persona M2 | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
