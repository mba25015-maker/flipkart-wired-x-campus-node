"""
BUILD _release_repo/ FROM A MANIFEST, NOT BY HAND.

_release_repo/ is what gets pushed. It was assembled and refreshed BY HAND, which put the
package's own defect class into the one tree a judge actually reads: a mirror maintained by
copying. After the last round the working folder verified 366/183 while the staged tree still
carried the previous build's deck, workbook, README and four .py files - a discrepancy nothing
could detect, because no verifier compares the two trees.

So the tree is now DERIVED. ROOT_FILES and TREES below are the whole definition of what is
published; EXCLUDE is the whole definition of what never is. Anything in the working folder and
not named here does not reach GitHub - which is the safe default for a folder that also holds
licensed PDFs, the organisers' template and an internal push note.

Run by release.py at step 5, after the package has passed. verify_artifacts.py then re-runs the
whole five-layer sequence INSIDE the staged tree, so the claim "a clean clone reproduces this"
is tested rather than asserted.
"""
import os, shutil, subprocess, sys

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(HERE)
STAGE = os.path.join(ROOT, "_release_repo")

# EVERYTHING THAT IS PUBLISHED, AND NOTHING ELSE.
ROOT_FILES = [
    ".gitignore",
    "Flipkart_Minutes_WiRED_SemiFinal_FULL_light.pptx",
    "Campus_Store_Model.xlsx",
    "README.md",
    "HANDOFF.md",
    "DECK_SPEC_SemiFinal.md",
    "PPT_BUILD_PROMPT_SemiFinal.md",
    "requirements.txt",
]
TREES = ["Model", "notebooks"]

# EVERYTHING THAT IS NEVER PUBLISHED. Licensed source and the organisers' template are excluded
# by omission (they are not in ROOT_FILES or TREES); these are the paths that live INSIDE a
# published tree and would otherwise ride along.
EXCLUDE = [
    ".DS_Store", "__pycache__", "*.pyc", "*.pyo", ".ipynb_checkpoints",
    "_render",              # local render scratch
    "appendix", "charts",   # superseded builders, kept locally for reference only
    "_verification.json",   # a local run record; the staged tree writes its own
]

def main():
    if not os.path.isdir(STAGE):
        os.makedirs(STAGE)
    ex = []
    for pat in EXCLUDE:
        ex += ["--exclude", pat]
    for t in TREES:
        src = os.path.join(ROOT, t)
        if not os.path.isdir(src):
            print(f"  MISSING tree {t} - cannot stage"); return 1
        r = subprocess.run(["rsync", "-a", "--delete"] + ex + [src + "/",
                           os.path.join(STAGE, t) + "/"])
        if r.returncode: return r.returncode
        print(f"  {t}/")
    for f in ROOT_FILES:
        src = os.path.join(ROOT, f)
        if not os.path.exists(src):
            print(f"  MISSING file {f} - cannot stage"); return 1
        shutil.copy2(src, os.path.join(STAGE, f))
        print(f"  {f}")
    # A LOUD ASSERTION, NOT A COMMENT. The push note names local paths and sandbox workflow and
    # must never be published; the same goes for the licensed corpora and the template. If any
    # of them ever appears in the staged tree, staging fails rather than warning.
    banned = ["PUSH_INSTRUCTIONS.md", "Research Pulls", "papers", ".nbdeps", "Case",
              "_superseded", "_release_repo"]
    present = [b for b in banned if os.path.exists(os.path.join(STAGE, b))]
    if present:
        print(f"  STAGING FAILED: must never be published -> {present}")
        return 1
    print(f"  staged {STAGE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
