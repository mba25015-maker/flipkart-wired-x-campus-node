"""
EVERY COUNT THE DECK STATES ABOUT ITSELF - AND WHETHER IT ACTUALLY PASSED.

The first version of this file held AUDIT_COUNT = 352 and DECK_CHECK_COUNT = 116 as declared
constants, and the self-check asserted that the number of checks DEFINED matched. That is not
the same thing as the number that PASSED, which is how the deck was able to print "116 / 116"
on a build whose verifier was actually returning 115/116. A tile that reports a pass rate must
be sourced from a run, not from a constant.

So the constants below now declare only how many checks EXIST - which is still worth pinning,
because it is what stops a check being added without the slide noticing. The pass counts come
from _verification.json, which run_all.py writes and nothing else does.

    tile("audit")  ->  "336 checks defined"   before a run, or after a failing one
                   ->  "336 / 336"            only when a run actually passed

The release sequence is build -> verify -> stamp -> verify-exact-final (`release.py`). The
deck can only claim a pass after one happened, and the final file is re-verified after the
claim is stamped into it.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "_verification.json")

AUDIT_COUNT = 366   # audit.py       - checks DEFINED, not passed
DOCS_COUNT  = 31    # verify_docs.py
SPEC_COUNT  = 79    # verify_spec.py
ARTF_COUNT  = 23    # verify_artifacts.py - workbook, notebooks, manifest, public data

from deck_checks import DECK_CHECK_COUNT   # verify_deck.py

DEFINED = {"audit": AUDIT_COUNT, "docs": DOCS_COUNT, "spec": SPEC_COUNT,
           "deck": DECK_CHECK_COUNT, "artefacts": ARTF_COUNT}

def results():
    """What the last run_all.py actually found, or None if there has not been one."""
    try:
        with open(RESULTS, encoding="utf-8") as fh: return json.load(fh)
    except Exception:
        return None

def verified(name):
    """True only if a recorded run passed every check of this layer."""
    r = results()
    if not r or name not in r: return False
    return r[name]["passed"] == r[name]["total"] == DEFINED[name]

def tile(name):
    """The string the deck is allowed to print about itself."""
    n = DEFINED[name]
    return f"{n} / {n}" if verified(name) else f"{n} checks defined"

def all_verified():
    return all(verified(k) for k in DEFINED)
