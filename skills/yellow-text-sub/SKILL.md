---
name: yellow-text-sub
description: Burn TikTok / Submagic-style captions on a video — per-word YELLOW TEXT highlight (or yellow box behind white text), all-caps Arial Black, plus an optional legal disclaimer overlay at the bottom. Use when the user says "caption this", "add subtitles", "TikTok captions", "Submagic style", "yellow highlight subs", "burn captions", or wants captioned UGC ads.
---

# yellow-text-sub

Burns Submagic / TikTok-style captions onto a video. Each word gets highlighted YELLOW as it's spoken (with WHITE plain text for non-active words in the chunk). Optional legal disclaimer overlays at the bottom of the frame in a hard-cut window.

## When to invoke

User asks to:
- "Caption this video" / "add captions" / "add subtitles"
- "Submagic style" / "TikTok captions" / "yellow highlight subs"
- "Add the disclaimer too" or wants a legal-ad overlay
- Match a UGC ad reference where words are highlighted one at a time

## The script

`scripts/caption_styled.py` in the aicreative project.

```bash
.venv/bin/python scripts/caption_styled.py <input.mp4> --out <output.mp4> --highlight-style yellow_text
```

If working in a different project that doesn't have `caption_styled.py`, copy it in or rebuild from the spec below.

## Locked-in settings (user-approved 2026-05-12)

These are the values that produce the look the user signed off on. Do not change without asking.

### Captions

| Setting | Value | Notes |
|---|---|---|
| `--highlight-style` | **`yellow_text`** | Yellow fill on the spoken word (with black stroke). Other chunk words stay white. |
| `fontsize_ratio` | **`0.04`** (campaign-approved 2026-05-12) | ~4% of frame height. User signed off on this for the Chowchilla 4:5 deliverables — slightly larger than original 0.0336. Override with `--font-ratio 0.NN`. |
| `vertical_pos` | **auto by aspect** | `0.72` for 9:16 / 3:5, `0.82` for 4:5. **Caption ALWAYS lands just below the chin regardless of aspect ratio.** Linear interp `0.72 + (w/h - 0.6) * 0.5`, clamped `[0.70, 0.85]`. Override with `--vertical-pos 0.NN`. |
| `max_words` | `3` | 2-3 words per chunk; chunk also splits on >0.35s pauses. |
| `max_lines` | `2` | Adaptive font shrink (8% per attempt) if a chunk wraps wider. |
| Font | Arial Black (macOS) | Heavy display face. Falls back to Impact / DejaVu Sans Bold. |
| Stroke | `0.09 * fontsize` | Black outline; ~2px min. |
| Casing | UPPER | All caps. |

### Disclaimer

| Setting | Value | Notes |
|---|---|---|
| `--disclaimer-start` | `7.0` | Hard-cut IN at 7s. |
| `--disclaimer-end` | `12.0` | Hard-cut OUT at 12s. ~5s window. |
| `fontsize_ratio` | `0.013` | ~1.3% of frame height — Submagic-tight. |
| `vertical_pos` | `0.99` | Bottom-anchor at 99% (sits flush with bottom edge). |
| Layer order | disclaimer UNDER captions | Captions drawn on top so they stay readable over disclaimer. |
| Style | white text + black stroke | No background fill. |

### Default disclaimer text (Chowchilla / CCWF Pulaski + Jones campaign)

```
Paid legal advertisement. Jordan M. Jones, Attorney at Law (360 E 2nd St #820, Los Angeles, CA 90012) and Adam Pulaski, Attorney at Law (2925 Richmond Ave #1725, Houston, TX 77098) are responsible for this advertisement. A California-licensed attorney is associated for CA cases. This ad uses paid actors, dramatizations, and AI-generated imagery for illustration only and does not depict real clients or events. No guarantee or prediction of outcome is made. Cases may be referred to other attorneys.
```

This is the **exact** legal text the campaign uses. Don't paraphrase. Override with `--disclaimer-text "..."` for other campaigns or `--no-disclaimer` to skip.

## Whisper proper-noun fixups (built into script)

The script applies these substitutions to caption text before render (Whisper mistranscribes them, but the burned-in caption should show the correct spelling):

| Whisper output | Correct spelling |
|---|---|
| `MIHA`, `MEHA`, `NIHA`, `MI-HA`, `MEE-HAH` | `MIJA` |
| `CHOWCHILLY`, `CHOW CHILLER`, `CHOW-CHILLA`, etc. | `CHOWCHILLA` |

Add new fixups inline in `caption_styled.py:SUBSTITUTIONS` as needed.

## Standard invocations

```bash
# Full ad with disclaimer (most common — campaign default)
.venv/bin/python scripts/caption_styled.py outputs/.../final_lr01.mp4 \
  --out outputs/.../final_lr01_styled.mp4 \
  --highlight-style yellow_text

# No disclaimer
.venv/bin/python scripts/caption_styled.py path/to/in.mp4 \
  --out path/to/out.mp4 \
  --highlight-style yellow_text \
  --no-disclaimer

# Custom disclaimer window (e.g., from 3-9s)
.venv/bin/python scripts/caption_styled.py path/to/in.mp4 \
  --out path/to/out.mp4 \
  --highlight-style yellow_text \
  --disclaimer-start 3 --disclaimer-end 9

# Box style (yellow rect behind WHITE text — alternate visual)
.venv/bin/python scripts/caption_styled.py path/to/in.mp4 \
  --out path/to/out.mp4 \
  --highlight-style box
```

## Pipeline

The script does this internally — useful to know when debugging:

1. `ffmpeg` extracts mono 16kHz audio
2. Whisper (`small` by default) transcribes with word-level timestamps
3. Words grouped into 2-3 word chunks (split on >0.35s pause OR on `max_words` reached)
4. For EACH word in EACH chunk, render a separate transparent PNG showing the chunk text with that one word's color/highlight changed
5. ffmpeg `-filter_complex` overlay chain — disclaimer overlays first (under), then per-word caption frames in time-order (on top), each enabled via `between(t,start,end)` on its specific word's whisper-derived timestamp

## When the script needs a fresh build

If you're in a project without `caption_styled.py`, the full source is at `/Users/harry/aicreative/scripts/caption_styled.py`. Copy it. Don't rewrite from scratch — the rendering logic has subtle gotchas:

- **Yellow rect must use `draw.textbbox()` for positioning**, not `cur_y + line_h`. The latter includes line-leading and makes the box hang below the text. (Lesson learned the hard way.)
- **Tesseract on macOS must be invoked via stdin**, not file path — sandbox blocks file reads. (Only relevant if extending with OCR validation.)
- **Layer order matters**: in the `-filter_complex` chain, disclaimer overlay must come BEFORE caption overlays so captions render on top.
- **Whisper TSV `conf` is a float, not int** — parse with `float()`, not `int()`. (Filtering by confidence breaks silently otherwise.)

## Visual reference

Looks like the references in `/Users/harry/Desktop/0502*.mp4` and matches the "Submagic" / TikTok creator caption template. White text + black outline + per-word yellow-text highlight.

## Memory tie-ins

- `feedback_skip_burned_captions` — the user normally captions in post; this skill is invoked ONLY when they explicitly want burned captions on a deliverable.
- `feedback_disclaimer_hardcut_default` — disclaimer is hard-cut in/out (no fade), per the default settings here.
