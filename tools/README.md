# Repository tooling

The Corpus-Management compiler (`build-corpus-management.py`) generates two full always-loaded
prose rules, a compact rule index in the corpus-management skill directory (read when the skill
loads, on the skill's instruction, not at session start), and on-demand bodies outside
`.claude/rules/`; see
[pack tooling](../.corpus-management/tools/README.md) for the generation and validation contract.

This directory contains repository quality tooling. The scripts are intentionally minimal: they run with the standard Python 3 interpreter, take no third-party dependencies, and are designed to be invoked locally, by pre-commit, or by CI.

## Scripts

The library's audit programme is a set of linters, build-and-check generators, and the linter regression test suite. The canonical inventory of every gate, with its name, script, category, and the current gate count, is maintained in [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6. Gate 35 (gate-name parity audit) enforces that the §6 inventory, the CI workflow, the local runner, and the pre-commit config declare identical gates with identical names and scripts, and that the three execution surfaces (workflow, runner, pre-commit) invoke each gate with identical flags, and that each section 6 gate number appears exactly once in the section 5 category lists and that those lists name no number the inventory lacks; the inventory is the single source of truth.

To see the current gate set in one place, run [`tools/run_all_audits.sh`](run_all_audits.sh) or read the §6 table.

Each individual linter is self-documenting via its module docstring (`python3 tools/<script>.py --help` where supported, or read the docstring directly). The shared helper module is [`tools/lint_common.py`](lint_common.py); the regression test suite (gate 36) is at [`tools/run-linter-regression.py`](run-linter-regression.py), which discovers every top-level `tests/test_*.py` file (sorted by module name), prints the module list it runs, and runs all of the modules in one `unittest` invocation. It refuses (exit 2, naming the offender) each of the following, never softening one to green (this list matches [`tests/README.md`](../tests/README.md), and a regression test holds the two surfaces together):

- a run list that does not match an independent `os.walk` enumeration of `tests/` (checked once in the parent and again by the child driver against its own argv, so a filter on either side cannot drop a module);
- a test file nested in a `tests/` subdirectory, a `test_*/` package directory, a symlinked subdirectory, or a subdirectory the walk cannot inspect (all of which could hide test files);
- finding no `tests/test_*.py` files at all;
- a module that cannot be imported (any `BaseException`, so an import-time `SystemExit(0)` cannot pass as green);
- a module that contributes zero test cases;
- a module with no credited start, on a run unittest reports green, refused as `tests/X.py: N loaded, 0 credited starts`; this per-module rule is separate from the sentinel's `notStarted` count below. A credited start is a test from this module's loaded suite that reached `startTest` outside a skip-decorated class: a started test is credited to the handed module whose suite, as `unittest.main` loads it (one suite per module, in argv order), contains it, whatever the test's type; the gate checks that each module's suite starts something, not who wrote the test's code. A test that a `SkipTest` raised in `setUpModule` or `setUpClass` kept from `startTest` is not a credited start, and neither is a test whose class is skipped by a class decorator (`unittest.skip`, or `skipIf`/`skipUnless` whose condition skips), although unittest calls `startTest` for that test before it reads the class flag. The refusal states the loaded count and that no start was credited, not a cause. A run unittest reports as failed (including an error, not a skip, raised by `setUpModule` or `setUpClass`) is not turned into this refusal and keeps unittest's failure report and exit 1. Accepted residuals: a module that only imports and loads another module's `TestCase` classes earns credit for their started tests (borrowing; no current module does this; the gate checks that each module's suite starts something, not who wrote it); a test skipped individually (a skip decorator on the test method, or `self.skipTest` inside the test or its `setUp`) is a credited start, so a module whose every test is skipped individually is not refused; the pairing check compares case counts per suite, not case identity, so a second load that returns different cases in the same number passes it, and its cases are credited as `unittest.main` loaded them; a start is matched to the next pending occurrence in unittest's run order, so a test that itself starts another loaded case object (outside the suite's own iteration) can move the match (test code controlling the run is the in-process residual below); a suite that reorders, drops or substitutes cases, in its own `run` or its `__iter__`, and a test object that is not a suite but runs inner cases, are outside what the gate can account for, because crediting and the `setUpClass` skip reconciliation both assume a suite runs its cases in its flattened order (observed effects: a module whose reordering suite holds a `setUpClass`-skipped class can be falsely refused, and a dropping suite can produce a false pass without a shared case object; no current module uses such a suite or test object); and test code can forge the result in-process (the `__main__.nonce` residual below);
- a load whose started tests cannot be paired with the handed modules: `unittest.main` must load exactly one suite per handed module, each with the case count the driver's own load found for that module (a `load_tests` that returns a different case count on a second load fails this; one that returns different cases in the same number does not, see the residuals above), so started tests are never credited by guesswork; the refusal names the mismatch;
- a test case object in the loaded suites of more than one module (for example a helper's module-level case loaded by two modules), refused before the run, naming the modules: its starts cannot be credited to one module;
- a green child exit whose output lacks unittest's own `Ran N tests` line with N at least 1; and
- a green child exit whose LAST stderr line is not the child driver's completion sentinel, carrying the per-run nonce the parent delivered over the child's stdin (never on argv or in the environment, and consumed before any test module is imported), `testsRun`, `notStarted` (loaded tests a `SkipTest` raised in `setUpClass` kept from starting, counted from the loaded suite: unittest runs `setUpClass` once per run of consecutive cases of the same class object, so each such run of never-started occurrences since the previous matched start takes one skip record of its class arrived in that stretch and counts each of its occurrences once, two classes sharing a module and qualname are two runs, and one skip record never covers two runs; one run contributes at most one counted record: a class cleanup's `SkipTest` after a skipped `setUpClass` is recorded under the same `setUpClass` name, and such further records of one run, told apart from a later run's by arriving back to back (no start and no other skip record in between) with the same holder and the same `_previousTestClass` on the result, are discarded, not credited to a later run; the grouping of records into runs depends on unittest's private `_previousTestClass` attribute and its set-up order (set to a run's class only after that class's set-up; read in CPython 3.14 and 3.11 `suite.py`), which unittest does not document, so a change there could misgroup records (an accepted residual); when the result object has no `_previousTestClass` attribute at all as a `setUpClass` skip record arrives, the run is refused (exit 2, naming `_previousTestClass` and the Python version), never grouped by a default (`None`, its value before the first test, is an answer); so a green run with such a skip in a module that otherwise started a test is not refused; it does not count tests of a skip-decorated class, which reach `startTest`, nor tests a `SkipTest` in `setUpModule` kept from starting, which therefore fail this reconciliation), the per-module test counts and `wasSuccessful=True`.

Passing output: stdout carries the module list (`Running test modules:` and one indented module name per line), printed before the run; stderr carries unittest's own output unchanged, followed by the completion sentinel as its one extra, last line. A regression test in [`tests/test_regression_gate.py`](../tests/test_regression_gate.py) pins this shape against a direct `python3 -m unittest` run.

What the nonce and sentinel defend against: accidental early exits (a premature `SystemExit` before the sentinel), grandchild or stray output standing in for the summary or the sentinel, dropped modules, and zero-test modules (a module hollowed to zero tests). What they do NOT defend against: test code in the child process that deliberately reads the driver's state. The driver is a `python -c` script, so the nonce is a module-level global of `__main__`; one line of test code (`import __main__`) recovers it and can forge a complete sentinel. This is a documented accepted residual, pinned by a test in [`tests/test_regression_gate.py`](../tests/test_regression_gate.py), so a change that closes the channel must update that test and this paragraph together. They also do not defend against a partially hollowed module (a `load_tests` that returns some but not all of a module's tests), because the loaded suite is the gate's only ground truth. No in-process scheme is proof against deliberately adversarial in-process code.

The linter fixtures live in [`tests/test_linters.py`](../tests/test_linters.py). [`tools/external_overlay.py`](external_overlay.py) declares the third-party skill directories shared by the external-overlay licence and ungated-surface dash audits.

## Running

Run the full audit programme from the repository root:

```
bash tools/run_all_audits.sh
```

This runs every gate in the order defined in [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6 and aggregates results. Use `FAIL_FAST=1 bash tools/run_all_audits.sh` to stop on first failure.

Individual scripts also run standalone:

```
python3 tools/lint-metadata.py
python3 tools/lint-language.py ai security    # restrict scope to specific paths
python3 tools/build-taxonomy.py --check        # regen-and-check
```

Each script prints `OK: ...` on a clean run and exits zero. On findings it prints a grouped report and exits one (or two for environmental failure, e.g., a missing register).

To regenerate the auto-generated artefacts after editing document metadata or document structure, run without `--check`:

```
python3 tools/build-taxonomy.py
python3 tools/build-narrative-registry.py
python3 tools/build-portal.py
```

The narrative registry derives independently from `executive/` page metadata. The portal
generator depends on the taxonomy; always regenerate the taxonomy first.

Further generated artefacts derive from their own source files rather than from
document metadata and document structure, and are regenerated when that source
changes:

```
python3 tools/build-relationship-model.py       # from governance/relationship-model-source.json
python3 tools/build-todo-number-allocation.py   # from tools/todo-number-floor.json + the live TODO ids
python3 tools/build-citation-publishers.py      # section 7.1 table from its json citation-publishers block
```

## Pre-commit integration

[`.pre-commit-config.yaml`](../.pre-commit-config.yaml) at the repository root wires every gate as a local hook. Install once:

```
pip install pre-commit
pre-commit install
```

Three git-native hooks are installed by `tools/install-git-hooks.sh`: a pre-push hook (`tools/git-hooks/pre-push`), a pre-commit hook (`tools/git-hooks/pre-commit`) that refuses a commit on a `main` or `master` checkout, a commit that changes a document's `**Version:**` or `**Date:**` line (or a generated output) while the staged `taxonomy.yml`, `docs/portal.md` or `docs/maturity-scorecard.md` is out of sync (`tools/check-generated-commit.py` runs the staged generators' `--check` on a copy of the index being committed; override `GRC_ALLOW_STALE_GENERATED_COMMIT=1`), and a commit that stages `CHANGELOG.md` while `python3 tools/preflight-changelog.py --staged` fails (override `GRC_ALLOW_FAILING_CHANGELOG_COMMIT=1`), and a commit-msg hook (`tools/git-hooks/commit-msg`) that refuses a commit whose staged versioned document changed its body without a Version change (a `VersionBump: none <reason>` message line opts out README.md only). A local commit-msg hook is kept by renaming it to `commit-msg-local`; the managed hook runs it first. Run it once per clone, BEFORE `pre-commit install`: the framework then chains the managed pre-commit hook as `pre-commit.legacy`. If the framework is already installed, run `pre-commit uninstall`, then this installer, then `pre-commit install`. A later re-run of the installer cannot verify the chain from file contents, so it reports the pre-commit half as unverified (non-zero) and names the behavioural check: on a `main` checkout, `git commit --allow-empty -m probe` must be refused. It refuses a `git push` when the tracked working tree is modified or staged AND the push includes the current HEAD, mirroring [`pre-push-guard.sh`](pre-push-guard.sh)'s dirty-tree attestation (override `PRE_PUSH_GUARD_ALLOW_DIRTY=1`), as a backstop on every destination; the full guard below clears this override. It is a raw git hook, not a pre-commit-framework hook, because the framework stashes unstaged edits before running hooks (which would defeat the check).

Subsequent commits run the full audit programme before the commit is finalized. Run on demand against the entire corpus:

```
pre-commit run --all-files
```

## Continuous integration

[`.github/workflows/quality.yml`](../.github/workflows/quality.yml) runs the same gate set on every push to `main` and on every pull request. The CI environment uses Python 3.11 from `actions/setup-python`. No third-party dependencies are installed.

## Exemptions

- Draggable AI-context rule files under `guardrails/` are exempt from the metadata and structural audits because they serve a different purpose (loaded into AI coding sessions, not consumed as governance documents).
- Tooling docs in this directory and adopter docs in `docs/` are exempt from the structural audit.
- The superseded [`privacy/annex-regional-privacy-requirements.md`](../privacy/annex-regional-privacy-requirements.md) is exempt from the structural audit (retained for history; superseded by [`privacy/annex-privacy-jurisdiction-index.md`](../privacy/annex-privacy-jurisdiction-index.md) and the jurisdiction subfolder).

## Exploratory tools (not gates)

Some scripts in this directory are exploratory tools the maintainer runs on demand rather than verification gates wired into the audit programme. They exit 0 on every run (they surface findings; they do not fail). The set:

- [`tools/detect-collection-candidates.py`](detect-collection-candidates.py): heuristic detector for new candidate collections that should be added to gate 41 (Collection-enumeration consistency audit). Walks candidate-source roots, scores each subdirectory's items against corpus markdown files for coverage, and surfaces candidates with rationale for the maintainer to triage one-by-one. Companion to gate 41's hard-coded configuration.

The pre-push hook runs the full guard on every branch update to a destination
whose normalized path ends in `jposluns/grc_library`, on any host or remote name.
HTTPS, SSH, scp-like and local URLs are matched case-insensitively, ignoring a
trailing slash and `.git` (including a `/.git` component). After installation,
use plain `git push`.
Every non-deletion `refs/heads/*` destination must carry a commit equal to the
active checkout's HEAD; otherwise push from a checkout at that commit. Tags and
other namespaces do not run the full guard, including tags pointing to commits.
Deletion-only pushes and other repositories skip it. The dirty-tree backstop
still receives every original ref record.

`tools/install-git-hooks.sh --check` compares the shared pre-push shim byte for
byte and rejects any `core.hooksPath` setting; without a private store it skips.
Install once per clone; linked worktrees share the persistent shim, which resolves
the active checkout. Older hooks are refused for guarded destinations (including
tags and deletions), with a message to rebase; other destinations run the older
tracked hook, or succeed if that hook is absent. An existing v1, v2, v3, v4 or v5 shim
is deliberately treated as foreign:
inspect and remove that old managed
pre-push shim, then rerun the installer. Foreign hooks are never overwritten.

Direct `tools/pre-push-guard.sh` runs remain available and retain pipe refusal.
Every guarded push reruns all checks, even after a direct pass or transport
failure. Output streams through a regular temporary file with the guard's exit
status preserved. The guard environment allows only `LANG`, `LC_*`,
`TMPDIR`, `TERM`, `GRC_STORE`, `SSH_AUTH_SOCK` and the lowercase and uppercase
`http_proxy`, `https_proxy`, `ftp_proxy`, `all_proxy` and `no_proxy` variables.
`GRC_STORE` is a deliberate caller-controlled store selection. Askpass settings
and global Git credential helpers, URL rewrites and SSH command settings are
not preserved. Helpers outside the fixed PATH are unavailable; a failed fetch
prints a warning that delta gates may use a stale local base.
Both hook entry points fix `PATH` to `/usr/bin:/bin` and unset shell startup,
loader and Git executable-path variables before invoking commands. They verify
that the selected toplevel is a registered work tree of the current repository
before running its tracked hook. Symlinked `.git` entries are refused; canonical
paths, not inode aliases, bind ordinary and linked checkouts. Relative linked
worktree backlinks resolve from the Git directory. Separate Git directories
outside the conventional parent-owned `.git` location are accepted only when the
checkout gitfile names that directory and `core.worktree` is set to that checkout
(relative values resolve from the Git directory). An unset `core.worktree` is
refused with the command that sets it. The hooks read `core.worktree` only from
the Git directory's own `config` file, so `-c` and `GIT_CONFIG_COUNT` overrides
cannot change it.
Hook Python entry points run with `-I`. The
guard resets `HOME` to the account home from the password database, drops caller
`PYTHON*` variables and sets `PYTHONNOUSERSITE=1` for child interpreters. It sets
`GIT_CONFIG_GLOBAL=/dev/null`, retaining repository and administrator system
config, including system `safe.directory` entries. Caller `GIT_CONFIG_SYSTEM`
and `GIT_CONFIG_NOSYSTEM` settings are dropped. Other Git settings and
direct-run overrides are excluded, including in linked worktrees. These overrides do
not exempt guarded pushes. After the guard passes, HEAD must still match every
pushed branch SHA and the tracked tree must still be clean.

Residual: `git push --no-verify` and a command-level `core.hooksPath` override
can skip the hook entirely, including overrides supplied through
`GIT_CONFIG_COUNT` or `GIT_CONFIG_PARAMETERS`. A `core.hooksPath` selected before
the hook runs through `HOME`, `GIT_CONFIG_GLOBAL`, `XDG_CONFIG_HOME` or
`GIT_CONFIG_SYSTEM` is also a residual handled by the governance pack's guard.
The hook cannot undo loader code already executed when Git or its initial shell
starts. `git push -n` is a dry run and still runs the hook. Local hooks are not a
server-side boundary.

## Operator tools (not gates)

[tools/ci-status.sh](ci-status.sh) wraps [tools/ci-status.py](ci-status.py), a point-in-time Actions workflow reader, not a merge gate. It uses authenticated gh calls to read a PR head or an explicit SHA and one Actions runs page. In PR mode, the case-insensitive REQUIRED_RUNS lookup (after normalizing a trailing .git and rejecting a trailing .) requires Repository quality checks and PR attribution for jposluns/grc_library, each from its configured path on a pull_request event. Unlisted repositories and SHA mode have no required set. Missing required runs are pending unless failure or uncertainty requires not-green. The reader validates metadata before selecting the highest run_number per (path, event); malformed fields, duplicate IDs or workflow run numbers across events, and retries of older runs fail closed. Every JSON response, including the PR-head reads, rejects duplicate members. The conclusion field must be present, with null allowed only for non-completed runs. It does not infer cross-run retry chronology from timestamps or attempt numbers. A retried older run keeps that head NOT-GREEN while it is listed, even when it and the newest run succeeded; only a new push with a new head clears it. Superseded first-attempt runs remain visible with markers; incomplete pages retain diagnostic markers but never pass. PR mode re-reads the head and rejects movement. Exit codes: 0 green, 1 not-green, 2 usage/gh/JSON or unusable-head error, 3 pending. The pure --self-test is wired into the linter suite. GREEN describes only interpretable returned workflow evidence: it does not verify jobs, other apps' checks, commit statuses, PR association, or server freshness. The merge-time decision remains merge-when-green.py's.
