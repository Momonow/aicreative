"""Burn the verbatim Pulaski/Jones legal disclaimer onto a static image ad.

The regulated text is loaded from config/campaigns/pulaski-jones/disclaimer.txt.

Styles:
  auto (default) — sample the bottom strip; light background -> plain dark-grey smallprint
                   (like the reference quiz ad), busy/photo background -> translucent dark band
                   with white smallprint.
  band | plain   — force a style.

  python scripts/burn_pulaski_jones_disclaimer_image.py <in.png> <out.png>
  python scripts/burn_pulaski_jones_disclaimer_image.py <in.png> <out.png> --style bar
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/HelveticaNeue.ttc"   # index 0 regular
REPO = Path(__file__).resolve().parent.parent
DEFAULT_TEXT_PATH = REPO / "config/campaigns/pulaski-jones/disclaimer.txt"


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def burn(src, out, style="auto", font_frac=0.0145, text=None):
    img = Image.open(src).convert("RGB")
    W, H = img.size
    fpx = max(11, int(H * font_frac))
    font = ImageFont.truetype(FONT, fpx, index=0)
    d = ImageDraw.Draw(img, "RGBA")
    max_w = int(W * 0.92)
    lines = wrap(d, text or DEFAULT_TEXT_PATH.read_text().strip(), font, max_w)
    lh = int(fpx * 1.32)
    block_h = len(lines) * lh
    pad = int(fpx * 1.1)
    y0 = H - block_h - pad * 2

    if style == "auto":
        import numpy as np
        strip = np.asarray(img.crop((0, y0, W, H)).convert("L"), float)
        style = "plain" if strip.mean() > 200 and strip.std() < 40 else "band"

    if style == "bar":
        # APPEND a solid black bar BELOW the full-size artwork (canvas grows slightly past 1:1 —
        # user-locked: never downscale the photo to fit; a slightly-off ratio is fine on FB).
        strip_h = block_h + pad * 2
        canvas = Image.new("RGB", (W, H + strip_h), (0, 0, 0))
        canvas.paste(img, (0, 0))
        img = canvas
        d = ImageDraw.Draw(img, "RGBA")
        y0 = H
        fill = (235, 235, 235)
    elif style == "fit":
        # shrink the artwork to reserve a clean white strip INSIDE the original canvas (for design
        # cards whose layout fills the frame — avoids covering logos/CTAs; stays exactly 1:1).
        strip_h = block_h + pad * 2
        art_h = H - strip_h
        art_w = int(W * art_h / H)
        art = img.resize((art_w, art_h), Image.LANCZOS)
        img = Image.new("RGB", (W, H), (255, 255, 255))
        img.paste(art, ((W - art_w) // 2, 0))
        d = ImageDraw.Draw(img, "RGBA")
        y0 = art_h
        fill = (70, 70, 70)
    elif style == "band":
        d.rectangle([0, y0, W, H], fill=(0, 0, 0, 150))
        fill = (245, 245, 245)
    else:
        fill = (70, 70, 70)

    y = y0 + pad
    for ln in lines:
        d.text((W // 2, y), ln, font=font, fill=fill, anchor="ma")
        y += lh
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"saved {out}  ({style}, {len(lines)} lines @ {fpx}px)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("out")
    parser.add_argument(
        "--style",
        choices=["auto", "band", "plain", "fit", "bar"],
        default="auto",
    )
    parser.add_argument("--font-frac", type=float, default=0.0145)
    parser.add_argument("--text", default=None, help="explicit approved override")
    args = parser.parse_args()
    burn(args.src, args.out, args.style, args.font_frac, args.text)


if __name__ == "__main__":
    main()
