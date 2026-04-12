# Subaward Pull Lessons Learned -- v2 (April 2026)

Field notes from the FY2026 key programs pull session that produced
`FY2026_Key_Programs_Contract_Awards.md`. **Focus: USAspending subaward
data quality and the per-`sub_id` dedup methodology.**

This is a **companion** to `Federal_Procurement_Research_Lessons_Learned.md`
(the v1 lessons file) and documents lessons learned **after** that file
was written. The v1 file's §5 covered the basic two-call subaward
workflow and the >$5B sanity floor. This file documents what we learned
when we actually tried to apply that workflow at scale across 170 PIIDs
and discovered the cumulative-snapshot duplication problem that had been
silently corrupting every subaward number in the prior analysis.

If you only read one section: **§1 (the cumulative-snapshot problem)**
and **§2 (the 3-stage v3 dedup methodology)**. Everything else is
elaboration.

---

## Table of Contents

1. [The USAspending Subaward Cumulative-Snapshot Problem](#1-the-usaspending-subaward-cumulative-snapshot-problem)
2. [The 3-Stage v3 Dedup Methodology](#2-the-3-stage-v3-dedup-methodology)
3. [The "Phantom $920M" Depot Pattern](#3-the-phantom-920m-depot-pattern)
4. [Per-Pair Sanity Cap: A Sub Cannot Exceed Its Prime](#4-per-pair-sanity-cap-a-sub-cannot-exceed-its-prime)
5. [Apparent Prime/Sub Mismatches on Long-Running Contracts](#5-apparent-primesub-mismatches-on-long-running-contracts)
6. [Cross-PIID Aggregation Requires Vendor Normalization](#6-cross-piid-aggregation-requires-vendor-normalization)
7. [The Iterative Dedup Discovery Process](#7-the-iterative-dedup-discovery-process)
8. [USAspending Subaward Schema Is Minimal](#8-usaspending-subaward-schema-is-minimal)
9. [PIID Search in FPDS Atom Feed: Works (Correction to v1 §2)](#9-piid-search-in-fpds-atom-feed-works-correction-to-v1-2)
10. [Per-Mod Sum Method: SLIN Splits and Option-Exercise Caveats](#10-per-mod-sum-method-slin-splits-and-option-exercise-caveats)
11. [The Vendor-Sweep Round 3 Catches a Lot](#11-the-vendor-sweep-round-3-catches-a-lot)
12. [Background Scripts + Incremental Save](#12-background-scripts--incremental-save)
13. [Recommended Pull Pipeline for Subaward-Focused Analyses](#13-recommended-pull-pipeline-for-subaward-focused-analyses)
14. [Quick-Reference Code Snippets](#14-quick-reference-code-snippets)
15. [Summary -- The Most Important Things](#15-summary--the-most-important-things)

---

## 1. The USAspending Subaward Cumulative-Snapshot Problem

**This is the single most important finding from the entire session.**
Every other subaward lesson in this file is downstream of this one.

### The bug

USAspending's `/api/v2/subawards/` endpoint returns multiple records
for the **same** `subaward_number` at different `action_date`s, with
each record reporting a **cumulative-style amount** rather than the
incremental value of that action. If you naively sum the records, you
multiply the real subaward value by the number of times the prime
contract has been modified to touch that sub.

### The smoking gun

We pulled subawards for `N0002411C2300` (the LM LCS Freedom variant
construction prime) and got 1,208 records. The prior file's analysis
summed amounts and got Marinette Marine at **$47.17 billion** of
subawards on a $5B prime contract. That's impossible.

We dumped all the Marinette records and saw this:

```
sub_id=4100090097  2020-01-28  $497.1M
sub_id=4100090097  2020-02-13  $497.1M
sub_id=4100090097  2020-03-27  $497.1M
sub_id=4100090097  2020-04-27  $499.4M
sub_id=4100090097  2020-05-14  $499.4M
sub_id=4100090097  2020-06-05  $499.4M
sub_id=4100090097  2020-07-17  $498.0M
sub_id=4100090097  2020-10-07  $498.0M
sub_id=4100090097  2020-12-16  $498.0M
sub_id=4100090097  2021-02-10  $498.0M
sub_id=4100090097  2021-04-21  $498.0M
sub_id=4100090097  2021-06-03  $498.0M
```

That's the **same `sub_id` 12 times**, each with the same subaward
description, each at slightly-growing $497-499M values. This is one
single Marinette subcontract worth ~$500M being snapshotted at each
action_date as the prime contract is modified to fund it.

If you sum: 12 × $498M = ~$6B for one $500M sub. Multiply that by 23
distinct Marinette `sub_id`s (each with similar duplication) and you
get the $47.17B fiction.

### Why this is so insidious

The USAspending API doesn't tell you the records are duplicates.
There's no "snapshot date" field, no "is this cumulative" flag, no
indicator that record 5 is "an update to record 1". They just look
like 12 separate subaward actions. The `id` field is unique per
record (USAspending's internal counter), the `action_date`s are
distinct, and the amounts vary slightly. A naive aggregation by
recipient name appears to be doing the right thing.

### The fix at a glance

```python
# WRONG: naive aggregation
total = sum(rec["amount"] for rec in subaward_records)

# RIGHT: dedup per sub_id, take MAX amount
by_sid = defaultdict(list)
for r in subaward_records:
    by_sid[r["sub_id"]].append(r)
deduped = [max(recs, key=lambda x: x["amount"]) for recs in by_sid.values()]
total = sum(r["amount"] for r in deduped)
```

But that's only Stage 1 of the fix — see §2.

### Scale of the problem in the prior file

When we re-pulled all 170 in-scope PIIDs and applied corrected dedup,
the totals dropped by 3-50x across the board:

| Vendor | Prior file claim | v3 corrected | Inflation factor |
|---|---|---|---|
| Marinette Marine (LM LCS) | $47.17B | $2.49B | **19x** |
| LM SEWIP Block 2 sub total | $2.85B | ~$0.005B | **570x** (mostly pre-window) |
| NG Knifefish/LCS sub total | $1.48B | $0.13B | **11x** |
| HELIOS MZA Associates | $395M | $25M | **16x** |
| HELIOS L3 Technologies | $209M | $22M | **9x** |
| Hampton Roads PCE | $942M | $30M | **31x** |
| TECNICO Corporation | $230M | $55M | **4x** |
| CAES + Mercury combined RF | $5B+ claim | $503M | **10x** |

**Every single subaward number in the prior file was inflated by some
factor between 3x and 570x.** The $5B sanity-floor rule from v1 §7
flagged the most egregious cases (Marinette, the CAES claims) but
missed the systemic ~5-10x inflation across the entire dataset.

### Lesson

**Never trust a USAspending subaward total without applying per-`sub_id`
dedup.** Treat every aggregate from that endpoint as suspect until
you've verified the dedup. The corruption is invisible to spot-checks
because individual records look reasonable.

---

## 2. The 3-Stage v3 Dedup Methodology

The Stage 1 (per `sub_id` MAX) fix from §1 is necessary but not
sufficient. There are two more failure modes that need their own
stages:

### Stage 1: Per `sub_id`, take MAX amount

Handles: same subcontract reported at multiple action_date snapshots
with growing amounts (the Marinette case from §1).

```python
def stage1_per_sub_id_max(records):
    """For each unique sub_id, keep only the record with the max amount."""
    by_sid = defaultdict(list)
    for r in records:
        sid = r.get("sub_id") or ""
        by_sid[sid].append(r)
    return [max(recs, key=lambda x: x["amount"] or 0) for recs in by_sid.values()]
```

This alone takes Marinette from $47.17B → $2.49B. But it's not enough
for cases where USAspending issues **separate `sub_id`s** for the
same underlying subcontract.

### Stage 2: Per (recipient, amount), collapse identical amounts

Handles: multi-`sub_id` artifacts where USAspending creates new
`subaward_number`s for the same purchase order under different prime
mods, each at the exact same cumulative amount.

The trigger case was HL Welding on `N0002418C4439` (NASSCO USS Cowpens
MODPRD), where THREE distinct sub_ids each reported exactly $919.5M:

```
sub_id=MUH5233978  2021-01-19  $919.50M
sub_id=MUH5233759  2021-01-12  $919.50M
sub_id=MUH5234309  2021-01-26  $919.50M
```

Stage 1 dedup keeps each as a separate record (different sub_ids).
Summing gives $2.76B for HL Welding on a single $200M depot prime.
Stage 2 collapses identical amounts:

```python
def stage2_dedupe_identical_amounts(stage1_records):
    """Per (recipient, amount), keep only one record."""
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
```

The (recipient, amount) tuple as key means: "if the same recipient
shows the exact same amount under multiple sub_ids, those are
duplicates of the same underlying subcontract."

**Risk:** This may incorrectly collapse two genuinely-distinct
subcontracts that happen to have identical amounts. In practice this
is rare for non-trivial values; the rounding to 2 decimal places
makes false collisions unlikely.

### Stage 3: Cap at 1.0× prime size, exclude > 2× prime

Handles: USAspending data corruption that survives the first two
stages — typically phantom amounts being attributed to multiple
unrelated recipients (see §3).

```python
def stage3_cap_and_exclude(per_recipient, prime_size, slack=1.0, exclude=2.0):
    """Per recipient, cap their total at slack × prime_size.
    Exclude entirely if raw > exclude × prime_size."""
    if prime_size <= 0:
        return per_recipient.copy(), [], []
    cap = prime_size * slack
    exclusion = prime_size * exclude
    capped = {}
    flagged = []
    excluded = []
    for rec, amt in per_recipient.items():
        if amt > exclusion:
            excluded.append(rec)
            continue  # drop entirely
        if amt > cap:
            capped[rec] = cap
            flagged.append(rec)
        else:
            capped[rec] = amt
    return capped, flagged, excluded
```

The fundamental rule: **a sub cannot deliver more than the prime
contract's total value**. If a single (recipient, prime) pair claims
to be larger than the prime, the data is wrong. Cap at the prime
size; if it's wildly bigger (>2× prime), drop entirely.

### Why all three stages are needed

| Stage | Catches | Misses without it |
|---|---|---|
| Stage 1 (per `sub_id` MAX) | Same sub_id at multiple snapshots | Marinette at $47.17B |
| Stage 2 (collapse identical amounts) | Same sub under multiple sub_ids | HL Welding at $2.76B |
| Stage 3 (cap at prime) | Phantom amounts attributed to wrong recipients | NASSCO Cowpens five-recipient $920M phantom |

Apply them in order. Each stage catches a different failure mode.

### Reference output

After v3 dedup applied to all 170 in-scope PIIDs in the FY2026 key
programs analysis, the grand total of in-window subawards dropped from
~$80B+ implied by the prior file's individual numbers to **~$10.35B**.
That's an 8x correction across the entire dataset.

---

## 3. The "Phantom $920M" Depot Pattern

This is the most egregious data corruption case we found. It deserves
its own section because it's a pattern that future pulls should look
for and exclude.

### The pattern

On `N0002418C4439` (NASSCO USS Cowpens FY18 MODPRD, total prime
~$197M), FIVE entirely-unrelated recipients each reported the **exact
same $920M** in subaward amounts:

```
HL WELDING, INC.                $921.6M raw
HAWTHORNE MACHINERY CO.         $921.3M raw
DIAMOND ENVIRONMENTAL SERVICES  $920.8M raw
BREWER CRANE LLC                $920.4M raw
AMERICAN SCAFFOLD LLC            $920.0M raw  (also on N0002418C2404)
```

These are a Norfolk welding shop, a heavy equipment dealer, a
porta-potty company, a crane rental, and a scaffolding rental
respectively. None of them could plausibly do $920M of work on a
$197M cruiser modernization. The fact that 5 different vendors all
reported the same impossible number on the same prime is conclusive
evidence of USAspending data corruption.

### What's happening

We don't know the root cause — possibly the prime's total contract
value is being mis-attributed to subawards as a default field, or
the cumulative-snapshot bug (§1) plus Stage 2 deduplication is
producing the same artifact for multiple recipients. Either way,
the data is wrong.

### How to detect it

Two heuristics:

1. **Multiple recipients with identical values on the same prime.**
   If 3+ unrelated recipients all show the same amount (especially
   one larger than the prime), exclude all of them.

2. **Recipient amount >> prime size.** If a single (recipient,
   prime) pair has raw amount > 2× the prime's total obligation,
   it's clear corruption. Drop it.

The Stage 3 cap-and-exclude rule (§2) catches case 2. For case 1,
you may want to add a separate check.

### Affected PIIDs in this dataset

The phantom-pattern PIIDs in the FY2026 key programs pull:
- **N0002418C4439** (NASSCO USS Cowpens MODPRD) — 5 recipients
- **N0002418C2404** (NASSCO LHA 7 fitting out) — 2 recipients (HL Welding, American Scaffold) at $919.5M each on a $23M prime

There may be more. The cleanest defense is the Stage 3 hard cap
applied automatically across all PIIDs.

### Lesson

**When a depot sweep returns 5 unrelated vendors all at suspiciously-
identical large amounts on the same prime, it's data corruption.**
Build detection into the pipeline; don't trust a manual review to
catch it after the fact.

---

## 4. Per-Pair Sanity Cap: A Sub Cannot Exceed Its Prime

This rule sounds obvious but the prior file's numbers violated it
hundreds of times. Encoding it as a hard cap removes the bulk of the
remaining data quality issues after Stages 1 and 2.

### The rule

**For any (recipient, prime_piid) pair, the recipient's total cannot
exceed the prime contract's total obligated value.** A subcontract is
a portion of the prime; mathematically it cannot be larger.

### Implementation choice: 1.0× cap, exclude > 2× prime

We chose:
- **Cap at 1.0× prime** for amounts in the 1.0-2.0× range (clearly
  inflated but possibly recoverable as ~prime-size deliveries)
- **Exclude entirely** for amounts > 2× prime (clear corruption)

### Why not strict equality?

A few legitimate cases can produce sub > prime:
1. **Inter-fiscal-year scope shifts**: prime obligation gets
   re-allocated between years, but sub records persist
2. **Cost reimbursable contracts**: total sub disbursement may
   exceed initial prime obligation as the prime is modified
3. **Sub's own subcontracts being aggregated upward** by USAspending
4. **Currency or rounding artifacts** for small contracts

The 1.0× cap with 2.0× exclusion threshold is a middle-ground that
preserves legitimate cases at the boundary while excluding obvious
phantoms.

### Two pairs hit the cap in this dataset

After v3 dedup, two pairs flagged at exactly 1.0× cap:

| Prime | Recipient | Raw | Capped | Prime size |
|---|---|---|---|---|
| N0002419C4447 (Vigor Marine CG-71 PSE) | Timken Gears & Services | $830.7M | $447.3M | $447.3M |
| N6133111C0017 (GDMS SMCM Unmanned) | Trident Sensors Limited | $233.3M | $143.3M | $143.3M |

Both are real subs (Timken supplies CG propulsion gears, Trident
supplies SMCM sensors) but the raw amount is implausibly high. The
cap brings them to plausible values and flags for manual review.

### Lesson

**Build the cap-at-prime rule into the aggregator from day one.**
It catches a wide class of data quality issues with a single check.
Flag the cases that hit the cap so they get reviewed rather than
silently included.

---

## 5. Apparent Prime/Sub Mismatches on Long-Running Contracts

After applying the v3 dedup, you'll see cases where a prime contract
has small in-window obligation but a sub on that prime has large
in-window delivery. **These are legitimate, not bugs.**

### Two clear examples in this dataset

**LCS Freedom (N0002411C2300):**
- Prime window obligation (per-mod sum): **$250M**
- Marinette Marine sub window delivery: **$2.49B**

**GDMS Surface MCM Unmanned (N6133111C0017):**
- Prime window obligation: **$15M**
- Teledyne + Trident sub window delivery: **~$1.18B**

### What's happening

Both contracts were awarded **before 2020** with multi-billion-dollar
pre-window cumulative obligations:
- N0002411C2300 (FY10 award): $4.74B pre-window cumulative
- N6133111C0017 (FY11 award): $130M pre-window cumulative

The subs (Marinette, Teledyne, Trident) are delivering work in
2020-2026 that was funded by **pre-window prime obligations**. The
prime contract isn't getting much new money because it's been fully
funded for years; the sub is just spending down the existing scope.

### The conceptual model

For long-running contracts, prime obligation and sub delivery are
**out of phase**:
- Prime obligation happens up-front (or in big chunks at
  multi-year-procurement boundaries)
- Sub delivery is spread over the execution years

A prime that was fully funded in FY15 will have $0 of "new prime
obligation" in FY20-26, but its sub delivery will continue throughout.

### Why this matters

If you cap subs at the prime's **window** obligation, you lose all
the legitimate delivery on long-running contracts. We chose to cap
at the **larger of (window delta, latest cumulative)** which gives
proper credit for pre-window-funded scope:

```python
prime_cap_basis = max(window_delta_obligated, latest_in_window_total_obligated)
```

For LCS Freedom, that's $4.98B (cumulative), so Marinette's $2.49B
fits comfortably under the cap. For SMCM Unmanned, it's $143M
(cumulative), which is why Teledyne + Trident hit the cap (as
documented in §4).

### Lesson

**Use cumulative (latest in-window mod) as the cap basis for
long-running pre-window contracts**, not just window delta.
Otherwise you'll discard legitimate sub delivery that's funded by
pre-window prime obligations.

---

## 6. Cross-PIID Aggregation Requires Vendor Normalization

The raw subaward records use the legal entity name as it appears in
USAspending. To produce a meaningful "top hidden subs" table you need
to roll up the legal entities to parent companies.

### The mess

A single parent company can appear under many names:

**General Dynamics** (10+ legal entities seen in this pull):
- GENERAL DYNAMICS MISSION SYSTEMS, INC.
- GENERAL DYNAMICS LAND SYSTEMS, INC.
- GENERAL DYNAMICS-OTS, INC.
- GENERAL DYNAMICS INFORMATION TECHNOLOGY (GDIT)
- GENERAL DYNAMICS ADVANCED INFORMATION SYSTEMS
- BATH IRON WORKS CORPORATION
- ELECTRIC BOAT CORPORATION
- NATIONAL STEEL AND SHIPBUILDING COMPANY (NASSCO)
- GD MISSION SYSTEMS (the abbreviated form)
- GD-OTS

**L3Harris** (8+ legal entities):
- L3 TECHNOLOGIES, INC.
- L3HARRIS TECHNOLOGIES
- L3 COMMUNICATIONS
- L3HARRIS MARITIME POWER & ENERGY SOLUTIONS
- L3HARRIS CINCINNATI ELECTRONICS
- L3HARRIS FUZING & ORDNANCE SYSTEMS
- L3HARRIS INTERSTATE ELECTRONICS
- L-3 COMMUNICATIONS

Plus the **Aerojet Rocketdyne** acquisition (2023) folds yet another
entity into L3Harris.

### The mapping table approach

We built a hand-curated dict mapping each known legal entity to its
parent:

```python
PARENT_MAP = {
    "GENERAL DYNAMICS MISSION SYSTEMS": "General Dynamics",
    "GENERAL DYNAMICS LAND SYSTEMS": "General Dynamics",
    "GD-OTS": "General Dynamics",
    "GDIT": "General Dynamics",
    "BATH IRON WORKS": "General Dynamics",
    "ELECTRIC BOAT": "General Dynamics",
    "NASSCO": "General Dynamics",
    "NATIONAL STEEL AND SHIPBUILDING": "General Dynamics",
    # ... ~150 entries
    "L3 TECHNOLOGIES": "L3Harris",
    "L3HARRIS": "L3Harris",
    "AEROJET ROCKETDYNE": "L3Harris (Aerojet Rocketdyne)",
    # ...
}

def parent_of(normalized_name):
    if normalized_name in PARENT_MAP:
        return PARENT_MAP[normalized_name]
    # Fallback: prefix match
    for key in PARENT_MAP:
        if normalized_name.startswith(key + " "):
            return PARENT_MAP[key]
    return normalized_name  # itself if no mapping
```

### Why hand-curated and not automated

We tried automated approaches (string similarity, fuzzy matching) and
they all produced wrong rollups. The right answer requires knowing
that:
- Earl Industries is now BAE Norfolk (acquisition 2014)
- Coltec is the parent of Fairbanks Morse
- York International is a Johnson Controls division
- Aerojet Rocketdyne is now under L3Harris (acquisition 2023)
- Marinette Marine is owned by Fincantieri

These corporate relationships aren't visible in the vendor name
strings. They require domain knowledge.

### Maintenance burden

The mapping table needs to be updated whenever:
- A new acquisition closes
- A new subsidiary appears in the data
- A vendor renames (e.g., Raytheon Company → RTX Corporation in 2020)

For this analysis, ~150 mappings cover the top ~50 parent companies
representing >95% of the in-window sub volume. The long tail of small
vendors falls back to "itself as parent" without rollup.

### Lesson

**Build the parent-company mapping table once and version it.** Treat
it as a first-class data file. The unmapped fallback gives reasonable
default behavior so partial coverage is OK.

See `data_pull/aggregate_subs.py::PARENT_MAP` for the working table.

---

## 7. The Iterative Dedup Discovery Process

We needed FOUR iterations to land on the right dedup approach. Future
analyses should not expect to get it right on the first try.

### v0: Naive sum (the prior file)

```python
total = sum(r["amount"] for r in records)
```

Result: Marinette $47.17B. Spectacular failure.

### v1: Dedup by `(sub_id, action_date, recipient, amount)`

```python
seen = set()
for r in records:
    key = (r["sub_id"], r["action_date"], r["recipient_name"], r["amount"])
    if key in seen: continue
    seen.add(key)
    deduped.append(r)
```

Result: Marinette $37.77B. Still corrupted because each snapshot has
a unique date — the tuple is always distinct so nothing gets deduped.

### v2: Per `sub_id`, take MAX amount

```python
by_sid = defaultdict(list)
for r in records:
    by_sid[r["sub_id"]].append(r)
deduped = [max(recs, key=lambda x: x["amount"]) for recs in by_sid.values()]
```

Result: Marinette $2.49B. Looks plausible! But...

Then we discovered HL Welding at $2.76B on a $200M depot prime
(same `sub_id` with identical amounts under different ID variations
that v2 couldn't catch because the IDs were technically different
strings).

### v2.5: Per (recipient, prime), take MAX

```python
by_pair = defaultdict(list)
for r in records:
    by_pair[r["recipient_name"]].append(r)
collapsed = {rec: max(recs, key=lambda x: x["amount"])["amount"]
             for rec, recs in by_pair.items()}
```

Result: Marinette **$499M**. Now we've gone too far — collapsed all
23 distinct Marinette subcontracts into one max-amount record. This
is the opposite mistake.

### v3 (final): Stage 1 + Stage 2 + Stage 3

```python
def v3_dedup(records, prime_size):
    # Stage 1: per sub_id MAX
    by_sid = defaultdict(list)
    for r in records:
        by_sid[r["sub_id"]].append(r)
    stage1 = [max(recs, key=lambda x: x["amount"]) for recs in by_sid.values()]
    
    # Stage 2: per (recipient, amount), keep one
    seen = set()
    stage2 = []
    for r in stage1:
        key = (r["recipient_name"], round(r["amount"], 2))
        if key in seen: continue
        seen.add(key)
        stage2.append(r)
    
    # Aggregate by recipient
    by_rec = defaultdict(float)
    for r in stage2:
        by_rec[r["recipient_name"]] += r["amount"]
    
    # Stage 3: cap at 1.0x prime, exclude > 2x prime
    cap = prime_size * 1.0
    excl = prime_size * 2.0
    out = {}
    for rec, amt in by_rec.items():
        if amt > excl: continue
        out[rec] = min(amt, cap) if prime_size > 0 else amt
    return out
```

Result: Marinette $2.49B (validates), HL Welding excluded entirely
(>2× prime), other recipients reasonable.

### Lesson

**Test your dedup against multiple known cases before trusting it.**
Marinette alone wouldn't have caught the HL Welding case, and HL
Welding alone might have led to over-aggressive collapsing. You need
both extremes to find the right middle ground.

A good test set:
1. **The Marinette case**: high-value sub on a long-running prime
   (validates Stage 1)
2. **The HL Welding case**: identical-amount duplicates under
   different sub_ids (validates Stage 2)
3. **The NASSCO Cowpens phantom**: multiple unrelated recipients
   at impossible amounts (validates Stage 3 exclusion)
4. **A clean window-native case** (e.g., HII DDG-51 FY23-27 MYP):
   verify the deduped numbers don't lose legitimate detail

---

## 8. USAspending Subaward Schema Is Minimal

The `/api/v2/subawards/` endpoint returns only **6 fields** per record:

```json
{
  "id": 380064,
  "subaward_number": "4100090097",
  "description": "SERVICE ITEM TDP LCS TECHNICAL DATA PACKAGE...",
  "action_date": "2020-05-14",
  "amount": 499395618.0,
  "recipient_name": "MARINETTE MARINE CORPORATION"
}
```

Notable **missing** fields:
- No "is this cumulative or incremental" flag
- No prime PIID (you have to know it from your query)
- No sub-recipient location / city / state
- No award type (purchase order? task order? blanket agreement?)
- No NAICS / PSC code for the sub
- No contract reference for the sub itself
- No DUNS / UEI for the sub (just the name)

The `description` field is a **concatenated jumble** of all the line
item descriptions for that subaward across all action dates. Look at
the Marinette example:
> "SERVICE ITEM TDP LCS TECHNICAL DATA PACKAGE SHIP CONSTRUCTION
> SHIP CONSTRUCTION SERVICE ITEM - WATERFRONT CHIT PROCESS SERVICE
> ITEM - WATERFRONT CHIT PROCESS SERVICE ITEM - LCS5 CLIN 0001 MMC
> LCS 7 GEAR SUPPORT LCS 5- MMC FSST INCENTIVE SIF LCS 7- MMC SIF"

That's clearly multiple line items joined together. You can't parse
it cleanly.

### Implication for analysis

The minimal schema means:
1. You can only aggregate by recipient name (no UEI, no location)
2. You can't distinguish sub types
3. You can't build a clean per-mod history of a specific sub
4. You depend entirely on the prime PIID to know which program a sub
   is associated with

For richer sub data, the **subaward bulk download** at
`download.usaspending.gov` includes more fields than the API. We
didn't use it for this pull but it may be necessary for future
analyses that need sub-level NAICS or location data.

### Lesson

**Don't expect the API to give you the rich sub data you'd want.**
Plan your analysis around the 6 fields you actually get. If you
need more, use the bulk download or a paid commercial source.

---

## 9. PIID Search in FPDS Atom Feed: Works (Correction to v1 §2)

The v1 lessons file claimed:

> | `PIID:N0002419C2116` | **0 results** -- direct PIID lookup doesn't work |
> | `PIID:"N00024-19-C-2116"` (hyphenated) | **0 results** |

**This is wrong, or at least not universally true.** In this session
PIID search worked reliably for all 82+13 = 95 PIIDs we queried:

```
q=PIID:"N0002422C5500"  → returns all 30 mods of the SPY-6 production contract
q=PIID:"N0002418C2307"  → returns all 760 mods of HII DDG FY18-22 MYP
```

The format that works:
- **Quoted, no hyphens**: `PIID:"N0002422C5500"` ✓

Format that doesn't:
- Hyphenated: `PIID:"N00024-22-C-5500"` (the v1 form)

### Implication

You can build per-PIID per-mod pulls that don't require vendor name
or date-range searches. This is much more efficient than the v1
recommended approach of "vendor + date range, then filter in code"
when you already know the PIID you want.

### The per-mod pull pattern

```python
def pull_all_mods(piid):
    records = []
    start = 0
    while True:
        q = f'PIID:"{piid}"'
        url = f"{BASE}&{urlencode({'q': q})}&start={start}"
        xml = fetch(url)
        page = list(parse_entries(xml))
        if not page:
            break
        records.extend(page)
        # Find last page
        last = re.search(r'rel="last".*?start=(\d+)', xml)
        if last and start >= int(last.group(1)):
            break
        start += 10
        time.sleep(0.3)
    return records
```

This is the foundation of the per-mod window-delta computation
methodology described in v1 §14. With PIID search working, you can
hit each in-scope contract directly instead of doing broad sweeps.

### Lesson

**Re-test v1 claims when you build a new pull.** The FPDS feed is
an old system and behavior may have changed. The previous "PIID
search doesn't work" claim cost the v1 author significant
workarounds.

---

## 10. Per-Mod Sum Method: SLIN Splits and Option-Exercise Caveats

The v1 §14 alternative method recommends summing per-mod
`obligatedAmount` (this action only) for window-delta computation.
We used this method extensively in this session and discovered two
new failure modes.

### Failure mode 1: SLIN-split CARs

Some mods produce **multiple Contract Action Records (CARs) for the
same mod number**, typically one for FMS scope and one for US scope,
each with its own `obligatedAmount` and `totalObligatedAmount`.

Example: `N0002425C5501` (Raytheon SPY-6 FoR design agent) has 18
mods, but each mod has 2 CARs:

```
2025-05-30 mod=0       this=$3.1M   total=$4.9M    (FMS scope)
2025-05-30 mod=0       this=$54.4M  total=$229.6M  (US scope)
2025-06-23 mod=P00001  this=$0.0M   total=$4.9M    (FMS)
2025-06-23 mod=P00001  this=$43.8M  total=$229.6M  (US)
```

The `totalObligatedAmount` field reports per-SLIN totals, not
contract totals. If you read "the latest mod's total" you get
$4.9M (the FMS view) — wildly understating the $235M contract.

Per-mod sum across all CARs gives the right answer: $205M (sum of
all "this action" values across all 18 mods). But you have to sum
**all** CARs, not pick one per mod.

**Recognition:** When `window_delta_sum` substantially **exceeds**
`latest_in_window_total_obligated`, you have SLIN splits. The
per-mod sum is correct.

### Failure mode 2: Option-exercise undercounting

Some mods exercise options or incorporate previously-authorized
changes, where the cumulative `totalObligatedAmount` jumps but the
per-mod `obligatedAmount` (this action only) is recorded as $0.

Example: `N0002424C2467` (HII LHA 10 AP) — fully window-native FY23
contract:

```
2025-08-13 mod=A00003  this=$0.0M   total=$306.3M
2025-12-17 mod=P00006  this=$15.2M  total=$807.0M
```

Between the two mods, the cumulative jumped from $306M to $807M
($501M increase) but only $15M was recorded as new per-mod
obligation. There's $486M of "phantom" growth that the per-mod sum
misses.

Per-mod sum across all mods of this contract: $322M.
Latest in-window cumulative: $807M.
Real value somewhere in between (likely closer to $807M because the
contract is fully window-native).

**Recognition:** When `window_delta_sum` is substantially **less
than** `latest_in_window_total_obligated` for a window-native
contract (no pre-window mods), you have option-exercise
undercounting. The cumulative is more accurate.

### Combined heuristic

For window-native contracts where the per-mod sum and latest
cumulative disagree, **trust the larger number** as a conservative
estimate of true window obligation:

```python
true_window_obligation = max(
    window_delta_sum,
    latest_in_window_total_obligated  # if no pre-window mods
)
```

For straddle contracts (some pre-window mods), the per-mod sum is
more conservative and probably right:

```python
if pre_window_total_obligated > 0:
    true_window_delta = window_delta_sum  # per-mod sum
else:
    true_window_delta = max(window_delta_sum, latest_in_window_total_obligated)
```

### Lesson

**Compute both numbers and compare.** If they disagree by more than
~5%, investigate. The per-mod sum is more accurate in some cases
and the cumulative is more accurate in others; the right choice
depends on the contract's mod structure.

---

## 11. The Vendor-Sweep Round 3 Catches a Lot

The v1 lessons §4 three-round pattern (description → vendor →
agency+dollar-floor) was validated in this session as essential.
Round 3 specifically caught contracts the original keyword search
missed completely.

### What round 3 found

Sweep query:
```
VENDOR_NAME:"RAYTHEON" 
CONTRACTING_AGENCY_ID:"1700" 
SIGNED_DATE:[2023/01/01,2026/04/10] 
OBLIGATED_AMOUNT:[100000000,99999999999]
```

This caught **13 in-scope Raytheon contracts** the prior file's
keyword pull missed entirely. The combined window obligation:
**~$7.5B**.

| PIID | Window Δ | Description |
|---|---|---|
| N0002424C5408 | $1.38B | GMA (MK25) Option Exercise + TE |
| N0002420C5405 | $1.15B | SM Increase Production Capacity |
| N0002424C6104 | $765M | SM Production Lot #2 |
| N0002421C5411 | $719M | SM-2 BLK IIIB TAC AUR |
| N0002422C5400 | $638M | RAM GMRP MK 44 MOD 6 BLK 2B |
| N0002425C5409 | $573M | FY25 SM-6 BLK IA TAC AUR |
| N0002418C5432 | $495M | Encanistered Missile (EM) |
| N0002423C5408 | $484M | SM-2 DLMF Maintenance Spares |
| N0002421C5406 | $400M | Block 1B BSL2 Class A Overhaul |
| N0002424C5406 | $377M | FY25 CIWS Production |
| N0038325FNE02 | $165M | Non-Recurring Demand #2 |
| N0002426C5403 | $146M | FY26 RAM GMRP MK 44 MOD 6 BLK 2B |
| N0038325F0NE1 | $139M | MK-99 PBL NRD Order #1 |

**Without round 3, the FY2026 file would have shown $0 of in-window
Standard Missile activity** (because the 6 SM PIIDs in the prior
file were all pre-window or borderline straddle). The real
Standard Missile family window total is $5.73B, surfaced almost
entirely by the round 3 sweep.

### Why keyword search missed these

Most of these contracts had descriptions that didn't include the
exact phrase "STANDARD MISSILE":
- "GMA (MK25)" — refers to Guided Missile Assembly
- "ENCANISTERED MISSILE (EM)" — refers to packaging
- "RAM GMRP" — Rolling Airframe Missile Guided Missile Round Pack
- "PRODUCTION LOT #2" — generic
- "MK-99 PBL NRD" — Mk 99 Performance-Based Logistics

A search for `DESCRIPTION_OF_REQUIREMENT:"STANDARD MISSILE"` doesn't
match any of these. But they're all in scope.

### Recommended round 3 sweeps for surface combatant work

For any future surface-combatant analysis, run these sweeps as
mandatory backstops:

```python
# Major prime vendors x Navy x dollar floor
for vendor in ["RAYTHEON", "LOCKHEED MARTIN", "NORTHROP GRUMMAN",
               "BAE SYSTEMS", "GENERAL DYNAMICS", "HUNTINGTON INGALLS"]:
    sweep(f'VENDOR_NAME:"{vendor}" '
          f'CONTRACTING_AGENCY_ID:"1700" '
          f'SIGNED_DATE:[2023/01/01,2026/04/10] '
          f'OBLIGATED_AMOUNT:[100000000,99999999999]')
```

Plus the agency-only catch-all:
```python
sweep('CONTRACTING_AGENCY_ID:"1700" '
      'SIGNED_DATE:[2025/01/01,2026/04/10] '
      'OBLIGATED_AMOUNT:[100000000,99999999999]')
```

### Lesson

**Always run round 3 sweeps before finalizing any analysis.** The
~$7.5B Standard Missile gap in the prior file was a known-knowable
miss that round 3 catches automatically.

---

## 12. Background Scripts + Incremental Save

Pulls of 100+ PIIDs take 5-30 minutes. Script crashes, network
hiccups, and rate-limit retries happen. Always design for
resumability.

### The pattern

```python
def main():
    # Load existing cache
    data = load_cache()
    print(f"Cached: {len(data)}")
    
    for piid in PIIDS:
        if piid in data and data[piid].get("_complete"):
            continue  # skip cached
        
        # Pull this PIID
        try:
            result = pull_subawards(piid)
        except Exception as e:
            data[piid] = {"error": str(e), "_complete": False}
            save_cache(data)
            continue
        
        data[piid] = {**result, "_complete": True}
        save_cache(data)  # ← save after EVERY PIID, not at end
```

### Why the `_complete` flag matters

Without the `_complete` boolean, you can't distinguish "cached and
finished" from "cached but errored mid-pull". The next run will
either:
- Skip an erroring PIID forever (missing data)
- Re-pull a finished PIID (wastes time)

The `_complete: True` flag lets the resume logic do the right thing.

### Save format: atomic write

```python
def save_cache(data):
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, OUT)  # atomic
```

A direct write-to-final could corrupt the cache if interrupted
mid-write. The tmp + atomic-rename pattern is safe.

### Background execution

For multi-PIID pulls, run in the background:

```bash
python3 -u my_pull.py 2>&1 | tee my_pull.log &
```

Use `-u` for unbuffered output so the log file gets updates in
real-time. Use `tee` to both display and save. Background lets you
work on the next thing while the pull runs.

### Reasonable progress checks

While a long pull runs, check progress periodically without
disrupting it:

```bash
python3 -c "
import json
with open('subaward_full.json') as f:
    d = json.load(f)
print(f'{len([k for k,v in d.items() if v.get(\"_complete\")])} / 170')
"
```

Don't poll the running script's stdout — read the cache file
directly.

### Lesson

**Treat every API pull as if it might fail mid-run.** The
incremental-save pattern adds 10 lines of code and saves hours when
something goes wrong. For 170-PIID pulls it's mandatory.

---

## 13. Recommended Pull Pipeline for Subaward-Focused Analyses

Based on this session's experience, here's the pipeline I'd
recommend for any future analysis where subcontractor data is the
primary deliverable:

### Step 1: Build the prime PIID list

a. **Description-keyword sweeps** (the v1 §4 round 1) — get the
   first wave of obviously-relevant primes
b. **Vendor-name sweeps** (round 2) — catch contracts with
   non-matching descriptions
c. **Agency + dollar-floor backstop** (round 3) — see §11 above
d. **Vendor + agency + dollar-floor** for each major prime — catches
   newer contracts the keyword pull missed

### Step 2: Per-mod FPDS pull

For each prime PIID, pull all mods via `PIID:"<piid>"` query (§9).
Compute window deltas via per-mod sum AND cumulative-method delta;
compare them and use the larger for window-native contracts (§10).

### Step 3: Subaward pull with v3 dedup

For each prime PIID:
a. Look up `generated_internal_id` via `/search/spending_by_award/`
   (try contracts group, then IDV group fallback)
b. Pull all subaward records via `/subawards/`
c. Apply Stage 1 dedup (per `sub_id` MAX) immediately
d. Save to cache (incremental, see §12)

After the full pull:
e. Apply Stage 2 dedup (collapse identical amounts)
f. Apply Stage 3 cap-and-exclude
g. Aggregate by recipient with vendor normalization
h. Roll up to parent companies (see §6)

### Step 4: Per-program rollups

Group PIIDs by program area and produce per-program subaward
breakdowns. Useful for "who are the major subs on SPY-6 vs CIWS vs
LCS construction".

### Step 5: Sanity checks

a. Any single (recipient, prime) pair > $500M → manual review
b. Any cross-PIID parent-company total > $1B → spot-check the
   contributing PIIDs
c. Any prime where 3+ recipients show identical large amounts →
   exclude the prime entirely (corrupted data)
d. Any sub > prime contract value → cap or exclude
e. Compare window deltas (per-mod sum) vs latest cumulative for
   each PIID — large mismatches need investigation

### Step 6: Acknowledge limits explicitly

In the final output, document:
- Which PIIDs were re-pulled with corrected dedup
- Which were inherited from prior analyses (if any)
- Which subs were capped or excluded
- Which BIW / Bollinger / Birdon-style primes have zero sub reporting

The reader needs to know what's been verified vs what's directional.

---

## 14. Quick-Reference Code Snippets

### v3 subaward dedup (the algorithm)

```python
from collections import defaultdict

def v3_subaward_dedup(records, prime_size, slack=1.0, exclude=2.0):
    """3-stage dedup for USAspending subaward records.
    
    records: list of dicts with sub_id, recipient_name, amount, action_date
    prime_size: prime contract's total obligation (use larger of
                window_delta and latest_cumulative)
    """
    # Stage 1: per sub_id MAX
    by_sid = defaultdict(list)
    for r in records:
        sid = r.get("sub_id") or ""
        by_sid[sid].append(r)
    stage1 = [max(recs, key=lambda x: x.get("amount") or 0)
              for recs in by_sid.values()]
    
    # Stage 2: collapse identical (recipient, amount) duplicates
    seen = set()
    stage2 = []
    for r in stage1:
        rec = (r.get("recipient_name") or "").strip()
        amt = round(r.get("amount") or 0, 2)
        key = (rec, amt)
        if key in seen:
            continue
        seen.add(key)
        stage2.append(r)
    
    # Aggregate by recipient
    by_rec = defaultdict(float)
    for r in stage2:
        rec = (r.get("recipient_name") or "").strip()
        if not rec:
            continue
        by_rec[rec] += r.get("amount") or 0
    
    # Stage 3: cap and exclude
    if prime_size <= 0:
        return dict(by_rec), [], []
    
    cap = prime_size * slack
    exclusion = prime_size * exclude
    capped = {}
    flagged = []
    excluded = []
    for rec, amt in by_rec.items():
        if amt > exclusion:
            excluded.append({"recipient": rec, "raw": amt})
            continue
        if amt > cap:
            capped[rec] = cap
            flagged.append({"recipient": rec, "raw": amt, "capped_at": cap})
        else:
            capped[rec] = amt
    
    return capped, flagged, excluded
```

### Two-call subaward pull (the workflow)

```python
import json
import urllib.request

CONTRACT_GROUPS = [
    ["A", "B", "C", "D"],  # Contracts
    ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C",
     "IDV_C", "IDV_D", "IDV_E"],  # IDVs
]

def find_gid(piid):
    """Find generated_internal_id for a PIID. Try contracts then IDV."""
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
            "fields": ["generated_internal_id"],
            "limit": 1,
            "page": 1,
        }
        try:
            j = post_json(url, payload)
            if j.get("results"):
                return j["results"][0]["generated_internal_id"]
        except urllib.error.HTTPError as e:
            if e.code == 422:
                continue  # try IDV group
            raise
    return None

def pull_subs(gid, max_records=5000):
    """Page through all subawards for a generated_internal_id."""
    url = "https://api.usaspending.gov/api/v2/subawards/"
    subs = []
    page = 1
    while len(subs) < max_records:
        payload = {
            "award_id": gid,
            "limit": 100,
            "page": page,
            "sort": "amount",
            "order": "desc",
        }
        j = post_json(url, payload)
        results = j.get("results", [])
        if not results:
            break
        subs.extend(results)
        if not j.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
    return subs
```

### Vendor-name normalization

```python
import re

SUFFIX_RE = re.compile(
    r"\b(INC\.?|L\.?L\.?C\.?|CORP\.?|CORPORATION|CO\.?|LTD\.?|LP|L\.P\.|"
    r"COMPANY|HOLDINGS|GROUP|PARTNERSHIP|LIMITED)\b\.?,?\s*$",
    re.IGNORECASE,
)

def normalize_vendor(name):
    """Strip legal-entity suffixes and normalize whitespace."""
    if not name:
        return None
    s = name.upper().strip()
    s = re.sub(r"[,.]\s*$", "", s)
    for _ in range(3):
        new = SUFFIX_RE.sub("", s).strip().rstrip(",.")
        if new == s:
            break
        s = new
    return re.sub(r"\s+", " ", s).strip() or None
```

### Detection: phantom-amount cluster on a single prime

```python
def detect_phantom_cluster(per_recipient, prime_size, threshold=0.5):
    """Returns True if 3+ recipients have identical (rounded) amounts
    that exceed `threshold * prime_size`. Indicates USAspending data
    corruption like the NASSCO Cowpens case."""
    if prime_size <= 0:
        return False
    floor = prime_size * threshold
    by_amt = defaultdict(list)
    for rec, amt in per_recipient.items():
        if amt > floor:
            by_amt[round(amt, 0)].append(rec)
    return any(len(recs) >= 3 for recs in by_amt.values())
```

---

## 15. Summary -- The Most Important Things

If you only remember 7 things from this file:

1. **USAspending subaward records have a cumulative-snapshot
   duplication problem.** The `/api/v2/subawards/` endpoint returns
   multiple records for the same `subaward_number` at different
   action_dates, each at a cumulative-style amount. Naive sums
   inflate by 5-50x. Always apply per-`sub_id` MAX dedup first.
   (See §1.)

2. **The v3 3-stage dedup is the right algorithm.** Stage 1 (per
   `sub_id` MAX), Stage 2 (collapse identical recipient-amount
   duplicates), Stage 3 (cap at 1.0× prime, exclude > 2× prime).
   Each stage catches a different failure mode. (See §2.)

3. **A sub cannot exceed its prime contract value.** If your data
   says otherwise, your data is wrong. Build the cap-at-prime check
   into the aggregator. For long-running contracts, use the larger
   of (window delta, latest cumulative) as the cap basis. (See §4
   and §5.)

4. **Vendor normalization with hand-curated parent-company mapping
   is unavoidable.** GD has 10+ legal entities, L3Harris has 8+.
   Build a mapping table once and version it. Without rollup, your
   "top hidden subs" table is fragmented and useless. (See §6.)

5. **Apparent prime/sub mismatches on long-running contracts are
   normal, not bugs.** A FY10 prime with $250M of new in-window
   obligation can have a $2.49B in-window sub delivery because the
   sub is spending down pre-window-funded scope. Don't try to "fix"
   this. (See §5.)

6. **PIID search in FPDS Atom Feed works** (correcting v1 §2). Use
   `q=PIID:"N0002422C5500"` (quoted, no hyphens). This enables
   per-mod pulls per PIID without broad sweeps, much more efficient
   than the v1-recommended workflow. (See §9.)

7. **Per-mod sum and cumulative-method window deltas should agree
   for window-native contracts.** When they don't, you have either
   SLIN-split CARs (per-mod sum is right) or option-exercise mods
   (cumulative is right). Compute both, compare, and trust the
   larger for window-native; trust per-mod sum for straddles.
   (See §10.)

### Bonus -- the corrections this methodology produced

The v3 dedup applied to all 170 in-scope PIIDs in the FY2026 key
programs analysis dropped grand-total in-window subs from a prior-
file-implied **$80B+** to a corrected **$10.35B**. Individual vendor
corrections:

| Vendor | Prior | v3 corrected | Ratio |
|---|---|---|---|
| Marinette Marine | $47.17B | $2.49B | 19x |
| LM SEWIP Block 2 (total subs) | $2.85B | ~$0.005B | 570x |
| HELIOS MZA Associates | $395M | $25M | 16x |
| Hampton Roads PCE | $942M | $30M | 31x |
| CAES + Mercury combined RF | $5B+ | $503M | 10x |

Every number in the prior file was inflated. The v3 dedup is what
makes the corrected output trustworthy.

---

*Generated 2026-04-10 from direct experience pulling FPDS Atom Feed
and USAspending subawards for the FY2026 surface combatant + amphib
key programs analysis. Companion to
`Federal_Procurement_Research_Lessons_Learned.md` (v1 lessons file)
and `FY2026_Key_Programs_Contract_Awards.md` (the analysis output).*

*This file documents lessons learned AFTER the v1 file was written,
specifically the USAspending subaward cumulative-snapshot
duplication problem and the 3-stage v3 dedup that fixes it. If you
do future subaward-focused analyses, read §1, §2, §11, and §15
first.*
