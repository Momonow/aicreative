# Session digest — 2026-07-12 (women's-prison interview series: build → QA → launch)

High-signal record of the mistakes made this session and where each is now prevented, so a
parallel/future session doesn't repeat them. Everything below is committed; the auto-surfacing
lives in the named skills + CLAUDE.md.

## Video production / QA (skills: `street-interview-production`, `veo-interview-qa`, `proper-noun-pronunciation`)

1. **Eyeline broke** — both interviewer + interviewee faced the SAME screen direction ("her left"
   wording is unreliable). Fix: interviewer looks SCREEN-RIGHT, survivor SCREEN-LEFT; bake the
   direction into the ANCHOR (i2i) and eyeball-verify (tile side by side) BEFORE generating clips.
   Wrong-facing anchor ⇒ every clip regenerates. (~1.5h lost.)
2. **Male / two-voice audio** slipped through a visual-only review — Veo dropped a male voice into
   underfilled female clips. Fix: `veo_clip_qa.py` F0 male-fraction (<160 Hz, >22% ⇒ reject) +
   bimodal two-voice check + **adaptive clip duration** (match seconds to line length) so there's no
   void to fill. Measure the FRACTION below 160 Hz, never the median.
3. **Verifier false-rejects burned ~9 rerolls** — raw transcript matching split `didn't`→`didn`+`t`
   and choked on Scribe garbling the first word. Fix: canonicalize both sides (strip apostrophes,
   fold numbers eleven↔11), tightest-span subsequence with garbled-leading tolerance, keep-BEST take
   (never drop a beat). Root-cause the reject reason before re-rolling.
4. **Gaze/angle can't be nudged in-motion** — regenerate the anchor in gpt-image-2 (identity via
   `input_urls`, minimal prompt), don't fight Veo at the video stage.
5. Provider: **useapi FIRST** (flat plan paid) — free Veo Lite via google-flow. Poyo/KIE are
   fallbacks only. Poyo ran out of credits mid-run (402) — the script's provider switch handled it.

## Cloud session presentation (CLAUDE.md)

- Backticked paths DON'T preview in cloud — use **SendUserFile, `display:"render"`, one file per
  call, filename first in the caption**. Always show the preview when presenting a video/idea.

## AdMachin launch — the biggest time sink (skill: `admachin-platform-ops`)

6. **No native adset copy in cloud REST** — no `/copy`/`/duplicate`, no create-from-source field,
   no adset update/delete (all 401/unknown-field). The exact-clone `use_create_from_source` is
   **MCP-server-only (runs on the Mac)**. **DECISION RULE: for a faithful adset duplicate, launch
   from the MCP on the Mac; the cloud REST path can only reconstruct and WILL differ.**
7. **Reconstruction silently changed placements** — dropping the placement block flipped adsets to
   Advantage+ (Audience Network ON, not intended). SET placements explicitly. BUT the cloud create
   endpoint's allowlist is OUTDATED: it rejects `threads`, `biz_disco_feed`, `facebook_reels_overlay`,
   `profile_feed`, `notification`, `explore_home`, `ig_search` — so a cloud reconstruction gets ~11
   of the source's ~19 placements. It CANNOT reproduce "all placements except Audience Network"; only
   the MCP native copy can. (This is why the user's source had 19 placements and the REST rebuild had 11.)
8. **Endpoint quirks** (all in the skill): `daily_budget` is DOLLARS with a $300/day cap (not cents);
   drop bid cap via `LOWEST_COST_WITHOUT_CAP`; omit `attribution_spec` (source's format rejected);
   `adset_params` must NOT include `status`; API gateway intermittently serves the SPA (HTML) on 200
   → retry until JSON; POSTs carry an Idempotency-Key so retries dedup (bump the key version when the
   body legitimately changes, or a 409 fires).
9. **Meta code-6000 "video upload" errors are TRANSIENT** — idempotent retry clears them (hit
   relationship + moved, both launched on retry). Don't treat as a real failure.
10. **Default UTM** must be the full `{{ }}` template appended to `landing_url` (the `/launches`
    endpoint has no url_tags field). Canonical builder: `admachin_utm.default_landing_url()`.

## Compliance / copy (unchanged locks, reaffirmed)

- "significant potential compensation" verbatim; explicit "sexual abuse" beat; real facilities
  (list all four: CCWF Chowchilla / CIW Chino / Valley State / Folsom); free/confidential/no-court;
  Pulaski/Jones verbatim disclaimer in BOTH the burned video AND the FB primary text; present copy
  verbatim for approval BEFORE creating any AdMachin rows.

## Current campaign state (see `wp_interview_series_learnings.md` for IDs)

6 finished ads (one per unique script) staged + launched PAUSED in YJE-23 / WPA - Latina - HJ P1.
Adsets 45/46/47 = corrected (Audience Network off, 11 placements); **42/43/44 = wrong (Advantage+),
delete in Meta UI**. Placement fidelity (all-except-Audience-Network) still pending the user's choice
of MCP-copy vs Meta-UI top-up — do NOT re-attempt via cloud REST.
