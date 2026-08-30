"""
GENERATE THE PUBLIC-SAFE DATA THE REPOSITORY SHIPS.

The AISHE institution register is licensed source data and is deliberately not redistributed.
The repository therefore shipped pre-aggregated CSVs - and, to read them, a SECOND VARIANT of
aishe_district.py. A fork of the model is worse than a duplicated constant: `model_drift/original`
against `model_drift/public` already showed the two producing different output.

So there is one module, and it always reads Model/data. This script regenerates Model/data from
the licensed source when the source is present, and does nothing when it is not. The public data
is a projection of the private data, never a second model.

Run automatically at release time; skipped silently on a clean clone that has no source.
"""
import json, os, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC  = os.path.join(ROOT, "Research Pulls", "AISHE")
OUT  = os.path.join(HERE, "data")

# Imported, never re-typed: this set defines the cohort and a second copy of it would be exactly
# the duplicate-constant defect this package has met four times.
from aishe_district import HIGH_PROPENSITY_STA

def _load(fname, sheet):
    d = pd.read_excel(os.path.join(SRC, fname), sheet_name=sheet, header=2)
    d = d[d["Aishe Code"].notna() & d["Aishe Code"].astype(str).str.match(r"^[CUS]-")]
    d["District"] = d["District"].astype(str).str.strip()
    d["State"] = d["State"].astype(str).str.strip()
    return d

def build():
    if not os.path.isdir(SRC):
        print("  no licensed source present — Model/data left as shipped"); return None
    COL = _load("College-ALL COLLEGE.xlsx", "College-")
    UNI = _load("University-ALL UNIVERSITIES.xlsx", "University-")
    STA = _load("Standalone-ALL STANDALONE.xlsx", "Standalone-")
    c = COL.groupby(["State","District"]).agg(
            colleges=("Aishe Code","size"),
            urban_colleges=("Location", lambda s: int((s=="Urban").sum())))
    u = UNI.groupby(["State","District"]).agg(universities=("Aishe Code","size"))
    s = STA.groupby(["State","District"]).agg(standalone=("Aishe Code","size"))
    hp = (STA[(STA["Location"]=="Urban") & (STA["Standalone Type"].isin(HIGH_PROPENSITY_STA))]
          .groupby(["State","District"]).size().rename("urb_hp_standalone"))
    t = c.join(u,how="outer").join(s,how="outer").join(hp,how="outer").fillna(0).astype(int).reset_index()
    t["hei"] = t.colleges + t.universities + t.standalone
    t["urban_share"] = t.apply(lambda r: (r.urban_colleges/r.colleges) if r.colleges else 0.0, axis=1)
    # ENTITY SAFETY. One register row carries no district. _load() does .astype(str), so a missing
    # value arrives here as the literal STRING "nan" - which passes notna() and passes a
    # non-empty test, and only becomes NA again on the CSV round-trip. It is not a district and
    # must not sit in the screen's universe.
    _d = t["District"].astype(str).str.strip()
    t = t[~_d.isin(["", "nan", "NaN", "None", "NA", "N/A"])]
    t = t.sort_values("urban_colleges", ascending=False).reset_index(drop=True)
    os.makedirs(OUT, exist_ok=True)
    t.to_csv(os.path.join(OUT,"aishe_district_aggregates.csv"), index=False)
    summary = {"as_of":"2026-08-28",
               "n_colleges":int(len(COL)), "n_universities":int(len(UNI)),
               "n_standalone":int(len(STA)),
               # PAIRS, NOT NAMES. This was COL["District"].nunique() - distinct district NAMES,
               # 760. Bilaspur, Hamirpur and Pratapgarh each exist in two states, and the screen
               # operates on (State, District) pairs, so the numerator counted pairs while the
               # denominator counted names. Two entity definitions inside one ratio.
               "n_districts":int(len(t)),
               "n_districts_with_colleges":int((t.colleges > 0).sum()),
               "n_district_names":int(t["District"].nunique()),
               "urban_colleges":int((COL["Location"]=="Urban").sum()),
               "rural_colleges":int((COL["Location"]=="Rural").sum()),
               "urban_high_propensity_standalone":int(len(
                   STA[(STA["Location"]=="Urban") & (STA["Standalone Type"].isin(HIGH_PROPENSITY_STA))])),
               "source_note":("Derived district aggregates from the AISHE live institution register; "
                              "no institution-level records included.")}
    json.dump(summary, open(os.path.join(OUT,"aishe_summary.json"),"w"), indent=2)
    print(f"  wrote Model/data: {len(t)} districts, {summary['n_colleges']:,} colleges")
    return t

def build_cache():
    """Dump the PARSED tables the licensed readers produce, so a clean clone runs the same code.
    Parsed derivatives only - no row-level source is redistributed."""
    if not os.path.isdir(os.path.join(ROOT, "Research Pulls")):
        print("  no licensed source — Model/data/cache left as shipped"); return
    cache = os.path.join(OUT, "cache"); os.makedirs(cache, exist_ok=True)
    n = 0
    import indiastat as S, tariff as TF
    for f in ("person statewise.xls", "15-29. 3.xls"):
        try:
            S.rd(f).to_csv(os.path.join(cache, f.replace(" ","_").replace(".","_")+".csv"), index=False); n += 1
        except Exception as e: print("   skip", f, e)
    for fn in TF.BRACKETS:
        try:
            d = TF.load_bracket(fn)
            d.to_csv(os.path.join(cache, "tariff_"+fn.replace(".","_")+".csv"), index=False); n += 1
        except Exception as e: print("   skip", fn, e)
    print(f"  wrote Model/data/cache: {n} parsed tables")

def build_derived():
    """The other three modules that read licensed source: their PUBLISHED derivatives only.
    Same principle - one code path, and the public file is generated from the private source."""
    import csv as _csv
    os.makedirs(OUT, exist_ok=True)
    wrote = []
    try:
        import index_model as I
        with open(os.path.join(OUT, "hces_urban_mpce_2023_24.csv"), "w", newline="", encoding="utf-8") as fh:
            w = _csv.writer(fh); w.writerow(["State", "MPCE_urban_2023_24"])
            for k, v in sorted(I.MPCE.items()):
                if v == v: w.writerow([k, v])
        wrote.append("hces_urban_mpce_2023_24.csv")
    except Exception as e: print("   skip HCES:", e)
    try:
        import indiastat as S
        json.dump({"digital_use_urban_15_24": {k: (round(v, 4) if isinstance(v, float) else v)
                                               for k, v in S.dig_stats.items()},
                   "source_note": "Derived state-level statistics from Indiastat tables; no row-level data."},
                  open(os.path.join(OUT, "indiastat_summary.json"), "w"), indent=2)
        wrote.append("indiastat_summary.json")
    except Exception as e: print("   skip indiastat:", e)
    try:
        import tariff as TF
        json.dump({"lt_commercial_rate_assumed": TF.ASSUMED if hasattr(TF, "ASSUMED") else None,
                   "source_note": "Derived tariff summary; no source tables redistributed."},
                  open(os.path.join(OUT, "tariff_summary.json"), "w"), indent=2)
        wrote.append("tariff_summary.json")
    except Exception as e: print("   skip tariff:", e)
    if wrote: print("  wrote Model/data derivatives:", ", ".join(wrote))

PROVENANCE = """# Public-safe derived inputs

Generated by `Model/make_public_data.py`. This directory holds the smallest derivatives needed to
run the model without the licensed corpus. It deliberately excludes paid reports, licensed raw
tables and institution-level source workbooks.

| File | Contents | Transformation |
|---|---|---|
| `aishe_district_aggregates.csv` | One row per **(State, District) pair**: colleges, urban colleges, universities, standalone institutions, urban high-propensity standalone institutions | Grouped from the AISHE live institution register, downloaded 28 August 2026. Institution identifiers and institution-level rows removed. Rows with no district are dropped. |
| `aishe_summary.json` | National counts used by the audit | Aggregate totals from the same register |
| `hces_urban_mpce_2023_24.csv` | State/UT urban MPCE, without imputation | Filtered from the HCES 2023-24 government workbook |
| `indiastat_summary.json` | Digital-use, gender-gap and dispersion summaries | Aggregate statistics from licensed IndiaStat/NSS tables; raw rows excluded |
| `tariff_summary.json` | Cross-section size, Karnataka anchor, rebasing factor | Aggregate statistics from the licensed tariff cross-section; paid state-level rows excluded |
| `cache/*.csv` | The **parsed** form of the licensed tables the model reads | Parsed output only. It exists so one module serves both trees, instead of the repository carrying separate public variants that drift apart. |

## On the district count

The screen operates on **(State, District) pairs**, not district names. Bilaspur, Hamirpur and
Pratapgarh each exist in two states, so a name-based count understates the universe by three and
puts the screen's numerator and denominator on different definitions. The published denominator
is the pair count.

These derivatives reproduce the analytical outputs and cannot reconstruct the excluded sources.
The source register carries publisher, vintage, evidence tier and exhibit citations.
"""

def write_provenance():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(PROVENANCE)
    print("  wrote Model/data/README.md (provenance)")

if __name__ == "__main__":
    build()
    build_cache()
    build_derived()
    write_provenance()
