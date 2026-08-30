# Assortment model handoff

## Decision position

The optimiser changes what the 2,000 sq ft node holds locally by demand state. It does not
reduce the Minutes network assortment: the local range plus SDFC backfill remains 16,500 SKUs
in every state. It does not infer rent or footprint savings from SKU count.

The evidence classes are deliberately separated. **16,500** is the midpoint of Minutes' publicly
reported 15,000–18,000-SKU dark-store range. The **7,000 / 8,000 / 4,200 local caps, category
floors and priority weights are modelled operating-policy inputs**, not observed demand forecasts
or an empirically estimated optimal assortment. Pilot category data is what would replace them.

## Current model output

| Metric | Trough | Average | Peak | Exam | Break |
|---|---:|---:|---:|---:|---:|
| Local SKUs | 7,000 | 8,000 | 8,000 | 8,000 | 4,200 |
| SDFC tail | 9,500 | 8,500 | 8,500 | 8,500 | 12,300 |
| Network assortment | 16,500 | 16,500 | 16,500 | 16,500 | 16,500 |
| Cold SKUs | 1,800 | 2,300 | 2,500 | 2,200 | 500 |

Peak allocation favours chilled/RTE, frozen and snacks/caffeine. Exam allocation favours
snacks/caffeine and BPC/stationery/print. Break allocation retains every category but strongly
rationalises cold and perishable stock.

## Financial treatment

The financial evidence gate is CLOSED. Incremental opex saving and NWC release are both zero,
and no assortment value enters the dead-zone solver. The existing cold-power saving remains in
`break_mode.cfg_cold` and is not counted twice.

Promotion requires observed category velocity by state, waste/markdown, shelf life and case
packs, replenishment lead time, cold-zone kWh and stockout/fill-rate guardrails.

## Slide use

- Main fulfilment slide: show the category-by-state policy, not a new financial headline.
- Dead-zone slide: call the existing lever “assortment and cold-chain flex”; retain 48.6% until
  pilot evidence produces an incremental saving.
- Roadmap: add T-21 inventory freeze/drawdown, T-7 cold consolidation, T-14 restart ordering and
  T-5 SDFC first-fill.
