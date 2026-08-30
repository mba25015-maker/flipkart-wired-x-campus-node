# Flipkart WiRED X — Campus Node Model

Reproducible analytical model, final deck, notebooks, and workbook supporting Team ANAVRIN's Flipkart WiRED X semi-final submission.

## Verify everything

From the repository root, run one command:

```bash
python3 Model/run_all.py
```

Expected output:

```text
344/344 checks pass
31/31 HANDOFF figures tie out to the model
79/79 spec figures tie out to the model
133/133 deck checks pass
ALL FOUR LAYERS PASS
```

`run_all.py` exits nonzero if any layer fails and verifies the exact presentation named by `Model/params.py`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 Model/run_all.py
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1`.

## Publication package

| Item | Purpose |
|---|---|
| `Model/run_all.py` | Runs all four verification layers |
| `Model/audit.py` | Model assertions and cross-module reconciliations |
| `Model/params.py` | Single source for contested policy constants and release paths |
| `Model/solver.py` | Dead-zone strategy comparison |
| `Model/roce.py` | ROCE, payback, IRR, and hurdle-AOV analysis |
| `Model/aishe_district.py` | Public-safe district screening model |
| `Model/sla.py` and `Model/fleet_mix.py` | Fulfilment, roster, SLA, and cost-per-order logic |
| `Model/basket.py` | Basket regression and mix ladder |
| `notebooks/` | Six judge-runnable notebook wrappers |
| `Campus_Store_Model.xlsx` | Auditable calculation workbook |
| `Flipkart_Minutes_WiRED_SemiFinal_FULL_light.pptx` | Exact deck checked by the verifier |

## Data and source boundary

The public repository contains permitted aggregate and derived inputs under `Model/data/`. Paid or licence-restricted PDFs and source tables are deliberately excluded. A paid subscription or downloaded copy does not automatically grant public redistribution rights.

The model records source provenance and assumptions, while the verification scripts establish internal consistency and reproducibility. They do not independently certify every third-party source or redistribution licence.

## Reproducibility notes

- Run commands from the repository root.
- The adopted topology is two employed runners per gate across three gates; pooling remains a priced conditional upside.
- Working capital uses one definition throughout the model.
- Last-mile cost is separated into a volume-weighted city leg and a roster-priced in-gate leg.
- The joint downside remains visible: payback exceeds the 60-month node life.
- The included presentation is the exact verified release copy. Rebuilding its visual shell requires the internal case template, which is not part of this public package; verification does not require that template.
