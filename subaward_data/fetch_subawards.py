"""Fetch USAspending subawards by PIID and save to JSON files.

Two-step process:
1. Look up prime award by PIID via /search/spending_by_award/ to get generated_internal_id
2. Pull all subawards via /subawards/ endpoint using the internal_id
"""
import urllib.request
import json
import time
import sys
import os

BASE = "https://api.usaspending.gov/api/v2"
OUTDIR = "/Users/brendantoole/projects2/buildco3/subaward_data"

def lookup_award(piid):
    """Find the generated_internal_id for a given PIID. Tries contracts then IDVs."""
    for award_types in (["A", "B", "C", "D"], ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]):
        payload = {
            "filters": {
                "award_ids": [piid],
                "time_period": [{"start_date": "2020-01-01", "end_date": "2026-09-30"}],
                "award_type_codes": award_types,
            },
            "fields": ["Award ID", "Recipient Name", "Award Amount", "generated_internal_id"],
            "limit": 5,
            "page": 1,
            "subawards": False,
        }
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{BASE}/search/spending_by_award/",
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "BuildCo-Research/1.0"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
            for r in result.get("results", []):
                if r.get("Award ID") == piid:
                    return {
                        "generated_internal_id": r.get("generated_internal_id"),
                        "recipient": r.get("Recipient Name"),
                        "amount": r.get("Award Amount"),
                    }
        except Exception as e:
            print(f"  Lookup error for {piid}: {e}", file=sys.stderr)
        time.sleep(0.2)
    return None


def fetch_subawards(award_id):
    """Fetch all subawards for a given generated_internal_id."""
    all_results = []
    for page in range(1, 21):  # up to 2000 results
        payload = {
            "award_id": award_id,
            "sort": "amount",
            "order": "desc",
            "limit": 100,
            "page": page,
        }
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{BASE}/subawards/",
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "BuildCo-Research/1.0"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode())
            results = result.get("results", [])
            if not results:
                break
            all_results.extend(results)
            if len(results) < 100:
                break
        except Exception as e:
            print(f"  Subaward fetch error page {page}: {e}", file=sys.stderr)
            break
        time.sleep(0.2)
    return all_results


def fetch_award_summary(award_id):
    """Get total subaward count and amount for an award."""
    try:
        req = urllib.request.Request(
            f"{BASE}/awards/{award_id}/",
            headers={"User-Agent": "BuildCo-Research/1.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        return {
            "subaward_count": result.get("subaward_count") or 0,
            "total_subaward_amount": result.get("total_subaward_amount") or 0,
        }
    except Exception as e:
        print(f"  Award summary error: {e}", file=sys.stderr)
        return {"subaward_count": 0, "total_subaward_amount": 0}


def process_batch(batch_name, piids):
    output = {}
    for piid, label in piids:
        print(f"[{batch_name}] {piid} ({label})...", file=sys.stderr)
        info = lookup_award(piid)
        if not info or not info.get("generated_internal_id"):
            print(f"  -> not found", file=sys.stderr)
            output[piid] = {"label": label, "found": False}
            continue

        award_id = info["generated_internal_id"]
        summary = fetch_award_summary(award_id)
        time.sleep(0.2)

        # Only fetch full subaward list if there are subawards
        if summary["subaward_count"] > 0:
            subs = fetch_subawards(award_id)
        else:
            subs = []

        output[piid] = {
            "label": label,
            "found": True,
            "generated_internal_id": award_id,
            "prime_recipient": info["recipient"],
            "prime_amount": info["amount"],
            "subaward_count": summary["subaward_count"],
            "total_subaward_amount": summary["total_subaward_amount"],
            "subawards": subs,
        }
        print(f"  -> {summary['subaward_count']} subawards, ${summary['total_subaward_amount']:,.0f} total", file=sys.stderr)
        time.sleep(0.3)

    outfile = os.path.join(OUTDIR, f"{batch_name}.json")
    with open(outfile, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {outfile}", file=sys.stderr)


BATCHES = {
    "ddg_construction": [
        ("N0002423C2307", "HII DDG-51 FY23-27"),
        ("N0002418C2307", "HII DDG-51 FY18-22"),
        ("N0002413C2307", "HII DDG-51 FY13-17"),
        ("N0002411C2307", "HII DDG-51 FY11"),
        ("N0002411C2309", "HII DDG-51 FY10"),
        ("N0002418C2305", "BIW DDG-51 FY18-22"),
        ("N0002423C2305", "BIW DDG-51 FY23-27"),
        ("N0002413C2305", "BIW DDG-51 FY13-17"),
        ("N0002411C2305", "BIW DDG-51 FY11"),
        ("N0002418C2313", "BIW DDG-51 Lead Yard FY18-22"),
        ("N0002424C2313", "BIW DDG-51 Lead Yard FY24+"),
    ],
    "ddg_1000": [
        ("N0002406C2303", "BIW DDG-1000 Detail Design"),
        ("N0002411C2306", "BIW DDG-1000 Construction"),
        ("N0002410C5126", "Raytheon DDG-1000 DMS"),
        ("N0002417C5145", "Raytheon DDG-1000 TSA"),
        ("N0002422C5522", "Raytheon DDG-1000 AS&M"),
        ("N0002423C2324", "HII DDG-1000 Mod Planning"),
        ("N0002424C2331", "BIW DDG-1000 Planning Yard"),
        ("N0002415C5344", "GDLS MK 46 MOD 2 Gun"),
        ("N0002403C5115", "LM DDG-51 Combat Systems"),
    ],
    "ddg_subsystems": [
        ("N0002422C5500", "Raytheon SPY-6 Production"),
        ("N0002425C5501", "Raytheon SPY-6 FoR"),
        ("N0002420C5503", "LM SLQ-32(V)6"),
        ("N0002416C5363", "LM SEWIP Block 2"),
        ("N0002409C5300", "LM SEWIP Block 2 older"),
        ("N0002415C5319", "NG SEWIP Block 3"),
        ("N0002422C5520", "NG SEWIP Block 3 design"),
        ("N0002416C5352", "GDMS SEWIP Block 1B3"),
        ("N0002414C5341", "GDMS SEWIP Block 1B3 LRIP"),
        ("N0002419C5200", "Raytheon CEC design agent"),
        ("N0002413C5212", "Raytheon CEC"),
        ("N0002425C5239", "Raytheon CEC follow-on"),
        ("N0002419C5603", "LM SSDS CSEA"),
        ("N0002414C5128", "Raytheon SSDS PSEA"),
    ],
    "weapons": [
        ("N0002418C5406", "Raytheon FY18 CIWS"),
        ("N0002419C5406", "Raytheon SeaRAM upgrade"),
        ("N0038319F0VP0", "Raytheon CIWS PBL"),
        ("N0002407C6119", "Raytheon SM-3"),
        ("N0002417C5410", "Raytheon FY17-21 SM"),
        ("N0002413C5403", "Raytheon FY13-17 SM"),
        ("N0002425C6401", "GDMS MK 54 MOD 1 LWT Sonar"),
        ("N0002418C6405", "Ultra Electronics MK 54 MOD 0 Array"),
    ],
    "lpd_lha": [
        ("N0002424C2473", "HII LPD 33/34/35"),
        ("N0002418C2406", "HII LPD 30/31/32"),
        ("N0002416C2431", "HII LPD 28"),
        ("N0002416C2415", "HII LPD 17 LCE&S"),
        ("N0002421C2443", "HII LPD 17 Class Eng"),
        ("N0002426C2443", "HII LPD 17 PD&ES"),
        ("N0002410C2203", "HII LPD 17 Class Eng older"),
        ("N0002421C2451", "BAE Norfolk LPD 28 FOA"),
        ("N0002410C2205", "Raytheon LPD 17 LCE&S"),
        ("N0002416C2427", "HII LHA 8 Bougainville"),
        ("N0002420C2437", "HII LHA 9"),
        ("N0002424C2467", "HII LHA 10 AP"),
        ("N0002425C4404", "NASSCO USS America LHA 6"),
    ],
    "lhd_maint": [
        ("N0002411C4407", "BAE Norfolk LHD 3 FY11"),
        ("N0002423C4408", "BAE Norfolk Kearsarge FY23"),
        ("N0002426C4405", "BAE Norfolk Iwo Jima FY26"),
        ("N0002425C4430", "BAE Norfolk Wasp FY25"),
        ("N0002421C4404", "BAE Norfolk Wasp FY21"),
        ("N0002424C4418", "Metro Machine Bataan FY24"),
        ("N0002422C4490", "Metro Machine Iwo Jima FY22"),
        ("N0002420C4467", "Metro Machine Bataan FY20"),
        ("N0002422C4420", "BAE SD Essex FY22"),
        ("N0002420C4308", "BAE SD Boxer DSRA"),
        ("N0002423C4404", "NASSCO Makin Island FY23"),
        ("N0002418C4404", "NASSCO Bonhomme Richard"),
    ],
    "lcs_mcm": [
        ("N0002413C6300", "LM LCS Integration"),
        ("N0002421C5105", "LM LCS Freedom"),
        ("N6339419F0043", "LM LCS Freedom Design Agent"),
        ("N6339424C0003", "LM LCS Freedom Combat ISEA"),
        ("N6339424C0004", "GDMS LCS Independence ISEA"),
        ("N0001923F2544", "Textron LCS Independence"),
        ("N0002411C2300", "LM LCS construction"),
        ("N0002414C6322", "Textron UISS"),
        ("N0002421C6304", "GDMS Knifefish UUV"),
        ("N0002417C6311", "NG Knifefish/LCS"),
        ("N0002422C6305", "Bollinger MCM USV"),
        ("N0002418C6300", "Raytheon Barracuda"),
        ("N0002415C6318", "NG ALMDS production"),
        ("N0002422C6418", "NG ALMDS production support"),
        ("N0002403C6310", "Raytheon AMNS Upgrade -3"),
        ("N0002410C6307", "Raytheon AMNS LRIP"),
        ("N0002417C6305", "Raytheon AMNS LRIP newer"),
        ("N6133111C0017", "GDMS Surface MCM Unmanned"),
    ],
    "misc": [
        ("N0002418C5392", "LM Aculight HELIOS"),
        ("N0002417C5375", "BAE L&A MK 110 MOD 0"),
        ("N0002412C5316", "BAE L&A MK 110 USCG NSC"),
        ("N6660418F3013", "SAIC SSTD Nixie"),
    ],
}


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "all":
        for name, piids in BATCHES.items():
            process_batch(name, piids)
    elif arg in BATCHES:
        process_batch(arg, BATCHES[arg])
    else:
        print(f"Unknown: {arg}. Options: {list(BATCHES.keys())} or 'all'", file=sys.stderr)
        sys.exit(1)
