"""CILOCALA 'under 500g ultralight' UGC angle — 2 cuts. Board-anchored, no text."""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cilocala_ugc"); OUT.mkdir(parents=True, exist_ok=True)
BOARD = "/tmp/cilo_ref_board.png"
LOCK = ("Reproduce the EXACT backpack from the reference: pastel-yellow rounded-top nylon daypack, white FLAT silicone "
        "strap zipper pulls, front pocket with a horizontal webbing tape band and a white flat pull at the left, white "
        "barrel drawstring toggle with orange-and-white braided cord, white rounded-square 'CILO CALA' rubber logo patch. ")
UGC = ("Casual REAL-CUSTOMER UGC smartphone photo — authentic, slightly imperfect lighting, soft phone-camera look with a "
       "little grain, candid and un-staged, NOT a studio shot. Absolutely NO text, captions or graphics overlaid. ")
Y = "the pastel-yellow CILOCALA Classic backpack from the reference "

CUTS = [
    dict(slug="featherlight-finger", aspect="4:5",
         prompt=("A casual UGC phone photo of a person's hand holding " + Y + "dangling effortlessly from just two "
                 "fingers hooked through the top grab-handle, lifted up to show how light it is, in a real home or shop "
                 "with natural light. The bag hangs light and easy, arm relaxed. " + UGC + LOCK)),
    dict(slug="featherlight-scale", aspect="1:1",
         prompt=("A casual UGC 'weight-proof' phone photo: " + Y + "hanging from a small handheld luggage scale held up "
                 "by a hand, at home, the scale's small digital display visible (a low number). Looks like a real customer "
                 "weighing the bag for a review. " + UGC + LOCK)),
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
    BOARD_URL = kie.upload_file(BOARD)
    print(f"board_url: {BOARD_URL}", flush=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one, c): c for c in CUTS}
        for f in as_completed(futs):
            slug, path, status = f.result()
            print(f"[{status}] {slug} -> {path}", flush=True)
