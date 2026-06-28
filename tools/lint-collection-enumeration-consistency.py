#!/usr/bin/env python3
"""Collection-enumeration consistency audit.

The corpus carries several "collections" of items that are enumerated
in multiple places: the pack's eleven governance rules are listed in the
pack README directory-tree section, in the pack's own CLAUDE.md
Development-governance discipline section, and in the project's
CLAUDE.md Security-and-governance-requirements section; the pack's
skills are listed in the pack README; and the external overlay
sources (TikiTribe, Kariedo, addyosmani) are listed in NOTICE.md and
the project's CLAUDE.md.

When an item is added to a collection (new governance rule, new
skill, new external source) the canonical source-of-truth (the
directory) gains a new entry, but the enumeration locations elsewhere
in the corpus can fall behind, causing drift. This audit detects that
drift by parsing each enumeration location and comparing its set of
items to the canonical directory listing.

Phase 1 (this iteration): two hard-coded collections (the pack's
governance rules and its skills), each with one or more enumeration
locations. The external overlay sources noted above are enumerated
similarly but are not yet wired into this linter. The companion detector tool
(``tools/detect-collection-candidates.py``, separate PR) finds
additional candidate collections by heuristic scan; the maintainer
triages those one-by-one and adds approved candidates to this
linter's configuration.

Exit codes: 0 pass, 1 findings (drift detected), 2 internal error.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from lint_common import REPO_ROOT, read_text_safe


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
    # by listing entries matching the glob and normalising their names.
    source_dir: str
    source_glob: str
    # Function name (in this file) that normalises a source filename
    # to the canonical item name. Each collection picks a normaliser
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


COLLECTIONS: tuple[Collection, ...] = (
    Collection(
        name="pack-governance-rules",
        source_dir="dev-security/claude-rules/governance",
        source_glob="*.md",
        source_normaliser="strip_md",
        enumerations=(
            EnumerationLocation(
                file="dev-security/claude-rules/README.md",
                section_start_regex=r"^├── governance/",
                section_end_regex=r"^├── \w+/",
                item_regex=r"^│\s+[├└]──\s+([\w-]+)\.md",
            ),
            EnumerationLocation(
                file="dev-security/claude-rules/CLAUDE.md",
                section_start_regex=r"^- \[`governance/",
                section_end_regex=r"^The phased governance rollout|^---|^## ",
                item_regex=r"^- \[`governance/([\w-]+)\.md`\]",
            ),
            EnumerationLocation(
                file=".claude/CLAUDE.md",
                section_start_regex=r"^- `\.claude/rules/governance/",
                section_end_regex=r"^The `dev-security/claude-rules/` pack|^---|^## ",
                item_regex=r"^- `\.claude/rules/governance/([\w-]+)\.md`",
            ),
        ),
    ),
    Collection(
        name="pack-skills",
        source_dir="dev-security/claude-rules/skills",
        source_glob="*",
        source_normaliser="dirname",
        enumerations=(
            EnumerationLocation(
                file="dev-security/claude-rules/README.md",
                section_start_regex=r"^├── skills/",
                section_end_regex=r"^├── \w+|^└── ",
                item_regex=r"^│\s+[├└]──\s+([\w-]+)/SKILL\.md",
            ),
        ),
    ),
)


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
    for line in text.splitlines():
        if not in_section:
            if start_re.search(line):
                in_section = True
                # The start line itself MAY contain an item if the
                # pattern allows. Try item_regex on this line too.
                m = item_re.search(line)
                if m:
                    items.add(m.group(1))
            continue
        # In section: check for end first
        if end_re is not None and end_re.search(line):
            break
        m = item_re.search(line)
        if m:
            items.add(m.group(1))
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
    sys.exit(main(sys.argv))
