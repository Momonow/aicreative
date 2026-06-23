"""
Depo — 50 MORE "speak-to-the-diagnosed" image ads (n21-70), gpt-image-2 full-render, 1:1 2K, KIE.
Reads outputs/depo_ads/diagnosed50/prompts.json (authored by 3 agents, compliance+risk scanned).
Run: .venv/bin/python scripts/depo_diagnosed50_gen.py [--only <slug|n,..>] [--regen] [--workers 5]
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/depo_ads/diagnosed50")
ADS = json.load(open(OUT / "prompts.json"))["ads"]
SUFFIX = (" Render ONLY the exact text specified — do not invent extra text, headlines, or claims. "
          "No watermark, no logo, no disclaimer.")


def run_one(ad, regen):
    dest = OUT / f"{ad['n']:02d}_{ad['slug']}_{ad['style']}.png".replace("/", "-")
    if dest.exists() and not regen:
        return ad, "skip"
    p = ad["prompt"] + ("" if "Render ONLY" in ad["prompt"] else SUFFIX)
    try:
        r = kie.generate_gpt_image(p, aspect_ratio="1:1", resolution="2K")
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
