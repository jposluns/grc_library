#!/usr/bin/env python3
"""Intra-document section-reference audit (grc gate): pack-owned engine (source of record).

Validate that an in-document section reference (``§N``, ``§N.N``, ``Section N``,
``Section N.N`` ...) matches a numbered heading in the SAME document. Numbered
headings (``## N. Title``, ``### N.N Title``, ``## Section N: Title`` ...) are
extracted outside fenced code blocks; a reference whose numeric identifier is not
among them is a finding, UNLESS the ``is_cross_doc_context`` heuristic claims the
reference for another document (a nearby markdown link or ``.md`` filename within a
60-char window either side, a doctype word, or an external-framework name).
The link/filename window is checked first, even for a cued mark on a regime line.
For GDPR, CPPA, PIPEDA, HIPAA, PCI DSS, and SOC 2, a name anywhere on the line
claims each mark unless that mark has an explicit local cue (in any case). A cued
mark is checked against this document even if another doctype or framework is
named on the line. Externally meant cues in ``GDPR §33 in this context requires
notice`` and ``For breach notice, see §33 of the GDPR.`` are known false
positives. Regime names match case-sensitively as whole words, so ``UKGDPR``
and ``SOC 25`` do not name a regime. Lines without a regime retain the
doctype/framework behaviour, including ``See §99.99 of this standard.``
An uncued stale internal mark on a regime line (for example,
``GDPR §33 and §99.99 apply.``) is not checked. References and headings are
compared at full numeric depth.

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
# or "## Section 5: title", "## Section 5.1 title". Keep every numeric level.
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+)*)[.\s:]")

# In-document section references: §N, §N.N, §N.N.N, Section N(.N)*.
# Keep every numeric level so a five-level reference cannot match four levels.
REF_PATTERNS = [
    re.compile(r"§(\d+(?:\.\d+)*)"),
    re.compile(r"\bSection\s+(\d+(?:\.\d+)*)\b"),
]

PRIVACY_REGIME_RE = re.compile(r"\b(?:GDPR|CPPA|PIPEDA|HIPAA|PCI DSS|SOC 2)\b")


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
    - Doctype words and most external-framework names: whole-line scans (ISO,
      NIST, OWASP, CSA, MITRE, COBIT, BASC, etc).
      Framework-mapping tables typically reference external framework
      section numbers in their cells; this scan catches that pattern.
      Canadian federal instruments are marked by identifier only: ``ITSP.``,
      ``ITSAP.``, ``ITSG-``, ``SPIN 20`` and the held CCCS baseline title
      ``Baseline Cyber Security Controls``. The issuer names CCCS, TBS and
      Treasury Board are not markers, so a stale mark on a line that names
      only an issuer is still checked. Residual: a mark on a line that names
      one of these instruments is not checked, as for ISO and NIST; e.g.
      security/standard-authentication-and-password-management.md line 104
      names ITSP.30.031 (and the baseline title), so its own "Section 5"
      (which resolves today) is not checked.
    - GDPR, CPPA, PIPEDA, HIPAA, PCI DSS, and SOC 2 claim every mark on
      their line unless the mark is immediately preceded by "see" (optionally
      "see also") or immediately followed by "above", "below", "here",
      "herein", "in this" plus one word, or "of this" plus one word.
      Cues match in any case. The link/filename window takes precedence over
      this rule, and a cued mark wins over doctype/framework words on a regime
      line. This can flag an externally meant cue. Regime names match
      case-sensitively as whole words, so ``UKGDPR`` and ``SOC 25`` do not
      name a regime. The doctype/framework heuristic still claims marks
      without a regime
      (e.g. ``See §99.99 of this standard.``).
      An uncued stale internal mark on a regime line remains unchecked.
      A dotted single-letter or parenthesized suffix may precede a trailing cue;
      a separated parenthesized suffix or a comma before the cue does not qualify.
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
    mark = r"(?:§|Section\s+)\d+(?:\.\d+)*(?:\.[A-Za-z])?(?:\([A-Za-z0-9]+\))*"
    before = line[:ref_start]
    after = line[ref_start:]
    local_cue = bool(
        re.search(r"\bsee(?:\s+also)?\s+$", before, re.I)
        or re.match(rf"{mark}\s+(?:above|below|here|herein)\b", after, re.I)
        or re.match(rf"{mark}\s+(?:in|of)\s+this\s+\w+\b", after, re.I)
    )
    regime = PRIVACY_REGIME_RE.search(line)
    if regime and local_cue:
        return False
    if regime:
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
        "BASC", "CTPAT", "AEO", "WCO", "IMO", "ICAO", "NERC", "IEC 62443",
        "IEC 61511", "IEC 61508", "NFPA", "EN 54", "ASHRAE",
        "EU AI Act", "EU NIS", "EU DORA", "FedRAMP", "FIPS",
        "Clause", "Article", "DSS", "ISM-", "CCC-", "CEK-", "I&S-",
        "Rev ", "SP 800",
        # Canadian federal instrument identifiers only (CCCS ITSP./ITSAP./ITSG-
        # publication numbers, the TBS SPIN number form, and the title of the
        # held CCCS baseline, which the corpus pinpoints without a number); the
        # issuer names CCCS, TBS and Treasury Board are not markers
        "ITSP.", "ITSAP.", "ITSG-", "SPIN 20", "Baseline Cyber Security Controls",
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
