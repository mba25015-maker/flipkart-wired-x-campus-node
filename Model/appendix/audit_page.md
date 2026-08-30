# Appendix — model audit

`audit.py` asserts every on-slide number against the model output. **344/344 pass.**

| Check | On slide | Model | OK |
|---|---:|---:|:--:|
| RECON sla in-gate leg == fleet_mix plan roster | 3.364 | 3.364 | yes |
| RECON sla gate count == params topology | 3 | 3 | yes |
| RECON fleet_mix optimises the gate volume params declares | 3 | 3 | yes |
| RECON roce last-mile == sla two-leg total | 17.613 | 17.613 | yes |
| RECON break_mode last-mile == sla weighted (no hardcoded 19.0) | 17.613 | 17.613 | yes |
| RECON break_mode restart WC == adopted 14d-on-NOV construct, scaled | 7552294.738 | 7552294.738 | yes |
| RECON working_capital adopted basis == params.NWC_DAYS | 14.0 | 14.0 | yes |
| RECON campus_model ceiling == params cluster volume | 1400 | 1400 | yes |
| S6     SLA table cost, trough | 54.5 | 54.541 | yes |
| S6     SLA table cost, average | 28.9 | 28.952 | yes |
| S6     SLA table cost, peak 4x | 8.5 | 8.482 | yes |
| S6     SLA table cost, exam 6x | 7.6 | 7.629 | yes |
| S6     the in-gate leg is FLAT across demand states | 0.0 | 0.0 | yes |
| SCAN  no policy literal redeclared outside params.py | 0 | 0 | yes |
| SCAN  no unsupported attribution in any build input | 0 | 0 | yes |
| RECON break_mode restart state == params.RESTART_CREDIT_STATE | 1.0 | 1.0 | yes |
| RECON basket TARGET_AOV == the D2-consistent spine breakeven | 573.096 | 573.096 | yes |
| RECON pooled upside is an UPSIDE, i.e. cheaper than the plan | 1.0 | 1.0 | yes |
| RECON campus_model.NWC_DAYS stays deleted | absent | absent | yes |
| CLAIM cheapest band is the peak band | Peak | Peak (late evening, exam windows) | yes |
| CLAIM fastest band is NOT peak (deck must not say fastest) | Normal | Normal | yes |
| S2/A2  full breakeven AOV @3x = Rs528 | 528 | 528.158 | yes |
| S2/A2  model contribution @Blinkit AOV = Rs29.4 | 29.4 | 29.4 | yes |
| A2     revenue per order = Rs134.7 | 134.7 | 134.705 | yes |
| A2     itemised stack = Rs93.0 | 93.0 | 93.0 | yes |
| A2     unallocated residual = Rs12.3 | 12.3 | 12.305 | yes |
| A1/A2  calendar surcharge = 1.412x | 1.412 | 1.412 | yes |
| A2     contribution breakeven @1x = Rs543 | 543 | 542.532 | yes |
| A2     contribution breakeven @3x = Rs398 | 398 | 398.276 | yes |
| A2     full breakeven @1x = Rs672 | 672 | 672.414 | yes |
| A2     full breakeven @4x = Rs510 | 510 | 510.126 | yes |
| A2     gate-drop lever = Rs144 | 144 | 144.256 | yes |
| A2     take-rate sensitivity low = Rs495 | 495 | 495.005 | yes |
| A2     throughput sensitivity, 1,334/day = Rs535 | 535 | 534.584 | yes |
| A2     throughput sensitivity, 1,487/day = Rs521 | 521 | 520.559 | yes |
| A2     consolidation span 1x-4x = Rs162 | 162 | 162.287 | yes |
| A2     full breakeven @2x = Rs564 | 564 | 564.222 | yes |
| A2/R1  city asset turn, ROUND 1 basis = 12.6x | 12.6 | 12.639 | yes |
| A2     campus asset turn = 8.1x | 8.1 | 8.133 | yes |
| A2     campus NOV = Rs19.1 cr | 19.1 | 19.111 | yes |
| A2/R1  city NOV, ROUND 1 basis = Rs29.7 cr | 29.7 | 29.702 | yes |
| S3/A3  minimum cluster = 7,778 residents | 7778 | 7777.778 | yes |
| A3     state gate = 38,889 residents | 38889 | 38888.889 | yes |
| S3/A3  states clearing gate = 21 | 21 | 21 | yes |
| S3/A3  states screened = 33 | 33 | 33 | yes |
| S1     hostel residents share = 11.1% | 11.1 | 11.076 | yes |
| S1     day-scholar + distance share = 89% | 89 | 88.924 | yes |
| S1     national hostel occupancy = 56.3% | 56.3 | 56.328 | yes |
| S1     empty hostel capacity = 44% | 44 | 43.672 | yes |
| S3     digital use low = 90.5% | 90.5 | 90.5 | yes |
| S3     gender gap = 1.3pp | 1.3 | 1.316 | yes |
| A3     concentration stability rho = 0.90 | 0.9 | 0.9 | yes |
| A3     axis-swap rho = 0.90 | 0.895 | 0.895 | yes |
| SF cal    v1 rent within 4% of JM | 3.2 | 3.226 | yes |
| SF cal    v1 labour within 4% of JM | 3.7 | 3.733 | yes |
| SF/JM     metro stack = Rs13,16,000/mo | 1316000 | 1316000 | yes |
| SF/JM     metro cost per order = Rs27 | 27 | 27.417 | yes |
| SF/JM     non-metro stack = Rs9,02,000/mo | 902000 | 902000 | yes |
| SF/JM     non-metro cost per order = Rs32 | 31.6 | 31.649 | yes |
| SF/D1    fixed stack sums to Rs9.02L | 902000 | 902000.0 | yes |
| SF/D1    rent share = 24.1% | 24.1 | 24.058 | yes |
| SF/D1    labour share = 41.6% | 41.6 | 41.574 | yes |
| SF/D1    truly-fixed share = 28.8% | 28.8 | 28.787 | yes |
| SF/D1    flexible share of fixed base = 71.2% | 71.2 | 71.213 | yes |
| SF/D1    store power draw = 4,260 kWh/month | 4260 | 4260.0 | yes |
| SF/D1    breakeven at Round 1 fixed = Rs528 | 528 | 528.158 | yes |
| SF/D1    breakeven at JM non-metro = Rs554 | 554 | 554.481 | yes |
| SF/D1    breakeven at JM metro = Rs626 | 626 | 626.176 | yes |
| SF/D2    JPM route = Rs42.1/delivery | 42.1 | 42.063 | yes |
| SF/D2    JM metro route = Rs48.1/delivery | 48.1 | 48.077 | yes |
| SF/D2    JM non-metro route = Rs44.0/delivery | 44.0 | 43.956 | yes |
| SF/D2    JPM route reconciles to LAST_MILE | 42.0 | 42.063 | yes |
| SF/D2    baseline batching = 1.20x | 1.2 | 1.2 | yes |
| SF/D2    rider cost per active hour = Rs168 | 168 | 168.254 | yes |
| SF/D2    rider utilisation = 40% | 40 | 40.385 | yes |
| SF/D2    intra-campus leg = 4.05 min | 4.05 | 4.05 | yes |
| SF/D2    campus door-drop trip = 29.1 min | 29.1 | 29.1 | yes |
| SF/D2    campus door-drop last mile = Rs68.0 | 68.0 | 68.003 | yes |
| SF/D2    Type A door-drop penalty = +62% | 62 | 61.911 | yes |
| SF/D2    pre-approved gate saves Rs6.4 | 6.4 | 6.426 | yes |
| SF/D2    Type B last mile = Rs26.9 | 26.9 | 26.874 | yes |
| SF/D2    gate-drop 4x last mile = Rs12.8 | 12.8 | 12.794 | yes |
| SF/D2    fee ceiling vs city @4x = Rs29.2 | 29.2 | 29.206 | yes |
| SF/D2    fee ceiling vs door-drop @4x = Rs55.2 | 55.2 | 55.208 | yes |
| SF/D2    campus runner labour floor = Rs9.6 | 9.6 | 9.615 | yes |
| SF/FM    gig rider per active hour = Rs168 | 168 | 168.254 | yes |
| SF/FM    employed runner per hour = Rs72 | 72 | 72.115 | yes |
| SF/FM    labour class ratio = 2.3x | 2.3 | 2.333 | yes |
| SF/FM    e-cart in-cluster @n=8 = Rs4.7 | 4.7 | 4.657 | yes |
| SF/FM    cycle in-cluster @n=3 = Rs8.4 | 8.4 | 8.413 | yes |
| SF/FM    on-foot in-cluster @n=4 = Rs13.8 | 13.8 | 13.762 | yes |
| SF/FM    cycle beats petrol 2W at n=3 | 1 | 1 | yes |
| SF/FM    full campus, e-cart+shelf @n=8 = Rs9.3 | 9.3 | 9.252 | yes |
| SF/FM    designed campus beats standard zone by 78% | 78 | 77.972 | yes |
| SF/FM    runner fully loaded = Rs577/day | 577 | 576.923 | yes |
| SF/FM    runner capacity = 202 orders/shift | 202 | 202.105 | yes |
| SF/FM    runner breakeven volume = 87 ord/day | 87 | 86.624 | yes |
| SF/FM    optimal roster at 1,400/day = 7 runners | 7 | 7 | yes |
| SF/FM    runner share at 1,400/day = 100% | 1.0 | 1.0 | yes |
| SF/FM    in-gate cost at 1,400/day = Rs2.88 | 2.88 | 2.885 | yes |
| SF/FM    1,400/day is 99% of 7 runners' capacity | 0.99 | 0.99 | yes |
| SF/FM    store floor 681/day tops up with gig | 0.89 | 0.89 | yes |
| SF/FM    in-gate cost at 681/day = Rs3.27 | 3.27 | 3.272 | yes |
| SF/FM    all-gig on the same leg = Rs6.66 | 6.66 | 6.66 | yes |
| SF/FM    optimised mix saves 57% against all-gig | 0.57 | 0.567 | yes |
| SF/FM    block shelf is worth Rs1.80/order | 1.8 | 1.803 | yes |
| SF/FM    door drop on the same circuit = Rs4.66 | 4.66 | 4.657 | yes |
| SF/FM    the closed form is not beaten by search | 1 | 1 | yes |
| SF/FM    Round 1 cluster orders/day = 1,400 | 1400 | 1400.04 | yes |
| SF/FM    cluster clears runner breakeven 16x | 16 | 16.162 | yes |
| SF/BM    break months = 3.5 | 3.5 | 3.5 | yes |
| SF/BM    unmitigated break deficit = Rs31.6L | 31.57 | 31.57 | yes |
| SF/BM    solvency runway at r=0 = 1.00x | 1.0 | 1.0 | yes |
| SF/BM    do-nothing threshold = 1/1.412 | 70.8 | 70.837 | yes |
| SF/BM    do-nothing threshold = 1/surcharge | 0.7083333333333333 | 0.708 | yes |
| SF/BM    labour-flex threshold = 59.1% | 59.1 | 59.058 | yes |
| SF/BM    + cold-chain threshold = 56.9% | 56.9 | 57.013 | yes |
| SF/BM    + small-format threshold = 48.5% | 48.5 | 48.615 | yes |
| SF/BM    cost levers cut threshold 31% | 31.5 | 31.372 | yes |
| SF/RL    small-format saving = Rs77,000 | 77000 | 77000.0 | yes |
| SF/RL    campus node format = 2,000 sqft | 2000 | 2000.0 | yes |
| SF/RL    on-campus node rent immaterial | 18.45 | 18.45 | yes |
| SF/BM    adjacent catchment lo = 469/day | 469 | 470.603 | yes |
| SF/BM    adjacent catchment hi = 567/day | 567 | 568.603 | yes |
| SF/SLA   one-gate arrival rate = 25.9/hr | 25.9 | 25.926 | yes |
| SF/SLA   average-state SLA = 21.6 min | 21.6 | 21.579 | yes |
| SF/SLA   peak-state SLA = 27.1 min | 27.1 | 27.136 | yes |
| SF/SLA   exam-night SLA = 27.1 min | 27.1 | 27.079 | yes |
| SF/SLA   10-15 min unreachable at every state | 1 | 1 | yes |
| SF/SLA   peak cost per order = Rs7.7 | 7.7 | 7.666 | yes |
| SF/SLA   dynamic batch at peak = 10 | 10 | 10 | yes |
| SF/SLA   dynamic batch at average = 2 | 2 | 2 | yes |
| SF/SLA   runners at peak = 3.7 | 3.7 | 3.664 | yes |
| SF/SLA   4x demand needs only 1.4x runners | 1.4 | 1.368 | yes |
| SF/SLA   volume-weighted cost = Rs17.6 | 17.6 | 17.613 | yes |
| SF/SLA   volume-weighted saving = 58% | 58 | 58.064 | yes |
| SF/SLA   peak carries 63% of daily orders | 62.7 | 62.745 | yes |
| SF/RB    rider days SOLVED = 28.7 | 28.7 | 28.68 | yes |
| SF/RB    rider days at Rs42 = 30.0 | 30.0 | 30.045 | yes |
| SF/RB    wind-down saving = Rs13.09L | 13.09 | 13.055 | yes |
| SF/RB    reactivation margin = 5.0x | 5.0 | 4.981 | yes |
| SF/RB    e-cart at Rs2.5L capex = Rs0.30/ord | 0.3 | 0.298 | yes |
| SF/RB    e-cart material only above Rs8.4L | 840000 | 840000.0 | yes |
| SF/RB    spread 0-0.5km moves cost <Rs2.2 | 2.2 | 2.163 | yes |
| SF/Q     min break for wind-down = 7 weeks | 7 | 7.0 | yes |
| SF/Q     revocation exposure = Rs145 lakh | 144.81 | 144.81 | yes |
| SF/Q     post-revocation orders needed = 513 | 513 | 513.393 | yes |
| SF/Q     binding site filter = 567/day | 567 | 568.603 | yes |
| SF/Q     revocation floor binds at low residual | 1 | 1 | yes |
| SF/Q     gig levy cap = Rs88,200/month | 88200 | 88200.0 | yes |
| SF/Q     gig levy = 9.8% of fixed base | 9.8 | 9.778 | yes |
| SF/JS    survey n = 35 stores | 35 | 35 | yes |
| SF/JS    area~SKU R2 within format = 0.02 | 0.02 | 0.015 | yes |
| SF/JS    observed NAOV median = Rs450 | 450 | 450.0 | yes |
| SF/JS    observed delivery median = 15 min | 15 | 15.0 | yes |
| SF/JS    stores at 10 min or less = 9% | 9 | 8.824 | yes |
| SF/JS    stores at 15 min or more = 68% | 68 | 67.647 | yes |
| SF/JS    observed OPD median = 1,500 | 1500 | 1500.0 | yes |
| SF/TF    Karnataka 2016 total = Rs8.98 | 8.98 | 8.98 | yes |
| SF/TF    BESCOM FY26 = Rs8.73 | 8.73 | 8.73 | yes |
| SF/TF    ten-year rebase factor = 0.972 | 0.972 | 0.972 | yes |
| SF/TF    model tariff equals sourced rate | 8.73 | 8.73 | yes |
| SF/TF    48 states/UTs in the cross-section | 48 | 48 | yes |
| SF/TF    state tariff CV = 30% | 30 | 30.282 | yes |
| SF/BM    runner floor = 6.2% of term volume | 6.2 | 6.187 | yes |
| SF/BM    reactivation opex @r=15% = Rs2.62L | 2.62 | 2.621 | yes |
| SF/BM    reactivation opex @r=0.15 = Rs2,62,119 | 262119 | 262118.537 | yes |
| SF/BM    reactivation = 0.71 months of surplus | 0.71 | 0.706 | yes |
| SF/BM    WC re-injection @r=15% = Rs75.5L [S20, pending 2.1] | 75.5 | 75.523 | yes |
| SF/BM    ramp-up lead time = 28 days | 28 | 28 | yes |
| S1     enrolment 4.46 cr vs hostel capacity 87.7 L | 19.7 | 19.664 | yes |
| S3     digital CV = 4% | 4 | 4.186 | yes |
| S3     concentration CV = 55% | 55 | 55.219 | yes |
| S3     orders/resident = 1.5x Blinkit 3.6/mo | 0.18 | 0.18 | yes |
| S2/A2  campus CM required = 4.8% of order value | 4.8 | 4.775 | yes |
| A2     top-cohort store CM benchmark = 4.0% | 4.0 | 4.0 | yes |
| S2     franchise payback = 56 months | 56 | 56 | yes |
| A3     scale gate anchor = 0.18 (1.5x Blinkit) | 0.18 | 0.18 | yes |
| S17    Exhibit 13 rent Rs70/sqft is in Tier-1/2 band | 1 | 1 | yes |
| S17    fixed base @ Rs60/sqft = Rs8.71L | 871000 | 871000 | yes |
| S17    fixed base @ Rs75/sqft = Rs9.18L | 917500 | 917500 | yes |
| S17    Tier-1/2 band width = 5.2% of base | 5.2 | 5.155 | yes |
| S17    Tier-3+ store would be Rs7.66L | 765750 | 765750.0 | yes |
| S17    Tier-3+ is 15.1% below our base | -15.1 | -15.105 | yes |
| S17    util+other Rs3.10L is JM Rs100/sqft blended | 310000 | 310000 | yes |
| S18    model basis is GROSS order value | 1 | 1 | yes |
| S18    BLINKIT_AOV 694 inside gross band 691-719 | 1 | 1 | yes |
| S18    Rs528 breakeven vs Blinkit NAOV Rs528 is coincidence | 0 | -0.042 | yes |
| S18    MINUTES_AOV adopted = Rs450 (S4) | 450 | 450.0 | yes |
| S18    city asset turn, adopted basis = 7.34x | 7.34 | 7.339 | yes |
| S18    campus asset turn, adopted basis = 6.93x | 6.93 | 6.931 | yes |
| S18    campus/city turn ratio = 0.944 | 0.944 | 0.944 | yes |
| S18    ratio == density x calendar identity | 0 | 0.0 | yes |
| S18    calendar leg of identity = 0.708 = 1/1.412 | 0.708 | 0.708 | yes |
| S18    city NOV, adopted basis = Rs17.2 cr | 17.2 | 17.246 | yes |
| S18    CRISIL per-tonne rate does NOT price our cold room | 0 | 0 | yes |
| S18    CRISIL rate implies absurd 41t inside 3,100 sqft | 41 | 41.143 | yes |
| S19    D2 volume-weighted last mile = Rs17.6 | 17.6 | 17.613 | yes |
| S19    UBS 2.7/hr is FOOD DELIVERY, not adopted | 0 | 0 | yes |
| S19    gig:runner ratio, JPM anchor = 2.33x | 2.33 | 2.333 | yes |
| S19    gig:runner ratio, FD anchor = 1.60x | 1.6 | 1.596 | yes |
| S19    labour-class conclusion holds on both | 1 | 1 | yes |
| S19    ads already inside the 19.41% take rate | 1 | 1 | yes |
| S19    D2-implied consolidation = 2.38x | 2.38 | 2.385 | yes |
| S19    breakeven @3.00x proxy = Rs554 (superseded) | 554.5 | 554.481 | yes |
| S19    breakeven D2-consistent = Rs573 (ADOPTED) | 573.1 | 573.096 | yes |
| S21    Instamart mix->AOV slope = Rs11.3/pt | 11.28 | 11.281 | yes |
| S21    fit R2 = 0.918 | 0.918 | 0.918 | yes |
| S21    non-grocery needed after occasions = 24.3% | 24.3 | 24.293 | yes |
| S21    fits under mgmt 30-40% ceiling | 1 | 1 | yes |
| S21    Minutes non-grocery today = 20% | 20.0 | 20.0 | yes |
| S21    term-start occasion lifts AOV to Rs525 | 525 | 524.661 | yes |
| S21    hold-through-break cost = Rs21.3L | 21.3 | 21.256 | yes |
| S21    relocation capex = Rs89L | 89.0 | 89.0 | yes |
| S21    holding = 24% of one relocation | 0.24 | 0.239 | yes |
| S22    NWC days now 14 (was 18, target 12) | 14.0 | 14.0 | yes |
| S22    WC adopted = Rs88.9L (NWC days x NOV) | 88.9 | 88.851 | yes |
| S22    WC at 12-day steady state = Rs76.2L | 76.2 | 76.158 | yes |
| S22    old COGS x 18d construct = Rs116.4L (rejected) | 116.4 | 116.388 | yes |
| S22    restatement vs Rs95.7L = -7.2% | -7.2 | -7.157 | yes |
| S22    Zepto cash conversion cycle = -47 days | -47.0 | -47.0 | yes |
| S22    State A (credit intact) WC = Rs0 | 0 | 0.0 | yes |
| S22    State B, 30d to re-establish = Rs44.4L | 44.4 | 44.425 | yes |
| S22    per-store inventory benchmark UNRESOLVED | 0 | 0 | yes |
| S22    shrinkage 1.8% of NOV = Rs3.43L/month | 3.43 | 3.427 | yes |
| CC1     solver rows = 5 strategies | 5 | 5 | yes |
| CC1     DO_NOTHING dead-zone deficit = Rs31.57L | 31.57 | 31.57 | yes |
| CC1     LABOUR_FLEX dead-zone deficit = Rs21.60L | 21.595 | 21.595 | yes |
| CC1     COLD_RIGHTSIZE dead-zone deficit = Rs21.21L | 21.21 | 21.21 | yes |
| CC1     SMALL_FORMAT dead-zone deficit = Rs18.52L | 18.515 | 18.515 | yes |
| CC1     REPURPOSE dead-zone deficit = Rs0 | 0 | 0.0 | yes |
| CC1     DO_NOTHING residual req = 70.8% | 70.8 | 70.837 | yes |
| CC1     LABOUR_FLEX residual req = 59.1% | 59.1 | 59.058 | yes |
| CC1     SMALL_FORMAT residual req = 48.6% | 48.6 | 48.615 | yes |
| CC1     REPURPOSE residual req == SMALL_FORMAT | 0 | 0.0 | yes |
| CC1     wind-down reactivation opex = Rs2.74L | 2.741 | 2.741 | yes |
| CC1     DO_NOTHING reactivation = Rs0 | 0 | 0.0 | yes |
| CC1     REPURPOSE reactivation = Rs0 | 0 | 0.0 | yes |
| CC1     wind-down days to full service = 28 | 28 | 28 | yes |
| CC1     DO_NOTHING days to full service = 0 | 0 | 0 | yes |
| CC1     lead-time constraint = 28 days | 28 | 28 | yes |
| CC1     SLA-at-peak constraint = 27.1 min | 27.1 | 27.136 | yes |
| CC1     catchment-floor constraint = 513/day | 513.4 | 513.393 | yes |
| CC1     7-week wind-down rule = 7 weeks | 7 | 7.0 | yes |
| CC1     BEST = REPURPOSE | 1 | 1 | yes |
| CC1     SMALL_FORMAT beats DO_NOTHING on burn | 1 | 1 | yes |
| S23    HANDOFF.md figures tie out to the model | 1 | 1 | yes |
| S24    colleges in register = 54,014 | 54014 | 54014 | yes |
| S24    universities = 1,428 | 1428 | 1428 | yes |
| S24    standalone = 16,910 | 16910 | 16910 | yes |
| S24    total HEIs = 72,352 | 72352 | 72352 | yes |
| S24    districts covered = 760 | 760 | 760 | yes |
| S24    urban colleges = 21,000 | 21000 | 21000 | yes |
| S24    rural colleges = 32,336 | 32336 | 32336 | yes |
| S24    URBAN SHARE of colleges = 39.4% | 39.4 | 39.373 | yes |
| S24    candidate districts after screen = 111 | 111 | 111 | yes |
| S24    urban high-propensity standalones = 1,897 | 1897 | 1897 | yes |
| S24    top-ranked district is Khordha (Odisha) | 1 | 1 | yes |
| S24    Karnataka districts in top 20 = 14 | 14 | 14 | yes |
| CC4     lever set = 7 | 7 | 7 | yes |
| CC4     dimensions = 5 | 5 | 5 | yes |
| CC4     silhouette-selected k = 4 | 4 | 4 | yes |
| CC4     chosen k has the max silhouette | 1 | 1 | yes |
| CC4     LABOUR_FLEX recoverability = 31.6% of base | 31.6 | 31.596 | yes |
| CC4     SMALL_FORMAT recoverability = 8.5% of base | 8.5 | 8.537 | yes |
| CC4     LABOUR_FLEX restart cost = 0.48 months of surplus | 0.479 | 0.479 | yes |
| CC4     DYNAMIC_BATCH SLA cost at peak = +10.2 min | 10.157 | 10.157 | yes |
| CC4     LABOUR_FLEX is a singleton cluster | 1 | 1 | yes |
| CC4     E_CART is a singleton cluster (only capex lever) | 1 | 1 | yes |
| S26    contiguous dead-zone cost = Rs21.3L | 21.3 | 21.297 | yes |
| S26    typical fragmented cost = Rs27.5L | 27.5 | 27.494 | yes |
| S26    typical penalty = +29% | 29.0 | 29.101 | yes |
| S26    worst-shape penalty = +49% | 49.0 | 48.563 | yes |
| S26    typical wind-downable share = 53% | 53.0 | 52.632 | yes |
| S26    all-short-gaps calendar qualifies = NO | 0 | 0 | yes |
| S26    typical calendar qualifies = YES | 1 | 1 | yes |
| S26    -30% volume shock on ADOPTED basis = Rs647 | 647.1 | 647.186 | yes |
| S8      shock base = D2-consistent Rs573 | 573.1 | 573.096 | yes |
| S8      volume -30% -> Rs640 | 640.0 | 640.041 | yes |
| S8      shrinkage upper bound -> Rs615 | 615.1 | 615.135 | yes |
| S8      gig levy -> Rs588 | 588.4 | 588.37 | yes |
| S8      calendar fragmentation -> Rs582 | 582.0 | 582.04 | yes |
| S8      volume is the largest shock | 1 | 1 | yes |
| S8      shrinkage is 80% of the residual = DOUBLE COUNT | 80.3 | 80.299 | yes |
| S8      shrinkage double-count flag is set | 1 | 1 | yes |
| S8      basket reaches Rs637 at the 30% floor | 637.5 | 637.475 | yes |
| S8      basket reaches Rs750 at the 40% ceiling | 750.3 | 750.29 | yes |
| S8      3 of 4 shocks covered inside the 30% floor | 3 | 3 | yes |
| S8      4 of 4 shocks covered inside the 40% ceiling | 1 | 1 | yes |
| CC6     labour classes = 4 | 4 | 4 | yes |
| CC6     gig cost/order, JPM anchor = Rs42.1 | 42.06 | 42.063 | yes |
| CC6     gig cost/active hour = Rs168 | 168 | 168.254 | yes |
| CC6     gig fixed cost/day = Rs0 (structural) | 0 | 0.0 | yes |
| CC6     runner fixed cost/day = Rs577 | 577 | 576.923 | yes |
| CC6     runner in-cluster cost/order = Rs4.7 | 4.7 | 4.657 | yes |
| CC6     runner rostered hour = Rs72 | 72 | 72.115 | yes |
| CC6     runner threshold SOLVED = 87 orders/day | 87 | 86.624 | yes |
| CC6     gig cost/km derived = Rs2.36 | 2.357 | 2.357 | yes |
| CC6     gig km per order = 4.44 | 4.444 | 4.444 | yes |
| CC6     JM non-metro rider utilisation = 36% | 36.5 | 36.458 | yes |
| CC6     labour-class ratio = 2.33x | 2.333 | 2.333 | yes |
| CC6     incentive column FLAGGED, not invented | 0 | 0 | yes |
| CC7     five-operator store total = 6,693 | 6693 | 6693 | yes |
| CC7     non-metro stores = 2,393 | 2393 | 2393 | yes |
| CC7     metros run +19% over sustainable capacity | 19.4 | 19.444 | yes |
| CC7     stores added per NEW pin code = 5.9 | 5.92 | 5.921 | yes |
| CC7     operators per served pin code = 2.46 | 2.459 | 2.459 | yes |
| CC7     metro:non-metro store density = 10.0x | 10.0 | 10.014 | yes |
| CC7     candidate districts screened = 111 | 111 | 111 | yes |
| CC7     uncontested candidate districts = 9 | 9 | 9 | yes |
| CC7     stacked share of candidates = 72% | 72 | 72.072 | yes |
| CC7     filter restated = 569/day UNCONTESTED | 568.6 | 568.603 | yes |
| CC7     gross required at metro overlap = 1,015/day | 1015.4 | 1015.363 | yes |
| CC7     uncontested filter == risk_quadrant binding filter | 0 | 0.0 | yes |
| S5      turn ratio at 1,000 orders/day = 0.675 | 0.675 | 0.675 | yes |
| S5      turn ratio at 1,200 orders/day = 0.810 | 0.81 | 0.81 | yes |
| S5      turn ratio at 1,400 orders/day = 0.944 | 0.944 | 0.944 | yes |
| S5      parity throughput = 1,482 orders/day | 1482 | 1482.353 | yes |
| S5      parity sits INSIDE Blinkit's observed range | 1 | 1 | yes |
| S5      parity = 99.7% of the observed maximum | 0.997 | 0.997 | yes |
| S5      ratio across the observed range, low  = 0.900 | 0.9 | 0.9 | yes |
| S5      ratio across the observed range, high = 1.003 | 1.003 | 1.003 | yes |
| S5      parity OPD == city OPD x calendar surcharge | 0 | -0.0 | yes |
| S30     capital employed rounds to Rs324 lakh | 324.0 | 323.851 | yes |
| S30     capex midpoint = Rs235.0 lakh | 235.0 | 235.0 | yes |
| S30     orders/year, term-only basis | 361900 | 361958.333 | yes |
| S30     ROCE breakeven AOV reproduces the spine | 1 | 1 | yes |
| S30     day-count gap to the spine = Rs2.14 | 2.14 | 2.14 | yes |
| S30     AOV for ROCE = 0 is Rs571 | 571 | 570.956 | yes |
| S30     AOV for the 40% hurdle is Rs755 | 755 | 755.339 | yes |
| S30     post-tax hurdle AOV is Rs817 | 817 | 817.359 | yes |
| S30     hurdle premium over breakeven = Rs185 | 185 | 184.383 | yes |
| S30     non-grocery share implied by the hurdle = 32.3% | 32.3 | 32.301 | yes |
| S30     hurdle sits within the external comparator range | 1 | 1 | yes |
| S30     DuPont identity closes: margin x turn = ROCE | 0 | 0.0 | yes |
| S30     ROCE at the hurdle AOV = 40% | 0.4 | 0.4 | yes |
| S30     ROCE at a 30% non-grocery basket = 34.4% | 34.4 | 34.369 | yes |
| S30     ROCE under the -30% volume shock = 14.0% | 14.0 | 14.032 | yes |
| S30     downside payback exceeds the node's anchored life | 1 | 1 | yes |
| S30     IRR at the hurdle AOV = 34.4% | 34.4 | 34.357 | yes |
| S30     repurpose is worth Rs26 of AOV | 26 | 25.696 | yes |
| S30     slide-4 turn is the like-for-like quantity | 6.93 | 6.931 | yes |
| S30     tax rate = 25.17% | 25.17 | 25.17 | yes |
| SELF  check_counts.AUDIT_COUNT matches this run | 344 | 344 | yes |
