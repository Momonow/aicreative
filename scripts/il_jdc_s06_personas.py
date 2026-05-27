"""
Script 06 — Generate 5 Black male personas (outdoor, 9:16) for IL JDC script.
Uses useapi.net Google Flow nano-banana-pro for high-quality portrait images.

Character: 36-year-old man, dark-brown skin, outside settings, UGC selfie style,
reflective/serious expression matching the tone of a personal testimony.

5 persona variations (setting + wardrobe + look):
  A: Urban sidewalk, brick building exterior, dark hoodie
  B: Park / green space, trees behind him, casual bomber jacket
  C: Front steps of a brownstone / apartment building exterior, sitting on steps
  D: Suburban street, residential neighborhood, quiet afternoon
  E: Community/church building exterior steps, institutional stone behind him
"""
import os, sys, time, requests
from pathlib import Path

USEAPI_TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {USEAPI_TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/il_jdc_script06_personas")
OUT.mkdir(exist_ok=True)

MODEL = "nano-banana-pro"

PERSONAS = [
    {
        "id": "A",
        "setting": "urban_sidewalk",
        "prompt": """Portrait photo. Man, deep dark-brown complexion, mid-30s, medium-athletic build, short natural low-cut hair with a clean fade. Standing outside on a city sidewalk, leaning slightly against a worn brick building exterior wall — the brick is mildly out of focus behind him, soft depth of field. Overcast midday light, diffused and flat, no dramatic shadows. Dark charcoal zip-up hoodie, clean dark jeans. Holding phone at chest-level in selfie style, lens slightly below his eye level looking up at him. Direct, unguarded gaze straight into the camera lens — serious, heavy, contemplative. Not angry. The expression of someone who carries something. Natural authentic face: visible pores on cheeks and nose, slight under-eye darkness, fine lines at the corners of his eyes, natural lip texture, slight facial asymmetry. No beauty mode, no filter, no skin smoothing, no retouching, no studio lighting. Looks like a real UGC phone selfie. 9:16 vertical portrait.""",
    },
    {
        "id": "B",
        "setting": "park_greenery",
        "prompt": """Portrait photo. Man, rich dark-brown complexion, mid-30s, medium build, natural short twist-out hair, slight beard stubble. Standing outdoors in a public park — green grass and blurred tree trunks behind him, leaves softly out of focus, late afternoon light warm but overcast. Olive-green bomber jacket, plain white tee underneath, dark jogger pants. Phone held straight, selfie angle, camera at mid-chest level tilted up slightly toward his face. Eyes direct on the lens, expression serious and steady — a quiet gravity, not performing emotion, just present. Authentic face: natural skin texture, pores visible, slight weathering around the eyes, no makeup, natural brow shape. Phone-camera quality, slight natural vignette. No studio, no beauty filter, no retouching. Real-looking UGC portrait. 9:16 vertical.""",
    },
    {
        "id": "C",
        "setting": "brownstone_steps",
        "prompt": """Portrait photo. Man, medium dark-brown complexion, mid-30s, stocky-medium build, close-cropped natural hair, clean low fade, small neat goatee. Sitting on the concrete front steps of a city brownstone apartment building exterior — worn stone steps, black iron railing, brick front in soft focus behind him. Flat grey-sky afternoon light. Navy blue crewneck sweatshirt, dark pants. Elbows resting on knees, phone held forward at slightly upward angle — natural selfie posture for someone sitting. Gaze locked straight into the camera, expression heavy and thoughtful — the face of someone who has processed a lot of pain and is now calmly owning it. Authentic portrait: visible skin texture and pores, under-eye shadow, slight asymmetry of features, natural lip color. No retouching, no studio, no filter. Genuine UGC selfie look. 9:16 vertical portrait.""",
    },
    {
        "id": "D",
        "setting": "residential_street",
        "prompt": """Portrait photo. Man, deep brown complexion with warm undertones, mid-30s, lean-medium build, short natural hair with a taper fade, no beard. Standing outside on a quiet residential suburban street — modest houses and parked cars softly blurred far behind him, afternoon overcast sky. Black puffer vest over a heather grey long-sleeve shirt. Holding phone with one hand at stomach height tilted upward slightly, natural selfie angle. Looking directly into the camera with a steady, unsmiling, honest expression — calm and purposeful, not vacant. Natural face: visible pores, slight redness in the cheeks and nose bridge, natural brow hair, soft eye bags, authentic texture. Shot looks like a front-facing phone camera in flat daylight. No studio light, no ring light catch, no beauty filter. Real-person UGC aesthetic. 9:16 vertical portrait.""",
    },
    {
        "id": "E",
        "setting": "church_building_steps",
        "prompt": """Portrait photo. Man, dark-brown skin, mid-30s, medium-heavyset build, very short natural hair almost a shaved head, full short beard, well-groomed. Standing outside on the wide stone steps of a large institutional building — could be a church, community center, or courthouse. Aged stone columns or facade slightly out of focus behind him, overcast flat afternoon light. Dark forest-green pullover fleece, dark pants. Phone held at chest level, camera tilted slightly upward. Gaze directly into the lens, expression resolute and reflective — the kind of face that has made peace with something hard. Authentic skin: visible pores, some uneven skin tone, natural beard texture, no retouching. Looks like a real selfie taken outside before or after a meeting. No studio, no filter. Genuine UGC portrait. 9:16 vertical.""",
    },
]


def generate_persona(p):
    # Check if at least one variation already exists
    first_path = OUT / f"persona_{p['id']}_{p['setting']}_v1.jpg"
    if first_path.exists():
        print(f"  Persona {p['id']}: already exists, skipping")
        return p["id"], [str(first_path)]

    payload = {
        "prompt": p["prompt"],
        "model": MODEL,
        "aspectRatio": "9:16",
    }
    print(f"  Persona {p['id']} ({p['setting']}): submitting …", flush=True)
    r = requests.post(
        "https://api.useapi.net/v1/google-flow/images",
        headers=HEADERS,
        json=payload,
        timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Persona {p['id']} failed: {r.status_code} {r.text[:300]}")

    data = r.json()

    # nano-banana-pro returns 4 variations in data["media"]
    # Each: media[i]["image"]["generatedImage"]["fifeUrl"]
    media_list = data.get("media", [])
    if not media_list:
        raise RuntimeError(f"Persona {p['id']}: no media in response: {list(data.keys())}")

    saved_paths = []
    for i, m in enumerate(media_list, start=1):
        fife_url = m.get("image", {}).get("generatedImage", {}).get("fifeUrl", "")
        media_id = m.get("image", {}).get("generatedImage", {}).get("mediaGenerationId", "")
        if not fife_url:
            print(f"    Persona {p['id']} v{i}: no fifeUrl, skipping")
            continue
        out_path = OUT / f"persona_{p['id']}_{p['setting']}_v{i}.jpg"
        r2 = requests.get(fife_url, timeout=60)
        r2.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(r2.content)
        size = out_path.stat().st_size
        # Save media_id for use as video anchor
        mid_path = OUT / f"persona_{p['id']}_{p['setting']}_v{i}_mediaId.txt"
        mid_path.write_text(media_id)
        print(f"  Persona {p['id']} v{i}: saved → {out_path.name} ({size//1024}KB)")
        saved_paths.append(str(out_path))

    return p["id"], saved_paths


def poll_image_job(job_id, pid, timeout=300, interval=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(
            f"https://api.useapi.net/v1/google-flow/jobs/{job_id}",
            headers=HEADERS,
            timeout=30,
        )
        if r.status_code != 200:
            time.sleep(interval)
            continue
        data = r.json()
        status = data.get("status", "")
        if status == "completed":
            resp = data.get("response", {})
            media = resp.get("media", [{}])
            url = media[0].get("imageUrl", "") if media else ""
            if url:
                return url
            raise RuntimeError(f"Persona {pid} completed but no imageUrl: {data}")
        elif status == "failed":
            raise RuntimeError(f"Persona {pid} FAILED: {data}")
        else:
            print(f"    Persona {pid}: {status} …", flush=True)
            time.sleep(interval)
    raise TimeoutError(f"Persona {pid} timed out after {timeout}s")


if __name__ == "__main__":
    print(f"Generating 5 personas → {OUT}")
    print(f"Model: {MODEL} | AspectRatio: 9:16 portrait\n")

    results = {}
    for p in PERSONAS:
        try:
            pid, paths = generate_persona(p)
            results[pid] = paths
        except Exception as e:
            print(f"✗ Persona {p['id']} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/5")
    for pid in sorted(results):
        for path in results[pid]:
            print(f"  Persona {pid}: {path}")
