# Provider Routing

Current project defaults:

| Need | Provider and model | Rule |
|---|---|---|
| Veo 3.1 | useapi Google Flow `veo-3.1-lite-low-priority` | Unlimited default for every Veo 3.1 clip. Retry/resume; no paid fallback without approval. |
| GPT image | KIE `generate_gpt_image`, 2K | Default for persona and scene stills. |
| Seedance | useapi `seedance-2`, 480p | High-volume generated B-roll. Persist task IDs; explore queue can take hours. |
| Kling | useapi Kling 3 standard/pro | Use when element references or stronger multi-character control are needed. |
| Runway Gen-4 | useapi Runway wrapper | Use for supported general motion when selected for the job. |
| Speech-to-text | ElevenLabs Scribe | Never use Whisper in this project. |
| Voice change/clone | ElevenLabs direct | Use only for measured continuity or cleanup needs. |

Before any bulk run:

1. Confirm the route is still current in `CLAUDE.md`.
2. Calculate cost or credit exposure.
3. Pilot one clip.
4. Save provider task IDs immediately.
5. Use skip-if-exists and resume logic.

Provider failures do not justify silent switching. Queue outages, moderation, and deterministic prompt failures require different responses; identify which one occurred before retrying.
