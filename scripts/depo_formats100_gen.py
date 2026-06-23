"""
Depo-Provera — 100 DISTINCT image ads (image-ad-formats skill: format × style × angle).
Pure gpt-image-2 full-render via OpenAI-direct (KIE gpt-image-2 was down 2026-06-19).
Prompts authored by 5 parallel agents, merged + compliance-scanned into prompts.json.

Run:  .venv/bin/python scripts/depo_formats100_gen.py [--only <slug|n,...>] [--regen] [--workers 6]
Output: outputs/depo_ads/formats100/<NNN>_<slug>_<style>.png  (skip-if-exists)
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image
import kie_client as kie

PROVIDER = "openai"   # set in main(): openai (1024x1024) | kie (native 1:1 2K)
SIZE = "1024x1024"    # OpenAI square
OUT = Path("outputs/depo_ads/formats100")
ADS = json.load(open(OUT / "prompts.json"))["ads"]
SUFFIX = (" Render ONLY the exact text specified — do not invent extra text, headlines, or claims. "
          "No watermark, no logo, no disclaimer.")


def dest_for(ad):
    style = ad["style"].replace("/", "-")
    return OUT / f"{ad['n']:03d}_{ad['slug']}_{style}.png"


def run_one(ad, regen):
    dest = dest_for(ad)
    if dest.exists() and not regen:
        return ad["n"], ad["slug"], "skip"
    prompt = ad["prompt"]
    if "Render ONLY" not in prompt:
        prompt += SUFFIX
    try:
        if PROVIDER == "kie":
            r = kie.generate_gpt_image(prompt, aspect_ratio="1:1", resolution="2K")
            if r.get("status") == "success" and r.get("urls"):
                kie.download(r["urls"][0], dest)
                return ad["n"], ad["slug"], "ok"
            return ad["n"], ad["slug"], f"fail:{str(r.get('raw'))[:80]}"
        r = generate_image(prompt, out_path=str(dest), size=SIZE, quality="high")
    except Exception as e:
        return ad["n"], ad["slug"], f"err:{type(e).__name__}:{str(e)[:70]}"
    return ad["n"], ad["slug"], "ok" if r.get("status") == "success" else f"fail:{str(r)[:80]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--provider", default="openai", choices=["openai", "kie"])
    ap.add_argument("--size", default="1024x1024")
    args = ap.parse_args()
    global PROVIDER, SIZE
    PROVIDER, SIZE = args.provider, args.size
    ads = ADS
    if args.only:
        want = {s.strip() for s in args.only.split(",") if s.strip()}
        ads = [a for a in ADS if a["slug"] in want or str(a["n"]) in want]
    ok = fail = skip = 0
    fails = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, args.regen): a for a in ads}
        for f in as_completed(futs):
            n, slug, st = f.result()
            print(f"[{st}] {n:03d} {slug}", flush=True)
            if st == "ok":
                ok += 1
            elif st == "skip":
                skip += 1
            else:
                fail += 1
                fails.append(f"{n:03d}_{slug}")
    print(f"\n=== ok={ok} skip={skip} fail={fail} / {len(ads)} ===", flush=True)
    if fails:
        print("FAILS:", ",".join(fails), flush=True)


if __name__ == "__main__":
    main()
