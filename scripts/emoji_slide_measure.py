"""Measure each emoji's TRUE slide-in vector by template-tracking its settled appearance BACKWARD
through the entrance, on the DIFF image (captioned - master, which isolates the emoji on black).
Template = the emoji's settled diff-crop. Each earlier frame: multi-scale match in a LOCAL window
that follows the last position (so it tracks through slide + scale-up without locking onto text).
Reports the start offset (dx,dy from rest) = the direction/distance it slid IN from, per emoji,
for SM and ours.

  python scripts/emoji_slide_measure.py
"""
import sys, subprocess, json
import numpy as np
import cv2

W, H, FPS = 720, 1280, 24.0
SCALES = np.round(np.arange(0.40, 1.21, 0.05), 2)


def _diff(v, m, t):
    def fr(p):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1",
                              "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
        return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3).astype(np.int16) if len(raw) >= W * H * 3 else None
    a, b = fr(v), fr(m)
    if a is None or b is None:
        return None
    d = np.abs(a - b).sum(axis=2).clip(0, 255).astype(np.uint8)
    # ZERO the text rows (wide ink) + margin so template-matching can ONLY lock onto the emoji,
    # never a text fragment — this is what kept contaminating the entrance track.
    band = (d[820:1120] > 55)
    rw = band.sum(axis=1)
    wide = np.where(rw > 150)[0]
    for r in wide:
        for dr in range(-4, 5):
            rr = r + dr
            if 0 <= rr < band.shape[0]:
                d[820 + rr, :] = 0
    return d


def settled(v, m, t_inv, rx_hint=None):
    """Settled rest (cx,cy,half) from the diff over the body; returns template crop too."""
    d = _diff(v, m, t_inv + 0.45)
    if d is None:
        return None
    band = d[840:1115]
    msk = cv2.morphologyEx((band > 55).astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    rw = (msk > 0).sum(axis=1); msk[rw > 150, :] = 0
    er = rw > 150
    for dy in (-3, -2, -1, 1, 2, 3):
        msk[np.roll(er, dy), :] = 0
    n, lbl, st, cen = cv2.connectedComponentsWithStats(msk, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if 28 <= w <= 110 and 28 <= h <= 110 and 0.6 < w / h < 1.7 and a / (w * h) > 0.45:
            sc = a
            if best is None or sc > best[0]:
                best = (a, int(cen[i][0]), int(cen[i][1]) + 840, int(w), int(h))
    if best is None:
        return None
    cx, cy, w, h = best[1], best[2], best[3], best[4]
    half = max(w, h) // 2 + 6
    tmpl = d[cy - half:cy + half, cx - half:cx + half]
    return cx, cy, half, tmpl


def trace(v, m, t_inv, rx, ry, half, tmpl):
    th0 = tmpl.shape[0]
    lx, ly = rx, ry
    traj = []
    t = t_inv + 0.30
    while t > t_inv - 0.6:
        d = _diff(v, m, t)
        if d is None:
            break
        y0, x0 = max(0, ly - 90), max(0, lx - 90)          # local window follows last position
        win = d[y0:ly + 90, x0:lx + 90]
        best = (-1, lx, ly, 1.0)
        for s in SCALES:
            ts = max(10, int(th0 * s))
            if ts >= win.shape[0] or ts >= win.shape[1]:
                continue
            tm = cv2.resize(tmpl, (ts, ts), interpolation=cv2.INTER_AREA)
            r = cv2.matchTemplate(win, tm, cv2.TM_CCOEFF_NORMED)
            _, mx, _, loc = cv2.minMaxLoc(r)
            if mx > best[0]:
                best = (mx, x0 + loc[0] + ts // 2, y0 + loc[1] + ts // 2, s)
        if best[0] < 0.45:
            break
        traj.append((round(t, 3), best[1], best[2], best[3]))
        lx, ly = best[1], best[2]
        t -= 1 / FPS
    if len(traj) < 2:
        return []
    traj.reverse()
    t0 = traj[0][0]
    return [(round(p[0] - t0, 3), p[1] - rx, p[2] - ry, p[3]) for p in traj]


def classify(tr):
    if not tr:
        return "no-track"
    dx, dy = tr[0][1], tr[0][2]
    mag = (dx * dx + dy * dy) ** 0.5
    if mag < 14:
        return f"pop (start {dx:+d},{dy:+d} mag={mag:.0f})"
    ratio = abs(dx) / (abs(dy) + 1e-6)
    kind = "horizontal" if ratio > 2.2 else ("vertical" if ratio < 0.45 else "diagonal")
    return f"SLIDE {kind} from ({dx:+d},{dy:+d}) mag={mag:.0f} over {tr[-1][0]:.2f}s"


if __name__ == "__main__":
    EO = "outputs/illinois_jdc_storytime_e_b14"
    M, SM = f"{EO}/story_e_b14_final.mp4", f"{EO}/story_e_b14_final_submagic_hormozi3.mp4"
    O = f"{EO}/story_e_b14_final_hormozi_emoji.mp4"
    inv = json.load(open("inventory/submagic_emoji_inventory.json"))
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for e in inv["emojis"]:
        if only and e["emoji"] != only:
            continue
        t = e["t"]
        s = settled(SM, M, t)
        print(f"\n{e['emoji']} inv_t={t:.2f}")
        if s:
            tr = trace(SM, M, t, s[0], s[1], s[2], s[3])
            print(f"  SM rest=({s[0]},{s[1]}) half={s[2]}  {classify(tr)}")
            print(f"     {tr}")
        so = settled(O, M, t)
        if so:
            tro = trace(O, M, t, so[0], so[1], so[2], so[3])
            print(f"  OURS rest=({so[0]},{so[1]})  {classify(tro)}")
