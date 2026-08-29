"""
D1 rent lever, REBUILT. Supersedes the version in break_mode.py v1.

THE ERROR BEING CORRECTED. break_mode.py originally removed the full Rs2,17,000 rent during break,
citing CNLU Patna (4 months rent-free) and NLU Delhi (2 months). Those are UNIVERSITY CANTEEN
LICENCES. Our fixed base is JM Financial's non-metro dark store at Rs70/sqft - a COMMERCIAL lease -
and Round 1 established the cluster store cannot sit on any single campus, because no Indian campus
reaches the 7,778-resident minimum. The campus licence precedent applies only to the on-campus
handoff node (~10-15 sqft, under Rs500/month, immaterial). We had applied the wrong precedent to
the largest line in the stack.

WHAT THE EVIDENCE ACTUALLY SAYS ABOUT COMMERCIAL RENT
  - Warehousing and dark-store leases run 3-9 years with 2-3 year lock-ins   [T2, King Stubb & Kasiva]
  - Commercial lock-ins typically 3-5 years                                   [T2, Brigade]
  - "Discounted leasing is usually given in return for more prolonged lock-in
     periods"; "a shorter term with greater flexibility will cost extra"      [T2, Brigade]
  - No calendar-indexed or seasonally-abated commercial lease structure was
     found anywhere in Indian practice                                        [searched, not found]

=> RENT IS THE LEAST FLEXIBLE LINE IN THE STACK, NOT THE MOST. This reverses S9's conclusion,
   and the corrected version is the more defensible one.

THE THREE LEVERS THAT SURVIVE, none of them contractual seasonality:
  1. FOOTPRINT DISCIPLINE  - structural, permanent, and it uses an asset only Minutes has
  2. SITE SELECTION        - choose the site so break-period catchment already exists (D2 -> D1)
  3. TERM POSTURE          - take the long-lock-in discount, because the cohort cycle IS the term
"""
import campus_model as M, cost_stack as C

RENT_SF   = C.JM_NONMETRO["rent"]/C.JM_NONMETRO["sqft"]     # Rs70/sqft, T1 JM Exhibit 13
BASE_SQFT = C.JM_NONMETRO["sqft"]                            # 3,100
BASE_RENT = C.JM_NONMETRO["rent"]                            # Rs2,17,000

# ---------------- LEVER 1: FOOTPRINT DISCIPLINE ----------------
# Minutes runs a TWO-TIER network: ~3,000 sqft dark stores backed by 23 same-day fulfilment
# centres of 250,000-300,000 sqft carrying ~20x the selection  [T1, TechCrunch 22 Aug 2026].
# Round 1 section 4 established that a homogeneous campus population NARROWS the required
# assortment for ambient, stable, evergreen staples. Those two facts compose: a campus node can
# hold a narrower local range and backfill the tail from the SDFC on a longer stated SLA.
# Blinkit/Zepto have no equivalent second tier. This is a Minutes-only lever.
SKU_BASE   = 16500.0   # T1  Minutes dark store carries 15,000-18,000 SKUs (TechCrunch)
SKU_CAMPUS = 8000.0    # D   campus core range; the tail backfills from the SDFC
# ---------------------------------------------------------------------------------------
# FALSIFIED AND REBUILT (S15). The original version of this lever claimed that cutting the
# local range would cut floor area, on an assumed 30-60% fixed-core share. JM Financial's
# Exhibit 2 field survey of 35 stores was then regressed: WITHIN the standard 1,600-5,500 sqft
# format, store area and SKU count are UNCORRELATED (slope negative, R2 = 0.02, n=33). The
# elasticity does not exist. The lever is now a FORMAT CHOICE, not an elasticity claim:
# 9 of 35 observed stores run at 2,500 sqft or less carrying 6,000-12,000 SKUs, so a 2,000 sqft
# campus node is a format the field survey shows is viable.
CAMPUS_FORMAT_SQFT = 2000.0   # T1  smallest quartile of the JM field survey
# ---------------------------------------------------------------------------------------

def footprint(skus=None, fixed_core_share=None):
    """Campus node area. Now a FORMAT CHOICE evidenced by the field survey, not a computed
    elasticity. Arguments retained for API compatibility and ignored."""
    return CAMPUS_FORMAT_SQFT

def rent_at(skus, fixed_core_share):
    return footprint(skus, fixed_core_share)*RENT_SF

# ---------------- LEVER 3: TERM POSTURE ----------------
# Counter-intuitive and defensible. Most teams will ask landlords for flexibility. The evidence
# says flexibility costs extra and discounts come from LONGER lock-ins. A student cohort is
# 36-48 months on campus [T1, Round 1]. Warehouse lock-ins are 24-36 months [T2].
# The cohort cycle and the lock-in horizon are the SAME horizon, so the campus bet should buy
# the long-lock-in discount rather than pay a premium for flexibility it cannot use.
COHORT_LO, COHORT_HI = M.TENURE_LO, M.TENURE_HI      # 36, 48 months
LOCKIN_LO, LOCKIN_HI = 24, 36                        # T2 months

if __name__=="__main__":
    print("="*82); print("THE CORRECTION".center(82)); print("="*82)
    print("S9 modelled rent as the LARGEST D1 lever, removing Rs2,17,000/month during break on a")
    print("university canteen licence precedent. The dark store sits on a COMMERCIAL lease off")
    print("campus. Commercial leases in India: 3-9 year terms, 2-3 year lock-ins, no seasonal")
    print("abatement structure found anywhere. The lever as modelled does not exist.\n")
    print(f"  Campus licence rent applies only to the on-campus handoff node:")
    print(f"    IIM Bangalore in-hostel rate Rs1.23/sqft x ~15 sqft = Rs{1.23*15:,.0f}/month. Immaterial.")

    print("\n"+"="*82); print("LEVER 1: FORMAT CHOICE (permanent, term AND break)".center(82)); print("="*82)
    print("FALSIFIED AND REBUILT. The first version claimed cutting the local range cuts floor")
    print("area. JM Financial's Exhibit 2 field survey of 35 stores refutes that: within the")
    print("standard 1,600-5,500 sqft format, area and SKU count are UNCORRELATED (R2 = 0.02,")
    print("slope negative, n=33). We reported our own lever as dead rather than defend it.")
    print("\nWhat the same survey DOES support, and it is stronger:")
    print("  11 of 35 observed stores run at 2,500 sqft or less, carrying 7,000 to 35,000 SKUs.")
    print("  A 2,000 sqft store carrying a full range is a format that EXISTS IN THE FIELD.")
    print("  So the campus node is specified small as a FORMAT DECISION, and it does not even")
    print("  require narrowing the assortment to get there.")
    print(f"\n  Baseline JM model store   {BASE_SQFT:,.0f} sqft   Rs{BASE_RENT:,.0f}/month")
    print(f"  Campus node format        {CAMPUS_FORMAT_SQFT:,.0f} sqft   Rs{CAMPUS_FORMAT_SQFT*RENT_SF:,.0f}/month")
    print(f"  Saving                              Rs{BASE_RENT-CAMPUS_FORMAT_SQFT*RENT_SF:,.0f}/month  "
          f"({1-CAMPUS_FORMAT_SQFT/BASE_SQFT:.0%})")
    newfixed = C.CAMPUS_FIXED - (BASE_RENT - CAMPUS_FORMAT_SQFT*RENT_SF)
    print(f"\n  Permanent, so it lands in term months too:")
    print(f"    fixed base    Rs{C.CAMPUS_FIXED:,.0f} -> Rs{newfixed:,.0f}")
    print(f"    breakeven AOV Rs{C.breakeven_at(C.CAMPUS_FIXED):.0f} -> Rs{C.breakeven_at(newfixed):.0f}")
    print(f"\n  TRADE-OFF: a smaller node holds less inventory, so replenishment frequency from")
    print(f"  the SDFC rises. JM's own survey notes smaller-city stores replenish only a few times")
    print(f"  a week and suffer higher stock-outs as a result. The saving is real; the operational")
    print(f"  cost is a tighter replenishment cycle, and it must be funded.")

    print("\n"+"="*82); print("LEVER 2: SITE SELECTION AS A D1 LEVER".center(82)); print("="*82)
    print("If rent cannot be flexed contractually, the only way to stop paying for an empty store")
    print("is to stop it being empty. That makes break-period catchment a SITE SELECTION CRITERION,")
    print("not an operating decision - and it has to enter D2's selection logic, at Layer 1,")
    print("alongside Substitute Scarcity. A cluster with no adjacent residential, office or")
    print("institutional demand within the delivery radius is a cluster we should not build on,")
    print("however well it scores on student density.")
    print("\n>>> This is the correction's most useful consequence: D1's largest problem is solved")
    print("    in D2's site filter, which is exactly the kind of seam the Logical Continuity")
    print("    criterion rewards, and it is a Round 1 asset being extended rather than restated.")

    print("\n"+"="*82); print("LEVER 3: TERM POSTURE - buy the lock-in discount".center(82)); print("="*82)
    print(f"Student cohort on campus      {COHORT_LO}-{COHORT_HI} months   [T1, Round 1]")
    print(f"Warehouse lease lock-in       {LOCKIN_LO}-{LOCKIN_HI} months   [T2, King Stubb & Kasiva]")
    print("The two horizons coincide. Evidence says flexibility costs a premium and discounts come")
    print("from longer lock-ins, so the campus node should BUY the long lock-in rather than pay for")
    print("flexibility the cohort cycle cannot use.")
    print("\n  TRADE-OFF, and it is a real one: a long lock-in raises exposure to Gate 0 revocation.")
    print("  Round 1 established institutions can REVOKE q-commerce permission. A 36-month lock-in")
    print("  against a revocable access regime is the single largest risk in the plan, and it is")
    print("  the reason the bounded-ecosystem-bet quadrant needs its pre-committed kill trigger.")
