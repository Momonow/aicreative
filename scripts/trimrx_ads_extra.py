"""
TrimRx GLP-1 — EXTRA image-ad formats (additive to scripts/trimrx_ads_gen.py).

The main generator (trimrx_ads_gen.py) already defines 24 formats (01-24). This adds 6 GENUINELY-NEW
concepts the main set doesn't cover, each in a DIFFERENT composition lane (per the locked creative
direction: image-forward, big fonts, every ad a different format, relatable midsize/plus-size bodies
+ weight-loss cues, NO fake FB/iMessage UI). Same compliance locks + footnote + pricing.

It IMPORTS the main generator's lanes/helpers (read-only — never runs its main()), renders into the
SAME final/ dir with a NON-COLLIDING number block (25-30) and new slugs, and writes its own copy deck
(copy_extra.md) so it never clobbers copy.md.

Run:
  .venv/bin/python scripts/trimrx_ads_extra.py
  .venv/bin/python scripts/trimrx_ads_extra.py --only doorstep,closet
  .venv/bin/python scripts/trimrx_ads_extra.py --regen-base tape_progress
Skip-if-exists on base images.
"""
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image

import trimrx_ads_gen as T  # reuse lanes, helpers, gen_base, constants (does NOT run its main())

OUT, FINAL_DIR, DISC = T.OUT, T.FINAL_DIR, T.DISC
NOTEXT, PLUS, LIFE = T.NOTEXT, T.PLUS, T.LIFE

# 6 NEW formats, numbered 25-30 (main set stops at 24), each a different lane/composition.
FORMATS = [
    dict(n=25, slug="doorstep", lane="hero", vbias=0.34,
         images={"": "A relatable midsize woman about 40 standing in her sunny front doorway, smiling warmly "
                     "as she holds a plain unbranded cardboard delivery box in her arms, cozy home entrance, "
                     "bright natural daylight." + PLUS + NOTEXT},
         kicker="NO CLINIC. NO PHARMACY LINE.",
         headline="Care that comes to you.", hsize=96,
         sub="Compounded GLP-1, from $149/mo — shipped discreetly.",
         cta="See if you qualify →",
         headline_fb="Care That Comes to You",
         primary=("Skip the waiting room and the pharmacy line — a 3-minute quiz, a licensed-provider review, "
                  "and compounded GLP-1 shipped discreetly to your door. From $149/month, no insurance "
                  "needed. See if you qualify.")),

    dict(n=26, slug="closet", lane="meme", vbias=0.30,
         images={"": "A relatable midsize woman about 42 standing in her bedroom closet, holding a favorite "
                     "blouse on a hanger up against herself and looking hopeful, soft warm light, fuller "
                     "realistic figure." + PLUS + NOTEXT},
         top="the clothes you're not ready to give up", tsize=58,
         bottom="a compounded GLP-1 plan may help — from $149/mo", bsize=52,
         headline_fb="For the Clothes You're Not Ready to Give Up",
         primary=("You don't have to pack away the clothes you love. A compounded GLP-1 program, guided by "
                  "licensed providers, may help — gradually, from $149/month. See if you qualify. Individual "
                  "results vary.")),

    dict(n=27, slug="keep_up", lane="split", vbias=0.24,
         images={"": "A relatable midsize woman about 38 laughing and playing with her two young kids in a "
                     "sunny backyard, full of genuine energy, candid joyful family moment, fuller realistic "
                     "figure." + PLUS + NOTEXT},
         headline="Keep up with the people who matter.", hsize=72,
         sub="Compounded GLP-1, from $149/mo.",
         cta="See if you qualify →",
         headline_fb="Keep Up With the People Who Matter",
         primary=("It's about more than a number on a scale — it's having the energy for the people you love. "
                  "A compounded GLP-1 program, guided by licensed providers, may help. From $149/month. See "
                  "if you qualify.")),

    dict(n=28, slug="five_a_day", lane="bigstat", vbias=0.32,
         images={"": "A relatable midsize woman about 40 in a cozy kitchen holding a warm mug of coffee in "
                     "soft morning light, calm and content, fuller realistic figure." + PLUS + NOTEXT},
         big="~$5/day", label="for everything-included GLP-1 care.",
         sub="Visits, shipping & dose changes included. From $149/mo.",
         cta="See if you qualify →",
         headline_fb="About $5 a Day, Everything Included",
         primary=("About $5 a day covers everything — compounded GLP-1 medication, unlimited licensed-provider "
                  "visits, shipping, and free dose changes. From $149/month, no insurance needed. See if you "
                  "qualify.")),

    dict(n=29, slug="tape_progress", lane="annotated", vbias=0.28,
         images={"": "A relatable midsize woman about 40 wrapping a soft cloth measuring tape around her waist "
                     "over a fitted top, looking down with quiet hope, bright clean bathroom light, fuller "
                     "realistic figure." + PLUS + NOTEXT},
         tags=["Gradual & consistent", "Licensed providers", "From $149/mo"],
         headline="Progress you can actually feel.", hsize=70,
         cta="See if you qualify →",
         headline_fb="Progress You Can Actually Feel",
         primary=("Real change is gradual and consistent — not overnight. A compounded GLP-1 program, guided "
                  "by licensed providers, may help you get there. From $149/month. See if you qualify. "
                  "Individual results vary.")),

    dict(n=30, slug="not_a_gimmick", lane="product", images={},
         product="duo", pheight=600, kicker="NOT A TEA. NOT A GUMMY.",
         headline="Real prescription GLP-1 care.", hsize=78,
         sub="Semaglutide from $149/mo · Tirzepatide from $179/mo — prescribed by licensed providers.",
         cta="See if you qualify →",
         headline_fb="Real Prescription GLP-1 — Not a Gimmick",
         primary=("No teas, no gummies, no gimmicks — compounded GLP-1 medication (semaglutide or "
                  "tirzepatide), prescribed by licensed providers and delivered to your door. From "
                  "$149/month, no insurance needed. See if you qualify.")),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--regen-base", default="")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    fmts = FORMATS
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        fmts = [f for f in FORMATS if f["slug"] in want or f["lane"] in want]
    regen = {s.strip() for s in args.regen_base.split(",") if s.strip()}

    jobs = [(f["slug"], k, p) for f in fmts for k, p in f.get("images", {}).items()]
    bases = {}
    if jobs:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(T.gen_base, s, k, p, s in regen): (s, k) for s, k, p in jobs}
            for fut in as_completed(futs):
                s, k, path, st = fut.result()
                print(f"[base:{st}] {s} {k or ''} -> {path}", flush=True)
                bases[(s, k)] = path

    print("---- rendering ----", flush=True)
    copy_lines = ["# TrimRx GLP-1 — EXTRA FB ad copy (formats 25-30)\n",
                  "Every primary text MUST end with the mandatory disclaimer (appended below).\n"]
    for f in fmts:
        imgs = {}
        for k in f.get("images", {}):
            p = bases.get((f["slug"], k))
            imgs[k] = Image.open(p).convert("RGB") if p and os.path.exists(p) else None
        img = T.LANES[f["lane"]](imgs, f)
        out = os.path.join(FINAL_DIR, f"{f['n']:02d}_{f['slug']}_4x5.png")
        img.save(out)
        miss = [k or "(main)" for k in f.get("images", {}) if imgs.get(k) is None]
        print(f"[render] {out}{'  MISSING:' + ','.join(miss) if miss else ''}", flush=True)
        hl = f.get("headline_fb", f.get("headline", ""))
        copy_lines.append(f"\n## {f['n']:02d} · {f['slug']}  ({f['lane']})\n")
        copy_lines.append(f"**Headline:** {hl}\n")
        copy_lines.append(f"**Primary text:** {f.get('primary','')}\n\n{DISC}\n")

    with open(os.path.join(OUT, "copy_extra.md"), "w") as fh:
        fh.write("\n".join(copy_lines))
    print(f"[copy] wrote {os.path.join(OUT, 'copy_extra.md')}", flush=True)


if __name__ == "__main__":
    main()
