# Newbuild SAM Cost Category Restructuring — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add P-5c cost category breakdown (Basic Construction, Electronics, Ordnance, etc.) to the FY26 Newbuild SAM sheet and create a supplemental sheet with gross cost detail and P-8a system-level data, enabling component-level market sizing for new construction.

**Architecture:** Modify `build/build_workbook.py` to: (1) populate two derived columns in Sheet 1 (Exhibit Level, Cost Category) by parsing ALT_VIEW title strings, (2) extend `read_data()` to pre-scan P-5c/P-8a data for layout decisions, (3) add sections (D) and (E) to `create_newbuild_sam()` for FY26 only, and (4) create a new `create_newbuild_cost_detail()` sheet builder. All formulas use SUMIFS referencing the new derived columns via named ranges.

**Tech Stack:** Python 3 + openpyxl. Single file: `build/build_workbook.py`.

**Key constraint:** FY2026 only. P-5c/P-8a ALT_VIEW rows have FY2026 Request/Total populated but zero for FY2027/DAA Enacted. FY27 sheets are untouched.

---

## File Structure

All changes are in one file:

- Modify: `build/build_workbook.py` (the entire build script)
  - New constants: `P5C_COST_CATEGORIES`, `P8A_COST_CATEGORIES`
  - New functions: `parse_exhibit_level()`, `parse_cost_category()`, `populate_derived_columns()`, `make_altview_cascade()`, `create_newbuild_cost_detail()`
  - Modified functions: `read_data()`, `create_newbuild_sam()`, `create_named_ranges()`, `main()`

New columns in output workbook Sheet 1 (not in source):
- Col 38 (AL): `Exhibit Level` — values: `P-5c`, `P-8a`, `P-35`, or blank
- Col 39 (AM): `Cost Category` — values: `Basic Construction`, `Electronics`, etc., or blank

---

### Task 1: Add title parsing functions and constants

**Files:**
- Modify: `build/build_workbook.py:66-84` (after existing taxonomy constants)

- [ ] **Step 1: Add P-5c/P-8a constants after line 84 (after `MRO_BKTS`)**

```python
# ── P-5c / P-8a cost breakdown ───────────────────────────────

P5C_COST_CATEGORIES = [
    'Plan Costs',
    'Basic Construction',
    'Change Orders',
    'Electronics',
    'Propulsion Equipment',
    'Hull, Mechanical, and Electrical',
    'Ordnance',
    'Other Cost',
    'Technology Insertion',
]
P5C_VALID = set(P5C_COST_CATEGORIES)

P8A_COST_CATEGORIES = {'Electronics', 'Hull, Mechanical, and Electrical', 'Ordnance'}
```

- [ ] **Step 2: Add title parsing functions after the new constants**

```python
def parse_exhibit_level(title):
    """Extract exhibit level from an ALT_VIEW title string.
    Returns 'P-5c', 'P-8a', 'P-35', or None."""
    if not title:
        return None
    t = str(title).strip()
    if ' - P-5c - ' in t:
        return 'P-5c'
    if ' - P-8a ' in t:
        # Validate it has a known category (filters out narrative text fragments)
        for cat in P8A_COST_CATEGORIES:
            if f' - P-8a {cat} - ' in t:
                return 'P-8a'
        return None
    if ' - P-35 ' in t:
        return 'P-35'
    return None


def parse_cost_category(title, exhibit_level):
    """Extract P-5c cost category from an ALT_VIEW title string.
    For P-5c rows: the category after ' - P-5c - '.
    For P-8a/P-35 rows: the P-5c parent category (Electronics, HM&E, Ordnance).
    Returns a category string or None."""
    if not title or not exhibit_level:
        return None
    t = str(title).strip()

    if exhibit_level == 'P-5c':
        cat = t.split(' - P-5c - ', 1)[1].strip()
        return cat if cat in P5C_VALID else None

    if exhibit_level == 'P-8a':
        for cat in P8A_COST_CATEGORIES:
            if f' - P-8a {cat} - ' in t:
                return cat
        return None

    if exhibit_level == 'P-35':
        # P-35 category inferred from title — system names map to P-8a categories.
        # Heuristic: check if title contains category keywords from P-8a.
        # Most P-35 titles follow pattern: "{Program} - P-35 {SystemName} - {Suffix}"
        # The system's category must be looked up from preceding P-8a rows.
        # For now, leave P-35 Cost Category blank (not needed for SAM formulas).
        return None

    return None
```

- [ ] **Step 3: Verify parsing works**

Run:
```bash
python3 -c "
import sys; sys.path.insert(0, 'build')
from build_workbook import parse_exhibit_level, parse_cost_category
tests = [
    ('DDG-51 - P-5c - Electronics', 'P-5c', 'Electronics'),
    ('DDG-51 - P-8a Ordnance - AN/SPY-6(V)1 (AMDR) 2', 'P-8a', 'Ordnance'),
    ('DDG-51 - P-35 AEGIS WEAPON SYSTEM - Major Hardware', 'P-35', None),
    ('DDG 1000', None, None),
    ('Carrier Replacement Program - P-8a  - Increase of \$', None, None),
]
for title, exp_ex, exp_cc in tests:
    ex = parse_exhibit_level(title)
    cc = parse_cost_category(title, ex)
    ok = '  OK' if ex == exp_ex and cc == exp_cc else ' FAIL'
    print(f'{ok}: \"{title[:60]}\" -> ex={ex}, cc={cc}')
"
```
Expected: all OK.

---

### Task 2: Column population and named ranges

**Files:**
- Modify: `build/build_workbook.py:956-971` (named ranges function)
- Add new function after `create_competitive_dynamics` (~line 953)

- [ ] **Step 1: Add `populate_derived_columns()` function**

Add after `create_competitive_dynamics()` (before the named ranges section):

```python
# ── Derived columns ──────────────────────────────────────────

def populate_derived_columns(wb):
    """Populate Exhibit Level (col 38) and Cost Category (col 39) for ALT_VIEW rows.
    These columns exist only in the output, not the source."""
    ws = wb['J Book Items Cons.']
    # Headers
    ws.cell(row=4, column=38, value='Exhibit Level')
    ws.cell(row=4, column=39, value='Cost Category')
    for c in (38, 39):
        ws.cell(row=4, column=c).font = Font(name='Arial', size=8, bold=True)

    count = 0
    for row in range(5, ws.max_row + 1):
        rt = ws.cell(row, 22).value
        if rt != '[ALT_VIEW]':
            continue
        title = ws.cell(row, 4).value
        ex = parse_exhibit_level(title)
        if ex:
            ws.cell(row, 38, value=ex)
            cc = parse_cost_category(title, ex)
            if cc:
                ws.cell(row, 39, value=cc)
            count += 1
    print(f'  Derived columns: populated {count} ALT_VIEW rows')
```

- [ ] **Step 2: Add named ranges for the new columns + Cost Element**

Modify `create_named_ranges()` (line 958). Add to the `shared` list:

```python
    shared = [
        ('JB_A', 'A'), ('JB_B', 'E'), ('JB_F', 'F'),
        ('JB_S', 'V'), ('JB_U', 'X'), ('JB_V', 'Y'), ('JB_W', 'Z'),
        ('JB_CE', 'AH'),   # Cost Element (existing col 34)
        ('JB_EX', 'AL'),   # Exhibit Level (new col 38)
        ('JB_CC', 'AM'),   # Cost Category (new col 39)
    ]
```

- [ ] **Step 3: Wire `populate_derived_columns()` into `main()`**

In `main()`, after `create_named_ranges(wb)` (line 991), add:

```python
    create_named_ranges(wb)

    # Populate derived columns in Sheet 1
    print('Populating derived columns...')
    populate_derived_columns(wb)
```

- [ ] **Step 4: Build and verify columns are populated**

Run:
```bash
python3 build/build_workbook.py
```

Then verify:
```bash
python3 -c "
import openpyxl
# Use the output file path printed by the build script
wb = openpyxl.load_workbook('output/08APR2028_Newbuild_and_MRO_Spend_v3.17.xlsx', data_only=True)
ws = wb['J Book Items Cons.']
print(f'Col 38 header: {ws.cell(4,38).value}')
print(f'Col 39 header: {ws.cell(4,39).value}')
# Spot check P-5c row
print(f'Row 94: ex={ws.cell(94,38).value}, cc={ws.cell(94,39).value}')
# Spot check P-8a row
print(f'Row 1210: ex={ws.cell(1210,38).value}, cc={ws.cell(1210,39).value}')
# Count populated
ex_count = sum(1 for r in range(5, ws.max_row+1) if ws.cell(r,38).value)
cc_count = sum(1 for r in range(5, ws.max_row+1) if ws.cell(r,39).value)
print(f'Exhibit Level populated: {ex_count} rows')
print(f'Cost Category populated: {cc_count} rows')
"
```

Expected: ~1420 Exhibit Level rows (172 P-5c + 410 P-8a + 833 P-35), ~720 Cost Category rows (172 P-5c valid + ~410 P-8a + 0 P-35).

- [ ] **Step 5: Commit**

```bash
git add build/build_workbook.py
git commit -m "feat: add derived columns (Exhibit Level, Cost Category) and title parsing"
```

---

### Task 3: Extend `read_data()` for P-5c and P-8a pre-scan

**Files:**
- Modify: `build/build_workbook.py:266-349` (`read_data` function)

The pre-scan determines which vessel types and cost categories have data, so the build script knows which rows/columns to generate in the output sheets.

- [ ] **Step 1: Add P-5c/P-8a accumulation to `read_data()`**

After the existing loop (line 318, after `wb.close()`), add a second pass that scans ALT_VIEW rows. Or integrate into the existing loop. I recommend integrating — add to the existing `for row in ws.iter_rows(...)` loop, before the `if not additive(rt): continue` filter:

After line 305 (`if bs not in ('1',...): continue`), the existing code processes additive rows. BEFORE the `if not additive(rt): continue` on line 301, add the ALT_VIEW scan:

Replace lines 300-318 with:

```python
        rt = row[21].value
        bk = row[4].value

        # ── ALT_VIEW scan (P-5c / P-8a for cost category breakdown) ──
        if str(rt).strip() == '[ALT_VIEW]' and bk is not None and str(bk).strip() == '1':
            title = str(row[3].value).strip() if row[3].value else ''
            ex = parse_exhibit_level(title)
            cc = parse_cost_category(title, ex)
            if ex and cc and cat in TAM_CATEGORIES and vt and vt not in SAM_EXCLUDED_TYPES:
                val = read_val(row)
                if ex == 'P-5c' and cc in P5C_VALID:
                    p5c_data[(vt, cc)] += val
                    p5c_types.add(vt)
                elif ex == 'P-8a':
                    ce = str(row[33].value).strip() if row[33].value else ''
                    if ce:
                        p8a_data[(vt, cc, ce)] += val
                        p8a_types.add(vt)

        if not additive(rt): continue
        # ... existing additive-row code continues unchanged ...
```

Also add the accumulator initialization before the loop (after line 288):

```python
    p5c_data = defaultdict(float)   # (vessel_type, cost_category) -> $K
    p5c_types = set()
    p8a_data = defaultdict(float)   # (vessel_type, cost_category, system_name) -> $K
    p8a_types = set()
```

- [ ] **Step 2: Add P-5c/P-8a results to the return dict**

Add to the return dict (line 335):

```python
        # P-5c / P-8a breakdown data
        'p5c_data': dict(p5c_data),
        'p5c_types': sorted_svc([t for t in p5c_types if p5c_data.get((t, 'Basic Construction'), 0) > 0
                                  or any(p5c_data.get((t, c), 0) > 0 for c in P5C_VALID)],
                                 nb),
        'p8a_data': dict(p8a_data),
        'p8a_types': sorted_svc(list(p8a_types), nb),
```

- [ ] **Step 3: Build and verify pre-scan data**

Run:
```bash
python3 -c "
import sys; sys.path.insert(0, 'build')
from build_workbook import read_data
d = read_data('output/08APR2028_Newbuild_and_MRO_Spend_v2.3.xlsx', [17, 13, 11])
print('P-5c vessel types:', d['p5c_types'])
print('P-8a vessel types:', d['p8a_types'])
print('P-5c data sample (Surface Combatants):')
for cat in ['Basic Construction', 'Electronics', 'Ordnance']:
    print(f'  {cat}: {d[\"p5c_data\"].get((\"Surface Combatants\", cat), 0):,.0f}')
print(f'P-8a entries: {len(d[\"p8a_data\"])}')
"
```

Expected: Surface Combatants has large values for Basic Construction, Electronics, Ordnance.

- [ ] **Step 4: Commit**

```bash
git add build/build_workbook.py
git commit -m "feat: extend read_data with P-5c/P-8a pre-scan for cost category breakdown"
```

---

### Task 4: Add `make_altview_cascade()` helper

**Files:**
- Modify: `build/build_workbook.py:131-159` (after existing `make_cascade`)

- [ ] **Step 1: Add the ALT_VIEW cascade function after `make_cascade`**

```python
def make_altview_cascade(value_ranges):
    """
    Build cf / cf_inner for [ALT_VIEW] rows only.
    Same cascade logic as make_cascade but matches JB_S="[ALT_VIEW]" instead
    of "" and "[PARENT]".  Simpler: only one row-type term, not two.
    """
    def cf(*conditions):
        cond = (',' + ','.join(conditions)) if conditions else ''
        t = []
        for i, vr in enumerate(value_ranges):
            prior = ''.join(f',{value_ranges[j]},""' for j in range(i))
            check = f',{vr},"<>"' if i < len(value_ranges) - 1 else ''
            t.append(f'SUMIFS({vr},JB_S,"[ALT_VIEW]"{cond}{prior}{check})')
        return '=' + '+'.join(t)

    def cf_inner(*conditions):
        return cf(*conditions)[1:]

    return cf, cf_inner
```

- [ ] **Step 2: Commit**

```bash
git add build/build_workbook.py
git commit -m "feat: add make_altview_cascade for ALT_VIEW SUMIFS formulas"
```

---

### Task 5: Add sections (D) and (E) to `create_newbuild_sam()`

**Files:**
- Modify: `build/build_workbook.py:492-563` (`create_newbuild_sam` function)

This is the core change. Add two new sections below the existing Mekko (C):
- **(D)** Gross P-5c cost category mix (intermediate — shows raw proportions)
- **(E)** Proportional allocation to SAM net totals (final answer)

Both sections only appear when P-5c data exists (FY26 only).

- [ ] **Step 1: Modify function signature to accept extra parameters**

Change line 492:

```python
def create_newbuild_sam(wb, d, label, prefix, cf, cf_neg, cf_inner):
```

to:

```python
def create_newbuild_sam(wb, d, label, prefix, cf, cf_neg, cf_inner, altview_cf=None, altview_inner=None):
```

- [ ] **Step 2: Add sections (D) and (E) before `finish_sheet(ws)`**

Before the `finish_sheet(ws)` call at line 563, add the new sections. They are gated on `d['p5c_types']` being non-empty:

```python
    # ── Sections D & E: P-5c cost category breakdown (FY26 only) ──

    p5c_types = d.get('p5c_types', [])
    if p5c_types and altview_inner:
        # Filter to types that are in the SAM scope AND have P-5c data
        sam_p5c = [t for t in p5c_types if t not in SAM_EXCLUDED_TYPES]
        if not sam_p5c:
            sam_p5c = []

        if sam_p5c:
            cats = [c for c in P5C_COST_CATEGORIES
                    if any(d['p5c_data'].get((t, c), 0) > 0 for t in sam_p5c)]

            n_types = len(sam_p5c)
            tc = 2 + n_types  # Total column

            # ── (D) Gross P-5c Cost Category Breakdown ──
            r += 3
            subsec_band(ws, r, f'(D) P-5c Gross Cost Category Breakdown by Vessel Type \u2014 {label} ($K)', tc)
            r += 1
            purpose_row(ws, r, 'Gross total-ship-estimate costs from Exhibit P-5c. These are pre-AP/SFF and will NOT match SAM net totals.')
            r += 1
            svc_r_d = r
            sam_p5c_ordered, n_usn_d, n_cg_d = write_svc_header(ws, r, sam_p5c, d['type_svc'])

            r += 1
            wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR); cw(ws, 1, 30)
            for i, vt in enumerate(sam_p5c_ordered):
                c = 2 + i
                wc(ws, r, c, vt, font=F_HDR, border=B_HDR); cw(ws, c, 14)
            wc(ws, r, tc, 'Total', font=F_HDR, border=B_HDR); cw(ws, tc, 14)
            hdr_r_d = r

            # Data rows — one per cost category, $ values
            first_d = r + 1
            for cat in cats:
                r += 1
                wc(ws, r, 1, cat, font=F_DATA)
                for i, vt in enumerate(sam_p5c_ordered):
                    c = 2 + i
                    formula = altview_inner('JB_B,1', f'JB_EX,"P-5c"', f'JB_CC,"{cat}"', f'JB_W,"{vt}"')
                    wc(ws, r, c, '=' + formula, font=F_DATA, fmt=NUM_FMT)
                wc(ws, r, tc, f'=SUM({get_column_letter(2)}{r}:{get_column_letter(tc-1)}{r})',
                   font=F_DATA, fmt=NUM_FMT)
            last_d = r

            # Total row
            r += 1; tkr_d = r
            wc(ws, r, 1, 'Gross Total ($K)', font=F_TOTAL, border=B_TOT)
            for c in range(2, tc + 1):
                total_cell(ws, r, c,
                           f'=SUM({get_column_letter(c)}{first_d}:{get_column_letter(c)}{last_d})')
            span_top_border(ws, r, tc)
            apply_group_borders(ws, svc_r_d, tkr_d, 2, n_usn_d, n_cg_d)

            # Percentage rows below total
            r += 1
            wc(ws, r, 1, '', font=F_GRAY)  # spacer label
            r += 1
            subsubsec_band(ws, r, 'Cost category mix (% of gross total per vessel type)', tc)
            r += 1
            wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR)
            for i, vt in enumerate(sam_p5c_ordered):
                wc(ws, r, 2 + i, vt, font=F_HDR, border=B_HDR)
            wc(ws, r, tc, 'Total', font=F_HDR, border=B_HDR)

            pct_first = r + 1
            for ci, cat in enumerate(cats):
                r += 1
                data_row = first_d + ci
                wc(ws, r, 1, cat, font=F_DATA)
                for c in range(2, tc + 1):
                    cl = get_column_letter(c)
                    wc(ws, r, c, f'=IFERROR({cl}{data_row}/{cl}${tkr_d},0)',
                       font=F_PCT, fmt=PCT_FMT)
            pct_last = r
            r += 1
            wc(ws, r, 1, 'Total', font=F_TOTAL, border=B_TOT)
            for c in range(2, tc + 1):
                pct_total(ws, r, c, 1.0)
            span_top_border(ws, r, tc)

            # ── (E) Proportional Cost Category Allocation to SAM Net Totals ──
            r += 3
            subsec_band(ws, r, f'(E) Proportional Cost Category Allocation to SAM Net Totals \u2014 {label} ($K)', tc)
            r += 1
            purpose_row(ws, r, 'P-5c percentage mix from (D) applied to SAM net budget-authority totals from (B). Totals reconcile to SAM.')
            r += 1
            svc_r_e = r
            sam_p5c_ordered_e, n_usn_e, n_cg_e = write_svc_header(ws, r, sam_p5c, d['type_svc'])

            r += 1
            wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR)
            for i, vt in enumerate(sam_p5c_ordered_e):
                c = 2 + i
                wc(ws, r, c, vt, font=F_HDR, border=B_HDR); cw(ws, c, 14)
            wc(ws, r, tc, 'Total', font=F_HDR, border=B_HDR)

            # SAM net total row (reference from section B via formula)
            r += 1; sam_ref_r = r
            wc(ws, r, 1, 'SAM Net Total ($K)', font=F_KPI, fill=BG_TEAL)
            for i, vt in enumerate(sam_p5c_ordered_e):
                c = 2 + i
                wc(ws, r, c, cf('JB_B,1', f'JB_W,"{vt}"'), font=F_KPI, fill=BG_TEAL, fmt=NUM_FMT)
            wc(ws, r, tc, f'=SUM({get_column_letter(2)}{r}:{get_column_letter(tc-1)}{r})',
               font=F_KPI, fill=BG_TEAL, fmt=NUM_FMT)

            # Allocated rows — SAM net total * P-5c percentage
            r += 1
            alloc_first = r
            for ci, cat in enumerate(cats):
                pct_row = pct_first + ci
                wc(ws, r, 1, cat, font=F_DATA)
                for c in range(2, tc + 1):
                    cl = get_column_letter(c)
                    wc(ws, r, c, f'=IFERROR({cl}${sam_ref_r}*{cl}{pct_row},0)',
                       font=F_DATA, fmt=NUM_FMT)
                r += 1
            r -= 1  # back up to last data row
            alloc_last = r

            # Total row
            r += 1
            wc(ws, r, 1, 'Allocated Total ($K)', font=F_TOTAL, border=B_TOT)
            for c in range(2, tc + 1):
                total_cell(ws, r, c,
                           f'=SUM({get_column_letter(c)}{alloc_first}:{get_column_letter(c)}{alloc_last})')
            span_top_border(ws, r, tc)

            # Verification row — should equal SAM net total
            r += 1
            wc(ws, r, 1, 'Check: matches SAM net?', font=F_GRAY)
            for c in range(2, tc + 1):
                cl = get_column_letter(c)
                wc(ws, r, c, f'=IFERROR({cl}{r-1}/{cl}{sam_ref_r}-1,0)', font=F_GRAY, fmt='0.0%')

            apply_group_borders(ws, svc_r_e, r, 2, n_usn_e, n_cg_e)

    finish_sheet(ws)
```

**IMPORTANT:** Remove the existing `finish_sheet(ws)` call at line 563 — it's now at the end of the new code above.

- [ ] **Step 3: Update the call site in `main()` to pass altview cascade**

In `main()`, after `cf, cf_neg, cf_inner = make_cascade(fyc['value_ranges'])` (line 1015), add:

```python
        acf, acf_inner = make_altview_cascade(fyc['value_ranges'])
```

Then update the `create_newbuild_sam` call (currently line 1020):

```python
        create_newbuild_sam(*args, altview_cf=acf, altview_inner=acf_inner)
```

- [ ] **Step 4: Build and verify sections (D) and (E)**

Run:
```bash
python3 build/build_workbook.py
```

Open the output in Excel/Numbers. Check:
1. FY26 Newbuild SAM has sections (D) and (E) below the existing Mekko
2. Section (D) shows gross $ values by vessel type and cost category
3. Section (D) percentage sub-table shows percentages summing to ~100% per column
4. Section (E) shows allocated $ values that sum to the SAM net total per vessel type
5. The "Check: matches SAM net?" row shows 0.0% (perfect reconciliation)
6. FY27 Newbuild SAM is UNCHANGED (no sections D/E)

- [ ] **Step 5: Commit**

```bash
git add build/build_workbook.py
git commit -m "feat: add P-5c cost category breakdown sections (D)/(E) to FY26 Newbuild SAM"
```

---

### Task 6: Create supplemental sheet — `create_newbuild_cost_detail()`

**Files:**
- Modify: `build/build_workbook.py` (add new function after `create_mro_sam`)

- [ ] **Step 1: Add the new sheet builder function**

Add after `create_mro_sam()`:

```python
def create_newbuild_cost_detail(wb, d, label, prefix, acf_inner):
    """Supplemental sheet: direct P-5c costs (Approach 2) + P-8a system detail.
    Only created when P-5c data is available (FY26)."""
    p5c_types = d.get('p5c_types', [])
    p8a_types = d.get('p8a_types', [])
    if not p5c_types:
        return

    ws = wb.create_sheet(f'{prefix} Newbuild Cost Detail')

    sam_p5c = [t for t in p5c_types if t not in SAM_EXCLUDED_TYPES]
    cats = [c for c in P5C_COST_CATEGORIES
            if any(d['p5c_data'].get((t, c), 0) > 0 for t in sam_p5c)]

    tc = 2 + len(sam_p5c)  # Total column
    mc = max(tc, 6)
    cw(ws, 1, 32)

    r = 1; title_band(ws, r, f'Newbuild Cost Detail \u2014 {label} ($K)', mc)
    r = 2; purpose_row(ws, r,
        'Gross ship-cost breakdown from P-5c and P-8a exhibits. '
        'NOT net budget authority \u2014 see Newbuild SAM for reconciled values.')

    # ── (A) Direct P-5c Cost Category Breakdown (Approach 2) ──
    r = 4; subsec_band(ws, r,
        f'(A) P-5c Total Ship Cost by Vessel Type & Cost Category \u2014 {label} ($K)', tc)
    r += 1
    svc_r = r
    ordered, n_usn, n_cg = write_svc_header(ws, r, sam_p5c, d['type_svc'])

    r += 1
    wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR)
    for i, vt in enumerate(ordered):
        c = 2 + i
        wc(ws, r, c, vt, font=F_HDR, border=B_HDR); cw(ws, c, 14)
    wc(ws, r, tc, 'Total', font=F_HDR, border=B_HDR); cw(ws, tc, 14)

    first_a = r + 1
    for cat in cats:
        r += 1
        wc(ws, r, 1, cat, font=F_DATA)
        for i, vt in enumerate(ordered):
            c = 2 + i
            formula = acf_inner('JB_B,1', f'JB_EX,"P-5c"', f'JB_CC,"{cat}"', f'JB_W,"{vt}"')
            wc(ws, r, c, '=' + formula, font=F_DATA, fmt=NUM_FMT)
        wc(ws, r, tc, f'=SUM({get_column_letter(2)}{r}:{get_column_letter(tc-1)}{r})',
           font=F_DATA, fmt=NUM_FMT)
    last_a = r

    r += 1; tkr_a = r
    wc(ws, r, 1, 'Gross Total ($K)', font=F_TOTAL, border=B_TOT)
    for c in range(2, tc + 1):
        total_cell(ws, r, c,
                   f'=SUM({get_column_letter(c)}{first_a}:{get_column_letter(c)}{last_a})')
    span_top_border(ws, r, tc)
    apply_group_borders(ws, svc_r, tkr_a, 2, n_usn, n_cg)

    # ── (B) P-8a System-Level Detail by Vessel Type ──
    r += 3; subsec_band(ws, r,
        f'(B) P-8a System-Level Detail by Vessel Type \u2014 {label} ($K)', 4)
    r += 1
    purpose_row(ws, r, 'Individual GFE systems from Exhibit P-8a, grouped by cost category within each vessel type.')

    sam_p8a = [t for t in p8a_types if t not in SAM_EXCLUDED_TYPES]

    for vt in sam_p8a:
        # Gather systems for this vessel type
        systems = []
        for (vt2, cc, ce), val in sorted(d['p8a_data'].items(), key=lambda x: -x[1]):
            if vt2 == vt and val > 0:
                systems.append((cc, ce, val))
        if not systems:
            continue

        r += 2
        subsubsec_band(ws, r, vt, 4)
        r += 1
        hdr_row(ws, r, [('System', 32), ('Cost Category', 22), (f'{label} ($K)', 14), ('% of Type', 10)])
        ft = r + 1

        # Group by cost category
        from itertools import groupby
        systems_sorted = sorted(systems, key=lambda x: (list(P8A_COST_CATEGORIES).index(x[0])
                                                         if x[0] in P8A_COST_CATEGORIES else 99, -x[2]))
        for cc, ce, val in systems_sorted:
            r += 1
            wc(ws, r, 1, ce, font=F_DATA)
            wc(ws, r, 2, cc, font=F_GRAY)
            wc(ws, r, 3, val, font=F_BLUE, fmt=NUM_FMT)
        lt = r

        r += 1
        total_label(ws, r, 1, f'{vt} Total')
        total_cell(ws, r, 3, f'=SUM(C{ft}:C{lt})')
        span_top_border(ws, r, 4)

        # Fill percentage column
        for rn in range(ft, lt + 1):
            wc(ws, rn, 4, f'=IFERROR(C{rn}/C${r},0)', font=F_PCT, fmt=PCT_FMT)
        pct_total(ws, r, 4, 1.0)

    # ── (C) Top P-8a Systems — Cross-Program Summary ──
    r += 3; subsec_band(ws, r,
        f'(C) Top P-8a Systems \u2014 Cross-Program Summary \u2014 {label} ($K)', 5)
    r += 1
    purpose_row(ws, r, 'Largest GFE systems aggregated across all SAM vessel types.')

    # Aggregate by system name across vessel types
    sys_agg = defaultdict(lambda: {'total': 0, 'category': '', 'programs': []})
    for (vt, cc, ce), val in d['p8a_data'].items():
        if vt in SAM_EXCLUDED_TYPES or val <= 0:
            continue
        sys_agg[ce]['total'] += val
        sys_agg[ce]['category'] = cc
        sys_agg[ce]['programs'].append(vt)

    top_systems = sorted(sys_agg.items(), key=lambda x: -x[1]['total'])[:30]

    r += 1
    hdr_row(ws, r, [('System', 32), ('Cost Category', 22), (f'{label} ($K)', 14),
                     ('# Programs', 10), ('Vessel Types', 40)])
    ft = r + 1
    for ce, info in top_systems:
        r += 1
        wc(ws, r, 1, ce, font=F_DATA)
        wc(ws, r, 2, info['category'], font=F_GRAY)
        wc(ws, r, 3, info['total'], font=F_BLUE, fmt=NUM_FMT)
        wc(ws, r, 4, len(set(info['programs'])), font=F_DATA)
        wc(ws, r, 5, ', '.join(sorted(set(info['programs']))), font=F_GRAY)
    lt = r

    r += 1
    total_label(ws, r, 1, 'Total (top systems)')
    total_cell(ws, r, 3, f'=SUM(C{ft}:C{lt})')
    span_top_border(ws, r, 5)

    finish_sheet(ws)
```

Note: The `from itertools import groupby` inside the function should be moved to the top of the file with other imports. Add `from itertools import groupby` to the imports if not already present. Actually, looking at the code above, `groupby` isn't used (I sorted instead). Remove that import line from inside the function.

- [ ] **Step 2: Wire the supplemental sheet into `main()`**

In `main()`, after the `create_mro_sam` call, add:

```python
        # Supplemental cost detail (FY26 only — P-5c/P-8a data availability)
        cost_detail_name = None
        if d.get('p5c_types'):
            create_newbuild_cost_detail(wb, d, label, prefix, acf_inner)
            cost_detail_name = f'{prefix} Newbuild Cost Detail'
```

Update the `fy_sheets` list (line 1026) and `generated` list to include the new sheet:

```python
        fy_sheets = [
            f'{prefix} Total Funding', f'{prefix} Newbuild TAM',
            f'{prefix} Newbuild SAM',  f'{prefix} MRO TAM',
            f'{prefix} MRO SAM',
        ]
        if cost_detail_name:
            fy_sheets.append(cost_detail_name)

        for sn in fy_sheets:
            if sn in wb.sheetnames:
                wb[sn].sheet_properties.tabColor = tab_color
```

Update the `generated` list similarly:

```python
        generated.extend([
            f'{prefix} Total Funding', f'{prefix} Newbuild TAM',
            f'{prefix} Newbuild SAM',  f'{prefix} MRO TAM',
            f'{prefix} MRO SAM',
        ])
        if cost_detail_name:
            generated.append(cost_detail_name)
```

- [ ] **Step 3: Add `defaultdict` import to the function**

The `create_newbuild_cost_detail` function uses `defaultdict` in the cross-program summary section. This is already imported at the top of the file (`from collections import defaultdict`). Verify this — no action needed if already imported.

- [ ] **Step 4: Build and verify the supplemental sheet**

Run:
```bash
python3 build/build_workbook.py
```

Open output in Excel/Numbers. Check:
1. New sheet "FY26 Newbuild Cost Detail" exists
2. Section (A) shows P-5c gross costs matching section (D) in the SAM sheet
3. Section (B) shows per-vessel-type system detail with $ values and percentages
4. Section (C) shows top 30 systems across all SAM vessel types
5. No "FY27 Newbuild Cost Detail" sheet exists

- [ ] **Step 5: Commit**

```bash
git add build/build_workbook.py
git commit -m "feat: add FY26 Newbuild Cost Detail supplemental sheet with P-8a system data"
```

---

### Task 7: Final integration and verification

**Files:**
- Modify: `build/build_workbook.py` (final touches)

- [ ] **Step 1: Update Validation sheet documentation**

This is optional but good practice. The Validation sheet documents the data dictionary. Consider adding entries for the new columns and sections in a future pass (not blocking).

- [ ] **Step 2: Full build from clean state**

```bash
python3 build/build_workbook.py
```

Verify console output shows:
- `Derived columns: populated ~1420 ALT_VIEW rows`
- `P-5c types` and `P-8a types` listed for FY26
- No errors
- Max formula length under 8192

- [ ] **Step 3: Verify in Excel/Numbers — comprehensive check**

Open the output workbook. Check each item:

FY26 Newbuild SAM:
- [ ] Sections (A), (B), (C) unchanged from previous version
- [ ] Section (D): 8-9 cost category rows × vessel type columns, dollar values populated
- [ ] Section (D) percentage sub-table: percentages sum to ~100% per column
- [ ] Section (E): SAM net total row matches section (B) totals
- [ ] Section (E): allocated values = SAM total × percentage, sum to SAM total
- [ ] Section (E): "Check" row shows 0.0% or very small rounding error

FY27 Newbuild SAM:
- [ ] Unchanged — no sections (D) or (E)

FY26 Newbuild Cost Detail:
- [ ] Section (A) gross values match section (D) in SAM
- [ ] Section (B) per-vessel-type P-8a detail present for major types
- [ ] Section (C) top systems list is populated and sorted by $ value

J Book Items Cons.:
- [ ] Col AL header = "Exhibit Level"
- [ ] Col AM header = "Cost Category"
- [ ] P-5c rows have both columns populated
- [ ] P-8a rows have both columns populated
- [ ] P-35 rows have Exhibit Level only (Cost Category blank)
- [ ] Non-ALT_VIEW rows have both columns blank

- [ ] **Step 4: Commit final state**

```bash
git add build/build_workbook.py
git commit -m "feat: complete Newbuild SAM cost category restructuring for FY26"
```
