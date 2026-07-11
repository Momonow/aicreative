"""Autonomous finalize for the OMNI interview: verify each 2-turn chunk (both lines present, no
heavy improv, Chowchilla pronunciation if applicable); re-roll bad chunks up to MAX; report.
"""
import subprocess, re, sys, pathlib, tempfile, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from elevenlabs_client import scribe
from wp_interview_omni_produce import CHUNKS

D = pathlib.Path("outputs/wp_voxpop/interview_omni")
MAX = 3
def toks(s): return re.findall(r"[a-z0-9]+", s.lower())
def wt(w): return (w.get("text") or w.get("word") or "")

def check(path, turns):
    line = " ".join(t for _, t in turns)
    res = scribe(path, biased_keywords=["Chowchilla"])
    ws = [w for w in res.get("words", []) if w.get("type") == "word"]
    if not ws: return False, "no speech"
    exp = toks(line); trans = [re.sub(r"[^a-z0-9]", "", wt(w).lower()) for w in ws]
    ei = 0
    for tw_ in trans:
        if ei < len(exp) and tw_ == exp[ei]: ei += 1
    if ei < 0.65 * len(exp): return False, f"missing ({ei}/{len(exp)})"
    if len(trans) > len(exp) * 1.8 + 4: return False, f"improv ({len(trans)}vs{len(exp)})"
    if "chowchilla" in line.lower():
        full = " ".join(wt(w).lower() for w in scribe(path).get("words", []))
        if "chauch" in full or "chochil" in full: return False, "Chowchilla mispron"
        if "chowchill" not in full: return False, "Chowchilla unclear"
    return True, "ok"

report = []
for slug, turns in CHUNKS.items():
    path = D / f"{slug}.mp4"
    for attempt in range(1, MAX + 1):
        if not path.exists():
            subprocess.run([".venv/bin/python", "scripts/wp_interview_omni_produce.py", slug],
                           capture_output=True, env={**os.environ, "PYTHONPATH": "."})
        if not path.exists(): report.append((slug, "GEN FAILED")); break
        ok, reason = check(str(path), turns)
        print(f"{slug} attempt {attempt}: {reason}", flush=True)
        if ok: report.append((slug, "ok")); break
        path.unlink(missing_ok=True)
        if attempt == MAX: report.append((slug, f"STILL BAD: {reason}"))
print("=== OMNI CHUNK REPORT ==="); [print(f"  {s}: {st}") for s, st in report]
print("OMNI FINALIZE DONE")
