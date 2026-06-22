# Overnight PR

**Status:** in-flight

<!-- OVERNIGHT-PR-IN-FLIGHT -->

## Authorization scope

Maintainer directive (2026-06-22 evening EST / 2026-06-22 night UTC): batch up small → medium → large TODO items from both fitness runs (2026-06-21 r1 and 2026-06-22 r1) that do NOT need maintainer approval. Run autonomously overnight per the new batching rule (PR #192): each PR carries one substantive item + the prior PR's /validate-pr history row + any fix for findings from the prior PR's /validate-pr. The expected morning state is a list of merged items in CHANGELOG for review.

Skip rules:
- Any item that requires a design decision (canonical pick between conflicting sources; new template shape; new policy threshold; new role definition; CLAUDE.md edits) → pause and move to next item.
- If the initial list is exhausted, queue more no-approval items from the TODO fitness backlog.

## Items planned (initial list)

Sequence (small → medium):
1. FR-127 (small) — TLS 1.2 → TLS 1.3 in `security/framework-zero-trust-architecture.md` (align to encryption-policy canonical)
2. FR-128 (small) — CAPA records retention 5y → 7y in `governance/register-data-retention-schedule.md` (align to procedure)
3. FR-129 (small) — Internal audit reports retention 5y → 7y in `governance/register-data-retention-schedule.md` (align to procedure)
4. FR-113 (small) — Expand CAPA + SIEM acronyms in `README.md` Repository Structure (align to PR #172/#179 pattern)
5. FR-115 (small-medium) — Add Risk Owner row to `governance/register-role-authority.md` (uses existing ERM standard §3 definition from PR #178)
6. FR-132 (small) — Glossary order in `docs/decision-tree.md` (move earlier or note PR #4/#106 acronym-density reductions)
7. FR-87 (medium) — SSRF range list completion (add canonical entries)
8. FR-88 (medium) — Cipher suite enumeration (add canonical entries)
9. FR-46 (medium) — "Chief" role-name inconsistency sweep
10. FR-49 (medium) — Governance heading drift sweep
11. FR-50 (medium) — NIST citation format drift sweep
12. FR-51 (medium) — ISO 27001 Annex-form drift sweep
13. FR-52 (medium) — review-frequency "and/or" sweep
14. FR-48 (medium-large) — H2 numbering drift sweep
15. FR-116 (medium) — Risk Owner monitoring cadence (extend §8.1 with score-band cadences; aligned to risk register conventions)
16. FR-117 (medium) — Risk Owner evidence expectations (extend §9)
17. FR-125 (medium) — Emergency-access revocation escalation (add escalation clause mirroring §1.2.1-1.2.4)
18. FR-126 (medium) — Auto-escalation mechanic specify ITSM automation
19. FR-130 (small-medium) — Decision-tree entry sequence (move portal to item 1)
20. FR-104 (medium) — Newcomer per-regulation context

Items deliberately skipped (need approval):
- FR-12/118 (treatment-vocab canonical choice)
- FR-14/114 (maturity-ladder reconciliation, multi-doc decision)
- FR-119 (Risk Owner duplicate definition rename or unify)
- FR-120 (180-day citation justification rework)
- FR-121-123 (emergency-access definitions need operational thresholds)
- FR-124 (access-review revocation timeline pick)
- FR-131 (Quickstart vs adopter-guide reconciliation)
- FR-112 (README maintainer-context narrative reframe)
- FR-58 (inheritance vocab design)
- FR-47 (DPO role structural)
- New documents (FR-30/31/32/33/34/70/71/72/73/83)
- FR-15/23/24 (methodology decisions)
- FR-53 (metadata field unification)
- FR-36/59/60/61/62/63/64/65/66 (substantial-content additions)

## Files being authored / modified

Will be enumerated as PRs ship.

## Files NOT touched

`.claude/CLAUDE.md`, `dev-security/claude-rules/*` rule files, audit gate source files (`tools/lint-*.py` other than necessary regression fixtures), `governance/specification-*` files.

## Build progress

PRs shipped overnight (will be enumerated):

## Open ambiguities surfaced

Will be enumerated as encountered.
