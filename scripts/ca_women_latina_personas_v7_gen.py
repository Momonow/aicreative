"""
CA Women's Prison — 4 Survivor-Authentic Latina Personas v7 (ages 42–62)
Demographic: CA women's prison population — Central Valley / LA / Inland Empire / Bay Area
UGC SELFIE MODE — phone held at arm's length, candid, NOT glamorous
Realism tail baked in: weathered, visible age, practical hair, faded tattoos, natural teeth
2 outdoor + 2 indoor | heritages fresh vs v1–v6
useapi.net nano-banana-pro | 9:16
"""
import os, requests, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_women_latina_personas_v7")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_CWL7_F1",
        "label": "Latina 52 — Central Valley Mexican-American 3rd gen — indoor kitchen — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held slightly below eye level — she's seated at a kitchen table looking up at the lens. "
            "Authentic candid feel, NOT a studio portrait.\n\n"
            "52-year-old Mexican-American woman, third-generation Central Valley California "
            "(Fresno / Madera County area). "
            "FACE SHAPE: round and full — broad forehead, high soft cheekbones, full cheeks, "
            "rounded chin. Face carries weight and life. "
            "SKIN: warm medium-dark brown — classic Central Valley complexion, sun-weathered. "
            "Age marks: deep horizontal forehead lines, pronounced nasolabial folds, beginning jowl "
            "softness, age spots along jaw and temple, sun damage on the nose bridge, "
            "uneven blotchy tone, visible pores. "
            "NO makeup, NO beauty mode, NO retouching, NO filter, NO skin smoothing. "
            "HAIR: thick black hair with heavy grey roots growing out — 2–3 inches of silver-grey "
            "at the crown, black below, pulled into a loose low ponytail with flyaways and frizz. "
            "NOT recently dyed, NOT styled. Practical and unselfconscious. "
            "EYES: dark warm brown, slightly droopy outer corners, prominent bags underneath, "
            "a quiet steadiness — looking directly upward into the lens. "
            "MOUTH: medium-full lips, natural warm brown-rose tone, slightly downturned resting "
            "neutral. Slightly imperfect teeth — natural off-white, not polished, not bright white. "
            "BODY: broader heavier build, visible clavicle and upper chest. "
            "VISIBLE DETAIL: a faded tattoo on the upper chest or collarbone — older ink, "
            "a simple name or design, edges blurred with age and sun.\n\n"
            "SETTING: indoors at a small California apartment kitchen — overhead fluorescent "
            "or plain ceiling light, old tile backsplash and laminate countertop slightly visible "
            "behind her, basic kitchen table surface at frame edge. Flat practical light. "
            "Background completely blurred. "
            "CLOTHING: plain heather-grey t-shirt, worn fabric, slightly stretched collar.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, sun damage, age spots, faded tattoo, natural imperfect teeth. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL7_F2",
        "label": "Latina 46 — Guatemalan-American Ladino — outdoor apartment stoop — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held at arm's length, eye level — standing or sitting on a concrete apartment stoop "
            "outdoors. Subject looks directly at the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "46-year-old Guatemalan-American woman, Ladino heritage (Spanish-colonial descent, "
            "NOT Maya indigenous — European-influenced Guatemalan features). "
            "FACE SHAPE: angular oval — strong defined jaw, angular high cheekbones, slightly narrow "
            "forehead, moderately pointed chin. Lean facial structure. "
            "SKIN: warm medium olive-brown — a rich tawny-olive tone, NOT pale white, NOT dark. "
            "Age marks: moderate forehead lines, developing nasolabial folds, slight hollowing under "
            "cheekbones, faint acne scarring on the cheeks, dark circles under the eyes, "
            "visible pores, no makeup whatsoever. "
            "HAIR: dark brown straight hair — worn in a simple low ponytail, a few loose strands "
            "framing the face, early grey appearing at the temples only, flat and unstyled. "
            "NOT highlighted, NOT blow-dried. "
            "EYES: medium warm-dark brown, slightly deep-set, alert and direct, noticeable tiredness "
            "in the lower lids. Looking directly at the lens. "
            "MOUTH: medium lips, natural neutral-rose tone, composed slightly firm resting expression. "
            "Slightly imperfect teeth — natural tone, not polished, visible if mouth is relaxed open. "
            "BODY: slim to medium build, visible neck and collarbone. "
            "CLOTHING: plain black worn hoodie, zipped partway, lived-in look.\n\n"
            "SETTING: outdoors on a concrete stoop of a modest Los Angeles apartment building — "
            "late afternoon warm golden side-light. Background blurred — stucco wall, metal railing, "
            "parked cars at the curb, faded paint on the building facade. "
            "Urban unglamorous background.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, acne scarring, dark circles, natural imperfect teeth. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL7_F3",
        "label": "Latina 58 — Panamanian Afro-Latina mix — indoor motel-style bedroom — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held at arm's length, angled slightly downward — a quick bedroom selfie, "
            "she's sitting on or near a bed. Subject looks directly up into the lens. "
            "Authentic candid feel, NOT a studio portrait.\n\n"
            "58-year-old Panamanian-American woman with Afro-Latina heritage — "
            "mixed indigenous-Black-Spanish Panamanian, California resident. "
            "FACE SHAPE: broader oval — wide forehead, prominent cheekbones, "
            "broad nose with rounded tip, strong jaw, full rounded chin. "
            "SKIN: warm deep medium-brown — a rich warm brown tone, reddish-brown undertone, "
            "NOT dark-dark, NOT copper — deep warm café-au-lait brown. "
            "Heavily aged: deep forehead creases, pronounced smile lines, significant jowl softness, "
            "under-eye darkness and crêpiness, age spots on the cheeks and forehead, "
            "uneven tone, sun weathering at the temples. 58 years fully visible. NO makeup. "
            "HAIR: natural 3B-3C coily-curly hair, black heavily threaded with silver-grey — "
            "significant grey at the temples and crown, dark curls beneath. "
            "Worn loose, some shrinkage, not stretched or blow-dried. Natural and real. "
            "EYES: very dark warm brown, slightly wide-set, carrying age and quiet weight, "
            "direct calm gaze upward at the lens. "
            "MOUTH: medium-full lips, natural deep warm rose tone, resting neutral — "
            "composed and still. Slightly imperfect teeth — natural off-white, authentic. "
            "BODY: medium build, visible neck and collarbone. "
            "VISIBLE DETAIL: a small simple tattoo on the forearm or wrist — faded older ink, "
            "simple design, blurred edges from age.\n\n"
            "SETTING: indoors in a modest bedroom — single bedside lamp or dim window light. "
            "Background completely blurred — plain bed with simple sheets, basic nightstand, "
            "generic motel-ish or basic apartment bedroom. Warm dim light. "
            "CLOTHING: plain dark navy blue v-neck t-shirt, simple and worn.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, deep age lines, age spots, faded tattoo, natural imperfect teeth. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL7_F4",
        "label": "Latina 44 — Mixed Chicana Mexican-Indigenous-White — outdoor parking lot — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held at arm's length, approximately eye level — a quick outdoor selfie, "
            "she's standing near a car in a parking lot. Subject looks directly at the lens. "
            "Authentic candid feel, NOT a studio portrait.\n\n"
            "44-year-old woman of mixed Chicana heritage — Mexican-American with "
            "indigenous and white ancestry, Bay Area / Central Valley California. "
            "FACE SHAPE: heart-shaped — broader forehead tapering, high cheekbones, "
            "slightly fuller mid-cheek, softly rounded chin. "
            "SKIN: warm golden-brown — a medium warm caramel-brown tone, golden undertone, "
            "NOT dark, NOT pale — a sun-kissed warm middle. "
            "Age-appropriate: moderate forehead lines, developing smile lines, slight skin texture "
            "at the cheeks, under-eye darkness, faint melasma patches on the forehead, "
            "visible pores, uneven tone. NO makeup, NO beauty mode. "
            "HAIR: natural 2B-2C wavy dark brown hair with scattered grey throughout — "
            "NOT dyed, natural wave texture and slight frizz, falls to the shoulder, worn loose "
            "or pushed back. Practical and real. "
            "EYES: medium warm brown, alert and direct, slight bags underneath, "
            "a quiet steadiness looking directly at the lens. "
            "MOUTH: medium lips, natural warm rose-brown tone, composed and neutral. "
            "Slightly imperfect teeth — authentic off-white, not polished. "
            "BODY: medium build, visible neck and collarbone. "
            "VISIBLE DETAIL: a small faded tattoo on the neck or upper chest — older ink, "
            "a simple design (small star, initials, or simple symbol), edges blurred with age. "
            "CLOTHING: dark olive army-green zip-up jacket over a plain white t-shirt, "
            "casual and worn.\n\n"
            "SETTING: outdoors near a parking lot — an older sedan partially visible and blurred "
            "behind her, chain-link fence or concrete wall further back, flat overcast "
            "California daylight, even light on her face. Urban, unglamorous, real.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, melasma, faded tattoo, natural imperfect teeth, wavy natural hair. "
            "9:16 vertical portrait, photo-realistic."
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
    print(f"CA Women Latina Personas V7 (survivor-authentic, ages 42–62) — nano-banana-pro → {OUT}\n")
    print("F1: 52, Central Valley Mexican-American 3rd gen  — kitchen (indoor)   — selfie")
    print("F2: 46, Guatemalan-American Ladino               — apartment stoop (outdoor) — selfie")
    print("F3: 58, Panamanian Afro-Latina mix               — bedroom (indoor)   — selfie")
    print("F4: 44, Mixed Chicana Mexican-Indigenous-White   — parking lot (outdoor) — selfie\n")

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
