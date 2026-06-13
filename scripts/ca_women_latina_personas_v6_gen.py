"""
CA Women's Prison — 4 DISTINCT Latina Personas v6 (ages 50–55)
UGC SELFIE MODE — phone held at arm's length, slight overhead angle, candid
2 outdoor + 2 indoor | fresh locations not used in v1–v5
Heritages not used before: Ecuadorian, Bolivian/Aymara, Chilean, Costa Rican
useapi.net nano-banana-2 | 9:16
"""
import os, requests, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_women_latina_personas_v6")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_CWL6_F1",
        "label": "Latina 52 — Ecuadorian mestiza — outdoor CA apartment front steps — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, slightly above eye level — "
            "casual outdoor selfie on the front steps of an apartment building, unstaged. "
            "Subject looks slightly upward toward the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "52-year-old Ecuadorian-American woman. "
            "FACE SHAPE: soft oval — evenly proportioned, gently wide at the cheekbones, "
            "tapering to a rounded softly defined chin. Slight fullness in the cheeks, "
            "forehead broad and smooth except for natural age lines. "
            "SKIN: warm medium olive-brown — a rich tawny-gold tone, warm neutral undertone, "
            "NOT pale, NOT dark. Age-appropriate texture: "
            "soft horizontal forehead lines, deepening smile lines around the mouth, "
            "slight looseness at the jaw, visible pores, natural uneven tone, faint dark circles. "
            "HAIR: shoulder-length straight dark brown hair with generous scattered grey throughout — "
            "salt-and-pepper effect, not dyed, slightly coarse, worn down and loose, "
            "parted slightly off-center, a few face-framing strands. "
            "EYES: warm medium-dark brown — gentle and steady, slight heaviness of the upper lid, "
            "subtle crow's feet at the outer corners, looking slightly upward at the lens. "
            "MOUTH: medium lips, natural neutral-rose tone, a flat closed mouth — "
            "composed, neither smiling nor frowning.\n\n"
            "SETTING: outdoors on the concrete front steps of a modest California stucco apartment building — "
            "worn painted metal railing to the side, a row of apartment mailboxes slightly blurred "
            "in the background, quiet residential street and parked cars soft behind her. "
            "Morning light — cool diffuse overcast California morning, even light on her face. "
            "Wearing a plain burgundy v-neck sweater, visible clavicle and shoulders.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL6_F2",
        "label": "Latina 54 — Bolivian Aymara heritage — indoor apartment dining table — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, angled very slightly downward — "
            "a casual seated selfie at a kitchen or dining table. "
            "Subject looks directly up into the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "54-year-old Bolivian-American woman with Aymara indigenous heritage. "
            "FACE SHAPE: wide, low and broad — a distinctively wide flat forehead, "
            "very prominent broad cheekbones set high and wide, broad compact nose with a low bridge "
            "and slightly flared nostrils, round compact chin. Face is wide relative to its height. "
            "SKIN: deep warm bronze-brown — a rich medium-dark warm tone with reddish-brown undertone, "
            "NOT dark, NOT copper — the deeper bronze of indigenous Andean heritage. "
            "Age: deep forehead creases, strong smile lines, slight jowl softness, "
            "sun weathering around the temples, age spots, no makeup whatsoever. "
            "HAIR: thick coarse dark brown hair heavily threaded with grey — "
            "NOT a neat style — worn loose and somewhat tousled, falls past the shoulders, "
            "natural density and slight frizz, no dye, substantial weight. "
            "EYES: very dark near-black brown, slightly wide-set, slightly small and deep-set under "
            "prominent broad brows, direct calm gaze upward at the lens. "
            "MOUTH: medium-wide full lips, natural deep rose-brown tone, "
            "flat relaxed and calm — resting neutral.\n\n"
            "SETTING: indoors at a small modest California apartment dining table — "
            "afternoon warm natural light from a nearby window falling across her face from the side. "
            "Background completely blurred — a simple chair, a folded piece of laundry on the table "
            "edge, and a trailing houseplant on a shelf, all out of focus. "
            "Wearing a plain dark navy blue long-sleeve shirt, visible neck.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL6_F3",
        "label": "Latina 50 — Chilean mestiza — outdoor neighborhood park bench — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, approximately eye level — "
            "a casual outdoor park selfie, she stopped for a moment and took a photo. "
            "Subject looks directly at the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "50-year-old Chilean-American woman with European-Mapuche mestiza heritage. "
            "FACE SHAPE: longer oval — slightly narrow forehead, higher cheekbones, "
            "straight jaw, gently pointed chin. Refined, angular but not harsh. "
            "SKIN: warm light-medium fair olive — a creamy warm tone, NOT pale white, "
            "NOT dark — a Southern European-inflected Latina olive, warmed by sun. "
            "Age-appropriate: light forehead creases, moderate smile lines, "
            "faint broken capillaries at the nose, slight under-eye softness, no makeup, no filter. "
            "HAIR: naturally wavy medium-to-dark brown hair with significant silver-grey mixed in — "
            "waves are natural, slightly textured, falls past the collarbone, "
            "worn loose or loosely behind one ear, NOT blow-dried. "
            "EYES: light warm hazel-brown — greenish-brown in warm light, "
            "medium-sized, slight droop at the outer corners giving a soft relaxed expression, "
            "looking directly and evenly into the lens. "
            "MOUTH: medium lips, natural muted rose tone, composed and neutral — "
            "a quiet natural expression, not performing.\n\n"
            "SETTING: outdoors on a wooden park bench in a California neighborhood park — "
            "late afternoon dappled light filtering through mature oak trees behind her, "
            "golden warm light on her face and hair, blurred green lawn and another bench "
            "far in the background, soft bokeh from tree canopy overhead. "
            "Wearing a casual olive-green quilted vest over a plain white long-sleeve shirt, "
            "visible neck and collarbones.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CWL6_F4",
        "label": "Latina 53 — Costa Rican mestiza — indoor apartment entryway hallway — selfie mode",
        "prompt": (
            "UGC phone selfie photograph in 9:16 vertical. "
            "The phone is held at arm's length, approximately eye level — "
            "a quick selfie just inside the front door of her apartment. "
            "Subject looks directly at the lens. Authentic candid feel, NOT a studio portrait.\n\n"
            "53-year-old Costa Rican-American woman with mestiza heritage. "
            "FACE SHAPE: heart-shaped — wider forehead tapering to a soft rounded-pointed chin, "
            "high cheekbones, gentle fullness in the mid-cheek area. "
            "SKIN: warm caramel-olive — a medium warm tan tone, golden-brown undertone, "
            "NOT dark, NOT light — classic warm Central American mestiza complexion. "
            "Age: soft forehead creases, prominent smile lines, beginning jowl softness, "
            "slight texture around the nose and cheeks, a few small age spots at the temple, "
            "visible pores, no makeup, no filter. "
            "HAIR: thick natural 2C-3A curls, rich dark brown heavily threaded with silver — "
            "the silver is concentrated at the temples and part, with dark brown beneath, "
            "curls fall to mid-neck, some frizz, very much alive and real, not blow-dried or straightened. "
            "EYES: warm medium brown, slightly wide-set, alert and direct, "
            "slight bags underneath — lived-in eyes, looking directly at the lens. "
            "MOUTH: medium-full lips, natural warm neutral-rose tone, "
            "a very small composed closed-mouth expression — the beginning of a natural resting face, "
            "not performing anything.\n\n"
            "SETTING: indoors in a modest California apartment entryway or narrow hallway — "
            "warm overhead light from a ceiling fixture. "
            "Background completely blurred — a coat hook on the wall with a canvas tote bag "
            "and a light jacket hanging, the corner of a doorframe, a small rug on the floor, "
            "all soft and out of focus. "
            "Wearing a plain heather-grey zip-up hoodie, front zipper halfway up, "
            "visible neck.\n\n"
            "Photoreal UGC phone selfie. Ordinary everyday woman — NOT glamour, NOT celebrity. "
            "No makeup, no filter, no retouching, no beauty mode. "
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
    print(f"CA Women Latina Personas V6 (UGC selfie mode, ages 50–55) — nano-banana-2 → {OUT}\n")
    print("F1: 52, Ecuadorian mestiza          — front steps CA apartment (outdoor) — selfie")
    print("F2: 54, Bolivian/Aymara heritage    — apartment dining table (indoor) — selfie")
    print("F3: 50, Chilean mestiza             — neighborhood park bench (outdoor) — selfie")
    print("F4: 53, Costa Rican mestiza         — apartment entryway hallway (indoor) — selfie\n")

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
