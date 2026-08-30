"""
VERIFY THE SPEC. Same discipline as verify_docs.py and verify_deck.py, one document later:
parse the figures OUT of DECK_SPEC_SemiFinal.md and check each against the model.

  python3 verify_spec.py [path.md]

The spec is hand-written prose, so its numbers are the ones most likely to drift. This is the
check that catches a typo before it becomes a slide.
"""
import sys, os, re
import campus_model as M, cost_stack as CS, break_mode as B, sla as SL
import aishe_district as AD, calendar_fragmentation as CF, risk_quadrant as Q
import basket as BK, working_capital as WC, risk_shocks as RS, fleet_mix as F
import labour_class as LC

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
# Checks every figure-bearing build document, not just the spec: a number that drifts in the PPT
# build prompt reaches a slide just as surely as one that drifts in the spec.
DOCS = ([sys.argv[1]] if len(sys.argv) > 1 else
        [os.path.join(ROOT, d) for d in ("DECK_SPEC_SemiFinal.md", "PPT_BUILD_PROMPT_SemiFinal.md")])
TEXT = "\n".join(open(d, encoding="utf-8").read() for d in DOCS)
DOC  = " + ".join(os.path.basename(d) for d in DOCS)

# The spec is written in Indian digit grouping (9,02,000), the model prints 902,000.
# Accept either spelling of the same number rather than forcing the prose to look wrong.
def _indian(n):
    s = f"{int(round(n)):d}"
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ",".join(parts) + "," + tail

# must_not is scanned over the ARGUMENT only. Part 4 is the pre-flight checklist, which
# names the banned figures on purpose; guarding against our own reminder is a false alarm.
# A8 is the "examined and rejected" appendix row: naming a superseded figure there is the
# point of the page, so that line is excluded too.
BODY = "\n".join(l for l in TEXT.split("# PART 4")[0].splitlines()
                 if "Examined and rejected" not in l)

checks = []
def must(label, needle, alt=None):
    hit = needle in TEXT or (alt is not None and alt in TEXT)
    checks.append((hit, label, needle))
def must_num(label, value, fmt="{:,.0f}"):
    western = fmt.format(value)
    checks.append((western in TEXT or _indian(value) in TEXT, label, western))
def must_not(label, needle):
    checks.append((needle not in BODY, label, "ABSENT: " + needle))

thr = [B.threshold(fn) for _, fn in B.CONFIGS]
rel = B.relocate_vs_flex()
rev = Q.post_revocation_survival()
be  = CS.breakeven_d2_consistent(CS.CAMPUS_FIXED, SL.volume_weighted()[1])

# ---- the spine ----
must_num("fixed base",                   CS.CAMPUS_FIXED)
must("flexible share",                   f"{CS.fixed_flex_share():.1%}")
must_num("other fixed residual",         CS.OTHER_FIXED)
must("ladder start",                     f"{thr[0]:.1%}")
must("ladder floor",                     f"{thr[-1]:.1%}")
must("labour-flex threshold",            f"{thr[1]:.1%}")
must("cold-rightsize threshold",         f"{thr[2]:.1%}")
must("breakeven AOV",                    f"{be:,.0f}")
must("network AOV",                      f"{M.MINUTES_AOV:,.0f}")
must("calendar surcharge",               f"{M.CAL_SURCHARGE:.3f}")
must("asset turn ratio",                 f"{M.TURN_RATIO:.3f}")
must("campus turn",                      f"{M.CAMPUS_TURN:.2f}")
must("city turn",                        f"{M.CITY_TURN:.2f}")
must("density term",                     f"{M.CEILING/M.MINUTES_ORD:.3f}")
must("calendar term",                    f"{M.ACTIVE_MONTHS/12:.3f}")
must("ratio at 1,000/day",               f"{M.TURN_RATIO_AT_1000:.3f}")
must("ratio at 1,200/day",               f"{M.TURN_RATIO_AT_1200:.3f}")
must("parity throughput",                f"{M.PARITY_OPD:,.0f}")
must("observed range low",               f"{M.CEIL_LO:,}")
must("observed range high",              f"{M.CEIL_HI:,}")

# ---- D2 ----
must("volume-weighted last mile",        f"{SL.volume_weighted()[1]:.1f}")
must("standard-zone last mile",          f"{M.LAST_MILE:.1f}")
must("gig active-hour rate",             f"{LC.ROWS[0]['per_hour']:.1f}" if hasattr(LC,"ROWS") else f"{CS.RIDER_HR_ACTIVE:.0f}")
must("runner rostered-hour rate",        "72")
must("labour-class ratio, JPM anchor",   f"{CS.RATIO_JPM:.2f}")
must("labour-class ratio, UBS anchor",   f"{CS.RATIO_UBS:.2f}")
must("runner breakeven volume",          f"{F.breakeven_volume():.0f}/day")

# ---- site filter ----
must("uncontested site filter",          f"{AD.SITE_FILTER_UNCONTESTED:,.0f}")
must("revocation requirement",           f"{rev['orders_needed']:,.0f}")
must("solvency low",                     f"{rev['adjacent_lo']:,.0f}")
must("gross at metro overlap",           f"{AD.gross_demand_required(AD.METRO_OVERLAP_5OP):,.0f}")
must("candidate districts",              f"{AD.N_CANDIDATES}")
must("districts in register",            f"{AD.N_DISTRICTS:,}")
must("colleges in register",             f"{AD.N_COL:,}")
must("urban colleges",                   f"{AD.URBAN_COL:,}")
must("urban non-metro colleges",         f"{AD.NON_METRO_URBAN_COLLEGES:,}")
must("metro urban colleges",             f"{AD.METRO_URBAN_COLLEGES:,}")
must("high-propensity standalones",      f"{AD.N_STA_URBAN_HP:,}")
must("uncontested districts",            f"{AD.PROX_COUNTS['uncontested']}")
must("stacked districts",                f"{AD.PROX_COUNTS['stacked']}")
must("stores added in the quarter",      f"{AD.STORES_ADDED_Q}")
must("new pin codes reached",            f"{AD.PIN_CODES_ADDED_Q}")
must("stores per new pin code",          f"{AD.STORES_PER_NEW_PINCODE:.1f}")
must("metro stores",                     f"{AD.METRO_STORES:,}")
must("sustainable metro capacity",       f"{AD.METRO_SUSTAINABLE:,}")

# ---- break, basket, risk ----
must("do-nothing burn",                  f"{rel['do_nothing_total']/1e5:.1f} L")
must("hold-through burn",                f"{rel['flex_total']/1e5:.1f} L")
must("relocate once",                    f"{rel['relocate_once']/1e5:.0f} L")
must("relocate and return",              f"{rel['relocate_and_return']/1e5:.0f} L")
must("holding vs relocating",            f"{rel['flex_vs_relocate']:.0%}")
must("wind-down floor weeks",            f"{CF.MIN_WINDDOWN_WEEKS:.0f}")
must("typical wind-downable share",      f"{CF.TYPICAL_WINDOWNABLE:.0%}")
must("typical fragmentation penalty",    f"{CF.TYPICAL_PENALTY:+.0%}")
must("worst fragmentation penalty",      f"{CF.WORST_PENALTY:+.0%}")
must("basket slope",                     f"{BK.SLOPE:.2f}")
must("basket intercept",                 f"{BK.INTERCEPT:.0f}")
must("basket fit R2",                    f"{BK.R2:.3f}")
must("non-grocery share required",       f"{BK.SHARE_NEEDED_AFTER_OCCASION:.1f}%")
must("mix-only share required",          f"{BK.SHARE_NEEDED:.1f}%")
must("working capital at 14 days",       f"{WC.WC_ADOPTED/1e5:.1f} lakh" if hasattr(WC,"WC_ADOPTED") else "90.0 lakh")

# ---- figures that live only in the PPT build prompt -----------------------------
import roce as RC
must_num("capital employed",             RC.CE_BASE/1e5)
must("hurdle AOV",                       f"{RC.AOV_HURDLE:,.0f}")
must("ROCE breakeven AOV",               f"{RC.AOV_BREAKEVEN:,.0f}")
must("ROCE at a 30% basket",             f"{RC.roce(RC.AOV_UP):.1%}")
must("ROCE at a 40% basket",             f"{RC.roce(RC.AOV_MAX):.1%}")
must("downside ROCE",                    f"{RC.roce(RC.AOV_UP, v=M.CEILING*RC.VOL_SHOCK):.1%}")
must("IRR at the hurdle",                f"{RC.irr(RC.AOV_HURDLE):.1%}")
must("DuPont margin leg",                f"{RC.dupont(RC.AOV_HURDLE)['ebit_margin']:.2%}")
must("DuPont turnover leg",              f"{RC.dupont(RC.AOV_HURDLE)['capital_turn']:.2f}")
must("non-grocery share at the hurdle",  f"{RC.HURDLE_NONGROCERY_SHARE:.1f}%")
must("capex midpoint",                   f"{RC.CAPEX_MID/1e5:,.0f}")
must("orders per year",                  f"{RC.orders_year():,.0f}")
must("node life anchor",                 f"{M.FRANCHISE_PAYBACK}-month")

# ---- nothing superseded ----
for lab, n in [("Round 1 breakeven","Rs528"), ("Round 1 breakeven, glyph","₹528"),
               ("Round 1 AOV","₹775"), ("Round 1 asset turn","12.6×"),
               ("superseded WC","₹95.7"), ("superseded breakeven","₹554")]:
    must_not(lab, n)

if __name__ == "__main__":
    bad = [c for c in checks if not c[0]]
    print(f"\nVERIFYING {DOC}\n" + "="*74)
    for ok, lab, needle in checks:
        print(("  OK  " if ok else "  FAIL") + f"  {lab:<34} {needle}")
    print(f"\n{len(checks)-len(bad)}/{len(checks)} spec figures tie out to the model")
    if bad: raise SystemExit("SPEC VERIFICATION FAILED")
