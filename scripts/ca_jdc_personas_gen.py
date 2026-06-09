"""
CA JDC — 4 California Black Male Personas
Ages 29–39 | 2 outdoor + 2 indoor California locations
useapi.net nano-banana-pro | 9:16
"""
import os, requests, time, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/ca_jdc_personas")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_CA_M1",
        "label": "Outside — Venice Beach Boardwalk — Close-up — 31yo",
        "prompt": (
            "Portrait photograph of a 31-year-old man, medium-dark brown skin tone, close-up shot "
            "framing from chest to top of head, standing on the Venice Beach boardwalk in Los Angeles. "
            "Short taper fade haircut, neat trimmed stubble beard about 4 days growth, direct steady "
            "gaze straight into the camera lens, mouth closed and neutral, slight tension around the "
            "eyes like he's holding something heavy. "
            "Wearing a plain white or light grey crew-neck t-shirt. "
            "Natural bright California afternoon sunlight, warm golden overhead light on skin, "
            "slight squint from the sun. "
            "Background slightly out of focus — concrete boardwalk surface, blurred silhouettes "
            "of distant people, a basketball backboard visible at the upper edge, pale blue "
            "Pacific Ocean sky in the far distance. "
            "Visible pores, natural skin texture, slight under-eye darkness, faint sun-worn texture "
            "on cheeks and forehead, no filter, no retouching, no beauty mode, no skin smoothing. "
            "Looks like a candid real phone portrait taken on a warm California afternoon. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CA_M2",
        "label": "Outside — South LA Suburban Sidewalk / Stucco House — Medium Close-up — 35yo",
        "prompt": (
            "Portrait photograph of a 35-year-old man, deep brown skin tone, medium close-up shot "
            "framing from mid-torso to top of head, standing on a residential sidewalk in front of "
            "a stucco California home in South Los Angeles. "
            "Mid-fade haircut, full short beard about one inch, evenly groomed, calm direct "
            "expression, eyes looking directly into the lens, jaw relaxed, mouth closed. "
            "Wearing a plain dark olive or charcoal zip-up hoodie, collar up slightly. "
            "Natural flat overcast Southern California daylight, even soft light on face, "
            "no harsh shadows. "
            "Background slightly out of focus — white stucco house exterior, a mature palm tree "
            "at the corner, concrete driveway edge, a section of chain-link fence, a parked "
            "car bumper at the edge of frame, working-class residential street feel. "
            "Visible pores, natural skin texture, slight lip dryness, under-eye shadow, "
            "faint skin unevenness, no filter, no retouching, no beauty mode, no skin smoothing. "
            "Feels like a genuine candid phone portrait taken on a South LA residential street. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CA_M3",
        "label": "Inside — Modest Apartment Living Room — Close-up — 29yo",
        "prompt": (
            "Portrait photograph of a 29-year-old man, medium-dark brown skin tone, close-up shot "
            "framing from shoulders to top of head, standing in the living room of a modest "
            "California apartment. "
            "Short natural fade haircut, very light 3-day stubble, direct gaze into the camera, "
            "thoughtful serious expression, mouth closed, slight tension in the brow, eyes "
            "slightly tired. "
            "Wearing a plain dark navy or black t-shirt. "
            "Natural afternoon light filtering through horizontal mini blinds creating soft "
            "parallel light bars across the background, warm subdued indoor light falling "
            "on face from the side. "
            "Background slightly out of focus — low sectional couch with a plain grey cushion, "
            "a small worn coffee table, simple off-white painted wall, a few everyday items "
            "on the table, lived-in domestic space that feels real and unstaged. "
            "Visible pores, natural skin texture, faint under-eye darkness, slight forehead "
            "shine from indoor warmth, no filter, no retouching, no beauty mode, no skin smoothing. "
            "Looks like a candid phone portrait taken inside a real apartment on a regular afternoon. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_CA_M4",
        "label": "Inside — Modest California Home Kitchen — Medium Close-up — 38yo",
        "prompt": (
            "Portrait photograph of a 38-year-old man, deep brown skin tone, medium close-up shot "
            "framing from chest to top of head, standing in the kitchen of a modest California home. "
            "Short low wave cut, full beard approximately 1.5 to 2 inches, slightly unkempt at the "
            "edges, natural texture, calm steady gaze directly into the lens, serious neutral "
            "expression, jaw set. "
            "Wearing a plain dark burgundy or charcoal long-sleeve shirt. "
            "Natural window light coming from the side, warm-cool indoor daylight mix, "
            "slight shadow falling across one side of face. "
            "Background slightly out of focus — white or beige subway tile backsplash, "
            "plain wooden cabinet fronts, a laminate kitchen counter edge, a small potted "
            "herb plant on the windowsill, everyday modest California home kitchen. "
            "Visible pores, natural skin texture, visible beard texture and grey flecks, "
            "under-eye shadow, faint skin unevenness, no filter, no retouching, no beauty mode, "
            "no skin smoothing. "
            "Feels like a real candid phone portrait taken inside a home kitchen. "
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
    print(f"CA JDC — 4 California Black Male Personas (nano-banana-pro) → {OUT}\n")
    print("M1: Venice Beach boardwalk | M2: South LA stucco sidewalk")
    print("M3: Apartment living room | M4: Home kitchen\n")

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
