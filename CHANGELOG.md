# Changelog

All notable changes to this repository are recorded in this file as lead-paragraph summaries. Detailed maintainer-level entries (full Added / Changed / Removed / Fixed / Security / Verification sections per change) are kept in [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md). This is how this project's maintainer tracks the full audit trail. The convention is project-specific; forks may delete `.working/` and adopt their own approach to detailed change tracking. The mechanics are documented in the [`change-tracking` governance rule](dev-security/claude-rules/governance/change-tracking.md).

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

## 2026-06-24, Library Version 2026.06.273, PR #295

`.working/` for local project: refreshed the [`.working/hallucination-metrics.md`](.working/hallucination-metrics.md) summary table (TODO §4.9), which had been frozen at PR #176, recomputing the counts from the live catches/escapes logs; the recompute separates worker-draft errors (the defined metric, low and falling) from orchestrator-side discipline catches (the now-active multi-surface-incompleteness class) and notes that post-#275 catches live in the `/retro` and `/validate-pr` records. Closes TODO §4.9 (rotated to DONE). Carries the batched PR #294 `/validate-pr` and `/retro` records. Library `2026.06.272` to `2026.06.273`; README `1.9.143` to `1.9.144`.

## 2026-06-23, Library Version 2026.06.272, PR #294

**PR-H of the XS/S batch: a seven-item governance/registers and ESG bundle (FR-120, FR-155, FR-53, FR-109, DD-6/DD-7, FR-75, FR-76); B2 deferred on egress.** Each directional choice was confirmed with the maintainer. [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) (`1.3.2` to `1.3.3`) softens the 180-day-baseline attribution: it now states that neither NIST 800-53 CA-6 (organisation-defined frequency) nor ISO 27001:2022 Clause 9.2 ("planned intervals") prescribes a fixed interval, keeping 180 days as the library's own convention (FR-120). [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md) (`1.4.4` to `1.4.5`) corrects the stale CSA CCM v3 "GRM" governance-domain id to the v4.1 "GRC" (FR-155; the worker found only this one of the three cited files carried the drift). [`specification-ingestion.md`](specification-ingestion.md) (`1.7.3` to `1.7.4`) documents the Classification (lifecycle category) versus Confidentiality (content-sensitivity tier) distinction so the two metadata fields are non-redundant (FR-53, decided: document, not deprecate). [`governance/charter-governance-library.md`](governance/charter-governance-library.md) (`1.2.0` to `1.2.1`) tightens the dense Purpose paragraph (FR-109). [`ai/checklist-ai-algorithmic-compliance.md`](ai/checklist-ai-algorithmic-compliance.md) (`1.0.2` to `1.0.3`) and [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md) (`1.0.5` to `1.0.6`) reconcile AI-log retention up from 12 months to the canonical 7 years and add a matching AI decision-and-detection-logs row (7 years; ISO/IEC 42001 and EU AI Act Annex IV), also fixing a broken "12 months per logging standard" cross-reference; the figure and basis already existed at [`operations/procedure-security-monitoring-and-alert-management.md`](operations/procedure-security-monitoring-and-alert-management.md):298, so the three surfaces now converge (DD-6/DD-7). [`governance/guideline-esg-and-ai-ethics-disclosure.md`](governance/guideline-esg-and-ai-ethics-disclosure.md) (`1.0.0` to `1.1.0`) adds a qualitative double-materiality assessment process for the materiality threshold (FR-75), and [`governance/framework-sustainability-and-responsible-technology.md`](governance/framework-sustainability-and-responsible-technology.md) (`1.1.1` to `1.2.0`) adds qualitative ESG escalation triggers, CIO to ERC to Board (FR-76), both organisation-neutral with no invented numbers. B2 (five EDPB/WP29 soft-law citations) was deferred: verifying the titles needs web egress that is policy-blocked (403) this session, and per the no-fabrication discipline they are not added unverified. Seven items rotated TODO to DONE; B2 annotated deferred; a pre-existing ERC-expansion inconsistency surfaced during authoring was routed to TODO. Carries the batched PR #293 `/validate-pr` and `/retro` rows. Library `2026.06.271` to `2026.06.272`; README `1.9.142` to `1.9.143`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.271, PR #293

**Sweep 34 (`/validate`) close-out: correct a false "the Day-1 floor nests inside Tier 1" claim across two adopter-onboarding surfaces, and reconcile a breach-response role lead-in.** The `/resume` compensating-control corpus-wide `/validate` (Sweep 34, the standing loop-break control for the session-closing handoff PR #292, which skipped its trailing `/validate-pr` + `/retro`) ran a full three-subagent dispatch over the whole corpus plus the #289-#292 deltas. Subagents B (corpus-wide stale-reference) and C (audit-programme integrity) returned 0 findings; the security-critical FR-153 crypto and FR-90 browser-hardening citations from #291 verified clean, and a subagent WebSearch over-correction (PBKDF2-HMAC-SHA512 "210,000") was refuted at apply-time against the authoritative OWASP source (the corpus's 220,000 is correct). Subagent A surfaced one in-window defect across two parallel surfaces: [`docs/adopter-guide.md`](docs/adopter-guide.md) (`1.3.0` → `1.3.1`) and [`docs/template-quickstart.md`](docs/template-quickstart.md) (`3.0.2` → `3.0.3`) both claimed the six-artefact Day-1 floor "nests inside" / "is a subset of" the 15-document Tier 1 starter set, but two floor items ([`security/policy-acceptable-use.md`](security/policy-acceptable-use.md) and [`security/policy-identity-and-access-management.md`](security/policy-identity-and-access-management.md)) are absent from Tier 1, so the overlap is four of six. The maintainer chose to soften the prose (preserve the curated 15-document Tier 1) rather than expand Tier 1 to 17; both surfaces now state the accurate overlap and describe the three sizes as complementary. A note-level finding in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) (`1.4.12` → `1.4.13`) was reconciled in the same PR: a "two roles conduct it jointly" lead-in was in tension with a table assigning two determinations to "DPO, with Legal". Carries the Sweep 34 history row and per-iteration detail file. Library `2026.06.270` → `2026.06.271`; README `1.9.141` → `1.9.142`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail and [`.working/validate-sweeps/2026-06-23-sweep34-iter1.md`](.working/validate-sweeps/2026-06-23-sweep34-iter1.md) for the full sweep record.

## 2026-06-23, Library Version 2026.06.270, PR #292

**Session-closing handoff PR for the 2026-06-23 resume session, carrying the one PR #291 `/validate-pr` finding-fix.** [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (`1.27.31` to `1.27.32`): the BYOD policy's index-row relevance descriptor "MAM controls" is updated to "MAM and MDM controls", since PR #291 reframed the BYOD policy to cover both deployment models (the sole in-window cross-reference finding from #291's `/validate-pr`). Also carries the #291 `/validate-pr` record + history row and detail file, the #291 `/retro` row (which recorded a 2nd-occurrence redundant-re-ask degradation signal that prompted closing the session here), and the [`.working/session-handoff.md`](.working/session-handoff.md) refresh to the post-#291 state (PR-H next; Sweep 34 is the next `/resume` compensating control). Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide Sweep 34 the next `/resume` runs first. Library `2026.06.269` to `2026.06.270`; README `1.9.140` to `1.9.141`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.269, PR #291

**PR-F of the XS/S batch: a six-item security and crypto bundle (FR-153, BYOD MDM/MAM, FR-90, FR-84, FR-85, FR-86), each directional choice confirmed with the maintainer.** [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md) (`1.3.3` to `1.3.4`) updates the password-based key-derivation requirement from an unqualified "PBKDF2 or Argon2id with minimum 310,000 iterations" to Argon2id (preferred) at the OWASP minimum parameters or PBKDF2-HMAC-SHA256 at minimum 600,000 iterations (PBKDF2-HMAC-SHA512 at 220,000), per the OWASP Password Storage Cheat Sheet; the maintainer chose the SHA-256 target with the SHA-512 figure noted, resolving both the stale count and the previously unspecified HMAC hash (FR-153). [`security/policy-byod.md`](security/policy-byod.md) (`1.0.1` to `1.1.0`) is reframed from a MAM-only posture to present mobile application management (MAM) and mobile device management (MDM) as adopter-selectable deployment models: a new "BYOD deployment models" section defines each, the access-model and "what the organisation does not do" sections are scoped as model-conditional, MDM requires recorded enrolment consent, and the wipe and offboarding language now covers both selective-container and full-device wipes (maintainer-directed). [`dev-security/standard-developer-security-requirements.md`](dev-security/standard-developer-security-requirements.md) (`1.0.2` to `1.1.0`) adds browser-hardening requirements to its input-validation and output-encoding section: a Content-Security-Policy with Trusted Types, and Strict-Transport-Security with preload plus the companion content-type and frame-ancestors headers (FR-90). [`operations/procedure-patch-management.md`](operations/procedure-patch-management.md) (`1.0.1` to `1.0.2`) reformats the section 2.3 regression-testing checklist from inline bullets into a tick-through table a tester records results against (FR-84). [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) (`1.4.11` to `1.4.12`) assigns a named lead (Data Protection Officer, CISO, or DPO-with-Legal) to each of the six 24-hour initial-assessment determinations instead of diffuse joint ownership (FR-85). [`resilience/template-recovery-runbook.md`](resilience/template-recovery-runbook.md) (`1.0.2` to `1.0.3`) cross-references the [`resilience/plan-crisis-communication.md`](resilience/plan-crisis-communication.md) from its communications section so the runbook and the crisis-communication plan do not drift (FR-86). Six items rotated TODO to DONE. Also carries the batched PR #290 `/validate-pr` (0 findings) and `/retro` rows and the post-#290 handoff refresh. Library `2026.06.268` to `2026.06.269`; README `1.9.139` to `1.9.140`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.268, PR #290

**PR-E of the XS/S batch: a ten-item adopter and docs-UX bundle (FR-64, FR-65, FR-66, FR-78, FR-152, FR-69, FR-68, FR-156, FR-157, FR-158), each directional choice confirmed with the maintainer.** [`CONTRIBUTING.md`](CONTRIBUTING.md) (`1.2.0` to `1.2.1`) now tells a contributor authoring a new sector or jurisdiction overlay to mirror an exemplar annex (a privacy jurisdiction annex, or a compliance sector annex such as telecommunications or FedRAMP) instead of inventing a structure (FR-64). [`docs/adopter-guide.md`](docs/adopter-guide.md) (`1.2.0` to `1.3.0`) expands "Tracking upstream updates" to cover customised-fork merge conflicts, adopter-side audit-gate relaxation (the maintainer chose the relax-and-document posture, matching the pack's gate-discipline exception mechanism), and version-monotonicity conflicts (FR-65); adds a "Running the audit toolchain on your fork" note that the PII and secrets gates assume a neutral corpus and will trip on real adopter values, with the `DEFAULT_EXEMPT_DIRS` private-overlay mechanism as the remedy (FR-66); adds an enforcement and disciplinary-clause row to the "What to change" table (FR-156); adds shortest-binding-window guidance where multiple regulators overlap (FR-158); and cross-references the nesting of the 6 / 15 / about-25 starter-set sizes (FR-69). [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md) (`1.1.0` to `1.1.1`) drops the "audit theatre with nicer fonts" maintainer aside (FR-78). [`docs/template-quickstart.md`](docs/template-quickstart.md) (`3.0.1` to `3.0.2`) reorders "Next steps" to the portal's canonical workflow sequence with the startup roadmap set apart as the "add later" path (FR-152), expands "DPO" to "DPO (Data Protection Officer)" on the Day-1 path (FR-157), and adds the starter-set nesting note (FR-69). [`docs/decision-tree.md`](docs/decision-tree.md) (`1.0.4` to `1.0.5`) labels the about-25-document EU-fintech path as sector-conditional and nesting on the smaller sets (FR-69). [`docs/template-startup-roadmap.md`](docs/template-startup-roadmap.md) (`2.2.0` to `2.2.1`) corrects the incoherent "minus the A1 elements" wording so the skip applies to the optional A1 module, not to subtracting from the mandatory baseline (FR-68). Ten items rotated TODO to DONE. Also carries the batched PR #289 `/validate-pr` (0 findings) and `/retro` rows and the post-#289 handoff refresh. Library `2026.06.267` to `2026.06.268`; README `1.9.138` to `1.9.139`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.267, PR #289

**Sweep 33 (`/validate`) close-out: clarify a CIS-benchmark column label in the cloud-security baseline.** The `/resume` compensating-control corpus-wide `/validate` (Sweep 33, the standing control for the session-closing handoff PR #288, which skipped its trailing `/validate-pr`) ran a full three-subagent dispatch over the whole corpus plus the #282-#288 deltas. Subagents B (corpus-wide stale-reference) and C (audit-programme integrity) returned 0 findings; live counts (47 gates, 10 rules, 15 skills, 8 commands) and risk-vocabulary harmonization all verified clean against canonical sources. Subagent A (recent-PR deep review) surfaced one in-window `note`: [`operations/standard-cloud-security-configuration-baseline.md`](operations/standard-cloud-security-configuration-baseline.md) (`1.4.5` → `1.4.6`) §8's per-section mapping table (added in #287) carried the single column header "CIS Cloud Foundations area", but its §5 row maps the cloud-productivity baseline to areas governed by the separately-named CIS Cloud Productivity Foundations Benchmark v3.0 per the same section's own framework table, not the Cloud Foundations Benchmark v2.0. The header is generalized to "CIS benchmark area" and the preceding prose now names which benchmark governs each section (Cloud Foundations for §4/§6, Cloud Productivity Foundations for §5). One subagent observation (a doubled licence string) was refuted at apply-time (corpus-wide grep returned zero hits) and not routed. Carries the Sweep 33 history row and per-iteration detail file. Library `2026.06.266` → `2026.06.267`; README `1.9.137` → `1.9.138`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail and [`.working/validate-sweeps/2026-06-23-sweep33-iter1.md`](.working/validate-sweeps/2026-06-23-sweep33-iter1.md) for the full sweep record.

## 2026-06-23, Library Version 2026.06.266, PR #288

**Session-closing handoff PR for the resumed XS/S batch session, carrying the one PR #287 `/validate-pr` finding-fix.** [`compliance/procedure-capa.md`](compliance/procedure-capa.md) (`1.0.3` → `1.0.4`) §7.5 corrected from "90 business days" to "90 days" to match the cited [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md) §4.3 verbatim (the sole note-level finding from #287's `/validate-pr`). Also carries the #287 `/validate-pr` record + history row, the #287 `/retro` row (new pattern: self-authored citation over-specification), and the [`.working/session-handoff.md`](.working/session-handoff.md) refresh to the post-#287 state (PR-E next; Sweep 33 is the next `/resume` compensating control). Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide Sweep 33 the next `/resume` runs first. Library `2026.06.265` → `2026.06.266`; README `1.9.136` → `1.9.137`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.265, PR #287

**PR-C of the XS/S batch: the assurance/3LoD + audit/CAPA bundle (seven Medium fitness items), built as one PR per maintainer direction.** FR-147: [`compliance/standard-internal-audit.md`](compliance/standard-internal-audit.md) (`1.0.1` → `1.0.2`) now acknowledges the audit-planning procedure's 15-business-day final-report extension instead of stating a flat 10 days. FR-148: [`compliance/procedure-capa.md`](compliance/procedure-capa.md) (`1.0.2` → `1.0.3`) anchors the policy's 90-business-day post-implementation effectiveness validation by Internal Audit or Compliance (new §7.5). FR-101: [`risk/register-assurance-map.md`](risk/register-assurance-map.md) (`1.1.0` → `1.1.1`) makes gap-closure sign-off explicit (first-line proposes, relevant second-line confirms). FR-102: [`operations/procedure-change-management-and-configuration-control.md`](operations/procedure-change-management-and-configuration-control.md) (`1.3.0` → `1.3.1`) adds a compensating-control pathway as an alternative to deferring an untested-rollback change. FR-100: [`operations/standard-cloud-security-configuration-baseline.md`](operations/standard-cloud-security-configuration-baseline.md) (`1.4.4` → `1.4.5`) expands its ISO row to the corpus-verified A.8.9/A.8.23/A.8.24 and adds a per-section ISO/CIS/NIST mapping table (corpus-safe; no fabricated CIS recommendation numbers). FR-77: [`governance/register-key-terms-and-definitions.md`](governance/register-key-terms-and-definitions.md) (`1.1.1` → `1.1.2`) defines the Three Lines Model. FR-83: [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md) (`1.3.9` → `1.3.10`) and [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) (`1.4.10` → `1.4.11`) each gain a one-page 60-minute / 4-hour / 24-hour incident-command execution checklist (every line grounded in an existing step; the TODO gloss "independent challenge" was a mislabel for the incident-command checklist). Seven items rotated TODO → DONE; carries the batched PR #286 `/validate-pr` (0 findings) and `/retro` rows. Library `2026.06.264` → `2026.06.265`; README `1.9.135` → `1.9.136`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.264, PR #286

**Sweep 32 (`/validate`) close-out: harmonize the operational risk register to the canonical risk vocabulary and fix a self-contradicting audit-programme procedure step.** The `/resume` compensating-control corpus-wide `/validate` (Sweep 32, the standing control for the session-closing handoff PR #285 that skipped its trailing `/validate-pr`) surfaced three confirmed out-of-window `warning`-level findings (Subagent A on the recent #282-#284 corpus returned 0 findings). [`risk/template-operational-risk-register.md`](risk/template-operational-risk-register.md) (`1.0.1` → `1.0.2`) was never swept by the FR-161/162/146 risk-vocabulary harmonization: its Treatment-decision field definition listed the retired four-option set (missing the canonical Exploit / Enhance) and its Status field definition listed a non-canonical "monitoring" value; both field definitions now read the canonical sets (Avoid / Mitigate / Transfer / Accept / Exploit / Enhance; Open / Closed) per [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) Sections 6 and 7.1, matching the already-harmonized sibling templates (the maintainer chose full harmonization over a downside-only carve-out). [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) (`1.16.0` → `1.16.1`) §10 step 4 instructed updating "the gate count in §2.1", but §2.1 carries no count (it defers to §6, which the same sentence names as canonical); the stale clause is removed. Also carries the Sweep 32 history row and per-iteration detail file. Library `2026.06.263` → `2026.06.264`; README `1.9.134` → `1.9.135`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail and [`.working/validate-sweeps/2026-06-23-sweep32-iter1.md`](.working/validate-sweeps/2026-06-23-sweep32-iter1.md) for the full sweep record.

## 2026-06-23, Library Version 2026.06.263, PR #285

`.working/` for local project: **session-closing handoff PR** for the 2026-06-23 XS/S batch-reduction session. Working-state only; no adopter-facing corpus content changed. Carries the PR #284 `/validate-pr` (0 findings) and `/retro` rows, and refreshes [`.working/session-handoff.md`](.working/session-handoff.md) to the post-#284 state (library 2026.06.262; batch PRs #281-#284 merged; the remaining XS/S batch PR-C/E/F/H/I/J/K1/K2 plus the FR-144 template queued, each to be shipped with the per-directional-item ask discipline). The wind-down at four PRs was a deliberate degradation-signal response (a same-document sibling-surface miss caught by #283's `/validate-pr` and fixed in #284, plus a redundant re-ask) per the PRIMORDIAL RULE and the session-migration discipline. Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide `/validate` (Sweep 32) the next `/resume` runs first. Library `2026.06.262` to `2026.06.263`; README `1.9.133` to `1.9.134`.

## 2026-06-23, Library Version 2026.06.262, PR #284

**Complete FR-162's sample-row reconcile in the AI risk register** (closes a PR #283 `/validate-pr` in-window finding). PR #283 reconciled the AI register's Status field definition to the canonical `Open / Closed` but left five sample rows in [`ai/register-ai-risk.md`](ai/register-ai-risk.md) showing the retired `In Treatment`; those five cells now read `Open`, consistent with the field definition and with the parallel ERM-template sample rows that FR-146 fixed in #283. The miss was a same-document sibling surface (schema fixed, governed example data not) that the post-merge `/validate-pr` caught. Register `1.0.2` to `1.0.3`. Also carries the batched PR #283 `/validate-pr` (1 in-window finding, fixed here) and `/retro` rows. Library `2026.06.261` to `2026.06.262`; README `1.9.132` to `1.9.133`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.261, PR #283

**FR-161 + FR-162 + FR-163 + FR-146: align the AI and ERM-template risk vocabulary to the canonical enterprise-risk set** (PR-B of the XS/S batch). The AI risk register ([`ai/register-ai-risk.md`](ai/register-ai-risk.md)) and the AI risk-methodology annex ([`risk/annex-ai-risk-methodology.md`](risk/annex-ai-risk-methodology.md)) listed Treatment Options that omitted the canonical positive-risk options and (in the annex) used the retired "Reduce"; both now read the canonical six per [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §6: Avoid / Mitigate / Transfer / Accept / Exploit / Enhance. The AI register's Status field used the retired/conflated "Open / In Treatment / Accepted / Closed" and the ERM template's sample rows used retired "Implemented" / "Verified" / "In Progress"; both now use the canonical lifecycle Status Open / Closed (minimal reconcile per maintainer direction; the separate Treatment Status field was left unchanged where it already existed and not added where it did not). Per-doc bumps: AI risk register `1.0.1` to `1.0.2`, AI risk-methodology annex `1.0.0` to `1.0.1`, ERM template `1.1.2` to `1.1.3`. Also carries the batched PR #282 `/validate-pr` (0 findings) and `/retro` rows. Library `2026.06.260` to `2026.06.261`; README `1.9.131` to `1.9.132`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.260, PR #282

**FR-142 + FR-143: AI-procedure step accountability and a de-looped supplier escalation path** (first PR of the XS/S backlog-reduction batch). FR-142: both AI assessment procedures ([`ai/procedure-ai-model-risk-assessment.md`](ai/procedure-ai-model-risk-assessment.md), [`ai/procedure-ai-system-impact-assessment.md`](ai/procedure-ai-system-impact-assessment.md)) assigned no role to any step; each now carries a "Roles and responsibilities" subsection naming the AI Governance Lead (performs the steps), the model/system owner (supplies evidence and owns treatment items), and the AI Governance Approver / approving authority (makes the decision, escalating to the AI Governance Council for high-tier or high-risk cases). FR-143: the supplier-onboarding escalation row in [`supply-chain/procedure-supplier-onboarding-security-review.md`](supply-chain/procedure-supplier-onboarding-security-review.md) looped DPO to CISO back to the Data Protection Officer; it now terminates at the Chief Risk Officer. Also carries the batched PR #281 `/validate-pr` (0 findings) and `/retro` rows, and re-scopes FR-144 (the breach-notification individual-clock finding) to a regulator-register template deliverable per maintainer direction. Per-doc bumps: model-risk `1.0.1` to `1.0.2`, system-impact `1.0.1` to `1.0.2`, supplier-onboarding `1.0.3` to `1.0.4`. Library `2026.06.259` to `2026.06.260`; README `1.9.130` to `1.9.131`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.259, PR #281

`.working/` + TODO for local project: **Sweep 31 `/validate` close-out plus the maintainer-directed TODO restructure.** Working-state only; no adopter-facing corpus content changed. Carries: (1) the corpus-wide Sweep 31 `/validate` (the `/resume` compensating control for the session-closing handoff PR #280; full three-subagent A/B/C dispatch; mechanical baseline 47/47; 0 in-window corpus findings; clean bill), recorded as a history row plus detail file; (2) the fix for the two note-level findings the sweep surfaced, both gate-number mislabels in [`TODO.md`](TODO.md) (the [`tools/lint-citations.py`](tools/lint-citations.py) framework-citation-hallucination gate is **gate 5**, not "gate 27"; [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py) is **gate 6**); and (3) the maintainer-directed restructure of [`TODO.md`](TODO.md): the cross-cutting "Deferred decisions" and trust-recovery headings were dissolved, every item integrated into the P1 through P7 priority sections ordered lowest-effort-first, the P4 through P6 subsection detail and stable `4.N`/`5.N`/`6.N` ids kept, and two new P4 items added that were surfaced by the hallucination-tracking and retro-log review (4.9 hallucination-metrics-table refresh; 4.10 TODO/DONE rotation gate). Library `2026.06.258` to `2026.06.259`; README `1.9.129` to `1.9.130`.

## 2026-06-23, Library Version 2026.06.258, PR #280

`.working/` + TODO for local project: **session-closing handoff PR** for the 2026-06-23 DD-triage + Track-1-start session. Working-state only; no adopter-facing corpus content changed. Carries the PR #279 `/validate-pr` record + history row (one in-window finding: the DD-9 own-rotation miss) and `/retro` row (the TODO/DONE rotation miss is now two consecutive PRs, escalated to a mechanical-rotation-gate candidate), the DD-9 TODO to DONE rotation (the finding's fix), and the [`.working/session-handoff.md`](.working/session-handoff.md) refresh to the post-#279 state (all 16 of the session's open decisions triaged with dispositions in [`TODO.md`](TODO.md); next-actions queue led by the Sweep 31 `/validate` then a maintainer checkpoint per the maintainer's stop-and-assess directive). Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide `/validate` the next `/resume` runs first. Library `2026.06.257 → 2026.06.258`; README `1.9.128 → 1.9.129`.

## 2026-06-23, Library Version 2026.06.257, PR #279

**DD-9 (DR header tidy) plus the PR #278 close-out bookkeeping fixes.** A Track-1 quick-win bundled with the three in-window findings PR #278's `/validate-pr` surfaced (batched per recursion-avoidance). DD-9: [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md) (`1.3.1 → 1.3.2`) broadens the "Backup and restore requirements" header from "All Tier 1 and Tier 2 systems must have:" to "All systems must have:", since its bullets already span all four tiers after the FR-139 / Sweep-28 edits. The #278 fixes: [`TODO.md`](TODO.md) DD-1 resolution line rewritten to the new-entries-only resolution that actually shipped (it had recorded the superseded "extend to all of CHANGELOG" plan), the resolved DD-1 backlog item rotated to [`.working/DONE.md`](.working/DONE.md), and the running-order range reconciled to DD-2..DD-12; and [`.claude/CLAUDE.md`](.claude/CLAUDE.md)'s PR-workflow delta-gate enumeration updated to include D3 alongside D1 and D2. Carries the batched PR #278 `/validate-pr` record + history row and `/retro` row. Library `2026.06.256 → 2026.06.257`; README `1.9.127 → 1.9.128`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.256, PR #278

**DD-1: add PR-time delta gate D3 so new CHANGELOG entries follow the no-dash prose convention, leaving history untouched.** Deferred decision DD-1 asked whether to bring the root [`CHANGELOG.md`](CHANGELOG.md) under the em-dash and en-dash prohibition that [`tools/lint-language.py`](tools/lint-language.py) enforces on the corpus. The CHANGELOG sits outside that whole-file linter because its append-only history holds roughly 130 dashes accumulated before the convention applied, and rewriting historical entries would churn the record and risk altering past entries' meaning. The maintainer chose the new-entries-only resolution: a PR-time delta gate (D3, [`tools/check-changelog-dash-on-pr.py`](tools/check-changelog-dash-on-pr.py)) that inspects only the CHANGELOG lines a PR adds and fails on any em dash or en dash, so future entries follow the convention while history stays intact. Wired into the local PR-time runner [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh), CI ([`.github/workflows/quality.yml`](.github/workflows/quality.yml), PR-only, alongside D1 and D2), and the audit-programme spec [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) section 6.1 (`1.15.0 → 1.16.0`). The scope was re-confirmed with the maintainer at action time after investigation found roughly 130 dashes (not the approximately five the decision assumed), making a whole-file rewrite disproportionate. Also carries the batched PR #277 `/validate-pr` (0 findings) and `/retro` rows. Library `2026.06.255 → 2026.06.256`; README `1.9.126 → 1.9.127`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.255, PR #277

**Sweep 30 (`/validate`) close-out: correct five hallucinated "Cloud Controls Matrix v5" citations and broaden the citation gate.** The `/resume` compensating-control corpus-wide `/validate` (the standing control for the session-closing checkpoint handoff PR #276, which skips its trailing `/validate-pr`) surfaced one new out-of-window finding: five documents cite a nonexistent "CSA Cloud Controls Matrix **v5**" against the corpus-wide v4.1 convention. The mechanical [`lint-citations.py`](tools/lint-citations.py) gate already denies the abbreviated `CSA CCM v5` / `CCM v5` forms but missed these because they spell the standard out ("Cloud Controls Matrix v5", no `CCM` substring) — all five present since the initial public release and never caught by Sweeps 22-29 (a gate blind spot). Fixed: [`dev-security/standard-api-security.md`](dev-security/standard-api-security.md):233, [`security/standard-saas-security-posture-management.md`](security/standard-saas-security-posture-management.md):196, [`security/procedure-key-escrow-and-recovery.md`](security/procedure-key-escrow-and-recovery.md):217 (the v5 fix on this row also corrected the same cell's stale v3 domain code `EKM → CEK`, since CCM v4.1 has no `EKM` domain), [`supply-chain/procedure-supplier-audit.md`](supply-chain/procedure-supplier-audit.md):173 and [`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):160 (the last two also resolve intra-document contradictions where the body cited v4.1 but the References cited v5). The gate is broadened: [`tools/lint-citations.py`](tools/lint-citations.py) gains a `Cloud Controls Matrix v5` denylist entry (with a regression test in [`tests/test_linters.py`](tests/test_linters.py)), so gate 27 now catches both the abbreviated and the spelled-out hallucinated-version forms; the new pattern has zero corpus matches after the fixes (a forward-looking guard). Carries the batched Sweep 30 `/validate` history row + detail file and the hallucination-metrics catch (the orchestrator's apply-time grep corrected an incomplete/mis-classified subagent finding set). Per-doc bumps as listed; library `2026.06.254 → 2026.06.255`; README `1.9.125 → 1.9.126`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail and [`.working/validate-sweeps/2026-06-23-sweep30-iter1.md`](.working/validate-sweeps/2026-06-23-sweep30-iter1.md) for the full sweep record.

## 2026-06-23, Library Version 2026.06.254, PR #276

`.working/` + TODO for local project: **session-closing checkpoint handoff PR** for the 2026-06-23 FR-167 session. Working-state only; no adopter-facing corpus content changed. Carries: (1) the **PR #275 `/validate-pr`** record + history row (1 out-of-window note — the matrix legend documents only the `": "` no-mapping convention while `N/A` is now dominant; deferred to FR-167 batch 2) and the **#275 `/retro`** row; (2) acting on a **maintainer-requested review of the retro log**, the **worker-brief-template `1.0.0 → 1.1.0`** — the review found the convention/checklist layer absorbs retro candidates well but the worker-brief-template had stayed frozen at 1.0.0 despite ~6 queued additions, so this folds in the worker-side guard rails it had accrued (control-identifier verification, new-acronym-glossary, a corpus-wide-rename override, and a matrix-expansion/FR-167 override codifying the framework-code crib), each citing its source catch per the template's own self-update protocol; (3) the [`hallucination-metrics.md`](.working/hallucination-metrics.md) entry for #275's apply-time catches (worker-proposed `IPY-02`/`DSP-10` corrected to `IPY-01`/`DSP-04`); (4) [`TODO.md`](TODO.md) edits — S1 (retention-consistency gate) flagged unblocked now that FR-136/137 have landed, and a new **§4.8** consolidating the retro-log review's still-open process loops (codify the orchestrator-side bare-token-search and parallel-case-verification disciplines; codify compute-don't-ask in the clarify-before-acting rule; the P4.6 QA-cadence gate; the remaining count-gate idioms); (5) the [`.working/session-handoff.md`](.working/session-handoff.md) refresh (FR-167 batch 2 top of queue). Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide `/validate` the next `/resume` runs first. Library `2026.06.253 → 2026.06.254`; README `1.9.124 → 1.9.125`.

## 2026-06-23, Library Version 2026.06.253, PR #275

**FR-167 (batch 1 of ~11): expand the compliance alignment matrix — add the Architecture domain.** [`compliance/matrix-grc-compliance-alignment.md`](compliance/matrix-grc-compliance-alignment.md) mapped only ~42 of the library's ~280 substantive documents; FR-167 expands it to comprehensive coverage, one domain per PR. This first batch adds the **Architecture domain** (8 documents: the enterprise-architecture framework, the architecture-review procedure, and the API-design, ADR, data-architecture, integration-architecture, reference-architecture, and technology-radar standards), each mapped across all eight framework columns with honest N/A on the five customs/trade frameworks (architecture-governance content sits outside customs scope). Mappings use the corpus's established control identifiers (CSA CCM v4.1 domains including AIS/IVS/IPY/DSP/GRC/CCC/STA, ISO 27001:2022 Annex A controls and clauses, and NIST CSF families including the corpus's PR.IP convention) per the maintainer's "mirror corpus convention" decision, and every cell was verified at apply-time against the source documents (research-assistant discipline; the two research agents' candidate `IPY-02` and `DSP-10` identifiers, which are not in corpus use, were corrected to `IPY-01`/`DSP-04` at apply-time). Also softens the stale "All 42 documents" coverage summary to a count-agnostic description and clarifies the matrix's scope of intent (it is now a living, mid-expansion document). Two pre-existing matrix framework-taxonomy anomalies surfaced during the expansion (the lone non-v4.1 `NET` row; the `PR.IP`-under-CSF-2.0 convention) are routed to [`TODO.md`](TODO.md) DD-12 rather than folded into the expansion. Also carries the batched Sweep 29 `/validate` records (the `/resume` compensating control for handoff PR #274 — clean bill, two notes: one dismissed at apply-time, one routed to DD-11). Per-doc: matrix `1.0.0 → 1.1.0`. Library `2026.06.252 → 2026.06.253`; README `1.9.123 → 1.9.124`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.252, PR #274

`.working/` + TODO for local project: **session-closing handoff PR** for the 2026-06-23 FR-166 / small-items session. Working-state only; no adopter-facing corpus content changed. Refreshes [`.working/session-handoff.md`](.working/session-handoff.md) to after #273 (library 2026.06.252, 47 gates, 10 rules, 15 skills; last-merged #271 Sweep 28 DR fix, #272 FR-166, #273 count-gate P8) with the next-actions queue led by **FR-167** (steer resolved: all 8 framework columns comprehensive; use the FR-166 suggest tool + 10+ research agents) then DD-1..DD-11 triage then the smallest-items batch-reduction; rotates **FR-166** out of [`TODO.md`](TODO.md) into [`.working/DONE.md`](.working/DONE.md) (alongside DONE entries for #271 and #273) and trims the TODO Priority-1 listing-surface section to the remaining FR-167; and carries the batched PR #273 `/validate-pr` (0 findings) + `/retro` rows. Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide `/validate` the next `/resume` runs first. Library `2026.06.251 → 2026.06.252`; README `1.9.122 → 1.9.123`.

## 2026-06-23, Library Version 2026.06.251, PR #273

**Count-gate coverage: fix a stale audit count that escaped gate 39, and broaden gate 39 to catch the idiom.** PR #272's `/validate-pr` cross-reference check surfaced a pre-existing stale count in [`governance/template-library-health-report.md`](governance/template-library-health-report.md):63 ("Aggregated output of the **32** automated audits") — stale since the initial public release (the programme now has 47 gates) and never caught, because gate 39 ([`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py)) anchors all its idioms on "gate(s)" and the phrase used "automated **audits**". Two fixes: (1) the health-report template's line is re-phrased count-agnostically ("the automated audits ... §6 for the canonical gate inventory and current count"), matching the count-agnostic style every other audit-programme citer already uses (`1.0.1 → 1.0.2`); (2) gate 39 gains pattern **P8** (`<N> automated audits`), narrow by design (it requires the exact "automated audits" phrasing, not a bare "N audits" that would false-positive on audit-event counts), with a regression-test fixture and a docstring entry. After the rephrase, P8 has zero corpus matches (a purely forward-looking guard); gate 39 passes across 434 files at the canonical 47. This closes the out-of-window finding the #272 `/validate-pr` bundled here and the P4 "broaden the count gate" candidate it raised. Carries the batched PR #272 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.250 → 2026.06.251`; README `1.9.121 → 1.9.122`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.250, PR #272

**FR-166: corpus listing-surface completeness gate + authoring-time sweep tool.** Governance work must be meticulous, so when a new document is added, every surface that should list it must be updated. This PR adds the mechanism. The new **gate 47** ([`tools/lint-listing-surface-completeness.py`](tools/lint-listing-surface-completeness.py)) enforces completeness for the MECHANICAL listing surfaces against the canonical active-document set in [`taxonomy.yml`](taxonomy.yml): the document-index register ([`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) must list every domain-prefixed active document, and each domain README must reference every active document in its own domain. Root-level meta-specifications (`specification-*.md`) are exempt by a documented rule (the register is organized by domain and has never indexed them). The new authoring helper [`tools/suggest-listing-surfaces.py`](tools/suggest-listing-surfaces.py) `<doc>` reports, for a new document, the MECHANICAL surfaces (present/missing) plus a ranked high-recall list of SEMANTIC candidates (the framework matrices and crosswalks, the glossary, the Related Documents field) for a human to ratify. Honest contract per `gate-discipline`: MECHANICAL surfaces are hard-gated; the relevance-based SEMANTIC surfaces are NOT gated (a noisy completeness gate over a judgment-based surface would erode gate-discipline), they get suggestions and a `/validate` Subagent B coverage-drift check instead. Wired across all four audit-programme surfaces (workflow, runner, pre-commit, spec §6) with a regression fixture; the gate count moves 46 → 47. The corpus is already complete (the gate passes at HEAD); the only register gap measured (the two root meta-specs) is the documented exemption. Also wires the helper into the new-document procedure ([`specification-ingestion.md`](specification-ingestion.md) checklist item 12) and adds the SEMANTIC coverage-drift check to the [`validation-sweep`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) SKILL's Subagent B scope. Carries the batched PR #271 `/validate-pr` (0 findings) + `/retro` rows. Per-doc: audit-programme spec `1.14.2 → 1.15.0`, ingestion spec `1.7.2 → 1.7.3`; pack `1.49.2 → 1.49.3`; library `2026.06.249 → 2026.06.250`; README `1.9.120 → 1.9.121`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.249, PR #271

**Sweep 28 (`/validate`) close-out: fix an in-window DR backup-cadence contradiction surfaced by the session-resume sweep.** The `/resume` compensating-control corpus-wide `/validate` (the standing control for the session-closing handoff PR #270, which skips its trailing `/validate-pr`) ran a full three-subagent dispatch over the whole corpus + the #259-#270 window. Mechanical baseline clean (46/46); all FR-134..141 overnight fixes confirmed internally and cross-document coherent. It surfaced **one in-window defect**: [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md):97 prescribed only "at least daily backups for Tier 2 and lower tiers", but the same document binds Tier 2 to a 4-hour backup gap (:99) matching its 4-hour RPO (:50), and treats any gap exceeding the RPO as a permanent P2 risk event (:101) — so a compliant Tier-2 system on daily backups would sit permanently in P2 escalation, the exact failure mode PR #265/FR-139 was written to eliminate for Tier 1, reproduced one tier down. FR-139 fixed Tier 1's cadence but, in rewriting the gap clause to bind Tier 2 explicitly to 4 hours, left Tier 2 on the old "daily" cadence. Fixed here: the cadence clause now reads "backups at least every 4 hours for Tier 2's 4-hour RPO, and at least daily backups for Tier 3 and Tier 4" — consistent with the gap clause, the RTO/RPO targets table, and the locked FR-139 principle (cadence must meet RPO), so no new authorial decision (the binding 4-hour gap requirement was already present at :99); per-doc version `1.3.0 → 1.3.1`. Out-of-window observations all dedupe against existing deferred decisions (CPPA-as-live → DD-8; TLS-1.2 floor → DD-4/DD-5; impact-5 label → DD-3; DR header scope → DD-9) except one new one (the operational-risk-register's distinct "Moderate" likelihood/rating scale) routed to **DD-11**. Also records the maintainer's running-order directive for the session in [`TODO.md`](TODO.md) (FR-166/167 → DD triage → batch-reduce the smallest backlog items with 10+ research-assistant agents). Library `2026.06.248 → 2026.06.249`; README `1.9.119 → 1.9.120`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail and [`.working/validate-sweeps/2026-06-23-sweep28-iter1.md`](.working/validate-sweeps/2026-06-23-sweep28-iter1.md) for the full sweep record.

## 2026-06-23, Library Version 2026.06.248, PR #270

`.working/` + TODO for local project: **session-closing handoff PR** for the 2026-06-23 resume + wind-down session. Working-state only; no adopter-facing corpus content changed. Lands: (1) **Sweep 27** — a maintainer-directed final pre-resume corpus-wide `/validate` (full three-subagent dispatch; the overnight run's clean in-window bill holds, PR #269's docstring fix verified, all gates/counts/citations current; one in-window note fixed — [`.working/overnight-pr.md`](.working/overnight-pr.md) stub "11 deferred" → "9" — and one out-of-scope observation routed to DD-10), recorded in [`.working/validate-sweeps/2026-06-23-sweep27-iter1.md`](.working/validate-sweeps/2026-06-23-sweep27-iter1.md); (2) the **overnight-pr.md morning processing** (resolved decisions already in [`.working/design-decisions.md`](.working/design-decisions.md); the 9 deferred "Open ambiguities" routed to [`TODO.md`](TODO.md) as the DD-1..DD-9 block; file reset to `stub`); (3) the **alignment-matrix completeness decision** — [`compliance/matrix-grc-compliance-alignment.md`](compliance/matrix-grc-compliance-alignment.md) maps only 42 of 341 documents, so the maintainer chose to expand it to comprehensive + clarify its intent wording and to build a corpus listing-surface completeness gate + authoring sweep tool, queued as **FR-166/FR-167** (top priority next session); (4) the carried PR #269 `/validate-pr` (clean) + `/retro` rows (the `/retro` records a maintainer-flagged "compute-don't-ask" discipline lesson); (5) the [`.working/session-handoff.md`](.working/session-handoff.md) refresh. Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide `/validate` the next `/resume` runs first. Library `2026.06.247 → 2026.06.248`; README `1.9.118 → 1.9.119`.

## 2026-06-23, Library Version 2026.06.247, PR #269

Tooling + `.working/` for local project: cleanup PR after the session-resume corpus-wide `/validate` (Sweep 26, the compensating control for handoff PR #268). Corrected a stale docstring in [`tools/lint-collection-enumeration-consistency.py`](tools/lint-collection-enumeration-consistency.py) ("three hard-coded collections" → "two", matching the two-entry `COLLECTIONS` tuple, the runtime "2 collection(s)" output, and the [`specification-audit-programme.md`](governance/specification-audit-programme.md) §6 inventory; the external-overlay collection was described but never wired). Sweep 26 found **zero in-window regressions** across the overnight run (PRs #259-#268, FR-134..141 + Sweep 25) and two confirmed pre-existing out-of-window findings — the docstring (fixed here) and a CPPA-as-live framework row in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md):255 (folded into the deferred broader-CPPA sweep, not fixed piecemeal) — plus one refuted false positive ([`compliance/matrix-grc-compliance-alignment.md`](compliance/matrix-grc-compliance-alignment.md):151 "All 42 documents" is correct: 42 unique documents, 43 rows because one document is dual-domain-mapped). Carries the [`.working/validate-sweeps/2026-06-23-sweep26-iter1.md`](.working/validate-sweeps/2026-06-23-sweep26-iter1.md) record + history row. Library `2026.06.246 → 2026.06.247`; README `1.9.117 → 1.9.118`.

## 2026-06-23, Library Version 2026.06.246, PR #268

`.working/` changes for local project: session-closing handoff PR for the maintainer-authorized autonomous overnight run. Refreshes [`.working/session-handoff.md`](.working/session-handoff.md) (state snapshot after #268, last-merged #259-#268, trust-recovery + criticals COMPLETE, next-actions = maintainer review of the deferred-decision items then the remaining P1 Highs FR-140/142/143/144/145) and [`.working/overnight-pr.md`](.working/overnight-pr.md) (build progress + RUN-PAUSED note: the run completed the six H[critical] criticals FR-134..139, the corpus-wide Sweep 25, and FR-141, then paused before the judgment-heavier Batch B1 Highs on a quality-first / degradation basis). Carries the batched PR #267 `/validate-pr` (0 in-window) + `/retro` rows. Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), this PR skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide `/validate` the next `/resume` runs first. No corpus content changed. Library `2026.06.245 → 2026.06.246`; README `1.9.116 → 1.9.117`.

## 2026-06-23, Library Version 2026.06.245, PR #267

**FR-141 (High): remove the invented PIPEDA breach "72-hour target".** Canada's federal `PIPEDA` Breach of Security Safeguards Regulations require reporting to the OPC "as soon as feasible after the organization determines that the breach has occurred" — there is no fixed statutory hour clock, so the "(72-hour target)" annotation was a fabricated deadline (the 72-hour figure is GDPR's, and Quebec Law 25's to the CAI — neither is the PIPEDA federal rule). A bare-token search found the invented annotation at two surfaces (not just the one named in the finding): [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md):171 (`1.4.9 → 1.4.10`; §6.2 jurisdiction table, "Without unreasonable delay (72-hour target)") and [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md):176 (`1.3.8 → 1.3.9`; §6 regulatory-notification table, "As soon as feasible (72-hour target)"). Both deadline cells now read "As soon as feasible (no fixed statutory deadline)". The correct 72-hour references elsewhere (GDPR threshold in [`risk/template-risk-appetite-statement.md`](risk/template-risk-appetite-statement.md), Quebec Law 25 to the CAI, Malaysia's PDPC rule) were verified accurate and left unchanged. That §176 cell's separate "CPPA (Canada)" regime label (an FR-138 CPPA-not-in-force issue) is left for the deferred broader-CPPA sweep (logged in [`.working/overnight-pr.md`](.working/overnight-pr.md)); only the FR-141 deadline was changed here. Carries the batched PR #266 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.244 → 2026.06.245`; README `1.9.115 → 1.9.116`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.244, PR #266

**Sweep 25 (`/validate`) close-out: four Low consistency fixes after the H[critical] criticals batch.** The Batch-A-seam corpus-wide validation sweep (three subagents over the FR-134..139 window + the whole corpus) confirmed the six locked-value fixes are internally and cross-document coherent (zero new cross-PR inconsistencies) and surfaced four Low findings, all fixed here: (1) [`dev-security/claude-rules/skills/guardrail-review/SKILL.md`](dev-security/claude-rules/skills/guardrail-review/SKILL.md):93 growth-narrative "grew from five rules to nine" corrected to "ten" (the 10th rule, [`project-integrity.md`](dev-security/claude-rules/governance/project-integrity.md), landed in PR #258 but this free-prose count is invisible to the gate-41 enumeration check); (2) [`TODO.md`](TODO.md):182 "the nine `governance/` pack rules" corrected to "ten" (same #258 free-prose miss); (3) [`privacy/template-record-of-processing-activities.md`](privacy/template-record-of-processing-activities.md):46 lawful-basis example "CPPA Sec 12 consent" — the lone unmarked live-CPPA-section citation in the corpus — re-grounded on the in-force PIPEDA Schedule 1 Principle 3 (consent) with "CPPA Sec 12 ... proposed, not in force" (extends the FR-138 scrub to this surface); (4) [`security/policy-identity-and-access-management.md`](security/policy-identity-and-access-management.md):75 privileged-access session retention "minimum of one year" now defers to the authoritative [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md) (2 years), resolving an under-floor against the FR-136 canonical. Findings 1-2 are in-window #258 misses; 3-4 are pre-existing surfaces whose fix direction is determined by the locked FR-138/FR-136 decisions + the stricter-is-safer rule (no new authorial decision). All 9 pre-flight scanner candidates confirmed false positives. Per-doc versions: ROPA template `1.0.4 → 1.0.5`, IAM policy `1.3.0 → 1.3.1`, pack `1.49.1 → 1.49.2`. A recurring pattern (3rd occurrence) is noted in the sweep record: new-rule additions miss free-prose rule counts that gate 41 does not parse — candidate for a broadened gate / close-out-checklist line. Carries the batched PR #265 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.243 → 2026.06.244`; README `1.9.114 → 1.9.115`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail and [`.working/validate-sweeps/2026-06-23-sweep25-iter1.md`](.working/validate-sweeps/2026-06-23-sweep25-iter1.md) for the full sweep record.

## 2026-06-23, Library Version 2026.06.243, PR #265

**FR-139 (H[critical]): DR Tier-1 backup cadence aligned to the 1-hour RPO.** [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md) set a 1-hour RPO for Tier 1 (Mission Critical) in its RTO/RPO targets table, but the backup section mandated "automated daily backups" and a "backup gap not exceeding 24 hours for Tier 1" — both incompatible with a 1-hour RPO. Combined with the rule that "any backup gap exceeding the defined RPO is treated as a P2 risk event", a compliant Tier-1 system would *permanently* sit in P2 escalation, a self-contradiction. Per the maintainer's locked decision (1h RPO binding; the 24h figure is the error and belongs to lower tiers), the backup cadence now requires continuous or near-continuous data protection (journaled/snapshot replication or log shipping) for Tier 1's 1-hour RPO with at least daily backups for Tier 2 and below, and the backup-gap limit is stated per tier (1 hour Tier 1, 4 hours Tier 2; 24h/72h for Tier 3/Tier 4 per the targets table). Per-doc version `1.2.0 → 1.3.0` (minor; the Tier-1 backup-cadence requirement changed substantively). A bare-token search confirms the DR plan is now internally consistent and that [`operations/standard-production-security-requirements.md`](operations/standard-production-security-requirements.md):43 ("RPO 1 hour, RTO 4 hours") corroborates rather than diverges. **This completes the six-item H[critical] locked-criticals batch (FR-134 through FR-139).** Carries the batched PR #264 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.242 → 2026.06.243`; README `1.9.113 → 1.9.114`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.242, PR #264

**FR-138 (H[critical]): scrub CPPA-as-live from the three named privacy documents.** The Consumer Privacy Protection Act (CPPA, Part 1 of Bill C-27) lapsed at the 2025-01-06 prorogation and is not in force ([`privacy/jurisdictions/annex-privacy-canada.md`](privacy/jurisdictions/annex-privacy-canada.md):28 is the canonical statement; PIPEDA remains the federal private-sector law), yet three documents cited CPPA as a live legal basis — with invented-looking section numbers ("CPPA s.63", "s.66", "s.69", "s.67", "s.63(3)") presented as current obligations. Per the maintainer's locked decision, those are replaced with the in-force PIPEDA Schedule 1 basis (the CSA Model Code fair-information principles), with a "CPPA pending reintroduction" note where relevant. [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md) (`1.4.1 → 1.5.0`): the rights table and the summary mapping table now cite PIPEDA Schedule 1 Principle 9 (Individual Access) for access/correction and Principle 3 (Consent, withdrawal) for objection; the erasure and automated-decision rows drop the CPPA citation because PIPEDA provides no such right (GDPR remains the basis); a new "Canadian legal basis" note explains this and that CPPA, if reintroduced, would add disposal and automated-decision rights; the intro, the §4 alignment line, the fees-table row, and the §8.3 heading are de-CPPA'd. [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) (`1.4.8 → 1.4.9`): the Canada federal breach basis becomes PIPEDA (Breach of Security Safeguards Regulations) with "CPPA pending reintroduction"; the alignment line and the §notification-basis row aligned. [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md) (`1.4.3 → 1.4.4`): the data-steward list, the rights bullet, and two control-mapping cells aligned to PIPEDA (Principle 1 Accountability, Principle 9 Individual Access). The PIPEDA Schedule 1 principle numbering is grounded in the corpus's own usage ([`privacy/template-privacy-notice.md`](privacy/template-privacy-notice.md):158 uses "Principle 8 = Openness"). **Deferred to a follow-up sweep** (not in the locked-named scope): the broader CPPA-as-live mentions in [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md), the document-index framework tags, matrices, and other privacy templates (logged in [`.working/overnight-pr.md`](.working/overnight-pr.md)). Carries the batched PR #263 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.241 → 2026.06.242`; README `1.9.112 → 1.9.113`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.241, PR #263

**FR-137 (H[critical]): DSAR-record retention harmonized to 3 years.** Three documents disagreed on how long Data Subject Access Request records are kept: the authoritative [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md):74 says "3 years" (GDPR Article 30), while [`governance/standard-records-retention-and-destruction.md`](governance/standard-records-retention-and-destruction.md):79 said "2 years post-closure" and [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md) §9.2 said "2 years following the closure date". Per the maintainer's locked decision (3 years canonical), the records standard's DSR row and the privacy procedure §9.2 (plus its parenthetical) are aligned to **3 years post-closure**, both now citing the register as authoritative. The register was already canonical and is unchanged. Per-doc versions: records `1.4.2 → 1.4.3`, privacy procedure `1.4.0 → 1.4.1`. A bare-token search confirms no other DSR-retention surface still says 2 years. Carries the batched PR #262 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.240 → 2026.06.241`; README `1.9.111 → 1.9.112`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.240, PR #262

**FR-136 (H[critical]): the data-retention schedule is authoritative for log retention.** The logging standard flatly required "a minimum of seven years" for security and audit logs ([`security/standard-logging-and-monitoring.md`](security/standard-logging-and-monitoring.md):92), while the authoritative [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md) tiers retention by log class (access logs 1 year, privileged-access session logs 2 years, SIEM events 1 year hot + 2 years cold, security incident records 5 years) and the records standard's IT/Security row said "1 to 3 years" — three different answers for the same logs. Per the maintainer's locked decision, the schedule is authoritative: logging-standard §4.1 now defers to the schedule's tiered periods (retaining the BASC/legal-mandate longer-retention clause), and the records standard's IT/Security row ([`governance/standard-records-retention-and-destruction.md`](governance/standard-records-retention-and-destruction.md):77) now cites the schedule (tiered; 1 to 5 years). Per-doc versions: logging `1.4.1 → 1.4.2`, records `1.4.1 → 1.4.2`. **Downstream reconciliation**: [`operations/procedure-security-monitoring-and-alert-management.md`](operations/procedure-security-monitoring-and-alert-management.md):298 cited "§4.1" for a 7-year AI-decision-log retention; since §4.1 no longer states a flat 7 years, that citation is re-grounded on the established ISO/IEC 42001 + EU AI Act Annex IV AI-audit-log basis (the same basis used in [`supply-chain/procedure-third-party-ai-due-diligence.md`](supply-chain/procedure-third-party-ai-due-diligence.md)), **preserving** its 7-year retention (no reduction) and noting it is a longer tier than the general SIEM events (`1.3.1 → 1.3.2`). **Correction to PR #261**: that PR's verification statement ("a corpus-wide contradiction search confirms no org surface still permits TLS 1.2") was over-broad — it rested on a contradiction-search regex tuned to the migrated phrasings, which did not match other permissive constructions. The #261 `/validate-pr` (run after merge) surfaced two additional permissive-1.2 surfaces ([`operations/procedure-media-handling-and-transport.md`](operations/procedure-media-handling-and-transport.md):124, a governed documented-technical-constraint exception; [`supply-chain/template-supplier-security-questionnaire.md`](supply-chain/template-supplier-security-questionnaire.md):87, a vendor minimum-bar question), both deferred to maintainer review; FR-135's named surfaces remain correctly migrated. Carries the batched PR #261 `/validate-pr` (1 High in-window, this correction) + `/retro` rows. Library `2026.06.239 → 2026.06.240`; README `1.9.110 → 1.9.111`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.239, PR #261

**FR-135 (H[critical]): TLS 1.3 everywhere.** The authoritative encryption policy ([`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md):54) and the developer-security standard mandate TLS 1.3 and prohibit 1.2, but several surfaces still permitted "TLS 1.2 (minimum)" or "TLS 1.2+", so the corpus contradicted itself on the TLS floor. Per the maintainer's locked decision ("TLS 1.3 everywhere"), every org TLS-floor surface is migrated to **TLS 1.3 (or stronger)** with TLS 1.2 moved to the prohibited set, following the canonical pattern FR-81 established: [`dev-security/standard-security-quick-reference.md`](dev-security/standard-security-quick-reference.md) (`1.1.2 → 1.1.3`; the crypto-do/don't row, the four data-classification rows, and the transit-crypto row), [`dev-security/standard-security-baseline-and-standards-reference.md`](dev-security/standard-security-baseline-and-standards-reference.md) (`1.1.0 → 1.1.1`), [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) (`1.1.1 → 1.1.2`), [`operations/standard-production-security-requirements.md`](operations/standard-production-security-requirements.md) (`1.1.3 → 1.1.4`; the B2B/EDI HTTP/SOAP adapter, unconditionally — no partner exception), [`compliance/healthcare/annex-healthcare-sector-requirements.md`](compliance/healthcare/annex-healthcare-sector-requirements.md) (`1.1.0 → 1.1.1`; the HIPAA transmission-security control), and the pack rules [`dev-security/claude-rules/core/cryptography.md`](dev-security/claude-rules/core/cryptography.md) + [`dev-security/claude-rules/ai/mcp-security.md`](dev-security/claude-rules/ai/mcp-security.md) (pack `1.49.0 → 1.49.1`). A corpus-wide contradiction search confirms no org surface still permits TLS 1.2. **Two surfaces deferred to maintainer review** (not force-migrated, on quality grounds): [`dev-security/claude-rules/core/owasp.md`](dev-security/claude-rules/core/owasp.md) (represents OWASP ASVS, which permits TLS 1.2 at baseline — migrating would misstate the external standard) and [`dev-security/claude-rules/languages/go.md`](dev-security/claude-rules/languages/go.md) (the TLS code example needs a coherent rewrite, since Go ignores the explicit 1.2 cipher-suite list under a 1.3 minimum). Carries the batched PR #260 `/validate-pr` (0 in-window) + `/retro` rows. Library `2026.06.238 → 2026.06.239`; README `1.9.109 → 1.9.110`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.238, PR #260

**FR-134 (H[critical]): one canonical risk-scoring scale across the three risk documents.** The risk standard's §5.2 scoring scale diverged from the canonical risk-assessment procedure: the standard used likelihood labels Rare→Almost Certain and score-to-rating bands `1-5 / 6-10 / 11-15 / 16-25`, while [`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md) (the canonical methodology, per maintainer decision) uses Very Low→Very High and bands `1-4 / 5-9 / 10-16 / 17-25`, so the same risk score produced a different rating, review cadence, and escalation depending on which document an assessor read (e.g. a score of 16 was "Critical" under the standard but "High" under the procedure). [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §5.2 is realigned to the canonical scale (likelihood labels Very Low→Very High; bands `1-4 / 5-9 / 10-16 / 17-25` with ratings Low/Medium/High/Critical), with a new sentence citing the procedure and template as sharing the one scale; the §8.1 monitoring-cadence bands and the §9.1 evidence-table cadence phrase (both stated as "taken verbatim from §5.2") are rebanded to match, and the "Moderate" rating label is corrected to "Medium" throughout. [`risk/template-enterprise-risk-register.md`](risk/template-enterprise-risk-register.md) (whose bands already agreed and which already cited the procedure) has its stale likelihood labels fixed: the Inherent/Residual Likelihood fields and the 5×5 matrix axis move from Rare→Almost Certain to Very Low→Very High. Per-document versions: standard `1.6.0 → 1.7.0`, template `1.1.1 → 1.1.2`. Carries the batched PR #259 `/validate-pr` (0 in-window) + `/retro` rows. Two related observations surfaced and deferred to maintainer review (not folded into this scoped fix): a fourth surface ([`supply-chain/register-concentration-risk.md`](supply-chain/register-concentration-risk.md) descriptive likelihood scale) and the impact-5 label divergence (Catastrophic vs Critical). Library `2026.06.237 → 2026.06.238`; README `1.9.108 → 1.9.109`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.237, PR #259

`.working/` + `.claude/` changes for local project: initiates a maintainer-authorized autonomous overnight run through the Priority 1 / Priority 2 (then P3/P4) backlog. Transitions [`.working/overnight-pr.md`](.working/overnight-pr.md) from `stub` to `in-flight` with the authorization scope, the eight design decisions resolved with the maintainer before sleep, and the PR plan-of-record; records the same eight authorizations in [`.working/design-decisions.md`](.working/design-decisions.md); carries the batched PR #258 `/validate-pr` (0 findings) + `/retro` rows. No corpus content changed in this PR. Library `2026.06.236 → 2026.06.237`; README `1.9.107 → 1.9.108`.

## 2026-06-23, Library Version 2026.06.236, PR #258

**Distributes the PRIMORDIAL RULE as the tenth pack governance rule [`project-integrity.md`](dev-security/claude-rules/governance/project-integrity.md)** (pack `1.48.0 → 1.49.0`; closes TODO P4.0). The project's apex `## PRIMORDIAL RULE: PROJECT INTEGRITY` section of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) is generalized into a project-agnostic pack governance rule so adopters inherit the lexicographic **Quality > Speed > Cost** ordering and the integrity non-negotiables rather than re-deriving them under pressure. The rule governs a different axis than the other nine: where each of those constrains a specific behaviour, this one fixes the priority ordering that decides which optimization dimension wins when quality, speed, and cost conflict (quality always, then speed, then cost, lexicographically). It re-states the integrity non-negotiables (correctness over apparent completion; no stub/mock/fabrication; no gate suppression; no silent changes; failing states surfaced) as the apex-precedence forms of `gate-discipline`, `evidence-grounded-completion`, and `clarify-before-acting`, and prescribes the self-reminder checkpoint cadence (task start, before persistence, before completion claims, at tension points). Wired across every surface a new governance rule touches: the pack rule file + its [`.claude/rules/governance/project-integrity.md`](.claude/rules/governance/project-integrity.md) byte-identical mirror (gate 37) with the [`tools/lint-claude-rules-sync.py`](tools/lint-claude-rules-sync.py) MIRROR_MAP entry; all three enumeration surfaces (the pack README directory-tree AND its "two areas" prose list, the pack [`CLAUDE.md`](dev-security/claude-rules/CLAUDE.md), the project [`.claude/CLAUDE.md`](.claude/CLAUDE.md); gate 41); the rollout-history narrative in both CLAUDE.md files extended to name the tenth rule; the [`tools/lint-collection-enumeration-consistency.py`](tools/lint-collection-enumeration-consistency.py) docstring "nine" → "ten" governance rules; and the project CLAUDE.md PRIMORDIAL RULE forward-reference ("queued as TODO P4.0") now resolved to the shipped rule. Carries the batched PR #257 `/validate-pr` (0 findings) + `/retro` rows. Pack `1.48.0 → 1.49.0`; library `2026.06.235 → 2026.06.236`; README `1.9.106 → 1.9.107`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.235, PR #257

**Adds the fifteenth pack skill [`guardrail-review`](dev-security/claude-rules/skills/guardrail-review/SKILL.md) (`/guardrails`)** (pack `1.47.3 → 1.48.0`). The periodic structural-integrity review of the governance machinery itself: the rules, skills, and audit gates, plus their wiring surfaces, reviewed through three lenses the mechanical parity gates cannot apply because they check identity and count, not meaning. **Overlap**: two rules/skills/gates covering the same ground redundantly or contradictorily. **Gap**: a stated discipline no gate enforces, a recurring failure mode (in [`improvement-log.md`](.working/improvement-log.md) / [`hallucination-metrics.md`](.working/hallucination-metrics.md)) no rule names, a rule with no warranted skill, a gate covering one surface while a sibling is ungated. **Drift**: a rule/skill/gate whose meaning diverged across wiring surfaces below the parity gates' resolution (the recurring real instance being a convention revised in a rule but left stale in a one-line enumeration description, which the resume `/validate` of 2026-06-23 caught in the pack README). It is distinct from the content sweeps (`/validate`, `/validate-pr`, which review the corpus) and the trust-recovery suite (`/full-qa`, `/fitness`, which re-examine a window of work): `/guardrails` reviews the apparatus, not the corpus. Cadence: maintainer-triggered plus an auto-prompt after any PR that adds, removes, or renames a rule, skill, or gate. It is a single-pass periodic review (like `/fitness`), not a fix-to-fixed-point loop, because structural findings are maintainer-decision proposals (merge overlapping rules, add a gate, retire a decorative check, reconcile a drifted description), routed tagged `[guardrails]`, tiered by severity, none dropped. Wired across every surface a new skill touches: the SKILL (`derives_from` [`gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md)), the [`/guardrails`](.claude/commands/guardrails.md) slash command with step-identifier parity (steps 1-6, gate 44), the [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py) PAIRS registry, the pack README skills tree (14 to 15 skills, gate 41), bidirectional `## See Also` back-references in `skill-authoring-discipline` and `deep-qa-review`, and a `.working/guardrail-reviews/` record-directory scaffold. Closes the TODO structural-review codification item. Carries the batched PR #256 `/validate-pr` (0 findings) + `/retro` rows. Pack `1.47.3 → 1.48.0`; library `2026.06.234 → 2026.06.235`; README `1.9.105 → 1.9.106`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.234, PR #256

**Resume `/validate` close-out: pack README staleness from the trust-recovery work** (pack `1.47.2 → 1.47.3`). The corpus-wide `/validate` that `/resume` runs first (the compensating control for the session-closing handoff PR's skipped trailing sweep) surfaced three residual prose defects in [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) that the multi-surface trust-recovery edits (PR #246's ninth-rule addition, PR #252's routing revision) touched this file but missed: (1) the "two areas" governance-rule enumeration listed eight rules and omitted the ninth ([`trust-recovery-escalation.md`](dev-security/claude-rules/governance/trust-recovery-escalation.md)); (2) the directory-tree one-line description of that rule and (3) of [`deep-qa-review/SKILL.md`](dev-security/claude-rules/skills/deep-qa-review/SKILL.md) both still carried the superseded "every finding to backlog top" single-tier routing phrasing. All three are harmonized to the current state (nine rules; severity-tiered routing). A corpus-wide grep confirmed these were the only live-corpus residues of the old phrasing (version-history rows and append-only CHANGELOG narrative are accurate-to-time and left intact). The sweep's three subagents otherwise returned clean (Subagent C, audit-programme integrity: zero findings). Both pre-flight scanner candidates ("a suite of two skills") were confirmed false positives. Carries the resume `/validate` history row. Pack `1.47.2 → 1.47.3`; library `2026.06.233 → 2026.06.234`; README `1.9.104 → 1.9.105`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.233, PR #255

**Session-closing handoff PR: resume-hardening guardrails + handoff refresh.** The maintainer-endorsed quality-first refresh before the next session's higher-multi-surface-wiring builds (the `/guardrails` skill and the `project-integrity` pack rule), landing the guardrails this session's experience surfaced so the next `/resume` does not repeat the same issue-types. The [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR close-out checklist gains two items: a **`lint-language` pre-flight on new pack prose** (em-dashes and British `-ise` are recurrently reintroduced in new SKILL/rule/command drafts) and a **grep-after-wiring** item (after a convention/count/routing/gate-wiring change restated across surfaces, grep the old phrasing across the full file plus every sibling surface, zero hits before commit; this would have pre-empted PR #252's multi-surface-incompleteness defect). The [`/resume`](.claude/commands/resume.md) command now reads [`.working/third-party-issues.md`](.working/third-party-issues.md) and notes the stop-hook auto-persist behaviour. [`.working/session-handoff.md`](.working/session-handoff.md) is refreshed to the after-#255 snapshot with a new "Known environment behaviours" section (stop-hook auto-commit/push, commit-signing-server 503, shallow-clone) and the next-session queue (full `/validate` then `/guardrails` then P4.0 then criticals). Carries the batched PR #254 `/validate-pr` (0 findings) + `/retro` rows. As the session-closing handoff PR it runs no trailing `/validate-pr`/`/retro` (loop-break, PR-workflow step 5a); the compensating control is the next `/resume`'s full corpus `/validate`. Working-state and config change; the only gated file touched is [`README.md`](README.md) (version lines). Library `2026.06.232 → 2026.06.233`; README `1.9.103 → 1.9.104`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-23, Library Version 2026.06.232, PR #254

**Adds the `/trust-recovery` convenience wrapper** (maintainer-approved). A thin slash command at [`.claude/commands/trust-recovery.md`](.claude/commands/trust-recovery.md) that runs the trust-recovery escalation suite in order: the full-clone check (step 0), then [`/full-qa`](.claude/commands/full-qa.md) (the AI-failure-pattern forensic pass), then [`/fitness`](.claude/commands/fitness.md) (the fresh-reader persona pass), then holds for maintainer sign-off. It sequences the two existing skills (which hold the authoritative step detail) and routes findings per the severity-tiered convention; it does not replace either skill and does not self-authorize. Like [`/resume`](.claude/commands/resume.md), it is a thin non-paired command (no SKILL counterpart, not in the gate-44 PAIRS registry). A discoverability mention was added to the trust-recovery rule bullet in [`.claude/CLAUDE.md`](.claude/CLAUDE.md). Carries the deferred PR #253 `/validate-pr` (0 findings) + `/retro` rows. Working-state and config change; the only gated file touched is [`README.md`](README.md) (version lines). Library `2026.06.231 → 2026.06.232`; README `1.9.102 → 1.9.103`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.231, PR #253

**Completes the trust-recovery routing-convention revision + signing-outage note** (pack `1.47.1 → 1.47.2`). PR #252's severity-tiered routing revision was incomplete: it updated [`deep-qa-review`](dev-security/claude-rules/skills/deep-qa-review/SKILL.md) §4 (heading, body) and frontmatter but left two same-file spots asserting the superseded single-top-priority-tier routing: the Verification completion criterion and a Common-Rationalizations cell. PR #252's `/validate-pr` Subagent A caught both in-window (a multi-surface-incompleteness defect introduced by omission); a corpus-wide grep confirmed they were the only two missed spots. Both are harmonized here to the severity-tiered convention (generic project-agnostic tier wording). Per the maintainer's request, also adds [`.working/third-party-issues.md`](.working/third-party-issues.md), a running log of execution-environment / third-party-service issues, with a first entry documenting the **commit-signing-server 503 outage** encountered during PR #252 (the symptom: gate 36's regression fixtures could not `git commit`, and a commit was left unsigned; the diagnosis: an environment artifact, distinguished from a real defect because gates 31/40 passed on the real corpus; the resolution: the server recovered and the commit was re-signed). Carries the PR #252 `/validate-pr` (2 findings, fixed here) + `/retro` rows per recursion-avoidance. Working-state and pack change; the gated files touched are [`dev-security/claude-rules/skills/deep-qa-review/SKILL.md`](dev-security/claude-rules/skills/deep-qa-review/SKILL.md), [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) (pack version), and [`README.md`](README.md) (versions). Pack `1.47.1 → 1.47.2`; library `2026.06.230 → 2026.06.231`; README `1.9.101 → 1.9.102`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.230, PR #252

**Trust-recovery routing convention revised to severity-tiered** (pack `1.47.0 → 1.47.1`). Per maintainer direction ("routing flag only"), the trust-recovery findings-routing convention changes from "every confirmed finding to a single top-priority tier regardless of severity" to **severity-tiered routing**: High[critical] and High to the top-priority tier (this project: P1), Medium and Low to the next tier (P2). The core invariant is unchanged: nothing the assistant judges trivial is silently dropped (severity governs the destination tier, not whether a finding is surfaced), the maintainer (not the assistant) decides what to defer, and the maintainer-sign-off termination still ends the tier. Propagated in lock-step across every surface that states the convention: the [`trust-recovery-escalation.md`](dev-security/claude-rules/governance/trust-recovery-escalation.md) rule and its [`.claude/rules/governance/trust-recovery-escalation.md`](.claude/rules/governance/trust-recovery-escalation.md) byte-identical mirror; the [`deep-qa-review`](dev-security/claude-rules/skills/deep-qa-review/SKILL.md) SKILL plus the [`/full-qa`](.claude/commands/full-qa.md) command; the [`library-fitness-review`](dev-security/claude-rules/skills/library-fitness-review/SKILL.md) SKILL (new step 5.5 routing-flag) plus the [`/fitness`](.claude/commands/fitness.md) command; and the pack [`CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) plus project [`.claude/CLAUDE.md`](.claude/CLAUDE.md) rule-description bullets. The pack [`README.md`](dev-security/claude-rules/README.md) gains a 1.47.1 version-history row; the historical 1.47.0 row is left accurate-to-time. Also carries the deferred PR #251 `/validate-pr` (1 note, reconciled) + `/retro` rows and the routing-surface-list reconciliation per recursion-avoidance. Pack `1.47.0 → 1.47.1`; library `2026.06.229 → 2026.06.230`; README `1.9.100 → 1.9.101`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.229, PR #251

**Session decision capture (P1–P4 backlog triage)** — working-state housekeeping. Records the maintainer's 2026-06-22 decisions from the requested TODO P1–P4 analysis so the remediation and codification PRs execute against settled targets, and carries the PR #250 `/validate-pr` (0 findings) + `/retro` rows per recursion-avoidance. Decisions captured (in [`TODO.md`](TODO.md) annotations + [`.working/design-decisions.md`](.working/design-decisions.md)): the six H[critical] canonical values accepted as recommended (FR-134 procedure scoring canonical; FR-135 TLS 1.3 everywhere incl the B2B/EDI adapter unconditionally; FR-136 retention-schedule authoritative + tiered; FR-137 DSAR 3 years; FR-138 scrub CPPA-as-live to PIPEDA Schedule 1; FR-139 1h RPO binding); trust-recovery findings routing revised to **severity-tiered** (H[critical]+High→P1, Medium+Low→P2, "routing flag only", sign-off retained) — the 8-surface revision is queued as the next substantive PR; P4.0 = ship the `project-integrity` pack rule as the 10th governance rule standalone after the codification batch; P4.1 = skill-family + prescriptive-only + existing-pack bump; P4.4 = JS/TS+Go+Java baseline pointing to OWASP; P4.5 = build the S1 retention gate, defer S2/S3. Also refreshes [`.working/session-handoff.md`](.working/session-handoff.md) to the after-PR-#250 snapshot with the locked decisions and the routing-revision next-action. Working-state and config change; the only gated files touched are [`README.md`](README.md) (version lines), [`TODO.md`](TODO.md) (gate-45 annotations), and this CHANGELOG. Library `2026.06.228 → 2026.06.229`; README `1.9.99 → 1.9.100`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.228, PR #250

**`/resume` Sweep 23 close-out** — the session-resume compensating-control `/validate`. A fresh session opened on `claude/resume-oojneh` from `main` at PR #249; per the [`/resume`](.claude/commands/resume.md) protocol's step 5, the first substantive task is a full corpus-wide `/validate` (the compensating control for the session-closing handoff PRs #248/#249 that skipped their trailing `/validate-pr`). The clone started shallow and was unshallowed before any history-aware audit per the full-clone methodology rule; the mechanical baseline was clean (46/46). All three subagents (A recent-PR deep review of #243–#249, B corpus-wide stale-reference, C audit-programme integrity) were dispatched. Subagents A and C returned zero findings — the trust-recovery codification is internally and cross-surface consistent (the 2 suite-skills / 6 subagents / 10 personas count systems do not collide; the local rule mirror is byte-identical; version chains are contiguous), and four-surface gate parity holds at 46. Subagent B surfaced one in-window note: [`.claude/CLAUDE.md`](.claude/CLAUDE.md) line 263's close-out-checklist example read "the eight governance rules" when the current count is nine (the same file's own enumeration and [`tools/lint-collection-enumeration-consistency.py`](tools/lint-collection-enumeration-consistency.py) both confirm nine); corrected here, in-window because the checklist was added in PR #247 when the count was already nine. The two pre-flight scanner candidates were confirmed false positives ("a suite of two skills" names the trust-recovery suite size, not the 14-skill total). The cross-document drift cluster (FR-134..139, FR-161, FR-163) was confirmed present in the live corpus but is already tracked in the P1/P2 backlog from the trust-recovery passes — reported for dedupe, not re-routed. Working-state and config change; the gated files touched are [`README.md`](README.md) (version lines), [`TODO.md`](TODO.md) (sweep cursor advanced to Sweep 23, caught by gate 45 as a paired-surface miss), and this CHANGELOG. Library `2026.06.227 → 2026.06.228`; README `1.9.98 → 1.9.99`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.227, PR #249

**Handoff-PR QA loop-break** — closes a recursion in the per-PR QA cadence at session boundaries. A session-closing handoff PR (one whose purpose is to land working-state on `main` as a green merge so the next session resumes from `main`) previously would, per step 5a, run a trailing `/validate-pr` + `/retro`; those produce ledger rows that, per recursion-avoidance, must batch into a *new* PR, whose merge triggers another `/validate-pr` — an unterminating loop, because at a session boundary there is no "next substantive PR" to absorb the rows. This PR codifies the fix the maintainer directed: the session-closing handoff PR is **exempt from the trailing `/validate-pr`/`/retro`**, and the compensating control is that the next session's [`/resume`](.claude/commands/resume.md) runs a full corpus-wide `/validate` as its first task (stronger than the skipped per-PR sweep, since it re-examines the whole corpus). Wired across [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (PR-workflow step 5a handoff-PR exception; a new "closing-handoff-PR discipline" point in the session-migration section), [`.claude/commands/resume.md`](.claude/commands/resume.md) (full `/validate` as the first task), and [`.working/session-handoff.md`](.working/session-handoff.md) (how-to-resume step, next-actions item, standing-disciplines exception). The exemption is recorded as a maintainer-authorised standing exception in the [`.working/validate-pr/history.md`](.working/validate-pr/history.md) row for #248+#249 per the no-skip discipline. Follow-ups queued in [`TODO.md`](TODO.md): generalize the carve-out into the pack `validation-sweep-pr-scoped` SKILL + `ai-assistant-workflow-disciplines` rule (so adopters inherit it), the P4.6 gate must design in the handoff-PR exemption, and a new P4.7 scopes an external overnight-driver loop (fresh `claude -p`/SDK session per task-unit reading the handoff) for unattended longer runs. This is itself the session's closing handoff PR. Working-state and config change; the only gated files touched are [`README.md`](README.md) (version lines) and this CHANGELOG. Library `2026.06.226 → 2026.06.227`; README `1.9.97 → 1.9.98`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.226, PR #248

`.working/` session close-out for local project: adds [`.working/session-length-considerations.md`](.working/session-length-considerations.md), a generic write-up of why long AI-assistant sessions degrade (context dilution, lossy compaction, state drift, error compounding, late-session throughput pressure, no reliable internal gauge) and how to mitigate it (durable state in committed files, mechanical gates and fresh-context reviewers, small frequent merges, fresh sessions at boundaries); refreshes [`.working/session-handoff.md`](.working/session-handoff.md) to the after-PR-#248 snapshot with a pointer to the new lesson; and carries the PR #247 `/validate-pr` (clean) and `/retro` rows per recursion-avoidance. This is the session's closing handoff PR, merged green per the maintainer's "a session's last act is a green merge" discipline. Working-state only; the only gated files touched are [`README.md`](README.md) (version lines) and this CHANGELOG. Library `2026.06.225 → 2026.06.226`; README `1.9.96 → 1.9.97`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.225, PR #247

**Session migration protocol** — the long-session-degradation defence, and the close-out of the trust-recovery codification's bookkeeping. Adds [`.working/session-handoff.md`](.working/session-handoff.md): the single resume point for a new session (state snapshot, last-merged PRs, next-actions queue, open decisions, standing disciplines), refreshed at every PR close-out. Adds the [`/resume` command](.claude/commands/resume.md) so a fresh session continues from one instruction. Adds a `## Session migration and PR close-out checklist` section to [`.claude/CLAUDE.md`](.claude/CLAUDE.md) plus PR-workflow step 5c. The close-out checklist is the convention-level guard against the **"paired-bookkeeping-surface missed"** degradation pattern (a correct substantive change shipped with a paired ledger, rotation, or count surface dropped) that surfaced twice this session. This PR also clears the rotation debt that pattern produced: FR-164 rotated out of [`TODO.md`](TODO.md) into [`.working/DONE.md`](.working/DONE.md) (it was closed in PR #246's CHANGELOG but not rotated); the shipped codification-checklist items (deep-qa-review #244, ninth rule #246) rotated to DONE with session-bringing-current entries for #243-#247; a stale "eight governance rules" count at TODO P4.1 corrected to "nine"; and the deferred PR #246 `/validate-pr` + `/retro` rows carried per recursion-avoidance. Working-state and config change; no adopter-facing corpus content. Library `2026.06.224 → 2026.06.225`; README `1.9.95 → 1.9.96`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.224, PR #246

**Adds the ninth governance rule [`trust-recovery-escalation.md`](dev-security/claude-rules/governance/trust-recovery-escalation.md) to the dev-security pack** — the second trust-recovery codification PR. The rule names the escalation tier invoked when an AI assistant's discipline failures put a maintainer's confidence in a *window* of work in question: the trigger classes (abbreviated or skipped QA across changes, a skipped verification reaching the shared pipeline, a wrong-cadence automation, an unvalidated inference that cascaded), the two-skill suite (the AI-failure-pattern forensic pass `deep-qa-review` / `/full-qa` first, then the fresh-reader persona pass `library-fitness-review` / `/fitness`), the findings-routing convention (every confirmed finding to the backlog's top priority regardless of severity, apply-time-verified, deduped), and the sign-off discipline (the tier terminates only on explicit maintainer sign-off, not on an empty finding-set). It also carries the full-clone methodology rule. Wired across the three governance-rule enumeration surfaces (pack README directory-tree, pack [`CLAUDE.md`](dev-security/claude-rules/CLAUDE.md), project [`.claude/CLAUDE.md`](.claude/CLAUDE.md)) plus the [`.claude/rules/governance/`](.claude/rules/governance/) local mirror and its sync mapping in [`tools/lint-claude-rules-sync.py`](tools/lint-claude-rules-sync.py); the `deep-qa-review` SKILL's two forward references to the rule are now linkified. **Closes FR-164**: the [`tools/lint-collection-enumeration-consistency.py`](tools/lint-collection-enumeration-consistency.py) docstring's stale "seven governance rules" is corrected to "nine". Also bundles the deferred PR #245 `/retro` row and the PR #244 + #245 `/validate-pr` history rows (the #244 row was a recursion-avoidance bookkeeping slip missed in PR #245, caught and corrected here), plus a cosmetic "(TODO P4)" → "(TODO P4.0)" fix in the PRIMORDIAL RULE. Pack `1.46.0 → 1.47.0`; library `2026.06.223 → 2026.06.224`; README `1.9.94 → 1.9.95`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.223, PR #245

**Adds the PRIMORDIAL RULE: PROJECT INTEGRITY (highest precedence) to [`.claude/CLAUDE.md`](.claude/CLAUDE.md).** By maintainer direction, the project now carries an apex rule establishing a lexicographic, absolute priority ordering (Quality > Speed > Cost) with non-negotiable integrity clauses (correctness over apparent completion; no silent changes; no suppression of tests, audit gates, linting, or error handling to force a pass; no fabrication of APIs/citations/behaviour; failing states always surfaced), an escalation directive (halt and surface any forced quality compromise rather than resolve it silently toward speed or cost), and a semantic-checkpoint self-reminder cadence (task start, before commit, before completion claims, at quality/speed/cost tension; the per-file-write and per-N-operations mechanical triggers were dropped as noise by maintainer calibration). The rule consolidates and elevates the integrity disciplines already in the [`dev-security/claude-rules/governance/`](dev-security/claude-rules/governance/) pack (gate-discipline, evidence-grounded-completion, clarify-before-acting, change-tracking) under one priority; it governs optimization-dimension conflicts and is complementary to the existing rule-source layering note. A project-agnostic distributable form is queued as a pack governance rule ([`TODO.md`](TODO.md) P4.0). This PR also carries the deferred PR #244 `/retro` row. Working-state / config change; no adopter-facing corpus content changed. Library `2026.06.222 → 2026.06.223`; README `1.9.93 → 1.9.94`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.222, PR #244

**Codifies the `deep-qa-review` skill (`/full-qa`)** — the AI-failure-pattern half of the trust-recovery escalation tier, and the first codification PR after the trust-recovery suite's sign-off. `deep-qa-review` is a six-subagent forensic QA pass (recent-PR deep review, corpus-wide stale-reference, audit-programme integrity, citation forensic, generated-artefact forensic, discipline-violation forensic) run over a maintainer-named PR window when an AI assistant's discipline failures call for a white-box re-examination beyond the routine sweeps; it pairs with `library-fitness-review` (`/fitness`) to form the suite. The skill bakes in a binding step-0 rule learned from its own first run: verify a full (non-shallow) clone before any git-history-aware audit, because `git log --follow` on a shallow clone mis-attributes last-commit dates and makes gates 31 and 40 emit false positives (iteration 1 caught a 153-document gate-31 false positive this way). Findings route to the backlog top priority tagged `[full-qa]` regardless of severity; the pass terminates on maintainer sign-off, not on an empty finding-set. Shipped with the [`/full-qa` slash command](.claude/commands/full-qa.md) (step-identifier parity 0-6 with the SKILL, enforced by gate 44), the PAIRS-registry extension in [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py), and the pack-skills enumeration update in [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) (13 to 14 skills). This PR also carries the deferred PR #242 and #243 `/validate-pr` and `/retro` ledger rows per recursion-avoidance. Pack `1.45.2 → 1.46.0`; library `2026.06.221 → 2026.06.222`; README `1.9.92 → 1.9.93`. The ninth governance rule (the `trust-recovery-escalation` rule) and the `/fitness` routing-flag amendment follow in subsequent PRs. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.221, PR #243

**Trust-recovery suite — findings routed and re-tiered.** Ran the maintainer-directed trust-recovery escalation tier (the response to the prior session's discipline failures: abbreviated `/validate-pr` over 11 PRs, a skipped post-commit audit on #242, a 60-minute-vs-60-second timer). Two complementary white-box passes over PRs #218-#242 and the whole corpus: `/full-qa` (the new `deep-qa-review` six-subagent forensic lens; record at [`.working/full-qa/2026-06-22-iter1.md`](.working/full-qa/2026-06-22-iter1.md)) then `/fitness` r2 (ten persona lenses; report at [`.working/fitness-reviews/2026-06-22-r2.md`](.working/fitness-reviews/2026-06-22-r2.md)). 32 confirmed findings routed to TODO: 6 H[critical] + 6 High retained in P1 (six convergent multi-surface contradictions — risk-scoring divergence, TLS 1.2/1.3 floor, log and DSAR retention, CPPA-cited-as-in-force, DR RPO-vs-backup-gap, adopter starter-set divergence), with the Medium/Low/FYI re-tiered to P2/P3 (FR-146 to FR-165) per maintainer direction. The most consequential outcome was a finding *prevented*: a `/full-qa` subagent's "gate 31 fails on 153 documents" was validated as a shallow-clone artifact (the takeover container was a depth-50 clone; `git log --follow` mis-attributed dates) and excluded before it reached the backlog; the full-clone audit exits 0. Two findings deduped against existing FR-30 (Art-28 DPA template) and FR-44-generalisation (shall/must). Working-state only ([`.working/`](.working/) records plus [`TODO.md`](TODO.md) routing); no adopter-facing corpus content changed. Codification of `deep-qa-review`, a ninth governance rule, the `/fitness` routing flag, and a recurring structural-review skill follows in subsequent PRs. Library `2026.06.220 → 2026.06.221`; README `1.9.91 → 1.9.92`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for detail.

## 2026-06-22, Library Version 2026.06.220, PR #242

**Sweep 22 close-out** — maintainer-directed full `/validate` after surfacing a discipline failure: the orchestrator had recorded "abbreviated spot-check, 0 findings" rows in [`.working/validate-pr/history.md`](.working/validate-pr/history.md) for 11 consecutive PRs (#231-#241) without dispatching the formal Subagent A that the [`validation-sweep-pr-scoped` SKILL](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) mandates. Sweep 22 surfaced 4 in-window errors (all C-3 multi-surface-incompleteness from PR #238/#239's treatment-vocab decomposition not propagating to policy, methodology procedure, register procedure Status field, or the enterprise-risk-register template) and 1 out-of-window note (5 EDPB soft-law citations not in the canonical-citations register; surfaced to TODO P7). In-window fixes propagate the canonical 6-option treatment set (Avoid / Mitigate / Transfer / Accept / Exploit / Enhance) and canonical 3-state Treatment Status set (Pending / In Progress / Complete) into the four affected risk-domain files; risk-record Status field corrected to Open / Closed lifecycle. Discipline corrective actions land in the same PR: both `validation-sweep` SKILL.md files now explicitly prohibit abbreviation parallel to skipping; both copies of the [`ai-assistant-workflow-disciplines`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) pack rule extend the "Orchestrator-side judgment-call skipping" bullet to "skipping OR abbreviation" with throughput-pressure clause; new section "Throughput pressure does not authorise QA abbreviation" added to the project CLAUDE.md. P4.6 queued in TODO for mechanical-enforcement audit-gate candidate. Pack version `1.45.1 → 1.45.2`. Library `2026.06.219 → 2026.06.220`; README `1.9.90 → 1.9.91`. See [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) for the full file list and the 7-point discipline-failure assessment.

## 2026-06-22, Library Version 2026.06.219, PR #241

**Closes FR-97 (M, S) + FR-98 (M, S)** — P2.3 cross-framework matrix bundle. PR-E in Batch 2. **FR-97**: ISO 31000 clause-numbering misalignment in [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) corrected against ISO 31000:2018 actual clause numbers — "Clause 6 Identify / Analyse / Treat / Monitor and review" updated to "Clause 6.4.2 Risk identification / 6.4.3 Risk analysis / 6.5 Risk treatment / 6.6 Monitoring and review"; "Clause 5.3 Design" for third-party row corrected to "Clause 6.3 Scope, context, criteria and Clause 5.3 Integration"; AI lifecycle row clarified as "Clause 6 Process applied iteratively across the AI lifecycle"; Exception and acceptance row clarified as "Clause 6.5 Risk treatment, acceptance option". Per-doc `1.1.3 → 1.1.4`. **FR-98**: [`compliance/annex-nis-2-implementation.md`](compliance/annex-nis-2-implementation.md) Article 21.2 sub-measures table gains an Evidence class column (parallel to the matrix's evidence-class column) for each of the ten (a)-(j) sub-measures, naming the artefact classes adopters collect as evidence of operating the measure. Per-doc `1.0.1 → 1.1.0`. Library `2026.06.218 → 2026.06.219`; README `1.9.89 → 1.9.90`.

## 2026-06-22, Library Version 2026.06.218, PR #240

**Closes FR-93 (M, S) + FR-94 (M, S)** — P2.6 KRI/KPI bundle. PR-D in Batch 2. **FR-93**: [`risk/register-key-risk-indicators.md`](risk/register-key-risk-indicators.md) v1.0.2 → 1.1.0; KRI schema gains two fields — **Red-Threshold Escalation Owner** (the named role with decision authority when the Red threshold is breached; defaults per category: CISO for cyber, CCO for compliance, Risk Committee for operational; adopters substitute their escalation hierarchy) and **Red-Threshold Evidence Class** (the evidence captured on breach: timestamp, value trajectory, decision and rationale, risk-register link, incident or control-intervention link; retained per records-retention schedule). **FR-94**: [`risk/register-assurance-map.md`](risk/register-assurance-map.md) v1.0.1 → 1.1.0; Linked-controls field now explicitly named as adopter-defined ("the library does not ship a control register because the control identifier scheme is necessarily adopter-defined; the worked example below uses placeholder IDs in the form CTL-IAM-001 to illustrate the field shape; adopters substitute their own scheme"); guidance added on a typical control-register column set and on how to extract controls from existing policies and standards as a bootstrap. Library `2026.06.217 → 2026.06.218`; README `1.9.88 → 1.9.89`.

## 2026-06-22, Library Version 2026.06.217, PR #239

**Closes FR-12 cross-doc follow-up (M, S)** — reconciles [`risk/procedure-risk-register.md`](risk/procedure-risk-register.md) treatment vocabulary with the ERM standard's canonical 6-option set (Avoid / Mitigate / Transfer / Accept / Exploit / Enhance, per the [enterprise risk management standard](risk/standard-enterprise-risk-management.md) §6). The procedure previously listed a different 6-option set (Mitigate / Avoid / Transfer / Accept / Monitor / Further Analysis or Analyze) that conflated workflow states with treatment options. Now the procedure references the standard's canonical six and explicitly notes that "Monitor" and "Further Analysis" map to Treatment Status workflow values (Pending / In Progress) rather than to separate treatment options. Both the "Select Treatment Option" step and the register-field "Treatment Decision" row are updated; the latter is split into Treatment Option (canonical 6) + Treatment Status (workflow 3) to match the standard's §7.1 schema introduced in PR #238. PR-C in Batch 2 effort-first run. Per-doc `1.0.0 → 1.1.0`. Library `2026.06.216 → 2026.06.217`; README `1.9.87 → 1.9.88`.

## 2026-06-22, Library Version 2026.06.216, PR #238

**Closes FR-118 (H, S)** — ERM standard internal §6/§7 treatment-vocab inconsistency resolved in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) v1.5.1 → 1.6.0. Section 6 (Risk treatment) gains a terminology paragraph distinguishing **Treatment Option** (the risk owner's choice: Avoid / Mitigate / Transfer / Accept / Exploit / Enhance) from **Treatment Status** (workflow state of the option's execution: Pending / In Progress / Complete) and from **Status** (risk-record lifecycle: Open / Closed). Section 7.1 register fields updated: prior single "Status" field with mixed semantics (Open / Mitigated / Accepted / Closed — which conflated treatment outcomes with workflow states) is replaced by three explicit fields: Treatment Option (unchanged from §6's 6 options), new Treatment Status field (Pending / In Progress / Complete), and Status field with cleaned semantics (Open / Closed only, with prose clarifying that Status names risk-record lifecycle and NOT treatment outcome). Closes the structural ambiguity FR-118 surfaced during Pass-2 reshape (where an Avoided risk had no clean Status value other than "Closed"). PR-B in Batch 2 effort-first run. Per-doc `1.5.1 → 1.6.0`. Library `2026.06.215 → 2026.06.216`; README `1.9.86 → 1.9.87`.

## 2026-06-22, Library Version 2026.06.215, PR #237

**Closes FR-36 (H, S)** — GDPR Article 8 child-consent age thresholds per Member State now documented in [`privacy/jurisdictions/annex-privacy-european-union.md`](privacy/jurisdictions/annex-privacy-european-union.md) (new section between Cross-border-transfer-mechanisms and Enforcement-and-fines). The prior single line in [`privacy/framework-childrens-data.md`](privacy/framework-childrens-data.md):41 ("13 to 16 depending on the state") is now backed by a 30-row table covering all 27 EU Member States plus the 3 EEA countries (Iceland, Liechtenstein, Norway), each with the chosen age (13, 14, 15, or 16) and the national implementing-law citation. Notes added on (a) the GDPR Article 8 default age of 16 where no derogation is enacted; (b) Article 8 governs information society services (other lawful bases may apply at different age thresholds); (c) adopters operating across multiple Member States apply the per-state age; (d) adopters must verify against current national law before relying on the values; (e) the UK is documented separately under UK GDPR Article 8 in the UK annex. Cross-reference added in the children's-data framework's Per-jurisdiction-age-thresholds table pointing at the new EU annex section. PR-A in Batch 2 effort-first run. Per-doc bumps: EU annex `1.0.3 → 1.1.0`; children's framework `1.0.4 → 1.0.5`. Also carries Sweep 21 zero-finding history row (post PRs #229-#236 batch; all 3 subagents dispatched per discipline; empty-delta termination) and deferred PR #236 /validate-pr (0 findings) + /retro register rows. Library `2026.06.214 → 2026.06.215`; README `1.9.85 → 1.9.86`.

## 2026-06-22, Library Version 2026.06.214, PR #236

**Closes P7 maintainer-decision queue (3 items: A2, B4, FR-47)** — PR-G in Batch 1 effort-first run. Three Sweep-20-surfaced and pending-closure items actioned per maintainer's pre-approved P7 decision. **A2 (Sweep 20 in-window note)**: [`governance/register-role-authority.md`](governance/register-role-authority.md) DPO row gains one-clause cross-reference: "The role is subject to the GDPR Article 38(3) independence requirements and the Article 38(6) conflict-of-interest constraint elaborated in [`privacy/charter-privacy-management-programme.md`](privacy/charter-privacy-management-programme.md)." Per-doc `1.5.0 → 1.5.1`. **B4 (Sweep 20 out-of-window note)**: [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) scope extended to soft-law supervisory guidance. New Conventions paragraph names the scope extension; new "Soft-law supervisory guidance" section added before Maintenance with WP243 rev.01 (Article 29 Working Party Guidelines on Data Protection Officers, endorsed by EDPB May 2018) as first entry. Per-doc `1.4.23 → 1.5.0` (minor; scope extension). **FR-47 (P2.10 formal closure pending review)**: surface-consolidated in PR #218 (canonical DPO label across register + glossary + privacy/README); formal closure recorded now via removal from P7 + DONE entry. Also carries deferred PR #235 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.213 → 2026.06.214`; README `1.9.84 → 1.9.85`.

## 2026-06-22, Library Version 2026.06.213, PR #235

**Closes C2 convergent finding bundle (FR-121 + FR-122 + FR-123 + FR-124 + FR-125 + FR-126)** — emergency-access operational clarity in [`security/procedure-access-control.md`](security/procedure-access-control.md) (PR-E in Batch 1 effort-first run). Per maintainer direction, ships with sample-data defaults that adopters MUST adjust upon adoption (a header note in §1.4 names this explicitly). Specific changes: (1) FR-121 "material business or safety harm" now defined inline — delay that would on its own more likely than not cause a P1 or P2 incident under the adopter's severity policy; (2) FR-122 "declared incident response" tied to P1 or P2 severity (with note that adopters using a different severity model substitute the top-two bands); (3) FR-123 "Delegated Security Lead" added as a row to the Roles and Responsibilities table, defined as a named deputy of the CISO (sample data: senior IRT member or deputy CISO); (4) FR-124 access-review revocation timeline contradiction (§3.2 "next review" vs §3.3 "immediate") resolved by introducing a 24-hour window for revocation processing after the reviewer flags access, distinct from the immediate revocation case for security incidents in §5.1; (5) FR-125 emergency-access revocation enforcement gains a 30-min/30-min escalation chain (Identity Team → SOC L2 → CISO); (6) FR-126 auto-escalation mechanic clarified — the ITSM portal's SLA timer fires automatically; the escalation requires no human trigger. Per-doc `1.1.1 → 1.2.0`. Also carries deferred PR #234 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.212 → 2026.06.213`; README `1.9.83 → 1.9.84`.

## 2026-06-22, Library Version 2026.06.212, PR #234

**Closes FR-67 (L, XS)** — adds a new sub-tier **E0: Zero in-house headcount (outsourced contractor)** to the Dimension E (GRC team capacity) ladder in [`docs/template-startup-roadmap.md`](docs/template-startup-roadmap.md). The prior ladder started at E1 (None or founder part-time, where "None" meant zero in-house headcount but the founder still wore the GRC hat part-time). E0 covers the case where the GRC function is entirely outsourced to a third-party contractor or fractional consultant and nobody on the adopter's permanent staff carries GRC duties; the adopter retains accountability (decision authority on residual risk acceptance, sign-off, executive forum participation) but delegates execution; same artefact subset as E1; the operational difference is who holds the pen. PR-D in Batch 1 effort-first run. Per-doc `2.1.0 → 2.2.0`. Also carries deferred PR #233 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.211 → 2026.06.212`; README `1.9.82 → 1.9.83`.

## 2026-06-22, Library Version 2026.06.211, PR #233

**Closes FR-89 (L, XS) + FR-91 (L, XS)** — security-XS bundle in [`dev-security/standard-api-security.md`](dev-security/standard-api-security.md) (PR-C in Batch 1 effort-first run). JWT algorithm-key-type binding requirement added to the Token validation row of the authentication-controls table (Section 2): validators must verify the JWT `alg` header is consistent with the key type used (RS256 with RSA public key, HS256 with the corresponding shared secret); a single key MUST NOT accept multiple algorithm families. Prevents the RSA-public-key-as-HMAC-secret confusion attack per RFC 8725 (BCP 225, JSON Web Token Best Current Practices). Closes FR-89. Webhook signing row in Section 12 expanded with canonical-string definition (HTTP method + canonical URL path + canonical query string + canonical headers + body hash; both sender and receiver derive the same canonical string) and constant-time comparison requirement (`hmac.compare_digest` or equivalent). Replay-prevention row expanded with explicit 5-minute (or documented service-specific) replay window plus seen-nonce cache. Closes FR-91. Per-doc `0.0.4 → 0.0.5`. Also carries deferred PR #232 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.210 → 2026.06.211`; README `1.9.81 → 1.9.82`.

## 2026-06-22, Library Version 2026.06.210, PR #232

**Closes FR-107 (L, XS) + FR-108 (L, XS) + FR-111 (L, XS)** — newcomer-UX bundle in [`docs/adopter-guide.md`](docs/adopter-guide.md) (PR-B in Batch 1 effort-first run). Adds new "Two reference registers you will need early" subsection surfacing both [`governance/register-glossary.md`](governance/register-glossary.md) (acronyms + external-domain terms) and [`governance/register-key-terms-and-definitions.md`](governance/register-key-terms-and-definitions.md) (library-internal GRC concepts) before the "How the library is meant to be used" section, explaining the split-by-term-class so newcomers don't bounce between the two registers wondering which holds what (closes FR-107 + FR-108). Adds reading-time estimate to the Tier 1 starter set ("4 to 6 hours to read all 15 documents at moderate pace") plus an "if you only read three" pick (Charter + Framework + Role Authority Register, since they ground the structure that the rest of Tier 1 operationalises) (closes FR-111). Per-doc `1.1.2 → 1.2.0`. Also carries deferred PR #231 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.209 → 2026.06.210`; README `1.9.80 → 1.9.81`.

## 2026-06-22, Library Version 2026.06.209, PR #231

**Closes FR-112 (M, XS) + FR-131 (FYI, XS)** — maintainer-context cleanup in adopter-facing docs. [`README.md`](README.md) line 58 expanded with a clarifying sentence that the audit toolchain is the maintainer's quality-assurance machinery, NOT an adopter dependency: "Adopters who only consume the corpus do not need it. Adopters who want the same maintenance discipline for their own fork can adopt the toolchain (it is permissively licensed and copy-paste portable), but doing so is optional." Closes FR-112 (the prior text framed the toolchain as a required dependency). [`docs/template-quickstart.md`](docs/template-quickstart.md) line 39 risk-anchor changed from the risk-register procedure to [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md) (the canonical risk policy) so the quickstart's "core baseline" aligns with the adopter-guide Tier 1 starter set (which lists the policy + standard, not the register procedure). Closes FR-131 (Quickstart vs adopter-guide Tier 1 divergence). Per-doc template-quickstart `3.0.0 → 3.0.1`. Also carries deferred PR #230 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.208 → 2026.06.209`; README `1.9.79 → 1.9.80`.

## 2026-06-22, Library Version 2026.06.208, PR #230

**TODO reorganization (maintainer-directed)**: restructured [`TODO.md`](TODO.md) so every backlog item fits cleanly into priority sections P1-P7 rather than separate per-topic sections. Per the maintainer's direction: "every one cleanly fits into priorities rather than sections about different topics. Each item should be clearly described so that you know what to do next without looking visually discombobulated." Two open design questions surfaced before the rewrite: (1) FR-70/71/72/73 placement (H[critical] severity AND new-domain shape) — decision: severity wins, place in P1 only with cross-references to P6; (2) meta-section justification — decision: promote "Investigation / blocked" to P7 ("Awaiting maintainer decision"), keep Standing conventions and Notes on maintenance as meta-sections after the priorities. **New structure**: P1 Urgent quality (H[critical] + H, 14 items), P2 Substantive improvements (M, ~30 items including Phase 2 clusters + BYOD + file relocations), P3 Low-priority cleanup (L + FYI, ~16 items including FR-44 generalisation and Sweep 3 follow-up), P4 Adopter experience (5 process/meta items: sharable skill, effort-sizing, version-upgrade procedure, language coverage, S1/S2/S3 audit-gate candidates), P5 Content expansion (8 subsections of country/regulator overlays), P6 Domain-level expansion (5 new-domain items including CMMI capability levels), P7 Awaiting maintainer decision (Sweep 20 A2 + B4, FR-47 formal closure pending, dropped-decision audit trail). Fitness review backlogs from the 2026-06-21 and 2026-06-22 r1 reviews are now distributed by severity into the matching priorities. Each item has a consistent shape: `**FR-N (severity, effort)**: description with location reference` for scannability. Also carries deferred PR #229 /validate-pr history row (0 findings) and /retro register row (acronym-undefined pattern firmly at pattern stage; worker-brief template update due). Library `2026.06.207 → 2026.06.208`; README `1.9.78 → 1.9.79`.

## 2026-06-22, Library Version 2026.06.207, PR #229

**/validate Sweep 20 iter 1 close-out** — corpus-wide sweep post 8-PR FR batch (PRs #221-#228 closing FR-33/82/49/37/38/39/40/42) surfaced **4 in-window warnings** (3 newly-introduced acronyms missing from glossary: CIIO, HKDF, AEAD; 1 cross-document drift: [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md):46 didn't cross-reference PR #228's Article 38(6) conflict framework in the charter) plus 2 maintainer-surfaced notes (A2: should [`governance/register-role-authority.md`](governance/register-role-authority.md):39 DPO row reference Article 38(3)/(6) constraints; B4: scope-of-register policy question on whether WP243 / EDPB soft-law guidance belongs in [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md)). **Fixes applied**: 3 new glossary entries (AEAD per RFC 8439 + NIST SP 800-38D; CIIO per Cybersecurity Law of China + PIPL Articles 38 / 40; HKDF per RFC 5869) in [`governance/register-glossary.md`](governance/register-glossary.md) (per-doc `1.3.0 → 1.4.0`); cross-reference sentence added to [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md):46 pointing at the charter's "DPO independence and conflict of interest" subsection (per-doc `1.4.2 → 1.4.3`). **Pattern observed**: "newly-introduced acronym not added to glossary in same PR" at 3 occurrences in single batch (CIIO, HKDF, AEAD); worker-brief candidate strengthened. Sweep 20 iter 1 detail file at [`.working/validate-sweeps/2026-06-22-sweep20-iter1.md`](.working/validate-sweeps/2026-06-22-sweep20-iter1.md). Also carries deferred PR #228 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.206 → 2026.06.207`; README `1.9.77 → 1.9.78`.

## 2026-06-22, Library Version 2026.06.206, PR #228

**Closes FR-42 (medium, P2.1)**: DPO independence (GDPR Article 38(3)) and conflict-of-interest (GDPR Article 38(6)) framework. [`privacy/charter-privacy-management-programme.md`](privacy/charter-privacy-management-programme.md) previously had a one-line "Interim Accountability" note declaring the CIO assumes DPO responsibilities when no formal DPO is designated, without flagging the structural tension this creates with Article 38(3) independence and Article 38(6) conflict-of-interest constraint. Added a new subsection covering: Article 38(3) 3-row independence requirements (no instructions on task exercise; no dismissal / penalty; direct reporting to highest management level) each with practical forbidden-conduct example; Article 38(6) conflict-of-interest test naming the WP243 rev.01 / EDPB list of typically incompatible positions (CEO, COO, CFO, CIO, CISO determining purposes / means, Head of Marketing / HR / IT-ops, audit authority); explicit "Interim CIO-as-DPO: known conflict" subsection making the structural tension visible and naming 3 adopter paths (formal DPO designation, mitigation controls, or formal Article 37(1) exemption analysis); 5-row mitigation controls table for the interim arrangement (independent escalation path, documented role separation, external counsel arms-length channel, annual effectiveness review, public statement in privacy notice and ROPA); cross-regime independence equivalents (UK GDPR, LGPD Article 41, PIPL Article 52, India DPDP). The Interim Accountability note now cross-references the new subsection. Per-doc `1.4.0 → 1.5.0`. Also carries deferred PR #227 /validate-pr history row (0 findings) and /retro register row (single-occurrence Commonwealth orthography drift). Library `2026.06.205 → 2026.06.206`; README `1.9.76 → 1.9.77`.

## 2026-06-22, Library Version 2026.06.205, PR #227

**Closes FR-40 (medium, P2.1)**: PIPL Articles 38 to 40 cross-border outbound mechanics operationalised in [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md). The prior procedure documented PIPL cross-border in a single line ("Apply PIPL Articles 38 to 40"); expanded into a 7-step PIPL-specific workflow: Step A (applicability and CIIO status), Step B (mechanism selection per Article 38, 5-tier volume table including safe-harbor under 100,000, Standard Contract 100,000 to 1,000,000 or under 10,000 sensitive, CAC Security Assessment over 1,000,000 / CIIO / important-data / 10,000+ sensitive, third-party certification for intra-group), Step C (Article 39 separate consent, 5 mandatory consent elements, not bundleable with Article 13 general consent), Step D (Article 40 CIIO and regulated-quantity domestic-storage obligations), Step E (PIA per Article 55), Step F (documentation and re-assessment cadence, quarterly volume re-check, 3-year security-assessment renewal), Step G (coordinated triggers across regimes, parallel GDPR Chapter V, Article 36 prior consultation interaction). Reflects the CAC **Provisions on Promoting and Regulating the Cross-Border Flow of Data** (effective 22 March 2024) with revised thresholds. Per-doc `1.4.1 → 1.5.0`. Also carries deferred PR #226 /validate-pr history row (0 findings) and /retro register row (em-dash temptation pattern shifted to converging after preemptive avoidance). Library `2026.06.204 → 2026.06.205`; README `1.9.75 → 1.9.76`.

## 2026-06-22, Library Version 2026.06.204, PR #226

**Closes FR-39 (medium, P2.1)**: EU representative (GDPR Article 27) appointment process. [`privacy/charter-privacy-management-programme.md`](privacy/charter-privacy-management-programme.md) previously mentioned the EU representative only in passing (in the joint-controller template and privacy-notice template fields). Added a dedicated subsection under "Privacy accountability structure" covering: Article 3(2) trigger criteria; Article 27(2) 4-criterion exemption table (occasional + no Art 9/10 + low risk + public-authority); Article 27(3)(4) representative criteria (Member-State location, written designation, mandate scope, GDPR knowledge, ROPA copy maintenance); 7-step designation process (DPO assessment, identification, written mandate, CIO sign-off, privacy-notice publication, ROPA entry, supervisory-authority filing); maintenance triggers (annual, material processing change, representative capacity change); Article 27(5) liability-shield clarification; and cross-regime equivalents (UK GDPR, LGPD legal representative, PIPL Article 53, India DPDP, Saudi PDPL). Per-doc `1.3.3 → 1.4.0`. Also carries deferred PR #225 /validate-pr history row (0 findings) and /retro register row (em-dash temptation pattern now at 3rd occurrence / pattern stage; worker-brief template update due). Library `2026.06.203 → 2026.06.204`; README `1.9.74 → 1.9.75`.

## 2026-06-22, Library Version 2026.06.203, PR #225

**Closes FR-38 (medium, P2.1)**: GDPR Article 12(5) assessment checklist for manifestly unfounded or excessive DSRs. [`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md) §7 previously addressed Article 12(5) in a single line; expanded into a structured 7-subsection checklist covering default-free-of-charge baseline (§7.2.1), 4-criterion manifestly-unfounded test with per-criterion evidence requirements (§7.2.2: no nexus, contradicted by records, abusive purpose, lack of coherent specification), 4-criterion manifestly-excessive test (§7.2.3: repetitive short interval, disproportionate volume, disproportionate scope sweep, request-as-discovery), action-options either/or election (§7.2.4: charge reasonable fee OR refuse), 5-step burden-of-proof documentation (§7.2.5: written assessment + Legal Counsel sign-off + DPO sign-off + subject communication + DSR register entry with 3-year minimum retention), reasonable-fee cost-recovery calculation method (§7.2.6: cost categories, hourly rate, no profit margin, itemisation, waiver for hardship), and cross-regime equivalents table (§7.2.7: UK GDPR, LGPD, PIPL, CPPA-PIPEDA, CCPA-CPRA, APPI). Prior §7.2 (Denial process) renumbered to §7.3; no downstream references break. Per-doc `1.3.5 → 1.4.0` (minor; substantive new subsection structure). Also carries deferred PR #224 /validate-pr history row (0 findings) and /retro register row (pattern signal: "em-dash temptation in new-template drafting" at 2nd occurrence; worker-brief candidate queued). Library `2026.06.202 → 2026.06.203`; README `1.9.73 → 1.9.74`.

## 2026-06-22, Library Version 2026.06.202, PR #224

**Closes FR-37 (medium, P2.1)**: Adds [`privacy/template-joint-controller-arrangement.md`](privacy/template-joint-controller-arrangement.md) (v1.0.0), a new template covering joint controller arrangements per GDPR Article 26 and equivalent obligations under UK GDPR, LGPD (Article 5(VI) operadores conjuntos), PIPL (Article 20 joint personal information handlers), India DPDP Act 2023, and other regimes. Nine sections: (1) joint controller identification (parties, signatories, DPO contacts, EU representatives, lead supervisory authority); (2) joint processing description (purposes, categories, lawful basis, data flows, retention); (3) allocation-of-GDPR-responsibilities table covering every relevant article (6, 9, 10, 13, 14, 15-22, 28, 30, 31, 32, 33, 34, 35, 36, 37-39, 44-49, 26(1) contact point, 26(3) joint-and-several liability) with assignable responsible-party column; (4) operational coordination; (5) liability and indemnification with explicit note that internal indemnity does NOT defeat Article 26(3) joint-and-several liability toward subjects; (6) term and termination; (7) cross-regime alternatives (UK GDPR / LGPD / PIPL / India DPDP / CPPA-PIPEDA / CCPA-CPRA each with notable variations); (8) documentation and audit trail; (9) essence-of-arrangement publication per Article 26(2) naming the 8 elements to publish in each joint controller's privacy notice. Cross-listed in [`privacy/README.md`](privacy/README.md) Active documents (per-doc `1.2.0 → 1.2.1`) and [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (per-doc `1.27.30 → 1.27.31`). Applied apply-time language-audit catches on em-dashes in identification rows and on bare "ensure" usage. Also carries deferred PR #223 /validate-pr history row (0 findings) and /retro register row (CHANGELOG link-coverage convention surfaced: name domains in root entries; full file list in the detailed mirror). Library `2026.06.201 → 2026.06.202`; README `1.9.72 → 1.9.73`.

## 2026-06-22, Library Version 2026.06.201, PR #223

**Closes FR-49 (medium, P1.5)**: H2 label drift across 14 files — `## Governance` renamed to `## Governance and accountability` (the canonical form used by 20+ documents corpus-wide). Renamed via a one-shot Python script with line-anchored pattern matching (`^## Governance$` only; does not affect `## Governance and X` headings). Files touched span ai, governance, operations, privacy, resilience, security, and supply-chain domains (full list with links in the detailed mirror entry). Per-doc Version patch-bump + Date `2026-06-22` for each. [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated. Also carries deferred PR #222 /validate-pr history row (0 findings) and /retro register row. Library `2026.06.200 → 2026.06.201`; README `1.9.71 → 1.9.72`.

## 2026-06-22, Library Version 2026.06.200, PR #222

**Closes FR-82 (medium, P1.6)**: Clarifies the "AI and Model Data" cryptography row in [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md):56 — the prior text `"AES-256 + key hashing (SHA-512)"` conflated three distinct cryptographic concerns (encryption, integrity, key derivation) under the ambiguous phrase "key hashing". Corrected to: `"AES-256-GCM (AEAD: confidentiality with built-in integrity tag); HKDF-SHA-256 for key derivation from high-entropy material; Argon2id (or scrypt) for password-derived keys. SHA-512 alone is a hash function, not a key-derivation function."` Disambiguates: (a) AES-256-GCM is the AEAD mode pairing confidentiality with built-in integrity (no separate HMAC needed); (b) HKDF-SHA-256 is the standard key-derivation-from-existing-high-entropy-material function per RFC 5869; (c) Argon2id / scrypt are the modern password-based KDFs; (d) explicit note that SHA-512 alone is not a KDF. Per-doc `1.3.1 → 1.3.2`; Date refreshed to 2026-06-22. Also carries the deferred PR #221 /validate-pr history row (0 findings) and /retro register row (no new pattern; Article 36(3) table format flagged as reusable for FR-34 and FR-37 to FR-42). Library `2026.06.199 → 2026.06.200`; README `1.9.70 → 1.9.71`.

## 2026-06-22, Library Version 2026.06.199, PR #221

**Closes FR-33 (high[critical], P1.4b standalone)**: GDPR Article 36 prior-consultation pathway in [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md). Step 5 previously conflated internal ERC executive sign-off with the GDPR Article 36 regulatory prior-consultation pathway; they are distinct (internal ERC = governance; Article 36 = regulatory mandate when DPIA residual risk remains high). Restructured Step 5 into three substeps: 5.1 (internal escalation pathway, prior content retained), 5.2 (NEW: Article 36 prior consultation, covering trigger criteria per Art 36(1), six-item consultation content per Art 36(3), 8-week-plus-6-week timeline per Art 36(2) with no-processing-during-consultation, supervisory authority Art 58 corrective powers, 5-step interaction with internal pathway, and non-EU equivalents pointing to LGPD Art 38, PIPL Arts 55-56, UK GDPR Art 36), and 5.3 (documentation requirements split by pathway). Per-doc `1.3.4 → 1.4.0` (minor; substantive new substep). Also carries deferred PR #220 /validate-pr history row (0 findings; abbreviated spot-check) and /retro register row (pattern strengthened to signal stage on "corpus-wide rename script: incomplete substitution coverage" — worker-brief candidate queued). Library `2026.06.198 → 2026.06.199`; README `1.9.69 → 1.9.70`.

## 2026-06-22, Library Version 2026.06.198, PR #220

**Sweep 19 iter 1 close-out** — corpus-wide /validate sweep covering PRs #215-#219 surfaced 2 in-window warnings in [`governance/guideline-minimum-viable-governance-structure.md`](governance/guideline-minimum-viable-governance-structure.md) (lines 67 and 114, stale "CPO" in executive-role enumerations missed by PR #218's spelled-out-only rename script). Same root cause as PR #218 /validate-pr Finding 2 (`risk/register-key-risk-indicators.md:142`): the rename script's substitution list was scoped to spelled-out "Chief Privacy Officer" forms only; bare acronyms slipped through. Both fixes applied in this PR (CPO → DPO on both lines; per-doc `1.0.1 → 1.0.2`; Date refreshed to 2026-06-22). Subagents B (corpus-wide stale-reference sweep) and C (audit-programme integrity) returned 0 findings. Iter 2 verification via direct corpus-wide `\bCPO\b` grep confirmed clean post-fix. **Also carries the deferred PR #219 /validate-pr history row** (0 findings; abbreviated spot-check at session-time given homogeneous mechanical scope) **and the PR #219 /retro register row** (no new pattern surfaced; the rename-script-bare-acronym pattern from PR #218's /retro is reinforced — now at second occurrence / signal stage). Sweep 19 iter 1 detail file at [`.working/validate-sweeps/2026-06-22-sweep19-iter1.md`](.working/validate-sweeps/2026-06-22-sweep19-iter1.md). Library `2026.06.197 → 2026.06.198`; README `1.9.68 → 1.9.69`.

## 2026-06-22, Library Version 2026.06.197, PR #219

**Follow-up to PR #218** (FR-46 DPO consolidation canonical flip): adds at-top "Role-name convention" notes in **24 privacy-relevant documents** (privacy core, AI, supply-chain, security, governance), placed as a blockquote callout immediately after the metadata block and before the first H2 section. Each note names **Data Protection Officer (DPO)** as the canonical privacy-lead role, acknowledges **Chief Privacy Officer (CPO)** as the adopter substitution (typically Canada / US), and points to [`governance/register-role-authority.md`](governance/register-role-authority.md) for the canonical definition and adopter-customisation guidance. Adopters who land directly in a privacy-relevant doc (without first reading the domain README) now see the convention inline. **Also bundles the two PR #218 /validate-pr fixes** per the recursion-avoidance rule: [`tools/build-portal.py`](tools/build-portal.py) line 95 collapsed from `"Data Protection Officer or Data Protection Officer"` (a synonym-collapse double-substitution artefact from the PR #218 rename script) to `"Data Protection Officer"`; [`docs/portal.md`](docs/portal.md) regenerated. [`risk/register-key-risk-indicators.md`](risk/register-key-risk-indicators.md) line 142 stale bare acronym "CPO" replaced with "DPO" (the PR #218 rename script scoped to spelled-out forms only; the bare acronym slipped through); per-doc `1.0.1 → 1.0.2`. PR #218 /validate-pr per-PR record file ([`.working/validate-pr/2026-06-22-PR-218.md`](.working/validate-pr/2026-06-22-PR-218.md)) and history row added; /retro improvement-log row for PR #218 added with a first-occurrence observation that corpus-wide rename scripts should include both spelled-out and acronym substitution lists (queued worker-brief candidate). Library `2026.06.196 → 2026.06.197`; README `1.9.67 → 1.9.68`.

## 2026-06-22, Library Version 2026.06.196, PR #218

**Closes FR-46 DPO consolidation** (medium, P1.5) by **flipping** the canonical privacy-lead role from "Chief Privacy Officer" to "Data Protection Officer", reversing the canonical direction set by PR #210 + PR #217 (closed unmerged). Maintainer-directed: DPO has legislative force in many jurisdictions (GDPR Article 37, LGPD Article 41, India DPDP Act 2023 §10, Malaysia PDPA as amended, etc.) and is the more globally-applicable term; CPO is a Canadian / US convention. The new canonical statement lives in [`governance/register-role-authority.md`](governance/register-role-authority.md) (Data Protection Officer row with expanded adopter-customisation note: Canada / US adopters substitute "Chief Privacy Officer" / "CPO"; some adopters maintain both as distinct roles), with the equivalence convention also documented in [`governance/register-glossary.md`](governance/register-glossary.md) (DPO entry extended) and [`privacy/README.md`](privacy/README.md) (new Role terminology section). Corpus prose rename across 73 files: "Chief Privacy Officer" → "Data Protection Officer", with synonym-pattern pre-cleanup collapsing "Chief Privacy Officer / DPO", "Chief Privacy Officer (or Data Protection Officer)", and similar constructs to single canonical form. Approximately 30 `**Owner:**` metadata fields flipped in jurisdiction annexes and a handful of other documents. [`tools/build-portal.py`](tools/build-portal.py) hardcoded string updated; [`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated; [`taxonomy.yml`](taxonomy.yml) regenerated. **PR-2 follows**: adds at-top "Role-name convention" notes in privacy-relevant docs (post-metadata-block placement, pointing to the role authority register for adopter customisation). Library `2026.06.195 → 2026.06.196`; README `1.9.66 → 1.9.67`.

## 2026-06-22, Library Version 2026.06.195, PR #216

Hot-fix PR for the two real defects /validate-pr surfaced on PR #215 (chat-surfaced findings per the chat-surfacing discipline). Fixed (E1) [`CHANGELOG.md`](CHANGELOG.md) PR #215 entry's "24 failure-mode classes" arithmetic (rephrased to drop the count since the canonical SKILL.md defines 8 classes and the 24 was the sum of three subagent class-sets, which contradicts the canonical surface); fixed (W2) [`TODO.md`](TODO.md) line 13 "synced after PR #213 merge" missed in the PR #215 resume-state refresh (updated to PR #215). Also recorded the deferred PR #215 + PR #214 /validate-pr history rows and the PR #214 + PR #215 /retro improvement-log entries (PR #215 retrospective surfaced a second-occurrence signal of the "single PR refreshes parallel surfaces and misses some lines on each" pattern; pattern stage requires a third occurrence). W3 (closing-sentence drift between root and detailed mirror) left as-is per maintainer decision.

## 2026-06-22, Library Version 2026.06.194, PR #215

Working-state housekeeping for local project: Sweep 18 iter 1 recording (clean bill — 0 in-window, 0 out-of-window across all three subagents A/B/C on the post-PR-#214 HEAD covering PRs #186-#214). Sweep-history row appended to [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md) (Version `2.0.10 → 2.0.11`); TODO resume-state cursor refreshed (sweep 17→18, library 192→193, pack 1.45.0→1.45.1, README 1.9.63→1.9.64). No detail file (zero-finding sweep). The clean-bill streak validates the cumulative discipline of the editorial sweeps (PRs #207-209), the FR-46 rename (PR #210), the CMMI reconciliation (PR #212), the /retro skill introduction (PR #213), and the morning-processing PR #214 across the failure-mode classes the three subagents check.

## 2026-06-22, Library Version 2026.06.193, PR #214

Morning-processing PR for the overnight session that ended at PR #213. Routed the overnight session's design decisions into [`.working/design-decisions.md`](.working/design-decisions.md) (two explicit-drop entries for FR-104 and FR-130 closures), reset [`.working/overnight-pr.md`](.working/overnight-pr.md) from `Status: in-flight` back to stub, and updated TODO and the Next-up recommendations to reflect FR-119 and FR-14+FR-114 closures. Also carried the PR #213 batched items per the recursion-avoidance rule: fixed a stale forward-reference at [`dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) line 175 (the queued-for-PR-186 framing is now stale since the skill it referenced shipped in PR #213); appended the PR #213 validate-pr history row and the PR #213 improvement-log row with the first pattern observation (new-skill drafting checklist candidate). Pack `1.45.0 → 1.45.1` (patch on the SKILL.md prose fix).

## 2026-06-22, Library Version 2026.06.192, PR #213

**Added.** New pack skill [`pr-retrospective`](dev-security/claude-rules/skills/pr-retrospective/SKILL.md) (slash command [`/retro`](.claude/commands/retro.md)) and the paired improvement-log register at [`.working/improvement-log.md`](.working/improvement-log.md). The skill is the **continuous process-improvement loop**: post-merge retrospective on each successful PR, output is one entry per PR in the register, recurring patterns surface as candidates for pack-rule updates / worker-brief template additions / new audit gates.

**Process design (the maintainer's earlier "design a process improvement skill" direction)**:
- Trigger: after every successful merge + `/validate-pr` completes (post-merge sequence: sync main → delete merged branch → `/validate-pr` → `/retro` → next-PR planning).
- Input: `/validate-pr` findings (if any), apply-time worker corrections from [`.working/hallucination-metrics.md`](.working/hallucination-metrics.md) (if any), recently-shipped PRs in the same cluster (for pattern surfacing).
- Output: one row appended to the improvement-log register with columns `Date | PR | FR closed | What went well | Friction | Pattern (if any) | Proposed improvement`.
- Discipline: chat-surfacing for Pattern/Proposed-improvement entries; recursion-avoidance batching of register-row commits into the next substantive PR; no orchestrator-side skip discretion.

**Three-layer learning loop**: the skill pairs with (a) the worker-side [`worker-brief-template.md`](.working/worker-brief-template.md) (catches recurring worker-side failures before they reach the orchestrator), and (b) the apply-time-catch tracking in [`hallucination-metrics.md`](.working/hallucination-metrics.md) (logs orchestrator-side verifications). Together: worker brief prevents → apply-time-catches log → /retro surfaces process-level patterns warranting pack-rule updates.

**Wired-in**:
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR workflow gains step 5b (the `/retro` invocation).
- [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py) PAIRS registry extended with the new pair (gate 44 now validates 4 paired surfaces).
- Pack-skills enumeration in [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) tree updated.

**Register seeded** with the PR #213 entry (the meta-self-application: the skill's first /retro is its own creation PR).

Pack `1.44.1 → 1.45.0` (minor; new skill addition). Library `2026.06.191 → 2026.06.192`; README `1.9.62 → 1.9.63`. Also carries PR #212's /validate-pr history row (0 findings).

---

## 2026-06-22, Library Version 2026.06.191, PR #212

**Closes FR-14 + FR-114** (high[critical]): CMMI 5-tier maturity-ladder reconciliation. Maintainer-confirmed canonical: **CMMI 5-tier** (Initial / Managed / Defined / Quantitatively Managed / Optimized). Two corpus surfaces aligned:

1. [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md): Tier 2 renamed `Developing → Managed`; Tier 4 renamed `Managed → Quantitatively Managed`; Tier 5 renamed `Optimising → Optimized`. Definitions extended with CMMI's process-property language ("repeatable and tracked, with basic metrics defined" / "standardised and documented for organisation-wide consistency" / "statistical controls applied to quantitative objectives"). Overview prose updated to cite [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2 (Maturity assessment) as the canonical reference. Three per-tier next-step section headers updated (`Tier 2 (Developing) → (Managed)`, `Tier 4 (Managed) → (Quantitatively Managed)`, `Tier 5 (Optimising) → (Optimized)`). Per-doc `1.0.2 → 1.0.3`.

2. [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md):65 DTI Thresholds replaced from 4-tier variant (Developing/Managed/Integrated/Optimized) to **CMMI 5-tier** with even 1.0-band thresholds: `0.0-0.9 = Initial`; `1.0-1.9 = Managed`; `2.0-2.9 = Defined`; `3.0-3.9 = Quantitatively Managed`; `4.0-5.0 = Optimized`. Cross-reference added to the canonical framework. Per-doc `1.0.0 → 1.0.1`.

The [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2 framework table is already CMMI-canonical (lines 41-47); no change required. **Both r1 FR-14 and r2 FR-114 close together**.

Library `2026.06.190 → 2026.06.191`; README `1.9.61 → 1.9.62`. Also carries PR #211's /validate-pr history row (0 findings).

---

## 2026-06-22, Library Version 2026.06.190, PR #211

**Closes FR-119** (medium): Risk Owner role unification across ERM standard and exception policy. Maintainer-approved per "decision 9": same role. Two coordinated edits:

1. [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §3 Risk Owner row: extended from five accountability actions to **six**, adding "validates risk assessments supporting exception requests (per [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §2: confirms residual exposure stays within the enterprise risk appetite when an exception is requested)." §9.2 evidence table extended with the corresponding sixth row mapping exception-request validation to "Risk acceptance approvals (per Risk Acceptance Procedure)" evidence type. Per-doc ERM standard `1.5.0 → 1.5.1`.
2. [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §2 Risk Owner row: extended to cross-reference the ERM standard's canonical definition, explicitly stating "Same role as the Risk Owner defined in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §3 (sixth accountability action: validates risk assessments for exception requests)." Also fixed grammar issue ("ensures that alignment" → "confirms alignment"). Per-doc exception policy `1.3.1 → 1.3.2`.

The unification closes the **last remaining item of Convergent Finding C1** (Risk Owner role insufficiency). C1 now fully closed: FR-115 (PR #197 register row), FR-116 (PR #198 cadence), FR-117 (PR #199 evidence map), FR-119 (this PR).

Library `2026.06.189 → 2026.06.190`; README `1.9.60 → 1.9.61`. Also carries PR #210's /validate-pr history row (0 findings).

---

## 2026-06-22, Library Version 2026.06.189, PR #210

**Closes FR-46 (Privacy Officer rename portion)** (medium). Maintainer-approved per "decision 6": "Privacy Officer" (used in ~50 corpus locations without the "Chief" prefix) is the same role as "Chief Privacy Officer" (the canonical role per [`governance/register-role-authority.md`](governance/register-role-authority.md):39). Corpus-wide regex sweep with negative lookbehind `(?<!Chief )Privacy Officer` → `Chief Privacy Officer` across **36 files**. Per-doc Version+Date patch-bumped for all 36 in the same commit. [`CHANGELOG.md`](CHANGELOG.md) historical entries excluded; `.working/` excluded.

**DPO scope assessment** (the second half of decision 6 — "may also be the same as DPO, needs assessment"): research subagent's assessment evidence strongly supports that **DPO and Chief Privacy Officer are the same role** under different names (canonical register has no separate DPO entry; 8+ corpus locations use `Privacy Officer / DPO` as synonyms; [`ai/charter-ai-governance-council.md`](ai/charter-ai-governance-council.md):62 and [`docs/portal.md`](docs/portal.md):411 explicitly write `Chief Privacy Officer (or Data Protection Officer)`; jurisdictions like Brazil/India/Kenya/Malaysia/Nigeria/Philippines/Thailand mandate DPO appointment as the privacy lead — the same accountability the corpus assigns to its Chief Privacy Officer). One outlier ([`supply-chain/procedure-supplier-onboarding-security-review.md`](supply-chain/procedure-supplier-onboarding-security-review.md):135 escalation chain "DPO → CISO → Chief Privacy Officer") treats them as distinct hierarchy levels and appears to be a drafting error. **DPO consolidation is queued as a separate decision; named options surfaced for maintainer go-ahead.** Glossary, jurisdiction annexes, and "CIO (acting DPO)" pattern require care.

Library `2026.06.188 → 2026.06.189`; README `1.9.59 → 1.9.60`. Carries PR #209's /validate-pr history row (0 findings).

---

## 2026-06-22, Library Version 2026.06.188, PR #209

**Closes FR-52** (medium): review-frequency `Annual and upon ...` form. Maintainer-approved per "decision 5": canonical form is "annually AND on material change" (both triggers required, not either-or). Two documents in the corpus used the OR variant ("Annual or upon ..."); both converted to AND.

Files modified:
- [`dev-security/standard-security-baseline-and-standards-reference.md`](dev-security/standard-security-baseline-and-standards-reference.md):12 — "Annual or upon material threat, regulatory, or framework change" → "Annual and upon material threat, regulatory, or framework change". Per-doc Version `1.1.0 → 1.1.1`.
- [`security/sop-security-ticket-reporting-scheme.md`](security/sop-security-ticket-reporting-scheme.md):12 — "Annual or upon significant change to vendor or tooling landscape" → "Annual and upon significant change to vendor or tooling landscape". Per-doc Version `1.1.0 → 1.1.1`.

The semantic shift is meaningful: AND requires both triggers (the annual cycle AND a material change event); OR allowed either to trigger a review independently. The AND form is consistent with the rest of the corpus and matches the project's review-cadence discipline.

Also carries PR #208's /validate-pr history row. Library `2026.06.187 → 2026.06.188`; README `1.9.58 → 1.9.59`.

---

## 2026-06-22, Library Version 2026.06.187, PR #208

**Closes FR-51** (medium): ISO 27001 Annex-form sweep. Maintainer-approved per "decision 4": canonical form is `Annex A.X` (with prefix), matching ISO 27001:2022 publisher convention. Corpus-wide sweep across **12 files** (7 corpus + 5 pack SKILL.md) converted `27001 A.X` → `27001 Annex A.X` (preserving multi-control `/`-separated lists by prefixing only the first control). Pattern was tightly anchored on `\b27001(:YYYY)? A\.[0-9]` to avoid false positives on non-ISO-27001 `A.X` occurrences (e.g., ISO 42001, ISO 27017, ISO 27018, ISO 27701, all of which were verified absent from `27001-prefixed A.X` matches). 7 corpus files received per-doc Version+Date patch bumps; pack README bumped `1.44.0 → 1.44.1` to cover the 5 SKILL.md edits which lack per-doc metadata. Also carries PR #207's `/validate-pr` history row (0 findings). Library `2026.06.186 → 2026.06.187`; README `1.9.57 → 1.9.58`.

---

## 2026-06-22, Library Version 2026.06.186, PR #207

**Closes FR-50** (medium): NIST citation format sweep. Maintainer-approved per "decision 3": canonical form is `Rev. N` (with period), matching NIST's publisher convention. Corpus-wide sweep across **50 corpus files** converted `Rev N` (no period) → `Rev. N` (with period) for 91 occurrences. Files include the canonical-citations register itself, governance registers (document-index, glossary, coverage-gaps, matrices, worklists), domain standards (security, dev-security, supply-chain, operations, OT, ai, compliance, resilience, privacy), and specification-master-project. The `compliance/register-compliance-obligations-template.md:56` example "NIST SP 800-53 Rev. 4 → Rev. 5" was reworded to a generic "for example, a NIST SP publishes a new revision" framing because the standards-currency gate (correctly) flagged "Rev. 4" as superseded. [`CHANGELOG.md`](CHANGELOG.md) historical entries deliberately preserved as written (frozen audit-trail content per artefact-and-branch-discipline). Per-doc version bumps applied to all 50 touched files (typically patch-level). Also carries PR #206's `/validate-pr` history row (0 findings). Library `2026.06.185 → 2026.06.186`; README `1.9.56 → 1.9.57`. Future Pass-1 verifications should recognize that the canonical-citations register's example line is the source of truth for citation form.

---

## 2026-06-22, Library Version 2026.06.185, PR #206

**Closes FR-87** (SSRF range list completion) **and FR-88** (cipher suite enumeration). Maintainer-approved per "decision 2".

**FR-87** ([`dev-security/claude-rules/core/owasp.md`](dev-security/claude-rules/core/owasp.md):145): SSRF range list completed in canonical CIDR notation with RFC citations. IPv4 ranges restated (`10.0.0.0/8` RFC 1918, `172.16.0.0/12` RFC 1918 with explicit `172.16-31.x.x` span note, `192.168.0.0/16` RFC 1918, `169.254.0.0/16` link-local RFC 3927 with `169.254.169.254` cloud-metadata note, `127.0.0.0/8` loopback RFC 1122, `100.64.0.0/10` CGNAT RFC 6598). IPv6 ranges added (`::1/128` loopback, `fc00::/7` ULA RFC 4193, `fe80::/10` link-local RFC 4291 with `fd00:ec2::254` AWS IMDS IPv6 note). The previous list missed IPv6 entirely and used non-canonical `172.16.x.x` notation (suggesting only /16; should be /12 spanning 16-31).

**FR-88** ([`dev-security/standard-api-security.md`](dev-security/standard-api-security.md):110): cipher row enumerated TLS 1.3 AEAD suites per NIST SP 800-52 Rev. 2 §3.3.1: `TLS_AES_256_GCM_SHA384` (recommended), `TLS_AES_128_GCM_SHA256`, `TLS_CHACHA20_POLY1305_SHA256`. Rejected suite categories enumerated (RC4, 3DES, MD5-based, CBC-mode without AEAD, RSA key-exchange without forward secrecy, anonymous DH).

Pack `1.43.0 → 1.44.0` (minor; both FRs close in pack core/owasp.md + dev-security standard surfaces); new pack version-history row added. Per-doc api-security `0.0.3 → 0.0.4`. Also carries PR #205's /validate-pr history row (0 findings). Library `2026.06.184 → 2026.06.185`; README `1.9.55 → 1.9.56`.

---

## 2026-06-22, Library Version 2026.06.184, PR #205

**Closes FR-81 fully** (medium). Pack [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md):58 TLS row updated from `TLS 1.3 (preferred), TLS 1.2 (minimum)` → `TLS 1.3 (or stronger), aligned to security/policy-encryption-and-key-management.md §1 (Encryption standards) canonical mandate`; TLS 1.2 added to Prohibited column. Same alignment pattern as PR #193 (ZTA framework) and PR #201 (dev-security standards). Maintainer-approved per "decision 1" on the deferred-items list. **FR-81 is now fully closed** across all three originally-named surfaces. Pack `1.42.0 → 1.43.0` (minor; FR-81 third-surface close); new pack version-history row added. Also carries (a) PR #204's `/validate-pr` history row (3 in-window findings), and (b) the three fixes for those findings: stale "(12 items)" count → "(10 items)" with reconciled bucket math (9 ✅ + 1 ⚠️ = 10 active; FR-114 moved out of the active-verified list to live in the maintainer-decided table only); in-flight self-correction prose in PR #204's CHANGELOG entry rewritten to clean prose; pack-README version-history row added for 1.43.0. Library `2026.06.183 → 2026.06.184`; README `1.9.54 → 1.9.55`.

---

## 2026-06-22, Library Version 2026.06.183, PR #204

**Pass-1 verification of the 2026-06-22 fitness review (r2)**. Twelfth PR in the day's batch. [`.working/fitness-reviews/2026-06-22-r1.md`](.working/fitness-reviews/2026-06-22-r1.md) gains a new §9 (Pass-1 Verification Results) with per-finding verdict tags per the `library-fitness-review` SKILL's Pass-1 protocol. Aggregate: 10 active verifications (9 ✅ confirmed-as-stated for FR-112, FR-120, FR-121, FR-122, FR-123, FR-124, FR-125, FR-126, FR-131; plus 1 ⚠️ confirmed-with-modification for FR-118 — broader divergence than originally framed), 9 ✅ batch-tagged for findings already closed in overnight PRs (#193-#203), 3 maintainer-decided (FR-119 same role, FR-130 keep README first, FR-14/FR-114 CMMI canonical), 0 ❌, 0 🤔. Totals to 22 FRs matching the §8 backlog table. One severity escalation flagged: **FR-124 Medium → High** (the access-revocation contradiction has a 12-month risk-exposure window). One scope expansion flagged: **FR-118 ⚠️ broader divergence** (ERM standard §6 and §7 are themselves inconsistent in addition to the cross-doc divergence with the procedure). Per-doc fitness-reviews/history.md `1.2.3 → 1.3.0` (minor; Pass-1 milestone). Also carries PR #203's /validate-pr history row (0 findings). Library `2026.06.182 → 2026.06.183`; README `1.9.53 → 1.9.54`. Pass-2 (maintainer-interactive bucket processing) is the next step.

---

## 2026-06-22, Library Version 2026.06.182, PR #203

Closes **FR-133** (FYI). Eleventh overnight-batch PR. [`docs/decision-tree.md`](docs/decision-tree.md) §4.1 (Privacy / jurisdictional) restructured: the jurisdiction-index pointer is now a stand-alone paragraph at the top of the section noting the full library coverage (currently 25 jurisdictions including non-Anglosphere regions across Asia-Pacific, Latin America, Middle East, Africa, and Europe); the four Common Anglosphere selections (EU/UK/US/Canada) remain as a representative-not-exhaustive list; a closing sentence names example non-Anglosphere annexes (Australia, Singapore, India, Brazil, Japan, South Korea, China, and others) and redirects to the jurisdiction index for the complete list. Resolves the FR-133 finding by surfacing the index pointer prominently rather than burying it in the last bullet. Per-doc decision-tree `1.0.3 → 1.0.4` (patch). Also carries (a) PR #202's /validate-pr history row (0 in-window findings + 1 out-of-window observation), and (b) the out-of-window cleanup: TODO "Next-up recommendations" §C1/C2/C3 narrative updated to reflect overnight closures (C1 3 of 4 closed, C3 fully closed, C2 6 deferred). Library `2026.06.181 → 2026.06.182`; README `1.9.52 → 1.9.53`.

---

## 2026-06-22, Library Version 2026.06.181, PR #202

Overnight session wrap-up PR. Updates [`.working/overnight-pr.md`](.working/overnight-pr.md) with the final build-progress list (9 PRs / 8 full FR closures + 1 partial closure, in order: PR #193 FR-127 / PR #194 FR-128 / PR #195 FR-129 / PR #196 FR-113 / PR #197 FR-115 / PR #198 FR-116 / PR #199 FR-117 / PR #200 FR-132 / PR #201 FR-81 partial), the files-modified inventory (corpus content + working-state + generated artefacts), the files-NOT-touched inventory (pack rules + spec files + audit gates), and the open-ambiguities-surfaced list for maintainer review (9 items: FR-81 third surface, FR-87/88 pack edits, FR-50 NIST citation, FR-51 ISO Annex form, FR-52 and/or, FR-46 Chief role-name, FR-104 regulation descriptors, FR-130 portal entry-point reorder, Privacy Officer scope). Status remains `in-flight` per the protocol (`done` causes gate failure; the morning-processing PR by the maintainer will route content and transition to `stub`). Also carries PR #201's /validate-pr history row (0 findings). Library `2026.06.180 → 2026.06.181`; README `1.9.51 → 1.9.52`.

---

## 2026-06-22, Library Version 2026.06.180, PR #201

Partially closes **FR-81** (medium). Ninth overnight-batch PR. Two dev-security standards aligned to the canonical [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md):54 §1 (Encryption standards) TLS 1.3+ mandate: [`dev-security/standard-developer-security-requirements.md`](dev-security/standard-developer-security-requirements.md):151 changed from `TLS 1.2 (minimum), TLS 1.3 (preferred)` → `TLS 1.3 (or stronger), aligned to ...`; [`dev-security/standard-api-security.md`](dev-security/standard-api-security.md):109 changed from `TLS 1.2 minimum; TLS 1.3 preferred; HSTS ...` → `TLS 1.3 or stronger (aligned to ...); HSTS ...`. The encryption policy is the canonical authority (PR #193 also aligned the ZTA framework to it for FR-127). FR-81's third surface is the pack [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md), which carries the same "TLS 1.2 minimum, 1.3 preferred" framing; **that one is deferred** (pack-rule edit considered approval-needed for the overnight batch). FR-81 marked partial-close in TODO. Per-doc bumps: developer security requirements `1.0.1 → 1.0.2`; API security standard `0.0.2 → 0.0.3`; both Dates `2026-05-28 → 2026-06-22`. Also carries PR #200's /validate-pr history row (0 findings). Library `2026.06.179 → 2026.06.180`; README `1.9.50 → 1.9.51`.

---

## 2026-06-22, Library Version 2026.06.179, PR #200

Closes **FR-132** (low). Eighth overnight-batch PR. [`docs/decision-tree.md`](docs/decision-tree.md) §2.1 Orientation list refined: item 1 (README) and item 2 (adopter-guide) get an inline note that acronyms are expanded at first occurrence (per PR #172 / FR-4, PR #179 / FR-106, PR #196 / FR-113 acronym-polish work); item 3 (glossary) gets a note that it's reserved for deeper-domain documents in §2.2+ where the orientation files' inline expansion no longer applies. Resolves the FR-132 finding (glossary at item 3 of 4 in the orientation block) by adopting the recommendation's second option ("note that recent improvements reduced acronym density in earlier-read docs") rather than reordering the entry sequence (which would conflict with the existing intentional ordering: README → adopter-guide → glossary as a "skim → orient → reference" pattern). Per-doc decision-tree `1.0.2 → 1.0.3` (patch). Also carries PR #199's /validate-pr history row (0 findings). Library `2026.06.178 → 2026.06.179`; README `1.9.49 → 1.9.50`.

---

## 2026-06-22, Library Version 2026.06.178, PR #199

Closes **FR-117** (medium). Seventh overnight-batch PR. [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §9 (Evidence requirements) restructured: existing list moved to §9.1 (General evidence catalogue); new §9.2 (Risk Owner evidence by accountability action) adds an explicit table mapping each of the five Risk Owner accountability actions defined in §3 (confirms risk statement / selects treatment option / owns treatment plan and target dates / monitors residual exposure / reports status per §8.1 cadence) to the evidence type from §9.1 that proves execution. Mechanical mapping using existing canonical sources: §3 Risk Owner row (definition added in PR #178), §6 treatment options (the six-option set Avoid/Mitigate/Transfer/Accept/Exploit/Enhance), §8.1 cadence (refined in PR #198). No new policy decisions. Per-doc ERM standard `1.4.2 → 1.5.0` (minor; new subsection). Also carries PR #198's /validate-pr history row (0 findings). Library `2026.06.177 → 2026.06.178`; README `1.9.48 → 1.9.49`. Convergent Finding C1 progress: FR-115 (PR #197), FR-116 (PR #198), FR-117 (this PR) closed; FR-119 deferred (needs decision).

---

## 2026-06-22, Library Version 2026.06.177, PR #198

Closes **FR-116** (medium). Sixth overnight-batch PR. [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §8.1 extended with explicit Risk Owner review cadences per score band, matching the §5.2 "Score thresholds and required response" table's review-interval column (Low: annually; Moderate: quarterly; High: monthly; Critical: monthly per the existing §8.1 position). The previous §8.1 specified only Critical (monthly) explicitly; the other bands' cadences were implicit from §5.2 but not affirmed in §8.1 directly. The fix is mechanical alignment: Low/Moderate/High cadences taken verbatim from the §5.2 table; Critical's monthly cadence preserved from the existing §8.1 line. Per-doc ERM standard `1.4.1 → 1.4.2` (patch). Also carries PR #197's /validate-pr history row (0 findings). Library `2026.06.176 → 2026.06.177`; README `1.9.47 → 1.9.48`. Convergent Finding C1 progress: FR-115 closed in PR #197, FR-116 closed here; FR-117 (evidence expectations) still doable; FR-119 deferred.

---

## 2026-06-22, Library Version 2026.06.176, PR #197

Closes **FR-115** (high). Fifth overnight-batch PR. Adds the **Risk Owner** row to [`governance/register-role-authority.md`](governance/register-role-authority.md) §Authority register. The role was added to [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §3 in PR #178 but did NOT propagate to the canonical Role Authority Register; the register cannot serve as a single source of truth for the role's RACI until it carries the row. The new register row uses the verbatim "Primary Accountability" text from the ERM standard §3 and adds a "Typical Approval Authority" cell with the three accountability surfaces (treatment-option selection, treatment-plan ownership, status reports to the ERC). Also added a reciprocal cross-reference from the ERM standard §3 Risk Owner row back to the register's canonical definition (per the FR-115 recommendation). Per-doc bumps: register `1.3.2 → 1.4.0` (minor; new role row); ERM standard `1.4.0 → 1.4.1` (patch; cross-reference added); both Dates `2026-06-21 → 2026-06-22`. Also carries PR #196's /validate-pr history row (0 findings). Library `2026.06.175 → 2026.06.176`; README `1.9.46 → 1.9.47`. Convergent Finding C1 (Risk Owner role insufficiency) partial close: FR-115 done; FR-116/FR-117 remain (cadence and evidence expectations); FR-119 needs decision (different responsibility set in exception policy).

---

## 2026-06-22, Library Version 2026.06.175, PR #196

Closes **FR-113** (medium). Fourth overnight-batch PR. [`README.md`](README.md) Repository Structure block: expanded the **CAPA** acronym to "CAPA (Corrective and Preventive Action)" at first occurrence (line 108) and the **SIEM** acronym to "SIEM (Security Information and Event Management)" at first occurrence (line 123). Restores the acronym-first-occurrence-expansion pattern PRs #172 and #179 established. Also carries (a) PR #195's /validate-pr history row (0 in-window findings + 1 out-of-window observation), and (b) the out-of-window cleanup the observation surfaced: [`.working/fitness-reviews/history.md`](.working/fitness-reviews/history.md) backlog table FR-127/128/129 rows had stale `pending` / `— PR` cells despite the three FRs closing in PRs #193/#194/#195; rotated to `closed` with the closing-PR link. Pre-existing discipline gap (the rotation wasn't applied when those FRs closed earlier in the cascade); mechanical cleanup. Library `2026.06.174 → 2026.06.175`; README `1.9.45 → 1.9.46`.

---

## 2026-06-22, Library Version 2026.06.174, PR #195

Closes **FR-129** (high[critical]). Third overnight-batch PR. [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md):83 internal audit reports retention raised from `5 years` to `7 years`, aligning the register with the canonical [`compliance/standard-internal-audit.md`](compliance/standard-internal-audit.md):360 §8.3 (Evidence retention) which mandates a 7-year minimum for audit working papers, evidence, draft findings, management responses, and final reports. Closes the second audit-evidence chain break (after FR-128's CAPA row in PR #194). The procedure-side retention also matches: [`compliance/procedure-audit-planning.md`](compliance/procedure-audit-planning.md):447 mandates 7y. Per-doc retention register `1.0.3 → 1.0.4` (patch). Also carries PR #194's /validate-pr history row (0 findings). Library `2026.06.173 → 2026.06.174`; README `1.9.44 → 1.9.45`.

---

## 2026-06-22, Library Version 2026.06.173, PR #194

Closes **FR-128** (high[critical]). Second overnight-batch PR. [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md):66 CAPA records retention raised from `5 years after closure` to `7 years after closure`, aligning the register with the canonical [`compliance/procedure-capa.md`](compliance/procedure-capa.md):454 §12 (Evidence retention) which mandates a 7-year minimum. The previous 5-year retention created an audit-evidence chain break: control-testing evidence retention is 7y (raised in PR #179) but CAPA records (which document remediation of audit findings) were still 5y; the chain would break at year 5 when CAPA expires while the control test it remediated remains. Per-doc retention register `1.0.2 → 1.0.3` (patch); Date `2026-06-21 → 2026-06-22`. Also carries (a) PR #193's /validate-pr history row (1 in-window finding bundled into this PR per the batching rule), and (b) PR #193's /validate-pr finding fix: TODO.md "Next-up recommendations" section had FR-127 still listed despite FR-127 closing in PR #193; removed the stale item, renumbered items 5+ accordingly. Library `2026.06.172 → 2026.06.173`; README `1.9.43 → 1.9.44`.

---

## 2026-06-22, Library Version 2026.06.172, PR #193

Closes **FR-127** (high[critical]). First overnight-batch PR. [`security/framework-zero-trust-architecture.md`](security/framework-zero-trust-architecture.md) Pillar 3 (Networks) Encryption-in-transit row updated from `TLS 1.2 or above` to `TLS 1.3 or stronger`, aligning the ZTA framework's maturity expectation with the canonical [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md):54 mandate. The previous TLS 1.2 floor was below the encryption policy's TLS 1.3+ mandate; TLS 1.2 has reached end-of-life guidance from NIST and OWASP 2025. Per-doc ZTA framework `0.0.2 → 0.0.3` (patch). Also carries PR #192's /validate-pr history row (0 findings) per the new batching rule. Library `2026.06.171 → 2026.06.172`; README `1.9.42 → 1.9.43`. Overnight session active per [`.working/overnight-pr.md`](.working/overnight-pr.md) (Status: in-flight).

---

## 2026-06-22, Library Version 2026.06.171, PR #192

**Changed.** Codified the **batching-into-the-next-PR rule** in both [`/validate`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) and [`/validate-pr`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) SKILL.md surfaces plus their slash commands ([`.claude/commands/validate.md`](.claude/commands/validate.md), [`.claude/commands/validate-pr.md`](.claude/commands/validate-pr.md)). The naive interpretation of "every merge gets /validate-pr; every invocation gets a history row" creates a recursive PR cascade: each PR's /validate-pr generates a new PR (for the row or for hot-fixes), which itself triggers /validate-pr. The day's #187 → #188 → #189 → #190 cascade made the recursion apparent. New rule: /validate-pr outputs are batched into the next PR whatever its substantive purpose. (1) Zero-finding invocations append the history row to the next PR's diff. (2) Findings-producing invocations bundle the fix(es) into the next PR (do NOT open a dedicated hot-fix PR; the next PR absorbs the fixes alongside its own work). A findings-producing `/validate` (corpus-wide sibling) may still warrant its own close-out PR when findings are numerous or coherent enough; for /validate-pr the bundle is always the default. Maintainer direction: "If there's nothing to actually fix or correct, then keep findings to bundle into the next PR whatever it is. If there are multiple PRs queued, then the fix of anything found in validate-pr can be bundled into the next PR whatever it is. Only the full validate should have its own PR for fixing multiple things." This PR also carries PR #191's zero-finding /validate-pr history row (the first application of the new batching rule). Pack `1.41.0 → 1.42.0` (minor; new SKILL sub-section). Library `2026.06.170 → 2026.06.171`; README `1.9.41 → 1.9.42`.

---

## 2026-06-22, Library Version 2026.06.170, PR #191

`.working/` changes for local project: appended the history row recording the `/validate-pr` run against PR #190 (0 findings; cascade terminated). Subagent A deep-read all 14 PR #190 touched files plus the cross-reference check; verified parity between the two new "Surfacing findings in chat" SKILL.md sections, the slash-command parallel paragraphs, the UTC convention citations in [`.claude/CLAUDE.md`](.claude/CLAUDE.md), and the version-bump consistency across all surfaces. PR #190's structural fix (full-date "Originating run" column in [`.working/fitness-reviews/history.md`](.working/fitness-reviews/history.md) + UTC convention + chat-surfacing discipline) resolved the r1/r2 cross-date ambiguity at the convention level, terminating the three-PR cascade (#187 → #188 → #189 → #190 = 2 + 2 + 2 + 0 findings respectively). Library `2026.06.169 → 2026.06.170`; README `1.9.40 → 1.9.41`. No corpus content changes; housekeeping PR for the /validate-pr record.

---

## 2026-06-22, Library Version 2026.06.169, PR #190

**Fixed.** Three bundled threads: (1) hot-fix the two `/validate-pr` findings on PR #189 (both multi-surface incompleteness; PR #189's r2→r1 relabel did not propagate to [`.working/fitness-reviews/history.md`](.working/fitness-reviews/history.md) line 22 narrative or the H[critical] backlog table's "Originating run" column rows 43-48; fixed by changing "For run r2" to "For the 2026-06-22 run" and switching all "Originating run" cells to full dates `2026-06-21` / `2026-06-22` for unambiguous cross-date disambiguation). (2) Codified the **UTC convention** in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (new "Date and timezone convention" section): the assistant works in UTC for all date-bearing fields and "today" calculations; maintainer's local timezone (America/Toronto, GMT-5 standard / GMT-4 daylight) is noted but does not drive metadata dates. Gate 31 timezone-boundary edge case on PR #187 is the recorded justification. (3) Codified the **chat-surfacing discipline** in both [`/validate`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) and [`/validate-pr`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) SKILL.md surfaces plus their slash commands ([`.claude/commands/validate.md`](.claude/commands/validate.md), [`.claude/commands/validate-pr.md`](.claude/commands/validate-pr.md)): when findings exist, surface them prominently in chat (per-finding ruleId, severity, `path:line`, evidence quote, impact, recommendation, in-window classification) rather than burying them in `.working/` archives or [`CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md). Pack `1.40.2 → 1.41.0` (minor; new SKILL section). Library `2026.06.168 → 2026.06.169`; README `1.9.39 → 1.9.40`. Recorded the `/validate-pr` on PR #189 run at [`.working/validate-pr/2026-06-22-PR-189.md`](.working/validate-pr/2026-06-22-PR-189.md). Third consecutive findings-producing /validate-pr (#187, #188, #189); the cascade should converge with PR #190's /validate-pr (structural fix to the r1/r2 cross-date ambiguity).

---

## 2026-06-22, Library Version 2026.06.168, PR #189

**Fixed.** Hot-fix for the two `/validate-pr` findings on PR #188. Subagent A surfaced (1) multi-surface incompleteness: the new fitness-review file was named [`2026-06-22-r1.md`](.working/fitness-reviews/2026-06-22-r1.md) (per the README's per-date `rN` convention) but the report's H1, "Run ordinal" line, and the [`history.md`](.working/fitness-reviews/history.md) row all labelled the run "r2" (cumulative interpretation). Per-date is the documented convention; re-labelled the 8 internal "r2" references in [`.working/fitness-reviews/2026-06-22-r1.md`](.working/fitness-reviews/2026-06-22-r1.md) to "r1" and disambiguated cross-date references via dates (e.g., "FR-14 from r1" became "FR-14 from the 2026-06-21 run"); updated the history.md row's Run column to r1 and replaced the "(this PR)" placeholder with the PR #188 link. (2) Stale prose reference: the pack [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) 1.40.1 version-history row credited the Date-bump catch to "gate 31 caught it via the second `/validate-pr` cycle"; the [`/validate-pr` per-PR record](.working/validate-pr/2026-06-22-PR-187.md) explicitly says gate 31 did NOT fire (timezone-boundary edge case, with both commit-date and Date-field at `2026-06-21` at PR #187 merge time; lag opened only after midnight UTC). Reworded the 1.40.1 row's catch-attribution to credit /validate-pr deep-read; added a 1.40.2 row documenting the correction. Recorded the `/validate-pr` on PR #188 run: history row at [`.working/validate-pr/history.md`](.working/validate-pr/history.md) plus per-PR detail file at [`.working/validate-pr/2026-06-22-PR-188.md`](.working/validate-pr/2026-06-22-PR-188.md). Second consecutive findings-producing /validate-pr; the discipline is working as designed (each meta-PR creates opportunities for the next /validate-pr to catch). Pack `1.40.1 → 1.40.2`; library `2026.06.167 → 2026.06.168`; README `1.9.38 → 1.9.39`.

---

## 2026-06-22, Library Version 2026.06.167, PR #188

**Changed.** End-of-evening close-out PR. Three independent threads bundled because they share the "end of day" framing: (1) two hot-fixes for the `/validate-pr` findings on PR #187; (2) recording the `/fitness` r2 review (10 personas, 27 findings, 22 new FR IDs FR-112 through FR-133); (3) `/validate-pr` history record for PR #187 itself (the belated invocation after the no-skip-discretion policy correction). **Validate-pr hot-fix 1** (multi-surface incompleteness): the "no orchestrator-side skip discretion" wording on [`dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) line 23 and [`.claude/commands/validate-pr.md`](.claude/commands/validate-pr.md) line 15 diverged (different rejected-rationale lists; different "proof-of-discipline" framing); slash command now matches SKILL.md verbatim. **Validate-pr hot-fix 2** (per-document version-bump omission): [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) Date bumped `2026-06-21 → 2026-06-22`; Version `1.40.0 → 1.40.1`; version-history row added. PR #187 commit message said "Date stamp 2026-06-22 (policy correction landed after midnight UTC)" but the Date field stayed at `2026-06-21` — a timezone-boundary edge case in gate 31 (commit and Date were both 2026-06-21 at merge time; lag opened only post-midnight UTC). **Fitness r2 record**: report file at [`.working/fitness-reviews/2026-06-22-r1.md`](.working/fitness-reviews/2026-06-22-r1.md) (293 lines, 8 sections plus a Final Assessment); history row appended to [`.working/fitness-reviews/history.md`](.working/fitness-reviews/history.md) with full summary; 6 H[critical] r2 rows added to the file's H[critical] backlog table. Aggregate: 6 H[critical] + 8 H + 11 M + 2 L/FYI = 27 findings. P5 Policy Editor and P9 Privacy/DPO both returned 0 findings. Three Convergent Findings dominate: C1 Risk Owner role insufficiency (4 FRs), C2 Emergency-access trigger ambiguity (6 FRs), C3 Retention chain breaks (2 FRs). All findings `verification: unverified` pending Pass-1; deferred to next session. **Validate-pr record for PR #187**: per-PR detail file at [`.working/validate-pr/2026-06-22-PR-187.md`](.working/validate-pr/2026-06-22-PR-187.md) with full Subagent A SARIF-lite findings, cross-reference check, orchestrator triage, and discipline-observation notes (this is the first /validate-pr invocation that surfaced findings; the gate-31 timezone-boundary edge case is documented for future reference). **TODO updates**: new "Fitness review backlog (from r2, unverified pending Pass-1)" section in [`TODO.md`](TODO.md) with all 22 FR-112 through FR-133 entries grouped by severity tier, the three Convergent Findings flagged at the top, the three Standardization recommendations surfaced for maintainer review, and the top-5 next-up recommendations. Backlog totals updated: 91 total open items (69 r1 + 22 r2). Pack `1.40.0 → 1.40.1`; library `2026.06.166 → 2026.06.167`; README `1.9.37 → 1.9.38`.

---

## 2026-06-22, Library Version 2026.06.166, PR #187

**Changed.** Codified the **no orchestrator-side skip discretion** discipline across the validation-pr surfaces after a maintainer-flagged policy deviation: during the previous batch, the orchestrator deliberately skipped `/validate-pr` invocations on PRs #185 and #186 citing "circular" / "redundant" rationale. The maintainer rejected the framing , the discipline says every merge gets `/validate-pr`, and the orchestrator does NOT have unilateral discretion to skip a QA step. Three surfaces updated with explicit "no skip" language: [`dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) When-to-Use; [`.claude/commands/validate-pr.md`](.claude/commands/validate-pr.md) Termination; [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) Prohibited-anti-patterns gains a new anti-pattern for "Orchestrator-side judgment-call skipping of mandatory QA/testing steps". Same anti-pattern mirrored to [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](.claude/rules/governance/ai-assistant-workflow-disciplines.md). Also fixed a docstring staleness in [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py) (claimed "Currently only validation-sweep" has both SKILL.md and slash command but PAIRS now has 3 pairs); rewrote to be generic. Captured as new failure-mode class C-9 in [`.working/hallucination-metrics.md`](.working/hallucination-metrics.md) with future-gate candidate (mechanical check that every merged PR appears in [`.working/validate-pr/history.md`](.working/validate-pr/history.md)). Pack `1.39.0 → 1.40.0`; library `2026.06.165 → 2026.06.166`; README `1.9.36 → 1.9.37`. Date stamp 2026-06-22 (policy correction landed after midnight UTC).

---

## 2026-06-21, Library Version 2026.06.165, PR #186

Sweep 17 iteration 1 close-out. First full `/validate` sweep since Sweep 16's close-out (PR #181); 4 intervening substantive PRs (#182, #183, #184, plus #185 housekeeping). Three subagents dispatched in parallel (A, B, C); Subagent A surfaced 1 in-window finding, Subagent C surfaced 1 in-window finding (plus 4 positive verification notes and 1 future-gate candidate), Subagent B surfaced 0 findings (high-confidence clean bill on corpus-wide stale-reference search). Fixes: (A) [`dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) line 151's forward-reference "queued for PR #185" updated to "queued for PR #186" (PR #185 became the housekeeping recording PR; /retro skill is now queued for PR #186); (C) [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py) PAIRS registry extended with the `validation-sweep-pr-scoped` + `/validate-pr` pair. Gate 44 was not previously checking step-parity on the new skill (real defect from PR #183, which added the skill but forgot to register it for the gate). Gate 44 now actively validates 3 paired surfaces; the new pair's 5-step structure is verified step-aligned. **Future-gate candidate from Subagent C**: collection-enumeration auto-detection — gate 41 could surface unmapped collections to reduce manual maintenance. Captured for consideration. Sweep history row appended; detail file at [`.working/validate-sweeps/2026-06-21-sweep17-iter1.md`](.working/validate-sweeps/2026-06-21-sweep17-iter1.md). Library `2026.06.164 → 2026.06.165`; README `1.9.35 → 1.9.36`.

---

## 2026-06-21, Library Version 2026.06.164, PR #185

`.working/` changes for local project: recorded the first real `/validate-pr` invocation (run against PR #184, 0 findings) by appending a row to [`.working/validate-pr/history.md`](.working/validate-pr/history.md). Library `2026.06.163 → 2026.06.164`; README `1.9.34 → 1.9.35`. No corpus content changes; this is the per-PR record artefact for the just-merged PR #184's `/validate-pr` sweep.

---

## 2026-06-21, Library Version 2026.06.163, PR #184

**Changed.** Extended the pack rule [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) §1 (Research-assistant discipline) with a new "Worker-brief template and hallucination-assessment update protocol" subsection. The new subsection codifies the discipline of maintaining a project-local worker-brief template the orchestrator uses as the starting point for every worker dispatch, plus the protocol for updating the template when a new failure class is caught at apply-time (log → classify fix → update inline or queue → reference from catch entry). This makes the research-assistant discipline self-improving: each new failure class observed becomes a permanent guard rail. **Added** the project's own worker-brief template at [`.working/worker-brief-template.md`](.working/worker-brief-template.md) v1.0.0 with initial guard rails derived from the four known apply-time-catch failure classes: (1) file-path confabulation (caught at PR #169 P1.3 boundary); (2) stale external-standard citations (caught at Sweep 15 — ISO/IEC 29134:2023 vs 2017); (3) wrong PR / FR cross-references (caught at PR #172 — FR-3 cited #158 vs actual #147); (4) absolute current library/README version numbers in drafts (recurring; worker drafts always drift). The template has DO and DO-NOT lists, per-PR-class overrides, and an assembly description. [`.claude/CLAUDE.md`](.claude/CLAUDE.md) summary extended to point at the template. Pack version `1.38.0 → 1.39.0`; library `2026.06.162 → 2026.06.163`; README `1.9.33 → 1.9.34`. No corpus content changes; this is a discipline calibration plus initial template artefact.

---

## 2026-06-21, Library Version 2026.06.162, PR #183

**Added.** New pack skill [`dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md`](dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) and the [`/validate-pr` slash command](.claude/commands/validate-pr.md): PR-scoped post-merge validation sweep that runs after every merge to catch per-PR drift before it compounds across subsequent PRs. Dispatches Subagent A on the just-merged PR's diff (same eight failure-mode classes as the corpus-wide [`validation-sweep` SKILL](dev-security/claude-rules/skills/validation-sweep/SKILL.md), scoped to the touched files), plus a lightweight cross-reference check on files that cite the touched files. Complements the corpus-wide `/validate` sweep (the two are not substitutes; they cover different scopes at different cadences). New working-state activity directory at [`.working/validate-pr/`](.working/validate-pr/) with [`README.md`](.working/validate-pr/README.md), [`history.md`](.working/validate-pr/history.md), and per-PR detail-file convention matching the existing [`.working/validate-sweeps/`](.working/validate-sweeps/) structure. PR workflow step 5a added in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) to mandate `/validate-pr` after every merge. First real per-PR sweep will land starting with FR-33 (P1.4b). Pack version `1.37.0 → 1.38.0`; library `2026.06.161 → 2026.06.162`; README `1.9.32 → 1.9.33`.

---

## 2026-06-21, Library Version 2026.06.161, PR #182

**Changed.** Corpus-wide count-genericization sweep queued by PR #181's close-out. **Assessment criterion**: a count-in-prose is a genericization candidate when (a) the items live in a different location (file, directory, or table) than the citing prose, AND (b) the canonical authority can grow or shrink, AND (c) the prose could be rewritten to point at the canonical authority generically without information loss. Counts co-located with their canonical authority (e.g., "ten persona reviewers" in `library-fitness-review` SKILL.md where the personas are listed in the same file) are NOT candidates: they're self-consistent and changing them is done in the same edit that changed the count anyway. **Findings**: across the active corpus (excluding `.working/`, `.git/`, and historical CHANGELOG entries), only **one** genericization candidate remained after PR #181's fix to skill-authoring SKILL.md: [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §5 line 64 said "The gates fall into seven functional categories". Although the categories themselves are listed in the same §5 (so technically co-located), the count introduces drift risk if a future gate fits a new category. Genericized to "The gates fall into the following functional categories:". Per-doc `1.14.0 → 1.14.1` (patch). **Negative findings (intentionally kept)**: "ten persona reviewers" in `library-fitness-review` SKILL.md (personas listed in same file; count is informative and stable); "five disciplines" in [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) (sections listed in same file); "207 controls across 17 domains" for CCM v4.1 (external authoritative count, not project-internal); "About 125 controls" for FedRAMP tiers (external authoritative count); "five categories" in [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) for the adversarial test suite (intra-document structure). [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated. Library `2026.06.160 → 2026.06.161`; README `1.9.31 → 1.9.32`.

---

## 2026-06-21, Library Version 2026.06.160, PR #181

Sweep 16 iteration 1 close-out. First `/validate` sweep since Sweep 15 (PR #167), covering 13 intervening PRs (#168-#180). Three subagents dispatched in parallel (A, B, C); Subagent A surfaced 1 in-window finding, Subagent B surfaced 1 in-window finding, Subagent C surfaced 0 findings (audit-programme integrity clean). Both findings are the **multi-surface incompleteness** class: an orchestrator updating one surface but missing paired narrative prose elsewhere. Fixes: (A) [`TODO.md`](TODO.md) line 22's Queued-sequence narrative refreshed from "PRs #142-#176 have closed 34 findings" to "PRs #142-#180 have closed 42 findings", with the recent-PRs list extended to name #177/#178/#179/#180; (B) [`dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md) line 26's "one of the seven governance rules" rewritten as "one of the governance rules under `dev-security/claude-rules/governance/`" — the count was the bug; the directory listing is the canonical authority and citing a count in prose creates a drift-prone paraphrase. Per the maintainer's direction during this sweep, finding B's resolution is a **genericization** rather than a re-count: the broader pattern (count-in-prose where the directory or table is the canonical authority) is queued as a follow-up corpus-wide sweep PR. Both findings logged as orchestrator-side oversights in [`.working/hallucination-metrics.md`](.working/hallucination-metrics.md) under the multi-surface incompleteness pattern. Library `2026.06.159 → 2026.06.160`; README `1.9.30 → 1.9.31`. Sweep history row appended to [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md); detail file at [`.working/validate-sweeps/2026-06-21-sweep16-iter1.md`](.working/validate-sweeps/2026-06-21-sweep16-iter1.md).

---

## 2026-06-21, Library Version 2026.06.159, PR #180

**Changed.** Extended the version-bump discipline from three surfaces (per-document `Version`, library CalVer, README `Version`) to four (adding per-document `Date`). Surfaced as a discipline gap by PR #179's gate-31 catch: the orchestrator bumped Version on six touched files but missed bumping Date on two of them ([`security/policy-information-security.md`](security/policy-information-security.md) Date lag 25 days; [`resilience/template-tabletop-exercise.md`](resilience/template-tabletop-exercise.md) Date lag 19 days). The recurring failure mode is "bump Version, forget Date" — and CI's gate 31 (document-date-staleness) caught it, but the cost was a re-run cycle. Adding Date to the explicit discipline checklist avoids the loop. The project-local [`.claude/CLAUDE.md`](.claude/CLAUDE.md) `## Version-bump discipline` section is expanded from three surfaces to four, with the operationalization checklist now four questions instead of three (the new question 1 reads "Did this commit change a versioned document's body? → Bump that document's Version **and** Date in this commit"). The pack rule [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) §3 (Apply-time worker correction) gains an explicit per-file metadata-bump check as a new numbered step, and the common-patterns enumeration is extended to call out "orchestrator bumping Version but missing Date" as a recurring failure mode worth designing out. The local-copy mirror at [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](.claude/rules/governance/ai-assistant-workflow-disciplines.md) is synced byte-for-byte. Pack version `1.36.0 → 1.37.0`; library `2026.06.158 → 2026.06.159`; README `1.9.29 → 1.9.30`. No corpus content changes; this is a process-discipline calibration.

---

## 2026-06-21, Library Version 2026.06.158, PR #179

Closes **FR-18** (medium) + **FR-25** (medium) + **FR-79** (medium) + **FR-105** (medium) + **FR-106** (medium) + **FR-110** (medium). Phase 1 P1.4a velocity bundle: six unrelated medium-tier findings shipped as one PR; FR-33 (high[critical] from the same originally-planned P1.4 bundle) split out to its own PR (P1.4b) per the "always split when in doubt" discipline (different severity tier; larger scope). FR-18 — [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §3.7 gains a new §3.7.1 anchoring the 180-day initial-term baseline as a library convention aligned with NIST SP 800-53 Rev 5 CA-6 ongoing-authorisation maintenance cycles and ISO/IEC 27001:2022 Clause 9.2 internal-audit cycles, so an exception's renewal point coincides with the next scheduled control-evidence refresh; adopters whose monitoring cadence differs may tune the base term with the §3.4 cumulative ceiling tuning proportionally. FR-25 — control-testing evidence retention raised from 5 to 7 years in both [`compliance/procedure-control-testing.md`](compliance/procedure-control-testing.md) §3.3 (with explicit cross-reference to [`governance/standard-records-retention-and-destruction.md`](governance/standard-records-retention-and-destruction.md)) and [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md) line 87; the previous 5-year floor sat below Sarbanes-Oxley §103 audit-evidence retention. FR-79 — [`resilience/template-tabletop-exercise.md`](resilience/template-tabletop-exercise.md) inject-schedule table replaces two occurrences of "Slack" (vendor product name) with "Chat / collaboration platform" (generic phrasing), matching the library's sanitisation convention. FR-105 — [`security/policy-information-security.md`](security/policy-information-security.md) line 23 normalises "NIST Cybersecurity Framework 2.0" to "NIST CSF 2.0" so the Purpose section matches the Framework Alignment table header at line 134 and the §8.4 in-prose reference. FR-106 — [`README.md`](README.md) line 109 expands the seven trade-programme acronyms (CTPAT, BASC, PIP, AEO, AEO-S, WCO SAFE, ISO 28000) at first occurrence and adds a "(logistics-specific; skip if not applicable)" marker so non-logistics newcomers know to bypass. FR-110 — [`docs/decision-tree.md`](docs/decision-tree.md) line 119 reframes the document-index reference from "the master navigation register" to "comprehensive machine-readable register" and explicitly redirects readers to [`docs/portal.md`](docs/portal.md) as the canonical navigation point per PR #156 (FR-2) and PR #165 (FR-56). Authored under the research-assistant + apply-time-correction discipline (PR #176); worker file-state quotes verified accurate during PR #178 CI wait per discipline #5 (background work during CI waits). Apply-time corrections were version-drift only (library `2026.06.151 → 2026.06.158` instead of worker-drafted `2026.06.151 → 2026.06.152`). [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated. Per-doc bumps: exception policy `1.2.0 → 1.3.0`; control-testing procedure `1.0.1 → 1.0.2`; retention schedule `1.0.1 → 1.0.2`; tabletop template `1.0.1 → 1.0.3` (two-step: 1.0.1 → 1.0.2 with the body change; then 1.0.2 → 1.0.3 with the Date refresh on the gate-31 catch-up commit); ISMS policy `1.3.0 → 1.3.2` (two-step: 1.3.0 → 1.3.1 with the body change; then 1.3.1 → 1.3.2 with the Date refresh on the gate-31 catch-up commit); decision tree `1.0.1 → 1.0.2`. Library `2026.06.157 → 2026.06.158`; README `1.9.28 → 1.9.29`. Backlog 75 → 69 open. **Gate-31 catch.** CI flagged that two of the six touched files ([`security/policy-information-security.md`](security/policy-information-security.md) Date `2026-05-27` and [`resilience/template-tabletop-exercise.md`](resilience/template-tabletop-exercise.md) Date `2026-06-02`) lagged by more than 1 day; the original commit bumped Version but missed Date. A follow-up commit on the same branch bumped both Dates to `2026-06-21` and bumped per-doc Version again per the version-bump-recency discipline. Catch logged in [`.working/hallucination-metrics.md`](.working/hallucination-metrics.md) as a CI-caught miss (not shipped).

---

## 2026-06-21, Library Version 2026.06.157, PR #178

Closes **FR-11** (medium) + **FR-12** (medium, within-document scope). Phase 1 P1.2 bundle. Two ERM-standard findings closed in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md). FR-11 — the §3 governance table did not define Risk Owner as a distinct role despite the §7.1 register-field schema referencing the role; a new §3 row defines Risk Owner with per-risk accountability scope (confirms statement, selects treatment, owns plan and target dates, monitors residual exposure, reports per §8 cadence) and explicit boundary clauses distinguishing the role from CRO (framework owner) and from Process/System Owners (operational identifiers). FR-12 — three within-document treatment-vocabulary divergences fixed: §5.2 line 119 "Treat and monitor" harmonised to "Mitigate and monitor" matching the canonical verb used in §6 and §5.2 line 120; §6's combined "Exploit / Enhance" row split into two self-contained rows so each opportunity-side treatment carries its own definition; §7.1 Treatment Option enum extended from five options to the full six (Enhance added) so the register-field enum matches §6 verbatim. Cross-document harmonisation against [`risk/procedure-risk-register.md`](risk/procedure-risk-register.md) (which uses a different six-option set including `Monitor` and `Further Analysis` instead of `Exploit` and `Enhance`) deferred to a follow-up PR pending maintainer decision on canonical authority. First Phase 1 bundle authored under the research-assistant + apply-time-correction discipline shipped in PR #176; the worker draft's file-state quotes were verified accurate at pre-verification time (during PR #176 CI wait), so apply-time corrections were limited to version-drift (library `2026.06.150 → 2026.06.157` instead of the worker-drafted `2026.06.151`, backlog `77 → 75` instead of the worker-drafted `85 → 83`). [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated to absorb the per-doc Version bump. Per-doc `1.3.4 → 1.4.0` (minor: structural role definition); library `2026.06.156 → 2026.06.157`; README `1.9.27 → 1.9.28`. Backlog 77 → 75 open.

---

## 2026-06-21, Library Version 2026.06.156, PR #177

**Added.** New "Phase 1 / Phase 2 execution plan" subsection in [`TODO.md`](TODO.md)'s Queued-sequence section. Rotates the Phase 1 (P1.2, P1.4, P1.5, P1.6, P1.7) and Phase 2 (P2.1-P2.15, 15 items) plan out of session memory and into the project's durable TODO file so the plan survives session boundaries. Each Phase 1 item references its FR-N targets and notes scope (single-doc, multi-FR cluster, or low-tier sweep); each Phase 2 item references its FR-N targets and notes that research is already prepared per the research-assistant discipline shipped in PR #176. The plan codifies the maintainer-directed pause point at end of Phase 2 (a `/fitness` run triages the post-Phase-2 backlog before Phase 3 is planned). The Queued-sequence narrative is also refreshed to reflect that PRs #142-#176 have closed 34 findings to date, with the most recent meta-PRs #173 (CHANGELOG backfill), #174 (skip-trailer retirement), #175 (DONE shortening), and #176 (workflow-disciplines pack rule) named alongside the fitness-remediation PRs. Library `2026.06.155 → 2026.06.156`; README `1.9.26 → 1.9.27`.

---

## 2026-06-21, Library Version 2026.06.155, PR #176

**Added.** New pack rule [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) (mirrored to [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](.claude/rules/governance/ai-assistant-workflow-disciplines.md)) covering five disciplines for an AI coding assistant driving multi-PR work over a long session: (1) research-assistant discipline — workers produce research files; the orchestrator authors all final prose after independently re-reading target files; worker claims (quoted lines, version numbers, PR cross-references, file paths, citation years) verified at apply-time before commit; (2) pipeline PR construction — parallel research, serial apply, CI gating between PRs; (3) apply-time worker correction — catch worker errors at apply-time and document them in the closing PR's CHANGELOG-detailed entry; (4) "always split when in doubt" PR discipline — default to separate PRs unless changes are tightly coherent (same conceptual theme, same files, same maintainer-direction line item); (5) background work during CI waits — read-only prep on the next PR (read research files, run pre-verification greps, confirm referenced file paths); no file edits during the wait. Each discipline emerged from a recurring failure mode observed during the corpus-remediation work that drove the pack's recent evolution. The pack's [`README.md`](dev-security/claude-rules/README.md) inventory tree, available-rules table, and pack-CLAUDE.md one-line summary were extended in parallel; [`tools/lint-claude-rules-sync.py`](tools/lint-claude-rules-sync.py) gains a new mapping entry for the rule's pack-to-local mirroring. The project-local [`.claude/CLAUDE.md`](.claude/CLAUDE.md) summary references the new rule and the project-specific tracking artefact. **New**: [`.working/hallucination-metrics.md`](.working/hallucination-metrics.md) records the catch / escape ratio for the research-assistant discipline — the project's operational counterpart to the rule's tracking convention. Initial state seeded with the known catches (FR-3 PR cross-reference, stale version numbers) and the known shipped escapes (ISO/IEC 29134 year corrected in Sweep 15; P1.3 file-path confabulation caught at boundary). Pack version `1.35.0 → 1.36.0`; library `2026.06.154 → 2026.06.155`; README `1.9.25 → 1.9.26`.

---

## 2026-06-21, Library Version 2026.06.154, PR #175

`.working/` changes for local project: retroactively shortened every existing entry in [`.working/DONE.md`](.working/DONE.md) to the 1-2-sentence, no-links, no-version-bumps "scrolling battle-text" shape adopted in PR #174. Library version unchanged from PR #174; the file changed is maintainer working state.

---

## 2026-06-21, Library Version 2026.06.154, PR #174

**Changed.** Retired the `Changelog: skip` opt-out path in [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) (and its mirror at [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md)) in favour of a terse-entry convention: every PR carries an entry, even if terse. Substantive entries (the existing structured-section form) cover anything that ships, modifies, or removes adopter-facing content. Terse entries (date + version header + one sentence on what was accomplished) cover ancillary changes (internal tooling, working-state housekeeping, pure refactors, typo fixes); there is no skip path. The paired DONE-ledger guidance is also revised: entries are 1-2 sentences, no links, no version bumps — "scrolling battle-text" framing as an at-a-glance index rather than a CHANGELOG duplicate. The change-tracking workflow skill at [`dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md`](dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md) is updated in parallel (paired-skill step-parity gate). The pack's [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) and the project-local [`.claude/CLAUDE.md`](.claude/CLAUDE.md) one-line summaries of the change-tracking rule are updated to match. Pack version `1.34.0 → 1.35.0`; library `2026.06.153 → 2026.06.154`; README `1.9.24 → 1.9.25`. **Back-compat note.** The D1 CHANGELOG-delta CI gate ([`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py)) still accepts the legacy skip trailer as a transition-window measure; tightening the gate to match the rule is queued as a follow-up.

---

## 2026-06-21, Library Version 2026.06.153, PR #173

`.claude/` changes for local project: backfilled the missing CHANGELOG entries for PRs #170 and #171 (added below). Library version unchanged from PR #172, since this PR introduces no new corpus content beyond the audit-trail repair. Per the maintainer's updated audit-trail discipline, `.claude/`-only changes carry a one-line CHANGELOG entry rather than `Changelog: skip`; the skip-rule adjustment in the pack rule file itself is queued as a follow-up PR.

---

## 2026-06-21, Library Version 2026.06.152, PR #171

`.claude/` changes for local project: added a `## PR activity subscription discipline` section to [`.claude/CLAUDE.md`](.claude/CLAUDE.md) requiring every `mcp__github__subscribe_pr_activity` call to arm a paired 60-second fallback timer (subscriptions reliably deliver failure events but not all success transitions; the timer is the catch-net). [`.claude/CLAUDE.md`](.claude/CLAUDE.md)'s PR workflow step 3 updated to reference the new section. Backfilled in PR #173.

---

## 2026-06-21, Library Version 2026.06.152, PR #170

`.claude/` changes for local project: added a `## Version-bump discipline` section to [`.claude/CLAUDE.md`](.claude/CLAUDE.md) codifying (1) per-document `Version` bumps in the same commit that changes the document's body, (2) library CalVer bumps once per PR in the last commit before push, and (3) README `Version` field bumps in the same commit as the CalVer bump. Surfaced after PR #169's gate 40 catch on a body-change commit that missed its per-doc bump. Backfilled in PR #173.

---

## 2026-06-21, Library Version 2026.06.153, PR #172

Closes **FR-4** (medium), **FR-5** (medium), **FR-6** (medium), **FR-7** (medium), and **FR-8** (medium, ⚠️ confirmed-with-modification). Phase 1 velocity bundle: five medium README polish findings shipped as one PR; all edits localise to [`README.md`](README.md). FR-4 — the "Framework alignment model" section's one-sentence acronym chain (ISO, NIST, COBIT, CSA CCM, STAR, OWASP, ASVS, SAMM, MITRE ATLAS, MITRE ATT&CK) is reformulated as a bulleted list with first-use expansion for each acronym, plus a soft pointer to [`governance/register-glossary.md`](governance/register-glossary.md) for fuller definitions. FR-5 — the paradoxical "approximately 300+ documents" line that promised "automated counts in a future release" is replaced with a direct pointer to the already-machine-generated [`taxonomy.yml`](taxonomy.yml) and the human-readable [`docs/portal.md`](docs/portal.md); sector-subdirectory paths are linked. FR-6 — the standalone CalVer paragraph at line 10 is removed from the front matter; the version-policy reference is folded into the existing "Specification and authoring files" table row for [`specification-master-project.md`](specification-master-project.md), which is the policy's normative home. FR-7 — the "Where to go next, by intent" bulleted list is reformulated as a table with an explicit "This README orients first-time readers and contributors to the library as a whole; most adopters do not need to read it end-to-end" lead clause, and names [`docs/portal.md`](docs/portal.md) as the canonical front door per PR #165 (FR-56). FR-8 — the dual `Library Version` + `README Version` rows are reordered to the bottom of the metadata block (demoting the churn-impression visual prominence) and gain inline parenthetical explanations distinguishing CalVer (library-wide) from semantic per-document versioning (this file); the Pass-1 ⚠️ modification note ("numbers have moved on; structural concern remains") is acted on by the demote-and-explain edit. Rec-6 from the fitness review (the original FR-1 through FR-8 README cluster) is now fully closed; FR-1, FR-2, and FR-3 shipped earlier as severity-warranted individual PRs (#155, #156, #147). Per-doc README `1.9.23 → 1.9.24`; library `2026.06.152 → 2026.06.153`. Backlog 82 → 77 open.

---

## 2026-06-21, Library Version 2026.06.152, PR #169

Closes **FR-26** (medium), **FR-27** (medium), and **FR-28** (medium): three access-control polish findings in [`security/procedure-access-control.md`](security/procedure-access-control.md). FR-26 — §1.2 3-business-day approval SLA gains a tiered escalation ladder (manager at +2 days, CISO at +2 more days, auto-decline at +2 beyond that), following the 1-2-3-ceiling pattern PR #152 / FR-19 introduced for CAPA §6.3.1 and PR #157 / FR-16 used for exception renewal §3.5. FR-27 — §3.2 access-review "appropriate" replaced with four bounded acceptance criteria (RBAC-catalogue match, least-privilege envelope, current business justification, PIM-role membership for privileged access); access failing any criterion is treated as unjustified and revoked under the next access review. FR-28 — §1.4 emergency-access "may be approved verbally" gains trigger conditions (active declared incident response per [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md), or material business / safety harm from portal-submission delay), retains the 24-hour formalisation clock, and adds the explicit consequence (Identity Team must revoke at the 24-hour mark if not formalised). The "may" permission verb is preserved per FR-44 §6.1; the revocation consequence uses "must revoke" per FR-45 / PR #150. Opportunistic Canadian-English spelling rolled in (`formalized` → `formalised`). Subsequent commits on this branch added the §3.2 prose tightening (heading-anchor compliance) and the per-doc Version bump that gate 40 requires. Per-doc `1.0.0 → 1.1.1`; library `2026.06.150 → 2026.06.152`. Backlog 85 → 82 open.

---

## 2026-06-21, Library Version 2026.06.150, PR #168

Sweep 15 follow-up: closes the BASC information-security 3-vs-5 classification gap surfaced by Sweep 15 Subagent A. [`compliance/logistics/policy-basc-information-security.md`](compliance/logistics/policy-basc-information-security.md) lines 99 and 190 enumerated only 3 classification levels (Confidential / Internal / Public) instead of the canonical 5 (Public, Controlled, Internal, Confidential, Restricted). Maintainer direction: expand to 5-level since the canonical scheme is a superset of the BASC 3 levels (any BASC-mandated sector requirement maps onto 3 of the 5 canonical levels; using all 5 cannot be worse than using 3). Both lines now enumerate the full canonical scheme with explicit cross-reference to [`security/standard-data-classification-and-handling.md`](security/standard-data-classification-and-handling.md). Per-doc `1.1.1 → 1.2.0` (minor: classification-scheme extension); library `2026.06.149 → 2026.06.150`.

---

## 2026-06-21, Library Version 2026.06.149, PR #167

Sweep 15 iteration 1 close-out. Three in-window findings fixed; one out-of-window note surfaced to operator. Subagents A, B, C all dispatched (Subagent A: 3 findings; Subagent B: 1; Subagent C: 0). In-window fixes:

- **(M)** [`docs/template-implementation-roadmap.md:12`](docs/template-implementation-roadmap.md): Review Frequency metadata field still referenced "quickstart-template module catalogue" — stale after PR #166 (FR-57) renamed the module-catalogue file to [`docs/template-startup-roadmap.md`](docs/template-startup-roadmap.md). Fixed. Per-doc `1.0.3 → 1.0.4`.
- **(M)** [`privacy/template-dpia.md:197`](privacy/template-dpia.md) and [`governance/register-document-index-and-classification.md:125`](governance/register-document-index-and-classification.md): cited `ISO/IEC 29134:2023` which is unverified — the publicly verifiable edition of ISO/IEC 29134 is the 2017 publication, with no recorded 2023 republication in the canonical-citations register. The 2023 year was likely a hallucination in the FR-29 DPIA template draft. Corrected to ISO/IEC 29134:2017 in both locations. Per-doc bumps: DPIA template `1.0.0 → 1.0.1`; document index `1.27.25 → 1.27.26`.
- **(W)** [`TODO.md:22`](TODO.md): "Queued sequence" narrative said "PRs #142-#159 have closed 21 findings to date" — lagged actual state by 5 PRs and contradicted line 113 of the same file ("26 closed across PRs #142-#166"). Refreshed to current state.

Out-of-window finding surfaced to operator (not actioned this PR):

- [`compliance/logistics/policy-basc-information-security.md:99,190`](compliance/logistics/policy-basc-information-security.md): enumerates 3 classification levels (Confidential / Internal / Public) instead of the canonical 5. Possibly intentional per BASC International Standard v6 Chapter 6, or a multi-surface gap PR #164 (FR-43-reshape) did not address. Operator decision needed: either confirm BASC mandates the 3-level scheme (add cross-reference to canonical standard with rationale) or expand to the 5-level scheme.

Subagent C surfaced one future-gate candidate as a non-finding: [`tools/build-portal.py`](tools/build-portal.py) had two same-day schema bumps in this batch (PR #165: 1.0.0 → 1.1.0; PR #166: 1.1.0 → 1.2.0). A future convention could require an inline `# Schema history:` comment block on generator-schema constants so the bump history is discoverable without grepping CHANGELOG. Recorded for future consideration; not actioned.

Also captures maintainer-directed standard-version-upgrade-process work as a new TODO section: a documented process for transitioning the corpus when an external standard republishes at a new version (covering diff, reference enumeration, content-vs-positional classification, systematic update, register update, audit-gate integration, communication). Sweep 15's ISO/IEC 29134 issue plus FR-21's ISO/IEC 27701:2019 → 2025 work motivated capturing this as a process. Owner: maintainer. Effort: M. Schedule: after FR backlog completes.

Detail report at [`.working/validate-sweeps/2026-06-21-sweep15-iter1.md`](.working/validate-sweeps/2026-06-21-sweep15-iter1.md). Library `2026.06.148 → 2026.06.149`.

---

## 2026-06-21, Library Version 2026.06.148, PR #166

Closes **FR-57** (high). [`docs/template-quickstart.md`](docs/template-quickstart.md) was 319 lines covering 5 dimensions × 23 modules — not a quickstart by any reasonable interpretation. Reconciled via Option B (rename + new short doc): the existing long-form composition workbook moves to [`docs/template-startup-roadmap.md`](docs/template-startup-roadmap.md) (renamed, content preserved with metadata + preface updates), and a new short [`docs/template-quickstart.md`](docs/template-quickstart.md) ships as a true 10-minute on-ramp (six-artefact core baseline, role-name substitution discipline, portal pointer, plus a "Next steps" block linking to the renamed long-form roadmap and the other three adopter-facing paths). Cross-references updated in [`docs/template-implementation-roadmap.md`](docs/template-implementation-roadmap.md) (Related Documents + body wording) and [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) (Related Documents). Portal generator updated to surface the two as separate rows: quickstart now answers "What do I copy on Day 1?"; startup-roadmap answers "And what do I add later?". Per-doc bumps: new quickstart `2.0.2 → 3.0.0` (major: file at this path materially redefined); renamed startup-roadmap `2.0.2 → 2.1.0`; implementation roadmap `1.0.2 → 1.0.3`; maturity self-assessment `1.0.1 → 1.0.2`; portal generator schema `1.1.0 → 1.2.0`; library `2026.06.147 → 2026.06.148`. Also captures effort-sizing labels (XS/S/M/L/XL) for future FR-item TODO entries as a post-backlog process improvement. Backlog 86 → 85 open.

---

## 2026-06-21, Library Version 2026.06.147, PR #165

Closes **FR-56** (high, adopter entry-point reconciliation). The corpus had six distinct entry-point sequences (README → portal; adopter guide → Tier 1/2/3; quickstart → core baseline + modules; decision tree → 30/90/180 sequenced reading; implementation roadmap → Phase 1/2/3 calendar; fitness-review path for maintainers); adopters could land on any of the five adopter-facing entries and not know how they relate. Reconciled via Option A (declare the portal canonical, document the other paths as deeper-dive branches). [`tools/build-portal.py`](tools/build-portal.py) now emits a new "Other entry points and when to use them" section immediately after the Overview, with a table that picks the right entry by question (role / adopt principles / Day 1 copy / reading order / calendar phasing). Four adopter-facing documents ([`docs/adopter-guide.md`](docs/adopter-guide.md), [`docs/template-quickstart.md`](docs/template-quickstart.md), [`docs/decision-tree.md`](docs/decision-tree.md), [`docs/template-implementation-roadmap.md`](docs/template-implementation-roadmap.md)) gain a "Where this fits among the adopter entry points" preface that names the portal as canonical and identifies each document's role among the five paths. The maintainer-facing fitness-review path is intentionally not surfaced in the adopter-facing portal block. Per-doc bumps: portal generator schema `1.0.0 → 1.1.0`; adopter guide `1.1.1 → 1.1.2`; quickstart `2.0.1 → 2.0.2`; decision tree `1.0.0 → 1.0.1`; implementation roadmap `1.0.1 → 1.0.2`; library `2026.06.146 → 2026.06.147`. Also captures BYOD MDM/MAM expansion as a maintainer-directed follow-up item in TODO. Backlog 87 → 86 open.

---

## 2026-06-21, Library Version 2026.06.146, PR #164

Closes **FR-43** (high[critical], reshape — data-classification level reconciliation). The canonical [`security/standard-data-classification-and-handling.md`](security/standard-data-classification-and-handling.md) defines five classification levels (Public / Controlled / Internal / Confidential / Restricted), but six subordinate documents enumerated only four (Controlled omitted); one prose line in [`security/standard-remote-working-security.md`](security/standard-remote-working-security.md) §7.1.1 explicitly said "four classification tiers", directly contradicting the canonical standard. Reconciled via Option A (propagate the 5-level scheme library-wide): six subordinate documents updated to enumerate all five levels with explicit cross-references to the canonical standard. The three documents already at 5 levels (DLP standard, media-handling procedure, records-retention standard) are unchanged. The canonical standard's preamble (line 17) now states the 5-level scheme as authoritative so future subordinate documents have a citable rationale. Opportunistic `shall → must` rolled in for [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md) §2 per PR #159 / FR-44 §6.1 convention. Per-doc bumps: classification standard `1.3.1 → 1.3.2`; remote-working standard `1.0.2 → 1.0.3`; BYOD policy `1.0.0 → 1.0.1`; privacy policy `1.3.0 → 1.4.0`; asset inventory register `1.0.1 → 1.0.2`; dev-security baseline reference `1.0.0 → 1.1.0`; dev-security quick reference `1.0.1 → 1.1.0`; library `2026.06.145 → 2026.06.146`. Also captures the maintainer's amendment to the validate-cadence rule (5 PRs per batch → 1-8 PRs per batch when logical grouping warrants). Backlog 88 → 87 open.

---

## 2026-06-21, Library Version 2026.06.145, PR #163

Maintainer-directed format harmonisation: [`.working/DONE.md`](.working/DONE.md) H3 headings now surface `FR-N (severity)` matching the TODO backlog's tier-grouped one-line bullet format. Earlier DONE entries had drifted to prose paragraphs with FR-N and severity buried mid-body, breaking scannability when the backlog grew to 23 closed items. Option A (lightest touch) retrofits 22 existing entries across PRs #142-#162 plus the FR-only cross-reference entries for FR-9, FR-10, FR-13, FR-21, FR-54, FR-55, FR-103. The body paragraphs are preserved verbatim; only the H3 heading gains the `(severity)` suffix and the convention is documented in the file's "How items get here" §. Pre-fitness historical entries (PRs #141 and earlier) left in their original form. No FR item closed by this PR; backlog totals unchanged. Library `2026.06.144 → 2026.06.145`.

---

## 2026-06-21, Library Version 2026.06.144, PR #162

Closes **FR-29** (high[critical]). The existing [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md) referenced a DPIA process but did not provide a working template; adopters could not evidence GDPR Article 35 compliance without inventing one. New [`privacy/template-dpia.md`](privacy/template-dpia.md) ships a CC BY-SA 4.0 structural template covering the three Article 35 limbs: §1 Article 35(1) trigger checklist (the three explicit Article 35(3) triggers plus supervisory-authority-list consultation), §2 EDPB WP248 nine-criteria framework (the indicators that signal high-risk processing, with the "two or more = DPIA required" decision rule), §3 Article 35(7) content checklist (the four mandatory blocks: systematic description; necessity and proportionality; risks to rights and freedoms; mitigation measures), and §4 sign-off and review. Framework alignment table cites GDPR, UK GDPR, EDPB WP248, LGPD Art 38, PIPL Art 55, EU AI Act Art 27, ISO/IEC 29134:2023, ISO/IEC 27701:2025, NIST Privacy Framework, AIDA §29. The procedure gains cross-references in §Related Documents, Step 1 (Initiation), and Step 6 (Record keeping); the document index registers the new template. Transfer Impact Assessments remain a separate FR. Per-doc: template `1.0.0` (new); procedure `1.3.2 → 1.3.3`; document index `1.27.24 → 1.27.25`; library `2026.06.143 → 2026.06.144`. Backlog 89 → 88 open.

---

## 2026-06-21, Library Version 2026.06.143, PR #161

Closes **FR-17** (high, Pass-1 ⚠️ confirmed-with-modification). The exception policy's §2.2 approval pathway (Department Head / CIO / Executive Committee or Board Risk Committee, with §3.5 ERC and Board Risk Committee renewal tiers from PR #157) named approvers that did not align with the [`governance/register-role-authority.md`](governance/register-role-authority.md) "Approve exception" RACI row, which carried a stub "Risk Accountable Role" placeholder. The RACI's Accountable cell now names the tiered pathway and points at [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §2.2 (with §3.5 cross-reference for renewals); the policy gains a new §2.4 that explicitly declares §2.2 / §3.5 as the source of truth for the RACI's chain, identifies the adopter-tunable seams (tier thresholds in §2.2; named bodies in §3.5 via the substitution clauses), and matches the reciprocal cross-reference pattern from PR #146 (FR-96). Per-doc bumps: role authority register `1.3.1 → 1.3.2`; exception policy `1.1.1 → 1.2.0`; library `2026.06.142 → 2026.06.143`. Backlog 90 → 89 open.

---

## 2026-06-21, Library Version 2026.06.142, PR #160

Sweep 14 iteration 1 close-out. Four in-window findings (Subagent A surfaced 3 FR-44-self-violations introduced by PRs #157 + #159 landing the same day; Subagent B independently flagged the same master-spec finding plus a stale TODO queued-sequence framing; Subagent C zero findings):

- **(W)** [`specification-master-project.md:126`](specification-master-project.md): legacy "shall" in §4.1 #2 — the §6.1 verb register added in PR #159 should have opportunistically converted this minority-verb occurrence. Fixed (rephrased to read naturally with "must not"). Per-doc `1.6.0 → 1.6.1`.
- **(W)** [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) lines 88, 94: new normative content from PR #157 used "may not" as a prohibition twice — contradicts §6.1 rule 3 ("Do not use 'may not' as a prohibition") which PR #159 introduced the same day. Both fixed to "must not". Per-doc `1.1.0 → 1.1.1`.
- **(N)** [`TODO.md`](TODO.md) Queued-sequence section: "Next, PR #N: First fitness-remediation PR" narrative is stale — 21 fitness-remediation PRs have shipped under maintainer direction across PRs #142-#159. Reframed to describe the working pattern and to name the still-queued large items explicitly (FR-14 maturity-ladder reconciliation; FR-44-generalisation corpus-wide "shall" sweep).

Subagent C also surfaced two future-gate candidates as non-findings: an ordinal-ceiling pattern observed twice (PR #152 / FR-19 + PR #157 / FR-16) recommended for codification after a third occurrence; a numerical-coherence pattern set extension to cover retention periods (would have caught FR-80) recommended after empirical analysis. Detail report at [`.working/validate-sweeps/2026-06-21-sweep14-iter1.md`](.working/validate-sweeps/2026-06-21-sweep14-iter1.md). Library `2026.06.141 → 2026.06.142`.

---

## 2026-06-21, Library Version 2026.06.141, PR #159

Closes **FR-44** (high, requirement-language register drift). The library had a de facto "must" / "must not" requirement-language convention (PR #150 / FR-45 implicitly settled on it for prohibitions; PR #154 generalised the same fix to three `ai/` occurrences) but the convention had never been documented at the library level. [`specification-master-project.md`](specification-master-project.md) §6.1 now states the convention explicitly: "must" / "must not" is the canonical normative pair; "should" / "should not" for recommendations; "may" as the permission verb (never "may not" for prohibitions, per the FR-45 precedent); "shall" / "shall not" reserved for direct quotation of external standards (ISO/IEC, NIST SP, IEC) or legacy content awaiting harmonisation. RFC 2119 / RFC 8174 cited. A corpus-wide harmonisation of legacy "shall" → "must" occurrences is deferred to a separate "FR-44 generalisation" item in TODO. Per-doc `1.5.2 → 1.6.0` (minor: new normative library-wide convention); library `2026.06.140 → 2026.06.141`. Backlog 91 → 90 open.

---

## 2026-06-21, Library Version 2026.06.140, PR #158

Closes **FR-80** (high[critical], SIEM / cloud-activity-log retention contradiction). [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md) said 3 years for SIEM event logs; [`operations/standard-cloud-security-configuration-baseline.md`](operations/standard-cloud-security-configuration-baseline.md) §6.3 said 90 days minimum for cloud activity-log retention. Cloud-activity logs forward into the SIEM, so the downstream baseline's 90-day floor appeared to undercut the upstream 3-year retention. Reconciled by reframing the 90-day figure as the platform-side forwarding floor (the window in which the SIEM ingests activity events) and clarifying that the SIEM is the authoritative retention authority for the long-tail. Both documents now say so explicitly with cross-references to each other. This PR also adds a TODO item to review the [`dev-security/claude-rules/`](dev-security/claude-rules/) language coverage (currently Python-focused) and decide which mainstream languages warrant baseline files and where the pack should reference dedicated technical-security projects rather than try to be one. Per-doc bumps: cloud baseline `1.4.3 → 1.4.4`; retention schedule `1.0.0 → 1.0.1`; library `2026.06.139 → 2026.06.140`. Backlog 92 → 91 open.

---

## 2026-06-21, Library Version 2026.06.139, PR #157

Closes **FR-16** (high[critical], [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md)). The exception register schema previously lacked hard ceiling fields and the policy used a weak "should not exceed 180 days" clause that allowed indefinite drift under repeated soft renewals. The schema now requires two new fields — `max_duration` (default 540 days, cumulative across all renewals) and `renewal_count_limit` (default 3) — and §3 is extended with a renewal-ceiling escalation pathway mirroring the FR-19 / PR #152 CAPA §6.3.1 structure: 1st renewal at the original approver, 2nd at the ERC, 3rd at the Board Risk Committee, 4th not permitted (forces close, descope, conversion to risk acceptance, or re-baseline). A re-baselining carve-out is added for materially-changed scope, with an anti-abuse condition. §5.1 register field list is extended in lock-step with the new schema fields. Per-doc `1.0.3 → 1.1.0` (minor: schema-level addition); library `2026.06.138 → 2026.06.139`. Backlog 93 → 92 open.

---

## 2026-06-21, Library Version 2026.06.138, PR #156

Closes **FR-2** (high, README). The "How to use" step 1 had directed readers to the 300-row document index ([`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) before the audience-keyed portal ([`docs/portal.md`](docs/portal.md)). The "New to GRC?" block already routes first-time visitors to the portal (added in PR #147); the older step 1 contradicted that signposting. Step 1 now opens with the portal as the primary pointer and retains the document index as a secondary pointer for readers who already know what they want. Steps 2-5 unchanged. Per-doc `1.9.8 → 1.9.9`; library `2026.06.137 → 2026.06.138`. Backlog 94 → 93 open.

---

## 2026-06-21, Library Version 2026.06.137, PR #155

Closes **FR-1** (high, README). The "What this repository is" section had previously framed the project as "two coordinated halves" giving the GRC corpus and the AI-assisted-maintenance reference implementation equal billing. [`README.md`](README.md) is now rewritten so the **GRC documentation corpus** is the unambiguous headline product; the audit toolchain at [`tools/`](tools/) and the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack are positioned as the operational layer used to maintain corpus consistency, with the pack described as a by-product of corpus maintenance rather than a parallel deliverable. The "Three adoption modes" section is untouched (pack-only adoption remains a documented mode); the co-evolution paragraph is preserved but reordered to make the causal direction explicit (the corpus generated the disciplines, not the reverse). Per-doc `1.9.7 → 1.9.8`; library `2026.06.136 → 2026.06.137`. Backlog 95 → 94 open.

---

## 2026-06-21, Library Version 2026.06.136, PR #154

Sweep 13 iteration 1 close-out. Five out-of-window findings from Subagent A (Subagents B and C zero findings):

- **FR-45 generalisation** to `ai/` domain: [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) `ADTEST-SEC-02` ("Test cases may not be removed") and `OFFAI-SEC-10` (GPL/AGPL embedding prohibition) tightened from "may not" to "must not be" / "must not be embedded"; [`ai/guide-ai-adversarial-test-reference.md`](ai/guide-ai-adversarial-test-reference.md) parallel restatement of `ADTEST-SEC-02` updated in lock-step. PR #150 had limited its corpus-wide grep to `security/`; these three `ai/` occurrences escaped that scope.
- **FR-92 generalisation** to BASC IT KPIs register: [`compliance/logistics/register-basc-it-compliance-kpis.md`](compliance/logistics/register-basc-it-compliance-kpis.md) gains `Escalation Owner` and `Remediation Sign-off` columns on its 10-row KPI table, applying the FR-92 design principle introduced for the IT-ops register.
- **Document history table backfill** on the same BASC file: frontmatter declared 1.1.1 but the history table only listed 1.0.0; rows for 1.1.0, 1.1.1, and 1.2.0 added.

Per-doc bumps: ai standard `1.8.1 → 1.8.2`; ai guide `1.3.0 → 1.3.1`; BASC KPIs register `1.1.1 → 1.2.0`. Library `2026.06.135 → 2026.06.136`. Detail report at [`.working/validate-sweeps/2026-06-21-sweep13-iter1.md`](.working/validate-sweeps/2026-06-21-sweep13-iter1.md).

---

## 2026-06-21, Library Version 2026.06.135, PR #153

Closes **FR-92** (high). [`operations/register-it-operations-kpis.md`](operations/register-it-operations-kpis.md) gains two new columns on every KPI table (Sections 1-8): `Escalation Owner` (the named role accountable for breach response when the target is missed) and `Remediation Sign-off` (the named role responsible for confirming that the breach event is closed). Roles are drawn from the [Role Authority Register](governance/register-role-authority.md): CIO escalation for IT-operations KPIs, CISO escalation for security-flavoured KPIs (patch/vulnerability management, security operations, EDR coverage), and ERC escalation where the KPI's Owner Role is already CIO or CISO (so escalation cannot meaningfully go to the same role). The KPI design principles list also gains a new principle 2 requiring both fields to be populated from the role-authority register, and the related-documents header now references that register. Per-doc `1.0.0 → 1.1.0` (minor: schema-level column addition); library `2026.06.134 → 2026.06.135`. Backlog 96 → 95 open.

---

## 2026-06-21, Library Version 2026.06.134, PR #152

Closes **FR-19** (high[critical]) and **FR-20** (high), both in [`compliance/procedure-capa.md`](compliance/procedure-capa.md). FR-19: CAPA target-date extensions lacked a governance ceiling, allowing Critical findings to remain open indefinitely under repeated single-step CISO sign-off. FR-20: root-cause statements had an aspirational "specific and actionable" requirement but no quality checklist, so generic phrases like "process gap" passed as written. New §4.1.1 supplies a five-criterion quality checklist (Specific / Causal / Actionable / Bounded / Evidence-anchored) that the GRC Manager applies during verification; new §6.3.1 supplies a hard extension ceiling (2nd extension to ERC, 3rd to Board Risk Committee, 4th not permitted) with a re-baselining carve-out for materially-changed root causes. The §9.1 escalation table and the trailing Moderate/Low sentence are updated to cross-reference the new ceiling so the two chains (days-past-target and extension-count) operate consistently. Per-doc `1.0.1 → 1.0.2`; library `2026.06.133 → 2026.06.134`. Backlog 98 → 96 open.

---

## 2026-06-21, Library Version 2026.06.133, PR #151

Closes **FR-35** (high, ✅ confirmed-as-stated, privacy breach-response). [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) now makes the GDPR Article 33(2) processor-to-controller timeline asymmetry explicit: the contractual 24-hour supplier clock starts at *processor* awareness of the breach (the Article 33(2) trigger), not at controller notification or any later milestone. §4.1 tightened ("becoming aware" anchor + cross-reference to §6.3); §6.3 gains a dedicated note explaining the two-clock model (24-hour processor-awareness clock vs 72-hour controller-awareness clock) and why a delayed Article 33(2) notification erodes the controller's Article 33(1) budget; §10 supplier-notification metric reworded to specify supplier awareness as the clock-start. Per-doc `1.4.3 → 1.4.4`; library `2026.06.132 → 2026.06.133`. Backlog 99 → 98 open.

---

## 2026-06-21, Library Version 2026.06.132, PR #150

Closes **FR-45** (high, ⚠️ confirmed-with-modification). RFC 2119 vocabulary tightening in two security standards: [`security/standard-authentication-and-password-management.md`](security/standard-authentication-and-password-management.md) §"Password requirements" and [`security/standard-remote-working-security.md`](security/standard-remote-working-security.md) §8.2 both used "may not" where the intent is a prohibition. Pass-1 flagged the drift under a strict RFC 2119 reading: "may not" admits a permissible-negative-possibility interpretation distinct from MUST NOT. Both lines now read "must not be" to match each file's prevailing normative verb ("must" appears 5 times in the password standard and 24 times in the remote-working standard; "shall" is essentially absent from both). Per-doc `1.0.1 → 1.0.2` in each file; library `2026.06.131 → 2026.06.132`. Backlog 100 → 99 open.

---

## 2026-06-21, Library Version 2026.06.131, PR #149

Closes **FR-21** (high[critical]). [`compliance/register-compliance-obligations-template.md`](compliance/register-compliance-obligations-template.md) Source Reference field tightened so register citations resolve to a single unambiguous source location: revised description plus a new "Source Reference granularity requirements" sub-section listing minimum-precision patterns (with acceptable / unacceptable examples) for NIST publications, ISO/IEC standards, statutes, COBIT, PCI DSS, CSA CCM, contracts, and voluntary commitments. Closes a register-defeating ambiguity. Per-doc `1.0.2 → 1.0.3`; library `2026.06.130 → 2026.06.131`. Backlog 101 → 100 open.

---

## 2026-06-21, Library Version 2026.06.130, PR #148

Sweep 12 iteration 1 close-out. Three in-window findings from subagents A/B (C zero findings):
- **(H)** [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md): Owner CIO → CRO + governance table CRO row added + CIO row reshaped. PR #143 had only fixed the companion standard; the policy retained the contradiction.
- **(M)** [`compliance/procedure-control-testing.md`](compliance/procedure-control-testing.md) §2.2: cross-reference added to the new sampling-justification field in [`compliance/template-audit-evidence-package.md`](compliance/template-audit-evidence-package.md) (PR #144 added the field but didn't update the procedure).
- **(L)** [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §5.2: reciprocal "related risk acceptance ID" field added; closes the latent bidirectional-asymmetry follow-up noted in PR #146's detailed CHANGELOG.

Detail report at [`.working/validate-sweeps/2026-06-21-sweep12-iter1.md`](.working/validate-sweeps/2026-06-21-sweep12-iter1.md). Library `2026.06.129 → 2026.06.130`.

---

## 2026-06-21, Library Version 2026.06.129, PR #147

Closes **FR-3** (high, newcomer-onboarding). New "New to GRC? Start here" section added to [`README.md`](README.md) between the metadata header and §Purpose. The block expands the acronym (the README's title carries `GRC` but never defines it), defines Governance / Risk / Compliance in plain language for a reader unfamiliar with the discipline, names the adjacent domains the library treats as siblings (security, privacy, resilience, supplier governance, AI governance), and signposts five role/intent-keyed next steps (first-time visitor, adopter, auditor, maintainer, glossary-lookup). README per-doc `1.8.84 → 1.9.0` (minor: new top-level section). Library `2026.06.128 → 2026.06.129`. Backlog 102 → 101 open.

---

## 2026-06-21, Library Version 2026.06.128, PR #146

Closes **FR-96** (high, ⚠️ confirmed-with-modification). [`risk/procedure-risk-acceptance.md`](risk/procedure-risk-acceptance.md) "Required record fields" gains a `Related exception register entry` field — the ID of the corresponding entry in the exception register if the acceptance derives from a policy/control exception, or `None` if pure risk acceptance. The linkage makes the two registers cross-traversable for audit traceability. Per-doc `1.0.0 → 1.0.1`; library `2026.06.127 → 2026.06.128`. Backlog 103 → 102 open.

---

## 2026-06-21, Library Version 2026.06.127, PR #145

Closes **FR-95** (high). [`risk/template-enterprise-risk-register.md`](risk/template-enterprise-risk-register.md) Acceptance section now requires a `Compensating Controls` field. The procedure already required compensating-controls analysis per [`risk/procedure-risk-acceptance.md`](risk/procedure-risk-acceptance.md) §5; the template now records each control with a brief note on how it offsets the un-treated risk so the acceptance record is self-contained and auditable. Per-doc `1.0.1 → 1.0.2`; library `2026.06.126 → 2026.06.127`. Backlog 104 → 103 open.

---

## 2026-06-21, Library Version 2026.06.126, PR #144

Closes **FR-22** (high). [`compliance/template-audit-evidence-package.md`](compliance/template-audit-evidence-package.md) operating-evidence section now requires a mandatory `Sampling justification` field per test (population size, sample size, selection method, confidence-level assumption, citation to [`compliance/procedure-control-testing.md`](compliance/procedure-control-testing.md) §2.2 sample-size table). "100% population review" is the explicit response when sampling doesn't apply. External auditors now see the statistical-basis justification for every sample without reconstructing it from peer documents. Per-doc `1.0.0 → 1.0.1`; library `2026.06.125 → 2026.06.126`. Backlog 105 → 104 open.

---

## 2026-06-21, Library Version 2026.06.125, PR #143

Closes FR-9 (high[critical]) and FR-10 (high) together — both relate to Chief Risk Officer presence in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md). The standard's `Owner` field changes from "Chief Information Officer" to "Chief Risk Officer"; §3 Governance gets a new CRO row scoped to risk strategy, risk appetite stewardship, and ERM programme outcomes; the pre-existing CIO row is reshaped to "provides executive support on technology-risk integration". Per-doc `1.3.3 → 1.3.4`; library `2026.06.124 → 2026.06.125`. Backlog 107 → 105 open.

---

## 2026-06-21, Library Version 2026.06.124, PR #142

First fitness-remediation PR. Closes four unambiguous quick-win findings at maintainer direction while the maintainer reviews the broader 111-item backlog: **FR-13** disambiguates `CPPA` in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §10 framework alignment table; **FR-54 / FR-55** add an explicit doctype-prefix mapping table to [`specification-master-project.md`](specification-master-project.md) §4.3 covering all 17 doctypes; **FR-103** adds a Chief Compliance Officer row to the Continuous Assurance framework's governance table. Backlog totals updated: 93 immediate-priority + 14 deferred = 107 open (4 closed). Library `2026.06.123 → 2026.06.124`.

---

## 2026-06-21, Library Version 2026.06.123, PR #141

Pass-2 of the fitness review (per the discipline in PR #139). Surfaced the four Pass-1 buckets to the maintainer via structured triage; outcomes: ✅ batch (91) accepted with Low tier deferred; ⚠️ batch (16) accepted with orchestrator's modifications; 🤔 batch (2) — FR-14 resolved to ✅ with library-wide CMMI propagation plan, FR-110 to ✅ at Medium; ❌ batch (2) reshaped (FR-43 kept at High[critical] with corrected 5-level-standard vs 4-level-subset framing; FR-53 downgraded to Low as metadata-field-unification question). New "Fitness review backlog" section in [`TODO.md`](TODO.md) groups all 111 FR-IDs by severity tier with brief summaries for High[critical] and High items; **no remediation begins until maintainer directs**. Also corrects PR #140's narrative miscount (93/14 → 91/16). Library `2026.06.122 → 2026.06.123`.

---

## 2026-06-21, Library Version 2026.06.122, PR #140

Pass-1 verification (per the discipline introduced in PR #139) applied to the existing 111 FR-N findings in [`.working/fitness-reviews/2026-06-21-r1.md`](.working/fitness-reviews/2026-06-21-r1.md). Five verification-task subagents dispatched in parallel; each performed direct source re-reads (no persona role) and applied one verdict tag per finding. Aggregate: **93 ✅ confirmed-as-stated / 14 ⚠️ confirmed-with-modification / 2 🤔 ambiguous-needs-maintainer / 2 ❌ rejected**. New §8.5 "Pass-1 Verification Results" added to the report with verdict table + per-bucket summary. Pass-2 (maintainer-interactive bucket processing) is the next queued PR. Library `2026.06.121 → 2026.06.122`.

---

## 2026-06-21, Library Version 2026.06.121, PR #139

Amends the `library-fitness-review` skill (`/fitness`) to introduce the unverified→confirmed labelling discipline. Subagent findings are now `verification: unverified` at output time; Pass-1 (orchestrator re-reads cited source and tags `✅` / `⚠️` / `❌` / `🤔`); Pass-2 (maintainer-interactive bucket processing). Triage by severity applies only to confirmed findings, which produce TODO entries carrying FR-N ID + run reference + verification date. SKILL.md Step 5 restructured into four sub-steps; [`.claude/commands/fitness.md`](.claude/commands/fitness.md) updated in parallel (paired-skill step-parity gate); [`.working/fitness-reviews/README.md`](.working/fitness-reviews/README.md) workflow rewritten. The existing 111 findings in [`.working/fitness-reviews/2026-06-21-r1.md`](.working/fitness-reviews/2026-06-21-r1.md) retroactively marked `verification: unverified` pending Pass-1 in the next PR. Pack `1.33.0 → 1.34.0`; library `2026.06.120 → 2026.06.121`.

---

## 2026-06-21, Library Version 2026.06.120, PR #138

Rotates the five shipped Priority 4 items (P4.1 through P4.5) from [`TODO.md`](TODO.md) into [`.working/DONE.md`](.working/DONE.md) as `### TODO P4.x` entries cross-referenced to the original "Shipped 2026-06-20 as ..." framing. P4.6 (corpus-management discipline as a shareable skill) remains forward-looking. Also removes the Sweep 4 follow-up historical note from "Open follow-ups from validation sweeps" (resolved and previously noted as no-longer-tracked). Closes the TODO content cleanup queued since PR #135. Library `2026.06.119 → 2026.06.120`.

---

## 2026-06-21, Library Version 2026.06.119, PR #137

New audit gate 46 ([`tools/lint-overnight-file.py`](tools/lint-overnight-file.py)) plus stub-format [`.working/overnight-pr.md`](.working/overnight-pr.md) plus pack rule amendment documenting the overnight-work protocol. The file's `Status:` field encodes lifecycle: `stub` (no overnight in flight, default) and `in-flight` (active session) pass; `done` (ended, awaiting morning processing) fails. The three-state field preserves the overnight workflow (overnight PRs land with `in-flight`) while applying mechanical pressure for morning processing once the session ends. Pack rule [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) gains a new "Overnight-work protocol" subsection under PR finalization protocol; mirrored to [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md). Pack `1.32.0 → 1.33.0`; spec `1.13.1 → 1.14.0`; library `2026.06.118 → 2026.06.119`.

---

## 2026-06-21, Library Version 2026.06.118, PR #135

Restructures the working-state ledgers: new [`.working/design-decisions.md`](.working/design-decisions.md) file becomes the home for design-decision content; the "Design decisions made" section is rotated out of [`.working/DONE.md`](.working/DONE.md) (which is now strictly closed-TODO items); fitness-skill-specific decisions migrate out of the project's overnight-PR working file; TODO's "Decisions log" section migrates in as "Decisions explicitly dropped"; the overnight-PR working file is deleted as its substantive content has been routed and its procedural content has no forward-looking value. [`TODO.md`](TODO.md) "Notes on maintenance" updated to reflect the DONE-and-design-decisions routing. Maintainer-confirmed overnight-protocol-with-stub-and-gate standard added to TODO queued sequence as the next PR. Library `2026.06.117 → 2026.06.118`.

---

## 2026-06-21, Library Version 2026.06.117, PR #134

Gate 45 (TODO staleness audit) regex tightened to eliminate a false positive. The earlier `[^\n]{0,80}` window between "next/queued/pending" markers and `PR #<digit>` matched any digit-bearing PR ref within 80 characters, including historical parenthetical references in queued-item descriptions (e.g. `**Next, PR #N: TODO content cleanup.** Maintainer-surfaced (2026-06-21, during PR #133):`). The tighter character class `[\s,:—–-]*` allows only whitespace, commas, colons, and dashes between the marker and the digit-bearing PR ref, so the queued PR must be the immediately-following PR target. False-positive eliminated; real-drift cases (`Next, PR #128`, `Next — PR #128`, `queued PR #128`) still match. Post-PR-#133 merge `push`-event run on `main` failed on this false positive; this PR is the small focused fix.

---

## 2026-06-21, Library Version 2026.06.116, PR #133

Documents the project's language convention as **Canadian English first, Commonwealth (UK / Australian) English second, other dialects last**. Canadian English shares the `-ize` / `-ization` orthography with American English (the Oxford convention adopted in Canadian usage), so the [`tools/lint-language.py`](tools/lint-language.py) enforcement is the Canadian-orthography manifestation of the convention, not a generic American mandate. Doc-only change: linter docstring, [`.claude/CLAUDE.md`](.claude/CLAUDE.md) Conventions section, and [`CONTRIBUTING.md`](CONTRIBUTING.md) Style requirements rewritten to lead with the convention statement. No linter behaviour change. CONTRIBUTING `1.1.0 → 1.2.0`; library `2026.06.115 → 2026.06.116`.

---

## 2026-06-21, Library Version 2026.06.115, PR #132

Adds [Ryk Edelstein](https://github.com/fedelst) to the Acknowledged contributors list in [`AUTHORS.md`](AUTHORS.md). First PR exercising the post-PR-#131 steady-state TODO/DONE rotation discipline (item rotated from TODO to DONE in the same commit). Includes a one-time bootstrap correction: PR #131 itself is added to DONE retroactively, since it created DONE but did not record its own entry.

---

## 2026-06-21, Library Version 2026.06.114, PR #131

Introduces [`.working/DONE.md`](.working/DONE.md), the closed-TODO ledger, and rotates all historical "PRs completed this session" entries (PRs #110-#130) and "Key design decisions made this session" subsections out of [`TODO.md`](TODO.md) into DONE. TODO is now forward-looking only. Pack rule [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) gains a "PR finalization protocol" section documenting three disciplines: TODO is forward-looking (delete-on-close, no strikethroughs); DONE complements CHANGELOG (CHANGELOG by PR, DONE by closed item); after-merge protocol of listing the next-N planned PRs from TODO. [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR workflow extended with two new steps capturing both disciplines durably. Pack `1.31.0 → 1.32.0`; library `2026.06.113 → 2026.06.114`.

---

## 2026-06-21, Library Version 2026.06.113, PR #130

Removes decorative gate-count narrations from prose throughout the corpus and tooling. Phrases like "the 45-gate audit programme", "all 45 gates", "gates 1-45", and "45 corpus gates" are now "the audit programme", "every gate", "all corpus gates", and "the corpus gates" respectively; the spec §6 inventory remains the canonical single source for the count. Eleven prose locations updated across seven files. Implements the maintainer's just-surfaced proposal that decorative counts add no information beyond what readers can derive from the inventory table, and add real cost on every gate-add PR (PR #128 cascaded ten N-gate references across seven files; PR #129 cascaded one more). Gate 39 (cross-file gate-count consistency) remains as the defence against new decorations creeping back in.

---

## 2026-06-21, Library Version 2026.06.112, PR #129

Post-PR-#128 catch-up: [`TODO.md`](TODO.md) still framed PR #128 as "Next" after PR #128 merged, which the brand-new gate 45 (TODO staleness audit) correctly flagged on the post-merge `main` `push`-event run. Fixes the TODO drift: PR #128 moved to PRs-completed list with its summary; queued sequence rebased to start with the fitness-skill amendment; version-snapshot refreshed to 2026.06.111; the maintainer's two design proposals (DONE.md ledger; decorative-gate-count cleanup) recorded as queued follow-ups. This is the first instance of gate 45 catching exactly the failure mode it was built to catch — its own PR's lingering "queued" framing.

---

## 2026-06-21, Library Version 2026.06.111, PR #128

New audit gate 45 (TODO staleness audit) plus a PR-time-checks wrapper script. Gate 45 mechanically catches the two TODO drift shapes that recurred across four consecutive validation sweeps (queued PR already merged; sweep cursor behind history); the wrapper [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh) bundles the two PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR version-bump) and gate 45 into one local runner the maintainer invokes before push. Together with [`tools/run_all_audits.sh`](tools/run_all_audits.sh), the two runners cover every gate the CI workflow runs. The two-runner split is a structural fix for the version-bump-omission failure mode that surfaced in PR #127's first push: every gate now has a local invocation path. Spec [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 inventory extended; [`TODO.md`](TODO.md) preamble amended to note the narrow gate-45 exception to TODO's "informational only" status; [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR workflow updated to require both runners. New TODO P4.6 records the "corpus-management discipline as a shareable skill" follow-up the maintainer authorised, scheduled after the fitness backlog closes.

---

## 2026-06-21, Library Version 2026.06.110, PR #127

Sweep 11 iteration 1 close-out. Eight in-window findings actioned: corrected the fitness report's count mismatch across six surfaces (95/18/22/31/24 → mechanically-tabulated 111/17/20/57/17); updated [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) D1 description for dual-entry post-PR-#125; refreshed TODO and reframed its session-pause snapshot as "as-of-last-refresh" (one-time convention amendment to address the four-consecutive-sweep recurring drift); softened workflow ordering in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md); renamed [`.working/README.md`](.working/README.md) "Created by" column to "Origin"; bumped library version.

---

## 2026-06-21, Library Version 2026.06.109, PR #125

Splits the CHANGELOG into a two-file convention: root file carries lead-paragraph summaries (adopter-facing); detailed mirror in a working directory carries full structured-section entries (maintainer-grade). Historical content preserved verbatim in the detailed mirror; root file trimmed to first paragraphs (2926 lines → 675 lines). Delta gate extended to require both files move in lock-step. Change-tracking governance rule amended; pack version 1.30.0 → 1.31.0. First PR using the dual-entry convention; this entry dogfoods it.

---

## 2026-06-21, Library Version 2026.06.108, PR #124

First-ever invocation of the `library-fitness-review` skill (`/fitness`). Ten persona subagents dispatched in parallel. Aggregate raw findings 145; after dedupe approximately 95 unique. Severity distribution: 18 high[critical] / 22 high / 31 medium / 24 low.

---

## 2026-06-21, Library Version 2026.06.107, PR #123

Sweep 10 iteration 3 close-out: one in-window Medium finding actioned. Convergence-delta narrowing from iter 2's 7 findings to iter 3's 1.

---

## 2026-06-21, Library Version 2026.06.106, PR #121

Sweep 10 iteration 2 close-out: seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120).

---

## 2026-06-21, Library Version 2026.06.105, PR #120

Adds a new `library-fitness-review` skill to the `dev-security/claude-rules/` pack, invoked via the `/fitness` slash command. The skill is a comprehensive whole-corpus library-quality review dispatching ten persona reviewers in parallel (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer). Designed as a periodic deliverable (after major changes or quarterly minimum), not a per-PR gate; complements the per-PR `validation-sweep` skill (`/validate`). Output is an 8-section combined report with a discrete remediation backlog. This PR was authored end-to-end during an overnight session under explicit maintainer authorisation; see [`.working/overnight-pr.md`](.working/overnight-pr.md) for the decision log.

---

## 2026-06-21, Library Version 2026.06.104, PR #118

Restructured `.working/validate-sweeps/` to the canonical `<activity>/{README,history,detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory going forward. The validation-sweep history file moves into the subdirectory; verbose static content (failure-mode taxonomy, maintenance protocol, accept-list rules, dating discipline, framework alignment) moves to the subdirectory's README; the history file becomes a slim reverse-chronological table; per-iteration detail files are created only when findings exist.

---

## 2026-06-21, Library Version 2026.06.103, PR #117

Sweep 10 iteration 1 close-out: six in-window prose drift findings actioned, all introduced or made visible by the three-PR `.working/` sequence (PRs #114-#116).

---

## 2026-06-21, Library Version 2026.06.102, PR #116

Move the validation-sweep history file from `governance/` to `.working/`. The file is project-specific application of the validation-sweep discipline, not template content for adopters; per the framing established with the maintainer, application belongs in `.working/`. Template content (the failure-mode class taxonomy, the maintenance protocol, the false-positive accept-list rules, the dispatch-declaration discipline) lives in the [`validation-sweep` SKILL.md](dev-security/claude-rules/skills/validation-sweep/SKILL.md) in the pack; adopters get the discipline from the SKILL.md and start their own history file from zero in their fork.

---

## 2026-06-21, Library Version 2026.06.101, PR #115

`/validate` slash-command rename + per-iteration record convention. Second of the four-PR sequence around `.working/` (PR #114 shipped the infrastructure; this PR populates the first subdirectory and adds the persistent-record discipline to the validation-sweep skill).

---

## 2026-06-21, Library Version 2026.06.100, PR #114

Establishes the `.working/` top-level convention for maintainer working state. First of a four-PR sequence: this PR ships the infrastructure; subsequent PRs (`/validate` rename + per-run records, `/fitness` skill, changelog-details migration) populate the convention with content.

---

## 2026-06-21, Library Version 2026.06.99, PR #113

Sweep 9 iteration 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 actioned.

---

## 2026-06-21, Library Version 2026.06.98, PR #112

Sweep 9 iteration 2 closure + seventh governance rule ([`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md)).

---

## 2026-06-20, Library Version 2026.06.97, PR #111

Sweep 9 closure: Subagent C findings actioned + structural prevention of unauthorised subagent skips.

---

## 2026-06-20, Library Version 2026.06.96, PR #110

Validation-sweep finding (post-P4.5 sweep, Subagent B): two stale "42 gates" prose references that gate 39 missed. Plus a related pattern-set extension to close the gap going forward.

---

## 2026-06-20, Library Version 2026.06.95, PR #109

TODO P4.5: audit evidence package template. **Fifth and last of the Priority 4 items in sequence.**

---

## 2026-06-20, Library Version 2026.06.94, PR #108

Rename the adopter quickstart template from its prior "by-profile" filename to [`docs/template-quickstart.md`](docs/template-quickstart.md). Maintainer feedback: the file is no longer a per-profile template (after the P4.1 rewrite to activity-modular shape in PR #105), so the prior filename was misleading. The document title was already "Adopter Quickstart Template" so no title change is needed.

---

## 2026-06-20, Library Version 2026.06.93, PR #107

TODO P4.4: regulator interaction templates. Fourth of five Priority 4 items.

---

## 2026-06-20, Library Version 2026.06.92, PR #106

TODO P4.3: implementation roadmap template. Third of five Priority 4 items.

---

## 2026-06-20, Library Version 2026.06.91, PR #105

Heavy rewrite of [`docs/template-quickstart.md`](docs/template-quickstart.md). Maintainer's feedback on PR #103: the six fixed profiles (small business, mid-market regulated industry, multi-national enterprise, public-sector adopter, healthcare adopter, financial-services adopter) were too rigid; companies do not fit into the categories, and the same category contains very different operational realities.

---

## 2026-06-20, Library Version 2026.06.90, PR #104

TODO Priority 4.2: adopter maturity self-assessment template. Second of five Priority 4 items in sequence.

---

## 2026-06-20, Library Version 2026.06.89, PR #103

TODO Priority 4.1: adopter quickstart template per profile. First of five Priority 4 items the maintainer authorised in sequence.

---

## 2026-06-20, Library Version 2026.06.88, PR #102

Register-to-TODO alignment for [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) §6 (Document-type capability gaps). The register-vs-TODO diff (per the maintainer's "complete everything that isn't yet logged in TODO" instruction) found three drift items in §6; all are resolved here by lightweight bookkeeping updates rather than substantive document creation.

---

## 2026-06-20, Library Version 2026.06.87, PR #101

Refresh the `Cross-document numerical coherence shipped as scaffold` entry in [`TODO.md`](TODO.md)'s Decisions log. The prior text described the linter as tracking "0 terms" and the framework as "in place for future term curation"; that description is stale relative to the implementation. The scaffold has been progressively widened since the decision was logged: Phase 23.26 added P1/P2/P3 acknowledgement-time patterns as scaffolding, Phase 23.35 added the GDPR breach-notification-hours pattern after empirical confirmation. The current scaffold tracks four terms; the [`tools/lint-cross-doc-numbers.py`](tools/lint-cross-doc-numbers.py) docstring documents why each candidate (RTO, RPO, retention, P4, NIS 2, DORA) was considered and excluded with rationale.

---

## 2026-06-20, Library Version 2026.06.86, PR #100

**Closes the three-item queued-session backlog**: new audit gate 44 (paired-skill step-parity audit), third and last of the items announced in the maintainer's status summary (after PR #98 PF-04 stale-version-literal scanner extension and PR #99 gate 43 follow-up ageing audit). Mechanises the cross-document term-and-identifier consistency check the validation-sweep history register flagged as a recurring gap.

---

## 2026-06-20, Library Version 2026.06.85, PR #99

New audit gate 43: follow-up ageing audit. Mechanises Rule 3 of the maintenance-tag dating discipline introduced in PR #90 (the convention shipped without a mechanical gate; this PR adds it). Second of three queued session items.

---

## 2026-06-20, Library Version 2026.06.84, PR #98

Pre-flight scanner pattern set extended. Adds **PF-04 stale-version-literal**: catches phrases like "currently 1.22.0" / "the current 1.22.0" / "now at 1.22.0" / "now on 1.22.0" where the captured version does not match any of the canonical library, README, pack, or spec versions. Motivated by the Sweep 4 finding in `docs/adopter-guide.md:57` ("ships with its own version sequence (currently `1.22.0`)"); the new pattern would have caught that finding mechanically rather than requiring semantic triage. First of the three queued session items announced in the maintainer's status summary.

---

## 2026-06-20, Library Version 2026.06.83, PR #97

Validation-sweep maintenance-protocol change plus retroactive CHANGELOG prune. Maintainer observed that zero-finding sweeps were producing standalone PRs with full CHANGELOG entries that contained no user-visible content, distracting from substantive entries. The convention is revised: **zero-finding sweeps leave no trace** (no register entry, no CHANGELOG entry, no standalone PR; the convergence-delta trend lives in the iteration counter, not in a per-sweep record).

---

## 2026-06-20, Library Version 2026.06.82, PR #96

Validation-sweep enhancement, seventh and last from the late-research-findings queue. **Closes the queue.** Adds the hold-the-line ratcheting-baseline discipline to step 6 (Triage) of the SKILL: fingerprint-not-count, expiry plus rationale, net-negative invariant on sweep close. This is the "largest" tier (after the smallest four: synthesis rubric, pre-tool verification, maintenance-tag dating, convergence-delta; and the medium two: multi-agent debate, SARIF-lite).

---

## 2026-06-20, Library Version 2026.06.80, PR #94

Validation-sweep enhancement, sixth of seven from the late-research-findings queue. Adds the SARIF-lite output format to step 4 of the SKILL: each subagent finding is a fenced markdown block with six labelled lines (tool / ruleId / level / location / fingerprint / rubric) plus an evidence paragraph. Closes the "medium" tier of the queue (after Rule 5.5 multi-agent debate in PR #93); only the "largest" tier (hold-the-line ratcheting baselines) remains.

---

## 2026-06-20, Library Version 2026.06.79, PR #93

Validation-sweep enhancement, fifth of seven from the late-research-findings queue. Adds Rule 5.5 to the synthesis rubric: single-round asymmetric debate for high-divergence disagreement between subagents. First of the "medium" tier (after the smaller-scope patterns 1-4).

---

## 2026-06-20, Library Version 2026.06.77, PR #91

Validation-sweep enhancement, fourth of seven from the late-research-findings queue. Replaces the fixed 3-iteration cap in step 7 with a principled three-condition termination: empty-delta primary stop, patience-plateau secondary stop, and a 6-iteration hard ceiling as runaway guard. Closes the last of the "smallest" tier in the queue (synthesis rubric, pre-tool verification, maintenance-tag dating, convergence-delta).

---

## 2026-06-20, Library Version 2026.06.76, PR #90

Validation-sweep enhancement, third of seven from the late-research-findings queue. Adds the Wikipedia-style maintenance-tag dating convention to the sweep-history register's Maintenance protocol, closing the gap where deferred findings accumulated without ageing signal.

---

## 2026-06-20, Library Version 2026.06.74, PR #88

Validation-sweep enhancement, second of seven from the late-research-findings queue. Adds a pre-tool verification preamble to the subagent fan-out discipline in step 4 of the validation-sweep skill. Closes the gap where subagents could make redundant or misdirected tool calls without an auditable justification trace.

---

## 2026-06-20, Library Version 2026.06.72, PR #86

Validation-sweep pre-flight scanner: noise-reduction enhancement. Across Sweeps 3, 4, and 5, the same 12-13 candidate findings re-surfaced on every run and were re-triaged as false positives every time. The maintainer asked: should the scanner be enhanced so it does not keep tagging the same shapes? Chose option 3 of the named alternatives: both heuristics and an exemption file.

---

## 2026-06-20, Library Version 2026.06.71, PR #85

Closes the Sweep 4 out-of-window classification-convention follow-up. The maintainer's decision (asked-and-answered, option "both, with primary tag"): a finding may carry more than one failure-mode class; one is tagged primary (the dominant mechanism) and one or more may be tagged secondary (the symptom shape). Historical entries from Sweeps 1-3 are not retro-applied; the convention applies from Sweep 5 onwards.

---

## 2026-06-20, Library Version 2026.06.69, PR #83

Validation Sweep 4 in-window finding (C1 stale-prose): the adopter-guide's Mode C section says the pack "ships with its own version sequence (currently `1.22.0`)" but the pack is at 1.26.6. Surfaced by Subagent B of the Sweep 4 fan-out; the new synthesis rubric tagged this `R` (read-verified), severity `should-fix-this-PR`. Fix uses number-stable wording rather than bumping the literal so the same drift does not recur on the next pack bump.

---

## 2026-06-20, Library Version 2026.06.68, PR #82

Validation-sweep enhancement, first of seven from the late-research-findings queue. Adds a deterministic four-rule synthesis rubric to step 5 of the validation-sweep skill. Closes the prior gap where the parent's synthesis after subagent fan-out was ad-hoc and unreproducible across sweeps.

---

## 2026-06-20, Library Version 2026.06.66, PR #80

Validation-sweep self-finding from the post-PR-79 sweep: cross-surface step-numbering drift. PR #78 introduced the deterministic pre-flight scanner as `### 3.5.` in [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) and as `3a.` in [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): same logical step, two different identifiers across parallel surfaces. Surfaced by subagent A of the validation-sweep fan-out (Medium severity, in-window finding).

---

## 2026-06-20, Library Version 2026.06.65, PR #79

Validation-sweep enhancement 4 of 4 from the process-assessment review: nightly scheduled mechanical sweep on `main`. Closes the original four-enhancement queue; the late-research-findings queue (SARIF, hold-the-line, multi-agent debate, maintenance-tag dating, pre-tool verification, synthesis rubric, convergence-delta termination) plus the queued pre-flight pattern-set extension follow in subsequent PRs.

---

## 2026-06-20, Library Version 2026.06.64, PR #78

Validation-sweep enhancement 3 of 4 from the process-assessment review: deterministic pre-flight scanner. The fourth (nightly scheduled sweep) follows in PR #79; then the late-research-findings queue.

---

## 2026-06-20, Library Version 2026.06.63, PR #77

Two validation-sweep discipline enhancements from the maintainer's process-assessment review. Other enhancements (deterministic pre-flight scanner; nightly scheduled sweep) follow in subsequent PRs.

---

## 2026-06-20, Library Version 2026.06.62, PR #76

Validation-sweep cleanup after the morning's `/validation-sweep` run on the post-PR-75 state surfaced two High-severity findings, both meta-ironic instances of the new [`skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md) skill catching itself violating its own rules. Plus one Medium-severity stale-prose finding from the sibling sweep.

---

## 2026-06-20, Library Version 2026.06.61, PR #75

Add three new skills to the dev-security/claude-rules/ pack, recreated as in-house CC BY-SA 4.0 content from cross-source research. The maintainer authorised the research-then-recreate pattern after a survey of Claude Code Skills on GitHub (kfchou/wiki-skills MIT, anthropics/skills Apache 2.0, obra/superpowers MIT, plus a Sushegaad GRC-content pack) identified three gaps in the existing pack worth filling without importing additional external overlays.

---

## 2026-06-20, Library Version 2026.06.60, PR #74

Layer 3 of the validation programme — invocation-pattern documentation. The validation-sweep skill (shipped in PR #62) is now discoverable via a project slash command and cross-referenced bidirectionally from related skills.

---

## 2026-06-20, Library Version 2026.06.59, PR #73

Wire the collection-candidate detector (shipped in PR #72) to run automatically on PRs that modify the pack. The detector was previously on-demand only; per the maintainer's clarification, it should also fire automatically whenever there is a new addition or an updated pack.

---

## 2026-06-20, Library Version 2026.06.58, PR #72

Add a companion exploratory tool to gate 41 (Collection-enumeration consistency audit): [`tools/detect-collection-candidates.py`](tools/detect-collection-candidates.py). Phase 2 of the Layer 2 / 3 deliverable the maintainer authorised during gate 41's design (PR #69). Gate 41 enforces drift discipline on a hard-coded list of collections; this tool surfaces NEW candidate collections by heuristic scan so the maintainer can triage them one-by-one and add approved candidates to gate 41's configuration.

---

## 2026-06-20, Library Version 2026.06.57, PR #71

Add gate 42 (**External-overlay license consistency audit**). Closes the licence-validation loop the maintainer specified: every file in the repository now has its licence mechanically validated against the appropriate expectation. Gate 15 already enforced the project's `CC BY-SA 4.0` requirement on the corpus's own content; gate 42 extends the same discipline to the external overlay at [`.claude/rules/external/`](.claude/rules/external/), where files retain their source project's licence rather than the project's own.

---

## 2026-06-20, Library Version 2026.06.56, PR #70

Minor formatting cleanup in a historical CHANGELOG entry for prose consistency. No content or behaviour changes.

---

## 2026-06-20, Library Version 2026.06.55, PR #69

Add gate 41 (**Collection-enumeration consistency audit**) — Layer 2 / 3 of 3 in the validation programme. The linter walks a hard-coded configuration of "collections" (currently: pack governance rules and pack skills), each declaring a canonical source-of-truth directory and one or more enumeration locations elsewhere in the corpus. For each collection, the linter compares the canonical set against each enumeration set and flags missing-or-extra items.

---

## 2026-06-20, Library Version 2026.06.54, PR #68

Three discipline + tooling improvements informed by the CI failures across PRs #65 and #67. The maintainer's post-CI assessment identified that (1) git-history-aware gates need post-commit re-audit, not just pre-push; (2) gate 40's regression test was weak (only asserted "runs clean on HEAD", didn't verify failure detection); (3) metadata bumps need automatic taxonomy/portal regeneration to avoid the cascade observed in PR #67. This entry lands all three.

---

## 2026-06-20, Library Version 2026.06.53, PR #67

Add a new audit gate (#40): **Corpus version-bump-recency audit**. Layer 2 deliverable 2b of 3 in the validation programme (Layer 1: the `validation-sweep` skill in PR #62; 2a: the D2 PR-only delta gate in PR #65; this PR: the corpus-side counterpart). The new linter uses `git log -G` pickaxe matching to compare, for each versioned document, the SHA of the most-recent commit that touched the file at all against the SHA of the most-recent commit that modified a Version metadata line. If they differ, the body has changed since the last Version bump; the gate fails.

---

## 2026-06-20, Library Version 2026.06.52, PR #66

End-of-day validation-sweep cleanup and discipline update. After eight PRs landed today (#59 through #65), the maintainer invoked the [`validation-sweep`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) skill as a follow-up. Two parallel subagent sweeps (8-PR deep review + corpus-wide stale-reference scan) surfaced three findings (one stale comment, one CHANGELOG narrative error, one pre-existing §5 categorisation gap). The maintainer responded with a discipline update for the skill: action all findings regardless of whether they were introduced today, and change the skill's focus window from "past 24 hours" to "past two calendar days" so out-of-window findings get **surfaced as questions rather than auto-deferred**. This entry closes all three findings and lands the skill update.

---

## 2026-06-20, Library Version 2026.06.51, PR #65

Add a new PR-only delta gate (**D2: Per-PR version-bump check**). Layer 2 deliverable 2 of 3 in the validation programme, shipped as a §6.1 delta gate alongside the existing D1 CHANGELOG-on-PR check. The new gate compares each markdown file modified in a PR between its merge-base and head, reading the `**Version:**` field at each, and fails if a file's body changed but its Version did not bump. Catches the per-document-version-bump-omission class of defect that the §6 monotonicity audit (gate 13) cannot detect: gate 13 confirms versions strictly increase across the corpus, but cannot tell whether a particular file should have bumped on a particular PR.

---

## 2026-06-20, Library Version 2026.06.50, PR #64

Add a new audit gate (#39): **Cross-file gate-count consistency audit**. This is Layer 2 gate 1 of 3 in the validation programme. The gate scans the corpus for prose phrases that reference an audit-programme gate count and compares the captured number against the canonical row count of the §6 inventory. Any mismatch is flagged. The gate would have caught all seven stale "37-gate" references PR #59 missed, the two PR #61 missed (caught later by PR #63), and the nine additional stale "32-gate" references this PR's own first run surfaced in rule prose and tooling docs.

---

## 2026-06-20, Library Version 2026.06.49, PR #63

Dogfood-cleanup pass: the first run of the `validation-sweep` skill (shipped in PR #62) on the post-PR-61 main state found four sibling defects that PR #61's "cleanup all stale 37-gate references" pass had missed. This entry records what the dogfood run caught, and the small cleanup PR that closes them. The finding is itself a positive signal: shipping the skill in PR #62 led directly, on its first invocation, to surfacing two High-severity references that the unaided multi-PR cleanup had not caught. The Layer 2 gate-39 candidate (cross-file gate-count consistency) would have caught both mechanically.

---

## 2026-06-20, Library Version 2026.06.48, PR #62

Add the `validation-sweep` skill to the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack: a corpus-wide regression sweep designed to run as a follow-up after any issue is identified and corrected, to confirm no sibling issue remains anywhere in the repository. The skill operationalises the worked example added to `evidence-grounded-completion` in PR #60 (and corrected in PR #61) at corpus scope: combines the mechanical audit suite ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) — the canonical 38-gate full-audit invocation) with a structured semantic fan-out across parallel subagents (recent-PR deep review, corpus-wide stale-reference sweep, audit-programme integrity check), and loops until the cycle returns clean.

---

## 2026-06-20, Library Version 2026.06.47, PR #61

Cleanup pass after PR #59 and PR #60, surfaced by a recursive consistency review the maintainer requested before resuming Phase A work. Two failure shapes were found: (1) PR #60's worked example for `evidence-grounded-completion` mis-attributed the citing rule (claimed "step 4 of the verification protocol: when in doubt, re-run the verification standalone" — but step 4 is "Proactively search for contradictions", and the "when in doubt" phrasing is from the user-level Claude Code memory file's Rule 1.4 (outside this repository), not from the pack rule); (2) PR #59 added gate 38 to the §6 inventory and the four parity surfaces but missed seven downstream prose references in five files that still said "37 gates", and the spec's §5 categorisation was left without a slot for gate 38. The irony is that PR #60 shipped a worked example about exactly this multi-surface-omission failure mode and itself committed the mis-attribution variant of it.

---

## 2026-06-20, Library Version 2026.06.46, PR #60

Memorialise the multi-surface gate-parity failure mode as a worked example in the `evidence-grounded-completion` governance rule. The rule already names the abstract failure (claiming a gate suite passes from inference rather than from running it on the final state); the worked example grounds the abstraction in the concrete shape it took in practice — a session wiring a new gate into N–1 of N parallel surfaces and prepping the work for the next operator without re-running the audit, with the gate-name-parity gate catching the omission when the next session ran the full audit. The lesson generalises beyond audit gates to any work that touches parallel surfaces (mirror-sync, generator-output drift, polyglot lockfiles, cross-package version registers).

---

## 2026-06-20, Library Version 2026.06.45, PR #59

Add a new audit gate (#38) — the Section placement audit — that codifies two placement conventions a corpus-wide section-ordering survey found universally observed: orientation sections (Purpose, Scope, Overview, Applicability, Introduction, Executive Summary) must appear in the top three `##` sections, and Licence and Version-history sections must appear in the bottom three. The gate catches future drift mechanically without requiring per-doctype canonical-order codification. Library version `2026.06.44 → 2026.06.45`; audit-programme specification version `1.5.0 → 1.6.0` (minor bump: new gate added); README version `1.8.0 → 1.8.1` (patch: library-version-only bump).

---

## 2026-06-19, Library Version 2026.06.44, PR #58

Two coordinated cleanups in one PR: (1) move the root [`README.md`](README.md) "Licence and third-party reference boundary" section to the bottom of the file so it aligns with the placement convention every other README and the audit-programme survey found universal across the corpus; (2) update five places across the corpus where the external-rule-sources list still enumerated three names (TikiTribe, Wiz, Kariedo) instead of four (TikiTribe, Kariedo, addyosmani, Wiz). Library version `2026.06.43 → 2026.06.44`.

---

## 2026-06-19, Library Version 2026.06.43, PR #57

Restructure the [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) so the action-oriented content (scope, ways to use, directory structure, how to use, rule files) appears first and the historical reference content (per-version shipping log) appears near the bottom. The dense `## Pack scope` section that grew over many small additions is trimmed to the load-bearing content; the historical detail it carried (per-version shipping history, framing of the rollout's completion, enumeration of every skill that has ever shipped) is moved into a new compact `## Version history` table near the end of the README.

---

## 2026-06-19, Library Version 2026.06.42, PR #56

Tidy the [`README.md`](README.md) Mode C ("Adopt the pack only") paragraph: add a one-click link to the AI-assisted installer and remove the inline search-terms sentence that has become redundant with the GitHub repository topics and the [`CITATION.cff`](CITATION.cff) keywords shipped in PR #55. Two prose edits to the same paragraph; no structural changes.

---

## 2026-06-19, Library Version 2026.06.41, PR #55

Acknowledge the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack across the project's attribution and contribution surfaces, and enrich [`CITATION.cff`](CITATION.cff) with pack-specific search-term keywords so the pack is discoverable to readers who arrive looking for Claude Code rules or skills rather than for GRC content. Continues the reframe shipped in PR #54 by ensuring the pack is named in the attribution surfaces, not only in the positioning prose. Prose-only across five files; no structural changes.

---

## 2026-06-19, Library Version 2026.06.40, PR #54

Reframe the project's stated positioning to make explicit a dual-deliverable model that has been emerging across recent pack releases. The library is both (a) a CC BY-SA 4.0 GRC corpus and (b) a reference implementation showing how to maintain such a corpus with AI assistance, where the audit toolchain under [`tools/`](tools/) and the operational pack under [`dev-security/claude-rules/`](dev-security/claude-rules/) are the operational layer. The reframe also explicitly names a third, emergent adoption mode: the pack is usable as a standalone Claude Code baseline on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. No structural changes; prose-only across six framing surfaces.

---

## 2026-06-19, Library Version 2026.06.39, PR #53

Wrap the two remaining workflow-shaped governance rules as Claude Code Skills, closing out the post-S.3 evaluation that [`TODO.md`](TODO.md) recorded as deferred-until-trigger. Pack version `1.21.0 → 1.22.0` (minor bump, additive). The trigger condition (the next time the maintainer touched the skills pack) fired with PR #52; this PR acts on it by choosing the "Add both" outcome from the evaluation's possible outcomes.

---

## 2026-06-19, Library Version 2026.06.38, PR #52

Add a sixth governance rule to the `dev-security/claude-rules/` pack: [`governance/action-before-explanation-of-inaction.md`](dev-security/claude-rules/governance/action-before-explanation-of-inaction.md), the pack-distributable form of the user-level Rule 8 added on 2026-06-19. The discipline: never explain why an external action cannot or will not proceed without first attempting it (when the action is safe and reversible) or naming it and asking (when it is destructive). The phased governance rollout announced at pack version 1.6.0 completed at 1.11.0 with the first five rules; this entry extends the set post-rollout after a recurring AI-coding-assistant failure mode was observed in production sessions (narrating a reason to wait — "the PR is blocked because it needs a reviewer" — instead of attempting the cheap, reversible action that would have produced a real result).

---

## 2026-06-19, Library Version 2026.06.37, PR #50

Make every file under `docs/` carry the canonical 13-field metadata block, so the `docs/` tree is governed by the same audit programme as the rest of the corpus rather than carved out as a partial exemption with a per-file allowlist. Two hand-authored reference documents are promoted from informational aids to controlled artefacts; the two generator outputs ([`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md)) acquire metadata emitted by the generator itself. The previous mechanism, a `docs/` directory exemption in [`tools/lint-metadata.py`](tools/lint-metadata.py) with a `FORCE_INCLUDE_PATHS` carve-out for [`docs/worked-example.md`](docs/worked-example.md), is retired in favour of uniform enforcement.

---

## 2026-06-19, Library Version 2026.06.36, PR #49

Agent-production-authority controls, part C of three: operational closure. Completes the set begun in PR #47 (core control and evidence home) and PR #48 (governance integration). This part connects a harmful or unauthorised agent action to its reversal in incident response, and records the agentic standard in the cross-framework alignment matrix.

---

## 2026-06-19, Library Version 2026.06.35, PR #48

Agent-production-authority controls, part B of three: governance integration. Part A (PR #47) placed the `AGENT-PROD-01` to `AGENT-PROD-06` controls and their evidence home; this part wires the production-authority precondition into the acceptance-into-service gate, anchors it at the AI-governance framework tier, and binds the standing accountability to a named role. No new control language is introduced; each edit references the `AGENT-PROD-*` controls from part A so the gate is enforced at the formal acceptance decision, named in the framework that governs AI approval, and owned by an accountable human in the authority register.

---

## 2026-06-19, Library Version 2026.06.34, PR #47

Agent-production-authority controls, part A of the three-part set from the agentic-governance assessment: the core control, its evidence home, and the access-standard wiring. The governing principle is that autonomous agents do not receive production authority until reversibility, auditability, accountability, and permission boundaries are designed, tested, and governed; authority sits in the system boundary, the permissions model, the approval path, the immutable audit trail, the reversal mechanism, and a named accountable human, never in the agent. This closes the assessment's identified gap: the corpus treated reversibility as a classification input to an approval decision, not as a designed-and-tested precondition for production authority, and it did not consolidate the four properties into a single gate wired to acceptance-into-service.

---

## 2026-06-19, Library Version 2026.06.33, PR #46

Consistency follow-up to PR #45: broaden the summary surfaces that describe the evidence-grounded-completion rule, so they match the rule's scope after PR #45 extended it from completion claims to any state assertion. PR #45 deliberately left these surfaces untouched on the reasoning that each named the rule by its primary purpose and "remained accurate"; a subsequent read (prompted by the maintainer's "always confirm" instruction) showed that reasoning was an unverified inference that did not fully hold. Specifically, the pack's distributable governance instruction file made an explicit trigger claim ("the vocabulary of completion is a flag that the protocol must precede") that the broadened rule outgrew, and the project instruction file linked the rule only to user-level Rule 6 when a user-level Rule 7 now also exists. This PR corrects the surfaces that made trigger or linkage claims and broadens the lossy summaries for consistency.

---

## 2026-06-19, Library Version 2026.06.32, PR #45

Extend the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) pack rule from "evidence before completion claims" to "evidence before any state assertion." A session failure prompted this: during a governance assessment the assistant asserted that two templates "need new fields" and that a cross-framework matrix "needs control mappings" without having read those files; a later read confirmed the templates but showed the matrix operated at a different granularity than asserted. The existing rule did not fire because these were mid-analysis state assertions, not completion claims ("done", "fixed", "ready"). The rule's machinery (read, quote, contradiction-search, label-the-unverified) was already the right discipline; only its stated trigger was too narrow.

---

## 2026-06-19, Library Version 2026.06.31, PR #44

New audit gate (gate 37), **Claude-rules local-copy sync audit**, closing the systemic drift class the regression audit identified. The project keeps copies of a subset of the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack under `.claude/rules/` so a Claude Code session loads them as context. Both trees are exempt from the corpus linters, so until now nothing caught a local copy drifting from its pack source — the exact gap that let the evidence-grounded-completion local copy fall out of sync (fixed manually in PR #41) and would have re-opened on the next pack edit. This gate makes that drift class mechanically detectable.

---

## 2026-06-19, Library Version 2026.06.30, PR #43

Security fix: harden the gate-21 (Secret pattern audit) private-key detection regex, which had a false-negative gap. The maintainer's regression-audit review asked whether the example was RSA-specific; investigation found the detection regex itself enumerated five algorithm tokens (`RSA|DSA|EC|OPENSSH|PGP`) and consequently MISSED three real PEM private-key header forms (named here by their PEM label only, without the dash-fenced envelope, so this entry does not itself reproduce a scanner-detectable string): the bare `PRIVATE KEY` label (PKCS#8 unencrypted, the most common modern serialization and OpenSSL's default); the `ENCRYPTED PRIVATE KEY` label (PKCS#8 encrypted); and the `PGP PRIVATE KEY BLOCK` label (the real PGP header; the old regex's `PGP` branch matched a non-existent `PGP PRIVATE KEY` form and missed the actual one with the ` BLOCK` suffix). A PKCS#8 private key pasted into any corpus document would have passed gate 21 undetected.

---

## 2026-06-19, Library Version 2026.06.29, PR #42

Regression-audit fix: correct three stale gate-count references in the project instruction file [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md). All three said "32 gates" / "32-gate audit programme"; the audit programme has grown well past 32 (it was already past 32 before this session, and is 36 as of PR #37). The `.claude/` tree is exempt from the corpus linters, so no gate caught the drift; the regression audit found it.

---

## 2026-06-19, Library Version 2026.06.28, PR #41

Regression-audit fix: re-sync the project-local copy of the evidence-grounded-completion rule with its pack source. PR #38 added two subsections ("API polling and webhook subscriptions", "No decorative external links") to the pack source at [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) but did not propagate the change to the project-local copy at [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md). The two files are intended to be byte-identical (the local copy is the one a Claude Code session loads as session-start context; the pack copy is the distributable source). The `.claude/` tree is exempt from the corpus linters, so no gate caught the drift; the regression audit's `diff` of source against local copy found it.

---

## 2026-06-19, Library Version 2026.06.27, PR #40

Regression-audit fix: correct a stale gate-number reference in the docstring of [`tools/run-linter-regression.py`](tools/run-linter-regression.py). The docstring claimed "the audit programme's gate 35 invokes this script"; PR #37's gate renumber (35 → 36 gates) moved the linter regression test suite from gate 35 to gate 36, but the docstring was not updated. The docstring is a Python comment, not markdown, so no corpus gate scans it; the regression audit found it.

---

## 2026-06-19, Library Version 2026.06.26, PR #39

Regression-audit fix: correct stale gate-number and pack-version references in [`TODO.md`](TODO.md) left behind by the PR #37 gate renumber (35 → 36 gates, which shifted the Skill derives-from reference audit from gate 31 to gate 32) and the PR #38 pack bump (`1.20.0 → 1.20.1`). A full-repository regression audit found these references in the "Pack and tooling extension" section of [`TODO.md`](TODO.md); they were never updated when the underlying gate number and pack version changed.

---

## 2026-06-19, Library Version 2026.06.25, PR #38

Extend the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) pack rule with two new "Tool-specific guidance" subsections capturing two failure modes that surfaced in this session: a polling-pattern failure (raw `curl` against the unauthenticated GitHub API exhausted the 60-requests-per-hour-per-IP cap mid-session, after which every call returned HTTP 403, every iteration produced a Python `JSONDecodeError`, the loop never saw `completed`, and silent indefinite looping followed) and a URL-hallucination failure (auto-piloting from the project's file-path-link convention to a tool-name reference, inventing a plausible-looking documentation path under a real domain that did not in fact exist). Both lessons sit under §"Tool-specific guidance for AI coding assistants" next to the existing "Pipe-masked exit codes" subsection, with which they share the shape: a verification's actual outcome can be hidden by the way the verification is run.

---

## 2026-06-19, Library Version 2026.06.24

Option B from the S.4 follow-up: close the audit-coverage gap that allowed the S.2 and S.4 PRs to substantively edit governance documents without bumping the per-document `Date` metadata. New audit gate 31, **Document Date staleness audit**, compares each in-scope markdown file's `**Date:**` metadata to the file's most-recent git commit date (committer date in UTC) and fails when the metadata lags by more than `--max-lag-days` (default 1). Historical drift is grandfathered via a `--baseline-date` flag (default `2026-06-19`); the audit only enforces on commits at or after the baseline so the audit's introduction does not block CI on the 233-file pre-existing backlog identified at design time.

---

## 2026-06-19, Library Version 2026.06.23

S.4 backfill: correct per-document Date and Version metadata on five governance files that were substantively edited in the S.4 PR (library version `2026.06.21`, shipped 2026-06-19) without their per-document metadata being bumped. The omission violated the [`specification-ingestion.md`](specification-ingestion.md) contract that every substantive content change must update the document's Date to the current date and bump its Version per the disposition (patch for minor revision, minor for material revision). No existing audit gate caught the omission; the gap is acknowledged here and is closed by the follow-up audit-gate work tracked separately.

---

## 2026-06-19, Library Version 2026.06.22

S.4 follow-up: move the speculative "fourth skill" narrative out of the merged S.3 and S.4 CHANGELOG entries (where it violated Keep a Changelog's retrospective-only convention) and into [`TODO.md`](TODO.md) as a proper plan with a decision trigger, the empirical evidence to weigh at the trigger, an enumerated candidate set, and a selection criterion. The original CHANGELOG sentences pre-committed the project to a specific candidate (`change-tracking-write-entry`) without acknowledging the equally-strong alternative (`artefact-discipline-check`) or defining what "proven their format in practice" actually means; the TODO entry now records both and the criterion for choosing.

---

## 2026-06-19, Library Version 2026.06.21

Phase S.4 of the addyosmani agent-skills integration plan: add a new audit gate that enforces the derive-and-cite contract between skills and pack rules. The gate verifies that every skill document under [`dev-security/claude-rules/skills/`](dev-security/claude-rules/skills/) declares a `derives_from:` YAML frontmatter field whose value resolves to an existing pack rule, closing the maintenance loop opened in S.3 (skill workflows reference canonical rules rather than duplicate them).

---

## 2026-06-19, Library Version 2026.06.20

Phase S.3 of the addyosmani agent-skills integration plan: introduce a third pack-content type, **Claude Code Skills** in the Skills workflow format (one SKILL-named file per skill), under a new `skills/` subdirectory. Three skills land in this PR, each derived from an existing governance rule with the rule remaining as the source of truth for normative content.

---

## 2026-06-19, Library Version 2026.06.19

Phase S.2 of the addyosmani agent-skills integration plan: cherry-pick the STRIDE-per-trust-boundary framing and the three-tier disposition model from the addyosmani `security-and-hardening` overlay into a new library-canonical Standard, then add surgical "See also" cross-references from two existing documents.

---

## 2026-06-19, Library Version 2026.06.18

Phase S.1 of the addyosmani agent-skills integration plan: add `addyosmani/agent-skills` as the fourth external rule source the pack vouches for, fully vet 5 of its 24 skills, copy those 5 plus the upstream MIT licence file into this project's overlay directory, and announce the fourth source through the setup-generator's offer flow.

---

## 2026-06-03, Library Version 2026.06.17

Update the main-branch-protection register to reflect the bypass-actor configuration added on 2026-06-02. Closes the silent-drift gap between the register's claim ("bypass-actor list is empty") and the live ruleset state.

---

## 2026-06-02, Library Version 2026.06.16

Phase D.1 of the follow-up plan: give five previously-exempt repo-root meta files their own canonical 13-field metadata block and bring them under the corpus metadata audit. Closes the inconsistency where [`README.md`](README.md) carried a metadata block but other adjacent repo-root files did not.

---

## 2026-06-02, Library Version 2026.06.15

Phase C.1 of the follow-up plan: document the `main` branch-protection configuration as a governance register so it can be audited from the repository rather than from a privileged settings-page view.

---

## 2026-06-02, Library Version 2026.06.14

Phase B.1 of the follow-up plan: promote the metadata-line-breaks scanner methodology developed during the rendering-cleanup PRs (#23, #24, #25) into a 34th audit gate. This catches the soft-wrap rendering bug class going forward in CI rather than relying on ad-hoc scans.

---

## 2026-06-02, Library Version 2026.06.13

Phase A.1 of the follow-up plan: fix the underlying defect in the version-monotonicity audit that caused two real problems earlier today. The audit's regex previously matched any `**Version:** x.y.z` line in a Markdown file regardless of context, including lines inside fenced code blocks. This let (a) Phase 0's bulk sed sweep match a template field in [`CONTRIBUTING.md`](CONTRIBUTING.md), and (b) the audit block the cleaner revert in PR #24.

---

## 2026-06-02, Library Version 2026.06.12

Three additional files from a tightened metadata-rendering scan that my original scanner missed. Closes the metadata-rendering cleanup with **zero** remaining flagged files corpus-wide.

---

## 2026-06-02, Library Version 2026.06.11

Third and final file from the metadata-rendering scan: [`CONTRIBUTING.md`](CONTRIBUTING.md). Backslash fix plus a Version-field placeholder change that resolves an underlying gap exposed by today's investigation.

---

## 2026-06-02, Library Version 2026.06.10

Fix metadata-rendering bug in two files where consecutive metadata lines lacked the trailing `\` line-break that this corpus uses to force hard wraps. Without it, GitHub soft-wraps the metadata block into a single paragraph, making it unreadable. A full-corpus scan found exactly three affected files; two are fixed in this PR ([`CONTRIBUTING.md`](CONTRIBUTING.md) follows in a separate PR because its metadata block is a contributor template with its own Version-field considerations).

---

## 2026-06-02, Library Version 2026.06.9

Mobile-app security work, Phase 7 of 8 (final): Capacitor / Ionic pack rule file. The mobile-app security work announced as the 8-phase plan is complete with this release.

---

## 2026-06-02, Library Version 2026.06.8

Mobile-app security work, Phase 6 of 8: .NET MAUI pack rule file.

---

## 2026-06-02, Library Version 2026.06.7

Mobile-app security work, Phase 5 of 8: Flutter pack rule file.

---

## 2026-06-02, Library Version 2026.06.6

Mobile-app security work, Phase 4 of 8: React Native pack rule file.

---

## 2026-06-02, Library Version 2026.06.5

Mobile-app security work, Phase 3 of 8: Android pack rule file.

---

## 2026-06-02, Library Version 2026.06.4

Mobile-app security work, Phase 2 of 8: first per-language pack rule file for mobile.

---

## 2026-06-02, Library Version 2026.06.3

Mobile-app security work, Phase 1 of 8: expand the mobile standard with three substantive additions that close 2024-2026 currency gaps. Per-doc version bumped `1.0.1 → 1.1.0` (minor bump per semver for added sections).

---

## 2026-06-02, Library Version 2026.06.2

Mobile-app security work, Phase 0 of 8: project-wide ratification signal. All documents previously at v0.0.1 are bumped to v1.0.1 to signal that the content is no longer "first draft" status and is ratified for downstream use.

---

## 2026-06-01, Library Version 2026.06.1

Make the project's strict-mode stance on exceptions explicit in [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md), and document the `refs/preservation/` convention for the rare case of a legitimate protected-branch force-push. Both additions close gaps identified by the new pack governance rules: three pack rules reference a project "exception register" that this project does not maintain (the absence was implicit; now it is explicit), and one pack rule names the `refs/preservation/` namespace as the audit-trail convention for force-push exceptions (the convention is now documented so it can be followed without invention).

---

## 2026-06-01, Library Version 2026.06.0

Add a mechanical version-date consistency gate; bump to `2026.06.0` per [`specification-master-project.md`](specification-master-project.md) section 4.5; record the six-phase month discontinuity inherited from prior PRs.

---

## 2026-06-01, Library Version 2026.05.144

Phase 6 (final) of the dev-security pack scope expansion: fifth and last governance rule lands; the phased rollout announced at pack version 1.6.0 is complete.

---

## 2026-06-01, Library Version 2026.05.143

Phase 5 of the dev-security pack scope expansion: fourth governance rule lands.

---

## 2026-06-01, Library Version 2026.05.142

Phase 4 of the dev-security pack scope expansion: third governance rule lands.

---

## 2026-06-01, Library Version 2026.05.141

Phase 3 of the dev-security pack scope expansion: second governance rule lands.

---

## 2026-06-01, Library Version 2026.05.140

Phase 2 of the dev-security pack scope expansion: first governance rule lands.

---

## 2026-06-01, Library Version 2026.05.139

Phase 1 of the dev-security pack scope expansion: announce broadened contract from security-only to security + development-governance discipline.

---

## 2026-06-01, Library Version 2026.05.138

CHANGELOG enforcement gate and prior-PR catch-up entry.

---

## 2026-05-31, Library Version 2026.05.137

Corpus-wide hyperlink sweep and TODO.md cleanup.

---

## Initial public release (2026-05-31, Library Version 2026.05.136): CC BY-SA 4.0

First public commit of the Governance, Risk, and Compliance Documentation Library, published under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). See [`LICENSE`](LICENSE) for the full legal code and [`NOTICE.md`](NOTICE.md) for the repository's external-reference boundary.
