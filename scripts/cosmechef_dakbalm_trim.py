"""
Word-aware trailing trim for the 4 DAK BALM clips — cut to each clip's last INTENDED word
(removes Veo trailing improv: 'and-', 'Mm', 'Mmm. Hm.'). Uniform re-encode for clean concat.
Also prints per-clip integrated loudness so we can decide global vs per-clip gain.
"""
import json, re, subprocess, sys
from pathlib import Path

DIR = Path("outputs/cosmechef_dakbalm")
CLIPS = DIR / "clips"
TRIM = DIR / "trimmed"; TRIM.mkdir(parents=True, exist_ok=True)
# transcripts live in outputs/clip{N}/transcript.json (dissect output)
TARGET = {1: "it", 2: "better", 3: "healthy", 4: "lipstick"}
PAD = 0.30


def norm(w):
    return re.sub(r"[^a-z]", "", w.lower())


def words_for(n):
    t = json.load(open(f"outputs/clip{n}/transcript.json"))
    segs = t.get("segments") or []
    return segs[0].get("words", []) if segs else []


def loudness(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "loudnorm=I=-16:TP=-1.5:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r'"input_i"\s*:\s*"(-?[0-9.]+)"', r.stderr)
    return float(m[0]) if m else None


for n in (1, 2, 3, 4):
    ws = words_for(n)
    tgt = TARGET[n]
    idx = max((i for i, w in enumerate(ws) if norm(w["word"]) == tgt), default=None)
    if idx is None:
        print(f"clip{n}: TARGET '{tgt}' NOT FOUND — using full duration", flush=True)
        cut = None
    else:
        end = ws[idx]["end"]
        nxt = ws[idx + 1]["start"] if idx + 1 < len(ws) else None
        cut = min(end + PAD, nxt - 0.03) if nxt else end + PAD
        trailing = " ".join(w["word"] for w in ws[idx + 1:]) or "(none)"
        print(f"clip{n}: last '{tgt}' ends {end:.2f}s -> cut {cut:.2f}s | trailing removed: {trailing}", flush=True)
    src = CLIPS / f"clip{n}.mp4"
    dst = TRIM / f"clip{n}_trim.mp4"
    cmd = ["ffmpeg", "-y", "-i", str(src)]
    if cut:
        cmd += ["-t", f"{cut:.3f}"]
    cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", str(dst)]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"        -> {dst.name}  LUFS={loudness(dst)}", flush=True)
