#!/usr/bin/env python3
"""On-demand instruction-cut ledger check; stdlib-only Python 3.11.

Usage:
    python3 tools/check-clause-preservation.py --base REV --path FILE --extract
    python3 tools/check-clause-preservation.py --base REV --path FILE --ledger LEDGER

--extract prints a JSON ledger template, initially all K. Review every row.
A clause is a complete physical BASE line, excluding its LF terminator.
Selection includes keywords, dates, maintainer mentions, hook/gate/lint
references, tool filenames and Markdown headings (including setext titles).
Fences and quotations are included. Untagged wrapped continuations are not:
this is a lexical inventory, not proof of semantic or whole-file preservation.

Ledger keys: base_revision (resolved commit ID), base_path, clauses.
Row keys: base_line (1-based), base_quote, state, quote, destination.
K = unchanged in the base path; M = unchanged elsewhere; S = superseded or
compressed, requiring human equivalence review. All states need a nonempty
quote verbatim in a regular UTF-8 file at committed HEAD. K/M require the
complete base quote. Whitespace/case matter; repeated lines need separate rows.
HEAD is resolved once. Dirty/index/untracked content cannot satisfy a row.

Exit 0: complete lexical evidence; 1: preservation findings; 2: input/git error.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRIGGER = re.compile(
    r"\b(?:must|never|always|required|maintainer|hooks?|gates?|lints?)\b"
    r"|\b\d{4}-\d{2}-\d{2}\b"
    r"|\b(?:lint|check|block)-[\w.-]+|\bD\d+\b"
    r"|\b(?:PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd|"
    r"PreCompact|SubagentStart|SubagentStop|Stop|Notification)\b"
    r"|\b(?:pre-commit|pre-push|commit-msg|post-checkout)\b",
    re.IGNORECASE,
)
ATX = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
SETEXT = re.compile(r"^ {0,3}(?:=+|-+)[ \t\r]*$")
ROW_KEYS = {"base_line", "base_quote", "state", "quote", "destination"}


def clauses(text: str) -> dict[int, str]:
    """Preserve physical lines; include headings to retain cadence/context."""
    lines = text.split("\n")
    selected = {}
    for index, line in enumerate(lines):
        title = (line.strip() and index + 1 < len(lines)
                 and SETEXT.fullmatch(lines[index + 1]))
        if TRIGGER.search(line) or ATX.match(line) or title:
            selected[index + 1] = line
    return selected


def repo_path(value: str) -> str:
    if (not isinstance(value, str) or not value or value.startswith("/")
            or any(c in value for c in "\\\0\n\r:")
            or any(p in {"", ".", "..", ".git"} for p in value.split("/"))):
        raise ValueError(f"expected canonical repository-relative path: {value!r}")
    return value


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--literal-pathspecs", "-C", str(root), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def commit(root: Path, revision: str) -> str:
    return git(root, "rev-parse", "--verify", "--end-of-options",
               revision + "^{commit}").decode("ascii").strip()


def read_blob(root: Path, revision: str, path: str) -> str:
    records = git(root, "ls-tree", "-z", revision, "--", repo_path(path))
    entries = [entry for entry in records.split(b"\0") if entry]
    if len(entries) != 1:
        raise FileNotFoundError(f"{revision}:{path}: missing regular file")
    metadata, name = entries[0].split(b"\t", 1)
    mode, kind, oid = metadata.split()
    if (name.decode("utf-8") != path or kind != b"blob"
            or mode not in {b"100644", b"100755"}):
        raise ValueError(f"{revision}:{path}: expected regular file (no symlinks)")
    text = git(root, "cat-file", "blob", oid.decode("ascii")).decode("utf-8")
    if "\0" in text:
        raise ValueError(f"{revision}:{path}: NUL in text")
    return text


def unique_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate_ledger(data: object, base: str, path: str) -> list[dict]:
    if (not isinstance(data, dict)
            or set(data) != {"base_revision", "base_path", "clauses"}
            or data["base_revision"] != base or data["base_path"] != path
            or not isinstance(data["clauses"], list)):
        raise ValueError("ledger needs matching resolved base_revision, base_path and clauses")
    for row in data["clauses"]:
        if not isinstance(row, dict) or set(row) != ROW_KEYS:
            raise ValueError(f"row must have exactly {sorted(ROW_KEYS)}")
        if type(row["base_line"]) is not int or row["base_line"] < 1:
            raise ValueError("base_line must be a positive integer")
        if not isinstance(row["state"], str) or row["state"] not in {"K", "M", "S"}:
            raise ValueError("state must be K, M or S")
        for key in ("base_quote", "quote"):
            if (not isinstance(row[key], str) or not row[key].strip()
                    or "\0" in row[key]):
                raise ValueError(f"{key} must be nonempty text without NUL")
        repo_path(row["destination"])
    return data["clauses"]


def check(root: Path, head: str, path: str, expected: dict[int, str],
          rows: list[dict]) -> list[str]:
    findings, seen, destinations = [], set(), {}
    for row in rows:
        line = row["base_line"]
        label = f"{path}:{line}"
        if line in seen:
            findings.append(f"{label}: duplicate ledger row")
        seen.add(line)
        if line not in expected:
            findings.append(f"{label}: not an extracted base clause")
            continue
        if row["base_quote"] != expected[line]:
            findings.append(f"{label}: base_quote differs from BASE")
        state, destination, quote = row["state"], row["destination"], row["quote"]
        if state in {"K", "M"} and quote != expected[line]:
            findings.append(f"{label}: {state} requires complete verbatim base quote; use S")
        if state == "K" and destination != path:
            findings.append(f"{label}: K must stay in {path}; use M")
        if state == "M" and destination == path:
            findings.append(f"{label}: M must name a different destination; use K")
        if destination not in destinations:
            try:
                destinations[destination] = read_blob(root, head, destination)
            except FileNotFoundError:
                destinations[destination] = None
        surviving = destinations[destination]
        if surviving is None or quote not in surviving:
            findings.append(f"{label}: {state} quote not found verbatim at HEAD:{destination}")
    for line in sorted(expected.keys() - seen):
        findings.append(f"{path}:{line}: missing ledger row")
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--base", required=True, help="base git commit or revision")
    parser.add_argument("--path", required=True, help="base repository-relative file")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--extract", action="store_true", help="print JSON ledger template")
    mode.add_argument("--ledger", type=Path, help="JSON file; relative to current directory")
    args = parser.parse_args(argv)
    try:
        root = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip())
        path = repo_path(args.path)
        base = commit(root, args.base)
        expected = clauses(read_blob(root, base, path))
        if not expected:
            raise ValueError("no base clauses extracted; check input and review manually")
        if args.extract:
            rows = [dict(base_line=line, base_quote=quote, state="K", quote=quote,
                         destination=path) for line, quote in expected.items()]
            print(json.dumps(dict(base_revision=base, base_path=path, clauses=rows),
                             indent=2, ensure_ascii=False))
            return 0
        head = commit(root, "HEAD")
        data = json.loads(args.ledger.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
        rows = validate_ledger(data, base, path)
        findings = check(root, head, path, expected, rows)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: clause preservation: {exc}", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"FAIL: {finding}")
    superseded = sum(row["state"] == "S" for row in rows)
    print(f"{'FAIL' if findings else 'OK'}: {len(expected)} clauses; "
          f"{superseded} S rows require semantic review; BASE {base}; HEAD {head}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
