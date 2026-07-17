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

# REDESIGNED FUNNEL — LEAN (user-locked 2026-07-09)

**This is a MARKETING funnel, not a legal intake. Volume is the goal. Do not tank conversion.**

**DIVISION OF LABOUR (user-locked): the FORM qualifies. The AGENTS collect the record data.**
**NEVER ask doctor name / hospital / pharmacy in the funnel** — those are typing + memory questions,
they are where a form bleeds leads, and our agents ask them on the call anyway. *That is also the
answer to MTM's "capture it at intake level": **the agents ARE the intake.*** The form's only job is
max leads + the qualification facts that cost a single tap.

**Rules the form obeys:** taps only, never typing · never name the drug in a yes/no · never label the
losing option · never put the qualifying threshold at the floor of a list · **mirror the ad's order —
brain meningioma FIRST** (they self-identified from the ad, so it's an instant "that's me" and builds
momentum), the Depo relation second.

## The form — 5 taps, then contact

**Q1 — the hook (matches the ad). "What were you (or your loved one) diagnosed with?"**
Brain meningioma · Another kind of brain tumor · Glioma / glioblastoma · Acoustic neuroma ·
Pituitary tumor · Something else · Not diagnosed with anything
→ Real conditions mixed in, **no "(you do not qualify)" label on anything**. Meningioma stops being
the obvious pick at zero conversion cost.

**Q2 — "What year were you diagnosed?"** dropdown **1985 → 2026**
→ Criterion 3 (dx 1992+) and the sequence check (dx after use). The wide range hides the cut-off.

**Q3 — "When were you getting the Depo shot?"** ONE screen, two dropdowns: **first year** / **last
year** (**1985 → 2026**, + *"Still getting them"*)
→ Duration AND the 1992–2019 window both fall out of this, and no option advertises a threshold.
**This replaces the broken live Q3.**

**Q4 — "About how many shots in total?"** 1 · 2 · 3 · 4–6 · 7–12 · 13–20 · More than 20 · Not sure
→ The most precise qualifier we can get in one tap (MTM's real line is **4+ shots**, and dates alone
miss "2 shots spread over 2 years"). 4 sits **mid-list**, never at the floor.

**Q5 — "Currently represented by an attorney for this matter?"** Yes/No *(unchanged from live)*

→ **CAPTURE:** first · last · email · phone · consent. **Done. No second form, no enrichment step.**

**Net: 5 taps vs the live 4** — one extra tap buys duration + both date windows + the fraud fixes.
If even that is too long, **cut Q2** (dx year) first — pre-1992 diagnoses are vanishingly rare and
the agent can confirm the date on the call. **Never cut Q4** — it is the whole qualification.

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
