"""Full-track ElevenLabs audio-isolation on Story E masters (remove background music).
Extract master audio -> isolate -> re-gain to -16 LUFS + limiter -> re-mux. Keeps a _premusic backup.
"""
import sys, subprocess, json, re, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import elevenlabs_client as ec
import requests

EO = Path("outputs/illinois_jdc_storytime_e_b14")
TARGET = -16.0


def isolate(infile, outfile):
    with open(infile, "rb") as f:
        r = requests.post("https://api.elevenlabs.io/v1/audio-isolation",
                          headers={"xi-api-key": ec.API_KEY},
                          files={"audio": (Path(infile).name, f, "audio/mpeg")}, timeout=600)
    if not r.ok:
        print(f"  isolation FAILED {r.status_code}: {r.text[:200]}", flush=True)
        return False
    open(outfile, "wb").write(r.content)
    return True


def measure_i(p):
    out = subprocess.run(["ffmpeg", "-i", str(p), "-af",
                          "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(json.loads(out[out.rfind("{"):out.rfind("}") + 1])["input_i"])


def process(master):
    master = Path(master)
    if not master.exists():
        print(f"  skip (missing): {master}"); return False
    backup = master.with_name(master.stem + "_premusic.mp4")
    if not backup.exists():
        shutil.copy(master, backup)
    raw = Path(f"/tmp/{master.stem}_raw.mp3")
    clean = Path(f"/tmp/{master.stem}_clean.mp3")
    subprocess.run(["ffmpeg", "-y", "-i", str(master), "-vn", "-ar", "44100", "-ac", "1", "-b:a", "192k", str(raw)],
                   capture_output=True)
    print(f"  isolating {master.name} ...", flush=True)
    if not isolate(str(raw), str(clean)):
        return False
    g = TARGET - measure_i(clean)
    tmp = Path(f"/tmp/_remux_{master.stem}.mp4")   # NEVER write in-place (ffmpeg can't read+write same file)
    subprocess.run(["ffmpeg", "-y", "-i", str(master), "-i", str(clean),
                    "-filter_complex", f"[1:a]volume={g:.2f}dB,alimiter=limit=0.794:level=disabled:asc=1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    str(tmp)], capture_output=True)
    shutil.move(str(tmp), str(master))
    print(f"  -> {master.name}  gain {g:+.1f}dB", flush=True)
    return True


def main():
    for m in ["story_e_b14_final.mp4", "story_e_b14_final_safe.mp4"]:
        process(EO / m)


if __name__ == "__main__":
    main()
