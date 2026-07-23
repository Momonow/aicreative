---
name: yellow-text-sub
description: Burn compact creator captions with all-caps heavy text and a per-word yellow treatment, either yellow text or a yellow box behind white text. Use for TikTok, Reels, UGC, and social-video subtitles when the user asks for yellow karaoke captions or the legacy Submagic-style yellow treatment.
---

# Yellow Text Subtitle

Use `scripts/caption_styled.py` for a compact, word-timed creator-caption treatment.

## Default Look

- all caps, heavy sans-serif
- white words with black stroke
- active word rendered as yellow text or a yellow box
- two to three words per card
- aspect-aware lower-third placement
- adaptive shrink when a card exceeds its viewport allowance
- ElevenLabs Scribe word timings

Generic rendering contains no campaign-specific spelling replacements and no legal disclaimer.

## Commands

```bash
# Yellow active word
.venv/bin/python scripts/caption_styled.py input.mp4 \
  --out output_yellow.mp4 \
  --highlight-style yellow_text

# Yellow box behind the active word
.venv/bin/python scripts/caption_styled.py input.mp4 \
  --out output_box.mp4 \
  --highlight-style box

# Explicit position or sizing adjustment
.venv/bin/python scripts/caption_styled.py input.mp4 \
  --out output_yellow.mp4 \
  --highlight-style yellow_text \
  --vertical-pos 0.72 \
  --font-ratio 0.04
```

## Campaign Inputs

Proper-noun corrections must come from an explicit JSON file:

```bash
.venv/bin/python scripts/caption_styled.py input.mp4 \
  --out output_yellow.mp4 \
  --highlight-style yellow_text \
  --biased-keywords ProductName PersonName \
  --substitutions-json config/campaigns/example/caption_substitutions.json
```

An optional legal disclaimer must also be supplied explicitly:

```bash
.venv/bin/python scripts/caption_styled.py input.mp4 \
  --out output_with_disclaimer.mp4 \
  --highlight-style yellow_text \
  --disclaimer-file config/campaigns/example/disclaimer.txt \
  --disclaimer-start 7 \
  --disclaimer-end 12
```

Load the relevant campaign disclaimer skill; do not put that text or its corrections back into
this general skill.

## Rendering Rules

- Use `draw.textbbox()` including stroke for highlight geometry.
- Render the disclaimer below captions in the layer stack.
- Review the widest card at mobile size; do not trust character count alone.
- Pilot one video before batching.
- Keep the source duration and native playback speed unchanged.
- Preserve a clean master without captions or legal text.

## Related

- `hormozi3`: rotating accent colors, line emphasis, and animated emoji.
- `redwood-subtitle`: pink karaoke box with tracked Anton.
- `nick-subtitle`: calm white text on a dark rounded box.
- `caption-engine-builder`: create a genuinely new caption style.
