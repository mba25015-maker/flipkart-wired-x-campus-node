"""Campus Opportunity Index. AISHE 2023-24 (T-31, T-42) + HCES 2023-24 urban MPCE."""
import pandas as pd, numpy as np, itertools, campus_model as M
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # repo root, portable across sessions

# AISHE 2023-24 T-42, avg enrolment per college (campus concentration)
CONC = {"Andhra Pradesh":517,"Arunachal Pradesh":642,"Assam":864,"Bihar":1884,"Chandigarh":1942,
"Chhattisgarh":482,"Delhi":1747,"Goa":646,"Gujarat":515,"Haryana":601,"Himachal Pradesh":555,
"Jammu & Kashmir":544,"Jharkhand":1611,"Karnataka":433,"Kerala":552,"Ladakh":432,
"Madhya Pradesh":709,"Maharashtra":607,"Manipur":742,"Meghalaya":961,"Mizoram":601,
"Nagaland":478,"Odisha":525,"Puducherry":671,"Punjab":506,"Rajasthan":452,"Sikkim":637,
"Tamil Nadu":840,"Telangana":618,"Tripura":1392,"Uttar Pradesh":735,"Uttarakhand":649,
"West Bengal":1084}
# AISHE 2023-24 T-31, total hostel students residing
RES = {"Andhra Pradesh":399991,"Arunachal Pradesh":10513,"Assam":84411,"Bihar":118504,
"Chandigarh":16086,"Chhattisgarh":60914,"Delhi":49229,"Goa":9117,"Gujarat":288923,
"Haryana":112444,"Himachal Pradesh":42897,"Jammu & Kashmir":30623,"Jharkhand":107395,
"Karnataka":590304,"Kerala":205476,"Ladakh":654,"Madhya Pradesh":130094,"Maharashtra":432483,
"Manipur":16953,"Meghalaya":11799,"Mizoram":5704,"Nagaland":9276,"Odisha":309561,
"Puducherry":23003,"Punjab":172815,"Rajasthan":153329,"Sikkim":5680,"Tamil Nadu":693996,
"Telangana":245113,"Tripura":8182,"Uttar Pradesh":355305,"Uttarakhand":65978,"West Bengal":176808}

_HCES = _os.path.join(_ROOT, "Research Pulls", "HCES.xlsx")
_MPCE_CSV = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data",
                          "hces_urban_mpce_2023_24.csv")
if _os.path.exists(_HCES):
    mp = pd.read_excel(_HCES, sheet_name="MonthlyPerCapitaConsumptionExpe", header=0)
    mp.columns=["Year","State","Sector","Imputation","MPCE"]
    urb = mp[(mp.Year=="2023-24")&(mp.Sector=="Urban")&(mp.Imputation=="Without Imputation")]
    MPCE = dict(zip(urb.State, urb.MPCE))
else:
    # The published urban MPCE series the repository ships, generated from the source.
    _m = pd.read_csv(_MPCE_CSV)
    MPCE = dict(zip(_m.iloc[:,0], _m.iloc[:,1]))
MPCE["Jammu & Kashmir"]=MPCE.get("Jammu & Kashmir", MPCE.get("Jammu and Kashmir"))

df = pd.DataFrame({"State":list(CONC)}).assign(
    Concentration=lambda d:d.State.map(CONC),
    Residents=lambda d:d.State.map(RES),
    MPCE=lambda d:d.State.map(MPCE)).dropna()

# ---- SCALE GATE, derived from campus_model, not chosen ----
OD_BE   = M.CEILING                                 # 1,400 orders/day, inside Blinkit's observed 1,334-1,487
import params as P
ORD_RES = P.ORDERS_PER_RESIDENT_DAY                  # [params] 1.5x Blinkit disclosed frequency
CLUSTER = OD_BE/ORD_RES                             # ~7,800 residents per viable cluster
MIN_CLUSTERS = P.MIN_CLUSTERS_PER_STATE
GATE = CLUSTER*MIN_CLUSTERS
df["Clusters supportable"] = (df.Residents/CLUSTER).round(1)
df["Clears gate"] = df.Residents >= GATE

g = df[df["Clears gate"]].copy()
def nm(s): return (s-s.min())/(s.max()-s.min())
W = {"Concentration":0.40,"MPCE":0.35,"Residents":0.25}
for k in W: g["n_"+k]=nm(g[k])
g["COI"] = sum(W[k]*g["n_"+k] for k in W)
g = g.sort_values("COI",ascending=False).reset_index(drop=True)
g["Rank"]=g.index+1

# ---- sensitivity: +/-10pp on every weight ----
base=list(g.State[:5]); flips={}
for d1,d2 in itertools.product([-.10,0,.10],repeat=2):
    w={"Concentration":W["Concentration"]+d1,"MPCE":W["MPCE"]+d2,
       "Residents":1-(W["Concentration"]+d1)-(W["MPCE"]+d2)}
    if min(w.values())<0: continue
    s=sum(w[k]*g["n_"+k] for k in w)
    top5=list(g.assign(x=s).sort_values("x",ascending=False).State[:5])
    for i,st in enumerate(top5):
        flips.setdefault(st,set()).add(i+1)
stable=[s for s in base if len(flips.get(s,{}))==1]

if __name__=="__main__":
    print(f"Breakeven orders/day (8.5-mo basis): {OD_BE:.0f}")
    print(f"Minimum viable CLUSTER: {CLUSTER:,.0f} hostel residents in one delivery radius")
    print(f"State screen (>={MIN_CLUSTERS} clusters): {GATE:,.0f} residents")
    print(f"States clearing gate: {len(g)} of {len(df)}\n")
    print(g[["Rank","State","Concentration","MPCE","Residents","Clusters supportable","COI"]]
          .head(12).to_string(index=False))
    print("\nExcluded (sub-scale):", ", ".join(df[~df["Clears gate"]].State))
    print(f"\nSensitivity: top-5 base = {base}")
    print(f"Rank-stable under +/-10pp on all weights: {stable}")
    print("Rank ranges:", {s:sorted(flips[s]) for s in base})
