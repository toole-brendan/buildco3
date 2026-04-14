# MRO SAM Sheet Restructure — Progressive Narrowing with Cost-Element Coverage Gap

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the FY26/FY27 MRO SAM sheets to follow the same progressive narrowing pattern as Newbuild SAM (vessel type → hull program → cost-element coverage), with honest acknowledgment that cost-element data does not exist for MRO work.

**Architecture:** Add MRO hull accumulators to `read_data()`, then rewrite `create_mro_sam()` with sections A through E mirroring the Newbuild SAM pattern. A sticky note on each MRO SAM sheet explains why cost-element coverage drops to zero. The Mekko section uses hull-level granularity instead of vessel-type.

**Tech Stack:** Python 3, openpyxl, OOXML sticky notes via `prototype_annotations.py`

---

## File Structure

- **Modify:** `build/build_from_data.py` — `read_data()` (add MRO hull accumulators), `create_mro_sam()` (full rewrite), `main()` (add MRO SAM sticky note annotations)
- **Modify:** `build/validation_sheet.py` — update MRO SAM definition text

No new files. No test files (build script verified by running and inspecting output).

---

## Current State

The MRO SAM sheet currently has 3 sections:
- (A) Bridge: MRO TAM → MRO SAM (waterfall removing vessel types + work types)
- (B) MRO SAM by Vessel Type — SDM/Mod/Total/% columns
- (C) Mekko — SDM vs Mod % by vessel type

## Target State

The restructured sheet has 5 sections, mirroring Newbuild SAM:
- **(A)** Bridge: MRO TAM → MRO SAM (same logic, cleaner)
- **(B)** MRO SAM by Vessel Type — SDM/Mod/Total/% (existing, unchanged)
- **(C)** MRO SAM by Hull Program — **new**: hull-level SDM/Mod/Total/% 
- **(C→D)** Bridge: All Programs → Cost-Element Coverage — **new**: shows every hull dropping off (zero P-5c data), sticky note explains the gap
- **(D)** MRO SAM — SDM vs Modernization by Hull (Mekko) — relocated from old (C), upgraded to hull-level granularity

## Data Findings

- Hull-level MRO data is **complete**: 15 hulls sum exactly to vessel-type totals ($7.64B, zero gap)
- **Zero** MRO rows have exhibit level (P-5c/P-8a) or cost category data
- ALT_VIEW data for MRO exists but is by availability type (OH/SRA/SIA) and by public shipyard (NNSY/PSNSY/etc.) — not cost-element breakdowns
- All OPN Mod items without vessel type are already excluded from MRO SAM (they fail the TAM_CATEGORIES filter)

---

### Task 1: Add MRO Hull Accumulators to `read_data()`

**Files:**
- Modify: `build/build_from_data.py:385-530` (the `read_data()` function)

- [ ] **Step 1: Add MRO hull accumulators**

In `read_data()`, after the existing hull-level accumulators (line ~398), add:

```python
mro_hull = defaultdict(lambda: defaultdict(float))  # hull -> bucket -> $K
```

Then inside the MRO accumulation block (line ~456-459), add hull tracking:

```python
elif bs in MRO_BKTS:
    if cat in TAM_CATEGORIES:
        mro[vt] += v; mro_bkt[vt][bs] += v; mro_b[bs] += v
        if hl:
            mro_hull[hl][bs] += v   # <-- NEW
    elif cat: mro_excl[cat] += v
```

- [ ] **Step 2: Add hull-level MRO lists to return dict**

After `mro_sam_nz` (line ~482), add:

```python
mro_hull_sam_nz = [h for h in sorted_svc_hull(
    {h for h in mro_hull
     if hull_type.get(h, '') not in SAM_EXCLUDED_TYPES
     and (mro_hull[h].get('2', 0) + mro_hull[h].get('4', 0)) > 0},
    {h: mro_hull[h].get('2', 0) + mro_hull[h].get('4', 0)
     for h in mro_hull})
    if (mro_hull.get(h, {}).get('2', 0) + mro_hull.get(h, {}).get('4', 0)) > 0]
```

In the return dict (line ~484+), add:

```python
'mro_hull': dict(mro_hull),
'mro_hull_sam_nz': mro_hull_sam_nz,
```

- [ ] **Step 3: Add diagnostic print in `main()`**

After the existing MRO SAM print (line ~1751), add:

```python
print(f'  MRO SAM hulls: {len(d["mro_hull_sam_nz"])}')
```

- [ ] **Step 4: Verify data prep**

Run:
```bash
python3 -c "
import sys; sys.path.insert(0, 'build')
from build_from_data import read_data
d = read_data('build/data_v2.xlsx', [24, 20, 18])
print(f'MRO SAM hulls: {len(d[\"mro_hull_sam_nz\"])}')
for h in d['mro_hull_sam_nz']:
    bkts = d['mro_hull'].get(h, {})
    b2 = bkts.get('2', 0); b4 = bkts.get('4', 0)
    print(f'  {h}: SDM={b2:,.0f}  Mod={b4:,.0f}  Total={b2+b4:,.0f}')
"
```

Expected: 15 hulls, totals matching the vessel-type sums ($7,642,430K total).

- [ ] **Step 5: Commit**

```bash
git add build/build_from_data.py
git commit -m "Add MRO hull accumulators to read_data()"
```

---

### Task 2: Rewrite `create_mro_sam()` — Sections A and B

**Files:**
- Modify: `build/build_from_data.py:1196-1303` (the `create_mro_sam()` function)

- [ ] **Step 1: Update function signature and setup**

Replace the entire `create_mro_sam()` function. Start with the signature, setup, and sections A-B:

```python
def create_mro_sam(wb, d, label, prefix, cf, cf_neg, cf_inner, mro_tam_info=None):
    ws = wb.create_sheet(f'{prefix} MRO SAM')

    hull_nz = d.get('mro_hull_sam_nz', [])
    mc = max(6, 2 + len(hull_nz) + 1)
    cw(ws, 1, 30); cw(ws, 2, 12)

    tam_sheet = f'{prefix} MRO TAM'

    # ── Title & Purpose ──
    r = 1; title_band(ws, r, f'MRO SAM — {label} ($K)', mc)
    r = 2; purpose_row(ws, r,
        'Outsourceable MRO sized at hull-program level. Starts from MRO TAM, '
        'excludes single-yard/nuclear programs (Submarines, Aircraft Carriers, UUVs), '
        'then narrows work types to scheduled depot maintenance (Bucket 2) and '
        'modernization/alteration installation (Bucket 4) — the categories where '
        'a company could compete for repair or upgrade work.')

    # ── (A) Bridge: MRO TAM → MRO SAM ──
    r = 4; subsec_band(ws, r, '(A) Bridge: MRO TAM → MRO SAM', 2)
    r += 1; bridge_first = r
    tam_ref_row = mro_tam_info['bkt_total_row'] if mro_tam_info else 18
    wc(ws, r, 1, 'MRO TAM', font=F_DATA)
    wc(ws, r, 2, f"='{tam_sheet}'!B{tam_ref_row}", font=F_GREEN, fmt=NUM_FMT)

    excl_rows = []
    for vt in ['Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles']:
        r += 1; excl_rows.append(r)
        wc(ws, r, 1, f'  Less: {vt}', font=F_DATA)
        parts = '+'.join(cf_inner(f'JB_B,{b}', f'JB_W,"{vt}"') for b in MRO_BKTS)
        wc(ws, r, 2, f'=-({parts})', font=F_DATA, fmt=NUM_FMT)

    r += 1; nowork_row = r
    wc(ws, r, 1, '  Less: Non-outsourceable work types (Buckets 3, 5, 6, 7)', font=F_DATA)

    r += 1; sam_result_row = r
    total_label(ws, r, 1, 'MRO SAM')
    sam_parts = '+'.join(
        cf_inner(f'JB_B,{b}', f'JB_V,"{c}"')
        for b in ['2', '4'] for c in sorted(TAM_CATEGORIES))
    excl_parts = '+'.join(
        f'-({cf_inner(f"JB_B,{b}", f"""JB_W,"{vt}" """.strip())})'
        for b in ['2', '4']
        for vt in ['Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles'])
    total_cell(ws, r, 2, f'={sam_parts}{excl_parts}')
    span_top_border(ws, r, 2)

    excl_sum = '+'.join(f'B{er}' for er in excl_rows)
    wc(ws, nowork_row, 2, f'=-(B{bridge_first}+{excl_sum}-B{sam_result_row})',
       font=F_DATA, fmt=NUM_FMT)

    # ── (B) MRO SAM by Vessel Type ──
    all_types = svc_order(d['all_sam_mro_sorted'], d['type_svc'])
    r += 3; subsec_band(ws, r, '(B) MRO SAM by Vessel Type', 6)
    r += 1; hdr_row(ws, r, [
        ('Vessel Type', 30), ('Service', 8),
        ('SDM ($K)', 12), ('Mod ($K)', 12), ('Total ($K)', 12), ('% of SAM', 10),
    ])
    ft = r + 1
    for vt in all_types:
        r += 1
        wc(ws, r, 1, vt, font=F_DATA)
        wc(ws, r, 2, d['type_svc'].get(vt, ''), font=F_DATA)
        wc(ws, r, 3, cf('JB_B,2', f'JB_W,"{vt}"'), font=F_DATA, fmt=NUM_FMT)
        wc(ws, r, 4, cf('JB_B,4', f'JB_W,"{vt}"'), font=F_DATA, fmt=NUM_FMT)
        wc(ws, r, 5, f'=C{r}+D{r}', font=F_DATA, fmt=NUM_FMT)
    lt = r; r += 1; tr = r
    total_label(ws, r, 1, 'MRO SAM'); total_label(ws, r, 2, '')
    for c in [3, 4, 5]:
        total_cell(ws, r, c,
                   f'=SUM({get_column_letter(c)}{ft}:{get_column_letter(c)}{lt})')
    pct_total(ws, r, 6, 1.0)
    span_top_border(ws, r, 6)
    for rn in range(ft, lt + 1):
        wc(ws, rn, 6, f'=IFERROR(E{rn}/E${tr},0)', font=F_PCT, fmt=PCT_FMT)
```

This preserves sections A and B from the current implementation with minor improvements (clearer "Less:" label for non-outsourceable work types).

- [ ] **Step 2: Verify sections A-B compile**

Save and run:
```bash
cd /Users/brendantoole/projects2/buildco3 && python3 -c "import ast; ast.parse(open('build/build_from_data.py').read()); print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add build/build_from_data.py
git commit -m "Rewrite MRO SAM sections A-B with updated purpose row"
```

---

### Task 3: Add Section C — MRO SAM by Hull Program

**Files:**
- Modify: `build/build_from_data.py` — inside `create_mro_sam()`, after section B

- [ ] **Step 1: Add section C — hull program table**

Continue in `create_mro_sam()` immediately after section B's total row and percentage loop. This section mirrors Newbuild SAM section C exactly:

```python
    # ── (C) MRO SAM by Hull Program ──
    mc_hull = 7  # Hull, VT, Svc, SDM, Mod, Total, %
    tr_c = None
    if hull_nz:
        r += 3
        subsec_band(ws, r, f'(C) MRO SAM by Hull Program — {label} ($K)', mc_hull)
        r += 1
        purpose_row(ws, r,
            'Same funding as (B) broken down to individual hull programs — '
            'the level at which depot maintenance and modernization line items are traceable.')
        r += 1
        hdr_row(ws, r, [
            ('Hull Program', 16), ('Vessel Type', 24), ('Service', 8),
            ('SDM ($K)', 12), ('Mod ($K)', 12), ('Total ($K)', 12), ('% of Total', 10),
        ])
        ft_c = r + 1
        for hl in hull_nz:
            r += 1
            wc(ws, r, 1, hl, font=F_DATA)
            wc(ws, r, 2, d['hull_type'].get(hl, ''), font=F_DATA)
            wc(ws, r, 3, d['hull_svc'].get(hl, ''), font=F_DATA)
            wc(ws, r, 4, cf('JB_B,2', f'JB_H,"{hl}"'), font=F_DATA, fmt=NUM_FMT)
            wc(ws, r, 5, cf('JB_B,4', f'JB_H,"{hl}"'), font=F_DATA, fmt=NUM_FMT)
            wc(ws, r, 6, f'=D{r}+E{r}', font=F_DATA, fmt=NUM_FMT)
        lt_c = r; r += 1; tr_c = r
        total_label(ws, r, 1, 'MRO SAM (all programs)')
        total_label(ws, r, 2, ''); total_label(ws, r, 3, '')
        for c in range(4, 7):
            total_cell(ws, r, c,
                       f'=SUM({get_column_letter(c)}{ft_c}:{get_column_letter(c)}{lt_c})')
        pct_total(ws, r, 7, 1.0)
        span_top_border(ws, r, 7)
        for rn in range(ft_c, lt_c + 1):
            wc(ws, rn, 7, f'=IFERROR(F{rn}/F${tr_c},0)', font=F_PCT, fmt=PCT_FMT)
```

- [ ] **Step 2: Commit**

```bash
git add build/build_from_data.py
git commit -m "Add MRO SAM section C — hull program breakdown"
```

---

### Task 4: Add Section C→D Bridge and Mekko (Section D)

**Files:**
- Modify: `build/build_from_data.py` — inside `create_mro_sam()`, after section C

- [ ] **Step 1: Add section C→D bridge — cost-element coverage gap**

This is where MRO diverges from Newbuild SAM. Instead of dropping hulls without P-5c, we drop ALL hulls (none have cost-element data). The bridge makes this explicit:

```python
    # ── (C→D) Bridge: All Programs → Cost-Element Coverage ──
    if hull_nz and tr_c:
        r += 3
        subsec_band(ws, r, '(C→D) Bridge: All Programs → Cost-Element Coverage', 2)
        r += 1; bridge2_first = r
        wc(ws, r, 1, 'MRO SAM (all programs)', font=F_DATA)
        wc(ws, r, 2, f'=F{tr_c}', font=F_DATA, fmt=NUM_FMT)
        for hl in hull_nz:
            r += 1
            vt_label = d['hull_type'].get(hl, '')
            svc_label = d['hull_svc'].get(hl, '')
            svc_tag = f', {svc_label}' if svc_label == 'USCG' else ''
            wc(ws, r, 1, f'  Less: {hl} ({vt_label}{svc_tag} — no P-5c)', font=F_DATA)
            wc(ws, r, 2, f'=-({cf_inner("JB_B,2", f"""JB_H,"{hl}" """.strip())}+{cf_inner("JB_B,4", f"""JB_H,"{hl}" """.strip())})',
               font=F_DATA, fmt=NUM_FMT)
        r += 1; _cost_elem_row = r
        total_label(ws, r, 1, 'MRO SAM (cost-element coverage)')
        total_cell(ws, r, 2, f'=SUM(B{bridge2_first}:B{r-1})')
        span_top_border(ws, r, 2)
```

Note: `_cost_elem_row` is where the sticky note will anchor (row tracking for annotation in Task 5).

- [ ] **Step 2: Add section D — Mekko at hull level**

The mekko table uses hull granularity (not vessel type like the old section C). SDM vs Modernization percentages by hull program:

```python
    # ── (D) MRO SAM — SDM vs Modernization by Hull (Mekko) ──
    mk = svc_order(hull_nz, d['hull_svc'])
    mk_nz = [h for h in mk
             if (d['mro_hull'].get(h, {}).get('2', 0)
                 + d['mro_hull'].get(h, {}).get('4', 0)) > 0]
    if mk_nz:
        r += 3
        subsec_band(ws, r,
                    '(D) MRO SAM — SDM vs Modernization by Hull (Mekko)',
                    2 + len(mk_nz))
        r += 1; svc_r = r
        mk_nz, n_usn, n_cg = write_svc_header(ws, r, mk_nz, d['hull_svc'],
                                                col_start=2)
        r += 1
        wc(ws, r, 1, 'Work Type', font=F_HDR, border=B_HDR); cw(ws, 1, 30)
        for i, hl in enumerate(mk_nz):
            c = 2 + i
            wc(ws, r, c, hl, font=F_HDR, border=B_HDR); cw(ws, c, 12)
        tc = 2 + len(mk_nz)
        wc(ws, r, tc, 'Total', font=F_HDR, border=B_HDR); cw(ws, tc, 12)
        sr = r + 1; mr = r + 2; tkr = r + 3

        wc(ws, tkr, 1, 'Total ($K)', font=F_TOTAL, border=B_TOT)
        for i, hl in enumerate(mk_nz):
            c = 2 + i
            parts = (cf_inner('JB_B,2', f'JB_H,"{hl}"') + '+'
                     + cf_inner('JB_B,4', f'JB_H,"{hl}"'))
            total_cell(ws, tkr, c, '=' + parts)
        total_cell(ws, tkr, tc,
                   f'=SUM({get_column_letter(2)}{tkr}:'
                   f'{get_column_letter(tc-1)}{tkr})')

        tcl = get_column_letter(tc)
        wc(ws, sr, 1, 'Scheduled Depot Maintenance', font=F_DATA)
        for i, hl in enumerate(mk_nz):
            c = 2 + i; cl = get_column_letter(c)
            wc(ws, sr, c,
               f'=IFERROR(({cf_inner("JB_B,2", f"""JB_H,"{hl}" """.strip())})'
               f'/{cl}${tkr},0)',
               font=F_PCT, fmt=PCT_FMT)
        wc(ws, sr, tc, f'=IFERROR(1-{tcl}{mr},0)', font=F_PCT, fmt=PCT_FMT)

        wc(ws, mr, 1, 'Modernization', font=F_DATA)
        for i, hl in enumerate(mk_nz):
            c = 2 + i; cl = get_column_letter(c)
            wc(ws, mr, c,
               f'=IFERROR(({cf_inner("JB_B,4", f"""JB_H,"{hl}" """.strip())})'
               f'/{cl}${tkr},0)',
               font=F_PCT, fmt=PCT_FMT)
        mod_parts = '+'.join(
            cf_inner('JB_B,4', f'JB_H,"{hl}"') for hl in mk_nz)
        wc(ws, mr, tc,
           f'=IFERROR(({mod_parts})/{tcl}${tkr},0)',
           font=F_PCT, fmt=PCT_FMT)

        span_top_border(ws, tkr, tc)
        apply_group_borders(ws, svc_r, tkr, 2, n_usn, n_cg)

    finish_sheet(ws)
    return {'bridge_cd_row': _cost_elem_row if hull_nz and tr_c else None,
            'mc': mc}
```

Note the return dict now includes `bridge_cd_row` for sticky note anchoring.

- [ ] **Step 3: Commit**

```bash
git add build/build_from_data.py
git commit -m "Add MRO SAM sections C→D bridge and hull-level mekko"
```

---

### Task 5: Add Sticky Note Annotation

**Files:**
- Modify: `build/build_from_data.py:1826-1872` — the annotation block in `main()`

- [ ] **Step 1: Update `create_mro_sam()` call to capture return value**

In `main()`, the existing call (line ~1771) is:

```python
create_mro_sam(*args, mro_tam_info=mro_tam_info)
```

Change to:

```python
mro_sam_info = create_mro_sam(*args, mro_tam_info=mro_tam_info)
```

Also capture FY26 MRO SAM info like we do for Newbuild SAM info. After the `if prefix == 'FY26':` block (line ~1780), add:

```python
if prefix == 'FY26':
    fy26_sam_info = sam_info
    fy26_detail_info = detail_info
    fy26_mro_sam_info = mro_sam_info
```

Initialize `fy26_mro_sam_info = None` alongside `fy26_sam_info` (line ~1741).

- [ ] **Step 2: Add MRO SAM sticky note**

In the annotations block (after the existing Newbuild SAM annotations, before `if annotations:`), add:

```python
    if fy26_mro_sam_info and fy26_mro_sam_info.get('bridge_cd_row'):
        cd_row = fy26_mro_sam_info['bridge_cd_row'] - 1  # 0-based
        annotations.append({
            'sheet': 'FY26 MRO SAM',
            'from_col': 3, 'from_row': cd_row - 2,
            'to_col': 9, 'to_row': cd_row + 16,
            'lines': [
                '**MRO Cost-Element Coverage**',
                '',
                'P-5c / P-8a cost-element breakdowns do not',
                'exist for MRO work. Justification books do',
                'not provide Electronics / HM&E / Ordnance',
                'splits for maintenance the way they do for',
                'new construction.',
                '',
                '**What DOES exist as alternative detail:**',
                '',
                'For SDM (Bucket 2): hull-level totals, plus',
                'ALT_VIEW data by availability type (OH, SRA,',
                'SIA, PIA) and by public shipyard (NNSY,',
                'PSNSY, etc.) with performance data (labor /',
                'material / contracts) — but these cover ALL',
                'vessels at those yards, not just SAM-eligible.',
                '',
                'For Mod (Bucket 4): some hulls have identified',
                'OPN line items (DDG Mod, LCS In-Service Mod,',
                'DDG-1000 Support Equipment) plus fleet-wide',
                'systems without hull attribution (CANES,',
                'AN/SLQ-32, ISSP, etc.).',
            ],
        })
```

- [ ] **Step 3: Commit**

```bash
git add build/build_from_data.py
git commit -m "Add sticky note annotation for MRO SAM cost-element gap"
```

---

### Task 6: Update Validation Sheet MRO SAM Definition

**Files:**
- Modify: `build/validation_sheet.py:87-90` — MRO SAM definition text

- [ ] **Step 1: Update MRO SAM definition**

Replace the current MRO SAM tuple (lines 87-90) with:

```python
        ('MRO SAM',
         'MRO TAM narrowed to outsourceable work types (scheduled depot maintenance and '
         'modernization/alteration installation) and outsourceable vessel types (excludes '
         'Submarines, Aircraft Carriers & UUVs). Sized at hull-program level. '
         'Cost-element coverage (P-5c/P-8a) is not available for MRO work — '
         'justification books do not break maintenance spending by Electronics / HM&E / '
         'Ordnance the way they do for new construction.'),
```

- [ ] **Step 2: Commit**

```bash
git add build/validation_sheet.py
git commit -m "Update MRO SAM definition in validation sheet"
```

---

### Task 7: Build, Verify, Commit

- [ ] **Step 1: Run the build**

```bash
cd /Users/brendantoole/projects2/buildco3 && python3 build/build_from_data.py
```

Expected output includes:
```
  MRO SAM hulls: 15
```
And no errors/tracebacks.

- [ ] **Step 2: Verify the output in Python**

```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('output/08APR2028_Newbuild_and_MRO_Spend_v5.34.xlsx', data_only=True)
ws = wb['FY26 MRO SAM']
for r in range(1, ws.max_row + 1):
    vals = []
    for c in range(1, min(ws.max_column + 1, 10)):
        v = ws.cell(r, c).value
        if v is not None:
            vals.append(f'c{c}={repr(v)[:70]}')
    if vals:
        print(f'R{r}: {chr(10).join(\"  \" + v for v in vals)}')
"
```

Verify:
- Row 1: title band "MRO SAM — FY2026 ($K)"
- Row 2: updated purpose text
- Section (A): Bridge with 3 vessel-type exclusions + non-outsourceable
- Section (B): Vessel types with SDM/Mod/Total/% columns
- Section (C): **New** — hull programs (DDG, LCS, LHD, etc.) with SDM/Mod/Total/%
- Section (C→D): **New** — bridge showing all hulls drop off for cost-element coverage
- Section (D): **New** — mekko with hull-level columns

- [ ] **Step 3: Open in Excel and inspect**

Tell user to open the output file and check:
1. Section (C) hull programs sum to same total as section (B) vessel types
2. Section (C→D) bridge arrives at $0 for cost-element coverage
3. Sticky note is visible near the bridge section
4. Mekko section (D) has hull-level columns with USN/USCG grouping
5. FY27 MRO SAM also has the new structure (but may have fewer hulls)
