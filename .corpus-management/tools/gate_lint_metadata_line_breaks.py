#!/usr/bin/env python3
"""Metadata-block line-break audit (grc gate): pack-owned engine (source of record).

Detect runs of consecutive ``**Field:**`` metadata lines that lack a Markdown
hard-break marker on the non-last lines of the run. Without a hard-break, GitHub
renders the metadata block as a single soft-wrapped paragraph rather than as a
vertical list of labelled facts. Two hard-break markers are accepted: a trailing
backslash (``\\``) or two-or-more trailing spaces. The last line of a run is exempt
(the following blank line or ``---`` separator already breaks the paragraph).
Fenced code blocks are skipped via ``aiqt_corpus.iter_non_code_lines``, so a
metadata-format example inside ``` ``` ``` is not a false positive.

Engine/wrapper split (SHARED/SAFETY lane, Pattern A): this engine carries the PURE
check (``META_LINE``, ``has_hard_break``, ``scan_file``); the project wrapper
(``tools/lint-metadata-line-breaks.py``) supplies the grc scan scope
(``DEFAULT_TARGETS`` / ``iter_target_files``) and the grouped reporting in ``main``,
and keeps a thin module-global ``scan_file`` shim delegating here, so the
scan-scope regression test (which patches ``mod.scan_file`` and runs ``main``)
observes the original signature and behaviour. The engine's check is generic (no
scan-scope or repository-root policy).

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_metadata_line_breaks: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# A field name starts with a letter and runs, without an asterisk, to the closing colon, so a
# hyphen, slash, parenthesis or underscore in it (an SPDX-License-Identifier-style key, an
# "Owner/Approver" key) cannot split a run and hide a missing hard break before it (P-1.89(b)).
META_LINE = re.compile(r"^\*\*[A-Za-z][^*]*?:\*\*")


def has_hard_break(line: str) -> bool:
    """A line has a Markdown hard-break marker if it ends with ``\\`` or two-plus spaces."""
    if line.endswith("\\"):
        return True
    if len(line) >= 2 and line.endswith("  "):
        return True
    return False


def scan_file(path: Path) -> list[tuple[int, int]]:
    """Return ``[(block_start_line, missing_count), ...]`` for every offending block."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, int]] = []
    block: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal block
        if len(block) >= 2:
            non_last = block[:-1]
            missing = sum(1 for _, ln in non_last if not has_hard_break(ln))
            if missing:
                findings.append((block[0][0], missing))
        block = []

    prev = 0
    for lineno, line in iter_non_code_lines(text):
        # The fence-aware scan omits fenced lines, so a gap in line numbers is a fenced block.
        # A fence between metadata lines ends the run: the lines either side are not one
        # paragraph, so the one before the fence needs no hard break (P-1.89(c)).
        if lineno != prev + 1:
            flush()
        prev = lineno
        if META_LINE.match(line):
            block.append((lineno, line))
        else:
            flush()
    flush()
    return findings
