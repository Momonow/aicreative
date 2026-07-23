# CLAUDE.md - aicreative

This repository produces videos, images, paid-social creative, and campaign assets. Keep the always-on rules here short. Load specialist skills for detailed workflows and keep campaign facts in memory or `inventory/`.

## Instruction Order

1. `/Users/harry/aicreative/AGENTS.md`
2. This file
3. The relevant skill in `/Users/harry/.codex/skills/`
4. Campaign memory or `inventory/`
5. Historical detail in `docs/video-production-learnings-archive.md` only when troubleshooting an old edge case

Do not copy campaign-specific people, scripts, IDs, or provider incidents back into this file.

## Video Skill Router

Start every video task with `video-production`.

| Work | Skill |
|---|---|
| End-to-end planning, reference analysis, routing, and delivery | `video-production` |
| AI people/scenes, image-to-video, provider choice, continuity, generation QA | `ai-video-generation` |
| Editing, B-roll timing, audio, captions, aspect variants, final QA | `video-post-production` |
| Performance ads, AdSwipe, regulated copy, AdMachin drafts/launches | `admachin-video-ads` |
| Paid-social primary/headline structure diversity | `ad-copy-formats` |
| Caption styles | `redwood-subtitle`, `hormozi3`, `nick-subtitle`, `yellow-text-sub`, `embedded-captions` |
| New caption-style clone | `caption-engine-builder` |
| PIP/stacked formats | `pip-composite`, `hf-pip-composite`, `stacked-format` |
| Motion graphics/compositions | `hyperframes` and its routed specialist |
| Existing talking-head recut | `talking-head-recut` |
| Podcast/interview creative | `podcast-video` |
| Feed aspect conversion | `feed-4x5` |

The installed `general-video` skill is a HyperFrames fallback, not the universal production skill.

## Locked Provider Defaults

- Speech-to-text: ElevenLabs Scribe. Never use Whisper.
- GPT image: `kie_client.generate_gpt_image` at 2K.
- Veo 3.1: useapi Google Flow unlimited:
  `googleflow_client.generate_veo(model="veo-3.1-lite-low-priority")`.
- Never switch Veo to Poyo, KIE, OpenRouter, or another paid host without explicit approval.
- Seedance: useapi `seedance-2` at 480p for high-volume B-roll unless the user chooses another route.
- Local work is ffmpeg, Tesseract, inspection, and orchestration. Keep generation/transcription API-first.
- Show the exact provider/model and full prompt before generated-media submission.
- Calculate expected cost or credits before bulk work.

## Universal Production Gates

### Inspect

- Probe sources with `ffprobe`.
- Use `dissect.py` for reference analysis and finished-video diagnosis.
- Read transcript, scene map, representative frames, and audio measurements together.
- For a reference clone, map the function of every visual insert, not only the spoken copy.

### Approve

- Show proposed host/persona stills before animation.
- Show proposed B-roll individually before final assembly when the user is curating assets.
- Every ad in a multi-ad batch uses a visibly different approved person unless reuse is explicitly approved.
- Show each generated video immediately, before deep QA or cleanup.

### Generate

- The first frame is the sole visual truth for image-to-video.
- Prompts describe action, voice, dialogue, camera behavior, and intentional changes only.
- Never restate appearance, medical details, wardrobe, setting, lighting, or framing.
- Pilot the highest-risk clip first.
- Preserve accepted clips, persist task IDs, and reroll only the failing unit.
- Use deterministic-random, eyes-open, forward-gaze frames from accepted clip 1 when a continuous
  presenter needs multiple clips. Never recursively anchor from clip 2, clip 3, and onward.

### Edit

- Keep every source at native playback speed.
- Never slow, speed up, time-stretch, duplicate, freeze, or hold frames to repair timing or defects.
- Use native-speed trims, stronger coverage, or regeneration.
- Frame-quantize every visual boundary.
- Adjacent B-roll shots share one exact boundary or have a deliberate host run between them.
- Never allow a one- or two-frame host flash.

### Audio

- Prefer raw model audio for one ad generated from one persona.
- Use `voice_changer` only for measured timbre drift, cross-video persona consistency, or music/room cleanup.
- Run both `scripts/audio_match.py` and `scripts/voice_consistency.py`.
- Apply final loudness on the assembled master.
- When using ffmpeg `alimiter`, set `level=disabled`; default makeup can undo the LUFS target.
- Measure final integrated LUFS and true peak after rendering.

### Captions

- Route through an existing named caption skill before modifying a renderer.
- Fit from rendered bounds, including tracking, stroke, shadow, highlight box, and animation scale.
- Preserve mobile horizontal margins.
- Review every video's longest cards; one pilot does not validate a batch.
- If a dense interface has no safe caption area, stop captions at its exact first frame while preserving the full video duration.
- Keep clean, captioned, and disclaimer versions separate.

### Final QA

- Use ElevenLabs Scribe for transcript verification.
- Canonicalize intended and heard text before rejecting harmless formatting/homophone differences.
- For image-to-video, compare the anchor against start/mid/end plus quarter-points for clips of 8 seconds or longer.
- Identity or scene drift is an automatic reroll; never hide it with B-roll or trimming.
- Before delivery run:

```bash
.venv/bin/python dissect.py <final.mp4> --every-frame --no-ocr
.venv/bin/python scripts/framewise_video_qa.py <final.mp4>
```

- Inspect every transition before/at/after.
- Reject black frames, freezes, isolated flashes, accidental visual runs under 12 frames, clipped captions, audio clipping, and changed source duration.

## B-Roll Standards

- Match the narrative function and emotional intensity of the spoken beat.
- Prefer specific human action, diagnosis, product, or proof over generic paperwork.
- Treat laptop/article screens as secondary proof when stronger human or real-world footage exists.
- Reject blank or unreadable phone/computer screens.
- Reels form footage uses true 9:16 mobile states with feed-readable text and no exposed selected answers or private data unless the task explicitly demonstrates those interactions.
- Upload approved generated B-roll to the project's asset library with descriptive title, tags, provider/model, and full prompt metadata. Verify the record.

## Paid-Social And Legal

- Load `admachin-video-ads` for strategy, copy, staging, or launch work.
- Present final headline and primary text verbatim for approval before creating AdMachin copy rows.
- Sensitive legal copy uses `may qualify` and `significant potential compensation`; never promise outcomes.
- Say `sexual abuse` explicitly when it is the qualifying harm.
- Keep the Pulaski/Jones disclaimer verbatim by loading its skill.
- AdMachin launches spend real money. Validate first, require explicit confirmation, and reconcile server-side runs after timeouts before retrying.

## Core Tools

- `dissect.py`: transcript, scenes, visual sampling, OCR, every-frame extraction
- `scripts/framewise_video_qa.py`: flashes, black frames, freezes, short runs, transition sheet
- `scripts/audio_match.py`: loudness/noise/spectral checks
- `scripts/voice_consistency.py`: speaker identity and F0
- `scripts/caption_redwood.py`: Redwood captions and `--caption-end`
- `scripts/pick_clean_anchors.py`: clean clip-1 anchor rotation with a reproducible manifest
- `scripts/crop_4x5.py`: crop-detect-aware feed conversion
- `admachin_client.py` and existing staging scripts: AdMachin automation

Prefer existing scripts and asset libraries over rewriting the same pipeline.

## Memory Placement

- Project-wide behavior: this file and `AGENTS.md`
- Reusable video behavior: live skill under `/Users/harry/.codex/skills/` and mirrored repo skill
- Campaign scripts, assets, IDs, rejects, and launch state:
  `/Users/harry/.claude/projects/-Users-harry-aicreative/memory/*.md` or `inventory/`
- Historical incidents and old provider details:
  `docs/video-production-learnings-archive.md`

When a reusable skill changes, update the live Codex copy and repo mirror together.

## Git Safety

- Multiple sessions may share this worktree and index.
- Recheck branch/status immediately before staging, pulling, committing, and pushing.
- Never revert changes from another session.
- Scan staged content for secrets before every push.
- Commit only the intended paths unless the user explicitly requests a complete repository sync.
- After a server timeout, verify remote state before repeating any action that can create or spend.
