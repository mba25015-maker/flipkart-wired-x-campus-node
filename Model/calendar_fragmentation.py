"""
THE GAP OUR OWN ADVERSARIAL PROBE FOUND AND WE NEVER CLOSED.

`break_mode.py` treats the academic break as a SINGLE CONTIGUOUS 3.5-month block
(BREAK_MONTHS = 12 - ACTIVE_MONTHS = 3.5). `gap_check.py` PROBE 4 has been saying since it was
written that this may not exist:

    "Indian academic calendars are FRAGMENTED (summer + winter + exam gaps), so a single
     3.5-month contiguous break may not exist at many campuses."

and, from the same probe, the binding operational rule:

    "Breaks shorter than 7 weeks cannot be wound down at all: the ramp and the wind-down collide."

Put those two together and the wind-down playbook may fire on far less than 3.5 months of the year.
THIS MODULE PRICES THAT. It is the difference between a plan that works on a spreadsheet calendar
and one that works on a real university's calendar.

TIERS: T1 disclosure/analyst | T2 published academic calendars | D derived | A assumed
"""
import campus_model as M, break_mode as B

WEEKS_PER_MONTH = 52.0/12.0
TOTAL_BREAK_WEEKS = B.BREAK_MONTHS * WEEKS_PER_MONTH        # 15.2 weeks
MIN_WINDDOWN_WEEKS = 7.0    # D  gap_check PROBE 4: below this the 28-day ramp and the
                            #    T-21d wind-down collide, so no lever can be pulled

# Calendar shapes. The contiguous one is what the model has always assumed; the others are what
# Indian university calendars actually look like.  [T2, published academic calendars]
SHAPES = {
 "Contiguous (model's current assumption)": [15.2],
 "Typical: summer + winter + exam gaps":    [8.0, 4.0, 3.2],
 "Fragmented: many short gaps":             [6.0, 4.0, 3.0, 2.2],
 "Semester system, one long summer":        [11.0, 4.2],
}

def segment_cost(weeks, r=0.0):
    """Monthly deficit x months, choosing the configuration the segment length ALLOWS."""
    months = weeks/WEEKS_PER_MONTH
    if weeks >= MIN_WINDDOWN_WEEKS:
        name, fn = B.CONFIGS[-1]                 # full ladder available
        react = B.reactivation(r)["opex_total"]  # and it must be paid to come back
    else:
        name, fn = B.CONFIGS[0]                  # do nothing - cannot wind down
        react = 0.0
    return -B.break_monthly_cm(r, fn)*months + react, name

def shape_cost(segments, r=0.0):
    tot, detail = 0.0, []
    for w in segments:
        c, name = segment_cost(w, r)
        tot += c; detail.append((w, name, c))
    return tot, detail

def windownable_share(segments):
    return sum(w for w in segments if w >= MIN_WINDDOWN_WEEKS)/sum(segments)

BASE_COST, _ = shape_cost(SHAPES["Contiguous (model's current assumption)"])
RESULTS = {k: shape_cost(v) for k, v in SHAPES.items()}
TYPICAL_COST = RESULTS["Typical: summer + winter + exam gaps"][0]
TYPICAL_PENALTY = TYPICAL_COST/BASE_COST - 1
TYPICAL_WINDOWNABLE = windownable_share(SHAPES["Typical: summer + winter + exam gaps"])
WORST_COST = max(v[0] for v in RESULTS.values())
WORST_PENALTY = WORST_COST/BASE_COST - 1

# The design response: this is not a reason to abandon the plan, it is a SITE-SELECTION CRITERION,
# which is the same conclusion the whole deck reaches by a different route.
def qualifies(segments):
    """A campus qualifies for the wind-down playbook only if it has at least one segment long
    enough to wind down. Otherwise the node runs do-nothing all year and must be underwritten
    entirely on adjacent catchment."""
    return any(w >= MIN_WINDDOWN_WEEKS for w in segments)

def report():
    print("="*88); print("CALENDAR FRAGMENTATION: WHAT IF THE BREAK IS NOT ONE BLOCK?".center(88)); print("="*88)
    print(f"  Model assumes {B.BREAK_MONTHS} contiguous months = {TOTAL_BREAK_WEEKS:.1f} weeks")
    print(f"  Wind-down is impossible below {MIN_WINDDOWN_WEEKS:.0f} weeks (28-day ramp vs T-21d wind-down)")
    print()
    print(f"  {'calendar shape':<42}{'segments':<22}{'wind-downable':>14}{'dead-zone cost':>16}{'vs base':>9}")
    print("  "+"-"*84)
    for name, segs in SHAPES.items():
        cost, _ = RESULTS[name]
        print(f"  {name:<42}{str([f'{w:.1f}w' for w in segs])[:21]:<22}"
              f"{windownable_share(segs):>13.0%}{cost/1e5:>15.1f}L{cost/BASE_COST-1:>+8.0%}")
    print("  "+"-"*84)
    print()
    print(f"  >>> On a TYPICAL Indian calendar the dead-zone cost is {TYPICAL_PENALTY:+.0%} vs the contiguous")
    print(f"      assumption, because only {TYPICAL_WINDOWNABLE:.0%} of break weeks are long enough to wind down.")
    print(f"      Worst shape modelled: {WORST_PENALTY:+.0%}.")
    print()
    print("  WHY THIS IS NOT FATAL, AND IS ACTUALLY ON-THESIS:")
    print("    the fix is not a cheaper lever, it is the SAME site-selection answer the rest of the")
    print("    deck reaches by another route. Add one condition to the filter:")
    print("      >> the campus must have at least ONE break segment of 7+ weeks.")
    print("    A campus whose calendar is all short gaps cannot be wound down at all and must be")
    print("    underwritten ENTIRELY on adjacent catchment. That is a different, worse node.")
    print()
    print("  ADD TO THE RISK REGISTER, and say it before a panellist does:")
    print("    every D1 saving in this deck is quoted on a contiguous break. On a fragmented")
    print(f"    calendar the levers reach only {TYPICAL_WINDOWNABLE:.0%} of the dead zone.")

if __name__ == "__main__":
    report()
