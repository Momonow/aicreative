"""
CILOCALA ad TEMPLATES with product-placement placeholders.

Workflow: gpt-image-2 generates the ad design (background + Korean text + callouts) with an
EMPTY product zone (no AI-rendered bag), then PIL draws a crisp dotted-circle placeholder where
the REAL product photo will be composited later. Circle is sized SMALLER than the product so the
dotted line hides under the dropped-in product.

Run test:  .venv/bin/python scripts/cilocala_templates.py --only hero-colorblock,feature-board
Run all:   .venv/bin/python scripts/cilocala_templates.py
"""
import argparse, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_templates"); OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw"; RAW.mkdir(exist_ok=True)

NOTEXT = "Render any Korean text as clean, correctly-spelled, well-kerned Hangul — no gibberish. "
EMPTY = ("IMPORTANT: do NOT draw any backpack, bag, product or object — leave the product area "
         "completely EMPTY and clean for a real product photo to be composited in later. ")

# placeholder = list of (cx_frac, cy_frac, r_frac_of_width) circles
TEMPLATES = [
    dict(n=2, slug="hero-colorblock", aspect="1:1",
         holes=[(0.50, 0.45, 0.19)],
         prompt=("Minimal premium ad background TEMPLATE, square. A bold two-tone pastel color-block "
                 "background: left half soft lilac, right half soft mint, with a soft oval drop-shadow on "
                 "the floor in the lower center as if a product will stand there. " + EMPTY +
                 "Near the bottom center, a clean Korean headline: '가벼운데, 예쁘기까지.' and below it a small "
                 "letter-spaced wordmark 'CILOCALA'. Flat colors, generous empty center. " + NOTEXT)),
    dict(n=4, slug="feature-board", aspect="1:1",
         holes=[(0.50, 0.52, 0.17)],
         prompt=("E-commerce feature-callout ad TEMPLATE, square, clean soft butter-cream background. "
                 "Around an empty center, five minimal thin-line icon badges in soft pastel circles, each "
                 "with a short Korean label: top-left a feather '초경량'; mid-left a water-drop '발수 코팅'; "
                 "bottom-left a shopping-bag '데일리'; top-right a laptop '노트북 수납'; mid-right a document 'A4 수납'. "
                 "Top headline: '예쁜 가방인데, 할 건 다 해요'. " + EMPTY + NOTEXT)),
    dict(n=8, slug="review-proof", aspect="1:1",
         holes=[(0.30, 0.50, 0.18)],
         prompt=("Social-proof review ad TEMPLATE, square, clean soft-pink pastel background. The LEFT side is "
                 "left empty for a product photo. On the RIGHT, five gold star icons and a short Korean review "
                 "quote inside a soft rounded white card: '색 보고 샀다가, 가벼워서 또 삼'. A small accent badge reads "
                 "'누적 판매 10만'. " + EMPTY + NOTEXT)),
    dict(n=10, slug="event-drop", aspect="4:5",
         holes=[(0.50, 0.50, 0.19)],
         prompt=("Festive promotional event ad TEMPLATE, portrait 4:5, celebratory pastel background with subtle "
                 "confetti and a few balloons at the edges. A small 'NEW' tag top-left and a '20% OFF' ribbon flag "
                 "top-right. Korean headline near top: 'Carry Colors 이벤트', subtext: '단독 컬러 오픈'. Bottom row: three "
                 "tiny benefit chips '이벤트 기간 한정 / 오직 여기서만 / 지금 바로'. " + EMPTY +
                 "Keep the whole center empty for a product. " + NOTEXT)),
]


def dashed_circle(draw, cx, cy, r, color=(120, 120, 120), width=5, dash=11, gap=10):
    a = 0
    while a < 360:
        draw.arc([cx - r, cy - r, cx + r, cy + r], a, a + dash, fill=color, width=width)
        a += dash + gap


def add_placeholders(img_path, holes, out_path):
    im = Image.open(img_path).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    for (cxf, cyf, rf) in holes:
        cx, cy, r = cxf * W, cyf * H, rf * W
        dashed_circle(d, cx, cy, r, color=(110, 110, 110), width=max(4, W // 380))
        # center cross
        s = r * 0.10
        d.line([cx - s, cy, cx + s, cy], fill=(110, 110, 110), width=max(2, W // 700))
        d.line([cx, cy - s, cx, cy + s], fill=(110, 110, 110), width=max(2, W // 700))
    im.save(out_path)
    return out_path


def run_one(t):
    raw = RAW / f"{t['n']:02d}_{t['slug']}_raw.png"
    final = OUT / f"{t['n']:02d}_{t['slug']}_template.png"
    if not raw.exists():
        try:
            res = kie.generate_gpt_image(t["prompt"], aspect_ratio=t["aspect"], resolution="2K")
        except Exception as e:
            return t, None, f"error:{e}"
        if res.get("status") != "success" or not res.get("urls"):
            return t, None, f"fail:{res.get('failMsg','')[:120]}"
        kie.download(res["urls"][0], raw)
    add_placeholders(raw, t["holes"], final)
    return t, str(final), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    ts = TEMPLATES
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        ts = [t for t in TEMPLATES if t["slug"] in want]
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, t): t for t in ts}
        for f in as_completed(futs):
            t, path, status = f.result()
            print(f"[{status}] {t['n']:02d} {t['slug']} -> {path}", flush=True)
            results.append((t["n"], t["slug"], path, status))
    print("\n==== SUMMARY ====", flush=True)
    for n, slug, path, status in sorted(results):
        print(f"{n:02d} {slug:18s} {status:12s} {path or '-'}", flush=True)


if __name__ == "__main__":
    main()
