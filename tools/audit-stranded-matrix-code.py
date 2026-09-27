#!/usr/bin/env python3
"""Master-matrix same-family stranded control-code scan (master compliance matrix vs per-document).

Advisory enumeration (exit 0 once a matrix code was compared with its document, exit 2 on input it cannot check; `audit-*` not `lint-*`) of the same-family subset of the STRANDED paired-surface
class: the master matrix cites a CSA CCM / AICM control code that is absent from the
referenced document's own expanded code set, while that set contains another code of the
SAME prefix (family). This is a SIGNAL of a possible stale mapping (a per-document
control-fit fix may have re-mapped the document to a sibling while the matrix row kept the
old code); the scan establishes only the token-level absence, not catalogue membership,
revision history, or whether the mapping is actually wrong. Existence gates cannot see this
class (they check code validity, not per-document fit); each candidate is judged at source.

The per-PR D13 gate catches an intra-document table-vs-body strand within one PR's
diff. This scan is the cross-DOCUMENT, master-matrix complement: matrix-row-vs-document,
run report-only to enumerate the same-family-signature candidates before the fixes (scan-first, maintainer
decision 2026-09-02).

Advisory, because a matrix row may legitimately cite a representative control the
document expresses in prose rather than as a verbatim token; each candidate is judged
at source, not auto-fixed.

Scope of the strand SIGNATURE (deliberate, low-false-positive): a code is flagged only
when the document engages the SAME control FAMILY (carries a same-prefix sibling) but
not this code, the signature of a per-doc fix that re-mapped to a sibling while the
matrix row kept the stale code. A matrix code whose family the document does NOT engage
at all is treated as a representative mapping and is NOT flagged; whether those should
also be dropped is the master-matrix strict-reproduce-vs-representative principle routed
to the maintainer (pending-decisions 2026-09-02), and this scan does not pre-empt it.

Code shape and ranges. A standalone control token is `PREFIX-NN`, where PREFIX starts with
an uppercase ASCII letter followed by 1-4 uppercase ASCII letters or ampersands (so the
`A&A` and `I&S` families match, but ampersand-leading prefixes do not), and NN is two digits. A document (or a matrix cell) may express a
contiguous block as a RANGE (`IAM-01 to 15`, `LOG-01 through LOG-14`); the scan expands
both sides' ranges before comparing, so a code covered by a range the document carries is
not falsely reported stranded.

Input handling (3b107, rebuilt over QA rounds 1-6). The matrix is read as GFM tables, split as cmark-gfm splits them: a table is a
header line followed at once by a delimiter row with the same number of cells, it ends at a blank line or
at a line that starts another block (a heading, even one carrying pipes; a quote; a fence; a list item,
empty or not; a thematic break; an HTML line), tables inside code fences are ignored, and a pipe preceded
by a backslash is cell content. A matrix containing an HTML block, an indented line carrying a pipe or a
quoted line carrying a pipe is refused rather than modelled: the matrix must follow a closed line grammar
(matrix_refusal: blank lines, ATX headings, thematic breaks, plain prose without a pipe or block marker,
and table lines at column 0, with tables set apart from prose; each run of table lines is one table opening
with its header and delimiter rows; no escape, entity or HTML in a table line; only space and tab as
whitespace; no control or format character). A master table has exactly one CCM and one AICM column; a
CCM/AICM table that is not one is listed. A row is read only when its CCM and AICM cells are plain code
lists with real ranges (one family, ascending) and its Path cell is exactly a backticked path or exactly a
link whose backticked text is the path it points to; the referenced document is read only at that
repository-relative path, inside the repository, as a regular UTF-8 file. Every row not read is listed.
A run exits 0 only after comparing at least one CCM or AICM code with its document. The run exits 2, never 0, for a matrix that is not a readable regular UTF-8 file,
that holds no master-matrix table, or none of whose rows could be checked.

The scan stays ADVISORY (never a blocking gate) until the strict-reproduce principle is
decided, since the residual candidates' disposition depends on it. A future run diffs its
output against the committed baseline to surface NEW strands.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import stat
import unicodedata
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aiqt_bootstrap  # noqa: E402,F401  # single shim: puts the AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT  # noqa: E402  # grc-config, stays local
from matrix_code_parse import (  # shared canonical parser (P-1.62 I10)
    CSA_CODE_RE as _CSA_CODE,
    CSA_RANGE_RE as _CSA_RANGE,
    expand_codes as _expand_codes,
)

MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"
# _CSA_CODE / _CSA_RANGE / _expand_codes are the shared canonical CSA parser,
# imported (aliased to the historical private names) from tools/matrix_code_parse.py
# above (unified with audit-matrix-semantic-fit, P-1.62 I10).
# A matrix header row (locates the CCM/AICM columns).
_HEADER_CELLS = ("Domain", "Document Title", "Path", "CSA CCM v4.1", "CSA AICM v1.1")




_LINE_BREAK_RE = re.compile(r"\r\n|\r|\n")
# A line that starts another block ends a GFM table (a heading, even one carrying pipes; a quote; a fence;
# a list item, empty or not; a thematic break; an HTML line) (3b107). This parser is the second layer: the
# closed grammar in matrix_refusal already refuses most of these constructs in the CLI run.
_BLOCK_START_RE = re.compile(r" {0,3}(?:#{1,6}(?:[ \t]|$)|>|[-*+](?:[ \t]|$)|\d{1,9}[.)](?:[ \t]|$)|<"
                             r"|([-*_])(?:[ \t]*\1){2,}[ \t]*$)")
# A fence opener; a backtick fence whose info string contains a backtick is not one (CommonMark), which is
# how an inline code span at the start of a pipe-less row stays a row (3b107 QA r1).
_FENCE_RE = re.compile(r" {0,3}(`{3,}(?=[^`]*$)|~{3,})")
_DELIM_CELL_RE = re.compile(r":?-+:?")


def _block_start(line: str) -> bool:
    return bool(_BLOCK_START_RE.match(line) or _FENCE_RE.match(line))


_HEADING_LINE_RE = re.compile(r"#{1,6}(?: |$)")
_BREAK_LINE_RE = re.compile(r"([-*_])(?: *\1){2,} *")
_PROSE_LINE_RE = re.compile(r"(?![#>`~<=|\s])(?![-*+](?:[ \t]|$))(?!\d{1,9}[.)](?:[ \t]|$))[^|]*")


# A CCM or AICM cell the scan reads: N/A, a dash, empty, or a plain list of codes and ranges (3b107 QA r4).
# Inline markup (emphasis, code spans, links) can hide a displayed code or reveal a hidden one, so a cell
# that is anything else is not read and its row is listed as not assessed.
_CELL_CODE = r"[A-Z][A-Z&]{1,4}-[0-9]{2}"
_CELL_ITEM = rf"{_CELL_CODE}(?:[ \t]+(?:to|through)[ \t]+(?:{_CELL_CODE}|[0-9]{{2}}))?"
_CODE_LIST_RE = re.compile(rf"(?:N/A|-|)|{_CELL_ITEM}(?:[ \t]*[,;][ \t]*{_CELL_ITEM})*")


_PLAIN_HEADER_CELL_RE = re.compile(r"[A-Za-z0-9 ./:(),&-]*")


def _line_kind(line: str) -> "str | None":
    if line.strip(" \t") == "":
        return "blank"
    if _HEADING_LINE_RE.match(line):
        return "heading"
    if _BREAK_LINE_RE.fullmatch(line):
        return "break"
    if line.startswith("|"):
        return "table"
    if _PROSE_LINE_RE.fullmatch(line):
        return "prose"
    return None


def matrix_refusal(text: str) -> "str | None":
    """Why the matrix cannot be read reliably, or None (3b107 QA r1-r6). The grammar is CLOSED: rather than
    model every CommonMark construct that can hide a table or pull its text into something else (HTML,
    fences, indented code, quotes, lists and their lazy continuations), the matrix may hold only blank lines
    (spaces and tabs), ATX headings, thematic breaks, plain prose lines without a pipe or a block marker, and
    table lines starting with a pipe at column 0; a table must follow a blank line, a heading, a break or the
    start of the file, and be followed by one of those; each run of table lines must open with its own
    header and delimiter row; a table line may carry no escape (other than before a pipe), entity or HTML
    and must have cells; no whitespace other than space and tab, and no control or format character, may
    appear. Anything else refuses the matrix, and the reason names the line. Cell CONTENT is checked in
    scan: a CCM/AICM cell that is not a plain code list is not read, and its row is listed."""
    if "\ufeff" in text:
        return "it contains a byte-order mark"
    for ch in set(text):
        if ch not in "\t\n\r" and (unicodedata.category(ch) in ("Zs", "Zl", "Zp", "Cc", "Cf") and ch != " "):
            return f"it contains the character {ch!r}, which Markdown and this parser may read differently"
    prev = "blank"
    lines = _LINE_BREAK_RE.split(text)
    for n, line in enumerate(lines, 1):
        kind = _line_kind(line)
        if kind is None:
            return f"line {n} is not a blank line, heading, thematic break, plain prose or a table line at column 0"
        if kind == "table" and not _cells(line):
            return f"line {n} is a table line with no cells, which ends a table in cmark-gfm"
        if kind == "table" and re.search(r"<|&(?:#|[A-Za-z][A-Za-z0-9]*;)|\\(?!\|)", line):
            return (f"line {n} is a table line with an escape, an entity or HTML, which can hide or reveal a "
                    "code the scan would not see")
        if kind == "table" and prev != "table":
            head = _cells(line)
            plain = [c for c in head if not _PLAIN_HEADER_CELL_RE.fullmatch(c)]
            if plain:
                return (f"line {n} is a table header with markup or unusual characters in {plain[0]!r}; headers must be "
                        "plain text so a CCM or AICM column cannot be disguised (3b107 QA r7)")
            delim = _cells(lines[n]) if n < len(lines) else []
            if not (len(delim) == len(head) and _is_delimiter_row(delim)):
                return (f"line {n} starts a run of table lines that is not a header followed by its delimiter row "
                        "(cmark-gfm would not read a table later in the same run)")
        if kind == "table" and prev == "prose":
            return f"line {n} starts a table directly after prose, which may join the paragraph"
        if kind == "prose" and prev == "table":
            return f"line {n} is prose directly after a table, which may continue the table"
        prev = kind
    return None


def _cells(line: str) -> list[str]:
    """The cells of a table line, split as cmark-gfm splits them: a pipe preceded by a backslash is cell
    content (so ``\\|`` is too, the escape binds to the pipe) and becomes a literal pipe; one leading and one
    trailing delimiter pipe are optional. [] when the line has no delimiter pipe (it is not a table line)."""
    s = line.strip(" \t")
    parts: list[str] = []
    cur: list[str] = []
    found = False
    k = 0
    while k < len(s):
        c = s[k]
        if c == "\\" and k + 1 < len(s) and s[k + 1] == "|":
            cur.append("|")
            k += 2
            continue
        if c == "|":
            parts.append("".join(cur))
            cur = []
            found = True
        else:
            cur.append(c)
        k += 1
    parts.append("".join(cur))
    if not found:
        return []
    if s.startswith("|"):
        parts = parts[1:]
    if parts and parts[-1] == "" and s.endswith("|"):
        parts = parts[:-1]
    return [c.strip(" \t") for c in parts]


def _is_delimiter_row(cells: list[str]) -> bool:
    return bool(cells) and all(_DELIM_CELL_RE.fullmatch(c) for c in cells)


def _tables(text: str):
    """Yield (header_cells, [(line_number, cells), ...], header_line_number) for each GFM table outside code fences. A table is a
    header line followed at once by a delimiter row with the same number of cells; it continues until a
    blank line (spaces and tabs only) or a line that starts another block. A body row with fewer cells is padded and one with more is
    cut to the header's width, as GFM renders it."""
    lines = _LINE_BREAK_RE.split(text)
    fence = None
    k = 0
    while k < len(lines):
        line = lines[k]
        m = _FENCE_RE.match(line)
        if fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not line.strip(" \t")[len(m.group(1)):].strip(" \t"):
                fence = None
            k += 1
            continue
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            k += 1
            continue
        header = _cells(line) if not _block_start(line) else []
        if header and k + 1 < len(lines):
            delim = _cells(lines[k + 1])
            if len(delim) == len(header) and _is_delimiter_row(delim):
                rows = []
                k += 2
                while k < len(lines) and lines[k].strip(" \t") and not _block_start(lines[k]):
                    cells = _cells(lines[k]) or [lines[k].strip()]
                    cells = (cells + [""] * len(header))[:len(header)]
                    rows.append((k + 1, cells))
                    k += 1
                yield header, rows, k - len(rows) - 1
                continue
        k += 1


_PATH_BARE_RE = re.compile(r"`([A-Za-z0-9_.-][A-Za-z0-9_./-]*\.md)`")
_PATH_LINK_RE = re.compile(r"\[`([A-Za-z0-9_.-][A-Za-z0-9_./-]*\.md)`\]\(([A-Za-z0-9_./-]+\.md)\)")


def _doc_path(path_cell: str) -> str | None:
    """The document a Path cell names, or None (3b107 QA r5). Only two shapes are read, so that text GFM does
    not display (a link title, image alt text, struck-through text) cannot choose the document: the cell is
    exactly a backticked path, or exactly a link whose backticked text is the path its target resolves to from
    compliance/. Anything else is not read and its row is listed."""
    m = _PATH_BARE_RE.fullmatch(path_cell)
    if m:
        return m.group(1)
    m = _PATH_LINK_RE.fullmatch(path_cell)
    if m and posixpath.normpath(posixpath.join("compliance", m.group(2))) == posixpath.normpath(m.group(1)):
        return m.group(1)
    return None


def _range_problem(cell: str) -> "str | None":
    """Why a cell's range is not a real one, or None: a range must stay in one family and ascend (QA r5)."""
    for m in re.finditer(rf"({_CELL_CODE})[ \t]+(?:to|through)[ \t]+({_CELL_CODE}|[0-9]{{2}})", cell):
        start, end = m.group(1), m.group(2)
        prefix, s = start.rsplit("-", 1)
        if "-" in end:
            end_prefix, e = end.rsplit("-", 1)
            if end_prefix != prefix:
                return f"the range {m.group(0)!r} crosses families"
        else:
            e = end
        if int(e) < int(s):
            return f"the range {m.group(0)!r} runs backwards"
    return None


def _default_doc_reader(docrel: str) -> str | None:
    """The referenced document's text, or None. The path is repository-relative and is the only location
    tried, so a broken link cannot fall back to a different file (3b107 QA r6); it counts only when it
    resolves inside the repository to a regular UTF-8 file. Any filesystem or decoding error makes the row
    unassessed rather than crashing the run."""
    root = REPO_ROOT.resolve()
    for cand in (REPO_ROOT / docrel,):
        try:
            real = cand.resolve()
            if not real.is_relative_to(root):
                continue
            st = real.stat()
        except (OSError, RuntimeError, ValueError):
            continue
        if not stat.S_ISREG(st.st_mode):
            continue
        try:
            return real.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            return None
    return None


def scan(matrix_text: str, doc_reader=_default_doc_reader, matrix_rel: str = MATRIX_REL,
         stats: "dict | None" = None) -> list[str]:
    """Flag same-family strand candidates. `doc_reader(docrel) -> text|None` is the
    document-text source (injected by the self-test; the corpus reader by default).
    A None return skips the row. `stats`, when given, receives ``tables`` (master-matrix tables found),
    ``rows`` (rows whose document was read), ``codes`` (matrix codes compared with a document) and ``skipped`` (one
    ``line N: reason`` per row that was not assessed, or per CCM/AICM table that is not a master table,
    listed even when it has no rows)."""
    findings: list[str] = []
    doc_cache: dict[str, set[str] | None] = {}
    n_tables = n_rows = n_codes = 0
    skipped: list[str] = []
    for header, rows, header_line in _tables(matrix_text):
        code_cols = [h for h in header if "ccm" in h.lower() or "aicm" in h.lower()]
        if (header[:3] != list(_HEADER_CELLS[:3]) or sorted(code_cols) != ["CSA AICM v1.1", "CSA CCM v4.1"]
                or header.count("Path") != 1):
            if any(("ccm" in h.lower() or "aicm" in h.lower()) for h in header):
                skipped.append(f"line {header_line}: a table with CCM or AICM columns whose header is not the "
                               f"master header (or has more than one CCM or AICM column); its {len(rows)} row(s) "
                               "are not read")
            continue
        n_tables += 1
        path_idx = header.index("Path")
        ccm_idx = header.index("CSA CCM v4.1")
        aicm_idx = header.index("CSA AICM v1.1")
        for lineno, cells in rows:
            odd = [name for name, idx in (("CCM", ccm_idx), ("AICM", aicm_idx)) if not _CODE_LIST_RE.fullmatch(cells[idx])]
            if odd:
                skipped.append(f"line {lineno}: the {' and '.join(odd)} cell is not a plain list of codes and ranges "
                               "(inline markup could hide or reveal a code); not read")
                continue
            bad_range = next((f"{name}: {why}" for name, idx in (("CCM", ccm_idx), ("AICM", aicm_idx))
                              for why in [_range_problem(cells[idx])] if why), None)
            if bad_range:
                skipped.append(f"line {lineno}: {bad_range}; not read")
                continue
            docrel = _doc_path(cells[path_idx])
            if not docrel:
                skipped.append(f"line {lineno}: the Path cell is not a backticked path, or a link whose backticked "
                               "text is the path it points to; not read")
                continue
            if docrel not in doc_cache:
                dt = doc_reader(docrel)
                doc_cache[docrel] = _expand_codes(dt) if dt is not None else None
            doc_codes = doc_cache[docrel]
            if doc_codes is None:
                skipped.append(f"line {lineno}: `{docrel}` is not a readable document inside the repository")
                continue
            n_rows += 1
            doc_prefixes = {c.split("-")[0] for c in doc_codes}
            for col, colname in ((ccm_idx, "CCM"), (aicm_idx, "AICM")):
                cell = cells[col]
                if cell in ("", "N/A", "-"):
                    continue
                for code in sorted(_expand_codes(cell)):
                    n_codes += 1
                    if code in doc_codes:
                        continue
                    prefix = code.split("-")[0]
                    # Strand SIGNATURE: the document engages this control FAMILY (has a
                    # same-prefix code) but not THIS code -> a per-doc fix likely replaced
                    # it with a sibling while the matrix row kept the old code. A document
                    # with NO same-family code is treated as representative, not a strand.
                    if prefix in doc_prefixes:
                        siblings = sorted(c for c in doc_codes if c.split("-")[0] == prefix)
                        findings.append(
                            f"{matrix_rel}:{lineno}: matrix cites {colname} '{code}' for "
                            f"`{docrel}`, absent from the document, which instead has "
                            f"{prefix}: {', '.join(siblings)} (stranded-code candidate; verify at source)"
                        )
    if stats is not None:
        stats.update(tables=n_tables, rows=n_rows, codes=n_codes, skipped=skipped)
    return findings


def _outside_read_refused() -> bool:
    """A real .md file outside the repository is not read, by absolute path or by ../ path (3b107)."""
    import os
    import tempfile
    with tempfile.TemporaryDirectory(prefix="stranded-outside-") as d:
        f = Path(d) / "outside.md"
        f.write_text("STA-01", encoding="utf-8")
        if f.resolve().is_relative_to(REPO_ROOT.resolve()):
            return True  # the temp dir is inside the repository here; the case cannot be built
        rel = os.path.relpath(f, REPO_ROOT)
        return _default_doc_reader(str(f)) is None and _default_doc_reader(rel) is None


def _self_test() -> int:
    """Exercise the strand signature against constructed fixtures (the reader cases read two corpus paths and
    create, then remove, one temporary directory under the system temp directory),
    covering the same-family, carried, representative, missing-doc, RANGE, and
    ampersand-family (A&A/I&S) cases the production defects of 2026-09-02 exposed."""
    docs = {
        "risk/a.md": "aligns to STA-01 only",                 # STA family, carries STA-01
        "risk/b.md": "aligns to STA-01 only",                 # STA family, carries STA-01
        "ops/c.md": "engages LOG-03 for monitoring",          # LOG family only, no SEF
        "gov/r.md": "carries GRC-01 to GRC-08 as a block",    # RANGE covers GRC-06
        "gov/aa.md": "engages A&A-01, A&A-05",                # ampersand family, no A&A-02
        "gov/m.md": "carries GRC-01 only",                   # for matrix-side range expansion
    }
    matrix = (
        "| Domain | Document Title | Path | CSA CCM v4.1 | CSA AICM v1.1 | X |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| Risk | A | `risk/a.md` | STA-02 | N/A | . |\n"     # same-family strand -> FLAG
        "| Risk | B | `risk/b.md` | STA-01 | N/A | . |\n"     # carried -> no flag
        "| Ops  | C | `ops/c.md`  | SEF-01 | N/A | . |\n"     # no SEF family -> no flag
        "| Ops  | D | `ops/missing.md` | SEF-01 | N/A | . |\n"  # missing doc -> skip
        "| Gov  | R | `gov/r.md`  | GRC-06 | N/A | . |\n"     # covered by doc RANGE -> no flag
        "| Gov  | AA | `gov/aa.md`| A&A-02 | N/A | . |\n"     # ampersand same-family strand -> FLAG
        "| Gov  | M | `gov/m.md`  | GRC-01 to GRC-03 | N/A | . |\n"  # MATRIX-side range -> GRC-02/03 FLAG
    )
    cited = {c for r in scan(matrix, doc_reader=docs.get)
             for c in re.findall(r"cites \w+ '([A-Z][A-Z&]{1,4}-\d{2})'", r)}
    custom_findings = scan(matrix, doc_reader=docs.get, matrix_rel="other/x.md")
    checks = [
        (bool(custom_findings) and all(
            f.startswith("other/x.md:") and not f.startswith(f"{MATRIX_REL}:")
            for f in custom_findings
        ), "custom matrix path used in finding labels"),
        ("STA-02" in cited, "same-family strand STA-02 flagged"),
        ("A&A-02" in cited, "ampersand-family strand A&A-02 flagged"),
        ("STA-01" not in cited, "carried STA-01 not flagged"),
        ("SEF-01" not in cited, "representative/missing SEF-01 not flagged"),
        ("GRC-06" not in cited, "range-covered GRC-06 not flagged"),
        ("GRC-02" in cited, "matrix-side range GRC-02 flagged"),
    ]
    # 3.57: a header with the AICPA TSC 2017 column appended still parses, and TSC
    # tokens are never read as CSA codes.
    matrix_tsc = (
        "| Domain | Document Title | Path | CSA CCM v4.1 | CSA AICM v1.1 | X | AICPA TSC 2017 |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        "| Risk | A | `risk/a.md` | STA-02 | N/A | . | CC6.1, A1.2 |\n"
        "| Risk | B | `risk/b.md` | STA-01 | N/A | . | N/A |\n"
    )
    tsc_findings = scan(matrix_tsc, doc_reader=docs.get)
    checks += [
        (any("'STA-02'" in f for f in tsc_findings), "TSC-column header parsed; STA-02 strand flagged"),
        (not any("CC6.1" in f or "A1.2" in f for f in tsc_findings), "TSC tokens never read as CSA codes"),
    ]
    # 3b107: the structural table parser and the contained document reader.
    hdr = "| Domain | Document Title | Path | CSA CCM v4.1 | CSA AICM v1.1 |\n| --- | --- | --- | --- | --- |\n"
    row = lambda d: f"| Risk | A | `{d}` | STA-02 | N/A |\n"

    def rows_seen(text):
        st: dict = {}
        scan(text, doc_reader=docs.get, stats=st)
        return st["tables"], st["rows"], len(st["skipped"])

    checks += [
        (_cells("| a \\| b | c |") == ["a | b", "c"], "an escaped pipe is cell content"),
        (_cells("| a \\\\| b |") == ["a \\| b"], "a pipe after an escaped backslash is still escaped (cmark-gfm)"),
        (_cells("no pipes here") == [] and _cells("a | b") == ["a", "b"], "outer pipes optional; no pipe, no cells"),
        (rows_seen(hdr + row("risk/a.md") + "## Next | heading\n" + row("risk/b.md")) == (1, 1, 0),
         "a pipe-bearing heading ends the table"),
        (rows_seen(hdr + row("risk/a.md") + "\n" + row("risk/b.md")) == (1, 1, 0), "a blank line ends the table"),
        (rows_seen("````md\n```\n" + hdr + row("risk/a.md") + "```\n````\n") == (0, 0, 0),
         "a table inside a longer fence is not read"),
        (rows_seen(hdr.replace("| --- | --- | --- | --- | --- |", "| --- | --- | --- | --- |") + row("risk/a.md"))
         == (0, 0, 0), "a delimiter row with the wrong cell count is not a table"),
        (rows_seen(hdr + "pipeless line\n" + row("risk/a.md")) == (1, 1, 1),
         "a pipe-less line inside the table is a row (reported), and later rows are still read"),
        (rows_seen(hdr.replace("\n", "\r") + row("risk/a.md").replace("\n", "\r")) == (1, 1, 0),
         "CR line endings split lines"),
        (_outside_read_refused(), "the reader does not leave the repository"),
        (_default_doc_reader("compliance") is None and _default_doc_reader("governance/README.md") is not None,
         "the reader reads regular files only"),
        # QA r1: every CommonMark block start ends a table; a fake fence is a row; refusals.
        (all(rows_seen(hdr + row("risk/a.md") + sep + row("risk/b.md")) == (1, 1, 0)
             for sep in ("***\n", "---\n", "___\n", "> quote\n", "- item\n", "-\n", "1. item\n", "<div>\n")),
         "a thematic break, quote, list item or HTML line ends the table"),
        (rows_seen(hdr + row("risk/a.md") + "```bash``` | x | `risk/b.md` | STA-02 | N/A\n" + row("risk/b.md")) == (1, 3, 0),
         "a line starting with inline code is a row, not a fence"),
        (rows_seen("~~~\n```\n" + hdr + row("risk/a.md") + "~~~\n") == (0, 0, 0)
         and rows_seen("```\n~~~\n```x\n" + hdr + row("risk/a.md") + "```\n") == (0, 0, 0),
         "a fence closes only on its own character with no trailing text"),
        (rows_seen("| Domain | Document Title | Other | CSA CCM v4.1 | CSA AICM v1.1 |\n"
                   "| --- | --- | --- | --- | --- |\n" + row("risk/a.md")) == (0, 0, 1),
         "a CCM/AICM table without the master header is listed, not read, and does not crash"),
        (rows_seen("| Domain | Document Title | Path | CSA CCM v4.1 | CSA AICM v1.1 |\n"
                   "| a | b | c | d | e |\n" + row("risk/a.md")) == (0, 0, 0), "the second line must be a delimiter row"),
        (rows_seen(hdr + row("risk/a.md") + "\u00a0\n" + row("risk/b.md"))[1] == 2,
         "a line of Unicode space is not blank; the table goes on"),
        (matrix_refusal("<!--\n" + hdr + row("risk/a.md") + "-->\n") is not None
         and matrix_refusal(hdr + "    " + row("risk/a.md")) is not None
         and matrix_refusal("> " + hdr) is not None and matrix_refusal(hdr + row("risk/a.md")) is None,
         "HTML blocks, indented pipe lines and quoted pipe lines refuse the matrix"),
        # QA r2: the closed matrix grammar.
        (all(matrix_refusal(bad) is not None for bad in (
            "- item\n  ```\n\n" + hdr + row("risk/a.md"),          # a fence inside a list item
            "> quote\n" + hdr + row("risk/a.md"),                   # a lazy quote continuation
            "- item\n" + hdr + row("risk/a.md"),                    # a lazy list continuation
            "Some prose.\n" + hdr + row("risk/a.md"),              # a table joined to a paragraph
            hdr + row("risk/a.md") + "trailing prose\n",            # prose continuing the table
            hdr.replace("---", "---\u00a0") + row("risk/a.md"),     # Unicode space in a delimiter
            "```\n```\u00a0\n" + hdr + row("risk/a.md"),           # Unicode space after a fence
            "note\x0c\n\n" + hdr + row("risk/a.md"),                # a form feed
            "\ufeff" + hdr + row("risk/a.md"))),                    # a byte-order mark
         "the closed matrix grammar refuses constructs outside it"),
        (matrix_refusal("# Title\n\n**Bold:** prose\\\n\n---\n\n" + hdr + row("risk/a.md") + "\n## Next\n") is None,
         "the grammar accepts headings, emphasis-led prose, breaks and tables"),
        ("byte-order" in (matrix_refusal("\ufeffnote") or "")
         and matrix_refusal("A | B\n--- | ---\n\n" + hdr + row("risk/a.md")) is not None
         and matrix_refusal("- item\n\n" + hdr + row("risk/a.md")) is not None
         and _cells("| a\u00a0 | b |") == ["a\u00a0", "b"],
         "each refusal layer holds on its own: BOM, pipe-less table line, list item; cells strip only spaces and tabs"),
        (matrix_refusal(hdr + row("risk/a.md") + "|\n" + row("risk/b.md")) is not None, "a lone pipe line refuses the matrix"),
        # QA r4: CCM/AICM cells are a plain code list; format characters refuse; CCM-like headers are listed.
        (all(rows_seen(hdr + row("risk/a.md").replace("STA-02", bad)) == (1, 0, 1) for bad in (
            "STA-01, _STA-02_", "STA-01, __STA-02__", "STA-0*2*", "STA-01, **STA-02**", "STA-0`2`",
            "[STA-01](STA-02)", "STA-01 to _09_")),
         "a CCM cell with inline markup is not read and its row is listed"),
        (all(rows_seen(hdr + row("risk/a.md").replace("STA-02", ok))[1] == 1 for ok in (
            "STA-02", "STA-01, STA-02", "STA-01; STA-02", "STA-01 to 09", "STA-01 through STA-09", "A&A-02", "N/A", "-")),
         "plain code lists, ranges and N/A are read"),
        (matrix_refusal(hdr + row("risk/a.md").replace("STA-02", "STA\u00ad-02")) is not None
         and matrix_refusal(hdr + row("risk/a.md").replace("STA-02", "STA-\u200b02")) is not None,
         "a soft hyphen or zero-width space refuses the matrix"),
        # QA r5: the Path cell shapes, real ranges, a single CCM and AICM column.
        (all(rows_seen(hdr + f"| R | A | {cell} | STA-02 | N/A |\n") == (1, 0, 1) for cell in (
            '[doc](gov/x.md "`risk/a.md`")', "![`risk/a.md`](x.png)", "~~`risk/b.md`~~ `risk/a.md`",
            "[`risk/a.md`](../gov/other.md)", "see `risk/a.md`")),
         "a Path cell outside the two shapes is not read and its row is listed"),
        (rows_seen(hdr + "| R | A | [`risk/a.md`](../risk/a.md) | STA-02 | N/A |\n")[1] == 1,
         "a link whose text is the path it points to is read"),
        (all(rows_seen(hdr + row("risk/a.md").replace("STA-02", r)) == (1, 0, 1) for r in ("STA-05 to 02", "STA-01 to GRC-05"))
         and rows_seen(hdr + row("risk/a.md").replace("STA-02", "STA-01 to 05"))[1] == 1,
         "a backward or cross-family range is listed; an ascending one is read"),
        (all(rows_seen(hdr.replace("| CSA AICM v1.1 |", f"| CSA AICM v1.1 | {extra} |").replace("| --- |\n", "| --- | --- |\n")
                       + row("risk/a.md").replace("| N/A |", "| N/A | STA-03 |")) == (0, 0, 1)
             for extra in ("CSA CCM v4.1", "CSA CCM v4.1 (extra)")),
         "a second CCM column makes the table not the master table, and it is listed"),
        (matrix_refusal("note\u00a0here\n\n" + hdr + row("risk/a.md")) is not None, "a no-break space in prose refuses"),
        # QA r6: each prose exclusion holds on its own; a broken link does not fall back.
        (all(_line_kind(s) is None for s in ("> q", "`code` start", "~~~", "=== x", "1. item", "2) item", "- x", "+ x", "* x"))
         and all(_line_kind(s) == "prose" for s in ("**Bold:** x", "1.26.44 has no grant", "*emphasis* x")),
         "prose exclusions: quote, backtick, tilde, setext, ordered and bullet markers; emphasis and dotted ids are prose"),
        # QA r7: plain headers; one Path column; ASCII digits; no absolute Path; empty non-master tables listed.
        (matrix_refusal(hdr.replace("CSA CCM v4.1", "CSA C**C**M v4.1") + row("risk/a.md")) is not None
         and matrix_refusal(hdr.replace("Domain", "_Domain_") + row("risk/a.md")) is not None,
         "a header with markup refuses the matrix"),
        (rows_seen(hdr.replace("| CSA AICM v1.1 |", "| CSA AICM v1.1 | Path |").replace("| --- |\n", "| --- | --- |\n")
                   + row("risk/a.md").replace("| N/A |", "| N/A | `risk/b.md` |")) == (0, 0, 1),
         "a second Path column makes the table not a master table, and it is listed"),
        (all(rows_seen(hdr + row("risk/a.md").replace("STA-02", c)) == (1, 0, 1) for c in ("STA-\u0660\u0662", "STA-01 to \u0660\u0663")),
         "non-ASCII digits are not a plain code list"),
        (rows_seen(hdr + row("risk/a.md").replace("`risk/a.md`", "`/abs/risk/a.md`")) == (1, 0, 1),
         "an absolute Path is not read"),
        (_doc_path("`/abs/risk/a.md`") is None and _doc_path("`risk/a.md`") == "risk/a.md", "_doc_path refuses an absolute path"),
        (rows_seen("| Other | CSA CCM v4.1 |\n| --- | --- |\n\n" + hdr + row("risk/a.md")) == (1, 1, 1),
         "an empty non-master CCM table is listed"),
        (_default_doc_reader("matrix-grc-compliance-alignment.md") is None,
         "the reader does not fall back from the repository root to compliance/"),
        (rows_seen(hdr.replace("CSA CCM v4.1", "*CSA CCM v4.1*").replace("CSA AICM v1.1", "**CSA AICM v1.1**")
                   + row("risk/a.md")) == (0, 0, 1),
         "a table whose CCM header is emphasized is listed, not dropped"),
        # QA r3
        (all(matrix_refusal(hdr + row("risk/a.md").replace("STA-02", bad)) is not None
             for bad in ("STA\\-02", "STA&#45;02", "STA-01 <!-- STA-02 -->")),
         "an escape, entity or HTML in a table line refuses the matrix"),
        (all(matrix_refusal(hdr + row("risk/a.md").replace("STA-02", bad)) is not None for bad in ("STA&amp;02", "A&#65;A-02"))
         and matrix_refusal(hdr + row("risk/a.md").replace("STA-02", "A&A-02, I&S-01")) is None,
         "named and numeric entities refuse; the A&A and I&S families do not"),
        (matrix_refusal(hdr + row("risk/a.md").replace("STA-02", "a \\| b")) is None, "an escaped pipe is allowed"),
        (matrix_refusal("| a |\n| --- | --- |\n" + hdr + row("risk/a.md")) is not None
         and matrix_refusal("| a | b |\n| - |\n" + hdr + row("risk/a.md")) is not None,
         "a run of table lines must open with its own header and delimiter"),
        (matrix_refusal("<!--\n\n" + hdr + row("risk/a.md") + "\n-->\n") is not None
         and matrix_refusal("  <!--\n\n" + hdr + row("risk/a.md")) is not None,
         "an HTML or indented line before a set-apart table refuses"),
    ]
    ok = True
    for passed, label in checks:
        if not passed:
            print(f"SELF-TEST FAIL: expected {label}"); ok = False
    if ok:
        print("SELF-TEST OK: same-family + ampersand strands flagged; carried, "
              "representative, missing-doc, and range-covered codes not flagged.")
        return 0
    return 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Master-matrix same-family stranded control-code scan (advisory).")
    ap.add_argument("--matrix", default=str(REPO_ROOT / MATRIX_REL))
    ap.add_argument("--self-test", action="store_true", help="run the built-in fixtures and exit")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    mp = Path(args.matrix)
    # Input refusals (3b107): the matrix must be a readable regular UTF-8 file, it must hold a master-matrix
    # table, and at least one of its rows must be checked; anything less exits 2 rather than reading as clean.
    try:
        st = mp.stat()
        if not stat.S_ISREG(st.st_mode):
            print(f"ERROR: --matrix {args.matrix} is not a regular file", file=sys.stderr)
            return 2
        text = mp.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read --matrix {args.matrix}: {exc}", file=sys.stderr)
        return 2
    refusal = matrix_refusal(text)
    if refusal:
        print(f"ERROR: {args.matrix} cannot be scanned reliably: {refusal}", file=sys.stderr)
        return 2
    try:
        matrix_rel = str(mp.resolve().relative_to(REPO_ROOT))
    except (ValueError, OSError, RuntimeError):
        matrix_rel = args.matrix
    stats: dict = {}
    findings = scan(text, matrix_rel=matrix_rel, stats=stats)
    skipped = stats["skipped"]
    if not stats["tables"]:
        for s in skipped:
            print(f"  - {s}", file=sys.stderr)
        print(f"ERROR: {args.matrix} holds no master-matrix table (a header starting Domain | Document Title | "
              "Path with the CSA CCM v4.1 and CSA AICM v1.1 columns, followed at once by its delimiter row)",
              file=sys.stderr)
        return 2
    if not stats["rows"]:
        print(f"ERROR: no matrix row in {args.matrix} could be checked; nothing is established:", file=sys.stderr)
        for s in skipped:
            print(f"  - {s}", file=sys.stderr)
        return 2
    if not stats["codes"]:
        print(f"ERROR: no CCM or AICM code in {args.matrix} was compared with its document; nothing is established",
              file=sys.stderr)
        for s in skipped:
            print(f"  - {s}", file=sys.stderr)
        return 2
    if skipped:
        print(f"NOTE: {len(skipped)} matrix row(s) not assessed (listed at the end); {stats['rows']} row(s) checked.")
    if findings:
        uniq = sorted(set(findings))
        print(f"REPORT: {len(uniq)} stranded-code candidate(s) (matrix cites a code absent "
              f"from a referenced document that engages the SAME control family):")
        for f in uniq:
            print(f"  - {f}")
        print("\nAdvisory: each is a candidate, not a confirmed defect. Verify against the held "
              "control title and the document's own alignment table, then fix or dismiss.")
    else:
        print("OK: no stranded-code candidates under the flagging signature (a CCM/AICM code in the "
              "scanned matrix's CCM/AICM columns absent from its referenced document, which engages the "
              "SAME control family via a same-prefix sibling). This does NOT establish universal presence: "
              "a code whose family the document does not engage is TREATED AS a representative mapping and "
              "is deliberately not flagged (module docstring; strict-reproduce-vs-representative decision), "
              "and rows that could not be read (their reason is listed below) are not assessed.")
    for s in skipped:
        print(f"  not assessed: {s}")
    return 0  # advisory: never blocks


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
