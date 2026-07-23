# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-07-23, Library Version 2026.07.570, PR #1082

Canonicalizes the "GRC Manager" role title to "GRC Programme Manager" corpus-wide per TODO §3.71 (a Tier-2, single-session, corpus-wide rename). The canonical role is the one in [`governance/register-role-authority.md`](../../governance/register-role-authority.md); no "GRC Manager" role exists.

### Changed
- **60 role-title occurrences across 5 corpus documents** renamed from "GRC Manager" to "GRC Programme Manager": [`compliance/procedure-audit-planning.md`](../../compliance/procedure-audit-planning.md) (25), [`compliance/procedure-capa.md`](../../compliance/procedure-capa.md) (30, including the two section headings §2.3 and §7.2), [`security/policy-encryption-and-key-management.md`](../../security/policy-encryption-and-key-management.md) (2), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md) (1), and [`supply-chain/procedure-supplier-audit.md`](../../supply-chain/procedure-supplier-audit.md) (2). Compound forms (`CAE/GRC Programme Manager`, `Compliance and GRC Programme Manager`, the possessive, the plural) and the two headings were all handled. Each document's `Version` and `Date` were co-bumped and [`taxonomy.yml`](../../taxonomy.yml) + [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated. Out of the FR-210 internal-audit scope (that standard was already canonical since #906/#907), so routed and done as this sweep.

### Verification
- Applied deterministically: an ordered `str.replace` (plural, then title-case, then lowercase-heading form) across the 5 files, count-verified at exactly 60 (25/30/2/1/2, matching the offloaded census) with zero residual in those files; a full-corpus grep confirms zero in-scope residual (only frozen `.working/` QA records and the now-deleted TODO block retained the historical string). All 73 audit gates pass.
- The two renamed CAPA headings (§2.3, §7.2) break no anchor: a repo-wide grep found no `#grc-manager-*` inbound links, and the in-doc references use section NUMBERS (unchanged).
- A substantive-tier skeptical verifier (refute-briefed) read every changed line: all 60 substitutions read naturally with no double-substitution, the distinct `Compliance Manager` and `Trade Compliance Manager` roles were correctly left untouched, and the count reconciliation is exact (60 removed = 60 added). Verdict SHIP, 0 findings. The per-touch reference-breadth check was run on the 5 docs (candidates were pre-existing topic-match breadth suggestions orthogonal to a role-title rename; no citation action) and the doc-state refreshed.

### Discipline observation
Offloaded census + substitution rules (worker-a, pinned to the current main tip, per the worker-brief `### Corpus-wide rename PR` override); a corpus-wide rename is single-session-apply (not partitioned across workers), so the orchestrator applied the deterministic substitution serially and re-verified. Batched PR #1081's `/validate-pr` plus `/retro` rows. Library 2026.07.569 to 2026.07.570.

## 2026-07-23, Library Version 2026.07.569, PR #1081

Widens the decision-log deferral-trigger keyword set per TODO §3.103. Machinery (a hook + its cross-repo mirror + a self-test + a stale-pointer fix); no corpus, gate, or version-corpus-doc change. Cross-repo, orchestrator-only (workers cannot read or write `_private`).

### Changed
- **[`.claude/hooks/block-unjustified-decision.py`](../../.claude/hooks/block-unjustified-decision.py)**: the deferral/hold keyword tuple that gates the forbidden-internal-state-justification check was widened from the original five (`blocked`, `defer`, `wind down`, `wind-down`, `skip`) to also cover the common synonyms (`hold off`, `postpone`, `punt`, `back-burner`, `sit on`, `leave for later`, `do it later`, `push to`, `park it`), so a deferral phrased around the original five no longer escapes the forbidden-phrase check (the #1049 validate-pr NOTE). `park it` (not bare `park`) is used to avoid a substring false match; the check is double-gated (a keyword AND a forbidden phrase must both be present), so the false-positive surface is minimal. A new `test_synonym_deferral_with_forbidden_blocked` self-test proves a synonym-phrased deferral carrying a forbidden phrase is caught (10 hook self-tests pass).
- The mirrored `_private` decisions-log validate check (`grc_library_private`, direct-pushed separately) was widened to the IDENTICAL tuple, keeping the two in exact parity per their shared contract.
- **[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md)** `## Decision discipline`: the paragraph's stale forward pointer ("widening the deferral-marker set ... is TODO §3.103") was removed and replaced with a done-state description, and the old five-marker enumeration was updated to name the widened set with synonym examples (the §N-orphan cross-file cleanup for closing §3.103).

### Verification
- All 73 audit gates pass; the hook self-test suite passes 10/10 (including the new synonym case); `ast.parse` clean on both edited Python files; the `_private` validate run reports `validation OK`. Both the hook and the `_private` mirror carry the byte-identical widened tuple (parity confirmed). Per the #1080 discipline, the language and unbalanced-fence audits were run on the edited [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) (fences balanced; the added lines carry no new language findings).
- Verified directly by the orchestrator (a small mechanical keyword-set widening kept in cross-repo parity); no standing skeptical-verifier subagent, proportionate to the change weight.

### Discipline observation
Offloaded investigation would not help here (the `_private` half is orchestrator-only), so the whole change is orchestrator-authored. The `_private` half was pushed directly to its repo in lock-step; a brief inter-repo parity skew during the grc_library PR window is harmless (both are independent defence-in-depth checks, neither depends on the other at runtime). Batched PR #1080's `/validate-pr` plus `/retro` rows. Library 2026.07.568 to 2026.07.569.

## 2026-07-23, Library Version 2026.07.568, PR #1080

Closes the gate-66 (Unbalanced-fence audit) default-population shape gap per TODO §3.11. Documentation only (a close-out checklist clause in the project governance file); no gate-code, gate-count, or four-surface change.

### Added
- **[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md)**: a clause appended to the existing new-pack-prose close-out checklist bullet (the `## Session migration and PR close-out checklist` section). Gate 66, the Unbalanced-fence audit [`tools/lint-unbalanced-fences.py`](../../tools/lint-unbalanced-fences.py), fails any scanned markdown file that ends inside an open fenced code block, but its DEFAULT walk exempts the `.claude/` tree (via the shared `DEFAULT_EXEMPT_DIRS`), while the mandated new-pack-prose language audit [`tools/lint-language.py`](../../tools/lint-language.py) scans `.claude/` files via explicit paths; so an unbalanced fence in a `.claude/` file could silently truncate the language audit's tail while the unbalanced-fence audit's default walk never sees the file. The new clause requires running the unbalanced-fence audit on the SAME explicit paths (it accepts explicit path arguments), catching the unbalanced fence rather than letting it suppress the language audit. This is exactly the paired usage the tool's own module docstring already prescribes.

### Verification
- All 73 audit gates pass (documentation add; the `.claude/` tree is exempt from the corpus gates). Applying the very discipline this clause documents: the language audit and the unbalanced-fence audit were both run on the edited governance file; the unbalanced-fence audit is clean (balanced), and the added six lines introduced zero new language findings (the file's pre-existing, ungated `.claude/`-exempt dashes are unchanged and out of scope).
- Chose the conservative option (b) of the two §3.11 named (a close-out checklist clause), NOT option (a) (widening the audit's default walk, a gate-code change): the gap is specific to the files the language audit scans explicitly, so pairing the two audits on that same invocation is the tightest fit and avoids a permanent default-scope divergence from the shared exempt-dirs convention.
- Verified directly by the orchestrator; no standing skeptical-verifier subagent, proportionate to the change weight.

### Discipline observation
Offloaded investigation+draft (worker-a), pinned to the current main tip. The worker identified gate 66 exactly (spec §6 line 147), confirmed the concern against the tool's docstring, and recommended option (b); the orchestrator verified gate 66's identity and applied the clause to the protected governance file. Recycled-number note: the closed wind-down-SOP §3.11 (PR #523) is a distinct item. Batched PR #1079's `/validate-pr` plus `/retro` rows. Library 2026.07.567 to 2026.07.568.

## 2026-07-23, Library Version 2026.07.567, PR #1079

Adds a new-jurisdiction/sector-annex discoverability override to the worker brief per TODO §3.23. Documentation only (a [`.working/worker-brief-template.md`](../worker-brief-template.md) override block); no gate, no code change.

### Added
- **[`.working/worker-brief-template.md`](../worker-brief-template.md)**: a new `### New jurisdiction / sector annex PR` block in `## Overrides per PR class`. For a new-annex PR, the worker's research must enumerate, beyond the annex body, the FULL discoverability surface set: the document-index register and domain README listing; the decision-tree surfaces the annex routes into (§5.1, §3.3, FAQ §7 in [`docs/decision-tree.md`](../../docs/decision-tree.md), all three verified present at apply); the register-coverage-gaps §2.5 entry; the glossary entry for new acronyms; the generated taxonomy/portal/maturity-scorecard; plus completeness extras (matrix/crosswalk rows, Related-Documents cross-links) marked as beyond the §3.23 block's explicit list. Closes the multi-surface-incompleteness class from deep-assessment Sweep 92 (the #733 US HIPAA and #743 EU AI Act annexes wired primary surfaces but left the decision-tree FAQ §7, decision-tree §3.3, and register-coverage-gaps §2.5 stale).
- The worker-brief-template `Version` co-bumped 1.4.6 to 1.4.7 with `Date` (D2/D4).

### Verification
- All 73 audit gates pass (documentation add). The three decision-tree section numbers the override cites (§5.1 "AI", §3.3 "healthcare", §7 FAQ) were verified present in the live [`docs/decision-tree.md`](../../docs/decision-tree.md) before applying.
- Verified directly by the orchestrator; no standing skeptical-verifier subagent, proportionate to the change weight.

### Discipline observation
Offloaded candidate (worker-a), pinned to the current main tip (the pin-to-main lesson from #1078, applied). The order's framing matched the actual §3.23 TODO block this time (worker confirmed). Batched PR #1078's `/validate-pr` plus `/retro` rows. Library 2026.07.566 to 2026.07.567.

## 2026-07-23, Library Version 2026.07.566, PR #1078

Adds a worker-brief guard rail for path-enumerating gates per TODO §3.35. Documentation only (a [`.working/worker-brief-template.md`](../worker-brief-template.md) rail); no gate, no code change, no version-surface ripple.

### Added
- **[`.working/worker-brief-template.md`](../worker-brief-template.md)**: guard rail 15 (appended to `## Guard rails (verify before submitting)`). A new gate or check whose configuration enumerates live repo paths (a `SURFACES`-style table of a file path plus the header or field the gate reads from it) ships a regression fixture that asserts every configured path EXISTS in the real repo and that its parse target matches that file, so a renamed, misspelled, or relocated configured path fails in the fixture rather than silently mis-resolving on the next triggering PR in CI. Precedent: the D7 handoff-snapshot check's `test_surfaces_table_paths_resolve_in_real_repo`. Closes the F6 confabulated-live-path class (caught at PR #634: a gate's config named a live path that did not exist, so the gate mis-resolved and failed its own PR).

### Verification
- All 73 audit gates pass (documentation add; no behavioural change), including gate 51 (`.working/` prose-hygiene) on the new rail.
- Verified directly by the orchestrator; no standing skeptical-verifier subagent, proportionate to the change weight.

### Discipline observation
Offloaded candidate (worker-a). Apply-time correction (research-assistant discipline): the dispatch order mis-framed §3.35 as link-resolution-coverage; the worker read the ACTUAL §3.35 TODO block and corrected it to the CONFIGURED-PATHS-EXIST (F6) intent, which the orchestrator verified against [`TODO.md`](../../TODO.md) before applying. The worker also flagged (not silently) that the order's pinned `grc_library_sha` was the pre-squash PR branch-head (unreachable after the squash-merge), and ran against the content-equivalent `main` tip; the pin-to-squash-merge/main-SHA lesson is recorded in the §3.35 retro. Batched PR #1077's `/validate-pr` plus `/retro` rows. Library 2026.07.565 to 2026.07.566.

## 2026-07-23, Library Version 2026.07.565, PR #1077

Codifies a test-isolation convention per TODO §3.96. Documentation only (a new section in [`tests/README.md`](../../tests/README.md), which is not a versioned corpus document); no gate, no code change, no version-surface ripple.

### Added
- **[`tests/README.md`](../../tests/README.md)**: a new `## Global-state isolation` section (after `## Fixture isolation`). It states that because [`run-linter-regression.py`](../../tools/run-linter-regression.py) drives every linter in ONE Python interpreter, a test patching a shared or module-level global (an environment variable, a module attribute, `sys.argv`, a class attribute, or a monkeypatched function) must restore it deterministically, via `unittest.mock.patch` (context-manager or decorator form) or a `try/finally` save-and-restore, or the mutation leaks into a sibling test later in the same process. It explicitly warns against relying on a discarded per-test module instance for isolation (fragile: a later shared/cached-import refactor silently reintroduces the leak). This codifies the prevention the #1006 `resolve_sibling` monkeypatch-without-restore leak motivated.

### Verification
- All 73 audit gates pass (documentation add; no behavioural change). The offloaded survey of the full [`tests/test_linters.py`](../../tests/test_linters.py) suite found ZERO live isolation leaks: every shared/process-global patch already restores via `try/finally`. It surfaced two convention-nonconforming-but-currently-safe patch sites (the `_origin_url` / `classify` detect-env tests, safe today via fresh per-test module loads) as optional hygiene, deliberately NOT fixed here to keep the change a disjoint documentation add.
- Verified directly by the orchestrator (a documentation-only convention add); no standing skeptical-verifier subagent, proportionate to the change weight.

### Discipline observation
Offloaded candidate (worker-a), applied by the orchestrator. Batched PR #1076's `/validate-pr` plus `/retro` rows. Library 2026.07.564 to 2026.07.565.

## 2026-07-23, Library Version 2026.07.564, PR #1076

Fixes the D7 handoff-snapshot pre-commit check per TODO §3.89 + §3.101 (a duplicate pair, closed together). Tooling only; a PR-time delta check (`check-*-on-pr.py`), not one of the 73 numbered `run_all_audits.sh` gates, so no gate-count or four-surface ripple.

### Fixed
- **[`tools/check-handoff-snapshot-on-pr.py`](../../tools/check-handoff-snapshot-on-pr.py)**: the D7 check had gone INERT on the current [`.working/session-handoff.md`](../session-handoff.md) layout. It located its snapshot line by the marker `Current truth`, but the version tokens had moved to a dedicated `Version snapshot (D7 validates these tokens)` sub-line, leaving `Current truth` on a token-less header bullet; the token loop then found zero tokens and printed a VACUOUS pass, so a stale snapshot would have passed. The marker now targets the dedicated token line. A **non-vacuity guard** (a refactored, git-free `validate_snapshot_tokens` core) now fails loud if a located snapshot line ever again carries no recognized token, so this silent-inert class cannot recur even if the layout drifts.
- **[`tests/test_linters.py`](../../tests/test_linters.py)** (`HandoffSnapshotOnPrTests`): the `_handoff` fixture helper now reproduces the real two-line production layout (a token-less `Current truth` header, then the `Version snapshot` token sub-line), which both fixes the four tests that encoded the stale single-line layout and regresses the bug; the missing-line assertion updated to the new marker; and a new `test_tokenless_snapshot_line_fails_non_vacuously` proves the guard (a token-less marker line must FAIL, not pass). 7 D7 tests pass.
- **[`tools/lint-changelog-link-coverage.py`](../../tools/lint-changelog-link-coverage.py)** (rider, closing the #1075 `/validate-pr` W1): the module docstring's recognized-extension enumeration was widened to `(.md, .py, .yaml, .yml, .json, .txt, .cff, .toml, .html, .css, .js)` to match the `FILE_EXTENSIONS` tuple #1075 widened. #1075 named the docstring a §3.77 paired surface but updated only the tuple and the fixture; its post-merge `validate-pr` caught the stale enumeration (documentation drift, no behavioural impact), fixed here in the batch that records that warning.

### Verification
- The 7 `HandoffSnapshotOnPrTests` pass (including the new non-vacuity test); the full linter-regression suite passes; all 73 audit gates pass; `ast.parse` clean and stdlib-only (gate 71). Apply-time check confirmed the current handoff carries the `Version snapshot (D7 validates these tokens)` marker (so the new marker choice is live and correct), and the candidate diff applied clean over the intervening [`tests/test_linters.py`](../../tests/test_linters.py) edits from #1074/#1075.
- Verified directly by the orchestrator (a tool + fixture machinery fix; the worker ran the full 444-test suite pre-delivery); proportionate to the change weight, no standing skeptical-verifier subagent.

### Discipline observation
Offloaded candidate (worker-a), applied by the orchestrator via `git apply`. Batched PR #1075's `/validate-pr` plus `/retro` rows. Library 2026.07.563 to 2026.07.564.

## 2026-07-23, Library Version 2026.07.563, PR #1075

Teaches the CHANGELOG link gates to recognize web-template file types per TODO §3.77. Tooling only; a detection-logic widening of an existing gate (no new gate, no four-surface / count ripple).

### Changed
- **[`tools/lint-changelog-link-coverage.py`](../../tools/lint-changelog-link-coverage.py)** (the gate) and **[`tools/preflight-changelog.py`](../../tools/preflight-changelog.py)** (its pre-commit aid): `.html`, `.css`, and `.js` added to the shared `FILE_EXTENSIONS` tuple, kept in step across both files (the aid's tuple is mirrored from the gate's). A bare backtick web-template path (for example an `.html` template under the `.web/templates/` directory) in a CHANGELOG line is now recognized as path-shaped and therefore link-required, closing the gap where a website PR's template reference could ship unlinked (the #950 `/validate-pr` catch, fixed by hand in #951).
- A regression fixture in [`tests/test_linters.py`](../../tests/test_linters.py) (`ChangelogLinkCoverageTests`): a detect case (an unlinked `.html` path fails) and a clean case (a linked `.html` path passes).

### Verification
- The two new fixtures pass; the full linter-regression suite and all 73 audit gates pass. The widened gate run against the live root [`CHANGELOG.md`](../../CHANGELOG.md) returns clean (the re-scan the worker candidate confirmed: zero `.html`/`.css`/`.js` tokens in the root changelog or the detailed mirror, so no reference is newly flagged and no accompanying changelog edit was needed).
- Verified directly by the orchestrator (a 3-line FP-safe symmetric tuple widening with the worker's empirical sandbox proof); no standing skeptical-verifier subagent, proportionate to the change weight.

### Discipline observation
Offloaded candidate (worker-b), applied by the orchestrator: the two tool edits plus the fixture, no CHANGELOG edit needed. Both `FILE_EXTENSIONS` tuples changed together (the aid mirrors the gate; applying only one would drift the aid from the gate). Batched PR #1074's `/validate-pr` plus `/retro` rows. Library 2026.07.562 to 2026.07.563.

## 2026-07-23, Library Version 2026.07.562, PR #1074

Adds gate 73 (COBIT objective title-text) per TODO §1.16 and normalizes the corpus to the canonical COBIT 2019 objective titles, guard-first (the gate and its backfill land together so the corpus is clean when the gate goes live). Maintainer-confirmed 2026-07-17: normalize to the past-participle form; the imperative is not a house paraphrase.

### Added
- **[`tools/lint-cobit-title-text.py`](../../tools/lint-cobit-title-text.py)** (gate 73): a precision-first COBIT 2019 objective title-text audit. Where a corpus document pairs an objective code with a title (a `Managed` / `Manage` / `Ensured` / `Ensure`-led phrase after an optional separator), the title is validated against the canonical `COBIT_OBJECTIVES` title in [`tools/cobit_iso31000_reference.py`](../../tools/cobit_iso31000_reference.py); a code cited with no title or beside a crosswalk cell is allowed. It complements gate 61 (code EXISTENCE), which it defers to (no double-flag), and it leaves the practice titles unchecked (they line-wrap in the held extract; only the 40 objective titles extract cleanly). stdlib-only; shares gate 61's `iter_markdown_targets` scope and `EXEMPT_FILES`. A `CobitTitleTextTests` regression fixture (a detect case plus a clean case) in [`tests/test_linters.py`](../../tests/test_linters.py).
- Four-surface wiring per the gate-35 parity discipline: [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml), [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh), [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml), and the [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 inventory row plus §6 detailed-prose paragraph plus §5 content-drift-defence grouped-list clause.

### Changed
- **Backfill (41 carriers across 32 corpus documents)**: the non-canonical imperative "Manage X" objective titles corrected to the canonical past-participle form (`APO14: Manage Data` to `Managed Data`, `DSS05: Manage Security Services` to `Managed Security Services`, the `APO01` `IT`-to-`I&T` fix, and the `BAI07` truncation fix, among others). Each touched document's `Version` and `Date` were co-bumped; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated. The authoritative count is 41 carriers across 32 files (the gate caught 2 the manual re-derive missed), above the §1.16 estimate of 35 across 28.
- Gate count 72 to 73: the §6 inventory grew by one row; the cross-file count-consistency gate confirms 73 across 545 files with no stale "72" prose in any scanned surface.
- **[`TODO.md`](../../TODO.md)**: §1.16 rotated to [`DONE.md`](../DONE.md); the P1 standing-item intro count moved from five to four.
- Batched PR #1073's `/validate-pr` plus `/retro` rows. Library 2026.07.561 to 2026.07.562.

### Verification
- Full suite green: all 73 audit gates pass. Guard-first: the new gate reports 0 findings post-backfill across 422 files (every objective title now canonical), and the `CobitTitleTextTests` fixture passes 2/2.
- Backfill applied deterministically: the worker's exact per-line diff was `git apply --check`-clean, applied (net +41/-41 across 32 files, only title lines), then the gate re-run confirmed 0 findings (the guard-first re-parse).
- Guardrail-review r12 (the gate-60 cadence, gates 70 to 73 delta): 0 genuine findings across overlap / gap / drift; one below-Low recall-cost note fixed in-window (a docstring clause naming the verb-led recall limitation, matching gate 62's discipline). Recorded in [`.working/guardrail-reviews/history.md`](../guardrail-reviews/history.md), inventory token 73 gates / 13 rules / 24 skills / 15 commands.
- Substantive-tier skeptical verifier on the diff, refute-briefed to check the 41 backfilled titles against the HELD COBIT source in `grc_library_ref` (not merely the gate's own reference module, which would be circular): an 18-title sample across all five domains matched the held source exactly, including the subtle `APO01` "I&T" vs `BAI07` "IT" distinction. SHIP on the substantive change, with two findings fixed pre-push: a Medium (this gate-spec document's body was edited for the gate-73 wiring without its own `Version`/`Date` co-bump, which the pre-push guard's D2/D4 would have failed on) and a Low (a stale `72/72/72/72` parity snapshot in TODO §3.99), both corrected.

### Discipline observation
Offloaded candidate (worker-b: gate plus wiring plus fixture plus the 41-carrier backfill diff), with the canonical-title map re-derived from [`tools/cobit_iso31000_reference.py`](../../tools/cobit_iso31000_reference.py) (the worker corrected the constant name from the seed's `COBIT_OBJECTIVE_TITLES` to the real `COBIT_OBJECTIVES`). Apply-time: the gate authored from the candidate; the backfill git-applied; the 32 `Version` / `Date` bumps scripted; the count migration driven by the count-consistency gate (adding the §6 row was sufficient, no scanned-prose "72" carrier existed). Two apply-time prose catches in the §6 gate-73 paragraph, both fixed before the suite went green: gate 9 flagged "must" near "(TODO section 1.16)", and [`tools/lint-language.py`](../../tools/lint-language.py) flagged a slash-joined backtick run `` `Managed`/`Manage`/`Ensured`/`Ensure` `` whose bare `` `Ensure` `` leaked past its code-span stripping.

## 2026-07-23, Library Version 2026.07.561, PR #1073

Distributes the unattended-degradation auto-handoff discipline into the [`session-lifecycle`](../../dev-security/claude-rules/governance/session-lifecycle.md) governance pack rule per TODO §3.102 (the project instantiation already lives in the project CLAUDE.md; this ships the portable form). Pack-rule prose only; no corpus, gate, or behaviour change.

### Changed
- **[`dev-security/claude-rules/governance/session-lifecycle.md`](../../dev-security/claude-rules/governance/session-lifecycle.md)** and its **[`.claude/rules/governance/session-lifecycle.md`](../../.claude/rules/governance/session-lifecycle.md)** mirror (byte-identical body, gate 37): section 4 (wind-down) gains a paragraph specifying that in an UNATTENDED mode an evidence-triggered close is EXECUTED as the section-5 closing handoff (land working state as a green merge, reconcile the durable handoff record, release the lease) directly, because that handoff is itself the conservative, reversible, no-regret action, and is NOT a bare mid-turn pause that strands unmerged working state and a half-written record. A matching `## Prohibited anti-patterns` bullet is added.
- **[`.claude/rules/governance/session-lifecycle.md`](../../.claude/rules/governance/session-lifecycle.md)** PROJECT-OVERLAY block: adds the project instantiation (the closing handoff takes no `AskUserQuestion`; the concrete close is a green merged PR + a refreshed [`session-handoff.md`](../session-handoff.md) + the [`session-state.md`](../session-state.md) lease RELEASE), kept local-only per the overlay convention.
- **[`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md)**: pack Version 1.62.5 to 1.62.6 plus a `## Version history` row (patch; no new rule or skill; gate 41 rule-count stays 13).
- **[`TODO.md`](../../TODO.md)**: §3.102 rotated to [`DONE.md`](../DONE.md).
- Batched PR #1072's `/validate-pr` (CLEAN) plus `/retro` rows. Library 2026.07.560 to 2026.07.561.

### Verification
- Pre-push guard green (`run_all_audits.sh` 72 gates plus `run-pr-time-checks.sh` D1-D8), including gate 37 (pack-sync body parity) and gate 41 (rule-count parity, 13 unchanged).
- Substantive-tier skeptical verifier (orchestrator-side, refute-briefed) on the pack-prose diff: core change SHIP (body parity byte-identical across both trees, no project-token leak into the pack body, source-faithful, house style clean, rule count 13 unchanged). Two LOW cosmetic nits fixed pre-push (em-dashes in the [`next-prs.txt`](../next-prs.txt) `# then:` line; the pack README `Date` co-bump), both in gate-exempt surfaces.

## 2026-07-23, Library Version 2026.07.560, PR #1072

Adds the cross-repo reference-existence advisory tool per TODO §1.22.4 (the second half of the §1.22.3/§1.22.4 shared-engine pair). Tooling only; advisory (never fails CI); no corpus, gate, or behaviour change.

### Changed
- **[`tools/audit-cross-repo-references.py`](../../tools/audit-cross-repo-references.py)** (new): scans references/pointers/filenames across all trees and file types and classifies each as **in-repo-exists**, **in-repo-missing (dangling)**, **cross-repo pointer** (`_ref`/`_scratch`/`_private`/`grc_library_private`, flagging possible over-exposure of the private siblings), or **ambiguous**. Reuses the existing machinery, NOT a reimplementation: gate 3's link resolver, `lint_common`'s `resolve_sibling`/`sibling_placeholder_present` (the §1.19.2 portable-clone helpers), and the §1.22.3 entry-iteration seam. ADVISORY only (never exits non-zero to fail CI, spans gate-exempt trees), stdlib-only (gate 71), and NO-OPs + exits 0 on sibling-absence (the sibling-absent path emits "existence not verified" notes rather than raising, confirmed against a sibling-free worktree). 5 `--self-test` cases (in-repo-exists, dangling, cross-repo pointer, sibling-absent no-op, resolver reuse).
- **[`TODO.md`](../../TODO.md)**: §1.22.4 rotated to [`DONE.md`](../DONE.md).
- Batched PR #1071's `/validate-pr` (CLEAN) + `/retro` rows. Library 2026.07.559 to 2026.07.560.

### Discipline observation (offload + verify)
- The tool was OFFLOADED as a candidate diff (worker-b) and independently adversarially verified (worker-a, verdict SHIP, all five concerns refuted: advisory, sibling-absent no-op, stdlib-only, classification correctness, resolver-reuse-without-drift). The orchestrator applied it deterministically (`git apply`), re-read the full file, and re-ran `--self-test` (5/5) + a live sample. Two optional future refinements the verifier noted (inline-code-span parity with gate 3; a `tests/tmp/` allow-list) are recorded, not required to ship.

### Verification
- `--self-test` 5/5 OK; a live advisory run exercised (classifies the `_private` pointers as review-over-exposure, exit 0). [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) all gates pass; pre-push guard green.

## 2026-07-23, Library Version 2026.07.559, PR #1071

Adds the no-priority "Maintainer or Egress Gated" registry section to [`TODO.md`](../../TODO.md) per §1.22.7, so the run has one unambiguous place for everything the assistant cannot clear alone (and never claims "done all I could" while maintainer-actionable items remain). Working-state/backlog bookkeeping; no corpus, gate, or behaviour change.

### Changed
- **[`TODO.md`](../../TODO.md)**: appended the "## Maintainer or Egress Gated" section, 47 `MEG-NN` reference-numbered items across four gate groups (Group 1 maintainer-download/source-gated; Group 2 egress-blocked; Group 3 maintainer-decision; Group 4 maintainer-sign-off, LAST by design), each cross-referencing its priority-section item and, for downloads, the recorded source lead. The section flags the **§2.22 status drift** (the egress-queue Fulfilled record indicates the 16 Canada.ca sources were ingested in `_ref` #87 and the currency half discharged, so §2.22's "DEFERRED-BLOCKED" may be stale, reconcile when worked) and the **egress re-test candidates** (MEG-02 MiCA via EUR-Lex, MEG-07 ISO, MEG-20 ISO/IEC 5259, since iso-org + nist-csrc now respond HTTP 200 where earlier sessions saw 403; re-test and clear rather than park). The §1.22.7 backlog bullet was rotated to [`DONE.md`](../DONE.md).
- Batched PR #1070's `/validate-pr` (CLEAN) + `/retro` rows. Library 2026.07.558 to 2026.07.559.

### Discipline observation (worker `_private` readability)
- The offloaded enumeration worker reported it could read `grc_library_private` this session (a maintainer-provisioned clone in the worker's home dir); it read the egress queue read-only and wrote nothing. The §1.19 design intent (`_private` is orchestrator-only; the worker-brief template is locked to scratch) is unchanged, but a worker holding a readable `_private` clone is a deviation from that trust boundary, surfaced to the maintainer for awareness.

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) all gates pass; [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean; pre-push guard green. The MEG enumeration was offloaded (worker-b) and spot-verified by the orchestrator against the live TODO before authoring.

## 2026-07-23, Library Version 2026.07.558, PR #1070

Extends the `.working` cycle-out sweep tool per TODO §1.22.3 (the tool build; the initial destructive sweep and the destructive DONE/pending-decisions entry sweeps are deliberately deferred). Conservative-by-default: the only new destructive path (the one-off-dir sweep) rides the existing emit-verify-prune sequence, and the broader-surface DONE/pending sweeps are surfaced read-only. Tooling only; no corpus, gate, or behaviour change.

### Changed
- **[`tools/sweep-working-records-to-private.py`](../../tools/sweep-working-records-to-private.py)**: (1) added the one-off completed-directory sweep, an explicit orchestrator-maintained `ONEOFF_DIRS` allow-list (never auto-detected; seeded `pack-hygiene-acceptance`, `pack-hygiene-fragments`, both grep-confirmed to have no audit-gate reader), swept WHOLE into `archive/oneoff-dirs/<name>/` on `--emit-archive` and removed on `--prune` after every re-parse assertion; (2) added the read-only `--staleness-report` mode (advisory counts of aged DONE-ledger entries and resolved-and-aged pending-decisions entries whose DESTRUCTIVE sweep is NOT enabled, pending a maintainer cutoff + a DONE `effective_floor` + the conservative pending-decisions predicate); (3) extracted the one-off verify-before-prune into the self-tested `oneoff_missing_from_archive` helper (the verify's one required fix), so the only new destructive path's data-safety guard is locked under `--self-test` (now 7 self-tests).
- **[`TODO.md`](../../TODO.md)**: §1.22.3 marked tool-build-shipped, with the initial destructive sweep (a dedicated cleanup-PR), the DONE/pending destructive-sweep enablement (maintainer-gated), and the policy codification tracked as the remaining follow-ups.
- Batched PR #1069's `/validate-pr` (CLEAN) + `/retro` rows. Library 2026.07.557 to 2026.07.558.

### Discipline observation (offload + verify)
- The implementation was OFFLOADED as a candidate diff (worker-a) and independently adversarially verified (worker-b, verdict SHIP-WITH-FIXES) before the orchestrator applied it. The orchestrator applied the candidate deterministically (`git apply`), re-read the full applied diff, applied the one required fix (the self-tested helper), and re-ran `--self-test` (7/7) + `--dry-run` + `--staleness-report`. The two deferred destructive sweeps are recorded with their gating conditions so a future session does not enable them without the maintainer decision.

### Verification
- `--self-test` 7/7 OK; `--dry-run` and `--staleness-report` exercised against the live tree. [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) all gates pass; pre-push guard green.

## 2026-07-23, Library Version 2026.07.557, PR #1069

Cites the now-held authoritative **OWASP Top 10 for Agentic Applications 2026** in the corpus, correcting the RB-7 residual where the corpus could not cite the framework because only the untrusted AIUC-1 crosswalk was held. The authoritative framework was ingested into `grc_library_ref` separately (`grc_library_ref` PR #101, `frameworks/OWASP/`); its upstream currency was confirmed this turn (Version 2026, released December 2025, current on genai.owasp.org; ASI01-ASI10 roster verified). Corpus content change (two documents); no behaviour or control-requirement change.

### Changed
- **[`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md)**: upgraded the OWASP agentic row from "OWASP Agentic AI Top 10" (URL wrongly pointing at the `agentic-ai-threats-and-mitigations` T-code guide) to the authoritative "OWASP Top 10 for Agentic Applications" (URL `genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/`, description adds ASI01-ASI10, Last-verified 2026-07-23). Version 1.5.38 to 1.5.39.
- **[`ai/register-ai-risk.md`](../../ai/register-ai-risk.md)**: added an OWASP Top 10 for Agentic Applications (2026) framework-alignment row (Reference ASI01-ASI10; relevance = the agentic-AI risk taxonomy), mirroring the #1063 NIST IR 8596 row precedent. Version 1.0.8 to 1.0.9.
- **[`taxonomy.yml`](../../taxonomy.yml)**, **[`docs/portal.md`](../../docs/portal.md)**, **[`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md)**: regenerated (the two Version bumps).
- **[`TODO.md`](../../TODO.md)**: the RB-7 residual's OWASP-Agentic item marked RESOLVED, with the fuller per-control ASI mapping in [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md) (a §36 matrix column + §6 crosswalk, incl. the ASI08/09/10 no-clean-TC-home decision) tracked as a `/matrix-fit`-class follow-up; Colombia RNBD remains egress-gated.
- **`grc_library_ref` (PR #101, separate)**: ingested the authoritative OWASP Top 10 for Agentic Applications 2026 into `frameworks/OWASP/` (extract + catalogue + index regen + gate green); `last_checked` to be backfilled to 2026-07-23 now that currency is confirmed.
- **`grc_library_private` (pushed separately)**: the OWASP Agentic item in the maintainer-egress-requests queue moved to Fulfilled.

### Verification
- Upstream currency confirmed via WebSearch on genai.owasp.org (Top 10 for Agentic Applications 2026, released December 2025, current; ASI01-ASI10 roster matches the held extract). The ASI roster and the register URL were verified against the authoritative source.
- A pre-push skeptical verifier reviewed the diff (citation accuracy, URL correctness, gate-safety of the ASI tokens). [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) all gates pass; [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean; pre-push guard green.

## 2026-07-23, Library Version 2026.07.556, PR #1068

Resume close-out for the 2026-07-23 overnight session (`/resume` from the #1066 handoff, with #1067 merged first per its NEXT block). This is the first PR of the resumed session: the loop-break `/validate` compensating control for the #1067 session-closing handoff, plus the lease acquire, the handoff prune, and the fix of the two notes the sweep surfaced. Working-state only; no corpus or website content changed. (This PR is NOT itself a session-closing handoff, so it takes the normal per-PR `/validate-pr` + `/retro`, batched into the next PR.)

### Changed
- **[`.working/session-state.md`](../session-state.md)**: lease ACQUIRED for this session (`Active-session: claude/resume-sweep118-closeout`, `Status: active`, `Operating-mode: overnight-unattended`, fresh heartbeat); Current-task and Worker-dispatches refreshed for the 2026-07-23 overnight run (both workers live Opus 4.8).
- **[`.working/validate-sweeps/history.md`](../validate-sweeps/history.md)**: added the Sweep 118 iter 1 row (PASS, 0 error / 0 warning / 2 note; loop-break control for #1067). Version 2.0.118 to 2.0.119, Date to 2026-07-23 (its newest-row date).
- **[`.working/session-handoff.md`](../session-handoff.md)**: advanced the resume cursor to Sweep 118, and pruned the Next-actions stack to keep-current-plus-one-prior (deleted the 2026-07-19b/c #1054/#1055 CLOSING + NEXT blocks; Sweep 118 note N-A1). The State-snapshot and Asserted-expectations stacks were already at two blocks.
- **[`README.md`](../../README.md)**: library CalVer `2026.07.555` to `2026.07.556`, README Version `1.9.916` to `1.9.917`, Date co-bumped to 2026-07-23 (the routine per-PR version-surface bump). Note: the `validate-pr` history file is NOT touched this PR; the Sweep 118 note N-A2 against it was re-examined as a false positive (see below).
- **[`.working/next-prs.txt`](../next-prs.txt)**: refreshed the statusline and the `# then:` projection for the #1068 close-out and the overnight tooling queue.
- **`grc_library_private` (pushed separately)**: appended the 2026-07-23 session-start row to the `grc_library_private` degradation-watch log.
- **`grc_library_scratch` (coordination plane, pushed separately)**: enqueued and consumed `sweep-118-validate` (worker-a); enqueued the background `research-1223-working-cycleout`, `research-inbox-delivery-triage`, and `research-p1p3-quickclear-survey` orders for the overnight tooling + quick-clear work.

### Sweep 118 (loop-break compensating control for #1067)
- Full A/B/C `/validate` over the **#1067** delta (base #1066 `f9906bec`, head #1067 `3ceb0c54`), OFFLOADED to worker-20260716-a (Opus 4.8) as blocking prio-0 `sweep-118-validate`, consumed under ELEVATED QA (worker-a delivery 1 this fresh session). **PASS, 0 error / 0 warning / 2 note.** The #1067 delta is bookkeeping-only (8 files, `.working`/CHANGELOG/README; no corpus-domain document). Mechanical baseline 72/72 at the pinned SHA; counts 72/13/24/15/18; four-surface parity 72; gate 54 CSF-clean (336 docs); generated artefacts in sync; 443-test regression rc 0.
- Both notes are C-class `.working/` bookkeeping (gate-exempt; no corpus/gate/adopter impact), re-verified by the orchestrator at source. N-A1 (handoff Next-actions retained three CLOSING blocks vs the stated keep-current-plus-one-prior) was a real over-retention, FIXED this close-out (the 2026-07-19b/c blocks deleted). N-A2 (a [`validate-pr/history.md`](../validate-pr/history.md) header-date "outlier") was re-examined and found to be a FALSE POSITIVE: the file's `2026-07-23` Date is the correct Version-Date co-bump date (delta gate D4) for its #1067 bump, not an error, so the file is left unchanged. Asserted-expectations (the #1056-#1065 block) all CORROBORATED, 0 contradicted. **Loop-break control for #1067 PASSES.**

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): all 72 gates pass. [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean. Pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green.

## 2026-07-22, Library Version 2026.07.555, PR #1067

Resume close-out AND session-closing handoff for the 2026-07-22b resumed session (`/resume` from the #1066 session-closing handoff). The session ran this single PR (the loop-break `/validate` compensating control, the handoff prune, the maintainer-authorized watchdog-alert clear) and then WOUND DOWN at the maintainer's direction, because branch protection requires a `gh pr merge --admin` permission the harness auto-mode classifier blocked (self-granting the permission was likewise blocked). The maintainer will grant the permission and merge this PR next session. Because #1067 is therefore this session's session-closing handoff PR, it takes the handoff-PR exception (skips its own trailing `/validate-pr` + `/retro`; the next `/resume` corpus-wide `/validate` is the compensating control). Working-state only; no corpus or website content changed.

### Changed
- **[`.working/validate-sweeps/history.md`](../validate-sweeps/history.md)**: added the Sweep 117 iter 1 row (CLEAN PASS, 0 error / 0 warning / 0 note / 0 novel; loop-break control for #1066). Version 2.0.117 to 2.0.118.
- **[`.working/session-handoff.md`](../session-handoff.md)**: advanced the resume cursor to Sweep 117, and pruned the per-session Next-actions and State-snapshot stacks to keep-current-plus-one-prior (deleted the 2026-07-19 #1040-#1043 blocks and the superseded mid-session #1044 snapshot of the 2026-07-19b/c session).
- **[`.working/session-state.md`](../session-state.md)**: lease RELEASED at wind-down (`Status: released`, `Active-session: none`, `Operating-mode: attended-autonomous`, heartbeat refreshed) so that when the maintainer merges #1067 next session, `main` lands in a clean released state and the next `/resume` acquires a fresh lease without a stale-active takeover prompt.
- **[`.working/validate-pr/history.md`](../validate-pr/history.md)**: added the #1067 handoff-PR-exemption row (`SKIPPED (handoff-PR exception)` in the Findings cell, gate-50-recognized). Version 1.2.825 to 1.2.826.
- **`grc_library_scratch` (coordination plane, pushed separately)**: enqueued and consumed `sweep-117-validate` (worker-20260716-b), and cleared the scratch maintainer-alert channel's alert 2026-07-22-a (LOW, queue-liveness; already fixed, order delivered clean) on maintainer authorization.

### Sweep 117 (loop-break compensating control for #1066)
- Full A/B/C `/validate` over the **#1056..#1066** deltas (base #1055 `501d77a2`, head #1066 `f9906bec`), OFFLOADED to worker-20260716-b (Opus 4.8) as blocking prio-0 `sweep-117-validate`, consumed under ELEVATED QA (worker-b delivery 1 this fresh session). **CLEAN PASS, 0 findings.** Mechanical baseline 72/72 at the pinned SHA (independently re-run by the orchestrator, matches); counts 72/13/24/15/18; four-surface parity 72; generated artefacts in sync.
- Orchestrator independent corroboration: the #1056..#1066 diff scope (35 files, corpus docs only in the RB-7-cite set); the crypto tighten (EC P-256 in the prohibited asymmetric-encryption cell, not the approved one); the "48h/14d/30d" grep flag resolved as pre-existing own-content (base=head=6, no fabricated GC-attributed matrix). All #1056-#1065 asserted-clean surfaces CORROBORATED, 0 contradicted. **Loop-break control for #1066 PASSES.**

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): all 72 gates pass. [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean. Pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green.

## 2026-07-22, Library Version 2026.07.554, PR #1066

Session-closing handoff for the 2026-07-22 resumed session (`/resume` from #1055; merged #1056-#1065 plus `_ref` #100). Working-state only; no corpus or website content changed. Per the handoff-PR exception (loop-break), this PR skips its own trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` over the #1056..#1066 deltas, cross-checked against this session's asserted-expectations.

### Changed
- **[`.working/session-handoff.md`](../session-handoff.md)**: prepended this session's Next-actions (CLOSING + NEXT SESSION), State snapshot (SESSION-CLOSING at #1066), and Asserted-expectations blocks (the closing session adds; the next `/resume` prunes to keep-current-plus-one-prior).
- **[`.working/session-state.md`](../session-state.md)**: lease RELEASED (`Status: released`, `Active-session: none`, heartbeat refreshed).
- **[`.working/validate-pr/history.md`](../validate-pr/history.md)**: #1065 `/validate-pr` row (CLEAN 0/0/0, offloaded worker-b) batched, plus the #1066 handoff-PR-exemption row (`SKIPPED (handoff-PR exception)` in the Findings cell, gate-50-recognized). Version 1.2.823 to 1.2.825.
- **[`.working/improvement-log.md`](../improvement-log.md)**: #1065 `/retro` row batched (the order-status `new`-vs-`pending` intent-is-not-action lesson). Version 1.0.756 to 1.0.757.
- **[`.working/next-prs.txt`](../next-prs.txt)**: cycled forward to the next session's queue (resume `/validate`, then the §3.87 wiring post-migration, then the RB-7 egress residuals).

### Session summary (durable record; see CHANGELOG root entries #1056-#1065 for detail)
- RB-7 reference-citation track: #1057-#1063 (corpus use/cite of the four maintainer-acquired AI-security frameworks), #1064 (§3.70 pack crypto parity), #1065 (RB-7 close). `_ref` PR #100 merged (Wiz "Securing AI Agents 101" discard-candidate delete; catalogue 727 to 726, `_ref` HEAD `8126580`).
- Started + checkpointed the §3.87 same-VM file-drop transport build: the transport core module (a new file-drop transport tool in `grc_library_scratch`, committed `b1f7ef4`, end-to-end tested) and the maintainer-run migration runbook (in `grc_library_private`) are ready; the wiring resumes next session after the maintainer's `/home/grc` migration (maintainer's checkpoint choice).

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): all 72 gates pass. [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean. Pre-push guard green. Handoff-PR exception: no trailing `/validate-pr`/`/retro`; the next `/resume` corpus-wide `/validate` is the compensating control.

## 2026-07-22, Library Version 2026.07.553, PR #1065

RB-7 reference-acquisition track close-out. RB-7 (maintainer-directed 2026-07-19, from the aidefensematrix.com gap analysis) acquired four AI-security frameworks the maintainer fetched, ingested them into `grc_library_ref`, and applied their corpus use/cite across PRs #1057-#1063 (with the §3.70 pack crypto parity tighten #1064 landed alongside). This PR closes the track: the backlog rotation, the reference-audit pass record, and the batched #1064 QA rows. Working-state only; no corpus or website content changed.

### Changed
- **[`TODO.md`](../../TODO.md)**: the completed RB-7 acquire-and-assess block replaced by a compact RB-7-residual bullet naming the two egress-gated follow-ups (the authoritative OWASP Top 10 for Agentic Applications source; Colombia RNBD Decreto 886/2014), both on the `grc_library_private` maintainer-egress queue.
- **[`.working/reference-audit/history.md`](../reference-audit/history.md)**: a new-ingest + held-item run row for the RB-7 pass (Version 1.0.2 to 1.0.3), linking the per-run detail file; records the two premise corrections the offloaded re-verify caught before apply (the fabricated GC VM 48h/14d/30d matrix kept ABSENT; OWASP Agentic held only as an untrusted AIUC-1 crosswalk, routed to egress, no body cite) and the high-assurance harness's demonstrable improvement on #1060.
- **[`.working/reference-audit/doc-state.md`](../reference-audit/doc-state.md)**: per-document reference-audit state refreshed (via `tools/audit-reference-breadth.py --update-state`) for the 13 touched corpus documents at `grc_library_ref` HEAD `8126580`.
- **[`.working/validate-pr/history.md`](../validate-pr/history.md)**: #1064 `/validate-pr` row (CLEAN PASS, 0 findings, 72/72; offloaded worker-b, byte-identical at HEAD) batched per recursion-avoidance (Version 1.2.822 to 1.2.823).
- **[`.working/improvement-log.md`](../improvement-log.md)**: #1064 `/retro` row batched (Version 1.0.755 to 1.0.756).

### Added
- **[`.working/reference-audit/2026-07-22-rb7-aidefensematrix.md`](../reference-audit/2026-07-22-rb7-aidefensematrix.md)**: per-run detail file for the RB-7 reference-breadth pass (worklist, judge, finding-to-PR mapping, residuals).

### Added (done ledger)
- **[`.working/DONE.md`](../DONE.md)**: RB-7 close entry (PRs #1057-#1064), naming the four acquired frameworks, the seven applying PRs, the two egress-gated residuals, and the `_ref` #100 Wiz delete.

### Cross-repo (companion, not in this PR's diff)
- **`grc_library_ref` PR #100** (merged, HEAD `8126580`): deleted the discard-candidate publication Wiz "Securing AI Agents 101" (full-text, OCR-extracted originals, catalogue entry, SCREENING.md row); catalogue 727 to 726; indexes regenerated; the reference-base validate check passed.
- **`grc_library_private`**: the maintainer-egress-requests register updated (four RB-7 frameworks + Brazil/Colombia legislation moved to Fulfilled; OWASP Agentic authoritative source + Colombia RNBD Decreto 886/2014 added as new pending requests).

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): all 72 gates pass. [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean. Pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green. Working-state / bookkeeping change; the paired root + detailed CHANGELOG entries and the library CalVer / README Version single-bump are the only version surfaces (no corpus document body touched, so no per-document Version/Date bumps).

## 2026-07-22, Library Version 2026.07.552, PR #1064

Pack-layer parity for the §3.70 crypto tightening (maintainer decision 2026-07-22: after the corpus dev-security crypto tables were tightened to P-384 / RSA-4096 in #1052, tighten the distributable pack too rather than leave it approving a below-floor curve). Resolves the pending-decisions §3.70 entry.

### Changed
- **[`dev-security/claude-rules/core/cryptography.md`](../../dev-security/claude-rules/core/cryptography.md)**: the Asymmetric-encryption row changed from "RSA-4096, EC P-256, EC P-384 / RSA < 2048, EC P-192" to "RSA-4096, EC P-384 / RSA < 4096, EC P-256, EC P-192" (EC P-256 moved from approved to prohibited; RSA floor raised to 4096), matching the corpus §3.70 floor.
- **[`dev-security/claude-rules/CLAUDE.md`](../../dev-security/claude-rules/CLAUDE.md)**: the Asymmetric crypto-table row changed from "RSA-4096, EC P-256/P-384 / RSA < 2048" to "RSA-4096, EC P-384 / RSA < 4096".
- **[`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md)**: pack Version 1.62.4 to 1.62.5 with a matching Version-history row.
- **[`pending-decisions.md`](../pending-decisions.md)**: the §3.70 pack-divergence entry marked RESOLVED.

### Scope note
- Only the Asymmetric-ENCRYPTION rows were tightened (the corpus §3.70 change's scope). The Digital-signatures and TLS-certificate rows (ECDSA P-256/P-384) are unchanged: P-256 for ECDSA signatures and certificates is standard-acceptable and out of the §3.70 asymmetric-encryption scope.
- No corpus document changed; the pack cryptography rule is not `.claude/rules`-mirrored (gate 37), so no mirror edit; the pack files are not taxonomy-tracked, so no generated-artefact regen.

### Verification
- `run_all_audits.sh` 72/72; pre-push guard green; an offloaded pre-merge skeptical verify on the pushed SHA. Batches PR #1063's `/validate-pr` + `/retro` rows.

## 2026-07-22, Library Version 2026.07.551, PR #1063

RB-7 held-but-uncited-breadth residual (the two items RB-7 named that were held before the 2026-07 ingest, so the `--ref-since` worklist did not surface them). Offloaded research (`research-rb7-heldbreadth`) corrected the RB-7 premise on both.

### Changed
- **[`ai/register-ai-risk.md`](../../ai/register-ai-risk.md)** (1.0.7 to 1.0.8): a draft-watch see-also row in the Framework-alignment list for **NIST IR 8596 (Cyber AI Profile), Initial Preliminary Draft** (a CSF 2.0-organized AI security profile, three focus areas Secure/Defend/Thwart), clearly labelled DRAFT-WATCH and to be re-pointed to a normative citation on finalization.
- Taxonomy and maturity-scorecard regenerated for the Version bump.

### Findings / decisions
- **NIST IR 8596:** RB-7 named the AI-asset-taxonomy doc as the target, but IR 8596 is a cybersecurity-framework profile (not an asset taxonomy), so the AI system register ([`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md)) is not the fit; the AI risk register's framework-alignment list is. It is a DRAFT (IPRD, `authoritative: false`), so it is added as a draft-watch see-also only, never a normative anchor.
- **OWASP Agentic Top 10:** RB-7 recorded it as held and citable, but the ref base holds only an untrusted publication (the AIUC-1 crosswalk, `trust: untrusted`) that reproduces the taxonomy, not the authoritative OWASP framework. Per the trust model a normative citation cannot rest on it. Maintainer decision (2026-07-22): route the authoritative OWASP Top 10 for Agentic Applications to the maintainer-egress-acquisition queue (the RB-7-four model) and cite it once acquired; not cited now.

### Verification
- Held-source located via the `grc_library_ref` catalogue and INDEX (not an assumed path) and re-verified; the offloaded pre-merge skeptical verify runs on the pushed SHA.
- `run_all_audits.sh` 72/72; pre-push guard green. Batches PR #1062's `/validate-pr` + `/retro` rows.

## 2026-07-22, Library Version 2026.07.550, PR #1062

RB-7 new-ingest reference-breadth (NY DFS financial-services cluster, findings N-1, N-2, N-3): three newly-held NY DFS / NY financial-services sources engaged in the financial-services sector annex.

### Changed
- **[`compliance/financial-services/annex-financial-services-sector-requirements.md`](../../compliance/financial-services/annex-financial-services-sector-requirements.md)** (1.0.10 to 1.0.11):
  - **N-1** (3 NYCRR Part 504): the AML/CFT Transaction-Monitoring row and the AML-gap row now cite Part 504 (504.3 reasonably-designed transaction-monitoring and OFAC-filtering program; 504.4 annual board resolution or senior-officer compliance finding by April 15).
  - **N-2** (23 NYCRR 500.19 + Part 500 deadlines): the 23 NYCRR 500 scope row adds the 500.19(a) limited-exemption thresholds (fewer than 20 employees and independent contractors, or under USD 7.5M gross annual revenue in each of the last 3 fiscal years, or under USD 15M year-end total assets); a new requirement-table row adds the annual filing (by April 15, 500.17(b)) and policy review (by April 29, 500.3) deadlines.
  - **N-3** (500.12 amended MFA): the MFA row is updated from the narrower prior scope to the amended 500.12 universal-MFA requirement (any individual accessing any information system, regardless of location, user type, or information type, effective 1 November 2025, with the 500.19(a) limited-exemption carve-out), aligning with the corpus-wide MFA-scope harmonization from #1053.
- Taxonomy and maturity-scorecard regenerated for the Version bump.

### Verification
- Held-source re-verified via offloaded research (`research-nydfs-breadth`, every value confirmed verbatim: the 20-employee / USD 7.5M / USD 15M thresholds, the April 15 and April 29 dates, the 504.4 April 15 finding, the 1 November 2025 MFA scope) and the offloaded pre-merge skeptical verify.
- `run_all_audits.sh` 72/72; pre-push guard green. Batches PR #1061's `/validate-pr` + `/retro` rows.

## 2026-07-22, Library Version 2026.07.549, PR #1061

RB-7 new-ingest reference-breadth (Latin-American privacy cluster, findings L-2 and L-3): two newly-held citation-grade legislation sources engaged in their secondary carriers.

### Changed
- **[`privacy/register-cross-border-data-flow.md`](../../privacy/register-cross-border-data-flow.md)** (1.0.6 to 1.0.7): the LGPD transfer-mechanism row now names the live instances, Resolution CD/ANPD No. 19/2024 (SCCs) and the first ANPD adequacy decision Resolution CD/ANPD No. 32/2026 (EU/EEA).
- **[`privacy/annex-privacy-jurisdiction-index.md`](../../privacy/annex-privacy-jurisdiction-index.md)** (1.0.14 to 1.0.15): the Brazil row's cross-border-mechanism cell adds "EU/EEA adequacy (Resolution 32/2026)" alongside the existing ANPD SCCs (Resolution 19/2024).
- **[`privacy/jurisdictions/annex-privacy-latin-america.md`](../../privacy/jurisdictions/annex-privacy-latin-america.md)** (1.0.4 to 1.0.5): the Colombia applicable-laws entry now cites the implementing regulation Decreto Unico Reglamentario 1074 de 2015, Capitulo 25 (international transfer and transmission rules, Seccion 5 art. 2.2.2.25.5.1; the Binding Corporate Rules / Normas Corporativas Vinculantes route art. 2.2.2.25.7), and the Colombia transfer-mechanism row adds the Binding Corporate Rules route.
- Taxonomy and maturity-scorecard regenerated for the Version bumps.

### Verification
- Held-source re-verified via offloaded research (`research-latam-breadth`, quoting the Brazil Resolution 32/2026 Article 1 and Sole Paragraph and the Colombia Decreto 1074/2015 Seccion 5 and BCR articles) and the offloaded pre-merge skeptical verify.
- `run_all_audits.sh` 72/72; pre-push guard green. Batches PR #1060's `/validate-pr` + `/retro` rows.

## 2026-07-22, Library Version 2026.07.548, PR #1060

RB-7 AI-security full-column integration (maintainer-decided full columns, not see-also): two newly-held AI-security frameworks, OWASP AI Exchange and SANS Critical AI Security Guidelines v1.4, engaged across five AI documents. Run through the high-assurance verification harness (research fan-out, then two independent adversarial verifiers, then a deterministic apply from an explicit verified map, then a re-parse).

### Changed
- **[`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md)** (1.8.10 to 1.8.11): the section-36 framework-alignment matrix gains two columns (OWASP AI Exchange, SANS CAISG v1.4), one cell per control-area row. Two cells are N/A per the adversarial verifiers: "Unsafe code generation" (both frameworks; the OWASP LLM Top 10 column already carries LLM05, and neither new framework has a generated-code-security control) and "Overreliance" SANS (SANS names no overreliance control; its Human Oversight is a decision-authority control).
- **[`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md)** (0.0.10 to 0.0.11): two framework rows (OWASP AI Exchange least model privilege; SANS Secure Agentic Systems and AI Autonomy Controls).
- **[`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md)** (1.1.3 to 1.1.4): two framework rows (OWASP AI Exchange umbrella taxonomy; SANS scope-precise categories, not the over-generic ISMS anchor the verifier rejected).
- **[`ai/guide-ai-security-technical-implementation.md`](../../ai/guide-ai-security-technical-implementation.md)** (1.3.4 to 1.3.5): an OWASP AI Exchange External-references bullet (the SANS bullet dropped as redundant per the false-positive verifier).
- **[`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md)** (1.0.8 to 1.0.9): two framework rows (SANS Incident Response and Forensics for AI Systems as the primary AI-IR anchor; OWASP AI Exchange Monitor use as a secondary).
- Taxonomy and maturity-scorecard regenerated for the Version bumps.

### Verification (high-assurance harness)
- Stage 1 research fan-out (`research-ha-aisec-mappings`, quoted every candidate at held source). Stage 3 two independent adversarial verifiers, blind to each other and to the research rationale: false-negative (`ha-aisec-verify-fn`, hunt misses) returned NO MATERIAL MISS with every N/A grounded (and caught a SANS "overreliance" homonym false-lead); false-positive (`ha-aisec-verify-fp`, hunt over-assignments) returned three OVER-ASSIGNED (all among the candidate's own flagged cells) plus one borderline, which drove the two N/A cells, the Table-3 anchor replacement, and the dropped Doc-4 SANS bullet. Stage 5 deterministic apply from the reconciled explicit map, then a re-parse cross-checking every applied cell against the map.
- The new columns use control NAMES (OWASP AI Exchange, SANS CAISG have no short codes), so the existence-gate families (CSA/NIST/ISO/COBIT) and the `/matrix-fit` worklist tool do not apply; the two adversarial verifiers performed the semantic-fit role instead.
- `run_all_audits.sh` 72/72 (lint-language OK); pre-push guard green; an offloaded pre-merge skeptical verify on the pushed SHA.
- Batches PR #1059's `/validate-pr` + `/retro` rows.

## 2026-07-22, Library Version 2026.07.547, PR #1059

RB-7 new-ingest reference-breadth (Canada cluster, findings C-1 and C-2): two newly-held Canadian government sources engaged as authoritative companion references. Offloaded research (`research-canada-breadth`) caught and corrected the original reference-audit's C-1 overstatement: the GC Guideline does NOT publish a Critical/High/Medium remediation-hours matrix (its timed table is scanning frequencies; remediation timing is qualitative), so the addition is grounded in the guideline's verified risk-based framing, not the "48h/14d/30d" figures the original finding claimed.

### Changed
- **[`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md)** (1.3.6 to 1.3.7): a companion-reference note in the Framework-alignment section citing the Government of Canada TBS Guideline on Vulnerability Management, grounded in its verified text (VM-program scope; "timelines for vulnerability remediation should be defined based on risk"; risk acceptance "must include an expiry date that is less than 12 months from when it is issued"), as a risk-based structural parallel, not a numeric SLA equivalence.
- **[`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md)** (1.4.6 to 1.4.7): a companion-reference note citing CCCS ITSP.50.103 as an injury-based security-categorization methodology ("applies to both private and public-sector organizations") bridging this standard's classification to cloud control-profile selection.
- Taxonomy and maturity-scorecard regenerated for the Version bumps.

### Verification
- Held-source re-verified via offloaded research (`research-canada-breadth`, which corrected C-1) and the offloaded pre-push skeptical verifier: the GC VM Guideline quotes at their cited lines and the ITSP.50.103 private-and-public applicability, injury-based categorization definition, and control-profile-selection basis.
- `run_all_audits.sh` 72/72; pre-push guard green.
- Batches PR #1058's `/validate-pr` + `/retro` rows per recursion-avoidance.

## 2026-07-22, Library Version 2026.07.546, PR #1058

Citation-accuracy fix from the RB-7 new-ingest reference-audit (Google SAIF existing-citation verification, OVERREACH verdict): two developer-security README reference entries described SAIF's coverage as including an "execution" lifecycle stage, which the now-held SAIF source does not support.

### Changed
- **[`dev-security/README.md`](../../dev-security/README.md)** (1.4.5 to 1.4.6): the Google SAIF reference line dropped "execution" from "secure development, deployment, execution, and monitoring".
- **[`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md)** (pack 1.62.3 to 1.62.4, a patch with no new rule or skill): the SAIF Coverage line dropped "execution"; a Version-history row records the patch.

### Verification
- Re-verified at the held source (the six Google SAIF full-text files in the reference base at ref `3e63317`): SAIF describes "six core elements" across a software-development lifecycle (development, deployment, monitoring); "execute" and "execution" appear only for agent actions and attacks (prompt injection, remote code execution), never as a SAIF lifecycle stage. The sibling reference line in the AI-coding-assistant guideline (which already read "development, deployment, and monitoring") was already accurate and is unchanged; the TikiTribe-coverage SAIF mentions are third-party-scoped and unchanged.
- Corpus-wide grep confirmed exactly two carriers of the overreach phrase, both fixed; no generated-artefact regen was needed (the README Version is not taxonomy-tracked); `run_all_audits.sh` 72/72; a refute-briefed skeptical verifier ran pre-push.

## 2026-07-22, Library Version 2026.07.545, PR #1057

Corpus accuracy fix from the RB-7 new-ingest reference-audit (finding L-1): the Brazil privacy annex stated the ANPD had not yet issued adequacy decisions, which the newly-held Resolution CD/ANPD No. 32 of 26 January 2026 (the ANPD's first adequacy decision, recognizing the European Union) disproves.

### Changed
- **[`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md)** (1.1.6 to 1.1.7): the Cross-border transfer-mechanisms Adequacy item replaced "As of 2025, the ANPD has not yet issued adequacy decisions" with the ANPD's first adequacy decision (Resolution CD/ANPD No. 32 of 26 January 2026, recognizing the EU: all EU Member States, the three EFTA states in the EEA, and EU institutions; subject to reassessment within four years); the standard-contractual-clauses paragraph reworded so SCCs remain primary for destinations not covered by an adequacy decision, with the new adequacy route as the alternative for the EU and EFTA/EEA.
- The taxonomy, portal, and maturity-scorecard artefacts were regenerated for the Version bump.

### Verification
- Re-verified at the held source (the Brazil ANPD Resolution No. 32 of 26 January 2026 full-text in the reference base at ref `3e63317`): Article 1 recognizes the EU as providing an adequate level of protection under the LGPD; the Sole Paragraph extends it to the EU Member States, the EFTA/EEA states (Iceland, Liechtenstein, Norway), and EU institutions; Paragraph 1 sets a four-year reassessment. The item is catalogued in the reference base.
- `run_all_audits.sh` 72/72 standalone; both generator `--check` runs in sync; the pre-push guard green; a refute-briefed skeptical verifier ran pre-push.

## 2026-07-22, Library Version 2026.07.544, PR #1056

Resume close-out for the 2026-07-22 session (the orchestrator's prior session ingested +31 reference items into `grc_library_ref`, catalogue 696 to 727; this session assesses corpus use/cite of them per TODO RB-7). This is the first PR of the resumed session: it runs the loop-break Sweep 116 corpus-wide `/validate`, clears the one aged-follow-up gate artefact, prunes the handoff, and re-acquires the lease.

### Changed
- **[`session-state.md`](../session-state.md)**: lease ACQUIRED for this session (`Status: active`, `Active-session: claude/resume-sweep116-closeout`, fresh heartbeat) after the `/resume` step-0 interlock confirmed the prior lease released and no live sibling session.
- **[`validate-sweeps/history.md`](../validate-sweeps/history.md)**: added the Sweep 116 row (Version 2.0.117); **re-triaged** the aged Sweep-3 follow-up at L133 (added `re-triaged: 2026-07-22` and an explicit `re-triage-by: 2026-08-21`; the default 30-day clock lapsed 2026-07-20 during the multi-day gap, failing gate 43 and the FollowupAgeing regression test), restoring the mechanical baseline to 72 of 72. Kept open as a future-gate candidate, not resolved.
- **[`session-handoff.md`](../session-handoff.md)**: advanced the Resume cursor to Sweep 116; pruned per keep-current-plus-one-prior (removed the 2-prior 2026-07-18b asserted-expectations block, whose substance is durable in the Sweep 113 history row and the CHANGELOG).
- **degradation-watch-log**: a `session-start` row appended in the private companion repo (the `/resume` step 0.4 evidence trail).

### Verification
- Loop-break Sweep 116 `/validate` (OFFLOADED to worker-20260716-b, blocking prio-0, pinned `501d77a2` / ref `3e63317`): **CLEAN PASS, 0 error / 0 warning / 0 note / 0 novel**. The #1054..#1055 delta is `.working`, `.claude`, CHANGELOG, README, and TODO only (no corpus-domain document); the CHANGELOG daily-tier condensation was verified faithful; all #1040-#1042 asserted-clean surfaces corroborated, 0 contradicted. Consumed under elevated QA (worker-b delivery 1 this session; the orchestrator's independent baseline re-derivation matched 70 of 72, same L133 root cause, restored to 72 of 72 by the re-triage).
- Post-commit `run_all_audits.sh` 72 of 72 standalone; the pre-push guard green at push. This PR's own `/validate-pr` and `/retro` batch into the next PR per recursion-avoidance.

## 2026-07-19, Library Version 2026.07.543, PR #1055

Condenses the 2026-07-19 root CHANGELOG entries (PRs #1039-#1054) into one daily summary and prunes the matching detailed-mirror entries, completing the daily-tier condensation for the day during the multi-day session gap. Also records TODO RB-7 (retrieve and ingest four not-held AI-security frameworks the aidefensematrix.com gap analysis surfaced, routed to maintainer-acquisition) and closes the 2026-07-19b/c session, releasing the concurrency lease.

### Changed
- **Root CHANGELOG**: the 16 per-PR 2026-07-19 entries (#1039-#1054) replaced by one `**2026-07-19 (PRs #1039-#1054)**` daily summary, per the §1.22.5 daily-tier model; #1055 (this PR) stays per-PR as the current entry.
- **Detailed mirror**: the matching #1039-#1054 structured entries pruned (git history preserves the full detail); gate 59's parity cutoff floors above them.
- **TODO RB-7**: records the aidefensematrix.com gap-analysis outcome (worker-offloaded, then orchestrator-`_ref`-index-verified with [`ref-holds.py`](../../tools/ref-holds.py)): four not-held AI-security frameworks (OWASP AI Exchange, SANS CAISG v1.4, Google SAIF, Cyber Defense Matrix) routed to maintainer-acquisition, then a corpus use/cite assessment; the matrix itself is NOT acquired (maintainer decision: a derivative CSF-2.0-by-asset-class mapping the project can re-create); OWASP Agentic Top 10 and NIST IR 8596 are HELD-but-uncited breadth items, not acquisitions.
- **The private maintainer-egress-requests queue** (v1.0.3): the four not-held frameworks added as a maintainer-acquisition block (drop-destination `grc_library_ref/ingest/`) for the Wednesday 2026-07-22 resume.
- **Session close**: [`session-state.md`](../session-state.md) lease RELEASED (`Status: released`, `Active-session: none`); [`session-handoff.md`](../session-handoff.md) and [`next-prs.txt`](../next-prs.txt) refreshed with the continuation note and the RB-7 ingest step; the [`validate-pr/history.md`](../validate-pr/history.md) row records the handoff-PR exemption.

### Verification
- Gate 59 (mirror-header-parity) re-run clean after the prune; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green at push. **Session-closing PR:** per the loop-break rule this PR skips its own trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume` corpus-wide `/validate`, and this session additionally ran Sweep 115 pre-close (0 error / 0 warning over #1044..#1053). The concurrency lease is RELEASED here.

