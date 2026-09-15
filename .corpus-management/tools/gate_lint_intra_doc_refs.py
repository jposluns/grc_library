#!/usr/bin/env python3
"""Intra-document section-reference audit (grc gate): pack-owned engine (source of record).

Validate that an in-document section reference (``§N``, ``§N.N``, ``Section N``,
``Section N.N`` ...) matches a numbered heading in the SAME document. Numbered
headings (``## N. Title``, ``### N.N Title``, ``## Section N: Title`` ...) are
extracted outside fenced code blocks; a reference whose numeric identifier is not
among them is a finding, UNLESS the ``is_cross_doc_context`` heuristic claims the
reference for another document (a nearby markdown link or ``.md`` filename within a
60-char window either side, a doctype word, or an external-framework name anywhere on
the line). The cross-doc heuristic vocabulary is fixed in the check implementation.

Engine/wrapper split (SHARED/SAFETY lane PR-36, Pattern A): this engine carries the
pure check (``HEADING_RE``, ``REF_PATTERNS``, ``extract_sections``,
``is_cross_doc_context``, ``scan``); the project wrapper
(``tools/lint-intra-doc-refs.py``) supplies the grc scan scope (``iter_markdown_targets``)
and the grc-specific exempt-file set (meta-documents that legitimately discuss section
references), the grouped reporting in ``main``, and keeps a thin module-global ``scan``
shim delegating here so the scan-scope regression test (which patches ``mod.scan`` and
runs ``main``) observes the original signature and behaviour. ``scan`` is scope-free and
repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_intra_doc_refs: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


# Headings of form "## 5. Title", "### 5.1 Title", "#### 5.1.2 Title",
# or "## Section 5: title", "## Section 5.1 title".
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]")

# In-document section reference patterns: §N, §N.N, §N.N.N, Section N(.N)*
REF_PATTERNS = [
    re.compile(r"§(\d+(?:\.\d+){0,3})"),
    re.compile(r"\bSection\s+(\d+(?:\.\d+){0,3})\b"),
]


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
