import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, os
from matplotlib.patches import Polygon, FancyBboxPatch, Wedge, Circle
import campus_model as M, cost_stack as C, sla as SL

# ---- restated economics, read from the model (S18/S19/S21) -------------------
D2_LAST_MILE = SL.volume_weighted()[1]                       # Rs19.0/order, D2 circuit model
D2_CONS      = M.LAST_MILE / D2_LAST_MILE                    # 2.21x implied consolidation
BREAKEVEN_AOV = C.breakeven_d2_consistent(C.CAMPUS_FIXED, D2_LAST_MILE)   # Rs580, D2-consistent

def _cm_d2(aov):
    """Contribution per order on the D2-consistent last-mile basis."""
    return M.TAKE_RATE*aov - (D2_LAST_MILE + M.STORE_OPS + M.PACKAGING + M.RESIDUAL)

def _opd_to_breakeven(aov):
    """Orders/day the campus fixed base needs at this AOV (calendar-adjusted)."""
    c = _cm_d2(aov)
    return np.nan if c <= 0 else C.CAMPUS_FIXED/30.0*M.CAL_SURCHARGE/c

THEMES = {
 "light": dict(bg="none", fg="#0D1F5C", mute="#5A6785", grid="#D9E0F0",
               pos="#1E7A46", neg="#C0392B", accent="#0D1F5C", hi="#F5B301",
               band="#EEF3FF", card="#FFFFFF"),
 "dark":  dict(bg="none", fg="#FFFFFF", mute="#D3DEF7", grid="#2C4180",
               pos="#4ED08A", neg="#FF7B6B", accent="#FFFFFF", hi="#FFC220",
               band="#16296B", card="#0D1F5C"),
}
plt.rcParams["font.family"]="DejaVu Sans"

def save(fig, name, theme):
    d=f"charts/{theme}"; os.makedirs(d,exist_ok=True)
    fig.savefig(f"{d}/{name}.png", dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

# ============ 1. THREE WATERFALLS (hero, slide 2) ============
def waterfalls(T):
    c=THEMES[T]
    # restated at S18/S19: network AOV has converged to Rs450; the D2 circuit model
    # replaces the 3x proxy; the minimum viable campus AOV is Rs580.
    scen=[("MINUTES NETWORK TODAY",
           f"AOV Rs{M.MINUTES_AOV:.0f} - baseline batch {C.BATCH_BASE:.1f}x",
           M.MINUTES_AOV, C.BATCH_BASE),
          ("CAMPUS ON A STUDENT BASKET",
           f"AOV Rs{M.MINUTES_AOV:.0f} - D2 circuit, {D2_CONS:.1f}x consolidation",
           M.MINUTES_AOV, D2_CONS),
          ("CAMPUS AT BREAKEVEN",
           f"AOV Rs{BREAKEVEN_AOV:.0f} - D2 circuit, {D2_CONS:.1f}x consolidation",
           BREAKEVEN_AOV, D2_CONS)]
    fig,axes=plt.subplots(1,3,figsize=(9.3,2.32),sharey=True)
    for ax,(t,sub,aov,cons) in zip(axes,scen):
        net=M.TAKE_RATE*aov; lm=M.LAST_MILE/cons
        steps=[("Net\nrevenue",net,"base"),("Last\nmile",-lm,"cost"),
               ("Store\nops",-M.STORE_OPS,"cost"),("Pack\n+ supp",-M.PACKAGING,"cost"),
               ("Unalloc.",-M.RESIDUAL,"cost")]
        cm=net-lm-M.STORE_OPS-M.PACKAGING-M.RESIDUAL
        run=0.0
        for i,(lab,val,kind) in enumerate(steps):
            if kind=="base":
                ax.bar(i,val,bottom=0,color=c["accent"],width=.62,zorder=3)
                ax.text(i,val+3,f"{val:.0f}",ha="center",va="bottom",fontsize=8.5,
                        color=c["fg"],fontweight="bold")
                run=val
            else:
                ax.bar(i,val,bottom=run,color=c["neg"],width=.62,alpha=.9,zorder=3)
                if abs(val) >= 16:      # label fits inside the bar
                    ax.text(i,run+val/2,f"{val:.0f}",ha="center",va="center",fontsize=8,
                            color="white",fontweight="bold")
                else:                   # bar too short - label to the left, cost colour
                    ax.text(i-0.40,run+val/2,f"{val:.0f}",ha="right",va="center",fontsize=7,
                            color=c["neg"],fontweight="bold")
                ax.plot([i-0.31,i+0.31],[run,run],color=c["grid"],lw=.8,zorder=2)
                run+=val
        col=c["pos"] if cm>0 else c["neg"]
        ax.bar(5,cm,bottom=0,color=col,width=.62,zorder=3)
        ax.text(5,cm+(9 if cm>0 else -9),f"{cm:+.0f}",ha="center",
                va="bottom" if cm>0 else "top",fontsize=10,color=col,fontweight="bold")
        ax.axhline(0,color=c["mute"],lw=1,zorder=4)
        ax.set_xlim(-0.7,5.7)
        ax.set_xticks(range(6)); ax.set_xticklabels([s[0] for s in steps]+["CM /\norder"],
                                                    fontsize=6.2,color=c["mute"])
        ax.text(0,1.155,t,transform=ax.transAxes,fontsize=8.2,color=c["fg"],
                fontweight="bold",ha="left",va="bottom")
        ax.text(0,1.035,sub,transform=ax.transAxes,fontsize=6.6,color=c["mute"],
                ha="left",va="bottom")
        for s in ax.spines.values(): s.set_visible(False)
        ax.tick_params(left=False,bottom=False); ax.set_ylim(-55,175)
        ax.grid(axis="y",color=c["grid"],lw=.5,alpha=.5,zorder=0)
    axes[0].set_yticks([-50,0,50,100,150]); axes[0].tick_params(labelsize=7,colors=c["mute"])
    axes[0].set_ylabel("Rs per order",fontsize=7.5,color=c["mute"])
    for ax in axes[1:]: ax.set_yticks([])
    fig.subplots_adjust(wspace=.13)
    save(fig,"waterfall",T)

# ============ 2. THE VIABILITY CLIFF (slide 2) ============
def cliff(T):
    c=THEMES[T]
    fig,ax=plt.subplots(figsize=(4.5,2.35))
    aovs=np.arange(440,700,2)
    od=[_opd_to_breakeven(a) for a in aovs]          # campus fixed base + D2 circuit last mile
    ax.plot(aovs,od,color=c["accent"],lw=2.4,zorder=4)
    ax.axhline(M.CEILING,color=c["hi"],lw=1.6,ls="--",zorder=3)
    ax.text(690,M.CEILING,"1,400/day\nobserved\nceiling",fontsize=6.8,color=c["hi"],
            va="center",ha="left",fontweight="bold")
    ax.fill_between(aovs,od,7000,where=(np.array(od)>M.CEILING),color=c["neg"],alpha=.10,zorder=1)
    ax.fill_between(aovs,0,od,where=(np.array(od)<=M.CEILING),color=c["pos"],alpha=.12,zorder=1)
    xcross=aovs[np.argmin(np.abs(np.array(od)-M.CEILING))]
    ax.scatter([xcross],[M.CEILING],s=48,color=c["hi"],zorder=6,ec=c["card"],lw=1.2)
    ax.annotate("",(xcross,M.CEILING),xytext=(xcross+30,2650),
                arrowprops=dict(arrowstyle="-",color=c["mute"],lw=.8))
    ax.text(xcross+32,3050,f"Rs{xcross:.0f}",fontsize=11,color=c["fg"],fontweight="bold")
    ax.text(xcross+32,2500,"minimum viable\ncampus AOV\n(D2-consistent)",fontsize=6.8,color=c["mute"],va="top")
    ax.set_ylim(0,6000); ax.set_xlim(440,685)
    ax.set_xlabel("Campus AOV (Rs)",fontsize=7.5,color=c["mute"])
    ax.set_ylabel("Orders/day to break even",fontsize=7.5,color=c["mute"])
    ax.tick_params(labelsize=7,colors=c["mute"])
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    for s in ["left","bottom"]: ax.spines[s].set_color(c["grid"])
    ax.grid(color=c["grid"],lw=.45,alpha=.5,zorder=0)
    save(fig,"cliff",T)

# ============ 3. REACHABILITY FUNNEL (slide 1) ============
def funnel(T):
    c=THEMES[T]
    fig,ax=plt.subplots(figsize=(4.35,2.75))
    rows=[("4.46 cr","Total higher-ed enrolment","100%",1.00),
          ("87.7 L","Hostel capacity built","19.7%",0.80),
          ("49.4 L","Actually residing in hostels","11.1%",0.62),
          ("Sub-set","Clears the cluster scale gate","< 11%",0.44)]
    cols=([c["accent"],"#3355A6",c["pos"],c["hi"]] if T=="light"
          else ["#8FB0FF","#4B6FD6","#2E9E6B","#FFC220"])
    y=1.0; h=0.205; gap=0.045
    for (big,lab,pct,w),col in zip(rows,cols):
        x=(1-w)/2
        ax.add_patch(FancyBboxPatch((x,y-h),w,h,boxstyle="round,pad=0.004,rounding_size=0.012",
                                    fc=col,ec="none"))
        tc="#0D1F5C" if col in (c["hi"],"#FFC220","#8FB0FF") else "white"
        ax.text(x+0.022,y-h/2,big,fontsize=11.5,fontweight="bold",color=tc,va="center")
        ax.text(1.05,y-h/2+0.028,pct,fontsize=8.6,color=c["fg"],fontweight="bold",va="center",ha="left")
        ax.text(1.05,y-h/2-0.045,lab,fontsize=7.5,color=c["mute"],va="center",ha="left")
        if y>1.0-3*(h+gap):
            ax.annotate("",xy=(0.5,y-h-gap+0.008),xytext=(0.5,y-h-0.004),
                        arrowprops=dict(arrowstyle="-|>",color=c["grid"],lw=1.1))
        y-=h+gap
    ax.set_xlim(-0.02,2.05); ax.set_ylim(y+0.02,1.03); ax.axis("off")
    save(fig,"funnel",T)

# ============ 4. 24-HOUR DEMAND RIBBON (slide 1) ============
def curfew(T):
    c=THEMES[T]
    fig,ax=plt.subplots(figsize=(4.35,1.6))
    hours=np.arange(0,24)
    # illustrative shape, labelled as such on-slide: late-evening + late-night double peak
    shape=np.array([.55,.30,.14,.06,.04,.05,.12,.28,.40,.34,.30,.36,
                    .52,.44,.34,.32,.40,.58,.74,.88,1.00,.95,.82,.70])
    for i,(y,lab) in enumerate([(1,"24x7 PERMITTED"),(0,"CURFEW-CAPPED, 8 PM")]):
        for h in hours:
            live = True if y==1 else (h<20 and h>=6)
            col = c["hi"] if (live and shape[h]>0.55) else (c["accent"] if live else c["grid"])
            al  = 1.0 if live else 0.35
            ax.add_patch(FancyBboxPatch((h+.09,y+.12),0.82,shape[h]*0.62,
                        boxstyle="round,pad=0,rounding_size=0.06",fc=col,ec="none",alpha=al))
        ax.text(-0.4,y+0.40,lab,fontsize=7,color=c["fg"],fontweight="bold",ha="right",va="center")
    ax.axvline(20,ymin=0.02,ymax=0.46,color=c["neg"],lw=1.4,ls=(0,(3,2)))
    ax.text(20.25,0.30,"peak lost",fontsize=7,color=c["neg"],fontweight="bold",va="center")
    for h,lab in [(0,"12a"),(6,"6a"),(12,"12p"),(18,"6p"),(23,"11p")]:
        ax.text(h+.5,-0.12,lab,fontsize=6.3,color=c["mute"],ha="center")
    ax.set_xlim(-7.2,24.6); ax.set_ylim(-0.22,1.92); ax.axis("off")
    save(fig,"curfew",T)

for T in THEMES:
    waterfalls(T); cliff(T); funnel(T); curfew(T)
print("charts written")
