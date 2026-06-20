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

Noise reduction (added 2026-06-20):
- Heuristic context-aware skips: section references (`Section N`),
  legal bill references (`AB 1394`), year-adjacent legal references
  (`The 2025 Rules`), version-history table rows (markdown rows with
  both version-shape and date-shape strings), historical-narrative
  keywords (`completed at`, `now ships`, `previously`).
- Exemption file at tools/sweep-preflight-exemptions.json: per-entry
  (path, pattern_id, line_hash, reason) records that suppress unique
  edge cases the heuristics miss. Stable under line-number drift; the
  line_hash is SHA-256 of the stripped line content.

Output format: structured findings on stdout that a subagent can
consume as a checklist. Each finding has: pattern_id, file_path, line,
captured text, expected value.

Stdlib-only Python 3.11. Exit code 0 always (informational tool).
"""

from __future__ import annotations

import hashlib
import json
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
        "tools/sweep-preflight-scanner.py",  # docstring describes patterns
        "tests/test_linters.py",  # may contain fixture strings
    }
)

# Path to the exemption file (JSON, stdlib-friendly).
EXEMPTION_FILE = "tools/sweep-preflight-exemptions.json"

# Number-word to digit mapping for catching prose-form counts.
NUMBER_WORDS: dict[str, int] = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}

# Heuristic context tokens that flag a line as historical narrative.
HISTORICAL_KEYWORDS = (
    "completed at", "now ships", "previously", "past ", "originally",
    "historically", "earlier", "before gate", "before the gate",
)

# Section-like prefixes that flag the matched number as a non-count reference.
SECTION_PREFIXES = (
    "Section", "Article", "Phase", "Title", "Chapter", "Part", "Step",
)


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


def line_hash(line: str) -> str:
    """Stable hash of the stripped line content for exemption keying."""
    return hashlib.sha256(line.strip().encode("utf-8")).hexdigest()[:16]


def load_exemptions() -> dict[tuple[str, str], set[str]]:
    """Load the exemption file. Returns {(path, pattern_id): {line_hash, ...}}.

    File format (JSON):
      {
        "exemptions": [
          {
            "path": "<file>",
            "pattern_id": "<PF-...>",
            "line_hash": "<sha256[:16] of stripped line content>",
            "reason": "<short rationale>"
          },
          ...
        ]
      }
    """
    exemption_path = REPO_ROOT / EXEMPTION_FILE
    if not exemption_path.is_file():
        return {}
    try:
        data = json.loads(exemption_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    exemptions: dict[tuple[str, str], set[str]] = {}
    for entry in data.get("exemptions", []):
        key = (entry["path"], entry["pattern_id"])
        exemptions.setdefault(key, set()).add(entry["line_hash"])
    return exemptions


def is_exempt_by_heuristic(
    line: str, match_start: int, match_end: int, captured: str
) -> tuple[bool, str]:
    """Heuristic context-aware exemption.

    Returns (skip, reason). When skip is True, the finding is suppressed.
    Heuristics are precision-tuned: they should only catch shapes that
    are unambiguously not stale-count claims.
    """
    before = line[:match_start]
    after = line[match_end:]
    matched = line[match_start:match_end]
    stripped = line.strip()

    # H1: matched number is preceded by a section-like word
    # ("Section 13", "Article 4", "Phase 2", "Chapter 7", "Step 3")
    last_word = before.rstrip().split()[-1] if before.rstrip() else ""
    if last_word.rstrip(".,;:") in SECTION_PREFIXES:
        return True, "section-prefix"

    # H1b: matched number is part of a hyphenated compound
    # ("under-14 rules", "1-5 rules", "post-9 weeks")
    if before.endswith("-"):
        return True, "hyphenated-compound"

    # H2: legal bill / act reference ("AB 1394", "SB 234", "HB 41",
    # "Bill 1394", "Act 4")
    if re.search(r"\b([A-Z]{1,3}|Bill|Act)\s+$", before):
        return True, "legal-bill-reference"

    # H3: 4-digit year matched with a title-cased legal-shape noun
    # inside the match ("The 2025 Rules", "2024 Directive"). The collection
    # name (Rules / Act / etc.) is inside the matched span, so detect via
    # case sensitivity of the matched text rather than via after-context.
    if re.match(r"^(19|20)\d{2}$", captured) and re.search(
        r"\s+(Rules|Act|Regulation|Directive|Code|Law|Amendment)\b",
        matched,
    ):
        return True, "year-legal-reference"

    # H4: markdown version-history table row: starts with `|`, contains
    # both a version-shape and a date-shape (or YYYY.MM.NN library
    # version)
    if stripped.startswith("|") and re.search(
        r"\b\d+\.\d+(\.\d+|\.\w+)?\b", stripped
    ) and re.search(
        r"\b\d{4}-\d{2}-\d{2}\b|\b\d{4}\.\d{2}\.\d+\b", stripped
    ):
        return True, "version-history-table-row"

    # H5: historical-narrative keyword anywhere in the line
    line_lower = line.lower()
    for kw in HISTORICAL_KEYWORDS:
        if kw in line_lower:
            return True, f"historical-narrative-keyword:{kw.strip()}"

    _ = after  # context reserved for future heuristics
    return False, ""


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
    exemptions: dict[tuple[str, str], set[str]],
) -> tuple[list[Finding], int, int]:
    """Pattern PF-01 / PF-02 / PF-03: 'N skills' / 'N rules' / 'N foo'.

    Returns (findings, heuristic_skips, exemption_skips).
    """
    findings: list[Finding] = []
    heuristic_skips = 0
    exemption_skips = 0
    for name, canonical_count in canonical.items():
        # Digit form: "N <name>"
        digit_re = re.compile(rf"\b(\d+)\s+{re.escape(name)}\b", re.IGNORECASE)
        # Word form: "<word> <name>"
        word_re = re.compile(
            r"\b(" + "|".join(NUMBER_WORDS.keys()) + r")\s+" + re.escape(name) + r"\b",
            re.IGNORECASE,
        )
        digit_pattern_id = f"PF-collection-{name}"
        word_pattern_id = f"PF-collection-{name}-word"
        for path in targets:
            text = read_text_safe(path)
            if text is None:
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            for lineno, line in enumerate(text.splitlines(), start=1):
                for m in digit_re.finditer(line):
                    captured = m.group(1)
                    if int(captured) == canonical_count:
                        continue
                    skip, _reason = is_exempt_by_heuristic(
                        line, m.start(), m.end(), captured
                    )
                    if skip:
                        heuristic_skips += 1
                        continue
                    if line_hash(line) in exemptions.get(
                        (rel, digit_pattern_id), set()
                    ):
                        exemption_skips += 1
                        continue
                    findings.append(
                        Finding(
                            pattern_id=digit_pattern_id,
                            path=rel,
                            line=lineno,
                            captured=captured,
                            expected=str(canonical_count),
                            text=line.strip()[:120],
                        )
                    )
                for m in word_re.finditer(line):
                    word = m.group(1).lower()
                    captured = NUMBER_WORDS[word]
                    if captured == canonical_count:
                        continue
                    skip, _reason = is_exempt_by_heuristic(
                        line, m.start(), m.end(), word
                    )
                    if skip:
                        heuristic_skips += 1
                        continue
                    if line_hash(line) in exemptions.get(
                        (rel, word_pattern_id), set()
                    ):
                        exemption_skips += 1
                        continue
                    findings.append(
                        Finding(
                            pattern_id=word_pattern_id,
                            path=rel,
                            line=lineno,
                            captured=word,
                            expected=str(canonical_count),
                            text=line.strip()[:120],
                        )
                    )
    return findings, heuristic_skips, exemption_skips


def main(argv: list[str]) -> int:
    canonical: dict[str, int] = {}
    for name, directory, item_filter in CANONICAL_COLLECTIONS:
        count = count_collection(directory, item_filter)
        if count is not None:
            canonical[name] = count

    exemptions = load_exemptions()
    targets = iter_targets()
    findings, heuristic_skips, exemption_skips = scan_collection_counts(
        targets, canonical, exemptions
    )

    suppressed_total = heuristic_skips + exemption_skips
    print(
        f"Pre-flight scanner: {len(targets)} files scanned, "
        f"{len(canonical)} canonical collections tracked, "
        f"{suppressed_total} candidate(s) suppressed "
        f"({heuristic_skips} by heuristic, {exemption_skips} by exemption file).\n"
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
    print(
        "\nTo suppress a known-false-positive candidate that the heuristics "
        "do not catch, add an entry to tools/sweep-preflight-exemptions.json "
        "with the file path, pattern_id, and line_hash (16-char sha256 prefix "
        "of the stripped line content)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
