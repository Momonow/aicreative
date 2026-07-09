"""Depo docu b-roll library — animate approved stills into clips (veo-3.1-lite i2v).
Each approved still (gpt2 v01-v24 portrait, nano nn_*/rp_* landscape) becomes an 8s muted-use
b-roll clip via startImage i2v. Subtle-documentary motion prompts; audio ignored at edit time.
Skip-if-exists → re-run resumes. Output: outputs/depo_docu/broll_clips/<slug>.mp4

  .venv/bin/python scripts/depo_docu_broll_i2v.py [--only slug1,slug2]
"""
import argparse
import glob
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from googleflow_client import generate_veo, upload_asset, download

SRC = "outputs/depo_docu/broll_stills"
OUT = "outputs/depo_docu/broll_clips"
os.makedirs(OUT, exist_ok=True)

BASE = ("Subtle documentary motion only: gentle handheld drift, people and hands in frame continue "
        "their natural small movements, nothing new enters the frame, no cuts, no zoom bursts. "
        "Keep the scene exactly as the image. Muted natural light. No speech. "
        "NO on-screen text, NO captions, NO logos, NO watermark.")
HINT = {
    "v01": "The doctor's pen traces slowly along the scan; the patient nods slightly.",
    "v02": "The doctor gestures at the screen; the woman's hand lowers slowly from her mouth.",
    "v03": "The radiologist scrolls; scan slices change on the monitor with a soft glow.",
    "v04": "The films pass slowly from one hand to the other.",
    "v05": "The doctor's hands turn the brain model slightly while gesturing.",
    "v06": "The nurse's hands finish adjusting the IV line; the patient breathes slowly.",
    "v07": "The bed keeps rolling down the corridor; ceiling lights pass overhead.",
    "v08": "The table slides slowly into the scanner bore.",
    "v09": "The drip chamber drips once; fingers twitch slightly.",
    "v10": "The plunger draws liquid up slowly from the vial.",
    "v11": "The nurse completes the injection smoothly; the woman stays looking away.",
    "v12": "The swab wipes a small circle on the arm.",
    "v13": "Very slow push-in toward the box and vial.",
    "v14": "Slow lateral pan along the shelf, focus holding on the violet box.",
    "v15": "The gloved hand sets the vial down and withdraws.",
    "v16": "She taps the screen; the younger woman leans in closer.",
    "v17": "The cursor clicks to the next scan image.",
    "v18": "The phone tilts slightly in her hand, screen catching light.",
    "v19": "A page turns slowly in the folder.",
    "v20": "The document slides the rest of the way out of the envelope.",
    "v21": "The red pen completes its circle around the paragraph.",
    "v22": "The pen finishes the signature stroke.",
    "v23": "The folder passes across the table between hands.",
    "v24": "She climbs two more steps, coat moving slightly.",
    "nn_doc_points": "The doctor's pen moves along the lightbox scan; the patient stays still.",
    "nn_monitor": "The doctor steadies the monitor; the woman blinks, hand at her mouth.",
    "nn_postop": "The nurse's hands finish the IV adjustment; the patient rests.",
    "nn_injection": "The injection completes smoothly; she keeps facing the window.",
    "nn_depo_box": "Very slow push-in; the pharmacist moves softly out of focus behind.",
    "nn_laptop_point": "She points along the scan on screen; the younger woman nods.",
    "rp1_desk": "Very slow push-in toward the paper's title; light flickers softly.",
    "rp2_laptop": "She scrolls the document slightly; screen glow shifts on her hands.",
    "rp3_hands": "The page tilts gently in her hands as she reads.",
}


def stills():
    out = []
    for f in sorted(glob.glob(f"{SRC}/v*.png")) + sorted(glob.glob(f"{SRC}/nn_*.png")) + sorted(glob.glob(f"{SRC}/rp*.png")):
        slug = os.path.splitext(os.path.basename(f))[0]
        out.append((slug, f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    todo = stills()
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        todo = [(s, f) for s, f in todo if s in want]
    print(f"{len(todo)} stills to animate", flush=True)
    for slug, path in todo:
        dest = f"{OUT}/{slug}.mp4"
        if os.path.exists(dest) and os.path.getsize(dest) > 50000:
            print(f"  {slug} cached", flush=True)
            continue
        w, h = Image.open(path).size
        aspect = "portrait" if h >= w else "landscape"
        key = slug[:3] if slug.startswith("v") and slug[1:3].isdigit() else slug
        hint = HINT.get(key, HINT.get(slug, ""))
        prompt = (hint + " " + BASE).strip()
        try:
            mgid = upload_asset(path)
            r = generate_veo(prompt=prompt, image_mgid=mgid, duration=8,
                             aspect_ratio=aspect, model="veo-3.1-lite", attempts=2)
            if r.get("status") == "success" and r.get("urls"):
                download(r["urls"][0], dest)
                print(f"  {slug} -> ok", flush=True)
            else:
                print(f"  {slug} -> FAIL: {str(r.get('raw'))[:90]}", flush=True)
        except Exception as e:
            print(f"  {slug} -> EXC: {str(e)[:90]}", flush=True)


if __name__ == "__main__":
    main()
