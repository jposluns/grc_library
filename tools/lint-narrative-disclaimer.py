#!/usr/bin/env python3
"""Executive-narrative authority-disclaimer audit - grc wrapper over the pack engine.

Verify every executive-narrative page carries the verbatim authority disclaimer as the
first body content after the metadata block.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(disclaimer_finding, check_file) is the source of record in the pack engine
(.corpus-management/tools/gate_lint_narrative_disclaimer.py); it is content-free and
takes the required disclaimer via configure(). This wrapper supplies the grc disclaimer
+ entry-point exemption + the narrative scan scope (discover), configures the engine,
and keeps the self-test, main, module-global shims (check_file / disclaimer_finding),
and the exit codes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

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


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_narrative_disclaimer  # the pack-owned engine (source of record)
    return gate_lint_narrative_disclaimer


# Configure the engine ONCE with the grc required disclaimer text.
_engine().configure(DISCLAIMER)


def disclaimer_finding(text: str, rel: str) -> str | None:
    """Shim -> engine (engine already configured); kept module-global for the self-test."""
    return _engine().disclaimer_finding(text, rel)


def check_file(path: Path, rel: str) -> list[str]:
    """Shim -> engine (engine already configured); kept module-global for parity/reuse."""
    return _engine().check_file(path, rel)


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
