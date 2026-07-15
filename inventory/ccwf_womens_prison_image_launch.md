# CA Women's Prison — image-ad expansion + launch (session 2026-07)

Advertiser: Jordan M. Jones / Adam Pulaski (Pulaski Kherkher PLLC). Niche: CA women's-prison
staff sexual-abuse legal lead-gen. AdMachin **Tort** project `e15c60bd-95c2-47b9-9730-c29fb5325461`
→ **Women's Prison** subproject `acf1b974-9721-488b-a4e0-ffe0664070c5`.

## Data-validated winners (pulled from FB Insights, lifetime, via bulk CSV export)
- **Overall #1 = WPA - Latina - HJ P1 VIDEO** (account YJE-23): **$81.8k spend / 378 leads / ~$216 CPL**. Best ad "2" (63 leads @ $190); persona **"54yr latina"** is the single biggest lead-driver in the account.
- **Proven IMAGE winners:** Depo `5-img-testimonial` (CTR ~5%, best CTR), IL JDC `11-img-different-ideas` (CPL **$44**), IL JDC `4-img-text-ads` (CPL $142), Depo `14-img` (CPL $166). → testimonial-photo = best engagement; simple text/news images = cheapest leads.
- Report saved: `outputs/perf_reports/legal_ads_lifetime.csv`.

## The 30 new image ads (built + launched this session)
Two batches, all **gpt-image-2 (KIE, 1:1, 2K), full-render** (headline + text + layout baked in the prompt, NO PIL). Black + Latina personas. "significant potential compensation" (women's prison KEEPS "potential"). Facilities: CCWF/Chowchilla, Valley State, CIW/Chino, Folsom.

- **Batch 3 — `scripts/ccwf_jdcstyle20.py`** → `outputs/ccwf_women/jdcstyle20/` (j01–j20). IL-JDC *designed/news* style, **every ad a different format**: newspaper front-page, TV broadcast, accountability hero, explainer, magazine, op-ed, Reddit, comment-section, Google autocomplete, native post, dictionary, no-deadline calendar, voicemail, sticky-note, FAQ, myth/fact, by-the-numbers, claims-review, loved-one referral, testimonial (only 1 — user asked "less testimonials").
- **Batch 4 — `scripts/ccwf_social10.py`** → `outputs/ccwf_women/social10/` (s01–s10). Comment / chat / forum social-proof, **DE-BRANDED** (user-locked: NO Facebook logo/look, no Reddit/Apple/WhatsApp/Messenger logos — generic UIs): 2 Reddit-style, group chat, 1:1 text DM, advocate DM, 3 comment threads, support-forum, star-reviews.
- **Staging — `scripts/ccwf_launch30_stage.py`** (resumable, one-writer state `outputs/ccwf_women/launch30_stage.json`): burns the Pulaski/Jones disclaimer BAR (`burn_disclaimer_image.py --style bar`) → uploads → per-ad headline + primary copy (verbatim disclaimer **appended** to each primary) → assembles 30 DRAFT ads. Approved copy verbatim is embedded in the script's `COPY` list.

## Launch (LIVE, paused) — into the winning campaign
`bulk_launch_ads` into **WPA - Latina - HJ P1** `120242151877070281`, account **YJE-23** `act_885970616544640`.
- **6 new adsets `36`–`41`**, 5 ads each, **round-robin** (each adset a format mix). Duplicated targeting from **`10 - 50yr latina - 20-64 -b350`** `120248628379300281` (ABO campaign → each adset carries its own **$50/day**).
- page **Justice Covered** `451791144678410` · pixel `1345276490863660` (LEAD) · landing `https://womensprison.justicecovered.com/` · CTA `LEARN_MORE`.
- **All adsets PAUSED** (no spend until a human flips them ACTIVE in Meta). Needed `use_create_from_source:true` (adset 10 had placement-coupling). One ad (`j03`) hit a transient fetch-fail → re-attached via `launch_ad`.
- ⚠️ **CA WPA Pulaski HJ** (the OTHER women's-prison campaign, in SC2-200 `act_866025392591299`) is **CBO** + uses a DIFFERENT pixel/landing/cta (`cawomensprison.justicecovered.com`, SEE_DETAILS) — don't cross the two.

## NO-REPEAT format inventory (74 formats already used across the campaign)
`ccwf_image_ads` img01–20 (testimonial selfie + cinematic prison scenes) · `ccwf_swipe_concepts` c01–20 (id_card, yesno_poll, tap_location, input_field, checkbox_quiz, facility_checklist/grid, dublin_precedent, settlement_100m, breaking_news, official_notice, news_quote, fake_tweet, news_article, provocative, memory_hook, cdcr_headline, visit_photo_headline, relational, thennow) · `ccwf_swipe2_concepts` n01–20 (tap_years, ca_map, select_happened, form_preview, survivors_counter, imessage, ask_me, review_quote, consensual_reframe, feeling_enough, no_paperwork, urgency, calculator, postcard, whisper_quote, then_now_split, problem_solution, two_women, button_macro, verdict_clipping) · `ccwf_creative_concepts` m01–14 (return_gate, at_fence_now, windshield, small_against_wall, then_now_fence, photo_held, two_survivors_gate, empty_visiting_room, payphone, gate_dusk, made_bunk, redacted_grievance, editorial_poster, torn_mended) + jdcstyle20 j01–20 + social10 s01–10. **Any new batch must avoid all of these** (concept scripts live on the `ccwf-image-ad-tooling` branch — retrieve via `git show <branch>:scripts/<f>.py`).

## Competitor AdSwipe dissection (IL JDC serials 1512–1519, via `export_swipe_creatives_for_agent`)
Winning competitor formats worth adapting (1516 was a stray car-dealership TikTok, ignore):
- **1519** (Pulaski Kherkher's own CA-juvie ad) — tabloid **"DIRTY SECRETS"** rust/yellow + B&W *dramatized* guard-over-detainee photo + "serious money" + black CTA bar.
- **1513** — dark + doodle illustration + **"$350,000 settlements / 900 victims"** + 60-sec quiz.
- **1515** — clean **3-Myth / 3-Fact** objection-killer (denial / no name / self-blame).
- **1512** — **qualification-criteria icon grid** over a real facility photo (age/facility/staff/identify).
- **1514** — **split**: real facility photo + yellow callout panel ("STAFF ABUSE AT HORSHAM?").
- **1517** — bold yellow question over dark corridor photo + "YOUR VOICE MATTERS" + red CTA.
- **1518** — urban-vernacular **UGC video** ("Yo, have you been sexually abused in the IL JDC…").

**Compliance adaptations for our version:** DROP "$350,000 / settlements / serious money / entitled" → "significant potential compensation" + "may qualify"; soften "900 victims" → "survivors are coming forward / you are not alone" (no hard number); dramatized photos stay institutional + non-explicit (covered by the paid-actors/dramatization disclaimer).

## Pending (for the next session)
- **6 competitor-format adaptations** proposed (`wp_dirtysecrets`, `wp_voice_matters`, `wp_facility_split`, `wp_qual_grid`, `wp_mythfact3`, `wp_illustration_quiz`) — awaiting user go + explicit OK on the dramatized `wp_dirtysecrets` photo. NOT generated yet.
- **IL-JDC performance optimizer** (turn-off losers / scale winners for YJE-23) — designed, not built; thresholds TBD (target CPL, kill rule, scale rule, recommend-vs-auto-pause). **Blocked until the FB connection is reconnected in AdMachin.**
- Flip adsets 36–41 ACTIVE in Meta to start delivery (~$300/day total).
