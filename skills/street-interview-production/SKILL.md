---
name: street-interview-production
description: End-to-end recipe for street-interview / vox-pop / shot-reverse-shot UGC ad videos — persona anchors, eyeline (gaze left/right), matched props (podcast mic), into-lens CTA closer, dialogue+audio prompt locks, adaptive clip duration, solo-clip-per-turn topology, and assembly. Use when the user says "street interview", "vox pop", "interview ad", "shot reverse shot", "person interviewing", "podcast mic interview", "two people talking ad", or wants any back-and-forth conversation video built with Veo/Grok/Kling. Pairs with the veo-interview-qa skill for verification.
---

# Street-Interview / Shot-Reverse-Shot Production

The battle-tested recipe from the women's-prison campaign (Nice One + It-Was-Never-Consent series,
2026-07). Reference implementations: `scripts/wp_series2_produce.py` (produce),
`wp_series2_finalize.py` (assemble), `wp_series2_personas.py` / `wp_series2_camlock.py` /
`wp_series2_eyeline_fix.py` (anchors). **Verification is the sibling skill `veo-interview-qa`
(`scripts/veo_clip_qa.py`) — always run it; do not re-invent checks.**

## Topology: SOLO clip per turn (not two-shots)

Veo cannot reliably decide who speaks in a two-shot, and two voices in ONE clip collapse to the
same voice (ΔF0 ≈ 1.4 Hz measured). **Generate each dialogue turn as its own SOLO clip** from a
per-person anchor, then cut alternating. A wide two-shot + punch-in crop (`wp_voxpop_reframe.py`)
is the legacy alternative — keep for archival, don't default to it.

## Anchors (all gpt-image-2 via KIE, 2K, 9:16)

1. **Personas t2i** — explicit per-persona anthropometry (age, build, face shape, skin tone/texture,
   hair, marks, jewelry) or gpt-image-2 mode-collapses repeated demographics to one face. Append the
   documentary-realism tail (visible pores, no makeup/retouching/filter, NOT glamour/celebrity).
2. **Bake the prop into the prompt** so it matches across all anchors: e.g. the small podcast mic =
   *"short black cylindrical handle, round black foam windscreen ball on top, a tiny blue LED on the
   handle"*. If two anchors come back with different mics, i2i-swap using a canonical mic reference
   image (`outputs/wp_interview2/reference/mic_ref.png` pattern).
3. **EYELINE (the 180° rule)** — interviewer = LEFT person → looks **SCREEN-RIGHT**; interviewee =
   RIGHT person → looks **SCREEN-LEFT**. They must be opposite or the cut reads as two monologues.
   **"her left / his right" wording is UNRELIABLE** — always say *"turned toward the LEFT edge of
   the frame, looking off-camera to the LEFT (screen-left)"*. **VERIFY BY EYE before generating any
   clips**: tile the anchors side by side (`ffmpeg hstack`) and confirm the noses point at each
   other. A wrong-facing anchor ⇒ every clip from it must be regenerated (~1.5h lost when skipped).
4. **Into-lens CTA closer** — a separate anchor where the interviewee holds the mic herself, squared
   to camera, *"BOTH eyes locked DIRECTLY on the camera lens, looking right down the barrel"*.
   Gaze/angle is baked into the anchor — Veo can't swing an off-axis gaze onto the lens; regenerate
   the image, don't fight the video prompt.
5. **All pose/gaze changes = i2i with `input_urls`** (identity held) + a MINIMAL prompt describing
   ONLY the change ("this exact same woman, same face/hair/clothing/background; change ONLY her
   orientation…"). Describing the person drifts identity. `input_fidelity="high"`. Back up the old
   anchor before overwriting (`<name>_rightgaze.png` pattern).

## Per-clip generation prompt (i2v, keep SHORT)

Structure per turn (see `prompt_for()` in wp_series2_produce.py):
- WHO+GAZE line matched to the anchor: interviewer *"speaks to the person off to the RIGHT side of
  the frame … gaze off-camera to the RIGHT (screen-right)"*; interviewee mirror-left; closer
  *"STRAIGHT INTO the camera lens"*.
- **PACE**: `~2.4 words per second.`
- **AUDIO CRITICAL**: *"clear full conversational volume, clean, NO music."*
- **PRONUNCIATION lock** only on lines containing the proper noun (see below).
- **DIALOGUE LOCK**: *"English only, no filler, no 'um/uh', no extra or trailing words, stop after
  the final word. SPOKEN DIALOGUE (verbatim): "…". No on-screen text, no captions."*
- Write every line as **closed sentences** — no trailing em-dash/colon (Veo completes the thought
  with improv/invented names).

## Duration = f(line length) — the #1 error preventer

An underfilled clip is where Veo invents off-screen words and injects a male/second voice.
**Match duration to the line at ~2.4 wps** and round to the provider's allowed buckets
(google-flow: 4/6/8s → `est=nwords/2.4; 4 if est<=4 else 6 if est<=6.2 else 8`). Never leave >2s
of unscripted room.

## Pronunciation (e.g. Chowchilla)

Winning combo (A/B tested): **plain spelling in the dialogue + descriptive lock** —
*"'Chowchilla' = three English syllables chow (rhymes with cow) + chill + uh, stress the middle
syllable, one fluid word, never Spanish."* Hyphenated respellings LOST to this.
Verify objectively (`scripts/wp_verify_chowchilla.py` pattern): biased pass to locate the word,
then re-transcribe the ISOLATED window (start−0.15s, end+0.20s) UNBIASED — Scribe auto-corrects a
mispronunciation in context, the isolated pass reveals true phonetics ("chow…" pass, "chau…" fail).

## Providers (user-locked 2026-07-12)

**useapi FIRST, always** (flat plan already paid): Veo → `googleflow_client` (free Veo 3.1 Lite);
Seedance/Kling/Runway → `useapi_client`. Poyo Veo Fast ($0.10/clip) → KIE ($0.30) are FALLBACKS for
useapi compliance blocks / captcha / account problems / outages only — announce in chat before
switching (spends credits). `WP_PROVIDER=googleflow|poyo|kie` env switch; `_gen()` dispatcher
normalizes call shapes (Poyo/KIE: `image_urls=[url,url]` frame mode; google-flow: local
`image_path`, `aspect_ratio="portrait"`, integer duration).

## QA + assembly

- **Every clip through `veo_clip_qa.qa_clip()`** (transcript recall ≥0.85 canonicalized, improv,
  male-voice frac <22%, two-voice bimodal, pronunciation, coverage/underfill, burned-text OCR).
  Keep-BEST take across ≤3 attempts (`_take{idx}.mp4`), never drop a beat; `reroll_shorter` when
  underfilled. Cap Scribe-using QA at 4 parallel (ElevenLabs 5-concurrent).
- **Trim to the intended-line span** from Scribe word-timings (subsequence span ±0.05/+0.25s) — NOT
  silencedetect (street ambience defeats it) and NOT full-clip (keeps other-speaker bleed).
- Per-piece normalize: `scale=720:1280,setsar=1,fps=30`, then concat + `loudnorm=I=-16:TP=-1.5:LRA=11`,
  master crf=20 + web copy crf=26.
- Captions (`caption_nick.py` for legal/sensitive) + `burn_disclaimer.py` AFTER QA-gated assembly,
  never before. Then a **final sweep** on the assembled video (voice + transcript + eyeline).

## Order of operations (checklist)

1. Personas t2i (distinct anthropometry) → user picks
2. Prop-match check (mic) → i2i swap if needed
3. Eyeline anchors: interviewer→right, interviewee→left, closer→lens; **tile + eyeball verify**
4. Scripts: closed sentences, per-turn word counts sized to duration buckets, compliance wording
5. Produce solo clips (useapi first, skip-if-exists, bounded concurrency)
6. QA every clip (veo-interview-qa) → reroll/reroll_shorter, keep-best
7. Trim → concat → loudnorm → captions+disclaimer → final sweep
8. Backtick every produced file path in chat immediately
