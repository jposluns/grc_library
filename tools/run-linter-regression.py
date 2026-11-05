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

CI sharding (maintainer directive 2026-11-04, the 3b789 gate 36 split):
``--shard I/K`` runs one deterministic slice of the same suite, and
``--verify-shards K`` checks the slicing without running a test. A UNIT
is a maximal run of consecutive occurrences of one class object within
one module's loaded suite, flattened in suite order, exactly the unit
``tools/measure-regression-timings.py`` measures (``compute_units``
here is kept in agreement with that tool by a regression test). Units
are assigned to the K shards by a deterministic greedy balance over
the measured weights in ``tests/regression-shard-weights.json``
(largest weight first, ties by unit key, each unit to the least-loaded
shard, ties to the lowest shard number); a unit the weights file does
not name gets a small default weight, so the weights only move units
between shards and never decide whether one runs. Every shard child
recomputes the WHOLE selection and refuses (exit 2) unless it is an
exact partition of the units its own suite load found: a unit no shard
selects, a unit two shards select, a selected unit the suites do not
hold, and an empty shard are each a refusal, so a selection defect
fails every shard loudly rather than dropping a test silently. The
shard child keeps the plain run's refusal posture: its argv module
list must match the on-disk tests/test_*.py files, an import that
raises anything (BaseException included) is a refusal, a zero-case
module is a refusal, a case object in two modules' suites is a
refusal, an unreadable or malformed weights file is a refusal, the
nonce travels over the child's stdin, and a green exit is believed
only with unittest's own ``Ran N tests`` line and a nonce-carrying
sentinel as the last stderr line whose ``testsRun`` plus ``notStarted``
equals the selected occurrence count, reconciled per unit (every
selected occurrence reached ``startTest`` or is accounted by a
``setUpClass`` ``SkipTest`` record, with the same record-grouping
rules as the full run), with at least one credited start in the shard.
The shard sentinel also carries ``credited`` (the shard's credited
starts) and one per-module credited-start token for EVERY discovered
module (zero allowed): a credited start is credited to the module
whose loaded suite holds the started occurrence, exactly as in the
full run. The parent refuses a sentinel whose module names are not
exactly the handed modules, whose per-module counts do not sum to its
``credited`` total, or whose ``credited`` exceeds ``testsRun``; and,
when the ``GITHUB_OUTPUT`` environment file is set (a GitHub Actions
step), it appends the counts as a ``credited`` multi-line step output
of block-style ``module: count`` lines (refusing, exit 2, when that
file cannot be written), so each CI shard job publishes its counts as
a job output. The sentinel and the outputs also carry two digests
(``unit_set_digest``): ``unitset``, the sha256 of the TOTAL unit list
the shard's own suite load found, and ``selection``, that of its
selected units, published as the ``units_sha256`` and
``selected_sha256`` outputs. The CI summary job's reconcile step
(tools/reconcile-regression-shards.py) sums the counts across all
shards and fails when any discovered module's total is zero, restoring
before merge the serial runner's refusal of a module with no credited
start, and fails unless every shard's ``units_sha256`` is the same, so
two runners that discovered different suites cannot pass as one
partition; a shard output that is missing, malformed, or naming a
module set other than the on-disk tests/test_*.py files is a refusal
there, never a pass. The pre-push guard (tools/pre-push-guard.sh) runs
the same K shards locally, each in its own temporary detached checkout
with ``GITHUB_OUTPUT`` pointed at a per-shard file, and reconciles
those files with ``reconcile-regression-shards.py --shard-outputs``.
Residuals specific to shard mode, beyond the full run's: within one
shard the zero-credited refusal is for the shard as a whole (at least
one credited start anywhere in it); the per-module rule is enforced
across shards by the reconcile step, so it holds only where that step
runs (CI's summary job and the pre-push guard; the plain run, which
tools/run_all_audits.sh and the pre-commit hook still invoke, keeps
the serial per-module rule). Two units of one class object
that land in one shard with nothing between them run under one
``setUpClass`` where the whole suite sets the class up twice (the
standard loader yields one unit per class, so no current module is
affected). Weights are advisory balance data; the selection mechanism,
never a weight, decides membership.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Shard-mode constants (see the docstring's CI-sharding section). The weights
# file is committed, measured data from tools/measure-regression-timings.py;
# a unit it does not name gets DEFAULT_UNIT_WEIGHT, and no effective weight
# falls below MINIMUM_UNIT_WEIGHT, so a crowd of unmeasured units still
# spreads across shards instead of piling onto one.
WEIGHTS_RELATIVE_PATH = "tests/regression-shard-weights.json"
WEIGHTS_SCHEMA_VERSION = 1
DEFAULT_UNIT_WEIGHT = 0.1
MINIMUM_UNIT_WEIGHT = 0.001

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


# ----------------------------------------------------------------------
# CI sharding (the docstring's CI-sharding section). The pure selection
# functions below are the single source of truth: the parent, the shard
# child driver (which loads this file by path) and the tests all call
# them, so the slicing CI runs is the slicing the tests exercise.
# ----------------------------------------------------------------------


def compute_units(module: str, cases: list) -> list[tuple[str, int, int]]:
    """Group a module's flattened cases into units.

    Returns ``[(key, first_index, last_index), ...]`` in suite order. A
    unit is a maximal run of consecutive occurrences of one class
    object; a case that is not a ``unittest.TestCase`` instance is its
    own unit. Ordinals count units per qualname within the module, from
    0, so every returned key is unique within the module. This mirrors
    ``compute_units`` in tools/measure-regression-timings.py (whose
    keys the weights file holds); a regression test keeps the two in
    agreement.
    """
    units: list[list] = []
    ordinals: dict[str, int] = {}
    previous = None
    for index, case in enumerate(cases):
        grouped = isinstance(case, unittest.TestCase)
        if grouped and units and type(case) is previous:
            units[-1][2] = index
        else:
            qualname = type(case).__qualname__
            ordinal = ordinals.get(qualname, 0)
            ordinals[qualname] = ordinal + 1
            units.append(["%s:%s#%d" % (module, qualname, ordinal), index, index])
        previous = type(case) if grouped else None
    return [tuple(unit) for unit in units]


def load_shard_weights(path) -> dict[str, float]:
    """The measured unit weights, or a ValueError naming what is wrong.

    Shard mode fails closed on balance data it cannot read: a missing,
    unreadable or malformed weights file is a refusal (exit 2 in the
    caller), never a silent fallback, so every shard of one commit
    computes its selection from one agreed input.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(
            "cannot read the shard weights file %s: %s" % (path, exc)) from None
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise ValueError(
            "the shard weights file %s is not valid JSON: %s" % (path, exc)) from None
    if (not isinstance(payload, dict)
            or payload.get("schema") != WEIGHTS_SCHEMA_VERSION
            or not isinstance(payload.get("units"), dict)):
        raise ValueError(
            "the shard weights file %s does not hold schema %d with a units "
            "object" % (path, WEIGHTS_SCHEMA_VERSION))
    weights: dict[str, float] = {}
    for key, value in payload["units"].items():
        if (not isinstance(key, str) or isinstance(value, bool)
                or not isinstance(value, (int, float)) or value < 0):
            raise ValueError(
                "the shard weights file %s holds a unit entry that is not a "
                "string key with a nonnegative number: %r" % (path, key))
        weights[key] = float(value)
    return weights


def effective_weight(weights: dict[str, float], key: str) -> float:
    """A unit's balance weight: measured, else the default, floored."""
    return max(float(weights.get(key, DEFAULT_UNIT_WEIGHT)), MINIMUM_UNIT_WEIGHT)


def shard_selection(unit_keys: list[str], weights: dict[str, float],
                    count: int) -> dict[int, list[str]]:
    """Deterministically partition ``unit_keys`` into ``count`` shards.

    Greedy balance: units in descending effective weight (ties by key),
    each to the least-loaded shard so far (ties to the lowest shard
    number). The result maps each shard number (1-based) to its units
    in ``unit_keys`` order. Deterministic for one input; weights only
    move a unit between shards, never in or out of the run.
    """
    if count < 1:
        raise ValueError("shard count must be at least 1, not %d" % count)
    if len(set(unit_keys)) != len(unit_keys):
        raise ValueError("the unit list holds a duplicate key")
    loads = [0.0] * count
    assigned: dict[str, int] = {}
    for key in sorted(unit_keys, key=lambda k: (-effective_weight(weights, k), k)):
        shard = min(range(count), key=lambda i: (loads[i], i))
        assigned[key] = shard + 1
        loads[shard] += effective_weight(weights, key)
    selection: dict[int, list[str]] = {n: [] for n in range(1, count + 1)}
    for key in unit_keys:
        selection[assigned[key]].append(key)
    return selection


def partition_refusal(selection: dict[int, list[str]], unit_keys: list[str],
                      count: int) -> str | None:
    """Refusal message unless ``selection`` is an exact partition.

    Fail closed: shard numbers must be exactly 1..count, every shard
    must select at least one unit, every unit of ``unit_keys`` must be
    selected exactly once, and nothing outside ``unit_keys`` may be
    selected. Returns None when the partition is exact.
    """
    if sorted(selection) != list(range(1, count + 1)):
        return ("the selection names shards %s, not exactly 1..%d"
                % (sorted(selection), count))
    if len(set(unit_keys)) != len(unit_keys):
        return "the unit list holds a duplicate key"
    expected = set(unit_keys)
    seen: dict[str, int] = {}
    for number in range(1, count + 1):
        keys = selection[number]
        if not keys:
            return "shard %d/%d selects zero units" % (number, count)
        for key in keys:
            if key in seen:
                return ("unit %s is selected by shard %d and shard %d; every "
                        "unit must run exactly once" % (key, seen[key], number))
            seen[key] = number
            if key not in expected:
                return ("shard %d selects unit %s, which the loaded suites do "
                        "not hold" % (number, key))
    missing = sorted(expected - set(seen))
    if missing:
        return ("no shard selects unit(s) %s; every unit must run exactly once"
                % ", ".join(missing))
    return None


def unit_set_digest(unit_keys) -> str:
    """The sha256 of a unit list as a SET: the sorted keys, one per line.

    Each shard publishes the digest of the TOTAL unit list its own suite
    load found and of its SELECTED units; the reconcile step requires
    every shard's total digest to agree, so a discovery difference between
    runners fails rather than splitting two different suites.
    """
    text = "".join(key + "\n" for key in sorted(unit_keys))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_shard_count(text: str) -> int:
    """The shard count K from its decimal spelling, or a ValueError."""
    if not (text.isascii() and text.isdigit()) or int(text) < 1:
        raise ValueError("shard count must be a positive integer, not %r" % text)
    return int(text)


def parse_shard_spec(text: str) -> tuple[int, int]:
    """(index, count) from an ``I/K`` shard spec, or a ValueError."""
    index_text, sep, count_text = text.partition("/")
    if not sep or not (index_text.isascii() and index_text.isdigit()):
        raise ValueError("a shard is named I/K with integers I and K, not %r" % text)
    count = parse_shard_count(count_text)
    index = int(index_text)
    if not 1 <= index <= count:
        raise ValueError("shard index %d is outside 1..%d" % (index, count))
    return index, count


# Shard child driver. It repeats the plain driver's refusal posture (see
# _DRIVER: nonce over stdin, argv-vs-disk module check, import and
# zero-case refusals, the shared-case refusal), loads THIS file by the
# path handed on argv to compute the selection with the same functions
# the parent and the tests use, refuses unless that selection exactly
# partitions the units its own suite load found, and then either reports
# the selection (verify mode) or runs its own shard's occurrences with
# per-unit accounting: every selected occurrence must reach startTest or
# be accounted by a setUpClass SkipTest record (grouped into runs by the
# same rules as the plain driver), and the shard must earn at least one
# credited start (a start outside a skip-decorated class). The sentinel
# additionally carries the shard's credited total and one credited-start
# count per handed module (zero allowed), credited to the module whose
# loaded suite holds the started occurrence, as in the plain driver, and
# the digests of the total and selected unit lists; the parent reconciles
# those counts and, when GITHUB_OUTPUT is set, publishes them as the
# ``credited`` output for the cross-shard per-module check, beside the
# digests.
_SHARD_DRIVER = """\
import importlib
import importlib.util
import os
import sys
import unittest

nonce = sys.stdin.readline().strip()
devnull = os.open(os.devnull, os.O_RDONLY)
os.dup2(devnull, 0)
os.close(devnull)
argv = sys.argv[1:]
if argv.count("--shard-spec") != 1:
    print("REFUSED: the shard driver needs exactly one --shard-spec",
          file=sys.stderr)
    sys.exit(2)
split = argv.index("--shard-spec")
modules = argv[:split]
tail = argv[split + 1:]
if len(tail) != 5 or tail[1] != "--tool" or tail[3] != "--weights":
    print("REFUSED: the shard driver's argv tail is not "
          "--shard-spec S --tool T --weights W", file=sys.stderr)
    sys.exit(2)
spec_text, tool_path, weights_path = tail[0], tail[2], tail[4]
on_disk = sorted(
    "tests." + entry.name[:-3]
    for entry in os.scandir("tests")
    if entry.is_file(follow_symlinks=False)
    and entry.name.startswith("test_") and entry.name.endswith(".py"))
if sorted(modules) != on_disk:
    print("REFUSED: shard driver argv modules %s do not match on-disk "
          "tests/test_*.py files %s" % (sorted(modules), on_disk),
          file=sys.stderr)
    sys.exit(2)
tool_spec = importlib.util.spec_from_file_location("regression_shard_tool",
                                                   tool_path)
tool = importlib.util.module_from_spec(tool_spec)
tool_spec.loader.exec_module(tool)
verify_only = spec_text.startswith("verify/")
try:
    if verify_only:
        shard_index = 0
        shard_count = tool.parse_shard_count(spec_text[len("verify/"):])
    else:
        shard_index, shard_count = tool.parse_shard_spec(spec_text)
    weights = tool.load_shard_weights(weights_path)
except ValueError as exc:
    print("REFUSED: %s" % exc, file=sys.stderr)
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
occurrences = []
unit_of_occurrence = []
unit_keys = []
unit_sizes = {}
for name in modules:
    suite = loader.loadTestsFromName(name)
    cases = list(flatten([suite]))
    if len(cases) < 1:
        print("REFUSED: tests/%s.py contributes zero test cases"
              % name.partition(".")[2], file=sys.stderr)
        failed = True
        continue
    for key, first, last in tool.compute_units(name, cases):
        if key in unit_sizes:
            print("REFUSED: unit key %s computed twice" % key, file=sys.stderr)
            failed = True
        unit_keys.append(key)
        unit_sizes[key] = last - first + 1
        for position in range(first, last + 1):
            occurrences.append((cases[position], name))
            unit_of_occurrence.append(key)
if failed:
    sys.exit(2)
loaded_in = {}
for case, loaded_by in occurrences:
    loaded_in.setdefault(id(case), (case, set()))[1].add(loaded_by)
for case, loaded_by in loaded_in.values():
    names = sorted(loaded_by)
    if len(names) > 1:
        print("REFUSED: test case object %r is in the loaded suites of more "
              "than one module (%s); its starts cannot be credited to one "
              "module" % (case, ", ".join("tests/%s.py" % n.partition(".")[2]
                                          for n in names)), file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
selection = tool.shard_selection(unit_keys, weights, shard_count)
refusal = tool.partition_refusal(selection, unit_keys, shard_count)
if refusal is not None:
    print("REFUSED: %s" % refusal, file=sys.stderr)
    sys.exit(2)
if verify_only:
    for number in range(1, shard_count + 1):
        keys = selection[number]
        print("shard %d/%d: %d units, %d occurrences, estimated %.1f s"
              % (number, shard_count, len(keys),
                 sum(unit_sizes[key] for key in keys),
                 sum(tool.effective_weight(weights, key) for key in keys)),
              file=sys.stderr)
    print("REGRESSION-SHARD-SELECTION %s shards=%d units=%d occurrences=%d"
          % (nonce, shard_count, len(unit_keys), len(occurrences)),
          file=sys.stderr)
    sys.exit(0)
selected = set(selection[shard_index])
shard_occurrences = []
for position, (case, name) in enumerate(occurrences):
    key = unit_of_occurrence[position]
    if key in selected:
        shard_occurrences.append((case, key, name))
started_any = dict.fromkeys(selected, 0)
not_started_by_unit = dict.fromkeys(selected, 0)
credited = 0
# Per-module credited starts, over EVERY handed module (zero stays zero for
# a module none of this shard's units came from), so the sentinel reports a
# complete per-module row the CI summary can sum across shards.
credited_by_module = dict.fromkeys(modules, 0)
class ShardResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_occurrence = 0
        self.class_skips = {}
        self.last_record = None
        self.not_started = 0
    def settle(self, upto):
        previous = None
        covered = False
        for position in range(self.next_occurrence, upto):
            case, key, _name = shard_occurrences[position]
            if case.__class__ is not previous:
                holder = unittest.util.strclass(case.__class__)
                covered = self.class_skips.get(holder, 0) > 0
                if covered:
                    self.class_skips[holder] -= 1
                previous = case.__class__
            if covered:
                self.not_started += 1
                not_started_by_unit[key] += 1
        self.next_occurrence = upto
        self.class_skips.clear()
    def addSkip(self, test, reason):
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
            self.last_record = None
        super().addSkip(test, reason)
    def startTest(self, test):
        global credited
        self.last_record = None
        for position in range(self.next_occurrence, len(shard_occurrences)):
            case, key, name = shard_occurrences[position]
            if case is test:
                self.settle(position)
                self.next_occurrence = position + 1
                started_any[key] += 1
                if not getattr(test.__class__, "__unittest_skip__", False):
                    credited += 1
                    credited_by_module[name] += 1
                break
        super().startTest(test)
suite = unittest.TestSuite(case for case, _key, _name in shard_occurrences)
runner = unittest.TextTestRunner(resultclass=ShardResult)
result = runner.run(suite)
result.settle(len(shard_occurrences))
if result.wasSuccessful():
    for key in selection[shard_index]:
        expected = unit_sizes[key]
        if started_any[key] + not_started_by_unit[key] != expected:
            print("REFUSED: unit %s: %d occurrences loaded, %d reached "
                  "startTest and %d are accounted by setUpClass skips; a "
                  "selected test did not run" % (key, expected,
                  started_any[key], not_started_by_unit[key]),
                  file=sys.stderr)
            failed = True
    if not failed and credited < 1:
        print("REFUSED: shard %d/%d ran zero credited tests (no start outside "
              "a skip-decorated class)" % (shard_index, shard_count),
              file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
print("REGRESSION-SHARD-RESULT %s shard=%d/%d testsRun=%d notStarted=%d "
      "wasSuccessful=%s selected=%d units=%d unitset=%s selection=%s "
      "credited=%d %s"
      % (nonce, shard_index, shard_count, result.testsRun, result.not_started,
         result.wasSuccessful(), len(shard_occurrences), len(selected),
         tool.unit_set_digest(unit_keys),
         tool.unit_set_digest(selection[shard_index]), credited,
         " ".join("%s=%d" % (name, credited_by_module[name])
                  for name in sorted(credited_by_module))),
      file=sys.stderr)
sys.exit(0 if result.wasSuccessful() else 1)
"""

# The shard run's completion sentinel and verify mode's selection sentinel.
# The credited tail mirrors the plain sentinel's per-module counts: credited
# starts for EVERY handed module (zero allowed), summed by the CI summary's
# reconcile step across shards.
_SHARD_SENTINEL = re.compile(
    r"^REGRESSION-SHARD-RESULT (?P<nonce>[0-9a-f]{32}) "
    r"shard=(?P<index>\d+)/(?P<count>\d+) testsRun=(?P<ran>\d+) "
    r"notStarted=(?P<notstarted>\d+) wasSuccessful=(?P<ok>True|False) "
    r"selected=(?P<selected>\d+) units=(?P<units>\d+) "
    r"unitset=(?P<unitset>[0-9a-f]{64}) selection=(?P<selection>[0-9a-f]{64}) "
    r"credited=(?P<credited>\d+)(?P<counts>( [A-Za-z0-9_.]+=\d+)*)$")

# The GITHUB_OUTPUT heredoc delimiter for the per-module credited counts. The
# counts' lines are "tests.<name>: <int>" (module names match the sentinel's
# [A-Za-z0-9_.]+ tokens), so no counts line can equal the delimiter. The two
# digest outputs are single-line: the sha256 of the shard's total unit set
# and of its selected units (unit_set_digest).
_CREDITED_OUTPUT_NAME = "credited"
_CREDITED_OUTPUT_DELIMITER = "GRC-CREDITED-COUNTS"
_UNIT_SET_OUTPUT_NAME = "units_sha256"
_SELECTED_OUTPUT_NAME = "selected_sha256"
_SELECTION_SENTINEL = re.compile(
    r"^REGRESSION-SHARD-SELECTION (?P<nonce>[0-9a-f]{32}) "
    r"shards=(?P<count>\d+) units=(?P<units>\d+) occurrences=(?P<occ>\d+)$")


def _refuse(lines: list[str], message: str) -> int:
    """Print a refusal on its own line, as main()'s refuse does."""
    if lines and not lines[-1].endswith("\n"):
        sys.stderr.write("\n")
    print("REFUSED: " + message, file=sys.stderr)
    return 2


def _run_shard_driver(spec_text: str, repo_root: Path, popen):
    """Spawn the shard driver; (returncode, stderr lines, nonce).

    Mirrors main(): discovery and the completeness self-check run here
    in the parent, the nonce travels over the child's stdin, and the
    child's stderr streams through while being accumulated. On a parent
    refusal the lines are None and the returncode is 2.
    """
    modules = discover_test_modules(repo_root)
    refusal = completeness_refusal(modules, repo_root)
    if refusal is not None:
        print("REFUSED: " + refusal, file=sys.stderr)
        return 2, None, "", []
    print("Running test modules:")
    for name in modules:
        print("  " + name)
    sys.stdout.flush()
    nonce = secrets.token_hex(16)
    proc = popen(
        [sys.executable, "-c", _SHARD_DRIVER, *modules,
         "--shard-spec", spec_text,
         "--tool", str(Path(__file__).resolve()),
         "--weights", str(Path(repo_root) / WEIGHTS_RELATIVE_PATH)],
        cwd=str(repo_root),
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.stdin.write((nonce + "\n").encode("ascii"))
    proc.stdin.close()
    lines: list[str] = []
    for raw in proc.stderr:
        line = raw.decode("utf-8", "replace")
        sys.stderr.write(line)
        sys.stderr.flush()
        lines.append(line)
    returncode = proc.wait()
    proc.stderr.close()
    return returncode, lines, nonce, modules


def _shard_sentinel_counts(last_line: str) -> dict[str, int]:
    """The per-module credited counts of a MATCHING shard sentinel."""
    match = _SHARD_SENTINEL.match(last_line)
    counts: dict[str, int] = {}
    for token in match.group("counts").split():
        name, _, value = token.partition("=")
        counts[name] = int(value)
    return counts


def _shard_sentinel_refusal(last_line: str, nonce: str, index: int,
                            count: int, modules: list[str]) -> str | None:
    """Refusal message when ``last_line`` is not a believable shard sentinel."""
    match = _SHARD_SENTINEL.match(last_line)
    if match is None:
        return ("the child's last stderr line is not the shard driver's "
                "completion sentinel; completion is established only from "
                "the executed suite's own result")
    if match.group("nonce") != nonce:
        return "the shard sentinel does not carry this run's nonce"
    if (int(match.group("index")), int(match.group("count"))) != (index, count):
        return ("the shard sentinel reports shard %s/%s, not the requested "
                "%d/%d" % (match.group("index"), match.group("count"),
                           index, count))
    ran = int(match.group("ran"))
    not_started = int(match.group("notstarted"))
    selected = int(match.group("selected"))
    units = int(match.group("units"))
    if units < 1 or selected < units:
        return ("the shard sentinel reports %d selected occurrences over %d "
                "units; a shard runs at least one unit with at least one "
                "occurrence each" % (selected, units))
    if ran < 1 or ran + not_started != selected:
        return ("the shard sentinel's testsRun=%d plus notStarted=%d does "
                "not equal the %d selected occurrences (with at least one "
                "test run)" % (ran, not_started, selected))
    credited = int(match.group("credited"))
    counts = _shard_sentinel_counts(last_line)
    if sorted(counts) != sorted(modules):
        return ("the shard sentinel's per-module credited counts %s do not "
                "name exactly the handed modules %s"
                % (sorted(counts), sorted(modules)))
    if credited < 1 or sum(counts.values()) != credited or credited > ran:
        return ("the shard sentinel's per-module credited counts sum to %d, "
                "which does not reconcile with credited=%d and testsRun=%d "
                "(at least one credited start, summing exactly, never more "
                "than the started tests)"
                % (sum(counts.values()), credited, ran))
    if match.group("ok") != "True":
        return ("the child exited 0 but its own result reports "
                "wasSuccessful=False")
    return None


def _shard_sentinel_digests(last_line: str) -> tuple[str, str]:
    """(total unit-set digest, selected-unit digest) of a MATCHING shard
    sentinel."""
    match = _SHARD_SENTINEL.match(last_line)
    return match.group("unitset"), match.group("selection")


def _write_credited_output(counts: dict[str, int],
                           digests: tuple[str, str]) -> str | None:
    """Append the shard's outputs to the GITHUB_OUTPUT file: the
    per-module credited counts and the two unit-list digests.

    No-op (None) when GITHUB_OUTPUT is unset or empty. Returns a refusal
    message when the file cannot be written: in CI (and in the pre-push
    guard's local shards) the outputs ARE the shard's contribution to the
    per-module reconciliation and unit-set agreement, so losing them
    silently would hollow those checks out. ``credited`` is block-style
    ``module: count`` lines, every handed module present (zero allowed),
    sorted by module name; ``units_sha256`` and ``selected_sha256`` are
    the 64-hex digests.
    """
    target = os.environ.get("GITHUB_OUTPUT")
    if not target:
        return None
    lines = "".join("%s: %d\n" % (name, counts[name])
                    for name in sorted(counts))
    payload = ("%s=%s\n%s=%s\n%s<<%s\n%s%s\n"
               % (_UNIT_SET_OUTPUT_NAME, digests[0],
                  _SELECTED_OUTPUT_NAME, digests[1],
                  _CREDITED_OUTPUT_NAME, _CREDITED_OUTPUT_DELIMITER,
                  lines, _CREDITED_OUTPUT_DELIMITER))
    try:
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(payload)
    except OSError as exc:
        return ("cannot append the per-module credited counts to "
                "GITHUB_OUTPUT (%s): %s" % (target, exc))
    return None


def shard_main(index: int, count: int, repo_root: Path = REPO_ROOT,
               popen=subprocess.Popen) -> int:
    """Run shard ``index`` of ``count``; forwarded unittest exit code."""
    returncode, lines, nonce, modules = _run_shard_driver(
        "%d/%d" % (index, count), repo_root, popen)
    if lines is None:
        return returncode
    if returncode == 0:
        stderr_text = "".join(lines)
        counts = _SUMMARY_LINE.findall(stderr_text)
        if not counts or int(counts[-1]) < 1:
            return _refuse(lines, "unittest exited 0 without a 'Ran N tests' "
                                  "line with N at least 1; not a believable "
                                  "green shard run")
        last_line = lines[-1].rstrip("\n") if lines else ""
        message = _shard_sentinel_refusal(last_line, nonce, index, count,
                                          modules)
        if message is not None:
            return _refuse(lines, message)
        message = _write_credited_output(_shard_sentinel_counts(last_line),
                                         _shard_sentinel_digests(last_line))
        if message is not None:
            return _refuse(lines, message)
    return returncode


def verify_shards_main(count: int, repo_root: Path = REPO_ROOT,
                       popen=subprocess.Popen) -> int:
    """Check the ``count``-way selection without running a test."""
    returncode, lines, nonce, _modules = _run_shard_driver("verify/%d" % count,
                                                           repo_root, popen)
    if lines is None:
        return returncode
    if returncode == 0:
        last_line = lines[-1].rstrip("\n") if lines else ""
        match = _SELECTION_SENTINEL.match(last_line)
        if match is None:
            return _refuse(lines, "the child's last stderr line is not the "
                                  "shard driver's selection sentinel")
        if match.group("nonce") != nonce:
            return _refuse(lines, "the selection sentinel does not carry "
                                  "this run's nonce")
        if int(match.group("count")) != count:
            return _refuse(lines, "the selection sentinel reports %s shards, "
                                  "not the requested %d"
                                  % (match.group("count"), count))
        if int(match.group("units")) < 1 or (int(match.group("occ"))
                                             < int(match.group("units"))):
            return _refuse(lines, "the selection sentinel reports no units")
    return returncode


def cli(argv: list[str] | None = None) -> int:
    """Dispatch: no argument runs the whole gate, as every runner surface
    invokes it; ``--shard I/K`` and ``--verify-shards K`` are the CI shard
    modes. Anything else is a refusal (exit 2), never a silent full run."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        return main()
    try:
        if argv[0] == "--shard" and len(argv) == 2:
            index, count = parse_shard_spec(argv[1])
            return shard_main(index, count)
        if argv[0] == "--verify-shards" and len(argv) == 2:
            return verify_shards_main(parse_shard_count(argv[1]))
    except ValueError as exc:
        print("REFUSED: " + str(exc), file=sys.stderr)
        return 2
    print("REFUSED: usage: run-linter-regression.py [--shard I/K | "
          "--verify-shards K] (no other argument)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(cli())
