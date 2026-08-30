"""
PUSH_INSTRUCTIONS.md CARRIES THE LIVE LAYER COUNTS, AND IT IS NOT ALLOWED TO CARRY THEM BY HAND.

The counts appear in five places: check_counts.py, deck_checks.py, the README, the workbook and
this internal note. The first two are PINS - typed deliberately, so that adding a check without
noticing fails the run loudly. The last three are REPORTS: they describe the pins, and a report
that is typed goes stale the moment a pin moves. It did, three times.

So the README and the workbook are generated, and this script does the same for
PUSH_INSTRUCTIONS.md - rewriting the "a / b / c / d / e" string wherever it appears from
check_counts.DEFINED. Nothing is asserted here that was not already asserted upstream; this only
stops a human copy of an already-checked number from drifting.

The file itself is INTERNAL - it holds sandbox paths and workflow detail and is deliberately
outside _release_repo/ and named in .gitignore. It is never published.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_counts as CC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "PUSH_INSTRUCTIONS.md")
ORDER = ("audit", "docs", "spec", "deck", "artefacts")
WANT = " / ".join(str(CC.DEFINED[k]) for k in ORDER)
PAT = re.compile(r"\d+ / \d+ / \d+ / \d+ / \d+")

def main():
    if not os.path.exists(PATH):
        print(f"  PUSH_INSTRUCTIONS.md absent - nothing to sync (this is normal in a staged tree)")
        return 0
    src = open(PATH, encoding="utf-8").read()
    out, n = PAT.subn(WANT, src)
    if n == 0:
        print(f"  WARNING: no layer-count string found in PUSH_INSTRUCTIONS.md")
        return 1
    if out != src:
        open(PATH, "w", encoding="utf-8").write(out)
    print(f"  PUSH_INSTRUCTIONS.md  {n} count string(s) -> {WANT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
