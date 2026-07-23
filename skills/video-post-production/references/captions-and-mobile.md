# Captions And Mobile

## Select An Existing Engine

- Redwood: tracked Anton, white/black, karaoke highlight box.
- Hormozi: bold compact word cards.
- Nick: controlled phrase captions for calmer or regulated work.
- Yellow: yellow text treatment.
- Embedded captions: cinematic/VFX treatments.

Use `caption-engine-builder` only when the user is cloning a genuinely new style.

## Fit Rules

- Size from output width, not height.
- Fit using rendered RGBA bounds for every active-word variant.
- Include tracking, stroke, shadow, highlight padding, and motion scale.
- Keep at least the style's required horizontal viewport margin.
- Review the longest medical, legal, and CTA phrases.
- Pilot one video, then inspect a contact sheet for every video in a batch.

For dense interface footage, move captions only when a safe area exists. Otherwise stop caption drawing at the exact first interface frame while preserving the full video duration.

The caption overlay must end with the source; never repeat or freeze the final source frame.
