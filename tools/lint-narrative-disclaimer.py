#!/usr/bin/env python3
"""Narrative disclaimer-presence gate (gate 89): the universal authority disclaimer,
verbatim and in the required position, on every executive-narrative page.

Every narrative page under the root ``executive/`` tree (except the single named,
path-scoped entry point ``executive/README.md``) must carry the universal
authority disclaimer VERBATIM as the first body content after the metadata
block's closing ``---`` separator and before the first section heading
(``specification-executive-narrative.md``, "Narrative status and the authority
disclaimer", and Gates item 5). The disclaimer is universal and identical on
every page; subtype-specific cautions belong in the page's limitations section,
never in a modified disclaimer.

This gate proves a STRING-LEVEL property only: that the exact disclaimer text is
present in the required position. It does not certify the absence of authority
confusion in the reader, which is a review outcome backed by the per-claim
matrices, not a mechanical guarantee (spec, the separation-invariant paragraph).

Position rule: after the leading metadata run's closing ``---`` separator, the
FIRST non-blank body line must be the verbatim disclaimer blockquote at column 0.
Anything else first (a section heading, prose, a fenced block, an indented copy,
a different blockquote) is a defect: the disclaimer is missing or misplaced. A
fenced or indented copy is body content that is not the rendered disclaimer, so
it does not satisfy the requirement.

Fail-loud: a page that cannot be read as UTF-8 is a finding, never silently
skipped (a page whose disclaimer cannot be read cannot be cleared of the
requirement).

Usage:
    python3 tools/lint-narrative-disclaimer.py
    python3 tools/lint-narrative-disclaimer.py --self-test

Exit codes:
    0 : every narrative page carries the verbatim disclaimer in position (or the
        executive/ tree holds no narrative pages).
    1 : at least one page is missing the disclaimer, has it non-verbatim, or has
        it out of position; or a page is not readable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lint_common import (
    METADATA_FIELD_RE,
    REPO_ROOT,
    read_text_safe,
)

# The single named, PATH-scoped entry-point exemption, applied consistently
# across every narrative gate (spec Gates item 4 / listing-surface note).
ENTRY_POINT = "executive/README.md"

# The universal authority disclaimer, VERBATIM, fixed by the specification
# ("Narrative status and the authority disclaimer"). It is one blockquote line;
# the match is exact (stripped of surrounding whitespace only), so a rewrap, a
# typo, or a modified clause is a defect.
DISCLAIMER = (
    "> **Authority disclaimer.** This page is an executive narrative. It does not "
    "establish requirements; the linked corpus governs. It is provided to support "
    "understanding, discussion, and decision-making by the governing body and "
    "accountable executive leadership (board, ELT, or senior management, as "
    "applicable). It creates no obligation, control, or assurance by itself. Its "
    "publication approval is an editorial act only and confers no authority over "
    "any corpus document. Where it differs from a corpus document, the corpus "
    "document prevails."
)



def disclaimer_finding(text: str, rel: str) -> str | None:
    """Return a finding string if the page lacks the verbatim disclaimer in the
    required position, else None. PURE (operates on the page text)."""
    lines = text.splitlines()

    # Locate the leading metadata block's closing `---` separator. The metadata
    # block is the CONTIGUOUS leading run of metadata-field lines (matching
    # METADATA_FIELD_RE, so a `**bold body**` paragraph is NOT a field: it lacks
    # the `Name:**` label), optionally preceded by a `# Title` and blank lines,
    # ending at the first `---` after that run. Body text therefore cannot FORGE
    # the anchor: a `**bold**` paragraph plus a later `---` is not a metadata block.
    seen_field = False
    close_idx: int | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if METADATA_FIELD_RE.match(line):
            seen_field = True
            continue
        if not seen_field:
            # Before any field: tolerate a leading `# Title` and blank lines; any
            # other non-field content means there is no leading metadata block.
            if not stripped or stripped.startswith("#"):
                continue
            break
        # After the field run: tolerate blank lines up to the closing `---`.
        if not stripped:
            continue
        if stripped == "---":
            close_idx = i
            break
        # A non-field, non-blank, non-`---` line ends the run without a separator.
        break

    if close_idx is None:
        return (
            f"{rel}: could not locate the metadata block's closing '---' separator, "
            f"so the authority disclaimer's required position cannot be confirmed "
            f"(the disclaimer must be the first body content after that separator)"
        )

    # The FIRST non-blank line after the closing `---` must be the verbatim
    # disclaimer. Fences are NOT skipped: a fenced block is body content, so a
    # fence appearing before the disclaimer means the disclaimer is not the first
    # body content. The comparison uses rstrip only (never lstrip), so a leading-
    # indented line (a Markdown indented CODE block, not a rendered blockquote) is
    # not accepted as the disclaimer.
    for line in lines[close_idx + 1:]:
        if not line.strip():
            continue
        if line.rstrip() == DISCLAIMER:
            return None
        if line.lstrip().startswith("#"):
            return (
                f"{rel}: the first body content after the metadata block is a section "
                f"heading, not the authority disclaimer; the verbatim disclaimer must "
                f"appear before the first section heading"
            )
        return (
            f"{rel}: the first body content after the metadata block is not the "
            f"verbatim authority disclaimer (found: {line.strip()[:60]!r}...); the "
            f"disclaimer text is fixed by the specification and must appear verbatim "
            f"at column 0, as the first body content"
        )

    return (
        f"{rel}: no body content after the metadata block; the verbatim authority "
        f"disclaimer is required as the first body content"
    )


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return [
            f"{rel}: not readable / not utf-8 (a page whose disclaimer cannot be read "
            f"cannot be cleared of the requirement; fail loud, not open)"
        ]
    finding = disclaimer_finding(text, rel)
    return [finding] if finding else []


def discover(root: Path = REPO_ROOT) -> list[tuple[Path, str]]:
    """Narrative pages: every .md under the root executive/ tree, minus the
    entry-point exemption. Anchored at <root>/executive by construction."""
    exec_root = root / "executive"
    if not exec_root.is_dir():
        return []
    pages: list[tuple[Path, str]] = []
    for p in sorted(exec_root.rglob("*.md")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel == ENTRY_POINT:
            continue
        pages.append((p, rel))
    return pages


def _self_test() -> int:
    meta = (
        "# Why controls matter\n\n"
        "**Document Title:** Why controls matter\\\n"
        "**Document Type:** Executive Narrative\\\n"
        "**Version:** 0.0.1\\\n"
        "---\n\n"
    )
    section = "\n## Overview\n\nBody.\n"
    cases: list[tuple[str, str, bool]] = [
        # (name, page_text, expect_finding)
        ("valid", meta + DISCLAIMER + "\n" + section, False),
        ("valid-extra-blank", meta + "\n\n" + DISCLAIMER + "\n" + section, False),
        ("missing-disclaimer", meta + section, True),
        ("heading-first", meta + "## Overview\n\nBody.\n", True),
        ("prose-first", meta + "Some intro prose.\n\n" + DISCLAIMER + "\n", True),
        ("non-verbatim", meta + "> **Authority disclaimer.** This page is an executive narrative.\n" + section, True),
        ("no-closing-separator", "# T\n\n**Document Title:** T\\\n\n" + DISCLAIMER + "\n", True),
        ("empty-after-metadata", meta, True),
        # A fenced example of the disclaimer earlier does not satisfy it (must be
        # real body content after the metadata run).
        ("fenced-disclaimer-only", "# T\n\n**Document Title:** T\\\n```\n" + DISCLAIMER + "\n```\n---\n\n" + section, True),
        # F1: an INDENTED disclaimer is a Markdown code block, not a blockquote, so
        # it does not satisfy the requirement (rstrip-only comparison).
        ("indented-code-disclaimer", meta + "    " + DISCLAIMER + "\n" + section, True),
        # F2: a fenced block BEFORE the disclaimer means the disclaimer is not the
        # first body content.
        ("fence-before-disclaimer", meta + "```\nexample\n```\n\n" + DISCLAIMER + "\n" + section, True),
        # F3: ordinary body bold text plus a later `---` must NOT forge the
        # metadata-close anchor (no real leading metadata field run).
        ("forged-metadata-close", "# T\n\nSome **bold** body text.\n\n---\n\n" + DISCLAIMER + "\n" + section, True),
        # A blank line between the field run and the closing `---` is tolerated.
        ("blank-before-separator", "# T\n\n**Document Title:** T\\\n\n---\n\n" + DISCLAIMER + "\n" + section, False),
    ]
    failed = 0
    for name, text, expect in cases:
        got = disclaimer_finding(text, name) is not None
        if got != expect:
            failed += 1
            print(
                f"SELF-TEST FAIL [{name}]: expected finding={expect}, got={got} "
                f"(result={disclaimer_finding(text, name)!r})",
                file=sys.stderr,
            )
    if failed:
        print(f"self-test: {failed} case(s) FAILED", file=sys.stderr)
        return 1
    print(f"self-test: all {len(cases)} disclaimer cases passed.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify every executive-narrative page carries the verbatim "
        "authority disclaimer in the required position."
    )
    parser.add_argument("--self-test", action="store_true", help="Run the self-test and exit.")
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return _self_test()

    findings: list[str] = []
    pages = discover()
    for path, rel in pages:
        findings.extend(check_file(path, rel))

    if findings:
        for f in findings:
            print(f"  {f}", file=sys.stderr)
        print(
            f"FAIL: {len(findings)} narrative page(s) missing the verbatim authority "
            f"disclaimer in position.",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {len(pages)} narrative page(s) checked; each carries the verbatim "
        f"authority disclaimer as the first body content after the metadata block."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
