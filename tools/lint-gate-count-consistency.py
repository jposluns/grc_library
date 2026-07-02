#!/usr/bin/env python3
"""Cross-file gate-count consistency audit for the audit programme.

(Name is historical: the gate's primary job is the gate count, but it also
validates word-form governance-rule and skill counts in narrow anchored
idioms, see the WORD-FORM patterns below.)

The audit programme declares its current gate count in the §6 inventory
table of governance/specification-audit-programme.md (one row per gate).
Many other files in the corpus reference that count in prose: "the N
audit gates", "N-gate audit programme", "gates 1-N", and similar
idioms. When a new gate is added, the §6 inventory grows by one row,
but the prose references elsewhere are easy to miss; the failure mode
surfaced in the PR #59 / PR #61 / PR #63 sequence (each pass missed a
different set of references).

This linter scans the corpus for prose phrases that mention a collection
count and verifies the count matches its canonical source. Three
collections are checked: the gate count (the §6 inventory row count), the
governance-rule count (markdown files under dev-security/claude-rules/
governance/), and the skill count (subdirectories of dev-security/
claude-rules/skills/), mirroring gate 41's collection sources. Any
mismatch is flagged.

DIGIT patterns (gate count only):

  P1  ``N-gate``                   matches hyphenated forms ``X-gate``
  P2  ``N audit gates``            matches ``the X audit gates``
  P3  ``gates 1-N`` / ``gates 1--N`` (also handles en-dashes)
  P4  ``gates 1 through N``
  P5  ``all N gates``
  P6  bare ``<two-digit N> gates`` without preceding qualifier, with a
      negative lookahead so ``gate-name`` / ``gate-count`` / ``gates 1-N``
      shapes do not false-positive (added after a Sweep finding)
  P7  ``<two-digit N> <short adjective> gates`` where one short word
      intervenes between the digit and ``gates`` (e.g. ``N corpus
      gates``); same negative lookahead as P6 (added after a follow-on
      Sweep finding where P6 missed an adjective-intervening case)
  P8  ``<N> automated audits`` -- the audit programme referred to by
      its audits rather than its gates; anchors on the exact phrase
      ``automated audits`` (not a bare ``N audits``) to avoid
      false-positives on audit-event counts (added after PR #272's
      /validate-pr found a stale ``<N> automated audits`` phrasing that
      no P1-P7 pattern caught)

WORD-FORM patterns (shipped in #511, closing the then-open word-form
backlog item: the gate-39-blind word-form class that
let a stale "fifty-seven" survive in the guardrail-review growth narrative
until #510 fixed it by hand). These are deliberately narrow and anchored so
the pervasive small-word-number prose ("one gate, one concern", "two rules
overlap", "Six rules", "the two skills run as a suite") is never matched: a
bare "<word> rules/skills/gates" is NOT a pattern.

  P9   ``<word> audit gates``        word-form sibling of P2 (gate count)
  P10  ``<word>-gate``               word-form sibling of P1 (gate count)
  P11  ``<word> governance rules``   qualified rule count (rule count)
  P12  ``<collection> to <word>``    the growth-narrative TO-target, where
       the collection keyword (rules/skills/gates) selects which count is
       checked; the only skill-count check (a bare "<word> skills" is too
       FP-prone). A word->number map (1-99) resolves the captured word.

A ``## Version history`` section is treated as a frozen change log and
skipped (its rows narrate past changes and legitimately quote superseded
counts), the in-document analogue of CHANGELOG.md being file-exempt.

Captured count is compared to its collection's canonical source. Mismatch
means the prose was not updated when an item was added or retired.

Scope: ``*.md``, ``*.py``, ``*.sh`` files under the repository root,
minus the exempt set (CHANGELOG.md, generated artefacts, regression
fixtures that intentionally embed stale counts).

Exit codes: 0 pass, 1 findings, 2 internal error (canonical §6 not
parseable).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, read_text_safe


SPEC_PATH = REPO_ROOT / "governance" / "specification-audit-programme.md"

# Canonical-count source directories for the word-form collection checks
# (gates come from the §6 inventory row count, parsed separately). These
# mirror gate 41's collection sources so the two gates agree on what counts.
RULES_DIR = REPO_ROOT / "dev-security" / "claude-rules" / "governance"
SKILLS_DIR = REPO_ROOT / "dev-security" / "claude-rules" / "skills"

# Word-number map for the word-form count patterns (P9-P12 below), covering
# 1-99: enough for every current collection size (12 rules, 17 skills, 58
# gates) with headroom. Built from units, teens, and tens plus hyphenated
# compounds (e.g. "fifty-eight"). Used both to build the regex alternation
# and to resolve a captured word to its integer value.
_UNITS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9,
}
_TEENS = {
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19,
}
_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}


def _build_word_to_num() -> dict[str, int]:
    m: dict[str, int] = {}
    m.update(_UNITS)
    m.update(_TEENS)
    m.update(_TENS)
    for tens_word, tens_val in _TENS.items():
        for unit_word, unit_val in _UNITS.items():
            m[f"{tens_word}-{unit_word}"] = tens_val + unit_val
    return m


WORD_TO_NUM: dict[str, int] = _build_word_to_num()

# Regex alternation matching any mapped word-number. Longest keys first so a
# compound ("fifty-eight") is preferred over its tens prefix ("fifty").
_WORDNUM_ALT = "|".join(
    re.escape(w) for w in sorted(WORD_TO_NUM, key=len, reverse=True)
)
_WORDNUM = rf"(?:{_WORDNUM_ALT})"

# Files that legitimately contain stale gate-count references and must
# not be flagged. CHANGELOG.md is the corpus's historical record;
# generated artefacts are derived; the regression-test fixtures
# intentionally embed wrong-N strings to exercise the linter itself.
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
        "tests/test_linters.py",
    }
)

# Note: the validation-sweep history file (now at
# `.working/validate-sweeps/history.md`, relocated within `.working/`
# in PR #118) is a historical-record artefact by purpose; the file is
# in `.working/` which is in `DEFAULT_EXEMPT_DIRS`, so a per-file
# exemption here is not needed.

# Directories whose contents are out of scope for this audit. The
# pack's tests and fixtures may also embed sample counts.
EXEMPT_DIRS: frozenset[str] = DEFAULT_EXEMPT_DIRS | frozenset(
    {"tests/fixtures"}
)

# File suffixes the linter scans. Markdown is the primary surface;
# Python and shell scripts are included because their docstrings and
# top-of-file comments frequently cite the gate count.
SCAN_SUFFIXES: frozenset[str] = frozenset({".md", ".py", ".sh"})


# Patterns: each is a compiled regex with one capturing group for the
# numeric count. Patterns are matched against non-code-block prose
# only (fenced code blocks would carry too many false positives, e.g.
# scripts referencing test-fixture counts in code comments).
# Each pattern carries a ``kind`` tag controlling how a match resolves to a
# (target-collection, captured-count) pair:
#   "gate_digit" -- group 1 is a digit; target is the gate count.
#   "gate_word"  -- group 1 is a word-number; target is the gate count.
#   "rule_word"  -- group 1 is a word-number; target is the rule count.
#   "growth"     -- group 1 is a collection keyword (rules/skills/gates) and
#                   group 2 is a word-number; target is chosen by group 1.
# The word-form patterns (P9-P12) are deliberately narrow and anchored so the
# pervasive small-word-number prose ("one gate, one concern", "two rules
# overlap", "Six rules", "two skills run as a suite") is never matched: a bare
# "<word> rules/skills/gates" is NOT a pattern; only the qualified
# ("governance rules", "audit gates", "N-gate") and growth-narrative
# ("rules/skills/gates to <word>") shapes are.
PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("N-gate", re.compile(r"\b(\d+)-gate\b", re.IGNORECASE), "gate_digit"),
    ("N audit gates", re.compile(r"\b(\d+)\s+audit\s+gates?\b", re.IGNORECASE), "gate_digit"),
    (
        "gates 1-N",
        re.compile(r"\bgates?\s+1[-–—]\s*(\d+)\b", re.IGNORECASE),
        "gate_digit",
    ),
    (
        "gates 1 through N",
        re.compile(r"\bgates?\s+1\s+through\s+(\d+)\b", re.IGNORECASE),
        "gate_digit",
    ),
    ("all N gates", re.compile(r"\ball\s+(\d+)\s+gates?\b", re.IGNORECASE), "gate_digit"),
    # P6: bare "<two-digit number> gates" without preceding qualifier.
    # Narrower than the other patterns and added after a Sweep finding
    # in tools/README.md where prose used a bare "<stale-count> gates"
    # phrasing without an "audit" or "all" qualifier; patterns P1-P5
    # missed it. Requires the captured number to be at least 10 (two
    # digits) to avoid matching small physical-gate references that
    # may legitimately appear (e.g. "5 gates of NAND").
    ("N gates", re.compile(r"\b(\d{2,})\s+gates?(?![-\w])", re.IGNORECASE), "gate_digit"),
    # P7: "<two-digit N> <single-word> gates" where the intervening
    # word is a short adjective (e.g. "<N> corpus gates"; "N audit
    # gates" already covered by P2 but the broader shape needed
    # explicit coverage). Added after a Sweep cycle iteration
    # surfaced a stale-count "<N> corpus gates" prose pattern in
    # both tools/run_all_audits.sh and tools/check-changelog-on-pr.py;
    # P6 missed both because a single word ("corpus") intervenes
    # between the digit and "gates". Negative lookahead matches P6's,
    # plus the intervening word is limited to short (<= 12 char)
    # alphabetic strings to avoid matching unrelated multi-word
    # constructs.
    (
        "N <word> gates",
        re.compile(
            r"\b(\d{2,})\s+[a-z]{2,12}\s+gates?(?![-\w])",
            re.IGNORECASE,
        ),
        "gate_digit",
    ),
    # P8: "<N> automated audits". The audit programme is sometimes
    # referred to by its audits rather than its gates ("the N automated
    # audits"); this idiom carries the gate count but uses "audits" as
    # the noun, so patterns P1-P7 (which all anchor on "gate(s)") miss
    # it. Added after PR #272's /validate-pr cross-reference check found
    # a stale "the <N> automated audits" phrasing in the library-health
    # report template that no P1-P7 pattern caught. Narrow by design: it requires the
    # exact "automated audits" phrasing (not a bare "N audits", which
    # would false-positive on audit-event counts), so it matches only
    # references to the audit programme's gate set.
    (
        "N automated audits",
        re.compile(r"\b(\d+)\s+automated\s+audits?\b", re.IGNORECASE),
        "gate_digit",
    ),
    # P9: word-form "<word> audit gates" -- the word-form sibling of P2,
    # anchored on the "audit gates" qualifier so it never matches a bare
    # "<word> gates" (the pervasive small-number prose). Catches a stale
    # word-form "<word> audit gates" phrase whose word does not resolve to
    # the current gate count.
    (
        "N audit gates (word)",
        re.compile(rf"\b({_WORDNUM})\s+audit\s+gates?\b", re.IGNORECASE),
        "gate_word",
    ),
    # P10: word-form "<word>-gate" -- the word-form sibling of P1.
    (
        "N-gate (word)",
        re.compile(rf"\b({_WORDNUM})-gate\b", re.IGNORECASE),
        "gate_word",
    ),
    # P11: word-form "<word> governance rules" -- anchored on the qualified
    # "governance rules" so it never matches a bare "<word> rules" (the
    # pervasive "two rules overlap", "Six rules" prose). Catches the
    # collection-enumeration docstring's qualified word-form rule-count idiom.
    # Target is the rule count.
    (
        "N governance rules (word)",
        re.compile(rf"\b({_WORDNUM})\s+governance\s+rules?\b", re.IGNORECASE),
        "rule_word",
    ),
    # P12: the growth-narrative shape "<collection> to <word>", where the
    # collection keyword (rules / skills / gates) selects the target count and
    # the trailing word-number is the asserted size. This matches the
    # guardrail-review SKILL's growth sentence ("from <a> rules to <b>, from a
    # handful of skills to <c>, and from a dozen gates to <d>") by capturing
    # only the TO-target after each collection keyword; the rounded FROM
    # values (the "<a> rules", "a dozen gates" starting points) are not
    # matched, so they do not false-positive. This is the only pattern that
    # validates the skills count (a bare "<word> skills" is too FP-prone to
    # gate, e.g. "the two skills run as a suite", so skills are checked only
    # in this anchored growth shape).
    (
        "<collection> to N (word)",
        re.compile(rf"\b(rules|skills|gates)\s+to\s+({_WORDNUM})\b", re.IGNORECASE),
        "growth",
    ),
]


class Finding(NamedTuple):
    path: Path
    line: int
    pattern_name: str
    target: str
    captured: int
    expected: int
    text: str


def count_collection(source_dir: Path, glob: str) -> int:
    """Count items in a collection source directory (mirrors gate 41).

    ``glob`` ``"*.md"`` counts markdown files (the governance rules);
    ``"*/"`` counts immediate subdirectories (the skills). README/index
    files are not part of either collection's item set, so a ``*.md`` count
    excludes a top-level ``README.md`` only if the collection convention
    does (the governance dir holds only rule files, no README)."""
    if not source_dir.is_dir():
        return 0
    if glob == "*.md":
        return sum(1 for p in source_dir.iterdir() if p.is_file() and p.suffix == ".md")
    if glob == "*/":
        return sum(1 for p in source_dir.iterdir() if p.is_dir())
    return 0


def resolve_match(kind: str, match: re.Match) -> tuple[str, int] | None:
    """Return ``(target_collection, captured_count)`` for a pattern match.

    ``target_collection`` is one of ``"gate"`` / ``"rule"`` / ``"skill"``.
    Returns ``None`` if a word-number cannot be mapped (a defensive guard;
    the regex only matches mapped words, so this should not occur)."""
    if kind == "gate_digit":
        return ("gate", int(match.group(1)))
    if kind == "gate_word":
        n = WORD_TO_NUM.get(match.group(1).lower())
        return ("gate", n) if n is not None else None
    if kind == "rule_word":
        n = WORD_TO_NUM.get(match.group(1).lower())
        return ("rule", n) if n is not None else None
    if kind == "growth":
        keyword = match.group(1).lower()
        target = {"rules": "rule", "skills": "skill", "gates": "gate"}[keyword]
        n = WORD_TO_NUM.get(match.group(2).lower())
        return (target, n) if n is not None else None
    return None


def parse_canonical_count() -> int:
    """Parse §6 inventory of the audit-programme spec and return the
    row count.

    The §6 inventory is a markdown table with one row per audit gate.
    The header row is ``| # | Gate | Script |`` followed by a
    separator row of dashes. Data rows have numeric first cells.

    Raises ``RuntimeError`` if the inventory cannot be located or
    parsed.
    """
    text = read_text_safe(SPEC_PATH)
    if text is None:
        raise RuntimeError(f"cannot read {SPEC_PATH}")
    lines = text.splitlines()

    # Locate the §6 inventory header.
    inventory_start = None
    for lineno, line in enumerate(lines):
        if line.strip().startswith("## 6.") and "inventory" in line.lower():
            inventory_start = lineno
            break
    if inventory_start is None:
        raise RuntimeError("§6 inventory header not found in spec")

    # Find the table header row after the §6 header. The header row
    # starts with ``| #`` and contains the column ``Gate``.
    table_start = None
    for lineno in range(inventory_start, len(lines)):
        line = lines[lineno].strip()
        if line.startswith("| #") and "Gate" in line:
            table_start = lineno
            break
    if table_start is None:
        raise RuntimeError("§6 inventory table header not found")

    # Count data rows: after the header and the separator row, each
    # subsequent line beginning with ``|`` and a digit is a data row.
    # Stop at the first non-table line.
    count = 0
    for lineno in range(table_start + 2, len(lines)):
        line = lines[lineno].strip()
        if not line.startswith("|"):
            break
        # First cell is the gate number. Strip the leading ``|`` and
        # whitespace, then check the cell is numeric.
        first_cell = line.split("|", 2)[1].strip() if line.count("|") >= 2 else ""
        if first_cell.isdigit():
            count += 1
        else:
            break
    if count == 0:
        raise RuntimeError("§6 inventory has zero data rows")
    return count


def iter_targets(paths: list[str]) -> list[Path]:
    """Yield scannable files. ``paths`` is a list of repo-relative or
    absolute paths; if a path is a directory, it is walked recursively.
    If ``paths`` is empty, the entire repository root is walked. Exempt
    files and directories are skipped in either mode."""
    targets: list[Path] = []
    seen: set[Path] = set()

    def consider(path: Path) -> None:
        if not path.is_file():
            return
        if path.suffix not in SCAN_SUFFIXES:
            return
        try:
            rel = path.resolve().relative_to(REPO_ROOT).as_posix()
            parts = set(path.resolve().relative_to(REPO_ROOT).parts)
        except ValueError:
            # Path is outside the repo (e.g. a temporary fixture).
            rel = path.as_posix()
            parts = set(path.parts)
        if parts & EXEMPT_DIRS:
            return
        if rel in EXEMPT_FILES:
            return
        if path.resolve() in seen:
            return
        targets.append(path.resolve())
        seen.add(path.resolve())

    roots = [Path(p) for p in paths] if paths else [REPO_ROOT]
    for root in roots:
        root = root.resolve() if root.exists() else root
        if root.is_file():
            consider(root)
        elif root.is_dir():
            for path in root.rglob("*"):
                consider(path)
    return sorted(targets)


def scan_file(path: Path, counts: dict[str, int]) -> list[Finding]:
    """Apply all patterns to a single file's text, returning findings.

    ``counts`` maps each target collection (``"gate"`` / ``"rule"`` /
    ``"skill"``) to its canonical count. Each match resolves to a
    (target, captured) pair via ``resolve_match``; a mismatch against that
    target's canonical count is a finding."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    # A `## Version history` section is a frozen change log: its rows narrate
    # past changes and legitimately quote superseded counts (a new-rule PR row
    # records the old-to-new rule-count correction; a new-gate row advances the
    # word-form gate count). Skip count-matching inside such a section, the
    # in-document analogue of CHANGELOG.md being exempt. The section runs from
    # its heading to the next heading of any level (or EOF).
    in_version_history = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        heading = re.match(r"^#{1,6}\s+(.*)$", line)
        if heading:
            in_version_history = "version history" in heading.group(1).lower()
            continue
        if in_version_history:
            continue
        for pattern_name, pattern, kind in PATTERNS:
            for match in pattern.finditer(line):
                resolved = resolve_match(kind, match)
                if resolved is None:
                    continue
                target, captured = resolved
                expected = counts[target]
                if captured == expected:
                    continue
                findings.append(
                    Finding(
                        path=path,
                        line=lineno,
                        pattern_name=pattern_name,
                        target=target,
                        captured=captured,
                        expected=expected,
                        text=line.strip(),
                    )
                )
    return findings


def main(argv: list[str]) -> int:
    try:
        gate_count = parse_canonical_count()
    except RuntimeError as exc:
        print(f"ERROR: cannot determine canonical gate count: {exc}", file=sys.stderr)
        return 2

    counts = {
        "gate": gate_count,
        "rule": count_collection(RULES_DIR, "*.md"),
        "skill": count_collection(SKILLS_DIR, "*/"),
    }

    paths = argv[1:]
    targets = iter_targets(paths)
    all_findings: list[Finding] = []
    for path in targets:
        all_findings.extend(scan_file(path, counts))

    if not all_findings:
        print(
            f"OK: collection-count references consistent across {len(targets)} files "
            f"(gates {counts['gate']}, governance rules {counts['rule']}, "
            f"skills {counts['skill']}; digit and word-form)."
        )
        return 0

    # Group findings by file for readable output.
    by_file: dict[Path, list[Finding]] = {}
    for finding in all_findings:
        by_file.setdefault(finding.path, []).append(finding)
    for path in sorted(by_file):
        # A finding on an out-of-repo target (e.g. a regression fixture in a
        # tmp dir) is not relative to REPO_ROOT; fall back to the raw path
        # rather than crashing (mirrors iter_targets' guard).
        try:
            rel = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        print(f"=== {rel} ===")
        for finding in by_file[path]:
            print(
                f"  L{finding.line} [{finding.pattern_name}] "
                f"{finding.target} count: captured {finding.captured}, "
                f"expected {finding.expected}: {finding.text[:120]}"
            )
    print(
        f"\nFAIL: {len(all_findings)} stale collection-count reference(s) across "
        f"{len(by_file)} file(s).",
        file=sys.stderr,
    )
    print(
        f"Canonical counts: {counts['gate']} gates (§6 inventory of "
        f"{SPEC_PATH.relative_to(REPO_ROOT)}), {counts['rule']} governance rules, "
        f"{counts['skill']} skills. Each finding above shows a prose reference "
        f"that does not match its collection's current count.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
