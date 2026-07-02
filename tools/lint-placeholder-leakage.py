#!/usr/bin/env python3
"""Detect placeholder leakage in production library documents.

A library document containing placeholder markers is either a stub
leaked into production or a template artefact that escaped its template
directory. Either case is a credibility problem for adopters.

Patterns currently detected (PATTERNS):

  - Words: ``TODO``, ``TBD``, ``FIXME``, ``XXX``, ``Coming soon``,
    ``(placeholder)``.
  - Markers: ``[Unverified]``.
  - Angle-bracket placeholders: ``<YYYY-MM-DD>``, ``<role>``,
    ``<organisation>``, ``<organization>``, ``<name>``, ``<date>``,
    ``<version>``.

Exemptions are layered:

  - EXEMPT_FILES: by filename — CHANGELOG.md, TODO.md, the master spec,
    the ingestion spec, the citation-verification spec, the
    audit-programme spec, the citation-verification worklist template,
    the coverage-gaps register (uses ``TODO backlog: <topic>``
    planned-target references by design), the decision tree, and the linter scripts that enumerate
    these patterns.
  - EXEMPT_DIR_PARTS: by directory — ``.git``, ``node_modules``,
    ``__pycache__``, ``claude-rules`` (its rule files use angle-bracket
    placeholders as documentation of command syntax).
  - Filename-prefix exemptions: files beginning with ``template-`` or
    ``worklist-`` are auto-exempt because their purpose is to carry
    fill-in markers.
  - Fenced code blocks are skipped so example syntax does not produce
    false positives.

Usage:
    python3 tools/lint-placeholder-leakage.py
    python3 tools/lint-placeholder-leakage.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

# Filenames whose content legitimately mentions these markers.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "specification-citation-verification.md",
    # The Audit Programme Specification discusses the placeholder linter's
    # rule set and references TODO.md by name; both produce false positives.
    "specification-audit-programme.md",
    # The coverage-gaps register uses "TODO backlog: <topic>" planned-target
    # references to TODO.md items; this is by design, not leakage.
    "register-coverage-gaps.md",
    # The decision tree references TODO.md and coverage gaps by name.
    "decision-tree.md",
}
# Note (Phase 23.59): three linter-script entries (lint-shall-near-
# uncertainty.py, lint-placeholder-leakage.py, lint-language.py) and
# the template-citation-verification-worklist.md entry were removed.
# The .py entries were unreachable because is_exempt short-circuits
# on `suffix != ".md"` (line 119) before the EXEMPT_FILES check.
# The template- entry was redundant with the template- filename-prefix
# carve-out below.

# Directories whose content is exempt. The default set
# (``.git``/``node_modules``/``__pycache__``) plus ``claude-rules``,
# where rule files use angle-bracket placeholders as documentation of
# command syntax, not as template-fill markers.
EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS | {"claude-rules"}

# Patterns whose presence indicates a placeholder leak. Each pattern uses
# word boundaries or angle-bracket-syntax to avoid false matches on prose.
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
    # Phase 23.63: template-placeholder organization domains. These
    # strings are legitimate in template- / worklist- prefixed files
    # (exempted via the filename-prefix carve-out below) but flag
    # everywhere else as leaked template content. They are also kept
    # in lint-pii-in-content.py EXAMPLE_DOMAINS so the PII linter
    # does NOT flag them as suspected PII (a placeholder is not real
    # personal data); the production-leak concern is enforced here
    # instead.
    (re.compile(r"\byourcompany\.com\b"), "yourcompany.com placeholder"),
    (re.compile(r"\byour-org\.com\b"), "your-org.com placeholder"),
    (re.compile(r"\byour-org\.example\.com\b"), "your-org.example.com placeholder"),
]


def is_exempt(path: Path) -> bool:
    """Return True if the file should be skipped."""
    if path.name in EXEMPT_FILES:
        return True
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return True
    # Template documents legitimately contain placeholders.
    if path.name.startswith("template-"):
        return True
    # Worklist documents contain intentional blank fields for human completion.
    if path.name.startswith("worklist-"):
        return True
    # Only scan markdown documents.
    if path.suffix != ".md":
        return True
    return False


def iter_targets(paths: list[str]) -> list[Path]:
    """Walk supplied paths and return markdown files to scan."""
    targets: list[Path] = []
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if not is_exempt(f):
                    targets.append(f)
    # Remove duplicates while preserving order
    seen = set()
    out = []
    for t in targets:
        if t in seen:
            continue
        seen.add(t)
        if not is_exempt(t):
            out.append(t)
    return out


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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect placeholder leakage in production library documents."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=DEFAULT_PATHS,
        help="Files or directories to scan (default: whole repo).",
    )
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
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
            rel = path.relative_to(REPO_ROOT)
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
