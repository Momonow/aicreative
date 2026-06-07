"""Detect the emoji blob in a captioned video frame-by-frame (for reverse-engineering Submagic's
emoji size/position/motion). Emoji = a compact, FILLED, MULTI-HUE blob (text is single-hue strokes).

  python scripts/detect_emojis.py <video> --test 5.5 9 117      # print detection at timestamps
  python scripts/detect_emojis.py <video> --fps 10 --out x.json  # full per-frame track
"""
import sys, subprocess, argparse, json
import numpy as np, cv2

CROPW, CROPH, CROPX, CROPY = 720, 560, 0, 640   # caption band in the 720x1280 frame


def frame_at(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
                          "-vf", f"crop={CROPW}:{CROPH}:{CROPX}:{CROPY}", "-pix_fmt", "bgr24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    if len(raw) < CROPW * CROPH * 3:
        return None
    return np.frombuffer(raw[:CROPW * CROPH * 3], np.uint8).reshape(CROPH, CROPW, 3)


def detect(bgr, min_div=0.22):
    """Return (cx, cy, w, h, huediv) of the emoji in band-coords, or None."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)
    colored = (((S > 70) & (V > 90)).astype(np.uint8)) * 255
    colored = cv2.morphologyEx(colored, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lbl, stats, _ = cv2.connectedComponentsWithStats(colored, 8)
    best, best_div = None, -1
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < 500 or w == 0 or h == 0:
            continue
        fill = area / (w * h); asp = w / h
        if not (0.5 < asp < 1.9 and fill > 0.42 and 26 < w < 130 and 26 < h < 130):
            continue
        mask = lbl == i
        hsel = H[mask & (S > 70)]
        if len(hsel) < 40:
            continue
        ang = hsel.astype(float) / 180.0 * 2 * np.pi          # circular hue variance (multi-hue = emoji)
        div = 1 - np.hypot(np.mean(np.cos(ang)), np.mean(np.sin(ang)))
        if div > best_div:
            best_div = div; best = (int(x + w / 2), int(y + h / 2), int(w), int(h), round(float(div), 3))
    if best and best[4] >= min_div:
        return best
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--fps", type=float, default=10)
    ap.add_argument("--test", nargs="*", type=float); ap.add_argument("--out")
    a = ap.parse_args()
    if a.test:
        for t in a.test:
            f = frame_at(a.video, t)
            print(f"  {t}s -> {detect(f) if f is not None else 'no frame'}")
        return
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout)
    track = []
    t = 0.0
    while t < dur - 0.05:
        f = frame_at(a.video, t)
        d = detect(f) if f is not None else None
        track.append({"t": round(t, 2), "e": d})   # e = [cx,cy,w,h,div] (band coords) or None
        t += 1.0 / a.fps
    json.dump(track, open(a.out, "w"))
    present = sum(1 for x in track if x["e"])
    print(f"{len(track)} frames, {present} with emoji -> {a.out}")


if __name__ == "__main__":
    main()
