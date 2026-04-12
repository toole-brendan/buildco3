#!/usr/bin/env python3
"""
Sweep FPDS for depot maintenance PIIDs across the major surface-combatant
and amphib regional ship-repair primes. Output a list of unique PIIDs in
the FY20-26 window over $10M obligated, suitable for feeding into the
subaward pull script.

Vendors swept:
  BAE Systems (Norfolk, San Diego, Jacksonville, Hawaii Ship Repair)
  NASSCO (General Dynamics)
  Metro Machine Corp (Norfolk)
  Vigor Marine LLC (Portland, OR)
  Continental Maritime of San Diego
  Marine Hydraulics International (Norfolk)
  Pacific Ship Repair & Fabrication
  HII San Diego Shipyard

Output: depot_piids.json
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
HDRS = {"User-Agent": "research-tool/1.0"}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depot_piids.json")

# Vendor sweeps. Each tuple: (vendor_name, label)
VENDORS = [
    ("BAE SYSTEMS NORFOLK SHIP REPAIR", "BAE Norfolk"),
    ("BAE SYSTEMS SAN DIEGO SHIP REPAIR", "BAE San Diego"),
    ("BAE SYSTEMS JACKSONVILLE SHIP REPAIR", "BAE Jacksonville"),
    ("BAE SYSTEMS HAWAII SHIPYARDS", "BAE Hawaii"),
    ("METRO MACHINE", "Metro Machine"),
    ("VIGOR MARINE", "Vigor Marine"),
    ("CONTINENTAL MARITIME", "Continental Maritime SD"),
    ("MARINE HYDRAULICS INTERNATIONAL", "MHI Norfolk"),
    ("HUNTINGTON INGALLS INDUSTRIES SAN DIEGO", "HII San Diego"),
    ("PACIFIC SHIP REPAIR", "Pacific Ship Repair"),
    ("NATIONAL STEEL AND SHIPBUILDING", "NASSCO"),
]


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

        rec = {
            "piid": get_text(".//ns1:awardContractID/ns1:PIID")
                or get_text(".//ns1:IDVID/ns1:PIID")
                or get_text(".//ns1:OtherTransactionAwardContractID/ns1:PIID")
                or get_text(".//ns1:OtherTransactionIDVContractID/ns1:PIID"),
            "signed_date": (get_text(".//ns1:signedDate") or "")[:10],
            "obligated_amount": parse_amount(get_text(".//ns1:obligatedAmount")),
            "total_obligated_amount": parse_amount(get_text(".//ns1:totalObligatedAmount")),
            "vendor_name": get_text(".//ns1:vendorName"),
            "description": get_text(".//ns1:descriptionOfContractRequirement"),
        }
        yield rec


def sweep_vendor(vendor, label, max_pages=300):
    """Pull all FY20-26 records over $10M for a vendor."""
    q = (
        f'VENDOR_NAME:"{vendor}" '
        f'CONTRACTING_AGENCY_ID:"1700" '
        f'SIGNED_DATE:[2020/01/01,2026/04/10] '
        f'OBLIGATED_AMOUNT:[10000000,99999999999]'
    )
    print(f"\n=== {label} ===")
    print(f"Q: {q}")
    records = []
    start = 0
    last_known = None
    while start // 10 < max_pages:
        url = f"{BASE}&{parse.urlencode({'q': q})}&start={start}"
        try:
            xml_text = fetch(url)
        except Exception as e:
            print(f"  ! fetch failed: {e}", file=sys.stderr)
            break
        if not xml_text:
            break
        page = list(parse_entries(xml_text))
        if last_known is None:
            m = re.search(r'rel="last"[^>]*start=(\d+)', xml_text)
            last_known = int(m.group(1)) if m else 0
        if not page and start == 0:
            break
        if not page:
            break
        records.extend(page)
        if start >= last_known:
            break
        start += 10
        time.sleep(0.3)
    print(f"  pulled {len(records)} records, ~{(last_known+10) if last_known else len(records)} total")
    return records


def main():
    all_records = []
    by_piid = {}

    for vendor, label in VENDORS:
        try:
            records = sweep_vendor(vendor, label)
        except Exception as e:
            print(f"  !! sweep failed for {vendor}: {e}", file=sys.stderr)
            continue
        all_records.extend(records)
        # Dedupe to one record per PIID (keep latest by signed_date)
        for r in records:
            piid = r.get("piid")
            if not piid:
                continue
            prev = by_piid.get(piid)
            if prev is None or (r.get("signed_date") or "") > (prev.get("signed_date") or ""):
                by_piid[piid] = {**r, "_swept_as": label}

    print(f"\n\nTotal records across all sweeps: {len(all_records)}")
    print(f"Unique PIIDs: {len(by_piid)}")
    print()

    # Sort by total_obligated descending
    sorted_piids = sorted(by_piid.values(), key=lambda r: -r.get("total_obligated_amount", 0))
    print(f"Top 30 unique PIIDs by total_obligated:")
    for r in sorted_piids[:30]:
        v = (r["vendor_name"] or "")[:30]
        print(f"  {r['piid']:22s} {r['signed_date']:10s} ${r['total_obligated_amount']/1e6:>8.1f}M  {v:30s} {r['description'][:50]}")

    out = {
        "vendors_swept": [v[0] for v in VENDORS],
        "total_records": len(all_records),
        "unique_piids": len(by_piid),
        "piids": sorted_piids,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
