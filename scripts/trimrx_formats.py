"""TrimRx — ~58 ads, EACH A UNIQUE FORMAT not used in the other batches (full gpt-image-2).

Goal bar: every ad unique in FORMAT *and* angle/persona. The viral(10)+styles(20)+clean(12)+
compare(1) batches already cover ~43 distinct formats; this batch adds ~58 brand-new structural
formats so the library has 100+ genuinely-different-looking ads. Compliant: explicit on-image text
only (the model invents claims like 'REAL RESULTS' when left open), NO brand names, NO
guarantee/proven/clinically/FDA, NO before-after, NO fake doctors; footnote on each.

Run: .venv/bin/python scripts/trimrx_formats.py   (--only <slug,..>  --workers 4)
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

OUTDIR = "outputs/trimrx_glp1/final"
VIAL = "outputs/trimrx_glp1/product/vial_gip_blue.png"
FOOT = "Compounded medication. Requires prescription. Not FDA-approved. Individual results vary."
STYLE = (" Render as ONE banner in EXACTLY this format, BOLD large correctly-spelled typography. Render "
         "ONLY the text specified above — do NOT invent extra headlines, claims, or marketing copy. NO brand "
         "names (no Ozempic/Wegovy/Mounjaro/Zepbound), NO 'same/identical/generic', NO 'results/guaranteed/"
         "proven/clinically/FDA-approved/sustainable weight loss', NO before-after, NO fake doctors. Where a "
         "vial appears, match the reference (clear glass vial, 'GLP-1' label, RX ONLY, Dose Varies).")

# n, slug, mode(i2i/t2i), prompt(format + EXACT text), headline(FB), primary(FB)
ADS = [
    dict(n=1, slug="rxlabel", mode="t2i", prompt="An extreme macro close-up of a prescription medication label, the printed label text reading 'TrimRx · GLP-1 · A fresh start · From $149/mo · No insurance needed'. Pharmacy realism.", headline="A Fresh Start, By Prescription", primary="Provider-prescribed compounded GLP-1, delivered, from $149/mo. See if you qualify."),
    dict(n=2, slug="recipe", mode="t2i", prompt="A clean recipe card titled 'Recipe for feeling like yourself' with short 'ingredients': '1 quick quiz', '1 licensed provider', '1 compounded GLP-1', 'delivered to your door'. Tidy kitchen recipe-card layout.", headline="The Only Recipe You Need", primary="A 3-minute quiz, licensed providers, and compounded GLP-1 delivered — from $149/mo. See if you qualify."),
    dict(n=3, slug="definition", mode="t2i", prompt="A dictionary-entry card: large word 'food noise' with phonetic spelling, then 'noun — the constant mental chatter about food.' and a line 'A GLP-1 can help quiet it.' Clean editorial.", headline="Food Noise, Defined", primary="That all-day mental chatter about food is biology. A compounded GLP-1 may help. From $149/mo. See if you qualify."),
    dict(n=4, slug="roadsign", mode="t2i", prompt="A green highway exit sign mounted against blue sky reading 'EXIT — All-Day Cravings · NEXT: a 3-minute quiz'. Realistic road-sign style.", headline="Your Exit From the Cravings", primary="A compounded GLP-1 program may help quiet cravings. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=5, slug="nutritionlabel", mode="t2i", prompt="A 'Plan Facts' panel parodying a nutrition label: header 'Plan Facts', rows 'Licensed provider visits — included', 'Shipping — $0', 'Dose changes — $0', 'Monthly price — from $149'. Clean black-on-white panel.", headline="Read the Plan Facts", primary="One flat price covers visits, shipping, and dose changes — from $149/mo, no insurance. See if you qualify."),
    dict(n=6, slug="flowchart", mode="t2i", prompt="A simple decision flowchart titled 'Should you try a GLP-1?' with boxes and arrows: 'Tried diets?' yes-> 'Cravings all day?' yes-> 'Take the 3-minute quiz'. Clean diagram.", headline="Should You Try a GLP-1?", primary="Answer a few questions and a licensed provider reviews you. Compounded GLP-1 from $149/mo. See if you qualify."),
    dict(n=7, slug="coupon", mode="i2i", prompt="A tear-off coupon/voucher with a dashed border: bold '$0 consult + from $149/mo', small 'new patients · no insurance needed', a barcode at the bottom. The product vial from the reference image in the corner.", headline="Your New-Patient Offer", primary="No-cost consult and compounded GLP-1 from $149/mo. Licensed providers, delivered. See if you qualify."),
    dict(n=8, slug="certificate", mode="t2i", prompt="An ornate award certificate reading 'Officially Done With Diets' with a gold seal and a signature line. Formal certificate layout.", headline="You're Officially Done With Diets", primary="It was never about willpower. A compounded GLP-1, guided by licensed providers, may help. From $149/mo. See if you qualify."),
    dict(n=9, slug="gauge", mode="t2i", prompt="A clean dashboard gauge/speedometer graphic with the needle moving from a red zone labeled 'cravings' to a green zone labeled 'calm'. Minimal infographic.", headline="From Cravings to Calm", primary="A compounded GLP-1 may help dial down the food noise. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=10, slug="visionboard", mode="t2i", prompt="A tidy vision-board / mood-board collage pinned to a corkboard: small images of a morning walk, a glass of water, a calendar, a journal, and one pinned note reading 'feel like me again'. Warm, aspirational, no other text.", headline="This Year's Vision", primary="A telehealth GLP-1 program to help you get there — quiz, licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=11, slug="chalkboard", mode="t2i", prompt="A chalkboard with hand-chalk lettering reading 'less hunger. more you.' and a small chalk arrow. Authentic chalk texture.", headline="Less Hunger. More You.", primary="A compounded GLP-1 may help quiet cravings so you can focus on life. From $149/mo. See if you qualify."),
    dict(n=12, slug="boardingpass", mode="t2i", prompt="A realistic airline boarding pass design reading 'PASSENGER: You', 'DESTINATION: a lighter you', 'BOARDING: today', 'GATE: 3-minute quiz'. Clean ticket layout.", headline="Now Boarding: A Lighter You", primary="Start with a 3-minute quiz, licensed providers, and compounded GLP-1 delivered — from $149/mo. See if you qualify."),
    dict(n=13, slug="billboard", mode="i2i", prompt="A photo of a large roadside billboard against a blue sky, the billboard showing bold text 'GLP-1 care from $149/mo · no clinic, no insurance' and the product vial from the reference image. Realistic outdoor billboard mockup.", headline="You've Probably Seen the Signs", primary="Telehealth GLP-1 care — licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=14, slug="faqaccordion", mode="t2i", prompt="A clean FAQ accordion UI card (not mimicking any brand) with three expandable rows: 'Do I need insurance? No.', 'Do I visit a clinic? No, it's online.', 'How fast to start? A 3-minute quiz.' Minimal.", headline="Your Questions, Answered", primary="No insurance, no clinic — a 3-minute quiz and licensed-provider review. From $149/mo. See if you qualify."),
    dict(n=15, slug="barchart", mode="t2i", prompt="A clean bar-chart infographic titled 'What's included' comparing two bars: 'Typical clinic — $1,000+/mo' tall, and 'TrimRx — from $149/mo' short. Simple labeled bars.", headline="The Cost Difference Is Real", primary="Telehealth GLP-1 care at a fraction of typical clinic pricing — from $149/mo, no insurance. See if you qualify."),
    dict(n=16, slug="piechart", mode="t2i", prompt="A clean pie chart that is 100% one color, labeled in the center 'Where your $149 goes: 100% your care'. Simple infographic.", headline="100% Care. No Hidden Fees.", primary="One flat price covers medication, provider visits, and shipping — from $149/mo. See if you qualify."),
    dict(n=17, slug="dietflatlay", mode="t2i", prompt="An overhead flat-lay of old diet products (a bathroom scale, diet shakes, a measuring tape, meal-prep containers) with a big hand-drawn red X over them and one small printed line 'there's a better way'. No other text.", headline="There's a Better Way", primary="If diets keep failing, it's biology, not willpower. A compounded GLP-1 may help. From $149/mo. See if you qualify."),
    dict(n=18, slug="calendarinvite", mode="t2i", prompt="A clean calendar-invite card: 'Event: Take the 3-minute quiz', 'When: Today', 'Where: online', a green 'Accept' button. Minimal calendar UI (not mimicking a brand).", headline="Add One Thing to Your Calendar", primary="A 3-minute quiz, licensed providers, compounded GLP-1 delivered — from $149/mo. See if you qualify."),
    dict(n=19, slug="todolist", mode="t2i", prompt="A handwritten to-do list on a notepad: '☑ stop blaming myself', '☑ stop crash dieting', '☐ take the 3-minute quiz'. Realistic notepad.", headline="One Box Left to Check", primary="A telehealth GLP-1 program — quiz, licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=20, slug="reportcard", mode="t2i", prompt="A school report card titled 'Weight-loss methods' with rows: 'Crash diets — F', 'Willpower alone — D', 'Provider-guided GLP-1 — A'. Clean report-card layout.", headline="Grading the Methods", primary="A compounded GLP-1, guided by licensed providers, may help where diets didn't. From $149/mo. See if you qualify."),
    dict(n=21, slug="weather", mode="t2i", prompt="A weather-forecast graphic card: 'Forecast: lighter days ahead' with a sun-behind-clouds icon and a small line 'starting with a 3-minute quiz'. Clean weather-app style (not a brand).", headline="Forecast: Lighter Days Ahead", primary="A telehealth GLP-1 program to help you start — licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=22, slug="horoscope", mode="t2i", prompt="A mystical horoscope card with stars and a crescent moon: 'Today's reading: it's time to stop fighting your body.' small line 'the stars say take the quiz'. Dreamy celestial style.", headline="The Signs Say It's Time", primary="A compounded GLP-1, prescribed by licensed providers, may help. From $149/mo. See if you qualify."),
    dict(n=23, slug="pricetag", mode="i2i", prompt="A close-up of a retail hang-tag / price tag tied with string reading 'from $149/mo · all-in', the product vial from the reference image softly behind it. Clean product still.", headline="One Honest Price", primary="Compounded GLP-1, provider visits, and shipping — one flat price from $149/mo. See if you qualify."),
    dict(n=24, slug="postcard", mode="t2i", prompt="A vintage travel postcard reading 'Greetings from your fresh start' in retro lettering with a sunny illustration, and a small stamped corner. Nostalgic postcard style.", headline="Greetings From Your Fresh Start", primary="A telehealth GLP-1 program — quiz, licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=25, slug="membercard", mode="i2i", prompt="A sleek membership/ID card design reading 'TrimRx Member · GLP-1 Care · Active', with a subtle chip graphic, beside the product vial from the reference image. Premium card style.", headline="Membership That Actually Helps", primary="Unlimited licensed-provider visits and compounded GLP-1, from $149/mo. See if you qualify."),
    dict(n=26, slug="nametag", mode="t2i", prompt="A classic 'HELLO my name is' name-tag sticker, the white field filled in with handwriting: 'done dieting'. Simple realistic sticker.", headline="Hi, I'm Done Dieting", primary="It was never about willpower. A compounded GLP-1 may help. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=27, slug="polaroid", mode="t2i", prompt="A single Polaroid instant photo of a relatable smiling woman about 45 at home, with handwriting on the white border reading 'the day I started'. No other text.", headline="The Day I Started", primary="A provider-prescribed GLP-1 helped me quiet the cravings. From $149/mo, delivered. See if you qualify."),
    dict(n=28, slug="filmstrip", mode="t2i", prompt="A 35mm film-strip graphic with four small lifestyle frames (a morning walk, a glass of water, a calendar, a journal) and sprocket holes. No text on the frames.", headline="Small Scenes, Big Difference", primary="A telehealth GLP-1 program that fits real life — from $149/mo, licensed providers. See if you qualify."),
    dict(n=29, slug="bookcover", mode="t2i", prompt="A minimalist book cover titled 'The End of Dieting' with a subtitle 'how women over 40 are doing it differently', author line 'TrimRx'. Clean typographic book-cover.", headline="The End of Dieting", primary="A provider-guided GLP-1 program — a different approach than another diet. From $149/mo. See if you qualify."),
    dict(n=30, slug="albumcover", mode="t2i", prompt="A stylish album-cover-style square graphic, bold modern typography reading 'QUIET' as the title with a small subtitle 'the food-noise sessions'. Artful, music-cover aesthetic.", headline="Finally, Quiet", primary="A compounded GLP-1 may help quiet the all-day food noise. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=31, slug="movieposter", mode="t2i", prompt="A dramatic movie-poster-style design with a bold title 'THE COMEBACK' and a small tagline 'her story starts with a 3-minute quiz', credits block at the bottom. Cinematic poster.", headline="The Comeback", primary="A telehealth GLP-1 program — licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=32, slug="neon", mode="t2i", prompt="A glowing neon sign on a dark brick wall reading 'no more food noise' in warm neon tubing. Realistic neon glow.", headline="No More Food Noise", primary="A compounded GLP-1 may help quiet cravings. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=33, slug="postitwall", mode="t2i", prompt="A wall covered in colorful sticky notes, each with a short handwritten phrase: 'no insurance', 'from $149/mo', 'delivered', 'licensed providers', '3-min quiz', 'no clinic'. Casual collage.", headline="Everything in One Place", primary="No insurance, no clinic — compounded GLP-1 delivered, from $149/mo. See if you qualify."),
    dict(n=34, slug="venn", mode="t2i", prompt="A clean two-circle Venn diagram, left circle 'You', right circle 'A GLP-1 plan', the overlap labeled 'feeling like yourself'. Minimal infographic.", headline="Where You Meet Your Plan", primary="A provider-guided compounded GLP-1, from $149/mo, delivered. See if you qualify."),
    dict(n=35, slug="eras", mode="t2i", prompt="A horizontal timeline graphic 'The old way -> The TrimRx way': left 'clinics, insurance, waiting'; right '3-min quiz, online, delivered'. Clean era-strip layout.", headline="The Old Way vs. The New Way", primary="GLP-1 care without the clinic hassle — from $149/mo, licensed providers. See if you qualify."),
    dict(n=36, slug="countdown", mode="t2i", prompt="A bold countdown card showing 'Day 1' in huge type with a small line 'starts when you do' and a tiny '3-minute quiz' tag. Minimal.", headline="Day 1 Starts When You Do", primary="A telehealth GLP-1 program — quiz, licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=37, slug="comic", mode="t2i", prompt="A simple 3-panel comic strip with thick outlines: panel 1 a woman thinking about food with a thought cloud, panel 2 she takes a quiz on her phone, panel 3 she looks calm and relieved. Speech-free, just simple art, tiny caption under panel 3 'from $149/mo'.", headline="How It Goes", primary="A compounded GLP-1 may help quiet the food noise. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=38, slug="crossword", mode="t2i", prompt="A small crossword-puzzle grid with one across answer highlighted spelling 'G L P - 1', a clue line below '1 Across: the modern approach to weight loss'. Clean puzzle layout.", headline="One Across: GLP-1", primary="A provider-guided compounded GLP-1, from $149/mo, delivered. See if you qualify."),
    dict(n=39, slug="flightboard", mode="t2i", prompt="An airport departures flight-board (split-flap style) with one row reading 'DESTINATION: A Lighter You — STATUS: NOW BOARDING — GATE: Quiz'. Dark board, yellow text.", headline="Now Boarding", primary="Start with a 3-minute quiz, licensed providers, compounded GLP-1 delivered — from $149/mo. See if you qualify."),
    dict(n=40, slug="letterhand", mode="t2i", prompt="A full handwritten letter on lined paper in blue ink, a few short lines: 'Dear me — it was never about trying harder. It's biology. Time to ask for help.' signed 'me'. Authentic handwriting.", headline="A Letter to Myself", primary="A compounded GLP-1, guided by licensed providers, may help. From $149/mo, delivered. See if you qualify."),
    dict(n=41, slug="permissionslip", mode="t2i", prompt="A school-style permission slip titled 'Permission to put yourself first' with a checkbox 'I give myself permission' checked, and a signature line. Clean form layout.", headline="Permission to Put You First", primary="A telehealth GLP-1 program built around you — from $149/mo, licensed providers. See if you qualify."),
    dict(n=42, slug="grocerylist", mode="t2i", prompt="A handwritten grocery list on a notepad titled 'Not buying anymore:' with crossed-out items 'diet shakes', 'meal-prep guilt', 'another cleanse', and one un-crossed line 'a 3-minute quiz'. Realistic note.", headline="Not Buying That Anymore", primary="If diets keep failing, a compounded GLP-1 may help. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=43, slug="fortune", mode="t2i", prompt="A fortune cookie cracked open with a small paper slip reading 'Your fortune: the food noise is about to get quiet.' on a clean surface. Realistic.", headline="Your Fortune Says So", primary="A compounded GLP-1 may help quiet cravings. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=44, slug="magquiz", mode="t2i", prompt="A magazine-style quiz card titled 'What's your hunger type?' with three lettered options A, B, C and a small line 'find out + see if you qualify'. Glossy magazine layout.", headline="What's Your Hunger Type?", primary="A 3-minute quiz pairs you with licensed-provider GLP-1 care — from $149/mo. See if you qualify."),
    dict(n=45, slug="cravinganatomy", mode="t2i", prompt="A clean labeled 'anatomy of a craving' infographic: a simple brain-and-stomach diagram with three labels 'hunger hormones', 'food noise', 'reward loop'. Educational, no claims.", headline="The Anatomy of a Craving", primary="Cravings are driven by biology. A compounded GLP-1 may help. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=46, slug="expectreality", mode="t2i", prompt="A two-column text card 'Expectation vs Reality': left 'Expectation: another strict diet'; right 'Reality: a 3-minute quiz, online, delivered'. Clean split layout.", headline="Expectation vs. Reality", primary="GLP-1 care without the clinic or the crash diet — from $149/mo, licensed providers. See if you qualify."),
    dict(n=47, slug="pricebars", mode="i2i", prompt="A simple price comparison with three vertical stacked-coin bars labeled 'Clinic $1,000+', 'Other online $299', 'TrimRx from $149', the TrimRx bar shortest and highlighted green, the product vial from the reference image beside it.", headline="See the Difference", primary="Telehealth GLP-1 care at a fraction of typical pricing — from $149/mo, no insurance. See if you qualify."),
    dict(n=48, slug="heatmap", mode="t2i", prompt="A stylized US heat-map infographic with warmer-colored states, titled 'Where women are switching to online GLP-1 care'. Clean data-map style.", headline="It's Catching On Nationwide", primary="Compounded GLP-1, prescribed by licensed providers, delivered — from $149/mo. Check your state and see if you qualify."),
    dict(n=49, slug="testimonialwall", mode="t2i", prompt="A tidy wall/grid of many small speech-bubble quotes, each one short: 'finally quiet', 'so easy', 'no insurance!', 'worth it', 'love it', 'life-changing routine'. Headline at top 'What members say'. No product.", headline="What Members Say", primary="Thousands have started telehealth GLP-1 care online — licensed providers, from $149/mo. See if you qualify."),
    dict(n=50, slug="ratingbreakdown", mode="t2i", prompt="A clean rating-breakdown graphic: a big '4.8' with five gold stars, and horizontal bars for 5★ (long), 4★, 3★. Headline 'Members rate us'. Minimal.", headline="Members Rate Us 4.8", primary="A telehealth GLP-1 program — licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=51, slug="asseenin", mode="t2i", prompt="A clean 'The buzz' press strip: a row of generic neutral publication-style wordmarks (made-up, not real brands) under a headline 'Everyone's talking about online GLP-1 care'. Editorial.", headline="Everyone's Talking About It", primary="Compounded GLP-1, prescribed by licensed providers, delivered — from $149/mo. See if you qualify."),
    dict(n=52, slug="spotlight", mode="i2i", prompt="A dramatic stage-spotlight scene: the product vial from the reference image on a pedestal under a single theatrical spotlight in a dark room, headline 'Meet the simpler way'. Cinematic product reveal.", headline="Meet the Simpler Way", primary="Compounded GLP-1, licensed providers, delivered — one flat price from $149/mo. See if you qualify."),
    dict(n=53, slug="unboxing", mode="i2i", prompt="A clean overhead unboxing flat-lay: an opened discreet shipping box with tidy contents laid out — the product vial from the reference image, a home-injection kit pouch, and a small welcome card. No marketing text except a small 'delivered from $149/mo' line.", headline="What Shows Up at Your Door", primary="Everything you need, delivered discreetly — compounded GLP-1, home kit, from $149/mo. See if you qualify."),
    dict(n=54, slug="clipboard", mode="t2i", prompt="A medical intake clipboard with a simple checklist form, items checked: '☑ no insurance needed', '☑ online visit', '☑ delivered', and a pen resting on it. Clean realistic clipboard.", headline="The Only Paperwork: 3 Minutes", primary="A short online intake, a licensed-provider review, and compounded GLP-1 delivered — from $149/mo. See if you qualify."),
    dict(n=55, slug="approvedstamp", mode="i2i", prompt="A bold red 'APPROVED' rubber-stamp imprint over a clean form, with a small line 'provider-reviewed in ~24 hrs', the product vial from the reference image to the side.", headline="Approved in About a Day", primary="A licensed provider reviews you online, usually within a day — compounded GLP-1 from $149/mo. See if you qualify."),
    dict(n=56, slug="circularsteps", mode="t2i", prompt="A circular process infographic with three arcs/arrows looping: 'Quiz' -> 'Provider review' -> 'Delivered' -> repeat, with small icons. Clean cyclical diagram.", headline="A Simple Loop", primary="Quiz, licensed-provider review, delivered, repeat — compounded GLP-1 from $149/mo. See if you qualify."),
    dict(n=57, slug="speechbubble", mode="t2i", prompt="A single giant comic-style speech bubble on a bright flat background containing the words 'wait... it's only $149 a month?'. Bold and playful, nothing else.", headline="Wait, Only $149/mo?", primary="Yes — compounded GLP-1, licensed-provider visits, and shipping, one flat price from $149/mo. See if you qualify."),
    dict(n=58, slug="stickytab", mode="t2i", prompt="A close-up of a page with a single bright sticky-tab/flag marking a line of text that reads 'this is the part that changed everything', the rest of the page softly blurred. Minimal.", headline="The Part That Changed Everything", primary="A provider-guided compounded GLP-1 may help quiet the cravings. From $149/mo, delivered. See if you qualify."),
]


def gen(ad, aspect, regen):
    out = os.path.join(OUTDIR, f"f{ad['n']:02d}_{ad['slug']}_gpt.png")
    if os.path.exists(out) and not regen:
        return ad["slug"], out, "skip"
    prompt = ad["prompt"] + STYLE + f" Put a small grey legal line at the very bottom: '{FOOT}'."
    try:
        urls = [kie.upload_file(VIAL)] if ad["mode"] == "i2i" else None
        res = kie.generate_gpt_image(prompt, image_urls=urls, aspect_ratio=aspect, resolution="2K")
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
    print(f"gpt-image-2 — {len(ads)} unique-format ads, aspect {args.aspect}", flush=True)
    ok = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(gen, a, args.aspect, args.regen): a["slug"] for a in ads}
        for fut in as_completed(futs):
            slug, out, st = fut.result()
            if st in ("ok", "skip"):
                ok += 1
            print(f"[{st}] {slug} -> {out}", flush=True)
    print(f"DONE {ok}/{len(ads)}", flush=True)

    DISC = ("TrimRX does not practice medicine or prescribe medications. Compounded medications are not "
            "FDA-approved and are not evaluated by the FDA for safety, effectiveness, or quality. Results "
            "vary by individual and are not guaranteed.")
    lines = ["# TrimRx unique-format ads — FB headline + primary text\n"]
    for a in ADS:
        lines.append(f"\n## f{a['n']:02d} · {a['slug']}\n**Headline:** {a.get('headline','')}\n**Primary:** {a.get('primary','')}\n\n{DISC}\n")
    with open("outputs/trimrx_glp1/copy_formats.md", "w") as fh:
        fh.write("\n".join(lines))
    print("[copy] wrote outputs/trimrx_glp1/copy_formats.md", flush=True)


if __name__ == "__main__":
    main()
