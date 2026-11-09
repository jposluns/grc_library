#!/usr/bin/env python3
"""Collection-enumeration consistency audit.

The corpus carries "collections" of items that are enumerated in more
than one place. Each collection has a canonical source-of-truth (a
directory) and one or more enumeration locations elsewhere in the
corpus. When an item is added to a collection the directory gains a new
entry, but the enumeration locations can fall behind, causing drift.
This audit detects that drift by parsing each enumeration location and
comparing its set of items to the canonical directory listing.

Companion note (gate 39 symmetry): ``.claude/skills/corpus-management/tools/lint-gate-count-consistency.py``
(gate 39) mirrors this gate's collection-source list so the two gates
agree on what counts as a collection item (see its
``# mirror gate 41's collection sources`` comment). An editor who changes
the collection sources here should keep gate 39's mirrored list in step.

The collections that ship are the pinned AIQT principles
(``.claude/aiqt/rules/aiqt/``) and the pinned security rules
(``.claude/aiqt/rules/security/``). Each is checked against the pinned
manifest inventory and against its entries in the generated
``AIQT-RULES`` index block of ``.claude/CLAUDE.md``. The pack
governance-rule and pack-skill collections, and the README, pack
CLAUDE.md and rule-provenance enumerations of the pinned families, lived
in the ``guardrails/`` tree, which does not ship, so they are no longer
configured; the tree holds no retained legacy-procedures directory or
enumeration block either. The external overlay sources are enumerated
in NOTICE.md but are not wired into this linter.

Exit codes: 0 pass, 1 findings (drift detected), 2 internal error.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import NamedTuple

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/skills/corpus-management/tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT  # noqa: E402  # grc-config/store, stays local


@dataclass(frozen=True)
class EnumerationLocation:
    """Where in the corpus a collection is enumerated."""
    file: str
    # Regex that anchors the start of the enumeration section. The
    # parser searches for the FIRST match and treats lines AFTER it
    # as candidates.
    section_start_regex: str
    # Regex that anchors the end of the enumeration. The parser stops
    # at the FIRST match after the section start. If None, the parser
    # continues until either end-of-file or a blank line followed by a
    # non-matching line.
    section_end_regex: str | None
    # Regex that extracts the item name from each line in the section.
    # Capturing group 1 is the item name (basename, no extension).
    item_regex: str


@dataclass(frozen=True)
class Collection:
    name: str
    # Source-of-truth directory and glob pattern. Items are discovered
    # by listing entries matching the glob and normalizing their names.
    source_dir: str
    source_glob: str
    # Function name (in this file) that normalizes a source filename
    # to the canonical item name. Each collection picks a normalizer
    # appropriate for its source layout.
    source_normaliser: str
    # Locations elsewhere in the corpus that enumerate the same
    # collection.
    enumerations: tuple[EnumerationLocation, ...]


def normalise_strip_md(name: str) -> str:
    """``foo.md`` -> ``foo``. Used for rule files."""
    return name[:-3] if name.endswith(".md") else name


def normalise_dirname(name: str) -> str:
    """Directory-as-item: ``foo/`` -> ``foo``."""
    return name.rstrip("/")


NORMALISERS: dict[str, callable] = {
    "strip_md": normalise_strip_md,
    "dirname": normalise_dirname,
}


COLLECTIONS: tuple[Collection, ...] = ()


# Each pinned AIQT family is checked against its directory and the pinned
# manifest inventory (list_source) and against its entries in the generated
# AIQT-RULES index block of .claude/CLAUDE.md, the enumeration surface that
# ships. The guardrails/ README, pack CLAUDE.md and rule-provenance surfaces
# do not ship and are not configured.
for family in ("aiqt", "security"):
    locations = [EnumerationLocation(".claude/CLAUDE.md", r"^<!-- AIQT-RULES-BEGIN -->$",
        r"^<!-- AIQT-RULES-END -->$", rf"\[`{family}/([\w-]+)\.md`\]")]
    COLLECTIONS += (Collection("pinned-" + family, ".claude/aiqt/rules/" + family,
                              "*.md", "strip_md", tuple(locations)),)

class Finding(NamedTuple):
    collection: str
    location: str
    missing: tuple[str, ...]
    extra: tuple[str, ...]


def list_source(collection: Collection) -> set[str]:
    """Return the canonical set of item names for a collection."""
    norm = NORMALISERS[collection.source_normaliser]
    source_path = REPO_ROOT / collection.source_dir
    if not source_path.is_dir():
        raise RuntimeError(f"source directory does not exist: {source_path}")
    items: set[str] = set()
    for entry in source_path.iterdir():
        if entry.name.startswith("."):
            continue
        # Match glob: simple suffix check for *.md, otherwise accept all.
        if collection.source_glob.startswith("*."):
            suffix = collection.source_glob[1:]
            if entry.is_file() and entry.name.endswith(suffix):
                items.add(norm(entry.name))
        else:
            # Generic glob (``*``): include directories and files.
            items.add(norm(entry.name))
    if collection.name.startswith("pinned-"):
        from aiqt_rules import inventory
        try:
            manifest = inventory(REPO_ROOT)
            prefix = collection.source_dir + "/"
            declared = {normalise_strip_md(r["path"].removeprefix(prefix))
                        for r in manifest["files"] if r["path"].startswith(prefix)}
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise RuntimeError(f"invalid AIQT manifest: {exc}") from exc
        if items != declared:
            raise RuntimeError(f"AIQT manifest/directory disagreement: {collection.name}")
    return items


def parse_enumeration(location: EnumerationLocation) -> set[str]:
    """Parse an enumeration location and return the set of item names."""
    path = REPO_ROOT / location.file
    text = read_text_safe(path)
    if text is None:
        raise RuntimeError(f"enumeration location not readable: {path}")
    start_re = re.compile(location.section_start_regex)
    end_re = re.compile(location.section_end_regex) if location.section_end_regex else None
    item_re = re.compile(location.item_regex)
    items: set[str] = set()
    in_section = False
    ended = False
    for line in text.splitlines():
        if not in_section:
            if not start_re.search(line):
                continue
            in_section = True
        elif end_re is not None and end_re.search(line):
            ended = True
            break
        for match in item_re.finditer(line):
            item = match.group(1)
            if item in items:
                raise RuntimeError(f"duplicate enumeration {item}: {location.file}")
            items.add(item)
    if not in_section or not items:
        raise RuntimeError(f"missing or empty enumeration: {location.file}")
    if location.section_start_regex.startswith("^<!--") and not ended:
        raise RuntimeError(f"missing enumeration end marker: {location.file}")
    return items


def check_collection(collection: Collection) -> list[Finding]:
    findings: list[Finding] = []
    canonical = list_source(collection)
    for location in collection.enumerations:
        enumerated = parse_enumeration(location)
        missing = tuple(sorted(canonical - enumerated))
        extra = tuple(sorted(enumerated - canonical))
        if missing or extra:
            findings.append(
                Finding(
                    collection=collection.name,
                    location=location.file,
                    missing=missing,
                    extra=extra,
                )
            )
    return findings


def main(argv: list[str]) -> int:
    all_findings: list[Finding] = []
    try:
        for collection in COLLECTIONS:
            all_findings.extend(check_collection(collection))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not all_findings:
        n_checked = sum(len(c.enumerations) for c in COLLECTIONS)
        print(
            f"OK: {len(COLLECTIONS)} collection(s), "
            f"{n_checked} enumeration location(s) checked, all consistent."
        )
        return 0

    for finding in all_findings:
        print(f"=== {finding.collection} in {finding.location} ===")
        if finding.missing:
            print(f"  missing items (in canonical but not enumeration): {', '.join(finding.missing)}")
        if finding.extra:
            print(f"  extra items (in enumeration but not canonical): {', '.join(finding.extra)}")
    print(
        f"\nFAIL: {len(all_findings)} collection-enumeration drift finding(s). "
        f"Each finding shows items that drifted between the canonical source "
        f"(directory listing) and an enumeration location elsewhere in the corpus. "
        f"Resolve by updating the enumeration to match the canonical set.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ())
    sys.exit(main(sys.argv))
