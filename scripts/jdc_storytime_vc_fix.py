"""Voice-unify a free-path storytime ad (clips have cross-clip voice drift).
Clone the persona voice from its cleanest clips -> voice_changer every clip -> re-gain -> re-stitch.
Outputs story_<x>_final_vc.mp4 (keeps the raw final for A/B).

  python scripts/jdc_storytime_vc_fix.py a    # Story A (b1)
  python scripts/jdc_storytime_vc_fix.py b    # Story B (b2)
"""
import sys, subprocess, json, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from elevenlabs_client import clone_voice, voice_changer

CFG = {
    # story: (slug, persona, finalstem, reuse_voice_id)  -- reuse existing clones (account at 30/30)
    "a": ("illinois_jdc_storytime_a_b1", "b1", "story_a_b1_final", "2nT64nF1gSMWc5jDr97U"),  # jdc_p1_young_clean
    "b": ("illinois_jdc_storytime_b_b2", "b2", "story_b_b2_final", "qa8eVHMu37gMYzEvO5gb"),  # jdc_p2_guarded_clean
}
story = sys.argv[1]
slug, persona, finalstem, REUSE_VOICE_ID = CFG[story]
SRC = Path(f"outputs/{slug}")
WORK = SRC / "finalize"
VC = SRC / "vc"; VC.mkdir(exist_ok=True)
CLIPS = [f"clip{n:02d}" for n in range(1, 15)]
TARGET_CLIP = -18.0
TARGET_MASTER = -16.0


def run(cmd): subprocess.run(cmd, check=True, capture_output=True, text=True)
def measure_i(p):
    r = subprocess.run(["ffmpeg", "-i", str(p), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(json.loads(r[r.rfind("{"):r.rfind("}") + 1])["input_i"])
def centroid(p):
    import librosa, numpy as np
    wav = VC / f"_c_{Path(p).stem}.wav"
    run(["ffmpeg", "-y", "-i", str(p), "-vn", "-ar", "22050", "-ac", "1", str(wav)])
    y, sr = librosa.load(str(wav), sr=22050)
    return float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))


def main():
    present = [c for c in CLIPS if (WORK / f"{c}.mp4").exists()]
    # Reuse an existing JDC clone (account at 30/30 voice slots — no room to clone, no deletion).
    voice_id = REUSE_VOICE_ID
    print(f"[voice] reusing existing clone {voice_id}", flush=True)

    # 2) voice_changer each clip's audio (ElevenLabs 5-concurrent -> 4 workers)
    def vc_one(c):
        src = WORK / f"{c}.mp4"
        a_in = VC / f"_in_{c}.mp3"; a_out = VC / f"{c}_vc.mp3"
        if not a_out.exists():
            run(["ffmpeg", "-y", "-i", str(src), "-vn", "-ar", "44100", "-ac", "1", "-b:a", "192k", str(a_in)])
            voice_changer(str(a_in), voice_id, str(a_out), model_id="eleven_english_sts_v2",
                          stability=0.5, similarity_boost=0.70)
        # gain to TARGET_CLIP, re-mux with original video
        i = measure_i(a_out); gain = TARGET_CLIP - i
        out = VC / f"{c}.mp4"
        run(["ffmpeg", "-y", "-i", str(src), "-i", str(a_out),
             "-filter_complex", f"[1:a]volume={gain:.2f}dB[a]", "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)])
        return c, f"{i:.1f}->{gain:+.1f}dB"

    print("[vc] voice_changer all clips...", flush=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        for f in as_completed({ex.submit(vc_one, c): c for c in present}):
            print("  ", f.result(), flush=True)

    # 3) concat + master
    listf = VC / "concat.txt"
    listf.write_text("".join(f"file '{(VC / f'{c}.mp4').resolve()}'\n" for c in present))
    stitched = VC / "stitched.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(stitched)])
    mi = measure_i(stitched)
    final = SRC / f"{finalstem}_vc.mp4"
    run(["ffmpeg", "-y", "-i", str(stitched), "-af",
         f"volume={TARGET_MASTER - mi:.2f}dB,alimiter=limit=0.794:level=disabled:asc=1",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final)])
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(final)], capture_output=True, text=True).stdout.strip()
    print(f"\nVC FINAL: {final}  dur {dur}s  {measure_i(final):.1f} LUFS", flush=True)


if __name__ == "__main__":
    main()
