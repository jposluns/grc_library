#!/usr/bin/env python3
"""Per-document framework control-code validity check (grc gate): pack-owned engine.

Validate the NIST CSF 2.0 control codes that appear in a document's NIST-labelled
framework tables: every ``FUNCTION.CATEGORY`` code cited in a NIST-CSF table cell
must be a real CSF 2.0 Category; a CSF-1.1-era code is flagged with a relocation
note. When the caller also supplies the Subcategory predicates, a cited
``FUNCTION.CATEGORY-NN`` Subcategory under a valid Category must be live in CSF
2.0: a withdrawn one is flagged with a withdrawal note, and any other is flagged
as unknown. The engine handles both table orientations: framework-as-column (a
table whose header names a NIST CSF column) and framework-as-row (a row whose
first cell names NIST CSF, with the codes in the second cell).

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE scan (``check_code``, ``codes_in``, ``scan_file``) plus the NIST-CSF
parsing patterns (the label regex and the FUNCTION.CATEGORY token regex). The
framework CATALOGUE is supplied by the caller as two required predicates
(``is_valid_category`` and ``relocation_note``) and two optional keyword predicates
(``is_valid_subcategory`` and ``withdrawal_note``; when omitted, the check stays at
the Category level), and ``repo_root`` is passed in, so the engine is
repository-root-free and holds no catalogue of its own; the project wrapper
(``tools/lint-document-control-codes.py``) imports the shared NIST CSF reference,
supplies those predicates, and keeps the scan scope (``collect_targets``) and
reporting.

Exit codes (the wrapper returns these): 0 clean; 1 findings; 2 explicit target not found.
"""

from __future__ import annotations

import re
from collections import namedtuple
from pathlib import Path

try:
    from aiqt_corpus import is_fence_line, is_separator_row, read_text_safe, split_row
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_document_control_codes: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# NIST CSF label: matches "NIST CSF" / "NIST Cybersecurity Framework"
# (optionally "2.0"), but NOT "NIST SP 800-...".
NIST_CSF_LABEL_RE = re.compile(r"\bNIST\s+(?:CSF|Cybersecurity\s+Framework)\b", re.IGNORECASE)

# A NIST CSF code token: FUNCTION.CATEGORY with FUNCTION one of the six CSF
# Functions, optionally a subcategory suffix. The function set is embedded in
# the alternation so the regex never matches an ISO "A.5.19" or a NIST SP "SA-9".
# The suffix is one or more hyphens (ASCII or one of _HYPHEN_CHARS) plus a digit
# and the whole word-character run after it, so "DE.CM-07a", "DE.CM--07", or
# "DE.CM-07" written with U+2011, is one token, never cut back to the bare
# Category. A hyphen not followed by a digit ends the token, so a following
# Category ("GV.OC-PR.IP") or word ("GV.OC-aligned") is never consumed.
# _HYPHEN_CHARS: U+2010..U+2015, U+2212 minus sign, U+FE63 small hyphen-minus,
# U+FF0D fullwidth hyphen-minus and U+00AD soft hyphen.
_HYPHEN_CHARS = "".join(map(chr, (*range(0x2010, 0x2016), 0x2212, 0xFE63, 0xFF0D, 0x00AD)))
NIST_CODE_RE = re.compile(
    r"\b((?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2})(?:[-" + _HYPHEN_CHARS + r"]+\d\w*)?\b"
)

# The non-ASCII hyphens NIST_CODE_RE accepts, mapped to "-" before the check.
_HYPHENS = str.maketrans(dict.fromkeys(_HYPHEN_CHARS, "-"))

# An exact CSF 2.0 Subcategory ID: FUNCTION.CATEGORY plus two ASCII digits.
NIST_SUBCATEGORY_RE = re.compile(r"(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}-[0-9]{2}")

Finding = namedtuple("Finding", "path line rule message")


def _require_subcategory_predicate(is_valid_subcategory, withdrawal_note) -> None:
    """Raise TypeError if ``withdrawal_note`` is given without ``is_valid_subcategory``."""
    if withdrawal_note is not None and is_valid_subcategory is None:
        raise TypeError("withdrawal_note requires is_valid_subcategory")


def check_code(
    tok: str,
    is_valid_category,
    relocation_note,
    *,
    is_valid_subcategory=None,
    withdrawal_note=None,
) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a valid CSF 2.0 code, else None.

    A non-ASCII hyphen (``_HYPHEN_CHARS``) in ``tok`` is first normalised to "-".
    The Category part is checked first, exactly as before. Only when it is a valid
    Category, ``tok`` carries a suffix and ``is_valid_subcategory`` is supplied is
    the exact ``FUNCTION.CATEGORY-NN`` ID checked: withdrawn (``withdrawal_note``
    returns a note) is a finding, and so is a suffix that is not exactly one
    hyphen plus two ASCII digits or an ID that is otherwise not live. Only a
    suffix that is not two ASCII digits gets the two-digit hint, whose example is
    a live ID of the cited Category; for a one-digit suffix whose zero-padded ID
    is withdrawn, the hint gives that ID's withdrawal note instead. Raises
    TypeError when ``withdrawal_note`` is given without ``is_valid_subcategory``.
    """
    _require_subcategory_predicate(is_valid_subcategory, withdrawal_note)
    tok = tok.translate(_HYPHENS)
    category, _, suffix = tok.partition("-")
    if not is_valid_category(category):
        note = relocation_note(category)
        if note:
            return (
                "nist-csf1-carrier",
                f"'{category}' is a CSF-1.1-era code, not a CSF 2.0 Category ({note})",
            )
        return (
            "nist-unknown-category",
            f"'{category}' is not a CSF 2.0 Category (no such FUNCTION.CATEGORY in the CSF 2.0 Core)",
        )
    if not suffix or is_valid_subcategory is None:
        return None
    if NIST_SUBCATEGORY_RE.fullmatch(tok):
        note = withdrawal_note(tok) if withdrawal_note is not None else None
        if note:
            return (
                "nist-withdrawn-subcategory",
                f"'{tok}' is a withdrawn CSF Subcategory, not live in CSF 2.0 ({note})",
            )
        if is_valid_subcategory(tok):
            return None
    message = f"'{tok}' is not a CSF 2.0 Subcategory (no such ID in the CSF 2.0 Core"
    if re.fullmatch(r"[0-9]{2}", suffix):
        return ("nist-unknown-subcategory", f"{message})")
    hint = _two_digit_hint(category, suffix, is_valid_subcategory, withdrawal_note)
    return ("nist-unknown-subcategory", f"{message}; {hint})")


def _two_digit_hint(category: str, suffix: str, is_valid_subcategory, withdrawal_note) -> str:
    """Return the two-digit hint for a malformed suffix under ``category``.

    For a one-digit suffix the zero-padded ID is tried first: its withdrawal note
    when withdrawn, else it is the example when live. Otherwise the example is
    the lowest live ``category-NN`` the predicate accepts, if any."""
    lead = "CSF 2.0 IDs use two digits"
    if suffix.startswith("-"):  # a doubled hyphen, as in "DE.CM--07"
        lead = "CSF 2.0 IDs use one hyphen and two digits"
    candidates = [f"{category}-{n:02d}" for n in range(1, 100)]
    if re.fullmatch(r"[0-9]", suffix):
        padded = f"{category}-0{suffix}"
        padded_note = withdrawal_note(padded) if withdrawal_note is not None else None
        if padded_note:
            return f"{lead}, but {padded} is withdrawn too ({padded_note})"
        candidates.insert(0, padded)
    example = next((code for code in candidates if is_valid_subcategory(code)), None)
    return f"{lead}, e.g. {example}" if example else lead


def codes_in(cell: str) -> list[str]:
    """Return the distinct CSF code tokens in ``cell``, any subcategory suffix kept."""
    found: list[str] = []
    for m in NIST_CODE_RE.finditer(cell):
        code = m.group(0)
        if code not in found:
            found.append(code)
    return found


def scan_file(
    path: Path,
    repo_root: Path,
    is_valid_category,
    relocation_note,
    *,
    is_valid_subcategory=None,
    withdrawal_note=None,
) -> list[Finding]:
    """Validate NIST CSF 2.0 codes in the NIST-labelled tables of ``path``.

    Raises TypeError when ``withdrawal_note`` is given without ``is_valid_subcategory``.
    """
    _require_subcategory_predicate(is_valid_subcategory, withdrawal_note)
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    rel = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else str(path)

    def check_cell(cell: str, lineno: int) -> None:
        # One finding per distinct (rule, message) in a cell, so two suffixed codes
        # of one bad Category report it once, as the Category-level scan always did.
        seen: list[tuple[str, str]] = []
        for code in codes_in(cell):
            result = check_code(
                code, is_valid_category, relocation_note,
                is_valid_subcategory=is_valid_subcategory, withdrawal_note=withdrawal_note,
            )
            if result and result not in seen:
                seen.append(result)
                findings.append(Finding(rel, lineno, result[0], result[1]))

    lines = text.splitlines()
    in_fence = False
    prev_cells: list[str] | None = None  # the previous table row, for header lookahead
    nist_col: int | None = None  # set when the current table is framework-as-column

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if is_fence_line(line):
            in_fence = not in_fence
            prev_cells = None
            nist_col = None
            continue
        if in_fence:
            continue
        if not stripped.startswith("|"):
            prev_cells = None
            nist_col = None
            continue

        cells = split_row(line)

        if is_separator_row(cells):
            if prev_cells is not None and nist_col is None:
                for idx, c in enumerate(prev_cells):
                    if NIST_CSF_LABEL_RE.search(c):
                        nist_col = idx
                        break
            continue

        if nist_col is not None:
            if len(cells) > nist_col and not NIST_CSF_LABEL_RE.search(cells[nist_col]):
                check_cell(cells[nist_col], lineno)
        elif cells and NIST_CSF_LABEL_RE.search(cells[0]) and len(cells) > 1:
            check_cell(cells[1], lineno)

        prev_cells = cells

    return findings
