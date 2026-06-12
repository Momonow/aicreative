# IL JDC Campaign Learnings

Durable notes for Tort / IL JDC legal lead-gen work.

## AdMachin State

- Project: `Tort` (`e15c60bd-95c2-47b9-9730-c29fb5325461`).
- Subproject: `IL JDC` (`7f876467-8262-4647-91b1-d56574976079`).
- Recent storytime creative rows uploaded under IL JDC include `#627`-`#633`.
- Recent tort testimonial creative rows include `#641`-`#649`.
- Final ad rows from the storytime batch include `#337`-`#343`; later tort rows
  include `#348`-`#356`.

## Wording Rules

- For IL JDC, the user allowed `significant compensation` without `potential`.
- Still keep recovery language cautious: `may qualify`, `might qualify`, or
  `may qualify for significant compensation`. Do not promise outcome.
- Explicitly say `juvenile detention center` or `juvenile center` early enough
  when prison confusion is possible.
- The qualifying harm must be `sexual abuse` / `sexually abused`; do not let
  generic `abuse` carry the legal topic by itself.
- CTA should push the form: tap below, name and phone number, about 30 seconds.
  The `part 2` device is optional but should not replace the form CTA.

## Clip And Prompt Lessons

- Do not slow clips down or add frozen-frame pads to make cut-off speech feel
  smoother unless the user explicitly approves. The user prefers rerolls or
  original-speed word-aware trims.
- If the first word is cut off or unclear, reroll the clip with clearer pacing
  rather than stretching playback.
- `qualify` can render as `qualifee`; use pronunciation guidance like
  `KWAH-luh-fy, rhyming with fly`.
- For counting/finger list prompts, Veo may start with the wrong number of
  fingers even if instructed. If a "two fingers" shot starts with three fingers,
  reroll from a seed frame where the hand is down/out of frame, or avoid the
  gesture. Do not seed from a frame already showing the wrong hand shape.
- For #6/peer style scripts, mention `Cook County juvenile detention center`
  explicitly so viewers do not confuse it with adult prison.

## Subtitle Lessons

- For sensitive direct-to-camera IL JDC UGC, use in-house captions when exact
  wording matters. Submagic can alter legal wording (`SA'ed` risked bad STT).
- Hormozi 3 Submagic-match captions are available for creator-style videos, but
  avoid flashy per-word styles by default on trauma/legal ads unless requested.

## Podcast / Winner-Style Learnings

- Confession-podcast reads should feel like one person talking to someone else
  in the room: off-camera gaze, conversational rhythm, natural room-response.
- Winner/announcer reads should be direct-to-lens. Do not put a hype
  direct-response script on an off-camera confession visual.
- `mm-hmm` / `yeah` reactions are acceptable in podcast format. Keep them in
  audio if they feel natural, but do not caption them.
- `Ayo` renders badly in Veo. Prefer one clean opener such as `Yo, Illinois.
  Listen up.` or `Listen up, Illinois.`
- Use well-known Illinois facilities or phonetic guidance. Obscure names can
  mangle (`Pere Marquette` came back wrong).
- If every clip uses the same approved persona anchor, keep raw Veo audio by
  default. Use voice changer only when it solves actual cross-clip drift or
  multi-video host consistency.
- If headphones or a mic suddenly appear, inspect the prompt first. In this
  batch the recurring prop problem came from the prompt, not the source image.

### Winner/Announcer Track — Shipped Decisions (2026-06-12)

- 3 announcer videos shipped: `jdc_pod_winnerA_h11`, `jdc_pod_winnerB_h15`,
  `jdc_pod_winnerC_h14` (hosts real_11 / real_15 / real_14 from
  `scripts/jdc_podcast_real2.py`; user wanted Black hosts only for this track,
  no headphones, direct-to-lens announcer gaze).
- Pipeline order: `jdc_podcast_real2.py` (2K personas) →
  `scripts/jdc_pod_upscale_4k.py` (Real-ESRGAN 4K BEFORE any video work — user
  flagged the 2K refs as too low-res to build on) →
  `scripts/jdc_pod_winner_gen.py` (KIE veo3_lite; clip1 from the 4K image,
  clips 2-5 from rotated eyes-open anchors) → `scripts/jdc_pod_clone.py` (one
  clone per host) → `scripts/jdc_pod_finalize.py`.
- AUDIO (user-locked for this track): ship the voice-changer chain as-is —
  `eleven_english_sts_v2`, `use_speaker_boost` ON, master at -16 LUFS, NO
  further post volume changes. A raw-Veo A/B was offered; the user explicitly
  chose to stay on VC at -16 here, even though raw Veo remains the default for
  single-persona confession videos.
- Final openers after the `Ayo` failures: A = "Listen up, Illinois." ·
  B = "Yo, Illinois. Listen up." · C = "Yo, Illinois, listen."
- One-syllable slang fix: "Nah" rendered as "LA" — fixed with a rhyme anchor in
  the TONE line: `Say 'Nah' as a clear, open 'NAH' (rhymes with 'spa')`. Reuse
  the rhyme-anchor trick whenever a short slang word mangles.
- Delivery format: user wants **9:16 only** in the final delivery folder
  (`outputs/jdc_podcast_delivery/`); do not add 4:5 variants unless asked.
