#!/usr/bin/env python3
"""Push a finished video into AdMachin: upload -> assemble -> (gated) launch.

    .venv/bin/python scripts/admachin_push.py <video.mp4> [options]

Default run (NO spend): uploads the file as a creative, creates whatever copy
you pass, assembles ONE draft ad, and prints the ad id. It stops there.

Launching to Facebook (⚠ SPENDS REAL MONEY) is gated behind --launch AND a
confirmation: in a terminal you must type LAUNCH; for automation pass --yes.
Without a TTY and without --yes the launch is refused (never silently spends).

Targeting (project + the Facebook ids needed to launch) can live in a
per-campaign JSON under admachin_targets/<name>.json and be selected with
--campaign <name>; any CLI flag overrides the file. Print a starter template:

    .venv/bin/python scripts/admachin_push.py --print-config-template
"""
import argparse
import hashlib
import json
import pathlib
import sys

# import the sibling client whether run from repo root or scripts/
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import admachin_client as am  # noqa: E402

TARGETS_DIR = pathlib.Path(__file__).resolve().parent.parent / "admachin_targets"

CONFIG_TEMPLATE = {
    "project_id": "<project uuid — find via list_ad_plans() or the web UI>",
    "subproject_id": None,
    "copy": {
        "headline": "Optional default headline",
        "primary_text": "Optional default primary text",
        "description": "Optional default description",
    },
    "launch": {
        "ad_account_id": "act_1234567890",
        "campaign_id": "120210000000000000",
        "adset_id": "120210000000000001",
        "page_id": "1234567890",
        "cta_type": "LEARN_MORE",
        "landing_url": "https://example.com/lp?utm_source=facebook",
        "connection_id": None,
        "pixel_id": None,
        "event_type": None,
    },
}

LAUNCH_REQUIRED = ["ad_account_id", "campaign_id", "adset_id", "page_id", "cta_type", "landing_url"]


def _stable_key(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:32]


def _load_campaign(name):
    path = TARGETS_DIR / f"{name}.json"
    if not path.is_file():
        sys.exit(f"campaign config not found: {path}\n"
                 f"create it (see --print-config-template) or pass flags directly.")
    return json.loads(path.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?", help="path to the finished video (mp4/mov, ≤200 MiB)")
    ap.add_argument("--campaign", help="load admachin_targets/<name>.json for defaults")
    ap.add_argument("--project-id")
    ap.add_argument("--subproject-id")
    ap.add_argument("--type", default="video", choices=["video", "image"])
    ap.add_argument("--rating", type=int, help="creative quality rating 0..5")
    ap.add_argument("--headline")
    ap.add_argument("--primary", help="primary text")
    ap.add_argument("--description")
    ap.add_argument("--ad-type", help="free-text label grouping this ad (e.g. campaign-slug-2026-06-01)")

    g = ap.add_argument_group("launch (⚠ spends real money)")
    g.add_argument("--launch", action="store_true", help="also launch the assembled ad live on Facebook")
    g.add_argument("--yes", action="store_true", help="skip the interactive confirm (for automation)")
    g.add_argument("--ad-account-id")
    g.add_argument("--campaign-id", dest="fb_campaign_id")
    g.add_argument("--adset-id")
    g.add_argument("--page-id")
    g.add_argument("--cta", dest="cta_type", help="e.g. LEARN_MORE, SHOP_NOW, SIGN_UP")
    g.add_argument("--landing-url")
    g.add_argument("--connection-id")
    g.add_argument("--pixel-id")
    g.add_argument("--event-type")

    ap.add_argument("--print-config-template", action="store_true")
    args = ap.parse_args()

    if args.print_config_template:
        print(json.dumps(CONFIG_TEMPLATE, indent=2))
        return

    if not args.video:
        ap.error("video path is required (or use --print-config-template)")

    cfg = _load_campaign(args.campaign) if args.campaign else {}
    cfg_launch = cfg.get("launch", {})
    cfg_copy = cfg.get("copy", {})

    project_id = args.project_id or cfg.get("project_id")
    subproject_id = args.subproject_id or cfg.get("subproject_id")
    headline = args.headline if args.headline is not None else cfg_copy.get("headline")
    primary = args.primary if args.primary is not None else cfg_copy.get("primary_text")
    description = args.description if args.description is not None else cfg_copy.get("description")

    video = pathlib.Path(args.video)

    # --- 1. upload creative (stable idem key => re-run won't re-store bytes) ---
    up_key = _stable_key("upload", video.resolve(), video.stat().st_size if video.is_file() else 0)
    print(f"↑ uploading creative: {video.name} ({video.stat().st_size/1048576:.1f} MiB)" if video.is_file() else "↑ uploading…")
    creative = am.upload_creative(video, type=args.type, project_id=project_id,
                                  subproject_id=subproject_id, rating=args.rating, idem_key=up_key)
    creative_id = creative["id"]
    print(f"  creative_id = {creative_id}  (status={creative.get('status')})")

    # --- 2. copy (only the slots provided) ---
    copy_ids = {}
    for slot, text in (("headline", headline), ("primary_text", primary), ("description", description)):
        if text:
            row = am.create_ad_copy(text, slot, project_id=project_id, subproject_id=subproject_id)
            copy_ids[slot] = row["id"]
            print(f"  {slot} copy = {row['id']}  {text[:50]!r}")

    # --- 3. assemble one draft ad ---
    ad = am.create_ad(
        creative_id,
        headline_id=copy_ids.get("headline"),
        primary_id=copy_ids.get("primary_text"),
        description_id=copy_ids.get("description"),
        ad_type=args.ad_type,
        project_id=project_id,
        subproject_id=subproject_id,
    )
    ad_id = ad["id"]
    print(f"✓ assembled draft ad: {ad_id}")

    if not args.launch:
        print("\nDone (no launch). Review in the AdMachin web UI, or re-run with "
              "--launch + targeting to go live.")
        print(f"  ad_id = {ad_id}")
        return

    # --- 4. launch (gated) ---
    targeting = {
        "ad_account_id": args.ad_account_id or cfg_launch.get("ad_account_id"),
        "campaign_id": args.fb_campaign_id or cfg_launch.get("campaign_id"),
        "adset_id": args.adset_id or cfg_launch.get("adset_id"),
        "page_id": args.page_id or cfg_launch.get("page_id"),
        "cta_type": args.cta_type or cfg_launch.get("cta_type"),
        "landing_url": args.landing_url or cfg_launch.get("landing_url"),
        "connection_id": args.connection_id or cfg_launch.get("connection_id"),
        "pixel_id": args.pixel_id or cfg_launch.get("pixel_id"),
        "event_type": args.event_type or cfg_launch.get("event_type"),
    }
    missing = [k for k in LAUNCH_REQUIRED if not targeting.get(k)]
    if missing:
        sys.exit(f"✗ cannot launch — missing targeting: {', '.join(missing)}\n"
                 f"  supply via --campaign <name> config or CLI flags.")

    print("\n⚠  LAUNCH — this creates a LIVE Facebook ad and SPENDS REAL MONEY:")
    print(f"     ad         {ad_id}")
    print(f"     account    {targeting['ad_account_id']}")
    print(f"     campaign   {targeting['campaign_id']}")
    print(f"     ad set     {targeting['adset_id']}")
    print(f"     page       {targeting['page_id']}")
    print(f"     CTA        {targeting['cta_type']}")
    print(f"     landing    {targeting['landing_url']}")

    if not args.yes:
        if not sys.stdin.isatty():
            sys.exit("✗ refusing to launch: not a terminal and --yes not given.")
        if input('\n  Type "LAUNCH" to spend: ').strip() != "LAUNCH":
            sys.exit("✗ aborted — nothing launched.")

    launched = am.launch_ad(ad_id, **{k: v for k, v in targeting.items() if v is not None})
    print(f"\n✓ LAUNCHED  launch_id={launched['id']}  fb_ad_id={launched.get('fb_ad_id')}  "
          f"status={launched.get('status')}")
    print(f"  campaign: {launched.get('fb_campaign_name')}  adset: {launched.get('fb_adset_name')}")


if __name__ == "__main__":
    try:
        main()
    except am.AdMachinError as e:
        sys.exit(f"✗ AdMachin error {e}")
