"""Crop the wide L-tracks shot into 2 single-character portrait anchors.

Source: outputs/illinois_jdc_news_eltracks/wide/wide_shot.png (1536x1024 landscape)

Reporter (LEFT character, ~25% of width) — crop a portrait window centered
on him, including the mic extending toward right.

Interviewee (RIGHT character, ~70% of width) — crop a portrait window
centered on him, including the mic tip from off-frame-left.

Each cropped portrait is then resized to 720x1280 (9:16, Veo output size).

Output:
  outputs/illinois_jdc_news_eltracks/wide/reporter_solo.png  (720x1280)
  outputs/illinois_jdc_news_eltracks/wide/interviewee_solo.png (720x1280)
"""
from pathlib import Path
from PIL import Image

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/wide")
src = OUT_DIR / "wide_shot.png"

img = Image.open(src)
w, h = img.size
print(f"Source: {w}x{h}")

# Reporter crop: from x=0 to ~52% of width. 9:16 portrait = w/h = 9/16 = 0.5625.
# Take crop_w = 0.52*W = 800, crop_h = 800 / 9 * 16 = 1422 — but source is only 1024 tall.
# So crop_h = 1024 (full source height), crop_w = 1024 * 9 / 16 = 576.
# Reporter face center ≈ x = 0.18 * 1536 = 280.
# Crop_w 576 centered at x=280 → crop_x0 = max(0, 280 - 288) = 0, crop_x1 = 576.
rep_x0, rep_x1 = 0, 576
reporter = img.crop((rep_x0, 0, rep_x1, h))
print(f"Reporter crop: ({rep_x0}, 0) - ({rep_x1}, {h}) = {reporter.size}")

# Interviewee crop: face center ≈ x = 0.78 * 1536 = 1198.
# crop_w 576 centered at x=1198 → x0 = 1198 - 288 = 910, x1 = 1486.
# Better: pull right edge to source max (1536) to keep his right shoulder.
int_x1 = w
int_x0 = w - 576  # = 960
interviewee = img.crop((int_x0, 0, int_x1, h))
print(f"Interviewee crop: ({int_x0}, 0) - ({int_x1}, {h}) = {interviewee.size}")

# Resize each to 720x1280 (Veo 9:16 output size; preserves anchor aspect for direct match).
TARGET = (720, 1280)
reporter_resized = reporter.resize(TARGET, Image.LANCZOS)
interviewee_resized = interviewee.resize(TARGET, Image.LANCZOS)

reporter_resized.save(OUT_DIR / "reporter_solo.png", optimize=True)
interviewee_resized.save(OUT_DIR / "interviewee_solo.png", optimize=True)
print(f"\nSaved:")
print(f"  {OUT_DIR / 'reporter_solo.png'}")
print(f"  {OUT_DIR / 'interviewee_solo.png'}")
