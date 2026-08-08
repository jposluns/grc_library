#!/usr/bin/env python3
"""Reject a PR whose delta touches BOTH narrative content and a corpus document (D11, mixed-diff).

This is a CI-only PR-time delta check, not part of the corpus audit programme
(the corpus gates check repository state at HEAD; this compares HEAD to the PR
merge-base). It is the pull-request-process half of the executive-narrative
one-way authority boundary specified in ``specification-executive-narrative.md``
Gates item 11 (collision-ledger and mixed-diff gate).

The boundary is one-way: a narrative page under ``executive/`` pins corpus
sources but must never EDIT corpus content, and a corpus document must never
reference ``executive/`` (the at-rest half is gate 87). This check closes the
PR-process seam: a single pull request that edits both a narrative content page
and a corpus document at once is exactly the shape in which a corpus edit could
ride in under narrative review (or vice versa), so it is rejected.

Scope, and why it is drawn this way:

- **Narrative content** is a changed ``.md`` under ``executive/`` OTHER than the
  ``executive/README.md`` entry point (the entry point is a listing/frame page,
  not authored narrative content, and is exempt from the narrative content
  gates too).
- **Corpus document** is a changed ``.md`` under a published-corpus domain
  directory (``CORPUS_DOMAINS`` = ``AUDITED_DOMAIN_DIRS`` minus
  ``.project-governance``, which build-taxonomy excludes as an operational, not
  published, tree), OR a root-level governed corpus document (a
  ``specification-*`` / ``instruction-*`` ``.md`` at the repository root, the
  prefix set gate 1 governs; this includes ``specification-executive-narrative.md``
  itself, a corpus document that is not a ``taxonomy.yml`` row). It deliberately
  does NOT count the root bookkeeping/meta surfaces every PR touches (``README.md``
  CalVer line, ``CHANGELOG.md``, ``NOTICE.md``, and the rest, none of which carry
  the governed prefixes) nor the generated registries (``taxonomy.yml``,
  ``narrative.yml``, ``docs/portal.md``, ``docs/maturity-scorecard.md``): a narrative-page PR must
  bump the root ``README.md`` CalVer, so counting a bookkeeping surface as a
  corpus document would trip this check on every legitimate narrative PR.

Interim posture (fail-closed, no override path):

The specification's item 11 calls for an "accountably-reviewed override marker
(never mere presence)". Designing what makes an override ACCOUNTABLE (the review
rule, not the marker's mere presence) is a governance-design decision reserved
to the maintainer. Until it is decided, this check is fail-closed with NO
override path: a mixed narrative+corpus diff is rejected outright. That is
stricter than the specified end state, never looser, so it is faithful to the
one-way boundary rather than contradicting it, and it has zero false-positive
surface while ``executive/`` holds no authored content pages. A mere-presence
override would contradict the specification's explicit "never mere presence"
requirement, so it is intentionally NOT implemented here; the accountable
override is added when its review rule is decided.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-narrative-corpus-mixed-diff-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-narrative-corpus-mixed-diff-on-pr.py origin/main
    python3 tools/check-narrative-corpus-mixed-diff-on-pr.py origin/main HEAD

    # Deterministic pure-logic self-test (no git, no refs):
    python3 tools/check-narrative-corpus-mixed-diff-on-pr.py --self-test

Exit codes:
    0 : the diff does not touch both surfaces (or is empty).
    1 : the diff touches BOTH a narrative content page and a corpus document.
    2 : invocation or environment error (cannot determine base/head, git failure),
        or a self-test failure.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from lint_common import (
    AUDITED_DOMAIN_DIRS,
    NARRATIVE_DIRS,
    PrRangeError,
    git,
    resolve_pr_range,
)

# The executive/ entry point: a listing/frame page, not authored narrative
# content, exempt from the narrative content gates and from this check.
NARRATIVE_ENTRY_POINT = "README.md"


def is_narrative_content(path: str) -> bool:
    """True for an authored narrative content page (``executive/*.md`` minus the
    top-level README entry point). The README exemption is PATH-SCOPED, not
    basename-keyed: only ``<narrative-dir>/README.md`` at the top level is exempt,
    so a nested ``executive/sub/README.md`` is still narrative content (spec item
    3: the README skip is path-scoped, not basename-keyed). PURE."""
    parts = path.split("/")
    return (
        len(parts) >= 2
        and parts[0] in NARRATIVE_DIRS
        and path.endswith(".md")
        and not (len(parts) == 2 and parts[-1] == NARRATIVE_ENTRY_POINT)
    )


# Corpus CONTENT scope for the boundary. The published-corpus domain set is
# AUDITED_DOMAIN_DIRS MINUS ``.project-governance``, which build-taxonomy.py
# excludes as "NOT a domain: it holds project-governance operational records, not
# the published deliverable"; treating those operational records as corpus content
# would be a false positive. Root-level governed corpus CONTENT documents (the
# specification-* / instruction-* files gate 1 governs by prefix, including
# specification-executive-narrative.md, a corpus document per the spec Gates item
# 2 that is not a taxonomy.yml row) are matched by prefix; the root
# bookkeeping/meta surfaces (README, CHANGELOG, NOTICE, CONTRIBUTING, AUTHORS,
# SECURITY, TODO, RESUME) carry none of those prefixes and are correctly excluded.
CORPUS_DOMAINS = frozenset(AUDITED_DOMAIN_DIRS) - {".project-governance"}
ROOT_CORPUS_PREFIXES = ("specification-", "instruction-")


def is_corpus_document(path: str) -> bool:
    """True for a corpus CONTENT document: a ``.md`` under a published-corpus
    domain directory (``CORPUS_DOMAINS``), or a root-level governed corpus document
    (a ``specification-*`` / ``instruction-*`` ``.md`` at the repository root).
    Excludes ``.project-governance`` operational records, the root
    bookkeeping/meta surfaces, and the generated registries by construction. PURE."""
    parts = path.split("/")
    if not path.endswith(".md"):
        return False
    if len(parts) >= 2 and parts[0] in CORPUS_DOMAINS:
        return True
    if len(parts) == 1 and path.startswith(ROOT_CORPUS_PREFIXES):
        return True
    return False


def evaluate(changed: list[str]) -> tuple[list[str], list[str]]:
    """Return ``(narrative_hits, corpus_hits)`` among the changed paths. PURE:
    the whole decision is a function of the file list, so it is testable without
    git and the thin git observer in ``main`` gathers and decides nothing."""
    narrative = [p for p in changed if is_narrative_content(p)]
    corpus = [p for p in changed if is_corpus_document(p)]
    return narrative, corpus


def _self_test() -> int:
    cases: list[tuple[str, list[str], bool]] = [
        # (name, changed_files, expect_violation)
        ("empty", [], False),
        ("narrative-only", ["executive/why-controls-matter.md"], False),
        ("corpus-only", ["risk/standard-risk-management.md"], False),
        ("both-flat", ["executive/why-controls-matter.md", "risk/standard-x.md"], True),
        ("both-nested-narrative", ["executive/sub/page.md", "governance/standard-y.md"], True),
        # README entry point is exempt: a corpus edit alongside ONLY the
        # executive README is not a narrative-content mixed diff.
        ("readme-entrypoint-plus-corpus", ["executive/README.md", "risk/standard-x.md"], False),
        # The mandatory root README CalVer bump on a narrative PR must NOT trip:
        # root README.md is not a corpus document.
        ("narrative-plus-root-readme", ["executive/page.md", "README.md"], False),
        # Generated registries / bookkeeping are not corpus documents.
        ("narrative-plus-taxonomy", ["executive/page.md", "taxonomy.yml"], False),
        ("narrative-plus-changelog", ["executive/page.md", "CHANGELOG.md"], False),
        ("narrative-plus-portal", ["executive/page.md", "docs/portal.md"], False),
        # tools/ is not a corpus content document.
        ("narrative-plus-tool", ["executive/page.md", "tools/x.py"], False),
        # A root governed corpus doc (specification-* / instruction-*) IS corpus
        # content, even the narrative spec itself (a corpus document per gate 1
        # that is not a taxonomy.yml row): a narrative page plus a root-spec edit
        # crosses the boundary.
        ("both-root-spec-executive", ["executive/page.md", "specification-executive-narrative.md"], True),
        ("both-root-spec-master", ["executive/page.md", "specification-master-project.md"], True),
        ("both-root-instruction", ["executive/page.md", "instruction-ai-document-ingestion.md"], True),
        # A root bookkeeping/meta .md (no specification-/instruction- prefix) is
        # NOT corpus content, so it does not trip the boundary.
        ("narrative-plus-root-security", ["executive/page.md", "SECURITY.md"], False),
        ("narrative-plus-root-notice", ["executive/page.md", "NOTICE.md"], False),
        # .project-governance/ holds operational records, NOT the published corpus
        # deliverable (build-taxonomy excludes it as "not a domain"), so a narrative
        # page plus a .project-governance edit is NOT a corpus-content mixed diff.
        ("dotproject-governance-not-corpus", ["executive/page.md", ".project-governance/record.md"], False),
        # F1: a NESTED executive README is authored narrative content (the exemption
        # is path-scoped to the top-level executive/README.md only).
        ("nested-narrative-readme-plus-corpus", ["executive/sub/README.md", "risk/x.md"], True),
        # A non-md executive file is not narrative content.
        ("executive-nonmd-plus-corpus", ["executive/assets/logo.svg", "risk/x.md"], False),
    ]
    failed = 0
    for name, changed, expect in cases:
        narrative, corpus = evaluate(changed)
        got = bool(narrative and corpus)
        if got != expect:
            failed += 1
            print(
                f"SELF-TEST FAIL [{name}]: expected violation={expect}, got={got} "
                f"(narrative={narrative}, corpus={corpus})",
                file=sys.stderr,
            )
    if failed:
        print(f"self-test: {failed} case(s) FAILED", file=sys.stderr)
        return 2
    print(f"self-test: all {len(cases)} mixed-diff cases passed.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reject a pull request whose delta touches both a narrative content "
            "page (executive/*.md minus the top-level README) and a corpus "
            "document (a .md under a published-corpus domain dir, i.e. the audited "
            "domains minus .project-governance, or a root specification-* / "
            "instruction-* governed corpus doc)."
        ),
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the deterministic pure-logic self-test and exit.",
    )
    parser.add_argument(
        "base",
        nargs="?",
        help=(
            "Base ref to diff against (default: origin/$GITHUB_BASE_REF in CI; "
            "must be supplied explicitly when running locally)."
        ),
    )
    parser.add_argument("head", nargs="?", default="HEAD", help="Head ref (default: HEAD).")
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return _self_test()

    try:
        merge_base, head = resolve_pr_range(args.base, args.head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        # --no-renames: a boundary-crossing rename is reported as delete+add so
        # BOTH sides are seen (default rename detection reports only the
        # destination, losing one side of a cross-boundary move). -z: NUL-delimited
        # raw paths, so a path containing a space, newline, or non-ASCII byte is
        # emitted verbatim rather than git-quoted and still classifies correctly.
        changed_raw = git("diff", "--name-only", "--no-renames", "-z", merge_base, head)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    changed = [entry for entry in changed_raw.split("\0") if entry]
    if not changed:
        print(f"OK: no files changed between {merge_base[:8]} and {head}.")
        return 0

    narrative, corpus = evaluate(changed)

    if narrative and corpus:
        print(
            "FAIL: this pull request touches BOTH narrative content and a corpus "
            "document, crossing the one-way executive-narrative authority boundary.",
            file=sys.stderr,
        )
        print("", file=sys.stderr)
        print("  Narrative content page(s):", file=sys.stderr)
        for p in narrative:
            print(f"    - {p}", file=sys.stderr)
        print("  Corpus document(s):", file=sys.stderr)
        for p in corpus:
            print(f"    - {p}", file=sys.stderr)
        print("", file=sys.stderr)
        print(
            "The narrative layer is one-way: a narrative page pins corpus sources "
            "but must not edit corpus content, and vice versa. Split the corpus "
            "change and the narrative change into separate pull requests.",
            file=sys.stderr,
        )
        return 1

    if narrative:
        print(f"OK: narrative content changed ({len(narrative)} page(s)); no corpus document touched.")
    elif corpus:
        print(f"OK: corpus document(s) changed ({len(corpus)}); no narrative content touched.")
    else:
        print(f"OK: {len(changed)} file(s) changed; neither surface touched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
