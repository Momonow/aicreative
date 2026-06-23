"""
CILOCALA testimonial UGC images — TEST (3 cuts, one per target).
Authentic real-customer phone-photo look, NO text (testimonial lives in primary text).
gpt-image-2 i2i anchored on the yellow reference board for product fidelity.
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_ugc"); OUT.mkdir(parents=True, exist_ok=True)
BOARD = "/tmp/cilo_ref_board.png"

LOCK = ("Reproduce the EXACT backpack from the reference: pastel-yellow rounded-top nylon daypack, white FLAT "
        "silicone strap zipper pulls (two on the top zipper), front pocket with a horizontal webbing tape band and a "
        "white flat pull at the left, white barrel drawstring toggle with orange-and-white braided cord, white "
        "rounded-square 'CILO CALA' rubber logo patch, side slip pockets. ")
UGC = ("Casual REAL-CUSTOMER UGC smartphone photo — looks like an authentic review photo a customer posted: natural, "
       "slightly imperfect lighting, soft phone-camera look with a little grain, candid and un-staged, NOT a studio or "
       "advertising shot. Absolutely NO text, captions, watermarks or logos overlaid. ")
Y = "the pastel-yellow CILOCALA Classic backpack from the reference "

CUTS = [
    dict(slug="elem-siblings", aspect="4:5",
         prompt=("A young Korean elementary-school child seen from BEHIND (back view, face not visible) wearing " + Y +
                 "on both shoulders, standing in a real Korean apartment living room (TV, sofa, light wood floor), "
                 "afternoon daylight. The yellow backpack is the clear focal point. " + UGC + LOCK)),
    dict(slug="teen-popular", aspect="4:5",
         prompt=("A Korean middle/high-school student (early teens) wearing " + Y + "on both shoulders, seen from "
                 "behind and slightly to the side, at a school hallway or a bus stop, casual school-style clothes, "
                 "daytime. Candid everyday moment. " + UGC + LOCK)),
    dict(slug="travel-carryon", aspect="4:5",
         prompt=(Y + "clipped onto the telescopic handle of a small carry-on suitcase inside an airport terminal "
                 "near a boarding gate, large windows with daylight, a few blurred travelers in the background. "
                 "Looks like a quick phone snap right before a trip. " + UGC + LOCK)),
]


def run_one(c):
    dest = OUT / f"{c['slug']}.png"
    if dest.exists():
        return c['slug'], str(dest), "skip-exists"
    try:
        res = kie.generate_gpt_image(c["prompt"], image_urls=[BOARD_URL], aspect_ratio=c["aspect"], resolution="2K")
    except Exception as e:
        return c['slug'], None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return c['slug'], None, f"fail:{res.get('failMsg','')[:120]}"
    kie.download(res["urls"][0], dest)
    return c['slug'], str(dest), "ok"


if __name__ == "__main__":
    print(f"Uploading board: {BOARD}", flush=True)
    BOARD_URL = kie.upload_file(BOARD)
    print(f"board_url: {BOARD_URL}", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(run_one, c): c for c in CUTS}
        for f in as_completed(futs):
            slug, path, status = f.result()
            print(f"[{status}] {slug} -> {path}", flush=True)
            results.append((slug, path, status))
    print("\n==== SUMMARY ====", flush=True)
    for slug, path, status in results:
        print(f"{slug:18s} {status:12s} {path or '-'}", flush=True)
