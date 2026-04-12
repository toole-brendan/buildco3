"""Retry the PIIDs that failed due to connection drops."""
import json
import os
import sys
import time
sys.path.insert(0, "/Users/brendantoole/projects2/buildco3/subaward_data")
from fetch_subawards import lookup_award, fetch_award_summary, fetch_subawards

OUTDIR = "/Users/brendantoole/projects2/buildco3/subaward_data"

# (file, piid, label)
RETRY = [
    ("ddg_subsystems", "N0002409C5300", "LM SEWIP Block 2 older"),
    ("lpd_lha", "N0002420C2437", "HII LHA 9"),
    ("weapons", "N0002419C5406", "Raytheon SeaRAM upgrade"),
    ("weapons", "N0038319F0VP0", "Raytheon CIWS PBL"),
    ("weapons", "N0002407C6119", "Raytheon SM-3"),
    ("weapons", "N0002417C5410", "Raytheon FY17-21 SM"),
    # Also extras that returned 0 subawards which might have been errors:
    ("ddg_construction", "N0002423C2305", "BIW DDG-51 FY23-27"),
]

for batch_file, piid, label in RETRY:
    fpath = os.path.join(OUTDIR, f"{batch_file}.json")
    with open(fpath) as f:
        data = json.load(f)

    print(f"Retrying {piid} ({label})...", file=sys.stderr)
    info = None
    for attempt in range(3):
        try:
            info = lookup_award(piid)
            if info and info.get("generated_internal_id"):
                break
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}", file=sys.stderr)
        time.sleep(2)

    if not info or not info.get("generated_internal_id"):
        print(f"  -> still not found", file=sys.stderr)
        continue

    award_id = info["generated_internal_id"]
    summary = fetch_award_summary(award_id)
    time.sleep(0.5)
    if summary["subaward_count"] > 0:
        subs = fetch_subawards(award_id)
    else:
        subs = []

    data[piid] = {
        "label": label,
        "found": True,
        "generated_internal_id": award_id,
        "prime_recipient": info["recipient"],
        "prime_amount": info["amount"],
        "subaward_count": summary["subaward_count"],
        "total_subaward_amount": summary["total_subaward_amount"],
        "subawards": subs,
    }
    print(f"  -> {summary['subaward_count']} subawards, ${summary['total_subaward_amount']:,.0f}", file=sys.stderr)

    with open(fpath, "w") as f:
        json.dump(data, f, indent=2)
    time.sleep(1)
