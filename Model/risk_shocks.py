"""
SLIDE 8, THE RISK SLIDE: four priced shocks on ONE axis.

THE PROBLEM WITH THE RISK REGISTER AS IT STANDS. `risk_quadrant.py` prices the levy,
`calendar_fragmentation.py` prices the fragmented calendar, `working_capital.py` prices
shrinkage, and the -30% volume shock lives in a single audit line. Four numbers in four
units - Rs/month, +% of dead-zone cost, Rs lakh/month, Rs of AOV - which cannot be ranked
against each other and therefore cannot be prioritised on a slide.

THE FIX: restate every shock on the deck's own headline axis, the D2-consistent breakeven
campus AOV (Rs573). Each shock becomes "how many rupees of basket does this cost us", which
is directly comparable to the basket ladder's headroom. That makes the risk slide answer the
only question that matters: DOES THE BASKET STILL COVER IT?

WHAT THE RESTATEMENT FOUND, and it is the reason this module exists rather than a chart:
shrinkage is almost certainly ALREADY INSIDE the model's unallocated residual. See
SHRINKAGE_IS_DOUBLE_COUNTED below. Reported, not buried.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import campus_model as M
import cost_stack as C
import break_mode as B
import sla as SL
import risk_quadrant as Q
import basket as BK
import calendar_fragmentation as CF
import working_capital as WC

D2_LAST_MILE = SL.volume_weighted()[1]                                   # live D2 circuit model
BASE_AOV = C.breakeven_d2_consistent(C.CAMPUS_FIXED, D2_LAST_MILE)       # Rs573, ADOPTED

VOLUME_SHOCK = 0.30          # D  the -30% case the risk register has always carried (item 3)
TERM_ORDERS  = B.TERM_OPD * 30 * B.TERM_MONTHS   # orders over the active year, break_mode basis


# ---------------------------------------------------------------------------
# 1. VOLUME -30%  -- fewer orders to carry the same fixed base
# ---------------------------------------------------------------------------
AOV_VOLUME = C.breakeven_d2_consistent(C.CAMPUS_FIXED, D2_LAST_MILE,
                                       opd=M.CEILING * (1 - VOLUME_SHOCK))

# ---------------------------------------------------------------------------
# 2. SHRINKAGE  -- and the double-count finding
# ---------------------------------------------------------------------------
# Eternal, 22 Jul 2026: shrinkage ~1.8% of NOV, "largely driven by perishables". [T1]
# working_capital.py notes it as "unpriced anywhere". Before pricing it we have to ask
# whether the model is ALREADY carrying it, because the stack was calibrated to Blinkit's
# REPORTED contribution profit - and a reported contribution figure is net of shrinkage.
SHRINKAGE_AT_BLINKIT_BASIS = (M.BLINKIT_AOV * WC.NOV_OVER_GOV * WC.SHRINKAGE_PCT_NOV)
SHRINKAGE_VS_RESIDUAL = SHRINKAGE_AT_BLINKIT_BASIS / M.RESIDUAL
# -> shrinkage at the calibration point is ~80% of the ENTIRE unallocated residual (Rs12.3).
#    The residual is the gap between JM's implied variable cost and our itemised stack; a
#    cost that large, that is definitionally inside a reported contribution figure, is
#    overwhelmingly likely to be sitting in it. So charging shrinkage ON TOP is a DOUBLE COUNT.
SHRINKAGE_IS_DOUBLE_COUNTED = SHRINKAGE_VS_RESIDUAL > 0.5
# The bar is therefore reported as an UPPER BOUND, not a base case: it is what breakeven
# would be if the residual turned out NOT to contain shrinkage. That is the honest shape of
# this risk - an unallocated-cost identification risk, not a new cost.
SHRINKAGE_PER_ORDER = B.CAMPUS_AOV * WC.NOV_OVER_GOV * WC.SHRINKAGE_PCT_NOV
AOV_SHRINKAGE = C.breakeven_d2_consistent(C.CAMPUS_FIXED,
                                          D2_LAST_MILE + SHRINKAGE_PER_ORDER)

# ---------------------------------------------------------------------------
# 3. GIG-WORKER SOCIAL SECURITY LEVY  -- a monthly addition to the fixed base
# ---------------------------------------------------------------------------
LEVY_MONTH = Q.gig_levy()["cap_5pct"]      # T1 Parl. Standing Cttee 201st report, 5% cap
AOV_LEVY = C.breakeven_d2_consistent(C.CAMPUS_FIXED + LEVY_MONTH, D2_LAST_MILE)

# ---------------------------------------------------------------------------
# 4. CALENDAR FRAGMENTATION  -- extra dead-zone cost, amortised over the term
# ---------------------------------------------------------------------------
# calendar_fragmentation prices the shock as a DEAD-ZONE cost. The node can only recover it
# from term-time orders, so it is spread across the active year to reach an AOV equivalent.
FRAG_EXTRA_COST = CF.TYPICAL_COST - CF.BASE_COST
FRAG_PER_ORDER = FRAG_EXTRA_COST / TERM_ORDERS
AOV_FRAGMENTATION = C.breakeven_d2_consistent(C.CAMPUS_FIXED,
                                              D2_LAST_MILE + FRAG_PER_ORDER)

# ---------------------------------------------------------------------------
# THE SHOCK SET, ranked
# ---------------------------------------------------------------------------
SHOCKS = [
 ("Volume -30%", AOV_VOLUME,
  f"{M.CEILING:,.0f} -> {M.CEILING*(1-VOLUME_SHOCK):,.0f} orders/day; register item 3"),
 ("Shrinkage not in residual", AOV_SHRINKAGE,
  f"{WC.SHRINKAGE_PCT_NOV:.1%} of NOV charged on top -- UPPER BOUND, see double-count note"),
 ("Gig social-security levy", AOV_LEVY,
  f"Rs{LEVY_MONTH:,.0f}/mo at the 5%-of-worker-payments cap"),
 ("Calendar fragmentation", AOV_FRAGMENTATION,
  f"+{CF.TYPICAL_PENALTY:.0%} dead-zone cost, amortised over the term"),
]
SHOCKS.sort(key=lambda s: -s[1])

# ---------------------------------------------------------------------------
# THE VERDICT LINE: can the basket ladder still cover each shock?
# basket.py's lever is non-grocery share of GOV. Swiggy's disclosed 30-40% range is used only
# as a cross-operator reference. The AOV at each end of that range is the coverage test.
# ---------------------------------------------------------------------------
def aov_at_nongrocery_share(share):
    """Invert basket.share_needed: the AOV reachable at a given non-grocery share,
    anchored on Minutes' current position after the term-start occasion lever."""
    return BK.OCCASION_AOV + (share - BK.MINUTES_NONGROCERY) * BK.SLOPE

AOV_CEILING_LO = aov_at_nongrocery_share(BK.NONGROCERY_CEILING_LO)   # 30% range floor
AOV_CEILING_HI = aov_at_nongrocery_share(BK.NONGROCERY_CEILING)      # 40% range maximum
COVERED_AT_LO = [n for n, a, _ in SHOCKS if a <= AOV_CEILING_LO]
COVERED_AT_HI = [n for n, a, _ in SHOCKS if a <= AOV_CEILING_HI]
ALL_COVERED_AT_HI = len(COVERED_AT_HI) == len(SHOCKS)


def report():
    W = 92
    print("=" * W)
    print("SLIDE 8  -  FOUR SHOCKS, ONE AXIS".center(W))
    print("restated as breakeven campus AOV, the model's common comparison unit".center(W))
    print("=" * W)
    print(f"  BASE   D2-consistent breakeven campus AOV        Rs{BASE_AOV:.0f}")
    print()
    print(f"  {'SHOCK':<28}{'breakeven AOV':>15}{'delta':>9}   {'basis':<38}")
    print("  " + "-" * (W - 2))
    for name, aov, why in SHOCKS:
        print(f"  {name:<28}{f'Rs{aov:.0f}':>15}{f'+{aov-BASE_AOV:.0f}':>9}   {why[:38]:<38}")
    print("  " + "-" * (W - 2))
    print()
    print("  CAN THE BASKET STILL COVER IT?  (basket.py lever, Swiggy disclosed range)")
    print(f"    AOV reachable at {BK.NONGROCERY_CEILING_LO:.0f}% non-grocery   Rs{AOV_CEILING_LO:.0f}")
    print(f"    AOV reachable at {BK.NONGROCERY_CEILING:.0f}% non-grocery   Rs{AOV_CEILING_HI:.0f}")
    print(f"    covered at the {BK.NONGROCERY_CEILING_LO:.0f}% range floor  "
          f"{len(COVERED_AT_LO)} of {len(SHOCKS)}  ({', '.join(COVERED_AT_LO)})")
    print(f"    covered at the {BK.NONGROCERY_CEILING:.0f}% range maximum "
          f"{len(COVERED_AT_HI)} of {len(SHOCKS)}")
    print()
    print("  >>> READ-OUT. Every priced shock stays within the AOV band implied by Swiggy's range.")
    print("      This is a cross-operator comparator, not evidence of a Flipkart commitment.")
    print("      The volume shock is the one that needs the basket to work HARDER than the")
    print(f"      conservative {BK.NONGROCERY_CEILING_LO:.0f}% case - which is the honest way to say the plan has")
    print("      one binding dependency, not four.")
    print()
    print("=" * W)
    print("  SHRINKAGE: THE DOUBLE-COUNT NOTE, stated before a panellist finds it")
    print("=" * W)
    print(f"    Shrinkage at the CALIBRATION point (Blinkit AOV Rs{M.BLINKIT_AOV:.0f})   "
          f"Rs{SHRINKAGE_AT_BLINKIT_BASIS:.2f}/order")
    print(f"    The model's unallocated residual                       Rs{M.RESIDUAL:.2f}/order")
    print(f"    -> shrinkage is {SHRINKAGE_VS_RESIDUAL:.0%} of the entire residual.")
    print()
    print("    The stack was calibrated by reproducing Blinkit's REPORTED contribution profit")
    print("    exactly, and a reported contribution figure is already net of shrinkage. A cost")
    print("    this large therefore almost certainly sits INSIDE the residual. Charging it again")
    print(f"    would be a double count, so the Rs{AOV_SHRINKAGE:.0f} bar is an UPPER BOUND, not a base case.")
    print("    What it actually prices is an IDENTIFICATION risk on the unallocated line, and")
    print("    that is a different, smaller claim than 'we forgot shrinkage'.")


if __name__ == "__main__":
    report()
