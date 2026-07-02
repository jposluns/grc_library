#!/usr/bin/env python3
"""External-overlay license-consistency audit.

The project ships an "external overlay" of third-party rules under
``.claude/rules/external/``. Each subdirectory corresponds to a source
project (TikiTribe, Kariedo, addyosmani, etc.) and carries the source
project's own LICENSE file. The corpus linters (gate 15 in particular)
skip the external overlay because those files are not the project's
own content; they retain the source project's licence.

This audit enforces three invariants on the external overlay:

1. Every subdirectory of ``.claude/rules/external/`` MUST appear in
   the ``EXPECTED_LICENSE`` map below. Adding a new external source
   without declaring its expected licence is a configuration error.

2. Each subdirectory MUST contain a LICENSE file at its root, and the
   LICENSE's first non-empty line MUST match the expected source
   licence. Catches the failure mode of a LICENSE file being deleted
   or replaced with the wrong licence.

3. No markdown file under ``.claude/rules/external/`` MAY contain
   ``**License:** CC BY-SA 4.0`` (or any other claim to the project's
   own licence) in its metadata. External files retain their source
   project's licence; claiming the project's licence is incorrect.

Together with gate 15 (which enforces the project's own licence
discipline on the corpus), these three checks close the
licence-consistency loop: every file in the repository — project
content or external overlay — has its licence validated against the
appropriate expectation.

Exit codes: 0 pass, 1 findings, 2 internal error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

from lint_common import REPO_ROOT, read_text_safe


EXTERNAL_OVERLAY_DIR = REPO_ROOT / ".claude" / "rules" / "external"

# Map of (external source subdir name) -> (expected licence identifier).
# The expected identifier is matched against the LICENSE file's first
# non-empty line, case-insensitive prefix match. Adding a new external
# source requires adding an entry here.
EXPECTED_LICENSE: dict[str, str] = {
    "addyosmani": "MIT",
    "kariedo": "MIT",
    "tikitribe": "MIT",
}

# Project licence claim that external markdown files MUST NOT contain
# in their metadata block.
PROJECT_LICENCE_CLAIM = "**License:** CC BY-SA 4.0"

# Mapping from the LICENSE-file first-line prefix to the canonical
# identifier used in EXPECTED_LICENSE.
LICENSE_PREFIX_TO_IDENT: dict[str, str] = {
    "MIT License": "MIT",
    "Apache License": "Apache 2.0",
    "BSD ": "BSD",
    "BSD-": "BSD",
    "GNU GENERAL PUBLIC LICENSE": "GPL",
    "Mozilla Public License": "MPL",
    "ISC License": "ISC",
    "Creative Commons CC0": "CC0",
    "Creative Commons Attribution": "CC BY",
    "The Unlicense": "Unlicense",
}


class Finding(NamedTuple):
    kind: str
    location: str
    detail: str


def identify_license(text: str) -> str | None:
    """Return the canonical identifier of a LICENSE file's text, or None
    if no known prefix matches the file's first non-empty line."""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        for prefix, ident in LICENSE_PREFIX_TO_IDENT.items():
            if stripped.lower().startswith(prefix.lower()):
                return ident
        return None
    return None


def check() -> list[Finding]:
    findings: list[Finding] = []

    if not EXTERNAL_OVERLAY_DIR.is_dir():
        # No external overlay present; nothing to check. (Not a finding.)
        return findings

    declared_sources = set(EXPECTED_LICENSE.keys())
    present_sources: set[str] = set()
    for entry in EXTERNAL_OVERLAY_DIR.iterdir():
        if entry.is_dir() and not entry.name.startswith("."):
            present_sources.add(entry.name)

    # Check 1: every present source declares an expected licence.
    for source in sorted(present_sources - declared_sources):
        findings.append(
            Finding(
                kind="undeclared-source",
                location=f".claude/rules/external/{source}/",
                detail=(
                    f"present in the external overlay but no expected licence "
                    f"declared in EXPECTED_LICENSE. Add the source to the "
                    f"map in tools/lint-external-overlay-license.py."
                ),
            )
        )

    # Check 1b: every declared source is actually present (catches stale map entries).
    for source in sorted(declared_sources - present_sources):
        findings.append(
            Finding(
                kind="stale-declaration",
                location=f".claude/rules/external/{source}/",
                detail=(
                    f"declared in EXPECTED_LICENSE but no directory present. "
                    f"Remove the source from the map in "
                    f"tools/lint-external-overlay-license.py."
                ),
            )
        )

    # Check 2: each present, declared source has a LICENSE file matching expected.
    for source in sorted(present_sources & declared_sources):
        expected = EXPECTED_LICENSE[source]
        license_path = EXTERNAL_OVERLAY_DIR / source / "LICENSE"
        if not license_path.is_file():
            findings.append(
                Finding(
                    kind="missing-license-file",
                    location=f".claude/rules/external/{source}/LICENSE",
                    detail=(
                        f"expected to exist (source's licence is {expected}) "
                        f"but the file is absent or unreadable."
                    ),
                )
            )
            continue
        text = read_text_safe(license_path)
        if text is None:
            findings.append(
                Finding(
                    kind="unreadable-license-file",
                    location=f".claude/rules/external/{source}/LICENSE",
                    detail="LICENSE file is not readable as UTF-8 text.",
                )
            )
            continue
        actual = identify_license(text)
        if actual is None:
            findings.append(
                Finding(
                    kind="unrecognized-license",
                    location=f".claude/rules/external/{source}/LICENSE",
                    detail=(
                        f"LICENSE first non-empty line did not match any known "
                        f"prefix in LICENSE_PREFIX_TO_IDENT. Expected: {expected}. "
                        f"Either update the LICENSE to a recognized form or add "
                        f"a new prefix to LICENSE_PREFIX_TO_IDENT."
                    ),
                )
            )
            continue
        if actual != expected:
            findings.append(
                Finding(
                    kind="license-mismatch",
                    location=f".claude/rules/external/{source}/LICENSE",
                    detail=(
                        f"LICENSE file identifies as {actual}, but EXPECTED_LICENSE "
                        f"declares {expected}. Either the LICENSE was changed "
                        f"upstream (update EXPECTED_LICENSE) or the file is wrong."
                    ),
                )
            )

    # Check 3: no markdown file in the external overlay may claim the project licence.
    for source in sorted(present_sources):
        for md_file in (EXTERNAL_OVERLAY_DIR / source).rglob("*.md"):
            text = read_text_safe(md_file)
            if text is None:
                continue
            if PROJECT_LICENCE_CLAIM in text:
                rel = md_file.relative_to(REPO_ROOT).as_posix()
                findings.append(
                    Finding(
                        kind="external-file-claims-project-licence",
                        location=rel,
                        detail=(
                            f"contains the literal string '{PROJECT_LICENCE_CLAIM}' "
                            f"but is an external file. External files retain their "
                            f"source project's licence (per the overlay's "
                            f"directory-level LICENSE file)."
                        ),
                    )
                )

    return findings


def main(argv: list[str]) -> int:
    findings = check()
    if not findings:
        print(
            f"OK: external overlay licence consistency confirmed "
            f"({len(EXPECTED_LICENSE)} declared source(s); all LICENSE files "
            f"present and matching expected; no external markdown file claims "
            f"the project licence)."
        )
        return 0

    for finding in findings:
        print(f"=== {finding.kind} ===")
        print(f"  {finding.location}: {finding.detail}")
    print(
        f"\nFAIL: {len(findings)} external-overlay licence finding(s). "
        f"Resolve by updating EXPECTED_LICENSE, restoring the LICENSE file, "
        f"or removing the incorrect project-licence claim from the external file.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
