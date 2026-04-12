#!/usr/bin/env python3
"""
FPDS per-mod pull for window-delta computation.

For each PIID in scope, pull all mods, filter to window 2020-01-01..2026-04-10,
sum per-mod obligatedAmount (this action only) for true window delta. Also
capture totalObligatedAmount at latest in-window mod (cumulative reported)
and the totalBaseAndAllOptionsValue ceiling for comparison.

Saves results incrementally to fpds_mod_data.json so a partial run can be
resumed.

Per Lessons-Learned §11: cache after every successful call, retry with
exponential backoff, polite delays.
"""

import json
import os
import sys
import time
from urllib import parse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree.ElementTree import fromstring

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "research-tool/1.0 (FY2026 SAM key programs analysis)"}

WINDOW_START = "2020-01-01"
WINDOW_END = "2026-04-10"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fpds_mod_data.json")

# All in-scope PIIDs from FY2026_Key_Programs_Contract_Awards.md
# Tagged with section and program for traceability
PIIDS = [
    # --- §1 DDG-51 New Construction ---
    ("N0002423C2307", "DDG-51 NEW CONSTRUCTION", "HII Ingalls FY23-27 MYP"),
    ("N0002423C2305", "DDG-51 NEW CONSTRUCTION", "BIW FY23-27 MYP"),
    ("N0002418C2307", "DDG-51 NEW CONSTRUCTION", "HII Ingalls FY18-22 MYP"),
    ("N0002418C2305", "DDG-51 NEW CONSTRUCTION", "BIW FY18-22 MYP"),
    ("N0002413C2305", "DDG-51 NEW CONSTRUCTION", "BIW FY13-17 MYP"),
    ("N0002413C2307", "DDG-51 NEW CONSTRUCTION", "HII DDG 117 FY13/16"),
    ("N0002418C2313", "DDG-51 NEW CONSTRUCTION", "BIW Lead Yard FY18-22"),
    ("N0002424C2313", "DDG-51 NEW CONSTRUCTION", "BIW Lead Yard FY24+"),
    ("N0002403C5115", "DDG-51 NEW CONSTRUCTION", "LM Aegis Combat System (legacy)"),
    # --- §2 DDG-1000 ---
    ("N0002406C2303", "DDG-1000", "BIW lead shipbuilder"),
    ("N0002410C5126", "DDG-1000", "Raytheon Mission Systems Integrator"),
    ("N0002417C5145", "DDG-1000", "Raytheon Total Ship Activation / MSE"),
    ("N0002422C5522", "DDG-1000", "Raytheon AS&M Support"),
    ("N0002423C2324", "DDG-1000", "HII DDG 1000/1001 Mod Planning"),
    ("N0002424C2331", "DDG-1000", "BIW Planning Yard Follow On"),
    ("N0002415C5344", "DDG-1000", "GD Land Systems MK 46 MOD 2 Gun"),
    # --- §3 LPD Flight II ---
    ("N0002424C2473", "LPD FLIGHT II", "HII LPD 33/34/35 block buy"),
    ("N0002418C2406", "LPD FLIGHT II", "HII LPD 30/31/32"),
    ("N0002416C2431", "LPD FLIGHT II", "HII LPD 28 Fort Lauderdale"),
    ("N0002416C2415", "LPD FLIGHT II", "HII LPD 17 LCE&S Core"),
    ("N0002421C2443", "LPD FLIGHT II", "HII LPD 17 Class Eng Svcs"),
    ("N0002426C2443", "LPD FLIGHT II", "HII LPD 17 PD&ES"),
    # --- §4 LHA Replacement ---
    ("N0002416C2427", "LHA REPLACEMENT", "HII LHA 8 Bougainville"),
    ("N0002420C2437", "LHA REPLACEMENT", "HII LHA 9"),
    ("N0002424C2467", "LHA REPLACEMENT", "HII LHA 10 AP"),
    # --- §12 DDG Modernization Subsystems ---
    # SPY-6
    ("N0002422C5500", "DDG MOD - SPY-6", "Raytheon AN/SPY-6(V) Production"),
    ("N0002425C5501", "DDG MOD - SPY-6", "Raytheon SPY-6 FoR design agent"),
    ("N0001424C1103", "DDG MOD - SPY-6", "RASP enhanced radar signal processing"),
    # SEWIP
    ("N0002420C5503", "DDG MOD - SEWIP", "LM SLQ-32(V)6 production"),
    ("N0002416C5363", "DDG MOD - SEWIP", "LM SEWIP Block 2 subsystems"),
    ("N0002409C5300", "DDG MOD - SEWIP", "LM AN/SLQ-32X(V) Block 2 (FY09)"),
    ("N0002415C5319", "DDG MOD - SEWIP", "NG SEWIP Block 3 pre-design"),
    ("N0002422C5520", "DDG MOD - SEWIP", "NG SEWIP Block 3 design agent"),
    ("N0002414C5341", "DDG MOD - SEWIP", "GDMS SEWIP Block 1B3 LRIP"),
    ("N0002416C5352", "DDG MOD - SEWIP", "GDMS SEWIP Block 1B3 systems"),
    # SSDS
    ("N0002419C5603", "DDG MOD - SSDS", "LM SSDS CSEA"),
    ("N0002414C5128", "DDG MOD - SSDS", "Raytheon SSDS PSEA"),
    # CEC
    ("N0002419C5200", "DDG MOD - CEC", "Raytheon CEC design agent"),
    ("N0002413C5212", "DDG MOD - CEC", "Raytheon CEC (FY13)"),
    ("N0002425C5239", "DDG MOD - CEC", "Raytheon CEC follow-on"),
    # CIWS
    ("N0002418C5406", "DDG MOD - CIWS", "Raytheon FY18 CIWS Production"),
    ("N0002419C5406", "DDG MOD - CIWS", "Raytheon SeaRAM upgrade"),
    ("N0002407C5437", "DDG MOD - CIWS", "Raytheon Mk 15 Phalanx R&D (FY07)"),
    # HELIOS
    ("N0002418C5392", "DDG MOD - HELIOS", "LM Aculight HELIOS"),
    # --- §16 Standard Missile ---
    ("N0002407C6119", "STANDARD MISSILE", "Raytheon SM-3 (FY07)"),
    ("N0002417C5410", "STANDARD MISSILE", "Raytheon FY17-21 SM Production"),
    ("N0002413C5403", "STANDARD MISSILE", "Raytheon FY13-17 SM Production"),
    ("N0002402C5319", "STANDARD MISSILE", "Raytheon SM (FY02)"),
    ("N0002400C5390", "STANDARD MISSILE", "Raytheon SM (FY00)"),
    ("N0002418C5407", "STANDARD MISSILE", "Raytheon SM DLMF/ILM"),
    # --- §17 MK-54 ---
    ("N0002425C6401", "MK-54", "GDMS MK 54 MOD 1 LWT Sonar Assembly"),
    ("N0002418C6405", "MK-54", "Ultra Electronics MK 54 MOD 0 Array Kits"),
    # --- §20 Ship Gun Systems ---
    ("N0002417C5375", "SHIP GUN SYSTEMS", "BAE 57mm MK 110 MOD 0 Gun Mount"),
    ("N0002412C5316", "SHIP GUN SYSTEMS", "BAE MK 110 Naval Gun (NSC)"),
    ("N0002418F5302", "SHIP GUN SYSTEMS", "BAE MK 110 GWS Engineering Services"),
    # --- §21 Airborne MCM ---
    ("N0002415C6318", "AIRBORNE MCM - ALMDS", "NG ALMDS production"),
    ("N0002422C6418", "AIRBORNE MCM - ALMDS", "NG ALMDS production support"),
    ("N0002403C6310", "AIRBORNE MCM - AMNS", "Raytheon AMNS Upgrade (FY03)"),
    ("N0002410C6307", "AIRBORNE MCM - AMNS", "Raytheon AMNS LRIP (FY09)"),
    ("N0002417C6305", "AIRBORNE MCM - AMNS", "Raytheon AMNS LRIP"),
    ("N0002425F6404", "AIRBORNE MCM - AMNS", "Raytheon AMNS Test & Depot Support"),
    ("N0002421F6412", "AIRBORNE MCM - AMNS", "Raytheon AMNS Test & Depot Support"),
    ("N0002418C6300", "AIRBORNE MCM - BARRACUDA", "Raytheon Barracuda mine neutralizer"),
    # --- §13 LCS Mission Modules ---
    ("N0002414C6322", "LCS MCM - UISS", "Textron UISS"),
    ("N0002421C6304", "LCS MCM - KNIFEFISH", "GDMS Knifefish Block 1 LRIP"),
    ("N0002417C6311", "LCS MCM - KNIFEFISH", "NG Knifefish/LCS systems"),
    ("N0002422C6305", "LCS MCM - MCM USV", "Bollinger MCM USV"),
    ("N6133111C0017", "LCS MCM - SMCM", "GDMS Surface MCM Unmanned"),
    # --- §10 LCS Freedom (Marinette flag PIID) ---
    ("N0002411C2300", "LCS FREEDOM", "LM Freedom Variant Construction (FY10)"),
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


def parse_amount(text):
    if not text:
        return 0.0
    try:
        return float(text)
    except (TypeError, ValueError):
        return 0.0


def parse_mods_from_xml(xml_text):
    """Yield dict per <entry> with mod-level fields we care about."""
    try:
        root = fromstring(xml_text)
    except Exception as e:
        print(f"  ! XML parse error: {e}", file=sys.stderr)
        return
    for entry in root.findall("a:entry", NS):
        content = entry.find("a:content", NS)
        if content is None:
            continue
        # Could be award, OtherTransactionAward, or OtherTransactionIDV
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

        mod = {
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
            "contract_action_type": get_attr(".//ns1:contractActionType", "description"),
        }
        yield mod


def pull_piid(piid, max_pages=300):
    """Pull all mods for a PIID. Returns list of mod dicts."""
    mods = []
    start = 0
    page = 0
    last_known = None
    while page < max_pages:
        q = f'PIID:"{piid}"'
        url = f"{BASE}&{parse.urlencode({'q': q})}&start={start}"
        try:
            xml_text = fetch(url)
        except Exception as e:
            print(f"  ! fetch failed at start={start}: {e}", file=sys.stderr)
            break
        if not xml_text:
            break

        page_mods = list(parse_mods_from_xml(xml_text))
        if not page_mods and page == 0:
            # No results at all
            break
        if not page_mods:
            break

        mods.extend(page_mods)

        # Find last page on first request
        if last_known is None:
            import re
            m = re.search(r'rel="last"[^>]*start=(\d+)', xml_text)
            last_known = int(m.group(1)) if m else 0

        # Have we exhausted?
        if start >= last_known:
            break
        start += 10
        page += 1
        time.sleep(0.3)
    return mods


def compute_window_delta(mods, start=WINDOW_START, end=WINDOW_END):
    """Per Lessons §14: sum per-mod obligatedAmount for in-window mods.
    Returns dict with summary stats."""
    in_window = [m for m in mods if start <= (m.get("signed_date") or "") <= end]
    out = {
        "total_mods_pulled": len(mods),
        "in_window_mods": len(in_window),
        "window_delta_obligated": sum(m["obligated_amount"] for m in in_window),
        "earliest_signed": min((m["signed_date"] for m in mods if m.get("signed_date")), default=""),
        "latest_signed": max((m["signed_date"] for m in mods if m.get("signed_date")), default=""),
        "earliest_in_window_signed": min((m["signed_date"] for m in in_window), default=""),
        "latest_in_window_signed": max((m["signed_date"] for m in in_window), default=""),
    }
    if in_window:
        # Cumulative at latest in-window mod (the existing "Cumulative Obligated" col)
        latest = max(in_window, key=lambda m: (m.get("signed_date") or "", m.get("mod_number") or ""))
        out["latest_in_window_total_obligated"] = latest["total_obligated_amount"]
        out["latest_in_window_ceiling"] = latest["total_base_and_all_options_value"]
        out["latest_in_window_mod_number"] = latest["mod_number"]
        out["latest_in_window_description"] = latest["description"][:200]
    else:
        out["latest_in_window_total_obligated"] = 0.0
        out["latest_in_window_ceiling"] = 0.0
        out["latest_in_window_mod_number"] = ""
        out["latest_in_window_description"] = ""
    # Pre-window state for sanity check
    pre = [m for m in mods if (m.get("signed_date") or "") < start]
    if pre:
        latest_pre = max(pre, key=lambda m: (m.get("signed_date") or "", m.get("mod_number") or ""))
        out["pre_window_total_obligated"] = latest_pre["total_obligated_amount"]
        out["pre_window_latest_signed"] = latest_pre["signed_date"]
    else:
        out["pre_window_total_obligated"] = 0.0
        out["pre_window_latest_signed"] = ""
    # Cumulative-method delta (from totals)
    out["window_delta_via_totals"] = (
        out["latest_in_window_total_obligated"] - out["pre_window_total_obligated"]
    )
    # Vendor / description from base mod (mod 0) if present
    base = next((m for m in mods if m.get("mod_number") in ("0", "")), None)
    out["base_vendor"] = base["vendor_name"] if base else (mods[0]["vendor_name"] if mods else "")
    out["base_description"] = (base["description"] if base else (mods[0]["description"] if mods else ""))[:200]
    return out


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
        json.dump(data, f, indent=2)
    os.replace(tmp, OUT)


def main():
    data = load_existing()
    print(f"Loaded {len(data)} cached PIIDs from {OUT}")
    print(f"Total PIIDs to process: {len(PIIDS)}")
    print(f"Window: {WINDOW_START} to {WINDOW_END}\n")

    for i, (piid, section, label) in enumerate(PIIDS, 1):
        if piid in data and data[piid].get("_complete"):
            print(f"[{i}/{len(PIIDS)}] {piid} -- cached, skip")
            continue
        print(f"[{i}/{len(PIIDS)}] {piid} ({section}: {label})")
        try:
            mods = pull_piid(piid)
        except Exception as e:
            print(f"  !! ERROR: {e}", file=sys.stderr)
            data[piid] = {"section": section, "label": label, "error": str(e), "_complete": False}
            save_data(data)
            continue
        summary = compute_window_delta(mods)
        record = {
            "section": section,
            "label": label,
            **summary,
            "mods": mods,  # full mod list for downstream verification
            "_complete": True,
        }
        data[piid] = record
        save_data(data)
        # Print key stats
        print(f"  mods={summary['total_mods_pulled']:3d}  in_window={summary['in_window_mods']:3d}  "
              f"window_delta=${summary['window_delta_obligated']/1e6:>9.1f}M  "
              f"latest_cumulative=${summary['latest_in_window_total_obligated']/1e6:>10.1f}M")
        time.sleep(0.4)

    print(f"\nDone. Wrote {len(data)} PIIDs to {OUT}")


if __name__ == "__main__":
    main()
