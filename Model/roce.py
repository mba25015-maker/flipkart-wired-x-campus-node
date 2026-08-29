"""
S30  RETURN ON CAPITAL EMPLOYED — breakeven and an external return benchmark.

WHY THIS MODULE EXISTS. Everything upstream solves for BREAKEVEN: the AOV at which the node
stops losing money (Rs580). Eternal has publicly stated a ROCE benchmark "north of 40%"
[T1, earnings call Jan 2026]. This is an external comparator, not a disclosed Flipkart target.
A node that clears Rs580 earns exactly zero, so this module separately reports the basket needed
for breakeven and the basket implied by the external return benchmark.

THE DECOMPOSITION THAT CONNECTS THIS TO THE MONEYSHOT (DuPont):

    ROCE  =  EBIT / CE  =  (EBIT / NOV)  x  (NOV / CE)
                            ---------        --------
                            margin leg       turnover leg

The turnover leg contains the 0.944 comparison: campus asset turn against a city store's. The
margin leg is where AOV enters. The DuPont identity therefore connects throughput, basket mix and
capital employed without treating another operator's benchmark as a Flipkart commitment.

WHAT IS SOLVED AND WHAT IS ASSUMED, stated up front:
  SOLVED     AOV at which ROCE = 40%; AOV at which ROCE = 0 (reproduces Rs580 as a check);
             payback months; the margin the turnover leg implies.
  SOURCED    take rate, cost lines, fixed base, capex band, NWC days, tax rate, node life anchor.
  ASSUMED    ramp shape inside the 3-month implementation cap (linear, flagged, and the IRR is
             reported across the range rather than at a point).

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import numpy as np
import campus_model as M, cost_stack as CS, sla as SL, break_mode as B, working_capital as WC

# ---------------- SOURCED INPUTS ----------------
TAX_RATE      = 0.2517   # T1  Indian statutory corporate rate, 22% + surcharge + cess
ROCE_HURDLE   = M.ROCE_TARGET          # T1  Eternal earnings call Jan 2026, "north of 40%"
NODE_LIFE_MO  = 60                     # D   5 years, anchored on JPM's 56-month franchised-store
                                       #     payback: a node must outlive its own payback [T1]
RAMP_MONTHS   = 3                      # A   the case's own implementation cap; linear ramp
CAPEX_MID     = (M.CAPEX_LO + M.CAPEX_HI) / 2          # T2  Rs2.35 cr
LAST_MILE_D2  = SL.volume_weighted()[1]                # D   Rs19.0/order, D2 circuit model
RESIDUAL_SHARE = B.threshold(B.CONFIGS[-1][1])         # D   48.6%, the REPURPOSE fill rate

# BASIS, AND THIS MATTERS ENOUGH TO BE A CONSTANT RATHER THAN A DEFAULT ARGUMENT.
# The Rs580 spine is quoted TERM-ONLY: fixed base carried across twelve months, contribution
# earned across 8.5. Running the same arithmetic on the REPURPOSE configuration (break-period
# orders at r = 48.6%) gives a LOWER breakeven, because the node is earning through the break.
# Both are true; they are different configurations. The deck's headline is the term-only one,
# so that is the default here, and the repurpose case is reported as the upside it is.
BASIS_R = 0.0

DAYS_TERM  = 365 * M.ACTIVE_MONTHS / 12                # 258.5 active days
DAYS_BREAK = 365 - DAYS_TERM                           # 106.5 break days

# ---------------- THE P&L, PER ORDER AND PER YEAR ----------------
def cm_order(aov):
    """Contribution per order on the D2-consistent last-mile basis. Same stack as campus_model,
    with LAST_MILE replaced by the circuit model's volume-weighted figure."""
    return M.TAKE_RATE*aov - (LAST_MILE_D2 + M.STORE_OPS + M.PACKAGING + M.RESIDUAL)

def orders_year(v=M.CEILING, r=BASIS_R):
    """Annual orders on the REPURPOSE configuration: term volume through the term, r x term
    volume through the break. The node never closes, which is the S1 decision."""
    return v*DAYS_TERM + r*v*DAYS_BREAK

def nov_year(aov, v=M.CEILING, r=BASIS_R):
    return orders_year(v, r) * aov

def ebit_year(aov, v=M.CEILING, r=BASIS_R, fixed=CS.CAMPUS_FIXED):
    """EBIT = contribution on every order the node fills, less twelve months of fixed base.
    The fixed base does not stop in the break -- that is the whole D1 problem."""
    return cm_order(aov)*orders_year(v, r) - fixed*12

# ---------------- CAPITAL EMPLOYED ----------------
# Two constructions, because the working-capital sign is itself a finding [S22].
CE_STATES = {
    "capex + NWC (Eternal 14 days)":  CAPEX_MID + WC.WC_ADOPTED,
    "capex + NWC (12-day target)":    CAPEX_MID + WC.WC_TARGET,
    "capex only (supplier-funded)":   CAPEX_MID,
}
CE_BASE = CE_STATES["capex + NWC (Eternal 14 days)"]

def roce(aov, ce=None, v=M.CEILING, r=BASIS_R, post_tax=False):
    ce = CE_BASE if ce is None else ce
    e = ebit_year(aov, v, r)
    return (e*(1-TAX_RATE) if post_tax else e) / ce

# ---------------- THE DUPONT DECOMPOSITION ----------------
def dupont(aov, ce=None, v=M.CEILING, r=BASIS_R):
    """ROCE = EBIT margin x capital turnover. Returns both legs and their product."""
    ce = CE_BASE if ce is None else ce
    nov = nov_year(aov, v, r)
    margin, turn = ebit_year(aov, v, r)/nov, nov/ce
    return {"ebit_margin": margin, "capital_turn": turn, "roce": margin*turn}

# ---------------- SOLVING FOR THE AOV, NOT ASSUMING IT ----------------
# ROCE is linear in AOV (EBIT is linear in AOV, CE does not depend on it), so the AOV that hits
# any target return is closed-form. No search, no simulation.
#
#   ROCE = [ tau*AOV - c ] * N / CE  -  F*12/CE
#   ->  AOV* = ( ROCE_target*CE + F*12 ) / (tau*N) + c/tau
def aov_for_roce(target, ce=None, v=M.CEILING, r=BASIS_R, fixed=CS.CAMPUS_FIXED):
    ce = CE_BASE if ce is None else ce
    n = orders_year(v, r)
    c = LAST_MILE_D2 + M.STORE_OPS + M.PACKAGING + M.RESIDUAL
    return (target*ce + fixed*12) / (M.TAKE_RATE*n) + c/M.TAKE_RATE

AOV_BREAKEVEN = aov_for_roce(0.0)                      # reproduces the Rs580 spine as a check
# Ties to the spine within Rs2.5, and the residual gap is a DAY-COUNT convention rather than a
# disagreement: this module runs a 365-day year (365 x 8.5/12 = 258.5 active days), the spine runs
# 12 x 30-day months (255.0 days). 3.5 more active days = Rs2.14 lower breakeven. Stated, not
# smoothed, and asserted so it can never drift further without failing the audit.
SPINE_BREAKEVEN = CS.breakeven_d2_consistent(CS.CAMPUS_FIXED, LAST_MILE_D2)
DAYCOUNT_GAP = SPINE_BREAKEVEN - AOV_BREAKEVEN
BREAKEVEN_TIES_TO_SPINE = abs(DAYCOUNT_GAP) < 2.5

# THE REPURPOSE UPSIDE, priced. Filling 48.6% of term volume through the break from adjacent
# catchment is worth this much AOV -- the demand-side lever expressed in the same unit as the
# basket lever, which is the only way to compare them.
AOV_BREAKEVEN_REPURPOSE = aov_for_roce(0.0, r=RESIDUAL_SHARE)
REPURPOSE_WORTH_AOV     = AOV_BREAKEVEN - AOV_BREAKEVEN_REPURPOSE
AOV_HURDLE    = aov_for_roce(ROCE_HURDLE)              # AOV implied by Eternal's benchmark
AOV_HURDLE_POSTTAX = aov_for_roce(ROCE_HURDLE/(1-TAX_RATE))
HURDLE_PREMIUM = AOV_HURDLE - AOV_BREAKEVEN

# ---------------- PAYBACK AND IRR ----------------
def monthly_ebitda(aov, v=M.CEILING, r=BASIS_R):
    return ebit_year(aov, v, r)/12.0

def payback_months(aov, ce=None):
    ce = CAPEX_MID if ce is None else ce
    m = monthly_ebitda(aov)
    return np.inf if m <= 0 else ce/m

def irr(aov, life_mo=NODE_LIFE_MO, ramp=RAMP_MONTHS, ce=None):
    """Monthly IRR annualised. Month 0: capital out. Ramp: linear to full volume over `ramp`
    months, which is the case's own 3-month implementation cap [A]. No terminal value --
    a node that only works with a terminal value does not work."""
    ce = CE_BASE if ce is None else ce
    flows = [-ce]
    full = monthly_ebitda(aov)
    for m in range(1, life_mo+1):
        flows.append(full * min(1.0, m/ramp))
    r_lo, r_hi = -0.99, 5.0
    for _ in range(200):                                # bisection on NPV(monthly rate)
        mid = (r_lo+r_hi)/2
        npv = sum(f/(1+mid)**i for i, f in enumerate(flows))
        if npv > 0: r_lo = mid
        else: r_hi = mid
    return (1+r_lo)**12 - 1

def npv(aov, rate_annual, life_mo=NODE_LIFE_MO, ramp=RAMP_MONTHS, ce=None):
    ce = CE_BASE if ce is None else ce
    rm = (1+rate_annual)**(1/12) - 1
    full = monthly_ebitda(aov)
    return -ce + sum(full*min(1.0, m/ramp)/(1+rm)**m for m in range(1, life_mo+1))

# ---------------- SCENARIOS ----------------
# Three, using inputs already priced elsewhere in the model. Nothing new is assumed here.
import basket as BK
AOV_BASE  = AOV_BREAKEVEN                                   # the plan as underwritten
AOV_UP    = BK.SLOPE*BK.NONGROCERY_CEILING_LO + BK.INTERCEPT # 30% floor of Swiggy's disclosed range
AOV_MAX   = BK.SLOPE*BK.NONGROCERY_CEILING + BK.INTERCEPT    # 40% top of Swiggy's disclosed range
VOL_SHOCK = 0.70                                             # the -30% register item

SCENARIOS = [
    ("Underwritten  (AOV at breakeven)",        AOV_BASE, 1.00),
    ("Basket at 30% non-grocery",               AOV_UP,   1.00),
    ("Basket at 40% non-grocery",               AOV_MAX,  1.00),
    ("Basket at 30%, volume -30%",              AOV_UP,   VOL_SHOCK),
]

def scenario_rows():
    out = []
    for name, aov, vmul in SCENARIOS:
        v = M.CEILING*vmul
        d = dupont(aov, v=v)
        out.append(dict(name=name, aov=aov, volume=v,
                        ebit=ebit_year(aov, v), nov=nov_year(aov, v),
                        margin=d["ebit_margin"], turn=d["capital_turn"], roce=d["roce"],
                        roce_post=roce(aov, v=v, post_tax=True),
                        payback=payback_months(aov) if vmul == 1.0 else CAPEX_MID/max(monthly_ebitda(aov, v),1e-9),
                        irr=irr(aov) if vmul == 1.0 else np.nan))
    return out

# ---------------- THE EXTERNAL BENCHMARK, CHECKED AGAINST THE BASKET ----------------
HURDLE_INSIDE_CEILING = AOV_HURDLE <= AOV_MAX
HURDLE_NONGROCERY_SHARE = (AOV_HURDLE - BK.INTERCEPT)/BK.SLOPE     # share of GOV implied
HURDLE_HEADROOM_PTS = BK.NONGROCERY_CEILING - HURDLE_NONGROCERY_SHARE

# ---------------- RECONCILING TWO ASSET TURNS ----------------
# Slide 4 quotes campus asset turn 6.93x and the ratio 0.944. This module's turnover leg is a
# larger number, and both are right, because they are different quantities:
#
#   SLIDE 4      T = q x AOV_common x 365 x (m/12) / CAPEX      like-for-like COMPARISON,
#                both stores valued at the SAME AOV (Rs450) so the ratio isolates density x calendar
#   ROCE LEG     T = NOV_actual / CAPITAL EMPLOYED               the node's OWN turnover, at its own
#                achieved AOV, on capital that includes working capital
#
# Quoting either without its basis is how a panel finds a contradiction that is not there.
def turn_like_for_like(aov=M.MINUTES_AOV, opd=M.CEILING, months=M.ACTIVE_MONTHS):
    return opd*aov*(365*months/12)/CAPEX_MID

TURN_SLIDE4      = turn_like_for_like()                  # 6.93x, the slide-4 quantity
TURN_ROCE_LEG    = None                                  # set after AOV_HURDLE is known

W = 88
def report():
    print("\n" + "="*W); print("S30  RETURN ON CAPITAL — BREAKEVEN VS EXTERNAL BENCHMARK".center(W)); print("="*W)
    print(f"  Capital employed, base case      Rs{CE_BASE/1e5:,.1f} lakh"
          f"   (capex Rs{CAPEX_MID/1e5:,.1f} L + NWC Rs{WC.WC_ADOPTED/1e5:,.1f} L)")
    for k, v in CE_STATES.items():
        print(f"    {k:<34} Rs{v/1e5:>8,.1f} lakh")
    print(f"  Orders per year (REPURPOSE, r={RESIDUAL_SHARE:.1%})   {orders_year():,.0f}")
    print(f"  External benchmark [T1, Eternal, Jan 2026]   ROCE north of {ROCE_HURDLE:.0%}")
    print()
    print("-"*W); print("  THE TWO AOVs — BREAKEVEN AND AN EXTERNAL RETURN BENCHMARK"); print("-"*W)
    print(f"    AOV for ROCE = 0   (breakeven)              Rs{AOV_BREAKEVEN:,.0f}"
          f"   <- reproduces the D1/D2 spine")
    print(f"    AOV for ROCE = {ROCE_HURDLE:.0%}  (Eternal benchmark)     Rs{AOV_HURDLE:,.0f}"
          f"   <- premium of Rs{HURDLE_PREMIUM:,.0f}")
    print(f"    AOV for {ROCE_HURDLE:.0%} POST-TAX at {TAX_RATE:.2%}              Rs{AOV_HURDLE_POSTTAX:,.0f}")
    print(f"    Non-grocery share of GOV implied by benchmark    {HURDLE_NONGROCERY_SHARE:.1f}%"
          f"   (Swiggy range max {BK.NONGROCERY_CEILING:.0f}%, headroom {HURDLE_HEADROOM_PTS:+.1f} pts)")
    print(f"    >>> The benchmark-implied mix is {'WITHIN' if HURDLE_INSIDE_CEILING else 'OUTSIDE'} "
          f"Swiggy's disclosed {BK.NONGROCERY_CEILING_LO:.0f}-{BK.NONGROCERY_CEILING:.0f}% range.")
    print("        Cross-operator reference only; not a Flipkart target or commitment.")
    print()
    print("-"*W); print("  DUPONT — MARGIN AND TURNOVER LEGS OF THE IDENTITY"); print("-"*W)
    d = dupont(AOV_HURDLE)
    print(f"    ROCE = EBIT margin x capital turnover")
    print(f"         = {d['ebit_margin']:.2%}  x  {d['capital_turn']:.2f}x  =  {d['roce']:.1%}   at AOV Rs{AOV_HURDLE:,.0f}")
    print(f"    Capital turnover on capex alone            {nov_year(AOV_HURDLE)/CAPEX_MID:.2f}x")
    print()
    print(f"    RECONCILING THE TWO ASSET TURNS — different quantities, both correct:")
    print(f"      slide 4, like-for-like at a COMMON AOV Rs{M.MINUTES_AOV:.0f}      {TURN_SLIDE4:.2f}x"
          f"   ratio to city {M.TURN_RATIO:.3f}")
    print(f"      here, the node's OWN turnover at AOV Rs{AOV_HURDLE:,.0f} on CE   {dupont(AOV_HURDLE)['capital_turn']:.2f}x")
    print(f"      the first isolates density x calendar; the second is the DuPont leg. Quote the basis.")
    print(f"    Margin required at this turnover for {ROCE_HURDLE:.0%}   {ROCE_HURDLE/d['capital_turn']:.2%}")
    print()
    print("-"*W); print("  SCENARIOS"); print("-"*W)
    print(f"  {'scenario':<34}{'AOV':>7}{'orders/d':>10}{'EBIT Rs L':>11}{'margin':>9}{'turn':>7}{'ROCE':>8}{'payback mo':>12}")
    for r_ in scenario_rows():
        pb = "n/a" if not np.isfinite(r_['payback']) else f"{r_['payback']:.0f}"
        print(f"  {r_['name']:<34}{r_['aov']:>7,.0f}{r_['volume']:>10,.0f}{r_['ebit']/1e5:>11,.1f}"
              f"{r_['margin']:>9.2%}{r_['turn']:>7.2f}{r_['roce']:>8.1%}{pb:>12}")
    print()
    print(f"  IRR at the benchmark AOV, {NODE_LIFE_MO//12}-year life, {RAMP_MONTHS}-month linear ramp [A]"
          f"    {irr(AOV_HURDLE):.1%}")
    print(f"  IRR sensitivity to the ramp        2 mo {irr(AOV_HURDLE, ramp=2):.1%}"
          f"   |  3 mo {irr(AOV_HURDLE, ramp=3):.1%}   |  6 mo {irr(AOV_HURDLE, ramp=6):.1%}")
    print(f"  NPV at 12% / 15% [A, no WACC is disclosed]   "
          f"Rs{npv(AOV_HURDLE,0.12)/1e5:,.1f} L  /  Rs{npv(AOV_HURDLE,0.15)/1e5:,.1f} L")
    print(f"  Node life anchored on JPM's {M.FRANCHISE_PAYBACK}-month franchised-store payback [T1]")
    print()
    print("-"*W); print("  THE REPURPOSE LEVER, IN THE SAME UNIT AS THE BASKET LEVER"); print("-"*W)
    print(f"    breakeven AOV, term-only basis                         Rs{AOV_BREAKEVEN:,.0f}")
    print(f"    breakeven AOV, REPURPOSE at r={RESIDUAL_SHARE:.1%}                  Rs{AOV_BREAKEVEN_REPURPOSE:,.0f}")
    print(f"    >>> filling the break from adjacent catchment is worth Rs{REPURPOSE_WORTH_AOV:,.0f} of AOV.")
    print(f"        The site filter and the basket lever are therefore SUBSTITUTES at the margin,")
    print(f"        and the site filter is the cheaper of the two to buy.")
    print()
    print("-"*W); print("  INTERPRETATION AND SOURCE BOUNDARY"); print("-"*W)
    print(f"    At Rs{AOV_BREAKEVEN:,.0f} AOV, modeled EBIT is zero on Rs{CE_BASE/1e5:,.1f} lakh of capital employed.")
    print(f"    A {ROCE_HURDLE:.0%} ROCE benchmark requires Rs{AOV_HURDLE:,.0f} AOV, implying approximately")
    print(f"    {HURDLE_NONGROCERY_SHARE:.1f}% non-grocery share versus Minutes' estimated {BK.MINUTES_NONGROCERY:.0f}%.")
    print(f"    The required mix falls within Swiggy's disclosed {BK.NONGROCERY_CEILING_LO:.0f}-{BK.NONGROCERY_CEILING:.0f}% range.")
    print("    Both comparisons are cross-operator references, not Flipkart targets or commitments.")

if __name__ == "__main__":
    report()
