"""Validate the FREE google-flow veo-3.1-lite-low-priority path on one b14 clip."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from googleflow_client import upload_asset, generate_veo, download

HOST = "outputs/illinois_jdc_storytime_bed/reference/bed_b14.png"
OUT = Path("outputs/illinois_jdc_storytime_e_b14/flowtest_clip01.mp4")
OUT.parent.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "He is lying back in bed talking into his phone, filming a quiet selfie confession. "
    "GAZE: soft intimate eye contact straight into the phone lens, with an occasional brief glance away then back. "
    "Warm dark-brown eyes, OPEN, the SAME color throughout. "
    "BODY: small natural head shifts on the pillow, slow blinks, weary; a slow swallow before he starts. "
    "VOICE: low weary young man, late 20s, quiet and heavy, slightly hoarse. "
    "TONE: heavy, bracing himself to say it out loud; the very end lifts with a faint flicker of hope. "
    "SPEED: about 2.5 words per second, slow and deliberate. "
    "AUDIO CRITICAL: clear and fully audible at a close intimate volume right into the phone mic, NOT whispered. "
    'PRONUNCIATION: say "SA\'ed" as the letters "ess-ay-d", NOT "sad"; "juvie" = "JOO-vee"; "Illinois" = "ill-uh-NOY". '
    "DIALOGUE LOCK: English only. Say ONLY the words in SPOKEN DIALOGUE, in order, no fillers, no extra or trailing words, stop after \"it\". "
    "NO on-screen text, NO captions, NO subtitles, NO watermark. "
    'SPOKEN DIALOGUE (verbatim, stop after final word): "A guard SA\'ed me at Illinois juvie. This is my story, and how I might finally be getting compensated for it."'
)

print("uploading bed_b14 to google-flow...", flush=True)
mgid = upload_asset(HOST)
print("mgid:", mgid, flush=True)
print("generating on veo-3.1-lite-low-priority (FREE, ultra-low-priority — may be slow)...", flush=True)
r = generate_veo(PROMPT, image_mgid=mgid, duration=8, seed=101)
print("status:", r["status"], flush=True)
if r["status"] == "success":
    download(r["urls"][0], str(OUT))
    print("SAVED:", OUT, flush=True)
else:
    print("RAW:", str(r["raw"])[:400], flush=True)
