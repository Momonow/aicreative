"""
CA Women CWL7_F3 — 'Three Lies' — 9 clips
Persona: CWL7_F3_v4 — Panamanian Afro-Latina mix 58, indoor bedroom selfie
9 clips × 8s | useapi google-flow veo-3.1-lite-low-priority (free tier)
9:16 portrait | bit emotions, deliberate pacing | no disclaimer
"""
import os, sys, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent.parent))
from googleflow_client import upload_asset

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

OUT = Path("outputs/ca_women_cwl7f3_cam1")
OUT.mkdir(parents=True, exist_ok=True)

ANCHOR_IMG = Path("outputs/ca_women_latina_personas_v7/persona_CWL7_F3_v4.jpg")
MGID_FILE = OUT / "anchor_mgid.txt"

# ── clip dialogue split ────────────────────────────────────────────────────────
#  C1: "Three lies California women's prison staff told women to make sure
#       you'd never file a sexual abuse compensation claim."
#  C2: "Lie one. If you didn't report it at the time, it's too late."
#  C3: "Lie two. It's your word against ours."
#  C4: "Lie three. This is just how it works in here."
#  C5: "None of those are true."
#  C6: "Women abused by staff at Chow-chilluh, Valley State, Folsom, and CIW"
#  C7: "may qualify for significant potential compensation.
#       Years later, no report needed, no witness."
#  C8: "Simple. No one in your life finds out you looked."
#  C9: "Free and completely confidential to check. Tap below."

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Looking directly into the camera lens from the first frame. "
            "Eyes carry a controlled intensity — she is naming something deliberate.\n"
            "BODY LANGUAGE: Still. A single slow breath before she speaks. "
            "Jaw set with quiet resolve. Head level, no tilt.\n"
            "VOICE: Warm, lived-in, 58-year-old woman. Medium-low pitch. Unhurried authority.\n"
            "TONE: Controlled. She is not angry — she is naming. "
            "Each word placed with the weight of someone who has known this a long time.\n"
            "SPEED: ~2.4 wps. The pace of someone who wants every word heard.\n\n"
            "EMOTION: The composure of someone naming a deception they survived.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio that fills the foreground.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color. She does NOT close her eyes during dialogue.\n\n"
            "CRITICAL — NO SMILE: Mouth stays in a soft neutral line throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words, no improvisation. "
            "STOP speaking after the final word.\n\n"
            'SPOKEN DIALOGUE: "Three lies California women\'s prison staff told women to make sure '
            'you\'d never file a sexual abuse compensation claim."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Directly into the camera lens. Eyes steady and even — slightly sardonic. "
            "She has heard this lie before.\n"
            "BODY LANGUAGE: Completely still. A fractional pause after 'Lie one' before she continues. "
            "Chin very slightly forward on 'it's too late' — quiet certainty.\n"
            "VOICE: Same woman. Flat, matter-of-fact. The lie stated as the institution stated it.\n"
            "TONE: Controlled flatness. She is quoting them — not performing anger. "
            "'It's too late' delivered like something she memorized against her will.\n"
            "SPEED: ~1.8 wps. Natural pause between 'Lie one.' and the rest.\n\n"
            "EMOTION: The weariness of someone who was told this and almost believed it.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Lie one. If you didn\'t report it at the time, it\'s too late."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Into the lens. Eyes carry a flat, knowing quality — almost contemptuous. "
            "The shorter the lie, the more she lets it sit.\n"
            "BODY LANGUAGE: Completely still. A long natural pause after 'Lie two.' "
            "A barely perceptible tightening around the jaw on 'your word against ours.' "
            "Eyes don't flinch.\n"
            "VOICE: Same woman. Even flatter than clip 2. Short sentences, big silence.\n"
            "TONE: Contemptuous calm. She has heard this dismissal and she's simply naming it. "
            "No drama — just the truth of it sitting there.\n"
            "SPEED: ~1.2 wps. Deliberate. Full space around each word.\n\n"
            "EMOTION: The quiet fury of someone who was told her word didn't count.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Lie two. It\'s your word against ours."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Into the lens. Eyes carry the heaviest weight of the three lies — "
            "a quiet, steely stillness.\n"
            "BODY LANGUAGE: A barely perceptible head drop at the start — like she's steadying herself. "
            "On 'how it works in here,' eyes hold absolutely steady. "
            "A single slow breath after the sentence ends.\n"
            "VOICE: Same woman. Most quiet and deliberate register yet. The weight is in the slowness.\n"
            "TONE: The most chilling lie — institutional. Not anger, not contempt. "
            "'This is just how it works in here' delivered like a wall. Heavy and final.\n"
            "SPEED: ~1.4 wps. The slowest clip. Each word given full room.\n\n"
            "EMOTION: The suffocating weight of a system telling you this is normal.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Lie three. This is just how it works in here."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Directly into the lens — the most present and certain gaze of the ad. "
            "Eyes lock with quiet absolute authority.\n"
            "BODY LANGUAGE: Completely still. A fractional chin lift at 'None.' "
            "Eyes hold. No blink. No movement. Just the fact.\n"
            "VOICE: Same woman. Most assured register. Five words, each one a closed door on the lies.\n"
            "TONE: Quiet authority. Not a shout — a certainty. "
            "The turn of the ad, delivered without drama or heat. Just truth.\n"
            "SPEED: ~1.0 wps. The slowest words of the ad. Every word its own sentence.\n\n"
            "EMOTION: The stillness after a long deception is named and dismissed.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "None of those are true."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Steady directly into the lens. Eyes present and even. "
            "She is naming real places — she knows them.\n"
            "BODY LANGUAGE: Almost completely still. A barely audible breath before she begins. "
            "Natural micro-pause after each facility name.\n"
            "VOICE: Measured and factual. Same woman. Each facility name is its own moment.\n"
            "TONE: Grounded authority. She names these places without flinching.\n"
            "SPEED: ~1.8 wps. Brief natural pause between each facility name.\n\n"
            "PRONUNCIATION LOCK: 'Chow-chilluh' = Chowchilla (CHOW-chill-uh). "
            "Valley State. Folsom. CIW. All delivered clearly.\n\n"
            "EMOTION: The weight is in the naming. She knows these walls.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Women abused by staff at Chow-chilluh, Valley State, Folsom, and CIW"\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Into the lens. Eyes even and steady. A trace warmer — she is opening a door.\n"
            "BODY LANGUAGE: Completely still. On 'Years later,' a barely perceptible nod. "
            "On 'no witness,' eyes settle and hold.\n"
            "VOICE: Same woman. A touch fuller. Still plain — but the warmth is audible.\n"
            "TONE: Factual reassurance. Not a pitch. She is listing what is NOT required. "
            "'No report needed, no witness' — each one a burden set down.\n"
            "SPEED: ~1.9 wps. Steady. Natural pause between the two sentences.\n\n"
            "EMOTION: Each 'no' in the list is something that was used against her — and it no longer applies.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "may qualify for significant potential compensation. '
            'Years later, no report needed, no witness."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Into the lens — softer now. A quiet, almost tender steadiness.\n"
            "BODY LANGUAGE: Completely still. A single breath between 'Simple.' and the rest. "
            "On 'finds out you looked,' her gaze holds — she means this.\n"
            "VOICE: Same woman. Most private register of the ad. Warm without performance.\n"
            "TONE: Quiet reassurance. 'Simple.' is plain — not emphatic. "
            "'No one in your life finds out you looked' — delivered like a private guarantee.\n"
            "SPEED: ~1.5 wps. Full pause after 'Simple.' Unhurried.\n\n"
            "EMOTION: The relief of a private door. She's giving them something no one took from her.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Simple. No one in your life finds out you looked."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Into the lens — the most personal gaze of the entire ad. "
            "A quiet, warm steadiness. She's asking, not selling.\n"
            "BODY LANGUAGE: Completely still. A tiny barely-visible nod at 'Tap below.' "
            "Mouth softly closed at the end. No performance.\n"
            "VOICE: Same woman — most quiet register. NOT commercial. NOT TV-ad delivery.\n"
            "TONE: Quiet close. She removes the last barrier and steps back. "
            "'Tap below' — the quietest invitation.\n"
            "SPEED: ~1.5 wps. Full pause between the two sentences.\n\n"
            "EMOTION: Warm stillness. The last thing she offers is ease.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection. "
            "NOT whispered but very quiet. Clean clear audio. NO commercial inflection.\n\n"
            "EYES LOCK: Warm dark-brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Free and completely confidential to check. Tap below."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
]


def get_anchor_mgid():
    if MGID_FILE.exists():
        mgid = MGID_FILE.read_text().strip()
        if mgid:
            print(f"  anchor: reusing mgid {mgid[:40]}…")
            return mgid
    print(f"  anchor: uploading {ANCHOR_IMG} …")
    mgid = upload_asset(str(ANCHOR_IMG), ctype="image/jpeg")
    MGID_FILE.write_text(mgid)
    print(f"  anchor: mgid {mgid[:40]}… saved")
    return mgid


def poll(job_id, n, timeout=1800, interval=20):
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
            url = (media[0].get("videoUrl", "") or
                   media[0].get("video", {}).get("videoUrl", "")) if media else ""
            if url:
                return url
            raise RuntimeError(f"clip{n}: completed but no videoUrl — {data}")
        elif status == "failed":
            raise RuntimeError(f"clip{n} FAILED: {data.get('error', data)}")
        pct = data.get("progressRatio", "?")
        print(f"    clip{n}: {status} {pct} …", flush=True)
        time.sleep(interval)
    raise TimeoutError(f"clip{n} timed out after {timeout}s")


def gen(clip, anchor_mgid):
    n = clip["n"]
    out_path = OUT / f"clip{n}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        print(f"  clip{n}: exists ({out_path.stat().st_size // 1024}KB), skipping")
        return n, str(out_path)

    payload = {
        "prompt": clip["prompt"],
        "model": "veo-3.1-lite-low-priority",
        "startImage": anchor_mgid,
        "endImage": anchor_mgid,
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
    print(f"  clip{n}: submitted → {str(job_id)[:55]}…", flush=True)

    url = poll(job_id, n)
    r2 = requests.get(url, timeout=300, stream=True)
    r2.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in r2.iter_content(65536):
            f.write(chunk)
    print(f"  clip{n}: ✓ saved {out_path.stat().st_size // 1024}KB")
    return n, str(out_path)


if __name__ == "__main__":
    print("CA Women CWL7_F3 — 'Three Lies'")
    print("Persona: Panamanian Afro-Latina mix 58 — indoor bedroom selfie")
    print("Model: veo-3.1-lite-low-priority (free, ultra-low-priority queue)")
    print(f"Output: {OUT}\n")

    anchor_mgid = get_anchor_mgid()
    print()

    results = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(gen, c, anchor_mgid): c["n"] for c in CLIPS}
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
    if len(results) < len(CLIPS):
        missing = [c["n"] for c in CLIPS if c["n"] not in results]
        print(f"\nMissing: clips {missing} — re-run to retry (skip-if-exists active)")
