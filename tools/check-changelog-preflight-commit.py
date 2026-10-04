#!/usr/bin/env python3
"""Git-native pre-commit check: refuse a commit that stages CHANGELOG.md while
tools/preflight-changelog.py --staged fails (2026-09-30).

Why a git hook. The preflight gates a commit only when it is chained as
`python3 tools/preflight-changelog.py && git commit`. Twice in one session the chain was
written with ';', which runs the commit whatever the preflight's exit status, so a failing preflight
did not stop the commit. git runs pre-commit inside every commit, in the committing worktree, with
the index being committed, however the command was spelled.

Why pre-commit and not commit-msg. check-version-bump-commit.py is a commit-msg hook because its
opt-out is a line in the commit MESSAGE; this check has no message opt-out, so it runs before the
message is written, from the tracked tools/git-hooks/pre-commit after check-commit-on-main.py and
check-generated-commit.py. The dispatcher that tools/install-git-hooks.sh installs execs that tracked
file, so a clone that has run the installer gets this check with no re-install.

What it checks. When the index being committed carries a non-deleted root CHANGELOG.md change, it
runs the ACTIVE checkout's tools/preflight-changelog.py --staged (the preflight itself, not a copy of
its rules) and refuses unless it exits 0, relaying the preflight's report; a pass prints nothing. The
preflight inherits the hook's environment, so it diffs the index git named in GIT_INDEX_FILE (the one
`git commit -a` or `git commit <path>` is about to commit). Its diff of a mirror kept in ANOTHER
repository (the operational store or the private sibling) runs without the variables that
`git rev-parse --local-env-vars` names as local to one repository (GIT_INDEX_FILE and GIT_DIR among
them), so it reads that repository's own index (3b141 QA r2: under `git commit -a` it read this
repository's temporary index there, found no staged mirror addition, and let a failing commit
through). The preflight's own `git diff` overrides
every setting that would reshape what it parses (an external diff driver, textconv, a -diff or binary
attribute, colour, the `+++ b/` prefix) and exits 2 when that diff fails, rather than finding no added
line and passing (3b141 QA r1). This check's own `git diff` passes --no-ext-diff and --no-textconv too
(its --name-only output uses neither today). Diff presentation settings are also pinned for both,
appended last to GIT_CONFIG_PARAMETERS (the channel `git -c` uses; the last value wins):
diff.noprefix, diff.mnemonicPrefix, diff.srcPrefix/dstPrefix and color.diff=always each reshape the
`+++ b/` headers or `+` lines the preflight parses. GIT_CONFIG_PARAMETERS is local to one repository
too, so the pins do not reach the mirror diff in another repository; there the preflight's own flags
override the same settings.

Allowed without checking: the override GRC_ALLOW_FAILING_CHANGELOG_COMMIT=1, honoured only when the
value is exactly "1" (as the GRC_ALLOW_BULK_ADD and GRC_ALLOW_PR_ATTRIBUTION hooks read theirs), so
"0", "false" or an empty value is not the override (3b141 QA r1). A commit that does not stage
CHANGELOG.md is not judged, an initial commit on an unborn HEAD included: there the staged state is
read against the empty tree, as there is no HEAD to diff against (3b141 QA r4). A commit that concludes a
conflicted merge, cherry-pick, or revert is checked like any other (3b141 QA r1), whether `git commit`
or `git merge|cherry-pick|revert --continue` makes it (each runs pre-commit; a rebase does not, see
the residue below): CHANGELOG.md is the file most likely to conflict (every PR adds an entry in the
same place), so the resolution is a hand edit of exactly the kind this check exists for. The other
side's added lines, when they come from main, have already passed the D3, D7 and link-coverage
gates, so they rarely refuse, and the override covers the rest. check-version-bump-commit.py exempts
these commits because a Version bump belongs to a PR, which a merge does not have; a dash belongs to
a line, which it does. It REFUSES, naming the override (ignorance refuses, as in
check-version-bump-commit.py): a git error while reading the staged state; a staged CHANGELOG.md on
an unborn HEAD (the preflight diffs against HEAD, so it has nothing to check against and exits 2);
a staged CHANGELOG.md in a checkout without tools/preflight-changelog.py (3b141 QA r4: this once
failed open, silently, for an "older branch", but no older branch reaches this check: the tracked
shim runs it only in a tree that carries it, and the preflight predates it, so only a working tree
that has deleted or renamed the preflight gets here); and a preflight that cannot be started or
exits other than 0 (its 1 is a finding or a crash, its 2 a git error or a gate-2 language
engine it could not load or use).

Residue, stated: the preflight's full detailed-mirror link scan runs on every call, so a dangling link
in the mirror refuses a CHANGELOG commit that did not touch the mirror (as the `&&` chain does; fix
the link or use the override); the preflight resolves link targets, and runs that scan, in the WORKING
TREE, not the index, so a staged link to a file that exists only unstaged passes here and a target
deleted only in the working tree refuses; a mirror kept in ANOTHER repository is judged by what is
staged in that repository's own index, whatever this commit's `-a` or pathspec (that repository's own
commits are outside this hook); `git commit --amend` checks only what the amend adds to HEAD, as the
preflight does; a merge that git commits itself (a clean `git merge` runs pre-merge-commit, not
pre-commit) is not checked; nor is a commit that git's sequencer makes itself, for which git runs no
pre-commit hook (3b141 QA r2): every `git rebase` pick, including one concluded by
`git rebase --continue` after a CHANGELOG.md conflict, a cherry-pick or revert that applies
cleanly, and a `git am` commit (git am runs pre-applypatch, not pre-commit). No hook can refuse those commits (post-rewrite runs after they exist). A conflict resolved at
a rebase stop IS checked when `git commit` concludes it before `git rebase --continue`, and a root
CHANGELOG.md dash that a rebase carries still meets the D3 delta gate (tools/run-pr-time-checks.sh,
which the pre-push guard runs, and CI). `--no-verify` skips the hook; and it guards nothing until
tools/install-git-hooks.sh has installed the pre-commit shim in the clone.
"""
import os
import subprocess
import sys
from pathlib import Path

_OVERRIDE = "GRC_ALLOW_FAILING_CHANGELOG_COMMIT"
_CHANGELOG = "CHANGELOG.md"
_PREFLIGHT = Path("tools") / "preflight-changelog.py"
# Each overrides the repository, global, and earlier `git -c` value of its key (the last value wins).
_PINNED = ("diff.noprefix=false", "diff.mnemonicPrefix=false", "diff.srcPrefix=a/", "diff.dstPrefix=b/",
           "color.diff=never")


def override_set(environ):
    """PURE. The override is honoured only when its value is exactly "1", as the GRC_ALLOW_BULK_ADD and
    GRC_ALLOW_PR_ATTRIBUTION hooks read theirs (3b141 QA r1: any non-empty value, "0" included, once
    skipped the check)."""
    return environ.get(_OVERRIDE) == "1"


def decide(allow, ok, staged, code):
    """PURE. Returns (exit_code, stderr_message).

    allow: override set; ok: the staged state was read; staged: the index carries a non-deleted
    CHANGELOG.md change (meaningful only when ok); code: the preflight's exit code, or None when it
    could not be started (meaningful only when staged). A merge, cherry-pick or revert conclusion is
    decided like any other commit (see the module docstring)."""
    if allow:
        return 0, (f"check-changelog-preflight-commit: NOTE: {_OVERRIDE}=1 is set; skipping the CHANGELOG "
                   "preflight check.")
    if not ok:
        return 1, ("check-changelog-preflight-commit: REFUSING the commit: the staged state could not be "
                   "read (or HEAD is unborn, so the preflight has no diff to check), so it is unknown "
                   f"whether the staged {_CHANGELOG} passes tools/preflight-changelog.py. "
                   f"Deliberate override: {_OVERRIDE}=1.")
    if not staged or code == 0:
        return 0, ""
    if code == 1:
        return 1, ("check-changelog-preflight-commit: REFUSING the commit: tools/preflight-changelog.py "
                   f"--staged failed on the staged {_CHANGELOG} (exit 1; its report is above). Fix the "
                   f"reported lines, `git add {_CHANGELOG}`, and commit again. "
                   f"Deliberate override: {_OVERRIDE}=1.")
    how = "it could not be started" if code is None else f"exit {code}"
    return 1, ("check-changelog-preflight-commit: REFUSING the commit: tools/preflight-changelog.py "
               f"--staged did not complete ({how}), so it is unknown whether the staged {_CHANGELOG} "
               f"passes it. Deliberate override: {_OVERRIDE}=1.")


def pinned_env(environ):
    """PURE. The environment for the git commands this check and the preflight run: _PINNED appended
    LAST to GIT_CONFIG_PARAMETERS, every other variable (GIT_INDEX_FILE above all) kept as git gave it."""
    env = dict(environ)
    pins = " ".join(f"'{kv}'" for kv in _PINNED)
    prior = env.get("GIT_CONFIG_PARAMETERS")
    env["GIT_CONFIG_PARAMETERS"] = f"{prior} {pins}" if prior else pins
    return env


def _git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True,
                          env=pinned_env(os.environ)).stdout


def head_born(root):
    """Thin observer: True when HEAD names a commit, False when HEAD is unborn (a branch with no commit
    yet, as at an initial commit). A HEAD that is neither (a detached HEAD naming no commit) raises."""
    cp = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "-q", "HEAD^{commit}"],
                        capture_output=True, text=True, env=pinned_env(os.environ))
    if cp.returncode == 0:
        return True
    _git(root, "symbolic-ref", "-q", "HEAD")
    return False


def changelog_staged(root):
    """Thin observer: does the index being committed carry a non-deleted CHANGELOG.md change? It reads
    the index named in GIT_INDEX_FILE against HEAD, or against the empty tree when HEAD is unborn, so an
    initial commit that does not stage CHANGELOG.md is not judged (3b141 QA r4). A git error raises
    (ignorance refuses), and so does a staged CHANGELOG.md on an unborn HEAD, which the preflight
    (diffing against HEAD) cannot check. --no-ext-diff and --no-textconv are passed although
    --name-only output uses neither today."""
    born = head_born(root)
    base = "HEAD" if born else _git(root, "hash-object", "-t", "tree", os.devnull).strip()
    names = _git(root, "diff", "--cached", "--name-only", "--no-ext-diff", "--no-textconv", "--no-renames",
                 "--diff-filter=d", "-z", base, "--", _CHANGELOG).split("\0")
    if _CHANGELOG not in names:
        return False
    if not born:
        raise RuntimeError("HEAD is unborn, so the preflight has no diff to check")
    return True


def run_preflight(root):
    """(exit_code, report) of the ACTIVE checkout's preflight on the staged diff; (None, reason) when it
    could not be started, as in a checkout without it (3b141 QA r4: that once failed open, silently)."""
    if not (root / _PREFLIGHT).is_file():
        return None, f"check-changelog-preflight-commit: {_PREFLIGHT.as_posix()} is not in this checkout."
    try:
        cp = subprocess.run([sys.executable, str(root / _PREFLIGHT), "--staged"], cwd=root,
                            capture_output=True, text=True, env=pinned_env(os.environ))
    except OSError as exc:
        return None, str(exc)
    return cp.returncode, (cp.stdout + cp.stderr).strip()


def _pre_commit():
    allow = override_set(os.environ)
    staged = False
    code, report = None, ""
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                             check=True).stdout.strip()
        root = Path(top)
        if not allow:  # the override skips the preflight run, not only its verdict
            staged = changelog_staged(root)
            if staged:
                code, report = run_preflight(root)
        ok = True
    except Exception:
        ok = False
    rc, msg = decide(allow, ok, staged, code)
    if rc and report:
        print(report, file=sys.stderr)
    if msg:
        print(msg, file=sys.stderr)
    return rc


def _integration_self_test():
    """End to end: a real repository under a spaced path, the real installer, the real preflight, and
    real commits. Returns (failures, number of checks)."""
    import shutil
    import tempfile
    src = Path(__file__).resolve().parents[1]
    failures, checks = [], []

    def expect(cond, message):
        checks.append(message)
        if not cond:
            failures.append(message)

    with tempfile.TemporaryDirectory() as base:
        repo = Path(base) / "clone with space" / "r"
        for rel in ("tools/check-changelog-preflight-commit.py", "tools/check-commit-on-main.py",
                    "tools/install-git-hooks.sh", "tools/git-hooks/pre-commit", str(_PREFLIGHT),
                    "tools/check-changelog-length-on-pr.py", "tools/lint_common.py",
                    "tools/aiqt_bootstrap.py", "tools/lint-language.py",
                    ".corpus-management/tools/gate_lint_language.py",
                    ".corpus-management/tools/profile_loader.py",
                    ".corpus-management/defaults/grc/language.toml"):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src / rel, repo / rel)
        # Isolated from the caller: no inherited GIT_* (GIT_INDEX_FILE above all), no global or system
        # config, and no GRC_STORE (it would point the preflight's mirror scan at the real mirror). The
        # fixture does not carry the vendored AIQT pack the preflight imports, so it is named here.
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")
               and k not in (_OVERRIDE, "GRC_ALLOW_MAIN_COMMIT", "GRC_STORE")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid",
                   AIQT_PACK_ROOT=str(src / "vendor" / "aiqt"))

        def run(args, cwd=repo, extra=None):
            return subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True, text=True,
                                  env={**env, **(extra or {})})

        def must(args, cwd=repo):
            cp = run(args, cwd=cwd)
            if cp.returncode != 0:
                failures.append(f"fixture step failed: {' '.join(map(str, args))}: {cp.stderr.strip()}")
            return cp

        def refused(cp, reason="--staged failed on the staged"):
            """The check refused for REASON: by default the preflight's finding (its exit 1), so a case
            expecting that finding fails when the check refused for another reason instead, a git error
            reading the staged state or a preflight that did not complete (3b141 QA r2)."""
            return (cp.returncode != 0 and "check-changelog-preflight-commit: REFUSING" in cp.stderr
                    and reason in cp.stderr)

        changelog = repo / _CHANGELOG
        clean, dashed = "a clean entry\n", "a dashed entry \u2014 here\n"

        def append(line, path=changelog):
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(line)

        must(["git", "init", "-q", "-b", "feature"])
        must(["git", "config", "commit.gpgsign", "false"])
        cp = run(["sh", "tools/install-git-hooks.sh"])
        expect(cp.returncode == 0, f"the installer failed: {cp.stderr.strip()}")
        # An initial commit on an unborn HEAD that does not stage CHANGELOG.md is not judged (3b141 QA
        # r4: reading the staged state against HEAD, which an unborn branch lacks, would refuse it). It
        # is made on another branch, so that feature stays unborn for the case after it.
        must(["git", "symbolic-ref", "HEAD", "refs/heads/first"])
        # The gate-2 engine the preflight loads is committed with tools/, so a linked worktree carries
        # it (3b201: untracked, it was absent there, and that case passed on the preflight's crash).
        must(["git", "add", "tools", ".corpus-management"])
        cp = run(["git", "commit", "-q", "-m", "first"])
        expect(cp.returncode == 0 and "check-changelog" not in cp.stderr,
               f"an unborn initial commit not staging CHANGELOG.md was refused or not silent: {cp.stderr.strip()}")
        must(["git", "symbolic-ref", "HEAD", "refs/heads/feature"])
        changelog.write_text("# Changelog\n\n", encoding="utf-8")
        must(["git", "add", "tools", _CHANGELOG])
        cp = run(["git", "commit", "-q", "-m", "init"])
        expect(refused(cp, "could not be read") and _OVERRIDE in cp.stderr,
               "a staged CHANGELOG.md on an unborn HEAD was not refused")
        # The preflight itself fails closed on a git error (3b141 QA r1): `git diff HEAD` on an unborn
        # HEAD fails, which it once reported as 0 added lines and a pass (exit 0).
        for args in ([], ["--staged"]):
            cp = run([sys.executable, _PREFLIGHT, *args])
            expect(cp.returncode == 2 and "git diff failed" in cp.stderr,
                   f"the preflight {args} did not exit 2 on a git error: exit {cp.returncode}")
        cp = run(["git", "commit", "-q", "-m", "init"], extra={_OVERRIDE: "1"})
        expect(cp.returncode == 0 and "NOTE" in cp.stderr,
               f"the override did not allow the commit: {cp.stderr.strip()}")
        # The motivating shape: a ';' join runs the commit whatever the preflight's exit status.
        append(dashed)
        must(["git", "add", _CHANGELOG])
        cp = run(["sh", "-c", "python3 tools/preflight-changelog.py --staged; git commit -q -m dashed"])
        expect(refused(cp), "a ';'-joined commit after a failing preflight was not refused")
        cp = run(["git", "commit", "-q", "-m", "dashed"])
        expect(refused(cp) and "em/en dash in prose" in cp.stderr and _OVERRIDE in cp.stderr,
               "a staged CHANGELOG dash was not refused with the preflight's report and the override")
        cp = run(["git", "commit", "-q", "-m", "dashed"], extra={_OVERRIDE: "0"})
        expect(refused(cp), f"{_OVERRIDE}=0 was taken as the override")
        # A gate-2 spelling in a staged entry refuses with the preflight's report too (3b201).
        changelog.write_text("# Changelog\n\na centralised entry\n", encoding="utf-8")
        must(["git", "add", _CHANGELOG])
        cp = run(["git", "commit", "-q", "-m", "spelling"])
        expect(refused(cp) and "gate 2 spelling [ise]: centralised" in cp.stderr,
               f"a staged CHANGELOG -ise spelling was not refused with the preflight's report: {cp.stderr.strip()}")
        # Only the staged diff is judged: an unstaged dash is not this commit's, and a pass is silent.
        changelog.write_text("# Changelog\n\n" + clean, encoding="utf-8")
        must(["git", "add", _CHANGELOG])
        append(dashed)
        cp = run(["git", "commit", "-q", "-m", "clean"])
        expect(cp.returncode == 0 and "OK:" not in cp.stderr and "check-changelog" not in cp.stderr,
               f"a clean staged entry was refused or not silent beside an unstaged dash: {cp.stderr.strip()}")
        # GIT_INDEX_FILE: `commit -a` and a pathspec commit commit an index other than .git/index.
        cp = run(["git", "commit", "-q", "-a", "-m", "all"])
        expect(refused(cp), "`git commit -a` carrying a CHANGELOG dash was not refused")
        cp = run(["git", "commit", "-q", "-m", "only", "--", _CHANGELOG])
        expect(refused(cp), "`git commit -- CHANGELOG.md` carrying a CHANGELOG dash was not refused")
        # Presentation settings that reshape the preflight's diff cannot hide the dash.
        must(["git", "add", _CHANGELOG])
        for key, value in (("diff.noprefix", "true"), ("diff.mnemonicPrefix", "true"),
                           ("diff.dstPrefix", "x/"), ("color.diff", "always")):
            must(["git", "config", key, value])
            cp = run(["git", "commit", "-q", "-m", key])
            expect(refused(cp), f"{key}={value} hid a staged CHANGELOG dash from the preflight")
            must(["git", "config", "--unset", key])
        cp = run(["git", "-c", "diff.noprefix=true", "commit", "-q", "-m", "git -c"])
        expect(refused(cp), "`git -c diff.noprefix=true commit` hid a staged CHANGELOG dash from the preflight")
        # Settings that hand the preflight's diff to something else cannot hide the dash either (3b141
        # QA r1): an external diff driver that succeeds silently (as difftastic succeeds with its own
        # format), a textconv filter, and a -diff attribute ("Binary files ... differ").
        attributes = repo / ".git" / "info" / "attributes"
        attributes.parent.mkdir(parents=True, exist_ok=True)
        for what, config, attrs, extra in (
                ("diff.external", ("diff.external", "true"), None, None),
                ("GIT_EXTERNAL_DIFF", None, None, {"GIT_EXTERNAL_DIFF": "true"}),
                ("a textconv filter", ("diff.drv.textconv", "true"), f"{_CHANGELOG} diff=drv\n", None),
                ("a -diff attribute", None, f"{_CHANGELOG} -diff\n", None)):
            if config:
                must(["git", "config", *config])
            if attrs:
                attributes.write_text(attrs, encoding="utf-8")
            cp = run(["git", "commit", "-q", "-m", what], extra=extra)
            expect(refused(cp), f"{what} hid a staged CHANGELOG dash from the preflight")
            if config:
                must(["git", "config", "--unset", config[0]])
            if attrs:
                attributes.unlink()
        must(["git", "restore", "--staged", _CHANGELOG])
        must(["git", "checkout", "--", _CHANGELOG])
        # The trigger is a staged CHANGELOG.md: the preflight's full-mirror scan fails on this dangling
        # link, which refuses a CHANGELOG commit and leaves every other commit alone.
        mirror = repo / ".working" / "changelog-details" / "CHANGELOG-detailed.md"
        mirror.parent.mkdir(parents=True)
        mirror.write_text("[gone](no-such-file.md)\n", encoding="utf-8")
        (repo / "other.txt").write_text("1\n", encoding="utf-8")
        must(["git", "add", "other.txt"])
        cp = run(["git", "commit", "-q", "-m", "no changelog"])
        expect(cp.returncode == 0, f"a commit not staging CHANGELOG.md was judged: {cp.stderr.strip()}")
        # The pins, appended to a caller's `git -c` values, parse in a real git (3b141 QA r2).
        (repo / "other.txt").write_text("1b\n", encoding="utf-8")
        must(["git", "add", "other.txt"])
        cp = run(["git", "-c", "diff.noprefix=true", "commit", "-q", "-m", "git -c, no changelog"])
        expect(cp.returncode == 0, f"`git -c` refused a commit not staging CHANGELOG.md: {cp.stderr.strip()}")
        append(clean)
        must(["git", "add", _CHANGELOG])
        cp = run(["git", "commit", "-q", "-m", "mirror"])
        expect(refused(cp) and "dangling markdown-link target" in cp.stderr,
               "the preflight's full-mirror finding did not refuse a CHANGELOG commit")
        shutil.rmtree(repo / ".working")
        must(["git", "commit", "-q", "-m", "clean again"])
        # A commit concluding a conflicted merge is checked (3b141 QA r1): CHANGELOG.md is the file most
        # likely to conflict, and its resolution is typed by hand.
        must(["git", "switch", "-q", "-c", "side"])
        append("side entry\n")
        must(["git", "commit", "-q", "-a", "-m", "side"])
        must(["git", "switch", "-q", "feature"])
        append("feature entry\n")
        must(["git", "commit", "-q", "-a", "-m", "feature"])
        run(["git", "merge", "--no-edit", "side"])
        expect(run(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"]).returncode == 0,
               "the merge fixture did not stop on a CHANGELOG.md conflict")
        merged = changelog.read_text(encoding="utf-8")
        ours = merged[:merged.index("<" * 7)] + "feature entry\n"
        changelog.write_text(ours + "side entry \u2014 resolved\n", encoding="utf-8")
        must(["git", "add", _CHANGELOG])
        cp = run(["git", "commit", "-q", "--no-edit"])
        expect(refused(cp), "a merge conclusion carrying a CHANGELOG dash was not refused")
        changelog.write_text(ours + "side entry resolved\n", encoding="utf-8")
        must(["git", "add", _CHANGELOG])
        must(["git", "commit", "-q", "--no-edit"])
        # The crux: a commit made with `git -C` in a LINKED worktree is checked too.
        linked = Path(base) / "wt"
        must(["git", "worktree", "add", "-q", "-b", "other", str(linked)])
        append(dashed, linked / _CHANGELOG)
        must(["git", "-C", str(linked), "add", _CHANGELOG])
        cp = run(["git", "-C", str(linked), "commit", "-q", "-m", "worktree"], cwd=base)
        expect(refused(cp) and "em/en dash in prose" in cp.stderr,
               "a CHANGELOG dash committed with git -C in a linked worktree was not refused")
        # A mirror kept in a SEPARATE repository (the operational store, <repo-parent>/private) is
        # judged by that repository's own index (3b141 QA r2): the hook's GIT_INDEX_FILE, which
        # `commit -a` and a pathspec commit point at this repository's temporary index, once reached
        # the mirror's diff, so a staged mirror dash that the standalone preflight refuses passed.
        store = repo.parent / "private"
        store_mirror = store / "changelog-details" / "CHANGELOG-detailed.md"
        store_mirror.parent.mkdir(parents=True)
        store_mirror.write_text("# Detailed\n\n", encoding="utf-8")
        must(["git", "init", "-q", "-b", "store"], cwd=store)
        must(["git", "config", "commit.gpgsign", "false"], cwd=store)
        must(["git", "add", "-A"], cwd=store)
        must(["git", "commit", "-q", "-m", "store"], cwd=store)
        append("a store entry \u2014 staged\n", store_mirror)
        must(["git", "add", "-A"], cwd=store)
        append(clean)
        cp = run([sys.executable, _PREFLIGHT, "--staged"])
        expect(cp.returncode == 1 and "em/en dash in prose" in cp.stderr,
               f"the standalone preflight did not report a staged store-mirror dash: exit {cp.returncode}")
        for how, args in (("commit -a", ["-a"]), ("commit -- CHANGELOG.md", ["--", _CHANGELOG]),
                          ("commit", None)):
            if args is None:
                must(["git", "add", _CHANGELOG])
            cp = run(["git", "commit", "-q", "-m", how, *(args or [])])
            expect(refused(cp) and "em/en dash in prose" in cp.stderr,
                   f"`git {how}` passed a dash staged in the store's mirror: {cp.stderr.strip()}")
        # A clean staged store entry passes beside an unstaged store dash: that repository's index,
        # not its working tree, is judged, and its diff runs cleanly under the hook.
        must(["git", "checkout", "-q", "HEAD", "--", "."], cwd=store)
        append("a clean store entry\n", store_mirror)
        must(["git", "add", "-A"], cwd=store)
        append("an unstaged store entry \u2014 here\n", store_mirror)
        cp = run(["git", "commit", "-q", "-m", "store clean"])
        expect(cp.returncode == 0 and "check-changelog" not in cp.stderr,
               f"a clean staged store-mirror entry was refused or not silent: {cp.stderr.strip()}")
        shutil.rmtree(store)
        # A gate-2 language engine the preflight cannot load refuses as a preflight that did not
        # complete, with the preflight's named reason rather than a traceback (3b201).
        engine = repo / ".corpus-management" / "tools" / "gate_lint_language.py"
        engine_text = engine.read_text(encoding="utf-8")
        engine.unlink()
        append(clean)
        must(["git", "add", _CHANGELOG])
        cp = run(["git", "commit", "-q", "-m", "no engine"])
        expect(refused(cp, "did not complete (exit 2)")
               and "gate-2 language engine could not be loaded" in cp.stderr
               and "Traceback" not in cp.stderr,
               f"a missing gate-2 language engine did not refuse with a named reason: {cp.stderr.strip()}")
        engine.write_text(engine_text, encoding="utf-8")
        # A preflight that does not complete refuses, and so does one that is absent (3b141 QA r4: that
        # once failed open, silently).
        preflight = repo / _PREFLIGHT
        real = preflight.read_text(encoding="utf-8")
        preflight.write_text("import sys\nsys.exit(2)\n", encoding="utf-8")
        append(clean)
        must(["git", "add", _CHANGELOG])
        cp = run(["git", "commit", "-q", "-m", "exit 2"])
        expect(refused(cp, "did not complete (exit 2)"), "a preflight exiting 2 did not refuse the commit")
        preflight.unlink()
        cp = run(["git", "commit", "-q", "-m", "no preflight"])
        expect(refused(cp, "could not be started") and "is not in this checkout" in cp.stderr,
               f"a checkout without the preflight did not refuse a staged CHANGELOG.md: {cp.stderr.strip()}")
        preflight.write_text(real, encoding="utf-8")
        # The tracked shim fails OPEN for a tree without this check (the other hooks' fixtures copy the
        # shim without it), and a commit-on-main refusal still stops the commit before this check runs.
        check = repo / "tools" / "check-changelog-preflight-commit.py"
        check.rename(repo / "moved-check.py")
        append(dashed)
        must(["git", "add", _CHANGELOG])
        cp = run(["git", "commit", "-q", "-m", "no check"])
        expect(cp.returncode == 0, f"the shim did not fail open without this check: {cp.stderr.strip()}")
        (repo / "moved-check.py").rename(check)
        must(["git", "switch", "-q", "-c", "main"])
        (repo / "other.txt").write_text("2\n", encoding="utf-8")
        must(["git", "add", "other.txt"])
        cp = run(["git", "commit", "-q", "-m", "on main"])
        expect(cp.returncode != 0 and "check-commit-on-main: REFUSING" in cp.stderr,
               "the shim ran on past a commit-on-main refusal")
    return failures, len(checks)


def _self_test():
    pins = pinned_env({"GIT_CONFIG_PARAMETERS": "'diff.noprefix=true'", "GIT_INDEX_FILE": "/i"})
    cases = [
        ("override allows a failing preflight", decide(True, True, True, 1)[0], 0),
        ("override allows an unreadable state", decide(True, False, False, None)[0], 0),
        ("unreadable state refuses", decide(False, False, False, None)[0], 1),
        ("no staged CHANGELOG.md allows", decide(False, True, False, None)[0], 0),
        ("a passing preflight allows", decide(False, True, True, 0)[0], 0),
        ("a failing preflight refuses", decide(False, True, True, 1)[0], 1),
        ("a preflight git error (exit 2) refuses", decide(False, True, True, 2)[0], 1),
        ("a preflight killed by a signal refuses", decide(False, True, True, -15)[0], 1),
        ("a preflight that could not start refuses", decide(False, True, True, None)[0], 1),
        ("every refusal names the override",
         all(_OVERRIDE in decide(False, *a)[1]
             for a in ((False, False, None), (True, True, 1), (True, True, 2))), True),
        ("the override is exactly 1", override_set({_OVERRIDE: "1"}), True),
        ("0 is not the override", override_set({_OVERRIDE: "0"}), False),
        ("an empty value is not the override", override_set({_OVERRIDE: ""}), False),
        ("the pins follow the caller's `git -c` values",
         pins["GIT_CONFIG_PARAMETERS"].startswith("'diff.noprefix=true' 'diff.noprefix=false'"), True),
        ("the pins stand alone without caller values",
         pinned_env({})["GIT_CONFIG_PARAMETERS"].startswith("'diff.noprefix=false'"), True),
        ("GIT_INDEX_FILE is kept for the preflight", pins.get("GIT_INDEX_FILE"), "/i"),
    ]
    failures = [f"{n}: got {g!r}, want {w!r}" for n, g, w in cases if g != w]
    integ, checks = _integration_self_test()
    failures += integ
    total = len(cases) + checks
    for f in failures:
        print(f"  FAIL: {f}")
    print(f"self-test: {total - len(failures)}/{total} passed" if not failures
          else f"self-test: FAILED ({len(failures)} of {total})")
    return 1 if failures else 0


def main(argv):
    if argv[1:] == ["--self-test"]:  # 3b50b2f: only the documented forms are accepted; anything else is a usage error (exit 2)
        return _self_test()
    if argv[1:] == ["--pre-commit"]:
        return _pre_commit()
    print("usage: check-changelog-preflight-commit.py --pre-commit | --self-test", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
