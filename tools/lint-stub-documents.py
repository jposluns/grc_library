#!/usr/bin/env python3
"""Detect stub documents masquerading as production library content.

A stub document is one that exists in the repository but contains
no substantive content: a metadata block followed by an empty body,
an "end of document" marker only, or a body consisting of placeholder
phrases (see STUB_PHRASES) such as "[content to be added]", "details
forthcoming", "to be completed in a later phase", or "stub document".

This linter catches such stubs in artefact documents. README files,
NOTICE, AUTHORS, and CHANGELOG (which describes the linter patterns
and is therefore self-referential) are exempt by name in EXEMPT_FILES.
LICENSE and CITATION.cff were previously listed but removed in Phase
23.62 since they are not .md files and the scanner only processes .md.
The audit-programme specification is also exempt because its §6
inventory legitimately contains the phrase "stub document" as a gate
name.

Documents explicitly marked ``**Status:** Superseded`` (the lifecycle
marker, re-keyed from the former ``Classification: Deprecated``
overload) are exempt: a superseded document is allowed to be a short
redirect notice. The exemption is implemented by scanning the metadata
block for the Superseded status before applying the word-count rule.

Word-count threshold (post-metadata, post-trailing-marker): 100 words.
Files under threshold are flagged unless exempted above. The linter
does not implement a table-content exemption.

Usage:
    python3 tools/lint-stub-documents.py
    python3 tools/lint-stub-documents.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more stub-document findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

WORD_COUNT_THRESHOLD = 100  # words in document body, excluding metadata block

EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS

# Files exempt because they are indexes / short by design / describe the linter patterns.
# Phase 23.62 removed `LICENSE` and `CITATION.cff` from this set: the
# linter scans `.md` files only, so non-`.md` entries were unreachable.
EXEMPT_FILES = {
    "README.md",  # domain READMEs are indexes; main README is a navigation hub
    "NOTICE.md",  # license notice; short by design
    "AUTHORS.md",
    # CHANGELOG.md describes phase changes including this linter's patterns.
    "CHANGELOG.md",
    # The Audit Programme Specification names this gate in its inventory
    # and therefore contains the literal phrase "stub document".
    "specification-audit-programme.md",
}

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


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    # Templates legitimately have placeholder content.
    if path.name.startswith("template-"):
        return False
    # Worklists have blank fields for human completion.
    if path.name.startswith("worklist-"):
        return False
    # Documents marked Status: Superseded (the lifecycle marker) are
    # deliberately short redirect notices and not stubs.
    try:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\*\*Status:\*\*\s+Superseded", text, re.MULTILINE):
            return False
    except (OSError, UnicodeDecodeError):
        pass
    return True


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


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect stub documents in production library content."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
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
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
