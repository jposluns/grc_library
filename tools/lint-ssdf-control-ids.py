#!/usr/bin/env python3
"""NIST SSDF control-identifier validity audit.

Catches fabricated, mistyped, or retired NIST SSDF (SP 800-218 v1.1) control
identifiers cited in the corpus and pack. A wrong control *mapping* (whether a
document semantically belongs under a given SSDF practice) is a judgement call
and stays the author's apply-time responsibility; a wrong control *code* IS
mechanically checkable, and this gate checks it, the same philosophy as the
matrix control-code validity gate.

The gate exists because the external-audit remediation (TODO 1.27) found
fabricated SSDF families (``VE.1``, ``DS.2`` -- there is no VE or DS group)
and the dual-family verifies kept catching parallel occurrences the register
had not named. A mechanical gate closes that class.

Scope (deliberately bounded, low false-positive):

  * **Mode A (global valid-family id check).** The four SSDF practice groups
    ``PO`` / ``PS`` / ``PW`` / ``RV`` are unique to SSDF (no other framework
    the corpus cites uses a ``PO|PS|PW|RV.<n>`` code shape; ISO is ``A.x``,
    NIST CSF is ``FUNCTION.CATEGORY`` with letter categories, NIST 800-53 is
    ``XX-n``, CSA is ``XXX-n``). So any ``PO|PS|PW|RV.<n>[.<m>[.<k>]]`` token
    anywhere in a scanned file is an SSDF citation, and is validated against
    the closed set of valid practice and task ids below (the union of SP 800-218 v1.1
    and the SP 800-218A Generative AI profile, since the corpus cites both).
    This catches non-existent ids (a family or number in neither document).

  * **Mode B (SSDF-column invalid-family check).** In a markdown table that
    has a header cell naming the NIST SSDF column, every code-shaped token
    (``XX.<n>...``) in that column must have a valid SSDF family
    (``PO|PS|PW|RV``); a token with any other two-letter family (``VE``,
    ``DS``, ...) is a fabricated SSDF id and is flagged. ``N/A`` and free
    text are ignored.

The valid id sets are structural facts of SP 800-218 v1.1 and SP 800-218A,
extracted from the NIST-published OSCAL catalogue and the 800-218A publication and hard-coded here so the gate is
stdlib-only and does not depend on a reference checkout at run time (the same
approach as the ISO Annex A counts in the matrix control-code gate).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import (  # noqa: E402
    REPO_ROOT, iter_markdown_targets, read_text_safe, iter_non_code_lines,
)
import argparse

# --- Valid SSDF ids (SP 800-218 v1.1, from the NIST OSCAL catalogue) ---
VALID_PRACTICES = {
    "PO.1", "PO.2", "PO.3", "PO.4", "PO.5",
    "PS.1", "PS.2", "PS.3",
    "PW.1", "PW.2", "PW.3", "PW.4", "PW.5", "PW.6", "PW.7", "PW.8", "PW.9",  # PW.3 is 800-218A
    "RV.1", "RV.2", "RV.3",
}
VALID_TASKS = {
    # Union of SP 800-218 v1.1 (base) and SP 800-218A (Generative AI profile),
    # since the corpus cites both. 800-218A adds PW.3.x, PO.5.3, PS.1.2/1.3.
    # NB: PW.4.3 is NOT valid: a v1.0 task moved for v1.1 whose id was not reused
    # (218A gap-numbering note, lines 579-580); PW.4 has 4.1/4.2/4.4 only.
    "PO.1.1", "PO.1.2", "PO.1.3", "PO.2.1", "PO.2.2", "PO.2.3",
    "PO.3.1", "PO.3.2", "PO.3.3", "PO.4.1", "PO.4.2", "PO.5.1", "PO.5.2", "PO.5.3",
    "PS.1.1", "PS.1.2", "PS.1.3", "PS.2.1", "PS.3.1", "PS.3.2",
    "PW.1.1", "PW.1.2", "PW.1.3", "PW.2.1", "PW.3.1", "PW.3.2", "PW.3.3",
    "PW.4.1", "PW.4.2", "PW.4.4",
    "PW.5.1", "PW.6.1", "PW.6.2", "PW.7.1", "PW.7.2", "PW.8.1", "PW.8.2",
    "PW.9.1", "PW.9.2",
    "RV.1.1", "RV.1.2", "RV.1.3", "RV.2.1", "RV.2.2",
    "RV.3.1", "RV.3.2", "RV.3.3", "RV.3.4",
}
SSDF_FAMILIES = ("PO", "PS", "PW", "RV")

# Mode A: any PO/PS/PW/RV.<n> token (SSDF-unique families).
_SSDF_ID = re.compile(r"\b(PO|PS|PW|RV)\.(\d+)(?:\.(\d+))?(?:\.(\d+))?\b")
# Mode B: any XX.<n> code-shaped token (to spot a non-SSDF family in the SSDF column).
_CODE_SHAPE = re.compile(r"\b([A-Z]{2})\.(\d+(?:\.\d+){0,2})\b")
# A header cell that names the NIST SSDF column.
_SSDF_HEADER = re.compile(r"\bNIST SSDF\b|\bSSDF\b|\bSP\s*800-218\b", re.IGNORECASE)

# Files where SSDF-shaped strings are historical description, not live citations.
EXEMPT_SUFFIXES = (
    "CHANGELOG.md",
    "dev-security/claude-rules/README.md",  # pack version-history describes fixed codes
    "governance/specification-audit-programme.md",  # gate-description prose uses example codes
)


def _split_cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def _is_sep(cells: list[str]) -> bool:
    return bool(cells) and set("".join(cells)) <= set("-: ")


def _validate_ssdf_id(fam: str, rest_groups: tuple) -> str | None:
    """Return an error message if the PO/PS/PW/RV id is not valid, else None."""
    nums = [g for g in rest_groups if g is not None]
    parts = [fam] + nums
    ident = ".".join(parts)
    if len(nums) == 1:
        if ident not in VALID_PRACTICES:
            return f"'{ident}' is not a valid SSDF {fam} practice (SP 800-218 v1.1)"
    else:
        if ident not in VALID_TASKS:
            # a task whose practice is valid but the task id is retired/nonexistent
            practice = f"{fam}.{nums[0]}"
            hint = "" if practice in VALID_PRACTICES else f" (and {practice} is not a valid practice)"
            return f"'{ident}' is not a valid SSDF task id (SP 800-218 v1.1){hint}"
    return None


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    lines = text.splitlines()

    # Precompute SSDF-column index per table (Mode B).
    # Walk tables: a header row followed by a separator row.
    ssdf_col_for_line: dict[int, int] = {}
    i = 0
    n = len(lines)
    while i < n - 1:
        cells = _split_cells(lines[i]) if "|" in lines[i] else []
        nxt = _split_cells(lines[i + 1]) if "|" in lines[i + 1] else []
        if cells and nxt and _is_sep(nxt) and not _is_sep(cells):
            # header row at i; find an SSDF column
            col = next((c for c, h in enumerate(cells) if _SSDF_HEADER.search(h)), None)
            if col is not None:
                j = i + 2
                while j < n and "|" in lines[j] and not _is_sep(_split_cells(lines[j])):
                    ssdf_col_for_line[j] = col
                    j += 1
                i = j
                continue
        i += 1

    for lineno, raw in iter_non_code_lines(text):
        idx = lineno - 1
        # Mode A: validate every PO/PS/PW/RV id on the line.
        for m in _SSDF_ID.finditer(raw):
            msg = _validate_ssdf_id(m.group(1), (m.group(2), m.group(3), m.group(4)))
            if msg:
                findings.append(f"{rel}:{lineno}: {msg}")
        # Mode B: in an SSDF column, flag a code-shaped token with a non-SSDF family.
        if idx in ssdf_col_for_line:
            cells = _split_cells(raw)
            col = ssdf_col_for_line[idx]
            if col < len(cells):
                for cm in _CODE_SHAPE.finditer(cells[col]):
                    fam = cm.group(1)
                    if fam not in SSDF_FAMILIES:
                        findings.append(
                            f"{rel}:{lineno}: '{cm.group(0)}' in the NIST SSDF column is "
                            f"not a valid SSDF id ({fam} is not an SSDF practice group; "
                            f"SSDF groups are PO/PS/PW/RV)"
                        )
    return findings


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="NIST SSDF control-identifier validity audit.")
    ap.add_argument("paths", nargs="*", default=[str(REPO_ROOT)],
                    help="files or directories to scan (default: the whole repository)")
    args = ap.parse_args(argv[1:])
    findings: list[str] = []
    for path in iter_markdown_targets(args.paths or [str(REPO_ROOT)]):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.endswith(EXEMPT_SUFFIXES):
            continue
        findings.extend(check_file(path, rel))
    if findings:
        print("FAIL: invalid NIST SSDF control identifier(s) found:")
        for f in sorted(set(findings)):
            print(f"  - {f}")
        print(
            "\nSSDF (SP 800-218 v1.1) has exactly four practice groups: PO, PS, PW, RV. "
            "Correct the id to a valid practice/task, or (for a semantic remap) to the "
            "SSDF task that fits."
        )
        return 1
    print("OK: all NIST SSDF control identifiers are valid (SP 800-218 v1.1).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
