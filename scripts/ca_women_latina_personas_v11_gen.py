"""
CA Women's Prison — 4 American Latina Personas v11 (ages 50–60)
Very different faces from v8/v9/v10. Low necklines, some tattoos visible.
useapi.net nano-banana-pro | 9:16
"""
import os, requests, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_women_latina_personas_v11")
OUT.mkdir(parents=True, exist_ok=True)

REALISM = (
    "Photoreal candid phone selfie. NOT a glamour or fashion shoot. "
    "Ordinary real American woman, natural skin with visible pores, fine lines, "
    "under-eye shadows, slightly imperfect teeth, no beauty retouching, no filter, no makeup. "
    "9:16 vertical, photo-realistic."
)

PERSONAS = [
    {
        "id": "persona_CWL11_F1",
        "label": "Latina 53 — angular jawline, medium olive, chest tattoo, v-neck top, kitchen counter",
        "prompt": (
            "UGC phone selfie, 9:16 vertical portrait. "
            "Phone held slightly below the face, angled upward — leaning back against a kitchen counter, "
            "chest and face visible. Candid, real.\n\n"
            "53-year-old Latina woman, American-born. "
            "FACE: strong angular face — sharp defined jawline, prominent cheekbones, "
            "slightly hollow cheeks, medium olive-warm complexion. "
            "DISTINCTLY angular features — NOT round, NOT soft. "
            "Natural aging: defined lines around the mouth and eyes, slight marionette lines. "
            "HAIR: straight dark brown hair with scattered silver strands, "
            "worn loose to just below the shoulder, flat and simple. "
            "EYES: deep-set almond-shaped, dark brown, steady direct gaze. "
            "MOUTH: medium lips, natural tone, neutral expression. "
            "BODY: medium-lean build, visible neck, collarbone, and upper chest. "
            "CLOTHING: deep V-neck burgundy top, showing collarbone and slight cleavage. "
            "TATTOO: small black ink cross or simple floral design on the upper left chest, "
            "just below the collarbone — old ink, slightly faded.\n\n"
            "SETTING: indoor — leaning against a kitchen counter, modest California home. "
            "Blurred background — countertop, cabinets, overhead kitchen light. "
            "Natural daylight from a window to the side.\n\n"
            + REALISM
        ),
    },
    {
        "id": "persona_CWL11_F2",
        "label": "Latina 57 — soft round face, darker brown skin, fuller figure, shoulder tattoo, scoop-neck, outdoor wall",
        "prompt": (
            "UGC phone selfie, 9:16 vertical portrait. "
            "Phone held at arm's length, eye level — standing against an exterior wall, "
            "slight downward angle to the camera. Candid, real.\n\n"
            "57-year-old Latina woman, American-born, California. "
            "FACE: very soft round face — full cheeks, rounded chin, broad smooth forehead, "
            "NO sharp angles. Deep warm brown complexion, rich chocolate-brown skin tone, "
            "smooth but with real texture and aging. "
            "DISTINCTLY round soft face — completely different from angular. "
            "Natural aging for 57: pronounced smile lines, softer jaw, some puffiness under the eyes. "
            "HAIR: natural tight-curly hair (4A texture), dark brown going heavily grey — "
            "worn in a loose low puff or short natural at the ears, natural texture, no heat styling. "
            "EYES: warm dark brown, wide and expressive, looking into the lens. "
            "MOUTH: full wide lips, natural dark rose tone, relaxed open expression. "
            "BODY: fuller curvier build, visible neck and shoulder. "
            "CLOTHING: wide scoop-neck tank top, soft teal or sage green color, "
            "showing collarbone, chest, and upper cleavage. "
            "TATTOO: colorful floral tattoo on the right shoulder — roses or hibiscus, "
            "older faded ink, partially visible at the shoulder strap.\n\n"
            "SETTING: outdoor — exterior wall of an apartment building or house, "
            "California suburban daylight. Blurred stucco or concrete wall behind her.\n\n"
            + REALISM
        ),
    },
    {
        "id": "persona_CWL11_F3",
        "label": "Latina 50 — narrow elongated face, light warm skin, forearm tattoo, low-cut top, bedroom mirror",
        "prompt": (
            "UGC phone selfie, 9:16 vertical portrait. "
            "Phone held at mid-chest level, mirror selfie — standing in front of a bathroom "
            "or bedroom mirror, full face and upper body visible. Candid, real.\n\n"
            "50-year-old Latina woman, born in the United States. "
            "FACE: narrow elongated oval face — long slim face, high narrow forehead, "
            "small pointed chin, visible cheekbone structure but NOT round at all. "
            "Light warm Latina complexion — fair to light golden skin, Spanish-European mix. "
            "Younger-looking for 50: mild forehead lines, slight crow's feet, still mostly smooth. "
            "HAIR: wavy medium-brown hair, highlighted with warm caramel tones (salon-highlighted), "
            "worn loose to the collarbone, with some wave. One of few in the group with colored highlights. "
            "EYES: green-hazel or light brown, almond-shaped, looking into the phone/mirror. "
            "MOUTH: thinner lips, natural rosy tone, slight smirk or composed neutral. "
            "BODY: slim build, visible neck, collarbone, chest. "
            "CLOTHING: low-cut black cami or deep-cut tank, showing collarbone and cleavage. "
            "TATTOO: script tattoo on the left forearm — cursive lettering (could be a name or word), "
            "black ink, clear and readable, real tattoo proportions.\n\n"
            "SETTING: indoor — bathroom or bedroom mirror selfie. "
            "Reflection visible in the mirror — she's holding the phone up. "
            "Simple background — plain wall, light fixture, or doorframe behind. "
            "Warm indoor light.\n\n"
            + REALISM
        ),
    },
    {
        "id": "persona_CWL11_F4",
        "label": "Latina 59 — wide square face, medium warm skin, no tattoo, off-shoulder top, backyard",
        "prompt": (
            "UGC phone selfie, 9:16 vertical portrait. "
            "Phone held slightly above eye level, looking up — sitting on a backyard step "
            "or patio chair, relaxed. Candid, real.\n\n"
            "59-year-old Latina woman, California-raised. "
            "FACE: wide square face — broad flat forehead, wide cheekbones at the same width "
            "as the forehead, strong square jaw. Medium warm brown complexion, "
            "sun-kissed California skin with some sun damage and freckles. "
            "DISTINCTLY wide square face — completely different shape from the other three. "
            "Natural aging for 59: deep smile lines, heavier forehead creases, "
            "some jowl softening, real lived-in skin. "
            "HAIR: thick wavy hair, heavily salt-and-pepper — roughly equal grey and dark brown, "
            "cut in a medium shag or layered cut to the collarbone, slightly messy and natural. "
            "EYES: warm medium brown, direct calm gaze. "
            "MOUTH: medium lips, natural warm tone, composed neutral expression. "
            "BODY: medium-heavier build, visible neck, bare shoulders. "
            "CLOTHING: off-shoulder top or wide-neck sweatshirt worn off one shoulder — "
            "dusty mauve or heather grey, showing one bare shoulder and collarbone, "
            "slight chest visible. No tattoos on this one.\n\n"
            "SETTING: outdoor — backyard or patio, California afternoon light. "
            "Blurred background — dry grass, wood fence, a plant pot. "
            "Flat warm natural daylight.\n\n"
            + REALISM
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
        if not url:
            continue
        vpath = OUT / f"{pid}_v{i+1}.jpg"
        img_r = requests.get(url, timeout=60)
        img_r.raise_for_status()
        vpath.write_bytes(img_r.content)
        saved.append(vpath)
        print(f"  {pid}_v{i+1}: saved {vpath.stat().st_size // 1024}KB")

    if saved:
        shutil.copy(saved[0], out_path)

    print(f"✓ {pid}: [{p['label']}]  ({len(saved)} variants)")
    return pid, str(out_path)


if __name__ == "__main__":
    print(f"CA Women Latina Personas V11 (American Latina, ages 50–60) — nano-banana-pro → {OUT}\n")
    print("F1: 53  angular jawline, olive, chest tattoo     — kitchen counter (indoor)")
    print("F2: 57  soft round, dark brown skin, shoulder tattoo — exterior wall (outdoor)")
    print("F3: 50  narrow elongated, light skin, forearm tattoo — mirror selfie (indoor)")
    print("F4: 59  wide square face, salt-pepper shag        — backyard patio (outdoor)\n")

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
