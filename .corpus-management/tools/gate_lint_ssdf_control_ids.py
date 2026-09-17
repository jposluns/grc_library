#!/usr/bin/env python3
"""NIST SSDF control-identifier validity - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(the SSDF id/code-shape/header regexes, _split_cells, _is_sep, _validate_ssdf_id,
check_file) is the source of record here in the pack, moved verbatim from the grc
gate. The SSDF valid-practice and valid-task catalogue
is supplied by the adopter via configure(ref) (the SSDF family tuple is engine-fixed), so the engine carries no project
catalogue; the grc wrapper (tools/lint-ssdf-control-ids.py) supplies the catalogue,
configures the engine, and keeps EXEMPT_SUFFIXES, a module-global check_file shim,
main, and the exit codes.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  # used in check_file's annotation (get_type_hints fidelity)

try:
    from aiqt_corpus import read_text_safe, iter_non_code_lines
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_ssdf_control_ids: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- SSDF catalogue: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
VALID_PRACTICES: set = set()
VALID_TASKS: set = set()

# The SSDF family prefixes are intrinsic to the standard (also hardcoded in _SSDF_ID);
# engine-fixed, not adopter-varying catalogue data.
SSDF_FAMILIES = ("PO", "PS", "PW", "RV")


def configure(ref) -> None:
    """Populate the SSDF catalogue (valid practices, valid tasks) from
    the adopter's reference (the family tuple is engine-fixed, above). _validate_ssdf_id and check_file resolve these as module
    globals; call once before check_file()."""
    global VALID_PRACTICES, VALID_TASKS
    VALID_PRACTICES = ref.valid_practices
    VALID_TASKS = ref.valid_tasks


# Mode A: any PO/PS/PW/RV.<n> token (SSDF-unique families).
_SSDF_ID = re.compile(r"\b(PO|PS|PW|RV)\.(\d+)(?:\.(\d+))?(?:\.(\d+))?\b")
# Mode B: any XX.<n> code-shaped token (to spot a non-SSDF family in the SSDF column).
_CODE_SHAPE = re.compile(r"\b([A-Z]{2})\.(\d+(?:\.\d+){0,2})\b")
# A header cell that names the NIST SSDF column.
_SSDF_HEADER = re.compile(r"\bNIST SSDF\b|\bSSDF\b|\bSP\s*800-218\b", re.IGNORECASE)


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

