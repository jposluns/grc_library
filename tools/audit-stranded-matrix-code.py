#!/usr/bin/env python3
"""Full-corpus stranded control-code scan (master compliance matrix vs per-document).

Advisory enumeration (exit 0, `audit-*` not `lint-*`) of the STRANDED paired-surface
class: the master matrix cites a CSA CCM / AICM control code for a document whose OWN
text no longer contains that code, because a per-document control-fit fix (the P-1.60
campaign) corrected the document's table but the matrix row predates the fix. No
existence gate can see this: the code exists and is in-catalogue; it is simply the
WRONG code for THAT document now.

The per-PR D13 gate catches an intra-document table-vs-body strand within one PR's
diff. This scan is the cross-DOCUMENT, whole-corpus complement: matrix-row-vs-document,
run report-only to enumerate the complete set before the fixes (scan-first, maintainer
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

Code shape and ranges. A control code is `PREFIX-NN`, where PREFIX is 2-5 characters of
uppercase letters and ampersands (so the `A&A` and `I&S` families match, not only the
letter-only families) and NN is two digits. A document (or a matrix cell) may express a
contiguous block as a RANGE (`IAM-01 to 15`, `LOG-01 through LOG-14`); the scan expands
both sides' ranges before comparing, so a code covered by a range the document carries is
not falsely reported stranded.

The scan stays ADVISORY (never a blocking gate) until the strict-reproduce principle is
decided, since the residual candidates' disposition depends on it. A future run diffs its
output against the committed baseline to surface NEW strands.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT, read_text_safe  # noqa: E402

MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"
# CSA CCM / AICM code: 2-5 char prefix of letters+ampersand (A&A, I&S, TVM, CEK, ...),
# hyphen, two digits. Leading char is always a letter.
_CSA_CODE = re.compile(r"(?<![\w&])([A-Z][A-Z&]{1,4}-\d{2})\b")
# A contiguous range: "IAM-01 to 15", "LOG-01 through LOG-14", "A&A-01 to A&A-06".
_CSA_RANGE = re.compile(
    r"(?<![\w&])([A-Z][A-Z&]{1,4})-(\d{1,2})\s*(?:to|through)\s*"
    r"(?:([A-Z][A-Z&]{1,4})-)?(\d{1,2})\b"
)
# A matrix header row (locates the CCM/AICM columns).
_HEADER_CELLS = ("Domain", "Document Title", "Path", "CSA CCM v4.1", "CSA AICM v1.1")


def _expand_codes(text: str) -> set[str]:
    """All control codes the text carries, with contiguous ranges expanded."""
    codes: set[str] = set(_CSA_CODE.findall(text))
    for prefix, start, end_prefix, end in _CSA_RANGE.findall(text):
        if end_prefix and end_prefix != prefix:  # cross-family range: not a real range
            continue
        s, e = int(start), int(end)
        if s <= e and e - s < 100:  # sane bound
            for n in range(s, e + 1):
                codes.add(f"{prefix}-{n:02d}")
    return codes


def _cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def _is_sep(cells: list[str]) -> bool:
    return bool(cells) and set("".join(cells)) <= set("-: ")


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
    """Return the document's text, or None if it does not exist. Resolves a path
    repo-relative first, then relative to the matrix's own directory (the link-fallback
    form can yield a matrix-dir-relative or bare-filename path)."""
    for cand in (REPO_ROOT / docrel, REPO_ROOT / "compliance" / docrel):
        if cand.exists():
            return read_text_safe(cand)
    return None


def scan(matrix_text: str, doc_reader=_default_doc_reader) -> list[str]:
    """Flag same-family strand candidates. `doc_reader(docrel) -> text|None` is the
    document-text source (injected by the self-test; the corpus reader by default). A
    None return means the document does not exist and the row is skipped."""
    findings: list[str] = []
    lines = matrix_text.splitlines()
    ccm_idx = aicm_idx = path_idx = None
    doc_cache: dict[str, set[str] | None] = {}
    i = 0
    n = len(lines)
    while i < n:
        cells = _cells(lines[i]) if "|" in lines[i] else []
        if cells[:3] == list(_HEADER_CELLS[:3]) and "CSA CCM v4.1" in cells:
            path_idx = cells.index("Path")
            ccm_idx = cells.index("CSA CCM v4.1")
            aicm_idx = cells.index("CSA AICM v1.1")
            i += 1
            continue
        if ccm_idx is None or not cells or _is_sep(cells) or "|" not in lines[i]:
            i += 1
            continue
        if len(cells) <= max(ccm_idx, aicm_idx, path_idx):
            i += 1
            continue
        docrel = _doc_path(cells[path_idx])
        if not docrel:
            i += 1
            continue
        if docrel not in doc_cache:
            dt = doc_reader(docrel)
            doc_cache[docrel] = _expand_codes(dt) if dt is not None else None
        doc_codes = doc_cache[docrel]
        if doc_codes is None:  # document does not exist
            i += 1
            continue
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
                # with NO same-family code is a representative mapping, not a strand.
                if prefix in doc_prefixes:
                    siblings = sorted(c for c in doc_codes if c.split("-")[0] == prefix)
                    findings.append(
                        f"{MATRIX_REL}:{i+1}: matrix cites {colname} '{code}' for "
                        f"`{docrel}`, absent from the document, which instead has "
                        f"{prefix}: {', '.join(siblings)} (stranded-code candidate; verify at source)"
                    )
        i += 1
    return findings


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
    checks = [
        ("STA-02" in cited, "same-family strand STA-02 flagged"),
        ("A&A-02" in cited, "ampersand-family strand A&A-02 flagged"),
        ("STA-01" not in cited, "carried STA-01 not flagged"),
        ("SEF-01" not in cited, "representative/missing SEF-01 not flagged"),
        ("GRC-06" not in cited, "range-covered GRC-06 not flagged"),
        ("GRC-02" in cited, "matrix-side range GRC-02 flagged"),
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
    ap = argparse.ArgumentParser(description="Full-corpus stranded control-code scan (advisory).")
    ap.add_argument("--matrix", default=str(REPO_ROOT / MATRIX_REL))
    ap.add_argument("--self-test", action="store_true", help="run the built-in fixtures and exit")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    mp = Path(args.matrix)
    if not mp.exists():
        print(f"ERROR: cannot read matrix {args.matrix}", file=sys.stderr)
        return 2
    text = read_text_safe(mp)
    if text is None:
        print(f"ERROR: cannot read matrix {args.matrix}", file=sys.stderr)
        return 2
    findings = scan(text)
    if findings:
        uniq = sorted(set(findings))
        print(f"REPORT: {len(uniq)} stranded-code candidate(s) (matrix cites a code absent "
              f"from the referenced document):")
        for f in uniq:
            print(f"  - {f}")
        print("\nAdvisory: each is a candidate, not a confirmed defect. Verify against the held "
              "control title and the document's own alignment table, then fix or dismiss.")
    else:
        print("OK: every CCM/AICM code the master matrix cites appears in its referenced document.")
    return 0  # advisory: never blocks


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
