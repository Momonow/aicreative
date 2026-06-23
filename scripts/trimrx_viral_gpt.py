"""10 viral / direct-response TrimRx banners — each rendered ENTIRELY by gpt-image-2 (KIE).

NO PIL / code compositing. Each ad is gpt-image-2 IMAGE-TO-IMAGE with a real TrimRx vial PNG
as the reference, so the actual product appears in every banner and the model renders all
text + layout itself. Python is only the API caller + downloader.

Run:
  .venv/bin/python scripts/trimrx_viral_gpt.py                    # all 10, 1:1, skip-if-exists
  .venv/bin/python scripts/trimrx_viral_gpt.py --only ugc,review  # subset / re-roll
  .venv/bin/python scripts/trimrx_viral_gpt.py --aspect 3:4       # taller feed
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

OUTDIR = "outputs/trimrx_glp1/final"
VIALS = {"blue": "outputs/trimrx_glp1/product/vial_gip_blue.png",   # tirzepatide GLP-1+GIP
         "duo": "outputs/trimrx_glp1/product/vials_duo.png"}        # green semaglutide + blue tirzepatide

STYLE = (" Clean modern high-end telehealth weight-loss brand ad, ONE single social-media banner, premium "
         "look, BOLD large readable and correctly-spelled typography, strong contrast, generous spacing, no "
         "clutter, no other brand names or logos, no fake doctors. Render the product vial(s) to look "
         "exactly like the reference image (clear glass vial, colored cap, 'GLP-1' label, RX ONLY, Dose "
         "Varies). At the very bottom, a small grey legal line: 'Compounded medication. Requires "
         "prescription. Not FDA-approved. Individual results vary.'")

ADS = [
    dict(n=1, slug="ugc", vial="blue", prompt=(
        "An authentic candid UGC smartphone photo (looks shot on an iPhone, slightly imperfect natural "
        "lighting, real and unpolished, NOT a studio ad) of an ordinary relatable woman's hand holding up "
        "the product vial from the reference image in a real home kitchen. A short casual white caption near "
        "the bottom reads: 'okay this actually changed my whole routine'. A small line under it: "
        "'Compounded GLP-1 · from $149/mo · trimrx'.")),
    dict(n=2, slug="review", vial="duo", prompt=(
        "A clean 5-star review banner: a big row of five gold stars near the top, then a large bold "
        "quote: 'I finally stopped thinking about food all day.' below it smaller text 'Jamie R. — verified "
        "member'. The two product vials from the reference image shown prominently. A bright green rounded "
        "button reads 'See if you qualify'. A small line: 'Compounded GLP-1 · from $149/mo'.")),
    dict(n=3, slug="authority", vial="duo", prompt=(
        "A credibility / social-proof banner: a big bold headline 'Trusted by 300,000+ members'. A row of "
        "three small badges each with a green check: 'Licensed U.S. providers', 'State-licensed pharmacies', "
        "'Delivered to your door'. The two product vials from the reference image. A green rounded button "
        "'See if you qualify'. A small line: 'Compounded GLP-1 from $149/mo'. Premium and trustworthy.")),
    dict(n=4, slug="curiosity", vial="blue", prompt=(
        "A scroll-stopping curiosity banner, clean and intriguing: a huge bold headline 'Why are women over "
        "40 quietly switching to this?'. The single product vial from the reference image shown to one side. "
        "A green rounded button 'See why'. A small line: 'Compounded GLP-1 · prescribed online · from "
        "$149/mo'.")),
    dict(n=5, slug="qualify", vial="duo", prompt=(
        "A checklist qualifier banner. Headline 'You might qualify if…'. A vertical list of four items, each "
        "with a green check mark: 'You think about food all day', 'You've tried every diet', 'You don't have "
        "insurance', 'You want provider support'. The two product vials from the reference image to one "
        "side. A green rounded button 'See if you qualify'. Small line 'Compounded GLP-1 from $149/mo'.")),
    dict(n=6, slug="thisorthat", vial="duo", prompt=(
        "A 'this or that' choice banner. Headline 'Which one is right for you?'. Two side-by-side option "
        "cards: the LEFT card labeled 'SEMAGLUTIDE — GLP-1' next to the GREEN-capped vial from the reference "
        "image; the RIGHT card labeled 'TIRZEPATIDE — GLP-1 + GIP' next to the BLUE-capped vial from the "
        "reference image. Subtext 'Take the 3-minute quiz to find your match.' A green rounded button 'Find "
        "your match'. Small line 'from $149/mo · prescribed by licensed providers'.")),
    dict(n=7, slug="timeline", vial="blue", prompt=(
        "A clean 'Your first 30 days' timeline banner. Title 'Your first 30 days'. Four milestone steps with "
        "small simple icons and short labels: 'Day 1 — 3-minute quiz', 'Week 1 — first dose', 'Week 4 — "
        "cravings ease', 'Ongoing — provider check-ins'. The single product vial from the reference image. A "
        "green rounded button 'Start day 1'. Small line 'Compounded GLP-1 from $149/mo'.")),
    dict(n=8, slug="howitworks", vial="blue", prompt=(
        "A simple educational infographic banner. Headline 'How a GLP-1 works with your body'. A clean, "
        "simple stomach/body silhouette diagram with three short labeled points: 'Slows digestion', 'Curbs "
        "appetite', 'Helps you feel full longer'. The single product vial from the reference image. A green "
        "rounded button 'See if you qualify'. Small line 'Compounded GLP-1 from $149/mo'. Clean infographic "
        "style.")),
    dict(n=9, slug="scarcity", vial="duo", prompt=(
        "A bold urgency deal banner with warm energy. A ribbon reading 'LIMITED NEW-PATIENT PRICING'. A huge "
        "bold price 'From $149/mo'. Subtext 'All doses & shipping included · no insurance needed'. The two "
        "product vials from the reference image. A bright green rounded button 'Claim this price'. A small "
        "line 'Limited intake this month'.")),
    dict(n=10, slug="warning", vial="duo", prompt=(
        "A pattern-interrupt PSA banner, serious and attention-grabbing but clean. Bold headline 'Before you "
        "pay $1,000+ for weight-loss care, read this.'. Subtext 'A telehealth GLP-1 program starts at just "
        "$149/mo — prescribed by licensed providers, delivered to your door.'. The two product vials from "
        "the reference image. A green rounded button 'See if you qualify'.")),
]


def gen(ad, aspect, regen):
    out = os.path.join(OUTDIR, f"v{ad['n']:02d}_{ad['slug']}_gpt.png")
    if os.path.exists(out) and not regen:
        return ad["slug"], out, "skip"
    try:
        url = kie.upload_file(VIALS[ad["vial"]])
        res = kie.generate_gpt_image(ad["prompt"] + STYLE, image_urls=[url], aspect_ratio=aspect, resolution="2K")
    except Exception as e:
        return ad["slug"], None, f"err:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return ad["slug"], None, f"fail:{str(res.get('raw'))[:120]}"
    kie.download(res["urls"][0], out)
    return ad["slug"], out, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--aspect", default="1:1")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--regen", action="store_true")
    args = ap.parse_args()
    ads = ADS
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        ads = [a for a in ADS if a["slug"] in want]
    print(f"MODEL: gpt-image-2-image-to-image (KIE)  ASPECT {args.aspect}  2K  — {len(ads)} ads")
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(gen, a, args.aspect, args.regen): a["slug"] for a in ads}
        for fut in as_completed(futs):
            slug, out, st = fut.result()
            print(f"[{st}] {slug} -> {out}", flush=True)


if __name__ == "__main__":
    main()
