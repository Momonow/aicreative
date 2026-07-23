---
name: pip-composite
description: Build a documentary picture-in-picture video with a background-removed presenter over full-frame rotating proof or context media. Use when the user asks for PIP, picture in picture, a presenter cutout over B-roll, or a commentator layered over evidence.
---

# PIP Composite

Use a large foreground presenter as commentary over full-frame proof or context media. Campaign
content, provider choice, caption style, and disclaimer are supplied separately.

## Inputs

- approved presenter video and alpha matte
- curated 9:16 backdrop set
- final audio
- selected caption skill
- optional campaign disclaimer skill

## Composition

- Use a true alpha foreground; verify alpha before assembly.
- Keep the presenter large enough to read on mobile, normally anchored to one side.
- Use restrained positional drift only when it supports the reference.
- Compose backdrop action away from the presenter so neither subject is hidden.
- Rotate backdrops at narratively meaningful beats, not a blind fixed cadence.
- Vary push-in, pull-back, and lateral crop motion across stills to avoid repetition.
- Start with the strongest hook-relevant proof, then context, then texture.
- Offset opening assets across a batch so every ad does not begin on the same image.

## Background Removal

Use the project-approved background-removal route from `media-use` or the existing pipeline.
When handling VP9 alpha:

- put `-c:v libvpx-vp9` before the alpha-webm input during ffmpeg decoding
- verify whether the removal service preserved audio
- if audio was removed, mux from the approved original presenter file

## Captions

- Preview the real composite and choose vertical position per video.
- Do not inherit a campaign-specific position.
- Check the caption at every foreground waypoint and on every backdrop.
- Apply legal text as a separate campaign-controlled layer.

## Workflow

1. Approve presenter and every proposed backdrop.
2. Remove the presenter background and verify alpha/audio.
3. Assemble one clean pilot.
4. Preview caption positions and obtain approval.
5. Render clean, captioned, and disclaimer variants separately.
6. Run `video-post-production` framewise and audio QA before batching.

## Related

- `hf-pip-composite`: deterministic HyperFrames motion treatment.
- `stacked-format`: proof above, presenter below.
- `caption-engine-builder`: create a new caption treatment.
