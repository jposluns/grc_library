# Linter regression tests

This directory contains regression tests for the audit-programme linters
in [`tools/`](../tools/). Each test:

1. Constructs a minimal synthetic fixture appropriate to each linter's target surface (Markdown for the corpus linters, Python source for the gate-94/95 code linters) that should trigger
   exactly one linter rule.
2. Invokes the target linter against the fixture.
3. Asserts that the linter exits non-zero and emits a finding
   matching the expected pattern.

The tests exist to catch a class of defect that no other gate in the
audit programme can catch: a regression in a linter's own detection
logic. If a future refactor accidentally weakens a regex or breaks an
exemption list, the corpus may still happen to be clean (no false
positives), but the linter no longer detects the violation class it
exists to detect. The regression tests catch this.

## Scope

The default test shape is a **positive test**: a fixture containing
exactly one violation, asserting the linter exits non-zero and emits
the expected finding. The suite also includes **negative tests**
(fixtures whose content is permissible in context and must not be
flagged, such as a template placeholder inside a template file, or a
placeholder string inside a fenced code block), and **environmental
tests** (a linter that depends on an external register must exit 2,
not 1, when the register is missing). The audit programme itself
provides additional implicit negative coverage by running every
linter against the clean corpus on every commit and expecting exit 0.

## External overlay skill bytes

`ExternalOverlayLicenseTests` writes raw byte fixtures for all five registered
skills. The gate rejects CR (including CRLF), invalid UTF-8, NUL and the reserved
interpolation sentinels U+FFFE/U+FFFF before scanning the body. The restricted
frontmatter rule also rejects an initial UTF-8 BOM; embedded U+FEFF retains its
JavaScript whitespace meaning. A newline mutation moves tokens from metadata
into the runtime body and must produce a finding.

The optional [installed-parser probe](probe_overlay_parser.py) runs with
`python3 tests/probe_overlay_parser.py`. On 2026-10-02 it executed the extracted
`jw`, `jk` and `Ms` body-boundary statements from `/usr/bin/claude` 2.1.287 under
Node v22.22.1, plus the complete `jTe` function with empty arguments. It does not
execute YAML metadata parsing. CR-only and mixed headers left the header tokens
in the body; CRLF still recognized frontmatter. `jTe` rewrote U+FFFE/U+FFFF.
The probe prints the binary SHA-256 and the result for each byte fixture.

## Running

The complete regression command (audit-programme gate 36) is:

```
python3 tools/run-linter-regression.py
```

It discovers and runs every top-level `tests/test_*.py` module in one
`unittest` invocation. It refuses (exit 2, naming the offender) each
of the following, never softening one to green:

- a run list that does not match an independent `os.walk` enumeration
  of `tests/` (checked once in the parent and again by the child
  driver against its own argv, so a filter on either side cannot drop
  a module);
- a test file nested in a `tests/` subdirectory, a `test_*/`
  package directory, a symlinked subdirectory, or a subdirectory the
  walk cannot inspect (all of which could hide test files);
- finding no `tests/test_*.py` files at all;
- a module that cannot be imported (any `BaseException`, so an
  import-time `SystemExit(0)` cannot pass as green);
- a module that contributes zero test cases;
- a module with no credited start, on a run unittest reports green,
  refused as `tests/X.py: N loaded, 0 credited starts`. This
  per-module rule is separate from the sentinel's `notStarted` count
  below. A credited start is a test from this module's loaded suite
  that reached `startTest` outside a skip-decorated class: a started
  test is credited to the handed module whose suite, as
  `unittest.main` loads it (one suite per module, in argv order),
  contains it, whatever the test's type. The gate checks that each
  module's suite starts something, not who wrote the test's code.
  A test that a `SkipTest`
  raised in `setUpModule` or `setUpClass` kept from `startTest` is not
  a credited start, and neither is a test whose class is skipped by a
  class decorator (`unittest.skip`, or `skipIf`/`skipUnless` whose
  condition skips), although unittest calls `startTest` for that test
  before it reads the class flag. So a module whose every loaded test
  is skipped at class level, by either means, is refused. The refusal
  states the loaded count and that no start was credited, not a
  cause. A run unittest reports as failed (including an error, not a
  skip, raised by `setUpModule` or `setUpClass`) is not turned into
  this refusal: it keeps unittest's failure report and exit 1.
  Accepted residuals: a module that only imports and loads another
  module's `TestCase` classes earns credit for their started tests
  (borrowing; no current module does this; the gate checks that each
  module's suite starts something, not who wrote it); a test skipped
  individually (a skip decorator on the test method, or
  `self.skipTest`) is a credited start, so a module whose every test
  is skipped individually is not refused; a `TestSuite` subclass that
  reorders, drops or substitutes cases in its own `run` is outside
  what the gate can account for, because crediting and the
  `setUpClass` skip reconciliation both assume a suite runs its cases
  in its flattened order (two observed effects: a module whose
  reordering suite holds a `setUpClass`-skipped class can be falsely
  refused, and a false pass needed a case object shared by two
  modules, which the shared-case refusal below now refuses; no current
  module uses such a suite); and test code can forge the result
  in-process (the `__main__.nonce` residual below);
- a load whose started tests cannot be paired with the handed
  modules: `unittest.main` must load exactly one suite per handed
  module, each with the case count the driver's own load found for
  that module (a `load_tests` that returns a different suite on a
  second load fails this), so started tests are never credited by
  guesswork; the refusal names the mismatch;
- a test case object in the loaded suites of more than one module
  (for example a helper's module-level case loaded by two modules),
  refused before the run, naming the modules: its starts cannot be
  credited to one module;
- a green child exit whose output lacks unittest's own `Ran N tests`
  line with N at least 1; and
- a green child exit whose LAST stderr line is not the child driver's
  completion sentinel: a per-run nonce from the parent plus
  `testsRun`, `notStarted` (loaded tests a `SkipTest` raised in
  `setUpClass` kept from starting, counted from the loaded suite, so a
  green run with such a skip in a module that otherwise started a
  test is not refused; it does not count tests of a skip-decorated
  class, which reach `startTest`, nor tests a `SkipTest` in
  `setUpModule` kept from starting, which therefore fail this
  reconciliation), the per-module test counts (naming exactly the
  handed modules, each at least 1, with `testsRun` plus `notStarted`
  summing to their total and `testsRun` at least 1) and
  `wasSuccessful=True`. Completion is established from the executed
  suite's own result, so a premature `SystemExit` from `load_tests`,
  `setUpClass` or `setUpModule`, or a stray summary line written by a
  grandchild that inherits stderr, is refused.

The nonce travels over the child's stdin (the parent writes it to a
pipe; the driver consumes it and rebinds its stdin to `/dev/null`,
closing the pipe, before importing any test module), never on argv and
never in the environment, so it never appears in `sys.argv`,
`os.environ` or `/proc/<pid>/cmdline`. What the nonce and sentinel
defend against: accidental early exits (a premature `SystemExit`
before the sentinel), grandchild or stray output standing in for the
summary or the sentinel, dropped modules, and zero-test modules (a
module hollowed to zero tests). What they do NOT defend against: test
code in the child process that deliberately reads the driver's state.
The driver is a `python -c` script, so the nonce is a module-level
global of `__main__`; one line of test code (`import __main__`)
recovers it and can forge a complete sentinel. This is a documented
accepted residual, pinned by
`test_main_accepts_main_nonce_forgery_residual` in
`tests/test_regression_gate.py`, so a change that closes the channel
must update that test and this paragraph together. They also do not
defend against a partially hollowed module (a `load_tests` that
returns some but not all of a module's tests), because the loaded
suite is the gate's only ground truth. Such code can equally
monkeypatch `unittest` or the driver's globals; no in-process scheme
is proof against deliberately adversarial in-process code.

A single module can still be run directly, for example:

```
python3 -m unittest tests.test_linters -v
```

but this direct command has a narrower scope: it runs only that one
module and misses the other `tests/test_*.py` modules the gate runs
(session facts, standards currency, release delta and the
regression-gate guards).

The whole audit programme runs with:

```
tools/run_all_audits.sh
```

The regression suite runs as gate 36 of the audit programme. See
[`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6.

## Fixture isolation

Most tests create a fixture in a per-test temporary directory under
`tests/tmp/` (created on demand) and pass explicit file paths to
the linter under test, so the linter does not scan the rest of the
repository during the test. Default-scope coverage fixtures instead build
a synthetic repository-shaped tree in a temporary directory, point the
linter's module root at it, and call the linter's collector or `main` in
process, to prove a path is reached in DEFAULT mode (not merely when an
explicit path bypasses default target selection). Either way the temporary
tree is removed after the test.

Isolation is provided by two complementary mechanisms:

1. **Per-test cleanup**: every fixture is owned and cleaned by the test
   that created it. `make_fixture` writes into a unique per-instance
   `mkdtemp` directory under `tests/tmp/` and registers its removal with
   `addCleanup`, and the other fixture helpers use `mkdtemp` the same
   way. The module-level `setUpModule` in `tests/test_linters.py` only
   creates `tests/tmp/`; neither it nor any module-level teardown
   deletes anything, because a sweep could only ever delete fixtures a
   concurrently running instance owns (one run already overlaps itself:
   `DirectRunTests` launches the module as a child process).
   `ModuleFixtureOwnershipTests` pins this ownership contract.
2. **`.gitignore`**: `tests/tmp/` is gitignored so a leftover
   fixture from a crashed test never enters version control.

Where fixtures actually live: `make_fixture` and most other helpers
allocate a unique per-instance `mkdtemp` directory under `tests/tmp/`,
and `_fixture_base` (for trees that hold permission-stripped entries)
allocates one outside the repository, in the system temporary
directory, which no gate walks. So `tests/tmp/` holds only uniquely
named per-run directories, plus one remaining fixed-name
positive-control file (`NarrativeScanScopeTests`, removed by its own
test's `finally`).

Linters themselves do NOT exempt `tests/tmp/` (it is not in
`tools/lint_common.py`'s `DEFAULT_EXEMPT_DIRS`). If a fixture from a
crashed test remains in the directory, the main
`tools/run_all_audits.sh` sweep sees it and can trip a content gate.
Crash residue is deliberately NOT removed by the next run: a sweep
cannot tell a crashed run's files from a live run's, so an automatic
sweep could only ever delete fixtures a concurrently running instance
owns. Remove residue only by an explicit cleanup, run from the
repository root while no test run is active:

```
rm -rf tests/tmp
```

Never run that cleanup while a suite may be running: the live
fixtures under `tests/tmp/` are the running tests' own uniquely named
directories, so the command would delete fixtures those tests own.

## Global-state isolation

The regression suite is driven by `run-linter-regression.py`, which runs
the `unittest` module as a subprocess, and many linter invocations run in
their own subprocesses via the `run_linter` helper; some tests, however,
import linter modules and drive them in-process, so such a test
that patches a shared or module-level global (an environment variable, a
module attribute, `sys.argv`, a class attribute, or a monkeypatched function)
must restore it deterministically, or the mutation leaks into a sibling test
that runs later in the same process. Use one of the two sanctioned
mechanisms: `unittest.mock.patch` (in its context-manager or decorator form,
which restores the original on exit and on exception), or an explicit
`try/finally` that saves the prior value before the patch and restores it in
the `finally`. Restore even when the patched module was loaded fresh for the
test: relying on a discarded per-test module instance for isolation is
fragile, since a later change to a shared or cached import would silently
reintroduce the leak.

## Real-shell checks

A test or a verification that has to confirm how a real shell treats a command string (whether bash joins
a continuation, whether `sh -c` runs an argument) runs it through
[`tools/run-shell-stubbed.py`](../tools/run-shell-stubbed.py), never through a shell-function stub, which a
nested `sh -c` does not inherit (that gap once let a real `gh pr merge` run during hook verification,
backlog item 3b116). The tool runs the command in restricted bash with PATH holding only gh and git stand-ins,
restricted `bash` and `sh` wrappers and a few harmless utilities, and with an environment built from scratch;
restricted mode then refuses a slash in a command name, a PATH change, `command -p`, `exec` and similar, so
a real gh or git cannot be reached. Output redirection is refused too, and `sh` is emulated by
`bash --posix`; the tool's docstring states these limits.

## Coverage

Each linter has its own `LinterTestCase` subclass (e.g. `LanguageLinterTests`,
`SecretsLinterTests`); the linter under test is identified by the
enclosing class, and individual test methods are named
`test_<rule>_<expected_outcome>` (e.g. `test_em_dash_flagged`,
`test_template_placeholder_domain_allowed_in_template_file`). Every
linter in the audit programme has at least one positive test for its
primary rule. Additional rule-specific, negative, and environmental
tests can be added as maintenance reveals the need.

Generator-output drift checks use the same positive-control principle. Gate 34
(`tools/build-portal.py --check`) is covered by `PortalGeneratorCheckTests`: one
test requires the checked-out portal and scorecard to be in sync, and one
redirects the generator to a temporary tree and requires drift in either
generated output to return non-zero.

When a fixture targets a specific filter path or branch of a linter
CHANGE (a widened window, a new skip class, a new verdict), verify
before commit that the fixture FAILS against the pre-change linter
(or a deliberately weakened copy): a fixture that passes both states
guards nothing. The motivating catch is the #624 hollow fixture,
whose link filename satisfied an unrelated filter path, so the new
trailing-window code was never exercised; the #625 build applied the
weakened-copy mutation test to all four of its fixtures as the
standing form of this rail.
