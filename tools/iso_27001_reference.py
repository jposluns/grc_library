#!/usr/bin/env python3
"""Authoritative ISO/IEC 27001:2022 Annex A and clause reference data.

Shared single source of truth for the structural facts of ISO/IEC
27001:2022, used by ``lint-matrix-control-codes.py`` (gate 49, the central
matrix's ISO column) and ``lint-document-iso-annex-a.py`` (gate 58,
per-document ISO Annex A citations). Mirrors the role ``nist_csf_reference.py``
plays for the two NIST CSF gates: the reference data lives here so the two
gates that validate ISO codes cannot drift apart.

The numbers are structural facts of the 2022 edition, verified against
multiple published references:

  * **Annex A** has four themes, A.5 Organizational (37 controls), A.6
    People (8), A.7 Physical (14), A.8 Technological (34); 37+8+14+34 = 93.
  * **Management-system clauses** run from clause 4 (Context of the
    organization) through clause 10 (Improvement).

A token is validated as either an Annex A control code ``A.<theme>.<n>``
(theme 5-8, ``<n>`` within the theme's control count) or a clause
``§<n>`` / ``§<n>.<m>`` (leading clause 4-10). A token matching neither
shape is flagged. ``check_iso_token`` validates a single atomic token; the
per-document gate layers theme-only references (``A.5``) and ranges
(``A.5.19 to A.5.22``) on top of these primitives.
"""

from __future__ import annotations

import re

# ISO/IEC 27001:2022 Annex A control counts per theme (A.5 Organizational,
# A.6 People, A.7 Physical, A.8 Technological); 37+8+14+34 = 93 controls.
ISO_ANNEX_A_RANGES = {5: 37, 6: 8, 7: 14, 8: 34}
# ISO/IEC 27001:2022 management-system clauses: 4 (Context) through
# 10 (Improvement).
ISO_CLAUSE_MIN, ISO_CLAUSE_MAX = 4, 10

ISO_ANNEX_RE = re.compile(r"^A\.(\d+)\.(\d+)$")
ISO_CLAUSE_RE = re.compile(r"^§(\d+)(?:\.\d+)*$")


def check_iso_token(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a valid ISO token, else None.

    Validates a single atomic token as an Annex A control code
    (``A.<5-8>.<n>``) or a management-system clause (``§<4-10>``). Theme-only
    references (``A.5``) and ranges are NOT handled here; a caller that
    accepts those forms recognises them before calling this function.
    """
    if tok == "N/A":
        return None
    m = ISO_ANNEX_RE.match(tok)
    if m:
        theme, num = int(m.group(1)), int(m.group(2))
        if theme not in ISO_ANNEX_A_RANGES:
            return (
                "iso-annex-theme",
                f"ISO 27001:2022 Annex A theme 'A.{theme}' does not exist "
                f"(valid themes: A.5-A.8): '{tok}'",
            )
        if not 1 <= num <= ISO_ANNEX_A_RANGES[theme]:
            return (
                "iso-annex-range",
                f"ISO 27001:2022 Annex A control '{tok}' out of range "
                f"(A.{theme}.1-A.{theme}.{ISO_ANNEX_A_RANGES[theme]})",
            )
        return None
    m = ISO_CLAUSE_RE.match(tok)
    if m:
        clause = int(m.group(1))
        if not ISO_CLAUSE_MIN <= clause <= ISO_CLAUSE_MAX:
            return (
                "iso-clause-range",
                f"ISO 27001:2022 clause '{tok}' out of range "
                f"(§{ISO_CLAUSE_MIN}-§{ISO_CLAUSE_MAX})",
            )
        return None
    return (
        "iso-malformed",
        f"unrecognized ISO 27001:2022 token '{tok}' "
        f"(expected an Annex A code 'A.5-A.8.N' or a clause '§4-§10')",
    )
