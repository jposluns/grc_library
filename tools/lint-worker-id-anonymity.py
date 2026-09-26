#!/usr/bin/env python3
"""Worker-id anonymity audit (gate 103).

Scan tracked working-tree files, including hidden directories and code fences.
No directory exemptions apply. A NUL byte marks binary content; other content
must be UTF-8. Explicit paths are repo-relative and select tracked files only.

Usage:
    python3 tools/lint-worker-id-anonymity.py [path ...]

Exit 0: clean; 1: findings; 2: environment or argument error.
History, split/encoded strings, and arbitrary account names outside account
paths and the plan vocabulary are not checked. Record aliases use family-Wn.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from lint_common import REPO_ROOT, guard_explicit_paths, positional_args

# Character classes keep the source itself free of matching example paths.
FAMILY = r"\b(claude|codex|gemini)-"
ALIAS = re.compile(r"(?:acct|acct-[a-z0-9]|orchestrator|<account>|example)", re.I)
RULES = (
    ("R1", re.compile(
        r"\borch[-]accounts/[^/\s\"'`]+/(?P<account>[^/\s\"'`]+)",
        re.I,
    )),
    ("R2", re.compile(
        FAMILY + r"(team|pro|max|plus|aistudio|vertex|api|enterprise|business|personal)"
        r"\b(-[a-z0-9]+)*", re.I,
    )),
    ("R3", re.compile(FAMILY + r"[a-z0-9-]*worker[0-9]+\b", re.I)),
    ("R4", re.compile(
        FAMILY + r"(?!(opus|sonnet|haiku|fable)\b)[a-z0-9]+(-[a-z0-9]+)*-"
        r"(20\d{6}(T?\d{4,6}Z?)?|\d{10,13})\b", re.I,
    )),
    ("R5", re.compile(r"/(worker-registry|orch-worker-broker)/[^\s\"'`]*", re.I)),
)


def scan_bytes(data: bytes) -> list[tuple[int, str, str]]:
    """Return line, rule and matched text; a decode failure is also a finding."""
    if b"\0" in data:
        return []
    findings: list[tuple[int, str, str]] = []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        line = data[:exc.start].count(b"\n") + 1
        findings.append((line, "UTF8", repr(data[exc.start:exc.end])))
        # Still detect identifiers elsewhere in a malformed text file.
        text = data.decode("utf-8", errors="replace")
    for lineno, line in enumerate(text.split("\n"), 1):
        for rule, pattern in RULES:
            for match in pattern.finditer(line):
                if rule == "R1" and ALIAS.fullmatch(match.group("account")):
                    continue
                findings.append((lineno, rule, match.group(0)))
    return sorted(findings)


def tracked_files() -> list[Path]:
    """Enumerate the index without quoting or splitting whitespace in names."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    return sorted({
        REPO_ROOT / os.fsdecode(name)
        for name in result.stdout.split(b"\0") if name
    })


def select_targets(paths: list[str]) -> list[Path]:
    """Validate explicit inputs, then select from the same tracked-file set."""
    normalized = guard_explicit_paths(paths, repo_root=REPO_ROOT) if paths else []
    tracked = tracked_files()
    if not normalized:
        return tracked
    selected: set[Path] = set()
    for name in normalized:
        root = REPO_ROOT / name
        matches = [p for p in tracked if p == root or root in p.parents]
        if not matches:
            raise ValueError(f"{name}: no tracked files selected")
        selected.update(matches)
    return sorted(selected)


def main(argv: list[str]) -> int:
    paths = positional_args(argv[1:], known_flags=())
    try:
        targets = select_targets(paths)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: cannot enumerate tracked files: {exc}", file=sys.stderr)
        return 2

    count = 0
    errors = False
    for path in targets:
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            findings = scan_bytes(path.read_bytes())
        except OSError as exc:
            print(f"ERROR: {rel}: {exc}", file=sys.stderr)
            errors = True
            continue
        for lineno, rule, match in findings:
            print(f"{rel}:{lineno}: {rule}: {match}")
        count += len(findings)

    if errors:
        return 2
    if count:
        print(f"FAIL: {count} worker-id anonymity finding(s).")
        return 1
    print(f"OK: worker-id anonymity clean across {len(targets)} tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
