"""20 completely-different VISUAL STYLES for TrimRx — each a full gpt-image-2 (KIE) banner.

NO PIL compositing. Each ad = gpt-image-2 IMAGE-TO-IMAGE with a real TrimRx vial PNG as
reference (product appears in every one); the model renders all text + layout. Goal: 20
distinct, attention-grabbing looks that feel nothing alike. All compliant (footnote, no
brand names, no before/after, no fake doctors, no FB-UI mimicry).

Run:
  .venv/bin/python scripts/trimrx_styles20.py                 # all 20, 1:1, skip-if-exists
  .venv/bin/python scripts/trimrx_styles20.py --only luxe,popart
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

OUTDIR = "outputs/trimrx_glp1/final"
VIALS = {"blue": "outputs/trimrx_glp1/product/vial_gip_blue.png",
         "duo": "outputs/trimrx_glp1/product/vials_duo.png"}

STYLE = (" Render as ONE single attention-grabbing social-media banner, BOLD large correctly-spelled "
         "typography, strong composition, no other brand names or logos, no fake doctors, no before-and-after "
         "imagery. Make the product vial(s) look like the reference image (clear glass vial, 'GLP-1' label, "
         "RX ONLY, Dose Varies). Put a small grey legal line at the very bottom: 'Compounded medication. "
         "Requires prescription. Not FDA-approved. Individual results vary.'")

ADS = [
    dict(n=1, slug="minimal", vial="blue", prompt=(
        "Ultra-minimalist premium product hero, Apple-keynote style: the single product vial from the "
        "reference image centered on a soft clean off-white-to-pale-mint gradient with lots of empty negative "
        "space and a soft studio reflection. A small elegant centered line below: 'Compounded GLP-1. From "
        "$149/mo.' and a tiny 'See if you qualify' link. Refined, calm, expensive.")),
    dict(n=2, slug="brutalist", vial="blue", prompt=(
        "Bold brutalist Swiss-design poster: one massive ultra-bold black sans-serif word 'ENOUGH.' filling "
        "a stark white canvas, a single small magenta accent block, the product vial from the reference image "
        "small in a lower corner, a tiny caption 'Done with crash diets. A compounded GLP-1 program · from "
        "$149/mo · See if you qualify.' Stark, graphic, design-forward.")),
    dict(n=3, slug="vintage", vial="blue", prompt=(
        "Vintage apothecary / old-school pharmacy poster: warm cream and kraft paper texture, ornate vintage "
        "serif typography, a decorative engraved border, the product vial from the reference image styled like "
        "a classic remedy bottle. Headline 'Modern medicine. Old-fashioned care.' subtext 'Provider-prescribed "
        "GLP-1 · from $149/mo'. Aged, timeless, characterful.")),
    dict(n=4, slug="y2k", vial="duo", prompt=(
        "Y2K / chrome gen-z aesthetic: glossy liquid-chrome 3D headline text reading 'glow up szn' in "
        "lowercase, a holographic iridescent pink-blue-silver gradient background, playful sparkles, the "
        "product vials from the reference image with a glossy treatment. Small line 'compounded GLP-1 · from "
        "$149/mo · take the quiz'. Trendy, fun, scroll-stopping.")),
    dict(n=5, slug="journal", vial="blue", prompt=(
        "A handwritten personal journal / diary page: ruled notebook paper, warm blue-ink handwriting reading "
        "'day 1. decided to actually do something about it.' a little hand-drawn checkmark and heart, a strip "
        "of tape holding the product vial from the reference image like a taped-in keepsake. A small printed "
        "line 'Compounded GLP-1 · from $149/mo · trimrx'. Intimate, authentic.")),
    dict(n=6, slug="receipt", vial="blue", prompt=(
        "A clean itemized receipt on white thermal paper, monospace type, header 'TRIMRX — YOUR MONTHLY "
        "TOTAL'. Line items with dotted leaders: 'GLP-1 medication .... included', 'Provider visits .... "
        "$0.00', 'Shipping .... $0.00', 'Dose increases .... $0.00', then a bold total 'TOTAL: $149/mo'. The "
        "product vial from the reference image beside the receipt. Small CTA 'See if you qualify'.")),
    dict(n=7, slug="tabloid", vial="duo", prompt=(
        "A vintage newspaper / tabloid clipping: black-and-white newsprint texture with halftone dots, a bold "
        "old-style headline 'Women Are Skipping the Clinic — and the $1,000 Bill'. A short newspaper body "
        "column reading EXACTLY: 'More women are skipping the clinic and the waiting room. With a telehealth "
        "program they get compounded GLP-1 medication, licensed-provider care, and home delivery — without "
        "insurance or sky-high office bills. Lower cost. More control.' The product vials from the reference "
        "image printed like a news photo with a caption. A small modern line 'Compounded GLP-1 · from $149/mo "
        "· trimrx.com'. Do NOT write the words 'same' or 'identical' or any drug brand name. Editorial.")),
    dict(n=8, slug="tracker", vial="blue", prompt=(
        "A clean habit-tracker calendar banner: a tidy 30-day month grid where most days have a green "
        "checkmark, the grid header reads 'YOUR FIRST 30 DAYS'. Headline 'Consistency, not perfection.' "
        "subtext 'A GLP-1 program that fits real life — from $149/mo'. A small caption 'Small steps. Real "
        "support.' The product vial from the reference image to the side. Green CTA 'Start day 1'. Do NOT use "
        "the words 'transformation', 'results', or any pounds/weight numbers. Modern, motivating.")),
    dict(n=9, slug="threed", vial="duo", prompt=(
        "A playful stylized 3D-render scene: the product vials from the reference image as glossy 3D objects "
        "on a soft pastel pedestal surrounded by bouncy 3D shapes, confetti and soft shadows, bright cheerful "
        "palette. A big rounded bubbly headline 'Weight loss, minus the hassle'. Small line 'Compounded GLP-1 "
        "· from $149/mo'. Green CTA 'See if you qualify'. Fun, tactile, eye-candy.")),
    dict(n=10, slug="duotone", vial="blue", prompt=(
        "A bold duotone design banner: a portrait of a confident relatable woman rendered in a striking "
        "two-tone teal-and-magenta duotone, high contrast, a bold white headline over it 'It finally clicked.' "
        "The product vial from the reference image in a corner in full color so it pops. Small line 'Compounded "
        "GLP-1 · from $149/mo'. Design-forward, modern.")),
    dict(n=11, slug="quizcard", vial="blue", prompt=(
        "A clean interactive-looking quiz card (do NOT imitate any app or social UI): headline 'Question 1 of "
        "3', a question 'Do you think about food all day?' with two big rounded answer buttons 'Yes' and "
        "'Sometimes', and a thin progress bar. The product vial from the reference image small in a corner. "
        "Bottom line 'Compounded GLP-1 · from $149/mo'. Green CTA 'Start the quiz'. Engaging.")),
    dict(n=12, slug="grid", vial="duo", prompt=(
        "A clean feature COMPARISON TABLE (a grid, not a price ladder): three columns headed 'TrimRx', 'Local "
        "clinic', 'Doing nothing', and rows 'Licensed providers', 'No insurance needed', 'Delivered to your "
        "door', 'From $149/mo' — green checkmarks down the TrimRx column, red X marks or dashes in the others. "
        "The product vials from the reference image at the top. Green CTA 'See if you qualify'. Clear, decisive.")),
    dict(n=13, slug="luxe", vial="blue", prompt=(
        "A luxe premium banner: deep matte-black background with elegant thin gold accents and a fine gold "
        "frame, a sophisticated serif headline 'Your weight-loss reset.' The product vial from the reference "
        "image lit dramatically like a luxury product. A small gold line 'Compounded GLP-1 · prescribed by "
        "licensed providers · from $149/mo'. Gold CTA 'See if you qualify'. High-end, exclusive.")),
    dict(n=14, slug="stickynote", vial="blue", prompt=(
        "A casual desk flat-lay shot from above: a bright yellow sticky note on a light wooden desk with "
        "handwriting 'finally dealt with my weight :)' and a hand-drawn checkmark, beside it the product vial "
        "from the reference image, a coffee cup and a phone. A small printed strip 'Compounded GLP-1 · from "
        "$149/mo · trimrx'. Relatable, casual, native.")),
    dict(n=15, slug="popart", vial="duo", prompt=(
        "A bold pop-art / comic-book banner (Lichtenstein/Warhol vibe): halftone Ben-Day dots, thick black "
        "outlines, bright primary colors, a comic speech bubble reading 'No more food noise!' and a bold "
        "starburst reading 'FROM $149/mo'. The product vials from the reference image illustrated in pop-art "
        "style. Small line 'Compounded GLP-1 · see if you qualify'. Loud, fun.")),
    dict(n=16, slug="map", vial="duo", prompt=(
        "A clean 'now available' localization banner: a stylized minimalist map of the United States with a "
        "few states subtly highlighted, headline 'Now available online across the U.S.' subtext 'Compounded "
        "GLP-1, prescribed by licensed providers · from $149/mo'. The product vials from the reference image. "
        "Green CTA 'Check your state'. Modern, relevant.")),
    dict(n=17, slug="macro", vial="blue", prompt=(
        "A striking macro extreme close-up: a crisp glass of ice water with condensation and light refraction "
        "filling the background, the product vial from the reference image sharp in the foreground. A bold "
        "white overlay headline 'Less hunger. More you.' Small line 'Compounded GLP-1 · from $149/mo'. Green "
        "CTA 'See if you qualify'. Fresh, clean, premium.")),
    dict(n=18, slug="pastel", vial="blue", prompt=(
        "A soft calming pastel wellness banner: a gentle blush-and-sage pastel gradient, airy and spa-like, a "
        "delicate friendly rounded-font headline 'Weight loss without the chaos.' The product vial from the "
        "reference image resting softly beside a sprig of greenery. Small line 'Compounded GLP-1 · from "
        "$149/mo'. Soft green CTA 'See if you qualify'. Calm, premium, gentle.")),
    dict(n=19, slug="icongrid", vial="duo", prompt=(
        "A colorful 'everything included' icon-grid banner: a tidy grid of six rounded tiles, each with a "
        "simple flat icon and short label — 'Licensed providers', 'Free shipping', 'Free dose changes', 'No "
        "insurance', '24/7 support', 'Delivered'. Headline 'One price. Everything in.' The product vials from "
        "the reference image. Bold price 'From $149/mo'. Green CTA 'See if you qualify'. Clean, vibrant.")),
    dict(n=20, slug="cinematic", vial="blue", prompt=(
        "A cinematic moody film-still lifestyle banner: a relatable woman by a rain-streaked window in soft "
        "directional light, contemplative and hopeful, shallow depth of field, filmic color grade. A bold "
        "lower-third headline 'This year felt different.' The product vial from the reference image subtly on "
        "the windowsill. Small line 'Compounded GLP-1 · from $149/mo'. Green CTA 'See if you qualify'.")),
]


def gen(ad, aspect, regen):
    out = os.path.join(OUTDIR, f"s{ad['n']:02d}_{ad['slug']}_gpt.png")
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
