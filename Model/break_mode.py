"""
D1: the academic dead zone, priced. Wind-down, break-mode operation, and the restart.

METHOD. The residual demand ratio during break has no source anywhere, so it is NOT assumed.
The break-mode P&L is computed across the full range and the THRESHOLD is reported - the residual
ratio at which each lever configuration turns break-period contribution positive. That threshold
is the trigger a rules-based playbook actually needs, and it is a computed output rather than
an input we had to invent. Same move Round 1 used on campus AOV.

THE TIMING ASYMMETRY, which is the core of D1: wind-down can be gradual because the break is
scheduled years in advance. Ramp-up cannot, because semester-start demand STEPS rather than ramps
(Round 1's term-start durables finding: coolers, blankets, mosquito nets in a 2-3 week window).
Capacity must be complete BEFORE day one. So reactivation lead time is the binding constraint and
the playbook must fire on dates, not on observed volume.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import campus_model as M, cost_stack as C, fleet_mix as F, rent_lever as R
import params as P, sla as SL

TERM_MONTHS, BREAK_MONTHS = M.ACTIVE_MONTHS, 12 - M.ACTIVE_MONTHS      # 8.5 / 3.5
TERM_OPD   = M.CEILING                                                  # 1,400 orders/day
_D2_LM   = SL.volume_weighted()[1]                 # D2 circuit model, NOT re-typed:
                                                   # a hardcoded 19.0 lived here and would
                                                   # have survived the roster-basis change
_D2_CONS = M.LAST_MILE / _D2_LM                    # 2.21x, the consolidation D2 actually delivers
CAMPUS_AOV = C.breakeven_d2_consistent(C.CAMPUS_FIXED, _D2_LM)          # Rs580, D1/D2 tie-out
FIXED      = C.CAMPUS_FIXED                                             # Rs9,02,000/month
RENT, STAFF, UTIL, OTHER = (C.JM_NONMETRO["rent"], C.JM_NONMETRO["labour"],
                            C.UTILITIES_POWER, C.OTHER_FIXED)

def cm_order(aov=None, consolidation=None):
    consolidation = _D2_CONS if consolidation is None else consolidation
    return M.cm_per_order(aov if aov else CAMPUS_AOV, consolidation)

# ---------------- LEVER CONFIGURATIONS ----------------
# Each returns monthly fixed cost during break, given residual demand ratio r.
def cfg_do_nothing(r):
    return RENT + STAFF + UTIL + OTHER

def cfg_labour_only(r):
    """Staff scales with volume, floored at a minimum viable crew. JM scales staff with OPD."""
    staff_n = max(6, round(25*r))          # floor of 6 for 24/7 cover and asset custody
    return RENT + staff_n*15000 + UTIL + OTHER

def cfg_cold(r):
    """+ cold chain right-sized: frozen powered down, chilled consolidated to one zone."""
    cold_saving = (C.COLD_KW*C.COLD_HRS*30*C.TARIFF)*0.60
    return cfg_labour_only(r) - cold_saving

RENT_SAVED = R.BASE_RENT - R.CAMPUS_FORMAT_SQFT*R.RENT_SF   # format choice, evidenced by JM Exhibit 2

def cfg_footprint(r):
    """+ footprint discipline. NOT a break-period lever - it is a PERMANENT reduction in the
    local range and therefore the leased area, which lands in term months too. Included here
    because it lowers the break-period fixed base as a side effect of lowering it always."""
    return cfg_cold(r) - RENT_SAVED

# NOTE ON WHAT IS ABSENT. There is no calendar-indexed rent configuration. The cluster dark store
# sits on a commercial lease (3-9 year term, 2-3 year lock-in, no seasonal abatement structure
# found in Indian practice). The CNLU Patna and NLU Delhi rent-free clauses are university canteen
# licences and apply only to the on-campus handoff node, whose rent is ~Rs18/month. See rent_lever.py.

CONFIGS = [("Do nothing", cfg_do_nothing), ("Labour flex only", cfg_labour_only),
           ("+ cold-chain right-sizing", cfg_cold), ("+ small-format node", cfg_footprint)]

def break_monthly_cm(r, fixed_fn):
    """Monthly contribution after fixed cost during break, at residual ratio r."""
    return TERM_OPD*r*30*cm_order() - fixed_fn(r)

def threshold(fixed_fn, lo=0.0, hi=1.0, tol=1e-4):
    """Residual ratio at which break-mode monthly contribution turns positive."""
    if break_monthly_cm(hi, fixed_fn) < 0: return None
    while hi-lo > tol:
        mid=(lo+hi)/2
        if break_monthly_cm(mid, fixed_fn) < 0: lo=mid
        else: hi=mid
    return hi

# ---------------- BREAK-PERIOD SOLVENCY RUNWAY (Round 1 metric 4) ----------------
def term_surplus_monthly():
    return TERM_OPD*30*cm_order() - FIXED

def runway(fixed_fn, r):
    """Months of break-period deficit the term surplus can fund. Round 1 band: >=1.0x."""
    deficit = -break_monthly_cm(r, fixed_fn)
    if deficit <= 0: return float('inf')
    return (term_surplus_monthly()*TERM_MONTHS)/(deficit*BREAK_MONTHS)

# ---------------- REACTIVATION ----------------
ATTRITION_MO   = 0.20     # T2  dark-store monthly attrition 15-30% (QuickCommerceMap 2026)
HIRE_COST      = 8000.0   # A   recruit + onboard + train one dark-store associate. NO SOURCE.
COLD_PULLDOWN  = 1.5      # A   days of full cold-chain power to bring zones back to temperature
FSSAI_REVERIFY = 15000.0  # A   re-verification, pest control, deep clean before restock
RIDER_REACQ    = 1200.0   # A   incentive to re-attract one gig rider to the zone after 3.5 months

def reactivation(r, fixed_fn=cfg_footprint):
    skeleton = max(6, round(25*r))
    to_rehire = 25 - skeleton*( (1-ATTRITION_MO)**BREAK_MONTHS )
    rehire = max(0, to_rehire)*HIRE_COST
    cold = C.COLD_KW*24*COLD_PULLDOWN*C.TARIFF + FSSAI_REVERIFY
    # Rider supply: fleet sized on term volume. JPM: 21 orders/rider/day.
    riders = TERM_OPD/21.0
    rider = riders*(1-r)*RIDER_REACQ
    # Working capital: released on drawdown, re-injected at restart. ADOPTED CONSTRUCT ONLY.
    # NWC days are NET and stated on NOV (params.NWC_DAYS = 14), so this scales the adopted
    # figure by the share of volume that actually stood down. The COGS/day x 18-day construct
    # that lived here gave Rs100.16 lakh against Rs76.46 lakh at r=0.15 - a Rs23.7 lakh error,
    # in a package whose own working_capital.py calls that construct "wrong twice over". Both
    # passed audit because neither was ever checked against the other. See audit.recon().
    import working_capital as WC          # lazy: working_capital imports this module
    daily_gov = TERM_OPD*CAMPUS_AOV
    wc = WC.reactivation_wc({'A':'A','B30':'B','B':'B'}[P.RESTART_CREDIT_STATE],
                            days_credit=30 if P.RESTART_CREDIT_STATE=='B30' else None)*(1-r)
    return {"rehire":rehire, "cold":cold, "rider":rider, "opex_total":rehire+cold+rider,
            "working_capital":wc, "to_rehire":to_rehire, "riders":riders}

if __name__=="__main__":
    print("="*86); print("THE HOLE, SIZED".center(86)); print("="*86)
    print(f"Term months {TERM_MONTHS}  |  break months {BREAK_MONTHS}  |  calendar surcharge {M.CAL_SURCHARGE:.3f}x")
    print(f"Term volume {TERM_OPD:,} orders/day  |  campus AOV Rs{CAMPUS_AOV:.0f}  |  CM/order Rs{cm_order():.1f}")
    print(f"Fixed base Rs{FIXED:,.0f}/month  |  term surplus Rs{term_surplus_monthly():,.0f}/month")
    print(f"\nUnmitigated break-period deficit: Rs{-break_monthly_cm(0,cfg_do_nothing):,.0f}/month "
          f"x {BREAK_MONTHS} months = Rs{-break_monthly_cm(0,cfg_do_nothing)*BREAK_MONTHS/1e5:,.1f} lakh")

    print("\n"+"="*86); print("RESIDUAL-DEMAND THRESHOLD BY LEVER CONFIGURATION".center(86)); print("="*86)
    print(f"{'Configuration':<30}{'break fixed/mo':>16}{'threshold r':>14}{'orders/day':>13}{'runway @r=15%':>15}")
    print("-"*86)
    for name, fn in CONFIGS:
        t = threshold(fn)
        rw = runway(fn, 0.15)
        print(f"{name:<30}{fn(0.15):>16,.0f}{(f'{t:.1%}' if t else 'never'):>14}"
              f"{(f'{t*TERM_OPD:,.0f}' if t else '--'):>13}"
              f"{('inf' if rw==float('inf') else f'{rw:.2f}x'):>15}")
    print("-"*86)
    print("threshold r = residual demand, as a share of term volume, at which break-mode")
    print("contribution turns positive. Round 1 band on Break-Period Solvency Runway is >=1.0x.")

    print("\n"+"="*86); print("BREAK-MODE FLEET".center(86)); print("="*86)
    floor = F.breakeven_volume()
    print(f"Employed in-cluster runner breakeven volume  {floor:.0f} orders/day  (from fleet_mix.py)")
    print(f"As a share of term volume                    {floor/TERM_OPD:.1%}")
    print(f"\n{'residual r':>12}{'orders/day':>13}{'runner viable':>16}{'fleet decision':>34}")
    for r in (0.05,0.062,0.10,0.15,0.25,0.40):
        od = r*TERM_OPD
        viable = od >= floor
        dec = "keep rostered runner" if viable else "release runner, gig riders to door"
        print(f"{r:>11.1%}{od:>13,.0f}{('yes' if viable else 'NO'):>16} {dec:<34}")
    print(f"\n>>> The runner roster and the store BOTH have volume floors, and they are different.")
    print(f"    Runner floor {floor/TERM_OPD:.1%} of term volume; store floor is the threshold above.")
    print(f"    Between them is the band where the node runs but the in-cluster leg reverts to gig.")

    print("\n"+"="*86); print("REACTIVATION - the part everyone slides past".center(86)); print("="*86)
    for r in (0.10, 0.15):
        x = reactivation(r)
        print(f"\nAt residual r={r:.0%}, skeleton crew {max(6,round(25*r))}:")
        print(f"  Rehire {x['to_rehire']:.0f} associates @Rs{HIRE_COST:,.0f}        Rs{x['rehire']:>10,.0f}  [A]")
        print(f"  Cold-chain pull-down + FSSAI re-verify        Rs{x['cold']:>10,.0f}  [A]")
        print(f"  Re-attract {x['riders']*(1-r):.0f} of {x['riders']:.0f} gig riders          Rs{x['rider']:>10,.0f}  [A]")
        print(f"  {'-'*54}")
        print(f"  Reactivation opex                            Rs{x['opex_total']:>10,.0f}")
        print(f"  Working capital re-injection (NWC {P.NWC_DAYS:.0f}d, on NOV) Rs{x['working_capital']:>10,.0f}  [T1]")
        print(f"  Reactivation opex as months of term surplus   {x['opex_total']/term_surplus_monthly():>10.2f}")

    print("\n"+"="*86); print("THE RULES-BASED PLAYBOOK - triggers, lead times, owners".center(86)); print("="*86)
    print("Wind-down can be gradual; ramp-up cannot. Semester-start demand STEPS (term-start durables,")
    print("a 2-3 week window). So every ramp action fires on a DATE from the published academic")
    print("calendar, never on observed volume - by the time volume tells you, you are already late.\n")
    print(f"{'Trigger':<20}{'Action':<46}{'Owner':<20}")
    print("-"*86)
    PLAYBOOK = [
     ("T-21d to break",  "Freeze replenishment; begin inventory drawdown", "Store manager"),
     ("T-14d to break",  "Serve notice on flex crew; confirm skeleton 6",  "Cluster ops lead"),
     ("T-7d to break",   "Consolidate chilled to one zone; frozen down",   "Store manager"),
     ("T-0 break start", "Licence fee suspension takes effect",            "Contracts"),
     ("Break, weekly",   f"Check residual vs {F.breakeven_volume():.0f}/day runner floor",   "Cluster ops lead"),
     ("T-28d to term",   "Open rehire; 4-week lead on 19 associates",      "Cluster ops lead"),
     ("T-14d to term",   "Rider re-acquisition incentives live in zone",   "Fleet"),
     ("T-7d to term",    "Cold chain pull-down; FSSAI re-verification",    "Store manager"),
     ("T-5d to term",    "First-fill from SDFC; WC re-injection",          "Supply chain"),
     ("T-0 term start",  "Full assortment, full roster, durables staged",  "Store manager"),
    ]
    for t,a,o in PLAYBOOK: print(f"{t:<20}{a:<46}{o:<20}")
    print("-"*86)
    print("Ramp-up lead time is 28 days. The break is 3.5 months, so the ramp begins")
    print("inside the final month of the break - the node is never fully idle for its whole break.")

    print("\n>>> The working-capital swing is the point. Drawdown RELEASES cash during break and")
    print(f"    restart RE-INJECTS Rs{reactivation(0.15)['working_capital']/1e5:.0f} lakh - landing exactly when the node has")
    print(f"    {BREAK_MONTHS} months of accumulated deficit behind it. This is a cash-timing problem,")
    print("    not only a cost problem, and no competing team will price it.")

# ============================================================================
# THE DEMAND SIDE - forced into the open by the rent correction
# Cost-side levers take the threshold from 70.8% to 52.3%. They cannot go further, because
# rent will not flex and a skeleton crew has a floor. 52.3% of term volume is far more than
# a residual campus population plausibly supplies. So the demand-side repurpose is not a
# supplementary lever - it is the MAJORITY of the answer, and it must be sized.
# ============================================================================
RESID_CAMPUS_LO, RESID_CAMPUS_HI = 0.08, 0.15   # D  staff, faculty, research scholars,
# non-vacating students. Round 1: national hostel occupancy 56.3%, 44% of built capacity empty
# even in term time, so a residual base exists. Range stated, not a point estimate.

def adjacent_catchment_required(fixed_fn=cfg_footprint):
    t = threshold(fixed_fn)
    return {"threshold":t, "orders_needed":t*TERM_OPD,
            "from_campus_lo":RESID_CAMPUS_LO*TERM_OPD, "from_campus_hi":RESID_CAMPUS_HI*TERM_OPD,
            "adjacent_lo":(t-RESID_CAMPUS_HI)*TERM_OPD, "adjacent_hi":(t-RESID_CAMPUS_LO)*TERM_OPD}

if __name__=="__main__":
    a = adjacent_catchment_required()
    print("\n"+"="*86); print("WHAT THE DEMAND SIDE MUST DELIVER".center(86)); print("="*86)
    print(f"Cost-side levers floor the threshold at        {a['threshold']:.1%} of term volume "
          f"= {a['orders_needed']:,.0f} orders/day")
    print(f"Residual campus population plausibly supplies  {RESID_CAMPUS_LO:.0%}-{RESID_CAMPUS_HI:.0%} "
          f"= {a['from_campus_lo']:,.0f}-{a['from_campus_hi']:,.0f} orders/day")
    print(f"{'':<46}{'-'*24}")
    print(f"ADJACENT CATCHMENT MUST SUPPLY                 {a['adjacent_lo']:,.0f}-{a['adjacent_hi']:,.0f} orders/day")
    print(f"  as a share of a standard store's throughput  "
          f"{a['adjacent_lo']/M.CEILING:.0%}-{a['adjacent_hi']/M.CEILING:.0%}")
    print("\n>>> THE SITE FILTER THIS PRODUCES, and it is the correction's real payoff:")
    print(f"    A campus cluster is only buildable if adjacent NON-STUDENT catchment within the")
    print(f"    delivery radius can carry roughly {a['adjacent_lo']/M.CEILING:.0%}-{a['adjacent_hi']/M.CEILING:.0%} of a standard store's volume.")
    print("    That is a hard, quantified site-selection criterion, it enters D2's Layer 1")
    print("    alongside Substitute Scarcity, and it means D1's largest problem is solved by")
    print("    D2's site filter rather than by an operating lever.")
    print("\n>>> And the honest corollary: a genuinely ISOLATED campus - no adjacent catchment -")
    print("    cannot be underwritten as a standalone node at all. It is a Round 1 quadrant")
    print("    decision (serve from the existing city store, or do not serve), not a D1 problem.")


# ============================================================================
# S21 [2026-08-28]  THE RELOCATION OBJECTION, ANSWERED
# ============================================================================
# THE OBJECTION, and it is the strongest one a Flipkart ops leader can make:
#   "Nobody mothballs a dark store. Whatever shutdown of stores happens is basically
#    because we want to relocate." (Blinkit management)  "Closure rate is very low."
#   Swiggy Q2FY26 cut store ADDITIONS to ~40 from 316 to drive utilisation instead.
#   Blinkit's only closure rule is performance-based: "Fail Fast" -- 600 OPD by month 3,
#   1,000 by month 6, else churned.  [all T1, earnings calls and JM store visits]
#
# THE ANSWER IS NOT A DEFENCE OF MOTHBALLING, BECAUSE WE DO NOT PROPOSE MOTHBALLING.
# Read CONFIGS above: every configuration keeps the node OPEN and serving. The model
# solves for the RESIDUAL DEMAND RATIO r at which each configuration turns positive.
# S1 locked the break-mode default as "repurpose the catchment". The node is re-aimed,
# not switched off. That is why the site filter requires 469-567 orders/day of ADJACENT
# NON-STUDENT catchment: it is the demand the node serves when the students leave.
#
# WHY THE INDUSTRY HAS NO PLAYBOOK FOR THIS, and it is not because the playbook failed:
#   Urban q-commerce demand is SPATIALLY MOBILE and TEMPORALLY CONTINUOUS.
#     -> if a catchment underperforms, the demand still exists somewhere else in the city,
#        so you MOVE THE ASSET TO THE DEMAND. Relocation is the correct answer, and it is
#        the answer the industry has converged on.
#   Campus demand is SPATIALLY FIXED and TEMPORALLY DISCONTINUOUS.
#     -> the demand does not exist anywhere else, and it returns on a date known years in
#        advance. Relocation cannot address it: you would be moving away from a catchment
#        that is coming back.
# The absence of a mothball playbook is evidence that THE CASE HAS NOT ARISEN in Indian
# q-commerce, not evidence that it fails. Say it that way.
#
# THE INDUSTRY THAT HAS FACED EXACTLY THIS CALENDAR IS CAMPUS FOODSERVICE, and it has a
# playbook, documented and consistent across operators: close most units, keep a skeleton
# open, cut hours. [T2, UC Santa Cruz / Oklahoma / Michigan State / UConn summer schedules]
# That is our lever ladder in different words, and it is worth citing as precedent.

RELOCATE_CAPEX = 8_900_000.0   # T1  JM Financial, Swiggy initiation 13 Nov 2024, Ex.87 -
                               #     itemised cost to set up ONE dark store

def relocate_vs_flex(r=0.0):
    """Cost of abandoning the campus node and rebuilding elsewhere, against the cost of
    holding it through the break on the best lever configuration. Relocation is costed at
    ONE rebuild; if the campus is re-entered later it is TWO."""
    best_name, best_fn = CONFIGS[-1]
    flex_cost   = -break_monthly_cm(r, best_fn)*BREAK_MONTHS + reactivation(r)["opex_total"]
    donothing   = -break_monthly_cm(r, cfg_do_nothing)*BREAK_MONTHS
    return {"flex_total": flex_cost, "do_nothing_total": donothing,
            "relocate_once": RELOCATE_CAPEX, "relocate_and_return": 2*RELOCATE_CAPEX,
            "best_config": best_name,
            "flex_vs_relocate": flex_cost/RELOCATE_CAPEX}

def relocation_report(r=0.0):
    d = relocate_vs_flex(r)
    print("\n"+"="*84)
    print("S21  THE RELOCATION OBJECTION, PRICED".center(84))
    print("="*84)
    print(f"  Hold the node through the break on '{d['best_config']}'")
    print(f"    break-period deficit + reactivation opex        Rs{d['flex_total']:>12,.0f}")
    print(f"  Do nothing (no levers) through the break          Rs{d['do_nothing_total']:>12,.0f}")
    print(f"  Relocate: build one replacement dark store        Rs{d['relocate_once']:>12,.0f}")
    print(f"  Relocate AND return next term                     Rs{d['relocate_and_return']:>12,.0f}")
    print()
    print(f"  >>> Holding the node costs {d['flex_vs_relocate']:.0%} of ONE relocation, and the campus")
    print(f"      catchment is not lost. Relocation forfeits a catchment that returns on a")
    print(f"      date known years in advance -- and re-entering costs the capex again.")
    print()
    print(f"  WE DO NOT PROPOSE MOTHBALLING. Every configuration keeps the node open and")
    print(f"  serving; the model solves for the residual demand ratio at which each turns")
    print(f"  positive. The break-mode default locked at S1 is REPURPOSE THE CATCHMENT.")
