#!/usr/bin/env python3
"""Enforce required orientation section presence by document type.

Library documents follow a canonical structure. This linter verifies
that documents of certain doctypes contain at least one *orientation*
section so a reader can quickly determine what the document is about.

Acceptable orientation headings (case-insensitive substring match,
ORIENTATION_OPTIONS): Purpose, Scope, Applicability, Purpose and Scope,
Introduction, Overview, Executive Summary, Summary.

Doctypes currently covered (REQUIRED_SECTIONS):

  Charter, Framework, Policy, Standard, Procedure, Specification, Plan,
  Annex, Register, Guide, Guideline.

The linter is deliberately conservative: it requires only the single
orientation requirement above. Framework alignment, role responsibility,
metrics, and other section conventions are NOT enforced (Phase 23.20
loosened the rule to avoid false positives where the convention exists
in practice but the canonical heading name varies).

Doctypes not in REQUIRED_SECTIONS (SOP, Roadmap, Matrix, Template,
Checklist, Worklist) are not enforced by this linter. Each has a
different shape that the orientation rule does not fit cleanly.

Usage:
    python3 tools/lint-required-sections.py
    python3 tools/lint-required-sections.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more documents missing a required orientation section
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

DOCTYPE_RE = re.compile(r"^\*\*Document Type:\*\*\s+(.+?)(?:\\)?\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")

# Directory-walk exemption: shared default set from lint_common. The
# is_target function reads each file's metadata to check for the
# Classification: Deprecated exemption, so this linter cannot use the
# shared iter_markdown_targets helper as-is.
EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS

# Per-doctype required sections. Each requirement is a list of acceptable
# heading names (case-insensitive substring match against the heading
# text, after stripping leading numbers and punctuation).
#
# Library practice: most artefacts have Purpose and Scope as separate
# sections, but some combine them, and some skip directly to numbered
# domain sections. The requirement is therefore "at least one orientation
# section" rather than "Purpose AND Scope both present."
ORIENTATION_OPTIONS = [
    "purpose",
    "scope",
    "applicability",
    "purpose and scope",
    "introduction",
    "overview",
    "executive summary",
    "summary",
]

REQUIRED_SECTIONS: dict[str, list[list[str]]] = {
    "Standard": [ORIENTATION_OPTIONS],
    "Procedure": [ORIENTATION_OPTIONS],
    "Policy": [ORIENTATION_OPTIONS],
    "Specification": [ORIENTATION_OPTIONS],
    "Plan": [ORIENTATION_OPTIONS],
    "Framework": [ORIENTATION_OPTIONS],
    "Charter": [ORIENTATION_OPTIONS],
    "Annex": [ORIENTATION_OPTIONS],
    "Register": [ORIENTATION_OPTIONS],
    "Guide": [ORIENTATION_OPTIONS],
    "Guideline": [ORIENTATION_OPTIONS],
}

EXEMPT_FILES: set[str] = {
    # README files use a simpler shape than canonical artefacts.
    # Phase 23.73b removed `CITATION.cff` and `LICENSE`: this linter scans
    # `.md` files only (see `is_target`), so non-`.md` entries were
    # unreachable defensive listings.
    "README.md",
    "NOTICE.md",
    "AUTHORS.md",
    "CHANGELOG.md",
    "TODO.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    # Worklists and templates use their own shapes.
}


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    if path.name.startswith("template-"):
        return False
    if path.name.startswith("worklist-"):
        return False
    # Documents marked Classification: Deprecated are short redirect notices.
    try:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\*\*Classification:\*\*\s+Deprecated", text, re.MULTILINE):
            return False
    except (OSError, UnicodeDecodeError):
        pass
    return True


def extract_doctype(text: str) -> str | None:
    m = DOCTYPE_RE.search(text)
    if not m:
        return None
    return m.group(1).strip().rstrip("\\").strip()


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for _lineno, line in iter_non_code_lines(text):
        m = HEADING_RE.match(line)
        if m:
            heading = m.group(2)
            # Strip leading numbering and punctuation
            cleaned = re.sub(r"^\d+(\.\d+)*[.\s:]*", "", heading)
            cleaned = re.sub(r"^Section\s+\d+(\.\d+)*[.\s:]*", "", cleaned)
            headings.append(cleaned.strip().lower())
    return headings


def scan(path: Path) -> list[str]:
    findings: list[str] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    doctype = extract_doctype(text)
    if doctype is None:
        return findings
    required = REQUIRED_SECTIONS.get(doctype)
    if not required:
        return findings
    headings = extract_headings(text)
    for requirement in required:
        # Each requirement is a list of acceptable heading names; at least
        # one must appear in the document's headings.
        matched = False
        for option in requirement:
            for h in headings:
                if option in h:
                    matched = True
                    break
            if matched:
                break
        if not matched:
            findings.append(f"missing required section (any of: {requirement})")
    return findings


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce required section presence by document type."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
    grouped: dict[Path, list[str]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all documents have required sections by doctype (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for msg in findings:
            print(f"  [required-section] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} required-section finding(s) across {len(grouped)} file(s).")
    print(
        "Documents missing canonically-expected sections by doctype. Either "
        "add the section under one of the acceptable heading names, or change "
        "the Document Type field to one that does not require this section."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
