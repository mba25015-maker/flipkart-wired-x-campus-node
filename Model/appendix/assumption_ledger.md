# Appendix — assumption ledger

From `robustness.py`: twelve assumptions retired by source / derive / solve / neutralise, and what remains.

```
====================================================================================
              ASSUMPTION LEDGER - twelve down to what actually remains              
====================================================================================

1. RIDER WORKING DAYS  ->  SOLVED
   Rs26,500/mo / (21 orders/day x D) = Rs44 (Eternal disclosed)  ->  D = 28.7 days
   Same solve against Round 1's Rs42 constant                    ->  D = 30.0 days
   Both land inside a plausible gig roster. No longer assumed.

2. RUNNER ROSTER  ->  SOURCED
   8h day / 48h week under the Shops and Establishments Acts. Statutory, not assumed.

3. DROP TIME  ->  COLLAPSED to one parameter, and tested
     shelf:room ratio   Rs/order @n=10   vs standard zone
                 1.00              9.5               77%
                 0.50              8.3               80%
                 0.25              7.7               82%
                 0.10              7.3               83%
   The conclusion holds across the entire plausible range. Not decision-relevant.

4. IN-CLUSTER SPREAD  ->  NEUTRALISED
       spread km/drop   Rs/order @n=10
                 0.00              7.0
                 0.15              7.7
                 0.30              8.3
                 0.50              9.2
   A 0 to 0.5 km swing moves cost per order by under Rs1. Immaterial.

5. FOUR REACTIVATION ASSUMPTIONS  ->  NEUTRALISED IN ONE MOVE
   Wind-down saving over the break        Rs 1,305,499
   Our reactivation estimate              Rs   262,119
   Reactivation would have to be                 5.0x our estimate
                                          before winding down stops being worth doing.
   >>> Four unsourced inputs cannot change the decision. That is a stronger position
       than sourcing them badly, and it is the move Round 1 used on campus AOV.

6. THE E-CART  ->  PRICED, contradiction resolved
          capex    Rs/order   one campus gate, 14,000 orders/month, 60-mo life
        150,000        0.18
        250,000        0.30
        350,000        0.42
   Capex at which it would add Rs1/order:  Rs840,000
   >>> An e-cart would have to cost Rs8 lakh before it registered against a
       Rs17.61/order total. The no-vehicle-capex argument survives, now quantified
       rather than asserted, and the contradiction is closed.

====================================================================================
                        WHAT REMAINS ASSUMED, STATED PLAINLY                        
====================================================================================
  LT commercial electricity tariff    Rs9.50/kWh    splits JM's 'utilities and other' line; DATABASE PULL open (CMIE/Indiastat)
  Doorstep / in-cluster dwell         2.0 min       one of two unknowns in the trip identity; the other (batching) is SOLVED from it
  Residual campus demand share        8-15% range   reported as a range, and the site filter is derived FROM it rather than resting ON it
  Fixed-core share of store area      30-60% range  footprint lever reported across the full range, conservative case used
  Demand profile (4x peak, 4/8/6 hrs) stated on-slidesupplied by Round 1 metric 1 (PTDR) once live data exists

  Five, of which three are RANGES rather than point estimates, and one is a parameter
  our own Round 1 metric architecture was built to measure. Down from twelve.
```
