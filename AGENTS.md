# AGENTS.md - aicreative

Read `/Users/harry/aicreative/CLAUDE.md` before working in this repository.

## Skill Loading

- Any video task: start with `/Users/harry/.codex/skills/video-production/SKILL.md`.
- Generated people, scenes, or B-roll: also load `ai-video-generation`.
- Editing, audio, captions, assembly, or delivery QA: also load `video-post-production`.
- Paid-social, AdSwipe, legal/tort copy, AdMachin staging, or launch: also load `admachin-video-ads`.
- Load caption, format, HyperFrames, and disclaimer skills only when their specialty is used.

The general video skills own reusable craft. Domain skills add constraints; campaign memory owns scripts, people, assets, IDs, rejects, and launch state.

## Durable Learning

- Project-wide operating behavior: `/Users/harry/aicreative/CLAUDE.md`
- Reusable behavior: live skill under `/Users/harry/.codex/skills/`
- Repo mirror: `/Users/harry/aicreative/skills/<skill>/`
- Campaign-specific notes: `/Users/harry/.claude/projects/-Users-harry-aicreative/memory/*.md` or `inventory/`
- Historical incident detail: `/Users/harry/aicreative/docs/video-production-learnings-archive.md`

When a reusable skill changes, update the live copy and repo mirror together.

## Locked Defaults

- STT: ElevenLabs Scribe, never Whisper.
- GPT image: KIE `generate_gpt_image` at 2K.
- Veo 3.1: useapi Google Flow unlimited with `veo-3.1-lite-low-priority`; no paid-provider fallback without explicit approval.
- Keep all video at native playback speed; no slowdown, speedup, time-stretch, duplicated frames, freezes, or holds.
- Treat image-to-video anchors as the sole visual truth and reroll material person/scene drift.
- Use named caption skills and run every-frame transition QA before delivery.
- AdMachin launch actions spend real money and require explicit confirmation.

## Repository Safety

- Put new campaign orchestration in `jobs/<campaign>/<concept>/`; keep reusable utilities in
  `scripts/`.
- Preserve stable legacy script paths unless deliberately migrating them with a compatibility
  wrapper.
- Multiple sessions may share the worktree and index.
- Recheck status immediately before staging, pulling, committing, and pushing.
- Never revert another session's changes.
- Scan staged content for secrets before every push.
