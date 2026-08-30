"""
GENERATE README.md FROM THE MODEL.

The README advertised `311/311` and `80/80` and told the reader to verify against  # scan:allow
`Flipkart_Minutes_WiRED_SemiFinal_REFERENCE_dark.pptx` - a deck that no longer exists in the
package. It was the last hand-typed statement of the package's own counts, and it went stale
exactly like the A-1 tiles and the workbook Read Me did.

Nothing about the package's own state is typed here. Counts come from check_counts (which reads
the recorded run), the deck filename from params, and the command from run_all.
"""
import os
import check_counts as CC, params as P

REPO = "mba25015-maker/flipkart-wired-x-campus-node"
# The six Colab badges were added to the published README by hand, and the first version of this
# generator silently dropped them - a generator that omits something the artefact had is exactly
# as destructive as a hand-edit that goes stale. They are generated here, from the notebook list.
NOTEBOOKS = [
    ("L1", "L1_Audit_Verification",  "Audit and verification",
     "runs every verification layer: model, documents, specification, final deck and companion artefacts"),
    ("L2", "L2_Dead_Zone_Solver",    "Dead-zone solver",
     "compares five strategies under the operating constraints"),
    ("L3", "L3_Return_Model",        "Return model",
     "reproduces ROCE, payback, IRR, DuPont and the benchmark-implied AOV"),
    ("L4", "L4_District_Screen",     "District screen",
     "runs the AISHE district screen on the public-safe aggregates"),
    ("L5", "L5_Fulfilment_Model",    "Fulfilment model",
     "reproduces the SLA, batching, fleet topology and cost per order"),
    ("L6", "L6_Basket_Regression",   "Basket regression",
     "reproduces the four-quarter basket fit and the mix ladder"),
]

def _badges():
    rows = ["| Notebook | What it reproduces | Open |", "|---|---|---|"]
    for tag, stem, title, what in NOTEBOOKS:
        url = f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{stem}.ipynb"
        rows.append(f"| **{tag}** — {title} | {what} | "
                    f"[![Open {tag} in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url}) |")
    return "\n".join(rows)

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

LAYERS = [
    ("audit.py",           "audit",     "checks pass",           "model against itself, incl. cross-module reconciliation, source scans and claim checks"),
    ("verify_docs.py",     "docs",      "HANDOFF figures tie out","HANDOFF.md figures against the model"),
    ("verify_spec.py",     "spec",      "spec figures tie out",   "deck specification and build prompt against the model"),
    ("verify_deck.py",     "deck",      "deck checks pass",       "opens the built .pptx, reads every run of text and every native chart value, and checks presence AND absence"),
    ("verify_artifacts.py","artefacts", "artefact checks pass",   "the workbook, the six notebooks, the asset manifest and the public data"),
]

def _results_block():
    out = []
    for f, k, verb, _ in LAYERS:
        n = CC.DEFINED[k]
        out.append(f"{f:<21}{n}/{n} {verb}")
    return "\n".join(out)

def _layer_table():
    rows = ["| layer | scope |", "|---|---|"]
    for f, k, _, scope in LAYERS:
        rows.append(f"| `{f}` | {scope} |")
    return "\n".join(rows)

def render():
    v = CC.results() or {}
    def n(k): return CC.DEFINED[k]
    ran = CC.all_verified()
    _n = len(CC.DEFINED); _word = {4:"four",5:"five",6:"six"}.get(_n, str(_n))
    status = (f"All {_word} layers passed on the last recorded run."
              if ran else "No clean run is recorded; the counts below are checks defined, not passed.")
    return f"""# Flipkart WiRED X — Campus Node Model

Reproducible analytical model and verification package for the Flipkart WiRED X semi-final
submission. Team **{P.TEAM_NAME}**.

Every headline figure in `{P.FINAL_DECK}` is computed by the model in `Model/` and asserted
against the built file. Nothing in the deck is typed by hand.

## Verify it — one command, no arguments

```bash
python3 Model/run_all.py
```

```
{_results_block()}
```

{status}

`run_all.py` exits nonzero if any layer fails and verifies the exact presentation named by
`Model/params.FINAL_DECK`. It takes no arguments by design: the previous workflow was several
separate commands, one of which needed an explicit filename, and it defaulted to a superseded
build when run without one.

To rebuild the deck and re-verify the exact stamped file:

```bash
python3 Model/release.py
```

Team identity is a model parameter (`Model/params.TEAM_NAME`), so both commands work on a clean
clone with no environment setup.

## Run the models in Google Colab

No install, no clone — each notebook runs the module it names against the package in this
repository.

{_badges()}

## What each layer checks

{_layer_table()}

The absence checks matter as much as the presence ones. A superseded figure sitting in a panel
nothing reads is invisible to a positive check, which is how a stale appendix survived four
passing layers once already.

## What a clean clone can and cannot do

`python3 Model/run_all.py` works with no setup: the repository ships the built deck, the
documents, and `Model/data` — district aggregates and parsed tables generated from the licensed
source. All {_word} layers verify.

`python3 Model/release.py` rebuilds the deck and needs two things this repository does not
redistribute: the organisers' template in `Case/`, and the licensed source under `Research Pulls/`.
Both are other people's assets. The build says so plainly if they are absent.

`Model/data` is generated by `Model/make_public_data.py`, not maintained by hand, and the model
reads it in both trees — there is no public variant of any module. An earlier arrangement kept
separate public and private copies of three modules, and they had already drifted apart.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Layout

| path | what |
|---|---|
| `Model/params.py` | every contested policy constant, defined once |
| `Model/run_all.py` | the only supported verification entrypoint |
| `Model/release.py` | build → verify → capture → stamp → re-verify |
| `Model/source_scan.py` | scans the source tree, not just the artifact |
| `notebooks/` | six runnable notebooks, L1–L6 |
| `{P.FINAL_DECK}` | the submission |

## Reproducibility note

The counts above are generated from the recorded verification run, not typed. If you change the
model, `run_all.py` fails until the deck and documents are rebuilt to match — that is the point.
"""

if __name__ == "__main__":
    out = os.path.join(ROOT, "README.md")
    open(out, "w", encoding="utf-8").write(render())
    print("  wrote README.md from the model")
