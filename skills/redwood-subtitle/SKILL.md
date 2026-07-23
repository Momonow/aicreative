---
name: redwood-subtitle
description: Burn "Redwood" captions — ALL-CAPS tracked Anton, white with black stroke, and a hot-pink rounded box that karaoke-tracks the spoken word (synced to Scribe word timings). Use when the user says "Redwood captions/subtitles", "pink karaoke captions", "pink highlight subtitles", or wants the reference style from ad-1926019294732556. Engine: scripts/caption_redwood.py.
---

# redwood-subtitle

```bash
.venv/bin/python scripts/caption_redwood.py <in.mp4> --out <out.mp4> --vertical-pos <ASK>
.venv/bin/python scripts/caption_redwood.py <in.mp4> --preview 8      # vpos candidates first
.venv/bin/python scripts/caption_redwood.py <in.mp4> --out <out.mp4> --caption-end <SECONDS>  # preserve full video, stop captions before dense screens
.venv/bin/python scripts/burn_disclaimer.py <out.mp4> <out>_disclaimer.mp4   # combo
```

LOCKED spec (do NOT re-derive; calibrated vs the reference 2026-07-15):
- Font **Anton** (`assets/fonts/Anton-Regular.ttf`) + **tracking 0.055em** (tracked Anton = the
  reference look; Montserrat is too wide, untracked Anton too tight).
- **Width-anchored size** `px = width * 16/9 * 0.0336` (Hormozi guideline).
- ALL-CAPS, punctuation KEPT. White fill, black stroke 0.08em, soft shadow 0.045em.
- **Pink box `rgb(219,18,86)` karaoke-tracks the spoken word**: fires on each Scribe word start,
  HOLDS until the next word. Box = real stroked ink bbox (textbbox) + symmetric **0.10em margin**
  on all four sides, radius 0.22*box_h. Words drawn at explicit cursor positions (same coordinate
  system as the box — never anchor="mm" + advance math).
- Maximum 3 words/card, cards never straddle sentence ends, card pop 0.95→1.0 over 0.10s. Shorter cards prevent legal and medical phrases from turning into edge-to-edge banners.
- Every card must be fit from the rendered RGBA bounds of every karaoke-word variant, not from plain `textlength()`. Tracking, outline, shadow, and pink-box padding all count. Require at least an 8% horizontal viewport margin on both sides and shrink until every variant passes.
- **vpos is per-video — run --preview and ASK the user** (0.80 for the 2026-07 DJI yapper set).
- Pilot ONE video for sign-off before batching a set.
- Before delivery, inspect a contact sheet spanning every video in the batch. A single passing pilot is not enough when different transcripts produce different line widths.
- The caption overlay must end with the source video (`overlay shortest=1:eof_action=endall`). Never let the caption PNG sequence extend the source, repeat its last frame, or alter native playback speed.
- For dense mobile forms with no safe caption area, use `--caption-end` at the exact first form frame. This stops drawing captions while preserving the source's full duration; do not use `--end`, which intentionally shortens the render.

Built with the `caption-engine-builder` method; sister engines: nick-subtitle, hormozi3.
