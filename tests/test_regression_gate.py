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

_SENTINEL_PREFIX = "REGRESSION-GATE-RESULT "


def _minimal_environ() -> dict[str, str]:
    """Only PATH: child interpreters need nothing else here, and an
    ambient PYTHONPATH/PYTHONSAFEPATH/GIT_* must not reach a fixture."""
    return {"PATH": os.environ.get("PATH", "")}


class _FakeProc:
    def __init__(self, returncode: int, stderr: bytes) -> None:
        self.stderr = io.BytesIO(stderr)
        self.returncode = returncode

    def wait(self) -> int:
        return self.returncode


class _FakePopen:
    """Stands in for subprocess.Popen inside main(); records each command
    and fabricates the driver's stderr: a unittest summary plus (by
    default) a completion sentinel built from the command's own nonce
    and module list, the way the real driver would emit it."""

    def __init__(self, returncode: int = 0, summary: bytes | None = None,
                 sentinel: bool = True, mutate=None,
                 trailer: bytes = b"") -> None:
        self.commands = []
        self._returncode = returncode
        self._summary = summary
        self._sentinel = sentinel
        self._mutate = mutate
        self._trailer = trailer

    def __call__(self, cmd, **kwargs):
        self.commands.append(list(cmd))
        # Command shape: [sys.executable, "-c", driver, nonce, *modules].
        nonce, modules = cmd[3], list(cmd[4:])
        if self._summary is None:
            stderr = b"Ran %d tests in 0.001s\n\nOK\n" % len(modules)
        else:
            stderr = self._summary
        if self._sentinel:
            ran = len(modules)
            ok = "True"
            counts = {name: 1 for name in modules}
            if self._mutate is not None:
                nonce, ran, ok, counts = self._mutate(nonce, ran, ok, counts)
            stderr += ("%s%s testsRun=%d wasSuccessful=%s %s\n" % (
                _SENTINEL_PREFIX, nonce, ran, ok,
                " ".join("%s=%d" % (name, counts[name])
                         for name in sorted(counts)))).encode()
        stderr += self._trailer
        return _FakeProc(self._returncode, stderr)


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
        (not discovery alone) covers every on-disk tests/test_*.py, after
        a per-run nonce the child's sentinel must echo."""
        runner = self._runner()
        fake = _FakePopen()
        code, _out, err = self._call_main(runner, popen=fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(len(fake.commands), 1)
        # Command shape: [sys.executable, "-c", driver, nonce, *modules].
        self.assertRegex(fake.commands[0][3], r"^[0-9a-f]{32}$")
        executed = fake.commands[0][4:]
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
        self.assertEqual(fake.commands[0][4:],
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
                    [sys.executable, "-c", driver, "0" * 32,
                     "tests.test_boom", "tests.test_ok"],
                    cwd=str(root), env=_minimal_environ(),
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
                [sys.executable, "-c", driver, "0" * 32,
                 "tests.test_boom", "tests.test_ok"],
                cwd=str(root), env=_minimal_environ(),
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
            [sys.executable, "-c", driver, "0" * 32, "tests.test_a"],
            cwd=str(root), env=_minimal_environ(),
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
            [sys.executable, "-c", driver, "0" * 32,
             "tests.test_empty", "tests.test_ok"],
            cwd=str(root), env=_minimal_environ(),
            capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 2, result.stderr[-500:])
        self.assertIn(b"REFUSED: tests/test_empty.py contributes zero "
                      b"test cases", result.stderr)
        self.assertNotIn(b"tests/test_ok.py", result.stderr)
        # Control: with real tests in both modules the driver runs them
        # and its LAST stderr line is the sentinel echoing the nonce.
        control = self._tmp_repo(["test_a.py", "test_b.py"])
        result = subprocess.run(
            [sys.executable, "-c", driver, "f" * 32,
             "tests.test_a", "tests.test_b"],
            cwd=str(control), env=_minimal_environ(),
            capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr[-500:])
        last = result.stderr.decode().splitlines()[-1]
        self.assertRegex(
            last,
            r"^REGRESSION-GATE-RESULT f{32} testsRun=2 wasSuccessful=True "
            r"tests\.test_a=1 tests\.test_b=1$")

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

    def test_readme_documents_complete_regression_command(self) -> None:
        """tests/README.md names the runner as the complete regression
        command, labels the direct module command's narrower scope, and
        lists every refusal the runner can make."""
        text = (REPO_ROOT / "tests" / "README.md").read_text(encoding="utf-8")
        self.assertIn("python3 tools/run-linter-regression.py", text)
        self.assertIn("complete regression command", text)
        self.assertIn("narrower scope", text)
        for refusal in (
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
        ):
            self.assertIn(refusal, text,
                          "tests/README.md must list the %r refusal"
                          % refusal)

    def test_linters_module_is_on_disk(self) -> None:
        """tests/test_linters.py hosts most other guards (including the
        runner's sha256 inventory pin and the reciprocal executed-argv
        check); its outright deletion must fail here, in a module whose
        presence does not depend on it."""
        self.assertTrue((REPO_ROOT / "tests" / "test_linters.py").is_file())


if __name__ == "__main__":
    unittest.main()
