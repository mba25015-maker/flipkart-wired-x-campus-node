"""PG ADJACENCY — a gated demand scenario, never a hidden base-case uplift.

The case names paying-guest accommodation, and cost_stack.py already prices two service
geometries. What the public evidence does not provide is the site-level demand denominator:
occupied student PG beds inside a node radius. This module adds the missing calculation without
pretending that denominator is known.

The operating rule is deliberately conservative:

* Phase-1 hostel volume remains the underwritten base case.
* PG orders enter only spare term capacity or available break-period capacity.
* Orders above the 1,400/day working ceiling are reported as overflow, not revenue.
* The published base case stays unchanged while params.PG_DEMAND_ENABLED is False.
* Financial outputs require an explicit PG AOV; no AOV is inferred from hostel demand.

TIERS: T1 disclosure/analyst | D derived | A sensitivity assumption | P pilot input
"""
from math import inf

import campus_model as M
import cost_stack as CS
import params as P
import roce as RC
import working_capital as WC

PG_ORDERS_PER_ACTIVE_USER_DAY = M.BLINKIT_FREQ / 30.0  # T1, 3.6/month; no captive-campus uplift
_COST = CS.segment_cpo()
PG_DOORSTEP_CPO = _COST["Type B urban PG cluster"]
PG_COMMON_DROP_CPO = _COST["Type B PG cluster, common-drop"]


def _share(value, name):
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def orders_day(occupied_student_beds, active_user_penetration,
               orders_per_active_user_day=PG_ORDERS_PER_ACTIVE_USER_DAY):
    """Daily PG orders from a VERIFIED occupied-student-bed count.

    Occupancy and student share are intentionally upstream of this function: the input is
    occupied STUDENT beds, so neither can be silently assumed inside the model.
    """
    beds = float(occupied_student_beds)
    if beds < 0:
        raise ValueError("occupied_student_beds cannot be negative")
    penetration = _share(active_user_penetration, "active_user_penetration")
    frequency = float(orders_per_active_user_day)
    if frequency < 0:
        raise ValueError("orders_per_active_user_day cannot be negative")
    return beds * penetration * frequency


def last_mile_cpo(common_drop_share):
    share = _share(common_drop_share, "common_drop_share")
    return (1.0 - share) * PG_DOORSTEP_CPO + share * PG_COMMON_DROP_CPO


def contribution_order(aov, common_drop_share, take_rate=M.TAKE_RATE):
    """PG contribution/order on the same store-cost basis as the campus model."""
    aov = float(aov)
    if aov <= 0:
        raise ValueError("aov must be positive for a financial scenario")
    return (take_rate * aov
            - (last_mile_cpo(common_drop_share) + M.STORE_OPS + M.PACKAGING + M.RESIDUAL))


def inputs_are_admissible(enabled=None, occupied_student_beds=None,
                          active_user_penetration=None, aov=None):
    """True only when the evidence gate and every demand/financial input are populated."""
    enabled = P.PG_DEMAND_ENABLED if enabled is None else bool(enabled)
    beds = P.PG_VERIFIED_OCCUPIED_STUDENT_BEDS if occupied_student_beds is None else occupied_student_beds
    penetration = P.PG_ACTIVE_USER_PENETRATION if active_user_penetration is None else active_user_penetration
    aov = P.PG_AOV if aov is None else aov
    return bool(enabled and beds > 0 and penetration > 0 and aov > 0)


def scenario(occupied_student_beds, active_user_penetration, *,
             hostel_term_opd=M.CEILING, common_drop_share=0.0,
             break_retention=0.0, pg_aov=None, hostel_aov=RC.AOV_UP):
    """Capacity- and finance-aware PG adjacency scenario.

    `break_retention` is the share of term PG orders that persists through the academic break.
    The function does not assume that PG residents remain: zero is the conservative default.
    """
    hostel_term_opd = float(hostel_term_opd)
    if hostel_term_opd < 0:
        raise ValueError("hostel_term_opd cannot be negative")
    common_drop_share = _share(common_drop_share, "common_drop_share")
    break_retention = _share(break_retention, "break_retention")

    gross = orders_day(occupied_student_beds, active_user_penetration)
    spare_term = max(0.0, P.CLUSTER_VOLUME - hostel_term_opd)
    term_served = min(gross, spare_term)
    term_overflow = max(0.0, gross - term_served)
    break_served = min(P.CLUSTER_VOLUME, gross * break_retention)
    annual_orders = term_served * RC.DAYS_TERM + break_served * RC.DAYS_BREAK

    out = {
        "occupied_student_beds": float(occupied_student_beds),
        "active_user_penetration": float(active_user_penetration),
        "orders_per_active_user_day": PG_ORDERS_PER_ACTIVE_USER_DAY,
        "gross_pg_opd": gross,
        "hostel_term_opd": hostel_term_opd,
        "spare_term_capacity": spare_term,
        "term_pg_served_opd": term_served,
        "term_pg_overflow_opd": term_overflow,
        "break_pg_served_opd": break_served,
        "annual_pg_orders": annual_orders,
        "common_drop_share": common_drop_share,
        "pg_last_mile_cpo": last_mile_cpo(common_drop_share),
        "pg_aov": pg_aov,
        "incremental_ebit": None,
        "incremental_nwc": None,
        "pro_forma_roce": None,
        "pro_forma_payback_months": None,
    }

    if pg_aov is not None:
        cm = contribution_order(pg_aov, common_drop_share)
        incremental_ebit = annual_orders * cm
        peak_incremental_opd = max(term_served, break_served)
        incremental_nwc = peak_incremental_opd * float(pg_aov) * WC.NOV_OVER_GOV * P.NWC_DAYS
        base_ebit = RC.ebit_year(hostel_aov, v=hostel_term_opd)
        pro_forma_ebit = base_ebit + incremental_ebit
        pro_forma_ce = RC.CE_BASE + incremental_nwc
        monthly_ebit = pro_forma_ebit / 12.0
        out.update({
            "pg_cm_order": cm,
            "incremental_ebit": incremental_ebit,
            "incremental_nwc": incremental_nwc,
            "pro_forma_roce": pro_forma_ebit / pro_forma_ce,
            "pro_forma_payback_months": inf if monthly_ebit <= 0 else RC.CAPEX_MID / monthly_ebit,
        })
    return out


def configured_scenario():
    """The scenario represented by params.py. It stays zero until the evidence gate opens."""
    if not inputs_are_admissible():
        return scenario(0, 0, hostel_term_opd=P.PG_HOSTEL_TERM_OPD)
    return scenario(P.PG_VERIFIED_OCCUPIED_STUDENT_BEDS, P.PG_ACTIVE_USER_PENETRATION,
                    hostel_term_opd=P.PG_HOSTEL_TERM_OPD,
                    common_drop_share=P.PG_COMMON_DROP_SHARE,
                    break_retention=P.PG_BREAK_RETENTION, pg_aov=P.PG_AOV)


def sensitivity_rows(beds=P.PG_NORMALISED_BEDS,
                     penetrations=P.PG_PENETRATION_SENSITIVITY,
                     hostel_volumes=(1000, 1200, 1400)):
    """Demand/capacity sensitivity with no financial assumption."""
    rows = []
    for penetration in penetrations:
        for hostel_opd in hostel_volumes:
            rows.append(scenario(beds, penetration, hostel_term_opd=hostel_opd))
    return rows


def report():
    cfg = configured_scenario()
    print("=" * 88)
    print("PG ADJACENCY — DEMAND IS GATED; CAPACITY IS NOT DOUBLE-COUNTED".center(88))
    print("=" * 88)
    print(f"  Evidence gate                   {'OPEN' if inputs_are_admissible() else 'CLOSED'}")
    print(f"  Configured PG orders/day         {cfg['gross_pg_opd']:,.1f}")
    print(f"  Base-case PG orders admitted     {cfg['term_pg_served_opd']:,.1f}")
    print("  Base case remains hostel-only until verified beds, adoption and AOV are populated.\n")
    print(f"  Frequency anchor                {PG_ORDERS_PER_ACTIVE_USER_DAY:.3f}/active user/day"
          f"  ({M.BLINKIT_FREQ:.1f}/month, no hostel uplift)")
    print(f"  PG last mile                    doorstep Rs{PG_DOORSTEP_CPO:.2f}"
          f"  | common-drop Rs{PG_COMMON_DROP_CPO:.2f}\n")
    print(f"  NORMALISED SENSITIVITY — {P.PG_NORMALISED_BEDS:,} verified occupied student beds")
    print(f"  {'active':>8}{'hostel':>10}{'gross PG':>11}{'served':>10}{'overflow':>11}")
    for row in sensitivity_rows():
        print(f"  {row['active_user_penetration']:>7.0%}{row['hostel_term_opd']:>10,.0f}"
              f"{row['gross_pg_opd']:>11,.0f}{row['term_pg_served_opd']:>10,.0f}"
              f"{row['term_pg_overflow_opd']:>11,.0f}")


if __name__ == "__main__":
    report()
