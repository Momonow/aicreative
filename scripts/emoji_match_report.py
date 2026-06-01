"""Frame-by-frame Submagic-vs-ours emoji match report. For each inventory emoji, diff-track it in
BOTH the Submagic export and our render, align by first-appearance frame, and report:
  - resting position (cx,cy)  -> tune `pos` + fine offset
  - scale curve (w / resting_w over the entrance)  -> tune s0 / dur / type
  - vertical entrance travel (cy - resting_cy over the entrance)  -> detect/tune drop
so we can drive per-frame position+movement to ~100% match.

  python scripts/emoji_match_report.py
"""
import json
import numpy as np
from emoji_diff_track import track

EO = "outputs/illinois_jdc_storytime_e_b14"
M = f"{EO}/story_e_b14_final.mp4"
SM = f"{EO}/story_e_b14_final_submagic_hormozi3.mp4"
O = f"{EO}/story_e_b14_final_hormozi_emoji.mp4"
inv = json.load(open("inventory/submagic_emoji_inventory.json"))


def _med(body, k):
    vals = [p[k] for p in body if k in p]
    return int(np.median(vals)) if vals else None


def rest(tr):
    """resting state = MEDIAN over the emoji's settled body (skip entrance frames). Returns absolute
    (cx,cy,w) AND position RELATIVE to the text block (rel_dx vs text center, rel_dy below text bottom),
    which is the position metric that matters (emoji sits relative to the subtitle, not absolute y)."""
    if len(tr) < 4:
        return None
    body = tr[4:] if len(tr) > 8 else tr[len(tr) // 3:]
    if not body:
        body = tr
    return {"cx": _med(body, "cx"), "cy": _med(body, "cy"), "w": _med(body, "w"),
            "rdx": _med(body, "rel_dx"), "rdy": _med(body, "rel_dy")}


def curve(tr, rcx, rcy, rw, n=8):
    """first n frames relative to appearance: (dt, dcx, dcy, w/rw)."""
    if not tr:
        return []
    t0 = tr[0]["t"]
    return [(round(p["t"] - t0, 3), p["cx"] - rcx, p["cy"] - rcy, round(p["w"] / max(1, rw), 2))
            for p in tr[:n]]


for e in inv["emojis"]:
    g, t = e["emoji"], e["t"]
    sm = track(SM, M, t - 0.35, t + 0.85)
    ou = track(O, M, t - 0.35, t + 1.05)            # our emoji may appear a touch later (timeline skew)
    rs, ro = rest(sm), rest(ou)
    print(f"\n{g}  inv_t={t:.2f} pos={e.get('pos')} motion={e['motion']}")
    if not rs or not ro:
        print(f"   SM frames={len(sm)} OURS frames={len(ou)}  -> INSUFFICIENT DETECTION")
        continue
    def fmt(d): return {k: v for k, v in d.items()}
    print(f"   ABS   SM cx={rs['cx']} cy={rs['cy']} w={rs['w']}   OURS cx={ro['cx']} cy={ro['cy']} w={ro['w']}")
    rel = ""
    if rs['rdx'] is not None and ro['rdx'] is not None:
        rel = (f"   REL-to-text  SM(dx={rs['rdx']:+d},dy_below={rs['rdy']:+d})  "
               f"OURS(dx={ro['rdx']:+d},dy_below={ro['rdy']:+d})  "
               f"|ΔRELdx|={abs(ro['rdx']-rs['rdx'])} |ΔRELdy|={abs(ro['rdy']-rs['rdy'])}")
    print(rel or "   REL-to-text  (text block not measured)")
    print(f"   appears SM t={sm[0]['t']:.2f}  OURS t={ou[0]['t']:.2f}  Δ={ou[0]['t']-sm[0]['t']:+.2f}s")
    print(f"   SM curve (dt,dcx,dcy,w/rw): {curve(sm, rs['cx'], rs['cy'], rs['w'])}")
    print(f"   OU curve (dt,dcx,dcy,w/rw): {curve(ou, ro['cx'], ro['cy'], ro['w'])}")
