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
- **Maintainer-directed running order (2026-06-30 work-type re-tier)**: work the tiers in order. **P1** first (the cheap fix/prevent items: FR-48 and the §1.4 / §1.5 integrity tooling); then **P2** gaps (FR-59 and FR-60 deepenings and the deepen-baselines cluster first, then **FR-70**, the XL crypto-asset domain, last); then **P3** clean-up-and-tooling; then **P4** adopter experience. **P5 / P6 expansion waits** (maintainer: expansion can wait). The standing **fix-issues-first** directive (2026-06-27) governs within each tier, and the routine `/validate`, `/validate-pr`, and `/matrix-fit` cadences are the reactive half of P1. FR-167, the NIST SP 800 ingestion, and the OT post-ingestion validation are COMPLETE (2026-06-30; ingestion in `grc_library_scratch`, validation in #495).
- **Integrity-tooling items** (the former "guard-rails phase"): the citation-precision gate (§1.4 S3) and the reference version-currency residuals (§1.5) live in **P1** (fix errors and prevent recurrence); the QA-cadence and TODO/DONE-rotation surfaces are already covered by the bookkeeping-parity gate family (gates 50 and 57, plus the D5 PR-time check), and the retro guard rails (the former retro-log consolidation item) closed across #510 (the new-skill-drafting checklist) and #511 (the word-form count gate). Research fan-out (workers produce verified research from [`.working/worker-brief-template.md`](.working/worker-brief-template.md); the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing. The routine `/validate`, `/validate-pr`, and `/matrix-fit` cadences are the reactive half of this tier; the items below are the standing preventive half.

### 1.1 H2 numbering-pattern drift, entangled residual (FR-48, M, L)

Policy and standard documents used three H2 numbering patterns (fully-numbered `## N.`, fully-unnumbered `## Title`, and `## Section N:` labels). Maintainer decision 2026-07-01: normalize to **fully-numbered** (`## N.` H2 + hierarchical `### N.M` H3), taking the **safe subset first and deferring the entangled docs**. The safe subset (28 docs with no inbound `§N`/"Section N" citation, no anchor link, no intra-doc section self-reference, and no inline prose clause numbering coupled to the headings) was normalized via deterministic scripted apply + re-parse in this PR. **Residual (deferred, this item):** the 38 entangled docs whose sections ARE cited elsewhere, self-referenced, or coupled to inline clause numbers and would require a lockstep citation/clause remap (the full enumerated set, with each doc's entanglement reason, is the worklist in [`.working/fr48-deferred-worklist.md`](.working/fr48-deferred-worklist.md)), across four reference forms: (a) `§N`/`§N.M` subsection citations, markdown-link or bare-parenthetical (e.g. `policy-exception-and-risk-acceptance-management`, `standard-enterprise-risk-management`, `standard-logging-and-monitoring`, `policy-compliance-and-audit-management` cited `§4.3` by `procedure-capa.md`); (b) "Section N" prose citations (e.g. `standard-mobile-application-security`, which was cited by 6 `dev-security/claude-rules/languages/*.md` pack files plus the pack `README.md` (7 pack files total), all renumbered in #548; done); (c) intra-doc "Section N" self-references (`architecture/standard-technology-radar`, `architecture/standard-integration-architecture`); (d) inline prose clause numbering keyed to the old headings (`policy-compliance-and-audit-management`, `policy-legal-and-regulatory-compliance`, `policy-secure-development-and-engineering`, `policy-network-communications-security`, `policy-information-security`; a pre-push verifier caught these mid-PR, so they were reverted). Each needs its old-section-number to new-`§N` map applied to every citer and inline clause in the same PR; the numbering itself is gate-blind (gate 38 strips numbering), so this is editorial-consistency, not error-prevention. A dedicated effort (**one document per PR**, deterministic apply + citation remap + re-parse) is the shape being worked, per the maintainer's 2026-07-01 directive: one document at a time with maximal QA, no mass change until certain the renumber leaves zero broken links or references anywhere (this supersedes the earlier "one domain-batch per PR" framing, chosen for its smaller per-PR blast radius on a high-risk structural change).

### 1.4 Audit-gate candidates from the 2026-06-22 review (M, S each) (was 4.5)

Decided 2026-06-23 (maintainer triage): **build them all** from the 2026-06-22 review. **S3 remains** (the only open item in this section); the original S1 retention-consistency gate shipped in #462, S2 was closed in #463 as a register consolidation (the role-consistency check already existing as gate 8 `lint-roles.py`), and **S4 (no-bare-normative-`shall`) shipped in #466** (gate 56). Each is a `lint-*.py` + 4-surface wiring + regression fixture; one gate per PR to keep diffs reviewable.

- **S3 Citation-precision-for-claim gate**: flag "aligned with [normative source] X" claims and verify X actually contains the supporting language (catches FR-120-class issues).

### 1.5 Reference version-currency residuals (from the register version-currency build, #505) (S each)

The §1.5 reference version-currency register **shipped in #505** (the `Upstream check location` + `Last verified (UTC)` columns across all 16 register tables, the advisory staleness cadence in [`specification-citation-verification.md`](governance/specification-citation-verification.md) §12.3, the scratch-is-storage / upstream-is-authority principle, the §7 publisher allow-list extension, and 7 upstream-confirmed register corrections), and **all three citation version-upgrade follow-ups have now shipped** (ISO/IEC 27033 -> 27033-1:2015 #506; ISO/IEC 27036-2 2014 -> 2022 #507; NIST SP 800-88 Rev. 2 re-point + IEEE 2883 introduction #508). Remaining residuals:

- The **51 `needs-reconfirm` rows** (iso.org, the IEC webstore, and several government sources block automated fetch) await a browser or different-egress reconfirm pass to fill their `Upstream check location` URLs and stamp a verified date.

### 1.6 Risk-model internal consistency (audit 2026-07-02, items 1-3, H, L)

Three coupled risk-model defects surfaced by the 2026-07-02 read-only audit and re-validated at source. Not partitionable within the cluster (they share the risk taxonomy / scoring model); each sub-item is a distinct fix.

- **(item 1, H, M) Residual-risk formula contradiction.** [`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):111 computes `Residual = Inherent x (1 - control effectiveness)` (inherent = Likelihood x Impact at :107), while [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md):164 and [`risk/template-enterprise-risk-register.md`](risk/template-enterprise-risk-register.md):78 both give `Residual = Likelihood x Impact` (re-scored residual L x I). Two distinct models yielding different numbers. Pick a canonical residual model and align the dissenting surfaces. NOTE: standard §5.2 (:83) asserts scale/threshold parity with the methodology and points at the very section (§4-§5) containing the divergent formula, but the parity claim is scoped to the likelihood/impact scales and score-to-rating thresholds (which DO match), so it is not itself false, only misleading-adjacent.
- **(item 2, H, S) FR-171 residual carrier.** [`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):145 ("require ERC approval for High and Critical risks") and its roles table :38 ("ERC ... approves risk acceptance decisions") still carry the pre-FR-171 authority. FR-171 (closed #412/#416) realigned the acceptance procedure + appetite template to "Executive Committee or Board Risk Committee" with the ERC recommending only (per the role register); this methodology surface was missed. Residual of a closed FR, not a new FR.
- **(item 3, taxonomy H/effort L; AI-misroute H/S; band M/XS) Taxonomy fragmentation + misroute + band-name.** Risk-category schemes diverge: [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §4 has 10 categories, [`risk/template-enterprise-risk-register.md`](risk/template-enterprise-risk-register.md) has 12, [`risk/procedure-risk-register.md`](risk/procedure-risk-register.md):47 lists 8 + "other". Also [`risk/annex-ai-risk-methodology.md`](risk/annex-ai-risk-methodology.md):161 routes AI risks to the "Supplier category" despite a dedicated AI category existing (a correctness misroute), and [`risk/procedure-risk-acceptance.md`](risk/procedure-risk-acceptance.md):46 keys acceptance authority to a "Moderate" band that appears nowhere in the scoring model ("Medium" everywhere else). Canonical-taxonomy reconcile is non-partitionable; the AI-misroute and band-name are quick. Dedup: relates to §3.1 (term consistency) and §2.9 (FR-154).

### 1.7 Retention-value conflicts (audit item 4, H, M)

Cross-document retention-period conflicts that break the evidence chain (re-validated; three clear conflicts, one PARTIAL). [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md):99 mandates >=7 years for all audit reports (scope :32 includes AI + supplier audits) vs [`ai/procedure-ai-audit.md`](ai/procedure-ai-audit.md):108 ("5 years") and [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md):105,126 ("5 years"); [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md):290 ("minimum 7 years, consistent with the retention schedule") vs register :76 ("5 years"); PIA 7-years-flat ([`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md):235) vs register :73 ("5 years after decommission"). Reconcile to canonical values (stricter-safe leans to the 7-year floor for audit records) and correct the "consistent with the retention schedule" claims. PARTIAL sub-claim: register :84 "certification period + 5 years" is not a demonstrable absolute undershoot (a ~3y cert period + 5y likely exceeds 7y). Coupled P3 tooling: extend gate 55's `RETENTION_CHECKS` (in [`tools/lint-retention-consistency.py`](tools/lint-retention-consistency.py)) once canonical values are set (it is deliberately narrow today, only CAPA / internal-audit / control-testing pairs, and did not catch this cluster).

### 1.8 DSAR operational conflicts (audit item 5, H, M)

DSAR paired-document operational conflicts (re-validated; the audit misattributed two sub-claims to `template-dsar-workflow.md`, but the defects are real and live in the PROCEDURE). Sub-items:

- **Ladder conflict (M/H, M).** [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):96-100 (Standard/Enhanced/Re-verification, 10-business-day clock, fail->suspend) vs [`privacy/template-dsar-workflow.md`](privacy/template-dsar-workflow.md):56-66 (Low/Medium/High, 3-business-day SLA, fail->close); the template (:25) claims to provide "the identity verification ladder the procedure relies on", yet the two differ on levels, clock, and failure disposition. Decide which governs.
- **Denial self-review (H, S/M; partly authorial).** [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):47 makes the CIO the "acting DPO" who "Signs off on all denials", and :56 resolves all DPO references to the CIO, so the :289-295 denial workflow ("DPO documents grounds" -> "CIO (acting DPO) signs off") collapses into self-review (Legal Counsel is the only independent check). Needs an independent denial sign-off while the roles are merged. (Audit cited these as `template-dsar-workflow.md:56`; the template has no `CIO`/`72` at all: locator corrected to the procedure.)
- **72h restriction ack vs triage (M, S).** [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):70 sets a 72-hour restriction-of-processing acknowledgement that sits awkwardly against the multi-business-day triage SLAs. (Audit cited `template-dsar-workflow.md:70`; corrected to the procedure.) Dedup: §2.9 (FR-154) already lists DSR items (:52/:84/:70), so this partly overlaps that cluster.


---

## Priority 2 — Fill significant gaps

Deepening thin-but-present content to operational sufficiency, and the significant missing capabilities. The deepen-baselines cluster (FR-15 / 23 / 63 / 74 / 99 / 154 / 41) was decided for operational deepening (maintainer 2026-06-25).

### 2.1 Privacy jurisdiction annex operational deepening (FR-59, H, L)

Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the 25 country annexes to operational level. **Reference-base aid (2026-06-27 scratch-review S-7)**: `grc_library_scratch/ref/legislation/` now holds primary-source full-text for Japan APPI, Virginia VCDPA, Colorado Privacy Act, and the LATAM laws (Mexico, Brazil, Argentina, Colombia, Uruguay); author the deepening against those held sources. Honest caveat: APAC beyond Japan (Singapore, Australia, Korea, China, India) remains maintainer-drop (absent from the ref base).

### 2.2 HIPAA operational deepening (FR-60, H, L)

HIPAA adopter has no operational detail beyond a single 261-line sector annex in `compliance/healthcare`. Deepen.

### 2.3 Crypto-asset / blockchain governance domain (FR-70, H[critical], XL)

New domain for crypto-asset / blockchain governance — digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense. (Cross-references P6.x for domain-level shaping.)

### 2.4 Per-control effectiveness metrics (FR-99, M, M) ⚠

Per-control effectiveness metrics (continuous assurance / 3LoD).

### 2.5 Maturity-ladder methodology (FR-15, M, M)

Maturity-ladder methodology — median-of-medians scoring concern.

### 2.6 Audit-evidence assembler-verification standard (FR-23, M, M) ⚠

Audit-evidence assembler-verification standard absent.

### 2.7 Worked example: adoption, not ingestion (FR-63, M, M)

Worked example walks ingestion not adoption.

### 2.8 Schrems II operational deepening (FR-74, M, M)

Schrems II-light treatment. **Update 2026-06-30: the TIA instrument shipped in #483 (FR-34), which delivers the six-step transfer-impact assessment; FR-74's residual is the Schrems II operational deepening of the EU jurisdiction annex and the cross-border procedure (per the FR-154 "deepen to operational depth" decision). The TIA cross-reference wiring shipped in #489.** Consolidates with FR-34 (Transfer Impact Assessment, now shipped).

### 2.9 Operational-vagueness cluster (FR-154, M, M) ⚠

Operational-vagueness cluster: DSR forward immediate-vs-same-day ([`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):52/:84); DSR restriction clock start (:70); critical-risk interim authority ([`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):124); supplier remediation gate ([`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):85); whistleblower timelines ([`governance/procedure-whistleblower-and-incident-reporting.md`](governance/procedure-whistleblower-and-incident-reporting.md):103); dept-continuity template blanks; incident-reporting escalation thresholds; model-lifecycle thresholds. **Decided (maintainer 2026-06-25): deepen all of the thin-baseline cluster** (FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154) to operational depth; this overrides the earlier "calibrate first, several are deliberately-thin baselines" guidance.

### 2.10 AI Article 22 + EU AI Act + FRIA unified workflow (FR-41, M, L)

AI Article 22 + EU AI Act + FRIA dual/triple-compliance workflow not documented as a unified workflow. (Privacy completion; FR-37/38/39/40/42 closed in #224-#228.)

### 2.11 Publications-assessment / poisoning-detection process for the scratch reference base (M, M) — surfaced 2026-06-25 (was 4.12)

The `grc_library_scratch` reference knowledge base is split by trust into `ref/standards/`
(accepted standards, trusted, cite-as-authoritative) and `ref/publications/` (vendor
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
with the §3.6 multi-session track (the scratch ref base is part of that capability) and
the existing `governance/` trust disciplines. Honest-backstop framing: the process raises
the bar against poisoned reference input; it does not by itself guarantee detection.

### 2.12 External-citation corrections (audit 2026-07-02, items 6-10; H/M, S-M)

Citation-accuracy defects re-validated at source; three need upstream/source confirmation before the fix lands (the corpus CARRIER is confirmed in every case, the true external VALUE is flagged).

- **(item 6, L-M, XS) CCM "PRI" domain.** [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md):27 cites "CSA CCM v4.1 domains PRI and DSP"; PRI is a v3.x family (the project CCM v4.1 module classifies `PRI-*` as not-v4.1). Residual carrier the #428 domain-wide PRI sweep missed; line 27 is the sole remaining live-corpus PRI carrier. Drop "PRI and" or substitute the correct v4.1 domain.
- **(item 7, M, M; NEEDS-UPSTREAM year) BASC v6 year.** [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md):203 says BASC v6 (2022); ~12 live docs cite "v6 2023" (e.g. [`supply-chain/procedure-supplier-audit.md`](supply-chain/procedure-supplier-audit.md):23,92,175, [`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):23,164, [`security/policy-network-communications-security.md`](security/policy-network-communications-security.md):154). Register-vs-citer split is itself an internal-consistency defect; confirm the true BASC v6 year upstream (WBASCO), then reconcile with a bare-token grep (do not mass-flip 12 docs before confirmation).
- **(item 8, M, XS) ISO A.5.36 title fabricated.** [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md):23,128 cite "ISO/IEC 27001:2022 A.5.36 Policy on Exceptions"; the true Annex A title is "Compliance with policies, rules and standards for information security" (verified against the held ISO/IEC 27002:2022 extract in scratch). Correct the TITLE, x2 (not x3, the audit overcounted; :143-148 carry the bare code without the invented title, which is fine); the code A.5.36 itself is defensible.
- **(item 9, M, S; NEEDS-UPSTREAM titles) COBIT APO12.07 + ISO 31000 clause swap.** [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md):72 cites COBIT "APO12.07 Risk acceptance", which does not exist (COBIT 2019 APO12 ends at .06); :64-66 carry non-canonical APO12.01/.02/.03 titles; :66 mislabels ISO 31000 Integration as "5.4" while :70 correctly labels it "5.3" (an internally-provable self-inconsistency). Confirm canonical COBIT 2019 + ISO 31000:2018 clause titles upstream. Coupled P3 tooling: COBIT/ISO 31000 citations are gate-blind (gates 48/49/54/58 do not cover them); see §3.13.
- **(item 10, H, S; NEEDS-UPSTREAM regulation) Brazil breach citation.** [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md):177,321 and [`privacy/jurisdictions/annex-privacy-brazil.md`](privacy/jurisdictions/annex-privacy-brazil.md):41 cite "ANPD Resolution CD/ANPD No. 2, 2 business days"; the breach-notification regulation is likely Resolucao CD/ANPD no 15/2024 (3 business days; Res. No. 2 is the small-agents regulation). Confirm the current ANPD regulation + deadline upstream before correcting; two carriers already hedge "verify the current ANPD timeline".

### 2.13 Cross-document control and timing contradictions (audit 2026-07-02, items 11-14,16-19; H/M, S-M)

Unreconciled contradictions between paired documents (all re-validated at source). Each sub-item is independently fixable; several need a which-value-governs decision (stricter-safe leaning noted).

- **(item 11, M, S) GDPR DSR clock wording.** DSR clock written "30 days" not the statutory "one month" (GDPR Art 12(3)) in [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):66-72, [`privacy/template-dsar-workflow.md`](privacy/template-dsar-workflow.md):85, [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md):117; extension ceiling stated 90 days in the procedure vs "60 or 90" in the template; CCPA's 45-day window absent from the rights table. Dedup: DSR-clock cluster with §2.9 (FR-154) + §1.8.
- **(item 12, M, S) Incident P1 exec clock.** [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md):48 ("immediately" for P1) vs [`security/sop-incident-escalation-matrix.md`](security/sop-incident-escalation-matrix.md):40 ("CISO/CIO within 30 minutes"). Reconcile (stricter = immediately).
- **(item 13, M, S) MFA absolute-vs-exception.** [`security/standard-authentication-and-password-management.md`](security/standard-authentication-and-password-management.md):60 ("no circumstances ... without exception") vs :39/:91 CISO MFA-exception path. Authorial: decide whether MFA is truly absolute or exception-eligible.
- **(item 14, M, S) Internal-tier encryption at rest.** [`security/standard-data-classification-and-handling.md`](security/standard-data-classification-and-handling.md):57,116 ("optional"/portable-only) vs [`dev-security/standard-security-quick-reference.md`](dev-security/standard-security-quick-reference.md):90 ("Required for databases and backups"). Stricter-safe = required.
- **(item 16, M, S) Tier-3 supplier notification clock.** [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](supply-chain/standard-supplier-security-and-privacy-assurance.md):73,129 (72h incident) vs :91 (24h personal-data breach), no precedence rule for a Tier-3 personal-data processor. Stricter-safe = 24h where personal data is in scope.
- **(item 17, M, S) AI-audit CAPA crosswalk missing.** [`ai/procedure-ai-audit.md`](ai/procedure-ai-audit.md):88-92,121,125 (Minor/Major NC) routes to CAPA with no crosswalk to the canonical CAPA Critical/High/Moderate scheme; [`compliance/procedure-control-testing.md`](compliance/procedure-control-testing.md):162 is the precedent note. Major->10 business days maps to CAPA High, not Critical.
- **(item 18, M, S) CMS accountability.** [`compliance/policy-legal-and-regulatory-compliance.md`](compliance/policy-legal-and-regulatory-compliance.md):39 (CIO accountable for the CMS) vs [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md):44 (CCO maintains the CMS) and [`governance/register-role-authority.md`](governance/register-role-authority.md) (CCO owns compliance management). CIO:39 is the outlier; canonical = CCO.
- **(item 19, M-H, M) Risk-acceptance renewal-ceiling loophole.** [`risk/procedure-risk-acceptance.md`](risk/procedure-risk-acceptance.md):54-67 (pure risk-acceptance path) has no 540-day lifetime ceiling or renewal cap, while the exception path enforces them ([`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §3.4/§3.5). The exception policy's 4th-renewal escape hatch is conversion to a risk acceptance, so the ceiling is evadable via re-baselining. Add a matching ceiling or explicit cross-reference (stricter-safe).

### 2.14 Generated-surface count + positional-reference drift (audit 2026-07-02, items 20-21; M/L, S)

- **(item 20, L-M, M) Coverage-gaps positional TODO refs.** [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) cites positional backlog tokens (`TODO P5.1`, `P5.7`, `P6`, etc. at :63,:85,:103,:119 and throughout) that are renumber-fragile and now resolve to different topics after the 2026-06-30 re-tier. Root fix: reference stable FR-ids / topic names, not positional `P?N.M`. Optional coupled tooling: a lint for `TODO P?N.M` tokens in gate-scanned prose (see §3.13). Same fragility class as the CLAUDE.md §N-orphan guard.
- **(item 21, L, S) Portal hardcoded "four" vs five.** [`tools/build-portal.py`](tools/build-portal.py):322,343 hardcode "Four further adopter-facing documents" / "The four deeper-dive paths" while the emitted table lists five (the `template-startup-roadmap` was added later); siblings [`docs/adopter-guide.md`](docs/adopter-guide.md):25 and [`docs/decision-tree.md`](docs/decision-tree.md):25 repeat "one of four". Fix the generator source + the two siblings + regenerate [`docs/portal.md`](docs/portal.md). NOTE: [`docs/template-quickstart.md`](docs/template-quickstart.md):25 is already correct ("one of the deeper-dive paths", references the startup-roadmap): the audit's inclusion of it is REFUTED.


---

## Priority 3 — Clean up and tooling

Cross-document consistency cleanup and routine development / quality tooling: lower-priority than gaps, not error-prevention or adopter-facing. Picked deliberately into batches, not from the routine P1/P2 queue.

### 3.1 Sweep 3 follow-up: cross-document term/identifier consistency (L, S)

Cross-document term-and-identifier consistency gap (the prose-and-numbering C3 surface mechanical gates 35/39/41 don't cover). Candidate for a future mechanical gate; a manual sweep closes the open items meanwhile.

### 3.4 Backlog effort-sizing labels convention (M, S) (was 4.2)

Backlog items now carry `(severity, effort)`; this item formalises the convention. Proposed scale:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Surfaces to update when the convention formally lands**: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; this file (already in use); `.working/DONE.md` heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 3.6 Multi-session / multi-worker orchestration codification (M, L) — track; maintainer-scheduled (was 4.11)

Stand up the parallel-worker capability per the **"Multi-session / multi-worker orchestration model"** entry in [`.working/design-decisions.md`](.working/design-decisions.md) (the authoritative design; recovered to `main` in #316). A deliberately-scheduled meta/process track, not a routine backlog fix.

Deliverables 1-3 have shipped: the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md), the Model-B worker section in [`.working/worker-brief-template.md`](.working/worker-brief-template.md), and the light-SOP default in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) + the [`ai-assistant-workflow-disciplines`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) rule. **Remaining (the residue):**

4. A **worker-provenance audit gate**, co-designed with the shipped bookkeeping-parity gate family (gate 50 QA-cadence parity, plus gate 57 and the D5 PR-time check for rotation) as one "bookkeeping-parity" gate family, built the project way (`tools/lint-*.py` + four-surface wiring + regression fixture), honest-backstop framing per [`gate-discipline`](dev-security/claude-rules/governance/gate-discipline.md) (it enforces the PRESENCE of the verification record and provenance attestation, not semantic correctness). The separate pre-push-runner gate (folding gate-40/gate-31 into [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh)) already shipped in #333, so this gate extends rather than duplicates it. The codification PR is itself NOT partitionable (single orchestrator session).

- **Feasibility note:** `grc_library_scratch` is in scope, reachable, and now populated (the `ref/` base). The in-session subagent primitive is exercised; the separate-session external-collaborator primitive and harness support for repo-event subscription remain to confirm at implementation time (the design gates event-driven triggering as opt-in, not the default).
- **SCHEDULING (maintainer decides when):** default is to implement this AFTER the Priority 1 and Priority 2 backlog items are addressed. **Standing exception (do NOT self-authorize):** if at any point the orchestrator judges that standing up this capability would clear the REMAINING P1/P2 backlog faster than working solo on those items, net of the codification cost and counting only partitionable remaining work, surface a pull-forward recommendation with the reasoning (estimated remaining partitionable volume, expected speedup, build cost) and let the maintainer decide.

### 3.7 Session-concurrency safety: session-state lease + git cross-check (M, M) — maintainer-requested 2026-06-26 (was 4.18)

Build the concurrent-session interlock so a `/resume` issued while a prior session is still live cannot corrupt shared `main` state (handoff / TODO / DONE / validate-sweeps / detailed CHANGELOG / the four version surfaces). Full design (problem, options A/B/C, recommended mechanism, honest limitations, build steps, open sub-decisions) is captured in [`.working/design-decisions.md`](.working/design-decisions.md) under "Session-concurrency safety". Summary of the recommended option (C): a gate-exempt `.working/session-state.md` lease (active-session branch, status, `date -u` heartbeat, worker-dispatch list) PLUS a `git fetch` cross-check of recent unmerged `origin/claude/*` branches, wired as a new `/resume` step 0 that HOLDs + surfaces when a session looks live. Deliverables: the lease file + schema; `/resume` step 0; acquire/refresh/release lifecycle wiring in `.claude/CLAUDE.md` + the handoff; optionally a `lint-overnight-file`-style well-formedness gate (four-surface-wired). **Open sub-decisions for the maintainer to confirm at build time**: the staleness-window value (proposed 60 min), advisory-HOLD vs hard-block on a fresh-heartbeat active lease (proposed advisory), and whether to build the well-formedness gate now or defer. Honest scope note: this is an advisory interlock, not a hard mutex (no cross-container lock primitive exists); it prevents the realistic accidental-double-resume, not a determined simultaneous launch. Pairs with §3.6 (multi-session) and the bookkeeping-parity gate family (gate 50 QA-cadence parity plus gate 57 and the D5 PR-time check for rotation).

### 3.8 Orchestrator main-loop token instrumentation for session-metrics (L, S) — maintainer-requested 2026-06-27 (was 4.19)

The [`.working/session-metrics.md`](.working/session-metrics.md) ledger records measured `subagent_tokens` per phase, but the **Orchestrator tokens** column is always `not instrumented` (the convention forbids a fabricated figure). Maintainer-flagged 2026-06-27 to close the gap if feasible. **Feasibility investigated this session (PR #388)**: orchestrator main-loop tokens are NOT instrumentable from inside a session, because (a) no tool surfaces the orchestrator's own per-turn usage (the `Agent` tool returns only `subagent_tokens` for subagents), and (b) no main-session transcript carrying per-message `usage` / `output_tokens` is written to a readable on-disk location during the session (the session project dir holds only `subagents/` and `tool-results/` subdirectories; `~/.claude/sessions/<n>.json` is bare process metadata with no token fields). The realistic paths, none assistant-self-instrumentable today: (1) **harness support**, surface main-loop `usage` the way the `Agent` tool already surfaces `subagent_tokens`, or expose an end-of-session usage-summary (the clean fix; needs a Claude Code feature, so it is a feature request, not an in-repo build); (2) **maintainer-side external measurement**, read total session token usage from the Claude Code UI or the Anthropic Console usage view and record it out-of-band into the metrics row (available today; maintainer action, not assistant self-instrumentation); (3) **post-hoc transcript analysis**, IF a main-session conversation JSONL with `usage` fields is persisted to a readable location after the session ends (the subagent JSONLs persist under `projects/.../subagents/`, so a main transcript may appear post-session, but this is not verifiable from inside a live session), a small summing script over `output_tokens` would then be a low-effort build. Until a path lands the column stays `not instrumented`, which is the honest state the convention already mandates. Next concrete step (maintainer-gated): confirm whether a main-session `*.jsonl` carrying `usage` is retrievable post-session; if yes, a post-hoc summing aid is a small build; if no, the gap is a harness-feature request to file. This item closes when either the aid ships or the maintainer accepts `not instrumented` as the permanent state.

### 3.10 TODO-hygiene completion pass + accretion guard (S, S) — surfaced 2026-06-27 (was 4.23)

The maintainer flagged (2026-06-27) that shipped/historical content had accreted in TODO instead of rotating out. Parts (a) and (b) shipped in the TODO-hygiene PR: (a) §3.6 (multi-session orchestration) trimmed to its residue (deliverable 4, the worker-provenance gate; deliverables 1-3 shipped) after verifying against the gate inventory of the time; (b) the unambiguous shipped/closed clauses deleted (the Queueing-rules "FR-166/DD-1/DD-9 already shipped" note, the P3-intro "B2 closed #408 / DD-12 closed" parenthetical, the retro-log section's "actioned in #275" line, the §3.7 "D4 shipped in #366" clause, the Backlog-totals "closed in #N" clauses).

**Remaining (open):** (c) **whether the `## Standing conventions`, `## Backlog totals`, and `## Priority 7` (audit-trail-only) sections belong in TODO at all** or in a conventions / design-decisions doc. This is a **maintainer call** (they are non-forward-looking but appear intentionally retained); filed for decision in `## Priority 7`. The **accretion guard** is the TODO/DONE-rotation gate family, now shipped (gate 57 catches in-place self-marking; the D5 PR-time check catches a wholesale-forgotten rotation when a PR's CHANGELOG asserts a backlog-item closure). A possible extension (consider) is teaching gate 45 to flag shipped-PR-number history accreting inside an open TODO item, so accretion is mechanically prompted rather than convention-only.

### 3.12 CLAUDE.md removal-ledger review cadence (standing) — added 2026-06-28, PR #441 (was 4.27)

The PR #441 condense of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) moved the cut rationale, war-stories, and provenance into [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) (the removal ledger), each entry carrying an "evidence the removal was wrong" signal. Standing activity (not a one-time task): each `/retro` does a quick scan of the ledger's open RM entries and the periodic hallucination-metrics pass does a deeper one; if an entry's signal appears, advise the maintainer to restore the cut text or make a new CLAUDE.md change, and record the disposition in that entry's Status. Wired into [`.working/improvement-log.md`](.working/improvement-log.md)'s Convention section. This item is the durable tracker so the cadence is not lost; it stays open by design.

### 3.13 Audit-surfaced gate / tooling extensions (audit 2026-07-02) (M each)

Mechanical-coverage extensions the 2026-07-02 audit surfaced; each is a `tools/` change built the project way (four-surface wiring + regression fixture where a new/changed gate). Several are coupled to a fix item and should land after that item's canonical values are set.

- **(from item 4) Extend gate 55 `RETENTION_CHECKS`.** [`tools/lint-retention-consistency.py`](tools/lint-retention-consistency.py) tracks only three curated register/procedure retention pairs; extend it to the AI-audit, supplier-audit, privacy-breach, and PIA rows once §1.7 sets canonical values (do the reconcile first, then widen the gate so it locks the reconciled values).
- **(from item 25) Extend `lint-language.py` spelling coverage.** `ISE_PATTERN` (:99-118) covers 18 verb stems, verb-forms only, no `-isation` noun forms and missing stems (authorise/anonymise/pseudonymise). Add a companion `-isation` noun pattern + the missing stems. `customisation` (37 governed-corpus carriers, `customise` IS a stem but the noun is uncaught) is the cleanest proof. Gated on the §7.4 `organisation` decision (which noun forms are in scope).
- **(from item 9) COBIT + ISO 31000 citation coverage.** Gates 48/49/54/58 cover CCM/NIST/ISO-Annex-A control-code existence but not COBIT practice codes or ISO 31000 clause numbers, so the APO12.07 fabrication and the ISO 31000 clause swap in [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) are gate-blind. Extend `/matrix-fit` coverage or add a dedicated existence check (needs held COBIT 2019 / ISO 31000:2018 reference data, which scratch does not currently hold, so this may be source-gated).
- **(from item 20) Positional-backlog-token lint.** Optional: a lint flagging `TODO P?N.M` positional tokens in gate-scanned corpus prose (they are renumber-fragile), nudging references toward stable FR-ids / topic names. Same class as the CLAUDE.md §N-orphan guard.

### 3.14 Low-severity cleanup batch (audit 2026-07-02 low-sev + items 15,22,23,24) (L, XS-S)

Cheap, mostly-mechanical corrections re-validated at source; bundle into one or a few small PRs. (One audit low-sev candidate, the glossary CalVer/PR, was REFUTED: the glossary carries the standard 13-field block like its peers, and no document carries a Library Version/PR in its metadata, so it is not a finding.)

- **(item 15, XS) TLS 1.2 inline caveat.** [`dev-security/claude-rules/core/owasp.md`](dev-security/claude-rules/core/owasp.md):42,209 keeps the ASVS-baseline TLS 1.2 with no inline note that the project canonical mandate is TLS 1.3 ([`core/cryptography.md`](dev-security/claude-rules/core/cryptography.md):15,77 puts TLS 1.2 in the prohibited column). Add a one-line caveat; do not change the ASVS baseline.
- **(item 22, XS) Rollout phasing.** [`docs/decision-tree.md`](docs/decision-tree.md):36 ("30 / 90 / 180 days") vs the implementation-roadmap 90/180/365 ([`docs/template-quickstart.md`](docs/template-quickstart.md):54, portal). Align the decision-tree outlier or note they are distinct phasings.
- **(item 23, XS) Gate 55 absent from §5 grouping.** [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md):66-72 §5 category lists omit gate 55 (its §6 table row + prose exist); add it to the category-3 (content-drift) list.
- **(item 24, XS) "D1-D4" stale where D5 runs.** [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh):9-13 header, [`tools/pre-push-guard.sh`](tools/pre-push-guard.sh):14, and [`.claude/CLAUDE.md`](.claude/CLAUDE.md):152 say "D1-D4" though D5 now runs; update to D1-D5. (CLAUDE.md is a protected file, so its line is a maintainer-gated edit.)
- **(L-a, XS) Closed-section-1.3 docstring pointers.** [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py):46 and [`tools/check-todo-rotation-on-pr.py`](tools/check-todo-rotation-on-pr.py):74 cite the now-closed TODO section 1.3 (compute-don't-ask + word-form count gate, shipped #504/#511) in lineage comments; reword them to drop the closed-section reference (the section-orphan cleanup convention).
- **(L-b, XS) Stale "No open decisions".** [`.working/pending-decisions.md`](.working/pending-decisions.md) carries a "No open decisions" summary line that contradicts the top-of-file Status ("1 pending") and the open advisory-directive entry; reword the stale summary.
- **(L-c, S) FR-48 §1.1 stale framing.** This file's §1.1 (line ~28) still lists technology-radar / integration-architecture as deferred examples (done in #539/#540) and frames "38 entangled docs" as the residual (13 remain per [`.working/fr48-deferred-worklist.md`](.working/fr48-deferred-worklist.md)); refresh the examples + remaining-count.
- **(L-d, XS) Verbless "ensure that" sentences.** [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md):41 ("The CEO ensures that resourcing and independence of audit functions.") and :59 (broken "to ensure that adherence to ... programs"); corpus grep found only these two carriers.
- **(L-e, XS) Japan transliteration.** [`privacy/jurisdictions/annex-privacy-japan.md`](privacy/jurisdictions/annex-privacy-japan.md):37 has garbled "jūmyō kakomu jōhō"; correct to "kamei kakō jōhō (仮名加工情報)".
- **(L-f, M, S; cross-ref §1.7) Forensic-vs-incident retention.** [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md):239 (forensic evidence 7y) outlives [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md):63 (incident record 5y); align the incident-record row to the evidence floor or document the rationale. (A retention conflict like §1.7; kept here per the audit's low-sev tiering but flagged M.)
- **(L-g, S) Privacy charter hardcoded scope.** [`privacy/charter-privacy-management-programme.md`](privacy/charter-privacy-management-programme.md):32 hardcodes a four-region footprint against adopter-neutrality; make configurable.
- **(L-h, S) Risk-appetite template logistics leak.** [`risk/template-risk-appetite-statement.md`](risk/template-risk-appetite-statement.md):31,46,47,56 leak logistics/cargo/supply-chain specifics into a general template; genericize.
- **(L-j, XS) Classification field overloaded.** [`privacy/annex-regional-privacy-requirements.md`](privacy/annex-regional-privacy-requirements.md):10 `Classification: Deprecated` overloads the Classification metadata field with a lifecycle status.
- **(L-k, S) Pre-commit regen-before-check ordering.** [`.pre-commit-config.yaml`](.pre-commit-config.yaml):243-248 regenerates derived artefacts (no `--check`) BEFORE the `--check` hooks (:250-262), a local false-green (CI backstops with check-only). Reorder so `--check` precedes regen, or drop the local regen hook.


---

## Priority 4 — Adopter experience

Capability and guidance for organisations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install.

- **Distillation source**: the twelve `governance/` pack rules form the discipline core; `validation-sweep` and `library-fitness-review` form the periodic-review surface; the audit-programme architecture forms the mechanical-enforcement surface.
- **Generalisation**: carry the patterns and discipline without the GRC-specific control-set citations; adopters supply their own document-type model and metadata-field set.
- **Open questions resolved 2026-06-22**: skill **family** (not omnibus); **prescriptive-only** (no linter scaffolds); **existing pack 1.x bump** (not a new pack). Sequencing: after the FR backlog closes.

### 4.2 Pack: dev-security/claude-rules language coverage review (M, M) (was 4.4)

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/). Today the pack ships Python-focused guidance plus external overlay rules. Decided 2026-06-22: baseline subset = **JS/TS + Go + Java** (others deferred); **explicitly position the pack as pointing to OWASP cheat sheets / dedicated technical-security sources rather than duplicating them**. Scope: one or more small PRs each adding a language baseline file (mirror `python.md`'s shape) OR updating the pack README's positioning.

### 4.3 Overnight unattended-run driver (M, L) (was 4.7)

Deferred to a future session (maintainer-directed 2026-06-22). For longer unattended runs, a single overnight session is the wrong shape (it degrades like any long session). The sound architecture is an **external driver loop** (cron / CI / Agent SDK script, outside the corpus) that launches a **fresh `claude -p` or SDK session per task-unit**, each reading `.working/session-handoff.md` + the TODO/DONE queue, doing one unit, committing, advancing the queue, and exiting. The durable-state layer already exists (`session-handoff.md`, `/resume`, the green-merge-as-last-act + loop-break disciplines); the missing piece is the driver plus an overnight runbook.

- **Design questions**: where the driver runs; merge authority for unattended worker sessions; the stop condition; how a worker signals "needs maintainer" vs "safe to continue"; interaction with the `## overnight-work protocol` in the change-tracking rule.
- **Building blocks confirmed** (2026-06-22): `claude -p` fresh-by-default; Agent SDK fresh-session-per-call; no built-in overnight/auto-reset scheduler in CLI or web.

### 4.4 Multi-session research-brief staging + `/subagent` external-worker entry (M, M) — maintainer-requested 2026-06-26 (was 4.16)

Stand up the INPUT half of the §3.6 multi-session capability so separate-session / separate-account workers can pick up research tasks (the existing §3.6 work delivered the runbook, the worker `CLAUDE.md` contract, the light SOP, and the bookkeeping-parity gate; this adds the brief-staging input channel and the worker entry command). Design advised 2026-06-26; deliverables:

1. **A `research/<work-unit-id>/brief.md` convention in [`grc_library_scratch`](https://github.com/jposluns/grc_library_scratch)** (one brief per partitionable TODO or per FR-167 batch), orchestrator-authored from [`.working/worker-brief-template.md`](.working/worker-brief-template.md): the task, the exact main-repo target paths, the verified-disjoint partition, the `path:line` evidence requirement, the deliverable shape (research, not final prose), the stop-don't-merge and verify-against-live-main invariants, and a pointer to the scratch worker `CLAUDE.md` for the general contract (reference, do not duplicate). Workers deliver findings to the existing `inbox/<worker-id>/`.
2. **A `/subagent` slash command** as the external-worker entry point: read the assigned brief, claim it in `claims-ledger.md`, read the named main-repo files read-only, produce findings, deliver to `inbox/`, stop. **Read-only-on-main MUST be enforced by the worker GitHub account's permissions, not by the prompt** (a prompt is not a security boundary, per [`.claude/rules/secrets.md`](.claude/rules/secrets.md) / the security rules).
3. **Codify both** in the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md); add the `/subagent` command file.

**Gating maintainer action**: provision the least-privilege worker account (read `grc_library` / write `grc_library_scratch` only). In-session `Agent` fan-out works today (shares the orchestrator's credentials, spends its budget); the external-worker path needs the account. **Partitionability**: the decided-content TODOs (the FR-59 / FR-60 deepenings and the deepen-baselines cluster, separate files) are the cleanest fit; a corpus-wide sweep, rename, or single matrix stays single-session. **The apply stage stays single-session with full QA regardless** (the validate-then-apply no-bypass invariant: worker provenance never reduces the QA a change receives). Pairs with §3.6 and §2.11 (the publications-assessment process).

### 4.5 Fork-facing guidance + scripts for building an own reference base (L, L) — maintainer-directed 2026-06-27 (was 4.21)

Enable people who fork this library to assemble their **own** reference knowledge base (the authoritative source texts that authoring and citation work draws on) instead of depending on the maintainer's private one. The library is CC BY-SA 4.0 prose, but the source standards it cites (ISO/IEC 27001:2022 and the wider ISO catalogue, CSA CCM v4.1 / AICM v1.1 / CAIQ, NIST CSF 2.0, MITRE, OWASP, jurisdiction legislation) are proprietary or licence-restricted and are **not** redistributed in the corpus. The maintainer keeps those source texts in the separate `grc_library_scratch` repo's `ref/` tree (trust-bucketed `standards/` trusted, `legislation/` trusted-but-version-sensitive, `publications/` assess-first; plus an `ingest/` staging area, a `catalogue.yml`, and PDF-to-text / XLSX-to-CSV extracts for AI-readability). **That scratch repo is the maintainer's own private usage-and-reference and is NOT to be shared / not redistributed** (it holds licensed third-party works); this item is explicitly NOT "publish our scratch repo", it is "give a forker the method and tooling to build their own equivalent from sources they are licensed to hold".

Maintainer note (2026-06-27): the scratch `ref/` now holds the ISO references and is being expanded across the other source families; it stands as the maintainer's reference for content. The fork-facing capability mirrors its proven structure without exposing its contents.

Deliverables to scope at build (none built yet, this item only records the work):

1. **A fork-facing guidance doc** (candidate home: a `docs/` adopter guide, scope-and-confirm at build): where to obtain each cited standard from a known reputable / authoritative source (the issuing body's own store or an authorized distributor), the licensing posture (what a forker may hold privately vs redistribute), and how to upload their own licensed copies (e.g. purchased ISO PDFs) into a local reference tree.
2. **The trust-model and tree convention** a forker should adopt, mirroring the scratch `ref/` model: `standards/` (trusted ground truth, one dir per issuing body) vs `publications/` (assess-first, screen for bias / poisoning before use, per §2.11) vs `legislation/` (authoritative but version-sensitive), with an `ingest/` staging area and a machine-readable catalogue.
3. **Helper scripts** (`tools/`-style, scope precision at build): scaffold the `ref/` tree; fetch-from-reputable-source where a licence and a stable URL permit (never bypass paywalls / licensing); extract text for AI-readability (PDF to `--full-text.md`, spreadsheet to per-sheet CSV) mirroring the scratch extraction form; build / refresh the catalogue. Honour the security rules: no credential-bearing fetches in tracked config; treat downloaded `publications/` content as untrusted until screened.
4. **Wiring notes**: how a forker's reference base feeds the in-repo validator modules ([`tools/ccm_aicm_reference.py`](tools/ccm_aicm_reference.py), [`tools/nist_csf_reference.py`](tools/nist_csf_reference.py)) that gates 48/49/54 build on, and the `/matrix-fit` semantic-fit audit (the [`matrix-fit`](dev-security/claude-rules/skills/matrix-fit/SKILL.md) skill, shipped #399), so a fork can validate control-code citations against its own ground truth.

Low urgency (maintainer flagged it as deferred, "a priority 5 item"); it is filed here in Priority 4 (adopter experience / tooling) because it is fork-facing tooling + guidance, the same class as the other Priority 4 tooling items, rather than the country / regulator content overlays Priority 5 enumerates. Pairs with §2.11 (the publications-assessment / poisoning-detection process) and the standing reference-base discipline the `/resume` Reference-knowledge-base step and the [`multi-session-orchestration`](.working/multi-session-orchestration.md) runbook §6 describe.

### 4.6 Adopter-experience enhancements (audit 2026-07-02, S-a..S-e; FYI/L, XS-M) — suggestions for maintainer triage

Fresh-reader suggestions from the 2026-07-02 audit's persona pass; factual basis re-validated. These are enhancement suggestions (not defects); the maintainer triages which to pursue.

- **(S-a, L, M) Portal audience + maturity tags.** [`docs/portal.md`](docs/portal.md) has audience sections for CIO/CISO/GRC/architecture/privacy/compliance/audit/resilience/engineering but no Board/CEO section, and entries carry no inline maturity/status tag, so Draft v0.x annexes are indistinguishable from mature docs.
- **(S-b, XS) decision-tree unreachable from README.** [`docs/decision-tree.md`](docs/decision-tree.md) (the stated reading order) is not linked from the [`README.md`](README.md) routing table (reachable only via the portal). Add a routing-table link.
- **(S-c, M) No adopter-direction demo.** The adoption path terminates in [`docs/worked-example.md`](docs/worked-example.md), which is a contributor/ingestion walkthrough; there is no adopter-direction role-substitution demo.
- **(S-d, M) No multi-entity/group-structure adoption guidance.** No `docs/` adoption-surface guidance for adopting the library across a group / multi-entity / subsidiary structure (the concept appears only in substantive domain content).
- **(S-e, XS) Approving-Authority legend.** Add a legend note explaining the meta-role "Governance Library Maintainer" (285 docs) as an approving authority. NOTE: the audit framed [`dev-security/policy-secure-development-and-engineering.md`](dev-security/policy-secure-development-and-engineering.md):8 (approved by CIO) as a lone outlier; that is PARTIAL: CIO is the second-most-common approving authority (39 docs), so it is not anomalous.


---

## Priority 5 — Expand: country / regulator / programme overlays

Adding new coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately.

### 5.1 AI jurisdiction annexes (FR-62, M, S)

AI jurisdiction annexes absent. (Cross-references P5.9.) **Reference-base aid (2026-06-27 scratch-review S-8)**: `grc_library_scratch/ref/legislation/` holds the Colorado AI Act and EU AI Act full-text, and `ref/frameworks/ETSI/` holds the Securing-AI TR/GR set + EN 304 223 (AI baseline); ground the US-state and EU AI-annex authoring in those held sources.

### 5.2 Logistics country / programme expansion (was 5.1)

The WCO AEO Compendium identifies ~94 trusted-trader programmes globally; the library covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions: EU AEO (covers 27 member states under EU UCC Art 38), Mexico NEEC / OEA, Australia Trusted Trader (ATT), Singapore STP / STP-Plus, Japan AEO, Korea AEO, New Zealand Secure Exports Scheme (SES), China AEO.

### 5.3 Financial-services country regulator overlays (was 5.2)

Within `compliance/financial-services/`: UK PRA / FCA (`annex-uk-pra-fca.md`); US OCC / FRB / FDIC / SEC / FINRA; Canada OSFI; Australia APRA; Singapore MAS; Japan FSA.

### 5.4 Healthcare country regulator overlays (was 5.3)

Within `compliance/healthcare/`: US HIPAA detail (Privacy/Security/Breach-Notification Rules, HITECH); UK NHS DSPT; EU MDR / IVDR; Canada PHIPA and provincial frameworks; Australia My Health Records Act.

### 5.5 Energy and utilities country regulator overlays (was 5.4)

Within `compliance/energy-and-utilities/`: US NERC CIP standards; US TSA pipeline cybersecurity directives; UK Ofgem cyber requirements; EU ENISA sectoral guidance.

### 5.6 Telecommunications country regulator overlays (was 5.5)

Within `compliance/telecommunications/`: EU EECC; UK Ofcom telecom security framework; US FCC regulations; Australia ACMA requirements.

### 5.7 Public-sector country / regulator overlays (was 5.6)

Within `compliance/public-sector/`: UK Government Cyber Security Strategy and GovAssure; Australia ISM and PSPF; Canada IT Standards for federal departments; EU eIDAS public-sector authentication.

### 5.8 Privacy jurisdiction gaps (was 5.7)

Existing privacy domain covers 25 country annexes. Known gaps or stale entries: Argentina (PDPA 2025 update pending); Saudi Arabia PDPL (recent updates pending); Mexico LFPDPPP (standalone annex possible); re-review of EU member-state derogations where applicable.

### 5.9 AI jurisdiction overlays (was 5.8)

The library cites EU AI Act extensively but lacks a dedicated `ai/jurisdictions/` subdirectory parallel to `privacy/jurisdictions/`. Candidates: EU AI Act detailed annex; Canada AIDA; UK AI policy framework; US state-by-state AI laws (Colorado AI Act, NYC bias audit law); China generative AI rules; Korea AI framework.


---

## Priority 6 — Expand: new domains

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. Ordered lowest-effort-first.

### 6.1 Identity-specific content depth (L) (was 6.2)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. The library has IAM policy and procedure but no dedicated content for these patterns.

### 6.2 Quantum cryptography readiness deepening (L) (was 6.3)

The library has a phase-level PQC roadmap ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md)) but not detailed implementation content. Pending: a PQC migration playbook (operational steps per system class), crypto-agility patterns (key abstraction, algorithm switching, hybrid schemes), and post-quantum-ready CA / PKI management.

### 6.3 Cross-framework matrix expansion (L) (was 6.4)

Current matrix ([`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)) covers major frameworks; expand to additional sectoral and regional frameworks as the P5 country/sector content grows.

### 6.4 CMMI capability levels alongside maturity levels (L) (was 6.5)

Per maintainer direction 2026-06-22 (low priority, after the FR backlog completes). The corpus uses the 5-tier maturity-level scale at both organisation-wide and per-domain granularity; CMMI distinguishes the two (maturity levels 1-5 org-wide; capability levels 0-3 per practice area). Introducing capability levels would: (1) add a capability-level scheme to [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2; (2) update [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) to use capability levels per domain and aggregate to maturity levels at the programme rollup; (3) possibly extend [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md) DTI thresholds with a capability-level surface.

### 6.5 Multi-cloud governance overlay (XL) (was 6.1)

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain.


---

## Priority 7 — Awaiting maintainer decision

Three open decisions pending (§7.1 the TODO audit-trail-only sections question / §3.10(c); §7.4 the "organisation" spelling convention; §7.5 the tracked O'Reilly EPUBs). The FR-104 / FR-130 entries are dropped-decision audit-trail records (see [`.working/design-decisions.md`](.working/design-decisions.md)).

### 7.1 Do the audit-trail-only sections belong in TODO? (§3.10(c))

Do the audit-trail-only sections (`## Standing conventions`, `## Backlog totals`, `## Priority 7`) belong in TODO at all, or in a conventions / design-decisions doc? They are non-forward-looking but appear intentionally retained. Maintainer call; left in place pending the decision.

### 7.2 Per-regulation context (FR-104)

Per-regulation context not pursued.

### 7.3 Portal reorder (FR-130)

Portal reorder not pursued (README stays at decision-tree item 1).

### 7.4 "organisation" spelling: Commonwealth exception vs harmonize (audit 2026-07-02, item 25)

The corpus carries **~1026 governed-corpus `organisation`** against **3 `organization`**, contradicting the stated Canadian `-ize`/`-ization` convention (which `tools/lint-language.py` enforces for verb stems). This is an overwhelming de-facto Commonwealth house choice, not drift, so it is an authorial decision, not a mechanical sweep: **either** sanction `organisation` as an explicit documented Commonwealth exception in the language convention (and add it to the linter's allowed set), **or** harmonize the ~1026 instances to `organization`. Decide before the §3.13 `lint-language` noun-form extension lands (that extension's scope depends on this). Do NOT silently pick.

### 7.5 O'Reilly EPUBs tracked in git (audit 2026-07-02, item 33; scratch; H copyright)

`grc_library_scratch` tracks **22 full copyrighted O'Reilly EPUBs** under `ref/publications/originals/books/` in git, despite the "not redistributed" stance in scratch `CONTRIBUTING.md` (tracking full copyrighted binaries in a git repo is itself distribution of them). Maintainer decision: keep as-is, purge from git, move to git-LFS/out-of-band, or de-track. Copyright/licensing exposure, so escalated rather than actioned autonomously.

---

## Scratch reference-base work (`grc_library_scratch`; ships via MCP PR per the git-proxy issue)

Validated defects in the `grc_library_scratch` reference repo from the 2026-07-02 audit. These ship as PRs to `grc_library_scratch` (not this repo); tracked here for visibility. Item 33 (tracked EPUBs) is the §7.5 decision; item 32's corpus-side carrier is noted in SR-5.

### SR-1 `last_checked` currency mechanism is inert (item 26, P2, S)

0 of 233 `ref/catalogue.yml` items carry a `last_checked` field (even the 2026-07-01 ATLAS refresh did not stamp it), and `tools/validate.py`:72-74 checks the field's FORMAT only if present (no presence requirement), so the 7-day-throttle currency discipline in `CONTRIBUTING.md` has no on-disk footprint. Backfill stamps on currency-sensitive buckets and add a presence/due-item check, OR amend the documented SOP. (Design decision: whether to require presence.)

### SR-2 no publications screening-record check (item 27, P2, M; pairs §2.11)

`tools/validate.py` has no publications screening-record check; 15 of 27 publication extracts (the EDPB/WP29 batch) have no per-extract screening record, and the batch's poisoning screen is provenance-only (`ingest-queue.md:92-94`). Pairs with §2.11 (the publications-assessment / poisoning-detection process).

### SR-3 `validate.py` binary-scan coverage gaps (items 28-29, P3, M)

(item 28) The disk->catalogue orphan check (`validate.py`:206) covers only `--full-text.md`; ~20 substantive CSV extracts (ATLAS/ATT&CK tactics + mitigations CSVs, CSA implementation/auditing-guideline tabs) are uncatalogued and unchecked. (item 29) The watermark/PII scan (`validate.py`:219-221) covers `.pdf` only; 22 EPUB + 16 office docs are unscanned. The audit directly scanned all 22 EPUBs and found NO watermark strings (a scan-coverage gap, not a live exposure); the .doc/.docx residual is unchecked. Widen both checks.

### SR-4 catalogue / extract hygiene (items 30-31, P3, XS)

(item 30) `ref/publications/WP-BCR-P-Processor-Application-Form--full-text.md` is a 589-byte failed conversion ("conversion produced no text; consult the .doc original") catalogued as a usable extract; drop it from the catalogue or redo the .doc conversion. (item 31) `ref/publications/README.md`:19 says 13 report PDFs (12 on disk; the 13th was reclassified to standards), and `ingest-queue.md`:31-33 says "the 12 KEEP extracts are trimmed" when only 9 are KEEP-TRIM (3 are KEEP-FULL); correct both counts.

### SR-5 ETSI designation is wrong: "EN 304 223" -> "TS 104 223" (item 32, P2, H)

Scratch labels the ETSI AI baseline "ETSI EN 304 223 V2.1.1 (2025-12)" as a formal adopted European Standard in `ref/standards/ETSI/`, `catalogue.yml`:636, and the indexes. Upstream (verified this turn) the document is **ETSI TS 104 223 V1.1.1 (2025-04)**, a **Technical Specification** (a lower normative tier than an EN), titled "Securing Artificial Intelligence (SAI); Baseline Cyber Security Requirements for AI Models and Systems". Wrong on type, number, and version; the "cite-as-authoritative European Standard" trust framing rides on the incorrect designation. Correct across all scratch surfaces, re-assess the `standards/` vs `frameworks/` bucketing, regenerate indexes; if the held PDF genuinely reads "EN 304 223 V2.1.1", escalate as a source-integrity question. **Corpus-side coupling:** this repo's [`TODO.md`](TODO.md) §5.1 carries the same wrong "EN 304 223" designation, to be corrected when SR-5 lands.

---

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see.
- **"Inference must be validated before committing or before anything else uses that information"** — operationalised in [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — operationalised in the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — operationalised in the validation-sweep [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9.
- **Sweep history is project-application, not template content** — operationalised by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — operationalised in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) PR-finalization-protocol section.
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — operationalised in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section and the same pack rule.
- **Validate cadence is 1-8 PRs per batch, not strictly 5** — the 5-PR cadence is default; the batch boundary is chosen at the natural seam.
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)` so the two ledgers are scannable in the same shape. Harmonised in PR #163.
- **Compute-don't-ask** (maintainer-flagged 2026-06-23) — before surfacing a question, apply a "can I compute/verify this myself?" gate; surface the result, not the raw question. (Codified 2026-06-30 into the `clarify-before-acting` rule's compute-first gate, #504.)

---

## Backlog totals

Approximate active counts after the 2026-06-30 work-type re-tier and the 2026-07-02 audit intake (the priority sections themselves are the source of truth; these drift).

- **P1 (fix errors and prevent recurrence)**: 6 items (1.1 FR-48, 1.4 audit-gate candidates, 1.5 reference version-currency, plus the 2026-07-02 audit cluster: 1.6 risk-model consistency, 1.7 retention conflicts, 1.8 DSAR conflicts).
- **P2 (fill significant gaps)**: 14 items (2.1-2.10 the FR deepenings FR-59 / 60 / 70 / 99 / 15 / 23 / 63 / 74 / 154 / 41, 2.11 publications-assessment, plus the 2026-07-02 audit clusters 2.12 external-citation corrections, 2.13 cross-document contradictions, 2.14 generated-surface drift).
- **P3 (clean up and tooling)**: 9 items (3.1, 3.4, 3.6-3.8, 3.10, 3.12, plus 3.13 audit tooling extensions, 3.14 low-severity cleanup batch).
- **P4 (adopter experience)**: 6 items (4.1-4.5, plus 4.6 adopter-experience enhancements).
- **P5 (expand: country / regulator / programme overlays)**: 9 items (5.1-5.9).
- **P6 (expand: new domains)**: 5 items (6.1-6.5).
- **P7 (awaiting decision)**: 3 pending (7.1, 7.4 organisation spelling, 7.5 O'Reilly EPUBs) + 2 dropped-decision audit-trail entries (7.2 / 7.3).
- **Scratch reference-base work (`grc_library_scratch`)**: 5 items (SR-1 last_checked, SR-2 screening-record check, SR-3 validate.py binary-scan gaps, SR-4 catalogue/extract hygiene, SR-5 ETSI designation).

---

## Notes on maintenance

- Add new items at the appropriate priority; within a section keep the lowest-effort-first ordering. Move items between priorities as context changes.
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO. The P7 "dropped-decision" entries cross-reference those decisions for audit-trail completeness without duplicating the rationale.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view, kept in sync at fitness-review-cycle time.
