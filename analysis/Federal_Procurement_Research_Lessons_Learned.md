# Federal Procurement Research -- Lessons Learned & Best Practices

Field notes from actually pulling FPDS + USAspending data for the SAM
submarine and cutter program analysis (April 2026). These are the
gotchas, workflow patterns, and traps that the standing
`federal_procurement_data_guide.txt` doesn't fully cover -- written from
fresh experience, not theory.

This file is a **companion** to `federal_procurement_data_guide.txt` (the
field reference) and the three program-level award files. Think of the
guide as "what the APIs do" and this file as "what to actually watch out
for when you use them."

---

## Table of Contents

1. [The 80/20 Workflow](#1-the-8020-workflow)
2. [FPDS Field-Name Traps](#2-fpds-field-name-traps)
3. [FPDS Query Tokenization & Result Bloat](#3-fpds-query-tokenization--result-bloat)
4. [The Three-Round Search Pattern](#4-the-three-round-search-pattern)
5. [USAspending Subaward Workflow](#5-usaspending-subaward-workflow)
6. [Subaward Reporting Gaps -- Who Doesn't Report](#6-subaward-reporting-gaps--who-doesnt-report)
7. [Data Quality Outliers to Watch For](#7-data-quality-outliers-to-watch-for)
8. [Vendor Identity Problems](#8-vendor-identity-problems)
9. [Federal Shipyards & Other Invisible Work](#9-federal-shipyards--other-invisible-work)
10. [Team Build Contracts -- The HII/EB Submarine Pattern](#10-team-build-contracts--the-hiieb-submarine-pattern)
11. [Letter Contracts, IDIQ Ceilings, & Obligation Lag](#11-letter-contracts-idiq-ceilings--obligation-lag)
12. [Pre-Flight Checklist for a New Domain Pull](#12-pre-flight-checklist-for-a-new-domain-pull)
13. [Quick-Reference Code Snippets](#13-quick-reference-code-snippets)
14. [The Cumulative-vs-Window Trap (Worked Example)](#14-the-cumulative-vs-window-trap-worked-example)
15. [Reading Mod Descriptions to Identify Programs](#15-reading-mod-descriptions-to-identify-programs)

---

## 1. The 80/20 Workflow

When you have a list of programs and need contractor data fast, this is
the pipeline that produces clean results in the least time:

```
1. Description-keyword search in FPDS
   ↓ (extract top vendors + top PIIDs)
2. Vendor-name search in FPDS for the primes you found
   ↓ (catches contracts the description search missed)
3. USAspending /search/spending_by_award/ to get generated_internal_id
   ↓ (one lookup per PIID you care about)
4. USAspending /subawards/ to pull the full sub tree
   ↓ (aggregate by recipient_name, rank by amount)
5. Cross-reference: agency code + obligated-amount filter
   ↓ (catches the new awards that haven't surfaced via keywords yet)
```

The single most useful "catch-all" query in this whole project was:

```
DEPARTMENT_ID:"7000" AGENCY_CODE:"7008"
SIGNED_DATE:[2020/01/01,2026/12/31]
OBLIGATED_AMOUNT:[50000000,99999999999]
```

That query (USCG, FY20-26, >$50M obligated) returned 38 records covering
**every** major USCG cutter award including the Davie, Rauma, and
Bollinger Arctic Security Cutter awards from late 2025/early 2026 that
I would have missed entirely if I'd only done description-keyword searches.

**Lesson:** After doing your keyword and vendor searches, always run an
agency + dollar-floor sweep as a backstop. It catches whatever fell
through the keyword cracks.

---

## 2. FPDS Field-Name Traps

The federal_procurement_data_guide.txt lists `UEI_NAME` as the vendor
search field. **It works, but it's not the only one, and it's not the
best one.** Here's what I found by direct testing:

| Field Name | Behavior |
|---|---|
| `VENDOR_NAME:"ELECTRIC BOAT"` | **WORKS** -- 34,140 records (USCG + Navy + small) |
| `CONTRACTOR_NAME:"ELECTRIC BOAT CORPORATION"` | **WORKS** -- but pulls broader fuzzy matches (3.97M records) |
| `GLOBAL_VENDOR_NAME:"ELECTRIC BOAT CORPORATION"` | **WORKS** -- 18.6M records (very broad) |
| `UEI_NAME:ELECTRIC` (no quotes) | Works partially -- 557K records |
| `UEI_NAME:"GENERAL DYNAMICS ELECTRIC BOAT CORPORATION"` | **0 results** -- exact-match fails |
| `VENDOR_FULL_NAME:"GENERAL DYNAMICS ELECTRIC BOAT"` | **0 results** -- field doesn't exist |
| `LEGAL_BUSINESS_NAME:"ELECTRIC BOAT"` | **0 results** -- field doesn't exist |
| `GLOBAL_DUNS_NAME:"ELECTRIC BOAT"` | **0 results** -- field doesn't exist |
| `VENDOR_UEI:WMPLJ3NRCJ43` (UEI code) | **0 results** -- direct UEI lookup fails too |

**Use `VENDOR_NAME:"..."` as your default vendor search field.** It's the
most reliable. `CONTRACTOR_NAME` is a fallback if you suspect the legal
name has variants.

PIID lookup also has a trap:

| Field | Behavior |
|---|---|
| `PIID:N0002419C2116` | **0 results** -- direct PIID lookup doesn't work |
| `PIID:"N00024-19-C-2116"` (hyphenated) | **0 results** |

There is no clean way to look up a single contract by PIID directly in
FPDS Atom. You have to find it via vendor name + signed date, then
filter the results in code. **For PIID-based lookups, use USAspending's
`/search/spending_by_award/` endpoint with the `award_ids` filter
instead** -- it actually works.

---

## 3. FPDS Query Tokenization & Result Bloat

FPDS's "exact phrase" matching is **not** truly exact. The Atom feed
tokenizes inside quoted strings on whitespace and certain punctuation,
which causes two failure modes:

### Failure mode 1: Hyphens kill matches

```
DESCRIPTION_OF_REQUIREMENT:"MK-48"     →    2 records
DESCRIPTION_OF_REQUIREMENT:"MK 48 TORPEDO"  →  24,490 records
DESCRIPTION_OF_REQUIREMENT:"MK-48 MOD 7"  →  1 record
```

The hyphen in "MK-48" appears to break the tokenizer. When you can't
find what you expect, **try removing hyphens and slashes**.

### Failure mode 2: Multi-word phrases match individual words

```
DESCRIPTION_OF_REQUIREMENT:"SUBMARINE SUPPORT EQUIPMENT"
  → 1,021,250 records (102,125 pages)
```

That should be a niche search. Instead it returned a million records
because FPDS appears to OR the words rather than match the phrase.
Quoting helps but doesn't fully constrain.

**Mitigation:**
- Always check the `<link rel="last">` page count before paginating
- If it shows >1,000 records on a query you expected to be tight,
  STOP and refine -- you're going to waste pagination on noise
- Add a second `DESCRIPTION_OF_REQUIREMENT:` clause to AND-narrow:
  ```
  DESCRIPTION_OF_REQUIREMENT:"SUBMARINE"
  DESCRIPTION_OF_REQUIREMENT:"ACOUSTIC"
  ```
  Two clauses get ANDed and dramatically reduce result count.
- Add agency or vendor constraints to narrow further
- **Always post-filter** the description field in your code with a
  proper regex

### Failure mode 3: ANDed phrases that look the same return different counts

```
DESCRIPTION_OF_REQUIREMENT:"NAVAL REACTOR"   →  49,670 records
DESCRIPTION_OF_REQUIREMENT:"NUCLEAR REACTOR"   → likely millions
```

"Naval reactor" is the actual term of art for the submarine reactor
program, but the search returned mostly unrelated NAVAIR results
because "naval" and "reactor" matched separately. The vendor-based
search for `BECHTEL PLANT MACHINERY` was 100x more useful for this
domain.

**Lesson:** When a description search returns absurd numbers, switch
strategies to vendor-name search instead.

---

## 4. The Three-Round Search Pattern

For any new program domain, run three rounds of FPDS pulls in order:

### Round 1: Description keywords (cast a wide net)

Start with the program's official name and a couple of obvious variants.
Use date + agency filters to constrain.

```python
queries = [
    'DESCRIPTION_OF_REQUIREMENT:"VIRGINIA CLASS" SIGNED_DATE:[2020/01/01,2026/12/31] AGENCY_CODE:"9700"',
    'DESCRIPTION_OF_REQUIREMENT:"COLUMBIA CLASS" SIGNED_DATE:[2020/01/01,2026/12/31] AGENCY_CODE:"9700"',
    'DESCRIPTION_OF_REQUIREMENT:"FAST RESPONSE CUTTER" SIGNED_DATE:[2020/01/01,2026/12/31]',
]
```

What you're looking for in Round 1: **the names of the prime
contractors**. You don't yet care about specific PIIDs.

### Round 2: Vendor-name searches for the primes you found

Now that you know who the primes are, query them directly. This catches
contracts that have vague or non-matching descriptions.

```python
queries = [
    'VENDOR_NAME:"ELECTRIC BOAT CORPORATION" SIGNED_DATE:[2020/01/01,2026/12/31]',
    'VENDOR_NAME:"BOLLINGER" SIGNED_DATE:[2020/01/01,2026/12/31]',
    'VENDOR_NAME:"BECHTEL PLANT MACHINERY" SIGNED_DATE:[2020/01/01,2026/12/31]',
]
```

In this project, Round 2 is what surfaced the Bechtel naval-reactor
contracts ($18B in obligations) -- they had vague "FUNDING ACTION" or
"DE-OBLIGATION" descriptions that no description-keyword search would
ever find.

### Round 3: Agency + dollar-floor backstop

After Rounds 1 and 2, run a sweep to catch what's left:

```python
queries = [
    'DEPARTMENT_ID:"7000" AGENCY_CODE:"7008" SIGNED_DATE:[2020/01/01,2026/12/31] OBLIGATED_AMOUNT:[50000000,99999999999]',
    'AGENCY_CODE:"9700" SIGNED_DATE:[2020/01/01,2026/12/31] OBLIGATED_AMOUNT:[100000000,99999999999]',
]
```

This is where the Davie Defense / Rauma Marine / Bollinger Arctic
Security Cutter awards surfaced -- none of which would have been caught
by description searches because "Arctic Security Cutter" wasn't yet a
known program name when I built my keyword list.

**Lesson:** New programs are invisible to keyword search until you know
their names. The dollar-floor backstop is how you find programs you
didn't know existed.

---

## 5. USAspending Subaward Workflow

The `/api/v2/subawards/` endpoint is **the** killer feature of
USAspending for competitive analysis. The existing
`SAM_Program_Contract_Awards.md` and `SAM_Program_Component_Contracts.md`
files were entirely rewritten on 2026-04-10 because of this endpoint --
it surfaces tens of billions of dollars of subcontractor activity that
prime-only FPDS searches completely miss.

But the workflow is non-obvious. You can't just hit `/subawards/` with
a PIID -- you need a `generated_internal_id` first.

### The two-call pattern

```python
# Step 1: Look up the generated_internal_id for a PIID
search_payload = {
    "filters": {
        "award_type_codes": ["A", "B", "C", "D"],   # Contracts group
        "award_ids": ["N0002417C2100"],
        "time_period": [{"start_date": "2007-10-01", "end_date": "2026-09-30"}],
    },
    "fields": ["Award ID", "generated_internal_id", "Recipient Name", "Award Amount"],
    "limit": 50,
    "page": 1,
}
resp = requests.post(
    "https://api.usaspending.gov/api/v2/search/spending_by_award/",
    json=search_payload,
).json()

# Get the generated_internal_id
gid = resp["results"][0]["generated_internal_id"]
# e.g. "CONT_AWD_N0002417C2100_9700_-NONE-_-NONE-"

# Step 2: Pull subawards by gid
sub_payload = {
    "award_id": gid,
    "limit": 100,
    "page": 1,
    "sort": "amount",
    "order": "desc",
}
subs = requests.post(
    "https://api.usaspending.gov/api/v2/subawards/",
    json=sub_payload,
).json()
```

### The retry-by-group requirement

If Step 1 returns no results with `award_type_codes: ["A", "B", "C", "D"]`,
**try the IDV group too** before giving up:

```python
search_payload["filters"]["award_type_codes"] = [
    "IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C",
    "IDV_C", "IDV_D", "IDV_E"
]
```

Many "PIIDs" in FPDS are actually task orders against IDIQ vehicles, and
those live under the IDV group. The two groups can't be mixed in one
call (HTTP 422), so you have to retry.

### The 2,000-record cap

The subaward endpoint has a practical ceiling around 2,000 records per
prime. The Virginia Block V prime (`N0002417C2100`) has more than 2,000
subaward records in the FY20-26 window -- I capped it at 2,000 and the
total still came to $4.14B. **For really large primes you'll be missing
the long tail.** That's OK for a top-20 sub list but be aware when
quoting "total subaward dollars" figures.

### The intra-corporate sub trap

Subaward records sometimes show one division of a parent company doing
work for another division of the same parent. Examples I saw:

- **GD Mission Systems** appearing as a $465M sub on the Lockheed Martin
  Trident SSBN material contract (`N0002417C6259`) -- this is Trident
  fire control work that LM is integrating but GD actually builds.
- **GD Mission Systems** appearing as a $608M sub on the Northrop
  Grumman Knifefish contract -- Independence-variant LCS combat systems.
- **Northrop Grumman Systems** appearing as a $1.27B sub on the Electric
  Boat Virginia Block V contract -- could be NG sonar work, OR could
  partly be HII Newport News team-build work routed through NG?
  (Unclear from the data.)

**Lesson:** Don't double-count parent companies. When summing up
"Northrop Grumman" exposure to a program, look at both NG primes and NG
subs but make sure the same dollars aren't being counted in both sides.

### The Round-Number Test

If a sub record shows a perfectly round number (e.g., $39,157,945,400 or
$1,000,000,000), **that's almost certainly a data error**. I hit this
exactly once: the L3Harris Trident D5 Flight Test Instrumentation
contract (`N0003022C2001`) had a CPI Satcom sub record at **$39
trillion**. The valid sub data on that PIID maxes out at $22M. The
$39T number came from 5 individual records that were clearly mis-keyed
in the source feed.

**Sanity check rule:** Any single sub line over $5B should be manually
verified before you put it in a report. The largest legitimate sub I
found in this whole project was BlueForge Alliance at $4.21B -- and
that's a real consortium pass-through.

---

## 6. Subaward Reporting Gaps -- Who Doesn't Report

A huge finding from this project: **many primes report 0 subawards**,
not because they don't subcontract, but because they don't comply with
FFATA reporting requirements (or report through a different channel).

Primes with 0 reported subs across all their FY20-26 contracts in this
project:

| Prime | Contracts with 0 subs | Notes |
|---|---|---|
| Bath Iron Works (DDG-51) | 6 PIIDs, ~$15B in primes | Per existing SAM file |
| Bollinger Mississippi Shipbuilding | Polar Security Cutter ($2.02B) | Post-acquisition |
| Bollinger Shipyards Lockport | FRC ($2.08B + $1.54B), Arctic Security Cutter ($921M) | All Bollinger entities |
| VT Halter Marine | Pre-acquisition PSC records | Acquired by Bollinger Nov 2022 |
| Birdon America | All WCC contracts ($430M obligated) | New program ramping |
| Austal USA | OPC Stage 2 ($1.40B) | Contract too new |
| Eastern Shipbuilding Group | Most non-OPC contracts | OPC PIID does report |
| Rauma Marine Constructions Oy (FI) | Arctic Security Cutter ($520M) | Foreign prime |
| Davie Defense Inc (CA) | Multi-Purpose Polar ($180M / $3.5B ceiling) | Foreign prime |
| Offshore Service Vessels LLC | CAPI Aiviq ($127M) | Vessel purchase, not construction |
| Bechtel Plant Machinery | Older naval reactor PIIDs | Newer ones DO report |
| Lockheed Martin Sippican | Smaller MK-48 contracts (`N0002411C6404`, `N0002418C6408`) | Larger one DOES report |

Patterns I observed:

1. **Foreign-owned primes don't report.** Rauma (Finland), Davie (Canada),
   VT Halter (pre-acq, Singapore-owned ST Engineering)
2. **New contracts (last 12-24 months) don't yet have sub records.**
   Subaward reporting lags prime obligation.
3. **Some US primes are systematically non-compliant** (Bollinger,
   BIW, Birdon). This is a known FFATA enforcement gap.
4. **The same prime can report on one contract and not another.**
   Bechtel and Lockheed Martin Sippican both have this pattern.

**Mitigation:** When you see "0 subs" on a major contract, don't report
it as "no subcontracting activity." Instead, say:

> Subawards: 0 reported -- Bollinger does not report subawards in
> USAspending. Known suppliers from public sources include [X, Y, Z].

And then fill the gap with FPDS-visible contracts to known component
vendors (e.g., MTU diesels, Hamilton Jet waterjets, Furuno radar) and
press releases.

---

## 7. Data Quality Outliers to Watch For

In the course of pulling this data I hit several types of data errors.
Build defensive checks for each:

### The $39 trillion subaward (mis-keyed amount)

```
N0003022C2001 CPI Satcom & Antenna Technologies: $39,157,945,400,000
```

A real sub record but the amount is off by 1,000,000x. **Check: any
single sub line >$5B should be flagged for manual review.**

### Negative obligations

I saw `total_obligated_amount` come back as `-$0.00M` and `-$189,198`
on several Austal LCS records. These are de-obligations -- valid but
they make sorting confusing. **Check: when computing rankings, use
`abs()` or filter out negatives explicitly.**

### Same PIID, two vendor names (novation)

```
N0002419C2210
  → VENDOR: VT HALTER MARINE, INC. (signed 2023-01-11) → $1.38B obligated
  → VENDOR: BOLLINGER MISSISSIPPI SHIPBUILDING (signed 2025-12-15) → $2.02B obligated
```

VT Halter was acquired by Bollinger in November 2022 and the contract
was novated. Both vendor names appear in FPDS for the same PIID. **If
you dedupe by PIID alone, you'll keep only the latest mod and lose the
historical vendor name.** Track novations explicitly.

### Description fields that contain other contracts' content

```
N0002418C2307 (HII DDG-51 FY18-22 prime)
  description: "SPQ-9B PERISCOPE DETECTION AND DISCRIMINATION UPGRADE
                FLIGHT III (ICP-3564 CONSTRUCTION..."
```

This is a $6.7B DDG-51 construction contract whose latest mod was for
a periscope detection radar upgrade. A search for
`DESCRIPTION_OF_REQUIREMENT:"PERISCOPE"` returned this contract as a
top result, which is technically correct but contextually misleading.
**Check: when filtering descriptions for a topic, look at the full
contract context (PIID, vendor, dollar value) before drawing conclusions.**

### Hard-coded test/sample data

```
HSCG2316CADB016 (HII NSC Production)
  description includes "MK-48 MOD 2 GWS"
```

This is the USCG MK-48 25mm gun, NOT the Navy MK-48 heavyweight
torpedo. They share a designation. **Check: the same nomenclature
across services means different things. Always verify against the
contracting agency.**

---

## 8. Vendor Identity Problems

Federal vendor data has inconsistent naming. Here are the patterns
that bit me:

### Acquisitions and rebrands

| Old Name | New Name | When |
|---|---|---|
| ATK Launch Systems LLC | Northrop Grumman Innovation Systems | 2018 (NG acq Orbital ATK) |
| L3 Technologies | L3Harris Technologies | 2019 (L3/Harris merger) |
| United Launch Alliance | -- | -- |
| Kollmorgen Photonics | L3Harris Maritime Services | 2017 |
| Raytheon Company | RTX Corporation | 2020 (Raytheon/UTC merger) |
| Earl Industries | BAE Systems Norfolk Ship Repair | 2014 (BAE acq) |
| VT Halter Marine | Bollinger Mississippi Shipbuilding | Nov 2022 |
| MTU Detroit Diesel | Rolls-Royce Solutions America | -- |
| Coltec Industries | Fairbanks Morse Defense (parent) | -- |
| Fincantieri Marine | Fincantieri Marinette Marine | -- |
| AAI Corporation | Textron Systems | -- |
| Engility Corporation | SAIC (acquired) | 2019 |
| ManTech | acquired by Carlyle Group | 2022 |
| Cobham Advanced Electronic Solutions | CAES Systems / CAES Mission Systems | -- |

When aggregating spend across rebrands, you need a parent company table.
The federal data shows the legal entity at the time of award, which can
make a single parent appear as 5+ different "vendors."

### Multiple legal entities under one parent

General Dynamics is the worst offender:
- General Dynamics Electric Boat Corporation
- General Dynamics Mission Systems, Inc.
- General Dynamics Information Technology
- General Dynamics Land Systems
- General Dynamics Advanced Information Systems
- General Dynamics-OTS (Ordnance & Tactical Systems)
- GDIT (yet another spelling)
- Bath Iron Works Corporation (also GD)

When summing "GD exposure to submarines," you need to roll up all of
these. The existing SAM files mostly do this in the summary tables.

### "Inc." vs "Incorporated" vs "L.L.C." vs ", LLC"

```
"BOLLINGER SHIPYARDS LOCKPORT, L.L.C."  ← FPDS
"Bollinger Shipyards Lockport LLC"       ← USAspending
"Bollinger Shipyards Inc."               ← press releases
```

When deduping vendor names, normalize:
1. Strip trailing punctuation (commas, periods)
2. Strip suffixes: INC, LLC, CORP, CORPORATION, CO, LTD, LP, L.P., L.L.C.
3. Strip CITY/STATE designators if they're separable
4. Uppercase everything
5. Collapse multiple spaces

Do this **before** you aggregate or compare.

### The "Inc" alone trap

USAspending sometimes returns just `"Inc."` or `"L.L.C."` as the
recipient name when the underlying record is malformed. Treat these as
"unknown" and exclude from rankings.

---

## 9. Federal Shipyards & Other Invisible Work

This is the biggest blind spot in FPDS for naval procurement: **the
four public naval shipyards perform billions of dollars of submarine
and carrier depot maintenance every year, and none of it appears in
FPDS or USAspending**.

| Shipyard | Mission | FY26 estimated workforce |
|---|---|---|
| Norfolk Naval Shipyard (NNSY), VA | SSN/SSBN/CVN East Coast | ~10,000 federal |
| Portsmouth Naval Shipyard (PNSY), ME | SSN East Coast attack subs | ~6,000 federal |
| Pearl Harbor Naval Shipyard & IMF (PHNSY), HI | Pacific SSN/SSBN | ~6,000 federal |
| Puget Sound Naval Shipyard & IMF (PSNS), WA | Pacific SSN/SSBN/CVN | ~14,000 federal |

Combined, these four yards consume the bulk of the **$5.21B SSN +
$878M SSBN OMN_Vol2 depot maintenance lines** in the FY26 SAM. None of
that money flows through contracts. It's federal payroll, federal
materiel procurement (which IS in FPDS but gets filed under generic
DLA descriptions), and federal facilities operations.

Other invisible work:
- **Navy Working Capital Fund (NWCF)** orders -- these show up partially
  in FPDS but with vague descriptions
- **Federally Funded R&D Centers (FFRDCs)** like JHU APL, Penn State
  ARL, MIT Lincoln Lab -- they appear as primes but their underlying
  task orders are often classified or aggregated
- **Classified work** -- the entire intelligence community submarine
  payload (e.g., the SubGroup 9 / NSA undersea cable taps) is invisible
- **First-tier sub work that doesn't trigger FFATA reporting**
  ($30K threshold; non-compliance gap)
- **Foreign Military Sales (FMS) cases** that flow to US primes show
  up but are hard to filter from US-funded work without parsing
  description fields carefully
- **University research grants** -- visible in NSF/NIH databases but
  not always in FPDS

**Lesson:** When the SAM sheet shows $5B for SSN depot maintenance and
your FPDS pull only finds ~$50M of relevant prime contracts, **the
99% missing is federal shipyard work, not a search failure**.

---

## 10. Team Build Contracts -- The HII/EB Submarine Pattern

This is a specific pattern that completely confused me until I worked
through the data:

**Both Virginia and Columbia class submarines are built by a team of
two shipyards: General Dynamics Electric Boat (Groton, CT) and HII
Newport News Shipbuilding (Newport News, VA).** Per the team
agreements:
- Virginia: ~50/50 work split
- Columbia: ~78/22 work split (EB lead, HII partner)

But in FPDS, **only Electric Boat appears as the prime of record** on
all SCN 2013 (Virginia) and SCN 1045 (Columbia) contracts. HII NNS does
not appear as a separate prime on submarine contracts. Their work
flows through EB via the team agreement.

This means:
1. A keyword search for `VENDOR_NAME:"NEWPORT NEWS"` looking for sub
   contracts will return... aircraft carrier contracts. 0 subs. The
   sub work is invisible.
2. A subaward pull on the EB Virginia/Columbia primes shows
   "Northrop Grumman Systems" as a $1.27B Virginia + $669M Columbia
   sub. **Some of that NG sub is genuine NG work; some of it might be
   HII NNS work that's been routed through NG as a flow-through.** The
   data doesn't distinguish.
3. To see HII's actual share of a sub program, you have to read HII
   investor filings, not federal procurement data.

Other team builds and joint ventures with similar visibility issues:
- **LCS Independence**: Austal USA prime, GDMS as combat system
  partner -- both visible
- **LCS Freedom**: Lockheed Martin prime, Marinette Marine
  (Fincantieri) as the actual builder. Marinette appears as a $47B
  sub on the LM prime, which is a massive finding from the existing
  SAM file -- but only because LM does report subs on that contract.
- **LHA/LPD**: HII Ingalls prime, sole-source. No team partner. Clean
  visibility.
- **TMASC Joint Venture**: TASC + Modern Technology Solutions joint
  venture for LPD program office. Appears as TMASC in FPDS.

**Lesson:** Always check whether a program is a team build before
drawing conclusions about vendor share. If it is, the prime of
record's sub data is your only window into the partner's work, and
even that is incomplete.

---

## 11. Letter Contracts, IDIQ Ceilings, & Obligation Lag

The relationship between "ceiling" and "obligated" is critical for
interpreting contract data, and the federal procurement guide
under-emphasizes this.

### IDIQ master + task orders

The Birdon Waterways Commerce Cutter is the cleanest example:

```
70Z02323D93270001  Birdon America Inc  $3.8M obligated / $1,196M ceiling
  ↓ task orders against the master ↓
70Z02324F93270004                      $106M obligated
70Z02325F93270007                       $84M obligated
70Z02325F93270005                       $74M obligated
70Z02323F93250008                       $47M obligated
70Z02323F93270002                       $40M obligated
70Z02324F93250008                       $38M obligated
70Z02325F93270002                       $37M obligated
... (50+ more task orders) ...
```

The master IDIQ (`70Z02323D93270001`) has only **$3.8M obligated**
against a **$1.20B ceiling**. That looks like an empty contract until
you realize that all the actual money is being obligated against the
**task orders**, which are separate FPDS records but reference the
master via `referencedIDVID/PIID`.

**Mitigation:**
- Always query the master IDIQ AND its task orders separately
- Sum task order obligations to get the real spend
- Don't report the master's "obligated" as the program total -- report
  the sum across the IDV tree

### Letter contracts (undefinitized)

Several USCG cutter awards in this project are "letter contracts" --
provisional awards made before terms are finalized:

```
70Z02326C93210002  Bollinger Shipyards Lockport
  $921.7M obligated / $2,143M ceiling
  description: "LETTER CONTRACT AWARD OF ARCTIC SECURITY CUTTERS"

70Z02326C93210003  Davie Defense Inc.
  $180.0M obligated / $3,500M ceiling
  description: "LETTER CONTRACT...FIVE (5) MULTI-PURPOSE POLAR ICEBREAKERS"
```

Letter contracts have HUGE ceilings (the full multi-year program
authorization) but tiny obligations (just the initial undefinitized
release). Over the next 12-18 months, the obligations will catch up to
some fraction of the ceiling.

**For market sizing:** Use ceiling, not obligated, when discussing
"this contract is worth up to X."
**For year-by-year competitive analysis:** Use obligated. Don't overstate.

### Obligation lag

A new prime contract signed in March 2026 will:
- Appear in FPDS within 30-90 days
- Show subawards in USAspending **6-18 months later**

Several of the most interesting findings in this project (Davie Defense,
Rauma Marine, Bollinger Arctic Security Cutter, Birdon WCC task orders)
have **0 subaward records** because the contracts are too fresh. Come
back in 12 months and the sub data will be there.

**Lesson:** When pulling sub data for "the latest contracts," expect
gaps. Tag those primes as "subaward data not yet available" rather than
"no subs."

---

## 12. Pre-Flight Checklist for a New Domain Pull

Before you start hitting the APIs for a new program domain, work
through this checklist:

### 1. Build the program ↔ prime ↔ keyword crosswalk first

Don't start by querying. Start with a spreadsheet that maps:

| Program Name | Hull/System | Funding Line | Known Prime | Search Keywords |
|---|---|---|---|---|

For my submarine pull, the SAM Excel sheet itself was the crosswalk.
For a domain you're new to, build it from:
- Program budget justification books (PB books / J-Books)
- DOT&E annual report
- GAO weapons system reports
- CRS reports for the program

### 2. Identify known program rebrands and successors

E.g., for the OPC: Eastern Shipbuilding had Stage 1, Austal USA has
Stage 2. If you only search for "Eastern Shipbuilding" you'll miss
half the program. If you only search "OFFSHORE PATROL CUTTER" you'll
catch both but also a lot of unrelated NOAA hydrographic survey work.

### 3. Check for novations

Has any major prime been acquired recently? In this project:
- VT Halter Marine → Bollinger Mississippi Shipbuilding (Nov 2022)
- Orbital ATK → Northrop Grumman (2018)
- Raytheon Company → RTX Corporation (2020)
- L3 Technologies → L3Harris (2019)

You need to query both the old and new vendor names to catch the full
window.

### 4. Identify federal-employee performers

For naval programs, list the federal facilities that perform work
in-house (Norfolk Naval Shipyard, Portsmouth Naval Shipyard, NSWC
Crane, NUWC Newport, NAVSEA labs, etc.). These are invisible to your
search, but you need to disclaim that gap in your final report.

### 5. Plan the three-round search pattern

Don't just queue up Round 1. Pre-decide which vendor names you'll
query in Round 2 and which agency+dollar floors you'll use in Round 3.
This prevents the "I forgot to check X" loop.

### 6. Pre-build your dedup and aggregation logic

Before the data starts flowing, write the code that will:
- Dedupe by PIID + mod_number → keep latest mod
- Normalize vendor names for cross-program rollup
- Aggregate subs by recipient for ranking
- Flag outliers (>$5B sub records, negative obligations, blank vendors)

### 7. Decide your scope window upfront

For this project: **2020-01-01 to 2026-04-10** (per user direction).
Stick to that throughout; don't drift.

### 8. Decide your dollar floor for "interesting"

For this project: any prime > $50M, any sub > $10M, anything else gets
binned as "long tail." Adjust based on the total program size.

### 9. Plan the output format before pulling

Look at your final markdown layout (program → primes → subs) before
you pull data. This determines how much detail you actually need per
program. For this project, the user explicitly said "less detailed
than the original" -- so I knew I could skip the engineering/logistics
narrative and stick to award tables.

### 10. Budget for re-pulls

Plan on running each pull twice: once exploratory, once final after
you've discovered which queries miss things. The full FPDS + USAspending
pipeline for this project ran maybe 5x because each round surfaced new
vendor names and PIIDs to check.

---

## 13. Quick-Reference Code Snippets

### FPDS Atom feed pull with pagination

```python
import re, time
from urllib.request import urlopen, Request
from urllib import parse
from xml.etree.ElementTree import fromstring

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "research-tool/1.0"}

def fpds_search(query, max_pages=30):
    records = []
    start = 0
    total_pages = None
    while True:
        url = f"{BASE}&{parse.urlencode({'q': query})}&start={start}"
        req = Request(url, headers=HDRS)
        with urlopen(req, timeout=60) as r:
            text = r.read().decode("utf-8")
        root = fromstring(text)
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        if total_pages is None:
            m = re.search(r'rel="last".*?start=(\d+)', text)
            total_pages = (int(m.group(1)) // 10) + 1 if m else 1
            print(f"  ~{total_pages * 10} records, {total_pages} pages")
        records.extend(entries)
        start += 10
        if start // 10 >= min(total_pages, max_pages):
            break
        time.sleep(0.25)
    return records
```

### Dedupe by PIID, keep latest mod

```python
def dedupe_to_latest_mod(records):
    by_piid = {}
    for r in records:
        if not r.get("piid"):
            continue
        prev = by_piid.get(r["piid"])
        if prev is None or (r.get("signed") or "") > (prev.get("signed") or ""):
            by_piid[r["piid"]] = r
    return list(by_piid.values())
```

### USAspending PIID → generated_internal_id

```python
import json, urllib.request

def find_generated_internal_id(piid):
    """Look up USAspending's generated_internal_id for a given FPDS PIID.
    Returns list of result dicts (may be empty)."""
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    
    # Try contracts group first
    for group in (["A", "B", "C", "D"],
                  ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C",
                   "IDV_C", "IDV_D", "IDV_E"]):
        payload = {
            "filters": {
                "award_type_codes": group,
                "award_ids": [piid],
                "time_period": [{"start_date": "2007-10-01",
                                  "end_date": "2026-09-30"}],
            },
            "fields": ["Award ID", "generated_internal_id",
                       "Recipient Name", "Award Amount"],
            "limit": 50,
            "page": 1,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json",
                     "User-Agent": "research-tool/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            j = json.loads(r.read().decode("utf-8"))
        if j.get("results"):
            return j["results"]
    return []
```

### Pull all subawards for a generated_internal_id

```python
def get_subawards(generated_internal_id, max_records=2000):
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
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json",
                     "User-Agent": "research-tool/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            j = json.loads(r.read().decode("utf-8"))
        results = j.get("results", [])
        if not results:
            break
        subs.extend(results)
        if not j.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
        time.sleep(0.2)
    return subs
```

### Aggregate subs by recipient with vendor-name normalization

```python
import re
from collections import defaultdict

SUFFIXES = re.compile(r"\b(INC\.?|L\.?L\.?C\.?|CORP\.?|CORPORATION|"
                      r"CO\.?|LTD\.?|LP|L\.P\.|COMPANY|HOLDINGS)\b\.?,?\s*$",
                      re.IGNORECASE)

def normalize_vendor(name):
    if not name:
        return None
    s = name.upper().strip()
    s = re.sub(r"[,.]\s*$", "", s)
    while True:
        new = SUFFIXES.sub("", s).strip().rstrip(",.")
        if new == s:
            break
        s = new
    return s.strip()


def aggregate_subs(subs):
    by_rec = defaultdict(lambda: {"amount": 0.0, "count": 0})
    for s in subs:
        rec = normalize_vendor(
            s.get("recipient_name") or s.get("Sub-Recipient Name")
        )
        if not rec:
            continue
        amt = s.get("amount") or s.get("Sub-Award Amount") or 0
        try:
            amt = float(amt)
        except (TypeError, ValueError):
            continue
        # Sanity check: skip outliers
        if abs(amt) > 5e9:
            print(f"  WARN: skipping outlier sub: {rec} ${amt}")
            continue
        by_rec[rec]["amount"] += amt
        by_rec[rec]["count"] += 1
    return sorted(by_rec.items(), key=lambda x: x[1]["amount"], reverse=True)
```

### Common agency codes (memorize these)

```
9700  Department of Defense (all branches)
1700  Department of the Navy
2100  Department of the Army
5700  Department of the Air Force
97AD  Office of the Secretary of Defense
97F5  Washington Headquarters Services
7000  Department of Homeland Security
7008  United States Coast Guard (sub-agency of 7000)
6900  Department of Transportation
8000  NASA
1300  Department of Commerce
4900  National Science Foundation
3600  Department of Veterans Affairs
8900  Department of Energy (NNSA contracts use 89xxx)
```

Note: USCG is `7008`, not `7000`. If you query `7000` you get all of
DHS including CBP, TSA, ICE, FEMA -- way too broad. Use `7008` for
cutter work.

---

## 14. The Cumulative-vs-Window Trap (Worked Example)

This is the single most insidious gotcha in FPDS analysis, and I fell
into it on the first draft of `SAM_Submarine_Cutter_Contract_Awards.md`.
A reviewer asked "are these contracts actually for the FY26 SAM line
items?" and the answer turned out to be: kind of, but the dollar
attribution was wrong.

### The trap

When you pull a contract from FPDS with a date filter like
`SIGNED_DATE:[2020/01/01,2026/12/31]`, you get all the **mods** signed
in that window. Each mod has two relevant dollar fields:

- `obligatedAmount` -- the dollars **added by this specific mod**
- `totalObligatedAmount` -- the **cumulative total of all mods up
  through this one** (since the contract was originally awarded)

If you naively dedupe by PIID and keep "the latest mod's
totalObligatedAmount" as the contract's value, you get the **cumulative
since contract inception**, which is wildly different from "money
obligated in your window" if the contract started before 2020.

### The worked example

I pulled the Virginia Block IV multi-year contract `N0002412C2115`
(the SSN 792-801 master contract awarded in FY14). My first-draft
table showed:

> N0002412C2115 -- General Dynamics Electric Boat -- $19.90B obligated
> -- 2025-12-23 latest mod -- "Virginia Class Block III Construction"

That table line is wrong in **three** ways:

1. **Block label is wrong.** The base contract description is "VIRGINIA
   CLASS SUBMARINE BLOCK IV CONSTRUCTION" and a later mod says
   "SSN 792 CONSTRUCTION (BOAT 1, FY14)". SSN 792 (USS Vermont) is the
   **first Block IV boat**, not Block III. I had the block off by one.

2. **Dollar value is misleading.** The $19.90B is the cumulative
   `totalObligatedAmount` at the latest mod we see. Looking at per-mod
   data:

   ```
   2021-12-16 mod=P00049 this=$ 21.9M  cumulative_total=$19,897.9M
   2022-04-11 mod=A00740 this=$  0.2M  cumulative_total=$19,897.9M
   2025-11-21 mod=A01279 this=$  0.0M  cumulative_total=$19,897.9M
   2025-12-23 mod=A01291 this=$  0.0M  cumulative_total=$19,898.2M
   ```

   The earliest mod we see in our 2020-26 window already had the
   contract at $19.9B. Subsequent mods added a grand total of **$22.1M
   of new money** in the entire window. The contract was essentially
   fully obligated by 2018-2019 and was just receiving paperwork mods
   inside our window.

   So reporting "$19.90B obligated FY20-26" is wrong. The true window
   delta is ~$22M.

3. **Latest mod date is misleading.** "2025-12-23 latest mod" suggests
   recent activity, but the mod itself moved $0 of new money. The
   description "INCORPORATION OF PREVIOUSLY AUTHORIZED CHANGES" is the
   tell.

### The three patterns to recognize

After running per-mod analysis on ~20 PIIDs, I found contracts fall
into three buckets:

**Pattern A: Pre-window contract, mostly inactive**
```
Contract awarded 2014, was at $19.9B by Jan 2020.
Latest mod 2025-12-23 still shows $19.9B.
Window delta: ~$22M.
Cumulative report would say: $19.9B (WRONG by 900x)
```
Examples: N0002412C2115 (Block IV), N0002417C2100 (Block V/VI master),
N0002409C2104 (Block II).

**Pattern B: Window-native contract**
```
Contract awarded 2023-12-22 with base mod = $772M.
Subsequent mods grow it to $2.54B by 2025-12-17.
Window delta: $2.54B (full cumulative is in window).
Cumulative report = correct.
```
Examples: N0002424C2114 (Bechtel S9G FY24 component), N0003023C0100
(Trident FY24), N0002424C2110 (Block VI LLTM).

**Pattern C: Window-straddling contract**
```
Contract awarded 2017, at $13.6B in early 2020.
Latest mod 2025-12-17 at $30.8B.
Window delta: $17.2B (real new money committed in window).
Cumulative report would say: $30.8B (overstates window by 1.8x)
```
Examples: N0002417C2117 (Columbia Build I+II), N0002419C2115 (Bechtel
Columbia industrial base), N0002419C2210 (Polar Security Cutter),
HSCG2316CAFR625 (FRC Bollinger).

### The correct calculation

To get the true window delta:

```python
def window_delta(mods, start="2020-01-01", end="2026-12-31"):
    """Compute true window obligation delta for one PIID's mods."""
    mods = sorted(mods, key=lambda r: r.get("signed") or "")
    pre_window_total = 0
    in_window_latest = 0
    found_pre = False
    found_in = False
    for r in mods:
        s = (r.get("signed") or "")[:10]
        t = r.get("total_obligated") or 0
        if s < start:
            pre_window_total = t  # baseline at start of window
            found_pre = True
        elif start <= s <= end:
            in_window_latest = t  # cumulative as of latest mod in window
            found_in = True
    if not found_in:
        return 0
    if not found_pre:
        return in_window_latest  # all activity is in window
    return in_window_latest - pre_window_total
```

**The catch:** This requires you to have pulled mods from BEFORE your
window of interest, so you can compute the baseline. If your FPDS query
filtered to `SIGNED_DATE:[2020/01/01,...]` you don't have any pre-2020
mods to subtract from. **Solution: pull mods from 2-3 years before your
analysis window** and use that for the baseline calculation, then
filter to your reporting window only when displaying.

Alternatively, you can sum the per-mod `obligatedAmount` (this action
only) field across mods in window. This is more accurate but the field
is sometimes blank or unreliable for SLIN-level mods.

### When to use cumulative vs delta

| Use case | Use this number |
|---|---|
| "How much is GD Electric Boat's Virginia Block IV contract worth?" | Cumulative (it's a contract size) |
| "How much money was obligated to Virginia Block IV in FY20-26?" | Delta (it's a window spend) |
| "Is this contract still receiving funding?" | Look at per-mod amounts in window |
| "Match the FY26 SAM line item to a vehicle" | Use ceiling for vehicle ID, then verify recent mod descriptions for FY26-tagged money |
| "Rank contractors by FY20-26 spend" | Delta (otherwise old contracts dominate) |

### What to do in your output

**Never silently report the cumulative number as if it were a window
delta.** Either:

1. Compute the actual window delta and use that, OR
2. Label the column unambiguously: "Cumulative obligation at latest
   in-window mod", and add a caveat box explaining what that means, OR
3. Show both columns side by side

In the corrected `SAM_Submarine_Cutter_Contract_Awards.md`, I went with
option 2 -- relabeled "Obligated" → "Cumulative Obligated (latest mod)"
and added a prominent caveat at the top of the file plus a dedicated
Section 21 walking through the SAM-line-to-contract mapping.

---

## 15. Reading Mod Descriptions to Identify Programs

The single most useful analytical move in FPDS is **reading the mod
descriptions for hull number references**. Mod descriptions are messy,
typo-filled, and often wrong about the latest scope, but they reliably
contain hull names/numbers when work is being added to a specific boat.

### The technique

For any submarine PIID, look at the descriptions across all the mods
in the window. You'll find references like:

```
"DIVERT BLOCK V FOUNDATIONS"
"SSN 792 CONSTRUCTION (BOAT 1, FY14)"
"SSN 812 CONSTRUCTION (BOAT 2, FY 24)"
"MOUNTING BOX PROCEDURE CHANGE SSBN 826/827"
"SSN 814 LONG LEAD TIME MATERIAL"
"USS HARTFORD (SSN 768) EOH EXECUTION"
```

These tell you exactly which block, build, hull, or program activity
the contract is funding. Build a hull number → block crosswalk
beforehand:

**Virginia hull → block:**
- SSN 774-779 → Block I
- SSN 780-785 → Block II
- SSN 786-791 → Block III
- SSN 792-801 → Block IV
- SSN 802-811 → Block V
- SSN 812-820 → Block VI

**Columbia hull → build:**
- SSBN 826 → Build I (USS District of Columbia)
- SSBN 827 → Build II (USS Wisconsin)

**USCG cutter hull → class:**
- WMSL 750-760 → Legend-class National Security Cutter (HII)
- WMSM 915-940 → Heritage-class Offshore Patrol Cutter
- WPC 1101-1164 → Sentinel-class Fast Response Cutter (Bollinger)

When you see a mod description like "SSN 814 LONG LEAD TIME MATERIAL"
on PIID `N0002424C2110`, you can immediately classify it as **Block VI
LLTM for the 4th Block VI hull** without any external research.

### Surface ship indicators

Same principle applies to surface ships. Look for:

```
"DDG 51 FY18-22 BLOCK"      → DDG-51 Flight III multi-year
"USS GERALD R. FORD (CVN 78)"  → CVN 78 specific work
"LPD 33, 34, 35"              → LPD Flight II block buy
"LHA 9 STRUCTURAL ASSEMBLY"   → LHA 9 specific
"FRC 1158"                    → Fast Response Cutter hull 1158
```

### When mod descriptions are unreliable

Sometimes the latest mod description is for a tiny administrative
change that doesn't reflect the contract's main scope. Examples:

```
N0002417C2100 latest mod (2025-12-23): "INCORPORATION OF PREVIOUSLY
  AUTHORIZED CHANGES UNDER COUPON PROCESS"
  → tells you nothing about the contract scope
```

```
N0002412C2115 latest mod (2025-12-23): "ADJUDICATED THE CONTRACT CHANGE
  TO REPLACE PHOTONICS MAST #1"
  → makes it sound like a photonics mast contract; actually it's the
    Block IV submarine construction MYP
```

**Mitigation:** Don't rely on a single mod description. Look at the
oldest mod we have and the largest dollar mods. The largest mods are
where the real scope lives.

```python
mods.sort(key=lambda r: abs(r.get("obligated") or 0), reverse=True)
top_mods_by_dollar = mods[:10]
for r in top_mods_by_dollar:
    print(r.get("desc", "")[:120])
```

### The crosswalk-table workflow

For any submarine/ship analysis, build a small table like this BEFORE
you start writing your output:

```
PIID                Earliest mod desc                  Hull refs found                  My block label
==================  =================================  ===============================  ================
N0002412C2115       VIRGINIA BLOCK IV CONSTRUCTION     SSN 792 (boat 1)                Block IV
N0002417C2100       DIVERT BLOCK V FOUNDATIONS         SSN 812 (boat 2 of Block VI)    Block V→VI master
N0002424C2110       SSN 814 LONG LEAD TIME MATERIAL    SSN 814 (boat 4 of Block VI)    Block VI LLTM
N0002417C2117       COLUMBIA DESIGN DRAWING REVISIONS  SSBN 826/827                    Build I + II
```

This crosswalk takes 15 minutes to build by reading mod descriptions
and saves you from labeling errors in your final output.

---

## Summary: The Most Important Things

If you only remember 7 things from this file:

1. **Use `VENDOR_NAME:"..."` for vendor searches**, not `UEI_NAME` or
   `VENDOR_FULL_NAME`. The other field names either don't work or
   return wildly different result counts.

2. **Run three rounds of searches**: description keywords, then vendor
   names of the primes you found, then an agency + dollar-floor
   backstop. Each round catches things the previous round missed.

3. **The USAspending subaward pipeline is the killer feature**, but
   you must use the two-call pattern (`/search/spending_by_award/` to
   get `generated_internal_id`, then `/subawards/`). And retry the
   IDV award type group if the contracts group returns nothing.

4. **0 reported subawards ≠ no subcontracting.** Bollinger, Birdon,
   Austal, BIW, and most foreign primes don't comply with FFATA. Fill
   the gap with FPDS-visible direct contracts to known component
   vendors and mark the limitation explicitly.

5. **Federal shipyard work is invisible.** When the budget sheet shows
   $5B for SSN depot maintenance and FPDS only finds $50M, that's not
   a search failure -- it's federal employee payroll at the four
   public shipyards (Norfolk, Portsmouth, Pearl Harbor, Puget Sound).

6. **`totalObligatedAmount` is cumulative-since-contract-award, NOT
   window spend.** A contract showing "$19.9B obligated, latest mod
   2025-12-23" might have only added $22M of new money inside your
   FY20-26 window. Compute window deltas with `(latest_in_window_total
   - latest_pre_window_total)`, OR sum per-mod `obligatedAmount`
   values, OR explicitly label your column as "cumulative" with a
   caveat. **Never silently report cumulative as if it were window
   spend.** (See Section 14 for the worked example.)

7. **Read mod descriptions for hull number references** to identify
   which block/build/program a contract is funding. Hull numbers like
   "SSN 812", "SSBN 826", "LHA 9", "FRC 1158" are unambiguous tags
   that immediately classify the work. The PIID year prefix is NOT
   reliable -- a `N00024-17-C-2100` PIID can fund Block VI work in
   FY26 if mods extend it. (See Section 15 for the workflow.)

---

*Generated 2026-04-10 from direct experience pulling FPDS Atom Feed and
USAspending subaward data for the SAM submarine and cutter program
analysis. Companion to `federal_procurement_data_guide.txt`,
`SAM_Program_Contract_Awards.md`, `SAM_Program_Component_Contracts.md`,
and `SAM_Submarine_Cutter_Contract_Awards.md`.*

*Updated 2026-04-10 (rev 2): Added Section 14 (cumulative-vs-window
trap) and Section 15 (reading mod descriptions for hull numbers) after
hitting both traps in the submarine/cutter pull. Expanded summary from
5 to 7 most-important items.*
