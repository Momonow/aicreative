"""Finalize Story C (b5, FREE google-flow path): trim -> WATERMARK-CROP -> static gain -> concat -> master.
Free tier burns a bottom-right "Veo" mark, so crop 664x1180 (center, off the bottom) and rescale to
clean 9:16 720x1280 (~8% zoom, no distortion). Output: outputs/illinois_jdc_storytime_f_b7/story_f_b7_final.mp4
"""
import json, subprocess, re, sys
from pathlib import Path

SRC = Path("outputs/illinois_jdc_storytime_f_b7")
WORK = SRC / "finalize"; WORK.mkdir(exist_ok=True)
CLIPS = [f"clip{n:02d}" for n in range(1, 15)]
TARGET_CLIP = -18.0
TARGET_MASTER = -16.0
# crop off the bottom-right "Veo" watermark, rescale to clean 9:16
VF = "crop=664:1180:28:0,scale=720:1280,setsar=1,fps=24"


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def measure_i(path):
    p = subprocess.run(["ffmpeg", "-i", str(path), "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    t = p.stderr
    return float(json.loads(t[t.rfind("{"):t.rfind("}") + 1])["input_i"])


def main():
    only = sys.argv[1:]
    clips = [c for c in CLIPS if not only or c in only]

    print("== trim + watermark-crop + gain ==", flush=True)
    for cid in clips:
        src = SRC / f"{cid}.mp4"
        if not src.exists():
            print(f"  {cid} MISSING — skipping", flush=True); continue
        trans = Path(f"outputs/jdc_f_b7_{cid}/transcript.json")
        if trans.exists():
            subprocess.run([".venv/bin/python", "scripts/trim_silence.py", str(src), str(trans),
                            "--lead", "0.10", "--tail", "0.25"], check=True, capture_output=True, text=True)
            tr = SRC / f"{cid}_trimmed.mp4"
        else:
            tr = src  # no transcript -> use raw
        i = measure_i(tr)
        gain = TARGET_CLIP - i
        out = WORK / f"{cid}.mp4"
        run(["ffmpeg", "-y", "-i", str(tr), "-vf", VF, "-af", f"volume={gain:.2f}dB",
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)])
        print(f"  {cid}: {i:.1f} LUFS -> {gain:+.1f}dB (cropped+rescaled)", flush=True)

    print("== concat ==", flush=True)
    present = [c for c in clips if (WORK / f"{c}.mp4").exists()]
    listf = WORK / "concat.txt"
    listf.write_text("".join(f"file '{(WORK / f'{c}.mp4').resolve()}'\n" for c in present))
    stitched = WORK / "stitched.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(stitched)])

    print("== master ==", flush=True)
    mi = measure_i(stitched)
    final = SRC / "story_f_b7_final.mp4"
    run(["ffmpeg", "-y", "-i", str(stitched),
         "-af", f"volume={TARGET_MASTER - mi:.2f}dB,alimiter=limit=0.794:level=disabled:asc=1",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final)])

    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout.strip()
    st = subprocess.run(["ffmpeg", "-i", str(final), "-af", "astats=metadata=1:reset=0", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    print(f"\nFINAL: {final}\n  dur {dur}s  {measure_i(final):.1f} LUFS  "
          f"peak {re.findall(r'Peak level dB:\\s*([-\\d.]+)', st)}  flat {re.findall(r'Flat factor:\\s*([-\\d.]+)', st)}")


if __name__ == "__main__":
    main()
