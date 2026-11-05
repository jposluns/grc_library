#!/usr/bin/env python3
"""PreToolUse AskUserQuestion hook: block a blocking prompt in unattended mode.

Shipped 2026-07-17 (the Mistake-1 fix). Reads the PreToolUse JSON payload on stdin,
reads the operating mode, and BLOCKS
(exit 2, reason on stderr) an ``AskUserQuestion`` call when the mode is unattended
(``overnight-unattended`` / ``daytime-unattended``). In unattended mode a maintainer
decision is recorded as pending and the run CONTINUES (no-idle-stop); a blocking prompt
idles the run until the maintainer returns. The recurrence that motivated it: an r4
deep-assessment Phase-8 sign-off was posed as an ``AskUserQuestion`` during overnight
mode and idled the run ~7 hours (with the work it was blocking already unblocked).
Attended modes (``attended``, ``fully-attended``, ``attended-autonomous``, and the fleet's
``decisions`` mode) allow the call; only an exact unattended mode (``unattended``,
``daytime-unattended``, ``overnight-unattended``) blocks.

Mode source (fixed 2026-09-25, maintainer-caught; extracted to the shared reader
``.claude/hooks/_operating_mode.py`` in 3b781). The AUTHORITY is the fleet's canonical,
root-owned mode file ``/opt/orch-operator/operating-mode`` (JSON: ``mode``, ``set_at``). Before the
2026-09-25 fix the hook read only the lease's ``Operating-mode`` field (``session-state.md``), a
hand-synced copy: the fleet went unattended at 2026-09-25T00:25:42Z while the lease still said
``attended-autonomous``, and an AskUserQuestion passed. Now the shared reader decides: a fleet
unattended (or fail-closed) reading blocks whatever the lease says; with the fleet file attended,
a lease DATED swap ``<mode>@<utc>`` (the CLAUDE.md #5(b) timeout swap) blocks only while its stamp
is strictly newer than the fleet ``set_at``, an undated lease value is superseded by any readable
fleet file (the supersession is named in the source, never silently dropped), and the lease
decides only when NOTHING exists at the fleet path, exactly as before 3b781: the reader hands
an undated value back RAW and this hook applies its own legacy rule, blocking on any value
that mentions ``unattended`` (stricter-is-safer). A fleet file that exists but cannot yield a
recognized mode WITH a parseable ``set_at`` (unreadable, wrong owner, a symlink, malformed or
duplicate-key JSON, a missing or non-string ``mode``, an unrecognized value, a directory, a FIFO,
or a missing ``set_at``) FAILS CLOSED to unattended, and so does a missing or unloadable shared
reader. There is no environment override of the fleet path (the self-test passes a path and an
owner uid as parameters), so no configuration switches the fleet file off.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason. The PAYLOAD fails open (an unparseable or non-object
payload does not block by itself), because a hook that blocked on a malformed payload would be
worse than the mistake it prevents; the MODE fails closed as described above. This is a
guardrail against one known mistake shape, not a security boundary, and it is defence in depth
with the no-blocking-questions-unattended discipline, not a substitute for it. NOTE: like the
sibling pipe-guard, this hook does not fire in a child session whose
``CLAUDE_PROJECT_DIR`` is unset (documented harness limitation); the discipline is the
primary control either way.

Self-test: ``python3 .claude/hooks/block-askuserquestion-unattended.py --self-test``.
"""

import json
import os
import re
import stat
import sys
from pathlib import Path

# The plain `Operating-mode: <mode>` line (gate 63's form since 3b679) or the earlier bold form,
# at column zero; the value is separated by spaces or tabs only, never a line end (3b679 r3).
MODE_RE = re.compile(r"(?:\*\*Operating-mode:\*\*|Operating-mode:)[ \t]+(\S+)[ \t]*")
COMMENT_DELIMITER = re.compile(r"<!--|-->")


def lease_mode_value(text: str) -> str | None:
    """The first exact `Operating-mode:` line's value, skipping every line that starts inside an
    HTML comment ("<!--" opens and "-->" closes one wherever either appears, across lines; no
    nesting; an unclosed comment runs to EOF). Lines split on LF; one trailing CR is dropped."""
    comment = False
    for raw in text.split("\n"):
        if not comment:
            m = MODE_RE.fullmatch(raw.removesuffix("\r"))
            if m:
                return m.group(1)
        for delimiter in COMMENT_DELIMITER.finditer(raw):
            comment = delimiter.group() == "<!--"
    return None


# `.working/` -> `_private` migration: resolve the (maintainer-only) working-state file through
# lint_common.resolve_working (the operational store, /opt/grc/private by default, preferred; then the private sibling, then in-repo). Fail-SAFE: if the
# helper cannot be imported, fall back to the historical in-repo path so this hook never breaks.
def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and every component from that root down to the hook and down to the helper (the
    root itself, .claude, .claude/hooks, tools, the hook file and the helper file)
    must not be a symlink; only then are real paths compared, requiring the hook's and
    the helper's real locations to sit at exactly their expected places under the real
    repository root (ancestors ABOVE the root may be symlinks: both sides of each
    comparison resolve them identically). Any violation is REFUSED fail-closed: exit 2
    with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        # A launch path holding a newline or a terminal escape is shown escaped, so the refusal
        # stays one line: block-turn-end-with-outstanding-work.py's rule (each character that is
        # neither printable nor a space separator becomes its ascii() escape).
        import unicodedata
        why = "".join(char if char.isprintable() or unicodedata.category(char) == "Zs"
                      else ascii(char)[1:-1] for char in why)
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = (".claude", "hooks") if name.startswith("_") else ("tools",)
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


try:
    _resolve_working = _load_sibling("lint_common").resolve_working
except Exception:  # pragma: no cover - fail-safe: never let a helper-load failure break the hook
    _resolve_working = None


def _working_file(rel_below, root):
    """`.working/<rel_below>` resolved via lint_common (private preferred), or None."""
    if _resolve_working is not None:
        return _resolve_working(rel_below, repo_root=root)
    cand = root / ".working" / rel_below
    return cand if cand.exists() else None


CANONICAL_MODE_FILE = "/opt/orch-operator/operating-mode"
UNATTENDED = frozenset({"unattended", "daytime-unattended", "overnight-unattended"})
# Modes in which the operator is present (the fleet's `decisions` mode exists so the operator can
# answer questions before going unattended).
ATTENDED = frozenset({"attended", "attended-autonomous", "fully-attended", "decisions"})


class _Unusable(Exception):
    pass


_MAX_BYTES = 65536


def _read_regular(path) -> bytes:
    """Read a REGULAR file without blocking (a FIFO or device raises), bounded: an oversized file
    raises, so a prefix is never mistaken for the whole file."""
    fd = os.open(str(path), os.O_RDONLY | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise _Unusable("not a regular file")
        raw = os.read(fd, _MAX_BYTES + 1)
    finally:
        os.close(fd)
    if len(raw) > _MAX_BYTES:
        raise _Unusable("oversized")
    return raw


def read_canonical_mode(path: str = CANONICAL_MODE_FILE,
                        require_owner_uid: int = 0) -> tuple[str | None, str]:
    """Return (mode, note) from the fleet's canonical mode file, via the shared reader
    (.claude/hooks/_operating_mode.py; 3b781). (None, "absent") only when the path genuinely
    does not exist; every other defect, a missing or unloadable shared reader, and a reader
    call that raises (3b781 r3, codex E1) FAIL CLOSED to "unattended" (blocking a prompt is
    this hook's safe direction). An isolation REFUSAL inside _load_sibling raises
    SystemExit(2), which blocks the call outright."""
    try:
        helper = _load_sibling("_operating_mode")
    except SystemExit:
        raise
    except Exception:  # noqa: BLE001 (a missing reader must not weaken the guard)
        return "unattended", "operating-mode reader unavailable (fail closed)"
    try:
        mode, _set_at, note = helper.read_fleet(path, require_owner_uid)
    except Exception:  # noqa: BLE001 (a raising reader must not weaken the guard)
        return "unattended", "operating-mode reader failed (fail closed)"
    return mode, note


def read_lease_mode(project_dir: str) -> str | None:
    """The lease's raw `Operating-mode` token, or None. The RAW token is returned (not lowered):
    a dated swap's stamp is case-sensitive, and the shared reader normalizes the mode's case."""
    try:
        ss = _working_file("session-state.md", Path(project_dir))
        if ss is None:
            return None  # no lease -> no lease mode
        text = _read_regular(ss).decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 (a bad project dir or unreadable lease is "no lease mode")
        return None
    return lease_mode_value(text) or None


def read_mode(project_dir: str, canonical_path: str = CANONICAL_MODE_FILE,
              require_owner_uid: int = 0) -> tuple[str | None, str]:
    """(mode, source), via the shared reader's effective_mode (3b781). The fleet file is the
    authority: a fleet unattended (or fail-closed) reading wins outright; with the fleet file
    attended, a lease DATED swap (the CLAUDE.md #5(b) timeout swap) counts only while its stamp
    is strictly newer than the fleet set_at, and an undated lease value is superseded by any
    readable fleet file, with the supersession named in the source; the lease decides only when
    the fleet file is absent. The canonical path and owner uid are parameters for the self-test
    only; there is deliberately no environment override, so no configuration can switch the
    fleet file off. A missing or unloadable shared reader, and a reader call that
    raises (3b781 r3, codex E1), fail closed to unattended.
    With the fleet file ABSENT the reader returns an undated lease value RAW (3b781 r2)
    and this hook applies its own pre-3b781 legacy rule: any lease value that mentions
    "unattended" blocks (stricter-is-safer). A fleet-derived or dated-swap mode is always
    canonical (in UNATTENDED or ATTENDED), so only the raw absent-fleet value, which is
    in neither set, can take that branch."""
    try:
        helper = _load_sibling("_operating_mode")
    except SystemExit:
        raise
    except Exception:  # noqa: BLE001 (a missing reader must not weaken the guard)
        return "unattended", "operating-mode reader unavailable (fail closed)"
    try:
        mode, source = helper.effective_mode(canonical_path, read_lease_mode(project_dir),
                                             require_owner_uid)
    except Exception:  # noqa: BLE001 (a raising reader must not weaken the guard)
        return "unattended", "operating-mode reader failed (fail closed)"
    if (isinstance(mode, str) and mode not in UNATTENDED and mode not in ATTENDED
            and "unattended" in mode.lower()):
        return "unattended", f"{source} (mentions unattended; this hook's legacy rule)"
    return mode, source


def decide(mode: str | None, source: str = "") -> tuple[bool, str]:
    """Return (block, reason). Block only on an exact unattended mode."""
    if mode in UNATTENDED:
        return True, (
            f"BLOCKED (askuserquestion-unattended): an AskUserQuestion while the operating mode "
            f"is `{mode}` (source: {source or 'unspecified'}).\n"
            f"WHY: a blocking prompt idles the run until the maintainer returns; unattended mode "
            f"records a maintainer decision as pending and CONTINUES (no-idle-stop).\n"
            f"CONSIDER INSTEAD: record the decision (with options and a recommendation) in the "
            f"pending-decisions register and proceed on the next authorized independent item via "
            f"graceful degradation (stricter-safe on a reversible action, defer-and-skip on an "
            f"authorial one). Only the operator ends unattended mode: the fleet mode file "
            f"({CANONICAL_MODE_FILE}) is operator-set and an assistant never edits it, and a lease "
            f"that is more unattended than the fleet file (a timeout swap) is ended only on an "
            f"explicit operator instruction, never because the fleet file already reads attended."
        )
    return False, ""


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # The fleet decision needs no payload: an unparseable payload still blocks when the fleet
        # file reads unattended (or is unusable), and otherwise fails open.
        payload = None
    if payload is None:
        result = read_canonical_mode()  # the fleet decision alone; allows unless it blocks
    else:
        if not isinstance(payload, dict):
            payload = {}  # a non-object payload carries no project dir; resolve it below
        workspace = payload.get("workspace")
        workspace = workspace if isinstance(workspace, dict) else {}
        project_dir = (
            workspace.get("project_dir")
            or os.environ.get("CLAUDE_PROJECT_DIR")
            # Last-resort fallback: resolve the project root from this hook's own location
            # (<project>/.claude/hooks/this.py -> parents[2]). No hardcoded path, so it stays
            # correct across a repo move (for example an /old/root -> /new/root relocation).
            or str(Path(__file__).resolve().parents[2])
        )
        result = read_mode(str(project_dir))
    # read_mode returns (mode, source); a bare mode string is accepted too (the message-contract
    # test in tests/test_linters.py patches read_mode at that seam).
    mode, source = result if isinstance(result, tuple) else (result, "")
    block, reason = decide(mode, source)
    if block:
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    os.environ.pop("GRC_STORE", None)  # the lease fixtures must not resolve to a real store

    def lease_root(d: str, mode: str | None, label: str = "Operating-mode:") -> str:
        root = Path(d) / "proj"
        (root / ".working").mkdir(parents=True)
        if mode is not None:
            (root / ".working" / "session-state.md").write_text(
                f"{label} {mode}\n", encoding="utf-8")
        return str(root)

    class T(unittest.TestCase):
        def test_plain_and_bold_lease_labels(self):
            # 3b679: the lease moves from **Operating-mode:** to the plain line; both read.
            for label in ("Operating-mode:", "**Operating-mode:**"):
                with tempfile.TemporaryDirectory() as d:
                    root = lease_root(d, "overnight-unattended", label)
                    self.assertEqual(read_lease_mode(root), "overnight-unattended", label)
            for label in ("**Operating-mode**:", " Operating-mode:", "Operating-mode :"):
                with tempfile.TemporaryDirectory() as d:
                    self.assertIsNone(read_lease_mode(lease_root(d, "overnight-unattended", label)), label)

        def test_commented_mode_lines_are_not_read(self):
            # 3b679 r3: only a column-zero field line outside every HTML comment is read, and the
            # value never crosses a line end (an empty commented label used to read "-->").
            head = "# Session state: grc\n\n"
            for text in ("<!-- Operating-mode: overnight-unattended -->\n",
                         "<!--\nOperating-mode: overnight-unattended\n-->\n",
                         "note <!-- was\nOperating-mode: overnight-unattended\n-->\n",
                         "<!--\n**Operating-mode:** overnight-unattended\n-->\n",
                         "<!--\nOperating-mode:\n-->\n", "Operating-mode:\n-->\n",
                         "Operating-mode: \noverall\n"):
                self.assertIsNone(lease_mode_value(head + text), text)
                with tempfile.TemporaryDirectory() as d:
                    root = Path(d) / "proj"
                    (root / ".working").mkdir(parents=True)
                    (root / ".working" / "session-state.md").write_text(head + text, encoding="utf-8")
                    self.assertIsNone(read_lease_mode(str(root)), text)
            for line in ("Operating-mode: fully-attended", "**Operating-mode:** fully-attended"):
                for above in ("<!--\nOperating-mode: overnight-unattended\n-->\n",
                              "note <!-- x\nOperating-mode: overnight-unattended\n-->\n",
                              "<!-- Operating-mode: overnight-unattended -->\n"):
                    text = head + above + line + "\n<!-- note -->\n"
                    self.assertEqual(lease_mode_value(text), "fully-attended", (above, line))

        def test_exact_modes(self):
            self.assertTrue(decide("overnight-unattended")[0])
            self.assertTrue(decide("daytime-unattended")[0])
            self.assertTrue(decide("unattended")[0])
            for m in ("attended-autonomous", "fully-attended", "attended", "decisions", None,
                      "attended-not-unattended"):
                self.assertFalse(decide(m)[0], m)

        def test_stale_lease_incident(self):
            # 2026-09-25: fleet file unattended, lease still attended-autonomous -> block.
            # Re-anchored on the shared reader (3b781): the fixture carries set_at and the
            # test passes its own uid as the required owner (the live default is uid 0).
            with tempfile.TemporaryDirectory() as d:
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"unattended","set_by":"x",'
                                 '"set_at":"2026-09-25T00:25:42Z"}', encoding="utf-8")
                root = lease_root(d, "attended-autonomous")
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0])

        def test_unusable_fleet_file_fails_closed(self):
            set_at = '"set_at":"2026-11-01T12:00:00Z"'
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, "attended-autonomous")
                fleet = Path(d) / "operating-mode"
                bodies = ['{"mode":"unattended"', '{"mode":"unattended","mode":"attended"}',
                          '{"mode":["unattended"],%s}' % set_at, '{"set_by":"x",%s}' % set_at,
                          '{"mode":"bananas",%s}' % set_at,
                          '{"mode":"attended"}',  # missing set_at is load-bearing (3b781)
                          '{"mode":"attended","set_at":"not-a-time"}', "", "[]"]
                for body in bodies:
                    fleet.write_text(body, encoding="utf-8")
                    self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0], body)
                # the wrong owner fails closed (fail direction only: an unprivileged test
                # cannot make a root-owned fixture, so the pass direction is untestable here)
                fleet.write_text('{"mode":"attended",%s}' % set_at, encoding="utf-8")
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid() + 1))[0])
                fleet.write_bytes(b"\xff\xfe{")
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0])
                fleet.unlink()
                fleet.mkdir()
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0])
                fleet.rmdir()
                os.mkfifo(str(fleet))  # a FIFO must fail closed without blocking
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0])
                fleet.unlink()
                os.symlink(str(Path(d) / "missing"), str(fleet))
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0])
                fleet.unlink()  # a symlink to a VALID attended file also fails closed (3b781)
                valid = Path(d) / "valid"
                valid.write_text('{"mode":"attended",%s}' % set_at, encoding="utf-8")
                os.symlink(str(valid), str(fleet))
                self.assertTrue(decide(*read_mode(root, str(fleet), os.geteuid()))[0])
                if os.geteuid() != 0:  # an inaccessible parent directory fails closed
                    locked = Path(d) / "locked"
                    locked.mkdir()
                    (locked / "operating-mode").write_text(
                        '{"mode":"attended",%s}' % set_at, encoding="utf-8")
                    locked.chmod(0)
                    try:
                        self.assertTrue(decide(*read_mode(
                            root, str(locked / "operating-mode"), os.geteuid()))[0])
                    finally:
                        locked.chmod(0o700)
                # a bad project dir cannot undo a fleet-unattended block
                fleet.unlink()
                fleet.write_text('{"mode":"unattended",%s}' % set_at, encoding="utf-8")
                self.assertTrue(decide(*read_mode("a\x00b", str(fleet), os.geteuid()))[0])

        def test_missing_reader_fails_closed(self):
            # 3b781: a missing or unloadable shared reader must not weaken the guard.
            from unittest import mock
            with mock.patch.dict(globals(), {"_load_sibling":
                                             mock.Mock(side_effect=OSError("absent"))}):
                self.assertEqual(read_mode("/nonexistent", "/nonexistent")[0], "unattended")
                self.assertEqual(read_canonical_mode("/nonexistent")[0], "unattended")

        def test_reader_exception_fails_closed_read_mode(self):
            # 3b781 r3 (codex E1): a reader-call exception in read_mode must take the
            # blocking fail-closed path (exit 2), never escape as a traceback (exit 1).
            from unittest import mock
            raising = mock.Mock()
            raising.effective_mode.side_effect = RuntimeError("reader defect")
            with mock.patch.dict(globals(), {"_load_sibling":
                                             mock.Mock(return_value=raising)}):
                mode, source = read_mode("/nonexistent", "/nonexistent")
            self.assertEqual(mode, "unattended")
            self.assertTrue(decide(mode, source)[0])

        def test_reader_exception_fails_closed_canonical(self):
            # 3b781 r3 (codex E1): the payloadless read_canonical_mode entry path
            # fails closed on a reader-call exception too.
            from unittest import mock
            raising = mock.Mock()
            raising.read_fleet.side_effect = RuntimeError("reader defect")
            with mock.patch.dict(globals(), {"_load_sibling":
                                             mock.Mock(return_value=raising)}):
                mode, note = read_canonical_mode("/nonexistent")
            self.assertEqual(mode, "unattended")
            self.assertTrue(decide(mode, note)[0])

        def test_bom_and_case_are_read(self):
            # 3b781 r3 (codex W3): an otherwise valid ATTENDED fixture read through the
            # BOM and case normalization to the specific allowing result, so removing
            # either cannot hide behind the fail-closed default.
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, "attended-autonomous")
                fleet = Path(d) / "operating-mode"
                fleet.write_text('\ufeff{"mode":" Attended ","set_at":"2026-11-01T12:00:00Z"}',
                                 encoding="utf-8")
                mode, source = read_mode(root, str(fleet), os.geteuid())
                self.assertEqual((mode, source), ("attended", "fleet mode file"))
                self.assertFalse(decide(mode, source)[0])

        def test_fleet_nonjson_constants_fail_closed(self):
            # 3b781 r4 (codex E1): NaN, Infinity and -Infinity are not JSON; each
            # constant alone in an otherwise valid ATTENDED fleet fixture must fail
            # closed to a block through this hook, on the payload path and on the
            # payloadless read_canonical_mode path, never read as attended.
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, "attended-autonomous")
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"attended","set_at":"2026-11-01T12:00:00Z"}',
                                 encoding="utf-8")
                self.assertFalse(  # control: the fixture is otherwise valid attended
                    decide(*read_mode(root, str(fleet), os.geteuid()))[0])
                for constant in ("NaN", "Infinity", "-Infinity"):
                    fleet.write_text('{"mode":"attended","set_at":"2026-11-01T12:00:00Z",'
                                     '"phase":%s}' % constant, encoding="utf-8")
                    mode, source = read_mode(root, str(fleet), os.geteuid())
                    self.assertEqual(
                        (mode, source),
                        ("unattended",
                         "unusable fleet mode file (non-JSON constant %s)" % constant),
                        constant)
                    self.assertTrue(decide(mode, source)[0], constant)
                    mode, note = read_canonical_mode(str(fleet), os.geteuid())
                    self.assertTrue(decide(mode, note)[0], constant)

        def test_malformed_lease_and_oversized_fleet(self):
            with tempfile.TemporaryDirectory() as d:
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"attended","set_at":"2026-11-01T12:00:00Z"}',
                                 encoding="utf-8")
                with tempfile.TemporaryDirectory() as e:
                    # 3b781 NEW behaviour: an UNDATED unattended-ish lease value, malformed
                    # included, is superseded by a readable attended fleet file (it used to
                    # block as stricter-is-safer); the supersession is named in the source.
                    for n, bad in enumerate(("daytime-unattended.", "unattended-overnight",
                                             "overnight_unattended")):
                        root = lease_root(os.path.join(e, str(n)), bad)
                        mode, source = read_mode(root, str(fleet), os.geteuid())
                        self.assertFalse(decide(mode, source)[0], bad)
                        self.assertIn("supersedes undated lease", source, bad)
                big = Path(d) / "big"
                # 3b781 r3 (codex W3): valid attended JSON with set_at end to end,
                # so only the size bound rejects it, and its reason is asserted.
                big.write_bytes(b'{"mode":"attended","set_at":"2026-11-01T12:00:00Z"}'
                                .ljust(_MAX_BYTES + 1, b" "))
                root = lease_root(os.path.join(d, "x"), "attended-autonomous")
                mode, source = read_mode(root, str(big), os.geteuid())
                self.assertEqual((mode, source),
                                 ("unattended", "unusable fleet mode file (oversized)"))
                self.assertTrue(decide(mode, source)[0])
                fifo_root = Path(d) / "fifo" / "proj"
                (fifo_root / ".working").mkdir(parents=True)
                os.mkfifo(str(fifo_root / ".working" / "session-state.md"))
                self.assertFalse(  # no hang
                    decide(*read_mode(str(fifo_root), str(fleet), os.geteuid()))[0])

        def test_timeout_swap_and_absent_fallback(self):
            # 3b781: the #5(b) timeout swap is a DATED record, honoured only while newer
            # than the fleet set_at; an undated swap is superseded (fails at 430da42ef).
            with tempfile.TemporaryDirectory() as d:
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"attended","set_at":"2026-11-01T12:00:00Z"}',
                                 encoding="utf-8")
                undated = lease_root(os.path.join(d, "a"), "daytime-unattended")
                mode, source = read_mode(undated, str(fleet), os.geteuid())
                self.assertFalse(decide(mode, source)[0])  # undated swap superseded (NEW)
                self.assertIn("supersedes undated lease", source)
                newer = lease_root(os.path.join(d, "b"),
                                   "daytime-unattended@2026-11-01T12:00:01Z")
                self.assertTrue(  # dated swap newer than set_at blocks
                    decide(*read_mode(newer, str(fleet), os.geteuid()))[0])
                older = lease_root(os.path.join(d, "c"),
                                   "daytime-unattended@2026-11-01T11:59:59Z")
                mode, source = read_mode(older, str(fleet), os.geteuid())
                self.assertFalse(decide(mode, source)[0])  # stale swap superseded, named
                self.assertIn("supersedes lease swap", source)
                dated_attended = lease_root(os.path.join(d, "e"),
                                            "attended@2026-11-02T00:00:00Z")
                self.assertFalse(  # a dated attended value is ignored (only-adds rule)
                    decide(*read_mode(dated_attended, str(fleet), os.geteuid()))[0])
                missing = str(Path(d) / "absent")
                # 3b781 r2 (codex E2): with the fleet file absent the reader returns the
                # raw lease value and THIS hook's legacy mentions-unattended rule applies
                # (the malformed unattended-overnight still blocks); the stop guard keeps
                # its different leading-token rule.
                for swap in ("daytime-unattended", "daytime-unattended@2026-11-01T12:00:01Z",
                             "unattended-overnight"):
                    root = lease_root(os.path.join(d, "f" + swap[-1]), swap)
                    self.assertTrue(  # absent fleet -> the lease decides, dated or legacy
                        decide(*read_mode(root, missing, os.geteuid()))[0], swap)
                attended_raw = lease_root(os.path.join(d, "g"), "fully-attended")
                mode, source = read_mode(attended_raw, missing, os.geteuid())
                self.assertFalse(decide(mode, source)[0])  # a raw attended value allows
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, None)
                self.assertFalse(decide(*read_mode(root, str(Path(d) / "absent")))[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
