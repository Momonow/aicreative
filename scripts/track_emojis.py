"""Per-emoji-event motion extraction via template matching (robust to the moving caption).
Uses the coarse <video>.emoji.json events to locate emojis, then for each event:
  - extracts a template from the best (most-settled) frame,
  - tracks the emoji at native fps across the event,
  - saves a crop (to identify the emoji TYPE by eye),
  - reports entrance motion (start->end px, duration, per-frame speed) + steady position + size.
Output: <video>.emoji_track.json  +  crops in <dir>/emoji_crops/
"""
import sys, subprocess, json
from pathlib import Path
import numpy as np, cv2

W, H = 720, 1280


def full(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                          "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3) if len(raw) >= W * H * 3 else None


def main():
    video = sys.argv[1]; fps = 24.0
    track = json.load(open(video.rsplit(".", 1)[0] + ".emoji.json"))
    # segment events (>=3 frames, allow 2-frame gaps)
    events, cur, gap = [], [], 0
    for fr in track:
        if fr["emoji"]:
            cur.append(fr); gap = 0
        else:
            gap += 1
            if cur and gap > 2:
                events.append(cur); cur = []
    if cur:
        events.append(cur)
    events = [e for e in events if len(e) >= 2]
    cropdir = Path(video).with_suffix("")  # dir base
    cropdir = cropdir.parent / "emoji_crops"; cropdir.mkdir(exist_ok=True)
    out = []
    for k, ev in enumerate(events):
        # template from the event's mid frame (most settled)
        mid = ev[len(ev) // 2]; cx, cy, w, h = mid["emoji"]
        tw, th = max(60, w), max(70, h)
        f0 = full(video, mid["t"])
        if f0 is None:
            continue
        x0, y0 = max(0, cx - tw // 2), max(0, cy - th // 2)
        tmpl = f0[y0:y0 + th, x0:x0 + tw]
        cv2.imwrite(str(cropdir / f"ev{k:02d}_{ev[0]['t']:.1f}s.png"), tmpl)
        # track across [start-0.3, end+0.3] at fps
        traj = []
        t = ev[0]["t"] - 0.35
        while t < ev[-1]["t"] + 0.35:
            f = full(video, t)
            if f is not None:
                res = cv2.matchTemplate(f, tmpl, cv2.TM_CCOEFF_NORMED)
                _, mx, _, loc = cv2.minMaxLoc(res)
                if mx > 0.6:
                    traj.append((round(t, 3), loc[0] + tw // 2, loc[1] + th // 2, round(float(mx), 2)))
            t += 1.0 / fps
        if len(traj) < 3:
            continue
        xs = [p[1] for p in traj]; ys = [p[2] for p in traj]
        # entrance = first third; steady = last third
        ent = traj[:max(2, len(traj) // 3)]
        out.append({"k": k, "t0": ev[0]["t"], "t1": ev[-1]["t"], "size": [tw, th],
                    "cx_med": int(np.median(xs)), "cy_med": int(np.median(ys)),
                    "cx_range": max(xs) - min(xs), "cy_range": max(ys) - min(ys),
                    "entrance": [(p[0], p[1], p[2]) for p in ent]})
        e0, e1 = traj[0], traj[len(ent) - 1]
        print(f"ev{k:02d} {ev[0]['t']:.1f}-{ev[-1]['t']:.1f}s size~{tw}x{th}  "
              f"cx {min(xs)}-{max(xs)}(Δ{max(xs)-min(xs)}) cy {min(ys)}-{max(ys)}(Δ{max(ys)-min(ys)})  "
              f"entrance dy={e1[2]-e0[2]:+d}px/{(e1[0]-e0[0]):.2f}s")
    json.dump(out, open(video.rsplit(".", 1)[0] + ".emoji_track.json", "w"))
    print(f"\n{len(out)} tracked events -> crops in {cropdir}/")


if __name__ == "__main__":
    main()
