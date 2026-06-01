"""Finalize Story E (b14): word-aware trim -> per-clip static gain -> concat -> master limiter.
No voice_changer (single persona, same anchor -> Veo voice already consistent; raw Veo is cleaner).
Output: outputs/illinois_jdc_storytime_e_b14/story_e_b14_final.mp4
"""
import json, subprocess, re, sys
from pathlib import Path

SRC = Path("outputs/illinois_jdc_storytime_e_b14")
WORK = SRC / "finalize"; WORK.mkdir(exist_ok=True)
CLIPS = [f"clip{n:02d}" for n in range(1, 23)]
TARGET_CLIP = -18.0
TARGET_MASTER = -16.0


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def measure_i(path):
    p = subprocess.run(["ffmpeg", "-i", str(path), "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    t = p.stderr
    j = t[t.rfind("{"):t.rfind("}") + 1]
    return float(json.loads(j)["input_i"])


def main():
    # 1) word-aware trim each clip
    print("== trim ==", flush=True)
    for cid in CLIPS:
        src = SRC / f"{cid}.mp4"
        trans = Path(f"outputs/jdc_e_b14_{cid}/transcript.json")
        subprocess.run([".venv/bin/python", "scripts/trim_silence.py", str(src), str(trans),
                        "--lead", "0.10", "--tail", "0.25"], check=True, capture_output=True, text=True)
        tr = SRC / f"{cid}_trimmed.mp4"
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(tr)], capture_output=True, text=True).stdout.strip()
        print(f"  {cid} trimmed -> {dur}s", flush=True)

    # 2) per-clip static gain to TARGET_CLIP, uniform re-encode
    print("== normalize (static gain) ==", flush=True)
    for cid in CLIPS:
        tr = SRC / f"{cid}_trimmed.mp4"
        i = measure_i(tr)
        gain = TARGET_CLIP - i
        out = WORK / f"{cid}.mp4"
        run(["ffmpeg", "-y", "-i", str(tr),
             "-vf", "scale=720:1280,setsar=1,fps=24",
             "-af", f"volume={gain:.2f}dB",
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)])
        print(f"  {cid}: {i:.1f} LUFS -> gain {gain:+.1f}dB", flush=True)

    # 3) concat (copy)
    print("== concat ==", flush=True)
    listf = WORK / "concat.txt"
    listf.write_text("".join(f"file '{(WORK / f'{c}.mp4').resolve()}'\n" for c in CLIPS))
    stitched = WORK / "stitched.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(stitched)])

    # 4) master: static gain to TARGET_MASTER + true-peak limiter
    print("== master ==", flush=True)
    mi = measure_i(stitched)
    mgain = TARGET_MASTER - mi
    final = SRC / "story_e_b14_final.mp4"
    run(["ffmpeg", "-y", "-i", str(stitched),
         "-af", f"volume={mgain:.2f}dB,alimiter=limit=0.794:level=disabled:asc=1",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final)])
    print(f"  master: {mi:.1f} LUFS -> gain {mgain:+.1f}dB", flush=True)

    # 5) verify
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout.strip()
    st = subprocess.run(["ffmpeg", "-i", str(final), "-af", "astats=metadata=1:reset=0", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    peaks = re.findall(r"Peak level dB:\s*([-\d.]+)", st)
    flats = re.findall(r"Flat factor:\s*([-\d.]+)", st)
    lufs = measure_i(final)
    print(f"\nFINAL: {final}")
    print(f"  duration: {dur}s   integrated: {lufs:.1f} LUFS")
    print(f"  peak dB: {peaks}   flat factor: {flats}")


if __name__ == "__main__":
    main()
