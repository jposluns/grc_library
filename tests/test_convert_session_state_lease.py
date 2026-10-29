"""tools/convert-session-state-lease.py (3b679 round 2): bold lease fields to the plain form."""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/convert-session-state-lease.py"
GATE = ROOT / "tools/lint-session-state.py"
PLAIN = ("# Session state: grc\n\n"
         "Active-session: orch-2026-10-04T13:36:00Z\n\n"
         "Status: active\n\n"
         "Operating-mode: attended-autonomous\n"
         "<!-- mode source -->\n<!-- set at resume -->\n\n"
         "Last-heartbeat-UTC: 2026-10-06T14:02:31Z\n\n"
         "Current-task: /orch resume (2026-10-04)\n\n"
         "Worker-dispatches: none\n\n"
         "<!-- history -->\n- 2026-10-06 resumed\n")
BOLD = re.sub(r"(?m)^([A-Z][A-Za-z-]+): ", r"**\1:** ", PLAIN)


class ConvertLeaseTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.lease = Path(self.dir.name) / "session-state.md"

    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(TOOL), "--lease", str(self.lease), *args],
                              capture_output=True, text=True, timeout=60)

    def gate(self):
        env = dict(os.environ, GRC_STORE=self.dir.name)
        return subprocess.run([sys.executable, str(GATE)], cwd=self.dir.name, env=env,
                              capture_output=True, text=True, timeout=60)

    def test_bold_converts_in_place_and_passes_gate(self):
        self.lease.write_text(BOLD)
        inode = self.lease.stat().st_ino
        proc = self.run_tool()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(self.lease.read_text(), PLAIN)
        self.assertEqual(self.lease.stat().st_ino, inode)
        gate = self.gate()
        self.assertEqual(gate.returncode, 0, gate.stderr)
        self.assertIn("lease is well-formed", gate.stdout)
        again = self.run_tool()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("nothing to change", again.stdout)
        self.assertEqual(self.lease.read_text(), PLAIN)

    def test_dry_run_writes_nothing(self):
        self.lease.write_text(BOLD)
        proc = self.run_tool("--dry-run")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("line 3: **Active-session:**", proc.stdout)
        self.assertEqual(self.lease.read_text(), BOLD)

    def test_refusals_write_nothing(self):
        cases = {
            "title": BOLD.replace("grc\n", "grc (concurrency lease)\n", 1),
            "missing": BOLD.replace("**Worker-dispatches:** none\n", ""),
            "duplicate": BOLD + "Status: active\n",
            "duplicate bold": BOLD + "**Status:** released\n",
            "gate fails": BOLD.replace("**Status:** active", "**Status:** winding-down"),
        }
        for name, text in cases.items():
            with self.subTest(case=name):
                self.lease.write_text(text)
                proc = self.run_tool()
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("nothing written", proc.stderr)
                self.assertEqual(self.lease.read_text(), text)

    def test_refuses_symlink_and_non_regular(self):
        target = Path(self.dir.name) / "real.md"
        target.write_text(BOLD)
        self.lease.symlink_to(target)
        self.assertEqual(self.run_tool().returncode, 2)
        self.assertEqual(target.read_text(), BOLD)
        self.lease.unlink()
        self.lease.mkdir()
        self.assertEqual(self.run_tool().returncode, 2)

    def test_r3_fifo_reaches_the_regular_file_check(self):
        # 3b679 r3: O_RDWR | O_NONBLOCK opens a FIFO, so the fstat branch refuses it.
        os.mkfifo(str(self.lease))
        proc = self.run_tool()
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("is not a regular file; nothing written", proc.stderr)

    def test_r3_lock_timeout_refuses(self):
        import fcntl
        import time
        self.lease.write_text(BOLD)
        with open(self.lease, "rb") as held:
            fcntl.flock(held.fileno(), fcntl.LOCK_EX)
            start = time.monotonic()
            proc = self.run_tool()
            elapsed = time.monotonic() - start
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("lock was not acquired within 5 seconds", proc.stderr)
        self.assertGreaterEqual(elapsed, 5)
        self.assertLess(elapsed, 30)
        self.assertEqual(self.lease.read_text(), BOLD)

    def test_r3_inode_recheck_after_lock(self):
        # The path is swapped to another inode while the lock is taken: refused,
        # and neither file is written.
        import importlib.util
        import io
        from contextlib import redirect_stderr, redirect_stdout
        spec = importlib.util.spec_from_file_location("_convert_lease", TOOL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.lease.write_text(BOLD)
        other = Path(self.dir.name) / "other.md"
        other.write_text(BOLD)
        real_lock = module.lock

        def swapping_lock(fd):
            real_lock(fd)
            os.replace(other, self.lease)

        module.lock = swapping_lock
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            code = module.run(str(self.lease), False)
        self.assertEqual(code, 2)
        self.assertIn("no longer names the locked inode; nothing written", stderr.getvalue())
        self.assertEqual(self.lease.read_text(), BOLD)

    def test_lease_is_required(self):
        proc = subprocess.run([sys.executable, str(TOOL)], capture_output=True, text=True,
                              timeout=60)
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
