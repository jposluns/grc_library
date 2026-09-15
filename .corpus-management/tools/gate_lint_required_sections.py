#!/usr/bin/env python3
"""Required-sections-by-doctype audit (grc gate): pack-owned engine (source of record).

Enforce that a document of a modelled type carries the sections its type requires. A
document declares its type in a ``**Document Type:**`` field; the section model maps a
type to a list of required sections, each expressed as a list of accepted heading
aliases (any one alias satisfies the requirement). A type absent from the model is
unconstrained. Headings are read outside fenced code blocks.

Engine/wrapper split (compile PR-11): this engine carries the PURE check
(``DOCTYPE_RE``, ``HEADING_RE``, ``extract_doctype``, ``extract_headings``, ``scan``)
and a ``run`` that groups + reports; the project wrapper
(``tools/lint-required-sections.py``) supplies the grc-specific section model
(composed in ``_sections_config()`` from the ``sections`` reference-vocabulary
profile since Phase-4 PR-C), the target selection (the exempt-file set, the narrative /
default-exempt scope predicates), and the repository root, passing the model and root
in. This engine holds no project section-model or scan-scope policy.

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
        "(python3 tools/lint-required-sections.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

DOCTYPE_RE = re.compile(r"^\*\*Document Type:\*\*\s+(.+?)(?:\\)?\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")


def extract_doctype(text: str) -> str | None:
    m = DOCTYPE_RE.search(text)
    if not m:
        return None
    return m.group(1).strip().rstrip("\\").strip()


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for _lineno, line in iter_non_code_lines(text):
        m = HEADING_RE.match(line)
        if m:
            heading = m.group(2)
            # Strip leading numbering and punctuation
            cleaned = re.sub(r"^\d+(\.\d+)*[.\s:]*", "", heading)
            cleaned = re.sub(r"^Section\s+\d+(\.\d+)*[.\s:]*", "", cleaned)
            headings.append(cleaned.strip().lower())
    return headings


def scan(path: Path, required_map: dict[str, list[list[str]]]) -> list[str]:
    findings: list[str] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    doctype = extract_doctype(text)
    if doctype is None:
        return findings
    required = required_map.get(doctype)
    if not required:
        return findings
    headings = extract_headings(text)
    for requirement in required:
        # Each requirement is a list of acceptable heading names; at least
        # one must appear in the document's headings.
        matched = False
        for option in requirement:
            for h in headings:
                if option in h:
                    matched = True
                    break
            if matched:
                break
        if not matched:
            findings.append(f"missing required section (any of: {requirement})")
    return findings


def run(targets: list[Path], required_map: dict[str, list[list[str]]], *, repo_root: Path) -> int:
    grouped: dict[Path, list[str]] = {}
    for t in targets:
        findings = scan(t, required_map)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all documents have required sections by doctype (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(repo_root)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for msg in findings:
            print(f"  [required-section] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} required-section finding(s) across {len(grouped)} file(s).")
    print(
        "Documents missing canonically-expected sections by doctype. Either "
        "add the section under one of the acceptable heading names, or change "
        "the Document Type field to one that does not require this section."
    )
    return 1
