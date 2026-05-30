#!/usr/bin/env python3
"""Validate intra-document section references.

Library documents frequently reference their own sections by number, e.g.
"see §5.4" or "per Section 11.3". If the document is renumbered or
restructured, such references can silently become broken — a control
referencing "per §5.1.2" is unenforceable if §5.1.2 was removed.

This linter:
- Extracts the numeric section identifiers from headings in each document
  (headings of the form `## N. Title`, `### N.N Title`, `#### N.N.N Title`).
- Finds intra-document references of the form `§N`, `§N.N`, `§N.N.N`,
  `Section N`, `Section N.N`, `Section N.N.N` in the document body.
- Fails if any reference's numeric identifier does not match a heading.

Cross-document references (e.g., "per the OT/ICS Security Standard §5.4")
are out of scope; this linter only validates references to the document's
own sections.

Usage:
    python3 tools/lint-intra-doc-refs.py
    python3 tools/lint-intra-doc-refs.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more intra-document references that do not resolve
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

# Headings of form "## 5. Title", "### 5.1 Title", "#### 5.1.2 Title",
# or "## Section 5: title", "## Section 5.1 title".
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]")

# In-document section reference patterns: §N, §N.N, §N.N.N, Section N(.N)*
REF_PATTERNS = [
    re.compile(r"§(\d+(?:\.\d+){0,3})"),
    re.compile(r"\bSection\s+(\d+(?:\.\d+){0,3})\b"),
]

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}

# Files exempt because the linter itself or specs describe these patterns.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "lint-intra-doc-refs.py",
    "specification-citation-verification.md",
}


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    return True


def extract_sections(text: str) -> set[str]:
    sections: set[str] = set()
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if m:
            sections.add(m.group(2))
    return sections


def is_cross_doc_context(line: str, ref_start: int) -> bool:
    """Heuristic: is the reference in a cross-doc context?

    Detection strategy:
    - Preceding-60-char window: closing bracket/paren (markdown link),
      a `.md` filename, or a doctype word ("Standard", "Procedure", etc).
    - Whole-line scan for external-framework names: ISO, NIST, OWASP, CSA,
      MITRE, COBIT, GDPR, CPPA, BASC, etc. Framework-mapping tables
      typically reference external framework section numbers in their
      cells; this scan catches that pattern.
    """
    window = line[max(0, ref_start - 60):ref_start]
    if ".md" in window:
        return True
    if "](" in window:
        return True
    # Doctype words anywhere on the line: when the library writes about
    # another document's section, the document is typically named on the
    # same line (often once, then multiple section refs follow).
    cross_doc_words = (
        "Standard", "Procedure", "Policy", "Specification", "Plan",
        "Framework", "Register", "Annex", "Guide", "Guideline", "Charter",
        "Matrix", "Worklist", "Template",
        # Plain-language doc references (lowercase)
        "guideline", "standard", "specification", "procedure", "policy",
        "register", "library",
        # NIST CSF function names indicate cross-doc framework mapping
        "Detect:", "Identify:", "Protect:", "Respond:", "Recover:", "Govern:",
    )
    for w in cross_doc_words:
        if w in line:
            return True
    # Whole-line scan for external framework names. Common in
    # framework-alignment tables.
    external_frameworks = (
        "ISO/IEC", "ISO ", "NIST", "OWASP", "CSA ", "MITRE", "COBIT",
        "GDPR", "CPPA", "PIPEDA", "HIPAA", "PCI DSS", "SOC 2",
        "BASC", "CTPAT", "AEO", "WCO", "IMO", "ICAO", "NERC", "IEC 62443",
        "IEC 61511", "IEC 61508", "NFPA", "EN 54", "ASHRAE",
        "EU AI Act", "EU NIS", "EU DORA", "FedRAMP", "FIPS",
        "Clause", "Article", "DSS", "ISM-", "CCC-", "CEK-", "I&S-",
        "Rev ", "SP 800",
    )
    for w in external_frameworks:
        if w in line:
            return True
    return False


def scan(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    sections = extract_sections(text)
    if not sections:
        # Documents without numbered headings have no intra-doc section refs to check.
        return findings
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Skip table rows that show section references in coverage / index documents
        # (they describe other documents' sections, not this one's).
        for pattern in REF_PATTERNS:
            for m in pattern.finditer(line):
                ref = m.group(1)
                if ref in sections:
                    continue
                # Skip references that look cross-doc
                if is_cross_doc_context(line, m.start()):
                    continue
                findings.append((lineno, ref, line.strip()[:140]))
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
        description="Validate intra-document section references."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all intra-document section references resolve (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, ref, excerpt in findings:
            print(f"  L{lineno} [intra-doc-ref] §{ref} not a heading in this document: {excerpt}")
        total += len(findings)
    print(f"\nFAIL: {total} unresolved intra-document reference(s) across {len(grouped)} file(s).")
    print(
        "References to §N or Section N inside a document must match a heading "
        "in the same document. If the reference is to another document, include "
        "a markdown link or name the document explicitly."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
