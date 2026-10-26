"""Gate 36 regression-gate guard tests (the 3b525 round-2/round-3 findings).

These tests guard the gate runner itself, so they live OUTSIDE
``tests/test_linters.py``: a discovery or run-list regression that
drops ``tests/test_linters.py`` (which hosts most other guards,
including the runner's sha256 inventory pin and the reciprocal
executed-argv check) cannot also drop this module's completeness
check. The runner additionally carries its own in-process completeness
self-check, the child driver repeats that check against its own argv,
and completion is established from the child's executed suite through
a nonce-carrying sentinel; these tests exercise those checks and the
runner's refusal paths hermetically, against synthetic
repository-shaped trees, an injected child runner and a scrubbed
environment, so no flip can pass by skipping execution and no ambient
variable can make a refusal assertion pass vacuously.
"""

from __future__ import annotations

import contextlib
import io
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNNER_PATH = REPO_ROOT / "tools" / "run-linter-regression.py"

# One real passing test, so a synthetic module survives the driver's
# zero-test-cases refusal.
PASSING_MODULE = """\
import unittest


class PassingTests(unittest.TestCase):
    def test_passes(self):
        self.assertTrue(True)
"""

FAILING_MODULE = """\
import unittest


class FailingTests(unittest.TestCase):
    def test_fails(self):
        self.fail("this test must be reached, or the run must be refused")
"""

# The round-3 review's forgery reproducer (3b525 F1): a load_tests that
# scrapes the passive channels (argv, stdin), prints a green summary
# plus a sentinel forged from the best nonce candidate it found, and
# exits 0 before a failing sibling can run. With the nonce delivered
# over stdin and consumed before any test module is imported, no 32-hex
# candidate is visible TO THIS SCRAPE, so the forged sentinel cannot
# carry this run's nonce; with the nonce on argv (the flip), the
# forgery would succeed. The nonce stays recoverable from the driver's
# own __main__ globals: see MAIN_NONCE_FORGING_MODULE below.
FORGING_MODULE = """\
import sys
import unittest


class ForgeTests(unittest.TestCase):
    def test_forge(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    seen = list(sys.argv[1:])
    try:
        seen.append(sys.stdin.read().strip())
    except (OSError, ValueError):
        pass
    hexdigits = set("0123456789abcdef")
    token = next(
        (s for s in seen if len(s) == 32 and set(s) <= hexdigits),
        seen[0] if seen else "nononce")
    modules = sorted(s for s in seen if s.startswith("tests."))
    sys.stderr.write("Ran %d tests in 0.001s\\n\\nOK\\n" % len(modules))
    sys.stderr.write(
        "REGRESSION-GATE-RESULT %s testsRun=%d notStarted=0 "
        "wasSuccessful=True %s\\n"
        % (token, len(modules),
           " ".join("%s=1" % name for name in modules)))
    raise SystemExit(0)
"""

# The round-4 review's forgery reproducer (3b525 round 4, F1): the
# driver is a python -c script, so the nonce it reads from stdin is a
# module-level global of __main__ for the life of the child. A
# load_tests that imports __main__ recovers it and forges a complete
# green sentinel, exiting 0 before a failing sibling runs. This is a
# DOCUMENTED ACCEPTED RESIDUAL (in-process secrecy is unattainable; the
# maintainer has a pending decision on whether gates must defend
# against deliberately adversarial in-process code), asserted as such
# by test_main_accepts_main_nonce_forgery_residual below.
MAIN_NONCE_FORGING_MODULE = """\
import sys
import unittest


class ForgeTests(unittest.TestCase):
    def test_forge(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    import __main__
    nonce = __main__.nonce
    modules = sorted(s for s in sys.argv[1:] if s.startswith("tests."))
    sys.stderr.write("Ran %d tests in 0.001s\\n\\nOK\\n" % len(modules))
    sys.stderr.write(
        "REGRESSION-GATE-RESULT %s testsRun=%d notStarted=0 "
        "wasSuccessful=True %s\\n"
        % (nonce, len(modules),
           " ".join("%s=1" % name for name in modules)))
    raise SystemExit(0)
"""

# setUpClass raises SkipTest (3b525 round 3, F4): both tests are loaded
# but neither reaches startTest, so testsRun undercounts the loaded
# suite by two while unittest itself reports the run green.
SKIPPING_CLASS_MODULE = """\
import unittest


class SkippedClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_first_never_starts(self):
        self.fail("must not start")

    def test_second_never_starts(self):
        self.fail("must not start")
"""

# setUpModule raises SkipTest: the module's one test never starts.
SKIPPING_MODULE_MODULE = """\
import unittest


def setUpModule():
    raise unittest.SkipTest("environment-dependent module skipped")


class SkippedModuleTests(unittest.TestCase):
    def test_never_starts(self):
        self.fail("must not start")
"""

# A module that otherwise ran (3b525 round 8, W1): one class is skipped
# in setUpClass (two tests never start), while the other class starts
# both of its tests, one of which is skipped individually and so still
# counts as started. Loaded 4, started 2, notStarted 2.
PARTLY_SKIPPED_MODULE = """\
import unittest


class SkippedClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_first_never_starts(self):
        self.fail("must not start")

    def test_second_never_starts(self):
        self.fail("must not start")


class RunningTests(unittest.TestCase):
    def test_runs(self):
        self.assertTrue(True)

    @unittest.skip("individually skipped: still started")
    def test_individually_skipped(self):
        self.fail("must not run")
"""

# Its own class is skipped in setUpClass, while it imports a passing
# class defined in tests/test_zz_ok.py (3b525 round-8 review, W1). A
# started test is credited to the module whose loaded suite contains it,
# so this module earns credit for the imported class: the documented
# borrowing residual (no current module does this).
BORROWING_MODULE = """\
import unittest

from tests.test_zz_ok import PassingTests


class SkippedClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")
"""

# Legitimate modules whose tests are not plain classes they define
# (3b525 round-9 and round-10 reviews): each started test is in the
# module's own loaded suite, so each module must be credited.
# FunctionTestCase's type is defined in unittest.case.
FUNCTION_TEST_CASE_MODULE = """\
import unittest


def check_runs():
    assert True


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([unittest.FunctionTestCase(check_runs)])
"""

# A doctest case's type is defined in doctest.
DOCTEST_SUITE_MODULE = """\
import doctest


def double(value):
    \"\"\"
    >>> double(2)
    4
    \"\"\"
    return value * 2


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite(__name__))
    return tests
"""

# Doctests of a library module outside tests/ (round-10 review: refused
# under defining-code crediting, whose globals name the library).
DOCTEST_LIBRARY = """\
def triple(value):
    \"\"\"
    >>> triple(2)
    6
    \"\"\"
    return value * 3
"""

DOCTEST_LIBRARY_MODULE = """\
import doctest


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite("doctest_library"))
    return tests
"""

# A doctest file found relative to a package (round-10 review: refused).
DOCFILE_TEXT = """\
>>> 1 + 1
2
"""

DOCFILE_SUITE_MODULE = """\
import doctest


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocFileSuite("docfile_example.txt",
                                        package="tests"))
    return tests
"""

# A FunctionTestCase wrapping a functools.partial, which has no
# __module__ of its own (round-10 review: refused). The partial is given
# a __name__ only because unittest's own FunctionTestCase.__str__ reads
# it (without one, unittest itself errors while recording the duration).
PARTIAL_MODULE = """\
import functools
import unittest


def check_double(value, expected):
    assert value * 2 == expected


def load_tests(loader, tests, pattern):
    check = functools.partial(check_double, 2, 4)
    check.__name__ = "check_double_2_4"
    return unittest.TestSuite([unittest.FunctionTestCase(check)])
"""

# A load_tests that returns one test on the driver's own load and two on
# unittest.main's load: the suites no longer pair with the loaded
# counts, so the driver refuses rather than credit by guesswork.
PAIRING_MISMATCH_MODULE = """\
import unittest

_loads = []


class PairingTests(unittest.TestCase):
    def test_one(self):
        self.assertTrue(True)

    def test_two(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    _loads.append(None)
    if len(_loads) == 1:
        return unittest.TestSuite([PairingTests("test_one")])
    return tests
"""

# A class factory in a helper module outside the run list: the built
# class's __module__ names the helper, its test method this module.
HELPER_FACTORY = """\
import unittest


def make_case(name, **methods):
    return type(name, (unittest.TestCase,), methods)
"""

HELPER_FACTORY_MODULE = """\
from tests.helper_factory import make_case


def _test_runs(self):
    self.assertTrue(True)


FactoryTests = make_case("FactoryTests", test_runs=_test_runs)
"""

# A helper outside the run list that defines its class's test methods
# itself: a handed module that only imports that class earns credit for
# it (the borrowing residual).
HELPER_SHARED = """\
import unittest


class SharedTests(unittest.TestCase):
    def test_shared(self):
        self.assertTrue(True)
"""

HELPER_BORROWING_MODULE = """\
from tests.helper_shared import SharedTests
"""

# A test object of no known case type, defined in a helper outside the
# run list and loaded by a handed module's load_tests: it is in that
# module's loaded suite, so that module is credited.
HELPER_PROBE = """\
class ProbeCase:
    def countTestCases(self):
        return 1

    def id(self):
        return "tests.helper_probe.ProbeCase"

    def shortDescription(self):
        return None

    def __str__(self):
        return self.id()

    def __call__(self, result):
        result.startTest(self)
        result.addSuccess(self)
        result.stopTest(self)
"""

UNKNOWN_CASE_TYPE_MODULE = """\
import unittest

from tests.helper_probe import ProbeCase


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([ProbeCase()])
"""

# A helper outside the run list whose setUpModule raises SkipTest
# (3b525 round-9 review, N2): its class, imported into a handed module
# that also runs its own class, never starts, and no skip holder is
# counted for it, so the parent's reconciliation refuses the run.
HELPER_MODULE_SKIP = """\
import unittest


def setUpModule():
    raise unittest.SkipTest("helper module skipped")


class HelperSkippedTests(unittest.TestCase):
    def test_never_starts(self):
        self.fail("must not start")
"""

HELPER_MODULE_SKIP_IMPORTING_MODULE = """\
import unittest

from tests.helper_moduleskip import HelperSkippedTests


class RunningTests(unittest.TestCase):
    def test_runs(self):
        self.assertTrue(True)
"""

# The module's only class is skipped by a class decorator (3b525
# round-8 review, N1): unittest calls startTest for each of its tests
# before reading the class flag, yet the class is skipped as a whole.
DECORATOR_SKIPPED_CLASS_MODULE = """\
import unittest


@unittest.skip("whole class skipped by decorator")
class DecoratedSkipTests(unittest.TestCase):
    def test_never_runs(self):
        self.fail("must not run")
"""

DECORATOR_SKIPUNLESS_FALSE_MODULE = """\
import unittest


@unittest.skipUnless(False, "whole class skipped by skipUnless(False)")
class DecoratedSkipUnlessTests(unittest.TestCase):
    def test_never_runs(self):
        self.fail("must not run")
"""

# A decorator-skipped class beside a class that runs: the module started
# a test, so it is not refused; the decorated class's test still reaches
# startTest, so testsRun counts it and notStarted stays 0.
DECORATOR_SKIPPED_BESIDE_RUNNING_MODULE = """\
import unittest


@unittest.skip("whole class skipped by decorator")
class DecoratedSkipTests(unittest.TestCase):
    def test_never_runs(self):
        self.fail("must not run")


class RunningTests(unittest.TestCase):
    def test_runs(self):
        self.assertTrue(True)
"""

# A fixture that raises an error, not SkipTest (3b525 round-8 review,
# N2): the run fails on unittest's own terms and keeps its exit 1.
ERRORING_SETUPMODULE_MODULE = """\
import unittest


def setUpModule():
    raise RuntimeError("module fixture broke")


class ErroringModuleTests(unittest.TestCase):
    def test_never_starts(self):
        self.fail("must not start")
"""

ERRORING_SETUPCLASS_MODULE = """\
import unittest


class ErroringClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise RuntimeError("class fixture broke")

    def test_never_starts(self):
        self.fail("must not start")
"""

# One case OBJECT in two handed modules' suites (3b525 round-11 review,
# codex E1): a helper's module-level case loaded by two modules. Round
# 12 credited each module per occurrence; round 13 refuses the shared
# object before the run, naming both modules, because forward matching
# across modules could credit the wrong one (round-12 review, codex E1
# and E2).
HELPER_SHARED_CASE = """\
import unittest


class SharedCaseTests(unittest.TestCase):
    def test_shared(self):
        self.assertTrue(True)


SHARED = SharedCaseTests("test_shared")
"""

SHARED_CASE_MODULE = """\
import unittest

from tests.helper_sharedcase import SHARED


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([SHARED])
"""

# One case object in two handed modules' suites whose class's setUpClass
# skips on its second call (3b525 round-11 review, codex E2): the first
# module's occurrence starts, the second's never does. Crediting by case
# object gave the first module's start to the second module, and a
# helper test that a setUpModule skip keeps from starting (counted by
# no holder) offset the per-class notStarted overcount, so that run
# reconciled and passed. Round 13 refuses it before the run: the case
# object is in both modules' suites.
HELPER_SHARED_ONCE = """\
import unittest


class SharedOnceTests(unittest.TestCase):
    setups = 0

    @classmethod
    def setUpClass(cls):
        cls.setups += 1
        if cls.setups > 1:
            raise unittest.SkipTest("second set-up skipped")

    def test_shared(self):
        self.assertTrue(True)


SHARED = SharedOnceTests("test_shared")
"""

SHARED_ONCE_FIRST_MODULE = """\
import unittest

from tests.helper_moduleskip import HelperSkippedTests
from tests.helper_sharedonce import SHARED


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([SHARED, OwnTests("test_own"),
                               HelperSkippedTests("test_never_starts")])
"""

SHARED_ONCE_SECOND_MODULE = """\
import unittest

from tests.helper_sharedonce import SHARED


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([SHARED])
"""

# A class whose setUpClass raises SkipTest, loaded twice in one module
# around a running class (3b525 round-11 review, codex E3): setUpClass
# runs, and skips, once per stretch, so counting the class's loaded
# tests per skip record gave notStarted=4 for this three-case suite.
SKIPPED_CLASS_LOADED_TWICE_MODULE = """\
import unittest


class SkippedClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


class RunningTests(unittest.TestCase):
    def test_runs(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([SkippedClassTests("test_never_starts"),
                               RunningTests("test_runs"),
                               SkippedClassTests("test_never_starts")])
"""

# unittest reads the class skip flag from test.__class__, not type(test)
# (3b525 round-11 review, claude N4). Here a __class__ property hides a
# skip-decorated class behind a plain type: unittest skips the test,
# so it is not a credited start.
CLASS_PROPERTY_HIDES_SKIP_MODULE = """\
import unittest


@unittest.skip("whole class skipped by decorator")
class HiddenSkippedTests(unittest.TestCase):
    pass


class DisguisedTests(unittest.TestCase):
    @property
    def __class__(self):
        return HiddenSkippedTests

    def test_never_runs(self):
        self.fail("must not run")
"""

# The converse: the skip flag is on the type only, and __class__ names a
# plain class, so unittest runs the test and it is a credited start.
CLASS_PROPERTY_HIDES_PLAIN_MODULE = """\
import unittest


class PlainTests(unittest.TestCase):
    pass


@unittest.skip("flag on the type only; unittest reads __class__")
class DecoratedTypeTests(unittest.TestCase):
    @property
    def __class__(self):
        return PlainTests

    def test_runs(self):
        self.assertTrue(True)
"""

# A load_tests returning a bare BaseTestSuite (3b525 round-11 review,
# claude W2): flatten must descend into any BaseTestSuite, not only
# unittest.TestSuite, or the case inside is never matched to a start.
BASE_TEST_SUITE_MODULE = """\
import unittest


class BaseSuiteTests(unittest.TestCase):
    def test_runs(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.suite.BaseTestSuite([BaseSuiteTests("test_runs")])
"""

# A test that starts many fresh case objects itself (3b525 round-11
# review, claude W1). unittest frees a module's never-started cases
# once their sub-suite has run, so a later fresh object can take a freed
# case's id; looked up by id, such a start credited the module whose
# only test a setUpModule SkipTest had stopped. The probes are kept
# alive, so each takes a new address and the freed one is reached.
DYNAMIC_START_MODULE = """\
import unittest


class DynamicStartTests(unittest.TestCase):
    def run(self, result=None):
        probe_class = type("Probe", (unittest.TestCase,),
                           {"test_probe": lambda self: None})
        probes = []
        for _ in range(20000):
            probe = probe_class("test_probe")
            probes.append(probe)
            result.startTest(probe)
            result.stopTest(probe)
        return super().run(result)

    def test_runs(self):
        self.assertTrue(True)
"""

# Two DISTINCT but equal case objects (TestCase equality compares type
# and method name) in two modules' suites, so the shared-case refusal
# does not apply (3b525 round-12 review, claude W2 and codex W). The
# class's first setUpClass skips and its second succeeds, and a skipped
# class separates the two occurrences, so no start falls between them:
# matched by identity, the second module's start is its own; matched
# by equality, it is taken by the first module's never-started
# occurrence and the second module is refused.
HELPER_SKIP_FIRST_SETUP = """\
import unittest


class LateSetUpTests(unittest.TestCase):
    setups = 0

    @classmethod
    def setUpClass(cls):
        cls.setups += 1
        if cls.setups == 1:
            raise unittest.SkipTest("first set-up skipped")

    def test_late(self):
        self.assertTrue(True)
"""

EQUAL_CASE_FIRST_MODULE = """\
import unittest

from tests.helper_skipfirst import LateSetUpTests


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


class SkippedClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([OwnTests("test_own"),
                               LateSetUpTests("test_late"),
                               SkippedClassTests("test_never_starts")])
"""

EQUAL_CASE_SECOND_MODULE = """\
import unittest

from tests.helper_skipfirst import LateSetUpTests


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([LateSetUpTests("test_late")])
"""

# A test dropped by a standard suite whose class skipped in setUpClass
# earlier in the run (3b525 round-12 review, claude W2 and codex W): the
# helper's setUpModule skips on its second call, which no counted holder
# records, so the class's second occurrence never starts. The class's
# skip record from the first stretch must not count it: the records are
# cleared at each matched start.
HELPER_MODULE_SKIP_SECOND = """\
import unittest

setups = 0


def setUpModule():
    global setups
    setups += 1
    if setups > 1:
        raise unittest.SkipTest("second module set-up skipped")


class ClassSkipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")
"""

DROPPED_AFTER_CLASS_SKIP_MODULE = """\
import unittest

from tests.helper_modskipsecond import ClassSkipTests


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([ClassSkipTests("test_never_starts"),
                               OwnTests("test_own"),
                               ClassSkipTests("test_never_starts")])
"""

# A shared case object whose __eq__ says equal to any string (3b525
# round-13 review, codex E): kept in one list with the module names and
# tested with "in", it matched each module name, so the shared-case
# check saw one module and the run passed. The __hash__ is restored
# because overriding __eq__ alone would make the case unhashable.
HELPER_STRING_EQUAL_CASE = """\
import unittest


class StringEqualTests(unittest.TestCase):
    __hash__ = unittest.TestCase.__hash__

    def __eq__(self, other):
        if isinstance(other, str):
            return True
        return super().__eq__(other)

    def test_shared(self):
        self.assertTrue(True)


SHARED = StringEqualTests("test_shared")
"""

STRING_EQUAL_CASE_MODULE = """\
import unittest

from tests.helper_stringequal import SHARED


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([SHARED])
"""

# A plain suite in which a class skipped in setUpClass is loaded twice
# around another setUpClass-skipped class, with no start between (3b525
# round-13 review, claude W1): the helper's setUpModule skips on its
# second call, so the class's second occurrence is dropped without a
# record. Its one skip record covered both occurrences, so notStarted
# was 3 and the run passed; one record covers one class occurrence.
DROPPED_BETWEEN_CLASS_SKIPS_MODULE = """\
import unittest

from tests.helper_modskipsecond import ClassSkipTests


class SkipSetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([ClassSkipTests("test_never_starts"),
                               SkipSetupTests("test_never_starts"),
                               ClassSkipTests("test_never_starts"),
                               OwnTests("test_own")])
"""

# Two distinct classes a factory built with one module and qualname,
# loaded consecutively: the first runs, the second skips in setUpClass
# (3b525 round-14 review, codex and claude). unittest sets a class up
# once per run of consecutive cases of the same class OBJECT, so the
# second class is set up and its skip recorded under the shared name;
# split by name, the second occurrence continued the first's run, took
# no record and was refused where plain unittest reports OK.
FACTORY_SAME_QUALNAME_MODULE = """\
import unittest


def make_class(skip):
    class FactoryTests(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            if skip:
                raise unittest.SkipTest("environment-dependent fixture missing")

        def test_case(self):
            self.assertFalse(skip)

    return FactoryTests


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([make_class(False)("test_case"),
                               make_class(True)("test_case")])
"""

# The converse: two factory-built classes sharing one name, both skipping
# in setUpClass, consecutive, then (after another setUpClass-skipped
# class) the first class again, dropped by its helper's setUpModule
# skipping on the second call (which no counted holder records). Split
# by class object, the two consecutive classes are two runs and take
# both records, so the dropped occurrence has none left; split by name,
# they were one run taking one record, and the leftover record counted
# the dropped occurrence (notStarted=4), a false pass.
HELPER_FACTORY_SKIP = """\
import unittest

setups = 0


def setUpModule():
    global setups
    setups += 1
    if setups > 1:
        raise unittest.SkipTest("second module set-up skipped")


def make_class():
    class FactoryTests(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            raise unittest.SkipTest("environment-dependent fixture missing")

        def test_never_starts(self):
            self.fail("must not start")

    return FactoryTests


FIRST = make_class()
SECOND = make_class()
"""

DROPPED_AFTER_SAME_NAME_SKIPS_MODULE = """\
import unittest

from tests.helper_factoryskip import FIRST, SECOND


class SkipSetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([FIRST("test_never_starts"),
                               SECOND("test_never_starts"),
                               SkipSetupTests("test_never_starts"),
                               FIRST("test_never_starts"),
                               OwnTests("test_own")])
"""

# A class whose class cleanup raises SkipTest and whose setUpClass then
# raises SkipTest: unittest records the cleanup's skip under the same
# "setUpClass (<module>.<Class>)" holder, so one run yields two records
# (3b525 round-15 review, claude). The helper's setUpModule skips on its
# second call, so the class's second occurrence is dropped without a
# record of its own. Counted one record per run, the spare record covered
# the dropped occurrence, notStarted=3, and the run passed.
HELPER_CLEANUP_SKIP = """\
import unittest

setups = 0


def setUpModule():
    global setups
    setups += 1
    if setups > 1:
        raise unittest.SkipTest("second module set-up skipped")


def skip_cleanup():
    raise unittest.SkipTest("cleanup skipped")


class CleanupSkipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.addClassCleanup(skip_cleanup)
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")
"""

DROPPED_AFTER_CLEANUP_SKIP_MODULE = """\
import unittest

from tests.helper_cleanupskip import CleanupSkipTests


class SkipSetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([CleanupSkipTests("test_never_starts"),
                               SkipSetupTests("test_never_starts"),
                               CleanupSkipTests("test_never_starts"),
                               OwnTests("test_own")])
"""

# Legitimate class cleanups that skip: one class's setUpClass succeeds
# and its cleanup skips (unittest records that under a "tearDownClass"
# holder, which notStarted does not count, and its test starts); another
# class's setUpClass and cleanup both skip, giving two records from its
# one run, which accounts for its one occurrence. unittest reports OK.
CLEANUP_SKIP_MODULE = """\
import unittest


def skip_cleanup():
    raise unittest.SkipTest("cleanup skipped")


class SetUpOkCleanupSkipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.addClassCleanup(skip_cleanup)

    def test_runs(self):
        self.assertTrue(True)


class BothSkipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.addClassCleanup(skip_cleanup)
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")
"""

# Own, C, Own, C: C's setUpClass and two class cleanups raise SkipTest,
# so each of C's two runs gives three records under one holder, and both
# runs have Own as unittest's _previousTestClass. Own's start between
# them ends "back to back", so the second run's first record counts
# (3b525 round-16 review, claude W1: without the reset in startTest the
# second run's records continued the first's, notStarted=1, and this
# legitimate run was refused). unittest reports OK (skipped=6).
CLEANUP_SKIPS_AROUND_STARTS_MODULE = """\
import unittest


def skip_cleanup():
    raise unittest.SkipTest("cleanup skipped")


class CleanupSkipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.addClassCleanup(skip_cleanup)
        cls.addClassCleanup(skip_cleanup)
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


class OwnTests(unittest.TestCase):
    def test_own(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([OwnTests("test_own"),
                               CleanupSkipTests("test_never_starts"),
                               OwnTests("test_own"),
                               CleanupSkipTests("test_never_starts")])
"""

# Stands in for a Python that renames _previousTestClass or stops setting
# it: at import, before the run, a data descriptor on unittest.TestResult
# makes the attribute unreadable on every result (class and instance
# lookup alike) and discards unittest's writes, so unittest itself sees
# None throughout. SkippedClassTests' setUpClass raises SkipTest, so a
# skip record arrives while the attribute is absent; RunningTests gives
# the module a credited start, so read as None the run would be green
# (3b525 round-16 review, agy: the getattr default None grouped such
# records silently).
HIDDEN_PREVIOUS_CLASS_MODULE = """\
import unittest


class _Hidden:
    def __get__(self, instance, owner=None):
        raise AttributeError("_previousTestClass")

    def __set__(self, instance, value):
        pass


unittest.TestResult._previousTestClass = _Hidden()


class SkippedClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("environment-dependent fixture missing")

    def test_never_starts(self):
        self.fail("must not start")


class RunningTests(unittest.TestCase):
    def test_runs(self):
        self.assertTrue(True)
"""

# Passes plus one individually skipped test, for the output-shape pin.
PASSING_WITH_SKIP_MODULE = """\
import unittest


class MixedTests(unittest.TestCase):
    def test_passes(self):
        self.assertTrue(True)

    @unittest.skip("individually skipped")
    def test_skipped(self):
        self.fail("must not run")
"""

_SENTINEL_PREFIX = "REGRESSION-GATE-RESULT "

# One nonce for direct driver invocations (delivered over stdin, as the
# parent does); the control run uses a distinct one to pin the echo.
_DRIVER_STDIN = b"0" * 32 + b"\n"


def _minimal_environ() -> dict[str, str]:
    """Only PATH: child interpreters need nothing else here, and an
    ambient PYTHONPATH/PYTHONSAFEPATH/GIT_* must not reach a fixture."""
    return {"PATH": os.environ.get("PATH", "")}


class _FakeStdin:
    """Captures what main() writes to the child's stdin (the nonce)."""

    def __init__(self) -> None:
        self.data = b""
        self.closed = False

    def write(self, payload: bytes) -> int:
        self.data += payload
        return len(payload)

    def close(self) -> None:
        self.closed = True


class _FakeProc:
    """Builds its stderr lazily: the nonce arrives over stdin AFTER the
    popen call returns, so the fabricated sentinel can only be composed
    once main() has written and closed the fake stdin."""

    def __init__(self, fake, cmd) -> None:
        self._fake = fake
        self._cmd = cmd
        self.stdin = _FakeStdin()
        self._stderr = None
        self.returncode = fake._returncode

    @property
    def stderr(self):
        if self._stderr is None:
            self._stderr = io.BytesIO(
                self._fake._stderr_bytes(self._cmd, self.stdin))
        return self._stderr

    def wait(self) -> int:
        return self.returncode


class _FakePopen:
    """Stands in for subprocess.Popen inside main(); records each command
    and fabricates the driver's stderr: a unittest summary plus (by
    default) a completion sentinel built from the nonce main() wrote to
    the child's stdin and the command's module list, the way the real
    driver would emit it. ``not_started`` fabricates a driver whose run
    had that many loaded tests kept from starting by a SkipTest in
    setUpClass (testsRun shrinks to match, as the real driver's
    would)."""

    def __init__(self, returncode: int = 0, summary: bytes | None = None,
                 sentinel: bool = True, mutate=None,
                 trailer: bytes = b"", not_started: int = 0) -> None:
        self.commands = []
        self.procs = []
        self._returncode = returncode
        self._summary = summary
        self._sentinel = sentinel
        self._mutate = mutate
        self._trailer = trailer
        self._not_started = not_started

    def __call__(self, cmd, **kwargs):
        self.commands.append(list(cmd))
        proc = _FakeProc(self, cmd)
        self.procs.append(proc)
        return proc

    def _stderr_bytes(self, cmd, stdin: _FakeStdin) -> bytes:
        # Command shape: [sys.executable, "-c", driver, *modules]; the
        # nonce travels over the child's stdin, never on argv.
        nonce = stdin.data.decode("utf-8", "replace").strip()
        modules = list(cmd[3:])
        if self._summary is None:
            stderr = b"Ran %d tests in 0.001s\n\nOK\n" % len(modules)
        else:
            stderr = self._summary
        if self._sentinel:
            ran = len(modules) - self._not_started
            ok = "True"
            counts = {name: 1 for name in modules}
            if self._mutate is not None:
                nonce, ran, ok, counts = self._mutate(nonce, ran, ok, counts)
            stderr += ("%s%s testsRun=%d notStarted=%d wasSuccessful=%s "
                       "%s\n" % (
                           _SENTINEL_PREFIX, nonce, ran, self._not_started,
                           ok,
                           " ".join("%s=%d" % (name, counts[name])
                                    for name in sorted(counts)))).encode()
        stderr += self._trailer
        return stderr


class RegressionGateCompletenessTests(unittest.TestCase):
    """main() runs every top-level tests/test_*.py, or refuses loud."""

    def _runner(self):
        return runpy.run_path(str(RUNNER_PATH))

    def _call_main(self, runner, **kwargs):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = runner["main"](**kwargs)
        return code, out.getvalue(), err.getvalue()

    def _tmp_repo(self, test_files, body: str = PASSING_MODULE):
        root = Path(tempfile.mkdtemp(prefix="gate36-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "tests").mkdir()
        (root / "tests" / "__init__.py").write_text("")
        for rel in test_files:
            path = root / "tests" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
        return root

    def test_main_executed_list_covers_every_test_file(self) -> None:
        """The module list main() actually hands to the child subprocess
        (not discovery alone) covers every on-disk tests/test_*.py; the
        per-run nonce the child's sentinel must echo travels over the
        child's stdin, never on argv (3b525 round 3, F1)."""
        runner = self._runner()
        fake = _FakePopen()
        code, _out, err = self._call_main(runner, popen=fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(len(fake.commands), 1)
        # Command shape: [sys.executable, "-c", driver, *modules].
        written = fake.procs[0].stdin.data.decode("utf-8", "replace")
        self.assertRegex(written, r"^[0-9a-f]{32}\n$")
        self.assertTrue(fake.procs[0].stdin.closed,
                        "main() must close the child's stdin after "
                        "writing the nonce")
        self.assertNotIn(written.strip(), " ".join(fake.commands[0]),
                         "the nonce must not appear on the child's argv")
        executed = fake.commands[0][3:]
        expected = sorted(
            "tests." + p.name[:-3]
            for p in (REPO_ROOT / "tests").iterdir()
            if p.is_file() and p.name.startswith("test_")
            and p.name.endswith(".py"))
        self.assertTrue(expected, "no tests/test_*.py files found")
        self.assertEqual(executed, expected,
                         "gate 36 runner's executed module list does not "
                         "cover every tests/test_*.py file")
        self.assertIn("tests.test_linters", executed)
        self.assertIn("tests.test_regression_gate", executed)

    def test_main_refuses_run_list_that_drops_a_module(self) -> None:
        """A filter applied between discovery and execution is refused by
        the runner's own os.walk self-check, before anything runs."""
        runner = self._runner()
        namespace = runner["main"].__globals__
        original = namespace["discover_test_modules"]

        def narrowed(repo_root):
            return [m for m in original(repo_root)
                    if m != "tests.test_session_facts"]

        fake = _FakePopen()
        namespace["discover_test_modules"] = narrowed
        try:
            code, _out, err = self._call_main(runner, popen=fake)
        finally:
            namespace["discover_test_modules"] = original
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", err)
        self.assertIn("test_session_facts", err)
        self.assertEqual(fake.commands, [],
                         "the refusal must precede any child run")

    def test_main_green_on_complete_run_list(self) -> None:
        """Control: a complete top-level run list passes the self-check
        and hands exactly the on-disk modules to the child."""
        runner = self._runner()
        root = self._tmp_repo(["test_a.py", "test_b.py"])
        fake = _FakePopen()
        code, out, err = self._call_main(runner, repo_root=root, popen=fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(fake.commands[0][3:],
                         ["tests.test_a", "tests.test_b"])
        self.assertIn("tests.test_a", out)

    def test_main_refuses_nested_test_file(self) -> None:
        """Only top-level tests/test_*.py files are in scope; a test file
        in a tests/ subdirectory is refused by name, never skipped."""
        runner = self._runner()
        root = self._tmp_repo(["test_a.py", "sub/test_nested.py"])
        fake = _FakePopen()
        code, _out, err = self._call_main(runner, repo_root=root, popen=fake)
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", err)
        self.assertIn("test_nested.py", err)
        self.assertIn("only top-level", err)
        self.assertEqual(fake.commands, [])

    def test_main_refuses_test_package_directory(self) -> None:
        """A tests/test_*/ package directory could hold TestCases that
        discovery would neither run nor refuse per file; the directory
        itself is refused by name (3b525 round 2, F8/VPR003)."""
        runner = self._runner()
        root = self._tmp_repo(["test_a.py"])
        pkg = root / "tests" / "test_pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text(PASSING_MODULE)
        fake = _FakePopen()
        code, _out, err = self._call_main(runner, repo_root=root, popen=fake)
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", err)
        self.assertIn("test_pkg", err)
        self.assertEqual(fake.commands, [])

    def test_main_refuses_symlinked_subdirectory(self) -> None:
        """os.walk does not follow directory symlinks, so a symlinked
        tests/ subdirectory could hide a test file; it is refused by
        name (3b525 round 2, VPR003)."""
        runner = self._runner()
        root = self._tmp_repo(["test_a.py"])
        target = root / "elsewhere"
        target.mkdir()
        (target / "test_hidden.py").write_text(FAILING_MODULE)
        (root / "tests" / "sub").symlink_to(target)
        fake = _FakePopen()
        code, _out, err = self._call_main(runner, repo_root=root, popen=fake)
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", err)
        self.assertIn("symlink", err)
        self.assertIn("sub", err)
        self.assertEqual(fake.commands, [])

    @unittest.skipIf(os.geteuid() == 0,
                     "root ignores directory permission bits")
    def test_main_refuses_unreadable_subdirectory(self) -> None:
        """A tests/ subdirectory the walk cannot list could hide a test
        file; the walk error is a refusal, never a silent skip (3b525
        round 2, VPR003)."""
        runner = self._runner()
        root = self._tmp_repo(["test_a.py"])
        sub = root / "tests" / "hidden"
        sub.mkdir()
        (sub / "test_hidden.py").write_text(FAILING_MODULE)
        os.chmod(sub, 0o000)
        self.addCleanup(os.chmod, sub, 0o755)
        fake = _FakePopen()
        code, _out, err = self._call_main(runner, repo_root=root, popen=fake)
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", err)
        self.assertIn("cannot inspect", err)
        self.assertEqual(fake.commands, [])

    def test_import_refusal_catches_base_exception(self) -> None:
        """An import-time SystemExit(0), or any other BaseException, is a
        refusal naming the file (exit 2), never a green run; the control
        module must NOT be refused, so a vacuous pass (both modules
        failing for an environmental reason) cannot hide a flip."""
        runner = self._runner()
        driver = runner["_DRIVER"]
        cases = (
            ("systemexit_zero", "raise SystemExit(0)\n"),
            ("systemexit_three", "raise SystemExit(3)\n"),
            ("keyboardinterrupt", "raise KeyboardInterrupt\n"),
            ("runtimeerror", "raise RuntimeError('import failure')\n"),
        )
        for label, body in cases:
            with self.subTest(label=label):
                root = self._tmp_repo(["test_ok.py"])
                (root / "tests" / "test_boom.py").write_text(body)
                result = subprocess.run(
                    [sys.executable, "-c", driver,
                     "tests.test_boom", "tests.test_ok"],
                    cwd=str(root), env=_minimal_environ(),
                    input=_DRIVER_STDIN,
                    capture_output=True, timeout=120)
                self.assertEqual(result.returncode, 2, result.stderr[-500:])
                self.assertIn(b"REFUSED: cannot import tests/test_boom.py",
                              result.stderr)
                self.assertNotIn(b"tests/test_ok.py", result.stderr,
                                 "the control module was refused: the "
                                 "refusal assertion is passing vacuously")

    def test_import_refusal_is_hermetic(self) -> None:
        """An ambient PYTHONSAFEPATH/PYTHONPATH must not reach the child
        driver (it would refuse BOTH modules and let a flip pass
        vacuously, 3b525 round 2 F5): the driver subprocess runs with a
        minimal environment, so the control module still imports."""
        runner = self._runner()
        driver = runner["_DRIVER"]
        root = self._tmp_repo(["test_ok.py"])
        (root / "tests" / "test_boom.py").write_text("raise SystemExit(0)\n")
        poisoned = dict(os.environ, PYTHONSAFEPATH="1",
                        PYTHONPATH=str(REPO_ROOT))
        with mock.patch.dict(os.environ, poisoned, clear=True):
            result = subprocess.run(
                [sys.executable, "-c", driver,
                 "tests.test_boom", "tests.test_ok"],
                cwd=str(root), env=_minimal_environ(),
                input=_DRIVER_STDIN,
                capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 2, result.stderr[-500:])
        self.assertIn(b"REFUSED: cannot import tests/test_boom.py",
                      result.stderr)
        self.assertNotIn(b"tests/test_ok.py", result.stderr,
                         "the control module was refused: the import "
                         "refusal test is passing vacuously")

    def test_driver_refuses_argv_that_drops_a_module(self) -> None:
        """The child driver re-enumerates tests/ itself and refuses an
        argv that differs, so a filter on the child's argv (or inside
        the driver, after a flip) cannot drop a module (3b525 round 2,
        VPR001/F1)."""
        runner = self._runner()
        driver = runner["_DRIVER"]
        root = self._tmp_repo(["test_a.py", "test_b.py"])
        result = subprocess.run(
            [sys.executable, "-c", driver, "tests.test_a"],
            cwd=str(root), env=_minimal_environ(),
            input=_DRIVER_STDIN,
            capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 2, result.stderr[-500:])
        self.assertIn(b"REFUSED: driver argv modules", result.stderr)
        self.assertIn(b"tests.test_b", result.stderr)

    def test_driver_refuses_zero_test_module(self) -> None:
        """A module that imports cleanly but contributes zero test cases
        (an empty load_tests, a class moved off TestCase) is refused by
        name; the control run with real tests emits the sentinel (3b525
        round 2, F2/VPR002)."""
        runner = self._runner()
        driver = runner["_DRIVER"]
        root = self._tmp_repo(["test_ok.py"])
        (root / "tests" / "test_empty.py").write_text("import unittest\n")
        result = subprocess.run(
            [sys.executable, "-c", driver,
             "tests.test_empty", "tests.test_ok"],
            cwd=str(root), env=_minimal_environ(),
            input=_DRIVER_STDIN,
            capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 2, result.stderr[-500:])
        self.assertIn(b"REFUSED: tests/test_empty.py contributes zero "
                      b"test cases", result.stderr)
        self.assertNotIn(b"tests/test_ok.py", result.stderr)
        # Control: with real tests in both modules the driver runs them
        # and its LAST stderr line is the sentinel echoing the nonce it
        # read from stdin.
        control = self._tmp_repo(["test_a.py", "test_b.py"])
        result = subprocess.run(
            [sys.executable, "-c", driver,
             "tests.test_a", "tests.test_b"],
            cwd=str(control), env=_minimal_environ(),
            input=b"f" * 32 + b"\n",
            capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr[-500:])
        last = result.stderr.decode().splitlines()[-1]
        self.assertRegex(
            last,
            r"^REGRESSION-GATE-RESULT f{32} testsRun=2 notStarted=0 "
            r"wasSuccessful=True tests\.test_a=1 tests\.test_b=1$")

    def test_main_refuses_green_exit_without_summary_line(self) -> None:
        """A child exit of 0 is believed only when unittest's output has a
        'Ran N tests' line with N at least 1; failures stay forwarded."""
        runner = self._runner()
        cases = (
            ("no_summary", 0, b"", 2),
            ("ran_zero", 0, b"Ran 0 tests in 0.000s\n\nOK\n", 2),
            ("ran_one", 0, b"Ran 1 test in 0.001s\n\nOK\n", 0),
            ("ran_many", 0, b"Ran 3 tests in 0.001s\n\nOK\n", 0),
            ("failure_forwarded", 1,
             b"Ran 5 tests in 0.100s\n\nFAILED (failures=1)\n", 1),
        )
        for label, returncode, stderr, expected in cases:
            with self.subTest(label=label):
                fake = _FakePopen(returncode=returncode, summary=stderr)
                code, _out, err = self._call_main(runner, popen=fake)
                self.assertEqual(code, expected, err)
                if returncode == 0 and expected == 2:
                    self.assertIn("REFUSED", err)
                    self.assertIn("Ran N tests", err)

    def test_main_requires_completion_sentinel(self) -> None:
        """A green child exit is believed only when the LAST stderr line
        is the driver's sentinel with this run's nonce, per-module
        counts naming exactly the handed modules (each at least 1) and
        a matching testsRun; an earlier real summary, a spoofed line or
        a dropped module is refused (3b525 round 2, VPR001/VPR002/F3)."""
        runner = self._runner()

        def drop_last(nonce, ran, ok, counts):
            counts.pop(sorted(counts)[-1])
            return nonce, len(counts), ok, counts

        def rename_one(nonce, ran, ok, counts):
            counts.pop(sorted(counts)[-1])
            counts["tests.test_imposter"] = 1
            return nonce, ran, ok, counts

        def zero_count(nonce, ran, ok, counts):
            counts[sorted(counts)[0]] = 0
            return nonce, ran - 1, ok, counts

        def inflate_ran(nonce, ran, ok, counts):
            return nonce, ran + 7, ok, counts

        def underrun(nonce, ran, ok, counts):
            # testsRun short of the loaded total with no matching
            # notStarted: a dropped test, not an accounted skip.
            return nonce, ran - 1, ok, counts

        def unsuccessful(nonce, ran, ok, counts):
            return nonce, ran, "False", counts

        def wrong_nonce(nonce, ran, ok, counts):
            return "0" * 32, ran, ok, counts

        cases = (
            ("missing_sentinel", _FakePopen(sentinel=False), "sentinel"),
            ("sentinel_not_last",
             _FakePopen(trailer=b"stray trailing line\n"), "sentinel"),
            ("wrong_nonce", _FakePopen(mutate=wrong_nonce), "nonce"),
            ("dropped_module", _FakePopen(mutate=drop_last), "module"),
            ("renamed_module", _FakePopen(mutate=rename_one), "module"),
            ("zero_count_module", _FakePopen(mutate=zero_count), "zero"),
            ("testsrun_mismatch", _FakePopen(mutate=inflate_ran),
             "testsRun"),
            ("dropped_test_unaccounted", _FakePopen(mutate=underrun),
             "notStarted"),
            ("skip_plus_inflated_ran",
             _FakePopen(mutate=inflate_ran, not_started=2), "notStarted"),
            ("unsuccessful_result", _FakePopen(mutate=unsuccessful),
             "wasSuccessful"),
        )
        for label, fake, needle in cases:
            with self.subTest(label=label):
                code, _out, err = self._call_main(runner, popen=fake)
                self.assertEqual(code, 2, err)
                self.assertIn("REFUSED", err)
                self.assertIn(needle, err)
        with self.subTest(label="control_green"):
            code, _out, err = self._call_main(runner, popen=_FakePopen())
            self.assertEqual(code, 0, err)
        with self.subTest(label="control_green_with_not_started"):
            # A faithful driver whose run had two loaded tests kept
            # from starting by a class-level SkipTest stays green:
            # testsRun plus notStarted equals the loaded total.
            code, _out, err = self._call_main(
                runner, popen=_FakePopen(not_started=2))
            self.assertEqual(code, 0, err)

    def test_main_end_to_end_green_on_synthetic_tree(self) -> None:
        """Control with the REAL child driver, on a tree whose modules
        carry the real guard-module names: a name-specific filter flip
        (drop tests.test_linters or tests.test_regression_gate) turns
        this green run into a refusal."""
        runner = self._runner()
        root = self._tmp_repo(["test_linters.py", "test_regression_gate.py"])
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 0, err)
        self.assertIn("Ran 2 tests", err)
        self.assertIn(_SENTINEL_PREFIX, err)
        self.assertIn("tests.test_linters=1", err)
        self.assertIn("tests.test_regression_gate=1", err)

    def test_main_refuses_load_tests_systemexit(self) -> None:
        """A load_tests that prints a real green unittest summary and then
        raises SystemExit(0) ends the child before the sentinel, so the
        run is refused even though a failing sibling never ran (3b525
        round 2, VPR002)."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_fail.py"], body=FAILING_MODULE)
        (root / "tests" / "test_aa_sneaky.py").write_text(
            "import sys\n"
            "import unittest\n\n\n"
            "class LocalTests(unittest.TestCase):\n"
            "    def test_local(self):\n"
            "        self.assertTrue(True)\n\n\n"
            "def load_tests(loader, tests, pattern):\n"
            "    sys.stderr.write('Ran 1 test in 0.000s\\n\\nOK\\n')\n"
            "    raise SystemExit(0)\n")
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 2, err)
        self.assertIn("REFUSED", err)
        self.assertIn("sentinel", err)

    def test_main_refuses_forged_sentinel_from_load_tests(self) -> None:
        """The round-3 reproducer (3b525 F1): a load_tests that reads
        argv and stdin, prints a green summary plus a forged completion
        sentinel and exits 0, beside a failing sibling that never runs.
        The nonce travels over the child's stdin and is consumed before
        any test module is imported, so a scrape of argv and stdin
        cannot see it (on argv it could, and this forgery then passed
        as green). With no 32-hex candidate in sight the scrape falls
        back to a non-hex token, so what refuses this run is the
        sentinel FORMAT check (the forged line never parses as the
        driver's completion sentinel), not the nonce comparison; that
        comparison is pinned by the wrong_nonce subtest of
        test_main_requires_completion_sentinel. The __main__.nonce
        channel stays open: see the residual test below."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_fail.py"], body=FAILING_MODULE)
        (root / "tests" / "test_aa_forge.py").write_text(FORGING_MODULE)
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 2,
                         "a forged sentinel from code that cannot see "
                         "the nonce must be refused:\n" + err)
        self.assertIn("REFUSED", err)
        self.assertIn("sentinel", err)

    def test_main_accepts_main_nonce_forgery_residual(self) -> None:
        """DOCUMENTED ACCEPTED RESIDUAL (3b525 round 4, F1): the driver
        is a python -c script, so the nonce is a module-level global of
        __main__; a load_tests that imports __main__ recovers it,
        forges a complete sentinel and exits 0, and the run passes as
        green while the failing sibling never runs. This test asserts
        that documented behaviour (it is NOT a skip): a change that
        closes the channel turns this exit 0 into a refusal and must
        update this test together with the three documentation
        surfaces that state the residual: the runner's module
        docstring (pinned below via the loaded module's __doc__, so
        the driver-comment copy cannot stand in for it) and
        tools/README.md and tests/README.md (each pinned as file
        text)."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_fail.py"], body=FAILING_MODULE)
        (root / "tests" / "test_aa_forge.py").write_text(
            MAIN_NONCE_FORGING_MODULE)
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(
            code, 0,
            "the __main__.nonce forgery is a documented accepted "
            "residual and currently passes as green; if it is now "
            "refused, the channel was closed: update this test, the "
            "runner docstring, tools/README.md and tests/README.md "
            "together:\n" + err)
        self.assertNotIn("REFUSED", err)
        self.assertIn(_SENTINEL_PREFIX, err)
        self.assertNotIn(
            "this test must be reached", err,
            "the forgery exits before the failing sibling runs; the "
            "sibling's failure appearing means the behaviour changed")
        # Every documentation surface names the residual's channel, so
        # closing it (or renaming the channel) stales the docs loudly.
        # The needle is the disclosure's recovery recipe, not the bare
        # "__main__": the runner's entry-point guard (its line
        # 'if __name__ == "__main__":') would satisfy the bare string
        # even with the disclosure deleted.
        # The runner surface is the module docstring alone, read as
        # runner["__doc__"] from the runpy.run_path namespace already
        # loaded above (which does not execute main): a driver comment
        # in the same file carries a second copy of the recipe, so a
        # file-wide search would stay green with the docstring
        # disclosure deleted (3b525 round 6, N1).
        self.assertIn(
            "import __main__",
            runner["__doc__"] or "",
            "the runner's module docstring must document the "
            "__main__.nonce accepted residual")
        for rel in ("tools/README.md", "tests/README.md"):
            self.assertIn(
                "import __main__",
                (REPO_ROOT / rel).read_text(encoding="utf-8"),
                "%s must document the __main__.nonce accepted "
                "residual" % rel)

    def test_main_green_with_class_level_skip_in_module_that_ran(
            self) -> None:
        """A SkipTest raised in setUpClass bypasses startTest for every
        test of that class, so testsRun undercounts the loaded suite
        while unittest itself reports the run green; when the module
        otherwise ran, the sentinel's notStarted accounts for those
        tests and the run is NOT refused (3b525 round 3, F4). A test
        skipped individually counts as started (3b525 round 8, W1
        rule). Loaded here: 4 (partly skipped module) + 1 (passing
        sibling) = 5; testsRun=3, notStarted=2."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_ok.py"])
        (root / "tests" / "test_aa_partlyskipped.py").write_text(
            PARTLY_SKIPPED_MODULE)
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 0,
                         "a run unittest reports green with a class-level "
                         "skip in a module that otherwise ran must not be "
                         "refused:\n" + err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=2)", err)
        self.assertIn("testsRun=3 notStarted=2", err)
        self.assertIn(_SENTINEL_PREFIX, err)

    def test_main_refuses_module_whose_tests_never_start(self) -> None:
        """A module none of whose tests started (a SkipTest raised in
        setUpModule, or in setUpClass for its only class) is refused by
        name even though unittest reports the run green and the other
        module ran (3b525 round 8, W1: before this check the run exited
        0 with testsRun=1 notStarted=3). A class skipped by a class
        decorator (unittest.skip, skipUnless(False)) counts the same as
        one skipped in setUpClass, although unittest calls startTest for
        its tests (3b525 round-8 review, N1)."""
        runner = self._runner()
        cases = (
            ("setupmodule_skip", SKIPPING_MODULE_MODULE),
            ("setupclass_skip_every_class", SKIPPING_CLASS_MODULE),
            ("class_skip_decorator", DECORATOR_SKIPPED_CLASS_MODULE),
            ("class_skipunless_false", DECORATOR_SKIPUNLESS_FALSE_MODULE),
        )
        for label, body in cases:
            with self.subTest(label=label):
                root = self._tmp_repo(["test_zz_ok.py"])
                (root / "tests" / "test_aa_neverstarts.py").write_text(body)
                with mock.patch.dict(os.environ, _minimal_environ(),
                                     clear=True):
                    code, _out, err = self._call_main(runner, repo_root=root)
                self.assertEqual(code, 2, err)
                self.assertRegex(
                    err, r"(?m)^REFUSED: tests/test_aa_neverstarts\.py: "
                    r"\d+ loaded, 0 credited starts \(")
                self._assert_refusal_names_no_cause(err)
                self.assertNotIn("tests/test_zz_ok.py", err,
                                 "the module that ran was refused: the "
                                 "refusal assertion is passing vacuously")
                self.assertNotIn(_SENTINEL_PREFIX, err)

    def test_main_accepts_borrowing_residual(self) -> None:
        """DOCUMENTED ACCEPTED RESIDUAL: a started test is credited to
        the module whose loaded suite contains it, so a module that only
        imports and loads another module's TestCase class earns credit
        for it and is not refused (rounds 9 and 10 refused this by
        crediting the defining code, and each variant broke legitimate
        modules). Here: a module whose own class is skipped in
        setUpClass beside a class imported from tests/test_zz_ok.py
        (loaded 2 + 1; testsRun=2, notStarted=1), and a module that only
        imports a class from a helper outside the run list."""
        cases = (
            ("handed_module_class",
             {"test_aa_borrows.py": BORROWING_MODULE},
             "testsRun=2 notStarted=1"),
            ("helper_module_class",
             {"helper_shared.py": HELPER_SHARED,
              "test_aa_helperborrow.py": HELPER_BORROWING_MODULE},
             "testsRun=2 notStarted=0"),
        )
        for label, files, counts in cases:
            with self.subTest(label=label):
                code, _out, err = self._run_gate_with(files)
                self.assertEqual(code, 0, err)
                self.assertNotIn("REFUSED", err)
                self.assertIn(counts, err)
                self.assertIn(_SENTINEL_PREFIX, err)

    def test_main_refuses_unpaired_load(self) -> None:
        """When unittest.main's suite for a module does not hold the case
        count the driver's own load found (here a load_tests returning
        one test on the first load and two on the second), the driver
        refuses by name, naming the mismatch, before any test runs."""
        code, _out, err = self._run_gate_with({
            "test_aa_pairing.py": PAIRING_MISMATCH_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertRegex(
            err, r"(?m)^REFUSED: tests/test_aa_pairing\.py: unittest\.main "
            r"loaded 2 test cases, the driver's own load 1; ")
        self.assertNotIn("tests/test_zz_ok.py", err)
        self.assertNotIn("Ran ", err)
        self.assertNotIn(_SENTINEL_PREFIX, err)

    def _assert_shared_case_refused(self, err: str, case: str) -> None:
        """The shared-case refusal names the case and both modules, and
        comes before the run (no test reached, no sentinel)."""
        self.assertRegex(
            err, r"(?m)^REFUSED: test case object <%s testMethod=\w+> is "
            r"in the loaded suites of more than one module "
            r"\(tests/test_aa_first\.py, tests/test_ab_second\.py\); "
            % re.escape(case))
        self.assertNotIn("tests/test_zz_ok.py", err)
        self.assertNotIn("Ran ", err)
        self.assertNotIn(_SENTINEL_PREFIX, err)

    def test_main_refuses_case_shared_by_two_modules(self) -> None:
        """A helper's module-level case object loaded by two modules is
        refused before the run, naming both (3b525 round 13). Round 12
        credited each module for its own occurrence (round-11 review,
        codex E1), but forward matching across modules could credit the
        wrong one (round-12 review, codex E1 and E2)."""
        code, _out, err = self._run_gate_with({
            "helper_sharedcase.py": HELPER_SHARED_CASE,
            "test_aa_first.py": SHARED_CASE_MODULE,
            "test_ab_second.py": SHARED_CASE_MODULE,
        })
        self.assertEqual(code, 2, err)
        self._assert_shared_case_refused(
            err, "tests.helper_sharedcase.SharedCaseTests")

    def test_main_refuses_module_whose_shared_occurrence_never_starts(
            self) -> None:
        """A shared case object whose second occurrence never starts
        (3b525 round-11 review, codex E2: that run passed; round 12
        refused the second module after the run) is now refused before
        the run by the shared-case refusal, naming both modules."""
        code, _out, err = self._run_gate_with({
            "helper_moduleskip.py": HELPER_MODULE_SKIP,
            "helper_sharedonce.py": HELPER_SHARED_ONCE,
            "test_aa_first.py": SHARED_ONCE_FIRST_MODULE,
            "test_ab_second.py": SHARED_ONCE_SECOND_MODULE,
        })
        self.assertEqual(code, 2, err)
        self._assert_shared_case_refused(
            err, "tests.helper_sharedonce.SharedOnceTests")

    def test_main_refuses_shared_case_equal_to_strings(self) -> None:
        """A shared case object whose __eq__ says equal to any string is
        still refused before the run, naming both modules: the check is
        keyed by identity and keeps the module names in a set of their
        own (3b525 round-13 review, codex E: compared with the module
        names by equality, the case hid the second module and the run
        exited 0)."""
        code, _out, err = self._run_gate_with({
            "helper_stringequal.py": HELPER_STRING_EQUAL_CASE,
            "test_aa_first.py": STRING_EQUAL_CASE_MODULE,
            "test_ab_second.py": STRING_EQUAL_CASE_MODULE,
        })
        self.assertEqual(code, 2, err)
        self._assert_shared_case_refused(
            err, "tests.helper_stringequal.StringEqualTests")

    def test_main_matches_starts_by_identity_not_equality(self) -> None:
        """Two distinct but equal case objects, one in each of two
        modules' suites, separated by a setUpClass-skipped class: each
        module is credited for its own object's start (3b525 round 13;
        with equality matching the second module's start is taken by
        the first module's never-started occurrence, and the second
        module is refused). Loaded 3 + 1 + 1; testsRun=3, notStarted=2."""
        code, _out, err = self._run_gate_with({
            "helper_skipfirst.py": HELPER_SKIP_FIRST_SETUP,
            "test_aa_first.py": EQUAL_CASE_FIRST_MODULE,
            "test_ab_second.py": EQUAL_CASE_SECOND_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=2)", err)
        self.assertIn("testsRun=3 notStarted=2", err)

    def test_main_refuses_dropped_test_whose_class_skipped_earlier(
            self) -> None:
        """A standard suite drops a test (its helper's setUpModule skips
        on the second call, which no counted holder records) whose class
        skipped in setUpClass earlier in the run: the earlier skip record
        must not count it, so the reconciliation refuses (3b525 round
        13; without clearing the records at each matched start, the
        dropped test counted as notStarted and the run passed). Loaded
        3 + 1; testsRun=2, notStarted=1."""
        code, _out, err = self._run_gate_with({
            "helper_modskipsecond.py": HELPER_MODULE_SKIP_SECOND,
            "test_aa_dropped.py": DROPPED_AFTER_CLASS_SKIP_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertIn("OK (skipped=2)", err)
        self.assertIn("testsRun=2 notStarted=1", err)
        refusal = [line for line in err.splitlines()
                   if line.startswith("REFUSED: ")]
        self.assertEqual(len(refusal), 1, err)
        self.assertIn("does not equal the per-module total 4", refusal[0])

    def test_main_refuses_dropped_occurrence_with_no_skip_record_left(
            self) -> None:
        """In a plain suite, a class skipped in setUpClass is loaded
        twice around another setUpClass-skipped class with no start
        between, and its second occurrence is dropped (the helper's
        setUpModule skips on its second call, which no counted holder
        records). Its one skip record covers one class occurrence, so
        the dropped one is not notStarted and the reconciliation refuses
        (3b525 round-13 review, claude W1: the record covered both, so
        notStarted was 3 and the run passed). Loaded 4 + 1; testsRun=2,
        notStarted=2."""
        code, _out, err = self._run_gate_with({
            "helper_modskipsecond.py": HELPER_MODULE_SKIP_SECOND,
            "test_aa_dropped.py": DROPPED_BETWEEN_CLASS_SKIPS_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertIn("OK (skipped=3)", err)
        self.assertIn("testsRun=2 notStarted=2", err)
        refusal = [line for line in err.splitlines()
                   if line.startswith("REFUSED: ")]
        self.assertEqual(len(refusal), 1, err)
        self.assertIn("does not equal the per-module total 5", refusal[0])

    def test_main_counts_trailing_class_skip_in_last_module(self) -> None:
        """A setUpClass-skipped class at the end of the last module (it
        sorts after tests/test_zz_ok.py) has no later start to settle
        it: the driver's final settle counts it, so the run is green
        (3b525 round 13; without the final settle notStarted is 0 and
        the reconciliation refuses). Loaded 1 + 4; testsRun=3,
        notStarted=2."""
        code, _out, err = self._run_gate_with({
            "test_zz_zpartlyskipped.py": PARTLY_SKIPPED_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=2)", err)
        self.assertIn("testsRun=3 notStarted=2", err)

    def test_main_counts_class_skip_per_occurrence(self) -> None:
        """A setUpClass-skipped class loaded twice in one module, around
        a running class, is set up (and skips) twice; notStarted counts
        each never-started occurrence once (3b525 round-11 review, codex
        E3: notStarted=4 for the three-case suite refused the run).
        Loaded 3 + 1; testsRun=2, notStarted=2."""
        code, _out, err = self._run_gate_with({
            "test_aa_skiptwice.py": SKIPPED_CLASS_LOADED_TWICE_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=2)", err)
        self.assertIn("testsRun=2 notStarted=2", err)

    def test_main_groups_class_runs_by_class_object(self) -> None:
        """Two distinct classes sharing a module and qualname (built by
        a factory), consecutive in one suite, the first running and the
        second skipping in setUpClass: unittest sets each up, as it
        splits runs by class object, so the second's skip record counts
        it (3b525 round-14 review: split by strclass name it continued
        the first's run, testsRun=2 notStarted=0 of 3, and was refused).
        Loaded 2 + 1; testsRun=2, notStarted=1."""
        code, _out, err = self._run_gate_with({
            "test_aa_factory.py": FACTORY_SAME_QUALNAME_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=1)", err)
        self.assertIn("testsRun=2 notStarted=1", err)

    def test_main_refuses_dropped_occurrence_after_same_name_skips(
            self) -> None:
        """Two distinct classes sharing a module and qualname, both
        skipping in setUpClass, consecutive, are two runs taking two skip
        records, so a later occurrence of the first class, dropped by
        its helper's setUpModule skipping on the second call, has no
        record left and the reconciliation refuses (3b525 round 15;
        split by strclass name the two were one run, the leftover record
        counted the dropped occurrence, notStarted=4, and the run
        passed). Loaded 5 + 1; testsRun=2, notStarted=3."""
        code, _out, err = self._run_gate_with({
            "helper_factoryskip.py": HELPER_FACTORY_SKIP,
            "test_aa_dropped.py": DROPPED_AFTER_SAME_NAME_SKIPS_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertIn("OK (skipped=4)", err)
        self.assertIn("testsRun=2 notStarted=3", err)
        refusal = [line for line in err.splitlines()
                   if line.startswith("REFUSED: ")]
        self.assertEqual(len(refusal), 1, err)
        self.assertIn("does not equal the per-module total 6", refusal[0])

    def test_main_refuses_dropped_occurrence_after_cleanup_skip(
            self) -> None:
        """A class whose class cleanup and setUpClass both raise SkipTest
        gives two records under one setUpClass holder from one run; one
        run consumes at most one of them, so a later occurrence of the
        class, dropped by its helper's setUpModule skipping on the second
        call, has no record left and the reconciliation refuses (3b525
        round-15 review, claude: the spare record covered the dropped
        occurrence, notStarted=3, and the run passed). Loaded 4 + 1;
        testsRun=2, notStarted=2."""
        code, _out, err = self._run_gate_with({
            "helper_cleanupskip.py": HELPER_CLEANUP_SKIP,
            "test_aa_dropped.py": DROPPED_AFTER_CLEANUP_SKIP_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertIn("OK (skipped=4)", err)
        self.assertIn("testsRun=2 notStarted=2", err)
        refusal = [line for line in err.splitlines()
                   if line.startswith("REFUSED: ")]
        self.assertEqual(len(refusal), 1, err)
        self.assertIn("does not equal the per-module total 5", refusal[0])

    def test_main_green_with_class_cleanup_skips(self) -> None:
        """A class cleanup that raises SkipTest while setUpClass succeeds
        (recorded under a tearDownClass holder, not counted) and a class
        whose setUpClass and cleanup both skip (two records from its one
        run, accounting for its one occurrence) are a run unittest
        reports OK, and the gate does not refuse it. Loaded 2 + 1;
        testsRun=2, notStarted=1."""
        code, _out, err = self._run_gate_with({
            "test_aa_cleanupskip.py": CLEANUP_SKIP_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=3)", err)
        self.assertIn("testsRun=2 notStarted=1", err)

    def test_main_green_with_cleanup_skips_around_starts(self) -> None:
        """Own, C, Own, C, where C's setUpClass and two class cleanups
        raise SkipTest: both of C's runs follow Own, so their records
        share holder and _previousTestClass, and only Own's start between
        them separates the runs; each run counts one record (3b525
        round-16 review, claude W1: the reset in startTest was untested).
        Loaded 4 + 1; testsRun=3, notStarted=2."""
        code, _out, err = self._run_gate_with({
            "test_aa_aroundstarts.py": CLEANUP_SKIPS_AROUND_STARTS_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=6)", err)
        self.assertIn("testsRun=3 notStarted=2", err)

    def test_main_refuses_absent_previous_test_class(self) -> None:
        """A setUpClass skip record arriving while the result has no
        _previousTestClass attribute at all is refused, naming the
        attribute and the Python version, rather than grouped as if the
        attribute were None (3b525 round-16 review, agy: getattr's
        default turned an input that cannot answer into an answer). Read
        as None, the run is green: loaded 2 + 1, testsRun=2,
        notStarted=1."""
        code, _out, err = self._run_gate_with({
            "test_aa_hidden.py": HIDDEN_PREVIOUS_CLASS_MODULE,
        })
        self.assertEqual(code, 2, err)
        refusal = [line for line in err.splitlines()
                   if line.startswith("REFUSED: ")]
        self.assertEqual(len(refusal), 1, err)
        self.assertIn("_previousTestClass", refusal[0])
        self.assertIn("Python %d.%d.%d" % sys.version_info[:3], refusal[0])
        self.assertNotIn(_SENTINEL_PREFIX, err)

    def test_main_reads_class_skip_flag_from_dunder_class(self) -> None:
        """The class skip flag is read from test.__class__, as unittest
        reads it (3b525 round-11 review, claude N4): a __class__
        property hiding a skip-decorated class behind a plain type is
        skipped by unittest and is not a credited start, and a skip flag
        on the type alone, behind a __class__ naming a plain class, does
        not stop unittest running the test, which is credited."""
        with self.subTest(label="dunder_class_hides_skipped_class"):
            code, _out, err = self._run_gate_with({
                "test_aa_disguised.py": CLASS_PROPERTY_HIDES_SKIP_MODULE,
            })
            self.assertEqual(code, 2, err)
            self.assertIn("OK (skipped=1)", err)
            self.assertRegex(
                err, r"(?m)^REFUSED: tests/test_aa_disguised\.py: 1 loaded, "
                r"0 credited starts \(")
            self.assertNotIn("tests/test_zz_ok.py", err)
        with self.subTest(label="skip_flag_on_type_only"):
            code, _out, err = self._run_gate_with({
                "test_aa_typeflag.py": CLASS_PROPERTY_HIDES_PLAIN_MODULE,
            })
            self.assertEqual(code, 0, err)
            self.assertNotIn("REFUSED", err)
            self.assertIn("testsRun=2 notStarted=0", err)

    def test_main_credits_case_inside_base_test_suite(self) -> None:
        """A load_tests returning unittest.suite.BaseTestSuite([case]) is
        credited: flatten descends into any BaseTestSuite (3b525
        round-11 review, claude W2; with flatten limited to
        unittest.TestSuite the case is never matched and the module is
        refused)."""
        code, _out, err = self._run_gate_with({
            "test_aa_basesuite.py": BASE_TEST_SUITE_MODULE,
        })
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("testsRun=2 notStarted=0", err)

    def test_driver_never_credits_a_freed_case_id(self) -> None:
        """Every flattened case stays alive until the run ends, so a
        fresh case object started later cannot take a freed case's id
        and credit its module (3b525 round-11 review, claude W1). The
        module whose only test a setUpModule SkipTest stopped is refused
        by name, by the driver itself, before the parent's
        reconciliation (which the probes' extra starts also fail)."""
        code, _out, err = self._run_gate_with({
            "test_ab_modskip.py": SKIPPING_MODULE_MODULE,
            "test_ac_dynamic.py": DYNAMIC_START_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertRegex(
            err, r"(?m)^REFUSED: tests/test_ab_modskip\.py: 1 loaded, "
            r"0 credited starts \(")
        self.assertNotIn("tests/test_ac_dynamic.py", err)
        self.assertNotIn(_SENTINEL_PREFIX, err)

    def _assert_refusal_names_no_cause(self, err: str) -> None:
        """The zero-credited refusal states what the gate observed, not a
        cause it cannot know (3b525 round-9 review, claude W)."""
        for line in err.splitlines():
            if "credited starts" in line:
                for cause in ("SkipTest", "setUpModule", "setUpClass",
                              "none of"):
                    self.assertNotIn(cause, line)

    def _run_gate_with(self, files: dict[str, str],
                       root_files: dict[str, str] | None = None):
        """The real gate on a synthetic tree holding a passing
        tests/test_zz_ok.py plus ``files`` (tests/-relative name: body)
        and ``root_files`` (repository-root-relative name: body)."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_ok.py"])
        for rel, body in files.items():
            (root / "tests" / rel).write_text(body)
        for rel, body in (root_files or {}).items():
            (root / rel).write_text(body)
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            return self._call_main(runner, repo_root=root)

    def test_main_credits_tests_in_the_modules_loaded_suite(self) -> None:
        """A started test is credited to the module whose loaded suite
        contains it, whatever type holds it (3b525 round-9 and round-10
        reviews: defining-code crediting refused several of these with
        unittest's OK): a FunctionTestCase wrapping the module's own
        function, one wrapping a functools.partial, a DocTestSuite of
        the module itself, a DocTestSuite of a library module outside
        tests/, a DocFileSuite found through a package, a class built by
        a factory in a helper module outside the run list, and a test
        object of no known case type."""
        cases = (
            ("function_test_case",
             {"test_aa_function.py": FUNCTION_TEST_CASE_MODULE}, {},
             "testsRun=2 notStarted=0"),
            ("functools_partial",
             {"test_aa_partial.py": PARTIAL_MODULE}, {},
             "testsRun=2 notStarted=0"),
            ("doctest_suite_own_module",
             {"test_aa_doctest.py": DOCTEST_SUITE_MODULE}, {},
             "testsRun=2 notStarted=0"),
            ("doctest_suite_library_module",
             {"test_aa_doclib.py": DOCTEST_LIBRARY_MODULE},
             {"doctest_library.py": DOCTEST_LIBRARY},
             "testsRun=2 notStarted=0"),
            ("docfile_suite_package",
             {"test_aa_docfile.py": DOCFILE_SUITE_MODULE,
              "docfile_example.txt": DOCFILE_TEXT}, {},
             "testsRun=2 notStarted=0"),
            ("helper_factory_class",
             {"helper_factory.py": HELPER_FACTORY,
              "test_aa_factory.py": HELPER_FACTORY_MODULE}, {},
             "testsRun=2 notStarted=0"),
            ("unknown_case_type",
             {"helper_probe.py": HELPER_PROBE,
              "test_aa_probe.py": UNKNOWN_CASE_TYPE_MODULE}, {},
             "testsRun=2 notStarted=0"),
        )
        for label, files, root_files, counts in cases:
            with self.subTest(label=label):
                code, _out, err = self._run_gate_with(files, root_files)
                self.assertEqual(code, 0, err)
                self.assertNotIn("REFUSED", err)
                self.assertIn(counts, err)
                self.assertIn(_SENTINEL_PREFIX, err)

    def test_main_refuses_helper_setupmodule_skip_by_reconciliation(
            self) -> None:
        """A SkipTest in the setUpModule of a helper outside the run list
        keeps its imported class from starting; the handed module still
        has a credited start, so the parent's reconciliation refuses the
        run, and its message names only the setUpClass holders that
        notStarted counts (3b525 round-9 review, N2)."""
        code, _out, err = self._run_gate_with({
            "helper_moduleskip.py": HELPER_MODULE_SKIP,
            "test_aa_helperskip.py": HELPER_MODULE_SKIP_IMPORTING_MODULE,
        })
        self.assertEqual(code, 2, err)
        self.assertIn("OK (skipped=1)", err)
        self.assertIn("testsRun=2 notStarted=0", err)
        refusal = [line for line in err.splitlines()
                   if line.startswith("REFUSED: ")]
        self.assertEqual(len(refusal), 1, err)
        self.assertIn("notStarted=0", refusal[0])
        self.assertIn("setUpModule SkipTest", refusal[0])
        self.assertIn("are not counted", refusal[0])

    def test_main_green_with_decorator_skipped_class_beside_running_class(
            self) -> None:
        """Control for the class-decorator rule (3b525 round-8 review,
        N1): a decorator-skipped class does not refuse a module that
        starts a test of another class it defines. The decorated class's
        test still reaches startTest, so testsRun counts it and
        notStarted stays 0. Loaded: 2 + 1 = 3; testsRun=3."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_ok.py"])
        (root / "tests" / "test_aa_decorated.py").write_text(
            DECORATOR_SKIPPED_BESIDE_RUNNING_MODULE)
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 0, err)
        self.assertNotIn("REFUSED", err)
        self.assertIn("OK (skipped=1)", err)
        self.assertIn("testsRun=3 notStarted=0", err)

    def test_main_forwards_failure_when_fixture_errors(self) -> None:
        """A setUpModule, or a module's only setUpClass, that raises an
        error (not SkipTest) fails the run on unittest's own terms: the
        exit stays unittest's 1 and no zero-started refusal names a
        SkipTest cause the run did not have (3b525 round-8 review, N2:
        before this the run printed that refusal and exited 2)."""
        runner = self._runner()
        cases = (
            ("setupmodule_runtimeerror", ERRORING_SETUPMODULE_MODULE,
             "module fixture broke"),
            ("setupclass_runtimeerror", ERRORING_SETUPCLASS_MODULE,
             "class fixture broke"),
        )
        for label, body, message in cases:
            with self.subTest(label=label):
                root = self._tmp_repo(["test_zz_ok.py"])
                (root / "tests" / "test_aa_errors.py").write_text(body)
                with mock.patch.dict(os.environ, _minimal_environ(),
                                     clear=True):
                    code, _out, err = self._call_main(runner, repo_root=root)
                self.assertEqual(code, 1, err)
                self.assertIn("FAILED (errors=1)", err)
                self.assertIn(message, err)
                self.assertNotIn("REFUSED", err)
                self.assertIn("wasSuccessful=False", err)

    def test_main_refuses_module_that_defines_no_tests(self) -> None:
        """A module that imports cleanly but defines no tests is refused
        with a message naming it, beside a module that runs (3b525
        round 8, W1). The driver's pre-run zero-test-cases check names
        it first; the post-run zero-started check names it too when
        that pre-run check is absent, so either layer alone keeps this
        refusal naming the file (the parent's sentinel check would
        still refuse, but without naming the module)."""
        runner = self._runner()
        root = self._tmp_repo(["test_zz_ok.py"])
        (root / "tests" / "test_aa_notests.py").write_text(
            "import unittest\n\n\n"
            "class NotATestCase:\n"
            "    def test_looks_like_a_test(self):\n"
            "        pass\n")
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 2, err)
        self.assertRegex(err, r"(?m)^REFUSED: .*tests/test_aa_notests\.py")
        self.assertNotIn("tests/test_zz_ok.py", err)

    def test_main_passing_output_forwards_unittest_output(self) -> None:
        """The passing output contract (3b525 round 8, W2): stdout is the
        module list alone; stderr is unittest's own output for the same
        modules, unchanged, followed by the sentinel as its one extra,
        last line. Compared against a direct `python -m unittest` run of
        the same tree, with only the elapsed time normalised."""
        root = self._tmp_repo(["test_a.py", "test_b.py"],
                              body=PASSING_WITH_SKIP_MODULE)
        wrapper = (
            "import runpy, sys\n"
            "from pathlib import Path\n"
            "ns = runpy.run_path(sys.argv[1])\n"
            "sys.exit(ns['main'](repo_root=Path(sys.argv[2])))\n")
        gate = subprocess.run(
            [sys.executable, "-c", wrapper, str(RUNNER_PATH), str(root)],
            capture_output=True, env=_minimal_environ(), timeout=120)
        direct = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.test_a", "tests.test_b"],
            cwd=str(root), capture_output=True, env=_minimal_environ(),
            timeout=120)
        gate_err = gate.stderr.decode("utf-8", "replace")
        self.assertEqual(gate.returncode, 0, gate_err[-500:])
        self.assertEqual(direct.returncode, 0, direct.stderr[-500:])
        self.assertEqual(
            gate.stdout.decode("utf-8", "replace"),
            "Running test modules:\n  tests.test_a\n  tests.test_b\n")
        body, _, last = gate_err.rstrip("\n").rpartition("\n")
        self.assertRegex(
            last,
            r"^REGRESSION-GATE-RESULT [0-9a-f]{32} testsRun=4 notStarted=0 "
            r"wasSuccessful=True tests\.test_a=2 tests\.test_b=2$")

        def normalise(text):
            return re.sub(r" in \d+\.\d+s", " in Ts", text)

        self.assertEqual(
            normalise(body + "\n"),
            normalise(direct.stderr.decode("utf-8", "replace")))
        self.assertIn("OK (skipped=2)", body)

    def test_main_refuses_setup_systemexit_with_spoofed_summary(self) -> None:
        """A green summary written by a test (standing in for a grandchild
        that inherits stderr) followed by a SystemExit(0) escaping from
        setUpClass cannot pass as green: the sentinel never appears, so
        the run is refused (3b525 round 2, F3)."""
        runner = self._runner()
        root = self._tmp_repo(["test_aa_spoof.py"])
        (root / "tests" / "test_aa_spoof.py").write_text(
            "import os\n"
            "import unittest\n\n\n"
            "class SpoofTests(unittest.TestCase):\n"
            "    def test_writes_summary(self):\n"
            "        os.write(2, b'Ran 1 test in 0.000s\\n\\nOK\\n')\n")
        (root / "tests" / "test_zz_exit.py").write_text(
            "import unittest\n\n\n"
            "class ExitTests(unittest.TestCase):\n"
            "    @classmethod\n"
            "    def setUpClass(cls):\n"
            "        raise SystemExit(0)\n\n"
            "    def test_never_runs(self):\n"
            "        self.fail('must be reached or refused')\n")
        with mock.patch.dict(os.environ, _minimal_environ(), clear=True):
            code, _out, err = self._call_main(runner, repo_root=root)
        self.assertEqual(code, 2, err)
        self.assertIn("REFUSED", err)
        self.assertIn("sentinel", err)

    def test_main_prints_refused_on_its_own_line(self) -> None:
        """A refusal after the child never rides the child's unterminated
        progress-dot line: it always starts at a line start."""
        runner = self._runner()
        fake = _FakePopen(summary=b"....", sentinel=False)
        code, _out, err = self._call_main(runner, popen=fake)
        self.assertEqual(code, 2)
        self.assertNotIn(".REFUSED", err)
        self.assertRegex(err, r"(?m)^REFUSED: ")

    def test_main_flushes_stdout_before_child(self) -> None:
        """With stdout a pipe, the module list is flushed before the child
        starts, so it precedes the child's output instead of appearing
        after the whole run (3b525 round 2, F6)."""
        root = self._tmp_repo(["test_a.py", "test_b.py"])
        wrapper = (
            "import runpy, sys\n"
            "from pathlib import Path\n"
            "ns = runpy.run_path(sys.argv[1])\n"
            "sys.exit(ns['main'](repo_root=Path(sys.argv[2])))\n")
        result = subprocess.run(
            [sys.executable, "-c", wrapper, str(RUNNER_PATH), str(root)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env=_minimal_environ(), timeout=120)
        text = result.stdout.decode("utf-8", "replace")
        self.assertEqual(result.returncode, 0, text[-500:])
        self.assertIn("Running test modules:", text)
        self.assertIn("Ran 2 tests", text)
        self.assertLess(text.index("Running test modules:"),
                        text.index("Ran 2 tests"),
                        "the module list must be flushed before the child "
                        "writes its output")

    # Every refusal the runner can make; BOTH documentation surfaces
    # (tests/README.md and tools/README.md) must list each of them, so
    # neither can drift stale again (3b525 rounds 2 and 3, F7/F3).
    _README_REFUSAL_NEEDLES = (
        "does not match",   # run-list / driver-argv mismatch
        "nested",           # nested test file
        "symlink",          # symlinked subdirectory
        "cannot inspect",   # unreadable subdirectory
        "package directory",
        "no `tests/test_*.py` files",
        "cannot be imported",
        "zero test cases",
        "Ran N tests",
        "sentinel",
        "nonce",
        "stdin",            # nonce delivery channel (round 3, F1)
        "notStarted",       # class/module-level skip accounting (F4)
        "0 credited starts",  # module with no credited start (W1)
        "cannot be paired",  # unittest.main load not paired with modules
        "more than one module",  # one case object in two modules' suites
    )

    # The key phrase of each crediting residual and of the pairing-check
    # wording; the runner docstring and both READMEs must carry every one
    # (3b525 round-13 review: agy W, codex W, claude N1 and N2; round 15:
    # every residual, and the per-run notStarted rule; round 16: its
    # stretch limit and one run's further records discarded).
    _RESIDUAL_PHRASES = (
        # the pairing check compares counts, not identity
        "compares case counts per suite, not case identity",
        # a test starting another loaded case can move the match
        "itself starts another loaded case object",
        "can move the match",
        # reordering, dropping or substituting suites, in run or __iter__
        "a suite that reorders, drops or substitutes cases, in its own "
        "run or its __iter__",
        # non-suite test objects that run inner cases
        "a test object that is not a suite but runs inner cases",
        "flattened order",
        # a dropping suite needs no shared object for a false pass
        "a dropping suite can produce a false pass without a shared "
        "case object",
        # the pairing check itself: a different count fails it
        "returns a different case count on a second load fails this",
        # borrowing another module's TestCase classes earns credit
        "earns credit for their started tests (borrowing",
        # individually skipped tests are credited starts
        "a skip decorator on the test method, or self.skipTest inside "
        "the test or its setUp) is a credited start",
        "a module whose every test is skipped individually is not "
        "refused",
        # a partially hollowed module is not detected
        "hollowed module (a load_tests that returns some but not all of "
        "a module's tests)",
        # in-process forgery
        "test code can forge the result in-process",
        # notStarted: one skip record per run of one class object
        "setUpClass once per run of consecutive cases of the same class "
        "object",
        "two classes sharing a module and qualname are two runs",
        "one skip record never covers two runs",
        # the stretch limit: records since the previous matched start
        "since the previous matched start",
        "arrived in that stretch",
        # round 16: a class cleanup's skip gives one run a second record
        # (round 17: worded as at most one counted record per run; round
        # 19: this phrase replaced the old "never yields two records"
        # clause in place, so restoring that clause drops it and fails
        # here, and no negative check on the old words is kept, since it
        # also fired on a correction quoting them; round 20: anchored to
        # the preceding clause and its colon, so a negation inserted
        # between them, as "It is false that one run contributes ...",
        # fails here)
        "one skip record never covers two runs; one run contributes at "
        "most one counted record:",
        "recorded under the same setUpClass name",
        "not credited to a later run",
        # round 17: "back to back" defined as the code applies it
        "arriving back to back (no start and no other skip record in "
        "between) with the same holder and the same _previousTestClass",
        # round 17: the rule relies on a private unittest attribute
        "depends on unittest's private _previousTestClass attribute and "
        "its set-up order",
        "read in CPython 3.14 and 3.11 suite.py",
        "a change there could misgroup records",
        # round 18: an absent attribute is refused, not read as None
        "has no _previousTestClass attribute at all as a setUpClass skip "
        "record arrives, the run is refused (exit 2, naming "
        "_previousTestClass and the Python version), never grouped by a "
        "default",
    )

    def test_docs_state_crediting_residuals_in_agreement(self) -> None:
        """The runner docstring and both READMEs state every crediting
        residual, the pairing-check wording and the per-run notStarted
        rule in the same words (markup and line breaks aside) (3b525
        rounds 13, 14 and 15). The one-run rule is pinned by its
        positive phrase alone (round 19: a negative check on the old
        wording failed a correction that quoted it), anchored to the
        clause before it (round 20). The pairing-check wording is also
        pinned by its positive phrase alone (round 22: the last negative
        check, on "different suite on a second load", was removed for
        the same reason). Every check
        here is an assertIn, so these wording checks establish only
        that the listed text is present; they cannot detect added text
        that contradicts it, before, after or elsewhere on a surface
        (round 20 showed both a negation placed before the anchored
        clause and a "correction" sentence appended after it pass)."""
        surfaces = {"runner docstring": self._runner()["__doc__"] or ""}
        for rel in ("tools/README.md", "tests/README.md"):
            surfaces[rel] = (REPO_ROOT / rel).read_text(encoding="utf-8")
        for label, text in surfaces.items():
            flat = " ".join(text.replace("`", "").split())
            for phrase in self._RESIDUAL_PHRASES:
                with self.subTest(surface=label, phrase=phrase):
                    self.assertIn(phrase, flat)

    def test_readme_documents_complete_regression_command(self) -> None:
        """tests/README.md names the runner as the complete regression
        command, labels the direct module command's narrower scope, and
        lists every refusal the runner can make."""
        text = (REPO_ROOT / "tests" / "README.md").read_text(encoding="utf-8")
        self.assertIn("python3 tools/run-linter-regression.py", text)
        self.assertIn("complete regression command", text)
        self.assertIn("narrower scope", text)
        for refusal in self._README_REFUSAL_NEEDLES:
            self.assertIn(refusal, text,
                          "tests/README.md must list the %r refusal"
                          % refusal)

    def test_tools_readme_documents_runner_refusals(self) -> None:
        """tools/README.md's gate-36 description stays in line with
        tests/README.md: every refusal listed on both surfaces (3b525
        round 3, F3: tools/README.md was the stale surface)."""
        text = (REPO_ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        for refusal in self._README_REFUSAL_NEEDLES:
            self.assertIn(refusal, text,
                          "tools/README.md must list the %r refusal"
                          % refusal)

    def test_linters_module_is_on_disk(self) -> None:
        """tests/test_linters.py hosts most other guards (including the
        runner's sha256 inventory pin and the reciprocal executed-argv
        check); its outright deletion must fail here, in a module whose
        presence does not depend on it."""
        self.assertTrue((REPO_ROOT / "tests" / "test_linters.py").is_file())


if __name__ == "__main__":
    unittest.main()
