#!/usr/bin/env python3
"""
v3 cross-PIID subaward aggregator. Two-stage dedup:

  Stage 1 (per sub_id, MAX amount): collapses snapshot inflation where the
    same subaward_number appears at multiple action_dates with growing
    amounts.

  Stage 2 (per recipient + prime + identical-amount, dedupe to one):
    collapses multi-sub_id artifacts where USAspending issues separate
    sub_ids for the same underlying subcontract that report identical
    cumulative-style amounts.

  Stage 3 (per recipient + prime, cap at prime contract size): if a single
    recipient on a single prime exceeds the prime's window obligation,
    cap at min(sum, 1.5 × prime_window_obligation). Flag everything that
    hits the cap.

Outputs subaward_aggregated_v3.json with parent rollups + per-section
breakdowns + flagged pairs.
"""

import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aggregate_subs import normalize, parent_of, get_section

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_full.json")
FPDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fpds_mod_data.json")
DEPOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depot_piids_filtered.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_aggregated_v3.json")


def load_prime_sizes():
    """Load prime contract window-delta sizes from FPDS pull + depot sweep."""
    sizes = {}
    if os.path.exists(FPDS):
        with open(FPDS) as f:
            d = json.load(f)
        for piid, rec in d.items():
            wd = rec.get("window_delta_obligated", 0)
            cum = rec.get("latest_in_window_total_obligated", 0)
            # Use the larger of the two as the prime size for capping purposes
            sizes[piid] = max(wd, cum, 0)

    if os.path.exists(DEPOT):
        with open(DEPOT) as f:
            d = json.load(f)
        for r in d.get("piids", []):
            piid = r["piid"]
            cum = r.get("total_obligated_amount", 0)
            if piid not in sizes or sizes[piid] < cum:
                sizes[piid] = cum

    return sizes


def stage1_per_sub_id_max(deduped):
    """Per unique sub_id, take MAX amount across snapshots."""
    by_sid = defaultdict(list)
    for r in deduped:
        sid = r.get("sub_id") or ""
        by_sid[sid].append(r)
    out = []
    for sid, recs in by_sid.items():
        max_rec = max(recs, key=lambda x: x.get("amount") or 0)
        out.append(max_rec)
    return out


def stage2_dedupe_identical_amounts(stage1_records):
    """Per (recipient_name, amount), keep only ONE record. Collapses
    multi-sub_id artifacts where the same subcontract is reported under
    different subaward_numbers."""
    seen = set()
    out = []
    for r in stage1_records:
        rec = (r.get("recipient_name") or "").strip()
        amt = round(r.get("amount") or 0, 2)
        key = (rec, amt)
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def stage3_cap_at_prime_size(per_recipient, prime_size, slack=1.5, exclude_above=4.0):
    """Per recipient, cap at slack × prime_size, BUT entirely exclude any
    recipient whose raw amount exceeds exclude_above × prime_size (clear
    USAspending data corruption -- the 4 NASSCO CG Cowpens depot phantoms
    where 5 different recipients all reported the exact same $920M on a
    $198M prime contract).

    per_recipient is a dict {recipient: sum_amount}.
    Returns (capped_dict, flagged_list, excluded_list).
    """
    if prime_size <= 0:
        return per_recipient.copy(), [], []
    cap = prime_size * slack
    exclusion_threshold = prime_size * exclude_above
    capped = {}
    flagged = []
    excluded = []
    for rec, amt in per_recipient.items():
        if amt > exclusion_threshold:
            excluded.append({"recipient": rec, "raw": amt, "prime_size": prime_size})
            continue  # drop entirely
        if amt > cap:
            capped[rec] = cap
            flagged.append({"recipient": rec, "raw": amt, "capped_at": cap})
        else:
            capped[rec] = amt
    return capped, flagged, excluded


def main():
    with open(IN) as f:
        data = json.load(f)

    prime_sizes = load_prime_sizes()
    print(f"Loaded {len(data)} PIIDs and {len(prime_sizes)} prime sizes\n")

    parent_totals = defaultdict(lambda: {"amount": 0.0, "n_pairs": 0, "piids": set()})
    section_parent_totals = defaultdict(
        lambda: defaultdict(lambda: {"amount": 0.0, "n_pairs": 0, "piids": set()})
    )

    per_piid_corrected = {}
    grand_total = 0
    flagged_pairs = []
    excluded_pairs = []

    for piid, rec in data.items():
        if not rec.get("_complete") or rec.get("no_data"):
            continue
        section = get_section(rec.get("label", ""))
        deduped = rec.get("all_deduped", [])

        # Stage 1: per sub_id MAX
        stage1 = stage1_per_sub_id_max(deduped)

        # Stage 2: collapse identical amounts per recipient
        stage2 = stage2_dedupe_identical_amounts(stage1)

        # Aggregate by recipient
        by_recipient_raw = defaultdict(float)
        for r in stage2:
            rec_name = (r.get("recipient_name") or "").strip()
            if not rec_name:
                continue
            by_recipient_raw[rec_name] += r.get("amount") or 0

        # Stage 3: cap at 1.0x prime size (a sub cannot exceed its prime);
        # exclude > 2x prime (clear corruption)
        prime_size = prime_sizes.get(piid, 0)
        capped, flags, excluded = stage3_cap_at_prime_size(
            by_recipient_raw, prime_size, slack=1.0, exclude_above=2.0
        )

        for f in flags:
            flagged_pairs.append({
                "piid": piid,
                "label": rec.get("label", "")[:80],
                "prime_size": prime_size,
                **f,
            })
        for e in excluded:
            excluded_pairs.append({
                "piid": piid,
                "label": rec.get("label", "")[:80],
                "prime_size": prime_size,
                **e,
            })

        piid_total = sum(capped.values())
        per_piid_corrected[piid] = {
            "label": rec.get("label", ""),
            "section": section,
            "prime_size": prime_size,
            "n_recipients": len(capped),
            "total_in_window_v3": piid_total,
            "top_recipients": sorted(
                ({"recipient": k, "amount": v} for k, v in capped.items()),
                key=lambda x: -x["amount"],
            )[:30],
        }
        grand_total += piid_total

        # Roll up to parent
        for rec_name, amt in capped.items():
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

    print("=" * 100)
    print("V3 TOP 60 PARENT COMPANIES (3-stage dedup, capped at 1.5x prime, FY20-26 window)")
    print("=" * 100)
    print(f"{'Rank':4s} {'Parent':55s} {'Sub $':>12s} {'Pairs':>6s} {'PIIDs':>6s}")
    for i, p in enumerate(parent_sorted[:60], 1):
        print(f"{i:4d} {p['parent'][:55]:55s} ${p['amount']/1e6:>10.1f}M {p['n_pairs']:>6d} {p['piid_count']:>6d}")
    print(f"\nGrand total in-window subs (v3): ${grand_total/1e9:.2f}B")

    print("\n" + "=" * 100)
    print(f"FLAGGED PAIRS (recipient sub > 1.5x prime size — capped)")
    print("=" * 100)
    for f in sorted(flagged_pairs, key=lambda x: -x["raw"])[:30]:
        print(f"  {f['piid']:18s} {f['recipient'][:35]:35s} raw=${f['raw']/1e6:>7.1f}M  cap=${f['capped_at']/1e6:>7.1f}M  prime=${f['prime_size']/1e6:>7.1f}M")
        print(f"    {f['label'][:90]}")

    print("\n" + "=" * 100)
    print("PER-SECTION ROLLUPS (v3)")
    print("=" * 100)
    for section in sorted(section_sorted.keys()):
        s = section_sorted[section]
        print(f"\n## {section} -- ${s['section_total']/1e9:.2f}B total")
        for p in s["top_parents"][:12]:
            print(f"  {p['parent'][:55]:55s} ${p['amount']/1e6:>9.1f}M ({p['piid_count']} PIIDs)")

    print("\n" + "=" * 100)
    print(f"EXCLUDED PAIRS (raw > 4x prime size — clear USAspending data corruption, dropped entirely)")
    print("=" * 100)
    for e in sorted(excluded_pairs, key=lambda x: -x["raw"])[:30]:
        print(f"  {e['piid']:18s} {e['recipient'][:35]:35s} raw=${e['raw']/1e6:>7.1f}M  prime=${e['prime_size']/1e6:>7.1f}M")
        print(f"    {e['label'][:90]}")

    out = {
        "grand_total_in_window_v3": grand_total,
        "total_piids_pulled": len(data),
        "parent_totals": parent_sorted,
        "section_rollups": section_sorted,
        "per_piid": per_piid_corrected,
        "flagged_pairs": flagged_pairs,
        "excluded_pairs": excluded_pairs,
        "method": "Stage1: per sub_id MAX. Stage2: per (recipient, amount) dedupe. Stage3: cap at 1.5x prime, exclude > 4x prime.",
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=lambda x: list(x) if isinstance(x, set) else str(x))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
