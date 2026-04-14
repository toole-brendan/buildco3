# BuildCo3 Tasks

## Group 1: Research & Investigation (do first)

Answers from these inform implementation decisions downstream.

| # | Task | Feeds into |
|---|------|-----------|
| R1 | **Do OMN sub-component names exist in the data sheet?** Check if rows attributed to OMN sub-components under the 1BRB `[PARENT]` program already have a column for this, or if one needs to be added. Check Section F titles too. | Section E/F fix (S2) |
| R2 | **Can other big OMN program lines be broken down** like 1BRB is in FY26 MRO SAM? | MRO SAM expansion (S3) |
| R3 | **Can the Modernization bucket be broken down further?** It's currently very large in the final Mekko. | MRO SAM expansion (S3) |
| R4 | **Why is "UUV" used instead of broader "unmanned"?** Is USV feeding any funding into sheets that say "Less UUV"? Or are we being specific because other unmanned types contributed $0 anyway? | Possible taxonomy fix (S4) |
| R5 | **Are all qualifying vessels accounted for in each TAM/SAM sheet?** No accidental drop-offs? Are inclusion/exclusion rules clear and being followed? | Validation / correctness |
| R6 | **Are the data quality issues in the Validation sheet still valid?** Is RCOH/SLEP listed in multiple bucket definitions (New Construction AND Major Life-Cycle)? Is there a GFE sub-category in the data sheet? | Data quality fixes (S5) |
| R7 | **How granular can we get on government-only vs. outsourceable work?** Can GFE items only be done by government? | MRO SAM purpose row (D2) |

Precedence within this group: R1 first (directly unblocks the most concrete implementation task). R5 and R6 next (foundational correctness). R4, R2, R3, R7 can be explored in parallel.

---

## Group 2: Structural / Data-Driven Changes (do second)

These change how sheets are built and what data they pull. Order matters.

| # | Task | Depends on |
|---|------|-----------|
| S1 | **Restructure Sections B/C/D/E on FY26 Newbuild TAM.** B = all vessel types for in-scope categories (with $0s shown). C = all hull programs for in-scope categories (with $0s shown). D = drop zero-funded vessel types. E = drop zero-funded hull programs, restructured so hull programs nest under vessel type header rows (like Section G on Newbuild SAM). | R5 (to confirm scope rules) |
| S2 | **Replace hardcoded values in Section E of FY26 MRO SAM** with SUMIF formulas from data sheet. Source OMN sub-component names properly. Possibly add a column to data sheet. Also fix Section F titles. | R1 (need to know where names live) |
| S3 | **Expand MRO SAM breakdowns** - other OMN programs beyond 1BRB, and Modernization bucket granularity. | R2, R3 |
| S4 | **Remove "Less: No vessel type" lines from Bridge sections** in TAM/SAM sheets. Fold into "Less: Unattributed" and add "vessel category" to that label. | Standalone, but do after R5 confirms scope |
| S5 | **Fix data quality issues** from Validation sheet. | R6 |
| S6 | **New sheet: Work type by $ by book source** (FY26 only). Executive summary format. | Standalone |

Precedence: S2 first (most concrete, unblocked once R1 is answered). S1 next (significant structural rework). S4 is quick once R5 confirms correctness. S3 and S5 depend on their research. S6 is independent.

---

## Group 3: Documentation & Style (do last - can be de-prioritized)

| # | Task | Notes |
|---|------|-------|
| D1 | **Replace em/en dashes with hyphens** throughout. Add preference note in build script and CLAUDE.md. | Pure find-and-replace + comment |
| D2 | **Add bucket 6+7 removal explanation** to MRO SAM row 2 purpose text and Validation sheet. | Partially depends on R7 for the GFE nuance |
| D3 | **Fix note annotations:** remove underscores from text, fix spurious newlines in note bubbles, improve bubble auto-sizing logic (text content determines dimensions, not the other way around). | Self-contained, but the bubble sizing may be intertwined with the newline bug (fixing newlines might fix sizing), so tackle newlines first |

---

## Suggested Execution Order

1. **R1** then **S2** - unblock the most concrete fix
2. **R5 + R6** - foundational correctness audit, informs almost everything
3. **S1** - big structural rework, self-contained once scope is confirmed
4. **R4** then **S4** - quick research then quick fix
5. **S5** - fix validated data quality issues
6. **R2 + R3** then **S3** - MRO SAM expansions, more open-ended
7. **S6** - new summary sheet, independent
8. **D1, D2, D3** - style/docs, lowest priority
9. **R7** - most open-ended research question, informs D2 nuance
