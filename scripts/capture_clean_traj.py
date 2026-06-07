"""DISSECT EVERY FRAME to capture each Submagic emoji's EXACT per-frame entrance trajectory, then
store it for frame-by-frame replay. Method (validated on 💸): diff each 24fps frame vs the master
(isolates the caption on identical bg), mask wide text rows, take the dominant emoji-sized compact
blob = emoji position. Find the contiguous SMOOTH run that ends at the settled rest = the entrance.
Express as offsets from rest [[t_rel, dx, dy], ...] so the renderer replays the exact movement.

  python scripts/capture_clean_traj.py          # capture all, write traj into the inventory
  python scripts/capture_clean_traj.py --dump 💸 # also dump a per-frame validation montage
"""
import sys, subprocess, json
import numpy as np
import cv2

W, H, FPS = 720, 1280, 24.0
EO = "outputs/illinois_jdc_storytime_e_b14"
SM = f"{EO}/story_e_b14_final_submagic_hormozi3.mp4"
M = f"{EO}/story_e_b14_final.mp4"


def fr(v, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1",
                          "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3).astype(np.int16) if len(raw) >= W * H * 3 else None


def dom(cap, mas, min_area=600):
    """Dominant emoji-sized compact blob in the diff's lower band (text rows masked)."""
    d = np.abs(cap - mas).sum(axis=2).astype(np.uint8)
    band = d[840:1115]
    m = cv2.morphologyEx((band > 55).astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    rw = (m > 0).sum(axis=1); m[rw > 150, :] = 0
    er = rw > 150
    for dy in (-3, -2, -1, 1, 2, 3):
        m[np.roll(er, dy), :] = 0
    n, lbl, st, cen = cv2.connectedComponentsWithStats(m, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if 22 <= w <= 120 and 22 <= h <= 120 and 0.5 < w / h < 2.0 and a / (w * h) > 0.42 and a > min_area:
            if best is None or a > best[0]:
                best = (a, int(cen[i][0]), int(cen[i][1]) + 840, w)
    return best[1:] if best else None


def per_frame(v, t0, t1):
    out = []
    t = t0
    while t < t1:
        cap, mas = fr(v, t), fr(M, t)
        if cap is not None:
            p = dom(cap, mas)
            out.append((round(t, 3), p[0], p[1]) if p else (round(t, 3), None, None))
        t += 1 / FPS
    return out


def capture(t_inv):
    """Return (rest_cx, rest_cy, traj[[t_rel,dx,dy]...]) using the DOMINANT-BLOB per-frame trace
    (validated clean — no backward chaining, which walked along text). Window starts at the card's
    appearance so the previous card's emoji isn't picked up; the entrance is the contiguous run
    (1-frame gaps allowed) ending at the settled rest."""
    raw = per_frame(SM, t_inv - 0.45, t_inv + 0.9)      # wide enough for emojis that appear before inv_t
    pts = [(t, x, y) for t, x, y in raw if x is not None]
    if len(pts) < 4:
        return None
    rx, ry = int(np.median([p[1] for p in pts[-6:]])), int(np.median([p[2] for p in pts[-6:]]))
    # the emoji slides at ~constant cy near its rest; keep only detections within 55px cy of rest —
    # this drops previous-card strays (different cy) without chaining along text.
    pts = [(t, x, y) for t, x, y in pts if abs(y - ry) <= 55]
    if len(pts) < 2:
        return rx, ry, []
    # contiguous run ending at the last detection (allow ≤3 missing frames, ≤70px/frame jump)
    run = [pts[-1]]
    for t, x, y in reversed(pts[:-1]):
        px = run[0]
        if px[0] - t <= 4.5 / FPS and abs(x - px[1]) <= 70:
            run.insert(0, (t, x, y))
        else:
            break
    if len(run) < 2:
        return rx, ry, []
    t0 = run[0][0]
    traj = [[round(t - t0, 3), x - rx, y - ry] for t, x, y in run]
    return rx, ry, traj


def dump(t_inv, name):
    raw = per_frame(SM, t_inv - 0.4, t_inv + 0.6)
    cells = []
    for t, x, y in raw:
        cap, mas = fr(SM, t), fr(M, t)
        d = np.abs(cap - mas).sum(axis=2).clip(0, 255).astype(np.uint8)
        vis = cv2.cvtColor(d[840:1115], cv2.COLOR_GRAY2BGR)
        if x is not None:
            cv2.circle(vis, (x, y - 840), 5, (0, 0, 255), -1)
        cv2.putText(vis, f"{t:.2f}", (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cells.append(cv2.resize(vis, (236, 90)))
    grid = np.vstack([np.hstack(cells[i:i + 3]) for i in range(0, len(cells) - 2, 3)])
    cv2.imwrite(f"/tmp/traj_{name}.png", grid)


if __name__ == "__main__":
    inv = json.load(open("inventory/submagic_emoji_inventory.json"))
    dumponly = None
    if "--dump" in sys.argv:
        dumponly = sys.argv[sys.argv.index("--dump") + 1]
    for e in inv["emojis"]:
        if dumponly and e["emoji"] != dumponly:
            continue
        r = capture(e["t"])
        if not r:
            print(f"{e['emoji']} t={e['t']:.2f}  NO CAPTURE")
            continue
        rx, ry, traj = r
        e["_sm_traj"] = traj
        e["_sm_rest"] = [rx, ry]
        d0 = traj[0] if traj else [0, 0, 0]
        mag = (d0[1] ** 2 + d0[2] ** 2) ** 0.5
        print(f"{e['emoji']} t={e['t']:.2f} rest=({rx},{ry}) frames={len(traj)} "
              f"start=({d0[1]:+d},{d0[2]:+d}) mag={mag:.0f} dur={traj[-1][0] if traj else 0:.2f}s")
        if dumponly:
            dump(e["t"], e["emoji"]); print(f"  dumped /tmp/traj_{e['emoji']}.png")
    if not dumponly:
        json.dump(inv, open("inventory/submagic_emoji_inventory.json", "w"), indent=2, ensure_ascii=False)
        print("\ncaptured trajectories written (_sm_traj / _sm_rest) into inventory")
