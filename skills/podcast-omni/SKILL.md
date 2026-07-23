---
name: podcast-omni
description: Run the legacy Google Flow omni-flash implementation for a podcast-style talking-head video when the user explicitly requests omni-flash, Omni credits, or the existing podcast_omni_produce.py workflow. Use only as a provider adapter after loading podcast-video and ai-video-generation; do not select omni-flash merely because the requested format is a podcast.
---

# Podcast Omni Adapter

Load `podcast-video` for creative and performance decisions and `ai-video-generation` for anchor, transcript, continuity, and cost QA.

Use the active campaign job's resumable producer. Campaign scripts, personas, dialogue, and task
IDs do not belong in this provider adapter.

## Omni-Specific Rules

- `omni-flash` is credit-metered, not the unlimited Veo route.
- 4s/6s/8s/10s generations cost 15/20/25/30 Flow credits.
- Guardrail failures may still consume credits.
- Use `startImage` image-to-video unless the user explicitly requests reference-to-video.
- Keep prompts short and reference-led. Describe behavior, voice, exact dialogue, and camera lock; do not describe the host or set.
- Use low parallelism, persist every task ID, and never kill in-flight jobs expecting to save credits.
- Preserve accepted clips and reroll only the confirmed failing chunk.
- Trim harmless leading/trailing improvisation by Scribe word timestamps; do not spend another generation on words that fall outside the kept span.
- Reject missing intended words, stutters or repeats inside the kept span, material visual drift, or burned text.

## Provider Boundary

Do not carry Omni assumptions into Veo 3.1. The repository's default Veo route remains useapi Google Flow unlimited with `veo-3.1-lite-low-priority`.

Do not use Omni for silent generated B-roll merely from old campaign habit. Choose the current provider through `ai-video-generation` and confirm cost first.

## Campaign State

Old personas, scripts, guardrail incidents, and credit totals remain in campaign memory and the
historical archive, not this reusable adapter.
