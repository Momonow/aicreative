#!/usr/bin/env python3
"""Depo interview ad — persona anchor candidates via KIE gpt-image-2 (2K, 9:16).

Survivor: Black woman ~45, documentary-real (appears in interview panes + solo CTA).
Documentarian: warm filmmaker interviewer (delivers the CTA to camera).

Skip-if-exists. Run: .venv/bin/python scripts/depo_interview_personas.py [--only survivor|doc]
"""
import argparse
import concurrent.futures as cf
from pathlib import Path

from kie_client import generate_gpt_image, download

OUT = Path("outputs/depo_interview/reference")
OUT.mkdir(parents=True, exist_ok=True)

REAL_TAIL = (
    "Natural real skin texture with visible pores, fine lines, uneven tone, no beauty "
    "retouching, no filter, no smile. Soft natural window light, documentary camera, "
    "shallow depth of field, muted realistic color. Medium chest-up framing. 9:16 vertical."
)

SURVIVOR = {
    "survivor_A_twistout": (
        "Photoreal candid documentary photograph of an ordinary Black woman, about 45, "
        "round face, deep-brown skin, short natural twist-out hair with a little gray, "
        "seated for a documentary interview at her kitchen table. Tired eyes, faint "
        "under-eye shadows, plain everyday look (NOT glamour, NOT fashion, NOT celebrity). "
        "She looks slightly off to the side as if listening to an off-camera interviewer. "
        + REAL_TAIL
    ),
    "survivor_B_locs": (
        "Photoreal candid documentary photograph of an ordinary Black woman, about 47, "
        "long oval face, medium-brown skin, silver-streaked locs pulled back, seated for a "
        "documentary interview on her living-room couch. Tired eyes, faint under-eye "
        "shadows, plain everyday look (NOT glamour, NOT fashion, NOT celebrity). She looks "
        "slightly off to the side as if listening to an off-camera interviewer. " + REAL_TAIL
    ),
    "survivor_C_cropped": (
        "Photoreal candid documentary photograph of an ordinary Black woman, about 44, "
        "fuller face, warm-brown skin, short cropped natural hair flecked with gray, seated "
        "for a documentary interview beside a window. Tired eyes, faint under-eye shadows, "
        "plain everyday look (NOT glamour, NOT fashion, NOT celebrity). She looks slightly "
        "off to the side as if listening to an off-camera interviewer. " + REAL_TAIL
    ),
    "survivor_D_headwrap": (
        "Photoreal candid documentary photograph of an ordinary Black woman, about 49, "
        "heart-shaped face, deep skin, wearing a simple patterned head-wrap, seated for a "
        "documentary interview at a dining table. Tired eyes, faint under-eye shadows, plain "
        "everyday look (NOT glamour, NOT fashion, NOT celebrity). She looks slightly off to "
        "the side as if listening to an off-camera interviewer. " + REAL_TAIL
    ),
}

DOC = {
    "doc_A_woman_curly": (
        "Photoreal candid documentary photograph of a documentary filmmaker, woman in her "
        "late 30s, natural curly hair, olive skin, casual soft knit top (NOT a suit, NOT a "
        "news blazer), seated in a neutral documentary setting looking toward an off-camera "
        "subject with a warm, attentive, empathetic expression. " + REAL_TAIL
    ),
    "doc_B_woman_gray": (
        "Photoreal candid documentary photograph of a documentary filmmaker, woman about 50, "
        "short gray hair, thin glasses, open-collar shirt (NOT a suit, NOT a news blazer), "
        "seated in a neutral documentary setting looking toward an off-camera subject with a "
        "warm, attentive, empathetic expression. " + REAL_TAIL
    ),
    "doc_C_man_beard": (
        "Photoreal candid documentary photograph of a documentary filmmaker, man in his 40s, "
        "short beard, warm face, henley shirt (NOT a suit, NOT a news blazer), seated in a "
        "neutral documentary setting looking toward an off-camera subject with a warm, "
        "attentive, empathetic expression. " + REAL_TAIL
    ),
    "doc_D_woman_dark": (
        "Photoreal candid documentary photograph of a documentary filmmaker, woman in her "
        "30s, dark hair tied back, medium skin, plain crew-neck top (NOT a suit, NOT a news "
        "blazer), seated in a neutral documentary setting looking toward an off-camera "
        "subject with a warm, attentive, empathetic expression. " + REAL_TAIL
    ),
}


def gen(name, prompt):
    out = OUT / f"{name}.png"
    if out.exists():
        print(f"[skip] {out}")
        return name, str(out)
    print(f"[gen ] {name} …")
    res = generate_gpt_image(prompt, aspect_ratio="9:16", resolution="2K")
    if res.get("status") != "success" or not res.get("urls"):
        print(f"[FAIL] {name}: {res.get('raw')}")
        return name, None
    download(res["urls"][0], out)
    print(f"[done] {out}")
    return name, str(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["survivor", "doc"], help="generate only one set")
    args = ap.parse_args()
    jobs = {}
    if args.only in (None, "survivor"):
        jobs.update(SURVIVOR)
    if args.only in (None, "doc"):
        jobs.update(DOC)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(lambda kv: gen(*kv), jobs.items()))


if __name__ == "__main__":
    main()
