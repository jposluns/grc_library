"""Gate 36 regression-gate guard tests (the 3b525 round-2 findings).

These tests guard the gate runner itself, so they live OUTSIDE
``tests/test_linters.py``: a discovery or run-list regression that
drops ``tests/test_linters.py`` (which hosts most other guards,
including the runner's sha256 inventory pin) cannot also drop this
module's completeness check. The runner additionally carries its own
in-process completeness self-check, which no test-module edit can
remove; these tests exercise that self-check and the runner's refusal
paths hermetically, against synthetic repository-shaped trees and an
injected child runner, so no flip can pass by skipping execution.
"""

from __future__ import annotations

import contextlib
import io
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNNER_PATH = REPO_ROOT / "tools" / "run-linter-regression.py"

GREEN_SUMMARY = b"Ran 3 tests in 0.001s\n\nOK\n"


class _FakeResult:
    def __init__(self, returncode: int, stderr: bytes) -> None:
        self.returncode = returncode
        self.stderr = stderr


class _FakeRun:
    """Stands in for subprocess.run inside main(); records each command."""

    def __init__(self, returncode: int = 0,
                 stderr: bytes = GREEN_SUMMARY) -> None:
        self.commands = []
        self._result = _FakeResult(returncode, stderr)

    def __call__(self, cmd, **kwargs):
        self.commands.append(list(cmd))
        return self._result


class RegressionGateCompletenessTests(unittest.TestCase):
    """main() runs every top-level tests/test_*.py, or refuses loud."""

    def _runner(self):
        return runpy.run_path(str(RUNNER_PATH))

    def _call_main(self, runner, **kwargs):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = runner["main"](**kwargs)
        return code, out.getvalue(), err.getvalue()

    def _tmp_repo(self, test_files):
        root = Path(tempfile.mkdtemp(prefix="gate36-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "tests").mkdir()
        (root / "tests" / "__init__.py").write_text("")
        for rel in test_files:
            path = root / "tests" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("import unittest\n")
        return root

    def test_main_executed_list_covers_every_test_file(self) -> None:
        """The module list main() actually hands to the child subprocess
        (not discovery alone) covers every on-disk tests/test_*.py."""
        runner = self._runner()
        fake = _FakeRun()
        code, _out, err = self._call_main(runner, run=fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(len(fake.commands), 1)
        # Command shape: [sys.executable, "-c", driver, *modules].
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

        fake = _FakeRun()
        namespace["discover_test_modules"] = narrowed
        try:
            code, _out, err = self._call_main(runner, run=fake)
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
        fake = _FakeRun()
        code, out, err = self._call_main(runner, repo_root=root, run=fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(fake.commands[0][3:],
                         ["tests.test_a", "tests.test_b"])
        self.assertIn("tests.test_a", out)

    def test_main_refuses_nested_test_file(self) -> None:
        """Only top-level tests/test_*.py files are in scope; a test file
        in a tests/ subdirectory is refused by name, never skipped."""
        runner = self._runner()
        root = self._tmp_repo(["test_a.py", "sub/test_nested.py"])
        fake = _FakeRun()
        code, _out, err = self._call_main(runner, repo_root=root, run=fake)
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", err)
        self.assertIn("test_nested.py", err)
        self.assertIn("only top-level", err)
        self.assertEqual(fake.commands, [])

    def test_import_refusal_catches_base_exception(self) -> None:
        """An import-time SystemExit(0), or any other BaseException, is a
        refusal naming the file (exit 2), never a green run."""
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
                     "tests.test_ok", "tests.test_boom"],
                    cwd=str(root), capture_output=True, timeout=120)
                self.assertEqual(result.returncode, 2, result.stderr[-500:])
                self.assertIn(b"REFUSED: cannot import tests/test_boom.py",
                              result.stderr)

    def test_main_refuses_green_exit_without_summary_line(self) -> None:
        """A child exit of 0 is believed only when unittest's output has a
        'Ran N tests' line with N at least 1; failures stay forwarded."""
        runner = self._runner()
        cases = (
            ("no_summary", 0, b"", 2),
            ("ran_zero", 0, b"Ran 0 tests in 0.000s\n\nOK\n", 2),
            ("ran_one", 0, b"Ran 1 test in 0.001s\n\nOK\n", 0),
            ("ran_many", 0, GREEN_SUMMARY, 0),
            ("failure_forwarded", 1,
             b"Ran 5 tests in 0.100s\n\nFAILED (failures=1)\n", 1),
        )
        for label, returncode, stderr, expected in cases:
            with self.subTest(label=label):
                fake = _FakeRun(returncode=returncode, stderr=stderr)
                code, _out, err = self._call_main(runner, run=fake)
                self.assertEqual(code, expected, err)
                if returncode == 0 and expected == 2:
                    self.assertIn("REFUSED", err)
                    self.assertIn("Ran N tests", err)

    def test_readme_documents_complete_regression_command(self) -> None:
        """tests/README.md names the runner as the complete regression
        command and labels the direct module command's narrower scope."""
        text = (REPO_ROOT / "tests" / "README.md").read_text(encoding="utf-8")
        self.assertIn("python3 tools/run-linter-regression.py", text)
        self.assertIn("complete regression command", text)
        self.assertIn("narrower scope", text)

    def test_linters_module_is_on_disk(self) -> None:
        """tests/test_linters.py hosts most other guards (including the
        runner's sha256 inventory pin); its outright deletion must fail
        here, in a module whose presence does not depend on it."""
        self.assertTrue((REPO_ROOT / "tests" / "test_linters.py").is_file())


if __name__ == "__main__":
    unittest.main()
