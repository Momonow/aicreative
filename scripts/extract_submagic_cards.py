"""Dissect a Submagic-captioned video to extract its EXACT card structure: for each card,
the time window, the words shown, and the line count. Reads the burned captions via a
value/saturation text mask + OCR (catches white AND colored active words). Output JSON:
[{start, end, n_lines, words:[...]}], used to make our in-house captions group identically.

  python scripts/extract_submagic_cards.py <submagic.mp4> [--step 0.3]
"""
import subprocess, sys, argparse, io, json, re
import numpy as np
from PIL import Image


def ocr_card(video, t):
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
                          "-vf", "crop=720:440:0:720", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True).stdout
    a = np.array(Image.open(io.BytesIO(png)).convert("RGB")).astype(np.int16)
    V = a.max(axis=2); mn = a.min(axis=2)
    mask = (V > 205) | ((V > 150) & ((V - mn) > 90))      # white/yellow OR colored(green/red) text
    buf = io.BytesIO(); Image.fromarray(np.where(mask, 0, 255).astype(np.uint8)).save(buf, "PNG")
    r = subprocess.run(["tesseract", "stdin", "-", "--psm", "6", "-l", "eng"],
                       input=buf.getvalue(), capture_output=True)
    rows = []
    for ln in r.stdout.decode("utf-8", "ignore").splitlines():
        ws = [w for w in ln.strip().split() if sum(c.isalpha() for c in w) >= 2]
        if ws:
            rows.append(ws)
    return rows


SHORT_OK = {"a", "i", "it", "at", "me", "to", "of", "be", "my", "is", "in", "no", "on",
            "us", "we", "so", "or", "if", "he", "up", "go", "do", "an", "as"}

def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())

def keep(w):
    """Drop OCR-noise tokens: keep words >=3 alpha, real short words, or numbers."""
    if not w:
        return False
    if w.isdigit():
        return True
    if w in SHORT_OK:
        return True
    return sum(c.isalpha() for c in w) >= 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--step", type=float, default=0.3)
    a = ap.parse_args()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout.strip())
    samples = []
    t = 0.6
    while t < dur - 0.2:
        rows = ocr_card(a.video, t)
        words = [norm(w) for r in rows for w in r if keep(norm(w))]
        # line count = rows that contain a kept word
        nlines = sum(1 for r in rows if any(keep(norm(w)) for w in r))
        samples.append((round(t, 2), nlines, words))
        t += a.step
    # group consecutive samples into cards: new card when the word set changes a lot
    cards = []
    cur = None
    for tt, nlines, words in samples:
        wset = set(words)
        if cur is None:
            cur = {"start": tt, "end": tt, "samples": [(tt, nlines, words)]}
        else:
            prev = set(w for _, _, ws in cur["samples"] for w in ws)
            inter = len(wset & prev)
            sim = inter / max(1, min(len(wset), len(prev)))
            if wset and sim < 0.5 and len(wset) >= 1:      # mostly new words -> new card
                cards.append(cur); cur = {"start": tt, "end": tt, "samples": [(tt, nlines, words)]}
            else:
                cur["end"] = tt; cur["samples"].append((tt, nlines, words))
    if cur:
        cards.append(cur)
    out = []
    for c in cards:
        # representative = sample with the most words; line count = its row count (capped at 2)
        best = max(c["samples"], key=lambda s: len(s[2]))
        words = best[2]; nlines = min(best[1], 2)
        out.append({"start": c["start"], "end": c["end"], "n_lines": max(1, nlines),
                    "n_words": len(words), "words": words})
    # POST-MERGE: collapse OCR re-detections of the SAME card (fuzzy-similar adjacent groups,
    # e.g. 'eight times' / 'eighttimes' / 'eight times'). Merge while the joined-text similarity
    # of adjacent cards is high OR one is a near-subset of the other.
    import difflib
    def joined(c): return " ".join(c["words"])
    merged = True
    while merged:
        merged = False
        res = [out[0]]
        for c in out[1:]:
            prev = res[-1]
            sim = difflib.SequenceMatcher(None, joined(prev), joined(c)).ratio()
            sa, sb = set(prev["words"]), set(c["words"])
            subset = bool(sa and sb) and (len(sa & sb) / min(len(sa), len(sb)) >= 0.6)
            if sim >= 0.55 or subset:
                base = prev["words"] if len(prev["words"]) >= len(c["words"]) else c["words"]
                prev["words"] = base
                prev["end"] = c["end"]; prev["n_words"] = len(base)
                prev["n_lines"] = max(prev["n_lines"], c["n_lines"])
                merged = True
            else:
                res.append(c)
        out = res
    p = a.video.rsplit(".", 1)[0] + ".cards.json"
    open(p, "w").write(json.dumps(out, indent=0))
    print(f"{len(out)} cards extracted -> {p}")
    for c in out[:18]:
        print(f"  {c['start']:5.1f}-{c['end']:4.1f}s  {c['n_lines']}L {c['n_words']}w  {c['words']}")


if __name__ == "__main__":
    main()
