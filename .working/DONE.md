# DONE

Closed-TODO ledger for the GRC Documentation Library. Records work that has shipped, keyed by the original backlog ID (PR number for PR-based items; the TODO `P-X.Y` identifier for backlog items). Reverse-chronological: newest at top.

This file complements two other working-state ledgers:

- [`CHANGELOG.md`](../CHANGELOG.md): records *what landed in each PR* (file-by-file changes, version bumps, verification). Organized by PR. Adopters and downstream consumers read CHANGELOG for the full story.
- [`design-decisions.md`](design-decisions.md): records *design decisions made* (working-state and convention decisions; decisions explicitly dropped). Organized thematically.

DONE records *which backlog items each PR closed*, formatted as **scrolling battle-text**: the `tail -f` view of shipped work. Each entry is a 1-2 sentence headline a maintainer scanning the file can recognize at a glance without parsing prose. Details (file paths, version bumps, verification, rationale) live in CHANGELOG; DONE does the at-a-glance index job. Adopters reading the corpus do not need any of these three files; they are maintainer working state and live under `.working/`.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. It is exempt from corpus audit gates per the `.working/` directory exemption.

## How items get here

When a PR closes a TODO item, the maintainer (or the AI assistant under the corpus-management discipline) rotates the item from [`TODO.md`](../TODO.md) into this file as part of the PR's diff. The rotation is enforced by convention rather than by a gate, per the discipline section in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md).

The format for each entry:

- `### PR #N — FR-X (severity): short title (YYYY-MM-DD merge date)` — primary header for a fitness-remediation PR that closes one FR. Severity values mirror the TODO backlog tiers: `high[critical]`, `high`, `medium`, `low`. The Pass-1 ⚠️ confirmed-with-modification flag is informational and stays in the body, not the heading.
- `### PR #N — FR-X (sev) + FR-Y (sev): short title (YYYY-MM-DD)` — for multi-FR PRs.
- `### PR #N — Sweep N iter M close-out: short title (YYYY-MM-DD)` — for validation-sweep close-out PRs (no single FR anchor; bundle multiple findings).
- `### PR #N — short title (YYYY-MM-DD)` — for non-FR PRs (workflow/infrastructure changes).
- `### FR-X (severity) — short title (closed by PR #N, YYYY-MM-DD)` — for FR-N cross-reference entries that need separate callouts (items closed across multiple PRs or items whose own narrative deserves its own H3 separate from the closing PR's entry).
- **One or two sentences** describing what was accomplished. No file links, no version bumps, no rationale. The narrative job belongs to CHANGELOG; the at-a-glance index job belongs to DONE.

The heading convention was harmonised with TODO's backlog format in PR #163 (2026-06-21) so a maintainer reading either file can scan FR-N + severity at the heading level without parsing the body paragraph. The "scrolling battle-text" body convention (1-2 sentences, no links, no version bumps) was adopted in PR #174 (2026-06-21); PR #175 retroactively shortened earlier entries to the new shape.

---

## Closed items

### PR #294 — FR-120 + FR-155 + FR-53 + FR-109 + DD-6/DD-7 + FR-75 + FR-76 (medium/low): governance/registers + ESG bundle (PR-H) (2026-06-23)

Seven governance/register/ESG fitness items shipped as PR-H: the exception policy's 180-day baseline attribution is softened to state that neither NIST 800-53 CA-6 nor ISO 27001 Clause 9.2 prescribes a fixed interval (FR-120); the enterprise-risk policy's stale CSA CCM v3 "GRM" domain id is corrected to v4.1 "GRC" (FR-155, one line — the other two cited files were already correct); the ingestion spec now documents the Classification (lifecycle) vs Confidentiality (content-sensitivity) distinction so the two metadata fields are non-redundant (FR-53, decided: document not deprecate); the governance-library charter's dense purpose paragraph is tightened (FR-109); the AI-compliance checklist's AI-log retention is reconciled up from 12 months to the canonical 7 years and a matching AI decision-and-detection-logs row (7 yr; ISO 42001 + EU AI Act Annex IV) added to the data-retention schedule, also fixing a broken "12 months per logging standard" cross-reference (DD-6/DD-7); the ESG disclosure guideline gains a qualitative double-materiality assessment process for the materiality threshold (FR-75); and the sustainability framework gains qualitative ESG escalation triggers, CIO to ERC to Board (FR-76). B2 (five EDPB/WP29 soft-law citations) was deferred from this PR: verifying the citation titles/years/bodies needs web egress that is policy-blocked this session.

### PR #291 — FR-153 + BYOD-MDM/MAM + FR-90 + FR-84 + FR-85 + FR-86 (medium/low): security/crypto bundle (PR-F) (2026-06-23)

Six security/crypto fitness items shipped as PR-F: the encryption policy's password-based KDF requirement is updated to Argon2id-preferred (OWASP min params) or PBKDF2-HMAC-SHA256 at 600,000 iterations (SHA-512 at 220,000), replacing the stale unqualified 310,000 (FR-153); the BYOD policy is reframed from MAM-only to present MDM and MAM as adopter-selectable deployment models with explicit enrolment-consent requirements for MDM (BYOD, maintainer-directed); the developer-security standard gains CSP / Trusted Types / HSTS-preload browser-hardening requirements (FR-90); the patch-management regression-testing checklist is reformatted into a tick-through table artefact (FR-84); the breach-response 24-hour initial assessment now assigns a per-question lead (DPO / CISO / Legal) instead of diffuse joint ownership (FR-85); and the recovery runbook's communications section now cross-references the Crisis Communication Plan (FR-86).

### PR #290 — FR-64 + FR-65 + FR-66 + FR-78 + FR-152 + FR-69 + FR-68 + FR-156 + FR-157 + FR-158 (medium/low): adopter/docs-UX bundle (PR-E) (2026-06-23)

Ten adopter-experience fitness items shipped as PR-E: CONTRIBUTING now points new-sector/jurisdiction contributors at exemplar annexes to mirror (FR-64); the adopter guide's upstream-sync section now covers merge conflicts, adopter-side gate relaxation (relax-and-document), and version-monotonicity, plus a new "running the audit toolchain on your fork" note on the PII/secrets gates and the exemption mechanism (FR-65, FR-66); the framework-architecture doc drops the "audit theatre with nicer fonts" maintainer aside (FR-78); the quickstart "Next steps" is reordered to the portal's canonical workflow sequence with startup-roadmap set apart as the "add later" path (FR-152); the 6 / 15 / ~25 starter-set sizes are now cross-referenced as nesting rather than competing across the quickstart, adopter guide, and decision tree (FR-69); the startup-roadmap's incoherent "minus the A1 elements" wording is corrected so the skip applies to the optional A1 module not the mandatory baseline (FR-68); the adopter guide gains an enforcement/disciplinary-clause "what to change" row (FR-156); "DPO" is expanded on the quickstart Day-1 path (FR-157); and the adopter guide adds shortest-binding-window guidance for multi-regulator overlap (FR-158).

### PR #287 — FR-147 + FR-148 + FR-101 + FR-102 + FR-100 + FR-77 + FR-83 (medium): assurance/3LoD + audit/CAPA bundle (2026-06-23)

Seven Medium fitness items shipped as one PR-C: the internal-audit standard now acknowledges the audit-planning procedure's 15-business-day final-report extension (FR-147); the CAPA procedure anchors the policy's 90-business-day post-implementation effectiveness validation by Internal Audit or Compliance (FR-148); the assurance-map closure step now names first-line-proposes / second-line-confirms sign-off (FR-101); the change-management procedure gains a compensating-control pathway as an alternative to deferring an untested-rollback change (FR-102); the cloud security configuration baseline expands its ISO row and adds a per-section CIS/ISO/NIST mapping table (FR-100); the key-terms register defines the Three Lines Model (FR-77); and the security IR and privacy breach procedures each gain a one-page 60-minute / 4-hour / 24-hour incident-command execution checklist (FR-83, whose TODO gloss "independent challenge" was a mislabel for the incident-command checklist).

### PR #283 — FR-161 + FR-162 + FR-163 + FR-146 (medium): risk/AI register vocabulary aligned to canonical ERM set (2026-06-23)

Aligned the AI risk register and AI risk-methodology annex Treatment Option lists to the canonical six (Avoid / Mitigate / Transfer / Accept / Exploit / Enhance), and reconciled the retired/conflated Status values in the AI register and the ERM-template sample rows to the canonical lifecycle Open / Closed. PR-B of the XS/S batch.

### PR #282 — FR-142 (high) + FR-143 (high): AI-procedure step roles + de-looped supplier escalation (2026-06-23)

FR-142: added a "Roles and responsibilities" subsection to both AI assessment procedures (model-risk and system-impact), naming the AI Governance Lead, the model/system owner, and the AI Governance Approver/Council. FR-143: fixed the circular DPO→CISO→Data Protection Officer escalation row in the supplier-onboarding procedure to terminate at the Chief Risk Officer. First PR of the XS/S batch-reduction sweep.

### PR #279 — DD-9 (low): DR backup-requirements header broadened to "All systems" (2026-06-23)

Broadened the disaster-recovery plan's "Backup and restore requirements" header from "All Tier 1 and Tier 2 systems must have:" to "All systems must have:", matching its bullets which already span all four tiers after the FR-139 / Sweep-28 edits. Also closed the three #278 `/validate-pr` bookkeeping findings in the same PR.

### PR #278 — DD-1 (low): new-entries-only CHANGELOG dash gate (D3) (2026-06-23)

Resolved DD-1 with a PR-time delta gate (D3, `check-changelog-dash-on-pr.py`) that flags em/en dashes only in lines a PR adds to `CHANGELOG.md`, leaving the ~130 historical dashes untouched. Scope narrowed from "extend to all of CHANGELOG" at action time after the dash count proved far larger than the backlog item assumed.

### PR #273 — count-gate coverage: stale-count fix + gate-39 P8 (2026-06-23)

Fixed the stale "32 automated audits" in the library-health-report template (now count-agnostic; the programme has 47 gates) that PR #272's `/validate-pr` surfaced, and broadened gate 39 with pattern P8 (`<N> automated audits`) so the idiom that escaped patterns P1-P7 is now caught. Closes the #272 out-of-window finding + the broaden-the-count-gate P4 candidate.

### PR #272 — FR-166 (high): corpus listing-surface completeness gate + authoring tool (2026-06-23)

Shipped audit gate 47 (`lint-listing-surface-completeness.py`), which hard-gates the MECHANICAL listing surfaces (the document-index register + all 11 domain READMEs) against the taxonomy active-document set, with root-level meta-specs exempt by a documented rule; plus `tools/suggest-listing-surfaces.py`, which reports MECHANICAL present/missing + ranked SEMANTIC candidates for a new doc. Fully wired across all four audit-programme surfaces with a regression fixture; SEMANTIC surfaces (matrices, glossary, Related Documents) left to suggestions + a `/validate` coverage-drift check, not a hard gate.

### PR #271 — Sweep 28 `/validate` close-out: DR Tier-2 backup-cadence fix (2026-06-23)

The `/resume` compensating-control corpus-wide `/validate` found one in-window defect: FR-139/#265 fixed Tier 1's backup cadence but left Tier 2 on "daily" while binding it to a 4-hour gap/RPO, reproducing the "compliant system permanently in P2 escalation" trap one tier down (and escaping #265's own `/validate-pr`). Fixed: Tier 2 cadence now "at least every 4 hours", daily scoped to Tier 3/4.

### PR #267 — FR-141 (high): remove invented PIPEDA breach "72-hour target" (2026-06-23)

PIPEDA's Breach of Security Safeguards Regulations set no fixed statutory clock ("as soon as feasible"), so the invented "(72-hour target)" was removed from the Canada-federal breach-notification deadline at both surfaces the bare-token search found: the privacy breach-response procedure (§6.2 jurisdiction table) and the security incident-response procedure (§6 regulatory-notification table). Both now read "As soon as feasible (no fixed statutory deadline)". The security-incident-response cell's separate "CPPA (Canada)" label remains for the deferred broader-CPPA sweep.

### PR #265 — FR-139 (high[critical]): DR Tier-1 backup cadence meets the 1h RPO (2026-06-23)

Resolved the DR-plan self-contradiction where Tier 1 carried a 1-hour RPO but the backup section mandated "daily backups" and allowed a "24-hour gap" (so every Tier-1 backup would permanently breach the RPO and trigger P2 escalation). The backup cadence now requires continuous/near-continuous data protection for Tier 1's 1h RPO, and the backup-gap limit is aligned per tier (1h Tier 1, 4h Tier 2, 24h/72h Tier 3/4). **Completes the 6-item H[critical] locked-criticals batch (FR-134 through FR-139).**

### PR #264 — FR-138 (high[critical]): scrub CPPA-as-live (3 named docs) (2026-06-23)

Removed Consumer Privacy Protection Act (CPPA, lapsed Bill C-27) treatment-as-in-force from the three named privacy documents: the data-subject-rights procedure (rights table + summary table + §8.3 + intro now cite PIPEDA Schedule 1 Principle 9/Principle 3, with a new "Canadian legal basis" note explaining PIPEDA lacks erasure/automated-decision rights and CPPA is pending reintroduction), the breach-response procedure (Canada federal basis = PIPEDA Breach of Security Safeguards Regulations; CPPA pending), and the privacy policy (rights + control-mapping cells). Broader corpus CPPA-as-live mentions (security incident-response, document-index framework tags, matrices, other privacy templates) deferred to a follow-up sweep.

### PR #263 — FR-137 (high[critical]): DSAR retention harmonized to 3 years (2026-06-23)

Aligned the DSAR-record retention to the authoritative schedule's 3-year value: the records standard's DSR row and the data-subject-rights procedure §9.2 moved from "2 years post-closure" to "3 years post-closure", citing `register-data-retention-schedule.md` (Data subject access request records: 3 years, GDPR Article 30). The register was already canonical and unchanged.

### PR #262 — FR-136 (high[critical]): log-retention schedule authoritative (2026-06-23)

Resolved the log-retention conflict by making `register-data-retention-schedule.md` authoritative: the logging standard §4.1 (flat "seven years") and the records standard's IT/Security row ("1 to 3 years") now defer to the schedule's tiered, by-log-class periods. Reconciled a downstream citer (security-monitoring §298, which cited §4.1 for a 7-year AI-decision-log retention) onto the established ISO/IEC 42001 + EU AI Act Annex IV basis, preserving its 7-year retention. Also forward-corrected PR #261's over-broad TLS verification claim.

### PR #261 — FR-135 (high[critical]): TLS 1.3 everywhere (2026-06-23)

Migrated every org TLS-floor surface from "TLS 1.2 minimum" / "1.2+" to TLS 1.3 (or stronger), with TLS 1.2 moved to the prohibited set, across the security quick-reference, baseline reference, mobile-app-security, production-security (B2B/EDI adapter, unconditionally), the healthcare HIPAA annex, and the pack cryptography + MCP-security rules. Two surfaces deferred to maintainer review: `core/owasp.md` (represents OWASP ASVS, which permits 1.2) and `languages/go.md` (TLS code example needs coherent rewrite).

### PR #260 — FR-134 (high[critical]): one canonical risk-scoring scale (2026-06-23)

Aligned the enterprise risk standard's §5.2 likelihood labels (Rare→Almost Certain ⇒ Very Low→Very High) and score-to-rating bands (1-5/6-10/11-15/16-25 ⇒ 1-4/5-9/10-16/17-25) to the canonical risk-assessment procedure, and fixed the register template's stale likelihood labels, so a given score now yields the same rating/cadence/escalation across all three risk documents. Fourth surface (concentration-risk register) and the impact-5 label divergence surfaced to the maintainer, not folded in.

### PR #258 — P4.0: project-integrity.md tenth governance rule (2026-06-23)

Distributed the PRIMORDIAL RULE (Quality > Speed > Cost apex ordering) as the tenth pack governance rule `project-integrity.md` + byte-identical `.claude/rules/` mirror, wired across all three enumeration surfaces + sync-map + rule-count. Closes TODO P4.0; resolves the PRIMORDIAL RULE's "queued as P4.0" forward-reference.

### PR #257 — guardrail-review skill + /guardrails (2026-06-23)

Shipped the fifteenth pack skill `guardrail-review` (`/guardrails`): the periodic structural-integrity review of the governance machinery (rules, skills, gates, wiring surfaces) for overlap, gap, and drift the mechanical parity gates cannot judge. Closes the trust-recovery-batch structural-review codification item; wired across SKILL + command + PAIRS + README tree + version bumps.

### PR #254 — /trust-recovery convenience wrapper (2026-06-23)

Added the thin non-paired `/trust-recovery` command that sequences the escalation suite (full-clone check → `/full-qa` → `/fitness` → hold for sign-off). Closes the optional-wrapper codification item.

### PR #252 + #253 — Trust-recovery routing convention severity-tiered (2026-06-22/23)

Revised the trust-recovery findings-routing convention from "every finding to one top tier" to severity-tiered (H[critical]/High → top tier, Medium/Low → next; nothing dropped), propagated across the rule, both SKILLs, the commands, and both CLAUDE.md bullets (#252), then completed two same-file spots the propagation missed (#253). Closes the routing-revision codification item.

### PR #247 — Session migration protocol + bookkeeping cleanup (2026-06-22)

Adds [`.working/session-handoff.md`](session-handoff.md) + the `/resume` command + the CLAUDE.md session-migration / PR-close-out-checklist section, so a fresh session resumes with one command (the long-session-degradation defence). Also rotated FR-164 and the shipped codification-checklist items into DONE, fixed a stale governance-rule count in TODO, and carried the #246 validate-pr/retro rows.

### PR #246 — Ninth governance rule trust-recovery-escalation + FR-164 (2026-06-22)

Shipped the ninth pack governance rule (the trust-recovery escalation tier: /full-qa + /fitness suite, top-priority findings routing, maintainer-sign-off termination) across all three enumeration surfaces + the `.claude/rules/` mirror. Closed FR-164 (collection-enumeration docstring "seven" → "nine").

### PR #245 — PRIMORDIAL RULE: project integrity (2026-06-22)

Added the apex Quality > Speed > Cost integrity rule to `.claude/CLAUDE.md`; queued P4.0 to distribute it as a project-agnostic pack governance rule.

### PR #244 — deep-qa-review skill (/full-qa) (2026-06-22)

Codified the trust-recovery AI-failure-pattern forensic pass as the `deep-qa-review` skill + `/full-qa` command, with the shallow-clone full-clone step-0 rule baked in.

### PR #243 — Trust-recovery suite routing + re-tier (2026-06-22)

Ran `/full-qa` + `/fitness` r2 (32 findings; a shallow-clone gate-31 false positive caught and excluded); routed and re-tiered findings to TODO P1/P2/P3 after maintainer sign-off.

### PR #242 — Sweep 22 iter 1 close-out + discipline-failure corrective actions (2026-06-22)

Sweep 22 reconciled 11 consecutive PRs (#231-#241) where the orchestrator had recorded "abbreviated spot-check" rows in `validate-pr/history.md` without dispatching the formal Subagent A; 4 in-window errors surfaced (treatment-vocab propagation gaps in 4 risk-domain files from PR #238/#239 surface drift), all fixed. SKILL files, pack-rule copies, and `.claude/CLAUDE.md` all updated with explicit abbreviation prohibition and throughput-pressure clause; P4.6 mechanical-enforcement gate candidate queued.

### PR #241 — Closes FR-97 + FR-98 (P2.3 cross-framework matrix bundle, both M, S) (2026-06-22)

`governance/matrix-cross-framework-alignment.md` v1.1.4: ISO 31000 clause numbers corrected against actual ISO 31000:2018 §§6.4.2/6.4.3/6.5/6.6/6.3/5.3 (closes FR-97). `compliance/annex-nis-2-implementation.md` v1.1.0: Article 21.2 sub-measures table gains Evidence class column for all 10 sub-measures (closes FR-98). PR-E in Batch 2.

### PR #240 — Closes FR-93 + FR-94 (P2.6 KRI/KPI bundle, both M, S) (2026-06-22)

`risk/register-key-risk-indicators.md` v1.1.0: KRI schema gains Red-Threshold Escalation Owner + Red-Threshold Evidence Class fields (closes FR-93). `risk/register-assurance-map.md` v1.1.0: Linked-controls field text expanded to name it as adopter-defined, explain the placeholder-ID convention, and bootstrap path (closes FR-94). PR-D in Batch 2.

### PR #239 — Closes FR-12 cross-doc (M, S): procedure-risk-register treatment vocab aligned with ERM standard canonical 6 (2026-06-22)

`risk/procedure-risk-register.md` v1.1.0: Step 8 "Select Treatment" now references the standard's canonical 6 options (Avoid/Mitigate/Transfer/Accept/Exploit/Enhance). "Monitor" / "Further Analysis" remapped to Treatment Status workflow values (Pending / In Progress / Complete). Register-field row split into Treatment Option + Treatment Status to match PR #238's standard §7.1 schema. PR-C in Batch 2.

### PR #238 — Closes FR-118 (H, S): ERM §6/§7 treatment-vocab internal inconsistency resolved (2026-06-22)

`risk/standard-enterprise-risk-management.md` v1.6.0: §6 gains terminology paragraph distinguishing Treatment Option (6 choices) / Treatment Status (workflow: Pending/In Progress/Complete) / Status (risk-record lifecycle: Open/Closed). §7.1 register fields update: Treatment Status field added; Status value set narrowed from "Open/Mitigated/Accepted/Closed" to "Open/Closed" with explanatory prose. Closes the ambiguity surfaced during Pass-2 reshape (Avoided risks had no clean Status value). PR-B in Batch 2.

### PR #237 — Closes FR-36 (H, S): GDPR Article 8 child-consent age table per Member State (2026-06-22)

`privacy/jurisdictions/annex-privacy-european-union.md` v1.1.0: new section between Cross-border-transfers and Enforcement covering 30 Member States (27 EU + 3 EEA) with each state's chosen age (13/14/15/16) and national implementing-law citation. `privacy/framework-childrens-data.md` v1.0.5 row updated to cross-reference the new table. PR-A in Batch 2 effort-first run. Also carries Sweep 21 zero-finding history row + PR #236 register rows.

### PR #236 — Closes P7 maintainer decisions (A2 + B4 + FR-47): role-authority cross-ref + canonical-citations soft-law scope (2026-06-22)

PR-G in Batch 1 effort-first run. **A2**: `governance/register-role-authority.md` v1.5.1 DPO row gains cross-reference to the charter's Article 38(3)(6) independence + conflict-of-interest framework. **B4**: `governance/register-canonical-citations.md` v1.5.0 scope extended to soft-law supervisory guidance; new "Soft-law supervisory guidance" section added with WP243 rev.01 (Article 29 Working Party Guidelines on DPOs, endorsed by EDPB May 2018) as first entry. **FR-47**: formally closed (surface-consolidated in PR #218; maintainer review now recorded).

### PR #235 — Closes C2 convergent finding bundle (FR-121+122+123+124+125+126): emergency-access operational clarity (2026-06-22)

`security/procedure-access-control.md` v1.2.0: 6 fixes ship with maintainer-approved sample-data defaults + section-level "Sample data, adjust upon adoption" callout. FR-121 material-harm defined (P1/P2 incident threshold); FR-122 declared-incident tied to P1/P2 severity; FR-123 Delegated Security Lead role row added (sample data: senior IRT member or deputy CISO); FR-124 access-review revocation timeline contradiction resolved (24h window for revocation processing post-flag, distinct from immediate-upon-instruction case); FR-125 emergency-access revocation gains 30-min/30-min escalation chain (Identity Team → SOC L2 → CISO); FR-126 auto-escalation made explicit (ITSM SLA timer, no human trigger). PR-E in Batch 1.

### PR #234 — Closes FR-67 (L, XS): zero-headcount-with-contractor sub-tier E0 in Dimension E (2026-06-22)

`docs/template-startup-roadmap.md` v2.2.0: new E0 sub-tier inserted before E1 in the Dimension E (GRC team capacity) ladder, covering the case where GRC function is entirely outsourced to a third-party contractor or fractional consultant. Adopter retains accountability; contractor executes. Same artefact subset as E1; operational difference is who holds the pen. PR-D in Batch 1.

### PR #233 — Closes FR-89 + FR-91: security XS bundle (JWT algorithm-key-type binding + webhook signing precision) (2026-06-22)

`dev-security/standard-api-security.md` v0.0.5: Token validation row gains JWT algorithm-key-type binding requirement per RFC 8725 (prevents RSA-public-key-as-HMAC-secret confusion). Webhook signing row gains canonical-string definition + constant-time comparison requirement. Replay-prevention row gains explicit 5-minute replay window + seen-nonce cache. 2 L XS items closed. PR-C in Batch 1 effort-first run.

### PR #232 — Closes FR-107 + FR-108 + FR-111: newcomer-UX bundle in adopter-guide (2026-06-22)

`docs/adopter-guide.md` v1.2.0: new "Two reference registers you will need early" subsection surfaces both the Glossary (acronyms + external-domain terms) and the Key Terms register (library-internal GRC concepts) BEFORE the How-the-library-is-meant-to-be-used section, explaining the split-by-term-class. Tier 1 starter set gains a "4-6 hours" reading-time estimate plus "if you only read three" pick (Charter + Framework + Role Authority Register). Closes 3 Low-severity XS items in one PR. PR-B in Batch 1 effort-first run.

### PR #231 — Closes FR-112 (M) + FR-131 (FYI): adopter-facing maintainer-context cleanup (2026-06-22)

`README.md` line 58 audit-toolchain framing clarified (toolchain is maintainer's QA machinery, not an adopter dependency). `docs/template-quickstart.md` line 39 risk anchor switched from risk-register procedure to enterprise risk policy, aligning the quickstart core baseline with the adopter-guide Tier 1 starter set. Per-doc template-quickstart `3.0.0 → 3.0.1`. First PR in the effort-first batching run (Batch 1).

### PR #230 — TODO reorganization (maintainer-directed): every item fits into P1-P7 priorities (2026-06-22)

Restructured `TODO.md` from 453 lines (mix of per-topic sections + dedicated fitness-review backlogs) to a priority-based layout: P1 Urgent quality (H[critical] + H, 14 items) / P2 Substantive improvements (M, ~30) / P3 Low-priority cleanup (L + FYI, ~16) / P4 Adopter experience (5 process/meta) / P5 Content expansion (8 country/regulator subsections) / P6 Domain-level (5 new-domain items) / P7 Awaiting maintainer decision. Fitness review backlogs from both 2026-06-21 r1 and 2026-06-22 r1 distributed by severity into matching priorities. "Investigation / blocked" promoted to P7. "Critical user feedback" renamed "Standing conventions" as meta-section. Item shape standardised: `**FR-N (severity, effort)**: description with location reference`. Also carries deferred PR #229 /validate-pr + /retro register rows.

### PR #229 — /validate Sweep 20 iter 1 close-out: 3 glossary entries + cross-doc drift fix (2026-06-22)

Sweep 20 iter 1 (post PRs #220-#228) surfaced 4 in-window warnings + 2 maintainer-surfaced notes. Fixed: 3 new glossary entries (AEAD per RFC 8439 + NIST SP 800-38D; CIIO per Cybersecurity Law of China + PIPL Arts 38/40; HKDF per RFC 5869); cross-reference sentence added to `privacy/policy-privacy-and-data-governance.md:46` pointing at the charter's Article 38(6) framework. Pattern observed: 3 newly-introduced acronyms missed glossary entries in same batch; worker-brief candidate queued. Maintainer-surfaced: A2 (DPO row in role-authority register) and B4 (WP243/EDPB scope in canonical-citations register). Also carries deferred PR #228 /validate-pr + /retro register rows.

### PR #228 — Closes FR-42 (medium, P2.1): DPO independence Article 38(3) + conflict-of-interest Article 38(6) framework (2026-06-22)

`privacy/charter-privacy-management-programme.md` previously had a one-line "Interim Accountability" note declaring the CIO assumes DPO responsibilities. Added subsection making the Article 38(6) conflict (CIO acting as DPO) visible rather than silent: Article 38(3) 3-row independence requirements; Article 38(6) WP243 conflict-of-interest list; explicit "known conflict" framing with 3 adopter paths (formal DPO designation, mitigation controls, exemption analysis); 5-row mitigation controls table; cross-regime equivalents (UK GDPR, LGPD Art 41, PIPL Art 52, India DPDP). Per-doc `1.4.0 → 1.5.0`. Also carries deferred PR #227 /validate-pr + /retro register rows.

### PR #227 — Closes FR-40 (medium, P2.1): PIPL Articles 38-40 cross-border outbound mechanics operationalised (2026-06-22)

`privacy/procedure-privacy-impact-and-cross-border-transfer.md` previously had one line on PIPL cross-border. Expanded into 7-step workflow covering applicability + CIIO assessment, Article 38 mechanism selection (5-tier volume table with 2024 CAC Provisions safe harbors and thresholds), Article 39 separate consent, Article 40 CIIO domestic-storage default, PIA per Article 55, documentation/re-assessment cadence, and coordinated triggers across regimes. Per-doc `1.4.1 → 1.5.0`. Also carries deferred PR #226 /validate-pr + /retro register rows.

### PR #226 — Closes FR-39 (medium, P2.1): EU representative Article 27 appointment process (2026-06-22)

`privacy/charter-privacy-management-programme.md` previously mentioned the EU representative only in passing. New subsection under Privacy accountability structure covering Article 3(2) trigger, Article 27(2) 4-criterion exemption, Article 27(3)(4) representative criteria, 7-step designation process, maintenance triggers, Article 27(5) liability clarification, and cross-regime equivalents (UK GDPR, LGPD, PIPL Art 53, India DPDP, Saudi PDPL). Per-doc `1.3.3 → 1.4.0`. Also carries deferred PR #225 /validate-pr + /retro register rows.

### PR #225 — Closes FR-38 (medium, P2.1): GDPR Article 12(5) assessment checklist (2026-06-22)

`privacy/procedure-data-subject-rights-management.md` §7 expanded from one line on Article 12(5) into a 7-subsection checklist: default free of charge; 4-criterion manifestly-unfounded test; 4-criterion manifestly-excessive test; either/or action options (fee or refuse); 5-step burden-of-proof documentation; reasonable-fee cost-recovery calculation; cross-regime equivalents (UK GDPR, LGPD, PIPL, CPPA/PIPEDA, CCPA/CPRA, APPI). Per-doc `1.3.5 → 1.4.0`. Also carries deferred PR #224 /validate-pr + /retro register rows.

### PR #224 — Closes FR-37 (medium, P2.1): Joint controller arrangement template (Article 26) (2026-06-22)

New template `privacy/template-joint-controller-arrangement.md` (v1.0.0) covering GDPR Article 26 joint controller arrangements with 9 sections (identification, joint processing, allocation of GDPR responsibilities table, operational coordination, liability, termination, cross-regime alternatives for UK GDPR / LGPD / PIPL / India DPDP / CPPA / CCPA, documentation, essence-of-arrangement publication). Cross-listed in privacy/README and document-index register. Also carries deferred PR #223 /validate-pr + /retro register rows.

### PR #223 — Closes FR-49 (medium, P1.5): H2 label drift "Governance" → "Governance and accountability" (14 files, 2026-06-22)

14 files used bare `## Governance` H2; canonical form `## Governance and accountability` (20+ uses). Renamed via line-anchored regex (`^## Governance$`) so `## Governance Council` etc. were preserved. Per-doc Version patch-bumps; taxonomy/portal/maturity-scorecard regenerated. Also carries deferred PR #222 /validate-pr + /retro register rows.

### PR #222 — Closes FR-82 (medium, P1.6): AI/model crypto "key hashing" ambiguity (2026-06-22)

`security/policy-encryption-and-key-management.md:56` "AI and Model Data" row's `"AES-256 + key hashing (SHA-512)"` conflated encryption, integrity, and key derivation; SHA-512 alone is NOT a KDF. Replaced with explicit per-purpose specification: AES-256-GCM (AEAD encryption with built-in integrity); HKDF-SHA-256 for key derivation from high-entropy material; Argon2id (or scrypt) for password-derived keys; explicit note that SHA-512 alone is a hash, not a KDF. Per-doc `1.3.1 → 1.3.2`. Also carries deferred PR #221 /validate-pr + /retro register rows.

### PR #221 — Closes FR-33 (H[critical]): GDPR Article 36 prior-consultation pathway (2026-06-22)

Step 5 of `privacy/procedure-privacy-impact-and-cross-border-transfer.md` previously conflated internal ERC executive sign-off with the GDPR Article 36 regulatory prior-consultation pathway. Restructured into three substeps: 5.1 internal escalation (prior content), 5.2 NEW Article 36 prior consultation (trigger per Art 36(1), six-item content table per Art 36(3), 8+6 week timeline per Art 36(2), supervisory authority Art 58 corrective powers, 5-step interaction with internal pathway, non-EU equivalents to LGPD/PIPL/UK GDPR), 5.3 documentation requirements split by pathway. Per-doc `1.3.4 → 1.4.0`. Also carries deferred PR #220 /validate-pr + /retro register rows.

### PR #220 — Sweep 19 iter 1 close-out + deferred PR #219 /validate-pr + /retro rows (2026-06-22)

/validate corpus-wide sweep on the post-PR-#219 state surfaced 2 in-window warnings in `governance/guideline-minimum-viable-governance-structure.md` (lines 67 and 114, stale "CPO" in executive-role enumerations missed by PR #218's spelled-out-only rename script). Both fixed; per-doc Version `1.0.1 → 1.0.2`. Pattern now at second occurrence (signal stage): "corpus-wide rename script: incomplete substitution coverage" — queued worker-brief candidate strengthened. Carries PR #219 /validate-pr history row (0 findings) and /retro register row.

### PR #219 — At-top "Role-name convention" notes in 24 privacy-relevant docs + PR #218 /validate-pr fixes (2026-06-22)

Follow-up to PR #218's DPO-canonical flip. Adds a blockquote callout note immediately after the metadata block (before the first H2 heading) in 24 privacy-relevant documents (privacy core 16, AI 3, supply-chain 3, security 1, governance 1) naming **Data Protection Officer (DPO)** as canonical, **Chief Privacy Officer (CPO)** as adopter substitution, and pointing to `governance/register-role-authority.md`. Bundles two PR #218 /validate-pr fixes per the recursion-avoidance rule: `tools/build-portal.py:95` "Data Protection Officer or Data Protection Officer" collapse fix (regen `docs/portal.md`); `risk/register-key-risk-indicators.md:142` stale "CPO" → "DPO" replacement. /validate-pr record + history row + /retro register row all carried in this PR. **No formal FR closed** (PR #218 closed FR-46/-47); this is the operational follow-through.

### PR #218 — FR-46 DPO consolidation (medium): canonical flipped to Data Protection Officer (2026-06-22)

Reverses the CPO-canonical direction of PR #210 (Privacy Officer → Chief Privacy Officer rename) + PR #217 (closed unmerged when maintainer redirected). Maintainer-directed canonical: **Data Protection Officer** — globally-applicable, legislatively mandated in many regimes (GDPR Art 37, LGPD Art 41, India DPDP Act 2023 §10, Malaysia PDPA, etc.). Canonical surfaces flipped: register-role-authority CPO row → Data Protection Officer row with adopter-customisation note; glossary DPO entry extended; privacy/README Role terminology section added. Corpus prose rename across 73 files via one-shot Python script with synonym-pattern pre-cleanup; ~30 OWNER-FIELD metadata flips; build-portal.py + portal + maturity-scorecard + taxonomy regenerated. **PR-2 follows**: at-top "Role-name convention" notes in privacy-relevant docs.

### PR #214 — Overnight-PR morning processing + PR #213 batched items (2026-06-22)

Morning-processing PR for the overnight session ending at PR #213: routed two design decisions (FR-104 and FR-130 explicit-drop closures) into `.working/design-decisions.md`, transitioned `.working/overnight-pr.md` back to stub form, and updated TODO and Next-up recommendations to reflect FR-119 / FR-14+FR-114 closures. Also carried the PR #213 batched items per the recursion-avoidance rule: stale forward-ref fix in `validation-sweep-pr-scoped/SKILL.md:175`, validate-pr history row for PR #213, improvement-log row for PR #213 with pattern observation #1 surfaced (new-skill drafting checklist candidate).

### FR-104 (medium) — decision-tree per-regulation context not pursued (decided by maintainer, recorded PR #214, 2026-06-22)

Maintainer decided 2026-06-22 not to add per-regulation context to decision-tree §1.4. Rationale logged at [`.working/design-decisions.md`](design-decisions.md) § Decisions explicitly dropped.

### FR-130 (medium) — decision-tree portal entry-point reorder not pursued (decided by maintainer, recorded PR #214, 2026-06-22)

Maintainer decided 2026-06-22 to keep README at decision-tree item 1; portal reorder not pursued. Rationale logged at [`.working/design-decisions.md`](design-decisions.md) § Decisions explicitly dropped.

### PR #213 — Continuous process-improvement loop: /retro skill + improvement-log register (2026-06-22)

New pack skill `pr-retrospective` (slash command `/retro`) and the paired `.working/improvement-log.md` register. Post-merge retrospective on each successful PR; output is one entry per PR; recurring patterns surface as candidates for pack-rule updates / worker-brief additions / new audit gates. Wired into PR workflow step 5b in CLAUDE.md. Closes the three-layer learning loop (worker-brief template + apply-time catch tracking + PR retrospective). Pack `1.44.1 → 1.45.0`.

### PR #212 — FR-14 + FR-114 (H[critical]): CMMI 5-tier maturity reconciliation (2026-06-22)

Maintainer-confirmed canonical: CMMI 5-tier (Initial/Managed/Defined/Quantitatively Managed/Optimized). Two surfaces aligned: template-maturity-self-assessment.md (Tier 2 Developing→Managed, Tier 4 Managed→Quantitatively Managed, Tier 5 Optimising→Optimized, all definitions extended with CMMI process-property language); register-digital-trust-and-assurance-metrics.md (DTI thresholds replaced from 4-tier variant with even 1.0-band 5-tier CMMI). Framework already canonical (no change). Closes the single largest cross-document issue in either fitness review.

### PR #211 — FR-119 (medium): Risk Owner unification across ERM standard + exception policy (2026-06-22)

Maintainer-approved (decision 9): same role. ERM standard §3 Risk Owner extended from 5 to 6 accountability actions (added exception-request validation); §9.2 evidence table extended to 6 rows. Exception policy §2 cross-references the canonical ERM definition. **Convergent Finding C1 (Risk Owner role insufficiency) now fully closed** across FR-115/116/117/119.

### PR #210 — FR-46 Privacy Officer rename (medium); DPO assessment surfaced (2026-06-22)

Maintainer-approved (decision 6): "Privacy Officer" not preceded by "Chief" → "Chief Privacy Officer" corpus-wide. 36 files modified, per-doc Version+Date patch bumped. DPO scope assessment: strong evidence that DPO and CPO are the same role (canonical register has only one entry, 8+ explicit equivalence statements, jurisdictions treat DPO as the privacy lead). DPO consolidation queued for separate maintainer go-ahead with named options A/B/C.

### PR #209 — FR-52 (medium): Review-frequency "AND" form (2026-06-22)

Maintainer-approved (decision 5): canonical review-frequency form is "annually AND on material change" (both triggers required). Two corpus documents using OR form ("Annual or upon ...") converted to AND form.

### PR #208 — FR-51 (medium): ISO 27001 Annex-form sweep — 12 files (2026-06-22)

Maintainer-approved (decision 4): canonical form is `Annex A.X` with prefix. Corpus-wide sweep converted `27001 A.X` → `27001 Annex A.X` across 7 corpus files + 5 pack SKILL.md files. Pattern tightly anchored on `27001` to avoid disturbing ISO 42001/27017/27018/27701 references. Multi-control `/`-separated lists got single Annex prefix per publisher convention.

### PR #207 — FR-50 (medium): NIST citation format sweep — 50 files, 91 occurrences (2026-06-22)

Maintainer-approved (decision 3): canonical NIST citation format is `Rev. N` (with period, publisher convention). Corpus-wide sweep converted `Rev N` → `Rev. N` across 50 files (excluded: CHANGELOG historical entries and `.working/` archives). All 50 files received per-doc Version+Date patch bumps in the same commit. Template's "Rev. 4 → Rev. 5" example reworded to generic framing to avoid standards-currency gate false-positive on the illustrative-of-drift use case.

### PR #206 — FR-87 + FR-88 (medium): SSRF range list + cipher suite enumeration (2026-06-22)

Maintainer-approved (decision 2). Pack core/owasp.md SSRF guidance updated with canonical IPv4 + IPv6 ranges + RFC citations (previously missed IPv6 entirely and used non-CIDR notation). Dev-security standard-api-security.md cipher row enumerated TLS 1.3 AEAD suites per NIST SP 800-52 Rev. 2 §3.3.1.

### PR #205 — FR-81 fully closed (medium) + PR #204 /validate-pr fixes (2026-06-22)

Maintainer-approved: pack `dev-security/claude-rules/CLAUDE.md` TLS row aligned to canonical encryption-policy mandate (TLS 1.3+ with TLS 1.2 in Prohibited). Same shape as PR #193/#201. FR-81 fully closed (all 3 named surfaces). Also bundles 3 /validate-pr fixes from PR #204: stale count, in-flight self-correction prose in CHANGELOG, FR-114 double-counted.

### PR #204 — Pass-1 verification of the 2026-06-22 fitness review (2026-06-22)

First Pass-1 verification in the project. r2 report file gains a new §9 (Pass-1 Verification Results) with verdict tags: 10 ✅ actively verified, 1 ⚠️ (FR-118 broader divergence than original framing), 0 ❌, 0 🤔, 9 ✅ batch-tagged for findings closed in overnight PRs, 3 maintainer-decided. FR-124 severity flagged for escalation Medium → High (12-month risk window). Pass-2 (maintainer-interactive bucket processing) is next.

### PR #203 — FR-133 (FYI): Jurisdiction-index pointer prominence (2026-06-22)

Closes FR-133 by restructuring `docs/decision-tree.md` §4.1: the jurisdiction-index pointer is now a stand-alone lead paragraph noting the full 25-jurisdiction coverage; common Anglosphere selections are framed as "representative, not exhaustive"; a closing sentence names example non-Anglosphere annexes (Australia, Singapore, India, Brazil, Japan, South Korea, China) with redirect to the jurisdiction index. Also bundles PR #202's out-of-window TODO drift cleanup (C1/C2/C3 next-up narrative rotated to reflect overnight closures).

### PR #202 — Overnight session wrap-up (2026-06-22)

Final overnight-batch PR. Updates `.working/overnight-pr.md` with the 9-PR build-progress list (PRs #193-#201, closing FR-127/128/129/113/115/116/117/132 fully + FR-81 partial), the files-modified inventory, the files-NOT-touched inventory, and the 9-item open-ambiguities list for maintainer morning review. Status remains `in-flight`; the morning-processing PR will transition to `stub` after routing content.

### PR #201 — FR-81 partial (medium): TLS 1.3+ alignment in dev-security standards (2026-06-22)

Two of three FR-81 surfaces aligned to the canonical encryption policy's TLS 1.3+ mandate: `dev-security/standard-developer-security-requirements.md`:151 and `dev-security/standard-api-security.md`:109. Pack `dev-security/claude-rules/CLAUDE.md` surface deferred (pack-rule edit; approval-needed). Same canonical-source pattern as PR #193's FR-127 ZTA framework alignment.

### PR #200 — FR-132 (low): Decision-tree glossary-order annotation (2026-06-22)

Closes FR-132 by annotating `docs/decision-tree.md` §2.1 Orientation list: items 1-2 (README, adopter-guide) get inline notes that acronyms are expanded at first occurrence per FR-4 / FR-106 / FR-113 polish; item 3 (glossary) gets a note about its scope (reserved for deeper-domain docs). Adopts the recommendation's option (b) "note recent improvements" rather than option (a) "move glossary to item 1" (the existing entry-point pattern is preserved).

### PR #199 — FR-117 (medium): Risk Owner evidence by accountability action (2026-06-22)

Closes FR-117 by adding a new §9.2 to the ERM standard mapping each of the five Risk Owner accountability actions (per §3) to the evidence type from §9.1 that proves execution. Mechanical mapping using existing canonical sources; no new policy. C1 Convergent Finding 3 of 4 closed (FR-115/116/117); FR-119 deferred (needs decision).

### PR #198 — FR-116 (medium): Risk Owner monitoring cadence by score band (2026-06-22)

Closes FR-116 by extending ERM standard §8.1 with explicit Risk Owner review cadences per score band (Low/annual, Moderate/quarterly, High/monthly, Critical/monthly), aligning to the §5.2 scoring-threshold table's review-interval column. Mechanical alignment, no new policy. Partial C1 close (after PR #197's FR-115).

### PR #197 — FR-115 (high): Risk Owner row in Role Authority Register (2026-06-22)

Closes FR-115 by adding the Risk Owner row to the canonical Role Authority Register, mirroring the verbatim Primary Accountability text from the ERM standard §3 (added in PR #178) and adding a reciprocal cross-reference. Partial close of Convergent Finding C1; FR-116/FR-117 still doable, FR-119 deferred (needs decision).

### PR #196 — FR-113 (medium): CAPA + SIEM acronym expansion in README (2026-06-22)

Closes FR-113 by expanding `CAPA` and `SIEM` acronyms at first occurrence in `README.md`'s Repository Structure block, restoring the acronym-expansion pattern established in PRs #172 and #179. Also bundles the mechanical cleanup of fitness-reviews backlog-table rotation for FR-127/128/129 (pre-existing discipline gap surfaced by PR #195's /validate-pr).

### PR #195 — FR-129 (H[critical]): Internal audit reports retention 5y → 7y (2026-06-22)

Closes FR-129 by raising internal audit reports retention in `governance/register-data-retention-schedule.md` from 5y to 7y, aligning with the internal-audit standard §8.3 canonical 7-year mandate. With PR #194's FR-128 closure, the C3 Convergent Finding (audit-evidence chain breaks) is fully resolved.

### PR #194 — FR-128 (H[critical]): CAPA retention 5y → 7y (2026-06-22)

Closes FR-128 by raising CAPA records retention in `governance/register-data-retention-schedule.md` from 5y to 7y, aligning with the CAPA procedure's §12 canonical 7-year mandate and closing the audit-evidence chain break with control-testing-evidence retention. Also fixes PR #193's /validate-pr finding (stale FR-127 entry in TODO's "Next-up recommendations" section) per the batching rule.

### PR #193 — FR-127 (H[critical]): TLS 1.2 → TLS 1.3 in ZTA framework (2026-06-22)

Closes FR-127 by aligning the ZTA framework's Pillar 3 transport-encryption maturity row with the canonical encryption policy's TLS 1.3+ mandate. First overnight-batch PR; carries PR #192's /validate-pr history row.

### PR #192 — Codify batching-into-next-PR rule for /validate-pr and /validate (2026-06-22)

New "Batching into the next PR (recursion-avoidance)" sub-section in both /validate and /validate-pr SKILL.md surfaces + slash commands: /validate-pr outputs (zero-finding history rows AND findings-producing fixes) bundle into the next PR whatever its purpose, eliminating dedicated hot-fix and housekeeping PRs. /validate retains an optional dedicated close-out PR for numerous or coherent corpus-wide findings. Carries PR #191's deferred /validate-pr history row as the rule's first application. Closes the day's cascade loop.

### PR #191 — Record /validate-pr for PR #190 (0 findings; cascade terminated) (2026-06-22)

`.working/` changes for local project: appended the history row recording the zero-finding /validate-pr run against PR #190. Four-PR cascade (#187 → #188 → #189 → #190 = 2+2+2+0 findings) terminated by PR #190's structural fix (full-date Originating run column + UTC convention + chat-surfacing discipline).

### PR #190 — Hot-fix /validate-pr findings on PR #189 + UTC convention + chat-surfacing discipline (2026-06-22)

Three bundled threads: hot-fix the two multi-surface incompleteness findings from /validate-pr on PR #189 (the r2→r1 relabel missed `.working/fitness-reviews/history.md` line 22 narrative + the H[critical] backlog table's "Originating run" column; resolved structurally by switching cross-date column to full dates); codified the UTC convention in CLAUDE.md (assistant works in UTC for all date-bearing fields); codified the chat-surfacing discipline in /validate and /validate-pr SKILL.md + slash commands (findings surface in chat with per-finding shape, not buried in .working/ files). Third consecutive findings-producing /validate-pr.

### PR #189 — Hot-fix /validate-pr findings on PR #188 (2026-06-22)

Two in-window findings from /validate-pr on PR #188 fixed: the fitness-review file's internal "r2" labels and history.md row corrected to "r1" per the per-date `rN` convention (8 internal references plus the history row); pack README's 1.40.1 row catch-attribution reworded from "gate 31 caught it" to credit /validate-pr deep-read (gate 31 didn't actually fire due to a timezone-boundary edge case). Recorded /validate-pr on PR #188 history row plus per-PR detail file. Second consecutive findings-producing /validate-pr (the discipline is converging).

### PR #188 — Close-out: /validate-pr fixes on #187 + record /fitness r2 (2026-06-22)

End-of-evening close-out bundling three independent threads: two hot-fixes for PR #187's `/validate-pr` findings (slash-command "no skip" wording harmonized to match SKILL.md verbatim; pack README Date bumped 2026-06-21→2026-06-22 with Version 1.40.0→1.40.1 patch); committing the /fitness r2 report (27 findings across 10 personas; 22 new FR IDs FR-112 through FR-133; three Convergent Findings dominate; zero regressions from the day's PRs); and the /validate-pr history record for PR #187 itself.

### PR #187 — Codify no-orchestrator-skip-discretion discipline + fix paired-skill docstring (2026-06-22)

Hot-fix after maintainer flagged that the orchestrator skipping /validate-pr on PRs #185/#186 was a real policy deviation. Three surfaces gain explicit "no skip" language (SKILL, slash command, pack-rule anti-patterns); paired-skill linter docstring updated; new failure-mode class C-9 captured in hallucination-metrics with a future-gate candidate for mechanical enforcement.

### PR #186 — Sweep 17 iter 1 close-out: SKILL forward-reference + gate 44 PAIRS registry (2026-06-21)

Sweep 17 (second full sweep of the day). Two in-window findings closed: validation-sweep-pr-scoped SKILL.md:151 stale "/retro queued for PR #185" → "PR #186"; gate 44 PAIRS registry extended with the new validation-sweep-pr-scoped + /validate-pr pair (was a real defect — gate not validating new skill).

### PR #185 — Record first /validate-pr invocation (PR #184, 0 findings) (2026-06-21)

`.working/` changes for local project: appended the history row recording the first real `/validate-pr` invocation (run post-merge on PR #184; 0 findings; full Subagent A coverage). Housekeeping PR; no corpus content changes. Re-numbers tomorrow's planned PRs: /retro becomes #186, FR-33 becomes #187.

### PR #184 — Worker-brief template + hallucination-assessment update protocol (2026-06-21)

New project-local worker-brief template at `.working/worker-brief-template.md` plus pack-rule update codifying the self-improving loop: when an apply-time catch occurs, log it, classify the fix, update the template inline. Initial template ships with four guard rails from the four known apply-time-catch classes.

### PR #183 — Add /validate-pr skill + slash command for post-merge per-PR validation (2026-06-21)

New pack skill and slash command for PR-scoped post-merge validation; runs after every merge to catch per-PR drift before it compounds. Complements the existing corpus-wide /validate sweep (every 10 merges).

### PR #182 — Corpus-wide count-genericization sweep (2026-06-21)

Applied PR #181's count-genericization principle corpus-wide. Found one additional candidate (`specification-audit-programme.md:64` "seven functional categories" → generic); negative findings (ten persona reviewers, five disciplines, external CCM/FedRAMP counts) documented per assessment criterion.

### PR #181 — Sweep 16 iter 1 close-out: TODO narrative refresh + skill-authoring genericization (2026-06-21)

Sweep 16 close-out (first full sweep since Sweep 15 at PR #167; 13-PR window). Two in-window findings closed: TODO.md:22 PR-range narrative refreshed to current state; skill-authoring-discipline SKILL.md:26 "seven governance rules" rewritten as generic phrasing per maintainer's count-genericization direction.

### PR #180 — Extend version-bump discipline to four surfaces (add per-document Date) (2026-06-21)

Closed the discipline gap surfaced by PR #179's gate-31 catch: the apply-time checklist now pairs Version-bump with Date-bump on every body-changing commit. Pack rule and project CLAUDE.md updated; pack version 1.36.0 → 1.37.0.

### PR #179 — FR-18 + FR-25 + FR-79 + FR-105 + FR-106 + FR-110 (all medium): P1.4a small singletons bundle (2026-06-21)

Six medium-tier singleton findings closed in one PR: exception 180-day baseline anchored to a library convention, control-testing evidence retention raised 5y→7y, tabletop template Slack→generic, ISMS NIST CSF name normalised, README trade-programme acronyms expanded, decision-tree document-index reframed. FR-33 (high[critical]) split out to P1.4b per "always split when in doubt".

### PR #178 — FR-11 (medium) + FR-12 (medium): ERM standard Risk Owner role definition + within-document treatment vocabulary harmonisation (2026-06-21)

§3 governance table gains a Risk Owner role definition; treatment vocabulary harmonised within the ERM standard (Treat→Mitigate, Exploit/Enhance row-split, Treatment Option enum extension). Cross-document harmonisation against procedure-risk-register deferred.

### PR #177 — Rotate Phase 1 / Phase 2 execution plan into TODO (2026-06-21)

Moved the multi-PR Phase 1 + Phase 2 execution plan out of session memory into TODO's Queued-sequence section so it survives session-end; identifies the `/fitness` pause point at end of Phase 2.

### PR #176 — Document five memory-only AI-assistant workflow disciplines as a new pack rule + hallucination-metrics tracking file (2026-06-21)

New pack rule `ai-assistant-workflow-disciplines.md` covers research-assistant discipline, pipeline PR construction, apply-time worker correction, "always split when in doubt", and background work during CI waits; `.working/hallucination-metrics.md` ships as the project's tracking artefact for the catch / escape ratio.

### PR #175 — Shorten historical DONE entries to scrolling-battle-text convention (2026-06-21)

Retroactively shortened every existing DONE entry to the 1-2-sentence, no-links, no-version-bumps shape adopted in PR #174.

### PR #174 — Retire CHANGELOG skip trailer; adopt terse-entry convention; reshape DONE as scrolling battle-text (2026-06-21)

Replaced the `Changelog: skip` opt-out in the change-tracking pack rule with a terse-entry convention (every PR carries an entry, even if a one-liner); reshaped the DONE-ledger guidance to 1-2 sentences, no links, at-a-glance index rather than CHANGELOG duplicate.

### PR #173 — CHANGELOG backfill for PRs #170 and #171 (2026-06-21)

Backfilled the missing CHANGELOG entries for the two `.claude/`-only PRs that shipped under the (then-active) skip-trailer exemption, repairing the visible #169 → #172 jump in the audit trail.

### PR #172 — FR-4 (medium) + FR-5 (medium) + FR-6 (medium) + FR-7 (medium) + FR-8 (medium, ⚠️): README polish bundle (2026-06-21)

Five medium README polish findings closed in one PR: acronym expansion, doc count pointer, CalVer placement, audience-signal panel, version-line demote.

### PR #171 — CLAUDE.md PR-activity-subscription + 60s-timer discipline (2026-06-21)

Added the discipline that every `mcp__github__subscribe_pr_activity` call arms a paired 60-second fallback timer, since subscriptions reliably deliver failure events but not all success transitions.

### PR #170 — CLAUDE.md three-surface version-bump discipline (2026-06-21)

Codified the three-sentence version-bump rule (per-doc per body-change commit; library CalVer once per PR in the last commit; README Version paired with CalVer) after PR #169's gate 40 catch.

### PR #169 — FR-26 (medium) + FR-27 (medium) + FR-28 (medium): access-control procedure decision-path gaps (2026-06-21)

Three medium-tier access-control polish findings closed: escalation ladder added to the 3-day approval SLA, vague "appropriate" replaced with four bounded review criteria, and emergency verbal approval gained trigger conditions plus a revocation consequence.

### PR #168 — Sweep 15 follow-up: BASC information security 5-level classification expansion (2026-06-21)

Expanded the BASC logistics policy from 3 classification levels to the canonical 5 (Public, Controlled, Internal, Confidential, Restricted) to align with the rest of the corpus.

### PR #167 — Sweep 15 iter 1 close-out: roadmap metadata + DPIA ISO/IEC citation + TODO narrative refresh (2026-06-21)

Three in-window fixes: roadmap Review Frequency metadata stale after FR-57 rename; DPIA template's ISO/IEC 29134:2023 citation corrected to 2017; TODO narrative refresh.

### PR #166 — FR-57 (high): rename long quickstart to startup-roadmap; ship new 10-minute quickstart (2026-06-21)

Renamed the 319-line composition workbook to `template-startup-roadmap.md` and shipped a true 10-minute quickstart as the new `template-quickstart.md`; portal updated to surface both with distinct questions.

### PR #165 — FR-56 (high): adopter entry-point reconciliation — portal declared canonical front door (2026-06-21)

Declared `docs/portal.md` the canonical adopter entry point; four other adopter-facing documents gained a "Where this fits among the adopter entry points" preface naming the portal as canonical.

### PR #164 — FR-43 (high[critical]): data-classification 5-level scheme propagated library-wide (2026-06-21)

Propagated the canonical 5-level classification scheme (Public / Controlled / Internal / Confidential / Restricted) into six subordinate documents that previously enumerated only four levels.

### PR #163 — DONE format harmonisation with TODO: surface FR-N and severity at heading level (2026-06-21)

Retrofitted 22 DONE H3 headings to surface `FR-N (severity)` at the heading level, matching TODO's tier-grouped bullet format for at-a-glance symmetry.

### PR #162 — FR-29 (high[critical]): Data Protection Impact Assessment template with Article 35 trigger / EDPB WP248 / Article 35(7) content checklists (2026-06-21)

Shipped a new DPIA template covering GDPR Article 35's three limbs (trigger checklist, EDPB WP248 nine-criteria framework, Article 35(7) content checklist).

### PR #161 — FR-17 (high): reconcile exception-approval authority between policy and Role Authority Register (2026-06-21)

Reconciled the exception policy's §2.2 approval pathway with the Role Authority Register's "Approve exception" RACI row, replacing a stub placeholder with the tiered pathway and adding a reciprocal cross-reference.

### PR #160 — Sweep 14 iter 1 close-out: FR-44-self-violations + TODO queued-sequence refresh (2026-06-21)

Sweep 14 close-out: fixed three FR-44 self-violations in the master spec and exception policy (legacy "shall" / "may not" → "must" / "must not"), plus a stale TODO queued-sequence narrative.

### PR #159 — FR-44 (high): requirement-language convention documented in master spec (2026-06-21)

Documented the library's requirement-language convention in the master spec: "must" / "must not" canonical; "should" / "should not" for recommendations; "may" for permission; "shall" reserved for external-standard quotation.

### PR #158 — FR-80 (high[critical]): SIEM / cloud-activity-log retention reconciliation (2026-06-21)

Reconciled the apparent contradiction between the 3-year SIEM-events retention and the 90-day cloud-activity-log retention by reframing the 90-day figure as the platform-side forwarding floor; the SIEM remains the authoritative retention authority.

### PR #157 — FR-16 (high[critical]): exception register hard caps + renewal-ceiling escalation pathway (2026-06-21)

Strengthened the exception policy with two new required schema fields (`max_duration` 540 days default, `renewal_count_limit` 3 default), a hard 180-day initial cap, and a 1-2-3 renewal-ceiling escalation (ERC at 2nd, Board at 3rd, prohibition at 4th).

### PR #156 — FR-2 (high): README "How to use" step 1 leads with the audience-keyed portal (2026-06-21)

Reordered the README's "How to use" step 1 so the audience-keyed portal is the primary pointer; the 300-row document index becomes the secondary pointer for readers who already know what they want.

### PR #155 — FR-1 (high): README reframing (corpus is the headline, AI-maintenance is the methodology) (2026-06-21)

Reframed the README so the GRC documentation corpus is the unambiguous headline product; the audit toolchain and the dev-security pack are positioned as the operational layer used to maintain corpus consistency.

### PR #154 — Sweep 13 iter 1 close-out: FR-45 + FR-92 generalisations (2026-06-21)

Sweep 13 close-out: three FR-45-class "may not" → "must not" fixes in AI standards; one FR-92-class addition of Escalation Owner + Remediation Sign-off columns to the BASC IT KPIs table; one metadata document-history backfill.

### PR #153 — FR-92 (high): KPI Escalation Owner + Remediation Sign-off columns (2026-06-21)

Added Escalation Owner + Remediation Sign-off columns to every KPI table in the IT operations register; roles drawn from the Role Authority Register, with ERC as the escalation target when the KPI's Owner is already CIO or CISO.

### PR #152 — FR-19 (high[critical]) + FR-20 (high): CAPA governance ceiling + root-cause quality checklist (2026-06-21)

CAPA procedure gains a 1-2-3 extension-ceiling (ERC at 2nd, Board Risk Committee at 3rd, prohibition at 4th) and a five-criterion root-cause quality checklist (Specific / Causal / Actionable / Bounded / Evidence-anchored).

### PR #151 — FR-35 (high): explicit GDPR Article 33(2) processor-awareness clock (2026-06-21)

Made the GDPR Article 33(2) two-clock asymmetry explicit in the privacy breach-response procedure: the 24-hour processor-to-controller window starts at processor awareness; the 72-hour Article 33(1) controller clock runs from controller awareness.

### PR #150 — FR-45 (high): RFC 2119 "may not" → "must not be" in two security standards (2026-06-21)

Replaced "may not" with "must not be" in two security standards where the intent was a prohibition rather than a permissible-negative-possibility per strict RFC 2119 reading.

### PR #149 — FR-21 (high[critical]): Compliance-obligations Source Reference granularity (2026-06-21)

Tightened the compliance-obligations Source Reference field so register citations resolve to a single unambiguous source location, with minimum-precision patterns per source type (NIST, ISO, statutes, COBIT, PCI DSS, CSA CCM, contracts, voluntary commitments).

### FR-21 (high[critical]) — Compliance-obligations Source Reference granularity (closed by PR #149, 2026-06-21)

Template previously accepted low-precision citations like "NIST 800-53" without revision or control number; closure tightened the field to require resolvable source locations.

### PR #148 — Sweep 12 iter 1 close-out (2026-06-21)

Sweep 12 close-out: three in-window findings fixed (cross-doc stale CIO-as-ERM-accountable, missing sampling-justification cross-reference, missing reciprocal risk-acceptance link).

### PR #147 — FR-3 (high): README "New to GRC?" introductory block (2026-06-21)

Added a "New to GRC? Start here" §2 to the README expanding the acronym, defining Governance / Risk / Compliance in plain language, and signposting five role/intent-keyed next steps.

### PR #146 — FR-96 (high): Risk-acceptance procedure cross-reference to exception register (2026-06-21)

Added a `Related exception register entry` field to the risk-acceptance procedure's required record fields so the exception and risk-acceptance registers are cross-traversable for auditors.

### PR #145 — FR-95 (high): Risk register compensating-controls field (2026-06-21)

Added a `Compensating Controls` field to the risk register Acceptance section so the acceptance record is self-contained and auditable.

### PR #144 — FR-22 (high): Audit-evidence sampling-justification field (2026-06-21)

Added a mandatory `Sampling justification` field to the audit-evidence template's per-control operating-evidence section, capturing population, sample size, selection method, and confidence-level assumption.

### PR #143 — FR-9 (high[critical]) + FR-10 (high): Chief Risk Officer in enterprise risk management standard (2026-06-21)

Changed the ERM standard's Owner from CIO to CRO and added a CRO row to §3 Governance scoped to risk strategy, risk appetite stewardship, and ERM-programme outcomes reporting.

### FR-10 (high) — Chief Risk Officer in ERM §3 governance table (closed by PR #143, 2026-06-21)

ERM §3 governance table omitted CRO despite CRO being a defined role; closed alongside FR-9.

### FR-9 (high[critical]) — Enterprise risk management Owner: CIO → CRO (closed by PR #143, 2026-06-21)

ERM-standard Owner field changed from "Chief Information Officer" to "Chief Risk Officer"; enterprise risk is a CRO accountability in most operating models.

### PR #142 — Fitness quick wins: FR-13 (medium) + FR-54 (low) + FR-55 (low) + FR-103 (low) (2026-06-21)

First fitness-remediation PR. Four single-file unambiguous findings closed at maintainer direction as quick wins while the rest of the backlog was under review.

### FR-103 (low) — Add Chief Compliance Officer row to framework-continuous-assurance governance table (closed by PR #142, 2026-06-21)

Continuous Assurance framework's governance table omitted CCO despite CCO being relevant to compliance-domain assurance closure; CCO row added.

### FR-55 (low) — Document `roadmap-` doctype prefix (closed by PR #142, 2026-06-21)

Closed alongside FR-54 by adding an explicit prefix-to-doctype mapping table to the master spec listing all 17 doctypes and their canonical filename prefixes.

### FR-54 (low) — Document `sop-` doctype prefix (closed by PR #142, 2026-06-21)

Same prefix-mapping table as FR-55, also covering `sop-`.

### FR-13 (medium) — Disambiguate `CPPA` in enterprise risk management standard (closed by PR #142, 2026-06-21)

`CPPA` in the framework alignment table expanded to "Canadian Consumer Privacy Protection Act, Bill C-27" to disambiguate from the California Privacy Protection Agency.

### PR #141 — Fitness backlog Pass-2: maintainer-interactive triage; structured TODO backlog (2026-06-21)

Pass-2 triage of the 111 fitness findings: ✅ batch accepted (Low deferred to later cleanup); ⚠️ batch accepted with modifications; FR-14 + FR-110 resolved to ✅; FR-43 + FR-53 reshaped. Structured backlog added to TODO.

### PR #140 — Fitness backlog Pass-1: orchestrator verification of all 111 FR-N findings (2026-06-21)

Pass-1 verification of the 111 FR-N findings via five parallel subagents: 93 ✅ confirmed-as-stated, 14 ⚠️ confirmed-with-modification, 2 🤔 ambiguous, 2 ❌ rejected.

### PR #139 — Fitness skill amendment: unverified→confirmed labelling discipline (2026-06-21)

Amended the library-fitness-review skill to introduce per-finding Pass-1 (orchestrator verification) and Pass-2 (maintainer-interactive triage) before any finding lands in the remediation backlog.

### PR #138 — Shipped Priority 4 items rotation (2026-06-21)

Rotated five completed Priority-4 TODO items (P4.1-P4.5) into DONE as their own cross-reference entries; P4.6 remains forward-looking.

### TODO P4.1 — Quickstart templates per adopter profile (shipped 2026-06-20)

Shipped as `docs/template-quickstart.md` v2.0.0: core baseline plus five stacking dimensions with about twenty modules and three worked examples (the v1.0.0 fixed-profile shape was rejected as too rigid).

### TODO P4.2 — Maturity assessment interactive template (shipped 2026-06-20)

Shipped as `docs/template-maturity-self-assessment.md`: guided checklist across 11 library domains on a 5-tier maturity ladder with per-tier next-step guidance.

### TODO P4.3 — Implementation roadmap templates (shipped 2026-06-20)

Shipped as `docs/template-implementation-roadmap.md`: three-phase (Floor / Operational / Year-1 close) sequence at 90 / 180 / 365 days, with pace adjustments for E1/E3/E4 capacity tiers.

### TODO P4.4 — Regulator interaction templates (shipped 2026-06-20)

Shipped as `compliance/template-regulator-interaction.md`: five sub-templates (breach notification, attestation submission, examination support, periodic report, regulatory inquiry response) in one consolidated document.

### TODO P4.5 — Audit evidence package templates (shipped 2026-06-20)

Shipped as `compliance/template-audit-evidence-package.md`: cover page, control inventory, per-control sections with framework references and evidence, per-domain summaries, package-level sign-off.

### PR #137 — Overnight-work protocol: stub format for `overnight-pr.md` + audit gate 46 + pack rule amendment (2026-06-21)

Implemented the overnight-work protocol: stub-form `overnight-pr.md` with three-state `Status` field, new audit gate 46 that fails on `Status: done`, and a pack-rule subsection documenting the lifecycle.

### PR #135 — Restructure design-decisions into its own file; clean up `overnight-pr.md` (2026-06-21)

Created `design-decisions.md` as the new home for design-decision content; rotated misplaced sections out of DONE and TODO; deleted the procedural-detail `overnight-pr.md` content from the prior session.

### PR #134 — Gate 45 false-positive fix: tighten queued-PR regex (2026-06-21)

Tightened gate 45's regex so the queued-PR marker must be the immediately-following PR reference, not any PR reference within 80 characters; fix for a false positive on `main` post-PR-#133 merge.

### PR #133 — Document the project's Canadian-first language convention (2026-06-21)

Documented the project's language convention as "Canadian English first, Commonwealth second, other dialects last"; Canadian-shared-with-Oxford `-ize` orthography is the linter behaviour, not an American mandate.

### PR #132 — Add Ryk Edelstein to `AUTHORS.md` (2026-06-21)

Single-line addition to AUTHORS.md's Acknowledged contributors list; first PR using the post-PR-#131 steady-state of TODO/DONE rotation in the same PR.

### PR #131 — DONE.md infrastructure + TODO refactored to forward-looking only (2026-06-21)

Bootstrap PR for this file: introduced `.working/DONE.md` as the closed-TODO ledger; rotated "PRs completed this session" and "design decisions made this session" content out of TODO; added the PR finalization protocol section to the change-tracking pack rule.

### PR #130 — Remove decorative gate-count narrations (2026-06-21)

Replaced 11 `"the N-gate audit programme"` prose references across 7 files with `"the audit programme"`; the spec §6 inventory remains the canonical source for the gate list and current count.

### PR #129 — PR #128 catch-up: TODO drift caught by gate 45 on post-merge `main` (2026-06-21)

Gate 45's first production catch: post-merge `push`-event CI on `main` flagged TODO still framing PR #128 as "Next" after its merge; TODO rotated and the gate validated as the intended drift-detection mechanism.

### PR #128 — Gate 45 (TODO staleness audit) + PR-time-checks wrapper (2026-06-21)

New gate 45 catches the two TODO drift shapes (queued PR already merged; sweep cursor behind history); bundled with `run-pr-time-checks.sh` so every gate the CI workflow runs has a local invocation path before push.

### PR #127 — Sweep 11 iter 1 close-out (2026-06-21)

Sweep 11 close-out: eight in-window findings including a corpus-wide count-mismatch correction (111/17/20/57/17 across six surfaces); reframed TODO's session-pause snapshot as "as-of-last-refresh".

### PR #126 — `.working/README.md` Activities table row for `changelog-details/` (2026-06-21)

Single-row addition to `.working/README.md`'s Activities table for the `changelog-details/` activity that was introduced in PR #125 but missed in that PR's README update.

### PR #125 — CHANGELOG two-file split: root keeps lead paragraphs, detailed mirror keeps full structured entries (2026-06-21)

Split CHANGELOG into a two-file convention: root carries lead-paragraph summaries (adopter-facing), detailed mirror at `.working/changelog-details/CHANGELOG-detailed.md` carries full structured-section entries (maintainer-grade). 2926 → 675 lines in root.

### PR #124 — First-ever fitness review (run r1, ten persona subagents) (2026-06-21)

First invocation of the library-fitness-review skill: ten persona subagents dispatched in parallel, producing 111 unique findings (FR-1 through FR-111) that became the fitness-remediation backlog.

### PR #123 — Sweep 10 iter 3 close-out (2026-06-21)

Sweep 10 iter 3 close-out: one in-window Medium finding actioned (TODO version-snapshot drift); convergence narrowing from iter 2's 7 findings to 1.

### PR #122 — TODO cleanup: removed completed Steps A/C/D/E from queued sequence (2026-06-21)

Pure TODO maintenance: removed completed steps from the queued sequence section and renumbered the next step; no library content change.

### PR #121 — Sweep 10 iter 2 close-out: post-overnight-sequence cleanup (2026-06-21)

Sweep 10 iter 2 close-out: seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120), including preflight exemption refresh, TODO snapshot refresh, and CHANGELOG narration correction.

### PR #120 — `/fitness` skill (`library-fitness-review`) (2026-06-21)

Added the `/fitness` slash command and the library-fitness-review skill: whole-corpus library-quality review dispatching ten persona reviewers in parallel; authored end-to-end during an overnight session under explicit maintainer authorisation.

### PR #119 — TODO update only (session-resume context capture) (2026-06-21)

Session-resume context capture in TODO; no library content change.

### PR #118 — Restructure `.working/<activity>/` to canonical layout (2026-06-21)

Restructured `.working/validate-sweeps/` to the canonical `<activity>/{README, history, detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory.

### PR #117 — Sweep 10 iter 1 close-out: six prose-drift findings post-PRs-#114-#116 (2026-06-21)

Sweep 10 iter 1 close-out: six prose-drift findings from the three-PR `.working/` sequence (stale step counts, stale subdir inventory, section-header drift, "Four rules" → "Six rules" updates).

### PR #116 — Move validation-sweep history file from `governance/` to `.working/` (2026-06-21)

Moved the validation-sweep history file from `governance/` to `.working/` since validation-sweep history is project-specific application of the discipline, not template content for adopters.

### PR #115 — `/validate` slash command rename + per-iteration record convention (2026-06-21)

Renamed the `/validation-sweep` slash command to `/validate` for short ergonomic verbs; added the per-iteration record convention (detail files only when findings exist; history-table row for every iteration).

### PR #114 — `.working/` top-level convention infrastructure (2026-06-21)

Established the `.working/` top-level convention for maintainer working state; created `.working/README.md` and added `.working/` to the linters' default exempt directories.

### PR #113 — Sweep 9 iter 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 (2026-06-21)

Sweep 9 iter 3 close-out: three documentation findings from Subagent A's deep review of PR #112; convergence narrowing from iter 2.

### PR #112 — 7th governance rule (`validate-inference-before-action.md`) + gate 39 pattern P7 (2026-06-21)

Added the seventh pack rule, `validate-inference-before-action.md`: when the next action depends on an inferred premise, validate the premise via tool call before acting. Action-side counterpart of the evidence-grounded-completion rule.

### PR #111 — Sweep 9 closure: Subagent C findings + Rule 5.6 (subagent-dispatch declaration discipline) (2026-06-21)

Sweep 9 closure: actioned Subagent C findings; added Rule 5.6 to the validation-sweep skill requiring every iteration to declare which subagents were dispatched in the history register's `Subagents` column.

### PR #110 — Corpus stale gate-count fixes + gate 39 pattern P6 (2026-06-21)

Corpus-wide stale gate-count reference fixes (the cascade-class issue PR #130 later addressed at the source by removing decorative gate-count narrations); gate 39 pattern P6 added.
