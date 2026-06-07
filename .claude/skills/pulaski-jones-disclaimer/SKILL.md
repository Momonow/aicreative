---
name: pulaski-jones-disclaimer
description: The exact verbatim legal disclaimer text + on-screen styling for the Jordan M. Jones / Adam Pulaski (CCWF Chowchilla women's prison sexual abuse) advertising campaign. Use when the user asks for "the disclaimer", "the legal text", "Pulaski/Jones disclaimer", "Chowchilla disclaimer", "CCWF disclaimer", or any prison-abuse legal-ad disclaimer overlay.
---

# pulaski-jones-disclaimer

The legal disclaimer for the **Jordan M. Jones / Adam Pulaski** law-firm campaign targeting **California women's prison (CCWF / CIW Chowchilla) sexual-abuse survivors**. This is the exact text + styling required on every ad creative for that campaign.

## When to invoke

User asks for:
- "Add the disclaimer" / "the legal text" / "the disclaimer"
- "Pulaski/Jones disclaimer" / "Chowchilla disclaimer" / "CCWF disclaimer"
- A prison-abuse legal-ad attorney disclaimer
- Compliance text for the women's-prison-abuse campaign

## The exact text — DO NOT PARAPHRASE

```
Paid legal advertisement. Jordan M. Jones, Attorney at Law (360 E 2nd St #820, Los Angeles, CA 90012) and Adam Pulaski, Attorney at Law (2925 Richmond Ave #1725, Houston, TX 77098) are responsible for this advertisement. A California-licensed attorney is associated for CA cases. This ad uses paid actors, dramatizations, and AI-generated imagery for illustration only and does not depict real clients or events. No guarantee or prediction of outcome is made. Cases may be referred to other attorneys.
```

This is REGULATED advertising copy. Every word, comma, and parenthetical is intentional. Do not modify, summarize, reorder, or "improve" it. If the user asks to tweak it, push back and confirm — they're likely the lawyers' client and need to coordinate with counsel.

## Attorney details (so you can verify nothing drifted)

| Field | Value |
|---|---|
| Lead attorney 1 | Jordan M. Jones, Attorney at Law |
| Address 1 | 360 E 2nd St #820, Los Angeles, CA 90012 |
| Lead attorney 2 | Adam Pulaski, Attorney at Law |
| Address 2 | 2925 Richmond Ave #1725, Houston, TX 77098 |
| Jurisdictional note | "A California-licensed attorney is associated for CA cases." |
| Production note | "uses paid actors, dramatizations, and AI-generated imagery for illustration only" |
| Outcome disclaimer | "No guarantee or prediction of outcome is made." |
| Referral clause | "Cases may be referred to other attorneys." |

## On-screen styling (when burning into a video)

Pair this with the `yellow-text-sub` skill (which has a `--disclaimer-text` flag). Defaults already match the campaign's reference creatives:

| Setting | Value | Why |
|---|---|---|
| Font | Arial Black + black stroke, white fill | Submagic / TikTok ad standard. |
| `fontsize_ratio` | `0.013` | ~1.3% of frame height. Tight, readable, doesn't dominate. |
| `vertical_pos` | `0.99` | Bottom-anchored at 99% — flush with bottom edge. |
| Hard cut in | `7.0s` | Default per campaign reference. |
| Hard cut out | `12.0s` | ~5s on-screen window. |
| Layer | Below captions | Captions stay readable on top. |
| Transition | **Hard cut both edges**, NO fade | Per `feedback_disclaimer_hardcut_default` memory rule. |

## How to invoke

If the active project has `caption_styled.py` (yellow-text-sub script):

```bash
# Default — campaign-standard 7-12s window
.venv/bin/python scripts/caption_styled.py path/to/in.mp4 \
  --out path/to/out.mp4 \
  --highlight-style yellow_text
# (disclaimer text + timing already defaults to this campaign)

# Custom window
.venv/bin/python scripts/caption_styled.py path/to/in.mp4 \
  --out path/to/out.mp4 \
  --highlight-style yellow_text \
  --disclaimer-start 5 --disclaimer-end 10

# Just the disclaimer, no captions → scripts/burn_disclaimer.py (same styling + calmest-window
# placement as the combo, but NO caption track). See the caption-disclaimer skill.
.venv/bin/python scripts/burn_disclaimer.py path/to/in.mp4 path/to/out.mp4
```

With the **`hormozi3`** caption script (`caption_hormozi3.py`) — use the `--disclaimer` flag, which **auto-places the disclaimer at the calmest "most boring" window** (no manual timing needed):

```bash
# Captions + disclaimer, auto-placed at the lowest-motion stretch
.venv/bin/python scripts/caption_hormozi3.py path/to/in.mp4 --out path/to/out.mp4 --disclaimer

# Force the window / length
.venv/bin/python scripts/caption_hormozi3.py path/to/in.mp4 --out path/to/out.mp4 \
  --disclaimer --disclaimer-start 20 --disclaimer-secs 6
```

`--disclaimer` defaults to this exact verbatim text, white + black stroke, vertical 0.99, **under** the captions, 6s. Override text with `--disclaimer-text "..."`.

### Auto "most boring window" placement (`find_boring_window`)

`caption_hormozi3.py:find_boring_window()` runs a **motion analysis** — samples the video at 2fps, computes frame-to-frame mean-absolute-difference, and picks the lowest-motion contiguous window of `--disclaimer-secs`, **skipping the first/last 4s** (hook / CTA). This drops the legal text into the calmest visual moment so it doesn't fight the hook or the call-to-action. Per-ad it auto-selects a different window. Override with `--disclaimer-start`.

If the project doesn't have the scripts: sources are at `/Users/harry/aicreative/scripts/caption_styled.py` and `/Users/harry/aicreative/scripts/caption_hormozi3.py`. Copy them.

## Visual reference

Reference creatives at `/Users/harry/Desktop/0502*.mp4` (the Pulaski/Jones reference UGC ads).

## Related

- `caption-disclaimer` — the router for the burn-in step: subtitle-only / disclaimer-only / combo. Use it to decide which layers go on a deliverable.
- `yellow-text-sub` — caption rendering + disclaimer overlay together (manual `--disclaimer-start/-end` window).
- `hormozi3` — Hormozi-style captions; its `--disclaimer` flag burns this text in with **automatic** calmest-window placement (`find_boring_window`).
- Memory `feedback_disclaimer_hardcut_default` — confirms hard-cut is the campaign default.
- Memory `feedback_explicit_sexual_abuse_qualifier` — the spoken script must explicitly include "sexual abuse" as a beat (a separate but related campaign rule for the script copy, not the disclaimer text).
