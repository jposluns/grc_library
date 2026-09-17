#!/usr/bin/env python3
"""Document metadata-block audit - grc wrapper over the pack-owned engine.

Validate every governance document's metadata block against the library's metadata
model: the 13 required fields present, Document Type in the allowed set, Version
semver, Date ISO-8601, Owner / Approving Authority role-based, License the canonical
value, Repository Path a self-referential link, filename prefix matching the
Document Type, and the backslash-newline hard-break markers on the block.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(extract_metadata, check_line_break_markers, looks_role_based, normalize_link_value,
check_file) plus the generic metadata-parsing regexes live in the pack-owned engine
(.corpus-management/tools/gate_lint_metadata.py, source of record). This wrapper
supplies the grc METADATA MODEL (allowed types, type-to-prefix map, required fields,
exempt sets, role vocabularies, canonical license) and the scan scope + grouped
reporting, and keeps module-global check_file(path) + iter_markdown_files shims so
the scan-scope regression test (which calls mod.check_file / mod.iter_markdown_files)
and the doctype-parity gate (which reads ALLOWED_TYPES / TYPE_TO_PREFIX from this
file) both keep working.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from lint_common import is_default_exempt_root, AUDITED_DOMAIN_DIRS, REPO_ROOT

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

ALLOWED_TYPES = {
    "Charter",
    "Framework",
    "Policy",
    "Principle",
    "Standard",
    "Procedure",
    "SOP",
    "Plan",
    "Roadmap",
    "Guideline",
    "Guide",
    "Register",
    "Matrix",
    "Specification",
    "Template",
    "Annex",
    "Checklist",
    "Worklist",
}

# Map document type -> allowed filename prefix(es).
TYPE_TO_PREFIX = {
    "Charter": ["charter-"],
    "Framework": ["framework-"],
    "Policy": ["policy-"],
    "Principle": ["principle-"],
    "Standard": ["standard-"],
    "Procedure": ["procedure-"],
    "SOP": ["sop-"],
    "Plan": ["plan-"],
    "Roadmap": ["roadmap-"],
    "Guideline": ["guideline-"],
    "Guide": ["guide-"],
    "Register": ["register-"],
    "Matrix": ["matrix-"],
    "Specification": ["specification-"],
    "Template": ["template-"],
    "Annex": ["annex-"],
    "Checklist": ["checklist-"],
    "Worklist": ["worklist-"],
}

# Files that do not require the full canonical metadata block.
EXEMPT = {
    "README.md",
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "instruction-ai-document-ingestion.md",
}

# Directories whose contents are exempt from the full canonical metadata block.
EXEMPT_PREFIXES = (
    "guardrails/",
    "tools/",
)

# Files exempt from the filename-prefix rule.
PREFIX_EXEMPT_BASENAMES = {
    "README.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "AUTHORS.md",
    "worked-example.md",
    "worked-example-adoption.md",
    "adopter-guide.md",
    "adopter-guide-multi-entity.md",
    "decision-tree.md",
    "portal.md",
    "maturity-scorecard.md",
    "reference-acquisition-manifest.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
}

REQUIRED_FIELDS = [
    "Document Title",
    "Document Type",
    "Version",
    "Date",
    "Owner",
    "Approving Authority",
    "Related Documents",
    "Classification",
    "Category",
    "Review Frequency",
    "Repository Path",
    "Confidentiality",
    "License",
]

# Role-based Owner / Approving Authority heuristic vocabularies.
ROLE_SUFFIXES = {
    "Officer",
    "Maintainer",
    "Owner",
    "Lead",
    "Manager",
    "Counsel",
    "Authority",
    "Administrator",
    "Council",
    "Committee",
    "Architect",
    "Team",
    "Director",
    "Directors",
    "Specialist",
    "Board",
    "Executive",
    "Function",
    "Office",
    "Reviewer",
    "Sponsor",
    "Custodian",
}

ROLE_STEMS = {
    "Chief",
    "Lead",
    "Head",
    "Principal",
    "Senior",
    "Executive",
    "Governance",
    "Risk",
    "Privacy",
    "Compliance",
    "Audit",
    "Security",
    "Information",
    "Data",
    "Resilience",
    "Supplier",
    "Continuity",
    "Communications",
    "Operations",
    "Technology",
    "Engineering",
    "Library",
    "Programme",
    "AI",
}

LICENSE_VALUE = "CC BY-SA 4.0"


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_metadata  # the pack-owned engine (source of record)
    return gate_lint_metadata


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


def check_file(path: Path) -> list[str]:
    """Thin shim delegating to the pack engine's pure check with the grc model.

    Kept as a module-global because the scan-scope regression test calls
    ``mod.check_file`` directly; the check logic lives in the pack engine.
    """
    return _engine().check_file(
        path,
        REPO_ROOT,
        is_exempt_root=is_default_exempt_root,
        exempt=EXEMPT,
        exempt_prefixes=EXEMPT_PREFIXES,
        required_fields=REQUIRED_FIELDS,
        allowed_types=ALLOWED_TYPES,
        type_to_prefix=TYPE_TO_PREFIX,
        prefix_exempt_basenames=PREFIX_EXEMPT_BASENAMES,
        role_suffixes=ROLE_SUFFIXES,
        role_stems=ROLE_STEMS,
        license_value=LICENSE_VALUE,
    )


def main(argv: list[str]) -> int:
    paths = argv[1:] or [
        "README.md",
        "NOTICE.md",
        "specification-master-project.md",
        "specification-ingestion.md",
        "specification-executive-narrative.md",
        "instruction-ai-document-ingestion.md",
        "docs",
        # Domain run splatted from lint_common (scan-scope parity gate
        # forbids hardcoding the run); ``docs`` above is a per-linter extra.
        *AUDITED_DOMAIN_DIRS,
    ]

    files = iter_markdown_files(paths)
    grouped: dict[str, list[str]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f):
            grouped[f.relative_to(REPO_ROOT).as_posix()].append(finding)
            total += 1

    if not grouped:
        print("OK: no metadata findings.")
        return 0

    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for finding in grouped[relpath]:
            print(f"  {finding}")

    print(f"\nFAIL: {total} finding(s) across {len(grouped)} file(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
