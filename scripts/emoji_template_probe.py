"""Caption a short test clip through several Submagic templates to find which animate emojis.
Output: outputs/_emoji_probe/<template>.mp4
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import submagic_client as sm

SRC = "/tmp/emoji_test_src.mp4"
OUT = Path("outputs/_emoji_probe"); OUT.mkdir(parents=True, exist_ok=True)
TEMPLATES = ["Hormozi 1", "Hormozi 2", "Hormozi 4", "Hormozi 5", "Beast", "Ali", "Iman", "David"]
DICT = ["Illinois", "Cook County"]


def run(tpl):
    tag = tpl.lower().replace(" ", "")
    out = OUT / f"{tag}.mp4"
    if out.exists() and out.stat().st_size > 50000:
        return tpl, "cached"
    try:
        sm.caption(SRC, str(out), template=tpl, dictionary=DICT)
        return tpl, "ok" if out.exists() else "NO_OUTPUT"
    except Exception as e:
        return tpl, f"FAIL {e}"


def main():
    only = sys.argv[1:]
    tpls = [t for t in TEMPLATES if not only or t.lower().replace(" ", "") in [o.lower() for o in only]]
    with ThreadPoolExecutor(max_workers=4) as ex:
        for f in as_completed({ex.submit(run, t): t for t in tpls}):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
