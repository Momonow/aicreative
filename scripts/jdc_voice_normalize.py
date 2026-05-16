"""Voice-normalize B and C via ElevenLabs voice_changer.

Per CLAUDE.md tier-2 recipe:
  1. Extract clip 1 mp3 per persona → voice clone source
  2. Clone voice → voice_id per persona
  3. Extract original mp3 from each clip
  4. voice_changer(clip_audio, voice_id) → unified-timbre mp3 per clip
  5. Re-mux: keep video, swap audio
  6. Re-loudnorm (voice_changer can drift loudness)

Output:
  outputs/illinois_jdc_<slug>/clip{N}_vc.mp4         — video + voice-changed audio
  outputs/illinois_jdc_<slug>/clip{N}_vc_norm.mp4    — same, post-loudnorm

ElevenLabs concurrent limit: 5. Use max_workers=4.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from elevenlabs_client import clone_voice, voice_changer

PERSONAS = ["blue_collar", "stoop_calm"]
OUT_ROOT = Path("outputs")


def extract_mp3(video_path, mp3_path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path),
         "-vn", "-ar", "44100", "-ac", "1", "-q:a", "2", str(mp3_path)],
        check=True, capture_output=True,
    )
    return mp3_path


def remux(video_path, mp3_path, out_path):
    """Replace audio track on video_path with mp3_path → out_path."""
    subprocess.run(
        ["ffmpeg", "-y",
         "-i", str(video_path), "-i", str(mp3_path),
         "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest",
         str(out_path)],
        check=True, capture_output=True,
    )
    return out_path


def loudnorm(video_path, out_path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path),
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         str(out_path)],
        check=True, capture_output=True,
    )
    return out_path


def main():
    # Step 1: extract clip 1 mp3 as cloning source
    sources = {}
    for slug in PERSONAS:
        d = OUT_ROOT / f"illinois_jdc_{slug}"
        src_mp3 = d / "clip1_source.mp3"
        extract_mp3(d / "clip1.mp4", src_mp3)
        sources[slug] = src_mp3
        print(f"[{slug}] cloning source extracted: {src_mp3}")

    # Step 2: clone voice per persona
    voice_ids = {}
    for slug in PERSONAS:
        vid = clone_voice(
            name=f"jdc_{slug}_v1",
            sample_files=[str(sources[slug])],
            description=f"Illinois JDC ad persona {slug} cloned from clip 1",
        )
        voice_ids[slug] = vid
        # persist
        (OUT_ROOT / f"illinois_jdc_{slug}" / "voice_id.txt").write_text(vid)

    # Step 3: extract original mp3 from each clip
    orig_audios = []
    for slug in PERSONAS:
        for idx in (1, 2, 3):
            d = OUT_ROOT / f"illinois_jdc_{slug}"
            in_mp4 = d / f"clip{idx}.mp4"
            orig_mp3 = d / f"clip{idx}_orig.mp3"
            extract_mp3(in_mp4, orig_mp3)
            orig_audios.append((slug, idx, orig_mp3))
            print(f"[{slug} clip{idx}] orig audio extracted")

    # Step 4: voice_changer in parallel (4 workers — under EL's 5-concurrent cap)
    def vc(job):
        slug, idx, orig_mp3 = job
        vc_mp3 = OUT_ROOT / f"illinois_jdc_{slug}" / f"clip{idx}_vc.mp3"
        try:
            voice_changer(
                str(orig_mp3),
                voice_ids[slug],
                str(vc_mp3),
                model_id="eleven_multilingual_sts_v2",
                stability=0.5,
                similarity_boost=0.85,
            )
            return slug, idx, vc_mp3, None
        except Exception as e:
            return slug, idx, None, str(e)

    print("\n--- voice_changer (4 parallel) ---")
    vc_results = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        for f in as_completed([ex.submit(vc, j) for j in orig_audios]):
            slug, idx, mp3, err = f.result()
            if err:
                print(f"[{slug} clip{idx}] VC FAILED: {err}")
            else:
                vc_results[(slug, idx)] = mp3
                print(f"[{slug} clip{idx}] vc done")

    # Step 5: remux + Step 6: re-loudnorm per clip
    print("\n--- remux + re-loudnorm ---")
    for (slug, idx), vc_mp3 in vc_results.items():
        d = OUT_ROOT / f"illinois_jdc_{slug}"
        vc_mp4 = d / f"clip{idx}_vc.mp4"
        vc_norm_mp4 = d / f"clip{idx}_vc_norm.mp4"
        remux(d / f"clip{idx}.mp4", vc_mp3, vc_mp4)
        loudnorm(vc_mp4, vc_norm_mp4)
        print(f"[{slug} clip{idx}] → {vc_norm_mp4}")


if __name__ == "__main__":
    main()
