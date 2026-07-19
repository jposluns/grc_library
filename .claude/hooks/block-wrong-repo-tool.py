#!/usr/bin/env python3
"""PreToolUse Bash hook: block a cwd-relative tool invocation aimed at the wrong repo.

Shipped 2026-07-19 (TODO §1.22.1) after the orchestrator ran ``python3
tools/credit-offload-queue.py`` from the ``grc_library`` cwd, but that helper lives in the
``grc_library_scratch`` sibling repo, so the command failed with a file-not-found the
orchestrator could have skimmed past. Tools live in BOTH ``grc_library/tools/`` and the
sibling repos' ``tools/`` dirs (``grc_library_scratch``, ``grc_library_ref``), and
``python3 tools/<x>`` is cwd-relative, so the same relative path means different things in
different repos. This hook turns the silent wrong-repo miss into a loud, corrective block.

What it does: reads the PreToolUse JSON payload on stdin, inspects ``tool_input.command``,
and for each ``tools/<name>.(py|sh)`` invoked AT COMMAND POSITION (not merely mentioned as
an argument), checks whether that file exists in the project repo's ``tools/`` dir. If it
does NOT exist there but DOES exist in a sibling repo's ``tools/`` dir, it BLOCKS (exit 2)
and names the correct repo. Everything else is allowed:
  - a command that contains an explicit ``cd `` is ALLOWED unhandled (the author is managing
    cwd deliberately, e.g. ``cd ../grc_library_scratch && python3 tools/foo.py`` is correct);
  - a tool that exists in the project repo is allowed (the normal case);
  - a tool absent from EVERY repo is allowed (a new tool being created, or a typo, is not
    this hook's concern);
  - a filename mentioned as an argument (``grep -n x tools/foo.py``) is allowed (not invoked).

Over-matching is deliberately toward ALLOWING (a false block just tells the orchestrator to
add a ``cd``, which is harmless; a false allow reintroduces the silent wrong-repo miss the
hook exists to catch, but bash's own file-not-found is the backstop there). Complements
``tools/repo-guard.sh`` (the write-mutation cross-repo guard, §1.15a) on the READ side.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason. Fail-OPEN on any parse/read failure: this is a
guardrail against one mistake shape, not a security boundary. NOTE: like the sibling guards,
this hook does not fire in a child session whose ``CLAUDE_PROJECT_DIR`` is unset (documented
harness limitation); the ``## Boundaries`` cross-repo convention and the unpiped-verification
habit are the primary controls either way.

Self-test: ``python3 .claude/hooks/block-wrong-repo-tool.py --self-test``.
"""

import json
import os
import re
import sys
from pathlib import Path

# The colocated repos whose tools/ dirs share the cwd-relative `tools/<x>` shape.
SIBLING_REPO_NAMES = (
    "grc_library",
    "grc_library_scratch",
    "grc_library_ref",
    "grc_library_private",
)

# A `tools/<name>.(py|sh)` token invoked at COMMAND POSITION: at command start, or after
# ; && || | & newline ( {, optionally preceded by env assignments, timeout/env, an
# interpreter (python3 [-m] / bash / sh), and a `./` prefix. This distinguishes EXECUTING
# `python3 tools/foo.py` from MENTIONING `grep x tools/foo.py` (an argument).
_INVOKE = re.compile(
    r"(?:^|[;&\n(]\s*|&&\s*|\|\|?\s*|\{\s+)"
    r"(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
    r"(?:timeout\s+[\w.]+\s+|env\s+)?"
    r"(?:python3?\s+(?:-m\s+)?|bash\s+|sh\s+)?"
    r"(?:\./)?tools/([A-Za-z0-9_.-]+\.(?:py|sh))\b",
    re.MULTILINE,
)


def _sibling_roots(project_dir: str) -> dict:
    """Map repo-name -> tools/ Path for each colocated repo that exists."""
    parent = Path(project_dir).resolve().parent
    roots = {}
    for name in SIBLING_REPO_NAMES:
        tdir = parent / name / "tools"
        if tdir.is_dir():
            roots[name] = tdir
    return roots


def decide(command: str, project_dir: str) -> tuple[bool, str]:
    if not isinstance(command, str) or not command.strip():
        return False, ""
    # An explicit `cd ` anywhere means the author is managing cwd deliberately; do not
    # second-guess it (the correct cross-repo pattern is `cd <repo> && tools/<x>`).
    if re.search(r"(?:^|[;&\n(]|&&|\|\|)\s*cd\s", command):
        return False, ""
    invoked = _INVOKE.findall(command)
    if not invoked:
        return False, ""
    roots = _sibling_roots(project_dir)
    if not roots:
        return False, ""  # fail-open: cannot locate any repo tools/ dir (adopter, etc.)
    project_name = Path(project_dir).resolve().name
    project_tools = roots.get(project_name)
    hits = []
    for tool in dict.fromkeys(invoked):  # dedup, order-preserving
        # present in the project repo -> the normal case, fine
        if project_tools is not None and (project_tools / tool).is_file():
            continue
        # absent locally: where does it live?
        elsewhere = [n for n, td in roots.items()
                     if n != project_name and (td / tool).is_file()]
        if elsewhere:
            hits.append((tool, elsewhere))
        # absent everywhere -> allow (new tool / typo, not this hook's concern)
    if not hits:
        return False, ""
    lines = []
    for tool, elsewhere in hits:
        where = " or ".join(elsewhere)
        lines.append(
            f"  - `tools/{tool}` is NOT in `{project_name}/tools/`; it lives in "
            f"`{where}`. Run it from there: `cd ../{elsewhere[0]} && python3 tools/{tool} ...` "
            f"(or use an absolute path)."
        )
    reason = (
        "BLOCKED (wrong-repo guardrail): this command invokes a cwd-relative `tools/<x>` "
        "that does not exist in the project repo but DOES exist in a sibling repo, so it "
        "would fail with a file-not-found from the wrong cwd (the 2026-07-19 "
        "`credit-offload-queue.py`-from-`grc_library` slip this guard exists to catch):\n"
        + "\n".join(lines)
        + "\nIf you genuinely intend the sibling repo, prefix the command with "
        "`cd ../<repo> &&` (which this hook then allows)."
    )
    return True, reason


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    command = (payload.get("tool_input") or {}).get("command", "")
    workspace = payload.get("workspace") or {}
    project_dir = (
        workspace.get("project_dir")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or "/home/jposluns/grc_library"
    )
    try:
        block, reason = decide(command, project_dir)
    except Exception:
        return 0  # fail-open
    if block:
        try:
            from _hook_state import record_block
            record_block(command, "wrong-repo")
        except Exception:
            pass
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    class T(unittest.TestCase):
        def setUp(self):
            # build a fake colocation: <parent>/{grc_library,grc_library_scratch}/tools/
            self.parent = tempfile.mkdtemp()
            self.proj = Path(self.parent) / "grc_library"
            (self.proj / "tools").mkdir(parents=True)
            (self.proj / "tools" / "run_all_audits.sh").write_text("")
            (self.proj / "tools" / "lint_common.py").write_text("")
            scratch = Path(self.parent) / "grc_library_scratch"
            (scratch / "tools").mkdir(parents=True)
            (scratch / "tools" / "credit-offload-queue.py").write_text("")
            self.pd = str(self.proj)

        def test_wrong_repo_blocks(self):
            block, reason = decide(
                "python3 tools/credit-offload-queue.py list-workers", self.pd)
            self.assertTrue(block)
            self.assertIn("grc_library_scratch", reason)

        def test_local_tool_allowed(self):
            block, _ = decide("bash tools/run_all_audits.sh", self.pd)
            self.assertFalse(block)

        def test_explicit_cd_allowed(self):
            block, _ = decide(
                "cd ../grc_library_scratch && python3 tools/credit-offload-queue.py "
                "list-workers", self.pd)
            self.assertFalse(block)

        def test_unknown_tool_allowed(self):
            # a brand-new tool being created exists nowhere -> allow
            block, _ = decide("python3 tools/brand-new-thing.py", self.pd)
            self.assertFalse(block)

        def test_mention_as_argument_allowed(self):
            # the scratch tool named as a grep argument, not invoked -> allow
            block, _ = decide(
                "grep -n queue tools/credit-offload-queue.py", self.pd)
            self.assertFalse(block)

        def test_dot_slash_invocation_blocks(self):
            block, _ = decide("./tools/credit-offload-queue.py", self.pd)
            self.assertTrue(block)

        def test_compound_second_segment(self):
            block, _ = decide(
                "echo hi && python3 tools/credit-offload-queue.py", self.pd)
            self.assertTrue(block)

        def test_empty_command_allowed(self):
            self.assertFalse(decide("", self.pd)[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
