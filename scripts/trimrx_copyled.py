"""Copy-led / minimal-image TrimRx ads — a STRUCTURAL break from the busy banners.

The idea: the FB PRIMARY TEXT does the selling; the IMAGE is minimal (a news photo, a plain
candid shot, a single statement, a search query, a clean product still, a quiet scene) with
little or no baked text — NO price, NO CTA button, NO 'GLP-1 RX ONLY' vial-label clutter.
Images via gpt-image-2 (KIE). The compliant disclaimer lives in the PRIMARY TEXT (Meta rule),
written per-ad and emitted to copy_led.md.

Run: .venv/bin/python scripts/trimrx_copyled.py   (--only news,statement)
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

OUTDIR = "outputs/trimrx_glp1/final"
VIAL = "outputs/trimrx_glp1/product/vial_gip_blue.png"
NOTEXT = (" Absolutely NO text, no words, no letters, no numbers, no captions, no logos, no watermark "
          "anywhere in the image.")
DISC = ("TrimRX does not practice medicine or prescribe medications. Compounded medications are not "
        "FDA-approved and are not evaluated by the FDA for safety, effectiveness, or quality. Results "
        "vary by individual and are not guaranteed.")

ADS = [
    dict(n=1, slug="news", mode="t2i", prompt=(
        "A documentary news-style photograph: a relatable woman in her late 40s sitting at her kitchen "
        "table at home holding a coffee mug, looking thoughtfully toward a window, natural candid daylight, "
        "realistic, looks like a still from a TV health-news segment (NOT an ad). Across the lower third a "
        "single clean white news-style title in a simple sans-serif reads exactly: 'More women are getting "
        "GLP-1 care without the clinic.' No other text, no price, no button, no logo, no product visible."),
        headline="GLP-1 Care, Without the Clinic",
        primary=("More women are skipping the clinic entirely. A telehealth program now connects you with "
                 "licensed providers who can prescribe a compounded GLP-1 — reviewed online and delivered to "
                 "your door, from $149/month, no insurance needed. If the weight hasn't budged no matter what "
                 "you try, it may be worth a look. Take the 3-minute quiz to see if you qualify.")),
    dict(n=2, slug="candid", mode="t2i", prompt=(
        "An authentic candid smartphone-style photo of an ordinary, relatable woman in her 40s at home in "
        "her kitchen, natural window light, a genuine unposed expression, real and believable with visible "
        "natural skin texture (NOT a glamour model, NOT a doctor)." + NOTEXT),
        headline="It Was Never About Willpower",
        primary=("For years I thought I just needed more discipline. Turns out the all-day food noise wasn't "
                 "a character flaw — it's biology. A compounded GLP-1, prescribed by a licensed provider, "
                 "helped me quiet it. No clinic, no insurance, delivered to my door, from $149/month. If "
                 "you've tried everything, this might be the piece you were missing. See if you qualify in 3 "
                 "minutes.")),
    dict(n=3, slug="statement", mode="t2i", prompt=(
        "A clean minimalist statement card: a plain deep teal-green background, ONE bold white sans-serif "
        "line of text centered, reading exactly: \"It's not your willpower. It's your biology.\" Nothing "
        "else at all — no product, no price, no button, no logo, no other text.")),
    dict(n=4, slug="search", mode="t2i", prompt=(
        "A clean, simple stylized search-bar graphic centered on a plain off-white background: a single "
        "rounded search input box containing the typed query 'why is it so hard to lose weight after 40?' "
        "with a small magnifying-glass icon. Minimal, lots of whitespace, no other text, no logos, do NOT "
        "imitate any specific company's interface.")),
    dict(n=5, slug="product_clean", mode="i2i", prompt=(
        "A clean minimalist editorial still-life of the medical vial from the reference image — a CLEAR GLASS "
        "pharmacy MEDICATION vial with a colored (blue or green) metal crimp cap and a plain white printed "
        "label reading 'GLP-1', 'RX ONLY', 'Dose Varies' — standing on a soft neutral stone surface with "
        "gentle directional light and a soft shadow, lots of negative space. It MUST look like a clinical "
        "medication vial exactly like the reference; it is NOT a cosmetic serum or oil bottle, NOT a gold "
        "cap, NO swirl or monogram logo, no added marketing text.")),
    dict(n=6, slug="scene", mode="t2i", prompt=(
        "A quiet, emotional documentary still-life photograph: a pair of folded denim jeans with a cloth "
        "measuring tape resting on top, on a softly-lit bed in warm morning light, no people, real and "
        "relatable." + NOTEXT)),
    dict(n=7, slug="article", mode="t2i", prompt=(
        "A content/article-style hero image: a documentary photo of a relatable woman in her 40s walking "
        "outdoors in a park in soft morning light, looks like the header photo of a health-website article. "
        "Across the bottom a single clean editorial headline in a serif font reads exactly: 'The quiet shift "
        "in how women over 40 are losing weight.' No other text, no price, no button, no logo."),
        headline="How Women Over 40 Are Losing Weight Now",
        primary=("A growing number of women are skipping the clinic and starting GLP-1 care online — a "
                 "3-minute quiz, a licensed provider's review, and compounded medication delivered to the "
                 "door, from $149/month with no insurance. Read why it's catching on, and see if you qualify.")),
    dict(n=8, slug="letter", mode="t2i", prompt=(
        "A clean, calm open-letter text card: a plain warm off-white background, a short heartfelt message in "
        "an elegant simple font reading exactly: \"If you've felt like your body stopped listening — you're "
        "not alone, and it's not your fault.\" A small signature line below: '— the TrimRx team'. Nothing "
        "else: no product, no price, no button, no logo."),
        headline="A Note for Anyone Tired of Trying",
        primary=("If you've blamed yourself for years, read this. The all-day hunger isn't a willpower "
                 "problem — it's biology, and a compounded GLP-1 program guided by licensed providers may "
                 "help. No clinic, no insurance, delivered, from $149/month. See if you qualify in 3 minutes.")),
    dict(n=9, slug="signs", mode="t2i", prompt=(
        "A clean minimalist text card on a plain soft-sage background: a simple title 'It might be more than "
        "willpower if…' followed by a short numbered list: '1. You think about food all day   2. You lose "
        "weight then gain it back   3. Diets stopped working after 40   4. You're hungry an hour after "
        "eating'. Clean simple sans-serif, lots of whitespace, no product, no price, no button, no logo."),
        headline="It Might Be More Than Willpower",
        primary=("If a few of these sound familiar, your biology may be working against you — and that's "
                 "exactly what a GLP-1 can help with. Provider-prescribed, delivered, from $149/month, no "
                 "insurance needed. Take the 3-minute quiz to see if you qualify.")),
    dict(n=10, slug="stat", mode="t2i", prompt=(
        "A clean minimalist single-stat card: a plain deep-navy background, one very large bold white number "
        "'300,000+' centered, with a smaller line beneath it reading 'started their GLP-1 journey online'. "
        "Nothing else: no product, no price, no button, no logo."),
        headline="Join 300,000+ Who Started Online",
        primary=("Hundreds of thousands have started a telehealth GLP-1 program — no clinic, no insurance. "
                 "Compounded GLP-1, prescribed by licensed providers, delivered to your door, from "
                 "$149/month. See if you qualify in 3 minutes.")),
    dict(n=11, slug="mirror", mode="t2i", prompt=(
        "An authentic candid mirror-selfie of an ordinary relatable woman in her 40s in casual clothes in her "
        "bedroom, holding her phone up to the mirror, natural light, real and unposed, genuine expression "
        "(NOT a glamour model)." + NOTEXT),
        headline="The Day I Stopped Fighting My Body",
        primary=("I spent years at war with my own appetite. Starting a provider-prescribed GLP-1 was the "
                 "first time it felt quiet. No clinic, no insurance, delivered, from $149/month. If you've "
                 "tried everything, this might be your missing piece. See if you qualify.")),
    dict(n=12, slug="doorstep", mode="t2i", prompt=(
        "A warm lifestyle photo: a plain discreet cardboard delivery box on a welcoming front doorstep in "
        "soft golden morning light, a potted plant beside the door, inviting and clean, no labels or text on "
        "the box." + NOTEXT),
        headline="It Just Shows Up at Your Door",
        primary=("No pharmacy lines, no clinic waiting rooms. A 3-minute quiz, a licensed provider's review, "
                 "and your compounded GLP-1 arrives discreetly at your door — from $149/month, no insurance "
                 "needed. See if you qualify.")),
]

# headline + primary text for the no-baked-copy minimal ones (the IMAGE has no/■1 line; copy sells)
COPY = {
    "statement": dict(headline="It's Biology, Not Willpower",
        primary=("If cutting calories only made the cravings louder, you're not weak — that's how appetite "
                 "works. A compounded GLP-1 program works with your biology to help quiet the food noise. "
                 "Prescribed by licensed providers, delivered, from $149/month, no insurance needed. See if "
                 "you qualify.")),
    "search": dict(headline="Why It Gets Harder After 40",
        primary=("Hormones and metabolism shift after 40, and the old tricks stop working. A provider-guided "
                 "GLP-1 program may help. A 3-minute quiz, licensed providers, delivered to your door, from "
                 "$149/month. See if you qualify.")),
    "product_clean": dict(headline="One Flat Price. Everything Included.",
        primary=("Compounded GLP-1 care, simplified: licensed-provider visits, free shipping, and free dose "
                 "changes — one flat price from $149/month, no insurance needed. Take the 3-minute quiz to "
                 "see if you qualify.")),
    "scene": dict(headline="When Nothing Fits the Way It Used To",
        primary=("If the jeans haven't fit in a while and every diet has let you down, it's not about "
                 "willpower. A compounded GLP-1 program, guided by licensed providers, may help — from "
                 "$149/month, delivered, no insurance. See if you qualify in 3 minutes.")),
}


def gen(ad, aspect, regen):
    out = os.path.join(OUTDIR, f"c{ad['n']:02d}_{ad['slug']}_gpt.png")
    if os.path.exists(out) and not regen:
        return ad["slug"], out, "skip"
    try:
        urls = [kie.upload_file(VIAL)] if ad["mode"] == "i2i" else None
        res = kie.generate_gpt_image(ad["prompt"], image_urls=urls, aspect_ratio=aspect, resolution="2K")
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
    print(f"MODEL: gpt-image-2 (KIE)  ASPECT {args.aspect}  2K — {len(ads)} copy-led/minimal ads")
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(gen, a, args.aspect, args.regen): a["slug"] for a in ads}
        for fut in as_completed(futs):
            slug, out, st = fut.result()
            print(f"[{st}] {slug} -> {out}", flush=True)

    lines = ["# TrimRx copy-led / minimal-image ads — FB headline + PRIMARY TEXT (the ad)\n",
             "Image is minimal; the primary text does the selling. Every primary text ends with the "
             "mandatory disclaimer.\n"]
    for a in ADS:
        c = COPY.get(a["slug"], a)
        lines.append(f"\n## c{a['n']:02d} · {a['slug']}\n**Headline:** {c.get('headline','')}\n")
        lines.append(f"**Primary text:** {c.get('primary','')}\n\n{DISC}\n")
    with open("outputs/trimrx_glp1/copy_led.md", "w") as fh:
        fh.write("\n".join(lines))
    print("[copy] wrote outputs/trimrx_glp1/copy_led.md", flush=True)


if __name__ == "__main__":
    main()
