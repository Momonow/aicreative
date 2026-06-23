"""Full 'STOP OVERPAYING' comparison banner generated ENTIRELY by gpt-image-2 (KIE).

NO PIL / code compositing — gpt-image-2 renders the whole creative (headline, review,
price ladder, product, CTA, footnote). The real TrimRx vial PNG is passed as an
image-to-image reference so the product stays the actual product. Python here is only
the API caller + downloader.

Run:
  .venv/bin/python scripts/trimrx_compare_gpt.py                 # i2i with real vial (default)
  .venv/bin/python scripts/trimrx_compare_gpt.py --t2i           # pure text-to-image (model invents vial)
  .venv/bin/python scripts/trimrx_compare_gpt.py --aspect 4:5
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

VIAL = "outputs/trimrx_glp1/product/vial_gip_blue.png"

PROMPT = (
    "Design a polished, modern direct-response weight-loss advertisement as a SINGLE square social-media "
    "banner with a deep navy-blue gradient background and a clean, professional graphic-design layout.\n\n"
    "TOP-LEFT: a bold large white condensed sans-serif headline reading exactly: STOP OVERPAYING FOR "
    "TIRZEPATIDE. Directly beneath it a smaller light-blue line reading: Provider-prescribed | All doses "
    "included | Free shipping.\n\n"
    "BELOW THE HEADLINE: a light rounded review card containing a small circular photo of an ordinary "
    "smiling woman, the name 'Nina J.', a row of five gold stars, and a short quote: \"I was paying double "
    "at a local med spa. TrimRx was a no-brainer.\"\n\n"
    "BELOW THE REVIEW: a vertical price-comparison ladder of three rounded dark cards (small label on top, "
    "large price under it):\n"
    "1) 'At a local clinic   $1,000+/mo'  with a big red X mark beside it.\n"
    "2) 'Typical online programs   $299/mo'  with a big red X mark beside it.\n"
    "3) 'TrimRx   $279/mo'  with the price in bright pink and a big green check mark (the best option).\n\n"
    "RIGHT SIDE: feature the product from the reference image — a clear glass medicine vial with a blue cap "
    "and a blue-and-white label reading 'GLP-1 + GIP Medication', 'RX ONLY', 'Dose Varies' — large, "
    "prominent, realistic product photography, keep it looking exactly like the reference vial.\n\n"
    "LOWER-RIGHT: a bright green rounded call-to-action button reading 'Start your free assessment'.\n\n"
    "VERY BOTTOM, small grey legal text: 'Compounded medication. Requires prescription. Not FDA-approved. "
    "Individual results vary.'\n\n"
    "Style: crisp high-end telehealth brand, strong contrast, bold and clean correctly-spelled typography, "
    "no clutter, no extra logos, no other brand names anywhere."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t2i", action="store_true", help="pure text-to-image (no product reference)")
    ap.add_argument("--aspect", default="1:1")
    args = ap.parse_args()
    out = f"outputs/trimrx_glp1/final/30g_compare_gpt_{args.aspect.replace(':','x')}{'_t2i' if args.t2i else ''}.png"

    image_urls = None
    if not args.t2i:
        url = kie.upload_file(VIAL)
        print("vial ref url:", url)
        image_urls = [url]

    print(f"MODEL: gpt-image-2-{'text-to-image' if args.t2i else 'image-to-image'} (KIE)  ASPECT {args.aspect}  2K")
    print("PROMPT:\n" + PROMPT + "\n")
    res = kie.generate_gpt_image(PROMPT, image_urls=image_urls, aspect_ratio=args.aspect, resolution="2K")
    if res.get("status") == "success" and res.get("urls"):
        kie.download(res["urls"][0], out)
        print("SAVED:", out)
    else:
        print("FAILED:", str(res.get("raw"))[:400])


if __name__ == "__main__":
    main()
