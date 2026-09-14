#!/usr/bin/env python3
"""Stub-document audit (grc gate): pack-owned engine (source of record).

Flag a production document that is a stub: its body (metadata block stripped) falls
below a substantive-word-count threshold, or it carries a stub-indicator phrase
(``[content to be added]``, ``details forthcoming``, ``stub document`` and kin). A body
under threshold is flagged; a stub phrase is flagged even in a longer body, because
mixing finished content with a stub marker is itself a defect. Code-fenced lines are not
counted toward the word count.

Engine/wrapper split (compile PR-17): this engine carries the PURE check (the stub-phrase
list, the word-count threshold, ``extract_body``, ``count_substantive_words``, ``scan``)
and a ``run`` that groups + reports; the project wrapper (``tools/lint-stub-documents.py``)
supplies the scan scope and the grc-specific target selection (the exempt files, the
``template-`` / ``worklist-`` / ``Status: Superseded`` skips, the narrative / default-exempt
predicates via ``is_target`` + ``iter_targets``). This engine holds no scan-scope or
project-file policy.

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
        "(python3 tools/lint-stub-documents.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

WORD_COUNT_THRESHOLD = 100  # words in document body, excluding metadata block

# Stub indicator phrases. If a document has any of these AND is under threshold,
# it's flagged. If it has any of these AND is over threshold, it's flagged
# because mixing finished content with stub markers is itself a defect.
STUB_PHRASES = [
    "[content to be added]",
    "[to be added]",
    "[to be defined]",
    "[to be completed]",
    "[details forthcoming]",
    "details forthcoming",
    "content forthcoming",
    "to be completed in a later phase",
    "section to be added",
    "stub document",
    "placeholder document",
]


def extract_body(text: str) -> str:
    """Return document body with metadata block stripped.

    Library metadata block ends at the first horizontal rule (---) after the
    initial header line. If no metadata block delimiter is found, return the
    whole text.
    """
    lines = text.splitlines()
    # Find first --- after first content
    seen_content = False
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if seen_content:
                body_start = i + 1
                break
        elif line.strip():
            seen_content = True
    return "\n".join(lines[body_start:])


def count_substantive_words(text: str) -> int:
    """Return rough word count of substantive prose.

    Skips code blocks. Counts whitespace-separated tokens that include at
    least one alphabetic character.
    """
    count = 0
    for _lineno, line in iter_non_code_lines(text):
        # Strip markdown formatting characters to a coarse approximation
        clean = re.sub(r"[`*_#>|\-]+", " ", line)
        for tok in clean.split():
            if re.search(r"[A-Za-z]", tok):
                count += 1
    return count


def scan(path: Path) -> list[str]:
    findings: list[str] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    body = extract_body(text)
    word_count = count_substantive_words(body)
    body_lower = body.lower()
    matched_phrases = [p for p in STUB_PHRASES if p.lower() in body_lower]
    if word_count < WORD_COUNT_THRESHOLD:
        findings.append(
            f"body word count {word_count} below threshold {WORD_COUNT_THRESHOLD}"
        )
    if matched_phrases:
        findings.append(
            f"stub-indicator phrase(s) present: {', '.join(repr(p) for p in matched_phrases)}"
        )
    return findings


def run(targets: list[Path], *, repo_root: Path) -> int:
    grouped: dict[Path, list[str]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: no stub documents (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        rel = path.relative_to(repo_root) if path.is_relative_to(repo_root) else path
        print(f"=== {rel} ===")
        for msg in findings:
            print(f"  [stub-document] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} stub-document finding(s) across {len(grouped)} file(s).")
    print(
        "Stub documents (under the word-count threshold or containing stub-indicator "
        "phrases) should be completed or moved to the template directory."
    )
    return 1
