"""
IL JDC Variation 5 — Persona Set C
2 personas, 1 image each. Chicago residential street background (matching
persona_J_forward_v1.jpg). Close-up, facing straight to camera, hyper-realistic.
nano-banana-pro via useapi.net Google Flow.
"""
import os, requests
from pathlib import Path

USEAPI_TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {USEAPI_TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/il_jdc_v5_personas_b")
OUT.mkdir(exist_ok=True)

MODEL = "nano-banana-pro"

PERSONAS = [
    {
        "id": "K",
        "setting": "chicago_street_closeup",
        "prompt": """RAW phone selfie photo. Man, medium dark-brown complexion, mid-30s, medium build, very short low-cut natural fade, thin patchy beard stubble on chin and jaw — not fully grown, natural growth pattern. Facing directly into the front camera. Framing is close — head and shoulders, chest just visible at bottom. Chicago suburban residential street behind him: brick ranch-style houses, a dark parked sedan at the curb, bare winter trees, dry dead leaves scattered on the concrete sidewalk, flat grey overcast sky. No sun, diffused cold afternoon light.

Dark grey zip-up hoodie partially zipped. Hands not in frame. Squared directly to camera, no tilt, looking directly into the lens with a still, heavy expression — the face of someone who keeps things to himself.

REALISM CRITICAL — this must look like a real person's phone photo:
Visible skin pores on the nose, cheeks, and forehead. Natural under-eye darkness. Slight uneven skin tone. Acne scar or two on the cheek. Fine lines at the corners of his eyes. Natural lip texture — slightly dry. Subtle natural asymmetry in his face. Faint stubble shine on the jaw.
Front-facing camera slight wide-angle distortion. Slightly noisy image from phone sensor. NOT smooth, NOT retouched, NOT studio-lit. Looks like he took this standing on the sidewalk, phone at arm's length.
9:16 vertical portrait.""",
    },
    {
        "id": "L",
        "setting": "chicago_street_closeup",
        "prompt": """RAW phone selfie photo. Man, deep warm dark-brown complexion, late 30s (38 years old), stocky build, short natural hair with a clean taper fade, full short beard — well-shaped but natural, visible grey hairs mixed in at the chin and jaw. Facing directly into the front camera, body straight on, no turn. Close framing — face and upper chest, cropped just below the collar. Chicago suburban residential street setting behind him: brick ranch-style houses, a parked sedan, bare trees with no leaves, autumn leaves on the ground and sidewalk, flat grey overcast sky. Cold flat afternoon light, no shadows.

Heather dark-grey crewneck sweatshirt. Arms at sides, not visible. Direct gaze into lens — calm, direct, unmoved. The expression of a man choosing carefully what to say.

REALISM CRITICAL — must look like a real human photographed on a real phone:
Deep visible skin texture — pores enlarged slightly on nose and cheeks, slight sheen on forehead. Natural beard showing individual hair strands, slight grey at chin. Bags under the eyes, natural redness in the whites of the eyes. Fine weathering lines at the eye corners and between the brows. Real lip color with slight dryness. Visible ear texture. Slight facial asymmetry.
Front-facing camera mild wide-angle barrel distortion. Slight image grain from phone sensor in low light. No studio lighting, no ring light catch in eyes, no beauty filter, no skin smoothing. Looks like a real guy took a selfie outside on a grey day.
9:16 vertical portrait.""",
    },
]


def generate_persona(p):
    out_path = OUT / f"persona_{p['id']}_{p['setting']}.jpg"
    if out_path.exists() and out_path.stat().st_size > 50_000:
        print(f"  Persona {p['id']}: already exists, skipping")
        return p["id"], str(out_path)

    payload = {"prompt": p["prompt"], "model": MODEL, "aspectRatio": "9:16"}
    print(f"  Persona {p['id']}: submitting …", flush=True)
    r = requests.post(
        "https://api.useapi.net/v1/google-flow/images",
        headers=HEADERS, json=payload, timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Persona {p['id']} failed: {r.status_code} {r.text[:300]}")

    data = r.json()
    media_list = data.get("media", [])
    if not media_list:
        raise RuntimeError(f"Persona {p['id']}: no media in response")

    m = media_list[0]
    fife_url = m.get("image", {}).get("generatedImage", {}).get("fifeUrl", "")
    media_id = m.get("image", {}).get("generatedImage", {}).get("mediaGenerationId", "")
    if not fife_url:
        raise RuntimeError(f"Persona {p['id']}: no fifeUrl")

    r2 = requests.get(fife_url, timeout=60)
    r2.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r2.content)
    (OUT / f"persona_{p['id']}_{p['setting']}_mediaId.txt").write_text(media_id)
    print(f"  Persona {p['id']}: saved → {out_path.name} ({out_path.stat().st_size//1024}KB)")
    return p["id"], str(out_path)


if __name__ == "__main__":
    print(f"Generating {len(PERSONAS)} personas → {OUT}\n")
    results = {}
    for p in PERSONAS:
        try:
            pid, path = generate_persona(p)
            results[pid] = path
        except Exception as e:
            print(f"✗ Persona {p['id']} ERROR: {e}")
    print(f"\nCompleted: {len(results)}/{len(PERSONAS)}")
    for pid in sorted(results):
        print(f"  Persona {pid}: {results[pid]}")
