"""
CA JDC Personas — batch 2, 5 new characters
4 Black/African American + 1 Hispanic/Latino
Ages 28-40, 9:16 portrait via useapi.net Google Flow nano-banana-pro
2 personas with direct California sunshine (G, I)
New backgrounds: concrete steps, laundromat exterior, parking lot,
                 apartment courtyard, neighborhood corner fence
"""
import os, requests, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

USEAPI_TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {USEAPI_TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_jdc_personas2")
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "nano-banana-pro"

PERSONAS = [
    # ─── BLACK / AFRICAN AMERICAN ───────────────────────────────────────────
    {
        "id": "G",
        "label": "Black male 31 — outdoor concrete steps (SUNSHINE)",
        "prompt": (
            "RAW phone selfie photo. Man, 31 years old, medium-brown complexion, "
            "short box fade haircut, thin well-trimmed mustache, athletic-lean build. "
            "Standing on outdoor concrete steps, arms relaxed at sides. "
            "Facing directly into the front camera — head-and-shoulders framing, head level. "
            "Heavy, serious gaze directly into the lens. Zero smile, flat neutral mouth.\n\n"
            "SUNSHINE — CRITICAL: Direct afternoon California sun hitting the LEFT side of his face "
            "and shoulder. Warm golden light raking across his features — real sun warmth on brown "
            "skin, not studio-lit. Natural highlight on his left cheek and forehead from direct sun. "
            "Subtle shadow on the right side of his face from the strong directional light. "
            "His skin glows warm in the afternoon light. Squint is subtle — eyes still open and forward.\n\n"
            "BACKGROUND: Outdoor concrete steps of a public park or building entrance — weathered gray "
            "concrete, metal handrail partially visible at the edge. Clear California sky behind him, "
            "warm afternoon haze. No dramatic post-processing — just real outdoor sunlight.\n\n"
            "WARDROBE: Plain white crew-neck t-shirt (warm-tinted in the sun), dark jeans. No jewelry.\n\n"
            "REALISM CRITICAL: Visible pores, natural skin texture, real sun warmth on brown skin. "
            "Sweat sheen from heat. Slight squint from sun brightness — eyes still open. "
            "No beauty filter, no ring light, no studio glow. Slight phone-camera grain. "
            "Looks like he took this himself standing on the steps in afternoon sun.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
    {
        "id": "H",
        "label": "Black male 36 — laundromat exterior",
        "prompt": (
            "RAW phone selfie photo. Man, 36 years old, deep dark-brown complexion, "
            "close-cropped 360 waves haircut (wave pattern visible close to scalp), "
            "full goatee trimmed tight, stocky broad-shouldered build. "
            "Standing outside, arms loosely at sides, one hand in pocket. "
            "Looking directly into the camera — measured, unhurried. "
            "No smile. The expression of a man who thinks before he speaks.\n\n"
            "BACKGROUND: Exterior wall of a neighborhood laundromat — painted white or cream stucco, "
            "slightly worn and faded. Glass window to his side with faded lettering partially visible. "
            "Plastic laundry carts faintly visible through the glass. Overcast diffused daylight — "
            "flat, even, no harsh shadows. Urban residential neighborhood.\n\n"
            "WARDROBE: Plain dark gray crewneck t-shirt, dark wash jeans. Nothing flashy.\n\n"
            "REALISM CRITICAL: Deep visible skin texture on his dark skin — pores enlarged on nose "
            "and forehead, natural sheen on cheeks. Goatee showing individual strands. "
            "No beauty filter, no ring light. Front-camera slight wide-angle distortion. "
            "Phone grain in the flat overcast light. Real guy outside the laundromat selfie.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
    {
        "id": "I",
        "label": "Black male 29 — open parking lot (SUNSHINE)",
        "prompt": (
            "RAW phone selfie photo. Man, 29 years old, warm medium-brown complexion, "
            "low taper fade (very clean lines), clean-shaven, lean build, sharp cheekbones. "
            "Standing upright, arms relaxed at sides. "
            "Cool, direct gaze into the front camera. No smile, neutral expression. "
            "Quiet confidence — the look of someone who has figured something out.\n\n"
            "SUNSHINE — CRITICAL: HARSH direct midday California sun from above and slightly in front. "
            "Strong warm bright light hitting his face and shoulders — real outdoor sun glare. "
            "Top-lit from the midday sun — bright on the crown of his head, forehead, nose, cheekbones. "
            "Deep natural shadow under the brow ridge and jawline from directional overhead light. "
            "His warm-brown skin looks vivid and real in the bright sun. No softening, no fill light.\n\n"
            "BACKGROUND: Open surface parking lot — faded dark asphalt with worn white parking stripe "
            "visible at the bottom of frame. Commercial building facade out of focus in the distance. "
            "Bright washed-out sky from the midday sun. Heat-haze feel.\n\n"
            "WARDROBE: Black sleeveless t-shirt (tank top), dark jeans. Simple, clean.\n\n"
            "REALISM CRITICAL: Natural skin under harsh direct sun — slight forehead sheen from heat, "
            "real skin texture and pores, no smoothing. Eyes slightly squinted from sun brightness "
            "but still open and forward. No beauty filter, no studio light. "
            "Phone grain from front-camera in direct bright light. Authentic outdoor selfie feel.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
    {
        "id": "J",
        "label": "Black male 40 — apartment complex courtyard",
        "prompt": (
            "RAW phone selfie photo. Man, 40 years old, dark-brown complexion, "
            "close-cropped hair with visible salt-and-pepper throughout (especially at the temples), "
            "short full beard with gray hairs mixed in, heavyset solid build, broad frame. "
            "Standing in a courtyard, one hand loosely in his pocket, other arm at side. "
            "Steady, unhurried gaze directly into the camera. "
            "No smile — the gravity of a man with some mileage on him.\n\n"
            "BACKGROUND: Outdoor courtyard of an older apartment complex — concrete walkway, "
            "weathered off-white stucco building wall behind him, metal stair railing visible "
            "at the far edge. Diffused overcast afternoon light — even, no harsh shadows. "
            "Lived-in, worn feel. Not run-down — just real.\n\n"
            "WARDROBE: Dark navy zip-up hoodie open over a plain white t-shirt, dark jeans. "
            "Practical, nothing flashy.\n\n"
            "REALISM CRITICAL: Skin texture showing age — visible pores, slight weathering lines "
            "at the eyes and corners of the mouth. Salt-and-pepper beard strands individually visible. "
            "Under-eye bags. Real lip texture. Subtle facial asymmetry. "
            "No beauty filter, no ring light, no studio glow. Slight wide-angle front-cam distortion. "
            "Phone grain. Looks like he took it himself standing in his building's courtyard.\n\n"
            "9:16 vertical portrait. No on-screen text, no captions, no watermarks."
        ),
    },
    # ─── HISPANIC / LATINO ──────────────────────────────────────────────────
    {
        "id": "K",
        "label": "Hispanic male 33 — neighborhood corner fence",
        "prompt": (
            "RAW phone selfie photo. Man, 33 years old, medium olive-tan skin tone, "
            "dark curly hair (medium length, natural curl pattern, slightly unruly), "
            "5-7 days stubble (fuller on jaw, patchy on cheeks), dark brown eyes, "
            "medium-lean build. Standing with his back against a chain-link or wooden slat fence, "
            "one arm resting loosely on the fence rail, the other at his side. "
            "Direct, quiet gaze into the front camera. No smile, controlled flat expression.\n\n"
            "BACKGROUND: Neighborhood corner — chain-link fence or weathered wooden plank fence "
            "behind him, concrete sidewalk and edge of a residential street visible. "
            "Mature trees partially in frame. Modest California residential neighborhood — "
            "not wealthy, not run-down. Partly cloudy diffused light, no dramatic shadows.\n\n"
            "WARDROBE: Dark olive-green hoodie (hood down), dark jeans. Nothing branded.\n\n"
            "REALISM CRITICAL: Natural skin texture — pores on nose and cheeks, "
            "olive undertone with slight redness at cheeks. Curly hair showing real strand detail, "
            "not smoothed or styled. Stubble with visible individual follicles. "
            "Real eye texture, no retouching. Slight phone-camera grain. "
            "Mild wide-angle front-camera distortion. Looks like a real selfie taken "
            "at a neighborhood corner.\n\n"
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
    print(f"Generating {len(PERSONAS)} CA JDC personas (batch 2) → {OUT}\n")
    print("4 Black/African American + 1 Hispanic/Latino | 2 with sunshine (G, I)\n")

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
