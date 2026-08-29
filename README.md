# Flipkart WiRED X — Campus Node Model

Public-safe, reproducible analytical model supporting the Flipkart WiRED X semi-final submission. Paid analyst documents and licensed raw workbooks are intentionally excluded.

[![Open the audit in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L1_Audit_Verification.ipynb)

## Run the public notebooks

| Link | Notebook | What it reproduces |
|---|---|---|
| [L1 — Audit](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L1_Audit_Verification.ipynb) | `audit.py` | Submission-wide 311-assertion audit |
| [L2 — Dead-zone solver](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L2_Dead_Zone_Solver.ipynb) | `solver.py` | Five-strategy decision rule |
| [L3 — Return model](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L3_Return_Model.ipynb) | `roce.py` | ROCE, DuPont, payback, IRR, external-benchmark AOV |
| [L4 — District screen](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L4_District_Screen.ipynb) | `aishe_district.py` | District shortlist and contestedness |
| [L5 — Fulfilment model](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L5_Fulfilment_Model.ipynb) | `sla.py`, `fleet_mix.py` | SLA, batching, runner threshold, volume weighting |
| [L6 — Basket regression](https://colab.research.google.com/github/mba25015-maker/flipkart-wired-x-campus-node/blob/main/notebooks/L6_Basket_Regression.ipynb) | `basket.py` | Four-quarter basket fit and limitation |

## Appendix assets

Judge-ready output captures, QR codes, and the page-by-page placement map are in [`assets/`](assets/):

- [`assets/screenshots/`](assets/screenshots/) — S1–S6, cropped at 2× resolution;
- [`assets/qr/`](assets/qr/) — one scan-ready QR image for each L1–L6 notebook;
- [`assets/manifests/deck_asset_manifest.csv`](assets/manifests/deck_asset_manifest.csv) — notebook, appendix page, proof line, QR, and screenshot mapping.

## Verify the submission

Run from the repository root:

```bash
python3 Model/audit.py
# Expected: 311/311 checks pass

python3 Model/verify_docs.py
# Expected: 31/31 HANDOFF figures tie out to the model

python3 Model/verify_spec.py
# Expected: 79/79 spec figures tie out to the model

python3 Model/verify_deck.py
# Expected: 80/80 deck checks pass
```

The public deck command verifies a text-only snapshot extracted from the passing reference deck; the PowerPoint itself is not redistributed. To verify the actual local submission artifact, supply its path explicitly:

```bash
python3 Model/verify_deck.py "/path/to/Flipkart_Minutes_WiRED_SemiFinal_REFERENCE_dark.pptx"
```

At packaging time, that local artifact passed `80/80` checks and had SHA-256 `f09fafc0006784c03e328752ed6194fe472e40baa24daabf09f8154cc1bece62`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\Activate.ps1`.

## Runnable modules

| Module | Purpose |
|---|---|
| `Model/audit.py` | Runs the submission-wide assertion framework |
| `Model/solver.py` | Compares five dead-zone strategies |
| `Model/roce.py` | Reproduces ROCE, DuPont, payback, IRR, and external-benchmark AOV calculations |
| `Model/aishe_district.py` | Runs the district screening and contestedness model |
| `Model/sla.py` | Reproduces fulfilment and SLA calculations |
| `Model/fleet_mix.py` | Calculates volume-weighted fulfilment cost |
| `Model/basket.py` | Runs the four-quarter basket regression |

Example:

```bash
python3 Model/solver.py
python3 Model/roce.py
python3 Model/aishe_district.py
python3 Model/sla.py
python3 Model/fleet_mix.py
```

## Public-safe data design

`Model/data/` contains only the minimal derived inputs needed to reproduce the calculations:

- district-level AISHE institution aggregates, with no institution-level records;
- state-level HCES urban MPCE values;
- aggregate IndiaStat/NSS screening statistics, with no paid source rows;
- aggregate tariff statistics, with no licensed cross-section.

The source PowerPoint, paid analyst PDFs, licensed workbooks, and the original `Research Pulls/` directory are not included. See [`Model/data/README.md`](Model/data/README.md) for provenance and limitations.

## Verification snapshots

`Model/verification/` contains authored analytical-document snapshots and a text-only deck snapshot. They let a public clone reproduce the document/spec/deck consistency counts without distributing the underlying PowerPoint or paid research files.

Passing a local document or PowerPoint path to a verification script checks that actual artifact instead of the packaged snapshot.

## Important limitation

The checks establish computational reproducibility and internal consistency. They do not independently certify the accuracy, currency, or licensing of every third-party source. District-level enrolment remains an imputation because the AISHE register supplies institution counts, not district enrolment.

## Benchmark attribution

The return model uses Eternal's publicly stated ROCE of “north of 40%” as an external comparator; it is not presented as a Flipkart target. The basket model compares its implied mix with Swiggy's disclosed 30–40% non-grocery range; that range is likewise a cross-operator reference, not a Flipkart commitment or proof of feasibility. Runnable outputs label both boundaries explicitly.
