#!/usr/bin/env python3
"""Date-format audit (grc gate): pack-owned engine (source of record).

Validate that every ``**Date:**`` metadata field is an ISO 8601 ``YYYY-MM-DD``
date: four-digit year in the plausible range 1900-2100, a real calendar date,
and exact two-digit zero padding on month and day. A ``**Date:**`` line inside a
fenced code block is documentation of the metadata-block format, not the file's
own metadata, and is not validated (the shared fence-aware scan skips it). The
placeholder values ``YYYY-MM-DD`` and ``<YYYY-MM-DD>`` are legitimate ONLY in a
template or worklist file (whose own metadata carries fill-in markers by
design), detected by the ``template-`` / ``worklist-`` filename prefix; in any
other file a placeholder Date is a finding.

Engine/wrapper split (SHARED/SAFETY lane PR-33, Pattern A): this engine carries
the PURE check (``ISO_DATE_RE``, ``validate_date``, ``PLACEHOLDER_VALUES``, and
``scan``); the project wrapper (``tools/lint-date-format.py``) supplies the grc
scan scope (``iter_markdown_targets``) and the grouped reporting in ``main``, and
keeps a thin module-global ``scan`` shim delegating here, so the scan-scope
regression test (which patches ``mod.scan`` and runs ``main``) observes the
original signature and behaviour. The engine's ``scan`` is generic (no scan-scope
or repository-root policy).

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_date_format: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

# Literal placeholder values that appear in template/worklist metadata
# blocks (which carry fill-in markers by design). Production artefacts
# (anything not prefixed `template-` or `worklist-`) may not use these.
PLACEHOLDER_VALUES = {"YYYY-MM-DD", "<YYYY-MM-DD>"}


def validate_date(value: str) -> str | None:
    """Return None if value is valid ISO 8601 date, else an error message."""
    value = value.strip()
    m = ISO_DATE_RE.match(value)
    if not m:
        return f"not ISO 8601 YYYY-MM-DD: {value!r}"
    y, mth, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if y < 1900 or y > 2100:
        return f"year {y} outside plausible range 1900-2100"
    try:
        date(y, mth, d)
    except ValueError as exc:
        return f"invalid calendar date: {exc}"
    # Check zero padding by exact length
    if len(m.group(2)) != 2 or len(m.group(3)) != 2:
        return f"missing zero padding: {value!r}"
    return None


def scan(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    # Placeholder Date values are only legitimate in templates and
    # worklists (which carry fill-in markers as their own metadata).
    is_placeholder_eligible = (
        path.name.startswith("template-")
        or path.name.startswith("worklist-")
    )
    # Iterate only outside fenced code blocks. A `**Date:**` line
    # inside a code block is documentation showing the metadata-block
    # format, not the file's own metadata, and is not validated.
    for lineno, line in iter_non_code_lines(text):
        if line.startswith("**Date:**"):
            # Strip trailing backslash (CommonMark hard-break syntax)
            value = line[len("**Date:**"):].rstrip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            value = value.strip()
            if not value:
                findings.append((lineno, "empty Date field"))
                continue
            if value in PLACEHOLDER_VALUES:
                if is_placeholder_eligible:
                    # Template/worklist's own metadata is a fill-in marker.
                    continue
                findings.append((lineno, f"placeholder Date {value!r} in non-template file"))
                continue
            err = validate_date(value)
            if err:
                findings.append((lineno, err))
    return findings
