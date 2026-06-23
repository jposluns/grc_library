#!/usr/bin/env python3
"""Authoring-time helper: which listing surfaces should a new document touch?

When a new document is added to the corpus, several listing surfaces
should be updated so the document is discoverable. This tool, run at
authoring time, reports them for a given document path, split into:

  MECHANICAL surfaces (hard-gated by lint-listing-surface-completeness.py
  and the taxonomy/portal sync gates): these MUST be updated or
  regenerated, and CI will fail otherwise. The tool reports, for each,
  whether the document is already present.

  SEMANTIC surfaces (matrices, crosswalks, glossary, Related Documents):
  these are relevance-based and are NOT gated. The tool emits a
  high-recall, ranked list of candidates for the author to ratify --
  it deliberately over-suggests rather than under-suggests, because a
  missed semantic surface is a silent gap whereas a spurious suggestion
  costs only a moment to dismiss.

Usage:
    python3 tools/suggest-listing-surfaces.py <doc-path> [<doc-path> ...]

    <doc-path> is a repository-relative path such as
    ``ai/standard-new-thing.md``. The document need not yet exist; the
    tool infers the domain from the path prefix and reads the document's
    metadata (title, type) if the file is present.

Exit codes: 0 always (advisory tool; it never fails a build). 2 on
usage error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe

REGISTER = "governance/register-document-index-and-classification.md"
PATH_IN_CODESPAN = re.compile(r"`([a-z][a-z0-9-]*(?:/[a-z0-9._-]+)+\.md)`")
TITLE_RE = re.compile(r"^\*\*Document Title:\*\*\s*(.+?)\s*\\?$", re.M)
TYPE_RE = re.compile(r"^\*\*Document Type:\*\*\s*(.+?)\s*\\?$", re.M)

# Words too common to be useful for keyword-overlap ranking.
STOPWORDS = frozenset(
    {
        "and",
        "the",
        "of",
        "for",
        "to",
        "a",
        "in",
        "on",
        "policy",
        "standard",
        "procedure",
        "template",
        "register",
        "framework",
        "guideline",
        "plan",
        "matrix",
        "annex",
        "charter",
        "management",
        "and-",
    }
)


def domain_of(path: str) -> str | None:
    return path.split("/", 1)[0] if "/" in path else None


def keywords(path: str) -> set[str]:
    """Salient keyword tokens from a document basename (no extension, no type prefix)."""
    stem = Path(path).stem
    tokens = {t for t in stem.split("-") if t and t not in STOPWORDS and len(t) > 2}
    return tokens


def find_matrix_surfaces() -> list[str]:
    """All matrix/crosswalk files in the corpus (the semantic listing surfaces)."""
    found: list[str] = []
    for p in sorted(REPO_ROOT.glob("**/*.md")):
        rel = p.relative_to(REPO_ROOT).as_posix()
        # Skip the working dir, the pack, generated docs.
        if rel.startswith((".working/", "dev-security/claude-rules/", "docs/", ".git/")):
            continue
        base = p.name
        if base.startswith("matrix-") or "crosswalk" in base:
            found.append(rel)
    return found


def referenced_paths(file_rel: str) -> set[str]:
    text = read_text_safe(REPO_ROOT / file_rel)
    if text is None:
        return set()
    return set(PATH_IN_CODESPAN.findall(text))


def report_one(doc_path: str) -> None:
    domain = domain_of(doc_path)
    exists = (REPO_ROOT / doc_path).is_file()
    title = doc_type = None
    if exists:
        text = read_text_safe(REPO_ROOT / doc_path) or ""
        m = TITLE_RE.search(text)
        title = m.group(1) if m else None
        m = TYPE_RE.search(text)
        doc_type = m.group(1) if m else None

    print(f"\n=== {doc_path} ===")
    if title:
        print(f"    title: {title}  (type: {doc_type or 'unknown'})")
    if domain is None:
        print(
            "    Root-level document (no domain prefix). The domain-index "
            "register and domain READMEs do not index root-level "
            "meta-specifications; no MECHANICAL listing surface applies. "
            "Confirm this is an intentional root-level document."
        )
        return

    # --- MECHANICAL surfaces (gated) ---
    print("  MECHANICAL surfaces (gated -- CI fails if not updated):")
    reg_listed = doc_path in referenced_paths(REGISTER)
    print(
        f"    [{'present' if reg_listed else 'MISSING'}] {REGISTER} "
        f"(add a row in the Active document index table)"
    )
    readme = f"{domain}/README.md"
    rm_listed = doc_path in referenced_paths(readme)
    print(
        f"    [{'present' if rm_listed else 'MISSING'}] {readme} "
        f"(add to the domain's document listing)"
    )
    print(
        "    [regenerate] taxonomy.yml, docs/portal.md, docs/maturity-scorecard.md "
        "-- run: python3 tools/build-taxonomy.py && python3 tools/build-portal.py"
    )

    # --- SEMANTIC surfaces (ranked candidates, not gated) ---
    kw = keywords(doc_path)
    candidates: list[tuple[int, str, str]] = []
    for surface in find_matrix_surfaces():
        if surface == doc_path:
            continue
        refs = referenced_paths(surface)
        if doc_path in refs:
            continue  # already mapped
        same_domain = sum(1 for r in refs if domain_of(r) == domain)
        surface_domain = domain_of(surface)
        # Score: a same-domain matrix is highly relevant; otherwise the
        # count of same-domain documents the matrix already maps is the
        # relevance signal; keyword overlap with the surface basename adds a point.
        score = same_domain
        reason_parts = []
        if surface_domain == domain:
            score += 100
            reason_parts.append("same-domain matrix")
        if same_domain:
            reason_parts.append(f"maps {same_domain} other {domain} doc(s)")
        if kw & keywords(surface):
            score += 1
            reason_parts.append("title-keyword overlap")
        if score > 0:
            candidates.append((score, surface, "; ".join(reason_parts) or "general matrix"))
    candidates.sort(key=lambda t: (-t[0], t[1]))

    print("  SEMANTIC surfaces (relevance-based -- ratify each; not gated):")
    if candidates:
        for score, surface, reason in candidates:
            print(f"    [consider] {surface}  ({reason})")
    else:
        print("    (no matrix/crosswalk currently maps this domain; check manually)")
    print(
        "    [consider] governance/register-glossary.md -- if the document "
        "introduces a new acronym or external-standard term."
    )
    print(
        "    [consider] the document's own 'Related Documents:' field -- link "
        "the documents this one depends on or elaborates."
    )


def main(argv: list[str]) -> int:
    docs = argv[1:]
    if not docs:
        print(__doc__)
        print("ERROR: provide at least one document path.", file=sys.stderr)
        return 2
    print(
        "Listing-surface suggestions. MECHANICAL surfaces are gated by "
        "lint-listing-surface-completeness.py (register + domain README) and "
        "the taxonomy/portal sync gates; SEMANTIC surfaces are advisory."
    )
    for doc_path in docs:
        report_one(doc_path.lstrip("./"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
