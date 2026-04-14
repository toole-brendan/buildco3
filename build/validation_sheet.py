"""
validation_sheet.py — Builds the Validation & Data Dictionary sheet.

Separated from build_from_data.py to keep the main build script concise.
Uses the same style primitives (title_band, subsec_band, etc.) via import.
"""

from build_from_data import (
    cw, wc, title_band, subsec_band, subsubsec_band,
    purpose_row, hdr_row, finish_sheet,
    F_DATA, F_GRAY,
)

def create_validation_sheet(wb):
    """Build the Validation & Data Dictionary sheet."""
    ws = wb.create_sheet('Validation')
    mc = 3
    cw(ws, 1, 35); cw(ws, 2, 70); cw(ws, 3, 50)

    def _dr(r, a, b, c=None):
        wc(ws, r, 1, a, font=F_DATA)
        wc(ws, r, 2, b, font=F_DATA)
        if c: wc(ws, r, 3, c, font=F_GRAY)

    def _nr(r, text):
        wc(ws, r, 1, text, font=F_GRAY)

    r = 1; title_band(ws, r, 'Validation & Data Dictionary', mc)
    r = 2; purpose_row(ws, r,
        'Data dictionary, validation rules, and taxonomy reference '
        'for the consolidated line-item dataset')

    # ── Row Types ────────────────────────────────────────────
    r = 4; subsec_band(ws, r, 'Row Types', mc)
    r += 1; purpose_row(ws, r,
        'Tags in the Row Type column (col E) classify how each line item '
        'participates in aggregation. Determines which rows are summed for TAM totals.')
    r += 1; hdr_row(ws, r, [('Tag', 35), ('Description', 70), ('Aggregation Rule', 50)])
    for tag, desc, rule in [
        ('(no tag)',
         'Additive \u2014 standalone budget line item whose funding is not double-counted elsewhere.',
         'TAM = sum of all (no tag) + [PARENT] rows'),
        ('[PARENT]',
         'Parent row \u2014 holds aggregate total; [SUB] children break it into components.',
         'Include in TAM sum alongside (no tag). Do NOT also sum [SUB] children.'),
        ('[SUB]',
         'Sub-item breakdown of a parent. Provides granular detail but double-counts if summed with parent.',
         'Exclude from TAM if summing [PARENT]. Parent Item column points to parent row.'),
        ('[ALT_VIEW]',
         'Alternative cut of the same money \u2014 e.g., P-5c cost breakdowns vs. P-40 line items.',
         'Always exclude from TAM sums. Parent Item indicates the alternative-view source.'),
        ('[UNFUNDED]',
         'Deferred maintenance or unfunded requirements \u2014 real need but NOT in enacted/requested funding.',
         'Exclude from TAM. Useful for gap analysis (funded vs. required).'),
        ('[REFERENCE]',
         'Context data that is not additive \u2014 unit costs, O&S program changes, revolving fund notes.',
         'Exclude from TAM. Included for analytical context only.'),
    ]:
        r += 1; _dr(r, tag, desc, rule)

    # ── Market Scope: Total Funding → TAM → SAM ─────────────
    r += 2; subsec_band(ws, r, 'Market Scope: Total Funding \u2192 TAM \u2192 SAM', mc)
    r += 1; purpose_row(ws, r,
        'How the workbook narrows from total budget authority to the addressable market. '
        'Each analysis sheet\'s row 2 carries the canonical scope definition.')

    for name, defn in [
        ('Total Funding',
         'All USN, MSC & USCG budget authority for any type of work on any type of vessel \u2014 '
         'from new construction through depot maintenance, modernization, sustainment, and end-of-life. '
         'Includes line items that lack vessel type or work type attribution.'),
        ('Newbuild TAM',
         'Total Funding narrowed to new construction only and only oceangoing vessels \u2014 '
         'excludes small craft (Combatant Crafts, Support Crafts) and USCG Boats. '
         'Limited to line items with clear vessel type designation; unattributed fleet-wide items are excluded.'),
        ('Newbuild SAM',
         'Outsourceable new construction sized at cost-element level. Starts from Newbuild TAM, '
         'excludes single-yard/nuclear programs (Submarines, Aircraft Carriers, UUVs), then narrows '
         'to hull programs with P-5c exhibit data. The SAM (cost-element coverage) is the P-5c '
         'percentage mix applied to net budget authority \u2014 the market a company could compete in, '
         'broken by component. SAM (all programs) retains the broader vessel-type scope.'),
        ('MRO TAM',
         'Total Funding narrowed to all post-construction work \u2014 depot maintenance, '
         'continuous & emergent repair, modernization & alterations, major life-cycle events, '
         'sustainment engineering, and availability support \u2014 and only oceangoing vessels. '
         'Same vessel scope as Newbuild TAM; limited to line items with clear vessel type designation.'),
        ('MRO SAM',
         'MRO TAM narrowed to outsourceable work types (scheduled depot maintenance, '
         'continuous/emergent maintenance, modernization/alteration installation, '
         'and major life-cycle events) and outsourceable vessel types (excludes '
         'Submarines, Aircraft Carriers & UUVs). Sized at hull-program level. '
         'Includes aggregate SDM cost-element estimation derived from OMN Ship Maintenance '
         'sub-component data \u2014 applies a single aggregate cost mix (government labor, '
         'contract, materials, etc.) to per-hull SDM totals as a directional approximation.'),
    ]:
        r += 2; subsubsec_band(ws, r, name, mc)
        r += 1; wc(ws, r, 1, defn, font=F_DATA)

    # TAM formula & aggregation rules
    r += 2; subsubsec_band(ws, r, 'TAM Formula & Aggregation', mc)
    r += 1; hdr_row(ws, r, [('Rule', 35), ('Description', 70), ('Notes', 50)])
    for rule, desc, notes in [
        ('TAM formula',
         'TAM = SUM(FY_Best) WHERE Row_Class = "ADD". Pre-computed in helper columns: '
         'Row Class (col AC), FY26 Best (col AD), FY27 Best (col AE).',
         'FY26 cascade: DAA Enacted (Y) > Total (U) > Request (S). FY27: Total (AB) > Request (Z).'),
        ('Double-counting guard',
         'Never sum [PARENT] and its [SUB] children together. '
         'Never sum [ALT_VIEW] with either [PARENT] or (no tag) rows.', None),
        ('OPN_BA4 convention',
         'OPN_BA4 has zero (no tag) rows \u2014 all items are [PARENT] or [SUB]. '
         'TAM for BA4 = sum of [PARENT] rows only.', None),
        ('Cross-book overlap',
         'NWCF and OMN fund some of the same activities '
         '(NWCF is a revolving fund reimbursed by OMN). Use Source_Book to isolate.', None),
    ]:
        r += 1; _dr(r, rule, desc, notes)

    # Outsourceable work types
    r += 2; subsubsec_band(ws, r, 'Outsourceable Work Types (SAM-eligible)', mc)
    r += 1; purpose_row(ws, r,
        'Work types a non-incumbent shipyard could compete for \u2014 these define SAM scope')
    r += 1; hdr_row(ws, r, [('Work Type', 35), ('Description', 70), ('Bucket', 50)])
    for wt, desc, bkt in [
        ('New Construction', 'Detail design, construction, and delivery of new vessels', 'Bucket 1'),
        ('Scheduled Depot Maintenance', 'CNO-scheduled depot-level maintenance availabilities', 'Bucket 2'),
        ('Continuous / Emergent Maintenance', 'Intermediate-level and emergent repair, continuous maintenance', 'Bucket 3'),
        ('Modernization & Alteration', 'Combat system upgrades, hull/mech/elec modernization', 'Bucket 4'),
        ('Major Life-Cycle Events', 'SLEP, MMA, RCOH \u2014 major overhauls extending service life', 'Bucket 5'),
    ]:
        r += 1; _dr(r, wt, desc, bkt)
    r += 1; _nr(r,
        'Excluded: Sustainment Engineering (6), Availability Support (7)')

    # TAM vessel categories
    r += 2; subsubsec_band(ws, r, 'TAM Vessel Category Scope', mc)
    r += 1; hdr_row(ws, r, [('Category', 35), ('TAM Scope', 70), ('Notes', 50)])
    for cat, scope, notes in [
        ('Combatant Ships', 'YES \u2192 TAM', None),
        ('Auxiliary Ships', 'YES \u2192 TAM', None),
        ('Cutters', 'YES \u2192 TAM', 'USCG'),
        ('Unmanned Maritime Platforms', 'YES \u2192 TAM', None),
        ('Combatant Crafts', 'No \u2014 small craft', 'Excluded'),
        ('Support Crafts', 'No \u2014 non-oceangoing', 'Excluded'),
        ('Boats', 'No \u2014 under 65 ft', 'USCG \u2014 excluded'),
    ]:
        r += 1; _dr(r, cat, scope, notes)

    # SAM vessel type exclusions
    r += 2; subsubsec_band(ws, r, 'SAM Vessel Type Exclusions', mc)
    r += 1; hdr_row(ws, r, [('Vessel Type', 35), ('Reason', 70), ('Notes', 50)])
    for vt, reason, notes in [
        ('Submarines', 'Nuclear-only yards \u2014 only two US facilities can build nuclear submarines',
         'Electric Boat (CT) and Newport News (VA)'),
        ('Aircraft Carriers', 'Newport News monopoly \u2014 single-source production',
         'Huntington Ingalls Industries'),
        ('Unmanned Undersea Vehicles', 'Specialized programs with limited competition', None),
    ]:
        r += 1; _dr(r, vt, reason, notes)

    # ── Work Type Buckets ────────────────────────────────────
    r += 2; subsec_band(ws, r, 'Work Type Buckets (1\u20137)', mc)
    r += 1; purpose_row(ws, r,
        'Seven-bucket taxonomy classifying all types of work performed on vessels, '
        'from new construction through end-of-life support')
    r += 1; hdr_row(ws, r, [('Bucket', 35), ('Description', 70), ('Budget Anchors / Keywords', 50)])
    for num, name, desc, kw in [
        ('1', 'New Construction',
         'Design, construction, and delivery of new vessels from detail design through sea trials.',
         'SCN (Navy), PC&I (USCG). Keywords: DD&C, LLTM, advance procurement.'),
        ('2', 'Scheduled Depot Maintenance & Repair',
         'Planned depot-level work to restore/sustain material condition during CNO-scheduled availabilities.',
         'O&M,N SAG 1B4B Ship Depot Maintenance. Keywords: DSRA, SRA, DPMA, PMA, PIA, ROH, drydock.'),
        ('3', 'Continuous / Intermediate / Emergent Maintenance',
         'Shorter-duration, intermediate-level, continuous, and emergent/casualty work outside the depot event.',
         'Keywords: CMAV, WOO, EM, emergent, casualty repair, voyage repair, dockside.'),
        ('4', 'Modernization & Alteration Installation',
         'Work that changes configuration or adds capability beyond restore-only repair. Funded primarily through procurement.',
         'OPN P-40 line items (DDG Mod, CG Mod, LCS Mod). Keywords: SHIPALT, ORDALT, tech refresh, backfit.'),
        ('5', 'Major Life-Cycle Events / SLEP / MMA / RCOH',
         'Multi-year platform- or class-scale recapitalization that gets its own budget line.',
         'Keywords: RCOH, EOH, SLEP, MMA, midlife. Separate from routine depot maintenance (Bucket 2).'),
        ('6', 'Sustainment Engineering / Planning / Obsolescence',
         'Engineering, planning, DMSMS/obsolescence, and program support for in-service vessels.',
         'O&M,N SAG 1B5B Ship Depot Ops Support; OPN spares (BA08). Keywords: SETA, DMSMS, survey & design.'),
        ('7', 'Availability Support / Husbanding / Port Services',
         'Services that enable repair/modernization but are not themselves repair or upgrade work.',
         'Keywords: husbanding, pilot, tug, berthing, crane, shore power, scaffolding, environmental.'),
    ]:
        r += 1; _dr(r, f'{num} \u2014 {name}', desc, kw)

    # Bucket 1 sub-categories
    r += 2; subsubsec_band(ws, r, 'Bucket 1 Sub-Categories', mc)
    r += 1; hdr_row(ws, r, [('Sub-Category', 35), ('Description', 70), ('Examples', 50)])
    for sub, desc, ex in [
        ('Full ship DD&C',
         'Detail design and construction of a complete vessel.',
         'DDG-51, FFG-62, CVN-79, LPD, LHA, T-AO, OPC, FRC, PSC'),
        ('Advance procurement / LLTM',
         'Long-lead time material and advance procurement funded 1\u20132 years ahead of DD&C.',
         'Reactor components, propulsion equipment, combat system long-lead items'),
        ('Construction engineering / planning yard',
         'Lead yard support, planning yard services, and design completion work.',
         'EB submarine planning yard, Columbia design completion'),
        ('GFE / combat systems for newbuild',
         'Government-furnished equipment / combat systems procured separately from hull construction (via OPN or RDT&E).',
         'Funded through OPN, not SCN \u2014 but supports new construction'),
    ]:
        r += 1; _dr(r, sub, desc, ex)

    # Bucket 2-7 sub-categories
    r += 2; subsubsec_band(ws, r, 'Bucket 2\u20137 Sub-Categories', mc)
    r += 1; hdr_row(ws, r, [('Sub-Category', 35), ('Description', 70), ('Coverage', 50)])
    for sub, desc, cov in [
        ('Bkt 2: Scheduled Depot Maintenance', 'CNO-scheduled depot-level maintenance availabilities.', '113 rows'),
        ('Bkt 2: Ship Availability', 'Ship availability periods for maintenance and repair work.', '105 rows'),
        ('Bkt 4: GFE / combat systems', 'Government-furnished equipment and combat system modernization.', 'Shared with Bucket 1'),
        ('Bkt 5: RCOH', 'Refueling Complex Overhaul \u2014 multi-year nuclear carrier recapitalization.', '187 rows'),
        ('Bkt 5: SLEP', 'Service Life Extension Program \u2014 extends platform beyond original design life.', '6 rows'),
        ('Bkt 6: Sustainment Eng. \u2014 spares', 'Spare parts procurement for sustainment engineering and obsolescence (OPN BA08).', '14 rows'),
        ('Bkt 7: Availability Support', 'Services enabling repair/mod \u2014 husbanding, port services, crane, scaffolding.', '76 rows'),
        ('Other: Full vessel procurement', 'USCG full vessel procurement \u2014 equivalent to Full ship DD&C for Coast Guard.', '6 rows'),
        ('Other: Full ship DD&C / LLTM', 'Combined full ship construction and long-lead time material in a single line item.', '3 rows'),
    ]:
        r += 1; _dr(r, sub, desc, cov)

    # Composite bucket values
    r += 2; subsubsec_band(ws, r, 'Composite Bucket Values', mc)
    r += 1; _dr(r, 'Multi-bucket line items',
        'Some line items span multiple work types. Bucket value uses a delimiter (pipe, comma, or slash): 2|3, 2,3, 2/4, 4/6, 1,4,5.',
        'Correctly excluded from per-bucket TAM sums (SUMPRODUCT checks fail on composite strings).')
    r += 1; _dr(r, 'TAM impact',
        'Composite-bucket rows excluded from TAM-by-work-type pivot because SUMPRODUCT checks D=1, D=2, etc. \u2014 '
        'a string like "2|3" fails all single-integer tests.',
        'To capture, filter Bucket for non-integer values.')

    # ── Vessel Taxonomy ──────────────────────────────────────
    r += 2; subsec_band(ws, r, 'Vessel Taxonomy', mc)
    r += 1; purpose_row(ws, r,
        'Four-column hierarchy: Vessel Service \u2192 Category \u2192 Type \u2192 Hull. '
        'Each column progressively more specific. All 4 may be populated or only broader levels.')

    _usn_cats = [
        ('Combatant Ships', True, 'Warships and other combatant vessels \u2014 the core fighting and logistics fleet.', [
            ('Aircraft Carriers', 'Nuclear-powered aircraft carriers', 'CVN'),
            ('Surface Combatants', 'Guided-missile cruisers, destroyers, frigates, littoral combat ships', 'CG, DDG, FFG, LCS'),
            ('Submarines', 'Attack submarines, ballistic missile submarines, guided-missile submarines', 'SSN, SSBN, SSGN'),
            ('Amphibious Warfare Ships', 'Amphibious assault ships and transport docks', 'LHA, LHD, LPD, LSD'),
            ('Mine Warfare', 'Mine countermeasure ships', 'MCM'),
            ('Combat Logistics Ships', 'Oilers, ammunition ships, dry cargo/ammunition ships', 'AO, AOE, AOL, AKE'),
            ('Command Ships', 'Afloat command and control platforms', 'LCC'),
            ('Material Support Ships', 'Submarine tenders', 'AS'),
            ('Surveillance Ships', 'Ocean surveillance ships', 'AGOS'),
            ('Salvage Ships & Fleet Ocean Tugs', 'Rescue/salvage ships and fleet tugs', 'ARS, ATF, ATS'),
            ('Expeditionary & Seabasing Ships', 'Expeditionary fast transports, sea bases, medium landing ships', 'EPF, ESB, ESD, LSM'),
        ]),
        ('Auxiliary Ships', True, 'Non-combatant support vessels \u2014 research, cargo, hospital, special-purpose.', [
            ('Crane Ship', 'Floating crane ship', 'ACS'),
            ('General Auxiliary', 'Multi-purpose auxiliary vessels', 'AG'),
            ('Research, Survey & Instrumentation Ships', 'Oceanographic and survey ships', 'AGM, AGOR, AGS'),
            ('Hospital Ship', 'Hospital ships', 'AH'),
            ('Cargo & Vehicle Cargo Ships', 'Cargo and vehicle transport ships', 'AK, AKR'),
            ('Transport Oiler', 'Transport oilers', 'AOT'),
            ('Cable Repairing Ship', 'Submarine cable repair ships', 'ARC'),
            ('Aviation Logistics Support Ship', 'Aviation support ships', 'AVB'),
            ('High Speed Transport', 'High speed transports', 'HST'),
            ('Submarine Escort Ship', 'Submarine escort/support vessels', 'AGSE'),
            ('USS Constitution', 'Historic warship \u2014 not operationally classified', '\u2014'),
        ]),
        ('Combatant Crafts', False, 'Smaller combatant craft \u2014 patrol, landing, and special warfare.', [
            ('Patrol Combatant', 'Coastal patrol craft', 'PC'),
            ('Amphibious Warfare Craft', 'Landing craft \u2014 air cushion and utility', 'LCAC, LCU'),
            ('Patrol Boats', 'Various patrol boats by length', '36PB, 64PB, 87PB'),
            ('Special Warfare Craft', 'Naval Special Warfare craft and swimmer delivery vehicles', 'DSB, CCA, CCM, CCH, NSW RHIB, SDV, SWCS, SSC'),
        ]),
        ('Unmanned Maritime Platforms', True, 'Unmanned surface and undersea vehicles.', [
            ('Unmanned Surface Vehicles', 'Large, medium, small, and very small USVs', 'LUSV, MUSV, SUSV, VSUSV'),
            ('Unmanned Undersea Vehicles', 'Extra-large, large, medium, and small UUVs', 'XLUUV, LUUV, MUUV, SUUV'),
        ]),
        ('Support Crafts', False, 'Yard craft, barges, tugs, and harbor support vessels.', [
            ('Dry Docks', 'Floating dry docks', 'AFDL, ARDM, AFDM'),
            ('Harbor Tugs', 'Yard and harbor tugboats', 'YT, YTB, YTL'),
            ('Lighters & Barges', 'Non-self-propelled barges and lighters', 'YC, YCV, YFN, YFNX, YFNB, YON, YOS, YWN, YWO'),
            ('Other Craft, Self-Propelled', 'Misc. self-propelled yard and special craft', 'FSF, SBX, YFB, YP, YSD, YDT, YTT'),
            ('Other Craft, Non-Self-Propelled', 'Berthing barges, floating workshops, misc. non-propelled', 'APL, YD, YFND, YFP, YR, YRB, YRBM, YRDH, YRDM, IX'),
            ('Sealift Support Craft', 'Sealift and marine pre-positioning support craft', 'INLS, LCM 8, LARC V, MPF UB, OPDS UB'),
            ('Ships Boats', 'Motor rescue boats carried aboard ships', '5MRB, 7MRB, 11MRB'),
            ('Shore-Based Harbor Security Boats', 'Harbor security patrol boats', '27HS, 28HS, 32HS, 33HS, 11MHS, 35HS, 36HS'),
        ]),
    ]

    r += 2; subsubsec_band(ws, r, 'USN \u2014 United States Navy', mc)
    r += 1; _nr(r, 'Commissioned warships and support craft with Navy crews.')
    for cat, in_tam, cat_desc, types in _usn_cats:
        scope = '(TAM scope)' if in_tam else '(excluded from TAM)'
        r += 2; subsubsec_band(ws, r, f'{cat} {scope}', mc)
        r += 1; _nr(r, cat_desc)
        r += 1; hdr_row(ws, r, [('Type', 35), ('Description', 70), ('Hull Designators', 50)])
        for tname, tdesc, hulls in types:
            r += 1; _dr(r, tname, tdesc, hulls)

    # MSC
    r += 2; subsubsec_band(ws, r, 'MSC \u2014 Military Sealift Command', mc)
    r += 1; _nr(r,
        'Civilian-crewed ships using T- prefix (e.g., T-AO, T-AKE, T-EPF). '
        'Shares USN categories and types. Service column = MSC when hull starts with T-.')
    r += 1; _nr(r,
        'Examples: T-AO (Combat Logistics), T-AGOS (Surveillance), T-EPF (Expeditionary & Seabasing)')

    # USCG
    _uscg_cats = [
        ('Cutters', True, 'Coast Guard cutters \u2014 65 feet and larger.', [
            ('Icebreakers, Oceangoing', 'Heavy polar icebreakers', 'WAGB'),
            ('Icebreakers, Great Lakes', 'Great Lakes icebreaking cutters', 'WLBB'),
            ('National Security Cutters', 'Legend-class national security cutters', 'WMSL'),
            ('High Endurance Cutters', 'Hamilton-class high endurance cutters (retiring)', 'WHEC'),
            ('Medium Endurance Cutters', '270-foot and 210-foot medium endurance cutters', 'WMEC'),
            ('Offshore Patrol Cutter', 'Heritage-class offshore patrol cutters', 'WMSM'),
            ('Fast Response Cutters', 'Sentinel-class fast response cutters', 'WPC'),
            ('Patrol Boats', 'Marine Protector-class patrol boats', 'WPB'),
            ('Seagoing Buoy Tenders', 'Juniper-class seagoing buoy tenders', 'WLB'),
            ('Coastal Buoy Tenders', 'Keeper-class coastal buoy tenders', 'WLM'),
            ('Inland Construction Tenders', 'Inland construction tenders', 'WLIC'),
            ('Ice Breaking Tugs', 'Ice-breaking harbor tugs', 'WTGB'),
            ('River Buoy Tenders', 'River buoy tenders', 'WLR'),
            ('Inland Buoy Tenders', 'Inland buoy tenders', 'WLI'),
            ('Small Harbor Tugs', '65-foot small harbor tugs', 'WYTL'),
            ('Barque Eagle', 'USCG training sailing vessel', 'WIX'),
        ]),
        ('Boats', False, 'Coast Guard boats \u2014 under 65 feet.', [
            ('Response Boats', 'Motor lifeboats, response boats, transportable port security boats', 'MLB, RB-M, TPSB, RB-S II, UTM, UTL'),
            ('Aids to Navigation Boats', 'Boats supporting aids to navigation mission', 'ANB, BUSL, TANB, AB-S, AB-SKF'),
            ('Cutter Boats', 'Small boats deployed from cutters', 'CB-LRI, CB-OTH, ASB/LC, MSB, CB-L, CB-ATON, CB-M, CB-S, UTL'),
            ('Special Purpose Craft', 'Specialized mission craft', 'SPC-SV, SPC-TTB, SPC-TB, SPC-LE, SPC-BTD, SPC-LEO, SPC-SW, SPC-IRT, SKF-ICE, SKF'),
            ('Training Craft', 'Academy and training center craft', 'CT-64, SB'),
        ]),
    ]

    r += 2; subsubsec_band(ws, r, 'USCG \u2014 United States Coast Guard', mc)
    r += 1; _nr(r, 'Cutters and boats. Part of DHS, not DoD.')
    for cat, in_tam, cat_desc, types in _uscg_cats:
        scope = '(TAM scope)' if in_tam else '(excluded from TAM)'
        r += 2; subsubsec_band(ws, r, f'{cat} {scope}', mc)
        r += 1; _nr(r, cat_desc)
        r += 1; hdr_row(ws, r, [('Type', 35), ('Description', 70), ('Hull Designators', 50)])
        for tname, tdesc, hulls in types:
            r += 1; _dr(r, tname, tdesc, hulls)

    # ── Vessel Class Reference ───────────────────────────────
    r += 2; subsec_band(ws, r, 'Vessel Class Reference', mc)
    r += 1; purpose_row(ws, r,
        'Reference only \u2014 not a column in the data sheet. Provides class-level context for hull designators.')

    _classes = [
        ('CVN', [
            ('Nimitz (CVN-68)', 'Nuclear-powered carrier, 10 ships (CVN-68 through CVN-77)', 'Active'),
            ('Gerald R. Ford (CVN-78)', 'Next-gen nuclear carrier: CVN-78, -79, -80, -81', 'Active / under construction'),
        ]),
        ('DDG', [
            ('Arleigh Burke (DDG-51)', 'Guided-missile destroyer \u2014 Flight I/II/IIA/III', 'Active / under construction'),
            ('Zumwalt (DDG-1000)', 'Multi-mission stealth destroyer, 3 ships', 'Active'),
        ]),
        ('CG', [
            ('Ticonderoga (CG-47)', 'Guided-missile cruiser (being decommissioned)', 'Active (retiring)'),
        ]),
        ('FFG', [
            ('Constellation (FFG-62)', 'Next-generation guided-missile frigate', 'Under construction'),
        ]),
        ('LCS', [
            ('Freedom (LCS-1)', 'Littoral combat ship \u2014 Freedom variant', 'Active'),
            ('Independence (LCS-2)', 'Littoral combat ship \u2014 Independence variant', 'Active'),
        ]),
        ('SSN / SSBN', [
            ('Los Angeles (SSN-688)', 'Nuclear attack submarine \u2014 largest SSN class', 'Active (retiring)'),
            ('Seawolf (SSN-21)', 'Nuclear attack submarine, 3 ships', 'Active'),
            ('Virginia (SSN-774)', 'Nuclear attack submarine \u2014 Block I through V', 'Active / under construction'),
            ('Ohio (SSBN-726 / SSGN-726)', 'Fleet ballistic missile sub (SSBN) and guided-missile sub (SSGN)', 'Active (retiring)'),
            ('Columbia (SSBN-826)', 'Next-gen ballistic missile submarine', 'Under construction'),
        ]),
        ('LHA / LHD / LPD / LSD', [
            ('America (LHA-6)', 'Amphibious assault ship', 'Active / under construction'),
            ('Wasp (LHD-1)', 'Multipurpose amphibious assault ship, 8 ships', 'Active'),
            ('San Antonio (LPD-17)', 'Amphibious transport dock \u2014 Flight I and II', 'Active / under construction'),
            ('Whidbey Island / Harpers Ferry (LSD-41/49)', 'Dock landing ships (replaced by LPD Flight II)', 'Active (retiring)'),
        ]),
        ('MCM', [
            ('Avenger (MCM-1)', 'Mine countermeasures ship', 'Active (retiring)'),
        ]),
        ('Oilers / Logistics', [
            ('Henry J. Kaiser (T-AO 187)', 'Fleet replenishment oiler (MSC)', 'Active'),
            ('John Lewis (T-AO 205)', 'Next-gen fleet replenishment oiler (MSC)', 'Under construction'),
            ('Lewis and Clark (T-AKE)', 'Dry cargo/ammunition ship (MSC)', 'Active'),
            ('Supply (T-AOE 6)', 'Fast combat support ship', 'Inactive'),
        ]),
        ('Expeditionary / Special', [
            ('Spearhead (T-EPF)', 'Expeditionary fast transport (MSC)', 'Active'),
            ('Lewis B. Puller (T-ESB)', 'Expeditionary sea base (MSC)', 'Active'),
            ('Medium Landing Ship (LSM)', 'New program \u2014 medium amphibious landing ship', 'Under development'),
            ('Ship to Shore Connector (SSC / LCAC 100)', 'Next-gen landing craft air cushion', 'Under construction'),
            ('LCU 1700', 'Landing craft utility \u2014 next generation', 'Under construction'),
        ]),
        ('Command / Support', [
            ('Blue Ridge (LCC-19/20)', 'Amphibious command ship', 'Active'),
            ('Emory S. Land (AS-39)', 'Submarine tender', 'Active'),
            ('Victorious (T-AGOS 19)', 'Ocean surveillance ship (MSC)', 'Active'),
            ('Pathfinder (T-AGS 60)', 'Oceanographic survey ship (MSC)', 'Active'),
            ('Mercy (T-AH 19)', 'Hospital ship (MSC)', 'Active'),
            ('Navajo (T-ATS)', 'Towing/salvage/rescue ship (MSC)', 'Under construction'),
            ('Safeguard (ARS-50)', 'Rescue and salvage ship', 'Active'),
        ]),
        ('USCG', [
            ('Legend (WMSL-750)', 'National Security Cutter', 'Active'),
            ('Heritage (WMSM-920)', 'Offshore Patrol Cutter', 'Under construction'),
            ('Sentinel (WPC-1101)', 'Fast Response Cutter', 'Active / under construction'),
            ('Famous (WMEC-270)', '270-foot medium endurance cutter', 'Active'),
            ('Reliance (WMEC-210)', '210-foot medium endurance cutter', 'Retiring'),
            ('Polar (WAGB-10)', 'Polar-class heavy icebreaker', 'Active (beyond service life)'),
            ('Polar Security Cutter (WAGB)', 'New heavy polar icebreaker program', 'Under construction'),
            ('Mackinaw (WLBB-30)', 'Great Lakes icebreaker', 'Active'),
            ('Juniper (WLB-201)', 'Seagoing buoy tender', 'Active'),
            ('Keeper (WLM-551)', 'Coastal buoy tender', 'Active'),
        ]),
    ]

    for hull_group, classes in _classes:
        r += 2; subsubsec_band(ws, r, hull_group, mc)
        r += 1; hdr_row(ws, r, [('Class', 35), ('Description', 70), ('Status', 50)])
        for cname, cdesc, status in classes:
            r += 1; _dr(r, cname, cdesc, status)

    # ── Vessel Column Standardization Rules ──────────────────
    r += 2; subsec_band(ws, r, 'Vessel Column Standardization Rules', mc)
    r += 1; purpose_row(ws, r,
        'Rules governing how Vessel Service, Category, Type, and Hull columns are populated')
    r += 1; hdr_row(ws, r, [('Rule', 35), ('Description', 70), ('Notes', 50)])
    for rule, desc, notes in [
        ('4-column vessel hierarchy',
         'Vessel data split into: Vessel_Service (USN/USCG/MSC), Vessel_Category, Vessel_Type, Vessel_Hull.',
         'Each column progressively more specific.'),
        ('Service determined by hull and source',
         'MSC when hull starts with T-. USCG for Cutters/Boats categories or USCG source book. All others USN.', None),
        ('Multi-type / multi-hull rows blanked',
         'If a line item applies to multiple vessel types or hulls, all 4 vessel columns are blank.',
         'Description or Citation preserves original scope.'),
        ('Vague values blanked',
         "Values like 'Multiple', 'Afloat (various)', 'N/A' that cannot map to a single canonical type are blanked.", None),
        ('Hull extracted from class or type',
         "Hull derived first from vessel class (Arleigh Burke \u2192 DDG). If no class but type was specific, hull extracted from type.", None),
        ('Type has no parentheticals',
         "Vessel_Type uses base name only (e.g., 'Surface Combatants'). Hull abbreviations belong in Vessel_Hull.", None),
        ('Blank stays blank',
         'If vessel info was originally blank, all 4 vessel columns remain blank.', None),
    ]:
        r += 1; _dr(r, rule, desc, notes)

    # ── Derived & Helper Columns ─────────────────────────────
    r += 2; subsec_band(ws, r, 'Derived & Helper Columns', mc)
    r += 1; purpose_row(ws, r,
        'Columns added by the build script for formula simplification and cost category analysis')

    r += 2; subsubsec_band(ws, r, 'Derived Columns (v4.0)', mc)
    r += 1; hdr_row(ws, r, [('Column', 35), ('Description', 70), ('Details', 50)])
    for col, desc, det in [
        ('Exhibit Level (col G)',
         'Populated for [ALT_VIEW] rows. Values: "P-5c", "P-8a", "P-35", or blank. '
         'Parsed from the Line Item Title.',
         'P-8a rows require a known cost category in the title. Blank for non-ALT_VIEW.'),
        ('Cost Category (col H)',
         'Populated for [ALT_VIEW] rows. One of 9 P-5c cost categories, or blank. '
         'For P-5c: extracted from title. For P-8a: parent P-5c category.',
         'Valid: Plan Costs, Basic Construction, Change Orders, Electronics, Propulsion Equipment, '
         'Hull Mechanical and Electrical, Ordnance, Other Cost, Technology Insertion.'),
    ]:
        r += 1; _dr(r, col, desc, det)

    r += 2; subsubsec_band(ws, r, 'Helper Columns (v5.14)', mc)
    r += 1; hdr_row(ws, r, [('Column', 35), ('Description', 70), ('Formula', 50)])
    for col, desc, formula in [
        ('Row Class (col AC)',
         'Classifies each row: "ADD" for additive (blank or [PARENT]), "ALT" for [ALT_VIEW], blank for others.',
         '=IF(OR(E="",E="[PARENT]"),"ADD",IF(E="[ALT_VIEW]","ALT",""))'),
        ('FY26 Best ($K) (col AD)',
         'Pre-computed FY2026 cascade. Picks first non-blank: DAA Enacted (Y), Total (U), Request (S).',
         '=IF(Y<>"",Y,IF(U<>"",U,S))'),
        ('FY27 Best ($K) (col AE)',
         'Pre-computed FY2027 cascade. Picks first non-blank: Total (AB), Request (Z).',
         '=IF(AB<>"",AB,Z)'),
    ]:
        r += 1; _dr(r, col, desc, formula)

    r += 2; subsubsec_band(ws, r, 'Formula Simplification Impact', mc)
    r += 1; _dr(r, 'Before v5.14',
        'Every SUMIFS encoded cascade inline \u2014 2 row types \u00d7 3 value columns = 6 SUMIFS per FY26 condition.',
        'Max formula: 6,013 chars / 84 SUMIFS')
    r += 1; _dr(r, 'After v5.14',
        'Each formula reduces to 1 SUMIFS: =SUMIFS(JB_26BV, ..., JB_RC, "ADD"). Helper columns are live formulas.',
        'Max formula: 853 chars / 14 SUMIFS (86% reduction)')

    # ── Named Ranges ─────────────────────────────────────────
    r += 2; subsec_band(ws, r, 'Named Ranges', mc)
    r += 1; purpose_row(ws, r,
        'Named ranges defined on J Book Items Cons. for use in SUMIFS formulas across all analysis sheets')
    r += 1; hdr_row(ws, r, [('Name', 35), ('Column & Description', 70), ('Range', 50)])
    for nm, coldesc, rng in [
        ('JB_A', 'col A \u2014 Source Book', '$A$6:$A$4000'),
        ('JB_B', 'col I \u2014 Bucket', '$I$6:$I$4000'),
        ('JB_V', 'col L \u2014 Vessel Category', '$L$6:$L$4000'),
        ('JB_W', 'col M \u2014 Vessel Type', '$M$6:$M$4000'),
        ('JB_H', 'col N \u2014 Vessel Hull', '$N$6:$N$4000'),
        ('JB_S', 'col E \u2014 Row Type', '$E$6:$E$4000'),
        ('JB_F', 'col J \u2014 Bucket Sub Category', '$J$6:$J$4000'),
        ('JB_EX', 'col G \u2014 Exhibit Level (derived)', '$G$6:$G$4000'),
        ('JB_CC', 'col H \u2014 Cost Category (derived)', '$H$6:$H$4000'),
        ('JB_CE', 'col AJ \u2014 Cost Element (system names for P-8a)', '$AJ$6:$AJ$4000'),
        ('JB_RC', 'col AC \u2014 Row Class (helper)', '$AC$6:$AC$4000'),
        ('JB_26BV', 'col AD \u2014 FY2026 Best Value (helper)', '$AD$6:$AD$4000'),
        ('JB_27BV', 'col AE \u2014 FY2027 Best Value (helper)', '$AE$6:$AE$4000'),
    ]:
        r += 1; _dr(r, nm, coldesc, rng)

    # ── Newbuild SAM Cost Category Detail ────────────────────
    r += 2; subsec_band(ws, r, 'Newbuild SAM Cost Category Detail', mc)
    r += 1; purpose_row(ws, r,
        'Supplemental cost category analysis on the Newbuild SAM sheet (FY26 only)')
    r += 1; hdr_row(ws, r, [('Section', 35), ('Description', 70), ('Notes', 50)])
    for sec, desc, notes in [
        ('SAM (D): P-5c Gross Cost Category',
         'Decomposes new-construction budget authority into P-5c cost categories by SAM vessel type. '
         'Gross total-ship-estimate costs \u2014 pre-AP/SFF, will NOT match SAM net totals.',
         'Uses SUMIFS on [ALT_VIEW] rows with JB_EX="P-5c". 6 SAM vessel types.'),
        ('SAM (E): Proportional Allocation',
         'P-5c percentage mix from (D) applied to SAM net budget-authority totals. '
         'Cost category decomposition reconciles to the SAM total.',
         'Allocated Total should equal SAM Net Total per vessel type.'),
        ('SAM (G): P-8a System Detail by Hull',
         'Individual GFE systems from Exhibit P-8a (radars, weapons, electronics, propulsion), '
         'grouped by cost category within each hull program. Laid out as a 4-across grid of per-hull tables.',
         'Bold category subtotal rows, italic system rows. Uses JB_EX="P-8a" with JB_CE per system.'),
    ]:
        r += 1; _dr(r, sec, desc, notes)
    r += 2; _nr(r,
        'FY2027 has no sections (D)/(E)/(G) \u2014 justification books (P-5c, P-8a, P-35) not yet released.')

    # ── FY2027 Methodology & Sourcing ────────────────────────
    r += 2; subsec_band(ws, r, 'FY2027 Methodology & Sourcing', mc)
    r += 1; purpose_row(ws, r,
        'How FY2027 columns were populated, sourcing, and methodological notes')
    r += 1; hdr_row(ws, r, [('Topic', 35), ('Description', 70), ('Notes', 50)])
    for topic, desc, notes in [
        ('Source document',
         'FY 2027 P-1 / O-1 (April 2026). New columns: FY2027 Request ($K), FY2027 Mandatory Request ($K), '
         'FY2027 Total ($K) at cols Z/AA/AB.',
         'Status: REQUEST only, not enacted.'),
        ('Discretionary vs Mandatory',
         'Two FY27 request columns: Discretionary Request (regular annual base) and Mandatory Request '
         '(a NEW reconciliation ask, separate from OBBBA, NOT enacted, NOT guaranteed).',
         'SCN FY27: Disc $60.18B + Mand $5.65B = $65.83B.'),
        ('TAM formula (FY27)',
         'Same as FY26 \u2014 sum (no tag) + [PARENT] rows. Uses FY2027 Total as per-row value.',
         'Same double-counting guards apply.'),
        ('Net vs Gross convention',
         'PARENT = NET (gross \u2212 Less:AP \u2212 Less:SFF). Same as FY26 DAA columns.',
         'Completion-PY rolldowns excluded from PARENT (live in [SUB] rows).'),
        ('OBBBA exclusion',
         'OBBBA (PL 119-21) is FY2026-only budget authority. 100% captured in FY2026 DAA columns. '
         'No FY27 OBBBA column \u2014 adding one would double-count.',
         'OBBBA contracts may sign in FY27/FY28 but BA is all FY26.'),
        ('Budget authority vs outlays',
         'This workbook measures BUDGET AUTHORITY (BA), not outlays. OBBBA gave $152.3B of FY2026 BA, '
         'available for obligation through Sept 30, 2029.',
         'Apples-to-apples basis for cross-year comparison.'),
        ('FY27 Mandatory vs OBBBA',
         'Different pots of money. OBBBA = enacted FY26 mandatory (PL 119-21, July 2025). '
         'FY27 Mandatory = a NEW ask in the Apr 2026 PB submission \u2014 NOT enacted.',
         'SCN FY27 Mand = $5.65B vs. SCN FY26 OBBBA = $17.93B.'),
        ('Coverage by source book',
         'High for SCN/OPN/WPN (line-item match). Blank for OMN/NWCF (SAG-level only) and USCG (DHS, not DoD).',
         'OMN/NWCF: Phase 2 prorated allocation. USCG: Phase 3 (DHS CJ).'),
        ('New programs (v1.21)',
         '9 new SCN rows for FY27 P-1 items not in v1.20: Surface Ship IB, BBG(X), FF(X), '
         'AS Sub Tender, SMS, Next Gen Logistics Ship, Bulk Fuel Vessel, T-AH(X), Fireboats.',
         'Each: Source=SCN, no Row Type tag (additive), full taxonomy where available.'),
        ('1613N Maritime Industrial Base Fund',
         'NOT added \u2014 FY26-only appropriation. Two line items (Sub IB $2.54B, Surface Ship IB $1.99B) '
         'are zero in FY27. OBBBA-only money already captured by other rows.', None),
    ]:
        r += 1; _dr(r, topic, desc, notes)

    # ── Data Quality Flags ───────────────────────────────────
    r += 2; subsec_band(ws, r, 'Data Quality Flags', mc)
    r += 1; purpose_row(ws, r,
        'Known duplicates, inconsistencies, and data quality issues in the current dataset')
    r += 1; hdr_row(ws, r, [('Issue', 35), ('Description', 70), ('Resolution', 50)])
    for issue, desc, resolution in [
        ('Surface Combatants variant (RESOLVED)',
         'Submarket column previously had hyphen and en-dash variants. As of v1.22, all standardized.',
         'Re-run consolidation if reloading from en-dash sources.'),
        ('OPN_BA3 / BA5-8 duplicate rows',
         '5 line items appear in both OPN_BA3 and OPN_BA5-8. Double-count when summed across all OPN_BAx.',
         'Est. impact: +$1.0M to +$1.3M. Pick canonical source, blank the other.'),
        ('LI 116 Advanced Arresting Gear (AAG)',
         'OPN_BA3 R2890 + OPN_BA5-8 R3208. Both reference same P-1 line item.',
         'Both FY27 = $23,551K. Pick one.'),
        ('LI 117 EMALS',
         'OPN_BA3 R2901 + OPN_BA5-8 R3209. Both reference same P-1 line item.',
         'Both FY27 = $36,908K. Pick one.'),
        ('LI 122 UMCS-UCA Mission Control Station',
         'OPN_BA3 R2947 + OPN_BA5-8 R3210. Both reference same P-1 line item.',
         'Both FY27 = $211,216K. Pick one.'),
        ('LI 176 Spares and Repair Parts',
         'OPN_BA3 R2973 + OPN_BA5-8 R3220. Both reference P-1 BA08 line 176.',
         'Both FY27 = $765,711K. Largest single-line double-count.'),
        ('LI 177 VIRGINIA Class Spares',
         'OPN_BA3 R2974 + OPN_BA5-8 R3221. In FY27, P-1 lacks a separate Virginia spares line \u2014 '
         'both rows blank in FY27.',
         'FY26: both have data. Consider prorating as share of consolidated BA08.'),
    ]:
        r += 1; _dr(r, issue, desc, resolution)

    # ── Phase 2 Plan ─────────────────────────────────────────
    r += 2; subsec_band(ws, r, 'Phase 2 \u2014 OMN/NWCF FY27 Allocation (Planned)', mc)
    r += 1; purpose_row(ws, r,
        'Planned methodology for populating FY27 values for OMN, OMN_Vol2, and NWCF source books')
    r += 1; hdr_row(ws, r, [('Topic', 35), ('Description', 70), ('Notes', 50)])
    for topic, desc, notes in [
        ('Why a separate sheet',
         'FY27 O-1/RF-1 only publish SAG-level totals \u2014 no per-line detail for OMN/NWCF. '
         'A "FY27 Allocation Workbench" will apportion SAG totals to individual rows.',
         'USCG is DHS, not DoD \u2014 cannot be filled from this exhibit set (Phase 3).'),
        ('Allocation rule',
         'Pro-rate by FY26 share: FY27_row = (FY26_row / FY26_SAG_total) \u00d7 FY27_SAG_total. '
         'Use FY26 DAA Enacted Total as baseline.',
         'Flag rows where prorated FY27 differs from FY26 by > \u00b125% for review.'),
        ('Source SAG totals (FY27)',
         'OMN SAGs: 1A5A Aircraft Depot Maint ($2,220M), 1B1B Mission & Ship Ops ($7,425M), '
         '1B2B Ship Ops Support ($1,713M), 1B4B Ship Depot Maint ($14,293M), 1B5B Depot Ops Support ($2,598M). '
         'NWCF: $266M.',
         'All FY27 Disc Request only \u2014 no Mandatory for OMN/NWCF.'),
        ('Workbench structure',
         'Columns: J Book row #, Source Book, LI, Title, SAG, FY26 DAA, FY26 SAG total, FY26 share %, '
         'FY27 SAG total, FY27 prorated, \u00b125% flag, manual override.',
         'Manual overrides take precedence when set.'),
        ('SAG \u2192 row mapping',
         'Parse SAG code from the Citation column (e.g., "OMN > BA01 > 1B4B Ship Depot Maintenance > ...").',
         'Ambiguous/missing citations require manual SAG assignment.'),
        ('Validation after Phase 2',
         'Sum of prorated FY27 values within a SAG should equal FY27 SAG total. '
         'Per-SAG summary: total, sum of prorated, variance.',
         'Only PARENT and (no tag) rows are additive for the SAG check.'),
        ('USCG handling (Phase 3)',
         '18 USCG rows cannot be populated from FY27 P-1/O-1 (CG is DHS). '
         'Requires FY27 DHS CG Congressional Justification.',
         'USCG FY27 columns remain blank until Phase 3.'),
    ]:
        r += 1; _dr(r, topic, desc, notes)

    finish_sheet(ws)
    print(f'  Built Validation sheet ({r} rows)')

