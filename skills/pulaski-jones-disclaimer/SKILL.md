---
name: pulaski-jones-disclaimer
description: Apply the exact regulated Jordan M. Jones and Adam Pulaski disclaimer for the California women's-prison sexual-abuse campaign. Use only for this campaign or when the user explicitly names the Pulaski/Jones, Chowchilla, CCWF, or CIW disclaimer.
---

# Pulaski/Jones Disclaimer

This is intentionally campaign-specific. Keep its copy, corrections, timing guidance, and
compliance behavior here rather than in general caption or video skills.

## Source Of Truth

Exact text:

`config/campaigns/pulaski-jones/disclaimer.txt`

Caption corrections:

`config/campaigns/pulaski-jones/caption_substitutions.json`

Never paraphrase, reorder, summarize, or silently edit the disclaimer. If counsel supplies a new
approved version, update the config first and retain the approval context in campaign memory.

## Exact Text

```text
Paid legal advertisement. Jordan M. Jones, Attorney at Law (360 E 2nd St #820, Los Angeles, CA 90012) and Adam Pulaski, Attorney at Law (2925 Richmond Ave #1725, Houston, TX 77098) are responsible for this advertisement. A California-licensed attorney is associated for CA cases. This ad uses paid actors, dramatizations, and AI-generated imagery for illustration only and does not depict real clients or events. No guarantee or prediction of outcome is made. Cases may be referred to other attorneys.
```

## Video Only

```bash
.venv/bin/python scripts/burn_pulaski_jones_disclaimer.py \
  input.mp4 output_disclaimer.mp4
```

The dedicated renderer uses the exact config text and defaults to a six-second, hard-cut window
at the lowest-motion eligible portion of the ad. Override with `--start` or `--secs` only when the
campaign edit requires it.

## Captions Plus Disclaimer

Yellow captions:

```bash
.venv/bin/python scripts/caption_styled.py input.mp4 \
  --out output_combo.mp4 \
  --highlight-style yellow_text \
  --substitutions-json config/campaigns/pulaski-jones/caption_substitutions.json \
  --disclaimer-file config/campaigns/pulaski-jones/disclaimer.txt \
  --disclaimer-start 7 \
  --disclaimer-end 12
```

Hormozi 3 captions:

```bash
.venv/bin/python scripts/caption_hormozi3.py input.mp4 \
  --out output_combo.mp4 \
  --substitutions-json config/campaigns/pulaski-jones/caption_substitutions.json \
  --disclaimer \
  --disclaimer-file config/campaigns/pulaski-jones/disclaimer.txt
```

Nick or Redwood captions:

```bash
.venv/bin/python scripts/caption_nick.py input.mp4 \
  --out output_nick.mp4 \
  --substitutions-json config/campaigns/pulaski-jones/caption_substitutions.json
.venv/bin/python scripts/burn_pulaski_jones_disclaimer.py \
  output_nick.mp4 output_nick_disclaimer.mp4
```

## Static Images

```bash
.venv/bin/python scripts/burn_pulaski_jones_disclaimer_image.py \
  input.png output_disclaimer.png --style auto
```

Available image styles are `auto`, `band`, `plain`, `fit`, and `bar`.

## Compliance Checks

- Compare the rendered copy with the config byte for byte before launch.
- Keep clean, captioned, and disclaimer versions separate.
- Preserve hard-cut edges; do not fade legal text unless counsel approves.
- Confirm the disclaimer does not cover the CTA, captions, or required interface content.
- Spoken copy for this campaign must say `sexual abuse` explicitly and use `may qualify` plus
  `significant potential compensation`.
