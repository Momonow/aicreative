# AGENTS.md — aicreative

Use `/Users/harry/aicreative/CLAUDE.md` as the detailed operating manual for this project.
Use `/Users/harry/.codex/skills/admachin-video-ads/SKILL.md` as the reusable ad-production playbook.

## Persist Learnings In Three Layers

- Claude / project memory: `/Users/harry/aicreative/CLAUDE.md`
- Codex reusable skill: `/Users/harry/.codex/skills/admachin-video-ads/SKILL.md`, mirrored to `/Users/harry/aicreative/skills/admachin-video-ads/SKILL.md`
- Campaign-specific notes: `inventory/` or `outputs/<campaign>/..._learnings.md`

When the user asks to save session learnings, update the live Codex copy and the repo mirror together.

## Locked Defaults For This Repo

- STT = ElevenLabs Scribe, not Whisper.
- GPT image = `kie_client.generate_gpt_image` at 2K unless the user explicitly asks for another path.
- All Veo 3.1 clips = useapi Google Flow unlimited queue via `googleflow_client.generate_veo(model="veo-3.1-lite-low-priority")`. Never switch a Veo 3.1 job to Poyo, KIE, OpenRouter, or another paid provider without explicit user approval.
- Use clip-1 anchor rotation with eyes-open, forward-gaze frames. Let the approved image lock eye color and other visual traits; do not restate them in the video prompt.
- If the user says a winner angle is working, preserve framing/beat structure only as scaffolding; rewrite sentence structure and discovery mechanism so variants do not sound like synonym swaps.
- For a single ad from one persona seed, prefer raw model audio plus loudness leveling. Use `voice_changer` when unifying the same persona across multiple ads or stripping music / timbre drift.
- For a multi-ad batch, use a visibly distinct approved persona for every ad unless the user explicitly approves reuse, and show each persona still before generation.
- Use descriptive slugs for approved concepts and finals, not only letters or version counters.
- Before presenter animation or final assembly, show the proposed host/persona still and every proposed B-roll clip individually and obtain explicit user approval. Generating candidate B-roll for review is allowed; using unapproved assets in the ad is not.
- Every newly generated B-roll clip must be uploaded to the appropriate AdMachin B-roll library immediately after it passes QA, with a descriptive title, project/subproject, tags, and complete generation model/prompt metadata. Verify the AdMachin record before treating the clip as a reusable resource; never leave approved generated B-roll local-only.
- Treat blank, empty-looking, or visually indecipherable phone/computer screens as failed B-roll. A screen-based shot must visibly communicate a populated form, record, article, or action at feed-viewing size while keeping personal data fictitious or obscured.
- For Reels eligibility/form B-roll, use true 9:16 mobile viewport captures with feed-readable text. Present each clean, unselected question state as its own short clip; never show cursor taps, selected radio buttons, pressed controls, or the viewer which answers were chosen. Reject desktop-like page framing.
- When cloning a medical/tort swipe, map the source's proof-media cuts and match each insert's function and emotional intensity. If the source uses patients, hospital recovery, scars, or diagnosis imagery, do not substitute generic calendars, folders, or paperwork; prioritize patient-first and diagnosis-first footage, and use PIP when the source keeps the host visible under proof. Treat laptop/article/study screens as secondary corroboration when stronger human diagnosis footage exists.
- Keep every generated video at its native playback speed. Never slow, speed up, time-stretch, duplicate, freeze, or hold frames; repair timing with native-speed trims or a re-generation.
- For image-to-video, the supplied first frame is the sole source of visual identity and scene truth. Video prompts describe action, voice, dialogue, camera behavior, and intentional changes only; never restate the person's appearance, medical details, wardrobe, or the scene's visual details. Compare the anchor with every clip's start, midpoint, and end, plus quarter-points for clips 8 seconds or longer. Any material person or scene drift is an automatic rejection: reroll the affected clip from the approved anchor and repeat QA before stitching, captioning, or delivery.
- In podcast/interview audio, keep natural `mm-hmm` / `yeah` reactions only between complete thoughts. If one splits diagnosis, eligibility, compensation, disclaimer, or CTA wording, reroll or remove it at native speed using Scribe timings under approved B-roll.
- When using ffmpeg `alimiter` after static loudness gain, set `level=disabled`; default auto makeup can undo the LUFS target. Re-measure integrated LUFS and true peak on the rendered final.
- Before captioning, route through the existing named caption skills: `hormozi3`, `nick-subtitle`, `yellow-text-sub`, or `redwood-subtitle`. Use `embedded-captions` for cinematic/VFX treatments and `caption-engine-builder` only when cloning a genuinely new style. Do not modify a generic renderer before checking this catalog.
- Frame-quantize B-roll edits. Adjacent B-roll shots must share one exact frame boundary; otherwise leave a deliberate host run, never a one- or two-frame host flash. Before delivery, run `dissect.py --every-frame` and `scripts/framewise_video_qa.py`, inspect every transition before/at/after, and reject isolated flashes, black frames, frozen runs, or visual runs shorter than 12 frames. Keep dense mobile form screens unobstructed; stop captions for that sequence when no safe caption position exists.
- Sensitive legal copy: say `sexual abuse` explicitly when needed, use `may qualify` plus `significant potential compensation`, and keep the Pulaski/Jones disclaimer verbatim.
