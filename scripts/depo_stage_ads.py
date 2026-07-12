#!/usr/bin/env python3
"""Stage the 6 Depo interview ads (3 concepts x stacked+cut) into AdMachin as DRAFT ads.
Creates copy rows (headline+primary per concept), uploads captioned creatives, assembles ads.
NO launch, NO spend. Resumable via state file. Run: .venv/bin/python scripts/depo_stage_ads.py
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from admachin_client import upload_creative, create_ad_copy, create_ad

TORT = "e15c60bd-95c2-47b9-9730-c29fb5325461"
DEPO = "9cfb5b76-1dd3-4e07-b037-2dda178ac266"
STATE = Path("outputs/depo_admachin_stage.json")

CONCEPTS = {
 "badluck": {
   "headline": "Brain Meningioma? You May Qualify for Significant Compensation",
   "primary": (
     "Diagnosed with a brain meningioma?\n\n"
     "If you were on the Depo-Provera shot for over a year, this may not be \"bad luck.\"\n\n"
     "Prolonged use of the Depo shot has been linked to a significantly higher risk of brain "
     "meningioma, and thousands of women are now part of a federal lawsuit.\n\n"
     "You may qualify for significant compensation.\n\n"
     "✅ Free, confidential case review\n"
     "✅ A few private questions — about a minute\n"
     "✅ No court\n"
     "✅ Even a diagnosis from years ago may still qualify\n\n"
     "Tap below to check. \U0001F447"),
 },
 "insider": {
   "headline": "Diagnosed With a Brain Meningioma?",
   "primary": (
     "Were you diagnosed with a brain meningioma?\n\n"
     "She was — and she'd spent years giving the Depo-Provera shot to other women before she "
     "became the one on the table.\n\n"
     "Women on the Depo shot for over a year were found to be up to five times more likely to "
     "develop a brain meningioma, and no one warned them.\n\n"
     "If that's you, you may qualify for significant compensation.\n\n"
     "✅ Free, confidential review\n"
     "✅ A few private questions — about a minute\n"
     "✅ No court\n"
     "✅ Even a diagnosis from years ago may still qualify\n\n"
     "Tap below. \U0001F447"),
 },
 "figured": {
   "headline": "Brain Meningioma After the Depo Shot?",
   "primary": (
     "Diagnosed with a brain meningioma and told it was just random?\n\n"
     "It might not be. Women on the Depo-Provera shot for over a year were found to be up to five "
     "times more likely to develop a brain meningioma.\n\n"
     "She figured that out herself — nobody told her.\n\n"
     "If that's you, you may qualify for significant compensation.\n\n"
     "It takes about a minute:\n"
     "• Answer a few private questions online\n"
     "• A lawyer reviews it for free\n"
     "• It's confidential\n"
     "• Even a diagnosis from years ago may still qualify\n\n"
     "Tap below. \U0001F447"),
 },
}

# (concept, layout, video path)
CREATIVES = [
 ("badluck", "stacked", "outputs/depo_interview/edits/badluck_stacked_cap.mp4"),
 ("badluck", "cut",     "outputs/depo_interview/edits/badluck_cut_cap.mp4"),
 ("insider", "stacked", "outputs/depo_insider/edits/insider_stacked_cap.mp4"),
 ("insider", "cut",     "outputs/depo_insider/edits/insider_cut_cap.mp4"),
 ("figured", "stacked", "outputs/depo_figured/edits/figured_stacked_cap.mp4"),
 ("figured", "cut",     "outputs/depo_figured/edits/figured_cut_cap.mp4"),
]

def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {"copy": {}, "creatives": {}, "ads": {}}
    def save(): STATE.write_text(json.dumps(st, indent=1))

    # 1) copy rows per concept (headline + primary)
    for c, copy in CONCEPTS.items():
        st["copy"].setdefault(c, {})
        if "headline_id" not in st["copy"][c]:
            r = create_ad_copy(copy["headline"], "headline", project_id=TORT, subproject_id=DEPO,
                               name=f"Depo {c} headline")
            st["copy"][c]["headline_id"] = r.get("id"); save(); print(f"headline {c} -> {r.get('id')}")
        if "primary_id" not in st["copy"][c]:
            r = create_ad_copy(copy["primary"], "primary_text", project_id=TORT, subproject_id=DEPO,
                               name=f"Depo {c} primary")
            st["copy"][c]["primary_id"] = r.get("id"); save(); print(f"primary  {c} -> {r.get('id')}")

    # 2) upload creatives + 3) assemble draft ads
    for concept, layout, path in CREATIVES:
        key = f"{concept}_{layout}"
        if key not in st["creatives"]:
            r = upload_creative(path, type="video", project_id=TORT, subproject_id=DEPO)
            st["creatives"][key] = r.get("id"); save(); print(f"creative {key} -> {r.get('id')}")
        if key not in st["ads"]:
            cid = st["creatives"][key]
            hid = st["copy"][concept]["headline_id"]; pid = st["copy"][concept]["primary_id"]
            try:
                r = create_ad(cid, headline_id=hid, primary_id=pid, project_id=TORT, subproject_id=DEPO)
                st["ads"][key] = r.get("id"); save(); print(f"AD {key} -> {r.get('id')}")
            except Exception as e:
                print(f"AD FAIL {key}: {type(e).__name__} {e}")
    print("\n=== DRAFT ADS STAGED (no spend) ===")
    for k, v in st["ads"].items(): print(f"  {k}: ad {v}")

if __name__ == "__main__":
    main()
