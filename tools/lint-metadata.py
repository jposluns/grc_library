#!/usr/bin/env python3
"""Metadata audit for the GRC Documentation Library.

Asserts the canonical 13-field metadata block for every active markdown
document:

1. Document Title
2. Document Type
3. Version
4. Date
5. Owner
6. Approving Authority
7. Related Documents
8. Classification
9. Category
10. Review Frequency
11. Repository Path
12. Confidentiality
13. License

Additional checks:

- Document Type is one of the 16 allowed types.
- Version follows semantic versioning (`x.y.z`).
- Date follows ISO 8601 (`YYYY-MM-DD`).
- Owner and Approving Authority are role-based (no obvious person names).
- License is `CC0 1.0 Universal`.
- Repository Path matches the file's actual path (after stripping the
  `[`display`](target)` markdown link wrapper).
- Filename prefix matches Document Type (e.g. `policy-foo.md` -> Policy).

Excluded from the metadata block requirement:

- Domain README files (these use a simpler shape).
- The repository root README, NOTICE, LICENSE, and AI ingestion instruction
  file, which are governance / meta files rather than artefact documents.

Usage:
    python3 tools/lint-metadata.py [paths...]

Exits non-zero on any findings.
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_TYPES = {
    "Charter",
    "Framework",
    "Policy",
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
}

# Map document type -> allowed filename prefix(es).
TYPE_TO_PREFIX = {
    "Charter": ["charter-"],
    "Framework": ["framework-"],
    "Policy": ["policy-"],
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
}

# Files that do not require the full canonical metadata block.
EXEMPT = {
    "README.md",
    "NOTICE.md",
    "LICENSE",
    "instruction-ai-document-ingestion.md",
}

# Directories whose contents are exempt from the full canonical metadata block.
# These are draggable AI-context files (claude-rules/) and tooling docs (tools/, docs/),
# which serve a different purpose than governance artefacts.
EXEMPT_PREFIXES = (
    "dev-security/claude-rules/",
    "tools/",
    "docs/",
)

# Domain README files: simpler shape; skipped from full block enforcement.
DOMAIN_README_NAMES = {"README.md"}

# Files exempt from the filename-prefix rule.
PREFIX_EXEMPT_BASENAMES = {
    "README.md",
    "NOTICE.md",
    "LICENSE",
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

FIELD_PATTERN = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")

# Heuristic for person names: two capitalised words. Allowed if it matches
# known role suffixes.
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


def extract_metadata(text: str) -> dict[str, str]:
    """Return the metadata block parsed as a field name to value dict."""
    fields: dict[str, str] = {}
    # The block ends at the first `---` separator line or first empty line
    # after at least one field has been seen.
    seen_field = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("---") and seen_field:
            break
        if not stripped and seen_field:
            break
        m = FIELD_PATTERN.match(line)
        if m:
            name, value = m.groups()
            fields[name.strip()] = value.strip()
            seen_field = True
    return fields


def looks_role_based(value: str) -> bool:
    if not value:
        return True
    # Strip a trailing parenthetical or comma list.
    cleaned = re.sub(r"\(.*?\)", "", value).strip()
    # Accept comma-separated multi-role declarations: check each part.
    parts = [p.strip() for p in re.split(r"[,/]", cleaned) if p.strip()]
    for part in parts:
        words = part.split()
        if any(w in ROLE_SUFFIXES for w in words):
            continue
        # Allow common role-stem words.
        if any(w in {"Chief", "Lead", "Head", "Principal", "Senior",
                     "Executive", "Governance", "Risk", "Privacy",
                     "Compliance", "Audit", "Security", "Information",
                     "Data", "Resilience", "Supplier", "Continuity",
                     "Communications", "Operations", "Technology",
                     "Engineering", "Library", "Programme", "AI"}
               for w in words):
            continue
        # Otherwise flag as suspicious.
        return False
    return True


def normalize_link_value(value: str) -> str:
    """If the field value is a markdown link, return the target; otherwise return value."""
    m = LINK_RE.search(value)
    if m:
        return m.group(2)
    return value.strip()


def check_file(path: Path) -> list[str]:
    findings: list[str] = []
    rel = path.relative_to(REPO_ROOT).as_posix()
    basename = path.name

    if rel in EXEMPT:
        return findings

    # Files in exempt directories (tooling docs, draggable rule files) are skipped.
    if any(rel.startswith(p) for p in EXEMPT_PREFIXES):
        return findings

    # Domain README files: enforce only the basic metadata header (loose check).
    if basename == "README.md" and rel != "README.md":
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append("file not utf-8")
            return findings
        meta = extract_metadata(text)
        # Loose: require Document Title and License at minimum.
        for required in ("Document Title", "License"):
            if required not in meta:
                findings.append(f"domain README missing field: {required}")
        return findings

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append("file not utf-8")
        return findings

    meta = extract_metadata(text)

    # 1. All required fields present.
    for f in REQUIRED_FIELDS:
        if f not in meta:
            findings.append(f"missing required metadata field: {f}")

    # 2. Document Type allowed.
    dtype = meta.get("Document Type", "").strip()
    if dtype and dtype not in ALLOWED_TYPES:
        findings.append(f"invalid Document Type: {dtype!r}")

    # 3. Version semver.
    version = meta.get("Version", "").strip()
    if version and not VERSION_RE.match(version):
        findings.append(f"invalid Version (expected x.y.z): {version!r}")

    # 4. Date ISO 8601.
    date_val = meta.get("Date", "").strip()
    if date_val and not DATE_RE.match(date_val):
        findings.append(f"invalid Date (expected YYYY-MM-DD): {date_val!r}")

    # 5. Owner / Approving Authority role-based.
    for role_field in ("Owner", "Approving Authority"):
        v = meta.get(role_field, "")
        if v and not looks_role_based(v):
            findings.append(f"{role_field} does not look role-based: {v!r}")

    # 6. License is CC0 1.0 Universal.
    lic = meta.get("License", "").strip()
    if lic and lic != "CC0 1.0 Universal":
        findings.append(f"License is not 'CC0 1.0 Universal': {lic!r}")

    # 7. Repository Path matches actual path (after link normalisation).
    repo_path_field = meta.get("Repository Path", "")
    if repo_path_field:
        link = LINK_RE.search(repo_path_field)
        if link:
            display = link.group(1)
            if display != rel:
                findings.append(f"Repository Path display does not match actual path: "
                                f"{display!r} vs {rel!r}")
        else:
            findings.append(f"Repository Path is not a markdown link: {repo_path_field!r}")

    # 8. Filename prefix matches Document Type.
    if basename not in PREFIX_EXEMPT_BASENAMES and dtype in TYPE_TO_PREFIX:
        prefixes = TYPE_TO_PREFIX[dtype]
        if not any(basename.startswith(p) for p in prefixes):
            findings.append(f"filename prefix does not match Document Type "
                            f"{dtype!r}: expected one of {prefixes}")

    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or [
        "README.md",
        "NOTICE.md",
        "specification-master-project.md",
        "specification-ingestion.md",
        "instruction-ai-document-ingestion.md",
        "ai",
        "compliance",
        "dev-security",
        "governance",
        "operations",
        "privacy",
        "resilience",
        "risk",
        "security",
        "supply-chain",
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
