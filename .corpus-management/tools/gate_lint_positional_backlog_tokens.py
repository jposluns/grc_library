#!/usr/bin/env python3
"""Positional backlog-token audit (grc gate): pack-owned engine (source of record).

Flag a positional reference to a backlog item by its section-shaped token, qualified by
``TODO`` (optionally ``TODO item(s)``) or ``backlog item(s)`` immediately before a
section token (a ``§``- or ``P``-prefixed number, or a dotted ``N.M``). A backlog item's
position is not a durable identifier, so a cross-reference must name the item some other
way. A bare single digit with no prefix and no dot is deliberately NOT matched (too
ambiguous). Blockquote lines are skipped, and inline backtick code spans are stripped
before matching so a backticked mention does not register.

Engine/wrapper split (compile PR-16): this engine carries the PURE check (``POSITIONAL_REF``,
the code-span strip, ``check_file``) and a ``run`` that groups + reports; the project wrapper
(``tools/lint-positional-backlog-tokens.py``) supplies the scan scope and the grc-specific
exempt-file set (the backlog source and append-only history). The engine's ``check_file`` is
generic (no exempt-file or repository-root policy); the wrapper filters the exempt files and
also keeps a thin ``check_file`` shim (exempt-check plus this engine's check) so a direct-call
regression test observes the original signature and behaviour.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import SIMPLE_CODE_SPAN_RE, iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-positional-backlog-tokens.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# A backlog reference qualified by TODO / TODO item(s) / backlog item(s) immediately before a
# section-shaped token (a §- or P-prefixed number, or a dotted N.M). Case-sensitive TODO;
# "item(s)" / "backlog item(s)" either case.
POSITIONAL_REF = re.compile(
    r"(?<![\w-])(?:TODO(?:\s+[Ii]tems?)?|[Bb]acklog items?)\s+(?:(?:§|P)\d+(?:\.\d+)*|\d+\.\d+)\b"
)

# Inline backtick code spans: stripped before matching so a backticked mention does not register.
INLINE_CODE_SPAN = SIMPLE_CODE_SPAN_RE


def check_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (lineno, match) findings. PURE (the wrapper applies the exempt-file policy)."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, str]] = []
    for lineno, line in iter_non_code_lines(text):
        if line.lstrip().startswith(">"):
            continue
        stripped = INLINE_CODE_SPAN.sub("", line)
        m = POSITIONAL_REF.search(stripped)
        if m:
            findings.append((lineno, m.group(0)))
    return findings


def run(files: list[Path], *, repo_root: Path) -> int:
    grouped: dict[str, list[tuple[int, str]]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        findings = check_file(f)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no renumber-fragile positional backlog-token references in "
              "corpus and pack prose.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, token in findings:
            print(f"  line {lineno}: {token!r} (reword to the stable coded id "
                  f"FR-N / GR-N / SR-N or the topic name)")
    print(f"\nFAIL: {total} positional backlog reference(s) in corpus and pack prose.")
    return 1
