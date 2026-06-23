#!/usr/bin/env python3
"""Stage the 70 Depo "speak-to-the-diagnosed" image ads into AdMachin as full DRAFT ads (no launch).

Combines the 20 (outputs/depo_ads/diagnosed20/) + the 50 (outputs/depo_ads/diagnosed50/) keyed by a
GLOBAL number (1-70) so colliding slugs (e.g. "spotlight" in both) stay distinct. Per ad:
upload creative -> headline copy -> primary copy -> assemble draft ad, under Tort / Depo Provera.
Resumable own state file. NO launch code. Skips any ad whose image isn't generated yet.

    .venv/bin/python scripts/depo_diag_admachin_stage.py [--only <n,..>]
"""
import argparse
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import admachin_client as am  # noqa: E402
from depo_diagnosed20_gen import ADS as ADS20  # noqa: E402

PROJECT_ID = "e15c60bd-95c2-47b9-9730-c29fb5325461"      # Tort
SUBPROJECT_ID = "9cfb5b76-1dd3-4e07-b037-2dda178ac266"   # Depo Provera
STATE = pathlib.Path("outputs/depo_ads/diagnosed_admachin_state.json")
D20 = pathlib.Path("outputs/depo_ads/diagnosed20")
D50 = pathlib.Path("outputs/depo_ads/diagnosed50")


def build_manifest():
    rows = []
    for a in ADS20:  # n 1-20
        img = D20 / f"{a['n']:02d}_{a['slug']}_{a['style']}.png"
        rows.append(dict(n=a["n"], slug=a["slug"], img=img, headline=a["headline"], primary=a["primary"]))
    for a in json.load(open(D50 / "prompts.json"))["ads"]:  # n 21-70
        img = D50 / f"{a['n']:02d}_{a['slug']}_{a['style']}.png".replace("/", "-")
        rows.append(dict(n=a["n"], slug=a["slug"], img=img, headline=a["headline"], primary=a["primary"]))
    return sorted(rows, key=lambda r: r["n"])


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2))


def stage_one(row, st):
    key = str(row["n"])
    rec = st.setdefault(key, {"slug": row["slug"]})
    img = row["img"]
    if not img.is_file():
        return "no-image-yet"
    if not rec.get("creative_id"):
        ik = hashlib.sha256(f"{img.resolve()}|{img.stat().st_size}".encode()).hexdigest()[:32]
        cr = am.upload_creative(img, type="image", project_id=PROJECT_ID, subproject_id=SUBPROJECT_ID, idem_key=ik)
        rec["creative_id"] = cr["id"]; save_state(st)
    if not rec.get("headline_id"):
        h = am.create_ad_copy(row["headline"], "headline", project_id=PROJECT_ID, subproject_id=SUBPROJECT_ID,
                              name=f"depo diag {row['n']:02d} {row['slug']} H")
        rec["headline_id"] = h["id"]; save_state(st)
    if not rec.get("primary_id"):
        p = am.create_ad_copy(row["primary"], "primary_text", project_id=PROJECT_ID, subproject_id=SUBPROJECT_ID,
                              name=f"depo diag {row['n']:02d} {row['slug']} P")
        rec["primary_id"] = p["id"]; save_state(st)
    if not rec.get("ad_id"):
        ad = am.create_ad(rec["creative_id"], headline_id=rec["headline_id"], primary_id=rec["primary_id"],
                          project_id=PROJECT_ID, subproject_id=SUBPROJECT_ID)   # ad_type omitted (DB-constrained)
        rec["ad_id"] = ad["id"]; save_state(st)
    return rec["ad_id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    want = {s.strip() for s in args.only.split(",") if s.strip()}
    rows = build_manifest()
    if want:
        rows = [r for r in rows if str(r["n"]) in want]
    st = load_state()
    print("Staging diagnosed ads into Tort / Depo Provera — DRAFTS, no launch\n")
    done = pend = 0
    for row in rows:
        if st.get(str(row["n"]), {}).get("ad_id"):
            print(f"[skip] {row['n']:02d} {row['slug']} -> {st[str(row['n'])]['ad_id']}"); done += 1; continue
        try:
            res = stage_one(row, st)
            if res == "no-image-yet":
                print(f"[wait] {row['n']:02d} {row['slug']} (image not generated yet)"); pend += 1
            else:
                print(f"[ok]   {row['n']:02d} {row['slug']} -> {res}"); done += 1
        except Exception as e:
            print(f"[ERR]  {row['n']:02d} {row['slug']} -> {type(e).__name__}: {e}")
    print(f"\n==== staged/known: {done}  waiting-on-image: {pend} ====\nstate: {STATE}")


if __name__ == "__main__":
    main()
