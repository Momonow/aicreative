"""Re-crop the wide L-tracks shot into head/shoulders single-character anchors —
WITHOUT showing the microphone. User flagged mic-hold rendering as visually odd.

For both reporter and interviewee, crop tight enough that the mic isn't in
frame. Each clip is then purely a documentary-style intimate close-up — no
mic prop needed to read as "news interview" since the wardrobe + framing
+ off-camera-listener gaze convey the format.

Source: outputs/illinois_jdc_news_eltracks/wide/wide_shot.png (1536x1024)

Output:
  outputs/illinois_jdc_news_eltracks/wide/reporter_nomic.png  (720x1280)
  outputs/illinois_jdc_news_eltracks/wide/interviewee_nomic.png (720x1280)
"""
from pathlib import Path
from PIL import Image

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/wide")
src = OUT_DIR / "wide_shot.png"

img = Image.open(src)
w, h = img.size
print(f"Source: {w}x{h}")

# Reporter — tight crop above the mic level. Mic is at ~y=600 in the 1024-tall
# wide shot. Crop height should be ~570 to keep face/shoulders but exclude
# the mic hand at the bottom.
# 9:16 portrait — crop_w / crop_h = 9/16. For crop_h = 570 → crop_w = 320.
# That's too narrow. Try crop_h = 800 (still cuts above mic) → crop_w = 450.
# Better: crop_h = 720 → crop_w = 405. Centered on reporter face at x≈280.
rep_crop_h = 720
rep_crop_w = int(rep_crop_h * 9 / 16)  # = 405
rep_face_x = 280
rep_x0 = max(0, rep_face_x - rep_crop_w // 2)
rep_x1 = rep_x0 + rep_crop_w
rep_y0 = 0
rep_y1 = rep_crop_h
reporter = img.crop((rep_x0, rep_y0, rep_x1, rep_y1))
print(f"Reporter crop (head/shoulders, no mic): ({rep_x0}, {rep_y0}) - ({rep_x1}, {rep_y1}) = {reporter.size}")

# Interviewee — tight crop above mic level. Interviewee face at x≈1198.
int_crop_h = 720
int_crop_w = int(int_crop_h * 9 / 16)  # = 405
int_face_x = 1198
int_x0 = int_face_x - int_crop_w // 2  # = 996
int_x1 = int_x0 + int_crop_w
int_y0 = 0
int_y1 = int_crop_h
interviewee = img.crop((int_x0, int_y0, int_x1, int_y1))
print(f"Interviewee crop (head/shoulders, no mic): ({int_x0}, {int_y0}) - ({int_x1}, {int_y1}) = {interviewee.size}")

# Resize each to 720x1280 (Veo 9:16 output size)
TARGET = (720, 1280)
reporter_resized = reporter.resize(TARGET, Image.LANCZOS)
interviewee_resized = interviewee.resize(TARGET, Image.LANCZOS)

reporter_resized.save(OUT_DIR / "reporter_nomic.png", optimize=True)
interviewee_resized.save(OUT_DIR / "interviewee_nomic.png", optimize=True)
print(f"\nSaved:")
print(f"  {OUT_DIR / 'reporter_nomic.png'}")
print(f"  {OUT_DIR / 'interviewee_nomic.png'}")
