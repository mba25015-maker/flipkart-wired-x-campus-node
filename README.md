# Flipkart WiRED X — Campus Node Model

Public-safe, reproducible analytical model supporting the Flipkart WiRED X semi-final submission. Paid analyst documents and licensed raw workbooks are intentionally excluded.

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
| `Model/roce.py` | Reproduces ROCE, DuPont, payback, IRR, and hurdle-AOV calculations |
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

