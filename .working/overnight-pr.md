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
- FR-167 batch 7 (compliance, 25 net-new rows, section 5 to 30): shipped in PR #383 (merged); `/validate-pr` 1 cosmetic note (row-93 Type word), `/retro` done.
- FR-167 batch 8 (governance, 15 net-new rows, section 4 to 19; the governance domain's many library-infrastructure/meta docs excluded per the coverage summary after a scoping pass): authored; gates 48/49 + full audit 54/54 green; shipped in PR #384. The #383 row-93 note fix bundled in.
- Next: FR-167 batch 9 (security, 34 docs).

## Batch-8 judgment calls (for the maintainer's morning, proceeded with stricter-safe defaults; confirm or redirect)

- **Trade columns N/A across all 15 governance rows.** Three of them (`framework-continuous-assurance-and-improvement`, `framework-metrics-monitoring-and-performance-reporting`, `register-data-retention-schedule`) carry incidental in-body BASC/WCO/AEO content (a section or alignment-table row), and precedent exists (the matrix charter row and the records-retention row carry trade columns). I held to N/A (stricter-safe: the docs' subject is enterprise governance, not trade security, and populating BASC would have required a chapter number the bodies do not cite, which would be fabrication). The maintainer may want these three populated with WCO "Pillar II (Customs-to-Business)" plus grounded requirement-area phrases.
- **`framework-document-architecture-and-interrelationship` INCLUDED (borderline).** Its Purpose line 21 ("how documents in the GRC Documentation Library relate") reads as library-infrastructure/meta, but line 24 ("a reusable architecture for organisations that need a coherent policy corpus") is adopter-facing; included on the line-24 reading. The maintainer may want it excluded as meta.

## Open ambiguities (for the maintainer's morning)

- None blocking. Confirm or redirect the batch-7 and batch-8 trade-column / scope judgment calls above on resume; everything else followed the durable handoff queue and the standing disciplines.
