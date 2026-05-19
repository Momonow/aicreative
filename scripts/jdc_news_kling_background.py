"""Generate 2 background-only images of the Chicago L-tracks setting (NO PEOPLE)
to use as the `element_setting` Kling element-ref.

Kling needs 2-4 imgs per element so we make 2 slightly different angles of the
same location.

Output: outputs/illinois_jdc_news_eltracks/reference/setting_1.png + setting_2.png
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openai_image import generate_image

OUT_DIR = Path("outputs/illinois_jdc_news_eltracks/reference")

COMMON = (
    "ABSOLUTELY NO PEOPLE in the scene. NO pedestrians, NO figures, NO silhouettes "
    "of people. Empty sidewalk. Photoreal news b-roll location photograph, real "
    "daylight, NOT studio. Late-afternoon overcast lighting, cool urban palette, "
    "subtle El-pattern shadows on the ground. Documentary handheld feel, shot on "
    "a phone or small mirrorless. Slight shallow depth-of-field. "
    "NO on-screen text, NO captions, NO watermarks, NO logos."
)

VARIATIONS = {
    "setting_1": (
        "Wide angle ground-level photograph of a sidewalk underneath the Chicago "
        "Loop elevated train tracks ('the L'). Massive black-painted riveted steel "
        "girders and lattice beams overhead form a structural ceiling. Large "
        "riveted black steel support columns rise from the sidewalk on both sides. "
        "Polished brick and concrete sidewalk underfoot. In the deep background, "
        "older granite-clad and red-brick Loop-era buildings line the far side of "
        "a downtown street, soft-focus. A faint yellow Chicago taxi cab visible at "
        "the curb in the distance. " + COMMON
    ),
    "setting_2": (
        "Medium shot ground-level photograph from a slightly different angle of the "
        "SAME sidewalk underneath the Chicago Loop elevated train tracks ('the L') "
        "— same black-painted riveted steel girders and lattice beams overhead, "
        "same riveted black steel support column visible to the side, same polished "
        "brick-and-concrete sidewalk. Background shows the same row of Loop-era "
        "granite-clad and red-brick buildings in soft focus, with another yellow "
        "Chicago taxi at the curb. Slightly tighter framing than the first, with "
        "the steel column more prominent at frame right. " + COMMON
    ),
}


def gen(slug, prompt):
    out = OUT_DIR / f"{slug}.png"
    if out.exists():
        return slug, "exists", str(out)
    print(f"[{slug}] generating...", flush=True)
    r = generate_image(
        prompt=prompt,
        out_path=str(out),
        size="1024x1536",
        quality="medium",
        n=1,
    )
    if r["status"] != "success":
        return slug, "failed", r["raw"].get("error", "unknown")
    return slug, "success", r["paths"][0]


def main():
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(gen, s, p): s for s, p in VARIATIONS.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                _, status, info = f.result()
                print(f"[{s}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
