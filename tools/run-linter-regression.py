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
* A ``SkipTest`` raised in ``setUpClass`` bypasses ``startTest`` for
  every test of that class, so ``testsRun`` legitimately undercounts
  the loaded suite. The driver counts those tests from the loaded
  suite (unittest runs ``setUpClass`` once per run of consecutive
  cases of the same class object, so among the occurrences the run
  passed over without a start since the previous matched start, each
  such run takes one ``setUpClass`` skip record of that class arrived
  in that stretch, matched by the ``module.qualname`` name unittest
  gives the record, and each occurrence in a run that took a record
  counts once; a run with no record left counts as dropped, so a
  skipped class loaded twice is counted per occurrence, two classes
  sharing a module and qualname are two runs, and one skip record
  never covers two runs; one run contributes at most one counted
  record: a class cleanup's ``SkipTest`` after a skipped
  ``setUpClass`` is recorded under the same ``setUpClass`` name, and
  such further records of one run, told apart from a later run's by
  arriving back to back (no start and no other skip record in
  between) with the same holder and the same ``_previousTestClass``
  on the result, are discarded, not credited to a later run) and
  reports them as ``notStarted`` in the
  sentinel, so a run unittest itself reports green with such skips in
  a module that otherwise ran is not refused, while a dropped test
  (which no skip record accounts for) still is. Both hold only for a
  suite that runs its cases in its flattened order (see the
  reordering-suite residual below). The grouping of records into
  runs depends on unittest's private _previousTestClass attribute
  and its set-up order (set to a run's class only after that class's
  set-up; read in CPython 3.14 and 3.11 ``suite.py``), which unittest
  does not document, so a change there could misgroup records (an
  accepted residual). When the result object has no
  ``_previousTestClass`` attribute at all as a ``setUpClass`` skip
  record arrives, the run is refused (exit 2, naming
  ``_previousTestClass`` and the Python version), never grouped by a
  default; ``None``, its value before the first test, is an answer
  (the 3b525 round-16 review, agy). ``notStarted`` counts
  only these ``setUpClass`` skips: a test of a skip-decorated class
  reaches ``startTest`` (``testsRun`` counts it), and a test a
  ``SkipTest`` in ``setUpModule`` kept from starting is not counted,
  so it can only make that reconciliation fail (a handed module with
  no credited start is refused by the next bullet; a helper module
  outside the run list, whose class a handed module loaded, is
  refused by the reconciliation).
* Every module must earn at least one CREDITED START (the 3b525
  round-8 W1 finding: a file on the run list is not a file whose
  tests ran). This per-module rule is separate from the sentinel's
  ``notStarted`` count above. A credited start is a test from this
  module's loaded suite that reaches ``startTest`` outside a
  skip-decorated class: a started test is credited to the handed
  module whose suite, as ``unittest.main`` loads it (one suite per
  module, in argv order), contains it, whatever the test's type
  (``TestCase``, ``unittest.FunctionTestCase``, a doctest case, or any
  other test object). Credit is per suite OCCURRENCE, not per case
  object: the driver lists every occurrence in flattened suite order
  (holding each case alive until the run ends, so no id or identity
  is reused) and matches each start, by identity, to the next pending
  occurrence of that object. Before the run, a case object that
  appears in more than one handed module's flattened suite is refused
  (exit 2, naming the modules): with one object in two modules'
  suites, forward matching plus a ``setUpClass``-skipped class between
  the occurrences credited the wrong module, giving a false pass or a
  false refusal (the 3b525 round-12 review, codex E1 and E2), so
  every occurrence a start can match lies in one module's suite.
  The gate checks that each module's suite starts
  something, not who wrote the test's code (rounds 9 and 10 tried to
  credit the module defining the code, and every variant refused
  legitimate modules or credited crafted ones). Before crediting, the
  driver checks the pairing: ``unittest.main`` must load exactly one
  suite per handed module, each with the case count the driver's own
  load found for that module; otherwise it refuses (exit 2, naming
  the mismatch) rather than guess (a ``load_tests`` that returns a
  different case count on a second load fails this; one that returns
  different cases in the same number does not, see the residuals
  below). When unittest itself
  reports the run green, the driver refuses (exit 2, naming the file)
  a module with no credited start, as "tests/X.py: N loaded, 0
  credited starts" plus the definition above; the refusal names no
  cause. Skips: a test that a ``SkipTest``
  raised in ``setUpModule`` or ``setUpClass`` kept from ``startTest``
  is not a credited start, and neither is a test whose class is
  skip-marked by a class decorator (``unittest.skip``, or ``skipIf``
  or ``skipUnless`` whose condition skips, on the class or a base
  class), even though unittest calls ``startTest`` for such a test
  before it reads the class flag (the 3b525 round-8 review N1); the
  flag is read from ``test.__class__``, as unittest reads it. So a
  module whose every loaded case is skipped at class level, by
  either means, is a refusal. A module whose loaded suite holds no
  cases is refused earlier, before the run, by the zero-test-cases
  check above. Accepted residuals: the pairing check compares case
  counts per suite, not case identity, so a second load that returns
  different cases in the same number passes it, and its cases are
  credited as ``unittest.main`` loaded them; a start is matched to the
  next pending occurrence in unittest's run order, so a test that
  itself starts another loaded case object (outside the suite's own
  iteration) can move the match (test code controlling the run is the
  in-process residual below); a suite that reorders, drops or
  substitutes cases, in its own ``run`` or its ``__iter__``, and a
  test object that is not a suite but runs inner cases, are outside
  what the gate can account for, because crediting and the
  ``setUpClass`` skip reconciliation both assume a suite runs its
  cases in its flattened order (observed effects: a module whose
  reordering suite holds a ``setUpClass``-skipped class can be falsely
  refused, and a dropping suite can produce a false pass without a
  shared case object; no current module uses such a suite or test
  object); a module that only imports and loads
  another module's ``TestCase`` classes earns credit for their
  started tests (borrowing; no current module does this; the gate
  checks that each module's suite starts something, not who wrote
  it); a test skipped individually (a skip decorator on the test
  method, or ``self.skipTest`` inside the test or its ``setUp``) is a
  credited start, so a module whose every test is skipped
  individually is not refused; and test code can forge the result
  in-process (the ``__main__.nonce`` residual above).
* A run unittest itself reports as failed (``wasSuccessful()`` False,
  including an error, not a skip, raised by ``setUpModule`` or
  ``setUpClass``) is never turned into that zero-started refusal: the
  driver exits 1 with unittest's own failure report, and this script
  forwards the 1 (the 3b525 round-8 review N2: such a run printed a
  refusal naming a ``SkipTest`` cause it did not have and exited 2).
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
non-zero on failure (1 when unittest reports a failure or an error).

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
# refuse (exit 2, naming the file) a module contributing zero test cases.
# Run with exit=False,
# refusing (exit 2) when unittest.main's suites do not pair one-to-one
# with the handed modules and their loaded counts, or when one case
# object is in more than one module's suite (naming them), recording per module
# its credited starts (occurrences in its loaded suite that reach
# startTest outside a skip-decorated class), and, when
# unittest reports the run green, refuse (exit 2, naming the file) a
# module with none. Then emit the sentinel line the parent requires as
# the last stderr line: the nonce, testsRun, notStarted (loaded
# occurrences a SkipTest in setUpClass kept from reaching startTest,
# counted per occurrence via the skip records' setUpClass holders),
# wasSuccessful and the per-module test counts.
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
        if isinstance(item, unittest.suite.BaseTestSuite):
            yield from flatten(item)
        else:
            yield item

loader = unittest.defaultTestLoader
counts = {}
for name in modules:
    suite = loader.loadTestsFromName(name)
    counts[name] = suite.countTestCases()
    if counts[name] < 1:
        print("REFUSED: tests/%s.py contributes zero test cases"
              % name.partition(".")[2], file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
# Record, per handed module, its credited starts: how many occurrences
# in its own loaded suite reach startTest. A started test is credited to
# the handed module whose suite (as unittest.main loads it, one per
# module in argv order) contains it; the gate checks that each module's
# suite starts something, not who wrote the test's code, so a module
# that loads another module's TestCase class earns credit for it (an
# accepted residual). Before crediting, the pairing is checked: one
# suite per handed module, each with that module's loaded count, or the
# run is refused rather than credited by guesswork. A test whose class
# is skip-marked (unittest.skip, or skipIf/skipUnless taking effect, on
# the class or a base) reaches startTest before unittest reads the
# class flag (from test.__class__, read the same way here), but is not
# credited. Credit is per suite occurrence, not per case object: every
# occurrence is listed as (case, module) in flattened suite order, and a
# start is matched to the next pending occurrence of that same object
# (identity, not equality). A case object in more than one module's
# suite is refused before the run, so a match never crosses modules;
# a suite that reorders, drops or substitutes cases (in its run or its
# __iter__), or a non-suite test object running inner cases, is a
# documented residual.
# The list holds every case alive until the run ends
# (unittest's suites drop each case or sub-suite once run, which frees
# it), so matching by identity never meets a reused id. Occurrences a
# start passes over never started; a run of consecutive occurrences of
# one class object among them is notStarted when a setUpClass skip
# record of that class, arrived since the previous matched start and not
# yet taken by an earlier such run, accounts for it (one counted record
# per run; a run's further records under the same holder, from a class
# cleanup that skips after setUpClass skipped, are discarded on arrival).
occurrences = []
started = dict.fromkeys(modules, 0)
class StartRecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_occurrence = 0
        self.class_skips = {}
        self.last_record = None
        self.not_started = 0
    def settle(self, upto):
        # unittest sets a class up once per run of consecutive cases of
        # the same class object (not the same name: two classes a factory
        # built with one module and qualname are two runs). Each such run
        # among the passed-over occurrences takes one skip record of its
        # class, looked up by strclass, the name unittest gives the
        # record's holder; a run with no record left is dropped, not
        # notStarted.
        previous = None
        covered = False
        for case, _name in occurrences[self.next_occurrence:upto]:
            if case.__class__ is not previous:
                holder = unittest.util.strclass(case.__class__)
                covered = self.class_skips.get(holder, 0) > 0
                if covered:
                    self.class_skips[holder] -= 1
                previous = case.__class__
            if covered:
                self.not_started += 1
        self.next_occurrence = upto
        self.class_skips.clear()
    def addSkip(self, test, reason):
        # One run of a class can give several records under its setUpClass
        # holder (unittest records a class cleanup's SkipTest, run after a
        # failed setUpClass, under the same name). They arrive back to back
        # while unittest's _previousTestClass still holds the class before
        # the run (it is set to the run's class only after set-up), so a
        # record continuing the previous one back to back (no start and
        # no other skip record in between), with the same holder and that
        # same previous class, is the same run's and is discarded: one
        # run contributes at most one counted record, never a spare for a
        # later run. _previousTestClass is private to unittest (an
        # accepted residual; see the docstring). An absent attribute (a
        # Python that renames it or stops setting it) cannot answer, so
        # it is refused rather than read as None, the value TestResult
        # gives it before the first test.
        holder = test.id()
        if holder.startswith("setUpClass (") and holder.endswith(")"):
            holder = holder[len("setUpClass ("):-1]
            try:
                previous = self._previousTestClass
            except AttributeError:
                print("\\nREFUSED: the unittest result has no "
                      "_previousTestClass attribute (Python %d.%d.%d); "
                      "setUpClass skip records cannot be grouped into runs"
                      % sys.version_info[:3], file=sys.stderr)
                sys.exit(2)
            run = (holder, previous)
            last = self.last_record
            if last is None or last[0] != run[0] or last[1] is not run[1]:
                self.class_skips[holder] = self.class_skips.get(holder, 0) + 1
            self.last_record = run
        else:
            # Any other skip record ends "back to back". In a standard
            # suite this changes no outcome: two runs of one class with
            # the same previous class have an occurrence of that previous
            # class between them, and on a run unittest reports green one
            # with no start and no setUpClass skip record of its own was
            # dropped by a skipping setUpModule; no record accounts for
            # it, so the reconciliation refuses with or without this
            # reset. Kept so the rule is the one documented.
            self.last_record = None
        super().addSkip(test, reason)
    def startTest(self, test):
        # A start ends "back to back": a later run of the same class
        # after the same previous class is a new run (pinned by
        # test_main_green_with_cleanup_skips_around_starts).
        self.last_record = None
        for index in range(self.next_occurrence, len(occurrences)):
            case, name = occurrences[index]
            if case is test:
                self.settle(index)
                self.next_occurrence = index + 1
                if not getattr(test.__class__, "__unittest_skip__", False):
                    started[name] += 1
                break
        super().startTest(test)
class StartRecordingRunner(unittest.TextTestRunner):
    resultclass = StartRecordingResult
    def run(self, test):
        # unittest.main loads one suite per handed module, in argv order;
        # refuse, naming the mismatch, when this load does not pair up
        # with the counts loaded above.
        suites = list(test)
        if len(suites) != len(modules):
            print("REFUSED: unittest.main loaded %d suites for %d handed "
                  "modules; started tests cannot be paired with modules"
                  % (len(suites), len(modules)), file=sys.stderr)
            sys.exit(2)
        for loaded_by, suite in zip(modules, suites):
            if suite.countTestCases() != counts[loaded_by]:
                print("REFUSED: tests/%s.py: unittest.main loaded %d test "
                      "cases, the driver's own load %d; started tests "
                      "cannot be paired with this module"
                      % (loaded_by.partition(".")[2], suite.countTestCases(),
                         counts[loaded_by]), file=sys.stderr)
                sys.exit(2)
            for case in flatten([suite]):
                occurrences.append((case, loaded_by))
        # Refuse, naming the modules, a case object in more than one
        # handed module's suite: its starts cannot be credited to one
        # module (every occurrence is held alive, so ids are not reused).
        # Keyed by identity, with the module names in a set of their own:
        # a case is never compared with a string (its __eq__ could say
        # equal).
        loaded_in = {}
        for case, loaded_by in occurrences:
            loaded_in.setdefault(id(case), (case, set()))[1].add(loaded_by)
        shared = False
        for case, loaded_by in loaded_in.values():
            names = sorted(loaded_by)
            if len(names) > 1:
                print("REFUSED: test case object %r is in the loaded suites "
                      "of more than one module (%s); its starts cannot be "
                      "credited to one module"
                      % (case, ", ".join("tests/%s.py" % name.partition(".")[2]
                                         for name in names)), file=sys.stderr)
                shared = True
        if shared:
            sys.exit(2)
        return super().run(test)
program = unittest.main(module=None, argv=["unittest"] + modules,
                        testRunner=StartRecordingRunner, exit=False)
result = program.result
result.settle(len(occurrences))
# On a run unittest itself reports green, a module with no credited start
# is a refusal naming the file: a file on the run list is not a file
# whose tests ran. The message states only what was observed (loaded and
# credited counts), not a cause: a SkipTest in setUpModule or setUpClass
# and a skip-decorated class both end here. A test
# skipped individually (a skip decorator on the method, or self.skipTest)
# is a credited start. A run that already failed keeps unittest's exit 1
# and its own error report (a setUpModule or setUpClass that raised, not
# skipped, also starts no test).
if result.wasSuccessful():
    for name in modules:
        if started[name] < 1:
            print("REFUSED: tests/%s.py: %d loaded, 0 credited starts (a "
                  "credited start is a test from this module's loaded "
                  "suite that reached startTest outside a skip-decorated "
                  "class)"
                  % (name.partition(".")[2], counts[name]),
                  file=sys.stderr)
            failed = True
if failed:
    sys.exit(2)
# A SkipTest from setUpClass is recorded as a skip on a holder named
# "setUpClass (<module>.<Class>)" and none of the class's tests reaches
# startTest; a class cleanup that then raises SkipTest adds a further
# record under the same holder, and one run contributes at most one
# counted record. StartRecordingResult counts those occurrences (once
# each, however often the class is loaded or set up) so the parent can
# reconcile testsRun against the loaded total. Any other holder counts
# 0, so a mismatch stays a refusal (fail closed). A "setUpModule
# (<module>)" holder is deliberately not counted. When that module is a
# handed one, it usually has no credited start and is refused above;
# when it is a helper outside the run list (whose class a handed module
# loaded) or a handed module whose suite also holds another module's
# started class, the run reaches the parent, whose reconciliation of testsRun plus
# notStarted against the loaded total fails and refuses it.
print("REGRESSION-GATE-RESULT %s testsRun=%d notStarted=%d "
      "wasSuccessful=%s %s"
      % (nonce, result.testsRun, result.not_started, result.wasSuccessful(),
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
                "notStarted=%d (loaded tests of classes whose setUpClass "
                "raised SkipTest; tests a setUpModule SkipTest kept from "
                "starting are not counted) does not equal the "
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
