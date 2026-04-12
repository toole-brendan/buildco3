# FY2026 Key Programs -- Contract Award Analysis

**Scope:** Surface combatants and amphibious warfare ships listed in the
user-provided `key programs.xlsx` (FY2026 Budget Justification books +
DAA JES FY2026): **LHD, LPD, LSD, LHA, DDG (DDG-51 + DDG-1000), LCS, CG**.

**Window:** FPDS prime contracts and USAspending subawards, signed dates
**2020-01-01 through 2026-04-10**.

**Sources (fresh API pulls — see §23 for full pipeline):**
- FPDS Atom Feed (`https://www.fpds.gov/ezsearch/FEEDS/ATOM`) -- per-mod pull on **82 in-scope PIIDs**, summing per-mod `obligatedAmount` (this action only) for true window deltas per Lessons-Learned §14 alternative method
- USAspending `/api/v2/search/spending_by_award/` -- PIID → `generated_internal_id` lookup
- USAspending `/api/v2/subawards/` -- first-tier subaward tree, **deduped per unique `sub_id` taking max amount** (not summed across action_dates) to avoid the cumulative-style double-counting that produced the $47.17B Marinette anomaly
- FPDS sweeps for new vehicles: Raytheon SM/CIWS/RAM signed FY23+, and Navy AGENCY_CODE 1700 dollar-floor backstop at $100M+ for FY25-26 — **surfaced 13 new in-scope PIIDs** the original keyword pull missed (see §16 and §12.5)

**Companion files:**
- `federal_procurement_data_guide.txt` -- API field reference
- `Federal_Procurement_Research_Lessons_Learned.md` -- gotchas and workflow notes
- `SAM_Submarine_Cutter_Contract_Awards.md` -- companion file for sub/cutter scope

**Supersedes within this scope:** `SAM_Program_Contract_Awards.md` and
`SAM_Program_Component_Contracts.md`. Those older files cover the same hulls
but were written before the cumulative-vs-window trap (Lessons-Learned §14)
and the >$5B sub-sanity rule (Lessons-Learned §7) were established. This file
applies both **and** is built on fresh API pulls rather than synthesizing
the older files' derived numbers.

---

> ## ✅ Window deltas are computed -- not cumulative figures
>
> Every "Window Δ (FY20-26)" column in this file is the **sum of per-mod
> `obligatedAmount` (this action only) values across all in-window mods**,
> per Lessons-Learned §14 alternative method. This produces **true
> FY20-26 obligation deltas**, not cumulative-since-contract-award.
>
> The previous version of this file showed cumulative numbers with
> `[PRE]/[STR]/[NEW]` tags as a workaround. The fresh per-mod pull replaces
> those tags with actual numbers. For reference, the prior cumulative is
> still shown in a "Cumulative" column where useful, so you can see the
> magnitude of correction.
>
> **The corrections were significant.** Examples:
>
> | PIID | Prior cumulative | True FY20-26 window Δ | Pre-window leakage |
> |---|---|---|---|
> | N0002418C2307 (HII DDG FY18-22 MYP) | $6.72B | **$4.06B** | $2.66B |
> | N0002418C2305 (BIW DDG FY18-22 MYP) | $5.34B | **$3.31B** | $2.03B |
> | N0002413C2305 (BIW DDG FY13-17 MYP) | $4.93B | **$0.48B** | $4.45B (90% pre-window) |
> | N0002413C2307 (HII DDG 117 FY13/16) | $3.35B | **$0.36B** | $2.99B |
> | N0002416C2431 (HII LPD 28) | $3.00B | **$0.08B** | $2.92B (97% pre-window!) |
> | N0002416C2427 (HII LHA 8) | $3.27B | **$1.01B** | $2.26B |
> | N0002418C2406 (HII LPD 30/31/32) | $4.63B | **$3.18B** | $1.45B |
> | N0002406C2303 (BIW DDG-1000) | $3.31B | **$0** | $3.31B (100% pre-window) |
> | N0002416C5363 (LM SEWIP Block 2) | $0.57B | **$0.005B** | $0.57B (99% pre-window!) |
> | N0002411C2300 (LM LCS Freedom) | $4.98B | **$0.25B** | $4.74B |
>
> **Per-mod method caveat:** A small number of contracts have option-exercise
> mods where the cumulative jumps but the per-mod `obligatedAmount` field is
> recorded as $0 or much smaller. For those, the per-mod sum understates
> reality. Conversely, contracts with multi-SLIN structure (FMS + US splits)
> may have per-mod sums that exceed the latest single-SLIN cumulative
> snapshot. Both effects are visible in the data and noted where they matter.
> The per-mod sum method is still strictly more accurate than reporting
> `totalObligatedAmount` cumulative-since-award as if it were window spend.

---

> ## ✅ Marinette Marine $47.17B subaward -- RESOLVED
>
> The previous version of `SAM_Program_Contract_Awards.md` reported
> Marinette Marine Corporation as a **$47.17 billion** subcontractor on the
> Lockheed Martin LCS Freedom-variant prime contract `N0002411C2300`. This
> file's first draft flagged the figure as corrupted but couldn't replace
> it. The fresh re-pull resolves the anomaly.
>
> **Root cause identified.** USAspending's `/api/v2/subawards/` endpoint
> returns subaward records that include cumulative-style amounts at each
> snapshot date. For example, sub_id `4100090097` (one Marinette
> subcontract) appears 12 times in 2020-2021 with amounts of ~$497M,
> ~$498M, ~$499M -- each a slightly-grown snapshot of the same subaward
> over time. The previous file summed all 12, getting $6B for one $500M
> subcontract. The original "$47.17B Marinette" figure was the
> aggregate of this same double-counting across 23 distinct Marinette
> subcontract IDs.
>
> **Corrected dedup applied.** Four iterations were needed to find the
> right approach:
>
> | Method | Marinette total |
> |---|---|
> | Original (cumulative-summed) | $47.17B |
> | Naive dedup by `(sub_id, action_date, recipient, amount)` | $37.77B (still corrupted -- each snapshot has unique date) |
> | Per `sub_id` MAX | $2.49B (validates) |
> | v3 with cap at 1.0× prime | **$2.49B** (uncapped because LM LCS Freedom prime is $4.98B cumulative) |
>
> **The real number is ~$2.5B**, distributed across 23 distinct Marinette
> subcontracts. This is plausible for the Freedom-variant LCS program
> (Marinette is the actual builder; LM Lockheed Martin is systems
> integrator and prime of record). It is consistent with the
> Virginia/Columbia EB/HII team-build pattern (Lessons §10).
>
> **The same 3-stage v3 dedup was applied to ALL 170 in-scope PIIDs** in
> a comprehensive subaward re-pull (82 construction/modernization/weapons
> primes + 88 depot maintenance availabilities). Cross-PIID parent-company
> rollups in §22 are built from this corrected dataset.
>
> **Note on the apparent prime/sub mismatch.** The LM LCS Freedom prime
> N0002411C2300 has only **$250M of new in-window obligation** (per per-mod
> sum), but Marinette's in-window subaward delivery was $2.49B. This is
> consistent with Marinette delivering FY20-25 ship work that was funded
> by **pre-2020 prime obligations** -- the contract was awarded in FY10
> with a $4.74B pre-window cumulative, and Marinette has been spending
> down that pre-window-funded scope ever since. The $250M new prime
> obligation in window represents incremental scope, not the total
> Marinette pipeline.
>
> **The same correction was applied to all 170 in-scope PIIDs** (not
> just the 6 originally-suspect ones). The most dramatic corrections:
>
> | Vendor | Prior file claim | v3 corrected | Ratio |
> |---|---|---|---|
> | Marinette Marine | $47.17B | $2.49B | 19x lower |
> | LM SEWIP Block 2 total subs | $2.85B | ~$0.005B | 570x lower (99% pre-window) |
> | NG Knifefish/LCS total subs | $1.48B | $0.13B | 11x lower |
> | LM SLQ-32(V)6 total subs | $1.42B | $0.33B | 4x lower |
> | HELIOS MZA Associates | $395M | $25M | 16x lower |
> | HELIOS L3 Technologies | $209M | $22M | 9x lower |
> | Hampton Roads PCE (LHD depot) | $942M | $30M | 31x lower |
> | TECNICO (LHD depot) | $230M | $55M | 4x lower |
> | DRS Network & Imaging (CIWS) | $233M | (in noise) | huge |
> | CAES + Mercury combined SPY-6/SEWIP/SLQ-32 | $5B+ claim | $503M | 10x lower |
>
> See §22 for the full corrected vendor totals across all 170 PIIDs.

---

## Table of Contents

### A. New Construction (SCN)
1. [DDG-51 Arleigh Burke -- New Construction](#1-ddg-51-arleigh-burke--new-construction)
2. [DDG-1000 Zumwalt -- Closeout & Activation](#2-ddg-1000-zumwalt--closeout--activation)
3. [LPD Flight II -- New Construction](#3-lpd-flight-ii--new-construction)
4. [LHA Replacement -- New Construction](#4-lha-replacement--new-construction)

### B. Scheduled Depot Maintenance & Repair (OMN)
5. [DDG-51 Depot Maintenance](#5-ddg-51-depot-maintenance)
6. [LHD Depot Maintenance](#6-lhd-depot-maintenance)
7. [LPD Depot Maintenance](#7-lpd-depot-maintenance)
8. [LSD Depot Maintenance](#8-lsd-depot-maintenance)
9. [LHA Depot Maintenance](#9-lha-depot-maintenance)
10. [LCS Depot Maintenance](#10-lcs-depot-maintenance)
11. [CG Ticonderoga Depot Maintenance](#11-cg-ticonderoga-depot-maintenance)

### C. Modernization & Alteration Installation
12. [DDG Modernization -- Combat Systems & Subsystems](#12-ddg-modernization--combat-systems--subsystems)
13. [LCS In-Service Modernization & Mission Modules](#13-lcs-in-service-modernization--mission-modules)
14. [LHA/LHD Midlife & LPD/LSD Class Support](#14-lhalhd-midlife--lpdlsd-class-support)
15. [DDG-1000 Class Support Equipment](#15-ddg-1000-class-support-equipment)

### D. Weapons (WPN + OPN BA2/BA4)
16. [Standard Missile (WPN 2234) + Standard Missile Mods (WPN 2356)](#16-standard-missile-wpn-2234--standard-missile-mods-wpn-2356)
17. [MK-54 Torpedo Mods (WPN 3215)](#17-mk-54-torpedo-mods-wpn-3215)
18. [Naval Strike Missile (WPN 2292) + LCS Module Weapons (WPN 4221)](#18-naval-strike-missile-wpn-2292--lcs-module-weapons-wpn-4221)
19. [Surface Ship Torpedo Defense -- SSTD (OPN BA2 2213)](#19-surface-ship-torpedo-defense--sstd-opn-ba2-2213)
20. [Ship Gun Systems Equipment (OPN BA4 5111)](#20-ship-gun-systems-equipment-opn-ba4-5111)
21. [Airborne MCM (OPN BA3 119)](#21-airborne-mcm-opn-ba3-119)

### E. Cross-Cutting
22. [Summary -- Top Primes & Hidden Subs](#22-summary--top-primes--hidden-subs)
23. [Methodology & Limitations](#23-methodology--limitations)
24. [SAM Line Item → Contract Vehicle Crosswalk](#24-sam-line-item--contract-vehicle-crosswalk)

---

# A. NEW CONSTRUCTION

## 1. DDG-51 Arleigh Burke -- New Construction

**FY26 SAM:** SCN 2122 -- **$5,410,773K** procurement + **$1,750,000K** advance
procurement. Combined ~**$7.16B** for FY26.

**Dual-source procurement strategy** with two prime shipbuilders. HII Ingalls
(Pascagoula, MS) and Bath Iron Works / GD (Bath, ME) split the production
schedule. BIW additionally serves as the **DDG-51 Lead Design Yard** and
holds the planning yard contract for class engineering across all hulls.

### Active Construction MYP Vehicles (window deltas from per-mod pull)

| PIID | Contractor | Block | **FY20-26 Window Δ** | Cumulative (latest in-window mod) | Pattern |
|---|---|---|---|---|---|
| **N0002423C2307** | HII Ingalls | DDG 51 FY23-27 MYP | **$6.95B** | $6.95B | NEW (window-native ✓) |
| **N0002423C2305** | BIW | DDG 51 FY23-27 MYP | **$5.03B** | $5.03B | NEW (window-native ✓) |
| **N0002418C2307** | HII Ingalls | DDG 51 FY18-22 MYP | **$4.06B** | $6.83B | STR (60% in window) |
| **N0002418C2305** | BIW | DDG 51 FY18-22 MYP | **$3.31B** | $5.34B | STR (62% in window) |
| **N0002413C2305** | BIW | DDG 51 FY13-17 MYP | **$0.48B** | $4.93B | STR (10% in window — closeout mods) |
| **N0002413C2307** | HII Ingalls | DDG 117 FY13/FY16 | **$0.36B** | $3.35B | STR (11% in window — closeout) |

**True FY20-26 window spend across the 6 MYP vehicles: ~$20.19B** (vs the
~$32.3B cumulative the prior file would have implied). The previous file
significantly overstated DDG-51 new construction window obligation by
approximately **$12B** -- almost the full value of the FY13-17 MYP plus
DDG 117 FY13/16 plus the pre-window portions of the FY18-22 MYPs.

### DDG-51 Lead Yard, Planning, and Combat System

| PIID | Contractor | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002418C2313** | BIW | **$182M** | $303M | DDG 51 Lead Yard Services FY18-22 (60% in window) |
| **N0002424C2313** | BIW | **$186M** | $186M | DDG 51 Lead Yard Services FY24+ (window-native) |
| **N0002403C5115** | Lockheed Martin | **$0** | $972M | DDG-51 Aegis Combat System (legacy, fully pre-window) |
| N0016422F3012 | Serco Inc | -- | $146M | Ship production planning (not in per-mod pull) |
| -- | QED Systems | -- | $140M | Third-party planning DDG 51 / CG 47 (not in per-mod pull) |

### Top First-Tier Subcontractors -- HII DDG-51 Stack (v3 corrected)

Aggregated across the 5 HII DDG-51 prime PIIDs after v3 dedup. **Total
in-window HII DDG-51 subs: ~$523M** (vs the prior file's $2.89B claim,
which was inflated ~5.5x by cumulative-snapshot duplication).

| Subcontractor | Sub $ (corrected, cross-PIID) | Role |
|---|---|---|
| **General Electric** (LM2500 turbines) | **$87M** (across N0002423C2307 + N0002418C2307) | LM2500 main propulsion gas turbines |
| **Johnson Controls** (incl. York International) | **$76M+** | HVAC / chilled water plants |
| **Rolls-Royce Marine North America** | **$96M** (across HII DDG PIIDs) | Propulsion components, gas turbines, gearing |
| **Timken Gears & Services** | **$41M** | Reduction gearing |
| **Leonardo DRS** (Naval Power Systems) | **$17M** | Switchboards, power distribution |
| **L3Harris Maritime Power & Energy Solutions** | **$14M** | Power conversion / electrical |
| **Ellwood National Forge** | **$13M** | Propulsion shafts |
| **Northrop Grumman Systems** | **$13M** | DDG steering systems |
| **Espey Mfg & Electronics** | **$13M** | Power conditioning |
| **Howden North America** | **$9M** | Fans / blowers |
| **Engineered Coil** | **$7M** | Coiled components / heat exchangers |
| **Southcoast Welding & Manufacturing** | **$9M** | Welding services |
| **Marmon Aerospace & Defense** | **$12M** | Various |
| **The Monroe Cable Company** | **$8M** | Marine cable |
| **Steelfab** | **$9M** | Steel fabrication |

**Per-prime detail (top sub volumes):**
- N0002418C2307 (HII FY18-22 MYP): $574M total subs — Rolls-Royce $94M, GE $64M, York Int'l $22M, Ellwood Forge $17M, JCNS $17M, DRS Naval Power $16M
- N0002423C2307 (HII FY23-27 MYP): $345M total subs — GE $87M, JCNS $74M, Timken $41M, DRS Naval Power $16M, Ellwood Forge $15M
- N0002413C2307 (HII DDG 117 FY13/16): $56M total subs — Southcoast Welding $9M (closeout)
- N0002418C2305 (BIW FY18-22): $46M reported — Johnson Controls Navy Systems $25M, the rest tiny
- N0002413C2305 (BIW FY13-17): $5M reported — almost nothing in window

> **BIW under-reporting confirmed.** BIW DDG-51 PIIDs report ~$51M of
> in-window subs total across 2 PIIDs (vs HII DDG-51's $523M across 3
> PIIDs). Per Lessons §6 this is a known FFATA reporting non-compliance
> pattern, not an absence of subcontracting. The "true" BIW supplier
> footprint is invisible in USAspending.

> **Cross-program note:** "Rolls-Royce" totals here ($96M) appear in the
> §22 Top Parents table at **$313M** because Rolls-Royce also supplies
> propulsion to LCS Freedom ($196M sub on N0002411C2300), LPD/LHA, and
> appears as mtu in depot diesel rebuild work.

### BIW DDG-51 Subaward Gap

> **⚠️ BIW reports near-zero subawards across all 6 BIW DDG-51 PIIDs**
> (~$60M total, vs. ~$15B in primes). Per Lessons-Learned §6, this is a
> known FFATA reporting non-compliance pattern, not an absence of
> subcontracting activity. The "true" BIW subcontractor footprint is
> almost certainly comparable to HII's (propulsion, HVAC, hull steel,
> combat systems integration) but is invisible in USAspending. Known BIW
> suppliers from public sources include the same Maine/New England
> machining and fabrication base, plus Rolls-Royce/GE for propulsion and
> Lockheed Martin for Aegis.

---

## 2. DDG-1000 Zumwalt -- Closeout & Activation

**FY26 SAM:** SCN 2119 -- **$52,358K** for FY26 (closeout funding only).
Three-ship class (DDG 1000, DDG 1001, DDG 1002), construction complete; the
remaining funds support activation, mission system upgrades, and CPS
hypersonic conversion.

### Prime Contracts (window deltas from per-mod pull)

| PIID | Contractor | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002422C5522** | Raytheon | **$568M** | $571M | AS&M Support (window-native) |
| **N0002423C2324** | HII | **$308M** | $329M | DDG 1000/1001 Mod Planning (window-native) |
| **N0002417C5145** | Raytheon | **$282M** | $790M | Total Ship Activation / MSE (36% in window) |
| **N0002424C2331** | BIW | **$196M** | $227M | Planning Yard Follow On (window-native) |
| **N0002406C2303** | Bath Iron Works | **$0** | $3.31B | DDG-1000 lead shipbuilder (FY06 award, **100% pre-window**) |
| **N0002410C5126** | Raytheon | **$0** | $1.34B | Mission systems integrator (FY10 award, **100% pre-window**) |
| **N0002415C5344** | GD Land Systems | **$0** | $76.6M | MK 46 MOD 2 Gun Weapon System (100% pre-window) |
| HC102820F0610 | Microsoft Corporation | -- | $9.4M | Zumwalt Operating Environment (ZOE) (not in per-mod pull) |
| -- | JHU Applied Physics Lab | -- | ~$12M | Combat System RDT&E (not in per-mod pull) |
| N0002413F2320 | Forethought, Inc. | -- | $30.5M | IDE Engineering Support (not in per-mod pull) |

**True FY20-26 window spend across the 7 pulled DDG-1000 PIIDs: ~$1.35B**
(vs the ~$5.3B cumulative the prior file would have implied). DDG-1000 is
a class in closeout — most of the apparent contract value is FY06-FY18
construction money, not new FY20-26 obligation.

### Top Subcontractors -- DDG-1000 Stack

Aggregated across DDG-1000 prime PIIDs = ~1,237 subaward records, ~$773M
cumulative observed. The single largest sub volume comes from the
**GD Land Systems MK 46 MOD 2 Gun System** (N0002415C5344) at 551 subawards
totaling $501M -- this one weapon system has more subaward visibility than
the entire ship construction.

| Subcontractor | Sub $ | Actions | Role |
|---|---|---|---|
| **Red River Technology** | $62.3M | 28 | DDG-1000 mission system computing |
| **Northrop Grumman Systems** | $51.7M | 13 | Semiconductors / electronics |
| **Systems Engineering & Manufacturing** | $47.6M | 51 | Industrial machinery |
| **Hart Technologies** | $45.2M | 20 | Engineering services |
| **Charles E. Gillman** | $44.8M | 36 | Motor vehicle electronics |
| **Laurel Technologies Partnership** | $43.2M | 14 | Printed circuit boards |
| **Lanzen, Inc.** | $42.5M | 5 | Antenna mounts |
| **Lapeer Industries** | $40.9M | 10 | Mission system parts |
| **VarTech Systems** | $40.8M | 5 | Rugged LCD displays |
| **Raytheon (intra-corporate)** | $34.2M | 16 | Search / detection / nav |
| **Kearfott Corp** | $31.2M | 39 | Inertial navigation |
| **Moog Industrial Controls** | $27.9M | 13 | Semiconductors |
| **Motorola Solutions** | $19.9M | 20 | Software |
| **Dell Marketing** | $17.2M | 19 | Computer hardware |
| **Atrenne Computing Solutions** | $14.5M | 13 | Test and tooling |
| **Curtiss-Wright DS** | $12.9M | 53 | Engineering services |
| **Sirius Federal** | $12.2M | 41 | UCS storage / enterprise hardware |
| **DRS Naval Power Systems** | $4.5M | 17 | Power distribution |
| **GE Energy Power Conversion USA** | $4.2M | 7 | Power conversion |

---

## 3. LPD Flight II -- New Construction

**FY26 SAM:** SCN 3010 -- **$835,037K** procurement + **$275,000K** advance
procurement. Combined ~**$1.11B** for FY26.

**Sole-source to HII Ingalls Shipbuilding** (Pascagoula, MS).

### Prime Contracts (window deltas from per-mod pull)

| PIID | Hulls | **Window Δ** | Cumulative | Ceiling | Description |
|---|---|---|---|---|---|
| **N0002418C2406** | LPD 30 (Harrisburg), 31, 32 | **$3.18B** | $4.72B | $4.66B | FY18 award, 67% executed in window |
| **N0002424C2473** | **LPD 33, 34, 35** | **$1.22B** | $1.22B | **$5.80B** | Block buy, FY24 award. Window-native — early obligation phase against $5.8B ceiling |
| **N0002421C2443** | LPD 17 Class Eng Svcs | **$125M** | $125M | $224.7M | Window-native |
| **N0002416C2431** | LPD 28 (Fort Lauderdale) | **$77M** | $3.00B | $3.26B | FY16 award. **97% pre-window** — almost no new money in FY20-26 |
| **N0002416C2415** | LPD 17 LCE&S Core Services | **$65M** | $307M | $320.7M | 21% in window |
| **N0002426C2443** | LPD 17 PD&ES (Post Delivery) | **$12M** | $20M | $223.3M | FY26 award, just starting |

**True FY20-26 window spend across the 6 pulled LPD PIIDs: ~$4.68B** (vs
~$10.7B cumulative). The previous file overstated by approximately $6B,
mostly from LPD 28 which was effectively fully obligated by 2018-2019.

**Other prime roles:**

| Tag | Contractor | Role | Value |
|---|---|---|---|
| [STR] | BAE Systems Norfolk Ship Repair | LPD 28 Fitting Out Availability | $75.5M / $169M ceiling |
| [STR] | Raytheon Company | LCE&S for electronic systems | $130M / $485M ceiling |
| [STR] | TMASC Joint Venture | LPD 17 Program Office support | $77M |
| [STR] | Northrop Grumman Systems | Pre-commissioning unit support | -- |

### Top Subcontractors -- HII LPD Stack (v3 corrected)

LPD Flight II construction subs after v3 dedup. **Total in-window LPD
subs: ~$340M** across 5 HII LPD PIIDs (vs the prior file's $1.59B claim
which combined LPD + LHA and was inflated ~5x).

| Subcontractor (LPD only) | Sub $ (corrected, cross-PIID) | Role |
|---|---|---|
| **Fairbanks Morse Defense** (Coltec combined) | **$65M** | Diesel generator sets / propulsion |
| **US Joiner** | **$36M** | Interior outfitting / joiner work |
| **Caterpillar** | **$20M** | Diesel engines |
| **Leonardo DRS** (Naval Power Systems) | **$16M** | LPD switchboards / power distribution |
| **American Superconductor Corp** | **$15M** | Likely degaussing system |
| **Timken Gears & Services** | **$12M** | Gearing |
| **Johnson Controls** (combined York + JCNS) | **$11M** | HVAC |
| **L3Harris Maritime P&E Solutions** | **$9M** | Power conversion |
| **Carolina Power Systems of Sumter** | **$8M** | LPD power systems |
| **HHE Services** | **$7M** | Control stations |
| **Ellwood National Forge** | **$7M** | Forgings |
| **Howden North America** | **$6M** | Fans / blowers |

**Per-prime detail:**
- N0002418C2406 (LPD 30/31/32): $505M total subs — US Joiner $55M, DRS Naval Power $41M, Fairbanks Morse $38M, Coltec $34M, Caterpillar $27M, AmSuperconductor $26M, Timken $21M, Carolina Power $15M
- N0002416C2431 (LPD 28): $54M total subs — Industrial Corrosion Control $11M, Supreme Integrated Tech $5M, US Joiner $4M, HHE Services $4M, Auxiliary Systems $3M
- N0002424C2473 (LPD 33/34/35 block buy): minimal subs yet (FY24 award, sub reporting still lagging)

### Top Subcontractors -- HII LHA Stack (v3 corrected)

LHA Replacement subs after v3 dedup. **Total in-window LHA subs: ~$340M**
across N0002416C2427 (LHA 8) + N0002420C2437 (LHA 9).

| Subcontractor (LHA only) | Sub $ (corrected) | Role |
|---|---|---|
| **L3Harris Maritime P&E Solutions** | **$39M** (LHA 9) | Power conversion |
| **Fairbanks Morse Defense** (Coltec combined) | **$40M** (LHA 9) | Diesel propulsion |
| **Leonardo DRS** (Naval Power Systems) | **$34M** (LHA 9) | Switchboards |
| **Industrial Corrosion Control** | **$26M** (LHA 8) | Tank coating |
| **Lake Shore Systems** | **$23M** (LHA 9) | Deck machinery |
| **Johnson Controls** (combined) | **$18M** (LHA 9) | HVAC |
| **Northrop Grumman Systems** | **$15M** (LHA 8) | Various |
| **Thermal Spray Solutions** | **$13M** (LHA 8) | Coatings |
| **GE Energy Power Conversion USA** | **$12M** (LHA 9) | Auxiliary propulsion |
| **Engineered Coil** | **$11M** (LHA 9) | Firefighting watermist |
| **US Joiner** | **$8M** (LHA 8) | Interior outfitting |
| **The Hiller Companies** | **$9M** (LHA 9) | Firefighting |
| **Surface Technologies Corporation** | **$8M** (LHA 8) | Surface treatments |

---

## 4. LHA Replacement -- New Construction

**FY26 SAM:** SCN 3041 -- **$634,963K** for FY26.

**Sole-source to HII Ingalls Shipbuilding** (Pascagoula, MS).

### Prime Contracts (window deltas from per-mod pull)

| PIID | Hull | **Window Δ** | Cumulative | Ceiling | Description |
|---|---|---|---|---|---|
| **N0002420C2437** | **LHA 9** | **$3.15B** | $3.16B | $3.14B | Window-native: signed FY20, all $$ in window ✓ |
| **N0002416C2427** | **LHA 8 (Bougainville)** | **$1.01B** | $3.32B | $3.31B | FY16 award, only 31% in window |
| **N0002424C2467** | **LHA 10** (Advance Procurement) | **$322M** | $807M | $130M (per prior file) | FY24 AP award. **Note:** cumulative jumped from $306M to $807M on a Dec 2025 mod (option exercise — see note below) |

**True FY20-26 window spend across the 3 LHA PIIDs: ~$4.49B** (vs ~$5.96B
cumulative). Note that the LHA 10 line shows a $322M per-mod sum but the
cumulative reached $807M, indicating an option-exercise mod where the
`obligatedAmount` field undercounts the actual obligation. The "true" LHA
10 window obligation is somewhere between $322M (per-mod sum, conservative)
and $807M (latest cumulative, since the contract is fully window-native).

### Notable LHA 9 Subs (from HII LPD/LHA combined pull)

The LHA 9 prime (N0002420C2437) alone reports 446 subaward records totaling
$333.4M. Major suppliers overlap with the LPD program and are listed in
Section 3 above. LHA-specific notables:

| Subcontractor | Sub $ | Role |
|---|---|---|
| American Superconductor Corp | $48.9M | Likely degaussing system |
| Sheffield Forgemasters Engineering (UK) | $14.9M | Strut castings (large forgings sourced from UK) |
| GE Energy Power Conversion USA | $12.2M | Auxiliary propulsion system |
| Dynalec | $11.2M | Switchboard alarm systems |
| Aqua-Chem | $5.0M | Freshwater generation |
| Lister Chain & Forge | $4.5M | Detachable anchor chain links |

---

# B. SCHEDULED DEPOT MAINTENANCE & REPAIR

> **Note on visibility:** Surface combatant and amphibious depot maintenance
> is **competed among private regional shipyards** and is fully visible in
> FPDS. This is a **different visibility regime** than submarine and CVN
> depot work, which is performed by federal employees at the four public
> naval shipyards (Norfolk, Portsmouth, Pearl Harbor, Puget Sound) and is
> invisible in FPDS. For the hulls in this file, FPDS coverage of depot
> work is essentially complete.
>
> Each ship availability is its own contract with a separate PIID, signed
> over a 1-3 year execution window. Contracts are tagged [NEW] if signed
> 2020+ or [STR] if signed before 2020 with execution extending into the
> window.

## 5. DDG-51 Depot Maintenance

**FY26 SAM:** OMN_Vol2 DDG -- ~**$960M** combined (DDG: $525M + $427M;
DDG-1000: $6M + $2M).

### West Coast (San Diego)

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [STR/NEW] | **BAE Systems San Diego Ship Repair** | Multiple DSRAs/EDSRAs | DDG 60, 73, 86, 104, 105, 106, 111 | $25M-$119M per availability |
| [STR/NEW] | **NASSCO** | Multiple DSRAs | DDG 54, 86, 91, 106 | $21M-$124M per availability |
| [NEW] | **Continental Maritime of San Diego** | N0002423C4XXX | DDG 90 FY23 DMP | $237M ceiling |
| [STR/NEW] | **HII San Diego Shipyard** | Various | DDG maintenance | $19M-$57M per availability |
| [STR] | **Pacific Ship Repair & Fabrication** | -- | DDG 92 FY17 SRA | $124M ceiling (pre-window award) |

### Pacific Northwest

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [NEW] | **Vigor Marine LLC** | Various | DDG 100 FY25 DMP, DDG 102 DSRA | $46M-$320M per availability |

### East Coast (Norfolk)

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [STR/NEW] | **BAE Systems Norfolk Ship Repair** | Multiple DSRAs | DDG 55, 57, 71, 109 | $58M-$129M per availability |
| [STR] | **BAE Systems Jacksonville Ship Repair** | -- | DDG 81 EDSRA | $235M ceiling |
| [STR] | **Marine Hydraulics International** | -- | DDG 67 SRA | $280M ceiling |
| [STR/NEW] | **Metro Machine Corp** | -- | DDG 94, 96 | $25M-$87M per availability |

### Overseas (Forward-Deployed)

| Shipyard | Location | Ships |
|---|---|---|
| **Sumitomo Heavy Industries** | Yokosuka, Japan | FDNF DDGs |
| **Navantia SA** | Rota, Spain | DDG 117 |

> **Aggregation note:** BAE Systems holds DDG depot work across at least
> four sites (Norfolk, San Diego, Jacksonville, Hawaii). For parent-company
> rollups, BAE's combined surface-combatant depot footprint across all
> hulls (DDG, LHD, LSD, CG) exceeds **$5B** in window.

---

## 6. LHD Depot Maintenance

**FY26 SAM:** OMN_Vol2 LHD/AMPHIBS depot -- **$346,443K** combined for FY26.

### Prime Shipyards -- East Coast (Norfolk)

| Tag | Shipyard | Contract | Ship | Cumulative | Ceiling |
|---|---|---|---|---|---|
| [PRE] | **BAE Systems Norfolk Ship Repair** | N0002411C4407 | LHD 3 FY11 PMA | -- | $849M (pre-window award; mostly executed pre-2020) |
| [NEW] | **BAE Systems Norfolk Ship Repair** | N0002423C4408 | USS Kearsarge (LHD 3) FY23 DSRA | $325M | $348M |
| [NEW] | **BAE Systems Norfolk Ship Repair** | N0002426C4405 | USS Iwo Jima (LHD 7) FY26 SRA | $204M | $241M |
| [NEW] | **BAE Systems Norfolk Ship Repair** | N0002425C4430 | USS Wasp (LHD 1) FY25 SRA | $102M | $102M |
| [NEW] | **BAE Systems Norfolk Ship Repair** | N0002421C4404 | USS Wasp (LHD 1) FY21 DSRA | $241M | $241M |
| [NEW] | **Metro Machine Corp** | N0002424C4418 | USS Bataan (LHD 5) FY24 DSRA | $338M | $394M |
| [NEW] | **Metro Machine Corp** | N0002422C4490 | USS Iwo Jima (LHD 7) FY22 DSRA | $259M | $358M |
| [NEW] | **Metro Machine Corp** | N0002420C4467 | USS Bataan (LHD 5) FY20 SRA | $112M | $131M |

### Prime Shipyards -- West Coast (San Diego)

| Tag | Shipyard | Contract | Ship | Cumulative | Ceiling |
|---|---|---|---|---|---|
| [NEW] | **BAE Systems San Diego Ship Repair** | N0002422C4420 | USS Essex (LHD 2) FY22 DSRA | $174M | $239M |
| [NEW] | **BAE Systems San Diego Ship Repair** | N0002420C4308 | USS Boxer (LHD 4) DSRA | $203M | $204M |
| [NEW] | **NASSCO** | N0002423C4404 | USS Makin Island (LHD 8) FY23 SRA | $75M | $101M |
| [STR] | **NASSCO** | N0002418C4404 | USS Bonhomme Richard (LHD 6) DPMA | $221M | $221M |

### Top First-Tier Subcontractors -- LHD Depot Stack

Aggregated across **12 LHD maintenance prime PIIDs** = approximately **4,820
subaward records, ~$3.57B cumulative observed**.

> **Major finding:** The LHD depot "primes" (BAE Systems Norfolk/San Diego,
> Metro Machine, NASSCO) are themselves subcontracting massive amounts to a
> hidden second tier of regional ship-repair specialists. This sub-tier
> ecosystem is invisible in FPDS but visible in USAspending subawards.

| Subcontractor | Sub $ | Actions | Primes | Role |
|---|---|---|---|---|
| **Propulsion Controls Engineering (PCE)** | $942.3M | 144 | 3 | Ship repair sub-prime -- propulsion systems |
| **Earl Industries** | $932.5M | 134 | 1 | Now part of BAE Norfolk (BAE acquired Earl in 2014); sub records reflect intra-BAE work allocation. **For parent-company rollups, combine with BAE Norfolk.** |
| **Marine Hydraulics International** | $414.0M | 261 | 1 | Norfolk-area ship repair sub-prime |
| **TECNICO Corporation** | $229.7M | 207 | 7 | Multi-yard ship repair specialist |
| **IMIA** (International Marine & Industrial Applicators) | $178.8M | 106 | 9 | Coatings / paint specialist |
| **EMS Industrial** | $117.9M | 210 | 7 | Industrial services |
| **Bay Metals & Fabrication** | $88.3M | 98 | 6 | Metal fab |
| **Metro Machine** (as sub) | $67.1M | 50 | 1 | Cross-prime support |
| **Walashek Industrial & Marine** | $44.9M | 118 | 9 | West Coast ship repair |
| **Auxiliary Systems** | $32.6M | 109 | 7 | Auxiliary equipment |
| **East Coast Repair & Fabrication** | $31.0M | 81 | 4 | Norfolk yard |
| **Marcom Services** | $30.4M | 36 | 4 | Equipment rental |
| **JRF Ship Repairs** | $23.4M | 31 | 4 | Ship repair |
| **Art Craft Fabricators** | $21.3M | 76 | 6 | Fabrication |
| **AMP United** | $15.6M | 10 | 4 | Specialty repair |
| **International Flooring & Protective Coatings** | $15.1M | 17 | 3 | Coatings |
| **HL Welding** | $11.8M | 96 | 1 | Coded repair welding |
| **Generation Refrigeration** | $11.4M | 68 | 7 | HVAC/refrigeration |
| **US Joiner** | $10.7M | 13 | 3 | Joiner/outfitting |
| **Consolidated Marine Systems** | $10.0M | 31 | 5 | Marine systems |
| **HII San Diego Shipyard** (as sub) | $9.0M | 28 | 1 | Cross-yard support |

> **Hampton Roads industrial base implication:** PCE, Earl, MHI, TECNICO,
> IMIA, EMS, and Bay Metals together represent a >$2B/window ship-repair
> sub-tier that operates under the BAE/Metro/NASSCO prime umbrella.

---

## 7. LPD Depot Maintenance

**FY26 SAM:** OMN_Vol2 LPD depot -- **$149,595K** combined.

### Prime Shipyards

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [NEW] | **BAE Systems San Diego Ship Repair** | N0002425C4415 | USS Somerset (LPD 25) FY25 DSRA | $193M |
| [STR/NEW] | **BAE Systems Norfolk Ship Repair** | Various | LPD East Coast availabilities | Varies |

LPD depot maintenance is a smaller line that competes among the same
Hampton Roads / San Diego ship-repair primes as the LHD work. Sub-tier
visibility is captured in the Section 6 LHD subaward table (same vendor
ecosystem).

---

## 8. LSD Depot Maintenance

**FY26 SAM:** OMN_Vol2 LSD depot -- **$94,421K** combined ($73M + $21M).

### Prime Shipyards -- West Coast

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [NEW] | **NASSCO** | Various | USS Comstock (LSD 45) FY21 DSRA | $128M |
| [NEW] | **NASSCO** | Various | USS Harpers Ferry (LSD 49) FY20 DPMA | $118M |
| [NEW] | **NASSCO** | Various | USS Harpers Ferry (LSD 49) FY25 SRA | $67M |
| [STR/NEW] | **BAE Systems San Diego** | Various | LSD 45, 52 (multiple) | $42M-$386M per avail |

### Prime Shipyards -- East Coast

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [STR] | **BAE Systems Norfolk** | Various | USS Tortuga (LSD 46) FY18 EDSRA/MODPRD | $259M |
| [NEW] | **BAE Systems Norfolk** | Various | USS Carter Hall (LSD 50) FY24 DSRA | $92M |
| [NEW] | **Metro Machine Corp** | Various | USS Oak Hill (LSD 51) FY25 DSRA | $142M |
| [PRE] | **Metro Machine Corp** | Various | USS Carter Hall (LSD 50) FY14 EDPMA | $704M (pre-window) |
| [PRE] | **Metro Machine Corp** | Various | USS Oak Hill / USS Whidbey Island MSMO | $502M (pre-window) |
| [STR] | **Marine Hydraulics International** | Various | USS Gunston Hall (LSD 44) FY19 DSRA | $162M |

---

## 9. LHA Depot Maintenance

**FY26 SAM:** OMN_Vol2 LHA depot -- **$45,012K** combined ($29M + $16M).

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [NEW] | **NASSCO** | N0002425C4404 | USS America (LHA 6) FY26 DSRA | $198M |
| [STR/NEW] | **HII (Ingalls)** | Various | LHA engineering/mod support | Varies |

---

## 10. LCS Depot Maintenance

**FY26 SAM:** OMN_Vol2 LCS depot -- **$576,389K** combined ($346M + $231M).

### Platform Sustainment Primes

| Tag | Contractor | Parent | Role | Key Contract | Value |
|---|---|---|---|---|---|
| [STR/NEW] | **Lockheed Martin Corporation** | LM | Freedom Variant Design Agent / ISEA | N6339419F0043, N6339424C0003 | $33.6M + $69M ceiling |
| [STR] | **Textron Systems Corporation** | Textron | Independence Variant support | N0001923F2544 | $51M ceiling |
| [NEW] | **General Dynamics Mission Systems** | GD | Independence Variant ISEA | N6339424C0004 | $72M |

### LCS Freedom Variant -- Original Construction Vehicle

| Tag | PIID | Contractor | Cumulative | Ceiling | Notes |
|---|---|---|---|---|---|
| **[PRE]** | **N0002411C2300** | Lockheed Martin (prime of record) | -- | -- | "FY10 LCS Construction" -- pre-window award. **See data integrity flag at top of file regarding the $47.17B Marinette Marine subaward figure.** |

> **LCS Freedom team-build pattern:** Marinette Marine Corporation
> (Wisconsin yard, owned by Fincantieri) is the actual builder of every
> Freedom-variant LCS hull. Lockheed Martin acts as the systems integrator
> and prime of record. This is the LCS analog of the Virginia/Columbia
> EB/HII team-build pattern (Lessons §10).
>
> The previous version of `SAM_Program_Contract_Awards.md` reported a
> $47.17B Marinette subaward total under N0002411C2300. **That figure
> fails the >$5B sanity check** and is almost certainly inflated by
> cumulative-mod double-counting (the same pattern as the documented $39T
> CPI Satcom case in Lessons §7). The qualitative finding -- "Marinette
> is the actual builder, LM is integrator" -- remains valid; the dollar
> figure should not be cited.

### LCS Subaward Stack (Excluding Marinette Anomaly)

LCS / MCM mission-module subcontractor totals across all relevant primes.
Numbers below are from PIIDs other than the corrupted N0002411C2300 entry.

| Subcontractor | Sub $ | Actions | Role |
|---|---|---|---|
| **Teledyne Defense Electronics** | $928.0M | 50 | Sub to NG Knifefish/LCS contract |
| **Teledyne Brown Engineering** | $715.1M | 158 | Complex forming, machine shop |
| **General Dynamics Mission Systems** (as sub to NG) | $607.8M | 70 | LCS Independence combat systems |
| **Rolls-Royce Marine North America** | $267.7M | 62 | LCS waterjets / propulsion |
| **Trident Sensors Limited** | $233.4M | 3 | Sensors |
| **Gibbs & Cox** | $207.1M | 87 | Naval architecture |
| **Airbus US Space & Defense** | $156.0M | 36 | Wave guide flanges |
| **Sparton DeLeon Springs** | $144.7M | 20 | ASW sensors / sonobuoys |
| **Northrop Grumman Systems** (as sub) | $136.8M | 76 | LCS Fathometer install kits, NAVDDS |
| **Fairlead Integrated** | $133.0M | 35 | Major systems / subsystems |
| **Renk Aktiengesellschaft** (Germany) | $91.0M | 18 | LCS gearing |
| **Coltec Industries / Fairbanks Morse** (combined) | $59.6M | 9 | Diesel engines |
| **Arete Associates** | $56.8M | 43 | LCS sensors |
| **Nielsen Beaumont Marine** | $54.5M | 260 | Engineering services |
| **Meggitt Defense Systems** | $46.6M | 25 | Major subsystems |
| **Applied Physical Sciences Corp** | $28.0M | 8 | NRE engineering |
| **Ultra Electronics Ocean Systems** | $19.5M | 13 | Sub work to LCS contracts |
| **L3Harris Fuzing & Ordnance Systems** | $17.1M | 8 | Barracuda mine neutralizer ESAD |
| **Hensoldt** | $16.6M | 29 | LCS 23 onsite engineering |

> **Teledyne consolidation note:** "Teledyne Defense Electronics" and
> "Teledyne Brown Engineering" are both Teledyne Technologies divisions.
> Combined Teledyne LCS sub footprint is **~$1.64B** -- noting that this
> figure is itself drawn from the same NG Knifefish/LCS prime
> (N0002417C6311) that returned 908 records totaling $1.475B, so the
> Teledyne lines may be cumulative-mod artifacts as well. **Treat
> aggregate Teledyne figures with caution; verify against per-action
> dedup before citing.**

---

## 11. CG Ticonderoga Depot Maintenance

**FY26 SAM:** OMN_Vol2 CG depot -- **$115,501K** combined ($75M + $40M).

> **Note:** CG cruiser modernization (MODPRD) contracts tend to be very
> large due to the scope of upgrades. The class is in active drawdown;
> remaining hulls are receiving life-extension MODPRDs.

| Tag | Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|---|
| [PRE] | **BAE Systems Norfolk Ship Repair** | -- | USS Leyte Gulf (CG 55) | $663M (pre-window) |
| [STR] | **BAE Systems Norfolk Ship Repair** | -- | USS Gettysburg (CG 64) FY18 MODPRD | $183M |
| [STR] | **BAE Systems Norfolk Ship Repair** | -- | USS Vicksburg (CG 69) FY18 SSRA | $68M |
| [STR] | **BAE Systems Hawaii Shipyards** | -- | USS Lake Erie (CG 70) DSRA | $549M |
| [NEW] | **Vigor Marine LLC** | -- | USS Chosin (CG 65) / USS Cape St. George (CG 71) FY20 MODPRD | $426M |
| [STR] | **NASSCO** | -- | USS Cowpens (CG 63) FY18 MODPRD | $205M |
| [STR/NEW] | **NASSCO** | -- | USS Lake Erie (CG 70) SRA | $62M |
| [STR/NEW] | **HII** | -- | CG 47 Class Advanced Planning & Installation | $453M ceiling |

---

# C. MODERNIZATION & ALTERATION INSTALLATION

## 12. DDG Modernization -- Combat Systems & Subsystems

**FY26 SAM (combined):**
- OMN_Vol2 DDG modernization: **$1,282,612K**
- OPN_BA1 Line 5 DDG Mod: **$878,787K**

The DDG modernization budget aggregates several major weapons and combat
system upgrade programs. Each subsystem has its own multi-year contract
vehicle that dwarfs the annual budget line.

### 12.1 AN/SPY-6(V) Radar (AMDR) -- The Largest Single Subsystem

| PIID | Contractor | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002422C5500** | **Raytheon** | **$3.27B** | $3.27B | AN/SPY-6(V) hardware production. Window-native — fresh per-mod pull shows $3.27B FY20-26 obligation (the prior file's $1.71B figure was outdated; the contract has grown via FY24-25 mods to its current $3.27B size) |
| **N0002425C5501** | Raytheon | **$205M** | $5M | AN/SPY-6(V) Family of Radars design agent (FMS). Contract has SLIN splits — per-mod sum ($205M) is more accurate than the latest single-SLIN snapshot |
| **N0001424C1103** | -- | **$15M** | $15M | RASP enhanced radar signal processing |

**SPY-6 family FY20-26 window total: ~$3.49B** (Raytheon, sole prime).

**OTA development** (Other Transaction Awards via consortium):
- Advanced Technology International: AN/SPY-6 RF Head Prototype -- 2 contracts, ~$9.8M combined (2023)

> **AN/SPY-6 is the single largest DDG modernization component.** Raytheon's
> $3.27B production contract covers radar arrays for DDG-51 Flight III and
> backfit to earlier Flights. This one ceiling exceeds the entire FY2026
> DDG Mod budget line.

**Subaward Stack -- N0002422C5500 (SPY-6 Production)** -- v3 corrected dedup
(prime size $3.27B, in-window subs total **$1.21B**):

| Subcontractor | Sub $ (corrected) | Role |
|---|---|---|
| **General Dynamics Mission Systems** | **$359M** | Intra-corporate RF / signal processing |
| **CAES Systems** (Cobham Advanced Electronic Solutions) | **$170M** | Multi-function RF assemblies |
| **Northrop Grumman Systems** | $114M | RF subassemblies |
| **Golden Star Technology** | $62M | Computer hardware |
| **Anaren** | $57M | RF combiners |
| **Major Tool & Machine** | $39M | General structural assemblies |
| **TTM Printed Circuit Group** | $38M | Sensor terminal boards |
| **Ducommun LaBarge Technologies** | $22M | RF cable assemblies |
| **M.S.M. Industries** | $21M | Integrated electronic assemblies |
| **Optima Stantron** | $20M | Cabinet assemblies |
| **Honeywell** | $19M | Inertial reference |
| **Technology Dynamics** | $18M | Power supplies |

> **CORRECTION:** The previous file claimed CAES + Mercury combined
> exposure across SPY-6 + SEWIP Block 2 + SLQ-32(V)6 exceeded $5B. **The
> corrected dedup shows the real combined total is approximately $503M:**
>
> | PIID | CAES | Mercury |
> |---|---|---|
> | N0002422C5500 (SPY-6 Production) | $170M | (not in top 10) |
> | N0002416C5363 (SEWIP Block 2) | $110M | $85M |
> | N0002420C5503 (SLQ-32(V)6) | $95M | $43M |
> | **Combined** | **$375M** | **$128M** |
>
> CAES and Mercury are still meaningful RF subs, but at <$200M each per
> program — not the $800M+ figures the prior file showed. The "$5B+
> hidden RF backbone" narrative was based on cumulative-summed sub
> records that double-counted each subcontract at every action_date
> snapshot.

### 12.2 SEWIP -- Surface Electronic Warfare Improvement Program

Three blocks, three different primes. Window deltas from per-mod pull:

**Block 2 -- AN/SLQ-32(V)6 (Lockheed Martin):**

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002420C5503** | **$783M** | $783M | SLQ-32(V)6 production (w/o shelter). Window-native ✓ |
| **N0002416C5363** | **$5M** | $572M | SLQ-32(V)6 SEWIP Block 2 subsystems. **99% pre-window** — almost no FY20-26 obligation; the contract was effectively fully obligated by 2018 |
| **N0002409C5300** | **$0** | $0 | AN/SLQ-32X(V) Block 2 (FY09, fully pre-window) |

**Block 3 -- AN/SLQ-32(V)Y (Northrop Grumman):**

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002415C5319** | **$59M** | $189M | Pre-design SEWIP Block 3 (FY15 award, 31% in window) |
| **N0002422C5520** | **$80M** | $80M | SEWIP Block 3 design agent (window-native) |

**Block 1B3 (GD Mission Systems):**

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002414C5341** | **$0.5M** | $17M | SEWIP Block 1B3 LRIP (effectively pre-window) |
| **N0002416C5352** | **$0** | $57M | SEWIP Block 1B3 systems (fully pre-window) |

**Support:**
- SAIC (N0016418F3006) — $32M — SEWIP Blocks 2-4 engineering & program support
- Penn State (N0001423FM002) — $6M — SEWIP Block 3 transceiver affordability
- Stratascor (N0018922F0223) — $4M — SEWIP support services

**SEWIP family FY20-26 window total (per-mod sum across pulled PIIDs): ~$928M.**
The previous file's "$2B+ across all blocks" headline was largely cumulative
ceiling rather than window obligation. SLQ-32(V)6 production
(N0002420C5503) at $783M is the dominant active vehicle.

**Subaward stacks (v3 corrected dedup):**
- LM SEWIP Block 2 (N0002416C5363): the prior file claimed $2.85B; v3 dedup with cap-at-prime brings this to effectively **$0M of in-window subs** because the SEWIP Block 2 prime is 99% pre-window. The CAES/Mercury figures are real but reflect work delivered in window from pre-window funding.
- LM SLQ-32(V)6 (N0002420C5503): **$329M in-window** (vs prior $1.42B claimed). The contract is window-native; CAES at $95M and Mercury at $43M are real.
- NG SEWIP Block 3 + Block 1B3: minimal subaward visibility — NG/GDMS perform Block 3 work in-house.

### 12.3 SSDS -- Ship Self Defense System

| PIID | Contractor | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002419C5603** | **Lockheed Martin** | **$368M** | $405M | SSDS Combat System Engineering Agent (CSEA). 91% in window |
| **N0002414C5128** | Raytheon | **$9M** | $358M | SSDS PSEA FY14-17 follow-on. **97% pre-window** |
| N0016425F3001 | BAE Systems | -- | $66M | Aegis/SSDS engineering (not in per-mod pull) |
| N0002421F8029 | JHU APL | -- | $27M | SSDS integrated combat system (not in per-mod pull) |
| N0017820FD507 | Lockheed Martin | -- | $20M | SSDS equipment production (not in per-mod pull) |
| N0017819FD518 | Northrop Grumman | -- | $21M | SSDS production hardware (not in per-mod pull) |
| 0007 | Geonorth, LLC | -- | $48M ceiling | Aegis/SSDS LBTTS activation planning |

**SSDS family FY20-26 window total (pulled PIIDs): ~$378M** (LM CSEA dominates).

**Subaward Stacks:**
- LM SSDS CSEA (N0002419C5603): 898 records, $270.1M
  - Top sub: **Mission Solutions** ($149.5M, SSDS IFFSIM, RVP studies)
  - **PMAT** (Programs Mgmt Analytics & Technologies): $43.3M, in-service support
  - **Epsilon Systems Solutions**: included in batch
- Raytheon SSDS PSEA (N0002414C5128): 206 records, $71.2M

### 12.4 CEC -- Cooperative Engagement Capability

| PIID | Contractor | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002419C5200** | **Raytheon** | **$393M** | $417M | CEC design agent and engineering. 94% in window |
| **N0002425C5239** | Raytheon | **$161M** | $54M | CEC design agent follow-on (window-native; SLIN splits cause per-mod sum > snapshot cumulative) |
| **N0002413C5212** | Raytheon | **$0** (-$8M de-ob) | $380M | CEC (FY13 award, fully pre-window with minor de-obligations) |
| HQ085221C0002 | Lockheed Martin | -- | $15M | CEC/Army IAMD integration (MDA) — not in per-mod pull |
| N0001421C1012 | Leidos | -- | $12M | Decoupling CEC processor from data distribution — not in per-mod pull |

**CEC family FY20-26 window total (Raytheon, sole prime): ~$554M.** The
prior file's "$1B+ total CEC" figure was cumulative-since-award; only ~55%
of that is window obligation.

### 12.5 CIWS / Phalanx / SeaRAM / RAM (Raytheon)

> **MAJOR EXPANSION:** The new vehicle sweep surfaced **6 CIWS/RAM
> contracts the prior file completely missed**, totaling ~$1.87B in
> window obligation. The corrected total ecosystem is roughly **$1.99B**
> in FY20-26 window obligation, vs the previous file's "$920M+ total
> identified."

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002422C5400** | **$638M** | $638M | RAM GMRP MK 44 MOD 6 BLK 2B (window-native) ⭐ NEW |
| **N0002421C5406** | **$400M** | $73M | Block 1B BSL2 to BSL2 Class A Overhaul (per-mod sum exceeds snapshot — SLIN splits) ⭐ NEW |
| **N0002424C5406** | **$377M** | $377M | FY25 CIWS Production (window-native) ⭐ NEW |
| **N0038325FNE02** | **$165M** | $165M | Non-Recurring Demand #2 (window-native) ⭐ NEW |
| **N0002426C5403** | **$146M** | $146M | FY26 RAM GMRP MK 44 MOD 6 BLK 2B (just signed Dec 2025) ⭐ NEW |
| **N0038325F0NE1** | **$139M** | $139M | MK-99 PBL NRD Order #1 (window-native) ⭐ NEW |
| **N0002419C5406** | **$125M** | $59M | Block 1 BSL 0 to SeaRAM upgrade & conversion |
| **N0002418C5406** | **$0** (-$0.1M) | $220M | FY18 CIWS production. **100% pre-window** (-$0.1M de-obligation in window) |
| **N0002407C5437** | **$0** | $194M | Mk 15 Phalanx CIWS R&D (FY07, fully pre-window) |
| N0038319F0VP0 | -- | $185M | PBL support: CIWS, Land-Based Phalanx, SeaRAM, RAM (not in per-mod pull) |
| N0016418F3004 | -- | $15M | Technology Service Corp — CIWS engineering & ILS |

**CIWS/RAM/SeaRAM family FY20-26 window total: ~$1.99B** (Raytheon, sole
prime). The 6 newly-discovered ⭐ NEW contracts represent ~$1.87B that
the original keyword search completely missed. Lessons §4 round-3
dollar-floor backstop catches contracts that keyword searches don't.

**Subaward Stacks -- CIWS / RAM / SeaRAM family** (v3 corrected dedup):

| Prime PIID | In-window Subs (v3) | Top sub on this PIID |
|---|---|---|
| **N0002421C5406** (Block 1B BSL2 Class A Overhaul) | **$162M** | GD-OTS $15M, L3Harris Cincinnati Electronics $15M |
| **N0002422C5400** (RAM GMRP MK 44 MOD 6 BLK 2B) | **$151M** | RAM-System GmbH $98M (foreign partner), NG $26M, Haigh-Farr $10M |
| **N0002419C5406** (SeaRAM upgrade) | **$138M** | L3Harris Cincinnati Electronics $13M, Ducommun $7M, Lourdes Industries $7M |
| **N0002418C5406** (FY18 CIWS Production) | **$79M** | L3Harris Cincinnati Electronics $6M, Whelan Machine $5M, AST/ACME $3M |
| **N0038325F0NE1** (MK-99 PBL NRD #1) | **$19M** | CDP Fastener $4M, Microwave Engineering $2M |
| **N0002424C5406** (FY25 CIWS Production) | **$7M** | L3Harris Cincinnati Electronics $3M, GD-OTS $1M |

**Combined CIWS/RAM/SeaRAM in-window subs (v3): ~$556M** across 6 PIIDs.

Top parent companies cross-PIID:

| Parent | Combined CIWS/RAM Subs | Note |
|---|---|---|
| **RAM-System GmbH** (Germany) | $98M | Single foreign partner on RAM GMRP — RAM missile co-development |
| **L3Harris Cincinnati Electronics** | $39M | Pedestal / gimbal platforms across 5 CIWS PIIDs |
| **General Dynamics** (GD-OTS, GDMS) | $35M | Bolts/structural (OTS), computing (Mission Systems) |
| **Northrop Grumman** | $26M | RAM GMRP RF subassemblies |
| **Ducommun LaBarge Technologies** | $18M | RF cable assemblies / CCAs |
| **Lourdes Industries** | $15M | Hydraulic assemblies |
| **Whelan Machine & Tool** | $12M | Precision machining |
| **AST/ACME** | $12M | Test/assembly tooling |
| **Haaa Group International** | $10M | Adhesives/coatings |
| **Haigh-Farr** | $10M | Antennas |
| **Abaco Systems** | $9M | Embedded computing |

> **CORRECTION:** The previous file claimed CIWS subaward totals of
> $1.76B across 6,341 records, with top subs DRS Network & Imaging at
> $232.5M, L3 Technologies at $117M, and many at $30-90M each. **Those
> figures were inflated by ~3-4x by cumulative-snapshot duplication.**
> The corrected v3 totals are roughly **$556M total**, with no individual
> sub above $100M (RAM-System GmbH at $98M is the largest).

### 12.6 HELIOS -- High Energy Laser with Integrated Optical-dazzler and Surveillance

| PIID | Contractor | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002418C5392** | **Lockheed Martin Aculight** | **$93M** | $225M | Development + delivery of 2 test units + options for 14 production units. FY18 award, 41% in window. Period 2018-2027. |

> HELIOS is the Navy's primary shipboard HEL weapon. Installed on USS Preble
> (DDG 88) for at-sea testing. LM Aculight is sole prime.

**Subaward Stack -- HELIOS (N0002418C5392)** -- v3 corrected dedup (prime
size $225M, in-window subs total **$62M**):

| Subcontractor | Sub $ (corrected) | Role |
|---|---|---|
| **MZA Associates Corporation** | **$25M** | Beam control I&T — HELIOS beam director (Albuquerque, NM) |
| **L3 Technologies** | $22M | Application development, training, software |
| **SPD Technologies** | $4M | Servers, signal processing bellows |
| **Sea Box** | $2M | TITAN structure production |
| **Riggs Distler** | $1M | Equipment / labor |

> **CORRECTION:** The previous file claimed MZA at **$395M** and L3 at
> **$209M** on HELIOS, with total HELIOS subs at $683M. After v3 dedup
> (cap at prime size of $225M), real numbers are MZA $25M and L3 $22M.
> The original figures were inflated by USAspending cumulative-snapshot
> reporting. MZA is still meaningful as a HELIOS co-developer, but their
> in-window obligation is one tenth of what the prior file showed.

### 12.7 Aegis Modernization Kits

| Tag | PIID | Contractor | Cumulative | Description |
|---|---|---|---|---|
| [NEW] | N0002424F5302 | Raytheon | $42.3M | Aegis modernization kit |
| [NEW] | N0002421F5314 | Raytheon | $35.7M | Mk 99 Aegis modernization kits |
| [NEW] | N0002423F5301 | Raytheon | $23.5M | Aegis modernization kits |

### 12.8 Mk 41 VLS Overhaul

| Tag | Contractor | PIIDs | Combined Value | Role |
|---|---|---|---|---|
| [NEW] | **GDIT** | N5005424F1017, F1023, multiple DOs | ~$5M+ | VLS overhaul on individual DDGs |
| [NEW] | Texas Research Institute | N0002425CS061 | $1.4M | Ablative material repair for Mk 41 VLS |
| [STR] | Electric Boat (GD) | N6660420F0611 | $1.1M | VLS repair |

> Note: Mk 41 VLS original production was by Lockheed Martin. Current
> sustainment and overhaul work is fragmented across smaller contractors.

### 12.9 NIFC-CA -- Naval Integrated Fire Control - Counter Air

| Tag | PIID | Contractor | Value | Role |
|---|---|---|---|---|
| [STR] | N6339419F3000 | Systems Engineering Group | $25.5M | Engineering / logistics support |
| [STR] | N0002416C5210 | GD Mission Systems | $14.6M | CDD and NIFC-CA requirements |

---

## 13. LCS In-Service Modernization & Mission Modules

**FY26 SAM (combined):**
- OPN_BA1 Line 37 LCS In-Service Modernization: **$189,458K**
- OPN_BA1 Line 34 LCS MCM Mission Modules: **$91,372K**
- OPN_BA1 Line 33 LCS Common Mission Modules Equipment: **$38,880K**
- OPN_BA1 Line 36 LCS SUW Mission Modules: **$3,790K**

### 13.1 LCS In-Service Modernization -- Sustainment Primes

| Tag | Contractor | Role | Contract | Value |
|---|---|---|---|---|
| [STR] | **Lockheed Martin** | Freedom Variant design agent & sustainment | N6339419F0043 | $33.6M |
| [NEW] | **Lockheed Martin** | Freedom Variant Combat System ISEA | N6339424C0003 | $69M ceiling |
| [NEW] | **General Dynamics Mission Systems** | Independence Variant ISEA | N6339424C0004 | $72M |
| [STR] | **Textron Systems** | Independence Variant Pre/Post-Deploy Support | N0001923F2544 | $51M ceiling |
| [STR] | Booz Allen Hamilton | EH04 -- PEO LCS Professional Support | -- | $228M |
| [STR] | Serco-IPS Corporation | EH11 -- Program/Tech/Financial Support | -- | $190M |
| [NEW] | Lockheed Martin | LCS ITT-2A Lethality & Survivability Update | N6134023F0385 | $45.6M ceiling |
| [STR] | Innovative Professional Solutions | LCS Mission Module Engineering | HR11 | $21M ceiling |
| [STR] | L-3 Communications | Shipboard Terminals | N0042118F0255 | $8.9M |

### 13.2 MCM Mission Module Components

The LCS MCM Mission Module budget line funds procurement of multiple
independent systems. Each has its own prime and contract vehicle.

**UISS -- Unmanned Influence Sweep System**

| PIID | Prime | **Window Δ** | Cumulative | Ceiling |
|---|---|---|---|---|
| **N0002414C6322** | Textron Systems Corporation | **$242M** | $331M | $342M (FY14 award, 73% in window) |

UISS subaward stack: 118 records (~$26M cumulative). Top sub: Coltec
Industries / Fairbanks Morse (diesel propulsion).

**Knifefish -- Mine Countermeasures UUV (Block 1)**

| PIID | Prime | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N0002421C6304** | GD Mission Systems | **$82M** | $82M | Knifefish Block 1 LRIP (window-native) |
| **N0002417C6311** | Northrop Grumman | **$348M** | $493M | Knifefish System Container ECPs, Gun Mission Modules, etc. (FY17 award, 70% in window) |

**Subaward stacks (CORRECTED dedup):**

- GDMS Knifefish (N0002421C6304): 52 records, ~$19M cumulative observed
- NG Knifefish/LCS (N0002417C6311): **CORRECTED dedup shows 36 unique
  subs, $37M in-window total** (vs the prior file's $1.475B claim).
  After correct dedup, the previously-cited Teledyne $928M and Teledyne
  Brown $715M figures **disappear from this PIID** — they were artifacts
  of cumulative-style snapshot summing. The real top subs on this PIID
  in window are Fairlead Integrated ($17M), GD Mission Systems ($13M),
  Teledyne Brown Engineering ($4M).

> **Where the real Teledyne work lives:** Teledyne Defense Electronics
> at **$922M** (9 unique large component buys) is on the GDMS Surface MCM
> Unmanned PIID **N6133111C0017**, NOT on the NG Knifefish/LCS PIID.
> See SMCM section below.

**MCM USV -- Mine Countermeasures Unmanned Surface Vehicle**

| PIID | Prime | **Window Δ** | Cumulative | Ceiling |
|---|---|---|---|---|
| **N0002422C6305** | Bollinger Shipyards Lockport, LLC | **$116M** | $116M | $168M (window-native) |

> Subawards: 0 reported -- Bollinger does not report subawards in
> USAspending across any of its USCG or Navy contracts (Lessons §6).
> Known suppliers from public sources include MTU/Rolls-Royce diesel,
> Hamilton Jet waterjets, and regional Lockport-area fab.

**AN/AQS-20 Mine Hunting Sonar**
| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [NEW] | Raytheon | N6133125F0058 | $497K | Minehunting Payload Delivery System |
| [STR] | Raytheon | N6133119F0228 | $694K | AN/AQS-20C sonar enhancement |
| [STR] | Technical Systems Integration | HR18 | $5.1M | AQS-20 ISEA |

**AN/AQS-24C Volume Search Minehunting Sonar**
| Tag | Field | Detail |
|---|---|---|
| [STR] | Prime | **University of Texas at Austin (Applied Research Labs)** |
| | Contracts | 0921, 0922, 0931 |
| | Combined Value | ~$5.3M |

**Barracuda Mine Neutralizer**
| Tag | Field | Detail |
|---|---|---|
| [STR] | Prime | **Raytheon Company** |
| | Contract | N0002418C6300 |
| | Cumulative | $11.4M |
| | Ceiling | $149.4M |

Subaward stack (N0002418C6300): 173 records, $248M cumulative observed.

**Surface MCM Unmanned (SMCM)**

| PIID | Prime | **Window Δ** | Cumulative | Description |
|---|---|---|---|---|
| **N6133111C0017** | GD Mission Systems | **$15M** | $143M | FY11 award, period 2011-2022, **89% pre-window** |

**Subaward stack (CORRECTED dedup):** 84 unique subs, **$1.18B in-window
total** — and unlike the other "billion-dollar sub pile" cases, this one is
LEGIT after dedup. Top subs:

| Subcontractor | Sub $ (corrected) | Role |
|---|---|---|
| **Teledyne Defense Electronics** | **$922M** (9 subs) | Major component buys (probably sonar arrays / payload sensors) |
| **Trident Sensors Limited** | **$233M** (1 sub) | Single large sensor procurement |
| Ultra Electronics Ocean Systems | $9M (2 subs) | Sonar processing |
| Oceaneering International | $6M (3 subs) | Subsea systems |
| Metron Incorporated | $4M (3 subs) | Software |

> **Apparent prime/sub mismatch:** The prime contract reports only $15M of
> in-window obligation, but $1.18B of subaward delivery in window. Same
> pattern as the LCS Freedom case — the contract was awarded in FY11 with
> a $143M cumulative pre-window, and Teledyne/Trident have been executing
> the pre-window-funded scope ever since. The subaward total reflects
> work delivered, not new prime obligation.

**MCM Mission Package Integration**
| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [STR] | Avian LLC | N6133118F3010 | $26.6M | LCS MCM Package C2, MCM Systems, MH-60S integration, MVCS production |
| [STR] | Innovative Professional Solutions | N6133121F3008 | $19.3M | LCS mission module engineering |
| [STR] | Innovative Professional Solutions | HR11 | $21.1M | LCS mission module tech support |
| [NEW] | JHU APL | N0002423F8905 | $10.4M | LCS mission module systems |
| [STR] | JHU APL | N0002422F8020 | $3.0M | LCS mission module systems |
| [STR] | Solpac Construction | N6247319F5055 | $13.4M | LCS Mission Module Readiness Center construction |
| [NEW] | Applied Technical Systems | N6133122F3010 | $4.9M | LCS MVCS support |
| [NEW] | Innovative Professional Solutions | N6133126C0001 | $13.6M | Minesweeping winches (legacy) |

### 13.3 Common Mission Modules Equipment

Common mission module infrastructure shared across MCM, SUW, and ASW
packages. Contractors overlap with LCS platform primes (LM, GD).

### 13.4 SUW Mission Modules

| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [STR] | Bowhead Professional Solutions | N0017817F3007 | $7.2M | LCS SUW Engineering Support |

---

## 14. LHA/LHD Midlife & LPD/LSD Class Support

### 14.1 LHA/LHD Midlife (OPN BA1 Line 8)

**FY26 SAM:** **$123,384K**

| Tag | Contractor | Role | Source |
|---|---|---|---|
| [STR/NEW] | **BAE Systems Norfolk / San Diego** | Hull, mechanical, electrical midlife work | FPDS |
| [STR/NEW] | **Metro Machine Corp** | Midlife availability execution | FPDS |
| [STR] | **Gibbs & Cox** | Electric plant control system engineering | FPDS |
| [STR] | **Advanced Technology International** | LHD midlife electrical cabinet fabrication (OTA) | FPDS |
| [STR] | **Amee Bay, LLC** | LHD midlife AIT | FPDS |
| [STR] | Orbis Sibro | Ship modernization program oversight | $15.8M / $25M ceiling |
| [STR] | Valkyrie Enterprises | LHD 2 & LHD 7 modifications | $3.7M |

### 14.2 LPD Class Support Equipment (OPN BA1 Line 15)

**FY26 SAM:** **$125,542K**

| Tag | Contractor | Role | Value |
|---|---|---|---|
| [STR/NEW] | **Huntington Ingalls** | Class engineering and support services | $224.7M ceiling |
| [STR] | **Raytheon Company** | Life Cycle Engineering & Support (electronics) | $485M ceiling |

### 14.3 LSD Midlife & Modernization (OPN BA1 Line 40)

**FY26 SAM:** **$4,079K** (very small line; class is in drawdown)

See LSD depot section (#8) for shipyard contractors. The OPN BA1 Line 40
funds incremental modernization on remaining LSD hulls -- the overall LSD
class is approaching end of service life.

---

## 15. DDG-1000 Class Support Equipment

**FY26 SAM:** OPN_BA1 Line 16 -- **$115,267K**

See DDG-1000 section (#2) above. Key contractors:

| Tag | Contractor | Role | Value |
|---|---|---|---|
| [STR] | **Raytheon Company** | Mission Systems Equipment | $888M ceiling |
| [NEW] | **Bath Iron Works** | Planning Yard | $196M |
| [STR] | **General Dynamics Land Systems** | MK 46 MOD 2 Gun Weapon System | $76.6M |
| [STR] | **Microsoft Corporation** | Zumwalt Operating Environment (ZOE) | $9.4M |

---

# D. WEAPONS

## 16. Standard Missile (WPN 2234) + Standard Missile Mods (WPN 2356)

**FY26 SAM:**
- WPN 2234 Standard Missile: **$1,008,875K**
- WPN 2356 Standard Missiles Mods: **$32,127K**

**Sole-source production program -- Raytheon (RTX) -- SM-2, SM-3, SM-6 families.**

> **MAJOR EXPANSION:** The new vehicle sweep surfaced **7 newer Raytheon
> SM contracts** the prior file completely missed, totaling **~$5.56B** in
> FY20-26 window obligation. The corrected SM family window total is
> approximately **$5.73B**, vs the $0 effective window contribution of
> the original 6 PIIDs (which were all pre-window).

### Prime Contracts -- New Contracts (window-native, sweep-discovered)

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002424C5408** | **$1.38B** | $1.38B | GMA (MK25) Option Exercise + TE ⭐ NEW |
| **N0002420C5405** | **$1.15B** | $1.42B | SM Increase Production Capacity (IPC) ⭐ NEW |
| **N0002424C6104** | **$765M** | $769M | SM Production Lot #2 ⭐ NEW |
| **N0002421C5411** | **$719M** | $719M | SM-2 BLK IIIB TAC AUR ⭐ NEW |
| **N0002425C5409** | **$573M** | $573M | FY25 SM-6 BLK IA TAC AUR ⭐ NEW |
| **N0002418C5432** | **$495M** | $554M | Encanistered Missile (EM) ⭐ NEW (FY18 award, 89% in window) |
| **N0002423C5408** | **$484M** | $479M | SM-2 DLMF Maintenance Spares PIO ⭐ NEW |

### Prime Contracts -- Older PIIDs (mostly pre-window leakage)

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002417C5410** | **$138M** | $292M | FY17-21 SM Production (47% in window — closeout mods) |
| **N0002418C5407** | **$25M** | $28M | Standard Missile DLMF/ILM (89% in window) |
| **N0002407C6119** | **$0** | $1.90B | Standard Missile 3 (FY07 award, fully pre-window) |
| **N0002413C5403** | **$0** | $276M | FY13-17 SM Production (fully pre-window) |
| **N0002402C5319** | **$0** | $227M | Standard Missile (FY02, fully pre-window) |
| **N0002400C5390** | **$0** | $211M | Standard Missile (FY00, fully pre-window) |

**Standard Missile family FY20-26 window total: ~$5.73B.** Raytheon is
sole prime. The seven sweep-discovered contracts represent the bulk of
real window obligation; the original keyword search caught only
pre-window/closeout PIIDs that contributed effectively zero new money.

### Key Support

| Tag | Contractor | Role | Value |
|---|---|---|---|
| [STR/NEW] | JHU Applied Physics Lab | Engineering & Evaluation | ~$29M total |
| [STR] | Millennium Engineering & Integration | Aegis BMD / SM Technical Support | $30M ceiling |

### Top Subcontractors -- Standard Missile Stack (v3 corrected)

Across all 13 SM PIIDs (7 sweep-discovered + 6 original) after v3 dedup.
**Total in-window SM subs: ~$930M.**

| Subcontractor | Sub $ (corrected, cross-PIID) | Role |
|---|---|---|
| **L3Harris (Aerojet Rocketdyne)** | **$378M** | Solid rocket motors (SM-2, SM-3, SM-6) — post-2023 L3Harris acquisition |
| **Honeywell International** | **$43M** | IMUs / IRUs (inertial guidance) |
| **Goodrich Actuation Systems** | **$32M** | Control actuators |
| **Magellan Aerospace, Middletown** | **$28M** | Missile components |
| **CAES (Cobham Advanced Electronic Solutions)** | **$26M** | RF/electronics |
| **Empirical Systems Aerospace** | **$26M** | Engineering services |
| **Nammo Raufoss AS** (Norway) | **$21M** | Solid rocket components (foreign supplier) |
| **General Dynamics** (combined) | **$20M** | Various |
| **Samuel, Son & Co. (USA)** | **$15M** | Metals |
| **Haas Group International** | **$15M** | Adhesives/coatings |
| **EaglePicher Technologies** | **$14M** | Thermal batteries |
| **Emhiser Research** | **$14M** | RF/test |

> **Aerojet Rocketdyne (now L3Harris)** is the dominant SM sub-prime at
> ~$378M across 4-5 production contracts — this is the SM solid rocket
> motor supply chain. The 2023 L3Harris acquisition of Aerojet Rocketdyne
> consolidated this work under one parent. Combined with L3Harris's
> Cincinnati Electronics work on CIWS, L3Harris has ~$580M of in-window
> sub work across the in-scope Raytheon weapons family.

> **The CAES exposure on Standard Missile is small ($26M).** CAES is
> primarily a SPY-6/SEWIP RF supplier; SM is not a major program for them.

---

## 17. MK-54 Torpedo Mods (WPN 3215)

**FY26 SAM:** **$128,513K**

### Prime Contractors

| PIID | Contractor | **Window Δ** | Cumulative | Ceiling | Role |
|---|---|---|---|---|---|
| **N0002425C6401** | **General Dynamics Mission Systems** | **$115M** | $115M | **$791.9M** | MK 54 MOD 1 LWT Sonar Assembly Kits. Window-native, FY25 award |
| **N0002418C6405** | Ultra Electronics Ocean Systems | **$68M** | $156M | $324.1M | MK 54 MOD 0 Array Kits (43% in window) |

### MK 54 MOD 2 Development (OTA via Advanced Technology International consortium)

| Tag | PIID | Cumulative | Ceiling | Role |
|---|---|---|---|---|
| [NEW] | N666042090101 | $73M | $76.9M | MOD 2 Warhead Section Development |
| [NEW] | N666042090119 | $134.2M | $134.4M | MOD 2 AUR Development |
| [NEW] | N666042594201 | $27.9M | $256.1M | MOD 2 Inc 1 AUR Proof of Manufacturing |

### Key Support

| Tag | Contractor | Role | Value |
|---|---|---|---|
| [STR/NEW] | Penn State Applied Research Lab | MOD 2 System Engineering & Testing | $36M + $29M ceiling |
| [STR] | Lockheed Martin | MK-54 Capability | $2.6M |
| [STR] | McLaughlin Research Corp | MK 32 / MK 54 Torpedo Tube Engineering | $23.5M ceiling |

> The GD Mission Systems MK 54 MOD 1 LWT Sonar Assembly prime
> (N0002425C6401) reports only 2 subawards totaling $25M -- almost all
> production work is held in-house at GDMS. Ultra Electronics MK 54 MOD 0
> Array Kits (N0002418C6405) reports 26 subawards totaling $12.1M.

---

## 18. Naval Strike Missile (WPN 2292) + LCS Module Weapons (WPN 4221)

**FY26 SAM:**
- WPN 2292 Naval Strike Missile: **$32,238K**
- WPN 4221 LCS Module Weapons: **$2,200K**

### Prime Contractors

| Tag | Contractor | Parent | Role | Contract | Value |
|---|---|---|---|---|---|
| [NEW] | **Raytheon Company** | RTX Corp | U.S. production integration prime | M6785422F1001 | $43.7M ceiling |
| -- | **Kongsberg Defence & Aerospace** | Kongsberg | OEM / designer (Norwegian) | -- | (FMS channel; limited FPDS visibility) |

> Note: Kongsberg is the original equipment manufacturer of the NSM.
> Raytheon handles U.S. integration and production. The $32M FY2026 budget
> covers procurement of NSM Launch Units and Weapons Control Systems for
> LCS. The Norwegian-side OEM work is invisible in FPDS.

LCS Module Weapons (WPN 4221) is a small procurement line at $2.2M
covering integration of weapons into LCS mission packages. Limited FPDS
visibility at this funding level.

---

## 19. Surface Ship Torpedo Defense -- SSTD (OPN BA2 2213)

**FY26 SAM:** **$14,915K**

### Prime Contractors

| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [STR] | **SAIC** | N6660418F3013 | $31.3M | AN/SLQ-25D Nixie towed torpedo countermeasure system engineering |
| [STR] | **SAIC** | N425 | $7.6M | Anti-torpedo torpedo defense system, Mk 2/3/4 countermeasures |
| [STR] | **Penn State University** | 0074 | $46.9M | CCAT (Canistered Countermeasure Anti-Torpedo Torpedo) development |
| [STR] | Penn State | 0492 | $3.0M | Full Sector Torpedo Defense -- ATT timeline compression |
| [STR] | ManTech | 7N01 | $1.7M | Advanced torpedo defense system engineering |
| [STR] | Applied Management Corp | 7N03 | $1.5M | SSTD support |

### Known First-Tier Subs (under SAIC)

| Subcontractor | Amount | Role |
|---|---|---|
| **RTX BBN Technologies** | ~$9.2M | AN/SLQ-25D Nixie engineering support |
| **Cardinal Engineering, LLC** | ~$4.9M | SSTD Nixie UW/UDF Family of Systems |

### AN/SLQ-25E Nixie Production (related)

| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [STR] | Ultra Electronics Ocean Systems | N0025321F0037 | $16.0M | Production of Nixie AN/SLQ-25E systems |
| [STR] | GDIT | N440 | $46.9M | SLQ-25 design, assembly, integration, testing |
| [STR] | Ultra Electronics Ocean Systems | N0025322F0167 | $231K | Nixie domestic spares |

---

## 20. Ship Gun Systems Equipment (OPN BA4 5111)

**FY26 SAM:** **$7,358K**

### Prime Contractor

**BAE Systems Land & Armaments, L.P.** -- sole producer of MK 110 MOD 0
(57mm) Naval Gun.

### Key Contracts

| PIID | **Window Δ** | Cumulative | Description |
|---|---|---|---|
| **N0002417C5375** | **$0** | $56M | 57MM MK 110 MOD 0 Gun Mount production (fully pre-window) |
| **N0002412C5316** | **$0** (-$0.5M) | $50M | MK 110 Naval Gun Procurement (USCG NSC) (fully pre-window) |
| **N0002418F5302** | **$0** (-$0.4M) | $8M | MK 110 MOD 0 GWS Engineering Services (fully pre-window) |

> **Ship Gun Systems Equipment FY20-26 window total: ~$0** for the listed
> BAE MK 110 PIIDs. The line is small ($7M FY26) and BAE's MK 110 production
> has been operating off pre-2020 obligations. New mods may exist that
> weren't in the original keyword pull.

### Mk 46 / 30mm Gun Weapon Systems

| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [STR] | **General Dynamics Land Systems** | N0002422F5306 | $9.6M | Mk 46 GWS support |
| [NEW] | **Raytheon** | N0002423C5316 | $8.6M | Mk 46 GWS HIRE II parts |
| [STR] | **General Dynamics Land Systems** | N0002415C5344 | $76.6M | Mk 46 MOD 2 GWS for DDG-1000 |

### 30mm Guns (MK44 MOD 4 / MK44S Stretch)

| Tag | Contractor | Contract | Value | Description |
|---|---|---|---|---|
| [NEW] | Northrop Grumman | N0016425FJ654 | $32.6M | MK44 MOD 4, 30mm guns w/ spares |
| [NEW] | Northrop Grumman | N0016424CJ001 | $8.4M | MK44S Stretch 30mm gun |
| [STR] | Alliant Techsystems | N0016422FJ124 | $7.1M | 30mm guns, spares, tools |
| [NEW] | Northrop Grumman | N0016424FJ012 | $6.6M | 30mm guns and associated spares |

---

## 21. Airborne MCM (OPN BA3 119)

**FY26 SAM:** **$9,643K**

The Airborne MCM line funds the AN/AES-1 Airborne Laser Mine Detection
System (ALMDS) and AN/ASQ-235 Airborne Mine Neutralization System (AMNS),
both deployed from MH-60S helicopters off LCS.

### ALMDS -- AN/AES-1 (Northrop Grumman)

| PIID | **Window Δ** | Cumulative | Ceiling | Description |
|---|---|---|---|---|
| **N0002415C6318** | **$13M** | $177M | $517M | ALMDS production main contract (FY15 award, 8% in window) |
| **N0002422C6418** | **$60M** | $60M | $107M | ALMDS production support (window-native) |

**ALMDS FY20-26 window total: ~$74M.** The bulk of the $624M ceiling is
pre-window obligation and unexercised options.

Subaward stacks:
- N0002415C6318 (production): 74 records, $91.3M
- N0002422C6418 (support): 38 records, $6.8M

ALMDS subs likely include laser sources, optical components, and pod
hardware. NG performs much of the work in-house.

### AMNS -- AN/ASQ-235 (Raytheon)

| PIID | **Window Δ** | Cumulative | Ceiling | Description |
|---|---|---|---|---|
| **N0002417C6305** | **$27M** | $51M | $64M | AMNS LRIP (FY17 award) |
| **N0002421F6412** | **$8M** | $8M | $17M | AMNS Test & Depot Support (window-native) |
| **N0002425F6404** | **$2M** | $2M | $19M | AMNS Test & Depot Support (window-native) |
| **N0002403C6310** | **$0** | $103M | -- | AMNS Upgrade (-3) (FY03, fully pre-window) |
| **N0002410C6307** | **$0** | $58M | $72M | AMNS LRIP (FY09, fully pre-window) |

**AMNS FY20-26 window total: ~$37M.** Same pattern — most "$170M+" headline
value is pre-window. The line item is small ($10M FY26).

Subaward stacks:
- N0002417C6305 (newer LRIP): 280 records, $117.9M
- Older AMNS contracts: 0 subs (pre-window, predates FFATA reporting)

### Other Airborne MCM

| Tag | Contractor | Contract | Value | Role |
|---|---|---|---|---|
| [STR] | Booz Allen Hamilton | HR02 | $9.8M | OAMCM systems engineering |
| [STR] | Booz Allen Hamilton | N6133122F3011 | $23.4M | ALMDS, AMNS, Barracuda, MIW eng & log |
| [STR] | Avian LLC | N6133118F3000 | $10.1M | Airborne MCM Performance Support System |
| [PRE] | QinetiQ | N6133107C0034 | $3.4M | RAMICS integration & live firing (pre-window) |
| [STR] | RE2 LLC | N0001421C2030 | $7.2M | Maritime Mine Neutralization System (M2NS, next-gen) |

---

# E. CROSS-CUTTING

## 22. Summary -- Top Primes & Hidden Subs

### Top Prime Contractors (by **TRUE FY20-26 window obligation**, per per-mod sum)

These figures are window deltas computed from per-mod `obligatedAmount`
sums, NOT cumulative-since-contract-award. They represent real new
obligation activity inside the FY20-26 window across the in-scope PIIDs
pulled in this analysis. Depot maintenance contracts (per-availability
PIIDs) are included as approximations from prior file totals — those are
mostly window-native.

| Rank | Contractor | Parent | Window Δ (in scope) | Notes |
|---|---|---|---|---|
| 1 | **Huntington Ingalls Industries** | HII | **~$22B** | DDG-51 (HII): $11.36B from N0002423C2307 + N0002418C2307 + N0002413C2307 + small. LPD: $4.68B. LHA: $4.49B. DDG-1000: $0.31B mod planning. Plus depot. |
| 2 | **Bath Iron Works** | General Dynamics | **~$8.8B** | DDG-51 (BIW): $5.03B (FY23-27) + $3.31B (FY18-22) + $0.48B (FY13-17) + lead yard. DDG-1000: $0.20B closeout. |
| 3 | **Raytheon Company / RTX** | RTX Corp | **~$13.7B** | Standard Missile family **$5.73B** (mostly the 7 sweep-discovered contracts), SPY-6 family $3.49B, CIWS/RAM family $1.99B, DDG-1000 mission systems $0.85B, CEC $0.55B, Aegis mod kits + AMNS + Barracuda + Encanistered Missile + others. **Now the #1 prime by window obligation across in-scope programs.** |
| 4 | **Lockheed Martin** (incl. LM Aculight) | LM | **~$1.5B** | LM SLQ-32(V)6 production $0.78B, SSDS CSEA $0.37B, HELIOS $0.09B, LCS Freedom $0.25B, plus older Aegis pre-window ($0). |
| 5 | **BAE Systems** (multiple divisions) | BAE Systems plc | **~$5B** (depot estimate) | DDG/LHD/LPD/LSD/CG depot maintenance across Norfolk, San Diego, Jacksonville, Hawaii. Window-native availabilities. |
| 6 | **Metro Machine Corp** | -- | **~$700M+** | LHD/DDG/LSD depot maintenance (Norfolk). |
| 7 | **NASSCO** | GD | **~$600M+** | LHA/LHD/LSD/DDG/CG depot maintenance (San Diego). |
| 8 | **Vigor Marine LLC** | -- | **~$500M** | DDG/CG depot maintenance (Portland, OR). |
| 9 | **Northrop Grumman Systems** | NG | **~$487M** | NG Knifefish/LCS $0.35B, SEWIP Block 3 $0.14B, ALMDS $0.07B. |
| 10 | **Textron Systems** | Textron | **$242M** | UISS $0.24B (window portion of N0002414C6322). |
| 11 | **General Dynamics Mission Systems** | GD | **~$210M** | MK-54 MOD 1 $0.12B, Knifefish Block 1 $0.08B. SMCM Unmanned was 89% pre-window. Plus LCS Independence ISEA. |
| 12 | **Bollinger Shipyards Lockport** | Bollinger | **$116M** | MCM USV production (window-native). |
| 13 | **Continental Maritime of San Diego** | -- | **~$300M** | DDG depot. |
| 14 | **Marine Hydraulics International** | -- | **~$200M+** | DDG/LSD depot + sub-prime work on LHD primes. |
| 15 | **QED Systems** | -- | **~$300M** | Third-party planning DDG/CG/LPD/LHD. |
| 16 | **SAIC** | SAIC | **~$200M** | DDG-1000 engineering, SSTD Nixie, torpedo defense. |
| 17 | **Penn State Applied Research Lab** | Penn State Univ | **~$60M** | MK-54 MOD 2 engineering, HEL development, CCAT. |
| 18 | **Ultra Electronics Ocean Systems** | Ultra | **$68M** | MK 54 MOD 0 array kits ($68M window) + Nixie production. |
| 19 | **Advanced Technology International** | -- (consortium) | **~$235M** | OTA consortium manager: MK-54 MOD 2 OTAs ($235M total across 3 OTA contracts), SPY-6 RF Head Prototype, HEL, LHD midlife. |
| 20 | **BAE Systems Land & Armaments** | BAE | **$0** (window) | MK 110 57mm gun production has been operating off pre-2020 obligations across the 3 listed PIIDs. New contracts may exist outside the keyword pull. |

### Top Hidden Subcontractors -- FRESH CROSS-PIID PULL (corrected v3 dedup)

**Methodology:** All 170 in-scope PIIDs (82 from per-mod construction/
modernization/weapons pull + 88 from depot maintenance vendor sweeps)
were re-pulled from USAspending `/api/v2/subawards/`. Three-stage dedup:

1. **Stage 1 (per `sub_id` MAX):** USAspending issues multiple snapshot
   records for the same `subaward_number` at different `action_date`s,
   each reporting cumulative-style amounts. Take the MAX per unique
   `sub_id`.
2. **Stage 2 (collapse identical-amount duplicates):** USAspending also
   issues separate `subaward_number`s for the same underlying subcontract
   when the prime gets a new mod. Per (recipient, prime_piid, amount),
   keep only one record.
3. **Stage 3 (cap + exclude at prime size):** Per (recipient, prime),
   cap the total at 1.0× the prime contract value (a sub cannot exceed
   its prime). Exclude entirely any pair > 2× prime (clear corruption,
   like the NASSCO USS Cowpens MODPRD where 5 unrelated recipients each
   reported the exact same phantom $920M).

**Cross-PIID totals after v3 dedup:** Grand total in-window subawards
across 170 PIIDs is **~$10.35B** (vs prior file totals that summed to
$80B+ across the same primes).

### Top Parent Companies by FY20-26 In-Window Sub Total

| Rank | Parent Company | Sub Total (window, capped) | Pairs | Distinct PIIDs | Primary Programs |
|---|---|---|---|---|---|
| 1 | **Fincantieri (Marinette Marine)** | **$2,487M** | 2 | 1 | Single LCS Freedom (LM) prime — actual hull builder; the corrected figure validates the team-build pattern |
| 2 | **Timken Gears & Services** | $516M ⚠️ | 22 | 20 | DDG/LHD/CG propulsion gearing. **Capped — Vigor CG-71 PIID had a $830M raw value capped to the prime's $447M; remaining $176M is real cross-program work** |
| 3 | **General Dynamics** (rolled up) | **$432M** | 23 | 14 | GD Mission Systems (largest contributor at $359M as sub on SPY-6), GD-OTS, GDIT, GDLS |
| 4 | **L3Harris (Aerojet Rocketdyne)** | **$378M** | 4 | 4 | Solid rocket motors for Standard Missile family (post-2023 L3Harris acquisition of Aerojet) |
| 5 | **Rolls-Royce** (combined) | **$313M** | 25 | 25 | Marine gas turbines, waterjets, gearing across DDG/LCS/LPD/LHA + mtu diesels (depot) |
| 6 | **CAES (Cobham Advanced Electronic Solutions)** | **$217M** | 10 | 8 | RF assemblies on SPY-6 ($170M), SEWIP Block 2 ($110M), SLQ-32(V)6 ($95M) — verified after dedup, vs prior $800M+ claim |
| 7 | **Northrop Grumman** (as sub) | **$215M** | 10 | 9 | SPY-6 RF subassemblies ($114M), CIWS, LPD/LHA construction |
| 8 | **Trident Sensors Limited** | $215M ⚠️ | 1 | 1 | Single large sensor procurement on GDMS Surface MCM Unmanned. **Capped — raw $233M on $143M prime** |
| 9 | **IMIA** (Int'l Marine & Industrial Applicators) | **$204M** | 28 | 28 | Hull coatings / paint specialist across 28 depot availabilities |
| 10 | **L3Harris** (excluding Aerojet) | **$203M** | 53 | 45 | Maritime Power & Energy Solutions, Cincinnati Electronics, Fuzing & Ordnance Systems — broadest cross-program footprint (45 distinct PIIDs) |
| 11 | **Johnson Controls** (incl. York) | **$172M** | 31 | 24 | HVAC / chilled water plants on DDG / LPD / LHA + depot |
| 12 | **GE Aerospace** | **$166M** | 16 | 14 | LM2500 gas turbines on DDG-51 + GE Energy Power Conversion on LHA 9 |
| 13 | **Fairbanks Morse Defense** (Coltec) | **$161M** | 25 | 18 | Diesel generator sets / propulsion on LPD/LHA + depot diesel rebuilds |
| 14 | **Leonardo DRS** | **$134M** | 18 | 15 | Naval Power Systems (switchboards), Network & Imaging Systems, Laurel Technologies |
| 15 | **Sparton DeLeon Springs** | **$108M** | 2 | 2 | ASW sensors / payload on Raytheon Barracuda mine neutralizer |
| 16 | **RAM-System GmbH** (Germany) | **$98M** | 1 | 1 | RAM missile system co-development with Raytheon (foreign partner) |
| 17 | **Bay Metals & Fabrication** | **$93M** | 9 | 9 | Norfolk-area metal fab serving 9 depot availabilities |
| 18 | **US Joiner LLC** | **$88M** | 12 | 12 | Interior outfitting / joiner work — LPD construction + depot |
| 19 | **United Rentals** | **$77M** | 29 | 29 | Equipment rental serving 29 depot availabilities |
| 20 | **Honeywell** | **$71M** | 12 | 12 | IMUs / IRUs (inertial guidance) on Standard Missile + CIWS |
| 21 | **Anaren** | **$64M** | 7 | 7 | RF combiners/dividers on SPY-6 ($57M dominates) |
| 22 | **Golden Star Technology** | **$63M** | 3 | 3 | Computer hardware on SPY-6 |
| 23 | **Red River Technology** | **$61M** | 2 | 2 | DDG-1000 mission system computing |
| 24 | **Nammo Raufoss AS** (Norway) | **$59M** | 1 | 1 | Solid rocket components for Standard Missile (foreign supplier) |
| 25 | **Ducommun LaBarge Technologies** | **$58M** | 14 | 11 | RF cable assemblies / CCAs on CIWS + Standard Missile + SPY-6 |
| 26 | **Southcoast Welding & Manufacturing** | **$57M** | 17 | 17 | Welding services on DDG-51 construction + depot |
| 27 | **Airbus US Space & Defense** | **$56M** | 1 | 1 | Wave guide flanges on LCS Freedom (Marinette pass-through) |
| 28 | **Teledyne** (rolled up) | **$55M** | 20 | 12 | Defense Electronics + Brown Engineering. **The prior file's claim of $928M Teledyne Defense Electronics on NG Knifefish was wrong — that figure was on GDMS SMCM Unmanned (N6133111C0017) and is capped at the $143M prime.** Real Teledyne in-window total across all in-scope primes is ~$55M after corrections. |
| 29 | **TECNICO Corporation** | **$55M** | 12 | 12 | Hampton Roads ship repair sub-prime — multi-yard |
| 30 | **Industrial Corrosion Control** | **$55M** | 6 | 6 | Tank coating / paint on LPD/LHA construction |
| 31 | **AMP United** | **$50M** | 14 | 14 | Specialty repair across 14 depot availabilities |
| 32 | **Engineered Coil** | **$47M** | 14 | 14 | Coiled components / heat exchangers on DDG/LPD/LHA |
| 33 | **Ellwood National Forge** | **$43M** | 4 | 4 | Propulsion shafts / forgings on DDG-51 |
| 34 | **TTM Printed Circuit Group** | **$41M** | 3 | 3 | Sensor terminal boards on SPY-6 |
| 35 | **Lake Shore Systems** | **$41M** | 22 | 22 | Capstans / deck machinery on DDG/LPD/LHA + depot |
| 36 | **Walashek Industrial & Marine** | **$41M** | 7 | 7 | West Coast ship repair (BAE San Diego ecosystem) |
| 37 | **EMS Industrial** | **$40M** | 8 | 8 | Industrial services across LHD depot |
| 38 | **Major Tool & Machine** | **$39M** | 1 | 1 | General structural assemblies on SPY-6 |
| 39 | **East Coast Repair & Fabrication** | **$36M** | 9 | 9 | Norfolk yard sub-tier on BAE/Metro/MHI primes |
| 40 | **Marcom Services** | **$35M** | 7 | 7 | Equipment rental on Hampton Roads depot |
| 41 | **JRF Ship Repairs** | **$34M** | 8 | 8 | Norfolk ship repair sub-tier |
| 42 | **Renk Aktiengesellschaft** (Germany) | **$34M** | 1 | 1 | LCS Freedom gearing (Marinette pass-through) |
| 43 | **Goodrich Actuation Systems** | **$32M** | 1 | 1 | Standard Missile actuators (single contract) |
| 44 | **Caterpillar** | **$31M** | 3 | 3 | LPD diesel engines |
| 45 | **Propulsion Controls Engineering (PCE)** | **$30M** | 19 | 19 | **CORRECTION:** Prior file claimed $942M for PCE across LHD depot. After v3 dedup (cap at prime size, exclude > 2x), real total is $30M across 19 depot availabilities. The prior figure was inflated by USAspending cumulative-snapshot artifacts. |
| 46 | **MZA Associates** | **$25M** | 1 | 1 | HELIOS beam control I&T (LM Aculight prime). **Prior file claimed $395M; real figure is $25M after dedup.** |

⚠️ flagged entries hit the per-pair sanity cap (raw amount exceeded
1.0× prime contract size; capped at the prime value). These are still
elevated but plausible — typically driven by a single large component
buy that USAspending's snapshot reporting inflates.

### Per-Program Subaward Rollups (window deltas, v3 dedup)

| Program Section | Total Subs (in window) | Top 3 Subs by Amount |
|---|---|---|
| **DDG-51 New Construction** | **$0.53B** | GE Aerospace $88M, Johnson Controls $76M, Timken Gears $41M |
| **DDG Mod - SPY-6** | **$1.22B** | GD Mission Systems $359M (intra-corp), CAES $170M, NG $114M |
| **DDG Mod - CIWS/RAM/SeaRAM** | **$0.56B** | RAM-System GmbH $98M, L3Harris $39M, GD $35M |
| **LCS Freedom (legacy construction)** | **$2.91B** | Marinette Marine $2,487M, Rolls-Royce $196M, Airbus US $56M |
| **LCS MCM Mission Modules** | **$1.23B** | Teledyne (Brown Eng) capped, Trident Sensors $215M (capped), GD $13M |
| **LHA Replacement New Construction** | **$0.34B** | L3Harris Maritime P&E $39M, Fairbanks Morse $40M, Leonardo DRS $34M |
| **LPD Flight II New Construction** | **$0.34B** | Fairbanks Morse $65M, US Joiner $36M, Caterpillar $20M |
| **DDG Mod - CEC** | **$0.03B** | Sechan Electronics $7M, Action Electronics $5M |
| **DDG Mod - SSDS** | **$0.04B** | Mission Solutions $14M, PMAT $6M |
| **DDG Mod - HELIOS** | **$0.06B** | MZA Associates $25M, L3 Technologies $22M |
| **DDG Mod - SEWIP** | **<$0.01B** | (depleted by per-PIID cap; SEWIP B2 was 99% pre-window per §12.2) |
| **DDG-1000** | **$0.13B** | Red River Technology $61M, Air Masters Mechanical $6M |
| **Standard Missile family** | **$0.93B** | L3Harris (Aerojet) $390M, Honeywell $43M, Goodrich Actuation $32M |
| **Airborne MCM (ALMDS/AMNS/Barracuda)** | **$0.15B** | Sparton DeLeon Springs $108M, Teledyne (on AMNS) $17M |
| **MK-54 Torpedo** | **$0.03B** | L3Harris (Aerojet) $25M, J&E Precision Tool $3M |
| **Ship Gun Systems** | **<$0.01B** | (BAE MK 110 PIIDs are fully pre-window) |
| **Depot Maintenance** | **~$1.5B** (post-cap) | Hampton Roads sub-tier (IMIA $204M, Bay Metals $93M, etc). The prior file's $3.57B LHD-depot figure was inflated by ~2x; the real distribution is across many small specialized vendors |

### Key Findings (revised after fresh per-mod pull AND v3 subaward dedup)

1. **Raytheon is now the #1 prime by FY20-26 window obligation across
   in-scope programs at ~$13.7B**, narrowly ahead of HII (~$22B) and well
   ahead of BIW (~$8.8B). The reason is Standard Missile family
   (~$5.73B), of which **$5.56B comes from 7 production contracts the
   prior file completely missed** (N0002424C5408 GMA, N0002420C5405 SM
   IPC, N0002424C6104 SM Production Lot #2, N0002421C5411 SM-2 BLK IIIB,
   N0002425C5409 FY25 SM-6, N0002418C5432 Encanistered Missile,
   N0002423C5408 SM-2 DLMF). The Lessons §4 round-3 dollar-floor backstop
   surfaced these via vendor + agency + dollar-floor sweep, which the
   original keyword search missed.

2. **The DDG-51 industrial base** is HII (~$11.7B in window across HII
   PIIDs) + BIW (~$9.0B) for hull construction. Combined ~$20.7B FY20-26
   window obligation across 6 MYP vehicles + lead yard services.
   Lockheed Martin for Aegis combat system is **fully pre-window**
   (legacy N0002403C5115 has $0 in window).

3. **Raytheon's CIWS/RAM family is much bigger than the prior file
   showed.** The new vehicle sweep added 6 contracts totaling ~$1.87B
   that the original keyword search missed (FY22-26 RAM GMRP, FY25 CIWS
   Production, MK-99 PBL NRD, etc.). Combined CIWS/RAM/SeaRAM window
   obligation is ~$1.99B (vs the prior file's "$920M+" total).

4. **DDG-1000 is in closeout** with only ~$1.35B of window obligation
   across the 7 pulled PIIDs (vs ~$5.3B cumulative). The BIW lead
   shipbuilder contract (N0002406C2303, FY06) and Raytheon mission systems
   integrator (N0002410C5126, FY10) are 100% pre-window.

5. **Many cumulative-vs-window corrections were dramatic.** The most
   striking: HII LPD 28 (N0002416C2431) is **97% pre-window** ($77M of
   $3.00B cumulative is in window); BIW DDG FY13-17 MYP is **90%
   pre-window**; LM SEWIP Block 2 subsystems is **99% pre-window**. The
   prior file's headline "cumulative" numbers significantly overstated
   FY20-26 obligation.

6. **Marinette Marine $2.49B is the verified figure** (from
   per-`sub_id` MAX dedup, not capped further because LCS Freedom prime
   has a $4.98B cumulative). The previous file's $47.17B was a 19x
   cumulative-snapshot artifact. Marinette is the actual Freedom-variant
   LCS hull builder with LM as integrator prime — this is the LCS
   analog of the Virginia/Columbia EB/HII team-build pattern.

7. **CAES + Mercury combined exposure across SPY-6/SEWIP B2/SLQ-32(V)6
   is ~$503M**, not $5B+. The "hidden RF backbone" narrative was based
   on cumulative-summed subaward records. CAES is at $217M total
   (cross-PIID) and Mercury at $128M after v3 dedup. Both still
   meaningful RF subs, but an order of magnitude smaller than the prior
   file claimed.

8. **The "hidden tier" is much smaller than the prior file showed.**
   After v3 dedup with cap-at-prime, the top 50 parent companies sum to
   approximately **$10.35B in window** across all 170 in-scope PIIDs.
   The prior file's totals would have suggested $80B+ across the same
   primes. The cumulative-snapshot duplication problem affected
   essentially every subaward number in the file.

9. **Hampton Roads ship-repair sub-tier figures shrunk dramatically.**
   The prior file's claims:
   - PCE $942M → corrected: **$30M**
   - Earl Industries $933M → corrected: tiny (mostly historical)
   - Marine Hydraulics International (as sub) $414M → corrected: tiny
   - TECNICO $230M → corrected: **$55M**
   - IMIA $179M → corrected: **$204M** (this one held up)
   - Bay Metals $88M → corrected: **$93M** (held up)

   The qualitative finding (a regional sub-tier exists under BAE/Metro/
   NASSCO depot primes) remains valid, but the dollar volume is closer
   to **$1-2B in-window total** across all depot subs, not $3.57B.

10. **Standard Missile is L3Harris (Aerojet Rocketdyne)'s game.** $378M
    of solid rocket motor work across 4-5 SM production contracts. This
    is the bulk of L3Harris-as-sub exposure across in-scope programs.
    Combined L3Harris (Cincinnati Electronics on CIWS + Maritime P&E on
    DDG/LPD/LHA + Aerojet Rocketdyne on SM) exceeds **$580M**.

11. **General Dynamics is the #3 parent at $432M as sub** — almost
    entirely driven by GDMS at $359M as sub on Raytheon SPY-6 production
    (intra-corporate-style work), plus GD-OTS / GDLS on CIWS/RAM/DDG-1000.

12. **Apparent prime/sub mismatches on long-running contracts** (LCS
    Freedom: $250M prime window vs $2.49B Marinette sub window) reflect
    subs delivering work in window funded by pre-window prime
    obligations. The contract was awarded FY10 with $4.74B pre-window
    cumulative; Marinette has been spending down that scope ever since.

13. **BIW under-reports subawards across all 6 DDG-51 PIIDs** (~$51M
    total reported vs. ~$8.8B in primes). The "true" BIW sub footprint
    is invisible in USAspending — same FFATA reporting gap pattern
    observed for Bollinger, Birdon, Austal, and foreign ICE Pact primes
    (Lessons §6).

14. **MZA Associates' HELIOS exposure was overstated 16x** — prior file
    showed $395M, v3 corrected shows **$25M**. The HELIOS subaward base
    overall is small (~$62M total in-window). LM Aculight handles most
    HELIOS work in-house.

15. **Teledyne Defense Electronics is a real $922M sub** at the raw
    record level — but it's on a single $143M prime (GDMS SMCM Unmanned)
    so v3 caps it at the prime size (~$143M, not $922M). Real cross-PIID
    Teledyne (rolled up) is **~$55M** after correction. The prior file
    placed Teledyne on multiple primes; in fact it's concentrated on
    SMCM Unmanned (which is itself a small program with a large
    component buy that USAspending mis-reports).

16. **Depot maintenance subs were dramatically inflated by USAspending
    data corruption on the NASSCO USS Cowpens MODPRD PIID
    (N0002418C4439).** Five different recipients (HL Welding, Brewer
    Crane, Diamond Environmental, Hawthorne Machinery, American
    Scaffold) all reported the exact same phantom $920M amount on a
    $198M prime contract. v3 excludes these entirely (raw > 2x prime).

---

## 23. Methodology & Limitations

### Data Pipeline (fresh API pulls 2026-04-10)

**Window: 2020-01-01 through 2026-04-10** (per user direction).

1. **FPDS Atom Feed** (https://www.fpds.gov/ezsearch/FEEDS/ATOM) -- **per-mod
   pull, not latest-mod-per-PIID dedup**
   - For each of **82 in-scope PIIDs**, queried `PIID:"<piid>"` and
     paginated through ALL mods (not just the latest)
   - Parsed `<ns1:award>`, `<ns1:OtherTransactionAward>`, and
     `<ns1:OtherTransactionIDV>` record types from XML
   - Captured per-mod fields: `signedDate`, `modNumber`, `obligatedAmount`
     (this action only), `totalObligatedAmount` (cumulative through this
     mod), `totalBaseAndAllOptionsValue` (cumulative ceiling),
     `vendorName`, `descriptionOfContractRequirement`
   - **Computed FY20-26 window delta** as:
     `sum(obligatedAmount for mod in mods if 2020-01-01 ≤ signedDate ≤ 2026-04-10)`
     This is the per-mod sum approach from Lessons-Learned §14 alternative
     method ("you can sum the per-mod `obligatedAmount` (this action only)
     field across mods in window")
   - Also retained `latest_in_window_total_obligated`,
     `pre_window_total_obligated`, and `latest_in_window_ceiling` for
     cross-reference and pattern classification (PRE/STR/NEW)
   - Saved to `data_pull/fpds_mod_data.json`

2. **FPDS new vehicle sweeps** (Lessons §4 round-3 backstop)
   - Sweep 1: `VENDOR_NAME:"RAYTHEON" DESCRIPTION_OF_REQUIREMENT:"STANDARD MISSILE" SIGNED_DATE:[2023/01/01,2026/04/10]`
     -- caught 5 PIIDs but most were already known
   - Sweep 2: `VENDOR_NAME:"RAYTHEON" CONTRACTING_AGENCY_ID:"1700" SIGNED_DATE:[2023/01/01,2026/04/10] OBLIGATED_AMOUNT:[100000000,99999999999]`
     -- caught **26 unique Raytheon Navy PIIDs**, of which **13 were new
     in-scope (7 SM family + 6 CIWS/RAM family) totaling ~$7.5B**
   - Sweep 3: `CONTRACTING_AGENCY_ID:"1700" SIGNED_DATE:[2025/01/01,2026/04/10] OBLIGATED_AMOUNT:[100000000,99999999999]`
     -- 128 unique PIIDs, validated coverage of in-scope contracts and
     surfaced out-of-scope contracts (carriers, oilers, submarines)
   - Saved to `data_pull/new_vehicles_sweep.json`

3. **USAspending Subaward Comprehensive Pull with v3 dedup**
   - **All 170 in-scope PIIDs** were re-pulled (82 from per-mod
     construction/modernization/weapons + 88 depot maintenance from a
     vendor sweep of BAE Norfolk/SD/Jax/Hawaii, NASSCO, Metro Machine,
     Vigor Marine, Continental Maritime SD, MHI, Pacific Ship Repair,
     plus filter to in-scope hull classes via description regex)
   - For each PIID: `POST /search/spending_by_award/` with contracts
     group then IDV group fallback to find `generated_internal_id`,
     then `POST /subawards/` paginating until `hasNext=false`
   - **v3 three-stage dedup applied per PIID:**
     1. **Stage 1 (per `sub_id` MAX):** USAspending issues multiple
        snapshot records for the same `subaward_number` at different
        action_dates. Take MAX per unique `sub_id`.
     2. **Stage 2 (collapse identical-amount duplicates):** USAspending
        also issues separate `subaward_number`s for the same underlying
        subcontract when the prime gets a new mod, each at the same
        cumulative amount. Per (recipient, amount), keep one record.
     3. **Stage 3 (cap + exclude at prime size):** Per (recipient,
        prime_piid), cap the total at 1.0× the prime contract value
        (a sub cannot exceed its prime). Entirely exclude any pair
        > 2× prime (clear data corruption).
   - **Cross-PIID rollup** by recipient with manually-curated parent
     company normalization (GD divisions → "General Dynamics", L3 +
     L3Harris + L3Harris divisions → "L3Harris", etc.)
   - Saved to `data_pull/subaward_full.json` (raw subaward records) and
     `data_pull/subaward_aggregated_v3.json` (rollups)

4. **SAM.gov Opportunities API:** Skipped per Lessons-Learned §3
   rate-limit and accuracy guidance (this is a contract-execution pull,
   not a pipeline pull)

### The per-mod sum method: caveats

Lessons-Learned §14 documents two methods for computing window deltas:
the cumulative-method (`latest_in_window_total - pre_window_total`) and
the per-mod sum (`sum of per-mod obligatedAmount across in-window mods`).
**This file uses the per-mod sum method** because it doesn't require
pulling pre-window mods. Two known limitations:

1. **Option-exercise undercounting.** When a mod exercises an option and
   the cumulative `totalObligatedAmount` jumps but the per-mod
   `obligatedAmount` (this action only) field is recorded as $0 or much
   smaller, the per-mod sum understates. Example in our data:
   N0002424C2467 (HII LHA 10 AP) shows window_delta=$322M but
   cumulative=$807M after a Dec 2025 mod; the contract is fully
   window-native so the "true" obligation is closer to $807M.

2. **SLIN-split overcounting (or undercounting).** Some mods produce
   multiple Contract Action Records (CARs) per mod number — typically
   one for FMS scope and one for US scope, each with its own
   `obligatedAmount` and `totalObligatedAmount`. The per-mod sum
   correctly captures both CARs. The "latest in-window cumulative" only
   captures whichever CAR was alphabetically/temporally latest, so it
   may be lower than the per-mod sum. Example: N0002425C5501 (Raytheon
   SPY-6 FoR design agent) shows window_delta=$205M but cumulative=$5M
   because the latest mod's `totalObligatedAmount` reflects only the
   FMS-scope SLIN view, not the US+FMS combined.

Both effects are visible in the data and noted where they materially
affect the headline number (e.g., LHA 10 AP, SPY-6 FoR design agent).
The per-mod sum method is still strictly more accurate than reporting
`totalObligatedAmount` cumulative-since-award as if it were window
spend (the prior file's mistake).

### Known Limitations

1. **Per-mod sum method caveats** (see above) — option exercises and
   SLIN splits cause known divergences from cumulative figures.

2. **The $47.17B Marinette Marine figure** has been re-pulled and
   corrected. Real value is $2.49B.

3. **All subaward figures in this file are v3 corrected** (170-PIID
   comprehensive pull, 3-stage dedup with cap at prime size). The
   previous file's subaward numbers were inflated by ~3-20x by
   USAspending cumulative-snapshot reporting; v3 dedup removes most of
   that inflation.

4. **Per-pair sanity cap may slightly understate.** Two flagged pairs
   hit the v3 cap: TIMKEN GEARS on N0002419C4447 (Vigor Marine Cape St
   George, raw $831M / capped at $447M prime) and TRIDENT SENSORS on
   N6133111C0017 (GDMS SMCM Unmanned, raw $233M / capped at $143M prime).
   The "real" delivery is somewhere between the capped value and the raw
   value.

5. **BIW reports near-zero subawards** across all 6 DDG-51 PIIDs (~$51M
   total reported on ~$8.8B in primes). Per Lessons §6, this is a known
   FFATA reporting non-compliance pattern, not an absence of
   subcontracting.

5. **Subaward reporting lag**: prime contracts signed in the last 12-18
   months will not have meaningful sub records yet. The newest LPD 33/34/35
   contract (N0002424C2473), the SPY-6 Family of Radars design agent
   (N0002425C5501), and several DDG depot contracts signed late 2025/early
   2026 have minimal or no sub data.

6. **Federal shipyard work is NOT a concern for this scope.** Surface
   combatant and amphibious depot maintenance is competed among private
   regional shipyards (BAE Norfolk/SD/Jacksonville/Hawaii, NASSCO, Metro
   Machine, Vigor, Continental Maritime, MHI). FPDS coverage is essentially
   complete for these hulls. The federal naval shipyards (Norfolk,
   Portsmouth, Pearl Harbor, Puget Sound) only swallow SSN/SSBN and CVN
   depot work -- both out of scope here.

7. **Vendor name normalization required.** Federal data lists parent and
   division entities separately (Coltec/Fairbanks Morse, York/Johnson
   Controls, L3/L3Harris, GD multiple divisions). The summary tables in
   §22 collapse these where flagged; individual contract tables retain
   the FPDS legal entity name.

8. **OTA awards via consortia** (ATI, NSTXL) may list the consortium as
   vendor rather than the performing company. Examples in this file:
   the MK-54 MOD 2 development OTA via Advanced Technology International
   and the SPY-6 RF Head Prototype.

9. **Classified programs** are excluded from all public databases.
   Surface combat classified content (intelligence-collection sensors,
   certain EW capabilities) is not visible.

10. **FMS (Foreign Military Sales)** content -- particularly Standard
    Missile and AN/SPY-6 Family of Radars -- shows up in FPDS but is
    hard to filter from US-funded work without parsing description
    fields carefully.

---

## 24. SAM Line Item → Contract Vehicle Crosswalk

This section maps each FY2026 SAM line from `key programs.xlsx` to the
contract vehicles identified above. **Use these crosswalks to interpret
the cumulative numbers in the prime tables as "size of vehicle" rather
than "FY26 spend."**

### LHD ($1.10B FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| OMN_Vol2 LHD/AMPHIBS depot | 346,443 | Ship-availability-specific PIIDs to BAE Norfolk/SD, Metro Machine, NASSCO. New FY26 SRA on USS Iwo Jima already signed (N0002426C4405, $204M obligated / $241M ceiling) |
| OMN_Vol2 LHD/AMPHIBS modernization | 631,859 | Existing alteration installation contracts to BAE Norfolk/SD and Metro Machine |
| OPN_BA1 Line 8 LHA/LHD Midlife | 123,384 | Cross-program: see §14.1. BAE/Metro/Gibbs & Cox |

### LPD ($1.26B FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| SCN 3010 LPD Flight II procurement | 835,037 | **N0002424C2473** (LPD 33/34/35 block buy, $5.80B ceiling) -- new FY26 mod |
| SCN 3010 LPD Flight II AP | 275,000 | **N0002424C2473** advance procurement scope OR new FY26 LLTM contract |
| OMN_Vol2 LPD depot | 149,595 | Ship-availability PIIDs to BAE Norfolk/SD |
| OPN_BA1 Line 15 LPD Class Support Equipment | 125,542 | HII LPD 17 Class Engineering ($224.7M ceiling), Raytheon LCE&S ($485M ceiling) |
| OMN_Vol2 LPD modernization | 11,852 | Small alteration installation work |

### LSD ($98M FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| OMN_Vol2 LSD depot | 94,421 | Ship-availability PIIDs to NASSCO, BAE Norfolk/SD, Metro Machine |
| OMN_Vol2 LSD modernization | 25,931 | Alteration installation work (small) |
| OPN_BA1 Line 40 LSD Midlife & Modernization | 4,079 | Class drawdown / minor mods |

### LHA ($691M FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| SCN 3041 LHA Replacement | 634,963 | **N0002420C2437 (LHA 9, $2.56B / $3.14B ceiling)** -- ongoing construction mods + N0002424C2467 (LHA 10 AP, $130M) follow-on |
| OMN_Vol2 LHA depot | 45,012 | NASSCO USS America (LHA 6) FY26 DSRA (N0002425C4404, $198M ceiling) |
| OMN_Vol2 LHA modernization | 12,065 | HII LHA engineering / mod support |

### DDG ($11.4B FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| SCN 2122 DDG-51 procurement | 5,410,773 | **N0002423C2307 (HII FY23-27 MYP)** + **N0002423C2305 (BIW FY23-27 MYP)** -- new FY26 boat funding mods |
| SCN 2122 DDG-51 AP | 1,750,000 | New FY26-FY28 AP funding mod against the FY23-27 MYP vehicles, OR a new FY28+ MYP LLTM contract if signed |
| SCN 2119 DDG 1000 | 52,358 | **N0002423C2324 (HII Mod Planning, $308M)** + **N0002424C2331 (BIW Planning Yard, $196M)** -- closeout/activation |
| OMN_Vol2 DDG depot ($525M + $427M) | 952,000 | Ship-availability PIIDs to BAE/NASSCO/Continental/Vigor/MHI/Metro -- many already signed in window |
| OMN_Vol2 DDG-1000 depot | ~7,800 | Small line; embedded in DDG-1000 activation contracts |
| OMN_Vol2 DDG modernization | 1,282,612 | Cross-vehicle alteration installation work |
| WPN 2234 Standard Missile | 1,008,875 | New FY26 production mods against the Raytheon SM PIIDs -- though all listed PIIDs are pre-window or borderline straddle, suggesting a newer Raytheon SM production vehicle exists that wasn't surfaced in our pull |
| OPN_BA1 Line 5 DDG Mod | 878,787 | Cross-vehicle: SPY-6 production (**N0002422C5500**), SEWIP Block 2/3 (**N0002420C5503** + N0002416C5363 + NG Block 3), SSDS (**N0002419C5603**), CEC (**N0002419C5200**), CIWS (**N0002418C5406**), HELIOS (**N0002418C5392**), Aegis Mod Kits |
| WPN 3215 MK-54 Torpedo Mods | 128,513 | **N0002425C6401 (GDMS MK 54 MOD 1 LWT, $791.9M ceiling)** + Ultra Electronics MK 54 MOD 0 + ATI consortium MOD 2 OTAs |
| OPN_BA1 Line 16 DDG 1000 Class Support Equip | 115,267 | Raytheon DDG-1000 mission systems vehicles (**N0002417C5145** $888M ceiling, **N0002422C5522** $568M) + BIW Planning Yard |
| WPN 2356 Standard Missiles Mods | 32,127 | Folded into Raytheon SM production (small mods line) |
| OPN_BA2 Line 2213 SSTD | 14,915 | SAIC Nixie engineering + Penn State CCAT |
| OPN_BA4 Line 5111 Ship Gun Systems | 7,358 | BAE Land & Armaments MK 110 production vehicles (small line) |

### LCS ($1.34B FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| OMN_Vol2 LCS depot | 576,389 | LM Freedom Variant ISEA + GDMS Independence Variant ISEA + ship availability contracts |
| OMN_Vol2 LCS modernization | 383,361 | LM Freedom Variant Combat System ISEA (N6339424C0003, $69M ceiling) + GDMS Independence ISEA (N6339424C0004, $72M) + LCS ITT-2A update (N6134023F0385, $45.6M) |
| OPN_BA1 Line 37 LCS In-Service Mod | 189,458 | Cross-platform sustainment vehicles (LM, GDMS, Textron, BAH PEO LCS support) |
| OPN_BA1 Line 34 LCS MCM Mission Modules | 91,372 | UISS (Textron N0002414C6322), Knifefish (GDMS N0002421C6304 + NG N0002417C6311), MCM USV (Bollinger N0002422C6305), AQS-20, AQS-24C, Barracuda (N0002418C6300) |
| OPN_BA1 Line 33 LCS Common Mission Modules Equip | 38,880 | Cross-package infrastructure (LM/GDMS shared) |
| WPN 2292 Naval Strike Missile | 32,238 | Raytheon NSM integration (M6785422F1001, $43.7M ceiling) -- Kongsberg OEM portion via FMS |
| OPN_BA3 Line 119 Airborne MCM | 9,643 | NG ALMDS (**N0002415C6318** $517M + N0002422C6418 $107M ceiling) + Raytheon AMNS (N0002417C6305 + N0002425F6404 + N0002421F6412) |
| OPN_BA1 Line 36 LCS SUW Mission Modules | 3,790 | Bowhead Professional Solutions (N0017817F3007) |
| WPN 4221 LCS Module Weapons | 2,200 | Small integration line; limited FPDS visibility |

### CG Ticonderoga ($160M FY26 total)

| FY26 SAM Line | $K | Likely receiving vehicle |
|---|---|---|
| OMN_Vol2 CG depot ($75M + $40M) | 115,501 | Vigor Marine MODPRD ($426M ceiling for CG 65/CG 71 FY20) + BAE Norfolk + NASSCO + HII CG 47 Advanced Planning ($453M) |
| OMN_Vol2 CG modernization | 44,940 | Same vendor pool; alteration installation work |

### How to verify "this mod was funded by FY26 money"

Per Lessons-Learned §15, read mod descriptions for FY26 references:

- "**FY26**", "**FY 26**", or "**FY2026**" explicitly
- "**INCREMENTAL FUNDING**" or "**INC FUNDING MOD**"
- A purchase request (PR) number with FY26 in the prefix
- A boat name/hull number that's FY26-procured

Example pattern (from the parallel submarine pull):
```
N0002424C2114 mod P00003 signed 2025-12-17, this action $927.6M
  description: "FY26 SHIPSET OF VIRGINIA CLASS COMPONENT FUNDING MOD"
```

That's an unambiguous FY26 obligation. Compare to:
```
N0002417C2100 mod A00343 signed 2025-12-23, this action $0.0M
  description: "INCORPORATION OF PREVIOUSLY AUTHORIZED CHANGES UNDER COUPON
                PROCESS FOR VIRGINIA CLASS AUTHORIZING MOD"
```

That's a paperwork mod -- doesn't count toward FY26 spend.

### The bottom line

**The cumulative `totalObligatedAmount` numbers in the prime tables are
useful for identifying which contractor holds which program**, but they
**should not be added up to compute "FY20-26 spend" or compared directly
to SAM annual appropriations**. Use them as "size of contract vehicle"
references, and use mod descriptions to attribute specific dollar amounts
to specific fiscal years.

For a true FY26-only spend pull on any of these programs, you'd:
1. Filter to mods with `signed_date` in FY26 (Oct 2025 - Sep 2026)
2. Sum the **per-mod `obligatedAmount`** field (this action only), NOT
   `totalObligatedAmount` (cumulative)
3. Cross-check against the description for "FY26" / boat-name / PR
   references

That per-mod analysis was not performed for this file -- the prime
tables are "contract size" references rather than "annual spend"
references. The window-native [NEW] entries are the closest to clean
window pulls because their entire cumulative is in window.

---

*Generated 2026-04-10 from fresh FPDS Atom Feed and USAspending
/api/v2/subawards/ pulls. Window: 2020-01-01 through 2026-04-10. Scope:
surface combatants and amphibious warfare ships per `key programs.xlsx`
(FY2026 Budget Justification books + DAA JES FY2026).*

*Data pull artifacts in `data_pull/`:*
- *`fpds_mod_data.json` — 82 in-scope construction/modernization/weapons*
  *PIIDs with full per-mod history for window-delta computation*
- *`new_vehicles_sweep.json` — FPDS sweep that surfaced 13 new Raytheon*
  *SM/CIWS/RAM contracts the prior file missed*
- *`depot_piids_filtered.json` — 88 depot maintenance PIIDs from a*
  *vendor sweep filtered to in-scope hull classes*
- *`subaward_full.json` — full subaward records for all 170 PIIDs*
- *`subaward_aggregated_v3.json` — cross-PIID rollup with v3 dedup*

*Supersedes `SAM_Program_Contract_Awards.md` and*
*`SAM_Program_Component_Contracts.md` within this scope. Applies:*
1. *Per-mod sum window-delta method (Lessons §14 alternative) for prime*
   *contract obligations*
2. *3-stage v3 subaward dedup (per sub_id MAX → collapse identical*
   *amounts → cap at prime size, exclude > 2× prime) for all 170 in-scope*
   *PIIDs*
3. *Manually-curated parent-company normalization for cross-PIID rollups*
4. *Corrected vendor numbers throughout — Marinette $2.49B (not $47.17B),*
   *CAES + Mercury $503M combined (not $5B+), MZA $25M on HELIOS (not*
   *$395M), Hampton Roads PCE $30M (not $942M), etc.*
