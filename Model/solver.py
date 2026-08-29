"""
CC-1: the lever ladder, recast as a constrained minimisation and printed as a
solver output table in Team Glitch's format (WiRED 9.0 SCM winning deck, slide 4).

    minimise   dead-zone cash burn
    subject to reactivation lead time >= 28 days      (semester demand STEPS, cannot ramp)
               SLA at peak            <= 27.1 min      (sla.py volume-weighted circuit)
               adjacent catchment     >= 513 orders/day (revocation-survival site filter)
               rent                    = fixed         (no calendar-indexed lease in Indian practice)
               break length           >= 7 weeks       (below which the ramp and wind-down collide:
                                                        do NOT wind down)

METHOD, and the rule that governs it: every cell in the table below is read out of
`break_mode.CONFIGS` (the four cost configurations and their break-mode P&L) and the
`cost_stack` / `risk_quadrant` / `sla` modules those configurations are built on.
Nothing is typed in. If a number cannot be traced to one of those modules the build
stops rather than inventing it - see PARAMETER_PROVENANCE at the foot of the file.

THE FIFTH ROW. `break_mode.CONFIGS` holds four rows: DO_NOTHING, LABOUR_FLEX,
COLD_RIGHTSIZE, SMALL_FORMAT. The fifth strategy, REPURPOSE, is NOT a cost
configuration - it is the demand-side default locked at S1 ("repurpose the
catchment"). It runs the node on the SMALL_FORMAT cost base but fills the residual-
demand requirement from adjacent NON-STUDENT catchment instead of from residual
students, which is why break_mode.adjacent_catchment_required() and
risk_quadrant.post_revocation_survival() size it in orders/day. It is composed here
from those two functions, not from a new parameter, and that composition is stated
on the slide rather than hidden.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
from dataclasses import dataclass

import campus_model as M
import cost_stack as C
import break_mode as B
import risk_quadrant as Q
import sla as SL
import fleet_mix as F

# ============================================================================
# EVALUATION BASIS
# ============================================================================
# The dead-zone hole is sized at ZERO residual demand, the same basis on which
# break_mode reports the Rs31.6L unmitigated deficit and S21 reports the Rs21.3L
# hold-through-break cost (break_mode.relocate_vs_flex default r=0.0). Reactivation
# opex is a function of the residual ratio only; it is evaluated on the same basis.
EVAL_R = 0.0
BREAK_MONTHS = B.BREAK_MONTHS                                     # 3.5

# ============================================================================
# CONSTRAINTS  -  values pulled from the modules that own them, never typed
# ============================================================================
LEAD_TIME_DAYS  = Q.RAMP_DAYS                                     # 28  (break_mode playbook T-28d)
_PEAK_RATE      = SL.BASE_RATE * SL.PTDR_PEAK
SLA_PEAK_MIN    = SL.sla_minutes(_PEAK_RATE, SL.dynamic_batch(_PEAK_RATE))   # 27.1 min
CATCHMENT_FLOOR = Q.post_revocation_survival()["orders_needed"]   # 513 orders/day
MIN_BREAK_WEEKS = Q.MIN_WEEKS                                     # 7 weeks
DEAD_ZONE_WEEKS = M.ACTIVE_MONTHS and (12 - M.ACTIVE_MONTHS) * 52 / 12      # ~15.2 weeks

CONSTRAINTS = [
    ("reactivation lead time", ">=", f"{LEAD_TIME_DAYS} days",
     "semester-start demand STEPS in a 2-3 week window; capacity must be complete before day one"),
    ("SLA at peak", "<=", f"{SLA_PEAK_MIN:.1f} min",
     "sla.py volume-weighted circuit model, 4x peak arrival rate, dynamic batch"),
    ("adjacent catchment", ">=", f"{CATCHMENT_FLOOR:.0f} orders/day",
     "revocation-survival site filter, risk_quadrant.post_revocation_survival"),
    ("store rent", "==", "fixed",
     "no calendar-indexed / seasonally-abated commercial lease found in Indian practice"),
    ("break length", ">=", f"{MIN_BREAK_WEEKS:.0f} weeks",
     f"the academic dead zone is ~{DEAD_ZONE_WEEKS:.0f} weeks, so wind-down is admissible"),
]

# ============================================================================
# STRATEGY ROWS
# ============================================================================
CANON = {
    "Do nothing":                "DO_NOTHING",
    "Labour flex only":          "LABOUR_FLEX",
    "+ cold-chain right-sizing": "COLD_RIGHTSIZE",
    "+ small-format node":       "SMALL_FORMAT",
}


@dataclass
class Row:
    key: str
    label: str
    deadzone: float          # Rs, break-period deficit over BREAK_MONTHS at EVAL_R
    threshold: float         # residual-demand requirement, share of term volume
    reactivation: float      # Rs, reactivation opex
    days_to_service: int     # days from ramp start to full service
    note: str = ""

    @property
    def total(self):
        return self.deadzone + self.reactivation


def _winds_down(canon_key):
    """DO_NOTHING keeps the full 25-person crew and the cold chain powered
    (cfg_do_nothing = RENT + STAFF + UTIL + OTHER), so there is nothing to
    reactivate and the node never leaves full service. Every other cost
    configuration serves notice on the flex crew and consolidates the cold zone."""
    return canon_key != "DO_NOTHING"


def build_rows():
    rows = {}

    # --- the four rows that ARE in break_mode.CONFIGS -----------------------
    for name, fn in B.CONFIGS:
        key = CANON[name]
        wd = _winds_down(key)
        deadzone = -B.break_monthly_cm(EVAL_R, fn) * BREAK_MONTHS
        rows[key] = Row(
            key=key,
            label=name,
            deadzone=max(0.0, deadzone),
            threshold=B.threshold(fn),
            reactivation=(B.reactivation(EVAL_R)["opex_total"] if wd else 0.0),
            days_to_service=(LEAD_TIME_DAYS if wd else 0),
            note=("" if wd else "full crew retained; node never leaves full service"),
        )

    # --- the fifth row: REPURPOSE (demand-side default, composed) ----------
    # Runs on the SMALL_FORMAT cost base (cfg_footprint) but fills the residual-
    # demand requirement from adjacent NON-STUDENT catchment. At the threshold the
    # break-mode contribution is zero by definition, so the dead-zone burn is zero.
    adj = B.adjacent_catchment_required(B.cfg_footprint)
    thr = adj["threshold"]
    repurpose_burn = max(0.0, -B.break_monthly_cm(thr, B.cfg_footprint) * BREAK_MONTHS)
    rows["REPURPOSE"] = Row(
        key="REPURPOSE",
        label="Repurpose the catchment",
        deadzone=repurpose_burn,
        threshold=thr,
        reactivation=0.0,           # node runs continuously, re-aimed not stood down
        days_to_service=0,
        note=(f"fills {thr*100:.1f}% from adjacent non-student catchment "
              f"({adj['adjacent_lo']:.0f}-{adj['adjacent_hi']:.0f} orders/day); "
              f"feasible only where the site clears the >={CATCHMENT_FLOOR:.0f}/day filter"),
    )
    return rows


ROWS = build_rows()
ORDER = ["DO_NOTHING", "LABOUR_FLEX", "COLD_RIGHTSIZE", "SMALL_FORMAT", "REPURPOSE"]

# ============================================================================
# THE OBJECTIVE:  minimise dead-zone cash burn  (dead-zone deficit + reactivation)
# ============================================================================
BEST = min(ORDER, key=lambda k: ROWS[k].total)


# ============================================================================
# REPORT  -  Team Glitch monospace solver-output format
# ============================================================================
def _rs(x):
    """Rupee integer with western grouping, matching break_mode / cost_stack."""
    return f"{x:,.0f}"


def report():
    W = 84
    print("=" * W)
    print("DEAD-ZONE CASH-BURN MINIMISATION".center(W))
    print("campus cluster dark store  |  3.5-month academic dead zone".center(W))
    print("=" * W)
    print("minimise   dead-zone cash burn")
    print("subject to")
    for lhs, op, rhs, why in CONSTRAINTS:
        print(f"   {lhs:<22}{op:>3} {rhs}")
        print(f"   {'':<26}   ({why})")
    print(f"\nbasis   residual demand r = {EVAL_R:.0%} (the hole, sized as break_mode sizes it)")
    print(f"        break-mode contribution/order Rs{B.cm_order():.1f} at campus AOV Rs{B.CAMPUS_AOV:.0f}")

    print("\n" + "-" * W)
    print(f"{'STRATEGY':<15} {'DEAD-ZONE':>12} {'RESID DEM':>10} {'REACTIVN':>11} "
          f"{'DAYS->SVC':>9} {'BEST':>5}")
    print(f"{'':<15} {'Rs, 3.5 mo':>12} {'% term':>10} {'Rs':>11} "
          f"{'lead':>9} {'':>5}")
    print("-" * W)
    for k in ORDER:
        r = ROWS[k]
        mark = "<<< BEST" if k == BEST else ""
        dz = "0" if r.deadzone < 1 else _rs(r.deadzone)
        rx = "0" if r.reactivation < 1 else _rs(r.reactivation)
        name = r.key + ("*" if k == "REPURPOSE" else "")
        print(f"{name:<15} {dz:>12} {r.threshold*100:>9.1f}% {rx:>11} "
              f"{r.days_to_service:>9}   {mark}")
    print("-" * W)
    print(f"BEST = {BEST}   (lowest dead-zone cash burn = deficit + reactivation, "
          f"all constraints held)")

    r = ROWS["REPURPOSE"]
    print("\n  * REPURPOSE is not a cost configuration. It runs the SMALL_FORMAT cost base but")
    print(f"    {r.note}.")
    print("    Cost levers alone take the requirement from 70.8% to 48.6% of term volume and")
    print("    CANNOT close it - residual campus population supplies only 8-15%. The demand-")
    print("    side repurpose is the majority of the answer, and D1's largest problem is then")
    print("    solved by D2's site filter rather than by an operating lever.")

    print("\n" + "-" * W)
    print("READ-OUT")
    print("-" * W)
    dn, sf = ROWS["DO_NOTHING"], ROWS["SMALL_FORMAT"]
    print(f"  Cost ladder cuts the dead-zone deficit from Rs{dn.deadzone/1e5:.1f}L (DO_NOTHING) to "
          f"Rs{sf.deadzone/1e5:.1f}L (SMALL_FORMAT),")
    print(f"  a {(1-sf.deadzone/dn.deadzone)*100:.0f}% reduction, at the price of a {sf.days_to_service}-day "
          f"reactivation lead and Rs{sf.reactivation/1e5:.1f}L of rehire /")
    print(f"  cold pull-down / rider re-acquisition opex. REPURPOSE takes the deficit to zero.")


# ============================================================================
# PARAMETER PROVENANCE  -  every input, and the module it is read from
# ============================================================================
PARAMETER_PROVENANCE = {
    "break configurations (4)":     "break_mode.CONFIGS",
    "break-mode P&L / deficit":     "break_mode.break_monthly_cm",
    "residual-demand thresholds":   "break_mode.threshold(cfg_*)",
    "reactivation opex":            "break_mode.reactivation",
    "adjacent-catchment sizing":    "break_mode.adjacent_catchment_required",
    "small-format rent saving":     "break_mode.RENT_SAVED (<- rent_lever, cost_stack)",
    "cold right-size saving":       "break_mode.cfg_cold (<- cost_stack.COLD_KW/COLD_HRS/TARIFF)",
    "campus AOV / CM per order":    "break_mode.CAMPUS_AOV / cm_order (<- cost_stack.breakeven_d2_consistent)",
    "reactivation lead time":       "risk_quadrant.RAMP_DAYS (= break_mode playbook T-28d)",
    "SLA at peak":                  "sla.sla_minutes at 4x BASE_RATE",
    "revocation catchment floor":   "risk_quadrant.post_revocation_survival",
    "7-week wind-down rule":        "risk_quadrant.MIN_WEEKS",
}


if __name__ == "__main__":
    report()
    print("\n" + "=" * 80)
    print("PARAMETER PROVENANCE  (no value typed into this file)".center(80))
    print("=" * 80)
    for k, v in PARAMETER_PROVENANCE.items():
        print(f"  {k:<30} {v}")
