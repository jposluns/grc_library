# Deferred protected-file changes (overnight → daytime apply queue)

**Purpose / persistent reminder (maintainer-directed 2026-07-05).** In OVERNIGHT mode,
protected-file edits are DEFERRED: they need the maintainer's authorization (a click/tap the
maintainer cannot give while away), per the A1 answer at the 2026-07-05 resume ("in overnight
mode I won't be there to authorize claude.md changes; do not pause asking me for
authorization, anything that requires me to click/tap must be deferred to day time runs").
Protected surfaces are `.claude/` (including `.claude/CLAUDE.md`, commands, hooks, settings)
and the `dev-security/claude-rules/` governance pack. This file is the persistent staging
area for those deferred changes; it lives in `.working/` (not protected), so it can be
written during the overnight run and survives across sessions on `main`.

**Mode-transition protocol (overnight → daytime).** When the maintainer switches the session
from overnight to daytime / attended mode:

1. **Finish the then-current PR** (do not abandon it mid-flight).
2. **Then clear this backlog**: apply every prepared protected-file change below, each as its
   own PR or a coherently-grouped one, with `tools/lint-language.py` run on the new/edited
   pack prose BEFORE the first commit, and full per-PR `/validate-pr` + `/retro`.
3. **Rotate each item out** of this file as it lands (record in CHANGELOG + DONE as usual);
   when the file is empty it holds only this header.

The items below are **drafted in advance during the overnight run** so the daytime apply is
quick: the content is ready and only the authorized apply + QA remains.

---

## Prepared items (apply at daytime, in this order)

_Landed in PR #652 (2026-07-05): item 1 (codify the mode-transition protocol in CLAUDE.md,
now the `Overnight-to-daytime protected-backlog clearance` paragraph in the
`## Attended-autonomous operating mode` section) and item 5(a) (reword the rule-3 fallback to
drop the longer-check-in option). Landed in PR #654 (2026-07-05): item 2 (the pack-tree ATLAS
technique-ID currency refresh, TODO 3.18 closed: eight `AML.T0048` re-pointed to `AML.T0053`
and two gloss drifts corrected against the held ATLAS 2026.06 CSVs). Landed in PR #655
(2026-07-05): item 3 (the guardrail-review SKILL cadence clause, TODO 3.15 D-F2 closed: the
auto-prompt bullet now names gate 60 and states the deferral is bounded, warn at drift 1 to 2,
fail at 3). Landed in PR #656 (2026-07-05): item 4's PACK surfaces (the D-F3 corollary clauses
on the pack CLAUDE.md rule-index one-liner, the pack README tree blurb, and the pack README
scope row; pack `1.54.6`). Landed in PR #657 (2026-07-05): item 4's remaining
project-CLAUDE.md clause, so TODO 3.15 D-F3 is now FULLY closed and item 4 is rotated out.
Item 5's remaining r5 close-out-checklist clauses re-scope from the former #657 bundle to a
focused #658 (maintainer-directed 2026-07-05: after #657, small Priority 3 and Priority 1
items first to clear TODO count; the larger GR-P design track, item 6, defers)._

### 5. [TODO 3.15 r5] CLAUDE.md close-out-checklist clauses (items (a)/(b)/lag landed in #652/#659; the `/claim-fit` clause remains, deferred to the next session)

- **Target:** `.claude/CLAUDE.md`.
- **(a) DONE, landed in #652 (2026-07-05):** the maintainer chose "reword the fallback"; the
  attended-autonomous rule-3 fallback now drops the "idle on a longer check-in" option and
  cross-references the no-long-interval-check-ins clause, so the self-contradiction is resolved.
- **(b) DONE, landed in #659 (2026-07-05):** the close-out checklist's reconcile bullet now names
  D7 (the handoff-snapshot freshness PR-time check) as the mechanized version-token half of the
  Current-truth reconcile (the gate-50 naming pattern).
- **Deferred, now content-ready (drafted 2026-07-06 overnight, spec pass done):** the `/claim-fit`
  cadence-section candidate (#630 out-of-window observation). The research pass is complete (the
  `claim-fit` SKILL was read and the clause modeled on the existing `## Compliance-matrix
  semantic-fit cadence (/matrix-fit)` section); only the authorized apply plus per-PR QA remain.
  Apply as a NEW `## Normative-attribution claim-precision cadence (/claim-fit)` section in
  `.claude/CLAUDE.md`, sibling to the `/matrix-fit` section, with this text (CLAUDE.md is gate-39
  and gate-51 exempt, so the gate-number phrasing and dashes are unconstrained there, but the draft
  is kept dash-free and P7-safe regardless):

  > Corpus documents attribute specific values (a retention period, a clock, a threshold) to named
  > normative sources. Whether the cited source actually PRESCRIBES the attributed value, its
  > precision, the citation gates cannot check: the existence, currency, and control-code gates
  > confirm a source exists and the citation is well-formed, not that the source states the value.
  > That class, "attributed value, silent source" (the FR-120 shape: a fixed 180-day baseline
  > attributed to NIST SP 800-53 CA-6 and ISO/IEC 27001 Clause 9.2, neither of which prescribes a
  > fixed interval), is gate-blind by construction. The durable instrument is a cadenced audit, the
  > `claim-fit` skill (slash command `/claim-fit`): it judges each worklisted claim against the held
  > source TEXT in the reference base (four verdicts: `prescribed`, `informed-not-prescribed`,
  > `mis-attributed`, `source-not-held`), scoped by the recall-oriented worklist
  > `tools/audit-claim-precision.py` produces.
  >
  > Run `/claim-fit` on this cadence: (1) the one-time full Tier-A pass at adoption (done in #630,
  > establishing the baseline); (2) after any batch that adds or edits normative-value claims (a P2
  > content batch, a jurisdiction annex, a KPI or SLA table), judging the new Tier-A rows the batch
  > introduced and sampling its Tier-B rows; (3) ad-hoc when a claim is in doubt (a maintainer flag,
  > a `/validate` or `/full-qa` note, an apply-time uncertainty about whether a source states a
  > value).
  >
  > It is NOT a gate and NOT a substitute for the citation gates; it is the precision layer on top of
  > them (a claim must pass the existence and currency gates first). An `informed-not-prescribed`
  > finding is fixed by the attribution PHRASING, never the value (the value is often the corpus's own
  > canonical choice); a `source-not-held` claim routes to the maintainer's source-drop queue, never
  > adjudicated from memory. Findings are fixed in-window or routed under the normal triage; a
  > zero-finding run still gets a history row. This cadence shipped across two PRs: the advisory tool
  > `tools/audit-claim-precision.py` in #621 and the skill plus the adoption pass in #630.

  On apply, wrap `claim-fit`, `matrix-fit`, `tools/audit-claim-precision.py`, and the SKILL path in
  markdown links (as the `/matrix-fit` section does) and confirm the broken-link gate passes. Its PR
  number is not yet assigned; do not re-pin it to a specific number here.
- **DONE, landed in #659 (2026-07-05, grouped with (b)):** the summary/description-lag close-out-checklist
  half-line (the #650-#653 `/retro` candidate, at four in-window occurrences): when a PR marks a
  summary surface resolved or landed, or a mid-PR verifier reword changes a term or value on a
  primary surface, update or grep the paired detail/description surfaces in the same commit.

### 6. [TODO 4.7 GR-P1..P5] Pack design improvements (design-tier)

- **Targets:** the `dev-security/claude-rules/` pack (rules, skills, README, overlay pointers).
- **Prep status:** design-tier, larger; draft the shape proposals during the overnight run if
  time permits after the corpus/tooling/P2 work, else leave prep notes. GR-P1 session-lifecycle
  pack rule; GR-P2 rule operative-core condense; GR-P3 third-occurrence-to-gate escalation;
  GR-P4 overlay primary-wins pointers + pruning stance; GR-P5 `derives_from` re-point + exception-
  register hoist + the CLAUDE.md Boundaries-line wrong-trio correction. These are their own PRs.

---

_Empty of items = nothing deferred. Add an item whenever an overnight task turns out to need a
protected-file edit; draft its content here rather than deferring it as a bare pointer._
