"""Re-export + re-download the 7 Submagic storytime projects AFTER manual caption edits.
Triggers a fresh export on each existing project, waits for the NEW render, downloads it.

Run only AFTER editing captions in the Submagic app.
  python scripts/jdc_submagic_redownload.py            # all 7
  python scripts/jdc_submagic_redownload.py A E         # only those keys
"""
import sys, time, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # scripts/ on path
import submagic_client as sm

# key -> (project_id, output_path)
PROJECTS = {
    "A": ("26ec8fd9-773d-4321-8238-cc6144e3d1ba", "outputs/illinois_jdc_storytime_a_b1/story_a_b1_final_submagic_lewis.mp4"),
    "B": ("b938c24d-d461-4f72-8774-f0a5a2007d7e", "outputs/illinois_jdc_storytime_b_b2/story_b_b2_final_submagic_hormozi3.mp4"),
    "C": ("922f421e-95ea-4d27-9594-69ea670a4e2a", "outputs/illinois_jdc_storytime_c_b5/story_c_b5_final_submagic_hormozi1.mp4"),
    "E": ("a9a3aa94-b0b1-48cd-bb2f-89767d86e5e1", "outputs/illinois_jdc_storytime_e_b14/story_e_b14_final_submagic_lewis.mp4"),
    "F": ("ae9c5cbf-517b-4248-b707-767c70abc00a", "outputs/illinois_jdc_storytime_f_b7/story_f_b7_final_submagic_hormozi4.mp4"),
    "G": ("15c4216e-a5f3-429f-bc00-baf9a1485391", "outputs/illinois_jdc_storytime_g_b11/story_g_b11_final_submagic_hormozi2.mp4"),
    "H": ("ba9e418b-b113-46e6-afde-b95994764655", "outputs/illinois_jdc_storytime_h_b10/story_h_b10_final_submagic_hormozi3.mp4"),
}


def reexport_download(key, pid, out_path, timeout=1800, every=10):
    p0 = sm.get(pid)
    old_url = p0.get("downloadUrl"); old_upd = p0.get("updatedAt")
    code, resp = sm.export(pid)
    print(f"[{key}] export HTTP {code}: {str(resp)[:120]}", flush=True)
    t0 = time.time(); saw_progress = False; retried = False
    while time.time() - t0 < timeout:
        p = sm.get(pid); st = p.get("status"); dl = p.get("downloadUrl"); upd = p.get("updatedAt")
        if st in ("exporting", "preparing", "processing", "transcribing"):
            saw_progress = True
        if st == "failed":
            return key, "FAILED", str(p.get("error"))
        # accept a download only once we've seen a fresh render (progress OR url/timestamp changed)
        fresh = saw_progress or (dl and dl != old_url) or (upd and upd != old_upd)
        if st == "completed" and dl and fresh:
            Path(out_path).write_bytes(requests.get(dl, timeout=600).content)
            return key, "success", f"{out_path} ({Path(out_path).stat().st_size//1024} KB)"
        if st == "completed" and not fresh and not retried and time.time() - t0 > 20:
            code, resp = sm.export(pid)   # render didn't kick; nudge once
            print(f"[{key}] re-trigger export HTTP {code}", flush=True)
            retried = True
        time.sleep(every)
    return key, "TIMEOUT", pid


def main():
    only = [a.upper() for a in sys.argv[1:]]
    keys = [k for k in PROJECTS if not only or k in only]
    for k in keys:
        pid, out = PROJECTS[k]
        print(reexport_download(k, pid, out), flush=True)


if __name__ == "__main__":
    main()
