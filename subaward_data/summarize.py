"""Summarize subaward data: top subcontractors per program area."""
import json
import os
import sys
from collections import defaultdict

OUTDIR = "/Users/brendantoole/projects2/buildco3/subaward_data"

def normalize_name(name):
    """Normalize vendor name for grouping."""
    if not name:
        return "UNKNOWN"
    n = name.upper().strip()
    # Strip common suffixes
    for suffix in [", INC.", ", INC", " INC.", " INC", ", LLC", " LLC", ", L.L.C.", " L.L.C.",
                   ", CORP.", " CORP.", " CORPORATION", " CO.", " COMPANY", " LTD", " LP",
                   ", L.P.", " L.P.", ", LP", ", CO."]:
        if n.endswith(suffix):
            n = n[:-len(suffix)]
    return n.strip()

def summarize_batch(batch_name):
    fpath = os.path.join(OUTDIR, f"{batch_name}.json")
    if not os.path.exists(fpath):
        return
    with open(fpath) as f:
        data = json.load(f)

    print(f"\n{'='*80}")
    print(f"BATCH: {batch_name}")
    print(f"{'='*80}")

    # Aggregate subawards across all PIIDs in this batch
    subs_by_vendor = defaultdict(lambda: {"total": 0, "count": 0, "primes": set(), "descs": set()})

    for piid, info in data.items():
        if not info.get("found"):
            continue
        for sub in info.get("subawards", []):
            name = normalize_name(sub.get("recipient_name"))
            amt = sub.get("amount") or 0
            desc = (sub.get("description") or "").strip()[:60]
            subs_by_vendor[name]["total"] += amt
            subs_by_vendor[name]["count"] += 1
            subs_by_vendor[name]["primes"].add(piid)
            if desc:
                subs_by_vendor[name]["descs"].add(desc)

    # Print per-PIID summary
    print("\nPer-PIID totals:")
    for piid, info in data.items():
        if not info.get("found"):
            print(f"  {piid} ({info.get('label', '')}): NOT FOUND")
            continue
        cnt = info.get("subaward_count", 0)
        amt = info.get("total_subaward_amount", 0) or 0
        prime = info.get("prime_recipient", "?")
        print(f"  {piid} ({info.get('label', '')}): {cnt} subs, ${amt:,.0f} -- prime: {prime}")

    # Top subcontractors aggregated across this batch
    sorted_vendors = sorted(subs_by_vendor.items(), key=lambda x: -x[1]["total"])
    print(f"\nTop 30 subcontractors aggregated across batch:")
    for name, info in sorted_vendors[:30]:
        primes_str = f"{len(info['primes'])} primes"
        sample_desc = list(info['descs'])[0] if info['descs'] else ""
        print(f"  ${info['total']:>14,.0f} | {info['count']:>4} actions | {primes_str:>10} | {name}")
        if sample_desc:
            print(f"      ex: {sample_desc}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        summarize_batch(sys.argv[1])
    else:
        for batch in ["ddg_construction", "ddg_1000", "ddg_subsystems", "weapons",
                      "lpd_lha", "lhd_maint", "lcs_mcm", "misc"]:
            summarize_batch(batch)
