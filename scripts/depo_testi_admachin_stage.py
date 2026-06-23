#!/usr/bin/env python3
"""Stage the 5 Depo TESTIMONIAL ads (headline variant) into AdMachin as full DRAFT ads (no launch).

Per ad: upload creative (the *_headline_4x5.png) -> create headline copy -> create primary copy ->
assemble ONE draft ad (creative + headline + primary) under Tort / Depo Provera. Resumable via its
OWN state file. NO launch code by construction. Copy = user-approved, brain-tumor-forward, no
disclaimer (inventory/depo_testimonials_copy.md).

    .venv/bin/python scripts/depo_testi_admachin_stage.py [--only t_confession,...]
"""
import argparse
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import admachin_client as am  # noqa: E402

PROJECT_ID = "e15c60bd-95c2-47b9-9730-c29fb5325461"      # Tort
SUBPROJECT_ID = "9cfb5b76-1dd3-4e07-b037-2dda178ac266"   # Depo Provera
FINAL = pathlib.Path("outputs/depo_ads/final")
STATE = pathlib.Path("outputs/depo_ads/admachin_testi_state.json")

ADS = [
    (21, "t_confession", "It Was a Brain Tumor. And No One Warned Me.",
     "It was a brain tumor. A meningioma, growing against my brain — and I was sitting in a freezing "
     "scan room when the doctor said the word, and the whole floor seemed to tilt.\n"
     "The first thing out of my mouth was, where did this come from? I don't smoke. I eat right. I did "
     "everything they tell you to do.\n"
     "The only thing I'd done for years was the Depo shot. Every three months, like clockwork. My doctor "
     "called it the easy one — no pill to forget — and I never thought about it again.\n"
     "Nobody ever warned me a birth control shot could grow a tumor in my head. Not my doctor, not the "
     "company that made it. The studies were already there. They knew, and they said nothing.\n"
     "One night I finally looked it up. Women diagnosed with a meningioma after using Depo-Provera may "
     "qualify for significant compensation.\n"
     "Here's what I wish someone had told me sooner: you don't need to have kept every record. It doesn't "
     "matter that the shot was years ago. It's free to check — you pay nothing unless compensation is "
     "recovered. And it's private; no one called my house.\n"
     "It took two minutes against years of me quietly blaming myself.\n"
     "If your chest got a little tight reading this, you already know. It is not too late. 👉 Tap below "
     "to see, privately, if you qualify."),
    (22, "t_daughter", "We Thought It Was Age. It Was a Brain Tumor.",
     "We thought it was just age. It wasn't. It was a brain tumor — a meningioma — and it had been "
     "growing in my mom's head for who knows how long.\n"
     "She's the kind of woman who never complains, so the forgetting, the repeating herself, we all "
     "waved it off. Until the scan.\n"
     "Back when I was small, she was on the Depo shot for years. The doctor told her it was simple and "
     "safe, one less thing for a busy mother to think about. She believed them. Why wouldn't she?\n"
     "Nobody ever told her it could cause something like this. I didn't know either, until I sat up one "
     "night reading about it — women diagnosed with a meningioma after using Depo-Provera may qualify "
     "for significant compensation.\n"
     "My mom would never look into this for herself; she'd say she doesn't want to be a bother. So I did "
     "it for her. You don't need a lawyer to start. You don't need old paperwork. It's free, it's "
     "private, and it took me about two minutes.\n"
     "If a woman you love was on that shot and then got this diagnosis, you can be the one who checks. "
     "Don't wait for her to ask. 👉 Tap below and see, privately, if she qualifies."),
    (23, "t_toolate", "A Brain Tumor Years Ago Still Counts Today.",
     "Three years ago they took a meningioma out of my head. A brain tumor. They opened my skull, "
     "removed it, and I spent a long time just trying to feel like myself again.\n"
     "So when I first heard the Depo shot was being linked to these tumors, I figured that ship had "
     "sailed. It happened to me years ago. Too late to matter now. I almost closed the page.\n"
     "I'm glad I didn't. Because that's not how it works.\n"
     "It doesn't matter that my diagnosis was a few years back. Women who were diagnosed with a "
     "meningioma after using Depo-Provera may still qualify for significant compensation.\n"
     "I was on that shot for years, and not one person ever warned me it could do this. I spent a long "
     "time thinking it was just bad luck. It may not have been luck at all.\n"
     "Here's what I'd tell the woman I was three years ago: you don't need a fresh diagnosis. You don't "
     "need a pile of records. It's free to find out, it's completely private, and it takes about two "
     "minutes.\n"
     "If you've been telling yourself it's too late — please, just check. It might not be. 👉 Tap below "
     "to see, privately, if you qualify."),
    (24, "t_longtime", "Fifteen Years on the Shot. Then a Brain Tumor.",
     "The headaches wouldn't stop. Then the dizziness, the moments where I'd lose my words. The scan "
     "showed a meningioma — a tumor in the lining of my brain.\n"
     "I kept asking how. I'd been healthy my whole life. The one constant was the Depo shot — fifteen "
     "years of it. One injection every few months, in and out of the office, and I never gave it a "
     "second thought.\n"
     "My doctor said it was the convenient one. No daily pill, nothing to remember. For a woman raising "
     "kids and working two jobs, it sounded perfect.\n"
     "All those years, all those appointments, and not one person ever mentioned a tumor could be the "
     "price. The research was already out there. They just didn't tell us.\n"
     "The longer a woman was on that shot, the higher the risk — and I was on it longer than anyone I "
     "know. When I read that women diagnosed with a meningioma after using Depo-Provera may qualify for "
     "significant compensation, I felt sick and relieved at the same time.\n"
     "Checking cost me nothing. No old records, no lawyer, no pressure — free and private, about two "
     "minutes.\n"
     "If you were on that shot for years like I was, and somewhere down the line they found a tumor, "
     "please don't let this pass. 👉 Tap below and see, privately, if you qualify."),
    (25, "t_newsreaction", 'I Almost Scrolled Past the Words "Brain Tumor."',
     "I almost scrolled right past it. Honestly, my thumb was already moving.\n"
     "Then I saw the word meningioma. That's the exact brain tumor they found in me two years ago. So "
     "I stopped.\n"
     "It was about the Depo shot — the birth control I was on for years in my thirties. They're saying "
     "it's been linked to these tumors, and there's a lawsuit now.\n"
     "I just sat there with my stomach in a knot. Because nobody — not a single doctor — ever warned me "
     "that shot could grow a tumor in my brain.\n"
     "So I checked to see if I qualified. It was free, it was private, and it honestly took about two "
     "minutes. Women diagnosed with a meningioma after using Depo-Provera may qualify for significant "
     "compensation.\n"
     "You don't need a police report or a stack of paperwork. It doesn't matter that the diagnosis was "
     "a while ago. No one will call your house.\n"
     "If you scrolled into this and you've had a meningioma after being on Depo, don't keep scrolling "
     "like I almost did. 👉 Tap below and see, privately, if you qualify."),
]


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2))


def stage_one(n, slug, headline, primary, st):
    rec = st.setdefault(slug, {})
    img = FINAL / f"{n:02d}_{slug}_headline_4x5.png"
    if not img.is_file():
        return f"MISSING IMAGE {img}"
    if not rec.get("creative_id"):
        key = hashlib.sha256(f"{img.resolve()}|{img.stat().st_size}".encode()).hexdigest()[:32]
        cr = am.upload_creative(img, type="image", project_id=PROJECT_ID,
                                subproject_id=SUBPROJECT_ID, idem_key=key)
        rec["creative_id"] = cr["id"]; save_state(st)
    if not rec.get("headline_id"):
        h = am.create_ad_copy(headline, "headline", project_id=PROJECT_ID,
                              subproject_id=SUBPROJECT_ID, name=f"depo {slug} headline")
        rec["headline_id"] = h["id"]; save_state(st)
    if not rec.get("primary_id"):
        p = am.create_ad_copy(primary, "primary_text", project_id=PROJECT_ID,
                              subproject_id=SUBPROJECT_ID, name=f"depo {slug} primary")
        rec["primary_id"] = p["id"]; save_state(st)
    if not rec.get("ad_id"):
        ad = am.create_ad(rec["creative_id"], headline_id=rec["headline_id"],
                          primary_id=rec["primary_id"], project_id=PROJECT_ID,
                          subproject_id=SUBPROJECT_ID)   # ad_type omitted (DB-constrained)
        rec["ad_id"] = ad["id"]; save_state(st)
    return rec["ad_id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    want = {s.strip() for s in args.only.split(",") if s.strip()}
    st = load_state()
    print("Staging 5 testimonials into Tort / Depo Provera — full DRAFT ads, no launch\n")
    done = []
    for n, slug, headline, primary in ADS:
        if want and slug not in want:
            continue
        if st.get(slug, {}).get("ad_id"):
            print(f"[skip] {n} {slug} -> ad {st[slug]['ad_id']}"); done.append((slug, st[slug]["ad_id"])); continue
        try:
            ad_id = stage_one(n, slug, headline, primary, st)
            print(f"[ok]   {n} {slug} -> ad {ad_id}"); done.append((slug, ad_id))
        except Exception as e:
            print(f"[ERR]  {n} {slug} -> {type(e).__name__}: {e}")
    print(f"\n==== {len(done)} testimonial draft ads staged ====")
    for slug, ad_id in done:
        print(f"  {slug:16s} {ad_id}")
    print(f"\nstate: {STATE}")


if __name__ == "__main__":
    main()
