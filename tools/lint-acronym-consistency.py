#!/usr/bin/env python3
"""Verify acronym definitions across the library against the glossary.

The library uses [`governance/register-glossary.md`](register-glossary.md) as the
single source of truth for acronym expansions. Inline definitions of the
form "Expansion (ACRONYM)" must match what the glossary records.

This linter:
- Parses the glossary register into an acronym -> expansion map.
- Walks every artefact document looking for inline acronym definitions
  of the form "Expansion (ACRONYM)" where ACRONYM is 2-6 characters of
  uppercase letters, digits, or hyphens (the regex permits hyphenated
  acronyms such as ``NIST-AI`` and digit-initial numeronyms such as
  ``3PL`` / ``2FA``; slash-separated forms such as ``ISO/IEC`` are not
  detected as inline definitions, but they are recognized by the
  glossary-row regex when listed in the glossary).
- Flags definitions whose expansion phrase materially diverges from
  the glossary.

The linter is conservative: it flags only cases where the inline
expansion's main content words do not overlap with the glossary's
expansion content words. Stylistic differences (a/the/of) are tolerated.

The inline-definition regex deliberately requires a Title-Case
expansion phrase (each expansion word capitalized). This is a
false-positive control, not an oversight: it anchors the phrase
boundary at the definition's first capitalized word. A lowercase-
tolerant expansion pattern (to catch canonical-order running-prose
definitions such as "financial market infrastructure (FMI)") was
assessed against the full corpus and rejected: a lowercase-starting
run over-captures incidental leading context words ("and presented to
the Enterprise Risk Committee (ERC)"), so the content-overlap check
would either false-positive on those over-captures or, if it flagged
only zero-overlap, false-positive on incidental parentheticals ("...
candidates list (STP)"); an initialism anchor is unreliable for
numeronyms (3PL / 2FA) and stopword-dropping acronyms (CAPA). Such
running-prose definitions are therefore intentionally not checked.

Acronyms not in the glossary are not flagged by this linter (a separate
"glossary coverage" linter would catch those; this one focuses on
expansion consistency).

Usage:
    python3 tools/lint-acronym-consistency.py
    python3 tools/lint-acronym-consistency.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more acronym expansion inconsistencies present
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import DEFAULT_EXEMPT_DIRS, is_narrative_root, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

GLOSSARY = REPO_ROOT / "governance" / "register-glossary.md"

EXEMPT_FILES = {
    # The glossary itself defines acronym ↔ expansion pairs.
    "register-glossary.md",
    # The CHANGELOG describes the patterns and is allowed to use them freely.
    "CHANGELOG.md",
    # Generated bibliography (tools/build-reference-manifest.py): its cells are
    # verbatim source titles/issuers, not authored prose (1.19.7 (closing PR #1007)).
    "reference-acquisition-manifest.md",
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_acronym_consistency  # the pack-owned engine (source of record)
    return gate_lint_acronym_consistency


def parse_glossary() -> dict[str, set[str]]:
    """Thin shim delegating to the pack engine, supplying the grc glossary path.

    Kept in the wrapper as a module-global because the scan-scope regression test
    patches ``mod.parse_glossary``; the parsing logic lives in the pack engine. The
    grc glossary-register PATH (``GLOSSARY``, rebindable via ``main --root``) is the
    wrapper's to supply.
    """
    return _engine().parse_glossary(GLOSSARY)


def scan(path: Path, glossary: dict[str, set[str]]) -> list[tuple[int, str, str, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression test
    patches ``mod.scan`` and runs ``main``; the check (INLINE_DEF_RE, STOPWORDS,
    the overlap logic) lives in the pack engine.
    """
    return _engine().scan(path, glossary)


def main(argv: list[str]) -> int:
    global GLOSSARY
    parser = argparse.ArgumentParser(
        description="Verify acronym expansion consistency against the glossary."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root the glossary register is read "
             "from (used by the gate-36 regression test suite for "
             "synthetic-fixture isolation testing). Default: the "
             "actual repository root derived from this file's location.",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        GLOSSARY = args.root.resolve() / "governance" / "register-glossary.md"
    glossary = parse_glossary()
    if not glossary:
        # Distinguish "glossary file missing" (environmental failure;
        # exit 2) from "glossary parses no rows" (parsing bug or
        # accidental wipe; exit 1). Either way, do NOT silently pass.
        if not GLOSSARY.exists():
            print(
                f"ERROR: glossary register not found at {GLOSSARY}",
                file=sys.stderr,
            )
            return 2
        print(
            "ERROR: glossary register parsed no entries. "
            "The register exists but no rows were extracted: likely a "
            "parsing bug or an accidental wipe. Linter cannot verify "
            "acronym consistency in this state.",
            file=sys.stderr,
        )
        return 1
    targets = [
        t
        for t in iter_markdown_targets(
            args.paths,
            exempt_dirs=DEFAULT_EXEMPT_DIRS,
            exempt_files=EXEMPT_FILES,
        )
        if not is_narrative_root(t)  # house-style gate: root executive/ excluded (P-1.25)
    ]
    grouped: dict[Path, list[tuple[int, str, str, str]]] = {}
    for t in targets:
        findings = scan(t, glossary)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all inline acronym expansions match the glossary (scanned {len(targets)} files; {len(glossary)} glossary entries).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, acr, phrase, msg in findings:
            print(f"  L{lineno} [acronym-inconsistency] {acr}: {phrase!r} - {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} acronym-consistency finding(s) across {len(grouped)} file(s).")
    print(
        "Inline acronym expansions should be consistent with the glossary "
        "(governance/register-glossary.md). Either match the glossary expansion or "
        "update the glossary if the inline definition is more current."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
