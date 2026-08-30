#!/usr/bin/env python3
"""
THE ONLY SUPPORTED WAY TO VERIFY THIS PACKAGE.

    python3 Model/run_all.py

No arguments. Nonzero exit on any failure. The deck's A-1 page and the repository README
quote THIS command, so the command a judge runs and the command we run are the same one.

WHY IT EXISTS. verify_deck.py used to default to the superseded four-slide reference build.
Run bare - exactly as the deck instructed a judge to run it - it reported 51/93 and DECK
VERIFICATION FAILED. Nothing caught it, because the verifier was only ever invoked by hand
with an explicit path by someone who already knew which path was right. A verification stack
that can be pointed at the wrong file eventually will be, so the path now comes from
params.FINAL_DECK and there is one entrypoint.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "_verification.json")
KEY = {"audit.py": "audit", "verify_docs.py": "docs",
       "verify_spec.py": "spec", "verify_deck.py": "deck"}
STEPS = [("audit.py",       "the model against itself, incl. cross-module reconciliation"),
         ("verify_docs.py", "HANDOFF.md against the model"),
         ("verify_spec.py", "DECK_SPEC + PPT_BUILD_PROMPT against the model"),
         ("verify_deck.py", "the BUILT .pptx against the model")]

def main():
    print("=" * 78); print("  VERIFYING THE FULL PACKAGE".center(78)); print("=" * 78)
    results, failed, record = [], False, {}
    for script, what in STEPS:
        r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                           capture_output=True, text=True)
        tail = [l for l in r.stdout.strip().split("\n") if "pass" in l or "tie out" in l]
        line = tail[-1].strip() if tail else "(no summary line)"
        ok = r.returncode == 0
        failed |= not ok
        m = re.search(r"(\d+)\s*/\s*(\d+)", line)
        if m: record[KEY[script]] = {"passed": int(m.group(1)), "total": int(m.group(2))}
        results.append((ok, script, line, what))
        print(f"  {'PASS' if ok else 'FAIL'}  {script:<16} {line:<48} {what}")
        if not ok:
            emitted = False
            for l in r.stdout.strip().split("\n"):
                if "FAIL" in l or "MISMATCH" in l:
                    print(f"          {l.strip()}")
                    emitted = True
            if not emitted and r.stderr.strip():
                for l in r.stderr.strip().split("\n")[-8:]:
                    print(f"          {l.strip()}")
    # The results file is what check_counts.tile() reads. Written on every run, pass or
    # fail, so a failing run REVOKES a previous pass claim rather than leaving it standing.
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, sort_keys=True)
    print("-" * 78)
    if failed:
        print("  PACKAGE VERIFICATION FAILED")
        print("  _verification.json updated: the deck's self-report drops to 'checks defined'")
        return 1
    print("  ALL FOUR LAYERS PASS"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
