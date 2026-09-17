#!/usr/bin/env python3
"""Cross-document retention-consistency check (grc gate): pack-owned engine (source of record).

Verify that each procedure document's evidence-retention period matches the
canonical period for the same category in a central retention-schedule register.
Each check names a register row (matched on its first table cell) and the
procedure document that must cite the same period; the procedure value is the
period stated after a configured anchor phrase, so an unrelated period elsewhere
in the document is not mistaken for the retention figure.

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE check (``normalise``, ``register_value``, ``procedure_value``,
``collect_findings``) plus the GENERIC period-parsing config (the number+unit regex
and the unit-to-days table). The project wrapper
(``tools/lint-retention-consistency.py``) supplies the corpus config: the register
path, the register-category-to-procedure check list, the procedure anchor phrase,
and the ``--root`` handling and reporting.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_retention_consistency: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

UNIT_TO_DAYS = {"year": 365, "month": 30, "day": 1}

# Captures a "<number> <unit>" period; tolerates a hyphen ("7-year") and the
# markdown bold markers around the value ("**7 years**").
PERIOD_RE = re.compile(r"(\d+)[\s-]*(year|month|day)s?", re.IGNORECASE)


def normalise(value: int, unit: str, unit_to_days: dict[str, int] = UNIT_TO_DAYS) -> int:
    """Return the period in days."""
    return value * unit_to_days.get(unit.lower().rstrip("s"), 0)


def register_value(
    text: str, category: str, period_re: re.Pattern = PERIOD_RE, unit_to_days: dict[str, int] = UNIT_TO_DAYS
) -> tuple[int, str] | None:
    """Return (days, raw) for the register row whose first cell is ``category``."""
    cat_lower = category.lower()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if cells[0].lower() == cat_lower:
            row_rest = " | ".join(cells[1:])
            m = period_re.search(row_rest)
            if m:
                return normalise(int(m.group(1)), m.group(2), unit_to_days), f"{m.group(1)} {m.group(2)}"
    return None


def procedure_value(
    text: str, procedure_anchor_re: re.Pattern, unit_to_days: dict[str, int] = UNIT_TO_DAYS
) -> tuple[int, str] | None:
    """Return (days, raw) for the procedure's anchored retention figure."""
    m = procedure_anchor_re.search(text)
    if m:
        return normalise(int(m.group(1)), m.group(2), unit_to_days), f"{m.group(1)} {m.group(2)}"
    return None


def collect_findings(
    register_text: str,
    root: Path,
    checks: list[dict[str, str]],
    procedure_anchor_re: re.Pattern,
    register_rel: str,
    period_re: re.Pattern = PERIOD_RE,
    unit_to_days: dict[str, int] = UNIT_TO_DAYS,
) -> list[str]:
    """Return retention-consistency finding strings for the configured check pairs."""
    findings: list[str] = []
    for check in checks:
        label = check["label"]
        category = check["register_category"]
        proc_rel = check["procedure"]
        reg = register_value(register_text, category, period_re, unit_to_days)
        if reg is None:
            findings.append(
                f"{label}: register row '{category}' not found in {register_rel} "
                f"(or its period could not be parsed)."
            )
            continue
        proc_path = root / proc_rel
        proc_text = read_text_safe(proc_path) if proc_path.is_file() else None
        if proc_text is None:
            findings.append(f"{label}: cannot read procedure {proc_rel}.")
            continue
        proc = procedure_value(proc_text, procedure_anchor_re, unit_to_days)
        if proc is None:
            findings.append(
                f"{label}: no 'retained for a minimum of ...' statement found in "
                f"{proc_rel} (the retention citation may have been removed or reworded)."
            )
            continue
        reg_days, reg_raw = reg
        proc_days, proc_raw = proc
        if reg_days != proc_days:
            findings.append(
                f"{label}: MISMATCH. Register '{category}' says {reg_raw}; "
                f"{proc_rel} says {proc_raw}. Reconcile to a single canonical period."
            )
    return findings
