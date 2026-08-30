#!/usr/bin/env python3
"""
THE RELEASE SEQUENCE:  build -> verify -> stamp -> verify the exact final file.

    TEAM_NAME="..." TEAM_ID="..." python3 Model/release.py

WHY IT IS FOUR STEPS AND NOT TWO. Slide A-1 reports the package's own verification result,
which is a self-reference: the deck cannot contain the outcome of verifying itself unless the
outcome is computed first and stamped in afterwards. The earlier build did this by carrying the
counts as constants, so the slide printed "116 / 116" on a build the verifier was actually
failing 115/116. A number a document states about itself must come from a run.

  1 BUILD      with no results file present, A-1 prints "N checks defined" - a claim about how
               many checks exist, which is true whether or not they pass.
  2 VERIFY     run_all.py runs all four layers and writes _verification.json.
  3a CAPTURE   photograph THAT run into A-1's two terminal images. They were previously
               captured by hand and went stale exactly like a literal - showing 311/311 and
               80/80 beside tiles reading 336 and 116, on the page arguing nothing drifts.
               An image cannot be asserted, so it has to be generated.
  3 STAMP      rebuild. A-1 now prints "N / N", but ONLY because step 2 recorded a clean run.
  4 RE-VERIFY  verify the EXACT file that carries the claim. This is the step that makes the
               claim true rather than merely consistent: the stamped file is a different file
               from the one verified in step 2, and it is the one going in front of a panel.

Any step failing stops the sequence and leaves the results file recording the failure, so the
next build reverts to "checks defined" instead of keeping a stale pass.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, "_verification.json")

def run(cmd, label):
    print(f"\n>>> {label}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(f"\n!!! {label} FAILED - stopping. The deck does not get to claim a pass.")
        raise SystemExit(r.returncode)

def main():
    py = sys.executable
    # Step 1 must build with NO standing claim. Blanked rather than deleted: an empty record
    # is unambiguous, and some mounts refuse deletion.
    with open(RESULTS, "w", encoding="utf-8") as fh: fh.write("{}\n")
    run([py, "Model/build_full.py", "light"], "1 BUILD  (A-1 prints 'checks defined')")
    run([py, "Model/run_all.py"],             "2 VERIFY (records _verification.json)")
    run([py, "Model/make_screenshots.py"],    "3a CAPTURE the clean run into A-1's screenshots")
    run([py, "Model/build_full.py", "light"], "3b STAMP  (A-1 prints passed/total)")
    run([py, "Model/verify_deck.py"],         "4 RE-VERIFY the exact stamped file")

    # And the claim must be the EARNED one. verify_deck only checks the form is legal, because
    # it cannot see its own outcome. This is the step that requires the passed form, on the
    # exact file that carries it, after that file has just verified clean.
    from pptx import Presentation
    import check_counts as _CC0, importlib as _il
    _il.reload(_CC0)
    _txt = " ".join(sh.text_frame.text for sl in Presentation(
        os.path.join(ROOT, _CC0.__dict__.get("FINAL", "") or __import__("params").FINAL_DECK)
    ).slides for sh in sl.shapes if sh.has_text_frame)
    _want = f"{_CC0.AUDIT_COUNT} / {_CC0.AUDIT_COUNT}"
    if _want not in _txt:
        print(f"\n!!! the stamped deck does not carry the earned claim {_want!r} - NOT RELEASED.")
        raise SystemExit(1)
    print(f"    stamped claim {_want!r} is present on the verified file.")
    import importlib, sys as _s
    _s.path.insert(0, HERE); import check_counts as CC; importlib.reload(CC)
    print("\n" + "=" * 78)
    print("  RELEASED." if CC.all_verified() else "  NOT RELEASED - results file is not clean.")
    for k in ("audit", "docs", "spec", "deck"):
        print(f"    {k:<6} {CC.tile(k)}")
    print("=" * 78)
    return 0 if CC.all_verified() else 1

if __name__ == "__main__":
    raise SystemExit(main())
