"""Motion-capture each Submagic emoji's FULL per-frame trajectory (position + scale) via
multi-scale template matching, expressed as offsets from its RESTING position. These keyframes
are replayed by caption_hormozi3 to reproduce the exact slide-in + drift + scale-pop per emoji.

  python scripts/capture_emoji_trajectories.py <submagic_video> <inventory.json>
Writes the trajectories back into the inventory ("traj": [[t_rel, dx, dy, scale], ...] per emoji),
where dx,dy are px offsets from the emoji's resting (end) position and t_rel is sec since appearance.
"""
import sys, subprocess, json
import numpy as np, cv2

W, H, FPS = 720, 1280, 24.0
SCALES = np.round(np.arange(0.40, 1.30, 0.03), 2)


def full(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                          "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3) if len(raw) >= W * H * 3 else None


def main():
    video, invpath = sys.argv[1], sys.argv[2]
    events = json.load(open(video.rsplit(".", 1)[0] + ".emoji_track.json"))
    inv = json.load(open(invpath))
    inv_emojis = inv["emojis"]
    for ev in events:
        # find the matching inventory emoji by nearest t0
        ie = min(inv_emojis, key=lambda e: abs(e["t"] - ev["t0"]))
        if abs(ie["t"] - ev["t0"]) > 1.5:
            continue
        cx0, cy0 = ev["cx_med"], ev["cy_med"]
        f0 = full(video, (ev["t0"] + ev["t1"]) / 2 + 0.2)
        if f0 is None:
            continue
        tmpl = f0[cy0 - 44:cy0 + 44, cx0 - 44:cx0 + 44]
        th0, tw0 = tmpl.shape[:2]
        raw = []
        t = ev["t0"] - 0.15
        while t < ev["t1"] + 0.25:
            f = full(video, t)
            if f is not None:
                y0, x0 = max(0, cy0 - 140), max(0, cx0 - 140)
                win = f[y0:cy0 + 140, x0:cx0 + 140]
                best = (-1, 1.0, 0, 0)
                for sc in SCALES:
                    tw, th = int(tw0 * sc), int(th0 * sc)
                    if tw < 14 or tw >= win.shape[1] or th >= win.shape[0]:
                        continue
                    r = cv2.matchTemplate(win, cv2.resize(tmpl, (tw, th), interpolation=cv2.INTER_AREA),
                                          cv2.TM_CCOEFF_NORMED)
                    _, mx, _, loc = cv2.minMaxLoc(r)
                    if mx > best[0]:
                        best = (mx, sc, x0 + loc[0] + tw // 2, y0 + loc[1] + th // 2)
                if best[0] > 0.7:
                    raw.append((round(t, 3), best[1], best[2], best[3]))
            t += 1.0 / FPS
        if len(raw) < 4:
            ie["traj"] = []
            continue
        # resting position = median of last 3 reliable frames
        restx = int(np.median([p[2] for p in raw[-3:]]))
        resty = int(np.median([p[3] for p in raw[-3:]]))
        t_app = raw[0][0]
        traj = [[round(p[0] - t_app, 3), p[2] - restx, p[3] - resty, round(float(p[1]), 2)] for p in raw]
        ie["traj"] = traj
        dx0, dy0 = traj[0][1], traj[0][2]
        print(f"t={ev['t0']:.1f}s {ie['emoji']}  {len(traj)} keyframes  start_offset=({dx0:+d},{dy0:+d})px "
              f"scale {traj[0][3]}->1.0  dur~{traj[-1][0]:.2f}s", flush=True)
    json.dump(inv, open(invpath, "w"), indent=2, ensure_ascii=False)
    print(f"\nwrote trajectories into {invpath}")


if __name__ == "__main__":
    main()
