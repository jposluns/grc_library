# Change Tracking Discipline

Every change to user-visible content carries a CHANGELOG entry by default. The entry records what changed, when, and why, in a form a future maintainer (or a future you) can read without re-reading the diff.

A "change" is any modification that:
- Adds, removes, or alters a public artefact (document, API, schema, config option, observable behaviour)
- Could surprise a downstream consumer who updated to the new version without reading the entry
- Will be cited later when answering "when did this happen?" or "why does this work this way?"

The audit trail is the value. Code review captures local correctness; the CHANGELOG captures temporal context. The two artefacts are complements, not substitutes.

This rule applies equally to human developers and to AI coding assistants. An AI assistant that ships a change without a CHANGELOG entry is, in this respect, indistinguishable from a junior developer who does the same; the resolution is identical: every PR carries an entry, even if terse.

---

## Where CHANGELOG entries live, the two-file split

A project's CHANGELOG may be a single file, OR may be split into two files for audience-separation:

- **Root `CHANGELOG.md`** carries only the **lead-paragraph summary** of each entry. This is the adopter-facing, public-facing, scan-friendly surface. Adopters and downstream consumers read this.
- **Detailed mirror** (project-specific location; in this project: `.working/changelog-details/CHANGELOG-detailed.md`) carries the **full structured-section entry**: Added / Changed / Removed / Fixed / Security / Verification / discipline observations. This is the maintainer-grade audit trail. Reviewers and auditors read this.

The detailed mirror's location is project-specific; the project chooses where to put it. A working-directory location (exempt from corpus audit gates) is the recommended default. Single-file projects keep all detail in root `CHANGELOG.md`; they are the trivial case of the rule (root file holds everything).

## What a CHANGELOG entry must contain

Every entry must include the following. Items 1, 2, and the lead "why" are recorded in the **root** file; items 3-7 (structured sections, file references, verification, phase context) are recorded in the **detailed** file when the project uses the two-file split, or in the root file when the project does not.

1. **A date-and-version header**. The date pins the entry to wall-clock time; the version pins it to a release. The version monotonically increases across entries.
2. **A short title sentence** summarising the change in plain language. "Phase 2: add gate-discipline rule to dev-security pack" is a title; "Updates" is not.
3. **Structured sections** following the Keep a Changelog convention: `Added`, `Changed`, `Removed`, `Fixed`, `Security`. A single entry may use multiple sections. Use the section that most accurately classifies the change; do not bury a removed-public-API event under `Changed`.
4. **File references**, with every touched file linked from the entry text. A link-coverage gate (see below) enforces that bare path references in markdown code spans are wrapped in markdown links so readers can navigate to the file from the entry.
5. **The "why"**, not only the "what". The diff already records what changed; the entry records why. "Bumped the version" is a what; "bumped the version because a downstream consumer needed v1.7 to ship Phase 3" is a why.
6. **Verification evidence** for any non-trivial change. Which gates ran, which passed, which were intentionally skipped (and why). "All audit gates pass standalone" is verification evidence; "looks good" is not.
7. **Phase context** for any change that is part of a multi-PR rollout: which phase this is, what is still ahead. Readers who land in the middle of a rollout need the table of contents.

---

## Terse-entry convention for ancillary changes

Every PR carries an entry. There is no skip path. The audit trail is the value, and the audit trail cannot have silent gaps.

What changes is the *shape* of the entry, not its existence. Two shapes are sanctioned:

1. **Substantive entry** (default): the full date-and-version header, structured Keep a Changelog sections, file references as markdown links, the "why", and verification evidence. This is what items 1-7 in `## What a CHANGELOG entry must contain` describe. Use this for any PR that ships, modifies, or removes adopter-facing content; changes observable behaviour; or carries a discipline lesson a future maintainer would benefit from.
2. **Terse entry** (one-liner): the date-and-version header followed by a single sentence describing what was accomplished. No structured sections, no file links, no verification block. Use this for ancillary changes whose substantive scope is small:
   - Internal tooling or AI-assistant guidance changes invisible to adopters (changes under `.claude/`, working-state-only edits under `.working/`).
   - Pure refactors with no behavioural change and no surface-area change.
   - Typo fixes in non-citable strings (a typo in a private internal variable name is a candidate; a typo in a normative requirement statement that other documents cite is not).

Terse-entry shape:

```
## YYYY-MM-DD, Library Version X.Y.Z, PR #N

[scope] for local project: [one sentence on what was accomplished].
```

Example: ``.claude/ changes for local project: added a `## Version-bump discipline` section to CLAUDE.md codifying when each version surface bumps across a multi-commit PR.``

The terse entry is not a free pass: a reviewer who sees a terse entry on a behaviour-changing PR is expected to reject it and require the substantive form. Classify generously when in doubt: the substantive entry is always allowed for ancillary changes (and is sometimes worth writing anyway, to record a discipline lesson). The terse entry is the floor, not the ceiling.

The two-file split applies regardless of shape: a terse entry in root `CHANGELOG.md` is paired with a terse entry in the detailed mirror. The detailed mirror's entry may carry a few sentences of additional context (which files were touched, which gates verified) without escalating to full structured sections; the discipline is "match the shape on both surfaces" rather than "always full detail in the mirror".

---

## Prohibited anti-patterns

These responses must never substitute for a real CHANGELOG entry:

- **Silent changes**. Shipping a change without any entry, terse or otherwise. The most common form of this anti-pattern is bundling "while I'm in here" cleanups into a feature PR and not mentioning them. Either add them to the entry, or split them into a separate PR with its own entry.
- **Skip-trailer shortcuts**. Previous conventions allowed a `Changelog: skip (reason: ...)` trailer to bypass the entry requirement. This rule no longer sanctions that pattern; every PR carries at least a terse entry. A project's CHANGELOG-delta CI gate may still accept the skip trailer as a back-compat measure during a transition window, but the rule does not authorise its use; the terse-entry convention replaces it.
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
- Requires the same PR to add a CHANGELOG entry (terse or substantive form per the convention above).
- **For projects using the two-file split**: requires the same PR to modify BOTH the root file and the detailed mirror in lock-step. A PR that modifies one without the other is a discipline failure caught by the gate.
- Fails closed: if the gate cannot determine whether an entry was added, it blocks the PR. Ambiguity is not approval.
- **Back-compat note**: a delta gate that historically accepted a `Changelog: skip` trailer may continue to do so during a transition window after a project adopts the no-skip convention. The rule does not authorise the skip trailer's use; the gate's continued acceptance is a measure of grace toward in-flight PRs, not a sanction.

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

Under the no-skip convention, every commit message carries the substantive narrative directly (the entry itself lives in `CHANGELOG.md` and its detailed mirror, not in the commit message). There is no project-mandated trailer.

Projects in the back-compat transition window described above may continue to find `Changelog: skip (reason: ...)` trailers in their git history. The trailer remains parseable via `git interpret-trailers --parse` for retrospective audit, but new PRs should not introduce it; use a terse entry instead.

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

### Two-file split workflow

When the project uses the two-file split (root file plus a detailed mirror at a project-specific location), a PR author writes both halves in the same commit. Authorship order within the commit is the author's choice; the gate only checks the diff.

- **In the detailed mirror file**: write the full structured entry. Include the date-version-PR header, the lead paragraph, then the full `### Added / ### Changed / ### Removed / ### Fixed / ### Security / ### Verification` sections plus any discipline observations or design-rationale sections.
- **In the root file**: write the lead paragraph only. Use the same date-version-PR header and the same lead-paragraph wording as the detailed entry. Do NOT carry the structured sections into the root file; they belong only in the detailed mirror.
- **Both files land in the same commit.** The PR-time delta gate enforces lock-step (modifying one without the other fails the gate). Terse entries are paired across both files the same as substantive entries; the discipline is "match the shape on both surfaces" rather than "always full detail in the mirror".

Adopter forks may choose any of these shapes:

- **Single-file**: abandon the split; keep everything in root `CHANGELOG.md`. The rule's content requirements (items 1-7) all apply to the root file in this case.
- **Two-file at a different location**: relocate the detailed mirror to wherever fits the fork's structure. Update the PR-time delta gate's path constant accordingly.
- **No detailed mirror**: rely on git history for full audit trail and keep root file as lead-paragraph summaries only. Document this choice in the fork's CONTRIBUTING.md.

The choice is project-specific; the rule does not mandate one shape. The discipline being enforced is "every substantive PR produces a discoverable entry with the required content placed somewhere", not "every project uses the same file layout".

---

## PR finalization protocol

CHANGELOG entries record what shipped in each PR. They do not, on their own, tell a reader which TODO items each PR closed; that information is implicit in the PR's CHANGELOG entry but is not surfaced for direct lookup. Projects that keep a forward-looking TODO file benefit from a complementary "closed-TODO" ledger and from a small set of PR-finalization behaviours that keep TODO and the ledger honest.

The discipline has three components.

### TODO is forward-looking; historical state rotates out

A project TODO file is for *upcoming work*, not for *completed work*. When a PR closes a TODO item, the item is removed from TODO in the same PR. Removal means deletion of the line, paragraph, or subsection, not a strikethrough, not a "[done]" suffix, not a `Status: completed` annotation. The audit trail of what closed lives elsewhere (CHANGELOG, DONE ledger, git history), so TODO stays small and current.

The same rule applies to subsections that record historical context: "PRs completed this session", "Key design decisions made this session", "Files we wrote last week". These have no place in TODO; they belong in a DONE-shaped ledger or in the CHANGELOG.

### DONE ledger keyed by original backlog ID

A `DONE.md` file (or equivalent name; the convention is the file, not the filename) records which backlog items each PR closed, keyed by the original TODO identifier or by the PR number. The DONE entry is **1-2 sentences**, no file links, no version-bump notes, no verification block: just a headline of what was accomplished.

The metaphor that works: DONE is **scrolling battle-text**, the `tail -f` view of shipped work. A maintainer scanning DONE should be able to recognize each item at a glance without parsing prose.

DONE complements CHANGELOG, does not duplicate it:

- **CHANGELOG entries** carry the narrative: file-level detail, version bumps, verification evidence, rationale, discipline lessons. Adopters and downstream consumers read CHANGELOG for the full story.
- **DONE entries** are the at-a-glance index: a maintainer (or auditor, or future you) grep-searches DONE asking "did we ever ship X?" and finds a one-or-two-sentence headline pointing at a PR. From the PR number, the maintainer navigates to CHANGELOG (or to the PR diff in git history) for detail. DONE does the index job; CHANGELOG does the narrative job.

Terse DONE-entry shape:

```
### PR #N: [headline] (YYYY-MM-DD)

[One sentence on what was accomplished, optionally a second sentence for cross-references that matter at a glance.]
```

Worked example:

```
### PR #172: FR-4+5+6+7+8: README polish bundle (2026-06-21)

Five medium README polish findings closed in one PR: acronym expansion, doc count pointer, CalVer placement, audience-signal panel, version-line demote.
```

That's it. No links, no version bumps, no rationale, no list of touched files. Those belong in CHANGELOG.

DONE is typically maintainer-only working state, so it lives wherever the project keeps such state. A working-directory location is the recommended default; under this project's convention, `.working/DONE.md`. The exact location is project-specific.

When a PR closes a TODO item:

1. Delete the item from TODO in the same PR.
2. Add a terse entry to DONE in the same PR. The entry's primary key is the PR number that closed the item, with the original backlog ID (`P-X.Y`, `FR-N`, etc.) folded into the headline where the item had one.
3. Both edits live in the same commit so reviewers see the rotation in one place.

The rotation is enforced by convention rather than by a gate (gate enforcement would require parsing TODO and DONE structurally, which is brittle; the convention is cheaper and matches how the maintainer mentally tracks the work).

### After-merge: list the upcoming next-N planned PRs

When a PR merges, the next thing the assistant (or the maintainer) does is consult TODO's forward-looking section and list the upcoming N planned PRs in the chat. Default N is 5; the exact count is project-configurable.

The rationale is the same as the "named alternatives" rule in `clarify-before-acting.md`: surfacing the queue lets the maintainer redirect early, before the assistant has committed work to a wrong-priority PR. Listing also forces the assistant to confirm that TODO is actually current; if TODO is stale, the list of "next 5 PRs" exposes it immediately.

Before listing the upcoming PRs, the assistant first checks whether any new items have surfaced during the just-finished work (proposals from the maintainer, new follow-ups from the PR's own findings, design questions deferred). New items are added to TODO before the list is published. This is the same shape as the rotation discipline above: TODO stays current as a precondition for any other reasoning about what to do next.

### Anti-patterns

- **Strikethrough-instead-of-delete.** A line `~~PR #99: do X~~` in a queued-work section is decoration, not signal. The line still has to be read every time someone reviews TODO, and it cumulatively makes TODO harder to navigate. Delete the line.
- **"Recently completed" subsection in TODO.** This is just DONE in a worse location. Move it to DONE.
- **Closing the item in CHANGELOG only and assuming TODO will get cleaned up "later".** Later never comes; TODO drifts. The rotation happens in the same PR or it doesn't happen reliably.
- **Listing the next-N PRs from memory rather than from TODO.** The point of the list is to surface what's actually queued and let the maintainer redirect; surfacing what the assistant happens to remember defeats the discipline. The list comes from TODO; if TODO is stale, refresh TODO first.
- **Closing an item that was never in TODO and pretending it was.** DONE entries cross-reference real TODO items by their original ID. If the work was unplanned, the DONE entry says so explicitly ("not previously in TODO; surfaced during PR #N as a follow-up"). The fiction of a phantom backlog item is worse than the absence.

### Overnight-work protocol

When the maintainer authorizes an autonomous overnight session (the assistant ships work while the maintainer is asleep or otherwise unavailable), the assistant records the session's state in a designated overnight file (project-specific location; in this project: `.working/overnight-pr.md`). The file's `Status` field encodes the session's lifecycle:

- `stub`: no overnight session is in flight. This is the default state. The file contains only the protocol description plus the `Status: stub` line.
- `in-flight`: an overnight session is active. The assistant has filled the file with session content (authorization scope, design decisions made, files being authored / modified, build progress, open ambiguities). Each overnight PR ships with `Status: in-flight`.
- `done`: the overnight session has ended. The next-morning processing PR then routes the content and resets the file.

The morning-processing PR routes the file's content into the appropriate working-state ledgers (design decisions to the design-decisions ledger, closed work to DONE, queued follow-ups to TODO) and resets the file to `Status: stub`.

An audit gate enforces this lifecycle: it fails when `Status: done` (overnight session ended but morning processing missing) or when the file is malformed (missing `Status:` line, invalid value). It passes on `stub` and `in-flight`. The three-state field (rather than a binary "stub vs non-stub") preserves the overnight workflow: overnight PRs need to pass CI to land, and they pass the gate while in flight.

The protocol matters because overnight work generates state that's easy to lose track of: design decisions, surfaced ambiguities, and queued follow-ups all accumulate in the overnight file. Without a structured handoff, the maintainer wakes up to a populated file with no mechanical pressure to process it. The gate's `done`-state failure is that mechanical pressure: CI goes red until the morning processing PR ships.

**Stub-form contents.** The stub file is not empty; it carries a short description of the protocol (so a future reader landing on the file understands its purpose) plus the `Status: stub` line. A `<!-- OVERNIGHT-PR-STUB -->` marker comment is recommended for grep-based detection but not strictly required by the gate; the gate's only check is the Status value.

**Initial overnight commit.** The first overnight PR's diff includes the file transitioning from `stub` to `in-flight` plus the initial content. The PR description explains the maintainer's authorization scope.

**Final overnight commit.** The session's last commit (often a dedicated close-out commit, but acceptable as the final overnight PR's last commit) transitions the file from `in-flight` to `done`. The morning-processing PR is now required.

**Morning-processing PR.** A small focused PR (no other scope) that:
1. Reads each section of the overnight file.
2. Routes content: design decisions → design-decisions ledger; closed work → DONE; queued follow-ups → TODO; any pure-noise content (build-progress checklists, files-touched lists) is discarded.
3. Resets the file to the stub form with `Status: stub`.
4. Bumps the library version per the change-tracking discipline; writes CHANGELOG entries.

The gate passes immediately after this PR lands.

**Exception path.** If a session's authorization changes mid-flight (e.g., the maintainer awakens earlier than expected and continues the work directly), the file's `Status` can transition from `in-flight` back to `stub` directly, as long as the file's content has been processed appropriately or was minimal enough to discard. The discipline is: do not leave `Status: done` lingering.

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
