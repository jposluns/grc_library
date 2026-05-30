#!/usr/bin/env python3
"""Detect placeholder leakage in production library documents.

A library document containing `TODO`, `TBD`, `FIXME`, `XXX`,
`<YYYY-MM-DD>`, `<role>`, `<organisation>`, `(placeholder)`, `[Unverified]`,
or "Coming soon" is either a stub leaked into production or a template
artefact that escaped its template directory. Either case is a credibility
problem for adopters.

This linter detects such markers in artefact documents. Templates,
worklists, the TODO file, the CHANGELOG (which describes phases that
discuss these patterns), and the linter source files themselves are
exempt by name.

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

REPO_ROOT = Path(__file__).resolve().parent.parent
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
    "template-citation-verification-worklist.md",
    "lint-shall-near-uncertainty.py",
    "lint-placeholder-leakage.py",
    "lint-language.py",
    # The coverage-gaps register uses "TODO P5.x" markers as cross-references
    # to TODO.md priorities; this is by design, not leakage.
    "register-coverage-gaps.md",
    # The decision tree references TODO.md and coverage gaps by name.
    "decision-tree.md",
}

# Directories whose content is exempt.
EXEMPT_DIR_PARTS = {
    ".git",
    "node_modules",
    "__pycache__",
    # Claude rules contain code-syntax placeholders like `<name>` and
    # `<package-name>` as documentation of command syntax, not as
    # template-fill markers.
    "claude-rules",
}

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
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    in_code_block = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
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
