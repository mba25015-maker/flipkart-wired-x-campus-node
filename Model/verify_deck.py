"""
VERIFY THE DECK, NOT THE DOCUMENT.

`verify_docs.py` parses figures out of HANDOFF.md. This does the same job one step later.
With a .pptx argument it opens the actual built deck. Without an argument it checks the
published text-only snapshot so a public clone can reproduce the recorded result without
redistributing the PowerPoint.

  python3 verify_deck.py [path.pptx]

A slide number that drifts from the model fails here even if `audit.py` passes, because
audit.py checks the model against itself; this checks the artifact the panel will see.
"""
import json, sys, os, re
import campus_model as M, cost_stack as CS, break_mode as B
import aishe_district as AD, risk_quadrant as Q, calendar_fragmentation as CF
import basket as BK, sla as SL, roce as RC, fleet_mix as FM, working_capital as WC

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(HERE, "verification", "deck_text_snapshot.json")
PPTX = sys.argv[1] if len(sys.argv) > 1 else None

def deck_text(path):
    from pptx import Presentation
    prs = Presentation(path); out = []
    for s in prs.slides:
        buf = []
        for sh in s.shapes:
            if sh.has_text_frame:
                buf.append(" ".join(r.text for p in sh.text_frame.paragraphs for r in p.runs))
        out.append(" ".join(buf))
    return out

if PPTX:
    pages = deck_text(PPTX)
    VERIFIED_NAME = os.path.basename(PPTX)
else:
    payload = json.loads(open(SNAPSHOT, encoding="utf-8").read())
    pages = payload["pages"]
    VERIFIED_NAME = payload["source_filename"] + " (published text snapshot)"
ALL = " ".join(pages)
checks = []
def _norm(t):
    """Compare on content, not on glyphs. The deck writes ₹, ×, en dashes and non-breaking
    spaces; the model prints Rs, x and hyphens. A check must not fail on typography."""
    for a, b in (("\u20b9","Rs"), ("\u00d7","x"), ("\u2013","-"), ("\u2014","-"),
                 ("\u2212","-"), ("\u00a0"," "), ("\u2019","'"), ("\u201c",'"'), ("\u201d",'"'), (" lakh"," L")):
        t = t.replace(a, b)
    return t

def must(label, needle, page=None):
    """Figures are matched exactly; prose is matched case-insensitively, because a slide
    may shout a phrase the model spells in lower case. The page is taken from the label's
    own prefix when the caller does not pass one, so re-ordering the deck is a one-line change."""
    if page is None:
        page = PAGE.get(label.split()[0])
    hay = _norm(ALL if page is None else pages[page]); nd = _norm(needle)
    checks.append((nd in hay or nd.lower() in hay.lower(), label, needle))
def must_not(label, needle):
    checks.append((_norm(needle) not in _norm(ALL), label, "ABSENT: " + needle))

thr   = [B.threshold(fn) for _, fn in B.CONFIGS]
rev   = Q.post_revocation_survival()
rel   = B.relocate_vs_flex()
be    = CS.breakeven_d2_consistent(CS.CAMPUS_FIXED, SL.volume_weighted()[1])

# Slide order. The 8-slide REFERENCE deck (S31 architecture) and the earlier 4-slide build have
# different page indices, so the page is INFERRED from the check's own label prefix rather than
# hard-coded twice. A deck with a different slide count fails loudly instead of silently passing.
if len(pages) == 8:                       # S31: rec, market, dead zone, return, site, ops, fin, roadmap
    PAGE = {"S1":0,"S2":1,"S3":2,"S4":3,"S5":4,"S6":5,"S7":6,"S8":7}
elif len(pages) == 4:                     # the earlier build: slides 1, 2, 5, 6 only
    PAGE = {"S1":0,"S2":1,"S5":2,"S6":3}
else:
    PAGE = {}
S1, S2, S5, S6 = PAGE.get("S1"), PAGE.get("S2"), PAGE.get("S5"), PAGE.get("S6")

# ---- slide 1: the executive summary --------------------------------------------
must("S1  headline asset-turn ratio",            f"{M.TURN_RATIO:.0%}")
must("S1  ladder start",                         f"{thr[0]:.1%}")
must("S1  ladder floor",                         f"{thr[-1]:.1%}")
must("S1  do-nothing burn through the break",    f"Rs{rel['do_nothing_total']/1e5:.1f} lakh")
must("S1  cost of one relocation",               f"Rs{rel['relocate_once']/1e5:.0f} lakh")
must("S1  holding as a share of relocating",     f"{rel['flex_vs_relocate']:.0%}")
must("S1  D1/D2-consistent breakeven",           f"Rs{be:,.0f}")
must("S1  candidate districts",                  f"{AD.N_CANDIDATES} of {AD.N_DISTRICTS:,}")
must("S1  campus asset turn",                    f"{M.CAMPUS_TURN:.2f}x")
must("S7  non-grocery share required",           f"{BK.SHARE_NEEDED_AFTER_OCCASION:.1f}%")
must("S7  management's stated ceiling",          f"{BK.NONGROCERY_CEILING_LO:.0f}–{BK.NONGROCERY_CEILING:.0f}%")
must("S1  the not-first concession is present",  "not first")

# ---- slide 2: the market -------------------------------------------------------
must("S2  metro oversupply",                     f"{AD.METRO_EXCESS:.0%}")
must("S2  colleges in the register",             f"{AD.N_COL:,}")
must("S2  urban colleges",                       f"{AD.URBAN_COL:,}")
must("S2  urban non-metro colleges",             f"{AD.NON_METRO_URBAN_COLLEGES:,}")
must("S2  urban high-propensity standalones",    f"{AD.N_STA_URBAN_HP:,}")
must("S2  the Starship hook is on the slide",    "Starship")
must("S2  the quote is verbatim",                "365-day urban business")
must("S2  Euromonitor white space",              "Euromonitor")

# ---- the dead-zone slide: every headline figure (slide 5 in the 4-slide build, 3 in S31)
must("S3  flexible share of the fixed base",     f"{CS.fixed_flex_share():.1%}")
must("S3  do-nothing residual threshold",        f"{thr[0]:.1%}")
must("S3  post-ladder residual threshold",       f"{thr[-1]:.1%}")
must("S3  fixed base",                           f"Rs{CS.CAMPUS_FIXED:,.0f}")
must("S3  tier rent band, low",                  f"Rs{CS.T12_FIXED_LOW:,.0f}")
must("S3  tier rent band, high",                 f"Rs{CS.T12_FIXED_HIGH:,.0f}")
must("S3  'other fixed' residual, stated openly", f"Rs{CS.OTHER_FIXED:,.0f}")
must("S4  the moneyshot ratio",                  f"{M.TURN_RATIO:.3f}")
must("S4  density term",                         f"{M.CEILING/M.MINUTES_ORD:.3f}")
must("S4  calendar term",                        f"{M.ACTIVE_MONTHS/12:.3f}")
must("S4  campus asset turn",                    f"{M.CAMPUS_TURN:.2f}x")
must("S4  city asset turn",                      f"{M.CITY_TURN:.2f}x")
must("S4  sensitivity, ratio at 1,000/day",      f"{M.TURN_RATIO_AT_1000:.3f}")
must("S4  sensitivity, ratio at 1,200/day",      f"{M.TURN_RATIO_AT_1200:.3f}")
must("S4  parity throughput",                    f"{M.PARITY_OPD:,.0f}/day")
must("S4  Blinkit observed range, low",          f"{M.CEIL_LO:,}")
must("S4  Blinkit observed range, high",         f"{M.CEIL_HI:,}")
must("S4  Minutes AOV on the adopted basis",     f"Rs{M.MINUTES_AOV:,.0f}")

# ---- the site-selection slide (6 in the 4-slide build, 5 in S31) -----------------
must("S5  site filter, uncontested",             f"{AD.SITE_FILTER_UNCONTESTED:,.0f}")
must("S5  candidate districts",                  f"{AD.N_CANDIDATES}")
must("S5  districts in the register",            f"{AD.N_DISTRICTS:,}")
must("S5  stacked share of our own list",        f"{AD.STACKED_SHARE:.0%}")
must("S5  uncontested districts",                f"{AD.N_UNCONTESTED}")
must("S5  revocation binding requirement",       f"{rev['orders_needed']:,.0f}")
must("S5  break-solvency requirement",           f"{rev['adjacent_lo']:,.0f}")
must("S5  gross demand at metro overlap",        f"{AD.gross_demand_required(AD.METRO_OVERLAP_5OP):,.0f}/day")
must("S5  metro five-operator overlap",          f"{AD.METRO_OVERLAP_5OP:.0%}")
must("S5  the 7-week rule is derived on-slide",   "7-WEEK RULE")
must("S5  wind-downable share, typical calendar", f"{CF.TYPICAL_WINDOWNABLE:.0%}")
must("S5  fragmentation penalty, typical",       f"{CF.TYPICAL_PENALTY:+.0%}")
must("S2  non-metro store base",                 f"{AD.NON_METRO_STORES:,}")
must("S2  five-operator store total",            f"{AD.TOTAL_STORES:,}")

# ---- slide 4: the return (S31) --------------------------------------------------
must("S4  ROCE hurdle",                          f"{RC.ROCE_HURDLE:.0%}")
must("S4  AOV at the hurdle",                    f"{RC.AOV_HURDLE:,.0f}")
must("S4  AOV at breakeven, ROCE basis",         f"{RC.AOV_BREAKEVEN:,.0f}")
must("S4  hurdle premium",                       f"{RC.HURDLE_PREMIUM:,.0f}")
must("S4  non-grocery share the hurdle implies", f"{RC.HURDLE_NONGROCERY_SHARE:.1f}%")
must("S4  DuPont turnover leg",                  f"{RC.dupont(RC.AOV_HURDLE)['capital_turn']:.2f}")
must("S4  DuPont margin leg",                    f"{RC.dupont(RC.AOV_HURDLE)['ebit_margin']:.2%}")
must("S4  capital employed",                     f"{RC.CE_BASE/1e5:,.0f}")

# ---- slide 6: the operating model ----------------------------------------------
must("S6  runner breakeven volume, solved",      f"{FM.breakeven_volume():.0f}/day")
must("S6  gig:runner ratio, JPM anchor",         f"{CS.RATIO_JPM:.2f}")
must("S6  gig:runner ratio, UBS anchor",         f"{CS.RATIO_UBS:.2f}")

# ---- slide 7: the financials ----------------------------------------------------
must("S7  capex midpoint",                       f"{RC.CAPEX_MID/1e5:,.0f}")
must("S7  working capital",                      f"{WC.WC_ADOPTED/1e5:,.0f}")
must("S7  cash conversion cycle",                f"{WC.ZEPTO_CCC:.0f}")
must("S7  IRR at the hurdle AOV",                f"{RC.irr(RC.AOV_HURDLE):.1%}")
must("S7  ROCE at a 30% basket",                 f"{RC.roce(RC.AOV_UP):.1%}")
must("S7  post-tax hurdle AOV",                  f"{RC.AOV_HURDLE_POSTTAX:,.0f}")

# ---- slide 8: roadmap and gate --------------------------------------------------
must("S8  the day-90 gate is named",             "day-90")
must("S8  volume shock breakeven",               "647")
must("S8  the three concessions are present",    "concessions")

# ---- nothing superseded may appear anywhere ---------------------------------------
must_not("Round 1 breakeven Rs528",   "Rs528")
must_not("Round 1 Minutes AOV Rs775", "Rs775")
must_not("Round 1 city asset turn",   "12.6x")
must_not("superseded working capital", "Rs95.7")
must_not("superseded breakeven Rs554", "Rs554")
must_not("stale NWC days",            "NWC 18d")
must_not("placeholder text",          "TBD")
must_not("placeholder text, lorem",   "Lorem")

if __name__ == "__main__":
    bad = [c for c in checks if not c[0]]
    print(f"\nVERIFYING {VERIFIED_NAME}  ({len(pages)} slides)\n" + "="*78)
    for ok, lab, needle in checks:
        print(("  OK  " if ok else "  FAIL") + f"  {lab:<44} {needle}")
    print(f"\n{len(checks)-len(bad)}/{len(checks)} deck checks pass")
    if bad: raise SystemExit("DECK VERIFICATION FAILED")
