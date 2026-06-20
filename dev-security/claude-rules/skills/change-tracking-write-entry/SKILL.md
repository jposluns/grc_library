---
name: change-tracking-write-entry
description: Composes a CHANGELOG entry (or the documented Changelog skip trailer) for a PR. Use when about to commit, open a PR, or finalize a change to user-visible content. Use also when about to claim a change does not need an entry, since the skip trailer is the only sanctioned silence. The entry's required parts (date-and-version header, structured Keep a Changelog sections, file references as markdown links, the "why" not just the "what", verification evidence, phase context) are walked step by step so an entry that would fail the link-coverage gate, the version-monotonicity audit, or the D1 delta gate is caught at the draft stage rather than at CI.
derives_from: ../../governance/change-tracking.md
---

# Change Tracking: Write Entry

## Overview

A CHANGELOG entry is the cheapest form of long-term institutional memory a project has. This skill runs the entry-writing workflow from the canonical rule [`governance/change-tracking.md`](../../governance/change-tracking.md) so an entry that satisfies the rule's contract (and the gates that enforce it) is composed in one pass rather than refined through CI failures.

The rule is the source of truth for normative content (what counts as user-visible content, what the opt-out path is, what the CI gates require, what exception-handling looks like). This skill is the workflow wrapper: when to invoke the protocol, in what order to execute each step, and how to verify the entry before commit.

## When to Use

- Before composing the commit message and PR description that close out a change to user-visible content (a public artefact, an API surface, an observable behaviour, configuration that ships to consumers).
- Before pushing a PR that touches the project's document corpus, schema files, public-facing prose, or any artefact a downstream reader cites.
- Before claiming a change does not need a CHANGELOG entry. Skipping silently is forbidden; the only sanctioned silence is the `Changelog: skip (reason: ...)` trailer with a documented rationale.
- When CI's delta gate, link-coverage gate, or version-monotonicity audit flags a missing or malformed entry. The fix is to write or correct the entry, not to weaken the gate.
- When opening a multi-PR rollout where each PR will land its own entry with phase context that connects them.

## Process

The entry-writing workflow from the canonical rule, executed in order:

1. **Classify the change**. Is the work in scope for an entry, or does it qualify for the skip trailer?
   - **Entry required** when the change adds, removes, or alters a public artefact; could surprise a downstream consumer who updated without reading the entry; or will be cited later in answering "when did this happen?" / "why does this work this way?".
   - **Skip trailer permitted** when the change is internal tooling invisible to users (CI runner bumps, dev-dependency lockfile-only updates), a pure refactor with no behavioural change, or a typo fix in a non-citable string. If skipping, draft the trailer with a one-line rationale; the trailer is logged as audit evidence the same way an entry is.
   - **When in doubt, write the entry.** The cost of an unneeded entry is small; the cost of a silently-missed entry compounds.

2. **Choose the date and version**. Use the project's existing convention (CalVer, SemVer, monotonic integer). The version must strictly increase over the prior entry; merge-conflict resolutions that drop a version bump are the failure mode the version-monotonicity audit catches. The date pins the entry to wall-clock time.

3. **Write the title sentence**. Plain language, summarising the change in one sentence a future reader can act on. "Phase 2: add gate-discipline rule to dev-security pack" is a title; "Updates" is not.

4. **Pick the Keep a Changelog section(s)** that most accurately classify the change: `Added`, `Changed`, `Removed`, `Fixed`, `Security`. A single entry may use multiple sections. Do not bury a removed-public-API event under `Changed`; misclassification is a documentation failure downstream consumers will pay for.

5. **Wrap every file reference as a markdown link**. The link-coverage gate scans for bare path-shaped code spans (text inside backticks that looks like a relative path) and fails on any not wrapped. The required form is a markdown link whose display text is the path in backticks and whose target is the same path; convert at draft time, not after the gate fails.

6. **Record the "why", not only the "what"**. The diff already records what changed. The entry records why. "Bumped the version" is a what; "bumped the version because a downstream consumer needed v1.7 to ship Phase 3" is a why.

7. **Attach verification evidence** for any non-trivial change. Which gates ran, which passed, which were intentionally skipped (and why). "All N audit gates pass standalone" is verification evidence; "looks good" is not.

8. **Add phase context** when the entry is one PR in a multi-PR rollout. Which phase this is, what is still ahead. Readers landing mid-rollout need the table of contents.

9. **Re-read the entry once before committing**. Catch the stale claims now: a file mentioned in the title that the diff did not touch; a version number that does not match the heading; a section heading that misclassifies the change.

## Skip Trailer Discipline

When the change qualifies for the skip trailer, the message footer (commit message or PR description) carries:

```
Changelog: skip (reason: <one-line rationale>)
```

The trailer is parsed by `git interpret-trailers --parse` and indexed for later audit. Reviewers who see `Changelog: skip` on a behaviour-changing PR are expected to reject it and require an entry; the trailer is not a free pass.

## Red Flags

- Vague titles ("Misc fixes", "various improvements", "general cleanup", "minor updates", "housekeeping"). If the work spans multiple unrelated changes, write multiple bullets, one per change.
- Bare file path references in code spans that are not wrapped as markdown links. The link-coverage gate will fail; fix at draft time.
- A `BREAKING` change classified under `Changed` to soften its appearance. Misclassification is a documentation failure.
- Copying the commit message verbatim into the entry. The audiences are different: the commit message is for the reviewer; the entry is for everyone who reads the project later.
- "I'll add the entry in a follow-up PR." The discipline is per-PR; follow-up entries decouple the change from its description and erode the audit trail.
- Bypassing the delta gate with `git commit --no-verify`. See the gate-discipline rule: never weaken a gate to silence a failure.
- Adding a `Changelog: skip` trailer to a behaviour-changing PR. The trailer is for internal tooling and non-user-visible changes; misuse defeats the audit trail.

## Verification

The entry is ready when:

- Date and version header are present; the version strictly increases over the prior entry.
- Title sentence summarises the change in plain language.
- Keep a Changelog section(s) classify the change accurately, including a `BREAKING` callout when relevant.
- Every file referenced in the entry text is wrapped as a markdown link.
- The "why" is captured, not only the "what".
- Verification evidence is named: which gates ran, which passed.
- Phase context is attached for multi-PR rollouts.
- A re-read has found no stale claims.

For skip-trailer PRs the verification is shorter: the trailer is present, the reason is documented in one line, and the reviewer has confirmed the skip is appropriate for the change class.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The change is small; the diff is the entry." | The diff is not searchable for "when did X happen?". The entry is. |
| "I'll roll up several PRs into one entry at release time." | The per-PR gate prevents this; do not defer entries to work around it. |
| "Adding an entry is bureaucratic overhead." | The cost is paid once by the author. The cost of *not* having an entry compounds across every future reader. |
| "The reviewer can read the diff if they want context." | The reviewer of this PR can. The reader two years from now cannot, because the PR thread is buried. |
| "It is just a refactor; no entry needed." | If the refactor changes a public API or observable behaviour, it needs an entry. Pure internal refactors qualify for the skip trailer with a documented reason. |

## See Also

- Canonical rule [`governance/change-tracking.md`](../../governance/change-tracking.md): the full discipline, the three CI gates that implement it (delta gate, link-coverage gate, version-monotonicity gate), monorepo coordination, generated-CHANGELOG workflows, document-corpus conventions, framework alignment (NIST SSDF PO.5 / RV.2 / PS.1 / RV.1, CSA CCM CCC-01 to 03 / LOG-02 / LOG-08 / CCC-04, ISO 27001 A.5.4 / A.8.32 / A.8.15 / A.8.27), and the exception-handling protocol for embargoed or deferred entries.
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): when the delta gate, link-coverage gate, or version-monotonicity audit fails, diagnose-then-fix the entry; do not weaken the gate.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): the verification-evidence section of an entry is itself a state assertion. Quote the gate output, do not paraphrase it.
- Related skill [`artefact-discipline-check`](../artefact-discipline-check/SKILL.md): generated artefacts are never hand-edited; if the CHANGELOG is generated by a tool (release-please, towncrier), the generated file is checked into the repository and the entry is reviewable in the PR diff.
- Related skill [`skill-authoring-discipline`](../skill-authoring-discipline/SKILL.md): adding a new skill is a tracked change; its CHANGELOG entry follows this skill's discipline (the new skill addition is itself a "Added" line that satisfies the delta gate and link-coverage gate).
