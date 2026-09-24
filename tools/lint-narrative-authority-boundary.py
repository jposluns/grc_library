#!/usr/bin/env python3
"""One-way narrative authority-boundary audit - grc wrapper over the pack engine.

The corpus is the sole normative surface and never references the narrative layer: no
corpus document metadata field or link, and no taxonomy.yml row, may reference the
executive/ narrative tree (the one-way authority boundary).

Engine/wrapper split (Group-A content-generic lane, Pattern A; narrative-family): the
PURE scan (the link regexes + _resolves_into_narrative + check_file +
check_taxonomy) is the source of record in the pack engine
(.corpus-management/tools/gate_lint_narrative_authority_boundary.py); it is
narrative-root-agnostic and takes the narrative root + its mention regexes via
configure(ref). This wrapper supplies the grc narrative root + corpus scan scope
(iter_markdown_files over the audited domains), configures the engine, and keeps the
self-test, main, module-global shims (check_file / check_taxonomy), and the exit codes.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import is_default_exempt_root, AUDITED_DOMAIN_DIRS, REPO_ROOT, guard_explicit_paths, positional_args, self_test_requested  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# The narrative directory: the target the direction rule forbids corpus
# documents from referencing.
NARRATIVE_ROOT = "executive"

# A plain-text / inline-code reference to the narrative tree inside a
# metadata FIELD value: ``executive/`` not preceded by a word character,
# dot, or hyphen (so ``chief-executive/`` or a hyphenated identifier never
# matches, while ``executive/x.md``, ``../executive/x.md`` and a backticked
# `executive/README.md` all do).
FIELD_MENTION_RE = re.compile(r"(?<![\w.-])executive/")

# taxonomy.yml is corpus-only by construction: any quoted executive/ path
# (a document row or a related_documents entry) is a defect.
TAXONOMY_MENTION_RE = re.compile(r"[\"'](?:\.\./)*executive/")

# Root-level deliverable documents (the published library specifications and
# front matter). Matches gate 53's root set PLUS the narrative authoring
# specification (deliberately in scope: it is a corpus document and must
# itself honour the one-way rule; it passes because its executive-path
# examples are inline-code prose; fenced blocks are scanned too, fail closed, 3b54).
ROOT_DELIVERABLE_DOCS: tuple[str, ...] = (
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "specification-executive-narrative.md",
    "instruction-ai-document-ingestion.md",
)

# Deliverable-corpus scan roots, derived from the single source of truth
# (adding a future audited domain propagates here; the scan-scope parity
# discipline forbids hardcoding the domain run).
DEFAULT_CORPUS_ROOTS: list[str] = [
    *(d for d in AUDITED_DOMAIN_DIRS if d != ".project-governance"),
    *ROOT_DELIVERABLE_DOCS,
]


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_narrative_authority_boundary  # the pack-owned engine (source of record)
    return gate_lint_narrative_authority_boundary


# Configure the engine ONCE with the grc narrative root + its derived mention regexes.
import types  # noqa: E402
_engine().configure(types.SimpleNamespace(
    narrative_root=NARRATIVE_ROOT, field_mention_re=FIELD_MENTION_RE,
    taxonomy_mention_re=TAXONOMY_MENTION_RE))


def check_file(path: Path, root: Path = REPO_ROOT) -> list[tuple[int, str]]:
    """Shim -> engine (engine already configured); kept module-global for the self-test + main."""
    return _engine().check_file(path, root)


def check_taxonomy(root: Path = REPO_ROOT) -> list[tuple[int, str]]:
    """Shim -> engine (engine already configured); kept module-global for the self-test + main."""
    return _engine().check_taxonomy(root)


def iter_markdown_files(paths: list[str], root: Path = REPO_ROOT) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = (root / p) if not Path(p).is_absolute() else Path(p)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(path.rglob("*.md"))
    # The narrative tree itself is never in the scan set (its corpus links
    # are the ALLOWED direction); guard explicit-path invocations too.
    kept = []
    for f in files:
        if is_default_exempt_root(f, repo_root=root):
            continue
        try:
            rel = f.resolve().relative_to(root.resolve())
            if rel.parts and rel.parts[0] == NARRATIVE_ROOT:
                continue
        except ValueError:
            pass  # a temp-dir fixture: in scope
        kept.append(f)
    return sorted(set(kept))


def _self_test() -> int:
    import tempfile

    failures: list[str] = []

    def expect(name: str, findings: list[tuple[int, str]], substr: str | None) -> None:
        msgs = [m for _, m in findings]
        if substr is None:
            if findings:
                failures.append(f"{name}: expected PASS, got {msgs}")
        elif not any(substr in m for m in msgs):
            failures.append(f"{name}: expected a finding containing {substr!r}, got {msgs}")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "risk").mkdir()
        (root / "executive").mkdir()
        (root / "governance" / "executive").mkdir(parents=True)

        def write(rel: str, content: str) -> Path:
            p = root / rel
            p.write_text(content, encoding="utf-8")
            return p

        # Clean corpus doc: corpus-to-corpus link, prose MENTION of executive/ in
        # backticks (legal).
        clean = write("risk/policy-a.md",
                      "# A\n\n**Document Title:** A\\\n**Related Documents:** "
                      "[`risk/annex-b.md`](annex-b.md)\n\n---\n\nSee `executive/README.md` for framing.\n")
        expect("clean-corpus-doc", check_file(clean, root), None)
        # FAIL CLOSED (3b54): a fenced example link into executive/ is scanned and flagged.
        fenced_link = write("risk/policy-fencedlink.md",
                            "# A\n\n---\n\n```markdown\n[`executive/brief-x.md`](../executive/brief-x.md)\n```\n")
        expect("fenced-link-flagged", check_file(fenced_link, root), "corpus-to-narrative link")

        # Fail-loud: an unreadable / non-UTF-8 corpus file is flagged, not skipped.
        unreadable = root / "risk" / "binary.md"
        unreadable.write_bytes(b"\xff\xfe not utf-8 \x00")
        expect("unreadable-corpus-failloud", check_file(unreadable, root), "not readable")
        unreadable.unlink()

        # Body link into executive/ (relative shape from a domain dir).
        bad_link = write("risk/policy-b.md",
                         "# B\n\n---\n\nExplained by [brief](../executive/brief-x.md).\n")
        expect("body-link-flagged", check_file(bad_link, root), "corpus-to-narrative link")

        # F1: a titled or angle-bracket body link must NOT fail open.
        titled = write("risk/policy-titled.md", "# T\n\n---\n\nExplained by [brief](../executive/brief-x.md \"Exec brief\").\n")
        expect("body-titled-link-flagged", check_file(titled, root), "corpus-to-narrative link")
        angle = write("risk/policy-angle.md", "# A\n\n---\n\nExplained by [brief](<../executive/brief-x.md>).\n")
        expect("body-angle-link-flagged", check_file(angle, root), "corpus-to-narrative link")
        # F1: a reference-STYLE link into executive/ (body ref use, ref-def below)
        # renders as a corpus-to-narrative link and must be flagged.
        ref_style = write("risk/policy-ref.md", "# R\n\n---\n\nExplained by [brief][n].\n\n[n]: ../executive/brief-x.md\n")
        expect("ref-style-link-flagged", check_file(ref_style, root), "corpus-to-narrative link")
        # F1 negative: a ref-def into a corpus doc, or an external URL, must pass.
        ref_clean = write("risk/policy-ref-clean.md", "# R\n\n---\n\nSee [b][n] and [x][h].\n\n[n]: ../risk/annex-b.md\n[h]: https://iso.org/x\n")
        expect("ref-style-clean-pass", check_file(ref_clean, root), None)
        # F1: a BLOCKQUOTED ref-def into executive/ still renders a link -> flag.
        bq_ref = write("risk/policy-bqref.md", "# R\n\n---\n\n> See [b][n].\n> [n]: ../executive/brief-x.md\n")
        expect("ref-style-blockquote-flagged", check_file(bq_ref, root), "corpus-to-narrative link")
        # F1 neg: a 4-space-indented ref-def is a CODE block, not a link -> pass.
        indent_ref = write("risk/policy-indentref.md", "# R\n\n---\n\n    [n]: ../executive/brief-x.md\n")
        expect("ref-style-indented-code-pass", check_file(indent_ref, root), None)
        # FAIL CLOSED (3b54): a ref-def inside a fence is scanned and flagged.
        fenced_ref = write("risk/policy-fencedref.md", "# R\n\n---\n\n~~~\n```\n[n]: ../executive/brief-x.md\n~~~\n")
        expect("ref-style-fenced-flagged", check_file(fenced_ref, root), "corpus-to-narrative link")

        # Root-doc link shape (no ../ prefix).
        bad_root = write("README.md", "# R\n\nSee [brief](executive/brief-x.md).\n")
        expect("root-link-flagged", check_file(bad_root, root), "corpus-to-narrative link")

        # Related Documents field carrying an executive/ link.
        bad_field = write("risk/policy-c.md",
                          "# C\n\n**Document Title:** C\\\n**Related Documents:** "
                          "[`executive/brief-x.md`](../executive/brief-x.md)\n\n---\n\nBody.\n")
        expect("related-documents-flagged", check_file(bad_field, root), "metadata field 'Related Documents'")

        # ANY field: a plain-text / inline-code mention inside a field value.
        bad_field2 = write("risk/policy-d.md",
                           "# D\n\n**Document Title:** D\\\n**Review Frequency:** "
                           "Upon change to `executive/README.md`\n\n---\n\nBody.\n")
        expect("any-field-mention-flagged", check_file(bad_field2, root), "metadata field 'Review Frequency'")

        # hyphenated non-match: chief-executive/ is not the narrative tree.
        hyphen = write("risk/policy-e.md",
                       "# E\n\n**Document Title:** E\\\n**Owner:** chief-executive/board liaison\n\n---\n\nBody.\n")
        expect("hyphenated-field-pass", check_file(hyphen, root), None)

        # Root-anchoring: a link into a NESTED dir named executive is not a finding.
        nested = write("risk/policy-f.md",
                       "# F\n\n---\n\nSee [doc](../governance/executive/note.md).\n")
        expect("nested-executive-link-pass", check_file(nested, root), None)

        # taxonomy.yml: an executive/ row or relationship target is a defect.
        write("taxonomy.yml",
              'documents:\n- path: "risk/policy-a.md"\n  related_documents:\n'
              '    - "executive/brief-x.md"\n')
        expect("taxonomy-flagged", check_taxonomy(root), "taxonomy.yml carries an executive/ target")
        write("taxonomy.yml", 'documents:\n- path: "risk/policy-a.md"\n  related_documents:\n    - "risk/annex-b.md"\n')
        expect("taxonomy-clean", check_taxonomy(root), None)

        # Scan-set guard: the executive/ tree is excluded even on explicit paths.
        write("executive/brief-x.md", "# X\n\n[corpus](../risk/policy-a.md)\n")
        files = iter_markdown_files([str(root / "executive"), str(root / "risk")], root)
        if any("executive" in f.parts for f in files):
            failures.append("scan-set-guard: executive/ file entered the scan set")

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all one-way authority-boundary cases passed (body link, root-doc link, "
          "Related Documents field, any-field mention, taxonomy row; hyphenated and "
          "nested-executive non-matches; prose mentions legal; fenced links flagged (fail closed); scan-set guard).")
    return 0


def main(argv: list[str]) -> int:
    explicit = positional_args(argv[1:])
    if self_test_requested(argv[1:], explicit):
        return _self_test()
    # 3b50: refuse (exit 2) a missing or out-of-tree explicit path; the check also reads this
    # checkout's taxonomy, so another tree's file cannot be judged soundly here.
    paths = guard_explicit_paths(explicit) if explicit else DEFAULT_CORPUS_ROOTS
    files = iter_markdown_files(paths)
    grouped: dict[str, list[tuple[int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f):
            try:
                display = f.relative_to(REPO_ROOT).as_posix()
            except ValueError:
                display = f.as_posix()
            grouped[display].append(finding)
            total += 1
    for finding in check_taxonomy():
        grouped["taxonomy.yml"].append(finding)
        total += 1

    if not grouped:
        print(f"OK: the authority boundary is one-way (no corpus document or taxonomy row "
              f"references {NARRATIVE_ROOT}/; {len(files)} corpus file(s) checked).")
        return 0
    print("One-way narrative authority-boundary audit FAILED:")
    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for lineno, message in grouped[relpath]:
            print(f"  L{lineno} {message}")
    print(f"\nFAIL: {total} corpus-to-narrative reference(s) across {len(grouped)} file(s). "
          "The corpus is the sole normative surface and never references the narrative "
          "layer; sever the reference (render-time derivation from the narrative "
          "registry is the only corpus-explained-by-narrative view).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
