# /claim-fit run: ISO/IEC 20000-1:2018 clause-attribution accuracy (2026-07-14)

## Trigger

TODO §3.72, routed from the #910 ISO 20000 reference-breadth research, which incidentally found mis-attributed ISO/IEC 20000-1 clause citations in the operations ITSM cluster. Full-cluster pass (not the worker's 2-of-9 spot-check) over all 9 corpus docs citing 20000-1, judged against the held source TOC. Research worker + orchestrator re-verification against the held clause structure this turn.

## Held source (verified this turn)

`grc_library_ref/standards/ISO/ISO-IEC-20000-1-2018--Service-management-system-requirements--full-text.md`. Confirmed clause-8 subclause titles verbatim from the body headings: §8.3 Relationship and agreement; **§8.3.3 Service level management**; §8.4 Supply and demand; **§8.4.1 Budgeting and accounting for services**; **§8.4.3 Capacity management**; §8.5 Service design, build and transition; **§8.5.3 Release and deployment management**; **§8.6 Resolution and fulfilment** (NOT "Service management"); **§9.1 Monitoring, measurement, analysis and evaluation**. IMPORTANT: no clause at any level is titled "Service management" (the label in several corpus rows is fabricated).

## Verdicts (11 citation instances across 9 docs)

- **correct (2):** `framework-it-service-management.md:92` (document-level, matches the doc title); `register-it-operations-kpis.md:21` (prose, document-level).
- **mis-attributed, FIXED #911 (4):**
  - `standard-service-level-management.md:210` §8.3 -> **§8.3.3 Service level management** (§8.3 is "Relationship and agreement").
  - `standard-service-level-management.md:21` (prose) §8.3 -> **§8.3.3**.
  - `standard-capacity-and-performance-management.md:213` "§8.6 Service management" -> **§8.4.3 Capacity management** (doubly wrong: §8.6 is "Resolution and fulfilment").
  - `standard-observability-and-telemetry.md:240` "§8.6 Service management" -> **§9.1 Monitoring, measurement, analysis and evaluation** (closest defensible home; §8.6 wrong, observability has no dedicated clause).
- **imprecise document-level, made precise FIXED #911 (2):**
  - `procedure-release-management.md:214` "Service management requirements" -> **§8.5.3 Release and deployment management**.
  - `standard-it-financial-management.md:226` "Service financial management" -> **§8.4.1 Budgeting and accounting for services**.
- **no-clean-home, LEFT as document-level (1):** `standard-site-reliability-engineering.md:218` ("Service management requirements"): SRE is not a named 20000-1 clause; acceptable as document-level, no wrong §number, so left unchanged (adding a spurious clause would be worse).
- **MISSED-then-FIXED (caught by the pre-push skeptical verifier):** `procedure-change-management-and-configuration-control.md` DID cite 20000-1: four Framework-alignment cells cite `§8.5` under a column headed bare "ISO/IEC 20000" (no `-1`). The initial file-discovery `grep 20000-1` MISSED the carrier because the header omits the part number (a pattern-width miss in file discovery, not just in the citation). The verifier caught it, and it is FIXED in-window: Configuration management `§8.5` -> **§8.2.6 Configuration management** (wrong-clause: config mgmt is §8.2.6, NOT under §8.5 "Service design, build and transition"); Change management / Emergency change / CAB governance `§8.5` -> **§8.5.1 Change management** (precise home); column header "ISO/IEC 20000" -> "ISO/IEC 20000-1" (doc 1.3.2 -> 1.3.3). All 9 in-scope operations docs are now genuinely judged.
- **ALSO caught by the re-verify (a carrier outside the 9-doc operations scope):** [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md):273, the doc-index register's Service Level Management Standard row, cited `ISO/IEC 20000-1:2018 §8.3` (coarse, a paired-surface mirror of the SLM doc's citation this pass tightened) -> **§8.3.3** (register 1.27.84 -> 1.27.85). Its sibling row :274 (KPIs register -> §9.1 Monitoring, measurement, analysis and evaluation) is CORRECT and left unchanged. A whole-corpus grep for `ISO/IEC 20000-1 ... §` now shows every clause-carrying 20000-1 citation consistent with the held TOC.

## Net

11 clause-citation corrections across 7 docs (6 operations docs + the governance doc-index register; plus the change-management column-header precision fix "ISO/IEC 20000" -> "ISO/IEC 20000-1"); each touched doc Version+Date co-bumped; taxonomy/scorecard regenerated. The fabricated "§8.6 Service management" label (2 docs) and the two wrong-clause citations (observability §8.6; change-mgmt Configuration management §8.5 -> §8.2.6) are the highest-severity, all corrected against the held source. Every clause number+title written was quoted from the held full-text this turn (orchestrator re-verified the worker's TOC extraction). ROOT-CAUSE LESSON: the file-discovery grep for a clause-accuracy pass must use the BARE standard token ("ISO/IEC 20000"), not the part-qualified form ("20000-1"), because a doc may cite the standard's clauses under a column/label that omits the part number; the part-qualified grep silently drops such a carrier (the change-mgmt miss, verifier-caught).
