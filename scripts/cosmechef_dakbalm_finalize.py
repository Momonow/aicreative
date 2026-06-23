"""
Finalize DAK BALM 30s ad:
  1. per-clip static gain -> -16 LUFS (even loudness, no pumping)
  2. concat the 4 normalized trimmed clips
  3. crop the Veo free-tier watermark once (720x1280 -> crop 675x1200 top-left -> scale 720x1280, ratio preserved)
  4. true-peak limiter on the master
"""
import json, re, subprocess
from pathlib import Path

DIR = Path("outputs/cosmechef_dakbalm")
TRIM = DIR / "trimmed"
NORM = DIR / "norm"; NORM.mkdir(parents=True, exist_ok=True)
FINAL = DIR / "cosmechef_dakbalm_testimonial_30s.mp4"
TARGET_LUFS = -16.0


def lufs(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "loudnorm=I=-16:TP=-1.5:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r'"input_i"\s*:\s*"(-?[0-9.]+)"', r.stderr)
    return float(m[0]) if m else None


# 1. per-clip gain
norm_files = []
for n in (1, 2, 3, 4):
    src = TRIM / f"clip{n}_trim.mp4"
    g = TARGET_LUFS - lufs(src)
    dst = NORM / f"clip{n}_norm.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(src), "-af", f"volume={g:.2f}dB",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(dst)], capture_output=True, check=True)
    print(f"clip{n}: gain {g:+.2f}dB -> {dst.name}", flush=True)
    norm_files.append(dst.resolve())

# 2. concat
lst = DIR / "_concat.txt"
lst.write_text("".join(f"file '{p}'\n" for p in norm_files))
raw = DIR / "_raw.mp4"
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                "-c", "copy", str(raw)], capture_output=True, check=True)
dur = float(json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format",
            str(raw)], capture_output=True, text=True).stdout)["format"]["duration"])
print(f"concat -> _raw.mp4  {dur:.2f}s", flush=True)

# 3+4. watermark crop + limiter
subprocess.run(["ffmpeg", "-y", "-i", str(raw),
                "-vf", "crop=675:1200:0:0,scale=720:1280,setsar=1",
                "-af", "alimiter=limit=0.794:asc=1",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", str(FINAL)], capture_output=True, check=True)
fd = float(json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format",
            str(FINAL)], capture_output=True, text=True).stdout)["format"]["duration"])
print(f"\nFINAL -> {FINAL}  {fd:.2f}s  LUFS={lufs(FINAL)}", flush=True)
