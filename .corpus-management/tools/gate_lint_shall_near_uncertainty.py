#!/usr/bin/env python3
"""Mandatory-near-uncertainty audit (grc gate): pack-owned engine (source of record).

Flag a mandatory-requirement word (``shall`` / ``must`` / ``is required`` and kin) that
appears within a small line window of an uncertainty marker (``TBD``, ``TODO``,
``FIXME``, ``[Unverified]``, ``placeholder`` and kin): a prescriptive requirement sitting
next to an unfinished-content marker is a drafting hazard. Both markers are read outside
fenced code blocks (a marker inside a fence is example syntax, not prose).

Engine/wrapper split (compile PR-14; vocab externalized in Phase-4 PR-I): this engine carries
the PURE check ALGORITHM (the two-pass window scan, fence exclusion, ``check_file``) and takes
the uncertainty + mandatory patterns + the window as an ``UncertaintyVocabulary`` (moved to the
``uncertainty`` reference-vocabulary profile, ``defaults/grc/uncertainty.toml``); a ``run`` groups
+ reports; the
project wrapper (``tools/lint-shall-near-uncertainty.py``) supplies the grc scan scope and the
grc-specific exempt-file set (filtered out before delegating), so this engine holds no
scan-scope or project-file policy and is repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

try:
    from aiqt_corpus import is_fence_line, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-shall-near-uncertainty.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

class UncertaintyVocabulary(NamedTuple):
    """The adopter-overridable mandatory-near-uncertainty vocabulary (Phase-4 PR-I).

    The check ALGORITHM (the two-pass window scan, fence exclusion) stays in this
    engine; only these DATA move to the ``uncertainty`` reference-vocabulary
    profile and are passed in. ``patterns`` order is policy (check_file reports the
    first matching uncertainty pattern per line).
    """
    patterns: tuple
    mandatory: "re.Pattern[str]"
    window_lines: int


def uncertainty_vocabulary(*, patterns, mandatory, window_lines) -> "UncertaintyVocabulary":
    """Compose the loaded profile (loader-compiled patterns) into the vocabulary;
    fail closed. ``patterns`` and ``mandatory`` are already compiled ``re.Pattern``
    objects (profile_loader compiles the {regex, ignorecase} tables)."""
    if not isinstance(patterns, list) or any(
        not isinstance(pat, re.Pattern) for pat in patterns
    ):
        raise ValueError(
            "uncertainty.patterns: expected an array of {regex, ignorecase} tables")
    if not isinstance(mandatory, re.Pattern):
        raise ValueError(
            "uncertainty.mandatory: expected a {regex, ignorecase} table")
    if (not isinstance(window_lines, int) or isinstance(window_lines, bool)
            or window_lines < 0):
        raise ValueError("uncertainty.window_lines: expected a nonnegative integer")
    return UncertaintyVocabulary(tuple(patterns), mandatory, window_lines)


def check_file(path: Path, *, vocab: UncertaintyVocabulary) -> list[tuple[int, str, str]]:
    """Return list of (lineno, uncertainty_match, line_snippet) findings. PURE (the wrapper filters exempt files)."""
    text = read_text_safe(path)
    if text is None:
        return []
    lines = text.splitlines()
    findings: list[tuple[int, str, str]] = []

    # Pre-compute the set of line indices that fall inside a fenced
    # code block. Both passes consult this set so a mandatory marker
    # inside a code block within window range of an uncertainty marker
    # outside the code block is correctly skipped (and vice versa).
    in_code_lines: set[int] = set()
    in_code_block = False
    for i, line in enumerate(lines):
        if is_fence_line(line):
            in_code_block = not in_code_block
            in_code_lines.add(i)  # the fence line itself is also non-content
            continue
        if in_code_block:
            in_code_lines.add(i)

    # First pass: locate uncertainty markers outside code blocks.
    uncertainty_lines: dict[int, str] = {}
    for i, line in enumerate(lines):
        if i in in_code_lines:
            continue
        for pat in vocab.patterns:
            m = pat.search(line)
            if m:
                uncertainty_lines[i] = m.group(0)
                break

    # Second pass: scan a window around each uncertainty marker for
    # mandatory words. Skip mandatory-marker lines that sit inside a
    # code block: they are example syntax, not prescriptive prose.
    for u_line, u_marker in uncertainty_lines.items():
        lo = max(0, u_line - vocab.window_lines)
        hi = min(len(lines), u_line + vocab.window_lines + 1)
        for i in range(lo, hi):
            if i in in_code_lines:
                continue
            if vocab.mandatory.search(lines[i]):
                findings.append((u_line + 1, u_marker, lines[u_line].strip()[:150]))
                break

    return findings


def run(files: list[Path], *, repo_root: Path, vocab: UncertaintyVocabulary) -> int:
    grouped: dict[str, list[tuple[int, str, str]]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        findings = check_file(f, vocab=vocab)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no mandatory-near-uncertainty findings.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, marker, snippet in findings:
            print(f"  L{lineno} [near {marker}] {snippet}")

    print(f"\nFAIL: {total} finding(s) across {len(grouped)} file(s).")
    print("Mandatory shall/must/will requirements should not appear next to uncertainty markers.")
    print("Either complete the requirement (remove the marker) or soften the language (may, recommended).")
    return 1
