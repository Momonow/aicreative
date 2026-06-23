"""
Extend the 1:1 nano-banana composites (D + real product) to vertical 9:16 for the Seedance anchor.
gpt-image-2 i2i, aspect_ratio=9:16: keep the woman + product EXACTLY, add natural headroom + vanity below.
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cosmechef_dakbalm/anchor_D"); OUT.mkdir(parents=True, exist_ok=True)
SRC = ["v3_show_to_lens", "v2_near_jaw"]

PROMPT = ("Extend this exact photo to a vertical 9:16 portrait frame. KEEP the woman and the cosmetic stick she is "
          "holding EXACTLY as they already are — identical face, identical loose wavy dark-blonde hair, identical "
          "matte-black COSME CHEF tinted lip balm with its glossy RED domed balm tip and white 'COSME CHEF' logo, "
          "identical vanity setting with soft warm bulb lighting and identical UGC front-phone-camera look. Do NOT "
          "change, restyle or re-pose her or the product. ONLY add natural photorealistic continuation: a little "
          "headroom above her head and more of her shoulders and the vanity counter below, so the framing becomes a "
          "tall 9:16 selfie. Real un-staged look, no on-screen text, no captions, no watermark, no graphics.")


def run_one(slug, url):
    dest = OUT / f"{slug}_916.png"
    if dest.exists():
        return slug, str(dest), "skip-exists"
    try:
        res = kie.generate_gpt_image(PROMPT, image_urls=[url], aspect_ratio="9:16", resolution="2K")
    except Exception as e:
        return slug, None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return slug, None, f"fail:{res.get('failMsg', res)}"
    kie.download(res["urls"][0], dest)
    return slug, str(dest), "ok"


if __name__ == "__main__":
    urls = {}
    for slug in SRC:
        p = f"outputs/cosmechef_dakbalm/anchor_D/{slug}.png"
        urls[slug] = kie.upload_file(p)
        print(f"uploaded {slug}: {urls[slug]}", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one, slug, urls[slug]): slug for slug in SRC}
        for f in as_completed(futs):
            slug, path, status = f.result()
            print(f"[{status}] {slug} -> {path}", flush=True)
            results.append((slug, path, status))
    print("\n==== SUMMARY ====", flush=True)
    for slug, path, status in sorted(results):
        print(f"{slug:18s} {status:12s} {path or '-'}", flush=True)
