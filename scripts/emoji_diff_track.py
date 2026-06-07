"""Per-frame emoji position+size measurement by DIFFING a captioned video against its clean master.
Both Submagic's export and our render overlay captions on the SAME master (story_e_b14_final.mp4),
so |captioned - master| isolates the caption layer cleanly — the emoji is the compact square-ish
blob in the lower band (text is wide rows). This is robust at ANY scale (unlike template matching,
which mis-locks during the fast scaling entrance).

API: track(captioned, master, t0, t1, fps=24) -> [{t, cx, cy, w, h, area}, ...] (emoji frames only)
CLI: python scripts/emoji_diff_track.py <captioned> <master> <t0> <t1>
"""
import sys, subprocess
import numpy as np
import cv2

W, H = 720, 1280
BAND_Y0, BAND_Y1 = 860, 1110      # lower caption band where the emoji lives (below the text rows)


def _frame(v, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1",
                          "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw[:W * H * 3], np.uint8).reshape(H, W, 3).astype(np.int16) if len(raw) >= W * H * 3 else None


def _emoji_in_frame(cap, mas):
    """Diff one frame pair, return the emoji blob (cx,cy,w,h,area) in the lower band, or None.

    The caption layer = TEXT (wide horizontal rows) + EMOJI (compact square blob below the text).
    To isolate the emoji we ZERO every wide text row first (>WIDE px of ink in that row), which
    erases full caption lines + the active-word highlight; the emoji's rows (~its own width, <WIDE)
    survive. Then the emoji is the largest compact square-ish blob remaining."""
    d = np.abs(cap - mas).sum(axis=2).astype(np.uint8)          # color L1 diff
    band = d[BAND_Y0:BAND_Y1]
    mask = (band > 60).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    WIDE = 140                                                  # an emoji is ≤~130px wide; text lines are far wider
    row_w = (mask > 0).sum(axis=1)
    # measure the TEXT block from the wide rows (so emoji position can be expressed RELATIVE to text)
    text_rows = np.where(row_w > WIDE)[0]
    text_bbox = None
    if len(text_rows):
        cols = np.where(mask[text_rows].sum(axis=0) > 0)[0]
        if len(cols):
            text_bbox = {"cx": int((cols.min() + cols.max()) / 2),
                         "top": int(text_rows.min()) + BAND_Y0,
                         "bottom": int(text_rows.max()) + BAND_Y0}
    mask[row_w > WIDE, :] = 0                                   # erase text lines + highlight bars
    er = row_w > WIDE                                          # erase a margin around them too (antialias fringe)
    for dy in (-3, -2, -1, 1, 2, 3):
        mask[np.roll(er, dy), :] = 0
    n, lbl, st, cen = cv2.connectedComponentsWithStats(mask, 8)
    best = None                                                 # pick the most EMOJI-SHAPED blob, not the largest
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if not (28 <= w <= 110 and 28 <= h <= 110 and 0.6 < w / h < 1.7):  # emojis are ~square
            continue
        fill = a / (w * h)
        if fill < 0.45:                                         # emojis are SOLID; word fragments are gappy/wide
            continue
        if a < 700:                                             # too small to be a real emoji glyph
            continue
        score = fill / (1 + abs(w / h - 1.0))                   # squareness × solidity
        if best is None or score > best[0]:
            best = (score, int(cen[i][0]), int(cen[i][1]) + BAND_Y0, int(w), int(h), int(a))
    if best is None:
        return None, text_bbox
    return {"cx": best[1], "cy": best[2], "w": best[3], "h": best[4], "area": best[5]}, text_bbox


def track(captioned, master, t0, t1, fps=24.0):
    out = []
    t = t0
    while t < t1:
        cap, mas = _frame(captioned, t), _frame(master, t)
        if cap is not None and mas is not None:
            e, tb = _emoji_in_frame(cap, mas)
            if e:
                e["t"] = round(t, 3)
                if tb:                                          # emoji position RELATIVE to the text block
                    e["rel_dx"] = e["cx"] - tb["cx"]            # +right of text center
                    e["rel_dy"] = e["cy"] - tb["bottom"]        # +below text bottom
                    e["text_cx"] = tb["cx"]; e["text_bottom"] = tb["bottom"]
                out.append(e)
        t += 1.0 / fps
    return out


if __name__ == "__main__":
    cap, mas, t0, t1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    for e in track(cap, mas, t0, t1):
        print(f"  t={e['t']:.3f}  cx={e['cx']:3d} cy={e['cy']:4d}  {e['w']:3d}x{e['h']:3d}  area={e['area']}")
