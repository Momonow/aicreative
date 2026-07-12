"""Regenerate the 'Nice One' closer anchor with a LOCKED-ON-LENS gaze via gpt-image-2 i2i.
Gaze/angle is baked into the anchor (Veo can't swing it in-motion), so we make a fresh
front-facing, eyes-on-lens version of the survivor closer — identity held via input_urls,
minimal prompt describing only the pose/gaze change. Writes survivor_cam_lock.png.
"""
import pathlib, requests
from kie_client import generate_gpt_image, upload_file

REF = "outputs/wp_interview2/reference/survivor_cam_b.png"   # identity + mic + background source
OUT = pathlib.Path("outputs/wp_interview2/reference/survivor_cam_lock.png")

PROMPT = ("This exact same woman, same face, same short greying hair, same gold hoop earrings, same "
          "black top under the grey cardigan, same courthouse-steps background. She now faces the "
          "camera straight on, squared to the lens, and BOTH eyes are locked DIRECTLY on the camera "
          "lens — looking right down the barrel of the lens at the viewer, not to either side, not "
          "down. She holds the small black podcast microphone in her own hand near her mouth as if "
          "speaking to camera. Photoreal candid documentary photo, natural skin, no retouching, no "
          "filter. Waist-up vertical 9:16 framing.")

def main():
    url = upload_file(REF)
    r = generate_gpt_image(PROMPT, image_urls=[url], aspect_ratio="9:16", resolution="2K",
                           input_fidelity="high")
    if r.get("status") == "success" and r.get("urls"):
        OUT.write_bytes(requests.get(r["urls"][0], timeout=120).content)
        print(f"[done] {OUT}")
    else:
        print("[FAIL]", str(r.get("raw"))[:200])

if __name__ == "__main__":
    main()
