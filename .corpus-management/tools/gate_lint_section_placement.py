#!/usr/bin/env python3
"""Section-placement audit (grc gate): pack-owned engine (source of record).

Enforce that named sections appear in their required position (near the top, or near
the bottom) of a document. A placement rule names a set of accepted heading spellings,
a position constraint (top-N or bottom-N), and an optional set of document types it
applies to. A rule scoped to document types is checked only for a document of one of
those types; an unscoped rule is checked for every scanned document. Headings are read
outside fenced code blocks.

Engine/wrapper split (compile PR-13): this engine carries the PURE check
(``DOCTYPE_RE``, ``HEADING_RE``, ``extract_doctype``, ``normalise_heading``,
``extract_headings``, ``check_placement``, ``scan``) and a ``run`` that groups +
reports; the project wrapper (``tools/lint-section-placement.py``) supplies the
grc-specific placement rules, the target selection, and the repository root, passing
the rules and root in. This engine holds no project placement-rule or scan-scope policy.

A placement rule is a
``(rule_id, description, accepted_names, (constraint_kind, n), doctypes_or_None)`` tuple.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-section-placement.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

DOCTYPE_RE = re.compile(r"^\*\*Document Type:\*\*\s+(.+?)(?:\\)?\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")


def extract_doctype(text: str) -> str | None:
    m = DOCTYPE_RE.search(text)
    if not m:
        return None
    return m.group(1).strip().rstrip("\\").strip()


def normalise_heading(heading: str) -> str:
    """Return the heading lower-cased with leading numbering stripped."""
    cleaned = re.sub(r"^\d+(\.\d+)*[.\s:]*", "", heading)
    cleaned = re.sub(r"^Section\s+\d+(\.\d+)*[.\s:]*", "", cleaned)
    return cleaned.strip().lower()


def extract_headings(text: str) -> list[tuple[int, str]]:
    """Return the ``##`` section headings as (sequence_index, normalised_heading)."""
    headings: list[tuple[int, str]] = []
    idx = 0
    for _lineno, line in iter_non_code_lines(text):
        m = HEADING_RE.match(line)
        if m:
            headings.append((idx, normalise_heading(m.group(1))))
            idx += 1
    return headings


def check_placement(
    headings: list[tuple[int, str]],
    rule: tuple[str, str, frozenset[str], tuple[str, int], tuple[str, ...] | None],
) -> list[str]:
    """Apply one placement rule against a file's section list."""
    rule_id, description, names, position, _doctypes = rule
    total = len(headings)
    if total == 0:
        return []
    findings: list[str] = []
    for seq, heading in headings:
        if heading not in names:
            continue
        constraint_kind, n = position
        if constraint_kind == "top":
            allowed = seq < n
            if not allowed:
                findings.append(
                    f"[{rule_id}] section #{seq + 1} of {total} "
                    f"({heading!r}) should appear in the top {n} sections; "
                    f"{description}"
                )
        elif constraint_kind == "bottom":
            allowed = seq >= max(0, total - n)
            if not allowed:
                findings.append(
                    f"[{rule_id}] section #{seq + 1} of {total} "
                    f"({heading!r}) should appear in the bottom {n} sections; "
                    f"{description}"
                )
    return findings


def scan(path: Path, placement_rules: list) -> list[str]:
    findings: list[str] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    doctype = extract_doctype(text)
    headings = extract_headings(text)
    if not headings:
        return findings
    for rule in placement_rules:
        _rid, _desc, _pre, _pos, doctypes = rule
        if doctypes is not None:
            if doctype is None or doctype not in doctypes:
                continue
        findings.extend(check_placement(headings, rule))
    return findings


def run(targets: list[Path], placement_rules: list, *, repo_root: Path) -> int:
    grouped: dict[Path, list[str]] = {}
    for t in targets:
        findings = scan(t, placement_rules)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(
            f"OK: all documents satisfy section-placement conventions "
            f"(scanned {len(targets)} files)."
        )
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(repo_root)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for msg in findings:
            print(f"  {msg}")
        total += len(findings)
    print(
        f"\nFAIL: {total} section-placement finding(s) across "
        f"{len(grouped)} file(s)."
    )
    return 1
