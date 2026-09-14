#!/usr/bin/env python3
"""Framework-citation denylist audit (grc gate): pack-owned engine (source of record).

Flag a line that cites an identifier on a citation denylist: a set of known-wrong
framework or standard identifiers, each paired with the reason it is wrong and the
identifier to use instead. A line outside a fenced code block that contains a
denylisted term is flagged, unless the document's path is on that term's exemption
list. Lines inside fenced code blocks are not scanned.

Engine/wrapper split (compile PR-12): this engine carries the PURE check
(``check_file``) and a ``run`` that groups + reports; the project wrapper
(``tools/lint-citations.py``) supplies the grc-specific denylist and per-term path
exemptions, the scan scope, and the repository root, passing them in. This engine
holds no project denylist, exemption, or scan-scope policy.

A denylist entry is a ``(term, why, suggested_replacement)`` tuple; the path
exemptions are a ``{term: {relpath, ...}}`` map.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-citations.py), which bootstraps the vendored copy, or put "
        "the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc


def check_file(
    path: Path,
    denylist: list[tuple[str, str, str]],
    path_exemptions: dict[str, set[str]],
    *,
    repo_root: Path,
) -> list[tuple[str, int, str, str, str]]:
    """Return list of (term, lineno, line, why, suggested_replacement) findings."""
    relative = path.relative_to(repo_root).as_posix()
    findings: list[tuple[str, int, str, str, str]] = []

    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for term, why, suggested in denylist:
            if relative in path_exemptions.get(term, set()):
                continue
            if term in line:
                findings.append((term, lineno, line.strip(), why, suggested))

    return findings


def run(
    files: list[Path],
    denylist: list[tuple[str, str, str]],
    path_exemptions: dict[str, set[str]],
    *,
    repo_root: Path,
) -> int:
    grouped: dict[str, list[tuple[str, int, str, str, str]]] = {}
    total = 0

    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        findings = check_file(f, denylist, path_exemptions, repo_root=repo_root)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no citation findings.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for term, lineno, line, why, suggested in findings:
            print(f"  L{lineno} [{term}] -> {suggested}")
            print(f"     {why}")
            print(f"     line: {line[:140]}")

    print(f"\nFAIL: {total} citation finding(s) across {len(grouped)} file(s).")
    return 1
