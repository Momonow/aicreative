---
name: hf-pip-composite
description: Build a deterministic HyperFrames picture-in-picture composite with a matted talking head animated over a still or video backdrop, optional title treatment, and beat-synced motion. Use for TikTok-style moving presenter overlays, proof backdrops, evidence imagery, or face-safe foreground/background compositions.
---

# HyperFrames PIP Composite

Use HyperFrames and GSAP to animate a foreground presenter matte over a backdrop. This skill owns
the reusable composition mechanics; backdrop content, title words, caption position, and campaign
claims remain project inputs.

Templates live in `assets/templates/`.

## Inputs

- approved presenter video
- background-removed presenter matte with alpha
- approved backdrop image or video
- final audio and Scribe word timings
- optional title text and brand font

## Build

```bash
npx hyperframes init project --example blank --resolution portrait --non-interactive
cp skills/hf-pip-composite/assets/templates/drift_facesafe.html project/index.html
npx hyperframes lint
npx hyperframes validate
npx hyperframes render --quality draft --output preview.mp4
npx hyperframes render --quality high --output final.mp4
```

Replace the template asset names and placeholder text inside the project copy.

## Face-Safe Layout

- Make the foreground presenter large enough to read on mobile.
- Crop into the presenter when needed so the head and upper torso stay prominent.
- Anchor foreground scaling at the bottom so growth moves upward predictably.
- Measure both faces at the largest scale and every horizontal waypoint.
- Keep a stable scale floor and cap; do not let the presenter shrink into a decorative inset.
- Place every waypoint deliberately. Repeated returns to one home position look mechanical.
- Select caption position from the actual composite preview; never inherit a campaign-specific
  vertical position.

## Motion Treatments

`drift_facesafe.html`

- continuous lateral glide
- gentle scale swell
- slow background counter-zoom
- best for sustained narration

`crash_facesafe.html`

- forceful opening push on the backdrop's focal proof
- presenter punch-in/punch-out
- settles into varied waypoints
- best for a high-impact hook

`hopper_facesafe.html`

- deliberate snap relocations
- background snap-zooms on the same beats
- use only when the reference supports jump-cut energy

Align emphasis moves to Scribe word starts for the important claim, proof, or CTA words. Keep
connective language visually calmer.

## HyperFrames Rules

- Video and audio elements must be direct children of the composition root.
- Keep the visual `<video>` muted and add a separate `<audio>` element.
- Define fonts through `@font-face`; do not depend on unavailable system fonts.
- Register one paused, finite GSAP timeline in `window.__timelines`.
- Do not use `Math.random` in composition JavaScript. Generate seeded literal waypoints outside
  the renderer when variation is needed.
- For VP9 alpha inspection, put `-c:v libvpx-vp9` before the input. Input-seeking can lose alpha;
  flatten a preview before extracting diagnostic frames.
- Render motion clean, then apply the selected caption skill as a separate pass.

## QA

- Preview first, middle, and last frame plus every motion beat.
- Check presenter matte edges, alpha, face occlusion, title fit, and caption-safe space.
- Confirm deterministic output by rerendering a short draft when the composition uses generated
  waypoints.
- Apply `video-post-production` framewise and audio QA before delivery.
