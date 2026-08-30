"""
THE ONLY FILE ALLOWED TO CONTAIN A CONTESTED POLICY CONSTANT.

WHY THIS FILE EXISTS. The package carried 322 passing assertions while three modules
operated under mutually contradictory policies:

  - working_capital.py rejected the 18-day COGS construct in its own docstring, and
    break_mode.py imported campus_model.NWC_DAYS = 18 and used exactly that construct.
    Gap at r=0.15: Rs100.16 lakh vs Rs76.46 lakh.
  - sla.py declared CAMPUSES = 3 and built its arrival rate on a per-gate basis;
    fleet_mix.py optimised the roster against one pooled queue of 1,400.
    Gap: Rs2.88 vs Rs3.36 per order.
  - sla.py priced the in-gate runner as a MARGINAL circuit-minute cost (Rs4.74/order);
    fleet_mix.py priced the same runner as a FIXED daily roster (Rs2.88/order).
    Gap: 64% on the same leg, and both numbers were on the deck.

Every one of those modules was internally consistent. audit.py compares a slide literal
to a computed value, so it can only detect drift between the deck and the model - never
disagreement between two modules. The defect class lives in the space audit.py cannot see.

THE RULE. A policy number that more than one module depends on is defined here and
imported everywhere else. It is never re-typed. A superseded value is not deprecated, it
is deleted - campus_model.NWC_DAYS = 18 was still importable and still tagged T1 twelve
days after it was superseded, and that is how it came back.

Enforcement lives in audit.py: recon() assertions compare two modules on the same
quantity, and they fail the run rather than the reader.
"""

# ---------------------------------------------------------------- WORKING CAPITAL
NWC_DAYS = 14.0
# T1  Eternal Q1FY27 call, 22 Jul 2026 ("down from 18"). Applied to NOV, NOT to COGS:
#     the disclosed figure is already NET, so a COGS multiplication double-counts the
#     netting. See working_capital.wc_nwc_on_nov(). 18 is SUPERSEDED - do not resurrect.
NWC_DAYS_TARGET = 12.0     # T1  same call, steady-state target
NWC_DAYS_R1     = 18.0     # T1  Jan 2026 call. Retained ONLY so working_capital.py can
                           #     show the rejected construct beside the adopted one.
                           #     No operating module may import this.

RESTART_CREDIT_STATE = "B"
# Which supplier-credit state the restart is underwritten on, after a 3.5-month stand-down.
#   "A"    credit intact - suppliers resume terms, the rebuild is payables-funded, WC ~ 0
#   "B30"  30 days to re-establish terms, partially self-funded
#   "B"    FULL credit reset - the whole 60-day cycle self-funded  <- ADOPTED, the downside
# break_mode.py used to reach past this and scale WC_ADOPTED directly, which silently picked
# the full-reset state without saying so. It now calls working_capital.reactivation_wc() with
# this constant, and the deck shows all three so the choice is visible rather than implied.

# ---------------------------------------------------------------- NODE TOPOLOGY
CAMPUSES_PER_NODE = 3
# D   No single campus reaches the 7,778-resident minimum cluster (index_model.CLUSTER),
#     so a node serves three campus gates. This binds BOTH the arrival rate in sla.py and
#     the roster optimisation in fleet_mix.py. It previously bound only the first.

GATE_TOPOLOGY = "per_gate"
# THE BASE CASE: runners are stationed per gate. 1,400/day across three gates is 467/day
# each, which optimal_roster solves to 2 runners at alpha=0.87 and Rs3.36/order.
#
# "pooled" - one dispatch pool serving all three gates - solves to 7 runners at
# alpha=1.00 and Rs2.88/order, but it assumes runners move between gates with no
# repositioning time, no access delay and no fragmented shift capacity. That is an
# operating claim we have not validated, so it is carried as a CONDITIONAL UPSIDE
# (fleet_mix.pooled_upside()) rather than as the plan. The pilot's cross-gate movement
# test is what would promote it.
#
# The base case costs 48 paise an order more than the pooled case and is defensible
# without a new assumption. That is the trade we are making deliberately.

# ---------------------------------------------------------------- LABOUR BASIS
LABOUR_BASIS = "roster"
# An employed runner is paid RUNNER_DAY whether volume arrives or not, so the in-gate
# leg is a FIXED daily cost divided by daily volume - not a marginal circuit-minute
# cost. sla.py priced it marginally because it predates the roster model in fleet_mix.py
# and was never migrated. This constant records which convention is the operating truth
# and audit.recon() asserts both modules obey it.
#
# The city leg is different in kind and stays volume-weighted: it is gig, priced per
# ACTIVE hour, bought per trip and divided by batch size, so it genuinely scales 1:1
# with volume and varies by demand band. Two legs, two cost structures, and treating
# them alike is what produced the error.

# ---------------------------------------------------------------- VOLUME
CLUSTER_VOLUME = 1400
# T1  Working throughput ceiling, inside JM Financial's observed 1,334-1,487 nine-quarter
#     range for Blinkit orders/day/dark-store (Exhibit 29). NOTE, and this is a live
#     weakness the reviewer was right to name: this is an OBSERVED CITY-FORMAT ceiling
#     that campus resident counts are then back-solved from, not a demand figure derived
#     forward from residents x penetration x frequency.

def gate_volume(cluster=None, topology=None):
    """Orders per day arriving at ONE optimisation unit, under the adopted topology."""
    cluster  = CLUSTER_VOLUME if cluster is None else cluster
    topology = GATE_TOPOLOGY if topology is None else topology
    return cluster if topology == "pooled" else cluster / CAMPUSES_PER_NODE

# ---------------------------------------------------------------- BUILD TARGETS
FINAL_DECK = "Flipkart_Minutes_WiRED_SemiFinal_FULL_light.pptx"
# verify_deck.py defaulted to Flipkart_Minutes_WiRED_SemiFinal_light.pptx - the
# superseded FOUR-SLIDE reference build. Run as the deck itself instructs a judge to run
# it, the verifier reported 51/93 and DECK VERIFICATION FAILED. It was never caught
# because the verifier was only ever invoked by hand with an explicit path. The default
# is now this constant, and run_all.py is the only supported entrypoint.
