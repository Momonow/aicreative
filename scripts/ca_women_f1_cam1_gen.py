"""
CA Women (CCWF/CIW) — cam1
Persona: CW_F1 — Latina 52yo, Central Valley porch
Script: "I'm fifty-two years old. I got grandkids..."
11 clips × 8s | useapi.net Google Flow veo-3.1-lite | low priority
"""
import os, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
# CW_F1 — Latina 52, Central Valley porch, maroon tee + cardigan, greying ponytail
ANCHOR = "user:2478-email:666c6f776d6f6d6f6d6564696140676d61696c2e636f6d-image:b2db4f46-5e6b-4439-a8dd-2346be6a02b2"
OUT = Path("outputs/ca_women_f1_cam1")
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Eyes looking into the lens with quiet settled distance from the first frame.\n"
            "BODY LANGUAGE: Seated still on the porch. Hands resting in lap. Slight exhale before speaking.\n"
            "VOICE STYLE: Warm slightly husky 50s Latina voice. Plain California. Not loud. Not announcer.\n"
            "TONE: Matter-of-fact. Stating facts about her own life. No emotion pushed.\n"
            "SPEED: ~2.2 wps. Even, unhurried.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full quiet conversational projection. NOT whispered. Every word distinct.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and on the lens throughout. Same eye color first to last frame.\n\n"
            "CRITICAL — NO SMILE: Mouth stays soft neutral. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. No extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "I\'m fifty-two years old. I got grandkids running around this house. I have not thought about Chowchilla in years."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Eyes on lens. A slight inward pull on 'almost deleted,' then steady.\n"
            "BODY LANGUAGE: Completely still. Very slight tilt of head on 'link.'\n"
            "VOICE STYLE: Same warm husky voice. 'And I almost' as a quiet pivot.\n"
            "TONE: Quiet disclosure. Understated. No drama.\n"
            "SPEED: ~2.3 wps. Even.\n\n"
            "AUDIO CRITICAL: Full projection. NOT whispered. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "And I almost deleted my sister\'s text without opening it. She sent me a link about women who were in California facilities."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Eyes on lens. Jaw set. Stating cold fact, not dramatizing it.\n"
            "BODY LANGUAGE: Completely still. Slight tension in the jaw. No movement.\n"
            "VOICE STYLE: Same warm voice. 'Abused by staff' spoken plain — not whispered, not emphasized.\n"
            "TONE: Quiet indictment. Cold factual. Not angry.\n"
            "SPEED: ~2.0 wps. Measured. Brief pause after 'by staff.'\n\n"
            "AUDIO CRITICAL: Full projection. NOT announcer-voiced. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens throughout.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Women who were abused by staff. Finding out they may qualify for significant potential compensation."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Eyes briefly drop to lap on 'two weeks,' then return to lens on 'anymore.'\n"
            "BODY LANGUAGE: Slight forward settle. Weight in the posture.\n"
            "VOICE STYLE: Same warm voice. 'I wasn't carrying it anymore' delivered with quiet finality.\n"
            "TONE: Recounting, not reliving. Matter-of-fact emotional memory.\n"
            "SPEED: ~2.0 wps. Slow. Natural pause between sentences.\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes return to lens and hold.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "I sat on it for two weeks. I wasn\'t carrying it anymore. I\'d put it down a long time ago."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Eyes direct on lens. A quiet conflict then a small turn of relief.\n"
            "BODY LANGUAGE: Still. Hands resting. A barely perceptible shift on 'found out.'\n"
            "VOICE STYLE: Same warm voice. 'Didn't have to be like that' with quiet arrival.\n"
            "TONE: Honest reluctance pivoting to quiet relief. The turn.\n"
            "SPEED: ~2.1 wps. Pause after 'back up.'\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The last thing I wanted was to pick it back up. What I found out was it didn\'t have to be like that."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Eyes direct on lens. A quiet steadiness. Slight release of tension.\n"
            "BODY LANGUAGE: Still. A very faint softening of the jaw.\n"
            "VOICE STYLE: Same warm voice. 'Less than a minute' flat and certain.\n"
            "TONE: Quiet reassurance from personal experience. Not a sales pitch.\n"
            "SPEED: ~2.0 wps. Even.\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "It took less than a minute to check. Nobody asked me to relive anything."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Eyes direct on lens. Level and still.\n"
            "BODY LANGUAGE: Completely still. Each barrier named one at a time.\n"
            "VOICE STYLE: Same warm voice. 'No court.' 'No record.' each flat and separate.\n"
            "TONE: Plain removal of obstacles. Not a pitch.\n"
            "SPEED: ~2.2 wps. Brief natural pauses after 'No court' and 'No record.'\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "No court. No record. No proof I didn\'t have. Just fill out a form in 60 seconds."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Eyes steady on lens. A quiet confidence. Present.\n"
            "BODY LANGUAGE: Settled. Slight forward lean. Hands at rest.\n"
            "VOICE STYLE: Same warm voice. 'That's it' flat and final. Done.\n"
            "TONE: Simple factual close on the process. The drama is completely gone.\n"
            "SPEED: ~2.0 wps. Even. Pause after 'where I stand.'\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "The attorneys reviewed what I shared in confidence and told me where I stand. That\'s it. That was the whole thing."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Eyes on lens. A small weight of sincerity.\n"
            "BODY LANGUAGE: Still. 'Not telling you what to do' with complete stillness — no gesture.\n"
            "VOICE STYLE: Same warm voice. Neither stern nor soft. Honest peer.\n"
            "TONE: Peer-to-peer honesty. Not preaching. Not selling.\n"
            "SPEED: ~2.2 wps. Even.\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "I\'m not telling you what to do. I\'m telling you I almost let the window close."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 10,
        "prompt": (
            "GAZE: Eyes on lens. Direct. The weight of the closing thought.\n"
            "BODY LANGUAGE: Still. Slight forward settle. 'You've been through enough' lands flat and final.\n"
            "VOICE STYLE: Same warm voice. 'You've been through enough' the quiet emotional peak.\n"
            "TONE: Quiet empathy. Not sales. The last line is for her, not at her.\n"
            "SPEED: ~2.1 wps. Natural pause before 'You've been through enough.'\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Because I thought it would cost me something it didn\'t cost me. You\'ve been through enough. This part is easy."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 11,
        "prompt": (
            "GAZE: Eyes on lens. Still and direct. Final settled presence.\n"
            "BODY LANGUAGE: Completely still. A last quiet exhale before speaking.\n"
            "VOICE STYLE: Same warm voice. Flat and certain.\n"
            "TONE: Quiet close. Not hyped. Just done.\n"
            "SPEED: ~2.0 wps. Slow. Slight pause after 'below.'\n\n"
            "AUDIO CRITICAL: Full projection. ONLY exact words.\n\n"
            "EYES LOCK: Warm dark-brown eyes OPEN and on lens.\n\n"
            "CRITICAL — NO SMILE: ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Tap below. Free and private. See where you stand."\n\n'
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
    print(f"CA Women F1 cam1 — CW_F1 (Porch) | veo-3.1-lite | {len(CLIPS)} clips → {OUT}\n")

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
