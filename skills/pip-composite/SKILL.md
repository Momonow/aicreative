---
name: pip-composite
description: Build a "PIP composite" ad — a background-removed persona cut-out over a rotating vertical documentary backdrop with a slow docu-zoom, subtitle below the persona. Project-agnostic format recipe with locked defaults. Trigger on "PIP", "PIP composite/cut/version", "picture in picture", "persona/cutout over a backdrop", "greenscreen persona over b-roll". For the CA women's-prison application see memory feedback_pip_composite_cawp.
---

# pip-composite

A talking-head ad where the **background-removed persona sits in a corner as a commentator over a
full-frame documentary backdrop.** Works for ANY campaign — swap the persona, the backdrop set,
the caption engine, the disclaimer. Reference implementation: `scripts/cawp_pip_composite.py`
(rotating backdrops + varied zoom + drift; paths/backdrops are CAWP-specific, mechanics general).

## Locked defaults (apply automatically — do NOT re-ask)

- **Persona background-removed via VEED on fal** (`fal_client.remove_background` → vp9 **alpha**
  webm). Two hard gotchas: put **`-c:v libvpx-vp9` BEFORE the webm input** or the alpha is lost;
  **VEED strips audio**, so mux audio from the original mp4.
- **Persona overlay:** anchored to one side (**default right**), height **~700** of the 1280
  canvas, with a subtle `sin()` **drift** so she isn't dead-still.
- **Backdrops are VERTICAL 9:16 stills** — generate them 9:16 (not 4:3) so there's no
  blur-letterbox. Compose the action **center/upper** so the corner PIP never covers it. The
  builder takes a COMMA LIST of backdrop slugs and **hard-cuts every ~5 s** (`--interval 5`),
  each segment with a **different zoompan recipe** (push-in / pull-back / left- / right-bias) so
  it never looks templated. A single slug = one static backdrop with a slow zoom.
- **Subtitle: caption engine at `--vertical-pos 0.78`** — the PIP override that lands the caption
  on the torso, clear of the face, above the mobile-feed UI. (Started at 0.85; 0.78 is the locked
  value.) Then disclaimer (if the project uses one).
- **Pipeline per video:** bg-remove (skip-if-exists) → composite → caption at `0.78` → disclaimer.
- **The user curates the backdrop per ad** — present a labeled contact-sheet board, let them pick
  a pool, then map one per video by angle and show the mapping. **Pilot ONE** before batching.

## What's per-project (supply these)

- The persona/master videos, the vertical 9:16 backdrop set (generate project-appropriate stills),
  the caption engine, the disclaimer text (if any), output dir. Any content rules on the backdrops
  (e.g. CAWP = male guards only) live in the campaign memory, not here.

## Related
- `stacked-format` — the sibling format (b-roll top / persona bottom).
- `feedback_pip_composite_cawp` (memory) — the CA women's-prison application (male-guard backdrops,
  Nick captions, Pulaski disclaimer, backdrop generator/mappings).
- `caption-engine-builder`, `nick-subtitle` — caption engines for the burn-in.
