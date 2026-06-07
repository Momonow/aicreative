"""Story E (Illinois juvie storytime confession) — persona bed_b14.
Confession selfie register, in bed. KIE veo3_lite, FIRST_AND_LAST_FRAMES_2_VIDEO (anchor x2).
clip01 from the bed_b14 host image; clips 02-21 from eyes-open anchors rotated off clip01.
Lines segmented to ~8s (<=~20 words) for natural ~2.5 wps pacing.

Usage:
  python scripts/jdc_storytime_e_gen.py clip01          # TEST clip 1 only
  python scripts/jdc_storytime_e_gen.py                 # all (wave1 clip01 -> anchors -> wave2 rest)
"""
import sys, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kie_client import generate_veo, upload_file, download

SLUG = "illinois_jdc_storytime_e_b14"
OUT = Path(f"outputs/{SLUG}")
OUT.mkdir(parents=True, exist_ok=True)
HOST_IMG = "outputs/illinois_jdc_storytime_bed/reference/bed_b14.png"

# Shared locks. Character/setting are IN the anchor — do NOT re-describe them here.
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
NO on-screen text, NO captions, NO subtitles, NO watermark.
SPOKEN DIALOGUE (verbatim, stop after final word): "{line}\""""

PRON_SA = 'Say "SA\'ed" as the spoken letters "ess-ay-d" (S then A then a d), NOT "sad" and NOT "sside". "juvie" = "JOO-vee". "Illinois" = "ill-uh-NOY".'
PRON_PLAIN = "Natural clear American English."

# (id, line, tone, body, pron)
CLIPS = [
    ("clip01", "A guard SA'ed me at Illinois juvie. This is my story, and how I might finally be getting compensated for it.",
     "Heavy and bracing himself to say it out loud; the very end lifts with a faint flicker of hope.",
     "A slow swallow before he starts.", PRON_SA),
    ("clip02", "I was fifteen at Cook County. Did something dumb to land in there, but I was still just a kid.",
     "Matter-of-fact, a little defensive.", "Slight shrug in the shoulders.", '"Cook County" said plainly.'),
    ("clip03", "It wasn't even sneaky. Two of them would restrain me, walk me back to my cell, and that's when it happened.",
     "Quiet, harder to get out, eyes drop for a beat.", "Looks down, then back to the lens.", PRON_PLAIN),
    ("clip04", "It wasn't once. It was seven, eight times. I lost count.",
     "Hollow and numb.", "Almost no movement, a thousand-yard look.", PRON_PLAIN),
    ("clip05", "And when I fought back, when I said no, that only made it worse.",
     "Low, defeated, wounded; quiet and flat, the pitch stays low and steady, NOT raised, NOT angry.",
     "Eyes lower, a slow small head shake.", PRON_PLAIN),
    ("clip06", "They threw me in the hole. Twenty-four, forty-eight hours at a time. Punished me for what they were doing.",
     "Incredulous, anger rising; vocal stress lands on 'me' and 'they' (delivery only, words stay lowercase).", "Brows pull together.", PRON_PLAIN),
    ("clip07", "That's when I learned there was no winning in there. Fighting back just cost me more.",
     "Defeated, resigned.", "Eyes lower, slow exhale.", PRON_PLAIN),
    ("clip08", "I came home angry at everything and couldn't tell a soul why. Took me years to put words to it.",
     "Vulnerable and reflective.", "Soft, tired eyes back to the lens.", PRON_PLAIN),
    ("clip09", "It wasn't until last year I found out I wasn't the only one.",
     "A turn toward relief and validation.", "A small lift in the face.", PRON_PLAIN),
    ("clip10", "Nearly a thousand of us have come forward about what happened in these places.",
     "Steadier, gathering resolve.", "Slight nod.", PRON_PLAIN),
    ("clip11", "Out in California, Los Angeles County just settled cases like ours for almost five billion dollars.",
     "Informative, a spark of this-is-real.", "Eyebrows raise slightly.", '"Los Angeles" = "loss AN-juh-luss".'),
    ("clip12", "Survivors out there got anywhere from a hundred thousand up to three million each. Illinois is where that fight is now.",
     "Grounded, building hope.", "Steady gaze.", '"Illinois" = "ill-uh-NOY".'),
    ("clip13", "So if you went through sexual abuse while you were locked up in Cook County, Saint Charles, or Joliet, this is for you too.",
     "Direct to the viewer now, sincere and steady.", "Leans a touch closer to the lens.", '"Saint Charles" plainly; "Joliet" = "JOH-lee-et".'),
    ("clip14", "You may qualify for significant potential compensation.",
     "Plain and sincere, zero salesiness.", "Calm steady eye contact.", PRON_PLAIN),
    ("clip15", "If that's you, a lawyer who handles these reviews it with you for free.",
     "Reassuring, practical.", "Small reassuring nod.", PRON_PLAIN),
    ("clip16", "You never pay anything out of pocket, and they only get paid if they win for you.",
     "Reassuring, steady.", "Calm.", PRON_PLAIN),
    ("clip17", "You don't need records, paperwork, or an old report. Your word is enough to start.",
     "Encouraging.", "Soft open expression.", PRON_PLAIN),
    ("clip18", "And most of these get handled without you ever stepping into a courtroom.",
     "Reassuring.", "Slight nod.", PRON_PLAIN),
    ("clip19", "It stays confidential the whole way. Nobody in your life has to know.",
     "Gentle, protective.", "Soft, sincere.", PRON_PLAIN),
    ("clip20", "The law changed so you can still come forward, but there are deadlines.",
     "Caring urgency.", "A touch more intent in the eyes.", PRON_PLAIN),
    ("clip21", "In part two I'll tell you what I did next. But if this was you, don't wait. Tap the button right below.",
     "Warm and resolved, then a direct caring nudge to act; sincere, NOT salesy, NO upbeat ad inflection.",
     "Looks directly into the lens for the ask, small nod toward the button.", PRON_PLAIN),
    ("clip22", "Fill out the quick form. It takes thirty seconds. Just your name and number, and someone reaches out.",
     "Calm and reassuring, matter-of-fact about how easy it is; sincere, NOT salesy, NO TV-ad voice.",
     "Soft sincere eye contact, slight reassuring nod.", PRON_PLAIN),
]


def last_word(s):
    import re
    t = re.findall(r"[A-Za-z']+", s)
    return t[-1] if t else ""


def gen(clip_id, line, tone, body, pron, anchor_url):
    out = OUT / f"{clip_id}.mp4"
    if out.exists() and out.stat().st_size > 50000:
        return clip_id, "cached", str(out)
    prompt = P(line, tone, body, pron, last_word(line))
    r = generate_veo(prompt=prompt, aspect_ratio="9:16", image_urls=[anchor_url, anchor_url],
                     mode="FIRST_AND_LAST_FRAMES_2_VIDEO", model="veo3_lite", resolution="720p")
    if r.get("status") != "success" or not r.get("urls"):
        return clip_id, "FAILED", str(r.get("raw"))[:300]
    download(r["urls"][0], str(out))
    return clip_id, "success", str(out)


def main():
    only = set(sys.argv[1:])
    by_id = {c[0]: c for c in CLIPS}

    # clip01 always seeds from the host image
    host_url = upload_file(HOST_IMG)
    print(f"[host] uploaded bed_b14 -> {host_url[:60]}...", flush=True)

    if only == {"clip01"} or not (OUT / "clip01.mp4").exists():
        cid, line, tone, body, pron = by_id["clip01"]
        print("=== TEST: clip01 (from bed_b14) ===", flush=True)
        print(gen("clip01", line, tone, body, pron, host_url), flush=True)
        if only == {"clip01"}:
            return

    # anchors off clip01 (eyes-open rotation)
    adir = OUT / "anchors"
    if not list(adir.glob("_anchor_*.jpg")):
        adir.mkdir(parents=True, exist_ok=True)
        subprocess.run([".venv/bin/python", "scripts/pick_clean_anchors.py", str(OUT / "clip01.mp4"),
                        "--out-dir", str(adir), "--n", "8", "--prefix", "_anchor"], check=False)
    anchors = sorted(adir.glob("_anchor_*.jpg"))
    anchor_urls = [upload_file(str(a)) for a in anchors] or [host_url]
    print(f"[anchors] {len(anchor_urls)} eyes-open frames", flush=True)

    rest = [c for c in CLIPS if c[0] != "clip01" and (not only or c[0] in only)]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {}
        for i, (cid, line, tone, body, pron) in enumerate(rest):
            au = anchor_urls[i % len(anchor_urls)]   # rotate anchors
            futs[ex.submit(gen, cid, line, tone, body, pron, au)] = cid
        for f in as_completed(futs):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
