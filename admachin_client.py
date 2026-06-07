"""AdMachin client — upload creatives, assemble ads, launch to Facebook.

REST v1:  https://admachin.com/api/v1
Auth:     Authorization: Bearer admachin_pat_...   (ADMACHIN_PAT in .env)
Docs:     https://admachin.com/docs/api   |   OpenAPI: /api/v1/openapi.json

Pipeline (see scripts/admachin_push.py for the orchestration):
    upload_creative(mp4)  ->  create_ad_copy x3  ->  create_ad / generate_combos
                          ->  launch_ad(...)        # ⚠ SPENDS REAL MONEY on Facebook

Notes baked in from the API contract:
  * Only POST /creatives is multipart; everything else is JSON.
  * Supported MIME: jpeg/png/webp/gif/mp4/quicktime. Max 200 MiB.
  * Ads have NO link field — the destination URL is passed at LAUNCH time as
    `landing_url`. `/links` is a separate tracking-link library (POST /links,
    needs name+url) that is NOT auto-attached to an ad. There is no
    /links/find-or-create endpoint despite what the recipe page implies.
  * No /projects or /me endpoint yet — find project_ids via the web UI or
    list_ad_plans(). PAT scopes can't be introspected up front; a missing
    scope surfaces as FORBIDDEN at call time (we annotate it).
  * Every POST/PATCH sends an Idempotency-Key (uuid4 by default). The server
    caches (token_id, key) for 24h, so passing a STABLE key makes a retry
    safe — important for launch_ad to avoid a double-spend on re-run.
"""
import os
import uuid
import pathlib

import requests
from dotenv import load_dotenv

load_dotenv()
PAT = os.getenv("ADMACHIN_PAT")
if not PAT:
    raise RuntimeError("ADMACHIN_PAT not set in .env")

BASE = os.getenv("ADMACHIN_API_BASE", "https://admachin.com").rstrip("/") + "/api/v1"

MAX_BYTES = 200 * 1024 * 1024
_MIME = {
    ".mp4": "video/mp4", ".mov": "video/quicktime",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".webp": "image/webp", ".gif": "image/gif",
}


class AdMachinError(RuntimeError):
    """Carries AdMachin's error envelope {error:{code,message,request_id}}.

    `.code` is one of UNAUTHENTICATED|FORBIDDEN|NOT_FOUND|CONFLICT|VALIDATION|
    RATE_LIMIT|INTERNAL (or HTTP_<status> if the body wasn't an envelope), so
    callers can branch — e.g. FORBIDDEN means the PAT lacks the needed scope.
    """

    def __init__(self, code, message, request_id=None, status=None):
        self.code = code
        self.message = message
        self.request_id = request_id
        self.status = status
        tail = f" (request_id={request_id})" if request_id else ""
        super().__init__(f"[{code}] {message}{tail}")


def _auth(extra=None):
    h = {"Authorization": f"Bearer {PAT}"}
    if extra:
        h.update(extra)
    return h


def _check(r):
    """Parse a response; raise AdMachinError on an error envelope / non-2xx."""
    try:
        body = r.json() if r.content else {}
    except ValueError:
        body = {}
    is_envelope = isinstance(body, dict) and isinstance(body.get("error"), dict) and "code" in body["error"]
    if r.status_code >= 400 or is_envelope:
        err = body.get("error", {}) if isinstance(body, dict) else {}
        code = err.get("code") or f"HTTP_{r.status_code}"
        msg = err.get("message") or (r.text[:300] if r.text else r.reason)
        if code == "FORBIDDEN":
            msg += " — your PAT is missing the scope required for this call."
        elif code == "UNAUTHENTICATED":
            msg += " — ADMACHIN_PAT is invalid or malformed."
        raise AdMachinError(code, msg, err.get("request_id"), r.status_code)
    return body


def _post(path, json=None, idem_key=None, timeout=120):
    h = _auth({"Content-Type": "application/json"} if json is not None else None)
    h["Idempotency-Key"] = idem_key or str(uuid.uuid4())
    return _check(requests.post(f"{BASE}{path}", headers=h, json=json, timeout=timeout))


def _patch(path, json=None, idem_key=None, timeout=60):
    h = _auth({"Content-Type": "application/json"})
    h["Idempotency-Key"] = idem_key or str(uuid.uuid4())
    return _check(requests.patch(f"{BASE}{path}", headers=h, json=json, timeout=timeout))


def _get(path, params=None, timeout=60):
    return _check(requests.get(f"{BASE}{path}", headers=_auth(), params=params, timeout=timeout))


# --------------------------------------------------------------------------
# Read helpers (no scope beyond read:*; safe to call freely)
# --------------------------------------------------------------------------
def list_workspaces():
    return _get("/workspaces")


def list_ad_plans(project_id=None):
    return _get("/ad-plans", params={"project_id": project_id} if project_id else None)


def list_creatives(limit=20, project_id=None):
    params = {"limit": limit}
    if project_id:
        params["project_id"] = project_id
    return _get("/creatives", params=params)


def get_creative(creative_id):
    return _get(f"/creatives/{creative_id}")


def get_ad(ad_id):
    return _get(f"/ads/{ad_id}")


def get_launch(launch_id):
    return _get(f"/launches/{launch_id}")


# --------------------------------------------------------------------------
# Upload — POST /creatives (multipart). Requires write:creative.
# --------------------------------------------------------------------------
def upload_creative(path, type=None, project_id=None, subproject_id=None,
                    rating=None, idem_key=None, timeout=600):
    """Upload a local image/video as a creative. ≤200 MiB.

    `type` defaults to 'video' for .mp4/.mov, else 'image'. Returns the
    creative dict {id, storage_path, thumbnail_path, ...}.
    """
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(path)
    size = p.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(f"{p.name} is {size / 1048576:.1f} MiB > 200 MiB cap")
    mime = _MIME.get(p.suffix.lower())
    if not mime:
        raise ValueError(f"Unsupported file type {p.suffix!r}; allowed: {sorted(_MIME)}")
    if type is None:
        type = "video" if mime.startswith("video") else "image"

    data = {"type": type}
    if project_id:
        data["project_id"] = project_id
    if subproject_id:
        data["subproject_id"] = subproject_id
    if rating is not None:
        data["rating"] = str(rating)

    h = _auth()
    h["Idempotency-Key"] = idem_key or str(uuid.uuid4())
    with open(p, "rb") as f:
        files = {"file": (p.name, f, mime)}
        r = requests.post(f"{BASE}/creatives", headers=h, files=files, data=data, timeout=timeout)
    return _check(r)


# --------------------------------------------------------------------------
# Copy — POST /ad-copies. Requires write:copy.
# --------------------------------------------------------------------------
def create_ad_copy(text, type, project_id=None, subproject_id=None, name=None, **kw):
    """`type` ∈ {'headline','primary_text','description'}."""
    if type not in ("headline", "primary_text", "description"):
        raise ValueError("type must be one of: headline, primary_text, description")
    body = {"text": text, "type": type}
    for k, v in (("project_id", project_id), ("subproject_id", subproject_id), ("name", name)):
        if v is not None:
            body[k] = v
    body.update(kw)
    return _post("/ad-copies", json=body)


# --------------------------------------------------------------------------
# Assemble — POST /ads (single) / POST /ads/generate-combos (cartesian).
# Requires write:assembly.
# --------------------------------------------------------------------------
def create_ad(creative_id, headline_id=None, primary_id=None, description_id=None,
              ad_type=None, traffic=None, project_id=None, subproject_id=None, **kw):
    """Assemble ONE ad pairing a creative with up to three copy ids."""
    body = {"creative_id": creative_id}
    for k, v in (("headline_id", headline_id), ("primary_id", primary_id),
                 ("description_id", description_id), ("ad_type", ad_type),
                 ("traffic", traffic), ("project_id", project_id),
                 ("subproject_id", subproject_id)):
        if v is not None:
            body[k] = v
    body.update(kw)
    return _post("/ads", json=body)


def generate_combos(creative_ids, headline_ids=None, primary_text_ids=None,
                    description_ids=None, ad_type=None, project_id=None, **kw):
    """Bulk-generate the cartesian product of creatives × copies. Returns rows."""
    body = {"creative_ids": list(creative_ids)}
    for k, v in (("headline_ids", headline_ids), ("primary_text_ids", primary_text_ids),
                 ("description_ids", description_ids), ("ad_type", ad_type),
                 ("project_id", project_id)):
        if v is not None:
            body[k] = list(v) if isinstance(v, (list, tuple)) else v
    body.update(kw)
    return _post("/ads/generate-combos", json=body)


# --------------------------------------------------------------------------
# Tracking link — POST /links. Requires write:links. NOT auto-attached to an
# ad (see module docstring); kept for completeness / the link library.
# --------------------------------------------------------------------------
def create_link(name, url, project_id=None, subproject_id=None, **kw):
    body = {"name": name, "url": url}
    for k, v in (("project_id", project_id), ("subproject_id", subproject_id)):
        if v is not None:
            body[k] = v
    body.update(kw)
    return _post("/links", json=body)


# --------------------------------------------------------------------------
# Launch — POST /launches.  ⚠ SPENDS REAL MONEY. Requires launch:meta.
# --------------------------------------------------------------------------
def launch_ad(ad_id, ad_account_id, campaign_id, adset_id, page_id, cta_type, landing_url,
              connection_id=None, pixel_id=None, event_type=None, idem_key=None, timeout=180):
    """⚠ Launch an assembled ad LIVE on Facebook. SPENDS REAL MONEY.

    The campaign + ad set + page must already exist on the ad account. Pass a
    STABLE `idem_key` (e.g. f"launch-{ad_id}") so a retry within 24h is deduped
    by the server instead of creating a second live ad. Returns LaunchedAd
    {id, fb_ad_id, fb_campaign_name, ...}.
    """
    body = {
        "ad_id": ad_id,
        "ad_account_id": ad_account_id,
        "campaign_id": campaign_id,
        "adset_id": adset_id,
        "page_id": page_id,
        "cta_type": cta_type,
        "landing_url": landing_url,
    }
    for k, v in (("connection_id", connection_id), ("pixel_id", pixel_id), ("event_type", event_type)):
        if v is not None:
            body[k] = v
    return _post("/launches", json=body, idem_key=idem_key or f"launch-{ad_id}", timeout=timeout)


def pause_launch(launch_id):
    """Pause a live ad on Facebook (stops spend)."""
    return _post(f"/launches/{launch_id}/pause")


def resume_launch(launch_id):
    """Resume a paused ad. ⚠ RE-STARTS SPEND."""
    return _post(f"/launches/{launch_id}/resume")
