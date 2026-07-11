"""Assemble the vox-pop clips into a tight ad: trim each clip's leading/trailing DEAD AIR
using Scribe word-timings (Grok clips have ambient street noise, so silencedetect misses the
trailing pause — word-timings are reliable), concat, even loudness with loudnorm.
Usage: python scripts/wp_voxpop_assemble.py <dir> <out.mp4> clip1 clip2 clip3 ...
"""
import sys, subprocess, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from elevenlabs_client import scribe

LEAD_PAD, TRAIL_PAD = 0.05, 0.25

def dur(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",f],capture_output=True,text=True).stdout.strip())

def speech_span(f):
    """Return (start, end) of speech from Scribe word-timings, with small pads."""
    res = scribe(f, biased_keywords=["Chowchilla"])
    words = [w for w in res.get("words", []) if w.get("type") == "word"]
    if not words:
        return 0.0, dur(f)
    s = max(0.0, words[0]["start"] - LEAD_PAD)
    e = min(dur(f), words[-1]["end"] + TRAIL_PAD)
    return round(s,2), round(e,2)

dirp = pathlib.Path(sys.argv[1]); out = sys.argv[2]; slugs = sys.argv[3:]
tmp = []
for i, slug in enumerate(slugs):
    f = str(dirp / f"{slug}.mp4")
    s, e = speech_span(f)
    t = str(dirp / f"_t{i}.mp4")
    subprocess.run(["ffmpeg","-y","-i",f,"-ss",str(s),"-to",str(e),
        "-c:v","libx264","-preset","fast","-crf","20","-c:a","aac","-b:a","192k",t],
        capture_output=True)
    print(f"[trim] {slug}: {s}->{e}s")
    tmp.append(t)

# build concat filter with loudnorm
inputs = []
for t in tmp: inputs += ["-i", t]
n = len(tmp)
fv = "".join(f"[{i}:v]scale=1280:720,setsar=1,fps=30[v{i}];" for i in range(n))
cc = "".join(f"[v{i}][{i}:a]" for i in range(n))
filt = fv + cc + f"concat=n={n}:v=1:a=1[v][a];[a]loudnorm=I=-16:TP=-1.5:LRA=11[ao]"
subprocess.run(["ffmpeg","-y",*inputs,"-filter_complex",filt,"-map","[v]","-map","[ao]",
    "-c:v","libx264","-preset","fast","-crf","20","-c:a","aac","-b:a","192k",out],
    capture_output=True)
# web-compressed copy
web = out.replace(".mp4","_web.mp4")
subprocess.run(["ffmpeg","-y","-i",out,"-c:v","libx264","-preset","fast","-crf","26",
    "-c:a","aac","-b:a","128k",web],capture_output=True)
print(f"[done] {out}  ({dur(out):.1f}s)  web={web}")
