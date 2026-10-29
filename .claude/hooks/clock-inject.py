#!/usr/bin/env python3
"""PostToolUse and PostToolUseFailure hook (all tools): inject the real clock into the orchestrator's context.

Fleet orchestrator operational guard (generic: no project name is hardcoded). Motivated by an orchestrator
composing console timestamps and "Session elapsed HH:MM" footers from its own sense of time instead of
reading the clock, drifting up to 4h40m ahead (timestamp-from-clock; claims-rest-on-observation). After a
tool call that ran, it emits ONE short additionalContext line read from the process clock, for example:

    CLOCK (read by hook, authoritative): 2026-09-23 13:45:02 EDT | 2026-09-23T17:45:02Z | session elapsed 03:27

so a fresh authoritative reading is the most recent time value in context.

Coverage. Registered under PostToolUse it fires after a tool call that SUCCEEDED; registered under
PostToolUseFailure it fires after a tool call that started and FAILED. The emitted hookEventName matches the
incoming payload's hook_event_name (PostToolUseFailure when that is the event, otherwise PostToolUse), as the
hooks contract requires. Both registrations are needed for both outcomes. Neither event fires for a tool
call rejected before execution (an unknown tool, input failing validation, or a permission denial), so such
calls, and any stretch of prose with no tool call, see no fresh reading.

Elapsed resolution. The lease file is, in order: env ORCH_LEASE_FILE; else <CLAUDE_PROJECT_DIR>/.working/
session-state.md when CLAUDE_PROJECT_DIR is an absolute path and that file exists; else <ORCH_PROJECT_ROOT>/
private/session-state.md when ORCH_PROJECT_ROOT is an absolute path; else /opt/<project>/private/
session-state.md derived from the payload cwd (or the process cwd) when that lies under /opt/<project>/.
Without ORCH_LEASE_FILE or a CLAUDE_PROJECT_DIR lease the lease therefore FOLLOWS THE CWD: a session working
in another project's tree, or outside /opt, reads that tree's lease or none. The fleet should set
ORCH_LEASE_FILE (absolute) per orchestrator. The lease start is read ONLY from the FIRST line beginning
`Active-session:`; when its value is not exactly `<label>-YYYYMMDDTHHMMSSZ`, where <label> is 1 to 32
characters of [A-Za-z0-9] (for example `sess-` or `S88-`), elapsed is unknown (for example for `none` or a
malformed id) and no later line is consulted. The file is opened non-blocking, must be a regular file, and at
most 1 MiB is read. When the file is absent, unreadable,
not regular, or the start lies in the future, the elapsed segment is omitted. Local time is the process zone.

Contract: context = hookSpecificOutput {hookEventName, additionalContext} JSON on stdout, exit 0. This hook
NEVER fails the tool: any error at all exits 0. Unparseable hook input still emits the clock line under
PostToolUse (the clock does not depend on the payload). Kill-switch: a pool worker, detected as env
ORCH_WORKER=1 OR env ORCH_VERIFY_OWNER present with any value, even empty (orch-verify exports the latter into
its worker shells and never sets the former), exits 0 with no output, so it never distorts worker output.
In-session subagents are deliberately NOT skipped (there is no agent_id check): they benefit from the true
time too, and this hook only adds context, it never blocks.

RESIDUAL COVERAGE (disclosed per disclose-guard-residuals). This INFORMS; it enforces nothing. The model can
still ignore the line or mis-copy it; the companion Stop hook (stamp-truth-stop.py) is the check. The line
reflects the host clock, so a wrong host clock (no NTP) is reproduced faithfully. Elapsed is only as right
as the lease: a lease id minted from a wrong clock, a stale id after an unclean exit, or (without
ORCH_LEASE_FILE) a cwd that selects another project's lease yields a wrong or missing elapsed. No session
ownership of the lease is validated. The events covered are exactly those listed under Coverage.

Self-test: python3 -I -B clock-inject.py --self-test
"""

import datetime
import json
import os
import re
import stat
import sys

LEASE_MAX_BYTES = 1 << 20
_SESS_RE = re.compile(r"[A-Za-z0-9]{1,32}-(\d{8}T\d{6}Z)")
_EVENTS = ("PostToolUse", "PostToolUseFailure")


def _is_worker(env=None):
    """True for an orch-verify pool worker: ORCH_WORKER=1, or ORCH_VERIFY_OWNER present (any value, even empty).
    Kept identical across the fleet hooks (python3 -I forbids a sibling import)."""
    env = os.environ if env is None else env
    return env.get("ORCH_WORKER") == "1" or "ORCH_VERIFY_OWNER" in env


# ---- lease / elapsed (kept identical to stamp-truth-stop.py; python3 -I forbids a sibling import) ----

def read_regular(path, limit):
    """Bytes (at most `limit`) of a REGULAR file, or None. Opened non-blocking so a FIFO cannot stall us."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_CLOEXEC", 0))
    except (OSError, TypeError, ValueError):
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        chunks, got = [], 0
        while got < limit:
            b = os.read(fd, min(1 << 16, limit - got))
            if not b:
                break
            chunks.append(b)
            got += len(b)
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(fd)


def lease_file(cwd=None):
    """Return the lease file path to use, or None when none can be derived."""
    env = os.environ.get("ORCH_LEASE_FILE")
    if env:
        return env
    proj = os.environ.get("CLAUDE_PROJECT_DIR")
    if proj and os.path.isabs(proj):
        cand = os.path.join(proj, ".working", "session-state.md")
        if os.path.isfile(cand):
            return cand
    root = os.environ.get("ORCH_PROJECT_ROOT")
    if root and os.path.isabs(root):
        return os.path.join(root, "private", "session-state.md")
    parts = os.path.abspath(cwd or os.getcwd()).split(os.sep)
    if len(parts) >= 3 and parts[0] == "" and parts[1] == "opt" and parts[2]:
        return os.path.join("/opt", parts[2], "private", "session-state.md")
    return None


def lease_start(path):
    """UTC start from the FIRST `Active-session:` line of `path`, or None (never searches past it)."""
    if not path:
        return None
    data = read_regular(path, LEASE_MAX_BYTES)
    if data is None:
        return None
    for line in data.decode("utf-8", "replace").splitlines():
        if line.startswith("Active-session:"):
            m = _SESS_RE.fullmatch(line[len("Active-session:"):].strip())
            if not m:
                return None
            try:
                return datetime.datetime.strptime(m.group(1), "%Y%m%dT%H%M%SZ").replace(
                    tzinfo=datetime.timezone.utc)
            except ValueError:
                return None
    return None


def fmt_elapsed(delta):
    """HH:MM (hours may exceed 24) for a non-negative timedelta, else None."""
    secs = int(delta.total_seconds())
    if secs < 0:
        return None
    return f"{secs // 3600:02d}:{(secs % 3600) // 60:02d}"


def clock_line(now_utc, start=None):
    local = now_utc.astimezone()
    line = (f"CLOCK (read by hook, authoritative): {local.strftime('%Y-%m-%d %H:%M:%S')} {local.tzname()} | "
            f"{now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    if start is not None:
        el = fmt_elapsed(now_utc - start)
        if el is not None:
            line += f" | session elapsed {el}"
    return line


def _emit(line, event="PostToolUse"):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": line}}))


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        if _is_worker():
            return 0
        try:
            payload = json.load(sys.stdin)
            if not isinstance(payload, dict):
                payload = {}
        except Exception:
            payload = {}
        event = payload.get("hook_event_name")
        event = event if event in _EVENTS else "PostToolUse"
        cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
        now = datetime.datetime.now(datetime.timezone.utc)
        _emit(clock_line(now, lease_start(lease_file(cwd))), event)
    except Exception:
        pass  # never fail the tool
    return 0


def _self_test():
    import io
    import shutil
    import subprocess
    import tempfile
    import unittest

    utc = datetime.timezone.utc
    line_re = re.compile(r"^CLOCK \(read by hook, authoritative\): \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \S+ \| "
                         r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z( \| session elapsed \d{2,}:\d{2})?$")

    def run_main(stdin_text, env=None):
        old_in, old_out, old_env = sys.stdin, sys.stdout, dict(os.environ)
        sys.stdin, sys.stdout = io.StringIO(stdin_text), io.StringIO()
        try:
            for k in ("ORCH_WORKER", "ORCH_VERIFY_OWNER", "ORCH_LEASE_FILE", "ORCH_PROJECT_ROOT",
                      "CLAUDE_PROJECT_DIR"):
                os.environ.pop(k, None)
            os.environ.update(env or {})
            rc = main(["clock-inject.py"])
            return rc, sys.stdout.getvalue()
        finally:
            sys.stdin, sys.stdout = old_in, old_out
            os.environ.clear()
            os.environ.update(old_env)

    class T(unittest.TestCase):
        def setUp(self):
            base = "/dev/shm" if os.path.isdir("/dev/shm") else None
            self.tmp = tempfile.mkdtemp(prefix="clk.", dir=base)
            self.lease = os.path.join(self.tmp, "session-state.md")
            self._env = {k: os.environ.pop(k, None) for k in ("ORCH_LEASE_FILE", "ORCH_PROJECT_ROOT",
                                                               "CLAUDE_PROJECT_DIR")}

        def tearDown(self):
            shutil.rmtree(self.tmp, ignore_errors=True)
            for k, v in self._env.items():
                os.environ.pop(k, None)
                if v is not None:
                    os.environ[k] = v

        def test_line_well_formed_with_elapsed(self):
            now = datetime.datetime(2026, 9, 23, 17, 45, 2, tzinfo=utc)
            ln = clock_line(now, datetime.datetime(2026, 9, 23, 14, 17, 10, tzinfo=utc))
            self.assertRegex(ln, line_re)
            self.assertIn("| 2026-09-23T17:45:02Z | session elapsed 03:27", ln)

        def test_line_omits_elapsed_when_unknown(self):
            ln = clock_line(datetime.datetime(2026, 9, 23, 17, 45, 2, tzinfo=utc), None)
            self.assertRegex(ln, line_re)
            self.assertNotIn("elapsed", ln)

        def test_future_lease_omits_elapsed(self):
            now = datetime.datetime(2026, 9, 23, 17, 0, 0, tzinfo=utc)
            self.assertNotIn("elapsed", clock_line(now, now + datetime.timedelta(hours=1)))

        def test_elapsed_over_24h(self):
            self.assertEqual(fmt_elapsed(datetime.timedelta(hours=27, minutes=5)), "27:05")

        def test_lease_parse_first_field_only(self):
            with open(self.lease, "w") as f:
                f.write("Status: active\nActive-session: sess-20260923T141710Z\n"
                        "Active-session: sess-20200101T000000Z\n")
            self.assertEqual(lease_start(self.lease), datetime.datetime(2026, 9, 23, 14, 17, 10, tzinfo=utc))

        def test_inactive_lease_never_reads_history(self):
            # finding: `none` followed by a history line used to resolve to the historical id
            with open(self.lease, "w") as f:
                f.write("Active-session: none\n## History\nActive-session: sess-20200101T000000Z\n")
            self.assertIsNone(lease_start(self.lease))
            with open(self.lease, "w") as f:
                f.write("Active-session: sess-2026BAD\nActive-session: sess-20200101T000000Z\n")
            self.assertIsNone(lease_start(self.lease))

        def test_lease_missing(self):
            self.assertIsNone(lease_start(os.path.join(self.tmp, "absent.md")))
            self.assertIsNone(lease_start(None))

        def test_fifo_lease_does_not_block(self):
            fifo = os.path.join(self.tmp, "fifo")
            os.mkfifo(fifo)
            code = ("import importlib.util as u;s=u.spec_from_file_location('m',%r);m=u.module_from_spec(s);"
                    "s.loader.exec_module(m);print(m.lease_start(%r))" % (os.path.abspath(__file__), fifo))
            r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, timeout=5)
            self.assertEqual(r.stdout.strip(), "None")

        def test_lease_file_derivation(self):
            self.assertEqual(lease_file("/opt/proj/work/x"), "/opt/proj/private/session-state.md")
            self.assertIsNone(lease_file("/home/someone"))
            os.environ["ORCH_PROJECT_ROOT"] = "/srv/proj"
            self.assertEqual(lease_file("/home/someone"), "/srv/proj/private/session-state.md")
            os.environ["ORCH_LEASE_FILE"] = self.lease
            self.assertEqual(lease_file("/opt/proj"), self.lease)

        def test_garbage_input_emits_and_exits_0(self):
            rc, out = run_main("}{ not json", {"ORCH_LEASE_FILE": self.lease})
            self.assertEqual(rc, 0)
            obj = json.loads(out)
            self.assertEqual(obj["hookSpecificOutput"]["hookEventName"], "PostToolUse")
            self.assertRegex(obj["hookSpecificOutput"]["additionalContext"], line_re)

        def test_payload_with_lease_emits_elapsed(self):
            with open(self.lease, "w") as f:
                f.write("Active-session: sess-20000101T000000Z\n")
            rc, out = run_main(json.dumps({"tool_name": "Bash", "cwd": "/"}), {"ORCH_LEASE_FILE": self.lease})
            self.assertEqual(rc, 0)
            self.assertIn("session elapsed", json.loads(out)["hookSpecificOutput"]["additionalContext"])

        def test_failure_event_name_matches(self):
            rc, out = run_main(json.dumps({"hook_event_name": "PostToolUseFailure", "tool_name": "Bash"}))
            self.assertEqual(json.loads(out)["hookSpecificOutput"]["hookEventName"], "PostToolUseFailure")
            rc, out = run_main(json.dumps({"hook_event_name": "PostToolUse", "tool_name": "Bash"}))
            self.assertEqual(json.loads(out)["hookSpecificOutput"]["hookEventName"], "PostToolUse")
            rc, out = run_main(json.dumps({"hook_event_name": "Bogus"}))
            self.assertEqual(json.loads(out)["hookSpecificOutput"]["hookEventName"], "PostToolUse")

        def test_worker_kill_switch_silent(self):
            rc, out = run_main(json.dumps({"tool_name": "Bash"}), {"ORCH_WORKER": "1"})
            self.assertEqual((rc, out), (0, ""))

        def test_worker_detected_by_verify_owner(self):
            # finding: orch-verify exports ORCH_VERIFY_OWNER into worker shells and never sets ORCH_WORKER
            for value in ("guardrails", ""):
                rc, out = run_main(json.dumps({"tool_name": "Bash"}), {"ORCH_VERIFY_OWNER": value})
                self.assertEqual((rc, out), (0, ""))
            self.assertTrue(_is_worker({"ORCH_VERIFY_OWNER": ""}))
            self.assertTrue(_is_worker({"ORCH_WORKER": "1"}))
            self.assertFalse(_is_worker({"ORCH_WORKER": "0"}))
            self.assertFalse(_is_worker({}))

        def test_subagent_still_gets_clock(self):
            # deliberate: in-session subagents are not skipped (context only, never a block)
            rc, out = run_main(json.dumps({"tool_name": "Bash", "agent_id": "a1"}))
            self.assertRegex(json.loads(out)["hookSpecificOutput"]["additionalContext"], line_re)

        def test_lease_label_portability(self):
            want = datetime.datetime(2026, 9, 23, 14, 17, 10, tzinfo=utc)
            for label in ("sess", "S88", "a", "A" * 32):
                with open(self.lease, "w") as f:
                    f.write(f"Active-session: {label}-20260923T141710Z\n")
                self.assertEqual(lease_start(self.lease), want, label)
            for bad in ("A" * 33 + "-20260923T141710Z", "-20260923T141710Z", "S_88-20260923T141710Z",
                        "S88 20260923T141710Z", "S88-20260923T141710"):
                with open(self.lease, "w") as f:
                    f.write(f"Active-session: {bad}\nActive-session: sess-20200101T000000Z\n")
                self.assertIsNone(lease_start(self.lease), bad)

        def test_lease_discovery_precedence(self):
            proj = os.path.join(self.tmp, "proj")
            wlease = os.path.join(proj, ".working", "session-state.md")
            os.environ["ORCH_PROJECT_ROOT"] = "/srv/proj"
            os.environ["CLAUDE_PROJECT_DIR"] = proj
            # CLAUDE_PROJECT_DIR lease absent: falls through to ORCH_PROJECT_ROOT
            self.assertEqual(lease_file("/opt/x"), "/srv/proj/private/session-state.md")
            os.makedirs(os.path.dirname(wlease))
            with open(wlease, "w") as f:
                f.write("Active-session: S88-20260923T141710Z\n")
            self.assertEqual(lease_file("/opt/x"), wlease)          # beats ORCH_PROJECT_ROOT and cwd
            os.environ["ORCH_LEASE_FILE"] = self.lease
            self.assertEqual(lease_file("/opt/x"), self.lease)      # ORCH_LEASE_FILE beats all
            del os.environ["ORCH_LEASE_FILE"], os.environ["ORCH_PROJECT_ROOT"]
            os.environ["CLAUDE_PROJECT_DIR"] = "rel/proj"           # relative: ignored
            self.assertEqual(lease_file("/opt/x/y"), "/opt/x/private/session-state.md")
            os.environ["CLAUDE_PROJECT_DIR"] = proj
            rc, out = run_main(json.dumps({"tool_name": "Bash", "cwd": "/"}), {"CLAUDE_PROJECT_DIR": proj})
            self.assertIn("session elapsed", json.loads(out)["hookSpecificOutput"]["additionalContext"])

    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
