"""Depo meningioma-focused 30s openers on omni-flash.

White-woman first pass for scripts #2/#3/#4 from the meningioma opener brainstorm.
Each ad uses a different KIE gpt-image-2 persona anchor, then short UGC clips via
useapi Google Flow omni-flash i2v startImage. Final outputs are clean masters, no captions.

Run:
  .venv/bin/python scripts/depo_meningioma_openers_omni.py
  .venv/bin/python scripts/depo_meningioma_openers_omni.py --only spell_it
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import kie_client
from elevenlabs_client import scribe_whisper_compat as scribe
from googleflow_client import download, generate_veo, upload_asset


OUT = Path("outputs/depo_meningioma_openers_omni")
MODEL = "omni-flash"

PERSONAS = {
    "spell_it": {
        "anchor": OUT / "white_woman_anchor.png",
        "voice_context": "Calm, serious, plain-spoken adult American voice, warm but direct, not announcer-like and not theatrical. Keep the same voice throughout.",
        "prompt": """Subject: an ordinary white woman around 52 years old, fair skin with faint freckles and mild sun damage, shoulder-length light brown hair with grey roots tucked loosely behind one ear, tired blue-grey eyes, slight under-eye darkness, average build, no makeup or minimal makeup, small silver hoop earrings. She wears a soft faded blue cardigan over a plain white t-shirt. She is seated in a modest real home kitchen/living-room corner, warm late-afternoon window light, plain wood table edge visible, beige wall, a few out-of-focus family photos in the background with no readable text. Chest-up vertical selfie framing, face fully visible, mouth unobstructed, hands low and mostly out of frame. Expression calm, serious, a little worn down, like someone about to explain something personal and important.

Photoreal candid vertical 9:16 selfie-style documentary photo, shot on a front phone camera, available light only. Ordinary everyday-looking woman, not glamour, not influencer, not celebrity. Natural skin texture with visible pores, fine lines, uneven tone, no beauty retouching, no smoothing, no filter. No on-screen text, no captions, no watermark, no logo."""
    },
    "not_symptoms": {
        "anchor": OUT / "white_woman_not_symptoms_anchor.png",
        "voice_context": "Firm but caring plain-spoken adult American voice, direct and corrective without sounding cold. Keep the same voice throughout.",
        "prompt": """Subject: an ordinary white woman around 47 years old, fair skin with a little redness in the cheeks, short practical auburn-brown hair tucked behind one ear, hazel-green eyes, average build, no makeup or very minimal makeup, faint forehead lines and natural skin texture. She wears a dark charcoal zip hoodie over a muted green t-shirt. She is seated near a laundry-room doorway in a modest home, soft daylight from the side, off-white wall, a folded towel stack and a plain cabinet blurred in the background with no readable text. Chest-up vertical selfie framing, face fully visible, mouth unobstructed, hands low and mostly out of frame. Expression serious, focused, a little protective, like she is correcting a common misunderstanding for someone she cares about.

Photoreal candid vertical 9:16 selfie-style documentary photo, shot on a front phone camera, available light only. Ordinary everyday-looking woman, not glamour, not influencer, not celebrity. Natural skin texture with visible pores, fine lines, uneven tone, no beauty retouching, no smoothing, no filter. No on-screen text, no captions, no watermark, no logo."""
    },
    "records_word": {
        "anchor": OUT / "white_woman_records_word_anchor.png",
        "voice_context": "Practical, calm, plain-spoken adult American voice, steady and reassuring without sounding polished. Keep the same voice throughout.",
        "prompt": """Subject: an ordinary white woman around 58 years old, fair skin with sun spots and natural wrinkles, chin-length grey-blonde hair loosely clipped back, pale blue eyes, average build, clear reading glasses pushed up on her head, no makeup or minimal makeup. She wears a washed burgundy cardigan over a plain grey shirt. She is seated at a modest dining table in a real home, afternoon window light, a closed laptop edge and a small stack of papers blurred low in the frame with no readable text, simple cream wall and wooden chair in the background. Chest-up vertical selfie framing, face fully visible, mouth unobstructed, hands low and mostly out of frame. Expression calm, practical, slightly tired, like she is walking someone through a private next step.

Photoreal candid vertical 9:16 selfie-style documentary photo, shot on a front phone camera, available light only. Ordinary everyday-looking woman, not glamour, not influencer, not celebrity. Natural skin texture with visible pores, fine lines, uneven tone, no beauty retouching, no smoothing, no filter. No on-screen text, no captions, no watermark, no logo."""
    },
    "post_op_scar": {
        "anchor": OUT / "white_woman_post_op_scar_anchor.png",
        "voice_context": "Quiet, plain-spoken adult American voice, serious and steady, slightly fatigued, not dramatic or polished. Keep the same voice throughout.",
        "prompt": """Use case: ads-marketing, photorealistic-natural.
Asset type: post-operative UGC persona anchor for a meningioma legal-awareness video.

An ordinary white woman around 50 years old sitting upright in a real hospital bed shortly after surgery to remove a diagnosed intracranial brain meningioma. She is nearly bald: most of her scalp has been freshly shaved, with only a little short light-brown hair remaining near the back and lower sides. A clearly visible curved cranial incision runs from above her right temple toward the upper side of her scalp, closed with neat dark surgical stitches. The incision is recent and noticeable, with mild pinkness and slight post-operative swelling, but it is clean, dry, respectful, and non-graphic. No blood, no open wound, no drainage.

She has tired blue eyes, natural redness, under-eye fatigue, no makeup, realistic pores and uneven skin tone. She wears a plain pale hospital gown and sits against white pillows. A hospital bed rail and softly blurred IV pole and monitor are visible behind her, with no readable text. Soft daylight mixed with ordinary hospital lighting.

Chest-up vertical phone-camera framing, face fully visible, mouth unobstructed, hands low and mostly outside frame. She looks directly into the lens with a tired, serious, steady expression, like she is ready to explain something personal after a difficult operation. Ordinary patient, not glamorous, not an influencer, not a celebrity. No beauty retouching, no smoothing, no filter.

Photoreal candid vertical 9:16 documentary photograph. No text, captions, logo, watermark, blood, exposed tissue, open wound, dramatic gore, or exaggerated suffering."""
    },
}

ADS = {
    "spell_it": {
        "title": "Meningioma. Learn The Word.",
        "tone": "quiet, direct, careful, like explaining one important medical word to a friend",
        "chunks": [
            "Meningioma after Depo-Provera may qualify for significant compensation. Listen closely.",
            "If you had to learn how to spell that word, this may be for you.",
            "This is for women whose records say brain meningioma.",
            "Not every diagnosis. Not every health problem. That specific word matters.",
            "If you were on the Depo shot for a year or more, you may qualify for significant financial compensation. Check the private page today.",
        ],
    },
    "not_symptoms": {
        "title": "Not Symptoms. A Diagnosis.",
        "tone": "firm filter-first warning, plain and corrective without sounding cold",
        "chunks": [
            "Brain meningioma after Depo-Provera may qualify for significant compensation.",
            "This is not for headaches. Not feeling off. Not guessing.",
            "This is for one specific diagnosis in your records.",
            "If you were on the shot for a year or more, those facts may matter.",
            "Check the page below and see where you stand.",
        ],
    },
    "records_word": {
        "title": "Look In Your Records.",
        "tone": "practical and calm, walking the viewer through one small next step",
        "chunks": [
            "Meningioma in your records after Depo-Provera may qualify for significant compensation.",
            "So pull up your records and look for that word.",
            "If it is there, do not scroll past this.",
            "Even if it happened years ago, or old shot records are missing.",
            "Checking is free and private. Tap below and see where you stand.",
        ],
    },
    "post_op_scar": {
        "title": "After Brain Surgery.",
        "tone": "post-surgery recovery, restrained and personal without becoming graphic or sensational",
        "chunks": [
            "If you had brain surgery for a brain meningioma after Depo-Provera, listen closely.",
            "That scar is not what qualifies you by itself.",
            "What matters is the diagnosis in your records: brain meningioma.",
            "And if you were on the Depo shot for a year or more, you may qualify for significant compensation.",
            "Answer a few private questions and see where you stand.",
        ],
    },
}


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, **kwargs)


def ensure_anchor(ad_slug, regen=False):
    OUT.mkdir(parents=True, exist_ok=True)
    persona = PERSONAS[ad_slug]
    anchor = persona["anchor"]
    if anchor.exists() and anchor.stat().st_size > 50000 and not regen:
        return anchor
    print(f"[persona:{ad_slug}] KIE gpt-image-2 2K 9:16", flush=True)
    result = kie_client.generate_gpt_image(persona["prompt"], aspect_ratio="9:16", resolution="2K")
    if result.get("status") != "success" or not result.get("urls"):
        raise RuntimeError(f"persona generation failed: {result.get('raw')}")
    kie_client.download(result["urls"][0], str(anchor))
    return anchor


def dur_for(line):
    words = len(line.split())
    if words <= 8:
        return 4
    if words <= 13:
        return 6
    return 8


def last_word(line):
    words = re.findall(r"[A-Za-z']+", line)
    return words[-1] if words else ""


def video_prompt(line, tone, voice_context):
    return f"""Use the supplied first frame as the sole visual source of truth. Continue that exact frame as a fixed-camera video. Do not redesign, restage, beautify, age-shift, or reinterpret any visible detail. Identity, face geometry, hair, eyes, skin texture, wardrobe, setting, lighting, framing, and camera position must remain unchanged from the supplied frame. No zoom, pan, reframing, cuts, or camera drift.

ACTION: She looks into the phone lens, blinks naturally, and speaks with restrained facial movement and only small natural gestures. Her mouth remains visible. TONE: {tone}.

VOICE: {voice_context} Clear close phone-mic audio. Natural conversational pace around 2.4 words per second. Pronounce "meningioma" as "men-in-jee-OH-muh" and "Depo" as "DEP-oh" with a short e like in "deck," not "depot."

DIALOGUE: Say only the supplied dialogue verbatim, with no extra or repeated words, then stop after "{last_word(line)}." No screen text, captions, subtitles, watermark, logo, or music.

SPOKEN DIALOGUE: {line}"""


def transcribe_clip(path):
    wav = path.with_suffix(".wav")
    run(["ffmpeg", "-y", "-i", str(path), "-vn", "-ar", "16000", "-ac", "1", str(wav)],
        capture_output=True)
    try:
        result = scribe(str(wav), biased_keywords=["meningioma", "Depo-Provera", "Depo"], language_code="en")
        return result.get("text", ""), result
    finally:
        try:
            wav.unlink()
        except FileNotFoundError:
            pass


def existing_clip_is_current(out, transcript_path, line):
    if not out.exists() or out.stat().st_size <= 50000 or not transcript_path.exists():
        return False
    try:
        data = json.loads(transcript_path.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    return data.get("intended") == line


def acceptable(text, line):
    t = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    must = []
    if "meningioma" in line.lower():
        must.append("meningioma")
    if "depo" in line.lower():
        must.append("depo")
    if "significant" in line.lower() and "compensation" in line.lower():
        must.extend(["significant", "compensation"])
    if "may qualify" in line.lower():
        must.append("may")
        must.append("qualif")
    if "were on the" in line.lower():
        must.append("were")
    return all(m in t for m in must)


def gen_clip(ad_slug, idx, line, tone, voice_context, mgid, retries=3):
    ad_dir = OUT / ad_slug
    ad_dir.mkdir(parents=True, exist_ok=True)
    out = ad_dir / f"clip{idx:02d}.mp4"
    transcript_path = ad_dir / f"clip{idx:02d}_transcript.json"
    if existing_clip_is_current(out, transcript_path, line):
        return out
    if out.exists():
        out.unlink()
    prompt = video_prompt(line, tone, voice_context)
    for attempt in range(1, retries + 1):
        print(f"[{ad_slug}] clip{idx:02d} attempt {attempt} ({MODEL}, {dur_for(line)}s)", flush=True)
        result = generate_veo(
            prompt=prompt,
            image_mgid=mgid,
            duration=dur_for(line),
            aspect_ratio="portrait",
            model=MODEL,
            attempts=1,
            ref_param="startImage",
        )
        if result.get("status") != "success" or not result.get("urls"):
            print(f"  failed: {str(result.get('raw'))[:160]}", flush=True)
            time.sleep(5)
            continue
        tmp = ad_dir / f"_clip{idx:02d}_attempt{attempt}.mp4"
        download(result["urls"][0], str(tmp))
        text, tr = transcribe_clip(tmp)
        transcript_path.write_text(json.dumps({"intended": line, "text": text, "raw": tr}, indent=2))
        print(f"  transcript: {text}", flush=True)
        if acceptable(text, line):
            tmp.replace(out)
            return out
        print("  transcript missing a locked keyword; rerolling", flush=True)
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
    raise RuntimeError(f"{ad_slug} clip{idx:02d} failed after retries")


def trim_activity(src, dest):
    duration = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
        capture_output=True, text=True, check=True,
    ).stdout.strip())
    sd = subprocess.run(
        ["ffmpeg", "-i", str(src), "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    silence_ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", sd)]
    silence_starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", sd)]
    start = 0.0
    end = duration
    if silence_ends and (not silence_starts or silence_starts[0] < 0.2):
        start = max(0.0, silence_ends[0] - 0.04)
    if silence_starts and silence_starts[-1] > start + 0.4:
        end = min(duration, silence_starts[-1] + 0.08)
    run([
        "ffmpeg", "-y", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{max(0.2, end - start):.3f}",
        "-vf", "scale=720:1280,fps=24,setsar=1", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-ar", "44100", "-b:a", "192k", str(dest),
    ], capture_output=True)


def assemble(ad_slug, clips):
    ad_dir = OUT / ad_slug
    trims = []
    for i, clip in enumerate(clips, 1):
        trim = ad_dir / f"_trim{i:02d}.mp4"
        trim_activity(clip, trim)
        trims.append(trim)
    concat = ad_dir / "_concat.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in trims))
    raw = ad_dir / "_raw_concat.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(raw)],
        capture_output=True)
    final = OUT / f"{ad_slug}_white_distinct_person_omni_clean.mp4"
    run([
        "ffmpeg", "-y", "-i", str(raw),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.891:level=disabled",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final),
    ], capture_output=True)
    return final


def assemble_native_full(ad_slug, clips):
    """Join accepted model clips without retiming, frame padding, or activity trimming."""
    ad_dir = OUT / ad_slug
    concat = ad_dir / "_native_full_concat.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in clips))
    raw = ad_dir / "_native_full_raw.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(raw)],
        capture_output=True)

    measured = subprocess.run([
        "ffmpeg", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ], capture_output=True, text=True, check=True)
    match = re.search(r"\{\s*\"input_i\".*?\n\}", measured.stderr, re.S)
    if not match:
        raise RuntimeError(f"Could not measure loudness for {raw}")
    input_i = float(json.loads(match.group(0))["input_i"])
    gain = -16.0 - input_i

    final = OUT / f"{ad_slug}_white_distinct_person_omni_native_full.mp4"
    run([
        "ffmpeg", "-y", "-i", str(raw),
        "-af", f"volume={gain:.2f}dB,alimiter=limit=0.891:level=disabled",
        "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-b:a", "192k", str(final),
    ], capture_output=True)
    return final


def generate_ad(ad_slug, regen_persona=False):
    ad = ADS[ad_slug]
    anchor = ensure_anchor(ad_slug, regen_persona)
    mgid = upload_asset(str(anchor), "image/png")
    clips = []
    print(f"=== {ad_slug}: {ad['title']} ===", flush=True)
    for idx, line in enumerate(ad["chunks"], 1):
        clips.append(gen_clip(ad_slug, idx, line, ad["tone"], PERSONAS[ad_slug]["voice_context"], mgid))
    final = assemble(ad_slug, clips)
    print(f"[done] {ad_slug} -> {final}", flush=True)
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="Comma-separated slugs")
    ap.add_argument("--regen-persona", action="store_true")
    args = ap.parse_args()
    slugs = list(ADS)
    if args.only:
        wanted = {s.strip() for s in args.only.split(",") if s.strip()}
        slugs = [s for s in slugs if s in wanted]
    finals = [str(generate_ad(slug, args.regen_persona)) for slug in slugs]
    print("\nFINALS:")
    for f in finals:
        print(f)


if __name__ == "__main__":
    main()
