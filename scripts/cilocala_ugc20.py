"""CILOCALA testimonial UGC ads — 20 distinct cuts, authentic real-customer phone-photo style.
No text in image (testimonial = primary text). Board-anchored yellow for product fidelity.
Run (bg):  .venv/bin/python scripts/cilocala_ugc20.py --workers 6
"""
import argparse, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_ugc20"); OUT.mkdir(parents=True, exist_ok=True)
BOARD = "/tmp/cilo_ref_board.png"
LOCK = ("Reproduce the EXACT backpack from the reference: pastel-yellow rounded-top nylon daypack, white FLAT silicone "
        "strap zipper pulls, front pocket with a horizontal webbing tape band and a white flat pull at the left, white "
        "barrel drawstring toggle with orange-and-white braided cord, white rounded-square 'CILO CALA' rubber logo patch, "
        "side slip pockets. Keep the bag faithful. ")
UGC = ("Casual REAL-CUSTOMER UGC smartphone photo — authentic, slightly imperfect natural lighting, soft phone-camera "
       "look with a little grain, candid and un-staged, looks like a real review photo, NOT a studio/ad shot. "
       "Absolutely NO text, captions, watermarks or graphics overlaid. ")
Y = "the pastel-yellow CILOCALA Classic backpack from the reference "
def C(seg, slug, aspect, scene): return dict(seg=seg, slug=slug, aspect=aspect, prompt=scene+UGC+LOCK)

CUTS = [
 # 초등 (6) — kids back/side view (faces not focal), parent-shot feel
 C("elem","elem-frontdoor","4:5", "A young Korean elementary child seen from behind at an apartment front door / entryway (shoes, hallway), wearing "+Y+"on both shoulders, morning, about to leave for school. "),
 C("elem","elem-desk-pack","4:5", "Casual close shot of a child's hands putting textbooks and a pencil case into "+Y+"open on a desk at home, top-down-ish. "),
 C("elem","elem-livingroom","4:5", "A young child seen from behind in a bright living room (sofa, TV), wearing "+Y+", relaxed home snapshot in the afternoon. "),
 C("elem","elem-schoolgate","4:5", "A young child walking toward a school gate, back view, wearing "+Y+", morning daylight, a few other kids blurred in the background. "),
 C("elem","elem-floor","1:1", Y+"sitting on a living-room floor next to a child's scattered school items (water bottle, notebook, crayons), casual real home photo. "),
 C("elem","elem-light-hand","4:5", "An adult's hand easily holding "+Y+"up with one hand inside a home, showing how light it is for a child to carry. "),
 # 중고등 (7)
 C("teen","teen-hallway","4:5", "A Korean high-school student in summer uniform, seen from the side/behind, wearing "+Y+"in a bright school hallway with windows, daytime. "),
 C("teen","teen-busstop","4:5", "A Korean teen student at a morning bus stop wearing "+Y+", casual school clothes, candid commute moment. "),
 C("teen","teen-desk-books","1:1", Y+"on a chair beside a study desk piled with textbooks and workbooks, a student's room, lamp light. "),
 C("teen","teen-device","4:5", "A teen's hands sliding a tablet and a thin laptop into the padded sleeve of "+Y+"at a desk. "),
 C("teen","teen-studycafe","4:5", Y+"hung on the back of a study-cafe chair, an open notebook and an iced drink on the table, cozy daylight. "),
 C("teen","teen-mirror","4:5", "A Korean teen taking a casual mirror selfie (phone in front of face) wearing "+Y+"in trendy casual clothes at home. "),
 C("teen","teen-locker","4:5", "A student holding "+Y+"by school lockers in a hallway, candid, daytime. "),
 # 여행/데일리 (7)
 C("travel","travel-gate","4:5", Y+"resting on an airport boarding-gate seat next to a passport and boarding pass, big windows with daylight, planes blurred outside. "),
 C("travel","travel-cafe","4:5", Y+"on a chair at an outdoor street cafe in a travel setting, sunny, a coffee cup on the table. "),
 C("travel","travel-rain","1:1", Y+"sitting on a windowsill by a rainy window, clear water droplets beading on its surface, soft indoor light. "),
 C("travel","travel-packed","4:5", Y+"open on a bed, packed with neatly folded clothes and small toiletries for a short trip, casual top-down. "),
 C("travel","travel-street","4:5", "An adult walking a city street wearing "+Y+", candid shot from behind, daytime, lifestyle. "),
 C("travel","travel-finger","4:5", "A hand holding "+Y+"dangling lightly from two fingers outdoors near a cafe, showing how light it is, travel-day mood. "),
 C("travel","travel-deskchair","1:1", Y+"hanging on the back of an office/home-desk chair in the morning, a laptop and mug on the desk, daily-commute mood. "),
]


def run_one(i, c):
    n = i + 1
    dest = OUT / f"{n:02d}_{c['seg']}_{c['slug']}.png"
    if dest.exists():
        return n, c['slug'], str(dest), "skip-exists"
    try:
        res = kie.generate_gpt_image(c["prompt"], image_urls=[BOARD_URL], aspect_ratio=c["aspect"], resolution="2K")
    except Exception as e:
        return n, c['slug'], None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return n, c['slug'], None, f"fail:{res.get('failMsg','')[:100]}"
    kie.download(res["urls"][0], dest)
    return n, c['slug'], str(dest), "ok"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=6); args = ap.parse_args()
    BOARD_URL = kie.upload_file(BOARD)
    print(f"board_url: {BOARD_URL}\nGenerating {len(CUTS)} UGC cuts...", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, i, c): c for i, c in enumerate(CUTS)}
        for f in as_completed(futs):
            n, slug, path, status = f.result()
            print(f"[{status}] {n:02d} {slug} -> {path}", flush=True)
            results.append((n, slug, status))
    ok = sum(1 for _, _, s in results if s in ("ok", "skip-exists"))
    print(f"\n{ok}/{len(CUTS)} done", flush=True)
