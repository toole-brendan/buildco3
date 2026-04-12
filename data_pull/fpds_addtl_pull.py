#!/usr/bin/env python3
"""Additional FPDS per-mod pull for newly-discovered Raytheon SM/CIWS/RAM
contracts surfaced by the new vehicle sweep. Adds to fpds_mod_data.json."""

import sys
sys.path.insert(0, '.')
from fpds_per_mod_pull import pull_piid, compute_window_delta, load_existing, save_data
import time

ADDTL = [
    # Raytheon SM new contracts surfaced by sweep
    ("N0002425C5409", "STANDARD MISSILE", "Raytheon FY25 SM-6 BLK IA TAC AUR"),
    ("N0002424C5408", "STANDARD MISSILE", "Raytheon GMA MK25 option exercise + TE"),
    ("N0002423C5408", "STANDARD MISSILE", "Raytheon SM-2 DLMF Maintenance Spares PIO"),
    ("N0002421C5411", "STANDARD MISSILE", "Raytheon SM-2 BLK IIIB TAC AUR"),
    ("N0002418C5432", "STANDARD MISSILE", "Raytheon Encanistered Missile (EM)"),
    ("N0002420C5405", "STANDARD MISSILE", "Raytheon SM Increase Production Capacity"),
    ("N0002424C6104", "STANDARD MISSILE", "Raytheon SM Production Lot #2"),
    # CIWS / RAM new contracts surfaced
    ("N0002422C5400", "DDG MOD - CIWS", "Raytheon RAM GMRP MK 44 MOD 6 BLK 2B"),
    ("N0002424C5406", "DDG MOD - CIWS", "Raytheon FY25 CIWS Production"),
    ("N0002426C5403", "DDG MOD - CIWS", "Raytheon FY26 RAM GMRP MK 44 MOD 6 BLK 2B"),
    ("N0002421C5406", "DDG MOD - CIWS", "Raytheon Block 1B BSL2 Class A Overhaul"),
    ("N0038325FNE02", "DDG MOD - CIWS", "Raytheon Non-Recurring Demand #2"),
    ("N0038325F0NE1", "DDG MOD - CIWS", "Raytheon MK-99 PBL NRD Order #1"),
]


def main():
    data = load_existing()
    print(f"Loaded {len(data)} cached PIIDs")
    print(f"Adding {len(ADDTL)} new PIIDs\n")

    for i, (piid, section, label) in enumerate(ADDTL, 1):
        if piid in data and data[piid].get("_complete"):
            print(f"[{i}/{len(ADDTL)}] {piid} -- cached, skip")
            continue
        print(f"[{i}/{len(ADDTL)}] {piid} ({section}: {label})")
        try:
            mods = pull_piid(piid)
        except Exception as e:
            print(f"  !! ERROR: {e}")
            data[piid] = {"section": section, "label": label, "error": str(e), "_complete": False}
            save_data(data)
            continue
        summary = compute_window_delta(mods)
        record = {
            "section": section,
            "label": label,
            **summary,
            "mods": mods,
            "_complete": True,
        }
        data[piid] = record
        save_data(data)
        print(f"  mods={summary['total_mods_pulled']:3d} in_window={summary['in_window_mods']:3d} "
              f"window_delta=${summary['window_delta_obligated']/1e6:>9.1f}M "
              f"latest_cumulative=${summary['latest_in_window_total_obligated']/1e6:>10.1f}M")
        time.sleep(0.4)

    print(f"\nDone. Total: {len(data)}")


if __name__ == "__main__":
    main()
