---
name: caption-disclaimer
description: Burn captions and/or the legal disclaimer onto a finished video as a SEPARATE post-production step — pick a mode (subtitle-only, disclaimer-only, combo) AND a caption engine (in-house caption_hormozi3, the Submagic API, or the OpusClip API). Use when the user says "add the disclaimer", "captions only", "disclaimer only", "burn the subs", "one with disclaimer one with captions", "subtitle-only version", "caption with Submagic", "use the Submagic API", "OpusClip captions", "apply <template> template", or wants to choose which of caption/disclaimer goes on a deliverable. Routes to caption_hormozi3.py / submagic_client.py / opusclip_client.py + burn_disclaimer.py.
---

# caption-disclaimer

The **post-production burn-in step** — applied AFTER the video is generated/approved, to any video. Captions and the legal disclaimer are **independent layers**, so you pick one of three modes per deliverable. The user often wants a **pair**: e.g. one disclaimer-only (they add captions in their own tool) AND one subtitle-only, from the same clean master.

This skill is the router/decision step. The actual rendering lives in the engines below; don't re-describe their parametrics here.

## The three modes

| Mode | Command | What burns |
|---|---|---|
| **Subtitle only** | `caption_hormozi3.py <in> --out <out>` (NO `--disclaimer`) | captions only |
| **Disclaimer only** | `scripts/burn_disclaimer.py <in> <out>` | legal text only, no captions |
| **Combo** (both) | `caption_hormozi3.py <in> --out <out> --disclaimer` | captions + disclaimer |

All run from the project venv: `.venv/bin/python scripts/...`.

### Subtitle only
```bash
.venv/bin/python scripts/caption_hormozi3.py <in.mp4> --out <in>_hormozi.mp4
#   --biased "Chowchilla:3.0,CCWF:2.0"  (default; pass --biased "" for generic text)
#   --no-emoji  to drop the emoji layer
```
Caption look (Montserrat Black, rotating yellow/green/red, sliding emojis, position) → **`hormozi3`** skill. Alt single-yellow style → **`yellow-text-sub`** (`caption_styled.py`).

### Disclaimer only (no captions)
```bash
.venv/bin/python scripts/burn_disclaimer.py <in.mp4> <in>_disclaimer.mp4
#   --start <sec>   force window (default: auto calmest window)
#   --secs 6.0      how long it stays up
#   --text "..."    override text (default: verbatim Pulaski/Jones)
```
`burn_disclaimer.py` reuses the SAME `render_disclaimer` + `find_boring_window` as the combo path, so the disclaimer styling and placement are IDENTICAL to the combo version — just with no caption track. Verbatim legal text + styling → **`pulaski-jones-disclaimer`** skill (REGULATED — never paraphrase).

### Combo (captions + disclaimer)
```bash
.venv/bin/python scripts/caption_hormozi3.py <in.mp4> --out <in>_hormozi.mp4 --disclaimer
#   --disclaimer-start <sec> / --disclaimer-secs 6.0  to control the window
```

## Caption engines — in-house vs Submagic vs OpusClip

Captions can come from THREE engines; the disclaimer is always our `burn_disclaimer.py`. Pick by what matters: exact text + position control → in-house; authentic template library → Submagic; OpusClip if asked.

| Engine | Script | Look | Verbatim text? | Resolution | Caption position | Credits |
|---|---|---|---|---|---|---|
| **In-house** | `caption_hormozi3.py` | reverse-eng Hormozi 3 (Montserrat, yellow/green/red) | **YES** (we hold the script) | keeps source | **direct** `--vertical-pos` | free |
| **Submagic API** | `submagic_client.py` | authentic templates: `Hormozi 1-5`, `Lewis`, `Beast`, … | NO (auto-transcribe) | keeps 720×1280 | template / `userThemeId` / `presetId` only | ~1/min source |
| **OpusClip API** | `opusclip_client.py` | brand templates / `preset-fancy-*` | NO (auto-transcribe) | **upscales to 1080×1920** | brand template only | ~1/min source |

**Two rules that bite (both APIs):** (1) they **auto-transcribe** — no way to inject our exact script, so they reformat ("a hundred" → "$100") and can split cards oddly ("was Don't"); for regulated/legal copy prefer **in-house** and spot-check API output. (2) **Neither burns the disclaimer** → always do the engine captions FIRST, then `burn_disclaimer.py` on top (the combo).

Example (Submagic Lewis + disclaimer, the Chowchilla final set):
```bash
.venv/bin/python scripts/submagic_client.py caption <in.mp4> <in>_submagic_lewis.mp4 "Lewis" "Chowchilla,CCWF,CIW"
.venv/bin/python scripts/burn_disclaimer.py <in>_submagic_lewis.mp4 <in>_submagic_lewis_disclaimer.mp4
```

**Full API flows, endpoints, billing, template lists, and every gotcha → `references/external-caption-apis.md`.** Read it before driving either API.

## Naming convention (so the three flavors don't collide)

From one clean master `<name>.mp4`, emit:
- `<name>_hormozi.mp4`     — subtitle only OR combo (combo also has the disclaimer)
- `<name>_disclaimer.mp4`  — disclaimer only

Keep the clean master untouched as `<name>.mp4`. (Chowchilla podcast campaign used exactly this: `<L>_full.mp4` clean, `<L>_full_hormozi.mp4` combo, `<L>_full_disclaimer.mp4` disclaimer-only.)

## Placement is deterministic — modes stay consistent

Both the combo and disclaimer-only paths auto-place the disclaimer via `find_boring_window` (motion analysis: lowest frame-to-frame difference, skipping the first/last 4s hook/CTA). It's **deterministic on a given master**, so a disclaimer-only render and a combo render of the SAME video drop the legal text in the SAME window. A subtitle-only + disclaimer-only pair therefore composites cleanly if ever recombined.

## Batch / pair pattern

To make a disclaimer-only version of a set already captioned, run `burn_disclaimer.py` on the CLEAN masters (not the captioned outputs) so you don't stack a disclaimer on top of one already burned. To make BOTH flavors for a set, loop the clean masters through `burn_disclaimer.py` (→ `_disclaimer.mp4`) and `caption_hormozi3.py` with no `--disclaimer` (→ `_hormozi.mp4`).

## Default rule

Per project memory `feedback_skip_burned_captions`: do NOT burn captions onto deliverables unless asked. Only run this skill when the user explicitly requests captions and/or the disclaimer. Disclaimer overlays are a **hard cut** both edges, no fade (`feedback_disclaimer_hardcut_default`).

## Related

- `references/external-caption-apis.md` — full Submagic + OpusClip API flows, endpoints, billing, template lists, and gotchas. Read before driving either API.
- `hormozi3` — Hormozi-3 caption styling + its own `--disclaimer` flag (the in-house combo engine).
- `yellow-text-sub` — alternative single-yellow caption style (`caption_styled.py`).
- `pulaski-jones-disclaimer` — the verbatim legal text + on-screen styling (REGULATED).
- `podcast-omni` — generates the clips this burn-in step runs on.
- Scripts (in `aicreative/scripts/`): `caption_hormozi3.py` (in-house), `submagic_client.py`, `opusclip_client.py`, `burn_disclaimer.py`. Keys in `.env`: `SUBMAGIC_API_KEY`, `OPUSCLIP_API_KEY`.
