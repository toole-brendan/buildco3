#!/usr/bin/env python3
"""
Comprehensive USAspending subaward pull for ALL in-scope PIIDs:
  - 82 PIIDs from fpds_mod_data.json (per-mod pull list)
  - 88 PIIDs from depot_piids_filtered.json (depot maintenance)

For each PIID:
  1. Look up generated_internal_id (try contracts group, then IDV group)
  2. Pull all subaward records (paginate)
  3. Apply CORRECT dedup: per unique sub_id, keep MAX amount across snapshots
  4. Filter to in-window (2020-01-01 to 2026-04-10)
  5. Aggregate by recipient (raw + normalized)

Saves incrementally to subaward_full.json. Resume-safe.

Per Lessons §5: two-call pattern, IDV group fallback, ~2000-record cap.
"""

import json
import os
import re
import sys
import time
from collections import defaultdict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_full.json")
WINDOW_START = "2020-01-01"
WINDOW_END = "2026-04-10"

HDRS = {"Content-Type": "application/json", "User-Agent": "research-tool/1.0"}

# Load PIID lists
def load_piid_list():
    piids = []  # list of (piid, source_label)

    # 82 from per-mod pull
    fpds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fpds_mod_data.json")
    if os.path.exists(fpds_path):
        with open(fpds_path) as f:
            d = json.load(f)
        for piid, rec in d.items():
            label = f"{rec.get('section','??')}::{rec.get('label','')}"
            piids.append((piid, label))

    # 88 depot PIIDs
    depot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depot_piids_filtered.json")
    if os.path.exists(depot_path):
        with open(depot_path) as f:
            d = json.load(f)
        for r in d["piids"]:
            piid = r["piid"]
            vendor = r.get("vendor_name", "")
            desc = (r.get("description", "") or "")[:60]
            label = f"DEPOT::{vendor}::{desc}"
            piids.append((piid, label))

    # Dedupe (some PIIDs may be in both lists)
    seen = set()
    unique = []
    for p, l in piids:
        if p in seen:
            continue
        seen.add(p)
        unique.append((p, l))
    return unique


def http_post_json(url, payload, max_retries=4):
    delay = 2.0
    for attempt in range(max_retries):
        try:
            data = json.dumps(payload).encode("utf-8")
            req = Request(url, data=data, headers=HDRS, method="POST")
            with urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 422:
                raise
            if attempt == max_retries - 1:
                raise
            print(f"  ! retry {attempt+1}: HTTP {e.code}", file=sys.stderr)
            time.sleep(delay)
            delay *= 2
        except (URLError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            print(f"  ! retry {attempt+1}: {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(delay)
            delay *= 2
    return None


CONTRACT_GROUPS = [
    ["A", "B", "C", "D"],
    ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"],
]


def find_generated_internal_id(piid):
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    for group in CONTRACT_GROUPS:
        payload = {
            "filters": {
                "award_type_codes": group,
                "award_ids": [piid],
                "time_period": [{"start_date": "2007-10-01", "end_date": "2026-09-30"}],
            },
            "fields": ["Award ID", "generated_internal_id", "Recipient Name",
                       "Award Amount", "Description"],
            "limit": 50,
            "page": 1,
        }
        try:
            j = http_post_json(url, payload)
        except HTTPError as e:
            if e.code == 422:
                continue
            raise
        results = j.get("results", []) if j else []
        if results:
            return results, group
    return [], None


def pull_subawards(generated_internal_id, max_records=5000):
    url = "https://api.usaspending.gov/api/v2/subawards/"
    subs = []
    page = 1
    while len(subs) < max_records:
        payload = {
            "award_id": generated_internal_id,
            "limit": 100,
            "page": page,
            "sort": "amount",
            "order": "desc",
        }
        try:
            j = http_post_json(url, payload)
        except Exception as e:
            print(f"  ! pull failed page {page}: {e}", file=sys.stderr)
            break
        if not j:
            break
        results = j.get("results", [])
        if not results:
            break
        subs.extend(results)
        if not j.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
        time.sleep(0.3)
    return subs


def get_amount(s):
    for k in ("subaward_amount", "amount", "Sub-Award Amount", "sub_award_amount"):
        v = s.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                pass
    return 0.0


def get_date(s):
    for k in ("action_date", "subaward_action_date", "Sub-Award Date", "subaward_date"):
        v = s.get(k)
        if v:
            return str(v)[:10]
    return ""


def get_recipient(s):
    for k in ("recipient_name", "Sub-Recipient Name", "subawardee_name"):
        v = s.get(k)
        if v:
            return v
    return ""


def get_sub_id(s):
    for k in ("subaward_number", "internal_id", "Sub-Award ID", "id"):
        v = s.get(k)
        if v:
            return str(v)
    return ""


def correct_dedup(subs, window_start=WINDOW_START, window_end=WINDOW_END):
    """Per unique sub_id (in window), take the max amount across snapshots."""
    by_sub_id = defaultdict(list)
    for s in subs:
        sid = get_sub_id(s)
        date = get_date(s)
        if not (window_start <= date <= window_end):
            continue
        rec = {
            "sub_id": sid,
            "action_date": date,
            "recipient_name": get_recipient(s),
            "amount": get_amount(s),
            "description": (s.get("description") or s.get("subaward_description") or "")[:120],
        }
        if sid:
            by_sub_id[sid].append(rec)
        else:
            # No sub_id -- treat each as unique
            by_sub_id[f"_no_id_{len(by_sub_id)}"].append(rec)

    deduped = []
    for sid, recs in by_sub_id.items():
        # Take record with max amount
        recs_sorted = sorted(recs, key=lambda x: (-(x.get("amount") or 0), x.get("action_date") or ""))
        deduped.append(recs_sorted[0])
    return deduped


def aggregate(deduped):
    by_rec = defaultdict(lambda: {"amount": 0.0, "count": 0})
    for r in deduped:
        rec = r.get("recipient_name") or ""
        amt = r.get("amount") or 0
        if not rec:
            continue
        by_rec[rec]["amount"] += amt
        by_rec[rec]["count"] += 1
    return sorted(
        ({"recipient": k, **v} for k, v in by_rec.items()),
        key=lambda x: x["amount"], reverse=True,
    )


def load_existing():
    if os.path.exists(OUT):
        try:
            with open(OUT) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_data(data):
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, default=str)
    os.replace(tmp, OUT)


def main():
    piid_list = load_piid_list()
    print(f"Total unique PIIDs to process: {len(piid_list)}")
    print(f"Window: {WINDOW_START} to {WINDOW_END}\n")

    data = load_existing()
    print(f"Cached: {len(data)}\n")

    for i, (piid, label) in enumerate(piid_list, 1):
        if piid in data and data[piid].get("_complete"):
            print(f"[{i}/{len(piid_list)}] {piid} -- cached, skip")
            continue
        print(f"[{i}/{len(piid_list)}] {piid} :: {label[:60]}")

        try:
            id_results, group = find_generated_internal_id(piid)
        except Exception as e:
            print(f"  !! id lookup error: {e}", file=sys.stderr)
            data[piid] = {"label": label, "error": str(e), "_complete": False}
            save_data(data)
            continue

        if not id_results:
            print(f"  -- no generated_internal_id found in either group")
            data[piid] = {
                "label": label,
                "no_data": True,
                "_complete": True,
            }
            save_data(data)
            continue

        gid = id_results[0].get("generated_internal_id", "")

        try:
            subs = pull_subawards(gid)
        except Exception as e:
            print(f"  !! subaward pull error: {e}", file=sys.stderr)
            data[piid] = {"label": label, "gid": gid, "error": str(e), "_complete": False}
            save_data(data)
            continue

        deduped = correct_dedup(subs)
        agg = aggregate(deduped)
        total = sum(r["amount"] for r in deduped)

        record = {
            "label": label,
            "group": group,
            "gid": gid,
            "total_records_pulled": len(subs),
            "deduped_unique_subs": len(deduped),
            "total_in_window_corrected": total,
            "by_recipient": agg[:50],  # top 50 only
            "all_deduped": deduped,  # full list for downstream rollup
            "_complete": True,
        }
        data[piid] = record
        save_data(data)

        print(f"  pulled={len(subs)}  unique_subs={len(deduped)}  in_window=${total/1e6:.1f}M")
        if agg:
            print(f"  top: {agg[0]['recipient'][:40]:40s} ${agg[0]['amount']/1e6:.1f}M")
        time.sleep(0.3)

    print(f"\nDone. Wrote {len(data)} PIIDs to {OUT}")


if __name__ == "__main__":
    main()
