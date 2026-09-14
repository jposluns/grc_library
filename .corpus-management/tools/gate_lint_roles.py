#!/usr/bin/env python3
"""Owner and Approving Authority role audit (grc gate 8): pack-owned engine (source of record).

Every ``Owner`` and ``Approving Authority`` value in a document metadata block must resolve to a
known role: a role defined in the project's role-authority register, or an entry on the project's
allow-list of cross-functional bodies / named forums / external authorities that are not formal
organizational roles. A value that resolves to neither is an undefined-role finding (governance
ambiguity). An obvious template placeholder (angle-bracketed, ``[bracketed]``, or a literal
``Role Name`` / ``Role Title``) is deliberately NOT flagged.

Engine/wrapper split: this engine carries the PURE check (``OWNER_PATTERN`` / ``APPROVER_PATTERN``,
``is_placeholder``, ``check_file``) and a ``run`` that groups + reports against a supplied set of
known roles. The project wrapper (``tools/lint-roles.py``) supplies the grc scan scope (default
roots, the markdown selector), loads the known-role set from the grc role-authority register (plus
the grc allow-list), and handles the register-prerequisite failure and the ``--root`` override
before delegating, so this engine holds no register path, allow-list, or scan-scope policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more undefined-role findings; 2 (wrapper
only) the role-authority register itself could not be loaded.
"""

from __future__ import annotations

import re
from pathlib import Path

OWNER_PATTERN = re.compile(r"^\*\*Owner:\*\*\s+(.+?)\s*$", re.MULTILINE)
APPROVER_PATTERN = re.compile(r"^\*\*Approving Authority:\*\*\s+(.+?)\s*$", re.MULTILINE)


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


def run(files: list[Path], *, known: set[str], repo_root: Path) -> int:
    grouped: dict[str, list[tuple[str, str]]] = {}
    undefined_values: dict[str, list[str]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
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
