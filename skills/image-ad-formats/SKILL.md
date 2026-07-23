---
name: image-ad-formats
description: Recall and reuse the library of ~100 DISTINCT static IMAGE-ad formats (gpt-image-2 banners) for DTC / lead-gen campaigns. Use when the user wants format variety for image ads, asks "what ad formats can we make", wants to recall/organize/name ad formats, says every ad must look different / be a unique format, or is building a batch of static image creatives. NOT for video formats (use ad-format-ideation) or copy shapes (use ad-copy-formats).
---

# Static Image Ad-Format Library

Use the format catalog to avoid batches where every ad is only a photo plus headline. Format,
visual style, audience angle, and copy shape are separate axes.

## How to produce / recall

- Full named catalog: `skills/image-ad-formats/FORMATS.md`.
- Historical campaign generators and results stay in their campaign inventory and workflow catalog.
- Name outputs descriptively: `outputs/<campaign>/final/<format>_<angle>_<slug>.png`.

## The 7 format buckets (pull across all of them for a varied batch)

1. **Offer / price / value** — scarcity ribbon, price-ladder-vs-clinic, itemized receipt, price tag, price bars, coupon, cost bar/pie chart, value gauge, clean-product+price, everything-included grid, countdown.
2. **Social proof / authority** — ★ review card, trusted-by badges, single big stat, testimonial wall, rating breakdown, as-seen-in press, member spotlight, member ID card.
3. **Curiosity / hook / pattern-interrupt** — open-loop question, warning PSA, search query, horoscope, fortune cookie, magazine quiz, quiz card, qualify checklist, expectation-vs-reality, speech bubble.
4. **Comparison** — feature table, Venn diagram, heat map, price ladder, price bars.
5. **Educational / mechanism** — how-it-works diagram, anatomy-of-X, first-30-days timeline, eras timeline, circular steps, flowchart, signs listicle, FAQ, dictionary definition, report card, nutrition-label parody, to-do list, grocery list, clipboard, weather forecast.
6. **Native / UGC / minimal (copy-led)** — UGC product-in-hand, news photo+title, candid+story, statement card, quiet scene, article preview, open letter, mirror selfie, doorstep, minimalist hero, cinematic still, macro, pastel, duotone portrait, journal, sticky-note desk, handwritten letter, polaroid, postcard, unboxing, flat-lay, vision board.
7. **Novelty "looks-like-a-thing" + bold style** — Rx label, recipe card, road sign, certificate, chalkboard, boarding pass, billboard, calendar invite, name tag, film strip, book/album/movie cover, neon sign, post-it wall, crossword, flight board, permission slip, approved stamp, sticky tab, comic strip, brutalist type, vintage apothecary, Y2K chrome, tabloid, habit-tracker, 3D, luxe, pop-art, US map, this-or-that.

## Visual style axis (independent of format)

Format = *what the ad is*; **visual style = *how it looks***. Any format renders in any style — add
the style to the prompt ("render the `compare` format as **watercolor**"). ~39 styles in 4 groups
(see `FORMATS.md`): **photographic** (minimalist, documentary-candid, cinematic, macro, golden-hour,
studio-product, flat-lay, ugc-phone, editorial-glossy, black-and-white), **illustrated** (cartoon-comic,
pop-art, 3d-render, flat-vector, doodle-sketch, claymation, watercolor, line-art, collage, isometric,
risograph, pixel-retro, anime, sticker-kawaii), **design/era** (brutalist, vintage, y2k-chrome, neon,
luxe, pastel, bauhaus, memphis-80s, art-deco, grunge-zine), **native** (news-broadcast, newsprint,
journal-handwritten, receipt-document, chalkboard). The variety engine is **format × style × angle**.

## Locked production rules (learned the hard way)

- **gpt-image-2 renders accurate text** for designed banners — even charts/diagrams/crosswords — IF you specify the exact on-image text in the prompt. Add: "Render ONLY the text specified — do not invent extra copy."
- **Pure-photo / "no-text" candids BACKFIRE:** the model fills empty space with invented claim copy ("REAL RESULTS", "proven", "sustainable weight loss"). For those use an emphatic *"Absolutely NO text, no words, no letters anywhere — a plain photo only"* clause and put the disclaimer in the FB primary text.
- **Product fidelity:** i2i can reinterpret packaging, colors, labels, and wordmarks. Use a
  fidelity-preserving edit route or deterministic composite when exact branding matters.
- **Compliance:** load the campaign/domain skill. Do not invent endorsements, guarantees,
  clinical claims, eligibility rules, legal footnotes, or professional identities.
- **Headlines:** short + front-loaded (~≤40 char; mobile feed truncates) — see `feedback_short_mobile_headlines`. Long persuasion goes in primary text.
- **Pair copy shapes** from the `ad-copy-formats` skill to each visual (testimonial-wall→advertorial, FAQ→Q&A, postcard→open letter, etc.).
- **Angle/persona is separate from format:** changing the person while reusing the same layout
  does not create a meaningfully different format.
- **Big batches — log task_ids on submit (recoverability).** KIE completes AND bills gpt-image-2 jobs server-side once submitted; killing the local runner doesn't cancel them, and WITHOUT a persisted task_id you can't re-fetch the finished image → a re-run re-submits and re-bills the in-flight ones. For 30+ ad batches, persist each task_id as it submits so a killed run is fully recoverable (skip-if-exists only recovers the already-DOWNLOADED ones). Also: gpt-image-2 handled dense designed banners (charts, flowcharts, crosswords, diagrams) with accurate text far better than expected — don't pre-emptively fall back to PIL.
