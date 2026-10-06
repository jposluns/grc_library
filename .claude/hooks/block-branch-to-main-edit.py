#!/usr/bin/env python3
"""PreToolUse Edit|Write hook: block an edit to a grc_library file while HEAD is on main.

Shipped 2026-07-24 (3.62 (closing PR #1134), the guardrail-review r10 G1 proposal; maintainer-decided
BUILD). A recurring class (improvement-log #595, #884): an edit lands on local ``main`` because
a merge+sync skipped the ``git checkout -b`` step that must precede any feature work. The project
PR workflow is strict, protected ``main`` is PR-only, so an edit to a ``grc_library`` file while
the repo is on ``main`` is essentially NEVER intended, which makes an FP-free block feasible (the
maintainer's assessment when routing G1). The rule "the FIRST action after merge+sync is ``git
checkout -b``" was convention-only until this hook.

What it does: reads the PreToolUse JSON payload on stdin, takes ``tool_input.file_path``, and
BLOCKS (exit 2) when BOTH hold:
  (1) the target file resolves to a path INSIDE the protected project repo (``project_dir``,
      i.e. ``grc_library``); AND
  (2) that repo's current branch (``git -C <project_dir> rev-parse --abbrev-ref HEAD``) is
      ``main`` or ``master``.
The block message suggests a feature branch via ``git checkout -b <branch>`` first.

Everything else is ALLOWED (the FP-safety envelope):
  - a target file NOT under ``project_dir`` (a sibling repo ``grc_library_scratch`` /
    ``grc_library_private`` / ``grc_library_ref``, or anywhere else): those repos legitimately
    take direct edits on their own ``main`` (scratch/private are push-direct), so the guard must
    NOT fire on them. It protects ONLY the PR-only ``grc_library`` main.
  - the project repo on a FEATURE branch (anything other than main/master): the normal case.
  - a detached HEAD (``rev-parse --abbrev-ref HEAD`` returns ``HEAD``): not main, allowed.
  - any parse / git / resolve failure: fail-OPEN (this is a workflow guard against one mistake
    shape, not a security boundary).

A false block just tells the orchestrator to branch first, the intended discipline. This is the
Edit|Write analogue of ``block-wrong-repo-tool.py`` (which guards the Bash repo-target side).
NOTE: when neither ``workspace.project_dir`` nor ``CLAUDE_PROJECT_DIR`` is set, ``main`` falls
back to the hardcoded project path below and still evaluates against it; if that path does not
match the session's repo, the branch check fails-open (the ``git -C`` errors), so a path
mismatch never blocks a legitimate edit. The PR-workflow "never develop on main" convention is
the primary control either way.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason.

Self-test: ``python3 .claude/hooks/block-branch-to-main-edit.py --self-test``.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# The settings.json launcher runs `python3 -I` (SECI-config-is-executable-trust-gate): no
# directory ever enters sys.path, the colocated `_hook_state` recorder executes ONLY from
# its reviewed source bytes, loaded at the recording site through _load_sibling below, and
# no import statement names it anywhere in this file, so nothing planted beside this hook
# (a decoy module, a __pycache__/*.pyc, a seeded sys.modules entry) can run.
# MISSING-HELPER BEHAVIOUR: the decision still blocks; only the recording is skipped.
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


_MAIN_BRANCHES = ("main", "master")


def _current_branch(repo_root: str):
    """Return the repo's current branch name, or None on any failure (fail-open)."""
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def decide(file_path: str, project_dir: str) -> tuple[bool, str]:
    if not isinstance(file_path, str) or not file_path.strip():
        return False, ""
    try:
        proj = Path(project_dir).resolve()
        target = Path(file_path).resolve()
    except Exception:
        return False, ""
    # (1) only the protected project repo is guarded; a sibling repo (scratch / private / ref)
    # or a path outside the repo is allowed (those take direct edits on their own main).
    try:
        target.relative_to(proj)
    except ValueError:
        return False, ""
    # (2) block only when the project repo is on main/master.
    branch = _current_branch(str(proj))
    if branch in _MAIN_BRANCHES:
        rel = target.relative_to(proj)
        reason = (
            "BLOCKED (branch-to-main-edit): an edit to a `grc_library` file "
            f"(`{rel}`) while the repo is on `{branch}`.\n"
            "WHY: `main` is PR-only; edits belong on a feature branch, and an edit on `main` "
            "is essentially never intended.\n"
            "CONSIDER INSTEAD: run `git -C {proj} checkout -b claude/<name>` first, then "
            "re-apply the edit. (If you genuinely intend to edit a SIBLING repo, use its "
            "absolute path so the target resolves outside `grc_library`.)"
        ).replace("{proj}", str(proj))
        return True, reason
    return False, ""


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    workspace = payload.get("workspace") or {}
    project_dir = (
        workspace.get("project_dir")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        # Last-resort fallback: resolve the project root from this hook's own location
        # (<project>/.claude/hooks/this.py -> parents[2]). No hardcoded path, so it stays
        # correct across a repo move (for example an /old/root -> /new/root relocation).
        or str(Path(__file__).resolve().parents[2])
    )
    try:
        block, reason = decide(file_path, project_dir)
    except Exception:
        return 0  # fail-open
    if block:
        try:
            _load_sibling("_hook_state").record_block(file_path, "branch-to-main-edit")
        except Exception:
            pass
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    # Every scratch path the self-test makes (including a child git's) lands under one root that is
    # removed on exit, so a run leaves nothing behind in the temp directory (3b103).
    import atexit as _atx, os as _os, shutil as _shu, tempfile as _tpf
    _tpf.tempdir = _tpf.mkdtemp(prefix="grc-selftest-"); _os.environ["TMPDIR"] = _tpf.tempdir
    _atx.register(_shu.rmtree, _tpf.tempdir, True)
    import tempfile
    import unittest

    def _git(repo, *args):
        subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True)

    class T(unittest.TestCase):
        def setUp(self):
            self.parent = tempfile.mkdtemp()
            # protected project repo on main, with one committed file
            self.proj = Path(self.parent) / "grc_library"
            (self.proj / "sub").mkdir(parents=True)
            _git(str(self.proj), "init", "-q", "-b", "main")
            _git(str(self.proj), "config", "user.email", "t@t")
            _git(str(self.proj), "config", "user.name", "t")
            (self.proj / "sub" / "doc.md").write_text("x")
            _git(str(self.proj), "add", "-A")
            _git(str(self.proj), "commit", "-q", "-m", "init")
            # sibling repo also on main
            self.sib = Path(self.parent) / "grc_library_scratch"
            (self.sib / "queue").mkdir(parents=True)
            _git(str(self.sib), "init", "-q", "-b", "main")
            _git(str(self.sib), "config", "user.email", "t@t")
            _git(str(self.sib), "config", "user.name", "t")
            (self.sib / "queue" / "o.md").write_text("x")
            _git(str(self.sib), "add", "-A")
            _git(str(self.sib), "commit", "-q", "-m", "init")
            self.pd = str(self.proj)

        def test_edit_project_file_on_main_blocks(self):
            block, reason = decide(str(self.proj / "sub" / "doc.md"), self.pd)
            self.assertTrue(block)
            self.assertIn("branch-to-main", reason)

        def test_edit_project_file_on_feature_branch_allowed(self):
            _git(self.pd, "checkout", "-q", "-b", "claude/feature")
            block, _ = decide(str(self.proj / "sub" / "doc.md"), self.pd)
            self.assertFalse(block)

        def test_edit_sibling_repo_file_while_project_on_main_allowed(self):
            # grc_library is on main, but the target is a scratch file: allowed (scratch is
            # push-direct on its own main). This is the key FP-safety case.
            block, _ = decide(str(self.sib / "queue" / "o.md"), self.pd)
            self.assertFalse(block)

        def test_edit_outside_any_repo_allowed(self):
            block, _ = decide(str(Path(self.parent) / "loose.txt"), self.pd)
            self.assertFalse(block)

        def test_detached_head_allowed(self):
            head = subprocess.run(
                ["git", "-C", self.pd, "rev-parse", "HEAD"],
                capture_output=True, text=True).stdout.strip()
            _git(self.pd, "checkout", "-q", head)  # detached
            block, _ = decide(str(self.proj / "sub" / "doc.md"), self.pd)
            self.assertFalse(block)

        def test_empty_file_path_allowed(self):
            self.assertFalse(decide("", self.pd)[0])

        def test_non_git_project_dir_fails_open(self):
            plain = tempfile.mkdtemp()
            (Path(plain) / "f.md").write_text("x")
            self.assertFalse(decide(str(Path(plain) / "f.md"), plain)[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
