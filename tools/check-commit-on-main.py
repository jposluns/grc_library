#!/usr/bin/env python3
"""Git-native pre-commit guard: refuse a commit on a grc_library ``main``/``master`` checkout.

P-TODO 3b17 (2026-09-24). ``.claude/hooks/block-branch-to-main-edit.py`` refuses an Edit/Write to a
grc_library file while HEAD is ``main``, but a file written through Bash (python, sed, a heredoc)
bypasses it: on 2026-09-24 01:04Z a gate edit was made on ``main`` after a merge and caught only by
chance before the commit. The durable step to refuse is the COMMIT. A PreToolUse shell parser would have
to model ``cd``, ``git -C``, subshells, and ``switch``/``checkout`` sequences; this check runs INSIDE
``git commit`` itself, so it sees every commit path (any tool, any worktree) and reads the committing
worktree's own HEAD, which is exactly the property in question. The remote ruleset already refuses a
push to ``main``; this catches the mistake one step earlier, before a commit has to be moved.

Installed by ``tools/install-git-hooks.sh`` as a shim in the SHARED hooks dir of the grc_library
repository, so it runs for the main checkout and every linked worktree (and for no other repository:
sibling repos such as grc_library_private have their own hooks dir and legitimately commit on main).
The shim execs the ACTIVE checkout's ``tools/git-hooks/pre-commit``, which execs this file.

Decision (``decide``, pure):
  - override ``GRC_ALLOW_MAIN_COMMIT`` set and non-empty: allow, with a NOTE;
  - HEAD state unreadable (a git error): REFUSE (ignorance refuses, as in check-dirty-tree-push.py);
  - HEAD detached: allow (not a branch commit);
  - HEAD on ``main`` or ``master``: REFUSE;
  - otherwise allow.

Residue, stated: git runs pre-commit for ``git commit`` (including ``--amend``, and a ``git commit``
that concludes a conflicted merge, cherry-pick, or revert), but NOT for the commits that ``git am``,
``git rebase``, or an automatic ``git cherry-pick`` / ``git revert`` create themselves, nor for a
fast-forward or a ``git merge`` that records its commit directly (that is ``pre-merge-commit``);
``--no-verify`` skips it; and it guards nothing until ``tools/install-git-hooks.sh`` has installed
the shim in this clone. The PR-only workflow never makes any of those on local ``main``, and the
remote ruleset remains the push barrier.

Branch identity is compared on the FULL ref (``refs/heads/main``), never a shortened name: git shortens
ambiguity-aware, so with a tag named ``main`` the short form of the branch is ``heads/main``.
"""
import os
import shutil
import subprocess
import sys

_OVERRIDE = "GRC_ALLOW_MAIN_COMMIT"
PROTECTED = ("refs/heads/main", "refs/heads/master")
_REFUSE_MAIN = (
    "check-commit-on-main: REFUSING the commit: this grc_library checkout is on '{branch}', which is "
    "PR-only. Move the work to a feature branch first: `git switch -c <branch>` (the staged changes "
    f"come with you), then commit. Deliberate override: {_OVERRIDE}=1."
)
_REFUSE_UNREADABLE = (
    "check-commit-on-main: REFUSING the commit: the checkout's HEAD could not be read, so it is "
    f"unknown whether this is a commit on main. Deliberate override: {_OVERRIDE}=1."
)
_NOTE_OVERRIDE = (
    f"check-commit-on-main: NOTE: {_OVERRIDE} is set; skipping the commit-on-main check "
    "(deliberate override)."
)


def decide(allow, head_ok, branch):
    """PURE. Returns (exit_code, stderr_message).

    allow:   the override env var is set to a non-empty value.
    head_ok: HEAD was read (``git symbolic-ref`` succeeded, or failed only because HEAD is detached).
    branch:  the FULL ref HEAD points at (refs/heads/...), or None when HEAD is detached.
    """
    if allow:
        return 0, _NOTE_OVERRIDE
    if not head_ok:
        return 1, _REFUSE_UNREADABLE
    if branch in PROTECTED:
        return 1, _REFUSE_MAIN.format(branch=branch[len("refs/heads/"):])
    return 0, ""


def read_head():
    """Thin observer: (head_ok, branch). ``git symbolic-ref -q HEAD`` exits 1 (quietly) exactly when
    HEAD is detached; any other failure (not a repository, a corrupt HEAD, git missing) is unreadable."""
    try:
        cp = subprocess.run(["git", "symbolic-ref", "-q", "HEAD"],
                            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return False, None
    if cp.returncode == 0:
        return True, cp.stdout.rstrip("\n") or None
    if cp.returncode == 1 and not cp.stderr.strip():
        return True, None
    return False, None


def _pre_commit():
    code, msg = decide(bool(os.environ.get(_OVERRIDE)), *read_head())
    if msg:
        print(msg, file=sys.stderr)
    return code


def _integration_self_test():
    """End to end: a real repository, the real installer, and real `git commit` calls."""
    import shutil
    import tempfile
    from pathlib import Path
    src = Path(__file__).resolve().parents[1]
    failures = []
    with tempfile.TemporaryDirectory() as base:
        repo = Path(base) / "r"
        (repo / "tools" / "git-hooks").mkdir(parents=True)
        for rel in ("tools/check-commit-on-main.py", "tools/install-git-hooks.sh",
                    "tools/git-hooks/pre-commit", "tools/git-hooks/pre-push"):
            shutil.copy2(src / rel, repo / rel)
        # Isolated from the caller: no inherited GIT_* (GIT_DIR, GIT_INDEX_FILE, ...), no global or
        # system config, as in check-dirty-tree-push.py's integration self-test.
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != _OVERRIDE}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid",
                   PRE_COMMIT_HOME=str(Path(base) / "pc-home"))

        def run(args, cwd=repo, extra=None):
            return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                                  env={**env, **(extra or {})})

        def must(args, cwd=repo):
            # Fixture setup: a failed step makes the later assertions meaningless, so it is recorded.
            cp = run(args, cwd=cwd)
            if cp.returncode != 0:
                failures.append(f"fixture step failed: {' '.join(map(str, args))}: {cp.stderr.strip()}")
            return cp

        must(["git", "init", "-q", "-b", "main"])
        must(["git", "config", "commit.gpgsign", "false"])
        inst = run(["sh", "tools/install-git-hooks.sh"])
        if inst.returncode != 0:
            failures.append(f"installer failed: {inst.stderr.strip()}")
        (repo / "a.txt").write_text("1\n")
        run(["git", "add", "a.txt", "tools"])  # tracked, so a linked worktree carries the hook
        cp = run(["git", "commit", "-q", "-m", "on main"])
        if cp.returncode == 0 or "REFUSING the commit" not in cp.stderr:
            failures.append("a commit on main was not refused")
        cp = run(["git", "commit", "-q", "-m", "override"], extra={_OVERRIDE: "1"})
        if cp.returncode != 0:
            failures.append(f"the override did not allow a commit on main: {cp.stderr.strip()}")
        must(["git", "switch", "-q", "-c", "feature"])
        (repo / "a.txt").write_text("2\n")
        run(["git", "add", "a.txt"])
        cp = run(["git", "commit", "-q", "-m", "on feature"])
        if cp.returncode != 0:
            failures.append(f"a commit on a feature branch was refused: {cp.stderr.strip()}")
        linked = Path(base) / "wt"
        must(["git", "worktree", "add", "-q", str(linked), "main"])
        (linked / "b.txt").write_text("x\n")
        run(["git", "add", "b.txt"], cwd=linked)
        cp = run(["git", "commit", "-q", "-m", "worktree main"], cwd=linked)
        if cp.returncode == 0:
            failures.append("a commit on main in a linked worktree was not refused")
        # An older checkout without the tracked hook file: the installed shim fails OPEN.
        (repo / "tools" / "git-hooks" / "pre-commit").rename(repo / "moved-pre-commit")
        (repo / "a.txt").write_text("3\n")
        run(["git", "add", "a.txt"])
        cp = run(["git", "commit", "-q", "-m", "no tracked hook"])
        if cp.returncode != 0:
            failures.append(f"the shim did not fail open without the tracked hook: {cp.stderr.strip()}")
        (repo / "moved-pre-commit").rename(repo / "tools" / "git-hooks" / "pre-commit")
        # A tag named 'main' makes git's SHORT name for the branch 'heads/main'; the full ref is compared.
        must(["git", "worktree", "remove", "--force", str(linked)])  # frees 'main' for the switch
        sw = run(["git", "switch", "-q", "main"])
        if sw.returncode != 0:
            failures.append(f"fixture: could not switch to main: {sw.stderr.strip()}")
        must(["git", "tag", "main", "feature"])
        (repo / "a.txt").write_text("4\n")
        run(["git", "add", "a.txt"])
        cp = run(["git", "commit", "-q", "-m", "tag named main"])
        if cp.returncode == 0:
            failures.append("a commit on main was allowed when a tag named 'main' exists")
        # Coexistence with the pre-commit framework (when installed): it chains the managed hook as
        # pre-commit.legacy, the commit on main is still refused, and a re-install reports the chain.
        if shutil.which("pre-commit"):
            (repo / ".pre-commit-config.yaml").write_text("repos: []\n")
            cp = run(["pre-commit", "install"])
            if cp.returncode != 0:
                failures.append(f"pre-commit install failed: {cp.stderr.strip()}")
            cp = run(["git", "commit", "-q", "-m", "framework chained"])
            if cp.returncode == 0 or "REFUSING the commit" not in cp.stderr:
                failures.append("the framework-chained guard did not refuse a commit on main")
            # File contents cannot prove the chain, so a re-install never claims it: it refuses the
            # pre-commit half (non-zero) and says the chain must be checked by behaviour.
            cp = run(["sh", "tools/install-git-hooks.sh"])
            if cp.returncode == 0 or "cannot be verified from file contents" not in cp.stderr:
                failures.append("the installer claimed or ignored a framework chain it cannot verify")
            # A FOREIGN active hook beside a managed .legacy is not a chain: it must be refused.
            hooks = Path(run(["git", "rev-parse", "--git-path", "hooks"]).stdout.strip())
            hooks = hooks if hooks.is_absolute() else repo / hooks
            (hooks / "pre-commit").write_text("#!/bin/sh\nexit 0\n")
            cp = run(["sh", "tools/install-git-hooks.sh"])
            if cp.returncode == 0 or "refusing to overwrite the existing hook" not in cp.stderr:
                failures.append("a foreign active hook beside a managed .legacy was accepted")
    return failures


def _self_test():
    cases = [
        ("override allows even on main", decide(True, True, "main")[0], 0),
        ("override allows an unreadable HEAD", decide(True, False, None)[0], 0),
        ("unreadable HEAD refuses", decide(False, False, None)[0], 1),
        ("main refuses", decide(False, True, "refs/heads/main")[0], 1),
        ("master refuses", decide(False, True, "refs/heads/master")[0], 1),
        ("detached HEAD allows", decide(False, True, None)[0], 0),
        ("feature branch allows", decide(False, True, "refs/heads/tooling/x")[0], 0),
        ("a branch merely containing 'main' allows", decide(False, True, "refs/heads/main-fix")[0], 0),
        ("a branch named 'heads/main' is not main", decide(False, True, "refs/heads/heads/main")[0], 0),
        ("a distinct branch 'main' + U+00A0 is not main", decide(False, True, "refs/heads/main\u00a0")[0], 0),
        ("the refusal names the override", "GRC_ALLOW_MAIN_COMMIT=1" in decide(False, True, "refs/heads/main")[1], True),
        ("the refusal names the short branch", "on 'main'" in decide(False, True, "refs/heads/main")[1], True),
    ]
    failures = [f"{name}: got {got!r}, want {want!r}" for name, got, want in cases if got != want]
    failures += _integration_self_test()
    total = len(cases) + 7 + (4 if shutil.which("pre-commit") else 0)
    for f in failures:
        print(f"  FAIL: {f}")
    print(f"self-test: {total - len(failures)}/{total} passed" if not failures
          else f"self-test: FAILED ({len(failures)} of {total})")
    return 1 if failures else 0


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    if len(argv) > 1 and argv[1] == "--pre-commit":
        return _pre_commit()
    print("usage: check-commit-on-main.py --pre-commit | --self-test", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
