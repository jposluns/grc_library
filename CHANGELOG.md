# Changelog

All notable changes to this repository are recorded in this file as lead-paragraph summaries. Detailed maintainer-level entries (full Added / Changed / Removed / Fixed / Security / Verification sections per change) are kept in [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md). This is how this project's maintainer tracks the full audit trail. The convention is project-specific; forks may delete `.working/` and adopt their own approach to detailed change tracking. The mechanics are documented in the [`change-tracking` governance rule](dev-security/claude-rules/governance/change-tracking.md).

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

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
