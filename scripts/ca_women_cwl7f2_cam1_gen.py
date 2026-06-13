"""
CA Women CWL7_F2 — 'I Filed a Grievance' — 9 clips
Persona: CWL7_F2_v1 — Guatemalan-American Ladino 46, apartment stoop outdoor
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

OUT = Path("outputs/ca_women_cwl7f2_cam1")
OUT.mkdir(parents=True, exist_ok=True)

ANCHOR_IMG = Path("outputs/ca_women_latina_personas_v7/persona_CWL7_F2_v1.jpg")
MGID_FILE = OUT / "anchor_mgid.txt"

# ── clip dialogue split ────────────────────────────────────────────────────────
#  C1: "I filed a grievance in a California women's prison after a staff member sexually abused me."
#  C2: "They threw it away. I kept my copy."
#  C3: "I just found out it still counts."
#  C4: "Women abused by staff at Chow-chilluh, Valley State, Folsom, and CIW"
#  C5: "may qualify for significant potential compensation."
#  C6: "Whether you reported it or not. Whether anyone listened or not."
#  C7: "Staying quiet, being ignored. None of that closes the door."
#  C8: "It's free to find out. Completely confidential. No court."
#  C9: "Tap below and answer a few questions about what happened."

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Looking directly into the camera lens from the first frame. "
            "Eyes carry the weight of something long-held. Steady, controlled, present.\n"
            "BODY LANGUAGE: Nearly motionless. One slow breath before she begins. "
            "A fractional jaw set as she starts — the composure of someone who has rehearsed this moment a hundred times.\n"
            "VOICE: Warm, lived-in, 46-year-old Guatemalan-American woman. Medium pitch. Subdued.\n"
            "TONE: Controlled raw disclosure. She's saying something she's held a long time. "
            "Not dramatic — just true. Each word placed deliberately.\n"
            "SPEED: ~2.1 wps. Measured but continuous — she doesn't stop once she starts.\n\n"
            "EMOTION: The weight of finally saying it out loud. Not tears — just the gravity of fact.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio that fills the foreground.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color. She does NOT close her eyes during dialogue.\n\n"
            "CRITICAL — NO SMILE: Mouth stays in a soft neutral line throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words, no improvisation. "
            "STOP speaking after the final word.\n\n"
            'SPOKEN DIALOGUE: "I filed a grievance in a California women\'s prison after a staff member sexually abused me."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Directly into the camera lens. Eyes carry a quiet heaviness — and a flicker of something harder underneath.\n"
            "BODY LANGUAGE: A barely perceptible tightening around the eyes on the first sentence. "
            "A fractional release — almost a small exhale — before the second sentence. No other movement.\n"
            "VOICE: Same woman. Slightly more inward, quiet defiance underneath.\n"
            "TONE: Two facts delivered plainly. Hurt in the first. Quiet resolve in the second. "
            "Big silence between them — she lets it land.\n"
            "SPEED: ~1.5 wps. Slow. Full space between the two sentences.\n\n"
            "EMOTION: The sting of being dismissed. And the small, private act of keeping her copy anyway.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "They threw it away. I kept my copy."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Directly into the lens. A fractional softening — something is shifting.\n"
            "BODY LANGUAGE: Almost completely still. A single slow blink mid-sentence. "
            "On 'still counts,' the faintest trace of something releasing in her eyes.\n"
            "VOICE: Same woman. A touch quieter. The most internal register yet.\n"
            "TONE: Quiet revelation. Not joy — more like relief arriving slowly, almost disbelief. "
            "Each word has weight because she didn't expect this to be true.\n"
            "SPEED: ~1.5 wps. Deliberate. Full pause between 'found out' and 'it still counts.'\n\n"
            "EMOTION: The thing she thought was gone, isn't. That realization landing quietly.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "I just found out it still counts."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Steady directly into the lens. Eyes present and even. "
            "She is naming real places — she knows them.\n"
            "BODY LANGUAGE: Almost completely still. Chin very slightly down. "
            "A barely audible breath before she begins. Natural micro-pause after each facility name.\n"
            "VOICE: Measured and factual. Same woman. Each facility name is its own moment.\n"
            "TONE: Grounded authority. She names these places without flinching. She's been there.\n"
            "SPEED: ~1.8 wps. Brief natural pause between each facility name.\n\n"
            "PRONUNCIATION LOCK: 'Chow-chilluh' = Chowchilla (CHOW-chill-uh). "
            "Valley State. Folsom. CIW. All delivered clearly.\n\n"
            "EMOTION: Flat calm with resolve. The weight is in the naming.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Women abused by staff at Chow-chilluh, Valley State, Folsom, and CIW"\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Into the lens. Eyes even and steady. This is the fact — she states it plainly.\n"
            "BODY LANGUAGE: Completely still. A fractional settling of the shoulders before she speaks. "
            "On 'compensation,' her gaze holds — she means this for whoever is watching.\n"
            "VOICE: Same woman. Not a pitch. Not a performance. Just the fact.\n"
            "TONE: Flat calm. She's not selling it. She's telling it. "
            "'Significant potential compensation' — delivered without emphasis, without hope or fear.\n"
            "SPEED: ~1.5 wps. Deliberate. Weight on each word.\n\n"
            "EMOTION: Restrained. She knows the weight of this sentence and doesn't dress it up.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "may qualify for significant potential compensation."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Into the lens — more present now. A fractional forward energy, like she's making sure the viewer hears this.\n"
            "BODY LANGUAGE: A barely perceptible lean on 'you.' "
            "On the second clause, her chin drops very slightly — she's covering both kinds of women.\n"
            "VOICE: Same woman. A touch more direct. Still quiet — but the most addressed she's been.\n"
            "TONE: Quiet insistence. Not a shout — a steady hand on the shoulder. "
            "Each clause its own complete thought.\n"
            "SPEED: ~1.8 wps. Natural pause between the two sentences.\n\n"
            "EMOTION: She wants whoever is doubting to hear this specifically. For them.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Whether you reported it or not. Whether anyone listened or not."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Into the lens. The softest, warmest gaze of the ad so far. "
            "A quiet steadiness — like she's seen this pain and she's naming it with care.\n"
            "BODY LANGUAGE: Completely still. On 'None of that closes the door,' "
            "a barely visible single nod — small, certain.\n"
            "VOICE: Same woman. Most gentle register yet. Still clear — but the warmth is audible.\n"
            "TONE: Resolving. Reassurance without sentiment. "
            "'None of that closes the door' — quiet finality. She means it.\n"
            "SPEED: ~1.5 wps. Full pause between the two sentences.\n\n"
            "EMOTION: She needed to hear this once too. She's giving it back.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Staying quiet, being ignored. None of that closes the door."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 8,
        "prompt": (
            "GAZE: Into the lens. Eyes even and steady. She's removing obstacles one by one.\n"
            "BODY LANGUAGE: Completely still. Tiny natural pause between each sentence — "
            "she gives each one room to land. No performance.\n"
            "VOICE: Same woman. Plain and clean. Most matter-of-fact register of the ad.\n"
            "TONE: Quiet removal of every excuse not to check. "
            "'Free.' 'Confidential.' 'No court.' — each one a door opened, not a sales pitch.\n"
            "SPEED: ~1.5 wps. Full pause between each sentence. Unhurried.\n\n"
            "EMOTION: Practical compassion. She's clearing the path.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "It\'s free to find out. Completely confidential. No court."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 9,
        "prompt": (
            "GAZE: Into the lens — the most personal and quiet gaze of the entire ad. "
            "A tender steadiness. She's asking, not telling.\n"
            "BODY LANGUAGE: Completely still. A tiny barely-visible nod at 'Tap below.' "
            "Mouth softly closed at the end. No performance.\n"
            "VOICE: Same woman — most private and quiet register. "
            "NOT commercial. NOT TV-ad delivery. NOT upbeat. Each phrase its own breath.\n"
            "TONE: Quiet close. She steps back and leaves the rest to the viewer. "
            "'A few questions about what happened' — delivered like a gentle hand extended.\n"
            "SPEED: ~1.5 wps. Full pause between 'Tap below' and the rest.\n\n"
            "EMOTION: Warm stillness. The last thing she offers is ease.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection. "
            "NOT whispered but very quiet. Clean clear audio. NO commercial inflection.\n\n"
            "EYES LOCK: Medium-dark brown eyes stay OPEN and looking directly into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Tap below and answer a few questions about what happened."\n\n'
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
    print("CA Women CWL7_F2 — 'I Filed a Grievance'")
    print("Persona: Guatemalan-American Ladino 46 — apartment stoop outdoor")
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
