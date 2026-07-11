#!/usr/bin/env python3
"""TRUE always-both-panes stacked with Grok SILENT listeners. SURVIVOR on TOP, doc on BOTTOM.
Listeners are real 10s Grok clips trimmed to each beat (no loops). Faces raised in each pane.
CTA full-frame. Veo watermark delogo'd on full-frame CTA.
"""
import subprocess, sys
from pathlib import Path
T=Path("outputs/depo_interview/trimmed"); G=Path("outputs/depo_interview/clips_grok"); E=Path("outputs/depo_interview/edits")
DOC_LISTEN=[G/"doc_listen_grok_1.mp4", G/"doc_listen_grok_2.mp4"]
SURV_LISTEN=[G/"surv_listen_grok_1.mp4", G/"surv_listen_grok_2.mp4"]
# crop windows (from 720x1280): raise faces. survivor face higher -> start y=40; doc -> y=90
SURV_CROP="crop=720:640:0:40,setsar=1,fps=30"
DOC_CROP="crop=720:640:0:150,setsar=1,fps=30"
BEATS=[("doc_talk_1","doc"),("surv_talk_1","surv"),("doc_talk_2","doc"),("surv_talk_2","surv"),
 ("surv_talk_3","surv"),("doc_talk_3","doc"),("surv_talk_4","surv"),("doc_talk_4","doc"),
 ("surv_talk_5","surv"),("surv_talk_6","surv"),("doc_cta","cta")]
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",str(p)],capture_output=True,text=True).stdout.strip())
segs=[]; di=0; si=0
for i,(talker,kind) in enumerate(BEATS):
    tf=T/f"{talker}.mp4"; d=dur(tf); seg=T/f"gk_{i:02d}.mp4"
    if kind=="cta":
        subprocess.run(["ffmpeg","-y","-i",str(tf),"-vf","scale=720:1280,setsar=1,fps=30,delogo=x=646:y=1222:w=72:h=48",
            "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",str(seg),"-loglevel","error"])
    else:
        # SURVIVOR TOP, DOC BOTTOM. talker audio kept; listener muted.
        if kind=="doc":   # doc talks (bottom), survivor listens (top)
            top=SURV_LISTEN[si%2]; si+=1; bot=tf; audmap="1:a"; top_crop=SURV_CROP; bot_crop=DOC_CROP
        else:             # survivor talks (top), doc listens (bottom)
            top=tf; bot=DOC_LISTEN[di%2]; di+=1; audmap="0:a"; top_crop=SURV_CROP; bot_crop=DOC_CROP
        subprocess.run(["ffmpeg","-y","-i",str(top),"-i",str(bot),"-filter_complex",
            f"[0:v]{top_crop}[t];[1:v]{bot_crop}[b];[t][b]vstack[v]",
            "-map","[v]","-map",audmap,"-t",f"{d:.2f}",
            "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",str(seg),"-loglevel","error"])
    segs.append(seg); print(f"seg {i:02d} {talker} {kind} {d:.2f}s")
lst=Path("/tmp/gk.txt"); lst.write_text("".join(f"file '{s.resolve()}'\n" for s in segs))
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),"-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",str(E/"stacked_grok.mp4"),"-loglevel","error"])
info=subprocess.run(["ffmpeg","-i",str(E/"stacked_grok.mp4"),"-af","loudnorm=I=-16:TP=-1.5:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
ii=[l for l in info.splitlines() if '"input_i"' in l]; gain=-16.0-float(ii[0].split(':')[1].strip().strip(',').strip('"')) if ii else 0.0
subprocess.run(["ffmpeg","-y","-i",str(E/"stacked_grok.mp4"),"-af",f"volume={gain:.2f}dB,alimiter=limit=0.89:asc=1","-c:v","copy","-c:a","aac","-b:a","192k",str(E/"stacked_grok_norm.mp4"),"-loglevel","error"])
subprocess.run(["ffmpeg","-y","-i",str(E/"stacked_grok_norm.mp4"),"-c:v","libx264","-crf","27","-preset","veryfast","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k",str(E/"stacked_grok_web.mp4"),"-loglevel","error"])
print("stacked_grok:", dur(E/"stacked_grok_norm.mp4"),"s")
