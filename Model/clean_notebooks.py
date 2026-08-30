"""
CLEAN THE PUBLISHED NOTEBOOKS.

Three things were shipping inside the six notebooks, none of which any verification layer could
see, because every layer read the model, the documents or the .pptx:

  1. SAVED OUTPUTS carrying a snapshot of a past run - L1 showed 344/344 and 133/133 against a
     package now at 352 and 167. A saved output is a screenshot in JSON: it looks like evidence
     and is not regenerated.
  2. HARDCODED EXPECTED COUNTS in markdown and source, so the notebook asserted a number instead
     of printing one. Judges run these; the run should produce the number.
  3. THE AUTHOR'S HOME PATH, /Users/dubsey, in every one of the six.

So outputs are cleared, execution counts reset, local paths scrubbed, and typed counts replaced
with a statement that the run itself produces the figure. `verify_artifacts.py` asserts all of
that afterwards, because a cleaning step nothing checks is the same trap one level up.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CANDIDATES = [os.path.join(ROOT, "notebooks"), os.path.join(ROOT, "_release_repo", "notebooks")]

HOMEPATH = re.compile(r"/Users/[A-Za-z0-9_.-]+(?:/[^\s'\"]*)?")
# A typed count is a claim; a run is evidence. Replace the claim with what the run will show.
TYPED = [(re.compile(r"\b344\s*/\s*344\b"), "the audit count the run prints"),
         (re.compile(r"\b133\s*/\s*133\b"), "the deck count the run prints"),
         (re.compile(r"\b311\s*/\s*311\b"), "the audit count the run prints"),
         (re.compile(r"\b(?:80|83)\s*/\s*(?:80|83)\b"), "the deck count the run prints"),
         (re.compile(r"\b760 districts\b"), "the district count the run prints"),  # scan:allow - this IS the pattern list
         # A bare 760 in prose is the same stale denominator without the word after it.  # scan:allow - this IS the pattern list
         (re.compile(r"\b760-district\b"), "district"),  # scan:allow - this IS the pattern list
         (re.compile(r"\b760\b(?!\s*[,)])"), "the district count the run prints"),
         # The layer COUNT is a number about the package itself. Typed into the notebook, it went
         # stale the moment a fifth verifier was added.
         (re.compile(r"ALL FOUR LAYERS PASS"), "ALL LAYERS PASS"),  # scan:allow - this IS the pattern list
         (re.compile(r"All four rows must say"), "Every row must say"),
         (re.compile(r"\ball four layers\b"), "every layer"),  # scan:allow - this IS the pattern list
         (re.compile(r"\bfour layers\b"), "every layer")]  # scan:allow - this IS the pattern list

def clean_file(path):
    nb = json.load(open(path, encoding="utf-8"))
    changed = 0
    for c in nb.get("cells", []):
        if c.get("outputs"):
            c["outputs"] = []; changed += 1
        if c.get("execution_count") is not None:
            c["execution_count"] = None; changed += 1
        src = c.get("source", [])
        new = []
        for line in src:
            o = line
            line = HOMEPATH.sub("<path to the repository>", line)
            for rx, rep in TYPED:
                line = rx.sub(rep, line)
            if line != o: changed += 1
            new.append(line)
        c["source"] = new
    nb.get("metadata", {}).pop("widgets", None)
    json.dump(nb, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return changed

def main():
    total = 0
    for d in CANDIDATES:
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".ipynb"): continue
            n = clean_file(os.path.join(d, f)); total += n
            print(f"  cleaned {os.path.relpath(os.path.join(d,f), ROOT)}  ({n} edits)")
    if not total: print("  notebooks already clean")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
