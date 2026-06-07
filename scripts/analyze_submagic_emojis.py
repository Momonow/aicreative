"""Full frame-by-frame analysis of Submagic emojis: for every 0.1s, detect the emoji blob
(compact, filled, square-ish, isolated below the text row) AND the caption text block, so we
can measure emoji position RELATIVE to the subtitle, its movement, and its size over time.

Output: <video>.emoji.json  = [{t, emoji:[cx,cy,w,h]|null, text:[x,y,w,h]|null}, ...]
Then prints segmented emoji EVENTS with motion/size/relative-position summaries.
"""
import sys, subprocess, json
import numpy as np, cv2

CW, CH, CX, CY = 720, 470, 0, 760     # caption region (lower third, below face)


def frames(video, fps):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video,
                          "-vf", f"crop={CW}:{CH}:{CX}:{CY},fps={fps}", "-pix_fmt", "bgr24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (CW * CH * 3)
    return np.frombuffer(raw[:n * CW * CH * 3], np.uint8).reshape(n, CH, CW, 3)


def analyze_frame(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    ink = (((V > 150) | ((S > 85) & (V > 90)))).astype(np.uint8)
    # text rows = rows with wide ink coverage
    row_w = ink.sum(axis=1)
    text_rows = row_w > 150
    ys = np.where(text_rows)[0]
    text_bbox = None
    if len(ys):
        cols = np.where(ink[ys].sum(axis=0) > 0)[0]
        if len(cols):
            text_bbox = [int(cols.min()), int(ys.min() + CY), int(cols.max() - cols.min()),
                         int(ys.max() - ys.min())]
    # emoji = compact, filled, square-ish blob, NOT sitting in a wide-text row
    m = cv2.morphologyEx(ink * 255, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lbl, st, cen = cv2.connectedComponentsWithStats(m, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if not (40 <= w <= 100 and 40 <= h <= 100 and 0.55 < w / h < 1.8):
            continue
        if a / (w * h) < 0.5:
            continue
        rmid = int(cen[i][1])
        if rmid < CH and row_w[rmid] > 320:      # inside a wide text line -> it's text, skip
            continue
        score = a
        if best is None or score > best[0]:
            best = (score, int(cen[i][0]), int(cen[i][1] + CY), int(w), int(h))
    emoji = list(best[1:]) if best else None
    return emoji, text_bbox


def main():
    video = sys.argv[1]
    fps = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    fr = frames(video, fps)
    track = []
    for i in range(len(fr)):
        e, t = analyze_frame(fr[i])
        track.append({"t": round(i / fps, 2), "emoji": e, "text": t})
    out = video.rsplit(".", 1)[0] + ".emoji.json"
    json.dump(track, open(out, "w"))
    # segment events: contiguous frames with an emoji (allow 2-frame gaps)
    events, cur = [], []
    gap = 0
    for fr_i in track:
        if fr_i["emoji"]:
            cur.append(fr_i); gap = 0
        else:
            gap += 1
            if cur and gap > 2:
                events.append(cur); cur = []
    if cur:
        events.append(cur)
    print(f"{len(fr)} frames @ {fps}fps -> {out}")
    print(f"{len([e for e in events if len(e) >= 2])} emoji events:\n")
    for ev in events:
        if len(ev) < 2:
            continue
        cxs = [f["emoji"][0] for f in ev]; cys = [f["emoji"][1] for f in ev]
        ws = [f["emoji"][2] for f in ev]; hs = [f["emoji"][3] for f in ev]
        # relative to text (use mid-event text bbox)
        rel = ""
        mid = ev[len(ev) // 2]
        if mid["text"]:
            tx, ty, tw, th = mid["text"]
            rel = f" relText: dx={cxs[len(ev)//2]-(tx+tw//2):+d} below={cys[len(ev)//2]-(ty+th):+d}"
        print(f"  t={ev[0]['t']:.1f}-{ev[-1]['t']:.1f}s ({len(ev)}f)  "
              f"cx {min(cxs)}-{max(cxs)} (Δ{max(cxs)-min(cxs)})  cy {min(cys)}-{max(cys)} (Δ{max(cys)-min(cys)})  "
              f"size~{int(np.median(ws))}x{int(np.median(hs))}{rel}")


if __name__ == "__main__":
    main()
