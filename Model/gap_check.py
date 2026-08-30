"""Adversarial self-audit. Testing our own numbers where a panel would push."""
import campus_model as M, cost_stack as C, fleet_mix as F, break_mode as B, index_model as I

print("="*84); print("PROBE 1: is the DESIGNED batch achievable at campus arrival rates?".center(84)); print("="*84)
# Round 1: minimum viable cluster 7,778 residents. No single Indian campus reaches it,
# so a cluster is MULTIPLE campuses. Batching is per-GATE, not per-cluster.
CLUSTER_RES = I.CLUSTER
print(f"Cluster {CLUSTER_RES:,.0f} residents -> {M.CEILING:,} orders/day across the cluster")
print(f"{'campuses/cluster':>18}{'orders/campus/day':>20}{'orders/hr (18h)':>17}"
      f"{'mins to batch 8':>18}{'mins to batch 4':>17}")
print("-"*84)
for n_campus in (1,2,3,4,6):
    opd = M.CEILING/n_campus
    per_hr = opd/18.0
    print(f"{n_campus:>18}{opd:>20,.0f}{per_hr:>17.1f}{60/per_hr*8:>18.1f}{60/per_hr*4:>17.1f}")
print("-"*84)
print("A batch window is dead time the customer waits. It is SLA, not just cost.")

print("\n"+"="*84); print("PROBE 2: the SLA the fleet can actually hit".center(84)); print("="*84)
PICK = 2.5     # T1 Blinkit pick-and-pack, founder via Parliamentary panel reporting
def sla(n_campus, batch):
    per_hr = (M.CEILING/n_campus)/18.0
    wait   = 60/per_hr*batch                                  # accumulate the batch
    to_gate= C.CITY_LEG_MIN + C.GATE_PREAPP_MIN
    circuit= F.circuit_min("E-cart, stationed", batch, F.SHELF_DROP)
    return {"wait":wait, "pick":PICK, "gate":to_gate, "avg_circuit":circuit/2,
            "avg":wait+PICK+to_gate+circuit/2, "last":wait+PICK+to_gate+circuit}
print(f"{'campuses':>9}{'batch':>7}{'batch wait':>12}{'pick':>7}{'to gate':>9}"
      f"{'in-cluster':>12}{'AVG SLA':>10}{'LAST in batch':>15}")
print("-"*84)
for nc,b in ((3,8),(3,4),(3,3),(4,4),(4,3),(2,6)):
    s=sla(nc,b)
    print(f"{nc:>9}{b:>7}{s['wait']:>12.1f}{s['pick']:>7.1f}{s['gate']:>9.1f}"
          f"{s['avg_circuit']:>12.1f}{s['avg']:>10.1f}{s['last']:>15.1f}")
print("-"*84)
print("A 10-15 minute promise is not reachable on ANY of these. The honest product is 20-30 min.")

print("\n"+"="*84); print("PROBE 3: cost per order at ACHIEVABLE batch sizes".center(84)); print("="*84)
# S26 REFRESH: the headline is no longer a single batch size. sla.volume_weighted() gives
# Rs19.0/order across the daypart (batch 10 at peak / 2 at average / 1 at trough, 62.7% of
# orders in the peak band). This probe now tests the DESIGN against fixed-batch alternatives.
import sla as _S
_rows, HEADLINE = _S.volume_weighted()
print(f"{'batch':>7}{'Rs/order':>11}{'vs volume-weighted Rs19.0':>27}{'vs standard zone':>19}")
head = HEADLINE
for b in (3,4,6,8):
    c=F.total_campus_cost("E-cart, stationed",b,F.RUNNER_HR,F.SHELF_DROP)
    print(f"{b:>7}{c:>11.1f}{c/head-1:>+21.0%}{c/M.LAST_MILE-1:>+19.0%}")
print("-"*84)
print(f"Volume-weighted headline Rs{HEADLINE:.1f}/order sits between the batch-3 and batch-4 fixed cases,")
print("i.e. the DESIGN is no more optimistic than a flat batch of 3-4 - which is the number this probe")
print("originally demanded. e-cart capacity is 12, so the peak batch of 10 is inside the physical limit.")

print("\n"+"="*84); print("PROBE 4: break length - the brief says 3-4 months, is it contiguous?".center(84)); print("="*84)
RAMP = 28  # days, from break_mode playbook
print(f"Ramp-up lead time {RAMP} days. Wind-down actions begin T-21d.")
print(f"{'break length':>14}{'days idle after ramp':>23}{'wind-down+ramp overlap':>25}{'verdict':>18}")
print("-"*84)
for wks in (2,4,6,8,10,15):
    days=wks*7; usable = days - RAMP - 21
    verdict = "DO NOT wind down" if usable <= 0 else ("marginal" if usable < 21 else "full playbook")
    print(f"{f'{wks} weeks':>14}{max(0,usable):>23}{('yes' if usable<0 else 'no'):>25}{verdict:>18}")
print("-"*84)
print(f">>> Breaks shorter than {(RAMP+21)/7:.0f} weeks cannot be wound down at all: the ramp and the")
print("    wind-down collide. Indian academic calendars are FRAGMENTED (summer + winter + exam gaps),")
print("    so a single 3.5-month contiguous break may not exist at many campuses.")

print("\n"+"="*84); print("PROBE 5: the -30% volume downside the brief explicitly asks for".center(84)); print("="*84)
for shock in (0.0,0.15,0.30):
    opd=M.CEILING*(1-shock)
    cpo=C.store_cost_per_order(C.CAMPUS_FIXED,opd)
    be =C.breakeven_d2_consistent(C.CAMPUS_FIXED,HEADLINE,opd)  # S26: adopted basis, from the model
    print(f"  volume {-shock:>+5.0%}  ->  {opd:>6,.0f} orders/day   store cost/order Rs{cpo:>5.1f}   "
          f"breakeven AOV Rs{be:>4.0f}")
print(f"\n  Runner floor {F.breakeven_volume():.0f}/day is unaffected by a term-time shock (still cleared).")
print(f"  But breakeven AOV rises Rs{C.breakeven_d2_consistent(C.CAMPUS_FIXED,HEADLINE,M.CEILING*0.7)-C.breakeven_d2_consistent(C.CAMPUS_FIXED,HEADLINE):.0f} "
      f"on a -30% shock, which is the whole basket-lifting gain wiped out.")
