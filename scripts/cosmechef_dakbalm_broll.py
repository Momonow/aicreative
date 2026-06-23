"""
DAK BALM application B-ROLL — FREE Veo 3.1 Lite (useapi google-flow), i2v from clip-1 frames.
She USES the product: swipes the balm on her lips. NO talking (testimonial VO plays underneath).
duration=6 (we use ~2.5s segments). Seeds from held-balm anchors; motion brings it to her lips.

Usage: python scripts/cosmechef_dakbalm_broll.py [1 2 3]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import googleflow_client as gf

DIR = Path("outputs/cosmechef_dakbalm")
ANCHOR_DIR = DIR / "anchor_D"
BROLL = DIR / "broll"; BROLL.mkdir(parents=True, exist_ok=True)

COMMON = (
    "B-ROLL, NO talking, no speech, she does NOT speak — her lips only move to apply the product.\n"
    "She applies the tinted lip balm: she brings the matte-black COSME CHEF balm stick up to her mouth and {motion}. "
    "CRITICAL: ONLY ONE single lip balm is EVER visible in the entire shot — she holds exactly one product in one "
    "hand; there is NO second product, NO duplicate balm, NO extra stick anywhere in the frame or in her other hand.\n"
    "Keep the same woman, same vanity setting and warm bulb lighting, same authentic phone-camera selfie look, slight "
    "natural handheld sway. Unhurried real movement.\n"
    "No on-screen text, no captions, no subtitles, no graphics."
)

BROLLS = {
    1: dict(anchor="clip1_firstframe.png",
            motion=("gently SWIPES the red balm across her lips a couple of times, then lowers it a little and looks "
                    "down at her lips, soft pleased expression")),
    2: dict(anchor="_anchor_1.jpg",
            motion=("swipes the balm across her lips and presses her lips together to blend the soft-red color, "
                    "eyes down toward her lips, small satisfied look")),
    3: dict(anchor="_anchor_2.jpg",
            motion=("dabs the balm onto the center of her lips, then rubs her lips together to spread the color, then "
                    "a soft closed-lip smile toward the camera")),
}


def gen(idx):
    dest = BROLL / f"broll{idx}.mp4"
    if dest.exists() and dest.stat().st_size > 10_000:
        return idx, str(dest), "skip-exists"
    spec = BROLLS[idx]
    anchor = ANCHOR_DIR / spec["anchor"]
    prompt = COMMON.format(motion=spec["motion"])
    print(f"\n=== BROLL {idx} === anchor={anchor.name}", flush=True)
    res = gf.generate_veo(prompt, image_path=str(anchor), duration=6, aspect_ratio="portrait")
    if res.get("status") != "success" or not res.get("urls"):
        return idx, None, f"fail:{str(res.get('raw'))[:200]}"
    gf.download(res["urls"][0], dest)
    return idx, str(dest), "ok"


if __name__ == "__main__":
    idxs = [int(a) for a in sys.argv[1:]] or [1, 2, 3]
    for i in idxs:
        try:
            r = gen(i)
        except Exception as e:
            r = (i, None, f"error:{e}")
        print(f"[{r[2]}] broll{r[0]} -> {r[1]}", flush=True)
