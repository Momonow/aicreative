"""
Depo-Provera — 20 NEW image ads, "SPEAK TO THE ALREADY-DIAGNOSED" angle (user pivot 2026-06-19).
Every ad addresses a woman who ALREADY has a meningioma/brain-tumor diagnosis — validation +
cause-reveal (Depo) + "you may qualify". NO future-risk/"5.6x more likely" framing. NO disclaimer.
Pure gpt-image-2 full-render at 1:1, 2K, via KIE (recovered).

Run: .venv/bin/python scripts/depo_diagnosed20_gen.py [--only <slug|n,..>] [--regen] [--workers 5]
Output: outputs/depo_ads/diagnosed20/<NN>_<slug>_<style>.png  (skip-if-exists)
"""
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/depo_ads/diagnosed20")
OUT.mkdir(parents=True, exist_ok=True)
ONLY = (" Render ONLY the exact text specified — do not invent extra text, headlines, or claims. "
        "No watermark, no logo, no disclaimer.")
REAL = (" Photoreal, ordinary relatable Black/African American woman, natural skin texture, no beauty "
        "retouching, no filter, looks like a real photo not a stock model.")

ADS = [
    dict(n=1, slug="brutalist", style="brutalist-swiss", headline="It May Not Be Your Fault",
         primary="A meningioma diagnosis leaves you asking what you did wrong. For many women the answer may be the Depo-Provera shot — now linked to these brain tumors. You may qualify for significant compensation. See if you qualify.",
         prompt="A bold brutalist-Swiss typographic poster, stark high-contrast, huge condensed black type on a flat off-white background, no imagery. The text reads exactly, top line smaller: 'YOU HAVE A BRAIN TUMOR.' then much larger below: 'IT MAY NOT BE YOUR FAULT.'"),
    dict(n=2, slug="letter", style="journal-handwritten", headline="To Every Woman Just Diagnosed",
         primary="The day you were told you had a brain tumor, everything changed. What no one told you: the Depo shot you were on may be the reason. You're not alone — and you may qualify for significant compensation. See if you qualify.",
         prompt="An open handwritten letter on aged cream paper with soft fold lines and legible cursive-style script. It reads exactly: 'To the woman who just heard the word \"meningioma\" — you are not alone. And it may not be random. The Depo shot you trusted may be why. You may qualify for significant compensation.' Warm, intimate."),
    dict(n=3, slug="search", style="flat-vector", headline="You've Been Searching for Answers",
         primary="If you've been trying to understand where your brain tumor came from, you're not the only one. Many women diagnosed with meningioma used Depo-Provera — and the two may be linked. You may qualify for significant compensation. See if you qualify.",
         prompt="A clean flat-vector illustration of a web search bar on a soft pastel background, a blinking cursor in the field. The typed query reads exactly: 'why did i get a meningioma after the depo shot'. A faint magnifier icon. Minimal, modern UI."),
    dict(n=4, slug="postsurgery", style="documentary-candid", headline="After the Surgery, the Questions",
         primary="Surgery, radiation, recovery — and still no explanation for why a brain tumor grew. For many women, the Depo-Provera shot may be the missing answer. You may qualify for significant compensation. See if you qualify.",
         prompt="A photoreal documentary portrait of an ordinary Black woman about 50 wearing a soft headscarf after brain surgery, sitting by a window, tired and reflective. A bold clean white headline across the lower third reads exactly: 'They removed the tumor. No one told me what caused it.'" + REAL),
    dict(n=5, slug="definition", style="editorial-glossy", headline="A Word You Never Wanted to Learn",
         primary="You didn't choose this diagnosis, but you deserve to know it may not have been random — research links Depo-Provera to meningioma. Women diagnosed may qualify for significant compensation. See if you qualify.",
         prompt="A clean editorial dictionary-entry card on white. A large serif word 'meningioma' with phonetic 'me·nin·gi·o·ma' and the label 'noun', then the definition reads exactly: 'a brain tumor now linked to the Depo-Provera shot.' Minimal elegant typography."),
    dict(n=6, slug="textmsg", style="ugc-phone", headline="\"Wait — The Shot Did This?\"",
         primary="Women are realizing the brain tumor they were diagnosed with may be linked to the Depo-Provera shot. If you had a meningioma and used Depo, you may qualify for significant compensation. See if you qualify.",
         prompt="A realistic smartphone Messages screen. Grey incoming bubbles and one blue outgoing bubble, reading exactly in order — incoming: 'did you ever take the depo shot??' / outgoing: 'yeah for years, why' / incoming: 'they're saying it's linked to the meningioma you had'. Clean phone UI."),
    dict(n=7, slug="newshead", style="newsprint-tabloid", headline="The Question Thousands Are Asking",
         primary="Across the country, women diagnosed with meningioma are finding a common thread: the Depo-Provera shot. A federal lawsuit is underway. You may qualify for significant compensation. See if you qualify.",
         prompt="A rights-clean stylized newspaper front-page clipping on off-white newsprint, bold serif masthead 'HEALTH WATCH', and a headline reading exactly: 'Women With Brain Tumors Are Asking the Same Question About Depo-Provera'. A small grayscale photo, authentic newsprint texture. NO real outlet logo."),
    dict(n=8, slug="solidarity", style="minimalist", headline="You Are Not the Only One",
         primary="A brain tumor diagnosis can feel isolating. But thousands of women who used Depo-Provera are facing the same meningioma diagnosis — and the same questions. You may qualify for significant compensation. See if you qualify.",
         prompt="A minimalist statement poster, lots of negative space, calm muted sage background. Centered bold sans text reads exactly: 'If you were diagnosed with a meningioma, you are not the only one.' Quiet, elegant."),
    dict(n=9, slug="faq", style="flat-vector", headline="Already Had Surgery? Read This",
         primary="Even if your meningioma was treated years ago, you may still have options. Women diagnosed after using Depo-Provera may qualify for significant compensation. Free and confidential to check. See if you qualify.",
         prompt="A clean FAQ card UI on a soft background. One question in bold: 'I already had surgery — is it too late?' and the answer directly below: 'No. If you had a meningioma after Depo, you may still qualify.' Minimal."),
    dict(n=10, slug="portraitquote", style="cinematic", headline="You Did Nothing Wrong",
         primary="A meningioma diagnosis comes with guilt and questions. But the Depo-Provera shot may be the real reason — not anything you did. You may qualify for significant compensation. See if you qualify.",
         prompt="A photoreal cinematic portrait of an ordinary Black woman about 48 in soft moody side light, looking quietly at the camera. A bold white quote across the lower third reads exactly: 'I kept asking what I did wrong. Turns out — nothing.' Film-still mood." + REAL),
    dict(n=11, slug="patientfile", style="receipt-document", headline="What Your File Doesn't Say",
         primary="Your records list the tumor — but may not connect it to the Depo shot. That link is now central to a federal lawsuit. You may qualify for significant compensation. See if you qualify.",
         prompt="A clinical medical patient-file card clipped to a clipboard, clean typeset fields. Two visible lines read exactly: 'Diagnosis: meningioma' and below it 'Possible factor: Depo-Provera (long-term use)'. Documentary realism."),
    dict(n=12, slug="scancaption", style="documentary-candid", headline="If This Is Your Scan, Read This",
         primary="A meningioma on your MRI may not be a coincidence. Research links the Depo-Provera shot to these brain tumors. You may qualify for significant compensation. See if you qualify.",
         prompt="A photoreal brain MRI scan on a dark radiology lightbox showing a rounded meningioma tumor. A bold white caption across the bottom reads exactly: 'If this looks like your scan, the Depo shot may be why.' Clinical, serious."),
    dict(n=13, slug="checklist", style="isometric", headline="Is This You?",
         primary="If you were diagnosed with a meningioma and used the Depo-Provera shot, the two may be connected — and you may qualify for significant compensation. Free and confidential. See if you qualify.",
         prompt="A clean isometric checklist card. Two checked items with green checkmarks read exactly: 'Diagnosed with a meningioma' and 'Used Depo-Provera', then a bold arrow pointing to: 'You may qualify.' Friendly, modern."),
    dict(n=14, slug="answer", style="pastel-soft", headline="Finally, an Answer",
         primary="Living with a brain tumor and no explanation is its own weight. The Depo-Provera shot may be the answer you were never given. You may qualify for significant compensation. See if you qualify.",
         prompt="A warm pastel-soft statement card, calm gentle gradient. Centered text reads exactly: 'For years, no one could tell you why. There may finally be an answer.' Soft, hopeful."),
    dict(n=15, slug="spotlight", style="luxe-goldblack", headline="Her Tumor Had an Explanation",
         primary="After her meningioma diagnosis, she learned the Depo-Provera shot may have been the cause. Her story isn't unique. You may qualify for significant compensation. See if you qualify.",
         prompt="A premium editorial spotlight card, gold-and-black, with a tasteful photoreal portrait of a dignified Black woman about 52. Bold text reads exactly: 'Her brain tumor finally had an explanation. So might yours.' Luxe, serious." + REAL),
    dict(n=16, slug="comic", style="cartoon-comic", headline="The Diagnosis. Then the Reason.",
         primary="First the brain tumor. Then the realization the Depo-Provera shot may have caused it. Women connecting the two may qualify for significant compensation. See if you qualify.",
         prompt="A clean two-panel comic strip. Panel 1: a woman at a doctor's office, caption box reading exactly 'The doctor said: meningioma.' Panel 2: the same woman looking at her phone, caption box reading exactly 'Then I learned the Depo shot may be why.' Bold comic style, clear lettering."),
    dict(n=17, slug="mythfact", style="bauhaus-geometric", headline="Think It Doesn't Count? It May.",
         primary="Even an older meningioma diagnosis may qualify if you used Depo-Provera. The link is now part of a federal lawsuit. See if you may qualify for significant compensation.",
         prompt="A bold two-panel geometric card. Top panel red labeled 'MYTH' reading exactly 'A tumor from years ago doesn't count.' Bottom panel green labeled 'FACT' reading exactly 'If it was a meningioma after Depo, you may still qualify.' High-contrast Bauhaus shapes."),
    dict(n=18, slug="quotewall", style="collage-cutpaper", headline="You're Not the Only One",
         primary="Women diagnosed with brain tumors after Depo-Provera share strikingly similar stories. If yours sounds like theirs, you may qualify for significant compensation. See if you qualify.",
         prompt="A cut-paper collage wall of short handwritten note fragments, each a different woman's voice, reading exactly: 'Stage 1 meningioma.' / 'Two surgeries.' / 'Years on the shot.' / 'Me too.' Layered torn-paper, authentic."),
    dict(n=19, slug="psa", style="vintage-retro", headline="Diagnosed After the Depo Shot?",
         primary="If you were diagnosed with a meningioma and used Depo-Provera, you may qualify for significant compensation. A federal lawsuit is underway. See if you qualify.",
         prompt="A vintage 1950s-style public-health poster, muted retro palette, bold period typography. The text reads exactly: 'DIAGNOSED WITH A MENINGIOMA AFTER THE DEPO SHOT? YOU MAY QUALIFY.' Retro poster look."),
    dict(n=20, slug="lovedone", style="golden-hour-lifestyle", headline="For the Woman You Love",
         primary="If your mom, sister, or friend was diagnosed with a meningioma after using Depo-Provera, you can help her find answers. She may qualify for significant compensation. See if she qualifies.",
         prompt="A photoreal warm documentary photo of two Black women at home in soft golden light, a younger woman about 30 gently supporting an older woman about 58 with an arm around her. A bold white line across the lower third reads exactly: 'If she was diagnosed with a brain tumor, she may have an answer — and options.'" + REAL),
]


def run_one(ad, regen):
    dest = OUT / f"{ad['n']:02d}_{ad['slug']}_{ad['style']}.png"
    if dest.exists() and not regen:
        return ad, "skip"
    try:
        r = kie.generate_gpt_image(ad["prompt"] + ONLY, aspect_ratio="1:1", resolution="2K")
    except Exception as e:
        return ad, f"err:{str(e)[:70]}"
    if r.get("status") == "success" and r.get("urls"):
        kie.download(r["urls"][0], dest)
        return ad, "ok"
    return ad, f"fail:{str(r.get('raw'))[:80]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()
    want = {s.strip() for s in args.only.split(",") if s.strip()}
    ads = [a for a in ADS if not want or a["slug"] in want or str(a["n"]) in want]
    fails = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, args.regen): a for a in ads}
        for f in as_completed(futs):
            ad, st = f.result()
            print(f"[{st}] {ad['n']:02d} {ad['slug']} ({ad['style']})", flush=True)
            if st.startswith(("err", "fail")):
                fails.append(f"{ad['n']:02d}_{ad['slug']}")
    print(f"\n=== done; fails: {fails or 'none'} ===", flush=True)


if __name__ == "__main__":
    main()
