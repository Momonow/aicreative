"""
Composite the REAL DAK BALM (black tube, red domed balm tip) into face D (d_blonde_vanity).
nano-banana-2 multi-image edit: keep the woman + vanity setting from image 1, place the EXACT
product from image 2 in her hand. 3 hold-pose variants. Pick best -> Seedance 10s i2v anchor.
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cosmechef_dakbalm/anchor_D"); OUT.mkdir(parents=True, exist_ok=True)
FACE = "outputs/cosmechef_dakbalm/reference/d_blonde_vanity.png"
PRODUCT = "outputs/cosmechef_dakbalm/product/dak_balm_real.jpg"

KEEP = ("KEEP the woman from the FIRST image exactly the same — same face and identity, same loose wavy dark-blonde "
        "hair, same vanity setting with soft warm bulb lighting, same natural skin and light makeup, same UGC "
        "front-phone-camera selfie look, vertical 9:16 framing. She looks straight into the lens, relaxed "
        "mid-conversation expression, lips slightly parted as if talking. ")
PROD = ("Place into her hand the EXACT product from the SECOND image: a small twist-up cosmetic stick with a MATTE "
        "BLACK tube (a wider matte-black base printed with a small white 'COSME CHEF' wordmark and bracket logo, plus "
        "a glossy black upper barrel) and a glossy RED / terracotta-orange DOMED tinted balm tip exposed at the top. "
        "Keep the product's real colors, proportions and logo faithful and clearly readable. Use ONLY the product "
        "object from the second image — her OWN hand and the vanity background, NOT the hand or room from the second "
        "image. ")
CLEAN = "Real un-staged UGC selfie, no on-screen text, no captions, no watermark, no graphics. "

CUTS = [
    dict(slug="v1_beside_cheek",
         prompt=("She holds the product up beside her cheek with the RED balm tip and COSME CHEF logo facing the "
                 "camera, clearly visible and in focus. " + KEEP + PROD + CLEAN)),
    dict(slug="v2_near_jaw",
         prompt=("She holds the product near her jaw at chest height, turned so the red tip and logo face the camera. "
                 + KEEP + PROD + CLEAN)),
    dict(slug="v3_show_to_lens",
         prompt=("She holds the product up between her fingers near her chin, presenting it toward the camera so the "
                 "red domed balm tip and the COSME CHEF logo are clearly shown. " + KEEP + PROD + CLEAN)),
]


def run_one(c, face_url, product_url):
    dest = OUT / f"{c['slug']}.png"
    if dest.exists():
        return c['slug'], str(dest), "skip-exists"
    try:
        res = kie.generate_nano_banana(c["prompt"], image_urls=[face_url, product_url])
    except Exception as e:
        return c['slug'], None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return c['slug'], None, f"fail:{res.get('failMsg', res)}"
    kie.download(res["urls"][0], dest)
    return c['slug'], str(dest), "ok"


if __name__ == "__main__":
    print(f"Uploading face: {FACE}", flush=True)
    face_url = kie.upload_file(FACE)
    print(f"Uploading product: {PRODUCT}", flush=True)
    product_url = kie.upload_file(PRODUCT)
    print(f"face_url: {face_url}\nproduct_url: {product_url}", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(run_one, c, face_url, product_url): c for c in CUTS}
        for f in as_completed(futs):
            slug, path, status = f.result()
            print(f"[{status}] {slug} -> {path}", flush=True)
            results.append((slug, path, status))
    print("\n==== SUMMARY ====", flush=True)
    for slug, path, status in sorted(results):
        print(f"{slug:18s} {status:12s} {path or '-'}", flush=True)
