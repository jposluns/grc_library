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

Mode source (fixed 2026-09-25, maintainer-caught). The AUTHORITY is the fleet's canonical,
root-owned mode file ``/opt/orch-operator/operating-mode`` (JSON, its ``mode`` field). Before the
fix the hook read only the lease's ``Operating-mode`` field (``session-state.md``), a hand-synced
copy: the fleet went unattended at 2026-09-25T00:25:42Z while the lease still said
``attended-autonomous``, and an AskUserQuestion passed. Now: an unattended reading from EITHER the
fleet file or the lease blocks (stricter-is-safer; the lease can legitimately be more unattended
through the CLAUDE.md #5(b) timeout swap); otherwise the fleet file decides; the lease decides
only when NOTHING exists at the fleet path. A fleet file that exists but cannot yield a recognized
mode (unreadable, malformed or duplicate-key JSON, a missing or non-string ``mode``, an
unrecognized value, a directory or a dangling symlink) FAILS CLOSED to unattended. There is no
environment override of the fleet path (the self-test passes a path as a parameter), so no
configuration switches the fleet file off.

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

MODE_RE = re.compile(r"^\*\*Operating-mode:\*\*\s+(\S+)\s*$", re.MULTILINE)


# `.working/` -> `_private` migration: resolve the (maintainer-only) working-state file through
# lint_common.resolve_working (private sibling preferred, in-repo fallback). Fail-SAFE: if the
# helper cannot be imported, fall back to the historical in-repo path so this hook never breaks.
_TOOLS_DIR = str(Path(__file__).resolve().parents[2] / "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
try:
    from lint_common import resolve_working as _resolve_working
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


def _no_duplicate_keys(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise _Unusable("duplicate key")
    return dict(pairs)


def read_canonical_mode(path: str = CANONICAL_MODE_FILE) -> tuple[str | None, str]:
    """Return (mode, note) from the fleet's canonical mode file.

    (None, "absent") only when the path genuinely does not exist (lstat raises ENOENT, or ENOTDIR
    because a path component is not a directory); that
    is the ONE case that falls back to the lease. Anything else that cannot yield a recognized
    mode FAILS CLOSED to "unattended": an inaccessible parent directory, a dangling symlink, a
    non-regular file (a directory, FIFO or device, rejected before any read so nothing can
    block), an unreadable file, malformed or duplicate-key JSON, a missing or non-string `mode`,
    or an unrecognized value. Ignorance never permits: an unusable authority is exactly when a
    stale lease would otherwise decide."""
    try:
        os.lstat(path)
    except (FileNotFoundError, NotADirectoryError):
        return None, "absent"
    except Exception as exc:  # noqa: BLE001 (e.g. PermissionError on a parent directory)
        return "unattended", f"unusable fleet mode file ({type(exc).__name__})"
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise _Unusable("not a regular file")
            raw = os.read(fd, _MAX_BYTES + 1)
        finally:
            os.close(fd)
        if len(raw) > _MAX_BYTES:
            raise _Unusable("oversized")  # a prefix is not the file; an oversized file fails closed
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_no_duplicate_keys)
        mode = data.get("mode") if isinstance(data, dict) else None
        if not isinstance(mode, str):
            raise _Unusable("no string mode")
        mode = mode.strip().lower()
    except Exception as exc:  # noqa: BLE001 (any unusable authority fails closed)
        return "unattended", f"unusable fleet mode file ({type(exc).__name__})"
    if mode in UNATTENDED or mode in ATTENDED:
        return mode, "fleet mode file"
    return "unattended", f"unrecognized fleet mode {mode!r}"


def read_lease_mode(project_dir: str) -> str | None:
    try:
        ss = _working_file("session-state.md", Path(project_dir))
        if ss is None:
            return None  # no lease -> no lease mode
        text = _read_regular(ss).decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 (a bad project dir or unreadable lease is "no lease mode")
        return None
    m = MODE_RE.search(text)
    return m.group(1).lower() if m else None


def read_mode(project_dir: str, canonical_path: str = CANONICAL_MODE_FILE) -> tuple[str | None, str]:
    """(mode, source). Stricter-is-safer: an unattended reading from EITHER source wins (the lease
    can legitimately be MORE unattended than the fleet file, through the CLAUDE.md #5(b) timeout
    swap). Otherwise the fleet file decides; the lease decides only when the fleet file is absent.
    The canonical path is a parameter for the self-test only; there is deliberately no
    environment override, so no configuration can switch the fleet file off."""
    canonical, note = read_canonical_mode(canonical_path)
    if canonical in UNATTENDED:
        return canonical, note  # decided before the lease is touched, so no lease error can undo it
    lease = read_lease_mode(project_dir)
    # The lease can only ADD a block (a timeout swap), never remove one, so any lease value that
    # mentions "unattended", however malformed, counts as unattended (stricter-is-safer).
    lease_unattended = bool(lease) and "unattended" in lease
    if canonical is None:
        if lease_unattended:
            return "unattended", f"lease Operating-mode {lease!r} (fleet mode file absent)"
        return lease, "lease Operating-mode (fleet mode file absent)"
    if lease_unattended:
        return "unattended", f"lease Operating-mode {lease!r} (more unattended than the fleet file)"
    return canonical, note


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

    def lease_root(d: str, mode: str | None) -> str:
        root = Path(d) / "proj"
        (root / ".working").mkdir(parents=True)
        if mode is not None:
            (root / ".working" / "session-state.md").write_text(
                f"**Operating-mode:** {mode}\n", encoding="utf-8")
        return str(root)

    class T(unittest.TestCase):
        def test_exact_modes(self):
            self.assertTrue(decide("overnight-unattended")[0])
            self.assertTrue(decide("daytime-unattended")[0])
            self.assertTrue(decide("unattended")[0])
            for m in ("attended-autonomous", "fully-attended", "attended", "decisions", None,
                      "attended-not-unattended"):
                self.assertFalse(decide(m)[0], m)

        def test_stale_lease_incident(self):
            # 2026-09-25: fleet file unattended, lease still attended-autonomous -> block.
            with tempfile.TemporaryDirectory() as d:
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"unattended","set_by":"x"}', encoding="utf-8")
                root = lease_root(d, "attended-autonomous")
                self.assertTrue(decide(*read_mode(root, str(fleet)))[0])

        def test_unusable_fleet_file_fails_closed(self):
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, "attended-autonomous")
                fleet = Path(d) / "operating-mode"
                bodies = ['{"mode":"unattended"', '{"mode":"unattended","mode":"attended"}',
                          '{"mode":["unattended"]}', '{"set_by":"x"}', '{"mode":"bananas"}', "", "[]"]
                for body in bodies:
                    fleet.write_text(body, encoding="utf-8")
                    self.assertTrue(decide(*read_mode(root, str(fleet)))[0], body)
                fleet.write_bytes(b"\xff\xfe{")
                self.assertTrue(decide(*read_mode(root, str(fleet)))[0])
                fleet.unlink()
                fleet.mkdir()
                self.assertTrue(decide(*read_mode(root, str(fleet)))[0])
                fleet.rmdir()
                os.mkfifo(str(fleet))  # a FIFO must fail closed without blocking
                self.assertTrue(decide(*read_mode(root, str(fleet)))[0])
                fleet.unlink()
                os.symlink(str(Path(d) / "missing"), str(fleet))
                self.assertTrue(decide(*read_mode(root, str(fleet)))[0])
                if os.geteuid() != 0:  # an inaccessible parent directory fails closed
                    locked = Path(d) / "locked"
                    locked.mkdir()
                    (locked / "operating-mode").write_text('{"mode":"attended"}', encoding="utf-8")
                    locked.chmod(0)
                    try:
                        self.assertTrue(decide(*read_mode(root, str(locked / "operating-mode")))[0])
                    finally:
                        locked.chmod(0o700)
                # a bad project dir cannot undo a fleet-unattended block
                fleet.unlink()
                fleet.write_text('{"mode":"unattended"}', encoding="utf-8")
                self.assertTrue(decide(*read_mode("a\x00b", str(fleet)))[0])

        def test_bom_and_case_are_read(self):
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, "attended-autonomous")
                fleet = Path(d) / "operating-mode"
                fleet.write_text('\ufeff{"mode":" UNATTENDED "}', encoding="utf-8")
                self.assertEqual(read_mode(root, str(fleet))[0], "unattended")
                fleet.write_text('{"mode":"attended"}', encoding="utf-8")
                self.assertFalse(decide(*read_mode(root, str(fleet)))[0])

        def test_malformed_lease_and_oversized_fleet(self):
            with tempfile.TemporaryDirectory() as d:
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"attended"}', encoding="utf-8")
                with tempfile.TemporaryDirectory() as e:
                    for n, bad in enumerate(("daytime-unattended.", "unattended-overnight",
                                             "overnight_unattended")):
                        root = lease_root(os.path.join(e, str(n)), bad)
                        self.assertTrue(decide(*read_mode(root, str(fleet)))[0], bad)
                big = Path(d) / "big"
                big.write_bytes(b'{"mode":"attended"}'.ljust(_MAX_BYTES, b" ") + b"X")
                root = lease_root(os.path.join(d, "x"), "attended-autonomous")
                self.assertTrue(decide(*read_mode(root, str(big)))[0])  # oversized fails closed
                fifo_root = Path(d) / "fifo" / "proj"
                (fifo_root / ".working").mkdir(parents=True)
                os.mkfifo(str(fifo_root / ".working" / "session-state.md"))
                self.assertFalse(decide(*read_mode(str(fifo_root), str(fleet)))[0])  # no hang

        def test_timeout_swap_and_absent_fallback(self):
            with tempfile.TemporaryDirectory() as d:
                fleet = Path(d) / "operating-mode"
                fleet.write_text('{"mode":"attended"}', encoding="utf-8")
                root = lease_root(d, "daytime-unattended")
                self.assertTrue(decide(*read_mode(root, str(fleet)))[0])  # #5(b) swap blocks
                missing = str(Path(d) / "absent")
                self.assertTrue(decide(*read_mode(root, missing))[0])  # absent -> lease decides
            with tempfile.TemporaryDirectory() as d:
                root = lease_root(d, None)
                self.assertFalse(decide(*read_mode(root, str(Path(d) / "absent")))[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
