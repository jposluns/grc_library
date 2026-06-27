# Overnight PR

**Status:** in-flight

A maintainer-authorized autonomous overnight session is in flight (started 2026-06-27 UTC; the maintainer said "I am going to sleep soon. Start overnight mode."). This file is the durable handoff record for the run; the next-morning processing PR routes its content to the durable ledgers and resets the file to `stub`. Audit gate 46 enforces the lifecycle (passes on `stub` / `in-flight`, fails on `done`).

## Authorization scope

- **Mode**: overnight (maintainer asleep / unreachable). Green CI = merge authority; stricter-is-safer-always on cross-value conflicts; genuinely-authorial, irreversible, or outward-facing decisions are deferred to [`pending-decisions.md`](pending-decisions.md) for the morning and routed around, never guessed.
- **Track**: the durable handoff queue, the FR-167 compliance-alignment matrix batches, smallest-first. Batch 7 (compliance) shipped in the opening PR; then governance (31), security (34), ai (34), privacy (42), then the partial sections. One PR per batch, each with the full per-PR `/validate-pr` + `/retro`, CI-gated, green CI = merge.
- **Reference inputs**: the maintainer re-attached CCM v4.1 / AICM v1.1 / NIST CSWP.29 (belt-and-suspenders; the in-repo reference modules `tools/ccm_aicm_reference.py` and `tools/nist_csf_reference.py` are the authoritative validators gates 48/49 use, so batch authoring is gate-protected without the binaries).

## Design decisions made this session

- The mandatory **Sweep 58** loop-break `/validate` ran first (the #382 handoff compensating control over the #380/#381/#382 deltas): full A/B/C dispatch, 0 findings, clean, no asserted-expectations contradiction.
- **Batch-7 trade-column authoring rule** (the one authorial call, resolved by stricter-safe default): a trade-column cell (CTPAT/PIP/BASC/WCO/AEO-S) is populated only where the source document's own framework-alignment table or body grounds the mapping; otherwise N/A. BASC cells use a cited chapter or N/A, never a fabricated clause. Apply-time corrections: the CTPAT full-MSC register personnel-screening ISO code was corrected from A.7.2 (physical entry) to A.6.1 (screening); inferred ISO/CSF cells on the four trade registers (no in-document ISO/CSF column) were trimmed to the strongest control-subject-grounded codes.

## Build progress

- Sweep 58: complete, clean (history row batched into the batch-7 PR #383).
- FR-167 batch 7 (compliance, 25 net-new rows, section 5 to 30): shipped #383 (merged); `/validate-pr` 1 cosmetic note (row-93 Type word, fixed in #384), `/retro` done.
- FR-167 batch 8 (governance, 15 net-new rows, section 4 to 19; library-infrastructure/meta docs excluded per the coverage summary after a scoping pass): shipped #384 (merged); `/validate-pr` 0 findings, `/retro` done.
- FR-167 batch 9 (security, 25 net-new rows, section 10 to 35): shipped #385 (merged); `/validate-pr` 0 findings, `/retro` done. Trade columns populated by grounded analogy to the Security-section convention (see learnings below); six source-doc framework-table code mislabels corrected in the matrix and flagged as a TODO follow-up.
- Session-closing handoff PR #386 lands this session's close-out (the #385 `/validate-pr`+`/retro` rows, session-metrics row, this overnight-pr update, the session-handoff refresh); it skips its own trailing `/validate-pr`+`/retro` per the loop-break.
- **Directive-tasks interlude (2026-06-27 resume from #386, this session):** the fresh session resumed the run but the maintainer had queued three pre-resume directive tasks that ran FIRST (not FR-167): #387 (scratch `ref/standards` durability + `/resume` reference-loading + persist-to-`main` codification; the CSA/NIST reference extracts seeded on scratch `main` via MCP PR #1) and #388 (orchestrator-token TODO section 4.19 + the feasibility investigation), preceded by the mandatory clean Sweep 59. Session-closing handoff PR #389 lands this interlude's close-out. FR-167 batch 10 was NOT started; it remains the next overnight item.
- **Next: FR-167 batch 10 (ai, ~34 docs)**, then batch 11 (privacy, ~42), then the matrix's partial sections. The overnight run CONTINUES in the next session; this file stays `in-flight`. Carry the batch-9 learnings below (trade-column convention varies by section: read the ai/privacy existing rows first).

## Batch-9 learnings (carry into batch 10+)

- **The trade-column convention VARIES by matrix section.** Governance docs (batch 8) are N/A across the 5 customs/trade columns; Security docs (batch 9) POPULATE them via the ICT-security / AEO-S requirement-area lens (all 10 pre-existing Security rows do). Before authoring a domain's trade columns, READ that domain's existing matrix rows and follow their convention rather than defaulting N/A. For ai and privacy: check the existing ai/privacy rows; likely mostly N/A (not customs domains) but verify.
- **Source docs mis-cite their own control codes.** Batches 7-9 surfaced ~7 docs whose framework-alignment tables carry wrong CCM/ISO codes (SEF-01-as-ethics, HRS-09-for-remote-working, AIS-01-as-acceptance, DSP-04-as-DLP, HRS-06/07-for-training, A.6.2-for-teleworking). The matrix carries corrected codes; a follow-up TODO item tracks fixing the source docs. Workers must validate the doc's OWN self-cited codes against the reference modules, never propagate.

## Batch-8 judgment calls (for the maintainer's morning, proceeded with stricter-safe defaults; confirm or redirect)

- **Trade columns N/A across all 15 governance rows.** Three of them (`framework-continuous-assurance-and-improvement`, `framework-metrics-monitoring-and-performance-reporting`, `register-data-retention-schedule`) carry incidental in-body BASC/WCO/AEO content (a section or alignment-table row), and precedent exists (the matrix charter row and the records-retention row carry trade columns). I held to N/A (stricter-safe: the docs' subject is enterprise governance, not trade security, and populating BASC would have required a chapter number the bodies do not cite, which would be fabrication). The maintainer may want these three populated with WCO "Pillar II (Customs-to-Business)" plus grounded requirement-area phrases.
- **`framework-document-architecture-and-interrelationship` INCLUDED (borderline).** Its Purpose line 21 ("how documents in the GRC Documentation Library relate") reads as library-infrastructure/meta, but line 24 ("a reusable architecture for organisations that need a coherent policy corpus") is adopter-facing; included on the line-24 reading. The maintainer may want it excluded as meta.

## Open ambiguities (for the maintainer's morning)

- None blocking. Confirm or redirect the batch-7 and batch-8 trade-column / scope judgment calls above on resume; everything else followed the durable handoff queue and the standing disciplines.
