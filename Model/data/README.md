# Public-safe derived inputs

This directory contains the smallest data derivatives needed to run the public model. It deliberately excludes paid reports, licensed raw tables, and institution-level source workbooks.

| File | Contents | Transformation |
|---|---|---|
| `aishe_district_aggregates.csv` | State/district counts of colleges, urban colleges, universities, standalone institutions, and urban high-propensity standalone institutions | Grouped from the AISHE live institution register downloaded 28 August 2026; institution identifiers and institution-level rows removed |
| `aishe_summary.json` | National counts used by the audit | Aggregate totals derived from the same AISHE register |
| `hces_urban_mpce_2023_24.csv` | State/UT urban MPCE values without imputation | Filtered from the HCES 2023–24 government workbook to the state-level values used by the opportunity index |
| `indiastat_summary.json` | Digital-use, gender-gap, coefficient-of-variation, and robustness summaries | Aggregate statistics derived from licensed IndiaStat/NSS tables; raw rows excluded |
| `tariff_summary.json` | Cross-section size, Karnataka anchor, rebasing factor, and dispersion | Aggregate statistics derived from the licensed tariff cross-section; state-level paid rows excluded |

These derivatives reproduce the analytical outputs but cannot reconstruct the excluded source documents. Consult the source register for publisher, vintage, evidence tier, and exhibit/page citations.

