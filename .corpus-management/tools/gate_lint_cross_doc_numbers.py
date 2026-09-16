#!/usr/bin/env python3
"""Cross-document number-consistency audit (grc gate): pack-owned engine (source of record).

Extract, per file, the numeric values a set of tracked canonical terms carry (each
normalised to minutes), so a caller can detect when the same term carries different
values across documents. Most terms are read from prose only (outside fenced code
blocks); a term listed in ``TERMS_SCANNED_IN_CODE_FENCES`` is also read inside fenced
blocks (it has a normative carrier there). ``scan`` returns a per-file
``{term: {(normalised_minutes, raw_text), ...}}`` map; the wrapper's ``main``
aggregates those maps across the corpus and flags any term with more than one value.

Engine/wrapper split (SHARED/SAFETY lane PR-42, Pattern A): this engine carries the
tracked-term regexes (``TERM_PATTERNS``), the fence-scan set, the unit table, the
``normalise`` helper, and the per-file ``scan`` (which returns a dict, so the
scan-scope regression test's capture returns ``{}`` for this gate). The project wrapper
(``tools/lint-cross-doc-numbers.py``) supplies the grc scan scope and the exempt-file
set and the cross-document aggregation in ``main``, and keeps a thin module-global
``scan`` shim delegating here so the scan-scope test (which patches ``mod.scan`` and
runs ``main``) observes the original signature and behaviour. The engine's ``scan`` is
scope-free and repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more divergent terms.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_cross_doc_numbers: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


TERM_PATTERNS: dict[str, re.Pattern[str]] = {
    # Privileged-role activation maximum. PAM Section 4.2 is authoritative;
    # the alternative value-before-term form binds the portable authentication
    # guardrail. The lookahead may not cross a semicolon, so the guardrail row
    # "8 hours absolute; 1 hour for elevated privilege sessions" captures the
    # elevated-privilege value rather than the standard-session timeout.
    "privileged-role-activation-maximum": re.compile(
        r"(?:\bprivileged-role activation\b[^.;\n]{0,160}?"
        r"|(?=[^.;\n]{0,80}\bfor elevated privilege sessions\b))"
        r"(\d+)[\s\-]*(minute|hour)s?\b",
        re.IGNORECASE,
    ),
    # GDPR (and UK GDPR) breach notification: Article 33 sets a 72-hour
    # deadline. Captures the first N-hour fragment after "GDPR" on the
    # same line, requiring "breach", "notif", "report", or "notify" to
    # appear within the same window to narrow the FP surface. Statutory:
    # any value other than 72 indicates a defect.
    "GDPR-breach-notification-hours": re.compile(
        r"\b(?:UK\s+)?GDPR\b[^.\n]{0,250}?(?:breach|notif|notify|report)[^.\n]{0,150}?(\d+)[\s\-]*(hour)s?\b",
        re.IGNORECASE,
    ),
}

# Most tracked terms inspect prose only. This term also has a normative
# carrier inside the portable guardrail's fenced timeout block.
TERMS_SCANNED_IN_CODE_FENCES: frozenset[str] = frozenset(
    {"privileged-role-activation-maximum"}
)

UNIT_TO_MINUTES = {
    "minute": 1,
    "hour": 60,
    "day": 60 * 24,
    "business day": 60 * 8,  # 8-hour business day
}


def normalise(value: int, unit: str) -> int:
    """Return value in minutes."""
    unit_clean = unit.lower().rstrip("s")
    return value * UNIT_TO_MINUTES.get(unit_clean, 0)


def scan(path: Path) -> dict[str, set[tuple[int, str]]]:
    """Return {term: {(normalised_minutes, raw_text), ...}} for the file."""
    out: dict[str, set[tuple[int, str]]] = defaultdict(set)
    text = read_text_safe(path)
    if text is None:
        return out
    non_code_lines = tuple(iter_non_code_lines(text))
    all_lines = tuple(enumerate(text.splitlines(), start=1))
    for term, pattern in TERM_PATTERNS.items():
        lines = all_lines if term in TERMS_SCANNED_IN_CODE_FENCES else non_code_lines
        for _lineno, line in lines:
            for m in pattern.finditer(line):
                value = int(m.group(1))
                unit = m.group(2)
                norm = normalise(value, unit)
                raw = f"{value} {unit}"
                out[term].add((norm, raw))
    return out
