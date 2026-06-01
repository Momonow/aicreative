# Submagic emoji-matching model (caption_hormozi3.py)

How the in-house Hormozi-3 captions reproduce Submagic's animated emoji track. Built by
**dissecting the Submagic export frame-by-frame** (diff each 24fps frame vs the clean master to
isolate the emoji on an identical background; the dominant compact blob below the text = the emoji).

## Per-emoji spec (`submagic_emoji_inventory.json`)

Each emoji carries: `emoji` (glyph), `t` (rough time), `_appear` (exact captured appearance frame),
`cx`/`cy` (rest position), and `motion` `{type, s0, dur, peak, ramp, traj}`.

- **`traj`** = captured per-frame `[[t_rel, dx, dy], ...]` offsets from rest. The renderer REPLAYS
  this so the slide path/speed/acceleration match Submagic frame-for-frame.
- Scale: snappy **overshoot-pop** (reach ~full in ~1 frame, bounce to ~1.10, settle to 1.0). 🦸 is
  the one gradual grow.

## Placement rules (user-locked, 2026-06)

Submagic places emojis under a keyword, so off-center is *intentional only when the emoji visibly
travels there*. A subtle slide parked far off-center reads as a broken "off-center static". So:

| Group | Travel | Rest position |
|---|---|---|
| **Static** (no real motion) | 0 | **centered** (cx≈359) |
| **Subtle sliders** (≲80px, e.g. 🔢 🏆 🔒 👊 ✅) | 20–67px | slide in, **rest centered** |
| **Big sliders** (≳200px, e.g. 📖 😴 🚫 💸) | ~230px horizontal | rest **off-center** (under keyword) — the long travel makes it obviously intentional |

- **Vertical**: emoji sits ~16px BELOW *our* text block (`ey = y0 + text_h + 16`). Do NOT pin to
  Submagic's absolute cy — our caption sits lower than theirs, so an absolute-cy pin lands the emoji
  ON our words. Position relative to OUR subtitle so it never blocks the text.
- **Multi-part glyphs** (💰 money-bag, 📊 bar-chart, 💸) render as several colored blobs; the
  position capture can lock onto one part and read as off-center. Verify the true CENTER (merge parts)
  — 💰/📊 are centered in Submagic, not off-center.
- **Size**: fixed ~68px box (`es = int(width*0.095)`) ≈ Submagic's mean ~69px.

## Pipeline

1. `scripts/rederive_emoji.py` — dissect every frame → rest (cx,cy) + appearance + trajectory per emoji.
2. Written into `submagic_emoji_inventory.json`.
3. `caption_hormozi3.py --submagic-cards <cards.json> --submagic-emojis <inventory.json>` replays it.
4. Verify: `scripts/emoji_match_report.py` (position/scale per frame) + `scripts/emoji_diff_track.py`.

## OPEN ITEM — emoji RATE + missing glyphs (flagged 2026-06)

A full-video scan found **Submagic uses ~29 emojis (~14/min); our inventory only has 14 (~7/min)** —
about HALF. ~15 are missing (≈0:00, 0:20, 0:25, 0:28, 0:42, 0:45, 0:55, 1:05, 1:10, 1:12, 1:23, 1:34,
1:45, 1:49, 1:53, 1:56, 1:58), and a few glyphs are wrong (e.g. 0:10 should be **😔/🥺**, not 😴;
missing **🧘** 0:42, **👩‍💼** 1:23, **⏳** 1:49). TODO: rebuild the inventory to all ~29 with correct
glyphs so the rate + choices match Submagic. Scan tooling: the full-scan loop in this session +
`scripts/analyze_submagic_emojis.py` / `scripts/track_emojis.py`.
