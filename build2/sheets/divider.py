"""
divider.py — FY divider tab (e.g. "FY2026 >>").
"""

from build2.styles import F_TITLE, BG_BLACK, ROW_HEIGHT
from build2.helpers import band


def create_divider(wb, label, tab_color):
    """Create a minimal divider tab for a fiscal year group."""
    name = f'{label} >>'
    ws = wb.create_sheet(name)
    ws.sheet_properties.tabColor = tab_color
    band(ws, 1, 6, label, F_TITLE, BG_BLACK)
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = ROW_HEIGHT
    return name
