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
_ASVS_MAJORS: frozenset = frozenset()  # the held editions' major numbers; a scope naming another is skipped
_CWE_ALL = frozenset()
_CWE_NAME = ""


def configure(ref) -> None:
    """Populate the framework catalogues (valid-identifier sets + framework names) from the
    adopter's registry. pf_all and pf_name are required; asvs_req, asvs_sec, asvs_name,
    asvs_editions (the held editions, e.g. ("5.0.0", "4.0.3"); a single asvs_edition string is also
    accepted), cwe_all and cwe_name are optional (an absent family is not checked). _check_pf and
    check_file resolve these as module globals; call once before check_file()."""
    global _PF_ALL, _PF_NAME, _ASVS_REQ, _ASVS_SEC, _ASVS_NAME, _ASVS_MAJORS, _CWE_ALL, _CWE_NAME
    _PF_ALL = ref.pf_all
    _PF_NAME = ref.pf_name
    _ASVS_REQ = frozenset(getattr(ref, "asvs_req", ()) or ())
    _ASVS_SEC = frozenset(getattr(ref, "asvs_sec", ()) or ())
    _ASVS_NAME = getattr(ref, "asvs_name", "") or ""
    editions = getattr(ref, "asvs_editions", None) or (
        [ref.asvs_edition] if getattr(ref, "asvs_edition", "") else [])
    _ASVS_MAJORS = frozenset(e.split(".")[0] for e in editions)
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
# only in ASVS context: on a line naming ASVS (the acronym as a word, never MASVS or "Mobile
# ASVS", or the full name, never the mobile standard's), in a table cell under an ASVS-labelled
# header, anywhere in the body of a table with any ASVS-labelled header cell (except, unless the
# token's own cell names ASVS, a column whose header signals a version, tool or other standard), in a
# header-row cell that names ASVS, or on a row whose first cell names ASVS.
# Bare chapters (Vn) are not checked.
# A token whose middle number is 0 (V5.0.0, V4.0.3, V2.0) is a version, never an identifier:
# ASVS numbers its sections from 1, so no section or requirement has a zero middle component.
# Tokens are validated against the UNION of the held editions (a legacy identifier of a held edition
# is not a fabrication). Editions that are NOT held are handled by SCOPE: a prose line naming one,
# or a table token whose own cell, column header, or row first cell names one, is not checked.
# Stated residues: an identifier valid only in another held edition passes, and a fabricated
# identifier inside a non-held-edition scope is missed.
_ASVS_WORD = re.compile(
    r"(?<!Mobile )\bASVS\b|(?<!Mobile )(?<!Mobile OWASP )Application Security Verification Standard",
    re.IGNORECASE)
# An edition mention: the name, then an optional version/edition/release word, then an edition
# number (markdown emphasis or a link target may sit in between). After such a word any form is an
# edition ("ASVS version V4.1.1"). Otherwise the edition must be dotted or lowercase-v-prefixed
# ("ASVS 4.0.3", "ASVS v4"), or a capital-V token with a zero middle number ("ASVS V4.0.3"): a bare
# integer (a count, a footnote marker, a section sign) is never an edition, a capital V with a
# dotless or non-zero-middle number is a chapter or an identifier, and a number followed by levels
# or chapters is a count. Only a major from 1 to 9 is read, so a year never is.
_ASVS_AFTER = re.compile(
    r"(?:\]\([^)\s]*\)|[^\w\n]|_){0,8}((?:version|edition|release)(?:[^\w\n]|_){0,4})?"
    r"(V|v)?([1-9])((?:\.\d+){0,2})\b(?![*_\s]*(?:levels?|chapters?)\b)",
    re.IGNORECASE)
_ASVS_BEFORE = re.compile(
    r"(?<![\w.])[vV]?([1-9])\.0(?:\.\d+)?[\s*_]+(?:of\s+(?:the\s+)?)?(?:OWASP\s+)?$", re.IGNORECASE)
_VERSION_HEADER = re.compile(
    r"\b(?:versions?|releases?|editions?|revisions?|spec(?:ification)?s?|CWE|CAPEC|ATLAS|ATT&CK|NIST|ISO"
    r"|CIS|PCI|IEEE|ETSI|CMMI|TOGAF|ITIL|COBIT|SAMM|CSF|BSI|MASVS|tools?|products?|packages?"
    r"|components?)\b", re.IGNORECASE)
_ASVS_TOKEN = re.compile(r"(?<![\w.])V(\d+)\.(\d+)(?:\.(\d+))?(?![\w]|\.\d)")
# A token directly after these is a version of that word's subject or of another publisher's
# document, not an ASVS identifier ("version V2.1", "EN 304 223 V2.1.1", "TOGAF V9.2").
_ASVS_NOT_ID_BEFORE = re.compile(
    r"(?:\b(?:version|edition|release|rev(?:ision)?)\s*[:(]?\s*`?"
    r"|\b(?:EN|TR|TS|ES|EG|GR|GS)(?:\s+[A-Z]{2,5})?\s+\d{3}(?:\s+\d{3})?(?:-\d+)*\s*`?"
    r"|\b(?:CMMI|TOGAF|ITIL|COBIT|SAMM|CSF|NIST|PCI\s+DSS|CIS|BSI|CWE|CAPEC|ATLAS|ATT&CK|MASVS|IEEE"
    r"|ISO(?:/IEC)?)"
    # an optional short name (capitalized words, never ASVS itself, case-sensitive), a document
    # number joined by spaces or a hyphen, an amendment or corrigendum, a bracketed year, and a
    # closing parenthesis ("NIST Special Publication 800-53", "ISO-27001", "(ISO 27001)").
    r"(?-i:(?:\s+(?!ASVS\b)[A-Z][A-Za-z]{0,11}){0,3})"
    r"(?:\s+(?:standard|framework|model|profile|guide|guidance|specification|benchmark)s?)?"
    r"(?:[\s-]*[vV]?\d[\w.:/-]*)?(?:\s*(?:Cor|Amd)\s*\d[\w.:/-]*)*(?:\s*\(?\d{4}\)?)?\)?"
    r"\s*[:,(]?\s*`?)$",
    re.IGNORECASE,
)
# --- MITRE CWE: CWE-n anywhere, case-insensitive (the shape collides with nothing else). ---
_CWE_TOKEN = re.compile(r"(?<![\w-])CWE-(\d+)(?![\w]|-\d|\.\d)", re.IGNORECASE)
_BLOCK_START = re.compile(r"\s{0,3}(?:#{1,6}(?:\s|$)|>|[-*+]\s|\d{1,9}[.)]\s)")
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
    return bool(cells) and all(re.fullmatch(r":?-+:?", c) for c in cells)


def _cell_index(line: str, pos: int) -> int:
    """0-based cell index of character `pos` in a table row, counting unescaped pipes."""
    before = len(_PIPE.findall(line[:pos]))
    return before - 1 if line.lstrip().startswith("|") else before


def _editions(text: str) -> set[str]:
    """The ASVS edition majors `text` names (see _ASVS_AFTER)."""
    out: set[str] = set()
    for name in _ASVS_WORD.finditer(text):
        m = _ASVS_AFTER.match(text, name.end())
        if not m:
            continue
        word, vee, major, rest = m.groups()
        vee = text[m.start(2)] if vee else ""
        if not word:
            if vee == "V" and not rest.startswith(".0"):
                continue  # a chapter or an identifier, not an edition
            if not vee and not rest:
                continue  # a bare integer (a count, a footnote, a section sign) is not an edition
        out.add(major)
    # An edition written before the name ("3.0.1 ASVS", "version 3.0 of the ASVS"): every ASVS
    # edition has a zero middle number, so only that shape counts.
    for name in _ASVS_WORD.finditer(text):
        b = _ASVS_BEFORE.search(text, 0, name.start())
        if b:
            out.add(b.group(1))
    return out


def _names_other_edition(text: str) -> bool:
    return bool(_ASVS_MAJORS) and bool(_editions(text) - _ASVS_MAJORS)


def _plain(text: str) -> str:
    """`text` with markdown link syntax reduced to its label and emphasis/code marks removed, so a
    listed standard written as a link, in code or with emphasis still reads as that standard."""
    text = re.sub(r"\[([^\]]*)\](?:\([^)]*\)|\[[^\]]*\])", r"\1", text)
    return re.sub(r"[*_`]", "", text)


def _check_asvs(raw: str, lineno: int, rel: str, header: list[str] | None,
                in_table: bool, findings: list[str], header_row: bool = False) -> None:
    if not (_ASVS_REQ or _ASVS_SEC):
        return
    cells = _cells(raw) if (in_table or header_row) else None
    if in_table and cells is None:
        cells = [raw.strip()]
    if cells is None and _names_other_edition(raw):
        return  # a prose line naming a non-held edition: out of scope (stated residue)
    line_ctx = bool(_ASVS_WORD.search(raw))
    hdr = header or []
    row_ctx = bool(cells) and bool(_ASVS_WORD.search(cells[0]))
    row_other = bool(cells) and _names_other_edition(cells[0])
    whole_table = any(_ASVS_WORD.search(h) and not _names_other_edition(h) for h in hdr)
    # A header naming ASVS with a version word ("ASVS version") is a version column, not context.
    col_ctx = {i for i, h in enumerate(hdr) if _ASVS_WORD.search(h) and not _VERSION_HEADER.search(h)}
    col_other = {i for i, h in enumerate(hdr) if _names_other_edition(h)}
    col_held = {i for i, h in enumerate(hdr) if _editions(h) & _ASVS_MAJORS}
    # A column whose header signals a version or another subject ("Tool version", "CycloneDX spec",
    # "CWE", "ASVS version") is not checked unless the token's own cell names ASVS.
    col_skip = {i for i, h in enumerate(hdr) if i not in col_ctx and _VERSION_HEADER.search(h)}
    for m in _ASVS_TOKEN.finditer(raw):
        if cells is not None:
            col = _cell_index(raw, m.start()) if len(cells) > 1 else 0
            cell = cells[col] if 0 <= col < len(cells) else ""
            if col in col_other or _names_other_edition(cell):
                continue  # its column header or its own cell names a non-held edition
            if row_other and col not in col_held:
                continue  # its row is about a non-held edition, and its column does not override
            if col in col_skip and not _ASVS_WORD.search(cell):
                continue  # a version, tool or other-standard column, unless the cell itself names ASVS
            if header_row and not _ASVS_WORD.search(cell):
                continue  # a header cell is context only when it names ASVS itself
            if not (line_ctx or row_ctx or col in col_ctx or whole_table):
                continue
        elif not line_ctx:
            continue
        if m.group(2) == "0":  # a zero middle number is a version, never an ASVS identifier
            continue
        if _ASVS_NOT_ID_BEFORE.search(_plain(raw[:m.start()])):
            continue
        tok = m.group(0)
        if m.group(3) is not None:
            if tok not in _ASVS_REQ:
                findings.append(f"{rel}:{lineno}: '{tok}' is not a valid {_ASVS_NAME} requirement "
                                f"identifier (no such requirement in any held edition)")
        elif tok not in _ASVS_SEC:
            findings.append(f"{rel}:{lineno}: '{tok}' is not a valid {_ASVS_NAME} section "
                            f"identifier (no such section in any held edition)")


def _check_cwe(raw: str, lineno: int, rel: str, findings: list[str]) -> None:
    if not _CWE_ALL:
        return
    for m in _CWE_TOKEN.finditer(raw):
        tok = "CWE-" + str(int(m.group(1)))  # CWE-079 is CWE-79
        if tok not in _CWE_ALL:
            findings.append(f"{rel}:{lineno}: '{m.group(0)}' is not a valid {_CWE_NAME} "
                            f"identifier (no such weakness in the held edition)")


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    # Table tracking: a table's header is the row directly above its separator row, so a
    # header without a leading pipe is read correctly; the table ends at the first line with no
    # unescaped pipe (so a pipeless GFM body row is not read as a table row: stated residue) or
    # where a fenced block was skipped.
    header: list[str] | None = None
    prev_cells: list[str] | None = None
    prev_lineno = 0
    lines = list(iter_non_code_lines(text))
    # A header row is the row directly above a separator; it is known only by looking ahead.
    header_rows = {
        ln for (ln, r), (ln2, r2) in zip(lines, lines[1:])
        if ln2 == ln + 1 and _cells(r) is not None and not _BLOCK_START.match(r)
        and not _is_separator(_cells(r)) and _is_separator(_cells(r2))
    }
    for lineno, raw in lines:
        cells = _cells(raw)
        if cells is not None and _BLOCK_START.match(raw):
            cells = None  # a heading, blockquote or list item starts a new block, even with pipes
        if cells is None or lineno != prev_lineno + 1:
            header = None  # a table ends at a line with no unescaped pipe or at a skipped fence
        elif header is None and prev_cells is not None and _is_separator(cells):
            header = prev_cells  # a separator-shaped row inside a table body is just a row
        prev_lineno = lineno
        in_body = header is not None and cells is not None and not _is_separator(cells)
        _check_asvs(raw, lineno, rel, header if in_body else None, in_body, findings,
                    header_row=lineno in header_rows and not in_body)
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

