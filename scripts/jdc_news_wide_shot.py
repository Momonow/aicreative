"""Generate ONE wide L-tracks shot (1536x1024 landscape, gpt-image-2 max-size)
showing BOTH characters in their established positions.

Then crop into 2 portrait shots, one per character, for use as Veo single-
character anchors. Each clip will show ONE character only — eliminating the
two-character-confusion problems we hit before (voice attribution, face
drift, interviewee-mouth-might-open during reporter dialogue).

Pipeline:
  1. Generate wide shot via gpt-image-2 (1536x1024 landscape, high quality)
  2. Crop reporter portion (left) → reporter_solo.png (1024x1536-ish portrait)
  3. Crop interviewee portion (right) → interviewee_solo.png
  4. Upload both to KIE for use as anchor refs

Output:
  outputs/illinois_jdc_news_eltracks/wide/wide_shot.png      (gpt-image full)
  outputs/illinois_jdc_news_eltracks/wide/reporter_solo.png  (left crop)
  outputs/illinois_jdc_news_eltracks/wide/interviewee_solo.png (right crop)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/wide")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT = """\
Photoreal wide news-b-roll two-shot photograph, real daylight under the Chicago
Loop elevated train tracks ('the L'). Massive black-painted riveted steel
girders and lattice beams overhead form a structural ceiling. Large riveted
black steel support columns rise from a polished brick-and-concrete sidewalk.
Older granite-clad and red-brick Loop-era buildings line the far side of a
downtown street in the soft-focus deep background, faint yellow Chicago taxi
visible at the curb. Late-afternoon overcast daylight, cool urban palette,
subtle pattern shadows on the ground from the steel structure above.

TWO MEN STANDING IN FRAME, ~5 feet apart, both framed mid-chest up, eye-level
two-shot composition.

LEFT side of frame — INTERVIEWER (OLDER REPORTER):
Man, medium-dark skin tone, late 30s. Close-cropped short black hair, full
neatly trimmed short beard, clean jawline. Wearing an unbuttoned black wool
overcoat over a charcoal-grey blazer and a crisp white open-collar
button-down shirt. STRONG LEFT-PROFILE to camera — viewer sees the back of
his head, ear, cheekbone, jaw, beard. His RIGHT hand holds a classic black
handheld stick microphone with a thick black foam windscreen and a
COMPLETELY BLANK WHITE square mic-flag (NO text, NO letters, NO logo, NO
symbols). The mic is extended forward at chest height, head pointed toward
the younger man. He is slightly leaning forward, professional, calm,
attentive — listening posture.

RIGHT side of frame — INTERVIEWEE (YOUNGER MAN):
Younger man, medium-dark skin tone, mid 20s. Short freeform twists with a
high temple-fade taper on the sides. Small gold stud earring in his LEFT
ear. Faint chin-strap goatee, light mustache stubble. Wearing a tan-camel
corduroy trucker jacket with a cream sherpa-collar lining over a
charcoal-grey zip hoodie, top hoodie zip-pull visible at chest. Body angled
3/4 toward camera (face clearly visible). Hands relaxed at his sides. He
looks slightly off-camera-left (toward the reporter), neutral expression,
mouth in a soft closed line.

Photoreal documentary handheld feel — NOT studio, NOT cinematic, NOT
polished broadcast. Visible pores, fine lines, slight skin texture
asymmetry on both faces. No makeup, no beauty mode, no retouching, no
filter. Shot on a small ENG news camera, slight shallow depth-of-field,
both subjects sharp, background softly blurred.

NO on-screen text, NO captions, NO chyrons, NO lower-thirds, NO station
logo, NO watermarks. The WHITE mic-flag stays COMPLETELY BLANK.
"""


def main():
    out = OUT_DIR / "wide_shot.png"
    print(f"Generating wide shot via gpt-image-2 (1536x1024 high quality)...", flush=True)
    print(f"Prompt length: {len(PROMPT)} chars", flush=True)
    r = generate_image(
        prompt=PROMPT,
        out_path=str(out),
        size="1536x1024",
        quality="high",
        n=1,
    )
    if r["status"] != "success":
        print(f"FAILED: {r['raw'].get('error', 'unknown')}", flush=True)
        return
    print(f"DONE → {out}", flush=True)


if __name__ == "__main__":
    main()
