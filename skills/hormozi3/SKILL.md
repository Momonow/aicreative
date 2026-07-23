---
name: hormozi3
description: "Burn the in-house Submagic-style Hormozi 3 caption treatment: Montserrat Black all caps, rotating yellow/green/red line accents, subtle card pop, and optional animated emoji. Use when the user asks for Hormozi captions, Submagic Hormozi 3, rotating color captions, or energetic creator subtitles."
---

# Hormozi 3

Use `scripts/caption_hormozi3.py`. The renderer is transcript- and campaign-neutral by default.

## Command

```bash
.venv/bin/python scripts/caption_hormozi3.py input.mp4 --out output_hormozi3.mp4
```

Useful options:

| Flag | Default | Purpose |
|---|---:|---|
| `--font-ratio` | `0.0336` | Width-anchored glyph size |
| `--max-words` | `4` | Maximum words per card |
| `--max-lines` | `2` | Maximum wrapped lines |
| `--vertical-pos` | auto | Per-video caption center |
| `--no-emoji` | off | Disable emoji |
| `--biased` | empty | Comma-separated Scribe proper nouns |
| `--substitutions-json` | none | Explicit campaign spelling corrections |
| `--emoji-keywords-json` | none | Optional campaign keyword-to-emoji map |
| `--end` | none | Caption only the first N seconds for a test |

## Locked Visual System

- Font: Montserrat Black, all caps.
- Size is width-anchored and remains uniform across cards; shrink only on overflow.
- Wrap tightly, normally about two words per line.
- Default text is white; active-line accent rotates yellow, green, red.
- Use a black stroke and subtle shadow, with no glow.
- Each card pops from about 96% through a small overshoot to 100% in roughly 0.12 seconds.
- Cards are continuous; do not flash each word independently.

## Emoji System

- Place at most one relevant emoji on a card.
- Do not repeat the same emoji on consecutive placements.
- Bind the emoji lifetime to its card.
- Use the established directional slide set with a fixed short travel and a 0.30-second
  ease-in-out entrance, then hold.
- Keep emoji close to the text and never let it cover the caption.
- Prefer an available animated asset, then a supported static color glyph, then a PNG fallback.
- Use `--no-emoji` when the subject or format calls for a restrained register.

## Campaign Inputs

No campaign names or disclaimer text are built in.

```bash
.venv/bin/python scripts/caption_hormozi3.py input.mp4 \
  --out output.mp4 \
  --biased "ProductName,PersonName" \
  --substitutions-json config/campaigns/example/caption_substitutions.json
```

For an approved campaign disclaimer:

```bash
.venv/bin/python scripts/caption_hormozi3.py input.mp4 \
  --out output.mp4 \
  --disclaimer \
  --disclaimer-file config/campaigns/example/disclaimer.txt
```

The disclaimer is placed in the lowest-motion eligible window unless `--disclaimer-start` is
supplied. Load the relevant campaign disclaimer skill before using it.

## QA

- ElevenLabs Scribe is the timing source.
- Render the caption track to a PNG sequence and composite in one ffmpeg pass.
- Fit every rendered state, including stroke, shadow, emoji, and pop scale, inside mobile margins.
- Preview the actual speaker frame before locking vertical position.
- Verify full source duration and native playback speed after render.

## Related

- `yellow-text-sub`: single yellow active-word treatment.
- `redwood-subtitle`: pink karaoke word box.
- `nick-subtitle`: calm dark-box treatment.
- `caption-engine-builder`: new style reverse engineering.
