---
name: admachin-platform-ops
description: AdMachin platform API mechanics — upload/verify creatives, compose ads with copy, the ad_type DB-constraint trap, launched-ad immutability, project/subproject filing, and launch gating. Use when the user says "upload to admachin", "stage the ad", "compose ad with copy", "ad_type error", "the upload didn't show up", "edit a launched ad", "move the creative", or any AdMachin API/staging/launch operation. Distinct from admachin-video-ads (creative/compliance rules) — this is the platform plumbing.
---

# AdMachin Platform Ops — API mechanics that recur every campaign

These traps have each recurred across ≥3 campaigns. Full API contract details in CLAUDE.md
("Publishing to AdMachin"); this skill is the operational checklist.

## Upload → verify (never trust the upload response)

- `upload_creative` can return a success record for a file that **doesn't actually persist** —
  ALWAYS verify via `list_creatives` (filter by project) before building ads on the id.
- Pass `project_id` on upload or the creative lands in the default (null) project. Mis-filed?
  `update_creative_metadata` MOVES it (re-tag, no re-upload).
- To hide a creative, MOVE it to a null project — soft-delete via `status:"deleted"` fails a DB
  check constraint.
- Tort project `e15c60bd-…`; Women's Prison subproject `acf1b974-…`, IL JDC `7f876467-…`.
  Resolve names → UUIDs via `list_projects(search=)` / `list_subprojects`.

## Compose (ads + copy)

- **`ad_type` is NOT free-text** — DB check constraint `ads_ad_type_allowed`; a custom label 500s
  `create_ad`/`compose_ad_with_copy` AFTER the creative+copy rows already succeeded. **OMIT
  `ad_type`** (or copy a known-allowed value from an existing ad). Keep a resumable state file so
  the retry only re-runs the ad row.
- **One writer per JSON state file** — two staging scripts sharing one state file clobber each
  other (read-modify-write race).
- **Copy approval gate (user-locked):** present every headline + primary text VERBATIM in chat and
  get explicit approval BEFORE creating copy rows or assembling ads. A template walkthrough is not
  approval.

## Launch & post-launch

- **Launched ads are IMMUTABLE.** Wrong copy on a live ad → CREATE ONE MORE ad (new draft), never
  edit the live one.
- **Launch is gated, never default** — `scripts/admachin_push.py --launch` + typed `LAUNCH`
  confirmation (or `--yes` for automation). No TTY + no `--yes` = refuse. Launch SPENDS REAL MONEY.
- Ads have NO link field — `landing_url` is supplied at launch time.

## Environment gotchas

- **macOS has no `timeout` command** — wrapping a batch in `timeout 300 …` silently aborts it (an
  entire 20-image batch once never generated). Use a Python-level timeout or plain background runs.
- ElevenLabs voice slots: 30 cap on Creator — do NOT delete voices to free slots without explicit
  user approval.
