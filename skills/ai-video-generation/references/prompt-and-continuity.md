# Prompt And Continuity

## Image-To-Video Prompt

The anchor already defines identity and scene. Prompt:

- action and restrained gesture
- gaze and speaking behavior
- voice/register/pacing
- exact dialogue
- camera behavior
- intentional requested change
- no unwanted text/music when relevant

Do not repeat age, ethnicity, face, hair, eyes, skin, scars, bandages, clothing, room, furniture, lighting, or framing. Re-description invites reinterpretation.

## Dialogue

- Use closed sentences with periods and commas.
- Avoid em dashes, trailing colons, quote-framing, and open lists.
- Keep one natural thought per clip.
- Prompt pronunciation for difficult medical/product/proper names.
- Require only the supplied words, in order, then stop.

## Anchor Rotation

After clip 1 passes, extract several eyes-open, forward-gaze frames from that accepted clip:

```bash
.venv/bin/python scripts/pick_clean_anchors.py clip01.mp4 \
  --out-dir outputs/<job>/anchors \
  --n 6 \
  --strategy random \
  --seed 17
```

The deterministic random subset prevents every later clip from inheriting the same transient
expression while keeping the anchor pool auditable in `anchor_manifest.json`.

- Rotate only clean frames from approved clip 1.
- Do not recursively seed clip 3 from clip 2, clip 4 from clip 3, and so on. That compounds
  generated defects and gradually degrades identity and scene fidelity.
- Keep a minimum temporal gap between picks so the pool is not six near-identical frames.
- Review the exported anchors before generation. Reject closed eyes, averted gaze, mouth
  distortion, transient hand occlusion, changed medical detail, or scene drift.
- The approved still remains the identity source of truth even when clip-1 frames are used for
  motion continuity.

## Identity Gate

Compare anchor versus start/mid/end, plus quarter-points for 8-second clips. Reject material changes in:

- face geometry or age
- skin or eye color
- hair
- medical details
- wardrobe
- room/furniture/lighting
- camera position/framing

Reroll the failing clip. Trimming around drift, covering it with B-roll, or freezing a frame is not a repair.
