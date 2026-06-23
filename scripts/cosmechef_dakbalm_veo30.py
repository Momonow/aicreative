"""
COSME CHEF — DAK BALM — 30s testimonial, FREE Veo 3.1 Lite (useapi google-flow), 4x ~8s clips.
She HOLDS the product the whole time (never applies it). startImage i2v.
Clip 1 = user's first frame; clips 2-4 = rotated eyes-open anchors from clip 1 (fallback: first frame).

Usage:  python scripts/cosmechef_dakbalm_veo30.py 1          # generate clip 1
        python scripts/cosmechef_dakbalm_veo30.py 2 3 4      # generate clips 2-4
        python scripts/cosmechef_dakbalm_veo30.py            # all
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import googleflow_client as gf

DIR = Path("outputs/cosmechef_dakbalm")
ANCHOR_DIR = DIR / "anchor_D"
CLIPS = DIR / "clips"; CLIPS.mkdir(parents=True, exist_ok=True)
FIRST_FRAME = ANCHOR_DIR / "clip1_firstframe.png"

BEATS = {
    1: "Okay, I have to talk about this tinted lip balm, because I am genuinely obsessed with it.",
    2: "It's the Dak Balm from Cosme Chef. This perfect soft red. My lips, but better.",
    3: "And it's a balm, so it's hydrating. My lips never feel dry, they just look healthy.",
    4: "It takes me two seconds in the morning, and that's it. I'm never going back to dry lipstick.",
}

TEMPLATE = (
    "She holds the lip balm up near her face the WHOLE clip and just talks. She does NOT apply it, does NOT bring it "
    "to her lips, does NOT twist or open it — she is only holding it.\n"
    "GAZE: looking directly into the phone lens, talking to the viewer.\n"
    "BODY: relaxed; small natural head movements and easy blinks; warm genuine expression; the hand holding the "
    "product stays up near her cheek, steady.\n"
    "VOICE: warm woman in her 30s, upbeat but natural, conversational.\n"
    "TONE: genuinely excited, like telling a friend.\n"
    "SPEED: about 2.4 words per second.\n"
    "AUDIO: clear, full conversational volume, right into the phone mic — not muttered, not whispered.\n"
    "DIALOGUE LOCK — English only; speak ONLY these exact words, no fillers, no extra or trailing words, stop after "
    "the final word:\n"
    '"{line}"\n'
    "No on-screen text, no captions, no subtitles, no graphics."
)


def anchor_for(idx):
    """clip{N}_anchor.jpg if present (rotated eyes-open frame from clip 1), else the first frame."""
    if idx == 1:
        return FIRST_FRAME
    cand = ANCHOR_DIR / f"clip{idx}_anchor.jpg"
    return cand if cand.exists() else FIRST_FRAME


def gen_clip(idx):
    dest = CLIPS / f"clip{idx}.mp4"
    if dest.exists() and dest.stat().st_size > 10_000:
        return idx, str(dest), "skip-exists"
    anchor = anchor_for(idx)
    prompt = TEMPLATE.format(line=BEATS[idx])
    print(f"\n=== CLIP {idx} === anchor={anchor.name}\n{BEATS[idx]}", flush=True)
    res = gf.generate_veo(prompt, image_path=str(anchor), duration=8, aspect_ratio="portrait")
    if res.get("status") != "success" or not res.get("urls"):
        return idx, None, f"fail:{str(res.get('raw'))[:200]}"
    gf.download(res["urls"][0], dest)
    return idx, str(dest), "ok"


if __name__ == "__main__":
    idxs = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4]
    results = []
    for i in idxs:
        try:
            r = gen_clip(i)
        except Exception as e:
            r = (i, None, f"error:{e}")
        print(f"[{r[2]}] clip{r[0]} -> {r[1]}", flush=True)
        results.append(r)
    print("\n==== SUMMARY ====", flush=True)
    for idx, path, status in results:
        print(f"clip{idx}  {status:12s} {path or '-'}", flush=True)
