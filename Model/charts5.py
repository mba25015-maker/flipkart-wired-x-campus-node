"""
Figures for SEMI-FINAL slide 2 — the market, and the two facts that reframe it.

  15. universe_narrow (S2)  54,014 colleges -> 21,000 urban -> 17,805 urban non-metro.
                            We shrink our own TAM on slide 2. No other team opens this way.
  16. metro_squeeze   (S2)  the densification wall: stores added vs NEW pin codes reached,
                            and the five-operator overlap that bought.

Nothing is typed. If a number is not in the model, this file does not draw it.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from charts import THEMES, save
import aishe_district as AD
plt.rcParams["font.family"] = "DejaVu Sans"


# ============ 15. THE UNIVERSE NARROWS (slide 2, left) ============
def universe_narrow(T):
    """Three stages, each one smaller, each one sourced from the same register."""
    c = THEMES[T]
    stages = [(AD.N_COL,                    "colleges in the\nAISHE register",      c["mute"]),
              (AD.URBAN_COL,                "are URBAN\n(six in ten are rural)",    c["fg"]),
              (AD.NON_METRO_URBAN_COLLEGES, "urban and NON-METRO\n— the archetype", c["hi"])]
    fig, ax = plt.subplots(figsize=(4.30, 1.78))
    ax.set_xlim(0, 10); ax.set_ylim(0.9, 10); ax.axis("off")
    top = stages[0][0]
    for i,(n, lab, col) in enumerate(stages):
        h = 5.6*n/top
        x = 0.25 + i*3.25
        ax.add_patch(plt.Rectangle((x, 2.35), 2.55, h, facecolor=col, alpha=.92,
                                   edgecolor="none", zorder=2))
        ax.text(x+1.275, 2.35+h+0.55, f"{n:,}", ha="center", va="center", fontsize=13,
                color=col, fontweight="bold", zorder=3)
        ax.text(x+1.275, 1.35, lab, ha="center", va="center", fontsize=6.0,
                color=c["mute"], linespacing=1.25, zorder=3)
        if i:
            ax.text(x-0.35, 4.2, "▶", ha="center", va="center", fontsize=6.5, color=c["mute"])
    ax.text(0.25, 9.55,
            f"URBAN SHARE {AD.URBAN_SHARE_COL:.1%} — the campus micro-market universe is "
            f"{AD.URBAN_COL:,} colleges, not {AD.N_COL:,}",
            fontsize=6.2, color=c["fg"], fontweight="bold", va="center")
    save(fig, "universe_narrow", T)


# ============ 16. THE METRO SQUEEZE (slide 2, right) ============
def metro_squeeze(T):
    """The marginal store is stacking, not reaching — in two pictures that share a story."""
    c = THEMES[T]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(4.30, 1.78),
                                 gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=.55))

    # --- left: 900 stores bought 152 new pin codes ---
    vals = [AD.STORES_ADDED_Q, AD.PIN_CODES_ADDED_Q]
    a1.bar([0,1], vals, width=.58, color=[c["accent"], c["accent"]], alpha=.85, zorder=3)
    for i,v in enumerate(vals):
        a1.text(i, v+22, f"{v:,}", ha="center", va="bottom", fontsize=8.6,
                color=c["fg"], fontweight="bold")
    a1.set_xticks([0,1])
    a1.set_xticklabels(["stores added\nApr–Jul 2026","NEW pin codes\nthey reached"],
                       fontsize=5.8, color=c["mute"], linespacing=1.25)
    a1.set_ylim(0, max(vals)*1.44)
    a1.set_yticks([]); a1.tick_params(labelsize=5.8, colors=c["mute"])
    for s in ["top","right","left"]: a1.spines[s].set_visible(False)
    a1.spines["bottom"].set_color(c["grid"])
    a1.text(.5, max(vals)*1.33, f"{AD.STORES_PER_NEW_PINCODE:.1f} stores per new pin code",
            ha="center", va="center", fontsize=6.2, color=c["neg"], fontweight="bold")

    # --- right: what that density bought, in one quarter ---
    ov = [AD.METRO_OVERLAP_PRIOR, AD.METRO_OVERLAP_5OP]
    a2.plot([0,1], ov, marker="o", ms=4.5, lw=1.8, color=c["neg"], zorder=3)
    for i,v in enumerate(ov):
        a2.text(i, v+.035, f"{v:.0%}", ha="center", va="bottom", fontsize=8.6,
                color=c["fg"], fontweight="bold")
    a2.set_xlim(-.35,1.35); a2.set_ylim(0, .62)
    a2.set_xticks([0,1]); a2.set_xticklabels(["Apr 2026","Jul 2026"], fontsize=5.8, color=c["mute"])
    a2.set_yticks([]); 
    for s in ["top","right","left"]: a2.spines[s].set_visible(False)
    a2.spines["bottom"].set_color(c["grid"])
    a2.text(.5, .58, "metro pin codes served by ALL FIVE majors",
            ha="center", va="center", fontsize=6.0, color=c["mute"])
    a2.text(.5, .12, f"{AD.METRO_STORES:,} metro stores against\n{AD.METRO_SUSTAINABLE:,} of sustainable capacity"
                     f"  (+{AD.METRO_EXCESS:.0%})",
            ha="center", va="center", fontsize=6.0, color=c["fg"], fontweight="bold",
            linespacing=1.3)
    save(fig, "metro_squeeze", T)


if __name__ == "__main__":
    for T in ("light","dark"):
        universe_narrow(T); metro_squeeze(T)
    print("charts5: universe_narrow, metro_squeeze written for light and dark")
