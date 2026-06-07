"""Story B (Illinois juvie storytime, "I never told a soul") — persona bed_b2.
FREE path: useapi google-flow veo-3.1-lite-low-priority (no credit, ultra-low-priority).
i2v startImage persona lock. clip01 from bed_b2; clips 02-14 from eyes-open clip1 anchors (rotated).
NOTE: free tier WATERMARKS output -> finalize crops the bottom strip.

  python scripts/jdc_storytime_b_gen.py clip01     # test clip 1
  python scripts/jdc_storytime_b_gen.py            # all
"""
import sys, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from googleflow_client import upload_asset, generate_veo, download

SLUG = "illinois_jdc_storytime_b_b2"
OUT = Path(f"outputs/{SLUG}"); OUT.mkdir(parents=True, exist_ok=True)
HOST_IMG = "outputs/illinois_jdc_storytime_bed/reference/bed_b2.png"


def P(line, tone, body, pron, last):
    return f"""He is lying back in bed talking into his phone, filming a quiet selfie confession.
GAZE: soft intimate eye contact straight into the phone lens like he is talking to one person he trusts, with an occasional brief glance away then back. Warm dark-brown eyes, OPEN, staying the SAME color throughout (never lighter or changing).
BODY: small natural head shifts on the pillow, slow blinks, weary. {body}
VOICE: low weary young man, late 20s, quiet and heavy, slightly hoarse.
TONE: {tone}
SPEED: about 2.5 words per second, slow and deliberate, each word given weight.
AUDIO CRITICAL: he speaks clearly and fully audibly at a close intimate volume right into the phone mic. NOT whispered, NOT muttered.
PRONUNCIATION: {pron}
DIALOGUE LOCK: English only. Say ONLY the words in SPOKEN DIALOGUE, in order. No fillers (no uh, um, like, you know), no extra or trailing words, no repetition. Stop after the final word "{last}".
NO on-screen text, NO captions, NO subtitles.
SPOKEN DIALOGUE (verbatim, stop after final word): "{line}\""""

PRON_SA = 'Say "SA\'ed" as the spoken letters "ess-ay-d" (S then A then a d), NOT "sad" and NOT "sside". "juvie" = "JOO-vee". "Illinois" = "ill-uh-NOY".'
PRON_PLAIN = "Natural clear American English."

CLIPS = [
    ("clip01", "A guard SA'ed me at Illinois juvie. I never told a single soul. This is my story.",
     "Heavy, bracing himself; quiet and raw, the weight of saying it for the first time.", "A slow swallow before he starts.", PRON_SA),
    ("clip02", "And how I just found out I might qualify for compensation for it. If it happened to you too, stay with me.",
     "A small turn toward hope, steadier.", "A slight lift in the eyes.", PRON_PLAIN),
    ("clip03", "I was fourteen. In there for something stupid, just counting down the days till I got out.",
     "Matter-of-fact, a little defensive.", "Faint shrug.", PRON_PLAIN),
    ("clip04", "It was the one man who was supposed to be in charge of me. The one with all the power.",
     "Quiet, harder to say, eyes drop.", "Looks down then back.", PRON_PLAIN),
    ("clip05", "And I knew right away nobody was gonna take my word over his. So I said nothing.",
     "Defeated, resigned, low and steady.", "Slow small head shake.", PRON_PLAIN),
    ("clip06", "I did my time. Walked out and acted like it never happened. For years.",
     "Hollow, numb.", "Distant look.", PRON_PLAIN),
    ("clip07", "But it changes you. Couldn't trust nobody, couldn't let anyone close. Carried it alone.",
     "Vulnerable, reflective.", "Soft tired eyes.", PRON_PLAIN),
    ("clip08", "I only started talking because I found out I wasn't the only one. Not even close.",
     "A turn toward relief and resolve.", "A small lift.", PRON_PLAIN),
    ("clip09", "Nearly a thousand of us have come forward about what happened in these places.",
     "Steadier, gathering resolve.", "Slight nod.", PRON_PLAIN),
    ("clip10", "Out in California, Los Angeles County just settled cases like ours for almost five billion dollars.",
     "Informative, a spark of this-is-real.", "Eyebrows raise slightly.", '"Los Angeles" = "loss AN-juh-luss".'),
    ("clip11", "So if you went through sexual abuse while you were locked up in Cook County, Saint Charles, or Harrisburg, this is for you.",
     "Direct to the viewer, sincere and steady.", "Leans a touch closer.", '"Saint Charles" plainly; "Harrisburg" = "HAIR-iss-burg".'),
    ("clip12", "You may qualify for significant potential compensation. A lawyer reviews it with you for free, and you only pay if they win.",
     "Reassuring, practical, zero salesiness.", "Calm steady eye contact.", PRON_PLAIN),
    ("clip13", "You don't need records or an old report. It stays confidential, and most never see a courtroom.",
     "Encouraging, gentle.", "Soft open expression.", PRON_PLAIN),
    ("clip14", "The law changed so you can still come forward, but there are deadlines. In part two I'll tell you what happened when I finally spoke up.",
     "Caring urgency, warm, resolved.", "Small final nod.", PRON_PLAIN),
]


def last_word(s):
    import re
    t = re.findall(r"[A-Za-z']+", s)
    return t[-1] if t else ""


def gen(clip_id, line, tone, body, pron, mgid):
    out = OUT / f"{clip_id}.mp4"
    if out.exists() and out.stat().st_size > 50000:
        return clip_id, "cached", str(out)
    prompt = P(line, tone, body, pron, last_word(line))
    dur = 8 if len(line.split()) > 12 else 6
    r = generate_veo(prompt, image_mgid=mgid, duration=dur, seed=(abs(hash(clip_id)) % 9000))
    if r.get("status") != "success" or not r.get("urls"):
        return clip_id, "FAILED", str(r.get("raw"))[:200]
    download(r["urls"][0], str(out))
    return clip_id, "success", str(out)


def main():
    only = set(sys.argv[1:])
    by_id = {c[0]: c for c in CLIPS}

    host_mgid = upload_asset(HOST_IMG)
    print(f"[host] bed_b2 -> {host_mgid[:50]}...", flush=True)

    if only == {"clip01"} or not (OUT / "clip01.mp4").exists():
        cid, line, tone, body, pron = by_id["clip01"]
        print("=== clip01 (from bed_b2, FREE path) ===", flush=True)
        print(gen("clip01", line, tone, body, pron, host_mgid), flush=True)
        if only == {"clip01"}:
            return

    # eyes-open anchors off clip01, uploaded to google-flow
    adir = OUT / "anchors"
    if not list(adir.glob("_anchor_*.jpg")):
        adir.mkdir(parents=True, exist_ok=True)
        subprocess.run([".venv/bin/python", "scripts/pick_clean_anchors.py", str(OUT / "clip01.mp4"),
                        "--out-dir", str(adir), "--n", "8", "--prefix", "_anchor"], check=False)
    anchor_mgids = [upload_asset(str(a), "image/jpeg") for a in sorted(adir.glob("_anchor_*.jpg"))] or [host_mgid]
    print(f"[anchors] {len(anchor_mgids)} eyes-open frames", flush=True)

    rest = [c for c in CLIPS if c[0] != "clip01" and (not only or c[0] in only)]
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {}
        for i, (cid, line, tone, body, pron) in enumerate(rest):
            futs[ex.submit(gen, cid, line, tone, body, pron, anchor_mgids[i % len(anchor_mgids)])] = cid
        for f in as_completed(futs):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
