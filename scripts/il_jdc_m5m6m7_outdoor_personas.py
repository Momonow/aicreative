"""
IL JDC — 3 Black Male Outdoor Personas (M5, M6, M7)
Ages 31-39 | Unique outdoor locations | useapi.net nano-banana-pro | 9:16
M6 has longer beard.
"""
import os, requests, time, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("USEAPI_TOKEN", "user:2478-GVIbsJwTLOJXBFuSQRV3a")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
OUT = Path("outputs/jdc_personas_outdoor")
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    {
        "id": "persona_M5",
        "label": "Outside - Urban Rooftop - Close-up - 33yo",
        "prompt": (
            "Portrait photograph of a 33-year-old Black American man, close-up shot framing "
            "from chest to top of head, standing on an urban residential rooftop. "
            "Short low fade haircut, very light 3-day stubble, calm direct gaze straight into "
            "the lens, mouth closed and neutral. "
            "Wearing a plain dark olive or charcoal zip-up jacket, collar up slightly. "
            "Natural overcast daylight — soft, even light on face with no harsh shadows. "
            "Background slightly out of focus — rooftop gravel surface, low brick parapet wall, "
            "blurred city rooftops and grey sky in the distance. Authentic Chicago residential "
            "neighborhood rooftop feel, not a penthouse. "
            "Visible pores, natural skin texture, slight under-eye shadow, faint fine lines, "
            "no filter, no retouching, no beauty mode, no skin smoothing, no airbrushing. "
            "Looks like a candid phone photo taken by someone who just climbed up to the roof. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_M6",
        "label": "Outside - Neighborhood Basketball Court - Medium Close-up - 38yo - Longer Beard",
        "prompt": (
            "Portrait photograph of a 38-year-old Black American man, medium close-up shot "
            "framing from mid-torso to top of head, standing near the edge of an outdoor "
            "neighborhood basketball court. "
            "Short taper fade haircut, FULL LONGER BEARD approximately 2.5 to 3 inches — "
            "dense, full growth, slightly unkempt at the edges, natural wave and texture, "
            "flecks of grey near the chin. Direct steady gaze into the lens, serious neutral "
            "expression, jaw set. "
            "Wearing a dark navy or dark grey crew-neck sweatshirt. "
            "Natural afternoon daylight from the side, warm-cool mix, slight shadows on face. "
            "Background slightly out of focus — chain-link fence, faded asphalt, the edge of "
            "a basketball backboard at the top corner, urban trees behind the fence. "
            "Feels like a real neighborhood park court in Chicago's South or West Side. "
            "Visible pores, natural skin texture, under-eye shadow, slight skin unevenness, "
            "no filter, no retouching, no beauty mode, no skin smoothing. "
            "Looks like a genuine outdoor candid phone portrait. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
    {
        "id": "persona_M7",
        "label": "Outside - Industrial Side Street / Brick Wall - Close-up - 35yo",
        "prompt": (
            "Portrait photograph of a 35-year-old Black American man, close-up shot framing "
            "from shoulders to top of head, standing in front of a worn industrial brick wall "
            "on a side street. "
            "Mid-fade haircut, neatly trimmed short beard about half an inch, calm serious "
            "expression, eyes directly into the lens, slight tension in the brow. "
            "Wearing a plain black or dark burgundy long-sleeve shirt. "
            "Natural flat daylight, slightly overcast, no dramatic shadows. "
            "Background slightly out of focus — aged red brick wall with faint paint remnants "
            "or old faded signage, cracked sidewalk edge, urban alley or side-street feel. "
            "Not glamorous — looks like the side of a warehouse or old commercial building "
            "in a working-class Chicago neighborhood. "
            "Visible pores, natural skin texture, faint under-eye darkness, slight lip dryness, "
            "no filter, no retouching, no beauty mode, no skin smoothing. "
            "Feels like a real phone portrait taken outside, not a studio shoot. "
            "9:16 vertical portrait, photo-realistic."
        ),
    },
]


def generate(p):
    pid = p["id"]
    out_path = OUT / f"{pid}.jpg"
    if out_path.exists() and out_path.stat().st_size > 50_000:
        print(f"  {pid}: exists ({out_path.stat().st_size//1024}KB), skipping")
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

    # save all variants
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
        print(f"  {pid}_v{i+1}: saved {vpath.stat().st_size//1024}KB  mediaId: {mid}")

    if saved:
        shutil.copy(saved[0], out_path)

    print(f"✓ {pid}: {out_path}  [{p['label']}]  ({len(saved)} variants)")
    return pid, str(out_path)


if __name__ == "__main__":
    print(f"Generating 3 outdoor Black male personas (nano-banana-pro) → {OUT}\n")
    print("M5: Urban rooftop | M6: Basketball court (longer beard) | M7: Industrial brick wall\n")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(generate, p): p["id"] for p in PERSONAS}
        for fut in as_completed(futs):
            pid = futs[fut]
            try:
                pid, path = fut.result()
                results[pid] = path
            except Exception as e:
                print(f"✗ {pid} ERROR: {e}")

    print(f"\nCompleted: {len(results)}/3")
    for pid in sorted(results):
        print(f"  {pid}: {results[pid]}")
