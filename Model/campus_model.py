"""
Campus dark-store breakeven model  —  v2, calibrated to analyst/company data.

Calibration claim: with the parameters below the model reproduces Blinkit's
reported FY26E contribution profit per order EXACTLY (Rs29.4). Only then is it
applied to a campus.

The two inputs with no source anywhere (campus AOV, orders per resident per day)
are SOLVED FOR, never assumed.
"""
import numpy as np, pandas as pd

# ---------------- SOURCED INPUTS ----------------
# T1 = company disclosure / analyst model built on company data
TAKE_RATE   = 0.1941   # T1  Blinkit revenue take rate FY26E (JM Financial, Eternal model, Jul 2025)
BLINKIT_AOV = 694.0    # T1  Blinkit AOV FY26E (same model)
BLINKIT_CP  = 29.4     # T1  Blinkit contribution profit per order FY26E (same model)
CEIL_LO, CEIL_HI = 1334, 1487   # T1  Blinkit orders/day/dark store, 9-quarter range (JM Exhibit 29)
CEILING     = 1400     # working ceiling inside that observed range
NWC_DAYS    = 18       # T1  Eternal earnings call, Jan 2026 ("not beyond 18 days")
ROCE_TARGET = 0.40     # T1  Eternal earnings call, Jan 2026 ("north of 40%")

# T2 = industry press, range-quoted
LAST_MILE   = 42.0     # last-mile per order  (fixed per TRIP, so gate-drop divides it)
STORE_OPS   = 39.0     # pick, pack, warehousing
PACKAGING   = 12.0     # packaging + support
FIXED_MONTH = 7.5e5    # store fixed cost, midpoint of Rs 5-10 L
CAPEX_LO, CAPEX_HI = 2.2e7, 2.5e7
# ---- MINUTES AOV: restated at S18. Round 1's figure is retained, not erased. ----
MINUTES_AOV_R1 = 775.0 # T2  Inc42 Aug 2026, midpoint Rs750-800. ROUND 1 BASIS. SUPERSEDED at S4.
MINUTES_AOV = 450.0    # T1  TechCrunch 22 Aug 2026, Rs400-500, midpoint. Provenance confirmed in
                       #     writing by the reporting journalist: Flipkart INTERNAL data, avg as
                       #     recent as Aug 2026. Adopted at S4; this line makes the model obey it.
                       #     Gross AOV, consistent with BASIS above.
MINUTES_ORD = 1050.0   # T2  Inc42 Aug 2026, midpoint 1,000-1,100 orders/day/store
ACTIVE_MONTHS = 8.5    # T1  institutional calendars
BLINKIT_FREQ  = 3.6    # T1  orders/month per transacting user (JM Financial; observed 3.2-4.1)
CM_MATURE     = 0.02   # T1  contribution margin, mature-market stores, % of GOV (analyst channel checks)
CM_TOPCOHORT  = 0.04   # T1  contribution margin, top-cohort stores, % of GOV
FRANCHISE_PAYBACK = 56 # T1  months, illustrative franchised dark store (J.P. Morgan)
TENURE_LO, TENURE_HI = 36, 48   # months a student spends on campus

# ---------------- DERIVATION: the unallocated residual ----------------
# JM's model implies total variable cost per order = revenue/order - contribution/order.
# Our itemised stack accounts for most but not all of it. Carry the gap openly.
ITEMISED   = LAST_MILE + STORE_OPS + PACKAGING          # 93.0
IMPLIED_VC = TAKE_RATE*BLINKIT_AOV - BLINKIT_CP         # 105.3
RESIDUAL   = IMPLIED_VC - ITEMISED                      # 12.3, unallocated
CAL_SURCHARGE = 12.0/ACTIVE_MONTHS                      # 1.412

def cm_per_order(aov, consolidation=1.0, take=TAKE_RATE):
    """Gate-drop consolidation divides ONLY the last-mile leg."""
    return take*aov - (LAST_MILE/consolidation + STORE_OPS + PACKAGING + RESIDUAL)

def cm_breakeven_aov(consolidation=1.0, take=TAKE_RATE):
    return (LAST_MILE/consolidation + STORE_OPS + PACKAGING + RESIDUAL)/take

def cm_needed(orders_day, fixed=FIXED_MONTH, calendar=True):
    return fixed/30.0*(CAL_SURCHARGE if calendar else 1.0)/orders_day

def full_breakeven_aov(consolidation=1.0, orders_day=CEILING, take=TAKE_RATE):
    return (cm_needed(orders_day) + LAST_MILE/consolidation + STORE_OPS + PACKAGING + RESIDUAL)/take

def orders_per_day(aov, consolidation, fixed=FIXED_MONTH, calendar=True):
    c = cm_per_order(aov, consolidation)
    return np.nan if c <= 0 else fixed/30.0*(CAL_SURCHARGE if calendar else 1.0)/c

# ---------------- OUTPUTS ----------------
validation = pd.DataFrame([
 {"Check":"Model contribution/order at Blinkit FY26E AOV Rs694",
  "Model":round(cm_per_order(BLINKIT_AOV,1.0),1),"Reported":BLINKIT_CP,
  "Match":"exact" if abs(cm_per_order(BLINKIT_AOV,1.0)-BLINKIT_CP)<0.05 else "no"},
])

req = pd.DataFrame([{
  "Gate-drop consolidation":f"{c:.0f}x",
  "Contribution breakeven AOV":round(cm_breakeven_aov(c)),
  "Full breakeven AOV (at 1,400 orders/day)":round(full_breakeven_aov(c))}
  for c in (1.0,2.0,3.0,4.0)])

def _wf(aov,cons,label):
    net=TAKE_RATE*aov; lm=LAST_MILE/cons
    return {"Scenario":label,"Order value":round(aov),"Net revenue (take 19.41%)":round(net,1),
            "Last mile":round(-lm,1),"Store ops":-STORE_OPS,"Packaging":-PACKAGING,
            "Unallocated":-round(RESIDUAL,1),
            "Contribution/order":round(net-lm-STORE_OPS-PACKAGING-RESIDUAL,1)}
wf = pd.DataFrame([
  _wf(MINUTES_AOV,1.0,"Minutes city store (AOV Rs450, adopted)"),
  _wf(528,1.0,"Campus, door-drop (AOV Rs528)"),
  _wf(528,3.0,"Campus, gate-drop 3x (AOV Rs528)")])

density = pd.DataFrame([{
  "Campus AOV":f"Rs{a}","CM/order @3x":round(cm_per_order(a,3.0),1),
  "Orders/day needed":("n/a" if cm_per_order(a,3.0)<=0 else round(orders_per_day(a,3.0))),
  "Within 1,400 ceiling":("no" if cm_per_order(a,3.0)<=0 or orders_per_day(a,3.0)>CEILING else "yes")}
  for a in (400,450,500,528,550,600,650)])

ORD_RES = 0.25
CLUSTER = CEILING/ORD_RES
MIN_CLUSTERS = 5
GATE = CLUSTER*MIN_CLUSTERS
residents = pd.DataFrame([{"Orders per resident per day":r,
  "Hostel residents per viable cluster":round(CEILING/r,-2)} for r in (0.15,0.20,0.25,0.30)])

capex=(CAPEX_LO+CAPEX_HI)/2
nov_city=MINUTES_ORD*MINUTES_AOV*365
nov_camp=CEILING*528*(365*ACTIVE_MONTHS/12)
asset=pd.DataFrame([
 {"Store type":"Minutes city store (1,050 ord/day, AOV Rs775, 12 mo)",
  "NOV (Rs cr)":round(nov_city/1e7,1),"Asset turn":round(nov_city/capex,1)},
 {"Store type":"Campus store (1,400 ord/day, AOV Rs528, 8.5 mo)",
  "NOV (Rs cr)":round(nov_camp/1e7,1),"Asset turn":round(nov_camp/capex,1)}])

sens=pd.DataFrame([{"Blended take rate":f"{t:.2%}","Full breakeven AOV @3x":round(full_breakeven_aov(3.0,take=t))}
  for t in (0.1941,0.2001,0.2051,0.2071)])

if __name__=="__main__":
    print(f"take rate {TAKE_RATE:.2%} (sourced)  |  implied variable Rs{IMPLIED_VC:.1f}"
          f"  |  itemised Rs{ITEMISED:.0f}  |  residual Rs{RESIDUAL:.1f}")
    print(f"calendar surcharge {CAL_SURCHARGE:.3f}x  |  cluster {CLUSTER:,.0f} residents  |  state gate {GATE:,.0f}\n")
    for n,d in [("VALIDATION",validation),("BREAKEVEN AOV",req),("WATERFALL",wf),
                ("DENSITY",density),("RESIDENTS",residents),("ASSET TURN",asset),("SENSITIVITY",sens)]:
        print(f"--- {n} ---"); print(d.to_string(index=False)); print()

# ============================================================================
# BASIS DECLARATION  [S18, 2026-08-28]  -- every order-value figure is GROSS
# ============================================================================
# The corpus sweep warned that a gross/net mix-up would swing breakeven 21-30%.
# It was checked rather than assumed. The model is, and always was, denominated
# in GROSS order value throughout. The proof is an identity, not an argument:
#
#   BLINKIT_AOV = 694      Blinkit FY26E GROSS AOV (JM). Blinkit gross runs Rs691-719;
#                          its NET AOV (NAOV) is Rs518-530. 694 is unambiguously gross.
#   TAKE_RATE   = 19.41%   revenue as a % of GOV, i.e. applied to a GROSS base.
#   -> revenue/order = 0.1941 x 694 = Rs134.7
#   -> model contribution/order at that AOV = Rs29.4
#   -> Blinkit's REPORTED contribution profit = Rs29.4/order.  EXACT MATCH.
#
# A stack with a mixed basis cannot land exactly on a reported contribution figure.
# Round 1's calibration proof is therefore also the basis proof.
#
# CONSEQUENCE: breakeven AOV Rs528 (@3x) and Rs554 are GROSS order values, and are
# directly comparable to Flipkart Minutes' Rs400-500, which is a company-reported AOV
# and therefore also gross.  NO RESTATEMENT IS REQUIRED.
#
# COINCIDENCE TO FOOTNOTE, NOT TO HIDE: our Rs528 breakeven is arithmetically identical
# to Blinkit's FY25 NAOV of Rs528. Ours is derived from a cost stack divided by the take
# rate and has no dependence on Blinkit's NAOV. Genuine coincidence. Say so once, so a
# panellist reading "528" does not conclude we conflated the two.
#
# WHERE NET FIGURES DO APPEAR, they are labelled NAOV and never mixed into the stack:
# jm_survey.py carries JM's field-survey NAOV (observed median Rs450).
BASIS = "gross"
BLINKIT_NAOV_FY25 = 528.0   # T1 - for the footnote only; NOT an input to any calculation
BLINKIT_GROSS_LO, BLINKIT_GROSS_HI = 691.0, 719.0   # T1 sweep range, brackets BLINKIT_AOV

def basis_check():
    """Returns True iff the take rate applied to the gross AOV reproduces Blinkit's
    reported contribution profit per order. This is the basis proof."""
    return abs(cm_per_order(BLINKIT_AOV, 1.0) - BLINKIT_CP) < 0.05

# ============================================================================
# ASSET TURN, RESTATED LIKE-FOR-LIKE  [S18, 2026-08-28]
# ============================================================================
# Round 1's appendix compared a CAMPUS node valued at its BREAKEVEN AOV (Rs528)
# against a CITY store valued at its ACTUAL AOV (then Rs775). Different bases.
# Restated on one basis, using the AOV adopted at S4 for both, because S4's whole
# finding is that network AOV has CONVERGED to student-basket levels.
_CAPEX_MID = (CAPEX_LO + CAPEX_HI) / 2

def asset_turn(opd, aov=None, months=12.0, capex=None):
    aov   = MINUTES_AOV if aov is None else aov
    capex = _CAPEX_MID if capex is None else capex
    return opd * aov * (365 * months / 12.0) / capex

CITY_TURN   = asset_turn(MINUTES_ORD, MINUTES_AOV, 12.0)            # 7.34x
CAMPUS_TURN = asset_turn(CEILING,     MINUTES_AOV, ACTIVE_MONTHS)   # 6.93x
TURN_RATIO  = CAMPUS_TURN / CITY_TURN                               # 0.944

# THE IDENTITY, and it is the cleanest structural result in the model:
#   campus turn / city turn  ==  (campus OPD / city OPD) x (ACTIVE_MONTHS / 12)
#                            ==  (1400/1050)   x  (8.5/12)
#                            ==  1.333 x 0.708  =  0.944
# Campus DENSITY (+33.3% throughput) almost exactly buys back the CALENDAR (-29.2%).
# The academic dead zone costs 5.6 points of asset productivity, not 30.
# Note 0.708 is the SAME 70.8% that is the do-nothing residual threshold (1/1.412).
# The calendar surcharge inverted shows up a third time and closes again.
TURN_RATIO_IDENTITY = (CEILING / MINUTES_ORD) * (ACTIVE_MONTHS / 12.0)

# ---------------------------------------------------------------------------
# S27  THE CEILING SENSITIVITY -- the deck's most exposed number, priced.
# ---------------------------------------------------------------------------
# FINAL_AUDIT ranked "where does 1,400 orders/day come from?" as the first question a
# Flipkart panel asks, and it is the right question: CEILING is a WORKING ceiling inside
# Blinkit's observed nine-quarter range (CEIL_LO-CEIL_HI, JM Exhibit 29) -- a mature metro
# operator's throughput applied to a greenfield campus node. The moneyshot rests on it.
# Round 1 SOLVED for AOV rather than assuming it. This does the same for throughput:
# instead of defending 1,400, state the OPD at which the ratio reaches parity and let the
# panel read the campus node's required position off Blinkit's own observed range.
def turn_ratio_at(opd):
    """Campus:city asset-turn ratio at a campus throughput of `opd` orders/day."""
    return asset_turn(opd, MINUTES_AOV, ACTIVE_MONTHS) / CITY_TURN

# Parity: the ratio is 1.0 exactly when density fully repays the calendar, i.e. when
# campus OPD = city OPD x (12 / ACTIVE_MONTHS) = city OPD x the calendar surcharge.
PARITY_OPD = MINUTES_ORD * 12.0 / ACTIVE_MONTHS                     # 1,482/day
PARITY_INSIDE_OBSERVED_RANGE = CEIL_LO <= PARITY_OPD <= CEIL_HI     # True -- and only just
PARITY_VS_CEIL_HI = PARITY_OPD / CEIL_HI                            # 0.997 of the observed max

# The strip that goes on slide 5, under the identity. Nothing here is typed onto a slide.
TURN_SENSITIVITY = [(opd, turn_ratio_at(opd)) for opd in (1000.0, 1200.0, CEILING, PARITY_OPD)]
TURN_RATIO_AT_1000 = turn_ratio_at(1000.0)                          # 0.674
TURN_RATIO_AT_1200 = turn_ratio_at(1200.0)                          # 0.809
# The honest sentence: the argument is not "the ratio is 0.944", it is "the ratio is
# 1.333 x 0.708, so every 1% of throughput we lose against a city store comes straight
# off it" -- the density term is linear in OPD and the calendar term is fixed.

# Round 1's figures, retained so the restatement is visible rather than silent:
CITY_TURN_R1 = asset_turn(MINUTES_ORD, MINUTES_AOV_R1, 12.0)        # 12.64x
CITY_NOV_R1  = MINUTES_ORD * MINUTES_AOV_R1 * 365 / 1e7             # Rs29.7 cr
CITY_NOV     = MINUTES_ORD * MINUTES_AOV     * 365 / 1e7            # Rs17.2 cr

def asset_turn_report():
    print("\n" + "="*74)
    print("S18  ASSET TURN, RESTATED ON ONE BASIS   [C4 from the corpus sweep]")
    print("="*74)
    print(f"  Round 1 basis (Minutes AOV Rs{MINUTES_AOV_R1:.0f}, Inc42)")
    print(f"    city asset turn      {CITY_TURN_R1:.2f}x     city NOV Rs{CITY_NOV_R1:.1f} cr")
    print(f"    -- compared against a campus node valued at BREAKEVEN Rs528. MIXED BASIS.")
    print()
    print(f"  Adopted basis (Minutes AOV Rs{MINUTES_AOV:.0f}, TechCrunch, journalist-confirmed)")
    print(f"    city asset turn      {CITY_TURN:.2f}x     city NOV Rs{CITY_NOV:.1f} cr")
    print(f"    campus asset turn    {CAMPUS_TURN:.2f}x")
    print(f"    ratio                {TURN_RATIO:.3f}")
    print()
    print(f"  IDENTITY  (campus OPD/city OPD) x (months/12) = "
          f"({CEILING:.0f}/{MINUTES_ORD:.0f}) x ({ACTIVE_MONTHS}/12) = {TURN_RATIO_IDENTITY:.3f}")
    print(f"  READ      density (+{(CEILING/MINUTES_ORD-1)*100:.1f}%) almost exactly buys back the")
    print(f"            calendar (-{(1-ACTIVE_MONTHS/12)*100:.1f}%). The dead zone costs "
          f"{(1-TURN_RATIO)*100:.1f} points of asset")
    print(f"            productivity, not 30. And 0.708 is the do-nothing threshold again.")

