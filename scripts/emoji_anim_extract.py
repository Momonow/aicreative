"""Exact per-frame emoji animation extraction (24fps) via MULTI-SCALE template matching.
For each emoji event, tracks position AND scale every frame across its lifetime, so we recover:
start position+size -> end position+size, movement path, speed (px/frame), and the size curve.

  python scripts/emoji_anim_extract.py <submagic_video>
Reads <video>.emoji_track.json (events: k,t0,t1,cx_med,cy_med,size) + emoji_crops/ev{k}_*.png.
Writes <video>.emoji_anim.json and prints a per-emoji animation summary.
"""
import sys, subprocess, json, glob
from pathlib import Path
import numpy as np, cv2

W, H, FPS = 720, 1280, 24.0
SCALES = np.round(np.arange(0.45, 1.26, 0.03), 2)


def full(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                          "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3) if len(raw) >= W * H * 3 else None


def main():
    video = sys.argv[1]
    base = video.rsplit(".", 1)[0]
    events = json.load(open(base + ".emoji_track.json"))
    cropdir = Path(video).parent / "emoji_crops"
    out = []
    for ev in events:
        k = ev["k"]; cx0, cy0 = ev["cx_med"], ev["cy_med"]
        cps = sorted(glob.glob(str(cropdir / f"ev{k:02d}_*.png")))
        if not cps:
            continue
        tmpl0 = cv2.imread(cps[0])
        th0, tw0 = tmpl0.shape[:2]
        traj = []
        t = ev["t0"] - 0.45
        while t < ev["t1"] + 0.45:
            f = full(video, t)
            if f is not None:
                y0, x0 = max(0, cy0 - 150), max(0, cx0 - 150)
                win = f[y0:cy0 + 150, x0:cx0 + 150]
                best = (-1, 1.0, 0, 0)
                for sc in SCALES:
                    tw, th = int(tw0 * sc), int(th0 * sc)
                    if tw < 12 or th < 12 or tw >= win.shape[1] or th >= win.shape[0]:
                        continue
                    tm = cv2.resize(tmpl0, (tw, th), interpolation=cv2.INTER_AREA)
                    r = cv2.matchTemplate(win, tm, cv2.TM_CCOEFF_NORMED)
                    _, mx, _, loc = cv2.minMaxLoc(r)
                    if mx > best[0]:
                        best = (mx, sc, x0 + loc[0] + tw // 2, y0 + loc[1] + th // 2)
                if best[0] > 0.55:
                    traj.append({"t": round(t, 3), "val": round(float(best[0]), 2),
                                 "scale": float(best[1]), "cx": int(best[2]), "cy": int(best[3])})
            t += 1.0 / FPS
        if len(traj) < 4:
            continue
        # summarize: find entrance (first frame with good val) -> settle
        g = [p for p in traj if p["val"] > 0.7]
        if len(g) < 3:
            g = traj
        sc = [p["scale"] for p in g]; cx = [p["cx"] for p in g]; cy = [p["cy"] for p in g]
        # entrance = until scale first reaches >=0.98 of its max
        smax = max(sc)
        settle_i = next((i for i, s in enumerate(sc) if s >= 0.98 * smax), len(sc) - 1)
        ent_dur = g[settle_i]["t"] - g[0]["t"]
        out.append({"k": k, "t0": ev["t0"], "n": len(g),
                    "start": {"scale": sc[0], "cx": cx[0], "cy": cy[0]},
                    "settle": {"scale": round(smax, 2), "cx": cx[settle_i], "cy": cy[settle_i],
                               "t_after_start": round(ent_dur, 3)},
                    "scale_curve": [round(s, 2) for s in sc[:settle_i + 2]],
                    "cy_curve": cy[:settle_i + 2], "cx_curve": cx[:settle_i + 2]})
        print(f"ev{k:02d} t={ev['t0']:.1f}s  start(scale={sc[0]:.2f},cx={cx[0]},cy={cy[0]}) -> "
              f"settle(scale={smax:.2f},cx={cx[settle_i]},cy={cy[settle_i]}) in {ent_dur:.3f}s "
              f"({settle_i} frames)  scaleΔ={smax-sc[0]:+.2f} cyΔ={cy[settle_i]-cy[0]:+d}  "
              f"scale_curve={[round(s,2) for s in sc[:settle_i+2]]}")
    json.dump(out, open(base + ".emoji_anim.json", "w"))
    print(f"\n{len(out)} emoji animations -> {base}.emoji_anim.json")


if __name__ == "__main__":
    main()
