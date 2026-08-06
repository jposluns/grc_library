#!/usr/bin/env python3
"""Symmetric narrative-boundary gate (P-1.25 Phase 1.3; spec Gates item 3).

Enforces the two-sided placement boundary of
``specification-executive-narrative.md`` ("Placement and audit scope" and
Gates item 3). The boundary is mechanical, not conventional, and it is
SYMMETRIC:

  OUTSIDE the root ``executive/`` tree: no file may carry the
  ``Executive Narrative`` document type or ANY narrative-extension metadata
  field, anywhere in the repository, README paths INCLUDED. The corpus
  metadata gate's README skip is basename-keyed (any ``README.md`` gets only
  the loose title/license check), which is one of the two known escapes this
  gate closes; here nothing is keyed off the basename. The other closed
  escape is the retyped leak: a page renamed and retyped to a valid corpus
  Document Type that RETAINS narrative-extension fields passes the corpus
  metadata gate (which does not reject unknown fields) but fails here on the
  extension-field check.

  INSIDE the root ``executive/`` tree: every page must carry
  ``Document Type: Executive Narrative`` and the full 8-field
  narrative-extension block, and must NOT carry a corpus document type. The
  single named, PATH-scoped exemption is the entry point
  ``executive/README.md`` (the hand-curated concern framing, not a narrative
  page); a nested ``executive/<sub>/README.md`` is NOT exempt.

Scope notes:
  - The outside scan walks the whole repository (every ``.md`` outside the
    root ``executive/`` tree, minus the vendored/non-content dirs), so corpus
    domains, ``docs/``, ``guardrails/``, ``.project-governance/``, root
    files, ``tests/``, and every README are covered.
  - Detection is FENCE-AWARE: the authoring specification's example
    metadata block (a fenced illustration carrying the narrative type and
    all 8 extension fields) is documentation, not a leak, so lines inside
    fenced code blocks never match. This is why the specification itself
    needs no named exemption.
  - Detection is LINE-ANCHORED (``**Field:** ...`` at line start), matching
    the corpus metadata-field shape; prose that DISCUSSES a field name in a
    list item or sentence does not match.
  - Root-anchored classification: only the repository-root ``executive/``
    tree is "inside"; a nested directory merely named ``executive``
    (e.g. ``governance/executive/``) is OUTSIDE, per the ``is_narrative_root``
    precedent in ``lint_common``.

Honest residue (recorded in the spec, Gates item 3): a file stripped of both
its type marker and all narrative-only fields is not detectable by
repository-state rules and is covered by review only.

Deeper narrative-page validation (field order, closed vocabularies, pins,
hard breaks) is the narrative metadata gate's job (lint-narrative-metadata.py);
this gate proves only the boundary: type + extension-block presence and side.

Usage:
    python3 tools/lint-narrative-boundary.py [--root DIR]
    python3 tools/lint-narrative-boundary.py --self-test

Exit 0 when the boundary holds (an ``executive/`` tree holding only the
exempt entry-point README is a valid empty page set). Exit 1 on any finding.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import (
    METADATA_FIELD_RE,
    REPO_ROOT,
    read_text_safe,
)

# The boundary gate scans the WHOLE repository (both sides), minus only the
# vendored / non-content directories (NOT the shared corpus exempt-dir set):
# the spec's "outside executive/, anywhere in the repository" is repository-wide,
# so the pack and reference trees are scanned too. The line-anchored, fence-aware
# match flags only a real narrative metadata-field line, never a prose mention or
# a fenced example, so operational prose that discusses the fields never
# false-positives.
BOUNDARY_SKIP_DIRS = frozenset({".git", "node_modules", "__pycache__"})

NARRATIVE_DOCUMENT_TYPE = "Executive Narrative"
ENTRY_POINT = "executive/README.md"  # the single named, PATH-scoped exemption

# The 8 narrative-extension fields (spec, "Canonical metadata and narrative
# extension"). Presence of ANY of these outside executive/ is a defect;
# presence of ALL of them is required on every page inside executive/.
EXTENSION_FIELDS: tuple[str, ...] = (
    "Narrative Type",
    "Narrative Status",
    "Audience",
    "Corpus Sources",
    "External Sources",
    "Claim Classes Present",
    "Review Record",
    "Last Reviewed",
)

# The allowed corpus document types. Mirrors lint-metadata.py ALLOWED_TYPES;
# keeping the two in step is an integration-phase parity obligation (either a
# regression fixture or a hoist to lint_common). `Executive Narrative` must
# NEVER be added to the corpus set (spec: "No one may ever resolve the failure
# by adding the type"); this constant is the other half of that symmetry: no
# corpus type may appear inside executive/.
CORPUS_DOCUMENT_TYPES: frozenset[str] = frozenset(
    {
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
)

# Line-anchored narrative markers (the corpus metadata-field shape, with the
# optional trailing backslash hard-break marker).
NARRATIVE_TYPE_LINE_RE = re.compile(
    r"^\*\*Document Type:\*\*\s*" + re.escape(NARRATIVE_DOCUMENT_TYPE) + r"\s*\\?\s*$"
)
EXTENSION_FIELD_LINE_RE = re.compile(
    r"^\*\*(" + "|".join(re.escape(f) for f in EXTENSION_FIELDS) + r"):\*\*"
)


# Marker-aware fence parser (CommonMark): a fenced block closes only on a line
# using the SAME marker char and a run length >= the opener, with no info string.
# The shared ``is_fence_line`` predicate is a bare toggle (by design, for its many
# consumers), so a ``` line inside a ~~~ fence would wrongly close it; gate 86 needs
# marker-type tracking so a fenced example's metadata line is not a false leak.
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _fence_marker(line: str) -> tuple[str, int, str] | None:
    """(char, run-length, info-string) for a fence delimiter line, else None."""
    m = _FENCE_RE.match(line)
    if not m:
        return None
    run = m.group(1)
    return run[0], len(run), m.group(2).strip()


def _closes(marker: "tuple[str, int, str] | None", opener: "tuple[str, int]") -> bool:
    """True iff ``marker`` closes a block opened by ``opener`` (same char, length
    >= opener, no info string)."""
    return (marker is not None and marker[0] == opener[0]
            and marker[1] >= opener[1] and not marker[2])


def parse_metadata_run(text: str) -> dict[str, str]:
    """First-occurrence field values of the leading metadata run (the block
    ending at the first ``---`` or blank line after at least one field)."""
    fields: dict[str, str] = {}
    seen = False
    open_fence: "tuple[str, int] | None" = None
    for line in text.splitlines():
        # Fence-aware (marker-type-tracking): a fenced example block is not the
        # metadata run. A block closes only on the same marker char and length; a
        # mismatched fence inside it (``` inside a ~~~ block) is content.
        marker = _fence_marker(line)
        if open_fence is not None:
            if _closes(marker, open_fence):
                open_fence = None
            continue
        if marker is not None:
            open_fence = (marker[0], marker[1])
            continue
        stripped = line.strip()
        if seen and (stripped.startswith("---") or not stripped):
            break
        m = METADATA_FIELD_RE.match(line)
        if m:
            name, value = m.group(1).strip(), m.group(2).strip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            fields.setdefault(name, value)
            seen = True
    return fields


def scan_outside_file(path: Path, rel: str) -> list[str]:
    """The OUTSIDE side: reject narrative type / extension fields anywhere.

    Fence-aware and line-anchored (see module docstring). Applied to every
    ``.md`` outside the root ``executive/`` tree, README paths included."""
    text = read_text_safe(path)
    if text is None:
        return [f"{rel}: not readable / not utf-8 (a file outside executive/ that cannot be "
                f"read cannot be cleared of narrative markers; fail loud, not open)"]
    findings: list[str] = []
    open_fence: "tuple[str, int] | None" = None
    for lineno, line in enumerate(text.splitlines(), 1):
        marker = _fence_marker(line)
        if open_fence is not None:
            # inside a fenced block: closes only on the same marker char and a
            # length >= the opener with no info string; a mismatched fence
            # (``` inside a ~~~ block) is content, not a close.
            if _closes(marker, open_fence):
                open_fence = None
            continue
        if marker is not None:
            open_fence = (marker[0], marker[1])
            continue
        if NARRATIVE_TYPE_LINE_RE.match(line):
            findings.append(
                f"{rel}:L{lineno}: narrative document type {NARRATIVE_DOCUMENT_TYPE!r} "
                f"outside executive/ (a narrative page outside executive/ is a defect; "
                f"move the page, never retype it)"
            )
        m = EXTENSION_FIELD_LINE_RE.match(line)
        if m:
            findings.append(
                f"{rel}:L{lineno}: narrative-extension field {m.group(1)!r} outside "
                f"executive/ (extension fields are narrative-only; this closes the "
                f"retyped-leak escape of the corpus metadata gate)"
            )
    return findings


def check_inside_page(path: Path, rel: str) -> list[str]:
    """The INSIDE side: require the narrative type and the full extension
    block; reject corpus document types. Applied to every ``.md`` under the
    root ``executive/`` tree except the path-scoped ``executive/README.md``."""
    text = read_text_safe(path)
    if text is None:
        return [f"{rel}: not readable / not utf-8"]
    findings: list[str] = []
    meta = parse_metadata_run(text)
    dtype = meta.get("Document Type")
    if dtype in CORPUS_DOCUMENT_TYPES:
        findings.append(
            f"{rel}: corpus document type {dtype!r} inside executive/ (executive/ is "
            f"not a corpus domain; a corpus document may never live here)"
        )
    elif dtype != NARRATIVE_DOCUMENT_TYPE:
        findings.append(
            f"{rel}: every page under executive/ must carry Document Type "
            f"{NARRATIVE_DOCUMENT_TYPE!r}, got {dtype!r} (only the entry point "
            f"{ENTRY_POINT} is exempt, path-scoped)"
        )
    for fld in EXTENSION_FIELDS:
        if fld not in meta:
            findings.append(
                f"{rel}: missing narrative-extension field {fld!r} (every narrative "
                f"page carries the full 8-field extension block)"
            )
    return findings


def discover(root: Path) -> tuple[list[tuple[Path, str]], list[tuple[Path, str]]]:
    """(outside_files, inside_pages) as (path, rel) pairs; exempt dirs skipped,
    the entry point excluded from both sets (it is neither a corpus-side file
    nor a narrative page)."""
    outside: list[tuple[Path, str]] = []
    inside: list[tuple[Path, str]] = []
    for p in sorted(root.rglob("*.md")):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(root).parts
        if any(part in BOUNDARY_SKIP_DIRS for part in rel_parts):
            continue
        rel = "/".join(rel_parts)
        if rel_parts[0] == "executive":
            if rel == ENTRY_POINT:
                continue
            inside.append((p, rel))
        else:
            outside.append((p, rel))
    return outside, inside


def run(root: Path) -> list[str]:
    outside, inside = discover(root)
    findings: list[str] = []
    for p, rel in outside:
        findings.extend(scan_outside_file(p, rel))
    for p, rel in inside:
        findings.extend(check_inside_page(p, rel))
    return findings


def _self_test() -> int:
    """Synthetic per-failure-class fixtures (the live executive/ tree holds only
    the exempt entry-point README, so detection is proven synthetically;
    mirrors the narrative metadata gate's self-test discipline)."""
    import tempfile

    ext_block = "".join(
        f"**{f}:** x\\\n" for f in EXTENSION_FIELDS[:-1]
    ) + f"**{EXTENSION_FIELDS[-1]}:** 2026-08-05\n"
    valid_page = (
        "# Brief\n\n"
        "**Document Title:** Brief\\\n"
        "**Document Type:** Executive Narrative\\\n"
        "**License:** CC BY-SA 4.0\\\n" + ext_block + "\n---\n\nBody.\n"
    )
    corpus_page = (
        "# Policy\n\n"
        "**Document Title:** Policy\\\n"
        "**Document Type:** Policy\\\n"
        "**License:** CC BY-SA 4.0\n\n---\n\nBody.\n"
    )
    failures: list[str] = []

    def expect(name: str, findings: list[str], substr: str | None) -> None:
        if substr is None:
            if findings:
                failures.append(f"{name}: expected PASS, got {findings}")
        elif not any(substr in f for f in findings):
            failures.append(f"{name}: expected a finding containing {substr!r}, got {findings}")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # Integrated valid tree: exempt README + valid page inside, clean corpus
        # outside, a fenced narrative example outside (documentation, not a leak).
        (root / "executive").mkdir()
        (root / "executive" / "README.md").write_text("# Entry point\n\n**License:** CC BY-SA 4.0\n")
        (root / "executive" / "brief-good.md").write_text(valid_page)
        (root / "risk").mkdir()
        (root / "risk" / "policy-x.md").write_text(corpus_page)
        (root / "spec.md").write_text(
            "# Spec\n\nExample:\n\n```markdown\n**Document Type:** Executive Narrative\\\n"
            "**Narrative Type:** Scenario\\\n```\n\nProse: 1. **Narrative Type:** one of seven.\n"
        )
        expect("integrated-valid-tree", run(root), None)

        # Root-anchoring: a nested dir named executive is OUTSIDE (scanned as corpus side).
        (root / "governance" / "executive").mkdir(parents=True)
        (root / "governance" / "executive" / "brief-leak.md").write_text(valid_page)
        expect("nested-executive-is-outside", run(root), "outside executive/")
        (root / "governance" / "executive" / "brief-leak.md").unlink()

        # Nested README under executive/ is NOT exempt (path-scoped, not basename-keyed).
        (root / "executive" / "sub").mkdir()
        (root / "executive" / "sub" / "README.md").write_text("# Nested readme\n\n**License:** x\n")
        expect("nested-readme-not-exempt", run(root), "must carry Document Type")
        (root / "executive" / "sub" / "README.md").unlink()

        # F1: the pack/reference trees are SCANNED (not the shared corpus exempt set);
        # a narrative leak there is caught, while vendored dirs stay skipped.
        (root / ".claude").mkdir()
        (root / ".claude" / "leak.md").write_text(valid_page)
        expect("dotclaude-leak-scanned", run(root), "outside executive/")
        (root / ".claude" / "leak.md").unlink()
        (root / ".git").mkdir()
        (root / ".git" / "leak.md").write_text(valid_page)
        expect("dotgit-vendored-skipped", run(root), None)
        (root / ".git" / "leak.md").unlink()

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # OUTSIDE per-file checks.
        leak = root / "leak.md"
        leak.write_text(valid_page)
        expect("outside-full-leak-type", scan_outside_file(leak, "risk/leak.md"), "narrative document type")
        expect("outside-full-leak-ext", scan_outside_file(leak, "risk/leak.md"), "narrative-extension field")
        # README-path leak (the basename escape this gate closes).
        readme = root / "README.md"
        readme.write_text(valid_page)
        expect("outside-readme-leak", scan_outside_file(readme, "risk/README.md"), "narrative document type")
        # Retyped leak: valid corpus type, one retained extension field.
        retyped = root / "policy-retyped.md"
        retyped.write_text(corpus_page.replace(
            "**License:** CC BY-SA 4.0\n",
            "**License:** CC BY-SA 4.0\\\n**Corpus Sources:** [`risk/x.md`](x.md)\n",
        ))
        expect("outside-retyped-leak", scan_outside_file(retyped, "risk/policy-retyped.md"), "'Corpus Sources' outside")
        # Fenced example only: pass.
        fenced = root / "doc.md"
        fenced.write_text("```\n**Document Type:** Executive Narrative\\\n**Audience:** x\\\n```\n")
        expect("outside-fenced-pass", scan_outside_file(fenced, "docs/doc.md"), None)
        # F4: a ~~~-fenced block containing a ``` line + metadata must NOT toggle
        # out of code (the fence closes only on the same marker char), so the
        # metadata line is content, not a false leak.
        mixedfence = root / "mixed-fence.md"
        mixedfence.write_text("# D\n\nExample:\n\n~~~\n```\n**Document Type:** Executive Narrative\\\n**Audience:** x\\\n~~~\n\nProse.\n")
        expect("outside-mixed-fence-noescape", scan_outside_file(mixedfence, "docs/mixed-fence.md"), None)
        # Prose discussion (not line-anchored): pass.
        prose = root / "prose.md"
        prose.write_text("1. **Narrative Type:** one of the seven subtypes.\nThe **Audience:** value is fixed.\n")
        expect("outside-prose-pass", scan_outside_file(prose, "docs/prose.md"), None)
        # F3: an unreadable / non-UTF-8 file outside executive/ fails LOUD, not open.
        unreadable = root / "binary.md"
        unreadable.write_bytes(b"\xff\xfe not utf-8 \x00")
        expect("outside-unreadable-failloud", scan_outside_file(unreadable, "risk/binary.md"), "not readable")

        # INSIDE per-page checks.
        good = root / "brief-good.md"
        good.write_text(valid_page)
        expect("inside-valid", check_inside_page(good, "executive/brief-good.md"), None)
        corpus_inside = root / "policy-inside.md"
        corpus_inside.write_text(corpus_page)
        expect("inside-corpus-type", check_inside_page(corpus_inside, "executive/policy-inside.md"), "corpus document type")
        untyped = root / "brief-untyped.md"
        untyped.write_text(valid_page.replace("**Document Type:** Executive Narrative\\\n", ""))
        expect("inside-missing-type", check_inside_page(untyped, "executive/brief-untyped.md"), "must carry Document Type")
        noext = root / "brief-noext.md"
        noext.write_text(valid_page.replace("**Audience:** x\\\n", ""))
        expect("inside-missing-ext", check_inside_page(noext, "executive/brief-noext.md"), "missing narrative-extension field 'Audience'")
        # F2: a page whose only field-shaped lines sit inside a fence has NO real
        # metadata (the inside check is fence-aware), so it fails the type requirement.
        fenced_only = root / "brief-fenced.md"
        fenced_only.write_text("# Brief\n\n```markdown\n**Document Type:** Executive Narrative\\\n**Audience:** x\\\n```\n\nNo real metadata block.\n")
        expect("inside-fenced-metadata-only", check_inside_page(fenced_only, "executive/brief-fenced.md"), "must carry Document Type")

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all symmetric-boundary cases passed (outside: full leak, README-path leak, "
          "retyped leak, fenced/prose non-leaks; inside: corpus type, missing type, missing "
          "extension; root-anchoring and the path-scoped README exemption).")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _self_test()
    root = REPO_ROOT
    if "--root" in argv[1:]:
        root = Path(argv[argv.index("--root") + 1]).resolve()
    findings = run(root)
    if findings:
        for f in findings:
            print(f"  {f}")
        print(f"FAIL: {len(findings)} narrative-boundary finding(s). The boundary is symmetric: "
              f"narrative form only and always inside executive/ (sole exemption: {ENTRY_POINT}).")
        return 1
    outside, inside = discover(root)
    print(f"OK: symmetric narrative boundary holds ({len(outside)} outside file(s) carry no "
          f"narrative markers; {len(inside)} page(s) inside executive/ carry full narrative form).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
