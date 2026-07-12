---
name: veo-interview-qa
description: Robust, repeatable production + QA gate for talking-head / street-interview / vox-pop UGC videos generated with Veo (Poyo, KIE, or the free google-flow Lite tier). Runs every clip through one solid checker (transcript, off-screen/improv words, MALE-voice & two-voice detection, proper-noun pronunciation, underfill, burned-in text) before it can enter an assembly, enforces the shot-reverse-shot eyeline, matches clip duration to line length, and structures parallel multi-video runs with provider fallback. Use whenever building or fixing Veo interview/UGC ad videos, or when the user says "make the interview video", "check for two voices / male voice", "off-screen words", "eyeline", "run these in parallel", "why did we get so many errors", or "verify the clips properly".
---

# Veo Interview / UGC — Production + QA Gate

A repeatable pipeline for interview / talking-head Veo videos that **catches the failures that
actually shipped bugs this project** (two voices, off-screen improv words, broken eyeline,
false-reject reroll churn). Every generated clip must pass `scripts/veo_clip_qa.py` before it goes
into an assembly. Reference implementation: `scripts/wp_series2_produce.py` + `wp_series2_finalize.py`.

## The core tool — `scripts/veo_clip_qa.py`

ONE call decides ship / trim / reroll for a clip and says WHY:

```python
from veo_clip_qa import qa_clip
v = qa_clip("clip.mp4", "Spoken line verbatim.", gender="female",
            proper_nouns=["Chowchilla"], ocr=True)
# -> {ok, action, recall, male_frac, extra, coverage, span:(s,e), fails:[...], detail}
# action in {accept, trim, reroll, reroll_shorter}
```
CLI: `.venv/bin/python scripts/veo_clip_qa.py clip.mp4 "the line" --pron Chowchilla --ocr`

### The 7 checks (each cost real debugging time — do NOT drop any)
1. **transcript** — intended line present? Canonicalized, tightest-span subsequence → recall (≥0.85).
   Canonicalizes BOTH sides: strips apostrophes/hyphens *within* tokens (`didn't`→`didnt`, not
   `didn`+`t`) and folds number-words↔digits (`eleven`↔`11`). Tolerates a Scribe-garbled leading
   word (`Shame`→`deshame`). **Skipping this canonicalization false-rejects correct takes and
   burns rerolls — it did, ~9 wasted gens this project.**
2. **improv / off-screen words** — mid-span extra words + total-vs-expected ratio. Catches the
   Veo-invented words heard between/around the scripted line.
3. **voice_gender** — female persona rendered with a MALE voice? Fraction of voiced frames
   `F0 < 160 Hz` (**NOT the median — a male segment medians ~180 Hz and hides**). Reject >22%.
4. **two_voice** — a 2nd speaker slipped in? Bimodal F0 (real low mass ≥15% AND real high mass ≥30%).
5. **pronoun** — required proper nouns present & not mangled (`Chowchilla` ≠ `Chauchilla`).
6. **coverage** — is the clip UNDERFILLED? voiced-time / clip-time; low ⇒ Veo fills the void with
   improv or a second voice ⇒ action becomes `reroll_shorter`.
7. **burned_text** (optional, needs tesseract) — Veo hallucinated on-screen subtitles.

## Production rules (prevent the errors before QA)

- **Match clip DURATION to the line** (~2.4 wps → 4/6/8s). An underfilled clip is the #1 cause of
  off-screen words AND the injected male/second voice. See adaptive-duration in `wp_series2_produce._gen`.
- **Shot-reverse-shot EYELINE (interview):** interviewer looks **screen-right**, interviewee looks
  **screen-left** (opposite → they face each other). Bake direction into the ANCHOR at image-gen
  time (i2i, identity via `input_urls`); "her left/right" wording is unreliable — use SCREEN
  direction. **VERIFY by eye**: tile interviewer + interviewee, confirm noses point at each other,
  BEFORE generating any clip. Fixing an anchor ⇒ every clip from it must be regenerated.
- **Closer / CTA** = survivor looks straight into the lens (regenerate that anchor, don't fight Veo).
- **Provider chain (user-locked 2026-07-12): useapi FIRST, always.** We pay useapi's flat monthly
  plan (~$250-300/mo) — consume it before spending per-clip credits. Veo → `googleflow_client`
  (useapi google-flow, free Veo 3.1 Lite); Seedance/Kling/Runway → `useapi_client` (unlimited).
  Escalate to **Poyo Veo Fast ($0.10/clip) → KIE `veo3_fast` ($0.30)** ONLY on useapi
  compliance/moderation blocks, captcha errors, account/queue problems, or outages — and tell the
  user before switching (credits get spent). `WP_PROVIDER=googleflow|poyo|kie`. Free Lite is
  sloppier ⇒ this QA gate is mandatory, and adaptive duration matters more (Lite loves to fill
  voids with improv/second voices).

## Parallel runs (multi-video)

Structure as phases, not one monolithic per-video loop, so slow generation never blocks fast QA and
a failed beat never silently drops:

1. **PRODUCE** — generate every clip across all videos, skip-if-exists, bounded concurrency:
   Poyo submit ≤ 20/10s (`max_workers=10`); ElevenLabs 5-concurrent shared cap; free Lite queue is
   slow (hours) — persist task state and rely on skip-if-exists across restarts.
2. **QA** — run `qa_clip` on every clip in parallel, **cap 4** (ElevenLabs Scribe limit). Collect
   `action` per clip.
3. **REROLL** — reroll only `reroll`/`reroll_shorter` clips (shorter duration when underfilled),
   re-QA. Loop to MAX (≈3–5). **Keep-BEST take across attempts — never drop a beat to a gap.**
4. **ASSEMBLE** per video — trim each clip to its `span`, concat, `loudnorm`, then captions +
   disclaimer as a separate pass.
5. **FINAL SWEEP** — re-run the voice + eyeline + transcript checks on the ASSEMBLED video (a clip
   can pass solo yet a boundary/loudness issue appears after concat).

Running one `finalize` per video in parallel is fine for a few videos; for large batches prefer the
explicit produce→QA→reroll→assemble phases so QA parallelism isn't gated by the slowest producer.

## Trim & assembly gotchas (each shipped a bug once)

- **Digit-eating trim:** Scribe reformats spoken numbers to digits ("a hundred and three"→"103"); a
  leading-word subsequence match can start AFTER the digit and eat it from the cut. When the first
  intended word is unmatched, back up over leading non-improv words before trimming.
- **Don't over-trim:** ghost tails / silence gaps / repeated phrases between Veo chunks are common —
  but do NOT trim a harmless leading article just to tighten a cut; only reroll when a meaningful
  word is cut or repeated.
- **Watermark crop:** free google-flow / Veo Lite bakes a bottom-right "Veo" watermark. Fix with a
  ratio-preserving center-crop on the ASSEMBLED master (e.g. crop 675:1200 → scale 720:1280,
  uniform axis scale, NEVER stretch), before captions.
- **Never crop a captioned combo** to a new aspect — re-burn captions from the clean master (see
  feed-4x5 skill).

## Visual QA extras (beyond the 7 audio/transcript checks)

- **OCR false-positives:** patterned wardrobe (floral/plaid/knit) false-flags as burned-in text —
  eyeball every OCR flag on a band-sheet before rerolling; don't auto-trust the flag.
- **Phantom motion in "static" shots** (parked car, idle machines): prompt lock alone is
  insufficient — generate 2 takes and auto-pick the one with least frame-diff in the motion region.
  Background-motion QA needs DENSE sampling (fps=6 tile grid over the whole clip), not spot frames.
- **Gesture/finger-count shots:** Veo can start with the wrong finger count; reroll from a seed
  frame with the hand DOWN/out of frame — never reseed from a frame already showing the wrong hand.

## Prompt-shape rules that prevent rerolls (write scripts this way BEFORE generating)

- **No em-dash / trailing colon in any spoken line** — Veo completes the thought with improv or an
  invented name. Closed sentences only (periods/commas).
- **Never join two proper nouns with "and"** — "Chowchilla and Chino" rendered as "Chowchilla in
  Chino" (conflated facilities). Use "or" or restructure the sentence.
- **Pronunciation wins are duration-sensitive** — a respell/lock that passes at 4s can drift at
  10s+. Retest the proper noun at the real clip duration, not just the short test.
- **Rhyme-anchor for stubborn short words** — "qualify" → `KWAH-luh-fy, rhyming with fly`; "Nah" →
  "rhymes with spa". Generalize: anchor the vowel to a common word.

## Do / Do-not

- **DO** run `veo_clip_qa` on every clip before assembly, and again on the finished video.
- **DO** measure male voice by *fraction below 160 Hz*, never the median.
- **DO** verify eyeline on the anchors visually before generating clips.
- **DON'T** reject/reroll on RAW exact-word transcript matching — canonicalize first.
- **DON'T** give a clip more duration than its line fills — that void becomes improv / a 2nd voice.
- **DON'T** drop a failing beat to a gap; keep the best take and reroll for better.
- **DON'T** trust a visual-only review — the male-voice bug is invisible on screen.

## Root-cause table (what happened, so it doesn't again)

| Symptom | Root cause | Fix (now enforced) |
|---|---|---|
| Male / 2nd voice in a clip | Underfilled clip; no voice check | adaptive duration + F0 male-frac + bimodal gate |
| Off-screen / invented words | Underfill; raw trailing-only trim | adaptive duration + tightest-span + improv check |
| Both people face same way | "her left/right" prompt wording | screen-direction in anchor + eyeline eyeball check |
| Many "failures" that were fine | apostrophe tokenizer + Scribe garble | canonicalize both sides + garbled-leading tolerance |
| Run stalled mid-batch | Poyo out of credits | provider fallback chain + skip-if-exists resume |
