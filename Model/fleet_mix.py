"""
D2: fleet mix compared on cost per order, not on vehicle capital cost.

WHY NOT VEHICLE CAPEX. cost_stack.py establishes that LAST_MILE reconciles to rider payout
almost exactly (J.P. Morgan route Rs42.1 vs the Rs42.0 model constant, 0.2% apart). The platform
does not own the vehicles - the rider does, and the rider absorbs fuel (Rs6.6K against Rs26.5K
gross income, 25%). A vehicle-capex comparison table would therefore be comparing costs that sit
on the rider's P&L, not Flipkart's.

What a fleet change actually moves is one of three things:
  1. TRIP TIME        -> orders per rider-hour -> cost per order
  2. ACCESS           -> whether the leg can be served at all inside a gated boundary
  3. LABOUR CLASS     -> gig rider at active-hour pricing vs employed runner at wage pricing
The third is the largest and it is the one a vehicle table would miss entirely.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import campus_model as M, cost_stack as C, params as P

# ---------------- LABOUR CLASSES ----------------
GIG_HR    = C.RIDER_HR_ACTIVE          # D  Rs168/active hour, from JPM: Rs26.5K/mo, 21 ord/day, 4 ord/hr
RUNNER_MO = 15000.0                    # T1 JM Financial non-metro dark-store staff salary
RUNNER_D, RUNNER_H = 26.0, 8.0         # A  employed roster
RUNNER_HR = RUNNER_MO/(RUNNER_D*RUNNER_H)
# A gig rider is priced per ACTIVE hour and bears the vehicle. An employed runner is priced per
# ROSTERED hour and the vehicle is a bicycle or their own feet. That gap is the fleet decision.

# ---------------- MODES ----------------
# speed_kmph, can enter a gated campus, orders carryable per trip, who bears the vehicle
MODES = {
 "Petrol 2W (incumbent)":   (20.0, False, 4,  "rider"),
 "E-2W":                    (20.0, True,  4,  "rider or leased"),
 "Cycle":                   (12.0, True,  3,  "rider or provided"),
 "On-foot runner":          ( 5.0, True,  4,  "none"),
 "E-cart, stationed":       (15.0, True, 12,  "operator or institution"),
}
# Campus access: petrol 2W is the mode institutions actually object to (noise, volume, safety).
# E-2W is the mode most likely to be permitted under a negotiated cap - quieter, no emissions,
# and the pitch is that consolidated credentialed vehicles REDUCE total movements. [judgement, A]

DROP_MIN     = 2.0    # A  per-drop inside the cluster: locate block/room, hand over
SHELF_DROP   = 0.5    # A  per-drop to a block-level pickup shelf instead of a room
SPREAD_KM    = 0.15   # A  added circuit distance per additional drop within a hostel cluster

def circuit_min(mode, drops, drop_min=DROP_MIN):
    """In-cluster circuit: gate -> blocks -> gate, for `drops` orders."""
    v = MODES[mode][0]
    dist = 2*C.CAMPUS_KM + SPREAD_KM*max(0, drops-1)
    return dist/v*60 + drops*drop_min

def in_cluster_cost(mode, drops, hourly, drop_min=DROP_MIN):
    """Cost per ORDER of the intra-campus leg alone."""
    return hourly * (circuit_min(mode, drops, drop_min)/60.0) / drops

def total_campus_cost(mode, drops, hourly, drop_min=DROP_MIN):
    """City leg (gig rider to the gate, batched) + intra-campus leg."""
    gate_trip = C.trip(C.GEOM["Type A campus, gate-drop"])
    city_leg  = GIG_HR * (gate_trip/60.0) / drops
    return city_leg + in_cluster_cost(mode, drops, hourly, drop_min)

# ============================================================================
# THE MIX, OPTIMISED - not "what roster do we run" but "what roster is cheapest"
# Decision variable: alpha, the share of in-gate orders served by ROSTERED runners.
# The remainder rides the same leg on gig, which carries no idle cost.
#   cost/order(alpha,V) = [ R(alpha)*RUNNER_DAY + (1-alpha)*V*gig_leg ] / V
#   R(alpha) = ceil(alpha*V / capacity)          runners are integers, and that is the point
# A runner costs RUNNER_DAY whether volume arrives or not, so the LAST runner is only
# worth rostering if the volume left for it clears the breakeven. That makes the optimum
# a closed form rather than a search.
# ============================================================================
def gig_leg_cost(mode="E-cart, stationed", drops=8, drop_min=SHELF_DROP):
    """Gig on the SAME in-gate leg. The comparison has to hold the leg constant."""
    return in_cluster_cost(mode, drops, GIG_HR, drop_min)

def mix_cost_per_order(alpha, orders_day, mode="E-cart, stationed", drops=8, drop_min=SHELF_DROP):
    import math
    cap = runner_capacity(0, drops, mode, drop_min)
    gig = gig_leg_cost(mode, drops, drop_min)
    R   = math.ceil(alpha*orders_day/cap) if alpha > 0 else 0
    return (R*RUNNER_DAY + (1-alpha)*orders_day*gig) / orders_day

def optimal_roster(orders_day, mode="E-cart, stationed", drops=8, drop_min=SHELF_DROP):
    """Closed form. Roster the whole runners the volume can keep busy; the residual gets a
    runner only if it clears the breakeven, otherwise it rides gig.
    Returns (runners, alpha, cost_per_order)."""
    cap = runner_capacity(0, drops, mode, drop_min)
    gig = gig_leg_cost(mode, drops, drop_min)
    be  = RUNNER_DAY/gig
    R   = int(orders_day // cap)
    residual = orders_day - R*cap
    if residual >= be:
        R += 1
        alpha = 1.0
    else:
        alpha = (R*cap)/orders_day if orders_day else 0.0
    cost = (R*RUNNER_DAY + (1-alpha)*orders_day*gig)/orders_day
    return R, alpha, cost

def plan_roster(cluster=None, topology=None, mode="E-cart, stationed", drops=8,
                drop_min=SHELF_DROP):
    """THE PLAN'S in-gate cost, under the adopted topology in params.GATE_TOPOLOGY.

    BASE CASE is per_gate: a node serves params.CAMPUSES_PER_NODE campus gates, runners
    are stationed at one gate and do not move between them, so the roster is optimised
    at each gate and aggregated. 1,400/day over three gates is 467/day each.

    Returns (runners_total, alpha_blended, cost_per_order, gates).
    """
    cluster  = P.CLUSTER_VOLUME if cluster is None else cluster
    topology = P.GATE_TOPOLOGY  if topology is None else topology
    gates    = 1 if topology == "pooled" else P.CAMPUSES_PER_NODE
    per_gate = cluster / gates
    R, a, c  = optimal_roster(per_gate, mode, drops, drop_min)
    return R*gates, a, c, gates

def pooled_upside(cluster=None, mode="E-cart, stationed", drops=8, drop_min=SHELF_DROP):
    """THE CONDITIONAL UPSIDE, not the plan.

    Pooling all gates into one dispatch queue is cheaper because integer runners are
    used more fully: one pool of 1,400 fills 7 runners at 99.0%, while three pools of
    467 each strand capacity at the top of each gate's own roster.

    It is NOT the base case, because it assumes runners reposition between gates with no
    travel time, no access delay and no fragmented shift capacity - none of which we have
    validated. The pilot's cross-gate movement test is the gate that would promote it.

    Returns (runners, alpha, cost_per_order, saving_per_order_vs_plan).
    """
    cluster = P.CLUSTER_VOLUME if cluster is None else cluster
    R, a, c = optimal_roster(cluster, mode, drops, drop_min)
    _, _, plan_c, _ = plan_roster(cluster, "per_gate", mode, drops, drop_min)
    return R, a, c, plan_c - c

def shelf_handoff_value(drops=8, mode="E-cart, stationed"):
    """What the block-level pickup shelf is worth per order, against a door drop.
    The deck argues for the shelf in the licence; this prices it."""
    door  = in_cluster_cost(mode, drops, RUNNER_HR, DROP_MIN)
    shelf = in_cluster_cost(mode, drops, RUNNER_HR, SHELF_DROP)
    return door - shelf, door, shelf

if __name__ == "__main__":
    print("="*84); print("WHY THE LABOUR CLASS DOMINATES THE VEHICLE".center(84)); print("="*84)
    print(f"Gig rider, per ACTIVE hour       Rs{GIG_HR:>6.0f}   bears own vehicle + fuel (25% of gross)")
    print(f"Employed runner, per ROSTERED hr Rs{RUNNER_HR:>6.0f}   bicycle or on foot, no fuel")
    print(f"                                 {'-'*8}")
    print(f"Ratio                            {GIG_HR/RUNNER_HR:>6.1f}x")
    print("\nThe intra-campus leg is the ONLY leg that can be served by the cheaper class,")
    print("because it is the only leg that never leaves the boundary.")

    print("\n"+"="*84); print("INTRA-CAMPUS LEG: COST PER ORDER BY MODE AND BATCH SIZE".center(84)); print("="*84)
    print(f"{'Mode':<26}{'access':>8}{'speed':>7}" + "".join(f"{f'n={n}':>9}" for n in (1,2,3,4,8,12)))
    print("-"*84)
    for m,(v,acc,cap,_) in MODES.items():
        hourly = RUNNER_HR if m in ("Cycle","On-foot runner","E-cart, stationed") else GIG_HR
        row = "".join(f"{(in_cluster_cost(m,n,hourly) if n<=cap else float('nan')):>9.1f}"
                      if n<=cap else f"{'--':>9}" for n in (1,2,3,4,8,12))
        print(f"{m:<26}{('yes' if acc else 'NO'):>8}{v:>6.0f}k" + row)
    print("\n  Rows using the employed-runner rate: Cycle, On-foot, E-cart. The two 2W rows are")
    print("  priced at the gig active-hour rate because that is who rides them today.")

    print("\n"+"="*84); print("FULL CAMPUS COST PER ORDER: city leg to gate + intra-campus leg".center(84)); print("="*84)
    print(f"{'Configuration':<48}{'n=3':>9}{'n=4':>9}{'n=8':>9}{'n=12':>9}")
    print("-"*84)
    combos = [
      ("Rider enters campus, door-drop (petrol 2W)", "Petrol 2W (incumbent)", GIG_HR, DROP_MIN),
      ("Gate-drop -> cycle runner, room delivery",   "Cycle",                RUNNER_HR, DROP_MIN),
      ("Gate-drop -> on-foot runner, room delivery", "On-foot runner",       RUNNER_HR, DROP_MIN),
      ("Gate-drop -> e-cart runner, room delivery",  "E-cart, stationed",    RUNNER_HR, DROP_MIN),
      ("Gate-drop -> e-cart, block SHELF handoff",   "E-cart, stationed",    RUNNER_HR, SHELF_DROP),
    ]
    for lbl, mode, hr, dm in combos:
        cells = ""
        for n in (3,4,8,12):
            if n > MODES[mode][2]: cells += f"{'--':>9}"
            else:
                gate_trip = C.trip(C.GEOM["Type A campus, gate-drop"])
                c = GIG_HR*(gate_trip/60.0)/n + in_cluster_cost(mode,n,hr,dm)
                cells += f"{c:>9.1f}"
        print(f"{lbl:<48}{cells}")
    print("-"*84)
    print(f"{'BENCHMARK  standard 2-3 km residential zone':<48}{M.LAST_MILE:>9.1f}")
    print(f"{'BENCHMARK  Type A campus, rider door-drop':<48}{C.DOOR:>9.1f}")

    print("\n"+"="*84); print("WHAT THE FEE BUYS: institution-operated leg vs our own runner".center(84)); print("="*84)
    for n in (4,8,12):
        gate_trip = C.trip(C.GEOM["Type A campus, gate-drop"])
        city = GIG_HR*(gate_trip/60.0)/n
        own  = in_cluster_cost("E-cart, stationed", n, RUNNER_HR, SHELF_DROP)
        print(f"  n={n:<3} city leg Rs{city:>5.1f}  +  in-cluster Rs{own:>5.1f}  =  Rs{city+own:>5.1f}"
              f"   |  fee ceiling vs city benchmark Rs{M.LAST_MILE-city:>5.1f}")
    print("\n  The fee ceiling is what remains after the city leg. Anything the institution charges")
    print("  below that leaves us at or under the standard-zone cost structure.")

# ============================================================================
# THE UTILISATION RISK - where the employed-runner case actually breaks
# A gig rider costs nothing when idle. An EMPLOYED runner is paid for rostered hours
# whether volume arrives or not. So the runner's cost per order is set by daily campus
# volume, not by batch size. This is the trade-off the circuit view hides.
# ============================================================================
RUNNER_DAY = RUNNER_MO/RUNNER_D                      # Rs577/day fully loaded

def runner_cost_per_order(orders_day, runners=1):
    return RUNNER_DAY*runners/orders_day

def runner_capacity(orders_day, drops=8, mode="E-cart, stationed", drop_min=SHELF_DROP):
    """Orders one rostered runner can physically clear in a shift."""
    per_circuit = circuit_min(mode, drops, drop_min)
    return 60.0/per_circuit*drops*RUNNER_H

def breakeven_volume(mode="E-cart, stationed", drops=8, drop_min=SHELF_DROP):
    """Daily campus orders at which an employed runner matches the gig rider on the same leg."""
    gig_leg = in_cluster_cost(mode, drops, GIG_HR, drop_min)
    return RUNNER_DAY/gig_leg

if __name__ == "__main__":
    print("\n"+"="*84); print("UTILISATION RISK: the employed runner is paid whether volume arrives or not".center(84)); print("="*84)
    cap = runner_capacity(0)
    print(f"One rostered runner, {RUNNER_H:.0f}h shift, e-cart + shelf handoff, batches of 8")
    print(f"  circuit time {circuit_min('E-cart, stationed',8,SHELF_DROP):.1f} min -> physical capacity "
          f"{cap:,.0f} orders/shift")
    print(f"  fully loaded cost Rs{RUNNER_DAY:.0f}/day\n")
    print(f"{'Campus orders/day':>18}{'runner Rs/order':>18}{'utilisation':>14}{'vs gig on same leg':>22}")
    print("-"*84)
    gig_leg = in_cluster_cost("E-cart, stationed", 8, GIG_HR, SHELF_DROP)
    for od in (20, 50, 100, 150, 200, 300, 500):
        cpo = runner_cost_per_order(od)
        print(f"{od:>18,}{cpo:>18.1f}{od/cap:>13.0%}{('cheaper' if cpo<gig_leg else 'WORSE'):>22}")
    print("-"*84)
    print(f"Gig rider on the same in-cluster leg: Rs{gig_leg:.1f}/order (no idle cost)")
    print(f">>> BREAKEVEN VOLUME: Rs{RUNNER_DAY:.0f}/day / Rs{gig_leg:.1f} = "
          f"{breakeven_volume():.0f} campus orders/day")
    print(f">>> Below that, an employed runner is more expensive than a gig rider doing the same job.")
    print(f">>> Round 1's minimum viable cluster is {7778:,} residents at 0.18 orders/resident/day")
    print(f"    = {7778*0.18:,.0f} orders/day, which clears the runner breakeven "
          f"{7778*0.18/breakeven_volume():.0f}x over.")
    print(f">>> But in BREAK MODE, campus volume collapses. The runner roster must collapse with it,")
    print(f"    which is exactly what Round 1's Calendar-Linked Labour Share (>=50%) metric measures.")
