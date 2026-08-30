# Flipkart WiRED X — Campus Node Model

Reproducible analytical model and verification package for the Flipkart WiRED X semi-final
submission. Team **ANAVRIN**.

Every headline figure in `Flipkart_Minutes_WiRED_SemiFinal_FULL_light.pptx` is computed by the model in `Model/` and asserted
against the built file. Nothing in the deck is typed by hand.

## Verify it — one command, no arguments

```bash
python3 Model/run_all.py
```

```
audit.py             378/378 checks pass
verify_docs.py       31/31 HANDOFF figures tie out
verify_spec.py       79/79 spec figures tie out
verify_deck.py       184/184 deck checks pass
verify_artifacts.py  28/28 artefact checks pass
```

All five layers passed on the last recorded run.

`run_all.py` exits nonzero if any layer fails and verifies the exact presentation named by
`Model/params.FINAL_DECK`. It takes no arguments by design: the previous workflow was several
separate commands, one of which needed an explicit filename, and it defaulted to a superseded
build when run without one.

The demand-state assortment policy has its own transparent guardrail report:

```bash
python3 Model/assortment.py
```

It preserves a 16,500-SKU network range through SDFC backfill while varying the modelled local
range by demand state. The 7,000 / 8,000 / 4,200 local caps are policy inputs, not observed demand
forecasts, and the financial evidence gate remains closed: no incremental saving enters the
published solver.

To rebuild the deck and re-verify the exact stamped file:

```bash
python3 Model/release.py
```

Team identity is a model parameter (`Model/params.TEAM_NAME`), so both commands work on a clean
clone with no environment setup.

## Run the models in Google Colab

No install, no clone — each notebook runs the module it names against the package in this
repository.

| Notebook | What it reproduces | Open |
|---|---|---|
| **L1** — Audit and verification | runs every verification layer: model, documents, specification, final deck and companion artefacts | [![Open L1 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L1_Audit_Verification.ipynb) |
| **L2** — Dead-zone solver | compares five strategies under the operating constraints | [![Open L2 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L2_Dead_Zone_Solver.ipynb) |
| **L3** — Return model | reproduces ROCE, payback, IRR, DuPont and the benchmark-implied AOV | [![Open L3 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L3_Return_Model.ipynb) |
| **L4** — District screen | runs the AISHE district screen on the public-safe aggregates | [![Open L4 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L4_District_Screen.ipynb) |
| **L5** — Fulfilment & demand-state assortment | reproduces the SLA, batching, fleet topology, cost per order and state-specific local range | [![Open L5 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L5_Fulfilment_Model.ipynb) |
| **L6** — Basket regression | reproduces the four-quarter basket fit and the mix ladder | [![Open L6 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L6_Basket_Regression.ipynb) |

## What each layer checks

| layer | scope |
|---|---|
| `audit.py` | model against itself, incl. cross-module reconciliation, source scans and claim checks |
| `verify_docs.py` | HANDOFF.md figures against the model |
| `verify_spec.py` | deck specification and build prompt against the model |
| `verify_deck.py` | opens the built .pptx, reads every run of text and every native chart value, and checks presence AND absence |
| `verify_artifacts.py` | the workbook, the six notebooks, the asset manifest and the public data |

The absence checks matter as much as the presence ones. A superseded figure sitting in a panel
nothing reads is invisible to a positive check, which is how a stale appendix survived four
passing layers once already.

## What a clean clone can and cannot do

`python3 Model/run_all.py` works with no setup: the repository ships the built deck, the
documents, and `Model/data` — district aggregates and parsed tables generated from the licensed
source. All five layers verify.

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
| `Model/assortment.py` | demand-state local allocation, temperature constraints and financial evidence gate |
| `Model/run_all.py` | the only supported verification entrypoint |
| `Model/release.py` | build → verify → capture → stamp → re-verify |
| `Model/source_scan.py` | scans the source tree, not just the artifact |
| `notebooks/` | six runnable notebooks, L1–L6 |
| `ASSORTMENT_MODEL_HANDOFF.md` | evidence classes, current state allocations and pilot inputs required for recalibration |
| `Flipkart_Minutes_WiRED_SemiFinal_FULL_light.pptx` | the submission |

## Reproducibility note

The counts above are generated from the recorded verification run, not typed. If you change the
model, `run_all.py` fails until the deck and documents are rebuilt to match — that is the point.
