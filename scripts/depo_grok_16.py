#!/usr/bin/env python3
"""First 16s stacked from GROK clips: survivor TOP (tight centered close-up), doc BOTTOM.
Beat1: doc asks (surv listens top). Beat2: surv answers (doc listens bottom). Grok = clean audio."""
import subprocess
from pathlib import Path
G=Path("outputs/depo_interview/clips_grok"); T=Path("outputs/depo_interview/trimmed"); E=Path("outputs/depo_interview/edits")
# tight centered close-ups: fill the face in each 720x640 pane
SURV_CROP="crop=520:462:80:260,scale=720:640,setsar=1,fps=30"   # survivor zoomed ~1.38x, centered
DOC_CROP ="crop=560:498:90:190,scale=720:640,setsar=1,fps=30"   # doc matched close-up
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",str(p)],capture_output=True,text=True).stdout.strip())
def seg(name, top, bot, audmap, d):
    out=T/f"g16_{name}.mp4"
    subprocess.run(["ffmpeg","-y","-i",str(top),"-i",str(bot),"-filter_complex",
        f"[0:v]{SURV_CROP}[t];[1:v]{DOC_CROP}[b];[t][b]vstack[v]",
        "-map","[v]","-map",audmap,"-t",f"{d:.2f}",
        "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",str(out),"-loglevel","error"])
    return out
dd=dur(G/"gtalk_doc_1.mp4"); sd=dur(G/"gtalk_surv_1.mp4")
# beat1: top surv listens, bottom doc talks (audio bottom=1:a)
a=seg("A", G/"surv_listen_grok_1.mp4", G/"gtalk_doc_1.mp4", "1:a", dd)
# beat2: top surv talks, bottom doc listens (audio top=0:a)
b=seg("B", G/"gtalk_surv_1.mp4", G/"doc_listen_grok_1.mp4", "0:a", sd)
lst=Path("/tmp/g16.txt"); lst.write_text(f"file '{a.resolve()}'\nfile '{b.resolve()}'\n")
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),"-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",str(E/"grok16.mp4"),"-loglevel","error"])
# normalize + web
info=subprocess.run(["ffmpeg","-i",str(E/"grok16.mp4"),"-af","loudnorm=I=-16:TP=-1.5:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
ii=[l for l in info.splitlines() if '"input_i"' in l]; gain=-16.0-float(ii[0].split(':')[1].strip().strip(',').strip('"')) if ii else 0.0
subprocess.run(["ffmpeg","-y","-i",str(E/"grok16.mp4"),"-af",f"volume={gain:.2f}dB,alimiter=limit=0.89:asc=1","-c:v","libx264","-crf","26","-preset","veryfast","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k",str(E/"grok16_web.mp4"),"-loglevel","error"])
print("grok16:", dur(E/"grok16_web.mp4"),"s")
