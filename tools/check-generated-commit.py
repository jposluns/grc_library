#!/usr/bin/env python3
"""Git-native pre-commit check: refuse a commit that changes a document's Version or Date line while the
staged taxonomy.yml, docs/portal.md or docs/maturity-scorecard.md is out of sync (P-TODO 3b200, 2026-10-03).

Why a git hook. Gate 33 (tools/build-taxonomy.py --check and tools/build-portal.py --check) finds a stale
generated output only when the audit suite runs, after the commit: twice on 2026-10-03 (#2683 and 3b197) a
Version or Date change was committed without the regenerated outputs. git runs pre-commit inside every
commit, in the committing worktree, with the index being committed, however the command was spelled.

Why pre-commit and not commit-msg. This check has no message opt-out, so it runs before the message is
written, from the tracked tools/git-hooks/pre-commit, after check-commit-on-main.py and before
check-changelog-preflight-commit.py. The dispatcher that tools/install-git-hooks.sh installs execs that
tracked file, so a clone that has run the installer gets this check with no re-install.

When it judges a commit. When the index being committed, against HEAD (against nothing on an unborn HEAD,
so every staged file counts), adds or removes a line in a staged Markdown file that build-taxonomy.py's
extract_metadata() would read as the Version or Date field (a line-start `**<key>:**` matching its
FIELD_PATTERN, the key compared after .strip(), so `**Version :**` and `** Date:**` count as well as
`**Version:**`; this check carries a verbatim copy of that pattern, and its self-test fails if the copy or
the key reading diverges from the generator's), or changes one of the three generated outputs (so a
hand-edited output is judged too). A bump, a new or deleted document, and a rename (read
with --no-renames, as a deletion plus an addition) all add or remove such a line. The diff is read with
--text, --no-ext-diff, --no-textconv and --no-color, so a -diff attribute, an external diff driver,
textconv or colour cannot hide a changed line; the staged Markdown names are passed as literal pathspecs.
Every other commit passes unjudged.

What it checks. It copies every stage-0 regular-file blob of the index being committed (the one git named
in GIT_INDEX_FILE, so `git commit -a` and `git commit <path>` are judged on what they commit) into a
temporary directory, byte for byte, with no checkout filter and no working-tree read. It then runs that
snapshot's own tools/build-taxonomy.py --check and tools/build-portal.py --check there (python3 -I, without
the GIT_ variables), and refuses unless both exit 0, relaying their reports. The staged generators judge
the staged sources and the staged outputs, so an output regenerated but not staged, or a working-tree edit,
changes nothing. The check never regenerates or stages anything: it refuses and names the fix.

Allowed without checking: the override GRC_ALLOW_STALE_GENERATED_COMMIT=1, honoured only when the value is
exactly "1" (as check-changelog-preflight-commit.py reads its own), so "0", "false" or an empty value is not
the override. A commit that concludes a merge, cherry-pick or revert is checked like any other: two
branches that each regenerated taxonomy.yml conflict there, and a hand resolution is what this check is for.
It REFUSES, naming the override (ignorance refuses, as in the sibling checks): a git error while reading
the staged state; an unmerged, unsafe or unknown-mode index entry; a generator missing from the staged tree
or failing to start; and a generator that exits other than 0. An exit 1 whose stderr carries a Python
traceback is reported as a generator crash, not as stale output; any other exit 1 is the generator's
stale-output report.

Residue, stated: a symlink or submodule entry is not copied into the snapshot, so a generator reading
through one finds it missing (and refuses when the staged outputs list it); a generator that stops with
sys.exit("message") exits 1 without a traceback, so it is reported as stale output (it still refuses); a
staged body change that moves no Version or Date line is not judged here (check-version-bump-commit.py
refuses an unbumped body at
commit-msg, and gate 33 still runs in the suite), nor is a change to a generator or tools/lint_common.py
alone (gate 33 again); `git commit --amend` is judged only when the amend itself changes a Version or Date
line or an output relative to the commit it replaces; a commit that git's sequencer makes itself (every
`git rebase` pick, a cherry-pick or revert that applies cleanly, a `git am` commit) and a clean `git merge`
run no pre-commit hook; `--no-verify` skips the hook; and it guards nothing until tools/install-git-hooks.sh
has installed the pre-commit shim in the clone.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_OVERRIDE = "GRC_ALLOW_STALE_GENERATED_COMMIT"
_BUILDERS = ("tools/build-taxonomy.py", "tools/build-portal.py")
_OUTPUTS = ("taxonomy.yml", "docs/portal.md", "docs/maturity-scorecard.md")
# build-taxonomy.py's FIELD_PATTERN, verbatim. Its extract_metadata() reads a line this matches as the field
# named by group 1 after .strip(), so `**Version :**` is the Version field; the self-test fails if this copy,
# or metadata_line_changed()'s key reading, diverges from the generator's.
_FIELD = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
_KEYS = ("Version", "Date")
# An uncaught Python exception also exits 1, the generators' stale-output code; its traceback tells them apart.
_TRACEBACK = "Traceback (most recent call last):"
_CRASHED = "crashed"
_UNFINISHED = {None: "could not be started", _CRASHED: "crashed with an uncaught exception"}
_REGULAR = ("100644", "100755")
_UNCOPIED = ("120000", "160000")   # a symlink or a submodule: no file content to copy
_FIX = ("Regenerate from the tree you are committing (`python3 tools/build-taxonomy.py && python3 "
        "tools/build-portal.py`), `git add taxonomy.yml docs/portal.md docs/maturity-scorecard.md`, and "
        "commit again.")


def override_set(environ):
    """PURE. The override is honoured only when its value is exactly "1"."""
    return environ.get(_OVERRIDE) == "1"


def metadata_line_changed(diff):
    """PURE. Does a unified diff add or remove a line that build-taxonomy.py's extract_metadata() would
    read as the Version or Date field? Each added or removed line is split as the generator splits a
    document (str.splitlines()), and a piece counts when _FIELD matches it and its key, stripped, is
    Version or Date. No diff header line can count: each starts with `diff `, `index `, `---`, `+++`,
    `@@` or a mode keyword, and git C-quotes a path holding a control character, so no header line is a
    `+` or `-` followed by `**`."""
    for line in diff.split("\n"):
        if line[:1] not in ("+", "-"):
            continue
        for piece in line[1:].splitlines():
            m = _FIELD.match(piece)
            if m and m.group(1).strip() in _KEYS:
                return True
    return False


def decide(allow, ok, judged, results):
    """PURE. Returns (exit_code, stderr_message).

    allow: override set; ok: the staged state was read (and, when judged, copied); judged: the commit
    changes a Version or Date line or a generated output (meaningful only when ok); results: one
    (generator, exit code, None when it could not be started, or _CRASHED when it exited 1 with a Python
    traceback) per generator (meaningful only when judged)."""
    if allow:
        return 0, (f"check-generated-commit: NOTE: {_OVERRIDE}=1 is set; skipping the generated-output "
                   "check.")
    if not ok:
        return 1, ("check-generated-commit: REFUSING the commit: the staged state could not be read or "
                   "copied, so it is unknown whether the staged taxonomy.yml, docs/portal.md and "
                   f"docs/maturity-scorecard.md are in sync. Deliberate override: {_OVERRIDE}=1.")
    if not judged:
        return 0, ""
    unfinished = [f"{name} ({_UNFINISHED.get(code, f'exit {code}')})"
                  for name, code in results if code not in (0, 1)]
    if unfinished or len(results) != len(_BUILDERS):
        return 1, ("check-generated-commit: REFUSING the commit: a staged generator did not complete ("
                   f"{', '.join(unfinished) or 'not run'}), so it is unknown whether the staged generated "
                   f"outputs are in sync. Deliberate override: {_OVERRIDE}=1.")
    if any(code for _, code in results):
        return 1, ("check-generated-commit: REFUSING the commit: this commit changes a Version or Date "
                   "line or a generated output, and the staged generated outputs are out of sync with the "
                   f"staged documents (the generators' report is above). {_FIX} "
                   f"Deliberate override: {_OVERRIDE}=1.")
    return 0, ""


def _git(root, *args, data=None, extra=None):
    return subprocess.run(["git", "-C", str(root), *args], input=data, capture_output=True, check=True,
                          env={**os.environ, **(extra or {})}).stdout


def staged_judged(root):
    """Thin observer: does the index being committed change a generated output, or add or remove a
    Version or Date line in a staged Markdown file? A git error raises (ignorance refuses)."""
    names = [os.fsdecode(n) for n in _git(root, "diff", "--cached", "--name-only", "--no-renames",
                                          "--no-ext-diff", "--no-textconv", "-z").split(b"\0") if n]
    if any(n in _OUTPUTS for n in names):
        return True
    docs = [n for n in names if n.endswith(".md")]
    if not docs:
        return False
    diff = _git(root, "diff", "--cached", "--no-renames", "--no-ext-diff", "--no-textconv", "--no-color",
                "--text", "--unified=0", "--", *docs, extra={"GIT_LITERAL_PATHSPECS": "1"})
    return metadata_line_changed(diff.decode("utf-8", errors="replace"))


def snapshot(root, dest):
    """Thin observer: copy every stage-0 regular-file blob of the index being committed into dest, byte
    for byte. An unmerged, unsafe or unknown-mode entry, or a short read, raises (ignorance refuses)."""
    entries = []
    for record in _git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, raw = record.split(b"\t", 1)
        mode, oid, stage = meta.decode("ascii").split()
        name = os.fsdecode(raw)
        rel = Path(name)
        if stage != "0":
            raise RuntimeError(f"unmerged index entry: {name!r}")
        if rel.is_absolute() or ".." in rel.parts or ".git" in rel.parts:
            raise RuntimeError(f"unsafe index path: {name!r}")
        if mode in _UNCOPIED:
            continue
        if mode not in _REGULAR:
            raise RuntimeError(f"unknown index mode {mode}: {name!r}")
        entries.append((rel, oid))
    out = _git(root, "cat-file", "--batch", data=b"".join(oid.encode("ascii") + b"\n" for _, oid in entries))
    pos = 0
    for rel, oid in entries:
        end = out.index(b"\n", pos)
        got, kind, size = out[pos:end].decode("ascii").split()
        size = int(size)
        body = out[end + 1:end + 1 + size]
        if got != oid or kind != "blob" or len(body) != size or out[end + 1 + size:end + 2 + size] != b"\n":
            raise RuntimeError(f"unexpected cat-file output for {rel.as_posix()!r}")
        pos = end + 2 + size
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_bytes(body)
    if pos != len(out):
        raise RuntimeError("unexpected trailing cat-file output")


def run_generators(dest):
    """[(generator, exit code, None, or _CRASHED)] and the combined report of the snapshot's own generators,
    each run with --check in the snapshot, isolated from Python and git environment overrides. An exit 1
    whose stderr carries a Python traceback is _CRASHED (an uncaught exception), not a stale report."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    results, reports = [], []
    for rel in _BUILDERS:
        script = dest / rel
        if not script.is_file():
            results.append((rel, None))
            reports.append(f"check-generated-commit: {rel} is not in the staged tree.")
            continue
        try:
            cp = subprocess.run([sys.executable, "-I", str(script), "--check"], cwd=dest, env=env,
                                capture_output=True, text=True)
        except OSError as exc:
            results.append((rel, None))
            reports.append(f"check-generated-commit: {rel}: {exc}")
            continue
        code = cp.returncode
        if code == 1 and _TRACEBACK in cp.stderr:
            code = _CRASHED
        results.append((rel, code))
        if cp.returncode:
            reports.append((cp.stdout + cp.stderr).strip())
    return results, "\n".join(r for r in reports if r)


def _pre_commit():
    allow = override_set(os.environ)
    judged, results, report = False, [], ""
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                             check=True).stdout.strip()
        root = Path(top)
        if not allow:  # the override skips the generator runs, not only their verdict
            judged = staged_judged(root)
            if judged:
                with tempfile.TemporaryDirectory(prefix="grc-generated-commit-") as tmp:
                    snapshot(root, Path(tmp))
                    results, report = run_generators(Path(tmp))
        ok = True
    except Exception as exc:
        ok, report = False, f"check-generated-commit: {type(exc).__name__}: {exc}"
    rc, msg = decide(allow, ok, judged, results)
    if rc and report:
        print(report, file=sys.stderr)
    if msg:
        print(msg, file=sys.stderr)
    return rc


def _integration_self_test():
    """End to end: a real repository under a spaced path, the real installer, the real generators, and
    real commits. Returns (failures, number of checks)."""
    import shutil
    src = Path(__file__).resolve().parents[1]
    failures, checks = [], []

    def expect(cond, message):
        checks.append(message)
        if not cond:
            failures.append(message)

    with tempfile.TemporaryDirectory() as base:
        repo = Path(base) / "clone with space" / "r"
        for rel in ("tools/check-generated-commit.py", "tools/check-commit-on-main.py",
                    "tools/install-git-hooks.sh", "tools/git-hooks/pre-commit", "tools/git-hooks/pre-push",
                    "tools/lint_common.py", *_BUILDERS):
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

        def must(args, cwd=repo, extra=None):
            cp = run(args, cwd=cwd, extra=extra)
            if cp.returncode != 0:
                failures.append(f"fixture step failed: {' '.join(map(str, args))}: {cp.stderr.strip()}")
            return cp

        def refused(cp, why="out of sync"):
            return (cp.returncode != 0 and "check-generated-commit: REFUSING" in cp.stderr
                    and why in cp.stderr and _OVERRIDE in cp.stderr)

        def reset():
            must(["git", "reset", "-q", "--hard", "HEAD"])

        def regenerate(where=repo):
            for rel in _BUILDERS:
                must([sys.executable, "-I", where / rel], cwd=where)

        doc = repo / "risk" / "policy-fixture.md"

        def write_doc(version="1.0.0", date="2026-01-01", purpose="Initial purpose.", where=doc, sep=""):
            where.parent.mkdir(parents=True, exist_ok=True)
            where.write_text(f"# Fixture\n\n**Document Title:** Fixture\\\n**Document Type:** Policy\\\n"
                             f"**Version{sep}:** {version}\\\n**Date{sep}:** {date}\\\n\n---\n\n## Purpose\n\n"
                             f"{purpose}\n",
                             encoding="utf-8")

        must(["git", "init", "-q", "-b", "feature"])
        must(["git", "config", "commit.gpgsign", "false"])
        expect(run(["sh", "tools/install-git-hooks.sh"]).returncode == 0, "the installer failed")
        # An initial commit on an unborn HEAD is judged against nothing: stale outputs refuse, fresh pass.
        write_doc()
        regenerate()
        (repo / "taxonomy.yml").write_text("stale\n", encoding="utf-8")
        must(["git", "add", "-A"])
        expect(refused(run(["git", "commit", "-q", "-m", "init stale"])),
               "an initial commit with a stale taxonomy.yml was not refused")
        regenerate()
        must(["git", "add", "-A"])
        cp = run(["git", "commit", "-q", "-m", "init"])
        expect(cp.returncode == 0, f"an initial commit with fresh outputs was refused: {cp.stderr.strip()}")
        # A Version bump, and a Date-only change, without regenerated outputs refuse.
        for version, date, label in (("1.0.1", "2026-01-01", "Version"), ("1.0.0", "2026-02-02", "Date")):
            write_doc(version, date)
            must(["git", "add", str(doc)])
            cp = run(["git", "commit", "-q", "-m", f"{label} only"])
            expect(refused(cp) and "python3 tools/build-taxonomy.py" in cp.stderr
                   and "FAIL: taxonomy.yml is out of sync" in cp.stderr,
                   f"a staged {label} change without regenerated outputs was not refused: {cp.stderr.strip()}")
            reset()
        # A key spelling build-taxonomy.py also reads as Version or Date (`**Version :**`, `**Date :**`),
        # committed in sync: a value change without regenerated outputs refuses, and with them passes.
        write_doc(sep=" ")
        regenerate()
        must(["git", "add", "-A"])
        must(["git", "commit", "-q", "-m", "spaced keys"])
        for version, date, label in (("1.0.1", "2026-01-01", "Version :"), ("1.0.1", "2026-02-02", "Date :")):
            write_doc(version, date, sep=" ")
            must(["git", "add", str(doc)])
            cp = run(["git", "commit", "-q", "-m", f"{label} stale"])
            expect(refused(cp) and "FAIL: taxonomy.yml is out of sync" in cp.stderr,
                   f"a staged `{label}` change without regenerated outputs was not refused: {cp.stderr.strip()}")
            regenerate()
            must(["git", "add", *_OUTPUTS])
            cp = run(["git", "commit", "-q", "-m", f"{label} regenerated"])
            expect(cp.returncode == 0,
                   f"a staged `{label}` change with regenerated outputs was refused: {cp.stderr.strip()}")
        # Outputs regenerated in the working tree but not staged: the index is judged, so it refuses.
        write_doc("1.0.1")
        must(["git", "add", str(doc)])
        regenerate()
        expect(refused(run(["git", "commit", "-q", "-m", "unstaged outputs"])),
               "outputs regenerated but not staged did not refuse")
        must(["git", "add", *_OUTPUTS])
        # Working-tree drift after staging cannot spoil a consistent index.
        write_doc("9.9.9")
        cp = run(["git", "commit", "-q", "-m", "bumped and regenerated"])
        expect(cp.returncode == 0, f"a bump staged with its regenerated outputs was refused: {cp.stderr.strip()}")
        reset()
        # `git commit -a` and a pathspec commit are judged on the index git builds for them.
        for args in (["-a"], ["--", str(doc)]):
            write_doc("1.0.2")
            cp = run(["git", "commit", "-q", "-m", "implicit index", *args])
            expect(refused(cp), f"`git commit {' '.join(args[:1])}` with a stale output was not refused")
            reset()
        # A -diff attribute, an external diff driver and colour cannot hide the changed Version line.
        (repo / ".gitattributes").write_text("*.md -diff\n", encoding="utf-8")
        must(["git", "add", ".gitattributes"])
        must(["git", "commit", "-q", "-m", "binary markdown"])
        must(["git", "config", "diff.external", "true"])
        must(["git", "config", "color.diff", "always"])
        write_doc("1.0.3")
        must(["git", "add", str(doc)])
        expect(refused(run(["git", "commit", "-q", "-m", "hostile config"])),
               "a -diff attribute, diff.external or color.diff=always hid a Version change")
        must(["git", "config", "--unset", "diff.external"])
        must(["git", "config", "--unset", "color.diff"])
        reset()
        # A hand-edited output, a deleted document and a renamed document each refuse.
        with (repo / "taxonomy.yml").open("a", encoding="utf-8") as fh:
            fh.write("# hand edit\n")
        must(["git", "add", "taxonomy.yml"])
        expect(refused(run(["git", "commit", "-q", "-m", "hand edit"])), "a hand-edited taxonomy.yml was not refused")
        reset()
        must(["git", "rm", "-q", str(doc)])
        expect(refused(run(["git", "commit", "-q", "-m", "delete"])), "a deleted document was not refused")
        reset()
        must(["git", "mv", str(doc), str(repo / "risk" / "policy renamed\tfixture.md")])
        expect(refused(run(["git", "commit", "-q", "-m", "rename"])), "a renamed document was not refused")
        reset()
        # A staged generator that crashes, or is missing, refuses as unknown, not as a pass.
        write_doc("1.0.4")
        regenerate()
        must(["git", "add", "-A"])
        (repo / _BUILDERS[1]).write_text("raise RuntimeError('fixture crash')\n", encoding="utf-8")
        must(["git", "add", _BUILDERS[1]])
        cp = run(["git", "commit", "-q", "-m", "crash"])
        expect(refused(cp, "did not complete (tools/build-portal.py (crashed with an uncaught exception))")
               and "RuntimeError: fixture crash" in cp.stderr and "out of sync with the staged" not in cp.stderr,
               f"a staged generator raising an exception was not refused as a crash: {cp.stderr.strip()}")
        (repo / _BUILDERS[1]).write_text("raise SystemExit(3)\n", encoding="utf-8")
        must(["git", "add", _BUILDERS[1]])
        expect(refused(run(["git", "commit", "-q", "-m", "crash"]), "did not complete (tools/build-portal.py (exit 3))"),
               "a staged generator exiting 3 did not refuse as unknown")
        must(["git", "rm", "-q", "--cached", _BUILDERS[1]])
        expect(refused(run(["git", "commit", "-q", "-m", "missing"]), "could not be started"),
               "a generator missing from the staged tree did not refuse")
        reset()
        # The override is exactly "1": "0" still refuses; "1" allows and says so.
        write_doc("1.0.5")
        must(["git", "add", str(doc)])
        expect(refused(run(["git", "commit", "-q", "-m", "zero"], extra={_OVERRIDE: "0"})),
               "an override of 0 skipped the check")
        cp = run(["git", "commit", "-q", "-m", "override"], extra={_OVERRIDE: "1"})
        expect(cp.returncode == 0 and "NOTE" in cp.stderr, f"the override did not allow the commit: {cp.stderr.strip()}")
        # HEAD's outputs are now stale. A commit that moves no Version or Date line and no output is not
        # judged (judging it would refuse): an unrelated file, and a body-only edit (which the commit-msg
        # Version-bump check, not this one, refuses in a full clone).
        (repo / "notes.txt").write_text("unrelated\n", encoding="utf-8")
        must(["git", "add", "notes.txt"])
        cp = run(["git", "commit", "-q", "-m", "unrelated"])
        expect(cp.returncode == 0, f"an unrelated commit was judged: {cp.stderr.strip()}")
        write_doc("1.0.5", purpose="Changed purpose.")
        must(["git", "add", str(doc)])
        cp = run(["git", "commit", "-q", "-m", "body only"])
        expect(cp.returncode == 0, f"a body-only commit was judged: {cp.stderr.strip()}")
        regenerate()
        must(["git", "add", *_OUTPUTS])
        must(["git", "commit", "-q", "-m", "regenerated"])
        # A commit made with `git -C` in a linked worktree is judged on that worktree's index.
        linked = Path(base) / "linked wt"
        must(["git", "worktree", "add", "-q", "-b", "other", str(linked)])
        write_doc("1.0.6", where=linked / "risk" / "policy-fixture.md")
        must(["git", "-C", str(linked), "add", "risk"])
        cp = run(["git", "-C", str(linked), "commit", "-q", "-m", "linked"], cwd=base)
        expect(refused(cp), f"a stale commit made with git -C in a linked worktree was not refused: {cp.stderr.strip()}")
        regenerate(linked)
        must(["git", "-C", str(linked), "add", "-A"])
        cp = run(["git", "-C", str(linked), "commit", "-q", "-m", "linked regenerated"], cwd=base)
        expect(cp.returncode == 0, f"a regenerated linked-worktree commit was refused: {cp.stderr.strip()}")
        # The tracked shim fails OPEN for a tree without this check (the other hooks' fixtures copy the
        # shim without it), and a commit-on-main refusal still stops the commit before this check runs.
        check = repo / "tools" / "check-generated-commit.py"
        check.rename(repo / "moved-check.py")
        write_doc("1.0.7")
        must(["git", "add", str(doc)])
        cp = run(["git", "commit", "-q", "-m", "no check"])
        expect(cp.returncode == 0, f"the shim did not fail open without this check: {cp.stderr.strip()}")
        (repo / "moved-check.py").rename(check)
        must(["git", "switch", "-q", "-c", "main"])
        write_doc("1.0.8")
        must(["git", "add", str(doc)])
        cp = run(["git", "commit", "-q", "-m", "on main"])
        expect(cp.returncode != 0 and "check-commit-on-main: REFUSING" in cp.stderr
               and "check-generated-commit" not in cp.stderr, "the shim ran on past a commit-on-main refusal")
        # A git error while reading the staged state refuses through the installed hook (ignorance
        # refuses): with HEAD's root tree gone from the object store, the check's `git diff --cached` fails.
        # Last, because it damages the fixture repository.
        reset()
        must(["git", "switch", "-q", "feature"])
        tree = must(["git", "rev-parse", "HEAD^{tree}"]).stdout.strip()
        write_doc("1.0.9")
        must(["git", "add", str(doc)])
        loose = repo / ".git" / "objects" / tree[:2] / tree[2:]
        if loose.is_file():
            loose.unlink()
            cp = run(["git", "commit", "-q", "-m", "unreadable"])
            expect(refused(cp, "could not be read or copied") and "CalledProcessError" in cp.stderr,
                   f"a git error reading the staged state did not refuse through the hook: {cp.stderr.strip()}")
        else:
            expect(False, f"fixture: HEAD's root tree {tree} is not a loose object")
    return failures, len(checks)


def _parity_failures():
    """The trigger reads Version and Date lines as build-taxonomy.py does: _FIELD is its FIELD_PATTERN
    verbatim, and on every probe line metadata_line_changed() agrees with its extract_metadata(). Returns
    (failures, number of checks)."""
    import ast
    import importlib.util
    path = Path(__file__).resolve().parent / "build-taxonomy.py"
    calls = [n.value for n in ast.parse(path.read_text(encoding="utf-8")).body
             if isinstance(n, ast.Assign) and [getattr(t, "id", None) for t in n.targets] == ["FIELD_PATTERN"]]
    literal = (calls[0].args[0].value if len(calls) == 1 and isinstance(calls[0], ast.Call)
               and len(calls[0].args) == 1 and not calls[0].keywords
               and isinstance(calls[0].args[0], ast.Constant) else None)
    failures = [] if literal == _FIELD.pattern else [
        f"_FIELD {_FIELD.pattern!r} is not build-taxonomy.py's FIELD_PATTERN (read {literal!r})"]
    spec = importlib.util.spec_from_file_location("_build_taxonomy_parity", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    probes = ("**Version:** 1.0.1\\", "**Version :** 1.0.1\\", "** Date:** 2026-01-01", "**Date\t:**2026-01-01",
              "**\u00a0Version\u00a0:** 1", "**Version:**", "**Version :**\r", "text\x0c**Date:** 2026-01-01",
              "**Library Version:** 1", "**Versions:** 1", "**version:** 1", "Version: 1", "**Version**: 1",
              "  **Version:** 1", "**Ver*sion:** 1")
    checks = 1
    for probe in probes:
        want = any(k in module.extract_metadata(probe) for k in _KEYS)
        for sign in "+-":
            checks += 1
            if metadata_line_changed(f"@@ -1 +1 @@\n{sign}{probe}") != want:
                failures.append(f"parity: {sign}{probe!r}: the trigger says {not want}, extract_metadata() {want}")
    return failures, checks


def _self_test():
    hunk = "@@ -3 +3 @@\n"
    cases = [
        ("override allows stale outputs", decide(True, True, True, [(b, 1) for b in _BUILDERS])[0], 0),
        ("override allows an unreadable state", decide(True, False, False, [])[0], 0),
        ("unreadable state refuses", decide(False, False, False, [])[0], 1),
        ("an unjudged commit allows", decide(False, True, False, [])[0], 0),
        ("in-sync outputs allow", decide(False, True, True, [(b, 0) for b in _BUILDERS])[0], 0),
        ("an out-of-sync output refuses", decide(False, True, True, [(_BUILDERS[0], 1), (_BUILDERS[1], 0)])[0], 1),
        ("a generator exit 2 refuses", decide(False, True, True, [(_BUILDERS[0], 0), (_BUILDERS[1], 2)])[0], 1),
        ("a generator killed by a signal refuses", decide(False, True, True, [(_BUILDERS[0], -15), (_BUILDERS[1], 0)])[0], 1),
        ("a generator that could not start refuses", decide(False, True, True, [(_BUILDERS[0], None), (_BUILDERS[1], 0)])[0], 1),
        ("a judged commit with no generator run refuses", decide(False, True, True, [])[0], 1),
        ("every refusal names the override",
         all(_OVERRIDE in decide(False, *a)[1] for a in ((False, False, []), (True, True, [(_BUILDERS[0], 1)]),
                                                        (True, True, [(_BUILDERS[0], None)]),
                                                        (True, True, [(_BUILDERS[0], _CRASHED)]))), True),
        ("a crashed generator refuses as unfinished, without the stale-output fix",
         (lambda r: (r[0], "crashed with an uncaught exception" in r[1], _FIX in r[1]))(
             decide(False, True, True, [(_BUILDERS[0], 0), (_BUILDERS[1], _CRASHED)])), (1, True, False)),
        ("the override is exactly 1", override_set({_OVERRIDE: "1"}), True),
        ("0 is not the override", override_set({_OVERRIDE: "0"}), False),
        ("an empty value is not the override", override_set({_OVERRIDE: ""}), False),
        ("an added Version line triggers", metadata_line_changed(hunk + "+**Version:** 1.0.1\\"), True),
        ("a removed Date line triggers", metadata_line_changed(hunk + "-**Date:** 2026-01-01\\"), True),
        ("a spaced `Version :` key triggers", metadata_line_changed(hunk + "+**Version :** 1.0.1\\"), True),
        ("a removed spaced `Date :` key triggers", metadata_line_changed(hunk + "-**Date :** 2026-01-01\\"), True),
        ("a padded `** Version:**` key triggers", metadata_line_changed(hunk + "+** Version:** 1.0.1"), True),
        ("another key ending in Version does not trigger",
         metadata_line_changed(hunk + "+**Library Version:** 1"), False),
        ("a line without the bold key does not trigger", metadata_line_changed(hunk + "+Version: 1.0.1"), False),
        ("an indented Version line (not FIELD_PATTERN's form) does not trigger",
         metadata_line_changed(hunk + "+  **Version:** 1.0.1"), False),
    ]
    failures = [f"{n}: got {g!r}, want {w!r}" for n, g, w in cases if g != w]
    parity, parity_checks = _parity_failures()
    integ, checks = _integration_self_test()
    failures += parity + integ
    total = len(cases) + parity_checks + checks
    for f in failures:
        print(f"  FAIL: {f}")
    print(f"self-test: {total - len(failures)}/{total} passed" if not failures
          else f"self-test: FAILED ({len(failures)} of {total})")
    return 1 if failures else 0


def main(argv):
    if argv[1:] == ["--self-test"]:  # only the documented forms are accepted; anything else is a usage error (exit 2)
        return _self_test()
    if argv[1:] == ["--pre-commit"]:
        return _pre_commit()
    print("usage: check-generated-commit.py --pre-commit | --self-test", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
