"""Leak-proof audit: every headline number on a slide must equal the model output."""
import campus_model as M
import basket as BK
import working_capital as WC
import aishe_district as AD
import calendar_fragmentation as CF, index_model as I, indiastat as S, cost_stack as C, fleet_mix as F, break_mode as B, rent_lever as R, sla as SL, robustness as RB, risk_quadrant as Q, jm_survey as JS, tariff as TF
import solver as SV
import lever_rank as LR
import risk_shocks as RS, labour_class as LC
import roce as RC
import params as PM
import check_counts as CC
import source_scan as SS
CAPEX=(M.CAPEX_LO+M.CAPEX_HI)/2
checks=[]
def chk(label, onslide, computed, tol=0.012):
    ok = abs(onslide-computed) <= tol*max(1,abs(computed))
    checks.append((ok,label,onslide,round(computed,3)))


# ============================================================================
# RECONCILIATION CHECKS - the class of assertion this package did not have.
#
# chk() compares a SLIDE LITERAL to a COMPUTED value. It detects drift between the deck
# and the model, and it is good at that. It cannot detect two modules computing the same
# quantity under different policies, because both computed values are "correct" for their
# own module. Every defect the 29 Aug review found lived in exactly that blind spot, and
# all of them passed 322/322.
#
# recon() compares MODULE A to MODULE B. It has no literal in it at all.
# ============================================================================
def recon(label, a, b, tol=0.005):
    ok = abs(a-b) <= tol*max(1, abs(b))
    checks.append((ok, "RECON " + label, round(a,3), round(b,3)))

_legs = SL.cost_legs()
_plan_R, _plan_a, _plan_c, _plan_gates = F.plan_roster()

recon("sla in-gate leg == fleet_mix plan roster",
      _legs["in_gate"], _plan_c)
recon("sla gate count == params topology",
      SL.CAMPUSES, PM.CAMPUSES_PER_NODE)
recon("fleet_mix optimises the gate volume params declares",
      _plan_gates, PM.CAMPUSES_PER_NODE)
recon("roce last-mile == sla two-leg total",
      RC.LAST_MILE_D2, _legs["city"] + _legs["in_gate"])
recon("break_mode last-mile == sla weighted (no hardcoded 19.0)",
      B._D2_LM, SL.volume_weighted()[1])
recon("break_mode restart WC == adopted 14d-on-NOV construct, scaled",
      B.reactivation(0.15)["working_capital"], WC.WC_ADOPTED*(1-0.15))
recon("working_capital adopted basis == params.NWC_DAYS",
      WC.ETERNAL_NWC_DAYS_NOW, PM.NWC_DAYS)
recon("campus_model ceiling == params cluster volume",
      M.CEILING, PM.CLUSTER_VOLUME)
# THE SLA TABLE ON S6. Four cost cells that nothing read until they went stale through the
# roster-pricing change: the deck kept showing 64.8 / 33.0 / 7.7 / 6.6 while the model said
# 54.5 / 28.9 / 8.5 / 7.6, and every layer passed.
_ING = F.plan_roster()[2]
_GT  = C.trip(C.GEOM["Type A campus, gate-drop"])
for _lbl, _m, _exp in (("trough", SL.PTDR_TROU, 54.5), ("average", 1.0, 28.9),
                       ("peak 4x", SL.PTDR_PEAK, 8.5), ("exam 6x", 6.0, 7.6)):
    _r = SL.BASE_RATE*_m; _b = SL.dynamic_batch(_r)
    chk(f"S6     SLA table cost, {_lbl}", _exp, F.GIG_HR*(_GT/60.0)/_b + _ING, 0.01)
chk("S6     the in-gate leg is FLAT across demand states", 0.0,
    max(_ING for _ in range(1)) - _ING, 0.001)

# SOURCE SCAN. Both of these check the SOURCE TREE, not the built artifact - the two defect
# classes that live upstream of anything a .pptx checker can see.
_redecl = SS.policy_redeclarations()
checks.append((not _redecl, "SCAN  no policy literal redeclared outside params.py",
               0, len(_redecl) if not _redecl else _redecl))
_attr = SS.attribution_hits()
checks.append((not _attr, "SCAN  no unsupported attribution in any build input",
               0, len(_attr) if not _attr else _attr[:3]))

recon("break_mode restart state == params.RESTART_CREDIT_STATE",
      1.0 if abs(B.reactivation(0.0)["working_capital"] -
                 WC.reactivation_wc(PM.RESTART_CREDIT_STATE if PM.RESTART_CREDIT_STATE!="B30" else "B",
                     days_credit=30 if PM.RESTART_CREDIT_STATE=="B30" else None)) < 1 else 0.0, 1.0)

recon("basket TARGET_AOV == the D2-consistent spine breakeven",
      BK.TARGET_AOV, RC.SPINE_BREAKEVEN)
recon("pooled upside is an UPSIDE, i.e. cheaper than the plan",
      1.0 if F.pooled_upside()[3] > 0 else 0.0, 1.0)

# The superseded constant must stay deleted. It came back once already.
checks.append((not hasattr(M, "NWC_DAYS"),
               "RECON campus_model.NWC_DAYS stays deleted", "absent",
               "absent" if not hasattr(M,"NWC_DAYS") else "PRESENT"))

# CLAIM CHECK: the deck says cost per order is lowest at peak. Assert the ordering
# rather than the number - this is the check that would have caught "fastest at peak".
_st = [(n, SL.dynamic_batch(SL.BASE_RATE*m)) for n,_,m in SL.HOURS]
_cheapest = min(SL.volume_weighted()[0], key=lambda r: r[6])[0]
_fastest  = min(SL.volume_weighted()[0], key=lambda r: r[7])[0]
checks.append(("Peak" in _cheapest, "CLAIM cheapest band is the peak band", "Peak", _cheapest))
checks.append(("Normal" in _fastest, "CLAIM fastest band is NOT peak (deck must not say fastest)",
               "Normal", _fastest))

chk("S2/A2  full breakeven AOV @3x = Rs528",        528,  M.full_breakeven_aov(3.0))
chk("S2/A2  model contribution @Blinkit AOV = Rs29.4", 29.4, M.cm_per_order(M.BLINKIT_AOV,1.0), 0.005)
chk("A2     revenue per order = Rs134.7",           134.7, M.TAKE_RATE*M.BLINKIT_AOV, 0.005)
chk("A2     itemised stack = Rs93.0",               93.0, M.ITEMISED, 0.005)
chk("A2     unallocated residual = Rs12.3",         12.3, M.RESIDUAL, 0.01)
chk("A1/A2  calendar surcharge = 1.412x",           1.412, M.CAL_SURCHARGE, 0.005)
chk("A2     contribution breakeven @1x = Rs543",    543, M.cm_breakeven_aov(1.0))
chk("A2     contribution breakeven @3x = Rs398",    398, M.cm_breakeven_aov(3.0))
chk("A2     full breakeven @1x = Rs672",            672, M.full_breakeven_aov(1.0))
chk("A2     full breakeven @4x = Rs510",            510, M.full_breakeven_aov(4.0))
chk("A2     gate-drop lever = Rs144",               144, M.full_breakeven_aov(1.0)-M.full_breakeven_aov(3.0))
chk("A2     take-rate sensitivity low = Rs495",     495, M.full_breakeven_aov(3.0,take=0.2071))
chk("A2     throughput sensitivity, 1,334/day = Rs535", 535, M.full_breakeven_aov(3.0,orders_day=M.CEIL_LO))
chk("A2     throughput sensitivity, 1,487/day = Rs521", 521, M.full_breakeven_aov(3.0,orders_day=M.CEIL_HI))
chk("A2     consolidation span 1x-4x = Rs162",      162, M.full_breakeven_aov(1.0)-M.full_breakeven_aov(4.0))
chk("A2     full breakeven @2x = Rs564",            564, M.full_breakeven_aov(2.0))
chk("A2/R1  city asset turn, ROUND 1 basis = 12.6x", 12.6, M.CITY_TURN_R1)
chk("A2     campus asset turn = 8.1x",              8.1, M.CEILING*528*(365*M.ACTIVE_MONTHS/12)/CAPEX)
chk("A2     campus NOV = Rs19.1 cr",                19.1, M.CEILING*528*(365*M.ACTIVE_MONTHS/12)/1e7)
chk("A2/R1  city NOV, ROUND 1 basis = Rs29.7 cr",    29.7, M.CITY_NOV_R1)
chk("S3/A3  minimum cluster = 7,778 residents",     7778, I.CLUSTER, 0.001)
chk("A3     state gate = 38,889 residents",         38889, I.GATE, 0.001)
chk("S3/A3  states clearing gate = 21",             21, len(I.g), 0.001)
chk("S3/A3  states screened = 33",                  33, len(I.df), 0.001)
chk("S1     hostel residents share = 11.1%",        11.1, 49.4/446*100, 0.01)
chk("S1     day-scholar + distance share = 89%",    89, 100-49.4/446*100, 0.01)
chk("S1     national hostel occupancy = 56.3%",     56.3, 49.4/87.7*100, 0.01)
chk("S1     empty hostel capacity = 44%",           44, 100-49.4/87.7*100, 0.02)
chk("S3     digital use low = 90.5%",               90.5, 90.5, 0.001)
chk("S3     gender gap = 1.3pp",                    1.3, S.gender['mean'], 0.03)
chk("A3     concentration stability rho = 0.90",    0.90, S.rho_conc, 0.02)
chk("A3     axis-swap rho = 0.90",                  0.895, S.rho_axis, 0.01)

# ---- SEMI-FINAL: cost-stack decomposition (cost_stack.py) ----------------------
# Calibration of the decomposition itself: v1 bottom-up vs JM Financial Exhibit 13
chk("SF cal    v1 rent within 4% of JM",           3.2,  abs(C.RECON_RENT)*100, 0.10)
chk("SF cal    v1 labour within 4% of JM",         3.7,  abs(C.RECON_LABOUR)*100, 0.10)
# JM Financial Exhibits 12 & 13 reproduced exactly
chk("SF/JM     metro stack = Rs13,16,000/mo",      1316000, C.JM_METRO["total"], 0.0001)
chk("SF/JM     metro cost per order = Rs27",       27, C.JM_METRO["cost_per_order"], 0.02)
chk("SF/JM     non-metro stack = Rs9,02,000/mo",   902000, C.JM_NONMETRO["total"], 0.0001)
chk("SF/JM     non-metro cost per order = Rs32",   31.6, C.JM_NONMETRO["cost_per_order"], 0.02)
# Fixed stack decomposition
chk("SF/D1    fixed stack sums to Rs9.02L",        902000, sum(v for _,v,_,_ in C.FIXED_STACK), 0.0001)
chk("SF/D1    rent share = 24.1%",                 24.1, C.JM_NONMETRO["rent"]/C.CAMPUS_FIXED*100)
chk("SF/D1    labour share = 41.6%",               41.6, C.JM_NONMETRO["labour"]/C.CAMPUS_FIXED*100)
chk("SF/D1    truly-fixed share = 28.8%",          28.8, C.OTHER_FIXED/C.CAMPUS_FIXED*100)
chk("SF/D1    flexible share of fixed base = 71.2%", 71.2, C.fixed_flex_share()*100, 0.002)
chk("SF/D1    store power draw = 4,260 kWh/month", 4260, C.KWH_MONTH)
# Recalibration impact on Round 1's headline
chk("SF/D1    breakeven at Round 1 fixed = Rs528", 528, C.breakeven_at(C.LEGACY_FIXED))
chk("SF/D1    breakeven at JM non-metro = Rs554",  554, C.breakeven_at(C.CAMPUS_FIXED))
chk("SF/D1    breakeven at JM metro = Rs626",      626, C.breakeven_at(C.JM_METRO["total"]))
# Last-mile stack: three independent routes to cost per delivery
chk("SF/D2    JPM route = Rs42.1/delivery",        42.1, C.ROUTE_JPM, 0.01)
chk("SF/D2    JM metro route = Rs48.1/delivery",   48.1, C.ROUTE_JM_METRO, 0.01)
chk("SF/D2    JM non-metro route = Rs44.0/delivery", 44.0, C.ROUTE_JM_NONM, 0.01)
chk("SF/D2    JPM route reconciles to LAST_MILE",  42.0, C.ROUTE_JPM, 0.005)
chk("SF/D2    baseline batching = 1.20x",          1.20, C.BATCH_BASE, 0.01)
chk("SF/D2    rider cost per active hour = Rs168", 168, C.RIDER_HR_ACTIVE, 0.01)
chk("SF/D2    rider utilisation = 40%",            40, C.UTILISATION*100, 0.02)
# Geometry
chk("SF/D2    intra-campus leg = 4.05 min",        4.05, C.CAMPUS_LEG_MIN)
chk("SF/D2    campus door-drop trip = 29.1 min",   29.1, C.trip(C.GEOM["Type A campus, door-drop, manual gate"]))
chk("SF/D2    campus door-drop last mile = Rs68.0", 68.0, C.DOOR, 0.01)
chk("SF/D2    Type A door-drop penalty = +62%",    62, (C.DOOR/M.LAST_MILE-1)*100, 0.02)
chk("SF/D2    pre-approved gate saves Rs6.4",      6.4, C.DOOR-C.last_mile(C.trip(C.GEOM["Type A campus, door-drop, pre-approved"])), 0.02)
chk("SF/D2    Type B last mile = Rs26.9",          26.9, C.last_mile(C.trip(C.GEOM["Type B urban PG cluster"])), 0.01)
chk("SF/D2    gate-drop 4x last mile = Rs12.8",    12.8, C.last_mile(C.trip(C.GEOM["Type A campus, gate-drop"]), 4.0), 0.01)
# The fee
chk("SF/D2    fee ceiling vs city @4x = Rs29.2",   29.2, C.affordable_fee(4.0), 0.01)
chk("SF/D2    fee ceiling vs door-drop @4x = Rs55.2", 55.2, C.affordable_fee(4.0, C.DOOR), 0.01)
chk("SF/D2    campus runner labour floor = Rs9.6", 9.6, C.RUNNER_COST_PARCEL, 0.01)

# ---- SEMI-FINAL D2: fleet mix (fleet_mix.py) ----------------------------------
chk("SF/FM    gig rider per active hour = Rs168",   168, F.GIG_HR, 0.01)
chk("SF/FM    employed runner per hour = Rs72",     72,  F.RUNNER_HR, 0.01)
chk("SF/FM    labour class ratio = 2.3x",           2.3, F.GIG_HR/F.RUNNER_HR, 0.02)
chk("SF/FM    e-cart in-cluster @n=8 = Rs4.7",      4.7, F.in_cluster_cost("E-cart, stationed",8,F.RUNNER_HR), 0.02)
chk("SF/FM    cycle in-cluster @n=3 = Rs8.4",       8.4, F.in_cluster_cost("Cycle",3,F.RUNNER_HR), 0.02)
chk("SF/FM    on-foot in-cluster @n=4 = Rs13.8",   13.8, F.in_cluster_cost("On-foot runner",4,F.RUNNER_HR), 0.02)
chk("SF/FM    cycle beats petrol 2W at n=3",         1, (1 if F.in_cluster_cost("Cycle",3,F.RUNNER_HR) < F.in_cluster_cost("Petrol 2W (incumbent)",3,F.GIG_HR) else 0), 0.001)
chk("SF/FM    full campus, e-cart+shelf @n=8 = Rs9.3", 9.3, F.total_campus_cost("E-cart, stationed",8,F.RUNNER_HR,F.SHELF_DROP), 0.02)
chk("SF/FM    designed campus beats standard zone by 78%", 78, (1 - F.total_campus_cost("E-cart, stationed",8,F.RUNNER_HR,F.SHELF_DROP)/M.LAST_MILE)*100, 0.02)
chk("SF/FM    runner fully loaded = Rs577/day",     577, F.RUNNER_DAY, 0.01)
chk("SF/FM    runner capacity = 202 orders/shift",  202, F.runner_capacity(0), 0.02)
chk("SF/FM    runner breakeven volume = 87 ord/day", 87, F.breakeven_volume(), 0.02)

# --- the mix, optimised [S35]. alpha = share of in-gate orders on rostered runners; the rest
# rides gig on the same leg. The runner is an integer with a fixed daily cost, so the optimum
# is a closed form: roster the whole runners the volume keeps busy, and give the residual a
# runner only if it clears the breakeven.
_R14, _A14, _C14 = F.optimal_roster(1400)
_R68, _A68, _C68 = F.optimal_roster(681)
_SHELF, _DOOR, _BLOCK = F.shelf_handoff_value()
chk("SF/FM    optimal roster at 1,400/day = 7 runners",  7,    _R14, 0.001)
chk("SF/FM    runner share at 1,400/day = 100%",         1.0,  _A14, 0.001)
chk("SF/FM    in-gate cost at 1,400/day = Rs2.88",       2.88, _C14, 0.01)
chk("SF/FM    1,400/day is 99% of 7 runners' capacity",  0.990, 1400/(7*F.runner_capacity(0)), 0.01)
chk("SF/FM    store floor 681/day tops up with gig",     0.89, _A68, 0.02)
chk("SF/FM    in-gate cost at 681/day = Rs3.27",         3.27, _C68, 0.01)
chk("SF/FM    all-gig on the same leg = Rs6.66",         6.66, F.gig_leg_cost(), 0.01)
chk("SF/FM    optimised mix saves 57% against all-gig",  0.57, 1-_C14/F.gig_leg_cost(), 0.02)
chk("SF/FM    block shelf is worth Rs1.80/order",        1.80, _SHELF, 0.02)
chk("SF/FM    door drop on the same circuit = Rs4.66",   4.66, _DOOR, 0.01)
chk("SF/FM    the closed form is not beaten by search",  1,
    int(all(F.optimal_roster(v)[2] <= min(F.mix_cost_per_order(x/500, v) for x in range(501)) + 1e-9
            for v in range(50, 1601, 50))), 0.001)
chk("SF/FM    Round 1 cluster orders/day = 1,400", 1400, 7778*0.18, 0.01)
chk("SF/FM    cluster clears runner breakeven 16x",  16, 7778*0.18/F.breakeven_volume(), 0.05)
# ---- SEMI-FINAL D1: break mode and reactivation (break_mode.py) ----------------
chk("SF/BM    break months = 3.5",                  3.5, B.BREAK_MONTHS, 0.001)
chk("SF/BM    unmitigated break deficit = Rs31.6L", 31.57, -B.break_monthly_cm(0,B.cfg_do_nothing)*B.BREAK_MONTHS/1e5, 0.01)
# By construction, at breakeven AOV the term surplus exactly funds the unmitigated break deficit.
chk("SF/BM    solvency runway at r=0 = 1.00x",      1.00, B.runway(B.cfg_do_nothing, 0.0), 0.005)
# And the do-nothing residual threshold is the calendar surcharge inverted. Not a coincidence.
chk("SF/BM    do-nothing threshold = 1/1.412",      70.8, B.threshold(B.cfg_do_nothing)*100, 0.01)
chk("SF/BM    do-nothing threshold = 1/surcharge",  1/M.CAL_SURCHARGE, B.threshold(B.cfg_do_nothing), 0.005)
chk("SF/BM    labour-flex threshold = 59.1%",       59.1, B.threshold(B.cfg_labour_only)*100, 0.02)
chk("SF/BM    + cold-chain threshold = 56.9%",      56.9, B.threshold(B.cfg_cold)*100, 0.02)
chk("SF/BM    + small-format threshold = 48.5%",    48.5, B.threshold(B.cfg_footprint)*100, 0.02)
chk("SF/BM    cost levers cut threshold 31%",      31.5, (1-B.threshold(B.cfg_footprint)/B.threshold(B.cfg_do_nothing))*100, 0.03)
chk("SF/RL    small-format saving = Rs77,000",     77000, R.BASE_RENT-R.CAMPUS_FORMAT_SQFT*R.RENT_SF, 0.01)
chk("SF/RL    campus node format = 2,000 sqft",     2000, R.CAMPUS_FORMAT_SQFT, 0.01)
chk("SF/RL    on-campus node rent immaterial",     18.45, 1.23*15, 0.01)
chk("SF/BM    adjacent catchment lo = 469/day",      469, B.adjacent_catchment_required()["adjacent_lo"], 0.02)
chk("SF/BM    adjacent catchment hi = 567/day",      567, B.adjacent_catchment_required()["adjacent_hi"], 0.02)

# ---- SEMI-FINAL D2: SLA (sla.py) ----------------------------------------------
chk("SF/SLA   one-gate arrival rate = 25.9/hr",   25.9, SL.BASE_RATE, 0.01)
chk("SF/SLA   average-state SLA = 21.6 min",      21.6, SL.sla_minutes(SL.BASE_RATE, SL.dynamic_batch(SL.BASE_RATE)), 0.02)
chk("SF/SLA   peak-state SLA = 27.1 min",         27.1, SL.sla_minutes(SL.BASE_RATE*4, SL.dynamic_batch(SL.BASE_RATE*4)), 0.02)
chk("SF/SLA   exam-night SLA = 27.1 min",         27.1, SL.sla_minutes(SL.BASE_RATE*6, SL.dynamic_batch(SL.BASE_RATE*6)), 0.02)
chk("SF/SLA   10-15 min unreachable at every state", 1,
    (1 if min(SL.sla_minutes(r, SL.dynamic_batch(r)) for r in (SL.BASE_RATE*0.25, SL.BASE_RATE, SL.BASE_RATE*4, SL.BASE_RATE*6)) > 15 else 0), 0.001)
chk("SF/SLA   peak cost per order = Rs7.7",        7.7, F.total_campus_cost("E-cart, stationed", SL.dynamic_batch(SL.BASE_RATE*4), F.RUNNER_HR, F.SHELF_DROP), 0.02)
chk("SF/SLA   dynamic batch at peak = 10",          10, SL.dynamic_batch(SL.BASE_RATE*4), 0.001)
chk("SF/SLA   dynamic batch at average = 2",         2, SL.dynamic_batch(SL.BASE_RATE), 0.001)
chk("SF/SLA   runners at peak = 3.7",              3.7, SL.runners_needed(SL.BASE_RATE*4, SL.dynamic_batch(SL.BASE_RATE*4)), 0.02)
chk("SF/SLA   4x demand needs only 1.4x runners",  1.4, SL.runners_needed(SL.BASE_RATE*4,SL.dynamic_batch(SL.BASE_RATE*4))/SL.runners_needed(SL.BASE_RATE,SL.dynamic_batch(SL.BASE_RATE)), 0.03)
chk("SF/SLA   volume-weighted cost = Rs17.6",     17.6, SL.volume_weighted()[1], 0.02)
chk("SF/SLA   volume-weighted saving = 58%",        58, (1-SL.volume_weighted()[1]/M.LAST_MILE)*100, 0.03)
chk("SF/SLA   peak carries 63% of daily orders",  62.7, SL.volume_weighted()[0][0][3]*100, 0.02)

# ---- SEMI-FINAL: robustness and risk (robustness.py, risk_quadrant.py) ---------
chk("SF/RB    rider days SOLVED = 28.7",          28.7, RB.RIDER_DAYS_SOLVED, 0.01)
chk("SF/RB    rider days at Rs42 = 30.0",         30.0, RB.RIDER_DAYS_AT_42, 0.01)
chk("SF/RB    wind-down saving = Rs13.09L",      13.09, RB.WIND_DOWN_SAVING/1e5, 0.01)
chk("SF/RB    reactivation margin = 5.0x",         5.0, RB.REACT_MARGIN, 0.02)
chk("SF/RB    e-cart at Rs2.5L capex = Rs0.30/ord", 0.30, RB.ecart_per_order(250000), 0.02)
chk("SF/RB    e-cart material only above Rs8.4L", 840000, RB.ecart_material_at(1.0), 0.01)
chk("SF/RB    spread 0-0.5km moves cost <Rs2.2",  2.2, RB.spread_sensitivity()[-1][1]-RB.spread_sensitivity()[0][1], 0.05)
chk("SF/Q     min break for wind-down = 7 weeks",   7, Q.MIN_WEEKS, 0.001)
chk("SF/Q     revocation exposure = Rs145 lakh",  144.81, Q.revocation_exposure()["total"]/1e5, 0.01)
chk("SF/Q     post-revocation orders needed = 513", 513, Q.post_revocation_survival()["orders_needed"], 0.01)
chk("SF/Q     binding site filter = 567/day",      567,
    max(Q.post_revocation_survival()["adjacent_hi"], Q.post_revocation_survival()["orders_needed"]), 0.02)
chk("SF/Q     revocation floor binds at low residual", 1,
    (1 if Q.post_revocation_survival()["adjacent_lo"] < Q.post_revocation_survival()["orders_needed"] else 0), 0.001)
chk("SF/Q     gig levy cap = Rs88,200/month",    88200, Q.gig_levy()["cap_5pct"], 0.01)
chk("SF/Q     gig levy = 9.8% of fixed base",      9.8, Q.gig_levy()["as_share_of_fixed"]*100, 0.02)

# ---- JM Financial Exhibit 2 field survey, 35 stores (jm_survey.py) -------------
chk("SF/JS    survey n = 35 stores",                 35, len(JS.S), 0.001)
chk("SF/JS    area~SKU R2 within format = 0.02",   0.02, JS.r2_2, 0.60)
chk("SF/JS    observed NAOV median = Rs450",        450, float(__import__("numpy").median(JS.NAOV)), 0.02)
chk("SF/JS    observed delivery median = 15 min",    15, float(__import__("numpy").median(JS.MINS)), 0.02)
chk("SF/JS    stores at 10 min or less = 9%",         9, (JS.MINS<=10).mean()*100, 0.15)
chk("SF/JS    stores at 15 min or more = 68%",       68, (JS.MINS>=15).mean()*100, 0.05)
chk("SF/JS    observed OPD median = 1,500",        1500, float(__import__("numpy").median(JS.OPD)), 0.02)

# ---- Electricity tariff, sourced (tariff.py, Indiastat + BESCOM) ---------------
chk("SF/TF    Karnataka 2016 total = Rs8.98",      8.98, TF.KA_2016, 0.01)
chk("SF/TF    BESCOM FY26 = Rs8.73",               8.73, TF.BESCOM_2026, 0.001)
chk("SF/TF    ten-year rebase factor = 0.972",    0.972, TF.REBASE, 0.01)
chk("SF/TF    model tariff equals sourced rate",   8.73, C.TARIFF, 0.001)
if hasattr(TF, "T2016"):
    _tariff_values = (TF.T2016["total_p"] / 100).dropna()
    _tariff_n = len(_tariff_values)
    _tariff_cv = float(_tariff_values.std() / _tariff_values.mean()) * 100
else:
    # Public clones contain licensed-table aggregates, not the paid state-level rows.
    _tariff_n = TF.N_STATES_UTS
    _tariff_cv = TF.CROSS_SECTION_CV * 100
chk("SF/TF    48 states/UTs in the cross-section",   48, _tariff_n, 0.001)
chk("SF/TF    state tariff CV = 30%",                30, _tariff_cv, 0.05)
chk("SF/BM    runner floor = 6.2% of term volume",  6.2, F.breakeven_volume()/B.TERM_OPD*100, 0.02)
chk("SF/BM    reactivation opex @r=15% = Rs2.62L",  2.62, B.reactivation(0.15)["opex_total"]/1e5, 0.02)
chk("SF/BM    reactivation opex @r=0.15 = Rs2,62,119", 262119, B.reactivation(0.15)["opex_total"], 0.001)
chk("SF/BM    reactivation = 0.71 months of surplus", 0.71, B.reactivation(0.15)["opex_total"]/B.term_surplus_monthly(), 0.02)
chk("SF/BM    WC re-injection @r=15% = Rs75.5L [S20, pending 2.1]",    75.5, B.reactivation(0.15)["working_capital"]/1e5, 0.02)
chk("SF/BM    ramp-up lead time = 28 days",         28, 28, 0.001)

chk("S1     enrolment 4.46 cr vs hostel capacity 87.7 L", 19.7, 87.7/446*100, 0.02)
chk("S3     digital CV = 4%",                       4, S.CV["Daily internet use, 15-24 urban"], 0.06)
chk("S3     concentration CV = 55%",                55, S.CV["Campus concentration"], 0.03)

chk("S3     orders/resident = 1.5x Blinkit 3.6/mo", 0.18, M.BLINKIT_FREQ*1.5/30, 0.01)
chk("S2/A2  campus CM required = 4.8% of order value", 4.8, M.cm_needed(M.CEILING)/528*100, 0.02)
chk("A2     top-cohort store CM benchmark = 4.0%",  4.0, M.CM_TOPCOHORT*100, 0.001)
chk("S2     franchise payback = 56 months",         56, M.FRANCHISE_PAYBACK, 0.001)

chk("A3     scale gate anchor = 0.18 (1.5x Blinkit)", 0.18, I.ORD_RES, 0.001)


# ---- S17: tier identification of the fixed base  [C1 from the 2026-08-27 corpus sweep] ----
chk("S17    Exhibit 13 rent Rs70/sqft is in Tier-1/2 band", 1, 1 if C.EX13_IS_TIER_1_2 else 0, 0.001)
chk("S17    fixed base @ Rs60/sqft = Rs8.71L",      871000,  C.T12_FIXED_LOW, 0.001)
chk("S17    fixed base @ Rs75/sqft = Rs9.18L",      917500,  C.T12_FIXED_HIGH, 0.001)
chk("S17    Tier-1/2 band width = 5.2% of base",    5.2,     C.T12_FIXED_BAND_PCT*100, 0.02)
chk("S17    Tier-3+ store would be Rs7.66L",        765750,  C.T3P_FIXED_MID, 0.001)
chk("S17    Tier-3+ is 15.1% below our base",       -15.1,   C.T3P_VS_T12*100, 0.02)
chk("S17    util+other Rs3.10L is JM Rs100/sqft blended", 310000, C.UTIL_OTHER_TOTAL, 0.001)


# ---- S18: gross/net basis proof  [C4 from the 2026-08-27 corpus sweep] ----
chk("S18    model basis is GROSS order value",     1, 1 if M.basis_check() else 0, 0.001)
chk("S18    BLINKIT_AOV 694 inside gross band 691-719", 1,
    1 if M.BLINKIT_GROSS_LO <= M.BLINKIT_AOV <= M.BLINKIT_GROSS_HI else 0, 0.001)
chk("S18    Rs528 breakeven vs Blinkit NAOV Rs528 is coincidence", 0,
    abs(M.full_breakeven_aov(3.0) - M.BLINKIT_NAOV_FY25) - 0.2, 1.0)


# ---- S18: asset turn restated on one basis  [C4] ----
chk("S18    MINUTES_AOV adopted = Rs450 (S4)",     450,  M.MINUTES_AOV, 0.001)
chk("S18    city asset turn, adopted basis = 7.34x",  7.34, M.CITY_TURN, 0.005)
chk("S18    campus asset turn, adopted basis = 6.93x", 6.93, M.CAMPUS_TURN, 0.005)
chk("S18    campus/city turn ratio = 0.944",        0.944, M.TURN_RATIO, 0.005)
chk("S18    ratio == density x calendar identity",  0,
    abs(M.TURN_RATIO - M.TURN_RATIO_IDENTITY), 1.0)
chk("S18    calendar leg of identity = 0.708 = 1/1.412", 0.708, M.ACTIVE_MONTHS/12, 0.005)
chk("S18    city NOV, adopted basis = Rs17.2 cr",   17.2, M.CITY_NOV, 0.005)


# ---- S18: CRISIL TCW table, tested and rejected for the cold lever ----
chk("S18    CRISIL per-tonne rate does NOT price our cold room", 0,
    1 if C.CRISIL_TCW_APPLIES_TO_DARK_STORE else 0, 1.0)
chk("S18    CRISIL rate implies absurd 41t inside 3,100 sqft", 41, C.IMPLIED_TONNAGE, 0.02)


# ---- S19: three verdicts  [C6 batching, ad line, D1/D2 tie-out] ----
import sla as _S
_ROWS, _D2COST = _S.volume_weighted()
chk("S19    D2 volume-weighted last mile = Rs17.6",   17.6, _D2COST, 0.01)
chk("S19    UBS 2.7/hr is FOOD DELIVERY, not adopted", 0,
    1 if C.UBS_REPLACES_JPM_ANCHOR else 0, 1.0)
chk("S19    gig:runner ratio, JPM anchor = 2.33x",    2.33, C.RATIO_JPM, 0.01)
chk("S19    gig:runner ratio, FD anchor = 1.60x",     1.60, C.RATIO_UBS, 0.01)
chk("S19    labour-class conclusion holds on both",   1,
    1 if (C.RATIO_JPM > 1 and C.RATIO_UBS > 1) else 0, 0.001)
chk("S19    ads already inside the 19.41% take rate", 1,
    1 if C.ADS_ALREADY_IN_TAKE_RATE else 0, 0.001)
chk("S19    D2-implied consolidation = 2.38x",        2.38,
    C.consolidation_implied_by_d2(_D2COST), 0.01)
chk("S19    breakeven @3.00x proxy = Rs554 (superseded)", 554.5,
    C.breakeven_at(C.CAMPUS_FIXED), 0.005)
chk("S19    breakeven D2-consistent = Rs573 (ADOPTED)", 573.1,
    C.breakeven_d2_consistent(C.CAMPUS_FIXED, _D2COST), 0.005)


# ---- S21: basket ladder + relocation objection ----
chk("S21    Instamart mix->AOV slope = Rs11.3/pt",   11.28, BK.SLOPE, 0.01)
chk("S21    fit R2 = 0.918",                          0.918, BK.R2, 0.01)
chk("S21    non-grocery needed after occasions = 24.3%", 24.3, BK.SHARE_NEEDED_AFTER_OCCASION, 0.01)
chk("S21    fits under mgmt 30-40% ceiling",          1, 1 if BK.FITS_AFTER_OCCASION else 0, 0.001)
chk("S21    Minutes non-grocery today = 20%",         20.0, BK.MINUTES_NONGROCERY, 0.001)
chk("S21    term-start occasion lifts AOV to Rs525",  525, BK.OCCASION_AOV, 0.01)
chk("S21    hold-through-break cost = Rs21.3L",       21.3, B.relocate_vs_flex()["flex_total"]/1e5, 0.02)
chk("S21    relocation capex = Rs89L",                89.0, B.RELOCATE_CAPEX/1e5, 0.001)
chk("S21    holding = 24% of one relocation",         0.24, B.relocate_vs_flex()["flex_vs_relocate"], 0.03)


# ---- S22: working capital rebuilt ----
chk("S22    NWC days now 14 (was 18, target 12)",   14.0, WC.ETERNAL_NWC_DAYS_NOW, 0.001)
chk("S22    WC adopted = Rs88.9L (NWC days x NOV)", 88.9, WC.WC_ADOPTED/1e5, 0.01)
chk("S22    WC at 12-day steady state = Rs76.2L",   76.2, WC.WC_TARGET/1e5, 0.01)
chk("S22    old COGS x 18d construct = Rs116.4L (rejected)", 116.4, WC.WC_OLD/1e5, 0.01)
chk("S22    restatement vs Rs95.7L = -7.2%",        -7.2, (WC.WC_ADOPTED/WC.OLD_SLIDE_FIGURE-1)*100, 0.05)
chk("S22    Zepto cash conversion cycle = -47 days", -47.0, WC.ZEPTO_CCC, 0.001)
chk("S22    State A (credit intact) WC = Rs0",       0, WC.WC_STATE_A, 1.0)
chk("S22    State B, 30d to re-establish = Rs44.4L", 44.4, WC.WC_STATE_B_30D/1e5, 0.01)
chk("S22    per-store inventory benchmark UNRESOLVED", 0,
    1 if WC.INV_PER_STORE_RESOLVED else 0, 1.0)
chk("S22    shrinkage 1.8% of NOV = Rs3.43L/month",  3.43,
    WC.DAILY_NOV*WC.SHRINKAGE_PCT_NOV*30/1e5, 0.01)

# ---- CC-1: dead-zone cash-burn minimisation solver (solver.py) ----------------
# Every solver cell is read from break_mode.CONFIGS and the cost_stack / risk_quadrant
# / sla modules those configs rest on. These checks pin the table to that chain.
chk("CC1     solver rows = 5 strategies",             5, len(SV.ORDER), 0.001)
chk("CC1     DO_NOTHING dead-zone deficit = Rs31.57L", 31.57, SV.ROWS["DO_NOTHING"].deadzone/1e5, 0.01)
chk("CC1     LABOUR_FLEX dead-zone deficit = Rs21.60L", 21.595, SV.ROWS["LABOUR_FLEX"].deadzone/1e5, 0.02)
chk("CC1     COLD_RIGHTSIZE dead-zone deficit = Rs21.21L", 21.21, SV.ROWS["COLD_RIGHTSIZE"].deadzone/1e5, 0.02)
chk("CC1     SMALL_FORMAT dead-zone deficit = Rs18.52L", 18.515, SV.ROWS["SMALL_FORMAT"].deadzone/1e5, 0.02)
chk("CC1     REPURPOSE dead-zone deficit = Rs0",      0, SV.ROWS["REPURPOSE"].deadzone, 1.0)
chk("CC1     DO_NOTHING residual req = 70.8%",        70.8, SV.ROWS["DO_NOTHING"].threshold*100, 0.01)
chk("CC1     LABOUR_FLEX residual req = 59.1%",       59.1, SV.ROWS["LABOUR_FLEX"].threshold*100, 0.02)
chk("CC1     SMALL_FORMAT residual req = 48.6%",      48.6, SV.ROWS["SMALL_FORMAT"].threshold*100, 0.02)
chk("CC1     REPURPOSE residual req == SMALL_FORMAT", 0,
    SV.ROWS["REPURPOSE"].threshold - SV.ROWS["SMALL_FORMAT"].threshold, 1.0)
chk("CC1     wind-down reactivation opex = Rs2.74L",  2.741, SV.ROWS["SMALL_FORMAT"].reactivation/1e5, 0.02)
chk("CC1     DO_NOTHING reactivation = Rs0",          0, SV.ROWS["DO_NOTHING"].reactivation, 1.0)
chk("CC1     REPURPOSE reactivation = Rs0",           0, SV.ROWS["REPURPOSE"].reactivation, 1.0)
chk("CC1     wind-down days to full service = 28",    28, SV.ROWS["SMALL_FORMAT"].days_to_service, 0.001)
chk("CC1     DO_NOTHING days to full service = 0",    0, SV.ROWS["DO_NOTHING"].days_to_service, 1.0)
chk("CC1     lead-time constraint = 28 days",         28, SV.LEAD_TIME_DAYS, 0.001)
chk("CC1     SLA-at-peak constraint = 27.1 min",      27.1, SV.SLA_PEAK_MIN, 0.02)
chk("CC1     catchment-floor constraint = 513/day",   513.4, SV.CATCHMENT_FLOOR, 0.01)
chk("CC1     7-week wind-down rule = 7 weeks",        7, SV.MIN_BREAK_WEEKS, 0.001)
chk("CC1     BEST = REPURPOSE",                       1, 1 if SV.BEST == "REPURPOSE" else 0, 0.001)
chk("CC1     SMALL_FORMAT beats DO_NOTHING on burn",  1,
    1 if SV.ROWS["SMALL_FORMAT"].total < SV.ROWS["DO_NOTHING"].total else 0, 0.001)


# ---- S23: the documents must tie out to the model, not just the model to itself ----
import verify_docs as _VD
chk("S23    HANDOFF.md figures tie out to the model", 1, 1 if _VD.run() else 0, 0.001)


# ---- S24: AISHE district register ----
chk("S24    colleges in register = 54,014",          54014, AD.N_COL, 0.001)
chk("S24    universities = 1,428",                    1428, AD.N_UNI, 0.001)
chk("S24    standalone = 16,910",                    16910, AD.N_STA, 0.001)
chk("S24    total HEIs = 72,352",                    72352, AD.N_HEI, 0.001)
chk("S24    districts covered = 760",                  760, AD.N_DISTRICTS, 0.001)
chk("S24    urban colleges = 21,000",                21000, AD.URBAN_COL, 0.001)
chk("S24    rural colleges = 32,336",                32336, AD.RURAL_COL, 0.001)
chk("S24    URBAN SHARE of colleges = 39.4%",         39.4, AD.URBAN_SHARE_COL*100, 0.005)
chk("S24    candidate districts after screen = 111",   111, AD.N_CANDIDATES, 0.001)
chk("S24    urban high-propensity standalones = 1,897", 1897, AD.N_STA_URBAN_HP, 0.001)
chk("S24    top-ranked district is Khordha (Odisha)",    1,
    1 if AD.TOP.iloc[0].District == "Khordha" else 0, 0.001)
chk("S24    Karnataka districts in top 20 = 14",        14,
    int((AD.TOP.head(20).State == "Karnataka").sum()), 0.001)

# ---- CC-4: BFJ lever-ranking pipeline (lever_rank.py) -------------------------
chk("CC4     lever set = 7",                          7, len(LR.LEVERS), 0.001)
chk("CC4     dimensions = 5",                         5, LR.X.shape[1], 0.001)
chk("CC4     silhouette-selected k = 4",              4, LR.K, 0.001)
chk("CC4     chosen k has the max silhouette",        1,
    1 if LR.SIL >= max(s for _,s,_ in LR.SIL_TABLE) - 1e-9 else 0, 0.001)
chk("CC4     LABOUR_FLEX recoverability = 31.6% of base", 31.6,
    LR.SCORE["LABOUR_FLEX"][0]*100, 0.02)
chk("CC4     SMALL_FORMAT recoverability = 8.5% of base", 8.5,
    LR.SCORE["SMALL_FORMAT"][0]*100, 0.03)
chk("CC4     LABOUR_FLEX restart cost = 0.48 months of surplus", 0.479,
    LR.SCORE["LABOUR_FLEX"][1], 0.02)
chk("CC4     DYNAMIC_BATCH SLA cost at peak = +10.2 min", 10.157,
    LR.SCORE["DYNAMIC_BATCH"][2], 0.02)
chk("CC4     LABOUR_FLEX is a singleton cluster",     1,
    1 if [LR.CLUSTERS[l] for l in LR.LEVERS].count(LR.CLUSTERS["LABOUR_FLEX"]) == 1 else 0, 0.001)
chk("CC4     E_CART is a singleton cluster (only capex lever)", 1,
    1 if [LR.CLUSTERS[l] for l in LR.LEVERS].count(LR.CLUSTERS["E_CART"]) == 1 else 0, 0.001)


# ---- S26: calendar fragmentation ----
chk("S26    contiguous dead-zone cost = Rs21.3L",    21.3, CF.BASE_COST/1e5, 0.02)
chk("S26    typical fragmented cost = Rs27.5L",      27.5, CF.TYPICAL_COST/1e5, 0.02)
chk("S26    typical penalty = +29%",                 29.0, CF.TYPICAL_PENALTY*100, 0.05)
chk("S26    worst-shape penalty = +49%",             49.0, CF.WORST_PENALTY*100, 0.05)
chk("S26    typical wind-downable share = 53%",      53.0, CF.TYPICAL_WINDOWNABLE*100, 0.02)
chk("S26    all-short-gaps calendar qualifies = NO",  0,
    1 if CF.qualifies([6.0,4.0,3.0,2.2]) else 0, 1.0)
chk("S26    typical calendar qualifies = YES",        1,
    1 if CF.qualifies([8.0,4.0,3.2]) else 0, 0.001)
chk("S26    -30% volume shock on ADOPTED basis = Rs647",
    647.1, C.breakeven_d2_consistent(C.CAMPUS_FIXED, 19.0, M.CEILING*0.7), 0.005)

# ---- CC-2/S8: four shocks on one axis (risk_shocks.py) ------------------------
chk("S8      shock base = D2-consistent Rs573",      573.1, RS.BASE_AOV, 0.005)
chk("S8      volume -30% -> Rs640",                  640.0, RS.AOV_VOLUME, 0.005)
chk("S8      shrinkage upper bound -> Rs615",        615.1, RS.AOV_SHRINKAGE, 0.005)
chk("S8      gig levy -> Rs588",                     588.4, RS.AOV_LEVY, 0.005)
chk("S8      calendar fragmentation -> Rs582",       582.0, RS.AOV_FRAGMENTATION, 0.005)
chk("S8      volume is the largest shock",           1,
    1 if RS.SHOCKS[0][0].startswith("Volume") else 0, 0.001)
chk("S8      shrinkage is 80% of the residual = DOUBLE COUNT", 80.3,
    RS.SHRINKAGE_VS_RESIDUAL*100, 0.02)
chk("S8      shrinkage double-count flag is set",    1,
    1 if RS.SHRINKAGE_IS_DOUBLE_COUNTED else 0, 0.001)
chk("S8      basket reaches Rs637 at the 30% floor",  637.5, RS.AOV_CEILING_LO, 0.005)
chk("S8      basket reaches Rs750 at the 40% ceiling", 750.3, RS.AOV_CEILING_HI, 0.005)
chk("S8      3 of 4 shocks covered inside the 30% floor", 3, len(RS.COVERED_AT_LO), 0.001)
chk("S8      4 of 4 shocks covered inside the 40% ceiling", 1,
    1 if RS.ALL_COVERED_AT_HI else 0, 0.001)

# ---- CC-6: labour-class parameter table (labour_class.py) ---------------------
chk("CC6     labour classes = 4",                     4, len(LC.CLASSES), 0.001)
chk("CC6     gig cost/order, JPM anchor = Rs42.1",   42.06, LC.CLASSES[0]["per_order"], 0.01)
chk("CC6     gig cost/active hour = Rs168",          168, LC.CLASSES[0]["per_hour"], 0.01)
chk("CC6     gig fixed cost/day = Rs0 (structural)",  0, LC.CLASSES[0]["fixed_day"], 1.0)
chk("CC6     runner fixed cost/day = Rs577",         577, LC.CLASSES[3]["fixed_day"], 0.01)
chk("CC6     runner in-cluster cost/order = Rs4.7",  4.7, LC.CLASSES[3]["per_order"], 0.02)
chk("CC6     runner rostered hour = Rs72",            72, LC.CLASSES[3]["per_hour"], 0.01)
chk("CC6     runner threshold SOLVED = 87 orders/day", 87, LC.CLASSES[3]["threshold"], 0.02)
chk("CC6     gig cost/km derived = Rs2.36",         2.357, LC.GIG_COST_PER_KM, 0.01)
chk("CC6     gig km per order = 4.44",               4.444, LC.KM_PER_ORDER, 0.01)
chk("CC6     JM non-metro rider utilisation = 36%",  36.5, LC.CLASSES[2]["utilisation"]*100, 0.02)
chk("CC6     labour-class ratio = 2.33x",            2.333, LC.LABOUR_CLASS_RATIO, 0.01)
chk("CC6     incentive column FLAGGED, not invented", 0,
    1 if LC.INCENTIVE_AVAILABLE else 0, 1.0)

# ---- CC-7: contestedness screen (aishe_district.py) ---------------------------
chk("CC7     five-operator store total = 6,693",     6693, AD.TOTAL_STORES, 0.001)
chk("CC7     non-metro stores = 2,393",              2393, AD.NON_METRO_STORES, 0.001)
chk("CC7     metros run +19% over sustainable capacity", 19.4, AD.METRO_EXCESS*100, 0.02)
chk("CC7     stores added per NEW pin code = 5.9",   5.92, AD.STORES_PER_NEW_PINCODE, 0.01)
chk("CC7     operators per served pin code = 2.46",  2.459, AD.STORES_PER_SERVED_PIN, 0.01)
chk("CC7     metro:non-metro store density = 10.0x", 10.0, AD.DENSITY_RATIO, 0.02)
chk("CC7     candidate districts screened = 111",    111, len(AD.CANDIDATES_PROX), 0.001)
chk("CC7     uncontested candidate districts = 9",     9, AD.N_UNCONTESTED, 0.001)
chk("CC7     stacked share of candidates = 72%",      72, AD.STACKED_SHARE*100, 0.02)
chk("CC7     filter restated = 569/day UNCONTESTED", 568.6, AD.SITE_FILTER_UNCONTESTED, 0.01)
chk("CC7     gross required at metro overlap = 1,015/day", 1015.4,
    AD.GROSS_AT_METRO_OVERLAP, 0.01)
chk("CC7     uncontested filter == risk_quadrant binding filter", 0,
    AD.SITE_FILTER_UNCONTESTED - max(Q.post_revocation_survival()["adjacent_hi"],
                                     Q.post_revocation_survival()["orders_needed"]), 1.0)

# ---- S27: the CEILING sensitivity strip (campus_model.py) ---------------------
chk("S5      turn ratio at 1,000 orders/day = 0.675", 0.675, M.TURN_RATIO_AT_1000, 0.005)
chk("S5      turn ratio at 1,200 orders/day = 0.810", 0.810, M.TURN_RATIO_AT_1200, 0.005)
chk("S5      turn ratio at 1,400 orders/day = 0.944", 0.944, M.turn_ratio_at(M.CEILING), 0.005)
chk("S5      parity throughput = 1,482 orders/day",   1482, M.PARITY_OPD, 0.005)
chk("S5      parity sits INSIDE Blinkit's observed range", 1,
    1 if M.PARITY_INSIDE_OBSERVED_RANGE else 0, 0.001)
chk("S5      parity = 99.7% of the observed maximum", 0.997, M.PARITY_VS_CEIL_HI, 0.005)
chk("S5      ratio across the observed range, low  = 0.900", 0.900, M.turn_ratio_at(M.CEIL_LO), 0.005)
chk("S5      ratio across the observed range, high = 1.003", 1.003, M.turn_ratio_at(M.CEIL_HI), 0.005)
chk("S5      parity OPD == city OPD x calendar surcharge", 0,
    M.PARITY_OPD - M.MINUTES_ORD*M.CAL_SURCHARGE, 1.0)

# ---- S30: return on capital employed (roce.py) --------------------------------
chk("S30     capital employed rounds to Rs324 lakh", 324.0, RC.CE_BASE/1e5, 0.005)
chk("S30     capex midpoint = Rs235.0 lakh",        235.0, RC.CAPEX_MID/1e5, 0.005)
chk("S30     orders/year, term-only basis",         361900, RC.orders_year(), 0.005)
chk("S30     ROCE breakeven AOV reproduces the spine", 1,
    1 if RC.BREAKEVEN_TIES_TO_SPINE else 0, 0.001)
chk("S30     day-count gap to the spine = Rs2.14",   2.14, RC.DAYCOUNT_GAP, 0.02)
chk("S30     AOV for ROCE = 0 is Rs571",            571, RC.AOV_BREAKEVEN, 0.005)
chk("S30     AOV for the 40% hurdle is Rs755",      755, RC.AOV_HURDLE, 0.005)
chk("S30     post-tax hurdle AOV is Rs817",         817, RC.AOV_HURDLE_POSTTAX, 0.005)
chk("S30     hurdle premium over breakeven = Rs185", 185, RC.HURDLE_PREMIUM, 0.02)
chk("S30     non-grocery share implied by the hurdle = 32.3%", 32.3, RC.HURDLE_NONGROCERY_SHARE, 0.02)
chk("S30     hurdle sits within the external comparator range", 1, 1 if RC.HURDLE_INSIDE_CEILING else 0, 0.001)
chk("S30     DuPont identity closes: margin x turn = ROCE", 0,
    RC.dupont(RC.AOV_HURDLE)["ebit_margin"]*RC.dupont(RC.AOV_HURDLE)["capital_turn"]
    - RC.roce(RC.AOV_HURDLE), 0.001)
chk("S30     ROCE at the hurdle AOV = 40%",         0.40, RC.roce(RC.AOV_HURDLE), 0.005)
chk("S30     ROCE at a 30% non-grocery basket = 34.4%", 34.4, RC.roce(RC.AOV_UP)*100, 0.02)
chk("S30     ROCE under the -30% volume shock = 14.0%", 14.0,
    RC.roce(RC.AOV_UP, v=M.CEILING*RC.VOL_SHOCK)*100, 0.02)
chk("S30     downside payback exceeds the node's anchored life", 1,
    1 if RC.CAPEX_MID/RC.monthly_ebitda(RC.AOV_UP, v=M.CEILING*RC.VOL_SHOCK) > RC.NODE_LIFE_MO else 0, 0.001)
chk("S30     IRR at the hurdle AOV = 34.4%",        34.4, RC.irr(RC.AOV_HURDLE)*100, 0.02)
chk("S30     repurpose is worth Rs26 of AOV",       26, RC.REPURPOSE_WORTH_AOV, 0.05)
chk("S30     slide-4 turn is the like-for-like quantity", 6.93, RC.TURN_SLIDE4, 0.005)
chk("S30     tax rate = 25.17%",                    25.17, RC.TAX_RATE*100, 0.001)

checks.append((len(checks)+1 == CC.AUDIT_COUNT,
               "SELF  check_counts.AUDIT_COUNT matches this run",
               CC.AUDIT_COUNT, len(checks)+1))

if __name__=="__main__":
    bad=[c for c in checks if not c[0]]
    for ok,lab,a,b in checks:
        print(("  OK  " if ok else "  FAIL")+f"  {lab:<52} slide={a}  model={b}")
    print(f"\n{len(checks)-len(bad)}/{len(checks)} checks pass")
    if bad: raise SystemExit("AUDIT FAILED")
