---
name: stacked-format
description: Build a "stacked" talking-head ad — top half rotating static b-roll stills, bottom half the persona talking-head, subtitle burned at the 50% seam. Project-agnostic format recipe with locked defaults. Trigger on "stacked", "stacked cut/format/version", "b-roll on top persona on bottom", "split-screen ad", "50/50 b-roll + talking head". For the CA women's-prison application see memory feedback_stacked_broll_format.
---

# stacked-format

A talking-head ad split 50/50 vertically: **top = topic b-roll, bottom = the person.** The
b-roll carries the subject; the persona reads as commentary. Works for ANY campaign — swap the
persona video, the b-roll set, the caption engine, and the disclaimer (if any). Reference
implementation: `scripts/cawp_stacked_assemble.py` (paths/sequence are CAWP-specific; the
mechanics below are general).

## Locked defaults (apply automatically — do NOT re-ask)

- **Canvas 720×1280, split 50/50.** Top `720×640` = static b-roll stills. Bottom `720×640` =
  persona talking-head cropped from the master.
- **B-roll rotates on hard cuts, ~4.5 s/slot.** Curate the order so what LEADS is hook-relevant
  (the subject/most-arresting shots first) → context/establishing → texture last. Mix real
  footage frames with generated stills. Give a per-item **offset** into the rotation so a BATCH
  of ads doesn't all open on the same image.
- **Bottom-half crop is AUTO per persona** — detect the face and set `crop_y = face_top −
  0.36·face_h` so the top of the head lands at the seam and the face fills the bottom. Personas
  frame very differently; a fixed crop leaves dead space above low-framed faces. (`detect_crop_y`
  in the reference script; `--crop-y N` to override.)
- **Subtitle burned at the 50% seam** — caption engine at `--vertical-pos 0.50`.
- **Pipeline per video:** assemble → caption (project's engine) at `0.50` → disclaimer (if the
  project uses one).
- **Produce ALONGSIDE the regular full-frame cut** — deliver both.
- **Pilot ONE** before batching the set.

## What's per-project (supply these)

- The persona/master videos, the b-roll image set (real + generated, project-appropriate), the
  caption engine (Redwood / Nick / Hormozi / etc.), the disclaimer text (if any), output dir.

## Related
- `pip-composite` — the sibling format (persona cut-out over a full backdrop).
- `feedback_stacked_broll_format` (memory) — the CA women's-prison application + male-guard b-roll.
- `caption-engine-builder`, `redwood-subtitle` — caption engines to burn at the seam.
