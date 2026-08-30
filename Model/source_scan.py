"""
SCAN THE SOURCE, NOT ONLY THE OUTPUT.

Two failure modes that a built-artifact checker cannot see, because both live upstream of
the artifact:

  1. A POLICY LITERAL REDECLARED OUTSIDE params.py. campus_model.NWC_DAYS = 18 survived
     twelve days past its supersession and break_mode imported it. Deleting that one line
     fixed the instance; only a scan fixes the CLASS. working_capital.py was still
     declaring 14.0, 12.0, 18.0 and carrying days=18.0 as a function default after the
     first pass - the same defect, one file over.

  2. UNSUPPORTED ATTRIBUTION IN A BUILD INPUT. The final PPTX was corrected while
     "the client manages to" and "management's own ceiling" survived in the build prompts,
     HANDOFF.md and two superseded builders - any of which can be regenerated INTO a deck.
     Checking the .pptx alone checks the last link in the chain.

Scope note: Decisions_Log.md and Research Pulls/ are HISTORICAL RECORDS and are excluded by
design. A log that records what we once believed is supposed to contain what we once
believed. Everything that can be built FROM is in scope.
"""
import ast, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- 1. policy literals
POLICY_NAME = re.compile(r"NWC.*DAYS|DAYS.*NWC|CAMPUSES|GATE_TOPOLOGY|LABOUR_BASIS|"
                         r"CLUSTER_VOLUME|RESTART_CREDIT", re.I)
POLICY_VALS = {14.0, 12.0, 18.0}

def policy_redeclarations():
    """Module-level assignments of a policy NAME to a bare literal, outside params.py."""
    bad = []
    for f in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        base = os.path.basename(f)
        if base in ("params.py", "source_scan.py"): continue
        try: tree = ast.parse(open(f, encoding="utf-8").read())
        except SyntaxError: continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and POLICY_NAME.search(t.id) \
                       and isinstance(node.value, ast.Constant) \
                       and isinstance(node.value.value, (int, float)) \
                       and float(node.value.value) in POLICY_VALS:
                        bad.append(f"{base}:{node.lineno}  {t.id} = {node.value.value}")
            # a policy value smuggled in as a function default
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for a, d in zip(node.args.args[-len(node.args.defaults):] if node.args.defaults else [],
                                node.args.defaults):
                    if isinstance(d, ast.Constant) and isinstance(d.value, (int, float)) \
                       and float(d.value) in POLICY_VALS and POLICY_NAME.search(a.arg + node.name):
                        bad.append(f"{base}:{node.lineno}  def {node.name}({a.arg}={d.value})")
    return bad

# ---------------------------------------------------------------- 2. attribution
# The 40% ROCE is ETERNAL's - Blinkit's PARENT, a competitor. The 30-40% non-grocery range is
# SWIGGY's. Neither is a Flipkart commitment, and language implying otherwise reads as
# manufacturing client endorsement.
BANNED = [
    "the client manages", "client manages to", "CLIENT MANAGES",
    "client's own hurdle", "the client's own",
    "management's own", "management's stated", "management has already",
    "management ceiling", "management's ceiling", "a ceiling management",
    "the client's hurdle",
    "stated ceiling",          # implies someone stated it as a ceiling; Swiggy disclosed a RANGE
]
# Records of what we once believed, not things anything is built from.
EXCLUDE_DIRS = ("_backup", "_superseded", "Research Pulls", "papers", "__pycache__",
                "_deck_pages", "Earlier wired case solution template", "skill-observations",
                "Case", "Semi Final Case", "Pngs")
EXCLUDE_FILES = ("Decisions_Log.md", "PROF_REVIEW_ADJUDICATION.md", "SYNC_REVIEW_2026-08-30.md",
                 "VERIFICATION_ARCHITECTURE_v2.md", "CHANGE_REPORT_2026-08-29.md",
                 "source_scan.py", "FINAL_AUDIT.md", "CORPUS_SWEEP_2026-08-27.md",
                 "DECK_TEARDOWN_WiRED9.md", "RUBRIC_CHECK.md")

def _in_scope(path):
    rel = os.path.relpath(path, ROOT)
    if any(d in rel for d in EXCLUDE_DIRS): return False
    return os.path.basename(path) not in EXCLUDE_FILES

def attribution_hits():
    hits = []
    for pat in ("*.py", "*.md", "Model/*.py"):
        for f in glob.glob(os.path.join(ROOT, pat)) + glob.glob(os.path.join(HERE, "*.py")):
            if not _in_scope(f): continue
            try: txt = open(f, encoding="utf-8").read()
            except Exception: continue
            for i, line in enumerate(txt.split("\n"), 1):
                # A blocklist has to contain the phrases it blocks, and the review documents
                # have to quote what they are correcting. `# scan:allow` marks a line whose
                # PURPOSE is to name the banned string. It is deliberately noisy to write.
                if "scan:allow" in line: continue
                for b in BANNED:
                    if b in line:
                        hits.append(f"{os.path.relpath(f, ROOT)}:{i}  ...{b}...")
    return sorted(set(hits))


# ---------------------------------------------------------------- 3. stale cost bases
# THE DEFECT: a superseded value passed as a LITERAL where a model quantity belongs.
#   audit.py:  breakeven_d2_consistent(CAMPUS_FIXED, 19.0, ...)   <- Rs19 last mile, now 17.61
#   cost_stack: def s19_report(d2_cost=19.0)                      <- as a function DEFAULT
#   gap_check:  breakeven_d2_consistent(CAMPUS_FIXED, 19.0, opd)  <- labelled "adopted basis"
# All three computed a stale answer that a stale literal on the other side then agreed with, so
# the check passed while asserting a number the deck does not contain. Function defaults are the
# quietest hiding place - the same shape as campus_model.NWC_DAYS = 18 and wc_old_construct(days=18.0).
SUPERSEDED_BASES = {19.0, 8.50, 325.0, 90.0, 578.0, 763.0, 580.0, 647.1, 622.7, 595.4,
                    589.1, 4.71, 825.0, 117.8, 77.1, 185.0}
BASIS_FUNCS = {"breakeven_d2_consistent", "consolidation_implied_by_d2", "cm_per_order",
               "wc_old_construct", "wc_nwc_on_nov", "s19_report", "aov_for_roce", "dupont"}

def stale_bases():
    """A superseded value passed as a literal argument to a basis-taking function, or sitting
    as one of its defaults."""
    bad = []
    for f in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        base = os.path.basename(f)
        if base in ("params.py", "source_scan.py"): continue
        try:
            src = open(f, encoding="utf-8").read(); tree = ast.parse(src)
        except SyntaxError: continue
        lines = src.split("\n")
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
                if fn in BASIS_FUNCS:
                    for a in list(node.args) + [k.value for k in node.keywords]:
                        if isinstance(a, ast.Constant) and isinstance(a.value, (int, float)) \
                           and float(a.value) in SUPERSEDED_BASES:
                            if "scan:allow" in lines[node.lineno-1]: continue
                            bad.append(f"{base}:{node.lineno}  {fn}(... {a.value} ...)")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in BASIS_FUNCS:
                for d in node.args.defaults:
                    if isinstance(d, ast.Constant) and isinstance(d.value, (int, float)) \
                       and float(d.value) in SUPERSEDED_BASES:
                        bad.append(f"{base}:{node.lineno}  def {node.name}(... = {d.value})")
    return sorted(set(bad))

# ---------------------------------------------------------------- 4. stale figures in documents
# verify_docs and verify_spec check the figures they were TOLD to check - 31 and 79 of them - so a
# superseded value anywhere outside those lists passes untouched. HANDOFF passed 31/31 while
# stating CE Rs325.0L and 8.50x; the spec passed 79/79 while listing shocks 647/623/595/589.
# Positive checks cannot find a figure nobody listed. Absence scans can.
DOC_STALE = {"Rs325.0": "CE (now 323.9)", "₹325.0": "CE (now 323.9)",
             "Rs90.0 L": "WC (now 88.9)", "₹90.0 L": "WC (now 88.9)",
             "Rs578": "ROCE breakeven (now 571)", "₹578": "ROCE breakeven (now 571)",
             "Rs763": "hurdle (now 755)", "₹763": "hurdle (now 755)",
             "Rs825": "post-tax (now 817)", "₹825": "post-tax (now 817)",
             "8.50x": "turn (now 8.44)", "8.50×": "turn (now 8.44)",
             "32.7%": "ROCE 30% (now 34.4%)", "57.1%": "ROCE 40% (now 58.8%)",
             "12.9%": "downside ROCE (now 14.0%)", "67 mo": "downside payback (now 62)",
             "67-month": "downside payback (now 62)",
             "Rs77.1": "WC target (now 76.2)", "₹77.1": "WC target (now 76.2)",
             "Rs647": "shock (now 640)", "₹647": "shock (now 640)",
             "Rs623": "shock (now 615)", "₹623": "shock (now 615)",
             "Rs595": "shock (now 588)", "₹595": "shock (now 588)",
             "Rs589": "shock (now 582)", "₹589": "shock (now 582)",
             "311/311": "audit count", "80/80": "deck count", "83/83": "deck count",
             "Rs19.0": "last mile (now 17.6)", "₹19.0": "last mile (now 17.6)",
             "of 760": "district denominator (now 765 pairs)",
             "four verification commands": "the layer count (one command, every layer)",
             "all four layers": "the layer count", "ALL FOUR LAYERS": "the layer count",
             "760 districts": "district denominator (now 765 pairs)"}
DOCS = ("HANDOFF.md", "DECK_SPEC_SemiFinal.md", "PPT_BUILD_PROMPT_SemiFinal.md", "README.md",
        "DECK_ASSET_PLAN_SemiFinal.md", "Napkin_Prompts_SemiFinal.md", "BUILD_PLAN.md")
# The GENERATORS are build inputs too. `make_workbook.py` typed "of 760 districts" into the sheet
# it generates - a hardcoded literal inside the file written to stop hardcoded literals.
GENERATORS = ("Model/make_workbook.py", "Model/make_readme.py", "Model/make_public_data.py",
              "Model/make_screenshots.py", "Model/clean_notebooks.py")

def stale_in_documents():
    bad = []
    for d in DOCS + GENERATORS:
        p = os.path.join(ROOT, d)
        if not os.path.exists(p): continue
        for i, line in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            if "scan:allow" in line or "SUPERSEDED" in line or "Round 1" in line: continue
            for k, what in DOC_STALE.items():
                if k in line: bad.append(f"{d}:{i}  {k}  ({what})")
    return sorted(set(bad))

if __name__ == "__main__":
    pr, ah = policy_redeclarations(), attribution_hits()
    sb, sd = stale_bases(), stale_in_documents()
    print(f"policy literals redeclared outside params.py: {len(pr)}")
    for b in pr: print("   ", b)
    print(f"unsupported attribution in build inputs:      {len(ah)}")
    for b in ah: print("   ", b)
    print(f"superseded value used as a cost basis:         {len(sb)}")
    for b in sb: print("   ", b)
    print(f"superseded figures in build documents:         {len(sd)}")
    for b in sd: print("   ", b)
