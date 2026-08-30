"""
D1 #4: CAN THE CAMPUS BASKET REACH THE BREAKEVEN AOV?

THE PROBLEM, STATED HONESTLY. S19/S20 put the D2-consistent minimum viable campus AOV at Rs580.
Round 1 already conceded that Rs528 sat "above every student-basket estimate". Rs580 sits further
above it. A well-audited impossibility is still an impossibility, so the deck has to show the path
or drop the standalone-viability claim.

THE METHOD. We do not assume a basket-lifting rate. We take the ONE disclosed, dated, quarterly
series in which an Indian q-commerce operator actually lifted its AOV, measure the relationship,
and ask what it implies for a campus node. Swiggy Instamart moved non-grocery from ~7% to 26.2% of
GOV across five quarters and its AOV moved Rs487 -> Rs697 over the same window. That is the only
observed AOV-lifting mechanism in the corpus with both variables disclosed by the same operator on
the same axis.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import numpy as np
import campus_model as M, cost_stack as C

# ---------------------------------------------------------------------------
# 1. THE OBSERVED LEVER  -- Instamart non-grocery share of GOV vs AOV  [T1]
#    Sources: JM Financial Exhibit 24 (category mix by value, company-sourced);
#    Nirmal Bang Q1FY26 result update, 1 Aug 2025 (AOV and mix in one exhibit);
#    JM/Elara quarterly result notes for the AOV series.
# ---------------------------------------------------------------------------
INSTAMART = [           # (quarter, non-grocery % of GOV, AOV Rs)
    ("Q1FY25",  7.0, 487.0),
    ("Q4FY25", 15.6, 527.0),
    ("Q1FY26", 18.5, 612.0),
    ("Q2FY26", 26.2, 697.0),
]
_x = np.array([r[1] for r in INSTAMART])
_y = np.array([r[2] for r in INSTAMART])
SLOPE, INTERCEPT = np.polyfit(_x, _y, 1)          # Rs of AOV per point of non-grocery share
R2 = 1 - ((_y - (SLOPE*_x + INTERCEPT))**2).sum() / ((_y - _y.mean())**2).sum()

# ---------------------------------------------------------------------------
# 2. WHERE FLIPKART MINUTES STARTS  [T2/T1]
# ---------------------------------------------------------------------------
MINUTES_NONGROCERY = 20.0     # T2  Netscribes, from Flipkart disclosure: mobiles/electronics
                              #     ~20% of Minutes sales. Third-party estimate, stated as such.
MINUTES_AOV_NOW    = M.MINUTES_AOV            # Rs450, T1, journalist-confirmed
# TARGET_AOV IS NOT A LITERAL. It was 580.0 typed here, a third copy of the D2-consistent
# breakeven that also lived in break_mode._D2_LM's downstream and in the audit literals. When
# the last-mile basis moved from marginal to roster pricing, the deck's text updated and this
# chart annotation did not - it kept drawing "breakeven Rs580" under a slide that said Rs573.
# Sourced from the model, and audit.recon() now asserts the tie.
import cost_stack as _CS, sla as _SL
TARGET_AOV         = _CS.breakeven_d2_consistent(_CS.CAMPUS_FIXED, _SL.volume_weighted()[1])

# Management's own ceiling, and it is a real constraint, not a modelling choice:
NONGROCERY_CEILING = 40.0     # T1  Swiggy management: non-grocery capped at 30-40% of GOV
                              #     "to retain the benefits of being on a high frequency platform"
NONGROCERY_CEILING_LO = 30.0

def aov_at_share(share):
    """Instamart-observed relationship, applied to a campus node."""
    return SLOPE*share + INTERCEPT

def share_needed(target_aov, base_aov=None, base_share=None):
    """Non-grocery share of GOV required to lift the basket to target, anchored on Minutes'
    CURRENT position rather than on Instamart's intercept -- Minutes is a different network."""
    base_aov   = MINUTES_AOV_NOW    if base_aov   is None else base_aov
    base_share = MINUTES_NONGROCERY if base_share is None else base_share
    return base_share + (target_aov - base_aov)/SLOPE

SHARE_NEEDED = share_needed(TARGET_AOV)
HEADROOM_TO_CEILING = NONGROCERY_CEILING - SHARE_NEEDED
FITS_UNDER_CEILING  = SHARE_NEEDED <= NONGROCERY_CEILING

# ---------------------------------------------------------------------------
# 3. WHAT THE NON-GROCERY IS, ON A CAMPUS  -- AOV by category  [T1, Swiggy DRHP 2023]
# ---------------------------------------------------------------------------
CATEGORY_AOV = {          # Rs per order
    "Electronics":        (4000, 5000),
    "Medicines":          ( 900, 1000),
    "Fashion":            ( 600,  700),
    "Beauty & personal care": (550, 600),
    "Grocery":            ( 400,  500),
}
# The campus-native non-grocery lines, and why each is defensible on this cohort:
CAMPUS_NONGROCERY = [
 ("Term-start durables", "coolers, blankets, buckets, mosquito nets, storage",
  "Rs1,000+ baskets concentrated in a 2-3 week window at each term start [Round 1 corpus, T2]"),
 ("Electronics accessories", "chargers, cables, earphones, power banks, mice",
  "Minutes' existing strength: mobiles/electronics already ~20% of its sales [T2]"),
 ("Stationery and print", "notebooks, pens, printouts",
  "Zepto shipped Express Prints Rs2/page at ~285 stores, 18 Apr 2026 -- a student SKU in market [T1]"),
 ("Beauty & personal care", "BPC at Rs550-600 AOV vs grocery Rs400-500",
  "highest-AOV category that is genuinely high-frequency for this cohort [T1, Swiggy DRHP]"),
 ("Medicines / OTC", "analgesics, antipyretics, first aid",
  "Rs900-1,000 AOV; hostel population, no on-site pharmacy at most campuses [T1]"),
]

# ---------------------------------------------------------------------------
# 4. THE SECOND LEVER: THRESHOLD ENGINEERING  [T1]
#    Minutes currently runs the LOWEST free-delivery threshold in the market. That is
#    optimised for small-basket acquisition and works AGAINST basket lifting.
# ---------------------------------------------------------------------------
FREE_DELIVERY_THRESHOLD = {      # Rs
    "Flipkart Minutes": 149.0,   # T1  free above Rs149; Rs30 delivery below Rs99; no handling fee
    "Blinkit":          499.0,   # T1  raised to Rs499 BY LOCATION AND DEMAND, plus Rs30 surcharge
    "Instamart":        199.0,   # T1  with a Rs74 deferred coupon used to lift a Rs125 cart to Rs199
}
THRESHOLD_GAP = FREE_DELIVERY_THRESHOLD["Blinkit"] - FREE_DELIVERY_THRESHOLD["Flipkart Minutes"]
# Blinkit already varies this BY LOCATION. A campus-specific threshold is therefore not a novel
# ask of the platform - it is an existing lever, set to its most permissive value on this network.

# ---------------------------------------------------------------------------
# 5. THE THIRD LEVER: OCCASION CONCENTRATION
#    Not every order has to reach Rs580. The ANNUAL AVERAGE has to.
# ---------------------------------------------------------------------------
def blended_aov(base_aov, occasion_aov, occasion_share):
    return base_aov*(1-occasion_share) + occasion_aov*occasion_share

TERM_START_AOV   = 1000.0   # T2  Round 1 corpus: term-start durables, Rs1,000+ baskets
TERM_START_WEEKS = 5.0      # D   2-3 weeks x 2 term starts per academic year
TERM_WEEKS       = M.ACTIVE_MONTHS*52/12          # 36.8 active weeks
TERM_START_SHARE = TERM_START_WEEKS/TERM_WEEKS    # ~13.6% of active weeks

def occasion_only_aov(base_aov=None):
    base_aov = MINUTES_AOV_NOW if base_aov is None else base_aov
    return blended_aov(base_aov, TERM_START_AOV, TERM_START_SHARE)

OCCASION_AOV = occasion_only_aov()
OCCASION_ALONE_CLOSES = OCCASION_AOV >= TARGET_AOV

# ---------------------------------------------------------------------------
# 6. THE LADDER  -- what each lever contributes, cumulatively
# ---------------------------------------------------------------------------
def ladder():
    rows = []
    aov = MINUTES_AOV_NOW
    rows.append(("Minutes network basket today", aov, "T1 TechCrunch, journalist-confirmed"))
    aov2 = occasion_only_aov(aov)
    rows.append(("+ term-start durable occasions", aov2,
                 f"Rs1,000 baskets over {TERM_START_SHARE:.0%} of active weeks"))
    # remaining gap closed by category mix
    need = share_needed(TARGET_AOV, aov2, MINUTES_NONGROCERY)
    rows.append((f"+ non-grocery mix to {need:.0f}% of GOV", TARGET_AOV,
                 f"vs {MINUTES_NONGROCERY:.0f}% today; disclosed range {NONGROCERY_CEILING_LO:.0f}-{NONGROCERY_CEILING:.0f}%"))
    return rows, need

LADDER_ROWS, SHARE_NEEDED_AFTER_OCCASION = ladder()
FITS_AFTER_OCCASION = SHARE_NEEDED_AFTER_OCCASION <= NONGROCERY_CEILING

def report():
    print("="*84)
    print("BASKET LADDER: CAN A CAMPUS BASKET REACH THE BREAKEVEN AOV?".center(84))
    print("="*84)
    print(f"  Target (D2-consistent minimum viable campus AOV)   Rs{TARGET_AOV:.0f}")
    print(f"  Starting point (Minutes network AOV, T1)           Rs{MINUTES_AOV_NOW:.0f}")
    print(f"  Gap to close                                       Rs{TARGET_AOV-MINUTES_AOV_NOW:.0f}")
    print()
    print("  THE OBSERVED LEVER -- Instamart, non-grocery share of GOV vs AOV")
    print(f"  {'quarter':<10}{'non-grocery % GOV':>20}{'AOV Rs':>10}")
    for q,s,a in INSTAMART: print(f"  {q:<10}{s:>20.1f}{a:>10.0f}")
    print(f"  fit: AOV = {SLOPE:.2f} x (non-grocery %) + {INTERCEPT:.0f}      R2 = {R2:.3f}")
    print(f"  >>> every point of non-grocery share is worth Rs{SLOPE:.2f} of AOV [T1-derived]")
    print()
    print("  THE LADDER")
    for name, aov, note in LADDER_ROWS:
        print(f"    {name:<40} Rs{aov:>6.0f}   {note}")
    print()
    print(f"  Non-grocery share required, mix lever alone      {SHARE_NEEDED:.1f}% of GOV")
    print(f"  Non-grocery share required, after occasions      {SHARE_NEEDED_AFTER_OCCASION:.1f}% of GOV")
    print(f"  Minutes today                                    {MINUTES_NONGROCERY:.1f}% of GOV")
    print(f"  Management ceiling (Swiggy, stated)              {NONGROCERY_CEILING_LO:.0f}-{NONGROCERY_CEILING:.0f}% of GOV")
    print(f"  VERDICT  {'REACHABLE inside the range Swiggy discloses' if FITS_AFTER_OCCASION else 'NOT reachable inside the ceiling'}"
          f"  (headroom {NONGROCERY_CEILING-SHARE_NEEDED_AFTER_OCCASION:+.1f} pts)")
    print()
    print("  SECOND LEVER -- free-delivery threshold, and Minutes is the market outlier")
    for k,v in FREE_DELIVERY_THRESHOLD.items(): print(f"    {k:<20} Rs{v:.0f}")
    print(f"    Blinkit already varies this BY LOCATION AND DEMAND. A campus-specific threshold")
    print(f"    is an existing platform lever, not a novel ask. Gap to Blinkit: Rs{THRESHOLD_GAP:.0f}.")
    print()
    print("  WHAT THE NON-GROCERY IS, ON A CAMPUS")
    for name, what, why in CAMPUS_NONGROCERY:
        print(f"    {name:<26} {what}")
        print(f"    {'':<26} {why}")

if __name__ == "__main__":
    report()
