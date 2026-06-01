"""Trace each emoji's TRUE entrance trajectory by tracking it BACKWARD from its settled position.
Starting from certainty (the settled emoji, isolated by diffing captioned vs master) and linking to
the nearest compact blob in each earlier frame, we follow the emoji back through its entrance — which
robustly captures SLIDE motion (horizontal / vertical / diagonal) that forward global search mislabels
as text contamination. Reports the start offset (dx,dy from rest) = the direction it slid IN from.

  python scripts/emoji_entrance_track.py            # all inventory emojis, SM vs OURS
"""
import sys, subprocess, json
import numpy as np
import cv2

W, H, FPS = 720, 1280, 24.0
BY0, BY1 = 840, 1115


def _frame(v, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1",
                          "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3).astype(np.int16) if len(raw) >= W * H * 3 else None


def _blobs(cap, mas):
    """All compact emoji-candidate blobs in the lower band of the diff (cx,cy,w,h,fill)."""
    d = np.abs(cap - mas).sum(axis=2).astype(np.uint8)
    band = d[BY0:BY1]
    m = cv2.morphologyEx((band > 55).astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    rw = (m > 0).sum(axis=1)
    m[rw > 150, :] = 0                                   # erase wide text rows
    er = rw > 150
    for dy in (-3, -2, -1, 1, 2, 3):
        m[np.roll(er, dy), :] = 0
    n, lbl, st, cen = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if 16 <= w <= 120 and 16 <= h <= 120 and 0.45 < w / h < 2.2 and a / (w * h) > 0.4 and a > 350:
            out.append((int(cen[i][0]), int(cen[i][1]) + BY0, int(w), int(h), a / (w * h)))
    return out


def settled(cap_v, mas_v, t_inv):
    """Settled position = median of compact-blob detections over the body after the entrance."""
    pts = []
    t = t_inv + 0.25
    while t < t_inv + 0.85:
        cap, mas = _frame(cap_v, t), _frame(mas_v, t)
        if cap is not None:
            bl = _blobs(cap, mas)
            if bl:
                bl.sort(key=lambda b: -b[2] * b[3])
                pts.append(bl[0])
        t += 1 / FPS
    if len(pts) < 2:
        return None
    return (int(np.median([p[0] for p in pts])), int(np.median([p[1] for p in pts])),
            int(np.median([p[2] for p in pts])))


def trace_back(cap_v, mas_v, t_inv, rx, ry, rw):
    """From the settled frame, link to the nearest compact blob in each EARLIER frame (max jump 70px),
    following the emoji back through its entrance. Returns [(t_rel, dx, dy, w/rw), ...] oldest-first."""
    path = []
    lx, ly = rx, ry
    # start at a frame where it's settled
    t = t_inv + 0.30
    traj = []
    JUMP = 38                                            # max px/frame: a real emoji slide is smooth;
    while t > t_inv - 0.55:                              # a larger cap lets the tracker WALK along text
        cap, mas = _frame(cap_v, t), _frame(mas_v, t)
        if cap is not None:
            cands = _blobs(cap, mas)
            near = [b for b in cands if abs(b[0] - lx) <= JUMP and abs(b[1] - ly) <= JUMP
                    and 0.5 * rw <= b[2] <= 1.7 * rw]    # consistent size -> not a text fragment
            if near:
                b = min(near, key=lambda b: (b[0] - lx) ** 2 + (b[1] - ly) ** 2)
                traj.append((round(t, 3), b[0], b[1], b[2]))
                lx, ly = b[0], b[1]
            else:
                break                                    # lost it -> entrance start reached
        t -= 1 / FPS
    if len(traj) < 2:
        return []
    traj.reverse()
    t0 = traj[0][0]
    return [(round(p[0] - t0, 3), p[1] - rx, p[2] - ry, round(p[3] / max(1, rw), 2)) for p in traj]


def classify(traj):
    if not traj:
        return "none"
    dx0, dy0 = traj[0][1], traj[0][2]
    mag = (dx0 ** 2 + dy0 ** 2) ** 0.5
    if mag < 12:
        return "pop (no slide)"
    ang = abs(dx0) / (abs(dy0) + 1e-6)
    d = "diagonal" if 0.4 < ang < 2.5 else ("horizontal" if ang >= 2.5 else "vertical")
    frm = ("left" if dx0 < 0 else "right") if abs(dx0) > 10 else ""
    frm2 = ("above" if dy0 < 0 else "below") if abs(dy0) > 10 else ""
    return f"SLIDE {d} from ({dx0:+d},{dy0:+d}) [{frm} {frm2}] mag={mag:.0f}"


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
        rs = settled(SM, M, t)
        ro = settled(O, M, t)
        print(f"\n{e['emoji']} inv_t={t:.2f}  motion={e['motion'].get('type')}")
        if rs:
            ts = trace_back(SM, M, t, *rs)
            print(f"  SM   rest=({rs[0]},{rs[1]})  {classify(ts)}")
            print(f"       traj {ts}")
        if ro:
            to = trace_back(O, M, t, *ro)
            print(f"  OURS rest=({ro[0]},{ro[1]})  {classify(to)}")
            print(f"       traj {to}")
