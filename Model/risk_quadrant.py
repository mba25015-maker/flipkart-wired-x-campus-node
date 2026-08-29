"""
Closing the last two S10 findings: quadrant differentiation, and a priced risk register.

Round 1 produced a four-quadrant posture map and S1 recorded that D1's playbook and D2's
fulfilment archetype should differ by quadrant. The semi-final work built ONE playbook and ONE
fulfilment model, which is exactly the one-size design the brief warns against. Fixed here.
"""
import campus_model as M, cost_stack as C, fleet_mix as F, break_mode as B, sla as SL, rent_lever as R

# ============================================================================
# QUADRANT-DIFFERENTIATED PLAYBOOK
# ============================================================================
QUADRANTS = [
 # name, posture, D1 cost-mitigation, D2 fulfilment archetype, SLA tier set
 ("Priority\n(dense + affluent)", "Build standalone",
  "Full playbook: labour flex, cold right-size, footprint discipline, long lock-in discount",
  "In-campus node + institution-operated leg, e-cart, shelf handoff",
  "All four tiers"),
 ("Dense, low spend", "Bounded ecosystem bet, pre-committed kill trigger",
  "Minimum capex: NO in-campus node, no cold chain beyond chilled, short lease accepted at a premium",
  "Gate-drop only. Rider to gate, customer collects. No institutional partnership to fund.",
  "Standard + Shelf hold only"),
 ("Affluent, fragmented", "Serve from existing city store - do not build",
  "Not applicable. We never take the campus fixed cost, so there is nothing to flex.",
  "Incremental gate-drop from the existing node, batched with residential volume",
  "Standard only"),
 ("Sub-scale", "Do not serve", "-", "-", "-"),
]

# ============================================================================
# BREAK-LENGTH CONDITIONAL TRIGGER
# ============================================================================
RAMP_DAYS, WINDDOWN_DAYS = 28, 21
def winddown_rule(break_weeks):
    usable = break_weeks*7 - RAMP_DAYS - WINDDOWN_DAYS
    if usable <= 0:  return "HOLD - do not wind down", usable
    if usable < 21:  return "PARTIAL - labour flex only", usable
    return "FULL playbook", usable
MIN_WEEKS = (RAMP_DAYS+WINDDOWN_DAYS)/7

# ============================================================================
# ACCESS REVOCATION, PRICED - and the hedge that already exists
# ============================================================================
LOCKIN_MO   = 30.0            # T2 midpoint of the 24-36 month warehouse lock-in band
CAPEX       = (M.CAPEX_LO+M.CAPEX_HI)/2
REDEPLOY    = 0.55            # A  racking, chillers, IT are movable; leasehold fit-out is not
CITY_AOV    = 700.0           # T2 Datum/Reuters blended AOV, used for a RESIDENTIAL catchment

def revocation_exposure(month_of_revocation=12.0):
    rent_left = (LOCKIN_MO-month_of_revocation)*C.JM_NONMETRO["rent"]
    stranded  = CAPEX*(1-REDEPLOY)
    return {"rent_left":rent_left, "stranded_capex":stranded, "total":rent_left+stranded}

def post_revocation_survival():
    """If access is revoked, can the node survive on the adjacent catchment alone?"""
    cm = M.cm_per_order(CITY_AOV, 3.0)
    need = C.JM_NONMETRO["total"]/30.0/cm
    adj  = B.adjacent_catchment_required()
    return {"cm_per_order":cm, "orders_needed":need,
            "adjacent_lo":adj["adjacent_lo"], "adjacent_hi":adj["adjacent_hi"]}

# ============================================================================
# GIG-WORKER LEVY, PRICED
# ============================================================================
# Parliamentary Standing Committee on Commerce, 201st report, 7 Aug 2026: social security fund
# of 1-2% of turnover, CAPPED at 5% of worker payments. [T1, committee report]
def gig_levy():
    rider_pay_mo = M.LAST_MILE*M.CEILING*30
    return {"rider_pay":rider_pay_mo, "cap_5pct":rider_pay_mo*0.05,
            "as_share_of_fixed": rider_pay_mo*0.05/C.JM_NONMETRO["total"]}

if __name__=="__main__":
    print("="*92); print("QUADRANT-DIFFERENTIATED PLAYBOOK".center(92)); print("="*92)
    for name,posture,d1,d2,tiers in QUADRANTS:
        print(f"\n{name.replace(chr(10),' ')}  ->  {posture}")
        print(f"   D1  {d1}")
        print(f"   D2  {d2}")
        print(f"   SLA {tiers}")
    print("\n>>> The load-bearing point: in the 'affluent fragmented' quadrant D1 does not apply at")
    print("    all, because we never take the campus fixed cost. A cost-mitigation model that")
    print("    assumes every campus needs mitigating has misread its own segmentation.")

    print("\n"+"="*92); print("BREAK-LENGTH CONDITIONAL TRIGGER".center(92)); print("="*92)
    print(f"Ramp-up {RAMP_DAYS}d + wind-down {WINDDOWN_DAYS}d = {RAMP_DAYS+WINDDOWN_DAYS}d of any break consumed by transition.")
    print(f"\n{'break length':>14}{'usable idle days':>19}{'rule':>32}")
    for wks in (2,4,6,7,8,10,15):
        rule,us = winddown_rule(wks)
        print(f"{f'{wks} weeks':>14}{max(0,us):>19}{rule:>32}")
    print(f"\n>>> Below {MIN_WEEKS:.0f} weeks the ramp and the wind-down collide and the correct action is to")
    print("    do NOTHING. India's '3-4 months of vacation' is an ANNUAL AGGREGATE fragmented into")
    print("    a long summer break plus a shorter winter break plus exam gaps. A playbook that")
    print("    always fires is less flexible than one that knows when not to.")

    print("\n"+"="*92); print("RISK REGISTER - priced where pricing is possible".center(92)); print("="*92)
    rv = revocation_exposure(); ps = post_revocation_survival(); gl = gig_levy()
    print(f"\n1. ACCESS REVOCATION (Gate 0) - the largest single risk in the plan")
    print(f"   Exposure if revoked at month 12 of a {LOCKIN_MO:.0f}-month lock-in:")
    print(f"     remaining rent obligation      Rs{rv['rent_left']:>12,.0f}")
    print(f"     stranded capex ({1-REDEPLOY:.0%} of Rs{CAPEX/1e7:.2f}cr)  Rs{rv['stranded_capex']:>12,.0f}")
    print(f"     TOTAL                          Rs{rv['total']:>12,.0f}  (Rs{rv['total']/1e5:.0f} lakh)")
    print(f"\n   THE HEDGE ALREADY EXISTS, and this is the convergence worth putting on a slide:")
    print(f"     post-revocation the node serves the adjacent catchment at residential AOV Rs{CITY_AOV:.0f}")
    print(f"     CM/order at that basket                 Rs{ps['cm_per_order']:.1f}")
    print(f"     orders/day needed to cover fixed cost   {ps['orders_needed']:.0f}")
    print(f"     adjacent catchment the SITE FILTER already requires  {ps['adjacent_lo']:.0f}-{ps['adjacent_hi']:.0f}/day")
    lo, hi, need = ps['adjacent_lo'], ps['adjacent_hi'], ps['orders_needed']
    print(f"\n   THE TWO THRESHOLDS CROSS, AND THAT TELLS US WHICH ONE BINDS:")
    print(f"     break-period solvency needs   {lo:.0f}-{hi:.0f} orders/day of adjacent catchment")
    print(f"     revocation survival needs     {need:.0f} orders/day")
    print(f"     -> at the LOW residual estimate ({lo:.0f}) the site clears break-period solvency but")
    print(f"        NOT revocation. At the HIGH estimate ({hi:.0f}) it clears both.")
    print(f"   >>> SET THE SITE FILTER AT THE HIGHER OF THE TWO: {max(hi,need):.0f} orders/day.")
    print(f"       REVOCATION RISK, NOT BREAK-PERIOD SOLVENCY, IS THE BINDING SITING CONSTRAINT.")
    print(f"       Worth noting how this emerged: the cost levers, by lowering the break-period")
    print(f"       requirement, WEAKENED the revocation hedge that the earlier draft claimed was")
    print(f"       automatic. Improving one number degraded another. That is the kind of coupling")
    print(f"       an audit surfaces and a slide deck hides.")
    print(f"\n2. GIG-WORKER SOCIAL SECURITY LEVY  [T1, Parl. Standing Cttee 201st report, 7 Aug 2026]")
    print(f"     rider payments per store/month  Rs{gl['rider_pay']:>12,.0f}")
    print(f"     levy at the 5%-of-worker-payments cap  Rs{gl['cap_5pct']:>7,.0f}/month")
    print(f"     as a share of the store fixed base      {gl['as_share_of_fixed']:.1%}")
    print(f"   >>> Material, not fatal. It lands on the leg we are shrinking, so the gate-drop")
    print(f"       design reduces exposure to it as a side effect.")
    print(f"\n3. VOLUME -30%          breakeven AOV Rs554 -> Rs621; wipes out the consolidation gain")
    print(f"4. BATCH DENSITY < n=3  SLA breaks before cost does; revert to Express tier and eat the cost")
    print(f"5. VOLUME < {F.breakeven_volume():.0f}/day     runner roster uneconomic; revert to gig riders at the gate")
    print(f"6. SHELF THEFT/SPOILAGE Indian public record contains NO consumer-forum ruling on gate-")
    print(f"                        handoff custody. Liability is unallocated - that ambiguity is the")
    print(f"                        argument for a logged, OTP-released chain of custody, not a gap.")
    print(f"7. BREAK FRAGMENTATION  handled by the conditional trigger above")
    print(f"8. PARTNER PERFORMANCE  institution-operated leg means service quality is not ours to")
    print(f"                        control; mitigated by per-parcel fee tied to an SLA, not a flat fee")
