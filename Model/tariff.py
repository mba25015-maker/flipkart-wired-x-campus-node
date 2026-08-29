"""Public-safe electricity-tariff summary.

The paid IndiaStat cross-section is not redistributed. Only the aggregate statistics used
by the audit are published. The current BESCOM point remains a directly stated model input.
"""
import json
from pathlib import Path

_DATA = Path(__file__).resolve().parent / "data"
_S = json.loads((_DATA / "tariff_summary.json").read_text(encoding="utf-8"))

N_STATES_UTS = int(_S["n_states_uts"])
KA_2016 = float(_S["karnataka_2016_rs_per_kwh"])
BESCOM_2026 = float(_S["bescom_2026_rs_per_kwh"])
REBASE = float(_S["rebase_factor"])
CROSS_SECTION_CV = float(_S["cross_section_cv"])

if __name__ == "__main__":
    print("LT COMMERCIAL TARIFF — PUBLIC-SAFE SUMMARY")
    print(f"Karnataka 2016 total: Rs{KA_2016:.2f}/kWh")
    print(f"BESCOM FY2025-26 anchor: Rs{BESCOM_2026:.2f}/kWh")
    print(f"Re-basing factor: {REBASE:.3f}x")
    print(f"Cross-section: {N_STATES_UTS} states/UTs; CV {CROSS_SECTION_CV:.0%}")
    print("Licensed state-level source rows are intentionally not redistributed.")

