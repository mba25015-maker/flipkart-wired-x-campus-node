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
]
# Records of what we once believed, not things anything is built from.
EXCLUDE_DIRS = ("_backup", "_superseded", "Research Pulls", "papers", "__pycache__",
                "_deck_pages", "Earlier wired case solution template", "skill-observations",
                "Case", "Semi Final Case", "Pngs")
EXCLUDE_FILES = ("Decisions_Log.md", "PROF_REVIEW_ADJUDICATION.md",
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

if __name__ == "__main__":
    pr, ah = policy_redeclarations(), attribution_hits()
    print(f"policy literals redeclared outside params.py: {len(pr)}")
    for b in pr: print("   ", b)
    print(f"unsupported attribution in build inputs:      {len(ah)}")
    for b in ah: print("   ", b)
