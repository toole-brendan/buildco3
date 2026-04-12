#!/usr/bin/env python3
"""
Re-pull USAspending subawards for the suspect aggregates that approached
or exceeded the >$5B sanity floor in the prior synthesis.

For each PIID:
  1. Look up generated_internal_id via /api/v2/search/spending_by_award/
     (try contracts group, then IDV group)
  2. Pull all pages of /api/v2/subawards/
  3. Filter to action_date in window 2020-01-01..2026-04-10
  4. Dedupe by (sub_award_number, action_date, sub_amount) tuple
     (recipient_name + amount alone is NOT a unique key)
  5. Aggregate by recipient_name with vendor normalization
  6. Save full subaward records + aggregated summary to JSON

Per Lessons §5: two-call pattern, retry IDV group on miss, 2,000-record cap.
Per Lessons §7: anything >$5B in a single recipient line is a sanity-check fail.
"""

import json
import os
import re
import sys
import time
from collections import defaultdict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subaward_dedup.json")
WINDOW_START = "2020-01-01"
WINDOW_END = "2026-04-10"

HDRS = {
    "Content-Type": "application/json",
    "User-Agent": "research-tool/1.0",
}

# PIIDs to re-pull, with the previously-reported sub total for comparison
SUSPECT_PIIDS = [
    ("N0002411C2300", "LM LCS Freedom Construction (Marinette flag)", 47.17e9, "Marinette $47B claim"),
    ("N0002422C5500", "Raytheon SPY-6 Production", 1.42e9, "CAES/Mercury aggregate base"),
    ("N0002416C5363", "LM SEWIP Block 2", 2.85e9, "approaches sanity floor"),
    ("N0002420C5503", "LM SLQ-32(V)6 Production", 1.42e9, "approaches sanity floor"),
    ("N0002417C6311", "NG Knifefish/LCS systems", 1.475e9, "Teledyne aggregate base"),
    ("N6133111C0017", "GDMS Surface MCM Unmanned", 1.23e9, "approaches sanity floor"),
]


def http_post_json(url, payload, max_retries=4):
    delay = 2.0
    for attempt in range(max_retries):
        try:
            data = json.dumps(payload).encode("utf-8")
            req = Request(url, data=data, headers=HDRS, method="POST")
            with urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as e:
            code = getattr(e, "code", None)
            if code == 422:
                # Don't retry on 422
                raise
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
    """Try contracts group then IDV group."""
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    for group in CONTRACT_GROUPS:
        payload = {
            "filters": {
                "award_type_codes": group,
                "award_ids": [piid],
                "time_period": [
                    {"start_date": "2007-10-01", "end_date": "2026-09-30"}
                ],
            },
            "fields": [
                "Award ID", "generated_internal_id", "Recipient Name",
                "Award Amount", "Total Outlays", "Description",
                "Awarding Agency", "Awarding Sub Agency",
                "Start Date", "End Date",
            ],
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
    """Page through subawards. Cap at max_records."""
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
            print(f"  ! subaward fetch failed page {page}: {e}", file=sys.stderr)
            break
        if not j:
            break
        results = j.get("results", [])
        if not results:
            break
        subs.extend(results)
        meta = j.get("page_metadata", {})
        if not meta.get("hasNext"):
            break
        page += 1
        time.sleep(0.4)
    return subs


SUFFIX_RE = re.compile(
    r"\b(INC\.?|L\.?L\.?C\.?|CORP\.?|CORPORATION|CO\.?|LTD\.?|LP|L\.P\.|"
    r"COMPANY|HOLDINGS|TECHNOLOGIES|TECHNOLOGY)\b\.?,?\s*$",
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


def get_sub_amount(s):
    """USAspending subaward records use various field names."""
    for k in ("subaward_amount", "amount", "Sub-Award Amount", "sub_award_amount"):
        v = s.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                pass
    return 0.0


def get_sub_date(s):
    for k in ("action_date", "subaward_action_date", "Sub-Award Date", "subaward_date"):
        v = s.get(k)
        if v:
            return str(v)[:10]
    return ""


def get_sub_recipient(s):
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


def aggregate(subs):
    """Dedupe by (sub_id, action_date, recipient, amount) and aggregate.
    Filters to in-window only."""
    seen = set()
    in_window = []
    for s in subs:
        sub_id = get_sub_id(s)
        date = get_sub_date(s)
        rec = get_sub_recipient(s)
        amt = get_sub_amount(s)
        if not (WINDOW_START <= date <= WINDOW_END):
            continue
        key = (sub_id, date, rec, round(amt, 2))
        if key in seen:
            continue
        seen.add(key)
        in_window.append({
            "sub_id": sub_id,
            "action_date": date,
            "recipient_name": rec,
            "amount": amt,
            "description": s.get("description") or s.get("subaward_description") or "",
        })

    by_rec = defaultdict(lambda: {"amount": 0.0, "count": 0, "raw_names": set()})
    by_norm = defaultdict(lambda: {"amount": 0.0, "count": 0, "raw_names": set()})
    for r in in_window:
        rec = r["recipient_name"]
        amt = r["amount"]
        if not rec:
            continue
        by_rec[rec]["amount"] += amt
        by_rec[rec]["count"] += 1
        norm = normalize_vendor(rec)
        if norm:
            by_norm[norm]["amount"] += amt
            by_norm[norm]["count"] += 1
            by_norm[norm]["raw_names"].add(rec)

    # Convert to sorted lists
    raw_sorted = sorted(
        ({"recipient": k, **v} for k, v in by_rec.items()),
        key=lambda x: x["amount"], reverse=True,
    )
    norm_sorted = sorted(
        ({"recipient": k, **{**v, "raw_names": sorted(v["raw_names"])}} for k, v in by_norm.items()),
        key=lambda x: x["amount"], reverse=True,
    )

    return {
        "total_records_pulled": len(subs),
        "deduped_in_window_records": len(in_window),
        "total_in_window_amount": sum(r["amount"] for r in in_window),
        "unique_recipients_raw": len(by_rec),
        "unique_recipients_normalized": len(by_norm),
        "by_recipient_raw": raw_sorted[:50],
        "by_recipient_normalized": norm_sorted[:50],
        "in_window_records": in_window,  # all of them, for downstream
    }


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
    data = load_existing()
    print(f"Loaded {len(data)} cached entries from {OUT}")
    print(f"Window: {WINDOW_START} to {WINDOW_END}\n")

    for i, (piid, label, prior_total, note) in enumerate(SUSPECT_PIIDS, 1):
        if piid in data and data[piid].get("_complete"):
            print(f"[{i}/{len(SUSPECT_PIIDS)}] {piid} -- cached, skip")
            continue
        print(f"[{i}/{len(SUSPECT_PIIDS)}] {piid} ({label})")
        print(f"  Prior reported: ${prior_total/1e9:.2f}B -- {note}")

        try:
            id_results, group = find_generated_internal_id(piid)
        except Exception as e:
            print(f"  !! id lookup failed: {e}", file=sys.stderr)
            data[piid] = {"label": label, "error": str(e), "_complete": False}
            save_data(data)
            continue

        if not id_results:
            print(f"  !! no generated_internal_id found in either group")
            data[piid] = {
                "label": label,
                "prior_reported_billion": prior_total / 1e9,
                "id_lookup_results": [],
                "_complete": True,
                "no_data": True,
            }
            save_data(data)
            continue

        gid = id_results[0].get("generated_internal_id", "")
        print(f"  group={group} gid={gid}")

        try:
            subs = pull_subawards(gid)
        except Exception as e:
            print(f"  !! subaward pull failed: {e}", file=sys.stderr)
            data[piid] = {"label": label, "gid": gid, "error": str(e), "_complete": False}
            save_data(data)
            continue

        agg = aggregate(subs)
        record = {
            "label": label,
            "prior_reported_billion": prior_total / 1e9,
            "note": note,
            "group": group,
            "gid": gid,
            "id_lookup_results": id_results[:3],
            **agg,
            "_complete": True,
        }
        data[piid] = record
        save_data(data)

        new_total = agg["total_in_window_amount"]
        ratio = (new_total / prior_total) if prior_total else 0
        print(f"  pulled={agg['total_records_pulled']}  in_window={agg['deduped_in_window_records']}  "
              f"new_total=${new_total/1e9:.3f}B  ({ratio*100:.0f}% of prior)")
        if agg["by_recipient_normalized"]:
            top = agg["by_recipient_normalized"][0]
            print(f"  top sub: {top['recipient']} ${top['amount']/1e6:.1f}M ({top['count']} actions)")
        time.sleep(0.5)

    print(f"\nDone. Wrote {len(data)} PIIDs to {OUT}")


if __name__ == "__main__":
    main()
