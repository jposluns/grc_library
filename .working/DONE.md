# DONE

Closed-TODO ledger for the GRC Documentation Library. Records work that has shipped, keyed by the original backlog ID (PR number for PR-based items; the TODO `P-X.Y` identifier for backlog items). Reverse-chronological: newest at top.

This file complements two other working-state ledgers:

- [`CHANGELOG.md`](../CHANGELOG.md): records *what landed in each PR* (file-by-file changes, version bumps, verification). Organized by PR.
- [`design-decisions.md`](design-decisions.md): records *design decisions made* (working-state and convention decisions; decisions explicitly dropped). Organized thematically.

DONE records *which backlog items each PR closed* (cross-referencing the original TODO entries that motivated the work). Organized reverse-chronologically by closing PR. Adopters reading the corpus do not need any of these three files; they are maintainer working state and live under `.working/`.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. It is exempt from corpus audit gates per the `.working/` directory exemption.

## How items get here

When a PR closes a TODO item, the maintainer (or the AI assistant under the corpus-management discipline) rotates the item from [`TODO.md`](../TODO.md) into this file as part of the PR's diff. The rotation is enforced by convention rather than by a gate, per the discipline section in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md).

The format for each entry:

- `### PR #N — FR-X (severity): short title (YYYY-MM-DD merge date)` — primary header for a fitness-remediation PR that closes one FR. Severity values mirror the TODO backlog tiers: `high[critical]`, `high`, `medium`, `low`. The Pass-1 ⚠️ confirmed-with-modification flag is informational and stays in the body, not the heading.
- `### PR #N — FR-X (sev) + FR-Y (sev): short title (YYYY-MM-DD)` — for multi-FR PRs.
- `### PR #N — Sweep N iter M close-out: short title (YYYY-MM-DD)` — for validation-sweep close-out PRs (no single FR anchor; bundle multiple findings).
- `### PR #N — short title (YYYY-MM-DD)` — for non-FR PRs (workflow/infrastructure changes).
- `### FR-X (severity) — short title (closed by PR #N, YYYY-MM-DD)` — for FR-N cross-reference entries that need separate callouts (items closed across multiple PRs or items whose own narrative deserves its own H3 separate from the closing PR's entry).
- One-paragraph summary of what closed and any context a future reader needs to understand why this item existed.

The heading convention was harmonised with TODO's backlog format in PR #163 (2026-06-21) so a maintainer reading either file can scan FR-N + severity at the heading level without parsing the body paragraph. Earlier entries (before PR #163) were retrofitted in that same PR; pre-fitness historical entries that don't carry an FR-N anchor were left in their original form.

---

## Closed items

### PR #169 — FR-26 (medium) + FR-27 (medium) + FR-28 (medium): access-control procedure decision-path gaps (2026-06-21)

Phase 1 velocity bundle. Three medium-tier access-control polish findings closed, all in [`security/procedure-access-control.md`](../security/procedure-access-control.md). FR-26 — §1.2 3-business-day approval SLA gains a tiered escalation ladder (manager at +2 days, CISO at +2 more days, auto-decline at +2 beyond that, all logged and reviewed quarterly) following the 1-2-3-ceiling pattern from PR #152 (FR-19 CAPA §6.3.1) and PR #157 (FR-16 exception renewal §3.5). FR-27 — §3.2 access-review "appropriate" replaced with four bounded acceptance criteria (RBAC-catalogue role-profile match, least-privilege envelope, current business justification, PIM-role membership for privileged access), with explicit consequence (access failing any criterion is revoked per §3.3). FR-28 — §1.4 emergency-access verbal approval gains trigger conditions (declared incident response active per security/procedure-security-incident-response.md, or material business/safety harm from portal delay), retains the 24-hour formalisation clock, and adds §1.4.2 revocation consequence (Identity Team must revoke at 24 hours if not formalised). Opportunistic Canadian-English spelling rolled in (`formalized` → `formalised`). The "may" permission verb is preserved per FR-44 §6.1 rule 3; revocation uses "must revoke" rather than "may not" per FR-45 / PR #150. Per-doc `1.0.0 → 1.1.0`.

### PR #168 — Sweep 15 follow-up: BASC information security 5-level classification expansion (2026-06-21)

Sweep 15 surfaced an out-of-window finding at `compliance/logistics/policy-basc-information-security.md` lines 99 and 190 — the file enumerated only 3 classification levels (Confidential / Internal / Public) instead of the canonical 5. Maintainer decision: expand to 5-level since the 3 sector levels naturally map to 3 of the 5 (the canonical scheme is a superset). Both lines now enumerate the full canonical scheme (Public, Controlled, Internal, Confidential, Restricted) with explicit cross-reference to the canonical standard. Per-doc `1.1.1 → 1.2.0` (minor: classification-scheme extension). Library `2026.06.149 → 2026.06.150`.

### PR #167 — Sweep 15 iter 1 close-out: roadmap metadata + DPIA ISO/IEC citation + TODO narrative refresh (2026-06-21)

Sweep 15 surfaced 4 findings (3 in-window, 1 out-of-window). Subagent A: 3 findings (`docs/template-implementation-roadmap.md:12` Review Frequency metadata stale after FR-57 rename; `privacy/template-dpia.md:197` cites `ISO/IEC 29134:2023` which is unverified — 2017 is the publicly verifiable edition; `compliance/logistics/policy-basc-information-security.md:99,190` enumerates 3 classification levels possibly sector-conditional). Subagent B: 1 finding (`TODO.md:22` narrative lagged actual state by 5 PRs; contradicted line 113 of same file). Subagent C: 0 findings; 1 future-gate candidate (schema-version inline-history convention for `tools/build-portal.py`). In-window fixes applied: roadmap metadata (per-doc 1.0.3 → 1.0.4); ISO/IEC 29134:2023 → 2017 in DPIA template (per-doc 1.0.0 → 1.0.1) + document index (per-doc 1.27.25 → 1.27.26); TODO narrative refresh. BASC 3-level question surfaced to operator. Also captures maintainer-directed standard-version-upgrade-process work as a TODO item for after the FR backlog completes.

### PR #166 — FR-57 (high): rename long quickstart to startup-roadmap; ship new 10-minute quickstart (2026-06-21)

High finding closed. `docs/template-quickstart.md` was 319 lines covering 5 dimensions × 23 modules — not a quickstart by any reasonable interpretation. Reconciled via Option B (rename + new short doc): the existing long-form composition workbook moves to `docs/template-startup-roadmap.md` (renamed, content preserved with metadata + preface updates), and a new `docs/template-quickstart.md` ships as a true 10-minute on-ramp (six-artefact core baseline, role-name substitution discipline, portal pointer, plus a "Next steps" block linking to the renamed long-form roadmap and the other three adopter-facing paths). Cross-references updated in `docs/template-implementation-roadmap.md` (Related Documents + body "complete the quickstart composition first" → "complete the startup-roadmap composition first"), `docs/template-maturity-self-assessment.md` (Related Documents). Portal generator (`tools/build-portal.py`) updated to surface the two as separate rows: quickstart now answers "What do I copy on Day 1?"; startup-roadmap answers "And what do I add later?". Per-doc bumps: new quickstart `1.0.0 → 3.0.0` (major: file at this path materially redefined for different audience/content); renamed startup-roadmap `2.0.2 → 2.1.0` (minor: preface tightening + cross-reference updates, content preserved); implementation roadmap `1.0.2 → 1.0.3`; maturity self-assessment `1.0.1 → 1.0.2`; portal generator schema `1.1.0 → 1.2.0`. Also captures effort-sizing labels (XS/S/M/L/XL) for future FR-item TODO entries as a post-backlog process improvement.

### PR #165 — FR-56 (high): adopter entry-point reconciliation — portal declared canonical front door (2026-06-21)

High finding closed. The corpus had six distinct entry-point sequences (README → portal; adopter guide → Tier 1/2/3; quickstart → core baseline + modules; decision tree → 30/90/180 sequenced reading; implementation roadmap → Phase 1/2/3 calendar; fitness-review path for maintainers). Adopters could land on any of the five adopter-facing entries and not know how they relate. Reconciled via Option A (declare the portal canonical, document the other paths as deeper-dive branches). [`tools/build-portal.py`](../tools/build-portal.py) now emits a new "Other entry points and when to use them" section immediately after the Overview, with a table that picks the right entry by question (role / adopt principles / Day 1 copy / reading order / calendar phasing). Four adopter-facing documents (`adopter-guide.md`, `template-quickstart.md`, `decision-tree.md`, `template-implementation-roadmap.md`) gain a "Where this fits among the adopter entry points" preface that names the portal as canonical and identifies each document's role among the five paths. The maintainer-facing fitness-review path (sequence 6) is intentionally not surfaced in the adopter-facing portal block; it lives in `.working/fitness-reviews/` as maintainer working state. Per-doc bumps: build-portal generator schema `1.0.0 → 1.1.0`; adopter guide `1.1.1 → 1.1.2`; quickstart `2.0.1 → 2.0.2`; decision tree `1.0.0 → 1.0.1`; implementation roadmap `1.0.1 → 1.0.2`. Also captures BYOD MDM/MAM expansion as a maintainer-directed follow-up item in TODO.

### PR #164 — FR-43 (high[critical]): data-classification 5-level scheme propagated library-wide (2026-06-21)

High[critical] (reshape) finding closed. The canonical [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md) defines five classification levels (Public / Controlled / Internal / Confidential / Restricted) but six subordinate documents enumerated only four (Controlled omitted); one prose line in [`security/standard-remote-working-security.md`](../security/standard-remote-working-security.md) §7.1.1 explicitly said "four classification tiers", directly contradicting the standard. Reconciled via Option A (propagate the 5-level scheme): six subordinate documents updated to enumerate all five levels with cross-references to the canonical standard. The three documents already at 5 levels (DLP standard, media-handling procedure, records-retention standard) are unchanged. The canonical standard's preamble (line 17) now states the 5-level scheme as authoritative so future subordinate documents have a citable rationale. Opportunistic `shall → must` rolled in for `privacy/policy-privacy-and-data-governance.md` §2 per PR #159 / FR-44 §6.1 convention. Per-doc bumps: classification standard `1.3.1 → 1.3.2`; remote-working standard `1.0.2 → 1.0.3`; BYOD policy `1.0.0 → 1.0.1`; privacy policy `1.3.0 → 1.4.0`; asset inventory register `1.0.1 → 1.0.2`; dev-security baseline reference `1.0.0 → 1.1.0`; dev-security quick reference `1.0.1 → 1.1.0`. Also captures the maintainer's amendment to the validate-cadence rule (5 PRs per batch → 1-8 PRs per batch when logical grouping warrants).

### PR #163 — DONE format harmonisation with TODO: surface FR-N and severity at heading level (2026-06-21)

Maintainer-directed format change. The TODO file lists fitness items in tier-grouped one-line bullets keyed by `FR-N` plus severity (e.g., "FR-16 (high[critical]): ..."), making large numbers of items scannable at a glance. DONE entries had drifted to prose paragraphs with FR-N + severity buried mid-body, breaking the symmetry. Maintainer asked for harmonisation. Option A chosen (lightest touch): retrofit DONE H3 headings to surface `FR-N (severity)` while keeping the prose body intact. Format convention now documented in the file's "How items get here" §, listing the five heading shapes (single-FR PR, multi-FR PR, sweep close-out, non-FR PR, FR-N cross-reference). Twenty-two entries retrofitted across the fitness backlog (PRs #142-#162) plus the FR-only cross-reference entries for FR-9, FR-10, FR-21, FR-54, FR-55, FR-103, FR-13. Pre-fitness historical entries (PRs #141 and earlier) left in their original form.

### PR #162 — FR-29 (high[critical]): Data Protection Impact Assessment template with Article 35 trigger / EDPB WP248 / Article 35(7) content checklists (2026-06-21)

High[critical] finding closed. The existing `privacy/procedure-privacy-impact-and-cross-border-transfer.md` referenced a DPIA process but did not provide a working template; adopters could not evidence GDPR Article 35 compliance without inventing one. New `privacy/template-dpia.md` ships a CC BY-SA 4.0 structural template covering the three Article 35 limbs: Section 1 Article 35(1) trigger checklist (the three explicit Article 35(3) triggers plus supervisory-authority-list consultation), Section 2 EDPB WP248 nine-criteria framework (the indicators that signal high-risk processing, with the "two or more = DPIA required" decision rule), Section 3 Article 35(7) content checklist (the four mandatory blocks: systematic description; necessity and proportionality; risks to rights and freedoms; mitigation measures). Section 4 captures sign-off and review. Framework alignment table cites GDPR, UK GDPR, EDPB WP248, LGPD Art 38, PIPL Art 55, EU AI Act Art 27, ISO/IEC 29134:2023, ISO/IEC 27701:2025, NIST Privacy Framework, AIDA §29. The procedure gains cross-references in §Related Documents, Step 1 (Initiation: trigger checklist anchor), and Step 6 (Record keeping: template anchor). The document index registers the new template. Transfer Impact Assessments remain a separate (still-open) FR. Per-doc bumps: template `1.0.0` (new); procedure `1.3.2 → 1.3.3`; document index `1.27.24 → 1.27.25`.

### PR #161 — FR-17 (high): reconcile exception-approval authority between policy and Role Authority Register (2026-06-21)

High finding (Pass-1 ⚠️ confirmed-with-modification) closed. The exception policy's §2.2 approval pathway (Department Head / CIO / Executive Committee or Board Risk Committee, with §3.5 ERC and Board Risk Committee renewal tiers from PR #157) named approvers that did not align with the Role Authority Register's "Approve exception" RACI row, which carried a stub "Risk Accountable Role" placeholder. The RACI's Accountable cell now names the tiered pathway and points at the policy's §2.2 (with §3.5 cross-reference for renewals); the policy gains a new §2.4 that explicitly declares §2.2 / §3.5 as the source of truth for the RACI's chain and identifies the adopter-tunable seams. Reciprocal cross-reference pattern matches PR #146 (FR-96). Per-doc bumps: role authority register `1.3.1 → 1.3.2`; exception policy `1.1.1 → 1.2.0`.

### PR #160 — Sweep 14 iter 1 close-out: FR-44-self-violations + TODO queued-sequence refresh (2026-06-21)

Sweep 14 found 4 in-window findings (Subagent A surfaced 3 FR-44-self-violations introduced by PRs #157 + #159 landing the same day; Subagent B independently flagged the same master-spec finding plus a stale TODO queued-sequence framing; Subagent C zero findings). All 4 fixed: [`specification-master-project.md:126`](../specification-master-project.md) "No directory shall contain..." → "Directories must not contain..." (per-doc 1.6.0 → 1.6.1); [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) two "may not" prohibitions in §3.5 / §3.6 → "must not" (per-doc 1.1.0 → 1.1.1); [`TODO.md`](../TODO.md) Queued-sequence narrative reframed to reflect that 21 fitness-remediation PRs have shipped under maintainer direction, not that remediation is queued behind first-PR direction. Subagent C also surfaced two future-gate candidates as non-findings (ordinal-ceiling pattern observed twice; numerical-coherence retention-period extension candidate) — captured in the detail file, not actioned.

### PR #159 — FR-44 (high): requirement-language convention documented in master spec (2026-06-21)

High-severity finding closed. The library had a de facto "must" / "must not" requirement-language convention (PR #150 / FR-45 implicitly settled on it for prohibitions; PR #154 generalised the same fix to three `ai/` occurrences) but the convention had never been documented. [`specification-master-project.md`](../specification-master-project.md) §6.1 now states the convention explicitly: "must" / "must not" is the canonical normative pair; "should" / "should not" for recommendations; "may" as the permission verb (never "may not" for prohibitions); "shall" / "shall not" reserved for direct quotation of external standards or legacy content awaiting harmonisation. RFC 2119 / RFC 8174 cited. A corpus-wide sweep of legacy "shall" → "must" occurrences is deferred to a separate "FR-44 generalisation" item in TODO. Per-doc `1.5.2 → 1.6.0` (minor: new normative library-wide convention).

### PR #158 — FR-80 (high[critical]): SIEM / cloud-activity-log retention reconciliation (2026-06-21)

High[critical] cross-document contradiction closed. `governance/register-data-retention-schedule.md:67` said 3 years for SIEM event logs (1y hot + 2y cold); `operations/standard-cloud-security-configuration-baseline.md:150` said 90 days minimum for activity-log retention. Cloud-activity logs forward into the SIEM in this architecture, so the downstream baseline's 90-day floor appeared to undercut the upstream 3-year retention. Reconciled by reframing the 90-day figure as the platform-side forwarding floor (so the SIEM has a window to ingest events) and clarifying that the SIEM is the authoritative retention authority for the long-tail. Both documents now say so explicitly. Per-doc bumps: cloud baseline `1.4.3 → 1.4.4`; retention schedule `1.0.0 → 1.0.1`.

### PR #157 — FR-16 (high[critical]): exception register hard caps + renewal-ceiling escalation pathway (2026-06-21)

High[critical] finding closed. [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) §1.2 / §3 / §5.1 strengthened. The schema gains two required fields (`max_duration`, default 540 days; `renewal_count_limit`, default 3); the weak "should not exceed 180 days" clause is replaced by a hard 180-day initial-term cap plus the cumulative `max_duration` ceiling and a renewal-ceiling escalation pathway patterned on PR #152's CAPA §6.3.1: 1st renewal at the original approver, 2nd at the ERC, 3rd at the Board Risk Committee, 4th absolutely prohibited (forces close / descope / convert to risk acceptance / re-baseline). A re-baselining carve-out for materially-changed scope is included with an anti-abuse condition (ERC-approved; a re-baseline without material change is treated as the next renewal in the sequence). The §5.1 register field list is extended in lock-step with the new schema fields. Per-doc `1.0.3 → 1.1.0` (minor: schema-level addition).

### PR #156 — FR-2 (high): README "How to use" step 1 leads with the audience-keyed portal (2026-06-21)

High-severity README finding closed. The "How to use" step 1 had directed readers to the 300-row document index ([`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md)) before the audience-keyed portal ([`docs/portal.md`](../docs/portal.md)). The "New to GRC?" block added in PR #147 already routes first-time visitors to the portal; the older step 1 contradicted that signposting. Step 1 now opens with the portal as the primary pointer and retains the document index as a secondary pointer for readers who already know what they want. README per-doc `1.9.8 → 1.9.9`.

### PR #155 — FR-1 (high): README reframing (corpus is the headline, AI-maintenance is the methodology) (2026-06-21)

High-severity README finding closed. The "What this repository is" section had previously framed the project as "two coordinated halves" giving the GRC corpus and the AI-assisted-maintenance reference implementation equal billing. The fitness review judged this misframed the project's primary value. The section is now rewritten so the GRC documentation corpus is the unambiguous headline product; the audit toolchain at `tools/` and the `dev-security/claude-rules/` pack are positioned as the operational layer used to maintain corpus consistency. The pack-only adoption mode (documented in the "Three adoption modes" section) is preserved, and the co-evolution paragraph is retained but reordered to make the causal direction (corpus generated the disciplines, not the reverse) explicit. README per-doc `1.9.7 → 1.9.8`.

### PR #154 — Sweep 13 iter 1 close-out: FR-45 + FR-92 generalisations (2026-06-21)

Sweep 13 surfaced 5 out-of-window findings, all from Subagent A (recent-PR deep review). Bundled into one close-out PR per maintainer direction. Three FR-45-class fixes in [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) and [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md): `ADTEST-SEC-02` "Test cases may not be removed" → "must not be removed" (standard line 543; guide line 164 parallel restatement); `OFFAI-SEC-10` GPL/AGPL embedding-prohibition `may not be embedded` → `must not be embedded`. One FR-92-class fix in [`compliance/logistics/register-basc-it-compliance-kpis.md`](../compliance/logistics/register-basc-it-compliance-kpis.md): Escalation Owner + Remediation Sign-off columns added to the BASC IT KPIs table (10 rows; CISO escalation for IT-ops-style KPIs, ERC escalation where Owner is already CISO, mirroring the FR-92 design rule). One metadata fix on the same BASC file: Document history table backfilled with rows for 1.1.0 / 1.1.1 / 1.2.0 to match the frontmatter version chain. Per-doc bumps: ai standard 1.8.1 → 1.8.2; ai guide 1.3.0 → 1.3.1; BASC KPIs register 1.1.1 → 1.2.0. Subagents B (corpus-wide stale-reference) and C (audit-programme integrity) returned zero findings.

### PR #153 — FR-92 (high): KPI Escalation Owner + Remediation Sign-off columns (2026-06-21)

High-severity finding closed. [`operations/register-it-operations-kpis.md`](../operations/register-it-operations-kpis.md) gains two new columns on every KPI table (Sections 1-8) — `Escalation Owner` (the named role accountable for breach response when the target is missed) and `Remediation Sign-off` (the named role responsible for confirming that the breach event is closed). Roles drawn from the [Role Authority Register](../governance/register-role-authority.md): CIO for IT-operations KPIs, CISO for security-flavoured KPIs (patch/vulnerability management, security operations, EDR coverage), and ERC where the KPI's Owner Role is already CIO or CISO so escalation cannot meaningfully go to the same role. The KPI design principles list gains a new principle 2 requiring both fields to be populated from the role-authority register (existing principles 2-6 renumber to 3-7), and `Related Documents` now references the role-authority register. Per-doc `1.0.0 → 1.1.0` (minor: schema-level column addition).

### PR #152 — FR-19 (high[critical]) + FR-20 (high): CAPA governance ceiling + root-cause quality checklist (2026-06-21)

Closes two findings from the Pass-1 fitness sweep, both in [`compliance/procedure-capa.md`](../compliance/procedure-capa.md): FR-19 (high[critical]) — the CAPA extension policy had no hard ceiling, allowing indefinite open-ended remediation under repeated single-step CISO approvals; and FR-20 (high) — CAPA root-cause statements had no quality checklist, so bare category labels like "process gap" satisfied the aspirational §4.1 "specific and actionable" requirement. New §4.1.1 supplies a five-criterion checklist (Specific / Causal / Actionable / Bounded / Evidence-anchored) applied by the GRC Manager during verification; new §6.3.1 supplies a 2/3/4 escalation ceiling (ERC at the 2nd extension, Board Risk Committee at the 3rd, prohibition at the 4th, with a re-baselining carve-out for materially-changed root causes). §9.1 cross-references updated for consistency. Per-doc `1.0.1 → 1.0.2`.

### PR #151 — FR-35 (high): explicit GDPR Article 33(2) processor-awareness clock (2026-06-21)

High-severity (✅ confirmed-as-stated) privacy breach-response finding closed. [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) now makes the GDPR Article 33(2) two-clock asymmetry explicit: the contractual 24-hour processor-to-controller notification window starts at *processor* awareness (the Article 33(2) trigger), not at controller notification or at any later milestone; the controller's separate 72-hour Article 33(1) regulatory clock then runs from controller awareness. §4.1 detection-sources bullet, §6.3 supplier-notification section, and §10 supplier-notification metric all updated; §6.3 gains a dedicated explanatory note covering both clocks and the consumption relationship (a delayed Article 33(2) notification erodes the controller's 72-hour Article 33(1) budget). Per-doc `1.4.3 → 1.4.4`; library `2026.06.132 → 2026.06.133`.

### PR #150 — FR-45 (high): RFC 2119 "may not" → "must not be" in two security standards (2026-06-21)

High-severity Pass-1-⚠️ finding closed. [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md) §"Password requirements" and [`security/standard-remote-working-security.md`](../security/standard-remote-working-security.md) §8.2 both used "may not" where the intent is a prohibition. Strict RFC 2119 reads "may not" as a permissible-negative-possibility, distinct from MUST NOT. Both lines now use "must not be" — chosen over "shall not be" because each file's prevailing normative verb is "must" (5 / 24 occurrences vs. 0 / 1 for "shall"). Per-doc `1.0.1 → 1.0.2` in each file.

### PR #149 — FR-21 (high[critical]): Compliance-obligations Source Reference granularity (2026-06-21)

High[critical]-severity finding closed. [`compliance/register-compliance-obligations-template.md`](../compliance/register-compliance-obligations-template.md) Source Reference field tightened so register citations resolve to a single unambiguous source location: revised field description plus a new "Source Reference granularity requirements" sub-section enumerating minimum-precision patterns for NIST publications, ISO/IEC standards, statutes and regulations, COBIT, PCI DSS, CSA CCM, contracts, and voluntary commitments — each row with acceptable and unacceptable example citations. Closes a register-defeating ambiguity: populators could previously enter `NIST 800-53` or `ISO 27001` without revision or control and still satisfy the prior field description. Per-doc `1.0.2 → 1.0.3`; library `2026.06.130 → 2026.06.131`.

### FR-21 (high[critical]) — Compliance-obligations Source Reference granularity (closed by PR #149, 2026-06-21)

High[critical] finding from r1: template accepted low-precision citations (e.g., "NIST 800-53" without revision/control). Defeated the register's audit-prep purpose because an auditor could not resolve the obligation to a specific source location.

### PR #148 — Sweep 12 iter 1 close-out (2026-06-21)

Validation sweep after the six fitness-remediation PRs #142-#147. Subagents A, B, C dispatched in parallel (Rule 5.6 declaration recorded in history). Three in-window findings, all fixed in this PR:

- **(H) cross-doc-stale-cio-erm**: `risk/policy-enterprise-governance-and-risk-management.md` still named CIO as accountable for ERM after PR #143 only updated the companion standard. Owner changed CIO → CRO; new CRO row added to §3 governance table; CIO row reshaped to technology-risk integration scope. Per-doc `1.4.1 → 1.4.2`.
- **(M) missing-sampling-justification-link**: `compliance/procedure-control-testing.md` §2.2 lacked a cross-reference to the new "Sampling justification" field added to the audit-evidence template in PR #144. Added a paragraph after the sample-size ranges pointing to the template's per-test field. Per-doc `1.0.0 → 1.0.1`.
- **(L) missing-reciprocal-risk-acceptance-link**: `governance/policy-exception-and-risk-acceptance-management.md` lacked the reciprocal field that pairs with the "Related exception register entry" field added in PR #146. New §5.2 records the related risk-acceptance ID per exception. Acknowledged as a latent follow-up in PR #146's detailed CHANGELOG; closed here. Per-doc `1.0.2 → 1.0.3`.

Subagent C: zero findings (audit-programme integrity sound). Library `2026.06.129 → 2026.06.130`.

### PR #147 — FR-3 (high): README "New to GRC?" introductory block (2026-06-21)

High-severity newcomer-onboarding finding closed. Added a new "New to GRC? Start here" §2 to [`README.md`](../README.md) between the metadata header and §Purpose. The block expands the acronym, defines Governance / Risk / Compliance in plain language for someone who hasn't worked in the discipline, names the adjacent overlapping domains (security, privacy, resilience, supplier governance, AI governance) and explains why this library treats them as siblings, and signposts five role/intent-keyed next steps (first-time visitor, adopter, auditor, maintainer, glossary-lookup) each linking to the most relevant document. README per-doc bumps to `1.9.0` (minor; new top-level section); library `2026.06.128 → 2026.06.129`.

### PR #146 — FR-96 (high): Risk-acceptance procedure cross-reference to exception register (2026-06-21)

High-severity (⚠️ confirmed-with-modification) finding closed. [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md) "Required record fields" now includes `Related exception register entry`: ID of the corresponding entry in the exception register if the acceptance derives from a policy/control exception, or `None` if the acceptance is pure-risk and unrelated to a policy exception. The linkage makes the two registers cross-traversable: an auditor reviewing an exception can find the corresponding risk acceptance and vice versa. Per-doc `1.0.0 → 1.0.1`; library `2026.06.127 → 2026.06.128`.

### PR #145 — FR-95 (high): Risk register compensating-controls field (2026-06-21)

High-severity finding closed. [`risk/template-enterprise-risk-register.md`](../risk/template-enterprise-risk-register.md) Acceptance section now requires a `Compensating Controls` field listing each control by ID with a brief note on how it offsets the un-treated risk. Required by [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md) §5 already; the template now records it so the acceptance record is self-contained and auditable. Per-doc `1.0.1 → 1.0.2`; library `2026.06.126 → 2026.06.127`.

### PR #144 — FR-22 (high): Audit-evidence sampling-justification field (2026-06-21)

High-severity finding closed. [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md) per-control operating-evidence section now requires a mandatory `Sampling justification` field for every test that uses sampling. The field captures population size, sample size, selection method (random / stratified / judgemental), confidence-level assumption (if statistical), and a citation back to [`procedure-control-testing.md`](../compliance/procedure-control-testing.md) §2.2 sample-size table or rationale for a different size. "100% population review" is the explicit response when sampling does not apply. Per-doc `1.0.0 → 1.0.1`; library `2026.06.125 → 2026.06.126`.

### PR #143 — FR-9 (high[critical]) + FR-10 (high): Chief Risk Officer in enterprise risk management standard (2026-06-21)

Closes two related ERM-standard findings together: **FR-9** (high[critical]) changes the standard's `Owner` field from "Chief Information Officer" to "Chief Risk Officer" — enterprise risk is a CRO accountability, and CIO ownership read as a category error; **FR-10** (high) adds a CRO row to §3 Governance, scoped to risk strategy, risk appetite stewardship, and ERM-programme outcomes reporting to the Board / Risk Committee. The pre-existing CIO row is reshaped from "accountable for the framework" to "provides executive support on technology-risk integration" to clarify the post-CRO role. Per-doc `1.3.3 → 1.3.4`; library `2026.06.124 → 2026.06.125`.

### FR-10 (high) — Chief Risk Officer in ERM §3 governance table (closed by PR #143, 2026-06-21)

High-severity finding from r1: §3 governance table omitted CRO despite CRO being a defined role in the role-authority register and referenced in `procedure-risk-register.md`. Closed alongside FR-9.

### FR-9 (high[critical]) — Enterprise risk management Owner: CIO → CRO (closed by PR #143, 2026-06-21)

High[critical]-severity finding from r1: ERM-standard Owner field was "Chief Information Officer" but enterprise risk is a CRO/CFO/Board accountability in most operating models. Resolved to CRO per the finding text's first-listed alternative and per FR-10's parallel call to add CRO to the governance table.

### PR #142 — Fitness quick wins: FR-13 (medium) + FR-54 (low) + FR-55 (low) + FR-103 (low) (2026-06-21)

First fitness-remediation PR. Four findings closed at maintainer direction ("pick quick wins absolutely certainly in need of working while I review the rest of the backlog"). Each finding had an unambiguous fix in a single file with no judgement call required.

Library `2026.06.123 → 2026.06.124`. Subsequent fitness-remediation PRs continue at maintainer direction; the backlog totals in TODO are updated to reflect 107 remaining open findings (4 closed in this PR).

### FR-103 (low) — Add Chief Compliance Officer row to framework-continuous-assurance governance table (closed by PR #142, 2026-06-21)

Low-severity finding from r1: the Continuous Assurance framework's "Governance and accountability" table omitted CCO despite CCO being relevant to compliance-domain assurance closure. Added a CCO row with scope "Oversees compliance-domain assurance outcomes; chairs closure validation for compliance-related continuous-assurance findings; aligns the assurance calendar with regulatory obligation cadence." Per-doc version `1.0.1 → 1.0.2`.

### FR-55 (low) — Document `roadmap-` doctype prefix (closed by PR #142, 2026-06-21)

Low-severity finding from r1: `roadmap-` prefix is used in filenames (e.g. `security/roadmap-post-quantum-cryptography.md`) and `Roadmap` is an allowed doctype in `specification-master-project.md` §4.3, but the prefix-to-type mapping was only sparsely documented (one line in `specification-ingestion.md:196`). Closed alongside FR-54 by adding an explicit prefix-mapping table to `specification-master-project.md` §4.3 listing all 17 doctypes and their canonical filename prefixes. Per-doc version `1.5.1 → 1.5.2`.

### FR-54 (low) — Document `sop-` doctype prefix (closed by PR #142, 2026-06-21)

Low-severity finding from r1: same shape as FR-55 but for `sop-`. Closed by the same explicit prefix-mapping table addition in `specification-master-project.md` §4.3.

### FR-13 (medium) — Disambiguate `CPPA` in enterprise risk management standard (closed by PR #142, 2026-06-21)

Medium-severity finding from r1: §10 framework alignment table listed `CPPA` without disambiguation (Canadian Bill C-27 vs California Privacy Protection Agency). The surrounding row mentioned "Canadian personal information" so context was implicit, but the acronym still ambiguous on first read. Fixed by expanding the label to `CPPA (Canadian Consumer Privacy Protection Act, Bill C-27)`. Per-doc version `1.3.2 → 1.3.3`.

### PR #141 — Fitness backlog Pass-2: maintainer-interactive triage; structured TODO backlog (2026-06-21)

Pass-2 per the discipline introduced in PR #139. Surfaced the four Pass-1 buckets to the maintainer via structured AskUserQuestion. Outcomes:

- **✅ batch (91)**: accepted; deferred Low tier to later routine cleanup cycle; High[critical]/High/Medium become immediate-priority.
- **⚠️ batch (16)**: accepted with orchestrator's inline modifications (severity unchanged).
- **🤔 batch (2)**: FR-14 resolved to ✅ with library-wide CMMI propagation plan (concrete scope across 3 documents + forward-looking convention candidate); FR-110 resolved to ✅ at Medium severity.
- **❌ batch (2)**: FR-43 reshaped (the actual issue is 5-level standard vs 4-level subordinate-doc subset, kept at High[critical]); FR-53 reshaped as lighter-weight metadata-field unification question (downgraded to Low).

Backlog totals after Pass-2: **94 immediate-priority** (High[critical] 17 + High 20 + Medium 57) + **17 deferred** Low = 111. Zero findings removed.

Also corrects PR #140's narrative miscount (93/14 → 91/16 ✅/⚠️). New structured "Fitness review backlog" section added to [`TODO.md`](../TODO.md) with FR-IDs grouped by severity tier, special breakout for FR-14 library-wide CMMI plan, brief 1-line summaries for High[critical] and High items, and topical-cluster summaries for Medium and Low. Maintainer-reviewable; no remediation begins until directed.

New §8.6 "Pass-2 Maintainer-Interactive Outcomes" added to [`.working/fitness-reviews/2026-06-21-r1.md`](fitness-reviews/2026-06-21-r1.md) documenting the bucket decisions and reshape framings. Library `2026.06.122 → 2026.06.123`.

### PR #140 — Fitness backlog Pass-1: orchestrator verification of all 111 FR-N findings (2026-06-21)

Applies the Pass-1 verification step (introduced in PR #139) retroactively against the existing 111 FR-N findings in [`.working/fitness-reviews/2026-06-21-r1.md`](fitness-reviews/2026-06-21-r1.md). Five verification-task subagents dispatched in parallel, each handling a ~22-finding slice; instructions: direct file reads, no persona role, one verdict per finding plus brief inline note for non-`✅` verdicts. Aggregate: **93 `✅ confirmed-as-stated` / 14 `⚠️ confirmed-with-modification` / 2 `🤔 ambiguous-needs-maintainer` / 2 `❌ rejected`**. New §8.5 "Pass-1 Verification Results" added to the report with the full verdict table and per-bucket summary; §3 retroactive note updated to point at §8.5. The two `❌` findings (FR-43 inter-policy classification mismatch as framed; FR-53 "every document" claim) leave the backlog absent Pass-2 escalation. Pass-2 is the next queued PR. Library `2026.06.121 → 2026.06.122`.

### PR #139 — Fitness skill amendment: unverified→confirmed labelling discipline (2026-06-21)

Amends the `library-fitness-review` skill to introduce per-finding verification before any finding lands in the remediation backlog. Subagent findings are now `verification: unverified` at output time; Pass-1 (orchestrator re-reads cited source) tags each with `✅ confirmed-as-stated` / `⚠️ confirmed-with-modification` / `❌ rejected` / `🤔 ambiguous-needs-maintainer`; Pass-2 (maintainer-interactive) processes the four buckets — `✅` batch-confirmed, `⚠️` per-finding prompts with adjustment, `🤔` per-finding prompts for resolution, `❌` batch-presented with optional escalation. Confirmed findings produce TODO entries carrying FR-N ID + run reference + verification date. Updated SKILL.md, the `/fitness` slash command (paired-skill step-parity gate), and `.working/fitness-reviews/README.md`. The existing 111 findings in `2026-06-21-r1.md` retroactively marked `unverified` pending Pass-1 in the next PR. Pack `1.33.0 → 1.34.0`; library `2026.06.120 → 2026.06.121`.

### PR #138 — Shipped Priority 4 items rotation (2026-06-21)

Maintainer-surfaced (during PR #131): TODO's Priority 4 items 4.1 through 4.5 were "Shipped 2026-06-20 as ..." entries — completed work, not forward-looking backlog. Rotated to DONE as five separate `### TODO P4.x` entries (preserved here cross-referenced to the original "shipped" framing); P4.6 (corpus-management discipline as a shareable skill) remains forward-looking in TODO. Also removes the Sweep 4 follow-up historical note from "Open follow-ups from validation sweeps" (already resolved and noted as no-longer-tracked). Library `2026.06.119 → 2026.06.120`. Closes the TODO content cleanup queued since PR #135.

### TODO P4.1 — Quickstart templates per adopter profile (shipped 2026-06-20)

Shipped as [`docs/template-quickstart.md`](../docs/template-quickstart.md) (v2.0.0). Core baseline plus five stacking dimensions (Activity, Data scope, Audience, Regulatory exposure, GRC capacity) with about twenty modules; three worked examples. The original v1.0.0 fixed-profile structure (PR #103) was rejected by the maintainer as too rigid; the rewrite (PR #105) adopts an activity-modular composition shape that lets adopters combine modules à la carte.

### TODO P4.2 — Maturity assessment interactive template (shipped 2026-06-20)

Shipped as [`docs/template-maturity-self-assessment.md`](../docs/template-maturity-self-assessment.md). Guided markdown checklist covering 11 library domains across a 5-tier maturity ladder (Initial / Developing / Defined / Managed / Optimising); per-tier next-step guidance; recording template.

### TODO P4.3 — Implementation roadmap templates (shipped 2026-06-20)

Shipped as [`docs/template-implementation-roadmap.md`](../docs/template-implementation-roadmap.md). Three-phase (Floor / Operational / Year-1 close) sequence at 90 / 180 / 365 days for the reference E2 pace, with pace adjustments for E1, E3, E4 capacity tiers and for composition complexity. Designed to sequence the modules picked via the quickstart template; not per-profile.

### TODO P4.4 — Regulator interaction templates (shipped 2026-06-20)

Shipped as [`compliance/template-regulator-interaction.md`](../compliance/template-regulator-interaction.md). Five sub-templates in one consolidated document: breach notification, attestation submission, examination support, periodic report submission, regulatory inquiry response. Shape-only; jurisdiction- and sector-specific timing/format requirements live in the relevant annex or sector folder.

### TODO P4.5 — Audit evidence package templates (shipped 2026-06-20)

Shipped as [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md). Cover page, control inventory index, per-control sections (framework references, implementation and operating evidence, gaps and compensating controls, per-control sign-off), optional per-domain summaries for 50+ control packages, optional cross-reference index for shared evidence, package-level sign-off. Anti-patterns to watch and eight review questions.

### PR #137 — Overnight-work protocol: stub format for `overnight-pr.md` + audit gate 46 + pack rule amendment (2026-06-21)

Implements the maintainer-confirmed overnight-work protocol. New stub-form [`.working/overnight-pr.md`](overnight-pr.md) with `**Status:**` field; new gate 46 ([`tools/lint-overnight-file.py`](../tools/lint-overnight-file.py)) scanning the file and failing on `Status: done`; new "Overnight-work protocol" subsection in [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md) documenting the lifecycle. Three-state Status field (`stub` / `in-flight` / `done`) rather than binary so overnight PRs land cleanly while the gate still applies mechanical pressure for morning processing once a session ends. Pack `1.32.0 → 1.33.0`; spec `1.13.1 → 1.14.0`; library `2026.06.118 → 2026.06.119`. The maintainer-confirmed standard (chat message 2026-06-21 mid-PR-#135) is the closing trigger for this PR.

### PR #135 — Restructure design-decisions into its own file; clean up `overnight-pr.md` (2026-06-21)

Creates [`design-decisions.md`](design-decisions.md) as the new home for design-decision content; rotates the "Design decisions made" section out of DONE; migrates fitness-skill-specific decisions out of `overnight-pr.md`; migrates TODO's "Decisions log" section in as "Decisions explicitly dropped"; deletes [`overnight-pr.md`](overnight-pr.md) (purely procedural detail with no forward-looking value after the overnight session it documented). [`README.md`](README.md) (`.working/`) Top-level files table extended with the new file. Implements the maintainer's "DONE should be for things that are DONE; we have the .working directory for our work, let's be as organized as we can moving forward" directive. The TODO's "Decisions log" subsection was specifically called out as misplaced and migrated.

### PR #134 — Gate 45 false-positive fix: tighten queued-PR regex (2026-06-21)

Post-PR-#133 merge `push`-event CI run on `main` failed because gate 45's regex was too permissive: an `[^\n]{0,80}` window between "next/queued/pending" markers and `PR #<digit>` matched a historical parenthetical reference (`...during PR #133`) instead of the intended queued-PR target (which was a placeholder `PR #N`). Regex tightened to `[\s,:—–-]*` so the queued PR must be the immediately-following PR ref structurally, not any PR ref within 80 chars. Real-drift cases (`Next, PR #128`, `queued PR #128`, etc.) continue to match. Library `2026.06.116 → 2026.06.117`. This is gate 45's second production catch and the second post-merge-`main` failure since gate 45 shipped (PR #128); the first was a genuine drift, this was a false positive.

### PR #133 — Document the project's Canadian-first language convention (2026-06-21)

Maintainer-surfaced during PR #131's chat thread: the project's `-ized`/`-ization` orthography is Canadian (which shares the Oxford convention with American English), not American-attributed. The convention is named explicitly as **Canadian English first, Commonwealth second, other dialects last**. Doc-only PR: [`tools/lint-language.py`](../tools/lint-language.py) module docstring rewritten to name the convention as Canadian (linter behaviour unchanged); new "Language convention" section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) Conventions section; [`CONTRIBUTING.md`](../CONTRIBUTING.md) Style requirements section rewritten to lead with the convention statement instead of just the linter rule. CONTRIBUTING per-doc `1.1.0 → 1.2.0`; library `2026.06.115 → 2026.06.116`.

### PR #132 — Add Ryk Edelstein to `AUTHORS.md` (2026-06-21)

Single-line addition to the Acknowledged contributors list in [`AUTHORS.md`](../AUTHORS.md) for [Ryk Edelstein](https://github.com/fedelst). Per-doc version `1.1.0 → 1.1.1`; library `2026.06.114 → 2026.06.115`. Closes the maintainer-surfaced TODO item from PR #131 ("In the next PR, add ..."). First PR using the post-PR-#131 steady-state discipline of TODO/DONE rotation in the same PR.

### PR #131 — DONE.md infrastructure + TODO refactored to forward-looking only (2026-06-21)

Bootstrap entry (added retroactively in PR #132 — PR #131 created this file but did not add its own entry; recorded here per the discipline that every PR henceforth adds its own DONE entry). PR #131 introduced [`.working/DONE.md`](DONE.md) as the closed-TODO ledger; rotated all "PRs completed this session" (PRs #110-#130) and "Key design decisions made this session" content out of [`TODO.md`](../TODO.md) into DONE; added a new "PR finalization protocol" section to the [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md) pack rule documenting three disciplines (TODO is forward-looking; DONE keyed by backlog ID; after-merge list-next-N PRs); operationalised both in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md). Pack `1.31.0 → 1.32.0`; library `2026.06.113 → 2026.06.114`.

### PR #130 — Remove decorative gate-count narrations (2026-06-21)

Replaced 11 prose `"the N-gate audit programme"` references across 7 files with `"the audit programme"`; the spec §6 inventory remains the canonical source for both the gate list and the current count. Implements the maintainer's just-surfaced proposal that decorative counts add no information beyond what readers can derive from §6 and cost real PR friction on every gate-add. PR #128 cascaded ten such references; PR #129 cascaded one more. Gate 39 (cross-file gate-count consistency audit) retained as the defence against new decorations creeping back in. Library `2026.06.112 → 2026.06.113`. Was queued as proposal "(b)" in TODO's Queued sequence follow-up paragraph after PR #129; closed in this PR.

### PR #129 — PR #128 catch-up: TODO drift caught by gate 45 on post-merge `main` (2026-06-21)

The post-merge `push`-event CI run on `main` (commit `1ee9dda`) failed because [`TODO.md`](../TODO.md) line 47 still framed PR #128 as "Next" while PR #128 had merged. Gate 45 (TODO staleness audit, the gate PR #128 itself introduced) correctly flagged the line. This was gate 45's first production catch and is precisely the failure mode it was built to detect. The fix is mechanical TODO rotation: PR #128 moved from Queued sequence into PRs-completed list; queued sequence rebased; two design proposals from the maintainer captured as follow-ups. Library `2026.06.111 → 2026.06.112`.

### PR #128 — Gate 45 (TODO staleness audit) + PR-time-checks wrapper (2026-06-21)

New audit gate 45 ([`tools/lint-todo-staleness.py`](../tools/lint-todo-staleness.py)) catches the two TODO drift shapes that recurred across four consecutive validation sweeps (queued PR already merged; sweep cursor behind history). Bundled with [`tools/run-pr-time-checks.sh`](../tools/run-pr-time-checks.sh), a local wrapper that runs the two PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR version-bump) plus gate 45, so every gate the CI workflow runs has a local invocation path before push. Spec `1.12.1 → 1.13.0`; library `2026.06.110 → 2026.06.111`. Added TODO P4.6 (corpus-management discipline as a shareable skill).

### PR #127 — Sweep 11 iter 1 close-out (2026-06-21)

Eight in-window findings actioned: corrected the fitness report's count mismatch across six surfaces (`95/18/22/31/24 → 111/17/20/57/17`); updated [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) D1 description for dual-entry post-PR-#125; refreshed TODO and reframed its session-pause snapshot as "as-of-last-refresh" (one-time convention amendment to address the four-consecutive-sweep recurring drift); softened workflow ordering in [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md); renamed [`.working/README.md`](README.md) "Created by" column to "Origin". Library `2026.06.109 → 2026.06.110`.

### PR #126 — `.working/README.md` Activities table row for `changelog-details/` (2026-06-21)

Single-row addition to [`.working/README.md`](README.md) Activities table for the `changelog-details/` activity (the activity directory itself was introduced in PR #125 but the README row was missed). Library `2026.06.109 → 2026.06.109` (no library bump, README-only edit).

### PR #125 — CHANGELOG two-file split: root keeps lead paragraphs, detailed mirror keeps full structured entries (2026-06-21)

Splits the CHANGELOG into a two-file convention: root [`CHANGELOG.md`](../CHANGELOG.md) carries lead-paragraph summaries (adopter-facing); detailed mirror at [`.working/changelog-details/CHANGELOG-detailed.md`](changelog-details/CHANGELOG-detailed.md) carries full structured-section entries (maintainer-grade). 2926 → 675 lines in root. Delta gate (`check-changelog-on-pr.py`) extended to require lock-step modification. Pack `1.30.0 → 1.31.0`. Library `2026.06.108 → 2026.06.109`.

### PR #124 — First-ever fitness review (run r1, ten persona subagents) (2026-06-21)

First invocation of the `library-fitness-review` skill (`/fitness`) shipped in PR #120. Ten persona subagents dispatched in parallel. **111 unique findings** (17 H[critical], 20 H, 57 M, 17 L; counts originally reported as "95/18/22/31/24" approximation, corrected in PR #127). Findings are FR-1 through FR-111 in [`.working/fitness-reviews/2026-06-21-r1.md`](fitness-reviews/2026-06-21-r1.md). Library `2026.06.107 → 2026.06.108`.

### PR #123 — Sweep 10 iter 3 close-out (2026-06-21)

One in-window Medium finding actioned: TODO version-snapshot drift fix. Convergence-delta narrowing from iter 2's 7 findings to iter 3's 1 (strong narrowing but not yet empty). Library `2026.06.106 → 2026.06.107`.

### PR #122 — TODO cleanup: removed completed Steps A/C/D/E from queued sequence (2026-06-21)

Removed completed steps from the queued sequence section; renumbered next step. Pure TODO maintenance; no library content change. `Changelog: skip` per TODO's informational status (pre-dating the PR #125 dual-entry convention).

### PR #121 — Sweep 10 iter 2 close-out: post-overnight-sequence cleanup (2026-06-21)

Seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120): re-added preflight exemption for "Six rules" line (new `line_hash` post-PR-#117 content change); refreshed TODO resume-state snapshot; fixed small CHANGELOG narration claim ("(new, version 1.0.0)" → "(new)"); updated [`.working/overnight-pr.md`](overnight-pr.md) status to merged. Library `2026.06.105 → 2026.06.106`.

### PR #120 — `/fitness` skill (`library-fitness-review`) (2026-06-21)

Adds a new skill to the `dev-security/claude-rules/` pack invoked via the `/fitness` slash command. Whole-corpus library-quality review dispatching ten persona reviewers in parallel (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer). Canonical `.working/fitness-reviews/` activity layout. Pack `1.29.0 → 1.30.0`. Authored end-to-end during an overnight session under explicit maintainer authorisation; full decision log at [`.working/overnight-pr.md`](overnight-pr.md). Library `2026.06.104 → 2026.06.105`.

### PR #119 — TODO update only (session-resume context capture) (2026-06-21)

Session-resume context capture in TODO; `Changelog: skip` per TODO's informational status (pre-dating the PR #125 dual-entry convention). No library content change.

### PR #118 — Restructure `.working/<activity>/` to canonical layout (2026-06-21)

Restructured [`.working/validate-sweeps/`](validate-sweeps/) to the canonical `<activity>/{README, history, detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory going forward. The validation-sweep history file moved into the subdirectory; verbose static content moved to the subdirectory's README; the history file became a slim reverse-chronological table; per-iteration detail files are created only when findings exist. Library `2026.06.103 → 2026.06.104`.

### PR #117 — Sweep 10 iter 1 close-out: six prose-drift findings post-PRs-#114-#116 (2026-06-21)

Six in-window prose-drift findings actioned, all introduced or made visible by the three-PR `.working/` sequence (PRs #114-#116). Stale step counts in SKILL.md and slash command; stale subdir inventory in `.working/README.md`; three-way section-header drift; awkward possessive; stale "Four rules" → "Six rules". Library `2026.06.102 → 2026.06.103`.

### PR #116 — Move validation-sweep history file from `governance/` to `.working/` (2026-06-21)

Validation-sweep history is project-specific application of the validation-sweep discipline, not template content for adopters. Application belongs in `.working/`; template content (the failure-mode class taxonomy, the maintenance protocol, the false-positive accept-list rules, the dispatch-declaration discipline) lives in the [`validation-sweep` SKILL.md](../dev-security/claude-rules/skills/validation-sweep/SKILL.md). Library `2026.06.101 → 2026.06.102`.

### PR #115 — `/validate` slash command rename + per-iteration record convention (2026-06-21)

Slash command rename from `/validation-sweep` to `/validate` per the maintainer's "short ergonomic verbs for slash commands" preference. Skill name remains `validation-sweep`. Added per-iteration record convention to the validation-sweep skill (detail files only when findings; history table row for every iteration including zero-finding ones). Library `2026.06.100 → 2026.06.101`.

### PR #114 — `.working/` top-level convention infrastructure (2026-06-21)

Established the `.working/` top-level convention for maintainer working state. First of a four-PR sequence (`.working/` infrastructure, `/validate` rename + per-run records, `/fitness` skill, changelog-details migration). Created [`.working/README.md`](README.md); added `.working/` to `DEFAULT_EXEMPT_DIRS` in [`tools/lint_common.py`](../tools/lint_common.py). Library `2026.06.99 → 2026.06.100`.

### PR #113 — Sweep 9 iter 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 (2026-06-21)

Three documentation findings actioned from Subagent A's deep review of PR #112. Convergence-delta narrowing from iter 2 to iter 3. Library `2026.06.98 → 2026.06.99`.

### PR #112 — 7th governance rule (`validate-inference-before-action.md`) + gate 39 pattern P7 (2026-06-21)

New seventh pack rule [`dev-security/claude-rules/governance/validate-inference-before-action.md`](../dev-security/claude-rules/governance/validate-inference-before-action.md): action-side counterpart of the evidence-grounded-completion rule. When the next action depends on an inferred premise, validate the premise via tool call before taking the action. Gate 39 pattern P7 ("N \<word\> gates") added. Pack `1.27.0`; library `2026.06.97 → 2026.06.98`.

### PR #111 — Sweep 9 closure: Subagent C findings + Rule 5.6 (subagent-dispatch declaration discipline) (2026-06-21)

Sweep 9 closure: actioned Subagent C findings; added Rule 5.6 to the validation-sweep SKILL.md (subagent dispatch declaration: every iteration must declare which subagents were dispatched in the history register's `Subagents` column). Library `2026.06.96 → 2026.06.97`.

### PR #110 — Corpus stale gate-count fixes + gate 39 pattern P6 (2026-06-21)

Corpus-wide stale gate-count reference fixes (the cascade-class issue that PR #130 ultimately addressed at the source by removing decorative gate-count narrations). Added gate 39 pattern P6 ("N gates" without preceding qualifier). Library `2026.06.95 → 2026.06.96`.
