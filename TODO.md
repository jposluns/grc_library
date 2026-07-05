# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for the queued-PR-already-merged drift shape (its companion sweep-cursor-behind-history check reads the resume cursor from [`.working/session-handoff.md`](.working/session-handoff.md)). The intra-document section-reference gate also scans it. Other audit gates skip this file.

**How items are numbered and formatted.** Items are grouped by priority (P1-P7), tiered by work type (maintainer's 2026-06-30 leaning): P1 fix errors and prevent recurrence, P2 fill significant gaps, P3 clean up and tooling, P4 adopter experience, P5-P6 expand the corpus (overlays, then new domains), P7 awaiting decision. **Every item is a `### N.M` subsection whose leading digit is its priority** (so a P3 item is `3.x`); within a section items run lowest-effort-first. The `N.M` number is a position, not a permanent id, so it changes if an item is re-tiered or resequenced; the **stable id is the `FR-N` / descriptive identifier in the heading**, and a `(was X.Y)` tag preserves the prior number for one cycle so older references (CHANGELOG, handoff, retro log, tool docstrings) stay resolvable. Each heading carries `(id, severity, effort)` where severity is `H[critical]` / `H` / `M` / `L` / `FYI` and effort is `XS` / `S` / `M` / `L` / `XL` (scale in 3.4). A `⚠` marks a persona-quoted finding to verify at action time.

---

## Queueing rules

- Orchestrator picks the next batch from **Priority 1 first, then Priority 2**, in highest-severity order; within a chosen section the effort ordering helps assemble like-effort batches.
- **1-8 PRs per batch** (logical grouping); `/validate` after each batch.
- Maintainer direction supersedes the orchestrator's pick at any time.
- Lower priorities (P3-P7) are picked deliberately, not from the routine batch queue, unless the maintainer triggers them.
- **Maintainer-directed running order (2026-06-30 work-type re-tier)**: work the tiers in order. **P1** first (the cheap fix/prevent items: the §1.5 integrity tooling; the former audit-gate-candidates section is COMPLETE, S3's `/claim-fit` skill shipping as the last of them, 2026-07-04; FR-48 is COMPLETE, 2026-07-03, #596 through #607); then **P2** gaps (FR-59 and FR-60 deepenings and the deepen-baselines cluster first, then **FR-70**, the XL crypto-asset domain, last); then **P3** clean-up-and-tooling; then **P4** adopter experience. **P5 / P6 expansion waits** (maintainer: expansion can wait). The standing **fix-issues-first** directive (2026-06-27) governs within each tier, and the routine `/validate`, `/validate-pr`, `/matrix-fit`, and `/claim-fit` cadences are the reactive half of P1. FR-167, the NIST SP 800 ingestion, and the OT post-ingestion validation are COMPLETE (2026-06-30; ingestion in `grc_library_scratch`, validation in #495).
- **Integrity-tooling items** (the former "guard-rails phase"): the reference version-currency residuals (§1.5) live in **P1** (fix errors and prevent recurrence; the sibling S3 citation-precision instrument is COMPLETE, the `/claim-fit` skill and Tier-A pass shipped 2026-07-04, closing the former audit-gate-candidates section); the QA-cadence and TODO/DONE-rotation surfaces are already covered by the bookkeeping-parity gate family (gates 50 and 57, plus the D5 PR-time check), and the retro guard rails (the former retro-log consolidation item) closed across #510 (the new-skill-drafting checklist) and #511 (the word-form count gate). Research fan-out (workers produce verified research from [`.working/worker-brief-template.md`](.working/worker-brief-template.md); the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing. The routine `/validate`, `/validate-pr`, `/matrix-fit`, and `/claim-fit` cadences are the reactive half of this tier; the items below are the standing preventive half.

### 1.5 Reference version-currency residuals (from the register version-currency build, #505) (S each)

The §1.5 reference version-currency register **shipped in #505** (the `Upstream check location` + `Last verified (UTC)` columns across all 16 register tables, the advisory staleness cadence in [`specification-citation-verification.md`](governance/specification-citation-verification.md) §12.3, the scratch-is-storage / upstream-is-authority principle, the §7 publisher allow-list extension, and 7 upstream-confirmed register corrections), and **all three citation version-upgrade follow-ups have now shipped** (ISO/IEC 27033 -> 27033-1:2015 #506; ISO/IEC 27036-2 2014 -> 2022 #507; NIST SP 800-88 Rev. 2 re-point + IEEE 2883 introduction #508). Remaining residuals:

- The **51 `needs-reconfirm` rows** (iso.org, the IEC webstore, and several government sources block automated fetch) await a browser or different-egress reconfirm pass to fill their `Upstream check location` URLs and stamp a verified date. **Maintainer 2026-07-02: DEFERRED until the new process (the maintainer's egress instance) is ready** (reaffirmed 2026-07-03), alongside the FR-70 and ISO-31000 deferrals; the FR-48 renumber series completed in #596 through #607.

### 1.9 RM-10 pipe-guardrail hardening (maintainer-directed 2026-07-03) (M, S total)

The maintainer observed that pipe-masked verification output (`guard | tail`, truncated gate
runs) is the session's most recurrent mechanical error class (seven RM-10 incidents: #569,
#583, #608, a fourth self-caught before the #615 push, a fifth display-only pipe
self-caught before the post-#618 branch push, a sixth post-commit audit run piped
to `tail` with a pipe-masked exit capture, self-caught in the slice-3 build, and a
seventh post-amend audit run piped to `tail`, self-caught and re-run unpiped in the #628
build; the PreToolUse hook did NOT block the seventh, hard evidence for both the (a)/(b)
hook-firing residual below and the (d) self-test wiring) and
accepted the assessed
guardrail set. Parts (a) and (b) shipped together as one small tooling PR (2026-07-03);
part (c), the authorized CLAUDE.md widening with its staged-clause bundle plus the hook
named-command/sink widening (run-linter-regression, generator --check invocations, tee/wc),
shipped in the #629 touch, and part (d), the self-test wiring (both enforcers'
`--self-test` runs as regression tests, so a broken enforcer fails the suite), shipped
2026-07-04, so the section stays open ONLY on the next-session hook-firing validation
noted below.

- **(a) and (b) SHIPPED 2026-07-03** (the hook [`.claude/hooks/block-verification-pipes.py`](.claude/hooks/block-verification-pipes.py) wired in [`.claude/settings.json`](.claude/settings.json), the wrapper [`tools/tail-safe.sh`](tools/tail-safe.sh) with inline self-test, and the guard pipe self-defence in [`tools/pre-push-guard.sh`](tools/pre-push-guard.sh) with the documented `PRE_PUSH_GUARD_ALLOW_PIPE=1` override; the tty check shipped as a `[ -p /dev/stdout ]` PIPE check because in this execution environment a plain invocation's stdout is a harness capture FILE, so the spec's literal tty test would refuse every sanctioned run while the pipe test refuses exactly the masking shape). **One residual validation (RAN 2026-07-05, resumed session): the hook does NOT fire here.** Hooks load at session start, so the shipping session validated only the script-level block/allow/malformed cases directly. The 2026-07-05 resumed session ran the deliberate test (a generator `--check` piped to `tail`; and separately `run_all_audits.sh 2>&1 | tail`): both ran UNBLOCKED, the PreToolUse hook did not fire, confirming the worker-restarted-session hook-firing limitation flagged above. The hook is wired in `settings.json` and its script self-tests pass, so this is not a corpus/config defect: the harness is not invoking the PreToolUse hook in this session type. In such sessions the hook gives no defence-in-depth, and the RM-10 unpiped-verification discipline (run standalone, read `${PIPESTATUS[0]}` / exit) is the sole active protection. Disposition (maintainer, low-stakes, surfaced 2026-07-05): accept as a known environment limitation and close 1.9, or pursue a harness-level fix; the RM-10 habit and the guard's own `PRE_PUSH_GUARD_ALLOW_PIPE`-gated pipe self-defence already cover the underlying risk.

### 1.11 Brazil ANPD-restructuring and breach-rule citation verification (maintainer-directed 2026-07-05) (S)

Four Brazilian statutory and regulatory designations in the corpus are 2024-to-2026-dated instruments this session could not confirm against a primary source (Sweep-84 finding A-F1). Newly-dated legal citations are exactly the fabrication-risk class the accuracy rules flag, so until confirmed they are annotated as pending primary-source verification in the corpus (the Sweep-84 Brazil annotation, queued as a corpus PR). This item tracks the verification itself, so the annotation is not left standing indefinitely. It is egress-gated like the §1.5 needs-reconfirm rows: the Planalto and ANPD primary sources need the maintainer's egress instance or a browser pass. Verify each against its primary source, then in the same PR remove the pending-verification annotation (or correct the designation if the primary source differs):

- **Lei No. 15.352/2026**: the law said to have restructured the ANPD into a regulatory agency, in [`privacy/jurisdictions/annex-privacy-brazil.md`](privacy/jurisdictions/annex-privacy-brazil.md) line 29.
- **Medida Provisória No. 1.317/2025**: the provisional measure said to have been converted by Lei 15.352/2026 and to have amended LGPD Articles 5 and 55-A (same line).
- **LGPD Article 55-A**: the article the provisional measure is said to have added (same line).
- **Resolution CD/ANPD No. 15/2024**: the Security Incident Communication Regulation carrying the 3-business-day breach-notification rule, cited in the annex (line 43) and in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) (lines 177 and 321).

While verifying, also confirm the two adjacent ANPD-resolution citations in the same annex (Resolution CD/ANPD No. 19/2023, the standard contractual clauses; Resolution CD/ANPD No. 2, the small-agents regulation), which are the same citation class. Provenance: Sweep-84 A-F1, routed to [`pending-decisions.md`](.working/pending-decisions.md) and resolved 2026-07-05 to annotate-now, plus the maintainer's 2026-07-05 direction to open a durable TODO item so the lookup is not forgotten.

## Priority 2 — Fill significant gaps

Deepening thin-but-present content to operational sufficiency, and the significant missing capabilities. The deepen-baselines cluster (FR-15 / 23 / 63 / 74 / 99 / 154 / 41) was decided for operational deepening (maintainer 2026-06-25).

### 2.1 Privacy jurisdiction annex operational deepening (FR-59, H, L)

Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the 25 country annexes to operational level. **Reference-base aid (2026-06-27 scratch-review S-7)**: `grc_library_scratch/ref/legislation/` now holds primary-source full-text for Japan APPI, Virginia VCDPA, Colorado Privacy Act, and the LATAM laws (Mexico, Brazil, Argentina, Colombia, Uruguay); author the deepening against those held sources. Honest caveat: APAC beyond Japan (Singapore, Australia, Korea, China, India) remains maintainer-drop (absent from the ref base). **Progress (2026-07-04, held-source batch PR 1)**: the Japan, United States, Canada, and Brazil annexes are deepened to operational level from the held texts (upstream-confirmed current at apply time). Remaining: the Latin America annex correction-plus-deepening with the paired index update and the standalone Mexico annex (batch PR 2, delivery in hand), then the 18 source-gated annexes, which wait on maintainer source drops (gap analysis delivered at `inbox/worker-20260703-a/fr-59-privacy-jurisdiction/research-source-gated-gaps.md`). Out of this item's remaining set by design: the EU annex (fr-74-owned) and the UK annex (already operationally deep; further held-source pinning available-for-later per the delivery manifest).

### 2.2 HIPAA operational deepening (FR-60, H, L)

HIPAA adopter has no operational detail beyond a single 261-line sector annex in `compliance/healthcare`. Deepen.

### 2.3 Crypto-asset / blockchain governance domain (FR-70, H[critical], XL)

New domain for crypto-asset / blockchain governance — digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense. (Cross-references P6.x for domain-level shaping.)

### 2.4 Per-control effectiveness metrics (FR-99, M, M) ⚠

Per-control effectiveness metrics (continuous assurance / 3LoD).

### 2.5 Maturity-ladder methodology (FR-15, M, M)

Maturity-ladder methodology — median-of-medians scoring concern. **Shape decided (maintainer, 2026-07-03): a methodology standard documenting the ladder, the aggregation, and its outlier-masking limitation (with a compensating floor-check narrative); the generator's scoring is unchanged.**

### 2.6 Audit-evidence assembler-verification standard (FR-23, M, M) ⚠

Audit-evidence assembler-verification standard absent.

### 2.7 Worked example: adoption, not ingestion (FR-63, M, M)

Worked example walks ingestion not adoption.

### 2.8 Schrems II operational deepening (FR-74, M, M)

Schrems II-light treatment. **Update 2026-06-30: the TIA instrument shipped in #483 (FR-34), which delivers the six-step transfer-impact assessment; FR-74's residual is the Schrems II operational deepening of the EU jurisdiction annex and the cross-border procedure (per the FR-154 "deepen to operational depth" decision). The TIA cross-reference wiring shipped in #489.** Consolidates with FR-34 (Transfer Impact Assessment, now shipped).

### 2.9 Operational-vagueness cluster (FR-154, M, M) ⚠

Operational-vagueness cluster: DSR forward immediate-vs-same-day ([`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):52/:88, pointers as of the #572 state); DSR restriction clock start (:70); critical-risk interim authority ([`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):124); supplier remediation gate ([`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):85); whistleblower timelines ([`governance/procedure-whistleblower-and-incident-reporting.md`](governance/procedure-whistleblower-and-incident-reporting.md):103); dept-continuity template blanks; incident-reporting escalation thresholds; model-lifecycle thresholds. **Decided (maintainer 2026-06-25): deepen all of the thin-baseline cluster** (FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154) to operational depth; this overrides the earlier "calibrate first, several are deliberately-thin baselines" guidance.

### 2.10 AI Article 22 + EU AI Act + FRIA unified workflow (FR-41, M, L)

AI Article 22 + EU AI Act + FRIA dual/triple-compliance workflow not documented as a unified workflow. (Privacy completion; FR-37/38/39/40/42 closed in #224-#228.)

### 2.11 Publications-assessment / poisoning-detection process for the scratch reference base (M, M) — surfaced 2026-06-25 (was 4.12)

The `grc_library_scratch` reference knowledge base is trust-bucketed: `ref/standards/`
and `ref/legislation/` (trusted, cite-as-authoritative), `ref/frameworks/` and the other
catalogue buckets (trusted per the scratch trust tiers), and `ref/publications/` (vendor
explainers, surveys, threat reports, interpretive guidance, **untrusted by default**).
The publications bucket is an AI trust-boundary / attack surface (an untrusted external
document in an AI's reference context can carry bias, error, or prompt-injection /
poisoning). **Maintainer-directed 2026-06-25**: create a formal process to (a) assess each
publication for useful and relevant information, and (b) identify poisoning or false
information, before any publication's content informs corpus work. Deliverables: a process
doc (likely a `skills/`-style workflow + a `ref/publications/README.md` protocol pointer)
covering intake screening (provenance, integrity, instruction-like-content detection per
the OWASP LLM prompt-injection / improper-output-handling guidance the corpus already
cites), an assess-and-tag step (relevant/useful vs discard; corroborate load-bearing
claims against a `standards/` source), and a recorded assessment per publication. Pairs
with the multi-session capability (closed as section 3.6 in the DONE ledger; the scratch ref base is part of it) and
the existing `governance/` trust disciplines. Honest-backstop framing: the process raises
the bar against poisoned reference input; it does not by itself guarantee detection.

---

### 2.12 DORA implementation annex operational deepening (M, M) — added 2026-07-04 (ad-hoc brief staged first per the convention)

Bring [`compliance/financial-services/annex-dora-implementation.md`](compliance/financial-services/annex-dora-implementation.md) to operational sufficiency per pillar (incident classification and reporting clocks, TLPT cadence, register-of-information, critical-ICT-third-party consequences), the FR-74 deepening shape; the held DORA text grounds every claim. Research brief staged in scratch (`research/dora-operational-deepening/`, 2026-07-04); the apply runs through the normal validate-then-apply pipeline when the delivery lands.

### 2.13 NIS2 implementation annex operational deepening (M, M) — added 2026-07-04 (ad-hoc brief staged first per the convention)

Bring [`compliance/annex-nis-2-implementation.md`](compliance/annex-nis-2-implementation.md) to operational sufficiency (scope determination, Article 21 measures, the Article 23 notification ladder, management-body accountability), grounded in the held directive; the DORA lex-specialis boundary coordinates with 2.12. Research brief staged in scratch (`research/nis2-implementation-deepening/`, 2026-07-04).

## Priority 3 — Clean up and tooling

Cross-document consistency cleanup and routine development / quality tooling: lower-priority than gaps, not error-prevention or adopter-facing. Picked deliberately into batches, not from the routine P1/P2 queue.

### 3.1 Sweep 3 follow-up: cross-document term/identifier consistency (L, S)

Cross-document term-and-identifier consistency gap (the prose-and-numbering C3 surface mechanical gates 35/39/41 don't cover). Candidate for a future mechanical gate; a manual sweep works the items meanwhile. **Both original bullets (the edition-explicit `ISO/IEC 27001:2022` header harmonization, 9 headers found and fixed; the stray-punctuation cells, all 7 recorded cells plus the supply-chain matrix's mangled legend line fixed) SHIPPED in the 2026-07-04 sweep PR**; the section stays open on the residual below.

- Sibling `/IEC`-form inconsistency (surfaced by the 2026-07-04 sweep census). **#650 (2026-07-05) shipped the 5 individual-document framework-alignment-table headers**: the 2 single `ISO 27001:2022` headers (`dev-security/guideline-ai-coding-assistant-security.md`, `operations/standard-production-security-requirements.md`) and the 3 combined-form `ISO 27001/27002` headers (`dev-security/standard-developer-security-requirements.md`, `dev-security/standard-devops-security-requirements.md`, `dev-security/standard-security-baseline-and-standards-reference.md`) were harmonized to the full `ISO/IEC` form (form only; values were already correct). Two parts remain OPEN, deferred to the maintainer as pending decisions ([`pending-decisions.md`](.working/pending-decisions.md)): (a) the FR-167 compliance matrix's 11 repeated per-domain `ISO 27001:2022` headers plus its line-29 legend row, which is NOT a display-only edit because gate 49 (`tools/lint-matrix-control-codes.py`) keys the matrix ISO column on the exact literal `ISO 27001:2022` (renaming the header silently blinds the gate), so harmonizing there requires a lockstep gate-constant, fixture, and docstring update in the same focused PR; (b) the FIT-8 register-CELL variant in [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (row 274's cell mixes bare `ISO 42001` with fully-qualified `ISO/IEC 42005:2025`; row 225's cell carries bare ISO forms `ISO 42001 §8, ISO 27001, ISO 23247`), a register-convention direction the maintainer must set. Values are correct throughout; this is form consistency only. The gate-exempt `dev-security/claude-rules/` pack tree carries its own bare `ISO 27001` headers and is deliberately outside this census frame.

### 3.4 Backlog effort-sizing labels convention (M, S) (was 4.2)

Backlog items now carry `(severity, effort)`; this item formalizes the convention. Proposed scale:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Surfaces to update when the convention formally lands**: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; this file (already in use); `.working/DONE.md` heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 3.12 CLAUDE.md removal-ledger review cadence (standing) — added 2026-06-28, PR #441 (was 4.27)

The PR #441 condense of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) moved the cut rationale, war-stories, and provenance into [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) (the removal ledger), each entry carrying an "evidence the removal was wrong" signal. Standing activity (not a one-time task): each `/retro` does a quick scan of the ledger's open RM entries and the periodic hallucination-metrics pass does a deeper one; if an entry's signal appears, advise the maintainer to restore the cut text or make a new CLAUDE.md change, and record the disposition in that entry's Status. Wired into [`.working/improvement-log.md`](.working/improvement-log.md)'s Convention section. This item is the durable tracker so the cadence is not lost; it stays open by design.

### 3.13 Audit-surfaced gate / tooling extensions (audit 2026-07-02) (S)

The citation-coverage extension shipped as gate 61 in its own PR; the remaining bullet is the optional positional-token lint below.

- **(from item 20) Positional-backlog-token lint.** Optional: a lint flagging `TODO P?N.M` positional tokens in gate-scanned corpus prose (they are renumber-fragile), nudging references toward stable FR-ids / topic names. Same class as the CLAUDE.md §N-orphan guard.

### 3.15 Guardrail-review machinery extensions (guardrail review 2026-07-02) (M mostly, S-M each)

Machinery findings from the 2026-07-02 guardrail review (gates, rules, skills, and toolchain assessed as a system; the corpus-audit siblings are section 3.13 above, still open on one optional bullet, and the former section 3.14, now closed; nothing below duplicated them). Every claim re-verified at source at intake; one lens-agent claim (a "gates 32 and 33" comment alleged in the date-staleness linter) was REFUTED at intake (zero grep hits) and is not carried. Each gate-shaped item is built the project way (four-surface wiring + regression fixture).

- **(GR-8 follow-on A, DECIDED 2026-07-04: build, L, S) Register-ageing advisory tool.** The GR-8(b) design round's option B, maintainer-chosen at the 2026-07-04 morning round: a small advisory `tools/audit-*.py` (not a gate) reporting improvement-log Proposed-improvement cells still pending after N PRs, the register-side analogue of the brief-freshness tool. Queue behind the P2 applies.
- **(GR-8 follow-on B, IN PROGRESS 2026-07-04, M) Expiry-tail one-pass batch review.** Maintainer-chosen mode for the aged pending candidates (236 pre-July rows): a drafted triage proposal (research subagent, orchestrator-verified) listing each row with a proposed CODIFIED/EXPIRED/ROUTED/keep verdict, reviewed by the maintainer in one round; tokens land only on the maintainer's dispositions (rejection and expiry are maintainer calls per the register convention).
- **(GR-10, L, S) History-aware gate subprocess batching.** Gate 31 spawns a git subprocess per document (200-plus spawns, run twice per pre-push via the guard) and gate 40 is heavier; a batched `git log --name-only` pass would trade `--follow` fidelity for one subprocess. Optimization only; correctness unaffected; queue behind the functional items.
- **(r3, [guardrails], L, S) D8 candidate (relabelled from the r3 review's "D6" after the pack-README co-bump check shipped as delta gate D6 in #623, and again from "D7" after the handoff-snapshot freshness check shipped as delta gate D7 in #634): TODO section-close orphan check.** A PR-time check failing when a TODO `###` heading deletion leaves live `§N` / `section N.M` references on gate-exempt surfaces (three logged misses: #469, #471, the #593 carrier pair). The close-out checklist's whole-repo grep is the convention it would mechanize; gate 62 does not cover bare refs or gate-exempt trees. The 2026-07-04 worker QA run's validated GR-GAP-2 duplicates this class and adds the one open design choice: an event-triggered PR-time delta check (fires on a TODO heading deletion, this bullet's original shape) versus a STANDING corpus scan of `.py` docstrings and `.claude/` markdown for stale section pointers; decide the shape at build time.
- **(QA-2026-07-04 GR-GAP-1, M-H, M) Require-registration citation-currency gate.** Both currency gates are enumeration-scoped: `lint-standards-currency.py` flags only register-recorded patterns and `lint-citations.py` is a hand-curated denylist, so a standard absent from both is structurally ungated; the corpus's own metrics record the ISO/IEC 29134 wrong-year escape (#162) and recurrence (#482) with exactly this diagnosis. Proposed: a gate extracting every `ISO/IEC NNNNN:YYYY`-shaped citation and failing on any standard-year pair not present in the canonical register (require-registration, not deny-known-bad). Validated from the worker QA run; DECIDED 2026-07-04 morning round: BUILD, queued after the P2 applies (the maintainer accepted the register-population and gate-27 re-verification costs). Boundary clause (r4 O-3): "present in the canonical register" is fixed as current-OR-superseded, so a superseded-but-registered standard-year pair stays gate 6's finding (the standards-currency audit already flags it) and this gate never double-fires on it; and every pair the register gains carries gate-27 citation-verification-freshness re-verification cost, named here so the scoping weighs it alongside population cost.
- **(r4 G-7, [guardrails], L-M, S) QA-report intake shape needs a durable carrier.** The three-layer intake (worker report, independent validation subagent, transcription-fidelity verifier) caught defects at each seam in its first run but lives only in the #626 records; DECIDED 2026-07-04 morning round: codify as a runbook section-5 subsection now, WITH a standing revisit note: on the channel's next recurrence, validate whether the full-skill option would serve better and surface that assessment to the maintainer.
- **(r5, [guardrails], M, S) Fence-predicate consolidation.** The fence-toggle predicate exists in at least ten carriers in three variants, and six private copies are TILDE-BLIND (pre-GR-4 semantics: gates 54 and 58's linters, `lint-links.py`, `lint-changelog-link-coverage.py`, `lint-shall-near-uncertainty.py`, `lint-directional-dependency.py`), so a file pairing one backtick fence with one tilde fence passes gate 66 (even shared-toggle count) while a tilde-blind linter sticks in code mode to EOF, the GR-4 silent-suppression class surviving in the copies. Consolidate on a shared `is_fence_line()` predicate (or the iterator itself) in `lint_common.py`, making gate 66's same-statement equivalence structural; latent today (zero tilde fences in the corpus census).
- **(r5, [guardrails], L-M, S) Count-vs-enumeration advisory candidate.** The figure-drift family's mechanizable subset: a delta-scoped advisory (not a gate) over added CHANGELOG/TODO lines flagging a spelled-or-numeral count that directly introduces a parenthesized enumeration whose marker count disagrees (the #636 five-vs-four shape). Honest limits: adjacent-enumeration subset only; dependent-clause and fold-omission drift stay with the staged recount clause. Full-history FP census before adoption; maintainer scopes (or adjudicates the subset too thin and rests on the EXPEDITE).
- **(r5, [guardrails], L, XS) Gate-66 default-population shape call.** The gate's default walk skips `.claude/`, but the mandated new-pack-prose `lint-language.py` run scans `.claude/` files via explicit paths with no exempt filter, so an unbalanced fence there suppresses that invocation's tail unseen (zero current findings; the docstring now records the residual honestly). Options: widen the default population to include `.claude/` (keep `.working/` exempt), or add the checklist half-line to run gate 66 on the same explicit paths.
- **(r5, [guardrails], protected-touch, S each) CLAUDE.md close-out-clause bundle (three shipped, one remaining).** SHIPPED: (1) the attended-autonomous rule-3 fallback reword dropping the longer-check-in option, in #652; (2) the close-out checklist's reconcile-bullet clause naming D7 as the mechanized version-token half (the gate-50 naming pattern), in #659; (3) the summary/description-lag close-out-checklist bullet (the #650-#653 /retro candidate, past the codification threshold at four in-window occurrences), in #659, grouped with (2) as both edit the same close-out-checklist section (the maintainer's 2026-07-05 group-by-logical-fit direction). REMAINING: the /claim-fit cadence-section clause (#630 out-of-window observation), sequenced as #660 after a research pass to spec it.
- **(#637 verifier F3, L, XS) D5 eighth escape form.** The bare closure phrasing `TODO N.M closed` (no `section` word, no `§`, no CLOSED marker) matches none of D5's seven forms; #637's lead was reworded to a detected form pre-push, but the phrasing is natural and will recur. Widen `tools/check-todo-rotation-on-pr.py` with an eighth form (backlog-file name then a bare decimal section token then a closed/closure word in the same clause, tolerating short intervening runs such as the #639 lead's "TODO 3.21's build-only half closed", forward-only window) AND a link-tolerant widening of the existing rotation-assertion form 6 (a markdown-linked DONE target defeats the literal, the #607 shape again: #640's "rotated to [`.working/DONE.md`](...)" was the NINTH escape phrasing), full-history FP census per the D5 convention, plus fixtures. The r5 gap lens adds the design-shape proposal for the same build: a DIFF-SIDE companion trigger (a PR whose TODO diff deletes a `###` heading or item block must carry the DONE ledger in the same diff, firing on the closure EVENT rather than its narration, closing the open-ended phrase tail from the other side; the existing `TodoRotation:` trailer covers the renumber/rescope false-positive cases, and the D8 candidate's heading-deletion detection is shareable code).
- **(#637 verifier F4/F6, L, XS) Acronym-linter digit-initial and reversed-order blind spots.** `tools/lint-acronym-consistency.py`'s `GLOSSARY_ROW_RE` and `INLINE_DEF_RE` require an `[A-Z]` first character, so the new 3PL glossary row (the register's first digit-initial term) and any future `2FA`-class entry are silently unparsed; and `INLINE_DEF_RE` additionally requires every expansion word to be capitalized, so canonical-order lowercase running-prose expansions (the #637 pair, `financial market infrastructure (FMI)` and `third-party logistics provider (3PL)`, verified consistent with their glossary rows by hand) are also invisible to it. Widen the row regex to `[A-Z0-9]`-initial and assess a lowercase-tolerant inline pattern, each with a fixture.

---

### 3.16 ETSI Securing-AI alignment map (L, M) — added 2026-07-04 (ad-hoc brief staged first per the convention)

Map the held ETSI SAI family (EN 304 223 plus the GR/TR set) against the corpus `ai/` security content: which requirements have no corpus carrier, which corpus claims an ETSI citation would strengthen, and a proposed alignment shape (options surfaced for maintainer scoping). Research DELIVERED (scratch inbox `inbox/worker-20260703-a/etsi-sai-alignment-research/`, 2026-07-04); research-only, the apply is a later decision. Citation form UNBLOCKED 2026-07-04: the maintainer supplied a fresh EN 304 223 V2.1.1 copy (identical page text to the held original), refuting the 2026-07-02 scratch-audit mis-designation finding (its TODO item is closed), so the map may cite the adopted EN as authoritative (scratch PR #100 records the confirmation).

### 3.17 MITRE ATLAS 2026.06 alignment and currency map (L, M) — added 2026-07-04 (ad-hoc brief staged first per the convention)

Coverage and identifier-currency map of the held ATLAS 2026.06 refresh against the corpus adversarial-AI content (which techniques lack carriers; which cited identifiers changed across the v5.6.0-to-2026.06 refresh), with a proposed update shape surfaced. Research DELIVERED (scratch inbox `inbox/worker-20260703-a/atlas-adversarial-alignment-research/`, 2026-07-04); research-only. **Pack-tree semantic-fit note (#654 verifier, 2026-07-05):** a future `/matrix-fit`-style pass over the pack `dev-security/claude-rules/ai/` LLM02 rows should weigh the kept `AML.T0024` (Exfiltration via AI Inference API) against `AML.T0057` (LLM Data Leakage), which may fit output-disclosure rows better; `AML.T0024` is current and correctly glossed, so #654 kept it within its currency-refresh scope, and this is a fit judgment rather than a currency defect.

### 3.21 Citation and naming hygiene residuals (S, XS) — rescoped 2026-07-04 (the three build-only fixes shipped; these await maintainer decisions)

The bundle's three build-only fixes SHIPPED 2026-07-04 (the ERC first-use expansion, the non-matrix legacy `C-TPAT` normalization, the reciprocal fresh-reader See-Also link, pack `1.54.1`; plus the same-family gate-13 DOCSTRING correction folded from the verifier's probe, distinct from the descoped spec-sentence reword in residual (c)). Four decision-parked residuals remain: (a) the compliance-matrix cell reading "C-TPAT Minimum Security Criteria" (arguably a legacy document-title quote; the maintainer's style call, chat decision item 1, recommended normalize); (b) FQ-F1, the five identical `tools/` PR-delta error strings using bare "ensure" (reword to the `ensure that` form or record the tool-string carve-out; chat decision item 7, recommended carve-out). (c) FQ-B1, DESCOPED from the 2026-07-04 build PR at the verifier-loop cap (three iterations on the replacement sentence, each refuted; maintainer chose descope): the master spec's line-214 "does not automatically enforce monotonicity" claim still stands and still needs the reword; the verifier's round-3 wording, evidence-quoted against gates 13/29/59 and P7-safe, awaits the maintainer's approval: "The audit suite's version-monotonicity audit (gate 13) enforces that the README's Library Version and every document's Version metadata field never decrease against the prior committed state; gate 13 passes an unchanged value (a missing library-version bump surfaces instead through the CHANGELOG-coupling gates 29 and 59, which require each PR's entry to carry a strictly higher Library Version matching the README), so reviewers should still verify the bump is present before approving the PR." (d) the three bare `PCI DSS v4` family-label citations in the AWS, Azure, and GCP cloud-hardening baselines (`dev-security/standard-cloud-hardening-baseline-{aws,azure,gcp}.md`) use the citation-form template's discouraged `PCI DSS v4` shape (a family label with no specific version or requirement ID); they are current (the v4 family, not the superseded `v4.0`), so TODO 3.22 (closed in #649) applied no currency migration to them, and the maintainer/citation-hygiene call is whether to normalize them to `v4.0.1` for specificity or leave the family reference (surfaced by the #648 verifier).

## Priority 4 — Adopter experience

Capability and guidance for organizations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install.

- **Distillation source**: the twelve `governance/` pack rules form the discipline core; `validation-sweep` and `library-fitness-review` form the periodic-review surface; the audit-programme architecture forms the mechanical-enforcement surface.
- **Generalization**: carry the patterns and discipline without the GRC-specific control-set citations; adopters supply their own document-type model and metadata-field set.
- **Open questions resolved 2026-06-22**: skill **family** (not omnibus); **prescriptive-only** (no linter scaffolds); **existing pack 1.x bump** (not a new pack). Sequencing: after the FR backlog closes.

### 4.2 Pack: dev-security/claude-rules language coverage review (M, M) (was 4.4)

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/). The pack's `languages/` tree already ships 11 language baseline files (including the decided subset; the earlier "Python-focused guidance only" premise was stale, corrected 2026-07-03), so the live work is the REVIEW of the existing subset files against `python.md`'s shape plus the positioning stance, not greenfield authoring. Decided 2026-06-22: baseline subset = **JS/TS + Go + Java** (others deferred); **explicitly position the pack as pointing to OWASP cheat sheets / dedicated technical-security sources rather than duplicating them**. Scope: one or more small PRs each bringing a subset baseline file up to `python.md`'s shape (adding a file only where the review finds a genuine gap) OR updating the pack README's positioning.

### 4.3 Overnight unattended-run driver (M, L) (was 4.7)

Deferred to a future session (maintainer-directed 2026-06-22). For longer unattended runs, a single overnight session is the wrong shape (it degrades like any long session). The sound architecture is an **external driver loop** (cron / CI / Agent SDK script, outside the corpus) that launches a **fresh `claude -p` or SDK session per task-unit**, each reading `.working/session-handoff.md` + the TODO/DONE queue, doing one unit, committing, advancing the queue, and exiting. The durable-state layer already exists (`session-handoff.md`, `/resume`, the green-merge-as-last-act + loop-break disciplines); the missing piece is the driver plus an overnight runbook.

- **Design questions**: where the driver runs; merge authority for unattended worker sessions; the stop condition; how a worker signals "needs maintainer" vs "safe to continue"; interaction with the `## overnight-work protocol` in the change-tracking rule.
- **Building blocks confirmed** (2026-06-22): `claude -p` fresh-by-default; Agent SDK fresh-session-per-call; no built-in overnight/auto-reset scheduler in CLI or web.

### 4.4 Worker-ready brief staging (whole eligible backlog) + `/subagent` external-worker entry (M, L) — maintainer-requested 2026-06-26; expanded per maintainer direction 2026-07-03 (was 4.16)

Stand up the INPUT half of the multi-session capability (its codification closed as section 3.6 in the DONE ledger) so separate-session / separate-account workers can pick up research tasks without waiting on the orchestrator. The 2026-07-03 maintainer direction expanded the original stage-on-dispatch design to STANDING WHOLE-BACKLOG COVERAGE: every TODO item has, in scratch, either a worker-ready brief or a recorded not-eligible verdict, kept current through the normal PR close-out. The settled design (the maintainer's three answers plus the accepted adjustments: eligible-only briefs with verdicts for the rest, the pointer-heavy content-light brief shape, a `Verified-against:` freshness stamp keyed on the main-repo PR number, artefact-derived state with no status fields, TODO-authoritative with briefs as a wipeable derived projection, TODO-delta-batched sync, targeted-first refresh with an advisory cross-repo freshness check) is recorded in [`.working/design-decisions.md`](.working/design-decisions.md) under "Worker-ready brief staging" and operationally in the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md) subsection 5.1 (both shipped with slice 1, 2026-07-03). Build state: slices 1, 2, 3, and 5 SHIPPED (slice 2 as scratch PR #50 plus scratch `validate.py` checks; slice 5 as the wave-1/2/3 seeding scratch PRs #51/#52/#53, whole backlog covered, 13 staged briefs and a verdict for every other item; slice 3 as the close-out pairing line, the `/resume` step-3 freshness check, and [`tools/audit-brief-freshness.py`](tools/audit-brief-freshness.py)). Remaining build slice:

1. **Slice 4, the `/subagent` slash command** as the external-worker entry point (read the assigned brief, claim it in `claims-ledger.md`, read the named main-repo files read-only, produce findings, deliver to `inbox/`, stop; **read-only-on-main MUST be enforced by the worker GitHub account's permissions, not by the prompt**, a prompt is not a security boundary per [`.claude/rules/secrets.md`](.claude/rules/secrets.md)) plus the maintainer-facing quick start in the runbook (provision the account, point the worker session at scratch, assign a brief, collect from `inbox/<worker-id>/`; maintainer-suggested 2026-07-02).

**Gating maintainer action**: provision the least-privilege worker account (read `grc_library` / write `grc_library_scratch` only). In-session `Agent` fan-out works today (shares the orchestrator's credentials, spends its budget); the external-worker path needs the account; slices 2 and 5 are useful before the account exists (maintainer-launched second-account sessions per the scratch `WORKER-ONBOARDING.md` can consume briefs today). **Partitionability**: unchanged; a corpus-wide sweep, rename, or single matrix stays single-session and gets a verdict, never a brief. **The apply stage stays single-session with full QA regardless** (the validate-then-apply no-bypass invariant: worker provenance never reduces the QA a change receives). **Seed-gap re-assessment (standing, maintainer-adopted 2026-07-04)**: at every close-out coverage sync, any not-eligible coverage row whose recorded reason names a decision or source that has since resolved gets a fresh verdict or a staged brief in the same sync; the operative convention text lives in the scratch coverage index header (first applied in the wave-4 seeding, scratch PR #70, which staged seven decision-unlocked briefs from the maintainer's 2026-07-04 overnight-prep round). Pairs with the closed section-3.6 codification (see the DONE ledger) and §2.11 (the publications-assessment process).

### 4.5 Fork-facing guidance + scripts for building an own reference base (L, L) — maintainer-directed 2026-06-27 (was 4.21)

Enable people who fork this library to assemble their **own** reference knowledge base (the authoritative source texts that authoring and citation work draws on) instead of depending on the maintainer's private one. The library is CC BY-SA 4.0 prose, but the source standards it cites (ISO/IEC 27001:2022 and the wider ISO catalogue, CSA CCM v4.1 / AICM v1.1 / CAIQ, NIST CSF 2.0, MITRE, OWASP, jurisdiction legislation) are proprietary or licence-restricted and are **not** redistributed in the corpus. The maintainer keeps those source texts in the separate `grc_library_scratch` repo's `ref/` tree (trust-bucketed `standards/` trusted, `legislation/` trusted-but-version-sensitive, `publications/` assess-first; plus an `ingest/` staging area, a `catalogue.yml`, and PDF-to-text / XLSX-to-CSV extracts for AI-readability). **That scratch repo is the maintainer's own private usage-and-reference and is NOT to be shared / not redistributed** (it holds licensed third-party works); this item is explicitly NOT "publish our scratch repo", it is "give a forker the method and tooling to build their own equivalent from sources they are licensed to hold".

Maintainer note (2026-06-27): the scratch `ref/` now holds the ISO references and is being expanded across the other source families; it stands as the maintainer's reference for content. The fork-facing capability mirrors its proven structure without exposing its contents.

Deliverables to scope at build (none built yet, this item only records the work):

1. **A fork-facing guidance doc** (candidate home: a `docs/` adopter guide, scope-and-confirm at build): where to obtain each cited standard from a known reputable / authoritative source (the issuing body's own store or an authorized distributor), the licensing posture (what a forker may hold privately vs redistribute), and how to upload their own licensed copies (e.g. purchased ISO PDFs) into a local reference tree.
2. **The trust-model and tree convention** a forker should adopt, mirroring the scratch `ref/` model: `standards/` (trusted ground truth, one dir per issuing body) vs `publications/` (assess-first, screen for bias / poisoning before use, per §2.11) vs `legislation/` (authoritative but version-sensitive), with an `ingest/` staging area and a machine-readable catalogue.
3. **Helper scripts** (`tools/`-style, scope precision at build): scaffold the `ref/` tree; fetch-from-reputable-source where a licence and a stable URL permit (never bypass paywalls / licensing); extract text for AI-readability (PDF to `--full-text.md`, spreadsheet to per-sheet CSV) mirroring the scratch extraction form; build / refresh the catalogue. Honour the security rules: no credential-bearing fetches in tracked config; treat downloaded `publications/` content as untrusted until screened.
4. **Wiring notes**: how a forker's reference base feeds the in-repo validator modules ([`tools/ccm_aicm_reference.py`](tools/ccm_aicm_reference.py), [`tools/nist_csf_reference.py`](tools/nist_csf_reference.py), [`tools/cobit_iso31000_reference.py`](tools/cobit_iso31000_reference.py)) that gates 48/49/54/58/61 build on, and the `/matrix-fit` semantic-fit audit (the [`matrix-fit`](dev-security/claude-rules/skills/matrix-fit/SKILL.md) skill, shipped #399), so a fork can validate control-code citations against its own ground truth.

Low urgency (maintainer flagged it as deferred, "a priority 5 item"); it is filed here in Priority 4 (adopter experience / tooling) because it is fork-facing tooling + guidance, the same class as the other Priority 4 tooling items, rather than the country / regulator content overlays Priority 5 enumerates. Pairs with §2.11 (the publications-assessment / poisoning-detection process) and the standing reference-base discipline the `/resume` Reference-knowledge-base step and the [`multi-session-orchestration`](.working/multi-session-orchestration.md) runbook §6 describe.

### 4.6 Adopter-experience enhancements (S-a..S-f; FYI/L, XS-L) — suggestions and maintainer-requested items

S-a through S-e are fresh-reader suggestions from the 2026-07-02 audit's persona pass (factual basis re-validated); S-f is a maintainer-requested item added 2026-07-04. The suggestions are enhancements (not defects) the maintainer triages; the maintainer-requested item is already accepted by construction. **Triage state 2026-07-04: S-c and S-d ACCEPTED by the maintainer** (research briefs staged in scratch, `research/s-c-adopter-direction-demo/` and `research/s-d-multi-entity-adoption/`, each owning one NEW `docs/` document; the builds apply through the normal validate-then-apply pipeline when the deliveries land); S-a, S-b, and S-e remain awaiting triage.

- **(S-a, L, M) Portal audience + maturity tags.** [`docs/portal.md`](docs/portal.md) has audience sections for CIO/CISO/GRC/architecture/privacy/compliance/audit/resilience/engineering but no Board/CEO section, and entries carry no inline maturity/status tag, so Draft v0.x annexes are indistinguishable from mature docs.
- **(S-b, XS) decision-tree unreachable from README.** [`docs/decision-tree.md`](docs/decision-tree.md) (the stated reading order) is not linked from the [`README.md`](README.md) routing table (reachable only via the portal). Add a routing-table link.
- **(S-c, M) No adopter-direction demo.** The adoption path terminates in [`docs/worked-example.md`](docs/worked-example.md), which is a contributor/ingestion walkthrough; there is no adopter-direction role-substitution demo.
- **(S-d, M) No multi-entity/group-structure adoption guidance.** No `docs/` adoption-surface guidance for adopting the library across a group / multi-entity / subsidiary structure (the concept appears only in substantive domain content).
- **(S-e, XS) Approving-Authority legend.** Add a legend note explaining the meta-role "Governance Library Maintainer" (285 docs) as an approving authority. NOTE: the audit framed [`dev-security/policy-secure-development-and-engineering.md`](dev-security/policy-secure-development-and-engineering.md):8 (approved by CIO) as a lone outlier; that is PARTIAL: CIO is the second-most-common approving authority (39 docs), so it is not anomalous.
- **(S-f, maintainer-requested 2026-07-04, M-L) Fork update-assessment tooling (upstream-change applicability report).** When an adopter's customized fork pulls upstream `grc_library` updates, nothing today helps THEIR AI assistant assess each upstream change against the fork's local customizations and present a decision matrix (accept / adapt / skip per change, with rationale), so cleanly understanding what upstream changed and selectively integrating the applicable components is manual. Design a fork-side instrument: likely a shareable skill (a prescriptive workflow: diff upstream release-to-release, classify each change by carrier class, document body, gate or linter, convention or pack rule, map each against the fork's recorded local divergences, and produce the per-change accept/adapt/skip report for the fork owner), plus upstream-side enablers where cheap (the structured CHANGELOG already carries the what and why per PR; consider machine-readable change-class tags or per-entry applicability hints as an upstream convention). Pairs with the delivered fork reference-base guidance (see the DONE ledger) and extends section 4.1's adopter framing; shape and upstream-vs-fork-side split are maintainer-scoped at design time.

### 4.7 Pack design improvements (guardrail review 2026-07-02) (M/L, S-L each)

Pack-architecture findings from the 2026-07-02 guardrail review; design-tier work scheduled last in the overnight sequence per the maintainer's interleave-by-risk direction.

- **(GR-P1, M, M) Session-lifecycle pack rule.** The wind-down / attended-autonomous / overnight / handoff apparatus lives only in the project [`.claude/CLAUDE.md`](.claude/CLAUDE.md); adopters inherit none of it, against the pack's own rule-is-the-distributable-form theory. Distribute it as a governance pack rule.
- **(GR-P2, M, L) Rule operative-core condense.** The 12 governance rules total roughly 31,000 words always-on, with fixed per-rule scaffolding (framework tables, why-sections, AI-assistant closers, repeated restatements of the audit-trail axiom) that is rationale, not operative instruction. Two-layer split per the PR #441 CLAUDE.md method: an always-on operative core plus on-demand rationale/provenance, with a removal ledger; per-rule PRs, `lint-language` run on each before first commit. Routed note (#560 `/validate-pr`, out-of-window): the change-tracking rule's two-file-split text says the root CHANGELOG entry carries "the same lead-paragraph wording as the detailed entry", but every entry in practice pairs matching headers with divergent lead wording (root long-form, mirror short-form); reconcile the rule text to the practice (or vice versa) when this rule is condensed.
- **(GR-P3, M, S) Third-occurrence-to-gate escalation convention.** The guardrail review's effectiveness finding: only false-positive-free mechanical gates extinguish failure classes; checklist/convention prose reduces but never stops recurrence (the narrow-scan class has recurred repeatedly across checklist lines, most recently inside Sweep 82's own verification). Codify: a failure class caught three or more times graduates automatically to a gate proposal (an improvement-log column plus a `/retro` step).
- **(GR-P4, L, S) Overlay primary-wins pointers and pruning stance.** The external overlay files under [`.claude/rules/external/`](.claude/rules/external/addyosmani/using-agent-skills.md) carry only a "supplementary" provenance tag; the primary-pack-wins-on-conflict resolution lives only in the project CLAUDE.md. Add a one-line pointer per overlay provenance comment, and record a pruning/refresh stance for the near-duplicate wrapper skills the review identified.
- **(GR-P5, L, S) `derives_from` re-point + coverage gaps.** [`dev-security/claude-rules/skills/deep-qa-review/SKILL.md`](dev-security/claude-rules/skills/deep-qa-review/SKILL.md) and [`dev-security/claude-rules/skills/library-fitness-review/SKILL.md`](dev-security/claude-rules/skills/library-fitness-review/SKILL.md) derive from `evidence-grounded-completion` (which already anchors many skills) rather than `trust-recovery-escalation` (the rule that defines them as its two-skill suite), leaving that rule looking skill-orphaned; re-point them. `validate-inference-before-action` and `surface-counterproductive-instructions` have no derived skill (the strongest candidates for one). Also hoist the exception-register "absent means strict mode" disclosure to the top of the rules that carry it: the hoistable sentence exists in gate-discipline and change-tracking only (artefact-and-branch-discipline carries a cross-reference, not the sentence), and the [`.claude/CLAUDE.md`](.claude/CLAUDE.md) Boundaries line names the wrong trio (it cites evidence-grounded-completion, which has zero exception-register mentions, instead of artefact-and-branch-discipline); correct that carrier in the same PR (a protected-file factual touch, logged per the overnight deferral rules).

---

## Priority 5 — Expand: country / regulator / programme overlays

Adding new coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately.

### 5.1 AI jurisdiction annexes (FR-62, M, S)

AI jurisdiction annexes absent. (Cross-references P5.9.) **Shape DECIDED 2026-07-04 (maintainer): a new `ai/jurisdictions/` subdirectory mirroring the `privacy/jurisdictions/` precedent, founded by the two held-source annexes (EU AI Act, Colorado AI Act), both carved out from the fr-41 work-unit's targets; research briefs staged in scratch (`research/fr-62-eu-ai-act-annex/`, `research/fr-62-colorado-ai-act-annex/`).** Remaining jurisdictions stay source-gated (see P5.9's candidate list). **Reference-base aid (2026-06-27 scratch-review S-8)**: `grc_library_scratch/ref/legislation/` holds the Colorado AI Act and EU AI Act full-text, and `ref/frameworks/ETSI/` holds the Securing-AI TR/GR set + EN 304 223 (AI baseline); ground the US-state and EU AI-annex authoring in those held sources.

### 5.2 Logistics country / programme expansion (was 5.1)

The WCO AEO Compendium identifies ~94 trusted-trader programmes globally; the library covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions: EU AEO (covers 27 member states under EU UCC Art 38), Mexico NEEC / OEA, Australia Trusted Trader (ATT), Singapore STP / STP-Plus, Japan AEO, Korea AEO, New Zealand Secure Exports Scheme (SES), Brazil OEA, China AEO.

### 5.3 Financial-services country regulator overlays (was 5.2)

Within `compliance/financial-services/`: UK PRA / FCA (`annex-uk-pra-fca.md`); US OCC / FRB / FDIC / SEC / FINRA; Canada OSFI; Australia APRA; Singapore MAS; Japan FSA.

### 5.4 Healthcare country regulator overlays (was 5.3)

Within `compliance/healthcare/`: US HIPAA detail (Privacy/Security/Breach-Notification Rules, HITECH); UK NHS DSPT; EU MDR / IVDR; Canada PHIPA and provincial frameworks; Australia My Health Records Act. **US HIPAA bullet UNLOCKED 2026-07-04 (maintainer): carved out of the delivered fr-60 work-unit as its own NEW US annex; research brief staged in scratch (`research/us-hipaa-healthcare-deepening/`, held HIPAA 45 CFR 160/162/164 plus NIST SP 800-66r2).** The other bullets stay source-gated (HITECH rides the US annex where the held CFR text supports it).

### 5.5 Energy and utilities country regulator overlays (was 5.4)

Within `compliance/energy-and-utilities/`: US NERC CIP standards; US TSA pipeline cybersecurity directives; UK Ofgem cyber requirements; EU ENISA sectoral guidance.

### 5.6 Telecommunications country regulator overlays (was 5.5)

Within `compliance/telecommunications/`: EU EECC; UK Ofcom telecom security framework; US FCC regulations; Australia ACMA requirements.

### 5.7 Public-sector country / regulator overlays (was 5.6)

Within `compliance/public-sector/`: UK Government Cyber Security Strategy and GovAssure; Australia ISM and PSPF; Canada IT Standards for federal departments; EU eIDAS public-sector authentication. **EU eIDAS bullet UNLOCKED 2026-07-04 (maintainer): a NEW eIDAS2 annex mirroring the FedRAMP annex shape; research brief staged in scratch (`research/eidas2-public-sector-annex/`, held eIDAS2 Regulation 2024/1183).** The other bullets stay source-gated.

### 5.8 Privacy jurisdiction gaps (was 5.7)

Existing privacy domain covers 25 country annexes. Known gaps or stale entries: Argentina (PDPA 2025 update pending); Saudi Arabia PDPL (recent updates pending); re-review of EU member-state derogations where applicable. **Mexico bullet UNLOCKED 2026-07-04 (maintainer): a standalone `annex-privacy-mexico.md`; research brief staged in scratch (`research/mexico-lfpdppp-privacy-annex/`, held LFPDPPP full text; fr-59's latin-america annex read-only in the partition).** The Argentina and Saudi bullets stay source-gated.

### 5.9 AI jurisdiction overlays (was 5.8)

The library cites EU AI Act extensively but lacked a dedicated `ai/jurisdictions/` subdirectory parallel to `privacy/jurisdictions/`. **The subdirectory shape and its first two annexes (EU AI Act, Colorado AI Act) were decided and briefed 2026-07-04 with P5.1 (one decision, one brief pair; see P5.1 for the staged-brief paths).** Remaining candidates, all source-gated pending maintainer drops: Canada AIDA; UK AI policy framework; NYC bias audit law; China generative AI rules; Korea AI framework.

---

## Priority 6 — Expand: new domains

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. Ordered lowest-effort-first.

### 6.1 Identity-specific content depth (L) (was 6.2)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. The library has IAM policy and procedure but no dedicated content for these patterns. **Research state (2026-07-04): the p6-1 scoping research is DELIVERED (scratch inbox, pending apply), and its three proposed documents are each briefed as follow-on work-units in scratch** (`research/ciam-governance-research/`, `research/identity-federation-patterns-research/`, `research/passwordless-adoption-research/`, grounded in the held NIST SP 800-63-4); the BUILD stays maintainer-schedule-gated.

### 6.2 Quantum cryptography readiness deepening (L) (was 6.3)

The library has a phase-level PQC roadmap ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md)) but not detailed implementation content. Pending: a PQC migration playbook (operational steps per system class), crypto-agility patterns (key abstraction, algorithm switching, hybrid schemes), and post-quantum-ready CA / PKI management. **Research state (2026-07-04): the corpus-internal scoping half is DELIVERED (scratch inbox `inbox/worker-20260703-a/quantum-pqc-readiness-scoping/`, pending apply; deepening options and a source-needs list surfaced, no regime claims)**; the regime half stays source-gated (no PQC standard held) and the BUILD schedule-gated.

### 6.3 Cross-framework matrix expansion (L) (was 6.4)

Current matrix ([`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)) covers major frameworks; expand to additional sectoral and regional frameworks as the P5 country/sector content grows.

### 6.4 CMMI capability levels alongside maturity levels (L) (was 6.5)

Per maintainer direction 2026-06-22 (low priority, after the FR backlog completes). The corpus uses the 5-tier maturity-level scale at both organization-wide and per-domain granularity; CMMI distinguishes the two (maturity levels 1-5 org-wide; capability levels 0-3 per practice area). Introducing capability levels would: (1) add a capability-level scheme to [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2; (2) update [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) to use capability levels per domain and aggregate to maturity levels at the programme rollup; (3) possibly extend [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md) DTI thresholds with a capability-level surface. **Research state (2026-07-04): the research-only integration mapping is DELIVERED (scratch inbox `inbox/worker-20260703-a/cmmi-sei-maturity-integration/`, pending maintainer decision; four integration-shape options surfaced, grounded in the CMMI V3.0 + SEI AI Adoption Maturity Model ingestions)**; the BUILD stays sequenced after the FR backlog completes.

### 6.5 Multi-cloud governance overlay (XL) (was 6.1)

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain. **Research state (2026-07-04): the research-only scoping is DELIVERED (scratch inbox `inbox/worker-20260703-a/multi-cloud-governance-scoping/`, pending maintainer decision; proposed document set and placement options surfaced)**; the BUILD stays P6 schedule-gated.

---

## Priority 7 — Awaiting maintainer decision

No open decisions pending. The FR-104 / FR-130 entries are dropped-decision audit-trail records (see [`.working/design-decisions.md`](.working/design-decisions.md)). The former 7.1 (do the audit-trail-only sections belong in TODO?) was decided 2026-07-03: all three sections KEEP, by design.

### 7.2 Per-regulation context (FR-104)

Per-regulation context not pursued.

### 7.3 Portal reorder (FR-130)

Portal reorder not pursued (README stays at decision-tree item 1).

---

## Scratch reference-base work (`grc_library_scratch`; ships via MCP PR per the git-proxy issue)

Validated defects in the `grc_library_scratch` reference repo from the 2026-07-02 audit. These ship as PRs to `grc_library_scratch` (not this repo); tracked here for visibility. Item 33 (tracked EPUBs) was decided 2026-07-02: keep tracked under the private-forever promise with watermark scrubbing gated (see [`.working/design-decisions.md`](.working/design-decisions.md)). Item 32 (the ETSI designation question) closed 2026-07-04: the maintainer-supplied fresh EN 304 223 copy refuted the mis-designation premise (scratch PR #100). SR-4 (catalogue/extract hygiene, items 30-31) closed 2026-07-05: item 31's report-PDF and KEEP-verdict count corrections (scratch PR #104) and item 30's drop of the WP-BCR failed-conversion stub (scratch PR #105); the SR-4 re-scoping against live scratch state surfaced a new finding (`ref/publications/originals/README.md` is a stale 2026-06-27 delivery snapshot making false present-tense claims), scoped as a maintainer decision in [`.working/pending-decisions.md`](.working/pending-decisions.md).

### SR-1 `last_checked` currency mechanism is inert (item 26, P2, S)

As of 2026-07-05, 5 of 240 `ref/catalogue.yml` items carry a `last_checked` field (the 2026-07-04 currency-check batch stamped ATLAS plus four others; scratch #101), and `tools/validate.py` checks the field's FORMAT only if present (no presence requirement), so the 7-day-throttle currency discipline in `CONTRIBUTING.md` has no on-disk footprint for the unstamped items. **Direction DECIDED** (maintainer, 2026-07-02, pending-decisions line 55): presence + backfill (backfill stamps on the currency-sensitive buckets, then add a presence/due-item check). **Execution egress-gated:** an honest backfill needs an upstream currency check per document (the reference-version-currency SOP), the same egress the 51 needs-reconfirm register rows and the ISO-31000 refresh wait on; stamping without checking would defeat the discipline. Held for the maintainer's egress instance.

### SR-2 no publications screening-record check (item 27, P2, M; pairs §2.11)

`tools/validate.py` has no publications screening-record check; 15 of 27 publication extracts (the EDPB/WP29 batch) have no per-extract screening record, and the batch's poisoning screen is provenance-only (`ingest-queue.md:92-94`). Pairs with §2.11 (the publications-assessment / poisoning-detection process).

### SR-3 `validate.py` binary-scan coverage gaps (items 28-29, P3, M)

(item 28) The disk->catalogue orphan check (`validate.py`:206) covers only `--full-text.md`; ~20 substantive CSV extracts (ATLAS/ATT&CK tactics + mitigations CSVs, CSA implementation/auditing-guideline tabs) are uncatalogued and unchecked. (item 29) The watermark/PII scan (`validate.py`:219-221) covers `.pdf` only; 22 EPUB + 16 office docs are unscanned. The audit directly scanned all 22 EPUBs and found NO watermark strings (a scan-coverage gap, not a live exposure); the .doc/.docx residual is unchecked. Widen both checks. The 2026-07-02 maintainer directive (watermarks always removed and never in the scratch repo; condition 3 of the keep-tracked decision) makes the item-29 widening load-bearing rather than hygiene: the widened scan is the mechanical enforcement of the scrub promise, so it covers every tracked binary format, not `.pdf` alone.

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see.
- **"Inference must be validated before committing or before anything else uses that information"** — operationalized in [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — operationalized in the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — operationalized in the validation-sweep [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9.
- **Sweep history is project-application, not template content** — operationalized by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — operationalized in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) PR-finalization-protocol section.
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — operationalized in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section and the same pack rule.
- **Validate cadence is 1-8 PRs per batch, not strictly 5** — the 5-PR cadence is default; the batch boundary is chosen at the natural seam.
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)` so the two ledgers are scannable in the same shape. Harmonized in PR #163.
- **Compute-don't-ask** (maintainer-flagged 2026-06-23) — before surfacing a question, apply a "can I compute/verify this myself?" gate; surface the result, not the raw question. (Codified 2026-06-30 into the `clarify-before-acting` rule's compute-first gate, #504.)

---

## Backlog totals

Approximate active counts after the 2026-06-30 work-type re-tier and the 2026-07-02 audit intake (the priority sections themselves are the source of truth; these drift).

- **P1 (fix errors and prevent recurrence)**: 3 items (1.5 reference version-currency, 1.9 the RM-10 pipe-guardrail hardening (maintainer-directed 2026-07-03, absorbing the section-3.15 r3 G-F1 bullet), and 1.11 the Brazil ANPD-restructuring and breach-rule citation verification (maintainer-directed 2026-07-05); the Quebec 72-hour confabulation sweep closed same-day, #631 catch to #633 fix; the audit-gate candidates closed with S3's `/claim-fit` ship 2026-07-04; the 2026-07-02 audit P1 cluster is fully closed; FR-48 completed in #596 through #607; the section-1.6 D5/CLAUDE.md codifications closed same-day).
- **P2 (fill significant gaps)**: 11 items (2.1-2.10 the FR deepenings FR-59 / 60 / 70 / 99 / 15 / 23 / 63 / 74 / 154 / 41, plus 2.11 publications-assessment; sections 2.12, 2.13, and 2.14 fully closed).
- **P3 (clean up and tooling)**: 5 items (3.1, 3.4, 3.12, plus 3.13 audit tooling extensions and 3.15 the 2026-07-02 guardrail-review machinery extensions; sections 3.6, 3.7, 3.8, 3.10, and 3.14 fully closed).
- **P4 (adopter experience)**: 7 items (4.1-4.5, plus 4.6 adopter-experience enhancements and 4.7 the 2026-07-02 guardrail-review pack-design improvements).
- **P5 (expand: country / regulator / programme overlays)**: 9 items (5.1-5.9).
- **P6 (expand: new domains)**: 5 items (6.1-6.5).
- **P7 (awaiting decision)**: 0 pending + 2 dropped-decision audit-trail entries (7.2 / 7.3; the former 7.1 decided 2026-07-03, keep-by-design).
- **Scratch reference-base work (`grc_library_scratch`)**: 3 open items (SR-1 last_checked, decided but egress-gated; SR-2 screening-record check; SR-3 validate.py binary-scan gaps), plus the 2026-07-05 `originals/README.md` stale-snapshot finding (scoped in pending-decisions). SR-4 (catalogue/extract hygiene) closed 2026-07-05 (scratch PRs #104, #105).

---

## Notes on maintenance

- Add new items at the appropriate priority; within a section keep the lowest-effort-first ordering. Move items between priorities as context changes.
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO. The P7 "dropped-decision" entries cross-reference those decisions for audit-trail completeness without duplicating the rationale.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view, kept in sync at fitness-review-cycle time.
