"""
Depo-Provera brain-tumor image ads — MEDICAL-IMAGERY subset, PURE gpt-image-2 full-render
(model bakes the text — NOT the PIL pipeline). Brain-scan / hospital / shows-the-tumor angles.
Diagnosis-first, Black target persona, "significant compensation", NO disclaimer. Short baked text
to keep gpt-image-2 legible; QA + re-roll any garbled spelling.

Run:  .venv/bin/python scripts/depo_scan_ads_gen.py [--only scan_circle,holding_scan] [--regen <slug>]
Output: outputs/depo_ads/scan/<NN>_<slug>_4x5.png   (skip-if-exists)
"""
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image  # KIE gpt-image-2 was down 2026-06-19; OpenAI-direct is the same model
from PIL import Image

OUT = Path("outputs/depo_ads/scan")
OUT.mkdir(parents=True, exist_ok=True)

# only the specified headline text may appear — nothing else
ONLYTEXT = (" Render ONLY the exact headline and sub-line specified, in a clean bold legible sans-serif, "
            "correctly spelled. Absolutely NO other text, NO watermark, NO logo, NO brand name, NO captions.")

ADS = [
    dict(n=26, slug="scan_circle", prompt=(
        "Photoreal close-up of a real brain MRI scan on a dark radiology lightbox, a rounded tumor clearly "
        "visible and circled in red marker. Across the bottom a bold clean white headline reads exactly: "
        "\"A BRAIN TUMOR. LINKED TO THE DEPO SHOT.\" and a smaller white line below reads exactly: "
        "\"You may qualify for significant compensation.\" Serious clinical documentary look, vertical 4:5.")),
    dict(n=27, slug="doctor_consult", prompt=(
        "Photoreal documentary photograph in a hospital consult room: a Black woman in her 50s sits beside a "
        "doctor who points at her brain MRI on a wall monitor that clearly shows a tumor; both look serious. "
        "A bold clean white headline across the bottom reads exactly: \"DIAGNOSED WITH A BRAIN TUMOR AFTER "
        "DEPO?\" and a smaller white line: \"You may qualify for significant compensation.\" Natural hospital "
        "lighting, realistic, vertical 4:5.")),
    dict(n=28, slug="holding_scan", prompt=(
        "Photoreal candid photograph: a worried Black woman in her 40s at home holding up her own brain MRI "
        "film toward the window light, studying it. A bold white headline across the bottom reads exactly: "
        "\"A BRAIN TUMOR. FROM BIRTH CONTROL.\" and a smaller white line: \"See if you qualify.\" Real, "
        "emotional, natural light, vertical 4:5.")),
    dict(n=29, slug="hospital_bed", prompt=(
        "Photoreal documentary photograph: a Black woman in her early 40s in a hospital gown with a head "
        "bandage after brain surgery, an IV in her arm, sitting up in a hospital bed looking out the window, "
        "tired and somber. A bold white headline across the bottom reads exactly: \"A BRAIN TUMOR AT 41. NO "
        "ONE WARNED ME.\" and a smaller white line: \"Used the Depo shot? You may qualify for significant "
        "compensation.\" Realistic hospital scene, vertical 4:5.")),
    dict(n=30, slug="mri_machine", prompt=(
        "Photoreal photograph: a Black woman lying on an MRI scanner table about to slide into the machine, a "
        "technician's hand guiding the table, cool clinical blue light. A bold white headline across the "
        "bottom reads exactly: \"SCANNED FOR A BRAIN TUMOR?\" and a smaller white line: \"If you used the Depo "
        "shot, you may qualify.\" Realistic radiology room, vertical 4:5.")),
    dict(n=31, slug="scar_portrait", prompt=(
        "Photoreal dignified portrait of a Black woman in her 50s with closely cropped natural hair revealing "
        "a healed curved surgical scar on the side of her scalp from brain surgery, looking calmly at the "
        "camera. A bold white headline across the bottom reads exactly: \"THIS SCAR CAME FROM A BRAIN TUMOR.\" "
        "and a smaller white line: \"Linked to the Depo shot. See if you qualify.\" Real documentary portrait, "
        "soft light, vertical 4:5.")),
    dict(n=32, slug="news_scan", prompt=(
        "Photoreal still that looks like a TV health-news segment: a Black woman's photo beside a brain MRI "
        "graphic, with a lower-third news banner. Bold white text in the banner reads exactly: \"BRAIN TUMOR "
        "LAWSUIT: THE DEPO SHOT\" and a smaller line: \"See if you qualify for compensation.\" Broadcast-news "
        "look, vertical 4:5.")),
    dict(n=33, slug="poster_scan", prompt=(
        "Photoreal clean public-awareness poster: a large brain MRI scan with a visible tumor filling the "
        "UPPER portion on a white background. Across the LOWER third, a big bold dark headline reads exactly: "
        "\"THE DEPO SHOT & BRAIN TUMORS\" and a smaller line directly below reads exactly: \"Diagnosed? You "
        "may qualify for significant compensation.\" Keep ALL text in the lower third, fully inside the frame. "
        "Minimal clinical poster layout, vertical.")),
]


def crop_45(path):
    """OpenAI returns 1024x1536 (2:3); crop to 4:5 (1024x1280) keeping the BOTTOM (text + face)."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    th = int(round(w * 5 / 4))
    if h > th:
        im.crop((0, h - th, w, h)).save(path)  # remove from top


def run_one(ad, regen):
    dest = OUT / f"{ad['n']:02d}_{ad['slug']}_4x5.png"
    if dest.exists() and not regen:
        return ad, str(dest), "skip"
    try:
        r = generate_image(ad["prompt"] + ONLYTEXT, out_path=str(dest), size="1024x1536", quality="high")
    except Exception as e:
        return ad, None, f"err:{type(e).__name__}:{str(e)[:90]}"
    if r.get("status") != "success":
        return ad, None, f"fail:{str(r)[:100]}"
    crop_45(dest)
    return ad, str(dest), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen", default="", help="comma slugs to force-regenerate")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()
    want = {s.strip() for s in args.only.split(",") if s.strip()}
    regen = {s.strip() for s in args.regen.split(",") if s.strip()}
    ads = [a for a in ADS if not want or a["slug"] in want]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, a, a["slug"] in regen): a for a in ads}
        for f in as_completed(futs):
            ad, path, st = f.result()
            print(f"[{st}] {ad['n']:02d} {ad['slug']} -> {path}", flush=True)


if __name__ == "__main__":
    main()
