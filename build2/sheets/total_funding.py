"""
total_funding.py — Total Funding sheet builder.
"""

from build2.config import TAM_EXCLUDED_CATEGORIES, BUCKET_NAMES
from build2.styles import F_DATA, F_GRAY, F_KPI, BG_TEAL, NUM_FMT
from build2.helpers import (
    title_band, subsec_band, purpose_row, hdr_row, wc,
    total_label, total_cell, span_top_border, finish_sheet,
)


def create_total_funding(wb, d, label, prefix, cf, cf_neg, cf_inner):
    ws = wb.create_sheet(f'{prefix} Total Funding')
    mc = 3

    r = 1; title_band(ws, r, 'Total Funding', mc)
    if prefix == 'FY27':
        r = 2; purpose_row(ws, r,
            f'All USN, MSC & USCG budget authority for any type of work on any type of vessel — '
            f'from new construction through depot maintenance, modernization, sustainment, and end-of-life. '
            f'Includes line items that lack vessel type or work type attribution. '
            f'{label} budget request — detailed justification books not yet released, program-level visibility only. ($K)')
    else:
        r = 2; purpose_row(ws, r,
            f'All USN, MSC & USCG budget authority for any type of work on any type of vessel — '
            f'from new construction through depot maintenance, modernization, sustainment, and end-of-life. '
            f'Includes line items that lack vessel type or work type attribution. {label} ($K)')

    # (A) By Work Type
    r = 4; subsec_band(ws, r, f'(A) {label} Total Funding by Work Type', 2)
    r += 1; hdr_row(ws, r, [('Work Type', 30), (f'{label} ($K)', 12)])
    first_data = r + 1
    for b in ['1', '2', '3', '4', '5', '6', '7']:
        r += 1; wc(ws, r, 1, BUCKET_NAMES[b], font=F_DATA)
        wc(ws, r, 2, cf(f'JB_B,{b}'), font=F_DATA, fmt=NUM_FMT)
    r += 1; total_label(ws, r, 1, 'Total'); total_cell(ws, r, 2, f'=SUM(B{first_data}:B{r-1})')
    span_top_border(ws, r, 2)

    # (B) By Vessel Category
    r += 3; subsec_band(ws, r, f'(B) {label} Total Funding by Vessel Category', 3)
    r += 1; hdr_row(ws, r, [('Category', 30), (f'{label} ($K)', 12), ('TAM Scope', 18)])
    cats = [
        ('Combatant Ships',            'YES \u2192 TAM'),
        ('Auxiliary Ships',             'YES \u2192 TAM'),
        ('Cutters',                     'YES \u2192 TAM'),
        ('Unmanned Maritime Platforms',  'YES \u2192 TAM'),
        ('Combatant Crafts',            'No \u2014 small craft'),
        ('Support Crafts',              'No \u2014 non-oceangoing'),
        ('Boats',                       'No \u2014 under 65 ft'),
    ]
    tam_rows = []; first = r + 1
    for cat, scope in cats:
        r += 1; wc(ws, r, 1, cat, font=F_DATA)
        wc(ws, r, 2, cf(f'JB_V,"{cat}"'), font=F_DATA, fmt=NUM_FMT)
        wc(ws, r, 3, scope, font=F_GRAY)
        if 'YES' in scope: tam_rows.append(r)
    r += 1; wc(ws, r, 1, 'Unattributed (fleet-wide)', font=F_DATA)
    wc(ws, r, 2, cf('JB_V,""'), font=F_DATA, fmt=NUM_FMT)
    wc(ws, r, 3, 'No \u2014 not vessel-specific', font=F_GRAY)
    r += 1; total_label(ws, r, 1, 'Total'); total_cell(ws, r, 2, f'=SUM(B{first}:B{r-1})')
    span_top_border(ws, r, 3)
    r += 1; wc(ws, r, 1, 'TAM-eligible', font=F_KPI, fill=BG_TEAL)
    wc(ws, r, 2, '=' + '+'.join(f'B{tr}' for tr in tam_rows), font=F_KPI, fill=BG_TEAL, fmt=NUM_FMT)

    # (C) By Source Book
    r += 3; subsec_band(ws, r, f'(C) {label} Total Funding by Source Book', 2)
    r += 1; hdr_row(ws, r, [('Source Book', 30), (f'{label} ($K)', 12)]); fs = r + 1
    for s in d['sources']:
        r += 1; wc(ws, r, 1, s, font=F_DATA)
        wc(ws, r, 2, cf(f'JB_A,"{s}"'), font=F_DATA, fmt=NUM_FMT)
    r += 1; total_label(ws, r, 1, 'Total'); total_cell(ws, r, 2, f'=SUM(B{fs}:B{r-1})')
    span_top_border(ws, r, 2)

    finish_sheet(ws)
