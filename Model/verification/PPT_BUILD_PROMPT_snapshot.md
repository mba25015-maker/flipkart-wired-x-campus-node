# PPT BUILD PROMPT — Flipkart WiRED X Semi-Final  ·  v2, template-native
*Built against the actual `Presentation_template.pptx`, measured. v1 assumed a 13.33×7.5 canvas and is
wrong — it is in `_superseded/`. Every figure below is asserted in `Model/audit.py` (311/311).*

---

# PART A — PASTE THIS ONCE, BEFORE ANY SLIDE

> You are building slides inside an existing PowerPoint template. **Do not create a new canvas, do not
> change the slide size, do not add background fills or borders — the template already provides them.**
> Your job is composition inside a fixed frame.
>
> ## A1. THE TEMPLATE, MEASURED — these are facts, not preferences
> Slide size **10.0 × 5.625 in**. Three layouts matter:
> | Layout | What it is | Use for |
> |---|---|---|
> | **CUSTOM_3** | White rounded card (x 0.20–9.78, y 0.18–5.45) inside a blue gradient frame. Blue Flipkart "f" top-right. | **All 8 content slides** |
> | **CUSTOM_2** | Full-bleed blue gradient, #0575E6 top-left → #021B79 bottom-right. White "f" top-right. | **Every appendix slide** |
> | **CUSTOM** | Reverse gradient, no placeholders. | Cover only |
>
> **Delete every inherited placeholder on each new slide, then place your own shapes.** The layout
> placeholders are Google-Slides leftovers at odd positions and will fight you.
>
> ## A2. THE SAFE BOX — nothing may cross these lines
> - **Content box: x 0.45 → 9.55 (9.10 in wide) · y 0.30 → 5.30.** The white card ends at 9.78/5.45;
>   the extra quarter-inch is the optical margin that stops the design touching the frame.
> - **LOGO NO-GO ZONE: x 8.80 → 9.78, y 0.30 → 0.95.** The "f" lives there on every layout.
>   **Action titles therefore wrap at 8.30 in wide, never 9.10.** This is the single most common
>   error — a title that runs under the logo makes the whole deck look unfinished.
> - Slide-number placeholder sits at x 9.27, y 5.10. Leave it; do not put content under it.
>
> ## A3. VERTICAL ZONES — identical on all 8 content slides
> ```
> 0.28 – 0.34   progress rail: 8 ticks + section name (left) + "SLIDE n OF 8" (right)
> 0.52 – 1.12   ACTION TITLE      max 2 lines, 15.5pt, width ≤ 8.30
> 1.14 – 1.38   KICKER            one sentence, 7.5pt italic
> 1.44 – 4.60   EXHIBIT ZONE      3.16 in tall = 56% of the slide. THIS IS THE SLIDE.
> 4.64 – 4.72   (optional) full-width limit/callout strip, 0.34 tall, ending by 4.72
> 4.76 – 5.10   SO-WHAT BAND      full-width navy, one sentence
> 5.29 – 5.45   FOOTNOTE          5.5pt italic, one line
> ```
> **The exhibit zone must never be more than 40% text.** If you are writing paragraphs into it, you
> have built the wrong thing — convert to a table, a chart, a schematic or a row of stat tiles.
>
> ## A4. THE GRID
> 12 columns across 9.10 in: **column 0.667 in, gutter 0.10 in.** Only these splits are allowed:
> `6+6` (4.45 each) · `4+8` (2.97 / 6.03) · `5+7` (3.75 / 5.25) · `4+4+4` (2.97 each) ·
> `3+3+3+3` (2.20 each). Panels start on a column line. Never eyeball a position.
>
> ## A5. COLOUR — taken from the template's own gradient, not invented
> **On white (content slides)**
> | Role | Hex | Where |
> |---|---|---|
> | Ink | **#0B1F3A** | all body text, table body |
> | Primary | **#0575E6** | the template's own blue — panel headers, primary chart series |
> | Deep | **#021B79** | the so-what band fill, table header fill |
> | **Answer / highlight** | **#FFC220** | ONE number per slide, and the operative clause in the band |
> | Positive | **#1E7A46** | a result that clears a threshold |
> | Negative / limit | **#C0392B** | risks, limits, the thing that fails |
> | Text secondary | **#5A6785** | kickers, captions, table labels |
> | Hairline | **#E3E8F0** | rules, table lines, card borders |
> | Panel fill | **#F5F8FD** | stat tiles, zebra rows |
>
> **On blue (appendix, CUSTOM_2)**
> Text #FFFFFF · secondary #A9BEDF · card fill **#0E2A63** (solid, so it sits above the gradient) ·
> hairline #2E5AA8 · accent #FFC220 · chart tints #6FA0FF, #7BD3A6, #FF9A8B.
>
> **Colour discipline — this is what separates a consulting deck from a student deck:**
> gold means *the answer*, red means *the limit*, green means *clears the bar*, everything else is
> navy or grey. **Four colours on a slide means no argument.** Never colour a shape decoratively.
>
> ## A6. TYPE — at this canvas size, these are the sizes that actually fit
> Segoe UI throughout (never Calibri). Consolas for monospace blocks.
> | Element | Size | Weight |
> |---|---|---|
> | Action title | 15.5pt | bold, line spacing 0.92 |
> | Kicker | 7.5pt | italic, #5A6785 |
> | Panel header bar | 6.5pt | bold caps, white on #021B79 |
> | Body / annotation | 7pt | regular |
> | Table header | 6pt | bold caps, #5A6785 |
> | Table body | 6.5pt | regular; the key column bold |
> | Stat tile number | 13pt | bold |
> | Hero number (moneyshot) | 24pt | bold, #FFC220 |
> | Monospace block | 6.5pt | Consolas |
> | Band | 8pt | regular, operative clause bold gold |
> | Footnote | 5.5pt | italic |
> **Rule: if content does not fit at 7pt, cut content. Never go below 6pt to make something fit.**
>
> ## A7. THE FIVE OBJECT STYLES — build once, reuse everywhere
> 1. **PANEL HEADER** — rounded rect, fill #021B79, height 0.22, corner 0.05, text 6.5pt bold caps
>    white, left-aligned with 0.08 inset. Every exhibit sits under one. This is what creates
>    *segregation* — the eye reads header → exhibit → caption, three times per slide.
> 2. **STAT TILE** — rect, fill #F5F8FD, no border, **3pt accent bar on the left edge** in the
>    semantic colour. Inside: 6pt caps label / 13pt bold number / 5.5pt grey sub-line. Height 0.50.
> 3. **CALLOUT** — white fill, 1pt border in the semantic colour, corner 0.05, 6.5pt caps label in
>    that colour then 6.5pt body. **Max three lines.** Gold border = insight. Red border = limit.
> 4. **BAND** — full-width rect at y 4.76, height 0.34, fill #021B79, 8pt white text, the operative
>    clause in bold #FFC220. Exactly one sentence.
> 5. **DATA TABLE** — header row fill #021B79 white 6pt caps; body rows 6.5pt; **horizontal hairlines
>    only, no vertical rules**; alternate rows #F5F8FD; numbers right-aligned; the decisive column bold.
>
> ## A8. SPACING — the rules that kill white space
> - Gap between panels: **0.10 in** (the gutter). Gap between a header bar and its exhibit: 0.05.
>   Gap between an exhibit and its caption: 0.06. Nothing else gets its own spacing value.
> - **No empty rectangle larger than 1.0 × 1.0 in anywhere inside the content box.** If one appears,
>   the fix is to widen the neighbouring exhibit, not to add filler text.
> - **No panel with fewer than three lines of content.** Delete it and give its space to the exhibit.
> - A chart is never narrower than 2.2 in (3 columns) — below that it is unreadable and should become
>   a table or a stat tile instead.
> - Captions under exhibits run the full width of the exhibit, never a narrow column.
>
> ## A9. HOW EVERY EXHIBIT MUST BE DRAWN
> - **Annotate on the plot.** The insight sits beside the mark it describes. No legends where a direct
>   label will do. No "see note below".
> - **Zero-based axes** on anything arguing about distance to zero.
> - **One number per slide is gold.** Everything else is navy, grey, or semantic.
> - Charts already exist as transparent PNGs and drop straight onto either background:
>   `Model/charts/light/*.png` for content slides, `Model/charts/dark/*.png` for appendix.
>   Available: `lever_ladder_s5`, `district_screen`, `universe_narrow`, `metro_squeeze`,
>   `roce_ladder`, `pnl_bridge`, `basket_ladder`, `risk_tornado`, `waterfall`, `relocate_hold`,
>   `asset_turn_identity`, `lever_rank`, `funnel`, `cliff`, `curfew`, `scatter`, `discriminate`.
>   **Native PowerPoint charts and tables are preferred where I will need to edit them; use the PNG
>   where the chart is annotation-heavy.** Each slide below says which.
> - Every exhibit gets a 6pt caps label "EXHIBIT n" at its top-left, in the panel header bar.
>
> ## A10. WORDS
> Every headline: a concrete noun and a number. No compressed abstractions
> ("cluster-plus-catchment node" is banned — say "one dark store per 3–6 college cluster").
> **Banned entirely:** leverage, synergy, holistic, seamless, unlock, drive, enable, ecosystem,
> journey, best-in-class, world-class, paradigm, deep dive, going forward, at scale, game-changer,
> disruptive, innovative, cutting-edge, robust (unless statistical), strategic (as filler),
> significant (give the number), optimise (unless naming an optimisation), curated, bespoke.
> Sentences ≤ 16 words. Units on every number (/day, /order, ×, pp, months, ₹ L, ₹ cr).
>
> Confirm you have this. I will send one slide at a time.

---

# PART B — ONE PASTE PER SLIDE

Each block gives you a **layout map in inches**, then the content. Build the map first as empty
shapes, check nothing crosses the safe box, then fill.

---

## SLIDE 1 — THE RECOMMENDATION

```
LAYOUT MAP (CUSTOM_3)
 rail 0.45→9.55 @0.28   "RECOMMENDATION"                       "SLIDE 1 OF 8"
 title 0.45→8.30 @0.52  2 lines
 kicker 0.45→9.55 @1.14
 ┌ 0.45→4.15 @1.44 ───────────┐ ┌ 4.25→9.55 @1.44 ─────────────────────────┐
 │ EXHIBIT 1  the node, drawn │ │ EXHIBIT 2  four stat tiles in a 2×2      │
 │ 3.70 wide × 1.80 tall      │ │ each 2.55 × 0.50, gutter 0.10            │
 └────────────────────────────┘ └──────────────────────────────────────────┘
 ┌ 0.45→4.15 @3.34 ───────────┐ ┌ 4.25→9.55 @2.56 ─────────────────────────┐
 │ decision list, 6 rows      │ │ EXHIBIT 3  two-column comparison table   │
 │ label 0.72 wide + text     │ │ 4 body rows, 5.30 wide × 1.90 tall       │
 └────────────────────────────┘ └──────────────────────────────────────────┘
 limit strip 0.45→9.55 @4.64 (red callout, 1 line)
 band @4.76 · footnote @5.29
```

**Action title (15.5pt, 2 lines):**
One dark store per 3–6 college cluster, sited on the academic calendar rather than the campus —
₹325 lakh of capital returning 33%, with a 90-day gate before the second node

**Kicker:** Two demand pools underwrite the node, not one: the colleges inside the gate, and ≥569 orders a day of adjacent non-student demand that is still there when the students leave.

**EXHIBIT 1 — the node, drawn as shapes.** Two rounded boxes stacked on the left: *"3–6 COLLEGE
CLUSTER · inside the gate · 8.5 months"* and *"ADJACENT CATCHMENT · ≥569 orders/day uncontested ·
12 months"*. A gold brace joins both into one navy circle 0.75 in across: **"ONE NODE · 2,000 sqft"**.
Three thin arrows out to three small labels: *asset turn 0.944 of a city store* · *break survivable by
construction* · *111 of 760 districts qualify*.

**Decision list (6 rows, label in #FFC220 caps 6pt, text 7pt):**
BUILD — 1 pilot node, 3–6 college cluster, non-metro Tier-1/2 district ·
UNDERWRITE — campus demand + ≥569 orders/day of uncontested adjacent catchment ·
FLEET — gig rider to the gate, institution-employed runner inside it ·
SLA — dynamic batch, 6-minute wait cap or 12 orders ·
BREAK — repurpose the catchment; the node never closes ·
GATE — go/no-go at day 90 on four instrumented metrics

**EXHIBIT 2 — four stat tiles (accent bars: blue, green, green, green):**
| CAPITAL EMPLOYED **₹325 L** capex ₹235 L + working capital ₹90 L | ROCE, 30% BASKET **32.7%** and 40% at AOV ₹763 against Eternal's public benchmark |
| PAYBACK **27 months** against a 56-month franchised-store benchmark¹¹ | IRR, 5-YEAR **34.4%** 31–35% across a 2–6 month ramp |

**EXHIBIT 3 — comparison table.** Header row two cells: left **"TREATED AS A COST PROBLEM"** on
#C0392B, right **"TREATED AS A SITE-SELECTION PROBLEM"** on #1E7A46, white 6pt caps. Four body rows:
| Cost problem | Site problem |
|---|---|
| Lever ladder moves the requirement 70.8% → 48.6% of term volume, then stops | 111 of 760 districts clear a four-part operational screen |
| 48.6 points still unfunded through a break that delivers nothing | Density buys the calendar back: 6.93× against a city store's 7.34× |
| Holding costs ₹31.6 L; relocating costs ₹89 L and forfeits a catchment that returns on a published date | The same node returns 32.7% at the modeled 30% basket mix |
| Network basket ₹450 against a required ₹580 | Repurposing the break is worth ₹26 of AOV — cheaper than lifting the basket |

**Limit strip (red callout, one line):** LIMIT, COMPUTED — at a 30% basket with volume 30% below plan, ROCE falls to 12.9% and payback runs to 67 months, longer than the node's 60-month life. Volume is what day 90 measures first.

**Band:** Approve one pilot node, ₹325 lakh, and a day-90 gate on four metrics. **If volume clears, node two is a siting decision we have already made 111 times.**

**Footnote:** Sources 1, 2, 4, 5, 6, 10, 11 · every figure asserted in A1 · return model A6b · district screen A7

---

## SLIDE 2 — THE MARKET

```
 rail "THE MARKET"                                            "SLIDE 2 OF 8"
 title 0.45→8.30 · kicker
 ┌ 0.45→9.55 @1.44 · red callout, 3 lines: the Starship precedent ┐
 ┌ 0.45→4.95 @1.96 ──────────┐ ┌ 5.05→9.55 @1.96 ────────────────┐
 │ EXH 4 universe_narrow.png │ │ EXH 5 metro_squeeze.png         │
 │ 4.50 × 1.55 + caption     │ │ 4.50 × 1.55 + caption           │
 └───────────────────────────┘ └─────────────────────────────────┘
 gold callout 0.45→9.55 @4.28 (Euromonitor white space)
 band @4.76 · footnote @5.29
```

**Action title:** Six in ten Indian colleges are rural and metros already run 19% above sustainable capacity — a smaller campus market than it looks, and an emptier one outside the metros

**Kicker:** Two registers, not a forecast. The first cuts our own addressable universe by 61%. The second is why we still recommend entry.

**Red callout (top):** PRECEDENT — In June 2026 Starship Technologies quit **all** US higher education after eight years and 60+ campuses, pulling ~1,200 robots. Its CEO: *"campus and grocery are fundamentally different operations: one is seasonal and contract-driven, the other is a 365-day urban business."* It did not lose to robots-versus-riders. **It lost 365-day utilisation to 8.5-month utilisation — the ratio on slide 4.** The campuses did not go dark: Avride took them on a national foodservice master agreement. A contract shape failed, not the segment.

**EXHIBIT 4** — `universe_narrow.png`. Caption: 54,014 colleges → 21,000 urban (39.4%) → 17,805 urban and non-metro, of which 1,897 are urban high-propensity standalones. Register count [6], not the 2023-24 report count [7]; the two instruments are never mixed.

**EXHIBIT 5** — `metro_squeeze.png`. Caption: 900 stores bought 152 new pin codes — 5.9 per pin code, so nine in ten went where an operator already served. Of 6,693 stores across five operators only 2,393 sit outside the metros; density per urban college is 1.35 metro against 0.13 non-metro, 10× headroom where the archetype sits.

**Gold callout:** AND IT IS UNCOUNTED — Euromonitor's Indian foodservice taxonomy has no education or institutional location type, and its household typology has no hostel or PG category. Students sit inside "Other", never broken out. This micro-market is not small in the standard dataset; it is absent from it.

**Band:** We shrink our own market on slide two and still recommend entry. **The question is not whether — it is where, and at what return.**

**Footnote:** Sources 5, 6, 7, 14, 15 · screen A7

---

## SLIDE 3 — THE DEAD ZONE

```
 rail "D1 · THE DEAD ZONE"                                    "SLIDE 3 OF 8"
 ┌ 0.45→3.30 @1.44 ─┐ ┌ 3.40→6.30 @1.44 ─┐ ┌ 6.40→9.55 @1.44 ────────────┐
 │ EXH 6 arithmetic │ │ EXH 7 lever      │ │ EXH 8 the solver, mono block │
 │ mono card 1.10   │ │ ladder PNG 1.35  │ │ 3.15 × 1.65 + 2-line caption │
 │ + read-line      │ │ + caption        │ │                              │
 ├──────────────────┤ └──────────────────┘ └──────────────────────────────┘
 │ EXH 9 fixed-base stacked bar 0.45→6.30 @3.10, height 0.22 + labels     │
 │ + red line: the 'other fixed' admission                                │
 band @4.76 · footnote @5.29
```

**Action title:** Cost levers cut the demand the node needs through the break from 70.8% to 48.6% of term volume — then stop, 48.6 points above a break that delivers nothing

**Kicker:** The fixed base is ₹9,02,000 a month and 71.2% of it can be flexed. Flexing every rupee is not enough, and the arithmetic says so before we do.

**EXHIBIT 6 — the arithmetic (mono card, Consolas 6.5pt):**
```
σ  = 12 / m = 12 / 8.5 = 1.412          calendar surcharge
r* = F_break / (30 · V · CM)
at breakeven CM,  r* = 1 / σ = 70.8%
```
Read-line (7pt): **The do-nothing threshold is the calendar surcharge inverted.** The same constant closes the argument from two directions.

**EXHIBIT 7** — `lever_ladder_s5.png`. Caption: the shaded band is the residual no lever reaches. The ladder cuts the requirement 31% — 992 orders/day down to 681 — and then stops.

**EXHIBIT 8 — the solver (mono, gold left bar on the REPURPOSE row):**
```
minimise   dead-zone cash burn = break deficit + reactivation
s.t.       reactivation lead ≥ 28 days · SLA ≤ 27.1 min at peak
           revocation ≥ 513 orders/day · no calendar-indexed lease
           7-week rule · basis: residual r = 0%, CM ₹30.3 at AOV ₹580

STRATEGY          DEAD ZONE   RESID DEM   REACTIVN   DAYS→SVC
DO_NOTHING          ₹31.6 L      70.8%          ₹0          0
LABOUR_FLEX         ₹21.6 L      59.1%   ₹2,74,119         28
COLD_RIGHTSIZE      ₹21.2 L      57.0%   ₹2,74,119         28
SMALL_FORMAT        ₹18.5 L      48.6%   ₹2,74,119         28
REPURPOSE            ₹0.0 L      48.6%          ₹0          0  ← BEST
```
Caption: **REPURPOSE is not a cost configuration.** It runs the small-format cost base and fills 48.6% from adjacent catchment. Residual campus population supplies only 8–15%, so the demand side is most of the answer — which makes D1's largest problem a siting decision.

**EXHIBIT 9 — the fixed base as one 100% stacked bar:** rent 24.1% (gold) · in-store staff 41.6%
(navy) · utilities and cold chain 5.6% (green) · other fixed 28.8% (grey). Bracket the first three:
**71.2% can be flexed.** Red line beneath: *"Other fixed" ₹2,59,660 is a residual we allocated from a
blended ₹100/sqft line, not an itemised figure — the least defensible number in our stack.*

**Band:** Cost is exhausted at 48.6% and a break delivers zero. **The gap has to be filled by demand, which makes it a question about where the store is, not how it is run.**

**Footnote:** Sources 1, 11, 17, 18 · last mile ₹19.0/order derived on slide 6 · solver A4 · fixed-base derivation A5

---

## SLIDE 4 — THE MONEYSHOT AND THE RETURN

```
 rail "THE RETURN"                                            "SLIDE 4 OF 8"
 ┌ 0.45→5.35 @1.44 · EXH 10 the identity, one wide card, height 0.56 ─────┐
 ┌ 0.45→5.35 @2.06 · EXH 11 four sensitivity cells, 1.20 wide each ───────┐
 ┌ 0.45→5.35 @3.06 · EXH 12 DuPont mono card, height 0.92 ────────────────┐
 ┌ 5.45→9.55 @1.44 · EXH 13 roce_ladder.png 4.10 × 1.42 ─────────────────┐
 ┌ 5.45→9.55 @3.00 · five-row fact list (breakeven → benchmark → premium)  ──┐
 red callout 0.45→5.35 @4.06 (two asset turns) · band @4.76 · footnote
```

**Action title:** Campus density buys back the academic calendar almost exactly — and reaches Eternal's public 40% ROCE benchmark at ₹763

**Kicker:** Asset turn is the turnover leg of ROCE. The node clears that leg at 94% of a city store. The margin leg is what the basket has to buy.

**EXHIBIT 10 — the identity, as a visual equation on one card:**
`(1,400 / 1,050) × (8.5 / 12) = 1.333 × 0.708 = ` **0.944** ← 24pt gold, the only gold number on the slide.
Sub-line: density +33.3% · calendar −29.2% · campus 6.93× against a city store's 7.34× · the dead zone costs 5.6 points of asset productivity, not 30.

**EXHIBIT 11 — throughput sensitivity, four cells:** 1,000/day → 0.675 · 1,200/day → 0.810 ·
**1,400/day → 0.944** (navy fill, white text) · 1,482/day → 1.000 parity (gold outline).
Caption: Blinkit's own observed nine-quarter range is 1,334–1,487 orders/day². Across all of it the node runs 0.90–1.00. Parity = city throughput × the calendar surcharge = 1,482, which is 99.7% of the observed maximum. At 1,000/day the ratio is 0.675 and the density argument weakens.

**EXHIBIT 12 — DuPont (mono):**
```
ROCE = EBIT/CE = (EBIT/NOV) × (NOV/CE)     DuPont
                  margin leg   turnover leg
     = 4.71%    ×   8.50×     =  40.0%     at AOV ₹763
AOV* = (ROCE·CE + F·12)/(τ·N) + c/τ        closed form, no search
```

**EXHIBIT 13** — `roce_ladder.png`, then a five-row fact list beneath it:
AOV for ROCE = 0 **₹578** · AOV for the 40% benchmark **₹763** · premium over breakeven **₹185** ·
non-grocery mix it implies **33.0% of GOV** · Swiggy disclosed reference range **30–40%**

**Red callout:** TWO ASSET TURNS, BOTH CORRECT — QUOTE THE BASIS. The 6.93× is a like-for-like comparison at a common AOV of ₹450, which is what isolates density × calendar. The DuPont leg (8.50×) is the node's own turnover at its achieved AOV on capital employed including working capital.

**Band:** Breakeven is not the return benchmark. **₹578 earns zero on ₹325 lakh; ₹763 earns 40%** — and the site is what supplies the throughput either one needs.

**Footnote:** Sources 1, 2, 4, 8, 10, 11 · ROCE model, DuPont reconciliation and the day-count note A6b

---

## SLIDE 5 — SITE SELECTION

```
 rail "SITE SELECTION"                                        "SLIDE 5 OF 8"
 ┌ 0.45→3.30 @1.44 EXH 14 filter mono card + caption ─┐
 ┌ 3.40→6.35 @1.44 EXH 15 district_screen.png ────────┐
 ┌ 6.45→9.55 @1.44 EXH 16 ranked district table ──────┐
 ┌ 0.45→3.30 @3.10 EXH 17 four requirement columns ───┐
 ┌ 3.40→6.35 @3.10 gold callout: the convergence  ────┐
 ┌ 6.45→9.55 @3.10 red callout: what the flag can't do┐
 band @4.76 · footnote @5.29
```

**Action title:** Underwrite on 569 orders a day of uncontested adjacent demand: 111 districts of 760 clear the screen, and we then disqualified 72% of our own shortlist

**Kicker:** The filter binds on losing the campus, not on surviving the break — 513 orders a day against 471 — so it is set at the higher of the two.

**EXHIBIT 14 (mono):**
```
D_adj ≥ max(D_solvency, D_revocation) / (1 − κ)
κ = contested share of the adjacent catchment
7-WEEK RULE, derived:  21d wind-down + 28d ramp = 49d
```

**EXHIBIT 15** — `district_screen.png`.

**EXHIBIT 16 — ranked candidates (data table):** District · State · Urban colleges · Resid index ·
Expected incumbent. Khordha, Odisha, 169, 20.1, 23 · Kalaburagi, Karnataka, 229, 11.2, 31 · Belagavi,
Karnataka, 190, 11.2, 26 · Visakhapatnam, Andhra Pradesh, 133, 15.0, 18 · Dharwad, Karnataka, 160,
11.2, 22 · Dakshina Kannada, Karnataka, 158, 11.2, 21.

**EXHIBIT 17 — four columns:** 0% contested → 569/day · 10% → 632 · 25% → 758 · 44% → 1,015 (red,
"metro five-operator overlap"). Caption: only the metro overlap is published, so we quote the band.

**Gold callout:** CONVERGENCE — Karnataka and Odisha were chosen at state level from residential intensity and hostel occupancy. The district register, a different table pulled later, puts 14 of the top 20 in Karnataka and Khordha first. The state was not picked and then justified.

**Red callout:** WHAT THE FLAG CANNOT DO — expected incumbent stores = urban colleges × non-metro density, so "uncontested" is arithmetically "6–7 urban colleges": the nine clean districts are the nine smallest. The flag ranks; it does not site. There is no large empty district, and the plan does not need one — demand inside the gate is uncontested by construction.

**Band:** Site chosen, break survivable, revocation hedged. **Now it has to run inside a gate an incumbent cannot pass without the same permission we need.**

**Footnote:** Sources 5, 6, 7 · the register carries no enrolment, so district student counts are imputed off state ratios · full screen A7 · calendar shapes A7b

---

## SLIDE 6 — THE OPERATING MODEL

```
 rail "THE OPERATING MODEL"                                   "SLIDE 6 OF 8"
 ┌ 0.45→4.15 @1.44 EXH 18 split-trip schematic 3.70 × 1.30 ──┐
 ┌ 4.25→9.55 @1.44 EXH 19 SLA scenario table 5.30 × 1.10 ────┐
 ┌ 0.45→4.15 @2.86 EXH 20 labour-class table ────────────────┐
 ┌ 4.25→6.85 @2.86 EXH 21 trip/batch mono card ──────────────┐
 ┌ 6.95→9.55 @2.86 EXH 22 UC Davis precedent tiles ──────────┐
 three stat tiles 0.45→9.55 @4.10 (store floor · runner floor · market)
 red concession strip @4.64 · band @4.76 · footnote
```

**Action title:** Split the trip at the gate and pay for the batch with time — last mile falls from ₹42.0 to ₹19.0 an order, and the product is fastest at exam-night peak

**Kicker:** Two decisions on one page. The fleet is a labour class, not a vehicle. The SLA is a batching rule, not a promise.

**EXHIBIT 18 — split-trip schematic (shapes):** store → thick arrow *"city leg · gig rider · ₹168 per
ACTIVE hour"* → gate → four thin arrows to hostel blocks *"in-gate leg · employed runner · ₹72 per
ROSTERED hour"*. Dashed vertical line through the gate: **the labour class changes here — 2.33×, and 1.60× on the least favourable anchor.**

**EXHIBIT 19 — SLA table:** Trough 6.5/hr, batch 1, 25.7 min, ₹64.8 · Average 25.9, 2, 21.6, ₹33.0 ·
**Peak 4× 103.7, 10, 27.1, ₹7.7** · Exam night 6× 155.6, 12, 27.1, ₹6.6.
Annotation in gold: a 4× spike needs 1.4× the runners — absorbed by batch size, not headcount. 62.7% of orders fall in the peak band, which is why the volume-weighted cost is ₹19.0 and an average-hour calculation would say ₹33.0.

**EXHIBIT 20 — labour class table:** Gig quick-commerce 0 / ₹42.06 / ₹2.36 / ₹168 / 40% / any ·
Gig JM non-metro 0 / ₹43.96 / ₹2.36 / ₹176 / 36% / any · **Employed runner ₹577 / ₹4.66 / ₹0 / ₹72 /
100% / 87 a day.** Caption: the threshold is **solved**, not chosen. The incentive column is
**flagged, not invented** — the rider-survey split is in our corpus but not in any module.

**EXHIBIT 21 (mono):**
```
t_trip  = 2·(d/v) + b·τ            C/order = (w/60)·t_trip / b
b(λ)    = min(K, ⌈λ·W/60⌉)         W = 6-min cap, K = 12
Little's Law   L = λ·W
```

**EXHIBIT 22 — precedent tiles:** $2.00 per package · 12 packages per stop against 3 for a truck (4×) ·
99.6% same-day · our fee band ₹9.6–₹29.2. Caption: scope it as continuous circuits, never as the parcel
desk's accumulate-and-sort round — that scoping error kills the service level, not the economics.

**Three stat tiles:** STORE FLOOR 681/day · below it the node cannot fund its fixed base |
RUNNER FLOOR 87/day · below it the gate leg reverts to gig | MARKET 53% of riders now batch >20% of
orders, up from 42%¹²

**Red strip:** CONCESSION — 11 minutes is a marketing number. Walmart's own CEO says under 13¹³, Euromonitor 15–20¹⁴, our 35-store field survey median 15 with 9% at ten or under³. The two ten-minute operators in J.P. Morgan's table did not batch¹¹.

**Band:** Both decisions are cheap and reversible. **Together they are the ₹19.0 an order the whole D1 case rests on.**

**Footnote:** Sources 1, 3, 11, 12, 13, 14, 16 · trip identity and volume weighting A5 · labour-class provenance A2

---

## SLIDE 7 — THE FINANCIALS

```
 rail "THE FINANCIALS"                                        "SLIDE 7 OF 8"
 ┌ 0.45→4.85 @1.44 EXH 23 pnl_bridge.png 4.40 × 1.50 ────────┐
 ┌ 0.45→4.85 @3.10 four capital rows ────────────────────────┐
 ┌ 4.95→7.15 @1.44 EXH 24 basket_ladder.png ─────────────────┐
 ┌ 7.25→9.55 @1.44 EXH 25 returns fact list, 6 rows ─────────┐
 ┌ 4.95→9.55 @3.10 EXH 26 scenario table, 4 rows ────────────┐
 red callout 0.45→9.55 @4.30 (the limit) · band @4.76 · footnote
```

**Action title:** One node earns ₹130 lakh of EBIT and 32.7% on capital at a 30% non-grocery basket, and reaches Eternal's public 40% benchmark at ₹763

**Kicker:** The basket is fitted, not assumed — the one disclosed quarterly series where an Indian operator actually lifted AOV. Every point of non-grocery mix is worth ₹11.28.

**EXHIBIT 23** — `pnl_bridge.png`. Header line above it: 361,958 orders a year at AOV ₹763, NOV ₹27.6 cr.

**Capital rows:** capex, midpoint of the band **₹235 L** · working capital at 14 NWC days **₹90 L** ·
**capital employed ₹325 L** · cash conversion cycle **−47 days — the node is supplier-funded**⁹

**EXHIBIT 24** — `basket_ladder.png`. Caption: ₹450 → ₹525 on term-start durables → ₹580 at 24.9%
non-grocery, from 20% today. The 40% benchmark needs 33.0% — within Swiggy's disclosed 30–40% range,
with 7.0 points of headroom. This is a cross-operator reference, not a Flipkart commitment.

**EXHIBIT 25 — returns:** breakeven AOV ₹578 · benchmark AOV, pre-tax **₹763** · post-tax at 25.17% ₹825 ·
IRR, 5-year, 3-month ramp **34.4%** · ramp 2–6 months 35%–31% · node life anchor 56-month payback¹¹

**EXHIBIT 26 — scenarios (data table):**
| Scenario | AOV | Margin | Turn | ROCE | Payback |
|---|---|---|---|---|---|
| Underwritten, at breakeven | ₹578 | 0.00% | 6.44× | 0.0% | — |
| Basket at 30% non-grocery | ₹729 | 4.03% | 8.12× | **32.7%** | 27 mo |
| Basket at 40% non-grocery | ₹842 | 6.09% | 9.38× | **57.1%** | 15 mo |
| **30% basket, volume −30%** | ₹729 | 2.27% | 5.69× | **12.9%** | **67 mo** |

**Red callout:** THE LIMIT, COMPUTED NOT ASSERTED — at a 30% basket with volume 30% below plan the node returns 12.9% and pays back in 67 months, longer than the 60 months its life is anchored on. Under that combination it does not pay back within its life. That is why day 90 measures volume before anything else, and why node two is not funded until it clears.

**Band:** The modeled basket mix falls within Swiggy's disclosed range; this does not establish Flipkart feasibility. **One dependency binds: term volume.**

**Footnote:** Sources 2, 4, 8, 9, 10, 11 · P&L, capital and ROCE derivation A6b · basket fit R²=0.918 on four disclosed quarters A6 · NPV at 12%/15% assumes a discount rate; no WACC is disclosed

---

## SLIDE 8 — ROADMAP, RISK, GATE

```
 rail "ROADMAP · RISK · GATE"                                 "SLIDE 8 OF 8"
 ┌ 0.45→5.75 @1.44 EXH 27 Gantt, 4 lanes × 12 weeks, 2.60 tall ┐
 ┌ 5.85→9.55 @1.44 EXH 28 gate metrics table ──────────────────┐
 ┌ 5.85→9.55 @2.90 EXH 29 risk_tornado.png ────────────────────┐
 ┌ 0.45→5.75 @4.10 gold callout: the three concessions ────────┐
 band @4.76 · footnote @5.29
```

**Action title:** Ninety days to a measured go/no-go: four workstreams, four instrumented metrics carried forward from Round 1, and one dependency that can stop the rollout

**Kicker:** Every action fires on a calendar date, never on observed volume. Semester demand steps rather than ramps, so by the time volume tells you, you are already late.

**EXHIBIT 27 — a real Gantt.** Four lanes with owners in the left column, weeks 1–12 across the top:
| Lane (owner) | Bars |
|---|---|
| SITE & LICENCE (Contracts) | W1–2 shortlist 6 sites in 2 districts · W3–5 campus licence **with a dormancy clause in supplier terms** · W6 sign |
| NODE BUILD (Cluster ops) | W3–6 fit-out 2,000 sqft, one chilled zone · W7–9 hire 25 staff, four-week rehire lead |
| FLEET & PARTNER (Fleet) | W5–8 runner agreement, per-parcel fee tied to an SLA · W8–10 e-cart circuits, OTP chain of custody |
| COMMERCIAL (Category) | W6–9 non-grocery mix to 25% · W10–12 campus free-delivery threshold test |
Gold diamond at week 12: **GO / NO-GO**.

**EXHIBIT 28 — the gate:** Peak-to-Trough Demand Ratio > 4.0× · Gate-Drop Consolidation Ratio ≥ 3.0× ·
Term-Weighted CM + Break Runway ≥ 1.0× · Calendar-Linked Labour Share ≥ 50%. Caption: these are Round
1's metrics doing the job they were designed for — the cumulative build the brief asks for, made
operational rather than restated.

**EXHIBIT 29** — `risk_tornado.png`. Caption: volume −30% → ₹647 · shrinkage → ₹623 (upper bound) ·
gig levy → ₹595 · fragmentation → ₹589. Three of four are covered inside a 30% basket (₹729); all four
inside 40% (₹842). Shrinkage is an upper bound — the stack was calibrated on a reported contribution
figure already net of it, so charging it again double-counts.

**Gold callout:** WHAT WE CONCEDE, BEFORE YOU ASK — 11 minutes is marketing (slide 6). The industry relocates rather than mothballs, and we never proposed mothballing: holding costs 24% of one move. We are not first — Swiggy, Blinkit and Zepto are all in this segment. None underwrites the node on the cluster rather than the campus.

**Band:** Approve one node, ₹325 lakh, and a day-90 gate on four metrics. **If volume clears, node two is a siting decision we have already made 111 times.**

**Footnote:** Sources 8, 13, 19, 20, 21 · shock derivations A5 · assumption ledger A3 · fragmentation A7b

---

# PART C — THE APPENDIX (switch to CUSTOM_2)

> Same grid, same object styles, same zones. Only the palette changes: text #FFFFFF, secondary
> #A9BEDF, **cards get a solid #0E2A63 fill** (a transparent card over a gradient looks like a mistake),
> hairlines #2E5AA8, accent stays #FFC220. **Use the `Model/charts/dark/*.png` versions** — they are
> the same charts recoloured for this background, already generated.
> The gradient runs light at top-left to deep navy at bottom-right, so **put dense content on the
> right half of appendix pages** where the background is darkest and contrast is highest.
>
> First appendix page is a divider: **"APPENDIX · THE VERIFICATION KIT"** with one line —
> *"Every number on the eight slides is asserted in code. This is the code, the sources, and what we
> examined and threw away."* — and a four-cell strip: 311 assertions · 31 document figures ·
> 79 spec figures · 80 deck checks.
>
> Then A1–A10 exactly as specified in `DECK_ASSET_PLAN_SemiFinal.md`, which also says which Colab link
> and which screenshot belongs on each page.
