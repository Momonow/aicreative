# External caption APIs — Submagic & OpusClip

Two third-party APIs that caption a finished video. **Both AUTO-TRANSCRIBE** (cannot ingest our exact
script/SRT) and **NEITHER burns the legal disclaimer** → always finish with our `burn_disclaimer.py`
combo pass. Keys live in `.env` (gitignored, treat as secrets): `SUBMAGIC_API_KEY`, `OPUSCLIP_API_KEY`.

Both support **direct local-file upload** — no public-host hack needed.

---

## Submagic — `scripts/submagic_client.py`

- Base `https://api.submagic.co/v1`, auth header **`x-api-key: sk-...`**.
- **Flow (3 calls):**
  1. `POST /v1/projects/upload` (multipart/form-data): `file`, `title`, `language` (`"en"`), `templateName`,
     `dictionary` (JSON-array string), `magicZooms`/`magicBrolls` (**string** `"true"`/`"false"`, default off).
     Returns `{id, status:"uploading"}`. (URL variant: `POST /v1/projects` with `videoUrl`.)
  2. `POST /v1/projects/{id}/export` (optional `width`/`height`/`fps`) — renders. **Export is a SEPARATE
     step and 400s if called before transcription finishes** (`"Project is not ready for export. Current
     status: uploading"`). Retry until 200. The client retries each poll cycle.
  3. `GET /v1/projects/{id}` — poll `status`: `uploading→processing→transcribing→exporting→completed|failed`.
     On `completed` → **`downloadUrl`** (also `directUrl`, `previewUrl`). ~60–190s end-to-end.
- **Templates** (`GET /v1/templates`, ~45): `Hormozi 1`–`Hormozi 5` (**Hormozi 3 = the authentic version of
  our in-house `caption_hormozi3.py` look**), **`Lewis`** (clean sentence-case white + green active-word
  highlight, emoji — used for the Chowchilla final set), `Beast`, `Ali`, `Iman`, `Karl`, `Ella`, etc.
  Default `"Sara"`.
- **Keeps native resolution** (720×1280 preserved — no upscaling).
- **`dictionary`** biases transcription for proper nouns (JSON-array string, ≤100 items / ≤50 chars each).
  Chowchilla: `["Chowchilla","CCWF","CIW"]` — verified it fixes "CHOWCHILLA" spelling.
- **`magicZooms`/`magicBrolls` OFF** for the locked-cam podcast aesthetic (they add zoom/B-roll motion we
  don't want on a static podcast shot).
- **NO verbatim-text control** — auto-transcribes; reformats ("a hundred dollars" → "$100"), and can split a
  card across a sentence boundary ("was Don't"). Only levers: `dictionary`, `disableCaptions`.
- **NO caption layer / SRT / transcript export** — output is a single flat burned MP4. Export has no
  alpha/format/codec option; there is no transcript/words endpoint anywhere in the API.
- **Caption position is NOT a request param** — set it via `templateName` (fixed) OR a custom
  `userThemeId` / `presetId` created in the Submagic app (open project → edit theme/preset → copy ID).
  Only `hookTitle.top` (0–80) positions the HOOK title, not the running subtitles.
- **Credits** ≈ 1 per minute of source (sub-minute rounds to 1).

---

## OpusClip — `scripts/opusclip_client.py`

- Base `https://api.opus.pro/api`, auth **`Authorization: Bearer <key>`**.
- **Local-file flow:**
  1. `POST /api/upload-links` `{"video":{"usecase":"LocalUpload"}}` → `{url, uploadId}`.
  2. `POST <url>` headers `x-goog-resumable: start`, `Content-Length: 0` → `Location` header (GCS session).
  3. `PUT <Location>` `Content-Type: application/octet-stream` + raw bytes.
  4. `POST /api/clip-projects` `{videoUrl:<uploadId>, curationPref:{skipCurate:true}, renderPref:{layoutAspectRatio:"portrait"}, brandTemplateId}` → `{id, stage:"QUEUED"}`.
  - Retrieve: `GET /api/exportable-clips?projectId=X` → `{data:[{uriForExport, uriForPreview, ...}]}`;
    project stage via `GET /api/clip-projects/{id}` (`stage`: QUEUED→…→COMPLETE).
- **`curationPref.skipCurate:true`** = caption-only (skips the long-video clipping pass; renders the whole clip).
- **Templates:** `GET /api/brand-templates?q=mine` → account templates (use the `templateId`, e.g.
  `cmf28xj4c0j5shz80s1hyjea0`). Built-in presets `preset-fancy-*` (`Mozi`=Hormozi, `Karaoke`, `Beast`,
  `Pod_P`, `Simple`, `Think_Media`, …) usable by ID. This account's saved presets: **`preset-1`**
  (Montserrat, green→yellow, `cmf28xj4c0j5shz80s1hyjea0`), **`preset-2`** (Komika-Axis, pink→purple,
  `cmf28xj4d0j5thz80dfp780em`).
- **Upscales output to 1080×1920** (re-renders; ~2× bigger files than Submagic/in-house).
- **Billing:** 1 credit = 1 minute of **source** video. **Under 1 min rounds UP to 1**; 1–2 min rounds DOWN
  to 1. NOT per-call, NO 10-credit minimum. ~$0.08–0.10/credit. No usage/balance endpoint (all 404 —
  check the dashboard).
- **`enableRemoveFillerWords` would strip podcast "mm-hmm" reactions** — leave OFF (we keep those).
- Same limits as Submagic: **no verbatim control, no disclaimer, position only via the brand template.**

---

## Cross-cutting (applies to both)

- **Neither burns the disclaimer.** Combo = engine captions → `scripts/burn_disclaimer.py` on the
  captioned output. (Chowchilla set: `<L>_full_submagic_lewis.mp4` → `<L>_full_submagic_lewis_disclaimer.mp4`.)
- **Neither guarantees verbatim text** (both auto-transcribe). For regulated/legal copy where exact wording
  matters, prefer the **in-house** `caption_hormozi3.py` (we hold the script) and spot-check API outputs.
- **Async + slow** (~1–3 min/clip): run batches as tracked background jobs; never kill mid-flight.
- **Naming:** `<name>_submagic_<template>.mp4`, `<name>_opusclip.mp4`, append `_disclaimer` after the
  disclaimer pass. Collect finals into a delivery folder (e.g. `final_lewis_disclaimer/`).
