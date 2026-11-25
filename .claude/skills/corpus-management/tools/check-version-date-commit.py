#!/usr/bin/env python3
"""Check staged Version and Date edits against the current UTC date.

Version-line changes require today's staged Date value; Date-line changes
require a Version-line change. Generator-owned, new and deleted documents are
out of scope. Read Git blobs, never working-tree document content. Compare the
index with HEAD only, including on amend: HEAD is the commit being amended,
so a Date-only change relative to its parent can pass at commit time. The Date
staleness and version-recency gates still catch stale Dates and missing Version
bumps before a push, within their documented scope and tolerances. No parent
process command line or process filesystem is read. Inspection failures exit 2;
metadata violations exit 1. No commit or repository history is written.
"""

import argparse
import datetime
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tomllib

sys.dont_write_bytecode = True
sys.path.append(str(Path(__file__).resolve().parent))
import aiqt_bootstrap  # noqa: E402,F401
from aiqt_corpus import parse_metadata_block  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
OWNERSHIP = ".claude/skills/corpus-management/src/core/ownership.toml"
GENERATED_FILES = frozenset({
    "governance/portal.md",
    "governance/maturity-scorecard.md",
    ".claude/skills/corpus-management/registers/reference-acquisition-manifest.md",
})


class InspectionError(Exception):
    """The staged document cannot be inspected reliably."""


def git(*args):
    env = {**os.environ, "GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0"}
    command = shlex.join(["git", "-C", str(ROOT), "-c", "core.fsmonitor=false", *args])
    try:
        result = subprocess.run(["bash", "-c", command], capture_output=True,
                                env=env, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InspectionError(f"cannot run git: {exc}") from exc
    if result.returncode:
        raise InspectionError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def utc_today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def generated_targets():
    """Read the staged compiler ownership register, excluding partial blocks."""
    files = set(GENERATED_FILES)
    trees = []
    raw = git("ls-files", "--stage", "-z", "--", OWNERSHIP)
    if not raw:
        return files, trees
    try:
        entries = raw.rstrip(b"\0").split(b"\0")
        if len(entries) != 1:
            raise ValueError("unmerged ownership register")
        header, path = entries[0].split(b"\t", 1)
        mode, oid, stage = header.decode("ascii").split()
        if stage != "0" or os.fsdecode(path) != OWNERSHIP:
            raise ValueError("invalid ownership index entry")
        register = tomllib.loads(read_document((mode, oid)))
        for entry in register["owned_targets"]:
            kind, target = entry["kind"], entry["target"]
            if not isinstance(target, str) or not target or target.startswith("/") or ".." in target.split("/"):
                raise ValueError("invalid generated target")
            if kind in {"file", "index"}:
                files.add(target)
            elif kind == "tree":
                trees.append(target.rstrip("/") + "/")
            elif kind != "block":
                raise ValueError("unknown generated target kind")
    except (ValueError, KeyError, TypeError) as exc:
        raise InspectionError(f"{OWNERSHIP}: {exc}") from exc
    return files, trees


def staged_documents():
    """Yield index/HEAD document pairs; preserve all Git filename bytes."""
    raw = git("diff", "--cached", "--raw", "--no-abbrev", "-z", "--find-renames",
              "--no-ext-diff", "--no-textconv", "--no-relative",
              "--ita-invisible-in-index", "--")
    if not raw:
        return
    records = raw.split(b"\0")
    if records.pop() != b"":
        raise InspectionError("unterminated staged diff")
    i = 0
    while i < len(records):
        try:
            header, old_path = records[i:i + 2]
            old_mode, new_mode, old_oid, new_oid, status = header.decode("ascii").split()
            if not old_mode.startswith(":"):
                raise ValueError("missing raw diff prefix")
            old_mode = old_mode[1:]
            i += 2
            new_path = old_path
            if status.startswith(("R", "C")):
                new_path = records[i]
                i += 1
            old_path = os.fsdecode(old_path)
            new_path = os.fsdecode(new_path)
        except (ValueError, IndexError, UnicodeError) as exc:
            raise InspectionError(f"invalid staged diff: {exc}") from exc
        if status == "U":
            raise InspectionError(f"unmerged index entry: {new_path}")
        if status in {"A", "D"}:
            continue
        if old_path.lower().endswith(".md") or new_path.lower().endswith(".md"):
            yield new_path, (old_mode, old_oid), (new_mode, new_oid)


def read_document(entry):
    mode, oid = entry
    if mode == "000000" and oid and set(oid) == {"0"}:
        return ""
    if mode not in ("100644", "100755"):
        raise InspectionError(f"document is not a regular blob (mode {mode})")
    try:
        return git("cat-file", "blob", oid).decode("utf-8-sig")
    except UnicodeError as exc:
        raise InspectionError("document is not UTF-8") from exc


def unpaired(before, after, today=None):
    """Use the shared metadata head window; compare lines without line numbers."""
    old_block = parse_metadata_block(before)
    new_block = parse_metadata_block(after)
    old, new = old_block.raw_lines, new_block.raw_lines
    if "Version" not in old and "Version" not in new:
        return False

    def line(fields, key):
        return fields[key][1] if key in fields else None

    version_changed = line(old, "Version") != line(new, "Version")
    date_changed = line(old, "Date") != line(new, "Date")
    if version_changed:
        return new_block.fields.get("Date", "").strip() != (today or utc_today())
    return date_changed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pre-commit", action="store_true", help="check the staged snapshot")
    parser.parse_args(argv)
    findings = []
    try:
        documents = list(staged_documents())
        files, trees = generated_targets() if documents else (set(), [])
    except InspectionError as exc:
        print(f"Version-Date commit check: cannot inspect staged index: {exc}", file=sys.stderr)
        return 2
    today = utc_today()
    for path, before, after in documents:
        if path in files or any(path.startswith(prefix) for prefix in trees):
            continue
        try:
            if unpaired(read_document(before), read_document(after), today):
                findings.append(path)
        except InspectionError as exc:
            print(f"Version-Date commit check: cannot inspect {path!r}: {exc}", file=sys.stderr)
            return 2
    for path in findings:
        print(f"FAIL {path!r}: a Version edit requires Date {today}; a Date-only edit requires a Version edit. Re-stage the document.")
    if findings:
        return 1
    print("OK: staged Version and Date edits satisfy the UTC date rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
