#!/usr/bin/env python3
"""Owner and Approving Authority role audit (grc gate 8): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_roles.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-roles``, enforcing the pack's ``role-authority`` clause); this thin
wrapper keeps the house ``python3 tools/lint-roles.py`` shape (gate 35 parses exactly that) and
supplies the grc-local configuration the pack engine deliberately does not carry: the markdown
scope selector (``iter_markdown_files``, kept here so the scan-scope regression's ALLOW map
observes it unmoved), the default scan roots, the role-authority register path and its parse
(``load_known_roles``), the grc allow-list (``EXTRA_KNOWN_ROLES``), the register-prerequisite
failure (exit 2), and the ``--root`` override the gate-36 regression suite uses for synthetic-fixture
isolation. These wrapper bytes are HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own
them.

The role authority register (``governance/register-role-authority.md``) is the source of truth for
organizational roles; every Owner and Approving Authority value should resolve to a role defined
there or to an ``EXTRA_KNOWN_ROLES`` entry (cross-functional bodies, named forums, external
authorities that are not formal organizational roles).

Usage:
    python3 tools/lint-roles.py
    python3 tools/lint-roles.py path1 path2 ...

Exit codes:
    0   no findings.
    1   one or more undefined-role findings.
    2   the role authority register itself could not be parsed (a prerequisite failure; the linter
        cannot run without it).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS, iter_scan_roots_markdown

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_REGISTER = REPO_ROOT / "governance" / "register-role-authority.md"

# Derive the pack tools/ from this file's location, independent of the (test-rebound) REPO_ROOT.
PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Roles that are intentionally not in the role authority register but are
# acceptable Owner values for cross-functional bodies, named forums, or
# external named entities the library legitimately references.
#
# Every entry here must appear as an Owner or Approving Authority in at
# least one document. Phase 23.63 removed three entries that did not
# satisfy this criterion: `Privacy Maintainer` and `Risk Maintainer`
# had zero corpus occurrences (the bare role names were never used as
# Owner/Approving Authority), and `Supplier Risk Maintainer` is in fact
# defined in governance/register-role-authority.md; keeping a copy
# here was redundant and contradicted the set's purpose.
# The five maintainer / library-meta roles formerly listed here (Governance
# Library Maintainer, Compliance Maintainer, Security Architecture Maintainer,
# GRC Programme Manager, Information Security Maintainer) were promoted to rows
# in governance/register-role-authority.md so the register is the single source
# of truth for them; they no longer need allow-list entries.
# AI Governance Maintainer was historically a single role; it has
# since been split into AI Governance Approver, AI Data Steward,
# and AI System Inventory Keeper. Those three are now in
# governance/register-role-authority.md and don't need entries
# here. The composite role no longer appears anywhere in the
# corpus.
# The set is intentionally empty: it remains as the mechanism for any future
# cross-functional body, named forum, or external named entity that is a
# legitimate Owner / Approving Authority value but is not a formal
# organizational role belonging in the register.
EXTRA_KNOWN_ROLES: set[str] = set()

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
    "guardrails",
]


def load_known_roles() -> set[str]:
    """Parse the role authority register for the set of known roles."""
    if not ROLE_REGISTER.exists():
        print(f"WARNING: role register not found at {ROLE_REGISTER}", file=sys.stderr)
        return set()

    text = ROLE_REGISTER.read_text(encoding="utf-8")
    roles: set[str] = set()
    # The register has a table where the first column is the role name.
    # Match lines that look like:  | <Role Name> | <Responsibility ...> | <Examples ...> |
    table_row = re.compile(r"^\|\s+([A-Z][^|]*?)\s+\|\s+[^|]+\|\s+[^|]+\|\s*$")
    for line in text.splitlines():
        m = table_row.match(line)
        if m:
            name = m.group(1).strip()
            # Skip the header row
            if name in ("Role", "---"):
                continue
            roles.add(name)

    roles |= EXTRA_KNOWN_ROLES
    return roles


def iter_markdown_files(paths: list[str]) -> list[Path]:
    return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_roles  # the pack-owned engine (source of record)
    return gate_lint_roles


def main(argv: list[str]) -> int:
    global REPO_ROOT, ROLE_REGISTER
    parser = argparse.ArgumentParser(description="Verify Owner and Approving Authority roles are defined.")
    parser.add_argument("paths", nargs="*", default=None)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root the role-authority register is "
             "read from (used by the gate-36 regression test suite for "
             "synthetic-fixture isolation testing). Default: the actual "
             "repository root derived from this file's location.",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        REPO_ROOT = args.root.resolve()
        ROLE_REGISTER = REPO_ROOT / "governance" / "register-role-authority.md"

    known = load_known_roles()
    if not known:
        print("FAIL: could not load role authority register.")
        return 2

    paths = args.paths or DEFAULT_PATHS
    files = iter_markdown_files(paths)
    return _engine().run(files, known=known, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
