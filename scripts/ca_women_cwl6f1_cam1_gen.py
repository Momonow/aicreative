"""
CA Women CWL6_F1 — 'Chest Tightening' — 7 clips
Persona: CWL6_F1_v3 — Ecuadorian mestiza 52, outdoor CA apartment front steps, selfie
7 clips × 8s | useapi google-flow veo-3.1-lite-low-priority (free tier)
9:16 portrait | bit emotions, deliberate pacing | no disclaimer
"""
import os, sys, time, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent.parent))
from googleflow_client import upload_asset

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

OUT = Path("outputs/ca_women_cwl6f1_cam1")
OUT.mkdir(parents=True, exist_ok=True)

ANCHOR_IMG = Path("outputs/ca_women_latina_personas_v6/persona_CWL6_F1_v3.jpg")
MGID_FILE = OUT / "anchor_mgid.txt"

# ── clip dialogue split ────────────────────────────────────────────────────────
#  C1: "There are women who did time in California women's prisons."
#  C2: "Women who can't walk past a corrections officer without their chest tightening."
#  C3: "If staff sexually abused you in there, and that's still with you,
#       there's a compensation claim you may qualify for right now."
#  C4: "Chow-chilluh, Valley State, Folsom, and CIW.
#       The law has caught up to what happened behind those walls."
#  C5: "Women who stayed quiet, women who reported and were ignored,
#       women who thought their chance was gone."
#  C6: "Hundreds have already come forward. Your memory alone is enough to check."
#  C7: "Free. Completely private. No one in your life finds out you looked. Tap below."

CLIPS = [
    {
        "n": 1,
        "prompt": (
            "GAZE: Looks slightly upward at the camera lens — the selfie angle. Her gaze is present "
            "but distant, like she's seeing something beyond the phone. Eyes carry a quiet recognition "
            "from the first frame.\n"
            "BODY LANGUAGE: Nearly motionless at the open. A slow quiet breath in through the nose "
            "before she speaks. Head perfectly still. A faint steadiness — like she's decided something.\n"
            "VOICE: Warm, lived-in, 52-year-old Latina woman. Medium-low pitch. Subdued and unhurried.\n"
            "TONE: Distant and reflective. Naming something she knows to be true. Not performing — "
            "just stating it. Like reading off a fact that carries weight.\n"
            "SPEED: ~1.5 wps. The slowest clip. Full space around each word.\n\n"
            "EMOTION: The opening note of recognition — like she knows exactly who she is about to talk to.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered, "
            "NOT muttered. Clean clear audio that fills the foreground.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color. She does NOT close her eyes during dialogue.\n\n"
            "CRITICAL — NO SMILE: Mouth stays in a soft neutral line throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words, no improvisation. "
            "STOP speaking after the final word.\n\n"
            'SPOKEN DIALOGUE: "There are women who did time in California women\'s prisons."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 2,
        "prompt": (
            "GAZE: Slightly upward into the camera lens. Eyes now carry a quiet heaviness — a knowing weight.\n"
            "BODY LANGUAGE: One slow blink at the very start, then eyes stay open and steady. "
            "A faint micro-tension in the jaw that gently releases — like a small involuntary recognition. "
            "No other movement.\n"
            "VOICE: Same warm midlife Latina woman. Slightly more inward, a fraction quieter.\n"
            "TONE: Weight of recognition. The physical detail — 'chest tightening' — is delivered plainly, "
            "like naming a thing everyone in the room already knows. Not heavy, not light. Just true.\n"
            "SPEED: ~1.5 wps. Still deliberate. Space around each word.\n\n"
            "EMOTION: She knows this feeling is real. The body keeps the record. She is not dramatizing it.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Women who can\'t walk past a corrections officer without their chest tightening."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 3,
        "prompt": (
            "GAZE: Slightly upward into the lens, now fully present and making direct eye contact. "
            "She has shifted from describing 'women' to addressing this specific viewer.\n"
            "BODY LANGUAGE: A barely perceptible forward lean at the word 'you.' "
            "A fractional nod mid-sentence. The body language of someone delivering something important, "
            "not lecturing.\n"
            "VOICE: Warmer and more direct. Same midlife Latina woman — the register shifts from "
            "reflective to steady and matter-of-fact.\n"
            "TONE: Controlled clarity. She is handing over a fact: there is a compensation claim. "
            "'May qualify for right now' is delivered plainly — no hype, no pitch energy.\n"
            "SPEED: ~2.0 wps. Slightly faster than clips 1–2.\n\n"
            "EMOTION: The pivot. She sees the viewer and speaks to them directly. Quiet authority.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners. NOT commercial.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "If staff sexually abused you in there, and that\'s still with you, '
            'there\'s a compensation claim you may qualify for right now."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 4,
        "prompt": (
            "GAZE: Steady and slightly upward into the lens. Eyes present and even. "
            "This is the factual beat — she is naming real places.\n"
            "BODY LANGUAGE: Almost completely still. Chin very slightly down — gravity without "
            "theatrical heaviness. A barely audible pause and tiny breath between the facility list "
            "and 'The law has caught up.' No other movement.\n"
            "VOICE: Same warm midlife Latina woman — measured, factual. Each facility name is its own moment.\n"
            "TONE: Grounded authority. She names the facilities with the confidence of someone who knows "
            "they are real. 'The law has caught up' is stated plainly — quiet finality.\n"
            "SPEED: ~1.8 wps. Brief natural micro-pause between each facility name.\n\n"
            "PRONUNCIATION LOCK: 'Chow-chilluh' = Chowchilla (phonetically: CHOW-chill-uh). "
            "Stress first syllable. Valley State. Folsom. CIW. All delivered clearly.\n\n"
            "EMOTION: Flat calm with resolve. The weight is in the facts, not the delivery.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Chow-chilluh, Valley State, Folsom, and CIW. '
            'The law has caught up to what happened behind those walls."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 5,
        "prompt": (
            "GAZE: Slightly upward into the lens, eyes carrying building quiet weight.\n"
            "BODY LANGUAGE: A very slight sideways head tilt at the start — like thinking through "
            "each item on the list as she says it. By 'women who thought their chance was gone,' "
            "a fractional softening in the eyes — something settles.\n"
            "VOICE: Same midlife Latina woman, careful and measured. The rhythm of the list has a natural "
            "falling cadence — each 'women who' phrase slightly quieter than the last.\n"
            "TONE: Gravity building. Not dramatic — like she is listing women she knows about. "
            "The last phrase, 'thought their chance was gone,' lands the heaviest — delivered quietest.\n"
            "SPEED: ~2.0 wps. Each 'women who' clause its own small space.\n\n"
            "EMOTION: Quiet acknowledgment of three distinct silences. The heaviness is earned by "
            "naming each one — not one mass description.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection, NOT whispered. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Women who stayed quiet, women who reported and were ignored, '
            'women who thought their chance was gone."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 6,
        "prompt": (
            "GAZE: Slightly upward into the lens, eyes a trace warmer now — not a smile, "
            "just a small opening. Like something has been released.\n"
            "BODY LANGUAGE: A barely visible exhale after 'come forward' — the lightest release, "
            "not theatrical. A single slow blink. On 'enough to check,' the chin very slightly drops "
            "and the eyes settle. The smallest signal of reassurance.\n"
            "VOICE: Same midlife Latina woman, a touch softer. The most intimate register yet.\n"
            "TONE: A quiet turning point. 'Hundreds have already come forward' is a fact she delivers "
            "with a trace of quiet warmth — not triumph, just plain good news. "
            "'Your memory alone is enough to check' is the gift — plain, honest, delivered gently.\n"
            "SPEED: ~1.8 wps. Unhurried.\n\n"
            "EMOTION: The first thread of reassurance. Not hope — just a small unlocking. "
            "The door is open and she is holding it.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection. "
            "Clean clear audio.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after final word.\n\n"
            'SPOKEN DIALOGUE: "Hundreds have already come forward. Your memory alone is enough to check."\n\n'
            "No on-screen text, no captions, no subtitles, no watermarks."
        ),
    },
    {
        "n": 7,
        "prompt": (
            "GAZE: Slightly upward into the lens. Eyes are the softest and most personal "
            "in the entire ad. A quiet, almost tender steadiness.\n"
            "BODY LANGUAGE: Completely still. A tiny barely-visible nod at 'Tap below' — "
            "the smallest of gestures, like a nod between two people who understand. "
            "Mouth softly closed. No performance.\n"
            "VOICE: Same midlife Latina woman — the most private and quiet register. "
            "NOT commercial. NOT TV-ad delivery. NOT upbeat. 'Free' gets no emphasis. "
            "'Private' is plain. 'Tap below' is the quietest invitation.\n"
            "TONE: Quiet close. She has said everything. She leaves the rest to the viewer. "
            "'No one in your life finds out you looked' — delivered like a quiet assurance, "
            "not a selling point.\n"
            "SPEED: ~1.5 wps. Slowest clip. Full pause between 'Free.' and 'Completely private.' "
            "Between each phrase.\n\n"
            "EMOTION: Warm stillness. The weight has been said. She steps back. "
            "The last thing she gives is privacy itself.\n\n"
            "AUDIO CRITICAL: Speaks CLEARLY AUDIBLY at full conversational projection. "
            "NOT whispered but very quiet. Clean clear audio. "
            "NO commercial inflection on any word.\n\n"
            "EYES LOCK: Warm medium-dark brown eyes stay OPEN and looking slightly upward into the lens "
            "throughout. Same color.\n\n"
            "CRITICAL — NO SMILE: Soft neutral mouth throughout. ZERO upturned corners.\n\n"
            "CRITICAL — DIALOGUE LOCK: English only. No fillers, no extra words. STOP after 'below.'\n\n"
            'SPOKEN DIALOGUE: "Free. Completely private. No one in your life finds out you looked. Tap below."\n\n'
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
    print("CA Women CWL6_F1 — 'Chest Tightening'")
    print("Persona: Ecuadorian mestiza 52 — outdoor CA apartment front steps — selfie")
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
