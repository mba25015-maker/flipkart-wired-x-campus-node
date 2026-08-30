"""
LT commercial electricity tariff by state - the last fully unsourced input in the fixed stack.

SOURCE: Indiastat, "State/Utility-wise Average Rate of Electricity Supply and Electricity Duty/Tax
{Commercial N KW}" in India, as on 01.04.2016. Abhishek's pull, 34 tables covering load brackets
from 2 kW to 50 kW plus state industrial schedules. [T1 government-compiled]

VINTAGE PROBLEM, HANDLED THE WAY ROUND 1 HANDLED THE MPCE RECONCILIATION.
The Indiastat series is as on 01.04.2016 and our model is FY2025-26. Rather than quote a
ten-year-old rate or silently inflate it, the 2016 cross-section is RE-BASED on a single sourced
current point: BESCOM LT-3 commercial, Karnataka FY2025-26, at Rs8.73/kWh effective.
The re-basing factor is Karnataka-2026 / Karnataka-2016, applied across the cross-section.
What this preserves is the RANKING and the DISPERSION between states, which is what the model
needs; what it assumes is that states have inflated at broadly similar rates. Stated, not hidden.
"""
import pandas as pd, warnings, os, re
warnings.filterwarnings("ignore")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DIR  = os.path.join(_ROOT, "Research Pulls", "India stat", "new")

BRACKETS = {  # file -> (sanctioned kW, units/month)
 "12.doc": (10, 1500), "30.doc": (20, 3000), "31.doc": (30, 4500),
 "32.doc": (40, 6000), "34.doc": (50, 7500), "29.doc": (2, 300), "33.doc": (5, 750),
}
_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cache")

def load_bracket(fn):
    """Licensed source if present, else the cached parse the repository ships. See indiastat.rd."""
    cached = os.path.join(_CACHE, "tariff_" + fn.replace(".", "_") + ".csv")
    src = os.path.join(_DIR, fn)
    if not os.path.exists(src) and os.path.exists(cached):
        d = pd.read_csv(cached)
    else:
        d = pd.read_html(src)[0]
    if list(d.columns[:4]) != ["state","rate_p","duty_p","total_p"]:
        d = d.iloc[2:, [0,2,3,4]].copy()
        d.columns = ["state","rate_p","duty_p","total_p"]
    for c in ("rate_p","duty_p","total_p"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=["total_p"])
    d["state"] = d["state"].astype(str).str.strip()
    return d.reset_index(drop=True)

TABLES = {}
for fn,(kw,units) in BRACKETS.items():
    try: TABLES[(kw,units)] = load_bracket(fn)
    except Exception: pass

# Our store: 4,260 kWh/month at ~15 kW sanctioned -> the 30 kW / 4,500-unit bracket is closest
STORE_KWH, STORE_KW = 4260.0, 15.0
BRACKET = (30, 4500)
T2016 = TABLES[BRACKET]

def _find(df, key):
    m = df[df["state"].str.contains(key, case=False, na=False)]
    return None if m.empty else float(m.iloc[0]["total_p"])/100.0   # paise -> rupees

KA_2016 = _find(T2016, "Karnataka")
BESCOM_2026 = 8.73          # T2 BESCOM LT-3 FY2025-26: Rs8.00 + FAC Rs0.31 + 5% e-tax
REBASE = BESCOM_2026/KA_2016 if KA_2016 else None

def tariff_2026(state):
    v = _find(T2016, state)
    return None if v is None else v*REBASE

FOCUS = ["Karnataka","Delhi","Maharashtra","Tamil Nadu","Telangana","Uttar Pradesh",
         "Bihar","West Bengal","Gujarat","Rajasthan","Kerala","Madhya Pradesh"]

if __name__=="__main__":
    print("="*78); print("LT COMMERCIAL TARIFF BY STATE - Indiastat 2016, re-based to FY2025-26".center(78)); print("="*78)
    print(f"Brackets parsed: {sorted(TABLES.keys())}")
    print(f"Store load {STORE_KWH:,.0f} kWh/month at ~{STORE_KW:.0f} kW -> using the {BRACKET[0]} kW / {BRACKET[1]:,} unit bracket")
    print(f"\nRe-basing anchor:  Karnataka 2016 Rs{KA_2016:.2f}/kWh  ->  BESCOM FY2025-26 Rs{BESCOM_2026:.2f}/kWh")
    print(f"Re-basing factor:  {REBASE:.3f}x over ~10 years  ({REBASE**(1/10)-1:+.1%} CAGR)")
    print(f"\n{'State':<22}{'2016 rate':>11}{'2016 duty':>11}{'2016 total':>12}{'2026 est':>11}")
    print("-"*78)
    for s in FOCUS:
        m = T2016[T2016["state"].str.contains(s, case=False, na=False)]
        if m.empty: print(f"{s:<22}{'not in table':>45}"); continue
        r=m.iloc[0]
        print(f"{s:<22}{r['rate_p']/100:>11.2f}{r['duty_p']/100:>11.2f}{r['total_p']/100:>12.2f}{tariff_2026(s):>11.2f}")
    print("-"*78)
    allv = (T2016["total_p"]/100*REBASE).dropna()
    print(f"All {len(allv)} states/UTs, re-based:  min Rs{allv.min():.2f}   median Rs{allv.median():.2f}   "
          f"max Rs{allv.max():.2f}   CV {allv.std()/allv.mean():.0%}")
    print(f"\n>>> MODEL INPUT. cost_stack.py currently uses Rs{BESCOM_2026:.2f} (Karnataka, our anchor).")
    print(f"    The state median is Rs{allv.median():.2f}. Using Karnataka is CONSERVATIVE by "
          f"{BESCOM_2026/allv.median()-1:+.0%} against the median.")
    print(f"\n>>> DISPERSION TEST, the Round 1 principle: does this variable earn its place?")
    print(f"    Coefficient of variation across states = {allv.std()/allv.mean():.0%}.")
    print(f"    Compare: campus concentration 55%, hostel residents 82%, digital penetration 4%")
    print(f"    (scored and DROPPED in Round 1 for failing this test).")
    cv=allv.std()/allv.mean()
    verdict = "EARNS a place" if cv>0.15 else "does NOT discriminate - report as a single national figure"
    print(f"    Verdict: tariff {verdict}.")
    print(f"\n>>> LIMITATION, stated: the cross-section is 2016 and is re-based on ONE current point.")
    print(f"    It preserves inter-state RANKING and DISPERSION, not absolute 2026 levels per state.")
    print(f"    Upgrade path: each state's SERC tariff order is public. Karnataka is already done.")
