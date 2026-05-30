"""
CA JDC Personas — batch 3, 3 characters
3 Black / dark-skin-tone males
Ages 27-40 | Close-up documentary portrait (NOT selfie)
9:16 portrait via useapi.net Google Flow nano-banana-pro
"""
import os, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

USEAPI_TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {USEAPI_TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_jdc_personas3")
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "nano-banana-pro"

PERSONAS = [
    {
        "id": "L",
        "label": "male 33 — outdoor brick wall, afternoon shade",
        "prompt": (
            "Close-up documentary portrait photograph, NOT a selfie. Camera on a tripod or "
            "held by another person at eye level — natural perspective, no wide-angle selfie distortion. "
            "Man, 33 years old, medium-dark brown skin tone, short low taper fade haircut (clean lines), "
            "thin mustache and short chin beard (3-4 day growth), lean-athletic build visible in shoulders. "
            "Tight close-up framing — face and upper chest fill the frame, chin near the bottom, "
            "crown of head near the top. Head slightly turned 3/4 toward the lens, eyes locked directly "
            "forward into the camera. Heavy controlled gaze. ZERO smile, mouth flat and neutral.\n\n"
            "BACKGROUND: Exterior brick wall — worn red-brown brick, slightly out of focus. "
            "Afternoon shade, diffused warm-cool light. Urban residential block. "
            "No sky visible, wall fills the background entirely.\n\n"
            "WARDROBE: Plain dark navy t-shirt, collar at the very bottom of frame.\n\n"
            "LIGHTING: Natural diffused shade light — soft shadows on his face, no harsh bright spots, "
            "no ring light, no studio fill. Real outdoor ambient light.\n\n"
            "REALISM CRITICAL: Visible pores and skin texture on dark-brown skin. "
            "Natural sebum sheen on forehead and nose. Individual beard follicles. "
            "Real eye texture, whites slightly warm. Subtle facial asymmetry. "
            "No beauty filter, no retouching, no skin smoothing. Grain from real camera sensor. "
            "Looks like a candid close-up documentary portrait.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
    {
        "id": "M",
        "label": "male 27 — indoor window light",
        "prompt": (
            "Close-up documentary portrait photograph, NOT a selfie. Camera positioned at eye level "
            "by another person or on a tripod — no front-cam wide-angle distortion. "
            "Man, 27 years old, warm medium-brown skin tone, short natural twists (small coils, "
            "1-2 inches long, even density), clean-shaven smooth face, sharp defined jawline, "
            "high cheekbones, lean build. "
            "Tight close-up — face fills majority of the frame from chin to crown. "
            "Face angled slightly toward the camera, direct eye contact, intense focused gaze. "
            "No smile. Serious, determined expression. Mouth closed, jaw slightly set.\n\n"
            "BACKGROUND: Indoors near a window — soft side-light from a window to his left "
            "creates a gentle gradient from light left side to darker right side of his face. "
            "Background is a soft dark-blur (interior wall, out of focus). "
            "Intimate, natural indoor lighting.\n\n"
            "WARDROBE: Black hoodie, edge of collar at the bottom of frame.\n\n"
            "LIGHTING: Natural window light — single-source, slightly warm late-afternoon quality. "
            "Soft shadow along the right side of his face. No ring light, no flash, no studio lights.\n\n"
            "REALISM CRITICAL: Skin texture catching the window light — pores visible, natural "
            "moisture on the lit cheekbone. Individual twist strands defined. "
            "Subtle eye redness at the inner corners. Real lip texture. "
            "No beauty filter, no smoothing. Film-grain quality. "
            "Feels like a real documentary portrait from a journalist or filmmaker.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
    {
        "id": "N",
        "label": "male 38 — outdoor alley/side street, overcast",
        "prompt": (
            "Close-up documentary portrait photograph, NOT a selfie. Camera on a tripod or "
            "hand-held by a second person at subject's eye level — standard lens perspective, "
            "no selfie distortion. "
            "Man, 38 years old, deep dark-brown skin tone (rich dark complexion), "
            "close-cropped hair (1/4 inch uniform fade, shape-up clean edges), "
            "full short beard (evenly trimmed, covering jaw and chin), broad forehead, "
            "deep-set dark eyes, heavyset solid build visible in the shoulders and neck. "
            "Tight close-up — face and top of chest fill the frame. "
            "Facing almost directly at the camera, slight chin-down tilt, eyes up and locked on lens. "
            "No smile. The measured, quiet expression of someone who's been through something.\n\n"
            "BACKGROUND: Side street or alley — out-of-focus concrete or stucco wall behind him, "
            "slightly weathered. Overcast California day — flat even gray light, "
            "no directional shadows, subdued tones. Urban, utilitarian.\n\n"
            "WARDROBE: Dark charcoal gray zip-up jacket (collar at bottom of frame).\n\n"
            "LIGHTING: Flat overcast daylight — even, diffused, no harsh shadows. "
            "His dark skin tones are rich and deep in the flat light. "
            "No ring light, no flash, no artificial fill.\n\n"
            "REALISM CRITICAL: Deep-skin texture in flat light — pores and skin sheen on forehead "
            "and nose, natural lip texture, whites of the eyes with real subtle vein detail. "
            "Individual beard hairs visible. Slight shadow under brow ridge. "
            "No beauty filter, no retouching. Real sensor grain. "
            "Candid close-up documentary feel — not a posed commercial headshot.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
]


def generate_persona(p):
    pid = p["id"]
    out_dir = OUT / f"persona_{pid}"
    out_dir.mkdir(exist_ok=True)

    payload = {"prompt": p["prompt"], "model": MODEL, "aspectRatio": "9:16"}
    print(f"  Persona {pid} ({p['label']}): submitting …", flush=True)

    r = requests.post(
        "https://api.useapi.net/v1/google-flow/images",
        headers=HEADERS, json=payload, timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Persona {pid}: HTTP {r.status_code} — {r.text[:300]}")

    data = r.json()
    media_list = data.get("media", [])
    if not media_list:
        raise RuntimeError(f"Persona {pid}: no media in response — {data}")

    saved = []
    for i, m in enumerate(media_list):
        fife_url = m.get("image", {}).get("generatedImage", {}).get("fifeUrl", "")
        media_id = m.get("image", {}).get("generatedImage", {}).get("mediaGenerationId", "")
        if not fife_url:
            continue
        out_path = out_dir / f"v{i+1}.jpg"
        r2 = requests.get(fife_url, timeout=60)
        r2.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(r2.content)
        if media_id:
            (out_dir / f"v{i+1}_mediaId.txt").write_text(media_id)
        saved.append((out_path, media_id))
        print(f"    Persona {pid} v{i+1}: {out_path.stat().st_size//1024}KB saved")

    print(f"  ✓ Persona {pid}: {len(saved)} image(s) → {out_dir}")
    return pid, saved


if __name__ == "__main__":
    print(f"Generating {len(PERSONAS)} CA JDC personas (batch 3) → {OUT}\n")
    print("3 close-up documentary portraits | NOT selfie mode\n")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(generate_persona, p): p["id"] for p in PERSONAS}
        for fut in as_completed(futs):
            pid = futs[fut]
            try:
                pid, saved = fut.result()
                results[pid] = saved
                print(f"✓ Persona {pid} complete")
            except Exception as e:
                print(f"✗ Persona {pid} ERROR: {e}")

    print(f"\n{'='*50}")
    print(f"Completed: {len(results)}/{len(PERSONAS)} personas")
    for pid in sorted(results):
        for path, mid in results[pid]:
            print(f"  {pid} → {path}")
