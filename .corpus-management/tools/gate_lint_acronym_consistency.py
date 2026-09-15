#!/usr/bin/env python3
"""Acronym-consistency audit (grc gate): pack-owned engine (source of record).

Verify that an inline acronym definition ("Some Title-Case Phrase (ACRONYM)")
whose acronym is in the glossary shares at least one significant word with the
glossary's expansion (stopwords and one-character tokens ignored). A mismatch is a
finding; an acronym not in the glossary, or an overlap, is accepted. The glossary
is parsed from a caller-supplied register file (``parse_glossary``) into an
acronym-to-significant-words map.

Engine/wrapper split (SHARED/SAFETY lane PR-41, Pattern A + 2nd seam): this engine
carries the vocab (``GLOSSARY_ROW_RE``, ``INLINE_DEF_RE``, ``STOPWORDS``) and both
pure functions (``parse_glossary`` taking the glossary path as a parameter, and
``scan`` taking the parsed glossary map). The project wrapper
(``tools/lint-acronym-consistency.py``) supplies the grc glossary-register PATH and
the grc scan scope, and keeps TWO thin module-global shims, ``parse_glossary`` and
``scan``, delegating here, because the scan-scope regression test patches BOTH of
those wrapper globals; keeping both as wrapper shims preserves that interception.
The engine functions are scope-free and repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_acronym_consistency: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


# Glossary entry: | **ACRONYM** | Expansion. ... |
# The acronym-capture group is digit-initial-tolerant ([A-Z0-9] first
# char) so numeronym rows such as **3PL** / **2FA** are parsed rather
# than silently skipped.
GLOSSARY_ROW_RE = re.compile(r"^\|\s*\*\*([A-Z0-9][A-Z0-9\-./]{1,8})\*\*\s*\|\s*(.+?)\s*\|", re.MULTILINE)

# Inline acronym definition: "Some Words Or Phrase (ACRONYM)"
# The acronym is 2-6 letters / digits / hyphens and may start with a
# digit ([A-Z0-9] first char) so numeronyms such as ``3PL`` / ``2FA``
# are recognized. The expansion phrase must be Title-Case (each word
# capitalized): that requirement is the false-positive control
# documented in the module docstring, not an oversight.
INLINE_DEF_RE = re.compile(
    r"\b((?:[A-Z][A-Za-z0-9'\-]+\s+){1,8}[A-Z][A-Za-z0-9'\-]+)\s+\(([A-Z0-9][A-Z0-9\-]{1,5})\)"
)

# Stopwords to ignore when comparing expansions
STOPWORDS = {
    "a", "an", "and", "or", "of", "for", "the", "in", "on", "to",
    "by", "with", "at", "from", "into", "via", "per", "as",
}


def parse_glossary(glossary_path: Path) -> dict[str, set[str]]:
    """Return acronym -> set of significant words in its glossary expansion."""
    out: dict[str, set[str]] = {}
    if not glossary_path.exists():
        return out
    text = glossary_path.read_text(encoding="utf-8")
    for m in GLOSSARY_ROW_RE.finditer(text):
        acr = m.group(1)
        # Use the whole expansion cell (including parenthetical alternate
        # expansions) so the linter accepts overloaded acronyms.
        expansion = m.group(2)
        # Strip markdown formatting
        expansion = re.sub(r"\*+", "", expansion)
        tokens = re.findall(r"[A-Za-z][A-Za-z0-9'\-]*", expansion.lower())
        sig = {t for t in tokens if t not in STOPWORDS and len(t) > 1}
        if acr in out:
            out[acr] |= sig
        else:
            out[acr] = sig
    return out


def scan(path: Path, glossary: dict[str, set[str]]) -> list[tuple[int, str, str, str]]:
    findings: list[tuple[int, str, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for m in INLINE_DEF_RE.finditer(line):
            expansion_phrase = m.group(1)
            acr = m.group(2)
            if acr not in glossary:
                continue
            inline_sig = {
                t for t in re.findall(r"[A-Za-z][A-Za-z0-9'\-]*", expansion_phrase.lower())
                if t not in STOPWORDS and len(t) > 1
            }
            glossary_sig = glossary[acr]
            if not inline_sig or not glossary_sig:
                continue
            # If at least one significant word overlaps, accept.
            if inline_sig & glossary_sig:
                continue
            findings.append(
                (
                    lineno,
                    acr,
                    expansion_phrase,
                    f"inline expansion words {sorted(inline_sig)} do not overlap glossary words {sorted(glossary_sig)}",
                )
            )
    return findings
