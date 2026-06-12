---
name: admachin-video-ads
description: Create, analyze, script, generate, caption, or QA AdMachin UGC video ads, especially AdSwipe transcript analysis, tort/legal lead-gen ads, women's prison/CIW/CCWF sexual-abuse compensation campaigns, Veo/Seedance/Kling clip workflows, persona images, disclaimers, and subtitle choices. Use when the user asks for ad ideas, hooks, scripts, transcript analysis, viral ad analysis, video generation, stitched UGC ads, or captions/disclaimers for sensitive legal ads.
---

# AdMachin Video Ads

Use this skill to avoid re-learning hard-won production lessons from AdMachin ad sessions.

## First Principles

- For AdSwipe, analyze transcript-first. Viral metrics are sparse; do not overfit to the few ads that show them.
- For tort/legal lead-gen, the first 5 seconds must say: who it is for, what happened, and that the person may qualify for significant potential compensation.
- Use legally careful language: "may qualify," "could be eligible," "potential compensation," or "significant potential compensation." Never guarantee money, payouts, settlements, or outcomes.
- Keep UGC copy spoken-simple: short lines, one idea per sentence, no legalese, no over-polished AI voice.
- When the user asks for a specific community voice, capture rhythm and directness without caricature or exaggerated slang.

## Sensitive Legal Caption Rules

For sexual abuse, prison abuse, juvenile detention, medical injury, or other trauma/legal ads:

- Do not use per-word flashing captions, emoji-heavy captions, or loud kinetic subtitle styles.
- Avoid `caption_styled.py` / `yellow-text-sub` unless the user explicitly asks for that exact look after seeing alternatives.
- Prefer calm phrase captions: Nick, simple `caption.py`, or `caption_hormozi3.py --no-emoji`.
- Keep disclaimer readable and calm; it should not compete with the survivor-facing message.
- For regulated legal copy, prefer in-house caption scripts where the wording can be controlled. Real Submagic/API can alter words.

## Tort Script Rules

- Mention facility specificity early when relevant: "CIW Chino and other California women's prisons."
- Avoid "private check"; it can sound like a payment/check. Prefer "private form," "private page," "free case review," or "private questions."
- If Veo/Scribe keeps confusing a spoken word, rewrite around it. Example: if "form" becomes "forum," use "private page" or "answer a few private questions."
- Connect abuse to action clearly: "If staff sexually abused you, you may qualify for significant potential compensation."
- Do not make every concept a testimonial. Rotate formats: direct notice, comment debate, news-style explainer, advocate PSA, checklist, myth-busting, family member, case-worker tone, overheard conversation, "things no one told you."

## Persona Image QA

- Pick animation-safe anchors: medium close-up or chest-up, face visible, mouth unobstructed, hands low or out of frame.
- Avoid hands/fingers close to camera, extreme gestures, blocked mouth, heavy shadows, tight crops, or photos that read too young for adult legal campaigns.
- For sensitive Veo prompts, reduce moderation risk by avoiding compounding visual triggers such as aggressive tattoo descriptors, car settings, or race words paired with sexual-abuse/lawsuit language. Use accurate, neutral visual description.

## Veo / Clip Workflow

- For Veo Lite/free Google Flow, route through `googleflow_client.generate_veo` with `model="veo-3.1-lite-low-priority"` unless the user requests otherwise.
- Verify clip 1 before generating the rest: check face, voice, framing, pronunciation, tone, and legal phrasing.
- Once clip 1 passes, generate clips 2-N in parallel if the user wants speed.
- Use clip-1 anchor rotation for multi-clip talking-head ads. Choose eyes-open, forward-gaze anchor frames.
- Dense 8-second dialogue can cause end-of-clip wobble. Shorten the line rather than trying to hide the transition.
- Check the last 0.5-1.0 seconds of every clip for trailing words, face morphs, ghost tails, and silent drift.

## Stitching And QA

- Clean masters, captioned versions, and disclaimer versions should be separate files.
- After stitching, create a boundary/contact-sheet check around every clip join.
- Default join style is hard jump cut unless the user asks for a transition.
- If a boundary looks like a soft dissolve, suspect the generated clip tail first. Trim or reroll the clip; do not assume ffmpeg caused it.
- Do not burn captions by default. Burn captions only when the user asks for captions/subtitles/disclaimer on the deliverable.

## Session Memory Pattern

When a mistake costs time, money, or quality, write it down in one of these places:

- `CLAUDE.md` for always-on project rules.
- `skills/admachin-video-ads/SKILL.md` for reusable ad-production behavior across sessions.
- `inventory/<campaign>_learnings.md` for campaign-specific language, selected persona, rejected styles, final asset paths, and QA findings.

Keep an explicit "do not repeat" note for rejected outputs, not just approved settings.
