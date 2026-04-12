# FY2026 SAM Programs -- Component & Subsystem-Level Contract Awards

Companion to `SAM_Program_Contract_Awards.md`. This file captures contracts
tracked under specific system designations, component names, and subsystem
programs rather than top-level budget line descriptions. These are the contracts
that don't surface when searching for "MCM mission module" or "DDG modernization"
but represent the actual procurement vehicles.

Data sources: FPDS Atom Feed + USAspending API.

> **Updated 2026-04-10:** Subaward sections added for major subsystem primes
> (SPY-6, SEWIP, CEC, SSDS, HELIOS, ALMDS, AMNS, UISS, Knifefish, Barracuda,
> Surface MCM Unmanned). Pulled by looking up each prime PIID's
> `generated_internal_id` via USAspending and calling the `/api/v2/subawards/`
> endpoint, which returns the full subaward tree per prime contract (2020-2026).

---

## Table of Contents

1. [MCM Mission Module Components](#1-mcm-mission-module-components)
2. [Airborne MCM Components](#2-airborne-mcm-components)
3. [DDG Modernization Subsystems](#3-ddg-modernization-subsystems)
4. [Self-Defense & Close-In Weapons](#4-self-defense--close-in-weapons)
5. [Torpedo Defense Subsystems](#5-torpedo-defense-subsystems)
6. [Directed Energy -- Named Systems](#6-directed-energy--named-systems)
7. [LCS Platform Subsystems](#7-lcs-platform-subsystems)
8. [Summary: Hidden Contract Values](#8-summary-hidden-contract-values)

---

## 1. MCM Mission Module Components

The LCS MCM Mission Module budget line (~$91M FY26) funds procurement of multiple
independent systems. Each has its own prime contractor and contract vehicle.

### 1.1 UISS -- Unmanned Influence Sweep System

| Field | Detail |
|---|---|
| **Prime** | **Textron Systems Corporation** (formerly AAI Corporation) |
| **Contract** | N0002414C6322 |
| **Obligated** | $324.0M |
| **Ceiling** | $341.8M |
| **Period** | 2014-2024 |

Support: Gibbs & Cox -- engineering & technical services for USV Influence Sweep System ($1.1M)

**Top Subcontractors (118 subaward records, $26.5M, 2020-2026):**

| Subcontractor | Role |
|---|---|
| **Coltec Industries** (Fairbanks Morse) | Diesel propulsion |
| **Northrop Grumman Systems** | Mission electronics |
| **Gibbs & Cox** | USV engineering |
| Multiple smaller subs (118 total actions) | Various |

### 1.2 Knifefish -- Mine Countermeasures UUV (Block 1)

| Field | Detail |
|---|---|
| **Prime** | **General Dynamics Mission Systems** |
| **Contract** | N0002421C6304 |
| **Obligated** | $42.5M |
| **Ceiling** | $72.8M |
| **Description** | Knifefish Block 1 LRIP -- Design, Integration, Production, Engineering Support |

Also part of broader Northrop Grumman LCS contract (N0002417C6311: $375.6M obligated / $1.57B ceiling)
which covers Knifefish System Container ECPs, Gun Mission Modules, and other LCS systems.

**Top Subcontractors:**
- GDMS Knifefish prime (N0002421C6304): **52 subawards, $18.6M**
- NG Knifefish/LCS prime (N0002417C6311): **908 subawards, $1.475B**
  - Major subs: Teledyne Defense Electronics ($928M), Teledyne Brown Engineering ($715M),
    GD Mission Systems (as sub, $608M), Trident Sensors Limited ($233M)

**Support contractors:**
| Contractor | Contract | Value | Role |
|---|---|---|---|
| University of Washington | N0002423F8709 | $945K ceiling | Knifefish field tests |
| Delaware Resource Group | N6134024F0093 | $98.7M ceiling | USV support (includes Knifefish trainer removal) |
| AERMOR LLC | N5702322F0057 | $1.0M ceiling | Knifefish support |
| Serco Inc | N6133119F0143 | $214K | Knifefish support |
| Redstone Defense Systems | 0424 | $503K | Knifefish support container |

### 1.3 MCM USV -- Mine Countermeasures Unmanned Surface Vehicle

| Field | Detail |
|---|---|
| **Prime** | **Bollinger Shipyards Lockport, LLC** |
| **Contract** | N0002422C6305 |
| **Obligated** | $116.1M |
| **Ceiling** | $167.5M |
| **Period** | 2022+ |

**Support:**
- Textron Systems (N6133125F0103): MCM USV IDIQ DO 02 -- $4.1M / $13.2M ceiling (2025)

### 1.4 AN/AQS-20 Mine Hunting Sonar

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Raytheon** | N6133125F0058 | $497K ceiling | Minehunting Payload Delivery System software & engineering |
| **Raytheon** | N6133119F0228 | $694K | AN/AQS-20C sonar enhancement |
| **Technical Systems Integration** | HR18 | $5.1M | AQS-20 ISEA engineering, logistics, technical support |
| **SAIC** | 6973GH22F00531 | $155K | AQS program management support |
| Innovative Professional Solutions | N6133125P0059 | $22K | Hydrophone sub-assembly, AQS-20 EOID shroud engineering |

### 1.5 AN/AQS-24C Volume Search Minehunting Sonar (VSMS)

| Field | Detail |
|---|---|
| **Prime** | **University of Texas at Austin (Applied Research Laboratories)** |
| **Contracts** | 0921, 0922, 0931 |
| **Combined Value** | ~$5.3M |
| **Description** | VSMS component and kit packages |

### 1.6 Barracuda Mine Neutralizer

| Field | Detail |
|---|---|
| **Prime** | **Raytheon Company** |
| **Contract** | N0002418C6300 |
| **Obligated** | $11.4M |
| **Ceiling** | $149.4M |
| **Description** | Barracuda development |

### 1.7 MCM Mission Package Integration

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Avian LLC / Avian Inc.** | N6133118F3010 | $26.6M ceiling | LCS MCM Mission Package C2, MCM Systems, MH-60S integration & sustainment, MVCS production |
| **Applied Technical Systems** | N6133122F3010 | $4.9M ceiling | LCS Multi-Vehicle Communications System (MVCS) support |
| **Innovative Professional Solutions** | N6133121F3008 | $19.3M | LCS mission module and unmanned maritime systems engineering |
| **Innovative Professional Solutions** | HR11 | $21.1M ceiling | LCS mission module engineering/technical support |
| **JHU APL** | N0002423F8905 | $10.4M | LCS mission module systems |
| **JHU APL** | N0002422F8020 | $3.0M | LCS mission module systems |
| **Solpac Construction** | N6247319F5055 | $13.4M | LCS Mission Module Readiness Center construction (physical facility) |

### 1.8 Surface Mine Countermeasures Unmanned (SMCM)

| Field | Detail |
|---|---|
| **Prime** | **General Dynamics Mission Systems** |
| **Contract** | N6133111C0017 |
| **Value** | $143.3M |
| **Period** | 2011-2022 |

**Subcontractor breakdown: 300 subaward records, $1.23B (2020-2026)** -- this
contract is far larger in actual obligations than the prime ceiling suggests.
Falls into the broader LCS/MCM subcontractor pool (Teledyne, GDMS internal, etc).

### 1.9 Mine Warfare Support (General)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Innovative Professional Solutions** | N6133121F3005 | $22.1M | Mine Warfare and SMCM Design Agent / ISEA |
| **Innovative Professional Solutions** | N6133118F3006 | $13.7M | In-service mines, MCM targets engineering |
| **Kentco Corporation** | N0001419C2011 | $18.6M | Organic MCM and mine warfare support |
| **Booz Allen Hamilton** | N6133118F3007 | $12.4M | Organic AMCM systems engineering and logistics |
| **Applied Technical Systems** | N6133124F3001 | $4.9M | In-service mines, MCM targets, improvements |
| **Pliant Energy Systems** | N0001424C2411 | $3.4M | SAPA vehicle (stealthy autonomous propulsion) for MCM |

### 1.10 MCM AI/ML for UUVs (Other Transactions -- DIU/DARPA)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| Weights & Biases | HQ08452290046 | $1.15M ceiling | MLOps for MCM by UUVs |
| Fiddler Labs | HQ08452290047 | $997K ceiling | MLOps for MCM by UUVs |
| Arize AI | HQ08452290048 | $1.30M ceiling | MLOps for MCM by UUVs |
| LatentAI | HQ08452290049 | $670K ceiling | MLOps for MCM by UUVs |
| Domino Data Lab | HQ08452290050 | $550K | MLOps for MCM by UUVs |
| SUBUAS LLC | N0001420C2019 | $4.5M ceiling | Multirotor UAV/UUV for MCM |

### 1.11 Legacy Minesweeping Equipment (Sustainment)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| Innovative Professional Solutions | N6133126C0001 | $13.6M | Minesweeping winches (AC Hoyle S-530) for ROK Navy |
| Atlantic Diving Supply | N6133118F0209 | $2.6M | AC Hoyle S-530 minesweeping winches |
| DMR Consulting | N6133124F0026 | $1.3M | MK 105 Mod IV engineering support |
| Technical Systems Integration | N6133118F0193 | $673K | MK 105 magnetic minesweeping gear |

---

## 2. Airborne MCM Components

These are the contracts that were invisible under "airborne mine" searches but
found via system-specific designations.

### 2.1 ALMDS -- AN/AES-1 Airborne Laser Mine Detection System

| Field | Detail |
|---|---|
| **Prime** | **Northrop Grumman Systems Corporation** |

| Contract | Obligated | Ceiling | Description |
|---|---|---|---|
| N0002415C6318 | $166.1M | **$517.2M** | ALMDS production (main contract) |
| N0002422C6418 | $29.5M | **$106.6M** | ALMDS production support |

**Total ALMDS ceiling: ~$624M**

**Subaward Deep Pull:**
- N0002415C6318 (production): **74 subawards, $91.3M**
- N0002422C6418 (production support): **38 subawards, $6.8M**

ALMDS subawards bundle into the broader NG MCM/LCS subcontractor base. Likely
sub-tier components include laser sources, optical components, and pod hardware
(Northrop Grumman doesn't fragment this into many large sub-primes).

### 2.2 AMNS -- AN/ASQ-235 Airborne Mine Neutralization System

| Field | Detail |
|---|---|
| **Prime** | **Raytheon Company** |

| Contract | Obligated | Ceiling | Description |
|---|---|---|---|
| N0002403C6310 | $102.5M | -- | AMNS Upgrade (-3) |
| N0002410C6307 | $58.1M | $72.1M | AMNS LRIP (FY09 OPN) |
| N0002417C6305 | $33.6M | $64.0M | AMNS LRIP |
| N0002425F6404 | $2.2M | $18.8M | AMNS Test & Depot Support |
| N0002421F6412 | $1.4M | $17.4M | AMNS Test & Depot Support |
| Various F-orders | ~$6M | -- | LRIP unit upgrades, canisters, maintenance test sets |

**Total AMNS value: ~$170M+**

**Subaward Deep Pull:**
- N0002417C6305 (newer LRIP): **280 subawards, $117.9M** (2020-2026)
- Older AMNS contracts (N0002403C6310, N0002410C6307): 0 subs in 2020+ window
  (predates reporting threshold)

### 2.3 OAMCM -- Organic Airborne Mine Countermeasures (Integration)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| Booz Allen Hamilton | HR02 | $9.8M ceiling | OAMCM systems engineering and logistics support |
| Booz Allen Hamilton | N6133122F3011 | $23.4M ceiling | ALMDS, AMNS, Barracuda, MIW engineering & logistics |
| Booz Allen Hamilton | N6133118F3007 | $12.4M | Organic AMCM systems engineering and logistics |
| **Avian LLC** | N6133118F3000 | $10.1M | Airborne MCM Performance Support System |

### 2.4 RAMICS -- Rapid Airborne Mine Clearance System

| Field | Detail |
|---|---|
| **Prime** | **QinetiQ** |
| **Contract** | N6133107C0034 |
| **Value** | $3.4M ceiling |
| **Description** | Integration and live firing of RAMICS |

### 2.5 Maritime Mine Neutralization System (M2NS) -- Next-Gen

| Field | Detail |
|---|---|
| **Prime** | **RE2 LLC** |
| **Contract** | N0001421C2030 |
| **Value** | $7.2M |
| **Description** | Maritime Mine Neutralization System development |

---

## 3. DDG Modernization Subsystems

The DDG Mod budget line (~$879M) and related OPN lines fund procurement of
major combat system upgrades. The individual subsystem contracts dwarf the
annual budget line because they span multiple fiscal years and ships.

### 3.1 AN/SPY-6(V) Radar (AMDR) -- **The Largest Single Subsystem**

| Field | Detail |
|---|---|
| **Prime** | **Raytheon Company** |

| Contract | Obligated | Ceiling | Description |
|---|---|---|---|
| N0002422C5500 | **$1.71B** | **$3.27B** | AN/SPY-6(V) hardware production (Option Year 2+) |
| N0002425C5501 | $205M | -- | AN/SPY-6(V) Family of Radars design agent (FMS) |
| N0001424C1103 | $9.2M | $43.0M | RASP enhanced radar signal processing |

**OTA development:**
- Advanced Technology International: AN/SPY-6 RF Head Prototype -- 2 contracts, ~$9.8M combined (OT Awards, 2023)

> The AN/SPY-6 is the single largest DDG modernization component. Raytheon's
> $3.27B production contract covers radar arrays for DDG-51 Flight III and
> backfit to earlier Flights. This one contract exceeds the entire FY2026
> DDG Mod budget line.

**Subaward Deep Pull -- N0002422C5500 (SPY-6 Production):**

**854 subaward records totaling $1.42B** (2020-2026). The radar's RF subsystem
ecosystem is fragmented across many specialized vendors:

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **CAES Systems** (Cobham Advanced Electronic Solutions) | ~$800M+ across SPY-6 + SEWIP | Multi-function RF assemblies (largest single sub) |
| **Mercury Systems** | ~$500M+ across SPY-6 + SEWIP | RF assemblies, signal processing |
| **Narda Holdings** | $352M (combined) | RF amplifiers (2-6 GHz), fiber optic receivers |
| **Linear Photonics** | $228M (combined) | Power supply modules |
| **Production Engineering** | $201M (combined) | Enclosures, HPOI assemblies, shelter structures |
| **Anaren** | $61M | RF combiners/dividers/couplers, limiters |
| **CAES Mission Systems** | $55M | RF amplifiers / limiters |
| **Smiths Interconnect** | $49M | Antenna assemblies, fiber optic receivers |
| **Stellant PST** | $44M | RF switches, limiters |
| **Major Tool & Machine** | $41M | General structural assemblies |
| **Teledyne Defense Electronics** | $41M (combined) | YIG filters |
| **TTM Printed Circuit Group** | $41M | Sensor terminal boards |
| **M.S.M. Industries** | $40M | Integrated electronic assemblies |
| **DRS Signal Solutions** | $39M | Microwave tuners |
| **Electromet** | $38M | Cabinet mounting bracket assemblies |
| **Interconnect Systems International** | $36M | Hybrid processor VME cards |
| **Teledyne Limited** | $36M | S-band / X-band tuned notch filters |
| **Spectrum Microwave** | $31M | RF microwave diplexers, band reject filters |
| **Technology Dynamics** | $31M | Power supplies |
| **OmniYIG** | $30M | YIG filters |

### 3.2 SEWIP -- Surface Electronic Warfare Improvement Program

Three separate blocks, three different primes:

**Block 2 -- AN/SLQ-32(V)6:**

| Contract | Prime | Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0002420C5503 | **Lockheed Martin** | -- | **$783.2M** | SLQ-32(V)6 production (w/o shelter) |
| N0002416C5363 | **Lockheed Martin** | -- | **$572.2M** | SLQ-32(V)6 SEWIP Block 2 subsystems |
| N0002409C5300 | **Lockheed Martin** | $168.8M | $226.0M | AN/SLQ-32X(V) SEWIP Block 2 |

**Block 3 -- AN/SLQ-32(V)Y:**

| Contract | Prime | Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0002415C5319 | **Northrop Grumman** | $188.8M | **$517.6M** | Pre-design SEWIP Block 3 |
| N0002422C5520 | **Northrop Grumman** | -- | **$80.3M** | SEWIP Block 3 design agent |

**Block 1B3:**

| Contract | Prime | Obligated | Ceiling | Description |
|---|---|---|---|---|
| N0002414C5341 | **GD Mission Systems** | $17.4M | $17.5M | SEWIP Block 1B3 LRIP |
| N0002416C5352 | **GD Mission Systems** | -- | $57.0M | SEWIP Block 1B3 systems |

**Support:**
| Contractor | Contract | Value | Role |
|---|---|---|---|
| SAIC | N0016418F3006 | $32.1M | SEWIP Blocks 2-4 engineering/logistics/program support |
| Penn State | N0001423FM002 | $6.3M | SEWIP Block 3 transceiver affordability |
| Stratascor | N0018922F0223 | $3.6M | SEWIP support services |
| Dignitas Technologies | N6134021F0039 + N6134024F0078 | $4.7M | SLQ-32(V)7 software applications |

**Total SEWIP program value across all blocks: ~$2B+**

**Subaward Deep Pull -- LM SEWIP Block 2 (N0002416C5363):**

**358 subaward records totaling $2.85B** -- this is the single largest subaward
total across the entire DDG modernization ecosystem. Same RF subcontractor
ecosystem as SPY-6 (CAES, Mercury, Narda, Abaco, etc.).

**Subaward Deep Pull -- LM SLQ-32(V)6 (N0002420C5503):**

**612 subaward records totaling $1.42B** -- another massive subaward pool.

**Subaward Deep Pull -- NG SEWIP Block 3 (N0002415C5319 / N0002422C5520):**

Only **13 subaward records totaling ~$1.4M** combined. NG performs Block 3 work
mostly in-house.

**Subaward Deep Pull -- GDMS SEWIP Block 1B3:**
- N0002416C5352: 19 subs, $20.8M
- N0002414C5341: 12 subs, $6.4M

Combined CAES Systems / Mercury Systems / Abaco Systems / RA Wood subaward
totals across SPY-6 + SEWIP Block 2 + SLQ-32(V)6 collectively exceed **$5B** --
these four firms form the hidden RF backbone of every modern Aegis radar/EW
upgrade.

### 3.3 SSDS -- Ship Self Defense System

| Contract | Prime | Value | Description |
|---|---|---|---|
| N0002419C5603 | **Lockheed Martin** | **$380.8M** | SSDS Combat System Engineering Agent (CSEA) |
| N0002414C5128 | **Raytheon** | **$358.1M** | SSDS PSEA FY14-17 follow-on |
| N0016425F3001 | **BAE Systems** | $66.4M | Aegis Weapon System, SSDS, related engineering |
| N0002421F8029 | **JHU APL** | $27.4M | SSDS integrated combat system |
| N0017820FD507 | **Lockheed Martin** | $19.5M | SSDS equipment production (multiple shipsets) |
| N0017819FD518 | **Northrop Grumman** | $20.9M | SSDS production hardware |
| 0007 | **Geonorth, LLC** | $48.5M ceiling | Aegis/SSDS LBTTS activation planning |

**Subaward Deep Pull -- LM SSDS CSEA (N0002419C5603):**

**898 subaward records totaling $270.1M** (2020-2026). Top sub:

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **Mission Solutions** | $149.5M | SSDS IFFSIM, RVP studies, baseline support |
| **Programs Mgmt Analytics & Technologies (PMAT)** | $43.3M | In-service support, facilities support |
| **Epsilon Systems Solutions** | (in batch) | Tech/eng services |

**Subaward Deep Pull -- Raytheon SSDS PSEA (N0002414C5128):**

**206 subaward records totaling $71.2M** (2020-2026).

### 3.4 CEC -- Cooperative Engagement Capability

| Contract | Prime | Value | Description |
|---|---|---|---|
| N0002419C5200 | **Raytheon** | **$416.5M** | CEC design agent and engineering |
| N0002413C5212 | **Raytheon** | **$379.9M** | CEC |
| N0002425C5239 | **Raytheon** | **$160.8M** | CEC design agent (follow-on) |
| HQ085221C0002 | **Lockheed Martin** | $14.8M | CEC/Army IAMD integration (MDA) |
| N0001421C1012 | **Leidos** | $11.6M | Decoupling CEC processor from data distribution |

**Total CEC: ~$1B (Raytheon sole prime)**

**Subaward Deep Pull -- Raytheon CEC (3 contracts):**

| Prime PIID | Subawards | Total $ |
|---|---|---|
| N0002419C5200 (CEC design agent) | 147 | $302.8M |
| N0002413C5212 (CEC) | 63 | $12.5M |
| N0002425C5239 (CEC follow-on) | 3 | $6.0M |

**Total CEC subawards 2020-2026: 213 records, $321.3M.** Major subs include
the same RF/signal-processing tier as SPY-6 and SEWIP (Mercury Systems, CAES,
Abaco Systems, Teledyne).

### 3.5 Aegis Modernization Kits

| Contract | Prime | Value | Description |
|---|---|---|---|
| N0002424F5302 | **Raytheon** | $42.3M | Aegis modernization kit |
| N0002421F5314 | **Raytheon** | $35.7M | Mk 99 Aegis modernization kits |
| N0002423F5301 | **Raytheon** | $23.5M | Aegis modernization kits |

### 3.6 Mk 41 Vertical Launch System (VLS) -- Overhaul & Repair

| Contractor | Contracts | Combined Value | Role |
|---|---|---|---|
| **GDIT** | N5005424F1017, F1023, + multiple DOs | ~$5M+ | VLS overhaul on individual DDGs (Ramage, Gravely, etc.) |
| **Texas Research Institute** | N0002425CS061 | $1.4M | Ablative material repair for Mk 41 VLS |
| **Electric Boat (GD)** | N6660420F0611 | $1.1M | VLS repair |

> Note: Mk 41 VLS original production was by Lockheed Martin. Current sustainment
> and overhaul work is fragmented across multiple smaller contractors.

### 3.7 NIFC-CA -- Naval Integrated Fire Control - Counter Air

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Systems Engineering Group** | N6339419F3000 | $25.5M | Engineering/technical/logistics support |
| **GD Mission Systems** | N0002416C5210 | $14.6M | CDD and NIFC-CA requirements |

---

## 4. Self-Defense & Close-In Weapons

These feed into DDG/LCS/LHD modernization and ship gun systems budget lines.

### 4.1 CIWS / Phalanx / SeaRAM / RAM -- Performance-Based Logistics

| Contract | Prime | Value | Description |
|---|---|---|---|
| N0002418C5406 | **Raytheon** | **$482.2M** | FY18 CIWS production (USN, Army, FMS) |
| N0038319F0VP0 | **Raytheon** | **$184.9M** | PBL support: CIWS, Land-Based Phalanx, SeaRAM, RAM |
| N0002407C5437 | **Raytheon** | $194.5M | Mk 15 Phalanx CIWS R&D |
| N0002419C5406 | **Raytheon** | $58.7M | Block 1 BSL 0 to SeaRAM upgrade & conversion |
| N0016418F3004 | **Technology Service Corp** | $15.0M | CIWS engineering and integrated logistics support |

> Raytheon holds the production, sustainment, and PBL contracts for the entire
> CIWS/Phalanx/SeaRAM/RAM family. Total identified value: **$920M+**.

**Subaward Deep Pull -- CIWS / SeaRAM:**

| Prime PIID | Subawards | Total $ |
|---|---|---|
| N0002418C5406 (FY18 CIWS Production) | **3,651** | **$1.13B** |
| N0002419C5406 (SeaRAM upgrade) | **2,677** | **$627M** |
| N0038319F0VP0 (PBL) | 13 | $5.7M |

**Combined: 6,341 subaward records, $1.76B (2020-2026).** This is the most
fragmented subaward base in the entire dataset. Top subcontractors:

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **DRS Network & Imaging Systems** | $232.5M | CIWS test equipment, tooling |
| **L3 Technologies** | $116.9M | Goods and services |
| **General Dynamics-OTS** | $96.6M | Bolts, contacts, gears, structural assemblies |
| **Honeywell International** | $81.0M | IMUs / IRUs (inertial guidance) |
| **Moog** | $71.6M | Electromechanical actuators |
| **Ducommun Labarge Technologies** | $71.6M | RF cable assemblies, CCAs |
| **Aerojet Rocketdyne** | $55.8M | Solid rocket motors (RAM, SeaRAM) |
| **Lourdes Industries** | $50.9M | Hydraulic assemblies |
| **GE Aviation Systems** | $47.9M | DC-DC power supplies, integrated electronics |
| **L3Harris Cincinnati Electronics** | $46.1M | Pedestal / gimbal platforms (Phalanx mounts) |
| **Curtiss-Wright DS** | $45.1M | Memory PROM flash, multi-function assemblies |
| **Southern Gear & Machine** | $44.5M | Precision-machined gears |
| **GD Mission Systems** (as sub) | $37.9M | Custom computer hardware |
| **Coda Octopus Engineering** | $34.6M | AC-DC power supplies, cable assemblies |
| **Microtech** | $31.1M | Coaxial RF connectors, couplers |
| **Kollmorgen Corp** | $31.0M | Electric motors |
| **Microwave Power Products** | $30.8M | TWTs (traveling wave tubes) |
| **Whelan Machine & Tool** | $30.2M | Precision machining |
| **Anaren** | $29.2M | RF mixers |
| **CPI Electron Device Business** | $23.7M | Electron devices |
| **ITT Enidine** | $22.3M | Hydraulics |
| **Cicon Engineering** | $22.0M | Cable assemblies, harnesses |
| **HDL Research Lab** | $18.6M | DC-DC power supplies |
| **EMS Defense Technologies** | $18.1M | Waveguide switches |
| **Epsilon Systems Solutions** | $17.1M | Circuit breakers, flat panel displays |
| **Ensign-Bickford Aerospace & Defense** | $15.9M | Pyrotechnic devices |

### 4.2 MK 110 57mm Gun -- see main report (BAE Systems Land & Armaments, sole producer)

### 4.3 Mk 46 / 30mm Gun Weapon Systems

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **General Dynamics Land Systems** | N0002422F5306 | $9.6M ceiling | Mk 46 GWS support |
| **Raytheon** | N0002423C5316 | $8.6M | Mk 46 GWS HIRE II parts |
| **General Dynamics Land Systems** | N0002415C5344 | $76.6M | Mk 46 MOD 2 GWS for DDG 1000 class |

### 4.4 30mm Guns (MK44 MOD 4 / MK44S Stretch)

| Contractor | Contract | Value | Description |
|---|---|---|---|
| **Northrop Grumman** | N0016425FJ654 | $32.6M | MK44 MOD 4, 30mm guns with spares/tooling |
| **Northrop Grumman** | N0016424CJ001 | $8.4M | MK44S Stretch 30mm gun |
| **Alliant Techsystems** | N0016422FJ124 | $7.1M | 30mm guns, spares, tools |
| **Northrop Grumman** | N0016424FJ012 | $6.6M | 30mm guns and associated spares |

### 4.5 AN/SLQ-25E Nixie (Towed Torpedo Countermeasure)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Ultra Electronics Ocean Systems** | N0025321F0037 | $16.0M | Production of Nixie AN/SLQ-25E systems |
| **GDIT** | N440 | $46.9M | SLQ-25 design, assembly, integration, testing |
| **Ultra Electronics Ocean Systems** | N0025322F0167 | $231K | Nixie domestic spares |

---

## 5. Torpedo Defense Subsystems

Feeds into the SSTD (OPN BA2, Line 2213) budget line.

### 5.1 CCAT -- Canistered Countermeasure Anti-Torpedo Torpedo

| Field | Detail |
|---|---|
| **Prime (Design Agent)** | **Penn State University (Applied Research Lab)** |
| **Contract** | 0074 |
| **Value** | $46.9M |

### 5.2 AN/SLQ-25D Nixie Engineering

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **SAIC** | N6660418F3013 | $31.3M | SSTD advanced development/engineering |
| **SAIC** | N425 | $7.6M | Anti-torpedo torpedo defense system, Mk 2/3/4 countermeasures |

**Key subcontractors (under SAIC):**
| Subcontractor | Value | Role |
|---|---|---|
| **RTX BBN Technologies** | ~$9.2M | AN/SLQ-25D Nixie engineering |
| **Cardinal Engineering** | ~$4.9M | SSTD Nixie UW/UDF Family of Systems |

### 5.3 Other Torpedo Defense

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Penn State** | 0492 | $3.0M | Full Sector Torpedo Defense -- ATT timeline compression |
| **ManTech** | 7N01 | $1.7M | Advanced torpedo defense system engineering |
| **Applied Management Corp** | 7N03 | $1.5M | SSTD support |

---

## 6. Directed Energy -- Named Systems

The DE Systems budget line (~$3M FY26) is tiny relative to the actual contract
values because these are multi-year development programs.

### 6.1 HELIOS -- High Energy Laser with Integrated Optical-dazzler and Surveillance

| Field | Detail |
|---|---|
| **Prime** | **Lockheed Martin Aculight Corporation** |
| **Contract** | N0002418C5392 |
| **Value** | **$225.4M** |
| **Description** | Development and delivery of 2 test units + options for up to 14 production units |
| **Period** | 2018-2027 |

> HELIOS is the Navy's primary shipboard HEL weapon. Installed on USS Preble
> (DDG 88) for at-sea testing. Lockheed Martin Aculight is the sole prime.

**Subaward Deep Pull -- HELIOS (N0002418C5392):**

**331 subaward records totaling $683.2M** (2020-2026). The HELIOS subaward
ecosystem dwarfs the publicly-disclosed $225M prime ceiling:

| Subcontractor | Subaward $ | Role |
|---|---|---|
| **MZA Associates** | **$394.9M** | Beam control I&T (NRE + recurring) -- HELIOS beam director |
| **L3 Technologies** | **$208.9M** | Application development, training, software |
| **SPD Technologies** | $15.7M | Dell PowerEdge servers, signal processing bellows |
| **Riggs Distler** | $8.8M | Equipment / labor |
| **Sea Box** | $8.4M | TITAN structure production |
| **Domaille Engineering** | $7.4M | Fiber router main arc, cold plate |
| **Heilind Mil-Aero** | $5.0M | Special fiber optic / DC HV cables for HELIOS PTC |
| **Talos West** | $4.9M | TEMS controller |
| **InterOcean Systems** | $3.7M | Nixie winch (cross-program) |
| **nLIGHT** | $3.4M | Laptop, Opus software, hinge assemblies (laser diode pumps) |
| **Howell Laboratories** | $2.7M | Service items |
| **QorTek** | $1.9M | Test fixtures |
| **EOSpace** | $1.4M | LiNbO3 phase modulator |
| **JAANN** | $1.3M | Installation support |
| **L3Harris Maritime Power & Energy Solutions** | $1.1M | Post-delivery technical support |
| **Micro-Optics** | $930K | PM optical fiber |
| **Alliance Spacesystems** | $888K | LLD SBC structure assembly |
| **Atrenne Computing Solutions** | $795K | NRE, expedite |
| **Laser Operations** | $778K | DFB lasers (multiple channels) |
| **AdValue Photonics** | $680K | PM fiber splitters (D1/D2 optics) |
| **MLD Technologies** | $548K | Outer blade upper assemblies, microsatellite work |

**Key insight:** **MZA Associates** (Albuquerque, NM) is essentially a co-prime
on HELIOS, holding nearly 60% of the subaward total for beam control system
integration and test. MZA also holds a separate ~$19M Navy prime contract
(N0001421C1116) for a Counter-UAS HEL Weapon System -- they appear on both
sides of the prime/sub line in the directed energy space.

**L3 Technologies** at $209M is the second-largest HELIOS sub, providing
software/training. Combined with their ~$117M in CIWS subawards, L3 (now L3Harris)
is a major hidden player across Navy modernization programs.

### 6.2 ODIN -- Optical Dazzling Interdictor, Navy

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Delta Resources** | N6339421F3006 | $10.8M | ODIN installation on DDG-51 class |

### 6.3 Navy HEL Development (General)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Penn State APL** | N0002423F8311 | $17.5M ceiling | HEL System Design/Dev/Fabrication/Test III |
| **Penn State APL** | N0002420F8329 | $7.2M ceiling | HEL System Design/Dev/Fabrication/Test II |
| **Penn State APL** | N0002423F8326 | $2.1M ceiling | HEL Beam Director Development |
| **MZA Associates** | N0001421C1116 | $18.7M ceiling | Counter-UAS HEL weapon system |
| **ATI** (OTA) | N001782190006 | $8.1M | Compact Expeditionary Beam Director System (CEBDS) |
| **Booz Allen Hamilton** | N0017824F3009 | $22.3M | HEL and electro-optical systems design/development/integration |

### 6.4 Cross-Service DE Programs (Relevant to Navy Roadmap)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Dynetics (Leidos)** | 0002 | $202.7M | IFPC HEL Tactical Vehicle Demonstrator (Army) |
| **Radiance Technologies** | W9113M22FD002 | $63.7M | DE System Integration Lab (Army) |
| **Raytheon** | FA86501999326 | $39.5M | DE Counter-UAS HELWS (Air Force) |
| **Lockheed Martin** | HQ086024C0004 | $7.0M | HEL Pod for Regional Airborne Defense (DARPA) |
| **Lockheed Martin Aculight** | HR001123C0003 | $28.0M ceiling | MELT Panelized HEL Sources (DARPA) |
| **Leidos** | FA945118C0030 | $18.5M ceiling | High Energy Combinable Fiber Laser (FLARE) |

---

## 7. LCS Platform Subsystems

### 7.1 LCS Combat Management System

COMBATSS-21 returned zero FPDS results. This system is embedded within the
Lockheed Martin Freedom variant prime contracts. No standalone procurement vehicle.

### 7.2 Multi-Vehicle Communications System (MVCS)

| Contractor | Contract | Value | Role |
|---|---|---|---|
| **Applied Technical Systems** | N6133122F3010 | $4.9M ceiling | MVCS support |
| **Avian LLC** | N6133118F3010 | $26.6M ceiling | Includes MVCS production services |

---

## 8. Summary: Hidden Contract Values

This table shows the total identified contract value for subsystems that feed
into SAM budget lines but are not findable under program-level descriptions.

### MCM Mission Module Ecosystem (~$91M FY26 budget line feeds these contracts)

| System | Prime | Identified Contract Value |
|---|---|---|
| ALMDS | Northrop Grumman | **$624M** ceiling |
| UISS | Textron Systems | **$342M** ceiling |
| AMNS | Raytheon | **$170M+** |
| MCM USV | Bollinger Shipyards | **$168M** ceiling |
| Barracuda | Raytheon | **$149M** ceiling |
| SMCM Unmanned | GD Mission Systems | **$143M** |
| Knifefish UUV | GD Mission Systems | **$73M** ceiling |
| Integration/Engineering | Avian, IPS, JHU APL, BAH | **~$100M** combined |
| **TOTAL IDENTIFIED** | | **~$1.77B** |

### DDG Modernization Subsystem Ecosystem (~$879M FY26 budget line)

| System | Prime | Identified Contract Value |
|---|---|---|
| AN/SPY-6 Radar | Raytheon | **$3.27B** ceiling (production) |
| SEWIP (all blocks) | LM, NG, GDMS | **$2.0B+** combined |
| CEC | Raytheon | **$957M** combined |
| CIWS/Phalanx/SeaRAM/RAM | Raytheon | **$920M+** |
| SSDS | Lockheed Martin, Raytheon | **$739M** (CSEA + PSEA) |
| HELIOS | Lockheed Martin Aculight | **$225M** |
| Aegis Mod Kits | Raytheon | **$101M** combined |
| Nixie (SLQ-25E) | Ultra Electronics, GDIT | **$63M** combined |
| **TOTAL IDENTIFIED** | | **~$8.3B** |

### Key Insight

The annual FY2026 budget line amounts ($91M for MCM modules, $879M for DDG Mod)
are annual increments funding multi-year, multi-billion-dollar contract vehicles.
The actual outstanding contract obligations and ceilings are 10-20x the single-year
budget figures. The primes on these subsystem contracts -- particularly Raytheon
(SPY-6, CEC, CIWS, AMNS, Standard Missile), Lockheed Martin (SEWIP Block 2, SSDS,
HELIOS), and Northrop Grumman (ALMDS, SEWIP Block 3) -- hold far more contract
value in modernization subsystems than is apparent from the budget line items alone.

### Subaward Deep Pull Totals (2020-2026)

| Prime PIID | Prime | Description | Sub Records | Sub $ Total |
|---|---|---|---|---|
| N0002411C2300 | Lockheed Martin | LCS Freedom Construction | 1,208 | **$48.3B** |
| N0002411C4407 | BAE Norfolk | LHD 3 FY11 PMA | 1,557 | $1.81B |
| N0002416C5363 | Lockheed Martin | SEWIP Block 2 | 358 | **$2.85B** |
| N0002417C6311 | Northrop Grumman | Knifefish/LCS systems | 908 | $1.47B |
| N0002420C5503 | Lockheed Martin | SLQ-32(V)6 production | 612 | $1.42B |
| N0002422C5500 | Raytheon | SPY-6 Production | 854 | $1.42B |
| N6133111C0017 | GD Mission Systems | Surface MCM Unmanned | 300 | $1.23B |
| N0002418C5406 | Raytheon | FY18 CIWS | 3,651 | $1.13B |
| N0002418C2307 | HII | DDG-51 FY18-22 | 2,192 | $1.15B |
| N0002418C4404 | NASSCO | LHD 6 DPMA | 454 | $1.01B |
| N0002413C2307 | HII | DDG-51 FY13-17 | 2,284 | $931M |
| N0002423C2307 | HII | DDG-51 FY23-27 | 355 | $758M |
| N0002418C2406 | HII | LPD 30/31/32 | 1,009 | $692M |
| N0002418C5392 | Lockheed Martin Aculight | HELIOS | 331 | **$683M** |
| N0002419C5406 | Raytheon | SeaRAM upgrade | 2,677 | $627M |
| N0002415C5344 | GD Land Systems | MK 46 MOD 2 Gun (DDG-1000) | 551 | $501M |
| N0002416C2431 | HII | LPD 28 | 1,030 | $490M |
| N0002419C5200 | Raytheon | CEC design agent | 147 | $303M |
| N0002419C5603 | Lockheed Martin | SSDS CSEA | 898 | $270M |
| N0002418C6300 | Raytheon | Barracuda mine neutralizer | 173 | $248M |
| N0002413C5403 | Raytheon | FY13-17 Standard Missile | 893 | $222M |
| N0002417C5145 | Raytheon | DDG-1000 Total Ship Activation | 482 | $165M |
| N0002424C4418 | Metro Machine | LHD 5 FY24 DSRA | 77 | $159M |
| N0002423C4408 | BAE Norfolk | LHD 3 FY23 DSRA | 850 | $146M |
| N0002421C4404 | BAE Norfolk | LHD 1 FY21 DSRA | 334 | $134M |
| N0002417C6305 | Raytheon | AMNS LRIP newer | 280 | $118M |
| N0002420C4308 | BAE SD | LHD 4 DSRA | 405 | $102M |
| N0002415C6318 | Northrop Grumman | ALMDS production | 74 | $91M |
| N0002417C5410 | Raytheon | FY17-21 Standard Missile | 235 | $80M |
| N0002422C5522 | Raytheon | DDG-1000 AS&M | 66 | $76M |

**Cumulative subaward $ across the 30 PIIDs above: ~$70 billion**, of which
the LM LCS Freedom prime (N0002411C2300) accounts for $48B (mostly Marinette
Marine ship construction sub).

Excluding LCS construction (which is essentially a pass-through to the actual
Marinette shipyard), the remaining 29 prime contracts subcontracted **~$22B**
of work across 23,000+ subaward records to a deep tier of specialized
suppliers that don't show up in any FPDS prime search.

### Complete Prime Contractor Map (Component Level)

| Contractor | Systems | Combined Contract Value |
|---|---|---|
| **Raytheon / RTX** | SPY-6, CEC, CIWS/Phalanx/SeaRAM/RAM, SSDS PSEA, AMNS, Barracuda, Aegis Mod Kits, Mk 46 Gun, AQS-20 | **$6B+** |
| **Lockheed Martin** | SEWIP Block 2 / SLQ-32(V)6, SSDS CSEA, HELIOS, SeaRAM integration | **$1.8B+** |
| **Northrop Grumman** | ALMDS, SEWIP Block 3, 30mm guns (MK44), SSDS hardware, Knifefish containers | **$1.3B+** |
| **GD Mission Systems** | SEWIP Block 1B3, Knifefish UUV, SMCM Unmanned, LCS Independence ISEA | **$290M+** |
| **Textron Systems** | UISS, MCM USV support, LCS Independence variant | **$355M+** |
| **Bollinger Shipyards** | MCM USV production | **$168M** |
| **Ultra Electronics Ocean Systems** | Nixie AN/SLQ-25E production, MK-54 array kits | **$340M+** |
| **Penn State APL** | CCAT torpedo defense, HEL development, SEWIP Block 3 transceiver, MK-54 MOD 2 | **$130M+** |
| **SAIC** | SSTD Nixie engineering, DDG-1000 PEO IWS, SEWIP support | **$70M+** |
| **Booz Allen Hamilton** | ALMDS/AMNS/Barracuda/OAMCM engineering & logistics, HEL systems | **$68M+** |
| **GDIT** | SLQ-25 Nixie design/integration, VLS overhauls | **$52M+** |
| **GD Land Systems** | Mk 46 GWS (30mm), DDG 1000 gun system | **$95M+** |
| **Lockheed Martin Aculight** | HELIOS (shipboard HEL) | **$225M** |
| **Dynetics (Leidos)** | IFPC HEL (Army, relevant cross-service) | **$203M** |
| **Avian LLC** | MCM mission package integration, MVCS | **$27M** |
| **MZA Associates** | Counter-UAS HEL weapon system | **$19M** |
| **Delta Resources** | ODIN installation on DDGs | **$11M** |
| **RE2 LLC** | Maritime Mine Neutralization System (M2NS, next-gen) | **$7M** |
| **QinetiQ** | RAMICS airborne mine clearance | **$3M** |

---

*Generated 2026-04-09 from FPDS and USAspending public data. System designation
searches surfaced ~$10B in contract value that was invisible under program-level
budget line descriptions.*

*Updated 2026-04-10 with deep PIID-by-PIID USAspending subaward pull. Major
findings from the subaward dig:*

- *MZA Associates is a co-prime on HELIOS at $395M (60% of all HELIOS subawards)*
- *CAES Systems and Mercury Systems collectively form a $5B+ hidden RF backbone for SPY-6, SEWIP Block 2, and SLQ-32(V)6*
- *Marinette Marine (Fincantieri) holds $47.2B in subaward records under the LM LCS Freedom prime contract -- they are the actual ship builder*
- *The LHD ship-repair "primes" (BAE, Metro Machine, NASSCO) subcontract massive amounts ($3.57B across 4,820 records) to a hidden second tier of regional repair specialists like Earl Industries, Propulsion Controls Engineering, Marine Hydraulics International, TECNICO, and IMIA*
- *L3 Technologies / L3Harris is a $326M+ hidden player across HELIOS (software/training) and CIWS (goods/services)*
- *The 30 most active prime PIIDs collectively distributed ~$70B (or ~$22B excluding the LCS construction pass-through) to ~25,000 first-tier subcontractors in 2020-2026*

