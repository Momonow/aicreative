#!/usr/bin/env python3
"""More Depo interview b-roll stills (documentary-real, text-free, 9:16) to cut in under the
answer beats. t2i via gpt-image-2. Skip-if-exists.
Run: .venv/bin/python scripts/depo_broll_more_stills.py [--only a,b]
"""
import sys, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie

OUT = Path("outputs/depo_interview/broll"); OUT.mkdir(parents=True, exist_ok=True)
DOC = ("Photoreal news b-roll / documentary cinematography (Frontline / PBS Newshour look), "
       "natural real-world lighting, slight grain, NOT cinematic, NOT stylized. "
       "ABSOLUTELY no on-screen text, no captions, no labels, no logos, no readable words.")

STILLS = [
 ("study_pages",
  "Close-up of a woman's hands flipping through a thick printed medical research journal on a "
  "wooden desk, a yellow highlighter marking a paragraph of blurred body text, reading glasses "
  "beside it. The text is out of focus and unreadable. " + DOC),
 ("depo_vial",
  "A clinical exam-room tray holding a small contraceptive injection vial and a prepared syringe, "
  "a clinician's blue-gloved hands drawing up the shot. Close product-level documentary framing, "
  "clean clinic light. " + DOC),
 ("depo_injection",
  "A nurse in scrubs giving an intramuscular injection into the upper arm of a seated woman "
  "patient, the patient's sleeve rolled up, in a clinic exam room. Documentary middle framing, "
  "faces partly out of the top of frame. " + DOC),
 ("women_group",
  "A quiet candid documentary shot of several diverse women in their thirties to sixties sitting "
  "in a support-group circle in a community room, listening, soft natural window light. Middle "
  "framing, not posed. " + DOC),
 ("legal_docs",
  "Close-up of a stack of manila legal case-file folders and court documents on an attorney's "
  "desk, a fountain pen resting on top, a blurred shelf of law books behind. All paper text is "
  "out of focus and unreadable. " + DOC),
 ("phone_form",
  "A woman's hands holding a smartphone that shows a simple blank online form: a few empty input "
  "fields and one button, her thumb about to tap. The screen shows only generic empty fields with "
  "no readable words. Documentary close-up, real indoor light. " + DOC),
 ("lawyer_review",
  "A woman attorney in a warm office reviewing an open document folder at her desk, reading "
  "glasses on, soft daylight from a window, a bookshelf behind her. Documentary middle framing, "
  "calm and reassuring. " + DOC),
]

def gen(name, prompt):
    out = OUT / f"broll_{name}.png"
    if out.exists(): print("skip", name); return
    res = kie.generate_gpt_image(prompt, aspect_ratio="9:16", resolution="2K")
    if res.get("status") == "success" and res.get("urls"):
        kie.download(res["urls"][0], out); print("done", name)
    else: print("FAIL", name, str(res.get("raw"))[:180])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="")
    a = ap.parse_args()
    items = STILLS if not a.only else [s for s in STILLS if s[0] in set(a.only.split(","))]
    for s in items: gen(*s)
    print("ALL DONE")

if __name__ == "__main__":
    main()
