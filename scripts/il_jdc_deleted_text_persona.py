"""
IL JDC 'Deleted Text' — persona generation
Heavy-set man, late 30s, medium-dark brown skin, green army jacket / black hoodie,
Chicago sidewalk. Matching the user-provided reference photo.
useapi.net nano-banana-pro | 9:16
"""
import os, requests
from pathlib import Path

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/il_jdc_deleted_text")
OUT.mkdir(parents=True, exist_ok=True)

REALISM = (
    "Photoreal candid documentary photo. NOT a glamour or fashion shoot. "
    "Ordinary real man — natural skin with visible pores, slight skin shine, "
    "no beauty retouching, no filter, no studio lighting. "
    "9:16 vertical, photo-realistic."
)

PROMPT = (
    "UGC phone selfie, 9:16 vertical portrait. "
    "Phone held at arm's length, slightly below eye level — "
    "standing on a Chicago sidewalk against a brick building wall. "
    "Looking directly into the camera with a serious, guarded expression. Candid, real.\n\n"

    "Man in his late 30s. Medium-dark warm brown skin tone — deep rich brown complexion, "
    "NOT light, NOT very dark, a true medium-dark brown. "
    "Heavy stocky build — broad shoulders, thick neck, full face. "
    "FACE: round broad face, heavy jaw, slightly prominent cheekbones, deep-set dark brown eyes. "
    "NO smile. Mouth in a flat neutral line. Expression is tired, guarded, serious — "
    "the look of someone who has been through a lot and doesn't show it easily. "
    "Slight under-eye heaviness. "
    "HAIR: very short natural coily hair, low fade on the sides, minimal length on top — "
    "natural 4A/4B texture, dark black, not styled. "
    "BEARD: short scruffy sparse beard — dark stubble to short beard, not full, "
    "coverage uneven, patches on cheeks, fuller on chin and jaw. "
    "TATTOOS: cursive script tattoos on the right hand and fingers — dark black ink, "
    "multiple words in flowing cursive, visible on the hand and wrist area. "
    "BODY: arms crossed loosely at waist or hanging. "
    "CLOTHING: olive green army field jacket worn open — "
    "has chest button pockets, shoulder epaulettes, slightly worn/faded military-style fabric. "
    "Underneath: black pullover hoodie with a visible drawstring at the neckline. "
    "No other layers visible.\n\n"

    "SETTING: Chicago urban sidewalk, daytime. "
    "Brick building wall close on his left side — red/brown brick, weathered. "
    "Behind him: a Chicago urban street — another brick building across the street, "
    "parked cars in the far background, grey overcast sky. "
    "Flat cold overcast daylight — no direct sun, no harsh shadows. "
    "The street reads as a Chicago South/West side neighborhood block.\n\n"

    + REALISM
)


def generate():
    out_path = OUT / "persona.jpg"
    if out_path.exists() and out_path.stat().st_size > 50_000:
        print(f"  persona: exists ({out_path.stat().st_size // 1024}KB), skipping")
        return str(out_path)

    payload = {
        "prompt": PROMPT,
        "model": "nano-banana-pro",
        "aspectRatio": "9:16",
    }
    r = requests.post(
        "https://api.useapi.net/v1/google-flow/images",
        headers=HEADERS, json=payload, timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"persona: {r.status_code} {r.text[:300]}")

    data = r.json()
    media = data.get("media", [])
    if not media:
        raise RuntimeError(f"no media — {data}")

    import shutil
    saved = []
    for i, m in enumerate(media):
        g = m.get("image", {}).get("generatedImage", {})
        url = g.get("fifeUrl", "")
        if not url:
            continue
        vpath = OUT / f"persona_v{i+1}.jpg"
        img_r = requests.get(url, timeout=60)
        img_r.raise_for_status()
        vpath.write_bytes(img_r.content)
        saved.append(vpath)
        print(f"  persona_v{i+1}: saved {vpath.stat().st_size // 1024}KB")

    if saved:
        shutil.copy(saved[0], out_path)
        print(f"  persona: → {out_path}")

    return str(out_path)


if __name__ == "__main__":
    print("IL JDC Deleted Text — persona generation (nano-banana-pro)\n")
    path = generate()
    print(f"\nDone → {path}")
    print("\nNOTE: If you want to use the exact uploaded reference image instead,")
    print(f"replace {out_path} with your file before running the gen script.")
