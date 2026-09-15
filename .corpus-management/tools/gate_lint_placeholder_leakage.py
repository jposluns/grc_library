#!/usr/bin/env python3
"""Placeholder-leakage audit (grc gate 12): pack-owned engine (source of record).

A production library document containing a placeholder marker is either a stub leaked into
production or a template artefact that escaped its template directory, and either is a credibility
problem for adopters. This engine carries the PURE check ALGORITHM over a placeholder-marker pattern set
(the ``placeholders`` reference-vocabulary profile since Phase-4 PR-H: TODO / TBD / FIXME / XXX / (placeholder) / [Unverified] / Coming soon, the
angle-bracket ``<role>`` / ``<date>`` / ``<version>`` family, and the template-placeholder
organization domains), a fence-aware ``scan`` (fenced code blocks are skipped so example syntax
does not false-positive), and a ``run`` that groups + reports.

Engine/wrapper split: the project wrapper (``tools/lint-placeholder-leakage.py``) supplies the grc
scan scope (default roots, the markdown selector, the exempt-file / exempt-dir / template- and
worklist- prefix policy via ``iter_targets`` + ``is_exempt``) and filters those files out before
delegating, so this engine holds no project-file policy. The pattern set is a generic
placeholder-marker inventory, supplied by the ``placeholders`` profile
(``defaults/grc/placeholders.toml``, loaded via the wrapper's ``_placeholders_config()`` since
Phase-4 PR-H) and passed to the check, like the stub-phrase list migrated in PR-G.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-placeholder-leakage.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# Patterns whose presence indicates a placeholder leak. Each pattern uses word boundaries or
# angle-bracket-syntax to avoid false matches on prose.
def placeholder_patterns(patterns) -> tuple[tuple["re.Pattern[str]", str], ...]:
    """Compose the loaded ``placeholders`` profile into ordered (compiled, label)
    pairs (Phase-4 PR-H); fail closed.

    ``patterns`` is the profile's ``patterns`` array: each item a table with a
    ``label`` string and a ``pattern`` that profile_loader has already compiled
    from its ``{regex, ignorecase}`` sub-table. ORDER IS PRESERVED (scan reports
    the first matching entry per line, so order is policy).
    """
    if not isinstance(patterns, list):
        raise ValueError("placeholders.patterns: expected an array of tables")
    composed: list[tuple["re.Pattern[str]", str]] = []
    for item in patterns:
        if (not isinstance(item, dict) or set(item) != {"label", "pattern"}
                or not isinstance(item.get("label"), str) or not item["label"]
                or not isinstance(item.get("pattern"), re.Pattern)):
            raise ValueError(
                "placeholders.patterns[*]: each needs a nonempty 'label' string "
                "and a compiled 'pattern' (a {regex, ignorecase} table)")
        composed.append((item["pattern"], item["label"]))
    return tuple(composed)


def scan(path: Path, *, patterns) -> list[tuple[int, str, str]]:
    """Return list of (line number, marker name, line excerpt) findings."""
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for pattern, label in patterns:
            if pattern.search(line):
                excerpt = line.strip()[:140]
                findings.append((lineno, label, excerpt))
                break  # one finding per line is enough
    return findings


def run(targets: list[Path], *, repo_root: Path, patterns) -> int:
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t, patterns=patterns)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: no placeholder leakage (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(repo_root)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, label, excerpt in findings:
            print(f"  L{lineno} [{label}] {excerpt}")
        total += len(findings)
    print(
        f"\nFAIL: {total} placeholder finding(s) across {len(grouped)} file(s)."
    )
    print(
        "Placeholders such as TODO, TBD, FIXME, XXX, or "
        "<YYYY-MM-DD>-style markers should not appear in production library "
        "documents. Either complete the content or move the document to the "
        "template directory (filename prefix `template-`)."
    )
    return 1
