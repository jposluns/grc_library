#!/usr/bin/env python3
"""Fabricated alignment-citation existence - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(the PF identifier/range regexes, _check_pf, check_file) is the source of record
here in the pack, moved verbatim from the grc gate. P-1.63 part d added two optional
families: OWASP ASVS requirement/section identifiers (context-gated, see _check_asvs)
and MITRE CWE identifiers (_check_cwe); an adopter that supplies no catalogue for a
family leaves it unchecked. The framework catalogue (the
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
# Optional families (P-1.63 part d): an adopter that supplies no catalogue for a family
# leaves it unchecked, so a Privacy-Framework-only configuration behaves exactly as before.
_ASVS_REQ = frozenset()
_ASVS_SEC = frozenset()
_ASVS_NAME = ""
_ASVS_MAJOR = ""  # the held edition's major number (from asvs_edition); a token attributed to another is skipped
_CWE_ALL = frozenset()
_CWE_NAME = ""


def configure(ref) -> None:
    """Populate the framework catalogues (valid-identifier sets + framework names) from the
    adopter's registry. pf_all and pf_name are required; asvs_req, asvs_sec, asvs_name,
    asvs_edition (the held edition, e.g. "5.0.0"), cwe_all and cwe_name are optional (an absent family is not checked). _check_pf and
    check_file resolve these as module globals; call once before check_file()."""
    global _PF_ALL, _PF_NAME, _ASVS_REQ, _ASVS_SEC, _ASVS_NAME, _ASVS_MAJOR, _CWE_ALL, _CWE_NAME
    _PF_ALL = ref.pf_all
    _PF_NAME = ref.pf_name
    _ASVS_REQ = frozenset(getattr(ref, "asvs_req", ()) or ())
    _ASVS_SEC = frozenset(getattr(ref, "asvs_sec", ()) or ())
    _ASVS_NAME = getattr(ref, "asvs_name", "") or ""
    _ASVS_MAJOR = (getattr(ref, "asvs_edition", "") or "").split(".")[0]
    _CWE_ALL = frozenset(getattr(ref, "cwe_all", ()) or ())
    _CWE_NAME = getattr(ref, "cwe_name", "") or ""


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


# --- OWASP ASVS: requirement (Vn.n.n) and section (Vn.n) identifiers, CONTEXT-GATED. ---
# A bare V-token is ambiguous: most corpus V-triples are other publishers' document versions
# (ETSI "EN 304 223 V2.1.1"), several of which coincide with real ASVS ids. A token is checked
# only in ASVS context: on a line naming ASVS (the acronym as a word, so never MASVS, or the
# framework's full name), in a table cell under an ASVS-labelled header, or on a row whose first
# cell names ASVS. Bare chapters (Vn) are not checked.
# A token whose middle number is 0 (V5.0.0, V4.0.3, V2.0) is a version, never an identifier:
# ASVS numbers its sections from 1, so no section or requirement has a zero middle component.
# A token attributed to a non-held edition (the nearest preceding ASVS mention on the line, or
# its column header, names ASVS 4.x) is not checked against the held numbering, which differs.
_ASVS_WORD = re.compile(r"\bASVS\b|Application Security Verification Standard", re.IGNORECASE)
# An edition mention: the framework name, optionally "version"/"edition"/"release", then an
# edition number. A capital-V token with a non-zero middle number right after the name is an
# identifier ("ASVS V1.2.4"), never an edition; "ASVS 4.0.3", "ASVS v4", "ASVS version 4.0.3" and
# "ASVS V5.0.0" are editions.
_ASVS_MENTION = re.compile(
    r"(?:\bASVS\b|Application Security Verification Standard)"
    r"(?:\W{0,3}(?:(?:version|edition|release)\W{0,3})?(V|v)?(\d+)(?:\.(\d+))?(?:\.\d+)?\b)?",
    re.IGNORECASE)
_ASVS_TOKEN = re.compile(r"(?<![\w.])V(\d+)\.(\d+)(?:\.(\d+))?(?![\w]|\.\d)")
# A token directly after these is a version of that word's subject or of another publisher's
# document, not an ASVS identifier ("version V2.1", "EN 304 223 V2.1.1", "TOGAF V9.2").
_ASVS_NOT_ID_BEFORE = re.compile(
    r"(?:\b(?:version|edition|release|rev(?:ision)?)\s*[:(]?\s*`?"
    r"|\b(?:EN|TR|TS|ES|EG|GR|GS)\s+\d{3}\s+\d{3}(?:-\d+)*\s*`?"
    r"|\b(?:CMMI|TOGAF|ITIL|COBIT|SAMM|CSF|IEEE\s*\d+(?:\.\d+)*|ISO(?:/IEC)?\s*\d+(?:[-:]\d+)*)"
    r"\s*[:,(]?\s*`?)$",
    re.IGNORECASE,
)
# --- MITRE CWE: CWE-n anywhere, case-insensitive (the shape collides with nothing else). ---
_CWE_TOKEN = re.compile(r"(?<![\w-])CWE-(\d+)(?![\w]|-\d)", re.IGNORECASE)
_PIPE = re.compile(r"(?<!\\)\|")  # an unescaped table pipe


def _cells(line: str) -> list[str] | None:
    """Split a markdown table row on unescaped pipes into cell texts, or None when the line has
    no unescaped pipe. A leading and a trailing pipe are optional, as in GFM."""
    s = line.strip()
    if not _PIPE.search(s):
        return None
    parts = _PIPE.split(s)
    if s.startswith("|"):
        parts = parts[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        parts = parts[:-1]
    return [c.strip() for c in parts]


def _is_separator(cells: list[str] | None) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def _cell_index(line: str, pos: int) -> int:
    """0-based cell index of character `pos` in a table row, counting unescaped pipes."""
    before = len(_PIPE.findall(line[:pos]))
    return before - 1 if line.lstrip().startswith("|") else before


def _mention_edition(m: "re.Match") -> str | None:
    """The major edition an ASVS mention names, or None when it names none (or when what follows
    the name is an identifier, not an edition)."""
    vee, major, minor = m.group(1), m.group(2), m.group(3)
    if major is None:
        return None
    if vee == "V" and minor not in (None, "0"):
        return None  # "ASVS V1.2.4": a capital-V token with a non-zero middle number is an identifier
    return major


def _attributed_to_other_edition(scope: str, pos: int) -> bool:
    """True when the ASVS mention that governs the token at `pos` in `scope` names a major edition
    other than the held one: the nearest preceding mention that names an edition, else the nearest
    following one. A mention naming no edition leaves the token attributed to the held edition."""
    if not _ASVS_MAJOR:
        return False
    before = [m for m in _ASVS_MENTION.finditer(scope) if m.end() <= pos and _mention_edition(m)]
    after = [m for m in _ASVS_MENTION.finditer(scope) if m.start() >= pos and _mention_edition(m)]
    gov = before[-1] if before else (after[0] if after else None)
    return bool(gov) and _mention_edition(gov) != _ASVS_MAJOR


def _check_asvs(raw: str, lineno: int, rel: str, header: list[str] | None,
                in_table: bool, findings: list[str]) -> None:
    if not (_ASVS_REQ or _ASVS_SEC):
        return
    line_ctx = bool(_ASVS_WORD.search(raw))
    cells = _cells(raw) if in_table else None
    row_ctx = bool(cells) and bool(_ASVS_WORD.search(cells[0]))
    col_ctx = {i for i, h in enumerate(header or []) if _ASVS_WORD.search(h)}
    col_other = {i for i in col_ctx if _attributed_to_other_edition(header[i], len(header[i]))}
    for m in _ASVS_TOKEN.finditer(raw):
        col = _cell_index(raw, m.start()) if cells is not None else -1
        in_col = col in col_ctx
        if not (line_ctx or row_ctx or in_col):
            continue
        if m.group(2) == "0":  # a zero middle number is a version, never an ASVS identifier
            continue
        prefix = raw[:m.start()]
        if _ASVS_NOT_ID_BEFORE.search(prefix):
            continue
        if cells is not None and col >= 0:
            # In a table the edition is attributed within the token's own cell, then by its column
            # header; another cell on the row never governs it.
            cell_start = [x.end() for x in _PIPE.finditer(raw) if x.end() <= m.start()]
            cstart = cell_start[-1] if cell_start else 0
            nxt = _PIPE.search(raw, m.end())
            cell = raw[cstart:nxt.start() if nxt else len(raw)]
            if _attributed_to_other_edition(cell, m.start() - cstart):
                continue
            if col in col_other and not any(_mention_edition(x) for x in _ASVS_MENTION.finditer(cell)):
                continue
        elif _attributed_to_other_edition(raw, m.start()):
            continue
        tok = m.group(0)
        if m.group(3) is not None:
            if tok not in _ASVS_REQ:
                findings.append(f"{rel}:{lineno}: '{tok}' is not a valid {_ASVS_NAME} requirement "
                                f"identifier (no such requirement in the held edition)")
        elif tok not in _ASVS_SEC:
            findings.append(f"{rel}:{lineno}: '{tok}' is not a valid {_ASVS_NAME} section "
                            f"identifier (no such section in the held edition)")


def _check_cwe(raw: str, lineno: int, rel: str, findings: list[str]) -> None:
    if not _CWE_ALL:
        return
    for m in _CWE_TOKEN.finditer(raw):
        tok = "CWE-" + m.group(1)
        if tok not in _CWE_ALL:
            findings.append(f"{rel}:{lineno}: '{m.group(0)}' is not a valid {_CWE_NAME} "
                            f"identifier (no such weakness in the held edition)")


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    # Table tracking: a table's header is the row directly above its separator row, so a
    # header without a leading pipe and back-to-back tables are both read correctly; the table
    # ends at the first line with no unescaped pipe.
    header: list[str] | None = None
    prev_cells: list[str] | None = None
    for lineno, raw in iter_non_code_lines(text):
        cells = _cells(raw)
        if cells is None:
            header = None
        elif _is_separator(cells):
            header = prev_cells
        in_body = header is not None and cells is not None and not _is_separator(cells)
        _check_asvs(raw, lineno, rel, header if in_body else None, in_body, findings)
        _check_cwe(raw, lineno, rel, findings)
        prev_cells = cells
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

