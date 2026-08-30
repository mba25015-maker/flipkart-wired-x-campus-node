# HANDOFF — Flipkart WiRED X Semi-Final
*Rewritten 2026-08-28 after sessions S17-S22. Supersedes the 2026-08-26 version entirely.*
*Every figure below is asserted in `Model/audit.py`; the release command passes **344/344**, **31/31**, **79/79**, and **133/133**.*

---

## BUILDING THE DECK? START HERE
**Abhishek builds it in PowerPoint with the Claude extension.** Paste from
**`PPT_BUILD_PROMPT_SemiFinal.md`** — Part A once (design system), then Part B one slide at a time.
**`DECK_ASSET_PLAN_SemiFinal.md`** carries the appendix architecture, the five Colab links and where
each one sits, and the six screenshots to capture. Three hours of prep, in the order given there.
**`DECK_ARCHITECTURE_SemiFinal.md` first** — it carries the S31 slide ORDER and supersedes the order
in `DECK_SPEC_SemiFinal.md` (the spec's content blocks all survive; four are re-homed).
**`Flipkart_Minutes_WiRED_SemiFinal_REFERENCE_light.pptx`** is the built reference for all 8 slides,
from `Model/build_deck.py [light|dark]`. Renders in `Model/_render/`.
**`DECK_SPEC_SemiFinal.md`** is the build reference for all eight slides and the appendix — copy,
tables, math boxes, footnote scheme, napkin prompts, kill lists. **`Napkin_Prompts_SemiFinal.md`** is
the visual pack. Verify anything you type: `python3 Model/verify_spec.py` (66/66) checks the spec,
`python3 Model/run_all.py` checks the model, documents, specification, and exact final deck.

## READ THESE, IN THIS ORDER
1. **`Flipkart_WiRED_X_ProjectPrompt_SemiFinal.md`** — the standing system prompt
2. **This file** — current state, current numbers
3. **`BUILD_PLAN.md`** — the live work list and the Claude Code split
4. **`Decisions_Log.md` S17-S24** — the six sessions that rebuilt the model. S1-S16 are the earlier
   semi-final record; sections 1-14 are Round 1 and still load-bearing
5. **`CORPUS_SWEEP_2026-08-27.md`** — the complete parse of `Research Pulls` (218 files, read in full)
6. **`DECK_TEARDOWN_WiRED9.md`** — last year's winning deck, and what we take from it

**Round 1 artifacts, kept for continuity, NOT current:** `Presentation_Flow.md`,
`Visual_Prompt_Pack.md`, `RUBRIC_CHECK.md`, `DECK_PLAN_v5.md`, `Napkin_Prompts.md`.
They carry Round 1's 3-content-slide structure and Round 1's numbers. **Do not read a figure off
them.** `PRIORITY_PLAN.md` is superseded by `BUILD_PLAN.md`.

## THE ONE-LINE STATE
**The final deck is built. The supported release check is `python3 Model/run_all.py`: 344/344 model
checks, 31/31 HANDOFF ties, 79/79 specification ties, and 133/133 checks on the exact final deck.
The deck verifier reopens the PowerPoint, checks text and native-chart values, and rejects
superseded figures and banned claim language.**

---

## HOW TO RUN THE MODEL
```
python3 Model/run_all.py              # one supported entrypoint; nonzero exit on any failure
python3 cost_stack.py                 # fixed + last-mile decomposition; tier_report(), s19_report(),
                                      #   crisil_tcw_report()
python3 campus_model.py               # breakeven, basis declaration, asset_turn_report()
python3 basket.py                     # the basket ladder to Rs573          [NEW, S21]
python3 aishe_district.py             # district register, urban screen      [NEW, S24]
python3 solver.py                     # 5-strategy comparison, BEST=REPURPOSE [CC-1]
python3 verify_docs.py                # HANDOFF figures vs the model         [NEW, S23]
python3 working_capital.py            # WC rebuilt, the credit-terms finding [NEW, S22]
python3 fleet_mix.py                  # fleet comparison, labour class, utilisation
python3 sla.py                        # SLA tiers, dynamic batching, volume-weighted cost
python3 break_mode.py                 # break-period P&L, lever ladder, relocation_report()
python3 rent_lever.py · risk_quadrant.py · robustness.py · jm_survey.py · tariff.py · gap_check.py
python3 charts4.py                    # lever_ladder_s5, district_screen        [NEW, S27]
python3 charts5.py                    # universe_narrow, metro_squeeze          [NEW, S28]
python3 build_semifinal.py light|dark # the semi-final deck: slides 1, 2, 5, 6  [S27, S28]
python3 verify_deck.py [deck.pptx]    # the BUILT slides vs the model, 133/133
python3 verify_spec.py                # SPEC + BUILD PROMPT vs the model, 79/79 [S29,S32]
python3 roce.py                       # ROCE, DuPont, payback, IRR, scenarios   [NEW, S30]
python3 charts6.py                    # roce_ladder, pnl_bridge                 [NEW, S31]
python3 build_deck.py light|dark      # THE REFERENCE DECK, all 8 slides        [NEW, S31]
```
**RULE: never type a figure onto a slide. Change the model, rebuild, run `audit.py`.** It has caught
a real error four times, most recently catching *me* reading an artefact of my own patch as a
discovery (S19 -> S20), and catching an arithmetic error I had propagated into three documents (S22).

---

## THE CURRENT NUMBERS — nothing else is current

### The fixed base
**Rs9,02,000/month**, JM Financial Exhibit 13. **71.2% is not truly fixed.**
**Exhibit 13 is a TIER-1/2 store, not a Tier-3+ store** — settled at S17 from Exhibit 5 of the same
report: rent Rs70/sqft sits inside the Tier-1/2 band (Rs60-75) and outside Tier-3+ (Rs35-50); picker
salary Rs15,000 sits in both bands and therefore does not discriminate.
Sensitivity across the full Tier-1/2 rent band: **Rs8,71,000 (Rs60/sqft) - Rs9,17,500 (Rs75/sqft),
band width 5.2%. Robust.** A Tier-3+ store would be Rs7,65,750 (-15.1%) — sensitivity case only.
**SAY ON SLIDE:** JM holds "utilities + other" at Rs100/sqft in BOTH tiers, so it is a blended
allocation. Our split into utilities (**Rs50,340**, sourced via `tariff.py`) and **"other fixed" (Rs2,59,660, 29% of
the base) is OURS and is a residual — the least-defensible line in the stack.**

### Breakeven AOV — three figures, all live, each with its own basis
| Figure | Basis | Status |
|---|---|---|
| **Rs573** | JM fixed base, last mile taken from D2's own circuit model (Rs17.6/order) | **ADOPTED. D1 and D2 tie out here.** |
| Rs554 | JM fixed base, Rs42/3.0x consolidation proxy | S7 base case, **superseded** |
| Rs528 | legacy Rs7.5L base, 3.0x proxy | **Round 1 headline**, retained for continuity |
**All three are GROSS order values.** Basis proved at S18, not asserted: model contribution per order
= **Rs29.4** = Blinkit's **reported** contribution profit. A mixed basis cannot land exactly on a
reported figure. **Footnote once:** Rs528 is arithmetically identical to Blinkit's FY25 NAOV of
Rs528. Coincidence — ours is a cost stack over a take rate.

### Minutes
**AOV Rs450** (TechCrunch, journalist-confirmed Flipkart-internal data). **Rs775 (Inc42) is
superseded and appears only as `MINUTES_AOV_R1`.** ~1,100 orders/store/day.
**Store count: crossed 1,000 in Jul 2026** (Bernstein via ET, +262 in the Apr-Jul quarter). Walmart's
own CEO said **">800 MFCs, <13 minutes, >30 cities"** on 21 May 2026. Run rate ~100/month.
**Concede the 11-minute figure.** Walmart says <13; Euromonitor 15-20; our own JM 35-store survey
median 15, only 9% at <=10 min.

### Return on capital — S30. THE HURDLE, NOT THE BREAKEVEN
**Capital employed Rs323.9 lakh** = capex Rs235.0 L + NWC Rs88.9 L. **AOV for ROCE = 0 is Rs571**
(ties to the Rs573 spine within Rs2.14 — a 365-day vs 12x30-day count, asserted). **AOV for the 40%
hurdle is Rs755**, a **Rs184 premium**, implying **32.3% non-grocery** against a disclosed 30-40% range.
**ROCE 34.4% at a 30% basket (payback 25 mo), 58.8% at 40% (15 mo). IRR 34.4%.**
**THE LIMIT: at a 30% basket with volume -30%, ROCE is 14.0% and payback is 62 months — longer than
the node's 60-month anchored life.** That is why the day-90 gate measures volume first.
**ROCE = margin x turnover, so the 0.944 moneyshot IS the turnover leg of the external benchmark's metric.**
**TWO ASSET TURNS, BOTH CORRECT — ALWAYS QUOTE THE BASIS:** 6.93x is like-for-like at a COMMON AOV
Rs450 (isolates density x calendar); 8.44x is the node's own turnover at its benchmark-implied AOV on capital
employed. **Repurpose is worth Rs26 of AOV** — the site filter and the basket lever are substitutes.

### Asset turn — restated on one basis at S18, ceiling sensitivity added at S27
**City 7.34x · campus 6.93x · ratio 0.944.**
**THE CEILING IS NO LONGER AN ASSUMPTION [S27].** The ratio is linear in throughput, so quote the
range, not the point: **across Blinkit's observed nine-quarter range 1,334–1,487 orders/day the
campus node runs 0.90–1.00.** **Parity at 1,482/day = 99.7% of the observed maximum**, and parity is
an identity — city OPD x the calendar surcharge (1,050 x 1.412). **At 1,000/day the ratio is 0.675**,
and that floor is on slide 5 in our own words. `campus_model.turn_ratio_at()`, `PARITY_OPD`,
`TURN_SENSITIVITY`.
Identity: **(1,400/1,050) x (8.5/12) = 1.333 x 0.708 = 0.944.**
**Campus density (+33.3%) almost exactly buys back the calendar (-29.2%). The dead zone costs 5.6
points of asset productivity, not 30.** And 0.708 is the do-nothing residual threshold, a third time.
Round 1's 12.6x / Rs29.7 cr survive only as `CITY_TURN_R1` / `CITY_NOV_R1` — they compared a campus
node at its breakeven AOV against a city store at its actual AOV. Mixed basis.

### D1 — the dead zone. INVARIANT to the Rs554 -> Rs573 restatement.
Break-period solvency runway at zero residual **1.00x** · do-nothing residual threshold **70.8% =
1/1.412** · ladder **labour flex 59.1% -> cold right-size 56.9% -> small-format node 48.5%** ·
adjacent catchment required **469-567/day** · binding site filter **567/day**.
**Every one of these is a ratio driven by the calendar surcharge, not by the level of AOV.** That
invariance is a robustness result and belongs on a slide.
**The 1.00x is an IDENTITY of the solve-for method** — setting achieved AOV = breakeven forces annual
contribution to zero, so term surplus must exactly offset break deficit. Say that; do not present it
as a lucky coincidence.

### D1 — reactivation
Opex **Rs2,62,119** (at 15% residual) · ramp-up lead time **28 days** · **below a 7-week break, do not wind down at all**.
**Working capital Rs88.9 lakh** (NWC days x daily NOV at Eternal's current **14 days**; Rs76.2 lakh at
their 12-day target). **The Rs95.7 lakh figure is superseded; Rs96 lakh never existed as a computed
number.** **NWC_DAYS = 18 was stale.**
**THE FINDING IS THE SIGN.** Zepto's audited MCA-filed balance sheet: **13 days inventory vs ~60 days
payables, cash conversion cycle -47 days.** The node is supplier-funded.
**State A, credit intact: reactivation WC ~ Rs0** — the rebuild is payables-funded and the cash cost
sits at wind-down. **State B, credit resets after 3.5 months dormant: Rs44.4 lakh at 30 days to
re-establish terms, Rs88.9 lakh for the full cycle.**
**It is a CREDIT-TERMS risk, not an inventory-value risk. The mitigation is contractual: negotiate
dormancy clauses into supplier terms alongside the campus licence, before the first break.**
**Shrinkage 1.8% of NOV, "largely perishables" = Rs3.43 lakh/month** — first perishable-loss rate we
have, and it prices the DOWNSIDE of the cold right-size lever.

### D1 — the relocation objection, answered at S21
**We do not propose mothballing.** Every configuration keeps the node open; S1's break-mode default
is **repurpose the catchment**, which is why the filter requires adjacent non-student demand.
Urban q-commerce demand is **spatially mobile, temporally continuous** — relocation is the right
answer and the industry has correctly converged on it. Campus demand is **spatially fixed, temporally
discontinuous** — relocation moves away from a catchment that is coming back.
**Hold through the break Rs21.3 lakh · relocate once Rs89 lakh · relocate and return Rs178 lakh.
Holding costs 24% of one relocation.**
Precedent: campus foodservice is the industry that HAS this calendar, and its cross-operator playbook
is close most units / skeleton crew / cut hours — our lever ladder in different words.

### D1 — can the basket reach Rs573? YES. `basket.py`, S21.
Method: no assumed lifting rate. Take the one disclosed quarterly series where an Indian operator
actually lifted AOV. **Instamart: AOV = 11.28 x (non-grocery % of GOV) + 391, R2 = 0.918.**
**Ladder: Rs450 -> Rs525 (term-start durables over 14% of active weeks) -> Rs573 at 24.3%
non-grocery**, from 20% today, against the **30-40% range disclosed by Swiggy. 15.1 pts headroom.**
Second lever: **Minutes' free-delivery threshold is Rs149, the market's lowest** (Instamart Rs199,
Blinkit Rs499 — and Blinkit already varies it **by location and demand**, so a campus threshold is an
existing platform lever, not a novel ask).


### Contestedness — CC-7, and what S27 found inside it
Filter restated as **569/day of UNCONTESTED demand**, rising to **1,015/day** on a catchment as
contested as a metro pin code (44% five-operator overlap). Quote the band, not a point.
**9 of our 111 candidate districts are uncontested — and they are the nine SMALLEST.** Expected
incumbent stores = urban colleges x non-metro density, so "uncontested" is exactly "6–7 urban
colleges", the screen's own floor. **The flag is monotone in district size and carries no independent
information; it ranks, it does not site.** Say it first: contestedness and cluster density trade off
directly, there is no large empty district to find, and **the plan does not need one — the campus
inside the gate is uncontested by construction.** On slide 6, red-ruled.

### The district layer — AISHE institution register, S24
`Model/aishe_district.py`. **54,014 colleges + 1,428 universities + 16,910 standalone = 72,352
institutions across 760 districts**, register as on 28-8-2026, each with district AND urban/rural flag.
**THE FINDING: urban colleges 21,000, rural 32,336. Urban share 39.4%. Six in ten Indian colleges are
rural, so the campus micro-market universe is 21,000 colleges, not 54,014.**
**Archetype now operational, not a label** — not a metro, >=6 urban colleges, urban share >=50%
**-> 111 candidate districts of 760.** That is the replicability number.
Top districts by urban colleges x state residential intensity x hostel occupancy:
**Khordha (Odisha) 169 · Kalaburagi 229 · Belagavi 190 · Visakhapatnam 133 · Dharwad 160 · Mysuru 156.**
**14 of the top 20 are in Karnataka** — the district data independently reproduces S17's state-level
selection from a different table.
Cohort proxy: **1,897 urban Technical/Polytechnic, PGDM, Pharmacy and Hotel Management standalones.**
**CAVEATS THAT TRAVEL WITH EVERY FIGURE:** the register carries **no enrolment** — district student
counts remain an imputation off state ratios. And it is the **live list at 28-8-2026 (54,014
colleges)** while the AISHE **2023-24 report** counts **48,246 at 31-12-2023**. Different instruments,
different dates; never mix a count from one with an enrolment from the other.
`College-Affiliated College.xlsx` is a byte-identical duplicate of `College-ALL COLLEGE.xlsx`.

### D2 — fulfilment, SLA, fleet
**Type A (bounded campus) vs Type B (urban PG cluster)** — the access-geometry axis extending Gate 0.
Type B is standard residential delivery and costs 36% LESS than a standard zone.
**Fleet is a LABOUR CLASS question.** Gig **Rs168/active hour** vs employed runner **Rs72/rostered
hour = 2.33x**. Cycle beats petrol 2W despite being 40% slower. On-foot loses to cycle at every batch.
**Sensitivity (S19):** on UBS's food-delivery productivity anchor the ratio is **1.60x**. **The
labour-class conclusion survives both anchors — state the range, the direction does not move.**
**UBS's 2.7 orders/active hour is FOOD DELIVERY and does not replace JPM's 4.0 for quick commerce.**
**Volume-weighted campus last mile Rs17.6/order against Rs42.0 for a standard zone.**
**SLA: abandon the uniform 10-15 minute promise.** Dynamic batching on a **6-minute wait cap or 12
orders**. Average 21.6 min, peak 27.1 min. **Batch wait FALLS as demand rises**, so the product is
fastest and cheapest at exam-night peak. Validated by JM's 35-store survey.
**Batching is bought with SLA** — JPM's 2022 table shows the two 10-minute operators did not batch.
That supports our design rather than threatening it.
**The institution runs the intra-campus leg for a per-parcel fee.** Ceiling Rs29.2, runner floor Rs9.6.
**Scope it as CONTINUOUS circuits, never as the campus parcel desk's accumulate-and-distribute model.**

### The opening, and it is sourced [S28]
**Starship Technologies quit ALL US higher education in June 2026** — eight years, 60+ campuses,
~1,200 robots withdrawn. Heinla, Food On Demand 10 Jun 2026: *"campus and grocery are fundamentally
different operations: one is seasonal and contract-driven, the other is a 365-day urban business."*
**It did not lose to robots-vs-humans — it lost 365-day utilisation to 8.5-month utilisation, our own
ratio.** And the campuses did not go dark: **Avride took them on a national foodservice master services
agreement with Chartwells (~350 campuses), university as permissioning party only.** So the segment did
not fail; **a contract shape did.** Slide 2, top strip.
**White space, sourced:** Euromonitor's Indian consumer-foodservice taxonomy has **no education/
institutional location** and no hostel/PG household type — students sit in "Other", never broken out.

### Advertising — there is NO missing revenue line
Blinkit's ad income is booked **entirely to revenue**, and the take rate is revenue/GOV. **Ads are
already inside the 19.41%**, proved by the same Rs29.4 contribution identity. **The earlier claim that
the ad line "may be worth more per store per month than the entire fixed base" is RETRACTED.**
The live risk is the inverse: a campus cohort may monetise ads **below** network rate.

---

## DECISIONS LOCKED — do not re-litigate (log section in brackets)
- D2 arithmetic runs before D1 costing [S1] — **and it now actually does: D1's last-mile line is
  taken from D2's circuit model, not a proxy** [S19/S20]
- Type A / Type B access-geometry axis, extending Gate 0, quadrants untouched [S1]
- Break-mode default: repurpose the catchment [S1] — **this is the answer to the relocation
  objection, not a defence of mothballing** [S21]
- Campus node = institution as paid last-mile operator [S3]
- Minutes AOV Rs400-500 adopted, provenance confirmed by the journalist [S4]
- **Site archetype = Tier-1/2 dense cluster**, selected on **demand resilience, not campus density**
  [S17]. Node underwritten by a **3-6 college cluster plus surrounding catchment.**
- Fixed base Rs9.02L, **confirmed as Tier-1/2 from JM Exhibit 5** [S17]
- **Model basis is GROSS order value throughout** [S18]
- Rent is the LEAST flexible line [S11] — **amended:** CRISIL says warehousing occupier contracts run
  **1-3 years, terminable by the client on short notice without compensation**, so the flexibility
  sits on our side of the table. No calendar-indexed *retail* lease exists in India.
- Footprint lever = format choice (2,000 sqft), NOT an SKU elasticity — falsified [S15]

## OPEN
**The build:** slides 3, 4, 7, 8 next, then the appendix. Run `verify_deck.py` on every export.
**Still-unplaced qualitative findings (FINAL_AUDIT §2):** **UC Davis** — institution as paid operator,
**$2/parcel, 12 packages per stop against 3 for a third-party truck (4x)**, 99.6% same-day — belongs on
**slide 3**, which currently asserts institution-as-operator with no precedent cited. **Flipkart's 650
festive-only hubs and 2.2 lakh seasonal jobs** and the **Gen Z occasion data** (VOC 2026, n=1,002)
belong on **slide 7**; the **counter-cyclical fleet asymmetry** on 7 or 8.
**Not blocking:** gig levy off the 5%-of-worker-payments cap · absolute breakeven OPD as a second
calibration anchor (CM 800-1,000; EBITDA 1,500-1,800; Zepto 2,000-3,000; non-metro 1,200-2,000) ·
contestedness screen on the site filter (569/day of **uncontested** demand) · labour-class parameter table · competitor table on the
campus axis · counter-cyclical fleet **with its asymmetry**.
**Abhishek's:** team name and ID on the cover · **re-read Eternal's FY26 balance-sheet inventory line** (the extraction gives both Rs281 cr and Rs2,181 cr).
**Claude Code, in parallel, no dependencies:** CC-1 solver · CC-2 regenerate all figures.

## THINGS THAT WILL BITE IF FORGOTTEN
- **Team name and ID are still placeholders on the Round 1 cover.** PDF must be re-exported.
  **Keep college and member names OFF** — last year's winners put names and photos on their cover
  and that rule changed this year.
- **Exactly 8 content slides** excluding cover and appendix. Appendix is uncapped and is a weapon.
- **3-month implementation cap.**
- The panel has our Round 1 appendix, which claims "no unsourced assumptions remain."
- **We are not first.** Swiggy runs a student rewards programme with **college canteens and hostels**,
  the **Toing** app (AOV <Rs200, ~50 cities), and a **Young India Skills University MoU** (Jan 2026).
  Blinkit runs **India's first in-airport q-commerce with Adani at CSMIA** (1 Apr 2026). Say it first.
- **Nobody in the industry mothballs a dark store — they relocate.** We answer that at S21; the answer
  must be in the deck, not improvised in Q&A.
- **Three times a primary observation was over-read into a stronger claim than it licensed**, and
  twice more since (S19 self-artefact, S22 arithmetic). Slow down on primary observations.
