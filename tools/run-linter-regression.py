#!/usr/bin/env python3
"""Thin wrapper that runs the full tests/ regression suite.

The audit programme's linter regression test suite gate invokes this
script (a gate in the inventory; its number is maintained in
``governance/specification-audit-programme.md`` §6 and is not repeated
here, because gate numbers shift when a gate is inserted). It exists so
that all four audit-programme surfaces (spec inventory, workflow,
runner, pre-commit hook) can reference the same ``tools/X.py`` shape
that the gate-name parity linter expects.

Discovers every top-level ``tests/test_*.py`` file itself (sorted by
module name), prints the module list it runs, and runs all of the
modules in ONE ``unittest`` invocation, so a new test file is in the
gate by existing rather than by a hand-maintained module list or a
per-class re-export in ``tests/test_linters.py`` (the 3b525 finding:
the hand-maintained list ran two modules and covered the other test
files only through such re-exports, which a new file or class silently
misses). Only top-level ``tests/test_*.py`` files are in scope: a
``test_*.py`` file inside a ``tests/`` SUBDIRECTORY is a refusal (exit
2, naming the nested file), never a silent omission, and so is a
``tests/`` subdirectory that cannot be inspected at all (a symlinked
subdirectory, an unreadable one, or a ``test_*`` package directory).

Refusals never soften to green (the 3b525 round-1 and round-2
findings):

* Before running anything, ``main`` re-enumerates ``tests/`` with
  ``os.walk`` (not the discovery glob) and refuses (exit 2) when the
  run list does not exactly match the on-disk top-level test files.
  This completeness self-check lives HERE, not in a test module, so a
  run-list regression that drops a test module (including
  ``tests/test_linters.py`` itself) cannot also remove the check. The
  walk uses an ``onerror`` handler and refuses a subdirectory it
  cannot inspect, a symlinked subdirectory, and a ``test_*`` package
  directory, so no test file can hide behind an unwalkable entry.
* The child driver repeats the enumeration itself against its OWN
  ``sys.argv`` and refuses (exit 2) when the two differ, so a filter
  applied to the child's argv, or inside the driver, cannot drop a
  module (the round-2 finding: the parent validated only its own
  module list, not what the child ran).
* A discovered file whose import raises ANYTHING, ``BaseException``
  included (an import-time ``SystemExit(0)`` must not become a green
  run), is a refusal: exit 2, naming the file.
* The driver loads each module's suite and refuses (exit 2, naming
  the file) a module that contributes zero test cases, so an empty
  ``load_tests`` or a class moved off ``TestCase`` cannot hollow a
  module out to ZERO tests silently. A PARTIALLY hollowed module (a
  ``load_tests`` that returns some but not all of a module's tests)
  is NOT detected: the loaded suite is the gate's only ground truth,
  so the sentinel's per-module counts match what was loaded, not what
  the file defines.
* Completion is established from the child's own executed suite, not
  from summary text: the driver runs with ``exit=False`` and emits a
  final sentinel line carrying a per-run nonce from this parent plus
  ``testsRun``, ``notStarted`` (see below), the per-module test counts
  and ``wasSuccessful``. A green child exit is believed only when that
  sentinel is the LAST stderr line, the nonce matches, the per-module
  counts name exactly the handed modules with at least one test each,
  ``testsRun`` plus ``notStarted`` equals their sum (with ``testsRun``
  at least 1), and ``wasSuccessful`` is True; otherwise the run is
  refused with exit 2. A premature ``SystemExit`` from ``load_tests``,
  ``setUpClass`` or ``setUpModule`` ends the child before the sentinel
  and is therefore refused, and a stray ``Ran N tests`` line written
  by a grandchild that inherits stderr cannot stand in for it.
* The nonce travels over the child's STDIN (this parent writes it to
  a pipe; the driver reads it and rebinds its stdin to ``os.devnull``,
  closing the pipe, before importing any test module), never on argv
  and never in the environment, so it never appears in ``sys.argv``,
  ``os.environ`` or ``/proc/<pid>/cmdline`` (the 3b525 round-3
  finding: on argv, a ``load_tests`` could read the nonce and forge
  the sentinel). What the nonce and sentinel defend against:
  accidental early exits (a premature ``SystemExit`` before the
  sentinel), grandchild or stray output standing in for the summary
  or the sentinel, dropped modules, and zero-test modules. What they
  do NOT defend against: test code in the child process that
  deliberately reads the driver's state and forges a complete
  sentinel. The driver is a ``python -c`` script, so the nonce it
  reads is a module-level global of ``__main__`` for the life of the
  child, and one line of test code (``import __main__`` and then
  ``__main__.nonce``) recovers it; this is a documented accepted
  residual, pinned by a test in ``tests/test_regression_gate.py``
  (such code could equally monkeypatch ``unittest``, patch the
  driver's globals, or replace the result object; no in-process
  scheme is proof against deliberately adversarial in-process code).
  Nor do they defend against a partially hollowed module (see the
  zero-test bullet above).
* A ``SkipTest`` raised in ``setUpClass`` or ``setUpModule`` bypasses
  ``startTest`` for every test it covers, so ``testsRun`` legitimately
  undercounts the loaded suite. The driver counts those never-started
  tests from the loaded suite (by skipped class and module) and
  reports them as ``notStarted`` in the sentinel, so a run unittest
  itself reports green with class-level skips in a module that
  otherwise ran is not refused, while a dropped test (which no skip
  record accounts for) still is.
* Every module must START at least one test (the 3b525 round-8 W1
  finding: a file on the run list is not a file whose tests ran). The
  driver records, per handed module, how many of its loaded tests
  reach ``startTest`` and, after the run, refuses (exit 2, naming the
  file) a module with none: a ``SkipTest`` raised in ``setUpModule``,
  or in ``setUpClass`` for every class the module has, is a refusal
  even when unittest itself reports the run green. A module that
  defines no tests is refused earlier, before the run, by the
  zero-test-cases check above. The rule for skips: a test skipped
  individually (a skip decorator, or ``self.skipTest`` inside the
  test) reaches ``startTest`` and counts as started, so per-test skips
  stay normal; only tests a class- or module-level ``SkipTest`` kept
  from ``startTest`` count as not started.
* A green child exit additionally needs unittest's own ``Ran N
  tests`` line with N at least 1 somewhere in its stderr.

The child's stderr is streamed to this process's stderr line by line
as it arrives (and accumulated for the checks above); stdout is
flushed before the child starts, so the module list precedes the
child's output even when stdout is a pipe, and a refusal message
always starts on its own line. Passing output: stdout carries the
module list ("Running test modules:" and one indented module name per
line); stderr carries unittest's own output unchanged (progress, any
failure detail, "Ran N tests" and "OK"), followed by the sentinel as
its one extra, last line.

Exit code is otherwise forwarded from unittest: 0 if all tests pass,
non-zero on failure.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import os
import re
import secrets
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Child driver: FIRST consume the per-run nonce from stdin and rebind
# stdin to os.devnull (closing the pipe), before any test module is
# imported; the nonce is never on argv or in the environment (a
# load_tests reading sys.argv or /proc/<pid>/cmdline finds only module
# names). The nonce binding below is a module-level global of __main__
# (this driver runs as a python -c script), so test code in this process
# CAN recover it via "import __main__" and forge the sentinel: a
# documented accepted residual, pinned by tests/test_regression_gate.py
# and stated in the module docstring above. Then refuse
# (exit 2) when the argv module list differs from the driver's own
# enumeration of top-level tests/test_*.py files, so a filtered child
# argv (or a filter inside this driver) cannot drop a module. Then
# import every module, refusing loud (exit 2, naming the file) when one
# cannot be imported; the import check catches BaseException, not Exception:
# a module raising SystemExit(0) at import time would otherwise end the
# child with exit 0 before any test runs. Then load each module's suite and
# refuse (exit 2, naming the file) a module contributing zero test cases,
# recording per-class loaded counts on the way. Run with exit=False,
# recording per module how many tests reach startTest, and refuse (exit 2,
# naming the file) a module none of whose tests started. Then emit the
# sentinel line the parent requires as the last stderr line: the
# nonce, testsRun, notStarted (loaded tests a class- or module-level
# SkipTest kept from reaching startTest, counted from the loaded suite via
# the skip records' setUpClass/setUpModule holders), wasSuccessful and the
# per-module test counts.
_DRIVER = """\
import importlib
import os
import sys
import unittest

nonce = sys.stdin.readline().strip()
devnull = os.open(os.devnull, os.O_RDONLY)
os.dup2(devnull, 0)
os.close(devnull)
modules = sys.argv[1:]
on_disk = sorted(
    "tests." + entry.name[:-3]
    for entry in os.scandir("tests")
    if entry.is_file(follow_symlinks=False)
    and entry.name.startswith("test_") and entry.name.endswith(".py"))
if sorted(modules) != on_disk:
    print("REFUSED: driver argv modules %s do not match on-disk "
          "tests/test_*.py files %s" % (sorted(modules), on_disk),
          file=sys.stderr)
    sys.exit(2)
failed = False
for name in modules:
    try:
        importlib.import_module(name)
    except BaseException as exc:
        print("REFUSED: cannot import tests/%s.py: %r"
              % (name.partition(".")[2], exc), file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item

loader = unittest.defaultTestLoader
counts = {}
class_counts = {}
for name in modules:
    suite = loader.loadTestsFromName(name)
    counts[name] = suite.countTestCases()
    if counts[name] < 1:
        print("REFUSED: tests/%s.py contributes zero test cases"
              % name.partition(".")[2], file=sys.stderr)
        failed = True
    for case in flatten(suite):
        key = "%s.%s" % (type(case).__module__, type(case).__qualname__)
        class_counts[key] = class_counts.get(key, 0) + 1
if failed:
    sys.exit(2)
# Record, per handed module, how many of its tests reach startTest. The
# map from each loaded case to its module is built from the very suite
# the runner is handed (one child suite per argv name, in argv order),
# before the run frees its cases; a started case is popped, so an id is
# only looked up while its case is alive.
case_module = {}
started = dict.fromkeys(modules, 0)
class StartRecordingResult(unittest.TextTestResult):
    def startTest(self, test):
        name = case_module.pop(id(test), None)
        if name is not None:
            started[name] += 1
        super().startTest(test)
class StartRecordingRunner(unittest.TextTestRunner):
    resultclass = StartRecordingResult
    def run(self, test):
        for name, module_suite in zip(modules, test):
            for case in flatten(module_suite):
                case_module[id(case)] = name
        return super().run(test)
program = unittest.main(module=None, argv=["unittest"] + modules,
                        testRunner=StartRecordingRunner, exit=False)
result = program.result
# A module none of whose tests started (a SkipTest from setUpModule, or
# from setUpClass in every class it has) is a refusal naming the file,
# whatever the rest of the run did: a file on the run list is not a file
# whose tests ran. A test skipped individually (a skip decorator or
# self.skipTest) reaches startTest and counts as started.
for name in modules:
    if started[name] < 1:
        print("REFUSED: none of the %d loaded tests of tests/%s.py "
              "started (a SkipTest raised in setUpModule, or in "
              "setUpClass for every class); every module must start at "
              "least one test" % (counts[name], name.partition(".")[2]),
              file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
# A SkipTest from setUpClass/setUpModule is recorded as ONE skip on a
# holder named "setUpClass (<module>.<Class>)" or "setUpModule
# (<module>)" and none of the covered tests reaches startTest; count
# those tests from the loaded suite so the parent can reconcile
# testsRun against the loaded total. An unknown holder counts 0, so a
# mismatch stays a refusal (fail closed).
not_started = 0
for skipped_test, _reason in result.skipped:
    holder = skipped_test.id()
    if holder.startswith("setUpClass (") and holder.endswith(")"):
        not_started += class_counts.get(holder[len("setUpClass ("):-1], 0)
    elif holder.startswith("setUpModule (") and holder.endswith(")"):
        not_started += counts.get(holder[len("setUpModule ("):-1], 0)
print("REGRESSION-GATE-RESULT %s testsRun=%d notStarted=%d "
      "wasSuccessful=%s %s"
      % (nonce, result.testsRun, not_started, result.wasSuccessful(),
         " ".join("%s=%d" % (name, counts[name])
                  for name in sorted(counts))),
      file=sys.stderr)
sys.exit(0 if result.wasSuccessful() else 1)
"""

# unittest's summary: "Ran 1 test in 0.001s", "Ran 3310 tests in 786.1s"
# (the count grows as tests are added; only N at least 1 is checked here).
_SUMMARY_LINE = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)

# The driver's completion sentinel (see _DRIVER). The nonce is 32 hex
# digits from secrets.token_hex(16), delivered to the child over stdin;
# the per-module counts are space-separated "tests.<name>=<count>"
# tokens.
_SENTINEL = re.compile(
    r"^REGRESSION-GATE-RESULT (?P<nonce>[0-9a-f]{32}) "
    r"testsRun=(?P<ran>\d+) notStarted=(?P<notstarted>\d+) "
    r"wasSuccessful=(?P<ok>True|False)"
    r"(?P<counts>( [A-Za-z0-9_.]+=\d+)*)$")


def discover_test_modules(repo_root: Path = REPO_ROOT) -> list[str]:
    """Every top-level tests/test_*.py as a dotted module name, sorted."""
    return sorted(
        "tests." + path.stem
        for path in (repo_root / "tests").glob("test_*.py")
    )


def completeness_refusal(modules: list[str],
                         repo_root: Path = REPO_ROOT) -> str | None:
    """Refusal message when ``modules`` is not the complete on-disk set.

    Re-enumerates tests/ with os.walk, independently of the discovery
    glob, so a narrowed glob or a filter applied to the run list no
    longer matches the walk. A test_*.py file in a tests/ subdirectory
    is a refusal: only top-level tests/test_*.py files are in scope.
    So is anything the walk cannot see through: a subdirectory that
    raises on listing (onerror), a symlinked subdirectory (os.walk
    does not follow links, so one could hide test files), and a
    test_* package directory (its tests would be neither discovered
    nor refused by the per-file check). Returns None when the run
    list is complete.
    """
    tests_dir = repo_root / "tests"
    walk_errors: list[OSError] = []
    on_disk = []
    for dirpath, dirnames, filenames in os.walk(tests_dir,
                                                onerror=walk_errors.append):
        for dirname in dirnames:
            subdir = Path(dirpath) / dirname
            if subdir.is_symlink():
                return ("symlinked subdirectory %s: tests/ must not "
                        "contain directory symlinks, which could hide "
                        "test files from this walk" % subdir)
            if dirname.startswith("test_"):
                return ("test package directory %s: only top-level "
                        "tests/test_*.py files are in scope" % subdir)
        for filename in filenames:
            if filename.startswith("test_") and filename.endswith(".py"):
                if Path(dirpath) != tests_dir:
                    return ("nested test file %s: only top-level "
                            "tests/test_*.py files are in scope"
                            % (Path(dirpath) / filename))
                on_disk.append("tests." + filename[:-3])
    if walk_errors:
        return ("cannot inspect %s: %s" % (
            getattr(walk_errors[0], "filename", tests_dir), walk_errors[0]))
    if not on_disk:
        return "no tests/test_*.py files found under %s" % tests_dir
    if sorted(modules) != sorted(on_disk):
        return ("run list %s does not match on-disk tests/test_*.py "
                "files %s" % (sorted(modules), sorted(on_disk)))
    return None


def _sentinel_refusal(last_line: str, nonce: str,
                      modules: list[str]) -> str | None:
    """Refusal message when ``last_line`` is not a believable sentinel."""
    match = _SENTINEL.match(last_line)
    if match is None:
        return ("the child's last stderr line is not the driver's "
                "completion sentinel; completion is established only "
                "from the executed suite's own result")
    if match.group("nonce") != nonce:
        return "the completion sentinel does not carry this run's nonce"
    counts: dict[str, int] = {}
    for token in match.group("counts").split():
        name, _, value = token.partition("=")
        counts[name] = int(value)
    if sorted(counts) != sorted(modules):
        return ("the completion sentinel's module counts %s do not name "
                "exactly the handed modules %s"
                % (sorted(counts), sorted(modules)))
    if any(count < 1 for count in counts.values()):
        return ("the completion sentinel reports a module with zero "
                "test cases")
    ran = int(match.group("ran"))
    not_started = int(match.group("notstarted"))
    if ran < 1 or ran + not_started != sum(counts.values()):
        return ("the completion sentinel's testsRun=%d plus "
                "notStarted=%d (loaded tests a class- or module-level "
                "SkipTest kept from starting) does not equal the "
                "per-module total %d (with at least one test run)"
                % (ran, not_started, sum(counts.values())))
    if match.group("ok") != "True":
        return ("the child exited 0 but its own result reports "
                "wasSuccessful=False")
    return None


def main(repo_root: Path = REPO_ROOT, popen=subprocess.Popen) -> int:
    modules = discover_test_modules(repo_root)
    refusal = completeness_refusal(modules, repo_root)
    if refusal is not None:
        print("REFUSED: " + refusal, file=sys.stderr)
        return 2
    print("Running test modules:")
    for name in modules:
        print("  " + name)
    # Flush before the child starts, so the module list precedes the
    # child's output even when stdout is a block-buffered pipe.
    sys.stdout.flush()
    nonce = secrets.token_hex(16)
    proc = popen(
        [sys.executable, "-c", _DRIVER, *modules],
        cwd=str(repo_root),
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # The nonce travels over the child's stdin, never on argv or in the
    # environment, so it never appears in /proc/<pid>/cmdline; the
    # driver consumes it before importing any test module. Test code
    # inside the child can still recover it from __main__.nonce and
    # forge the sentinel (the documented accepted residual; see the
    # module docstring). 33 bytes fit the pipe buffer, so this cannot
    # deadlock against the stderr read.
    proc.stdin.write((nonce + "\n").encode("ascii"))
    proc.stdin.close()
    # Stream the child's stderr through as it arrives (a hang or an
    # interrupt must not swallow the progress seen so far), while
    # accumulating it for the checks below.
    lines: list[str] = []
    for raw in proc.stderr:
        line = raw.decode("utf-8", "replace")
        sys.stderr.write(line)
        sys.stderr.flush()
        lines.append(line)
    returncode = proc.wait()

    def refuse(message: str) -> int:
        # The child's progress dots may leave an unterminated line;
        # a refusal always starts on its own line.
        if lines and not lines[-1].endswith("\n"):
            sys.stderr.write("\n")
        print("REFUSED: " + message, file=sys.stderr)
        return 2

    if returncode == 0:
        stderr_text = "".join(lines)
        counts = _SUMMARY_LINE.findall(stderr_text)
        if not counts or int(counts[-1]) < 1:
            return refuse(
                "unittest exited 0 without a 'Ran N tests' line "
                "with N at least 1; not a believable green run")
        last_line = lines[-1].rstrip("\n") if lines else ""
        sentinel_refusal = _sentinel_refusal(last_line, nonce, modules)
        if sentinel_refusal is not None:
            return refuse(sentinel_refusal)
    return returncode


if __name__ == "__main__":
    sys.exit(main())
