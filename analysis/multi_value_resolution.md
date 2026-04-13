# Multi-Value Row Resolution

Rows in `data_v2.xlsx` where the Bucket or Vessel Hull column contains multiple values, with recommended single-value assignments based on source document investigation.

---

## Multi-Bucket Rows (24 rows)

### Bucket "2|3" — OMN Ship Maintenance (SAG 1B4B) → **Bucket 2**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 1938 | OMN | — | Ship Maintenance | [PARENT] | 13,803,188 |
| 1957 | OMN | — | MSC Other Maintenance and Repair | [SUB] | 575,746 |
| 1973 | OMN | — | Efficiency - Contract Services Reduction | [SUB] | -76,395 |
| 1974 | OMN | — | Efficiency - Workforce Optimization (Public Shipyards) | [SUB] | -207,734 |
| 1976 | OMN | 922 | Equipment Maintenance By Contract | [SUB] | 502,290 |
| 1977 | OMN | 101 | Executive, General and Special Schedules | [SUB] | 3,057,102 |
| 1978 | OMN | 103 | Wage Board | [SUB] | 2,713,903 |
| 1979 | OMN | 412 | Navy Managed Supplies & Materials | [SUB] | 814,422 |
| 1980 | OMN | 424 | DLA Material Supply Chain - Weapon Systems | [SUB] | 696,056 |
| 1983 | OMN | 987 | Other Intra-Government Purchases | [SUB] | 236,115 |

**Source:** OMN_Book.txt, pp. 153–178 (BA1 > Ship Operations > 1B4B Ship Maintenance)

**Finding:** SAG 1B4B genuinely spans both buckets. The description covers "maintenance ranging from overhauls (OH) to restricted and technical availabilities (RA/TA)" (depot-level, Bucket 2) as well as "Non-depot/Intermediate Maintenance supports Fleet Maintenance performed by Navy personnel and civilians on repair ships, aircraft carriers, Intermediate Maintenance Facilities (IMFs), Navy Regional Maintenance Centers (RMCs)" (Bucket 3). The performance criteria table breaks FY25 into depot categories (OH $250M, SRA $384M, PIA $322M, plus $7.5B across four public shipyards) and non-depot categories (Emergent/ERATA $136M, Continuous Maintenance $663M, I-level $1.4B). Depot-level work is approximately 75% of spend.

**Recommendation:** Bucket **2** (Scheduled Depot Maintenance & Repair). Depot-level work dominates at ~75% of spend. The I-level/emergent component is material (~$2.5B) but is the minority share.

---

### Bucket "2|3" — OMN Weapons Maintenance (SAG 1D4D) → **Bucket 3**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 2229 | OMN | — | Weapons Maintenance | [PARENT] | 1,754,627 |

**Source:** OMN_Book.txt, p. 21 (BA1 > Weapons Support > 1D4D Weapons Maintenance)

**Finding:** Covers "a wide range of weapons system maintenance and support functions" including "operational maintenance support, intermediate maintenance, depot level maintenance and overhaul of systems and sub-system components" for missiles, ordnance, gun systems, ASW systems, mine warfare systems, UAS/USV/UUV, etc. Despite mentioning "depot level maintenance," this is weapons component maintenance performed at Fleet Readiness Centers, munitions commands, and commercial depots on a continuous/rolling basis — not CNO-scheduled ship availabilities. None of the Bucket 2 keywords apply (no DSRA, SRA, DPMA, PMA, PIA, ROH, drydock).

**Recommendation:** Bucket **3** (Continuous / Intermediate / Emergent Maintenance). Weapons systems sustainment performed continuously across organizational, intermediate, and depot levels — distinct from scheduled ship depot availabilities.

---

### Bucket "2,3" — USCG O&S Reference Rows → **Bucket 3**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 3352 | USCG | — | Surface Air and Shore Operations (PPA Level II) | [REFERENCE] | 3,425,335 |
| 3353 | USCG | — | Operation and Maintenance of Equipment (Field Ops OC 25.7) | [REFERENCE] | 969,498 |
| 3354 | USCG | — | Commercial Icebreaker Follow-On (O&S program change) | [REFERENCE] | 16,279 |
| 3355 | USCG | — | Fast Response Cutter (FRC) Follow-On (O&S program change) | [REFERENCE] | 13,447 |
| 3356 | USCG | — | Offshore Patrol Cutter (OPC) Follow-On (O&S program change) | [REFERENCE] | 1,027 |
| 3357 | USCG | — | Waterways Commerce Cutter (WCC) Follow-On (O&S program change) | [REFERENCE] | 4,365 |
| 3359 | USCG | — | Indo-Pacific Expansion (O&S program change) | [REFERENCE] | 116,405 |

**Source:** USCG_Justification.txt, pp. 34–61

**Finding:** The five "O&S program change" rows (3354–3359) fund initial operational standup of newly delivered assets — crew, O&M, homeport support, logistics. Example: FRC Follow-On "funds personnel, O&M, and mission support elements for four FRCs scheduled for delivery in FY 2026." OPC Follow-On is "almost entirely crew/personnel costs for a cutter not yet delivered." None describe planned depot events.

The two broader reference rows — Surface/Air/Shore Operations PPA ($3.4B) covers day-to-day fleet operations; OC 25.7 ($969M) covers all forms of equipment maintenance. The legislative language carves out only $400M across the entire O&S appropriation for depot-level maintenance, confirming depot work is a minority of the broader O&S spending.

**Recommendation:** Bucket **3** (Continuous / Intermediate / Emergent Maintenance) for all seven rows. These are operational O&S costs — crew, fuel, continuous maintenance, and fleet support — not scheduled depot events.

---

### Bucket "2/4" — OPN BA01 Ship Maintenance Repair & Modernization (LI 26) → **Bucket 2**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 2682 | OPN_BA1 | 26 | Ship Maintenance Repair and Modernization | [PARENT] | 2,392,620 |
| 2683 | OPN_BA1 | 26-CPF | Ship Maint Repair & Mod > U.S. Pacific Fleet Availabilities | [SUB] | 1,306,538 |
| 2684 | OPN_BA1 | 26-FFC | Ship Maint Repair & Mod > U.S. Fleet Forces Availabilities | [SUB] | 1,086,082 |

**Source:** OPN_BA1_Book.txt, p. 521 (BSA 10 Reactor Plant Equipment > P-40 LI 1000)

**Finding:** Despite "Modernization" in the title, this line item was created by Congress specifically to fund "private contracted ship maintenance." The justification states: "Funding for ship maintenance Overhauls (OH) to Restricted/Technical Availabilities (RA/TA) performed at private shipyards. Ship overhauls restore the ship, including all operating systems that affect safety or combat capability, to established performance standards." The P-5 cost breakdown lists every element as a named ship with a depot-level availability type — DSRA, SRA, DPMA, DMP, PIA, DPIA, EOH. The OPN appropriation was chosen for contracting flexibility (A-120 policy), not because the work is modernization. The language is about restoring ships to performance standards — maintenance, not configuration change.

**Recommendation:** Bucket **2** (Scheduled Depot Maintenance & Repair). Classic depot availability work (DSRA, SRA, DPMA, PIA, EOH) performed at private shipyards. The "Modernization" in the title is a misnomer.

---

### Bucket "4/6" — OPN BA03 Meteorological Equipment (LI 118) → **Bucket 4**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 2913 | OPN_BA3 | 118 | Meteorological Equipment | [PARENT] | 13,806 |

**Source:** OPN_BA3_Book.txt, p. 153 (P-40a / BSA03 Aircraft Support Equipment / LI 4226)

**Finding:** Procurement of new and upgraded equipment: 3 ESRP Afloat Modernized Systems (satellite receiver upgrades), 13 ASOS upgrades and 9 SWR upgrades (system life extension, DMSMS mitigation, cyber risk mitigation), 12 ocean gliders (replacements), 11 NIMS sensors (new tactical METOC systems), 2 HWDDC EASR software/hardware upgrades (AN/SPY-6 integration). Language consistently uses "modernization," "upgrades," and "backfits." While one sub-project mentions DMSMS, the actual work product is procured hardware upgrades, not engineering/planning services.

**Recommendation:** Bucket **4** (Modernization & Alteration Installation). Procurement-funded equipment upgrades and backfits being installed across the fleet.

---

### Bucket "4/6" — OPN BA03 Aviation Support Equipment (LI 121) → **Bucket 4**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 2931 | OPN_BA3 | 121 | Aviation Support Equipment | [PARENT] | 111,334 |

**Source:** OPN_BA3_Book.txt, p. 169 (P-40 / BSA03 Aircraft Support Equipment / LI 4268)

**Finding:** Four sub-elements, all focused on procurement and installation:
- **Other Aviation Support Equipment ($9.7M)** — IT hardware, servers, COTS software for JTDI, NALCOMIS, CBM+, Digital Production Floor.
- **Aviation Life Support ($80.0M)** — Procurement of helmets (IJHMCS, HPH, NGRWH), survival vests, hearing protection, physiological monitors.
- **Aviation Maintenance Advancement Solutions ($17.6M)** — PEMA hardware with SPECS software.
- **ALIS Ship Installation ($4.1M)** — Explicitly labeled "Add Capability." Installation of F-35 ALIS systems on CVN/LHD/LHA ships — textbook SHIPALT/backfit.

**Recommendation:** Bucket **4** (Modernization & Alteration Installation). All four sub-elements procure and install new/upgraded equipment. The language is dominated by "procurement," "fielding," "tech refresh," "installation," and "add capability."

---

### Bucket "1,4,5" — USCG Vessels PPA → **Bucket 1**

| Row | Source | LI | Title | Row Type | FY26 ($K) |
|-----|--------|-----|-------|----------|-----------|
| 3326 | USCG | — | Vessels PPA | [PARENT] | 1,439,300 |

**Source:** USCG_Justification.txt, p. 73 (PC&I > Vessels - PPA)

**Finding:** FY26 spend breakdown:

| Program | FY26 ($M) | Bucket |
|---------|-----------|--------|
| Offshore Patrol Cutter (OPC) | 812.4 | 1 — New Construction |
| Fast Response Cutter (FRC) | 216.0 | 1 — New Construction |
| Polar Security Cutter (PSC) | 130.0 | 1 — New Construction |
| Waterways Commerce Cutter (WCC) | 98.0 | 1 — New Construction |
| Boats | 30.9 | 1 — New Construction |
| In-Service Vessel Sustainment (ISVS) | 152.0 | 5 — SLEP/MMA |
| **Total** | **1,439.3** | |

New construction programs account for 89.4% of the PPA ($1,287M). The ISVS component ($152M) includes 47-ft MLB SLEP ($45M), 270-ft WMEC SLEP ($76M), 175-ft WLM MMA ($15M), CGC Healy SLEP ($11M), and 418-ft NSC MMA ($5M) — all Bucket 5. No meaningful Bucket 4 content was identified. The SLEPs "increase service life without significantly modifying capabilities."

**Recommendation:** Bucket **1** (New Construction). Dominates at 89.4%. Note that ~$152M (10.6%) is SLEP/MMA (Bucket 5), but this is a minority share of the parent row.

---

## Multi-Vessel Hull Rows (25 rows)

### SSBN / SSGN → **SSBN** (22 rows)

All Ohio-class submarine rows. Both SSBN and SSGN designations refer to the same Ohio-class hull; the four SSGN conversions (726–729) were originally SSBNs. SSBN is the canonical hull designation for the class.

| Rows | Source | Context |
|------|--------|---------|
| 1960, 1966, 1995 | OMN | Public shipyard inductions and SRAs |
| 2367, 2372, 2374, 2378, 2382, 2393, 2401, 2531, 2533, 2538, 2539 | OMN_Vol2 | ERO, ERP, MMP availability schedules |
| 2712, 2715, 2720, 2749 | OPN_BA2 | Strategic platform support equipment |
| 3103 | OPN_BA4 | SSBN modernization tech insertion |
| 3248, 3250 | OPN_BA5-8 | Strategic platform/missile systems replenishment |
| 3257 | WPN | TRIDENT II D5 Life Extension |

### T-AK / T-AKR → **T-AKR** (2 rows)

Strategic sealift vessels. T-AKR (vehicle cargo ships) is the dominant hull type in the strategic sealift fleet.

| Row | Source | LI | Title |
|-----|--------|----|-------|
| 55 | SCN | — | Strategic Sealift |
| 80 | SCN | 5201 | Auxiliary Vessels (Used Sealift) |

### SUSV / VSUSV → **SUSV** (1 row)

Small Unmanned Surface Vehicle. SUSV is the standard designation.

| Row | Source | LI | Title |
|-----|--------|----|-------|
| 2245 | OMN | — | Small Unmanned Surface Vehicle (sUSV) |

---

## Summary of Changes

| Rows | Current Value | Recommended Value | Column |
|------|---------------|-------------------|--------|
| 1938, 1957, 1973–1974, 1976–1980, 1983 | 2\|3 | 2 | Bucket |
| 2229 | 2\|3 | 3 | Bucket |
| 3352–3357, 3359 | 2,3 | 3 | Bucket |
| 2682–2684 | 2/4 | 2 | Bucket |
| 2913 | 4/6 | 4 | Bucket |
| 2931 | 4/6 | 4 | Bucket |
| 3326 | 1,4,5 | 1 | Bucket |
| 1960, 1966, 1995, 2367, 2372, 2374, 2378, 2382, 2393, 2401, 2531, 2533, 2538, 2539, 2712, 2715, 2720, 2749, 3103, 3248, 3250, 3257 | SSBN / SSGN | SSBN | Vessel Hull |
| 55, 80 | T-AK / T-AKR | T-AKR | Vessel Hull |
| 2245 | SUSV / VSUSV | SUSV | Vessel Hull |
