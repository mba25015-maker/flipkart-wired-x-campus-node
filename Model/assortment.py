"""Evidence-gated demand-state assortment optimiser for the campus node.

Allocates a state-specific local range, preserves the wider 16,500-SKU network promise through
SDFC backfill, and enforces category coverage and cold-capacity constraints. It never
infers rent savings from SKU count and never double-counts break_mode's cold-power saving.
"""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import params as P
import rent_lever as R
import sla as SL

@dataclass(frozen=True)
class Category:
    key: str
    label: str
    temperature: str
    max_skus: int
    term_floor: int
    break_floor: int

@dataclass(frozen=True)
class StatePolicy:
    key: str
    local_cap: int
    cold_cap: int
    priorities: dict

CATEGORIES = (
    Category("ambient", "Ambient staples", "ambient", 3200, 1800, 1800),
    Category("chilled", "Chilled / ready-to-eat", "chilled", 1200, 400, 250),
    Category("frozen", "Frozen snacks", "frozen", 1000, 300, 100),
    Category("perishables", "Fresh / perishables", "chilled", 1000, 450, 150),
    Category("snacks", "Snacks / caffeine", "ambient", 1600, 700, 700),
    Category("essentials", "BPC / stationery / print", "ambient", 1200, 400, 450),
    Category("long_tail", "Local long tail", "ambient", 1200, 350, 250),
)

# A-tier priorities: operating policy, not category-demand evidence and never revenue inputs.
POLICIES = (
    # local_cap and cold_cap are scenario policy inputs. They are not observed demand estimates;
    # the pilot evidence listed in ASSORTMENT_MODEL_HANDOFF.md is required to recalibrate them.
    StatePolicy("Trough", 7000, 1800,
        {"ambient":1.15,"chilled":0.85,"frozen":0.65,"perishables":0.75,
         "snacks":0.90,"essentials":0.80,"long_tail":0.45}),
    StatePolicy("Average", 8000, 2300,
        {"ambient":1.10,"chilled":1.00,"frozen":0.85,"perishables":0.90,
         "snacks":1.05,"essentials":0.85,"long_tail":0.60}),
    StatePolicy("Peak (4x)", 8000, 2500,
        {"ambient":0.95,"chilled":1.35,"frozen":1.25,"perishables":0.75,
         "snacks":1.55,"essentials":0.80,"long_tail":0.35}),
    StatePolicy("Exam night (6x)", 8000, 2200,
        {"ambient":0.95,"chilled":1.20,"frozen":0.95,"perishables":0.65,
         "snacks":1.60,"essentials":1.70,"long_tail":0.30}),
    StatePolicy("Break", 4200, 700,
        {"ambient":1.35,"chilled":0.55,"frozen":0.20,"perishables":0.25,
         "snacks":0.85,"essentials":0.75,"long_tail":0.15}),
)

TRANCHES = 6
COLD = {"chilled", "frozen"}

def _floor(cat, state):
    return cat.break_floor if state.key == "Break" else cat.term_floor

def optimise_state(state):
    """MILP allocation using diminishing-value SKU tranches and hard operating constraints."""
    floors = np.array([_floor(c, state) for c in CATEGORIES], dtype=int)
    if floors.sum() > state.local_cap:
        raise ValueError(f"{state.key}: category floors exceed local cap")

    sizes, utility, owner = [], [], []
    for i, cat in enumerate(CATEGORIES):
        room = cat.max_skus - floors[i]
        base, extra = divmod(room, TRANCHES)
        for t in range(TRANCHES):
            sizes.append(base + (1 if t < extra else 0))
            utility.append(state.priorities[cat.key] / (1.0 + 0.55*t))
            owner.append(i)
    sizes=np.array(sizes,float); utility=np.array(utility,float); owner=np.array(owner,int)
    remaining = int(state.local_cap - floors.sum())
    cold = np.array([1.0 if CATEGORIES[i].temperature in COLD else 0.0 for i in owner])
    cold_floor = sum(floors[i] for i,c in enumerate(CATEGORIES) if c.temperature in COLD)
    result = milp(c=-utility, integrality=np.ones(len(sizes)),
                  bounds=Bounds(np.zeros(len(sizes)), sizes),
                  constraints=[LinearConstraint(np.ones(len(sizes)), remaining, remaining),
                               LinearConstraint(cold, 0, state.cold_cap-cold_floor)],
                  options={"time_limit":5.0})
    if not result.success:
        raise RuntimeError(f"{state.key}: {result.message}")

    allocation=floors.copy()
    for q,i in zip(np.rint(result.x).astype(int),owner): allocation[i]+=q
    rows={c.key:int(allocation[i]) for i,c in enumerate(CATEGORIES)}
    local=sum(rows.values())
    cold_total=sum(rows[c.key] for c in CATEGORIES if c.temperature in COLD)
    return {"state":state.key,"allocation":rows,"local_skus":local,
            "sdfc_tail":max(0,int(R.SKU_BASE-local)),"network_skus":int(R.SKU_BASE),
            "cold_skus":cold_total,"local_cap":state.local_cap,"cold_cap":state.cold_cap,
            "objective":float(-result.fun)}

def plans():
    return {p.key:optimise_state(p) for p in POLICIES}

def evidence_open():
    total=(P.ASSORTMENT_WASTE_MARKDOWN_SAVING_MONTH+
           P.ASSORTMENT_HANDLING_SAVING_MONTH+P.ASSORTMENT_NWC_RELEASE)
    return bool(P.ASSORTMENT_FINANCIAL_ENABLED and total>0 and
                P.ASSORTMENT_WASTE_MARKDOWN_SAVING_MONTH>=0 and
                P.ASSORTMENT_HANDLING_SAVING_MONTH>=0 and P.ASSORTMENT_NWC_RELEASE>=0)

def financial_scenario():
    """Incremental values only. Promotion to the solver is deliberately a separate decision."""
    if not evidence_open():
        return {"status":"CLOSED","monthly_opex_saving":0.0,"nwc_release":0.0,
                "promoted_to_solver":False}
    return {"status":"OPEN",
            "monthly_opex_saving":float(P.ASSORTMENT_WASTE_MARKDOWN_SAVING_MONTH+
                                         P.ASSORTMENT_HANDLING_SAVING_MONTH),
            "nwc_release":float(P.ASSORTMENT_NWC_RELEASE),"promoted_to_solver":False}

def checks():
    ps=plans(); keys=[p.key for p in POLICIES]
    out=[(keys[:-1]==[n for n,_ in SL.demand_states()],"states reuse sla.demand_states"),
         (all(p["local_skus"]==p["local_cap"] for p in ps.values()),"local caps bind"),
         (all(p["cold_skus"]<=p["cold_cap"] for p in ps.values()),"cold caps hold"),
         (all(p["network_skus"]==int(R.SKU_BASE) for p in ps.values()),"wide network range preserved"),
         (all(all(p["allocation"][c.key]>0 for c in CATEGORIES) for p in ps.values()),"every category remains served"),
         (ps["Break"]["local_skus"]<ps["Average"]["local_skus"],"break range rationalises"),
         (ps["Break"]["cold_skus"]<ps["Average"]["cold_skus"],"break cold range rationalises"),
         (ps["Peak (4x)"]["allocation"]["snacks"]>=ps["Average"]["allocation"]["snacks"],"peak snacks do not fall"),
         (ps["Peak (4x)"]["allocation"]["frozen"]>=ps["Average"]["allocation"]["frozen"],"peak frozen does not fall"),
         (ps["Exam night (6x)"]["allocation"]["essentials"]>=ps["Average"]["allocation"]["essentials"],"exam essentials do not fall"),
         (ps["Exam night (6x)"]["allocation"]["snacks"]>=ps["Average"]["allocation"]["snacks"],"exam snacks do not fall"),
         (ps["Break"]["allocation"]["perishables"]<ps["Average"]["allocation"]["perishables"],"break perishables fall"),
         (financial_scenario()["monthly_opex_saving"]==0,"closed gate claims no saving"),
         (not financial_scenario()["promoted_to_solver"],"not silently promoted to solver")]
    return out

def report():
    ps=plans()
    print("ASSORTMENT OPTIMISER — WIDE NETWORK RANGE, STATE-SPECIFIC LOCAL RANGE")
    print(f"Financial gate: {financial_scenario()['status']} | incremental saving booked: Rs0")
    print(f"{'Category':<30}"+''.join(f"{p.key[:12]:>14}" for p in POLICIES))
    for c in CATEGORIES:
        print(f"{c.label:<30}"+''.join(f"{ps[p.key]['allocation'][c.key]:>14,}" for p in POLICIES))
    print(f"{'LOCAL SKUs':<30}"+''.join(f"{ps[p.key]['local_skus']:>14,}" for p in POLICIES))
    print(f"{'SDFC tail':<30}"+''.join(f"{ps[p.key]['sdfc_tail']:>14,}" for p in POLICIES))
    print(f"{'NETWORK assortment':<30}"+''.join(f"{ps[p.key]['network_skus']:>14,}" for p in POLICIES))
    bad=[name for ok,name in checks() if not ok]
    print(f"Guardrails: {len(checks())-len(bad)}/{len(checks())} pass")
    if bad: raise SystemExit("FAILED: "+"; ".join(bad))

if __name__=="__main__": report()
