"""IndiaStat / NSS layer: variable screening and robustness tests."""
import pandas as pd, numpy as np, warnings, glob, os
warnings.filterwarnings("ignore")
from scipy.stats import spearmanr
import index_model as I
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # repo root, portable across sessions
BASE=_os.path.join(_ROOT, "Research Pulls", "India stat")
_CACHE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "cache")

def rd(f):
    """Parse the licensed table, or read the cached parse the repository ships.

    ONE CODE PATH. The public repository used to carry a SEPARATE VARIANT of this module, and
    model_drift/original vs model_drift/public showed the two producing different output. What is
    cached here is the PARSED TABLE, generated from the source by Model/make_public_data.py - a
    projection of the licensed data, not a second model, and not row-level source."""
    cached = _os.path.join(_CACHE, f.replace(" ", "_").replace(".", "_") + ".csv")
    src = _os.path.join(BASE, f)
    if not _os.path.exists(src) and _os.path.exists(cached):
        return pd.read_csv(cached)
    raw=open(src,encoding="utf-8",errors="ignore").read()
    return pd.read_html(raw)[0].dropna(how="all").reset_index(drop=True)

# ---- A. digital saturation: 15-24 urban daily internet use ----
t=rd("person statewise.xls").iloc[3:].copy()
t.columns=["State","dR","dU","dA","wR","wU","wA","nR","nU","nA"]
t["dU"]=pd.to_numeric(t.dU,errors="coerce")
DIG=t.dropna(subset=["dU"])[["State","dU"]].rename(columns={"dU":"DailyUseUrban"})
dig_stats=dict(n=len(DIG),mean=DIG.DailyUseUrban.mean(),sd=DIG.DailyUseUrban.std(),
               lo=DIG.DailyUseUrban.min(),hi=DIG.DailyUseUrban.max())

# ---- B. gender parity, 15-29 urban ----
g=rd("15-29. 3.xls").iloc[3:].copy()
g.columns=["State","rM","rF","rP","uM","uF","uP","aM","aF","aP"]
for c in ("uM","uF"): g[c]=pd.to_numeric(g[c],errors="coerce")
g=g.dropna(subset=["uM","uF"]); g["gap"]=g.uM-g.uF
gender=dict(n=len(g),mean=g.gap.mean(),median=g.gap.median())

# ---- C. coefficient of variation: is the variable worth indexing on? ----
def cv(s): s=pd.to_numeric(s,errors="coerce").dropna(); return s.std()/s.mean()*100
CV = {"Campus concentration":cv(I.g.Concentration),
      "Hostel residents":cv(I.g.Residents),
      "Urban MPCE":cv(I.g.MPCE),
      "Daily internet use, 15-24 urban":cv(DIG.DailyUseUrban)}

# ---- D. concentration stability, AISHE T-42 ----
C5={"Andhra Pradesh":(547,517),"Assam":(870,864),"Bihar":(1703,1884),"Chhattisgarh":(557,482),
"Delhi":(1620,1747),"Gujarat":(528,515),"Haryana":(590,601),"Himachal Pradesh":(541,555),
"Jammu & Kashmir":(721,544),"Jharkhand":(1938,1611),"Karnataka":(415,433),"Kerala":(575,552),
"Madhya Pradesh":(771,709),"Maharashtra":(670,607),"Odisha":(659,525),"Punjab":(521,506),
"Rajasthan":(517,452),"Tamil Nadu":(872,840),"Telangana":(545,618),"West Bengal":(1175,1084),
"Uttar Pradesh":(742,735)}
c5=pd.DataFrame([{"State":k,"y2019":v[0],"y2023":v[1]} for k,v in C5.items()])
rho_conc,p_conc=spearmanr(c5.y2019,c5.y2023)

# ---- E. purchasing-power axis swap ----
NSDP={"Andhra Pradesh":266240,"Assam":153000,"Bihar":66828,"Chhattisgarh":167000,"Delhi":461910,
"Gujarat":323000,"Haryana":352000,"Himachal Pradesh":247000,"Jammu & Kashmir":168000,
"Jharkhand":110000,"Karnataka":382000,"Kerala":298000,"Madhya Pradesh":160000,"Maharashtra":320000,
"Odisha":179000,"Punjab":229000,"Rajasthan":184000,"Tamil Nadu":341000,"Telangana":384000,
"Uttar Pradesh":98000,"Uttarakhand":293000,"West Bengal":161000}
gg=I.g.assign(NSDP=I.g.State.map(NSDP)).dropna(subset=["NSDP"]).copy()
nm=lambda s:(s-s.min())/(s.max()-s.min())
gg["alt"]=0.40*nm(gg.Concentration)+0.35*nm(gg.NSDP)+0.25*nm(gg.Residents)
rho_axis,_=spearmanr(gg.COI,gg.alt)
top_mpce=list(gg.sort_values("COI",ascending=False).State[:5])
top_nsdp=list(gg.sort_values("alt",ascending=False).State[:5])
overlap=len(set(top_mpce)&set(top_nsdp))

if __name__=="__main__":
    print(f"A. digital saturation  n={dig_stats['n']}  mean {dig_stats['mean']:.1f}%  sd {dig_stats['sd']:.2f}  range {dig_stats['lo']:.1f}-{dig_stats['hi']:.1f}")
    print(f"B. gender gap  mean {gender['mean']:.1f}pp  median {gender['median']:.1f}pp  n={gender['n']}")
    print("C. coefficient of variation across the states we choose between:")
    for k,v in sorted(CV.items(),key=lambda kv:-kv[1]): print(f"     {k:<34} {v:5.1f}%")
    print(f"D. concentration stability  rho={rho_conc:.3f}  p={p_conc:.1e}")
    print(f"E. axis swap  rho={rho_axis:.3f}  top-5 overlap {overlap}/5")
