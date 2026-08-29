import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, os
import index_model as I, campus_model as M, cost_stack as C
from charts import THEMES, save, D2_LAST_MILE, BREAKEVEN_AOV
plt.rcParams["font.family"]="DejaVu Sans"

# ---------- 5. CONCENTRATION x PURCHASING POWER SCATTER ----------
def scatter(T):
    c=THEMES[T]; g=I.g
    fig,ax=plt.subplots(figsize=(5.15,3.15))
    xm,ym=g.Concentration.median(), g.MPCE.median()
    ax.axvline(xm,color=c["grid"],lw=.9,zorder=1); ax.axhline(ym,color=c["grid"],lw=.9,zorder=1)
    ax.add_patch(plt.Rectangle((xm,ym),3000,6000,fc=c["pos"],alpha=.07,zorder=0))
    for _,r in g.iterrows():
        dense, rich = r.Concentration>=xm, r.MPCE>=ym
        col = c["pos"] if (dense and rich) else (c["hi"] if dense else (c["accent"] if rich else c["mute"]))
        ax.scatter(r.Concentration, r.MPCE, s=28+ (r.Residents/700000)*230,
                   color=col, alpha=.85, ec="none", zorder=3)
    lab={"Delhi":(-8,16),"Tamil Nadu":(13,7),"Karnataka":(9,10),"Bihar":(-10,12),
         "Telangana":(10,6),"Uttar Pradesh":(11,7),"Maharashtra":(10,-12),
         "West Bengal":(11,4),"Jharkhand":(-8,-14)}
    for st,(dx,dy) in lab.items():
        r=g[g.State==st]
        if not len(r): continue
        r=r.iloc[0]
        bold = st in ("Uttar Pradesh","Delhi","Tamil Nadu","Karnataka")
        ax.annotate(st,(r.Concentration,r.MPCE),textcoords="offset points",xytext=(dx,dy),
                    fontsize=7.4 if bold else 6.8,color=c["fg"] if bold else c["mute"],
                    fontweight="bold" if bold else "normal")
    r=g[g.State=="Uttar Pradesh"].iloc[0]
    ax.annotate("5th-largest hostel base,\n17th on the index",(r.Concentration,r.MPCE),
                textcoords="offset points",xytext=(64,-30),fontsize=6.5,color=c["neg"],
                ha="center",arrowprops=dict(arrowstyle="-",color=c["neg"],lw=.7))
    qk=dict(fontsize=7.0,fontweight="bold",transform=ax.transAxes)
    ax.text(.985,.965,"PRIORITY",color=c["pos"],ha="right",va="top",**qk)
    ax.text(.015,.965,"AFFLUENT, FRAGMENTED",color=c["accent"],ha="left",va="top",**qk)
    ax.text(.985,.035,"DENSE, LOW SPEND",color=c["hi"],ha="right",va="bottom",**qk)
    ax.text(.015,.035,"DEPRIORITISE",color=c["mute"],ha="left",va="bottom",**qk)
    ax.set_xlabel("Campus concentration  →  avg enrolment per college (AISHE T-42)",
                  fontsize=7.2,color=c["mute"])
    ax.set_ylabel("Purchasing power  →  urban MPCE, Rs (HCES)",fontsize=7.2,color=c["mute"])
    ax.set_xlim(330,2180); ax.set_ylim(4500,9850)
    ax.tick_params(labelsize=6.8,colors=c["mute"])
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    for s in ["left","bottom"]: ax.spines[s].set_color(c["grid"])
    ax.text(.5,-.20,"bubble = hostel residents  |  quadrant split at median",
            transform=ax.transAxes,fontsize=6.2,color=c["mute"],ha="center",style="italic")
    save(fig,"scatter",T)

# ---------- 6. RANK STABILITY (honest sensitivity) ----------
def rankrange(T):
    c=THEMES[T]
    fig,ax=plt.subplots(figsize=(3.05,1.62))
    items=[(s,sorted(I.flips[s])) for s in I.flips]
    items=sorted(items,key=lambda kv:(min(kv[1]),len(kv[1])))[:8]
    for i,(st,rk) in enumerate(items):
        y=len(items)-i
        lo,hi=min(rk),max(rk)
        stable = lo==hi or hi-lo<=1
        col=c["pos"] if stable else c["hi"]
        if hi>lo: ax.plot([lo,hi],[y,y],color=col,lw=4.4,solid_capstyle="round",zorder=3)
        else: ax.scatter([lo],[y],s=34,color=col,zorder=3)
        ax.text(-0.35,y,st,fontsize=6.6,color=c["fg"],ha="right",va="center")
        ax.text(hi+0.22,y,f"{lo}-{hi}" if hi>lo else f"{lo}",fontsize=6.3,
                color=c["mute"],va="center")
    ax.set_xlim(-4.6,8.2); ax.set_ylim(0.3,len(items)+0.7)
    ax.set_xticks(range(1,7)); ax.tick_params(labelsize=6,colors=c["mute"],left=False)
    ax.set_yticks([]); ax.set_xlabel("rank range across +/-10pp weight scenarios",
                                     fontsize=6.3,color=c["mute"])
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(c["grid"])
    save(fig,"rankrange",T)

# ---------- 7. BREAKEVEN-AOV TORNADO ----------
def tornado(T):
    c=THEMES[T]
    # restated at S19: breakeven is the D2-consistent AOV on the campus fixed base,
    # not full_breakeven_aov(3x) on the legacy base.
    be=lambda d2=D2_LAST_MILE,**kw: C.breakeven_d2_consistent(C.CAMPUS_FIXED, d2, **kw)
    base=be()
    drivers=[("D2 circuit last mile  +25% / -25%", be(D2_LAST_MILE*1.25), be(D2_LAST_MILE*0.75)),
             ("Throughput  1,334 / 1,487 per day", be(opd=M.CEIL_LO), be(opd=M.CEIL_HI)),
             ("Take rate  19.41% / 20.71%",        be(take=0.1941),    be(take=0.2071))]
    drivers=sorted(drivers,key=lambda d:-abs(d[1]-d[2]))
    fig,ax=plt.subplots(figsize=(3.7,1.95))
    for i,(lab,hi,lo) in enumerate(drivers):
        y=len(drivers)-i
        ax.barh(y,hi-base,left=base,height=.40,color=c["neg"],alpha=.85,zorder=3)
        ax.barh(y,lo-base,left=base,height=.40,color=c["pos"],alpha=.85,zorder=3)
        ax.text(537,y+0.34,lab,fontsize=6.2,color=c["fg"],ha="left",va="bottom")
        if abs(hi-base)>0.5: ax.text(hi+2,y,f"{hi:.0f}",fontsize=6.2,color=c["neg"],va="center")
        if abs(lo-base)>0.5: ax.text(lo-2,y,f"{lo:.0f}",fontsize=6.2,color=c["pos"],va="center",ha="right")
    ax.axvline(base,color=c["fg"],lw=1.2,zorder=4)
    ax.text(base,0.30,f"base Rs{base:.0f}",fontsize=6.4,color=c["fg"],ha="center",fontweight="bold")
    ax.set_xlim(533,617); ax.set_ylim(0.15,len(drivers)+0.95)
    ax.set_yticks([]); ax.tick_params(labelsize=6,colors=c["mute"])
    ax.set_xlabel("D2-consistent breakeven campus AOV (Rs)",fontsize=6.3,color=c["mute"])
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(c["grid"])
    save(fig,"tornado",T)

for T in THEMES: scatter(T); rankrange(T); tornado(T)
print("charts2 written")

# ---------- 8. WHICH VARIABLES ACTUALLY DISCRIMINATE ----------
def discriminate(T):
    import indiastat as S
    c=THEMES[T]
    fig,ax=plt.subplots(figsize=(2.28,1.16))
    items=sorted(S.CV.items(),key=lambda kv:kv[1])
    for i,(lab,v) in enumerate(items):
        dead = v<10
        col = c["neg"] if dead else c["accent"]
        ax.barh(i,v,height=.56,color=col,alpha=.92,zorder=3)
        ax.text(v+1.6,i,f"{v:.0f}%",fontsize=6.2,color=col,va="center",fontweight="bold")
        ax.text(-2,i,lab,fontsize=5.9,color=c["fg"] if not dead else c["neg"],
                ha="right",va="center",fontweight="bold" if dead else "normal")
    ax.text(28,0,"dropped",fontsize=5.9,color=c["neg"],va="center",style="italic")
    ax.set_xlim(-46,100); ax.set_ylim(-0.6,len(items)-0.4)
    ax.set_yticks([]); ax.tick_params(labelsize=5.6,colors=c["mute"])
    ax.set_xticks([0,25,50,75])
    ax.set_xlabel("coefficient of variation across candidate states",fontsize=5.7,color=c["mute"])
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(c["grid"])
    save(fig,"discriminate",T)

for T in THEMES: discriminate(T)
print("discriminate written")
