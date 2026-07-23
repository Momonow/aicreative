---
name: feed-4x5
description: Convert a portrait video (9:16, 3:5, etc.) to 4:5 — the tallest aspect supported on Instagram/Facebook feed. Auto-detects baked-in letterbox bars (Veo, Sora, etc.) and crops around them so the 4:5 output is fully filled, no black bars. Use when the user says "make it 4:5", "feed version", "4 by 5", "Instagram feed crop", or "Reels to feed".
---

# feed-4x5

Crop a portrait video to 4:5 (the max tallness Instagram/Facebook feed supports — 1080×1350 typical) while automatically detecting and removing baked-in letterbox bars from upstream generators.

## When to invoke

User asks for:
- "Make a 4:5 version" / "4 by 5" / "convert to 4:5"
- "Feed version" / "Instagram feed crop" / "Reels to feed"
- A non-Reels deliverable from a 9:16 source

## Why this skill exists

Veo (and several other generators) bake **black letterbox bars** into their portrait outputs. The frame metadata says 720×1280 but the actual content occupies only ~720×1080 in the middle, with ~100px black bars top + ~20px bottom. A naive `ffmpeg crop=720:900:0:0` to make 4:5 keeps those bars in the output — looks broken on feed.

This skill detects the content region first, then crops around the letterbox.

## The script

`scripts/crop_4x5.py` in the aicreative project.

```bash
.venv/bin/python scripts/crop_4x5.py <input.mp4> [--out out.mp4] [--bias top|center|bottom]
```

If working in a project without it, the source is at `/Users/harry/aicreative/scripts/crop_4x5.py` — copy it.

## How it works

1. `ffprobe` reads source dimensions.
2. `ffmpeg -vf cropdetect=24:2:0` samples ~100 frames starting at t=2s, returns the actual non-black content region as `(x, y, w, h)`.
3. Compute the largest 4:5 window that fits inside the content area. Anchor vertically by bias (default `top` keeps face / upper body, drops couch).
4. `ffmpeg crop=...` + h264 re-encode (`crf 19`, audio copy).

## Bias options

| Bias | When |
|---|---|
| **`top`** (default) | Selfie / talking-head UGC. Keep face + upper body; drop chest/floor below. |
| `center` | Generic content where the subject is mid-frame. |
| `bottom` | Rare. Use only if the important content is at the bottom of the source. |

## Workflow with captions (full chain)

Generic chain:

```bash
.venv/bin/python scripts/crop_4x5.py input_9x16.mp4 \
  --out output_4x5.mp4
.venv/bin/python scripts/caption_styled.py output_4x5.mp4 \
  --out output_4x5_captioned.mp4 \
  --highlight-style yellow_text
```

The `yellow-text-sub` skill (sister to this one) handles caption rendering and auto-adjusts caption Y position based on the new aspect (lands below chin regardless of crop).

## Output dimensions

| Source | After cropdetect | After 4:5 crop |
|---|---|---|
| 720×1280 Veo (with letterbox) | 720×1080 content | 720×900 |
| 1080×1920 Sora (with letterbox) | 1080×~1620 content | 1080×1350 |

Width is preserved; height is recomputed to width / 0.8.

## Edge cases

- **No letterbox detected**: skill uses the full frame. Output is still 4:5.
- **Source already 4:5 or wider**: `cropdetect` returns close to full frame; script computes a narrower-than-source 4:5 window centered horizontally.
- **Odd dimensions**: forced to even (h264 requirement).

## Related skills

- `yellow-text-sub` — burns the per-word yellow-highlight captions onto the 4:5 video. Auto-adjusts caption Y by aspect so they always land below the chin.
