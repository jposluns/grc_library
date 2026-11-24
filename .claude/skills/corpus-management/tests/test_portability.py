"""Portability orchestration self-tests with stub Git and audit tools."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
TOOLS = Path(".claude/skills/corpus-management/tools")
PUBLIC = ("build-reference-manifest.py", "verify-reference-modules.py",
          "scan-publication-instruction-content.py")
PRIVATE = ("ref-holds.py", "audit-reference-breadth.py", "audit-claim-precision.py",
           "audit-register-currency.py", "audit-reference-acquisition-gaps.py")


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="portability-test-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = self.base / "repo"
        self.tools = self.repo / TOOLS
        self.tools.mkdir(parents=True)
        shutil.copyfile(ROOT / TOOLS / "check-portability.sh", self.tools / "check-portability.sh")
        self.calls = self.base / "calls"
        self.audit = self.tools / "run_all_audits.sh"
        self.audit.write_text('#!/bin/sh\necho audit >> "$PROBE_LOG"\nexit 0\n')
        self.audit.chmod(0o755)
        for name in PUBLIC:
            (self.tools / name).write_text(
                'import os\nfrom pathlib import Path\n'
                f'with Path(os.environ["PROBE_LOG"]).open("a") as log: log.write({name!r} + "\\n")\n')
        bindir = self.base / "bin"
        bindir.mkdir()
        git = bindir / "git"
        git.write_text("#!/usr/bin/env python3\n"
                       "import os, pathlib, shutil, sys\n"
                       "args = sys.argv[1:]\n"
                       "if 'rev-parse' in args: print('a' * 40)\n"
                       "elif args[0] == 'clone':\n"
                       "    if os.environ.get('CLONE_FAIL'): sys.exit(1)\n"
                       "    shutil.copytree(args[-2], args[-1])\n"
                       "    if os.environ.get('ADD_SIBLING'):\n"
                       "        (pathlib.Path(args[-1]).parent / 'grc_library_private').mkdir()\n"
                       "elif 'checkout' not in args: sys.exit(99)\n")
        git.chmod(0o755)
        self.env = {**os.environ, "PATH": str(bindir) + os.pathsep + os.environ["PATH"],
                    "TMPDIR": str(self.base), "PROBE_LOG": str(self.calls)}

    def run_check(self, code):
        cp = subprocess.run(["bash", str(self.tools / "check-portability.sh")],
                            env=self.env, text=True, capture_output=True, timeout=30)
        self.assertEqual(cp.returncode, code, cp.stdout + cp.stderr)
        self.assertEqual(list(self.base.glob("grc-portability.*")), [])
        return cp

    def test_all_public_probes_run_without_private_tools(self):
        self.assertIn("PORTABILITY: PASS", self.run_check(0).stdout)
        self.assertEqual(self.calls.read_text().splitlines(), ["audit", *PUBLIC])
        for name in PRIVATE:
            self.assertFalse((ROOT / TOOLS / name).exists(), name)
        for name in PUBLIC:
            self.assertTrue((ROOT / TOOLS / name).is_file(), name)

    def test_each_public_failure_is_propagated_and_other_probes_run(self):
        for name in PUBLIC:
            with self.subTest(tool=name):
                path = self.tools / name
                original = path.read_text()
                path.write_text(original + "raise SystemExit(7)\n")
                self.calls.unlink(missing_ok=True)
                cp = self.run_check(1)
                self.assertIn(f"{name} exited 7", cp.stdout)
                self.assertEqual(self.calls.read_text().splitlines(), ["audit", *PUBLIC])
                path.write_text(original)

    def test_each_missing_public_probe_is_a_failure(self):
        for name in PUBLIC:
            with self.subTest(tool=name):
                path = self.tools / name
                original = path.read_bytes()
                path.unlink()
                self.assertIn(f"{name} exited 2", self.run_check(1).stdout)
                path.write_bytes(original)

    def test_audit_failure_is_propagated(self):
        self.audit.write_text('#!/bin/sh\nexit 7\n')
        self.assertIn("run_all_audits rc=7", self.run_check(1).stdout)
        self.assertEqual(self.calls.read_text().splitlines(), list(PUBLIC))

    def test_clone_failure_refuses_before_checks(self):
        self.env["CLONE_FAIL"] = "1"
        self.assertIn("git clone failed", self.run_check(2).stdout)
        self.assertFalse(self.calls.exists())

    def test_sibling_contamination_refuses_before_checks(self):
        self.env["ADD_SIBLING"] = "1"
        self.assertIn("not sibling-free", self.run_check(2).stdout)
        self.assertFalse(self.calls.exists())


if __name__ == "__main__":
    unittest.main()
