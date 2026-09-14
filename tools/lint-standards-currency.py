#!/usr/bin/env python3
"""Standards-currency audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_standards_currency.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-standards-currency``, enforcing the pack's ``standards-currency``
clause); this thin wrapper keeps the house ``python3 tools/lint-standards-currency.py`` shape (gate 35
parses exactly that) and supplies the grc-local configuration the pack engine deliberately does not
carry: the AIQT bootstrap, the repo root, the markdown scope selector, the default scan roots, the
target-selection exemptions, and the grc canonical-citations REGISTER (it parses the grc register
format via ``parse_canonical_register``, honours the ``--root`` fixture-isolation override the
gate-36 regression uses, and passes the parsed entries -- compiled by the engine -- plus counts in).
The register missing / parses-no-rows error paths (exit 2 / exit 1) are the wrapper's. These wrapper
bytes are HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them; ``iter_files`` stays
here so the scan-scope regression's ALLOW map observes it unmoved.

Usage:
    python3 tools/lint-standards-currency.py
    python3 tools/lint-standards-currency.py --paths governance ai

Exit codes are the engine's: 0 clean; 1 finding(s) (plus the wrapper's 2 = register missing).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"
CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Files exempt from the linter (typically CHANGELOG-style records and
# discussions of the defect itself).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "governance/register-canonical-citations.md",
}

EXEMPT_DIRECTORY_PREFIXES = (
    "tools/",
    "docs/",
)

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
    "guardrails",
]


def parse_canonical_register() -> list[dict[str, object]]:
    """Parse the canonical register's tables into a list of standard entries.

    Each entry is a dict with keys:
        id          (str)    Standard identifier as it appears in the table
        current     (str)    Current version string
        superseded  (list)   Strings the linter should flag if seen with this id
    """
    if not CANONICAL_REGISTER.exists():
        print(
            f"ERROR: canonical citations register not found at {CANONICAL_REGISTER}",
            file=sys.stderr,
        )
        return []

    text = CANONICAL_REGISTER.read_text(encoding="utf-8")
    entries: list[dict[str, object]] = []

    # Each standard-table row is of the form:
    # | <id> | <current> | <date> | <topic> | <superseded comma-list> |
    # As of register v1.5.7 the five-column tables also carry two trailing
    # columns (| <upstream check location> | <last verified (UTC)> |) added by
    # the version-currency cadence. We extract id (1), current (2), and
    # superseded (5); the optional non-capturing trailing group consumes those
    # two new columns when present. The optional group matches EITHER zero or
    # EXACTLY two trailing columns, so a 5-column row (the legacy form, still
    # used by the regression fixtures) and a 7-column row (the current register)
    # both match, while the 6-/8-column AI-security-tooling table (which is not a
    # standards-currency source and was never parsed here) is still excluded.
    row_re = re.compile(
        r"^\|\s+([^|]+?)\s+\|\s+([^|]+?)\s+\|\s+[^|]+?\s+\|\s+[^|]+?\s+\|\s+([^|]+?)\s+\|"
        r"(?:\s+[^|]+?\s+\|\s+[^|]+?\s+\|)?$"
    )

    for raw in text.splitlines():
        m = row_re.match(raw)
        if not m:
            continue
        std_id = m.group(1).strip()
        current = m.group(2).strip()
        superseded_raw = m.group(3).strip()

        # Skip header rows
        if std_id.lower() in {"standard id", "---", "--- ", " --- "}:
            continue
        if std_id.startswith("---"):
            continue

        # Parse superseded
        if superseded_raw in {"\u2014", "-", ""}:
            superseded: list[str] = []
        else:
            superseded = [s.strip() for s in superseded_raw.split(",") if s.strip()]

        entries.append(
            {
                "id": std_id,
                "current": current,
                "superseded": superseded,
            }
        )

    return entries


def iter_files(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for f in iter_scan_roots_markdown(paths, repo_root=REPO_ROOT):
        rel = f.relative_to(REPO_ROOT).as_posix()
        if rel in EXEMPT_FILES:
            continue
        if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
            continue
        out.append(f)
    return out


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_standards_currency  # the pack-owned engine (source of record)
    return gate_lint_standards_currency


def main() -> int:
    global REPO_ROOT, CANONICAL_REGISTER
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths",
        nargs="+",
        default=DEFAULT_PATHS,
        help="Paths to scan (default: all active library directories and root files)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root the canonical-citations register "
             "is read from (used by the gate-36 regression test suite "
             "for synthetic-fixture isolation testing). Default: the "
             "actual repository root derived from this file's location.",
    )
    args = parser.parse_args()
    if args.root is not None:
        REPO_ROOT = args.root.resolve()
        CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

    entries = parse_canonical_register()
    if not entries:
        # Distinguish "register file missing" (exit 2; environmental
        # failure) from "register parses no rows" (exit 1; treat as a
        # gate failure rather than a silent no-op, because a register
        # that parses zero rows indicates either a parsing bug or an
        # accidental wipe, both of which should fail CI).
        register = REPO_ROOT / "governance" / "register-canonical-citations.md"
        if not register.exists():
            print(
                f"ERROR: canonical citations register not found at {register}",
                file=sys.stderr,
            )
            return 2
        print(
            "ERROR: canonical citations register parsed no entries. "
            "The register exists but no rows were extracted: likely a "
            "parsing bug or an accidental wipe. Linter cannot verify "
            "standards currency in this state.",
            file=sys.stderr,
        )
        return 1
    engine = _engine()
    compiled = engine.compile_entry_patterns(entries)
    return engine.run(iter_files(args.paths), compiled, len(entries), repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main())
