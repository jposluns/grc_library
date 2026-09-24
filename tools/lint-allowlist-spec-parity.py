#!/usr/bin/env python3
"""Gate 101: external-link allow-list and citation-verification section 7.1 parity.

Two surfaces list the publishers whose domains the library may link to: the
external-link gate's ``ALLOW_LIST`` in ``tools/lint-external-link-domains.py``
(gate 24) and the publisher table in section 7.1 of
``governance/specification-citation-verification.md``. They drifted apart before
(3b30 reconciled them by hand); this gate keeps them together.

Clause. Forward: every ``ALLOW_LIST`` entry is either covered by a section 7.1
domain under gate 24's own suffix semantics (the entry equals a 7.1 domain or is
a subdomain of one), or carries a same-line trailing marker comment naming its
classification with a non-empty reason:

    "linkedin.com",  # non-publisher: maintainer profile
    "cisecurity.org",  # pending-publisher: CIS register entry (3b33)

``non-publisher`` marks a host that is not a citation publisher (code hosting,
identifiers, format conventions, vendors and tools, the project's own sites);
``pending-publisher`` marks a publisher whose Canonical Citations Register entry,
and therefore its 7.1 row, is still to come. A marker applies to every entry on
its own physical line only; a comment on a preceding line never marks an entry,
so an entry appended to a commented group is still checked. Reverse: every
section 7.1 domain is admitted by the allow-list under the same matcher.

Fail-closed input checks: the ALLOW_LIST literal must be found and non-empty;
the section 7.1 table must be found; every 7.1 data row must carry at least one
code-span domain in its domain cell; and at least MIN_SPEC_DOMAINS domains must
parse, so a reflowed table cannot silently shrink the checked set.

Residue, stated: a marker proves a classification was asserted, not that it is
honest; a ``non-publisher`` marker on a genuine publisher passes mechanically,
and that judgement stays with review and the periodic section 7 reconciliation.

Exit codes: 0 in parity; 1 findings; 2 input error.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOW_SRC = REPO_ROOT / "tools" / "lint-external-link-domains.py"
SPEC = REPO_ROOT / "governance" / "specification-citation-verification.md"
MIN_SPEC_DOMAINS = 50
MARKER_RE = re.compile(r"#\s*(non-publisher|pending-publisher):\s*(\S.*)$")


class InputError(Exception):
    pass


def allow_entries(src: str) -> list[tuple[str, int, str | None]]:
    """(domain, line, marker kind or None) for each ALLOW_LIST literal element."""
    tree = ast.parse(src)
    lines = src.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "ALLOW_LIST" for t in node.targets
        ):
            if not isinstance(node.value, (ast.Set, ast.List, ast.Tuple)):
                raise InputError("ALLOW_LIST is not a literal set, list or tuple")
            out: list[tuple[str, int, str | None]] = []
            for elt in node.value.elts:
                if not (isinstance(elt, ast.Constant) and isinstance(elt.value, str)):
                    raise InputError(f"non-string ALLOW_LIST element at line {elt.lineno}")
                m = MARKER_RE.search(_comment(lines[elt.lineno - 1]))
                out.append((elt.value.lower(), elt.lineno, m.group(1) if m else None))
            if not out:
                raise InputError("ALLOW_LIST is empty")
            return out
    raise InputError("ALLOW_LIST assignment not found")


def _comment(line: str) -> str:
    """The trailing comment of a source line, ignoring '#' inside string literals."""
    in_str: str | None = None
    for i, ch in enumerate(line):
        if in_str:
            if ch == in_str:
                in_str = None
        elif ch in "\"'":
            in_str = ch
        elif ch == "#":
            return line[i:]
    return ""


def spec_domains(text: str) -> set[str]:
    """Code-span domains in the section 7.1 table's domain cell."""
    m = re.search(r"^### 7\.1 .*$", text, re.M)
    if not m:
        raise InputError("section 7.1 heading not found")
    end = re.search(r"^#{2,3} ", text[m.end():], re.M)
    section = text[m.end(): m.end() + end.start()] if end else text[m.end():]
    domains: set[str] = set()
    rows = 0
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "Publisher" or set(cells[0]) <= set("-: "):
            continue
        rows += 1
        found = re.findall(r"`([^`]+)`", cells[1] if len(cells) > 1 else "")
        if not found:
            raise InputError(f"section 7.1 row without a code-span domain: {line[:80]}")
        domains |= {d.lower() for d in found}
    if len(domains) < MIN_SPEC_DOMAINS:
        raise InputError(
            f"only {len(domains)} section 7.1 domains parsed from {rows} rows "
            f"(floor {MIN_SPEC_DOMAINS}); table format changed?")
    return domains


def covered(entry: str, domains: set[str]) -> bool:
    return any(entry == d or entry.endswith("." + d) for d in domains)


def check(allow: list[tuple[str, int, str | None]], domains: set[str]) -> list[str]:
    findings: list[str] = []
    for entry, line, marker in allow:
        if marker is None and not covered(entry, domains):
            findings.append(
                f"L{line} [allowlist-spec-parity] {entry}: not covered by a section 7.1 "
                f"domain and not marked non-publisher or pending-publisher")
    names = {e for e, _, _ in allow}
    for d in sorted(domains):
        if not covered(d, names):
            findings.append(
                f"[allowlist-spec-parity] section 7.1 domain {d} is not admitted by ALLOW_LIST")
    return findings


def main(argv: list[str]) -> int:
    try:
        allow = allow_entries(ALLOW_SRC.read_text(encoding="utf-8"))
        domains = spec_domains(SPEC.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, InputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    findings = check(allow, domains)
    for f in findings:
        print(f)
    if findings:
        print(f"FAIL: {len(findings)} allow-list / section 7.1 parity finding(s).")
        return 1
    marked = sum(1 for _, _, m in allow if m)
    print(f"OK: {len(allow)} allow-list entries ({marked} marked), "
          f"{len(domains)} section 7.1 domains, in parity.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
