# Change Tracking Discipline

Every change to user-visible content carries a CHANGELOG entry by default. The entry records what changed, when, and why, in a form a future maintainer (or a future you) can read without re-reading the diff.

A "change" is any modification that:
- Adds, removes, or alters a public artefact (document, API, schema, config option, observable behaviour)
- Could surprise a downstream consumer who updated to the new version without reading the entry
- Will be cited later when answering "when did this happen?" or "why does this work this way?"

The audit trail is the value. Code review captures local correctness; the CHANGELOG captures temporal context. The two artefacts are complements, not substitutes.

This rule applies equally to human developers and to AI coding assistants. An AI assistant that ships a change without a CHANGELOG entry (and without a documented skip trailer) is, in this respect, indistinguishable from a junior developer who does the same; the resolution is identical: every PR carries an entry, or carries a trailer explaining why it does not.

---

## What a CHANGELOG entry must contain

Every entry must include:

1. **A date-and-version header**. The date pins the entry to wall-clock time; the version pins it to a release. The version monotonically increases across entries.
2. **A short title sentence** summarising the change in plain language. "Phase 2: add gate-discipline rule to dev-security pack" is a title; "Updates" is not.
3. **Structured sections** following the Keep a Changelog convention: `Added`, `Changed`, `Removed`, `Fixed`, `Security`. A single entry may use multiple sections. Use the section that most accurately classifies the change; do not bury a removed-public-API event under `Changed`.
4. **File references**, with every touched file linked from the entry text. A link-coverage gate (see below) enforces that bare path references in markdown code spans are wrapped in markdown links so readers can navigate to the file from the entry.
5. **The "why"**, not only the "what". The diff already records what changed; the entry records why. "Bumped the version" is a what; "bumped the version because a downstream consumer needed v1.7 to ship Phase 3" is a why.
6. **Verification evidence** for any non-trivial change. Which gates ran, which passed, which were intentionally skipped (and why). "All audit gates pass standalone" is verification evidence; "looks good" is not.
7. **Phase context** for any change that is part of a multi-PR rollout: which phase this is, what is still ahead. Readers who land in the middle of a rollout need the table of contents.

---

## The opt-out path

Some PRs do not require a CHANGELOG entry. The exception is narrow and documented:

- Internal tooling changes invisible to users: CI runner version bumps, dev-dependency lockfile-only updates, comment-only changes in non-citable files.
- Pure refactors with no behavioural change and no surface-area change.
- Typo fixes in non-citable strings (a typo in a private internal variable name is a candidate; a typo in a normative requirement statement that other documents cite is not).

For these, the PR carries an explicit trailer in the commit message or in the PR description:

```
Changelog: skip (reason: <one-line rationale>)
```

The trailer is logged by the CI gate the same way an entry is. The reviewer must approve the skip; a missing entry with no trailer blocks the PR. The trailer is not a free pass: a reviewer who sees a `Changelog: skip` on a behaviour-changing PR is expected to reject it and require an entry.

The trailer-based opt-out is preferred over inline waivers, code-comment justifications, or verbal approvals in a chat channel because it is mechanically inspectable: a script can grep the trailer out of `git log` years later. Verbal approval is not auditable.

---

## Prohibited anti-patterns

These responses must never substitute for a real CHANGELOG entry:

- **Silent changes**. Shipping a user-visible change without an entry and without a skip trailer. The most common form of this anti-pattern is bundling "while I'm in here" cleanups into a feature PR and not mentioning them. Either add them to the entry, or split them into a separate PR with its own entry.
- **Vague entries**. "Misc fixes", "various improvements", "general cleanup", "minor updates", "housekeeping". A reader cannot act on these. If the work spans multiple unrelated changes, write multiple bullets, one per change.
- **Batched-up entries**. Rolling up many weeks of unrecorded changes into one omnibus entry at release time. The per-PR gate prevents this if enforced; do not work around the gate by deferring entries.
- **Retroactive entries**. Adding an entry after the change shipped, dated to look like it was concurrent. The git history shows the truth, and the deception is worse than the missing entry would have been.
- **Entries that reference files without links**. A link-coverage gate scans the CHANGELOG for bare path-shaped code spans and fails on any that are not wrapped in markdown links. The gate exists because an entry that says "we changed `foo/bar.py`" without linking it forces every future reader to find the file by hand.
- **Entries that hide behavioural changes under `Changed`**. A change that breaks downstream consumers belongs under `Removed`, or under a `BREAKING` callout near the top of the entry. Misclassifying a breaking change as a non-breaking one is a documentation failure that downstream consumers will pay for.
- **Entries that copy the commit message verbatim**. The commit message is for the reviewer of this PR; the entry is for everyone who reads the project later. The two audiences are different. The entry should explain the change to a reader who does not have the PR diff loaded.
- **Bypassing the gate with `git commit --no-verify` or by demoting the gate from required to optional**. See the gate-discipline rule: never weaken a gate to silence a failure; fix the artefact. A failing change-tracking gate is signalling that an entry or a trailer is missing; supply the missing artefact.

---

## CI enforcement

A change-tracking discipline needs at least three mechanical gates. Implementation details vary by repository; the contract does not.

### The delta gate

- Detects PRs that touch governed content (the document corpus, the public API surface, configuration files that ship to consumers, etc.).
- Requires the same PR to add a CHANGELOG entry, or carry the `Changelog: skip` trailer with a documented rationale.
- Fails closed: if the gate cannot determine whether an entry was added, it blocks the PR. Ambiguity is not approval.

### The link-coverage gate

- Scans CHANGELOG entries for path-shaped code spans (text inside backticks that looks like a relative path).
- Fails if any such code span is not wrapped in a markdown link to the same path.
- Rationale: an entry that mentions `tools/lint-foo.py` without linking it forces every future reader to find the file manually. The cost is paid by every reader; the link is paid once by the author.

### The version-monotonicity gate

- Verifies that version numbers across CHANGELOG entries strictly increase in the order the entries appear.
- Catches accidental version reuse, force-pushes that rewrite history and drop entries, and merge conflicts where two branches both bumped to the same number.
- Pair with a branch-protection rule against force-pushing the default branch; the gate is a backstop, not the primary defence.

---

## Tool-specific guidance

### Git trailers

Use RFC 5322-style key-and-value trailers at the bottom of the commit message:

```
git commit -m "$(cat <<'EOF'
Fix the parser's handling of trailing whitespace

The parser was stripping trailing whitespace before tokenisation, which
caused doctests with intentional trailing whitespace to fail.

Changelog: skip (reason: dev-only test runner; not user-visible)
EOF
)"
```

The trailer can be parsed by `git interpret-trailers --parse` and indexed for later audit. Use a fixed trailer key (`Changelog:`) so the gate parser does not have to fuzz-match.

### Monorepo coordination

In monorepos with per-package CHANGELOGs, the delta gate must know which packages were touched. The convention is:

- One `CHANGELOG.md` per package.
- A PR that touches multiple packages adds an entry to each affected package's CHANGELOG.
- A top-level unreleased CHANGELOG aggregates per-package entries at release time (build-time, not edit-time). The top-level file is generated; do not hand-edit it.

### Generated CHANGELOGs

Tools that generate a CHANGELOG from commit messages (release-please, semantic-release, changesets, towncrier) are acceptable provided:

- The generated file is checked into the repository, not a build-time-only artefact. The repository is the audit trail; ephemeral build output is not.
- The commit-message convention is enforced by a CI lint so the generator has well-formed input. Conventional Commits is one such convention; project-specific conventions are equally fine.
- The generation step is run locally before commit, not in CI alone. CI runs the generator in `--check` mode and fails on drift. (This mirrors the generator-output discipline in the gate-discipline rule.)
- Generated entries are reviewable in the PR diff, the same as hand-written entries. A generator that hides the entry behind "trust the tool" is not acceptable.

### Document corpora (this project's case)

Document repositories have a stronger discipline than code repositories because every document is a citable artefact. The conventions are:

- Per-document version fields are bumped on every substantive change.
- The CHANGELOG entry references the document by path and quotes the new version.
- A version-monotonicity audit verifies that per-document versions only increase.
- A citation-currency audit verifies that external standards references are not stale.

---

## Exception-handling protocol

The skip trailer is the everyday exception. For larger deviations (an embargoed security fix that cannot disclose the "why" yet, a vendor-issued patch that must ship before public attribution, a cross-team coordination that requires a CHANGELOG entry to land later), use the project's exception register:

1. The requestor documents the technical reason the CHANGELOG entry cannot be complete in this PR.
2. The requestor proposes a deadline for the full entry (default 30 days; longer requires governance authority approval).
3. The responsible governance authority reviews and approves, modifies, or denies.
4. The approved exception is recorded with approver, date, scope, and deadline.
5. The PR carries a link to the exception entry in its skip trailer (`Changelog: deferred (exception: <link>)`).
6. Before the deadline, the requestor either lands the full entry or requests renewal.

If the project does not have an exception register, the exception is not available; ship the entry, redacted if necessary.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Change recording | PO.5, RV.2 | CCC-01 to 03 | A.5.4, A.8.32 |
| Audit trail integrity | PS.1, RV.1 | LOG-02, LOG-08 | A.8.15 |
| Version monotonicity | RV.1 | CCC-04 | A.8.27 |
| Change classification (breaking vs non-breaking) | PO.5 | CCC-02 | A.8.32 |

---

## Why this rule exists

A CHANGELOG is the cheapest form of long-term institutional memory a project has. Code review answers "is this change correct now"; the CHANGELOG answers "what changed and why" months or years later, after the original reviewer has rotated off the project and the original PR thread is buried.

The cost of an entry (one short section) is paid once, by the person closest to the change. The cost of *not* having an entry compounds: each future reader who hits the artefact and asks "when did this happen?" pays the price of reading the diff, reconstructing the rationale, and risking a wrong inference. Multiplied across years and contributors, the total cost dwarfs the per-entry cost by orders of magnitude.

The opt-out path exists because some changes are genuinely invisible to consumers and an entry would be noise. It is a documented trailer, mechanically inspectable, reviewer-approved; it is not silence. Silence is exactly what the audit trail is supposed to prevent.

For AI coding assistants specifically: when shipping a change, the entry is part of the change, not a separate concern to be added later. Treat a PR without an entry the same way you would treat a PR without a test: incomplete by construction.
