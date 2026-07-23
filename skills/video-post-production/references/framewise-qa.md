# Framewise QA

## Timeline Rules

- Pick a final FPS before editing.
- Store cuts as integer frames.
- Adjacent inserts share an exact boundary.
- If host footage appears between inserts, make it a deliberate readable run.
- Treat any unplanned visual run under 12 frames as suspect.

## Required Final Pass

```bash
.venv/bin/python dissect.py <final.mp4> --every-frame --no-ocr
.venv/bin/python scripts/framewise_video_qa.py <final.mp4>
```

Inspect:

- every cut's previous, boundary, and next frame
- black/blank frames
- frozen runs
- single-frame flashes
- unexpectedly short scene runs
- caption bounds
- final frame and audio tail
- source versus output duration/frame count

Automation flags candidates; human inspection decides whether a legitimate fast cut is intentional.
