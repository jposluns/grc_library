#!/usr/bin/env python3
"""PreToolUse AskUserQuestion hook: block a blocking prompt in unattended mode.

Shipped 2026-07-17 (the Mistake-1 fix). Reads the PreToolUse JSON payload on stdin,
reads the ``Operating-mode`` field from ``.working/session-state.md``, and BLOCKS
(exit 2, reason on stderr) an ``AskUserQuestion`` call when the mode is unattended
(``overnight-unattended`` / ``daytime-unattended``). In unattended mode a maintainer
decision is recorded as pending and the run CONTINUES (no-idle-stop); a blocking prompt
idles the run until the maintainer returns. The recurrence that motivated it: an r4
deep-assessment Phase-8 sign-off was posed as an ``AskUserQuestion`` during overnight
mode and idled the run ~7 hours (with the work it was blocking already unblocked).
Attended modes (``fully-attended`` / ``attended-autonomous``) allow the call.

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


def read_mode(project_dir: str) -> str | None:
    ss = Path(project_dir) / ".working" / "session-state.md"
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
            f"AskUserQuestion BLOCKED: session Operating-mode is `{mode}` (unattended). "
            f"In unattended mode a maintainer decision is RECORDED as pending "
            f"(.working/pending-decisions.md or the relevant register) and the run CONTINUES "
            f"(no-idle-stop); a blocking prompt idles the run until the maintainer returns. "
            f"Record the decision, then proceed with the next authorized independent item using "
            f"graceful degradation (stricter-safe on a reversible action, defer-and-skip on an "
            f"authorial one). If the maintainer is in fact attended, update the Operating-mode "
            f"field in .working/session-state.md first, then re-issue the question."
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
        or "/home/jposluns/grc_library"
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

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
