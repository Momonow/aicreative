#!/usr/bin/env python3
"""Rebuild the STACKED edit with SILENT looped listeners (Poyo mouth-closed loops), reusing the
already word-trimmed talkers. doc TOP / survivor BOTTOM; CTA full-frame.
"""
import subprocess, sys
from pathlib import Path
T = Path("outputs/depo_interview/trimmed")
L = Path("outputs/depo_interview/listen_loops")
E = Path("outputs/depo_interview/edits")
DOC_LOOP = L/"doc_listen_loop.mp4"; SURV_LOOP = L/"surv_listen_loop.mp4"

# (talker_trimmed, persona, is_cta)
BEATS = [
 ("doc_talk_1","doc",False),("surv_talk_1","surv",False),("doc_talk_2","doc",False),
 ("surv_talk_2","surv",False),("surv_talk_3","surv",False),("doc_talk_3","doc",False),
 ("surv_talk_4","surv",False),("doc_talk_4","doc",False),("surv_talk_5","surv",False),
 ("surv_talk_6","surv",False),("doc_cta","doc",True),
]
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",str(p)],capture_output=True,text=True).stdout.strip())

segs=[]
for i,(talker,persona,cta) in enumerate(BEATS):
    tf = T/f"{talker}.mp4"; d = dur(tf); seg = T/f"st_{i:02d}.mp4"
    if cta:
        subprocess.run(["ffmpeg","-y","-i",str(tf),"-vf","scale=720:1280,setsar=1,fps=30",
            "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
            str(seg),"-loglevel","error"])
    else:
        loop = SURV_LOOP if persona=="doc" else DOC_LOOP   # doc talks -> surv listens (bottom); surv talks -> doc listens (top)
        if persona=="doc":
            top_in, bot_in = str(tf), str(loop); top_loop, bot_loop = False, True; audmap="0:a"
        else:
            top_in, bot_in = str(loop), str(tf); top_loop, bot_loop = True, False; audmap="1:a"
        cmd=["ffmpeg","-y"]
        if top_loop: cmd += ["-stream_loop","-1"]
        cmd += ["-i",top_in]
        if bot_loop: cmd += ["-stream_loop","-1"]
        cmd += ["-i",bot_in,"-filter_complex",
            "[0:v]crop=720:640:0:110,setsar=1,fps=30[t];[1:v]crop=720:640:0:110,setsar=1,fps=30[b];[t][b]vstack[v]",
            "-map","[v]","-map",audmap,"-t",f"{d:.2f}",
            "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
            str(seg),"-loglevel","error"]
        subprocess.run(cmd)
    segs.append(seg); print(f"seg {i:02d} {talker} ({d:.2f}s)")

lst=Path("/tmp/st_rebuild.txt"); lst.write_text("".join(f"file '{s.resolve()}'\n" for s in segs))
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),
    "-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
    str(E/"stacked_v2.mp4"),"-loglevel","error"])
# audio unify (static gain + limiter)
import json
info=subprocess.run(["ffmpeg","-i",str(E/"stacked_v2.mp4"),"-af","loudnorm=I=-16:TP=-1.5:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
ii=[l for l in info.splitlines() if '"input_i"' in l]
gain=-16.0-float(ii[0].split(':')[1].strip().strip(',').strip('"')) if ii else 0.0
subprocess.run(["ffmpeg","-y","-i",str(E/"stacked_v2.mp4"),"-af",f"volume={gain:.2f}dB,alimiter=limit=0.89:asc=1",
    "-c:v","copy","-c:a","aac","-b:a","192k",str(E/"stacked_v2_norm.mp4"),"-loglevel","error"])
print("stacked_v2_norm:", dur(E/"stacked_v2_norm.mp4"),"s  gain",round(gain,2))
