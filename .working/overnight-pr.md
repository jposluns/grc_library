# Overnight PR

**Status:** in-flight

Overnight session in flight, authorized by the maintainer 2026-06-23. The assistant
is working autonomously through the Priority 1 / Priority 2 backlog (then P3, then P4
as time allows) while the maintainer is asleep. This file is the durable handoff if
the session is reclaimed mid-run; it is updated as PRs land.

## Authorization scope

- **Granted**: "Get through as many P1 and P2 items as possible; if time remains,
  proceed to P3 then P4." Merge authority: **green CI = merge** (self-merge of own
  green PRs, the standing PR-workflow safe set, extended to this unattended run).
- **Hard quality rule**: any finding from `/validate-pr` or the per-batch `/validate`
  **must be fixed immediately, before the next planned PR** (not deferred/batched).
- **Per-PR discipline (no abbreviation)**: each PR runs post-commit `run_all_audits.sh`
  (46 gates) + pre-push `run-pr-time-checks.sh`, CI-green before merge, then a full
  `/validate-pr` + `/retro`. `/validate` (corpus-wide) at each batch seam.
- **Decision discipline**: every formal decision was either resolved with the maintainer
  before sleep (below) or, if it surfaces unanticipated mid-run, **skipped to morning**.
- **Governing principle**: Quality > Speed > Cost; project integrity absolute.

## Design decisions made (resolved with maintainer before sleep, 2026-06-23)

1. **New-document criticals FR-30/31/32/34/71/72**: author all six unattended, each its
   own PR, mirroring an existing same-type doc and anchored to its named external standard.
2. **FR-70 crypto-asset/blockchain domain (XL)**: defer to a dedicated session.
3. **Cross-document value conflicts**: resolve **stricter-is-safer + evidence** (matches
   the locked-criticals pattern), documenting each choice; skip any pick with no evidence
   or stricter basis to morning.
4. **FR-143 supplier escalation chain** (was circular DPO→CISO→DPO): **DPO → CISO → CRO**.
5. **FR-140 adopter starter-set**: **strict nesting; quickstart-6 is the canonical floor**
   (Tier-1 15 ⊇ the 6 incl. IAM + acceptable-use; 23 ⊇ 15; ~37 ⊇ 23; reconcile the 6th-artefact naming).
6. **FR-73 AI ethics**: introduce a **standing independent AI Ethics Panel** (subcommittee
   operationally independent of the AIGC risk/compliance function, documented challenge + dissent-escalation).
7. **FR-144 breach individual-notification clock**: add an internal floor "without undue
   delay, and in any event within 72 hours of the high-risk determination" (stricter rule; no separate decision).
8. **FR-58 inheritance vocabulary**: skipped to morning (taxonomy-design task needing discussion).

## Plan of record (PR sequence)

- **PR 1** — run initiation (this file → in-flight; design-decisions; carried #258 bookkeeping).
- **Batch A (locked H[critical])** — PR 2 FR-134, PR 3 FR-135, PR 4 FR-136, PR 5 FR-137, PR 6 FR-138, PR 7 FR-139 → /validate.
- **Batch B1** — PR 8 FR-141, PR 9 FR-161/162/163, PR 10 FR-146, PR 11 FR-153, PR 12 FR-144 → /validate.
- **Batch B2 (value-conflicts)** — PR 13 FR-149, PR 14 FR-151, PR 15 FR-147, PR 16 FR-150, PR 17 FR-148, PR 18 FR-152 → /validate.
- **Batch C (authorial-resolved)** — PR 19 FR-143, PR 20 FR-140, PR 21 FR-73 → /validate.
- **Batch D (new privacy docs)** — PR 22 FR-30, PR 23 FR-31, PR 24 FR-32, PR 25 FR-34 → /validate.
- **Batch E (new procedures)** — PR 26 FR-71, PR 27 FR-72 → /validate.
- **Batch F+ (P2 bulk)** — relocations ×3, then Phase-2 clusters in ≤8-PR batches (/validate each); then P3, then P4 as time allows.

## Files NOT touched (out of scope this run)

- FR-58 (inheritance vocabulary), FR-70 (crypto-asset domain), FR-48 (H2 numbering rename — already deferred).
- Any item surfacing an unanticipated formal decision (parked to morning).

## Build progress (updated as PRs merge)

- PR 1 (run initiation): in progress.

## Open ambiguities surfaced mid-run (for morning)

- **(from PR #259 /validate-pr, low)** Pre-existing en-dashes (`P1–P4`) in older CHANGELOG entries (CHANGELOG.md:41/45/49/57/61). CHANGELOG.md is outside `lint-language.py`'s root-file allowlist (README/NOTICE/specs only), so they pass CI legitimately. Decision: extend the dash gate to CHANGELOG, or keep it deliberately unscoped. Not auto-fixed (out-of-window; rewriting audit-trail prose is scope creep).
- **(from PR #260 / FR-134, medium)** `supply-chain/register-concentration-risk.md:95` uses a "Likelihood (descriptive)" field with the OLD enterprise labels (`Rare, Unlikely, Possible, Likely, Almost Certain`) and a third impact-label variant (`Severe`, vs standard `Catastrophic` / procedure `Critical`). NOT one of FR-134's three named surfaces. Decision needed: harmonize this register's descriptive scale to the canonical Very Low→Very High (+ pick the canonical impact-5 label), or is its qualitative scale intentionally distinct? Skipped to morning (unsanctioned scope expansion otherwise).
- **(from PR #260 / FR-134, low)** Impact-5 label divergence among the three risk-scoring docs: standard `Catastrophic` vs procedure/template `Critical`. Not named in FR-134's decision (which scoped to likelihood + bands) and does not affect the score→rating mapping; left as-is. Morning: decide whether to unify the impact-5 label (note: procedure's `Critical` collides with the top *rating* label `Critical`).
- **(from PR #261 / FR-135, low-medium)** Two pack TLS surfaces deferred (not force-migrated to 1.3): (a) [`dev-security/claude-rules/core/owasp.md`](dev-security/claude-rules/core/owasp.md):42 ("TLS 1.2 minimum on all connections...") and :209 (the ASVS V9 maturity table "TLS 1.2+, cert validation"). owasp.md represents **OWASP ASVS**, which permits TLS 1.2 at baseline; force-migrating would misstate the external standard. Decision: keep ASVS-accurate, or add an org-overlay note that the org requires 1.3 above the ASVS baseline. (b) [`dev-security/claude-rules/languages/go.md`](dev-security/claude-rules/languages/go.md):195 — the example sets `MinVersion: tls.VersionTLS12` with an explicit TLS-1.2 cipher-suite list that Go ignores under TLS 1.3; bumping to 1.3 needs a coherent rewrite (drop/rework the CipherSuites block), not a find-replace.
- **(from PR #261 /validate-pr → handled in PR #262, medium)** Two additional permissive-TLS-1.2 surfaces surfaced by the bare-token search (NOT force-migrated): (a) [`operations/procedure-media-handling-and-transport.md`](operations/procedure-media-handling-and-transport.md):124 — "TLS 1.2 may be used only where a documented technical constraint prevents TLS 1.3, recorded in the exception register, reviewed quarterly" (a *governed* exception, distinct from a flat "1.2 minimum"). Decision: does "TLS 1.3 everywhere" require removing even this exception-register-governed allowance, or is a documented-technical-constraint exception acceptable (it differs from the B2B "no partner exception" case)? (b) [`supply-chain/template-supplier-security-questionnaire.md`](supply-chain/template-supplier-security-questionnaire.md):87 — "Is data encrypted in transit using TLS 1.2 or higher?" (a vendor-facing minimum-bar assessment question, a different surface class). Decision: raise the supplier bar to 1.3, or keep 1.2-or-higher as a third-party minimum? PR #262 forward-corrected #261's over-broad "no org surface permits TLS 1.2" claim; these two surfaces are the deferred migrations.
- **(from PR #262 / FR-136, low)** Optional follow-up: add an explicit "AI-decision / detection logs" row (7 years; ISO/IEC 42001 + EU AI Act Annex IV) to [`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md) so the security-monitoring §298 retention has an authoritative schedule entry rather than an inline standard citation. PR #262 grounded §298 on the ISO 42001 / EU AI Act basis (preserving 7y); the schedule row would make it fully authoritative-and-complete.
- **(from PR #262 /validate-pr, medium)** AI-log-retention inconsistency: [`operations/procedure-security-monitoring-and-alert-management.md`](operations/procedure-security-monitoring-and-alert-management.md):298 sets AI-decision/SIEM logs at **7 years** (ISO 42001 / EU AI Act), but [`ai/checklist-ai-algorithmic-compliance.md`](ai/checklist-ai-algorithmic-compliance.md):99 cites the logging standard for a **"minimum of 12 months"** SIEM AI-log retention. Two different AI-log retention figures (12 months vs 7 years). Out-of-window (pre-existing; not introduced by #262). Decision: reconcile to one canonical AI-log retention value (folds into the AI-decision-log schedule-row item above).
- **(from PR #264 / FR-138, medium — TODO follow-up)** Broader CPPA-as-live sweep deferred. PR #264 scrubbed the three named docs (DSR procedure, breach procedure, privacy policy). The same "CPPA cited as a live basis" pattern remains in other docs not named in the locked decision — most notably [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md):176/:182 (CPPA as a live breach-notification regime, parallel to the breach procedure; NOTE :176's separate invented "72-hour target" was fixed in PR #267 / FR-141, but its "CPPA (Canada)" regime label still needs the CPPA→PIPEDA fix here), the [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) "Frameworks" tags for the three scrubbed docs (now list CPPA, should be PIPEDA), and numerous framework-LIST mentions across matrices, registers, sector annexes, and other privacy templates (`matrix-cross-framework-alignment`, `register-compliance-obligations-template`, the supplier/healthcare/financial-services annexes, `template-privacy-notice`/`template-dsar-workflow`/`register-automated-decision-making` which mark CPPA "(proposed)"). Triage needed: (a) security-incident-response is a live-regime treatment like the breach procedure → scrub to PIPEDA; (b) framework-LIST mentions are softer (regimes considered) → decide whether to swap CPPA→PIPEDA or annotate "(pending)"; (c) the "(proposed)"-marked template mappings are arguably already correct. Do NOT touch the US annex / joint-controller "CPPA" = California Privacy Protection **Agency** (a different entity). One coherent follow-up sweep PR.
- **(from PR #265 / FR-139, low)** Optional tidy: [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md):95 header reads "All Tier 1 and Tier 2 systems must have:", but the FR-139 backup-gap bullet (:99) now references Tier 3/Tier 4 RPOs in a clarifying parenthetical. Reads fine (cross-ref to the targets table), but the maintainer may wish to broaden the header to "All systems" so the section scope matches the per-tier guidance. Not a defect.
