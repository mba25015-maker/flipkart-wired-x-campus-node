"""
Figures for the restructured deck: slide 4 (the return) and slide 7 (the financials).

  17. roce_ladder  (S4/S7)  ROCE by scenario against Eternal's public 40% benchmark.
  18. pnl_bridge   (S7)     one node, one year: NOV -> revenue -> contribution -> EBIT.

Nothing typed. Values come from roce.py, which imports the rest of the model.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from charts import THEMES, save
import roce as RC, campus_model as M, cost_stack as CS
plt.rcParams["font.family"] = "DejaVu Sans"


# ============ 17. ROCE AGAINST THE EXTERNAL BENCHMARK ============
def roce_ladder(T):
    c = THEMES[T]
    rows = RC.scenario_rows()
    labels = ["underwritten\n(breakeven)", "basket 30%\nnon-grocery", "basket 40%\nnon-grocery",
              "basket 30%\nvolume -30%"]
    vals = [r["roce"]*100 for r in rows]
    order = [0, 3, 1, 2]                      # worst to best against the benchmark line
    vals   = [vals[i] for i in order]
    labels = [labels[i] for i in order]

    fig, ax = plt.subplots(figsize=(4.30, 1.86))
    hurdle = RC.ROCE_HURDLE*100
    for i, v in enumerate(vals):
        clears = v >= hurdle
        ax.bar(i, v, width=.58, zorder=3,
               color=c["pos"] if clears else (c["neg"] if v < 15 else c["mute"]),
               alpha=.9 if clears else .75)
        ax.text(i, v+1.6, f"{v:.1f}%", ha="center", va="bottom", fontsize=8.2,
                color=c["fg"], fontweight="bold", zorder=5)
    ax.axhline(hurdle, color=c["hi"], lw=1.4, ls="--", zorder=4)
    ax.text(len(vals)-.42, hurdle+1.8, f"Eternal benchmark {hurdle:.0f}%", ha="right", va="bottom",
            fontsize=6.4, color=c["hi"], fontweight="bold", zorder=5)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, fontsize=6.0, color=c["mute"], linespacing=1.2)
    ax.set_ylim(0, max(max(vals), hurdle)*1.28)
    ax.set_ylabel("ROCE, pre-tax", fontsize=6.4, color=c["mute"])
    ax.set_yticks([0, 20, 40, 60]); ax.tick_params(labelsize=6.2, colors=c["mute"])
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]: ax.spines[s].set_color(c["grid"])
    ax.grid(axis="y", color=c["grid"], lw=.45, alpha=.5, zorder=0)
    save(fig, "roce_ladder", T)


# ============ 18. THE P&L BRIDGE, ONE NODE, ONE YEAR ============
def pnl_bridge(T):
    """At the AOV implied by Eternal's public return benchmark."""
    c = THEMES[T]
    aov = RC.AOV_HURDLE
    n   = RC.orders_year()
    nov = RC.nov_year(aov)
    rev = M.TAKE_RATE*aov*n
    lm  = RC.LAST_MILE_D2*n; so = M.STORE_OPS*n; pk = M.PACKAGING*n; res = M.RESIDUAL*n
    fx  = CS.CAMPUS_FIXED*12
    ebit = RC.ebit_year(aov)

    fig, ax = plt.subplots(figsize=(4.35, 1.86))
    # A proper floating waterfall: start at revenue, subtract each cost, land on EBIT.
    # NOV is not a bar -- it is 5x the revenue bar and would flatten everything else.
    steps = [("revenue\n@19.41%", rev), ("last\nmile", -lm), ("store\nops", -so),
             ("pack", -pk), ("unalloc", -res), ("fixed base\n12 mo", -fx), ("EBIT", None)]
    run = 0.0
    for x, (lab, v) in enumerate(steps):
        if lab == "EBIT":
            L = ebit/1e5
            ax.bar(x, L, width=.62, color=c["pos"], alpha=.95, zorder=3)
            ax.text(x, L+8, f"{L:,.0f}", ha="center", va="bottom", fontsize=7.4,
                    color=c["pos"], fontweight="bold", zorder=5)
            continue
        L = v/1e5
        if x == 0:
            ax.bar(x, L, width=.62, color=c["fg"], alpha=.92, zorder=3); run = L
            ax.text(x, L+8, f"{L:,.0f}", ha="center", va="bottom", fontsize=7.4,
                    color=c["fg"], fontweight="bold", zorder=5)
        else:
            ax.bar(x, abs(L), bottom=run+L, width=.62, color=c["neg"], alpha=.8, zorder=3)
            ax.plot([x-.31, x-.69], [run, run], lw=.7, color=c["grid"], zorder=2)
            ax.text(x, run+8, f"-{abs(L):,.0f}", ha="center", va="bottom", fontsize=6.4,
                    color=c["neg"], fontweight="bold", zorder=5)
            run += L
    ax.text(0.02, .96, f"NOV ₹{nov/1e7:,.1f} cr  ·  {n:,.0f} orders  ·  AOV ₹{aov:,.0f}",
            transform=ax.transAxes, fontsize=6.2, color=c["mute"], va="top")
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels([s_[0] for s_ in steps], fontsize=5.8, color=c["mute"], linespacing=1.15)
    ax.set_ylabel("₹ lakh / node / year", fontsize=6.2, color=c["mute"])
    ax.set_ylim(0, rev/1e5*1.22)
    ax.tick_params(labelsize=6.0, colors=c["mute"])
    for s_ in ["top", "right"]: ax.spines[s_].set_visible(False)
    for s_ in ["left", "bottom"]: ax.spines[s_].set_color(c["grid"])
    ax.grid(axis="y", color=c["grid"], lw=.45, alpha=.45, zorder=0)
    save(fig, "pnl_bridge", T)


if __name__ == "__main__":
    for T in ("light", "dark"):
        roce_ladder(T); pnl_bridge(T)
    print("charts6: roce_ladder, pnl_bridge written for light and dark")
