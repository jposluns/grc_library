#!/usr/bin/env python3
"""Verify that every Owner/Approving Authority role used in metadata is defined.

The role authority register (`governance/register-role-authority.md`) is the
source of truth for organisational roles. Every Owner and Approving Authority
value in document metadata blocks should resolve to a role defined there. This
linter detects undefined-role usage that would otherwise create governance
ambiguity.

Usage:
    python3 tools/lint-roles.py
    python3 tools/lint-roles.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more undefined-role findings
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_REGISTER = REPO_ROOT / "governance" / "register-role-authority.md"

# Roles that are intentionally not in the role authority register but are
# acceptable Owner values for cross-functional bodies, named forums, or external
# named entities the library legitimately references.
EXTRA_KNOWN_ROLES = {
    "Governance Library Maintainer",  # repository maintainer role
    "Compliance Maintainer",          # alias used by some compliance docs
    "Privacy Maintainer",             # alias used by some privacy docs
    "Risk Maintainer",                # alias used by some risk docs
    "Security Architecture Maintainer",  # alias used by dev-security
    "Supplier Risk Maintainer",       # defined in Phase 12.10
    "GRC Programme Manager",          # referenced in continuous-improvement
    "Information Security Maintainer",  # security domain maintainer
    "AI Governance Maintainer (split into AI Governance Approver, AI Data Steward, AI System Inventory Keeper)",
}

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "sectors",
    "security",
    "supply-chain",
]

OWNER_PATTERN = re.compile(r"^\*\*Owner:\*\*\s+(.+?)\s*$", re.MULTILINE)
APPROVER_PATTERN = re.compile(r"^\*\*Approving Authority:\*\*\s+(.+?)\s*$", re.MULTILINE)


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
    files: list[Path] = []
    for p in paths:
        path = REPO_ROOT / p
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    return sorted(set(files))


def is_placeholder(value: str) -> bool:
    """Detect obvious template placeholders that shouldn't be linted."""
    if "<" in value or ">" in value:
        return True
    if value in ("Role Name", "Role Title", "<role title>", "<role name>"):
        return True
    if value.startswith("[") and value.endswith("]"):
        return True
    return False


def check_file(path: Path, known: set[str]) -> list[tuple[str, str]]:
    """Return list of (field, value) findings where the value is not a known role."""
    text = path.read_text(encoding="utf-8")
    findings: list[tuple[str, str]] = []

    def normalise(value: str) -> str:
        value = value.strip().rstrip()
        value = value.rstrip(" ").rstrip()
        # Strip CommonMark hard-line-break backslash if present.
        if value.endswith("\\"):
            value = value[:-1].rstrip()
        return value

    for m in OWNER_PATTERN.finditer(text):
        value = normalise(m.group(1))
        if is_placeholder(value):
            continue
        if value not in known:
            findings.append(("Owner", value))
    for m in APPROVER_PATTERN.finditer(text):
        value = normalise(m.group(1))
        if is_placeholder(value):
            continue
        if value not in known:
            findings.append(("Approving Authority", value))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Verify Owner and Approving Authority roles are defined.")
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv[1:])

    known = load_known_roles()
    if not known:
        print("FAIL: could not load role authority register.")
        return 2

    paths = args.paths or DEFAULT_PATHS
    files = iter_markdown_files(paths)

    grouped: dict[str, list[tuple[str, str]]] = {}
    undefined_values: dict[str, list[str]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        findings = check_file(f, known)
        if findings:
            grouped[rel] = findings
            for field, value in findings:
                undefined_values.setdefault(value, []).append(rel)
                total += 1

    if not grouped:
        print(f"OK: all roles in scanned files are defined (known: {len(known)}).")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for field, value in findings:
            print(f"  {field}: {value!r}")

    print(f"\nUndefined role values found:")
    for value, files_using in sorted(undefined_values.items()):
        print(f"  {value!r} used by {len(files_using)} file(s)")

    print(f"\nFAIL: {total} undefined-role usage(s) across {len(grouped)} file(s).")
    print("Add the role to governance/register-role-authority.md or to EXTRA_KNOWN_ROLES in this linter.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
