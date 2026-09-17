#!/usr/bin/env python3
"""Fabricated alignment-citation existence - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(the PF identifier/range regexes, _check_pf, check_file) is the source of record
here in the pack, moved verbatim from the grc gate. The framework catalogue (the
valid-identifier set and the framework name) is supplied by the adopter via
configure(ref), so the engine carries no project catalogue; the grc wrapper
(tools/lint-alignment-citation-existence.py) imports the alignment_citation_reference
registry, configures the engine, and keeps EXEMPT_SUFFIXES, a module-global check_file
shim, main, and the exit codes.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  # used in check_file's annotation (get_type_hints fidelity)

try:
    from aiqt_corpus import read_text_safe, iter_non_code_lines
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_alignment_citation_existence: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Framework catalogue: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
_PF_ALL = frozenset()
_PF_NAME = ""


def configure(ref) -> None:
    """Populate the framework catalogue (the valid-identifier set + the framework name)
    from the adopter's registry. _check_pf and check_file resolve these as module
    globals; call once before check_file()."""
    global _PF_ALL, _PF_NAME
    _PF_ALL = ref.pf_all
    _PF_NAME = ref.pf_name


# A single PF identifier: XX.YY-P optionally with a subcategory number.
_PF_SINGLE = re.compile(r"\b([A-Z]{2}\.[A-Z]{2}-P)(\d+)?\b")
# A PF range: "CT.PO-P1 to P5" / "CT.PO-P1 to CT.PO-P5" / hyphen or en-dash separated.
_ENDASH = "\u2013"  # en-dash, kept out of the source as a literal glyph (ungated-dash gate)
_PF_RANGE = re.compile(
    r"\b([A-Z]{2}\.[A-Z]{2}-P)(\d+)\s*(?:to|through|[-" + _ENDASH + r"])\s*"
    r"([A-Z]{2}\.[A-Z]{2}-P)?P?(\d+)\b"
)


def _check_pf(code: str) -> bool:
    """True if `code` (a category `XX.YY-P` or subcategory `XX.YY-Pn`) exists in PF."""
    return code in _PF_ALL


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    for lineno, raw in iter_non_code_lines(text):
        # Ranges first (so their endpoints are not double-reported as singles).
        range_spans: list[tuple[int, int]] = []
        for m in _PF_RANGE.finditer(raw):
            base1, start = m.group(1), int(m.group(2))
            base2, end = m.group(3), int(m.group(4))
            range_spans.append(m.span())
            # Each endpoint is validated against ITS OWN category prefix: a
            # cross-category range (CT.PO-P1 to CM.AW-P5) validates CM.AW-P5, not a
            # reconstructed CT.PO-P5.
            for code in (f"{base1}{start}", f"{base2 or base1}{end}"):
                if not _check_pf(code):
                    findings.append(
                        f"{rel}:{lineno}: '{code}' (from range '{m.group(0)}') is not a valid "
                        f"{_PF_NAME} identifier"
                    )
        for m in _PF_SINGLE.finditer(raw):
            # skip tokens already covered by a range match
            if any(s <= m.start() < e for s, e in range_spans):
                continue
            base, num = m.group(1), m.group(2)
            code = f"{base}{num}" if num else base
            if not _check_pf(code):
                findings.append(
                    f"{rel}:{lineno}: '{code}' is not a valid {_PF_NAME} identifier "
                    f"(the {base} category's subcategories do not include this number)"
                )
    return findings

