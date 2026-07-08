---
name: hf-pip-composite
description: HyperFrames TikTok-style PIP composite — a matted talking head (alpha webm) animated over a still backdrop (evidence photo) with a big title word. Use when the user says "pip composite", "talking head over backdrop", "scan/scar backdrop with her talking", "TikTok motion composite", "hyperframes composite", or wants the speaker to move around / zoom for emphasis over an image. USER-VALIDATED on the Depo gatekeeper ad (2026-07-09) — DRIFT is the picked primary motion, CRASH the approved opener; face-safe supersize layout law is locked.
---

# HyperFrames PIP composite (TikTok motion)

Deterministic HTML→MP4 render (HyperFrames + GSAP) compositing a **matted UGC talker** over a
**still backdrop** (the "evidence": hospital selfie, scan, document) with a big title word.
Replaces the static ffmpeg overlay when the user wants the talker to **move/zoom like TikTok**.

Reference build: `outputs/depo_tt/ad05_gatekeeper/composite/hf_v8_drift_fs.mp4` (drift) and
`hf_v6_facesafe.mp4` (crash). Templates in `templates/` (drop-in `index.html` for a project).

## Asset prep (existing pipeline)

1. Backdrop still: nano-banana (permissive on medical/scar imagery — gpt-image-2 REFUSES realistic
   MRI/anatomy) or gpt-image-2 for benign scenes. Must read AUTHENTIC (phone-selfie framing, not
   staged documentary — user rejected the cinematic hospital shot for a casual selfie w/ staples).
2. Talker matte: `fal_client.remove_background(video, out.webm)` → VEED vp9-alpha webm (keeps audio).
3. Word timings for beats: dissect the assembled ad audio; emphasis words drive the motion.

## Project setup (no bun needed — node 22+ + ffmpeg)

```bash
npx hyperframes init proj --example blank --resolution portrait --non-interactive
cp backdrop.png proj/assets/ ; cp matte.webm proj/assets/ ; cp Montserrat-Black.ttf proj/assets/fonts/
# author index.html from templates/, then:
npx hyperframes lint && npx hyperframes validate
npx hyperframes render --quality draft --output out.mp4     # iterate; --quality high to deliver
```

## FACE-SAFE SUPERSIZE layout law (user-locked)

The talker must read BIG but must NOT hide the backdrop subject's face ("people should look at
the face"). The compromise (approved): crop INTO the talker — head + chest only, shoulders/body
cut by the box — as a wide band rising from the bottom edge.

```css
#pip{position:absolute;left:90px;bottom:0;width:900px;height:850px;
     object-fit:cover;object-position:50% 12%;      /* head-focused crop */
     transform-origin:bottom center;z-index:2;}      /* scale grows UP from bottom */
```

- Canvas 1080×1920. Talker band top edge ≈ y1070 at rest — BELOW the subject's chin.
- Scale range **0.97–1.12 only** (bigger scales re-cover the face); big scales bias x to a side.
- Positions x ∈ [−260, 260]; **never return to a "home" position** (user: repeated home = fake);
  every waypoint is a new spot (min 140px from previous).
- Size floor is a hard rule: she must never appear smaller than the largest size of the prior
  approved render (user iterated bigger twice — small corner insets are rejected).
- Title word (e.g. MENINGIOMA): full-width top band, Montserrat Black ~140px, white +5px black
  stroke on rgba(0,0,0,.42) band, z-index above all; slam-in entrance (`from scale:1.6, power3.out`).

## Motion treatments (user-picked)

**DRIFT (primary):** one continuous glide, no stops.
```js
gsap.set("#pip",{x:-160,scale:0.97});
tl.to("#pip",{x:160,duration:9.6,ease:"sine.inOut"},0.2);
tl.to("#pip",{scale:1.12,duration:4.8,ease:"sine.inOut",yoyo:true,repeat:1},0.2);
tl.fromTo("#bg",{scale:1.26},{scale:1.02,duration:9.8,ease:"sine.out"},0);
```
For long ads: chain drift glides in 8–12s segments (alternate direction + swell timing).

**CRASH (approved opener / alt):** drastic open — backdrop punched in tight on the evidence
(set bg `transform-origin` near it, e.g. `38% 20%` for a scalp scar) then whips out with a small
re-punch, while the talker enters big and hard-punches out/in; then wander (seeded random walk,
varied ease per hop: elastic/back/power2/sine). See `templates/crash_facesafe.html`.

**HOPPER (also OK):** instant jump-cut teleports (`duration:.05, ease:"none"`), backdrop
snap-zooms in sync. See `templates/hopper_facesafe.html`.

Beat sync: put emphasis moves ON the Scribe word times of the money words (meningioma /
compensation / Go); calm connective lines get the smaller/zoom-out waypoints.

## Hard-won gotchas

- **`<video>`/`<audio>` MUST be direct children of the composition root** — wrapped/nested media
  never decodes (renders blank). Audio = separate `<audio>` (same webm src), video stays `muted`.
- Text: our homebrew ffmpeg has NO drawtext, and HyperFrames text is plain HTML/CSS — declare
  fonts via `@font-face` (lint errors on unresolvable families like Impact).
- vp9 alpha: ffmpeg-side previews need `-c:v libvpx-vp9` BEFORE the input; input-seeking (`-ss`
  before `-i`) on alpha webm drops the alpha — flatten to mp4 first for frame extraction.
- Determinism: no `Math.random` in composition JS — generate waypoints in PYTHON (seeded) and
  emit literal tweens (pattern: `depo_hf/gen_walk.py`, seed 11).
- One paused GSAP timeline at `window.__timelines["<composition-id>"]`; finite repeats only.
- Draft render ≈ 3-4s/video-second (10s ≈ 40s wall). Renders are sequential — never two at once.
- Captions: render the motion composite CLEAN, then burn Hormozi (`--no-emoji`) after, Reels-safe
  `--vertical-pos ~0.80` (bottom 15% is Reels UI-unsafe; captions land on the talker's band —
  normal TikTok look).
