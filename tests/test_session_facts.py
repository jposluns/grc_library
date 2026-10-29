"""Lease-reader regressions, copied lease shapes and reviewed-source isolation."""
import ast
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
# Shape and timestamps copied from the supplied 2026-10-06 14:06Z live snapshot.
# Operational prose is removed; no private-store access is needed. Since 3b679
# the fields use the plain `Name: value` form (the snapshot was bold).
LIVE = """# Session state: grc (concurrency lease)

Active-session: orch-2026-10-04T13:36:00Z

Status: active

Operating-mode: attended-autonomous
<!-- mode source -->

Last-heartbeat-UTC: 2026-10-06T14:02:31Z

Current-task: /orch resume (2026-10-04)

Worker-dispatches: none
"""
# Historical lease a57b45539449b3ee7b97bf4bbfb862b10d7d9125:
# .working/session-state.md (2026-07-28). Operational prose is scrubbed;
# fields converted to the plain form (3b679).
RELEASED = """# Session State (concurrency lease)

Active-session: none

Status: released

Operating-mode: attended-autonomous

Last-heartbeat-UTC: 2026-07-28T22:35:58Z

Current-task: SESSION CLOSED

Worker-dispatches: none
"""


class SessionFactsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "repo"
        self.store = self.base / "private"
        self.store.mkdir()
        (self.root / "tools").mkdir(parents=True)
        for name in ("handoff-snapshot.py", "session_facts.py", "lint_common.py", "lint-session-state.py"):
            shutil.copyfile(ROOT / "tools" / name, self.root / "tools" / name)
        self.lease = self.store / "session-state.md"
        self.log = self.store / "degradation-watch-log.md"
        self.lease.write_text(LIVE)
        self.log.write_text("- session-start 2026-08-23T11:23:55Z\n")
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        self.env.pop("GRC_STORE", None)  # Exercise the default SIBLING store.
        self.env.pop("ORCH_VERIFY_OWNER", None)

    def runpy(self, code):
        return subprocess.run([sys.executable, "-c", code], cwd=self.root,
                              env=self.env, capture_output=True, text=True)

    def metrics(self, now="2026-10-06T14:06:00+00:00"):
        proc = self.runpy("import runpy\nfrom pathlib import Path\nfrom datetime import datetime\n"
                         "m=runpy.run_path('tools/handoff-snapshot.py')\n"
                         "print(m['session_metrics'](Path.cwd(),datetime.fromisoformat("
                         + repr(now) + ")))\n")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return ast.literal_eval(proc.stdout)

    def cli(self):
        return subprocess.run([sys.executable, "tools/handoff-snapshot.py"],
                              cwd=self.root, env=self.env, capture_output=True, text=True)

    def error(self, name):
        proc = self.cli()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("- **Session:** UNKNOWN (" + name, proc.stdout)
        self.assertIn("- **HEAD:**", proc.stdout)
        self.assertEqual(proc.stderr, "")

    def change(self, a, b):
        self.lease.write_text(self.lease.read_text().replace(a, b))

    def hook(self):
        hooks = self.root / ".claude/hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / ".claude/hooks/surface-session-facts.py", hooks / "surface-session-facts.py")
        transcript = self.base / "transcript.jsonl"
        transcript.write_text(json.dumps({"type": "assistant", "message": {
            "content": [{"type": "text", "text": "session depth"}]}}) + "\n")
        return subprocess.run([sys.executable, "-I", str(hooks / "surface-session-facts.py")],
                              input=json.dumps({"transcript_path": str(transcript)}),
                              cwd=self.root, env=dict(self.env, CLAUDE_PROJECT_DIR=str(self.root)),
                              capture_output=True, text=True)

    def test_live_lease_beats_old_and_new_log(self):
        for stamp in ("2026-08-23T11:23:55Z", "2026-10-06T14:05:00Z"):
            self.log.write_text("- session-start " + stamp + "\n")
            facts = self.metrics()
            self.assertEqual(facts["start"], "2026-10-04T13:36:00Z")
            self.assertEqual(facts["elapsed"], "48h30m")
            self.assertIn("convention", facts["start_source"])


    def test_unknown_ids_fullmatch(self):
        for value in ("69556d8c", "sess-20260916T230059Z", "claude/example", "orch-20261004T133600Z",
                      "orch-2026-10-04T13:36:00Z-extra", "orch-2026-02-30T13:36:00Z", "orch-2026-10-04T13:36Z"):
            self.lease.write_text(LIVE.replace("orch-2026-10-04T13:36:00Z", value))
            facts = self.metrics()
            self.assertEqual(facts["start"], "UNKNOWN")
            self.assertEqual(facts["elapsed"], "UNKNOWN")
            self.assertEqual(facts["compaction_rows"], "UNKNOWN")
            self.assertIn("lease id does not record one", facts["start_source"])

    def test_missing_lease_is_unknown_not_old_log(self):
        self.lease.unlink()
        facts = self.metrics()
        self.assertEqual(facts["start"], "UNKNOWN")
        self.assertEqual(facts["elapsed"], "UNKNOWN")
        self.assertIn("start UNKNOWN, elapsed UNKNOWN", self.cli().stdout)

    def test_status_case_release_and_only_live_statuses(self):
        for status in ("Active", "WINDING-DOWN"):
            self.lease.write_text(LIVE.replace("Status: active", "Status: " + status))
            self.assertEqual(self.metrics()["start"], "2026-10-04T13:36:00Z")
        self.lease.write_text(RELEASED.replace("released", "Released"))
        self.error("SESSION_START_RELEASED")
        self.lease.write_text(LIVE.replace("orch-2026-10-04T13:36:00Z", "NONE"))
        self.error("SESSION_START_RELEASED")
        self.lease.write_text(LIVE.replace("Status: active", "Status: idle"))
        self.assertEqual(self.metrics()["start"], "UNKNOWN")

    def test_future_start_snapshot_unknown(self):
        self.change("orch-2026-10-04T13:36:00Z", "orch-2099-01-01T00:00:00Z")
        self.error("SESSION_START_FUTURE")

    def test_missing_and_unreadable_log(self):
        self.log.unlink()
        self.assertIn("compactions: no log", self.cli().stdout)
        self.assertIn("compactions: no log", self.hook().stdout)
        self.log.mkdir()
        self.error("COMPACTIONS_UNREADABLE")

    def test_unsearchable_store_strict_lookup(self):
        self.store.chmod(0)
        try:
            self.error("SESSION_START_UNREADABLE")
        finally:
            self.store.chmod(0o700)

    def test_unreadable_lease(self):
        self.lease.write_bytes(b"\xff")
        self.error("SESSION_START_UNREADABLE")

    def test_stale_cap_and_exact_24h_boundary(self):
        self.log.write_text(
            "| 2026-10-04T13:35:59Z | compaction | before |\n"
            "| 2026-10-04T13:36:00Z | compaction | equal |\n"
            "| 2026-10-06T14:02:31Z | compaction | heartbeat |\n"
            "| 2026-10-06T14:02:32Z | compaction | after |\n"
            "| 2099-01-01T00:00:00Z | compaction | future |\n"
            "| 2026-10-05T14:00Z | considered | quote | compaction | decoy |\n")
        fresh = self.metrics("2026-10-07T14:02:31+00:00")
        self.assertEqual(fresh["lease_warning"], "")
        self.assertEqual(fresh["compaction_rows"], 3)
        stale = self.metrics("2026-10-07T14:02:32+00:00")
        self.assertIn("older than 24h", stale["lease_warning"])
        self.assertEqual(stale["elapsed"], "48h26m")
        self.assertEqual(stale["compaction_rows"], 2)

    def test_hook_shared_reader_spacing_and_fail_open(self):
        proc = self.hook()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        message = json.loads(proc.stdout)["systemMessage"]
        self.assertIn("session-start 2026-10-04T13:36:00Z UTC", message)
        self.assertIn("convention", message)
        self.assertNotIn("  ", message)
        self.lease.write_text(RELEASED)
        proc = self.hook()
        self.assertEqual((proc.returncode, proc.stdout), (0, ""))

    def test_hook_compactions_bounded_at_lease(self):
        self.lease.write_text(LIVE.replace("2026-10-04T13:36:00Z", "2020-01-01T00:00:00Z").replace(
            "2026-10-06T14:02:31Z", "2020-01-01T01:00:00Z"))
        self.log.write_text("| 2019-12-31T23:59:59Z | compaction | before |\n"
                            "| 2020-01-01T00:00:00Z | compaction | start |\n"
                            "| 2020-01-01T01:00:00Z | compaction | end |\n"
                            "| 2020-01-01T01:00:01Z | compaction | after |\n")
        message = json.loads(self.hook().stdout)["systemMessage"]
        self.assertIn("length 1h0m", message)
        self.assertIn("compactions this session: 2", message)
        self.assertIn("STALE HEARTBEAT", message)
        self.assertNotIn("  ", message)

    def test_reviewed_loader_symlinks(self):
        for name in ("session_facts.py", "lint_common.py"):
            path = self.root / "tools" / name
            target = self.base / name
            shutil.move(path, target)
            path.symlink_to(target)
            try:
                proc = self.hook()
                self.assertEqual(proc.returncode, 2, proc.stderr)
                self.assertIn("symlink", proc.stderr)
            finally:
                path.unlink()
                shutil.move(target, path)
        # Exercise the helper's own guard, without hook-loader protection.
        path = self.root / "tools/lint_common.py"
        target = self.base / "lint_common.py"
        shutil.move(path, target)
        path.symlink_to(target)
        proc = self.runpy("import runpy\nrunpy.run_path('tools/session_facts.py')\n")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("symlink", proc.stderr)

    def test_reviewed_source_ignores_planted_bytecode_and_stdlib(self):
        import py_compile
        helper = self.root / "tools/session_facts.py"
        cache = Path(importlib.util.cache_from_source(str(helper)))
        marker = self.base / "executed"
        decoy = self.base / "decoy.py"
        decoy.write_text("open(" + repr(str(marker)) + ", 'w').write('executed')\n")
        (self.root / "tools/datetime.py").write_bytes(decoy.read_bytes())
        cache.parent.mkdir()
        py_compile.compile(str(decoy), cfile=str(cache), doraise=True,
                           invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
        before = cache.read_bytes()
        proc = self.hook()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("session-start 2026-10-04T13:36:00Z UTC", proc.stdout)
        self.assertFalse(marker.exists())
        self.assertEqual(cache.read_bytes(), before)
        self.assertEqual(list(cache.parent.iterdir()), [cache])

    def test_r8_invalid_compaction_timestamp(self):
        self.log.write_text("| 2026-10-04T13:36:00Z | compaction | valid |\n"
                            "| 2026-02-30T00:00:00Z | compaction | invalid |\n")
        facts = self.metrics()
        self.assertEqual(facts["start"], "2026-10-04T13:36:00Z")
        self.assertEqual(facts["elapsed"], "48h30m")
        self.assertEqual(facts["compaction_rows"], "UNKNOWN")
        self.assertIn("COMPACTIONS_UNREADABLE: invalid row timestamp", facts["lease_warning"])
        proc = self.cli()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("**Session:**", proc.stdout)
        self.assertIn("**HEAD:**", proc.stdout)
        self.assertIn("COMPACTIONS_UNREADABLE: invalid row timestamp", proc.stdout)
        proc = self.hook()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("COMPACTIONS_UNREADABLE: invalid row timestamp", proc.stdout)

    def test_r8_lease_changes_during_read(self):
        proc = self.runpy("import runpy\nfrom pathlib import Path\n"
                         "from unittest.mock import patch\n"
                         "m=runpy.run_path('tools/handoff-snapshot.py')\n"
                         "f=m['session_metrics']\ng=f.__globals__\n"
                         "original=g['_read']\n"
                         "def changing(root,name,error):\n"
                         " result=original(root,name,error)\n"
                         " if name=='degradation-watch-log.md':\n"
                         "  p=root.parent/'private/session-state.md'\n"
                         "  p.write_text(p.read_text()+'\\n<!-- changed -->\\n')\n"
                         " return result\n"
                         "with patch.dict(g,{'_read':changing}):\n"
                         " print(m['snapshot'](Path.cwd()))\n")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("**Session:** UNKNOWN (SESSION_START_STALE: "
                      "lease changed while reading snapshot)", proc.stdout)


    def assert_ambiguous(self, name):
        lease, field = AMBIGUOUS[name]
        self.lease.write_bytes(lease.encode("utf-8"))
        facts = self.metrics()
        for key in ("start", "start_source", "elapsed", "compaction_rows"):
            self.assertEqual(facts[key], "UNKNOWN", (name, key))
        self.assertIn("AMBIGUOUS LEASE FIELD: " + field, facts["lease_warning"])
        if name == "two_fields":
            self.assertIn("Last-heartbeat-UTC", facts["lease_warning"])

    def assert_heartbeat(self, kind):
        value, warning, elapsed, count = HEARTBEATS[kind]
        line = "" if value is None else "Last-heartbeat-UTC: " + value + "\n"
        self.lease.write_text(LIVE.replace(HBLINE, line))
        self.log.write_text("| 2026-10-04T13:36:00Z | compaction | start |\n"
                            "| 2026-10-05T14:00:00Z | compaction | boundary |\n"
                            "| 2026-10-06T14:05:00Z | compaction | later |\n")
        facts = self.metrics()
        self.assertEqual(facts["start"], "2026-10-04T13:36:00Z")
        self.assertEqual(facts["elapsed"], elapsed)
        self.assertEqual(facts["compaction_rows"], count)
        expected = (warning + UNVERIFIED if warning and kind != "stale" else warning)
        self.assertEqual(facts["lease_warning"], expected)

    def assert_invalid_compaction(self, value, context):
        if context == "future":
            self.change("2026-10-06T14:02:31Z", "2099-01-01T00:00:00Z")
        elif context == "unknown":
            self.change("orch-2026-10-04T13:36:00Z", "hex-id")
        elif context == "ambiguous":
            self.lease.write_text(LIVE + "Status: active\n")
        self.log.write_text("| " + value + " | compaction | bad |\n"
                            "| 2026-10-06T14:05:00Z | compaction | valid |\n")
        facts = self.metrics()
        invalid = value != "not-a-date"
        self.assertEqual(facts["compaction_rows"],
                         "UNKNOWN" if invalid or context != "known" else 1)
        self.assertEqual("COMPACTIONS_UNREADABLE: invalid row timestamp" in
                         facts["lease_warning"], invalid)
        other = {"future": "FUTURE HEARTBEAT", "unknown": "SESSION_START_UNKNOWN",
                 "ambiguous": "AMBIGUOUS LEASE FIELD"}
        if context in other:
            self.assertIn(other[context], facts["lease_warning"])
            self.assertEqual(facts["elapsed"], "UNKNOWN")
        else:
            self.assertEqual(facts["elapsed"], "48h30m")
        if context in ("unknown", "ambiguous"):
            self.assertEqual(facts["start"], "UNKNOWN")

    def test_compaction_rows_and_interval(self):
        self.log.write_text("| 2026-10-04T13:35:59Z | compaction | before |\n"
                            "| 2026-10-04T13:36:00Z | compaction | start |\n"
                            "| 2026-10-06T14:06Z | compaction | end |\n"
                            "| 2026-10-06T14:06:01Z | compaction | after |\n"
                            "| not-a-date | considered | quote | compaction |\n")
        facts = self.metrics()
        self.assertEqual(facts["compaction_rows"], 2)
        self.assertEqual(facts["lease_warning"], "")

    def test_absent_log_with_unknown_interval(self):
        self.log.unlink()
        self.change("2026-10-06T14:02:31Z", "2099-01-01T00:00:00Z")
        self.assertIsNone(self.metrics()["compaction_rows"])
        self.assertIn("compactions: no log", self.cli().stdout)
        self.assertIn("compactions: no log", self.hook().stdout)

    def test_unreadable_log_with_unknown_start(self):
        self.change("orch-2026-10-04T13:36:00Z", "hex-id")
        self.log.unlink()
        self.log.mkdir()
        self.error("COMPACTIONS_UNREADABLE")

    def test_hook_every_reader_error_fails_open(self):
        for message in ("SESSION_START_RELEASED", "SESSION_START_FUTURE",
                        "SESSION_START_UNREADABLE", "SESSION_START_STALE",
                        "COMPACTIONS_UNREADABLE", "unexpected reader error"):
            with self.subTest(message=message):
                (self.root / "tools/session_facts.py").write_text(
                    "def session_metrics(root):\n    raise RuntimeError(" + repr(message) + ")\n")
                proc = self.hook()
                self.assertEqual((proc.returncode, proc.stdout), (0, ""), proc.stderr)

    def test_gate_parity_for_usable_fixtures(self):
        fixtures = {"live": LIVE, "crlf": LIVE.replace("\n", "\r\n"),
                    "trailing": LIVE.replace("\n", " \t\n"),
                    "winding": LIVE.replace("Status: active", "Status: WINDING-DOWN")}
        fixtures.update({"ignored_" + name: lease for name, lease in ignored_placements(LIVE).items()})
        for name, (value, _, elapsed, _) in HEARTBEATS.items():
            if elapsed != "UNKNOWN":
                fixtures[name] = LIVE.replace(HBLINE, "Last-heartbeat-UTC: " + value + "\n")
        for name, lease in fixtures.items():
            with self.subTest(name=name):
                self.lease.write_bytes(lease.encode("utf-8"))
                facts = self.metrics()
                self.assertNotEqual(facts["start"], "UNKNOWN")
                self.assertNotEqual(facts["elapsed"], "UNKNOWN")
                self.assertNotEqual(facts["compaction_rows"], "UNKNOWN")
                proc = subprocess.run([sys.executable, "tools/lint-session-state.py"],
                                      cwd=self.root, env=self.env, capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_lf_only_and_one_trailing_cr(self):
        for prefix in ("\x85", "\x0c", "\u2028", "\r"):
            with self.subTest(prefix=repr(prefix)):
                self.lease.write_text(LIVE + prefix + "Active-session: orch-2020-01-01T00:00:00Z\n")
                self.assertIn("AMBIGUOUS LEASE FIELD: Active-session",
                              self.metrics()["lease_warning"])
        self.lease.write_bytes(LIVE.replace("\n", "\r\n").encode())
        self.assertEqual(self.metrics()["elapsed"], "48h30m")
        self.lease.write_bytes(LIVE.replace("Status: active\n", "Status: active\r\r\n").encode())
        self.assertIn("AMBIGUOUS LEASE FIELD: Status", self.metrics()["lease_warning"])

    def test_ambiguity_four_backticks(self):
        self.assert_ambiguous("four_backticks")

    def test_ambiguity_closing_text(self):
        self.assert_ambiguous("closing_text")

    def test_ambiguity_indent1(self):
        self.assert_ambiguous("indent1")

    def test_ambiguity_indent2(self):
        self.assert_ambiguous("indent2")

    def test_ambiguity_indent3(self):
        self.assert_ambiguous("indent3")

    def test_ambiguity_two_comments(self):
        self.assert_ambiguous("two_comments")

    def test_ambiguity_multiline_comment(self):
        self.assert_ambiguous("multiline_comment")

    def test_ambiguity_history(self):
        self.assert_ambiguous("history")

    def test_ambiguity_nel(self):
        self.assert_ambiguous("nel")

    def test_ambiguity_formfeed(self):
        self.assert_ambiguous("formfeed")

    def test_ambiguity_u2028(self):
        self.assert_ambiguous("u2028")

    def test_ambiguity_crlf(self):
        self.assert_ambiguous("crlf")

    def test_ambiguity_bullet(self):
        self.assert_ambiguous("bullet")

    def test_ambiguity_indented_copy(self):
        self.assert_ambiguous("indented_copy")

    def test_ambiguity_quoted_copy(self):
        self.assert_ambiguous("quoted_copy")

    def test_ambiguity_current_task(self):
        self.assert_ambiguous("current_task")

    def test_ambiguity_status_copy(self):
        self.assert_ambiguous("status_copy")

    def test_ambiguity_heartbeat_copy(self):
        self.assert_ambiguous("heartbeat_copy")

    def test_ambiguity_single_indented(self):
        self.assert_ambiguous("single_indented")

    def test_ambiguity_single_bullet(self):
        self.assert_ambiguous("single_bullet")

    def test_ambiguity_single_trailing(self):
        self.assert_ambiguous("single_trailing")

    def test_ambiguity_two_fields(self):
        self.assert_ambiguous("two_fields")

    def test_ambiguity_active_copy(self):
        self.assert_ambiguous("active_copy")

    def test_heartbeat_missing(self):
        self.assert_heartbeat("missing")

    def test_heartbeat_invalid(self):
        self.assert_heartbeat("invalid")

    def test_heartbeat_minute(self):
        self.assert_heartbeat("minute")

    def test_heartbeat_calendar(self):
        self.assert_heartbeat("calendar")

    def test_heartbeat_early(self):
        self.assert_heartbeat("early")

    def test_heartbeat_future(self):
        self.assert_heartbeat("future")

    def test_heartbeat_stale(self):
        self.assert_heartbeat("stale")

    def test_heartbeat_fresh(self):
        self.assert_heartbeat("fresh")

    def test_heartbeat_exact24(self):
        self.assert_heartbeat("exact24")

    def test_compaction_non_iso_known(self):
        self.assert_invalid_compaction('not-a-date', 'known')

    def test_compaction_non_iso_future(self):
        self.assert_invalid_compaction('not-a-date', 'future')

    def test_compaction_non_iso_unknown(self):
        self.assert_invalid_compaction('not-a-date', 'unknown')

    def test_compaction_non_iso_ambiguous(self):
        self.assert_invalid_compaction('not-a-date', 'ambiguous')

    def test_compaction_calendar_known(self):
        self.assert_invalid_compaction('2026-02-30T00:00:00Z', 'known')

    def test_compaction_calendar_future(self):
        self.assert_invalid_compaction('2026-02-30T00:00:00Z', 'future')

    def test_compaction_calendar_unknown(self):
        self.assert_invalid_compaction('2026-02-30T00:00:00Z', 'unknown')

    def test_compaction_calendar_ambiguous(self):
        self.assert_invalid_compaction('2026-02-30T00:00:00Z', 'ambiguous')


    def fixed_consumers(self, clock=(2026, 10, 6, 14, 6)):
        """Run both consumers with the same injected UTC clock; no sleep-based equality."""
        hooks = self.root / ".claude/hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / ".claude/hooks/surface-session-facts.py", hooks / "surface-session-facts.py")
        code = """import io, json, os, runpy, sys
from datetime import datetime, timezone
from pathlib import Path
class Clock(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(*clock, tzinfo=timezone.utc)
tool = runpy.run_path('tools/handoff-snapshot.py')
tool['session_metrics'].__globals__['datetime'] = Clock
print(tool['snapshot'](Path.cwd()), end='')
hook = runpy.run_path('.claude/hooks/surface-session-facts.py')
g = hook['main'].__globals__
loader = g['_load_sibling']
def load(name):
    module = loader(name)
    if name == 'session_facts':
        module.datetime = Clock
    return module
g['_load_sibling'] = load
transcript = Path('transcript.jsonl')
transcript.write_text(json.dumps({'type':'assistant','message':{
    'content':[{'type':'text','text':'session depth'}]}}) + '\\n')
sys.stdin = io.StringIO(json.dumps({'transcript_path':str(transcript.resolve())}))
os.environ['CLAUDE_PROJECT_DIR'] = str(Path.cwd())
hook['main']()
"""
        proc = self.runpy("clock = " + repr(clock) + "\n" + code)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def test_ignored_text_ten_placements(self):
        for session in ("orch-2026-10-04T13:36:00Z", "69556d8c"):
            base = LIVE.replace("orch-2026-10-04T13:36:00Z", session)
            self.lease.write_text(base)
            expected = self.metrics()
            consumers = self.fixed_consumers()
            for name, lease in ignored_placements(base).items():
                with self.subTest(session=session, placement=name):
                    self.lease.write_bytes(lease.encode())
                    self.assertEqual(self.metrics(), expected)
                    self.assertEqual(self.fixed_consumers(), consumers)

    def test_unknown_consumers_explain_id(self):
        self.change("orch-2026-10-04T13:36:00Z", "69556d8c")
        output = self.fixed_consumers()
        session = next(line for line in output.splitlines() if "**Session:**" in line)
        message = json.loads(output.splitlines()[-1])["systemMessage"]
        for text in (session, message):
            self.assertIn("start unknown because the lease id does not record one", text)
            self.assertNotIn("  ", text)
            self.assertNotIn("; ;", text)
        self.assertIn("start UNKNOWN, elapsed UNKNOWN", session)

    def test_no_other_field_supplies_start(self):
        self.change("orch-2026-10-04T13:36:00Z", "69556d8c")
        for field in ("Current-task", "Worker-dispatches", "Other-start"):
            with self.subTest(field=field):
                base = LIVE.replace("orch-2026-10-04T13:36:00Z", "69556d8c")
                self.lease.write_text(base + field + ": 2026-10-04T13:36:00Z\n")
                facts = self.metrics()
                self.assertEqual(facts["start"], "UNKNOWN")
                self.assertEqual(facts["elapsed"], "UNKNOWN")
                self.assertEqual(facts["compaction_rows"], "UNKNOWN")

    def test_each_used_field_whole_file_rule(self):
        for name, value in (("Active-session", "orch-2026-10-04T13:36:00Z"),
                            ("Status", "active"), ("Last-heartbeat-UTC", "2026-10-06T14:02:31Z")):
            line = name + ": " + value + "\n"
            bold = "**" + name + ":** " + value + "\n"
            for malformed in (" " + line, "- " + line, line.rstrip("\n") + " extra\n",
                              " " + bold, bold):
                # 3b679: a solitary bold field is read (both forms are), so the bold
                # copy is a second occurrence only beside the plain line.
                for duplicate in ((True,) if malformed == bold else (False, True)):
                    with self.subTest(field=name, malformed=malformed, duplicate=duplicate):
                        base = LIVE if duplicate else LIVE.replace(line, "")
                        self.lease.write_text(base + malformed)
                        facts = self.metrics()
                        for key in ("start", "elapsed", "compaction_rows"):
                            self.assertEqual(facts[key], "UNKNOWN")
                        self.assertIn("AMBIGUOUS LEASE FIELD: " + name, facts["lease_warning"])


    def test_3b679_plain_and_bold_leases_read_alike(self):
        # The reader accepts both forms, so a hook between the gate change and
        # the live lease's conversion reads the same facts; the gate refuses bold.
        self.env["GRC_STORE"] = str(self.store)
        bold = re.sub(r"(?m)^([A-Za-z-]+): ", r"**\1:** ", LIVE)
        mixed = LIVE.replace(CURRENT, "**" + CURRENT.replace(":", ":**", 1))
        self.assertNotEqual(bold, LIVE)
        for form, lease, code in (("plain", LIVE, 0), ("bold", bold, 2), ("mixed", mixed, 2)):
            with self.subTest(form=form):
                self.lease.write_text(lease)
                facts = self.metrics()
                self.assertEqual(facts, dict(
                    start="2026-10-04T13:36:00Z", elapsed="48h30m", compaction_rows=0,
                    lease_warning="", start_source="derived from Active-session "
                    "orch-<UTC start> convention"))
                proc = subprocess.run([sys.executable, "tools/lint-session-state.py"],
                                      cwd=self.root, env=self.env, capture_output=True, text=True)
                self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)
                self.assertEqual("write the plain form" in proc.stderr, bool(code))

    def test_3b679_tab_separator_read_but_refused(self):
        # orch_store.py needs "<name>: " (one space); the reader keeps reading a tab.
        self.env["GRC_STORE"] = str(self.store)
        self.lease.write_text(LIVE.replace("Status: ", "Status:\t"))
        self.assertEqual(self.metrics()["start"], "2026-10-04T13:36:00Z")
        proc = subprocess.run([sys.executable, "tools/lint-session-state.py"],
                              cwd=self.root, env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("wrong value shape", proc.stderr)

    def test_r11_all_other_field_orders(self):
        from itertools import permutations
        lines = (CURRENT, "Status: active\n", HBLINE)
        for order in permutations(range(3)):
            if order == (0, 1, 2):
                continue
            with self.subTest(order=order):
                self.lease.write_text("".join(lines[index] for index in order))
                facts = self.metrics()
                for key in ("start", "start_source", "elapsed", "compaction_rows"):
                    self.assertEqual(facts[key], "UNKNOWN")
                self.assertEqual(
                    facts["lease_warning"],
                    "AMBIGUOUS LEASE FIELD: fields are out of order: "
                    "Active-session, Status, Last-heartbeat-UTC")
                output = self.fixed_consumers()
                self.assertIn("start UNKNOWN, elapsed UNKNOWN", output)
                self.assertIn("length UNKNOWN", output)
                self.assertIn("fields are out of order", output)

    def test_r11_solitary_copies_below_header(self):
        copies = (
            LIVE.replace(CURRENT, "") + FENCE + "\n" + OLD + FENCE + "\n",
            LIVE.replace("Active-session:", "Active-Session:")
            + "<!--\n" + OLD + "-->\n",
            LIVE.replace("Active-session:", "Active-session :")
            + "## History\n" + OLD,
            LIVE.replace("Active-session:", "Active\u2011session:")
            + FENCE + "\n" + OLD + FENCE + "\n",
            LIVE.replace("Status: active", "STATUS: released")
            + FENCE + "\nStatus: active\n" + FENCE + "\n",
            # 3b679: a solitary bold copy below the header is read like a plain one.
            LIVE.replace(CURRENT, "") + "**" + OLD.replace(":", ":**", 1),
        )
        for index, lease in enumerate(copies):
            with self.subTest(shape=index):
                self.lease.write_text(lease)
                facts = self.metrics()
                for key in ("start", "elapsed", "compaction_rows"):
                    self.assertEqual(facts[key], "UNKNOWN")
                self.assertIn("AMBIGUOUS LEASE FIELD: fields are out of order",
                              facts["lease_warning"])

    def test_r11_absent_fields_keep_existing_handling(self):
        self.lease.write_text(LIVE.replace("Status: active\n", ""))
        facts = self.metrics()
        self.assertEqual(facts, dict(
            start="UNKNOWN", elapsed="UNKNOWN", compaction_rows="UNKNOWN",
            start_source="UNKNOWN",
            lease_warning="SESSION_START_UNKNOWN: no usable live lease start"))
        self.lease.write_text(LIVE.replace(HBLINE, ""))
        facts = self.metrics()
        self.assertEqual(facts["start"], "2026-10-04T13:36:00Z")
        self.assertEqual(facts["elapsed"], "UNKNOWN")
        self.assertEqual(facts["compaction_rows"], "UNKNOWN")
        self.assertEqual(facts["lease_warning"], "MISSING OR INVALID HEARTBEAT" + UNVERIFIED)

    def test_r11_precedence(self):
        for lease in (RELEASED, LIVE.replace("active", "released"),
                      LIVE.replace("orch-2026-10-04T13:36:00Z", "none")):
            with self.subTest(lease=lease):
                self.lease.write_text(lease)
                self.error("SESSION_START_RELEASED")
                self.lease.write_text(lease + "Status: active\n")
                self.assertIn("AMBIGUOUS LEASE FIELD: Status", self.metrics()["lease_warning"])
        for session, status in (("orch-2026-10-04T13:36:00Z", "released"), ("none", "active")):
            self.lease.write_text(HBLINE + "Status: " + status + "\n"
                                 + "Active-session: " + session + "\n")
            self.error("SESSION_START_RELEASED")

    def test_r11_known_limit_copy_above_status(self):
        self.lease.write_text(LIVE.replace(
            CURRENT, "Active-Session: orch-2026-10-04T13:36:00Z\n" + OLD))
        facts = self.metrics()
        self.assertEqual(facts["start"], "2020-01-01T00:00:00Z")
        self.assertEqual(facts["elapsed"], "59294h6m")
        self.assertEqual(facts["compaction_rows"], 0)
        self.assertEqual(facts["lease_warning"], "")

    def assert_r11_near_miss_separator(self, label, faults):
        self.env["GRC_STORE"] = str(self.store)
        self.lease.write_text(LIVE.replace(
            CURRENT, label + " orch-2026-10-04T13:36:00Z\n" + OLD))
        facts = self.metrics()
        self.assertEqual(facts["start"], "2020-01-01T00:00:00Z")
        self.assertEqual(facts["lease_warning"], "")
        proc = subprocess.run([sys.executable, "tools/lint-session-state.py"],
                              cwd=self.root, env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("has a near-miss label (" + faults + ")", proc.stderr)

    def test_r11_known_limit_space_separator_refused(self):
        self.assert_r11_near_miss_separator("Active session:", "wrong separators")

    def test_r11_known_limit_space_before_colon_refused(self):
        self.assert_r11_near_miss_separator("Active-session :", "space before the colon")

    def test_r11_known_limit_underscore_separator_refused(self):
        self.assert_r11_near_miss_separator("Active_session:", "wrong separators")

    def test_r11_known_limit_case_and_separator_refused(self):
        self.assert_r11_near_miss_separator("active session:",
                                            "wrong case, wrong separators")

    def test_hash_todo_between_fields_is_not_heading(self):
        self.env["GRC_STORE"] = str(self.store)
        self.lease.write_text(LIVE.replace(CURRENT, CURRENT + "#todo refresh\n"))
        proc = subprocess.run([sys.executable, "tools/lint-session-state.py"],
                              cwd=self.root, env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(self.metrics()["start"], "2026-10-04T13:36:00Z")

    def test_r11_out_of_order_without_log(self):
        self.log.unlink()
        self.lease.write_text(HBLINE + CURRENT + "Status: active\n")
        facts = self.metrics()
        for key in ("start", "elapsed", "compaction_rows"):
            self.assertEqual(facts[key], "UNKNOWN")
        self.assertIn("fields are out of order", facts["lease_warning"])

    def test_r11_heartbeat_equal_start(self):
        self.lease.write_text(LIVE.replace(HBLINE, "Last-heartbeat-UTC: 2026-10-04T13:36:00Z\n"))
        self.log.write_text("| 2026-10-04T13:35:59Z | compaction | before |\n"
                            "| 2026-10-04T13:36:00Z | compaction | start |\n"
                            "| 2026-10-04T13:36:01Z | compaction | after |\n")
        facts = self.metrics("2026-10-04T13:36:00+00:00")
        self.assertEqual(facts["start"], "2026-10-04T13:36:00Z")
        self.assertEqual(facts["elapsed"], "0h0m")
        self.assertEqual(facts["compaction_rows"], 1)
        self.assertEqual(facts["lease_warning"], "")



    def test_main_compaction_row_kinds(self):
        self.env["GRC_STORE"] = str(self.store)
        for name, content, count in COMPACTION_CASES:
            with self.subTest(kind=name):
                self.log.write_bytes(content.encode())
                facts = self.metrics()
                self.assertEqual(facts["compaction_rows"], count)
                self.assertEqual(facts["lease_warning"], "")

    def test_main_compaction_predicate_parity(self):
        self.env["GRC_STORE"] = str(self.store)
        content = "".join(row for _, row, _ in COMPACTION_CASES)
        # b950dcbd:.claude/hooks/surface-session-facts.py:108,242-246.
        main = re.compile(r"\|\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)"
                          r"\s*\|\s*compaction\s*\|")
        expected = [line for line in content.splitlines() if main.match(line)]
        proc = self.runpy("import runpy\n"
                         "m=runpy.run_path('tools/session_facts.py')\n"
                         "print([line for line in " + repr(content) + ".splitlines()\n"
                         "       if m['COMPACTION'].match(line)])\n")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(ast.literal_eval(proc.stdout), expected)
        self.log.write_bytes(content.encode())
        self.assertEqual(self.metrics()["compaction_rows"], len(expected))

    def fixed_cli(self, clock=(2026, 10, 6, 14, 6)):
        return self.runpy(
            "import runpy\nfrom datetime import datetime, timezone\n"
            "m=runpy.run_path('tools/handoff-snapshot.py')\n"
            "class Clock(datetime):\n"
            " @classmethod\n"
            " def now(cls,tz=None): return cls(*" + repr(clock) + ",tzinfo=timezone.utc)\n"
            "m['session_metrics'].__globals__['datetime']=Clock\n"
            "raise SystemExit(m['main']())\n")

    def test_reader_errors_preserve_snapshot_and_hook_silence(self):
        self.env["GRC_STORE"] = str(self.store)
        success = self.fixed_cli()
        self.assertEqual(success.returncode, 0, success.stderr)
        expected = [line for line in success.stdout.splitlines()
                    if not line.startswith("- **Session:**")]
        cases = ("released", "none", "future", "log_directory", "lease_decode",
                 "lease_directory", "log_decode")
        for kind in cases:
            with self.subTest(kind=kind):
                self.lease.write_text(LIVE)
                self.log.write_text("")
                error = "SESSION_START_UNREADABLE"
                if kind == "released":
                    self.change("Status: active", "Status: released")
                    error = "SESSION_START_RELEASED"
                elif kind == "none":
                    self.change("orch-2026-10-04T13:36:00Z", "none")
                    error = "SESSION_START_RELEASED"
                elif kind == "future":
                    self.change("orch-2026-10-04T13:36:00Z", "orch-2099-01-01T00:00:00Z")
                    error = "SESSION_START_FUTURE"
                elif kind == "log_directory":
                    self.log.unlink()
                    self.log.mkdir()
                    error = "COMPACTIONS_UNREADABLE"
                elif kind == "lease_decode":
                    self.lease.write_bytes(b"\xff")
                elif kind == "lease_directory":
                    self.lease.unlink()
                    self.lease.mkdir()
                elif kind == "log_decode":
                    self.log.write_bytes(b"\xff")
                    error = "COMPACTIONS_UNREADABLE"
                try:
                    proc = self.fixed_cli()
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    lines = proc.stdout.splitlines()
                    session = [line for line in lines if line.startswith("- **Session:**")]
                    self.assertEqual(len(session), 1, proc.stdout)
                    self.assertTrue(session[0].startswith("- **Session:** UNKNOWN (" + error + ":"),
                                    session[0])
                    self.assertTrue(session[0].endswith(")"), session[0])
                    self.assertEqual([line for line in lines if line not in session], expected)
                    hook = self.hook()
                    self.assertEqual((hook.returncode, hook.stdout, hook.stderr), (0, "", ""))
                finally:
                    for path in (self.lease, self.log):
                        if path.is_dir():
                            path.rmdir()
                        elif path.exists():
                            path.unlink()

    def test_absent_or_uncounted_header_substitution(self):
        self.env["GRC_STORE"] = str(self.store)
        expected = self.metrics()
        lines = (CURRENT, "Status: active\n", HBLINE)
        for line in lines:
            for replacement in ("", line.replace(":", " :", 1)):
                with self.subTest(field=line, replacement=replacement):
                    self.lease.write_text(LIVE.replace(line, replacement + "<!--\n" + line + "-->\n"))
                    self.assertEqual(self.metrics(), expected)
                    proc = subprocess.run([sys.executable, "tools/lint-session-state.py"],
                                          cwd=self.root, env=self.env, capture_output=True, text=True)
                    # 3b328: gate 63 refuses the copy and any near-miss header.
                    self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                    self.assertIn("is outside the header region (HTML comment)", proc.stderr)
                    self.assertEqual("near-miss label" in proc.stderr, bool(replacement))
        for count in (2, 3):
            with self.subTest(uncounted=count):
                lease = LIVE
                for line in lines[-count:]:
                    lease = lease.replace(line, "")
                self.lease.write_text(lease + FENCE + "\n" + "".join(lines[-count:]) + FENCE + "\n")
                self.assertEqual(self.metrics(), expected)

    def test_duplicate_without_log_reports_no_log(self):
        self.env["GRC_STORE"] = str(self.store)
        self.log.unlink()
        self.lease.write_text(LIVE + "Status: active\n")
        facts = self.metrics()
        self.assertEqual(facts["start"], "UNKNOWN")
        self.assertEqual(facts["elapsed"], "UNKNOWN")
        self.assertIsNone(facts["compaction_rows"])
        output = self.fixed_consumers()
        self.assertEqual(output.count("compactions: no log"), 2)

    def start_minute_fixture(self, rows, start="2026-10-06T14:05:45Z"):
        self.env["GRC_STORE"] = str(self.store)
        self.lease.write_text(LIVE.replace("2026-10-04T13:36:00Z", start).replace(
            "2026-10-06T14:02:31Z", "2026-10-06T14:06:00Z"))
        self.log.write_text(rows)

    def assert_start_minute_unknown(self, facts):
        self.assertEqual(facts["compaction_rows"], "UNKNOWN")
        self.assertIn(
            "AMBIGUOUS COMPACTION: a minute-form compaction row in the session's "
            "start minute cannot be placed before or after the start",
            facts["lease_warning"])

    def test_start_minute_reproduction(self):
        self.start_minute_fixture(
            "| 2026-10-06T14:05Z | compaction | event at 14:05:50 UTC |\n")
        facts = self.metrics()
        self.assert_start_minute_unknown(facts)
        self.assertEqual(facts["start"], "2026-10-06T14:05:45Z")
        self.assertEqual(facts["elapsed"], "0h0m")

    def test_start_minute_zero_seconds(self):
        self.start_minute_fixture(
            "| 2026-10-06T14:05Z | compaction | event at 14:05:50 UTC |\n",
            start="2026-10-06T14:05:00Z")
        facts = self.metrics()
        self.assertEqual(facts["compaction_rows"], 1)
        self.assertEqual(facts["lease_warning"], "")

    def test_start_minute_seconds_inside(self):
        self.start_minute_fixture("| 2026-10-06T14:05:50Z | compaction | inside |\n")
        facts = self.metrics()
        self.assertEqual(facts["compaction_rows"], 1)
        self.assertEqual(facts["lease_warning"], "")

    def test_start_minute_seconds_before(self):
        self.start_minute_fixture("| 2026-10-06T14:05:30Z | compaction | before |\n")
        facts = self.metrics()
        self.assertEqual(facts["compaction_rows"], 0)
        self.assertEqual(facts["lease_warning"], "")

    def test_start_minute_next_minute_and_end(self):
        for stamp, count in (("14:06Z", 1), ("14:06:00Z", 1),
                             ("14:06:01Z", 0), ("14:07Z", 0)):
            with self.subTest(stamp=stamp):
                self.start_minute_fixture("| 2026-10-06T" + stamp + " | compaction |\n")
                facts = self.metrics()
                self.assertEqual(facts["compaction_rows"], count)
                self.assertEqual(facts["lease_warning"], "")

    def test_start_minute_mixed_rows(self):
        self.start_minute_fixture("| 2026-10-06T14:05Z | compaction | ambiguous |\n"
                                  "| 2026-10-06T14:05:50Z | compaction | inside |\n")
        self.assert_start_minute_unknown(self.metrics())

    def test_start_minute_stale_cap(self):
        self.start_minute_fixture("| 2026-10-06T14:05Z | compaction | ambiguous |\n"
                                  "| 2026-10-06T14:06Z | compaction | end |\n"
                                  "| 2026-10-06T14:06:01Z | compaction | after |\n")
        facts = self.metrics("2026-10-08T14:06:00+00:00")
        self.assert_start_minute_unknown(facts)
        self.assertIn("STALE HEARTBEAT", facts["lease_warning"])
        self.assertEqual(facts["elapsed"], "0h0m")

    def test_start_minute_other_date(self):
        self.start_minute_fixture("| 2026-10-05T14:05Z | compaction | before |\n"
                                  "| 2026-10-07T14:05Z | compaction | future |\n")
        facts = self.metrics()
        self.assertEqual(facts["compaction_rows"], 0)
        self.assertEqual(facts["lease_warning"], "")

    def test_start_minute_row_predicate(self):
        row = "| 2026-10-06T14:05Z | compaction | ambiguous |\n"
        for content in (row, "<!--\n" + row + "-->\n", FENCE + "\n" + row + FENCE,
                        row.replace("\n", "\r\n"), row.rstrip("\n") + " extra cells |\n"):
            with self.subTest(content=content):
                self.start_minute_fixture(content)
                self.assert_start_minute_unknown(self.metrics())
        for content in (" " + row, row.replace("| compaction |", "| considered |")):
            with self.subTest(content=content):
                self.start_minute_fixture(content)
                facts = self.metrics()
                self.assertEqual(facts["compaction_rows"], 0)
                self.assertEqual(facts["lease_warning"], "")

    def test_start_minute_consumers(self):
        self.start_minute_fixture("| 2026-10-06T14:05Z | compaction | ambiguous |\n")
        for proc in (self.fixed_cli(), self.hook()):
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("compactions this session: UNKNOWN", proc.stdout)
            self.assertIn("a minute-form compaction row in the session's start minute "
                          "cannot be placed before or after the start", proc.stdout)

    def end_minute_fixture(self, rows, heartbeat="2026-10-06T14:30:20Z",
                           start="2026-10-06T13:00:00Z"):
        self.env["GRC_STORE"] = str(self.store)
        self.lease.write_text(LIVE.replace("2026-10-04T13:36:00Z", start).replace(
            "2026-10-06T14:02:31Z", heartbeat))
        self.log.write_text(rows)

    def assert_end_minute_unknown(self, facts):
        self.assertEqual(facts["compaction_rows"], "UNKNOWN")
        self.assertIn("AMBIGUOUS COMPACTION: a minute-form compaction row in the minute "
                      "of the last heartbeat cannot be placed before or after it",
                      facts["lease_warning"])

    def assert_end_minute_count(self, count):
        facts = self.metrics("2026-10-08T14:30:20+00:00")
        self.assertEqual(facts["compaction_rows"], count)
        self.assertTrue(facts["lease_warning"].startswith("STALE HEARTBEAT:"))
        self.assertNotIn("AMBIGUOUS COMPACTION", facts["lease_warning"])

    def test_end_minute_reproduction(self):
        self.end_minute_fixture("| 2026-10-06T14:30Z | compaction |\n")
        facts = self.metrics("2026-10-08T14:30:20+00:00")
        self.assert_end_minute_unknown(facts)
        self.assertIn("STALE HEARTBEAT", facts["lease_warning"])
        self.assertEqual(facts["elapsed"], "1h30m")

    def test_end_minute_zero_seconds(self):
        self.end_minute_fixture("| 2026-10-06T14:30Z | compaction |\n",
                                heartbeat="2026-10-06T14:30:00Z")
        self.assert_end_minute_unknown(self.metrics("2026-10-08T14:30:20+00:00"))

    def test_end_minute_seconds_inside(self):
        self.end_minute_fixture("| 2026-10-06T14:30:10Z | compaction |\n")
        self.assert_end_minute_count(1)

    def test_end_minute_seconds_after(self):
        self.end_minute_fixture("| 2026-10-06T14:30:40Z | compaction |\n")
        self.assert_end_minute_count(0)

    def test_end_minute_fresh(self):
        self.end_minute_fixture("| 2026-10-06T14:30Z | compaction |\n")
        facts = self.metrics("2026-10-06T14:30:20+00:00")
        self.assertEqual(facts["compaction_rows"], 1)
        self.assertEqual(facts["lease_warning"], "")

    def test_end_minute_both_boundaries(self):
        self.end_minute_fixture("| 2026-10-06T13:00Z | compaction |\n"
                                "| 2026-10-06T14:30Z | compaction |\n",
                                start="2026-10-06T13:00:45Z")
        facts = self.metrics("2026-10-08T14:30:20+00:00")
        self.assert_start_minute_unknown(facts)
        self.assert_end_minute_unknown(facts)

    def test_end_minute_after_window(self):
        self.end_minute_fixture("| 2026-10-06T14:31Z | compaction |\n"
                                "| 2026-10-07T14:30Z | compaction |\n")
        self.assert_end_minute_count(0)

    def test_end_minute_previous_minute(self):
        self.end_minute_fixture("| 2026-10-06T14:29Z | compaction |\n")
        self.assert_end_minute_count(1)

    def test_end_minute_row_predicate(self):
        self.end_minute_fixture(" | 2026-10-06T14:30Z | compaction |\n"
                                "| 2026-10-06T14:30Z | considered |\n")
        self.assert_end_minute_count(0)

    def test_end_minute_consumers(self):
        self.end_minute_fixture("| 2026-10-06T14:30Z | compaction |\n")
        clock = (2026, 10, 8, 14, 30, 20)
        proc = self.fixed_cli(clock)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for consumer, output, count in (("snapshot and hook", self.fixed_consumers(clock), 2),
                                        ("snapshot CLI", proc.stdout, 1)):
            with self.subTest(consumer=consumer):
                self.assertEqual(output.count("compactions this session: UNKNOWN"), count)
                self.assertEqual(output.count(
                    "a minute-form compaction row in the minute of the last "
                    "heartbeat cannot be placed before or after it"), count)

    def test_end_minute_worked_instants(self):
        cases = (
            ("14:30:00Z", "14:30Z", False, "UNKNOWN"),
            ("14:30:20Z", "14:30Z", False, "UNKNOWN"),
            ("14:30:59Z", "14:30Z", False, "UNKNOWN"),
            ("14:30:00Z", "14:29Z", False, 1),
            ("14:30:00Z", "14:30:00Z", False, 1),
            ("14:30:00Z", "14:30:01Z", False, 0),
            ("14:30:00Z", "14:31Z", False, 0),
            ("14:30:20Z", "14:30Z", True, 1),
        )
        for heartbeat, stamp, fresh, count in cases:
            with self.subTest(heartbeat=heartbeat, stamp=stamp, fresh=fresh):
                self.end_minute_fixture("| 2026-10-06T" + stamp + " | compaction |\n",
                                        heartbeat="2026-10-06T" + heartbeat)
                now = "2026-10-06T14:30:20+00:00" if fresh else "2026-10-08T14:30:20+00:00"
                facts = self.metrics(now)
                self.assertEqual(facts["compaction_rows"], count)
                if count == "UNKNOWN":
                    self.assert_end_minute_unknown(facts)
                else:
                    self.assertNotIn("AMBIGUOUS COMPACTION", facts["lease_warning"])
                if fresh:
                    self.assertEqual(facts["lease_warning"], "")
                else:
                    self.assertIn("STALE HEARTBEAT", facts["lease_warning"])

    def test_end_minute_unknown_start(self):
        self.end_minute_fixture("| 2026-10-06T14:30Z | compaction |\n")
        self.change("orch-2026-10-06T13:00:00Z", "unknown-id")
        facts = self.metrics("2026-10-08T14:30:20+00:00")
        for key in ("start", "elapsed", "compaction_rows"):
            self.assertEqual(facts[key], "UNKNOWN")
        self.assertIn("SESSION_START_UNKNOWN", facts["lease_warning"])
        self.assertIn("STALE HEARTBEAT", facts["lease_warning"])
        self.assertNotIn("AMBIGUOUS COMPACTION", facts["lease_warning"])

    def test_unverified_heartbeat_without_log(self):
        self.env["GRC_STORE"] = str(self.store)
        self.log.unlink()
        for value in (None, "not-a-date", "2020-01-01T00:00:00Z", "2099-01-01T00:00:00Z"):
            with self.subTest(heartbeat=value):
                line = "" if value is None else "Last-heartbeat-UTC: " + value + "\n"
                self.lease.write_text(LIVE.replace(HBLINE, line))
                facts = self.metrics()
                self.assertEqual(facts["start"], "2026-10-04T13:36:00Z")
                self.assertEqual(facts["elapsed"], "UNKNOWN")
                self.assertIsNone(facts["compaction_rows"])
                self.assertIn(UNVERIFIED, facts["lease_warning"])
                proc = self.fixed_cli()
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn("compactions: no log", proc.stdout)


HBLINE = "Last-heartbeat-UTC: 2026-10-06T14:02:31Z\n"
CURRENT = "Active-session: orch-2026-10-04T13:36:00Z\n"
OLD = "Active-session: orch-2020-01-01T00:00:00Z\n"
BASE = LIVE
FENCE = chr(96) * 3
COPIES = {
    "four_backticks": FENCE + chr(96) + "\n" + FENCE + "\n" + OLD + FENCE + chr(96) + "\n",
    "closing_text": FENCE + "\n" + FENCE + " trailing\n" + OLD + FENCE + "\n",
    "indent1": " " + FENCE + "\n" + OLD + " " + FENCE + "\n",
    "indent2": "  " + FENCE + "\n" + OLD + "  " + FENCE + "\n",
    "indent3": "   " + FENCE + "\n" + OLD + "   " + FENCE + "\n",
    "two_comments": "<!-- a --> <!-- b\n" + OLD + "-->\n",
    "multiline_comment": "<!--\n" + OLD + "-->\n",
    "history": "## History\n" + OLD,
    "nel": "\x85" + OLD,
    "formfeed": "\x0c" + OLD,
    "u2028": "\u2028" + OLD,
    "crlf": FENCE + "\n" + OLD + FENCE + "\n",
    "bullet": "- " + OLD,
    "indented_copy": "    " + OLD,
    "quoted_copy": "> " + OLD,
    "current_task": "Current-task: example " + OLD,
}
AMBIGUOUS = {name: (BASE + copy, "Active-session") for name, copy in COPIES.items()}
AMBIGUOUS["crlf"] = ((BASE + COPIES["crlf"]).replace("\n", "\r\n"), "Active-session")
AMBIGUOUS.update({
    "active_copy": (LIVE + "Active-session: orch-2020-01-01T00:00:00Z\n", "Active-session"),
    "status_copy": (LIVE + "Status: released\n", "Status"),
    "heartbeat_copy": (LIVE + HBLINE, "Last-heartbeat-UTC"),
    "single_indented": (LIVE.replace(CURRENT, "") + " " + OLD, "Active-session"),
    "single_bullet": (LIVE.replace(CURRENT, "") + "- " + OLD, "Active-session"),
    "single_trailing": (LIVE.replace(CURRENT, "") + OLD.rstrip("\n") + " extra\n", "Active-session"),
    "two_fields": (LIVE + "Status: active\n" + HBLINE, "Status"),
})
def ignored_placements(base):
    """Opaque extra text must not affect either metrics or consumer bytes."""
    line = "**Session-start-UTC:** 2020-01-01T00:00:00Z\n"
    return {
        "header": base.replace("\n\n", "\n\n" + line, 1),
        "fence": base + FENCE + "\n" + line + FENCE + "\n",
        "nested_fence": base + FENCE + chr(96) + "\n" + FENCE + "\n" + line + FENCE + "\n" + FENCE + chr(96) + "\n",
        "comment": base + "<!--\n" + line + "-->\n",
        "history": base + "## History\n" + line,
        "indented": base + "    " + line,
        "bulleted": base + "- " + line,
        "repeated": base + line * 3,
        "malformed": base + "Session-start-UTC: nonsense extra :**\n",
        "form_feed": base + "\x0c" + line,
    }


UNVERIFIED = ": activity since the start is unverified; elapsed and compactions UNKNOWN"
HEARTBEATS = {
    "missing": (None, "MISSING OR INVALID HEARTBEAT", "UNKNOWN", "UNKNOWN"),
    "invalid": ("not-a-date", "MISSING OR INVALID HEARTBEAT", "UNKNOWN", "UNKNOWN"),
    "minute": ("2026-10-06T14:02Z", "MISSING OR INVALID HEARTBEAT", "UNKNOWN", "UNKNOWN"),
    "calendar": ("2026-02-30T00:00:00Z", "MISSING OR INVALID HEARTBEAT", "UNKNOWN", "UNKNOWN"),
    "early": ("2020-01-01T00:00:00Z", "HEARTBEAT BEFORE START", "UNKNOWN", "UNKNOWN"),
    "future": ("2099-01-01T00:00:00Z", "FUTURE HEARTBEAT", "UNKNOWN", "UNKNOWN"),
    "stale": ("2026-10-05T14:00:00Z",
              "STALE HEARTBEAT: lease not refreshed since 2026-10-05T14:00:00Z"
              " (older than 24h; elapsed and compactions end at last heartbeat)", "24h24m", 2),
    "fresh": ("2026-10-06T14:02:31Z", "", "48h30m", 3),
    "exact24": ("2026-10-05T14:06:00Z", "", "48h30m", 3),
}


ROW = "| 2026-10-06T14:05:30Z | compaction | example |\n"
COMPACTION_CASES = (
    ("canonical", ROW, 1),
    ("indented", "    " + ROW, 0),
    ("comment", "<!--\n" + ROW + "-->\n", 1),
    ("fence", FENCE + "\n" + ROW + FENCE + "\n", 1),
    ("placeholder", "| <iso> | compaction |\n", 0),
    ("approximate", "| 2026-07-29T~16:20Z | compaction | example |\n", 0),
    ("offset", ROW.replace("Z", "+00:00"), 0),
    ("crlf", ROW.replace("\n", "\r\n"), 1),
    ("trailing", ROW.rstrip("\n") + " extra | cells |\n", 1),
    ("considered", ROW.replace("| compaction | example", "| considered | compaction"), 0),
    ("session_start", ROW.replace("| compaction | example", "| session-start | compaction"), 0),
    ("minute", ROW.replace(":30Z", "Z"), 1),
)


if __name__ == "__main__":
    unittest.main()
