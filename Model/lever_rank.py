"""
CC-4 (optional): the lever ladder as a ranked trade-off map.

Method, from Chavhan & Dutta (2025), British Food Journal 127(5), DOI
10.1108/BFJ-05-2024-0560 (IIT Bombay, EFA n=255 / CFA n=135): rate each practice
on fixed dimensions -> min-max normalise -> k-means, k chosen by highest mean
silhouette -> plot each practice's deviation from the dimension mean.

Their five sustainability dimensions are swapped for ours:
   D1  fixed-cost recoverability across the dead zone
   D2  reversibility / restart cost
   D3  SLA impact under bounded access
   D4  capex intensity
   D5  transferability to the next campus

EVERY CELL is a model expression or an explicit STRUCTURAL zero (a statement that
the lever does not act on that dimension, e.g. a last-mile lever does not touch the
fixed base). No 1-5 rating is invented. `CELL_PROVENANCE` records the source of
each cell; `STRUCTURAL` records which zeros are "does not apply" rather than "measured
as zero".

LIMITATION, stated plainly: n = 7 levers. Three dimensions (D3, D4, D5) are sparse -
most levers sit at a structural zero on them - so the k-means essentially recovers
the D1 / D2 / demand-side split that the ladder already shows. The load-bearing view
is the 2-axis one (recoverability x reversibility). Read the deviation plot as a
trade-off map, not as a discovered clustering.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import campus_model as M
import cost_stack as C
import break_mode as B
import sla as SL
import fleet_mix as F
import risk_quadrant as Q
import robustness as RB

FIX      = C.CAMPUS_FIXED                    # Rs9,02,000/month
SURPLUS  = B.term_surplus_monthly()          # one month's term surplus
CAPEX    = (M.CAPEX_LO + M.CAPEX_HI) / 2     # dark-store capex, mid
PEAK     = SL.BASE_RATE * SL.PTDR_PEAK
_COLD_SAVING = (C.COLD_KW * C.COLD_HRS * 30 * C.TARIFF) * 0.60   # break_mode.cfg_cold
_RX0     = B.reactivation(0.0)                # reactivation opex components at r=0

# in-cluster round-trip time, on-foot vs stationed e-cart, over the campus leg
_ONFOOT_RT = C.CAMPUS_KM / F.MODES["On-foot runner"][0] * 60 * 2
_ECART_RT  = C.CAMPUS_KM / F.MODES["E-cart, stationed"][0] * 60 * 2
# the batch lever's explicit SLA cost at peak (sla.py: batch wait is the swing term)
_BATCH_SLA_COST = (SL.sla_minutes(PEAK, SL.dynamic_batch(PEAK))
                   - SL.sla_minutes(PEAK, 1))
# gate-drop shifts the in-campus leg to the customer
_GATEDROP_SLA_COST = (C.trip(C.GEOM["Type A campus, door-drop, manual gate"])
                      - C.trip(C.GEOM["Type A campus, gate-drop"]))

DIMS = ["fixed-cost\nrecoverability", "reversibility\n(restart cost)",
        "SLA impact\nat peak", "capex\nintensity", "transferability\nto next campus"]

# ---- the matrix: lever -> [D1, D2, D3, D4, D5], every cell traced ------------
LEVERS = ["LABOUR_FLEX", "COLD_RIGHTSIZE", "SMALL_FORMAT", "REPURPOSE",
          "GATE_DROP", "E_CART", "DYNAMIC_BATCH"]

SCORE = {
 "LABOUR_FLEX": [
     (B.STAFF - 6 * 15000) / FIX,          # D1  skeleton crew removes this share of the base
     _RX0["rehire"] / SURPLUS,             # D2  rehire opex to restart, / term surplus
     0.0,                                  # D3  structural: does not touch the fulfilment circuit
     0.0,                                  # D4  structural: no capex
     1.0,                                  # D5  structural: a rostering SOP, ports fully
 ],
 "COLD_RIGHTSIZE": [
     _COLD_SAVING / FIX,                   # D1  cold-zone consolidation saving
     _RX0["cold"] / SURPLUS,               # D2  cold pull-down + FSSAI re-verify to restart
     0.0,                                  # D3  structural
     0.0,                                  # D4  structural: right-sizes an existing room; capex is sunk
     Q.REDEPLOY,                           # D5  a physical asset: movable share only
 ],
 "SMALL_FORMAT": [
     B.RENT_SAVED / FIX,                   # D1  2,000 sqft format saving
     0.0,                                  # D2  structural: permanent format choice, nothing to restart
     0.0,                                  # D3  structural
     0.0,                                  # D4  fit-out delta not modelled; the recurring effect is in D1
     Q.REDEPLOY,                           # D5  leasehold fit-out: movable share only
 ],
 "REPURPOSE": [
     0.0,                                  # D1  structural: recovers the base via REVENUE, not a cost cut
     0.0,                                  # D2  structural: node is re-aimed, never stood down
     0.0,                                  # D3  structural
     0.0,                                  # D4  structural: a demand-side / siting move
     1.0,                                  # D5  structural: a catchment strategy, ports fully
 ],
 "GATE_DROP": [
     0.0,                                  # D1  structural: a last-mile variable-cost lever
     0.0,                                  # D2  structural
     _GATEDROP_SLA_COST,                   # D3  in-campus leg shifted to the customer, minutes
     0.0,                                  # D4  structural: an SOP, no capex
     1.0,                                  # D5  structural: an SOP, ports fully
 ],
 "E_CART": [
     0.0,                                  # D1  structural: variable-cost lever
     0.0,                                  # D2  structural
     _ECART_RT - _ONFOOT_RT,               # D3  faster in-cluster leg: NEGATIVE (improves SLA)
     RB.ecart_material_at(1.0) / CAPEX,    # D4  capex threshold at which it registers at Rs1/order
     Q.REDEPLOY,                           # D5  a vehicle: movable share
 ],
 "DYNAMIC_BATCH": [
     0.0,                                  # D1  structural: variable-cost lever
     0.0,                                  # D2  structural
     _BATCH_SLA_COST,                      # D3  the batch lever's explicit SLA cost at peak, minutes
     0.0,                                  # D4  structural: an algorithm, no capex
     1.0,                                  # D5  structural: an algorithm, ports fully
 ],
}

CELL_PROVENANCE = {
 "D1": "break_mode.cfg_* saving / cost_stack.CAMPUS_FIXED",
 "D2": "break_mode.reactivation(0) component / break_mode.term_surplus_monthly",
 "D3": "sla.sla_minutes delta (batch) ; cost_stack.GEOM trip delta (gate-drop) ; "
       "fleet_mix.MODES speed over cost_stack.CAMPUS_KM (e-cart)",
 "D4": "robustness.ecart_material_at / campus_model capex",
 "D5": "risk_quadrant.REDEPLOY (physical assets) ; 1.0 for SOP/algorithm levers",
}
STRUCTURAL = [
 "D1 = 0 for REPURPOSE (revenue not cost) and for all three last-mile levers",
 "D2 = 0 for SMALL_FORMAT / REPURPOSE (permanent / never stood down) and last-mile levers",
 "D3 = 0 for the four D1 cost levers (sla.py circuit is invariant to them)",
 "D4 = 0 for every lever except E_CART; SMALL_FORMAT fit-out delta is not in the model",
 "D5 = 1.0 for SOP/algorithm levers; REDEPLOY (0.55) for the three physical-asset levers",
]

X = np.array([SCORE[l] for l in LEVERS], dtype=float)

# D3 is signed (+ SLA cost, - SLA gain). "SLA impact" is the MAGNITUDE of the move
# to the promise; direction is kept in the raw table and the read-out. Clustering and
# the deviation plot use |D3| so a structural zero stays at zero rather than landing
# mid-scale on a signed axis.
_MAG = X.copy()
_MAG[:, 2] = np.abs(_MAG[:, 2])


def normalise(x):
    """Min-max per column; a column with no spread maps to 0."""
    lo, hi = x.min(0), x.max(0)
    span = np.where(hi - lo == 0, 1.0, hi - lo)
    return (x - lo) / span


XN = normalise(_MAG)


def choose_k(xn, kmax=5):
    rows = []
    for k in range(2, min(kmax, len(xn) - 1) + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(xn)
        rows.append((k, silhouette_score(xn, km.labels_), km.labels_))
    best = max(rows, key=lambda r: r[1])
    return best, rows


(K, SIL, LABELS), SIL_TABLE = choose_k(XN)
CLUSTERS = {l: int(c) for l, c in zip(LEVERS, LABELS)}
DEVIATION = XN - XN.mean(0)                       # each lever's deviation from the dim mean


def report():
    W = 92
    print("=" * W)
    print("CC-4  LEVER-RANKING PIPELINE  (Chavhan & Dutta 2025 method, our dimensions)".center(W))
    print("=" * W)
    print(f"{'LEVER':<16}" + "".join(f"{d.replace(chr(10),' '):>16}" for d in DIMS))
    print("-" * W)
    for i, l in enumerate(LEVERS):
        print(f"{l:<16}" + "".join(f"{v:>16.3f}" for v in X[i]))
    print("-" * W)
    print("raw model scores. D3 minutes: + = SLA cost, - = SLA gain. below: min-max normalised.\n")
    for i, l in enumerate(LEVERS):
        print(f"{l:<16}" + "".join(f"{v:>16.2f}" for v in XN[i]) + f"   cluster {CLUSTERS[l]}")

    print("\n" + "-" * W)
    print("SILHOUETTE BY k")
    for k, s, _ in SIL_TABLE:
        mark = "  <- chosen" if k == K else ""
        print(f"   k = {k}   mean silhouette {s:+.3f}{mark}")
    print(f"\n   k = {K} clusters:")
    for c in sorted(set(LABELS)):
        members = [l for l in LEVERS if CLUSTERS[l] == c]
        print(f"     cluster {c}:  {', '.join(members)}")

    print("\n" + "-" * W)
    print("CELL PROVENANCE")
    for k, v in CELL_PROVENANCE.items():
        print(f"   {k}  {v}")
    print("\nSTRUCTURAL ZEROS  (\"does not act on this dimension\", not \"measured as zero\")")
    for s in STRUCTURAL:
        print(f"   - {s}")

    print("\n" + "-" * W)
    print("READ-OUT")
    print("-" * W)
    print(f"   With n = {len(LEVERS)} levers and D3/D4/D5 sparse, the k-means recovers the")
    print(f"   split the ladder already encodes: the D1 cost levers (LABOUR_FLEX,")
    print(f"   COLD_RIGHTSIZE, SMALL_FORMAT) separate from the demand-side move (REPURPOSE)")
    print(f"   and from the D2 fulfilment levers (GATE_DROP, E_CART, DYNAMIC_BATCH).")
    print(f"   LABOUR_FLEX is the outlier: highest recoverability AND highest restart cost.")
    print(f"   The load-bearing comparison is the 2-axis one - recoverability vs restart -")
    print(f"   which is exactly why the model presents these as a LADDER, not a map.")


# ---- deviation plot (Chavhan & Dutta figure form), themed like charts.py -----
def plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from charts import THEMES, save

    order = sorted(range(len(LEVERS)), key=lambda i: (LABELS[i], LEVERS[i]))
    for T, c in THEMES.items():
        dcols = [c["accent"], c["pos"], c["hi"], c["neg"], c["mute"]]
        fig, ax = plt.subplots(figsize=(6.6, 2.8))
        w = 0.16
        for di, d in enumerate(DIMS):
            xs = [j + (di - 2) * w for j in range(len(order))]
            ax.bar(xs, [DEVIATION[order[j], di] for j in range(len(order))],
                   width=w, color=dcols[di], label=d.replace("\n", " "), zorder=3)
        ax.axhline(0, color=c["mute"], lw=1)
        for j, i in enumerate(order):
            ax.text(j, -0.86, LEVERS[i], rotation=32, ha="right", va="top",
                    fontsize=6.2, color=c["fg"], fontweight="bold")
            ax.text(j, 0.82, f"cl {LABELS[i]}", ha="center", fontsize=5.6, color=c["mute"])
        ax.set_ylim(-0.9, 0.9); ax.set_xlim(-0.6, len(order) - 0.4)
        ax.set_xticks([])
        ax.set_ylabel("deviation from dimension mean\n(min-max normalised)",
                      fontsize=6.6, color=c["mute"])
        ax.tick_params(labelsize=6.5, colors=c["mute"])
        ax.legend(fontsize=5.4, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 1.01),
                  frameon=False, labelcolor=c["mute"], columnspacing=1.0, handlelength=1.1)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        for s in ["left", "bottom"]:
            ax.spines[s].set_color(c["grid"])
        ax.grid(axis="y", color=c["grid"], lw=.4, alpha=.5, zorder=0)
        save(fig, "lever_rank", T)


if __name__ == "__main__":
    report()
    plot()
    print("\nlever_rank chart written to charts/{light,dark}/lever_rank.png")
