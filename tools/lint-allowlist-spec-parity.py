#!/usr/bin/env python3
"""Gate 101: external-link allow-list and citation-verification section 7.1 parity.

Two surfaces list the publishers whose domains the library may link to: the
external-link gate's ``ALLOW_LIST`` in ``tools/lint-external-link-domains.py``
(gate 24) and the publisher allow-list in section 7.1 of
``governance/specification-citation-verification.md``. They drifted apart before
(3b30 reconciled them by hand); this gate keeps them together. Section 7.1's
source of record is its fenced ``json citation-publishers`` block (parsed strictly by
``tools/citation_publishers.py``); its table is generated from the block (gate 102),
so this gate never parses a Markdown table (3b31b redesign, maintainer ruling
2026-09-24: nine QA rounds showed hand-parsing a GFM table is an open-ended class).

Clause. Forward: every ``ALLOW_LIST`` entry is either covered by a section 7.1
domain under gate 24's own suffix matcher, imported from its pack engine rather than
re-implemented (the entry equals a 7.1 domain or is a subdomain of one), or carries a same-line trailing marker comment naming its
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
the section 7.1 block must satisfy every rule of ``tools/citation_publishers.py``
(exactly one block inside section 7.1, strict JSON, exact schema, canonical and
unique domains); and at least MIN_SPEC_DOMAINS domains must be declared, so a
valid but shrunken block cannot silently shrink the checked set.

Residue, stated: a marker proves a classification was asserted, not that it is
honest; a ``non-publisher`` marker on a genuine publisher passes mechanically,
and that judgement stays with review and the periodic section 7 reconciliation.

Exit codes: 0 in parity; 1 findings; 2 input error.
"""

from __future__ import annotations

import ast
import io
import re
import sys
import tokenize
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import citation_publishers  # noqa: E402  # section 7.1 source of record (shared with gate 102)
ALLOW_SRC = REPO_ROOT / "tools" / "lint-external-link-domains.py"
SPEC = REPO_ROOT / "governance" / "specification-citation-verification.md"
MIN_SPEC_DOMAINS = 50
MARKER_RE = re.compile(r"#\s*(non-publisher|pending-publisher):\s*(\S.*)$")
# Methods that only read a set; any other attribute use on ALLOW_LIST could
# change it after the literal and is rejected.
READ_ONLY_ATTRS = {"copy", "issubset", "issuperset", "isdisjoint", "union",
                   "intersection", "difference", "symmetric_difference"}


class InputError(Exception):
    pass


def _comments(src: str) -> dict[int, str]:
    """Line number -> comment text, from the tokenizer (so no string can fake one)."""
    out: dict[int, str] = {}
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            out[tok.start[0]] = tok.string
    return out


def _check_uses(tree: ast.AST, definition: ast.Assign) -> None:
    """Accept only an allow-list of uses of the name; reject every other form.

    Permitted: the single definition target; a plain load passed directly as a
    positional or keyword argument to a call; a plain load as the receiver of a
    read-only method call. Every other occurrence of the name in any AST field
    (an alias assignment, a subscript or slice store, a match-pattern capture, an
    import alias, a parameter, an except target, global or nonlocal) is an input
    error, since the runtime set could then differ from the literal. Residue: a
    function receiving the set as an argument could still mutate it; the one such
    call today is gate 24's own scan, which only reads it.
    """
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    for node in ast.walk(tree):
        mentions = False
        for _field, value in ast.iter_fields(node):
            if value == "ALLOW_LIST" or (isinstance(value, list) and "ALLOW_LIST" in value):
                mentions = True
        if not mentions:
            continue
        line = getattr(node, "lineno", "?")
        if isinstance(node, ast.Name):
            if node in definition.targets:
                continue
            parent = parents.get(node)
            if isinstance(node.ctx, ast.Load):
                if isinstance(parent, ast.Call) and node in parent.args:
                    continue
                if isinstance(parent, ast.keyword):
                    continue
                if isinstance(parent, ast.Attribute) and parent.attr in READ_ONLY_ATTRS \
                        and isinstance(parents.get(parent), ast.Call) \
                        and parents[parent].func is parent:
                    continue
        raise InputError(
            f"unsupported use of ALLOW_LIST at line {line} ({type(node).__name__}); only the "
            f"single literal definition, a direct call argument, or a read-only method call is allowed")


def allow_entries(src: str) -> list[tuple[str, int, str | None]]:
    """(domain, line, marker kind or None) for each ALLOW_LIST literal element.

    Exactly one module-level ``ALLOW_LIST = <literal>`` is supported. Any other
    binding, augmented assignment, deletion or non-read-only attribute use of the
    name is an input error, because the runtime set would then differ from the
    literal this gate reads.
    """
    tree = ast.parse(src)
    defs = [n for n in tree.body if isinstance(n, ast.Assign)
            and any(getattr(t, "id", None) == "ALLOW_LIST" for t in n.targets)]
    if not defs:
        raise InputError("ALLOW_LIST assignment not found")
    if len(defs) > 1:
        raise InputError(f"ALLOW_LIST is assigned {len(defs)} times at module level")
    definition = defs[0]
    if len(definition.targets) != 1 or not isinstance(definition.targets[0], ast.Name):
        raise InputError(
            f"ALLOW_LIST must be the only target of its assignment (line {definition.lineno}); "
            f"a chained assignment would create an unchecked alias")
    _check_uses(tree, definition)
    if not isinstance(definition.value, (ast.Set, ast.List, ast.Tuple)):
        raise InputError("ALLOW_LIST is not a literal set, list or tuple")
    comments = _comments(src)
    out: list[tuple[str, int, str | None]] = []
    for elt in definition.value.elts:
        if not (isinstance(elt, ast.Constant) and isinstance(elt.value, str)):
            raise InputError(f"non-string ALLOW_LIST element at line {elt.lineno}")
        m = MARKER_RE.search(comments.get(elt.lineno, ""))
        out.append((elt.value, elt.lineno, m.group(1) if m else None))
    if not out:
        raise InputError("ALLOW_LIST is empty")
    return out


def spec_domains(text: str) -> set[str]:
    """Every domain section 7.1's ``json citation-publishers`` block declares."""
    try:
        domains = citation_publishers.domains(text)
    except citation_publishers.InputError as exc:
        raise InputError(f"section 7.1 source of record: {exc}") from None
    if len(domains) < MIN_SPEC_DOMAINS:
        raise InputError(
            f"only {len(domains)} section 7.1 domains declared (floor {MIN_SPEC_DOMAINS}); "
            "was the publisher block truncated?")
    return domains


PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"


def _link_engine():
    """Gate 24's pack-owned engine, the single owner of allow-list suffix matching (3b52c)."""
    import aiqt_bootstrap  # noqa: F401  # the AIQT generic core the engine imports, as gate 24's wrapper does
    if str(PACK_TOOLS) not in sys.path:
        sys.path.insert(0, str(PACK_TOOLS))
    import gate_lint_external_link_domains
    return gate_lint_external_link_domains


def covered(entry: str, domains: set[str]) -> bool:
    """Whether `entry` is admitted by `domains` under gate 24's OWN matcher (imported, never
    re-implemented, so the two gates cannot disagree on what a suffix match is)."""
    return _link_engine().is_allowed(entry, allow_list=domains)


def check(allow: list[tuple[str, int, str | None]], domains: set[str]) -> list[str]:
    findings: list[str] = []
    for entry, line, marker in allow:
        if entry != entry.strip().lower().rstrip(".") or not entry.strip():
            findings.append(
                f"L{line} [allowlist-spec-parity] {entry!r}: not a canonical lowercase host "
                f"(gate 24 lowercases the URL host, not the allow-list)")
            continue
        if marker is not None and covered(entry, domains):
            findings.append(
                f"L{line} [allowlist-spec-parity] {entry}: marked {marker} but covered by "
                f"section 7.1; remove the stale marker")
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
