#!/usr/bin/env python3
"""License-consistency audit (grc gate): pack-owned engine (source of record).

Validate that every ``**License:**`` metadata field carries exactly the canonical
license string. A ``**License:**`` line is read anywhere in the file (the check is
NOT fence-aware: it scans raw physical lines), its value taken after the label with
a trailing CommonMark hard-break backslash stripped; a value differing from the
canonical string is a finding.

Engine/wrapper split (SHARED/SAFETY lane PR-34, Pattern A): this engine carries the
canonical string (``CANONICAL_LICENSE``) and the pure ``scan``; the project wrapper
(``tools/lint-license-consistency.py``) supplies the grc scan scope
(``iter_markdown_targets``) and the grc-specific exempt-file set (files whose License
value is nuanced by design, e.g. ``NOTICE.md``), the grouped reporting in ``main``,
and keeps a thin module-global ``scan`` shim delegating here so the scan-scope
regression test (which patches ``mod.scan`` and runs ``main``) observes the original
signature and behaviour. The engine's ``scan`` is scope-free and repo_root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

from pathlib import Path

try:
    from aiqt_corpus import read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_license_consistency: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

CANONICAL_LICENSE = "CC BY-SA 4.0"


def scan(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.startswith("**License:**"):
            value = line[len("**License:**"):].rstrip()
            # Strip CommonMark hard-break backslash
            if value.endswith("\\"):
                value = value[:-1]
            value = value.strip()
            if value != CANONICAL_LICENSE:
                findings.append(
                    (lineno, f"license value {value!r} differs from canonical {CANONICAL_LICENSE!r}")
                )
    return findings
