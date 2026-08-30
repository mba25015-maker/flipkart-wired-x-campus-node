"""Verify that the headline figures written in HANDOFF.md agree with the model.
Parses the numbers OUT OF THE DOCUMENT rather than comparing against hand-typed
expectations -- an earlier version of this check compared model-to-my-typing and
silently passed a figure that did not tie out."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campus_model as M, cost_stack as C, break_mode as B, basket as BK, working_capital as W, sla as S
_rows, D2 = S.volume_weighted()
DOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "HANDOFF.md")

def num(tok):
    t = re.sub(r"[^0-9.\-]", "", tok).rstrip(".")
    return float(t)

# label -> (regex capturing the number as written in the doc, model value)
CHECKS = {
 "fixed base":            (r"\*\*Rs([\d,]+)/month\*\*, JM Financial Exhibit 13", C.CAMPUS_FIXED),
 "flex share":            (r"\*\*([\d.]+)% is not truly fixed", C.fixed_flex_share()*100),
 "band low":              (r"\*\*Rs([\d,]+) \(Rs60/sqft\)", C.T12_FIXED_LOW),
 "band high":             (r"Rs([\d,]+) \(Rs75/sqft\)", C.T12_FIXED_HIGH),
 "band width":            (r"band width ([\d.]+)%", C.T12_FIXED_BAND_PCT*100),
 "tier3 counterfactual":  (r"Tier-3\+ store would be Rs([\d,]+)", C.T3P_FIXED_MID),
 "utilities":             (r"utilities \(\*\*Rs([\d,]+)\*\*, sourced", C.UTILITIES_POWER),
 "other fixed":           (r'"other fixed" \(Rs([\d,]+),', C.OTHER_FIXED),
 "breakeven adopted":     (r"\| \*\*Rs(\d+)\*\* \| JM fixed base, last mile", C.breakeven_d2_consistent(C.CAMPUS_FIXED, D2)),
 "contribution identity": (r"\*\*Rs([\d.]+)\*\* = Blinkit", M.cm_per_order(M.BLINKIT_AOV, 1.0)),
 "minutes aov":           (r"\*\*AOV Rs(\d+)\*\* \(TechCrunch", M.MINUTES_AOV),
 "city turn":             (r"\*\*City ([\d.]+)x", M.CITY_TURN),
 "campus turn":           (r"campus ([\d.]+)x · ratio", M.CAMPUS_TURN),
 "turn ratio":            (r"ratio ([\d.]+)\.\*\*", M.TURN_RATIO),
 "d2 last mile":          (r"campus last mile Rs([\d.]+)/order", D2),
 "gig ratio jpm":         (r"Rs72/rostered\n?hour = ([\d.]+)x", C.RATIO_JPM),
 "gig ratio ubs":         (r"the ratio is \*\*([\d.]+)x", C.RATIO_UBS),
 "wc adopted":            (r"\*\*Working capital Rs([\d.]+) lakh\*\*", W.WC_ADOPTED/1e5),
 "wc target":             (r"Rs([\d.]+) lakh at\ntheir 12-day target", W.WC_TARGET/1e5),
 "wc state b 30d":        (r"Rs([\d.]+) lakh at 30 days", W.WC_STATE_B_30D/1e5),
 "nwc days":              (r"Eternal's current \*\*(\d+) days", W.ETERNAL_NWC_DAYS_NOW),
 "zepto ccc":             (r"cash conversion cycle (-\d+) days", W.ZEPTO_CCC),
 "shrinkage":             (r'= Rs([\d.]+) lakh/month\*\*', W.DAILY_NOV*W.SHRINKAGE_PCT_NOV*30/1e5),
 "reactivation opex":     (r"Opex \*\*Rs([\d,]+)\*\*", B.reactivation(0.15)["opex_total"]),
 "hold cost":             (r"\*\*Hold through the break Rs([\d.]+) lakh", B.relocate_vs_flex()["flex_total"]/1e5),
 "relocate capex":        (r"relocate once Rs(\d+) lakh", B.RELOCATE_CAPEX/1e5),
 "hold pct":              (r"Holding costs (\d+)% of one relocation", B.relocate_vs_flex()["flex_vs_relocate"]*100),
 "basket slope":          (r"AOV = ([\d.]+) x \(non-grocery", BK.SLOPE),
 "basket r2":             (r"R2 = (0\.\d+)", BK.R2),
 "basket occasion":       (r"Rs450 -> Rs(\d+) \(term-start", BK.OCCASION_AOV),
 "basket share needed":   (r"Rs\d+ at ([\d.]+)%\nnon-grocery", BK.SHARE_NEEDED_AFTER_OCCASION),
}

def run():
    doc = open(DOC).read()
    bad, missing = [], []
    for label, (rx, model_val) in CHECKS.items():
        m = re.search(rx, doc)
        if not m:
            missing.append(label); continue
        raw = m.group(1)
        written = num(raw)
        dp = len(raw.split(".")[1]) if "." in raw else 0
        if round(float(model_val), dp) != round(written, dp):
            bad.append((label, written, float(model_val)))
    ok = len(CHECKS) - len(bad) - len(missing)
    for l, w, mv in bad:     print(f"  MISMATCH  {l:<24} doc={w:>12,.2f}   model={mv:>12,.2f}")
    for l in missing:        print(f"  NOT FOUND {l:<24} (regex did not match the document)")
    print(f"\n{ok}/{len(CHECKS)} HANDOFF figures tie out to the model")
    return not (bad or missing)

if __name__ == "__main__":
    sys.exit(0 if run() else 1)
