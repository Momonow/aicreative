"""
IL JDC — rebuild the 10 DESIGNED ads (11-20) as NEWS-HEADLINE-ARTICLE images.
Replaces the abstract designed formats with credible news-article looks; the on-image HEADLINE
explicitly names Illinois juvenile detention + (sexual) abuse so the topic is obvious at a glance.
Keeps the 10 UGC testimonials (01-10) untouched. Same output folder + naming.

Compliance: lawsuit/allegation framing ("allege", "lawsuits", "say"), "may qualify for significant
compensation" lives mainly in the FB primary + a couple decks; explicit "sexual abuse" + facilities;
rights-clean (generic made-up outlet, NO real network logos); IMAGE SAFETY: no people, no minors,
empty institutional / facility-exterior / courthouse / documents only.

Run: .venv/bin/python scripts/il_jdc_news_ads.py [--only <slug|n,..>] [--regen] [--workers 5]
                                                 [--provider kie|openai] [--dump]
"""
import argparse, json, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
OUT = Path("outputs/il_jdc_image_ads")
SAFE = (" Professional, credible, neutral journalistic look, clean editorial typography, fully "
        "legible. Render ONLY the exact text specified — no extra words, claims, real news-outlet "
        "names or logos, watermarks, or disclaimers. NO people, no children, no minors, nothing sexual.")


def news_img(layout, photo, eyebrow, headline, deck, source):
    return (f"A realistic {layout}. {photo} Above the headline a small all-caps category kicker reads "
            f"EXACTLY: \"{eyebrow}\". The bold main news headline reads EXACTLY: \"{headline}\". A "
            f"smaller deck/subhead beneath reads EXACTLY: \"{deck}\". A thin small source line reads "
            f"EXACTLY: \"{source}\" (a GENERIC made-up outlet)." + SAFE)


CTA = " It's free, confidential, no court — about 30 seconds to check. 👇"

NEWS = [
    {"n": 11, "slug": "d1_news_wave", "type": "designed", "format": "news article hero",
     "style": "news-website article hero", "angle": "Wave of lawsuits — establishing",
     "headline": "Sexual-abuse lawsuits mount against Illinois juvenile detention",
     "pull_quote": "Sexual-abuse lawsuits mount against Illinois juvenile detention",
     "primary": ("If you were sexually abused while locked up in an Illinois juvenile detention center, "
                 "you may qualify for significant compensation." + CTA),
     "image_prompt": news_img(
         "news-website article hero layout, a wide photo on top with the kicker, headline and deck on a "
         "clean white page below",
         "The photo shows the exterior of an institutional juvenile-detention building behind a tall "
         "chain-link fence with razor wire, overcast grey sky, completely empty.",
         "ILLINOIS INVESTIGATION", "Sexual-abuse lawsuits mount against Illinois juvenile detention",
         "Nearly 1,000 former detainees say staff abused them inside state youth centers.",
         "Illinois Statewide News")},

    {"n": 12, "slug": "d2_news_thousand", "type": "designed", "format": "newspaper clipping",
     "style": "black-and-white newspaper front page", "angle": "The number / not-alone",
     "headline": "Nearly 1,000 allege sexual abuse in Illinois juvenile detention",
     "pull_quote": "Nearly 1,000 allege sexual abuse in Illinois juvenile detention",
     "primary": ("Nearly a thousand people say they were sexually abused as kids in Illinois juvenile "
                 "detention centers. If that was you, you may qualify for significant compensation." + CTA),
     "image_prompt": news_img(
         "black-and-white newspaper front-page clipping with newsprint texture and column rules",
         "A small grainy newsprint photo of an empty institutional corridor lined with locked doors, "
         "no people.",
         "FRONT PAGE", "Nearly 1,000 allege sexual abuse in Illinois juvenile detention",
         "Survivors may qualify for significant compensation as suits against the state mount.",
         "The Midwest Ledger")},

    {"n": 13, "slug": "d3_news_staff", "type": "designed", "format": "news article card",
     "style": "clean news-website article card", "angle": "Staff perpetrators",
     "headline": "Staff sexual-abuse lawsuits hit Illinois youth centers",
     "pull_quote": "Staff sexual-abuse lawsuits hit Illinois youth centers",
     "primary": ("Lawsuits allege staff sexually abused kids inside Illinois juvenile detention centers. "
                 "If it happened to you, you may qualify for significant compensation." + CTA),
     "image_prompt": news_img(
         "clean news-website article card with a photo, kicker, headline and deck",
         "A photo of a courthouse exterior with tall stone columns and steps, daytime, no people.",
         "YOUTH-CENTER LAWSUITS", "Staff sexual-abuse lawsuits hit Illinois youth centers",
         "Allegations span decades at juvenile detention facilities across the state.",
         "Capitol Legal Report")},

    {"n": 14, "slug": "d4_news_decades", "type": "designed", "format": "news hero overlay",
     "style": "news hero, headline over a dark photo", "angle": "Decades later, no deadline",
     "headline": "Survivors break silence on Illinois juvenile-detention abuse",
     "pull_quote": "Survivors break silence on Illinois juvenile-detention abuse",
     "primary": ("It doesn't matter how long ago it was — there's no deadline in Illinois. If you were "
                 "sexually abused in a juvenile detention center as a kid, you may qualify for "
                 "significant compensation." + CTA),
     "image_prompt": news_img(
         "news-website article hero, a photo background with a dark gradient and the kicker, headline "
         "and deck overlaid in white",
         "The background photo is a chain-link fence topped with razor wire against an overcast sky, "
         "empty, no people.",
         "DECADES LATER", "Survivors break silence on Illinois juvenile-detention abuse",
         "There is no filing deadline in Illinois — survivors may still qualify for compensation.",
         "Statewide News · Investigations")},

    {"n": 15, "slug": "d5_news_audy", "type": "designed", "format": "local news hero",
     "style": "local-news website article hero", "angle": "Audy Home / Cook County named",
     "headline": "Cook County 'Audy Home' named in abuse lawsuits",
     "pull_quote": "Cook County 'Audy Home' named in abuse lawsuits",
     "primary": ("Were you locked up at the Audy Home — Cook County juvenile detention? If a staff "
                 "member sexually abused you there, you may qualify for significant compensation." + CTA),
     "image_prompt": news_img(
         "local-news website article hero with a photo, kicker, headline and deck",
         "A photo of an older brick institutional building behind a fence, overcast daylight, no people.",
         "CHICAGO METRO", "Cook County 'Audy Home' named in abuse lawsuits",
         "The Chicago youth facility is among several named in sexual-abuse suits against Illinois.",
         "Chicago Metro Wire")},

    {"n": 16, "slug": "d6_news_failed", "type": "designed", "format": "accountability news hero",
     "style": "accountability news-website hero", "angle": "Accountability — the state failed to act",
     "headline": "Suits: Illinois failed to stop youth-center sexual abuse",
     "pull_quote": "Suits: Illinois failed to stop youth-center sexual abuse",
     "primary": ("Lawsuits say Illinois failed to stop staff from sexually abusing kids in its juvenile "
                 "detention centers. If it happened to you, you may qualify for significant "
                 "compensation." + CTA),
     "image_prompt": news_img(
         "accountability news-website article hero with a photo, kicker, headline and deck",
         "A photo of a state government building exterior with stone steps and columns, daytime, "
         "no people.",
         "ACCOUNTABILITY", "Suits: Illinois failed to stop youth-center sexual abuse",
         "Survivors say the state ignored years of abuse at its juvenile detention centers.",
         "Capitol Accountability Desk")},

    {"n": 17, "slug": "d7_news_nodeadline", "type": "designed", "format": "explainer card",
     "style": "news-website explainer card", "angle": "No deadline / statute reopened",
     "headline": "No deadline for Illinois juvenile-detention abuse survivors",
     "pull_quote": "No deadline for Illinois juvenile-detention abuse survivors",
     "primary": ("There's no deadline in Illinois — even decades later, survivors of sexual abuse in "
                 "juvenile detention centers may still qualify for significant compensation." + CTA),
     "image_prompt": news_img(
         "news-website explainer article card with a photo, kicker, headline and deck",
         "A photo of a wall clock beside a wooden gavel and a stack of legal documents on a desk, no people.",
         "WHAT TO KNOW", "No deadline for Illinois juvenile-detention abuse survivors",
         "A change in state law reopened the window to file — even decades later.",
         "Capitol Legal Report")},

    {"n": 18, "slug": "d8_news_facilities", "type": "designed", "format": "news article + map",
     "style": "news article card with map inset", "angle": "The facilities named",
     "headline": "Illinois youth centers named in sexual-abuse lawsuits",
     "pull_quote": "Illinois youth centers named in sexual-abuse lawsuits",
     "primary": ("Cook County (Audy Home), St. Charles, Warrenville, Harrisburg. If you were sexually "
                 "abused in one of these Illinois juvenile centers as a kid, you may qualify for "
                 "significant compensation." + CTA),
     "image_prompt": news_img(
         "news-website article card with a small inset map graphic of Illinois beside the text",
         "A simple inset map silhouette of Illinois with four location markers, beside a photo of an "
         "institutional building gate, no people.",
         "FACILITIES NAMED", "Illinois youth centers named in sexual-abuse lawsuits",
         "St. Charles, Warrenville, Harrisburg and Cook County's Audy Home among those listed.",
         "Statewide News")},

    {"n": 19, "slug": "d9_news_silence", "type": "designed", "format": "longform feature hero",
     "style": "longform feature hero, large quote headline", "angle": "Culture of silence",
     "headline": "'Nobody believed a kid over a guard'",
     "pull_quote": "'Nobody believed a kid over a guard'",
     "primary": ("Nobody believed a kid over a guard. That was the bet back then. Not anymore. If you "
                 "were sexually abused in an Illinois juvenile detention center, you may qualify for "
                 "significant compensation." + CTA),
     "image_prompt": news_img(
         "longform feature article hero, a large quote headline over a muted photo with kicker and deck",
         "A muted photo of an empty institutional dormitory with rows of empty bunk beds, no people.",
         "ILLINOIS JUVENILE DETENTION · ABUSE", "'Nobody believed a kid over a guard'",
         "Inside the culture of silence at Illinois youth centers — and the sexual abuse survivors "
         "say it hid.",
         "Statewide News · Feature")},

    {"n": 20, "slug": "d10_news_compensate", "type": "designed", "format": "breaking news hero",
     "style": "breaking-news website hero", "angle": "Compensation / may qualify",
     "headline": "Illinois abuse survivors may qualify for compensation",
     "pull_quote": "Illinois abuse survivors may qualify for compensation",
     "primary": ("Survivors of sexual abuse in Illinois juvenile detention centers may qualify for "
                 "significant compensation. There's no deadline, and it's completely confidential." + CTA),
     "image_prompt": news_img(
         "breaking-news website article hero with a photo, kicker, headline and deck",
         "A photo of the Illinois State Capitol dome / a state government building exterior with a small "
         "gavel inset, daylight, no people.",
         "JUVENILE-DETENTION ABUSE", "Illinois abuse survivors may qualify for compensation",
         "Those sexually abused as children in state youth centers are coming forward.",
         "Capitol Wire")},
]


def dest_for(ad):
    return OUT / f"{ad['n']:02d}_{ad['slug']}.png"


def run_one(ad, regen, provider, size):
    dest = dest_for(ad)
    if dest.exists() and not regen:
        return ad["n"], ad["slug"], "skip"
    try:
        if provider == "kie":
            import kie_client as kie
            r = kie.generate_gpt_image(ad["image_prompt"], aspect_ratio="1:1", resolution="2K")
            if r.get("status") == "success" and r.get("urls"):
                kie.download(r["urls"][0], dest)
                return ad["n"], ad["slug"], "ok"
            return ad["n"], ad["slug"], f"fail:{str(r.get('raw',{}).get('failMsg',r.get('raw')))[:80]}"
        from openai_image import generate_image
        r = generate_image(ad["image_prompt"], out_path=str(dest), size=size, quality="high")
        return ad["n"], ad["slug"], "ok" if r.get("status") == "success" else f"fail:{str(r)[:80]}"
    except Exception as e:
        return ad["n"], ad["slug"], f"err:{type(e).__name__}:{str(e)[:70]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--provider", default="kie", choices=["kie", "openai"])
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.dump:
        copy = [{k: a[k] for k in ("n", "slug", "type", "format", "style", "angle",
                                    "headline", "pull_quote", "primary")} for a in NEWS]
        (OUT / "news_copy.json").write_text(json.dumps(copy, indent=2, ensure_ascii=False))
        print(f"wrote {OUT/'news_copy.json'}")
        return
    ads = NEWS
    if args.only:
        want = {s.strip() for s in args.only.split(",") if s.strip()}
        ads = [a for a in NEWS if a["slug"] in want or str(a["n"]) in want]
    ok = fail = skip = 0; fails = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, args.regen, args.provider, args.size): a for a in ads}
        for f in as_completed(futs):
            n, slug, st = f.result()
            print(f"[{st}] {n:02d} {slug}", flush=True)
            ok += st == "ok"; skip += st == "skip"
            if st not in ("ok", "skip"):
                fail += 1; fails.append(f"{n:02d}_{slug}")
    print(f"\n=== ok={ok} skip={skip} fail={fail} / {len(ads)} ===", flush=True)
    if fails:
        print("FAILS:", ",".join(fails), flush=True)


if __name__ == "__main__":
    main()
