# Pending Decisions

**Status:** non-empty

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (here, because the `AskUserQuestion` primitive errored repeatedly this session, a
transient permission-stream failure), it records the decision here and continues, rather
than stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Entries

### 2026-06-26: project-governance separation §5.3 register classifications

- **Question**: Should `register-coverage-gaps.md` and `register-document-review-schedule.md`
  both migrate to `.project-governance/` (the abstractly-recorded 2026-06-26 decision "move
  both"), given that the concrete citation map shows both are functionally cited by corpus
  deliverables?
- **Evidence surfaced (Sweep-56 resume session, this turn)**:
  - `register-coverage-gaps.md` is cited 4x as ADOPTER routing logic in
    [`docs/decision-tree.md`](../docs/decision-tree.md) (lines 38/112/275/342: "for known
    coverage gaps, see ..."; "check ... for whether your situation is recorded as Planned,
    Deferred, or Out of scope") and 1x in [`docs/template-startup-roadmap.md`](../docs/template-startup-roadmap.md):41,
    and the corpus index ([`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md):57)
    describes it as "Honest disclosure of sectors, jurisdictions, regulations, cloud
    providers, and capabilities not covered by the library". The separation spec's own
    [§3.1](../governance/specification-project-governance-separation.md) lists "the content
    registers an adopter would reference" as **corpus**. So the citation evidence supports
    `register-coverage-gaps.md` being corpus, not project; moving it forces severing
    adopter-guide routing with no §4-permitted re-point target (a deliverable cannot link
    into `.project-governance/`; gate 53 enforces this).
  - `register-document-review-schedule.md` is a filled-in operational instance (this
    project's review schedule) by §3.2, so the "move" intent is cleaner for it; its corpus
    citers are mostly Related-Documents pointers (clean sever) plus a body row in
    [`governance/procedure-library-quality-and-review-cadence.md`](../governance/procedure-library-quality-and-review-cadence.md):93
    and an adopter-template example in
    [`docs/template-maturity-self-assessment.md`](../docs/template-maturity-self-assessment.md):252
    (both re-pointable to the review-record TEMPLATE pattern rather than this project's
    filled instance).
- **Options** (surfaced in chat; recommended first):
  - **A (recommended)**: keep `register-coverage-gaps.md` as corpus (resolve its §5.3 row to
    §5.1 "stays"); migrate only `register-document-review-schedule.md` with careful
    re-pointing of its corpus citers. Justification: the spec's own §3.1 criterion plus the
    concrete adopter-routing evidence; no-degradation, fully reversible.
  - **B**: honour "move both" but reword the 4 `docs/decision-tree.md` references to route
    adopters via the decision tree's own logic rather than the moved register (preserve
    adopter function without the cross-layer link).
  - **C**: move both and sever the adopter-guide references outright (strict §4, accepts the
    adopter-guide functionality loss).
- **Originating task**: §5.3 register migration (handoff next-session-queue item 1).
- **Interim action**: `deferred-blocked: no safe default` (genuinely authorial per the spec's
  own §5.3 "decide per artefact on its own merits" framing; no default both honours the
  recorded "move both" AND avoids degrading adopter deliverables / overriding §3.1). Routed
  AROUND to the next independent queue item (FR-167 batch 5, resilience), which has no
  unresolved authorial decision. The §5.3 work is held pending the maintainer's pick.
- **Status**: pending.
