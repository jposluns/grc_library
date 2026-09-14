#!/usr/bin/env python3
"""Placeholder-leakage audit (grc gate 12): pack-owned engine (source of record).

A production library document containing a placeholder marker is either a stub leaked into
production or a template artefact that escaped its template directory, and either is a credibility
problem for adopters. This engine carries the PURE check: the placeholder-marker pattern set
(``PATTERNS``: TODO / TBD / FIXME / XXX / (placeholder) / [Unverified] / Coming soon, the
angle-bracket ``<role>`` / ``<date>`` / ``<version>`` family, and the template-placeholder
organization domains), a fence-aware ``scan`` (fenced code blocks are skipped so example syntax
does not false-positive), and a ``run`` that groups + reports.

Engine/wrapper split: the project wrapper (``tools/lint-placeholder-leakage.py``) supplies the grc
scan scope (default roots, the markdown selector, the exempt-file / exempt-dir / template- and
worklist- prefix policy via ``iter_targets`` + ``is_exempt``) and filters those files out before
delegating, so this engine holds no project-file policy. The pattern set is a generic
placeholder-marker inventory, like the stub-phrase list of the no-stub-documents engine.

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
        "(python3 tools/lint-placeholder-leakage.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# Patterns whose presence indicates a placeholder leak. Each pattern uses word boundaries or
# angle-bracket-syntax to avoid false matches on prose.
PATTERNS = [
    (re.compile(r"\bTODO\b"), "TODO marker"),
    (re.compile(r"\bTBD\b"), "TBD marker"),
    (re.compile(r"\bFIXME\b"), "FIXME marker"),
    (re.compile(r"\bXXX\b"), "XXX marker"),
    (re.compile(r"<YYYY-MM-DD>"), "<YYYY-MM-DD> placeholder"),
    (re.compile(r"<role>"), "<role> placeholder"),
    (re.compile(r"<organisation>"), "<organisation> placeholder"),
    (re.compile(r"<organization>"), "<organization> placeholder"),
    (re.compile(r"<name>"), "<name> placeholder"),
    (re.compile(r"<date>"), "<date> placeholder"),
    (re.compile(r"<version>"), "<version> placeholder"),
    (re.compile(r"\(placeholder\)", re.IGNORECASE), "(placeholder) marker"),
    (re.compile(r"\[Unverified\]"), "[Unverified] marker"),
    (re.compile(r"\bComing soon\b", re.IGNORECASE), "Coming soon marker"),
    # Template-placeholder organization domains. These strings are legitimate in template- /
    # worklist- prefixed files (exempted via the wrapper's filename-prefix carve-out) but flag
    # everywhere else as leaked template content.
    (re.compile(r"\byourcompany\.com\b"), "yourcompany.com placeholder"),
    (re.compile(r"\byour-org\.com\b"), "your-org.com placeholder"),
    (re.compile(r"\byour-org\.example\.com\b"), "your-org.example.com placeholder"),
]


def scan(path: Path) -> list[tuple[int, str, str]]:
    """Return list of (line number, marker name, line excerpt) findings."""
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for pattern, label in PATTERNS:
            if pattern.search(line):
                excerpt = line.strip()[:140]
                findings.append((lineno, label, excerpt))
                break  # one finding per line is enough
    return findings


def run(targets: list[Path], *, repo_root: Path) -> int:
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: no placeholder leakage (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(repo_root)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, label, excerpt in findings:
            print(f"  L{lineno} [{label}] {excerpt}")
        total += len(findings)
    print(
        f"\nFAIL: {total} placeholder finding(s) across {len(grouped)} file(s)."
    )
    print(
        "Placeholders such as TODO, TBD, FIXME, XXX, or "
        "<YYYY-MM-DD>-style markers should not appear in production library "
        "documents. Either complete the content or move the document to the "
        "template directory (filename prefix `template-`)."
    )
    return 1
