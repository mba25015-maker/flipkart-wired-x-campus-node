"""
D2: the SLA, derived from the fleet arithmetic rather than asserted.

THE CENTRAL DECISION. A uniform 10-15 minute promise is not reachable on a Type A campus at any
configuration we can staff. gap_check.py showed the best case is ~24 minutes average and ~31 for
the last customer in a batch. So the honest product is a 20-30 minute campus promise, stated as a
deliberate design decision rather than discovered by a panel doing our arithmetic for us.

This is defensible on its own terms: in January 2026 the government directed platforms to stop
marketing "10-minute" delivery after rider-safety strikes, and the Parliamentary Standing Committee
on Commerce (201st report, 7 Aug 2026) recommended guidelines against algorithmic speed targets.
A campus product that competes on reliability and price rather than on raw speed is aligned with
where the regulation is going, not fighting it.

THE COUNTER-INTUITIVE RESULT that falls out of the arithmetic: a batched SLA is BEST at peak and
WORST at trough - the inverse of a conventional network, where peak degrades service. Batch wait
is the dominant SLA term and it collapses as arrival rate rises. So the campus product is
structurally strongest exactly when student demand spikes (exam nights, mess-off nights), which is
the demand shape Round 1 identified as the thing that breaks standard dark-store models.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import campus_model as M, cost_stack as C, fleet_mix as F

PICK      = 2.5   # T1  Blinkit pick-and-pack, founder via Parliamentary panel reporting
CAMPUSES  = 3     # D   campuses per cluster (7,778-resident minimum, no single campus reaches it)
BASE_RATE = (M.CEILING/CAMPUSES)/18.0        # orders/hour at one campus gate, 18h day
PTDR_PEAK = 4.0   # T1  Round 1 metric 1 flag threshold: peak-to-trough demand ratio > 4.0x
PTDR_TROU = 0.25  # D   trough as a fraction of the daily average

def batch_wait(rate_hr, batch):
    return 60.0/rate_hr*batch

def sla_minutes(rate_hr, batch, position="avg"):
    """Order placed -> handed over. Batch wait + pick + ride to gate + in-cluster circuit."""
    circuit = F.circuit_min("E-cart, stationed", batch, F.SHELF_DROP)
    to_gate = C.CITY_LEG_MIN + C.GATE_PREAPP_MIN
    frac    = 0.5 if position=="avg" else 1.0
    return batch_wait(rate_hr, batch) + PICK + to_gate + circuit*frac

def dynamic_batch(rate_hr, max_wait=6.0, n_max=12):
    """THE MECHANISM. Batch closes on whichever comes first: target size, or the wait cap.
    This is what makes one SLA promise hold across peak and trough."""
    return max(1, min(n_max, int(rate_hr*max_wait/60.0)))

def runners_needed(rate_hr, batch, drop=F.SHELF_DROP):
    """Can the staffing model actually hit the promise at peak? The rubric asks this directly."""
    per_runner_hr = 60.0/F.circuit_min("E-cart, stationed", batch, drop)*batch
    return rate_hr/per_runner_hr

if __name__=="__main__":
    print("="*88); print("THE PROMISE WE CAN ACTUALLY KEEP".center(88)); print("="*88)
    print(f"Cluster {M.CEILING:,} orders/day across {CAMPUSES} campuses -> {BASE_RATE:.1f} orders/hour at one gate\n")
    print(f"{'state':<14}{'orders/hr':>11}{'batch (dyn)':>13}{'batch wait':>12}"
          f"{'AVG SLA':>10}{'LAST':>8}{'runners':>9}{'Rs/order':>10}")
    print("-"*88)
    STATES = [("Trough", BASE_RATE*PTDR_TROU), ("Average", BASE_RATE),
              ("Peak (4x)", BASE_RATE*PTDR_PEAK), ("Exam night (6x)", BASE_RATE*6)]
    for name, rate in STATES:
        b = dynamic_batch(rate)
        cost = F.total_campus_cost("E-cart, stationed", b, F.RUNNER_HR, F.SHELF_DROP)
        print(f"{name:<14}{rate:>11.1f}{b:>13}{batch_wait(rate,b):>12.1f}"
              f"{sla_minutes(rate,b):>10.1f}{sla_minutes(rate,b,'last'):>8.1f}"
              f"{runners_needed(rate,b):>9.1f}{cost:>10.1f}")
    print("-"*88)
    print(f"At trough the batched model is uneconomic (Rs64.8/order at batch 1) and volume is")
    print(f"below the {F.breakeven_volume():.0f}/day runner floor anyway - trough reverts to gig riders at the gate.")
    print("Batch closes on a 6-MINUTE WAIT CAP or 12 orders, whichever comes first. That single")
    print("rule is what holds one promise across a 24x swing in arrival rate.")
    print("\n>>> Batch wait FALLS as demand rises, so the campus product is fastest and cheapest")
    print("    exactly at exam-night peak - the inverse of a conventional zone. Round 1 called the")
    print("    student demand spike the thing that breaks dark-store models. Batched consolidation")
    print("    turns it into the thing that makes this one work.")

    print("\n"+"="*88); print("THE TIER STRUCTURE".center(88)); print("="*88)
    rate = BASE_RATE
    TIERS = [
     ("Express",        1,  "unbatched, dedicated runner run",       "chilled + frozen, or paid tier"),
     ("Standard",       dynamic_batch(rate), "dynamic batch, 6-min wait cap", "ambient core, default"),
     ("Scheduled slot", 12, "customer picks a 30-min window",        "predictable peaks, bulk, durables"),
    ]
    SCHED_WINDOW = 30.0   # the promise IS the window; accumulation happens inside it, not before it
    print(f"{'Tier':<16}{'batch':>7}{'AVG SLA':>10}{'LAST':>8}{'Rs/order':>10}  {'mechanism':<32}")
    print("-"*88)
    for name, b, mech, use in TIERS:
        cost = F.total_campus_cost("E-cart, stationed", b, F.RUNNER_HR, F.SHELF_DROP)
        if name == "Scheduled slot":
            print(f"{name:<16}{b:>7}{'window':>10}{SCHED_WINDOW:>7.0f}m{cost:>10.1f}  {mech:<32}")
        else:
            print(f"{name:<16}{b:>7}{sla_minutes(rate,b):>10.1f}{sla_minutes(rate,b,'last'):>8.1f}"
                  f"{cost:>10.1f}  {mech:<32}")
    print("-"*88)
    print(f"{'Tier':<16}{'serves':<50}")
    for name,b,mech,use in TIERS: print(f"{name:<16}{use:<50}")
    print(f"\n{'Shelf hold':<16}{'curfew campuses after cutoff: secured block shelf, morning collect':<50}")
    print(f"{'':<16}{'ambient only unless the shelf is refrigerated':<50}")

    print("\n"+"="*88); print("SLA x ACCESS REGIME  - Round 1's Gate 0 paying off in operations".center(88)); print("="*88)
    print(f"{'Access regime':<34}{'Express':>9}{'Standard':>10}{'Scheduled':>11}{'Shelf hold':>12}")
    print("-"*88)
    REGIMES = [
     ("Open (3 AM doorstep permitted)",        "yes","yes","yes","yes"),
     ("Curfew (gate shuts 8-11 PM)",           "to cutoff","to cutoff","to cutoff","yes"),
     ("Gate-only (no block entry)",            "gate pt","gate pt","gate pt","gate pt"),
     ("Banned",                                 "--","--","--","--"),
    ]
    for r,a,b,c,d in REGIMES: print(f"{r:<34}{a:>9}{b:>10}{c:>11}{d:>12}")
    print("-"*88)
    print("WHERE access rules genuinely differ by block - a different curfew hour for women's")
    print("hostels on the same campus - the SLA follows the block, not the campus. Round 1's coded")
    print("corpus found gender-differentiated delivery access in at least one campus, and that")
    print("caveat travels with the claim: theme salience, not population frequency.")
    print("\n  DO NOT confuse this with the campus PARCEL system, which also sorts by gender.")
    print("  That split is a sorting and propriety convenience for accumulated parcels (male guards")
    print("  do not handle collection at women's hostels), NOT a delivery-time restriction. The two")
    print("  are different things and an earlier draft of this model conflated them.")

    print("\n"+"="*88); print("TEMPERATURE ROUTING - the assortment tension resolved physically".center(88)); print("="*88)
    print("Ambient core   -> any tier. Batched, shelf handoff, longest wait tolerated.")
    print("Chilled        -> Express or Standard only. Never shelf-held without refrigeration.")
    print("Frozen         -> Express only, or not offered on that campus.")
    print("Long tail      -> backfilled from the SDFC on a next-day promise, not stocked locally.")
    print("\n>>> This is the wide-vs-curated tension Round 1 flagged and could not fit on a slide,")
    print("    resolved without violating the brief's wide-assortment value: we narrow what is")
    print("    STOCKED locally and what is PROMISED fast, never the catalogue.")

    print("\n"+"="*88); print("CAN THE STAFFING MODEL HIT IT AT PEAK?".center(88)); print("="*88)
    peak = BASE_RATE*PTDR_PEAK; b = dynamic_batch(peak)
    print(f"Peak {peak:.0f} orders/hour at one gate, dynamic batch {b}")
    print(f"  one runner clears {60.0/F.circuit_min('E-cart, stationed',b,F.SHELF_DROP)*b:.0f} orders/hour")
    print(f"  runners required at peak: {runners_needed(peak,b):.1f}  ->  roster {int(runners_needed(peak,b))+1}")
    print(f"  runners required at average: {runners_needed(BASE_RATE,dynamic_batch(BASE_RATE)):.1f}")
    flex = 1 - runners_needed(BASE_RATE,dynamic_batch(BASE_RATE))/runners_needed(peak,b)
    print(f"\n  Peak-variable share of the runner roster = {flex:.0%}")
    print(f"\n  HONEST READING, and it corrects a sloppy mapping. Round 1's Labour Flex Ratio")
    print(f"  (>=60%) came from stadium concessions - EVENT-DRIVEN hourly crew sizing. The runner")
    print(f"  roster does NOT meet that band ({flex:.0%}), and it should not be forced to, because")
    print(f"  DYNAMIC BATCHING ABSORBS THE HOURLY SPIKE INTO BATCH SIZE RATHER THAN HEADCOUNT.")
    print(f"  A {PTDR_PEAK:.0f}x demand spike needs only {runners_needed(peak,b)/runners_needed(BASE_RATE,dynamic_batch(BASE_RATE)):.1f}x the runners. That is the batching")
    print(f"  mechanism working, not a staffing failure.")
    print(f"\n  The two Round 1 labour metrics map to different pools and different axes:")
    print(f"    Labour Flex Ratio (>=60%, hourly/event)  -> STORE pick-pack crew, which does")
    print(f"       flex with hourly volume and is where the metric belongs")
    print(f"    Calendar-Linked Labour Share (>=50%)     -> BOTH pools, on the academic-calendar")
    print(f"       axis. The runner roster goes to zero below the {F.breakeven_volume():.0f}/day break floor,")
    print(f"       so it is calendar-flexible even though it is not hour-flexible.")

# ============================================================================
# VOLUME-WEIGHTED COST - the correct headline, replacing two earlier overclaims
# ============================================================================
# Correction 1: an earlier draft quoted Rs9.3/order at n=8. gap_check.py showed n=8 is not
#   reachable at average arrival rates. The dynamic batch at AVERAGE demand is only 2, giving
#   Rs33.0/order - far worse than the figure that was being quoted.
# Correction 2: but quoting the average-state cost is ALSO wrong, in the other direction. A
#   campus is peaky by construction (Round 1 metric 1, PTDR flag >4.0x), so most ORDERS occur
#   during peak hours, where batches fill fast and cost collapses. Weighting by TIME understates
#   the saving; weighting by VOLUME is the honest measure.
#
# The right question is not "what does an order cost at average demand" but "what does the
# average order cost", and on a spiky demand curve those are different numbers.

HOURS = [   # hours in an 18h day, rate as a multiple of the mean-hour rate
 ("Peak (late evening, exam windows)", 4, 4.0),
 ("Normal",                            8, 1.0),
 ("Trough (early morning, class hrs)", 6, 0.25),
]
def volume_weighted():
    tot_eq = sum(h*m for _,h,m in HOURS)          # average-hour equivalents
    rows, wcost = [], 0.0
    for name, h, m in HOURS:
        share = h*m/tot_eq                         # share of daily ORDERS, not of time
        rate  = BASE_RATE*m*(18.0/tot_eq)*(tot_eq/18.0)   # rate in that hour band
        rate  = BASE_RATE*m
        b     = dynamic_batch(rate)
        cost  = F.total_campus_cost("E-cart, stationed", b, F.RUNNER_HR, F.SHELF_DROP)
        wcost += share*cost
        rows.append((name, h, m, share, rate, b, cost, sla_minutes(rate,b)))
    return rows, wcost

if __name__=="__main__":
    rows, w = volume_weighted()
    print("\n"+"="*88); print("THE HONEST HEADLINE: cost weighted by ORDERS, not by hours".center(88)); print("="*88)
    print(f"{'demand band':<36}{'hrs':>5}{'rate':>6}{'% of orders':>13}{'batch':>7}{'Rs/order':>10}{'SLA':>7}")
    print("-"*88)
    for name,h,m,share,rate,b,cost,s in rows:
        print(f"{name:<36}{h:>5}{m:>5.2f}x{share:>12.1%}{b:>7}{cost:>10.1f}{s:>7.1f}")
    print("-"*88)
    print(f"{'VOLUME-WEIGHTED COST PER ORDER':<36}{'':<31}{w:>10.1f}")
    print(f"{'Standard 2-3 km residential zone':<36}{'':<31}{M.LAST_MILE:>10.1f}")
    print(f"{'Saving':<36}{'':<31}{1-w/M.LAST_MILE:>9.0%}")
    print("\n>>> Rs{:.0f}/order, {:.0%} below a standard zone. This supersedes BOTH the Rs9.3 figure".format(w, 1-w/M.LAST_MILE))
    print("    (peak-only, unreachable at average) and the Rs33.0 figure (average-hour, which")
    print("    ignores that most orders happen at peak). It is the number that goes on the slide.")
    print(f"\n    Sensitivity: the weighting depends on the demand profile. At a flatter 2x peak the")
    print(f"    weighted cost rises; at Round 1's >4x PTDR flag it falls. Profile stated on-slide.")

    print("\n"+"="*88); print("WHAT THE RUNNER IS NOT: the parcel-room model".center(88)); print("="*88)
    print("The incumbent campus parcel system accumulates all day and distributes ONCE, in the")
    print("evening, sorted by hostel. That works for a sealed parcel nobody is waiting for.")
    print("It does not transfer to quick commerce, and we are not proposing it.")
    print(f"\n  Incumbent parcel model     accumulate ~8 hours, one distribution round")
    print(f"  Our in-cluster runner      CONTINUOUS circuits, {F.circuit_min('E-cart, stationed',10,F.SHELF_DROP):.0f} min each, all day")
    print(f"  Customer-visible wait      {dynamic_batch(BASE_RATE*4)*0 + 6:.0f} min batch cap, not a scheduled round")
    print("\n>>> The institution supplies LABOUR and ACCESS on a continuous roster. It does not")
    print("    supply an accumulation-and-sort service. That distinction has to be explicit in the")
    print("    partnership scope or the university will scope it as the parcel desk, which is the")
    print("    one thing that would kill the service level.")
