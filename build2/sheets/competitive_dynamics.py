"""
competitive_dynamics.py — Competitive Dynamics sheet builder + hardcoded data tables.
"""

from build2.styles import (
    F_DATA, F_HDR, F_SUBSUBSEC, F_GRAY, F_BLUE, F_TOTAL,
    BG_GRAY, B_HDR, NUM_FMT, NOWRAP,
)
from build2.helpers import (
    cw, wc, title_band, subsec_band, purpose_row, hdr_row,
    total_label, total_cell, span_top_border, finish_sheet,
)


# ── Data tables ──────────────────────────────────────────────

PRIMES = [
    (1, 'Huntington Ingalls Industries', 'HII', 22000000, 'DDG-51 $11.4B, LPD $4.7B, LHA $4.5B, DDG-1000 $0.3B, depot'),
    (2, 'Raytheon / RTX', 'RTX Corp', 13700000, 'Standard Missile $5.7B, SPY-6 $3.5B, CIWS/RAM $2.0B, DDG-1000 $0.9B, CEC $0.6B'),
    (3, 'Bath Iron Works', 'General Dynamics', 8800000, 'DDG-51 FY23-27 $5.0B, FY18-22 $3.3B, FY13-17 $0.5B, DDG-1000 $0.2B'),
    (4, 'BAE Systems', 'BAE Systems plc', 5000000, 'DDG/LHD/LPD/LSD/CG depot maintenance — Norfolk, San Diego, Jacksonville, Hawaii'),
    (5, 'Lockheed Martin', 'LM', 1500000, 'SLQ-32(V)6 $0.8B, SSDS $0.4B, HELIOS $0.1B, LCS Freedom $0.3B'),
    (6, 'Metro Machine Corp', '--', 700000, 'LHD/DDG/LSD depot maintenance — Norfolk'),
    (7, 'NASSCO', 'General Dynamics', 600000, 'LHA/LHD/LSD/DDG/CG depot maintenance — San Diego'),
    (8, 'Vigor Marine LLC', '--', 500000, 'DDG/CG depot maintenance — Portland, OR'),
    (9, 'Northrop Grumman Systems', 'NG', 487000, 'Knifefish/LCS $0.35B, SEWIP Block 3 $0.14B, ALMDS $0.07B'),
    (10, 'QED Systems', '--', 300000, 'Third-party planning DDG/CG/LPD/LHD'),
    (11, 'Continental Maritime', '--', 300000, 'DDG depot — San Diego'),
    (12, 'Textron Systems', 'Textron', 242000, 'UISS $0.24B'),
    (13, 'Advanced Technology International', '--', 235000, 'OTA consortium: MK-54 MOD 2, SPY-6 prototype, HEL, LHD midlife'),
    (14, 'General Dynamics Mission Systems', 'General Dynamics', 210000, 'MK-54 MOD 1 $0.12B, Knifefish Block 1 $0.08B'),
    (15, 'SAIC', 'SAIC', 200000, 'DDG-1000 engineering, SSTD Nixie, torpedo defense'),
    (16, 'Marine Hydraulics International', '--', 200000, 'DDG/LSD depot + sub-prime on LHD primes'),
    (17, 'Bollinger Shipyards', 'Bollinger', 116000, 'MCM USV production'),
    (18, 'Ultra Electronics Ocean Systems', 'Ultra', 68000, 'MK 54 MOD 0 array kits + Nixie production'),
    (19, 'Penn State Applied Research Lab', 'Penn State', 60000, 'MK-54 MOD 2 engineering, HEL development'),
]

SUBS = [
    (1, 'Fincantieri (Marinette Marine)', 2487000, 2, 1, 'LCS Freedom hull builder — actual constructor under LM prime'),
    (2, 'Timken Gears & Services', 516000, 22, 20, 'DDG/LHD/CG propulsion gearing'),
    (3, 'General Dynamics (rolled up)', 432000, 23, 14, 'GD Mission Systems $359M on SPY-6, GD-OTS, GDIT'),
    (4, 'L3Harris (Aerojet Rocketdyne)', 378000, 4, 4, 'Solid rocket motors for Standard Missile family'),
    (5, 'Rolls-Royce', 313000, 25, 25, 'Gas turbines, waterjets, gearing — DDG/LCS/LPD/LHA + depot'),
    (6, 'CAES (Cobham)', 217000, 10, 8, 'RF assemblies on SPY-6 $170M, SEWIP $110M, SLQ-32 $95M'),
    (7, 'Northrop Grumman (as sub)', 215000, 10, 9, 'SPY-6 RF $114M, CIWS, LPD/LHA construction'),
    (8, 'IMIA', 204000, 28, 28, 'Hull coatings / paint across 28 depot availabilities'),
    (9, 'L3Harris (excl. Aerojet)', 203000, 53, 45, 'Maritime Power, Cincinnati Electronics, Fuzing — broadest footprint'),
    (10, 'Johnson Controls (incl. York)', 172000, 31, 24, 'HVAC / chilled water on DDG/LPD/LHA + depot'),
    (11, 'GE Aerospace', 166000, 16, 14, 'LM2500 gas turbines on DDG-51 + GE Power Conversion LHA 9'),
    (12, 'Fairbanks Morse Defense', 161000, 25, 18, 'Diesel generators / propulsion on LPD/LHA + depot rebuilds'),
    (13, 'Leonardo DRS', 134000, 18, 15, 'Naval Power Systems, Network & Imaging, Laurel Technologies'),
    (14, 'Sparton DeLeon Springs', 108000, 2, 2, 'ASW sensors / payload on Raytheon Barracuda'),
    (15, 'RAM-System GmbH', 98000, 1, 1, 'RAM missile co-development with Raytheon (Germany)'),
    (16, 'Bay Metals & Fabrication', 93000, 9, 9, 'Norfolk metal fab serving 9 depot availabilities'),
    (17, 'US Joiner LLC', 88000, 12, 12, 'Interior outfitting — LPD construction + depot'),
    (18, 'United Rentals', 77000, 29, 29, 'Equipment rental across 29 depot availabilities'),
    (19, 'Honeywell', 71000, 12, 12, 'IMUs / IRUs on Standard Missile + CIWS'),
    (20, 'Anaren', 64000, 7, 7, 'RF combiners/dividers on SPY-6'),
]

PROGRAMS = [
    ('DDG-51 New Construction', 530000, 'GE Aerospace $88M', 'Johnson Controls $76M', 'Timken Gears $41M'),
    ('DDG Mod — SPY-6', 1220000, 'GD Mission Systems $359M', 'CAES $170M', 'Northrop Grumman $114M'),
    ('DDG Mod — CIWS/RAM/SeaRAM', 560000, 'RAM-System GmbH $98M', 'L3Harris $39M', 'GD $35M'),
    ('LCS Freedom Construction', 2910000, 'Marinette Marine $2,487M', 'Rolls-Royce $196M', 'Airbus US $56M'),
    ('LCS MCM Mission Modules', 1230000, 'Trident Sensors $215M', 'Teledyne $55M', 'GD $13M'),
    ('LHA New Construction', 340000, 'Fairbanks Morse $40M', 'L3Harris $39M', 'Leonardo DRS $34M'),
    ('LPD Flight II New Construction', 340000, 'Fairbanks Morse $65M', 'US Joiner $36M', 'Caterpillar $20M'),
    ('Standard Missile Family', 930000, 'L3Harris (Aerojet) $390M', 'Honeywell $43M', 'Goodrich $32M'),
    ('DDG-1000', 130000, 'Red River Technology $61M', 'Air Masters $6M', '--'),
    ('DDG Mod — CEC', 30000, 'Sechan Electronics $7M', 'Action Electronics $5M', '--'),
    ('DDG Mod — SSDS', 40000, 'Mission Solutions $14M', 'PMAT $6M', '--'),
    ('DDG Mod — HELIOS', 60000, 'MZA Associates $25M', 'L3 Technologies $22M', '--'),
    ('Airborne MCM', 150000, 'Sparton $108M', 'Teledyne $17M', '--'),
    ('MK-54 Torpedo', 30000, 'L3Harris (Aerojet) $25M', 'J&E Precision Tool $3M', '--'),
    ('Depot Maintenance', 1500000, 'IMIA $204M', 'Bay Metals $93M', 'US Joiner $88M'),
]

CROSSWALK = {
    'LHD': [
        ('OMN_Vol2 LHD/AMPHIBS depot', 346443, 'BAE Norfolk/SD, Metro Machine, NASSCO'),
        ('OMN_Vol2 LHD/AMPHIBS modernization', 631859, 'BAE Norfolk/SD, Metro Machine'),
        ('OPN BA1 Line 8 LHA/LHD Midlife', 123384, 'BAE / Metro / Gibbs & Cox'),
    ],
    'LPD': [
        ('SCN 3010 LPD Flight II procurement', 835037, 'HII — N0002424C2473 ($5.80B ceiling)'),
        ('SCN 3010 LPD Flight II AP', 275000, 'HII — N0002424C2473 AP scope'),
        ('OMN_Vol2 LPD depot', 149595, 'BAE Norfolk/SD'),
        ('OPN BA1 Line 15 LPD Class Support', 125542, 'HII Class Eng ($225M) + Raytheon LCE&S ($485M)'),
    ],
    'LSD': [
        ('OMN_Vol2 LSD depot', 94421, 'NASSCO, BAE, Metro Machine'),
        ('OMN_Vol2 LSD modernization', 25931, 'Alteration installation (small)'),
    ],
    'LHA': [
        ('SCN 3041 LHA Replacement', 634963, 'HII — N0002420C2437 LHA 9 ($3.14B ceiling)'),
        ('OMN_Vol2 LHA depot', 45012, 'NASSCO — LHA 6 DSRA ($198M ceiling)'),
    ],
    'DDG': [
        ('SCN 2122 DDG-51 procurement', 5410773, 'HII FY23-27 MYP + BIW FY23-27 MYP'),
        ('SCN 2122 DDG-51 AP', 1750000, 'HII + BIW — AP against FY23-27 MYPs'),
        ('SCN 2119 DDG-1000', 52358, 'HII Mod Planning + BIW Planning Yard'),
        ('OMN_Vol2 DDG depot', 952000, 'BAE / NASSCO / Continental / Vigor / MHI / Metro'),
        ('OMN_Vol2 DDG modernization', 1282612, 'Cross-vehicle alteration installation'),
        ('WPN 2234 Standard Missile', 1008875, 'Raytheon SM production vehicles'),
        ('OPN BA1 Line 5 DDG Mod', 878787, 'SPY-6, SEWIP, SSDS, CEC, CIWS, HELIOS, Aegis kits'),
        ('WPN 3215 MK-54 Torpedo Mods', 128513, 'GDMS MK 54 MOD 1 + Ultra MK 54 MOD 0 + ATI OTAs'),
        ('OPN BA1 Line 16 DDG-1000 Support', 115267, 'Raytheon DDG-1000 mission sys + BIW Planning Yard'),
    ],
    'LCS': [
        ('OMN_Vol2 LCS depot', 576389, 'LM Freedom ISEA + GDMS Independence ISEA + avails'),
        ('OMN_Vol2 LCS modernization', 383361, 'LM + GDMS combat system ISEA + ITT-2A'),
        ('OPN BA1 Line 37 LCS In-Service Mod', 189458, 'LM, GDMS, Textron, BAH PEO LCS support'),
        ('OPN BA1 Line 34 LCS MCM Modules', 91372, 'UISS (Textron), Knifefish (GDMS/NG), MCM USV (Bollinger)'),
        ('WPN 2292 Naval Strike Missile', 32238, 'Raytheon NSM integration + Kongsberg OEM via FMS'),
    ],
    'CG': [
        ('OMN_Vol2 CG depot', 115501, 'Vigor, BAE Norfolk, NASSCO, HII CG planning'),
        ('OMN_Vol2 CG modernization', 44940, 'Same vendor pool — alteration installation'),
    ],
}


# ── Sheet builder ────────────────────────────────────────────

def create_competitive_dynamics(wb):
    ws = wb.create_sheet('Competitive Dynamics')
    ws.sheet_properties.tabColor = '7B5B3A'

    cw(ws, 1, 30); cw(ws, 2, 16); cw(ws, 3, 12); cw(ws, 4, 26); cw(ws, 5, 26)

    r = 1; title_band(ws, r, 'Competitive Dynamics', 5)
    r = 2; purpose_row(ws, r, 'FY20-26 contract obligation analysis — primes, subcontractors, and FY26 vehicle crosswalk ($K)')

    # (A) Top Prime Contractors
    r = 4; subsec_band(ws, r, '(A) Top Prime Contractors — FY20-26 Window Obligation', 4)
    r += 1; hdr_row(ws, r, [('Contractor', 30), ('Parent', 16), ('Window ($K)', 12), ('Key Programs', 44)])
    ft = r + 1
    for rank, name, parent, val, programs in PRIMES:
        r += 1
        wc(ws, r, 1, name, font=F_DATA)
        wc(ws, r, 2, parent, font=F_GRAY)
        wc(ws, r, 3, val, font=F_BLUE, fmt=NUM_FMT)
        wc(ws, r, 4, programs, font=F_GRAY)
    r += 1; total_label(ws, r, 1, 'Total (top 19)')
    total_cell(ws, r, 3, f'=SUM(C{ft}:C{r-1})')
    span_top_border(ws, r, 4)

    # (B) Top Subcontractors
    r += 3; subsec_band(ws, r, '(B) Top Subcontractors — Hidden Supply Chain', 5)
    r += 1; hdr_row(ws, r, [('Parent Company', 30), ('Sub Total ($K)', 16), ('# Primes', 12), ('# PIIDs', 10), ('Primary Programs', 44)])
    ft = r + 1
    for rank, name, val, pairs, piids, programs in SUBS:
        r += 1
        wc(ws, r, 1, name, font=F_DATA)
        wc(ws, r, 2, val, font=F_BLUE, fmt=NUM_FMT)
        wc(ws, r, 3, pairs, font=F_BLUE, fmt=NUM_FMT)
        wc(ws, r, 4, piids, font=F_BLUE, fmt=NUM_FMT)
        wc(ws, r, 5, programs, font=F_GRAY)
    r += 1; total_label(ws, r, 1, 'Total (top 20)')
    total_cell(ws, r, 2, f'=SUM(B{ft}:B{r-1})')
    span_top_border(ws, r, 5)

    # (C) Per-Program Subaward Summary
    r += 3; subsec_band(ws, r, '(C) Per-Program Subaward Summary', 5)
    r += 1; hdr_row(ws, r, [('Program', 30), ('Total Subs ($K)', 16), ('Top Sub 1', 26), ('Top Sub 2', 26), ('Top Sub 3', 26)])
    ft = r + 1
    for prog, val, s1, s2, s3 in PROGRAMS:
        r += 1
        wc(ws, r, 1, prog, font=F_DATA)
        wc(ws, r, 2, val, font=F_BLUE, fmt=NUM_FMT)
        wc(ws, r, 3, s1, font=F_GRAY)
        wc(ws, r, 4, s2, font=F_GRAY)
        wc(ws, r, 5, s3, font=F_GRAY)
    r += 1; total_label(ws, r, 1, 'Total')
    total_cell(ws, r, 2, f'=SUM(B{ft}:B{r-1})')
    span_top_border(ws, r, 5)

    # (D) FY26 Contract Vehicle Crosswalk
    r += 3; subsec_band(ws, r, '(D) FY2026 SAM Line Item to Contract Vehicle Crosswalk', 3)

    for hull, lines in CROSSWALK.items():
        r += 2
        for c in range(1, 4):
            cell = ws.cell(row=r, column=c)
            cell.fill = BG_GRAY; cell.alignment = NOWRAP
        wc(ws, r, 1, hull, font=F_SUBSUBSEC, fill=BG_GRAY)

        r += 1; hdr_row(ws, r, [('FY26 SAM Line', 30), ('FY26 ($K)', 16), ('Contract Vehicle / Prime', 44)])
        ft = r + 1
        for line, val, vehicle in lines:
            r += 1
            wc(ws, r, 1, line, font=F_DATA)
            wc(ws, r, 2, val, font=F_BLUE, fmt=NUM_FMT)
            wc(ws, r, 3, vehicle, font=F_GRAY)
        r += 1; total_label(ws, r, 1, f'{hull} Total')
        total_cell(ws, r, 2, f'=SUM(B{ft}:B{r-1})')
        span_top_border(ws, r, 3)

    finish_sheet(ws)
