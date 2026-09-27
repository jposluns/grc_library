#!/usr/bin/env python3
"""Master-matrix same-family stranded control-code scan (master compliance matrix vs per-document).

Advisory enumeration (exit 0, `audit-*` not `lint-*`) of the same-family subset of the STRANDED paired-surface
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

Input handling (3b107). The matrix is read as GFM tables, split as cmark-gfm splits them: a table is a
header line followed at once by a delimiter row with the same number of cells, it ends at a blank line or
at a line that starts another block (a heading, even one carrying pipes; a quote; a fence; a list item),
tables inside code fences are ignored, and a pipe preceded by a backslash is cell content. A referenced
document is read only when it resolves inside the repository to a regular UTF-8 file; any other row is
listed as not assessed. The run exits 2, never 0, for a matrix that is not a readable regular UTF-8 file,
that holds no master-matrix table, or none of whose rows could be checked.

The scan stays ADVISORY (never a blocking gate) until the strict-reproduce principle is
decided, since the residual candidates' disposition depends on it. A future run diffs its
output against the committed baseline to surface NEW strands.
"""
from __future__ import annotations

import argparse
import re
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aiqt_bootstrap  # noqa: E402,F401  # single shim: puts the AIQT pack tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
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
# a list item) (3b107; the round-6 cross-table reset missed a pipe-bearing heading).
_BLOCK_START_RE = re.compile(r" {0,3}(?:#{1,6}(?:[ \t]|$)|>|`{3,}|~{3,}|[-*+][ \t]|\d{1,9}[.)][ \t])")
_FENCE_RE = re.compile(r" {0,3}(`{3,}|~{3,})")
_DELIM_CELL_RE = re.compile(r":?-+:?")


def _cells(line: str) -> list[str]:
    """The cells of a table line, split as cmark-gfm splits them: a pipe preceded by a backslash is cell
    content (so ``\\|`` is too, the escape binds to the pipe) and becomes a literal pipe; one leading and one
    trailing delimiter pipe are optional. [] when the line has no delimiter pipe (it is not a table line)."""
    s = line.strip()
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
    return [c.strip() for c in parts]


def _is_delimiter_row(cells: list[str]) -> bool:
    return bool(cells) and all(_DELIM_CELL_RE.fullmatch(c) for c in cells)


def _tables(text: str):
    """Yield (header_cells, [(line_number, cells), ...]) for each GFM table outside code fences. A table is a
    header line followed at once by a delimiter row with the same number of cells; it continues until a
    blank line or a line that starts another block. A body row with fewer cells is padded and one with more is
    cut to the header's width, as GFM renders it."""
    lines = _LINE_BREAK_RE.split(text)
    fence = None
    k = 0
    while k < len(lines):
        line = lines[k]
        m = _FENCE_RE.match(line)
        if fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not line.strip()[len(m.group(1)):].strip():
                fence = None
            k += 1
            continue
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            k += 1
            continue
        header = _cells(line) if not _BLOCK_START_RE.match(line) else []
        if header and k + 1 < len(lines):
            delim = _cells(lines[k + 1])
            if len(delim) == len(header) and _is_delimiter_row(delim):
                rows = []
                k += 2
                while k < len(lines) and lines[k].strip() and not _BLOCK_START_RE.match(lines[k]):
                    cells = _cells(lines[k]) or [lines[k].strip()]
                    cells = (cells + [""] * len(header))[:len(header)]
                    rows.append((k + 1, cells))
                    k += 1
                yield header, rows
                continue
        k += 1


def _doc_path(path_cell: str) -> str | None:
    # Prefer the backtick code text; fall back to the link target.
    m = re.search(r"`([^`]+\.md)`", path_cell)
    if m:
        return m.group(1)
    m = re.search(r"\]\((?:\.\./)?([^)]+\.md)\)", path_cell)
    if m:
        return m.group(1)
    return None


def _default_doc_reader(docrel: str) -> str | None:
    """The referenced document's text, or None. Tries repo-relative, then compliance/-relative; a candidate
    counts only when it resolves inside the repository and is a regular file. Any filesystem or decoding
    error makes the row unassessed rather than crashing the run (3b107)."""
    root = REPO_ROOT.resolve()
    for cand in (REPO_ROOT / docrel, REPO_ROOT / "compliance" / docrel):
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
    ``rows`` (rows whose document was read and whose codes were compared) and ``skipped`` (one
    ``line N: reason`` per row that was not assessed)."""
    findings: list[str] = []
    doc_cache: dict[str, set[str] | None] = {}
    n_tables = n_rows = 0
    skipped: list[str] = []
    for header, rows in _tables(matrix_text):
        if header[:3] != list(_HEADER_CELLS[:3]) or "CSA CCM v4.1" not in header or "CSA AICM v1.1" not in header:
            continue
        n_tables += 1
        path_idx = header.index("Path")
        ccm_idx = header.index("CSA CCM v4.1")
        aicm_idx = header.index("CSA AICM v1.1")
        for lineno, cells in rows:
            docrel = _doc_path(cells[path_idx])
            if not docrel:
                skipped.append(f"line {lineno}: no document path in the Path cell")
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
        stats.update(tables=n_tables, rows=n_rows, skipped=skipped)
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
    """Exercise the strand signature against constructed fixtures (no corpus reads),
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
    try:
        matrix_rel = str(mp.resolve().relative_to(REPO_ROOT))
    except (ValueError, OSError, RuntimeError):
        matrix_rel = args.matrix
    stats: dict = {}
    findings = scan(text, matrix_rel=matrix_rel, stats=stats)
    skipped = stats["skipped"]
    if not stats["tables"]:
        print(f"ERROR: {args.matrix} holds no master-matrix table (a header starting Domain | Document Title | "
              "Path with the CSA CCM v4.1 and CSA AICM v1.1 columns, followed at once by its delimiter row)",
              file=sys.stderr)
        return 2
    if not stats["rows"]:
        print(f"ERROR: no matrix row in {args.matrix} could be checked; nothing is established:", file=sys.stderr)
        for s in skipped[:20]:
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
              "and rows without a readable document inside the repository are not assessed (listed below).")
    for s in skipped:
        print(f"  not assessed: {s}")
    return 0  # advisory: never blocks


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
