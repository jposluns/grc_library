#!/usr/bin/env python3
"""One-way narrative authority-boundary gate (P-1.25 Phase 1.3; spec Gates item 7).

Enforces the source-level direction rule of
``specification-executive-narrative.md`` ("Related Documents on a narrative
page"): the authority boundary is ONE-WAY. A corpus document must never
reference the root ``executive/`` tree in any field, including Related
Documents; any corpus-explained-by-narrative view is derived at render time
from the narrative registry, never written into corpus source or into
``taxonomy.yml``. The reverse direction (a narrative page linking corpus
documents) is not merely allowed but mandatory, and is out of scope here.

Modelled on the corpus-to-project directional-dependency gate (gate 53,
``lint-directional-dependency.py``): a derived deliverable-corpus scan set,
fence-aware link detection, resolution relative to the source file, and a
root-anchored membership test on the resolved target.

Three checks per the spec's wording:

  1. LINK check (whole document, fence-aware): no markdown link in a
     deliverable-corpus document may resolve into the root ``executive/``
     tree. Root-anchored: a link into a NESTED directory merely named
     ``executive`` (e.g. ``governance/executive/``) is not a finding.
  2. FIELD check (metadata head window): no metadata field value may
     reference ``executive/`` even as plain text or inline code ("in any
     field" is broader than "as a link"). Body PROSE that discusses
     ``executive/`` in backticks stays legal (the authoring specification
     itself does this throughout); only field values and links are policed.
  3. TAXONOMY check (defence-in-depth): no ``taxonomy.yml`` row may carry an
     ``executive/`` path or relationship target. Making the taxonomy GENERATOR
     itself reject ``executive/`` targets at emission time (spec Gates item 7)
     is a separate, not-yet-built obligation; this state-level scan is the
     current enforcement point and backstop, failing loudly if an
     ``executive/`` target ever reaches ``taxonomy.yml``.

Scope: the deliverable corpus, DERIVED from ``lint_common.AUDITED_DOMAIN_DIRS``
minus ``.project-governance`` (project governance is not corpus; the
one-way rule subordinates the NARRATIVE layer to the CORPUS), plus the root
deliverable documents including the narrative authoring specification itself
(which passes: its executive-path examples are fenced or inline-code prose,
never links or field values).

Usage:
    python3 tools/lint-narrative-authority-boundary.py [paths...]
    python3 tools/lint-narrative-authority-boundary.py --self-test

Exit 0 when no corpus document references executive/; exit 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from lint_common import (
    AUDITED_DOMAIN_DIRS,
    REPO_ROOT,
    is_fence_line,
    parse_metadata_block,
    read_text_safe,
)

# The narrative directory: the target the direction rule forbids corpus
# documents from referencing.
NARRATIVE_ROOT = "executive"

# Match markdown links ``[text](target)``; external schemes skipped.
# Same patterns as gates 3 and 53.
# Link destination in ``](dest)``, ``](dest "title")``, or ``](<dest>)`` form:
# capture the destination token (up to whitespace, ")", or ">") without
# requiring the closing ")", so a titled or angle-bracket link cannot fail open.
LINK_RE = re.compile(r"\]\(\s*<?([^\s)>]+)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")

# Reference-style link DEFINITION: ``[label]: dest`` at line start (optionally
# ``<dest>``). A corpus doc that references executive/ via a ref-def (``[brief][n]``
# in the body, ``[n]: ../executive/brief-x.md`` below) renders as a corpus-to-narrative
# link but is NOT an inline ``](dest)`` match, so LINK_RE alone fails open. The
# line-start ``[label]:`` shape cannot collide with an inline ``[text](url)`` (``](``
# not ``]:``) or a body reference ``[text][label]``, so there is no double-count.
# 0-3 leading spaces only (4+ is an indented code block, not a link def), an
# optional blockquote prefix (a blockquoted ref-def still renders a link), then
# the label. Marker-aware fence tracking (below) excludes fenced ref-defs.
REF_DEF_RE = re.compile(r"^ {0,3}(?:>[ \t]?)*\[[^\]]+\]:\s*<?([^\s>]+)")

# Marker-aware fence parser (CommonMark): a fenced block closes only on the same
# marker char and a run length >= the opener, no info string; the shared
# ``is_fence_line`` toggle is marker-blind, so a ``` inside a ~~~ example would
# wrongly flip the scan and mis-read fenced content (a ref-def inside a fenced
# block is not a rendered link). Local to gate 87, mirroring gate 86.
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _fence_marker(line: str):
    m = _FENCE_RE.match(line)
    if not m:
        return None
    run = m.group(1)
    return run[0], len(run), m.group(2).strip()


def _closes(marker, opener) -> bool:
    return (marker is not None and marker[0] == opener[0]
            and marker[1] >= opener[1] and not marker[2])


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
# examples are fenced or inline-code prose).
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


def _resolves_into_narrative(source: Path, target: str, root: Path) -> bool:
    """True iff ``target`` (a link in ``source``) resolves into the ROOT
    ``executive/`` tree of ``root``. Root-anchored: a nested ``executive``
    directory elsewhere does not count."""
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return False  # pure-anchor link
    resolved = (source.parent / target_no_anchor).resolve()
    try:
        rel = resolved.relative_to(root.resolve())
    except ValueError:
        return False  # outside the repo: not the narrative tree
    return len(rel.parts) >= 1 and rel.parts[0] == NARRATIVE_ROOT


def check_file(path: Path, root: Path = REPO_ROOT) -> list[tuple[int, str]]:
    """(lineno, message) findings for one corpus document."""
    text = read_text_safe(path)
    if text is None:
        # Fail LOUD, not open: an unreadable corpus file cannot be cleared of
        # executive/ references (the 1.3a fail-loud lesson).
        return [(0, "not readable / not utf-8 (cannot be cleared of executive/ references; fail loud)")]
    findings: list[tuple[int, str]] = []

    # FIELD check: any metadata field value referencing executive/.
    block = parse_metadata_block(text)
    for field, value in block.fields.items():
        if FIELD_MENTION_RE.search(value):
            lineno = block.raw_lines[field][0]
            findings.append(
                (lineno,
                 f"metadata field {field!r} references executive/ (the authority "
                 f"boundary is one-way: no corpus field may reference the "
                 f"narrative tree, Related Documents included)")
            )

    # LINK check: any markdown link resolving into the root executive/ tree.
    open_fence = None  # marker-aware: (char, run-length); ``` inside ~~~ is content
    for lineno, raw in enumerate(text.splitlines(), 1):
        marker = _fence_marker(raw)
        if open_fence is not None:
            if _closes(marker, open_fence):
                open_fence = None
            continue
        if marker is not None:
            open_fence = (marker[0], marker[1])
            continue
        for m in LINK_RE.finditer(raw):
            target = m.group(1)
            if EXTERNAL.match(target):
                continue
            if _resolves_into_narrative(path, target, root):
                findings.append(
                    (lineno,
                     f"corpus-to-narrative link {target!r} (derive any "
                     f"corpus-explained-by-narrative view at render time from the "
                     f"narrative registry; never write it into corpus source)")
                )
        rd = REF_DEF_RE.match(raw)
        if rd:
            target = rd.group(1)
            if not EXTERNAL.match(target) and _resolves_into_narrative(path, target, root):
                findings.append(
                    (lineno,
                     f"corpus-to-narrative link {target!r} via reference definition "
                     f"(derive any corpus-explained-by-narrative view at render time "
                     f"from the narrative registry; never write it into corpus source)")
                )
    return findings


def check_taxonomy(root: Path = REPO_ROOT) -> list[tuple[int, str]]:
    """Defence-in-depth: no executive/ path may appear in taxonomy.yml."""
    tax = root / "taxonomy.yml"
    if not tax.is_file():
        return []
    text = read_text_safe(tax)
    if text is None:
        return [(0, "taxonomy.yml not readable / not utf-8 (cannot be checked for executive/ targets; fail loud)")]
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if TAXONOMY_MENTION_RE.search(line):
            findings.append(
                (lineno,
                 "taxonomy.yml carries an executive/ target (taxonomy.yml is "
                 "corpus-only by construction; the generator must reject "
                 "executive/ targets and no narrative row is ever added)")
            )
    return findings


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
        # backticks (legal), fenced example link into executive/ (legal).
        clean = write("risk/policy-a.md",
                      "# A\n\n**Document Title:** A\\\n**Related Documents:** "
                      "[`risk/annex-b.md`](annex-b.md)\n\n---\n\nSee `executive/README.md` for framing.\n"
                      "```markdown\n[`executive/brief-x.md`](../executive/brief-x.md)\n```\n")
        expect("clean-corpus-doc", check_file(clean, root), None)

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
        # F1 neg: a ref-def INSIDE a ~~~ fence (with an internal ```) is content -> pass.
        fenced_ref = write("risk/policy-fencedref.md", "# R\n\n---\n\n~~~\n```\n[n]: ../executive/brief-x.md\n~~~\n")
        expect("ref-style-fenced-pass", check_file(fenced_ref, root), None)

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
          "nested-executive non-matches; prose/fenced mentions legal; scan-set guard).")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _self_test()
    paths = [a for a in argv[1:] if not a.startswith("-")] or DEFAULT_CORPUS_ROOTS
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
