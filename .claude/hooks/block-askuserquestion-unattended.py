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
Attended modes (``fully-attended`` / ``attended-autonomous``) allow the call.

Mode source (fixed 2026-09-25, maintainer-caught). The AUTHORITY is the fleet's canonical,
root-owned mode file ``/opt/orch-operator/operating-mode`` (JSON, its ``mode`` field), read
FIRST, and the lease's ``Operating-mode`` field (``session-state.md``) is also read: an
unattended reading from EITHER source blocks (stricter-is-safer; the lease can legitimately be
more unattended than the fleet file through the CLAUDE.md #5(b) timeout swap), and otherwise the
canonical mode decides, with the lease as the fallback when the canonical file is absent,
unreadable, or unparseable. Before the fix the hook read only the
lease, a hand-synced copy: the fleet went unattended at 2026-09-25T00:25:42Z while the lease
still said ``attended-autonomous``, and an AskUserQuestion passed. The test hook for the path
is ``GRC_OPERATOR_MODE_FILE`` (used by the self-test; not for normal operation).

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and
feeds stderr back to the model as the reason. Fail-OPEN on any parse/read failure or an
absent ``Operating-mode`` field: this is a guardrail against one known mistake shape, not
a security boundary, and a hook that blocked on a malformed payload would be worse than
the mistake it prevents. Defence-in-depth with the no-blocking-questions-unattended
discipline (CLAUDE.md / the assistant memory), not a substitute for it. NOTE: like the
sibling pipe-guard, this hook does not fire in a child session whose
``CLAUDE_PROJECT_DIR`` is unset (documented harness limitation); the discipline is the
primary control either way.

Self-test: ``python3 .claude/hooks/block-askuserquestion-unattended.py --self-test``.
"""

import json
import os
import re
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


def read_canonical_mode(path: str | None = None) -> str | None:
    """The fleet authority: the ``mode`` field of the root-owned JSON mode file, or None."""
    path = path or os.environ.get("GRC_OPERATOR_MODE_FILE") or CANONICAL_MODE_FILE
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None
    mode = data.get("mode") if isinstance(data, dict) else None
    return mode.strip().lower() if isinstance(mode, str) and mode.strip() else None


def read_mode(project_dir: str) -> str | None:
    """Stricter-is-safer across both sources: an unattended reading from EITHER the canonical
    fleet file or the lease wins (the lease can legitimately be MORE unattended, via the
    CLAUDE.md #5(b) timeout swap). Otherwise the canonical mode, then the lease."""
    canonical = read_canonical_mode()
    lease = read_lease_mode(project_dir)
    for mode in (canonical, lease):
        if mode and "unattended" in mode:
            return mode
    return canonical if canonical is not None else lease


def read_lease_mode(project_dir: str) -> str | None:
    ss = _working_file("session-state.md", Path(project_dir))
    if ss is None:
        return None  # fail-open: no session-state -> no mode -> allow (documented)
    try:
        text = ss.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = MODE_RE.search(text)
    return m.group(1).lower() if m else None


def decide(mode: str | None) -> tuple[bool, str]:
    """Return (block, reason). Block only when the mode is unattended."""
    if mode and "unattended" in mode:
        return True, (
            f"BLOCKED (askuserquestion-unattended): an AskUserQuestion while Operating-mode is "
            f"`{mode}` (unattended).\n"
            f"WHY: a blocking prompt idles the run until the maintainer returns; unattended mode "
            f"records a maintainer decision as pending and CONTINUES (no-idle-stop).\n"
            f"CONSIDER INSTEAD: record the decision (.working/pending-decisions.md or the relevant "
            f"register) and proceed on the next authorized independent item via graceful "
            f"degradation (stricter-safe on a reversible action, defer-and-skip on an authorial "
            f"one). Only the operator ends unattended mode: the fleet mode file "
            f"({CANONICAL_MODE_FILE}) is operator-set, and an assistant never edits it; when the "
            f"operator has set an attended mode there, sync the lease Operating-mode field to it."
        )
    return False, ""


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    workspace = payload.get("workspace") or {}
    project_dir = (
        workspace.get("project_dir")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        # Last-resort fallback: resolve the project root from this hook's own location
        # (<project>/.claude/hooks/this.py -> parents[2]). No hardcoded path, so it stays
        # correct across a repo move (for example an /old/root -> /new/root relocation).
        or str(Path(__file__).resolve().parents[2])
    )
    block, reason = decide(read_mode(project_dir))
    if block:
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def test_overnight_blocks(self):
            self.assertTrue(decide("overnight-unattended")[0])

        def test_daytime_unattended_blocks(self):
            self.assertTrue(decide("daytime-unattended")[0])

        def test_attended_allows(self):
            self.assertFalse(decide("attended-autonomous")[0])
            self.assertFalse(decide("fully-attended")[0])

        def test_absent_allows(self):
            self.assertFalse(decide(None)[0])

        def test_canonical_file_wins_over_a_stale_lease(self):
            # The 2026-09-25 shape: the fleet file says unattended, the lease still says
            # attended-autonomous. The canonical file must decide.
            import tempfile
            with tempfile.TemporaryDirectory() as d:
                root = Path(d)
                (root / ".working").mkdir()
                (root / ".working" / "session-state.md").write_text(
                    "**Operating-mode:** attended-autonomous\n", encoding="utf-8")
                fleet = root / "operating-mode"
                fleet.write_text('{"mode":"unattended","set_by":"x"}', encoding="utf-8")
                old = os.environ.get("GRC_OPERATOR_MODE_FILE")
                os.environ["GRC_OPERATOR_MODE_FILE"] = str(fleet)
                try:
                    self.assertEqual(read_mode(str(root)), "unattended")
                    self.assertTrue(decide(read_mode(str(root)))[0])
                    fleet.write_text('{"mode":"attended"}', encoding="utf-8")
                    (root / ".working" / "session-state.md").write_text(
                        "**Operating-mode:** daytime-unattended\n", encoding="utf-8")
                    self.assertTrue(decide(read_mode(str(root)))[0])  # #5(b) swap still blocks
                    (root / ".working" / "session-state.md").write_text(
                        "**Operating-mode:** attended-autonomous\n", encoding="utf-8")
                    self.assertEqual(read_mode(str(root)), "attended")  # canonical decides
                    fleet.write_text("not json", encoding="utf-8")  # unparseable -> lease
                    self.assertEqual(read_mode(str(root)), "attended-autonomous")
                    os.environ["GRC_OPERATOR_MODE_FILE"] = str(root / "missing")  # absent -> lease
                    self.assertEqual(read_mode(str(root)), "attended-autonomous")
                finally:
                    if old is None:
                        os.environ.pop("GRC_OPERATOR_MODE_FILE", None)
                    else:
                        os.environ["GRC_OPERATOR_MODE_FILE"] = old

        def test_canonical_attended_allows(self):
            import tempfile
            with tempfile.TemporaryDirectory() as d:
                f = Path(d) / "operating-mode"
                f.write_text('{"mode":"attended"}', encoding="utf-8")
                self.assertEqual(read_canonical_mode(str(f)), "attended")
                self.assertFalse(decide("attended")[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
