# Static Image Ad-Format Library — 101 formats (built on TrimRx GLP-1, reusable)

The TrimRx GLP-1 campaign produced **101 distinct static-image ad formats** (the 160-ad library =
101 unique formats + 60 angle/persona variants that reuse them). This is the named catalog so any
campaign can recall a format by slug. Each is a full **gpt-image-2** banner (i2i with the product
PNG as reference, or t2i for pure-photo); all compliant (footnote, no brand names, no before/after).

## Naming + recall

- **Files:** `outputs/<campaign>/final/<prefix><NN>_<slug>_gpt.png`
- **Prefix = batch/lane:** `v`=viral DR · `s`=visual style · `c`=clean copy-led/minimal · `f`=novelty format · `a`=angle/persona variant · `30g`=comparison.
- **Generators (one per lane):** `trimrx_viral_gpt.py` (10) · `trimrx_styles20.py` (20) · `trimrx_copyled.py` (12) · `trimrx_formats.py` (58) · `trimrx_compare_gpt.py` (1) · `trimrx_angles.py` (60 variants). Produce/re-roll one by slug: `.venv/bin/python scripts/<gen>.py --only <slug>`.
- **Copy decks:** `copy.md` · `copy_led.md` · `copy_angles.md` · `copy_formats.md`. Pair a copy shape from the `ad-copy-formats` skill to each visual format (e.g. testimonial-wall → first-person advertorial; FAQ image → Q&A copy).
- **Headlines:** short + front-loaded (~≤40 char, mobile-feed truncates) — see `feedback_short_mobile_headlines`.

## The 101 formats by category

### 1 · Offer / price / value (12)
| Format | slug | one-liner |
|---|---|---|
| Scarcity ribbon | `scarcity` (v09) | "limited-time pricing" urgency banner |
| Price ladder vs clinic | `compare` (30g) | "stop overpaying" — 3-tier ✗/✓ price comparison |
| Itemized receipt | `receipt` (s06) | thermal-paper receipt, $0.00 line items, one total |
| Price tag | `pricetag` (f23) | big price-tag/sticker |
| Price bars | `pricebars` (f47) | clinic vs us as bold price bars |
| Coupon | `coupon` (f07) | tear-off coupon look |
| Cost bar chart | `barchart` (f15) | $1,000+ vs $149 bar chart |
| What's-included pie | `piechart` (f16) | pie of included benefits |
| Value gauge | `gauge` (f09) | meter/dial pointing to "great value" |
| Clean product + price | `product_clean` (c05) | bare product still, one flat price |
| Everything-included grid | `icongrid` (s19) | 6 benefit tiles + price |
| Deadline countdown | `countdown` (f36) | countdown-timer urgency |

### 2 · Social proof / authority / reviews (8)
| Format | slug | one-liner |
|---|---|---|
| Star review card | `review` (v02) | ★★★★★ quote + member name |
| Trusted-by badges | `authority` (v03) | "300,000+ members" + trust badges |
| Single big stat | `stat` (c10) | one huge number on plain bg |
| Testimonial wall | `testimonialwall` (f49) | grid of short ★ reviews |
| Rating breakdown | `ratingbreakdown` (f50) | 5★ bar breakdown |
| As-seen-in press | `asseenin` (f51) | press/credibility strip |
| Member spotlight | `spotlight` (f52) | one member highlighted |
| Member ID card | `membercard` (f25) | membership-card look |

### 3 · Curiosity / hook / pattern-interrupt (10)
| Format | slug | one-liner |
|---|---|---|
| Open-loop question | `curiosity` (v04) | "why are women over 40 switching?" |
| Warning PSA | `warning` (v10) | "before you pay $1,000+, read this" |
| Search query | `search` (c04) | typed search-bar question |
| Horoscope | `horoscope` (f22) | playful horoscope-style |
| Fortune cookie | `fortune` (f43) | fortune-slip reveal |
| Magazine quiz | `magquiz` (f44) | "what's your type" quiz |
| Quiz card | `quizcard` (s11) | "do cravings run your day?" |
| Qualify checklist | `qualify` (v05) | "you might qualify if…" |
| Expectation vs reality | `expectreality` (f46) | two-panel relatable |
| Speech bubble | `speechbubble` (f57) | bold comic speech-bubble line |

### 4 · Comparison (5)
| Format | slug | one-liner |
|---|---|---|
| Feature table | `grid` (s12) | TrimRx vs clinic vs nothing matrix |
| Venn diagram | `venn` (f34) | "you" ∩ "a GLP-1 plan" |
| Heat map | `heatmap` (f48) | feature heat-map grid |
| (price ladder) | `compare` (30g) | see Offer |
| (price bars) | `pricebars` (f47) | see Offer |

### 5 · Educational / mechanism (15)
| Format | slug | one-liner |
|---|---|---|
| How-it-works diagram | `howitworks` (v08) | body diagram, 3 mechanism points |
| Anatomy of a craving | `cravinganatomy` (f45) | brain/stomach craving diagram |
| First-30-days timeline | `timeline` (v07) | day1→week4→ongoing |
| Eras timeline | `eras` (f35) | "diet era vs GLP-1 era" |
| Circular steps | `circularsteps` (f56) | quiz→provider→delivered loop |
| Flowchart | `flowchart` (f06) | "should you try a GLP-1?" |
| Signs listicle | `signs` (c09) | "more than willpower if…" |
| FAQ accordion | `faqaccordion` (f14) | Q&A objection-killer |
| Dictionary definition | `definition` (f03) | "food noise (n.)…" |
| Diet report card | `reportcard` (f20) | grades the old approaches |
| Nutrition-label parody | `nutritionlabel` (f05) | "label" of the program |
| To-do list | `todolist` (f19) | checked-off list |
| Grocery list | `grocerylist` (f42) | relatable list |
| Clipboard checklist | `clipboard` (f54) | intake-clipboard look |
| Weather forecast | `weather` (f21) | "forecast: lighter" metaphor |

### 6 · Native / UGC / lifestyle / minimal — copy-led (22)
| Format | slug | one-liner |
|---|---|---|
| UGC product-in-hand | `ugc` (v01) | shot-on-phone, holding vial |
| News photo + title | `news` (c01) | documentary still + 1 title |
| Candid + story | `candid` (c02) | plain photo, copy sells |
| Statement card | `statement` (c03) | one bold line, no product |
| Quiet scene | `scene` (c06) | jeans + tape measure |
| Article link-preview | `article` (c07) | content-card hero |
| Open letter | `letter` (c08) | heartfelt note |
| Mirror selfie | `mirror` (c11) | candid mirror, copy sells |
| Doorstep delivery | `doorstep` (c12) | discreet box at door |
| Minimalist premium | `minimal` (s01) | Apple-style hero, negative space |
| Cinematic film-still | `cinematic` (s20) | moody by-the-window |
| Macro water | `macro` (s17) | crisp close-up + line |
| Pastel spa | `pastel` (s18) | calm, gentle |
| Duotone portrait | `duotone` (s10) | two-tone bold portrait |
| Journal page | `journal` (s05) | handwritten diary |
| Sticky-note desk | `stickynote` (s14) | yellow note flat-lay |
| Handwritten letter | `letterhand` (f40) | pen-on-paper |
| Polaroid | `polaroid` (f27) | taped polaroid |
| Postcard | `postcard` (f24) | postcard front/back |
| Unboxing | `unboxing` (f53) | what's-in-the-box |
| Diet flat-lay | `dietflatlay` (f17) | overhead wellness items |
| Vision board | `visionboard` (f10) | pinned goals collage |

### 7 · Novelty "looks-like-a-thing" + bold style (29)
| Format | slug | one-liner |
|---|---|---|
| Prescription label | `rxlabel` (f01) | Rx-label close-up |
| Recipe card | `recipe` (f02) | "recipe for…" card |
| Road sign | `roadsign` (f04) | highway-sign metaphor |
| Certificate | `certificate` (f08) | award/certificate |
| Chalkboard | `chalkboard` (f11) | handwritten chalk |
| Boarding pass | `boardingpass` (f12) | travel-ticket metaphor |
| Billboard mockup | `billboard` (f13) | ad-on-a-billboard |
| Calendar invite | `calendarinvite` (f18) | "appointment with yourself" |
| Name tag | `nametag` (f26) | "Hello, my name is…" |
| Film strip | `filmstrip` (f28) | journey film frames |
| Book cover | `bookcover` (f29) | self-help book cover |
| Album cover | `albumcover` (f30) | album-art metaphor |
| Movie poster | `movieposter` (f31) | dramatic poster |
| Neon sign | `neon` (f32) | glowing neon line |
| Post-it wall | `postitwall` (f33) | wall of sticky notes |
| Crossword | `crossword` (f38) | "1 across: GLP-1" |
| Flight board | `flightboard` (f39) | split-flap departures |
| Permission slip | `permissionslip` (f41) | "permission to…" |
| Approved stamp | `approvedstamp` (f55) | big APPROVED stamp |
| Sticky tab | `stickytab` (f58) | bookmark-tab marker |
| Comic strip | `comic` (f37) | 3-panel cartoon |
| Brutalist type | `brutalist` (s02) | one giant word |
| Vintage apothecary | `vintage` (s03) | old-pharmacy poster |
| Y2K chrome | `y2k` (s04) | holographic/chrome |
| Tabloid newsprint | `tabloid` (s07) | b&w newspaper clipping |
| Habit-tracker calendar | `tracker` (s08) | 30-day check grid |
| 3D playful | `threed` (s09) | bouncy 3D render |
| Luxe gold/black | `luxe` (s13) | premium gold accents |
| Pop-art comic | `popart` (s15) | Ben-Day dots, bold |
| US map | `map` (s16) | "available in your state" |
| This-or-that | `thisorthat` (v06) | semaglutide vs tirzepatide |

(That's 101 across the 7 buckets; a few price/comparison formats are cross-listed.)

## Angle/persona axis — the 60 variants (a01–a60), each mapped to its base format
`trimrx_angles.py` layers **unique angles + personas** onto the formats above. Full manifest so every
ad is accounted for (slug · persona · base format reused):

| # | slug | persona / angle | base format |
|---|---|---|---|
| a01 | `meno_hero` | women 40+ / menopause-metabolism | minimalist/hero photo |
| a02 | `meno_statement` | women 40+ / "new rules after 40" | statement |
| a03 | `meno_news` | women 40+ / the over-40 shift | news |
| a04 | `meno_review` | women 40+ / cravings quiet | review |
| a05 | `fifties_reinvention` | women 50+ / next chapter | hero photo |
| a06 | `fifties_luxe` | women 50+ / premium reset | luxe |
| a07 | `men_hero` | men / "dads" | hero photo |
| a08 | `men_busy` | men / no-time | candid |
| a09 | `men_comparison` | men / stop overpaying | compare |
| a10 | `men_stat` | men / social proof | stat |
| a11 | `mom_notime` | busy mom / no time for clinic | hero photo |
| a12 | `mom_mirror` | busy mom / did it for me | mirror (no-text) |
| a13 | `mom_journal` | busy mom / self-care note | journal |
| a14 | `pcos_questions` | PCOS / qualifier questions | qualify/question-stack |
| a15 | `pcos_story` | PCOS / first-person | candid (no-text) |
| a16 | `pcos_signs` | PCOS / signs | signs |
| a17 | `postpartum_story` | postpartum / after the baby | candid (no-text) |
| a18 | `postpartum_letter` | postpartum / "feel like you" | letter |
| a19 | `exec_online` | professional / visit is online | hero photo |
| a20 | `exec_minimal` | professional / fits a busy life | minimalist |
| a21 | `budget_real` | budget / no $1,000 bills | offer |
| a22 | `budget_receipt` | budget / itemized | receipt |
| a23 | `budget_pricebig` | budget / big price | pricetag |
| a24 | `plus_tried` | plus-size / tried everything | hero photo |
| a25 | `plus_split` | plus-size / journey simplified | split/duotone |
| a26 | `plus_letter` | plus-size / tried harder | letter |
| a27 | `cravings_night` | late-night eater | scene/candid |
| a28 | `cravings_statement` | food-noise | statement |
| a29 | `plateau_stuck` | plateau / stuck | candid |
| a30 | `conv_steps` | convenience / 3 steps | steps/circular |
| a31 | `conv_noclinic` | convenience / no waiting room | candid |
| a32 | `conv_doorstep` | convenience / delivered | doorstep (no-text) |
| a33 | `sci_howitworks` | science / mechanism | howitworks |
| a34 | `sci_mythfact` | science / myth vs fact | myth-fact |
| a35 | `social_join` | community / join | authority/spotlight |
| a36 | `social_reviews` | community / reviews | testimonialwall |
| a37 | `es_hero` | Spanish / lifestyle | hero photo |
| a38 | `es_price` | Spanish / price | pricetag |
| a39 | `es_review` | Spanish / review | review |
| a40 | `confidence_hero` | confidence / feeling like myself | hero photo |
| a41 | `newchapter` | new chapter / 50s | cinematic |
| a42 | `energy_statement` | energy / less hunger | statement |
| a43 | `urgency_pricing` | urgency / limited pricing | scarcity |
| a44 | `offer_bundle` | value / multi-month plan | value/icongrid |
| a45 | `warning_psa` | warning / before you pay $1k | warning |
| a46 | `needlefear` | needle-fear / easier than you think | candid |
| a47 | `support_team` | support / not alone | candid |
| a48 | `quiz_card` | qualify / quiz | quizcard |
| a49 | `checklist_included` | value / everything included | checklist/icongrid |
| a50 | `comparison_grid` | comparison / clearer choice | grid |
| a51 | `vintage` | trust / old-fashioned care | vintage |
| a52 | `popart` | bold / food noise | pop-art |
| a53 | `duotone` | mindset / it clicked | duotone |
| a54 | `ugc_hand` | native / in-hand | ugc |
| a55 | `map_states` | availability | map |
| a56 | `habit_tracker` | consistency | tracker |
| a57 | `search_curiosity` | curiosity / no insurance | search |
| a58 | `firstperson_candid` | first-person / stopped blaming | candid (no-text) |
| a59 | `minimal_premium` | premium / simplified | minimalist |
| a60 | `scene_jeans` | nothing fits | scene (no-text) |

**For a NEW campaign:** drive uniqueness off the 101-format catalog × the ~38-style axis, then layer a
persona/angle on top (don't reuse one format across personas and call it "different" — the bar is
unique format AND unique angle).
