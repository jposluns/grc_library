#!/usr/bin/env python3
"""Cross-file gate-count consistency audit (grc gate 39): pack-owned engine (source of record).

A prose reference to a collection size (the audit gates, the governance rules, the skills) must
match that collection's canonical count, or it is a stale-count reference. This engine carries the
PURE check: the count-idiom pattern set (``PATTERNS``: digit and word-form shapes, deliberately
anchored so pervasive small-number prose is never matched), the word-number machinery, the
``Finding`` record, ``count_collection`` (a generic directory item counter), ``resolve_match``, a
``scan_file`` that applies the patterns to one file against a supplied canonical-count map (skipping
a Markdown ``## Version history`` frozen section), and a ``run`` that scans the target set and
reports.

Engine/wrapper split: the project wrapper (``tools/lint-gate-count-consistency.py``) supplies the
grc canonical-count sources (the audit-programme spec path parsed for the §6 gate-inventory row
count, and the rule / skill collection directories), the grc scan scope (default roots, the scanned
suffixes, the exempt-file / exempt-dir policy via ``iter_targets``), and a ``scan_file`` shim (so a
direct-module-load test observes it on the wrapper); it builds the canonical-count map and delegates
the scan + report to this engine, which holds no project path or scan-scope policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more stale-count findings; 2 (wrapper
only) the canonical gate count could not be parsed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    from aiqt_corpus import read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-gate-count-consistency.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc


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
    m["one hundred"] = 100
    m["one-hundred"] = 100
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
        re.compile(r"\bgates?\s+1[-\u2013\u2014]\s*(\d+)\b", re.IGNORECASE),
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


def scan_file(path: Path, counts: dict[str, int]) -> list[Finding]:
    """Apply all patterns to a single file's text, returning findings.

    ``counts`` maps each target collection (``"gate"`` / ``"rule"`` /
    ``"skill"``) to its canonical count. Each match resolves to a
    (target, captured) pair via ``resolve_match``; a mismatch against that
    target's canonical count is a finding."""
    try:
        text = read_text_safe(path)
    except FileNotFoundError:
        # A file can vanish between rglob discovery and read when the
        # regression suite runs concurrently in the same tree and drops a
        # temp fixture (the routed #577 sweep I2); serial CI is unaffected.
        # Treat exactly like an unreadable file: skip.
        return []
    if text is None:
        return []
    findings: list[Finding] = []
    # A `## Version history` section is a frozen change log: its rows narrate
    # past changes and legitimately quote superseded counts (a new-rule PR row
    # records the old-to-new rule-count correction; a new-gate row advances the
    # word-form gate count). Skip count-matching inside such a section, the
    # in-document analogue of CHANGELOG.md being exempt. The section runs from
    # its heading to the next heading of any level (or EOF).
    # The `## Version history` skip and heading detection are a MARKDOWN
    # construct. In a `.py`/`.sh` file a leading ``#`` is a code COMMENT, not a
    # heading, and comment lines frequently carry gate-count idioms (a shell
    # ``# ... N gates ...`` banner, a module-docstring-adjacent comment). Treating
    # a ``#``-comment line as a heading made gate 39 BLIND to a stale count in it
    # (the gate-80 vpr gF6 finding, 3.195 (closing PR #1287): a stale count idiom in a shell comment in
    # tools/quick-guard.sh line 9 that this gate skipped as a "heading"). So the
    # heading / version-history logic is applied to MARKDOWN files only; in a
    # non-markdown file every line (comments included) is scanned, and the
    # tightly-anchored patterns (P1-P12) keep that false-positive-safe.
    is_markdown = path.suffix == ".md"
    in_version_history = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_markdown:
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


def run(targets: list[Path], *, counts: dict[str, int], repo_root: Path, spec_rel: Path) -> int:
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
        # tmp dir) is not relative to repo_root; fall back to the raw path
        # rather than crashing (mirrors iter_targets' guard).
        try:
            rel = path.relative_to(repo_root).as_posix()
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
        f"{spec_rel}), {counts['rule']} governance rules, "
        f"{counts['skill']} skills. Each finding above shows a prose reference "
        f"that does not match its collection's current count.",
        file=sys.stderr,
    )
    return 1
