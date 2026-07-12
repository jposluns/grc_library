# `.working/`: Maintainer Working Space

This directory holds operational artefacts produced by maintainer-invoked tooling: per-run records, detailed reports, working drafts, and other outputs that assist the maintainer but are not part of the published GRC library content.

## What `.working/` is

- **Maintainer-only working state.** The files here are reference material for the library maintainer, used to justify decisions, track per-run outputs, and capture detail that does not belong in the canonical corpus.
- **Frozen-state archives.** Each file is a snapshot at the moment it was written. Cross-references and links are accurate as-of that moment and are not maintained against subsequent corpus changes.
- **Exempt from audit gates.** This directory is listed in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS`. Broken-link drift, language-style drift, citation staleness, and orphan status here are expected and do not fail CI.

## What `.working/` is not

- **Not library content.** Adopters reading the corpus do not need to read `.working/`. The library's normative content lives in the domain directories (`ai/`, `compliance/`, `governance/`, etc.) and the dev-security claude-rules pack.
- **Not generated artefacts.** `docs/portal.md`, `docs/maturity-scorecard.md`, and `taxonomy.yml` are mechanically generated from corpus metadata. `.working/` is hand-curated or AI-assisted but human-reviewed; not a build output.
- **Not for adopter consumption.** Adopters cloning the library should treat `.working/` as the upstream maintainer's local state; delete it, ignore it, or keep it as historical context, their choice.

## Standard layout for each activity

Each maintainer activity gets its own subdirectory. The subdirectory contains three artefact types, following a uniform convention so a fresh reader can navigate any activity the same way:

| Artefact | Path | Purpose |
|---|---|---|
| Static convention info | `<activity>/README.md` | What the activity is; file naming convention; file format spec; failure-mode taxonomies; maintenance protocol; framework alignment; fork guidance |
| Cumulative history | `<activity>/history.md` | Reverse-chronological table of every invocation: date, finding counts, resulting PR, one-line summary. New rows on top. |
| Per-run detail | `<activity>/YYYY-MM-DD-...md` | Full report. **Created only when the run produced findings.** Zero-finding runs leave only a row in the history table. |

This layout is the convention for any `.working/` activity. When a new activity ships, it creates its subdirectory with the README + history.md skeleton; per-run detail files are created on demand.

## Top-level files

Single-file artefacts that don't fit the activity-subdirectory shape because they're growing ledgers or single-purpose documents:

| File | Purpose | Origin |
| --- | --- | --- |
| [`DONE.md`](DONE.md) | Closed-TODO ledger: which backlog items each PR closed, keyed by original ID. Complements the root [`CHANGELOG.md`](../CHANGELOG.md) (which records file-level change detail). | PR #131 |
| [`design-decisions.md`](design-decisions.md) | Reference log of design decisions: working-state conventions, audit-programme architecture decisions, language conventions, decisions explicitly dropped. Thematically organized. Complements [`DONE.md`](DONE.md) (closed items, not decisions) and [`../CHANGELOG.md`](../CHANGELOG.md) (file-level change detail). | PR #135 |

## Activities

| Activity | Subdirectory | Purpose | Origin |
| --- | --- | --- | --- |
| Validation sweeps | [`validate-sweeps/`](validate-sweeps/) | Records from `/validate` invocations (corpus-wide regression sweep). | PRs #115-#118 |
| Library fitness reviews | [`fitness-reviews/`](fitness-reviews/) | Records from `/fitness` invocations (whole-corpus ten-persona library-quality review). | PR #120 |
| Detailed changelog | [`changelog-details/`](changelog-details/) | Maintainer-grade detailed CHANGELOG mirror (full structured-section entries per PR; root CHANGELOG carries lead paragraphs only). | PR #125 |
| Pack-hygiene scrub fragments | [`pack-hygiene-fragments/`](pack-hygiene-fragments/) | Verbatim removal archive for the pack-hygiene generalization of the distributable pack (skills, README, guidance); retained here as the archive, NOT appended to the removal ledger (the maintainer-choice option in that dir's README, to avoid bloating the ledger with the lineage fragments). | pack-hygiene staging (2026-07-11); applied #842 |

**To add a new activity**: create the subdirectory with `README.md` (absorbing static convention info) and `history.md` (empty table). Per-run detail files land as runs produce findings. Append a row to the Activities table above; the `Origin` column carries the PR / skill / activity that introduced the activity. Top-level single-file artefacts (DONE-shaped ledgers, single-purpose registers) go in the Top-level files table immediately above instead.

## Fork guidance

If you fork or clone this library as a starting point for your own GRC programme:

- **You may safely delete `.working/`**, nothing in the library's canonical content depends on it.
- **You may keep it as historical reference**, the contents document decisions the upstream maintainer made and may inform your own adaptation.
- **You should not extend the upstream `.working/` with your own working state**, create a fresh `.working/` for your own outputs; mixing the two histories defeats the audit-trail value on both sides.

## License

The contents of this directory inherit the library's CC BY-SA 4.0 license (see [`LICENSE`](../LICENSE)). Files written here by AI coding assistants may include verbatim subagent transcripts; those are derivative works of the corpus they review and carry the same license.
