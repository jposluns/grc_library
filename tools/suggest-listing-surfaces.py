#!/usr/bin/env python3
"""Authoring-time helper: which listing surfaces should a new document touch?

When a new document is added to the corpus, several listing surfaces
should be updated so the document is discoverable. This tool, run at
authoring time, reports them for a given document path, split into:

  MECHANICAL surfaces (hard-gated by lint-listing-surface-completeness.py
  and the generator --check stages of tools/pre-push-guard.sh): these MUST
  be updated or regenerated, and CI will fail otherwise. The tool reports,
  for each hand-edited surface, whether the document is already present.
  The regenerate list is DERIVED from the guard, never hand-listed: every
  ``python3 <script>.py --check`` stage line in the guard and in the runner
  scripts it chains (``tools/*.sh``) is a generator, and each one not in
  NOT_TRIGGERED_BY_NEW_DOCUMENT is listed, so a generator added to the
  guard joins this list without an edit here (SuggestListingSurfacesTests
  fails when a guard generator is neither derived nor recorded there).

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

import ast
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import is_default_exempt_root, REPO_ROOT, positional_args  # noqa: E402  # grc-config/store, stays local

REGISTER = "governance/register-document-index-and-classification.md"
PATH_IN_CODESPAN = re.compile(r"`([a-z][a-z0-9-]*(?:/[a-z0-9._-]+)+\.md)`")
TITLE_RE = re.compile(r"^\*\*Document Title:\*\*\s*(.+?)\s*\\?$", re.M)
TYPE_RE = re.compile(r"^\*\*Document Type:\*\*\s*(.+?)\s*\\?$", re.M)

GUARD = "tools/pre-push-guard.sh"
# A guard stage that runs a runner script: a bare `tools/<name>.sh` line.
GUARD_RUNNER_RE = re.compile(r"^\s*(tools/[a-z0-9_-]+\.sh)\s*$")
# A generator drift check: a whole line `python3 [-I ...] <script>.py [flags]`
# (optionally in the runner's `run_gate "<name>"` grammar, the one gate parity
# parses) whose flags include --check. Anchored, so a check inside $(...) or an
# if-test is not a stage (the guard's reference-manifest ADVISORY is one; it is
# recorded below).
CHECK_STAGE_RE = re.compile(
    r'^\s*(?:run_gate\s+"[^"]+"\s+)?python3(?:\s+-\w+)*\s+([\w./-]+\.py)((?:\s+--[a-z][a-z-]*)*)\s*$'
)
# Generators the guard runs whose inputs a new corpus or executive/ document
# does not change, with the reason. A generator the guard runs that is neither
# listed here nor derived as a stage fails SuggestListingSurfacesTests.
NOT_TRIGGERED_BY_NEW_DOCUMENT = {
    "tools/build-todo-number-allocation.py": "reads TODO.md, TODO-REFERENCE.md and tools/todo-number-floor.json",
    "tools/build-relationship-model.py": "reads governance/relationship-model-source.json",
    "tools/build-corpus-management.py": "reads the .corpus-management/ sources",
    "tools/build-citation-publishers.py": "reads the citation-publishers block of "
    "governance/specification-citation-verification.md",
    "tools/build-reference-manifest.py": "advisory guard check over the grc_library_ref sibling; never blocks",
}
# Generators whose inputs are executive/ narrative pages only, and those whose
# inputs are corpus metadata only (taxonomy.yml is corpus-only by construction).
# Any other derived generator applies to both.
NARRATIVE_ONLY = frozenset({"tools/build-narrative-registry.py"})
CORPUS_ONLY = frozenset({"tools/build-taxonomy.py", "tools/build-portal.py"})
# Generators a sound derivation must find (when present in the tree): a readable
# guard that yields a list without one of them was restructured past the parser,
# so the helper reports [unknown] rather than a silently partial list.
ANCHORS = ("tools/build-taxonomy.py", "tools/build-portal.py", ".web/build.py")
# Display only: the committed outputs a generator rewrites. A generator absent
# from this map is still listed, with a generic note.
OUTPUTS = {
    "tools/build-taxonomy.py": "taxonomy.yml",
    "tools/build-portal.py": "docs/portal.md, docs/maturity-scorecard.md",
    "tools/build-narrative-registry.py": "narrative.yml",
    ".web/build.py": ".web/corpus-link-manifest.md",
}
# taxonomy.yml indexes only the root-level files named in this builder's iter_all_docs().
TAXONOMY_BUILDER = "tools/build-taxonomy.py"

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
        if is_default_exempt_root(p, repo_root=REPO_ROOT):
            continue
        rel = p.relative_to(REPO_ROOT).as_posix()
        # Skip the working dir, the pack, generated docs.
        if rel.startswith((".working/", "guardrails/", "docs/", ".git/")):
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


def guard_generators(root: Path = REPO_ROOT) -> list[str] | None:
    """Scripts of the generator --check stages the pre-push guard runs, in run order.

    Walks the guard line by line, expanding each runner-script stage
    (``tools/<name>.sh``) in place, and keeps each ``python3 <script>.py ...
    --check`` stage whose script exists (the guard skips an absent
    .web/build.py). None when the guard or a runner it names cannot be read
    (absent, unreadable, or not UTF-8).
    """
    found: list[str] = []

    def walk(rel: str, expand_runners: bool) -> bool:
        path = root / rel
        try:
            text = read_text_safe(path) if path.is_file() else None
        except OSError:  # read_text_safe surfaces filesystem errors; this helper is advisory
            text = None
        if text is None:
            return False
        for line in text.splitlines():
            m = GUARD_RUNNER_RE.match(line)
            if m and expand_runners:
                if not walk(m.group(1), False):
                    return False
                continue
            m = CHECK_STAGE_RE.match(line)
            if m and "--check" in m.group(2).split():
                script = m.group(1)
                if script not in found and (root / script).is_file():
                    found.append(script)
        return True

    return found if walk(GUARD, True) else None


def indexed_root_documents(root: Path = REPO_ROOT) -> tuple[str, ...] | None:
    """Root-level files tools/build-taxonomy.py indexes, read from its source.

    Parses the builder (never imports it) and returns the string-literal tuple that a
    ``for`` loop in ``iter_all_docs()`` walks. None when the builder cannot be read or
    parsed, or no such loop is found.
    """
    path = root / TAXONOMY_BUILDER
    try:
        text = read_text_safe(path) if path.is_file() else None
        tree = ast.parse(text) if text is not None else None
    except (OSError, SyntaxError, ValueError):  # advisory helper: report unknown, never crash
        return None
    if tree is None:
        return None
    for fn in tree.body:
        if not (isinstance(fn, ast.FunctionDef) and fn.name == "iter_all_docs"):
            continue
        for node in ast.walk(fn):
            if (
                isinstance(node, ast.For)
                and isinstance(node.iter, ast.Tuple)
                and node.iter.elts
                and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.iter.elts)
            ):
                return tuple(e.value for e in node.iter.elts)
    return None


def report_regenerate(domain: str | None) -> None:
    generators = guard_generators()
    if generators is not None and any(
        a not in generators and (REPO_ROOT / a).is_file() for a in ANCHORS
    ):
        generators = None  # a partial derivation is reported as unknown, never listed
    if generators is None:
        print(
            f"    [unknown] could not read the generator stages from {GUARD} or a runner "
            f"it chains; run {GUARD} before pushing and regenerate whatever it reports stale."
        )
        return
    skip = CORPUS_ONLY if domain == "executive" else NARRATIVE_ONLY
    regen = [g for g in generators if g not in NOT_TRIGGERED_BY_NEW_DOCUMENT and g not in skip]
    if not regen:
        print(f"    [regenerate] none -- no generator stage in {GUARD} applies.")
        return
    outputs = ", ".join(OUTPUTS.get(g, f"the committed outputs of {g}") for g in regen)
    print(
        f"    [regenerate] {outputs} -- run: "
        + " && ".join(f"python3 {g}" for g in regen)
        + f" (derived from the --check stages of {GUARD}; commit the outputs with the document)"
    )


def report_one(doc_path: str) -> None:
    if is_default_exempt_root(doc_path, repo_root=REPO_ROOT):
        print(f"\n=== {doc_path} ===")
        print("    Source-pack path outside the corpus; no listing surfaces apply.")
        return
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
            "meta-specifications, so no hand-edited MECHANICAL surface applies. "
            "Confirm this is an intentional root-level document."
        )
        indexed = indexed_root_documents()
        if indexed is None:
            print(
                f"    [unknown] could not read the root specifications iter_all_docs() in "
                f"{TAXONOMY_BUILDER} indexes; check whether it names {doc_path} before regenerating."
            )
        elif doc_path in indexed:
            print("    taxonomy.yml indexes it (domain \"root\"), so the corpus generators apply.")
            report_regenerate(domain)
        else:
            print(
                f"    [add] {TAXONOMY_BUILDER} indexes only its named root specifications "
                f"({', '.join(indexed)}), so taxonomy.yml does not index this document and "
                f"regenerating does nothing for it. First add it to the root-file list in "
                f"iter_all_docs() in {TAXONOMY_BUILDER}; the regenerate line then applies "
                f"(rerun this tool)."
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
    if (REPO_ROOT / readme).is_file():
        rm_listed = doc_path in referenced_paths(readme)
        print(
            f"    [{'present' if rm_listed else 'MISSING'}] {readme} "
            f"(add to the domain's document listing)"
        )
    else:
        # No README for this first-path-segment: it is not a real corpus domain
        # (e.g. docs/, a root meta-dir) or the domain's README is missing. An
        # advisory tool must not crash (read_text_safe does not swallow a
        # FileNotFoundError, by design), so report it instead of reading a
        # non-existent file.
        print(
            f"    [n/a] {readme} does not exist -- '{domain}/' is not a corpus "
            f"domain with a README (no MECHANICAL domain-README surface applies)."
        )
    report_regenerate(domain)

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
    # 3b50b2e2: a flag-like token used to be treated as a document name; parse strictly (use '--'
    # before a path that begins with '-'). A path that does not exist yet stays valid: this tool
    # plans listing surfaces for PROPOSED documents (SuggestListingSurfacesTests).
    docs = positional_args(argv[1:], known_flags=())
    if not docs:
        print(__doc__)
        print("ERROR: provide at least one document path.", file=sys.stderr)
        return 2
    print(
        "Listing-surface suggestions. MECHANICAL surfaces are gated by "
        "lint-listing-surface-completeness.py (register + domain README) and "
        f"the generator --check stages of {GUARD}; SEMANTIC surfaces are advisory."
    )
    for doc_path in docs:
        report_one(doc_path.lstrip("./"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
