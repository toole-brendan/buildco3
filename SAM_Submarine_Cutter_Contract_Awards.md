# FY2026 SAM Programs -- Submarine & USCG Cutter Award Analysis (FY2020-2026)

Companion to `SAM_Program_Contract_Awards.md` and `SAM_Program_Component_Contracts.md`.
Covers the **submarine and USCG cutter** sections that were added to the SAM sheet
in version 1.9 (April 2026).

**Scope:** Award data only (no engineering/logistics narrative). FY2020-2026
signed-date window. Both prime contractors and first-tier subcontractors.

**Data sources:**
- **FPDS Atom Feed** -- Prime contracts (`SIGNED_DATE:[2020/01/01,2026/12/31]`)
- **USAspending /api/v2/subawards/** -- First-tier subaward tree per prime PIID
  (looked up via `generated_internal_id` from `/api/v2/search/spending_by_award/`)

**SAM hulls in scope (from Excel rows 125-196):**

| Hull | Class | FY26 SAM ($K) | Prime / OEM |
|---|---|---|---|
| **SSN** | Virginia (SSN-774) | 17,605,524 | General Dynamics Electric Boat (+ HII Newport News teaming) |
| **SSBN** | Columbia (SSBN-826) | 13,525,977 | General Dynamics Electric Boat (+ HII Newport News teaming) |
| **SSGN** | Ohio (SSGN-726) | 225,151 | (sustainment only -- retiring) |
| **WAGB** | Polar Security Cutter | 130,000 | Bollinger Mississippi Shipbuilding (acq. VT Halter Marine Nov 2022) |
| **WCC** | Waterways Commerce Cutter | 98,000 | Birdon America Inc |
| **WMSL** | National Security Cutter (Legend) | 31,000 | HII Ingalls Shipbuilding (sustainment) |
| **WMSM** | Offshore Patrol Cutter (Heritage) | 812,400 | Eastern Shipbuilding Group (Stage 1) + Austal USA (Stage 2) |
| **WPC** | Fast Response Cutter (Sentinel) | 216,000 | Bollinger Shipyards Lockport |

> **⚠️ IMPORTANT -- Cumulative vs. Window Dollars:** The "Obligated" amounts in
> the prime tables below are the **cumulative `totalObligatedAmount` value at
> the latest mod in our FY20-26 window**, NOT the sum of new obligations
> committed inside the window. Many of these contracts pre-date 2020 and were
> already at huge values when the window opened.
>
> **Where this matters:** A contract showing "$34.66B obligated" with latest
> mod 2025-12-23 might have only added ~$200M of NEW money inside the window
> (the rest was committed in 2017-2019). Per-mod analysis shows three patterns:
>
> 1. **Pre-window contracts (mostly inactive in window):** N0002417C2100,
>    N0002412C2115, N0002409C2104. The cumulative number reflects mostly
>    pre-2020 activity.
> 2. **Window-only contracts (fully attributable):** N0002424C2114 (Bechtel
>    S9G $2.54B), N0003019C0100, N0003020C0100, N0003023C0100 (Trident FY20/21/24
>    $1.1-1.2B each), N0002424C2110 (Block VI LLTM $4.96B). All money is window-real.
> 3. **Window-straddling contracts (partial delta):** N0002417C2117 (Columbia,
>    grew from $13.6B to $24-30B in window — true delta ~$11-17B),
>    N0002419C2115 (Bechtel Columbia industrial base, true delta ~$1.4B),
>    N0002419C2210 (Polar Security Cutter, true delta ~$1.3B), HSCG2316CAFR625
>    (FRC Bollinger, true delta ~$300-500M).
>
> **For market-sizing purposes,** treat the cumulative numbers as "the size of
> the active contract vehicle" rather than "FY20-26 spend." For year-by-year
> spend attribution, you'd need per-mod delta analysis -- see Section 21
> ("How to map FY26 SAM lines to specific contract vehicles") for the
> walkthrough.

> **Note on subaward visibility:** Subawards reported here come from
> USAspending's `/api/v2/subawards/` tree. Newer prime contracts (FRC post-2016,
> Polar Security Cutter, Arctic Security Cutter, Bollinger Mississippi/Lockport
> contracts, Birdon WCC, Austal OPC Stage 2) **report 0 subawards** -- this is
> a known reporting gap, not an absence of subcontracting activity. Where
> primes don't report subs, the subcontractor list is built from FPDS-visible
> direct DoD/USCG contracts to known component vendors.

> **Block / Build terminology** (read this before the Virginia & Columbia
> sections):
>
> Submarine procurement uses **block** (Virginia) or **build** (Columbia) to
> group multi-year buys. Each block/build is funded under its own multi-year
> procurement (MYP) authorization from Congress and gets its own master
> contract vehicle.
>
> **Virginia class blocks:**
> | Block | Hulls | Years | Boats | Active in window? |
> |---|---|---|---|---|
> | Block I | SSN 774-779 | FY99-03 | 6 | (closed out) |
> | Block II | SSN 780-785 | FY04-08 | 6 | residual mods only |
> | Block III | SSN 786-791 | FY09-13 | 6 | residual mods only |
> | Block IV | SSN 792-801 | FY14-18 | 10 | construction ongoing |
> | Block V | SSN 802-811 | FY19-23 | 9 (5 with VPM) | **active construction** |
> | Block VI | SSN 812-820 | FY24-28 | 9 planned | **early/LLTM phase** |
>
> **Columbia class builds:** Build I = SSBN 826 (USS District of Columbia,
> lead boat), Build II = SSBN 827 (USS Wisconsin). Both under construction.
>
> **PIID does not equal block.** A PIID's year prefix (e.g. `N00024-17-C-2100`)
> reflects when NAVSEA assigned the contract number, not which block it
> funds. Some master construction PIIDs span multiple blocks via mods.
> The only reliable way to identify a block is to read the **mod descriptions**,
> which often reference specific hull numbers (e.g., "SSN 812 CONSTRUCTION
> (BOAT 2, FY 24)" → Block VI second boat).

---

## Table of Contents

### Submarines
1. [SSN Virginia Class -- New Construction](#1-ssn-virginia-class--new-construction)
2. [SSBN Columbia Class -- New Construction](#2-ssbn-columbia-class--new-construction)
3. [Naval Reactors -- Bechtel Plant Machinery](#3-naval-reactors--bechtel-plant-machinery)
4. [SSN/SSBN Sonar, Acoustic & Combat Systems](#4-ssnssbn-sonar-acoustic--combat-systems)
5. [Submarine Periscope / Photonics Mast](#5-submarine-periscope--photonics-mast)
6. [Submarine Communications](#6-submarine-communications)
7. [TRIDENT II D5 Strategic Weapons System](#7-trident-ii-d5-strategic-weapons-system)
8. [Strategic Missile Systems Equipment (SSBN)](#8-strategic-missile-systems-equipment-ssbn)
9. [MK-48 Heavyweight Torpedo](#9-mk-48-heavyweight-torpedo)
10. [Conventional Prompt Strike (CPS) -- SSN Hypersonic](#10-conventional-prompt-strike-cps--ssn-hypersonic)
11. [SSN/SSBN Depot Maintenance](#11-ssnssbn-depot-maintenance)

### USCG Cutters
12. [Polar Security Cutter (WAGB)](#12-polar-security-cutter-wagb)
13. [Arctic Security Cutter / CAPI -- New Programs](#13-arctic-security-cutter--capi--new-programs)
14. [Offshore Patrol Cutter (WMSM)](#14-offshore-patrol-cutter-wmsm)
15. [Fast Response Cutter (WPC)](#15-fast-response-cutter-wpc)
16. [National Security Cutter (WMSL) -- Sustainment](#16-national-security-cutter-wmsl--sustainment)
17. [Waterways Commerce Cutter (WCC)](#17-waterways-commerce-cutter-wcc)
18. [NSC Unmanned Aircraft Systems](#18-nsc-unmanned-aircraft-systems)

### Cross-Cutting
19. [Summary: Top Primes & Subs Across All Programs](#19-summary-top-primes--subs-across-all-programs)
20. [Methodology & Limitations](#20-methodology--limitations)
21. [How to Map FY26 SAM Lines to Specific Contract Vehicles](#21-how-to-map-fy26-sam-lines-to-specific-contract-vehicles)

---

# SUBMARINES

## 1. SSN Virginia Class -- New Construction

**Sole-source team build by General Dynamics Electric Boat (Groton, CT) with
Huntington Ingalls Newport News Shipbuilding (Newport News, VA) as teaming
partner.** EB is prime of record on all SCN 2013 contracts; HII NNS work flows
through EB via the SSN team agreement (visible only in subaward records, not as
separate FPDS primes).

### Active Construction Contract Vehicles by Block

The Virginia program has multiple parallel master contract vehicles. Block
identification is based on the **boat hull numbers** referenced in mod
descriptions, not the PIID year prefix.

| PIID | Contractor | Cumulative Obligated (latest mod) | Ceiling | Block(s) | Evidence (mod desc) |
|---|---|---|---|---|---|
| **N0002412C2115** | GD Electric Boat | **$19.90B** | $19.93B | **Block IV** (SSN 792-801, 10 boats) | "VIRGINIA CLASS SUBMARINE BLOCK IV CONSTRUCTION"; "SSN 792 CONSTRUCTION (BOAT 1, FY14)" |
| **N0002417C2100** | GD Electric Boat | **$34.94B** | **$40.78B** | **Block V → Block VI** (multi-block master vehicle) | "DIVERT BLOCK V FOUNDATIONS" (early mods); "SSN 812 CONSTRUCTION (BOAT 2, FY 24)" (latest mod 2026-01-06) |
| **N0002424C2110** | GD Electric Boat | **$4.96B** | **$5.13B** | **Block VI LLTM** (long-lead time material) | "SSN 814 LONG LEAD TIME MATERIAL" (4th Block VI hull) -- contract awarded Dec 2023 |
| **N0002409C2104** | GD Electric Boat | $16.24B | $21.96B | **Block II** (residual / closing out) | "NO COST GOVERNMENT PROPERTY TRANSFER FROM THIS CONTRACT TO THE BLOCK V CONTRACT" -- being mined for parts |

### Virginia Payload Module (VPM) Component Contracts

VPM is the 84-foot midbody insert that carries Tomahawk and CPS hypersonic
weapons on Block V boats. VPM components are funded through separate
contract vehicles that appear in FPDS only via component-keyword search.

| PIID | Contractor | Cumulative Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **N0002416C2111** | GD Electric Boat | **$1.47B** | $1.57B | 2023-09-20 | VPM Ventilation Valve (FY16 award) |
| **N0002410C2118** | GD Electric Boat | **$1.42B** | $1.51B | 2023-03-20 | VPM Tube Fabrication (FY10 award, oldest VPM contract) |
| 0768 | Redstone Defense Systems | $9.6M | $16.1M | 2023-04-27 | VPT/VPM Support Equipment AUR |
| 0764 | Redstone Defense Systems | $4.2M | $13.2M | 2022-06-27 | VPT/VPM Support Equipment Center Cell |
| N4008525F0844 | Benaka Inc. | $3.2M | $3.2M | 2025-09-22 | Construction project for VPT area Building 1246 |

### Virginia Sustainment, Modernization & Combat Systems

| PIID | Contractor | Cumulative Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N0002419C2125** | GD Electric Boat | $1.37B | $1.39B | Virginia Class Block I-III HPADs (high pressure air dehydrators) backfit |
| **N0002420C4312** | GD Electric Boat | $1.33B | $1.36B | **USS Hartford (SSN 768) Engineered Overhaul (EOH) execution** -- depot, not new construction |
| **N0002410C6266** | Lockheed Martin | $899M | $1.37B | Virginia Class Combat Systems Hardware/Software |
| N666042291204 | Advanced Technology International (OTA consortium) | $90M | $228M | Code 25 Mission Electronic Subsystem -- Modified Virginia (subsea/seabed warfare) |
| **N0002421C4106** | BAE Systems Land & Armaments | $85M | $86M | **SSN 812 Forward Subassembly** (Block VI hull components) |
| N0016723F0083 | BAE Systems Land & Armaments | $23M | $27M | SSN 812 Forward Assembly Material |
| N0002421C4111 | Rolls-Royce Marine North America | $29M | $37M | Virginia Class Submarine Rotor |
| N4215822FST01 | International Marine & Industrial Applicators | $34M | $34M | Virginia Class Submarine Preservation |

> **The N0002417C2100 puzzle:** This PIID has the Year-17 prefix, suggesting
> it was originally awarded in FY17 -- but mod descriptions span Block V
> ("DIVERT BLOCK V FOUNDATIONS") through Block VI ("SSN 812 CONSTRUCTION
> (BOAT 2, FY 24)"). The most likely interpretation is that NAVSEA established
> a master construction contract in FY17 for component/long-lead funding and
> has been amending it ever since to add scope for newer boats. The latest
> mod (2026-01-06) ties it to SSN 812, the second Block VI boat. The
> $34.94B cumulative reflects ~9 years of accumulated construction work.

### Top First-Tier Subcontractors (USAspending Subaward Pull)

**N0002417C2100 (Virginia Block V→VI master vehicle) -- 2,000+ subaward records, $4.14B (capped at API limit):**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **Northrop Grumman Systems** | **$1.27B** | 25 | Sonar, electronics, mission systems |
| **BAE Systems Land & Armaments** | **$355M** | 18 | Propulsors, weapons handling |
| **Curtiss-Wright Electro-Mechanical** | $239M | 80 | Motors, valves, stators |
| **DC Fabricators** | $205M | 45 | Hull structures, fabrication |
| **Globe Composite Solutions** | $197M | 56 | Composite materials |
| **Scot Forge Company** | $145M | 184 | Forgings (shafts, structural) |
| **Johnson Controls Navy Systems** | $80M | 15 | HVAC / chilled water |
| **Teledyne Instruments** | $78M | 51 | Instrumentation |

**N0002412C2115 (Virginia Block IV MYP) -- 1,622 subs, $234M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| Northrop Grumman Systems | $15M | Sonar / electronics |
| Stryten Energy | $13M | Submarine batteries |
| Jamestown Metal Marine Sales | $12M | Marine hardware distribution |
| VACCO Industries | $11M | Fluid system components |
| GD Mission Systems | $8M | Combat systems (intra-GD) |
| L3 Technologies | $6M | Electronics |

**N0002419C2125 (Virginia Tech Instructions) -- 1,292 subs, $241M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| Northrop Grumman Systems | $57M | Tech-instruction-driven hardware |
| CIRCOR Naval Solutions | $14M | Marine valves |
| L3 Technologies | $9M | Electronics |
| KSARIA Corporation | $7.6M | Fiber optic interconnects |
| Collins & Jewell Company | $7.8M | Hatches, doors, openings |

> **HII Newport News work on Virginia class:** HII NNS does ~50% of Virginia
> hull construction work as the team partner. This work flows through EB as
> the prime; HII NNS does not appear as a direct DoD prime on Virginia
> contracts in FPDS. The HII labor share is captured inside the EB prime
> obligations above.

---

## 2. SSBN Columbia Class -- New Construction

**Sole-source team build by General Dynamics Electric Boat (lead) with
Huntington Ingalls Newport News Shipbuilding as teaming partner.** Same team
structure as Virginia class.

### Active Construction Contract Vehicles

| PIID | Contractor | Cumulative Obligated (latest mod) | Ceiling | Build(s) | Evidence (mod desc) |
|---|---|---|---|---|---|
| **N0002417C2117** | GD Electric Boat | **$24.21B - $30.83B** (varies by mod -- climbing fast) | **$42.18B** | **Build I + Build II** (SSBN 826 USS District of Columbia + SSBN 827 USS Wisconsin) | "MOUNTING BOX PROCEDURE CHANGE SSBN 826/827"; "ADDITIONAL SUPPLIER DEVELOPMENT AND CLASS LEAD YARD SUPPORT" (Jun 2025); "FUNDING ACTION ONLY" (Dec 2025) |
| **N0002413C2128** | GD Electric Boat | $3.07B | $3.13B | Columbia design (predecessor) | "COLUMBIA CLASS DESIGN DRAWING REVISIONS" |
| **N0002411C2109** | GD Electric Boat | $480M | $845M | SSBN-R concept formulation | "SEA073R SSBN REPLACEMENT CONCEPT FORMULA" |

### Columbia Support / R&D

| PIID | Contractor | Cumulative Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0001419C1002 | GD Electric Boat | $53M | $98M | Tech transition for Virginia & Columbia |
| N0002419F8435 | Penn State University ARL | $18M | $19M | Columbia Class Propulsor & Shafting Support FY19-22 |
| N0001423C1015 | Applied Physical Sciences Corp | $18M | $30M | Navy Supporting Tech for Virginia & Columbia + Next Gen |
| N0016725F0080 | BAE Systems Land & Armaments | $12M | $12M | Columbia Class Bearing Support Structure Assembly |
| N0016719F0074 | Seemann Composites | $9M | $9M | Columbia Class Component Full Scale Demo |
| N0002423F8296 | JHU Applied Physics Lab | $8M | $10M | Columbia Class Testing Program |

> **The Columbia value moves fast.** When I first pulled this contract on
> 2026-04-09 it showed $13.59B cumulative. A second pull on 2026-04-10 caught
> mods up to $24.21B and $30.83B depending on which mod was the latest at
> the moment of query. The contract is receiving billion-dollar mods on a
> roughly monthly cadence as Build I + Build II construction ramps. Use the
> $42.18B ceiling as the more stable "size of vehicle" reference.

### Top First-Tier Subcontractors

**N0002417C2117 (Columbia Build I + II) -- 2,000+ subaward records, $8.11B (capped at API limit):**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **BlueForge Alliance** | **$4.21B** | 7 | Submarine Industrial Base (SIB) consortium -- workforce, supplier development, capacity expansion across the entire sub supply chain |
| **Northrop Grumman Systems** | **$669M** | 32 | Combat / sonar / mission systems |
| **DRS Naval Power Systems** | **$403M** | 24 | Switchboards, power distribution |
| **Curtiss-Wright Electro-Mechanical** | $176M | 70 | Motors, valves, stators |
| **Babcock Marine (Rosyth, UK)** | $172M | 6 | UK strategic-deterrent partner -- propulsion components |
| **Scot Forge Company** | $171M | 132 | Forgings |
| **APCO Technologies SA (Switzerland)** | $131M | 31 | Launch tube structural components |
| **Rhoads Metal Fabrications** | $124M | 42 | Hull/structural fab |

> **BlueForge Alliance** is the single largest sub at **$4.21B** -- this is
> the Submarine Industrial Base (SIB) workforce and supplier development
> initiative funded through the Columbia program. BlueForge is a non-profit
> consortium based in College Station, TX that channels SIB funds to ~10,000+
> small/mid suppliers, training programs, and welding workforce development.
> It's effectively a pass-through for SIB grants and is the dominant "vendor"
> on the Columbia subaward tree.

**N0002413C2128 (Columbia Design Drawings) -- 608 subs, $274M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| Babcock Marine (Rosyth, UK) | $68M | UK design partner |
| BWXT Nuclear Operations Group | $18M | Reactor components |
| Lockheed Martin | $17M | Combat system / fire control |
| APCO Technologies SA | $14M | Launch tube design |
| Waukesha Bearings | $13M | Propulsion bearings |
| GD Mission Systems | $13M | Combat systems |
| CP Industries Holdings | $10M | Pressure vessels |

> **HII Newport News on Columbia:** Same as Virginia -- HII NNS does ~22% of
> Columbia hull construction as a team partner; the work flows through EB.

---

## 3. Naval Reactors -- Bechtel Plant Machinery

**Sole-source for naval nuclear reactor plant components.** BPMI is a Naval
Reactors prime that ships components for both Virginia and Columbia hulls.
Funded through SCN component lines and NWCF (National Sea Base Deterrence Fund).

### Prime Contracts (FY20-26 obligations)

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N0002419C2114** | Bechtel Plant Machinery | **$3.38B** | $3.66B | Naval Reactor Components (Columbia) |
| **N0002419C2115** | Bechtel Plant Machinery | **$3.00B** | $3.00B | Columbia Class Industrial Base Increase |
| **N0002416C2106** | Bechtel Plant Machinery | $2.71B | $2.71B | Naval Reactor Components |
| **N0002424C2114** | Bechtel Plant Machinery | $2.54B | $2.54B | FY26 Virginia Class Component Funding |
| **N0002424C2115** | Bechtel Plant Machinery | $2.03B | $2.37B | Reactor Components |
| **N0002412C2106** | Bechtel Plant Machinery | $1.32B | $1.32B | OPN Reactor Components |
| **N0002407C2102** | Bechtel Plant Machinery | $1.18B | $1.20B | Reactor Components |
| **N0002419C2112** | Bechtel Plant Machinery | $1.05B | $1.05B | Reactor Components |
| **N0002413C2121** | Bechtel Plant Machinery | $662M | $662M | Reactor Components |
| **N0002417C2110** | Bechtel Plant Machinery | $621M | $621M | Reactor Components |

### Top First-Tier Subcontractors

**N0002419C2115 (Columbia Industrial Base / Bechtel) -- 67 subs, $528M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **BWXT Nuclear Operations Group** | **$272M** | Reactor cores, fuel modules (Lynchburg, VA) |
| DRS Naval Power Systems | $56M | Reactor instrumentation power |
| **BWX Technologies** | $53M | Reactor pressure vessels (Mt. Vernon, IN) |
| Curtiss-Wright Electro-Mechanical | $42M | Reactor coolant pumps |
| Taylor Forge Engineered Systems | $21M | Pressure vessel forgings |
| Curtiss-Wright Flow Control | $14M | Valves |
| Peerless Instrument | $14M | Reactor instrumentation |
| Power Paragon | $11M | Switchgear |

> **BWXT** is the dominant Naval Reactors second-tier prime: it manufactures
> the actual nuclear reactor cores, fuel modules, and pressure vessels for
> every U.S. Navy submarine and aircraft carrier. BWXT also has direct DOE/NNSA
> prime contracts (`89233125FNA400743`, `89233123FNA400535`,
> `89303318CEM000007`) for HALEU production and uranium operations totaling
> $1.7B+ in the FY20-26 window.

---

## 4. SSN/SSBN Sonar, Acoustic & Combat Systems

Funded through OPN BA1 (Submarine Support Equipment, Periscope, Virginia Class
Support Equipment), OPN BA2 (Submarine Acoustic Equipment, Acoustic Warfare,
Comm), and OPN BA4 (SSN Combat Control Systems).

### Prime Contracts -- Acoustic / Sonar

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0016721F3010 | ManTech Advanced Systems Intl | $43M | $51M | Submarine & Surface Ship Acoustic Signature E&T Support |
| N0016721F3000 | General Dynamics IT | $35M | $50M | Acoustic Research Detachment scientific/eng support |
| N6660420F3011 | Purvis Systems | $4M | $7M | Submarine defense systems |
| N666042494110 | Advanced Technology International (OTA) | $2M | $3M | Upgraded Acoustic Positioning System (APS) for Submarine Rescue |
| N6660420DH001 | Mikel, Inc. | -- | $41M | Submarine Acoustic Navigation System |
| N6660420FH002 | Mikel, Inc. | $1M | $1M | Submarine Acoustic Navigation System |

### Prime Contracts -- Submarine Combat Control / BYG-1

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N6660420F3007** | Northrop Grumman Systems | $30M | $56M | Sub Combat System & Surface Ship Trainer software / SUWET |
| N0002417C6417 | Lockheed Martin | $9M | $13M | Brazil Sub Integrated Combat System Modernization |
| N5005418F3002 | Amentum Services | $8M | $12M | MARMC Submarine Combat Systems Tech Support |
| N5005418F3000 | L-3 Unidyne | $8M | $11M | MARMC Submarine Combat Systems |
| N0025324F0052 | Laurel Technologies Partnership | $4M | $4M | TIH 26 Combat Control & Sonar |
| 0017 | DRS Laurel Technologies | $7M | $7M | TIH 16 Production SSBN BYG-1 Hull #3 |

### Subaward Detail

**N6660420F3007 (NG Sub Combat Trainer) -- 119 subs, $64M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| Rite-Solutions, Inc. | $27M | Combat system software |
| Knight Federal Solutions | $26M | Trainer engineering |
| Insight Global | $7M | Staffing |

**N0016721F3000 (GDIT Acoustic Research) -- 29 subs, $21M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| ManTech Advanced Systems Intl | $6M | Acoustic engineering (cross-prime work) |
| Cosmic Software Technology | $5M | Software |
| Premier Technology | $5M | Test infrastructure |

---

## 5. Submarine Periscope / Photonics Mast

The "submarine periscope" is now a non-penetrating photonics mast (Type-18 /
Type-M1 family). Sustainment is fragmented across L3Harris (formerly Kollmorgen),
DRS Network & Imaging, GDIT, Leidos, and L-3 Communications.

### Prime Contracts (FY20-26 obligations)

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| SPRRA220F0132 | DRS Network & Imaging Systems | $43M | $43M | DLA Periscope Head Assembly Spares |
| SPRRA225F0038 | DRS Network & Imaging Systems | $36M | $36M | Periscope Head Assembly NSN 1240014424825 |
| 1601 (HQ085200D0001) | Leidos | $31M | $32M | Synthetic Signature Modeling/Sim of Periscope Systems |
| SPRRA219C0018 | DRS Network & Imaging Systems | $20M | $20M | Periscope Head Assembly |
| N6660418F3017 | GDIT | $16M | $18M | Periscope Mechanical/Electronic/Optical Repair Support |
| N0010416CFA16 | L-3 Communications | $12M | $12M | Periscope Outer Tube |
| N439 | GDIT | $10M | $10M | Periscope Mechanical/Electronic/Optical Repair Support |
| SPRRA224F0082 | DRS Network & Imaging Systems | $5M | $5M | Periscope Head Assembly |
| N0002425F8300 | Penn State Univ | $2M | $3M | Type-M1 Periscope Prototype Design |
| N4425524F4394 | Rogers, Lovelock & Fritz | $2M | $6M | P434 SSBN Regional Periscope & Photonics Mast Repair Center, NBK |

> **L3Harris (Kollmorgen photonics mast prime):** L3Harris is the OEM of the
> Type-18 photonics mast on Virginia/Columbia, but the production work flows
> through the Electric Boat Virginia/Columbia prime contracts (subaward
> records confirm L3 Technologies on those PIIDs at $6-9M per contract).
> L3Harris's direct DoD photonics mast contracts in the FY20-26 window are
> minimal -- almost all of the photonics mast volume is captured inside the
> EB prime.

---

## 6. Submarine Communications

Funded through OPN BA2 Lines 3107 (Submarine Broadcast Support) and 3130
(Submarine Communication Equipment).

### Prime Contracts -- Fixed Submarine Broadcast System (FSBS)

| PIID | Contractor | Obligated | Description |
|---|---|---|---|
| N6523626F0003 | Salient CRGT | $12M | FSBS Transmitter Control Console / Antenna Matching |
| N6600118F1425 | AECOM Technical Services | $5M | FSBS In-Service Engineering Activity (ISEA) |
| N6523621F0770 | Hi-Q Engineering | $5M | FSBS hardware |
| N6523621F0190 | Hi-Q Engineering | $2M | FSBS hardware |
| N6600123F0833 | Long Wave Inc | $1M | FSBS ISEA: Holt/Bushing |
| N6600122F0184 | AECOM Technical Services | $1M | FSBS ISEA support |
| N6523624F0172 | Salient CRGT | $1M | FSBS Tube to Solid Requirements Doc |

### Prime Contracts -- Submarine Communication Code 34

| PIID | Contractor | Obligated | Description |
|---|---|---|---|
| N6660417F3007 | Research & Development Solutions | $34M | Code 34 Sub Comm Systems Engineering & Tech Support |
| N5005417F3002 | Amentum Services | $14M | Submarine Electronic Surveillance Fleet Tech Assistance |
| N6660420F3008 | Precise Systems | $12M | Sub Code 34 Electromagnetic, Imaging, Antenna |
| N6449824F3097 | Noblis MSD | $8M | Submarine Communication |
| N6449823F4000 | NDI Engineering | $2M | Hull Mechanical & Electrical Verification Test Support |

---

## 7. TRIDENT II D5 Strategic Weapons System

**Sole-source to Lockheed Martin Space (formerly LM Strategic Programs).** SSP
(Strategic Systems Programs) is the Navy contracting authority. The TRIDENT II
D5 is the SLBM carried by Ohio and Columbia SSBNs and UK Vanguard/Dreadnought
SSBNs (UK uses pooled US missile inventory).

### Prime Contracts (FY20-26 obligations)

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N0003023C0100** | Lockheed Martin | **$1.20B** | $1.23B | FY24 Trident Production & Deployed Systems Support |
| **N0003019C0100** | Lockheed Martin | **$1.12B** | $1.29B | FY20 Trident Production & Deployed Systems Support |
| **N0003020C0100** | Lockheed Martin | **$1.12B** | $1.36B | FY21 Trident Production & Deployed Systems Support |
| N0003008C0100 | Lockheed Martin | $750M | $765M | Trident |
| N0003013C0100 | Lockheed Martin | $712M | $764M | FY14 Trident Production |
| **N0003022C2001** | L3Harris Interstate Electronics Corp | **$391M** | $458M | Follow-on Engineering Services for SSP-owned Flight Test Instrumentation |
| N0003020C0101 | Lockheed Martin | $216M | $217M | TRIDENT II D5LE2 SPALT Advanced Development |
| N0003018C0100 | Lockheed Martin | $144M | $1M | TRIDENT II D5 Instrumentation Incentive |
| N0003024C0100 | Lockheed Martin | $116M | $79M | FY25 Trident P&DSS |
| N0003023C6045 | Lockheed Martin | $106M | $114M | FY24 US Trident SWS Navigation Fleet Support |
| N0003010C0002 | Lockheed Martin | $95M | $134M | TRIDENT II Navigation Subsystem |
| N0003014C0002 | Lockheed Martin | $89M | $196M | TRIDENT II D5 Navigation Subsystem |
| N0003017C0002 | Boeing | $71M | $73M | US Fleet Tech Support TRIDENT II |
| N0003013C0002 | Boeing | $53M | $55M | FY13/FY14 TRIDENT II Navigation Subsystem |

### Top First-Tier Subcontractors

**N0003019C0100 (FY20 Trident D5 Production) -- 1,040 subs, $1.74B:**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **ATK Launch Systems / Northrop Grumman** | **$603M** | 30 | Solid rocket motors (1st/2nd/3rd stage) |
| **Aerojet Rocketdyne** | $186M | 38 | Post-boost propulsion (PBCS) |
| **CAES Mission Systems** | $147M | 25 | Mission/RF electronics |
| **GD Mission Systems** | $112M | 19 | Fire control |
| **Intermat** | $64M | 8 | Missile components |
| **Cometto S.p.A. (Italy)** | $60M | 35 | Missile transport vehicles |
| **Excelitas Technologies** | $57M | 14 | Optoelectronics |
| **BAE Systems Ordnance Systems** | $56M | 3 | Propellant / explosives |

**N0003020C0100 (FY21 Trident D5) -- 751 subs, $1.27B:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| ATK Launch Systems / Northrop Grumman | $724M | Solid rocket motors |
| Aerojet Rocketdyne | $86M | PBCS |
| Raytheon | $69M | Mission electronics |
| GD Mission Systems | $58M | Fire control |
| Cometto S.p.A. (Italy) | $44M | Transport vehicles |
| Northrop Grumman Systems | $30M | Electronics |
| CAES Mission Systems | $30M | RF |
| BAE Systems Ordnance Systems | $30M | Propellant |

**N0003023C0100 (FY24 Trident D5) -- 311 subs, $365M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **Northrop Grumman Systems** | **$235M** | Solid rocket motors (post-ATK rebrand) |
| Aerojet Rocketdyne | $52M | PBCS |
| Moog | $10M | Actuators |
| Honeywell International | $6M | IMUs |
| EaglePicher Technologies | $3M | Thermal batteries |

> **Northrop Grumman dominates Trident propulsion** through its 2018
> acquisition of Orbital ATK -- the SLBM solid rocket motors are now
> manufactured at NG facilities in Promontory, UT and Magna, UT. Combined
> ATK/NG sub totals across the FY20/FY21/FY24 Trident production contracts
> exceed **$1.56B** in the FY20-26 window.

---

## 8. Strategic Missile Systems Equipment (SSBN)

**OPN BA4 Line 5358** -- ground-side and shipboard equipment supporting the
Trident SWS. Funded as Lockheed Martin SSBN combat / fire control work.

### Prime Contracts

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N0002417C6259** | Lockheed Martin | **$1.02B** | **$1.52B** | TI18 SSBN Material & Kit Additions |
| N0003014C0005 | GD Advanced Information Systems | $164M | $208M | US/UK SSBN Replacement (SSBN-R) Development |
| N0003010C0005 | GD Advanced Information Systems | $121M | $139M | SSBN Fire Control System Sustainment |
| N0003016C0005 | GD Advanced Information Systems | $117M | $86M | SSBN Fire Control SS Rep / Support UK |
| 0793 | JHU Applied Physics Lab | $49M | $50M | S3115 SSBN Security Technology Program |
| N0003018C0005 | GD Mission Systems | $40M | $42M | SSBN Development |
| N0003017C0001 | BAE Systems Technology Solutions & Services | $30M | $48M | SP2012 SSBN Replacement CMC |

### Top First-Tier Subcontractors

**N0002417C6259 (LM TI18 SSBN Material) -- 1,609 subs, $1.05B:**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **GD Mission Systems** | **$465M** | 175 | Fire control system (intra-FCS work routed via LM) |
| Gromelski & Associates | $81M | 49 | Engineering services |
| **Mercury Systems -- Trusted Mission Solutions** | $80M | 64 | Secure mission processing |
| Turk Innovative Consulting Group | $79M | 24 | Engineering services |
| Sedna Digital Solutions | $44M | 28 | Mission software |
| Germane Systems | $26M | 13 | Rugged computing |
| NCS Technologies | $23M | 36 | Servers / storage |
| Venator Solutions | $22M | 41 | Engineering |

---

## 9. MK-48 Heavyweight Torpedo

**Sole-source to Lockheed Martin Sippican (Marion, MA)** for the MK-48 MOD 7
guidance & control section. WPN 3117 (production) and WPN 3225 (Mods).

### Prime Contracts

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N0002416C6412** | Lockheed Martin Sippican | **$489M** | **$537M** | MK48 MOD 7 G&C Section Production |
| N0002411C6404 | Lockheed Martin Sippican | $178M | $192M | MK48 MOD 7 G&C Kit POM/First Article |
| N0002418C6408 | Lockheed Martin Sippican | $63M | $65M | MK48 Transition & Planning |
| N0003920C0013 | Lockheed Martin Sippican | $62M | $76M | OE-538B Upgrade Kit (Legacy to B) |
| N6660411C0895 | Lockheed Martin Sippican | $33M | $35M | MK39 MOD 2 EMATT Targets |
| 0467 | Penn State University | $3M | $3M | Advanced MK-48 MOD 7 Fiber-Optic Torpedo Mounted Dispenser (FOTMD) Tether Project |

### Top First-Tier Subcontractors

**N0002416C6412 (MK-48 MOD 7 G&C Section) -- 824 subs, $268M:**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **Ultra Electronics Ocean Systems** | **$96M** | 26 | Sonar arrays for MK-48 MOD 7 |
| Frontgrade Technologies | $19M | 10 | Rad-hard / mil-spec ICs |
| TTM Technologies | $16M | 32 | Printed circuit boards |
| Arrow Electronics | $13M | 34 | Electronics distribution |
| Curtiss-Wright DS | $10M | 7 | Mission electronics |
| EMCORE Corporation | $8M | 7 | Fiber optic gyros |
| Rantec Power Systems | $8M | 6 | Power supplies |
| Advanced Acoustic Concepts | $7M | 27 | Sonar processing |

> **Ultra Electronics Ocean Systems** at $96M is the dominant MK-48 MOD 7
> sub-prime, supplying the sonar array hardware. Ultra also holds direct
> Navy primes for the AN/SLQ-25 Nixie torpedo countermeasure (see
> `SAM_Program_Component_Contracts.md` Section 5.2).

---

## 10. Conventional Prompt Strike (CPS) -- SSN Hypersonic

**OPN BA4 Line 5353** -- "CPS Support Equipment" (GFE for newbuild SSN).
The CPS program is the Navy's hypersonic boost-glide weapon, integrated into
the Block V Virginia Payload Module (VPM). The all-up-round prime is shared
with the Army's Long Range Hypersonic Weapon (LRHW) program -- Lockheed Martin
Space is the LRHW prime, with Dynetics as the glide body integrator and
Northrop Grumman / Aerojet Rocketdyne providing the booster.

### Prime Contracts (Navy CPS)

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0002423F8129 | JHU Applied Physics Lab | $46M | $62M | Navy CPS Program |
| N0002420F8027 | JHU Applied Physics Lab | $33M | $36M | CPS Performance / Test & Evaluation |
| N4008524F4411 | Bamforth Engineers + Surveyors | $5M | $5M | A-E Full Design for P-1419 CPS Weapons Test |
| N0002422F8348 | Penn State University | $4M | $6M | Digital Engineering for CPS |
| N0002420F8029 | JHU Applied Physics Lab | $3M | $3M | Navy CPS Program |
| N0002424F8186 | JHU Applied Physics Lab | $2M | $6M | Navy CPS RA |
| N0002423F8223 | JHU Applied Physics Lab | $2M | $2M | Navy CPS RA |
| HQ003423F0049 | Poplicus Inc. | $1M | $1M | SaaS Platform Licenses for SSP CPS |

> **CPS prime contractors are mostly captured under Army LRHW** (Dynetics,
> Lockheed Martin, NG, Aerojet Rocketdyne). Navy-side FPDS visibility is
> almost entirely JHU APL test & evaluation and SSP infrastructure.
> Joint program TBG (Tactical Boost Glide) work is funded via DARPA, not Navy SCN.

> The N0002417C2100 Virginia Block V prime contract had a CPS-related mod in
> 2023 that diverted Marotta valves from one hull to the CPS program office --
> the contract value $34.65B includes some CPS-related sub work captured in
> the Virginia subaward tree.

---

## 11. SSN/SSBN Depot Maintenance

**OMN_Vol2 SSN/SSBN/SSGN lines** ($5.21B SSN + $878M SSBN + $225M SSGN combined
in FY26 SAM). The bulk of submarine depot maintenance is performed at the four
public naval shipyards (Norfolk Naval Shipyard, Portsmouth Naval Shipyard,
Pearl Harbor Naval Shipyard & IMF, Puget Sound Naval Shipyard & IMF), which
are federal facilities and **do not appear in FPDS**. Private-sector primes
fill specialized gaps and modernization installations.

### Private-Sector Primes (FPDS-visible)

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0002420C4312 | General Dynamics Electric Boat | $1.33B | $1.36B | Virginia Class M&M (referenced in section 1) |
| 4T44 | HII (Newport News) | $1M | $1M | Emergent NNSY-ACE repairs |
| 8C01 | HII | $1M | $1M | USS La Jolla (SSN 701) Tech Engineering Support |

> **Most submarine depot work is invisible in public databases** because it's
> performed by federal shipyard workforce, not contracted out. The four public
> shipyards employ ~36,000 federal workers and consume the bulk of the $6B+
> annual SSN/SSBN OMN sustainment budget. Only the modernization installations,
> emergent repairs, and certain specialized support fall to private contractors.

---

# USCG CUTTERS

## 12. Polar Security Cutter (WAGB)

**Originally awarded to VT Halter Marine, Inc. (Pascagoula, MS)** in April 2019
for $745.9M ceiling for PSC 1 with options for PSC 2 and PSC 3. Bollinger
Shipyards acquired VT Halter Marine in November 2022, renaming it
**Bollinger Mississippi Shipbuilding**. The contract PIID `N0002419C2210` has
since been re-novated under the new vendor name.

### Prime Contract

| PIID | Contractor | Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **N0002419C2210** | **Bollinger Mississippi Shipbuilding** (formerly VT Halter Marine) | **$2.02B** | **$2.74B** | 2025-12-15 | PSC 1 & PSC 2 Detail Design and Construction |

The same PIID also appears under the legacy `VT HALTER MARINE, INC.` vendor
record at $1.38B obligated / $2.24B ceiling (mod signed 2023-01-11) -- this
is the pre-novation snapshot.

### Other Polar Security Cutter Contracts (Support / Logistics)

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| 70Z02321CAPB02300 | L3 Technologies | $12M | $16M | Additional certification for upgraded comms |
| 70Z02325CSALC0001 | Crow Point Energy | $4M | $14M | Generator Set (GENSET) Storage & Maintenance |
| 70Z02321FAPB01200 | Reed Integration | $2M | $10M | Engineering support |
| 70Z02321FPRT00200 | Powertrain | $2M | $6M | Human Systems Integration (HSI) eng support |
| 70Z02325FSALC0005 | Sunstone Technical Solutions | $2M | $2M | Integrated Logistics Support FY26 |
| 70Z02324FSALC0003 | Sunstone Technical Solutions | $2M | $2M | ILS Support 12 mo |
| 70Z08819FADM81300 | AMEC Foster Wheeler -- HDR JV | $1M | $1M | H-PSC Homeport Feasibility Study |

> **Subawards: 0** -- Bollinger Mississippi Shipbuilding does not currently
> report subawards on PSC. The Polar Security Cutter has had well-publicized
> design and welding issues since the contract was awarded; first steel
> cutting was delayed multiple times into 2024.

---

## 13. Arctic Security Cutter / CAPI -- New Programs

**Three new heavy icebreaker procurement vehicles** signed late 2025/early
2026 -- not yet reflected in the SAM sheet's $130M FY26 WAGB line, but
massive future obligations.

### Prime Contracts

| PIID | Contractor | Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **70Z02326C93210002** | **Bollinger Shipyards Lockport** | **$921.7M** | **$2.14B** | 2025-12-19 | **Letter Contract: Arctic Security Cutters** |
| **70Z02326C93210001** | **Rauma Marine Constructions Oy** (Finland) | **$520.5M** | **$1.12B** | 2025-12-26 | **Purchase of 2 Arctic Security Cutters** for USCG |
| **70Z02326C93210003** | **Davie Defense Inc.** (Canada) | **$180.0M** | **$3.50B** | 2026-02-10 | **Letter Contract: 5 Multi-Purpose Polar Icebreakers** |
| **70Z02325C93260001** | **Offshore Service Vessels, LLC** (Edison Chouest subsidiary) | **$126.9M** | **$126.9M** | 2024-11-20 | **Commercially Available Polar Icebreaker (CAPI)** -- purchase of M/V *Aiviq* |

### Context

- **Bollinger Lockport** and the Finnish/Canadian foreign primes are part of
  the **ICE Pact** (US-Canada-Finland trilateral icebreaker partnership)
  announced in 2024 to rapidly expand Arctic capacity. The combined 2026
  ceiling across all three vehicles exceeds **$6.8B** -- a 50x increase over
  the FY26 SAM line item amount.
- The **CAPI / Aiviq** purchase converts a commercial offshore supply vessel
  (built 2012 by Edison Chouest) into a USCG-operated medium icebreaker as
  an interim capability while PSC slips and Arctic Security Cutter ramps.

> **Subawards: 0 across all four** -- all signed within the last 6 months,
> too new for subaward reporting to flow.

---

## 14. Offshore Patrol Cutter (WMSM)

**Two-stage procurement.** Stage 1 (OPC 1-4) was awarded to Eastern Shipbuilding
Group in 2016. Following Hurricane Michael damage and contract restructuring,
Stage 2 (OPC 5-15) was re-competed and **awarded to Austal USA in June 2022**.
Both yards are now active building OPCs in parallel.

### Prime Contracts

| PIID | Contractor | Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **HSCG2314CAPC002** | **Eastern Shipbuilding Group** | **$1.40B** ($1.73B per DHS view) | **$2.05B** | 2026-02-20 | **OPC Stage 1** -- OPCs 1-4 (Argus, Chase, Ingham, Rush) |
| **70Z02322C93220001** | **Austal USA** | **$1.40B** | **$3.31B** | 2026-03-19 | **OPC Stage 2** -- OPCs 5-15 (Production & Classing exercise) |

### Other OPC-Related Contracts

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| 70Z02320CAPC03700 | VT Halter Marine | $3M | $3M | Industry studies for OPC re-compete |
| 70Z02320CAPC03200 | Eastern Shipbuilding Group | $1M | $1M | OPC industry studies (option period) |
| 70Z02324F93260001 | McHenry Management Group | $1M | $2M | OPC closeout |
| 0080 | Centurum IT | $1M | $1M | OPC acquisition support (also FRC) |

### Top First-Tier Subcontractors

**HSCG2314CAPC002 (Eastern Shipbuilding OPC Stage 1) -- 709 subs, $430M:**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **Marine Interior Systems** | **$63M** | 18 | Cabin / interior outfitting |
| **Rolls-Royce Marine North America** | **$46M** | 4 | Propulsion / waterjets |
| Trident Maritime Systems | $33M | 6 | Marine systems integration |
| IMENCO | $32M | 12 | Subsea / mission package |
| **Northrop Grumman Systems** | $30M | 8 | Combat / mission systems |
| W. & O. Supply | $25M | 85 | Marine hardware distribution |
| **Fairbanks Morse** | $24M | 11 | Diesel propulsion (Coltec) |
| Genuine Cable Group | $16M | 11 | Marine cable |

> **Austal USA OPC Stage 2 reports 0 subawards** in the FY20-26 window
> (contract is too new -- production funding only began Mar 2026). Austal's
> known suppliers from its earlier LCS Independence-variant work include
> Caterpillar (propulsion), Rolls-Royce (waterjets), GE (gas turbines), and
> regional Mobile, AL fabricators.

---

## 15. Fast Response Cutter (WPC)

**Sole-source to Bollinger Shipyards Lockport, LLC (Lockport, LA)** -- the
Sentinel-class FRC is built on a Damen Stan Patrol 4708 license. Production
runs against two main contract vehicles spanning 2008-2026.

### Prime Contracts

| PIID | Contractor | Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **HSCG2316CAFR625** | **Bollinger Shipyards Lockport** | **$2.08B** | **$2.14B** | 2026-02-25 | **FRC Post-2016** (FRCs 38+) -- includes excusable delay for FRC 1158 (Hurricane Francine), economic price adjustment |
| **HSCG2308C2FR125** | **Bollinger Shipyards Lockport** | **$1.54B** | **$1.54B** | 2024-05-03 | **FRC Original Contract** (FRC-B, FRCs 1-37) -- close out |

### FRC Support Contracts

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| 70Z02319FAFR92700 | Management & Technical Services Alliance (MTSA) | $35M | $45M | FRC Program Management & Engineering Support |
| 70Z02324F93240001 | MTSA | $5M | $9M | FRC PM/Eng/Logistics Support |
| HSCG5013JADM025 | M.A. Mortenson Company | $28M | $28M | Design-Build FRC Homeport Upgrades |
| 70Z02320COCOM0100 | JT Marine | $12M | $12M | PATFORSWA Mooring Solution Repair |
| HSCG2317FAFR729 | ITA International | $6M | $6M | FRC Acquisition Support |
| 70Z05022F43000001 | Whiting-Turner Contracting | $8M | $8M | FRC Homeporting & Moorage Design-Build |
| HSCG4711JA15001 | BlueScope Construction | $4M | $4M | FRC Support Facility Design/Construct |

> **Subawards: 0 on both Bollinger FRC primes** -- Bollinger does not report
> subawards. Known FRC suppliers from public sources: MTU Detroit Diesel
> (4000 series propulsion), Hamilton Jet (waterjets on early hulls),
> Furuno (radar), Rapp Marine (deck machinery).

---

## 16. National Security Cutter (WMSL) -- Sustainment

**Sole-source to HII Ingalls Shipbuilding (Pascagoula, MS).** Production
of all 11 NSCs (Bertholf-class / Legend-class WMSL 750-760) is largely
complete. The FY26 SAM line items ($30M ISSS + $1M UAS) are sustainment-only.
The historic NSC production contracts are still releasing residual
obligations and warranty work.

### Prime Contracts (legacy NSC production, residual mods in window)

| PIID | Contractor | Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **HSCG2313CADB014** | **HII (Ingalls Shipbuilding)** | **$1.65B** | **$1.66B** | 2024-07-15 | NSC Production / In-Service Systems Sustainment |
| **HSCG2316CADB016** | **HII (Ingalls Shipbuilding)** | **$1.46B** | **$1.48B** | 2025-07-29 | NSC Production -- includes MK-48 MOD 2 GWS (note: USCG MK-48 = 25mm gun, NOT the Navy MK-48 torpedo) |
| **HSCG2311C2DB043** | **HII (Ingalls Shipbuilding)** | **$1.16B** | **$1.17B** | 2024-04-16 | NSC Production close-out |

### NSC Sustainment & Support

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| **N0002412C5316** | BAE Systems Land & Armaments | $50M | $56M | MK 110 57mm Naval Gun for USCG NSC |
| 70Z02321CADB00700 | **Bird-Johnson Propeller Company** | $26M | $26M | Mission critical spares for 418-ft NSC & 270-ft MSC |
| 70Z02322F93210001 | McHenry Management Group | $26M | $27M | NSC PM support |
| 70Z02324F93210001 | McHenry Management Group | $9M | $23M | NSC / Arctic Security Cutter funds management |
| 70Z04425FC2PL0007 | L3 Technologies | $5M | $6M | NSC Shipboard Alarm & Announcing System OS Upgrade |
| 70Z02324C93350002 | Lockheed Martin | $4M | $4M | NSC RF Distribution / Maritime Comm Controller |
| 70Z04424FC2PL0009 | Chugach Technical Solutions | $3M | $7M | NSC Home Port / Underway Contractor Reps |

### Top First-Tier Subcontractors (NSC Sustainment Tier)

**HSCG2316CADB016 (HII NSC Production) -- 679 subs, $490M:**

| Subcontractor | Subaward $ | Actions | Role |
|---|---|---|---|
| **Lockheed Martin** | **$272M** | 20 | Combat system / SPQ-9B / sensors |
| **Rolls-Royce Solutions America** | **$68M** | 26 | Diesel propulsion (16V/20V mtu series) |
| Northrop Grumman Systems | $18M | 13 | Electronics |
| Caterpillar | $8M | 4 | Service diesels |
| **SOCAIL, LDA** (Portugal) | $8M | 1 | Foreign-sourced gas turbine engines |
| York International (Johnson Controls) | $6M | 5 | HVAC |
| Appleton Marine | $4M | 3 | Deck machinery |

**HSCG2313CADB014 (HII NSC Production / ISSS) -- 711 subs, $366M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **Lockheed Martin** | **$159M** | Combat system |
| **Rolls-Royce Solutions America** | $79M | Diesel propulsion |
| Northrop Grumman Systems | $18M | Electronics |
| Superior-Lidgerwood-Mundy | $7M | Deck machinery |
| American Bureau of Shipping | $6M | Classification |
| York International | $5M | HVAC |
| Caterpillar | $4M | Service diesels |
| W. & O. Supply | $4M | Marine hardware |

**HSCG2311C2DB043 (HII NSC Production Close-out) -- 161 subs, $96M:**

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **Lockheed Martin** | **$72M** | Combat system |
| Northrop Grumman Systems | $3M | Electronics |
| Rolls-Royce Solutions America | $3M | Diesel |
| Mid Atlantic Engineering Tech Services | $2M | Engineering |

> **Lockheed Martin is the dominant NSC sub-prime at $503M combined** across
> the three HII NSC contracts -- it provides the COMBATSS-21 / SPQ-9B / Mk
> 36 combat system and the SLQ-32(V)2 EW suite.
>
> **Rolls-Royce Solutions America** (formerly MTU Detroit Diesel) is the
> propulsion sub-prime at **$148M combined** -- supplying the 20V 1163 TB93
> and 16V 595 TE90 mtu diesel sets.

---

## 17. Waterways Commerce Cutter (WCC)

**Sole-source IDIQ to Birdon America Inc.** (subsidiary of Birdon Pty Ltd,
Australia). The WCC program replaces three legacy classes (WLR river buoy
tenders, WLIC inland construction tenders, WLM coastal buoy tenders) with a
single design family. Production ramping up FY24-26.

### Prime Contracts

| PIID | Contractor | Obligated | Ceiling | Latest Mod | Description |
|---|---|---|---|---|---|
| **70Z02323D93270001** | **Birdon America Inc** | **$3.8M** | **$1.20B** | 2022-10-05 | **WCC IDIQ** -- master contract |
| **70Z02324F93270004** | **Birdon America Inc** | **$106M** | **$110M** | 2026-02-26 | **LLTM for WLR 1803 (WCC-7) and WLIC 1605 (WCC-8)** + List #1 deep insurance spares |
| **70Z02325F93270007** | **Birdon America Inc** | **$84M** | **$84M** | 2026-02-26 | **WLR 1802 production + ECP bundle** |
| **70Z02325F93270005** | **Birdon America Inc** | **$74M** | **$74M** | 2026-02-26 | **WLIC 1603 & 1604 production + ECP bundle** |
| 70Z02323F93250008 | Birdon America Inc | $47M | $47M | 2025-10-07 | Period of performance extension |
| 70Z02323F93270002 | Birdon America Inc | $40M | $40M | 2025-09-16 | Cabling change scoping |
| 70Z02324F93250008 | Birdon America Inc | $38M | $38M | 2025-12-19 | Discovered item labor + materials |
| 70Z02325F93270002 | Birdon America Inc | $37M | $37M | 2025-09-18 | WLIC #1 Factory Training |

### WCC Support Contracts

| PIID | Contractor | Obligated | Ceiling | Description |
|---|---|---|---|---|
| 70Z02321FPRT00200 | Powertrain | $2M | $6M | HSI engineering support (cross-WCC/PSC) |
| 70Z02320FPAP01800 | McHenry Management Group | $2M | $3M | WCC support |
| 70Z02326FSALC0002 | Sunstone Technical Solutions | $2M | $5M | WCC ILS for Surface Acquisition |
| 70Z02325F93270003 | Thor Solutions | $1M | $6M | WCC project management support |
| 70Z02322F93270001 | The MITRE Corporation | $1M | $1M | WCC Acquisition Systems Security Engineering |
| 70Z02321FPRT01600 | Booz Allen Hamilton | $0.4M | $0.5M | Senior Review Team support |
| 70Z02324F92830003 | Technomics | $0.3M | $1M | Cost analyst services |
| 70Z08324FCLEV0032 | WSP USA Environment & Infra | $0.3M | $0.3M | Environmental assessments for Peoria homeport |

> **Subawards: 0 across all Birdon WCC contracts** -- production has only
> begun ramping in late 2025/early 2026, too new for subaward reporting.
> Birdon's known suppliers include local Mississippi/Louisiana steel fabricators
> and Caterpillar (propulsion).

---

## 18. NSC Unmanned Aircraft Systems

The FY26 SAM line includes **$1M for NSC Unmanned Aircraft Systems**. This
funds the **Insitu ScanEagle** (Boeing subsidiary) used as the NSC's organic
airborne sensor. ScanEagle production contracts are routed through DoD
program offices (Navy / Marine Corps) and don't appear under the USCG
acquisition column in FPDS. Standalone USCG ScanEagle / SmallUAS contracts
in the FY20-26 window are limited:

| PIID | Contractor | Obligated | Description |
|---|---|---|---|
| 70RSAT20FR0000056 | The MITRE Corporation | $4M | C-UAS Response & Engagement (FFRDC) |
| 70RDA224FR0000023 | The MITRE Corporation | $3M | Data analytics support C-UAS |
| 70RDAD22FR0000108 | The MITRE Corporation | $3M | Systems engineering for C-UAS |
| 70Z02322F71110007 | W.S. Darley & Co. | $1M | USCG procurement of 45 small UAS |
| 70Z02322F71110008 | Atlantic Diving Supply | $1M | USCG procurement of 27 small UAS |
| 70T05024F6116N002 | Atlantic Diving Supply | $1M | 25 Skydio X10D drones for LE-FAMS |
| 70RSAT21FR0000028 | The MITRE Corporation | $1M | SUAS R&D |

> **The actual ScanEagle production contracts** for NSC integration are
> under Navy NAVAIR PMA-263 (Insitu Inc., parent: Boeing) and not visible
> in USCG-coded FPDS records.

---

## 19. Summary: Top Primes & Subs Across All Programs

### Top Prime Contractors (by FY20-26 obligation, submarine + cutter scope)

| Rank | Contractor | Parent | Programs | FY20-26 Obligated |
|---|---|---|---|---|
| 1 | **General Dynamics Electric Boat** | General Dynamics | Virginia (SCN 2013), Columbia (SCN 1045), SSBN concept | **~$72B** |
| 2 | **Bechtel Plant Machinery** | Bechtel | Virginia + Columbia naval reactor components | **~$18B** |
| 3 | **Lockheed Martin** (Strategic + sub combat) | Lockheed Martin | Trident II D5 production, SSBN material/kits, Virginia combat system, NSC combat system | **~$8.0B** |
| 4 | **Bollinger Shipyards Lockport / Bollinger Mississippi** | Bollinger | FRC, Polar Security Cutter (post-acq), Arctic Security Cutter | **~$5.5B** |
| 5 | **HII Ingalls Shipbuilding** (NSC) | Huntington Ingalls | NSC production / sustainment | **~$4.3B** |
| 6 | **Eastern Shipbuilding Group** | -- | OPC Stage 1 (OPCs 1-4) | **~$1.66B** |
| 7 | **Austal USA** | Austal Limited (AU) | OPC Stage 2 (OPCs 5+) | **~$1.40B** |
| 8 | **L3Harris Interstate Electronics Corp** | L3Harris | Trident D5 Flight Test Instrumentation | **~$391M** |
| 9 | **Birdon America Inc** | Birdon Pty (AU) | Waterways Commerce Cutter (3 hull classes) | **~$430M obligated to date / $1.2B IDIQ ceiling** |
| 10 | **Lockheed Martin Sippican** | Lockheed Martin | MK-48 MOD 7 G&C section | **~$793M** |
| 11 | **Davie Defense Inc** | Davie Group (CA) | 5x Multi-purpose Polar Icebreakers | **$180M (signed Feb 2026 -- $3.5B ceiling)** |
| 12 | **Rauma Marine Constructions Oy** | Rauma (FI) | 2x Arctic Security Cutters | **$520M ($1.12B ceiling)** |
| 13 | **GD Advanced Information Systems / GD Mission Systems** | General Dynamics | SSBN fire control, Knifefish | **~$400M** |
| 14 | **Boeing** | Boeing | Trident D5 fleet tech support / navigation | **~$125M** |
| 15 | **BAE Systems Land & Armaments** | BAE Systems | MK 110 57mm gun (NSC), Virginia propulsor assemblies, Columbia bearings | **~$100M** |

### Top Hidden Subcontractors (USAspending Subaward Pull, 2020-2026)

These appear inside the Electric Boat / Lockheed / Bechtel prime contracts but
do massive volumes of work across the submarine industrial base:

| Subcontractor | Combined Sub $ | Primary Programs | Role |
|---|---|---|---|
| **BlueForge Alliance** | **$4.21B** | Columbia (EB) | SIB workforce / supplier consortium (College Station, TX) |
| **Northrop Grumman Systems** | **$2.21B+** | Virginia, Columbia, Trident D5, SSBN material | Sonar, electronics, solid rocket motors (post-ATK), 30mm guns |
| **ATK Launch Systems / NG** | **$1.56B** | Trident D5 production | 1st/2nd/3rd stage solid rocket motors (Promontory + Magna, UT) |
| **GD Mission Systems** | **$643M+** | SSBN material/fire control, Trident, Columbia | Trident SWS fire control, intra-GD work |
| **DRS Naval Power Systems** | **$459M+** | Columbia (EB), Bechtel reactor components | Switchboards, power distribution, reactor instrumentation power |
| **BAE Systems Land & Armaments** | **$355M+** | Virginia (EB) | Submarine propulsors, weapons handling |
| **Curtiss-Wright Electro-Mechanical** | **$457M+** | Virginia, Columbia, Bechtel | Motors, valves, reactor coolant pumps |
| **BWXT Nuclear Operations Group** | **$290M+** | Bechtel reactor components | Reactor cores, fuel modules (Lynchburg, VA) |
| **Lockheed Martin Corp** (as sub) | **$503M** | NSC (HII) | NSC combat system / SPQ-9B / sensors |
| **Babcock Marine Rosyth** (UK) | **$240M** | Columbia (EB) | UK strategic-deterrent partner -- propulsion components |
| **Rolls-Royce Solutions America** | **$148M** | NSC (HII) | mtu diesel propulsion |
| **Aerojet Rocketdyne** | **$324M+** | Trident D5 production | Post-boost propulsion (PBCS) |
| **Globe Composite Solutions** | **$197M** | Virginia (EB) | Composites |
| **Scot Forge Company** | **$316M+** | Virginia, Columbia | Forgings (shafts, structural) |
| **DC Fabricators** | **$205M** | Virginia (EB) | Hull / structural fab |
| **APCO Technologies SA** (Switzerland) | **$145M+** | Columbia (EB) | Launch tube structural components |
| **Mercury Systems** | **$80M** | SSBN material/kits | Secure mission processing |
| **CAES Mission Systems** | **$177M+** | Trident D5 production | RF / mission electronics |
| **Ultra Electronics Ocean Systems** | **$96M** | MK-48 MOD 7 (LM Sippican) | Sonar arrays |
| **Marine Interior Systems** | **$63M** | OPC (Eastern) | Cabin / interior outfitting |
| **Rolls-Royce Marine North America** | **$46M** | OPC (Eastern), Virginia | Propulsion / waterjets / rotor (cross-program) |
| **Cometto S.p.A.** (Italy) | **$104M** | Trident D5 | Missile transport vehicles |
| **BWX Technologies** | **$53M** | Bechtel | Reactor pressure vessels |
| **Stryten Energy** | **$13M** | Virginia Block III | Submarine batteries |

### Key Findings

1. **The Submarine Industrial Base flows almost entirely through 3 primes:**
   General Dynamics Electric Boat (~$72B), Bechtel Plant Machinery (~$18B
   reactor components), and Lockheed Martin (~$8B Trident + combat systems).
   Together these three primes account for ~$98B of FY20-26 Navy submarine
   obligation activity.

2. **HII Newport News Shipbuilding's Virginia/Columbia work is invisible
   in FPDS prime data.** All sub team-build work flows through Electric Boat
   as prime; HII NNS appears only in the EB subaward tree (and only partially,
   since Northrop Grumman Systems shows up as the dominant Virginia/Columbia
   sub at $1.94B+ across hulls -- some of which is HII subcontract work).

3. **BlueForge Alliance ($4.21B) is the single largest "subcontractor" on
   Columbia.** This is the Submarine Industrial Base initiative's pass-through
   consortium for workforce development and supplier expansion, funded
   directly out of Electric Boat's Columbia prime.

4. **Northrop Grumman dominates Trident propulsion** through its 2018
   Orbital ATK acquisition. Combined ATK Launch Systems + NG sub totals on
   FY20/FY21/FY24 Trident production exceed **$1.56B** -- effectively making
   NG the second-tier prime for SLBM solid rocket motors.

5. **USCG cutter procurement is being radically reshaped by ICE Pact
   (US-Canada-Finland icebreaker partnership).** In a 4-month window
   (Nov 2025 - Feb 2026), USCG obligated **>$1.7B** with combined ceilings
   exceeding **$6.8B** to Bollinger (Arctic Security Cutter), Rauma Marine
   (Finland, 2 ASCs), and Davie Defense (Canada, 5 multi-purpose icebreakers).
   The SAM sheet's $130M FY26 WAGB line dramatically understates this.

6. **Bollinger Shipyards is now the dominant USCG shipbuilder**, holding the
   FRC contract (~$3.6B combined obligated), the Polar Security Cutter
   (post-VT Halter acquisition, $2.02B), and the Arctic Security Cutter
   ($921M just-signed). Bollinger's combined USCG portfolio in FY20-26
   approaches **$6.5B**.

7. **Birdon America is the only WCC prime** -- a sole-source IDIQ with $1.2B
   ceiling. WCC production is just beginning to ramp; cumulative obligations
   so far are ~$430M against the IDIQ.

8. **HII Ingalls Shipbuilding's NSC franchise** (now in sustainment-only mode
   per the SAM sheet) generated ~$4.3B in FY20-26 obligations across 3
   legacy production PIIDs. **Lockheed Martin is the dominant sub at $503M
   combined** (NSC combat system / SPQ-9B). The NSC fleet is now in
   sustainment under HSCG2313CADB014 (the ISSS contract).

9. **Subaward visibility gap:** Bollinger, Birdon, Austal, and the foreign
   ICE Pact primes report **0 subawards** across all their contracts in
   USAspending. This is the same pattern observed for BIW DDG-51 in the
   companion file -- some primes simply don't report subs to FFATA. The
   "true" subcontractor footprint of these cutter programs is multiples
   larger than what's visible.

---

## 20. Methodology & Limitations

### Data Pipeline

1. **FPDS Atom Feed** (https://www.fpds.gov/ezsearch/FEEDS/ATOM):
   - Searched `DESCRIPTION_OF_REQUIREMENT` with program-specific keywords:
     "VIRGINIA CLASS", "COLUMBIA CLASS", "TRIDENT II", "POLAR SECURITY CUTTER",
     "OFFSHORE PATROL CUTTER", "FAST RESPONSE CUTTER", "WATERWAYS COMMERCE
     CUTTER", "NATIONAL SECURITY CUTTER", "SUBMARINE ACOUSTIC", "PERISCOPE",
     "AN/BYG", etc.
   - Searched `VENDOR_NAME` for known primes: "ELECTRIC BOAT", "HUNTINGTON
     INGALLS", "BOLLINGER", "VT HALTER", "EASTERN SHIPBUILDING", "AUSTAL",
     "BIRDON", "LOCKHEED MARTIN SIPPICAN", "BECHTEL PLANT MACHINERY", "BWXT".
   - Filtered by `SIGNED_DATE:[2020/01/01,2026/12/31]`.
   - Parsed `<ns1:award>`, `<ns1:OtherTransactionAward>`, `<ns1:OtherTransactionIDV>`
     record types from XML.
   - Deduplicated to one record per PIID, keeping latest mod.

2. **USAspending Subaward Tree** (https://api.usaspending.gov/api/v2/):
   - For each major prime PIID, looked up `generated_internal_id` via
     `POST /search/spending_by_award/` (separately for contracts and IDV groups).
   - Pulled the full subaward tree via `POST /subawards/` paginating until
     `hasNext=false` (capped at 2,000 records per prime due to API ceiling).
   - Aggregated subawards by recipient name and ranked by total amount.

3. **Time window:** All sub data filtered to **2020-01-01 through 2026-04-10**
   per user direction. Some primes pre-date 2020; only obligations from mods
   signed inside the window are counted.

### Known Limitations

1. **Federal shipyard work is invisible.** Submarine depot maintenance
   (~$5B/year) is performed by federal employees at Norfolk, Portsmouth,
   Pearl Harbor, and Puget Sound naval shipyards. None of this appears in
   FPDS or USAspending. The OMN_Vol2 SSN/SSBN sustainment dollars in the
   SAM sheet are largely federal payroll.

2. **Team-build work flows through prime of record.** HII Newport News
   Shipbuilding does ~50% of Virginia and ~22% of Columbia hull construction
   under the Electric Boat team agreement. None of this appears as HII NNS
   prime contracts; it's captured inside EB obligations and partially visible
   in EB's subaward tree (Northrop Grumman shows up as the largest single sub
   at $1.27B Virginia + $669M Columbia, but it's unclear how much of that is
   actually NG vs. HII NNS routed work).

3. **Subaward reporting is inconsistent.** The following primes report
   **0 subawards** in the FY20-26 window:
   - Bollinger Mississippi Shipbuilding (Polar Security Cutter)
   - Bollinger Shipyards Lockport (FRC, Arctic Security Cutter)
   - Birdon America (Waterways Commerce Cutter)
   - Austal USA (OPC Stage 2)
   - Rauma Marine Constructions Oy (Finland)
   - Davie Defense Inc (Canada)
   - Offshore Service Vessels LLC (CAPI Aiviq)
   - Lockheed Martin Sippican (smaller MK-48 contracts)
   - Bechtel Plant Machinery (older PIIDs)
   This is a known gap in FFATA reporting -- not an absence of subcontracting.

4. **Foreign primes are limited to US-cleared content.** Babcock Rosyth (UK),
   APCO Technologies SA (Switzerland), Cometto S.p.A. (Italy), Rauma (Finland),
   and Davie (Canada) appear in the data because they hold US prime or sub
   contracts. The full scope of UK/AUKUS/ICE Pact work is invisible from
   USAspending alone.

5. **Trident D5 Flight Test Instrumentation has a corrupt subaward record.**
   PIID `N0003022C2001` (L3Harris IEC) has an outlier sub record listing
   CPI Satcom & Antenna Technologies at **$39 trillion** -- this is clearly
   a data entry error in the source feed. The valid sub data on that PIID
   is the BAE Systems Space & Mission Systems entry at $22M and below.

6. **OPN BA1 line items roll up to broader vehicles.** Sub Periscope (Line 4),
   Sub Support Equipment (Line 11), Virginia Class Support Equipment (Line 12),
   and Submarine Combat Control Systems (Line 5420) are budget rollups that
   feed into multiple FPDS contracts. The crosswalk above is best-effort
   based on description-level keyword matching.

7. **CPS (hypersonic) prime is split between Army LRHW and Navy CPS.** Most
   of the all-up-round prime work (Lockheed Martin Space, Dynetics) is funded
   through Army LRHW contracts (W9113M-* PIIDs), not Navy CPS. The Navy CPS
   Support Equipment line (OPN BA4 5353) primarily funds JHU APL test &
   evaluation, military construction at Navy hypersonic test facilities, and
   GFE payload integration into the Virginia Block V VPM.

8. **Reporting lag.** FPDS has a 30-90 day lag. Awards signed in March/April
   2026 may not yet appear in the public feed.

9. **Cumulative-vs-window dollar attribution** (added 2026-04-10 after
   reviewer feedback). The "Obligated" column in the prime tables above is
   the **cumulative `totalObligatedAmount` at the latest mod in our window**,
   not the sum of new money added inside the window. Several big numbers
   (Block IV $19.9B, Block V/VI master $34.9B, Block II residual $16.2B)
   reflect contracts that were already at those values when 2020 began.
   See Section 21 below for the proper SAM-line-to-contract crosswalk.

---

## 21. How to Map FY26 SAM Lines to Specific Contract Vehicles

This section answers the question: **"Are the contracts I found in FPDS
actually receiving FY26 SAM appropriations, and how do I know?"** The
short answer is: contract obligation data and annual appropriation data
don't map 1:1, and untangling them requires reading mod descriptions
carefully.

### The conceptual gap

The SAM sheet shows **annual appropriations** -- what Congress is putting
into a budget line in a given fiscal year. FPDS shows **contract obligation
events** -- when DoD/USCG commits money against a specific contract vehicle.
These don't align cleanly because:

1. **An FY26 appropriation can be obligated against an OLD contract.** Block
   IV was awarded in FY14 but is still receiving FY26 funding mods to close
   out final SSN 801 (USS Utah) construction.
2. **An old contract's "cumulative obligation" is mostly pre-window money.**
   The Block V/VI master vehicle (`N0002417C2100`) shows $34.94B cumulative
   at its latest mod, but most of that was committed in 2017-2019.
3. **Multi-year (MYP) contracts span fiscal years.** Block V was awarded as
   one $22.2B contract in December 2019 covering FY19-23 boats.
   Each year's appropriation gets obligated against that single vehicle.
4. **Long Lead Time Material (LLTM)** is funded ~2 years before construction.
   FY26 LLTM money goes to a different contract vehicle than FY26 construction.

### The verified Virginia/Columbia contract → block crosswalk

| Block / Build | MYP Contract Vehicle | Status | Hulls | Cumulative (latest mod) |
|---|---|---|---|---|
| Virginia Block II | N0002409C2104 | Closing out / parts donor | SSN 780-785 | $16.24B |
| Virginia Block III | (not surfaced in our pulls -- predecessor of N0002412C2115?) | Active sustainment | SSN 786-791 | -- |
| Virginia Block IV | **N0002412C2115** | **Active construction** | SSN 792-801 (10 boats) | **$19.90B** |
| Virginia Block V → Block VI master | **N0002417C2100** | **Active construction** | SSN 802-811 + extending into Block VI | **$34.94B** |
| Virginia Block VI LLTM | **N0002424C2110** | **New (FY24 award)** | SSN 814 long-lead material | **$4.96B** |
| Virginia Payload Module (VPM) -- ventilation | N0002416C2111 | Active component | All Block V hulls (5 with VPM) | $1.47B |
| Virginia Payload Module (VPM) -- tubes | N0002410C2118 | Active component | All Block V hulls (5 with VPM) | $1.42B |
| Columbia Build I + II | **N0002417C2117** | **Active construction (rapidly growing)** | SSBN 826 + 827 | $24-30B (climbing) |
| Columbia design | N0002413C2128 | Closed | -- | $3.07B |
| Columbia industrial base / Bechtel reactor | **N0002419C2115** | **Active** | All Columbia hulls | $3.00B |
| Naval Reactors (cross-program) | N0002419C2114, N0002424C2114, N0002416C2106, etc. | Active | Both Virginia + Columbia | ~$18B across 10 PIIDs |

### Mapping the FY26 SAM line items

Using the SAM sheet rows (FY2026 dollars in $K):

**SSN Virginia Class -- $17,605,524 ($17.6B total hull):**

| FY26 SAM Sub-line | $K | Likely receiving vehicle |
|---|---|---|
| Full Ship DD&C [PARENT] | 7,340,305 | **N0002417C2100** (Block V/VI master) -- FY26 mods will fund SSN 813+ construction; possibly a new Block VI MYP contract if signed in FY26 |
| Advance Procurement / LLTM | 3,126,816 | **N0002424C2110** (Block VI LLTM) -- new mods extending SSN 814+ LLTM scope |
| Scheduled Depot Maintenance | 5,214,667 | Federal naval shipyards (NNSY, PNSY, PHNSY, PSNS) -- **invisible in FPDS**. Plus N0002420C4312 USS Hartford EOH ($1.33B) and similar private-yard EOH contracts |
| Modernization | 1,923,736 | N0002410C6266 (LM combat systems $899M); OPN BA1/2/4 line items ; ManTech / GDIT acoustic; Lockheed Martin BYG-1 |

**SSBN Columbia Class -- $13,525,977 ($13.5B total hull):**

| FY26 SAM Sub-line | $K | Likely receiving vehicle |
|---|---|---|
| Full Ship DD&C [PARENT] | 3,928,828 | **N0002417C2117** (Build I + II construction) -- ongoing billion-dollar mods through FY26 |
| Advance Procurement / LLTM | 5,350,766 | **N0002419C2115** (Bechtel reactor industrial base) + new mods to N0002417C2117 + new Build III LLTM contracts |
| NWCF SBDF | 193,600 | National Sea Base Deterrence Fund -- separate vehicle, mostly Bechtel/BWXT pass-through |
| Scheduled Depot Maintenance | 878,403 | Federal shipyards (Trident Refit Facility Bangor, Kings Bay) -- invisible in FPDS |
| Modernization | 3,174,380 | OPN BA4 5358 Strategic Missile Systems Equip → **N0002417C6259** (LM TI18, $1.02B) ; WPN 1250 TRIDENT II Mods → **N0003023/19/20C0100** Lockheed Martin Trident production ($1.1-1.2B each) |

### How to verify "this mod was funded by FY26 money"

Read the mod description. FY26-funded mods typically reference:
- "**FY26**", "**FY 26**", or "**FY2026**" explicitly
- "**INCREMENTAL FUNDING**" or "**INC FUNDING MOD**"
- A purchase request (PR) number with FY26 in the prefix
- A boat name/hull number that's FY26-procured (e.g., for Virginia Block VI,
  SSN 815-816 if those are FY26 boats)

Example from our data:
```
N0002424C2114 mod P00003 signed 2025-12-17, this action $927.6M
  description: "FY26 SHIPSET OF VIRGINIA CLASS COMPONENT FUNDING MOD"
```
That's an unambiguous FY26 obligation: $928M of FY26 appropriated money
flowed into the Bechtel S9G reactor component contract on December 17, 2025.

Compare to:
```
N0002417C2100 mod A00343 signed 2025-12-23, this action $0.0M
  description: "INCORPORATION OF PREVIOUSLY AUTHORIZED CHANGES UNDER COUPON
                PROCESS FOR VIRGINIA CLASS AUTHORIZING MOD"
```
That's a paperwork mod -- $0 new money, just incorporating previously
authorized scope. Doesn't count toward FY26 spend.

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

I did not do this for the prime tables in this file -- they are
"contract size" references rather than "annual spend" references. The
**Bechtel Section 3 table** is the closest to a clean window pull
because most Bechtel PIIDs were awarded inside FY20-26.

---

*Generated 2026-04-10 from FPDS Atom Feed and USAspending /api/v2/subawards/.
Subaward time window: 2020-01-01 to 2026-04-10. Submarine + USCG cutter scope
per SAM sheet rows 125-196 (added in workbook v1.9).*

*Updated 2026-04-10 (rev 2): Block/Build labels corrected after per-mod
verification (Block IV was mislabeled as Block III, Block V/VI master was
mislabeled as Block IV/V). Added missing contracts: N0002424C2110 (Block
VI LLTM, $4.96B), N0002416C2111 (VPM ventilation, $1.47B), N0002410C2118
(VPM tube fabrication, $1.42B). Updated Columbia value from $13.59B
(stale) to current $24-30B range. Added Section 21 with explicit SAM
line item → contract vehicle crosswalk and the cumulative-vs-window
caveat.*
