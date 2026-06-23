"""
COSME CHEF — DAK BALM (tinted lip balm) UGC anchors — PERSONA ONLY (no product in shot).
6 white-woman (30-40) candidates, USA home, talking-to-camera UGC selfie. 9:16, 2K.
gpt-image-2 text-to-image. Pick one -> Seedance 10s i2v (spoken testimonial).
(Product-in-hand versions preserved in reference/with_product/.)
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/cosmechef_dakbalm/reference"); OUT.mkdir(parents=True, exist_ok=True)

UGC = ("Authentic real-customer UGC selfie shot on a front phone camera in a USA home: natural slightly imperfect "
       "lighting, soft phone-camera look with faint grain, candid and un-staged, NOT an advertising shot. Real skin "
       "with visible pores, fine lines, faint under-eye shadows, slight asymmetry, no heavy retouching, no filter, "
       "light natural everyday makeup. Eyes OPEN and looking straight into the camera lens, relaxed mid-conversation "
       "expression as if talking to the viewer. Vertical 9:16 head-and-shoulders selfie framing. Absolutely NO "
       "on-screen text, captions, watermarks, logos or graphics overlaid. ")

CUTS = [
    dict(slug="a_blonde_bathroom",
         prompt=("A white woman aged 30-40 with shoulder-length blonde hair, fresh dewy skin and a warm relaxed "
                 "half-smile, standing at a bright white bathroom mirror, soft morning daylight. " + UGC)),
    dict(slug="b_brunette_bedroom",
         prompt=("A white woman aged 30-40 with dark brown wavy hair, calm pleased expression talking to the camera, "
                 "soft natural window light in a cozy bedroom. " + UGC)),
    dict(slug="c_lightbrown_neutral",
         prompt=("A white woman aged 30-40 with light-brown straight hair and a friendly genuine expression, plain "
                 "warm-beige wall background, soft even daylight. " + UGC)),
    dict(slug="d_blonde_vanity",
         prompt=("A white woman aged 30-40 with loose wavy dark-blonde hair, one hand resting lightly near her jaw, "
                 "content expression, sitting at a vanity with soft warm bulb lighting. " + UGC)),
    dict(slug="e_auburn_kitchen",
         prompt=("A white woman aged 30-40 with auburn red shoulder-length hair and light freckles, small natural "
                 "smile, bright kitchen with daylight from a window behind. " + UGC)),
    dict(slug="f_darkblonde_window",
         prompt=("A white woman aged 30-40 with straight dark-blonde hair tucked behind one ear, looking directly at "
                 "the camera, soft bright daylight beside a large window, plain light wall. " + UGC)),
]


def run_one(c):
    dest = OUT / f"{c['slug']}.png"
    if dest.exists():
        return c['slug'], str(dest), "skip-exists"
    try:
        res = kie.generate_gpt_image(c["prompt"], aspect_ratio="9:16", resolution="2K")
    except Exception as e:
        return c['slug'], None, f"error:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return c['slug'], None, f"fail:{res.get('failMsg', res)}"
    kie.download(res["urls"][0], dest)
    return c['slug'], str(dest), "ok"


if __name__ == "__main__":
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(run_one, c): c for c in CUTS}
        for f in as_completed(futs):
            slug, path, status = f.result()
            print(f"[{status}] {slug} -> {path}", flush=True)
            results.append((slug, path, status))
    print("\n==== SUMMARY ====", flush=True)
    for slug, path, status in sorted(results):
        print(f"{slug:22s} {status:12s} {path or '-'}", flush=True)
