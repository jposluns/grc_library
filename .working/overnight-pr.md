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

## Files being authored / modified (final list)

Corpus content files modified:
- `security/framework-zero-trust-architecture.md` (PR #193, FR-127)
- `governance/register-data-retention-schedule.md` (PR #194 + PR #195, FR-128 + FR-129)
- `README.md` (PR #196, FR-113; plus library-version bumps in every PR)
- `governance/register-role-authority.md` (PR #197, FR-115)
- `risk/standard-enterprise-risk-management.md` (PR #197 + #198 + #199, FR-115 + FR-116 + FR-117)
- `docs/decision-tree.md` (PR #200, FR-132)
- `dev-security/standard-developer-security-requirements.md` (PR #201, FR-81 partial)
- `dev-security/standard-api-security.md` (PR #201, FR-81 partial)

Working-state files updated (every PR):
- `CHANGELOG.md` and `.working/changelog-details/CHANGELOG-detailed.md`
- `.working/DONE.md`
- `TODO.md`
- `.working/validate-pr/history.md` (one row added per merged PR)
- `taxonomy.yml`, `docs/portal.md`, `docs/maturity-scorecard.md` (regenerated whenever per-doc metadata changes)

## Files NOT touched (preserved)

- `.claude/CLAUDE.md` — pack-rule file, approval-needed for the overnight batch.
- `dev-security/claude-rules/*` rule files — same; the FR-81 pack CLAUDE.md surface and the FR-87/FR-88 owasp.md surfaces are deferred.
- `governance/specification-*` files — spec changes are governance decisions.
- Audit gate source files (`tools/lint-*.py`) — except by necessity for regression fixtures, none touched.

## Build progress

PRs shipped overnight (in order):

| PR | FR | Severity | Outcome |
|---|---|---|---|
| #193 | FR-127 | H[critical] | TLS 1.2 → 1.3 in ZTA framework (align to encryption policy) |
| #194 | FR-128 | H[critical] | CAPA retention 5y → 7y (align to procedure-capa §12) |
| #195 | FR-129 | H[critical] | Internal audit reports retention 5y → 7y (align to standard-internal-audit §8.3) |
| #196 | FR-113 | M | CAPA + SIEM acronym expansion in README (matches PR #172/#179 pattern) |
| #197 | FR-115 | H | Risk Owner row added to Role Authority Register + reciprocal cross-reference |
| #198 | FR-116 | M | Risk Owner monitoring cadence by score band (align to §5.2 scoring-threshold table) |
| #199 | FR-117 | M | Risk Owner evidence by accountability action (new §9.2 mapping; uses existing §3/§6/§8.1/§9.1) |
| #200 | FR-132 | L | Decision-tree §2.1 glossary-order annotation |
| #201 | FR-81 | M (partial) | TLS 1.3+ alignment in dev-security/standard-developer-security-requirements + standard-api-security |

**9 PRs / 9 FR closures (8 full + 1 partial).** Convergent Finding C1 (Risk Owner role insufficiency): 3 of 4 closed (FR-115, FR-116, FR-117; FR-119 deferred — needs decision). Convergent Finding C3 (retention chain breaks): fully closed (FR-128 + FR-129).

All /validate-pr invocations on PRs #193 - #201 returned 0 findings each (one exception: PR #193 surfaced 1 finding which was bundled into PR #194 fix; PR #195 surfaced 1 out-of-window observation which was bundled into PR #196 cleanup). The batching rule (codified PR #192) worked as designed.

## Open ambiguities surfaced (for maintainer review)

These items were identified during the overnight session as needing decisions; they remain in TODO awaiting your input:

1. **FR-81 third surface**: `dev-security/claude-rules/CLAUDE.md` carries the same TLS 1.2-minimum framing as the corpus standards I aligned in PR #201. The pack CLAUDE.md edit is approval-needed (changes the assistant's pack-rule context). Apply the same TLS 1.3+ alignment? (Yes / No / Other framing).
2. **FR-87 + FR-88 (SSRF range list + cipher suite enumeration)**: live in `dev-security/claude-rules/core/owasp.md` (pack rule). Deferred — pack-rule edit. Worth fixing because the current SSRF list has both an incorrect notation (172.16.x.x — should be 172.16.0.0/12) and missing IPv6 ranges (fc00::/7, fe80::/10, ::1, 100.64.0.0/10 CGNAT, cloud-metadata IPv6 endpoint).
3. **FR-50 (NIST citation format drift)**: the canonical-citations register's example uses `NIST SP 800-53 Rev 5` (no period), but NIST's publisher convention is `NIST SP 800-53 Rev. 5` (with period). Picking one canonical form needs maintainer decision; the register itself may need updating.
4. **FR-51 (ISO 27001 Annex form drift)**: "Annex A.X" (28 instances) vs "A.X" (449 instances). The shorter form is dominant. Pick canonical form (or keep both as contextually-distinct usages).
5. **FR-52 (review-frequency "and/or")**: "annually AND on material change" vs "annually OR on material change" — semantically different (one mandates both triggers; the other allows either). Pick one as the project's intent.
6. **FR-46 (Chief role-name inconsistency)**: many docs say "Privacy Officer" where the register says "Chief Privacy Officer". May be intentional in some contexts (operational delegate role). Per-occurrence judgment required, or a maintainer-approved blanket rename.
7. **FR-104 (newcomer per-regulation context)**: decision-tree §1.4 lists 7 regulations as bullet-list choices. Each needs a 1-line "what each covers" descriptor; authorial choice.
8. **FR-130 (portal entry-point reorder)**: fitness suggests moving portal to item 1 of decision-tree §2.1, replacing README. PR #200 explicitly preserved the existing pattern; maintainer pick which structural ordering wins.
9. **Privacy Officer vs Chief Privacy Officer**: connected to FR-46; the corpus uses "Privacy Officer" 10+ times in `privacy/procedure-data-subject-rights-management.md`. Decide: are these distinct roles or shortenings?

## Status: in-flight

Session continues in-flight. Morning-processing PR by the maintainer will:
1. Read this file's content.
2. Route the design-decisions to `.working/design-decisions.md` (the 9 open ambiguities above).
3. Confirm the PR list has been fully reflected in CHANGELOG / DONE.
4. Transition Status: in-flight → stub.
