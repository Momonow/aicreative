#!/usr/bin/env python3
"""Animate the 20 future Depo b-roll stills and upload them into the AdMachin Depo Provera
B-Roll DB. Text-heavy documents get a deterministic ffmpeg slow push-in (keeps text crisp);
human/scene shots get Grok i2v. Skip-if-exists on the local clip; state file tracks uploads.
Run: .venv/bin/python scripts/depo_broll_future_animate_upload.py [--no-upload]
"""
import sys, json, argparse, subprocess, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kie_client as kie
from admachin_client import upload_broll_clip

STILLS = Path("outputs/depo_interview/broll_future")
CLIPS = Path("outputs/depo_interview/broll_future_clips"); CLIPS.mkdir(parents=True, exist_ok=True)
STATE = CLIPS / "uploaded.json"
TORT = "e15c60bd-95c2-47b9-9730-c29fb5325461"
DEPO = "9cfb5b76-1dd3-4e07-b037-2dda178ac266"

# (still_name, title, category, tags, kind, grok_motion)
GM = "Quiet, no talking, no voices, faint room ambience."
ZM = "slow gentle push-in, document stays still and text stays sharp"
ITEMS = [
 ("A1_neuro_model","Neurosurgeon points at a brain model","medical",["meningioma","surgery","consult"],"grok","The surgeon gestures at the brain model, the patient nods slightly. "+GM),
 ("A2_surgical_marking","Marking the scalp before brain surgery","medical",["surgery","preop"],"grok","The gloved hand finishes drawing the surgical marking on the scalp. "+GM),
 ("A3_mri_compare","Before and after brain MRI comparison","medical",["scan","mri","surgery"],"grok","A hand gestures between the two MRI scans on the monitor. "+GM),
 ("A4_neuro_rehab","Neuro rehab after brain surgery","medical",["recovery","rehab"],"grok","The woman takes a careful step as the therapist steadies her. "+GM),
 ("A5_postop_meds","Post-op medications pill organizer","medical",["recovery","medication"],"grok","A hand sets a pill bottle down beside the organizer, small motion. "+GM),
 ("B1_shot_record","Depo-Provera injection record card","depo",["depo","records"],"zoom",ZM),
 ("B2_pharmacy_handoff","Pharmacist hands over Depo-Provera box","depo",["depo","pharmacy"],"grok","The pharmacist extends the Depo-Provera box across the counter. "+GM),
 ("B3_chart_depo","Medical chart — Depo-Provera injection history","depo",["depo","records"],"zoom",ZM),
 ("B4_clinic_checkin","Checking in at the clinic front desk","depo",["clinic","checkin"],"grok","The woman hands the appointment card to the receptionist. "+GM),
 ("C1_paper_form","Filling out a paper claim form — Meningioma","process",["claim","form","meningioma"],"grok","The hand writes on the form, pen moving. "+GM),
 ("D1_bmj_study","BMJ 2024 study — progestogens and meningioma","credibility",["study","bmj","evidence"],"zoom",ZM),
 ("D2_bmj_stat","Study stat — medroxyprogesterone 5.6x meningioma risk","credibility",["study","evidence"],"zoom",ZM),
 ("D3_mdl_filing","Depo-Provera MDL No. 3140 court filing","credibility",["legal","mdl","lawsuit"],"zoom",ZM),
 ("D4_label_warning","Depo-Provera label — Meningioma warning","credibility",["depo","warning","label"],"zoom",ZM),
 ("D6_package_insert","Depo-Provera insert — Meningioma safety info","credibility",["depo","warning","insert"],"zoom",ZM),
 ("E1_scar_mirror","Touching the surgical scar in the mirror","emotional",["recovery","scar"],"grok","She gently touches the scar, a slow reflective moment. "+GM),
 ("E2_hair_cover","Styling hair to cover the scar","emotional",["recovery","scar"],"grok","She parts and smooths her hair over the scar at the mirror. "+GM),
 ("E3_legal_notice","Reading a legal notice at the kitchen table","emotional",["legal","claim"],"grok","She reads the letter, a slight worried shift, turns the page. "+GM),
 ("E4_hug_family","Hugging her child at home","emotional",["family","support"],"grok","They hold the hug, a small comforting sway. "+GM),
 ("E5_waiting_alone","Alone in the hospital waiting room","emotional",["worry","waiting"],"grok","She shifts slightly in the chair, looks down, a quiet moment. "+GM),
]

def zoom_clip(still, out):
    subprocess.run(["ffmpeg","-y","-loop","1","-i",str(still),
        "-f","lavfi","-t","8","-i","anullsrc=r=48000:cl=stereo",
        "-t","8","-r","30","-vf",
        "scale=1440:2560,zoompan=z='min(zoom+0.00035,1.12)':d=240:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30,setsar=1",
        "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-shortest",
        str(out),"-loglevel","error"])

def grok_clip(still, out, motion):
    url = kie.upload_file(str(still))
    payload = {"model":"grok-imagine/image-to-video","input":{"image_urls":[url],"prompt":motion,
               "mode":"normal","duration":"8","resolution":"720p","aspect_ratio":"9:16"}}
    r = requests.post(kie.JOBS_CREATE, headers=kie.HEADERS, json=payload)
    tid = (r.json().get("data") or {}).get("taskId")
    if not tid: print("  FAIL create", r.json()); return False
    res = kie._poll_jobs(tid, f"Grok {out.stem}")
    if res.get("status") == "success" and res.get("urls"):
        kie.download(res["urls"][0], out); return True
    print("  FAIL grok", str(res.get("raw"))[:150]); return False

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-upload", action="store_true")
    a = ap.parse_args()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for name, title, cat, tags, kind, motion in ITEMS:
        still = STILLS / f"{name}.png"
        clip = CLIPS / f"{name}.mp4"
        if not clip.exists():
            if not still.exists(): print("MISSING still", name); continue
            ok = zoom_clip(still, clip) if kind == "zoom" else grok_clip(still, clip, motion)
            if kind == "zoom": ok = clip.exists()
            print(("anim done " if clip.exists() else "anim FAIL ")+name)
        if a.no_upload or name in state: continue
        try:
            c = upload_broll_clip(str(clip), title=title, project_id=TORT, subproject_id=DEPO,
                                  platform="ai_video", clip_category=cat, tags=tags, note=title)
            cid = c.get("id") if isinstance(c, dict) else None
            state[name] = cid; STATE.write_text(json.dumps(state, indent=1))
            print(f"  UPLOADED {name} -> {cid}")
        except Exception as e:
            print(f"  UPLOAD FAIL {name}: {type(e).__name__} {e}")
    print("ALL DONE"); print(json.dumps(state, indent=1))

if __name__ == "__main__":
    main()
