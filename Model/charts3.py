"""
CC-2 new figures, restated model (S18/S19/S21/S26):
  9.  basket ladder       -- Rs450 -> 525 -> 580, the path to the breakeven AOV
  10. relocate vs hold    -- Rs21.3L / 31.6L / 89L / 178L
  11. asset-turn identity -- 1.333 x 0.708 = 0.944, density buys back the calendar
  12. risk tornado (S8)   -- the four priced shocks on ONE axis: breakeven campus AOV

Every number is read from the model. No figure is typed into this file.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from charts import THEMES, save, D2_LAST_MILE, BREAKEVEN_AOV
import campus_model as M, basket as BK, break_mode as B
import risk_shocks as RS
plt.rcParams["font.family"] = "DejaVu Sans"


# ============ 9. BASKET LADDER (S21) ============
def basket_ladder(T):
    c = THEMES[T]
    rows, need = BK.ladder()                       # [(label, aov, note), ...]
    labels = ["Minutes\nnetwork\ntoday",
              "+ term-start\ndurable\noccasions",
              f"+ non-grocery\nmix to {need:.0f}%\nof GOV"]
    vals = [r[1] for r in rows]                    # 450, ~525, 580
    target = vals[-1]
    fig, ax = plt.subplots(figsize=(3.4, 2.15))

    run = 0.0
    for i, v in enumerate(vals):
        if i == 0:
            ax.bar(i, v, color=c["accent"], width=.60, zorder=3)
            ax.text(i, v + 8, f"Rs{v:.0f}", ha="center", va="bottom",
                    fontsize=8.5, color=c["fg"], fontweight="bold")
            run = v
        else:
            step = v - run
            ax.bar(i, step, bottom=run, color=c["pos"], width=.60, zorder=3)
            ax.plot([i - .30, i - .70], [run, run], color=c["grid"], lw=.9, zorder=2)
            if i < len(vals) - 1:                    # last bar's value is the breakeven line
                ax.text(i, v + 10, f"Rs{v:.0f}", ha="center", va="bottom",
                        fontsize=8.5, color=c["fg"], fontweight="bold")
            ax.text(i, run + step / 2, f"+{step:.0f}", ha="center", va="center",
                    fontsize=7, color="white", fontweight="bold")
            run = v

    ax.axhline(target, color=c["hi"], lw=1.4, ls="--", zorder=1)
    ax.text(2.34, target + 6, f"breakeven Rs{target:.0f}", fontsize=6.6, color=c["hi"],
            va="bottom", ha="right", fontweight="bold")
    ax.set_xticks(range(3)); ax.set_xticklabels(labels, fontsize=6.3, color=c["mute"])
    ax.set_ylim(0, target * 1.28); ax.set_xlim(-0.6, 2.7)
    ax.set_yticks([0, 200, 400, 600]); ax.tick_params(labelsize=6.5, colors=c["mute"])
    ax.set_ylabel("Campus AOV (Rs, gross)", fontsize=7, color=c["mute"])
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]: ax.spines[s].set_color(c["grid"])
    ax.grid(axis="y", color=c["grid"], lw=.45, alpha=.5, zorder=0)
    save(fig, "basket_ladder", T)


# ============ 10. RELOCATE vs HOLD (S21) ============
def relocate_hold(T):
    c = THEMES[T]
    d = B.relocate_vs_flex()
    bars = [("Hold through break\n(small-format lever)", d["flex_total"],       c["pos"]),
            ("Do nothing\nthrough the break",            d["do_nothing_total"], c["accent"]),
            ("Relocate:\nbuild one replacement",         d["relocate_once"],    c["neg"]),
            ("Relocate AND\nreturn next term",           d["relocate_and_return"], c["neg"])]
    fig, ax = plt.subplots(figsize=(4.0, 2.2))
    ys = np.arange(len(bars))[::-1]
    for y, (lab, val, col) in zip(ys, bars):
        ax.barh(y, val / 1e5, height=.58, color=col, alpha=.9, zorder=3)
        ax.text(val / 1e5 + 3, y, f"Rs{val/1e5:.1f}L", va="center", fontsize=7.4,
                color=c["fg"], fontweight="bold")
        ax.text(-6, y, lab, va="center", ha="right", fontsize=6.3, color=c["fg"])
    ax.set_xlim(0, d["relocate_and_return"] / 1e5 * 1.20)
    ax.set_ylim(-0.6, len(bars) - 0.4)
    ax.set_yticks([]); ax.tick_params(labelsize=6.3, colors=c["mute"])
    ax.set_xlabel("Rs lakh", fontsize=7, color=c["mute"])
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(c["grid"])
    ax.text(.5, -.32, f"holding the node = {d['flex_vs_relocate']:.0%} of ONE relocation, "
            f"and the catchment is not lost", transform=ax.transAxes, fontsize=5.9,
            color=c["mute"], ha="center", style="italic")
    save(fig, "relocate_hold", T)


# ============ 11. ASSET-TURN IDENTITY (S18) ============
def asset_turn_identity(T):
    c = THEMES[T]
    dens = M.CEILING / M.MINUTES_ORD          # 1.333  (throughput density)
    cal  = M.ACTIVE_MONTHS / 12.0             # 0.708  (calendar, = 1/1.412)
    ratio = M.TURN_RATIO                      # 0.944
    fig, ax = plt.subplots(figsize=(4.2, 1.7))
    ax.axis("off")

    def chip(x, w, val, top, bot, col, tc="white"):
        ax.add_patch(FancyBboxPatch((x, 0.30), w, 0.42,
                     boxstyle="round,pad=0.01,rounding_size=0.03", fc=col, ec="none"))
        ax.text(x + w / 2, 0.60, val, ha="center", va="center", fontsize=13,
                fontweight="bold", color=tc)
        ax.text(x + w / 2, 0.90, top, ha="center", va="center", fontsize=6.6, color=c["mute"])
        ax.text(x + w / 2, 0.14, bot, ha="center", va="center", fontsize=6.2, color=c["mute"])

    chip(0.02, 0.24, f"{dens:.3f}", "campus / city\nthroughput", f"+{(dens-1)*100:.1f}%", c["pos"])
    ax.text(0.30, 0.51, "x", ha="center", va="center", fontsize=13, color=c["fg"])
    chip(0.34, 0.24, f"{cal:.3f}", "active months\n/ 12", f"-{(1-cal)*100:.1f}%", c["neg"])
    ax.text(0.62, 0.51, "=", ha="center", va="center", fontsize=13, color=c["fg"])
    chip(0.66, 0.30, f"{ratio:.3f}", "campus asset turn\nas a share of city", "the dead zone costs\n"
         f"{(1-ratio)*100:.1f} pts, not 30", c["hi"], tc=c["fg"] if T == "light" else "#0D1F5C")

    ax.text(0.5, 1.14, "DENSITY BUYS BACK THE CALENDAR", ha="center", fontsize=7.4,
            color=c["fg"], fontweight="bold")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.25)
    save(fig, "asset_turn_identity", T)


# ============ 12. RISK TORNADO, SLIDE 8 (S8) ============
def risk_tornado(T):
    """Four priced shocks on ONE axis: breakeven campus AOV. All from risk_shocks.py."""
    c = THEMES[T]
    base = RS.BASE_AOV
    rows = RS.SHOCKS                                   # already ranked, worst first
    fig, ax = plt.subplots(figsize=(4.6, 2.35))

    # the basket lever's coverage band, behind the bars
    ax.axvspan(base, RS.AOV_CEILING_LO, color=c["pos"], alpha=.10, zorder=0)
    ax.axvspan(RS.AOV_CEILING_LO, RS.AOV_CEILING_HI, color=c["hi"], alpha=.12, zorder=0)
    for x, lab in ((RS.AOV_CEILING_LO, f"{BK.NONGROCERY_CEILING_LO:.0f}% non-grocery"),
                   (RS.AOV_CEILING_HI, f"{BK.NONGROCERY_CEILING:.0f}% ceiling")):
        ax.axvline(x, color=c["hi"], lw=1.1, ls=(0, (3, 2)), zorder=2)
        ax.text(x, len(rows) - 0.32, f"Rs{x:.0f}\n{lab}", fontsize=5.6, color=c["hi"],
                ha="center", va="bottom", fontweight="bold")

    for i, (name, aov, _why) in enumerate(rows):
        y = len(rows) - 1 - i
        over = aov > RS.AOV_CEILING_LO
        ax.barh(y, aov - base, left=base, height=.46,
                color=c["neg"] if over else c["accent"], alpha=.9, zorder=3)
        ax.text(base - 2.5, y, name, ha="right", va="center", fontsize=6.3, color=c["fg"])
        ax.text(aov + 2.5, y, f"Rs{aov:.0f}", ha="left", va="center", fontsize=6.6,
                color=c["neg"] if over else c["fg"], fontweight="bold")

    ax.axvline(base, color=c["fg"], lw=1.4, zorder=4)
    ax.text(base - 2.5, -0.72, f"base Rs{base:.0f}", fontsize=6.4, color=c["fg"],
            ha="right", va="center", fontweight="bold")
    ax.set_xlim(base - 78, RS.AOV_CEILING_HI + 16)
    ax.set_ylim(-1.05, len(rows) + 0.55)
    ax.set_yticks([]); ax.tick_params(labelsize=6, colors=c["mute"])
    ax.set_xlabel("D2-consistent breakeven campus AOV (Rs)", fontsize=6.5, color=c["mute"])
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(c["grid"])
    ax.text(.5, -.30, "shaded = AOV the basket lever reaches inside management's stated "
            "30-40% non-grocery ceiling", transform=ax.transAxes, fontsize=5.5,
            color=c["mute"], ha="center", style="italic")
    save(fig, "risk_tornado", T)


for T in THEMES:
    basket_ladder(T); relocate_hold(T); asset_turn_identity(T); risk_tornado(T)
print("charts3 written")
