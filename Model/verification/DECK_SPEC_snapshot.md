# DECK SPEC — Semi-Final, all 8 slides + appendix

> **SLIDE ORDER SUPERSEDED [S31].** `DECK_ARCHITECTURE_SemiFinal.md` carries the current order:
> 1 recommendation · 2 market · 3 dead zone · 4 moneyshot + return · 5 site · 6 operating model
> (fleet + SLA merged) · 7 financials · 8 roadmap, risk, gate. **Every content block below still
> stands** — Part 0 (rules), the copy, the math boxes, the napkin prompts and the appendix map are
> unchanged; four blocks are re-homed and two new slides (financials, roadmap) are specified in the
> architecture file. Build from the architecture file's order and this file's content.
*The single build reference. Written 2026-08-28 against `audit.py` 291/291, `verify_docs.py` 31/31.*
*Every figure below is in the model. If you retype one, run `python3 Model/verify_deck.py <your.pptx>`
after export — it parses the built file and fails on a number that drifted or a Round 1 figure that crept back.*

---

# PART 0 — THE RULES THIS DECK IS BUILT ON

## 0.1 Citation: numbered, not narrated
No "Source:" prose on any content slide. Instead:

- A superscript numeral sits against the figure: `₹9,02,000¹` · `1,334–1,487²` · `54,014⁶`.
- The numeral is **global** — [4] means TechCrunch on slide 1 and on slide 8.
- One line at the very bottom of each slide, 6pt, grey: `Sources 1,2,11 · Assumptions A3 · Derivation A5`
- The master register lives on **A2**, sorted by number, with exhibit and date.

Last year's winner carried **zero** citations on eight content slides and still won. So citation is not
table stakes — which is exactly why doing it in a form that costs no space is cheap credibility.

**Master source register** (use these numbers everywhere):

| # | Source |
|---|---|
| 1 | JM Financial, Eternal model — dark-store cost stack, Exhibits 12/13; tier rent bands Exhibit 5 |
| 2 | JM Financial, Exhibit 29 — Blinkit orders/day/store, nine quarters |
| 3 | JM Financial, Exhibit 33 + 35-store field survey — non-metro multiple, observed delivery times |
| 4 | TechCrunch, 22 Aug 2026 — Minutes AOV ₹400–500, Flipkart internal data, confirmed by the reporter |
| 5 | Bernstein via Economic Times, 18 Jul 2026 — store counts, pin codes, five-operator overlap, metro capacity |
| 6 | AISHE institution register, as on 28-8-2026 — 54,014 colleges, urban/rural flag, district |
| 7 | AISHE 2023-24 report — enrolment, hostel occupancy. **Different instrument from [6]. Never mix a count from one with an enrolment from the other.** |
| 8 | Eternal / Blinkit FY26 disclosures — take rate 19.41%, contribution ₹29.4/order, shrinkage 1.8% of NOV, NWC days |
| 9 | Zepto, MCA-filed audited consolidated accounts — 13 days inventory, ~60 days payables |
| 10 | Swiggy Instamart quarterly disclosures — non-grocery share of GOV vs AOV; disclosed 30–40% reference range |
| 11 | J.P. Morgan quick-commerce channel work — 4.0 orders/active hour, sub-2km leg, rider cost; Physicswallah note 9 Jul 2026 |
| 12 | UBS Evidence Lab rider survey, n=100, Nov–Dec 2025 — batching incidence, food-delivery productivity |
| 13 | Walmart Q1 FY27 earnings call, 21 May 2026 — >800 MFCs, <13 minutes, >30 cities |
| 14 | Euromonitor International — Consumer Foodservice by Location in India, Mar 2026; household typology |
| 15 | Food On Demand, 10 Jun 2026 — Starship exit; Avride–Chartwells master services agreement |
| 16 | UC Davis Finance, Operations & Administration — Last Mile Initiative |
| 17 | CRISIL — warehousing occupier contracts, fixed-cost share, power tariffs |
| 18 | Kambli, Sinha & Srinivas (2020), *J. Hospitality & Tourism Mgmt* 43, 62–70, DOI 10.1016/j.jhtm.2020.02.008 |
| 19 | Parliamentary Standing Committee, 201st report, 7 Aug 2026 — gig social-security levy |
| 20 | Netscribes / Elara via EMIS — Flipkart 650 festive-only hubs, 2.2 lakh seasonal jobs; Swiggy student programme |
| 21 | Company announcements — Zepto Express Prints 18 Apr 2026; Blinkit–Adani CSMIA 1 Apr 2026; Swiggy YISU MoU Jan 2026 |
| 22 | VOC 2026 consumer survey, n=1,002 — Gen Z consumption occasions |

## 0.2 Density: the 12-column grid, and no empty quarters
16:9. Margins 0.45in. **12 columns, 8 rows.** Every slide fills six blocks:

```
┌─ action title (12 cols × 1 row) ──────────────────────────────────┐
├─ kicker: the mechanism in one line (12 × 0.5) ────────────────────┤
├─ MATH BOX (4 cols × 2.5)  │ EVIDENCE / CHART (8 cols × 2.5) ──────┤
├─ PARAMETER TABLE or LADDER (7 × 2.5) │ TRADE-OFF / LIMIT (5 × 2.5) ┤
├─ so-what band (12 × 0.6) ─────────────────────────────────────────┤
└─ footnote line (12 × 0.25) ───────────────────────────────────────┘
```
Rules that kill white space: no chart smaller than 3 columns; no box with fewer than 3 lines of content;
tables run to the panel edge; every panel has a 6.5pt ALL-CAPS label bar. If a panel is thin, the
content is thin — cut the panel and widen its neighbour, don't stretch it.

## 0.3 Voice: how the copy is written
Operator's voice, not essay voice.

- **Do:** noun-verb-number. *"Batch closes on a 6-minute cap or 12 orders."*
- **Don't:** "It is not X — it is Y." "Said before you ask." "The uncomfortable part." "Worth saying out loud."
- Labels are flat and technical: `ASSUMPTION EXPOSED` · `SENSITIVITY` · `LIMIT` · `PRECEDENT` · `TRIGGER` · `OWNER`.
- No rhetorical questions. No "simply", "clearly", "crucially". One idea per line, ≤14 words.
- Units on every number: `/day`, `/order`, `/month`, `pp`, `×`, `bps`.
- Where we concede, concede in four words and move: *"11 minutes is marketing.¹³"*

## 0.4 The four things that make this read as depth, not decoration
1. **A formula box on every operating slide**, with symbols defined and our value substituted. Nobody else does this.
2. **Parameter tables with units and provenance tier** `[T1 disclosure / T2 press / D derived / A assumed]`.
3. **A solved variable where others assume one.** Say which is which, per slide.
4. **A stated limit on every slide** — the sensitivity that hurts, in our words, in the same type size as the result.

---

# PART 1 — THE EIGHT SLIDES

---

## SLIDE 1 — RECOMMENDATION

**Action title**
> Enter on a cluster-plus-catchment node: 94% of a city store's asset productivity, at a site chosen so the academic break is survivable.

**Kicker**
> One node serves a 3–6 college cluster **and** its adjacent non-student catchment. The academic calendar enters as a site-selection criterion, not a cost line. 3-month build.

**Panel A — THE DECISION (4 cols)**
```
BUILD        1 pilot node, 3-6 college cluster, non-metro Tier-1/2 district
UNDERWRITE   campus demand + >=569 orders/day of uncontested adjacent catchment
FLEET        gig to the gate; institution-employed runner inside the gate, per-parcel fee
SLA          dynamic batch, 6-min wait cap or 12 orders. Not a 10-minute promise.
BREAK        repurpose the catchment. Node stays open in every configuration.
GATE         go/no-go at month 3 on 4 instrumented metrics (A4)
```

**Panel B — WHY NOT A COST PROBLEM (4 cols)**

| | |
|---|---|
| Cost ladder cuts the residual demand needed | **70.8% → 48.6%** of term volume, and stops |
| Dead-zone burn, no levers | **₹31.6 L** per break |
| Relocate instead | **₹89 L** once, **₹178 L** to return |
| Network basket vs required basket | **₹450⁴ → ₹580** |

**Panel C — WHY A SITE PROBLEM (4 cols)**

| | |
|---|---|
| Districts clearing the operational screen | **111 of 760**⁶ |
| Asset turn, campus vs city, one basis | **6.93× / 7.34× = 0.944** |
| Across Blinkit's whole observed range² | **0.90 – 1.00** |
| Basket to ₹580 | **24.9% non-grocery** vs Swiggy's 30–40% disclosed range¹⁰ |
| Holding through the break vs relocating | **24% of one relocation** |

**Limit strip (full width, ruled, not shaded)**
> `NOT FIRST` Swiggy: student rewards with college canteens and hostels, Toing (AOV <₹200, ~50 cities), YISU MoU²⁰˒²¹. Blinkit: in-airport with Adani at CSMIA²¹. Zepto: Express Prints ₹2/page, ~285 stores²¹. **None underwrites the node on the cluster. That is the whole difference.**

**So-what band**
> Site the node on the cluster, price the break as a filter, enter the 111 districts where both hold.

**Footnote line** — `Sources 2,4,5,6,10,20,21 · every figure asserted in A1 · derivations A5–A7`

**Napkin prompt**
> A single wide horizontal decision spine. Left: one rounded box labelled "CAMPUS CLUSTER — 3–6 colleges". Right of it, a second box labelled "ADJACENT CATCHMENT — ≥569 orders/day". A thick gold bracket joins both into one dark navy circle labelled "ONE NODE". From the circle, three thin arrows point right to three small square outcome tiles: "asset turn 0.944", "break survivable", "111 districts". Flat vector, no gradients or shadows. Navy #0D1F5C, gold #FFC220, grey #5A6785, transparent background. Sentence-case sans-serif labels. Wider than tall.

**Kill list** — no market-size number, no roadmap, no team credentials, no "why now".

---

## SLIDE 2 — MARKET

**Action title**
> Six in ten Indian colleges are rural and metros run 19% over sustainable capacity: a smaller market than it looks, and an emptier one.

**Kicker**
> Both facts come out of registers, not forecasts. The first shrinks our own addressable universe by 61%. The second is why we still recommend entry.

**Hook strip (full width, top, red rule)**
> `PRECEDENT — THE SEGMENT HAS ALREADY KILLED AN OPERATOR` Starship Technologies exited **all** US higher education in Jun 2026: 8 years, 60+ campuses, ~1,200 robots withdrawn (40% of its global fleet)¹⁵. CEO Ahti Heinla: *"campus and grocery are fundamentally different operations: one is seasonal and contract-driven, the other is a 365-day urban business."* **It lost 365-day utilisation to 8.5-month utilisation — the ratio on slide 5. The campuses did not go dark: Avride took them on a national foodservice master agreement (~350 campuses). A contract shape failed, not the segment.**

**Panel A — THE UNIVERSE NARROWS (6 cols)** — chart `universe_narrow`
```
54,014 colleges          ->  21,000 URBAN (39.4%)  ->  17,805 urban, non-metro
                             six in ten are rural       metros hold 3,195, excluded
        of which 1,897 urban high-propensity standalones (polytechnic, PGDM, pharmacy, hotel mgmt)
```
Caption: `Register count [6], not the 2023-24 report count [7]. The two instruments are never mixed.`

**Panel B — THE DENSIFICATION WALL (6 cols)** — chart `metro_squeeze`
```
900 stores added Apr-Jul 2026   ->   152 NEW pin codes reached      5.9 stores per new pin code
five-operator metro overlap     26% -> 44% in ONE quarter
metro stores 4,300 vs 3,600 sustainable capacity                    +19%
store density per urban college  metro 1.35  |  non-metro 0.13      10.0x headroom
```

**Limit strip**
> `UNCOUNTED` Euromonitor's Indian foodservice taxonomy has no education/institutional location, and its household typology has no hostel/PG/shared-student type — students fall into "Other", never broken out¹⁴. The segment is not small in the standard dataset; it is absent from it. That is why the register had to be parsed.

**So-what band**
> We have shrunk our own market on slide two and still recommend entry. The question is not whether — it is **where**. Slide 6.

**Footnote line** — `Sources 5,6,7,14,15 · screen A7`

**Napkin prompt**
> Two panels side by side. LEFT: three vertical bars descending in height, labelled 54,014 / 21,000 / 17,805, with a thin arrow between each, under the header "colleges → urban → urban non-metro". RIGHT: one tall bar labelled "900 stores added" beside a very short bar labelled "152 new pin codes", and above them a small rising line from "26%" to "44%" labelled "pin codes served by all five operators". Flat vector, navy #0D1F5C bars, gold #FFC220 for the last bar in each panel, grey labels, transparent background, no gradients or shadows. Wider than tall.

**Kill list** — no TAM pyramid, no "₹X bn by 2030", no Gen Z lifestyle imagery.

---

## SLIDE 3 — D2 · ACCESS GEOMETRY AND THE FLEET

**Action title**
> The campus is not an expensive zone; it is expensive to serve the way we serve everywhere else. Volume-weighted last mile falls ₹42.0 → ₹19.0 per order.

**Kicker**
> Split the trip at the gate. Gig rider to the gate, institution-employed runner inside it. The fleet decision is a labour class, not a vehicle.

**MATH BOX — the trip identity (4 cols)**
```
   t_trip = 2·(d / v) + b·τ            trip minutes
   C_order = (w / 60) · t_trip / b     cost per order

   d  leg distance km      v  speed km/h      b  batch size
   τ  dwell per drop min   w  labour cost per hour of the class serving the leg

   CITY LEG   gig class,      w = ₹168/active hr   [11]
   GATE LEG   employed class, w = ₹72/rostered hr  [1,11]
   RATIO 2.33x  — on UBS's food-delivery anchor 1.60x. Direction holds on both. [12]
```
Read-line: **cost per order falls linearly in b and rises linearly in w. Only the in-gate leg can change w.**

**PARAMETER TABLE — labour class (7 cols)** *(five costed parameters per class — the format last year's winner used, with sourced inputs instead of chosen ones)*

| CLASS | FIXED/day | ₹/order | ₹/km | ₹/hour | UTIL | THRESHOLD |
|---|---|---|---|---|---|---|
| GIG · quick commerce¹¹ | 0 | 42.06 | 2.36 | 168.3 | 40% | any |
| GIG · JM metro¹ | 0 | 48.08 | 2.36 | 192.3 | 62% | any |
| GIG · JM non-metro¹ | 0 | 43.96 | 2.36 | 175.8 | 36% | any |
| **EMPLOYED RUNNER** | **577** | **4.66** | **0.00** | **72.1** | **100%** | **87/day** |

```
FIXED/day  gig = 0 is structural: paid per delivery, carries the vehicle
₹/hour     ACTIVE hours for gig, ROSTERED for the runner. Different units. That is the finding.
UTIL       40% of a gig shift is active, so we pay a premium for the 60% we do not use
THRESHOLD  SOLVED, not chosen — fleet_mix.breakeven_volume(). Theirs was an input; ours is an output.
INCENTIVE  NOT AVAILABLE. UBS base+incentive split is in the corpus, not in a module. Flagged, not invented. [12]
```

**MODE TABLE — in-gate leg, ₹/order by batch (5 cols)**

| Mode | access | n=1 | n=3 | n=8 | n=12 |
|---|---|---|---|---|---|
| Petrol 2W (incumbent) | no | 28.3 | 14.0 | — | — |
| Cycle | yes | 18.6 | 8.4 | — | — |
| On-foot | yes | 41.3 | 16.8 | — | — |
| **E-cart, stationed** | yes | **15.4** | **7.2** | **4.7** | **4.1** |

Full campus, gate-drop → e-cart, room delivery: **₹19.0 at n=4**, ₹8.4 at n=12. Door-drop by 2W: ₹31.1. Standard 2–3 km residential zone: **₹42.0**. Type A campus served door-to-door: ₹68.0.

**PRECEDENT strip**
> `INSTITUTION AS PAID OPERATOR` UC Davis runs its own in-perimeter last mile and charges per parcel: **$2/package, 12 packages per stop against 3 for a third-party truck (4×), 99.6% same-day, ~400 packages/day**¹⁶. Our fee band: floor **₹9.6** (runner cost), ceiling **₹29.2** (what the leg is worth to us). **Scope it as continuous circuits, never as the parcel desk's accumulate-and-sort round** — that scoping error kills the service level, not the economics.

**Limit strip**
> E-cart capex would have to reach **₹8 lakh** before it added ₹1/order. Priced, not asserted (A3).

**So-what band**
> A cheaper labour class only pays if the SLA permits batching. Slide 4 buys the batch.

**Footnote line** — `Sources 1,11,12,16 · parameter provenance A2 · fleet derivation A5`

**Napkin prompt**
> A split-trip schematic across the page. LEFT: a dark store icon with one thick arrow labelled "city leg — gig rider, ₹168/active hr" pointing to a tall campus GATE icon in the middle. RIGHT of the gate: one small e-cart icon with four short thin arrows fanning to four hostel-block icons, labelled "in-gate leg — employed runner, ₹72/rostered hr". Under the left arrow: "₹42.0 standard zone". Under the right fan: "₹19.0 volume-weighted". A vertical dashed line runs through the gate labelled "the labour class changes here". Flat vector, navy #0D1F5C, gold #FFC220 gate, green #1E7A46 for the right-hand fan, grey labels, transparent background, no gradients or shadows.

**Kill list** — no vehicle photos, no "EV sustainability" line, no map.

---

## SLIDE 4 — D2 · THE SLA

**Action title**
> Abandon the uniform 10-minute promise: a 6-minute batch cap makes the campus product cheapest and fastest exactly at exam-night peak.

**Kicker**
> Batch size is a function of arrival rate. As demand rises the batch fills sooner, so wait falls and cost per order collapses. The spike becomes the asset.

**MATH BOX — batching under a wait cap (4 cols)**
```
   b(λ) = min( K , ⌈ λ · W / 60 ⌉ )        batch that closes first
   SLA  = W_actual + t_trip / 2             customer-visible minutes
   W_actual = min( W , 60·K / λ )           the cap binds only below K·60/λ

   λ arrival rate orders/hr    W wait cap = 6 min    K batch ceiling = 12 (e-cart capacity)

   Little's Law on the gate queue:  L = λ · W  →  orders waiting at the gate at any moment
   One runner clears 28 orders/hour on a 21-minute circuit.
```
Read-line: **a 4× demand spike needs 1.4× the runners, because the spike is absorbed by batch size, not headcount.**

**SCENARIO TABLE (7 cols)**

| State | orders/hr | batch | batch wait | AVG SLA | LAST drop | runners | ₹/order |
|---|---|---|---|---|---|---|---|
| Trough | 6.5 | 1 | 9.3 | 25.7 | 31.3 | 1.2 | 64.8 |
| Average | 25.9 | 2 | 4.6 | 21.6 | 27.8 | 2.7 | 33.0 |
| **Peak (4×)** | **103.7** | **10** | **5.8** | **27.1** | **37.7** | **3.7** | **7.7** |
| Exam night (6×) | 155.6 | 12 | 4.6 | 27.1 | 38.8 | 5.1 | 6.6 |

**Volume weighting — why ₹19.0 and not ₹33.0**
```
band        % of orders   ₹/order
peak              62.7%       7.7
normal            31.4%      33.0
trough             5.9%      64.8
                          -------
volume-weighted             19.0     an average-HOUR calculation gives 33.0 and is wrong
standard zone               42.0     saving 55%
```
Below the **87/day** runner floor the roster is uneconomic and the gate leg reverts to gig. Two floors, stated: store floor (slide 5) and runner floor (here).

**TIER TABLE (5 cols)**

| Tier | batch | AVG SLA | ₹/order | serves |
|---|---|---|---|---|
| Express | 1 | 18.7 | 64.8 | chilled/frozen, or paid tier |
| Standard | 2 | 21.6 | 33.0 | ambient core, default |
| Scheduled slot | 12 | 30-min window | 6.6 | predictable peaks, bulk, durables |

**Limit strip**
> `CONCESSION — 11 MINUTES IS MARKETING` Walmart's own CEO says <13 min¹³; Euromonitor 15–20¹⁴; our JM 35-store field survey median 15, only 9% at ≤10 min³. J.P. Morgan's channel table shows the two 10-minute operators did **not** batch¹¹. We are pricing a promise the market already breaks. Market is moving with us: 53% of riders now batch >20% of orders, up from 42%¹².
> `AND THE SENSITIVITY` The weighting depends on the demand profile. At a flatter 2× peak the weighted cost rises. Profile stated on-slide, measured by Round 1 metric 1 (PTDR) once live.

**So-what band**
> D2's cost stack is now fixed at ₹19.0/order. Apply it to the calendar. Slide 5.

**Footnote line** — `Sources 3,11,12,13,14 · SLA derivation A5 · access-regime matrix A4`

**Napkin prompt**
> One chart, two lines crossing, drawn as a simple hand-style plot. X axis "orders per hour" from 6 to 156. One descending curve labelled "cost per order ₹64.8 → ₹6.6" in navy. One flat-ish curve labelled "customer wait 25.7 → 27.1 min" in grey. A vertical gold band at the right labelled "exam-night peak" with a callout "cheapest and fastest here". Small annotation on the left: "batch = 1", on the right "batch = 12". Flat vector, no gradients or shadows, navy #0D1F5C, gold #FFC220, grey #5A6785, transparent background, wider than tall.

**Kill list** — no stopwatch icon, no "10 minutes" hero number, no rider photo.

---

## SLIDE 5 — D1 · THE DEAD ZONE PRICED  ·  **PIVOT SLIDE**

**Action title**
> 71.2% of the fixed base flexes, and flexing all of it still leaves the node needing 48.6% of term demand from a break that delivers none.

**Kicker**
> Fixed base ₹9,02,000/month¹, a Tier-1/2 store confirmed from the rent band in the same report. Robust across that band: ₹8.71L–₹9.18L, width 5.2%.

**MATH BOX — two identities that do all the work (4 cols)**
```
   CALENDAR SURCHARGE      σ = 12 / m = 12 / 8.5 = 1.412
   RESIDUAL THRESHOLD      r* = F_break / (30 · V · CM)
   at breakeven AOV, CM = F·σ / (30·V)   →   r* = 1/σ = 70.8%

   ASSET TURN              T = q · AOV · 365 · (m/12) / K
   RATIO                   T_campus / T_city = (q_c / q_city) · (m / 12)
                                             = (1,400 / 1,050) · (8.5 / 12)
                                             = 1.333 × 0.708 = 0.944

   F fixed ₹/month   V term volume orders/day   CM contribution ₹/order
   m active months   q orders/day   K capex ₹   AOV gross order value
```
Read-line: **0.708 is the same constant twice — the calendar surcharge inverted is the do-nothing threshold. Density (+33.3%) buys back the calendar (−29.2%) to within 5.6 points.**

**FIXED-BASE DECOMPOSITION (one stacked bar, full panel width)**
```
rent 24.1%  |  in-store staff 41.6%  |  utilities+cold 5.6%  |  other fixed 28.8%
            <------------- 71.2% can be flexed ------------->
```

**THE SOLVER — dead-zone minimisation (7 cols, monospace, verbatim from `solver.py`)**
```
minimise   dead-zone cash burn = break deficit + reactivation opex
subject to reactivation lead time >= 28 days
           SLA floor  (avg <= 27.1 min at peak)
           revocation survival >= 513 orders/day
           contract lock-in (no calendar-indexed retail lease exists in India) [17]
           7-week rule (below a 7-week segment, no lever can fire)
basis      residual demand r = 0%;  CM ₹30.3/order at campus AOV ₹580

STRATEGY           DEAD-ZONE   RESID DEM   REACTIVN   DAYS->SVC   BEST
                  ₹, 3.5 mo      % term          ₹        lead
------------------------------------------------------------------------
DO_NOTHING         3,157,000       70.8%          0          0
LABOUR_FLEX        2,159,500       59.1%    274,119         28
COLD_RIGHTSIZE     2,121,001       57.0%    274,119         28
SMALL_FORMAT       1,851,501       48.6%    274,119         28
REPURPOSE*                 0       48.6%          0          0    <<< BEST
------------------------------------------------------------------------
* REPURPOSE is not a cost configuration. It runs the SMALL_FORMAT cost base and fills
  48.6% from adjacent non-student catchment. Cost levers alone take the requirement from
  70.8% to 48.6% and CANNOT close it: residual campus population supplies only 8-15%.
  D1's largest problem is therefore solved by D2's site filter, not by an operating lever.
```
*(In orders/day: 992 → 827 → 798 → 681.)*

**SENSITIVITY — the throughput assumption, priced (5 cols)**

| campus orders/day | 1,000 | 1,200 | **1,400** | 1,482 |
|---|---|---|---|---|
| asset-turn ratio | 0.675 | 0.810 | **0.944** | **1.000 parity** |

```
Blinkit's observed nine-quarter range [2]      1,334 - 1,487 orders/day
ratio across that entire range                 0.90 - 1.00
parity throughput = q_city · σ = 1,050 · 1.412 = 1,482/day = 99.7% of the observed maximum
```
Read-line: **the ratio is linear in throughput, so we quote the range rather than defend a point. At 1,000/day it is 0.675 and the density argument weakens.**

**Limit strip**
> `ASSUMPTION EXPOSED` "Other fixed" of **₹2,59,660 (28.8% of the base)** is a residual we allocated out of JM's blended ₹100/sqft utilities-and-other line, not an itemised figure¹. It is the least defensible line in the stack and the one that persists through the break.
> `OUTSIDE EVIDENCE` Physicswallah's pre-Ind-AS EBITDA margin swings ~850bps Q4FY26→Q1FY27E on the academic calendar (with NEET postponement delaying offline batches)¹¹. Kambli 2020: worker reallocation alone cuts campus-dining wait 29% at $200 capex and $0/yr — labour beats capital, in a campus context¹⁸. CRISIL: occupier contracts run 1–3 years, terminable by the occupier on short notice — the flexibility is on our side of the table¹⁷.

**So-what band**
> Cost cannot close the calendar. Density can. So the break becomes a site-selection criterion. Slide 6.

**Footnote line** — `Sources 1,2,11,17,18 · solver A4 · fixed-base derivation A5 · basis proof A6`

**Napkin prompt**
> A descending step chart of four bars: 70.8%, 59.1%, 57.0%, 48.6%, labelled "do nothing", "labour flex", "+ cold right-size", "+ small-format". Draw a horizontal dashed red line at the last bar's height running across the whole chart, and shade everything BELOW that line in pale red, labelled "no lever reaches this — a break delivers none of it". Y axis "residual demand required, % of term volume", starting at zero. Flat vector, navy #0D1F5C for the first bar, grey for the middle two, gold #FFC220 for the last, red #C0392B dashed line, transparent background, no gradients or shadows, wider than tall.

**Kill list** — no ₹ waterfall of the contribution stack (that is A6), no cost-cutting imagery, no clock.

---

## SLIDE 6 — THE ANSWER · SITE SELECTION

**Action title**
> Choose the site: 569 orders/day of uncontested adjacent demand, 111 districts of 760 — and then we disqualified 72% of our own list.

**Kicker**
> The filter binds on access revocation (513/day), not on break-period solvency (471/day), so it is set at the higher of the two. A node that survives losing the campus survives the break by construction.

**MATH BOX — the filter (4 cols)**
```
   D_adjacent  >=  max( D_solvency , D_revocation ) / (1 - κ)

   D_solvency   = r* · V - D_residual        471 - 569 orders/day
   D_revocation = F_month / (30 · CM)        513 orders/day
   κ            = contested share of the adjacent catchment

   κ = 0%   ->   569/day      κ = 25%  ->    758/day
   κ = 10%  ->   632/day      κ = 44%  ->  1,015/day   (metro five-operator overlap [5])

   THE 7-WEEK RULE, derived not assumed:
   L_winddown + L_rampup  =  21d + 28d  =  49d  =  7 weeks
   a break segment shorter than this cannot be wound down at all.
```

**THE SCREEN (chart `district_screen`, 6 cols)**
```
760 districts [6]  ->  111 clear the screen
   not a metro · >=6 urban colleges · urban share >=50% · one break segment >=7 weeks
then screened for incumbent presence:   uncontested 9  |  contested 22  |  stacked 80
```

**RANKED CANDIDATES (6 cols)** — urban colleges × state residential intensity × hostel occupancy

| District | State | Urban colleges | Resid idx | Exp. incumbent |
|---|---|---|---|---|
| Khordha | Odisha | 169 | 20.1 | 23 stores |
| Kalaburagi | Karnataka | 229 | 11.2 | 31 |
| Belagavi | Karnataka | 190 | 11.2 | 26 |
| Visakhapatnam | Andhra Pradesh | 133 | 15.0 | 18 |
| Dharwad | Karnataka | 160 | 11.2 | 22 |
| Dakshina Kannada | Karnataka | 158 | 11.2 | 21 |

> `CONVERGENCE` Karnataka and Odisha were selected at **state** level off residential intensity and hostel occupancy. The district register — a different table, pulled later — puts **14 of the top 20 in Karnataka** and Khordha first. The state was not chosen and then justified.

**Limit strip**
> `WHAT THE FLAG CANNOT DO` Expected incumbent stores = urban colleges × non-metro store density, so "uncontested" is arithmetically "6–7 urban colleges": **the 9 clean districts are the 9 smallest**, sitting on the screen's own floor. The flag ranks; it does not site. Contestedness and cluster density trade off directly — there is no large empty district, and the plan does not need one: **campus demand inside the gate is uncontested by construction**, and what this screen prices is the adjacent half.
> `AND` The register carries no enrolment⁶, so district student counts are imputed off state ratios⁷ and labelled as such.

**So-what band**
> Site chosen, break survivable, revocation hedged. Can the basket clear ₹580? Slide 7.

**Footnote line** — `Sources 5,6,7 · full 111-district screen A7 · fragmentation A7b`

**Napkin prompt**
> A funnel in two stages, left to right. Stage one: a large box "760 districts" narrowing by arrow into a smaller gold box "111 candidates", with four small square bullets listed beside the arrow: "not a metro", "≥6 urban colleges", "urban share ≥50%", "one break segment ≥7 weeks". Stage two, below: a single horizontal bar split into three proportional segments labelled 9 / 22 / 80, coloured green, gold, red, with a legend beneath reading "uncontested / contested / stacked". Flat vector, navy #0D1F5C, gold #FFC220, green #1E7A46, red #C0392B, grey labels, transparent background, no gradients or shadows.

**Kill list** — no India map with pins (we cannot geocode; the map would overclaim), no state-level heat map.

---

## SLIDE 7 — THE BASKET AND THE BREAK PLAYBOOK

**Action title**
> ₹580 is modeled at 24.9% non-grocery, within Swiggy's disclosed reference range — and holding the node through the break costs 24% of relocating it.

**Kicker**
> No assumed lifting rate. The one disclosed quarterly series where an Indian operator actually lifted AOV, fitted and applied.

**MATH BOX — the basket, fitted not assumed (4 cols)**
```
   AOV = 11.28 · x + 391          x = non-grocery share of GOV, %
   R² = 0.918, n = 4 quarters, Swiggy Instamart Q1FY25 - Q2FY26 [10]

   every 1 pp of non-grocery share is worth ₹11.28 of AOV

   LADDER      ₹450  network basket today [4]
            +  ₹75   term-start durables: ₹1,000+ baskets over 14% of active weeks
            =  ₹525
            +  ₹55   non-grocery mix 20% -> 24.9% of GOV
            =  ₹580  required
   mix lever alone would need 31.5%. Occasions do the rest.
   Swiggy disclosed range 30-40% [10]  ->  headroom +15.1 pp
   Cross-operator reference only; not a Flipkart commitment.
```
Second lever: Minutes' free-delivery threshold is **₹149**, the market's lowest (Instamart ₹199, Blinkit ₹499 — and Blinkit already varies it by location and demand). A campus threshold is an existing platform lever, not a new ask.

**WHAT THE NON-GROCERY IS (5 cols)**

| Category | Why it lands on a campus |
|---|---|
| Term-start durables | coolers, blankets, buckets, storage — ₹1,000+, 2–3 week window per term |
| Electronics accessories | chargers, cables, power banks — already ~20% of Minutes' sales |
| Stationery & print | Zepto shipped Express Prints ₹2/page at ~285 stores²¹ |
| Beauty & personal care | ₹550–600 AOV vs ₹400–500 grocery, genuinely high-frequency |
| OTC medicine | ₹900–1,000 AOV; hostel population, no on-site pharmacy at most campuses |

Demand-side evidence²²: 40% of Gen Z order delivery weekly · 42% snack while streaming · 22% say *"I do not cook very well"* · 20% replace meals with snacks (Gen Z 23%).

**THE PLAYBOOK — three phases, dates not volumes (7 cols)**

| Trigger | Action | Owner |
|---|---|---|
| T−21d | freeze replenishment, begin inventory drawdown | Store manager |
| T−14d | notice to flex crew, confirm skeleton 6 | Cluster ops lead |
| T−7d | consolidate chilled to one zone, frozen down | Store manager |
| T−0 | licence-fee suspension takes effect | Contracts |
| weekly | check residual against the 87/day runner floor | Cluster ops lead |
| T−28d to term | open rehire, 4-week lead on 19 associates | Cluster ops lead |
| T−14d | rider re-acquisition incentives live in zone | Fleet |
| T−7d | cold-chain pull-down, FSSAI re-verification | Store manager |
| T−5d | first fill from SDFC, working-capital re-injection | Supply chain |

Ramp-up cannot be gradual: semester-start demand **steps**. Every action fires on a published calendar date, never on observed volume.

**WORKING CAPITAL — the sign is the finding (5 cols)**
```
   CCC = DIO + DSO - DPO = 13 + 0 - 60 = -47 days       [9, audited]
   WC  = NWC_days × NOV/day = ₹90.0 lakh at 14 days      [8]  (₹77.1 L at the 12-day target)

   STATE A  credit intact at restart      reactivation WC ≈ ₹0    stock rebuilds on payables
   STATE B  credit resets after dormancy  ₹45 L at 30 days, ₹90 L for the full cycle
   MITIGATION IS CONTRACTUAL: dormancy clauses in supplier terms, signed alongside the
   campus licence, before the first break.
```

**RELOCATION — the objection, answered (box)**
```
hold through the break  ₹21.3 L     do nothing  ₹31.6 L
relocate once           ₹89 L       relocate and return  ₹178 L      holding = 24% of one relocation
```
Urban demand is spatially mobile and temporally continuous — relocation is right there. Campus demand is spatially fixed and temporally discontinuous; relocation moves away from a catchment returning on a published date.

**THE MECHANISM ONLY FLIPKART HAS**
> Apr–Jun is a quick-commerce **up** quarter (Blinkit NOV +19.1% QoQ, "led by seasonality")⁸ and the campus empties in exactly those months, so labour, cold capacity and fleet free up while the surrounding network peaks. Flipkart already runs **650 festive-only delivery hubs and 2.2 lakh seasonal jobs** across Tier II/III²⁰ — this is that capability in a new phase, not a new capability. **Asymmetry stated: the Dec–Jan break sits in the network's trough, so the redeploy works for one break and not the other.**

**Footnote line** — `Sources 4,8,9,10,20,21,22 · basket fit A6 · playbook A4 · WC derivation A5`

**Napkin prompt**
> A waterfall of three ascending bars left to right: ₹450 labelled "network basket today", a small connector bar "+₹75 term-start durables", reaching ₹525, then a second connector "+₹55 non-grocery mix to 24.9%", reaching a final gold bar ₹580 labelled "breakeven". Above the final bar draw a light horizontal band spanning 30–40% labelled "Swiggy disclosed range — headroom 15.1 pp". Flat vector, navy #0D1F5C bars, gold #FFC220 final bar, grey connectors, transparent background, no gradients or shadows, wider than tall.

**Kill list** — no shopping-basket icon, no student persona, no "habit loop" diagram.

---

## SLIDE 8 — TRADE-OFFS AND WHERE THIS BREAKS

**Action title**
> Four things can break this node. Three are priced; all four fall within the AOV band implied by Swiggy's disclosed range, and one binds alone.

**Kicker**
> Shocks are quoted against the adopted ₹580 breakeven. The volume shock is the single binding dependency; the other three are absorbed.

**PRICED SHOCKS (7 cols) — tornado chart, widest bar at top**

| Shock | breakeven AOV | Δ | basis |
|---|---|---|---|
| **Volume −30%** | **₹647** | **+67** | 1,400 → 980 orders/day |
| Shrinkage charged on top | ₹623 | +43 | 1.8% of NOV⁸ — **upper bound, see limit** |
| Gig social-security levy | ₹595 | +15 | ₹88,200/mo at the 5%-of-worker-payments cap¹⁹ |
| Calendar fragmentation | ₹589 | +9 | +29% dead-zone cost, amortised |

```
CAN THE BASKET STILL COVER IT?
   AOV reachable at 30% non-grocery   ₹637      3 of 4 shocks covered inside the conservative floor
   AOV reachable at 40% non-grocery   ₹750      4 of 4 covered within Swiggy's range
   The volume shock needs the basket to work harder than the 30% case. One binding dependency, not four.
```

**CALENDAR FRAGMENTATION — priced, and it is on-thesis (5 cols)**

| Calendar shape | wind-downable | dead-zone cost | vs base |
|---|---|---|---|
| Contiguous 15.2w — what every D1 figure assumes | 100% | ₹21.3 L | — |
| **Typical: 8w + 4w + 3.2w** | **53%** | **₹27.5 L** | **+29%** |
| Semester: 11w + 4.2w | 72% | ₹24.9 L | +17% |
| All short gaps: 6+4+3+2.2w | **0%** | ₹31.6 L | **+49%** |

Fix is not a cheaper lever; it is the same site-selection answer arriving from a third direction — require one break segment ≥7 weeks (slide 6).

**LIMITS, IN OUR WORDS (5 cols)**
```
SHRINKAGE IS AN UPPER BOUND, NOT A BASE CASE
   shrinkage at the calibration point ₹9.88/order vs our unallocated residual ₹12.31/order
   the stack was calibrated by reproducing a REPORTED contribution figure, which is already
   net of shrinkage -> charging it again double-counts. ₹623 prices an IDENTIFICATION risk
   on the unallocated line, which is a smaller and different claim than "we forgot shrinkage".

TWO INPUTS REMAIN UNSOURCED BY DESIGN and are SOLVED across a range, not assumed:
   residual campus demand 8-15%   ·   doorstep/in-cluster dwell 2.0 min
   Five assumptions remain in total, three of them ranges. Down from twelve. (A3)

COUPLING THE AUDIT SURFACED
   the cost levers, by lowering the break-period requirement, WEAKENED the revocation hedge.
   Improving one number degraded another. That is why the filter is set on revocation.

UNALLOCATED LIABILITY
   no Indian consumer-forum ruling exists on gate-handoff custody. That gap is the argument
   for a logged, OTP-released chain of custody in the licence, not a risk we can price.
```

**CONCESSIONS, MADE FROM THE FRONT FOOT (strip)**
> **11 minutes is marketing**¹³ (slide 4) · **the industry relocates rather than mothballs** — and we never proposed mothballing (slide 7) · **we are not first**²⁰˒²¹ (slide 1).

**So-what band**
> One binding dependency: term volume. Instrument it in the pilot's first 90 days, on the four Round 1 metrics, and the go/no-go is a measurement, not a judgement.

**Footnote line** — `Sources 8,13,19,20,21 · shock derivations A5 · assumption ledger A3 · fragmentation A7b`

**Napkin prompt**
> A horizontal tornado chart. Four bars extending rightward from a common baseline labelled "₹580 breakeven", ordered longest to shortest: "volume −30% → ₹647", "shrinkage → ₹623", "gig levy → ₹595", "calendar fragmentation → ₹589". Draw two vertical dashed reference lines further right, one labelled "₹637 reachable at 30% non-grocery", one labelled "₹750 at 40%". Colour the longest bar red #C0392B and the rest grey; the two dashed lines gold #FFC220. Flat vector, transparent background, no gradients or shadows, wider than tall.

**Kill list** — no 2×2 risk matrix with vague labels, no "mitigation" column of platitudes, no traffic lights.

---

# PART 2 — THE APPENDIX (uncapped, and it is a weapon)

Last year's winner shipped a coordinate table that was one row repeated ~30 times, with points 100 km
outside Pune, and nobody caught it. **A clean appendix is cheap differentiation.**

| Page | Contents | Generator |
|---|---|---|
| **A1 Audit** | `audit.py` output, 291/291 assertions, every on-slide number tied to the model. Plus `verify_deck.py` 61/61 — the built file re-parsed and checked against the model. | `audit.py`, `verify_deck.py` |
| **A2 Source register** | The 22-source table above, expanded: every input with tier `[T1/T2/D/A]`, value, exhibit, date. Auto-generated. | `appendix.py` |
| **A3 Assumption ledger** | The five remaining assumptions, three as ranges, each with the span it is solved across. E-cart capex reductio (₹8 L before it moves ₹1/order). | `robustness.py` |
| **A4 Solver** | Full five-strategy comparison, all four constraints, parameter provenance block. Plus the playbook trigger table and the SLA × access-regime matrix. | `solver.py`, `sla.py` |
| **A5 Derivations** | Fixed base from Exhibits 12/13, tier identification from Exhibit 5, band sensitivity; trip identity; volume weighting; working capital three constructs. | `cost_stack.py`, `working_capital.py` |
| **A6 Basis proof** | Why the model is gross throughout: contribution ₹29.4 = Blinkit's reported ₹29.4, exactly. A mixed basis cannot land on a reported figure. Basket fit, four quarters, R²=0.918. | `campus_model.py`, `basket.py` |
| **A7 District register** | All 111 districts, the screen, the ranking, the contestedness bands. | `aishe_district.py` |
| **A7b Fragmentation** | Four calendar shapes priced; the 7-week rule derived from 21d + 28d. | `calendar_fragmentation.py` |
| **A8 Examined and rejected** | CRISIL per-tonne rates imply **41 tonnes inside a 3,100 sqft store** — bulk agri storage, not an in-store chiller. UBS's 2.7 orders/hr is food delivery, not quick commerce. Netscribes restated its own market size 59% in ten months. Round 1's 12.6× asset turn (mixed basis). Starship UK as a campus analogue (town-based, dropped). | S18/S19 |
| **A9 Literature screen** | 47 Scopus records screened, 3 usable. Kambli 2020 headline results and why the other 44 failed the screen. | sweep |
| **A10 Searched and not found** | kWh/day for a dark-store chiller · lease lock-in and notice terms · any operator-disclosed batching multiple · doorstep dwell · any vacation demand index · Minutes' own take rate · any Starship/Avride contract text with a seasonal-abatement clause. | sweep |

**A8 and A10 are the two the panel will remember.** Visible rejection is evidence of examination, and
almost no team produces either.

---

# PART 3 — WHAT WOULD MAKE THIS DEEPER STILL

Ranked by what it adds per hour of work.

1. **The formula boxes are the single biggest upgrade in this spec.** Four identities carry the whole
   argument: σ = 12/m, r* = 1/σ, T-ratio = (q/q)·(m/12), b(λ) = min(K, λW/60). Each is one line, each
   is checkable in the panel's head, and none of them is a framework. Put them in monospace and define
   every symbol underneath — that is what makes a deck read as engineering.
2. **The solver on a content slide** (slide 5) with sourced inputs, against a field that will bring
   frameworks. Last year's winner ran an SMILP over **simulated demand and a flat ₹700 AOV with no
   source.** We run a smaller optimisation over 291 audited assertions. Say the word "audited" once.
3. **Units discipline.** Gig ₹/**active** hour against runner ₹/**rostered** hour is the finding on
   slide 3 — the two are not the same unit, and naming that is what separates an ops answer from a
   cost table.
4. **Solved-vs-assumed, marked per variable.** The runner threshold (87/day), the residual threshold,
   the parity throughput and the site filter are all *solved*. Last year's threshold column was
   *chosen*. Same column, opposite epistemic status. Mark it: `[solved]` / `[assumed, range]`.
5. **Little's Law on the gate queue** (slide 4) — L = λW makes the batching argument a queueing result
   rather than an operational preference, and it costs one line.
6. **The cash conversion cycle** (slide 7). CCC = 13 − 60 = −47 days turns "working capital" from a
   number into a sign, and the sign changes the recommendation from financial to contractual.
7. **DuPont framing on the asset turn**, if you want one more layer: T = NOV/K is the turnover leg of
   ROCE, and Eternal has publicly targeted ROCE "north of 40%"⁸. Saying *the campus node clears the
   turnover leg at 94% of a city store* connects the asset-turn result to Eternal's public benchmark.
8. **Concepts to name explicitly** where they already apply, so the vocabulary is visible:
   *cost-to-serve decomposition* (slide 3), *risk pooling / consolidation* (slide 4), *capacity cushion*
   (slide 4 runners), *postponement* (scheduled-slot tier), *fixed-cost absorption and operating
   leverage* (slide 5), *network densification and cannibalisation* (slides 2, 6), *seasonality index*
   (slide 8), *cash conversion cycle* (slide 7), *service-level vs cost frontier* (slide 4 tiers).
9. **What we deliberately do NOT claim, and should say once:** no geocoded siting (the district flag
   ranks, it does not site), no demand forecast (we solve for the demand a site must have), no
   simulation (every input is a disclosure or a derivation from one). Each of those is a place where a
   competing team will overclaim, and a panel that has read three decks will notice.

---

# PART 4 — PRE-FLIGHT

- [ ] Every headline is a full-sentence finding with a number, not a topic label
- [ ] Every number traced: `python3 Model/audit.py` (291/291), `python3 Model/verify_deck.py <deck.pptx>`
- [ ] Exactly 8 content slides; cover and appendix excluded
- [ ] **Team name and ID on page one; college and member names OFF** (the rule changed this year)
- [ ] Superscript numerals only — no "Source:" prose on any content slide
- [ ] Three concessions present and used, not merely admitted
- [ ] The −30% volume shock stated, not softened
- [ ] No Round 1 figures anywhere: ₹528, ₹775, 12.6×, ₹95.7 L, ₹554
- [ ] No panel with fewer than three lines of content; no chart under 3 columns wide
