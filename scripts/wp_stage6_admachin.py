"""Stage the 6 approved women's-prison finals to AdMachin as DRAFTS (no launch, no spend).
Upload creative -> verify -> headline + primary copy rows -> create_ad (NO ad_type — DB constraint).
Resumable via outputs/wp_stage6_state.json (single writer). User-approved copy 2026-07-12
(recommended Headline A per video; full 4-facility list; verbatim Pulaski/Jones disclaimer
appended to every primary).
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from admachin_client import upload_creative, create_ad_copy, create_ad, get_creative

PROJECT = "e15c60bd-95c2-47b9-9730-c29fb5325461"        # Tort
SUBPROJECT = "acf1b974-9721-488b-a4e0-ffe0664070c5"     # Women's Prison
STATE = pathlib.Path("outputs/wp_stage6_state.json")

DISCLAIMER = ("Paid legal advertisement. Jordan M. Jones, Attorney at Law (360 E 2nd St #820, "
  "Los Angeles, CA 90012) and Adam Pulaski, Attorney at Law (2925 Richmond Ave #1725, Houston, "
  "TX 77098) are responsible for this advertisement. A California-licensed attorney is associated "
  "for CA cases. This ad uses paid actors, dramatizations, and AI-generated imagery for "
  "illustration only and does not depict real clients or events. No guarantee or prediction of "
  "outcome is made. Cases may be referred to other attorneys.")

FACILITIES = ("▪️ CCWF — Chowchilla\n▪️ CIW — Chino\n"
              "▪️ Valley State Prison\n▪️ Folsom Women’s Facility")
CTA = "\U0001f447 Tap below and see if you qualify for significant potential compensation."

ADS = [
 {"slug": "voxpop-didyouknow", "video": "outputs/wp_voxpop/FINAL_grok.mp4",
  "headline": "Chowchilla Survivors May Qualify — Check Now",
  "primary": ("Most people on the street had no idea this was happening.\n\n"
    f"Guards and staff sexually abused women at:\n{FACILITIES}\n\n"
    "\U0001f4c4 Never reported it? You may still qualify.\n"
    "✅ 100% free and confidential to check.\n\n"
    f"{CTA}\n\n{DISCLAIMER}")},
 {"slug": "omni-500women", "video": "outputs/wp_voxpop/FINAL_omni.mp4",
  "headline": "Even 20 Years Later, You May Qualify",
  "primary": ("Nearly 500 women from California’s prisons are coming forward. Many thought "
    "it was too late — it isn’t.\n\n"
    f"Guards and staff sexually abused women at:\n{FACILITIES}\n\n"
    "\U0001f4c4 Never reported it back then? You may still qualify.\n"
    "✅ Free, confidential, and you never go to court.\n\n"
    f"{CTA}\n\n{DISCLAIMER}")},
 {"slug": "niceone", "video": "outputs/wp_interview2/FINAL_niceone.mp4",
  "headline": "It Wasn’t Kindness. You May Qualify.",
  "primary": ("He was “the nice one.” Always asking how you were. That was the whole "
    "trick.\n\nIf a guard or staff member sexually abused you — even if you called it "
    "something else back then — the law is on your side. This applies at:\n"
    f"{FACILITIES}\n\n"
    "\U0001f4c4 Never reported it? You may still qualify.\n"
    "✅ Free, confidential, no court.\n\n"
    f"{CTA}\n\n{DISCLAIMER}")},
 {"slug": "relationship", "video": "outputs/wp_series2/FINAL_relationship.mp4",
  "headline": "In Prison, It Was Never Consent",
  "primary": ("She called it a relationship for years. California law calls it what it was.\n\n"
    "Under California law, a woman in prison cannot consent to a guard. If staff sexually "
    f"abused you at:\n{FACILITIES}\n\n"
    "\U0001f4c4 Never reported it? You may still qualify.\n"
    "✅ Free and confidential — it takes about 2 minutes.\n\n"
    f"{CTA}\n\n{DISCLAIMER}")},
 {"slug": "moved", "video": "outputs/wp_series2/FINAL_moved.mp4",
  "headline": "They Moved You to Keep You Quiet",
  "primary": ("She reported it. They shipped her to another yard and wrote her up for lying.\n\n"
    f"If you were sexually abused by staff at:\n{FACILITIES}\n\n"
    "\U0001f4c4 Punished for speaking up, or never reported it at all? You may still qualify.\n"
    "✅ Free, confidential, and there is no court.\n\n"
    f"{CTA}\n\n{DISCLAIMER}")},
 {"slug": "kids", "video": "outputs/wp_series2/FINAL_kids.mp4",
  "headline": "You Never Told Anyone. You May Still Qualify.",
  "primary": ("She carried it alone for eleven years. Her kids still don’t know.\n\n"
    f"If a guard sexually abused you at:\n{FACILITIES}\n\n"
    "\U0001f4c4 You don’t have to tell your family to come forward.\n"
    "✅ Free, private, no court.\n\n"
    f"{CTA}\n\n{DISCLAIMER}")},
]

def load(): return json.loads(STATE.read_text()) if STATE.exists() else {}
def save(s): STATE.write_text(json.dumps(s, indent=2))

def main():
    state = load()
    for ad in ADS:
        slug = ad["slug"]; st = state.setdefault(slug, {})
        # 1. creative
        if "creative_id" not in st:
            print(f"[{slug}] uploading {ad['video']} ...", flush=True)
            c = upload_creative(ad["video"], type="video", project_id=PROJECT,
                                subproject_id=SUBPROJECT, idem_key=f"wp6-{slug}-creative")
            st["creative_id"] = c["id"]; save(state)
            # verify persisted (upload can silently not persist)
            get_creative(st["creative_id"])
            print(f"[{slug}] creative {st['creative_id']} verified", flush=True)
        # 2. copy rows
        if "headline_id" not in st:
            h = create_ad_copy(ad["headline"], "headline", project_id=PROJECT,
                               subproject_id=SUBPROJECT, name=f"wp6 {slug} H")
            st["headline_id"] = h["id"]; save(state)
        if "primary_id" not in st:
            p = create_ad_copy(ad["primary"], "primary_text", project_id=PROJECT,
                               subproject_id=SUBPROJECT, name=f"wp6 {slug} P")
            st["primary_id"] = p["id"]; save(state)
        # 3. draft ad (OMIT ad_type)
        if "ad_id" not in st:
            a = create_ad(st["creative_id"], headline_id=st["headline_id"],
                          primary_id=st["primary_id"], project_id=PROJECT,
                          subproject_id=SUBPROJECT)
            st["ad_id"] = a["id"]; save(state)
        print(f"[{slug}] DRAFT ad {st['ad_id']}  (creative {st['creative_id'][:8]}, "
              f"H {st['headline_id'][:8]}, P {st['primary_id'][:8]})", flush=True)
    print("STAGING COMPLETE — 6 drafts, nothing launched.")

if __name__ == "__main__":
    main()
