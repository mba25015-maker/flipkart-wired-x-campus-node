"""
JM Financial Exhibit 2 [T1]: field survey of 35 dark stores across 20 Indian cities, Apr-Jun 2025.
"Summarised feedback from dark stores that we visited across 20 cities during Apr-Jun'25"
Source: JM Financial Institutional Securities, "Deep Dive: Quick Commerce", 27 Aug 2025, page 4.

Found by full-text grep of the Bloomberg corpus while trying to close an ASSUMED parameter.
It closes three at once and validates two others. Columns: city tier, store sqft, SKU count,
delivery radius km, net AOV, orders per day, observed delivery minutes, operating hours.
"""
import numpy as np

# tier, sqft, skus, radius_km, naov_lo, naov_hi, opd_lo, opd_hi, mins_lo, mins_hi, hrs24
S = [
 ("metro",3000,20000,4,   None,None, 2500,3000, 15,15, True),
 ("metro",4500,11000,3,   300,400,   2400,2400, 10,10, True),
 ("metro",2400,20000,5,   700,700,   1500,2000, 21,21, None),
 ("metro",3000,30000,5,   None,None, 2000,2000, 15,15, True),
 ("metro",2500,35000,4,   None,None, 2000,2000, 15,15, True),
 ("metro",11000,114000,10,None,None, 4000,4000, None,None, True),
 ("metro",2800,30000,4.5, 400,500,   1200,1300, 15,15, True),
 ("metro",7000,100000,4,  700,700,   2500,2500, 15,15, False),
 ("metro",2500,25000,3.5, None,None, 2000,2000, 10,10, False),
 ("metro",3500,12000,3,   400,500,   1700,1700, 15,15, True),
 ("metro",2500,11000,6,   500,500,   2200,2300, 20,20, True),
 ("metro",3000,12000,4,   500,500,   2000,2000, 15,15, True),
 ("metro",2500,10000,6,   500,600,   1500,1500, 20,20, True),
 ("metro",3000,8000,4,    400,400,   800,1000,  11,12, False),
 ("metro",3500,17000,4,   400,500,   2500,2500, 10,10, False),
 ("metro",2000,7000,4,    350,400,   600,800,   20,20, True),
 ("t12",4000,10000,3,     None,None, 1200,1200, 15,15, True),
 ("t12",3000,12000,4,     300,300,   700,700,   10,15, False),
 ("t12",3500,15000,5,     300,400,   1500,1500, 12,12, True),
 ("t12",3500,12000,3,     200,300,   2000,2000, 10,13, True),
 ("t12",3000,8000,4,      None,None, 1500,1500, 15,20, True),
 ("t12",3500,15000,7,     400,500,   1000,1000, 19,19, False),
 ("t12",3000,30000,10,    600,600,   400,500,   30,30, False),
 ("t12",2500,7500,5,      400,400,   400,400,   15,15, False),
 ("t12",2000,10000,5,     300,400,   800,800,   15,15, False),
 ("t12",2400,6000,4,      500,500,   1000,1000, 12,13, False),
 ("t3",5500,12000,4,      300,300,   1500,1500, 12,12, False),
 ("t3",3000,20000,5,      None,None, 1000,1000, 15,15, False),
 ("t12",3500,20000,10,    500,500,   3000,3000, 20,20, True),
 ("t12",2500,12000,4,     300,400,   1000,1000, 15,15, False),
 ("t3",3000,11000,4,      400,500,   2000,2000, 15,15, True),
 ("t3",4800,10000,3,      200,300,   800,900,   10,15, False),
 ("t3",1600,10000,None,   None,None, 700,800,   15,15, False),
 ("t3",4000,15000,None,   None,None, 900,900,   12,12, False),
 ("t3",5000,8000,None,    None,None, 1300,1300, 15,15, False),
]
def mid(a,b): return None if a is None else (a+b)/2.0

SQFT = np.array([r[1] for r in S], float)
SKUS = np.array([r[2] for r in S], float)

# ---- FIXED-CORE SHARE, DERIVED (was assumed at a 30-60% range) ----
# Regress store area on SKU count. The INTERCEPT is the area that does not scale with assortment:
# dispatch, staging, cold zone, aisles, packing bench. That intercept IS the fixed core.
b, a = np.polyfit(SKUS, SQFT, 1)            # sqft = a + b*skus
resid = SQFT - (a + b*SKUS)
r2 = 1 - (resid**2).sum()/((SQFT-SQFT.mean())**2).sum()
FIXED_CORE_SQFT   = a
FIXED_CORE_SHARE  = a/3100.0                 # against JM's own 3,100 sqft model store
SQFT_PER_SKU      = b

# Excluding the two outsized stores (11,000 sqft/114k SKUs and 7,000/100k) which are a different
# format - JM's own transcript calls these "large size dark stores of almost 10,000 square feet".
m = SKUS < 60000
b2, a2 = np.polyfit(SKUS[m], SQFT[m], 1)
r2_2 = 1 - ((SQFT[m]-(a2+b2*SKUS[m]))**2).sum()/((SQFT[m]-SQFT[m].mean())**2).sum()

# ---- OBSERVED NAOV, ORDERS/DAY, DELIVERY MINUTES ----
NAOV = np.array([v for v in (mid(r[4],r[5]) for r in S) if v is not None])
OPD  = np.array([mid(r[6],r[7]) for r in S], float)
MINS = np.array([v for v in (mid(r[8],r[9]) for r in S) if v is not None])
NAOV_M = np.array([mid(r[4],r[5]) for r in S if r[0]=="metro" and r[4] is not None])
NAOV_T = np.array([mid(r[4],r[5]) for r in S if r[0]!="metro" and r[4] is not None])

if __name__=="__main__":
    print("="*80); print(f"JM FINANCIAL EXHIBIT 2 - {len(S)} dark stores, 20 cities, Apr-Jun 2025 [T1]".center(80)); print("="*80)

    print("\n--- FIXED-CORE SHARE: THE REGRESSION FALSIFIES OUR OWN LEVER ------------------")
    print(f"  All {len(S)} stores      sqft = {a:,.0f} + {b:.4f} x SKUs      R2 = {r2:.2f}")
    print(f"  Excl. 2 outsized   sqft = {a2:,.0f} + {b2:.4f} x SKUs      R2 = {r2_2:.2f}   (n={m.sum()})")
    print(f"\n  >>> READ THIS HONESTLY. Within the standard dark-store format the slope is")
    print(f"      NEGATIVE and R2 is {r2_2:.2f}. Store area and SKU count are UNCORRELATED across")
    print(f"      33 observed stores of 1,600-5,500 sqft. The full-sample R2 of {r2:.2f} is carried")
    print(f"      entirely by two outsized stores (11,000 sqft/114k SKUs and 7,000/100k), which")
    print(f"      JM's own transcript describes as a different format.")
    print(f"\n  CONSEQUENCE: the S11 footprint-discipline lever, as specified, DOES NOT HOLD.")
    print(f"      Cutting the local range from 16,500 to 8,000 SKUs would not reliably reduce")
    print(f"      floor area, because that elasticity does not exist inside the format. Assortment")
    print(f"      drives area only when you CHANGE format, not when you trim SKUs within one.")
    print(f"\n  WHAT SURVIVES, and it is a format choice rather than an elasticity claim:")
    small = [r for r in S if r[1] <= 2500]
    print(f"      {len(small)} of {len(S)} observed stores run at 2,500 sqft or less, carrying")
    print(f"      {min(r[2] for r in small):,}-{max(r[2] for r in small):,} SKUs. The small format EXISTS in the field.")
    print(f"      Specifying a campus node at 2,000 sqft is choosing a format the survey shows")
    print(f"      is viable, not asserting an area-per-SKU relationship the survey refutes.")
    print(f"      Rent at 2,000 sqft x Rs70 = Rs{2000*70:,.0f} vs Rs{3100*70:,.0f} baseline "
          f"(-{1-2000/3100:.0%}).")

    print("\n--- OBSERVED NET AOV: the field data behind the AOV argument --------------------")
    print(f"  n={len(NAOV)} stores reporting NAOV      range Rs{NAOV.min():.0f}-{NAOV.max():.0f}   "
          f"median Rs{np.median(NAOV):.0f}   mean Rs{NAOV.mean():.0f}")
    print(f"  Metro    n={len(NAOV_M)}  median Rs{np.median(NAOV_M):.0f}")
    print(f"  Tier 1/2/3 n={len(NAOV_T)}  median Rs{np.median(NAOV_T):.0f}")
    print(f"  >>> Observed store-level NAOV brackets BOTH disputed figures. Rs400-500 (TechCrunch)")
    print(f"      and Rs700 (Datum) are both inside the observed field range, which supports the")
    print(f"      reading that they measure different things rather than one being wrong.")

    print("\n--- OBSERVED ORDERS PER DAY ---------------------------------------------------")
    print(f"  range {OPD.min():,.0f}-{OPD.max():,.0f}   median {np.median(OPD):,.0f}   mean {OPD.mean():,.0f}")
    print(f"  >>> Our 1,400/day working ceiling sits at the {(OPD<1400).mean():.0%}th percentile of")
    print(f"      observed stores. Defensible, and mid-range rather than aggressive.")

    print("\n--- OBSERVED DELIVERY MINUTES: the SLA argument, validated ----------------------")
    print(f"  n={len(MINS)}   range {MINS.min():.0f}-{MINS.max():.0f} min   median {np.median(MINS):.0f}   mean {MINS.mean():.1f}")
    print(f"  Stores delivering in 10 min or less: {(MINS<=10).mean():.0%}")
    print(f"  Stores taking 15 min or more:        {(MINS>=15).mean():.0%}")
    print(f"  >>> THE '10-MINUTE' PROMISE IS ALREADY NOT THE OPERATING REALITY. Observed median")
    print(f"      is {np.median(MINS):.0f} minutes across 33 stores in 20 cities, with a long tail to 30.")
    print(f"      Our 20-30 minute campus SLA is a modest extension of what the network already")
    print(f"      does, not a departure from it. This substantially de-risks the SLA argument.")
