"""Normalize Omni voice drift without changing native video timing.

Each ad gets a separate instant voice clone from two central, clean clips. Speech-to-speech
then replaces only the audio while retaining the original timing and mouth movements.
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elevenlabs_client import clone_voice, voice_changer


ROOT = Path("outputs/depo_meningioma_openers_omni")
ADS = {
    "not_symptoms": {"clone_clips": (3, 4)},
    "records_word": {"clone_clips": (1, 2)},
}


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, **kwargs)


def extract_audio(video, out):
    run([
        "ffmpeg", "-y", "-i", str(video), "-vn", "-ar", "44100", "-ac", "1",
        "-c:a", "libmp3lame", "-b:a", "192k", str(out),
    ], capture_output=True)


def join_audio(inputs, out):
    source_list = out.with_name(f"{out.stem}_list.txt")
    source_list.write_text("".join(f"file '{path.resolve()}'\n" for path in inputs))
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(source_list),
        "-c", "copy", str(out),
    ], capture_output=True)


def remux(video, audio, out):
    run([
        "ffmpeg", "-y", "-i", str(video), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-ar", "44100",
        "-b:a", "192k", "-shortest", str(out),
    ], capture_output=True)


def static_level(src, out):
    measured = run([
        "ffmpeg", "-i", str(src), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ], capture_output=True, text=True)
    match = re.search(r"\{\s*\"input_i\".*?\n\}", measured.stderr, re.S)
    if not match:
        raise RuntimeError(f"Could not measure loudness for {src}")
    input_i = float(json.loads(match.group(0))["input_i"])
    gain = -16.0 - input_i
    run([
        "ffmpeg", "-y", "-i", str(src),
        "-af", f"volume={gain:.2f}dB,alimiter=limit=0.891:level=disabled",
        "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-b:a", "192k", str(out),
    ], capture_output=True)


def make_voice_id(slug, clips, work):
    cache = work / "voice_id.txt"
    if cache.exists() and cache.read_text().strip():
        return cache.read_text().strip()
    sources = []
    for idx in ADS[slug]["clone_clips"]:
        audio = work / f"clone_clip{idx:02d}.mp3"
        extract_audio(clips[idx - 1], audio)
        sources.append(audio)
    joined = work / "clone_source.mp3"
    join_audio(sources, joined)
    voice_id = clone_voice(
        f"depo_{slug}_persona_v1",
        [str(joined)],
        description=f"Depo-Provera meningioma ad persona for {slug}",
    )
    cache.write_text(voice_id)
    return voice_id


def finalize(slug):
    ad_dir = ROOT / slug
    work = ad_dir / "voice_consistency"
    work.mkdir(exist_ok=True)
    clips = [ad_dir / f"clip{idx:02d}.mp4" for idx in range(1, 6)]
    if not all(path.exists() for path in clips):
        raise RuntimeError(f"Missing source clips for {slug}")
    voice_id = make_voice_id(slug, clips, work)

    jobs = []
    for idx, clip in enumerate(clips, 1):
        source_audio = work / f"clip{idx:02d}_source_native.mp3"
        if not source_audio.exists():
            extract_audio(clip, source_audio)
        changed_audio = work / f"clip{idx:02d}_changed_native.mp3"
        jobs.append((idx, clip, source_audio, changed_audio))

    def change(job):
        idx, source_video, source_audio, changed_audio = job
        if not changed_audio.exists() or changed_audio.stat().st_size < 50000:
            voice_changer(
                str(source_audio), voice_id, str(changed_audio),
                model_id="eleven_english_sts_v2", stability=0.5, similarity_boost=0.70,
                output_format="mp3_44100_192", use_speaker_boost=False,
            )
        remuxed = work / f"clip{idx:02d}_voice.mp4"
        remux(source_video, changed_audio, remuxed)
        return idx, remuxed

    remuxed = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(change, job) for job in jobs]
        for future in as_completed(futures):
            idx, path = future.result()
            remuxed[idx] = path

    source_list = work / "voice_concat.txt"
    source_list.write_text("".join(f"file '{remuxed[idx].resolve()}'\n" for idx in range(1, 6)))
    raw = work / "voice_consistent_raw.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(source_list), "-c", "copy", str(raw)], capture_output=True)
    final = ROOT / f"{slug}_white_distinct_person_omni_voice_consistent.mp4"
    static_level(raw, final)
    print(final)


if __name__ == "__main__":
    for ad_slug in ADS:
        finalize(ad_slug)
