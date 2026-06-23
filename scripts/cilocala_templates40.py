"""
CILOCALA — 40 DISTINCT ad TEMPLATES (photo-insertable version only).

Each template: gpt-image-2 t2i generates background + Korean copy + callouts/decorative with an
EMPTY product zone (NO AI bag). PIL then draws a dotted-circle placeholder (slightly smaller than
the product) where the real product photo gets composited later.

Styles borrowed (adapted to CILOCALA's REAL strengths — no false anti-theft claims):
  Branden feature-board / problem-solution / social-proof / discount-promo,
  JanSport retailer lookbook, HDEX/Salomon spec-gorpcore, UGC-native, NatGeo-kids seasonal.

Run (background recommended):  .venv/bin/python scripts/cilocala_templates40.py --workers 6
Subset:                        .venv/bin/python scripts/cilocala_templates40.py --only feature-board-5icon,pain-shoulder
"""
import argparse, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_templates40"); OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw"; RAW.mkdir(exist_ok=True)

NT = "All Korean text must be clean, correctly-spelled, well-kerned Hangul — no gibberish, no fake letters. "
ST = "Bright Korean e-commerce performance-ad look, high-contrast conversion layout, flat clean design. "
def E(loc): return (f"CRITICAL: do NOT draw any backpack, bag or product anywhere — leave {loc} completely "
                    "EMPTY and clean (background only) for a real product photo to be composited later. ")

C = (0.50, 0.52, 0.18)  # default center hole

ADS = [
 # ---- A. Branden feature / spec ----
 dict(slug="feature-board-5icon", aspect="1:1", holes=[(0.5,0.54,0.16)],
   prompt=ST+"Feature-callout ad. Five minimal line-icon badges in soft pastel circles around an empty center, "
   "Korean labels: top-left feather '초경량', mid-left water-drop '발수', bottom-left shopping-bag '데일리', "
   "top-right laptop '노트북 수납', mid-right document 'A4 수납'. Top headline: '예쁜데, 할 건 다 해요'. "+E("the center")+NT),
 dict(slug="spec-checklist", aspect="1:1", holes=[(0.70,0.5,0.16)],
   prompt=ST+"Spec checklist ad. LEFT third: a clean checklist with green ticks — '✔ 초경량  ✔ 발수 코팅  ✔ 노트북 수납  "
   "✔ A4 수납  ✔ 데일리'. RIGHT two-thirds empty for product. Top headline: '체크, 다 됩니다'. "+E("the right side")+NT),
 dict(slug="single-feature-hero", aspect="4:5", holes=[(0.5,0.58,0.2)],
   prompt=ST+"Bold single-benefit ad. Huge Korean headline across the top: '멘 듯 안 멘 듯, 초경량'. Big empty lower area "
   "for product. Minimal pastel background. "+E("the lower-center")+NT),
 dict(slug="cutaway-capacity", aspect="4:5", holes=[(0.5,0.5,0.19)],
   prompt=ST+"Capacity explainer ad. Thin hairline callouts with small icons pointing inward toward an empty center "
   "(노트북 / A4 서류 / 텀블러 / 파우치). Top headline: '이게 다 들어가요'. "+E("the center")+NT),
 dict(slug="water-repellent", aspect="1:1", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Water-repellent feature ad. Scattered crisp water droplets and a soft splash motif around an empty center. "
   "Headline: '비 와도 끄떡없이, 발수'. "+E("the center")+NT),
 dict(slug="weight-scale", aspect="1:1", holes=[(0.5,0.44,0.16)],
   prompt=ST+"Lightweight ad. A simple flat kitchen-scale graphic sitting at the bottom-center with an empty space above its "
   "platform for the product. Headline: '이 가벼움, 실화?'. "+E("the area above the scale platform")+NT),
 dict(slug="dimensions-spec", aspect="1:1", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Blueprint dimensions ad. Thin measurement arrows and cm guide lines (height/width/depth) framing an empty "
   "center. Headline: '딱 맞는 데일리 사이즈'. "+E("the center")+NT),
 dict(slug="chest-belt", aspect="4:5", holes=[(0.5,0.52,0.18)],
   prompt=ST+"Comfort feature ad. A single callout pointing to where a chest strap would be, around an empty product zone. "
   "Headline: '흘러내림 없이, 체스트벨트'. "+E("the center")+NT),
 dict(slug="laptop-pocket", aspect="1:1", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Laptop-pocket feature ad. A laptop line-icon callout beside an empty product zone. Headline: '노트북도 안심'. "
   +E("the center")+NT),
 dict(slug="side-pocket-tumbler", aspect="1:1", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Side-pocket feature ad. A tumbler/water-bottle line-icon callout beside an empty product zone. Headline: "
   "'텀블러 쏙, 사이드 포켓'. "+E("the center")+NT),
 # ---- B. Branden problem / hook ----
 dict(slug="pain-shoulder", aspect="4:5", holes=[(0.5,0.6,0.18)],
   prompt=ST+"Problem-solution ad. TOP: a simple illustration of slumped, aching shoulders weighed down (muted gray). "
   "BOTTOM: bright empty area for the light product. Headline: '어깨 빠지던 가방, 이제 안녕'. "+E("the lower half")+NT),
 dict(slug="pain-messy", aspect="1:1", holes=[(0.64,0.5,0.16)],
   prompt=ST+"Before/after organization ad. LEFT: messy scattered daily items (muted). RIGHT: empty product zone. "
   "Headline: '가방 속 대참사, 정리 끝'. "+E("the right side")+NT),
 dict(slug="pain-boring-black", aspect="1:1", holes=[(0.72,0.5,0.17)],
   prompt=ST+"Comparison ad split in two. LEFT: a dull plain BLACK backpack, desaturated, gloomy gray background. "
   "RIGHT: a bright warm pastel half with an empty product zone. Headline split: left '다 똑같은 검정 말고,' right '오늘은, 컬러.'. "
   +E("the right half")+NT),
 dict(slug="pain-wet", aspect="1:1", holes=[(0.5,0.52,0.18)],
   prompt=ST+"Rainy-day ad. Soft rain streaks and a cloud motif at the top, bright below. Headline: '갑자기 비 와도, 발수라 OK'. "
   +E("the center")+NT),
 dict(slug="question-hook", aspect="1:1", holes=[(0.5,0.58,0.17)],
   prompt=ST+"Curiosity-hook ad. Big Korean question across the top: '가방 살 때, 이거 확인했어요?'. Empty product zone below. "
   +E("the lower-center")+NT),
 # ---- C. Branden social proof / authority ----
 dict(slug="bestseller-badge", aspect="1:1", holes=[(0.5,0.52,0.17)],
   prompt=ST+"Bestseller ad. A bold ribbon/seal badge reading '누적 판매 10만' and a row of five gold stars near the top, "
   "empty product zone in the center. Headline: '괜히 베스트가 아니에요'. "+E("the center")+NT),
 dict(slug="staff-pick", aspect="4:5", holes=[(0.5,0.58,0.17)],
   prompt=ST+"Staff-testimonial ad. A speech bubble near the top: '직원이 진짜 매일 메는 가방'. Empty product zone below. "
   +E("the lower-center")+NT),
 dict(slug="review-quote", aspect="1:1", holes=[(0.30,0.5,0.16)],
   prompt=ST+"Review ad. LEFT empty for product. RIGHT: five gold stars over a soft rounded white quote card: "
   "'색 보고 샀다가, 가벼워서 또 삼'. "+E("the left side")+NT),
 dict(slug="review-collage", aspect="4:5", holes=[(0.5,0.64,0.15)],
   prompt=ST+"Review-collage ad. TOP: three small soft review-snippet bubbles with star rows. BOTTOM: empty product zone. "
   "Headline: '후기가 증명해요'. "+E("the lower-center")+NT),
 dict(slug="rank-1-badge", aspect="1:1", holes=[(0.5,0.54,0.17)],
   prompt=ST+"Ranking ad. A trophy/'1위' laurel badge near the top reading '백팩 카테고리 1위'. Empty product zone center. "
   +E("the center")+NT),
 dict(slug="as-seen-press", aspect="1:1", holes=[(0.5,0.56,0.16)],
   prompt=ST+"As-featured ad. A thin top strip of faux media/logo chips with '○○ 추천' captions. Empty product zone below. "
   "Headline: '여기저기서 먼저 알아본 가방'. "+E("the center-lower")+NT),
 # ---- D. Branden value / promo ----
 dict(slug="discount-ribbon", aspect="1:1", holes=[(0.5,0.54,0.17)],
   prompt=ST+"Discount ad. A bold red corner ribbon flag reading '단독 ~25% 🔥' in the top-right, empty product zone center. "
   "Headline: 'Carry Colors 단독가'. "+E("the center")+NT),
 dict(slug="value-pick", aspect="1:1", holes=[(0.5,0.55,0.17)],
   prompt=ST+"Value-shock ad. A huge playful Korean phrase top: '이 가격에, 컬러까지?!'. Empty product zone below. "
   +E("the lower-center")+NT),
 dict(slug="fomo-soldout", aspect="4:5", holes=[(0.5,0.56,0.17)],
   prompt=ST+"Urgency ad. A bold banner near the top: '품절 임박 🔥 한정 컬러'. Empty product zone below. "+E("the lower-center")+NT),
 dict(slug="bundle-gift", aspect="4:5", holes=[(0.42,0.5,0.17),(0.76,0.66,0.09)],
   prompt=ST+"Gift-with-purchase ad. LEFT empty zone for the main product, and a SMALLER empty zone at lower-right for a "
   "free pouch, with a '+증정' tag between them. Headline: '지금 사면, 파우치 증정'. "+E("both empty zones (large + small)")+NT),
 dict(slug="timer-limited", aspect="1:1", holes=[(0.5,0.56,0.16)],
   prompt=ST+"Limited-time ad. A calendar/clock motif near the top with '기간 한정'. Empty product zone below. "+E("the lower-center")+NT),
 dict(slug="coupon-newmember", aspect="4:5", holes=[(0.5,0.56,0.17)],
   prompt=ST+"Coupon ad. A dashed-edge coupon graphic near the top reading '신규가입 1만원 쿠폰'. Empty product zone below. "
   +E("the lower-center")+NT),
 # ---- E. multi-use / lifestyle framing ----
 dict(slug="one-bag-all", aspect="4:5", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Multi-use ad. Three small scene icons spaced around an empty center — 출근 / 학교 / 여행. Headline: '이거 하나면 끝'. "
   +E("the center")+NT),
 dict(slug="day-to-night", aspect="1:1", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Day-to-night ad. Background gradient from bright morning (left) to warm evening (right). Headline: "
   "'데일리부터 나들이까지'. "+E("the center")+NT),
 dict(slug="tpo-grid", aspect="1:1", holes=[(0.29,0.36,0.10),(0.71,0.36,0.10),(0.29,0.72,0.10),(0.71,0.72,0.10)],
   prompt=ST+"Four-scene TPO grid ad, 2x2 quadrants divided by thin lines, each quadrant labeled in Korean — "
   "통학 / 출근 / 여행 / 데이트 — and each has an empty circular product spot. Center title: 'TPO 다 되는 데일리백'. "
   +E("all four quadrant spots")+NT),
 # ---- F. retailer / lookbook ----
 dict(slug="bestseller-zip", aspect="1:1", holes=[(0.5,0.56,0.17)],
   prompt=ST+"Retailer lookbook ad, clean minimal. Top headline like a folder: '가장 많이 찾는 백팩 모음.zip'. Empty product zone "
   "below. Calm, premium. "+E("the center-lower")+NT),
 dict(slug="color-lineup", aspect="4:5", holes=[(0.18,0.52,0.085),(0.34,0.52,0.085),(0.5,0.52,0.085),(0.66,0.52,0.085),(0.82,0.52,0.085)],
   prompt=ST+"Color-lineup lookbook ad. Five empty product slots in a single neat row on a clean light shelf. Headline: "
   "'전 컬러, 골라 메세요'. small 'Carry Colors!'. "+E("all five slots in the row")+NT),
 dict(slug="new-color-drop", aspect="4:5", holes=[(0.5,0.54,0.2)],
   prompt=ST+"New-color drop ad. A 'NEW 컬러' tag near the top, festive but minimal. Big empty hero product zone. Headline: "
   "'새 컬러, 오픈'. "+E("the center")+NT),
 # ---- G. UGC native ----
 dict(slug="ugc-cafe", aspect="4:5", holes=[(0.5,0.52,0.19)],
   prompt=ST+"Casual UGC-style phone snapshot — a wooden cafe chair by a window with a latte nearby, natural light, slight "
   "grain, looks like a real Instagram post. Leave the chair seat empty for a bag. Handwritten Korean caption: "
   "'요즘 메는 가방 추천받음… 색 미쳤다'. "+E("the cafe chair seat")+NT),
 dict(slug="ugc-school", aspect="4:5", holes=[(0.5,0.55,0.18)],
   prompt=ST+"Casual UGC desk-flatlay snapshot — notebooks, pens, a coffee on a light desk, top-down, real-post feel. Leave a "
   "clear empty spot for a bag. Handwritten Korean caption: '신학기 가방 고민이면 이거 보고 가'. "+E("the empty desk spot")+NT),
 dict(slug="influencer-open", aspect="4:5", holes=[(0.5,0.55,0.18)],
   prompt=ST+"Influencer story-style ad, phone-screen vibe with a soft sticker frame. Top Korean caption: '오늘 컬러 오픈 🤍'. "
   "Empty product zone below. "+E("the lower-center")+NT),
 dict(slug="comment-flood", aspect="4:5", holes=[(0.5,0.4,0.17)],
   prompt=ST+"UGC ad. TOP: empty product zone on a simple soft background. BOTTOM: a faux social comment thread with a few "
   "Korean comments — '이거 어디꺼??', '링크 주세요!!', '색 예쁘다'. "+E("the upper-center")+NT),
 dict(slug="ugc-best-buy", aspect="4:5", holes=[(0.5,0.52,0.19)],
   prompt=ST+"Cozy home UGC snapshot — a bed/sofa corner with soft daylight, real-post feel. Leave a clear empty spot for a bag. "
   "Handwritten Korean caption: '올해 산 것 중 1위 💛'. "+E("the empty spot")+NT),
 # ---- H. spec / gorpcore / seasonal ----
 dict(slug="season-newterm", aspect="4:5", holes=[(0.5,0.55,0.18)],
   prompt=ST+"Back-to-school seasonal ad, bright and cheerful with confetti and a few stationery doodles at the edges. Headline: "
   "'신학기, 가볍게 시작'. Empty product zone center. "+E("the center")+NT),
 dict(slug="gorpcore-price", aspect="1:1", holes=[(0.5,0.5,0.18)],
   prompt=ST+"Minimal gorpcore spec ad, clean and slightly techy. A small price tag chip reads '₩59,000'. Empty product zone "
   "center. Headline: '가볍게, 슬림하게'. "+E("the center")+NT),
]


def dashed_circle(d, cx, cy, r, color=(110,110,110), width=5, dash=11, gap=10):
    a = 0
    while a < 360:
        d.arc([cx-r, cy-r, cx+r, cy+r], a, a+dash, fill=color, width=width); a += dash+gap


def add_placeholders(raw, holes, out):
    im = Image.open(raw).convert("RGB"); W, H = im.size; d = ImageDraw.Draw(im)
    for (cxf, cyf, rf) in holes:
        cx, cy, r = cxf*W, cyf*H, rf*W
        dashed_circle(d, cx, cy, r, width=max(4, W//420))
        s = r*0.10
        d.line([cx-s, cy, cx+s, cy], fill=(110,110,110), width=max(2, W//800))
        d.line([cx, cy-s, cx, cy+s], fill=(110,110,110), width=max(2, W//800))
    im.save(out); return out


def run_one(i, ad):
    n = i + 1
    raw = RAW / f"{n:02d}_{ad['slug']}_raw.png"
    final = OUT / f"{n:02d}_{ad['slug']}.png"
    if final.exists():
        return n, ad['slug'], str(final), "skip-exists"
    if not raw.exists():
        try:
            res = kie.generate_gpt_image(ad["prompt"], aspect_ratio=ad["aspect"], resolution="2K")
        except Exception as e:
            return n, ad['slug'], None, f"error:{e}"
        if res.get("status") != "success" or not res.get("urls"):
            return n, ad['slug'], None, f"fail:{res.get('failMsg','')[:100]}"
        kie.download(res["urls"][0], raw)
    add_placeholders(raw, ad["holes"], final)
    return n, ad['slug'], str(final), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    items = list(enumerate(ADS))
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        items = [(i, a) for i, a in items if a["slug"] in want]
    print(f"Generating {len(items)} templates...", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, i, a): a for i, a in items}
        for f in as_completed(futs):
            n, slug, path, status = f.result()
            print(f"[{status}] {n:02d} {slug} -> {path}", flush=True)
            results.append((n, slug, path, status))
    print("\n==== SUMMARY ====", flush=True)
    ok = 0
    for n, slug, path, status in sorted(results):
        print(f"{n:02d} {slug:22s} {status:12s} {path or '-'}", flush=True)
        if status in ("ok", "skip-exists"): ok += 1
    print(f"\n{ok}/{len(items)} done", flush=True)


if __name__ == "__main__":
    main()
