"""
Semi-final extension: decomposition of the two constants the semi-final is graded on.
v2 - rebuilt on JM Financial's itemised dark-store P&L found in the Bloomberg pull.

campus_model.py carries FIXED_MONTH = Rs7.5L/month and LAST_MILE = Rs42/order as single
undecomposed blobs. D1 asks how to flex the fixed base; D2 asks to optimise cost per order.
Neither is answerable at that resolution.

WHAT CHANGED IN v2. The first build was bottom-up from trade press. A full-text grep of the
92-document Bloomberg corpus then surfaced JM Financial's Exhibits 12/13 (27 Aug 2025), which
give a complete itemised dark-store P&L, and J.P. Morgan's dark-store channel survey, which
gives rider productivity directly. v1's independently-built rent and labour lines land within
4% of JM's analyst model. That is a calibration proof for the decomposition itself, and it is
reported below rather than quietly replaced.

TIERS:  T1 company disclosure / analyst model built on company data
        T2 trade press or industry reporting, range-quoted
        D  derived from T1/T2 inputs
        A  assumed - no source found, flagged for database pull
"""
import campus_model as M

# ============================================================================
# 0. THE ANALYST BASELINE  -  JM Financial Exhibits 12 & 13, 27 Aug 2025
#    "Deep Dive: Quick Commerce - QC is tailor made to unlock..."  [T1]
#    Same house whose 19.41% take rate anchors Round 1's calibration, so this is
#    internally consistent with the existing model rather than a competing source.
# ============================================================================
JM = {
 # label            sqft   staff  salary   rent/sqft  util+other/sqft  OPD
 "metro":         (3100,  35,    19000,   110,       100,             1600),
 "non_metro":     (3100,  25,    15000,   70,        100,             950),
}
def jm_stack(k):
    sqft, staff, sal, rent_sf, util_sf, opd = JM[k]
    labour, rent, util = staff*sal, sqft*rent_sf, sqft*util_sf
    total = labour + rent + util
    return {"labour":labour, "rent":rent, "util_other":util, "total":total,
            "opd":opd, "cost_per_order":total/30/opd, "sqft":sqft, "staff":staff}
JM_METRO, JM_NONMETRO = jm_stack("metro"), jm_stack("non_metro")
# JM's own stated outputs: ~Rs27/order at 1,600 OPD metro, ~Rs31/order at 950 OPD non-metro.

# ---- v1 bottom-up build, retained as the independent cross-check
V1_STORE_SQFT = 3000.0    # T1  Flipkart Minutes dark store, TechCrunch 22 Aug 2026
V1_RENT       = 3000*70.0 # T2  Rs55-85/sqft (Bengaluru Rs50-75 FE via ThePrint; Delhi Rs74-111)
V1_LABOUR     = 15*18000 + 2*23000 + 1*45000   # T2  QuickCommerceMap wage bands, 18 staff
RECON_RENT    = V1_RENT   / JM_NONMETRO["rent"]   - 1
RECON_LABOUR  = V1_LABOUR / JM_NONMETRO["labour"] - 1


# ============================================================================
# 0b. WHICH TIER IS EXHIBIT 13 ACTUALLY?   [S17, 2026-08-28]
#     The corpus sweep raised a challenge: Exhibit 13 is labelled "non-metro", and
#     "non-metro" in JM's own taxonomy spans BOTH Tier-1/2 and Tier-3+. If Exhibit 13
#     were a Tier-3+ store, the whole ladder would be denominated in the wrong base.
#     JM Exhibit 5 of the SAME report gives the tier bands, so the question is settled
#     from the source rather than argued.  [T1, JM Financial Deep Dive, 27 Aug 2025]
# ============================================================================
JM_EX5_RENT_SF = {          # Rs per sqft per month, dark store
    "metro":     (80, 120),
    "tier_1_2":  (60,  75),
    "tier_3p":   (35,  50),
}
JM_EX5_RENT_MONTH = {       # Rs per store per month, the same exhibit's other cut
    "metro":     (200000, 400000),
    "tier_1_2":  (150000, 200000),
    "tier_3p":   (100000, 150000),
}
JM_EX5_PICKER_SAL = {       # Rs per month, picker/packer
    "metro":     (16000, 20000),
    "tier_1_2":  (12000, 16000),
    "tier_3p":   (12000, 15000),
}
JM_EX5_HEADCOUNT = {        # store staff excluding supervisors
    "metro":     (26, 40),
    "tier_3p":   (21, 28),
}

def _in(v, band): return band[0] <= v <= band[1]

def identify_tier(rent_sf, salary):
    """Return every tier whose Exhibit 5 bands contain BOTH the rent and the salary."""
    return [t for t in JM_EX5_RENT_SF
            if _in(rent_sf, JM_EX5_RENT_SF[t]) and _in(salary, JM_EX5_PICKER_SAL[t])]

# Exhibit 13 inputs, restated: rent Rs70/sqft, picker salary Rs15,000.
EX13_RENT_SF, EX13_SALARY = JM["non_metro"][3], JM["non_metro"][2]
EX13_TIERS = identify_tier(EX13_RENT_SF, EX13_SALARY)
# -> rent Rs70 sits inside Tier-1/2 (60-75) and outside Tier-3+ (35-50).
#    salary Rs15,000 sits inside BOTH Tier-1/2 (12-16k) and Tier-3+ (12-15k, at its ceiling).
#    Rent therefore discriminates and salary does not: EXHIBIT 13 IS A TIER-1/2 STORE.
EX13_IS_TIER_1_2 = (EX13_TIERS == ["tier_1_2"])

# Cross-check on the other Exhibit 5 cut: does Exhibit 13's rent in Rs/month land in band?
_BASE_FIXED = JM_NONMETRO["total"]   # Rs9,02,000 - CAMPUS_FIXED aliases this below
EX13_RENT_MONTH = JM_NONMETRO["rent"]                       # Rs2,17,000
EX13_RENT_MONTH_IN_T12 = _in(EX13_RENT_MONTH, JM_EX5_RENT_MONTH["tier_1_2"])  # 1.5-2.0L -> just above
# Rs2,17,000 sits Rs17,000 ABOVE the Tier-1/2 monthly band ceiling because Exhibit 13's store
# is 3,100 sqft, larger than the footprint Exhibit 5's monthly band implies. Reported, not hidden.

# ---- SENSITIVITY: the fixed base across the full Tier-1/2 rent band ------------
def fixed_at_rent(rent_sf, sqft=None, staff=None, salary=None, util_sf=None):
    sqft   = JM["non_metro"][0] if sqft   is None else sqft
    staff  = JM["non_metro"][1] if staff  is None else staff
    salary = JM["non_metro"][2] if salary is None else salary
    util_sf= JM["non_metro"][4] if util_sf is None else util_sf
    return staff*salary + sqft*rent_sf + sqft*util_sf

T12_FIXED_LOW  = fixed_at_rent(JM_EX5_RENT_SF["tier_1_2"][0])   # Rs60/sqft
T12_FIXED_HIGH = fixed_at_rent(JM_EX5_RENT_SF["tier_1_2"][1])   # Rs75/sqft
T12_FIXED_BAND_PCT = (T12_FIXED_HIGH - T12_FIXED_LOW) / _BASE_FIXED   # width as % of base

# What a Tier-3+ store would have cost, for the sensitivity slide only. NOT our base.
T3P_FIXED_MID = fixed_at_rent(sum(JM_EX5_RENT_SF["tier_3p"])/2,
                              staff=sum(JM_EX5_HEADCOUNT["tier_3p"])//2,
                              salary=sum(JM_EX5_PICKER_SAL["tier_3p"])//2)
T3P_VS_T12 = T3P_FIXED_MID / _BASE_FIXED - 1

# ---- THE SOFT LINE, stated rather than buried --------------------------------
# JM holds "utilities + other" at Rs100/sqft in BOTH the metro and non-metro exhibits.
# It is therefore a blended allocation, not a tier-specific itemisation. Our own split of
# that line into utilities (sourced, tariff.py) and "other fixed" (residual) is OURS.
UTIL_OTHER_TOTAL   = JM_NONMETRO["util_other"]                  # Rs3,10,000
OTHER_FIXED_RESIDUAL_SHARE = None    # set after the utilities figure is computed below


# ============================================================================
# CRISIL TCW COST TABLE  [S18, 2026-08-28]  -- TESTED, AND MOSTLY REJECTED
#   Source: CRISIL Intelligence, "Cold Chain", exhibit "Estimated cost for TCW".
#   This exhibit is an embedded image in the PDF and did not survive text extraction;
#   supplied separately. Transcribed here verbatim.  [T1]
# ============================================================================
CRISIL_TCW = {
    "single_commodity_cold_storage_Rs_per_tonne": (5000, 6000),
    "multipurpose_cold_storage_Rs_per_tonne":     (30000, 40000),
    "temp_controlled_vehicle_Rs_per_unit":        (2_000_000, 3_000_000),  # for 8-10 tonne
    "temp_controlled_vehicle_tonnage":            (8, 10),
}

# ---- THE TEST: does the per-tonne rate price OUR cold room? ------------------
# JM/Swiggy Exhibit 87 itemises a dark-store cold room at Rs1.44mn (Rs14.4 lakh).
# If CRISIL's multipurpose rate applied, that capex would imply:
JM_COLD_ROOM_CAPEX = 1_440_000.0        # T1  JM Financial, Swiggy initiation, 13 Nov 2024, Ex.87
_mp_mid = sum(CRISIL_TCW["multipurpose_cold_storage_Rs_per_tonne"]) / 2
IMPLIED_TONNAGE = JM_COLD_ROOM_CAPEX / _mp_mid          # ~41 tonnes
DARK_STORE_SQFT = JM["non_metro"][0]                     # 3,100 sqft

# 41 tonnes of multi-commodity cold storage inside a 3,100 sqft dark store is not a
# chiller zone, it is a standalone agricultural cold store. CRISIL's per-tonne rates
# price BULK AGRI COLD STORAGE (a building), not an in-store chilled/frozen zone
# (a fitted room). Applying them to our cold lever would be a category error, and it
# is exactly the kind of error a panel finds. REJECTED, and recorded as rejected.
CRISIL_TCW_APPLIES_TO_DARK_STORE = False

# ---- WHAT IS USABLE, AND IT IS NARROW ---------------------------------------
# The temperature-controlled VEHICLE line is a different asset and it does transfer.
# It prices chilled inbound replenishment, which the campus node needs: JM's Trichy
# template (pop. 0.8mn, 21 Mar 2025) replenishes ONCE PER WEEK from a mother warehouse
# 140 km away. A campus cluster node on the same pattern needs chilled line-haul.
TCV_CAPEX_PER_TONNE = (CRISIL_TCW["temp_controlled_vehicle_Rs_per_unit"][0]
                       / CRISIL_TCW["temp_controlled_vehicle_tonnage"][1],
                       CRISIL_TCW["temp_controlled_vehicle_tonnage"][0] and
                       CRISIL_TCW["temp_controlled_vehicle_Rs_per_unit"][1]
                       / CRISIL_TCW["temp_controlled_vehicle_tonnage"][0])
# -> Rs2.0-3.75 lakh per tonne of chilled vehicle capacity.

def crisil_tcw_report():
    lo, hi = CRISIL_TCW["multipurpose_cold_storage_Rs_per_tonne"]
    print("\n" + "="*74)
    print("S18  CRISIL TCW COST TABLE -- TESTED AND MOSTLY REJECTED")
    print("="*74)
    print(f"  CRISIL multipurpose cold storage   Rs{lo:,}-{hi:,} per tonne")
    print(f"  JM dark-store cold room capex      Rs{JM_COLD_ROOM_CAPEX:,.0f}")
    print(f"  -> implied capacity at CRISIL rate {IMPLIED_TONNAGE:.0f} tonnes")
    print(f"  -> inside a {DARK_STORE_SQFT:,.0f} sqft dark store. Physically absurd.")
    print(f"  VERDICT  CRISIL prices BULK AGRI COLD STORAGE (a building). Our cold lever")
    print(f"           is an in-store chilled/frozen ZONE (a fitted room). Different asset")
    print(f"           class. NOT USED for the cold right-size lever. Recorded as examined.")
    print()
    print(f"  USABLE   temperature-controlled VEHICLE, Rs2-3mn for 8-10 tonne")
    print(f"           = Rs{TCV_CAPEX_PER_TONNE[0]:,.0f}-{TCV_CAPEX_PER_TONNE[1]:,.0f} per tonne of chilled capacity.")
    print(f"           Prices chilled INBOUND replenishment, which the campus node needs:")
    print(f"           JM's Trichy template replenishes weekly from 140 km away.")



def tier_report():
    print("\n" + "="*74)
    print("S17  WHICH TIER IS THE FIXED BASE?   [C1 from the corpus sweep]")
    print("="*74)
    print(f"  Exhibit 13 inputs      rent Rs{EX13_RENT_SF}/sqft, picker salary Rs{EX13_SALARY:,}")
    print(f"  Exhibit 5 rent bands   metro Rs80-120 | Tier-1/2 Rs60-75 | Tier-3+ Rs35-50")
    print(f"  Tiers containing both  {EX13_TIERS}")
    print(f"  VERDICT                Exhibit 13 is a TIER-1/2 store, not a Tier-3+ store.")
    print(f"                         Rent discriminates; salary Rs15,000 sits in both bands.")
    print()
    print(f"  Fixed base @ Rs60/sqft   Rs{T12_FIXED_LOW:,.0f}")
    print(f"  Fixed base @ Rs70/sqft   Rs{_BASE_FIXED:,.0f}   <- the model's base case")
    print(f"  Fixed base @ Rs75/sqft   Rs{T12_FIXED_HIGH:,.0f}")
    print(f"  Band width               {T12_FIXED_BAND_PCT*100:.1f}% of base  -> the base is ROBUST within its tier")
    print()
    print(f"  A Tier-3+ store would be Rs{T3P_FIXED_MID:,.0f}  ({T3P_VS_T12*100:+.1f}% vs our base)")
    print(f"                           -- reported for the sensitivity slide; NOT our archetype.")
    print()
    print(f"  SOFT LINE  'utilities + other' Rs{UTIL_OTHER_TOTAL:,.0f} is JM's Rs100/sqft held CONSTANT")
    print(f"             across metro and non-metro. It is a blended allocation, not a tier")
    print(f"             itemisation. Our utilities/other split of it is OURS, and 'other fixed'")
    print(f"             is the least-defensible line in the stack. State it; do not bury it.")

# ============================================================================
# 1. THE CAMPUS CLUSTER STORE  -  JM non-metro structure, campus throughput
#    A campus cluster store sits on the periphery, on non-metro wage and rent levels,
#    but runs at the campus throughput the Round 1 model uses.
# ============================================================================
CAMPUS_FIXED = JM_NONMETRO["total"]          # Rs9,02,000/month
LEGACY_FIXED = M.FIXED_MONTH                 # Rs7,50,000/month, Round 1 T2 band midpoint

def store_cost_per_order(fixed, opd, calendar=True):
    return fixed/30.0*(M.CAL_SURCHARGE if calendar else 1.0)/opd

def breakeven_at(fixed, consolidation=3.0, opd=M.CEILING, take=M.TAKE_RATE):
    """Round 1's full_breakeven_aov, re-expressed so the fixed base is a parameter."""
    return (store_cost_per_order(fixed, opd)
            + M.LAST_MILE/consolidation + M.STORE_OPS + M.PACKAGING + M.RESIDUAL)/take

# ---- FLEXIBILITY CLASSIFICATION  (this is the D1 answer)
# TF truly fixed | SV semi-variable, scales with throughput | CF contract-flexible:
# fixed only because of the term we signed, not because of physics.
#
# JM's stack has only three lines and folds everything non-rent, non-labour into
# "utilities and other". Classifying that whole line as semi-variable would report a
# 100% flexible base, which is an overclaim. It is split here using v1's independent
# power arithmetic, and the split is stated rather than buried.
COLD_KW, COLD_HRS = 3.5, 20.0   # D  ~100 m3 chilled+frozen zone; Alfa Laval load rules give
AMB_KW,  AMB_HRS  = 4.0, 18.0   #    3-4 kW running load for a 120 m3 room (fmax.in worked example)
KWH_MONTH = (COLD_KW*COLD_HRS + AMB_KW*AMB_HRS)*30
TARIFF    = 8.73   # T1/T2 SOURCED, no longer assumed. Two independent routes agree:
                   #  (a) BESCOM LT-3 commercial, Karnataka FY2025-26: Rs8.00 energy + FAC Rs0.31
                   #      + 5% electricity tax = Rs8.73/kWh effective [T2, BESCOM/KERC schedule]
                   #  (b) Indiastat, State/Utility-wise Average Rate of Electricity Supply and
                   #      Duty/Tax {Commercial 30 KW, 4,500 units/month}, 01.04.2016 [T1 govt]:
                   #      Karnataka Rs8.98/kWh total. Ten-year drift is -0.3% CAGR, i.e. Indian
                   #      commercial tariffs are broadly FLAT in nominal terms, so the 2016
                   #      cross-section is usable and the vintage objection is answered, not dodged.
                   #  State dispersion CV = 30% (see tariff.py); Karnataka is conservative by
                   #  +12% against the 48-state median of Rs7.80.
DEMAND_KW = 15.0   # D  sanctioned load implied by the 7.5 kW running draw plus headroom
UTILITIES_POWER = KWH_MONTH*TARIFF + DEMAND_KW*210 + 10000   # + BESCOM demand charge, water/waste/net
OTHER_FIXED     = JM_NONMETRO["util_other"] - UTILITIES_POWER
# OTHER_FIXED carries tech/POS licensing, FSSAI + trade + shops-and-establishments + fire NOC
# amortised, maintenance, security, insurance and allocated central overhead. Truly fixed.

FIXED_STACK = [
 ("Store rent",              JM_NONMETRO["rent"],   "CF",
  "Calendar-indexed licence. Precedent: CNLU Patna 4 months rent-free, NLU Delhi 2 months."),
 ("In-store staff",          JM_NONMETRO["labour"], "SV",
  "25 staff across 3 shifts. Skeleton crew sized on residual demand."),
 ("Utilities and cold chain",UTILITIES_POWER,       "SV",
  "Cold chain is the swing item. One chilled zone, power down frozen."),
 ("Other fixed",             OTHER_FIXED,           "TF",
  "Tech, licences, compliance, maintenance, security, insurance, central. Persists through break."),
]
def fixed_flex_share():
    return sum(v for _,v,c,_ in FIXED_STACK if c in ("CF","SV")) / CAMPUS_FIXED

# ---- On-campus handoff node rent, from real Indian university licence tenders
CAMPUS_LICENCE = {          # Rs/sqft/month  [T1, tender documents]
 "IIM Bangalore night canteen (in-hostel)": 1.23,
 "IIT Kanpur hostel canteen":              14.50,
 "IIT ISM Dhanbad hostel service":         14.30,
 "IIT Kanpur academic-block retail":       31.40,
 "IIT Bombay Cafe-92 retail":              60.00,
 "IIT Jodhpur retail (reserve)":          156.00,
}
COMMERCIAL_RENT_SF = JM_NONMETRO["rent"]/JM_NONMETRO["sqft"]   # Rs70/sqft

# ============================================================================
# 2. LAST-MILE STACK  ->  reconciles to M.LAST_MILE = Rs42/order
# The move that makes D2 answerable: last mile is fixed per TRIP, not per order,
# so it decomposes as TIME x COST-PER-RIDER-HOUR. Vehicle choice optimises travel;
# on a Type A campus travel is not where the time goes.
# ============================================================================
# --- J.P. Morgan dark-store channel survey, 2 May 2022 [T1]
#     18+ dark stores visited, store managers and delivery execs interviewed, Mumbai/Bengaluru
JPM_ORD_DAY     = 21.0     # T1  "delivers 20-22 orders per day"
JPM_ORD_HR      = 4.0      # T1  "on an average does four orders in a hour and most do order batching"
JPM_RIDER_MONTH = 26500.0  # T1  "average monthly income of a delivery executive was Rs26.5K"
JPM_RIDER_FUEL  = 6600.0   # T1  "fuel expenses are Rs6.6K"
JPM_RADIUS_KM   = 5.0      # T1  "dark stores cover a radius between 5-10kms" (Blinkit/Zepto 4-6)

# --- JM Financial delivery-partner channel checks, 27 Aug 2025 [T1]
JM_METRO_DELIV_SHIFT     = 30.0   # T1  "up to 30 deliveries per day in a 12-hour shift"
JM_NONMETRO_DELIV_SHIFT  = 17.5   # T1  "15-20 deliveries in a 12-hour shift"
JM_SHIFT_HRS             = 12.0   # T1
JM_METRO_EARN            = 37500.0  # T1  "monthly earnings ranged between INR 35k and INR 40k"
JM_NONMETRO_EARN         = 20000.0  # T1  "typically below INR 20k per month"
# JM names the cause of the gap explicitly: "high idle time between two orders."

RIDER_DAYS = 30.0          # A   assumed working days; gig, no fixed roster
# Cost per delivery, three independent routes:
ROUTE_JPM      = JPM_RIDER_MONTH   / (JPM_ORD_DAY * RIDER_DAYS)
ROUTE_JM_METRO = JM_METRO_EARN     / (JM_METRO_DELIV_SHIFT * 26)
ROUTE_JM_NONM  = JM_NONMETRO_EARN  / (JM_NONMETRO_DELIV_SHIFT * 26)
# Eternal's disclosed weighted average delivery cost per order = Rs44; Swiggy Rs55 [T1, JM Exhibit 1]
ETERNAL_DELIV, SWIGGY_DELIV = 44.0, 55.0

# --- Rider cost per PRODUCTIVE hour, derived
RIDER_HR_ACTIVE = ROUTE_JPM * JPM_ORD_HR       # cost/order x orders/active hour
UTILISATION     = (JPM_ORD_DAY / JPM_ORD_HR) / 13.0   # active hrs / typical 13-hr shift

# --- Trip geometry
CITY_LEG_MIN    = 8.0      # T1  Blinkit <2 km ride leg in ~8 min (founder, via Parl. panel reporting)
HANDOFF_MIN     = 2.0      # A   doorstep dwell
GATE_MANUAL_MIN = 3.0      # T2  manual gate check-in ~3 min (Mygate Bengaluru pilot, Mar 2024)
GATE_PREAPP_MIN = 0.25     # T2  pre-approved gate check-in <15 sec (same pilot, 1M+ uses)
CAMPUS_KM       = 1.35     # T1  IIM Jammu gate to boys' hostel, 1.2-1.5 km (primary, Abhishek)
CAMPUS_KMPH     = 20.0     # T1  observed intra-campus vehicle speed (primary, Abhishek)
CAMPUS_LEG_MIN  = CAMPUS_KM/CAMPUS_KMPH*60

trip = lambda legs: sum(legs)
STD_TRIP = trip([CITY_LEG_MIN, HANDOFF_MIN, CITY_LEG_MIN])
TRIPS_HR = 60.0/STD_TRIP                       # 3.33 geometric round trips per active hour
BATCH_BASE = JPM_ORD_HR / TRIPS_HR             # D  disclosed 4 orders/hr / 3.33 trips = 1.2x
# The baseline is ALREADY batched at 1.2x. Round 1 treated door-drop as 1x. It is not.

def last_mile(trip_min, batch=None, campus_fee=0.0):
    """Cost per ORDER of the last-mile leg for any geometry and consolidation level."""
    b = BATCH_BASE if batch is None else batch
    return RIDER_HR_ACTIVE / (60.0/trip_min * b) + campus_fee

GEOM = {
 "Standard 2-3 km residential":        [CITY_LEG_MIN, HANDOFF_MIN, CITY_LEG_MIN],
 "Type A campus, door-drop, manual gate": [CITY_LEG_MIN, GATE_MANUAL_MIN, CAMPUS_LEG_MIN,
                                           HANDOFF_MIN, CAMPUS_LEG_MIN, CITY_LEG_MIN],
 "Type A campus, door-drop, pre-approved": [CITY_LEG_MIN, GATE_PREAPP_MIN, CAMPUS_LEG_MIN,
                                            HANDOFF_MIN, CAMPUS_LEG_MIN, CITY_LEG_MIN],
 "Type A campus, gate-drop":           [CITY_LEG_MIN, GATE_PREAPP_MIN, HANDOFF_MIN, CITY_LEG_MIN],
 "Type B urban PG cluster":            [CITY_LEG_MIN*0.5, HANDOFF_MIN+1.5, CITY_LEG_MIN*0.5],
}
DOOR = last_mile(trip(GEOM["Type A campus, door-drop, manual gate"]))

def affordable_fee(batch, benchmark=None):
    bench = benchmark if benchmark is not None else M.LAST_MILE
    return bench - last_mile(trip(GEOM["Type A campus, gate-drop"]), batch)

RUNNER_WAGE, RUNNER_DELIV_D, RUNNER_DAYS = 15000.0, 60.0, 26.0   # T1 JM non-metro salary band
RUNNER_COST_PARCEL = RUNNER_WAGE/(RUNNER_DELIV_D*RUNNER_DAYS)

if __name__=="__main__":
    W=44
    print("="*80); print("CALIBRATION: v1 bottom-up vs JM Financial analyst model".center(80)); print("="*80)
    print(f"{'':<26}{'v1 build':>14}{'JM non-metro':>16}{'gap':>10}")
    print(f"{'Rent':<26}{V1_RENT:>14,.0f}{JM_NONMETRO['rent']:>16,.0f}{RECON_RENT:>10.1%}")
    print(f"{'In-store labour':<26}{V1_LABOUR:>14,.0f}{JM_NONMETRO['labour']:>16,.0f}{RECON_LABOUR:>10.1%}")
    print("  -> both within 4%. The decomposition itself is calibrated before it is used.")

    print("\n"+"="*80); print("FIXED-COST STACK  (campus cluster store, JM non-metro structure)".center(80)); print("="*80)
    for n,v,c,a in FIXED_STACK:
        print(f"{n:<{W}} {v:>10,.0f}  {v/CAMPUS_FIXED:>6.1%}  {c}")
    print("-"*80)
    print(f"{'TOTAL':<{W}} {CAMPUS_FIXED:>10,.0f}")
    print(f"\n>>> Flexible share of the fixed base (CF+SV) = {fixed_flex_share():.1%}")
    print(f">>> Utilities split: power Rs{UTILITIES_POWER:,.0f} ({KWH_MONTH:,.0f} kWh @Rs{TARIFF:.2f} [ASSUMED]), other fixed Rs{OTHER_FIXED:,.0f}")
    print(f">>> JM metro comparator: Rs{JM_METRO['total']:,.0f}/mo, Rs{JM_METRO['cost_per_order']:.0f}/order @1,600 OPD")
    print(f">>> JM non-metro:        Rs{JM_NONMETRO['total']:,.0f}/mo, Rs{JM_NONMETRO['cost_per_order']:.0f}/order @950 OPD")
    print(f">>> Round 1 used        Rs{LEGACY_FIXED:,.0f}/mo  ({LEGACY_FIXED/CAMPUS_FIXED-1:+.1%} vs JM non-metro)")

    print("\n" + "-"*80)
    print("IMPACT OF THE FIXED-BASE RECALIBRATION ON ROUND 1's HEADLINE NUMBER")
    print("-"*80)
    for lbl,f in (("Round 1 (Rs7.50L)",LEGACY_FIXED),("JM non-metro (Rs9.02L)",CAMPUS_FIXED),
                  ("JM metro (Rs13.16L)",JM_METRO["total"])):
        print(f"{lbl:<26} store cost/order Rs{store_cost_per_order(f,M.CEILING):>5.1f}"
              f"   full breakeven AOV @3x  Rs{breakeven_at(f):>5.0f}")

    print("\n" + "-"*80)
    print("ON-CAMPUS NODE RENT vs COMMERCIAL  (Rs/sqft/month)")
    print("-"*80)
    for k,v in CAMPUS_LICENCE.items():
        print(f"{k:<{W}} {v:>7.2f}   {v/COMMERCIAL_RENT_SF-1:>+8.0%} vs commercial Rs{COMMERCIAL_RENT_SF:.0f}")

    print("\n"+"="*80); print("LAST-MILE STACK  (per order)".center(80)); print("="*80)
    print(f"Rider cost per delivery, three independent routes:")
    print(f"  J.P. Morgan  Rs26.5K/mo / (21/day x 30)        Rs{ROUTE_JPM:.1f}")
    print(f"  JM metro     Rs37.5K/mo / (30/day x 26)        Rs{ROUTE_JM_METRO:.1f}")
    print(f"  JM non-metro Rs20.0K/mo / (17.5/day x 26)      Rs{ROUTE_JM_NONM:.1f}")
    print(f"  Eternal disclosed weighted delivery cost       Rs{ETERNAL_DELIV:.0f}   (Swiggy Rs{SWIGGY_DELIV:.0f})")
    print(f"  Round 1 model constant LAST_MILE               Rs{M.LAST_MILE:.0f}")
    print(f"\nDisclosed orders per ACTIVE hour                 {JPM_ORD_HR:.1f}")
    print(f"Geometric round trips per hour ({STD_TRIP:.0f} min trip)     {TRIPS_HR:.2f}")
    print(f">>> Implied BASELINE batching                    {BATCH_BASE:.2f}x  [DERIVED]")
    print(f">>> Rider cost per ACTIVE hour                   Rs{RIDER_HR_ACTIVE:.0f}")
    print(f">>> Rider utilisation ({JPM_ORD_DAY/JPM_ORD_HR:.1f} active hrs / 13-hr shift)  {UTILISATION:.0%}")

    print("\n"+"-"*80)
    print(f"{'GEOMETRY':<{W}} {'trip':>7} {'ord/hr':>7} {'Rs/order':>9} {'vs std':>8}")
    print("-"*80)
    base=None
    for n,legs in GEOM.items():
        t=trip(legs); c=last_mile(t)
        if base is None: base=c
        print(f"{n:<{W}} {t:>6.1f}m {60/t*BATCH_BASE:>7.2f} {c:>9.1f} {(c/base-1):>+8.0%}")

    print("\n"+"-"*80)
    print("GATE-DROP CONSOLIDATION  (rider stops at gate, N orders per trip)")
    print("-"*80)
    gd=trip(GEOM["Type A campus, gate-drop"])
    print(f"{'N':>3} {'ord/rider-hr':>13} {'Rs/order':>9} {'fee ceiling vs city':>21} {'vs campus door-drop':>21}")
    for n in (1.2,2,3,4,6,8):
        c=last_mile(gd,n)
        print(f"{n:>3} {60/gd*n:>13.2f} {c:>9.1f} {M.LAST_MILE-c:>21.1f} {DOOR-c:>21.1f}")

    print("\n"+"-"*80); print("THE PER-PARCEL FEE - CEILING vs FLOOR"); print("-"*80)
    print(f"Ceiling @4x, holding city cost structure      Rs{affordable_fee(4.0):.1f}/parcel")
    print(f"Ceiling @4x, holding campus door-drop cost    Rs{affordable_fee(4.0,DOOR):.1f}/parcel")
    print(f"Campus-runner labour floor (60 deliv/day)     Rs{RUNNER_COST_PARCEL:.1f}/parcel")

# ============================================================================
# 3. DECISION SUPPORT: which fixed base, and does GOV/store/day add anything
# ============================================================================
# JM scales staff WITH throughput (35 staff @1,600 OPD, 25 @950). A campus cluster store
# runs at the Round 1 ceiling of 1,400 OPD. Taking JM's 950-OPD staff count while claiming
# 1,400 OPD throughput uses their model half-way, which is worse than not using it.
def jm_interpolated(opd, salary=15000, rent_sf=70):
    s_lo, s_hi = JM["non_metro"][1], JM["metro"][1]      # 25, 35
    o_lo, o_hi = JM["non_metro"][5], JM["metro"][5]      # 950, 1600
    staff = s_lo + (s_hi-s_lo)*(opd-o_lo)/(o_hi-o_lo)
    sqft  = 3100
    return {"staff":staff, "labour":staff*salary, "rent":sqft*rent_sf,
            "util_other":sqft*100, "total":staff*salary + sqft*rent_sf + sqft*100}
CAMPUS_INTERP = jm_interpolated(M.CEILING)

def breakeven_gov_day(fixed, opd=M.CEILING, calendar=False):
    """Daily gross order value a store must clear to break even. Same constraint as
    breakeven AOV, expressed on the axis operators actually disclose."""
    aov = (store_cost_per_order(fixed, opd, calendar)
           + M.LAST_MILE/3.0 + M.STORE_OPS + M.PACKAGING + M.RESIDUAL)/M.TAKE_RATE
    return aov*opd, aov

BLINKIT_BE_GOV = 7.0e5   # T2  "Blinkit breakeven point: Rs7,00,000 in daily gross order value"
                         #     The Secretariat, trade press. NOT T1 - see shopping list item 10.

# Redseer / JM Financial Exhibit 31-33, non-metro vs top 10-15 cities  [T1]
RS_AOV_GAP, RS_LOGI_GAP, RS_BE_OPD = -0.35, +0.25, (1.5, 2.0)

if __name__ == "__main__":
    print("\n"+"="*80); print("DECISION: WHICH FIXED BASE".center(80)); print("="*80)
    print(f"{'Basis':<34}{'Rs/month':>11}{'staff':>7}{'BE AOV @3x':>12}{'BE GOV/day':>13}{'vs Rs7.0L':>10}")
    for lbl, fx, st in (
        ("Round 1  T2 band midpoint",  LEGACY_FIXED,            None),
        ("JM non-metro  T1 @950 OPD",  JM_NONMETRO["total"],    25),
        ("JM interpolated  T1 @1,400", CAMPUS_INTERP["total"],  CAMPUS_INTERP["staff"]),
        ("JM metro  T1 @1,600 OPD",    JM_METRO["total"],       35)):
        gov, _ = breakeven_gov_day(fx)
        print(f"{lbl:<34}{fx:>11,.0f}{(f'{st:.0f}' if st else '-'):>7}"
              f"{breakeven_at(fx):>12,.0f}{gov:>13,.0f}{gov/BLINKIT_BE_GOV-1:>+10.1%}")
    print("\n  BE GOV/day is computed WITHOUT the calendar surcharge, so it is comparable to")
    print("  a city-store benchmark. BE AOV @3x INCLUDES it, as Round 1 published it.")

    print("\n"+"-"*80)
    print("TRIANGULATION: Redseer/JM Exhibits 31-33, non-metro vs top 10-15 cities [T1]")
    print("-"*80)
    print(f"  Non-metro AOV                 {RS_AOV_GAP:+.0%}")
    print(f"  Non-metro per-order logistics {RS_LOGI_GAP:+.0%}  ('mother hubs underutilised')")
    print(f"  -> Non-metro breakeven OPD    {RS_BE_OPD[0]:.1f}-{RS_BE_OPD[1]:.1f}x metro")
    camp_logi = DOOR/M.LAST_MILE - 1
    print(f"\n  Type A campus logistics       {camp_logi:+.0%}   (our derived figure)")
    print(f"  -> campus breakeven OPD should exceed the non-metro {RS_BE_OPD[1]:.1f}x multiple.")
    print(f"     Against the {M.CEILING:,} orders/day observed ceiling, that is the whole problem,")
    print(f"     independently triangulated by a third-party benchmark we did not build.")

# ============================================================================
# S19 [2026-08-28]  THREE VERDICTS: batching anchor, ad revenue, D1/D2 tie-out
# ============================================================================

# ---- VERDICT 1: the UBS 2.7 orders/hour figure does NOT replace JPM's 4.0 ----
# The sweep proposed re-anchoring RIDER_HR_ACTIVE on UBS Evidence Lab (n=100 Indian
# riders, Nov-Dec 2025): c18 orders/day / 6.58 hours = c2.7 orders per active hour.
# TESTED AND REJECTED AS A REPLACEMENT, for one reason that is decisive:
# **UBS's 18 orders/day is FOOD DELIVERY.** UBS reports FD orders/day explicitly
# ("c18, stable vs 12 months ago"); the QUICK COMMERCE mean did not extract and UBS
# does not print it. JPM_ORD_HR = 4.0 is from a QUICK COMMERCE dark-store channel
# survey. Substituting a food-delivery productivity figure into a quick-commerce
# parameter is the same category error as pricing a dark-store chiller off bulk agri
# cold-storage rates. We do not do it.
UBS_FD_ORD_DAY, UBS_HRS_DAY = 18.0, 6.58     # T1  UBS Evidence Lab, Nov-Dec 2025, FOOD DELIVERY
UBS_FD_ORD_HR  = UBS_FD_ORD_DAY / UBS_HRS_DAY          # 2.74, FD only
UBS_REPLACES_JPM_ANCHOR = False

# What UBS DOES license is a sensitivity, and the conclusion must survive it.
RIDER_HR_ACTIVE_UBS = ROUTE_JPM * UBS_FD_ORD_HR        # if productivity were FD-like
def labour_class_ratio(gig_hr):
    """The D2 finding is a RATIO, not a level: gig active-hour vs employed rostered-hour."""
    return gig_hr / (15000.0 / (26.0 * 8.0))           # RUNNER_HR = Rs15,000/(26d x 8h)
RATIO_JPM = labour_class_ratio(RIDER_HR_ACTIVE)        # 2.33x, the headline
RATIO_UBS = labour_class_ratio(RIDER_HR_ACTIVE_UBS)    # 1.60x on the FD anchor
# Even on the most unfavourable anchor available, the employed runner is still cheaper
# per hour than the gig rider. THE FLEET CONCLUSION IS A LABOUR-CLASS CONCLUSION AND IT
# SURVIVES BOTH ANCHORS. State the range on the slide; the direction does not move.

# ---- VERDICT 2: there is NO missing advertising revenue line ----
# The sweep flagged that the model books no ad revenue while Blinkit earns >4% of GOV
# from ads. Checked: Blinkit's ad income is booked ENTIRELY TO REVENUE. TAKE_RATE is
# revenue as a % of GOV. Therefore ads are ALREADY INSIDE the 19.41%.
# The proof is the same identity that settled the gross/net question: the model's
# contribution per order reproduces Blinkit's REPORTED contribution profit exactly, and
# Blinkit's reported contribution includes ad income. If ads were missing from our
# revenue line the match could not close.
ADS_ALREADY_IN_TAKE_RATE = True
# The live risk is the OPPOSITE of the one flagged: a campus node with a smaller, more
# homogeneous cohort may monetise ads BELOW the network rate, which would make 19.41%
# optimistic for a campus. That is a downside sensitivity, not a missing revenue line.

# ---- VERDICT 3: D1 and D2 were NOT computed off the same last-mile cost. REAL. ----
# D1's breakeven divides the standard-zone rider cost (Rs42/order) by a consolidation
# factor of 3.0x. D2's circuit model computes the campus last mile from first principles
# -- employed runner, e-cart, dynamic batch, volume-weighted across the daypart -- and
# lands at Rs19.0/order. Rs42/3.0 = Rs14.0. The two deliverables disagreed by Rs5.0/order.
# The project rule locked at S1 is that D2 arithmetic runs BEFORE D1 costing. D1 must
# therefore take D2's number, not a proxy for it.
def consolidation_implied_by_d2(d2_cost_per_order):
    return M.LAST_MILE / d2_cost_per_order          # Rs42.0 / Rs19.0 = 2.21x

def breakeven_d2_consistent(fixed, d2_cost_per_order, opd=M.CEILING, take=M.TAKE_RATE):
    """D1 breakeven with the last-mile line taken straight from the D2 model."""
    return (store_cost_per_order(fixed, opd)
            + d2_cost_per_order + M.STORE_OPS + M.PACKAGING + M.RESIDUAL) / take

def s19_report(d2_cost=None):
    # WAS d2_cost=19.0 - the superseded last mile as a function default, the same defect that let
    # campus_model.NWC_DAYS = 18 survive. Defaults are the quietest place for a stale basis to live.
    if d2_cost is None:
        import sla as _SL; d2_cost = _SL.volume_weighted()[1]
    imp = consolidation_implied_by_d2(d2_cost)
    be_old = breakeven_at(CAMPUS_FIXED)
    be_new = breakeven_d2_consistent(CAMPUS_FIXED, d2_cost)
    print("\n" + "="*74)
    print("S19  THREE VERDICTS")
    print("="*74)
    print(f"  1  BATCHING ANCHOR")
    print(f"     UBS c18 orders/day / {UBS_HRS_DAY} h = {UBS_FD_ORD_HR:.2f} orders/active hr -- but FOOD DELIVERY.")
    print(f"     JPM 4.0/hr is QUICK COMMERCE. Not substituted. Sensitivity instead:")
    print(f"       gig cost/active hr   JPM anchor Rs{RIDER_HR_ACTIVE:.0f}   |  FD anchor Rs{RIDER_HR_ACTIVE_UBS:.0f}")
    print(f"       gig : runner ratio   {RATIO_JPM:.2f}x            |  {RATIO_UBS:.2f}x")
    print(f"     VERDICT  the labour-class conclusion survives both anchors. Range on slide.")
    print()
    print(f"  2  ADVERTISING REVENUE")
    print(f"     Ads are booked to revenue; TAKE_RATE is revenue/GOV; ads are already inside")
    print(f"     the {M.TAKE_RATE:.2%}. Proof: model contribution Rs{M.cm_per_order(M.BLINKIT_AOV,1.0):.1f}/order == Blinkit's")
    print(f"     REPORTED contribution Rs{M.BLINKIT_CP:.1f}/order, which includes ad income.")
    print(f"     VERDICT  no missing line. The real risk is the inverse: a campus cohort may")
    print(f"              monetise ads BELOW network rate. Downside sensitivity, not a gap.")
    print()
    print(f"  3  D1/D2 TIE-OUT  -- this one was real")
    print(f"     D1 last mile  Rs{M.LAST_MILE:.0f} / 3.00x consolidation = Rs{M.LAST_MILE/3.0:.1f}/order")
    print(f"     D2 last mile  volume-weighted circuit model        = Rs{d2_cost:.1f}/order")
    print(f"     -> D2 implies consolidation {imp:.2f}x, not 3.00x. The two disagreed by Rs{d2_cost-M.LAST_MILE/3.0:.1f}.")
    print(f"     Breakeven AOV, JM fixed base Rs{CAMPUS_FIXED:,.0f}:")
    print(f"       @3.00x proxy      Rs{be_old:.1f}   (S7 base case, SUPERSEDED)")
    print(f"       @D2 model         Rs{be_new:.1f}   <-- ADOPTED. D1 and D2 now tie out.")
    print(f"     VERDICT  +Rs{be_new-be_old:.1f} ({(be_new/be_old-1)*100:.1f}%). We were crediting a")
    print(f"              consolidation our own fulfilment design does not deliver.")
    print(f"     COINCIDENCE, flagged so nobody reads it as corroboration: the legacy Rs7.5L")
    print(f"     base at {imp:.2f}x also gives Rs{M.full_breakeven_aov(imp):.1f}. Two different roads, same number.")

BREAKEVEN_D2_CONSISTENT = None   # set by callers; see audit
