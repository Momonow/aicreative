#!/usr/bin/env python3
"""HyperFrames PIP composite for the women's-prison yapper ads: a matted persona
(alpha webm) doing TikTok-native DRIFT motion (seeded random-walk wander + scale swell)
as a bottom-anchored SIDE INSET over ROTATING prison b-roll backdrops (Ken Burns each).

Unlike the depo `hf-pip-composite` supersize bottom-band, here the persona is a side inset
so it never covers the backdrop's main subject (guard/inmate). Rotation set is chosen so all
subjects sit OPPOSITE the persona's side.

Usage:
  cawp_hf_pip.py <LETTER> <slug1,slug2,...> [--interval 5] [--side right|left] [--seed 7]
                 [--pip-w 560] [--pip-h 1000] [--quality draft|high]

  persona alpha : outputs/chowchilla_podcast/<L>_full_alpha.webm  (VEED/fal vp9 alpha, has audio)
  backdrops     : outputs/cawp_broll_wp/vert/<slug>.png
  proj          : outputs/chowchilla_podcast/hf_<L>/
  out           : outputs/chowchilla_podcast/<L>_hf.mp4   (1080x1920, NO captions yet)

Caption after with:  caption_nick.py <L>_hf.mp4 --vertical-pos 0.85
Determinism: the random walk is generated HERE (seeded) and emitted as literal GSAP tweens.
"""
import math
import os
import random
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POD  = os.path.join(ROOT, "outputs", "chowchilla_podcast")
VERT = os.path.join(ROOT, "outputs", "cawp_broll_wp", "vert")
W, H = 1080, 1920
FPS  = 30


def arg(flag, default=None, cast=str):
    if flag in sys.argv:
        return cast(sys.argv[sys.argv.index(flag) + 1])
    return default


def probe_dur(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path]).decode().strip())


def resolve_slug(slug):
    p = os.path.join(VERT, f"{slug}.png")
    if os.path.exists(p):
        return slug
    for f in sorted(os.listdir(VERT)):
        if f.endswith(".png") and f.startswith(f"{slug}_"):
            return f[:-4]
    raise FileNotFoundError(slug)


def main():
    L = sys.argv[1]
    slugs = [resolve_slug(s.strip()) for s in sys.argv[2].split(",") if s.strip()]
    interval = arg("--interval", 5.0, float)
    side = arg("--side", "right")
    seed = arg("--seed", 7, int)
    pip_w = arg("--pip-w", 560, int)
    pip_h = arg("--pip-h", 1000, int)
    motion = arg("--motion", "drift")     # drift | hopper
    quality = arg("--quality", "draft")

    alpha = os.path.join(POD, f"{L}_full_alpha.webm")
    assert os.path.exists(alpha), alpha
    dur = probe_dur(alpha)

    proj = os.path.join(POD, f"hf_{L}")
    assets = os.path.join(proj, "assets")
    os.makedirs(assets, exist_ok=True)
    # minimal project files
    with open(os.path.join(proj, "hyperframes.json"), "w") as f:
        f.write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n'
                '  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}\n}\n')
    with open(os.path.join(proj, "package.json"), "w") as f:
        f.write('{\n  "name": "hf-%s",\n  "private": true,\n  "scripts": {\n'
                '    "render": "npx --yes hyperframes@0.7.58 render"\n  }\n}\n' % L.lower())

    shutil.copy(alpha, os.path.join(assets, "matte.webm"))
    for i, slug in enumerate(slugs):
        shutil.copy(os.path.join(VERT, f"{slug}.png"), os.path.join(assets, f"bg{i}.png"))

    # ---- segment plan (rotate backdrops in a SEEDED-SHUFFLED order, no adjacent repeats) ----
    n_seg = max(1, math.ceil(dur / interval))
    rnd_bg = random.Random(seed * 131 + 7)
    order = []
    while len(order) < n_seg:
        block = list(range(len(slugs)))
        rnd_bg.shuffle(block)
        if order and len(slugs) > 1 and block[0] == order[-1]:
            block.append(block.pop(0))        # avoid a backdrop repeating across the wrap
        order += block
    order = order[:n_seg]
    segs = []
    for i in range(n_seg):
        s = i * interval
        e = min((i + 1) * interval, dur)
        segs.append((order[i], s, e))

    # ---- seeded random-walk waypoints for the PIP ----
    rnd = random.Random(seed)
    rest_left = (W - pip_w - 34) if side == "right" else 34
    if motion == "hopper":
        # TikTok tilt: big left<->right hops across the FULL width, big size + rotation change
        xmin, xmax = 24, W - pip_w - 24
        ybob = 60
    else:
        xspan = 60
        ybob = 34
        xmin, xmax = rest_left - xspan, rest_left + xspan
        if side == "right":
            xmin = max(xmin, W // 2 + 10)
        else:
            xmax = min(xmax, W // 2 - pip_w - 10)
    wp_dt = arg("--hop-secs", 4.0, float) if motion == "hopper" else 2.6
    n_wp = max(2, int(round(dur / wp_dt)) + 1)
    pts = []              # (t, x, y, scale, rot)
    px = rest_left
    prev_side = 0
    for k in range(n_wp):
        for _ in range(10):
            if motion == "hopper":
                # alternate left/right halves so hops read as big section jumps
                if prev_side >= 0:
                    nx = rnd.uniform(xmin, xmin + (xmax - xmin) * 0.42)
                    cur_side = -1
                else:
                    nx = rnd.uniform(xmin + (xmax - xmin) * 0.58, xmax)
                    cur_side = 1
                ny = rnd.uniform(-ybob, ybob)
                ns = rnd.choice([0.95, 1.06, 1.14, 1.22])
                nr = rnd.choice([-13, -9, 9, 13])
            else:
                nx = rnd.uniform(xmin, xmax)
                ny = rnd.uniform(-ybob, ybob)
                ns = rnd.uniform(0.95, 1.10)
                nr, cur_side = 0, 0
            if abs(nx - px) > (180 if motion == "hopper" else 40) or k == 0:
                break
        if k == 0:
            nx, ny, ns, nr = rest_left, 0, 1.0, 0
            cur_side = -1 if side == "right" else 1
        pts.append((k * wp_dt, nx, ny, ns, nr))
        px = nx
        prev_side = cur_side

    # ---- build HTML ----
    bg_divs, bg_tw = [], []
    for i, (bi, s, e) in enumerate(segs):
        seg_dur = e - s + (0.30 if i < n_seg - 1 else 0.0)   # overlap for crossfade
        z = 1     # DOM order = later on top
        bg_divs.append(
            f'<div id="bg{i}" class="clip" data-start="{s:.3f}" data-duration="{seg_dur:.3f}" '
            f'data-track-index="0" style="position:absolute;inset:0;'
            f'background:url(\'assets/bg{bi}.png\') center center/cover no-repeat;'
            f'opacity:{0 if i>0 else 1};transform-origin:{"38% 30%" if i%2==0 else "60% 35%"};"></div>'
        )
        if motion == "hopper":
            # snap-zoom: instant scale set, then hold (punchy cut feel)
            snap = [1.02, 1.14, 1.08, 1.18][i % 4]
            bg_tw.append(f'tl.set("#bg{i}",{{scale:{snap}}},{s:.3f});')
            if i > 0:
                bg_tw.append(f'tl.set("#bg{i}",{{opacity:1}},{s:.3f});')
        else:
            # Ken Burns: alternate push-in / pull-back
            if i % 2 == 0:
                bg_tw.append(f'tl.fromTo("#bg{i}",{{scale:1.02}},{{scale:1.16,duration:{e-s+0.3:.2f},ease:"sine.out"}},{s:.3f});')
            else:
                bg_tw.append(f'tl.fromTo("#bg{i}",{{scale:1.16}},{{scale:1.02,duration:{e-s+0.3:.2f},ease:"sine.out"}},{s:.3f});')
            if i > 0:
                bg_tw.append(f'tl.to("#bg{i}",{{opacity:1,duration:0.28,ease:"power1.out"}},{s:.3f});')

    # PIP tweens
    if motion == "hopper":
        x0, y0, s0, r0 = pts[0][1], pts[0][2], pts[0][3], pts[0][4]
        pip_tw = [f'gsap.set("#pip",{{x:{x0-rest_left:.1f},y:{-y0:.1f},scale:{s0:.3f},rotation:{r0}}});']
        for k in range(1, len(pts)):
            tk = min(pts[k][0], dur)
            _, nx, ny, ns, nr = pts[k]
            pip_tw.append(
                f'tl.to("#pip",{{x:{nx-rest_left:.1f},y:{-ny:.1f},scale:{ns:.3f},rotation:{nr},'
                f'duration:0.05,ease:"none"}},{tk:.3f});'
            )
    else:
        # DRIFT = big continuous glide across the safe band + scale swell + slow y bob,
        # all running concurrently (like the hf-pip-composite template).
        travel = 240                       # px horizontal glide
        if side == "right":
            off_hi = (W - pip_w - 24) - rest_left      # near far-right
            off_lo = off_hi - travel                    # toward center
        else:
            off_lo = 24 - rest_left
            off_hi = off_lo + travel
        seg = 8.5
        n_g = max(1, int(math.ceil(dur / seg)))
        pip_tw = [f'gsap.set("#pip",{{x:{off_lo:.1f},y:0,scale:0.97}});']
        t = 0.2
        cur_hi = True
        for _ in range(n_g):
            d = min(seg, dur - t)
            if d <= 0.3:
                break
            target = off_hi if cur_hi else off_lo
            pip_tw.append(f'tl.to("#pip",{{x:{target:.1f},duration:{d:.2f},ease:"sine.inOut"}},{t:.3f});')
            t += d
            cur_hi = not cur_hi
        rep_s = max(1, int(round(dur / 4.6)))
        pip_tw.append(f'tl.to("#pip",{{scale:1.13,duration:4.6,ease:"sine.inOut",yoyo:true,repeat:{rep_s}}},0.2);')
        rep_y = max(1, int(round(dur / 3.4)))
        pip_tw.append(f'tl.to("#pip",{{y:-26,duration:3.4,ease:"sine.inOut",yoyo:true,repeat:{rep_y}}},0.0);')

    left_css = rest_left
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;}}
#pip{{position:absolute;left:{left_css}px;bottom:0;width:{pip_w}px;height:{pip_h}px;
  object-fit:cover;object-position:50% 10%;transform-origin:bottom center;z-index:5;}}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur:.3f}" data-width="1080" data-height="1920">
{chr(10).join(bg_divs)}
<video id="pip" class="clip" src="assets/matte.webm" data-start="0" data-duration="{dur:.3f}" data-track-index="1" muted playsinline></video>
<audio id="pip-audio" src="assets/matte.webm" data-start="0" data-duration="{dur:.3f}" data-track-index="10" data-volume="1"></audio>
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{chr(10).join(bg_tw)}
{chr(10).join(pip_tw)}
window.__timelines["main"]=tl;
</script></body></html>
"""
    with open(os.path.join(proj, "index.html"), "w") as f:
        f.write(html)

    out = os.path.join(POD, f"{L}{arg('--out-suffix', '_hf')}.mp4")
    cmd = ["npx", "--yes", "hyperframes@0.7.58", "render",
           "--quality", quality, "--output", out]
    print("rendering", L, "| segs:", ",".join(slugs[bi] for bi, _, _ in segs), flush=True)
    subprocess.run(cmd, cwd=proj, check=True)
    print("OK", out)


if __name__ == "__main__":
    main()
