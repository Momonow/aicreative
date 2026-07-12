"""Eyeline fix: the 3 series-2 survivor reverse-shot anchors were generated facing SCREEN-RIGHT
(same direction as the interviewer -> broken shot-reverse-shot). Re-render each to face SCREEN-LEFT
(opposite the interviewer, matching the Nice One survivor) via gpt-image-2 i2i. Identity held via
input_urls; minimal prompt changes ONLY the look-direction. Overwrites <survivor>.png after backing
up the wrong-way version to <survivor>_rightgaze.png.
"""
import pathlib, shutil, requests
from kie_client import generate_gpt_image, upload_file

REF = pathlib.Path("outputs/wp_series2/reference")
SURV = ["surv1_maria", "surv2_denise", "surv3_kathy"]
PROMPT = ("This exact same woman, same face, same hair, same earrings, same clothing, same courthouse-"
          "steps background. Change ONLY her orientation: she is now turned toward the LEFT edge of "
          "the frame, looking off-camera to the LEFT (screen-left) at an interviewer standing just off "
          "the left side of the frame, mid-conversation, serious and candid. She holds the same small "
          "black podcast microphone (round black foam ball, tiny blue LED) near her mouth, the mic "
          "toward the left. Photoreal candid documentary photo, natural skin, no retouching, no filter. "
          "Waist-up vertical 9:16 framing.")

def main():
    for s in SURV:
        src = REF / f"{s}.png"
        bak = REF / f"{s}_rightgaze.png"
        if not bak.exists(): shutil.copy(src, bak)          # preserve the wrong-way original once
        url = upload_file(str(bak))
        r = generate_gpt_image(PROMPT, image_urls=[url], aspect_ratio="9:16", resolution="2K",
                               input_fidelity="high")
        if r.get("status") == "success" and r.get("urls"):
            src.write_bytes(requests.get(r["urls"][0], timeout=120).content); print(f"[done] {s} -> screen-left")
        else:
            print(f"[FAIL] {s}", str(r.get("raw"))[:160])
    print("EYELINE FIX DONE")

if __name__ == "__main__":
    main()
