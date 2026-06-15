"""
CA Women's Prison — 4 Survivor-Authentic Latina Personas v8 (ages 50–62)
Demographic: CA women's prison population — LA / Inland Empire / Bay Area / Central Valley
UGC SELFIE MODE — phone held at arm's length, candid, NOT glamorous
Realism tail baked in: weathered, visible age, practical hair, faded tattoos, natural teeth
Heritages DISTINCT from v7 (no repeat of Mexican 3rd-gen / Guatemalan Ladino / Panamanian / Chicana mixed)
2 outdoor + 2 indoor | ages 50–62 | useapi.net nano-banana-pro | 9:16
"""
import os, requests, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_women_latina_personas_v8")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_CWL8_F1",
        "label": "Latina 54 — Puerto Rican-American, Inland Empire — indoor living room — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held at arm's length, slightly above eye level — seated on a worn sofa in a small "
            "living room, looking up into the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "54-year-old Puerto Rican-American woman, born in New York, living in the Inland Empire "
            "(Riverside / San Bernardino area). Boricua heritage — mixed Spanish, African, and Taíno "
            "ancestry. "
            "FACE SHAPE: full round oval — wide soft cheekbones, full rounded cheeks, soft chin, "
            "broad forehead. A warm and substantial face. "
            "SKIN: warm medium brown — a rich honey-brown with golden-red undertone, "
            "Caribbean Latino complexion, NOT pale, NOT dark — a warm in-between. "
            "Age marks: pronounced forehead creases, deep nasolabial folds, developing jowl "
            "softness, under-eye darkness and puffiness, uneven skin tone with slight redness "
            "across the cheeks and nose, visible pores, NO makeup, NO beauty mode. "
            "HAIR: natural 3C-4A coily curly hair — black heavily threaded with silver-grey, "
            "significant grey at the temples and roots, pulled loosely into a high puff or bun "
            "with short curls escaping around the face. Natural shrinkage, real texture, "
            "NOT styled or blown out. "
            "EYES: medium warm dark brown, slightly wide-set and round, carrying tiredness, "
            "direct and steady gaze upward into the lens. "
            "MOUTH: full lips, natural warm rose-brown tone, resting neutral expression. "
            "Slightly imperfect teeth — natural off-white, not polished. "
            "BODY: heavier full build, visible neck and chest. "
            "VISIBLE DETAIL: a faded tattoo on the upper chest or collarbone — older ink, "
            "a simple name or design, edges blurred with age.\n\n"
            "SETTING: indoors in a small Inland Empire apartment living room — a worn fabric "
            "sofa behind her, basic ceiling light or lamp, plain painted walls, a folded blanket "
            "draped on the couch arm. Background completely blurred. Flat warm interior light. "
            "CLOTHING: loose dark burgundy tank top, plain and lived-in.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, forehead creases, under-eye puffiness, faded tattoo, natural coily hair. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL8_F2",
        "label": "Latina 60 — Salvadoran-American, South LA — outdoor bus stop / sidewalk — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held at arm's length, approximately eye level — standing on a South Los Angeles "
            "sidewalk near a bus stop, looking directly at the lens. "
            "Authentic candid feel, NOT a studio portrait.\n\n"
            "60-year-old Salvadoran-American woman, first-generation immigrant, South Los Angeles. "
            "Central American indigenous-mestizo heritage — Salvadoran features with indigenous Pipil "
            "and mestizo ancestry. "
            "FACE SHAPE: broad square-oval — wide flat forehead, broad prominent cheekbones set wide "
            "and flat, rounded jaw, compact broad chin. Solid and sturdy facial structure. "
            "SKIN: warm dark medium-brown — a deep warm brown, richer and darker than a light olive, "
            "NOT black — a strong warm mahogany-brown. "
            "Heavily aged: deep forehead furrows, very pronounced nasolabial folds carved deep, "
            "significant jowl softness, deep under-eye hollows and darkness, age spots on forehead "
            "and cheeks, sun-weathered rough skin texture, visible pores, NO makeup, NO beauty mode. "
            "HAIR: straight dark brown-black hair, heavy silver-grey throughout — "
            "mostly grey now, dark underneath, worn flat and practical in a simple low bun or "
            "pulled back with a clip. Flat, unstretched, simple. "
            "EYES: dark warm brown, slightly narrow and deep-set, carrying 60 years of weight, "
            "direct gaze at the lens. "
            "MOUTH: medium lips, natural warm neutral tone, firm composed resting expression. "
            "Slightly imperfect teeth — natural, not polished, slightly uneven. "
            "BODY: compact sturdy build, visible neck and upper chest. "
            "CLOTHING: plain royal blue short-sleeve work shirt, slightly faded.\n\n"
            "SETTING: outdoors on a South Los Angeles sidewalk — bus stop shelter or bus bench "
            "partially visible, blurred concrete city background, chain-link fence or building "
            "facade behind, flat California daylight, slightly overcast. Urban and unglamorous.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, deep furrows, age spots, sun damage, slightly uneven teeth. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL8_F3",
        "label": "Latina 50 — Dominican-American, LA / Compton area — outdoor apartment courtyard — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held at arm's length, slightly below eye level — standing in an apartment "
            "courtyard or near a doorway outdoors, looking up at the lens. "
            "Authentic candid feel, NOT a studio portrait.\n\n"
            "50-year-old Dominican-American woman, Caribbean Latina, "
            "raised in Compton / Watts area of Los Angeles. Dominican heritage — "
            "mixed Spanish, African, and Taíno — distinctly Caribbean features. "
            "FACE SHAPE: long angular oval — high prominent cheekbones, longer narrow face, "
            "angular jaw, slightly pointed chin. "
            "SKIN: warm medium-dark brown — a rich warm café-au-lait brown with reddish undertone, "
            "deep Caribbean complexion. "
            "Age marks: developing horizontal forehead lines, pronounced nasolabial folds, "
            "hollow cheekbones with slight gauntness, dark circles and hollowing under the eyes, "
            "uneven skin tone, some hyperpigmentation along the jaw, visible pores, "
            "NO makeup, NO beauty mode. "
            "HAIR: relaxed or heat-straightened dark brown hair — heavily grown-out, "
            "significant silver-grey roots showing several inches, darker brown below, "
            "shoulder-length, worn loose and flat, slightly dry and broken at the ends. "
            "NOT styled. Grown-out practical real-life hair. "
            "EYES: very dark warm brown, slightly hooded, angular almond shape, "
            "direct and measured gaze at the lens, carrying quiet wariness. "
            "MOUTH: fuller lips, natural warm brown-rose tone, slightly tense composed resting "
            "expression. Slightly imperfect teeth — natural color, not bright white. "
            "BODY: lean to medium build, visible neck and collarbone. "
            "VISIBLE DETAIL: a faded tattoo on the forearm — older ink, a name or simple "
            "design, lines blurred and spread with age. "
            "CLOTHING: plain white tank top under an open olive drab shirt, unbuttoned, "
            "casual and worn.\n\n"
            "SETTING: outdoors in an apartment building courtyard — "
            "concrete walkway, plain stucco walls with chipped paint, a metal gate or "
            "mailboxes partially blurred in background. Flat afternoon California light. "
            "Urban unglamorous real neighborhood.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, dark circles, hyperpigmentation, faded tattoo, grown-out roots. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL8_F4",
        "label": "Latina 62 — Oaxacan Mexican-indigenous (first gen), Central Valley — indoor kitchen/table — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "Phone held slightly below eye level, arm's length — seated at a small kitchen table, "
            "looking upward at the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "62-year-old woman, first-generation Mexican immigrant from Oaxaca, "
            "Zapotec indigenous heritage, Central Valley California (Fresno / Visalia area). "
            "FACE SHAPE: round and broad — very wide broad forehead, very prominent wide cheekbones, "
            "full broad cheeks, rounded compact jaw, short rounded chin. "
            "Distinctly Zapotec indigenous facial structure — broader, flatter, more compact than "
            "mestizo Mexican features. "
            "SKIN: warm deep golden-brown — a rich deep copper-brown, indigenous Central Mexican "
            "complexion, sun-darkened from decades in the Central Valley. "
            "Heavily aged: deep horizontal forehead lines carved in, very deep nasolabial folds, "
            "pronounced jowl droop, deep under-eye bags and darkness, age spots and sun damage "
            "across forehead and cheeks, very visible pores, dry skin texture. "
            "62 years FULLY visible. NO makeup, NO beauty mode. "
            "HAIR: thick straight hair — black with heavy white-grey throughout, "
            "especially at the temples and crown. Worn in a simple long braid down the shoulder "
            "or pulled back in a low bun with loose strands. "
            "Classic practical Oaxacan elder hair — NOT styled, NOT highlighted. "
            "EYES: very dark brown, slightly deep-set in a broader face, a quiet steady heaviness "
            "in the gaze — looking directly upward into the lens. "
            "MOUTH: medium lips, natural warm neutral-brown tone, resting expression settled "
            "and composed. Slightly imperfect teeth — natural, slightly worn, not polished. "
            "BODY: shorter compact build, heavier, visible neck and upper chest. "
            "CLOTHING: a worn patterned cotton blouse — simple floral or small geometric print, "
            "faded from washing, practical and unpretentious.\n\n"
            "SETTING: indoors at a very modest Central Valley kitchen — "
            "plain Formica or laminate table surface at frame edge, "
            "a window with plain curtains slightly visible, overhead light, "
            "old tile or plain wall slightly visible. Background completely blurred. "
            "Flat practical interior light.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday survivor woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "Visible pores, deep carved lines, age spots, sun damage, natural practical hair. "
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
    print(f"CA Women Latina Personas V8 (survivor-authentic, ages 50–62) — nano-banana-pro → {OUT}\n")
    print("F1: 54, Puerto Rican-American / Inland Empire      — living room (indoor)    — selfie")
    print("F2: 60, Salvadoran-American / South LA             — bus stop sidewalk (outdoor) — selfie")
    print("F3: 50, Dominican-American / Compton-LA            — apartment courtyard (outdoor) — selfie")
    print("F4: 62, Oaxacan indigenous-Mexican / Central Valley — kitchen table (indoor)  — selfie\n")

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
