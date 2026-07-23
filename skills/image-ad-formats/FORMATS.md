# Image Ad-Format Catalog — 101 formats (generic / campaign-agnostic)

The master list of static **image** ad formats. Each can be produced as a full generated banner
or recreated in a deterministic design pipeline. Reuse on any product or offer by supplying
approved product, copy, and compliance inputs. Historical campaign implementations are indexed
in `inventory/video_workflow_catalog.md`.

**Total: 101 distinct formats**, in 7 buckets. (Layer a unique angle/persona on top → effectively unlimited variants; keep format AND angle unique per ad.)

---

## 1 · Offer / price / value (12)
1. `scarcity` — limited-time / new-customer pricing ribbon
2. `compare` — price ladder vs competitor/old way (3-tier ✗/✓)
3. `receipt` — itemized receipt, line items + one total
4. `pricetag` — big price-tag / sticker
5. `pricebars` — competitor vs us as bold price bars
6. `coupon` — tear-off coupon look
7. `barchart` — cost/value bar chart
8. `piechart` — "what's included" pie
9. `gauge` — value meter/dial
10. `product_clean` — bare product still + one flat price
11. `icongrid` — everything-included icon grid
12. `countdown` — deadline countdown timer

## 2 · Social proof / authority / reviews (8)
13. `review` — ★★★★★ single review card + name
14. `authority` — "trusted by N" + credibility badges
15. `stat` — one huge number on plain bg
16. `testimonialwall` — grid/wall of short reviews
17. `ratingbreakdown` — 5★ bar breakdown
18. `asseenin` — press / "as seen in" strip
19. `spotlight` — one member/customer highlighted
20. `membercard` — membership / ID card look

## 3 · Curiosity / hook / pattern-interrupt (10)
21. `curiosity` — open-loop question ("why are people switching?")
22. `warning` — "before you do X, read this" PSA
23. `search` — typed search-bar question
24. `horoscope` — playful horoscope framing
25. `fortune` — fortune-cookie slip reveal
26. `magquiz` — magazine-style "what's your type" quiz
27. `quizcard` — single quiz question + answer buttons
28. `qualify` — "you might qualify if…" checklist
29. `expectreality` — expectation vs reality two-panel
30. `speechbubble` — bold comic speech-bubble line

## 4 · Comparison (3 unique + 2 cross-listed)
31. `grid` — feature comparison table (us vs alt vs nothing)
32. `venn` — Venn diagram (you ∩ the product)
33. `heatmap` — feature heat-map grid
   · (also: `compare` price ladder, `pricebars` — see Offer)

## 5 · Educational / mechanism (15)
34. `howitworks` — how-it-works diagram, 3 mechanism points
35. `cravinganatomy` — "anatomy of a [problem]" labeled diagram
36. `timeline` — "your first 30 days" milestone timeline
37. `eras` — "old era vs new era" timeline
38. `circularsteps` — circular 3-step process loop
39. `flowchart` — "should you try X?" decision flowchart
40. `signs` — "signs you might need this" listicle
41. `faqaccordion` — FAQ / objection-killer Q&A
42. `definition` — dictionary-definition card
43. `reportcard` — graded "report card" of the old way
44. `nutritionlabel` — nutrition-label parody of the offer
45. `todolist` — checked-off to-do list
46. `grocerylist` — relatable handwritten list
47. `clipboard` — intake-clipboard checklist
48. `weather` — weather-forecast metaphor

## 6 · Native / UGC / lifestyle / minimal — copy-led (22)
49. `ugc` — UGC "shot-on-phone" product-in-hand
50. `news` — documentary news photo + one title
51. `candid` — plain candid photo (copy carries it)
52. `statement` — one bold line, no product
53. `scene` — quiet object/lifestyle still
54. `article` — content/article link-preview hero
55. `letter` — open letter ("to the person reading this…")
56. `mirror` — candid mirror selfie
57. `doorstep` — discreet delivery at the door
58. `minimal` — minimalist premium hero, negative space
59. `cinematic` — moody film-still
60. `macro` — crisp macro close-up + line
61. `pastel` — calm pastel / spa mood
62. `duotone` — two-tone bold portrait
63. `journal` — handwritten diary page
64. `stickynote` — sticky-note desk flat-lay
65. `letterhand` — pen-on-paper handwritten letter
66. `polaroid` — taped polaroid
67. `postcard` — postcard front
68. `unboxing` — what's-in-the-box
69. `dietflatlay` — overhead lifestyle flat-lay
70. `visionboard` — pinned-goals collage

## 7 · Novelty "looks-like-a-thing" + bold style (31)
71. `rxlabel` — prescription/label close-up
72. `recipe` — recipe card ("recipe for…")
73. `roadsign` — highway-sign metaphor
74. `certificate` — award / certificate
75. `chalkboard` — handwritten chalkboard
76. `boardingpass` — boarding-pass / ticket metaphor
77. `billboard` — ad-on-a-billboard mockup
78. `calendarinvite` — "appointment with yourself" invite
79. `nametag` — "Hello, my name is…" tag
80. `filmstrip` — journey film strip
81. `bookcover` — self-help book cover
82. `albumcover` — album-art metaphor
83. `movieposter` — dramatic movie poster
84. `neon` — glowing neon-sign line
85. `postitwall` — wall of sticky notes
86. `crossword` — crossword clue reveal
87. `flightboard` — split-flap departures board
88. `permissionslip` — "permission to…" slip
89. `approvedstamp` — big APPROVED stamp
90. `stickytab` — bookmark/sticky-tab marker
91. `comic` — multi-panel comic strip
92. `brutalist` — one giant word, stark
93. `vintage` — vintage poster / apothecary
94. `y2k` — Y2K chrome / holographic
95. `tabloid` — b&w tabloid newsprint clipping
96. `tracker` — habit-tracker calendar grid
97. `threed` — bouncy 3D render
98. `luxe` — premium gold/black
99. `popart` — pop-art / Ben-Day dots
100. `map` — "available in your area" map
101. `thisorthat` — A-vs-B product chooser

---

## Visual style axis — apply ANY style to ANY format above

A **format** is *what the ad is* (review, flowchart, price ladder). A **visual style** is *how it
looks*. They're independent axes — any format can be rendered in any style, so **format × style ×
angle** is the variety engine. Add the style to the gpt-image-2 prompt (e.g. "render the `compare`
format as a **flat-vector illustration**", or "the `review` as **watercolor**"). Styles are 100%
campaign-agnostic.

**Photographic:** `minimalist` ✓ · `documentary-candid` ✓ · `cinematic` ✓ · `macro` ✓ · `golden-hour-lifestyle` ✓ · `studio-product` ✓ · `flat-lay` ✓ · `ugc-phone` ✓ · `editorial-glossy` + · `black-and-white` +

**Illustrated / drawn:** `cartoon-comic` ✓ · `pop-art` ✓ · `3d-render` ✓ · `flat-vector` + · `doodle-sketch` + · `claymation` + · `watercolor` + · `line-art` + · `collage-cutpaper` + · `isometric` + · `risograph` + · `pixel-retro` + · `anime` + · `sticker-kawaii` +

**Design / era:** `brutalist-swiss` ✓ · `vintage-retro` ✓ · `y2k-chrome` ✓ · `neon-cyberpunk` ✓ · `luxe-goldblack` ✓ · `pastel-soft` ✓ · `bauhaus-geometric` + · `memphis-80s` + · `art-deco` + · `grunge-zine` +

**Native / "looks-like":** `news-broadcast` ✓ · `newsprint-tabloid` ✓ · `journal-handwritten` ✓ · `receipt-document` ✓ · `chalkboard-whiteboard` +

`✓` = already produced · `+` = available to add. **~22 styles covered, ~17 to add.**

---

**Recall:** say "make the `receipt` + `flowchart` + `testimonialwall` formats for [campaign], in
`watercolor` and `flat-vector` styles" — pull formats from any of the 7 buckets, pick a visual style,
vary both across the batch, and layer a persona/angle on top. Pair each with a copy shape from the
`ad-copy-formats` skill.
