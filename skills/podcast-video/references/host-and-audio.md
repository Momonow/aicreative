# Host And Audio

## Host Continuity

- Use the approved anchor as visual truth.
- Rotate clean eyes-open frames from clip 1 for later clips when needed.
- Do not re-describe the host, mic, studio, or wardrobe in image-to-video prompts.
- Compare anchor to start/mid/end and quarter-points on long clips.

## Voice

- Prefer raw model audio for one host in one ad.
- Measure with `audio_match.py` and `voice_consistency.py`.
- Use one cloned persona voice across variants only when measured drift or cleanup requires it.
- Voice changer can normalize timbre and remove music/room bleed, but it may preserve source pitch drift.

## Reactions

Natural room reactions belong between complete thoughts. Remove them from captions. A reaction inside diagnosis, eligibility, compensation, disclaimer, or CTA wording is a defect.
