"""TrimRx — 60 MORE ads spanning unique angles + personas + styles (full gpt-image-2 banners).

Combined with the existing 43 (v01-10 viral, s01-20 styles, 30g compare, c01-12 clean) this brings
the library past 100, every ad a different angle/persona/look. All compliant: NO brand names, NO
equivalence/guarantee/clinically/FDA, NO before-after, NO fake doctors; mandatory footnote on each.
i2i = real vial reference; t2i = clean photo/persona (no vial).

Run: .venv/bin/python scripts/trimrx_angles.py        (--only <slug,slug>   --workers 4)
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

OUTDIR = "outputs/trimrx_glp1/final"
VIAL = "outputs/trimrx_glp1/product/vial_gip_blue.png"
FOOT_EN = "Compounded medication. Requires prescription. Not FDA-approved. Individual results vary."
FOOT_ES = "Medicamento compuesto. Requiere receta. No aprobado por la FDA. Los resultados varían."
STYLE = (" Render as ONE attention-grabbing social-media banner, BOLD large correctly-spelled typography, "
         "strong composition, premium and modern. Render ONLY the text specified above — do NOT invent extra "
         "copy. NO brand names (no Ozempic, Wegovy, Mounjaro, Zepbound), NO 'same as / identical / generic', "
         "NO 'guaranteed / proven / clinically proven / FDA-approved', NO before-and-after imagery, NO fake "
         "doctors. People shown are everyday relatable patients, not models, with natural real skin. Where a "
         "vial appears, match the reference (clear glass vial, 'GLP-1' label, RX ONLY, Dose Varies).")

# n, slug, mode, prompt, headline (FB), primary (FB), [foot]
ADS = [
    # ---- Women 40+ / perimenopause ----
    dict(n=1, slug="meno_hero", mode="t2i", prompt=(
        "A warm lifestyle photo of a relatable woman about 47 at home in soft daylight, calm and hopeful. "
        "Bold lower-third headline 'Menopause changed your metabolism.' and a second line 'A GLP-1 plan can "
        "help you respond.' Small line 'From $149/mo · prescribed online'."),
        headline="Weight Loss That Understands Menopause",
        primary="Hormones and metabolism shift in your 40s and the old tricks stop working. A provider-guided compounded GLP-1 may help. From $149/mo, no insurance. See if you qualify."),
    dict(n=2, slug="meno_statement", mode="t2i", prompt=(
        "A clean minimalist statement card, plain warm taupe background, one bold line centered: 'Your body "
        "after 40 plays by new rules.' a smaller line beneath: 'So should your approach.' No product."),
        headline="Your Body After 40 Plays By New Rules",
        primary="Perimenopause changes how your body holds weight. A compounded GLP-1 program, guided by licensed providers, may help you respond. From $149/mo. See if you qualify."),
    dict(n=3, slug="meno_news", mode="t2i", prompt=(
        "A documentary news-style photo of a woman about 48 in a kitchen, news-segment feel. One clean white "
        "lower title: 'Why GLP-1 is becoming the go-to for women over 40.' No price, no button, no product."),
        headline="The Over-40 Weight-Loss Shift",
        primary="More women over 40 are turning to telehealth GLP-1 care — licensed providers, delivered, from $149/mo, no insurance. See if you qualify in 3 minutes."),
    dict(n=4, slug="meno_review", mode="i2i", prompt=(
        "A clean review card: five gold stars, a bold quote 'For the first time since my 40s, the cravings "
        "are quiet.' name 'Donna M. — verified member'. The product vial from the reference image. Green "
        "button 'See if you qualify'. Small line 'from $149/mo'."),
        headline="Quiet Cravings, Finally", primary="A compounded GLP-1, prescribed by licensed providers, may help quiet the all-day food noise. From $149/mo, delivered, no insurance. See if you qualify."),
    # ---- Women 50+ ----
    dict(n=5, slug="fifties_reinvention", mode="t2i", prompt=(
        "A confident, warm lifestyle photo of a woman about 55 (relatable, natural), bright airy setting. "
        "Bold headline 'Your 50s can feel different.' Small line 'Compounded GLP-1 · from $149/mo'."),
        headline="Your 50s Can Feel Different",
        primary="It's never too late to feel like yourself. A provider-guided GLP-1 program may help. From $149/mo, delivered, no insurance needed. See if you qualify."),
    dict(n=6, slug="fifties_luxe", mode="i2i", prompt=(
        "A luxe premium banner: matte-black background, thin gold accents, elegant serif headline 'A reset "
        "for your next chapter.' The product vial from the reference image lit dramatically. Gold button "
        "'See if you qualify'. Small gold line 'Compounded GLP-1 · from $149/mo'."),
        headline="A Reset for Your Next Chapter",
        primary="Provider-prescribed compounded GLP-1, delivered to your door, from $149/mo — no insurance, no clinic. See if you qualify."),
    # ---- Men ----
    dict(n=7, slug="men_hero", mode="t2i", prompt=(
        "A relatable everyday man about 45 (average build, natural) in a kitchen or garage, candid daylight. "
        "Bold headline 'Dads, this one is for you.' Small line 'Compounded GLP-1 · from $149/mo · online'."),
        headline="Dads, This One's For You",
        primary="Busy, no time for a clinic, weight creeping up? A telehealth GLP-1 program — licensed providers, delivered, from $149/mo. See if you qualify in 3 minutes."),
    dict(n=8, slug="men_busy", mode="t2i", prompt=(
        "A documentary photo of a man about 48 checking his phone on a work break, realistic. Bold headline "
        "'No time for a clinic? It is all online.' Small line 'GLP-1 · from $149/mo'."),
        headline="No Time for a Clinic?",
        primary="A 3-minute quiz, a licensed provider's review online, and compounded GLP-1 delivered — from $149/mo, no insurance. See if you qualify."),
    dict(n=9, slug="men_comparison", mode="i2i", prompt=(
        "A bold comparison banner aimed at men, dark navy: headline 'Stop overpaying for your meds.' Two "
        "rows: 'Local clinic — $1,000+/mo' with a red X, 'TrimRx — from $279/mo' with a green check. The "
        "product vial from the reference image. Green button 'See if you qualify'."),
        headline="Stop Overpaying for Your GLP-1",
        primary="Telehealth GLP-1 care at a fraction of typical clinic pricing — licensed providers, delivered, tirzepatide from $279/mo. See if you qualify."),
    dict(n=10, slug="men_stat", mode="t2i", prompt=(
        "A clean single-stat card, deep slate background, huge white '300,000+' and a line 'started online — "
        "no clinic, no insurance'. No product."),
        headline="Join 300,000+ Who Started Online",
        primary="A telehealth GLP-1 program, prescribed by licensed providers, delivered, from $149/mo. See if you qualify in 3 minutes."),
    # ---- Busy moms ----
    dict(n=11, slug="mom_notime", mode="t2i", prompt=(
        "A warm candid photo of a busy mom about 38 in a messy-real kitchen, relatable. Bold headline "
        "'Between the kids and work, who has time for a clinic?' Small line 'GLP-1 · 100% online · $149/mo'."),
        headline="Who Has Time for a Clinic?",
        primary="Between the kids and everything else, a clinic visit isn't happening. A 3-minute quiz, licensed providers, delivered — from $149/mo. See if you qualify."),
    dict(n=12, slug="mom_mirror", mode="t2i", prompt=(
        "An authentic candid mirror selfie of an ordinary mom about 39 in casual clothes, real and unposed, "
        "natural light, no text anywhere."),
        headline="I Did It for Me This Time",
        primary="After years of putting everyone else first, I finally started. A provider-prescribed GLP-1, delivered, from $149/mo, no insurance. See if you qualify."),
    dict(n=13, slug="mom_journal", mode="t2i", prompt=(
        "A handwritten journal page, ruled paper, blue-ink handwriting 'note to self: it's okay to take care "
        "of me too.' a small doodled heart. A small printed line 'Compounded GLP-1 · from $149/mo · trimrx'."),
        headline="It's Okay to Take Care of You Too",
        primary="A telehealth GLP-1 program built for real life — quiz, licensed providers, delivered, from $149/mo. See if you qualify in 3 minutes."),
    # ---- PCOS ----
    dict(n=14, slug="pcos_questions", mode="t2i", prompt=(
        "A clean question-stack card on deep teal: title 'Living with PCOS?' then questions 'Why is losing "
        "weight so much harder?' 'Is it insulin resistance?' 'Could a GLP-1 plan help?' Bottom 'Take the "
        "3-minute quiz'. No product."),
        headline="PCOS Makes Weight Loss Harder",
        primary="If PCOS has made weight loss feel impossible, a provider-guided GLP-1 program may help. From $149/mo, no insurance. See if you qualify in 3 minutes."),
    dict(n=15, slug="pcos_story", mode="t2i", prompt=(
        "An authentic candid photo of a relatable woman about 33 at home, natural and real, no text."),
        headline="PCOS Made It Feel Impossible",
        primary="With PCOS, every diet felt useless. A compounded GLP-1, prescribed by a licensed provider, finally helped. From $149/mo, delivered. See if you qualify."),
    dict(n=16, slug="pcos_signs", mode="t2i", prompt=(
        "A clean text card on soft lavender: title 'Signs PCOS may be working against you:' short list "
        "'Stubborn weight gain', 'Constant hunger', 'Diets that stop working'. No product."),
        headline="Is PCOS Working Against You?",
        primary="These can be signs your body needs more support than willpower. A provider-guided GLP-1 may help. From $149/mo. See if you qualify."),
    # ---- Postpartum ----
    dict(n=17, slug="postpartum_story", mode="t2i", prompt=(
        "A warm, gentle candid photo of a relatable woman about 34 at home, tired but hopeful, real, no text."),
        headline="After the Baby, It Wouldn't Budge",
        primary="If the weight hasn't come off the way you hoped, you're not alone. Talk to a licensed provider about a compounded GLP-1 — from $149/mo, delivered. See if you qualify."),
    dict(n=18, slug="postpartum_letter", mode="t2i", prompt=(
        "A calm open-letter text card, soft cream background, message 'Your body did something amazing. "
        "Wanting to feel like you again is okay too.' signature '— the TrimRx team'. No product."),
        headline="Wanting to Feel Like You Again Is Okay",
        primary="A telehealth GLP-1 program, guided by licensed providers, may help. From $149/mo, no insurance, delivered. See if you qualify."),
    # ---- Professional / executive ----
    dict(n=19, slug="exec_online", mode="t2i", prompt=(
        "A polished but real professional woman about 42 at a desk with a laptop, natural. Bold headline "
        "'Your calendar's full. Your visit is online.' Small line 'GLP-1 · from $149/mo'."),
        headline="Your Calendar's Full. Your Visit Is Online.",
        primary="Skip the waiting room. A licensed provider reviews you online and your compounded GLP-1 ships to you — from $149/mo. See if you qualify."),
    dict(n=20, slug="exec_minimal", mode="i2i", prompt=(
        "An ultra-minimalist premium banner: the product vial from the reference image on a soft pale "
        "gradient, lots of negative space, a small elegant line 'Weight care that fits a busy life. From "
        "$149/mo.' tiny 'See if you qualify' link."),
        headline="Weight Care That Fits a Busy Life",
        primary="Compounded GLP-1, prescribed by licensed providers, delivered — one flat price from $149/mo, no insurance. See if you qualify."),
    # ---- Budget / affordability ----
    dict(n=21, slug="budget_real", mode="i2i", prompt=(
        "A bold banner, bright background: headline 'You don't need insurance or $1,000.' subline 'Compounded "
        "GLP-1 from $149/mo — everything included.' The product vial from the reference image. Green button "
        "'See if you qualify'."),
        headline="No Insurance? No $1,000 Bills.",
        primary="One flat price covers the medication, licensed-provider visits, and delivery — from $149/mo, no insurance. See if you qualify in 3 minutes."),
    dict(n=22, slug="budget_receipt", mode="i2i", prompt=(
        "A clean itemized receipt on white paper: header 'YOUR MONTHLY TOTAL', items 'GLP-1 medication .... "
        "included', 'Provider visits .... $0.00', 'Shipping .... $0.00', bold 'TOTAL: $149/mo'. The product "
        "vial from the reference image beside it. Small button 'See if you qualify'."),
        headline="Everything Included for $149/mo",
        primary="No surprise fees: medication, unlimited licensed-provider visits, and shipping, all in one flat price from $149/mo. See if you qualify."),
    dict(n=23, slug="budget_pricebig", mode="i2i", prompt=(
        "A bold price-hero banner: huge '$149' with '/mo' and a line 'all-in · no insurance needed'. The "
        "product vial from the reference image. Green button 'See if you qualify'."),
        headline="From $149/mo, All-In",
        primary="Compounded GLP-1, licensed providers, delivery — one flat price from $149/mo. See if you qualify."),
    # ---- Plus-size / tried everything ----
    dict(n=24, slug="plus_tried", mode="t2i", prompt=(
        "A relatable plus-size woman about 41 in fitted activewear at home, hopeful, natural fuller body. "
        "Bold headline 'Tried every diet?' second line 'It may not be willpower.' Small line 'GLP-1 · $149/mo'."),
        headline="Tried Every Diet?",
        primary="If diets keep failing, it's biology, not willpower. A compounded GLP-1, guided by licensed providers, may help. From $149/mo. See if you qualify."),
    dict(n=25, slug="plus_split", mode="t2i", prompt=(
        "A split banner: top half a relatable plus-size woman about 44 looking hopeful; bottom half a teal "
        "block with bold white headline 'Your weight-loss journey, made simple.' Small line 'GLP-1 · from "
        "$149/mo'. Green button 'See if you qualify'."),
        headline="Your Weight-Loss Journey, Made Simple",
        primary="A 3-minute quiz, licensed providers, and compounded GLP-1 delivered — from $149/mo, no insurance. See if you qualify."),
    dict(n=26, slug="plus_letter", mode="t2i", prompt=(
        "A calm open-letter text card, warm off-white: 'To anyone who's tried everything — it was never "
        "about trying harder.' signature '— the TrimRx team'. No product."),
        headline="It Was Never About Trying Harder",
        primary="A compounded GLP-1 program works with your biology, not against your willpower. From $149/mo, delivered. See if you qualify."),
    # ---- Late-night / emotional eating ----
    dict(n=27, slug="cravings_night", mode="t2i", prompt=(
        "A relatable nighttime kitchen scene, dim warm light, a woman about 40 standing by an open fridge, "
        "candid and real. Bold headline 'It's 9pm and you're back in the kitchen.' Small line 'GLP-1 · $149/mo'."),
        headline="It's 9pm and You're Back in the Kitchen",
        primary="Late-night cravings aren't a willpower problem — they're biology. A compounded GLP-1 may help quiet them. From $149/mo. See if you qualify."),
    dict(n=28, slug="cravings_statement", mode="t2i", prompt=(
        "A clean statement card, deep plum background, one bold white line 'The food noise. You know the one.' "
        "smaller line 'A GLP-1 can help quiet it.' No product."),
        headline="The Food Noise. You Know the One.",
        primary="That constant mental chatter about food is biology. A compounded GLP-1, prescribed by licensed providers, may help. From $149/mo. See if you qualify."),
    # ---- Plateau ----
    dict(n=29, slug="plateau_stuck", mode="t2i", prompt=(
        "A relatable woman about 43 looking thoughtfully at a window, natural. Bold headline 'Lost some — "
        "then stuck?' Small line 'A GLP-1 plan may help · from $149/mo'."),
        headline="Lost Some, Then Stuck?",
        primary="Plateaus are normal and frustrating. A provider-guided GLP-1 program may help you keep going. From $149/mo, delivered. See if you qualify."),
    # ---- Convenience / telehealth ----
    dict(n=30, slug="conv_steps", mode="i2i", prompt=(
        "A clean 3-step how-it-works banner: '1 Take the 3-min quiz  2 Meet your licensed provider  3 "
        "Delivered to your door'. The product vial from the reference image. Green button 'Start the quiz'. "
        "Small line 'from $149/mo'."),
        headline="Getting Started Takes 3 Minutes",
        primary="Quiz, licensed-provider review online, compounded GLP-1 delivered — from $149/mo, no insurance. See if you qualify."),
    dict(n=31, slug="conv_noclinic", mode="t2i", prompt=(
        "A warm photo of a woman about 45 relaxing on her couch with a phone, no waiting room. Bold headline "
        "'No clinic. No waiting room. No insurance.' Small line 'GLP-1 · from $149/mo'."),
        headline="No Clinic. No Waiting Room.",
        primary="Everything happens online: a quiz, a licensed provider, and medication at your door — from $149/mo. See if you qualify."),
    dict(n=32, slug="conv_doorstep", mode="t2i", prompt=(
        "A warm lifestyle photo of a discreet delivery box on a doorstep in golden light, no text anywhere."),
        headline="Care That Comes to You",
        primary="Skip the pharmacy lines. Compounded GLP-1, prescribed by licensed providers, delivered discreetly — from $149/mo. See if you qualify."),
    # ---- Science / education ----
    dict(n=33, slug="sci_howitworks", mode="i2i", prompt=(
        "A clean educational infographic: headline 'How a GLP-1 works with your body' with a simple body "
        "diagram and 3 points 'Slows digestion', 'Curbs appetite', 'Feel full longer'. The product vial from "
        "the reference image. Green button 'See if you qualify'."),
        headline="How a GLP-1 Works With Your Body",
        primary="A GLP-1 works in a similar way to your body's own hunger signals to help curb appetite. From $149/mo, provider-prescribed. See if you qualify."),
    dict(n=34, slug="sci_mythfact", mode="t2i", prompt=(
        "A clean myth-vs-fact card split into two halves: top (red) 'MYTH: It's just willpower.' bottom "
        "(green) 'FACT: Appetite is biology.' Small line 'A GLP-1 can help · from $149/mo'. No product."),
        headline="It Was Never Just Willpower",
        primary="Appetite is driven by biology, not discipline. A compounded GLP-1, guided by licensed providers, may help. From $149/mo. See if you qualify."),
    # ---- Social proof ----
    dict(n=35, slug="social_join", mode="i2i", prompt=(
        "A warm community banner: headline 'Join thousands of women who started online.' a row of small "
        "diverse smiling everyday women's circular photos. The product vial from the reference image. Green "
        "button 'See if you qualify'. Small line 'from $149/mo'."),
        headline="Join Thousands Who Started Online",
        primary="A telehealth GLP-1 program — licensed providers, delivered, from $149/mo, no insurance. See if you qualify in 3 minutes."),
    dict(n=36, slug="social_reviews", mode="t2i", prompt=(
        "A clean banner showing three short stacked 5-star review cards with names 'Maria', 'Dana', "
        "'Renee', each one short line like 'so easy', 'finally', 'worth it'. Headline 'Real members. Real "
        "reviews.' No product."),
        headline="Real Members. Real Reviews.",
        primary="Thousands have started a telehealth GLP-1 program online. Licensed providers, delivered, from $149/mo. See if you qualify."),
    # ---- Hispanic / Spanish ----
    dict(n=37, slug="es_hero", mode="t2i", foot=FOOT_ES, prompt=(
        "A warm lifestyle photo of a relatable Latina woman about 42 at home, natural. Bold Spanish headline "
        "'Baja de peso con un programa de GLP-1.' Small Spanish line 'Desde $149/mes · sin seguro'."),
        headline="Un programa de GLP-1, en español",
        primary="Programa de pérdida de peso por telesalud — médicos con licencia, entrega a domicilio, desde $149/mes, sin seguro. Ve si calificas."),
    dict(n=38, slug="es_price", mode="i2i", foot=FOOT_ES, prompt=(
        "A bold Spanish price banner: huge '$149/mes' and a line 'todo incluido · sin seguro'. The product "
        "vial from the reference image. Green button 'Ve si calificas'."),
        headline="GLP-1 desde $149/mes",
        primary="GLP-1 compuesto, recetado por médicos con licencia, entregado a tu puerta — desde $149/mes. Ve si calificas en 3 minutos."),
    dict(n=39, slug="es_review", mode="t2i", foot=FOOT_ES, prompt=(
        "A clean Spanish review card: five gold stars, quote 'Por fin dejé de pensar en comida todo el día.' "
        "name 'Lucia R. — miembro verificada'. Green button 'Ve si calificas'. Small line 'desde $149/mes'."),
        headline="Por fin, sin ansiedad por comida",
        primary="Un GLP-1 compuesto, recetado por médicos con licencia, puede ayudar. Desde $149/mes, entregado. Ve si calificas."),
    # ---- Confidence / energy / new chapter ----
    dict(n=40, slug="confidence_hero", mode="t2i", prompt=(
        "A fit, happy woman about 40 (someone doing well on her journey) walking outdoors, energetic, "
        "natural. Bold headline 'Feeling like myself again.' Small line 'GLP-1 · from $149/mo'."),
        headline="Feeling Like Myself Again",
        primary="A provider-prescribed GLP-1 helped me quiet the cravings and feel like me. From $149/mo, delivered. See if you qualify."),
    dict(n=41, slug="newchapter", mode="t2i", prompt=(
        "A cinematic film-still of a woman about 50 by a window in soft light, hopeful. Bold lower-third "
        "'This chapter is yours.' Small line 'GLP-1 · from $149/mo'."),
        headline="This Chapter Is Yours",
        primary="It's never too late to start. A telehealth GLP-1 program — licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=42, slug="energy_statement", mode="t2i", prompt=(
        "A clean statement card, bright background, bold line 'Less hunger. More energy for what matters.' No "
        "product. Small line 'GLP-1 · from $149/mo'."),
        headline="Less Hunger, More You",
        primary="A compounded GLP-1 may help quiet the food noise so you can focus on life. From $149/mo, provider-prescribed. See if you qualify."),
    # ---- Urgency / offer / bundle ----
    dict(n=43, slug="urgency_pricing", mode="i2i", prompt=(
        "A bold warm urgency banner: ribbon 'LIMITED NEW-PATIENT PRICING', huge 'From $149/mo', line 'all "
        "doses & shipping included'. The product vial from the reference image. Button 'Claim this price'."),
        headline="Limited New-Patient Pricing",
        primary="Lock in compounded GLP-1 care from $149/mo — licensed providers, delivered, no insurance. See if you qualify."),
    dict(n=44, slug="offer_bundle", mode="i2i", prompt=(
        "A clean value banner: headline 'Save more with a 3-month plan.' three small tiers '1 mo', '3 mo', "
        "'6 mo' with the 3-month highlighted 'most popular'. The product vial from the reference image. Green "
        "button 'See your options'. Small line 'GLP-1 · from $149/mo'."),
        headline="Save More With a Longer Plan",
        primary="Flexible plans — monthly or multi-month for bigger savings. Compounded GLP-1, licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=45, slug="warning_psa", mode="i2i", prompt=(
        "A pattern-interrupt PSA banner, dark: bold headline 'Before you pay $1,000+ for weight-loss care, "
        "read this.' subline 'A telehealth GLP-1 program starts at just $149/mo.' The product vial from the "
        "reference image. Green button 'See if you qualify'."),
        headline="Before You Pay $1,000+, Read This",
        primary="Telehealth GLP-1 care, prescribed by licensed providers and delivered, from $149/mo — no insurance. See if you qualify."),
    # ---- More personas / angles ----
    dict(n=46, slug="needlefear", mode="t2i", prompt=(
        "A reassuring warm photo of a woman about 38 holding a small home-injection pen calmly at a kitchen "
        "table, natural. Bold headline 'Easier than you think.' Small line 'Home kit included · GLP-1 · $149/mo'."),
        headline="Easier Than You Think",
        primary="A simple at-home routine with a home kit included and 24/7 support. Compounded GLP-1, from $149/mo. See if you qualify."),
    dict(n=47, slug="support_team", mode="t2i", prompt=(
        "A warm photo of a relatable woman about 45 smiling at her phone, supported feeling. Bold headline "
        "'You're not doing this alone.' Small line 'Unlimited provider visits · GLP-1 · $149/mo'."),
        headline="You're Not Doing This Alone",
        primary="Unlimited licensed-provider check-ins and 24/7 support, all included. Compounded GLP-1 from $149/mo. See if you qualify."),
    dict(n=48, slug="quiz_card", mode="t2i", prompt=(
        "A clean quiz card (NOT imitating any app UI): 'Question 1 of 3' progress bar, question 'Do cravings "
        "run your day?' buttons 'Yes' and 'Sometimes'. Green button 'Start the quiz'. Small line 'GLP-1 · "
        "from $149/mo'. No product."),
        headline="Do Cravings Run Your Day?",
        primary="A 3-minute quiz tells you whether a compounded GLP-1 program is a fit — reviewed by licensed providers. From $149/mo. See if you qualify."),
    dict(n=49, slug="checklist_included", mode="i2i", prompt=(
        "A clean checklist banner: headline 'Everything included' with green checks 'Provider visits', 'Free "
        "shipping', 'Free dose changes', 'Home kit', '24/7 support'. The product vial from the reference "
        "image. Green button 'See if you qualify'. Small line 'from $149/mo'."),
        headline="Everything's Included",
        primary="One flat price covers visits, shipping, dose changes, your home kit, and 24/7 support. Compounded GLP-1 from $149/mo. See if you qualify."),
    dict(n=50, slug="comparison_grid", mode="i2i", prompt=(
        "A clean feature comparison table: columns 'TrimRx', 'Local clinic', 'Doing nothing', rows 'Licensed "
        "providers', 'No insurance needed', 'Delivered', 'From $149/mo' — green checks for TrimRx, red X for "
        "others. The product vial from the reference image. Green button 'See if you qualify'."),
        headline="The Clearer Choice",
        primary="Licensed providers, no insurance, delivered, from $149/mo — versus the clinic hassle. See if you qualify."),
    dict(n=51, slug="vintage", mode="i2i", prompt=(
        "A vintage apothecary poster, cream/kraft, ornate serif headline 'Modern medicine. Old-fashioned "
        "care.' The product vial from the reference image styled like a remedy bottle. Small line "
        "'Provider-prescribed GLP-1 · from $149/mo'."),
        headline="Modern Medicine, Old-Fashioned Care",
        primary="Compounded GLP-1, prescribed by licensed providers, delivered with real human support — from $149/mo. See if you qualify."),
    dict(n=52, slug="popart", mode="i2i", prompt=(
        "A bold pop-art comic banner, halftone dots, thick outlines, a speech bubble 'No more food noise!' "
        "and a starburst 'FROM $149/mo'. The product vial from the reference image in pop-art style. Small "
        "line 'See if you qualify'."),
        headline="No More Food Noise!",
        primary="A compounded GLP-1 may help quiet the all-day cravings. Provider-prescribed, delivered, from $149/mo. See if you qualify."),
    dict(n=53, slug="duotone", mode="t2i", prompt=(
        "A bold duotone (teal-and-coral) portrait of a confident relatable woman about 43, bold white "
        "headline 'It finally clicked.' Small line 'GLP-1 · from $149/mo'. No product, design-forward."),
        headline="It Finally Clicked",
        primary="A compounded GLP-1, guided by licensed providers, helped the cravings finally quiet down. From $149/mo. See if you qualify."),
    dict(n=54, slug="ugc_hand", mode="i2i", prompt=(
        "An authentic UGC smartphone photo (shot-on-phone feel) of an ordinary woman's hand holding the "
        "product vial from the reference image in a real bathroom, casual caption 'this changed my whole "
        "routine' and a small line 'GLP-1 · from $149/mo · trimrx'."),
        headline="This Changed My Whole Routine",
        primary="A provider-prescribed GLP-1 delivered to my door, from $149/mo, no insurance. If you've tried everything, see if you qualify."),
    dict(n=55, slug="map_states", mode="i2i", prompt=(
        "A clean 'now available' banner with a stylized US map, a few states highlighted, headline 'Now "
        "available online across the U.S.' The product vial from the reference image. Green button 'Check "
        "your state'. Small line 'GLP-1 · from $149/mo'."),
        headline="Now Available Across the U.S.",
        primary="Compounded GLP-1, prescribed by licensed providers, delivered — from $149/mo, no insurance. Check your state and see if you qualify."),
    dict(n=56, slug="habit_tracker", mode="t2i", prompt=(
        "A clean habit-tracker calendar banner, 30-day grid with green checks, header 'YOUR FIRST 30 DAYS', "
        "headline 'Small steps. Real support.' Small line 'GLP-1 · from $149/mo'. No before-after, no "
        "weight numbers. No product."),
        headline="Small Steps. Real Support.",
        primary="A GLP-1 program that fits real life — quiz, licensed providers, delivered, from $149/mo. See if you qualify."),
    dict(n=57, slug="search_curiosity", mode="t2i", prompt=(
        "A clean stylized search-bar graphic on plain background, typed query 'GLP-1 weight loss without "
        "insurance?' with a magnifying-glass icon. Minimal, no logos. No product."),
        headline="GLP-1 Without Insurance?",
        primary="No insurance needed. A 3-minute quiz, licensed providers, and compounded GLP-1 delivered — from $149/mo. See if you qualify."),
    dict(n=58, slug="firstperson_candid", mode="t2i", prompt=(
        "An authentic candid photo of a relatable midsize woman about 46 at her kitchen table with coffee, "
        "real and warm, no text anywhere."),
        headline="I Stopped Blaming Myself",
        primary="For years I thought I lacked discipline. It was biology. A provider-prescribed GLP-1 helped — from $149/mo, delivered. See if you qualify."),
    dict(n=59, slug="minimal_premium", mode="i2i", prompt=(
        "An ultra-minimalist premium product hero: the product vial from the reference image centered on a "
        "soft pale-mint gradient, lots of negative space, a small elegant line 'Compounded GLP-1. From "
        "$149/mo.' tiny 'See if you qualify' link."),
        headline="Compounded GLP-1, Simplified",
        primary="Licensed-provider care, delivered, one flat price from $149/mo, no insurance. See if you qualify."),
    dict(n=60, slug="scene_jeans", mode="t2i", prompt=(
        "A quiet documentary still-life: a pair of folded jeans with a cloth tape measure on a softly lit "
        "bed, warm morning light, no people, no text anywhere."),
        headline="When Nothing Fits the Way It Used To",
        primary="If the jeans haven't fit in a while, it's not about willpower. A compounded GLP-1 may help — from $149/mo, delivered. See if you qualify."),
]


# Pure-photo candids: model must add ZERO text (it was inventing claim copy like "REAL RESULTS").
# Disclaimer for these lives in the FB primary text, not on the image.
NOTEXT_SLUGS = {"mom_mirror", "pcos_story", "postpartum_story", "conv_doorstep",
                "firstperson_candid", "scene_jeans"}


def gen(ad, aspect, regen):
    out = os.path.join(OUTDIR, f"a{ad['n']:02d}_{ad['slug']}_gpt.png")
    if os.path.exists(out) and not regen:
        return ad["slug"], out, "skip"
    if ad["slug"] in NOTEXT_SLUGS:
        prompt = (ad["prompt"] + " Absolutely NO text, no words, no letters, no numbers, no captions, no "
                  "logos, no watermark, no graphics anywhere in the image — it is a plain candid photograph "
                  "ONLY, with nothing written on it.")
    else:
        prompt = ad["prompt"] + STYLE + f" Put a small grey legal line at the very bottom: '{ad.get('foot', FOOT_EN)}'."
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
    print(f"gpt-image-2 — {len(ads)} angle/persona ads, aspect {args.aspect}", flush=True)
    ok = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(gen, a, args.aspect, args.regen): a["slug"] for a in ads}
        for fut in as_completed(futs):
            slug, out, st = fut.result()
            if st in ("ok", "skip"):
                ok += 1
            print(f"[{st}] {slug} -> {out}", flush=True)
    print(f"DONE {ok}/{len(ads)}", flush=True)

    # emit copy deck
    DISC = ("TrimRX does not practice medicine or prescribe medications. Compounded medications are not "
            "FDA-approved and are not evaluated by the FDA for safety, effectiveness, or quality. Results "
            "vary by individual and are not guaranteed.")
    lines = ["# TrimRx angle/persona ads — FB headline + primary text\n"]
    for a in ADS:
        lines.append(f"\n## a{a['n']:02d} · {a['slug']}\n**Headline:** {a.get('headline','')}\n")
        disc = "Medicamento compuesto..." if a.get("foot") == FOOT_ES else DISC
        lines.append(f"**Primary:** {a.get('primary','')}\n\n{disc}\n")
    with open("outputs/trimrx_glp1/copy_angles.md", "w") as fh:
        fh.write("\n".join(lines))
    print("[copy] wrote outputs/trimrx_glp1/copy_angles.md", flush=True)


if __name__ == "__main__":
    main()
