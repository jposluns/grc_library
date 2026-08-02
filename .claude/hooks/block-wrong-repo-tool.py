#!/usr/bin/env python3
"""PreToolUse Bash hook: block a command whose target repo depends on the ambient cwd.

Shipped 2026-07-19 (TODO §1.22.1) after the orchestrator ran ``python3
tools/credit-offload-queue.py`` from the ``grc_library`` cwd, but that helper lives in the
``grc_library_scratch`` sibling repo, so the command failed with a file-not-found. WIDENED
2026-07-24 (maintainer-directed) after the mirror failure: a ``grc_library`` tool
(``build-taxonomy.py``, ``preflight-changelog.py``) run from a DRIFTED ``scratch`` cwd, and a
near-miss ``git add -A`` staged against the wrong repo. Tools live in BOTH ``grc_library/tools/``
and the sibling repos' ``tools/`` dirs, and ``python3 tools/<x>`` and bare ``git`` are both
cwd-relative, so the same command means different things depending on the ambient working
directory. The original hook caught only the sibling-mismatch case (a tool absent from the
project repo). WIDENED 2026-07-24 (maintainer-directed, then SOFTENED after review) to ALSO
catch the silent-danger case: a repo-mutating bare ``git`` acting on whatever repo the ambient
cwd happens to be. The ``tools/<x>`` half is deliberately kept SIBLING-ONLY (a project tool run
cwd-relative is ALLOWED) so the guard does not contradict the project's own documented
``tools/<x>`` commands; a project tool's cwd-drift fails loud (file-not-found) and is covered by
the absolute-path convention, whereas a wrong-repo ``git`` commit is silent.

What it does: reads the PreToolUse JSON payload on stdin, inspects ``tool_input.command``, and
BLOCKS (exit 2) any of THREE cwd-dependent shapes, printing the copy-paste fix:
  (0) a cd-prefixed cwd-relative repo tool NOT in ``CWD_GUARD_ALLOWLIST`` where the ``cd``
      PRECEDES the tool (P-1.19): the directive is ABSOLUTE PATHS BY DEFAULT, so the absolute
      form is the default. (A ``tool``-then-``cd``, with the cd AFTER the tool, is NOT this shape.)
  (1) a cwd-relative ``tools/<name>.(py|sh)`` invoked AT COMMAND POSITION that is NOT a project
      tool but DOES exist in a SIBLING repo (``_INVOKE`` matches only the cwd-relative form, not
      an absolute ``/path/tools/x``), when the command has no explicit ``cd``. A PROJECT tool run
      cwd-relative is ALLOWED. The message names the sibling repo and the absolute form.
  (2) a repo-MUTATING bare ``git`` subcommand (add/commit/push/reset/checkout/switch/merge/
      rebase/stash/rm/mv/clean/apply/restore/cherry-pick/revert) without ``-C <path>`` and
      without a ``cd`` (a wrong-repo commit is silent, hence kept in scope).
Everything else is ALLOWED:
  - a ``cd `` with NO cd-preceded non-allowlist repo tool (a bare ls, a git, a cwd-guard
    tool, or a tool-then-cd);
  - a cwd-relative PROJECT tool with no preceding cd (softened scope: the documented
    ``tools/x`` commands stay valid);
  - an ABSOLUTE tool path (``python3 /home/grc/grc_library/tools/foo.py``);
  - a ``git -C <path> ...`` command (explicit target repo);
  - read-only git (``status``/``log``/``diff``/``show`` are not in the mutating set);
  - a filename mentioned as an argument (``grep -n x tools/foo.py``) (not invoked).
KNOWN RESIDUALS (accepted; fail-open nudge, not a shell parser): a QUOTED cwd-relative path
  and exotic cd syntax (an ``if cd``/``command cd`` prefix) slip the regexes; this guard
  catches the common cd-then-tool shape only (codex QA, P-1.19).

A false block just tells the orchestrator to use an absolute path or ``git -C``, the intended
discipline. Complements ``tools/repo-guard.sh`` (the write-mutation cross-repo guard, §1.15a)
on the READ side.

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

# (P-1.19) Tools for which a `cd <repo> && tools/<x>` is ALLOWED, the narrow cwd-guard
# exception to the absolute-paths-by-default directive. NOTE (2026-08-02): empirically these
# both ``os.chdir(ROOT)`` (ROOT from ``__file__``) or use absolute internal paths, so an
# ABSOLUTE invocation works for them too and the list could shrink to empty; it is kept per
# the maintainer's stated design as the documented cwd-guard set.
CWD_GUARD_ALLOWLIST = frozenset({"validate.py", "credit-offload-queue.py"})

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

# A repo-MUTATING `git` subcommand invoked at COMMAND POSITION without an explicit `-C
# <path>`. Such a command acts on whatever repo the ambient cwd happens to be, which is the
# `git add -A`-in-the-wrong-repo near-miss (2026-07-24). `git -C <path> ...` is exempt (the
# `(?!-C\b)` lookahead); read-only git (status/log/diff/show) is NOT matched (not mutating).
_GIT_MUTATE = re.compile(
    r"(?:^|[;&\n(]\s*|&&\s*|\|\|?\s*|\{\s+)"
    r"(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
    r"(?:timeout\s+[\w.]+\s+|env\s+)?"
    r"git\s+(?!-C\b)(?:-c\s+\S+\s+|--\S+\s+)*"
    r"(?:add|commit|push|reset|checkout|switch|merge|rebase|stash|rm|mv|clean|apply|restore"
    r"|cherry-pick|revert)\b",
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
    proj = Path(project_dir).resolve()
    project_name = proj.name
    parent = proj.parent
    roots = _sibling_roots(project_dir)
    project_tools = roots.get(project_name) if roots else None
    invoked = list(dict.fromkeys(_INVOKE.findall(command)))
    has_cd = bool(re.search(r"(?:^|[;&\n(]|&&|\|\|)\s*cd\s", command))

    def _tool_repo(tool: str):
        # the repo whose tools/ holds this cwd-relative tool (project first, then a sibling)
        if project_tools is not None and (project_tools / tool).is_file():
            return project_name
        for n, td in roots.items():
            if n != project_name and (td / tool).is_file():
                return n
        return None

    # (0, P-1.19) A `cd <repo> && tools/<x>` prefix for a repo tool NOT in the cwd-guard
    # allow-list: the maintainer directive is ABSOLUTE PATHS BY DEFAULT
    # (grc_library_private/INDEX.md), so the absolute form is the default and cd is reserved
    # for a genuine cwd-guard tool. A cd with no repo-tool invocation (`cd x && ls`,
    # `cd x && git ...`) or only allow-listed tools stays allowed (the prior deliberate-cd
    # behaviour). This closes the cd-escape that let the absolute-path convention be bypassed.
    # (0, P-1.19) Flag a repo tool NOT in CWD_GUARD_ALLOWLIST only when a `cd ` command-position
    # token PRECEDES it (the tool then runs via the cd'd cwd); a `tool && cd elsewhere` (cd AFTER
    # the tool) is NOT flagged (codex QA fixed the whole-command false positive). The directive is
    # ABSOLUTE PATHS BY DEFAULT (grc_library_private/INDEX.md); cd is reserved for a genuine
    # cwd-guard tool. A cd with no cd-preceded flagged tool (a bare ls, a git, an allow-listed
    # tool, or a tool-then-cd) stays allowed. KNOWN RESIDUALS (accepted; fail-open nudge, not a
    # shell parser): a QUOTED cwd-relative path and exotic cd syntax slip the regexes.
    cd_pos = [m.start() for m in re.finditer(r"(?:^|[;&\n(]|&&|\|\|)\s*cd\s", command)]
    flagged = []
    for m in _INVOKE.finditer(command):
        t = m.group(1)
        if t in CWD_GUARD_ALLOWLIST or _tool_repo(t) is None:
            continue
        if any(cp < m.start() for cp in cd_pos):
            flagged.append((t, _tool_repo(t)))
    flagged = list(dict.fromkeys(flagged))
    if flagged:
        lines = [f"  - `tools/{t}`: use `python3 {parent}/{repo}/tools/{t} ...` "
                 f"(absolute), not a cd-prefixed cwd-relative invocation."
                 for t, repo in flagged]
        reason = (
            "BLOCKED (absolute-path guardrail, P-1.19): the standing directive is "
            "ABSOLUTE PATHS BY DEFAULT (grc_library_private/INDEX.md); a cd-prefixed "
            "cwd-relative repo tool runs via the ambient cwd instead of an absolute path. "
            "Use the absolute form:\n" + "\n".join(lines)
            + "\n(cd is reserved for a genuine cwd-guard tool: "
            + ", ".join(sorted(CWD_GUARD_ALLOWLIST)) + ".)")
        return True, reason
    if has_cd:
        return False, ""  # deliberate cd, no cd-preceded flagged tool: allowed

    # (1) A cwd-relative `tools/<x>` that is NOT a project tool but DOES exist in a sibling
    # repo: it would fail file-not-found from the project cwd (the 2026-07-19
    # credit-offload-queue slip). SOFTENED SCOPE (maintainer-directed 2026-07-24): a PROJECT
    # tool run cwd-relative is ALLOWED, because blocking it would contradict the project's
    # own documented `tools/<x>` commands, and its cwd-drift failure is loud (file-not-found)
    # and covered by the absolute-path convention. A tool absent from every repo is allowed
    # (new tool / typo). `_INVOKE` matches only the cwd-relative form, so an absolute path is
    # never a hit.
    if invoked and roots:
        hits = []
        for tool in invoked:
            if project_tools is not None and (project_tools / tool).is_file():
                continue  # project tool run cwd-relative: allowed under the softened scope
            elsewhere = [n for n, td in roots.items()
                         if n != project_name and (td / tool).is_file()]
            if elsewhere:
                hits.append((tool, elsewhere[0]))
        if hits:
            lines = [
                f"  - `tools/{tool}` lives in `{where}`, NOT `{project_name}`; run it "
                f"cwd-independently: `python3 {parent}/{where}/tools/{tool} ...` (or "
                f"`cd {parent}/{where} && python3 tools/{tool} ...`)."
                for tool, where in hits
            ]
            reason = (
                "BLOCKED (wrong-repo guardrail): a cwd-relative `tools/<x>` that is NOT in "
                f"`{project_name}` but lives in a sibling repo would fail file-not-found from "
                "this cwd (the credit-offload-queue-from-the-wrong-repo slip). Use an absolute "
                "path (or an explicit `cd <repo> &&`):\n" + "\n".join(lines))
            return True, reason

    # (2) A repo-MUTATING bare `git` (no `-C <path>`, no `cd`): it stages/commits/pushes
    # against whatever repo the ambient cwd happens to be (the `git add -A`-in-the-wrong-repo
    # near-miss). This half is KEPT under the softened scope because a wrong-repo commit is
    # SILENT, unlike a tool's loud file-not-found. Read-only git (status/log/diff/show) is
    # not in the mutating set, and `git -C <path>` is exempt via the regex lookahead.
    if _GIT_MUTATE.search(command):
        reason = (
            "BLOCKED (repo-target guardrail): a repo-mutating `git` command without `-C <path>` "
            "acts on whatever repo the ambient cwd is, risking a stage/commit/push against the "
            "WRONG repo (the 2026-07-24 `git add -A`-in-scratch near-miss). Use "
            "`git -C <absolute-repo-path> <subcommand> ...`, or an explicit `cd <repo-root> &&`.")
        return True, reason
    return False, ""


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
        # A structurally-malformed payload (non-dict, or tool_input not a dict) must fail-OPEN,
        # not traceback: the extraction is INSIDE the try (codex QA, P-1.19).
        command = (payload.get("tool_input") or {}).get("command", "")
        workspace = payload.get("workspace") or {}
        project_dir = (
            workspace.get("project_dir")
            or os.environ.get("CLAUDE_PROJECT_DIR")
            # Last-resort fallback: resolve the project root from this hook's own location
            # (<project>/.claude/hooks/this.py -> parents[2]). No hardcoded path, so it stays
            # correct across a repo move (for example /home/jposluns -> /home/grc).
            or str(Path(__file__).resolve().parents[2])
        )
        block, reason = decide(command, project_dir)
    except Exception:
        return 0  # fail-open (malformed payload, non-dict, or decide error)
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
            (scratch / "tools" / "validate.py").write_text("")
            self.pd = str(self.proj)

        def test_sibling_tool_no_cd_blocks(self):
            block, reason = decide(
                "python3 tools/credit-offload-queue.py list-workers", self.pd)
            self.assertTrue(block)
            self.assertIn("grc_library_scratch", reason)

        def test_project_tool_cwd_relative_allowed(self):
            # softened scope (maintainer-directed 2026-07-24): a PROJECT tool run
            # cwd-relative is ALLOWED (blocking it would contradict the documented
            # commands; its cwd-drift failure is loud file-not-found, not silent)
            block, _ = decide("bash tools/run_all_audits.sh", self.pd)
            self.assertFalse(block)

        def test_absolute_path_allowed(self):
            block, _ = decide(f"python3 {self.proj}/tools/run_all_audits.sh", self.pd)
            self.assertFalse(block)

        def test_explicit_cd_allowed(self):
            block, _ = decide(
                "cd ../grc_library_scratch && python3 tools/credit-offload-queue.py "
                "list-workers", self.pd)
            self.assertFalse(block)

        def test_cd_nonallowlist_tool_blocks(self):
            # P-1.19: cd + a repo tool NOT in the cwd-guard allow-list is flagged toward
            # the absolute form (the maintainer absolute-paths-by-default directive).
            block, reason = decide(
                "cd ../grc_library && bash tools/run_all_audits.sh", self.pd)
            self.assertTrue(block)
            self.assertIn("absolute-path guardrail", reason)

        def test_cd_allowlist_tool_allowed(self):
            # P-1.19: cd + a cwd-guard allow-list tool stays allowed.
            block, _ = decide(
                "cd ../grc_library_scratch && python3 tools/validate.py", self.pd)
            self.assertFalse(block)

        def test_cd_git_allowed(self):
            # P-1.19: cd + git (no repo tool invoked) stays allowed (deliberate cd for git).
            block, _ = decide("cd ../grc_library && git commit -m x", self.pd)
            self.assertFalse(block)

        def test_cd_no_repo_tool_allowed(self):
            # P-1.19: cd + a non-repo-tool command stays allowed.
            block, _ = decide("cd /tmp && ls -la", self.pd)
            self.assertFalse(block)

        def test_cd_after_tool_allowed(self):
            # P-1.19 (codex QA): a tool-then-cd (cd AFTER the tool) is NOT flagged;
            # only cd-before-tool is the absolute-path shape.
            block, _ = decide("python3 tools/run_all_audits.sh && cd /tmp", self.pd)
            self.assertFalse(block)

        def test_unknown_cwd_relative_tool_allowed(self):
            # a tool absent from every repo (a new tool being created, or a typo) is allowed
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

        def test_compound_second_segment_blocks(self):
            block, _ = decide(
                "echo hi && python3 tools/credit-offload-queue.py", self.pd)
            self.assertTrue(block)

        def test_git_mutate_bare_blocks(self):
            self.assertTrue(decide("git add -A", self.pd)[0])
            self.assertTrue(decide("git commit -m x", self.pd)[0])
            self.assertTrue(decide("echo hi && git push origin HEAD:main", self.pd)[0])
            self.assertTrue(decide("git cherry-pick abc123", self.pd)[0])
            self.assertTrue(decide("git revert HEAD", self.pd)[0])

        def test_git_dash_C_allowed(self):
            self.assertFalse(decide("git -C /home/x/grc_library commit -m y", self.pd)[0])
            self.assertFalse(decide("git -C /home/x/grc_library add -A", self.pd)[0])

        def test_git_readonly_allowed(self):
            self.assertFalse(decide("git status --short", self.pd)[0])
            self.assertFalse(decide("git log --oneline -5", self.pd)[0])
            self.assertFalse(decide("git diff HEAD", self.pd)[0])

        def test_git_mutate_with_cd_allowed(self):
            self.assertFalse(
                decide("cd /home/x/grc_library && git commit -m y", self.pd)[0])

        def test_empty_command_allowed(self):
            self.assertFalse(decide("", self.pd)[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
