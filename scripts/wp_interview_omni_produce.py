"""OMNI (omni-flash) version of the conversational street interview — 6 two-turn chunks (8s each),
back-and-forth reporter+survivor. Google Flow via useapi, v2_profile two-shot anchor.
Chowchilla = plain spelling + descriptive lock. skip-if-exists.
"""
import sys, pathlib, requests
from googleflow_client import generate_veo

OUT = pathlib.Path("outputs/wp_voxpop/interview_omni"); OUT.mkdir(parents=True, exist_ok=True)
ANCHOR = "outputs/wp_voxpop/twoshot/v2_profile.png"
PRON = ("Chowchilla is said as three English syllables chow (rhymes with cow) + chill + uh, stress "
        "the middle syllable, one fluid word, never Spanish. ")
COMMON = ("Wide 16:9 candid street interview on a sunny sidewalk, static camera. A reporter on the "
          "LEFT (denim jacket, holding a microphone) and a weathered woman on the RIGHT (grey hoodie) "
          "take turns, only one talks at a time while the other listens with mouth closed. Calm, "
          "natural, clean audio, NO music. ")

# each chunk = 2 turns (L then R) unless noted; L=reporter, R=woman
CHUNKS = {
 "o1": [("L","Nearly 500 women from California's prisons are coming forward. You were at Chowchilla. What happened in there?"),
        ("R","The guards crossed the line. Sexually. Nobody would have believed us.")],
 "o2": [("L","A lot of women think that because they never reported it, it is too late."),
        ("R","That is exactly what I thought. I thought it was my fault.")],
 "o3": [("L","But under California law, a woman in prison cannot consent to a guard."),
        ("R","Wait. Even after all these years?")],
 "o4": [("L","You may qualify for significant potential compensation. It is free and confidential."),
        ("R","I never knew that was even possible.")],
 "o5": [("L","You never go to court. If you were at Chowchilla, Valley State, or Folsom, there is a private two-minute form."),
        ("R","So anyone who was in there should check?")],
 "o6": [("L","Yes. Tap below and see if you qualify.")],
}

def prompt_for(turns):
    has_chow = any("Chowchilla" in t for _, t in turns)
    lines = "\n".join(f"{'REPORTER' if s=='L' else 'WOMAN'}: \"{t}\"" for s, t in turns)
    return (COMMON + (PRON if has_chow else "") +
            "English only, follow the exact lines and speaker order, no filler, no extra words. "
            "No on-screen text, no captions.\nSPOKEN DIALOGUE (verbatim, in order):\n" + lines)

def _main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for slug, turns in CHUNKS.items():
        if only and only != slug: continue
        dst = OUT / f"{slug}.mp4"
        if dst.exists(): print(f"[skip] {slug}"); continue
        r = generate_veo(prompt_for(turns), image_path=ANCHOR, duration=8,
                         aspect_ratio="landscape", model="omni-flash")
        if r.get("urls"):
            dst.write_bytes(requests.get(r["urls"][0], timeout=600).content); print(f"[done] {slug}")
        else:
            print(f"[FAIL] {slug}", str(r.get("raw"))[:250])
    print("OMNI PRODUCE DONE")

if __name__ == "__main__":
    _main()
