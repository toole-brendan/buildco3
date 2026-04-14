# Fold P-8a System Detail into Newbuild SAM Section (D)

**Date:** 2026-04-14
**Status:** Approved

## Summary

Integrate the P-8a system-level detail (formerly Cost Detail Section B) directly into the Newbuild SAM sheet's Section (D) as indented rows under each P-5c cost category. Delete the entire "FY26 Newbuild SAM Cost Detail" sheet.

## Section (D) Expansion

### Current structure

Section (D) "P-5c Gross Cost Category Breakdown by Hull" has one row per P-5c cost category with hull programs as columns, followed by a Gross Total row and a percentage sub-table.

### New structure

After each P-5c cost category row, insert indented P-8a system rows showing the individual GFE systems that compose that category:

```
Cost Category              | DDG-51 | FFG-62 | LPD-17 | ... | Total
Electronics                | 1,234  |   567  |   ...  | ... |  ...
    SPY-6(V)6 Radar        |   800  |    -   |   ...  | ... |  800
    AEGIS MK 7 System      |   400  |   200  |   ...  | ... |  600
HM&E                       |   ...  |   ...  |   ...  | ... |  ...
    LM2500 Gas Turbine     |   ...  |   ...  |   ...  | ... |  ...
Ordnance                   |   ...  |   ...  |   ...  | ... |  ...
    MK 45 Gun System       |   ...  |   ...  |   ...  | ... |  ...
Gross Total ($K)           |   ...  |   ...  |   ...  | ... |  ...
```

### Rules

- **P-5c category rows**: unchanged (same formulas, `F_DATA` font, `altview_inner` with `JB_EX,"P-5c"`)
- **P-8a system rows**: indented 4 spaces in column 1, green font (`F_GREEN`), formulas use `altview_inner` with `JB_EX,"P-8a"` and `JB_CE` for the specific system name
- **Sorting**: P-8a systems within each cost category sorted by total value descending across all hulls
- **Scope**: only P-8a systems on `p5c_funded` hulls (matching section D's column scope)
- **Gross Total row**: sums only P-5c category rows (tracked by row number), not P-8a detail rows. P-8a is a decomposition of P-5c, not additive.
- **Percentage sub-table**: unchanged, references P-5c category rows only
- **Total column**: each P-8a row sums across hull columns, same as P-5c rows
- **Every P-8a system** included (no cap or minimum threshold)

### Data source

`d['p8a_hull']` dict keyed by `(hull, cost_category, cost_element)` — already loaded by the data pipeline. Filter to entries where `hull` is in `p5c_funded` set and `cost_category` matches the current P-5c category.

### Formula pattern

P-8a cell formula (per system per hull):
```
=altview_inner('JB_B,1', 'JB_EX,"P-8a"', 'JB_CC,"{category}"', 'JB_H,"{hull}"', 'JB_CE,"{system}"')
```

## Deletions

### Cost Detail sheet

Remove entirely:
- `create_newbuild_cost_detail()` function (~140 lines) from `build_from_data.py`
- Call to `create_newbuild_cost_detail()` in the main build loop
- `cost_detail_name` variable and all references (tab colors, `generated` list, `fy_sheets` list)
- `fy26_detail_info` variable
- Cost Detail sticky-note annotation (the "About This Table" note on section B)

### Validation sheet

- Remove the three "Cost Detail (A/B/C)" rows from the "Newbuild SAM Cost Category Detail" section
- Update "SAM (D)" description to note it now includes P-8a system-level detail indented under each cost category
- Simplify the FY2027 note: remove "or Cost Detail sheet" since that sheet no longer exists

### Annotations

- Keep the existing Newbuild SAM section (D) sticky note about "P-5c Gross vs Net" (still relevant)
- Delete the Cost Detail section (B) sticky note (sheet no longer exists)

## Sections NOT changed

- Newbuild SAM sections A, B, C, (C->D) bridge, E, F: untouched
- FY27 Newbuild SAM: untouched (no P-5c/P-8a data, stops before section D)
- All other sheets: untouched
