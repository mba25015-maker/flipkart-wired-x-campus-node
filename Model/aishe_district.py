"""
THE DISTRICT LAYER. AISHE institution register, as on 28-8-2026, parsed to district level.

WHY THIS MATTERS. Round 1 and the corpus sweep could only reach STATE level: the AISHE 2023-24
report publishes exactly ONE district table, ten rows long (Box 2, top districts by college count).
Section 4 of CORPUS_SWEEP recorded "no district or city enrolment anywhere" as a hard absence and
proposed imputing district shares pro-rata. That imputation is no longer necessary for the COUNT
layer: the full register gives every institution with its district AND its urban/rural flag.

WHAT IS NEW AND WHAT IS NOT.
  NEW  - institution counts by district, and the URBAN/RURAL split, which we never had.
  NOT  - enrolment. The register carries no student numbers. District enrolment is still an
         imputation off state totals and must stay labelled as one.

SOURCE  AISHE portal institution register, downloaded 28-8-2026:
        College-ALL COLLEGE.xlsx | University-ALL UNIVERSITIES.xlsx | Standalone-ALL STANDALONE.xlsx
        NOTE: 'College-Affiliated College.xlsx' is a BYTE-IDENTICAL DUPLICATE of ALL COLLEGE
        (same 54,014 AISHE codes). Same class of duplicate as CRISIL Benchmarks/cold chain. Ignored.

VINTAGE WARNING, and it must be stated wherever these counts appear next to the report's:
        this register is the LIVE list as on 28-8-2026 (54,014 colleges). The AISHE 2023-24 REPORT
        counts 48,246 colleges at 31-12-2023. Different instruments, different dates.
        DO NOT mix a count from here with an enrolment from the report without saying so.

TIERS: T1 government register | D derived
"""
import json
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
SUMMARY = json.loads((DATA / "aishe_summary.json").read_text(encoding="utf-8"))

# Public-safe derivative: one row per state/district. Institution-level records are
# deliberately not redistributed. See Model/data/README.md for provenance and limits.
DIST = pd.read_csv(DATA / "aishe_district_aggregates.csv")

N_COL = int(SUMMARY["n_colleges"])
N_UNI = int(SUMMARY["n_universities"])
N_STA = int(SUMMARY["n_standalone"])
N_HEI = N_COL + N_UNI + N_STA
N_DISTRICTS = int(SUMMARY["n_districts"])

# ---- the urban screen, and it is the finding ------------------------------
URBAN_COL = int(SUMMARY["urban_colleges"])
RURAL_COL = int(SUMMARY["rural_colleges"])
URBAN_SHARE_COL = URBAN_COL / (URBAN_COL + RURAL_COL)

# ---- the archetype screen, made operational ------------------------------
# S17 selected "Tier-1/2 dense cluster" and S17 also flagged that JM's "Tier-1/2" is a RENT-BAND
# taxonomy while AISHE has no tier concept. This is where the archetype stops being a label.
# Operational definition, all three conditions:
#   (a) NOT one of the eight metros - those carry ~4,300 dark stores against ~3,600 of sustainable
#       capacity and 44% five-operator pin-code overlap [Bernstein, 18 Jul 2026]
#   (b) at least MIN_URBAN_COLLEGES urban colleges in the district - the node is underwritten by a
#       3-6 college cluster, not one campus [S17]
#   (c) urban share of colleges above URBAN_SHARE_FLOOR - a district whose colleges are mostly rural
#       has no contiguous walk-scale cluster to serve
METROS = {"Bengaluru Urban","Mumbai","Mumbai Suburban","Delhi","New Delhi","Central Delhi",
          "North Delhi","South Delhi","East Delhi","West Delhi","North West Delhi",
          "South West Delhi","North East Delhi","South East Delhi","Shahdara",
          "Hyderabad","Chennai","Kolkata","Pune","Ahmadabad","Ahmedabad"}
MIN_URBAN_COLLEGES = 6      # D  a 3-6 college cluster plus headroom to choose within the district
URBAN_SHARE_FLOOR  = 0.50   # D  majority-urban district

def screen(min_urban=MIN_URBAN_COLLEGES, floor=URBAN_SHARE_FLOOR, drop_metros=True):
    t = DIST.copy()
    if drop_metros:
        t = t[~t.District.isin(METROS)]
    t = t[(t.urban_colleges >= min_urban) & (t.urban_share >= floor)]
    return t.sort_values("urban_colleges", ascending=False).reset_index(drop=True)

CANDIDATES = screen()
N_CANDIDATES = len(CANDIDATES)


# ---- COHORT QUALITY: which standalones are residential and high-propensity ----
# The register's Standalone Type is a usable cohort proxy. Technical/Polytechnic, PGDM, Pharmacy
# and Hotel Management are residential, urban-skewed and closest to the E&T/IT cohort that Round 1
# identified as the propensity core. Nursing and Teacher Training are large but rurally distributed.
N_STA_URBAN_HP = int(SUMMARY["urban_high_propensity_standalone"])

def with_cohort(t):
    if "urb_hp_standalone" in t.columns:
        return t
    hp = DIST[["State", "District", "urb_hp_standalone"]]
    return t.merge(hp, on=["State","District"], how="left").fillna({"urb_hp_standalone":0})

# ---- CLUSTER GEOMETRY: is the node underwritten by one campus or by a cluster? ----
# S17: "high-enrolment/low-density = one campus can underwrite a node; low-enrolment/high-density =
# the node must be underwritten by a 3-6 college cluster." The register gives the density half
# directly. A district with many urban colleges is a CLUSTER site; a district with few urban
# colleges but a university present is a SINGLE-CAMPUS site.
def geometry(row):
    if row.urban_colleges >= 40:  return "cluster-dense"
    if row.urban_colleges >= 15:  return "cluster"
    return "single-campus"

# ---- state-level residential intensity, to weight the candidates ----------
# From AISHE 2023-24 Tables 31/44, recorded in CORPUS_SWEEP section 4. State level ONLY.
# Applying a state ratio to a district is an IMPUTATION and is labelled as one everywhere it is used.
RESIDENTIAL_PCT = {   # hostel residents / regular-mode enrolment  [D, from T1 tables]
 "Odisha":27.6,"Andhra Pradesh":25.2,"Karnataka":22.7,"Tamil Nadu":21.7,"Punjab":21.1,
 "Kerala":20.1,"Gujarat":16.2,"Telangana":15.2,"Haryana":11.4,"Maharashtra":10.8,
 "Delhi":9.8,"West Bengal":8.5,"Rajasthan":6.5,"Madhya Pradesh":5.3,"Uttar Pradesh":5.1,"Bihar":4.6}
HOSTEL_OCCUPANCY = {  # residents / sanctioned intake  [D, from T1 Table 31]
 "Odisha":73.0,"Telangana":70.2,"Kerala":61.1,"Andhra Pradesh":59.4,"Uttar Pradesh":59.0,
 "West Bengal":58.9,"Bihar":57.4,"Madhya Pradesh":57.0,"Haryana":55.2,"Rajasthan":54.9,
 "Tamil Nadu":53.6,"Maharashtra":52.3,"Punjab":51.5,"Karnataka":49.2,"Gujarat":45.0,"Delhi":83.7}

def ranked(top=25):
    t = CANDIDATES.copy()
    t["residential_pct"] = t.State.map(RESIDENTIAL_PCT)
    t["hostel_occupancy"] = t.State.map(HOSTEL_OCCUPANCY)
    t = t[t.residential_pct.notna()]
    # S17's criterion: BOTH residential intensity AND occupancy must be high. Multiply, do not average
    # - a state with nominal hostel stock that sits empty is not a campus micro-market.
    t["resid_index"] = t.residential_pct * t.hostel_occupancy / 100.0
    t["score"] = t.urban_colleges * t.resid_index
    t = with_cohort(t)
    t["geometry"] = t.apply(geometry, axis=1)
    return t.sort_values("score", ascending=False).head(top).reset_index(drop=True)

TOP = ranked()

def report(n=20):
    print("="*92); print("AISHE DISTRICT REGISTER — THE SITE FILTER'S MISSING LAYER".center(92)); print("="*92)
    print(f"  Register as on 28-8-2026: {N_COL:,} colleges + {N_UNI:,} universities + {N_STA:,} standalone")
    print(f"  = {N_HEI:,} institutions across {N_DISTRICTS} districts")
    print(f"  (AISHE 2023-24 REPORT counts 48,246 colleges at 31-12-2023 — different instrument, different date)")
    print()
    print(f"  >>> URBAN/RURAL, and this is the finding we could not previously make:")
    print(f"      urban colleges {URBAN_COL:,}   rural colleges {RURAL_COL:,}   URBAN SHARE {URBAN_SHARE_COL:.1%}")
    print(f"      SIX IN TEN INDIAN COLLEGES ARE RURAL. The campus micro-market universe is")
    print(f"      {URBAN_COL:,} colleges, not {N_COL:,}. Nothing in the corpus said this before.")
    print()
    print(f"  ARCHETYPE, MADE OPERATIONAL (S17 left this open):")
    print(f"    exclude the 8 metros · >= {MIN_URBAN_COLLEGES} urban colleges · urban share >= {URBAN_SHARE_FLOOR:.0%}")
    print(f"    -> {N_CANDIDATES} candidate districts of {N_DISTRICTS}")
    print()
    print("  TOP DISTRICTS, weighted by state residential intensity x hostel occupancy")
    print(f"  {'district':<24}{'state':<16}{'urb col':>8}{'uni':>5}{'urb HP sta':>11}{'urb%':>6}{'resid idx':>10}  {'geometry':<14}")
    print("  "+"-"*92)
    for _,r in TOP.head(n).iterrows():
        print(f"  {r.District[:23]:<24}{r.State[:15]:<16}{r.urban_colleges:>8}{r.universities:>5}"
              f"{int(r.urb_hp_standalone):>11}{r.urban_share:>6.0%}{r.resid_index:>10.1f}  {r.geometry:<14}")
    print("  "+"-"*88)
    print(f"  urban high-propensity standalones nationally: {N_STA_URBAN_HP:,} of {N_STA:,}")
    print("  (Technical/Polytechnic, PGDM, Pharmacy, Hotel Mgmt - residential, urban, closest to the")
    print("   E&T/IT propensity core. Nursing and Teacher Training are large but rurally distributed.)")
    print("  resid idx = state residential % x state hostel occupancy / 100. STATE ratios applied to")
    print("  a DISTRICT: an imputation, labelled as one. The register carries no enrolment.")

if __name__ == "__main__":
    report()


# ============================================================================
# CC-7  THE CONTESTEDNESS SCREEN  [2026-08-29]
# ============================================================================
# WHAT THE FILTER DOES NOT SAY. risk_quadrant sets the site filter at 569 orders/day of
# adjacent non-student catchment (the higher of break-period solvency and revocation
# survival). That number is SILENT ABOUT WHO ELSE IS ALREADY SERVING IT. A campus cluster
# whose adjacent catchment is already covered by two incumbent dark stores does not have
# 569 orders/day available to it; it has whatever is left.
#
# THE EVIDENCE, and it is the strongest single argument against our own site list:
#   Apr-Jul 2026 the five largest operators added ~900 dark stores, but unique pin codes
#   served rose by only 152, to 2,722. Five-operator overlap in METRO pin codes went
#   26% -> 44% IN ONE QUARTER. Metros hold ~4,300 stores against ~3,600 of sustainable
#   capacity.  [T2, Bernstein via Economic Times, 18 Jul 2026 - corpus digest]
# The marginal store is going where stores already are. That is a densification wall, and
# it is the reason the campus thesis has to be stated in UNCONTESTED demand or not at all.
#
# TIERS: T2 analyst-via-press | D derived

OPERATOR_STORES = {          # T2  same Bernstein/ET line, Jul 2026
 "Blinkit": 2511, "Zepto": 1345, "Instamart": 1187,
 "Flipkart Minutes": 1000,   # "crossed 1,000"
 "Amazon Now": 650,          # midpoint of the 600-700 range given
}
PIN_CODES_SERVED   = 2722    # T2  unique pin codes served by the five largest operators
PIN_CODES_ADDED_Q  = 152     # T2  Apr-Jul 2026
STORES_ADDED_Q     = 900     # T2  Apr-Jul 2026
METRO_OVERLAP_5OP  = 0.44    # T2  share of metro pin codes served by all five, Jul 2026
METRO_OVERLAP_PRIOR = 0.26   # T2  the same measure one quarter earlier
METRO_STORES       = 4300    # T2  stores held in the eight metros
METRO_SUSTAINABLE  = 3600    # T2  Bernstein's estimate of sustainable metro capacity

TOTAL_STORES     = sum(OPERATOR_STORES.values())
NON_METRO_STORES = TOTAL_STORES - METRO_STORES
METRO_EXCESS     = METRO_STORES/METRO_SUSTAINABLE - 1          # +19% over capacity
STORES_PER_NEW_PINCODE  = STORES_ADDED_Q/PIN_CODES_ADDED_Q     # 5.9 - stacking, not reaching
STORES_PER_SERVED_PIN   = TOTAL_STORES/PIN_CODES_SERVED        # 2.46 operators per served pin

# ---- allocating stores to districts: an IMPUTATION, labelled as one -------------------
# The register carries no store locations and no district enrolment, so per-district store
# COUNTS cannot be observed. What the register does give is urban colleges by district, and
# dark stores and colleges both follow urban density. Stores are therefore allocated
# pro-rata to urban colleges, separately inside and outside the metros so the metro
# saturation does not leak into the non-metro estimate.
# This is the SAME class of imputation as RESIDENTIAL_PCT above (a state ratio applied to a
# district) and carries the same warning: it is a scale band, NOT a geocoded proximity
# measure. The pull that would replace it is operator pin-code coverage by district.
METRO_URBAN_COLLEGES     = int(DIST[DIST.District.isin(METROS)].urban_colleges.sum())
NON_METRO_URBAN_COLLEGES = URBAN_COL - METRO_URBAN_COLLEGES
METRO_STORE_DENSITY      = METRO_STORES / METRO_URBAN_COLLEGES          # stores per urban college
NON_METRO_STORE_DENSITY  = NON_METRO_STORES / NON_METRO_URBAN_COLLEGES
DENSITY_RATIO            = METRO_STORE_DENSITY / NON_METRO_STORE_DENSITY  # ~10x

def expected_incumbent_stores(urban_colleges):
    """Imputed incumbent dark stores in a non-metro district. Scale band, not a location."""
    return urban_colleges * NON_METRO_STORE_DENSITY

# Band edges are both SOURCED quantities, not chosen round numbers:
#   1.0  ................ an incumbent is present in the district at all
#   STORES_PER_SERVED_PIN  the national average operator stacking on an already-served
#                          location - at or above it, the district is as contested as the
#                          average place the industry already serves
PROXIMITY_BANDS = [("uncontested", 0.0, 1.0),
                   ("contested",   1.0, STORES_PER_SERVED_PIN),
                   ("stacked",     STORES_PER_SERVED_PIN, float("inf"))]

def proximity_flag(urban_colleges):
    e = expected_incumbent_stores(urban_colleges)
    for name, lo, hi in PROXIMITY_BANDS:
        if lo <= e < hi:
            return name
    return "stacked"

def with_proximity(t=None):
    t = CANDIDATES.copy() if t is None else t.copy()
    t["exp_incumbent_stores"] = t.urban_colleges.map(expected_incumbent_stores)
    t["proximity"] = t.urban_colleges.map(proximity_flag)
    return t

CANDIDATES_PROX = with_proximity()
PROX_COUNTS = {n: int((CANDIDATES_PROX.proximity == n).sum()) for n, _, _ in PROXIMITY_BANDS}
N_UNCONTESTED = PROX_COUNTS["uncontested"]
STACKED_SHARE = PROX_COUNTS["stacked"] / len(CANDIDATES_PROX)

# ---- THE FILTER, RESTATED ------------------------------------------------------------
# risk_quadrant's 569/day becomes a requirement on UNCONTESTED demand. The gross adjacent
# demand a site must carry to yield it is 569 / (1 - contested share). The contested share
# for a non-metro district is NOT sourceable - only the metro five-operator overlap is
# published - so the requirement is reported as a BAND between the two sourced ends, which
# is the same practice the model uses for residual campus demand (8-15%, never a point).
def _site_filter():
    import risk_quadrant as _Q
    ps = _Q.post_revocation_survival()
    return max(ps["adjacent_hi"], ps["orders_needed"])

SITE_FILTER_UNCONTESTED = _site_filter()                              # 569/day, uncontested
GROSS_AT_METRO_OVERLAP  = SITE_FILTER_UNCONTESTED/(1-METRO_OVERLAP_5OP)   # 1,015/day gross

def gross_demand_required(contested_share):
    """Gross adjacent demand a site needs to yield SITE_FILTER_UNCONTESTED of uncontested demand."""
    return SITE_FILTER_UNCONTESTED/(1-contested_share)

def contestedness_report(n=12):
    W = 92
    print("\n"+"="*W); print("CC-7  THE CONTESTEDNESS SCREEN".center(W)); print("="*W)
    print(f"  Operator store counts, Jul 2026  [T2, Bernstein via ET, 18 Jul 2026]")
    for k, v in OPERATOR_STORES.items():
        print(f"    {k:<20}{v:>7,}")
    print(f"    {'TOTAL':<20}{TOTAL_STORES:>7,}   of which metros hold {METRO_STORES:,}"
          f"  ({METRO_EXCESS:+.0%} vs sustainable capacity {METRO_SUSTAINABLE:,})")
    print()
    print(f"  THE DENSIFICATION WALL, in two numbers:")
    print(f"    stores added last quarter per NEW pin code served   {STORES_PER_NEW_PINCODE:.1f}")
    print(f"    five-operator overlap in metro pin codes            "
          f"{METRO_OVERLAP_PRIOR:.0%} -> {METRO_OVERLAP_5OP:.0%} in ONE quarter")
    print(f"    -> the marginal store is STACKING, not reaching. Nine of every ten new")
    print(f"       stores went somewhere an operator was already serving.")
    print()
    print(f"  STORE DENSITY PER URBAN COLLEGE  (imputation, see note in source)")
    print(f"    metro       {METRO_STORE_DENSITY:>6.2f}   ({METRO_STORES:,} stores / "
          f"{METRO_URBAN_COLLEGES:,} urban colleges)")
    print(f"    non-metro   {NON_METRO_STORE_DENSITY:>6.2f}   ({NON_METRO_STORES:,} stores / "
          f"{NON_METRO_URBAN_COLLEGES:,} urban colleges)")
    print(f"    ratio       {DENSITY_RATIO:>6.1f}x  -- the headroom outside the metros is real,")
    print(f"                        which is why the archetype excludes them in the first place.")
    print()
    print(f"  THE {len(CANDIDATES_PROX)} CANDIDATE DISTRICTS, SCREENED FOR INCUMBENT PRESENCE")
    print(f"    {'band':<14}{'expected incumbent stores':<28}{'districts':>10}")
    for name, lo, hi in PROXIMITY_BANDS:
        rng = (f"< {hi:.1f}" if lo == 0 else
               (f">= {lo:.2f}" if hi == float('inf') else f"{lo:.1f} - {hi:.2f}"))
        print(f"    {name:<14}{rng:<28}{PROX_COUNTS[name]:>10}")
    print(f"    -> {STACKED_SHARE:.0%} of our own candidate list is ALREADY as contested as the")
    print(f"       average location the industry serves. Only {N_UNCONTESTED} districts are clean.")
    print()
    print(f"  {'district':<22}{'state':<15}{'urb col':>8}{'exp stores':>11}  {'proximity':<12}")
    print("  "+"-"*(W-2))
    tp = with_proximity(TOP)
    for _, r in tp.head(n).iterrows():
        print(f"  {r.District[:21]:<22}{r.State[:14]:<15}{r.urban_colleges:>8}"
              f"{r.exp_incumbent_stores:>11.1f}  {r.proximity:<12}")
    print("  "+"-"*(W-2))
    print()
    print("="*W); print("  THE FILTER, RESTATED".center(W)); print("="*W)
    print(f"    WAS   adjacent catchment >= {SITE_FILTER_UNCONTESTED:.0f} orders/day")
    print(f"    IS    >= {SITE_FILTER_UNCONTESTED:.0f} orders/day of UNCONTESTED demand")
    print()
    print(f"    {'contested share of adjacent demand':<40}{'gross demand required':>22}")
    for c in (0.0, 0.10, 0.25, METRO_OVERLAP_5OP):
        tag = "  <- metro five-operator overlap [T2]" if c == METRO_OVERLAP_5OP else ""
        print(f"    {c:<40.0%}{gross_demand_required(c):>18,.0f}/day{tag}")
    print()
    print(f"    The non-metro contested share is NOT published - only the metro overlap is - so")
    print(f"    the requirement is a BAND: {SITE_FILTER_UNCONTESTED:,.0f}/day on a clean site rising to "
          f"{GROSS_AT_METRO_OVERLAP:,.0f}/day")
    print(f"    on a site as contested as a metro pin code. Quote the band, not a point.")
    print()
    print(f"    >>> WHY THIS STRENGTHENS THE THESIS RATHER THAN WEAKENING IT. A contested")
    print(f"        catchment is exactly what a CAMPUS is not: bounded access, a gate, and a")
    print(f"        population an incumbent cannot serve without the same permission we need.")
    print(f"        The campus demand inside the gate is uncontested BY CONSTRUCTION. It is the")
    print(f"        ADJACENT half of the catchment that this screen prices - and that is the half")
    print(f"        the break-period and revocation cases both lean on.")

if __name__ == "__main__":
    contestedness_report()
