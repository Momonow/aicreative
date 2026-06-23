"""
IL JDC — 20 DISTINCT image ads (image-ad-formats system: format x style x angle).
10 UGC testimonial longforms (photoreal adult survivor + pull-quote; long FB primary) +
10 designed-format banners (full gpt-image-2 render with exact on-image text).

Grounded in the Depo image-ad dissection (inventory/depo_provera_ad_formats.md) + the longform
mold (inventory/depo_testimonials_copy.md). Compliance LOCKED for IL JDC:
  - "may/might qualify for significant compensation" (NEVER owed/paid/settlement/guaranteed)
  - explicit "sexually abused" + "juvenile detention center"; real facilities only
  - form CTA (name + number, ~30s, free, confidential, no court, no deadline)
  - NO disclaimer lingo anywhere (feedback_no_disclaimer_lingo_in_copy)
  - IMAGE SAFETY: never a minor/child/abuse/sexualized — adults now + empty institutional + text design

Run:  .venv/bin/python scripts/il_jdc_image_ads.py [--only <slug|n,...>] [--regen] [--workers 5]
                                                  [--provider kie|openai] [--dump]
Output: outputs/il_jdc_image_ads/<NN>_<slug>.png  (skip-if-exists)
Copy sheet (for AdMachin staging): outputs/il_jdc_image_ads/copy.json (via --dump)
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

OUT = Path("outputs/il_jdc_image_ads")
SUFFIX = (" Render ONLY the exact text specified — no extra words, headlines, claims, logos, "
          "watermarks, or disclaimers. No children, no minors, nothing sexual.")

# ---- shared persona realism tail for the UGC photoreal images ----
REAL = (" Photoreal candid documentary photo, shot-on-phone realism, plain everyday setting, natural "
        "imperfect skin with visible pores and lines, no makeup, no glamour, no retouching, an "
        "ordinary relatable adult. ")


def ugc_img(person, quote):
    """Build a UGC image prompt: a distinct adult + a clean readable on-image pull-quote band."""
    return (f"{person}{REAL}Large clean highly-readable text overlay reading EXACTLY: \"{quote}\" "
            f"set in a clear high-contrast band across the lower third, bold legible sans-serif." + SUFFIX)


ADS = [
    # ================= 10 UGC TESTIMONIAL LONGFORMS =================
    {
        "n": 1, "slug": "u1_survivor_confession", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, plain room",
        "angle": "Male survivor ~40 finally saying it out loud",
        "headline": "Were you abused in an Illinois juvie?",
        "pull_quote": "I never told anyone what happened in there.",
        "primary": (
            "I was fourteen the first time I got locked up. Cook County. Scared out of my mind, "
            "just trying to do my time and go home.\n\n"
            "A staff member sexually abused me in there. I never told anyone. Who was going to "
            "believe a kid over a guard?\n\n"
            "I carried that by myself for almost thirty years. Told myself it was my fault. Told "
            "myself to forget it.\n\n"
            "Then I found out I wasn't the only one. Nearly a thousand of us are suing the state of "
            "Illinois for what happened in those juvenile detention centers.\n\n"
            "If a staff member sexually abused you when you were locked up in an Illinois juvenile "
            "detention center, you may qualify for significant compensation.\n\n"
            "You don't need a police report. It doesn't matter how long ago it was — there's no "
            "deadline. It's free, it's completely confidential, and you never set foot in a courtroom.\n\n"
            "It took me thirty years to say it out loud. It'll take you about thirty seconds to check. "
            "If this was you, you're not alone. 👇 Tap below — just your name and number."),
        "image_prompt": ugc_img(
            "A Black man about 40, short hair, light beard, plain dark t-shirt, sitting on a couch in a "
            "modest living room, serious and quiet, looking into a phone camera held at arm's length. ",
            "I never told anyone what happened in there."),
    },
    {
        "n": 2, "slug": "u2_brother", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, porch/car",
        "angle": "Man ~38 speaking for his younger brother",
        "headline": "Your brother came back from juvie different?",
        "pull_quote": "My little brother came home a different person.",
        "primary": (
            "My little brother got locked up in an Illinois juvenile center when he was fifteen. He "
            "came home a different person and never told anyone why.\n\n"
            "For years I thought he was just angry. Just troubled. We all did.\n\n"
            "Last year he finally told me. A staff member sexually abused him in there. He'd carried "
            "it alone the whole time, because who believes a kid over a guard?\n\n"
            "He's not the only one. Nearly a thousand people are suing the state of Illinois for what "
            "happened to them in those juvenile detention centers.\n\n"
            "If somebody you love came back from an Illinois juvie and shut down, this might be why — "
            "and they may qualify for significant compensation.\n\n"
            "It's free to check, completely confidential — nobody in your life has to know. No police "
            "report, no court, and no deadline, no matter how long ago it was.\n\n"
            "My brother took thirty seconds to put in his name and number. It was the first time in "
            "years he let himself believe it wasn't his fault. If this is your brother, your son, or "
            "you — 👇 tap below."),
        "image_prompt": ugc_img(
            "A Black man about 38 with a short beard and a maroon t-shirt, sitting on a front porch step "
            "in daylight, protective and steady, talking into a phone held at arm's length. ",
            "My little brother came home a different person."),
    },
    {
        "n": 3, "slug": "u3_cousins_audy", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, parked car",
        "angle": "Two cousins, Audy Home, abused years apart",
        "headline": "Locked up at the Audy Home as a kid?",
        "pull_quote": "Same place. Same kind of staff.",
        "primary": (
            "Me and my cousin were both locked up at the Audy Home — Cook County juvenile detention — "
            "years apart. Same place, same kind of staff.\n\n"
            "We both got sexually abused in there. We didn't tell each other until last year. We "
            "didn't tell anyone for years, because back then, nobody believed a kid over a guard.\n\n"
            "Turns out it's nearly a thousand of us now, suing the state of Illinois for what happened "
            "in those juvenile centers.\n\n"
            "We may both qualify for significant compensation. There's no deadline in Illinois — it "
            "doesn't matter how long ago it was.\n\n"
            "It's free to find out, it's confidential, and you never go to court. No old paperwork, no "
            "police report. About thirty seconds.\n\n"
            "If it hit two people in my family, it hit somebody in yours. If you were sexually abused "
            "as a kid in an Illinois juvenile detention center, please — 👇 tap below and put in your "
            "name and number."),
        "image_prompt": ugc_img(
            "A Black man about 35, bald with light stubble, charcoal hoodie with the hood down, sitting "
            "in the driver's seat of a parked car, calm but heavy, looking into a phone camera. ",
            "Same place. Same kind of staff."),
    },
    {
        "n": 4, "slug": "u4_almost_scrolled", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, bedroom",
        "angle": "Scroll-stopper — the facility name froze his thumb",
        "headline": "Locked up at St. Charles as a kid?",
        "pull_quote": "Then I saw the name of the place.",
        "primary": (
            "I almost scrolled right past this. My thumb was already moving.\n\n"
            "Then I saw the name of the place. Illinois Youth Center, St. Charles. That's where I got "
            "locked up when I was sixteen. So I stopped.\n\n"
            "A staff member sexually abused me in there. I never told a single soul. For twenty years "
            "I figured it was just something I had to live with.\n\n"
            "Then I read what they're actually doing about it. Nearly a thousand people are suing the "
            "state of Illinois over what happened to them in those juvenile detention centers.\n\n"
            "If that was you, you may qualify for significant compensation. It doesn't matter how long "
            "ago it was — there's no deadline. It's free, it's confidential, and nobody in your life "
            "has to know.\n\n"
            "It took me about thirty seconds. If you were in there too, stop scrolling like I almost "
            "did. 👇 Tap below — just your name and number."),
        "image_prompt": ugc_img(
            "A Black man about 42, short afro, plain white t-shirt, sitting on the edge of a bed in a "
            "plain room, low-key and reluctant, talking into a phone held at arm's length. ",
            "Then I saw the name of the place."),
    },
    {
        "n": 5, "slug": "u5_no_deadline", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, kitchen, older man",
        "angle": "Myth-buster — decades ago, still counts",
        "headline": "Think it was too long ago? It still counts.",
        "pull_quote": "I figured it was too late. It wasn't.",
        "primary": (
            "What happened to me in juvie was over thirty years ago. When I first heard people were "
            "doing something about it, I figured that ship had sailed for me. Too late. I almost "
            "closed the page.\n\n"
            "I'm glad I didn't. Because that's not how it works.\n\n"
            "I was locked up in an Illinois juvenile center as a kid, and a staff member sexually "
            "abused me in there. I spent a long time telling myself it was too long ago to matter.\n\n"
            "It's not. There's no deadline in Illinois. People who were sexually abused in those "
            "juvenile detention centers decades ago may still qualify for significant compensation.\n\n"
            "Nearly a thousand of us are coming forward now. You don't need a police report. You don't "
            "need a pile of records. It's free, it's private, and you never go to court.\n\n"
            "If you've been telling yourself it's too late — please, just check. It might not be. It "
            "took me thirty seconds. 👇 Tap below."),
        "image_prompt": ugc_img(
            "A Black man about 55, greying close fade and a grey-flecked beard, plain navy henley, "
            "sitting at a kitchen table under warm light, weathered and sober, looking into a phone. ",
            "I figured it was too late. It wasn't."),
    },
    {
        "n": 6, "slug": "u6_whistleblower", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, former staff",
        "angle": "Former St. Charles staff member who watched it happen",
        "headline": "Were you a kid locked up in St. Charles?",
        "pull_quote": "I watched it happen. I stayed quiet too long.",
        "primary": (
            "I worked inside St. Charles — one of Illinois' juvenile centers — for ten years. If you "
            "were a kid locked up in there, hear me out.\n\n"
            "I watched staff sexually abuse the kids in our care. I knew how they did it — the "
            "privileges, the phone time, the ones nobody was checking on. The showers, the room checks "
            "at night.\n\n"
            "And when a kid spoke up, he landed in the hole. Nobody believed a kid over a guard. I "
            "stayed quiet too long, and I have to live with that.\n\n"
            "Now the state of Illinois is finally being sued for it. Nearly a thousand people have "
            "come forward.\n\n"
            "If a staff member sexually abused you when you were locked up in an Illinois juvenile "
            "detention center, you may qualify for significant compensation. There's no deadline. It's "
            "free, it's confidential, and you never go to court.\n\n"
            "You were telling the truth back then. Somebody's finally listening now. 👇 Tap below — "
            "just your name and number."),
        "image_prompt": ugc_img(
            "A Black man about 50, bald with a short salt-and-pepper goatee and glasses, plain charcoal "
            "crew-neck, sitting on a couch in a modest home, grave and credible, looking into a phone. ",
            "I watched it happen. I stayed quiet too long."),
    },
    {
        "n": 7, "slug": "u7_mother", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, mother ~52",
        "angle": "Mother whose son told her twenty years later",
        "headline": "Was your son locked up in an Illinois juvie?",
        "pull_quote": "My son told me twenty years later.",
        "primary": (
            "My son got locked up in an Illinois juvenile center when he was fifteen. He came home "
            "quiet. Angry. He stayed that way for twenty years and I never knew why.\n\n"
            "He finally told me last year. A staff member sexually abused him in there. He never said "
            "a word back then because he didn't think anyone would believe a kid over a guard.\n\n"
            "I think about all the years he carried that alone and it breaks my heart.\n\n"
            "He's not the only one. Nearly a thousand people are suing the state of Illinois for what "
            "happened to them in those juvenile detention centers.\n\n"
            "If your son was sexually abused in an Illinois juvenile center, he may qualify for "
            "significant compensation. It's free to check, completely confidential, and there's no "
            "deadline — it doesn't matter how long ago it was. He never has to go to court.\n\n"
            "If you're a mother who's wondered what happened to your boy in that place — 👇 tap below. "
            "It takes about thirty seconds. He doesn't have to do it alone."),
        "image_prompt": ugc_img(
            "A woman about 52, medium-brown skin, short natural hair going grey, plain cardigan, sitting "
            "in a living room, warm but heavy-hearted, looking into a phone camera held at arm's length. ",
            "My son told me twenty years later."),
    },
    {
        "n": 8, "slug": "u8_told_no_one_believed", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, garage/plain",
        "angle": "He reported it back then and nothing happened",
        "headline": "You spoke up in juvie and nothing happened?",
        "pull_quote": "Nobody believed a kid over a guard.",
        "primary": (
            "I did tell someone. Back when it was happening.\n\n"
            "I was locked up in an Illinois juvenile center, I was fourteen, and a staff member was "
            "sexually abusing me. I worked up the nerve to say something. You know what happened? "
            "Nothing. They wrote me up. Said I was lying. Nobody believed a kid over a guard.\n\n"
            "So I stopped talking about it. For thirty years.\n\n"
            "Now the state of Illinois is being sued for exactly this. Nearly a thousand of us are "
            "coming forward, and people are finally listening.\n\n"
            "If you were sexually abused in an Illinois juvenile detention center, you may qualify for "
            "significant compensation. It doesn't matter that you told someone and nothing happened. "
            "It doesn't matter how long ago it was — there's no deadline. It's free, it's confidential, "
            "and you never go to court.\n\n"
            "They didn't believe you then. This is different. 👇 Tap below — just your name and number, "
            "about thirty seconds."),
        "image_prompt": ugc_img(
            "A Black man about 45, short hair and a full beard, plain blue work polo, standing in a "
            "garage with tools softly out of focus behind, plainspoken and firm, looking into a phone. ",
            "Nobody believed a kid over a guard."),
    },
    {
        "n": 9, "slug": "u9_not_alone_number", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, plain room",
        "angle": "Thought he was the only one — nearly a thousand",
        "headline": "You weren't the only one.",
        "pull_quote": "I thought I was the only one. I was wrong by nine hundred.",
        "primary": (
            "For twenty years I thought I was the only one this happened to.\n\n"
            "I was locked up in an Illinois juvenile center as a kid, and a staff member sexually "
            "abused me in there. I never told anyone, because I figured nobody would believe a kid "
            "over a guard, and because I figured it was just me.\n\n"
            "I was wrong by about nine hundred.\n\n"
            "Nearly a thousand people are suing the state of Illinois right now over what happened to "
            "them in those juvenile detention centers. Nine hundred people who all thought they were "
            "the only one.\n\n"
            "If a staff member sexually abused you when you were locked up in an Illinois juvenile "
            "center, you may qualify for significant compensation. There's no deadline. It's free, "
            "it's confidential, and you never go to court.\n\n"
            "You're not crazy, and you're not alone. There are nearly a thousand of us. 👇 Tap below — "
            "just your name and number, about thirty seconds."),
        "image_prompt": ugc_img(
            "A Black man about 40, low fade with a chin-strap beard, plain grey crew-neck, sitting in a "
            "plain room, steady and sober, looking directly into a phone camera held at arm's length. ",
            "I thought I was the only one."),
    },
    {
        "n": 10, "slug": "u10_peer_reveal", "type": "ugc",
        "format": "UGC testimonial longform", "style": "documentary phone selfie, parked car, animated",
        "angle": "A guy he did time with reached out — peer reveal",
        "headline": "Heard about the Illinois juvie lawsuits?",
        "pull_quote": "A guy I did time with told me. I thought it was a scam.",
        "primary": (
            "A guy I did time with at Cook County juvenile detention hit me up out of nowhere last "
            "week. Hadn't talked in twenty years.\n\n"
            "He told me Illinois is paying people who got sexually abused in those juvenile centers as "
            "kids. I thought it was a scam. Hung up halfway through.\n\n"
            "Then I looked it up. It's real. Nearly a thousand of us are suing the state for what staff "
            "did in there.\n\n"
            "Both of us were sexually abused when we were locked up in that place. Neither of us ever "
            "said a word, because who believes a kid over a guard?\n\n"
            "If a staff member sexually abused you when you were locked up in an Illinois juvenile "
            "detention center, you may qualify for significant compensation. There's no deadline, it "
            "doesn't matter how long ago. It's free, it's confidential, and you never go to court.\n\n"
            "Took me about thirty seconds. If you were in there, somebody you came up with might be "
            "trying to reach you too. 👇 Tap below."),
        "image_prompt": ugc_img(
            "A Black man about 41, short twists, deep-brown skin, plain maroon t-shirt, sitting in the "
            "driver's seat of a parked car, animated and a little surprised, looking into a phone. ",
            "A guy I did time with told me."),
    },

    # ================= 10 DESIGNED-FORMAT BANNERS =================
    {
        "n": 11, "slug": "d1_qualify_checklist", "type": "designed",
        "format": "qualify checklist", "style": "clipboard intake document",
        "angle": "Self-qualifying intake checklist",
        "headline": "Do you qualify? (30-second check)",
        "pull_quote": "DO YOU QUALIFY?",
        "primary": ("If you were locked up in an Illinois juvenile detention center as a kid and a "
                    "staff member sexually abused you, you may qualify for significant compensation. "
                    "Free, confidential, no court — about 30 seconds to check. 👇"),
        "image_prompt": (
            "A realistic top-down photo of an intake clipboard holding a printed checklist form on "
            "white paper, a pen resting on it, clean even documentary lighting. The form text reads "
            "EXACTLY: a bold large title 'DO YOU QUALIFY?', then three checked checkbox lines: "
            "'[x] Held in an Illinois juvenile detention center', '[x] Sexually abused while you were "
            "inside', '[x] Even if it was years ago', then a dark bottom bar with white text 'You may "
            "qualify for significant compensation', and small text beneath it 'Tap below — name & "
            "number, about 30 seconds.' High contrast, crisp, mobile-readable." + SUFFIX),
    },
    {
        "n": 12, "slug": "d2_warning_psa", "type": "designed",
        "format": "warning PSA", "style": "brutalist bold caution, black & safety-yellow",
        "angle": "Pattern-interrupt PSA",
        "headline": "Before you scroll — read this",
        "pull_quote": "BEFORE YOU SCROLL —",
        "primary": ("Before you scroll past — if you were sexually abused as a kid while locked up in "
                    "an Illinois juvenile detention center, you may qualify for significant "
                    "compensation. Free and confidential to check. 👇"),
        "image_prompt": (
            "A stark brutalist warning-poster graphic, high-contrast black and safety-yellow, bold "
            "heavy condensed sans-serif, slight print grain. Text reads EXACTLY: very large 'BEFORE "
            "YOU SCROLL —' across the top, then in the middle 'If you were sexually abused as a kid in "
            "an Illinois juvenile detention center, this is for you.', then a yellow bar at the bottom "
            "with black text 'You may qualify for significant compensation.' Loud, urgent, plain." + SUFFIX),
    },
    {
        "n": 13, "slug": "d3_search_bar", "type": "designed",
        "format": "search bar", "style": "clean phone-UI screenshot",
        "angle": "The search they've been afraid to make",
        "headline": "The search you've been afraid to make",
        "pull_quote": "illinois juvenile detention abuse lawsuit",
        "primary": ("If you've been searching this, you're not the only one. Sexually abused as a kid "
                    "in an Illinois juvenile center? You may qualify for significant compensation. "
                    "Free and confidential. 👇"),
        "image_prompt": (
            "A clean smartphone search screenshot on a white background, realistic mobile search UI "
            "with a rounded search field and a magnifier icon. The search field contains the typed "
            "text 'illinois juvenile detention abuse lawsuit'. Below it three autocomplete suggestion "
            "rows, each with a small magnifier icon, reading EXACTLY: 'illinois juvenile detention "
            "abuse lawsuit am i too late', 'illinois juvenile detention abuse lawsuit is it "
            "confidential', 'illinois juvenile detention abuse lawsuit how much could i qualify for'. "
            "A small footer line at the bottom: 'You may qualify for significant compensation. Tap "
            "below.' Crisp, authentic, legible." + SUFFIX),
    },
    {
        "n": 14, "slug": "d4_faq", "type": "designed",
        "format": "FAQ objection-killer", "style": "clean minimalist card",
        "angle": "Kills the four biggest objections",
        "headline": "No report. No court. No cost.",
        "pull_quote": "QUESTIONS? (we get these a lot)",
        "primary": ("The questions everyone asks first: no police report, nobody calls your house, "
                    "it's free, and there's no deadline. Sexually abused as a kid in an Illinois "
                    "juvenile center? You may qualify for significant compensation. 👇"),
        "image_prompt": (
            "A clean minimalist FAQ card, soft off-white background, simple modern sans-serif, "
            "generous spacing. Text reads EXACTLY: a heading 'QUESTIONS? (we get these a lot)', then "
            "four question-and-answer pairs (question bold, answer light): 'Need a police report?  "
            "No.', 'Will anyone call my house?  No.', 'Does it cost anything?  Free.', 'Too long ago?  "
            "There's no deadline.', then a footer line 'Sexually abused in an Illinois juvenile center "
            "as a kid? You may qualify.' Calm, legible, high contrast." + SUFFIX),
    },
    {
        "n": 15, "slug": "d5_stat", "type": "designed",
        "format": "big stat", "style": "stark black-and-white, negative space",
        "angle": "Not-alone social proof number",
        "headline": "Nearly 1,000 have come forward",
        "pull_quote": "NEARLY 1,000",
        "primary": ("Nearly a thousand people are suing Illinois over what staff did to them in "
                    "juvenile detention. If you were sexually abused in there as a kid, you may "
                    "qualify for significant compensation. 👇"),
        "image_prompt": (
            "A stark minimalist poster, plain black background, huge bold condensed white type, lots "
            "of negative space. Text reads EXACTLY: an enormous 'NEARLY 1,000' filling the upper half, "
            "then smaller beneath it 'people are suing Illinois over what happened to them in juvenile "
            "detention.', then small at the bottom 'You may qualify for significant compensation. Tap "
            "below.' Powerful, editorial, high contrast." + SUFFIX),
    },
    {
        "n": 16, "slug": "d6_news_facility", "type": "designed",
        "format": "news / facility exterior", "style": "documentary news-broadcast still",
        "angle": "Highest-trust news framing, building only",
        "headline": "Illinois juvenile-detention lawsuits",
        "pull_quote": "Illinois faces wave of juvenile-detention abuse lawsuits",
        "primary": ("Illinois is facing a wave of lawsuits over sexual abuse in its juvenile detention "
                    "centers. If a staff member abused you in one as a kid, you may qualify for "
                    "significant compensation. Free and confidential. 👇"),
        "image_prompt": (
            "A documentary news-broadcast still: the exterior of an empty institutional "
            "juvenile-detention facility — a plain brick building behind a tall chain-link fence "
            "topped with razor wire, overcast grey sky, completely empty, NO people. Across the lower "
            "third, a clean neutral news-style lower-third bar with the headline 'Illinois faces wave "
            "of juvenile-detention abuse lawsuits' and a small kicker beneath 'Survivors may qualify "
            "for significant compensation.' Realistic ENG news look, neutral grade, not stylized, no "
            "real network logos." + SUFFIX),
    },
    {
        "n": 17, "slug": "d7_timeline", "type": "designed",
        "format": "it-still-counts timeline", "style": "flat-vector journal timeline",
        "angle": "Statute myth-buster",
        "headline": "Years ago still counts today",
        "pull_quote": "There's no deadline in Illinois.",
        "primary": ("It doesn't matter how long ago it was — there's no deadline in Illinois. If you "
                    "were sexually abused as a kid in a juvenile detention center, you may qualify for "
                    "significant compensation. 👇"),
        "image_prompt": (
            "A clean flat-vector horizontal timeline on a warm paper-toned background, simple and "
            "editorial. A line runs left to right between two labeled dots: the left dot labeled "
            "'Locked up — years ago' and the right dot labeled 'Today'. Above the line a banner reads "
            "'There's no deadline in Illinois.' Below it a footer line 'Sexually abused in a juvenile "
            "center as a kid? You may qualify for significant compensation.' Minimal, flat, legible." + SUFFIX),
    },
    {
        "n": 18, "slug": "d8_map", "type": "designed",
        "format": "facilities map", "style": "clean flat-vector map",
        "angle": "Name the facilities to self-qualify",
        "headline": "Were you held in one of these?",
        "pull_quote": "Were you held in one of these?",
        "primary": ("Cook County (the Audy Home), St. Charles, Warrenville, Harrisburg. If you were "
                    "sexually abused as a kid in one of these Illinois juvenile centers, you may "
                    "qualify for significant compensation. 👇"),
        "image_prompt": (
            "A clean flat-vector map: a simple silhouette of the state of Illinois on a soft neutral "
            "background, with four location pins, each pin clearly labeled in readable text: 'Cook "
            "County / Audy Home', 'St. Charles', 'Warrenville', 'Harrisburg'. A heading above reads "
            "'Were you held in one of these?' and a footer below reads 'Sexually abused there as a "
            "kid? You may qualify for significant compensation.' Minimal flat illustration, legible." + SUFFIX),
    },
    {
        "n": 19, "slug": "d9_open_letter", "type": "designed",
        "format": "open letter", "style": "journal handwritten on paper",
        "angle": "Intimate handwritten note to survivors",
        "headline": "To the person who never told anyone",
        "pull_quote": "It was not your fault, and it is not too late.",
        "primary": ("To the person who's never told anyone: it wasn't your fault, and it isn't too "
                    "late. If you were sexually abused as a kid in an Illinois juvenile detention "
                    "center, you may qualify for significant compensation. 👇"),
        "image_prompt": (
            "A photoreal handwritten open letter on a sheet of plain off-white paper, warm natural "
            "lighting, slightly imperfect real handwriting in dark blue pen, fully legible. The "
            "handwritten text reads EXACTLY: 'To the person who was locked up and never told "
            "anyone — If you were sexually abused in an Illinois juvenile detention center, "
            "it was not your fault, and it is not too late. You may qualify for significant "
            "compensation. It's free, it's private, about 30 seconds. You're not alone.' Intimate, "
            "real, documentary." + SUFFIX),
    },
    {
        "n": 20, "slug": "d10_definition", "type": "designed",
        "format": "dictionary definition", "style": "clean editorial print serif",
        "angle": "Conceptual pattern-interrupt — the SOL is lifted",
        "headline": "Statute of limitations: lifted",
        "pull_quote": "statute of limitations — lifted in Illinois.",
        "primary": ("Statute of limitations — lifted in Illinois. If you were sexually abused as a kid "
                    "in a juvenile detention center, it's not too late. You may qualify for "
                    "significant compensation. 👇"),
        "image_prompt": (
            "A clean editorial dictionary-definition card, off-white paper, elegant serif typography "
            "like a printed dictionary page. Text reads EXACTLY: the entry word 'statute of "
            "limitations' in bold serif followed by '(n.)', then a definition line 'the time limit "
            "for bringing a legal claim', then on its own line in bold '— lifted in Illinois.', then "
            "in smaller text 'If you were sexually abused as a kid in a juvenile detention center, you "
            "may qualify for significant compensation. Tap below.' Refined, print-quality, legible." + SUFFIX),
    },
]


def dest_for(ad):
    return OUT / f"{ad['n']:02d}_{ad['slug']}.png"


def run_one(ad, regen, provider, size):
    dest = dest_for(ad)
    if dest.exists() and not regen:
        return ad["n"], ad["slug"], "skip"
    prompt = ad["image_prompt"]
    try:
        if provider == "kie":
            import kie_client as kie
            r = kie.generate_gpt_image(prompt, aspect_ratio="1:1", resolution="2K")
            if r.get("status") == "success" and r.get("urls"):
                kie.download(r["urls"][0], dest)
                return ad["n"], ad["slug"], "ok"
            return ad["n"], ad["slug"], f"fail:{str(r.get('raw'))[:80]}"
        from openai_image import generate_image
        r = generate_image(prompt, out_path=str(dest), size=size, quality="high")
        return ad["n"], ad["slug"], "ok" if r.get("status") == "success" else f"fail:{str(r)[:80]}"
    except Exception as e:
        return ad["n"], ad["slug"], f"err:{type(e).__name__}:{str(e)[:70]}"


def dump_copy():
    OUT.mkdir(parents=True, exist_ok=True)
    copy = [{k: ad[k] for k in ("n", "slug", "type", "format", "style", "angle",
                                 "headline", "pull_quote", "primary")} for ad in ADS]
    (OUT / "copy.json").write_text(json.dumps(copy, indent=2, ensure_ascii=False))
    print(f"wrote {OUT/'copy.json'} ({len(copy)} ads)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--provider", default="kie", choices=["kie", "openai"])
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--dump", action="store_true", help="write copy.json and exit")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.dump:
        dump_copy()
        return
    ads = ADS
    if args.only:
        want = {s.strip() for s in args.only.split(",") if s.strip()}
        ads = [a for a in ADS if a["slug"] in want or str(a["n"]) in want]
    ok = fail = skip = 0
    fails = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, args.regen, args.provider, args.size): a for a in ads}
        for f in as_completed(futs):
            n, slug, st = f.result()
            print(f"[{st}] {n:02d} {slug}", flush=True)
            if st == "ok":
                ok += 1
            elif st == "skip":
                skip += 1
            else:
                fail += 1
                fails.append(f"{n:02d}_{slug}")
    print(f"\n=== ok={ok} skip={skip} fail={fail} / {len(ads)} ===", flush=True)
    if fails:
        print("FAILS:", ",".join(fails), flush=True)


if __name__ == "__main__":
    main()
