"""The reviewed store-dependent gate 36 subset stays complete and wired.

CI has no private store (``GRC_STORE`` / ``<repo-parent>/private``), no
``grc_library_private`` sibling and no ``grc_library_ref`` sibling, so a
gate-36 test that skips or silently no-ops without them never executes on
the merge path (round-1 review, E1). The reviewed list
``tests/store-dependent-tests.txt`` names that subset (found by
observation: a CI-mode run, GRC_STORE at an empty directory and no
siblings, against a maintainer-inputs run), and the pre-push guard runs
exactly that list on every push through
``tools/run-store-dependent-tests.py``.

This module is the regression guard the round-1 review asked for: a
STATIC SCAN of the suite (skipTest calls and early returns guarded by a
store or sibling probe, and conditional-expression fallbacks on one, the
sanctioned ``skipTest`` / ``resolve_working`` scan) whose output must
equal the committed list, so a new store-dependent test that is not added
to the list fails here, in CI, where such a test otherwise goes silent.

What the scan reads as a STORE PROBE: ``REPO_ROOT.parent`` joined with a
path, a string holding ``grc_library_private`` or ``grc_library_ref``, a
``PTODO_PATH`` attribute, a ``resolve_working`` / ``resolve_working_dir``
call without a ``repo_root``/``root`` override, and a local variable
assigned from one of those; a same-class helper's probes count for its
caller (inlined two levels), a helper that returns None under a probe
makes its caller's ``is None`` guard a probe, and a probe-guarded skip in
``setUp`` or ``setUpClass`` flags every test of the class. Residuals,
accepted and reviewed here rather than hidden: a probe routed through a
module-level helper, another module, or a subprocess is not seen (the
live suite holds none; the observation runs are the backstop), and a
flagged test whose probe is genuinely fixture-local would be a false
positive to review, not to silence.

Also pinned here (round-1 findings 5 and 6): the nightly sweep installs
the pinned dependencies before running the audits, as quality.yml does,
and tools/run_all_audits.sh's rationale states the split that actually
holds. Stdlib-only Python 3.11.
"""

from __future__ import annotations

import ast
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIST_PATH = REPO_ROOT / "tests" / "store-dependent-tests.txt"
RUNNER_TOOL = REPO_ROOT / "tools" / "run-store-dependent-tests.py"

SIBLING_LITERALS = ("grc_library_private", "grc_library_ref")
RESOLVERS = {"resolve_working", "resolve_working_dir"}
PROBE_ATTRS = {"PTODO_PATH"}
FIXTURE_METHODS = ("setUp", "setUpClass")


def _expr_names(node: ast.AST) -> set[str]:
    names = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name):
            names.add(sub.id)
        elif isinstance(sub, ast.Attribute):
            names.add(sub.attr)
    return names


def _contains_probe(node: ast.AST, probe_locals: set[str]) -> bool:
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            if any(literal in sub.value for literal in SIBLING_LITERALS):
                return True
        if isinstance(sub, ast.Attribute):
            if sub.attr in PROBE_ATTRS:
                return True
            if sub.attr == "parent" and "REPO_ROOT" in _expr_names(sub.value):
                return True
        if isinstance(sub, ast.Call):
            name = (getattr(sub.func, "attr", None)
                    or getattr(sub.func, "id", None))
            if name in RESOLVERS and not any(
                    kw.arg in ("repo_root", "root") for kw in sub.keywords):
                return True
        if isinstance(sub, ast.Name) and sub.id in probe_locals:
            return True
    return False


def _is_skip_call(node: ast.AST) -> bool:
    return (isinstance(node, ast.Call)
            and (getattr(node.func, "attr", None) == "skipTest"
                 or getattr(node.func, "id", None) == "skipTest"))


def _analyze(func: ast.FunctionDef, methods: dict[str, ast.FunctionDef],
             depth: int = 0, seen: frozenset = frozenset()):
    """(skips_on_probe, noops_on_probe, returns_none_on_probe) for one
    method, with same-class helper calls inlined up to two levels."""
    probe_locals: set[str] = set()
    helper_none: set[str] = set()
    skips = noop = returns_none = False

    def sub_analysis(name: str):
        if depth >= 2 or name in seen or name not in methods:
            return (False, False, False)
        return _analyze(methods[name], methods, depth + 1,
                        seen | {name})

    for node in ast.walk(func):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            target = node.targets[0].id
            if _contains_probe(node.value, probe_locals):
                probe_locals.add(target)
            if (isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Attribute)
                    and isinstance(node.value.func.value, ast.Name)
                    and node.value.func.value.id == "self"
                    and sub_analysis(node.value.func.attr)[2]):
                helper_none.add(target)
        if isinstance(node, ast.If):
            probed = _contains_probe(node.test, probe_locals) or any(
                isinstance(sub, ast.Name) and sub.id in helper_none
                for sub in ast.walk(node.test))
            if probed:
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Expr) and _is_skip_call(stmt.value):
                        skips = True
                    if isinstance(stmt, ast.Return):
                        if (stmt.value is None
                                or (isinstance(stmt.value, ast.Constant)
                                    and stmt.value.value is None)):
                            returns_none = True
                        else:
                            noop = True
        if isinstance(node, ast.IfExp) and _contains_probe(node.test,
                                                           probe_locals):
            noop = True
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "self"):
            helper = sub_analysis(node.func.attr)
            skips = skips or helper[0]
            noop = noop or helper[1]
    return (skips, noop, returns_none)


def scan_source(source: str, module: str) -> dict[str, str]:
    """{test id: 'skips'|'no-ops'|'skips/no-ops'} for one module's source."""
    flagged: dict[str, str] = {}
    tree = ast.parse(source)
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        methods = {node.name: node for node in cls.body
                   if isinstance(node, ast.FunctionDef)}
        fixture_skips = any(_analyze(methods[name], methods)[0]
                            for name in FIXTURE_METHODS if name in methods)
        for name, func in methods.items():
            if not name.startswith("test_"):
                continue
            skips, noop, _none = _analyze(func, methods)
            skips = skips or fixture_skips
            if skips or noop:
                labels = (["skips"] if skips else []) + (
                    ["no-ops"] if noop else [])
                flagged["%s.%s.%s" % (module, cls.name, name)] = \
                    "/".join(labels)
    return flagged


def scan_suite(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    """The scan over every top-level tests/test_*.py module."""
    flagged: dict[str, str] = {}
    for path in sorted((repo_root / "tests").glob("test_*.py")):
        flagged.update(scan_source(path.read_text(encoding="utf-8"),
                                   "tests." + path.stem))
    return flagged


def _load_runner_tool():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_store_list_runner",
                                                  RUNNER_TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StoreDependentListTests(unittest.TestCase):
    """The committed list equals the static scan, is well formed, and
    names loadable tests."""

    def test_scan_matches_the_reviewed_list(self) -> None:
        """FLIP TABLE (round-1 E1): a store-dependent test missing from
        tests/store-dependent-tests.txt, or a listed test the scan no
        longer finds, fails here. The observed set is the expected set."""
        tool = _load_runner_tool()
        listed = tool.parse_list(LIST_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(listed, list, listed)
        self.assertEqual(
            sorted(scan_suite()), sorted(listed),
            "the static scan of skipTest / resolve_working store probes "
            "and the reviewed list in tests/store-dependent-tests.txt "
            "must name exactly the same tests; update the list (with the "
            "reason) or fix the test")

    def test_listed_tests_load_as_single_methods(self) -> None:
        tool = _load_runner_tool()
        listed = tool.parse_list(LIST_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(listed, list, listed)
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        loader = unittest.TestLoader()
        for test_id in listed:
            with self.subTest(test_id=test_id):
                loaded = loader.loadTestsFromName(test_id)
                self.assertFalse(loader.errors, loader.errors)
                cases = list(loaded)
                self.assertEqual(len(cases), 1)
                self.assertEqual(cases[0].id(), test_id)

    def test_scan_flags_each_known_pattern(self) -> None:
        """The scan's sensitivity is pinned per pattern, so a weakened
        scan fails here even while the live suite happens to match."""
        cases = {
            "sibling skip": (
                "class T(unittest.TestCase):\n"
                "    def test_x(self):\n"
                "        if not (REPO_ROOT.parent / 'grc_library_private'"
                ").is_dir():\n"
                "            self.skipTest('no sibling')\n",
                {"tests.m.T.test_x": "skips"}),
            "local sibling skip": (
                "class T(unittest.TestCase):\n"
                "    def test_x(self):\n"
                "        private = REPO_ROOT.parent / 'grc_library_ref'\n"
                "        if not private.is_dir():\n"
                "            self.skipTest('no sibling')\n",
                {"tests.m.T.test_x": "skips"}),
            "ptodo conditional no-op": (
                "class T(unittest.TestCase):\n"
                "    def test_x(self):\n"
                "        ptodo = tool.PTODO_PATH\n"
                "        text = ptodo.read_text() if ptodo.is_file() "
                "else None\n"
                "        self.assertTrue(check(text))\n",
                {"tests.m.T.test_x": "no-ops"}),
            "helper returning none": (
                "class T(unittest.TestCase):\n"
                "    def _outcome(self):\n"
                "        path = mod.resolve_working('x.md')\n"
                "        if path is None:\n"
                "            return None\n"
                "        return path\n"
                "    def test_x(self):\n"
                "        outcome = self._outcome()\n"
                "        if outcome is None:\n"
                "            self.skipTest('no store')\n",
                {"tests.m.T.test_x": "skips"}),
            "setUp skip flags the class": (
                "class T(unittest.TestCase):\n"
                "    def setUp(self):\n"
                "        if not (REPO_ROOT.parent / 'grc_library_private'"
                ").is_dir():\n"
                "            self.skipTest('no sibling')\n"
                "    def test_x(self):\n"
                "        self.assertTrue(True)\n",
                {"tests.m.T.test_x": "skips"}),
            "fixture-local sibling is not flagged": (
                "class T(unittest.TestCase):\n"
                "    def test_x(self):\n"
                "        root = Path(td) / 'grc_library_ref'\n"
                "        root.mkdir()\n"
                "        self.assertTrue(run(root))\n",
                {}),
            "unrelated skip is not flagged": (
                "class T(unittest.TestCase):\n"
                "    def test_x(self):\n"
                "        if os.geteuid() == 0:\n"
                "            self.skipTest('root')\n"
                "        self.assertTrue(True)\n",
                {}),
            "rooted resolve_working is not flagged": (
                "class T(unittest.TestCase):\n"
                "    def test_x(self):\n"
                "        path = lc.resolve_working('x.md', repo_root=root)\n"
                "        if path is None:\n"
                "            self.skipTest('fixture')\n",
                {}),
        }
        for label, (body, expected) in cases.items():
            with self.subTest(label=label):
                self.assertEqual(scan_source("import unittest\n" + body,
                                             "tests.m"), expected)

    def test_guard_runs_the_list_on_both_paths(self) -> None:
        """The pre-push guard names the list runner on the fast path (a
        fast_step) and the full path (its own step), so neither path can
        drop it silently (the behavioural halves live in the guard fixture
        tests in tests/test_linters.py)."""
        guard = (REPO_ROOT / "tools" / "pre-push-guard.sh").read_text(
            encoding="utf-8")
        calls = [line for line in guard.splitlines()
                 if "tools/run-store-dependent-tests.py" in line
                 and not line.lstrip().startswith("#")]
        self.assertGreaterEqual(
            len(calls), 2,
            "both guard paths must invoke tools/run-store-dependent-"
            "tests.py: %r" % calls)


class StoreDependentRunnerToolTests(unittest.TestCase):
    """tools/run-store-dependent-tests.py fails closed on the list and
    forwards the listed tests' own result."""

    LIST = ("# reviewed list fixture\n"
            "tests.test_one.PassTests.test_passes -- fixture reason\n")

    def _fixture(self, list_text: str | None, module_body: str) -> Path:
        root = Path(tempfile.mkdtemp(prefix="store-list-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "tools").mkdir()
        shutil.copyfile(RUNNER_TOOL, root / "tools" / RUNNER_TOOL.name)
        (root / "tests").mkdir()
        (root / "tests" / "__init__.py").write_text("", encoding="utf-8")
        (root / "tests" / "test_one.py").write_text(module_body,
                                                    encoding="utf-8")
        if list_text is not None:
            (root / "tests" / "store-dependent-tests.txt").write_text(
                list_text, encoding="utf-8")
        return root

    PASSING = ("import unittest\n\n\n"
               "class PassTests(unittest.TestCase):\n"
               "    def test_passes(self):\n"
               "        self.assertTrue(True)\n\n"
               "    def test_other(self):\n"
               "        self.assertTrue(True)\n")
    FAILING = ("import unittest\n\n\n"
               "class PassTests(unittest.TestCase):\n"
               "    def test_passes(self):\n"
               "        self.fail('listed test fails')\n")
    SKIPPING = ("import unittest\n\n\n"
                "class PassTests(unittest.TestCase):\n"
                "    def test_passes(self):\n"
                "        self.skipTest('no store in this clone')\n")

    def _run(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(root / "tools" / RUNNER_TOOL.name)],
            cwd=root, env={"PATH": os.environ.get("PATH", "")},
            capture_output=True, text=True, timeout=120)

    def test_green_skip_and_failure_outcomes(self) -> None:
        green = self._run(self._fixture(self.LIST, self.PASSING))
        self.assertEqual(green.returncode, 0, green.stdout + green.stderr)
        self.assertIn("tests.test_one.PassTests.test_passes", green.stdout)
        skip = self._run(self._fixture(self.LIST, self.SKIPPING))
        self.assertEqual(skip.returncode, 0, skip.stdout + skip.stderr)
        self.assertIn("skipped", skip.stderr)
        red = self._run(self._fixture(self.LIST, self.FAILING))
        self.assertEqual(red.returncode, 1, red.stdout + red.stderr)

    def test_list_refusals_fail_closed(self) -> None:
        """FLIP TABLE (round-1 E1): an unreadable or empty list, a
        malformed or duplicate line, and a missing listed test each
        refuse (exit 2), so the push fails rather than silently running
        nothing."""
        for label, list_text in (
                ("missing list", None),
                ("empty list", "# nothing\n"),
                ("malformed line", "tests.test_one.PassTests.test_passes\n"),
                ("not a method id", "tests.test_one -- whole module\n"),
                ("duplicate", self.LIST
                 + "tests.test_one.PassTests.test_passes -- again\n"),
                ("missing test",
                 "tests.test_one.PassTests.test_gone -- reason\n"),
                ("missing module",
                 "tests.test_zz.PassTests.test_passes -- reason\n")):
            with self.subTest(label=label):
                root = self._fixture(list_text, self.PASSING)
                result = self._run(root)
                self.assertEqual(result.returncode, 2,
                                 result.stdout + result.stderr)
                self.assertIn("REFUSED", result.stderr)

    def test_unreadable_list_refuses(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-000 file")
        root = self._fixture(self.LIST, self.PASSING)
        target = root / "tests" / "store-dependent-tests.txt"
        target.chmod(0)
        self.addCleanup(target.chmod, stat.S_IRUSR | stat.S_IWUSR)
        result = self._run(root)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("REFUSED", result.stderr)


class NightlySweepDependencyTests(unittest.TestCase):
    """Round-1 finding 5: the nightly sweep installs the pinned
    dependencies before running the audits, as quality.yml does."""

    def test_nightly_installs_pinned_dependencies_before_the_audits(self):
        text = (REPO_ROOT / ".github" / "workflows"
                / "nightly-sweep.yml").read_text(encoding="utf-8")
        install = text.find(
            "run: python3 -m pip install -r requirements.txt")
        audits = text.find("run: tools/run_all_audits.sh")
        self.assertGreater(install, -1,
                           "nightly-sweep.yml must install requirements.txt")
        self.assertGreater(audits, -1)
        self.assertLess(install, audits,
                        "the install step must precede the audit run")
        self.assertIn("- name: Install pinned dependencies", text)


class RunnerRationaleTests(unittest.TestCase):
    """Round-1 finding 6 (NOTE): tools/run_all_audits.sh's rationale says
    what is now true about the pre-push split."""

    def test_runner_rationale_states_the_actual_split(self):
        text = (REPO_ROOT / "tools" / "run_all_audits.sh").read_text(
            encoding="utf-8")
        # Comment leaders and line wraps aside, as the gate-36 doc tests
        # read their surfaces.
        flat = " ".join(text.replace("#", " ").split())
        self.assertNotIn(
            "requires the full audit sweep to pass locally before any push",
            flat,
            "the retired phase-completion claim must not return")
        for phrase in (
                "single deterministic invocation of the FULL",
                "EXCEPT the linter regression test",
                "tests/store-dependent-tests.txt",
                "nightly sweep and manual full runs still invoke this "
                "script whole"):
            self.assertIn(phrase, flat)


if __name__ == "__main__":
    unittest.main(verbosity=2)
