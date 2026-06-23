"""
CILOCALA FB image ads v2 — YELLOW, with faithful hardware (zipper pulls / webbing / toggle / patch).
Anchors on a multi-angle collage (+ flat-zipper-pull close-up) so gpt-image-2 reproduces the
real product construction.

Build collage first (4 yellow angles) -> /tmp/cilo_yellow_collage.png
Pull close-up ref: ~/Desktop/cilo_ref/CleanShot 2026-06-15 at 13.49.13@2x.png (lilac, flat pulls)

Run all:   .venv/bin/python scripts/cilocala_ads_v2.py
Test 2:    .venv/bin/python scripts/cilocala_ads_v2.py --only hero-colorblock,feature-board
"""
import argparse, glob, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_ads_v2"); OUT.mkdir(parents=True, exist_ok=True)
COLLAGE = "/tmp/cilo_yellow_collage.png"
REFDIR = os.path.expanduser("~/Desktop/cilo_ref")

# CRITICAL hardware lock — the v1 miss was generic round zipper pulls.
LOCK = ("CRITICAL product accuracy — reproduce the EXACT backpack shown in the reference images "
        "(a butter/pastel-yellow rounded-top nylon daypack). Keep these hardware details exactly: "
        "(1) WHITE FLAT silicone strap zipper pulls — long flat rectangular tabs, NOT round or teardrop; "
        "the main top zipper has TWO white flat pull-tabs side by side. "
        "(2) The front pocket has a horizontal flat woven WEBBING TAPE band across it; the front-pocket zip "
        "runs along the TOP of that pocket with a single white flat pull hanging at the LEFT. "
        "(3) A white barrel drawstring cord-lock TOGGLE at top center, thin orange-and-white braided cord, "
        "plus a short webbing grab handle. "
        "(4) A white rounded-square rubber LOGO PATCH debossed 'CILO CALA' (two stacked lines) on the upper front. "
        "(5) Matte nylon fabric, side slip pockets. Keep proportions, seams and hardware faithful. ")

NOTEXT = ("Render any Korean text as clean, correctly-spelled, well-kerned Hangul — no gibberish. ")

Y = "the EXACT pastel-yellow CILOCALA Classic backpack from the reference images "

ADS = [
    dict(n=1, slug="color-grid", aspect="1:1",
         prompt=(f"Clean studio e-commerce ad. A neat 3x3 grid of {Y}, but each of the 9 backpacks is a "
                 "different cheerful colorway — butter yellow, blush pink, mint, sky blue, royal blue, white, "
                 "kelly green, lilac, coral; only the body color changes, the white logo patch, white flat zipper "
                 "pulls and webbing stay identical on all. Bright soft-white background, soft shadows. Big bold "
                 "rounded sans-serif Korean headline top center: '오늘 기분, 무슨 컬러?' and smaller 'Carry Colors!'. "
                 + LOCK + NOTEXT)),
    dict(n=2, slug="hero-colorblock", aspect="1:1",
         prompt=(f"Premium minimal product ad. {Y}floating centered on a bold two-tone pastel color-block "
                 "background (left soft lilac, right soft mint), soft studio shadow, lots of negative space. "
                 "Short Korean headline near bottom center: '가벼운데, 예쁘기까지.' and a small wordmark 'CILOCALA'. "
                 + LOCK + NOTEXT)),
    dict(n=3, slug="whats-in-bag", aspect="4:5",
         prompt=(f"Top-down flatlay ad. {Y}shown open with neatly arranged daily items around it: a slim laptop, "
                 "a tumbler, a small pouch, an earbuds case, a paperback, a keyring — warm cream/yellow palette on a "
                 "soft beige surface, styled. Thin Korean callout labels with hairlines: '15인치 노트북','텀블러 칸','파우치'. "
                 "Top headline: '데일리, 이거 하나면 끝'. " + LOCK + NOTEXT)),
    dict(n=4, slug="feature-board", aspect="1:1",
         prompt=(f"E-commerce feature-callout ad. {Y}at a 3/4 front angle, centered on a clean pastel background. "
                 "Five minimal line-icon + short Korean label callouts evenly placed: '초경량','노트북 수납','발수 코팅',"
                 "'A4 수납','데일리'. Top headline: '예쁜 가방인데, 할 건 다 해요'. " + LOCK + NOTEXT)),
    dict(n=5, slug="size-guide", aspect="4:5",
         prompt=(f"Product size-guide ad. Three of {Y}in three sizes (small, medium, large) lined up left-to-right "
                 "on a clean pastel background, all yellow, soft shadows. Small Korean label under each: "
                 "'S 데일리','M 스쿨','L 여행'. Top headline: '내 사이즈, 한눈에'. " + LOCK + NOTEXT)),
    dict(n=6, slug="ugc-native", aspect="4:5",
         prompt=(f"Casual UGC-style smartphone photo that looks like a real Instagram snapshot — slightly imperfect "
                 f"framing, natural window light, a little grain. {Y}sitting on a wooden cafe chair by a window, a "
                 "latte beside it. Handwritten-style Korean caption overlaid casually: '요즘 메는 가방 추천받음… 색 미쳤다'. "
                 "Authentic, un-polished, NOT a studio shot. " + LOCK + NOTEXT)),
    dict(n=7, slug="lifestyle-onbody", aspect="4:5",
         prompt=("Photoreal lifestyle ad. A stylish young Korean woman in her early 20s walking on a sunny city "
                 f"street, wearing {Y}on both shoulders, candid natural stride, soft daylight, casual neutral outfit so "
                 "the yellow bag is the color pop. Natural skin texture, real photo look. "
                 "Minimal small Korean text along the bottom: '메는 순간, 룩이 산다'. " + LOCK + NOTEXT)),
    dict(n=8, slug="review-proof", aspect="1:1",
         prompt=(f"Social-proof review ad. {Y}on a clean pastel background, beside a five-star rating drawn as five "
                 "gold stars and a short Korean review quote inside a soft rounded white card: "
                 "'색 보고 샀다가, 가벼워서 또 삼'. A small accent badge reads '누적 판매 10만'. " + LOCK + NOTEXT)),
    dict(n=9, slug="color-vs-black", aspect="1:1",
         prompt=("Side-by-side comparison ad, split into two vertical halves. LEFT: a plain dull BLACK backpack, "
                 f"desaturated, gloomy, muted gray background. RIGHT: {Y}bright and cheerful on a soft warm background. "
                 "Korean headline split: left '다 똑같은 검정 말고,' right '오늘은, 컬러.'. " + LOCK + NOTEXT)),
    dict(n=10, slug="event-drop", aspect="4:5",
         prompt=(f"Festive promotional event ad. {Y}as hero on a celebratory pastel background with subtle confetti, "
                 "a small 'NEW' tag and a discount ribbon flag in the corner, plus a small matching free-gift pouch "
                 "graphic beside it. Korean headline: 'Carry Colors 이벤트', subtext: '단독 컬러 오픈'. " + LOCK + NOTEXT)),
]


def run_one(ad, refs, model):
    tag = "nb" if model == "nano" else "gi"
    dest = OUT / f"{ad['n']:02d}_{ad['slug']}_{tag}.png"
    if dest.exists():
        return ad, str(dest), "skip-exists"
    try:
        if model == "nano":
            res = kie.generate_nano_banana(ad["prompt"], image_urls=refs)
        else:
            res = kie.generate_gpt_image(ad["prompt"], image_urls=refs,
                                         aspect_ratio=ad["aspect"], resolution="2K")
    except Exception as e:
        return ad, None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return ad, None, f"fail:{res.get('failMsg','')[:120]}"
    kie.download(res["urls"][0], dest)
    return ad, str(dest), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--only", default="")
    ap.add_argument("--model", default="gpt", choices=["gpt", "nano"])
    args = ap.parse_args()

    board = "/tmp/cilo_ref_board.png"   # 4 yellow angles + 2 grayscale hardware close-ups
    print(f"Uploading reference board: {board}", flush=True)
    board_url = kie.upload_file(board)
    refs = [board_url]
    print(f"refs: {refs}", flush=True)

    ads = ADS
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        ads = [a for a in ADS if a["slug"] in want]

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, refs, args.model): a for a in ads}
        for f in as_completed(futs):
            ad, path, status = f.result()
            print(f"[{status}] {ad['n']:02d} {ad['slug']} -> {path}", flush=True)
            results.append((ad["n"], ad["slug"], path, status))

    print("\n==== SUMMARY ====", flush=True)
    for n, slug, path, status in sorted(results):
        print(f"{n:02d} {slug:18s} {status:12s} {path or '-'}", flush=True)


if __name__ == "__main__":
    main()
