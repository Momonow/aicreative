# Depo-Provera — LAW FIRM QUALIFICATION CRITERIA (source: MTM, 2026-07)

Authoritative sign-up criteria from the firm. **Ad copy + scripts must pre-qualify against these**
or we pay for leads that can't be retained. Campaign context: `project_depo_meningioma_campaign`.

## The 5 criteria

1. **1-year MINIMUM use of BRAND Depo-Provera** (injectable contraceptive) = **4+ shots**
   (one every 3 months). *It is OK to sign if the client is unsure brand vs generic.*
2. **DIAGNOSED with Brain Meningioma AFTER the 1 year of use.**
3. **Diagnosed 1992 or later.**
4. **Used the product between 1/1/1992 and 12/31/2019.**
5. **Intake questions must be OPEN-ENDED, not yes/no** — e.g. "What were you diagnosed with?",
   "Where is the injury located?" This weeds out fraud (a yes/no question tells the claimant the
   answer we want).

## Intake data the firm REQUIRES to sign a retainer (currently missing / "does not recall")

- **Diagnosing doctor name + hospital**
- **Prescribing doctor + pharmacy name**
- Must be **POSTED VIA API** — the PDF is only a backup; the docket team can't open PDFs at volume.
- This must be captured **at the intake level** for a cleaner, more qualified lead.

## Qualifying Depo products (any of these count)

Depo Provera · Depo-Provera · DPCI · Depo Provera IM · DMPA · Depot medroxyprogesterone acetate ·
Medroxyprogesterone Acetate · MPA · IM MPA · Depo-SubQ Provera 104 · Greenstone Medroxyprogesterone ·
Greenstone MPA · Prasco Medroxyprogesterone · Prasco MPA

## Qualifying brain/head meningioma variations

Intracranial meningioma · Intercranial meningioma · Cranial meningioma · Brain meningioma ·
Meninges tumor · **Arachnoid tumor (but NOT arachnoid cyst)** · Convexity meningioma ·
Falcine meningioma · Parasagittal meningioma · Intraventricular meningioma · Skull base meningioma ·
Sphenoid wing meningioma · Olfactory groove meningioma · Posterior fossa/petrous meningioma ·
Suprasellar meningioma · Recurrent meningioma · Foramen magnum meningioma · Meningothelial
meningioma · Fibrous meningioma · Psammomatous

## CREATIVE IMPLICATIONS (what this changes in our ads)

Our shipped Depo copy qualifies only on **"diagnosed with a brain meningioma after using the Depo
shot"** — it does NOT filter on duration or the usage window, so we are paying for leads the firm
cannot retain. Add these filters to copy/scripts:

- **Duration filter — the big one:** say **"a year or more"** / **"4 or more shots"** /
  **"every 3 months for at least a year"**. (Our docu VO already gestures at this — "the one given
  every three months, for years" — but the FB primary/headline don't.)
- **Date-window filter:** the shot must have been used **1992–2019**. Anyone whose only use is
  2020+ does NOT qualify. Worth a plain line like "if you were on it any time between 1992 and 2019".
- **Order of events:** the meningioma diagnosis must come **AFTER** the year of use — phrase as
  "used it for a year or more, and were **later** diagnosed".
- **Keep the wording locks:** still **"brain meningioma"**, still **never "tumor"**
  (`feedback_meningioma_only_targeting`) — note the firm's own list contains "meninges tumor" /
  "arachnoid tumor", but that is *their* intake vocabulary, NOT our ad-targeting vocabulary.
- **Don't turn the ad into a yes/no quiz.** Criterion 5 is about the INTAKE form, but it rhymes with
  our creative rule: the ad should state the qualifying facts, and let the open-ended intake do the
  screening.

**Not our surface:** the doctor/hospital/pharmacy capture + API posting is an **intake-form/CRM**
job (justicecovered / whoever owns the form), not something ad creative controls. Flagged here so
the ad side isn't blamed for a form gap — but our ads CAN reduce "does not recall" by setting the
expectation ("you'll be asked who diagnosed you and where you got the shot") if the firm wants that
trade-off (it costs conversion rate to gain lead quality — user's call).

---

# AUDIT: the LIVE funnel at depop.justicecovered.com (walked 2026-07-09)

**The live form is 4 questions → contact details. It captures NONE of the data MTM requires.**

1. "Did you or a loved one received Depo-Provera medication on a regular basis?" → Yes/No
2. "Were you diagnosed with Meningioma after taking the Depo Provera?" → Meningioma / Other type of
   brain tumor / Other injury / **"No injury (You do not qualify)"**
3. "Approximately how long did you or a loved one take Depo-Provera…?" → **1 year / 2 years /
   3 or more years / Never took Depo-Provera**
4. "Currently represented by an attorney?" → Yes/No → contact details → RECEIVE RESULTS

| MTM requires | Live form |
|---|---|
| Diagnosing doctor + hospital | ❌ never asked |
| Prescribing doctor + pharmacy | ❌ never asked |
| Open-ended, not yes/no (criterion 5) | ❌ every question is yes/no or signposted MC |
| Diagnosed 1992+ | ❌ never asked |
| Used 1992–2019 | ❌ never asked (no start/stop years) |
| 1 yr min / 4+ shots | ⚠️ asked but broken (below) |

**The API-vs-PDF debate is moot — the Dx/Rx data is never collected, so there's nothing to post.**
That is the root cause of "client does not recall": nobody ever asked.

### The three bugs

1. **Q2 signposts the losing answer** — the option is literally labelled **"No injury (You do not
   qualify)"**, and "Meningioma" is served as choice #1. It teaches every claimant which box to
   avoid and which to pick. Catastrophic for fraud; zero-cost to fix.
2. **Q3 manufactures qualifying answers — the root of the unqualified intakes.** The LOWEST real
   option (**1 year**) **IS the qualifying minimum**. A woman who took it for 3 months has no honest
   choice ("Never took Depo-Provera" is false), so she clicks "1 year." The form *generates* the
   exact leads MTM is rejecting. It also never asks start/stop years → the 1992–2019 window is never
   checked, and never asks shot count.
3. **Q1 is a leading yes/no that names the drug** → free "yes" for anyone.

---

# THE PLAN — ADDITIVE ONLY (user-locked 2026-07-09)

**Two hard constraints from the user:**
1. **This is a MARKETING funnel, not a legal intake. Volume is the goal.** **NEVER ask doctor name /
   hospital / pharmacy in the funnel** — typing + memory questions are where a form bleeds leads, and
   **our agents ask them on the call**. *That is also the answer to MTM's "capture it at intake
   level": **the agents ARE the intake.*** No post-capture enrichment step either — rejected as still
   too long.
2. **DO NOT touch the existing questions — UTM + pixel are tied to their conditions.** Reordering,
   rewording or re-optioning a tracked step breaks the pixel conditions and resets FB's learning on
   the conversion event. **Everything below is ADDED manually; nothing existing is edited.**

## The trick: you don't fix the broken Q3 — you NEUTRALIZE it by adding a shot count

The live duration question is structurally forced (its floor IS the qualifying minimum), so it will
keep returning "1 year" from everyone. **Leave it.** Add a shot-count question next to it and it
becomes harmless: **qualify on the shot count, ignore Q3's answer.** The bad data stays, the pixel
stays, the truth arrives alongside it.

## What to ADD, in priority order

**ADD #1 — "About how many shots in total?"** 1 · 2 · 3 · 4–6 · 7–12 · 13–20 · More than 20 · Not sure
→ **The single highest-value add.** MTM's real line is **4+ shots**; 4 sits **mid-list**, never at the
floor, so it can't be gamed by elimination the way the live Q3 can. This alone converts the funnel
from "manufactures unqualified leads" to "qualifies."

**ADD #2 — "When were you getting the Depo shot?"** ONE screen, two dropdowns: **first year** /
**last year** (**1985 → 2026**, + *"Still getting them"*)
→ The **1992–2019 usage window**, which is currently invisible. Also cross-checks duration.

**ADD #3 — "What year were you diagnosed?"** dropdown **1985 → 2026**
→ Criterion 3 (dx 1992+) + the sequence check (dx AFTER use). **Lowest value — cut this first if the
funnel feels long.** Pre-1992 diagnoses are vanishingly rare and an agent can confirm the date.

## WHERE to insert (matters — don't shift tracked steps)

**Safest: APPEND all new questions at the TAIL — after the attorney question, immediately before the
contact form.** Every existing step keeps its position, its index, and its conditions. Nothing that
the pixel or UTM logic keys on moves.
- **If the platform keys conditions on question ID (not step index)**, ADD #1 can instead sit right
  after the live duration question, where it reads more naturally. **Confirm which before inserting
  mid-funnel** — if it keys on index, a mid-funnel insert shifts the attorney step and breaks it.
- Trade-off of appending: the qualification data arrives last, so a drop between the attorney step
  and capture loses it. Drop-off there is low (they're nearly done), and it's worth it to never
  disturb the tracked path.

## The one edit worth checking (label-only, no logic change)

Q2's option is labelled **"No injury (You do not qualify)"** — it tells every claimant which box
loses. **If the pixel condition keys on the option's VALUE or index (not its display text), editing
the label to plain "No injury" is free** and costs zero conversion. Check first; if the condition
matches on label text, leave it and let ADD #1 carry the qualification.

## API fields (post all of it — PDF is backup only)

`dx_condition` · `dx_year` · `rx_first_year` · `rx_last_year` · `rx_still_using` ·
`rx_shot_count_bucket` · `has_attorney` · contact (`first_name` `last_name` `email` `phone` `consent`)
Derived server-side: `rx_duration_years` (last−first) · `qualifies_duration` (≥1yr / ≥4 shots) ·
`qualifies_window` (use within 1992–2019) · `qualifies_sequence` (dx_year ≥ first_year+1) ·
`qualifies_dx_year` (≥1992).
Agent-filled after the call (CRM, not the form): `dx_doctor_name` · `dx_hospital` ·
`rx_provider_name` · `rx_provider_type` · `rx_city_state`.

## What to tell MTM

- **"Which pharmacy" is the wrong question — Depo is administered IN-CLINIC, not dispensed.** It
  legitimately returns "none" for valid claimants. *"Who was giving you the shots"* (OB/GYN, family
  doctor, health department, Planned Parenthood) is the question that actually carries the Rx data.
- **"Does not recall" is a script problem, not a form problem.** A bare `Doctor name: ___` manufactures
  it. Agents should scaffold down: provider TYPE → city/state → hospital → insurer at the time. Any
  one of those lets the docket team find the provider; all are far easier to recall than a name from
  2003.

## Zero-conversion-cost fraud fixes (do these first)

1. **Delete the "(You do not qualify)" label.** Never tell a claimant which answer loses.
2. **Never put the qualifying threshold at the floor of an option list** (today's Q3 bug) — always
   extend the options past the qualifying range on BOTH sides so the qualifying zone sits mid-list.
3. **Don't name the drug in a yes/no.** Ask what they took / what they were diagnosed with; match
   against the qualifying-product list server-side.
