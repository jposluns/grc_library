#!/usr/bin/env python3
"""Measure wall seconds per unit of the linter regression test suite.

PR 1 of the gate 36 split plan (backlog item 3b789): before the suite
can be split across parallel CI jobs, the split needs per-unit timings.
This tool runs the regression suite's test modules in one process,
times each unit, and writes ``tests/regression-shard-weights.json``,
the weights file the planned ``--shard`` mode of
``tools/run-linter-regression.py`` will read to balance the shards.
Weights only affect where a test would run, never whether it runs; this
tool changes no gate. No gate surface runs it: the gate inventory in
the audit-programme specification
(``governance/specification-audit-programme.md``, section 6),
``.github/workflows/quality.yml``, ``tools/run_all_audits.sh`` and the
pre-commit configuration do not list it. Like every ``tools/`` file it
has an ordinary inventory pin row in ``ExplicitPathCliInventoryTests``
(``tests/test_linters.py``), which pins its bytes and path policy
without running it. The dispatch-only workflow
``.github/workflows/regression-timings.yml`` runs it on a CI runner and
uploads the JSON as a workflow artefact.

A UNIT is a maximal run of consecutive occurrences of one class object
within one module's loaded suite, flattened in suite order, so a unit
keeps ``setUpClass`` once per class, exactly as one unittest run of the
module does. A case that is not a ``unittest.TestCase`` instance is its
own unit. The unit key is ``module:qualname#ordinal``: ``qualname`` is
the case's class ``__qualname__``, and ``ordinal`` counts that module's
units of the same qualname in flattened suite order, from 0, so a class
whose occurrences fall into two separate runs gives two units (``#0``
and ``#1``), and two distinct class objects sharing a qualname
(factory-built classes) are likewise told apart by the ordinal.

Timing: a unit's wall seconds run from the previous unit's last
recorded ``stopTest`` (or the start of the module's run) to this unit's
last recorded ``stopTest``. A unit therefore includes its own
``setUpClass`` and ``setUp``/``tearDown`` overhead plus the previous
unit's ``tearDownClass``; a unit none of whose tests reached
``stopTest`` (for example a ``setUpClass`` that raised ``SkipTest``)
records 0.0, and its skip handling is absorbed by the next recorded
unit. These are advisory weights for shard balance, never a gate
result: a failing test is timed like a passing one, and the weights
file is still written when a module's run fails (the exit code reports
the failure). The regression gate itself is unchanged and stays the
only authority on whether the suite passes.

Refusals (exit 2, naming the offender, no weights file written): a
module name outside the discovered top-level ``tests/test_*.py`` set, a
duplicate module argument (the message names each duplicated module), a
module whose import raises (any ``BaseException``; each module is
imported explicitly with ``importlib.import_module`` before its tests
are loaded, as the gate's driver imports, because unittest's loader
would otherwise swallow the raise into a synthetic failed case), a
module whose loaded suite still contains a synthetic failed-import or
failed-load case, and a module that loads zero test cases.

Usage:
    python3 tools/measure-regression-timings.py
    python3 tools/measure-regression-timings.py tests.test_session_facts
    python3 tools/measure-regression-timings.py --output weights.json
    python3 tools/measure-regression-timings.py --self-test

With no module arguments it measures every discovered module in the
same sorted order the regression gate runs them. Module arguments are
dotted module names from that discovered set (selection keys, not
filesystem paths); ``--output`` names the file to write (default
``tests/regression-shard-weights.json``); a relative ``--output`` is
resolved against the invoker's working directory before the tool
changes directory to the repository root. The JSON holds a schema
version and one ``units`` object mapping each unit key to its measured
seconds, serialized with sorted keys, two-space indentation and a
trailing newline, so reruns differ only where timings differ.

Exit codes: 0 every measured module ran green and the file was
written; 1 at least one module's run was not successful (the file is
still written) or the self-test failed; 2 a refusal.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "tests" / "regression-shard-weights.json"
SCHEMA_VERSION = 1


class Refusal(Exception):
    """A condition the tool refuses to measure through (exit 2)."""


def discover_test_modules(repo_root: Path = REPO_ROOT) -> list[str]:
    """Every top-level tests/test_*.py as a dotted module name, sorted.

    Mirrors tools/run-linter-regression.py's discovery, so the measured
    population is the gate's population.
    """
    return sorted(
        "tests." + path.stem
        for path in (repo_root / "tests").glob("test_*.py")
    )


def module_label(name: str) -> str:
    """The gate's file form of a module name, for refusal messages."""
    if name.startswith("tests."):
        return "tests/%s.py" % name.partition(".")[2]
    return name


def flatten(suite):
    """Yield every case of a suite in flattened (run) order."""
    for item in suite:
        if isinstance(item, unittest.suite.BaseTestSuite):
            yield from flatten(item)
        else:
            yield item


def unit_key(module: str, qualname: str, ordinal: int) -> str:
    """The unit key the plan's shard rule defines: module:qualname#ordinal."""
    return "%s:%s#%d" % (module, qualname, ordinal)


def compute_units(module: str, cases: list) -> list[tuple[str, int, int]]:
    """Group a module's flattened cases into units.

    Returns ``[(key, first_index, last_index), ...]`` in suite order. A
    unit is a maximal run of consecutive occurrences of one class
    object; a case that is not a ``unittest.TestCase`` instance is its
    own unit. Ordinals count units per qualname within the module, from
    0, so every returned key is unique within the module.
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
            units.append([unit_key(module, qualname, ordinal), index, index])
        previous = type(case) if grouped else None
    return [tuple(unit) for unit in units]


def load_module_suite(name: str) -> unittest.TestSuite:
    """Load one module's suite; refuse an import error or zero cases.

    The module is imported explicitly first, as the gate's driver
    imports it: ``loadTestsFromName`` alone would swallow an import-time
    raise into a synthetic ``_FailedTest`` case, so the documented
    refusal would not happen and a phantom unit would be timed and
    written. Any synthetic failed-import or failed-load case the loader
    still produces is refused too.
    """
    try:
        importlib.import_module(name)
        suite = unittest.defaultTestLoader.loadTestsFromName(name)
    except BaseException as exc:  # the gate refuses any import-time raise
        raise Refusal("cannot import %s: %r" % (module_label(name), exc)) from exc
    synthetic = getattr(unittest.loader, "_FailedTest", ())
    for case in flatten([suite]):
        if isinstance(case, synthetic):
            raise Refusal(
                "%s loaded a synthetic failed-import or failed-load case: %s"
                % (module_label(name), case.id()))
    if suite.countTestCases() < 1:
        raise Refusal("%s contributes zero test cases" % module_label(name))
    return suite


class UnitTimingResult(unittest.TextTestResult):
    """TextTestResult that closes a unit's clock at its last stopTest.

    Starts are matched to the next pending occurrence of the same case
    object (identity, forward order), as the gate's driver matches them,
    so a case object loaded twice is timed per occurrence.
    """

    def configure(self, occurrences: list, units: list,
                  clock=time.perf_counter) -> None:
        self._occurrences = occurrences
        self._next_occurrence = 0
        self._current_index = None
        self._last_of_unit = {
            last: position for position, (_key, _first, last) in enumerate(units)
        }
        self.unit_seconds = [0.0] * len(units)
        self._clock = clock
        self._boundary = clock()

    def startTest(self, test) -> None:
        self._current_index = None
        for index in range(self._next_occurrence, len(self._occurrences)):
            if self._occurrences[index] is test:
                self._next_occurrence = index + 1
                self._current_index = index
                break
        super().startTest(test)

    def stopTest(self, test) -> None:
        super().stopTest(test)
        index = self._current_index
        self._current_index = None
        if index is not None and index in self._last_of_unit:
            now = self._clock()
            self.unit_seconds[self._last_of_unit[index]] += now - self._boundary
            self._boundary = now


class UnitTimingRunner(unittest.TextTestRunner):
    """TextTestRunner whose result times the configured units."""

    resultclass = UnitTimingResult

    def __init__(self, occurrences: list, units: list, stream=None,
                 verbosity: int = 1, clock=time.perf_counter):
        super().__init__(stream=stream, verbosity=verbosity)
        self._occurrences = occurrences
        self._units = units
        self._clock = clock

    def _makeResult(self):
        result = super()._makeResult()
        result.configure(self._occurrences, self._units, clock=self._clock)
        return result


def measure_suite(module: str, suite, stream=None, verbosity: int = 1,
                  clock=time.perf_counter):
    """Run one module's suite and time its units.

    Returns ``(units, seconds, result)``: the computed units, the
    measured wall seconds per unit (same order) and the unittest result.
    The cases list holds every occurrence alive until the run ends, so
    identity matching never meets a reused id. ``clock`` is the timer
    (default ``time.perf_counter``); a test injects a deterministic fake
    so per-unit seconds are asserted exactly, never merely nonnegative.
    """
    cases = list(flatten([suite]))
    units = compute_units(module, cases)
    runner = UnitTimingRunner(cases, units, stream=stream, verbosity=verbosity,
                              clock=clock)
    result = runner.run(suite)
    return units, list(result.unit_seconds), result


def render_weights(weights: dict[str, float]) -> str:
    """Serialize weights deterministically: schema, sorted keys, LF end."""
    payload = {
        "schema": SCHEMA_VERSION,
        "units": {key: round(value, 3) for key, value in weights.items()},
    }
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def self_test() -> int:
    """Exercise the measurement primitives on synthetic cases; 0 on pass."""
    import io
    import tempfile
    import types

    class AlphaTests(unittest.TestCase):
        def test_one(self):
            pass

        def test_two(self):
            pass

    class BetaTests(unittest.TestCase):
        def test_three(self):
            pass

    class BareCase:
        """A runnable non-TestCase test object (its own unit)."""

        def run(self, result=None):
            pass

        def countTestCases(self):
            return 1

    checks: list[tuple[str, bool]] = []
    alpha = AlphaTests.__qualname__
    beta = BetaTests.__qualname__

    checks.append((
        "unit-key construction",
        unit_key("tests.test_sample", "Outer.Inner", 2)
        == "tests.test_sample:Outer.Inner#2"))

    cases = [AlphaTests("test_one"), AlphaTests("test_two"),
             BetaTests("test_three"), AlphaTests("test_one")]
    checks.append((
        "class-run grouping with per-qualname ordinals",
        compute_units("tests.test_sample", cases) == [
            ("tests.test_sample:%s#0" % alpha, 0, 1),
            ("tests.test_sample:%s#0" % beta, 2, 2),
            ("tests.test_sample:%s#1" % alpha, 3, 3)]))

    twin_a = type("TwinTests", (unittest.TestCase,), {"test_t": lambda self: None})
    twin_b = type("TwinTests", (unittest.TestCase,), {"test_t": lambda self: None})
    checks.append((
        "two class objects sharing a qualname are two units",
        compute_units("tests.test_sample", [twin_a("test_t"), twin_b("test_t")]) == [
            ("tests.test_sample:TwinTests#0", 0, 0),
            ("tests.test_sample:TwinTests#1", 1, 1)]))

    bare_units = compute_units("tests.test_sample", [BareCase(), BareCase()])
    checks.append((
        "a non-TestCase case is its own unit",
        [unit[1:] for unit in bare_units] == [(0, 0), (1, 1)]
        and bare_units[0][0].endswith("#0") and bare_units[1][0].endswith("#1")
        and bare_units[0][0] != bare_units[1][0]))

    class StepClock:
        """A deterministic clock advancing 0.25 s per reading."""

        def __init__(self):
            self.now = 0.0

        def __call__(self):
            self.now += 0.25
            return self.now

    suite = unittest.TestSuite([AlphaTests("test_one"), AlphaTests("test_two"),
                                BetaTests("test_three")])
    units, seconds, result = measure_suite(
        "tests.test_sample", suite, stream=io.StringIO(), verbosity=0,
        clock=StepClock())
    checks.append((
        "measurement runs green and times every unit exactly (fake clock)",
        result.wasSuccessful() and result.testsRun == 3
        and [unit[0] for unit in units] == [
            "tests.test_sample:%s#0" % alpha, "tests.test_sample:%s#0" % beta]
        and seconds == [0.25, 0.25]))

    rendered = render_weights({"b:K#0": 1.23456, "a:K#0": 0.5})
    checks.append((
        "weights JSON shape (schema, sorted keys, stable formatting)",
        rendered == ('{\n'
                     '  "schema": 1,\n'
                     '  "units": {\n'
                     '    "a:K#0": 0.5,\n'
                     '    "b:K#0": 1.235\n'
                     '  }\n'
                     '}\n')))
    with tempfile.TemporaryDirectory() as scratch:
        out = Path(scratch) / "weights.json"
        out.write_text(rendered, encoding="utf-8")
        checks.append((
            "weights JSON round-trip",
            json.loads(out.read_text(encoding="utf-8")) == {
                "schema": 1, "units": {"a:K#0": 0.5, "b:K#0": 1.235}}))

    empty_name = "measure_regression_timings_selftest_empty"
    sys.modules[empty_name] = types.ModuleType(empty_name)
    try:
        try:
            load_module_suite(empty_name)
            refused = False
        except Refusal as refusal:
            refused = "zero test cases" in str(refusal)
    finally:
        del sys.modules[empty_name]
    checks.append(("zero-test module refused", refused))

    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print("%s: %s" % ("PASS" if passed else "FAIL", name))
    if failed:
        print("self-test FAILED: %d of %d checks" % (len(failed), len(checks)),
              file=sys.stderr)
        return 1
    print("OK: self-test passed (%d checks)" % len(checks))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Measure wall seconds per unit of the linter regression "
                    "test suite and write the shard-weights JSON.")
    parser.add_argument(
        "modules", nargs="*", metavar="MODULE",
        help="dotted test module names from the discovered top-level "
             "tests/test_*.py set (default: all of them)")
    parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT),
        help="weights file to write (default: tests/regression-shard-weights.json)")
    parser.add_argument(
        "--self-test", action="store_true",
        help="run the built-in checks on synthetic cases and exit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    # Resolve --output against the invoker's working directory before the
    # chdir to the repository root below, so a relative path lands where
    # the invoker ran the tool, not in the repository root.
    output = Path(os.path.abspath(args.output))
    try:
        discovered = discover_test_modules()
        if not discovered:
            raise Refusal(
                "no tests/test_*.py files found under %s" % (REPO_ROOT / "tests"))
        selected = list(args.modules) or discovered
        for name in selected:
            if name not in discovered:
                raise Refusal(
                    "unknown test module %r; expected dotted names from: %s"
                    % (name, ", ".join(discovered)))
        seen: set[str] = set()
        duplicates: list[str] = []
        for name in selected:
            if name in seen and name not in duplicates:
                duplicates.append(name)
            seen.add(name)
        if duplicates:
            raise Refusal(
                "duplicate module argument %s; each module is measured once"
                % ", ".join(repr(name) for name in duplicates))
        # The suite runs in-process, from the repository root, with the
        # root importable, as the gate's child driver runs it.
        if str(REPO_ROOT) not in sys.path:
            sys.path.append(str(REPO_ROOT))
        os.chdir(REPO_ROOT)
        weights: dict[str, float] = {}
        failures: list[str] = []
        for name in selected:
            suite = load_module_suite(name)
            units, seconds, result = measure_suite(name, suite)
            for (key, _first, _last), value in zip(units, seconds):
                weights[key] = value
            print("%s: %d units, %d tests run, %.3f s, wasSuccessful=%s"
                  % (name, len(units), result.testsRun, sum(seconds),
                     result.wasSuccessful()))
            sys.stdout.flush()
            if not result.wasSuccessful():
                failures.append(name)
        output.write_text(render_weights(weights), encoding="utf-8")
        print("Wrote %s (%d units, schema %d)"
              % (output, len(weights), SCHEMA_VERSION))
    except Refusal as refusal:
        print("REFUSED: " + str(refusal), file=sys.stderr)
        return 2
    if failures:
        print("FAILED modules: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
