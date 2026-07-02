#!/usr/bin/env python3
"""Generate `taxonomy.yml` from the metadata of every active document.

The taxonomy is a single derived registry that captures the canonical
13-field metadata block of every active artefact as structured data.
It is regenerated from the source documents; it is not the source of
truth. Other tooling (a future portal renderer, the reverse crosswalk
generator, etc.) reads `taxonomy.yml` to produce derived artefacts.

Usage:
    python3 tools/build-taxonomy.py
    python3 tools/build-taxonomy.py --check    # validate without writing

`--check` exits non-zero if the generated YAML differs from the file
already on disk, suitable for CI integration.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = REPO_ROOT / "taxonomy.yml"

DOMAINS = [
    "ai",
    "architecture",
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

# DOMAINS is the corpus deliverable's domain set. `.project-governance/`
# is deliberately NOT a domain: it holds project-governance operational
# records (not the published deliverable) and is excluded from the
# taxonomy, portal, and maturity scorecard per the project-governance
# separation specification (governance/specification-project-governance-separation.md
# section 7.2). Because the walk below is restricted to DOMAINS, the
# exclusion is structural; do not add `.project-governance` here.

EXEMPT_FROM_INDEX = {
    "privacy/annex-regional-privacy-requirements.md",
}

# Only the claude-rules subdirectory of dev-security is excluded from
# the per-domain walk. (Phase 23.62 removed `tools/` and `docs/` from
# this tuple because the walk is restricted to the DOMAINS list and
# never reaches those directories; EXEMPT_FILES was also removed as a
# whole because it was defined but never read.)
EXEMPT_DIRECTORY_PREFIXES = (
    "dev-security/claude-rules/",
)

FIELD_PATTERN = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
LINK_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")


def iter_all_docs() -> list[Path]:
    """Active governance artefacts (not READMEs, not exempt dirs, not superseded)."""
    files: list[Path] = []
    for domain in DOMAINS:
        base = REPO_ROOT / domain
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            rel = f.relative_to(REPO_ROOT).as_posix()
            if f.name == "README.md":
                continue
            if rel in EXEMPT_FROM_INDEX:
                continue
            if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
                continue
            files.append(f)
    # Add root-level controlled artefacts (the two specifications).
    for name in ("specification-master-project.md", "specification-ingestion.md"):
        p = REPO_ROOT / name
        if p.exists():
            files.append(p)
    return sorted(set(files))


def extract_metadata(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    seen = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("---") and seen:
            break
        if not s and seen:
            break
        m = FIELD_PATTERN.match(line)
        if m:
            name, value = m.groups()
            value = value.strip()
            # Strip CommonMark hard-line-break backslash if present.
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            fields[name.strip()] = value
            seen = True
    return fields


def normalize_link(value: str) -> str:
    m = LINK_RE.search(value)
    if m:
        return m.group(1)
    return value.strip()


def normalize_related(value: str) -> list[str]:
    """Return the list of repo-relative paths from a Related Documents field."""
    paths: list[str] = []
    for m in LINK_RE.finditer(value):
        display = m.group(1)
        if display.endswith(".md"):
            paths.append(display)
    return paths


def yaml_escape(s: str) -> str:
    """Conservative YAML scalar escape: prefer double-quoted strings."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit_doc(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    meta = extract_metadata(text)

    # Derive domain from first path segment (or 'root' for root-level files).
    if "/" in rel:
        domain = rel.split("/", 1)[0]
    else:
        domain = "root"

    title = meta.get("Document Title", path.stem)
    doc_type = meta.get("Document Type", "")
    version = meta.get("Version", "")
    date = meta.get("Date", "")
    owner = meta.get("Owner", "")
    approver = meta.get("Approving Authority", "")
    classification = meta.get("Classification", "")
    category = meta.get("Category", "")
    review = meta.get("Review Frequency", "")
    license_ = meta.get("License", "")
    related = normalize_related(meta.get("Related Documents", ""))

    lines: list[str] = []
    lines.append(f"- path: {yaml_escape(rel)}")
    lines.append(f"  domain: {yaml_escape(domain)}")
    lines.append(f"  type: {yaml_escape(doc_type)}")
    lines.append(f"  title: {yaml_escape(title)}")
    lines.append(f"  version: {yaml_escape(version)}")
    lines.append(f"  date: {yaml_escape(date)}")
    lines.append(f"  owner: {yaml_escape(owner)}")
    lines.append(f"  approving_authority: {yaml_escape(approver)}")
    lines.append(f"  classification: {yaml_escape(classification)}")
    lines.append(f"  category: {yaml_escape(category)}")
    lines.append(f"  review_frequency: {yaml_escape(review)}")
    lines.append(f"  license: {yaml_escape(license_)}")
    if related:
        lines.append("  related_documents:")
        for r in related:
            lines.append(f"    - {yaml_escape(r)}")
    else:
        lines.append("  related_documents: []")
    return "\n".join(lines)


def build() -> str:
    out: list[str] = []
    out.append("# Auto-generated machine-readable taxonomy for the GRC Documentation Library.")
    out.append("# Source of truth: the canonical metadata block of each artefact.")
    out.append("# Regenerate with `python3 tools/build-taxonomy.py`.")
    out.append("# Do not edit this file by hand.")
    out.append("")
    out.append("schema_version: 1")
    out.append("generated_by: tools/build-taxonomy.py")
    out.append("documents:")
    docs = iter_all_docs()
    for d in docs:
        out.append(emit_doc(d))
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate taxonomy.yml from document metadata.")
    parser.add_argument("--check", action="store_true",
                        help="Validate that taxonomy.yml is in sync with document metadata; "
                             "do not write. Exits non-zero on drift.")
    args = parser.parse_args()

    new_content = build()

    if args.check:
        if not TAXONOMY.exists():
            print(f"FAIL: {TAXONOMY.name} does not exist; run without --check to generate.")
            return 1
        current = TAXONOMY.read_text(encoding="utf-8")
        if current != new_content:
            print(f"FAIL: {TAXONOMY.name} is out of sync with document metadata.")
            print("Run `python3 tools/build-taxonomy.py` to regenerate.")
            return 1
        print(f"OK: {TAXONOMY.name} is in sync.")
        return 0

    TAXONOMY.write_text(new_content, encoding="utf-8")
    print(f"Wrote {TAXONOMY.name} ({len(new_content.splitlines())} lines).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
