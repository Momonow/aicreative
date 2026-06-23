"""
Insert application B-ROLL into the DAK BALM testimonial (_raw.mp4), keeping the testimonial audio
continuous, then crop the Veo watermark once + limiter. Face-first, ~15% b-roll.

v2: the "use" beat is the USER's real Seedance application clip (496x864 -> crop 9:16 -> 720x1280),
placed on "It takes me two seconds in the morning".

Inserts (testimonial timeline -> source trim):
  A apply  [8.80,11.00] <- broll2[3.20,5.40]   (clean single-product swipe)
  B blend  [15.40,16.30] <- broll3[5.00,5.90]  (clean fingertip blend tail)
  C use    [21.30,22.80] <- NEW[2.00,3.50]     (real "putting it on", over "two seconds in the morning")
"""
import subprocess, json
from pathlib import Path

DIR = Path("outputs/cosmechef_dakbalm")
RAW = DIR / "_raw.mp4"
BROLL = DIR / "broll"
NEW = Path("/Users/harry/Downloads/1781507724416-rjhfcj8ii3r.mp4")
OUT = DIR / "cosmechef_dakbalm_testimonial_broll.mp4"

# inputs: 0=raw, 1=broll2(apply), 2=broll3(blend), 3=NEW real-apply
inputs = [RAW, BROLL / "broll2.mp4", BROLL / "broll3.mp4", NEW]

# (timeline_start, timeline_end, input_idx, src_in, src_out, pre_filter_or_None)
INS = [
    (8.80, 11.00, 1, 3.20, 5.40, None),
    (15.40, 16.30, 2, 5.00, 5.90, None),
    (21.30, 22.80, 3, 2.00, 3.50, "crop=486:864"),   # 496x864 -> 9:16 before scale
]

NORM = "scale=720:1280,setsar=1,fps=24,format=yuv420p"
fc, labels = [], []
cursor = 0.0
for i, (ts, te, bidx, sin, sout, pre) in enumerate(INS):
    fc.append(f"[0:v]trim={cursor:.3f}:{ts:.3f},setpts=PTS-STARTPTS,{NORM}[s{i}]")
    labels.append(f"[s{i}]")
    chain = f"[{bidx}:v]trim={sin:.3f}:{sout:.3f},setpts=PTS-STARTPTS," + (f"{pre}," if pre else "") + NORM
    fc.append(f"{chain}[b{i}]")
    labels.append(f"[b{i}]")
    cursor = te
fc.append(f"[0:v]trim={cursor:.3f},setpts=PTS-STARTPTS,{NORM}[sT]")
labels.append("[sT]")

fc.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[vcat]")
fc.append("[vcat]crop=675:1200:0:0,scale=720:1280,setsar=1[vout]")
fc.append("[0:a]alimiter=limit=0.794:asc=1[aout]")

cmd = ["ffmpeg", "-y"]
for p in inputs:
    cmd += ["-i", str(p)]
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", str(OUT)]

print("inserts:", INS, flush=True)
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG ERROR:\n", r.stderr[-2500:], flush=True)
else:
    od = float(json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", str(OUT)], capture_output=True, text=True).stdout)["format"]["duration"])
    bt = sum(te - ts for ts, te, *_ in INS)
    print(f"OK -> {OUT}  {od:.2f}s  b-roll {bt:.1f}s = {bt/od*100:.0f}%", flush=True)
