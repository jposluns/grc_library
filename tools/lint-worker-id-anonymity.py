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

# Character classes keep the source itself free of matching example paths. Separators may be
# "-", "_" or ".", repeated; a family token may follow "_" (3b97 QA r1, r4).
FAMILY = r"(?<![A-Za-z0-9])(claude|codex|gemini)[-_.]+"
ALIAS = re.compile(r"(?:acct|acct-[a-z0-9]|orchestrator|example)", re.I)
RULES = (
    ("R1", re.compile(
        r"(?<![A-Za-z0-9])orch[-_]accounts[\\/]+(?:\.{1,2}[\\/]+)*(?!\.{1,2}[\\/])(?:(?!orch[-_]accounts)[^\\/\n`'\x22()<>\[\]])+"
        r"[\\/]+(?:\.{1,2}[\\/]+)*(?P<account>[A-Za-z0-9._-]+)",
        re.I,
    )),
    # A plan word followed by at least two "-" or "_" segments: every real account name has two, so
    # one-word product names (gemini-enterprise, claude.max_tokens) are not findings (3b97 QA r2).
    # Longer slugs and flags of that shape ARE reported: a parameter-word list removed few of them
    # and let an account whose name starts with such a word through (3b97 QA r3). "pro" and "api"
    # are left out as real product and model names; such an account is still caught by R3, or by R4
    # when a name segment that does not start with a digit carries its timestamp.
    ("R2", re.compile(
        FAMILY + r"(team|max|plus|aistudio|vertex|enterprise|business|personal|work)[-_]+"
        r"[a-z0-9]+([-_]+[a-z0-9]+)+", re.I,
    )),
    ("R3", re.compile(FAMILY + r"[a-z0-9._-]*worker[-_.]?[0-9]+(?![0-9])", re.I)),
    ("R4", re.compile(
        # A model id (a model word then a digit-led part, or a digit-led first part) is not an account
        # identifier; a model word followed by a name is (3b97 QA r4).
        FAMILY + r"(?!(opus|sonnet|haiku|fable|pro|flash|ultra|nano)[-_.]+[0-9]|[0-9])[a-z0-9]+([-_.]+[a-z0-9]+)*[-_.]+"
        r"(20[0-9]{6}([T_-]?[0-9]{4,6}Z?)?|20[0-9]{2}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:?[0-9]{2}(:?[0-9]{2})?Z?)?"
        r"|[0-9]{10,13})(?![0-9])", re.I,
    )),
    ("R5", re.compile(r"(?:/|(?<![A-Za-z0-9]))(worker-registry|orch-worker-broker)[\\/][^\s\"'`)\]>]*", re.I)),
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
        # The path itself is scanned too: a name in a file or directory name is as public as its
        # content (3b97 QA r1). Line 0 marks a path finding.
        findings += [(0, rule, match) for _, rule, match in scan_bytes(rel.encode("utf-8"))
                     if rule != "UTF8"]
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
