# FY2026 SAM Programs -- Prime & Subcontractor Award Analysis

Research compiled from FPDS Atom Feed and USAspending API. Covers the programs
identified in the SAM sheet bottom table ("FY2026 SAM -- Amphibious Warfare Ships
& Surface Combatants: Funding Line Detail by Hull").

Data sources: FPDS (authoritative contract-level data), USAspending (aggregated
views + subaward data). SAM.gov skipped per guidance.

> **Note on subcontractor data:** Public subaward data (via USAspending) only
> covers first-tier subs on contracts over $30K and is inconsistently reported.
> Companies doing significant work as lower-tier subcontractors are invisible in
> public data.
>
> **Updated 2026-04-10:** Subcontractor sections now include data from a deep
> USAspending subaward pull (2020-2026) that goes far beyond the initial 25-result
> keyword search. The HII DDG-51 FY18-22 contract alone has 2,192 subaward records
> totaling $1.15B; the LM SEWIP Block 2 contract has 358 subaward records totaling
> $2.85B. These were pulled by looking up each prime PIID's `generated_internal_id`
> via `/api/v2/search/spending_by_award/` and then calling the
> `/api/v2/subawards/` endpoint, which returns the full subaward tree per prime
> contract.

---

## Table of Contents

1. [DDG-51 Arleigh Burke -- New Construction](#1-ddg-51-arleigh-burke--new-construction-scn-2122--72b)
2. [DDG-51 -- Scheduled Depot Maintenance](#2-ddg-51--scheduled-depot-maintenance-omn--960m)
3. [DDG-51 -- Modernization](#3-ddg-51--modernization-multiple-lines--35b)
4. [DDG 1000 Zumwalt -- New Construction / Closeout](#4-ddg-1000-zumwalt-scn-2119--52m)
5. [LPD Flight II -- New Construction](#5-lpd-flight-ii--new-construction-scn-3010--11b)
6. [LPD -- Depot Maintenance & Modernization](#6-lpd--depot-maintenance--modernization--282m)
7. [LHA Replacement -- New Construction](#7-lha-replacement--new-construction-scn-3041--635m)
8. [LHA -- Depot Maintenance & Modernization](#8-lha--depot-maintenance--modernization--57m)
9. [LHD -- Depot Maintenance & Modernization](#9-lhd--depot-maintenance--modernization--11b)
10. [LCS -- Depot Maintenance & Modernization](#10-lcs--depot-maintenance--modernization--13b)
11. [LSD -- Depot Maintenance & Modernization](#11-lsd--depot-maintenance--modernization--124m)
12. [CG (Ticonderoga) -- Depot Maintenance & Modernization](#12-cg-ticonderoga--depot-maintenance--modernization--160m)
13. [Standard Missile (WPN 2234)](#13-standard-missile-wpn-2234--1b)
14. [DDG Mod (OPN BA1, Line 5)](#14-ddg-mod-opn-ba1-line-5--879m)
15. [DDG 1000 Class Support Equipment (OPN BA1, Line 16)](#15-ddg-1000-class-support-equipment-opn-ba1-line-16--115m)
16. [MK-54 Torpedo Mods (WPN 3215)](#16-mk-54-torpedo-mods-wpn-3215--129m)
17. [LHA/LHD Midlife (OPN BA1, Line 8)](#17-lhalhd-midlife-opn-ba1-line-8--123m)
18. [LPD Class Support Equipment (OPN BA1, Line 15)](#18-lpd-class-support-equipment-opn-ba1-line-15--126m)
19. [Naval Strike Missile (WPN 2292)](#19-naval-strike-missile-wpn-2292--32m)
20. [LCS In-Service Modernization (OPN BA1, Line 37)](#20-lcs-in-service-modernization-opn-ba1-line-37--189m)
21. [LCS MCM Mission Modules (OPN BA1, Line 34)](#21-lcs-mcm-mission-modules-opn-ba1-line-34--91m)
22. [LCS Common Mission Modules Equipment (OPN BA1, Line 33)](#22-lcs-common-mission-modules-equipment-opn-ba1-line-33--39m)
23. [LCS SUW Mission Modules (OPN BA1, Line 36)](#23-lcs-suw-mission-modules-opn-ba1-line-36--4m)
24. [Surface Ship Torpedo Defense (OPN BA2, Line 2213)](#24-surface-ship-torpedo-defense-opn-ba2-line-2213--15m)
25. [Ship Gun Systems Equipment (OPN BA4, Line 5111)](#25-ship-gun-systems-equipment-opn-ba4-line-5111--7m)
26. [Directed Energy Systems (OPN BA4, Line 5510)](#26-directed-energy-systems-opn-ba4-line-5510--3m)
27. [Airborne MCM (OPN BA3, Line 119)](#27-airborne-mcm-opn-ba3-line-119--10m)
28. [LCS Module Weapons (WPN 4221)](#28-lcs-module-weapons-wpn-4221--2m)
29. [Standard Missiles Mods (WPN 2356)](#29-standard-missiles-mods-wpn-2356--32m)
30. [LSD Midlife & Modernization (OPN BA1, Line 40)](#30-lsd-midlife--modernization-opn-ba1-line-40--4m)

---

## 1. DDG-51 Arleigh Burke -- New Construction (SCN 2122 / ~$7.2B)

**Dual-source procurement strategy with two prime shipbuilders.**

### Prime Contractors

| Contractor | Parent | Location | Role |
|---|---|---|---|
| **Huntington Ingalls Incorporated (Ingalls Shipbuilding)** | HII | Pascagoula, MS | DDG-51 shipbuilder (East Coast hulls) |
| **Bath Iron Works Corporation** | General Dynamics | Bath, ME | DDG-51 shipbuilder + Lead Design Yard |

### Key Contracts (FPDS + USAspending)

| PIID | Contractor | Ships | Obligated | Ceiling | Period |
|---|---|---|---|---|---|
| N0002423C2307 | HII | DDG 51 FY23-27 block | $6.95B | ~$7B | 2023+ |
| N0002418C2307 | HII | DDG 51 FY18-22 block | $6.72B | ~$6.7B | 2018-2024 |
| N0002418C2305 | BIW | DDG 51 FY18-22 block | $5.34B | ~$5.3B | 2018-2024 |
| N0002423C2305 | BIW | DDG 51 FY23-27 block | $5.03B | ~$5B | 2023+ |
| N0002413C2305 | BIW | DDG 51 FY13-17 block | $4.93B | ~$5B | 2013-2024 |
| N0002413C2307 | HII | DDG 117 FY13/FY16 | $3.35B | $3.54B | 2013-2024 |
| N0002418C2313 | BIW | DDG 51 Lead Yard Svcs FY18-22 | $303M | $303M | 2018+ |
| N0002424C2313 | BIW | DDG 51 Lead Yard Svcs FY24+ | $186M | ~$186M | 2024+ |

**Other prime roles:**
- **Lockheed Martin Corporation** -- DDG-51 Combat Systems / Aegis (N0002403C5115: $972M)
- **Serco Inc** -- Ship Production Planning (N0016422F3012: $146M)
- **QED Systems, Inc.** -- Third Party Planning DDG 51/CG 47 ($140M)

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull, 2020-2026)

Aggregated across **5 HII DDG-51 prime PIIDs** = **5,312 subaward records totaling
$2.89B**. BIW DDG-51 contracts have far thinner subaward reporting (~$60M total
across all 6 BIW PIIDs combined -- BIW appears to under-report subs).

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **Rolls-Royce Marine North America** | $384.6M | 109 | Propulsion components (gas turbines, gearing) |
| **General Electric** | $196.6M | 21 | LM2500 main propulsion gas turbines |
| **York International** (Johnson Controls) | $191.8M | 54 | HVAC / chilled water plants |
| **L3Harris Maritime Power & Energy Solutions** | $163.0M | 121 | Power conversion / electrical |
| **SOCAIL, LDA** (Portugal) | $151.4M | 10 | Gas turbine engines |
| **Northrop Grumman Systems** | $122.9M | 64 | DDG steering systems |
| **Johnson Controls Navy Systems** | $118.0M | 39 | HVAC systems |
| **DRS Naval Power Systems** | $103.3M | 96 | Switchboards / power distribution |
| **Timken Gears & Services** | $81.8M | 6 | Gearing |
| **Ellwood National Forge** | $73.9M | 13 | Propulsion shafts |
| **Engineered Coil** | $67.4M | 100 | Coiled components / heat exchangers |
| **Espey Mfg & Electronics** | $51.0M | 66 | Power conditioning |
| **Lake Shore Systems** | $43.9M | 137 | Capstans, deck machinery |
| **Erie Forge & Steel** | $35.6M | 8 | Forgings |
| **Power Paragon** | $33.0M | 44 | Switchgear |
| **The Entwistle Co** | $32.1M | 76 | Anchor handling, deck equipment |
| **Air & Liquid Systems** | $31.0M | 39 | Heat exchangers |
| **The Hiller Companies** | $31.0M | 45 | Firefighting systems |
| **US Joiner** | $30.6M | 82 | Outfitting / joiner work |
| **Parker Hannifin** | $30.0M | 26 | Hydraulics, fluid systems |
| **Maxim Evaporators of America** | $29.8M | 20 | Freshwater generation |
| **Alfa Laval** | $27.4M | 25 | Separators / heat exchangers |
| **American Metal Bearing** | $27.3M | 35 | Stern tube bearings |
| **Dover Pumps & Process Solutions** | $25.9M | 63 | Pumps |
| **Howden North America** | $25.3M | 43 | Fans / blowers |
| **RIX Industries** | $22.2M | 25 | Air compressors |
| **Milwaukee Valve** | $19.7M | 128 | Valves |
| **EMS Development** | $18.2M | 23 | Switchboard controls |

---

## 2. DDG-51 -- Scheduled Depot Maintenance (OMN / ~$960M)

**Competed regionally among private shipyards. Not sole-source.**

### Prime Shipyards by Region

**West Coast (San Diego):**

| Shipyard | Example Contract | Ship | Ceiling |
|---|---|---|---|
| **BAE Systems San Diego Ship Repair** | Multiple DSRAs/EDSRAs | DDG 60, 73, 86, 104, 105, 106, 111 | $25M-$119M per availability |
| **NASSCO** | Multiple DSRAs | DDG 54, 86, 91, 106 | $21M-$124M per availability |
| **Continental Maritime of San Diego** | N0002423C4XXX | DDG 90 FY23 DMP | $237M ceiling |
| **HII San Diego Shipyard** | Various | DDG maintenance | $19M-$57M per availability |
| **Pacific Ship Repair & Fabrication** | | DDG 92 FY17 SRA | $124M ceiling |

**Pacific Northwest:**

| Shipyard | Example Contract | Ship | Ceiling |
|---|---|---|---|
| **Vigor Marine LLC** | Various | DDG 100 FY25 DMP, DDG 102 DSRA | $46M-$320M per availability |

**East Coast (Norfolk):**

| Shipyard | Example Contract | Ship | Ceiling |
|---|---|---|---|
| **BAE Systems Norfolk Ship Repair** | Multiple DSRAs | DDG 55, 57, 71, 109 | $58M-$129M per availability |
| **BAE Systems Jacksonville Ship Repair** | | DDG 81 EDSRA | $235M ceiling |
| **Marine Hydraulics International** | | DDG 67 SRA | $280M ceiling |
| **Metro Machine Corp** | | DDG 94, 96 | $25M-$87M per availability |

**Overseas (Forward-Deployed):**

| Shipyard | Location | Ships |
|---|---|---|
| **Sumitomo Heavy Industries** | Yokosuka, Japan | FDNF DDGs |
| **Navantia SA** | Rota, Spain | DDG 117 |

---

## 3. DDG-51 -- Modernization (Multiple Lines / ~$3.5B)

The DDG modernization budget aggregates several major weapons and systems programs.
See dedicated sections below for Standard Missile (#13), DDG Mod (#14), MK-54 (#16),
DDG 1000 Support (#15), Standard Missiles Mods (#29), SSTD (#24), Ship Guns (#25),
and Directed Energy (#26).

---

## 4. DDG 1000 Zumwalt (SCN 2119 / ~$52M)

**Three-ship class; construction largely complete. Remaining funds are for activation/closeout.**

### Prime Contractors

| Contractor | Parent | Role | Key Contract | Value |
|---|---|---|---|---|
| **Bath Iron Works** | General Dynamics | Lead shipyard | N0002406C2303 | $3.31B ceiling |
| **Raytheon Company** | RTX Corp | Mission systems integrator | N0002410C5126 | $1.34B obligated |
| **Raytheon Company** | RTX Corp | Total Ship Activation / MSE | N0002417C5145 | $888M ceiling |
| **Raytheon Company** | RTX Corp | AS&M Support | N0002422C5522 | $568M |
| **HII** | HII | DDG 1000/1001 Mod Planning | N0002423C2324 | $308M |
| **BIW** | General Dynamics | Planning Yard Follow On | N0002424C2331 | $196M |
| **General Dynamics Land Systems** | General Dynamics | MK 46 MOD 2 Gun Weapon System | N0002415C5344 | $76.6M |
| **Microsoft Corporation** | Microsoft | Zumwalt Operating Environment (ZOE) | HC102820F0610 | $9.4M |
| **JHU Applied Physics Lab** | Johns Hopkins | Combat System RDT&E | Multiple | ~$12M |
| **Forethought, Inc.** | -- | IDE Engineering Support | N0002413F2320 | $30.5M |

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

Aggregated across **DDG-1000 prime PIIDs** = **1,237 subaward records totaling
$773.4M** (2020-2026). The largest single contract by subawards is the
**General Dynamics Land Systems MK 46 MOD 2 Gun System for DDG-1000**
(N0002415C5344) with **551 subawards totaling $501.4M** -- this single weapon
system program has more subaward visibility than the entire ship construction.

| Subcontractor | Subaward $ | Actions | Role / Notes |
|---|---|---|---|
| **Red River Technology** | $62.3M | 28 | Computer hardware/SW for DDG-1000 mission systems |
| **Northrop Grumman Systems** | $51.7M | 13 | Semiconductor / electronic components |
| **Systems Engineering & Manufacturing** | $47.6M | 51 | Industrial machinery |
| **Hart Technologies** | $45.2M | 20 | Engineering services |
| **Charles E. Gillman** | $44.8M | 36 | Motor vehicle electronic equipment |
| **Laurel Technologies Partnership** | $43.2M | 14 | Printed circuit boards |
| **Lanzen, Inc.** | $42.5M | 5 | Antenna mounts |
| **Lapeer Industries** | $40.9M | 10 | Aircraft / mission system parts |
| **VarTech Systems** | $40.8M | 5 | Rugged LCD displays / industrial computers |
| **Raytheon (internal)** | $34.2M | 16 | Search / detection / navigation |
| **Kearfott Corp** | $31.2M | 39 | Inertial navigation |
| **Moog Industrial Controls** | $27.9M | 13 | Semiconductors |
| **Motorola Solutions** | $19.9M | 20 | Computer software |
| **Dell Marketing** | $17.2M | 19 | Computer hardware |
| **Atrenne Computing Solutions** | $14.5M | 13 | Test and tooling |
| **Curtiss-Wright DS** | $12.9M | 53 | Engineering services |
| **Sirius Federal** | $12.2M | 41 | UCS storage / enterprise hardware |
| **Real-Time Innovations** | $11.1M | 34 | Software |
| **DRS Naval Power Systems** | $4.5M | 17 | DDG 1000 (VSR SA 24399) |
| **GE Energy Power Conversion USA** | $4.2M | 7 | DDG 1000 power conversion |

---

## 5. LPD Flight II -- New Construction (SCN 3010 / ~$1.1B)

**Sole-source to HII Ingalls Shipbuilding.**

### Prime Contractor

| Contractor | Parent | Location | Role |
|---|---|---|---|
| **Huntington Ingalls Incorporated (Ingalls Shipbuilding)** | HII | Pascagoula, MS | Sole builder, all LPD Flight II hulls |

### Key Contracts

| PIID | Ships | Obligated | Ceiling | Status |
|---|---|---|---|---|
| N0002424C2473 | **LPD 33, 34, 35** (newest block buy) | $1.22B | **$5.80B** | Active -- early obligation |
| N0002418C2406 | LPD 30 (Harrisburg), 31, 32 | $4.63B | $4.66B | Active |
| N0002416C2431 | LPD 28 (Fort Lauderdale) | $3.00B | $3.26B | Active |
| N0002421C2443 | LPD 17 Class Engineering Svcs | $80.6M | $224.7M | Active |
| N0002426C2443 | LPD 17 PD&ES (Post Delivery) | $20.2M | $223.3M | 2025+ |
| N0002416C2415 | LPD 17 LCE&S Core Services | $308.5M | $320.7M | Active |

**Other prime roles:**
- **BAE Systems Norfolk Ship Repair** -- LPD 28 Fitting Out Availability ($75.5M / $169M ceiling)
- **Raytheon Company** -- LCE&S for electronic systems ($130M / $485M ceiling)
- **TMASC Joint Venture** -- LPD 17 Program Office support ($77M)
- **Northrop Grumman Systems** -- Pre-commissioning unit support

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

Aggregated across **HII LPD 17 Class prime PIIDs (LPD 28, 30/31/32) + LHA 9** =
**~2,917 subaward records totaling $1.59B** (2020-2026). Subaward records aren't
yet flowing for the newest LPD 33/34/35 contract (N0002424C2473) -- still early.

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **US Joiner** | $161.6M | 53 | LPD interior outfitting (joiner work) |
| **Coltec Industries** (Fairbanks Morse parent) | $142.2M | 38 | Diesel generator sets |
| **DRS Naval Power Systems** | $125.0M | 50 | LPD switchboards / power distribution |
| **L3Harris Maritime Power & Energy Solutions** | $62.8M | 50 | Power conversion |
| **Caterpillar** | $59.0M | 11 | Diesel engines |
| **Timken Gears & Services** | $49.4M | 15 | Gearing |
| **American Superconductor Corp** | $48.9M | 5 | LHA 9 (superconducting degaussing? -- noteworthy) |
| **York International** | $45.3M | 19 | HVAC plant upgrade kits |
| **Engineered Coil** | $44.9M | 54 | LHA 9 firefighting watermist pumps |
| **Fairbanks Morse** | $44.4M | 45 | Diesel engines / VSR work |
| **Carolina Power Systems of Sumter** | $33.1M | 35 | LPD 29 power systems |
| **Ellwood National Forge** | $27.4M | 8 | Forgings |
| **Industrial Corrosion Control** | $27.0M | 63 | Tank coating / paint |
| **Lake Shore Systems** | $26.9M | 29 | Deck machinery |
| **Milwaukee Valve** | $25.8M | 157 | LPD valves |
| **Jered LLC** | $25.2M | 20 | Material handling |
| **Rolls-Royce Marine North America** | $23.5M | 11 | LPD 27 propulsion |
| **JA Moody** | $21.9M | 73 | LPD 31 butterfly valves |
| **Carver Pump** | $21.3M | 21 | LPD pumps |
| **Alfa Laval** | $20.4M | 13 | Separators / heat exchangers |
| **Griswold Industries** | $20.1M | 67 | LPD 32 control valves |
| **BNL Industries** | $16.1M | 120 | LHA 9 components |
| **HHE Services** | $15.2M | 28 | LPD 21 control stations |
| **Sheffield Forgemasters Engineering** (UK) | $14.9M | 10 | LHA 9 strut castings (large forgings) |
| **GE Energy Power Conversion USA** | $12.2M | 2 | LHA 9 auxiliary propulsion system |
| **Dynalec** | $11.2M | 55 | LHA 9 switchboard alarms |
| **The Hiller Companies** | $11.2M | 17 | Firefighting |
| **Howden North America** | $11.1M | 15 | LHA 9 fans |
| **Johnson Controls Navy Systems** | $11.1M | 15 | LHA 8 HVAC |

---

## 6. LPD -- Depot Maintenance & Modernization (~$282M)

**Competed among private shipyards.**

### Prime Shipyards

| Shipyard | Example Contract | Ship | Ceiling |
|---|---|---|---|
| **BAE Systems San Diego Ship Repair** | N0002425C4415 | USS Somerset (LPD 25) FY25 DSRA | $193M |
| **BAE Systems Norfolk Ship Repair** | Various | LPD East Coast availabilities | Varies |

---

## 7. LHA Replacement -- New Construction (SCN 3041 / ~$635M)

**Sole-source to HII Ingalls Shipbuilding.**

### Prime Contractor

| Contractor | Parent | Location | Role |
|---|---|---|---|
| **Huntington Ingalls Incorporated (Ingalls Shipbuilding)** | HII | Pascagoula, MS | Sole builder, all LHA hulls |

### Key Contracts

| PIID | Ship | Obligated | Ceiling | Status |
|---|---|---|---|---|
| N0002416C2427 | **LHA 8 (Bougainville)** | $3.27B | $3.31B | Active |
| N0002420C2437 | **LHA 9** | $2.56B | $3.14B | Active |
| N0002424C2467 | **LHA 10** (Advance Procurement) | $130M | $130M | Early stage |

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

The HII LHA 9 prime contract (N0002420C2437) alone has **446 subaward records
totaling $333.4M**. The combined LPD/LHA subcontractor table is shown in the LPD
section above (#5) since most major suppliers (Coltec/Fairbanks Morse, DRS Naval
Power, L3Harris Maritime, Engineered Coil, Sheffield Forgemasters, etc.) work
across both programs.

LHA-specific notable findings from the deep pull:

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **American Superconductor Corp** | $48.9M (LHA 9) | Likely degaussing system |
| **Sheffield Forgemasters Engineering Limited** (UK) | $14.9M | LHA 9 strut castings -- large forgings sourced from UK |
| **GE Energy Power Conversion USA** | $12.2M | LHA 9 auxiliary propulsion system |
| **Dynalec** | $11.2M | LHA 9 switchboard alarm systems |
| **Aqua-Chem** | $5.0M | LHA 9 freshwater generation |
| **Lister Chain & Forge** | $4.5M | LHA 9 detachable anchor chain links |

---

## 8. LHA -- Depot Maintenance & Modernization (~$57M)

### Prime Shipyards

| Shipyard | Example Contract | Ship | Ceiling |
|---|---|---|---|
| **NASSCO** | N0002425C4404 | USS America (LHA 6) FY26 DSRA | $198M |
| **HII (Ingalls)** | Various | LHA engineering/mod support | Varies |

### Key Support Contractors

| Contractor | Contract | Value | Role |
|---|---|---|---|
| Gibbs & Cox | Various | ~$2.7M | LHD/LHA midlife electric plant control system upgrades |
| Orbis Sibro | Various | $15.8M / $25M ceiling | Ship modernization program oversight |
| Amee Bay, LLC | Various | $2M / $3.8M ceiling | LHD midlife AIT |
| Valkyrie Enterprises | Various | $3.7M | LHD 2 & LHD 7 modifications |

---

## 9. LHD -- Depot Maintenance & Modernization (~$1.1B)

**Competed regionally. Largest MRO spend for amphibious ships.**

### Prime Shipyards

**East Coast (Norfolk):**

| Shipyard | Contract | Ship | Obligated | Ceiling |
|---|---|---|---|---|
| **BAE Systems Norfolk Ship Repair** | N0002411C4407 | LHD 3 FY11 PMA | -- | $849M |
| **BAE Systems Norfolk Ship Repair** | N0002423C4408 | USS Kearsarge (LHD 3) FY23 DSRA | $325M | $348M |
| **BAE Systems Norfolk Ship Repair** | N0002426C4405 | USS Iwo Jima (LHD 7) FY26 SRA | $204M | $241M |
| **BAE Systems Norfolk Ship Repair** | N0002425C4430 | USS Wasp (LHD 1) FY25 SRA | $102M | $102M |
| **BAE Systems Norfolk Ship Repair** | N0002421C4404 | USS Wasp (LHD 1) FY21 DSRA | $241M | $241M |
| **Metro Machine Corp** | N0002424C4418 | USS Bataan (LHD 5) FY24 DSRA | $338M | $394M |
| **Metro Machine Corp** | N0002422C4490 | USS Iwo Jima (LHD 7) FY22 DSRA | $259M | $358M |
| **Metro Machine Corp** | N0002420C4467 | USS Bataan (LHD 5) FY20 SRA | $112M | $131M |

**West Coast (San Diego):**

| Shipyard | Contract | Ship | Obligated | Ceiling |
|---|---|---|---|---|
| **BAE Systems San Diego Ship Repair** | N0002422C4420 | USS Essex (LHD 2) FY22 DSRA | $174M | $239M |
| **BAE Systems San Diego Ship Repair** | N0002420C4308 | USS Boxer (LHD 4) DSRA | $203M | $204M |
| **NASSCO** | N0002423C4404 | USS Makin Island (LHD 8) FY23 SRA | $75M | $101M |
| **NASSCO** | N0002418C4404 | USS Bonhomme Richard (LHD 6) DPMA | $221M | $221M |

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

> **Major finding:** The LHD/LSD/CG depot maintenance "primes" (BAE Systems
> Norfolk/San Diego, Metro Machine, NASSCO) are themselves subcontracting
> massive amounts to a hidden second tier of regional ship-repair specialists.
> This sub-tier ecosystem is invisible in FPDS but visible in USAspending
> subawards.

Aggregated across **12 LHD maintenance prime PIIDs** = **4,820 subaward records
totaling $3.57B** (2020-2026).

| Subcontractor | Subaward $ | Actions | Primes (count) | Role / Notes |
|---|---|---|---|---|
| **Propulsion Controls Engineering (PCE)** | **$942.3M** | 144 | 3 | Ship repair sub-prime -- propulsion systems |
| **Earl Industries** | **$932.5M** | 134 | 1 | Ship repair sub-prime (now part of BAE Norfolk) |
| **Marine Hydraulics International** | **$414.0M** | 261 | 1 | Norfolk-area ship repair sub-prime |
| **TECNICO Corporation** | $229.7M | 207 | 7 | Ship repair specialist (multi-yard) |
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

**Implications:**
- **Earl Industries** ($932M) is the historical core of BAE Norfolk Ship Repair (BAE acquired Earl in 2014); the sub records reflect intra-BAE work allocation but show the scale of BAE's Norfolk-based subcontracting.
- **Propulsion Controls Engineering (PCE)** at $942M is essentially a co-prime for propulsion overhaul work across multiple shipyards -- a major hidden player.
- **Marine Hydraulics International** at $414M spans multiple primes despite being known mainly as an LSD/DDG repair contractor.
- The "marine industrial base" in Hampton Roads is dramatically wider than the FPDS prime list suggests.

---

## 10. LCS -- Depot Maintenance & Modernization (~$1.3B)

### Platform Prime Contractors (Sustainment)

| Contractor | Parent | Role | Key Contract | Value |
|---|---|---|---|---|
| **Lockheed Martin Corporation** | LM | Freedom Variant prime / Design Agent | N6339419F0043, N6339424C0003 | $33.6M + $69M ceiling |
| **Textron Systems Corporation** | Textron | Independence Variant support | N0001923F2544 | $51M ceiling |
| **General Dynamics Mission Systems** | GD | Independence Variant ISEA | N6339424C0004 | $72M |

### Key Support Contracts

| Contractor | Contract | Value | Role |
|---|---|---|---|
| Booz Allen Hamilton | EH04 | $228M | PEO LCS Professional Support |
| Serco-IPS Corporation | EH11 | $190M | Program/Technical/Financial Support |
| Lockheed Martin | N6134023F0385 | $45.6M ceiling | LCS ITT-2A Lethality & Survivability Update |
| Innovative Professional Solutions | HR11 | $21M ceiling | LCS Mission Module Engineering |
| Applied Technical Systems | N6133122F3010 | $4.9M ceiling | LCS MVCS Support |
| Bowhead Professional Solutions | N0017817F3007 | $7.2M ceiling | LCS SUW Engineering |
| L-3 Communications | N0042118F0255 | $8.9M | Shipboard Terminals |
| Fincantieri Marine Systems NA | N4033924FF031 | $631K | Licensed Marine Engineer support |

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

> **Bombshell finding:** The Lockheed Martin LCS Freedom variant prime contract
> (N0002411C2300, "FY10 LCS Construction") subcontracts **$47.17 BILLION** to
> **Marinette Marine Corporation** (Wisconsin shipyard owned by Fincantieri).
> Marinette Marine is the actual builder of every Freedom-variant LCS hull.
> Lockheed Martin is effectively the systems integrator and prime of record;
> Marinette does the steel work. This was completely invisible in our prior
> FPDS prime search.

LCS / MCM mission module subcontractor totals across all relevant primes:

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **Marinette Marine** (Fincantieri) | **$47.17B** | 234 | LCS Freedom variant ship construction (sub to LM) |
| **Teledyne Defense Electronics** | $928.0M | 50 | Sub to NG Knifefish/LCS contract |
| **Teledyne Brown Engineering** | $715.1M | 158 | Complex forming, machine shop, assemblies |
| **General Dynamics Mission Systems** (as sub) | $607.8M | 70 | LCS Independence combat systems |
| **Rolls-Royce Marine North America** | $267.7M | 62 | LCS waterjets / propulsion |
| **Trident Sensors Limited** | $233.4M | 3 | Sensors |
| **Gibbs & Cox** | $207.1M | 87 | Naval architecture / engineering |
| **Airbus US Space & Defense** | $156.0M | 36 | Wave guide flanges |
| **Sparton DeLeon Springs** | $144.7M | 20 | ASW sensors / sonobuoys |
| **Northrop Grumman Systems** (as sub) | $136.8M | 76 | LCS Fathometer install kits, NAVDDS |
| **Fairlead Integrated** | $133.0M | 35 | Major systems / subsystems |
| **Renk Aktiengesellschaft** (Germany) | $91.0M | 18 | LCS gearing |
| **Coltec Industries** (Fairbanks Morse) | $59.6M | 9 | Diesel engines |
| **Arete Associates** | $56.8M | 43 | LCS sensors |
| **Nielsen Beaumont Marine** | $54.5M | 260 | Engineering services |
| **Meggitt Defense Systems** | $46.6M | 25 | Major subsystems |
| **Applied Physical Sciences Corp** | $28.0M | 8 | NRE engineering |
| **Ultra Electronics Ocean Systems** | $19.5M | 13 | Sub work to LCS contracts |
| **L3Harris Fuzing & Ordnance Systems** | $17.1M | 8 | Barracuda mine neutralizer ESAD |
| **Hensoldt** | $16.6M | 29 | LCS 23 onsite engineering |

---

## 11. LSD -- Depot Maintenance & Modernization (~$124M)

**Competed regionally among private shipyards.**

### Prime Shipyards

**West Coast:**

| Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|
| **NASSCO** | Various | USS Comstock (LSD 45) FY21 DSRA | $128M |
| **NASSCO** | Various | USS Harpers Ferry (LSD 49) FY20 DPMA | $118M |
| **NASSCO** | Various | USS Harpers Ferry (LSD 49) FY25 SRA | $67M |
| **BAE Systems San Diego** | Various | USS Comstock (LSD 45), USS Pearl Harbor (LSD 52) | $42M-$386M per avail |

**East Coast:**

| Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|
| **BAE Systems Norfolk** | Various | USS Tortuga (LSD 46) FY18 EDSRA/MODPRD | $259M |
| **BAE Systems Norfolk** | Various | USS Carter Hall (LSD 50) FY24 DSRA | $92M |
| **Metro Machine Corp** | Various | USS Oak Hill (LSD 51) FY25 DSRA | $142M |
| **Metro Machine Corp** | Various | USS Carter Hall (LSD 50) FY14 EDPMA | $704M |
| **Metro Machine Corp** | Various | USS Oak Hill / USS Whidbey Island MSMO | $502M |
| **Marine Hydraulics International** | Various | USS Gunston Hall (LSD 44) FY19 DSRA | $162M |

---

## 12. CG (Ticonderoga) -- Depot Maintenance & Modernization (~$160M)

**CG cruiser modernization (MODPRD) contracts tend to be very large due to scope of upgrades.**

### Prime Shipyards

| Shipyard | Contract | Ship | Ceiling |
|---|---|---|---|
| **BAE Systems Norfolk Ship Repair** | Various | USS Leyte Gulf (CG 55) | $663M |
| **BAE Systems Norfolk Ship Repair** | Various | USS Gettysburg (CG 64) FY18 MODPRD | $183M |
| **BAE Systems Norfolk Ship Repair** | Various | USS Vicksburg (CG 69) FY18 SSRA | $68M |
| **BAE Systems Hawaii Shipyards** | Various | USS Lake Erie (CG 70) DSRA | $549M |
| **Vigor Marine LLC** | Various | USS Chosin (CG 65) / USS Cape St. George (CG 71) FY20 MODPRD | $426M |
| **NASSCO** | Various | USS Cowpens (CG 63) FY18 MODPRD | $205M |
| **NASSCO** | Various | USS Lake Erie (CG 70) SRA | $62M |
| **HII** | Various | CG 47 Class Advanced Planning & Installation Support | $453M ceiling |

---

## 13. Standard Missile (WPN 2234 / ~$1B)

**Sole-source production program.**

### Prime Contractor

| Contractor | Parent | Role |
|---|---|---|
| **Raytheon Company** | RTX Corporation | Sole producer of SM-2, SM-3, SM-6 families |

### Key Contracts

| PIID | Obligated | Description |
|---|---|---|
| N0002407C6119 | $1.90B | Standard Missile 3 |
| N0002417C5410 | $292M | FY17-21 SM Production (US/FMS) |
| N0002413C5403 | $276M | FY13-17 SM Production (US/FMS) |
| N0002402C5319 | $227M | Standard Missile |
| N0002400C5390 | $211M | Standard Missile |
| N0002418C5407 | $128M | Standard Missile DLMF/ILM |

### Key Support

| Contractor | Role | Value |
|---|---|---|
| JHU Applied Physics Lab | Engineering & Evaluation | ~$29M total |
| Millennium Engineering & Integration | Aegis BMD / SM Technical Support | $30M ceiling |

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

Across **2 Standard Missile Raytheon prime PIIDs** (FY13-17 + FY17-21 production
contracts) = **1,128 subaward records totaling $301.8M**. Note: the SM-3 prime
contract N0002407C6119 returned 0 subawards (likely too old / pre-2020 reporting).

Major SM-program subcontractors are bundled in the broader weapons section
(see CIWS/SeaRAM batch totals). Standard Missile-specific significant subs include
the same propulsion/electronics tier as the CIWS family:

| Subcontractor | Role |
|---|---|
| **Aerojet Rocketdyne** | Solid rocket motors (SM-2, SM-3, SM-6) |
| **L3 Technologies** | Goods and services |
| **Honeywell International** | IMUs / IRUs (inertial guidance) |
| **Moog** | Actuators / control surfaces |
| **GE Aviation Systems** | DC-DC power supplies, electronic assemblies |
| **General Dynamics-OTS** | Bolts, contacts, gears, structural assemblies |
| **Curtiss-Wright DS** | Memory/PROM, multi-function assemblies |

---

## 14. DDG Mod (OPN BA1, Line 5 / ~$879M)

This line funds DDG-51 class modernization hardware/installation. Major contracts are embedded in the DDG-51 and DDG-1000 programs above. Key contractors involved in DDG modernization:

| Contractor | Role | Source |
|---|---|---|
| **Bath Iron Works** | Lead Design Yard / modernization planning | FPDS |
| **HII** | Installation support, planning | FPDS |
| **Lockheed Martin** | Aegis combat system upgrades | FPDS |
| **Raytheon** | Weapons system modernization | FPDS |
| **QED Systems** | Third-party planning | USAspending |

---

## 15. DDG 1000 Class Support Equipment (OPN BA1, Line 16 / ~$115M)

See DDG 1000 section (#4) above. Key contractors:

| Contractor | Role | Value |
|---|---|---|
| **Raytheon Company** | Mission Systems Equipment | $888M ceiling |
| **Bath Iron Works** | Planning Yard | $196M |
| **General Dynamics Land Systems** | MK 46 MOD 2 Gun Weapon System | $76.6M |
| **Microsoft Corporation** | Zumwalt Operating Environment (ZOE) | $9.4M |

---

## 16. MK-54 Torpedo Mods (WPN 3215 / ~$129M)

### Prime Contractors

| Contractor | Contract | Obligated | Ceiling | Role |
|---|---|---|---|---|
| **General Dynamics Mission Systems** | N0002425C6401 | $113.5M | **$791.9M** | MK 54 MOD 1 LWT Sonar Assembly Kits |
| **Ultra Electronics Ocean Systems** | N0002418C6405 | $134.1M | $324.1M | MK 54 MOD 0 Array Kits |

### MK 54 MOD 2 Development (OTA)

| Contractor | Contract | Obligated | Ceiling | Role |
|---|---|---|---|---|
| **Advanced Technology International** (consortium) | N666042090101 | $73M | $76.9M | MOD 2 Warhead Section Development |
| **Advanced Technology International** | N666042090119 | $134.2M | $134.4M | MOD 2 AUR Development |
| **Advanced Technology International** | N666042594201 | $27.9M | $256.1M | MOD 2 Inc 1 AUR Proof of Manufacturing |

### Key Support

| Contractor | Role | Value |
|---|---|---|
| Penn State Applied Research Lab | MOD 2 System Engineering & Testing | $36M + $29M ceiling |
| Lockheed Martin | MK-54 Capability | $2.6M |
| McLaughlin Research Corp | MK 32 / MK 54 Torpedo Tube Engineering | $23.5M ceiling |

### Top First-Tier Subcontractors (USAspending Subaward Deep Pull)

The GD Mission Systems MK 54 MOD 1 LWT Sonar Assembly Kits prime
(N0002425C6401) reports only **2 subawards totaling $25.0M** -- almost all the
production work is held in-house. Ultra Electronics MK 54 MOD 0 Array Kits
(N0002418C6405) reports **26 subawards totaling $12.1M**.

Combined with broader weapons batch:

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **DRS Network & Imaging Systems** | $232.5M | Sonar test equipment, tooling |
| **Ducommun Labarge Technologies** | $71.6M | RF cable assemblies, control actuation |
| **Lourdes Industries** | $50.9M | Hydraulic assemblies |
| **L3Harris Cincinnati Electronics** | $46.1M | Pedestals / gimbal platforms |
| **Southern Gear & Machine** | $44.5M | Precision-machined gears |
| **Coda Octopus Engineering** | $34.6M | AC-DC power supplies, cable assemblies |

---

## 17. LHA/LHD Midlife (OPN BA1, Line 8 / ~$123M)

See LHD section (#9) and LHA section (#8). Key midlife upgrade contractors:

| Contractor | Role | Source |
|---|---|---|
| **BAE Systems Norfolk / San Diego** | Hull, mechanical, electrical midlife work | FPDS |
| **Metro Machine Corp** | Midlife availability execution | FPDS |
| **Gibbs & Cox** | Electric plant control system engineering | FPDS |
| **Advanced Technology International** | LHD midlife electrical cabinet fabrication (OTA) | FPDS |
| **Amee Bay, LLC** | LHD midlife AIT | FPDS |

---

## 18. LPD Class Support Equipment (OPN BA1, Line 15 / ~$126M)

See LPD section (#5). Key contractors:

| Contractor | Role | Value |
|---|---|---|
| **Huntington Ingalls** | Class engineering and support services | $224.7M ceiling |
| **Raytheon Company** | Life Cycle Engineering & Support (electronics) | $485M ceiling |

---

## 19. Naval Strike Missile (WPN 2292 / ~$32M)

### Prime Contractors

| Contractor | Parent | Role | Contract | Value |
|---|---|---|---|---|
| **Raytheon Company** | RTX Corp | U.S. production integration prime | M6785422F1001 | $43.7M ceiling |
| **Kongsberg Defence & Aerospace** | Kongsberg | OEM / designer (Norwegian) | -- | (FMS channel, limited FPDS visibility) |

> Note: Kongsberg is the original equipment manufacturer of the NSM. Raytheon
> handles U.S. integration and production. The $32M FY2026 budget covers
> procurement of NSM Launch Units and Weapons Control Systems for LCS.

---

## 20. LCS In-Service Modernization (OPN BA1, Line 37 / ~$189M)

### Key Contractors

| Contractor | Role | Contract | Value |
|---|---|---|---|
| **Lockheed Martin** | Freedom Variant design agent & sustainment | N6339419F0043 | $33.6M ceiling |
| **Lockheed Martin** | Freedom Variant Combat System ISEA | N6339424C0003 | $69M ceiling |
| **General Dynamics Mission Systems** | Independence Variant In-Service Engineering | N6339424C0004 | $72M |
| **Textron Systems** | Independence Class Pre/Post-Deployment Support | N0001923F2544 | $51M ceiling |

---

## 21. LCS MCM Mission Modules (OPN BA1, Line 34 / ~$91M)

### Key Contractors

| Contractor | Role | Source |
|---|---|---|
| **Innovative Professional Solutions** | Mission Module Engineering & Technical Support | FPDS ($21M ceiling) |
| **JHU Applied Physics Lab** | Mission module testing/evaluation | USAspending ($10M) |
| **Lockheed Martin** | MCM module integration (embedded in LCS prime) | FPDS |

> Note: MCM mission modules include the AN/AQS-20 sonar, Remote Minehunting
> System (RMS), and Mine Neutralization System. Individual component contracts
> may be tracked under different descriptions in FPDS.

---

## 22. LCS Common Mission Modules Equipment (OPN BA1, Line 33 / ~$39M)

Common mission module infrastructure shared across MCM, SUW, and ASW packages.
Contractors overlap with LCS platform primes (Lockheed Martin, General Dynamics).

---

## 23. LCS SUW Mission Modules (OPN BA1, Line 36 / ~$4M)

### Key Contractors

| Contractor | Role | Contract | Value |
|---|---|---|---|
| **Bowhead Professional Solutions** | SUW Engineering Support | N0017817F3007 | $7.2M ceiling |

---

## 24. Surface Ship Torpedo Defense (OPN BA2, Line 2213 / ~$15M)

### Prime Contractors

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **SAIC** | N6660418F3013 | $31.3M | AN/SLQ-25D Nixie towed torpedo countermeasure system engineering |
| **Penn State University** | 0074 | $46.9M | CCAT (Canistered Countermeasure Anti-Torpedo Torpedo) development design agent |

### Known First-Tier Subcontractors

| Subcontractor | Prime | Amount | Role |
|---|---|---|---|
| **RTX BBN Technologies, Inc.** | SAIC | ~$9.2M (multiple) | AN/SLQ-25D Nixie engineering support |
| **Cardinal Engineering, LLC** | SAIC | ~$4.9M | SSTD Nixie UW/UDF Family of Systems |

---

## 25. Ship Gun Systems Equipment (OPN BA4, Line 5111 / ~$7M)

### Prime Contractor

| Contractor | Parent | Role |
|---|---|---|
| **BAE Systems Land & Armaments, L.P.** | BAE Systems | Sole producer of MK 110 MOD 0 (57mm) Naval Gun |

### Key Contracts

| PIID | Obligated | Ceiling | Description |
|---|---|---|---|
| N0002417C5375 | $56M | -- | 57MM MK 110 MOD 0 Gun Mount production |
| N0002412C5316 | $50.2M | $55.6M | MK 110 Naval Gun Procurement (USCG NSC) |
| N0002418F5302 | $7.7M | -- | MK 110 MOD 0 GWS Engineering Services |

---

## 26. Directed Energy Systems (OPN BA4, Line 5510 / ~$3M)

### Key Contractors (Navy-specific)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Penn State Applied Research Lab** | N0002423F8311 | $17.5M ceiling | HEL System Design/Dev/Fabrication/Test III |
| **Penn State Applied Research Lab** | N0002420F8329 | $7.2M ceiling | HEL System Design/Dev/Fabrication/Test II |
| **MZA Associates Corporation** | N0001421C1116 | $18.7M ceiling | Counter-UAS HEL Weapon System |
| **Advanced Technology International** | N001782190006 | $8.1M | CEBDS and HEL (OTA) |

### Key Contractors (Cross-service, relevant to Navy DE roadmap)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Dynetics, Inc.** | 0002 | $203M | IFPC HEL (Army) |
| **Raytheon Company** | FA86501999326 | $39.5M | Directed Energy Counter-UAS HELWS |
| **Lockheed Martin** | Multiple | ~$20M | HEL Pod, Panelized HEL Sources |
| **Radiance Technologies** | 0002 | $46.3M | HEL Integration & Demonstration |
| **Leidos, Inc.** | FA945118C0030 | $18.5M ceiling | High Energy Combinable Fiber Laser (FLARE) |

### Known First-Tier Subcontractors (Directed Energy)

| Subcontractor | Prime | Amount | Role |
|---|---|---|---|
| NOU Systems Inc | NTSI, LLC | $46.0M | MDA engineering/technical support |
| Modern Technology Solutions, Inc. | Radiance Technologies | $39.8M | Program mgmt, engineering |
| PeopleTec, Inc. | Radiance Technologies | $25.0M | Engineering, logistics |
| Koda Technologies Inc | Radiance Technologies | $20.1M | Engineering |
| **Lockheed Martin** | Radiance Technologies | $10.8M | Beam director assembly (DE MAC) |
| **nLIGHT Inc** | Radiance Technologies | $4.2M | High efficiency diode laser pump |
| Clemson University | University of Alabama Huntsville | $5.4M | Directed energy research |

---

## 27. Airborne MCM (OPN BA3, Line 119 / ~$10M)

No FPDS results were returned for airborne mine countermeasures searches across multiple
keyword variations. These contracts may be:
- Classified or restricted
- Indexed under different terminology (e.g., specific system designations)
- Embedded within broader helicopter/aviation platform contracts (MH-60S)

The Airborne MCM system includes the AN/AES-1 Airborne Laser Mine Detection System
(ALMDS) and AN/ASQ-235 Airborne Mine Neutralization System (AMNS). Prime contractors
historically include **Northrop Grumman** (ALMDS) and **Raytheon** (AMNS).

---

## 28. LCS Module Weapons (WPN 4221 / ~$2M)

Small weapons procurement line for LCS mission module weapons integration.
Limited FPDS visibility at this funding level.

---

## 29. Standard Missiles Mods (WPN 2356 / ~$32M)

Modifications and upgrades to Standard Missile inventory. Falls under the
Raytheon Standard Missile production and support contracts listed in section #13.

---

## 30. LSD Midlife & Modernization (OPN BA1, Line 40 / ~$4M)

Small modernization line for LSD class ships approaching end of service life.
See LSD depot maintenance section (#11) for shipyard contractors.

---

## Hidden Subcontractor Tier (USAspending Deep Pull, 2020-2026)

The deep subaward pull surfaced a "hidden tier" of major subcontractors that
don't appear as primes in any FPDS search. The most significant new findings:

| Subcontractor | Total Sub $ Identified | Primes | Programs |
|---|---|---|---|
| **Marinette Marine** (Fincantieri) | **$47.2B** | LM | LCS Freedom hull construction (essentially the actual builder) |
| **Earl Industries** (now BAE Norfolk) | **$932M** | BAE Norfolk | LHD ship repair |
| **Propulsion Controls Engineering** | **$942M** | BAE+Metro+NASSCO | Cross-yard propulsion overhaul |
| **MZA Associates** | **$395M** | LM Aculight | HELIOS beam control I&T |
| **Marine Hydraulics International** (as sub) | **$414M** | BAE Norfolk | Ship repair sub-prime |
| **Rolls-Royce Marine North America** | **$650M+** | HII + LCS | DDG/LCS propulsion (gas turbines, waterjets) |
| **L3 Technologies** | **$326M+** | LM Aculight + Raytheon | HELIOS software, CIWS |
| **Coltec Industries** (Fairbanks Morse parent) | **$200M+** | HII | LPD/LHA diesel propulsion |
| **TECNICO Corporation** | **$230M** | Multiple | Hampton Roads ship repair |
| **DRS Naval Power Systems** | **$228M+** | HII | DDG/LPD switchboards |
| **L3Harris Maritime Power & Energy Solutions** | **$226M+** | HII | DDG/LPD power conversion |
| **York International** (Johnson Controls) | **$237M+** | HII | DDG/LPD HVAC |
| **General Electric** | **$197M** | HII | LM2500 main propulsion gas turbines |
| **SOCAIL, LDA** (Portugal) | **$151M** | HII | Foreign-sourced gas turbine engines |
| **Northrop Grumman Systems** (as sub) | **$260M+** | HII + LCS | Steering systems, electronics |
| **IMIA** (paint/coatings) | **$179M** | Multiple ship repair | Hull coatings |
| **EMS Industrial** | **$118M** | Multiple ship repair | Industrial services |
| **DRS Network & Imaging Systems** | **$233M** | Raytheon CIWS | Test equipment, tooling |

> The "hidden tier" represents thousands of small-to-medium-sized firms that
> collectively perform multi-billion-dollar share of Navy modernization work
> but are invisible to anyone searching FPDS for prime contracts.

---

## Summary: Top Prime Contractors Across All SAM Programs

| Contractor | Parent Company | Programs | Estimated Combined Value |
|---|---|---|---|
| **Huntington Ingalls Industries** | HII | DDG-51 construction, LPD Flight II (sole), LHA (sole), DDG-1000 mod planning, CG planning | $25B+ |
| **Bath Iron Works** | General Dynamics | DDG-51 construction + lead yard, DDG-1000 (sole shipbuilder) | $15B+ |
| **Raytheon Company** | RTX Corporation | Standard Missile (sole), DDG-1000 mission systems, NSM integration, LPD electronic systems | $5B+ |
| **BAE Systems** (multiple divisions) | BAE Systems plc | DDG/LHD/LPD/LSD/CG depot maintenance (Norfolk, San Diego, Jacksonville, Hawaii), MK 110 gun | $5B+ |
| **Lockheed Martin** | Lockheed Martin | DDG-51 Aegis combat system, LCS Freedom variant prime | $1.5B+ |
| **Metro Machine Corp** | -- | LHD/DDG/LSD depot maintenance (Norfolk) | $1B+ |
| **General Dynamics Mission Systems** | General Dynamics | LCS Independence ISEA, MK-54 torpedo production | $900M+ |
| **NASSCO** | General Dynamics | LHA/LHD/LSD/DDG/CG depot maintenance (San Diego) | $800M+ |
| **Vigor Marine LLC** | -- | DDG/CG depot maintenance (Portland, OR) | $500M+ |
| **SAIC** | SAIC | DDG-1000 engineering, SSTD Nixie, torpedo defense | $300M+ |
| **Textron Systems** | Textron | LCS Independence variant support | $50M+ |
| **Penn State Applied Research Lab** | Penn State Univ | MK-54 MOD 2 engineering, HEL development, CCAT | $130M+ |
| **JHU Applied Physics Lab** | Johns Hopkins | DDG-1000 combat system RDT&E, Standard Missile evaluation | $50M+ |
| **Advanced Technology International** | -- | OTA consortium manager: MK-54 MOD 2, HEL, LHD midlife | $250M+ |
| **Continental Maritime of San Diego** | -- | DDG depot maintenance (San Diego) | $300M+ |
| **Marine Hydraulics International** | -- | DDG/LSD depot maintenance (Norfolk) | $300M+ |
| **QED Systems** | -- | Third-party planning (DDG, CG, LPD, LHD) | $300M+ |
| **BAE Systems Land & Armaments** | BAE Systems plc | MK 110 57mm gun production | $110M+ |

---

## Data Sources & Methodology

- **FPDS Atom Feed** (https://www.fpds.gov): Primary source for prime contracts.
  Searched DESCRIPTION_OF_REQUIREMENT with program-specific keywords, filtered by
  AGENCY_CODE 1700 (Navy) and SIGNED_DATE ranges. Parsed all three record types
  (award, OtherTransactionAward, OtherTransactionIDV).
- **USAspending API -- spending_by_award** (https://api.usaspending.gov): Used for
  prime award lookup by PIID and aggregated views.
- **USAspending API -- subawards endpoint**: For each major prime PIID identified
  via FPDS, looked up the `generated_internal_id` via `/api/v2/search/spending_by_award/`
  and then called `POST /api/v2/subawards/` with `award_id={generated_internal_id}`
  to pull the **complete subaward tree** (up to 1,000 records per prime). This
  gave deep first-tier subcontractor data that the keyword-based subaward search
  doesn't surface. Cross-referenced ~75 major prime PIIDs.
- **SAM.gov**: Skipped (unreliable per operational guidance).
- **Post-filtering**: Results filtered for relevance to specific program descriptions.
- **Deduplication**: By PIID for FPDS, Award ID for USAspending.
- **Subaward time window**: 2020-01-01 to 2026-09-30 (per user direction).

### Known Limitations

1. **Subcontractor data is incomplete.** Only first-tier subs on contracts >$30K are publicly
   reported, and coverage is inconsistent. Major subcontractors (e.g., propulsion, electronics,
   C4I systems providers) doing hundreds of millions in work are likely invisible.
2. **Classified programs** are excluded from all public databases.
3. **OTA awards** through consortia (e.g., ATI, NSTXL) may list the consortium rather than the
   performing company.
4. **Airborne MCM** returned zero FPDS results across all keyword variations -- likely classified
   or indexed under non-obvious descriptions.
5. **Reporting lag**: FPDS data has a 30-90 day lag. Very recent awards may not appear.
6. **OMN maintenance contracts** (the bulk of SDM spend) are individual ship availabilities
   competed among qualified shipyards. The specific FY2026 availability awards may not yet
   be in FPDS if they haven't been signed.

---

*Generated 2026-04-09. Subaward sections updated 2026-04-10 with deep PIID-by-PIID
USAspending subaward pull (~75 prime contracts, ~25,000 subaward records,
2020-2026 window).*
