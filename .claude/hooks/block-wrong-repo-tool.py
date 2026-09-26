#!/usr/bin/env python3
"""PreToolUse Bash hook: block selected textual patterns for cwd-relative repo operations.

Shipped 2026-07-19 (1.22.1 (closing PR #1042)) after the orchestrator ran ``python3
tools/credit-offload-queue.py`` from the ``grc_library`` cwd, but that helper lives in the
``grc_library_scratch`` sibling repo, so the command failed with a file-not-found. WIDENED
2026-07-24 (maintainer-directed) after the mirror failure: a ``grc_library`` tool
(``build-taxonomy.py``, ``preflight-changelog.py``) run from a DRIFTED ``scratch`` cwd, and a
near-miss ``git add -A`` staged against the wrong repo. Tools live in BOTH ``grc_library/tools/``
and the sibling repos' ``tools/`` dirs, and ``python3 tools/<x>`` and bare ``git`` are both
cwd-relative, so the same command means different things depending on the ambient working
directory. The original hook caught only the sibling-mismatch case (a tool absent from the
project repo). WIDENED 2026-07-24 (maintainer-directed, then SOFTENED after review) to ALSO
catch selected bare ``git`` subcommands that can mutate the wrong repo without necessarily
failing. The sibling-mismatch check permits a tool found in the scanned project tools
directory; the later P-1.19 absolute-path check also covers project tools preceded textually
by a matched ``cd``. Running a project tool from another cwd can fail file-not-found, but
can also resolve a different file with the same relative path.

What it does: reads the PreToolUse JSON payload on stdin, applies ``strip_heredocs`` to
``tool_input.command``, then checks THREE patterns in order. A block exits 2 and prints
suggestion templates. These are regex and filesystem checks, not shell execution analysis:
  (0) an ``_INVOKE`` tool match whose captured filename is outside ``CWD_GUARD_ALLOWLIST``
      and passes ``is_file()`` in a scanned repo's tools directory, with a matched ``cd``
      starting earlier in the command text. This does not establish that the cd executes,
      succeeds, selects that repo, or changes the tool's cwd.
  (1) if there is NO matched ``cd`` anywhere, an ``_INVOKE`` filename with no project-file
      match but an ``is_file()`` match in another scanned repo's tools directory.
  (2) if neither tool check blocks and there is NO matched ``cd`` anywhere, an
      ``_GIT_MUTATE`` match for add/commit/push/reset/checkout/switch/merge/rebase/stash/
      rm/mv/clean/apply/restore/cherry-pick/revert. Each listed name matches only where it
      ends at a word boundary, so a longer subcommand whose listed prefix ends at a boundary
      (``git commit-graph``, but not ``git commitment``) also matches; the set includes
      read-only uses such as ``git stash list`` and omits a subcommand sharing no listed
      prefix such as ``git tag``. Arguments are not checked for mutation or the actual target repo.

Scanning is limited to existing tools directories under the configured
``SIBLING_REPO_NAMES`` beside the resolved project directory. An unlisted project name has
no project tools entry in this scan, except that the project directory's own ``tools/`` always
counts (a linked-worktree session, 3b85). For the absolute-path suggestion, the last ``cd``
before the tool wins when its operand is an absolute directory holding ``tools/<name>`` (a
linked worktree's own copy, 3b85); otherwise a project-file match wins, then the first
matching configured repo. The operand is read textually (one enclosing quote pair removed,
no variable or ``~`` expansion, a bare ``cd`` has none), so a relative or option-prefixed
operand (``cd ../wt``, ``cd -P /x``) and a cd inside a subshell are residue: the suggestion
then falls back or names a tree the tool will not run in. The path is shell-quoted. The
sibling suggestion
uses the first matching other repo. Neither choice establishes the intended target.

After check (0), ANY matched ``cd`` allows the whole command, even a cd after a sibling
tool or Git command. Without such a cd, a project-file match skips only that tool in check
(1); another tool or Git match can still block. An absolute tool path, the plain argument
example ``grep -n x tools/foo.py``, ``git -C <path> ...``, and
``git status``/``log``/``diff``/``show`` do not themselves match the corresponding regexes.

KNOWN RESIDUALS: the regexes approximate command position and do not parse shell quoting,
comments, execution order, or scope. They can match command-like text inside arguments,
miss quoted tool paths and unsupported prefixes, and capture a filename prefix because
the tool pattern ends at a word boundary rather than a shell-token boundary. The cd
pattern misses forms such as ``if cd``, ``command cd``, and ``{ cd``; an unrecognized cd
does not provide the whole-command exemption.

Suggestions are templates, not verified copy-paste fixes: both tool-message generators
use ``python3`` even for ``.sh`` files, and an absolute script path does not establish the
script's internal cwd independence. The sibling message also supplies a cd alternative;
that alternative can trigger check (0) when the filename is outside the allowlist.

Complements ``tools/repo-guard.sh`` (the write-mutation cross-repo guard, 1.15a (closing PR #1013))
by checking selected repo-target command patterns, including potentially mutating Git uses.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason. Exceptions inside main's payload-parsing,
heredoc-filtering, project-root-selection, and decision try block return 0. This is a
guardrail for selected command patterns, not a security boundary.
Once launched, main selects the project root from ``workspace.project_dir``, then
``CLAUDE_PROJECT_DIR``, then this hook's resolved location. An unset environment variable
does not disable main. Separately, the configured launcher in ``.claude/settings.json``
uses ``CLAUDE_PROJECT_DIR`` to locate the script, so an unset value can prevent launch
before that fallback is reached. The ``## Boundaries`` cross-repo convention and the
unpiped-verification habit remain primary controls.

Self-test: ``python3 .claude/hooks/block-wrong-repo-tool.py --self-test``.
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

# Fixed colocated directory names checked for tools/; Git repository status is not verified.
SIBLING_REPO_NAMES = (
    "grc_library",
    "grc_library_scratch",
    "grc_library_ref",
    "grc_library_private",
)

# (P-1.19) Filename exemptions from check (0), the cd-before-tool absolute-path check.
# Membership alone grants the exemption; this hook does not verify cwd-guard behaviour
# or internal path handling. These names can still trigger the sibling check when no cd
# is matched. The allowlist does not exempt unrelated non-allowlisted tool matches.
CWD_GUARD_ALLOWLIST = frozenset({"validate.py", "credit-offload-queue.py"})

# Approximate command-position matching for an unquoted [./]tools/<name>.(py|sh) prefix.
# With MULTILINE, ^ matches a line start without consuming indentation; other alternatives
# accept ; & newline ( && | || plus optional whitespace, or { plus required whitespace.
# Prefixes are ordered: zero or more NAME=\S* assignments, at most one timeout [\w.]+
# or plain env wrapper, then optional python/python3 with optional -m, or bash/sh.
# Assignments after env, wrapper options, and other interpreter options are not handled.
# The final \b is a word boundary, not a shell-token boundary: tools/foo.py.bak can
# capture foo.py. The plain grep argument example is excluded, but quoting, comments,
# and shell execution are not parsed, so command-like argument text can still match.
_INVOKE = re.compile(
    r"(?:^|[;&\n(]\s*|&&\s*|\|\|?\s*|\{\s+)"
    r"(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
    r"(?:timeout\s+[\w.]+\s+|env\s+)?"
    r"(?:python3?\s+(?:-m\s+)?|bash\s+|sh\s+)?"
    r"(?:\./)?tools/([A-Za-z0-9_.-]+\.(?:py|sh))\b",
    re.MULTILINE,
)

# Approximate command-position matching for literal git and the fixed subcommand set below,
# using the same boundary, assignment, and timeout/env prefixes as _INVOKE.
# Before the subcommand, accept repeated -c plus one nonspace token, or --nonspace tokens.
# The (?!-C\b) lookahead rejects -C only immediately after git's whitespace; a standalone
# -C <path> in option position is not consumed (it is neither -c nor --), but a -C token
# supplied as the value after -c IS consumed by -c\s+\S+ (e.g. the malformed git -c -C commit).
# The alternation matches a listed NAME only where it ends at a word boundary, so a longer
# subcommand whose listed prefix ends at a boundary also matches (git commit-graph,
# git checkout-index, but not git commitment); one sharing no listed prefix (git tag) and
# status/log/diff/show do not. Arguments are not inspected, so git stash list matches. The
# final \b is not a shell-token boundary.
# Matching does not establish mutation or the target repo: accepted assignments and long
# options can specify another target, for example GIT_DIR=... or --git-dir=....
_GIT_MUTATE = re.compile(
    r"(?:^|[;&\n(]\s*|&&\s*|\|\|?\s*|\{\s+)"
    r"(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
    r"(?:timeout\s+[\w.]+\s+|env\s+)?"
    r"git\s+(?!-C\b)(?:-c\s+\S+\s+|--\S+\s+)*"
    r"(?:add|commit|push|reset|checkout|switch|merge|rebase|stash|rm|mv|clean|apply|restore"
    r"|cherry-pick|revert)\b",
    re.MULTILINE,
)



# Heredoc handling lives in the shared _hookutil helper. The first local copy here stripped
# interpreter bodies (hiding real commands inside a shell heredoc, finding H7 of the PR #1441
# review) and swallowed the whole remainder on an unterminated introducer (H8, a universal
# bypass). One implementation, one fixture set, shared with block-bulk-git-add.py.
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from _hookutil import strip_heredocs  # noqa: E402


def _sibling_roots(project_dir: str) -> dict:
    """Map configured names to existing tools/ directories beside the resolved project."""
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
    if project_tools is None and (proj / "tools").is_dir():
        # 3b85: a linked-worktree session (project dir /opt/grc/wt-X) is the project even though
        # its directory name is not a configured repo name; its own tools/ are project tools.
        project_tools = proj / "tools"
    invoked = list(dict.fromkeys(_INVOKE.findall(command)))
    has_cd = bool(re.search(r"(?:^|[;&\n(]|&&|\|\|)\s*cd\s", command))

    def _tool_repo(tool: str):
        # First scanned repo with an is_file() match: project first, then configured order.
        if project_tools is not None and (project_tools / tool).is_file():
            return project_name
        for n, td in roots.items():
            if n != project_name and (td / tool).is_file():
                return n
        return None

    # (0, P-1.19) Apply the ABSOLUTE PATHS BY DEFAULT directive
    # (grc_library_private/INDEX.md) to an _INVOKE match outside CWD_GUARD_ALLOWLIST
    # whose filename is found by _tool_repo, when any cd regex match starts earlier.
    # This compares text offsets only: the cd need not execute, succeed, target the
    # selected repo, or affect the tool's shell scope. A later cd alone does not flag
    # an earlier tool, but any matched cd suppresses checks (1) and (2) below if this
    # check finds no flagged tool. Allowlist membership is a filename exemption.
    # The cd regex accepts start, ; & newline ( && || followed by optional whitespace,
    # then cd and whitespace. It does not recognize every shell cd form or parse quoting.
    cd_pos = [m.start() for m in re.finditer(r"(?:^|[;&\n(]|&&|\|\|)\s*cd\s", command)]
    # The operand of each cd (None for a bare cd), for the suggestion below. Read textually:
    # exactly one enclosing quote pair is removed, nothing is expanded, and a bare cd counts.
    cd_args = []
    for cm in re.finditer(r"(?:^|[;&\n(]|&&|\|\|)\s*cd(?=[\s;&|)]|$)", command):
        om = re.match(r"[ \t]+(\"[^\"]*\"|'[^']*'|[^\s;&|)]+)", command[cm.end():])
        arg = om.group(1) if om else None
        if arg and len(arg) >= 2 and arg[0] == arg[-1] and arg[0] in "'\"":
            arg = arg[1:-1]
        cd_args.append((cm.start(), arg))

    def _suggested(t, repo, at):
        # 3b85: after `cd <absolute dir>` in a LINKED WORKTREE, the tool meant is that tree's own
        # copy; suggesting the main checkout's path would run the right tool against the wrong
        # tree. Name the cd target's tools/ path when it holds the tool; else the scanned repo.
        before = [arg for pos, arg in cd_args if pos < at]
        if before and before[-1] and before[-1].startswith("/"):
            cand = Path(before[-1]) / "tools" / t
            try:
                if cand.is_file():
                    return shlex.quote(str(cand))
            except OSError:
                pass
        return shlex.quote(f"{parent}/{repo}/tools/{t}")

    flagged = []
    for m in _INVOKE.finditer(command):
        t = m.group(1)
        if t in CWD_GUARD_ALLOWLIST or _tool_repo(t) is None:
            continue
        if any(cp < m.start() for cp in cd_pos):
            flagged.append((t, _suggested(t, _tool_repo(t), m.start())))
    flagged = list(dict.fromkeys(flagged))
    if flagged:
        lines = [f"  - `tools/{t}`: use `python3 {path} ...` "
                 f"(absolute), not a cd-prefixed cwd-relative invocation."
                 for t, path in flagged]
        reason = (
            "BLOCKED (wrong-repo-tool-abspath): (P-1.19) a cwd-relative repo-tool match follows a `cd` match in the command text.\n"
            "WHY: the standing directive is ABSOLUTE PATHS BY DEFAULT "
            "(grc_library_private/INDEX.md); this filename is outside the cwd-guard allowlist, "
            "and this textual pattern triggers the absolute-path guardrail.\n"
            "CONSIDER INSTEAD: use an absolute tool path; the templates use python3, so select the appropriate interpreter for the file:\n" + "\n".join(lines)
            + "\n(The filename exemptions from this cd-before-tool check are: "
            + ", ".join(sorted(CWD_GUARD_ALLOWLIST)) + ".)")
        return True, reason
    if has_cd:
        return False, ""  # Any cd match, no flagged tool: skip sibling and Git checks.

    # (1) Reached only without a cd match: check captured cwd-relative tool filenames
    # against the configured roots. Skip a project is_file() match; otherwise report the
    # first other repo with an is_file() match, in configured order.
    # SOFTENED SCOPE (maintainer-directed 2026-07-24): project-file matches do not trigger
    # this sibling check. Files absent from all scanned roots do not trigger it either.
    # This does not inspect the Bash cwd or establish file-not-found there: an unlisted
    # project has no project_tools entry, and another cwd may contain a matching path.
    # Absolute tool paths do not themselves match _INVOKE; other matches can still block.
    if invoked and roots:
        hits = []
        for tool in invoked:
            if project_tools is not None and (project_tools / tool).is_file():
                continue  # Skip this project-file match; other tool and Git checks remain.
            elsewhere = [n for n, td in roots.items()
                         if n != project_name and (td / tool).is_file()]
            if elsewhere:
                hits.append((tool, elsewhere[0]))
        if hits:
            lines = [
                f"  - `tools/{tool}`: found in `{where}`; no scanned project-file match for `{project_name}`. "
                f"Templates: `python3 {parent}/{where}/tools/{tool} ...` (or "
                f"`cd {parent}/{where} && python3 tools/{tool} ...`, subject to the cd-tool allowlist)."
                for tool, where in hits
            ]
            reason = (
                "BLOCKED (wrong-repo-tool-sibling): a cwd-relative `tools/<x>` match has no scanned project-file match for "
                f"`{project_name}` but has a file match in a configured sibling.\n"
                "WHY: this scan suggests a possible repo mismatch; "
                "the hook does not inspect the Bash cwd or establish which file would run.\n"
                "CONSIDER INSTEAD: use an absolute tool path; the templates use python3, so select the appropriate interpreter. "
                "Use the cd alternative only for an allowlisted filename; neither form establishes the script's internal cwd independence:\n" + "\n".join(lines))
            return True, reason

    # (2) Reached only without a cd match and without a preceding tool block.
    # Block any _GIT_MUTATE match for the fixed subcommand-name set, regardless of
    # whether its arguments actually mutate a repo or specify another target.
    # This includes git stash list and a longer subcommand whose listed prefix ends at a
    # word boundary (e.g. git commit-graph, but not git commitment); it excludes
    # status/log/diff/show and a subcommand sharing no listed prefix (e.g. git tag).
    # Standard git -C <path> forms do not match.
    # Motivation: operations such as git add -A can affect an unintended repo without
    # necessarily failing; neither a Git match nor tool-path drift guarantees that outcome.
    if _GIT_MUTATE.search(command):
        reason = (
            "BLOCKED (wrong-repo-git): a `git` match hits a guarded subcommand name at a word boundary, with no matched `cd` anywhere in the command text.\n"
            "WHY: this fixed subcommand-name check flags possible wrong-repo operations "
            "(the 2026-07-24 `git add -A`-in-scratch near-miss); it does not determine "
            "whether this use mutates a repo or which repo it targets.\n"
            "CONSIDER INSTEAD: use `git -C <absolute-repo-path> <subcommand> ...`, or an explicit "
            "`cd <repo-root> &&`.")
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
        command = strip_heredocs(command)
        workspace = payload.get("workspace") or {}
        project_dir = (
            workspace.get("project_dir")
            or os.environ.get("CLAUDE_PROJECT_DIR")
            # Last-resort fallback: resolve the project root from this hook's own location
            # (<project>/.claude/hooks/this.py -> parents[2]). No hardcoded path, so it stays
            # correct across a repo move (for example an /old/root -> /new/root relocation).
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

        def test_project_tool_without_cd_allowed(self):
            # Softened scope (maintainer-directed 2026-07-24): this project-file match
            # with no cd and no other blocking match is allowed. This fixture does
            # not test cwd drift or establish which file another cwd would resolve.
            block, _ = decide("bash tools/run_all_audits.sh", self.pd)
            self.assertFalse(block)

        def test_absolute_path_allowed(self):
            block, _ = decide(f"python3 {self.proj}/tools/run_all_audits.sh", self.pd)
            self.assertFalse(block)

        def test_explicit_cd_allowlisted_sibling_tool_allowed(self):
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
            self.assertIn("wrong-repo-tool-abspath", reason)

        def test_cd_into_linked_worktree_suggests_its_own_tool(self):
            # 3b85: after `cd <linked worktree>`, the suggestion names that tree's tools/ path,
            # not the main checkout's (which would run the right tool on the wrong tree).
            wt = Path(self.parent) / "wt-x"
            (wt / "tools").mkdir(parents=True)
            (wt / "tools" / "run_all_audits.sh").write_text("")
            block, reason = decide(f"cd {wt} && bash tools/run_all_audits.sh", self.pd)
            self.assertTrue(block)
            self.assertIn(f"python3 {wt}/tools/run_all_audits.sh", reason)
            self.assertNotIn(f"{self.proj}/tools/run_all_audits.sh", reason)
            # A cd target without the tool keeps the scanned repo's path.
            empty = Path(self.parent) / "elsewhere"
            empty.mkdir()
            block, reason = decide(f"cd {empty} && bash tools/run_all_audits.sh", self.pd)
            self.assertTrue(block)
            self.assertIn(f"{self.proj}/tools/run_all_audits.sh", reason)

        def test_worktree_suggestion_quoting_and_bare_cd(self):
            # 3b85 QA round 1 (codex, claude): a path with a space is shell-quoted; exactly one
            # enclosing quote pair is removed (a trailing apostrophe in the name survives); a
            # bare cd after the worktree cd means the tool no longer runs there, so the
            # suggestion falls back.
            import shlex as _sh
            sp = Path(self.parent) / "wt space"
            ap = Path(self.parent) / "wt'"
            plain = Path(self.parent) / "wt"
            for d in (sp, ap, plain):
                (d / "tools").mkdir(parents=True)
                (d / "tools" / "run_all_audits.sh").write_text("")
            _, reason = decide(f'cd "{sp}" && bash tools/run_all_audits.sh', self.pd)
            self.assertIn(f"python3 {_sh.quote(str(sp / 'tools' / 'run_all_audits.sh'))} ...", reason)
            _, reason = decide(f'cd "{ap}" && bash tools/run_all_audits.sh', self.pd)
            self.assertIn(_sh.quote(str(ap / "tools" / "run_all_audits.sh")), reason)
            self.assertNotIn(f"python3 {plain}/tools/run_all_audits.sh", reason)
            _, reason = decide(f"cd {plain} && cd && bash tools/run_all_audits.sh", self.pd)
            self.assertIn(f"python3 {self.proj}/tools/run_all_audits.sh", reason)

        def test_worktree_session_tools_are_project_tools(self):
            # 3b85 QA round 1 (claude): in a linked-worktree session (a project dir whose name is
            # not a configured repo name) its own tools/ are project tools, so a tool present
            # there and in a sibling is not a false sibling block.
            wt = Path(self.parent) / "wt-session"
            (wt / "tools").mkdir(parents=True)
            (wt / "tools" / "credit-offload-queue.py").write_text("")
            block, _ = decide("python3 tools/credit-offload-queue.py list-workers", str(wt))
            self.assertFalse(block)
            block, reason = decide("python3 tools/validate.py", str(wt))
            self.assertTrue(block)  # absent from the worktree, present in a sibling
            self.assertIn("grc_library_scratch", reason)

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

        def test_tool_absent_from_scanned_roots_allowed(self):
            # This filename is absent from the scanned fixture roots, so it does not block.
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

        def test_selected_bare_git_subcommands_block(self):
            self.assertTrue(decide("git add -A", self.pd)[0])
            self.assertTrue(decide("git commit -m x", self.pd)[0])
            self.assertTrue(decide("echo hi && git push origin HEAD:main", self.pd)[0])
            self.assertTrue(decide("git cherry-pick abc123", self.pd)[0])
            self.assertTrue(decide("git revert HEAD", self.pd)[0])

        def test_git_dash_C_allowed(self):
            self.assertFalse(decide("git -C /home/x/grc_library commit -m y", self.pd)[0])
            self.assertFalse(decide("git -C /home/x/grc_library add -A", self.pd)[0])

        def test_git_status_log_diff_allowed(self):
            self.assertFalse(decide("git status --short", self.pd)[0])
            self.assertFalse(decide("git log --oneline -5", self.pd)[0])
            self.assertFalse(decide("git diff HEAD", self.pd)[0])

        def test_git_commit_with_preceding_cd_allowed(self):
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
