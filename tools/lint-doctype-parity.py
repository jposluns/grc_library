#!/usr/bin/env python3
"""Document-Type enumeration parity audit - grc wrapper over the pack-owned engine.

The allowed Document-Type set is defined canonically in
[`tools/lint-metadata.py`](lint-metadata.py) as `ALLOWED_TYPES` (the type names)
and `TYPE_TO_PREFIX` (the filename prefixes). That same set is RE-ENUMERATED
across many other surfaces, and this gate checks that the enumerations agree:

  - a second linter's doctype set (`tools/lint-filename-title-alignment.py`, profile-loaded
    and read via `_alignment_config()`);
  - the required-sections linter's enforced keys (must all be valid canonical types);
  - the README `## Document types` table, the ingestion spec allowed-type list, the two
    governance `Document hierarchy` tables (name surfaces);
  - the master-spec section 4.3 Type-to-prefix table, the AI-ingestion instruction, the
    CONTRIBUTING filename-prefix list (prefix surfaces).

The gate treats `lint-metadata.py` as the single source of truth; a surface that
diverges is the failure, and the fix is to update the surface, never the gate.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(`name_is_cell`, `doctype_region`, the four-category reconciliation `collect_findings`)
plus the generic cell/item regex live in the pack-owned engine
(.corpus-management/tools/gate_lint_doctype_parity.py, source of record). This wrapper
supplies ALL grc schema and vocabulary: the canonical source (`canonical_sets` loads
`lint-metadata.py`), the two cross-gate config reads (`_alignment_config()` /
`_sections_config()`), the 7 surface reads, the per-surface region anchors and labels,
and every finding-message TEMPLATE (so the engine hard-codes no grc word). The wrapper
re-exports `name_is_cell` / `doctype_region` and keeps `canonical_sets` +
`NAME_REGION_ANCHOR` / `PREFIX_REGION_ANCHOR` as module attributes so the importlib
direct-load regression (tests/test_linters.py DoctypeParityTests, which monkeypatches
`canonical_sets` and calls the helpers) keeps working; `main()` stays no-arg.

Region-scoping (#729): each name/prefix check is scoped to the surface's specific
doctype table/list block via the anchor maps below, closing the former out-of-region
false-pass vector. An absent anchor is itself a hard parity failure.

Exit 0 clean, exit 1 on any parity break.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"


def _load_module(path: Path):
    """Load a hyphenated tools module by file path (no import side effects:
    the module guards main under __name__ == '__main__')."""
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_doctype_parity  # the pack-owned engine (source of record)
    return gate_lint_doctype_parity


# Re-export the pure helpers as module attributes so the importlib direct-load
# regression can call mod.name_is_cell / mod.doctype_region.
name_is_cell = _engine().name_is_cell
doctype_region = _engine().doctype_region


def canonical_sets():
    """Return (names, prefixes) from lint-metadata.py, the source of truth.
    Kept a module-global (monkeypatched by the synthetic-missing-type test)."""
    meta = _load_module(TOOLS / "lint-metadata.py")
    names = set(meta.ALLOWED_TYPES)
    prefixes = set()
    for plist in meta.TYPE_TO_PREFIX.values():
        prefixes.update(plist)
    return names, prefixes


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


# Per-surface doctype-region anchors (#729). Module-level so the anchor-resolution
# regression can iterate them. Each anchor is a heading (block runs to the next
# same-or-shallower heading) or, for the heading-less AI-ingestion numbered list,
# the distinctive prefix-list line.
NAME_REGION_ANCHOR = {
    "README.md": ("heading", "## Document types"),
    "specification-ingestion.md": ("heading", "## Document types"),
    "governance/charter-governance-library.md": ("heading", "## Document hierarchy"),
    "governance/framework-document-architecture-and-interrelationship.md":
        ("heading", "## Document hierarchy"),
}
PREFIX_REGION_ANCHOR = {
    "specification-master-project.md": ("heading", "### 4.3 Document-type definitions"),
    "instruction-ai-document-ingestion.md":
        ("phrase", "canonical filename using the type prefix"),
    "CONTRIBUTING.md": ("heading", "## Filename rules"),
}


def main() -> int:
    names, prefixes = canonical_sets()

    # Check 1: the second linter's doctype set (profile-loaded via _alignment_config())
    # must equal the canonical names, compared case-insensitively (the doctype set is
    # lowercase; ALLOWED_TYPES is CamelCase).
    fta = _load_module(TOOLS / "lint-filename-title-alignment.py")
    canon_lower = {n.lower() for n in names}
    doctypes = set(fta._alignment_config()[1])

    # Check 2: the required-sections linter's enforced keys must all be valid canonical
    # types (types absent from its map are not-enforced BY DESIGN; an invalid key fails).
    rs = _load_module(TOOLS / "lint-required-sections.py")
    rs_keys = set(rs._sections_config().keys())

    set_checks = [
        {
            "actual": doctypes,
            "canonical": canon_lower,
            "mode": "equal",
            "missing_template": (
                "tools/lint-filename-title-alignment.py alignment doctypes (from "
                "defaults/grc/alignment.toml) is missing canonical type(s): {tokens}"
            ),
            "extra_template": (
                "tools/lint-filename-title-alignment.py alignment doctypes (from "
                "defaults/grc/alignment.toml) has type(s) not in "
                "lint-metadata.py ALLOWED_TYPES: {tokens}"
            ),
        },
        {
            "actual": rs_keys,
            "canonical": names,
            "mode": "extra_only",
            "extra_template": (
                "tools/lint-required-sections.py section model (_sections_config, from "
                "defaults/grc/sections.toml) has doctype key(s) not in "
                "lint-metadata.py ALLOWED_TYPES: {tokens}"
            ),
        },
    ]

    name_labels = {
        "README.md": "README `## Document types` table",
        "specification-ingestion.md": "the ingestion spec allowed-type list",
        "governance/charter-governance-library.md": "the charter `Document hierarchy` table",
        "governance/framework-document-architecture-and-interrelationship.md":
            "the document-architecture `Document hierarchy` table",
    }
    name_surfaces = []
    for rel, label in name_labels.items():
        anchor = NAME_REGION_ANCHOR[rel]
        name_surfaces.append({
            "text": read(rel),
            "anchor": anchor,
            "anchor_absent_msg": (
                f"{rel} ({label}): the doctype-region anchor "
                f"{anchor[1]!r} is absent (cannot locate the enumeration)"
            ),
            "omit_template": (
                f"{rel} ({label}) omits type name(s) as a cell/item in its "
                f"doctype region: {{tokens}}"
            ),
        })

    prefix_labels = {
        "specification-master-project.md": "the master-spec section 4.3 Type-to-prefix table",
        "instruction-ai-document-ingestion.md": "the AI-ingestion instruction",
        "CONTRIBUTING.md": "the CONTRIBUTING filename-prefix list",
    }
    prefix_surfaces = []
    for rel, label in prefix_labels.items():
        anchor = PREFIX_REGION_ANCHOR[rel]
        prefix_surfaces.append({
            "text": read(rel),
            "anchor": anchor,
            "anchor_absent_msg": (
                f"{rel} ({label}): the doctype-region anchor "
                f"{anchor[1]!r} is absent (cannot locate the enumeration)"
            ),
            "omit_template": (
                f"{rel} ({label}) omits filename prefix(es) in its "
                f"doctype region: {{tokens}}"
            ),
        })

    failures = _engine().collect_findings(
        canonical_names=names,
        canonical_prefixes=prefixes,
        set_checks=set_checks,
        name_surfaces=name_surfaces,
        prefix_surfaces=prefix_surfaces,
    )

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
