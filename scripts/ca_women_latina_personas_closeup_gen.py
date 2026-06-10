"""
CA Women's Prison — 4 Latina Survivor Personas (ages 42–50) — CLOSE-UP
2 outdoor + 2 indoor | unique California working-class settings
useapi.net nano-banana-2 | 9:16 | extreme close-up face | realism tail baked in
"""
import os, requests, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_women_latina_personas_closeup")
OUT.mkdir(parents=True, exist_ok=True)

REAL = (
    "Photoreal candid documentary phone portrait, NOT a glamour or fashion shoot, "
    "NOT a celebrity portrait — an ordinary, everyday, hard-lived woman with plain average features. "
    "Weathered real skin with visible pores, sun damage, fine lines and wrinkles, under-eye darkness, "
    "no makeup or minimal, no filter, no retouching, no beauty mode, no skin smoothing. "
    "Tired but steady eyes carrying weight. Practical un-styled hair with grown-out color and grey roots. "
    "Plain worn clothing. 9:16 vertical portrait, photo-realistic."
)

PERSONAS = [
    {
        "id": "persona_CWL2_F1",
        "label": "Latina — 44 — Outside, South LA community garden — morning",
        "prompt": (
            "Extreme close-up portrait photograph of a 44-year-old Latina woman, face filling "
            "nearly the entire frame — from just below the chin to just above the crown, "
            "cheekbones, jawline, and full forehead all visible, face centered in 9:16 frame. "
            "Shot outdoors at a community garden in South Los Angeles, early morning soft diffused "
            "light, green leafy bokeh in the background. Medium-tan olive skin, highly visible "
            "pores, crow's feet, faint acne scars on one cheek, slight sun freckling across the "
            "nose, un-evened skin tone, no makeup whatsoever. Dark brown hair with prominent grey "
            "streaks at the temples, pulled back loosely in a simple elastic, flyaway strands "
            "around the face. Direct steady gaze straight into the camera lens, eyes slightly "
            "narrowed from squinting in light, lips closed in a flat neutral line, no expression "
            "performed. A small stud earring. Plain green t-shirt visible at very bottom edge. "
            "Background: soft green blur of garden beds and chain-link fencing, completely out "
            "of focus. " + REAL
        ),
    },
    {
        "id": "persona_CWL2_F2",
        "label": "Latina — 47 — Outside, urban bus stop / transit shelter — late afternoon",
        "prompt": (
            "Extreme close-up portrait photograph of a 47-year-old Latina woman, face filling "
            "nearly the entire frame — from just below the chin to just above the crown, "
            "face centered in 9:16 frame. Shot outdoors at a city bus stop or metro transit "
            "shelter in a dense California urban neighborhood, late afternoon side-light from "
            "low sun, slight warm golden cast. Medium-tan skin with deep nasolabial folds, "
            "forehead lines, slight drooping at the jaw, under-eye bags, dry lips, no makeup. "
            "Dark hair significantly greyed throughout, worn flat and straight to the shoulder, "
            "no styling, slight wind-blown texture. Calm tired direct gaze into the camera, "
            "mouth softly closed and neutral, a quiet weight in the eyes — waiting, patient. "
            "A worn strap of a tote bag visible at the shoulder edge. Plain dark navy top "
            "at very bottom edge of frame. Background: completely blurred — faded bus shelter "
            "glass, a partial transit ad poster, urban sidewalk edge. " + REAL
        ),
    },
    {
        "id": "persona_CWL2_F3",
        "label": "Latina — 43 — Inside, small Catholic church pew — dim ambient light",
        "prompt": (
            "Extreme close-up portrait photograph of a 43-year-old Latina woman, face filling "
            "nearly the entire frame — from just below the chin to just above the crown, "
            "face centered in 9:16 frame. Shot indoors, seated in a pew inside a small "
            "neighborhood Catholic church in California, dim warm ambient light from candles "
            "and faint colored light from a stained glass window, low-key soft shadows across "
            "the face. Tan skin with fine lines, slight under-eye circles, natural blemishes, "
            "no retouching, no filter, small dark mole near the corner of the mouth. Dark "
            "brown hair with grey roots growing in, worn simply down or pulled half back, "
            "straight and flat, no styling. Eyes directed into the lens with quiet seriousness — "
            "a look of someone who has held a lot privately. Lips pressed together in a soft "
            "flat line. A thin gold chain at the neck, just barely visible. Plain dark blouse. "
            "Background: completely out of focus warm amber blur of candles and pew wood. "
            + REAL
        ),
    },
    {
        "id": "persona_CWL2_F4",
        "label": "Latina — 50 — Inside, clinic waiting room — fluorescent overhead light",
        "prompt": (
            "Extreme close-up portrait photograph of a 50-year-old Latina woman, face filling "
            "nearly the entire frame — from just below the chin to just above the crown, "
            "face centered in 9:16 frame. Shot indoors in the waiting room of a community "
            "health clinic or county office in California, flat harsh fluorescent overhead "
            "light, slightly cold neutral-white cast, even illumination with no flattering "
            "shadows. Olive-tan skin, deeply weathered, pronounced forehead and cheek lines, "
            "age spots on the temple, visible capillaries along the nose, heavy under-eye "
            "darkness, no makeup. Greying dark hair cut short and practical, barely styled, "
            "significant silver at the crown. Direct steady gaze into the lens — a look of "
            "someone who is used to waiting, carrying something. Jaw set, lips in a flat "
            "neutral line, slight tension around the eyes. Plain charcoal grey top visible "
            "at the very bottom edge. Background: completely out of focus pale institutional "
            "wall, a blur of plastic chairs. " + REAL
        ),
    },
]


def generate(p):
    pid = p["id"]
    out_path = OUT / f"{pid}.jpg"
    if out_path.exists() and out_path.stat().st_size > 50_000:
        print(f"  {pid}: exists ({out_path.stat().st_size // 1024}KB), skipping")
        return pid, str(out_path)

    payload = {
        "prompt": p["prompt"],
        "model": "nano-banana-2",
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

    saved = []
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
        saved.append(vpath)
        print(f"  {pid}_v{i+1}: saved {vpath.stat().st_size // 1024}KB  mediaId: {mid}")

    if saved:
        shutil.copy(saved[0], out_path)

    print(f"✓ {pid}: {out_path}  [{p['label']}]  ({len(saved)} variants)")
    return pid, str(out_path)


if __name__ == "__main__":
    print(f"CA Women Latina Personas (CLOSE-UP) — 4 women ages 42–50 (nano-banana-2) → {OUT}\n")
    print("F1: Latina 44, South LA community garden (outdoor)")
    print("F2: Latina 47, urban bus stop / transit shelter (outdoor)")
    print("F3: Latina 43, small Catholic church pew (indoor)")
    print("F4: Latina 50, clinic / county office waiting room (indoor)\n")

    results = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(generate, p): p["id"] for p in PERSONAS}
        for fut in as_completed(futs):
            pid = futs[fut]
            try:
                pid, path = fut.result()
                results[pid] = path
            except Exception as e:
                print(f"✗ {pid} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/4")
    for pid in sorted(results):
        print(f"  {pid}: {results[pid]}")
