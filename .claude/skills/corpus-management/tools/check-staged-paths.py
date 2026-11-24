#!/usr/bin/env python3
"""Git-native pre-commit check: require exactly the declared staged path set.

Declare from any directory in the checkout with --declare -- followed by literal,
repository-relative file paths regardless of the working directory. Invoke the
script by its absolute path from a subdirectory. The JSON declaration lives at grc-staged-paths.json
in `git rev-parse --absolute-git-dir`, separate for each linked worktree. It binds
paths to HEAD (null for an unborn branch); declare again after HEAD changes.
--declare -- with no paths explicitly authorizes an empty staged diff. Declaration
never copies paths from the index and never stages files. No environment override.

--pre-commit reads the effective index, retaining GIT_INDEX_FILE for partial and
all-tracked commits. NUL-delimited Git names preserve spaces, newlines and non-UTF-8
bytes. Renames count as deletion plus addition. Missing/malformed/stale declarations,
unmerged entries and Git errors refuse. Installed native pre-commit wiring runs
this after the existing checks and refuses if this script is missing.

Residual: script files, shell heredocs and subprocesses evade general command-text
inspection; this check sees their staged result when pre-commit runs. It checks
path equality, not content, author intent, or the scope claimed by a message. The
declaration and local hooks are writable by the author, not an authorization
boundary. Concurrent changes or later hooks modifying the index after inspection remain a race. Uninstalled or
skipped hooks, older checkouts without this chain, and operations that do not run
pre-commit (such as clean merges and sequencer commits) are outside this check.
Amend checks the delta against HEAD, not the amended commit's full parent diff.
See ../docs/guide-command-text-hooks.md for setup, declaration and residual details.
"""

import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

DECLARATION = "grc-staged-paths.json"
LIMIT = 1024 * 1024
DECLARE_HELP = ("Paths are always repository-relative. From the repository root run: python3 -I "
                ".claude/skills/corpus-management/tools/check-staged-paths.py "
                "--declare -- path/to/file other/file")


def git(root, *args):
    """Observe the active repository and index; Git failures propagate."""
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, timeout=30).stdout


def context():
    root = Path(os.fsdecode(git(Path.cwd(), "rev-parse", "--show-toplevel").removesuffix(b"\n")))
    directory = Path(os.fsdecode(git(root, "rev-parse", "--absolute-git-dir").removesuffix(b"\n")))
    try:
        head = git(root, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    except subprocess.CalledProcessError:
        # Only a symbolic ref that does not exist is an unborn HEAD. A corrupt
        # existing ref must not silently turn into an initial-commit declaration.
        ref = git(root, "symbolic-ref", "-q", "HEAD").decode("ascii").strip()
        cp = subprocess.run(["git", "-C", str(root), "show-ref", "--verify", "--quiet", ref],
                            capture_output=True, timeout=30)
        if cp.returncode != 1:
            raise ValueError("HEAD could not be read")
        head = None
    return root, directory / DECLARATION, head


def validate_paths(paths):
    if not isinstance(paths, list):
        raise ValueError("paths must be a JSON list")
    for path in paths:
        if (not isinstance(path, str) or not path or "\0" in path
                or path.startswith("/") or any(p in ("", ".", "..") for p in path.split("/"))):
            raise ValueError("paths must be literal canonical repository-relative file names")
        os.fsencode(path)  # Reject Unicode values that cannot name local files.
    if len(set(paths)) != len(paths):
        raise ValueError("duplicate declared path")
    return set(paths)


def unique_members(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate declaration member: " + key)
        result[key] = value
    return result


def read_declaration(path, head):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("declaration must be a regular file with one link")
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("declaration exceeds size limit")
    obj = json.loads(data, object_pairs_hook=unique_members)
    if not isinstance(obj, dict) or set(obj) != {"head", "paths"}:
        raise ValueError("declaration needs exactly head and paths")
    if obj["head"] != head:
        raise ValueError("declaration is stale: HEAD changed; declare paths again")
    return validate_paths(obj["paths"])


def declare(path, head, paths):
    validate_paths(paths)
    data = (json.dumps({"head": head, "paths": paths}, ensure_ascii=True, indent=2) + "\n").encode()
    if len(data) > LIMIT:
        raise ValueError("declaration exceeds size limit")
    # Atomic replacement does not follow the old destination, including symlinks.
    fd, name = tempfile.mkstemp(prefix=DECLARATION + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def staged_paths(root):
    if git(root, "ls-files", "--unmerged", "-z"):
        raise ValueError("index has unresolved merge entries")
    data = git(root, "diff", "--cached", "--name-only", "--no-renames", "-z",
               "--no-ext-diff", "--no-textconv", "--ignore-submodules=none",
               "--ita-invisible-in-index", "--")
    if data and not data.endswith(b"\0"):
        raise ValueError("Git returned an incomplete path list")
    return {os.fsdecode(p) for p in data.split(b"\0") if p}


def check(root, path, head):
    declared = read_declaration(path, head)
    staged = staged_paths(root)
    if staged != declared:
        unexpected = sorted(staged - declared)
        missing = sorted(declared - staged)
        raise ValueError("staged paths differ from declaration; undeclared staged paths: "
                         + json.dumps(unexpected) + "; declared paths not staged: "
                         + json.dumps(missing))


def main(argv):
    if argv != ["--pre-commit"] and argv[:2] != ["--declare", "--"]:
        print("usage: check-staged-paths.py --pre-commit | --declare -- [path ...]", file=sys.stderr)
        return 2
    try:
        root, path, head = context()
        if argv == ["--pre-commit"]:
            check(root, path, head)
        else:
            declare(path, head, argv[2:])
            print("Declared staged paths in " + str(path))
    except (OSError, ValueError, RecursionError, subprocess.SubprocessError) as exc:
        print("check-staged-paths: REFUSING: " + str(exc) + ". " + DECLARE_HELP, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
