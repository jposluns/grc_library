#!/usr/bin/env python3
"""Push-time dirty-tracked-tree backstop (git-native raw pre-push hook, Layer B).

Runs at `git push` time as a RAW git `pre-push` hook (installed by
tools/install-git-hooks.sh as a persistent shim that resolves the active checkout
and invokes tools/git-hooks/pre-push, which execs this script with --pre-push).
It REFUSES a push when the tracked working tree is modified or staged AND the
push updates a BRANCH to the current HEAD, so a commit
that shipped an incomplete tree (the `git add <list>` that silently dropped a
file edited after the add) cannot be pushed unnoticed.

WHY a RAW hook, not the pre-commit framework: the pre-commit framework's
pre-push stage runs `staged_files_only`, which STASHES unstaged tracked edits
before invoking the hook, so the hook would see a clean tree and MISS the exact
unstaged git-add-drop case it exists to catch (verified empirically; codex
finding, OF-2026-09-20-dirty-tree-push-hook-defects). A raw hook runs before any
stashing and reads the real tree.

WHY stdin ref-scoping: an unconditional pre-push check wrongly blocks a
branch deletion (`git push origin :b`), a tag push (including a tag pointing at
HEAD), or pushing an unrelated branch when the working tree has unrelated edits.
git passes the refs being pushed on stdin (`<local_ref> <local_sha> <remote_ref>
<remote_sha>`); this hook checks the tree ONLY when the DESTINATION is a BRANCH ref
(`refs/heads/*`) receiving the current HEAD sha, i.e. you are
pushing your current commits, whose missing uncommitted edits are the concern.
A deletion (all-zero sha), a tag or other non-branch ref, or an older/other sha
leaves the working tree irrelevant, so the push is allowed. A non-empty malformed
stdin line forces a conservative check (fail closed).

This MIRRORS the dirty-tracked-tree attestation in tools/pre-push-guard.sh
(same `git status --porcelain --untracked-files=no`, same PRE_PUSH_GUARD_ALLOW_DIRTY
override with the same set-and-non-empty semantics, same FAIL-CLOSED stance on an
unreadable `git status`). pre-push-guard.sh is the sanctioned `pre-push-guard.sh
&& git push` wrapper; this hook is the automatic backstop that also covers a raw
`git push` which skips the wrapper. When pushing HEAD both run and agree (defence
in depth); on a deletion or tag push the unconditional wrapper refuses on a dirty
tree while this HEAD-scoped hook allows. Keep the shared dirty-tree check in
lock-step: a change to one is a change to both.

Untracked new files (`??`) are out of scope (same as pre-push-guard.sh):
`--untracked-files=no`. Exit 0 = allow the push; exit 1 = refuse.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

_OVERRIDE = "PRE_PUSH_GUARD_ALLOW_DIRTY"

_REFUSE_UNREADABLE = (
    "check-dirty-tree-push: REFUSING the push: 'git status' failed, so the "
    "working-tree state cannot be attested against HEAD (the committed tree "
    "that ships). Fix the repository state, then retry. Deliberate override: "
    f"{_OVERRIDE}=1."
)
_REFUSE_DIRTY = (
    "check-dirty-tree-push: REFUSING the push: tracked files are modified or "
    "staged, so what you are pushing may not be what the working tree holds "
    "(the `git add` that dropped a later edit). Commit or stash the changes, "
    f"then retry. Deliberate override: {_OVERRIDE}=1."
)
_NOTE_OVERRIDE = (
    f"check-dirty-tree-push: NOTE: {_OVERRIDE} is set; skipping the "
    "dirty-tracked-tree attestation check (deliberate override)."
)


def decide(allow_dirty, status_ok, porcelain):
    """Pure decision. Returns (exit_code, stderr_message).

    allow_dirty: the override env var is set to a non-empty value (matches the
                 shell guard's `[ -z "$VAR" ]`: set-and-non-empty = active).
    status_ok:   `git status` ran successfully (False = it errored).
    porcelain:   its stdout (only meaningful when status_ok); None otherwise.

    FAIL-CLOSED: an unreadable status refuses (ignorance refuses, never
    permits; the guard-input soundness discipline), matching pre-push-guard.sh.
    """
    if allow_dirty:
        return 0, _NOTE_OVERRIDE
    if not status_ok:
        return 1, _REFUSE_UNREADABLE
    if porcelain is not None and porcelain.strip():
        return 1, _REFUSE_DIRTY
    return 0, ""


def _is_zero_sha(sha):
    """True if sha is an all-zero object id (a ref deletion)."""
    s = (sha or "").strip()
    return s != "" and set(s) == {"0"}


def _valid_oid(value, width):
    """Git emits full SHA-1 or SHA-256 object IDs, including zero sentinels."""
    return width in (40, 64) and re.fullmatch(
        rf"[0-9a-fA-F]{{{width}}}", value
    ) is not None


def _valid_ref(value):
    """Validate a fully qualified ref using git check-ref-format's rules."""
    if not value.startswith("refs/") or value.endswith("."):
        return False
    if ".." in value or "@{" in value:
        return False
    if any(ord(c) < 32 or ord(c) == 127 or c in " ~^:?*[\\" for c in value):
        return False
    return all(
        part and not part.startswith(".") and not part.endswith(".lock")
        for part in value.split("/")
    )


def _valid_source(value, oid):
    """Accept canonical refs, HEAD, and full/abbreviated literal object IDs.

    Other revision expressions conservatively require the tree check.
    """
    return (
        _valid_ref(value)
        or value == "HEAD"
        or (
            re.fullmatch(r"[0-9a-fA-F]{4,64}", value) is not None
            and oid.lower().startswith(value.lower())
        )
    )


def head_is_pushed(stdin_lines, head_sha):
    """Check destination branch scope; malformed records require attestation.

    Records have exactly four fields:
    <local_ref> <local_sha> <remote_ref> <remote_sha>.
    Only a nonzero local object ID equal to HEAD going to refs/heads/*
    triggers the check for a well-formed record. Unknown HEAD is handled
    conservatively by the caller.
    """
    if not head_sha:
        return False
    width = len(head_sha)
    if not _valid_oid(head_sha, width):
        return True
    for line in stdin_lines:
        if not line.strip():
            continue
        parts = line.split(" ")  # single ASCII-space field separators (git protocol); NOT split() (Unicode whitespace in a valid ref must not split a field)
        if len(parts) != 4:
            return True
        local_ref, local_sha, remote_ref, remote_sha = parts
        # Validate BEFORE allowing deletions, other commits, or non-branches.
        if (
            not _valid_oid(local_sha, width)
            or not _valid_oid(remote_sha, width)
            or not _valid_ref(remote_ref)
        ):
            return True
        if _is_zero_sha(local_sha):
            if local_ref != "(delete)":
                return True
            continue
        if not _valid_source(local_ref, local_sha):
            return True
        if (
            remote_ref.startswith("refs/heads/")
            and local_sha.lower() == head_sha.lower()
        ):
            return True
    return False


def _run_git(args):
    """Run a git command; return (ok, stdout) with ok False on any failure."""
    try:
        cp = subprocess.run(
            ["git"] + args, capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return False, None
    if cp.returncode != 0:
        return False, None
    return True, cp.stdout


def _git_status():
    """Run `git status --porcelain --untracked-files=no`. Returns (ok, out)."""
    return _run_git(["status", "--porcelain", "--untracked-files=no"])


def _current_head():
    """Return the current HEAD sha, or None if it cannot be resolved."""
    ok, out = _run_git(["rev-parse", "HEAD"])
    return out.strip() if (ok and out) else None


def _allow_dirty_env():
    """Override active iff the env var is set to a non-empty value (shell `-z`)."""
    return os.environ.get(_OVERRIDE, "") != ""


def _check_tree():
    """Gather status and decide; print the message; return the exit code."""
    ok, out = _git_status()
    code, msg = decide(_allow_dirty_env(), ok, out)
    if msg:
        print(msg, file=sys.stderr)
    return code


def _pre_push():
    """Raw pre-push entry: scope to HEAD-bearing branch pushes, then check."""
    try:
        stdin_data = "" if sys.stdin.isatty() else sys.stdin.read()
    except Exception:
        # stdin unreadable -> fail closed: check the tree conservatively
        # (an unreadable input must never read as 'nothing to push' and pass).
        return _check_tree()
    stdin_lines = stdin_data.split("\n")  # LF record boundaries only (git protocol); NOT splitlines() (Unicode line seps in a valid ref must not split a record)
    head_sha = _current_head()
    # Check when the push updates a branch to HEAD. If HEAD is unresolvable
    # (e.g. unborn), fall back to checking (conservative, override-able).
    should_check = head_sha is None or head_is_pushed(stdin_lines, head_sha)
    if not should_check:
        return 0
    return _check_tree()


def _integration_self_test():
    """Exercise the real entry points and pushes in isolated local repositories."""
    checks = 0
    source_tools = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="dirty-tree-push-self-test-") as tmp:
        base = Path(tmp)
        repo, remote, linked = base / "repo", base / "remote.git", base / "linked"
        home = base / "home"
        home.mkdir()
        # Do not inherit repository selection, config injection, or an override
        # from the invoking hook/CI process. No network or user config is needed.
        env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("GIT_") and key != _OVERRIDE
        }
        env.update(
            HOME=str(home),
            XDG_CONFIG_HOME=str(home),
            GIT_CONFIG_NOSYSTEM="1",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_TERMINAL_PROMPT="0",
            GIT_ALLOW_PROTOCOL="file",
            LC_ALL="C",
        )

        def check(condition, message):
            nonlocal checks
            checks += 1
            if not condition:
                raise RuntimeError(message)

        def run(args, cwd=repo, expected=0, stdin=None):
            cp = subprocess.run(
                [str(arg) for arg in args], cwd=cwd, env=env,
                input=stdin, capture_output=True, text=True, timeout=30,
            )
            check(
                cp.returncode == expected,
                f"{args!r}: expected {expected}, got {cp.returncode}\n"
                f"stdout:\n{cp.stdout}\nstderr:\n{cp.stderr}",
            )
            return cp

        def git(*args, cwd=repo, expected=0):
            return run(["git", *args], cwd=cwd, expected=expected)

        def push(source, destination, blocked, cwd=repo):
            cp = git(
                "push", "origin", f"{source}:{destination}",
                cwd=cwd, expected=1 if blocked else 0,
            )
            if blocked:
                check(
                    "check-dirty-tree-push: REFUSING" in cp.stderr,
                    f"Push failed without the dirty-tree refusal:\n{cp.stderr}",
                )
            result = git(
                "--git-dir", str(remote), "rev-parse", "--verify",
                "--quiet", destination, expected=1 if blocked else 0,
            )
            if not blocked:
                check(result.stdout.strip() == head, "Remote received wrong object")

        git("init", "--quiet", "--template=", str(repo), cwd=base)
        git("init", "--quiet", "--bare", "--template=", str(remote), cwd=base)
        git("symbolic-ref", "HEAD", "refs/heads/main")
        git("config", "user.name", "Dirty-tree hook self-test")
        git("config", "user.email", "dirty-tree-self-test@example.com")
        git("config", "commit.gpgsign", "false")
        git("config", "tag.gpgsign", "false")
        git("config", "core.autocrlf", "false")
        git("remote", "add", "origin", str(remote))
        (repo / "tools" / "git-hooks").mkdir(parents=True)
        for relative in (
            "check-dirty-tree-push.py", "install-git-hooks.sh",
            "git-hooks/pre-push",
        ):
            shutil.copyfile(source_tools / relative, repo / "tools" / relative)
        tracked = repo / "tracked.txt"
        tracked.write_text("committed\n", encoding="utf-8")
        git("add", ".")
        git("commit", "--quiet", "-m", "Self-contained hook fixture")
        head = git("rev-parse", "HEAD").stdout.strip()
        zero = "0" * len(head)
        git("tag", "at-head")
        git("worktree", "add", "--quiet", "-b", "linked", str(linked))

        def install(cwd=repo, expected=0):
            return run(
                ["sh", cwd / "tools" / "install-git-hooks.sh"],
                cwd=cwd, expected=expected,
            )

        # Installing FROM a linked worktree must create a persistent file.
        install(cwd=linked)
        hook_path = Path(git("rev-parse", "--git-path", "hooks/pre-push").stdout.strip())
        hook = hook_path if hook_path.is_absolute() else repo / hook_path
        check(hook.is_file() and not hook.is_symlink(), "Installed hook is not a regular file")
        check(os.access(hook, os.X_OK), "Installed hook is not executable")
        installed = hook.read_bytes()
        install()
        check(hook.read_bytes() == installed, "Repeat installation changed the hook")

        # Resolve the ACTIVE linked checkout, rather than always checking main.
        linked_tracked = linked / "tracked.txt"
        linked_tracked.write_text("dirty linked checkout\n", encoding="utf-8")
        push("HEAD", "refs/heads/linked-dirty", True, cwd=linked)
        linked_tracked.write_text("committed\n", encoding="utf-8")
        git("worktree", "remove", str(linked))
        check(not linked.exists(), "Linked worktree was not removed")
        check(hook.is_file() and not hook.is_symlink(), "Hook lost after worktree removal")
        push("refs/heads/main", "refs/heads/clean", False)

        tracked.write_text("dirty main checkout\n", encoding="utf-8")
        # Real git push supplies the exact pre-push records for these F1 cases.
        push(head, "refs/heads/from-sha", True)
        push("refs/tags/at-head", "refs/heads/from-tag", True)
        push("main", "refs/tags/from-branch", False)
        push("refs/heads/main", "refs/heads/from-main", True)
        push("HEAD", "refs/heads/from-head", True)

        # F2 through _pre_push(), the tracked shim, AND the installed shim.
        for argv in (
            [sys.executable, repo / "tools/check-dirty-tree-push.py", "--pre-push"],
            ["sh", repo / "tools/git-hooks/pre-push"],
            [str(hook)],
        ):
            cp = run(
                [*argv, "origin", str(remote)], expected=1,
                stdin="garbage garbage garbage garbage\n",
            )
            check("check-dirty-tree-push: REFUSING" in cp.stderr, "Malformed input bypassed attestation")
            run(
                [*argv, "origin", str(remote)],
                stdin=f"refs/heads/main {head} refs/tags/direct {zero}\n",
            )

        # Exercise the staged-dirty half with a real push, then prove recovery.
        git("add", "tracked.txt")
        push("main", "refs/heads/staged", True)
        git("reset", "--hard", "--quiet", "HEAD")
        push("main", "refs/heads/recovered", False)

        # Preserve refusal behavior for both empty and nonempty hooksPath.
        hook.unlink()
        for value in ("", str(base / "custom-hooks")):
            git("config", "core.hooksPath", value)
            cp = install(expected=1)
            check("core.hooksPath is set" in cp.stderr, "hooksPath refusal was lost")
            check(not os.path.lexists(hook), "Installer wrote a hook under hooksPath")
            git("config", "--unset", "core.hooksPath")

        foreign = b"#!/bin/sh\n# A foreign hook must survive.\nexit 0\n"
        hook.write_bytes(foreign)
        hook.chmod(0o755)
        install(expected=1)
        check(hook.read_bytes() == foreign, "Foreign hook was overwritten")
        hook.unlink()
        for target in (
            "missing-foreign-hook",
            str(repo / "tools/git-hooks/pre-push"),  # Legacy install: explicit removal required.
        ):
            hook.symlink_to(target)
            install(expected=1)
            check(
                hook.is_symlink() and os.readlink(hook) == target,
                "Existing symlink was changed",
            )
            hook.unlink()
    return checks


def _self_test():
    """Pure decisions plus real entry-point, installer, and push regressions."""
    failures = []
    Z40 = "0" * 40
    HEAD = "a" * 40
    OTHER = "b" * 40
    decide_cases = [
        (False, True, "", 0),
        (False, True, " M autonomous-decisions.md\n", 1),
        (False, True, "M  staged.py\n", 1),
        (False, True, "\n  \n", 0),
        (False, False, None, 1),
        (True, True, " M anything\n", 0),
        (True, False, None, 0),
        (False, True, None, 0),
    ]
    for i, (ad, ok, por, exp) in enumerate(decide_cases):
        if decide(ad, ok, por)[0] != exp:
            failures.append(f"decide case {i}: expected {exp}")
    if decide(False, True, " M x\n")[0] == 0:
        failures.append("observer: dirty tree permitted without override")

    push_cases = [
        # (stdin_lines, head_sha, expected)
        ([f"refs/heads/main {HEAD} refs/heads/main {OTHER}"], HEAD, True),   # branch push of HEAD -> check
        ([f"refs/heads/main {OTHER} refs/heads/main {Z40}"], HEAD, False),   # older/other sha -> allow
        ([f"(delete) {Z40} refs/heads/old {OTHER}"], HEAD, False),           # deletion -> allow
        ([f"refs/tags/v1 {OTHER} refs/tags/v1 {Z40}"], HEAD, False),         # tag (non-HEAD) -> allow
        ([f"refs/tags/v1 {HEAD} refs/tags/v1 {OTHER}"], HEAD, False),        # TAG AT HEAD -> allow (codex F1)
        ([f"HEAD {HEAD} refs/heads/x {OTHER}"], HEAD, True),                 # bare HEAD ref -> check
        ([f"refs/notes/commits {HEAD} refs/notes/commits {OTHER}"], HEAD, False),  # notes at HEAD -> allow
        ([], HEAD, False),                                                    # nothing to push
        (["", "   "], HEAD, False),                                           # blank lines only
        ([f"refs/heads/main {HEAD} refs/heads/main {OTHER}"], None, False),  # HEAD unknown
        ([f"refs/heads/x {OTHER} refs/heads/y {Z40}", f"refs/heads/m {HEAD} refs/heads/n {OTHER}"], HEAD, True),  # HEAD among several
        (["garbage"], HEAD, True),                                            # malformed non-empty -> conservative (gemini F2)
        ([f"only three {HEAD}"], HEAD, True),                                 # <4 fields -> conservative
    ]
    push_cases.extend([
        ([f"{HEAD} {HEAD} refs/heads/from-sha {Z40}"], HEAD, True),
        ([f"refs/tags/at-head {HEAD} refs/heads/from-tag {Z40}"], HEAD, True),
        ([f"refs/heads/main {HEAD} refs/tags/from-branch {Z40}"], HEAD, False),
        ([f"HEAD {HEAD} refs/tags/from-head {Z40}"], HEAD, False),
        (["garbage garbage garbage garbage"], HEAD, True),
        ([f"refs/heads/x {OTHER} refs/heads/y {Z40} extra"], HEAD, True),
        ([f"refs/heads/x {'g' * 40} refs/heads/y {Z40}"], HEAD, True),
        ([f"refs/heads/x {OTHER} refs/heads/y invalid"], HEAD, True),
        ([f"garbage {OTHER} refs/heads/y {Z40}"], HEAD, True),
        ([f"refs/heads/.bad {OTHER} refs/heads/y {Z40}"], HEAD, True),
        ([f"refs/heads/x {OTHER} refs/heads/bad..name {Z40}"], HEAD, True),
        ([f"refs/heads/x {OTHER} refs/tags/x {'0' * 64}"], HEAD, True),
        ([f"(delete) {Z40} garbage {OTHER}"], HEAD, True),
        ([f"(delete) {OTHER} refs/heads/y {Z40}"], HEAD, True),
        ([f"refs/heads/x {Z40} refs/heads/y {OTHER}"], HEAD, True),
        ([
            f"refs/heads/x {OTHER} refs/heads/y {Z40}",
            "garbage garbage garbage garbage",
        ], HEAD, True),
        ([f"HEAD {'a' * 64} refs/heads/x {'0' * 64}"], "a" * 64, True),
        ([f"HEAD {'a' * 64} refs/tags/x {'0' * 64}"], "a" * 64, False),
        # Unicode-whitespace ref names are VALID git refs and must not falsely trigger (codex P2):
        ([f"refs/heads/old\u00a0branch {OTHER} refs/heads/old\u00a0branch {Z40}"], HEAD, False),  # older branch (not HEAD) -> no check
        ([f"refs/heads/main {HEAD} refs/tags/dest\u00a0tag {Z40}"], HEAD, False),  # HEAD -> tag dest -> no check
        ([f"refs/heads/main {HEAD} refs/heads/uni\u00a0branch {Z40}"], HEAD, True),  # HEAD -> valid unicode-ws branch -> check
        ([f"refs/heads/main {HEAD} refs/heads/uni\u2028branch {Z40}"], HEAD, True),  # U+2028 line-sep inside a valid ref -> check, not split
    ])
    for i, (lines, hs, exp) in enumerate(push_cases):
        if head_is_pushed(lines, hs) != exp:
            failures.append(f"head_is_pushed case {i}: expected {exp}")

    saved_override = os.environ.get(_OVERRIDE)
    try:
        for val, exp in [(None, False), ("", False), (" ", True), ("1", True)]:
            if val is None:
                os.environ.pop(_OVERRIDE, None)
            else:
                os.environ[_OVERRIDE] = val
            if _allow_dirty_env() != exp:
                failures.append(f"override {val!r}: expected {exp}")
    finally:
        if saved_override is None:
            os.environ.pop(_OVERRIDE, None)
        else:
            os.environ[_OVERRIDE] = saved_override

    total = len(decide_cases) + len(push_cases) + 5
    try:
        total += _integration_self_test()
    except Exception as exc:
        failures.append(f"integration: {exc}")
    if failures:
        for f in failures:
            print("SELF-TEST FAIL:", f, file=sys.stderr)
        print(f"check-dirty-tree-push self-test: {len(failures)} FAIL", file=sys.stderr)
        return 1
    print(f"check-dirty-tree-push self-test: {total}/{total} pass")
    return 0


def main(argv):
    if argv[1:] == ["--self-test"]:  # 3b50b2f: only the documented forms are accepted; anything else is a usage error (exit 2)
        return _self_test()
    if len(argv) > 1 and argv[1] == "--pre-push":
        # git passes the remote name and URL to a pre-push hook: at most two positionals. A remote
        # name may legitimately begin with '-', and this hook reads stdin, never these arguments.
        extra = argv[2:]
        if len(extra) > 2:
            print("usage: check-dirty-tree-push.py --pre-push [<remote> <url>]", file=sys.stderr)
            return 2
        return _pre_push()
    if len(argv) > 1:
        print("usage: check-dirty-tree-push.py [--pre-push [<remote> <url>] | --self-test]",
              file=sys.stderr)
        return 2
    # No-arg: unconditional tree check (manual parity with pre-push-guard.sh).
    return _check_tree()


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as exc:  # fail-closed on any unexpected error
        print(f"check-dirty-tree-push: refusing on unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
