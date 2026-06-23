"""
Depo — 20 story/news ads (the long-form testimonial winner format + news-article ads).
Testimonials (1-15): KIE gpt-image-2 persona (4:5 2K, no text) + PIL bold on-image headline + sub
(reuses r_testi_real from depo_ads_gen — the proven build). News (16-20): full KIE gpt-image-2
news-layout render. Reads outputs/depo_ads/story20/concepts.json.

Run: .venv/bin/python scripts/depo_story20_gen.py [--only <n,..>] [--regen] [--workers 5]
Output: outputs/depo_ads/story20/<NN>_<slug>.png   (persona bases in story20/base/)
"""
import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie
from depo_ads_gen import r_testi_real, REAL_IPHONE, NOTEXT  # proven testimonial renderer + clauses

OUT = Path("outputs/depo_ads/story20")
BASE = OUT / "base"
BASE.mkdir(parents=True, exist_ok=True)
ADS = json.load(open(OUT / "concepts.json"))["ads"]


def slug_for(ad):
    return f"{ad['n']:02d}_" + re.sub(r"[^a-z0-9]+", "_", ad["approach"].lower()).strip("_")[:22]


def gen_kie(prompt):
    r = kie.generate_gpt_image(prompt, aspect_ratio="4:5", resolution="2K")
    if r.get("status") == "success" and r.get("urls"):
        return r["urls"][0]
    return None


def run_one(ad, regen):
    slug = slug_for(ad)
    dest = OUT / f"{slug}.png"
    if dest.exists() and not regen:
        return ad["n"], slug, "skip"
    try:
        if "masthead" in ad:  # NEWS — full render
            url = gen_kie(ad["prompt"])
            if not url:
                return ad["n"], slug, "fail-news"
            kie.download(url, dest)
            return ad["n"], slug, "ok-news"
        # TESTIMONIAL — persona base + PIL headline overlay
        bdest = BASE / f"{slug}.png"
        if not bdest.exists() or regen:
            url = gen_kie(ad["persona"] + REAL_IPHONE + NOTEXT)
            if not url:
                return ad["n"], slug, "fail-persona"
            kie.download(url, bdest)
        base = Image.open(bdest).convert("RGB")
        f = {"headline": ad["headline"], "sub": ad.get("sub", "You may qualify for significant compensation.")}
        r_testi_real({"": base}, f, headline=True).save(dest)
        return ad["n"], slug, "ok"
    except Exception as e:
        return ad["n"], slug, f"err:{str(e)[:60]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()
    want = {s.strip() for s in args.only.split(",") if s.strip()}
    ads = [a for a in ADS if not want or str(a["n"]) in want]
    fails = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, args.regen): a for a in ads}
        for fu in as_completed(futs):
            n, slug, st = fu.result()
            print(f"[{st}] {slug}", flush=True)
            if st.startswith(("err", "fail")):
                fails.append(slug)
    print(f"\n=== done; fails: {fails or 'none'} ===", flush=True)


if __name__ == "__main__":
    main()
