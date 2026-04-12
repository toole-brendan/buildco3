#!/usr/bin/env python3
"""
v2 cross-PIID subaward aggregator with stronger dedup.

Key changes from v1:
  1. Per (prime_piid, recipient_name), collapse multiple sub_ids that have
     identical amounts. USAspending issues separate sub_ids for the same
     underlying subcontract when prime contract mods touch it, each
     snapshot reporting the same cumulative amount.
  2. Per (prime_piid, recipient_name), take ONLY the MAX amount across
     all snapshots — regardless of sub_id. This represents the latest
     observed total for that recipient on that prime contract.
  3. Apply a sanity-check ceiling: any single (recipient, prime) pair
     above $500M is flagged for manual review (per Lessons §7).
  4. Aggregate by parent company across all primes.
  5. Per-program rollups.

Imports the parent map from aggregate_subs.py.
"""

import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aggregate_subs import (
    PARENT_MAP, normalize, parent_of, get_section
)

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_full.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_aggregated_v2.json")

WINDOW_START = "2020-01-01"
WINDOW_END = "2026-04-10"

# Per-pair sanity floor: anything above this is flagged
PAIR_SANITY_FLOOR = 500_000_000  # $500M


def collapse_per_recipient_per_prime(deduped):
    """For each (recipient, prime_piid) pair, take ONLY the MAX amount
    across all snapshots. This is the strongest dedup possible.

    Returns list of (recipient_name, max_amount, n_distinct_sub_ids,
    n_total_records).
    """
    by_pair = defaultdict(list)
    for d in deduped:
        rec_name = (d.get("recipient_name") or "").strip()
        if not rec_name:
            continue
        amt = d.get("amount") or 0
        by_pair[rec_name].append(d)

    out = []
    for rec_name, recs in by_pair.items():
        max_amt = max(r["amount"] for r in recs)
        n_sub_ids = len(set(r.get("sub_id", "") for r in recs))
        n_records = len(recs)
        out.append({
            "recipient_name": rec_name,
            "amount": max_amt,
            "n_distinct_sub_ids": n_sub_ids,
            "n_records": n_records,
        })
    return sorted(out, key=lambda x: -x["amount"])


def main():
    with open(IN) as f:
        data = json.load(f)

    print(f"Loaded {len(data)} PIIDs from {IN}\n")

    # Per-PIID corrected aggregation
    per_piid_corrected = {}
    grand_total = 0

    # Cross-PIID parent rollup
    parent_totals = defaultdict(lambda: {"amount": 0.0, "n_pairs": 0, "piids": set()})
    section_parent_totals = defaultdict(
        lambda: defaultdict(lambda: {"amount": 0.0, "n_pairs": 0, "piids": set()})
    )

    flagged_pairs = []  # (piid, recipient, amount)

    for piid, rec in data.items():
        if not rec.get("_complete") or rec.get("no_data"):
            continue
        section = get_section(rec.get("label", ""))
        deduped = rec.get("all_deduped", [])
        collapsed = collapse_per_recipient_per_prime(deduped)

        piid_total = sum(c["amount"] for c in collapsed)
        per_piid_corrected[piid] = {
            "label": rec.get("label", ""),
            "section": section,
            "n_recipients": len(collapsed),
            "total_in_window_v2": piid_total,
            "top_recipients": collapsed[:30],
        }
        grand_total += piid_total

        for c in collapsed:
            rec_name = c["recipient_name"]
            amt = c["amount"]

            # Sanity flag
            if amt > PAIR_SANITY_FLOOR:
                flagged_pairs.append({
                    "piid": piid,
                    "label": rec.get("label", "")[:80],
                    "recipient": rec_name,
                    "amount": amt,
                    "n_records": c["n_records"],
                    "n_sub_ids": c["n_distinct_sub_ids"],
                })

            norm = normalize(rec_name)
            if not norm:
                continue
            parent = parent_of(norm)

            parent_totals[parent]["amount"] += amt
            parent_totals[parent]["n_pairs"] += 1
            parent_totals[parent]["piids"].add(piid)

            section_parent_totals[section][parent]["amount"] += amt
            section_parent_totals[section][parent]["n_pairs"] += 1
            section_parent_totals[section][parent]["piids"].add(piid)

    parent_sorted = sorted(
        ({"parent": k, "amount": v["amount"], "n_pairs": v["n_pairs"],
          "piid_count": len(v["piids"])} for k, v in parent_totals.items()),
        key=lambda x: -x["amount"],
    )

    section_sorted = {}
    for section, parents in section_parent_totals.items():
        section_sorted[section] = {
            "section_total": sum(p["amount"] for p in parents.values()),
            "top_parents": sorted(
                ({"parent": k, "amount": v["amount"], "n_pairs": v["n_pairs"],
                  "piid_count": len(v["piids"])} for k, v in parents.items()),
                key=lambda x: -x["amount"],
            )[:30],
        }

    # Print summary
    print("=" * 100)
    print("V2 TOP 60 PARENT COMPANIES (per-recipient-per-prime MAX dedup, FY20-26 window)")
    print("=" * 100)
    print(f"{'Rank':4s} {'Parent':55s} {'Sub $':>12s} {'Pairs':>6s} {'PIIDs':>6s}")
    for i, p in enumerate(parent_sorted[:60], 1):
        print(f"{i:4d} {p['parent'][:55]:55s} ${p['amount']/1e6:>10.1f}M {p['n_pairs']:>6d} {p['piid_count']:>6d}")
    print(f"\nGrand total in-window subs (v2): ${grand_total/1e9:.2f}B")

    print("\n" + "=" * 100)
    print(f"FLAGGED PAIRS (>${PAIR_SANITY_FLOOR/1e6:.0f}M single-recipient single-prime — manual review needed)")
    print("=" * 100)
    for f in sorted(flagged_pairs, key=lambda x: -x["amount"]):
        print(f"  {f['piid']:18s} {f['recipient'][:40]:40s} ${f['amount']/1e9:>5.2f}B  ({f['n_records']} records, {f['n_sub_ids']} sub_ids)")
        print(f"    {f['label'][:90]}")

    print("\n" + "=" * 100)
    print("PER-SECTION ROLLUPS (v2)")
    print("=" * 100)
    for section in sorted(section_sorted.keys()):
        s = section_sorted[section]
        print(f"\n## {section} -- ${s['section_total']/1e9:.2f}B total subs")
        for p in s["top_parents"][:12]:
            print(f"  {p['parent'][:55]:55s} ${p['amount']/1e6:>9.1f}M ({p['piid_count']} PIIDs)")

    out = {
        "grand_total_in_window_v2": grand_total,
        "total_piids_pulled": len(data),
        "parent_totals": parent_sorted,
        "section_rollups": section_sorted,
        "per_piid": per_piid_corrected,
        "flagged_pairs": flagged_pairs,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=lambda x: list(x) if isinstance(x, set) else str(x))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
