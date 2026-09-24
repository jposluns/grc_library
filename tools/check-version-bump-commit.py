#!/usr/bin/env python3
"""Git-native commit-msg check: refuse a commit whose staged versioned document changed its body
without its own Version change (P-TODO 3b25, 2026-09-24).

Why a git hook. The PreToolUse guard .claude/hooks/block-unbumped-version-commit.py resolves the
repository from its OWN location, so a commit made in a linked worktree (`git -C <worktree> commit`)
is never checked by it: on 2026-09-24 three worktree commits changed document bodies without their
per-commit bump and only gate 40 caught them, at pre-push. git runs commit-msg inside every commit,
in the committing worktree, with that worktree's index, however the command was spelled.

Why commit-msg and not pre-commit. The sanctioned opt-out is a `VersionBump: none <reason>` line in the
commit MESSAGE, which does not exist yet when pre-commit runs.

What it checks (the same rule as the PreToolUse guard, from the same source: the guard's pure
functions are LOADED from .claude/hooks/block-unbumped-version-commit.py, not copied). A staged
Markdown file whose STAGED content carries a `**Version:**` line, outside the generated artefacts and
.corpus-management/, is versioned; an offender is a versioned file whose staged diff changes its body
but not its Version line. This hook REFUSES and never auto-bumps: the PreToolUse guard auto-bumps
same-checkout commits before git runs, and a git hook that rewrites the index mid-commit is riskier
than a refusal naming the fix.

Allowed without checking: a commit that concludes a merge, cherry-pick, or revert (the staged diff
then carries other commits' changes); a message carrying `VersionBump: none <reason>` (comment lines
ignored); the override GRC_ALLOW_UNBUMPED_COMMIT=1. A checkout without the guard file (older branch)
is allowed (fail OPEN, stated). A git error while checking REFUSES, naming the override (ignorance
refuses, as in check-commit-on-main.py).

Residue, stated: `git commit --amend` is indistinguishable here, and an amend whose earlier commit
already bumped can be refused (use the opt-out or the override); `--no-verify` skips the hook; and it
guards nothing until tools/install-git-hooks.sh has installed the commit-msg shim in the clone.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

_OVERRIDE = "GRC_ALLOW_UNBUMPED_COMMIT"
_GUARD = Path(".claude") / "hooks" / "block-unbumped-version-commit.py"
_SEQUENCER = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD")


def decide(allow, sequencer, opt_out, ok, bad):
    """PURE. Returns (exit_code, stderr_message).

    allow: override set; sequencer: concluding a merge/cherry-pick/revert; opt_out: the message carries
    the opt-out; ok: the staged state was read; bad: the offender paths (meaningful only when ok)."""
    if allow:
        return 0, f"check-version-bump-commit: NOTE: {_OVERRIDE} is set; skipping the Version-bump check."
    if sequencer or opt_out:
        return 0, ""
    if not ok:
        return 1, ("check-version-bump-commit: REFUSING the commit: the staged state could not be read, so "
                   f"it is unknown whether a Version bump is missing. Deliberate override: {_OVERRIDE}=1.")
    if bad:
        return 1, ("check-version-bump-commit: REFUSING the commit: these staged documents changed their body "
                   f"without a Version change: {', '.join(sorted(bad))}. Bump **Version:** (patch) and set "
                   "**Date:** to today (UTC) in the same edit, `git add` them, and commit again; a commit that "
                   "genuinely needs no bump carries a `VersionBump: none <reason>` line in its message. "
                   f"Deliberate override: {_OVERRIDE}=1.")
    return 0, ""


def load_guard(root):
    """The PreToolUse guard module, or None when this checkout predates it."""
    path = root / _GUARD
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("_vbump_guard", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SCISSORS = " ------------------------ >8 ------------------------"
_AUTO_COMMENT_CHARS = "#;@!$%^&|:"   # git's candidates for core.commentChar=auto


def read_message(path):
    """Read the message file as git wrote it: bytes decoded with NO newline translation, since
    read_text() turns a stray CR into a line break git never sees and can manufacture an opt-out
    line (3b25 r6, codex)."""
    return Path(path).read_bytes().decode("utf-8", errors="replace")


def message_opts_out(text, guard, comment_char="#"):
    """PURE. Does the message carry the opt-out? Mirrors git's strip cleanup: text from the exact
    scissors line down is dropped (`git commit -v` appends the diff there; 3b25 r1), and lines that
    begin with the comment character are dropped. For core.commentChar=auto git picks the character
    BEFORE editing and it cannot be recovered from the final message, so lines beginning with ANY of
    git's candidates are dropped: that can only IGNORE an opt-out (refuse), never count a stripped
    comment as one (3b25 r3, codex P1: hard-coding '#' let a ';' comment line falsely allow). Residue, stated:
    under --cleanup=whitespace or verbatim git KEEPS comment-looking lines and text below a scissors
    line, which this treats as removed, so an opt-out written there is ignored: that errs only toward
    REFUSING, never toward a false allow, and the override remains (3b25 r2 codex/gemini)."""
    chars = _AUTO_COMMENT_CHARS if comment_char == "auto" else (comment_char[:1] or "#")
    kept = []
    for line in text.split("\n"):   # git's lines are \n-only; splitlines() also splits on \v, NEL, U+2028 (3b25 r5 claude)
        if line[:1] and line[:1] in chars and line.rstrip() == line[:1] + _SCISSORS:
            break
        if line[:1] and line[:1] in chars:
            continue
        kept.append(line)
    # Line by line: OPT_OUT's `\s*` would otherwise match across a newline, so removing a comment line
    # between "VersionBump:" and "none" could MANUFACTURE an opt-out (3b25 r4, codex).
    return any(guard.OPT_OUT.search(line) for line in kept)


def _comment_char(root):
    cp = subprocess.run(["git", "-C", str(root), "config", "--get", "core.commentChar"],
                        capture_output=True, text=True)
    return cp.stdout.strip() or "#"


def _gitz(guard, root, *args):
    """git diff plumbing with presentation settings pinned, so user config cannot reshape the output."""
    return guard.git(root, "-c", "diff.noprefix=false", "-c", "core.quotePath=false", *args)


def staged_offenders(root, guard):
    """Thin observer, PER FILE, from STAGED content (3b25 r1 codex): no diff-header parsing (so
    diff.noprefix, quoted names, and paths containing ' b/' cannot hide an offender); a rename is
    diffed old->new so a renamed document with a body edit is not mistaken for a new one; only a
    structurally reported deletion is skipped, and any other read failure raises (ignorance refuses)."""
    # --raw carries the index modes, so a submodule (gitlink, mode 160000) at a *.md path is
    # skipped rather than read as a document blob (3b25 r2 codex/gemini).
    raw = _gitz(guard, root, "diff", "--cached", "--raw", "-M", "-z").split("\0")
    entries, k = [], 0
    while k < len(raw) and raw[k]:
        meta = raw[k].split()
        dst_mode, status = meta[1], meta[4]
        if status[:1] in "RC":
            entries.append((status[:1], dst_mode, raw[k + 1], raw[k + 2])); k += 3
        else:
            entries.append((status[:1], dst_mode, None, raw[k + 1])); k += 2
    bad = []
    for status, dst_mode, old, new in entries:
        if status == "D" or dst_mode == "160000" or not new.endswith(".md") \
                or new in guard.GENERATED or new.startswith(".corpus-management/"):
            continue
        text = guard.git(root, "show", f":{new}")   # a non-deleted entry must be readable
        if not guard.VERSION_LINE.search(text):
            continue
        paths = [old, new] if old else [new]
        diff = _gitz(guard, root, "diff", "--cached", "-M", "--no-ext-diff", "--no-color",
                     "--no-textconv", "--unified=0", "--", *paths)
        body, version = guard.classify_hunk(guard._lf_lines(diff))
        if body and not version:
            bad.append(new)
    return bad


def _in_sequencer(root):
    for name in _SEQUENCER:
        cp = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-path", name],
                            capture_output=True, text=True)
        p = Path(cp.stdout.strip())
        if cp.returncode == 0 and (p if p.is_absolute() else root / p).exists():
            return True
    return False


def _commit_msg(msgfile):
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                             check=True).stdout.strip()
        root = Path(top)
        guard = load_guard(root)
        if guard is None:
            return 0
        text = read_message(msgfile)
        sequencer, opt_out = _in_sequencer(root), message_opts_out(text, guard, _comment_char(root))
        bad = [] if (sequencer or opt_out) else staged_offenders(root, guard)
        ok = True
    except Exception:
        sequencer = opt_out = False
        bad, ok = [], False
    code, msg = decide(bool(os.environ.get(_OVERRIDE)), sequencer, opt_out, ok, bad)
    if msg:
        print(msg, file=sys.stderr)
    return code


def _integration_self_test():
    """End to end: a real repository under a spaced path, the real installer, real commits."""
    import shutil
    import tempfile
    src = Path(__file__).resolve().parents[1]
    failures = []
    with tempfile.TemporaryDirectory() as base:
        repo = Path(base) / "clone with space" / "r"
        for rel in ("tools/check-version-bump-commit.py", "tools/check-commit-on-main.py",
                    "tools/install-git-hooks.sh", "tools/git-hooks/pre-commit",
                    "tools/git-hooks/pre-push", "tools/git-hooks/commit-msg", str(_GUARD)):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src / rel, repo / rel)
        env = {k: v for k, v in os.environ.items()
               if not k.startswith("GIT_") and k not in (_OVERRIDE, "GRC_ALLOW_MAIN_COMMIT")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid")

        def run(args, cwd=repo, extra=None):
            return subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True, text=True,
                                  env={**env, **(extra or {})})

        def must(args, cwd=repo):
            cp = run(args, cwd=cwd)
            if cp.returncode != 0:
                failures.append(f"fixture step failed: {' '.join(map(str, args))}: {cp.stderr.strip()}")
            return cp

        def doc(path, version, body):
            (path).parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"**Version:** {version}\\\n**Date:** 2026-01-01\\\n\n---\n\n{body}\n")

        must(["git", "init", "-q", "-b", "feature"])
        must(["git", "config", "commit.gpgsign", "false"])
        # A local (unmanaged) commit-msg hook is refused until renamed to commit-msg-local, then chained.
        hooks = Path(must(["git", "rev-parse", "--git-path", "hooks"]).stdout.strip())
        hooks = hooks if hooks.is_absolute() else repo / hooks
        hooks.mkdir(parents=True, exist_ok=True)
        local = hooks / "commit-msg"
        local.write_text("#!/bin/sh\necho 'local hook ran' >> \"$1\"\n")
        local.chmod(0o755)
        cp = run(["sh", "tools/install-git-hooks.sh"])
        if cp.returncode == 0 or "commit-msg-local" not in cp.stderr:
            failures.append("a foreign commit-msg hook was not refused with the .local migration step")
        local.rename(hooks / "commit-msg-local")
        cp = run(["sh", "tools/install-git-hooks.sh"])
        if cp.returncode != 0:
            failures.append(f"installer failed after the .local migration: {cp.stderr.strip()}")
        must(["git", "add", "tools", ".claude"])
        doc(repo / "d.md", "1.0.0", "first body")
        must(["git", "add", "d.md"])
        must(["git", "commit", "-q", "-m", "init"])
        if "local hook ran" not in must(["git", "log", "-1", "--format=%B"]).stdout:
            failures.append("the chained commit-msg-local hook did not run")
        doc(repo / "d.md", "1.0.0", "second body")
        must(["git", "add", "d.md"])
        cp = run(["git", "commit", "-q", "-m", "body only"])
        if cp.returncode == 0 or "without a Version change" not in cp.stderr:
            failures.append("a body-only change without a Version bump was not refused")
        cp = run(["git", "commit", "-q", "-m", "body only\n\nVersionBump: none (test)"])
        if cp.returncode != 0:
            failures.append(f"the VersionBump opt-out did not allow the commit: {cp.stderr.strip()}")
        doc(repo / "d.md", "1.0.1", "third body")
        must(["git", "add", "d.md"])
        cp = run(["git", "commit", "-q", "-m", "bumped"])
        if cp.returncode != 0:
            failures.append(f"a bumped change was refused: {cp.stderr.strip()}")
        doc(repo / "docs" / "maturity-scorecard.md", "1.0.0", "generated")
        must(["git", "add", "docs"])
        must(["git", "commit", "-q", "-m", "add scorecard"])
        doc(repo / "docs" / "maturity-scorecard.md", "1.0.0", "regenerated")
        must(["git", "add", "docs"])
        cp = run(["git", "commit", "-q", "-m", "regen"])
        if cp.returncode != 0:
            failures.append(f"a generated-artefact body change was refused: {cp.stderr.strip()}")
        # The crux: a commit made with `git -C` in a LINKED worktree is checked too.
        linked = Path(base) / "wt"
        must(["git", "worktree", "add", "-q", "-b", "other", str(linked)])
        doc(linked / "d.md", "1.0.1", "worktree body")
        must(["git", "-C", str(linked), "add", "d.md"])
        cp = run(["git", "-C", str(linked), "commit", "-q", "-m", "worktree body only"], cwd=base)
        if cp.returncode == 0 or "without a Version change" not in cp.stderr:
            failures.append("a body-only commit made with git -C in a linked worktree was not refused")
        cp = run(["git", "-C", str(linked), "commit", "-q", "-m", "override"], cwd=base,
                 extra={_OVERRIDE: "1"})
        if cp.returncode != 0:
            failures.append(f"the override did not allow the commit: {cp.stderr.strip()}")
        # --- 3b25 r1 regressions (codex, gemini, claude) ---
        # (a) diff.noprefix cannot hide an offender (no diff-header parsing any more).
        must(["git", "config", "diff.noprefix", "true"])
        doc(repo / "d.md", "1.0.1", "noprefix body")
        must(["git", "add", "d.md"])
        cp = run(["git", "commit", "-q", "-m", "noprefix"])
        if cp.returncode == 0 or "without a Version change" not in cp.stderr:
            failures.append("diff.noprefix=true hid an unbumped body change")
        must(["git", "config", "--unset", "diff.noprefix"])
        # (b) an opt-out below the scissors line (git commit -v) is not part of the message.
        msg = repo / "verbose-msg.txt"
        msg.write_text("subject\n\n# ------------------------ >8 ------------------------\n"
                       "+VersionBump: none (inside the appended diff)\n")
        cp = run(["git", "commit", "-q", "-F", str(msg), "--cleanup=scissors"])
        if cp.returncode == 0 or "without a Version change" not in cp.stderr:
            failures.append("an opt-out below the scissors line waived the check")
        # (c) a custom comment character: its comment lines are not the message either.
        must(["git", "config", "core.commentChar", ";"])
        msg.write_text("subject\n; VersionBump: none (a comment under ';')\n")
        cp = run(["git", "commit", "-q", "-F", str(msg), "--cleanup=strip"])
        if cp.returncode == 0 or "without a Version change" not in cp.stderr:
            failures.append("an opt-out in a custom-comment-character line waived the check")
        must(["git", "config", "--unset", "core.commentChar"])
        must(["git", "restore", "--staged", "d.md"]); must(["git", "checkout", "--", "d.md"])
        # (d) a rename with a body edit is diffed old -> new, not treated as a new document.
        must(["git", "mv", "d.md", "e.md"])
        doc(repo / "e.md", "1.0.1", "renamed and edited")
        must(["git", "add", "e.md"])
        cp = run(["git", "commit", "-q", "-m", "rename with body edit"])
        if cp.returncode == 0 or "without a Version change" not in cp.stderr:
            failures.append("a renamed document with an unbumped body edit was allowed")
        must(["git", "reset", "-q", "--hard"])
        # (e) a checkout OLDER than the tracked dispatcher still runs commit-msg-local.
        (repo / "tools" / "git-hooks" / "commit-msg").rename(repo / "moved-commit-msg")
        (repo / "f.txt").write_text("x\n")
        must(["git", "add", "f.txt"])
        must(["git", "commit", "-q", "-m", "older checkout"])
        if "local hook ran" not in must(["git", "log", "-1", "--format=%B"]).stdout:
            failures.append("commit-msg-local was skipped in a checkout without the tracked dispatcher")
    return failures


def _self_test():
    class _G:  # a stand-in guard exposing only OPT_OUT
        import re as _re
        OPT_OUT = _re.compile(r"VersionBump:\s*none\b", _re.I)
    import os as _os, tempfile as _tf
    _fd, _crp = _tf.mkstemp()
    _os.write(_fd, b"subject\n# junk\rVersionBump: none x\n"); _os.close(_fd)
    _cr_text = read_message(_crp); _os.unlink(_crp)
    cases = [
        ("a stray CR in a comment line is not translated into an opt-out line",
         message_opts_out(_cr_text, _G), False),
        ("override allows", decide(True, False, False, True, ["a.md"])[0], 0),
        ("sequencer state allows", decide(False, True, False, True, ["a.md"])[0], 0),
        ("opt-out allows", decide(False, False, True, True, ["a.md"])[0], 0),
        ("unreadable state refuses", decide(False, False, False, False, [])[0], 1),
        ("an offender refuses", decide(False, False, False, True, ["a.md"])[0], 1),
        ("no offender allows", decide(False, False, False, True, [])[0], 0),
        ("the refusal names the offender and the override",
         all(s in decide(False, False, False, True, ["x/a.md"])[1] for s in ("x/a.md", _OVERRIDE)), True),
        ("an opt-out in a comment line does not count",
         message_opts_out("subject\n# VersionBump: none (commented)\n", _G), False),
        ("an opt-out in the body counts", message_opts_out("subject\n\nVersionBump: none (reason)\n", _G), True),
        ("a vertical tab does not split a stripped comment line into an opt-out",
         message_opts_out("s\n# junk\x0bVersionBump: none x\n", _G), False),
        ("an opt-out below the scissors line does not count",
         message_opts_out("s\n# ------------------------ >8 ------------------------\n+VersionBump: none x\n", _G), False),
        ("a custom comment character is honoured", message_opts_out("s\n; VersionBump: none x\n", _G, ";"), False),
        ("'auto' strips every candidate (refuse-direction): a ';' comment is not an opt-out",
         message_opts_out("# subject\n; VersionBump: none x\n", _G, "auto"), False),
        ("an opt-out cannot be assembled across lines",
         message_opts_out("subject\n\nVersionBump:\n@ retained text\nnone\n", _G, "auto"), False),
        ("a scissors marker inside other comment text does not cut",
         message_opts_out("s\n# example ------------------------ >8 ------------------------\nVersionBump: none x\n", _G), True),
        ("a checkout without the guard is allowed", load_guard(Path("/nonexistent-checkout")), None),
    ]
    failures = [f"{n}: got {g!r}, want {w!r}" for n, g, w in cases if g != w]
    integ = _integration_self_test()
    failures += integ
    total = len(cases) + 14
    for f in failures:
        print(f"  FAIL: {f}")
    print(f"self-test: {total - len(failures)}/{total} passed" if not failures
          else f"self-test: FAILED ({len(failures)} of {total})")
    return 1 if failures else 0


def main(argv):
    if argv[1:] == ["--self-test"]:  # 3b50b2f: only the documented forms are accepted; anything else is a usage error (exit 2)
        return _self_test()
    if len(argv) == 3 and argv[1] == "--commit-msg":
        return _commit_msg(argv[2])
    print("usage: check-version-bump-commit.py --commit-msg <file> | --self-test", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
