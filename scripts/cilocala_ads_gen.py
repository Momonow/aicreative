"""
CILOCALA Facebook image-ad batch — 10 concepts.
gpt-image-2 image-to-image (KIE) anchored on the pink CILOCALA Classic backpack.

Run:  .venv/bin/python scripts/cilocala_ads_gen.py [--anchor /path/to/bag.jpg]
Skip-if-exists: re-running only regenerates missing outputs.
"""
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_ads")
OUT.mkdir(parents=True, exist_ok=True)

BAG = ("the SAME pastel-pink CILOCALA Classic backpack from the reference image — "
       "matte nylon body, rounded top with a white barrel drawstring toggle and a thin "
       "pink-and-white cord, a white rounded-square rubber logo patch debossed 'CILO CALA' "
       "on the upper front, a front zip pocket with a flat webbing pull, a side slip pocket, "
       "white zipper pulls. Keep the bag's exact design, proportions and logo. ")

NOTEXT = ("Render any Korean text as clean, correctly-spelled, well-kerned Hangul — "
          "absolutely no gibberish, no broken or fake letters. ")

ADS = [
    dict(n=1, slug="color-grid", aspect="1:1",
         prompt=(f"Clean studio e-commerce ad. A neat 3x3 grid of {BAG}"
                 "but each of the 9 backpacks is a different cheerful colorway — "
                 "butter yellow, blush pink, mint, sky blue, lilac, coral, cream, sage green, lavender; "
                 "only the body color changes, the white logo patch and white zippers stay the same on all. "
                 "Bright soft-white background, soft natural shadows. Big bold playful rounded sans-serif "
                 "Korean headline at top center: '오늘 기분, 무슨 컬러?' and a smaller tagline below: 'Carry Colors!'. "
                 "Modern, colorful, minimal, premium. " + NOTEXT)),
    dict(n=2, slug="hero-colorblock", aspect="1:1",
         prompt=(f"Premium minimal product ad. {BAG}"
                 "shown floating centered on a bold two-tone pastel color-block background "
                 "(left half soft lilac, right half soft mint), clean soft studio shadow, lots of negative space. "
                 "Short Korean headline near the bottom center: '가벼운데, 예쁘기까지.' and a small wordmark 'CILOCALA'. "
                 "Flat colors, editorial, clean. " + NOTEXT)),
    dict(n=3, slug="whats-in-bag", aspect="4:5",
         prompt=(f"Top-down flatlay ad. {BAG}"
                 "shown open with neatly arranged everyday items around it: a slim laptop, a tumbler, "
                 "a small makeup pouch, an earbuds case, a paperback book, a keyring — all in matching "
                 "pastel pink and cream tones on a soft beige surface, styled and aesthetic. "
                 "Thin Korean callout labels with hairlines pointing to a few items: '15인치 노트북', '텀블러 칸', '파우치'. "
                 "Top headline: '데일리, 이거 하나면 끝'. Bright, clean. " + NOTEXT)),
    dict(n=4, slug="feature-board", aspect="1:1",
         prompt=(f"E-commerce feature-callout ad. {BAG}"
                 "at a 3/4 angle, centered on a clean pastel background. Around it, five minimal "
                 "line-icon + short Korean label callouts evenly placed: '초경량', '노트북 수납', '발수 코팅', "
                 "'A4 수납', '데일리'. Top headline: '예쁜 가방인데, 할 건 다 해요'. "
                 "Modern colorful-minimal layout, soft shadows. " + NOTEXT)),
    dict(n=5, slug="size-guide", aspect="4:5",
         prompt=(f"Product size-guide ad. Three of {BAG}"
                 "in three sizes (small, medium, large) lined up left-to-right on a clean pastel background, "
                 "all the same pink colorway, soft shadows. A small Korean label centered under each: "
                 "'S 데일리', 'M 스쿨', 'L 여행'. Top headline: '내 사이즈, 한눈에'. Clean and informative. " + NOTEXT)),
    dict(n=6, slug="ugc-native", aspect="4:5",
         prompt=(f"Casual UGC-style smartphone photo that looks like a real Instagram snapshot — "
                 f"slightly imperfect framing, natural window light, a little grain. {BAG}"
                 "sitting on a wooden cafe chair next to a window, a latte cup beside it. "
                 "Handwritten-style Korean caption overlaid casually: '요즘 메는 가방 추천받음… 색 미쳤다'. "
                 "Authentic, un-polished, warm tones, NOT a studio shot. " + NOTEXT)),
    dict(n=7, slug="lifestyle-onbody", aspect="4:5",
         prompt=("Photoreal lifestyle ad. A stylish young Korean woman in her early 20s walking on a "
                 f"sunny city street, wearing {BAG}"
                 "on both shoulders, candid natural stride, soft daylight, casual neutral outfit so the "
                 "pink bag is the color pop. Natural skin texture, real photo look. "
                 "Minimal small Korean text along the bottom: '메는 순간, 룩이 산다'. " + NOTEXT)),
    dict(n=8, slug="review-proof", aspect="1:1",
         prompt=(f"Social-proof review ad. {BAG}"
                 "on a clean pastel background, beside a five-star rating drawn as five gold stars "
                 "and a short Korean review quote inside a soft rounded white card: '색 보고 샀다가, 가벼워서 또 삼'. "
                 "A small accent badge reads '누적 판매 10만'. Trustworthy, clean, friendly. " + NOTEXT)),
    dict(n=9, slug="color-vs-black", aspect="1:1",
         prompt=("Side-by-side comparison ad, frame split in two vertical halves. LEFT half: a plain dull "
                 "BLACK backpack, desaturated and gloomy, muted gray background. RIGHT half: "
                 f"{BAG}bright, cheerful and vivid on a soft warm background. "
                 "Korean headline split across the two halves: left '다 똑같은 검정 말고,' right '오늘은, 컬러.'. "
                 "Strong before/after contrast. " + NOTEXT)),
    dict(n=10, slug="event-drop", aspect="4:5",
         prompt=(f"Festive promotional event ad. {BAG}"
                 "as the hero on a celebratory pastel background with subtle confetti, a small 'NEW' tag and a "
                 "discount ribbon flag in the corner, plus a small matching free-gift pouch graphic beside it. "
                 "Korean headline: 'Carry Colors 이벤트', and subtext below: '단독 컬러 오픈'. "
                 "Bright, celebratory, retail-promo energy. " + NOTEXT)),
]


def run_one(ad, bag_url):
    dest = OUT / f"{ad['n']:02d}_{ad['slug']}.png"
    if dest.exists():
        return ad, str(dest), "skip-exists"
    try:
        res = kie.generate_gpt_image(ad["prompt"], image_urls=[bag_url],
                                     aspect_ratio=ad["aspect"], resolution="2K")
    except Exception as e:
        return ad, None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return ad, None, f"fail:{res.get('failMsg','')[:120]}"
    kie.download(res["urls"][0], dest)
    return ad, str(dest), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchor", default="/tmp/cilo_pink.jpg")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--only", default="", help="comma slugs to limit, e.g. color-grid,feature-board")
    args = ap.parse_args()

    print(f"Uploading anchor: {args.anchor}", flush=True)
    bag_url = kie.upload_file(args.anchor)
    print(f"Anchor URL: {bag_url}", flush=True)

    ads = ADS
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        ads = [a for a in ADS if a["slug"] in want]

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, bag_url): a for a in ads}
        for f in as_completed(futs):
            ad, path, status = f.result()
            print(f"[{status}] {ad['n']:02d} {ad['slug']} -> {path}", flush=True)
            results.append((ad["n"], ad["slug"], path, status))

    print("\n==== SUMMARY ====", flush=True)
    for n, slug, path, status in sorted(results):
        print(f"{n:02d} {slug:18s} {status:12s} {path or '-'}", flush=True)


if __name__ == "__main__":
    main()
