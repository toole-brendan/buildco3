#!/usr/bin/env python3
"""
Cross-PIID subaward aggregator with parent-company normalization.

Reads subaward_full.json (corrected per-sub_id dedup), rolls up by:
  1. Raw recipient name
  2. Normalized vendor (suffix-stripped)
  3. Parent company (manually-curated mappings for the top players)

Outputs:
  - Hidden tier ranking by parent company across all in-scope PIIDs
  - Per-program rollups (DDG construction, LPD/LHA, depot, mod, weapons)
  - Top sub by individual prime PIID
"""

import json
import os
import re
import sys
from collections import defaultdict

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_full.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_aggregated.json")

# ----------------------------------------------------------------------
# Vendor normalization: strip legal-entity suffixes
# ----------------------------------------------------------------------
SUFFIX_RE = re.compile(
    r"\b(INC\.?|L\.?L\.?C\.?|CORP\.?|CORPORATION|CO\.?|LTD\.?|LP|L\.P\.|"
    r"COMPANY|HOLDINGS|GROUP|PARTNERSHIP|LIMITED)\b\.?,?\s*$",
    re.IGNORECASE,
)


def normalize(name):
    if not name:
        return None
    s = name.upper().strip()
    s = re.sub(r"[,.]\s*$", "", s)
    for _ in range(3):
        new = SUFFIX_RE.sub("", s).strip().rstrip(",.")
        if new == s:
            break
        s = new
    s = re.sub(r"\s+", " ", s)
    return s.strip() or None


# ----------------------------------------------------------------------
# Parent company mapping (manually curated for the top players)
# Maps normalized vendor name → parent company
# ----------------------------------------------------------------------
PARENT_MAP = {
    # General Dynamics family
    "GENERAL DYNAMICS": "General Dynamics",
    "GENERAL DYNAMICS MISSION SYSTEMS": "General Dynamics",
    "GENERAL DYNAMICS LAND SYSTEMS": "General Dynamics",
    "GENERAL DYNAMICS-OTS": "General Dynamics",
    "GENERAL DYNAMICS OTS": "General Dynamics",
    "GENERAL DYNAMICS INFORMATION TECHNOLOGY": "General Dynamics",
    "GENERAL DYNAMICS ADVANCED INFORMATION SYSTEMS": "General Dynamics",
    "GD MISSION SYSTEMS": "General Dynamics",
    "GD LAND SYSTEMS": "General Dynamics",
    "GD-OTS": "General Dynamics",
    "GDIT": "General Dynamics",
    "BATH IRON WORKS": "General Dynamics",
    "ELECTRIC BOAT": "General Dynamics",
    "GENERAL DYNAMICS ELECTRIC BOAT": "General Dynamics",
    "NATIONAL STEEL AND SHIPBUILDING": "General Dynamics",
    "NASSCO": "General Dynamics",

    # Raytheon / RTX family
    "RAYTHEON": "RTX (Raytheon)",
    "RAYTHEON COMPANY": "RTX (Raytheon)",
    "RTX": "RTX (Raytheon)",
    "RTX CORPORATION": "RTX (Raytheon)",
    "RTX BBN": "RTX (Raytheon)",
    "RTX BBN TECHNOLOGIES": "RTX (Raytheon)",

    # Lockheed Martin family
    "LOCKHEED MARTIN": "Lockheed Martin",
    "LOCKHEED MARTIN ACULIGHT": "Lockheed Martin",
    "LM ACULIGHT": "Lockheed Martin",
    "LOCKHEED MARTIN SIPPICAN": "Lockheed Martin",
    "LOCKHEED MARTIN SPACE": "Lockheed Martin",

    # Northrop Grumman
    "NORTHROP GRUMMAN": "Northrop Grumman",
    "NORTHROP GRUMMAN SYSTEMS": "Northrop Grumman",
    "NG SYSTEMS": "Northrop Grumman",
    "ATK LAUNCH SYSTEMS": "Northrop Grumman",  # acquired 2018
    "ORBITAL ATK": "Northrop Grumman",

    # BAE Systems
    "BAE SYSTEMS": "BAE Systems",
    "BAE SYSTEMS NORFOLK SHIP REPAIR": "BAE Systems",
    "BAE SYSTEMS SAN DIEGO SHIP REPAIR": "BAE Systems",
    "BAE SYSTEMS JACKSONVILLE SHIP REPAIR": "BAE Systems",
    "BAE SYSTEMS HAWAII SHIPYARDS": "BAE Systems",
    "BAE SYSTEMS LAND & ARMAMENTS": "BAE Systems",
    "BAE SYSTEMS INFORMATION AND ELECTRONIC": "BAE Systems",
    "EARL INDUSTRIES": "BAE Systems",  # acquired 2014, became BAE Norfolk

    # HII (Huntington Ingalls)
    "HUNTINGTON INGALLS": "Huntington Ingalls (HII)",
    "HUNTINGTON INGALLS INCORPORATED": "Huntington Ingalls (HII)",
    "HII INGALLS SHIPBUILDING": "Huntington Ingalls (HII)",
    "INGALLS SHIPBUILDING": "Huntington Ingalls (HII)",
    "HII SAN DIEGO SHIPYARD": "Huntington Ingalls (HII)",
    "HUNTINGTON INGALLS INDUSTRIES SAN DIEGO": "Huntington Ingalls (HII)",

    # Rolls-Royce
    "ROLLS-ROYCE MARINE NORTH AMERICA": "Rolls-Royce",
    "ROLLS-ROYCE SOLUTIONS AMERICA": "Rolls-Royce",
    "ROLLS ROYCE MARINE NORTH AMERICA": "Rolls-Royce",
    "ROLLS-ROYCE": "Rolls-Royce",
    "MTU DETROIT DIESEL": "Rolls-Royce",
    "MTU AMERICA": "Rolls-Royce",

    # L3Harris
    "L3 TECHNOLOGIES": "L3Harris",
    "L3HARRIS": "L3Harris",
    "L3 COMMUNICATIONS": "L3Harris",
    "L3HARRIS MARITIME POWER & ENERGY SOLUTIONS": "L3Harris",
    "L3HARRIS CINCINNATI ELECTRONICS": "L3Harris",
    "L3HARRIS FUZING & ORDNANCE SYSTEMS": "L3Harris",
    "L3HARRIS INTERSTATE ELECTRONICS": "L3Harris",
    "L-3 COMMUNICATIONS": "L3Harris",

    # Honeywell
    "HONEYWELL INTERNATIONAL": "Honeywell",
    "HONEYWELL": "Honeywell",

    # Johnson Controls (HVAC + York)
    "JOHNSON CONTROLS NAVY SYSTEMS": "Johnson Controls",
    "JOHNSON CONTROLS": "Johnson Controls",
    "YORK INTERNATIONAL": "Johnson Controls",

    # Coltec / Fairbanks Morse
    "COLTEC INDUSTRIES": "Fairbanks Morse Defense",
    "FAIRBANKS MORSE": "Fairbanks Morse Defense",
    "FAIRBANKS MORSE DEFENSE": "Fairbanks Morse Defense",

    # Curtiss-Wright
    "CURTISS-WRIGHT DS": "Curtiss-Wright",
    "CURTISS-WRIGHT ELECTRO-MECHANICAL": "Curtiss-Wright",
    "CURTISS-WRIGHT FLOW CONTROL": "Curtiss-Wright",
    "CURTISS-WRIGHT": "Curtiss-Wright",

    # DRS
    "DRS NAVAL POWER SYSTEMS": "Leonardo DRS",
    "DRS NETWORK & IMAGING SYSTEMS": "Leonardo DRS",
    "DRS LAUREL TECHNOLOGIES": "Leonardo DRS",
    "DRS SIGNAL SOLUTIONS": "Leonardo DRS",
    "DRS TECHNOLOGIES": "Leonardo DRS",
    "LAUREL TECHNOLOGIES": "Leonardo DRS",
    "LAUREL TECHNOLOGIES PARTNERSHIP": "Leonardo DRS",

    # Teledyne
    "TELEDYNE DEFENSE ELECTRONICS": "Teledyne",
    "TELEDYNE BROWN ENGINEERING": "Teledyne",
    "TELEDYNE INSTRUMENTS": "Teledyne",
    "TELEDYNE LIMITED": "Teledyne",
    "TELEDYNE": "Teledyne",

    # CAES (Cobham Advanced Electronic Solutions)
    "CAES SYSTEMS": "CAES (Cobham Advanced Electronic Solutions)",
    "CAES MISSION SYSTEMS": "CAES (Cobham Advanced Electronic Solutions)",
    "CAES": "CAES (Cobham Advanced Electronic Solutions)",
    "COBHAM ADVANCED ELECTRONIC SOLUTIONS": "CAES (Cobham Advanced Electronic Solutions)",

    # Mercury Systems
    "MERCURY SYSTEMS": "Mercury Systems",
    "MERCURY SYSTEMS - TRUSTED MISSION SOLUTIONS": "Mercury Systems",

    # Ultra Electronics
    "ULTRA ELECTRONICS OCEAN SYSTEMS": "Ultra (Cobham Ultra)",
    "ULTRA ELECTRONICS": "Ultra (Cobham Ultra)",

    # Boeing
    "THE BOEING COMPANY": "Boeing",
    "BOEING": "Boeing",
    "INSITU": "Boeing",

    # Microsoft
    "MICROSOFT CORPORATION": "Microsoft",
    "MICROSOFT": "Microsoft",

    # Marinette / Fincantieri
    "MARINETTE MARINE": "Fincantieri (Marinette Marine)",
    "MARINETTE": "Fincantieri (Marinette Marine)",
    "FINCANTIERI": "Fincantieri (Marinette Marine)",
    "FINCANTIERI MARINE": "Fincantieri (Marinette Marine)",

    # Aerojet Rocketdyne
    "AEROJET ROCKETDYNE": "L3Harris (Aerojet Rocketdyne)",  # acquired 2023

    # GE Aerospace / Aviation
    "GENERAL ELECTRIC": "GE Aerospace",
    "GE AVIATION SYSTEMS": "GE Aerospace",
    "GE": "GE Aerospace",
    "GE ENERGY POWER CONVERSION USA": "GE Aerospace",

    # Bollinger
    "BOLLINGER SHIPYARDS LOCKPORT": "Bollinger Shipyards",
    "BOLLINGER MISSISSIPPI SHIPBUILDING": "Bollinger Shipyards",
    "BOLLINGER": "Bollinger Shipyards",

    # Textron
    "TEXTRON SYSTEMS": "Textron",
    "TEXTRON": "Textron",
    "AAI": "Textron",

    # Booz Allen
    "BOOZ ALLEN HAMILTON": "Booz Allen Hamilton",
    "BOOZ ALLEN": "Booz Allen Hamilton",

    # SAIC
    "SCIENCE APPLICATIONS INTERNATIONAL": "SAIC",
    "SAIC": "SAIC",

    # Leidos
    "LEIDOS": "Leidos",
    "DYNETICS": "Leidos",  # Dynetics is a Leidos subsidiary

    # ManTech
    "MANTECH": "ManTech (Carlyle Group)",
    "MANTECH ADVANCED SYSTEMS INTL": "ManTech (Carlyle Group)",

    # Parker Hannifin
    "PARKER HANNIFIN": "Parker Hannifin",
    "PARKER-HANNIFIN": "Parker Hannifin",

    # Caterpillar
    "CATERPILLAR": "Caterpillar",
    "CAT": "Caterpillar",

    # Moog
    "MOOG": "Moog",
    "MOOG INDUSTRIAL CONTROLS": "Moog",
    "MOOG INC": "Moog",

    # Penn State APL
    "PENNSYLVANIA STATE UNIVERSITY": "Penn State (FFRDC)",
    "PENN STATE": "Penn State (FFRDC)",
    "THE PENNSYLVANIA STATE UNIVERSITY": "Penn State (FFRDC)",

    # JHU APL
    "JOHNS HOPKINS UNIVERSITY APPLIED PHYSICS LAB": "JHU APL (FFRDC)",
    "JHU APL": "JHU APL (FFRDC)",
    "JHU APPLIED PHYSICS LAB": "JHU APL (FFRDC)",
    "JOHNS HOPKINS UNIVERSITY": "JHU APL (FFRDC)",

    # Bechtel
    "BECHTEL": "Bechtel",
    "BECHTEL PLANT MACHINERY": "Bechtel",

    # BWXT
    "BWX TECHNOLOGIES": "BWXT",
    "BWXT NUCLEAR OPERATIONS GROUP": "BWXT",
    "BWXT": "BWXT",

    # Smiths
    "SMITHS INTERCONNECT": "Smiths Group",
    "SMITHS": "Smiths Group",
}


def parent_of(normalized_name):
    """Map a normalized vendor name to a parent company. Falls back to
    the normalized name itself if no mapping exists."""
    if not normalized_name:
        return None
    # Direct match
    if normalized_name in PARENT_MAP:
        return PARENT_MAP[normalized_name]
    # Substring match -- check if any key is a prefix of the normalized name
    for key in PARENT_MAP:
        if normalized_name.startswith(key + " ") or normalized_name == key:
            return PARENT_MAP[key]
    return normalized_name  # itself as the "parent"


# ----------------------------------------------------------------------
# Section grouping for per-program rollups
# ----------------------------------------------------------------------
def get_section(label):
    """Group section labels into broad program areas."""
    label = (label or "").upper()
    if "DDG-51 NEW CONSTRUCTION" in label:
        return "DDG-51 New Construction"
    if "DDG-1000" in label:
        return "DDG-1000"
    if "LPD" in label and "FLIGHT II" in label:
        return "LPD Flight II New Construction"
    if "LHA REPLACEMENT" in label:
        return "LHA Replacement New Construction"
    if "LCS FREEDOM" in label:
        return "LCS Freedom (legacy construction)"
    if label.startswith("DDG MOD"):
        if "SPY-6" in label:
            return "DDG Mod - SPY-6"
        if "SEWIP" in label:
            return "DDG Mod - SEWIP"
        if "SSDS" in label:
            return "DDG Mod - SSDS"
        if "CEC" in label:
            return "DDG Mod - CEC"
        if "CIWS" in label:
            return "DDG Mod - CIWS/RAM/SeaRAM"
        if "HELIOS" in label:
            return "DDG Mod - HELIOS"
        return "DDG Mod - Other"
    if label.startswith("STANDARD MISSILE"):
        return "Standard Missile family"
    if label.startswith("MK-54"):
        return "MK-54 Torpedo"
    if label.startswith("SHIP GUN"):
        return "Ship Gun Systems"
    if label.startswith("AIRBORNE MCM"):
        return "Airborne MCM (ALMDS/AMNS/Barracuda)"
    if label.startswith("LCS MCM"):
        return "LCS MCM Mission Modules"
    if label.startswith("DEPOT"):
        return "Depot Maintenance"
    return "Other"


def main():
    if not os.path.exists(IN):
        print(f"Input file not found: {IN}", file=sys.stderr)
        sys.exit(1)

    with open(IN) as f:
        data = json.load(f)

    print(f"Loaded {len(data)} PIIDs from {IN}\n")

    # Cross-PIID aggregation by parent company
    parent_totals = defaultdict(lambda: {"amount": 0.0, "subs": 0, "piids": set()})
    section_parent_totals = defaultdict(lambda: defaultdict(lambda: {"amount": 0.0, "subs": 0, "piids": set()}))

    # Per-PIID top sub
    per_piid_top = []
    grand_total_in_window = 0
    grand_subs = 0

    for piid, rec in data.items():
        if not rec.get("_complete") or rec.get("no_data"):
            continue
        section = get_section(rec.get("label", ""))
        deduped = rec.get("all_deduped", [])
        for d in deduped:
            rec_name = d.get("recipient_name") or ""
            amt = d.get("amount") or 0
            if not rec_name:
                continue
            norm = normalize(rec_name)
            if not norm:
                continue
            parent = parent_of(norm)

            parent_totals[parent]["amount"] += amt
            parent_totals[parent]["subs"] += 1
            parent_totals[parent]["piids"].add(piid)

            section_parent_totals[section][parent]["amount"] += amt
            section_parent_totals[section][parent]["subs"] += 1
            section_parent_totals[section][parent]["piids"].add(piid)

            grand_total_in_window += amt
            grand_subs += 1

        # Top sub for this PIID
        if rec.get("by_recipient"):
            top = rec["by_recipient"][0]
            per_piid_top.append({
                "piid": piid,
                "label": rec.get("label", "")[:60],
                "section": section,
                "total_in_window": rec.get("total_in_window_corrected", 0),
                "top_sub": top["recipient"],
                "top_sub_amount": top["amount"],
            })

    # Sort parent totals
    parent_sorted = sorted(
        ({"parent": k, "amount": v["amount"], "subs": v["subs"], "piid_count": len(v["piids"])}
         for k, v in parent_totals.items()),
        key=lambda x: -x["amount"],
    )

    # Sort sections
    section_sorted = {}
    for section, parents in section_parent_totals.items():
        section_sorted[section] = {
            "parent_total": sum(p["amount"] for p in parents.values()),
            "top_parents": sorted(
                ({"parent": k, "amount": v["amount"], "subs": v["subs"], "piid_count": len(v["piids"])}
                 for k, v in parents.items()),
                key=lambda x: -x["amount"],
            )[:30],
        }

    # Print summary
    print("=" * 90)
    print("TOP 50 PARENT COMPANIES (cross-PIID, FY20-26 window deltas, corrected dedup)")
    print("=" * 90)
    print(f"{'Rank':4s} {'Parent':50s} {'Sub $':>12s} {'PIIDs':>6s} {'#subs':>7s}")
    for i, p in enumerate(parent_sorted[:50], 1):
        print(f"{i:4d} {p['parent'][:50]:50s} ${p['amount']/1e6:>10.1f}M {p['piid_count']:>6d} {p['subs']:>7d}")
    print(f"\nGrand total in-window subs across {len(data)} PIIDs: ${grand_total_in_window/1e9:.2f}B ({grand_subs} unique subaward records)")

    # Per-section
    print("\n" + "=" * 90)
    print("PER-SECTION ROLLUPS")
    print("=" * 90)
    for section in sorted(section_sorted.keys()):
        s = section_sorted[section]
        print(f"\n## {section} -- ${s['parent_total']/1e9:.2f}B total subs")
        for p in s["top_parents"][:10]:
            print(f"  {p['parent'][:50]:50s} ${p['amount']/1e6:>9.1f}M ({p['piid_count']} PIIDs, {p['subs']} subs)")

    # Save
    out = {
        "grand_total_in_window": grand_total_in_window,
        "total_subaward_records": grand_subs,
        "total_piids_pulled": len(data),
        "parent_totals": parent_sorted,
        "section_rollups": section_sorted,
        "per_piid_top": per_piid_top,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=lambda x: list(x) if isinstance(x, set) else str(x))
    print(f"\n\nWrote {OUT}")


if __name__ == "__main__":
    main()
