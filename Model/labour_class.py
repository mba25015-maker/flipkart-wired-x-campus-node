"""
CC-6: THE LABOUR-CLASS PARAMETER TABLE.

Team Glitch's slide 3 carried five costed parameters per rider class - fixed cost,
cost/order, cost/km, incentive, threshold - fifteen numbers. `DECK_TEARDOWN` records that
we had two: gig Rs168 per active hour against employed runner Rs72 per rostered hour.
This module builds the full table from what the model already holds.

THE ONE THING THEIR TABLE COULD NOT DO, and ours can: their THRESHOLD column
(FT 30 / PT 15 / GIG 10 orders) is an input they chose. Ours is SOLVED -
`fleet_mix.breakeven_volume()` returns the daily volume at which an employed runner
stops being more expensive than a gig rider on the same leg. Same column, opposite
epistemic status, and that is the sentence to say out loud.

WHAT IS NOT HERE, AND WHY. The INCENTIVE column has no model input. The corpus digest
carries a UBS rider-survey base+incentive split (Rs32-35 base + Rs33 incentive) but it is
not in any module, and the standing rule is import it or flag it. It is flagged - see
INCENTIVE_AVAILABLE. Four of five columns are derived; the fifth names its own pull.

LEGS DIFFER, AND THE TABLE MUST SAY SO. A gig rider runs the CITY trip (store -> gate).
An employed runner runs the IN-CLUSTER leg (gate -> block). They are not substitutes on
the same work, which is exactly why the load-bearing comparison is per HOUR, not per order.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import campus_model as M
import cost_stack as C
import fleet_mix as F

# ---------------------------------------------------------------------------
# COST PER KM  -  derived, and the derivation is the whole trick
# ---------------------------------------------------------------------------
# The platform does not bear vehicle running cost: the RIDER does, out of gross income.
# J.P. Morgan gives both sides of that - Rs26.5K income against Rs6.6K fuel. Converting
# fuel to a per-km rate needs the trip's distance, which the geometry already implies:
#   city leg  = CITY_LEG_MIN at the incumbent petrol-2W speed in fleet_mix.MODES
#   round trip = two legs; per order = round trip / the disclosed baseline batching
_2W_KMPH   = F.MODES["Petrol 2W (incumbent)"][0]
KM_PER_LEG = C.CITY_LEG_MIN / 60.0 * _2W_KMPH
KM_PER_TRIP = 2 * KM_PER_LEG
KM_PER_ORDER = KM_PER_TRIP / C.BATCH_BASE
FUEL_PER_ORDER = C.JPM_RIDER_FUEL / (C.JPM_ORD_DAY * C.RIDER_DAYS)
GIG_COST_PER_KM = FUEL_PER_ORDER / KM_PER_ORDER
# SENSITIVITY, stated not hidden: J.P. Morgan's own wording for the city leg is "<2 km",
# which would shorten the trip and RAISE the per-km rate. The derived figure is therefore
# a lower bound on rider-borne running cost, and it lands just under the Rs3.0-3.5/km that
# Team Glitch assumed - an independent cross-check we did not design for.
KM_PER_LEG_SOURCE_FLOOR = 2.0    # T1  JPM wording, "<2 km ride leg" - used only for the band
GIG_COST_PER_KM_HI = FUEL_PER_ORDER / (2 * KM_PER_LEG_SOURCE_FLOOR / C.BATCH_BASE)

# ---------------------------------------------------------------------------
# THE INCENTIVE COLUMN  -  flagged, not invented
# ---------------------------------------------------------------------------
INCENTIVE_AVAILABLE = False
INCENTIVE_PULL = ("UBS Evidence Lab rider survey (n=100, Nov-Dec 2025) base+incentive "
                  "split. Present in the corpus digest, absent from every module. "
                  "Pull it into cost_stack as a tagged input before this column is used.")

# ---------------------------------------------------------------------------
# THE CLASSES
# ---------------------------------------------------------------------------
# fixed_day   Rs/day borne by the platform whether or not an order flows
# per_order   Rs/order on the leg this class actually runs
# per_km      Rs/km of vehicle running cost, and who bears it
# per_hour    Rs/hour - ACTIVE for gig (paid per delivery), ROSTERED for the runner
# threshold   orders/day at which this class becomes the cheaper option on the campus leg
CLASSES = [
 dict(name="GIG  quick commerce", anchor="J.P. Morgan dark-store survey [T1]",
      leg="city trip, store -> gate",
      fixed_day=0.0,                       # structural: paid per delivery, no retainer
      per_order=C.ROUTE_JPM,
      per_km=GIG_COST_PER_KM, km_borne_by="rider",
      per_hour=C.RIDER_HR_ACTIVE, hour_basis="active",
      utilisation=C.UTILISATION,
      threshold=0.0),                      # structural: available at any volume
 dict(name="GIG  JM metro", anchor="JM Financial channel checks [T1]",
      leg="city trip, store -> gate",
      fixed_day=0.0,
      per_order=C.ROUTE_JM_METRO,
      per_km=GIG_COST_PER_KM, km_borne_by="rider",
      per_hour=C.ROUTE_JM_METRO * C.JPM_ORD_HR, hour_basis="active",
      utilisation=C.JM_METRO_DELIV_SHIFT / C.JPM_ORD_HR / C.JM_SHIFT_HRS,
      threshold=0.0),
 dict(name="GIG  JM non-metro", anchor="JM Financial channel checks [T1]",
      leg="city trip, store -> gate",
      fixed_day=0.0,
      per_order=C.ROUTE_JM_NONM,
      per_km=GIG_COST_PER_KM, km_borne_by="rider",
      per_hour=C.ROUTE_JM_NONM * C.JPM_ORD_HR, hour_basis="active",
      utilisation=C.JM_NONMETRO_DELIV_SHIFT / C.JPM_ORD_HR / C.JM_SHIFT_HRS,
      threshold=0.0),
 dict(name="EMPLOYED RUNNER", anchor="JM non-metro salary band + statutory roster [T1]",
      leg="in-cluster, gate -> block",
      fixed_day=F.RUNNER_DAY,
      per_order=F.in_cluster_cost("E-cart, stationed", 8, F.RUNNER_HR),   # audited Rs4.7
      per_km=0.0, km_borne_by="none (e-cart / cycle)",   # structural: no fuel borne
      per_hour=F.RUNNER_HR, hour_basis="rostered",
      utilisation=1.0,                     # rostered pricing: every hour is paid
      threshold=F.breakeven_volume()),     # SOLVED, not assumed
]

LABOUR_CLASS_RATIO = C.RIDER_HR_ACTIVE / F.RUNNER_HR      # 2.33x, the headline
RATIO_ON_FD_ANCHOR = C.RATIO_UBS                          # 1.60x, the unfavourable anchor


def report():
    W = 96
    print("=" * W)
    print("CC-6  LABOUR-CLASS PARAMETER TABLE".center(W))
    print("=" * W)
    print(f"{'CLASS':<22}{'FIXED/day':>11}{'Rs/ORDER':>10}{'Rs/KM':>8}"
          f"{'INCENTIVE':>11}{'THRESHOLD':>11}{'Rs/HOUR':>10}{'UTIL':>7}")
    print("-" * W)
    for c in CLASSES:
        inc = "n/a" if not INCENTIVE_AVAILABLE else ""
        thr = "any" if c["threshold"] == 0 else f"{c['threshold']:.0f}/day"
        print(f"{c['name']:<22}{c['fixed_day']:>11,.0f}{c['per_order']:>10.2f}"
              f"{c['per_km']:>8.2f}{inc:>11}{thr:>11}"
              f"{c['per_hour']:>10.1f}{c['utilisation']:>7.0%}")
    print("-" * W)
    print("  FIXED/day  Rs borne by the platform whether or not an order flows. Gig = 0 is")
    print("             STRUCTURAL: the rider is paid per delivery and carries the vehicle.")
    print("  Rs/KM      vehicle running cost, borne by:")
    for c in CLASSES:
        print(f"               {c['name']:<22}{c['km_borne_by']}")
    print(f"             derived: Rs{C.JPM_RIDER_FUEL:,.0f}/mo fuel / "
          f"({C.JPM_ORD_DAY:.0f} orders x {C.RIDER_DAYS:.0f} days) = Rs{FUEL_PER_ORDER:.2f}/order,")
    print(f"             over {KM_PER_ORDER:.2f} km/order (two {C.CITY_LEG_MIN:.0f}-min legs at "
          f"{_2W_KMPH:.0f} kmph / {C.BATCH_BASE:.1f}x batch)")
    print(f"             band on JPM's own '<2 km leg' wording: "
          f"Rs{GIG_COST_PER_KM:.2f}-{GIG_COST_PER_KM_HI:.2f}/km")
    print("  Rs/HOUR    ACTIVE hours for gig (idle time is unpaid and uncosted);")
    print("             ROSTERED hours for the runner (every hour is paid). Not the same unit,")
    print("             which is the point - see the ratio below.")
    print(f"  UTIL       active hours / shift, each on ITS OWN source's shift length")
    print(f"             (JPM 13h, JM {C.JM_SHIFT_HRS:.0f}h). JM's non-metro rider sits at "
          f"{CLASSES[2]['utilisation']:.0%}, which is")
    print(f"             JM's own explanation for the non-metro cost gap: 'high idle time'.")
    print("  THRESHOLD  orders/day at which the class becomes the cheaper option on the campus")
    print("             leg. For the runner this is SOLVED by fleet_mix.breakeven_volume(),")
    print("             not chosen. Gig has no threshold: it is available at any volume.")
    print()
    print("  INCENTIVE  NOT AVAILABLE. " + INCENTIVE_PULL)
    print()
    print("=" * W)
    print("  THE FINDING IS A RATIO, AND IT SURVIVES THE WORST ANCHOR")
    print("=" * W)
    print(f"    gig active hour Rs{C.RIDER_HR_ACTIVE:.0f}  :  runner rostered hour Rs{F.RUNNER_HR:.0f}"
          f"   =  {LABOUR_CLASS_RATIO:.2f}x   [JPM quick-commerce anchor]")
    print(f"    on the unfavourable food-delivery anchor                     "
          f"=  {RATIO_ON_FD_ANCHOR:.2f}x   [UBS, tested at S19]")
    print(f"    Rider utilisation is why: {C.UTILISATION:.0%} of a gig rider's shift is active, so")
    print(f"    the platform pays a premium for the {1-C.UTILISATION:.0%} it does not use. An employed")
    print(f"    runner on a bounded campus leg has no idle time to pay for.")
    print(f"    >>> The fleet decision is a LABOUR-CLASS decision, not a vehicle decision,")
    print(f"        and it holds on both anchors. State the range on the slide.")


if __name__ == "__main__":
    report()
