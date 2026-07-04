#!/usr/bin/env python3
"""Validate intra-document section references.

Library documents frequently reference their own sections by number,
e.g. "see §5.4" or "per Section 11.3". If the document is renumbered or
restructured, such references can silently become broken; a control
referencing "per §5.1.2" is unenforceable if §5.1.2 was removed.

This linter:

- Extracts the numeric section identifiers from headings in each
  document (headings of the form ``## N. Title``, ``### N.N Title``,
  ``#### N.N.N Title``).
- Finds intra-document references of the form ``§N``, ``§N.N``,
  ``§N.N.N``, ``Section N``, ``Section N.N``, ``Section N.N.N`` in the
  document body.
- Fails if any reference's numeric identifier does not match a heading.

Cross-document references are filtered out before the resolution check
via the ``is_cross_doc_context`` heuristic, which detects context
phrases such as "the X Standard §5.4", "the [linked doc] §5.4",
"specification ... §5.4", external framework names (ISO, NIST, OWASP,
etc.), and other markers that the reference is to a different document.

EXEMPT_FILES carries a small set of meta-documents (templates,
worklists) whose section references are by convention not to their own
headings.

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

from lint_common import REPO_ROOT, iter_markdown_targets, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

# Headings of form "## 5. Title", "### 5.1 Title", "#### 5.1.2 Title",
# or "## Section 5: title", "## Section 5.1 title".
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]")

# In-document section reference patterns: §N, §N.N, §N.N.N, Section N(.N)*
REF_PATTERNS = [
    re.compile(r"§(\d+(?:\.\d+){0,3})"),
    re.compile(r"\bSection\s+(\d+(?:\.\d+){0,3})\b"),
]

# Files exempt because they legitimately discuss intra-document
# section references (the patterns this linter checks).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "specification-citation-verification.md",
}
# Phase 23.62 removed `lint-intra-doc-refs.py` from this set: the
# linter scans `.md` only, so the .py entry was unreachable.


def extract_sections(text: str) -> set[str]:
    sections: set[str] = set()
    for _lineno, line in iter_non_code_lines(text):
        m = HEADING_RE.match(line)
        if m:
            sections.add(m.group(2))
    return sections


def is_cross_doc_context(line: str, ref_start: int) -> bool:
    """Heuristic: is the reference in a cross-doc context?

    Detection strategy:
    - Preceding-60-char window: closing bracket/paren (markdown link) or
      a `.md` filename, plus a TRAILING-60-char window for the same two
      signals (mirroring gate 62's bidirectional adjacency, so a
      "see section 5.4 in [foo](foo.md)" line, link AFTER the reference,
      is claimed by the cross-doc side here as gate 62 claims it (the
      r3 O-F1 seam). The mirror is approximate, not exact: gate 62's
      adjacency window is 40 chars and pipe-bounded while this filter
      accepts a bare ".md" or "](" within 60 chars of the reference
      start, so a link 41-60 chars after a reference is disclaimed
      here yet unclaimed by gates 62 and 65 (an accepted heuristic band, the
      same shape as the pre-existing preceding-side window).
    - Doctype words and external-framework names: whole-line scans (ISO,
      NIST, OWASP, CSA, MITRE, COBIT, GDPR, CPPA, BASC, etc).
      Framework-mapping tables typically reference external framework
      section numbers in their cells; this scan catches that pattern.
    """
    window = line[max(0, ref_start - 60):ref_start]
    if ".md" in window:
        return True
    if "](" in window:
        return True
    trailing = line[ref_start:ref_start + 60]
    if ".md" in trailing:
        return True
    if "](" in trailing:
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
    text = read_text_safe(path)
    if text is None:
        return findings
    sections = extract_sections(text)
    if not sections:
        # Documents without numbered headings have no intra-doc section refs to check.
        return findings
    for lineno, line in iter_non_code_lines(text):
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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate intra-document section references."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_markdown_targets(args.paths, exempt_files=EXEMPT_FILES)
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
