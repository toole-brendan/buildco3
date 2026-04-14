# MRO SAM Restructure: Expand Buckets & Add Cost-Element Estimation

**Date:** 2026-04-14
**Status:** Approved

## Summary

Restructure the MRO SAM sheet to:
1. Expand scope from buckets 2+4 to buckets 2+3+4+5 (exclude only 6 and 7)
2. Mirror the Newbuild SAM section layout (A through F)
3. Add an aggregate cost-element estimation section that applies OMN Ship Maintenance cost mix percentages to per-hull SDM totals — analogous to how Newbuild SAM applies P-5c percentages to net budget authority

## Motivation

The current MRO SAM only covers Scheduled Depot Maintenance (B2) and Modernization (B4), omitting Continuous/Emergent Maintenance (B3) and Major Life-Cycle Events (B5). Expanding to B2-B5 gives a more complete picture of outsourceable MRO work. The cost-element estimation for SDM provides directional insight into how maintenance dollars break down (labor vs. contract vs. materials) — the same analytical question Newbuild SAM answers with P-5c data.

## Data Findings

- **Buckets 2, 3, 4 have no P-5c/P-8a exhibit data** — ALT_VIEW rows are availability-type or program breakdowns, not cost-element exhibits
- **Bucket 5 has P-5c/P-8a only for CVN RCOH and LCAC SLEP** — both SAM-excluded
- **OMN Ship Maintenance (bucket 2)** has aggregate [SUB] cost categories covering 91.3% of the $15.7B parent:
  - Government Shipyard Labor (GS + Wage Board): 36.8%
  - Private Sector Contract (Ship + Equipment): 28.6%
  - Materials & Supply Chain (Navy + DLA): 9.6%
  - MSC Vessel Maintenance (MTA/ROH/Other): 10.1%
  - Weapons/Combat Systems Depot: 2.6%
  - Other: 3.7%
- **Buckets 3 and 4** have inconsistent/incomplete sub-breakdowns (B3 subs exceed parent at 270%, B4 only 20% coverage) — not suitable for cost-element estimation

## Design

### Constants / Configuration

Introduce `MRO_SAM_BKTS = ['2', '3', '4', '5']` to replace hardcoded `['2', '4']` throughout MRO SAM code. `MRO_BKTS` (all 2-7) remains unchanged for MRO TAM.

Bucket short labels for column headers:
- B2: "SDM" (Scheduled Depot Maintenance)
- B3: "Cont/Emerg" (Continuous / Emergent Maintenance)
- B4: "Mod" (Modernization)
- B5: "Major LC" (Major Life-Cycle Events)

Define aggregate SDM cost categories for section (D)/(E):
```python
SDM_COST_CATEGORIES = [
    'Government Shipyard Labor',
    'Private Sector Contract',
    'Materials & Supply Chain',
    'MSC Vessel Maintenance',
    'Weapons/Combat Systems Depot',
    'Other',
]
```

### pre_scan() Changes

1. **Expand MRO SAM filters**: Change `mro_sam_nz`, `mro_hull_sam_nz`, and `all_sam_mro_sorted` from summing B2+B4 to summing B2+B3+B4+B5.

2. **Collect aggregate SDM cost breakdown**: Scan OMN [SUB] rows in bucket 2 with no hull attribution. Group into the 6 cost categories above. Store as `sdm_cost_mix` in the returned dict — a dict mapping cost category name to $K value.

   Grouping rules for OMN B2 [SUB] no-hull rows:
   - **Government Shipyard Labor**: "Executive, General and Special Schedules" + "Wage Board"
   - **Private Sector Contract**: "Ship Maintenance By Contract" + "Equipment Maintenance By Contract"
   - **Materials & Supply Chain**: "Navy Managed Supplies & Materials" + "DLA Material Supply Chain - Weapon Systems"
   - **MSC Vessel Maintenance**: "MSC Mid-Term Availability (MTA)" + "MSC Regular Overhaul (ROH)" + "MSC Other Maintenance and Repair"
   - **Weapons/Combat Systems Depot**: All weapons-specific items (Tomahawk, Standard Missile, CIWS, NATO Seasparrow, RAM, Submarine Torpedo, Surface USW, SSTD, Submarine Acoustics)
   - **Other**: Everything else (Other Depot Maintenance Non-Fund, Other Intra-Government Purchases, Inactive Ship, Surface Ship Decommissioning, efficiencies, and any unmatched)

### Section (A): Bridge — MRO TAM → MRO SAM

Same structure as current. Changes:
- "Less: Non-outsourceable work types" label changes from "(Buckets 3, 5, 6, 7)" to **(Buckets 6, 7)**
- SAM result formula: `SUM(B2+B3+B4+B5)` for TAM categories, minus SAM-excluded vessel types for those same buckets
- Excluded vessel types unchanged: Submarines, Aircraft Carriers, UUVs

### Section (B): MRO SAM by Vessel Type

Expand columns from `VT | Svc | SDM | Mod | Total | %` to:

| Vessel Type | Svc | SDM ($K) | Cont/Emerg ($K) | Mod ($K) | Major LC ($K) | Total ($K) | % of SAM |
|---|---|---|---|---|---|---|---|

Each work-type column uses COUNTIFS on the corresponding bucket. Total = sum of 4 work-type columns. Percentage = row total / grand total.

### Section (C): MRO SAM by Hull Program

Expand columns from `Hull | VT | Svc | SDM | Mod | Total | %` to:

| Hull Program | Vessel Type | Svc | SDM ($K) | Cont/Emerg ($K) | Mod ($K) | Major LC ($K) | Total ($K) | % of Total |
|---|---|---|---|---|---|---|---|---|

Same COUNTIFS pattern, hull-level granularity.

### Section (D): Aggregate SDM Cost Breakdown

New section. Displays the OMN [SUB] aggregate cost categories from pre_scan as a reference table.

Purpose row: "Aggregate cost breakdown of OMN Ship Maintenance (Bucket 2) spending by cost type. Derived from OMN sub-component data — not hull-specific. Used in section (E) to estimate cost-element coverage per hull program."

| Cost Category | $K | % of SDM |
|---|---|---|
| Government Shipyard Labor | (from pre_scan) | 36.8% |
| Private Sector Contract | ... | 28.6% |
| Materials & Supply Chain | ... | 9.6% |
| MSC Vessel Maintenance | ... | 10.1% |
| Weapons/Combat Systems Depot | ... | 2.6% |
| Other | ... | 3.7% |
| **Total** | **sum** | **sum** |

Values are live references to named-range COUNTIFS from data sheet (OMN [SUB] B2 no-hull rows), or hardcoded from pre_scan if COUNTIFS can't isolate them. Percentages computed as category / grand total.

### Section (E): MRO SAM (SDM cost-element estimate)

The payoff section. Applies (D) percentages to per-hull SDM totals.

Purpose row: "Estimated SDM cost breakdown by hull program. Applies the aggregate OMN cost mix from section (D) to each hull's SDM funding. This is an approximation — actual cost mix varies by hull class. Analogous to Newbuild SAM section (E) which applies P-5c cost mix to net budget authority."

Layout (hull programs as columns, mirroring Newbuild SAM section E):

| Cost Category | Hull 1 | Hull 2 | ... | Total |
|---|---|---|---|---|
| SAM SDM Total ($K) | (ref to C) | (ref to C) | ... | sum |
| Government Shipyard Labor | =SDM × D% | ... | ... | sum |
| Private Sector Contract | =SDM × D% | ... | ... | sum |
| Materials & Supply Chain | =SDM × D% | ... | ... | sum |
| MSC Vessel Maintenance | =SDM × D% | ... | ... | sum |
| Weapons/Combat Systems Depot | =SDM × D% | ... | ... | sum |
| Other | =SDM × D% | ... | ... | sum |
| **Estimated SDM Total** | **sum** | **sum** | ... | **sum** |

Formula per cell: `= hull_SDM_ref × (category_$K / total_$K)` — references section (D) percentage row and section (C) hull SDM column.

Hull column ordering: same as section (C), USN/MSC first then USCG, descending by SDM value. Service header row above hull names (same pattern as Newbuild SAM).

### Section (F): Mekko — Work Type by Hull

Expands from 2 rows (SDM, Mod) to 4 rows:

| Work Type | Hull 1 | Hull 2 | ... | Total |
|---|---|---|---|---|
| SDM | % | % | ... | weighted % |
| Cont/Emerg | % | % | ... | weighted % |
| Mod | % | % | ... | weighted % |
| Major LC | % | % | ... | weighted % |
| **Total ($K)** | **sum** | **sum** | ... | **sum** |

Each cell = COUNTIFS for that hull × bucket / hull total. Total column = weighted average across hulls.

### Validation Sheet Updates

1. **MRO SAM definition**: Update from "scheduled depot maintenance and modernization/alteration installation" to "scheduled depot maintenance, continuous/emergent maintenance, modernization/alteration installation, and major life-cycle events"
2. **Outsourceable Work Types table**: Add Bucket 3 ("Continuous / Emergent Maintenance") and Bucket 5 ("Major Life-Cycle Events / RCOH") rows
3. **Excluded note**: Change to "Excluded: Sustainment Engineering (6), Availability Support (7)"

### Files Changed

| File | Change |
|---|---|
| `build/build_from_data.py` | Add `MRO_SAM_BKTS`, update `pre_scan()`, rewrite `create_mro_sam()` |
| `build/validation_sheet.py` | Update MRO SAM definition, outsourceable work types, exclusion note |

### What Does NOT Change

- MRO TAM: still uses all MRO buckets (2-7), unchanged
- Newbuild TAM/SAM: unchanged
- Total Funding sheet: unchanged
- `MRO_BKTS` constant: stays `['2','3','4','5','6','7']`
- Data sheet (J Book Items Cons.): no changes
- ALT_VIEW scanning in pre_scan: stays bucket-1 only (no MRO P-5c/P-8a to scan for)
