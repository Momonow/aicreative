"""Upload the Depo campaign product B-roll set to AdMachin and write native generation fields.
REST multipart upload (POST /brolls/clips/upload) then PATCH the Creative-Studio gen columns:
  image_generation_model = "poyo/gpt-image-2"  (provider/model format)
  video_generation_model = "omni-flash-useapi" (BARE id)
  *_prompt = free text
pv1 was already uploaded as row #80 (test) -> PATCH it in place. Run once.
"""
import os, json, uuid, requests

PAT = os.popen("grep -E '^ADMACHIN_PAT=' .env | cut -d= -f2- | tr -d ' '").read().strip()
BASE = "https://admachin.com/api/v1"
PROJ = "e15c60bd-95c2-47b9-9730-c29fb5325461"; SUB = "9cfb5b76-1dd3-4e07-b037-2dda178ac266"
IMG_MODEL = "poyo/gpt-image-2"; VID_MODEL = "omni-flash-useapi"
IMG_SFX = " | gpt-image-2 i2i from real Depo-Provera photo ref; vertical 9:16 2K; photoreal documentary product frame; faithful Pfizer/Depo-Provera label; muted clinical light"
VID_SFX = " | omni-flash i2v (useapi google-flow, startImage, 8s, audio stripped); subtle documentary motion, product/label kept exact, no new text/logos/watermark"

# slug: (title, image_prompt, video_prompt)
CLIPS = {
 "pv1_vial_tray": ("Depo-Provera vial + syringe on clinic tray", "The Depo-Provera vial standing on a stainless steel clinic tray beside a capped syringe and an alcohol swab, vertical framing, product centered.", "Very slow push-in across the clinic tray; the vial stays still."),
 "pv2_box_counter": ("Depo-Provera box + vial on pharmacy counter", "The Depo-Provera box lying on a pharmacy counter beside a small glass vial, vertical top-down-ish angle.", "Slow drift over the counter; product stays still."),
 "pv3_injection": ("Depo-Provera injection into arm", "A nurse giving the Depo-Provera pre-filled syringe injection into a woman's upper arm, gloved hand, vertical framing, product label visible.", "The gloved hand slowly depresses the plunger, the injection completing into the arm."),
 "pv4_box_hand": ("Depo-Provera box held in pharmacy aisle", "A hand holding the Depo-Provera box up in a pharmacy, shelves soft behind, vertical framing.", "The hand holds the box steady with a tiny tremor; slow push-in; shelves soft behind."),
 "pv5_vial_hand": ("Gloved hand lifting Depo-Provera vial", "A gloved hand picking up the Depo-Provera vial from a clinic tray, vertical close framing.", "The gloved hand slowly lifts the vial from the tray."),
 "pv6_vial_macro": ("Depo-Provera vial macro close-up", "Extreme vertical close-up of the standing Depo-Provera vial, label sharp, blurred clinic background.", "Very slow push-in on the vial; label stays sharp."),
 "pv7_box_upright": ("Depo-Provera box upright on counter", "A Depo-Provera box standing upright on a clean white pharmacy counter, front label facing camera, vertical centered framing.", "Very slow push-in toward the box on the counter; product stays still."),
 "pv8_box_eyelevel": ("Depo-Provera box held at eye level", "A hand holding the Depo-Provera box up at eye level in a pharmacy aisle, shelves soft behind, vertical framing.", "The hand holds the box steady with a tiny tremor; slow push-in; shelves soft behind."),
 "pv9_vial_tall": ("Depo-Provera vial on clinic tray", "A single Depo-Provera vial standing tall and centered on a stainless clinic tray, vertical framing, blurred clinical background.", "Very slow push-in toward the standing vial; shallow focus."),
 "pv10_vial_gloved": ("Gloved hand holding Depo-Provera vial", "A gloved nurse hand holding up the Depo-Provera vial to check it, clinic light, vertical close framing.", "The gloved hand slowly turns the vial slightly to read the label."),
 "pv11_injection_close": ("Nurse giving Depo-Provera injection", "Close vertical framing of a nurse giving the Depo-Provera pre-filled syringe injection into a woman's upper arm, label on the syringe visible.", "The nurse slowly depresses the plunger, the injection completing into the arm."),
 "pv12_box_vial_wood": ("Depo-Provera box + vial on wood (Rx)", "A Depo-Provera box lying beside a small glass vial on a warm wooden table, vertical top-down-ish angle.", "Slow drift over the box and vial on the table; nothing moves."),
 "pv13_vial_calendar": ("Depo-Provera vial on dose-schedule calendar", "A Depo-Provera vial standing on an open paper calendar with circled dates, implying a recurring shot schedule, vertical framing.", "Very slow push-in toward the vial standing on the calendar."),
 "pv14_box_shelf": ("Depo-Provera box on pharmacy shelf", "A Depo-Provera box on a pharmacy shelf among other medicine boxes, one box in sharp focus, vertical framing.", "Slow lateral drift along the shelf, focus holding on the Depo-Provera box."),
 "pv15_vial_macro2": ("Depo-Provera vial macro (5mL multi-dose)", "Extreme vertical macro of the standing Depo-Provera vial, label crisp and centered, deep blurred clinical background.", "Very slow push-in on the vial; label stays sharp."),
 "pv16_syringe_draw": ("Syringe drawing from Depo-Provera vial", "A syringe drawing liquid from the Depo-Provera vial on a clinic tray, gloved hands, vertical framing.", "The plunger slowly draws liquid up from the vial into the syringe."),
 "pv_online_boxvial": ("Depo-Provera box + vial (real catalog source)", "The Depo-Provera box and glass vial from a real InsiderX/Pfizer catalog photo, arranged on a clean pharmacy counter, front labels facing camera, vertical 9:16.", "Very slow push-in toward the box and vial; product stays still."),
}
EXISTING = {"pv1_vial_tray": "e1fc6281-de72-424c-b421-decbae770be2"}  # row #80 (test upload)
TAGS = ["depo", "depo-provera", "meningioma", "product", "9x16"]


def upload(slug, title):
    f = f"outputs/depo_docu/broll_clips/{slug}.mp4"
    h = {"Authorization": f"Bearer {PAT}", "Idempotency-Key": str(uuid.uuid4())}
    data = {"project_id": PROJ, "subproject_id": SUB, "title": title,
            "clip_category": "product", "tags": json.dumps(TAGS)}
    with open(f, "rb") as fh:
        r = requests.post(f"{BASE}/brolls/clips/upload", headers=h,
                          files={"file": (f"{slug}.mp4", fh, "video/mp4")}, data=data, timeout=300)
    j = r.json()
    return j.get("id"), j.get("row_number"), r.status_code


def patch(cid, img, vid, title=None):
    body = {"image_generation_model": IMG_MODEL, "image_generation_prompt": img + IMG_SFX,
            "video_generation_model": VID_MODEL, "video_generation_prompt": vid + VID_SFX}
    if title:
        body["title"] = title
    r = requests.patch(f"{BASE}/brolls/clips/{cid}",
                       headers={"Authorization": f"Bearer {PAT}", "Content-Type": "application/json"},
                       json=body, timeout=60)
    return r.status_code


rows = []
for slug, (title, img, vid) in CLIPS.items():
    if slug in EXISTING:
        cid = EXISTING[slug]; row = 80
        up = "reuse#80"
        ps = patch(cid, img, vid, title=title)
    else:
        cid, row, us = upload(slug, title)
        up = f"up{us}"
        ps = patch(cid, img, vid) if cid else "no-id"
    rows.append((row, slug, up, ps))
    print(f"  #{row} {slug}: {up} patch={ps}", flush=True)

print("\nUploaded rows:", sorted(r[0] for r in rows if r[0]))
