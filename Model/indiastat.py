"""Public-safe IndiaStat/NSS summary layer.

The licensed source tables are not redistributed. This module loads aggregate statistics
derived from those tables so the audit can reproduce the reported screening conclusions.
See ``Model/data/README.md`` for provenance and limitations.
"""
import json
from pathlib import Path

_DATA = Path(__file__).resolve().parent / "data"
_S = json.loads((_DATA / "indiastat_summary.json").read_text(encoding="utf-8"))

dig_stats = _S["digital"]
gender = _S["gender"]
CV = _S["cv"]
rho_conc = _S["rho_concentration"]
p_conc = _S["p_concentration"]
rho_axis = _S["rho_axis_swap"]
overlap = _S["top5_overlap"]
top_mpce = _S["top5_mpce"]
top_nsdp = _S["top5_nsdp"]

if __name__ == "__main__":
    print(f"A. digital saturation  n={dig_stats['n']}  mean {dig_stats['mean']:.1f}%  "
          f"sd {dig_stats['sd']:.2f}  range {dig_stats['lo']:.1f}-{dig_stats['hi']:.1f}")
    print(f"B. gender gap  mean {gender['mean']:.1f}pp  median {gender['median']:.1f}pp  "
          f"n={gender['n']}")
    print("C. coefficient of variation across the states we choose between:")
    for key, value in sorted(CV.items(), key=lambda item: -item[1]):
        print(f"     {key:<34} {value:5.1f}%")
    print(f"D. concentration stability  rho={rho_conc:.3f}  p={p_conc:.1e}")
    print(f"E. axis swap  rho={rho_axis:.3f}  top-5 overlap {overlap}/5")

