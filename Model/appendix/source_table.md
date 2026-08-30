# Appendix — source table

Every tagged input in `Model/*.py`. Value column is the **live model value** read at generation time, not a transcription. 97 inputs.

| # | Parameter | Value | Tier | Source | Module |
|---:|---|---:|:--:|---|---|
| 1 | `NONGROCERY_CEILING` | 40 | T1 | Swiggy disclosed non-grocery range: 30-40% of GOV | `basket` |
| 2 | `RELOCATE_CAPEX` | 8,900,000 | T1 | JM Financial, Swiggy initiation 13 Nov 2024, Ex.87 - itemised cost to set up ONE dark store | `break_mode` |
| 3 | `ACTIVE_MONTHS` | 8.5 | T1 | institutional calendars | `campus_model` |
| 4 | `BLINKIT_AOV` | 694 | T1 | Blinkit AOV FY26E (same model) | `campus_model` |
| 5 | `BLINKIT_CP` | 29.4 | T1 | Blinkit contribution profit per order FY26E (same model) | `campus_model` |
| 6 | `BLINKIT_FREQ` | 3.6 | T1 | orders/month per transacting user (JM Financial; observed 3.2-4.1) | `campus_model` |
| 7 | `BLINKIT_NAOV_FY25` | 528 | T1 | for the footnote only; NOT an input to any calculation | `campus_model` |
| 8 | `CM_MATURE` | 0.02 | T1 | contribution margin, mature-market stores, % of GOV (analyst channel checks) | `campus_model` |
| 9 | `CM_TOPCOHORT` | 0.04 | T1 | contribution margin, top-cohort stores, % of GOV | `campus_model` |
| 10 | `FRANCHISE_PAYBACK` | 56 | T1 | months, illustrative franchised dark store (J.P. Morgan) | `campus_model` |
| 11 | `MINUTES_AOV` | 450 | T1 | TechCrunch 22 Aug 2026, Rs400-500, midpoint. Provenance confirmed in writing by the reporting journalist: Flipkart INTERNAL data, avg as recent as Aug 2026. Adopted at S4; this line makes the model... | `campus_model` |
| 12 | `ROCE_TARGET` | 0.4 | T1 | Eternal earnings call, Jan 2026 ("north of 40%") | `campus_model` |
| 13 | `TAKE_RATE` | 0.1941 | T1 | Blinkit revenue take rate FY26E (JM Financial, Eternal model, Jul 2025) | `campus_model` |
| 14 | `CAMPUS_KM` | 1.35 | T1 | IIM Jammu gate to boys' hostel, 1.2-1.5 km (primary, Abhishek) | `cost_stack` |
| 15 | `CAMPUS_KMPH` | 20 | T1 | observed intra-campus vehicle speed (primary, Abhishek) | `cost_stack` |
| 16 | `CAMPUS_LICENCE` | {6 entries} | T1 | Rs/sqft/month tender documents | `cost_stack` |
| 17 | `CITY_LEG_MIN` | 8 | T1 | Blinkit <2 km ride leg in ~8 min (founder, via Parl. panel reporting) | `cost_stack` |
| 18 | `JM_COLD_ROOM_CAPEX` | 1,440,000 | T1 | JM Financial, Swiggy initiation, 13 Nov 2024, Ex.87 | `cost_stack` |
| 19 | `JM_METRO_DELIV_SHIFT` | 30 | T1 | "up to 30 deliveries per day in a 12-hour shift" | `cost_stack` |
| 20 | `JM_METRO_EARN` | 37,500 | T1 | "monthly earnings ranged between INR 35k and INR 40k" | `cost_stack` |
| 21 | `JM_NONMETRO_DELIV_SHIFT` | 17.5 | T1 | "15-20 deliveries in a 12-hour shift" | `cost_stack` |
| 22 | `JM_NONMETRO_EARN` | 20,000 | T1 | "typically below INR 20k per month" | `cost_stack` |
| 23 | `JM_SHIFT_HRS` | 12 | T1 | — | `cost_stack` |
| 24 | `JPM_ORD_DAY` | 21 | T1 | "delivers 20-22 orders per day" | `cost_stack` |
| 25 | `JPM_ORD_HR` | 4 | T1 | "on an average does four orders in a hour and most do order batching" | `cost_stack` |
| 26 | `JPM_RADIUS_KM` | 5 | T1 | "dark stores cover a radius between 5-10kms" (Blinkit/Zepto 4-6) | `cost_stack` |
| 27 | `JPM_RIDER_FUEL` | 6,600 | T1 | "fuel expenses are Rs6.6K" | `cost_stack` |
| 28 | `JPM_RIDER_MONTH` | 26,500 | T1 | "average monthly income of a delivery executive was Rs26.5K" | `cost_stack` |
| 29 | `V1_STORE_SQFT` | 3,000 | T1 | Flipkart Minutes dark store, TechCrunch 22 Aug 2026 | `cost_stack` |
| 30 | `RUNNER_MO` | 15,000 | T1 | JM Financial non-metro dark-store staff salary | `fleet_mix` |
| 31 | `PICK` | 2.5 | T1 | Blinkit pick-and-pack, founder via Parliamentary panel reporting | `gap_check` |
| 32 | `KM_PER_LEG_SOURCE_FLOOR` | 2 | T1 | JPM wording, "<2 km ride leg" - used only for the band | `labour_class` |
| 33 | `NWC_DAYS_R1` | 18 | T1 | Jan 2026 call. Retained ONLY so working_capital.py can show the rejected construct beside the adopted one. No operating module may import this | `params` |
| 34 | `NWC_DAYS_TARGET` | 12 | T1 | same call, steady-state target | `params` |
| 35 | `CAMPUS_FORMAT_SQFT` | 2,000 | T1 | smallest quartile of the JM field survey | `rent_lever` |
| 36 | `SKU_BASE` | 16,500 | T1 | Minutes dark store carries 15,000-18,000 SKUs (TechCrunch) | `rent_lever` |
| 37 | `LEVY_MONTH` | 88,200 | T1 | Parl. Standing Cttee 201st report, 5% cap | `risk_shocks` |
| 38 | `ROCE_HURDLE` | 0.4 | T1 | Eternal earnings call Jan 2026, "north of 40%" | `roce` |
| 39 | `TAX_RATE` | 0.2517 | T1 | Indian statutory corporate rate, 22% + surcharge + cess | `roce` |
| 40 | `PTDR_PEAK` | 4 | T1 | Round 1 metric 1 flag threshold: peak-to-trough demand ratio > 4.0x | `sla` |
| 41 | `BLINKIT_STORES_FY25` | 1,301 | T1 | disclosed | `working_capital` |
| 42 | `ETERNAL_NWC_DAYS_NOW` | 14 | T1 | Eternal Q1FY27 call, 22 Jul 2026 | `working_capital` |
| 43 | `ETERNAL_NWC_DAYS_R1` | 18 | T1 | Jan 2026 call - REJECTED, shown for contrast | `working_capital` |
| 44 | `ETERNAL_NWC_DAYS_TARGET` | 12 | T1 | same call, steady-state target | `working_capital` |
| 45 | `NOV_OVER_GOV` | 0.791 | T1 | Blinkit FY26E NOV/GOV | `working_capital` |
| 46 | `NWC_PCT_NOV` | {2 entries} | T1 | Eternal's own conversion, both points given | `working_capital` |
| 47 | `SHRINKAGE_PCT_NOV` | 0.018 | T1 | Eternal 22 Jul 2026: "about 1.8% of NOV, largely perishables" | `working_capital` |
| 48 | `TARIFF` | 8.73 | T1/T2 | SOURCED, no longer assumed. Two independent routes agree: (a) BESCOM LT-3 commercial, Karnataka FY2025-26: Rs8.00 energy + FAC Rs0.31 + 5% electricity tax = Rs8.73/kWh effective [T2, BESCOM/KERC sc... | `cost_stack` |
| 49 | `METRO_OVERLAP_5OP` | 0.44 | T2 | share of metro pin codes served by all five, Jul 2026 | `aishe_district` |
| 50 | `METRO_OVERLAP_PRIOR` | 0.26 | T2 | the same measure one quarter earlier | `aishe_district` |
| 51 | `METRO_STORES` | 4,300 | T2 | stores held in the eight metros | `aishe_district` |
| 52 | `METRO_SUSTAINABLE` | 3,600 | T2 | Bernstein's estimate of sustainable metro capacity | `aishe_district` |
| 53 | `OPERATOR_STORES` | {5 entries} | T2 | same Bernstein/ET line, Jul 2026 | `aishe_district` |
| 54 | `PIN_CODES_ADDED_Q` | 152 | T2 | Apr-Jul 2026 | `aishe_district` |
| 55 | `PIN_CODES_SERVED` | 2,722 | T2 | unique pin codes served by the five largest operators | `aishe_district` |
| 56 | `STORES_ADDED_Q` | 900 | T2 | Apr-Jul 2026 | `aishe_district` |
| 57 | `MINUTES_NONGROCERY` | 20 | T2 | Netscribes, from Flipkart disclosure: mobiles/electronics ~20% of Minutes sales. Third-party estimate, stated as such | `basket` |
| 58 | `TERM_START_AOV` | 1,000 | T2 | Round 1 corpus: term-start durables, Rs1,000+ baskets | `basket` |
| 59 | `ATTRITION_MO` | 0.2 | T2 | dark-store monthly attrition 15-30% (QuickCommerceMap 2026) | `break_mode` |
| 60 | `MINUTES_AOV_R1` | 775 | T2 | Inc42 Aug 2026, midpoint Rs750-800. ROUND 1 BASIS. SUPERSEDED at S4 | `campus_model` |
| 61 | `MINUTES_ORD` | 1,050 | T2 | Inc42 Aug 2026, midpoint 1,000-1,100 orders/day/store | `campus_model` |
| 62 | `BLINKIT_BE_GOV` | 700,000 | T2 | "Blinkit breakeven point: Rs7,00,000 in daily gross order value" The Secretariat, trade press. NOT T1 - see shopping list item 10 | `cost_stack` |
| 63 | `GATE_MANUAL_MIN` | 3 | T2 | manual gate check-in ~3 min (Mygate Bengaluru pilot, Mar 2024) | `cost_stack` |
| 64 | `GATE_PREAPP_MIN` | 0.25 | T2 | pre-approved gate check-in <15 sec (same pilot, 1M+ uses) | `cost_stack` |
| 65 | `V1_LABOUR` | 361,000 | T2 | QuickCommerceMap wage bands, 18 staff | `cost_stack` |
| 66 | `V1_RENT` | 210,000 | T2 | Rs55-85/sqft (Bengaluru Rs50-75 FE via ThePrint; Delhi Rs74-111) | `cost_stack` |
| 67 | `CITY_AOV` | 700 | T2 | Datum/Reuters blended AOV, used for a RESIDENTIAL catchment | `risk_quadrant` |
| 68 | `LOCKIN_MO` | 30 | T2 | midpoint of the 24-36 month warehouse lock-in band | `risk_quadrant` |
| 69 | `CAPEX_MID` | 23,500,000 | T2 | Rs2.35 cr | `roce` |
| 70 | `HOSTEL_OCCUPANCY` | {16 entries} | D | residents / sanctioned intake from T1 Table 31 | `aishe_district` |
| 71 | `MIN_URBAN_COLLEGES` | 6 | D | a 3-6 college cluster plus headroom to choose within the district | `aishe_district` |
| 72 | `RESIDENTIAL_PCT` | {16 entries} | D | hostel residents / regular-mode enrolment from T1 tables | `aishe_district` |
| 73 | `URBAN_SHARE_FLOOR` | 0.5 | D | majority-urban district | `aishe_district` |
| 74 | `TERM_START_WEEKS` | 5 | D | 2-3 weeks x 2 term starts per academic year | `basket` |
| 75 | `MIN_WINDDOWN_WEEKS` | 7 | D | gap_check PROBE 4: below this the 28-day ramp and the T-21d wind-down collide, so no lever can be pulled | `calendar_fragmentation` |
| 76 | `BATCH_BASE` | 1.2 | D | disclosed 4 orders/hr / 3.33 trips = 1.2x | `cost_stack` |
| 77 | `DEMAND_KW` | 15 | D | sanctioned load implied by the 7.5 kW running draw plus headroom | `cost_stack` |
| 78 | `GIG_HR` | 168.254 | D | Rs168/active hour, from JPM: Rs26.5K/mo, 21 ord/day, 4 ord/hr | `fleet_mix` |
| 79 | `SKU_CAMPUS` | 8,000 | D | campus core range; the tail backfills from the SDFC | `rent_lever` |
| 80 | `VOLUME_SHOCK` | 0.3 | D | the -30% case the risk register has always carried (item 3) | `risk_shocks` |
| 81 | `LAST_MILE_D2` | 17.6132 | D | live D2 circuit model | `roce` |
| 82 | `NODE_LIFE_MO` | 60 | D | 5 years, anchored on JPM's 56-month franchised-store payback: a node must outlive its own payback [T1] | `roce` |
| 83 | `RESIDUAL_SHARE` | 0.4861 | D | 48.6%, the REPURPOSE fill rate | `roce` |
| 84 | `CAMPUSES` | 3 | D | [params] campuses per cluster; no single campus reaches the 7,778-resident minimum. BINDS fleet_mix too | `sla` |
| 85 | `PTDR_TROU` | 0.25 | D | trough as a fraction of the daily average | `sla` |
| 86 | `BLINKIT_STORES_FY26` | (1,800, 2,000) | D | store count not disclosed for FY26; range | `working_capital` |
| 87 | `COLD_PULLDOWN` | 1.5 | A | days of full cold-chain power to bring zones back to temperature | `break_mode` |
| 88 | `FSSAI_REVERIFY` | 15,000 | A | re-verification, pest control, deep clean before restock | `break_mode` |
| 89 | `HIRE_COST` | 8,000 | A | recruit + onboard + train one dark-store associate. NO SOURCE | `break_mode` |
| 90 | `RIDER_REACQ` | 1,200 | A | incentive to re-attract one gig rider to the zone after 3.5 months | `break_mode` |
| 91 | `HANDOFF_MIN` | 2 | A | doorstep dwell | `cost_stack` |
| 92 | `RIDER_DAYS` | 30 | A | assumed working days; gig, no fixed roster | `cost_stack` |
| 93 | `DROP_MIN` | 2 | A | per-drop inside the cluster: locate block/room, hand over | `fleet_mix` |
| 94 | `SHELF_DROP` | 0.5 | A | per-drop to a block-level pickup shelf instead of a room | `fleet_mix` |
| 95 | `SPREAD_KM` | 0.15 | A | added circuit distance per additional drop within a hostel cluster | `fleet_mix` |
| 96 | `REDEPLOY` | 0.55 | A | racking, chillers, IT are movable; leasehold fit-out is not | `risk_quadrant` |
| 97 | `RAMP_MONTHS` | 3 | A | the case's own implementation cap; linear ramp | `roce` |

**By tier:** T1 disclosure/analyst — 47  T1/T2 sourced — 1  T2 trade press — 21  D derived — 17  A assumed — 11
