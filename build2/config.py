"""
config.py — Constants, taxonomy, and fiscal-year configuration.
"""

import re
import glob
import os
import shutil

# ── Output configuration ─────────────────────────────────────

WORKBOOK_SRC = 'build2/data_v2.xlsx'
VALIDATION_SRC = 'build2/validation_sheet.xlsx'
OUTPUT_DIR = 'output'
FILE_PREFIX = '08APR2028_Newbuild_and_MRO_Spend'
VERSION_MAJOR = 5

ARCHIVE_DIR = f'{OUTPUT_DIR}/archive'


def next_output_path():
    """Scan output/ for existing v{MAJOR}.x files, archive the previous minor
    version if present, and return the next version path."""
    pattern = re.compile(rf'{re.escape(FILE_PREFIX)}_v{VERSION_MAJOR}\.(\d+)\.xlsx$')
    max_minor = -1
    for path in glob.glob(f'{OUTPUT_DIR}/{FILE_PREFIX}_v{VERSION_MAJOR}.*.xlsx'):
        m = pattern.search(path)
        if m:
            max_minor = max(max_minor, int(m.group(1)))
    next_minor = max_minor + 1

    if next_minor >= 1:
        prev = f'{OUTPUT_DIR}/{FILE_PREFIX}_v{VERSION_MAJOR}.{next_minor - 1}.xlsx'
        if os.path.exists(prev):
            os.makedirs(ARCHIVE_DIR, exist_ok=True)
            dest = f'{ARCHIVE_DIR}/{os.path.basename(prev)}'
            shutil.move(prev, dest)
            print(f'Archived: {prev} → {dest}')

    return f'{OUTPUT_DIR}/{FILE_PREFIX}_v{VERSION_MAJOR}.{next_minor}.xlsx'


# Sheets that are hand-built data — never touched by this script
BASE_SHEETS = {'J Book Items Cons.', 'Notes'}


# ── Fiscal year configurations ───────────────────────────────

FY_CONFIGS = [
    {
        'label': 'FY2026',
        'prefix': 'FY26',
        'named_ranges': [('JB_R', 'Y'), ('JB_N', 'U'), ('JB_L', 'S')],
        'best_value_range': 'JB_26BV',
        'read_indices': [24, 20, 18],
        'best_value_formula': 'IF(Y{r}<>"",Y{r},IF(U{r}<>"",U{r},S{r}))',
        'tab_color': '4472C4',
    },
    {
        'label': 'FY2027',
        'prefix': 'FY27',
        'named_ranges': [('JB_27U', 'AB'), ('JB_27S', 'Z')],
        'best_value_range': 'JB_27BV',
        'read_indices': [27, 25],
        'best_value_formula': 'IF(AB{r}<>"",AB{r},Z{r})',
        'tab_color': '548235',
    },
]


# ── Taxonomy ─────────────────────────────────────────────────

TAM_CATEGORIES = {'Combatant Ships', 'Auxiliary Ships', 'Cutters', 'Unmanned Maritime Platforms'}
TAM_EXCLUDED_CATEGORIES = ['Combatant Crafts', 'Support Crafts']
SAM_EXCLUDED_TYPES = {'Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles'}

BUCKET_NAMES = {
    '1': 'New Construction', '2': 'Scheduled Depot Maintenance & Repair',
    '3': 'Continuous / Intermediate / Emergent Maintenance',
    '4': 'Modernization & Alteration Installation',
    '5': 'Major Life-Cycle Events / SLEP / MMA / RCOH',
    '6': 'Sustainment Engineering / Planning / Obsolescence Support',
    '7': 'Availability Support / Husbanding / Port Services',
}
BUCKET_SHORT = {
    '2': 'Scheduled Depot Maintenance', '3': 'Continuous / Emergent Maintenance',
    '4': 'Modernization', '5': 'Major Life-Cycle Events / RCOH',
    '6': 'Sustainment Engineering', '7': 'Availability Support',
}
MRO_BKTS = ['2', '3', '4', '5', '6', '7']


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
