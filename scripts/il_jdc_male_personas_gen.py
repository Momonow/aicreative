"""
IL JDC — 5 Black Male Personas | useapi.net nano-banana-pro | 9:16
"""
import os, requests, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/jdc_personas_male")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_M1",
        "label": "Inside - Living Room - Close-up",
        "prompt": (
            "Portrait photograph of a 33-year-old Black American man, close-up shot framing "
            "from chest to top of head, seated on a worn fabric couch in a lived-in living room. "
            "Low fade haircut, very light stubble, direct calm gaze straight into the lens. "
            "Wearing a plain dark crew-neck t-shirt. Warm lamp light from behind left, "
            "soft natural shadows on face. Visible pores, slight under-eye shadow, "
            "faint fine lines, natural skin texture, slight lip dryness, no filter, "
            "no retouching, no beauty mode, no skin smoothing. "
            "Real residential living room background slightly out of focus — couch cushions, "
            "side table, soft lamp glow. Looks like a real person's home, not a set. "
            "9:16 vertical portrait, photo-realistic, shot on a phone front camera."
        ),
    },
    {
        "id": "persona_M2",
        "label": "Inside - Kitchen - Medium Close-up - Longer Beard",
        "prompt": (
            "Portrait photograph of a 37-year-old Black American man, medium close-up shot "
            "framing from mid-torso to top of head, standing near a kitchen counter. "
            "Short taper fade haircut, FULL LONGER BEARD approximately 2 to 3 inches, "
            "well-kept but natural, slight wave to the beard. Direct steady gaze into the lens. "
            "Wearing a dark grey henley shirt. Natural window light from the left side, "
            "kitchen tiles and cabinets slightly out of focus in background. "
            "Visible pores, natural skin texture, slight under-eye shadow, "
            "no filter, no retouching, no beauty mode, no skin smoothing. "
            "Real residential kitchen background — counter edge, cabinet handles faintly visible. "
            "Looks like a genuine candid photograph taken in someone's kitchen. "
            "9:16 vertical portrait, photo-realistic, shot on a phone front camera."
        ),
    },
    {
        "id": "persona_M3",
        "label": "Inside - Bedroom - Close-up",
        "prompt": (
            "Portrait photograph of a 32-year-old Black American man, close-up shot framing "
            "from shoulders to top of head, sitting on the edge of a bed, back against the wall. "
            "Very low cut Caesar fade, completely clean shaven, calm neutral expression, "
            "eyes directly into the lens. Wearing a white or light grey t-shirt. "
            "Soft ambient bedroom lighting, slightly warm, bed headboard or wall visible behind. "
            "Visible pores, natural skin texture, faint under-eye darkness, "
            "no filter, no retouching, no beauty mode. "
            "Real residential bedroom feel — rumpled bedsheet edge, simple wall. "
            "9:16 vertical portrait, photo-realistic, shot on a phone front camera."
        ),
    },
    {
        "id": "persona_M4",
        "label": "Inside - Basement / Den - Medium Close-up",
        "prompt": (
            "Portrait photograph of a 36-year-old Black American man, medium close-up shot "
            "framing from mid-chest to top of head, standing in a home basement or den. "
            "Short box fade haircut, neatly trimmed short beard about half an inch, "
            "calm serious expression, direct eye contact into the lens. "
            "Wearing a dark navy or black hoodie. Dim interior lighting, "
            "slightly cool-toned, concrete block wall or paneling faintly visible in background. "
            "Visible pores, natural skin texture, slight stubble texture, "
            "no filter, no retouching, no beauty mode, no skin smoothing. "
            "Background slightly out of focus — looks like a real unfinished basement or spare room. "
            "9:16 vertical portrait, photo-realistic, shot on a phone front camera."
        ),
    },
    {
        "id": "persona_M5",
        "label": "Outside - Front Steps / Brick Wall - Close-up",
        "prompt": (
            "Portrait photograph of a 34-year-old Black American man, close-up shot framing "
            "from chest to top of head, standing outside on front steps or beside a brick wall "
            "of a residential building. Short clean fade haircut, light stubble, "
            "relaxed neutral expression, eyes directly into the lens. "
            "Wearing a dark zip-up or plain jacket. Natural daylight, slightly overcast, "
            "even soft outdoor light on face. "
            "Visible pores, natural skin texture, slight under-eye shadow, "
            "no filter, no retouching, no beauty mode. "
            "Background slightly out of focus — faded brick wall, concrete steps, "
            "residential neighborhood feel. Looks like a real outdoor phone selfie. "
            "9:16 vertical portrait, photo-realistic, shot on a phone front camera."
        ),
    },
]


def generate(p):
    pid = p["id"]
    out_path = OUT / f"{pid}.jpg"
    if out_path.exists() and out_path.stat().st_size > 50_000:
        print(f"  {pid}: exists ({out_path.stat().st_size//1024}KB), skipping")
        return pid, str(out_path), None

    payload = {
        "prompt": p["prompt"],
        "model": "nano-banana-pro",
        "aspectRatio": "9:16",
    }
    r = requests.post(
        "https://api.useapi.net/v1/google-flow/images",
        headers=HEADERS, json=payload, timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"{pid}: {r.status_code} {r.text[:300]}")

    data = r.json()
    media = data.get("media", [])
    if not media:
        raise RuntimeError(f"{pid}: no media in response — {data}")

    # response nests image data under media[i]["image"]["generatedImage"]
    gen = media[0].get("image", {}).get("generatedImage", {})
    fife_url = gen.get("fifeUrl", "")
    media_id = gen.get("mediaGenerationId", "")

    if not fife_url:
        raise RuntimeError(f"{pid}: no fifeUrl — {gen}")

    # save all variants
    for i, m in enumerate(media):
        g = m.get("image", {}).get("generatedImage", {})
        url = g.get("fifeUrl", "")
        mid = g.get("mediaGenerationId", "")
        if not url:
            continue
        vpath = OUT / f"{pid}_v{i+1}.jpg"
        img_r = requests.get(url, timeout=60)
        img_r.raise_for_status()
        vpath.write_bytes(img_r.content)
        print(f"  {pid}_v{i+1}: saved {vpath.stat().st_size//1024}KB  mediaId: {mid}")

    # primary = v1
    import shutil
    shutil.copy(OUT / f"{pid}_v1.jpg", out_path)
    print(f"✓ {pid}: {out_path}  [{p['label']}]")
    return pid, str(out_path), media_id


if __name__ == "__main__":
    print(f"Generating 5 Black male personas (nano-banana-pro) → {OUT}\n")
    results = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(generate, p): p["id"] for p in PERSONAS}
        for fut in as_completed(futs):
            pid = futs[fut]
            try:
                pid, path, media_id = fut.result()
                results[pid] = {"path": path, "media_id": media_id}
                print(f"✓ {pid}")
            except Exception as e:
                print(f"✗ {pid} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/5")
    for pid, info in sorted(results.items()):
        print(f"  {pid}: {info['path']}")
        if info["media_id"]:
            print(f"    mediaId: {info['media_id']}")
