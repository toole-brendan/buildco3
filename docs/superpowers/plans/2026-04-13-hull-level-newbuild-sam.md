# Hull-Level Newbuild SAM Restructuring

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure the Newbuild SAM sheet and Cost Detail sheet to show hull-level granularity (DDG, LPD, LHA, FFG, LSM, T-AO, etc.) instead of vessel-type level, so the user can trace budget line items to specific module/integration funding per hull program.

**Architecture:** Add hull-level data collection to `read_data()`, add a `JB_H` named range for SUMIFS, then replace SAM sections D/E with hull-oriented D/E/F and reorganize the Cost Detail sheet by hull. Sections A-C of SAM are unchanged.

**Tech Stack:** Python 3, openpyxl, Excel SUMIFS formulas

---

### Task 1: Add JB_H named range for hull column

**Files:**
- Modify: `build/build_from_data.py:1349-1360` (create_named_ranges)

- [ ] **Step 1: Add JB_H to shared named ranges**

In `create_named_ranges()`, add hull named range to the `shared` list:

```python
shared = [
    ('JB_A', 'A'),     # Source Book (col 1)
    ('JB_B', 'I'),     # Bucket (col 9)
    ('JB_F', 'J'),     # Bucket Sub Category (col 10)
    ('JB_H', 'N'),     # Vessel Hull (col 14)        <-- ADD
    ('JB_S', 'E'),     # Row Type (col 5)
    ('JB_U', 'K'),     # Vessel Service (col 11)
    ('JB_V', 'L'),     # Vessel Category (col 12)
    ('JB_W', 'M'),     # Vessel Type (col 13)
    ('JB_CE', 'AG'),   # Cost Element (col 33)
    ('JB_EX', 'G'),    # Exhibit Level (col 7)
    ('JB_CC', 'H'),    # Cost Category (col 8)
]
```

---

### Task 2: Extend read_data() for hull-level data collection

**Files:**
- Modify: `build/build_from_data.py:353-464` (read_data function)

- [ ] **Step 1: Add hull accumulators**

After existing accumulator declarations (line ~378), add:

```python
nb_hull = defaultdict(float)        # hull -> $K (bucket 1 additive)
hull_svc = {}                        # hull -> service (USN/MSC/USCG)
hull_type = {}                       # hull -> vessel type
p5c_hull = defaultdict(float)        # (hull, cost_category) -> $K
p5c_hull_set = set()
p8a_hull = defaultdict(float)        # (hull, cost_category, system_name) -> $K
p8a_hull_set = set()
```

- [ ] **Step 2: Read hull column in main loop and populate hull mappings**

After reading `sv` (Vessel Service), add hull read:

```python
hl  = str(row[13].value).strip() if row[13].value else ''   # Vessel Hull (col N)
```

In the existing `if cat in TAM_CATEGORIES and vt:` block, add hull mapping:

```python
if cat in TAM_CATEGORIES and vt:
    all_tam_types.add(vt)
    if sv: type_svc[vt] = sv
    type_cat[vt] = cat
    if hl:                          # <-- ADD
        if sv: hull_svc[hl] = sv
        hull_type[hl] = vt
```

- [ ] **Step 3: Accumulate hull-level P-5c/P-8a in ALT_VIEW scan**

In the ALT_VIEW scan block, after accumulating by vessel type, add hull accumulation:

For P-5c:
```python
if ex == 'P-5c' and cc_val in P5C_VALID:
    p5c_data[(vt, cc_val)] += val
    p5c_types.add(vt)
    if hl:                          # <-- ADD
        p5c_hull[(hl, cc_val)] += val
        p5c_hull_set.add(hl)
```

For P-8a:
```python
elif ex == 'P-8a':
    ce = str(row[32].value).strip() if row[32].value else ''
    if ce:
        p8a_data[(vt, cc_val, ce)] += val
        p8a_types.add(vt)
        if hl:                      # <-- ADD
            p8a_hull[(hl, cc_val, ce)] += val
            p8a_hull_set.add(hl)
```

- [ ] **Step 4: Accumulate hull-level newbuild totals in additive section**

In the `if bs == '1':` block:
```python
if bs == '1':
    if cat in TAM_CATEGORIES:
        nb[vt] += v
        if hl: nb_hull[hl] += v     # <-- ADD
    elif cat: nb_excl[cat] += v
```

- [ ] **Step 5: Add hull data to return dict**

Before the return statement, compute hull lists using the existing `sorted_svc` pattern but with hull_svc:

```python
def sorted_svc_hull(hulls, val_map):
    usn = sorted([h for h in hulls if hull_svc.get(h, '') in ('USN', 'MSC', '')],
                  key=lambda h: -val_map.get(h, 0))
    cg  = sorted([h for h in hulls if hull_svc.get(h, '') == 'USCG'],
                  key=lambda h: -val_map.get(h, 0))
    return usn + cg

nb_hull_nz = [h for h in sorted_svc_hull(
    {h for h in nb_hull if hull_type.get(h, '') not in SAM_EXCLUDED_TYPES}, nb_hull)
    if nb_hull.get(h, 0) > 0]
```

Add to the return dict:
```python
# Hull-level data
'nb_hull': dict(nb_hull),
'nb_hull_nz': nb_hull_nz,
'hull_svc': hull_svc,
'hull_type': hull_type,
'p5c_hull': dict(p5c_hull),
'p5c_hull_types': sorted_svc_hull(
    [h for h in p5c_hull_set if hull_type.get(h, '') not in SAM_EXCLUDED_TYPES
     and any(p5c_hull.get((h, c), 0) > 0 for c in P5C_VALID)], nb_hull),
'p8a_hull': dict(p8a_hull),
'p8a_hull_types': sorted_svc_hull(
    [h for h in p8a_hull_set if hull_type.get(h, '') not in SAM_EXCLUDED_TYPES], nb_hull),
```

- [ ] **Step 6: Add hull print diagnostics in main()**

After existing print statements in `main()`:
```python
print(f'  NB hulls non-zero: {len(d["nb_hull_nz"])}, P-5c hulls: {len(d["p5c_hull_types"])}, P-8a hulls: {len(d["p8a_hull_types"])}')
```

---

### Task 3: Restructure create_newbuild_sam() with hull-level sections D/E/F

**Files:**
- Modify: `build/build_from_data.py:607-809` (create_newbuild_sam function)

Sections A, B, C remain unchanged. Replace the existing sections D & E block (lines ~679-808) with new hull-level sections D, E, F.

- [ ] **Step 1: Replace section D — Newbuild SAM by Hull Program**

After section C (mekko) completes at `r = tkr`, replace everything from `# ── Sections D & E` through `finish_sheet(ws)` with:

```python
# ── Section D: Newbuild SAM by Hull Program ──

hull_nz = d.get('nb_hull_nz', [])
if hull_nz:
    r += 3
    subsec_band(ws, r, f'(D) Newbuild SAM by Hull Program \u2014 {label} ($K)', 4)
    r += 1
    purpose_row(ws, r, 'Same funding as (B) broken down to individual hull programs \u2014 the level at which budget line items are traceable.')
    r += 1
    hdr_row(ws, r, [('Hull Program', 30), ('Service', 8), (f'{label} ($K)', 12), ('% of SAM', 10)])
    ft_d = r + 1
    for hl in hull_nz:
        r += 1
        vt_label = d['hull_type'].get(hl, '')
        wc(ws, r, 1, f'{hl} ({vt_label})' if vt_label else hl, font=F_DATA)
        wc(ws, r, 2, d['hull_svc'].get(hl, ''), font=F_DATA)
        wc(ws, r, 3, cf('JB_B,1', f'JB_H,"{hl}"'), font=F_DATA, fmt=NUM_FMT)
    lt_d = r; r += 1; tr_d = r
    total_label(ws, r, 1, 'Newbuild SAM'); total_label(ws, r, 2, '')
    total_cell(ws, r, 3, f'=SUM(C{ft_d}:C{lt_d})')
    pct_total(ws, r, 4, 1.0)
    span_top_border(ws, r, 4)
    for rn in range(ft_d, lt_d + 1):
        wc(ws, rn, 4, f'=IFERROR(C{rn}/C${tr_d},0)', font=F_PCT, fmt=PCT_FMT)
```

- [ ] **Step 2: Add section E — P-5c Cost Category Breakdown by Hull**

Immediately after section D:

```python
# ── Section E: P-5c Cost Category Breakdown by Hull ──

p5c_hulls = d.get('p5c_hull_types', [])
if p5c_hulls and altview_inner:
    cats = [c for c in P5C_COST_CATEGORIES
            if any(d['p5c_hull'].get((h, c), 0) > 0 for h in p5c_hulls)]

    n_hulls = len(p5c_hulls)
    tc_e = 2 + n_hulls  # Total column

    r += 3
    subsec_band(ws, r, f'(E) P-5c Gross Cost Category Breakdown by Hull \u2014 {label} ($K)', tc_e)
    r += 1
    purpose_row(ws, r, 'Gross total-ship-estimate costs from Exhibit P-5c. These are pre-AP/SFF and will NOT match SAM net totals.')
    r += 1
    svc_r_e = r
    p5c_ordered, n_usn_e, n_cg_e = write_svc_header(ws, r, p5c_hulls, d['hull_svc'])

    r += 1
    wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR); cw(ws, 1, 30)
    for i, hl in enumerate(p5c_ordered):
        c = 2 + i
        wc(ws, r, c, hl, font=F_HDR, border=B_HDR); cw(ws, c, 14)
    wc(ws, r, tc_e, 'Total', font=F_HDR, border=B_HDR); cw(ws, tc_e, 14)
    hdr_r_e = r

    # Data rows
    first_e = r + 1
    for cat in cats:
        r += 1
        wc(ws, r, 1, cat, font=F_DATA)
        for i, hl in enumerate(p5c_ordered):
            c = 2 + i
            formula = altview_inner('JB_B,1', f'JB_EX,"P-5c"', f'JB_CC,"{cat}"', f'JB_H,"{hl}"')
            wc(ws, r, c, '=' + formula, font=F_DATA, fmt=NUM_FMT)
        wc(ws, r, tc_e, f'=SUM({get_column_letter(2)}{r}:{get_column_letter(tc_e-1)}{r})',
           font=F_DATA, fmt=NUM_FMT)
    last_e = r

    # Total row
    r += 1; tkr_e = r
    wc(ws, r, 1, 'Gross Total ($K)', font=F_TOTAL, border=B_TOT)
    for c in range(2, tc_e + 1):
        total_cell(ws, r, c,
                   f'=SUM({get_column_letter(c)}{first_e}:{get_column_letter(c)}{last_e})')
    span_top_border(ws, r, tc_e)
    apply_group_borders(ws, svc_r_e, tkr_e, 2, n_usn_e, n_cg_e)

    # Percentage sub-table
    r += 2
    subsubsec_band(ws, r, 'Cost category mix (% of gross total per hull program)', tc_e)
    r += 1
    wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR)
    for i, hl in enumerate(p5c_ordered):
        wc(ws, r, 2 + i, hl, font=F_HDR, border=B_HDR)
    wc(ws, r, tc_e, 'Total', font=F_HDR, border=B_HDR)

    pct_first_e = r + 1
    for ci, cat in enumerate(cats):
        r += 1
        data_row = first_e + ci
        wc(ws, r, 1, cat, font=F_DATA)
        for c in range(2, tc_e + 1):
            cl = get_column_letter(c)
            wc(ws, r, c, f'=IFERROR({cl}{data_row}/{cl}${tkr_e},0)',
               font=F_PCT, fmt=PCT_FMT)
    r += 1
    wc(ws, r, 1, 'Total', font=F_TOTAL, border=B_TOT)
    for c in range(2, tc_e + 1):
        pct_total(ws, r, c, 1.0)
    span_top_border(ws, r, tc_e)
```

- [ ] **Step 3: Add section F — Proportional Allocation by Hull to SAM Net**

Immediately after section E percentage table:

```python
    # ── Section F: Proportional Cost Category Allocation by Hull ──

    r += 3
    subsec_band(ws, r, f'(F) Proportional Cost Category Allocation to SAM Net Totals \u2014 {label} ($K)', tc_e)
    r += 1
    purpose_row(ws, r, 'P-5c percentage mix from (E) applied to SAM net budget-authority totals from (D). Totals reconcile to SAM.')
    r += 1
    svc_r_f = r
    p5c_ordered_f, n_usn_f, n_cg_f = write_svc_header(ws, r, p5c_hulls, d['hull_svc'])

    r += 1
    wc(ws, r, 1, 'Cost Category', font=F_HDR, border=B_HDR)
    for i, hl in enumerate(p5c_ordered_f):
        c = 2 + i
        wc(ws, r, c, hl, font=F_HDR, border=B_HDR); cw(ws, c, 14)
    wc(ws, r, tc_e, 'Total', font=F_HDR, border=B_HDR)

    # SAM net total reference row
    r += 1; sam_ref_r = r
    wc(ws, r, 1, 'SAM Net Total ($K)', font=F_KPI, fill=BG_TEAL)
    for i, hl in enumerate(p5c_ordered_f):
        c = 2 + i
        wc(ws, r, c, cf('JB_B,1', f'JB_H,"{hl}"'), font=F_KPI, fill=BG_TEAL, fmt=NUM_FMT)
    wc(ws, r, tc_e, f'=SUM({get_column_letter(2)}{r}:{get_column_letter(tc_e-1)}{r})',
       font=F_KPI, fill=BG_TEAL, fmt=NUM_FMT)

    # Allocated rows
    alloc_first = r + 1
    for ci, cat in enumerate(cats):
        r += 1
        pct_row = pct_first_e + ci
        wc(ws, r, 1, cat, font=F_DATA)
        for c in range(2, tc_e + 1):
            cl = get_column_letter(c)
            wc(ws, r, c, f'=IFERROR({cl}${sam_ref_r}*{cl}{pct_row},0)',
               font=F_DATA, fmt=NUM_FMT)
    alloc_last = r

    # Total row
    r += 1
    wc(ws, r, 1, 'Allocated Total ($K)', font=F_TOTAL, border=B_TOT)
    for c in range(2, tc_e + 1):
        total_cell(ws, r, c,
                   f'=SUM({get_column_letter(c)}{alloc_first}:{get_column_letter(c)}{alloc_last})')
    span_top_border(ws, r, tc_e)

    # Verification row
    r += 1
    wc(ws, r, 1, 'Check: matches SAM net?', font=F_GRAY)
    for c in range(2, tc_e + 1):
        cl = get_column_letter(c)
        wc(ws, r, c, f'=IFERROR({cl}{r-1}/{cl}{sam_ref_r}-1,0)', font=F_GRAY, fmt='0.0%')

    apply_group_borders(ws, svc_r_f, r, 2, n_usn_f, n_cg_f)

finish_sheet(ws)
```

---

### Task 4: Restructure Cost Detail sheet for hull-level organization

**Files:**
- Modify: `build/build_from_data.py:1006-1142` (create_newbuild_cost_detail function)

- [ ] **Step 1: Replace section A — P-5c by hull**

Change `p5c_types` references to `p5c_hull_types`, vessel type loop to hull loop, JB_W conditions to JB_H conditions. Replace the `sam_p5c` filter and column headers to use hull names.

- [ ] **Step 2: Replace section B — P-8a by hull**

Change `p8a_types` references to `p8a_hull_types`. In the per-type loop, iterate over hulls instead of vessel types. Use `p8a_hull` data dict keyed by `(hull, cc, ce)` instead of `(vt, cc, ce)`.

- [ ] **Step 3: Section C — Top systems cross-program (keep as-is)**

No changes needed. Already aggregates across programs.

---

### Task 5: Run build and verify

- [ ] **Step 1: Run build**

```bash
python3 build/build_from_data.py
```

Expected: Generates next v5.x output with hull-level sections.

- [ ] **Step 2: Verify output structure**

Open output XLSX. Check:
- FY26 Newbuild SAM sections D/E/F show hull columns (DDG, LSM, T-AO, etc.)
- Section D hull totals sum to SAM total from section B
- Section E shows P-5c cost categories with non-zero values per hull
- Section F verification row shows 0.0% (reconciles to SAM net)
- Cost Detail section A shows P-5c by hull
- Cost Detail section B shows P-8a systems grouped by hull
- All other sheets unchanged

- [ ] **Step 3: Commit**

```bash
git add build/build_from_data.py
git commit -m "Restructure Newbuild SAM to hull-level granularity (v5.x)"
```
