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
