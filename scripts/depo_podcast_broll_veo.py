"""Generate the two missing human-context B-roll clips for the #1419 podcast clone."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kie_client import download, generate_veo  # noqa: E402


OUT_DIR = Path("outputs/depo_podcast_1419_clone/broll")
MODEL = "veo3_fast"

SHOTS = {
    "06_recurring_treatment_calendar": (
        "Vertical 9:16 photoreal documentary B-roll. Close overhead view of an "
        "adult woman's hands at a kitchen table turning through several consecutive "
        "pages of a paper calendar. A few dates on each month are circled with small "
        "generic clinic appointment marks, suggesting a recurring treatment history "
        "over time. Natural daylight, restrained handheld movement, realistic paper "
        "texture, calm serious tone. No medication brand, no readable names, no "
        "personal information, no added graphics, no captions, no watermark. One "
        "continuous shot with no cuts."
    ),
    "07_reviewing_old_medical_records": (
        "Vertical 9:16 photoreal documentary B-roll. An ordinary middle-aged woman "
        "sits at a modest kitchen table and quietly sorts through an older folder of "
        "medical records, appointment cards, and envelopes. Frame primarily her "
        "hands, the folder, and a partial side profile while she pauses on one page "
        "and continues reviewing. Natural window light, subtle handheld camera, "
        "realistic unpolished home setting, calm thoughtful emotion. All document "
        "text is too small or softly out of focus to read; no personal information, "
        "no added graphics, no captions, no watermark. One continuous shot with no "
        "cuts."
    ),
}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, prompt in SHOTS.items():
        dest = OUT_DIR / f"{slug}.mp4"
        if dest.exists() and dest.stat().st_size > 100_000:
            print(f"SKIP {dest}")
            continue

        print(f"GENERATE {slug}", flush=True)
        result = generate_veo(
            prompt=prompt,
            aspect_ratio="9:16",
            resolution="720p",
            model=MODEL,
        )
        if result.get("status") != "success" or not result.get("urls"):
            raise RuntimeError(f"{slug} failed: {result}")
        download(result["urls"][0], str(dest))


if __name__ == "__main__":
    main()
