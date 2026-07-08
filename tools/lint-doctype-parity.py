#!/usr/bin/env python3
"""Gate 67: Document-Type enumeration parity audit.

The allowed Document-Type set is defined canonically in
[`tools/lint-metadata.py`](lint-metadata.py) as `ALLOWED_TYPES` (the type names)
and `TYPE_TO_PREFIX` (the filename prefixes). That same set is RE-ENUMERATED
across many other surfaces, and nothing checked that the enumerations agree:

  - a second linter's set (`tools/lint-filename-title-alignment.py` `DOCTYPES`);
  - the master-spec section 4.3 Type-to-prefix table;
  - the ingestion spec's allowed-type list;
  - the AI-ingestion instruction's type list + prefixes;
  - the two governance `Document hierarchy` tables (the charter and the
    document-architecture framework);
  - the README `## Document types` table;
  - the CONTRIBUTING filename-prefix list.

When a new type was added (the #711 "Principle" case), it was registered in
`lint-metadata.py` but silently omitted from those surfaces, and 66/66 stayed
green because no gate cross-checked them; #711 shipped the gap and #712 fixed it.
This gate closes that gate-blind class: every canonical type name (as a table
cell / list item) and every canonical prefix must be present on the surface that
enumerates it, and the second linter's set must equal the canonical set exactly.

The gate treats `lint-metadata.py` as the single source of truth; a surface that
diverges is the failure, and the fix is to update the surface, never the gate.

Known limitation (tracked, TODO 3.23): the name-cell and prefix checks scan each
surface's WHOLE file, not the specific doctype table/list region. This is robust
against a coincidental prose mention, and it catches the target class (a newly
added type absent everywhere), but it has a latent false-pass vector: a canonical
type word appearing as a cell in an UNRELATED table on a name-surface, or a prefix
appearing in a document-link filename elsewhere on a prefix-surface, could satisfy
the presence check even if the actual doctype table omitted the type. The corpus
is verified clear of that condition at build time (no type appears as a cell in
more than one location on any name-surface; each prefix appears once per
prefix-surface). Region-scoping each check to its table/list block is the queued
hardening.

Exit 0 clean, exit 1 on any parity break; prints every break with its surface and
the missing token(s).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"


def _load_module(path: Path):
    """Load a hyphenated tools module by file path (no import side effects:
    the module guards main under __name__ == '__main__')."""
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def canonical_sets():
    """Return (names, prefixes) from lint-metadata.py, the source of truth."""
    meta = _load_module(TOOLS / "lint-metadata.py")
    names = set(meta.ALLOWED_TYPES)
    prefixes = set()
    for plist in meta.TYPE_TO_PREFIX.values():
        prefixes.update(plist)
    return names, prefixes


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def name_is_cell(text: str, name: str) -> bool:
    """True if `name` appears as a bounded markdown table cell `| name |` or a
    plain list item `- name`. Both forms are robust against a coincidental
    prose mention of a common type word (Guide, Standard, Plan, ...)."""
    if re.search(r"\|\s*" + re.escape(name) + r"\s*\|", text):
        return True
    if re.search(r"^-\s+" + re.escape(name) + r"\s*$", text, re.M):
        return True
    return False


def main() -> int:
    names, prefixes = canonical_sets()
    failures: list[str] = []

    # Check 1: the second linter's DOCTYPES set must equal the canonical names,
    # compared case-insensitively (DOCTYPES is lowercase; ALLOWED_TYPES is CamelCase).
    fta = _load_module(TOOLS / "lint-filename-title-alignment.py")
    canon_lower = {n.lower() for n in names}
    doctypes = set(fta.DOCTYPES)
    missing = canon_lower - doctypes
    extra = doctypes - canon_lower
    if missing:
        failures.append(
            "tools/lint-filename-title-alignment.py DOCTYPES is missing "
            f"canonical type(s): {sorted(missing)}"
        )
    if extra:
        failures.append(
            "tools/lint-filename-title-alignment.py DOCTYPES has type(s) not in "
            f"lint-metadata.py ALLOWED_TYPES: {sorted(extra)}"
        )

    # Check 2: the required-sections linter's enforced keys must all be valid
    # canonical types (a stale/bogus key would silence or misapply the section
    # rule). Types absent from its map are not-enforced BY DESIGN, so absence is
    # not a failure; an invalid key is.
    rs = _load_module(TOOLS / "lint-required-sections.py")
    rs_keys = set(getattr(rs, "REQUIRED_SECTIONS", {}).keys())
    rs_bad = rs_keys - names
    if rs_bad:
        failures.append(
            "tools/lint-required-sections.py REQUIRED_SECTIONS has key(s) not in "
            f"lint-metadata.py ALLOWED_TYPES: {sorted(rs_bad)}"
        )

    # Check 3: name-cell surfaces. Every canonical type name must appear as a
    # table cell or list item in each of these enumerations.
    name_surfaces = {
        "README.md": "README `## Document types` table",
        "specification-ingestion.md": "the ingestion spec allowed-type list",
        "governance/charter-governance-library.md": "the charter `Document hierarchy` table",
        "governance/framework-document-architecture-and-interrelationship.md":
            "the document-architecture `Document hierarchy` table",
    }
    for rel, label in name_surfaces.items():
        text = read(rel)
        absent = sorted(n for n in names if not name_is_cell(text, n))
        if absent:
            failures.append(f"{rel} ({label}) omits type name(s) as a cell/item: {absent}")

    # Check 4: prefix-presence surfaces. Every canonical prefix must appear in
    # each of these enumerations (prefixes are distinctive; substring presence
    # is a robust, low-false-positive signal).
    prefix_surfaces = {
        "specification-master-project.md": "the master-spec section 4.3 Type-to-prefix table",
        "instruction-ai-document-ingestion.md": "the AI-ingestion instruction",
        "CONTRIBUTING.md": "the CONTRIBUTING filename-prefix list",
    }
    for rel, label in prefix_surfaces.items():
        text = read(rel)
        absent = sorted(p for p in prefixes if p not in text)
        if absent:
            failures.append(f"{rel} ({label}) omits filename prefix(es): {absent}")

    if failures:
        print("FAIL: Document-Type enumeration parity break(s):")
        for f in failures:
            print(f"  - {f}")
        print(
            f"\nCanonical set (tools/lint-metadata.py): {len(names)} type(s), "
            f"{len(prefixes)} prefix(es). Fix the diverging surface, never this gate."
        )
        return 1

    print(
        f"OK: Document-Type enumeration parity holds across all surfaces "
        f"({len(names)} type names, {len(prefixes)} prefixes; canonical source "
        f"tools/lint-metadata.py)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
