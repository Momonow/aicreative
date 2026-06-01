"""Compare caption LINE COUNT (and rough word grouping) between two videos, frame by frame,
via OCR. Used to tune our in-house captions to match Submagic's line organization.

  python scripts/caption_linecmp.py <ours.mp4> <submagic.mp4> [--interval 0.7]

Reports: per-second line counts side by side, line-count match %, and the line-count
distribution (how many sampled frames show 1 / 2 / 3 lines) for each.
"""
import sys, subprocess, argparse, statistics
from pathlib import Path


def ocr_lines(png_bytes):
    """OCR a caption-band frame -> number of text lines + the words, via y-clustering of word boxes."""
    r = subprocess.run(["tesseract", "stdin", "-", "--psm", "11", "-l", "eng", "tsv"],
                       input=png_bytes, capture_output=True)
    rows = []
    for ln in r.stdout.decode("utf-8", "ignore").splitlines()[1:]:
        p = ln.split("\t")
        if len(p) < 12:
            continue
        try:
            conf = float(p[10])
        except ValueError:
            continue
        txt = p[11].strip()
        if conf < 45 or not any(c.isalnum() for c in txt):
            continue
        top, h = int(p[7]), int(p[9])
        rows.append((top + h / 2, h, txt))
    if not rows:
        return 0, []
    rows.sort()
    med_h = statistics.median([h for _, h, _ in rows])
    lines, cur, cur_y = [], [], None
    for yc, h, txt in rows:
        if cur_y is None or abs(yc - cur_y) <= med_h * 0.6:
            cur.append(txt); cur_y = yc if cur_y is None else (cur_y + yc) / 2
        else:
            lines.append(cur); cur = [txt]; cur_y = yc
    if cur:
        lines.append(cur)
    return len(lines), [" ".join(l) for l in lines]


def sample(video, interval):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", video], capture_output=True, text=True).stdout.strip())
    out = {}
    t = 1.0
    while t < dur - 0.3:
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
                              "-vf", "crop=720:540:0:650", "-f", "image2pipe", "-vcodec", "png", "-"],
                             capture_output=True).stdout
        n, lines = ocr_lines(png)
        out[round(t, 1)] = (n, lines)
        t += interval
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ours"); ap.add_argument("submagic")
    ap.add_argument("--interval", type=float, default=0.7)
    ap.add_argument("--show", action="store_true", help="print per-timestamp table")
    a = ap.parse_args()
    o = sample(a.ours, a.interval); s = sample(a.submagic, a.interval)
    ts = sorted(set(o) & set(s))
    match = same = 0
    od = {1: 0, 2: 0, 3: 0}; sd = {1: 0, 2: 0, 3: 0}
    for t in ts:
        on, _ = o[t]; sn, _ = s[t]
        if on == 0 or sn == 0:
            continue
        match += 1
        if on == sn:
            same += 1
        od[min(on, 3)] = od.get(min(on, 3), 0) + 1
        sd[min(sn, 3)] = sd.get(min(sn, 3), 0) + 1
        if a.show:
            flag = "" if on == sn else "  <-- DIFF"
            print(f"  {t:5.1f}s  ours={on}  sm={sn}{flag}   ours:{o[t][1]}  sm:{s[t][1]}")
    print(f"\nline-count MATCH: {same}/{match} = {100*same/max(1,match):.0f}%")
    print(f"ours line distribution (1/2/3+): {od.get(1,0)}/{od.get(2,0)}/{od.get(3,0)}")
    print(f"subm line distribution (1/2/3+): {sd.get(1,0)}/{sd.get(2,0)}/{sd.get(3,0)}")


if __name__ == "__main__":
    main()
