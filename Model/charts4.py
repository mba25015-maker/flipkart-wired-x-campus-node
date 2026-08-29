"""
Figures for the SEMI-FINAL slides 5 and 6. Every value is read from the model.

  13. lever_ladder    (S5)  residual-demand threshold by lever configuration, drawn as a
                            descending ladder, with the gap the levers CANNOT close shaded.
  14. district_screen (S6)  the two-stage screen: 760 districts -> 111 candidates, then the
                            contestedness bands inside our own candidate list.

Nothing is typed. If a number is not in the model, this file does not draw it.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from charts import THEMES, save
import break_mode as B, aishe_district as AD
plt.rcParams["font.family"] = "DejaVu Sans"


# ============ 13. THE LEVER LADDER (slide 5) ============
def lever_ladder(T):
    """Descending residual-demand threshold, and the gap the ladder cannot close.

    The point of the picture is NOT that the bars fall. It is that they stop falling
    while still far above zero: a break delivers no term-time demand, so the honest
    floor of the chart is 0% and the whole remaining bar is unfunded.
    """
    c = THEMES[T]
    rows = [(label, B.threshold(fn), B.threshold(fn) * B.TERM_OPD)
            for label, fn in B.CONFIGS]
    labels = [r[0] for r in rows]
    vals   = [r[1] * 100 for r in rows]
    opds   = [r[2] for r in rows]
    base, floor = vals[0], vals[-1]

    fig, ax = plt.subplots(figsize=(4.35, 1.72))
    ax.axhspan(0, floor, color=c["neg"], alpha=.10, zorder=0)
    ax.axhline(floor, color=c["neg"], lw=1.1, ls="--", zorder=4)

    for i, v in enumerate(vals):
        last = (i == len(vals) - 1)
        ax.bar(i, v, width=.62, zorder=3,
               color=c["accent"] if i == 0 else (c["hi"] if last else c["mute"]),
               alpha=1.0 if (i == 0 or last) else .55)
        ax.text(i, v + 1.6, f"{v:.1f}%", ha="center", va="bottom", fontsize=8.4,
                color=c["fg"], fontweight="bold", zorder=5)
        ax.text(i, v - 3.6, f"{opds[i]:,.0f}/day", ha="center", va="top", fontsize=6.0,
                color="white" if (i == 0 or last) else c["fg"], zorder=5)
        if i:
            ax.annotate("", xy=(i - .32, v), xytext=(i - .68, vals[i - 1]),
                        arrowprops=dict(arrowstyle="-", lw=.8, ls=":", color=c["grid"]),
                        zorder=2)
            ax.text(i - .5, (v + vals[i - 1]) / 2 + 3.0, f"-{vals[i-1]-v:.1f}pp",
                    ha="center", va="bottom", fontsize=6.0, color=c["mute"], zorder=5)

    # The shaded band is the residual NO lever reaches. It is labelled in the slide
    # caption rather than inside the axes, where it would sit on top of a bar.
    # the floor line is labelled in the slide caption, not here: at this scale a label
    # inside the axes lands on the last bar's own value.

    ax.set_xticks(np.arange(len(vals)))
    wrap = {"Do nothing": "Do\nnothing",
            "Labour flex only": "labour\nflex",
            "+ cold-chain right-sizing": "+ cold-chain\nright-size",
            "+ small-format node": "+ small-format\nnode"}
    ax.set_xticklabels([wrap.get(l, l) for l in labels],
                       fontsize=6.1, color=c["mute"], linespacing=1.2)
    ax.set_ylim(0, base * 1.22)
    ax.set_ylabel("residual demand required\n(% of term volume)", fontsize=6.4,
                  color=c["mute"], linespacing=1.2)
    ax.set_yticks([0, 25, 50, 75]); ax.tick_params(labelsize=6.2, colors=c["mute"])
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]: ax.spines[s].set_color(c["grid"])
    ax.grid(axis="y", color=c["grid"], lw=.45, alpha=.5, zorder=0)
    save(fig, "lever_ladder_s5", T)


# ============ 14. THE DISTRICT SCREEN (slide 6) ============
def district_screen(T):
    """Two stages, and the second one screens OUR OWN candidate list."""
    c = THEMES[T]
    fig, ax = plt.subplots(figsize=(4.30, 1.62))
    ax.set_xlim(0, 10); ax.set_ylim(1.55, 10); ax.axis("off")

    stage = [(f"{AD.N_DISTRICTS:,}", "districts in the\nAISHE register"),
             (f"{AD.N_CANDIDATES:,}", "clear the\nscreen")]
    for i, (big, small) in enumerate(stage):
        x = 0.2 + i * 2.05
        ax.add_patch(plt.Rectangle((x, 6.15), 1.80, 3.45, facecolor=c["band"],
                                   edgecolor=c["grid"], lw=.7, zorder=2))
        ax.text(x + 0.90, 8.55, big, ha="center", va="center", fontsize=13.5,
                color=c["fg"] if i == 0 else c["hi"], fontweight="bold", zorder=3)
        ax.text(x + 0.90, 6.95, small, ha="center", va="center", fontsize=5.8,
                color=c["mute"], linespacing=1.25, zorder=3)
    ax.annotate("", xy=(2.22, 7.9), xytext=(2.03, 7.9),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color=c["mute"]))
    crit = [(9.20, "not a metro", False),
            (8.42, f">= {AD.MIN_URBAN_COLLEGES} urban colleges", False),
            (7.64, f"urban share >= {AD.URBAN_SHARE_FLOOR:.0%}", False),
            (6.86, "one break segment >= 7 weeks", True)]
    for yy, txt, strong in crit:
        ax.plot([4.42], [yy], marker="s", ms=2.2, color=c["fg"] if strong else c["mute"])
        ax.text(4.70, yy, txt, fontsize=5.9, va="center",
                color=c["fg"] if strong else c["mute"],
                fontweight="bold" if strong else "normal")

    ax.text(0.2, 5.15, "AND THEN WE SCREENED OUR OWN LIST FOR INCUMBENT PRESENCE",
            fontsize=6.2, color=c["fg"], fontweight="bold", va="center")
    bands = [("uncontested", AD.PROX_COUNTS["uncontested"], c["pos"]),
             ("contested",   AD.PROX_COUNTS["contested"],   c["hi"]),
             ("stacked",     AD.PROX_COUNTS["stacked"],     c["neg"])]
    total = sum(b[1] for b in bands)
    x0, W = 0.2, 9.6
    for lab, n, col in bands:
        w = W * n / total
        ax.add_patch(plt.Rectangle((x0, 2.75), w, 1.60, facecolor=col, alpha=.88,
                                   edgecolor="none", zorder=2))
        ax.text(x0 + w / 2, 3.55, f"{n}", ha="center", va="center", fontsize=9.5,
                color="white", fontweight="bold", zorder=3)
        x0 += w
    for i, (lab, n, col) in enumerate(bands):          # legend row, evenly spaced
        lx = 0.2 + i * 3.25
        ax.add_patch(plt.Rectangle((lx, 1.92), .26, .26, facecolor=col, zorder=3))
        ax.text(lx + .42, 2.05, f"{lab} {n}", fontsize=6.0, va="center",
                color=c["fg"], fontweight="bold", zorder=3)
    save(fig, "district_screen", T)


if __name__ == "__main__":
    for T in ("light", "dark"):
        lever_ladder(T); district_screen(T)
    print("charts4: lever_ladder_s5, district_screen written for light and dark")
