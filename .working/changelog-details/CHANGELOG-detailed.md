# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-07-22, Library Version 2026.07.548, PR #1060

RB-7 AI-security full-column integration (maintainer-decided full columns, not see-also): two newly-held AI-security frameworks, OWASP AI Exchange and SANS Critical AI Security Guidelines v1.4, engaged across five AI documents. Run through the high-assurance verification harness (research fan-out, then two independent adversarial verifiers, then a deterministic apply from an explicit verified map, then a re-parse).

### Changed
- **[`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md)** (1.8.10 to 1.8.11): the section-36 framework-alignment matrix gains two columns (OWASP AI Exchange, SANS CAISG v1.4), one cell per control-area row. Two cells are N/A per the adversarial verifiers: "Unsafe code generation" (both frameworks; the OWASP LLM Top 10 column already carries LLM05, and neither new framework has a generated-code-security control) and "Overreliance" SANS (SANS names no overreliance control; its Human Oversight is a decision-authority control).
- **[`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md)** (0.0.10 to 0.0.11): two framework rows (OWASP AI Exchange least model privilege; SANS Secure Agentic Systems and AI Autonomy Controls).
- **[`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md)** (1.1.3 to 1.1.4): two framework rows (OWASP AI Exchange umbrella taxonomy; SANS scope-precise categories, not the over-generic ISMS anchor the verifier rejected).
- **[`ai/guide-ai-security-technical-implementation.md`](../../ai/guide-ai-security-technical-implementation.md)** (1.3.4 to 1.3.5): an OWASP AI Exchange External-references bullet (the SANS bullet dropped as redundant per the false-positive verifier).
- **[`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md)** (1.0.8 to 1.0.9): two framework rows (SANS Incident Response and Forensics for AI Systems as the primary AI-IR anchor; OWASP AI Exchange Monitor use as a secondary).
- Taxonomy and maturity-scorecard regenerated for the Version bumps.

### Verification (high-assurance harness)
- Stage 1 research fan-out (`research-ha-aisec-mappings`, quoted every candidate at held source). Stage 3 two independent adversarial verifiers, blind to each other and to the research rationale: false-negative (`ha-aisec-verify-fn`, hunt misses) returned NO MATERIAL MISS with every N/A grounded (and caught a SANS "overreliance" homonym false-lead); false-positive (`ha-aisec-verify-fp`, hunt over-assignments) returned three OVER-ASSIGNED (all among the candidate's own flagged cells) plus one borderline, which drove the two N/A cells, the Table-3 anchor replacement, and the dropped Doc-4 SANS bullet. Stage 5 deterministic apply from the reconciled explicit map, then a re-parse cross-checking every applied cell against the map.
- The new columns use control NAMES (OWASP AI Exchange, SANS CAISG have no short codes), so the existence-gate families (CSA/NIST/ISO/COBIT) and the `/matrix-fit` worklist tool do not apply; the two adversarial verifiers performed the semantic-fit role instead.
- `run_all_audits.sh` 72/72 (lint-language OK); pre-push guard green; an offloaded pre-merge skeptical verify on the pushed SHA.
- Batches PR #1059's `/validate-pr` + `/retro` rows.

## 2026-07-22, Library Version 2026.07.547, PR #1059

RB-7 new-ingest reference-breadth (Canada cluster, findings C-1 and C-2): two newly-held Canadian government sources engaged as authoritative companion references. Offloaded research (`research-canada-breadth`) caught and corrected the original reference-audit's C-1 overstatement: the GC Guideline does NOT publish a Critical/High/Medium remediation-hours matrix (its timed table is scanning frequencies; remediation timing is qualitative), so the addition is grounded in the guideline's verified risk-based framing, not the "48h/14d/30d" figures the original finding claimed.

### Changed
- **[`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md)** (1.3.6 to 1.3.7): a companion-reference note in the Framework-alignment section citing the Government of Canada TBS Guideline on Vulnerability Management, grounded in its verified text (VM-program scope; "timelines for vulnerability remediation should be defined based on risk"; risk acceptance "must include an expiry date that is less than 12 months from when it is issued"), as a risk-based structural parallel, not a numeric SLA equivalence.
- **[`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md)** (1.4.6 to 1.4.7): a companion-reference note citing CCCS ITSP.50.103 as an injury-based security-categorization methodology ("applies to both private and public-sector organizations") bridging this standard's classification to cloud control-profile selection.
- Taxonomy and maturity-scorecard regenerated for the Version bumps.

### Verification
- Held-source re-verified via offloaded research (`research-canada-breadth`, which corrected C-1) and the offloaded pre-push skeptical verifier: the GC VM Guideline quotes at their cited lines and the ITSP.50.103 private-and-public applicability, injury-based categorization definition, and control-profile-selection basis.
- `run_all_audits.sh` 72/72; pre-push guard green.
- Batches PR #1058's `/validate-pr` + `/retro` rows per recursion-avoidance.

## 2026-07-22, Library Version 2026.07.546, PR #1058

Citation-accuracy fix from the RB-7 new-ingest reference-audit (Google SAIF existing-citation verification, OVERREACH verdict): two developer-security README reference entries described SAIF's coverage as including an "execution" lifecycle stage, which the now-held SAIF source does not support.

### Changed
- **[`dev-security/README.md`](../../dev-security/README.md)** (1.4.5 to 1.4.6): the Google SAIF reference line dropped "execution" from "secure development, deployment, execution, and monitoring".
- **[`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md)** (pack 1.62.3 to 1.62.4, a patch with no new rule or skill): the SAIF Coverage line dropped "execution"; a Version-history row records the patch.

### Verification
- Re-verified at the held source (the six Google SAIF full-text files in the reference base at ref `3e63317`): SAIF describes "six core elements" across a software-development lifecycle (development, deployment, monitoring); "execute" and "execution" appear only for agent actions and attacks (prompt injection, remote code execution), never as a SAIF lifecycle stage. The sibling reference line in the AI-coding-assistant guideline (which already read "development, deployment, and monitoring") was already accurate and is unchanged; the TikiTribe-coverage SAIF mentions are third-party-scoped and unchanged.
- Corpus-wide grep confirmed exactly two carriers of the overreach phrase, both fixed; no generated-artefact regen was needed (the README Version is not taxonomy-tracked); `run_all_audits.sh` 72/72; a refute-briefed skeptical verifier ran pre-push.

## 2026-07-22, Library Version 2026.07.545, PR #1057

Corpus accuracy fix from the RB-7 new-ingest reference-audit (finding L-1): the Brazil privacy annex stated the ANPD had not yet issued adequacy decisions, which the newly-held Resolution CD/ANPD No. 32 of 26 January 2026 (the ANPD's first adequacy decision, recognizing the European Union) disproves.

### Changed
- **[`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md)** (1.1.6 to 1.1.7): the Cross-border transfer-mechanisms Adequacy item replaced "As of 2025, the ANPD has not yet issued adequacy decisions" with the ANPD's first adequacy decision (Resolution CD/ANPD No. 32 of 26 January 2026, recognizing the EU: all EU Member States, the three EFTA states in the EEA, and EU institutions; subject to reassessment within four years); the standard-contractual-clauses paragraph reworded so SCCs remain primary for destinations not covered by an adequacy decision, with the new adequacy route as the alternative for the EU and EFTA/EEA.
- The taxonomy, portal, and maturity-scorecard artefacts were regenerated for the Version bump.

### Verification
- Re-verified at the held source (the Brazil ANPD Resolution No. 32 of 26 January 2026 full-text in the reference base at ref `3e63317`): Article 1 recognizes the EU as providing an adequate level of protection under the LGPD; the Sole Paragraph extends it to the EU Member States, the EFTA/EEA states (Iceland, Liechtenstein, Norway), and EU institutions; Paragraph 1 sets a four-year reassessment. The item is catalogued in the reference base.
- `run_all_audits.sh` 72/72 standalone; both generator `--check` runs in sync; the pre-push guard green; a refute-briefed skeptical verifier ran pre-push.

## 2026-07-22, Library Version 2026.07.544, PR #1056

Resume close-out for the 2026-07-22 session (the orchestrator's prior session ingested +31 reference items into `grc_library_ref`, catalogue 696 to 727; this session assesses corpus use/cite of them per TODO RB-7). This is the first PR of the resumed session: it runs the loop-break Sweep 116 corpus-wide `/validate`, clears the one aged-follow-up gate artefact, prunes the handoff, and re-acquires the lease.

### Changed
- **[`session-state.md`](../session-state.md)**: lease ACQUIRED for this session (`Status: active`, `Active-session: claude/resume-sweep116-closeout`, fresh heartbeat) after the `/resume` step-0 interlock confirmed the prior lease released and no live sibling session.
- **[`validate-sweeps/history.md`](../validate-sweeps/history.md)**: added the Sweep 116 row (Version 2.0.117); **re-triaged** the aged Sweep-3 follow-up at L133 (added `re-triaged: 2026-07-22` and an explicit `re-triage-by: 2026-08-21`; the default 30-day clock lapsed 2026-07-20 during the multi-day gap, failing gate 43 and the FollowupAgeing regression test), restoring the mechanical baseline to 72 of 72. Kept open as a future-gate candidate, not resolved.
- **[`session-handoff.md`](../session-handoff.md)**: advanced the Resume cursor to Sweep 116; pruned per keep-current-plus-one-prior (removed the 2-prior 2026-07-18b asserted-expectations block, whose substance is durable in the Sweep 113 history row and the CHANGELOG).
- **degradation-watch-log**: a `session-start` row appended in the private companion repo (the `/resume` step 0.4 evidence trail).

### Verification
- Loop-break Sweep 116 `/validate` (OFFLOADED to worker-20260716-b, blocking prio-0, pinned `501d77a2` / ref `3e63317`): **CLEAN PASS, 0 error / 0 warning / 0 note / 0 novel**. The #1054..#1055 delta is `.working`, `.claude`, CHANGELOG, README, and TODO only (no corpus-domain document); the CHANGELOG daily-tier condensation was verified faithful; all #1040-#1042 asserted-clean surfaces corroborated, 0 contradicted. Consumed under elevated QA (worker-b delivery 1 this session; the orchestrator's independent baseline re-derivation matched 70 of 72, same L133 root cause, restored to 72 of 72 by the re-triage).
- Post-commit `run_all_audits.sh` 72 of 72 standalone; the pre-push guard green at push. This PR's own `/validate-pr` and `/retro` batch into the next PR per recursion-avoidance.

## 2026-07-19, Library Version 2026.07.543, PR #1055

Condenses the 2026-07-19 root CHANGELOG entries (PRs #1039-#1054) into one daily summary and prunes the matching detailed-mirror entries, completing the daily-tier condensation for the day during the multi-day session gap. Also records TODO RB-7 (retrieve and ingest four not-held AI-security frameworks the aidefensematrix.com gap analysis surfaced, routed to maintainer-acquisition) and closes the 2026-07-19b/c session, releasing the concurrency lease.

### Changed
- **Root CHANGELOG**: the 16 per-PR 2026-07-19 entries (#1039-#1054) replaced by one `**2026-07-19 (PRs #1039-#1054)**` daily summary, per the §1.22.5 daily-tier model; #1055 (this PR) stays per-PR as the current entry.
- **Detailed mirror**: the matching #1039-#1054 structured entries pruned (git history preserves the full detail); gate 59's parity cutoff floors above them.
- **TODO RB-7**: records the aidefensematrix.com gap-analysis outcome (worker-offloaded, then orchestrator-`_ref`-index-verified with [`ref-holds.py`](../../tools/ref-holds.py)): four not-held AI-security frameworks (OWASP AI Exchange, SANS CAISG v1.4, Google SAIF, Cyber Defense Matrix) routed to maintainer-acquisition, then a corpus use/cite assessment; the matrix itself is NOT acquired (maintainer decision: a derivative CSF-2.0-by-asset-class mapping the project can re-create); OWASP Agentic Top 10 and NIST IR 8596 are HELD-but-uncited breadth items, not acquisitions.
- **The private maintainer-egress-requests queue** (v1.0.3): the four not-held frameworks added as a maintainer-acquisition block (drop-destination `grc_library_ref/ingest/`) for the Wednesday 2026-07-22 resume.
- **Session close**: [`session-state.md`](../session-state.md) lease RELEASED (`Status: released`, `Active-session: none`); [`session-handoff.md`](../session-handoff.md) and [`next-prs.txt`](../next-prs.txt) refreshed with the continuation note and the RB-7 ingest step; the [`validate-pr/history.md`](../validate-pr/history.md) row records the handoff-PR exemption.

### Verification
- Gate 59 (mirror-header-parity) re-run clean after the prune; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green at push. **Session-closing PR:** per the loop-break rule this PR skips its own trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume` corpus-wide `/validate`, and this session additionally ran Sweep 115 pre-close (0 error / 0 warning over #1044..#1053). The concurrency lease is RELEASED here.

