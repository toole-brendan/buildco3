#!/usr/bin/env python3
"""
Corrected subaward dedup: group by unique sub_id and take the MAX amount
across all action_date snapshots, NOT the sum. USAspending subaward records
report cumulative-style amounts at each action_date update, so summing
across action_dates double-counts (or 12x-counts in the Marinette case).

For each PIID, recompute aggregates with the corrected dedup and write
results to subaward_corrected.json.
"""

import json
import os
import re
from collections import defaultdict

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_dedup.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_corrected.json")

WINDOW_START = "2020-01-01"
WINDOW_END = "2026-04-10"

SUFFIX_RE = re.compile(
    r"\b(INC\.?|L\.?L\.?C\.?|CORP\.?|CORPORATION|CO\.?|LTD\.?|LP|L\.P\.|"
    r"COMPANY|HOLDINGS)\b\.?,?\s*$",
    re.IGNORECASE,
)


def normalize_vendor(name):
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


def correct_aggregate(in_window_records):
    """For each unique sub_id, keep only the MAX amount across snapshots.
    Then aggregate by recipient."""
    # Group by sub_id
    by_sub_id = defaultdict(list)
    for r in in_window_records:
        sid = r.get("sub_id") or ""
        by_sub_id[sid].append(r)

    # For each sub_id, take the record with the max amount (which is also
    # typically the latest action_date snapshot)
    deduped = []
    for sid, recs in by_sub_id.items():
        if not sid:
            # No sub_id -- assume each is unique, keep all
            deduped.extend(recs)
            continue
        # Sort by amount descending, then take the largest
        recs_sorted = sorted(recs, key=lambda x: (-(x.get("amount") or 0), x.get("action_date") or ""))
        deduped.append(recs_sorted[0])

    # Aggregate by recipient (raw and normalized)
    by_rec_raw = defaultdict(lambda: {"amount": 0.0, "count": 0})
    by_rec_norm = defaultdict(lambda: {"amount": 0.0, "count": 0, "raw_names": set()})

    for r in deduped:
        rec = (r.get("recipient_name") or "").strip()
        amt = r.get("amount") or 0
        if not rec:
            continue
        by_rec_raw[rec]["amount"] += amt
        by_rec_raw[rec]["count"] += 1
        norm = normalize_vendor(rec)
        if norm:
            by_rec_norm[norm]["amount"] += amt
            by_rec_norm[norm]["count"] += 1
            by_rec_norm[norm]["raw_names"].add(rec)

    raw_sorted = sorted(
        ({"recipient": k, **v} for k, v in by_rec_raw.items()),
        key=lambda x: x["amount"], reverse=True,
    )
    norm_sorted = sorted(
        ({"recipient": k, **{**v, "raw_names": sorted(v["raw_names"])}}
         for k, v in by_rec_norm.items()),
        key=lambda x: x["amount"], reverse=True,
    )

    return {
        "unique_sub_ids": len([s for s in by_sub_id if s]),
        "deduped_record_count": len(deduped),
        "total_amount_corrected": sum(r["amount"] or 0 for r in deduped),
        "by_recipient_raw": raw_sorted[:50],
        "by_recipient_normalized": norm_sorted[:50],
    }


def main():
    with open(IN) as f:
        data = json.load(f)

    out = {}
    for piid, rec in data.items():
        if not rec.get("_complete") or rec.get("no_data"):
            out[piid] = rec
            continue
        in_window = rec.get("in_window_records", [])
        prior = rec.get("total_in_window_amount", 0)
        prior_top = rec.get("by_recipient_normalized", [{}])[0]

        corrected = correct_aggregate(in_window)
        new_total = corrected["total_amount_corrected"]

        out[piid] = {
            "label": rec.get("label"),
            "prior_reported_billion": rec.get("prior_reported_billion"),
            "naive_dedup_in_window_total": prior,
            "naive_dedup_record_count": rec.get("deduped_in_window_records"),
            **corrected,
        }

        print(f"\n=== {piid}: {rec.get('label')} ===")
        print(f"  Original (prior file):    ${rec.get('prior_reported_billion', 0):.2f}B")
        print(f"  Naive dedup (sum):        ${prior/1e9:.3f}B  ({rec.get('deduped_in_window_records', 0)} records)")
        print(f"  CORRECTED (per sub_id):   ${new_total/1e9:.3f}B  ({corrected['deduped_record_count']} unique subs)")
        if corrected["by_recipient_normalized"]:
            top = corrected["by_recipient_normalized"][:5]
            print(f"  Top 5 corrected subs:")
            for t in top:
                print(f"    {t['recipient']:50s} ${t['amount']/1e6:>10.1f}M ({t['count']} subs)")

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
