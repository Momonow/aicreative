"""
CA Women's Prison — 4 DISTINCT Latina Personas v5 (ages 38–49)
UGC SELFIE MODE — phone held at arm's length, slight overhead angle, candid
2 outdoor + 2 indoor | fresh locations not used in v1–v4
Heritages not used before: Venezuelan, Colombian, Honduran, Cuban-American
useapi.net nano-banana-2 | 9:16
"""
import os, requests, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_women_latina_personas_v5")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_CWL5_F1",
        "label": "Latina 42 — Venezuelan — outdoor Venice Beach canal path — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, slightly above eye level — "
            "the camera angle is casual and slightly overhead, exactly like a real phone selfie. "
            "Subject looks slightly upward toward the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "42-year-old Venezuelan-American woman. "
            "FACE SHAPE: classic oval, balanced proportions — slightly wider at the cheekbones tapering evenly "
            "to a softly rounded chin. Moderate nose with a refined straight bridge. "
            "SKIN: warm light olive — a pale golden tan, NOT dark, NOT copper. "
            "Slight freckling across the nose, fine lines at the eye corners, "
            "natural uneven skin tone, visible pores, no makeup, no filter. "
            "HAIR: medium-length straight honey-brown hair with natural sun highlights — "
            "warm auburn undertones, slightly fine texture, worn loose and natural, "
            "parted off-center, falls past the shoulders. A few wisps catching a slight breeze. "
            "EYES: light warm hazel — golden-green-brown, medium-sized, slight tilt at outer corners, "
            "looking slightly up at the camera lens. "
            "MOUTH: medium lips, natural pale rose tone, relaxed slight open — mid-conversation.\n\n"
            "SETTING: outdoors on a narrow Venice Beach canal path — "
            "a low footbridge and calm turquoise-tinted canal water visible and blurred behind her, "
            "lush tropical greenery, dappled afternoon California sunlight. "
            "Warm golden-hour side-light on her face. "
            "Wearing a loose off-white linen tank top, visible clavicle and shoulders.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL5_F2",
        "label": "Latina 45 — Colombian mestiza — indoor apartment bedroom morning — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, angled very slightly downward — "
            "a casual bedroom selfie, the kind someone takes first thing in the morning. "
            "Subject looks directly up into the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "45-year-old Colombian-American woman with mestiza heritage. "
            "FACE SHAPE: heart-shaped — wide forehead narrowing to a soft pointed chin, "
            "rounded cheeks, defined widow's peak hairline. "
            "SKIN: warm medium brown — deeper than tan but lighter than dark brown, "
            "a warm caramel-mocha tone with yellow-warm undertone. "
            "Natural skin texture: forehead crease lines, smile lines, slight uneven tone, "
            "a few small spots at the jaw, visible pores, no makeup, no filter. "
            "HAIR: dark brown chin-length blunt bob with natural frizz — "
            "slight natural wave, dense and thick, with scattered grey hairs throughout, "
            "slightly tousled as if just woken up. NOT styled. "
            "EYES: dark brown, slightly wide-set, slightly droopy outer corners giving a "
            "gentle soft expression, direct gaze into the lens. "
            "MOUTH: full lips, medium-dark rose tone, parted slightly — "
            "a tired but warm almost-smile, corners relaxed.\n\n"
            "SETTING: indoors in a modest California apartment bedroom — "
            "early morning soft diffuse light from a curtained window to the side, "
            "warm pale-gold light on her face. Background completely blurred — "
            "a rumpled bedsheet, a pillow, and a charging cable on a nightstand out of focus. "
            "Wearing a plain light-grey sleep T-shirt, slightly worn, visible shoulders.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL5_F3",
        "label": "Latina 38 — Honduran Maya-mestiza — outdoor Oakland neighborhood sidewalk — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, slightly above eye level — "
            "a quick outdoor sidewalk selfie, casual and unstaged. "
            "Subject looks slightly upward toward the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "38-year-old Honduran-American woman with Maya-mestiza heritage. "
            "FACE SHAPE: wide and slightly low — broad flat forehead, very prominent wide cheekbones "
            "set high on the face, a broader nose with flared nostrils, "
            "compact rounded chin. Face reads young but weathered. "
            "SKIN: deeper warm copper-tan — richer and darker than olive, "
            "a medium-dark warm brown with coppery red undertone. "
            "Sun weathering: slight patchy tan lines on the neck, "
            "forehead texture, natural blemishes, visible pores, faint dark circles. "
            "HAIR: very thick coarse jet-black hair worn in a single loose low braid — "
            "the braid falls over one shoulder, slightly flyaway frizz at the crown, "
            "a few face-framing strands loose. No grey. "
            "EYES: dark near-black brown, slightly almond-shaped, "
            "slightly deep-set under prominent brows, steady gaze upward into the lens. "
            "MOUTH: wide full lips, deep natural rose-brown tone, flat relaxed line.\n\n"
            "SETTING: outdoors on an Oakland neighborhood sidewalk in late afternoon — "
            "a tree-lined residential street, mature oak tree canopy blurred behind her, "
            "dappled warm late afternoon light, a parked car and Victorian houses soft in the distance. "
            "Wearing a plain dark olive-green hoodie, front zipper half-open, "
            "visible neck and collarbones.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL5_F4",
        "label": "Latina 48 — Cuban-American — indoor home office plants window — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, approximately eye level — "
            "a work-from-home quick selfie in a home office. "
            "Subject looks directly into the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "48-year-old Cuban-American woman. "
            "FACE SHAPE: round full face — evenly rounded from forehead to cheeks to chin, "
            "soft rounded jawline, round forehead, full cheeks with natural plumpness. "
            "SKIN: light olive — warm neutral undertone, NOT tan, NOT dark — a pale-to-medium "
            "olive complexion. Age-appropriate skin: soft forehead lines, deeper smile lines "
            "around the mouth, slight jowl softness, under-eye creases, age spots at the temples. "
            "HAIR: shoulder-length natural 3A-3B loose spiral curls, salt-and-pepper — "
            "significantly grey throughout, dark brown visible underneath, "
            "curls worn natural and a little loose, some frizz. NOT dyed. "
            "EYES: medium warm brown with slight bags underneath, "
            "slight crow's feet, direct calm gaze into the lens. "
            "MOUTH: medium-full lips, natural neutral-pink tone, "
            "a small genuine relaxed smile — the first smile across all v5 personas, "
            "but soft and tired, not performative.\n\n"
            "SETTING: indoors at a home office desk corner — "
            "soft north-facing window light from the left, cool-white overcast California light. "
            "Background completely blurred — a bookshelf with plants, "
            "a trailing pothos plant, a small succulent on the windowsill, "
            "warm light peeking around a blind, all out of focus. "
            "Wearing a plain navy blue cotton cardigan over a white T-shirt, "
            "visible chest and shoulders.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "Visible pores, no beauty filter, no retouching, no beauty mode. "
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
    print(f"CA Women Latina Personas V5 (UGC selfie mode) — nano-banana-2 → {OUT}\n")
    print("F1: 42, Venezuelan — Venice Beach canal path (outdoor) — selfie")
    print("F2: 45, Colombian mestiza — apartment bedroom morning (indoor) — selfie")
    print("F3: 38, Honduran Maya-mestiza — Oakland sidewalk (outdoor) — selfie")
    print("F4: 48, Cuban-American — home office plants window (indoor) — selfie\n")

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
