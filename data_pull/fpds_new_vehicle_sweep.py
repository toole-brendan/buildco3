#!/usr/bin/env python3
"""
FPDS sweeps to catch in-scope contracts the original keyword search missed.

Two sweeps:

1. Raytheon Standard Missile newer vehicles (FY23+) -- the Section 16 prime
   list in FY2026_Key_Programs_Contract_Awards.md is all pre-window or
   borderline straddle, but the FY26 SAM line is $1.0B. There must be a
   newer SM production PIID in the system.

2. Navy AGENCY_CODE 1700 dollar-floor backstop at $100M+ for SIGNED_DATE
   2025-26. This is the Lessons §4 round-3 catch-all that previously
   surfaced the Davie / Rauma / Bollinger Arctic Security Cutter awards
   in the cutter pull.

Output: new_vehicles_sweep.json
"""

import json
import os
import re
import sys
import time
from urllib import parse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree.ElementTree import fromstring

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "research-tool/1.0 (FY2026 SAM key programs analysis)"}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_vehicles_sweep.json")

WINDOW_START = "2020-01-01"
WINDOW_END = "2026-04-10"


def fetch(url, max_retries=4):
    delay = 2.0
    for attempt in range(max_retries):
        try:
            req = Request(url, headers=HDRS)
            with urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            print(f"  ! retry {attempt+1}: {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(delay)
            delay *= 2
    return None


def parse_amount(t):
    if not t:
        return 0.0
    try:
        return float(t)
    except (TypeError, ValueError):
        return 0.0


def parse_entries(xml_text):
    try:
        root = fromstring(xml_text)
    except Exception as e:
        print(f"  ! XML parse error: {e}", file=sys.stderr)
        return
    for entry in root.findall("a:entry", NS):
        content = entry.find("a:content", NS)
        if content is None:
            continue
        elem = (
            content.find(".//ns1:award", NS)
            or content.find(".//ns1:OtherTransactionAward", NS)
            or content.find(".//ns1:OtherTransactionIDV", NS)
            or content.find(".//ns1:IDV", NS)
        )
        if elem is None:
            continue

        def get_text(path):
            n = elem.find(path, NS)
            return n.text if n is not None and n.text else ""

        def get_attr(path, attr):
            n = elem.find(path, NS)
            return n.get(attr, "") if n is not None else ""

        rec = {
            "piid": get_text(".//ns1:awardContractID/ns1:PIID")
                or get_text(".//ns1:IDVID/ns1:PIID")
                or get_text(".//ns1:OtherTransactionAwardContractID/ns1:PIID")
                or get_text(".//ns1:OtherTransactionIDVContractID/ns1:PIID"),
            "mod_number": get_text(".//ns1:awardContractID/ns1:modNumber")
                or get_text(".//ns1:IDVID/ns1:modNumber"),
            "signed_date": (get_text(".//ns1:signedDate") or "")[:10],
            "obligated_amount": parse_amount(get_text(".//ns1:obligatedAmount")),
            "total_obligated_amount": parse_amount(get_text(".//ns1:totalObligatedAmount")),
            "base_and_all_options_value": parse_amount(get_text(".//ns1:baseAndAllOptionsValue")),
            "total_base_and_all_options_value": parse_amount(get_text(".//ns1:totalBaseAndAllOptionsValue")),
            "vendor_name": get_text(".//ns1:vendorName"),
            "description": get_text(".//ns1:descriptionOfContractRequirement"),
            "agency": get_attr(".//ns1:contractingOfficeAgencyID", "name"),
            "office": get_attr(".//ns1:contractingOfficeID", "name"),
            "psc": get_text(".//ns1:productOrServiceCode"),
            "naics": get_text(".//ns1:principalNAICSCode"),
        }
        yield rec


def sweep(query, max_pages=200, label=""):
    """Run a paginated FPDS query and return all entry dicts."""
    print(f"\n=== SWEEP: {label} ===")
    print(f"Query: {query}")
    records = []
    start = 0
    last_known = None
    while start // 10 < max_pages:
        url = f"{BASE}&{parse.urlencode({'q': query})}&start={start}"
        try:
            xml_text = fetch(url)
        except Exception as e:
            print(f"  ! fetch failed at start={start}: {e}", file=sys.stderr)
            break
        if not xml_text:
            break

        page_records = list(parse_entries(xml_text))

        if last_known is None:
            m = re.search(r'rel="last"[^>]*start=(\d+)', xml_text)
            last_known = int(m.group(1)) if m else 0
            total = last_known + 10
            print(f"  ~{total} records (last_start={last_known})")

        if not page_records and start == 0:
            break
        if not page_records:
            break

        records.extend(page_records)

        if start >= last_known:
            break
        start += 10
        time.sleep(0.3)

    print(f"  pulled {len(records)} records")
    return records


def dedupe_to_latest_per_piid(records):
    """One record per PIID, keeping latest signed mod."""
    by_piid = {}
    for r in records:
        piid = r.get("piid")
        if not piid:
            continue
        prev = by_piid.get(piid)
        if prev is None or (r.get("signed_date") or "") > (prev.get("signed_date") or ""):
            by_piid[piid] = r
    return sorted(by_piid.values(), key=lambda x: -x.get("total_obligated_amount", 0))


def main():
    out = {}

    # SWEEP 1: Raytheon SM newer vehicles
    # The "Standard Missile" keyword + Raytheon vendor + FY23+ signed
    q1 = (
        f'VENDOR_NAME:"RAYTHEON" '
        f'DESCRIPTION_OF_REQUIREMENT:"STANDARD MISSILE" '
        f'SIGNED_DATE:[2023/01/01,2026/04/10]'
    )
    sm_records = sweep(q1, label="Raytheon Standard Missile FY23+")
    sm_unique = dedupe_to_latest_per_piid(sm_records)
    print(f"  unique PIIDs: {len(sm_unique)}")
    for r in sm_unique[:20]:
        print(f"    {r['piid']:20s} {r['signed_date']:10s} ${r['total_obligated_amount']/1e6:>8.1f}M  {r['description'][:80]}")
    out["raytheon_sm_fy23_plus"] = {
        "query": q1,
        "total_records": len(sm_records),
        "unique_piids": len(sm_unique),
        "records": sm_unique,
    }

    # SWEEP 2: Try also a vendor-only search to catch SM with non-matching desc
    q1b = (
        f'VENDOR_NAME:"RAYTHEON" '
        f'CONTRACTING_AGENCY_ID:"1700" '
        f'SIGNED_DATE:[2023/01/01,2026/04/10] '
        f'OBLIGATED_AMOUNT:[100000000,99999999999]'
    )
    raytheon_navy = sweep(q1b, label="Raytheon Navy $100M+ FY23+")
    raytheon_unique = dedupe_to_latest_per_piid(raytheon_navy)
    print(f"  unique PIIDs: {len(raytheon_unique)}")
    for r in raytheon_unique[:30]:
        print(f"    {r['piid']:20s} {r['signed_date']:10s} ${r['total_obligated_amount']/1e6:>8.1f}M  {r['description'][:80]}")
    out["raytheon_navy_100M_fy23_plus"] = {
        "query": q1b,
        "total_records": len(raytheon_navy),
        "unique_piids": len(raytheon_unique),
        "records": raytheon_unique,
    }

    # SWEEP 3: Navy dollar-floor backstop FY25-26
    q2 = (
        f'CONTRACTING_AGENCY_ID:"1700" '
        f'SIGNED_DATE:[2025/01/01,2026/04/10] '
        f'OBLIGATED_AMOUNT:[100000000,99999999999]'
    )
    navy_records = sweep(q2, label="Navy $100M+ FY25-26 backstop")
    navy_unique = dedupe_to_latest_per_piid(navy_records)
    print(f"  unique PIIDs: {len(navy_unique)}")
    print(f"  top 30 by total_obligated:")
    for r in navy_unique[:30]:
        v = r["vendor_name"][:30]
        print(f"    {r['piid']:22s} {r['signed_date']:10s} ${r['total_obligated_amount']/1e6:>8.1f}M  {v:30s} {r['description'][:60]}")
    out["navy_100M_fy25_26"] = {
        "query": q2,
        "total_records": len(navy_records),
        "unique_piids": len(navy_unique),
        "records": navy_unique,
    }

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
