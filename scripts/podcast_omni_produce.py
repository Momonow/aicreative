import os, json, requests, pathlib, time, subprocess, re, sys, concurrent.futures
from dotenv import load_dotenv
load_dotenv("/Users/harry/aicreative/.env")
sys.path.insert(0, "/Users/harry/aicreative")
from elevenlabs_client import scribe_whisper_compat as scribe
TOKEN = os.environ["USEAPI_TOKEN"]; H = {"Authorization": f"Bearer {TOKEN}"}; EMAIL = "flowmomomedia@gmail.com"
# google-flow model: "omni-flash" (default) or "veo-3.1-lite-low-priority" (Ultra low-prio, free).
# Veo R2V allows referenceImage_1..3; duration must be 4/6/8 (dur_for already complies).
MODEL = os.environ.get("POD_MODEL", "omni-flash")
TAG = {"omni-flash": "", "veo-3.1-lite-low-priority": "_veo"}.get(MODEL, "_" + re.sub(r"[^a-z0-9]+", "", MODEL.split("-")[0]))
# Reference mode: omni-flash uses R2V (referenceImage_1); Veo locks the persona PNG as the
# literal first frame via I2V (startImage) — far better background hold for a talking head.
IS_VEO = MODEL.startswith("veo")
REF_PARAM = "startImage" if IS_VEO else "referenceImage_1"
ROOT = pathlib.Path("/Users/harry/aicreative/outputs/chowchilla_podcast")
BR = pathlib.Path("/Users/harry/aicreative/outputs/chowchilla_podcast_bright")
MD = pathlib.Path("/Users/harry/aicreative/outputs/chowchilla_podcast_personas")  # moody set

PERSONAS = {"B1":BR/"1.png","B2":BR/"2.png","B3":BR/"3.png","B4":BR/"4.png","B5":BR/"5.png","B6":BR/"6.png","B9":BR/"9.png",
            "M8":MD/"8.png"}  # moody #8 — weathered, headphones, condenser mic, dark cardigan, low-key light

# letter: (persona, tone, vernacular_text)
SCRIPTS = {
 "A": ("B6","fired up, urgent, real grown-woman conviction",
   "Real talk. If a guard or an officer sexually abused you in a California women's prison, I need you to hear me. Whether it was Chowchilla, CCWF, or CIW, you may qualify for significant potential compensation. Survivors from another California women's prison already won over a hundred million dollars. You don't need paperwork, you don't need proof, none of that. Most of these get handled without you ever stepping foot in a courtroom. You only pay if you win. It all stay private, just between you and the lawyers. Don't sleep on what could be yours. Tap that button and see if you qualify."),
 "B": ("B2","earnest, building conviction, like she's putting you on to something",
   "This is how women who was sexually abused in the California prisons may qualify for significant potential compensation. I know it sound wild. Stay with me. Survivors from another California women's prison just won over a hundred and sixteen million dollars. If you was sexually abused by a guard or an officer while you was locked up in Chowchilla, you may qualify too. Even if it happened years ago. Even if you never told a soul. Even if you never reported it. Tap that button and take the quiz to see if you qualify. It's free, and it's private."),
 "D": ("B1","authoritative but warm, urgent",
   "Attention. If you was sexually abused by a guard or an officer while you was locked up in a California women's prison, you need to hear this. Whether it was Chowchilla, CCWF, or CIW, the law is on your side now. You may qualify for significant potential compensation. This ain't no scam. Survivors from another California women's prison already won over a hundred and sixteen million dollars. Cases is being reviewed right now. You don't need a old report. You don't need your own lawyer. You don't even gotta set foot in a courtroom. And you pay nothing unless they win for you. Everything stay private, just between you and the attorneys. Take one minute. Tap that button and find out if you qualify."),
 "F": ("B3","righteous anger, fierce, fired up",
   "Those guards in Chowchilla was betting on one thing. That after they sexually abused us, we would be too ashamed to ever open our mouths. That we would carry it straight to our graves. They bet wrong. Women who was sexually abused inside the California prisons may qualify for significant potential compensation now. Survivors from another women's prison out here already won over a hundred million dollars for it. You don't need proof, or a old report, or none of that. The courts is finally making these places answer. You only pay if you win. It all stay private, just between you and the lawyers. After everything they took, this part is yours. Tap that button and see if you qualify."),
 "H": ("B4","warm, targeted, building intensity",
   "This is for you if a guard or an officer sexually abused you in a California women's prison. This is for you if it was Chowchilla, CCWF, or CIW. This is for you if you told yourself it wasn't that bad, or it was too long ago to matter. It was that bad, and it still matter. You may qualify for significant potential compensation. Survivors from another California women's prison already won over a hundred million dollars. You don't need proof, you don't need a report, and you don't gotta go to court. You don't pay unless they win. It stay private, just you and the lawyers. If any of this is landing for you, it ain't a coincidence. Tap that button and see if you qualify."),
 "I": ("B9","heavy, confronting, intimate, fired up",
   "If a guard ever came in your cell at night when you was locked up in Chowchilla, don't scroll past this. What he did to you was sexual abuse, even if you never once called it that. Women who lived through it in the California prisons may qualify for significant potential compensation. Survivors from another women's prison out here already won over a hundred million dollars. You don't need no proof, no old report, nothing like that. You only pay if you win. You don't even gotta go to court. It stay private, just between you and the lawyers, no matter how many years it's been. Take a minute. Tap the button. See if you qualify."),
 "M": ("B5","tender naming it plainly, then urgent",
   "What that guard did to you in prison has a name. It was sexual abuse. And if it happened to you inside Chowchilla, or any California women's prison, you may qualify for significant potential compensation. Survivors from another California women's prison already won over a hundred and sixteen million dollars. Cases like yours is being reviewed right now. You don't need proof. You don't need a report. You don't gotta set foot in court. You only pay if you win. Nobody gotta know but you and the lawyers. It don't matter how many years gone by. Take one minute, tap that button, and see if you qualify."),
 "K": ("M8","intimate, warm, sister-to-sister, then fired up",
   "Sis, listen. If a guard or an officer sexually abused you while you was locked up in a California women's prison, this is for you. Chowchilla, CCWF, CIW, it don't matter which one. What he did to you was sexual abuse, even if you never once called it that. And you may qualify for significant potential compensation. Survivors from another California women's prison already won over a hundred and sixteen million dollars. You don't need proof. You don't need a old report. You don't even gotta step foot in a courtroom. You only pay if you win. And it stay private, just between you and the lawyers. Don't let them win twice. Tap that button and see if you qualify."),
}

# Veo i2v is 8s-flat and drags on tiny lines, so the omni short-chunk strategy doesn't transfer.
# For Veo, group each script into fuller ~13-22-word beats (6s if <=14 words, else 8s) so every
# clip is well-filled at ~2.2-2.6 words/sec. Curated per letter for clean beat boundaries.
VEO_CHUNKS = {
 "K": [
   "Sis, listen. If a guard or an officer sexually abused you while you was locked up in a California women's prison",
   "This is for you. Chowchilla, CCWF, CIW, it don't matter which one",
   "What he did to you was sexual abuse, even if you never once called it that",
   "And you may qualify for significant potential compensation. Survivors from another California women's prison already won over a hundred and sixteen million dollars",
   "You don't need proof. You don't need a old report. You don't even gotta step foot in a courtroom",
   "You only pay if you win. And it stay private, just between you and the lawyers",
   "Don't let them win twice. Tap that button and see if you qualify",
 ],
}

def chunk_for(letter, text):
    if IS_VEO and letter in VEO_CHUNKS: return VEO_CHUNKS[letter]
    return chunk(text)

GAZE = "GAZE LOCK: she looks DIRECTLY into the camera lens the ENTIRE clip, steady, never drifting off to the side."
BODY = ("She stays seated in place and speaks into the podcast microphone with natural expressive life: alive "
        "eyes and brows, small hand gestures, nods, blinks. She does NOT lunge at the camera and does NOT sway. No smile.")
BG = ("BACKGROUND LOCK: keep the EXACT SAME background, room, wall, and lighting as in the reference image. "
      "Do NOT change, swap, or re-imagine the background — reproduce the identical setting from the reference "
      "in every shot, unchanging across the whole clip. Same place, same background, same framing the entire time.")

def build(dia, tone):
    return ("Vertical podcast close-up, framed IDENTICALLY from the first frame to the last. The camera is a "
        "completely locked-off tripod: no reframing, no settling, no drift, no zoom, no pan. The background is "
        "a FROZEN still photograph that never moves or changes; only her face and hands move. Keep the exact "
        "same scene and background as the reference image. She stays seated and speaks with natural expressive life: alive eyes "
        "and brows, small hand gestures, nods, blinks, no smile, does not lunge. She looks straight into the lens. "
        "VOICE: a weathered late-40s Black woman from South Central Los Angeles, low, raspy, fired up, real LA "
        "vernacular, NOT flat, NOT an announcer. TONE: "+tone+". Brisk delivery, about 2.4 words per second, no "
        "long pauses. She says ONLY this, verbatim, no extra or repeated words, then stops: \""+dia+"\" No on-screen text, no music.")

def chunk(text):
    parts = re.split(r'(?<=[.?!])\s+', text.strip()); out=[]
    for p in parts:
        p=p.strip().rstrip('.?!').strip()
        if not p: continue
        if len(p.split())<=13: out.append(p); continue
        # pack comma-clauses into <=13-word groups (don't isolate tiny fragments)
        cur=[]
        for c in re.split(r',\s*', p):
            c=c.strip()
            if not c: continue
            if len((" ".join(cur+[c])).split())<=13: cur.append(c)
            else:
                if cur: out.append(", ".join(cur))
                cur=[c]
        if cur: out.append(", ".join(cur))
    return out

def dur_for(dia):
    w=len(dia.split())
    if IS_VEO:
        return 6 if w<=14 else 8        # Veo i2v drags on tiny lines; no 4s (guardrail-prone). 6 or 8 only.
    return 4 if w<=6 else (6 if w<=10 else 8)

def split_dia(dia):
    ws=dia.split()
    if ',' in dia:
        i=dia.find(','); return dia[:i].strip(), dia[i+1:].strip()
    mid=len(ws)//2; return " ".join(ws[:mid]), " ".join(ws[mid:])

NUMCORE=set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion".split())
NUMGLUE={"a","and","point","oh"}
NUMCUR={"dollar","dollars","cent","cents","buck","bucks","grand","percent"}

def _prep(text):
    # Returns (words, hyset). Canonicalizes a transcript/line into comparable word tokens:
    #  - strips podcast reaction tokens (mm-hmm / mm-mm / uh-huh / ah-ah / hm-mm ... any nasal/vowel
    #    chain joined by hyphen/space) — never a real word, always trailing improv the trim removes;
    #  - folds benign colloquial variants Veo/Scribe swap ("got to"<->"gotta", "going to"<->"gonna",
    #    "want to"<->"wanna", "an"->"a") so they don't read as missing/extra words;
    #  - folds any NUMBER phrase ("a hundred and sixteen million dollars" / "$116 million" / "116
    #    million") to a single "#num#" token — Scribe renders spoken amounts as digits, which would
    #    otherwise break the subsequence match (clip-03 "$116 million" false-"missing").
    # hyset = word-indices whose source token carried a hyphen (false-start candidate, e.g. "pr-").
    text=re.sub(r"\b[mhaeiouy]+(?:[-\s][mhaeiouy]+)+\b"," ",text,flags=re.I)
    t=text.lower()
    t=re.sub(r"\bgot to\b","gotta",t); t=re.sub(r"\bgoing to\b","gonna",t)
    t=re.sub(r"\bwant to\b","wanna",t); t=re.sub(r"\ban\b","a",t)
    toks=re.findall(r"[a-z'\-]+|\d[\d,\.]*",t)
    cw=[re.sub(r"[^a-z']","",x) for x in toks]
    member=[bool(re.match(r"\d",toks[k])) or cw[k] in NUMCORE for k in range(len(toks))]
    chg=True                                              # grow runs over adjacent glue/currency
    while chg:
        chg=False
        for k in range(len(toks)):
            if member[k] or not cw[k]: continue
            if cw[k] in NUMGLUE or cw[k] in NUMCUR:
                if (k>0 and member[k-1]) or (k+1<len(toks) and member[k+1]):
                    member[k]=True; chg=True
    words=[]; hyset=set(); k=0
    while k<len(toks):
        if member[k]:
            while k+1<len(toks) and member[k+1]: k+=1
            words.append("#num#"); k+=1; continue
        if cw[k]:
            if "-" in toks[k]: hyset.add(len(words))
            words.append(cw[k])
        k+=1
    return words,hyset

def _prep_ts(ws):
    # Canonicalize a Scribe word list (each {word,start,end}) the SAME way as _prep, but KEEP
    # timestamps, so jumpcut can trim to the intended span even when Scribe renders the amount as
    # digits ("$116 million") or swaps got-to/gotta, an/a. Returns (canon_words, starts, ends),
    # number-runs folded to a single "#num#" spanning [first start, last end].
    items=[]; i=0; n=len(ws)
    while i<n:
        raww=(ws[i].get("word") or "").strip(); s=ws[i].get("start"); e=ws[i].get("end")
        if re.fullmatch(r"[mhaeiouy]+(?:[-\s][mhaeiouy]+)+", raww, flags=re.I):
            i+=1; continue                                       # podcast reaction token -> drop
        if re.search(r"\d", raww):
            items.append(("#d#", s, e)); i+=1; continue          # digit -> number-core placeholder
        cw=re.sub(r"[^a-z']","",raww.lower())
        nxt=re.sub(r"[^a-z']","",(ws[i+1].get("word") or "").lower()) if i+1<n else ""
        if cw in ("got","going","want") and nxt=="to":
            items.append(({"got":"gotta","going":"gonna","want":"wanna"}[cw], s, ws[i+1].get("end"))); i+=2; continue
        if cw=="an": cw="a"
        if cw: items.append((cw,s,e))
        i+=1
    member=[(it[0]=="#d#" or it[0] in NUMCORE) for it in items]
    chg=True
    while chg:
        chg=False
        for k in range(len(items)):
            if member[k] or not items[k][0]: continue
            if items[k][0] in NUMGLUE or items[k][0] in NUMCUR:
                if (k>0 and member[k-1]) or (k+1<len(items) and member[k+1]):
                    member[k]=True; chg=True
    words=[]; starts=[]; ends=[]; k=0
    while k<len(items):
        if member[k]:
            j=k
            while j+1<len(items) and member[j+1]: j+=1
            words.append("#num#"); starts.append(items[k][1]); ends.append(items[j][2]); k=j+1; continue
        words.append(items[k][0]); starts.append(items[k][1]); ends.append(items[k][2]); k+=1
    return words,starts,ends

def clean(text, dia):
    # Trailing/leading improv is NOT rejected here — the jump-cut assembler trims to the
    # intended span via Scribe word-timestamps, so paying to re-roll it is pure waste.
    # Reject ONLY defects that survive the trim: the line not fully spoken (missing), a false-start
    # fragment BETWEEN intended words ("pr- prove"), or a stutter inside the kept span.
    w,hy=_prep(text)
    intended,_=_prep(dia)
    intset=set(intended)
    wi=0; first=None; last=None                           # ordered subsequence match -> kept span
    for j,tok in enumerate(w):
        if wi<len(intended) and tok==intended[wi]:
            if first is None: first=j
            last=j; wi+=1
    if wi<len(intended): return False,"missing"           # whole line not spoken -> re-roll
    for j in hy:                                          # false-start ONLY if interior AND not a
        if first<j<last and w[j] not in intset:           # complete scripted word (lets "C-C-W-F"
            return False,"hyphen"                          # letter-spelling pass; trailing cutoffs trimmed)
    span=w[first:last+1]                                  # exactly what survives the trim
    for n in (1,2,3):                                     # mid-line stutter in kept span
        for i in range(len(span)-2*n+1):
            if span[i:i+n]==span[i+n:i+2*n]: return False,f"{n}gram"
    return True,"ok"

def upload(path, ctype="image/png"):
    with open(path,"rb") as f:
        r=requests.post(f"https://api.useapi.net/v1/google-flow/assets/{requests.utils.quote(EMAIL)}",headers={**H,"Content-Type":ctype},data=f.read(),timeout=180)
    m=r.json().get("mediaGenerationId"); return m.get("mediaGenerationId") if isinstance(m,dict) else m

def gen(out, dia, dur, mgid, tone, attempts=3):
    if out.exists() and out.stat().st_size>50000: return True
    for a in range(1,attempts+1):
        payload={"prompt":build(dia,tone),"model":MODEL,"aspectRatio":"portrait","duration":dur,
                 "count":1,"captchaRetry":3,"seed":(abs(hash(out.name))%9000)+a*31}
        payload[REF_PARAM]=mgid
        try:
            g=requests.post("https://api.useapi.net/v1/google-flow/videos",headers={**H,"Content-Type":"application/json"},json=payload,timeout=600)
            gj=g.json()
            if g.status_code==200 and gj.get("media"):
                tmp=f"/tmp/_p_{out.stem}.mp4"; open(tmp,"wb").write(requests.get(gj["media"][0]["videoUrl"],timeout=180).content)
                subprocess.run(["ffmpeg","-y","-i",tmp,"-vn","-ar","16000","-ac","1",f"/tmp/_p_{out.stem}.wav"],capture_output=True)
                txt=scribe(f"/tmp/_p_{out.stem}.wav",biased_keywords=["Chowchilla","CCWF","CIW"],language_code="en").get("text","")
                ok,why=clean(txt,dia)
                if ok: open(out,"wb").write(open(tmp,"rb").read()); print(f"  {out.name} CLEAN a{a}",flush=True); return True
                print(f"  {out.name} a{a} REJECT[{why}]  txt={txt!r}",flush=True)
            else:
                try: rs=gj["response"]["media"][0]["mediaMetadata"]["mediaStatus"].get("failureReasons")
                except Exception: rs=str(gj.get("error") or gj)[:70]
                print(f"  {out.name} a{a} GENFAIL {rs}",flush=True)
        except Exception as e: print(f"  {out.name} a{a} EXC {str(e)[:70]}",flush=True)
        time.sleep(6)
    return False

def do_chunk(args):
    i,dia,mgid,tone=args
    base=DIR/f"{i:02d}.mp4"; a_=DIR/f"{i:02d}a.mp4"; b_=DIR/f"{i:02d}b.mp4"
    if base.exists() and base.stat().st_size>50000: return
    if a_.exists() and b_.exists(): return
    if gen(base,dia,dur_for(dia),mgid,tone,attempts=3): return
    if IS_VEO or len(dia.split())<=6:
        # Veo chunks are already fuller beats — splitting makes draggy fragments. Just drop on fail.
        print(f"  !! {i:02d} clip won't clear after retries, NOT splitting (dropping): '{dia}'",flush=True); return
    d1,d2=split_dia(dia)
    print(f"  >> splitting {i:02d}: '{d1}' | '{d2}'",flush=True)
    gen(a_,d1,dur_for(d1),mgid,tone,attempts=2); gen(b_,d2,dur_for(d2),mgid,tone,attempts=2)

def jumpcut(files, dias, out):
    trimmed=[]
    for j,fn in enumerate(files):
        p=DIR/fn; wav=f"/tmp/_jc_{p.stem}.wav"
        subprocess.run(["ffmpeg","-y","-i",str(p),"-vn","-ar","16000","-ac","1",wav],capture_output=True)
        ws=[w for w in scribe(wav,biased_keywords=["Chowchilla"],language_code="en").get("segments",[{}])[0].get("words",[]) if w.get("start") is not None]
        D=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",str(p)],capture_output=True,text=True).stdout.strip())
        # Trim to the INTENDED span: subsequence-match the scripted line against the transcript,
        # cut at the first & last intended word -> drops leading junk AND trailing improv
        # (so we keep clips that clean() now accepts instead of paying to re-roll them).
        # Canonicalize BOTH sides (reaction strip + got-to/gotta + an/a + number-fold) so the match
        # survives Scribe's digit rendering ("$116 million") and benign word swaps.
        intended,_=_prep(dias[j]) if j < len(dias) else ([],set())
        cwords,starts,ends=_prep_ts(ws)
        # TIGHTEST-span subsequence match: when the line contains a repeated word (e.g. two
        # "you"s), a greedy first-match latches the EARLIEST occurrence and drags improv that
        # sits between it and the real line into the kept span (omni's "if you give rent, you
        # only pay if you win" left "give rent" in). Try every start index where the first
        # intended word matches, and keep the span that consumes the FEWEST transcript words.
        best=None  # (span_word_count, start_time, end_time)
        for s in range(len(cwords)):
            if not intended or cwords[s]!=intended[0]: continue
            wi=0; en_t=None; consumed=0
            for k in range(s,len(cwords)):
                consumed=k-s+1
                if wi<len(intended) and cwords[k]==intended[wi]:
                    en_t=ends[k]; wi+=1
                    if wi==len(intended): break
            if wi==len(intended) and en_t is not None and starts[s] is not None and (best is None or consumed<best[0]):
                best=(consumed, starts[s], en_t)
        if best:
            st, en = best[1], best[2]
        else:                                        # match failed -> full speech span fallback
            st=ws[0]["start"] if ws else 0.0; en=ws[-1]["end"] if ws else D
        st=max(0.0,st-0.03); en=min(D,en+0.05)
        t=DIR/f"_jt{j:02d}.mp4"
        # NOTE: the Veo "Veo" watermark (bottom-right) is removed in ONE ratio-preserving pass at
        # the very end (center-crop 675x1200 -> scale 720x1280, uniform 16/15x, no stretch), not here.
        subprocess.run(["ffmpeg","-y","-ss",f"{st:.3f}","-i",str(p),"-t",f"{en-st:.3f}","-vf","scale=720:1280,fps=24,setsar=1","-c:v","libx264","-preset","fast","-crf","18","-c:a","aac","-ar","44100","-b:a","192k",str(t)],capture_output=True,check=True)
        trimmed.append(t)
    lst=DIR/"_jc.txt"; lst.write_text("".join(f"file '{t.resolve()}'\n" for t in trimmed))
    raw=DIR/"_jcraw.mp4"; subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(raw)],capture_output=True,check=True)
    meas=subprocess.run(["ffmpeg","-i",str(raw),"-af","loudnorm=I=-16:TP=-1.5:print_format=json","-f","null","-"],capture_output=True,text=True)
    mm=re.search(r"\{[^{}]*\"input_i\"[^{}]*\}",meas.stderr.replace("\n"," ")); gn=0.0
    if mm:
        try: gn=-16.0-float(json.loads(mm.group(0))["input_i"])
        except Exception: gn=0.0
    subprocess.run(["ffmpeg","-y","-i",str(raw),"-af",f"volume={gn:.2f}dB,alimiter=limit=0.891","-c:v","copy","-c:a","aac","-b:a","192k",out],capture_output=True,check=True)

if __name__=="__main__":
    letter=sys.argv[1]; persona,tone,text=SCRIPTS[letter]
    DIR=ROOT/f"{letter}_{persona}{TAG}_la"; DIR.mkdir(parents=True,exist_ok=True)
    print(f"    model={MODEL}  ref={REF_PARAM}  dir={DIR.name}",flush=True)
    chunks=chunk_for(letter,text)
    print(f"=== {letter} on {persona}: {len(chunks)} chunks ===",flush=True)
    mgid=upload(PERSONAS[persona])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(do_chunk,[(i,d,mgid,tone) for i,d in enumerate(chunks)]))
    files=[]; dias=[]
    for i in range(len(chunks)):
        if (DIR/f"{i:02d}.mp4").exists():
            files.append(f"{i:02d}.mp4"); dias.append(chunks[i])
        elif (DIR/f"{i:02d}a.mp4").exists() and (DIR/f"{i:02d}b.mp4").exists():
            d1,d2=split_dia(chunks[i]); files+=[f"{i:02d}a.mp4",f"{i:02d}b.mp4"]; dias+=[d1,d2]
        elif (DIR/f"{i:02d}a.mp4").exists():
            d1,_=split_dia(chunks[i]); files.append(f"{i:02d}a.mp4"); dias.append(d1)
        else: print(f"  !! chunk {i:02d} MISSING (gave up)",flush=True)
    print(f"  assembling {len(files)} clips",flush=True)
    out=str(ROOT/f"{letter}{TAG}_full.mp4")
    if files: jumpcut(files,dias,out); print(f"DONE {letter} -> {out}",flush=True)
    else: print(f"DONE {letter} -> NO CLIPS",flush=True)
