#!/usr/bin/env python3
"""Standards-currency audit (grc gate): pack-owned engine (source of record).

Flag a stale external-standard citation: a standard identifier cited with a version the
canonical register lists as superseded. The register supplies, per standard, the current
version and the superseded version strings; a line citing ``<id>:<version>``,
``<id> <version>``, ``<id> (<version>)``, or a ``v``-prefixed variant, where the version is
a superseded one, is flagged (a version-continuation guard prevents matching inside a longer
version string, e.g. ``4.0`` inside ``4.0.1``). Lines inside fenced code blocks are not scanned.

Engine/wrapper split (compile PR-19): this engine carries the PURE check
(``compile_entry_patterns`` turns register entries into compiled patterns; ``check_file``
matches them; ``run`` groups + reports), taking the compiled patterns and the entry count in.
The project wrapper (``tools/lint-standards-currency.py``) supplies the scan scope and the grc
canonical-citations REGISTER (it parses the grc register format, handles the ``--root``
fixture-isolation override, and passes the parsed-and-compiled patterns + counts in). This
engine holds no register-format, scan-scope, or repository-path policy.

A register entry is a dict ``{"id", "current", "superseded": [...]}``; a compiled item is a
``(prefilter, pattern, message)`` triple.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings (register/root error
paths are the wrapper's).
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-standards-currency.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc


def compile_entry_patterns(
    entries: list[dict[str, object]],
) -> list[tuple[str | None, re.Pattern[str], str]]:
    """Compile one (prefilter, pattern, finding-message) triple per (entry, superseded version).

    Compiled once per run rather than per scanned line: the patterns depend only on the
    register entries, and rebuilding them inside the per-line scan loop dominated runtime.
    The triple order preserves the register's entry order and each entry's superseded-list
    order, so the per-line finding order is unchanged.

    ``prefilter`` is the lower-cased standard id when the id is pure ASCII, else ``None``.
    Every pattern begins with the escaped standard id under ``re.IGNORECASE``. The prefilter
    substring test is applied ONLY when the LINE is ASCII (see ``check_file``): on an ASCII
    line ``str.lower`` and ``re.IGNORECASE`` agree exactly, so an ASCII id absent from the
    lower-cased line cannot match the pattern, making the skip a pure fast-path. A non-ASCII
    line, or a non-ASCII id (prefilter ``None``), bypasses the prefilter and runs the full
    pattern; both preserve exact equivalence with running every pattern on every line.
    """
    compiled: list[tuple[str | None, re.Pattern[str], str]] = []
    for entry in entries:
        std_id = entry["id"]
        current = entry["current"]
        superseded_list = entry["superseded"]  # type: ignore[assignment]
        if not isinstance(superseded_list, list):
            continue

        std_id_re = re.escape(str(std_id))
        for superseded in superseded_list:
            sup_re = re.escape(superseded)
            # The negative lookahead (?![.\-][\d\w]) prevents matching inside a longer
            # version string (e.g. "PCI DSS 4.0" must NOT match within "PCI DSS 4.0.1").
            # The optional "v?" admits a "v"-prefixed version label ("PCI DSS v4.0").
            pattern = re.compile(
                rf"\b{std_id_re}\b\s*(?::|\(|\s+)\s*v?{sup_re}\b(?![.\-][\d\w])",
                flags=re.IGNORECASE,
            )
            id_text = str(std_id)
            prefilter = id_text.lower() if id_text.isascii() else None
            compiled.append(
                (
                    prefilter,
                    pattern,
                    f"stale citation '{std_id} {superseded}' "
                    f"(current: {current})",
                )
            )
    return compiled


def check_file(
    path: Path, compiled: list[tuple[str | None, re.Pattern[str], str]]
) -> list[tuple[int, str]]:
    """Return list of (line-number, message) findings for the file."""
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for ln, line in iter_non_code_lines(text):
        line_lower = line.lower()
        line_is_ascii = line.isascii()
        for prefilter, pattern, message in compiled:
            if prefilter is not None and line_is_ascii and prefilter not in line_lower:
                continue
            if pattern.search(line):
                findings.append((ln, message))

    return findings


def run(
    files: list[Path],
    compiled: list[tuple[str | None, re.Pattern[str], str]],
    num_entries: int,
    *,
    repo_root: Path,
) -> int:
    total_findings = 0
    by_file: dict[str, list[tuple[int, str]]] = {}
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        findings = check_file(f, compiled)
        if findings:
            by_file[rel] = findings
            total_findings += len(findings)

    if total_findings == 0:
        print(
            f"OK: no standards-currency findings (checked {num_entries} standards "
            f"across {len(files)} files)."
        )
        return 0

    for rel, findings in sorted(by_file.items()):
        print(f"=== {rel} ===")
        for ln, msg in findings:
            print(f"  L{ln}: {msg}")

    print()
    print(
        f"FAIL: {total_findings} standards-currency finding(s) "
        f"across {len(by_file)} file(s)."
    )
    return 1
