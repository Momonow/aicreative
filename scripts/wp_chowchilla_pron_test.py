"""Chowchilla pronunciation experiment on Grok — short 6s single-speaker clips, each a different
respelling/lock. Judge by transcribing WITHOUT the biased keyword (raw phonetic proxy) + by ear.
Anchor: respondent_a (single clear speaker). Line: "My sister was locked up in {W}."
"""
import pathlib, requests
from kie_client import upload_file, generate_grok

OUT = pathlib.Path("outputs/wp_voxpop/pron"); OUT.mkdir(parents=True, exist_ok=True)
url = upload_file("outputs/wp_voxpop/reference/respondent_a.png")

LOCK = (" Pronunciation: 'Chowchilla' is a California town/prison, said as three English syllables — "
        "chow (rhymes with 'cow') + chill + uh — stress the MIDDLE syllable, one fluid word, never Spanish.")

# label -> (word-as-written-in-line, include_descriptive_lock)
VARIANTS = {
 "1_norm_lock":   ("Chowchilla", True),
 "2_norm_nolock": ("Chowchilla", False),
 "3_hyphCaps":    ("Chow-CHILL-uh", False),
 "4_hyphLow":     ("chow-chill-uh", False),
 "5_spaced":      ("chow chill uh", False),
 "6_hyphCaps_lock":("Chow-CHILL-uh", True),
}

BASE = ("Single woman talking straight to camera, close selfie, clean clear audio, one speaker only, "
        "natural conversational pace.")

for label, (word, withlock) in VARIANTS.items():
    dst = OUT / f"{label}.mp4"
    if dst.exists():
        print(f"[skip] {label}"); continue
    prompt = BASE + (LOCK if withlock else "") + (
        "\nDIALOGUE LOCK: English only, say ONLY this line verbatim and stop: "
        f"\"My sister was locked up in {word}.\"\nNo on-screen text.")
    print(f"[gen] {label}  word={word!r} lock={withlock}")
    r = generate_grok(prompt, image_urls=[url], duration="6", resolution="720p", aspect_ratio="9:16")
    if r.get("urls"):
        dst.write_bytes(requests.get(r["urls"][0], timeout=300).content)
        print(f"[done] {label}")
    else:
        print(f"[FAIL] {label}", str(r.get("raw"))[:200])
print("PRON TEST DONE")
