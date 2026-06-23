"""
TrimRx GLP-1 weight-loss image-ad batch — 10 ads, every one a DIFFERENT ad style.

Compliance-locked to the TrimRx affiliate sheet (NO branded names Ozempic/Wegovy/etc, NO branded
packaging, NO "same as/generic/clinically proven/FDA-approved/guarantee/proven", NO dramatic
before-after / lb claims, NO fake doctors, NO celebrities). Language: "compounded GLP-1",
"prescription", "licensed providers", "may help / can support". Pricing: semaglutide from $149/mo,
tirzepatide from $179/mo (semaglutide/tirzepatide are compound names — allowed; brand words are not).

Every creative carries the required on-image footnote:
  "Compounded medication. Requires prescription. Not FDA-approved. Individual results vary."
The full Meta primary-text disclaimer is emitted to outputs/trimrx_glp1/copy.md for the FB ad copy.

gpt-image-2 (KIE, 2K) renders BASE PHOTOS only (2 of 10 ads); PIL lays ALL text so headline/price/
footnote are pixel-perfect (no garbled text = no compliance risk). 8 ads are pure-PIL (instant).

Run:
  .venv/bin/python scripts/trimrx_ads_gen.py                 # all 10, 4:5 (1080x1350)
  .venv/bin/python scripts/trimrx_ads_gen.py --only pricecard,versus
  .venv/bin/python scripts/trimrx_ads_gen.py --regen-base social
Skip-if-exists on base images.
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kie_client as kie

OUT = "outputs/trimrx_glp1"
BASE_DIR = os.path.join(OUT, "base")
FINAL_DIR = os.path.join(OUT, "final")
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)
W, H = 1080, 1350  # 4:5 feed

BRAND = "trimrx"
FOOTNOTE = "Compounded medication. Requires prescription. Not FDA-approved. Individual results vary."
DISC = ("TrimRX does not practice medicine or prescribe medications. Compounded medications are not "
        "FDA-approved and are not evaluated by the FDA for safety, effectiveness, or quality. "
        "Results vary by individual and are not guaranteed.")

# palette — TrimRx wellness teal/mint/green
TEAL = (16, 94, 84); TEAL_DK = (9, 58, 52); MINT = (210, 238, 230); MINT_LT = (236, 248, 243)
INK = (26, 36, 34); WHITE = (250, 252, 251); GREEN = (33, 168, 108); GREEN_DK = (24, 132, 86)
CORAL = (238, 116, 92); AMBER = (245, 190, 70); GREY = (122, 130, 128); REDX = (198, 86, 74)
PAPER = (250, 248, 243); SAGE = (90, 120, 110); CREAM = (245, 241, 233)

FONT_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts"),
    "/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/", "/Library/Fonts/",
]


def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def F_black(s): return font(["Montserrat-Black.ttf", "Arial Black.ttf"], s)
def F_bold(s): return font(["Arial Bold.ttf", "HelveticaNeue.ttc"], s)
def F_reg(s): return font(["Arial.ttf", "Helvetica.ttc"], s)
def F_serif_b(s): return font(["Georgia Bold.ttf", "Times New Roman Bold.ttf"], s)
def F_serif(s): return font(["Georgia.ttf", "Times New Roman.ttf"], s)
def F_serif_i(s): return font(["Georgia Italic.ttf", "Georgia.ttf"], s)


# --------------------------------------------------------------------------- helpers
def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def cover(img, tw, th, vbias=0.5):
    s = max(tw / img.width, th / img.height)
    img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))))
    x = (img.width - tw) // 2
    y = int((img.height - th) * vbias)
    return img.crop((x, y, x + tw, y + th))


def scrim(img, frac, strength, top=False):
    h = int(H * frac)
    grad = Image.new("L", (1, h), 0)
    for i in range(h):
        t = (1 - i / h) if top else (i / h)
        grad.putpixel((0, i), int(strength * t ** 1.4))
    grad = grad.resize((W, h))
    blk = Image.new("RGB", (W, h), (0, 0, 0))
    img.paste(blk, (0, 0 if top else H - h), grad)
    return img


def block(draw, x, y, text, fnt, fill, lh, maxw, center_w=None):
    for ln in wrap(draw, text, fnt, maxw):
        if center_w is not None:
            tw = draw.textlength(ln, font=fnt)
            draw.text((x + (center_w - tw) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def chip(draw, xy, text, fnt, pad=(36, 22), fill=GREEN, fg=WHITE, radius=16):
    x, y = xy
    arr = text.rstrip().endswith("→")
    label = text.rstrip()[:-1].rstrip() if arr else text
    tw = draw.textlength(label, font=fnt); asc, desc = fnt.getmetrics(); th = asc + desc
    gap, aw = (20, int(th * 0.5)) if arr else (0, 0)
    draw.rounded_rectangle([x, y, x + tw + gap + aw + pad[0] * 2, y + th + pad[1] * 2], radius=radius, fill=fill)
    draw.text((x + pad[0], y + pad[1]), label, font=fnt, fill=fg)
    if arr:
        ax = x + pad[0] + tw + gap; cy = y + pad[1] + th / 2; ah = th * 0.46
        draw.polygon([(ax, cy - ah / 2), (ax, cy + ah / 2), (ax + aw, cy)], fill=fg)
    return y + th + pad[1] * 2


def check(d, x, y, s, col, w=7):
    d.line([x, y + s * 0.55, x + s * 0.40, y + s * 0.92], fill=col, width=w)
    d.line([x + s * 0.40, y + s * 0.92, x + s, y + s * 0.05], fill=col, width=w)


def cross(d, x, y, s, col, w=7):
    d.line([x, y, x + s, y + s], fill=col, width=w)
    d.line([x + s, y, x, y + s], fill=col, width=w)


def footnote(d, fg=GREY, center=False):
    size = 23
    while size > 13 and d.textlength(FOOTNOTE, font=F_reg(size)) > W - 96:
        size -= 1
    fnt = F_reg(size)
    if center:
        tw = d.textlength(FOOTNOTE, font=fnt)
        d.text(((W - tw) / 2, H - 46), FOOTNOTE, font=fnt, fill=fg)
    else:
        d.text((48, H - 46), FOOTNOTE, font=fnt, fill=fg)


def wordmark(d, x, y, color=WHITE, size=52):
    d.text((x, y), BRAND, font=F_black(size), fill=color)
    tw = d.textlength(BRAND, font=F_black(size))
    d.ellipse([x + tw + 8, y + size * 0.34, x + tw + 8 + size * 0.18, y + size * 0.34 + size * 0.18], fill=GREEN)


# --------------------------------------------------------------------------- render lanes
def r_pricecard(imgs, f):
    img = Image.new("RGB", (W, H), MINT_LT); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 132], fill=TEAL); wordmark(d, 64, 40, WHITE, 56)
    M = 72; y = 188
    y = block(d, M, y, f["title"], F_black(66), TEAL_DK, 76, W - 2 * M); y += 14
    y = block(d, M, y, f["subtitle"], F_bold(33), SAGE, 42, W - 2 * M); y += 40
    for label, price in f["prices"]:
        d.text((M, y + 2), label, font=F_bold(42), fill=INK)
        pw = d.textlength(price, font=F_black(48))
        d.text((W - M - pw, y), price, font=F_black(48), fill=GREEN_DK)
        y += 74
    y += 8
    d.line([M, y, W - M, y], fill=(196, 222, 212), width=3); y += 30
    for label, val in f["included"]:
        check(d, M, y - 2, 34, GREEN, 6)
        d.text((M + 58, y), label, font=F_reg(36), fill=(52, 64, 60))
        vw = d.textlength(val, font=F_bold(36))
        d.text((W - M - vw, y), val, font=F_bold(36), fill=GREEN_DK)
        y += 58
    y += 28
    chip(d, (M, y), f["cta"], F_black(38))
    footnote(d, GREY)
    return img


def r_versus(imgs, f):
    img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 150], fill=TEAL)
    block(d, 0, 44, f["title"], F_black(46), WHITE, 56, W, center_w=W)
    midx = W // 2; top = 150; bot = H - 210
    d.rectangle([0, top, midx, bot], fill=(237, 237, 237))
    d.rectangle([midx, top, W, bot], fill=MINT_LT)
    d.line([midx, top, midx, bot], fill=WHITE, width=6)
    block(d, 0, top + 36, "THE OLD WAY", F_black(34), (150, 150, 150), 40, midx, center_w=midx)
    block(d, midx, top + 36, "THE TRIMRX WAY", F_black(34), TEAL, 40, midx, center_w=midx)
    yL = top + 130
    for it in f["old"]:
        cross(d, 46, yL + 4, 30, REDX, 6)
        block(d, 92, yL, it, F_bold(33), (96, 96, 96), 42, midx - 120)
        yL += 112
    yR = top + 130
    for it in f["new"]:
        check(d, midx + 36, yR + 2, 32, GREEN, 6)
        block(d, midx + 84, yR, it, F_bold(33), INK, 42, midx - 130)
        yR += 112
    chip(d, ((W - (d.textlength(f["cta"][:-1].strip(), font=F_black(36)) + 150)) / 2, bot + 34),
         f["cta"], F_black(36))
    footnote(d, GREY, center=True)
    return img


def r_social(imgs, f):
    img = Image.new("RGB", (W, H), (240, 242, 245)); d = ImageDraw.Draw(img)
    pad = 30
    d.rectangle([pad, pad, W - pad, H - pad], fill=WHITE)
    x = pad + 28; y = pad + 28
    d.ellipse([x, y, x + 82, y + 82], fill=TEAL)
    d.text((x + 18, y + 16), "t", font=F_black(50), fill=WHITE)
    d.text((x + 102, y + 6), "TrimRx", font=F_bold(34), fill=(20, 22, 24))
    d.text((x + 102, y + 48), "Sponsored", font=F_reg(26), fill=(120, 122, 126))
    y += 108
    y = block(d, x, y, f["text"], F_reg(37), (30, 32, 34), 50, W - 2 * pad - 56); y += 22
    ph = 540
    if imgs.get(""):
        img.paste(cover(imgs[""], W - 2 * pad - 56, ph, vbias=0.16), (x, y))
    else:
        d.rectangle([x, y, x + W - 2 * pad - 56, y + ph], fill=MINT)
    y += ph + 22
    d.line([x, y, W - pad - 28, y], fill=(228, 228, 230), width=2); y += 20
    d.text((x, y), "1.4K        286 comments        173 shares", font=F_reg(26), fill=(120, 122, 126)); y += 50
    chip(d, (x, y), f["cta"], F_bold(34), fill=(24, 119, 242), fg=WHITE)
    footnote(d, (158, 158, 162))
    return img


def r_texts(imgs, f):
    img = Image.new("RGB", (W, H), (18, 20, 24)); d = ImageDraw.Draw(img); M = 52
    d.text((M, 60), "Messages", font=F_bold(34), fill=(150, 150, 156))
    d.line([0, 120, W, 120], fill=(40, 42, 48), width=2)
    y = 165
    for side, txt in f["bubbles"]:
        out = side == "out"
        bf = F_reg(36); maxw = 660
        lines = wrap(d, txt, bf, maxw - 60)
        bw = max(d.textlength(l, font=bf) for l in lines) + 60
        bh = len(lines) * 48 + 36
        bx = W - M - bw if out else M
        col = GREEN_DK if out else (58, 60, 66)
        d.rounded_rectangle([bx, y, bx + bw, y + bh], radius=28, fill=col)
        ty = y + 18
        for l in lines:
            d.text((bx + 30, ty), l, font=bf, fill=WHITE); ty += 48
        y += bh + 22
    y += 8
    d.rounded_rectangle([M, y, W - M, y + 150], radius=20, fill=(40, 42, 48))
    d.text((M + 28, y + 28), "TrimRx", font=F_bold(34), fill=WHITE)
    chip(d, (M + 28, y + 74), f["cta"], F_bold(32))
    footnote(d, (120, 120, 126))
    return img


def r_statement(imgs, f):
    bg = f.get("bg", TEAL); img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img); M = 88
    acc = f.get("accent", AMBER)
    kt = f["kicker"]; tw = d.textlength(kt, font=F_black(34))
    d.text(((W - tw) / 2, 220), kt, font=F_black(34), fill=acc)
    y = 320
    y = block(d, M, y, f["big"], F_black(72), WHITE, 84, W - 2 * M, center_w=W - 2 * M); y += 40
    y = block(d, M, y, f["sub"], F_bold(38), acc, 50, W - 2 * M, center_w=W - 2 * M); y += 52
    tw = d.textlength(f["cta"][:-1].strip(), font=F_black(38)) + 150
    chip(d, ((W - tw) / 2, y), f["cta"], F_black(38), fill=acc, fg=TEAL_DK)
    footnote(d, (210, 220, 216), center=True)
    return img


def r_caption_photo(imgs, f):
    img = cover(imgs[""], W, H) if imgs.get("") else Image.new("RGB", (W, H), TEAL)
    img = scrim(img, 0.55, 238)
    d = ImageDraw.Draw(img); M = 60
    sub_lines = wrap(d, f["sub"], F_bold(34), W - 2 * M)
    head_lines = wrap(d, f["headline"], F_black(60), W - 2 * M)
    y = H - 60 - 150 - len(sub_lines) * 44 - len(head_lines) * 72 - 60
    if f.get("kicker"):
        d.text((M, y), f["kicker"], font=F_black(32), fill=AMBER); y += 52
    for ln in head_lines:
        d.text((M, y), ln, font=F_black(60), fill=WHITE); y += 72
    y += 12
    y = block(d, M, y, f["sub"], F_bold(34), (236, 236, 236), 44, W - 2 * M); y += 18
    chip(d, (M, y), f["cta"], F_black(34))
    footnote(d, (224, 224, 224))
    return img


def r_steps(imgs, f):
    img = Image.new("RGB", (W, H), TEAL); d = ImageDraw.Draw(img); M = 80
    wordmark(d, M, 70, WHITE, 50)
    y = 170
    y = block(d, M, y, f["title"], F_black(60), WHITE, 72, W - 2 * M); y += 44
    for i, (head, sub) in enumerate(f["steps"], 1):
        th = 196
        d.rounded_rectangle([M, y, W - M, y + th], radius=24, fill=MINT_LT)
        d.ellipse([M + 28, y + 46, M + 28 + 104, y + 46 + 104], fill=GREEN)
        nw = d.textlength(str(i), font=F_black(60))
        d.text((M + 28 + 52 - nw / 2, y + 60), str(i), font=F_black(60), fill=WHITE)
        tx = M + 28 + 104 + 40
        d.text((tx, y + 52), head, font=F_black(40), fill=TEAL_DK)
        block(d, tx, y + 104, sub, F_reg(32), (70, 90, 84), 40, W - M - tx - 30)
        y += th + 26
    y += 6
    y = block(d, M, y, f["sub"], F_bold(36), AMBER, 46, W - 2 * M); y += 22
    chip(d, (M, y), f["cta"], F_black(36), fill=AMBER, fg=TEAL_DK)
    footnote(d, (210, 220, 216))
    return img


def r_textcard(imgs, f):
    img = Image.new("RGB", (W, H), f.get("bg", TEAL_DK)); d = ImageDraw.Draw(img)
    x, y = 72, 150
    wordmark(d, x, y, (150, 210, 195), 44); y += 96
    for q in f["questions"]:
        y = block(d, x, y, "“" + q + "”", F_black(54), WHITE, 66, W - 144); y += 26
    y += 10
    y = block(d, x, y, f["sub"], F_bold(40), AMBER, 50, W - 144); y += 28
    chip(d, (x, y), f["cta"], F_black(38), fill=AMBER, fg=TEAL_DK)
    footnote(d, (150, 190, 180))
    return img


def r_checklist(imgs, f):
    img = Image.new("RGB", (W, H), MINT_LT); d = ImageDraw.Draw(img); M = 76
    d.rectangle([0, 0, W, 132], fill=TEAL); wordmark(d, 64, 40, WHITE, 56)
    y = 196
    y = block(d, M, y, f["title"], F_black(62), TEAL_DK, 74, W - 2 * M); y += 44
    for it in f["items"]:
        d.ellipse([M, y + 2, M + 50, y + 52], fill=GREEN)
        check(d, M + 13, y + 9, 26, WHITE, 5)
        ny = block(d, M + 74, y, it, F_bold(38), INK, 46, W - 2 * M - 74)
        y = max(ny, y + 56) + 16
    y += 8
    if f.get("note"):
        y = block(d, M, y, f["note"], F_bold(38), GREEN_DK, 48, W - 2 * M); y += 24
    chip(d, (M, y), f["cta"], F_black(36))
    footnote(d, GREY)
    return img


def r_letter(imgs, f):
    img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img); M = 92
    wordmark(d, M, 110, TEAL, 50)
    y = 210
    for para in f["lines"]:
        y = block(d, M, y, para, F_serif(40), (44, 48, 46), 60, W - 2 * M); y += 28
    y += 12
    d.text((M, y), f.get("sign", "— the TrimRx team"), font=F_serif_i(44), fill=TEAL)
    y += 80
    chip(d, (M, y), f["cta"], F_black(34))
    footnote(d, GREY)
    return img


def r_hero(imgs, f):
    """Image-forward: full-bleed striking photo, ONE BIG punchy line, minimal text. Mobile-legible."""
    img = cover(imgs[""], W, H, vbias=f.get("vbias", 0.40)) if imgs.get("") else Image.new("RGB", (W, H), TEAL)
    pos = f.get("text_pos", "bottom")
    img = scrim(img, 0.66, 252, top=(pos == "top"))
    if pos == "bottom":
        img = scrim(img, 0.30, 150, top=True)  # gentle top scrim for the brand mark
    d = ImageDraw.Draw(img); M = 60
    wordmark(d, M, 60 if pos != "top" else H - 130, WHITE, 56)
    hs = f.get("hsize", 100); SUB = 50; KICK = 42; CTAS = 46
    hf = F_black(hs)
    head_lines = wrap(d, f["headline"], hf, W - 2 * M)
    sub_lines = wrap(d, f["sub"], F_bold(SUB), W - 2 * M) if f.get("sub") else []
    body_h = (len(head_lines) * (hs + 8) + (len(sub_lines) * (SUB + 10) + 18 if sub_lines else 0)
              + (KICK + 18 if f.get("kicker") else 0) + (CTAS + 60 if f.get("cta") else 0))
    if pos == "top":
        y = 150
    elif pos == "center":
        y = (H - body_h) // 2
    else:
        y = H - 100 - body_h - 24
    if f.get("kicker"):
        d.text((M, y), f["kicker"], font=F_black(KICK), fill=AMBER); y += KICK + 18
    for ln in head_lines:
        d.text((M, y), ln, font=hf, fill=WHITE); y += hs + 8
    y += 18
    for ln in sub_lines:
        d.text((M, y), ln, font=F_bold(SUB), fill=(240, 240, 240)); y += SUB + 10
    if f.get("cta"):
        y += 22
        chip(d, (M, y), f["cta"], F_black(CTAS), pad=(44, 26))
    footnote(d, (232, 232, 232))
    return img


def stroke_text(d, xy, text, fnt, fill=WHITE, stroke=(0, 0, 0), sw=8):
    d.text(xy, text, font=fnt, fill=fill, stroke_width=sw, stroke_fill=stroke)


def circle_paste(base, img, cx, cy, dia):
    im = cover(img, dia, dia, vbias=0.28)
    mask = Image.new("L", (dia, dia), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, dia, dia], fill=255)
    base.paste(im, (int(cx - dia / 2), int(cy - dia / 2)), mask)


def r_split(imgs, f):
    """50/50: photo (weight-loss context) on top, bold color block + BIG headline below."""
    img = Image.new("RGB", (W, H), f.get("bg", TEAL))
    ph = int(H * 0.55)
    if imgs.get(""):
        img.paste(cover(imgs[""], W, ph, vbias=f.get("vbias", 0.28)), (0, 0))
    img = scrim(img, 0.16, 120, top=True)
    d = ImageDraw.Draw(img); M = 60
    wordmark(d, M, 48, WHITE, 52)
    d.rectangle([0, ph, W, ph + 12], fill=AMBER)
    hs = f.get("hsize", 78); y = ph + 56
    y = block(d, M, y, f["headline"], F_black(hs), WHITE, hs + 10, W - 2 * M); y += 20
    if f.get("sub"):
        y = block(d, M, y, f["sub"], F_bold(42), MINT, 54, W - 2 * M); y += 26
    chip(d, (M, y), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, (210, 220, 216))
    return img


def r_magcover(imgs, f):
    """Health-magazine cover: full-bleed relatable model, masthead, bold cover lines."""
    img = cover(imgs[""], W, H, vbias=f.get("vbias", 0.22)) if imgs.get("") else Image.new("RGB", (W, H), TEAL)
    img = scrim(img, 0.50, 236)
    img = scrim(img, 0.22, 150, top=True)
    d = ImageDraw.Draw(img); M = 54
    d.text((M, 34), f["masthead"], font=F_black(106), fill=WHITE)
    hs = f.get("hsize", 74); subs = f.get("coverlines", [])
    head_lines = wrap(d, f["headline"], F_black(hs), W - 2 * M)
    y = H - 84 - len(head_lines) * (hs + 8) - len(subs) * 50 - (118 if f.get("cta") else 0) - 16
    for ln in head_lines:
        d.text((M, y), ln, font=F_black(hs), fill=AMBER); y += hs + 8
    y += 12
    for s in subs:
        check(d, M, y + 2, 30, GREEN, 6)
        d.text((M + 48, y), s, font=F_bold(38), fill=WHITE); y += 50
    if f.get("cta"):
        y += 20; chip(d, (M, y), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, (232, 232, 232))
    return img


def r_bigstat(imgs, f):
    """Number-dominant: HUGE stat up top, supporting weight-loss photo strip at the bottom."""
    img = Image.new("RGB", (W, H), f.get("bg", TEAL))
    sh = int(H * 0.40)
    if imgs.get(""):
        img.paste(cover(imgs[""], W, sh, vbias=0.30), (0, H - sh))
    img = scrim(img, 0.20, 175)
    d = ImageDraw.Draw(img); M = 60
    wordmark(d, M, 54, WHITE, 52)
    bs = 224
    while bs > 96 and d.textlength(f["big"], font=F_black(bs)) > W - 2 * M:
        bs -= 6
    d.text((M, 150), f["big"], font=F_black(bs), fill=AMBER)
    y = 150 + bs + 10
    y = block(d, M, y, f["label"], F_black(50), WHITE, 60, W - 2 * M); y += 14
    if f.get("sub"):
        block(d, M, y, f["sub"], F_bold(40), MINT, 50, W - 2 * M)
    chip(d, (M, H - sh + 44), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, (236, 236, 236))
    return img


def r_quote(imgs, f):
    """Branded testimonial quote card (NOT a chat/FB screenshot): big quote + circular photo."""
    img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img); M = 70
    d.text((38, 24), "“", font=F_serif_b(250), fill=GREEN)
    if imgs.get(""):
        circle_paste(img, imgs[""], W - 196, 250, 280)
    hs = f.get("hsize", 64); y = 470
    y = block(d, M, y, f["quote"], F_black(hs), INK, hs + 14, W - 2 * M); y += 26
    d.text((M, y), f.get("attrib", "— TrimRx member"), font=F_bold(38), fill=GREEN_DK); y += 74
    if f.get("sub"):
        y = block(d, M, y, f["sub"], F_bold(38), SAGE, 48, W - 2 * M); y += 22
    chip(d, (M, y), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, GREY)
    return img


def r_meme(imgs, f):
    """Relatable meme caption (impact text top+bottom) over a weight-loss photo. Not FB chrome."""
    img = cover(imgs[""], W, H, vbias=f.get("vbias", 0.32)) if imgs.get("") else Image.new("RGB", (W, H), INK)
    img = scrim(img, 0.34, 205, top=True)
    img = scrim(img, 0.42, 215)
    d = ImageDraw.Draw(img); M = 50
    ts = f.get("tsize", 62); y = 70
    for ln in wrap(d, f["top"], F_black(ts), W - 2 * M):
        stroke_text(d, (M, y), ln, F_black(ts), WHITE, (0, 0, 0), 7); y += ts + 8
    bs = f.get("bsize", 62); bl = wrap(d, f["bottom"], F_black(bs), W - 2 * M)
    by = H - 120 - len(bl) * (bs + 8)
    for ln in bl:
        stroke_text(d, (M, by), ln, F_black(bs), AMBER, (0, 0, 0), 7); by += bs + 8
    footnote(d, (236, 236, 236))
    return img


# TrimRx real product vials (transparent-bg PNGs — composite directly onto any ad)
PRODUCT = {"blue": os.path.join(OUT, "product", "vial_gip_blue.png"),   # tirzepatide GLP-1+GIP
           "duo": os.path.join(OUT, "product", "vials_duo.png")}        # semaglutide + tirzepatide pair


def paste_product(base, which="duo", height=560, cx=None, top=None, shadow=True):
    """Composite a TrimRx product vial (alpha PNG) onto base. cx=center-x, top=top-y."""
    p = Image.open(PRODUCT[which]).convert("RGBA")
    s = height / p.height
    p = p.resize((max(1, int(p.width * s)), height))
    cx = base.width // 2 if cx is None else cx
    x = int(cx - p.width / 2); y = 0 if top is None else top
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        from PIL import ImageFilter
        a = p.getchannel("A").point(lambda v: int(v * 0.35))
        blk = Image.new("RGBA", p.size, (0, 0, 0, 255)); blk.putalpha(a)
        sh.paste(blk, (x + 10, y + 22), blk)
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        base.alpha_composite(sh) if base.mode == "RGBA" else base.paste(sh, (0, 0), sh)
    base.paste(p, (x, y), p)
    return p.width, p.height


def r_product(imgs, f):
    """Product-forward: TrimRx vials as the hero + big price + CTA. Pure PIL (uses saved product PNG)."""
    img = Image.new("RGB", (W, H), MINT_LT); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 140], fill=TEAL); wordmark(d, 60, 38, WHITE, 54)
    ph = f.get("pheight", 600)
    paste_product(img, f.get("product", "duo"), height=ph, top=180)
    d = ImageDraw.Draw(img)
    y = 180 + ph + 28
    if f.get("kicker"):
        kw = d.textlength(f["kicker"], font=F_black(38)); d.text(((W - kw) / 2, y), f["kicker"], font=F_black(38), fill=SAGE); y += 56
    y = block(d, 60, y, f["headline"], F_black(f.get("hsize", 84)), TEAL_DK, f.get("hsize", 84) + 8, W - 120, center_w=W - 120); y += 16
    if f.get("sub"):
        y = block(d, 60, y, f["sub"], F_bold(38), SAGE, 48, W - 120, center_w=W - 120); y += 22
    cw = d.textlength(f["cta"][:-1].strip(), font=F_black(44)) + 150
    chip(d, ((W - cw) / 2, y), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, GREY, center=True)
    return img


def r_listicle(imgs, f):
    """'3 reasons' numbered listicle — photo banner on top, numbered reasons below."""
    img = Image.new("RGB", (W, H), MINT_LT)
    ph = int(H * 0.46)
    if imgs.get(""):
        img.paste(cover(imgs[""], W, ph, vbias=f.get("vbias", 0.24)), (0, 0))
    img = scrim(img, 0.14, 120, top=True)
    d = ImageDraw.Draw(img); M = 60
    wordmark(d, M, 44, WHITE, 50)
    y = ph + 40
    y = block(d, M, y, f.get("kicker", "3 REASONS WOMEN CHOOSE TRIMRX"), F_black(38), TEAL, 46, W - 2 * M); y += 24
    for i, item in enumerate(f["items"], 1):
        d.ellipse([M, y, M + 64, y + 64], fill=GREEN)
        nw = d.textlength(str(i), font=F_black(38)); d.text((M + 32 - nw / 2, y + 9), str(i), font=F_black(38), fill=WHITE)
        ny = block(d, M + 88, y + 4, item, F_bold(40), INK, 48, W - 2 * M - 88)
        y = max(ny, y + 70) + 16
    y += 8
    chip(d, (M, y), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, GREY)
    return img


def r_annotated(imgs, f):
    """Annotated photo — benefit 'tags' float over the image, big headline at the bottom."""
    img = cover(imgs[""], W, H, vbias=f.get("vbias", 0.3)) if imgs.get("") else Image.new("RGB", (W, H), TEAL)
    img = scrim(img, 0.42, 205)
    img = scrim(img, 0.18, 130, top=True)
    d = ImageDraw.Draw(img); M = 56
    wordmark(d, M, 44, WHITE, 50)
    ty = 250
    for t in f.get("tags", []):
        tw = d.textlength(t, font=F_bold(34)); bw = tw + 100
        bx = W - 48 - bw
        d.rounded_rectangle([bx, ty, bx + bw, ty + 70], radius=35, fill=(250, 250, 248))
        check(d, bx + 22, ty + 20, 26, GREEN, 5)
        d.text((bx + 64, ty + 16), t, font=F_bold(34), fill=TEAL_DK); ty += 90
    hf = F_black(f.get("hsize", 70)); hl = wrap(d, f["headline"], hf, W - 2 * M)
    y = H - 100 - len(hl) * (f.get("hsize", 70) + 8) - 112
    for ln in hl:
        d.text((M, y), ln, font=hf, fill=WHITE); y += f.get("hsize", 70) + 8
    y += 16; chip(d, (M, y), f["cta"], F_black(42), pad=(42, 24))
    footnote(d, (232, 232, 232))
    return img


def r_checkphoto(imgs, f):
    """Benefits checklist overlaid on a full-bleed lifestyle photo (distinct from the flat checklist)."""
    img = cover(imgs[""], W, H, vbias=f.get("vbias", 0.26)) if imgs.get("") else Image.new("RGB", (W, H), TEAL)
    img = scrim(img, 0.54, 218)
    d = ImageDraw.Draw(img); M = 56
    wordmark(d, M, 44, WHITE, 50)
    hs = f.get("hsize", 66); items = f["items"]
    hl = wrap(d, f["headline"], F_black(hs), W - 2 * M)
    blockh = len(hl) * (hs + 6) + 22 + len(items) * 64 + 120
    y = H - 88 - blockh
    for ln in hl:
        d.text((M, y), ln, font=F_black(hs), fill=WHITE); y += hs + 6
    y += 22
    for it in items:
        check(d, M, y + 2, 30, GREEN, 6); d.text((M + 52, y), it, font=F_bold(36), fill=WHITE); y += 64
    y += 16; chip(d, (M, y), f["cta"], F_black(42), pad=(42, 24))
    footnote(d, (232, 232, 232))
    return img


def r_flatlay(imgs, f):
    """Overhead lifestyle flat-lay (cues, no person) + minimal text."""
    img = cover(imgs[""], W, H, vbias=0.5) if imgs.get("") else Image.new("RGB", (W, H), MINT_LT)
    img = scrim(img, 0.40, 200)
    img = scrim(img, 0.16, 120, top=True)
    d = ImageDraw.Draw(img); M = 56
    wordmark(d, M, 44, WHITE, 50)
    hf = F_black(f.get("hsize", 72)); hl = wrap(d, f["headline"], hf, W - 2 * M)
    y = H - 100 - len(hl) * (f.get("hsize", 72) + 8) - (54 if f.get("sub") else 0) - 112
    for ln in hl:
        d.text((M, y), ln, font=hf, fill=WHITE); y += f.get("hsize", 72) + 8
    if f.get("sub"):
        y += 10; d.text((M, y), f["sub"], font=F_bold(38), fill=MINT); y += 54
    y += 16; chip(d, (M, y), f["cta"], F_black(42), pad=(42, 24))
    footnote(d, (232, 232, 232))
    return img


def r_faq(imgs, f):
    """Objection/FAQ card — bold Q&A pairs, small portrait inset. Vertically centered (no empty bottom)."""
    img = Image.new("RGB", (W, H), TEAL_DK); d = ImageDraw.Draw(img); M = 64
    wordmark(d, M, 56, WHITE, 52)
    if imgs.get(""):
        circle_paste(img, imgs[""], W - 150, 116, 200)
    qa = f["qa"]; tw = W - 2 * M - 64
    pair_h = [len(wrap(d, q, F_black(48), tw)) * 58 + 12 + len(wrap(d, a, F_bold(40), tw)) * 50 + 44 for q, a in qa]
    total = sum(pair_h) + 130  # + CTA
    y = max(300, (H - total) // 2)
    for q, a in qa:
        d.text((M, y), "Q", font=F_black(46), fill=AMBER)
        y = block(d, M + 64, y + 2, q, F_black(48), WHITE, 58, tw) + 12
        d.text((M, y), "A", font=F_black(46), fill=GREEN)
        y = block(d, M + 64, y + 2, a, F_bold(40), MINT, 50, tw) + 44
    y += 6
    chip(d, (M, y), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, (150, 190, 180))
    return img


def gradient_bg(c1, c2):
    base = Image.new("RGB", (W, H), c1); top = Image.new("RGB", (W, H), c2)
    m = Image.new("L", (1, H))
    for yy in range(H):
        m.putpixel((0, yy), int(255 * (yy / H) ** 1.1))
    base.paste(top, (0, 0), m.resize((W, H)))
    return base


def _ribbon(d, text, y, fill=CORAL, fg=WHITE):
    rf = F_black(34); rw = d.textlength(text, font=rf)
    d.rounded_rectangle([(W - rw - 76) / 2, y, (W + rw + 76) / 2, y + 70], radius=35, fill=fill)
    d.text(((W - rw) / 2, y + 15), text, font=rf, fill=fg)


def r_dr_offer(imgs, f):
    """DR offer hero: urgency ribbon + product vials + BIG price + CTA. Vertically centered."""
    img = gradient_bg(TEAL, TEAL_DK); d = ImageDraw.Draw(img)
    wordmark(d, 60, 46, WHITE, 52)
    ph = f.get("pheight", 460)
    bl = wrap(d, f["big"], F_black(92), W - 112)
    sl = wrap(d, f["sub"], F_bold(38), W - 120) if f.get("sub") else []
    total = (94 if f.get("ribbon") else 0) + ph + 16 + len(bl) * 100 + 8 + (len(sl) * 48 + 22 if sl else 0) + 112
    y = max(168, (H - 60 - total) // 2 + 50)
    if f.get("ribbon"): _ribbon(d, f["ribbon"], y); y += 94
    paste_product(img, f.get("product", "duo"), height=ph, top=y); d = ImageDraw.Draw(img); y += ph + 16
    y = block(d, 56, y, f["big"], F_black(92), WHITE, 100, W - 112, center_w=W - 112); y += 8
    if sl:
        y = block(d, 60, y, f["sub"], F_bold(38), MINT, 48, W - 120, center_w=W - 120); y += 22
    cw = d.textlength(f["cta"][:-1].strip(), font=F_black(44)) + 150
    chip(d, ((W - cw) / 2, y), f["cta"], F_black(44), fill=AMBER, fg=TEAL_DK, pad=(44, 26))
    footnote(d, (210, 220, 216), center=True)
    return img


def r_dr_probsol(imgs, f):
    """DR problem -> product -> solution + CTA (3-tier). Vertically centered."""
    img = gradient_bg(TEAL_DK, TEAL); d = ImageDraw.Draw(img)
    wordmark(d, 60, 44, WHITE, 50)
    ph = f.get("pheight", 360)
    pl = wrap(d, f["problem"], F_black(64), W - 120)
    sl = wrap(d, f["solution"], F_black(54), W - 120)
    total = len(pl) * 74 + 14 + ph + 22 + len(sl) * 64 + 24 + 112
    y = max(160, (H - 60 - total) // 2 + 50)
    y = block(d, 60, y, f["problem"], F_black(64), AMBER, 74, W - 120, center_w=W - 120); y += 14
    paste_product(img, f.get("product", "blue"), height=ph, top=y)
    d = ImageDraw.Draw(img); y = y + ph + 22
    y = block(d, 60, y, f["solution"], F_black(54), WHITE, 64, W - 120, center_w=W - 120); y += 24
    cw = d.textlength(f["cta"][:-1].strip(), font=F_black(44)) + 150
    chip(d, ((W - cw) / 2, y), f["cta"], F_black(44), fill=AMBER, fg=TEAL_DK, pad=(44, 26))
    footnote(d, (210, 220, 216), center=True)
    return img


def r_dr_value(imgs, f):
    """DR value: product vials left + $0 benefit list right + big price + CTA. Vertically centered."""
    img = Image.new("RGB", (W, H), MINT_LT); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 132], fill=TEAL); wordmark(d, 60, 38, WHITE, 54)
    n = len(f["included"]); list_h = n * 62; vial_h = 430
    bl = wrap(d, f["big"], F_black(76), W - 120)
    core = 84 + 24 + max(vial_h, list_h) + 26 + len(bl) * 86 + 14 + 112
    top = 132 + max(34, (H - 132 - 90 - core) // 2)
    y = block(d, 60, top, f["title"], F_black(58), TEAL_DK, 68, W - 120); y += 24
    cols = y
    paste_product(img, f.get("product", "duo"), height=vial_h, cx=296, top=cols)
    d = ImageDraw.Draw(img)
    ry = cols + 18; rx = 552; rend = W - 56
    for label, val in f["included"]:
        check(d, rx, ry + 4, 28, GREEN, 5)
        d.text((rx + 46, ry), label, font=F_bold(31), fill=INK)
        vw = d.textlength(val, font=F_black(34)); d.text((rend - vw, ry - 2), val, font=F_black(34), fill=GREEN_DK)
        ry += 62
    by = cols + max(vial_h, list_h) + 26
    by = block(d, 60, by, f["big"], F_black(76), TEAL_DK, 86, W - 120, center_w=W - 120); by += 14
    cw = d.textlength(f["cta"][:-1].strip(), font=F_black(44)) + 150
    chip(d, ((W - cw) / 2, by), f["cta"], F_black(44), pad=(44, 26))
    footnote(d, GREY, center=True)
    return img


def r_dr_urgency(imgs, f):
    """DR urgency poster: warm gradient, LIMITED-TIME ribbon, big lock-in price, vials, CTA. Centered."""
    img = gradient_bg(CORAL, (196, 72, 56)); d = ImageDraw.Draw(img)
    wordmark(d, 60, 46, WHITE, 52)
    ph = f.get("pheight", 320)
    bl = wrap(d, f["big"], F_black(100), W - 96)
    sl = wrap(d, f["sub"], F_bold(38), W - 120) if f.get("sub") else []
    total = 94 + len(bl) * 108 + 14 + (len(sl) * 48 + 18 if sl else 0) + ph + 24 + 116
    y = max(150, (H - 60 - total) // 2 + 40)
    _ribbon(d, f.get("ribbon", "LIMITED-TIME OFFER"), y, fill=WHITE, fg=(196, 72, 56)); y += 94
    y = block(d, 48, y, f["big"], F_black(100), WHITE, 108, W - 96, center_w=W - 96); y += 14
    if sl:
        y = block(d, 60, y, f["sub"], F_bold(38), (255, 238, 234), 48, W - 120, center_w=W - 120); y += 18
    paste_product(img, f.get("product", "duo"), height=ph, top=y + 6)
    d = ImageDraw.Draw(img); y = y + ph + 24
    cw = d.textlength(f["cta"][:-1].strip(), font=F_black(46)) + 160
    chip(d, ((W - cw) / 2, y), f["cta"], F_black(46), fill=WHITE, fg=(196, 72, 56), pad=(46, 28))
    footnote(d, (255, 236, 232), center=True)
    return img


def r_dr_hook(imgs, f):
    """DR hook question + product vials + CTA. Vertically centered."""
    img = gradient_bg(TEAL, TEAL_DK); d = ImageDraw.Draw(img)
    wordmark(d, 60, 46, WHITE, 52)
    ph = f.get("pheight", 350)
    hl = wrap(d, f["hook"], F_black(70), W - 112)
    sl = wrap(d, f["sub"], F_bold(38), W - 120) if f.get("sub") else []
    total = len(hl) * 80 + 16 + ph + 20 + (len(sl) * 48 + 20 if sl else 0) + 112
    y = max(158, (H - 60 - total) // 2 + 50)
    y = block(d, 56, y, f["hook"], F_black(70), WHITE, 80, W - 112, center_w=W - 112); y += 16
    paste_product(img, f.get("product", "blue"), height=ph, top=y)
    d = ImageDraw.Draw(img); y = y + ph + 20
    if sl:
        y = block(d, 60, y, f["sub"], F_bold(38), MINT, 48, W - 120, center_w=W - 120); y += 20
    cw = d.textlength(f["cta"][:-1].strip(), font=F_black(44)) + 150
    chip(d, ((W - cw) / 2, y), f["cta"], F_black(44), fill=AMBER, fg=TEAL_DK, pad=(44, 26))
    footnote(d, (210, 220, 216), center=True)
    return img


def _star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def r_compare(imgs, f):
    """1:1 'stop overpaying' price-ladder + ★ review + real product vial (clone + improve)."""
    SW = SH = 1080
    N1, N2 = (22, 46, 90), (9, 20, 44)
    img = Image.new("RGB", (SW, SH), N1); tp = Image.new("RGB", (SW, SH), N2)
    m = Image.new("L", (1, SH))
    for yy in range(SH):
        m.putpixel((0, yy), int(255 * (yy / SH) ** 1.25))
    img.paste(tp, (0, 0), m.resize((SW, SH)))
    d = ImageDraw.Draw(img)
    M = 56; PINK = (240, 72, 152); LBLU = (150, 182, 228); CARD = (15, 32, 64)
    paste_product(img, f.get("product", "blue"), height=560, cx=872, top=148)
    d = ImageDraw.Draw(img)
    hf = F_black(70); y = 56
    for ln in wrap(d, f["headline"], hf, 600):
        d.text((M, y), ln, font=hf, fill=WHITE); y += 76
    y += 8
    for ln in wrap(d, f["subhead"], F_bold(27), 600):
        d.text((M, y), ln, font=F_bold(27), fill=LBLU); y += 36
    ry = y + 20; cw = 600; ch = 188
    d.rounded_rectangle([M, ry, M + cw, ry + ch], radius=22, fill=(235, 240, 248))
    if f.get("avatar") and os.path.exists(f["avatar"]):
        circle_paste(img, Image.open(f["avatar"]).convert("RGBA"), M + 78, ry + 72, 104)
        d = ImageDraw.Draw(img)
    nx = M + 150
    d.text((nx, ry + 24), f.get("review_name", "Nina J."), font=F_black(32), fill=(18, 26, 42))
    for i in range(5):
        _star(d, nx + 18 + i * 40, ry + 72, 17, (0, 176, 118))
    block(d, nx, ry + 100, f["review"], F_bold(26), (44, 52, 68), 32, M + cw - nx - 24)
    ly = ry + ch + 26; rh = 110; gap = 18
    for label, price, ok in f["rows"]:
        d.rounded_rectangle([M, ly, M + 552, ly + rh], radius=16, fill=CARD)
        d.text((M + 28, ly + 16), label, font=F_bold(28), fill=LBLU)
        d.text((M + 26, ly + 50), price, font=F_black(50), fill=(PINK if ok else WHITE))
        if ok:
            check(d, M + 462, ly + 30, 60, (54, 226, 92), 13)
        else:
            cross(d, M + 470, ly + 34, 50, (236, 72, 60), 12)
        ly += rh + gap
    bx0, bx1, by0, bh = 640, 1052, 904, 104
    d.rounded_rectangle([bx0, by0, bx1, by0 + bh], radius=22, fill=GREEN)
    cl = wrap(d, f.get("cta", "Start your free assessment"), F_black(34), bx1 - bx0 - 48)
    cyy = by0 + (bh - len(cl) * 40) // 2 + 2
    for ln in cl:
        tw = d.textlength(ln, font=F_black(34)); d.text(((bx0 + bx1) / 2 - tw / 2, cyy), ln, font=F_black(34), fill=WHITE); cyy += 40
    fnt = ("Compounded medication. Requires prescription. Not FDA-approved. Individual results vary. "
           "Care provided by independent licensed physicians and pharmacies.")
    fy = SH - 100
    for ln in wrap(d, fnt, F_reg(21), 560):
        d.text((M, fy), ln, font=F_reg(21), fill=(150, 168, 198)); fy += 27
    return img


LANES = {"pricecard": r_pricecard, "versus": r_versus, "social": r_social, "texts": r_texts,
         "statement": r_statement, "caption_photo": r_caption_photo, "steps": r_steps,
         "textcard": r_textcard, "checklist": r_checklist, "letter": r_letter, "hero": r_hero,
         "split": r_split, "magcover": r_magcover, "bigstat": r_bigstat, "quote": r_quote, "meme": r_meme,
         "product": r_product, "listicle": r_listicle, "annotated": r_annotated, "checkphoto": r_checkphoto,
         "flatlay": r_flatlay, "faq": r_faq, "dr_offer": r_dr_offer, "dr_probsol": r_dr_probsol,
         "dr_value": r_dr_value, "dr_urgency": r_dr_urgency, "dr_hook": r_dr_hook, "compare": r_compare}

NOTEXT = (" Absolutely NO text, no letters, no numbers, no words, no captions, no watermark, no logo, "
          "no product packaging, no medical brand anywhere in the image.")
REAL = (" Photoreal candid documentary photo, natural skin texture with visible pores and fine lines, "
        "no beauty retouching, no filter, minimal makeup, an ordinary relatable everyday person, NOT a "
        "glamour or stock-model shot, NOT a doctor or medical professional, plain casual clothing.")
LIFE = (" Photoreal premium lifestyle photography, a real believable everyday woman with natural skin "
        "texture (not plastic, not over-retouched, no AI artifacts), vibrant true-to-life color, "
        "beautiful soft natural light, cinematic shallow depth of field, NOT a doctor or medical "
        "professional, NOT a glamour model." + " Leave the lower third simpler/darker for text overlay.")
PLUS = (" A relatable midsize-to-plus-size everyday woman with a fuller, realistic body type (this is a "
        "weight-loss program — clearly NOT a slim fitness model), natural real skin and features, warm "
        "and believable, minimal makeup, NOT glamour, NOT a doctor or medical professional, plain casual "
        "clothing, photoreal documentary-lifestyle photography, soft natural light.")
FIT = (" A real, healthy-looking woman who appears fit and energetic — representing someone doing well on "
       "her weight-loss journey — in well-fitting everyday activewear, genuine happy confident expression, "
       "natural real skin (not plastic, not a glamour model, no AI artifacts), NOT a doctor, photoreal "
       "lifestyle photography, soft natural light.")
MID = (" A relatable everyday woman about 40 of average / midsize build (not a slim model, not extreme), "
       "natural real skin, warm and believable, minimal makeup, NOT glamour, NOT a doctor, plain casual "
       "clothing, photoreal lifestyle photography, soft natural light.")


# --------------------------------------------------------------------------- the 10 ads
FORMATS = [
    dict(n=1, slug="pricecard", lane="pricecard", images={},
         title="One flat price. Everything included.",
         subtitle="Compounded GLP-1 · prescribed by licensed providers · delivered to your door",
         prices=[("Semaglutide (GLP-1)", "from $149/mo"), ("Tirzepatide (GLP-1+GIP)", "from $179/mo")],
         included=[("Unlimited provider visits", "$0"), ("Free dose increases", "$0"),
                   ("Expedited shipping", "$0"), ("Membership fees", "$0"), ("Hidden costs", "Never")],
         cta="See if you qualify →",
         headline="One Flat Price. Everything Included.",
         primary=("No upcharges when your dose changes, no membership games. From $149/month covers your "
                  "compounded GLP-1 medication, unlimited licensed-provider visits, and delivery to your "
                  "door. See if you qualify in 3 minutes.")),
    dict(n=2, slug="versus", lane="versus", images={},
         title="Weight-loss care without the waiting room",
         old=["Clinic waiting rooms", "Insurance approvals", "Weeks of back-and-forth", "Surprise costs"],
         new=["100% online", "Provider-prescribed in ~24 hrs", "From $149/month", "Delivered to your door"],
         cta="See if you qualify →",
         headline="Weight-Loss Care Without the Waiting Room",
         primary=("Getting GLP-1 care used to mean clinics, insurance hoops, and waiting. Now it's a "
                  "3-minute quiz, a licensed provider, and compounded medication shipped to your door — "
                  "from $149/month. See if you qualify.")),
    dict(n=3, slug="native_realization", lane="social",
         images={"": "A relatable woman about 42 with an everyday look sitting on her living-room couch in "
                     "soft natural daylight, holding her phone and a mug, glancing up with a small surprised "
                     "smile, cozy real home in the background." + REAL + NOTEXT},
         text=("I was today years old when I found out you can get a provider-prescribed GLP-1 for $149/month "
               "— no insurance, no waiting room. Took a 3-minute quiz and that was it."),
         cta="Learn more",
         headline="A Smarter Approach to Weight Loss",
         primary=("Turns out you don't need an in-person clinic or insurance to start GLP-1 care. A 3-minute "
                  "quiz, licensed providers, and compounded medication delivered — from $149/month.")),
    dict(n=4, slug="text_thread", lane="texts", images={},
         bubbles=[("in", "ok how is your weight-loss thing only $149??"),
                  ("out", "it's a compounded GLP-1 — the price covers the meds AND the licensed provider"),
                  ("in", "wait, no insurance?"),
                  ("out", "nope. did a 3-min quiz, got approved, ships straight to my door"),
                  ("in", "ok send me the link")],
         cta="See if you qualify →",
         headline="The Question Everyone Asks First",
         primary=("Does $149 really include the medication and the provider visit? It does — one flat price "
                  "for compounded GLP-1 care, no insurance needed. See if you qualify in 3 minutes.")),
    dict(n=5, slug="willpower", lane="statement", bg=TEAL, accent=AMBER, images={},
         kicker="IT WAS NEVER ABOUT WILLPOWER",
         big="Diets fight your hunger. A GLP-1 works with your biology.",
         sub="A compounded GLP-1 program may help quiet the food noise.",
         cta="See if you qualify →",
         headline="It Was Never About Willpower",
         primary=("If cutting calories only made the cravings louder, that's biology — not a lack of "
                  "discipline. A provider-guided, compounded GLP-1 program may help. See if you qualify.")),
    dict(n=6, slug="over40", lane="caption_photo", images={
        "": "A natural, relatable woman about 50 with light wrinkles and grey-streaked hair at her kitchen "
            "counter in warm morning light, calm and thoughtful, looking toward the window." + REAL + NOTEXT},
         kicker="OVER 40?",
         headline="The weight won't budge like it used to.",
         sub="After 40, hormones and metabolism shift. A provider-guided GLP-1 plan can help you respond.",
         cta="See if you qualify →",
         headline_fb="Weight Loss That Understands Your 40s",
         primary=("Hormones and metabolism change after 40 and the old tricks stop working. A compounded "
                  "GLP-1 plan, guided by licensed providers, can support you. See if you qualify.")),
    dict(n=7, slug="howitworks", lane="steps", images={},
         title="Getting started takes 3 minutes.",
         steps=[("Take the quiz", "A few quick questions — about 3 minutes."),
                ("Meet your provider", "A licensed provider reviews your information online."),
                ("Delivered to your door", "Your compounded GLP-1 ships discreetly to you.")],
         sub="Compounded GLP-1 from $149/month. No insurance needed.",
         cta="Start the 3-minute quiz →",
         headline="Getting Started Takes 3 Minutes",
         primary=("No clinic, no insurance, no guesswork: take a 3-minute quiz, get reviewed by a licensed "
                  "provider, and have compounded GLP-1 medication delivered. From $149/month.")),
    dict(n=8, slug="questions", lane="textcard", bg=TEAL_DK, images={},
         questions=["Why does the weight keep coming back?", "Is it my hormones?",
                    "Could a GLP-1 plan work for me?"],
         sub="Find out in a 3-minute quiz.",
         cta="See if you qualify →",
         headline="The Questions Worth Asking",
         primary=("If you've asked yourself any of these, a 3-minute quiz can tell you whether a compounded "
                  "GLP-1 program is a fit — reviewed by licensed providers. See if you qualify.")),
    dict(n=9, slug="included", lane="checklist", images={},
         title="Everything's included — one simple price.",
         items=["Unlimited licensed-provider consults", "Free dose increases, anytime",
                "Free expedited shipping", "Home injection kit included", "24/7 customer support"],
         note="Compounded GLP-1 from $149/month. No insurance needed.",
         cta="See if you qualify →",
         headline="Everything's Included — One Price",
         primary=("One simple price covers it: unlimited licensed-provider consults, free dose increases, "
                  "free shipping, your home kit, and 24/7 support. Compounded GLP-1 from $149/month.")),
    dict(n=10, slug="transparency", lane="letter", images={},
         lines=["If a weight-loss site has burned you before, read this.",
                "Most telehealth programs take your money and disappear. We built TrimRx differently — one "
                "flat price, licensed providers, and real people who pick up the phone.",
                "Compounded GLP-1 care, from $149/month. No insurance, no hidden fees.",
                "See if you qualify — it takes about 3 minutes."],
         sign="— the TrimRx team",
         cta="See if you qualify →",
         headline="Built for People Who Got Burned Before",
         primary=("Burned by a weight-loss site before? We built TrimRx differently: flat pricing, licensed "
                  "providers, compounded GLP-1 from $149/month, and no hidden fees. See if you qualify.")),

    # ---- image-forward "hero" direction (big font, striking photo, minimal text, NO FB-UI chrome) ----
    dict(n=11, slug="hero_confident", lane="hero", vbias=0.30,
         images={"": "A radiant confident woman about 44 with a warm genuine laugh, wearing flattering "
                     "everyday jeans and a simple fitted top, standing in a bright sunlit modern living room, "
                     "joyful and energetic, golden afternoon light." + LIFE + NOTEXT},
         headline="Feeling like yourself again.", hsize=100,
         sub="Compounded GLP-1, from $149/mo.", cta="See if you qualify →",
         headline_fb="A Smarter Approach to Weight Loss",
         primary=("A telehealth weight-loss program built around you: a 3-minute quiz, licensed providers, "
                  "and compounded GLP-1 medication delivered — from $149/month. See if you qualify.")),
    dict(n=12, slug="foodnoise", lane="hero", vbias=0.34,
         images={"": "Editorial close-up: a calm, content woman about 38 sitting at a cafe table holding a "
                     "warm cup of coffee, a plate of tempting pastries and donuts softly blurred in the "
                     "foreground, she looks serene and uninterested in the food, moody cinematic side light, "
                     "rich shallow depth of field." + NOTEXT},
         headline="The all-day food noise? Finally quiet.", hsize=86,
         cta="See if you qualify →",
         headline_fb="Quiet the Food Noise",
         primary=("If you think about food all day, that's biology — not willpower. A compounded GLP-1 "
                  "program, guided by licensed providers, may help. See if you qualify in 3 minutes.")),
    dict(n=13, slug="price_hero", lane="hero", vbias=0.32,
         images={"": "A happy, relatable woman about 40 in a bright sunny kitchen holding a glass of water, "
                     "looking out the window with a calm smile, airy premium lifestyle photography, vibrant "
                     "morning light." + LIFE + NOTEXT},
         kicker="COMPOUNDED GLP-1", headline="$149/mo. Everything included.", hsize=92,
         sub="Visits, shipping & dose changes — included.", cta="See if you qualify →",
         headline_fb="One Flat Price. Everything Included.",
         primary=("From $149/month covers your compounded GLP-1 medication, unlimited licensed-provider "
                  "visits, free dose changes, and delivery. No insurance needed. See if you qualify.")),

    # ---- 5 NEW FORMATS (each a different structure) + weight-loss imagery + big fonts ----
    dict(n=14, slug="split_journey", lane="split", vbias=0.26,
         images={"": "A relatable plus-size woman about 40 in simple fitted activewear standing in profile "
                     "in soft daylight in a calm home, one hand resting gently on her midsection, looking "
                     "thoughtful and hopeful, fuller realistic figure." + PLUS + NOTEXT},
         headline="Your weight-loss journey, made simple.", hsize=76,
         sub="Compounded GLP-1, from $149/mo.", cta="See if you qualify →",
         headline_fb="Your Weight-Loss Journey, Made Simple",
         primary=("A telehealth weight-loss program built around you — a 3-minute quiz, licensed providers, "
                  "and compounded GLP-1 medication delivered. From $149/month, no insurance needed.")),
    dict(n=15, slug="magcover", lane="magcover", vbias=0.20,
         images={"": "A warm, confident midsize woman about 46 in a cozy sweater with a gentle genuine "
                     "smile, looking right at the camera, clean soft studio background, fuller relatable "
                     "figure, magazine-cover portrait lighting." + PLUS + NOTEXT},
         masthead="TRIMRX", headline="The $149/mo GLP-1 program", hsize=72,
         coverlines=["No insurance needed", "Delivered to your door", "Prescribed by licensed providers"],
         cta="See if you qualify →",
         headline_fb="The $149/mo GLP-1 Program",
         primary=("Compounded GLP-1 care without the clinic: a 3-minute quiz, licensed providers, and "
                  "medication delivered to your door. From $149/month, no insurance needed.")),
    dict(n=16, slug="socialproof", lane="bigstat", vbias=0.30,
         images={"": "A relatable midsize woman about 38 stepping onto a bathroom scale at home, looking "
                     "down with quiet hope, soft morning bathroom light, fuller realistic body." + PLUS + NOTEXT},
         big="300,000+", label="started their journey online",
         sub="Compounded GLP-1 from $149/mo. No insurance needed.", cta="See if you qualify →",
         headline_fb="Join Hundreds of Thousands Online",
         primary=("Hundreds of thousands have started a telehealth GLP-1 program online — no clinic, no "
                  "insurance. Compounded GLP-1 from $149/month. See if you qualify in 3 minutes.")),
    dict(n=17, slug="quote", lane="quote", vbias=0.26,
         images={"": "A relatable plus-size woman about 42 sitting relaxed on her sofa at home with a warm "
                     "genuine smile, natural window light, fuller realistic body." + PLUS + NOTEXT},
         quote="I stopped fighting my body and finally asked for help.", attrib="— TrimRx member", hsize=62,
         sub="Compounded GLP-1, from $149/mo.", cta="See if you qualify →",
         headline_fb="I Finally Asked for Help",
         primary=("Asking for help isn't giving up. A compounded GLP-1 program, guided by licensed "
                  "providers, may help — from $149/month. See if you qualify. Individual results vary.")),
    dict(n=18, slug="meme_jeans", lane="meme", vbias=0.30,
         images={"": "A relatable plus-size woman about 35 in her bedroom holding up a pair of jeans that no "
                     "longer fit her, candid and real, soft natural light, fuller body, a little frustrated "
                     "but hopeful." + PLUS + NOTEXT},
         top="POV: the jeans haven't fit in two years", tsize=60,
         bottom="so she started a $149/mo GLP-1 program", bsize=58,
         headline_fb="When the Jeans Don't Fit Anymore",
         primary=("If the jeans haven't fit in years, you're not alone — and it's not about willpower. A "
                  "compounded GLP-1 program may help. From $149/month, no insurance needed. See if you qualify.")),
    dict(n=19, slug="product_price", lane="product", images={},
         product="duo", pheight=600, kicker="COMPOUNDED GLP-1",
         headline="From $149/month.", hsize=86,
         sub="Semaglutide or tirzepatide — prescribed by licensed providers, delivered.",
         cta="See if you qualify →",
         headline_fb="Compounded GLP-1 From $149/Month",
         primary=("Compounded GLP-1 care — semaglutide or tirzepatide — prescribed by licensed providers "
                  "and delivered to your door, from $149/month. No insurance needed. See if you qualify.")),

    # ---- batch 3: 5 NEW formats, MIXED body types (fit/lost-weight + midsize + cues) ----
    dict(n=20, slug="listicle_reasons", lane="listicle", vbias=0.22,
         images={"": "A fit, energetic woman about 40 mid-stride on a sunny morning walk outdoors, "
                     "genuinely happy and confident, healthy glow, well-fitting activewear." + FIT + NOTEXT},
         kicker="3 REASONS WOMEN CHOOSE TRIMRX",
         items=["Helps quiet all-day cravings", "One flat price from $149/mo — visits & shipping included",
                "Delivered to your door — no clinic, no insurance"],
         cta="See if you qualify →",
         headline_fb="3 Reasons Women Choose TrimRx",
         primary=("A telehealth GLP-1 program that helps quiet cravings, at one flat price from $149/month "
                  "with visits and shipping included, delivered to your door. See if you qualify.")),
    dict(n=21, slug="annotated", lane="annotated", vbias=0.28,
         images={"": "A relatable midsize woman about 42 standing in soft daylight at home in casual "
                     "clothes, calm and hopeful, average everyday body." + MID + NOTEXT},
         tags=["From $149/mo, all-in", "Licensed providers", "Delivered to your door"],
         headline="GLP-1 care, simplified.", hsize=72, cta="See if you qualify →",
         headline_fb="GLP-1 Care, Simplified",
         primary=("Everything in one flat price: compounded GLP-1 medication, licensed-provider visits, and "
                  "delivery — from $149/month, no insurance needed. See if you qualify in 3 minutes.")),
    dict(n=22, slug="checkphoto", lane="checkphoto", vbias=0.24,
         images={"": "A fit, happy woman about 38 sitting on her front steps lacing up running shoes in "
                     "golden morning light, energetic and healthy, well-fitting activewear." + FIT + NOTEXT},
         headline="Your routine, finally working with you.", hsize=64,
         items=["Compounded GLP-1, from $149/mo", "Unlimited licensed-provider visits",
                "Free shipping & dose changes"],
         cta="See if you qualify →",
         headline_fb="A Routine That Works With You",
         primary=("Compounded GLP-1 from $149/month with unlimited licensed-provider visits and free "
                  "shipping and dose changes. A telehealth program built to fit your life. See if you qualify.")),
    dict(n=23, slug="flatlay", lane="flatlay",
         images={"": "Overhead flat-lay on a clean light marble surface: a glass of water with lemon, an "
                     "open blank journal, a coiled cloth tape measure, clean white sneakers, a small sprig "
                     "of greenery, soft natural light, premium tidy wellness composition, no text, no "
                     "labels, no branded packaging." + NOTEXT},
         headline="Everything you need to start.", hsize=72,
         sub="Compounded GLP-1, from $149/mo.", cta="See if you qualify →",
         headline_fb="Everything You Need to Start",
         primary=("A simple telehealth weight-loss program: a 3-minute quiz, licensed providers, and "
                  "compounded GLP-1 delivered to your door — from $149/month. See if you qualify.")),
    dict(n=24, slug="faq", lane="faq", vbias=0.22,
         images={"": "A fit, smiling woman about 40, head and shoulders, healthy and confident, natural "
                     "light, well-fitting top." + FIT + NOTEXT},
         qa=[("Do I need insurance?", "No — one flat price from $149/mo."),
             ("Have to visit a clinic?", "No. Licensed providers review you online."),
             ("How do I start?", "A 3-minute quiz to see if you qualify.")],
         cta="See if you qualify →",
         headline_fb="Your GLP-1 Questions, Answered",
         primary=("No insurance, no clinic visits: a 3-minute quiz, licensed-provider review online, and "
                  "compounded GLP-1 delivered — from $149/month. See if you qualify.")),

    # ---- batch 4: DIRECT-RESPONSE, product-forward (real vials in every one) ----
    dict(n=25, slug="dr_offer", lane="dr_offer", images={}, product="duo", pheight=460,
         ribbon="LIMITED-TIME PRICING", big="$149/mo.",
         sub="Everything included — no insurance, no hidden fees.", cta="See if you qualify →",
         headline_fb="$149/mo — Everything Included",
         primary=("One flat price covers your compounded GLP-1 medication, licensed-provider visits, and "
                  "delivery — from $149/month, no insurance, no hidden fees. See if you qualify in 3 minutes.")),
    dict(n=26, slug="dr_probsol", lane="dr_probsol", images={}, product="blue", pheight=360,
         problem="Cravings running the show?", solution="A compounded GLP-1 may help. From $149/mo.",
         cta="See if you qualify →",
         headline_fb="Quiet the Cravings",
         primary=("If you think about food all day, a compounded GLP-1 program may help quiet the noise — "
                  "guided by licensed providers, from $149/month. See if you qualify.")),
    dict(n=27, slug="dr_value", lane="dr_value", images={}, product="duo",
         title="What $149/mo gets you:",
         included=[("Licensed-provider visits", "$0"), ("Expedited shipping", "$0"),
                   ("Dose increases", "$0"), ("Membership fees", "$0"), ("Hidden costs", "$0")],
         big="All-in — from $149/mo.", cta="See if you qualify →",
         headline_fb="Everything Included for $149/mo",
         primary=("From $149/month: compounded GLP-1 medication, unlimited licensed-provider visits, free "
                  "shipping, free dose increases, no membership fees, no hidden costs. See if you qualify.")),
    dict(n=28, slug="dr_urgency", lane="dr_urgency", images={}, product="duo", pheight=320,
         ribbon="LIMITED-TIME OFFER", big="LOCK IN $149/MO",
         sub="Compounded GLP-1 · no insurance needed.", cta="See if you qualify →",
         headline_fb="Lock In $149/mo",
         primary=("Lock in compounded GLP-1 care from $149/month — licensed providers, delivered, no "
                  "insurance needed. See if you qualify in 3 minutes.")),
    dict(n=29, slug="dr_hook", lane="dr_hook", images={}, product="blue", pheight=350,
         hook="Tried every diet and the weight won't go?",
         sub="It may not be willpower — a compounded GLP-1 may help. From $149/mo.",
         cta="See if you qualify →",
         headline_fb="It May Not Be Willpower",
         primary=("If diets keep failing, it may not be willpower — it's biology. A compounded GLP-1 "
                  "program, guided by licensed providers, may help. From $149/month. See if you qualify.")),

    # ---- cloned + improved "stop overpaying" price-ladder (1:1) ----
    dict(n=30, slug="compare_overpay", lane="compare", images={}, product="blue",
         avatar="outputs/trimrx_glp1/base/faq.png",
         headline="STOP OVERPAYING FOR TIRZEPATIDE.",
         subhead="Provider-prescribed · All doses included · Free shipping",
         review_name="Nina J.",
         review="I was paying double at a local med spa. TrimRx was a no-brainer.",
         rows=[("At a local clinic", "$1,000+/mo", False),
               ("Typical online programs", "$299/mo", False),
               ("TrimRx", "$279/mo", True)],
         cta="Start your free assessment",
         headline_fb="Stop Overpaying for Your GLP-1",
         primary=("Telehealth GLP-1 care at a fraction of typical clinic pricing: tirzepatide (GLP-1 + GIP) "
                  "from $279/month, all doses and shipping included, prescribed by licensed providers. "
                  "Start your free assessment.")),
]


def gen_base(slug, key, prompt, regen=False):
    fn = f"{slug}.png" if key == "" else f"{slug}__{key}.png"
    dest = os.path.join(BASE_DIR, fn)
    if os.path.exists(dest) and not regen:
        return slug, key, dest, "skip"
    try:
        res = kie.generate_gpt_image(prompt, aspect_ratio="3:4", resolution="2K")
    except Exception as e:
        return slug, key, None, f"err:{e}"
    if res.get("status") != "success" or not res.get("urls"):
        return slug, key, None, f"fail:{str(res.get('raw'))[:120]}"
    kie.download(res["urls"][0], dest)
    return slug, key, dest, "ok"


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
            futs = {ex.submit(gen_base, s, k, p, s in regen): (s, k) for s, k, p in jobs}
            for fut in as_completed(futs):
                s, k, path, st = fut.result()
                print(f"[base:{st}] {s} {k or ''} -> {path}", flush=True)
                bases[(s, k)] = path

    print("---- rendering ----", flush=True)
    copy_lines = ["# TrimRx GLP-1 — FB ad copy (headline + primary text)\n",
                  "Every primary text MUST end with the mandatory disclaimer (appended below).\n"]
    for f in fmts:
        imgs = {}
        for k in f.get("images", {}):
            p = bases.get((f["slug"], k))
            imgs[k] = Image.open(p).convert("RGB") if p and os.path.exists(p) else None
        img = LANES[f["lane"]](imgs, f)
        out = os.path.join(FINAL_DIR, f"{f['n']:02d}_{f['slug']}_4x5.png")
        img.save(out)
        miss = [k or "(main)" for k in f.get("images", {}) if imgs.get(k) is None]
        print(f"[render] {out}{'  MISSING:' + ','.join(miss) if miss else ''}", flush=True)
        hl = f.get("headline_fb", f.get("headline", ""))
        copy_lines.append(f"\n## {f['n']:02d} · {f['slug']}  ({f['lane']})\n")
        copy_lines.append(f"**Headline:** {hl}\n")
        copy_lines.append(f"**Primary text:** {f.get('primary','')}\n\n{DISC}\n")

    with open(os.path.join(OUT, "copy.md"), "w") as fh:
        fh.write("\n".join(copy_lines))
    print(f"[copy] wrote {os.path.join(OUT, 'copy.md')}", flush=True)


if __name__ == "__main__":
    main()
