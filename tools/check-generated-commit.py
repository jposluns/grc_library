#!/usr/bin/env python3
"""Git-native pre-commit check: refuse a commit that changes a document's leading metadata block (or a
generated output) while the staged taxonomy.yml, docs/portal.md or docs/maturity-scorecard.md is out of sync
(P-TODO 3b200, 2026-10-03).

Why a git hook. Gate 33 (tools/build-taxonomy.py --check and tools/build-portal.py --check) finds a stale
generated output only when the audit suite runs, after the commit: twice on 2026-10-03 (#2683 and 3b197) a
Version or Date change was committed without the regenerated outputs. git runs pre-commit inside every
commit, in the committing worktree, with the index being committed, however the command was spelled.

Why pre-commit and not commit-msg. This check has no message opt-out, so it runs before the message is
written, from the tracked tools/git-hooks/pre-commit, after check-commit-on-main.py and before
check-changelog-preflight-commit.py. The dispatcher that tools/install-git-hooks.sh installs execs that
tracked file, so a clone that has run the installer gets this check with no re-install.

When it judges a commit. When the index being committed, against HEAD (against nothing on an unborn HEAD,
so every staged file counts), changes one of the three generated outputs (so a hand-edited output is judged
too), adds or deletes a Markdown file (a rename, read with --no-renames, is a deletion plus an addition), or
changes the leading metadata block of a staged Markdown file. The block is exactly the span that
build-taxonomy.py's own extract_metadata() reads: from the first line through the line where it stops (the
first blank line, or line starting `---`, after a field line), or the whole file when it never stops.
This check carries no definition of its own: it compiles extract_metadata() and FIELD_PATTERN from the
STAGED tools/build-taxonomy.py (those two statements only, so no other generator code runs) and asks that
function where it stops, so the block follows any change to the generator's key pattern or stopping rule.
The HEAD and staged blocks are compared line for line, split as the generator splits a document (UTF-8,
str.splitlines()). So any field line (every key, not only Version and Date) judges the commit, as does any
line inserted, removed or changed within the block or at its stopping line (a blank or `---` line that
moves where the block ends); an edit below the block does not. When the block cannot be derived (the
staged tree has no tools/build-taxonomy.py, it does not parse, it lacks a single extract_metadata() and
FIELD_PATTERN, or the function raises), every staged Markdown change is judged and the staged generators'
--check decides. Every staged Markdown file is examined, a superset of the documents the generators index.
The blobs are read with git cat-file from the object names `git diff --cached --raw` gives, so no diff
attribute, external diff driver, textconv or colour setting lies in the path. Every other commit passes
unjudged.

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
staged change below a document's leading metadata block is not judged here: check-version-bump-commit.py
refuses, at commit-msg, an unbumped body change in a document that carries its own Version key, and the
bump it requires changes the block, but it counts a blank line or a column-zero `**Key:**` line anywhere as
metadata, so such a line changed below the block, like any body change in a document without its own
Version key, is judged by neither hook (gate 33 still runs in the suite); nor is a change to a generator or
tools/lint_common.py alone (gate 33 again); `git commit --amend` is judged only when the amend itself
changes a leading metadata block, adds or deletes a Markdown file, or changes an output relative to the
commit it replaces; a commit that git's sequencer makes itself (every `git rebase` pick, a cherry-pick or
revert that applies cleanly, a `git am` commit) and a clean `git merge` run no pre-commit hook;
`--no-verify` skips the hook; and it guards nothing until tools/install-git-hooks.sh has installed the
pre-commit shim in the clone.
"""
import __future__
import ast
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_OVERRIDE = "GRC_ALLOW_STALE_GENERATED_COMMIT"
_BUILDERS = ("tools/build-taxonomy.py", "tools/build-portal.py")
_OUTPUTS = ("taxonomy.yml", "docs/portal.md", "docs/maturity-scorecard.md")
# The generator whose extract_metadata() defines a document's leading metadata block.
_GENERATOR = _BUILDERS[0]
# A field line no document carries: extract_metadata() returns it exactly when it reads that far.
_PROBE = ("\0grc-generated-commit-probe", "\0reached")
_ABSENT = "000000"
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


def load_extract_metadata(source):
    """PURE. build-taxonomy.py's own extract_metadata(), compiled from its source with FIELD_PATTERN and
    nothing else (no other generator code runs). Raises unless each appears exactly once at top level."""
    tree = ast.parse(source, _GENERATOR)
    keep = [n for n in tree.body
            if (isinstance(n, ast.FunctionDef) and n.name == "extract_metadata")
            or (isinstance(n, ast.Assign) and [getattr(t, "id", None) for t in n.targets] == ["FIELD_PATTERN"])]
    if sorted(type(n).__name__ for n in keep) != ["Assign", "FunctionDef"]:
        raise ValueError(f"{_GENERATOR}: not exactly one extract_metadata() and one FIELD_PATTERN")
    namespace = {"re": re}
    exec(compile(ast.Module(body=keep, type_ignores=[]), _GENERATOR, "exec",
                 flags=__future__.annotations.compiler_flag, dont_inherit=True), namespace)
    return namespace["extract_metadata"]


def metadata_block(extract, text):
    """PURE. The lines of text that extract (build-taxonomy.py's extract_metadata()) reads, split as it
    splits them: the first line through the line where it stops, or every line when it never stops. The
    function itself says how far it reads: it reaches line k exactly when its answer for the first k lines
    plus the probe field line holds the probe, and reaching is monotone, so a binary search finds the last
    line it reaches."""
    lines = text.splitlines()
    probe = "**%s:** %s" % _PROBE

    def reaches(k):
        return extract("\n".join([*lines[:k], probe])).get(_PROBE[0]) == _PROBE[1]

    lo, hi = 0, len(lines)  # reaches(0) always holds: the probe is then the first line
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if reaches(mid):
            lo = mid
        else:
            hi = mid - 1
    return lines[:lo + 1]


def block_changed(extract, old, new):
    """PURE. Does a staged Markdown change (old and new as text, None for an absent side) judge the commit?
    An added or deleted file does; otherwise the leading metadata blocks are compared line for line."""
    if old is None or new is None:
        return True
    return metadata_block(extract, old) != metadata_block(extract, new)


def decide(allow, ok, judged, results):
    """PURE. Returns (exit_code, stderr_message).

    allow: override set; ok: the staged state was read (and, when judged, copied); judged: the commit
    changes a leading metadata block, a Markdown file's existence or a generated output (meaningful only
    when ok); results: one (generator, exit code, None when it could not be started, or _CRASHED when it
    exited 1 with a Python traceback) per generator (meaningful only when judged)."""
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
        return 1, ("check-generated-commit: REFUSING the commit: this commit changes a document's leading "
                   "metadata block or a generated output, and the staged generated outputs are out of sync "
                   f"with the staged documents (the generators' report is above). {_FIX} "
                   f"Deliberate override: {_OVERRIDE}=1.")
    return 0, ""


def _git(root, *args, data=None, extra=None):
    return subprocess.run(["git", "-C", str(root), *args], input=data, capture_output=True, check=True,
                          env={**os.environ, **(extra or {})}).stdout


def _read_blobs(root, oids):
    """The bytes of each named blob, in order, from one git cat-file --batch. A short read or an object
    that is not the named blob raises."""
    out = _git(root, "cat-file", "--batch", data=b"".join(oid.encode("ascii") + b"\n" for oid in oids))
    bodies, pos = [], 0
    for oid in oids:
        end = out.index(b"\n", pos)
        got, kind, size = out[pos:end].decode("ascii").split()
        size = int(size)
        body = out[end + 1:end + 1 + size]
        if got != oid or kind != "blob" or len(body) != size or out[end + 1 + size:end + 2 + size] != b"\n":
            raise RuntimeError(f"unexpected cat-file output for {oid}")
        pos = end + 2 + size
        bodies.append(body)
    if pos != len(out):
        raise RuntimeError("unexpected trailing cat-file output")
    return bodies


def staged_judged(root):
    """Thin observer: does the index being committed change a generated output, add or delete a Markdown
    file, or change a staged Markdown file's leading metadata block (the span the staged
    build-taxonomy.py's extract_metadata() reads)? A git error raises (ignorance refuses); a block that
    cannot be derived judges the commit."""
    fields = _git(root, "diff", "--cached", "--raw", "-z", "--no-renames", "--no-abbrev").split(b"\0")
    if fields[-1:] == [b""]:
        fields.pop()
    if len(fields) % 2:
        raise RuntimeError("unexpected git diff --raw output")
    docs = []
    for meta, raw in zip(fields[0::2], fields[1::2]):
        old_mode, new_mode, old_oid, new_oid, _ = meta.decode("ascii").lstrip(":").split()
        name = os.fsdecode(raw)
        if name in _OUTPUTS:
            return True
        if name.endswith(".md"):
            docs.append(((old_mode, old_oid), (new_mode, new_oid)))
    if not docs:
        return False
    sides = [side for doc in docs for side in doc if side[0] != _ABSENT]
    if any(mode not in (*_REGULAR, "120000") for mode, _ in sides):
        return True
    entry = _git(root, "ls-files", "--stage", "-z", "--", _GENERATOR,
                 extra={"GIT_LITERAL_PATHSPECS": "1"}).split(b"\0")[0]
    if not entry:
        return True
    mode, generator, _ = entry.split(b"\t", 1)[0].decode("ascii").split()
    if mode not in _REGULAR:
        return True
    oids = sorted({generator, *(oid for _, oid in sides)})
    text = {oid: body.decode("utf-8", errors="surrogateescape")
            for oid, body in zip(oids, _read_blobs(root, oids))}
    try:
        extract = load_extract_metadata(text[generator])
        return any(block_changed(extract, *(None if mode == _ABSENT else text[oid] for mode, oid in doc))
                   for doc in docs)
    except Exception:  # the block cannot be derived from the staged generator: judge, and its --check decides
        return True


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
    for (rel, _), body in zip(entries, _read_blobs(root, [oid for _, oid in entries])):
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_bytes(body)


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

        # The default is this check's own stale-output verdict (no generator prints it), so every stale case
        # also pins that an exit 1 without a traceback is reported as stale, not as a crash.
        def refused(cp, why="out of sync with the staged documents"):
            return (cp.returncode != 0 and "check-generated-commit: REFUSING" in cp.stderr
                    and why in cp.stderr and _OVERRIDE in cp.stderr)

        def reset():
            must(["git", "reset", "-q", "--hard", "HEAD"])

        def regenerate(where=repo):
            for rel in _BUILDERS:
                must([sys.executable, "-I", where / rel], cwd=where)

        doc = repo / "risk" / "policy-fixture.md"

        def write_doc(version="1.0.0", date="2026-01-01", purpose="Initial purpose.", where=doc, sep="",
                      kind="Policy", gap=""):
            where.parent.mkdir(parents=True, exist_ok=True)
            where.write_text(f"# Fixture\n\n**Document Title:** Fixture\\\n**Document Type:** {kind}\\\n{gap}"
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
        # Any change inside the leading metadata block, not only to a Version or Date line, refuses while
        # stale and passes once regenerated: a blank line inserted before `**Version :**` (the generator
        # then stops reading before Version and Date), the same on the usual keys, and another key's value.
        for label, fields in (("blank line before a spaced Version key", dict(sep=" ", gap="\n")),
                              ("blank line before the Version key", dict(gap="\n")),
                              ("Document Type change", dict(kind="Standard"))):
            if label == "blank line before the Version key":
                write_doc("1.0.1", "2026-02-02")
                regenerate()
                must(["git", "add", "-A"])
                must(["git", "commit", "-q", "-m", "usual keys"])
            write_doc("1.0.1", "2026-02-02", **fields)
            must(["git", "add", str(doc)])
            cp = run(["git", "commit", "-q", "-m", f"{label} stale"])
            expect(refused(cp) and "FAIL: taxonomy.yml is out of sync" in cp.stderr,
                   f"a staged {label} without regenerated outputs was not refused: {cp.stderr.strip()}")
            regenerate()
            must(["git", "add", *_OUTPUTS])
            cp = run(["git", "commit", "-q", "-m", f"{label} regenerated"])
            expect(cp.returncode == 0,
                   f"a staged {label} with regenerated outputs was refused: {cp.stderr.strip()}")
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
        # A staged build-taxonomy.py the block cannot be derived from, or none, judges even a body-only change.
        write_doc("1.0.4", purpose="Body only, with an underivable block.")
        (repo / _GENERATOR).write_text("raise SystemExit(3)\n", encoding="utf-8")
        must(["git", "add", str(doc), _GENERATOR])
        expect(refused(run(["git", "commit", "-q", "-m", "underivable"]), "(tools/build-taxonomy.py (exit 3)"),
               "a body-only change with a staged build-taxonomy.py lacking extract_metadata() was not judged")
        must(["git", "rm", "-q", "--cached", _GENERATOR])
        expect(refused(run(["git", "commit", "-q", "-m", "no generator"]),
                       "(tools/build-taxonomy.py (could not be started)"),
               "a body-only change with no staged build-taxonomy.py was not judged")
        reset()
        # The override is exactly "1": "0" still refuses; "1" allows and says so.
        write_doc("1.0.5")
        must(["git", "add", str(doc)])
        expect(refused(run(["git", "commit", "-q", "-m", "zero"], extra={_OVERRIDE: "0"})),
               "an override of 0 skipped the check")
        cp = run(["git", "commit", "-q", "-m", "override"], extra={_OVERRIDE: "1"})
        expect(cp.returncode == 0 and "NOTE" in cp.stderr, f"the override did not allow the commit: {cp.stderr.strip()}")
        # HEAD's outputs are now stale. A commit that changes no leading metadata block, adds or deletes no
        # Markdown file and changes no output is not judged (judging it would refuse): an unrelated file, a
        # body-only edit (which the commit-msg Version-bump check, not this one, refuses in a full clone),
        # and field and blank lines added below the block.
        (repo / "notes.txt").write_text("unrelated\n", encoding="utf-8")
        must(["git", "add", "notes.txt"])
        cp = run(["git", "commit", "-q", "-m", "unrelated"])
        expect(cp.returncode == 0, f"an unrelated commit was judged: {cp.stderr.strip()}")
        write_doc("1.0.5", purpose="Changed purpose.")
        must(["git", "add", str(doc)])
        cp = run(["git", "commit", "-q", "-m", "body only"])
        expect(cp.returncode == 0, f"a body-only commit was judged: {cp.stderr.strip()}")
        write_doc("1.0.5", purpose="Changed purpose.\n\n**Version:** 9.9.9\\\n\n**Owner:** Nobody")
        must(["git", "add", str(doc)])
        cp = run(["git", "commit", "-q", "-m", "field lines below the block"])
        expect(cp.returncode == 0, f"field and blank lines below the metadata block were judged: {cp.stderr.strip()}")
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


def _block_failures():
    """The block is the generator's: load_extract_metadata() compiles a function that answers as the
    imported build-taxonomy.py's extract_metadata() does, and on every probe document metadata_block() is
    exactly the lines that function reaches (a field line put in place of line i is read exactly when i
    falls inside the block), checked by brute force. Returns (failures, number of checks)."""
    import importlib.util
    path = Path(__file__).resolve().parent / "build-taxonomy.py"
    extract = load_extract_metadata(path.read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("_build_taxonomy_parity", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    head = "# T\n\n**Document Title:** T\\\n**Document Type:** Policy\\\n**Version:** 1\\\n**Date:** 2\\\n"
    probes = (head + "\n---\n\n## Purpose\n\nText.\n", head + "---\n## P\n", head + "Prose\n**Owner:** x\n\nBody\n",
              "# T\n\n**Version :** 1\r\n** Date:** 2\r\n\r\nBody\n", "**A:** 1\x0c**B:** 2\n\nBody", "No fields\n\nat all\n",
              head, "", "\n\n**A:** 1\n   \n**B:** 2\n", "**A:** 1\n-----\n**B:** 2\n", "\ufeff**A:** 1\n\nx\n", "**A:** 1\n\n")
    failures, checks = [], 0
    for text in probes:
        lines = text.splitlines()
        block = metadata_block(extract, text)
        checks += 2
        if extract(text) != module.extract_metadata(text):
            failures.append(f"block: the compiled extract_metadata() differs from the generator's on {text!r}")
        if block != lines[:len(block)] or extract("\n".join(block)) != extract(text):
            failures.append(f"block: {block!r} is not a leading span read as the whole of {text!r}")
        for i in range(len(lines)):
            checks += 1
            moved = "\n".join([*lines[:i], "**\0probe:** read", *lines[i + 1:]])
            inside = i < len(block)
            if (extract(moved).get("\0probe") == "read") != inside:
                failures.append(f"block: a field line in place of line {i} of {text!r} (inside {block!r}: "
                                f"{inside}) is read otherwise by the generator")
    return failures, checks


def _generator_failures():
    """Crash against stale, both ways, through run_generators() on stand-in generators: an exit 1 with no
    traceback (a stale report, or sys.exit("message")) is 1, and an uncaught exception is _CRASHED.
    Returns (failures, number of checks)."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "tools").mkdir()
        bodies = ("print('FAIL: stale'); raise SystemExit(1)", "raise RuntimeError('crash')")
        for rel, body in zip(_BUILDERS, bodies):
            (Path(tmp) / rel).write_text(body + "\n", encoding="utf-8")
        got = run_generators(Path(tmp))[0]
        (Path(tmp) / _BUILDERS[0]).write_text("import sys; sys.exit('message')\n", encoding="utf-8")
        exited = run_generators(Path(tmp))[0][0]
    want = [(_BUILDERS[0], 1), (_BUILDERS[1], _CRASHED)]
    failures = [f"generators: got {got!r}, want {want!r}"] if got != want else []
    if exited != (_BUILDERS[0], 1):
        failures.append(f"generators: sys.exit with a message gave {exited!r}, want exit 1")
    return failures, 2


def _self_test():
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
    ]
    extract = load_extract_metadata((Path(__file__).resolve().parent / "build-taxonomy.py").read_text(encoding="utf-8"))
    base = ("# Fixture\n\n**Document Title:** Fixture\\\n**Document Type:** Policy\\\n**Version:** 1.0.0\\\n"
            "**Date:** 2026-01-01\\\n\n---\n\n## Purpose\n\nInitial purpose.\n")
    spaced = base.replace("**Version:**", "**Version :**").replace("**Date:**", "**Date :**")
    edits = (
        ("a Version change", base, ("1.0.0", "1.0.1"), True),
        ("a Date change on a spaced key", spaced, ("2026-01-01", "2026-02-02"), True),
        ("another key's value (Document Type)", base, ("Policy", "Standard"), True),
        ("a blank line before the Version key", base, ("Policy\\\n", "Policy\\\n\n"), True),
        ("a blank line before a spaced Version key", spaced, ("Policy\\\n", "Policy\\\n\n"), True),
        ("a `---` before the Version key", base, ("Policy\\\n", "Policy\\\n---\n"), True),
        ("a blank line above the first field", base, ("# Fixture\n", "# Fixture\n\n"), True),
        ("the stopping blank line removed", base, ("01\\\n\n---", "01\\\n---"), True),
        ("a body edit below the block", base, ("Initial purpose.", "Changed purpose."), False),
        ("a heading edit below the block", base, ("## Purpose", "## Scope"), False),
        ("a Version line added below the block", base, ("purpose.\n", "purpose.\n\n**Version:** 9\n"), False),
        ("a blank line below the stopping line", base, ("---\n", "---\n\n"), False),
        ("a CRLF conversion the generator reads alike", base, ("\n", "\r\n"), False),
        ("a body edit in a document with no field line", "# Notes\n\nText.\n", ("Text.", "More."), True),
    )
    cases += [(f"block: {n}", block_changed(extract, text, text.replace(*sub)), want) for n, text, sub, want in edits]
    cases += [("block: an added document", block_changed(extract, None, base), True),
              ("block: a deleted document", block_changed(extract, base, None), True),
              ("block: an added empty document", block_changed(extract, None, ""), True),
              ("block: an unchanged document", block_changed(extract, base, base), False)]
    failures = [f"{n}: got {g!r}, want {w!r}" for n, g, w in cases if g != w]
    block, block_checks = _block_failures()
    generators, generator_checks = _generator_failures()
    integ, checks = _integration_self_test()
    failures += block + generators + integ
    total = len(cases) + block_checks + generator_checks + checks
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
