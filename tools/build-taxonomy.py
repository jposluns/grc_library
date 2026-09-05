#!/usr/bin/env python3
"""Generate `taxonomy.yml` from the metadata of every active document.

The taxonomy is a single derived registry that captures the canonical
metadata block of every active artefact plus its purpose, section outline,
and declared framework alignment, as structured data.
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
    "crypto",
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

# Only the guardrails pack directory is excluded from
# the per-domain walk. (Phase 23.62 removed `tools/` and `docs/` from
# this tuple because the walk is restricted to the DOMAINS list and
# never reaches those directories; EXEMPT_FILES was also removed as a
# whole because it was defined but never read.)
EXEMPT_DIRECTORY_PREFIXES = (
    "guardrails/",
)

FIELD_PATTERN = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
LINK_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")


# Reading-progression rank for the per-domain document order (maintainer-directed
# 2026-07-15, "source + type-priority ordering"). The taxonomy lists a domain's documents
# most-foundational-first (govern -> define -> do -> reference), then alphabetically by
# title within a type; the surfaces that render taxonomy order, notably the per-domain
# website pages, inherit it. Ordering at the source keeps taxonomy.yml, the website domain
# pages, and the scorecard consistent (the order-insensitive lint consumers are unaffected).
# A document type not listed here sorts AFTER all known types (rank = len), so a newly
# introduced type is visibly last rather than silently interleaved.
TYPE_ORDER = (
    "Principle", "Charter", "Policy", "Framework", "Standard", "Specification",
    "Procedure", "SOP", "Guide", "Guideline", "Plan", "Roadmap",
    "Matrix", "Register", "Checklist", "Template", "Annex",
)
TYPE_RANK = {t: i for i, t in enumerate(TYPE_ORDER)}


def _order_key(path: Path) -> tuple:
    """Sort key for the per-domain reading-progression order: (domain, type-rank, title, path).

    Domains keep their alphabetical grouping (unchanged); within a domain, documents run
    most-foundational-first by ``TYPE_RANK``, then alphabetically by title, with the
    repo-relative path as a final deterministic tiebreaker (so the order is reproducible and
    the drift gate stays clean). Reads the small metadata block so type/title are available
    before emission. Maintainer-directed 2026-07-15."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    domain = rel.split("/", 1)[0] if "/" in rel else "root"
    meta = extract_metadata(path.read_text(encoding="utf-8"))
    doc_type = meta.get("Document Type", "")
    title = meta.get("Document Title", path.stem)
    return (domain, TYPE_RANK.get(doc_type, len(TYPE_ORDER)), title.lower(), rel)


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
    return sorted(set(files), key=_order_key)


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


def _flatten_md(text: str) -> str:
    """Reduce inline Markdown in a one-paragraph string to display-ready prose so
    the taxonomy holds clean text for the on-site lede + meta description (the
    corpus purpose paragraphs carry links, bold, and code spans)."""
    text = re.sub(r"\[`?([^\]`]+)`?\]\([^)]*\)", r"\1", text)  # [text](url) -> text
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)             # **bold**
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)    # *italic*
    text = text.replace("`", "")                              # code spans
    return re.sub(r"\s{2,}", " ", text).strip()


def _first_paragraph(lines: list[str]) -> str:
    """First real prose paragraph, skipping intervening sub-headings (### and
    deeper). Stops at the next top-level (##) section or a horizontal rule."""
    para: list[str] = []
    for nxt in lines:
        st = nxt.strip()
        if st == "---" or re.match(r"^##\s", nxt):
            break
        if re.match(r"^#{3,}\s", nxt):
            if para:
                break
            continue
        if not st:
            if para:
                break
            continue
        para.append(st)
    return " ".join(para)


def extract_purpose(text: str) -> str:
    """Return the one-paragraph purpose: the first paragraph under a
    ``## [N.] Purpose...`` heading (matching combined headings like
    "Purpose and scope"). Falls back to the document intro paragraph (after the
    metadata block, before the first section) when no Purpose heading exists.
    Empty string only if neither is present."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+(?:\d+\.\s+)?Purpose\b", ln.strip(), re.I):
            return _flatten_md(_first_paragraph(lines[i + 1:]))
    # Fallback: the first prose paragraph after the metadata FIELDS and before
    # the first ``## `` section, wherever the ``---`` terminator sits (some docs
    # put the intro before the terminator, some after it).
    started = False
    para: list[str] = []
    for ln in lines:
        st = ln.strip()
        if st.startswith("## "):
            break
        if st.startswith("# "):
            continue
        if re.match(r"^\*\*[^*]+:\*\*", ln):
            started = True
            continue
        if st == "---" or re.match(r"^#{3,}\s", ln):
            continue
        if not st:
            if para:
                break
            continue
        if started:
            para.append(st)
        elif para:
            break
    return _flatten_md(" ".join(para)) if para else ""


def extract_sections(text: str) -> list[str]:
    """Return the ordered ``## `` section headings (the outline that proves the
    document's depth without dumping its body). Skips fenced code blocks."""
    out: list[str] = []
    in_fence = False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^##\s+(.+?)\s*$", ln)
        if m:
            out.append(m.group(1).strip())
    return out


def _is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(set(c) <= {"-", ":", " "} for c in cells)


# Header cells that label a column but are NOT framework names. Matched by
# pattern (case-insensitive), covering the generic labels and the catch-all
# category columns the corpus alignment tables carry.
_GENERIC_HEAD_RE = re.compile(
    r"^(?:(?:framework|regulatory|legal|standard|control|trade)\s+)*"
    r"(?:reference|references|relevance|note|notes|coverage|mapping|mappings|"
    r"description|requirement|requirements|status|topic|topics|provision|"
    r"provisions|other|others|legal|regulatory|compliance|programme|programmes|"
    r"program|programs|touchpoint|touchpoints|section|sections|area|areas|"
    r"domain|domains|baseline\s+section)$",
    re.I,
)


_GENERIC_HEAD_EXACT = {
    "trade and supply chain programs", "trade and supply chain programmes",
    "corpus ai-governance touchpoint", "regulatory references",
    "legal / regulatory", "legal and regulatory", "control area",
    "repository artefact", "external reference family", "alignment type",
    "applicability condition", "framework coverage", "control objective",
    "evidence class", "evidence sharing", "evidence or rationale",
    "applies", "applies?", "practice analogue", "corpus artefact",
}


def _is_internal_ref(value: str) -> bool:
    """A framework cell that is really an internal corpus cross-reference (a
    repo path, a .md file, or a "refer to ..." pointer) is NOT an external
    framework and is dropped from the chip list."""
    v = value.strip().lower()
    # A repo file reference (ends .md, or a path segment ending in .md). NOT a
    # framework name that merely contains a slash (ISO/IEC, WCO/SAFE).
    if v.endswith(".md") or re.search(r"[a-z0-9_-]+/[a-z0-9_./-]+\.md", v):
        return True
    if v.startswith(("refer to", "see the", "see ", "as per", "per the")):
        return True
    return False


# A jurisdiction/authority label column, e.g. "Australia instrument",
# "Colorado AI statute" (a leading name word + an instrument/statute noun).
# Scoped so a real framework column like "NIST reference" is NOT caught.
_JURIS_LABEL_RE = re.compile(
    r"^[a-z][a-z/ .-]*\s+(?:instruments?|statutes?|obligations?)$", re.I)


def _is_generic_label(cell: str) -> bool:
    c = cell.strip()
    return (c.lower() in _GENERIC_HEAD_EXACT
            or bool(_GENERIC_HEAD_RE.match(c))
            or bool(_JURIS_LABEL_RE.match(c)))


def _split_fw(cell: str) -> list[str]:
    """Split a framework data cell that lists several frameworks separated by
    TOP-LEVEL semicolons (control/reference mappings pack multiple per cell)
    into individual, Markdown-flattened framework strings. A semicolon inside
    parentheses is NOT a separator (e.g. a jurisdiction clause)."""
    parts: list[str] = []
    depth = 0
    buf = ""
    for ch in cell:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == ";" and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    return [f for f in (_flatten_md(p) for p in parts if p.strip())
            if f and not _is_internal_ref(f)]


def _clean_fw(cell: str) -> str:
    """Framework cell, Markdown-flattened (a few tables link the value)."""
    return _flatten_md(cell)


def _dedup(seq: list[str]) -> list[str]:
    out: dict[str, None] = {}
    for x in seq:
        if x and set(x) != {"-"}:
            out.setdefault(x, None)
    return list(out)


def extract_frameworks(text: str) -> list[str]:
    """Return the external frameworks a document declares alignment with, from
    its ``## [N.] Framework alignment`` / ``## [N.] Compliance mapping table``
    section. Handles the corpus's heterogeneous table shapes: COLUMN-oriented
    (control rows, framework names as header columns), ROW-oriented (one
    framework per data row, in the first cell, incl. a ``Framework``/``Reference``
    first-column header), and a 2-column control/reference mapping (frameworks in
    the reference-column data cells). Reads only the FIRST table in the section,
    drops generic label columns, flattens inline Markdown, and de-duplicates.
    Empty list if the document carries no such table."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        head = ln.strip()
        # A framework-alignment section heading: any h2-h4 heading naming a
        # framework/alignment/crosswalk concept (or a compliance mapping table).
        # Over-matching is harmless: a heading with no framework-shaped table or
        # bullet list yields no chips.
        if re.match(r"^#{2,4}\s", head) and (
            (re.search(r"\bframework", head, re.I) and re.search(r"\balign", head, re.I))
            or re.search(r"compliance mapping table", head, re.I)
        ):
            rows: list[list[str]] = []
            started = False
            for nxt in lines[i + 1:]:
                st = nxt.strip()
                if re.match(r"^#{2,4}\s", nxt):
                    break
                if st.startswith("|"):
                    started = True
                    rows.append([c.strip() for c in st.strip("|").split("|")])
                elif started and not st:
                    break  # blank line ends the first table (ignore any later one)
            if not rows:
                # No table: try a bulleted alignment list of the shape
                # "- **Framework name**: description" (or "- Name: description").
                bullets: list[str] = []
                for nxt in lines[i + 1:]:
                    st = nxt.strip()
                    if re.match(r"^#{2,4}\s", nxt):
                        break
                    if st.startswith("- "):
                        for bd in re.findall(r"\*\*(.+?)\*\*", st):
                            b = bd.strip()
                            # A bold span ending in ":" is a grouping label
                            # (e.g. "Canada AI governance:"), never a framework.
                            if b.endswith(":"):
                                continue
                            bullets.append(b)
                fws = [f for f in (_flatten_md(x) for x in bullets)
                       if f and not _is_internal_ref(f) and not _is_generic_label(f)]
                if fws:
                    return _dedup(fws)
                continue
            header = rows[0]
            data = [r for r in rows[1:] if not _is_sep_row(r)]
            first = header[0].strip().lower() if header else ""
            row_oriented = (
                first.startswith(("framework", "standard", "regulation", "source"))
                or first in ("reference", "references")
            )
            if row_oriented:
                out = []
                for r in data:
                    if r and r[0]:
                        out.extend(_split_fw(r[0]))
                return _dedup(out)
            # column-oriented: header columns after the first (control) column,
            # minus any generic label column heads.
            cols = [_clean_fw(c) for c in header[1:]
                    if c and set(c) != {"-"} and not _is_generic_label(c)]
            cols = [c for c in cols if c and not _is_internal_ref(c)]
            if cols:
                return _dedup(cols)
            # a 2-column control/reference mapping: frameworks are the
            # reference-column data cells.
            if len(header) == 2 and data:
                out = []
                for r in data:
                    if len(r) > 1 and r[1]:
                        out.extend(_split_fw(r[1]))
                return _dedup(out)
            return []
    return []


def emit_doc(path: Path, titles: frozenset[str] = frozenset()) -> str:
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
    confidentiality = meta.get("Confidentiality", "")
    related = normalize_related(meta.get("Related Documents", ""))
    purpose = extract_purpose(text)
    sections = extract_sections(text)
    frameworks = [f for f in extract_frameworks(text)
                  if f.strip() not in titles
                  and "(internal)" not in f.lower()]

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
    lines.append(f"  confidentiality: {yaml_escape(confidentiality)}")
    lines.append(f"  purpose: {yaml_escape(purpose)}")
    if related:
        lines.append("  related_documents:")
        for r in related:
            lines.append(f"    - {yaml_escape(r)}")
    else:
        lines.append("  related_documents: []")
    if sections:
        lines.append("  sections:")
        for sec in sections:
            lines.append(f"    - {yaml_escape(sec)}")
    else:
        lines.append("  sections: []")
    if frameworks:
        lines.append("  frameworks:")
        for fw in frameworks:
            lines.append(f"    - {yaml_escape(fw)}")
    else:
        lines.append("  frameworks: []")
    return "\n".join(lines)


def build() -> str:
    out: list[str] = []
    out.append("# Auto-generated machine-readable taxonomy for the GRC Documentation Library.")
    out.append("# Source of truth: the canonical metadata block and body structure of each artefact.")
    out.append("# Regenerate with `python3 tools/build-taxonomy.py`.")
    out.append("# Do not edit this file by hand.")
    out.append("")
    out.append("schema_version: 1")
    out.append("generated_by: tools/build-taxonomy.py")
    out.append("documents:")
    docs = iter_all_docs()
    # Pre-pass: every document title, so a framework chip that is really an
    # internal library-document cross-reference (its exact title) is dropped.
    titles = frozenset(
        t for t in (extract_metadata(d.read_text(encoding="utf-8")).get("Document Title", "").strip()
                    for d in docs) if t
    )
    for d in docs:
        out.append(emit_doc(d, titles))
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
