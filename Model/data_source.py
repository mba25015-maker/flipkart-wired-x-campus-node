"""
ONE MODEL, TWO TREES.

The working folder holds the licensed source data under `Research Pulls/`. The public repository
deliberately does not redistribute it, and shipped pre-aggregated CSVs under `Model/data/`
instead. That was handled by keeping TWO VARIANTS of aishe_district.py, indiastat.py and
tariff.py - a public one and an original one - which is a fork of the model itself, and forks of
a model drift exactly like copies of a number do. `model_drift/original` vs `model_drift/public`
already showed measurable differences between the two.

So there is one module now, and it resolves its data at import:

    PUBLIC (Model/data/*.csv)  if present     -> what a clean clone runs
    SOURCE (Research Pulls/)   otherwise      -> what the working folder runs

Both produce the same published figures; the aggregates in Model/data are generated FROM the
licensed source, so the public path is a projection of the private one rather than a second
model. `Model/data/README.md` carries the provenance.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PUBLIC = os.path.join(HERE, "data")
SOURCE = os.path.join(ROOT, "Research Pulls")

def have_public(name=None):
    if not os.path.isdir(PUBLIC): return False
    return os.path.exists(os.path.join(PUBLIC, name)) if name else True

def have_source():
    return os.path.isdir(SOURCE)

def mode():
    return "public" if have_public("aishe_district_aggregates.csv") else "source"
