#!/usr/bin/env python3
"""Validation-sweep pre-flight scanner.

A deterministic, regex-based scanner that runs BEFORE the validation-sweep
skill's parallel subagent fan-out, surfacing candidate findings for the
shapes mechanical gates do not directly catch. Designed as a lower-cost
filter pass: each subagent receives the pre-flight candidates as known-
suspect locations to verify or dismiss, rather than rediscovering them
unaided.

Distinct from the corpus mechanical gates (gate 39 cross-file gate-count
consistency, gate 40 version-bump recency, gate 41 collection enumeration,
gate 42 external-overlay licence):
- The gates BLOCK on failure; this scanner is INFORMATIONAL (exit 0
  always, like other exploratory tools).
- The gates target high-precision shapes; this scanner targets
  high-recall shapes likely to have false positives requiring
  semantic triage by a subagent.
- The gates run on every audit cycle; this scanner runs on
  `/validation-sweep` invocations and on demand.

Seed patterns (extensible; add new shapes here as the validation-sweep
history register accumulates findings):

  PF-01 stale-skill-count: "N skills" / "N pack skills" where N is not
        the actual count of subdirectories under
        dev-security/claude-rules/skills/.
  PF-02 stale-rule-count: "N rules" / "N governance rules" where N is
        not the actual count of *.md files under
        dev-security/claude-rules/governance/.
  PF-03 stale-collection-mention: any "N <collection-name>" where N is
        a digit and <collection-name> matches a known collection from
        the validation-sweep skill's collection list, and N does not
        match the canonical count.

Output format: structured findings on stdout that a subagent can
consume as a checklist. Each finding has: pattern_id, file_path, line,
captured text, expected value.

Stdlib-only Python 3.11. Exit code 0 always (informational tool).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, read_text_safe


# Canonical sources for collection counts. Each entry: (collection-name,
# directory path relative to REPO_ROOT, item-filter callable).
CANONICAL_COLLECTIONS: list[tuple[str, str, str]] = [
    ("skills", "dev-security/claude-rules/skills", "dir"),
    ("rules", "dev-security/claude-rules/governance", "md"),
]

# Files exempt from this scanner (CHANGELOG history, the scanner itself,
# generated artefacts).
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
        "tools/sweep-preflight-scanner.py",  # the docstring describes patterns
        "tests/test_linters.py",  # may contain fixture strings
    }
)

# Number-word to digit mapping for catching prose-form counts.
NUMBER_WORDS: dict[str, int] = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}


class Finding(NamedTuple):
    pattern_id: str
    path: str
    line: int
    captured: str
    expected: str
    text: str


def count_collection(collection_dir: str, item_filter: str) -> int | None:
    """Return the canonical count of items in a collection directory."""
    dir_path = REPO_ROOT / collection_dir
    if not dir_path.is_dir():
        return None
    if item_filter == "dir":
        return sum(
            1 for entry in dir_path.iterdir()
            if entry.is_dir() and not entry.name.startswith(".")
        )
    if item_filter == "md":
        return sum(
            1 for entry in dir_path.iterdir()
            if entry.is_file()
            and entry.name.endswith(".md")
            and not entry.name.startswith(".")
        )
    return None


def iter_targets() -> list[Path]:
    targets: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        parts = set(path.relative_to(REPO_ROOT).parts)
        if parts & DEFAULT_EXEMPT_DIRS:
            continue
        if rel in EXEMPT_FILES:
            continue
        targets.append(path)
    return sorted(targets)


def scan_collection_counts(
    targets: list[Path],
    canonical: dict[str, int],
) -> list[Finding]:
    """Pattern PF-01 / PF-02 / PF-03: 'N skills' / 'N rules' / 'N foo'."""
    findings: list[Finding] = []
    for name, canonical_count in canonical.items():
        # Digit form: "N <name>"
        digit_re = re.compile(rf"\b(\d+)\s+{re.escape(name)}\b", re.IGNORECASE)
        # Word form: "<word> <name>"
        word_re = re.compile(
            r"\b(" + "|".join(NUMBER_WORDS.keys()) + r")\s+" + re.escape(name) + r"\b",
            re.IGNORECASE,
        )
        for path in targets:
            text = read_text_safe(path)
            if text is None:
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            for lineno, line in enumerate(text.splitlines(), start=1):
                for m in digit_re.finditer(line):
                    captured = int(m.group(1))
                    if captured != canonical_count:
                        findings.append(
                            Finding(
                                pattern_id=f"PF-collection-{name}",
                                path=rel,
                                line=lineno,
                                captured=str(captured),
                                expected=str(canonical_count),
                                text=line.strip()[:120],
                            )
                        )
                for m in word_re.finditer(line):
                    word = m.group(1).lower()
                    captured = NUMBER_WORDS[word]
                    if captured != canonical_count:
                        findings.append(
                            Finding(
                                pattern_id=f"PF-collection-{name}-word",
                                path=rel,
                                line=lineno,
                                captured=word,
                                expected=str(canonical_count),
                                text=line.strip()[:120],
                            )
                        )
    return findings


def main(argv: list[str]) -> int:
    canonical: dict[str, int] = {}
    for name, directory, item_filter in CANONICAL_COLLECTIONS:
        count = count_collection(directory, item_filter)
        if count is not None:
            canonical[name] = count

    targets = iter_targets()
    findings = scan_collection_counts(targets, canonical)

    print(
        f"Pre-flight scanner: {len(targets)} files scanned, "
        f"{len(canonical)} canonical collections tracked.\n"
    )

    if not findings:
        print("No candidate findings. Sweep subagents proceed unhinted.")
        return 0

    # Group by file for readability.
    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.path, []).append(f)

    print(
        f"{len(findings)} candidate finding(s) across {len(by_file)} file(s). "
        f"Subagents should verify or dismiss each.\n"
    )
    for path in sorted(by_file):
        print(f"--- {path} ---")
        for f in by_file[path]:
            print(
                f"  L{f.line} [{f.pattern_id}] captured '{f.captured}', "
                f"expected '{f.expected}': {f.text}"
            )
        print()

    print(
        "Note: these are CANDIDATES, not verified findings. Many will be "
        "legitimate historical references (CHANGELOG-shape text in prose, "
        "comparative wording, etc.). Each candidate needs subagent semantic "
        "triage; the scanner's value is in catching what the high-precision "
        "gates miss, not in adjudicating intent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
