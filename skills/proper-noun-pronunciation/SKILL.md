---
name: proper-noun-pronunciation
description: Getting AI-video TTS (Veo/Seedance/Kling/Grok) to pronounce proper nouns and non-English words correctly — the descriptive-lock method, rhyme anchors, phonetic respelling heuristics, and the objective isolated-window Scribe verification that proves a pronunciation without human listening. Use when the user says "pronunciation is wrong", "it's saying Chowchilla wrong", "mispronounced", "how do we make it say X", "verify the pronunciation", or any proper noun / place name / Spanish word sounds off in a generated clip.
---

# Proper-Noun Pronunciation — lock it, then PROVE it

## Method 1 (WINNER for Veo): plain spelling + descriptive lock

A/B-tested on Chowchilla (2026-07): **normal spelling in the dialogue + a descriptive lock beats
hyphenated respellings.** Only add the lock to lines containing the word:

> PRONUNCIATION: 'Chowchilla' = three English syllables chow (rhymes with cow) + chill + uh,
> stress the middle syllable, one fluid word, never Spanish.

- Sentence position matters: **"at Chowchilla"** pronounces reliably; "out of Chowchilla" drifted
  to "Chauchilla". If a construction keeps failing, change the surrounding words.
- **Rhyme-anchor stubborn short words**: "qualify" → `KWAH-luh-fy, rhyming with fly`; "Nah" →
  "rhymes with spa". Anchor the vowel to a common word.
- **Never join two proper nouns with "and"** ("Chowchilla and Chino" → "Chowchilla in Chino").
  Use "or" or restructure.
- Prefer well-known names when legal accuracy matters — Veo mangled "Pere Marquette"→"Pere Martel";
  a wrong facility name in a legal ad is a real problem.

## Method 2 (Seedance & fallback): phonetic respelling heuristics

Hyphenate by syllable (`Chowchilla → Chow-chilluh`), Spanish j→h (`Mija → Mee-hah`), trailing
a→uh, i→ee, ll→y, CAPS for stress (`Chow-CHILL-uh`). **Judge by AUDIO, not by how Scribe spells
the transcript** — "Miha"/"me, huh?" in the transcript can be a CORRECT /ˈmi.xa/.
⚠ **Duration-sensitive:** a respell that passes at 4s can drift at 10s+ ("Chow chilla" →
"chowchillala" at 14s). Retest at the real clip duration.

## Objective verification — the isolated-window unbiased Scribe test

Scribe AUTO-CORRECTS a mispronounced word in context (biased or not), so a full-clip transcript
can't prove pronunciation. Reference: `scripts/wp_verify_chowchilla.py`.

1. Transcribe the full clip **with** `biased_keywords=[word]` → locate the word's start/end.
2. Cut the isolated window: `start − 0.15s` to `end + 0.20s` (ffmpeg).
3. Re-transcribe the isolated audio **UNBIASED** → the true phonetics come out:
   `"chowchill…"` = PASS, `"chauch…"/"chochil…"` = FAIL.
4. Inconclusive window (music/noise)? Fall back to the full unbiased transcript substring check.

Wire the word into the per-clip QA gate (`veo_clip_qa.qa_clip(..., proper_nouns=[word])`) so every
generation is checked automatically; add campaign words to `caption_styled.py:SUBSTITUTIONS` for
the caption layer (e.g. FALSUM→FOLSOM), and pass `--biased-keywords` to every dissect/caption run.

## When to give up

After ~2 lock/respell attempts still failing at the target duration: (a) rewrite the script to
avoid the word, or (b) plan an ElevenLabs dub (`voice_changer` keeps lip-sync; `tts` needs re-sync).
Don't burn more re-rolls.
