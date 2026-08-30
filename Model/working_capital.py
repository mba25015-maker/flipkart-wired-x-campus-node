"""
D1 item 2.1: THE WORKING-CAPITAL RE-INJECTION, REBUILT.

WHY IT NEEDED REBUILDING. The model carried a Rs96-100 lakh working-capital re-injection as a named
finding of the reactivation slide. The corpus sweep put derived inventory per store at Rs10.9-16.8
lakh (Blinkit) and Rs37.6 lakh (Zepto). An order of magnitude apart. One of the two is wrong.

WHAT THE REBUILD FOUND:
  1. The MAGNITUDE broadly survives. Rebuilt correctly it is ~Rs90 lakh, against the Rs95.7 lakh the
     appendix carries. A 6% restatement, not the order-of-magnitude error the sweep suspected.
     THE SWEEP'S "Rs10.9-17 lakh per store" WAS ITSELF WRONG - see construct (3) below.
  2. The METHOD was wrong twice over: the old construct multiplied COGS/day x NWC days, but the
     disclosed NWC-days figure is already NET and expressed on NOV, so it double-counted the
     netting; and NWC_DAYS = 18 was stale (Eternal, Q1FY27 call 22 Jul 2026: now 14, target 12).
  3. THE REAL FINDING IS THE SIGN. Zepto's audited MCA-filed balance sheet shows 13 days of
     inventory against ~60 days of payables: a NEGATIVE cash conversion cycle. On a negative cycle
     the node is SUPPLIER-FUNDED - standing down pays out float, restarting receives it.
     The re-injection is therefore a CREDIT-TERMS risk, not an inventory-value risk. Different
     sentence on the slide, and a different mitigation.

TIERS: T1 disclosure/analyst | T2 trade press | D derived | A assumed
"""
import campus_model as M, params as P, cost_stack as C, break_mode as B

# ---------------------------------------------------------------------------
# 1. THE DISCLOSED EVIDENCE
# ---------------------------------------------------------------------------
# --- Blinkit inventory per store: UNRESOLVED. DO NOT USE. -------------------
# The corpus digest reports Eternal FY26 inventory two ways in the same passage:
# "2,810,000 thousand" (= Rs281 crore) AND "INR 2,181 crore". Those differ by ~8x and cannot
# both be right. The derived "Rs10.9-17 lakh per store" that the sweep carried is ALSO wrong
# on its own arithmetic: Rs2,181 cr / 1,800-2,000 stores is Rs109-121 LAKH per store, not
# Rs10.9-12.1 lakh. A factor of ten, in the sweep's own working.
# Sanity check: at Rs2,181 cr and DIO 24.79 days, annual COGS is ~Rs32,100 cr, which is the
# right order against Blinkit FY26E NOV of Rs48,812 cr at ~80% 1P. So Rs2,181 cr is the more
# plausible reading - but "more plausible" is not a source.
# STATUS: flagged for direct re-read of the Eternal FY26 balance sheet. NOT used in any figure.
BLINKIT_INVENTORY_FY26_UNRESOLVED = (281e7, 2181e7)   # the two readings in the extraction
BLINKIT_STORES_FY25    = 1301          # T1  disclosed
BLINKIT_STORES_FY26    = (1800, 2000)  # D   store count not disclosed for FY26; range
INV_PER_STORE_RESOLVED = False

# THE POLICY LIVES IN params.py AND NOWHERE ELSE. These were three literals here and a fourth
# (18) as a function default, which is the same duplicate-constant defect that let
# campus_model.NWC_DAYS = 18 survive twelve days past its supersession. audit.py now scans the
# source tree and FAILS if any of these values is redeclared outside params.py.
ETERNAL_NWC_DAYS_NOW    = P.NWC_DAYS          # T1  Eternal Q1FY27 call, 22 Jul 2026
ETERNAL_NWC_DAYS_TARGET = P.NWC_DAYS_TARGET   # T1  same call, steady-state target
ETERNAL_NWC_DAYS_R1     = P.NWC_DAYS_R1       # T1  Jan 2026 call - REJECTED, shown for contrast
ETERNAL_NWC_DAYS_OLD    = ETERNAL_NWC_DAYS_R1 # back-compat alias
NWC_PCT_NOV = {P.NWC_DAYS_TARGET: 0.033, P.NWC_DAYS_R1: 0.050}   # T1  Eternal's own conversion, both points given

ZEPTO_INV_DAYS, ZEPTO_PAY_DAYS = 13.0, 60.0     # T1  EMIS/Zepto: 13 days inventory vs ~60 payables
ZEPTO_CCC = ZEPTO_INV_DAYS - ZEPTO_PAY_DAYS      # -47 days. Supplier-funded, cash-positive cycle.

BLINKIT_DIO_PRE_1P, BLINKIT_DIO_POST_1P = 11.36, 24.79   # T1  days inventory, FY25 -> FY26
NOV_OVER_GOV = 0.791     # T1  Blinkit FY26E NOV/GOV
SHRINKAGE_PCT_NOV = 0.018  # T1  Eternal 22 Jul 2026: "about 1.8% of NOV, largely perishables"

# ---------------------------------------------------------------------------
# 2. THREE CONSTRUCTS FOR THE SAME QUANTITY. Report all three; adopt one.
# ---------------------------------------------------------------------------
DAILY_GOV = B.TERM_OPD * B.CAMPUS_AOV          # 1,400 x current D2-consistent AOV
DAILY_NOV = DAILY_GOV * NOV_OVER_GOV
DAILY_COGS = DAILY_GOV * (1 - M.TAKE_RATE)

def wc_old_construct(days=None):
    days = P.NWC_DAYS_R1 if days is None else days
    """What the model was doing: COGS/day x NWC days. Double-counts the netting."""
    return DAILY_COGS * days

def wc_nwc_on_nov(days=None):
    """Correct use of the disclosed figure: NWC days are NET and expressed on NOV."""
    days = ETERNAL_NWC_DAYS_NOW if days is None else days
    return DAILY_NOV * days

def wc_store_held():
    """UNAVAILABLE. The per-store inventory benchmark cannot be computed until the Eternal FY26
    balance-sheet inventory line is re-read directly. Returns the two candidate readings scaled,
    for information only - neither is adopted."""
    blinkit_store_gov_day = 1490 * 694.0        # T1  OPD x gross AOV, FY26
    scale = DAILY_GOV / blinkit_store_gov_day
    return tuple(v/BLINKIT_STORES_FY26[0]*scale for v in BLINKIT_INVENTORY_FY26_UNRESOLVED)

WC_OLD      = wc_old_construct(ETERNAL_NWC_DAYS_OLD)
WC_NWC_NOV  = wc_nwc_on_nov(ETERNAL_NWC_DAYS_NOW)          # <- ADOPTED
WC_ADOPTED  = WC_NWC_NOV
WC_TARGET   = wc_nwc_on_nov(ETERNAL_NWC_DAYS_TARGET)       # at Eternal's 12-day steady state
WC_CAND_LO, WC_CAND_HI = wc_store_held()                   # information only, NOT adopted

# ---------------------------------------------------------------------------
# 3. THE SIGN. This is the finding.
# ---------------------------------------------------------------------------
# A node's working capital = store inventory - supplier payables against it.
# On Zepto's disclosed cycle (13 days inventory, 60 days payables) the node is NET CASH POSITIVE:
# suppliers fund the stock and leave float over. Two states at reactivation:
#
#   STATE A - CREDIT INTACT. Suppliers resume normal terms on restart. Rebuilding the store's
#             stock is funded by payables. Reactivation working capital ~= 0, and may be a
#             cash INFLOW as the float rebuilds. Standing down is what costs cash, because you
#             settle payables while inventory runs to zero.
#   STATE B - CREDIT RESET. A supplier who has not shipped to this node for 3.5 months puts it
#             back on cash-on-delivery until the relationship re-establishes. The store's stock
#             must then be self-funded at restart.
#
# THE RISK IS A CREDIT-TERMS RISK, NOT AN INVENTORY-VALUE RISK. That is a different sentence
# from the one on the current slide, and it is a different mitigation: negotiate dormancy
# clauses into supplier terms at the same time as the campus licence, before the first break.
def reactivation_wc(state="B", days_credit=None):
    """State A: suppliers resume terms -> the rebuild is payables-funded, reactivation WC ~ 0.
       State B: credit resets -> the node self-funds its working capital for `days_credit` of the
       normal 60-day payable cycle before terms re-establish. Default: the full cycle."""
    if state == "A":
        return 0.0
    frac = 1.0 if days_credit is None else min(1.0, days_credit/ZEPTO_PAY_DAYS)
    return WC_ADOPTED * frac

WC_STATE_A = reactivation_wc("A")
WC_STATE_B = reactivation_wc("B")
WC_STATE_B_30D = reactivation_wc("B", days_credit=30)

# The old figure, restated on the same basis, for the delta
OLD_SLIDE_FIGURE = 95.7e5    # the Round-1/S7 figure the appendix carries

def report():
    print("="*84); print("WORKING CAPITAL RE-INJECTION, REBUILT".center(84)); print("="*84)
    print(f"  Daily GOV Rs{DAILY_GOV:,.0f}   daily NOV Rs{DAILY_NOV:,.0f}   daily COGS Rs{DAILY_COGS:,.0f}")
    print()
    print("  CONSTRUCTS")
    print(f"    (1) old method: COGS/day x 18 days      Rs{WC_OLD/1e5:>7.1f} lakh   REJECTED")
    print(f"        wrong twice: NWC days are already NET and stated on NOV (double-counts the")
    print(f"        netting), and 18 days is stale -- Eternal Q1FY27 says 14, target 12.")
    print(f"    (2) NWC days x daily NOV @ 14 days      Rs{WC_ADOPTED/1e5:>7.1f} lakh   ADOPTED")
    print(f"        @ Eternal's 12-day steady state     Rs{WC_TARGET/1e5:>7.1f} lakh")
    print(f"    (3) per-store inventory benchmark            UNRESOLVED -- NOT USED")
    print(f"        the corpus extraction gives Eternal FY26 inventory as BOTH Rs281 cr and")
    print(f"        Rs2,181 cr in the same passage. And the sweep's derived 'Rs10.9-17 lakh per")
    print(f"        store' is wrong on its own arithmetic by a factor of ten (Rs2,181 cr over")
    print(f"        1,800-2,000 stores is Rs109-121 LAKH). Flagged for direct re-read.")
    print()
    print(f"  MAGNITUDE VERDICT  Rs{WC_ADOPTED/1e5:.1f} lakh vs the Rs{OLD_SLIDE_FIGURE/1e5:.1f} lakh the appendix carries")
    print(f"                     = {(WC_ADOPTED/OLD_SLIDE_FIGURE-1)*100:+.1f}%. A restatement, NOT an order-of-magnitude")
    print(f"                     error. The sweep's suspicion was itself the arithmetic error.")
    print()
    print("  THE SIGN -- this is the actual finding")
    print(f"    Zepto, audited MCA-filed consolidated balance sheet:")
    print(f"      {ZEPTO_INV_DAYS:.0f} days inventory vs {ZEPTO_PAY_DAYS:.0f} days payables -> cash conversion cycle {ZEPTO_CCC:+.0f} days.")
    print(f"      The node is SUPPLIER-FUNDED. Standing down PAYS OUT float; restarting RECEIVES it.")
    print()
    print(f"    STATE A  supplier credit intact at restart")
    print(f"             reactivation working capital     Rs{WC_STATE_A/1e5:>7.1f} lakh")
    print(f"             stock rebuilds on payables. The cash cost sits at WIND-DOWN, not restart.")
    print(f"    STATE B  credit resets after 3.5 months dormant")
    print(f"             full {ZEPTO_PAY_DAYS:.0f}-day cycle self-funded     Rs{WC_STATE_B/1e5:>7.1f} lakh")
    print(f"             30 days to re-establish terms   Rs{WC_STATE_B_30D/1e5:>7.1f} lakh")
    print()
    print(f"  VERDICT  The number barely moves. THE SENTENCE CHANGES COMPLETELY.")
    print(f"           It is a CREDIT-TERMS risk, not an inventory-value risk -- and the mitigation")
    print(f"           is contractual, not financial: negotiate dormancy clauses into supplier terms")
    print(f"           at the same time as the campus licence, BEFORE the first break. State A is")
    print(f"           reachable by negotiation. That is a mechanism an ops manager can own.")
    print(f"           Also unpriced anywhere and worth a line: shrinkage runs {SHRINKAGE_PCT_NOV:.1%} of NOV,")
    print(f"           'largely perishables' (Eternal, 22 Jul 2026) = Rs{DAILY_NOV*SHRINKAGE_PCT_NOV*30/1e5:.2f} lakh/month here.")

if __name__ == "__main__":
    report()
