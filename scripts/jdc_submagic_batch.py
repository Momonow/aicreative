"""Subtitle-only via Submagic on the 7 finished 9:16 storytime ads.
Varied template pick; proper-noun dictionary for facilities. Skip-if-exists.
Output: <slug>/<stem>_submagic_<template>.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import submagic_client

DICT = ["Illinois", "Cook County", "St. Charles", "Harrisburg", "Joliet", "Los Angeles"]

# (slug, stem, template) — template = my random pick, varied across the set
JOBS = [
    ("illinois_jdc_storytime_a_b1",  "story_a_b1_final",  "Lewis"),
    ("illinois_jdc_storytime_b_b2",  "story_b_b2_final",  "Hormozi 3"),
    ("illinois_jdc_storytime_c_b5",  "story_c_b5_final",  "Hormozi 1"),
    ("illinois_jdc_storytime_e_b14", "story_e_b14_final", "Lewis"),
    ("illinois_jdc_storytime_f_b7",  "story_f_b7_final",  "Hormozi 4"),
    ("illinois_jdc_storytime_g_b11", "story_g_b11_final", "Hormozi 2"),
    ("illinois_jdc_storytime_h_b10", "story_h_b10_final", "Hormozi 3"),
]


def run(slug, stem, template):
    inp = Path(f"outputs/{slug}/{stem}.mp4")
    tag = template.lower().replace(" ", "")
    out = Path(f"outputs/{slug}/{stem}_submagic_{tag}.mp4")
    if out.exists() and out.stat().st_size > 50000:
        return stem, "cached", str(out)
    try:
        submagic_client.caption(str(inp), str(out), template=template, dictionary=DICT)
        ok = out.exists() and out.stat().st_size > 50000
        return stem, ("success" if ok else "NO_OUTPUT"), f"{template} -> {out}"
    except Exception as e:
        return stem, "FAILED", f"{template}: {e}"


def main():
    only = set(sys.argv[1:])
    jobs = [j for j in JOBS if not only or j[0] in only or j[1] in only]
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(run, *j): j[1] for j in jobs}
        for f in as_completed(futs):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
