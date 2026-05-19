"""Poll 2 already-submitted Seedance task IDs (03, 18) that survived the
killed batch and are still THROTTLED on useapi's queue. Download when they
complete. Reuses the patched useapi_client._poll (3h timeout, handles poll-time 429).

These tasks are holding our account's queue depth — recovering them frees
slots for the rest of the batch.
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from useapi_client import _poll, download

OUT_DIR = Path("outputs/illinois_jdc_power_broll")

IN_FLIGHT = {
    "03_peephole_observation": "user:2478-runwayml:harry@momomedia.io-task:eb423ffd-a5e2-40f5-9ec9-a7c06a2d3d6b",
    "18_jdc_exterior_night":   "user:2478-runwayml:harry@momomedia.io-task:4515f50a-f9e0-477a-b3ee-3b8ee2187997",
}


def recover(slug, task_id):
    out = OUT_DIR / f"{slug}.mp4"
    if out.exists():
        return slug, "exists", str(out)
    print(f"[{slug}] polling existing task...", flush=True)
    try:
        r = _poll(task_id, label=f"recover[{slug}]")
    except Exception as e:
        return slug, "exception", str(e)[:400]
    if r["status"] != "success" or not r["urls"]:
        return slug, "failed", str(r.get("raw"))[:400]
    download(r["urls"][0], str(out))
    return slug, "success", str(out)


def main():
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(recover, s, tid): s for s, tid in IN_FLIGHT.items()}
        for f in as_completed(futures):
            s = futures[f]
            try:
                _, status, info = f.result()
                print(f"[{s}] {status}: {info}", flush=True)
            except Exception as e:
                print(f"[{s}] EXC: {e}", flush=True)


if __name__ == "__main__":
    main()
