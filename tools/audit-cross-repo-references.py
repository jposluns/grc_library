#!/usr/bin/env python3
"""Advisory cross-repo / in-repo reference-existence audit (TODO section 1.22.4).

Scans every text file across the WHOLE repository (including the gate-exempt
``.claude/`` and ``.working/`` trees, which the corpus CI gates deliberately
skip) and classifies each reference, pointer, and path-like filename it finds
into one of four buckets:

  1. ``in-repo-exists``   a relative markdown link whose target resolves inside
                          this repository and exists on disk.
  2. ``in-repo-missing``  a relative markdown link whose target resolves inside
                          this repository but does NOT exist (a dangling link).
  3. ``cross-repo``       a pointer into a sibling repository
                          (``../grc_library_ref`` / ``../grc_library_scratch`` /
                          ``../grc_library_private`` or a bare
                          ``grc_library_ref`` / ``grc_library_scratch`` /
                          ``grc_library_private`` token). Each is sub-flagged
                          ``intended-minimal`` (a ref/scratch pointer, the two
                          siblings the public repo legitimately references) or
                          ``review-over-exposure`` (a ``_private`` pointer from a
                          public-tree file, which the section-1.19 privatization
                          wants minimized). When the named sibling is PRESENT, the
                          pointed-to path (if any) is additionally checked for
                          existence in the sibling; when it is ABSENT the existence
                          check no-ops (see below).
  4. ``ambiguous``        a relative markdown link that resolves OUTSIDE this
                          repository and is not a recognized sibling (an escaping
                          or otherwise unresolvable path-string), surfaced for a
                          human to adjudicate.

This tool is ADVISORY, NOT a CI gate. It spans gate-exempt trees, always exits 0
(a findings count is informational, never a build failure), and is intended to be
worker-run or run on demand, like ``/validate-pr``, not wired into the per-PR lint
CI. It reuses the existing machinery rather than reinventing it: the gate-3
link-extraction and path-resolution shapes from ``lint-links.py``, and
``lint_common``'s repository root, directory-exemption set, fenced-code-aware line
iterator, UTF-8-safe reader, and the section-1.19.2 sibling resolver
(``resolve_sibling`` / ``sibling_placeholder_present``).

Portable-clone degradation (TODO section 1.19.2 / the gate-70 pattern): the
CROSS-REPO EXISTENCE check routes its sibling lookup through
``resolve_sibling(name)``. In an adopter clone that reaches no sibling, that
returns ``None`` and the existence check for that sibling NO-OPS (the pointer is
still classified from its path string, but its target is reported
``sibling-absent (existence not verified)`` rather than raising). A present in-repo
``.<name>`` placeholder marks the ``None`` as the EXPECTED portable-clone state.
The in-repo classification (buckets 1, 2, 4) is sibling-independent and always runs.

Stdlib-only (gate 71). Python 3.11.

Usage:
    python3 tools/audit-cross-repo-references.py            # audit the live tree
    python3 tools/audit-cross-repo-references.py --self-test
    python3 tools/audit-cross-repo-references.py --root DIR # audit an explicit root
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    is_fence_line,
    read_text_safe,
    resolve_sibling as _default_resolve_sibling,
    sibling_placeholder_present,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories skipped even by this advisory (noise / non-text / stubs). NOTE this
# is INTENTIONALLY smaller than lint_common.DEFAULT_EXEMPT_DIRS: the whole point of
# this advisory is to cover the .claude/ and .working/ trees the corpus gates skip,
# so those two are NOT exempt here. The sibling-placeholder stubs stay exempt (they
# hold only a README by the gate-70 invariant).
SCAN_EXEMPT_DIRS: frozenset[str] = frozenset(
    {".git", "node_modules", "__pycache__", ".ref", ".scratch", ".private"}
)

# gate-3 (lint-links.py) link + external-scheme shapes, reused verbatim so this
# tool classifies exactly the link set the link gate resolves.
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")

# The three siblings of the public grc_library repo. A pointer naming any of these
# (either the full ``grc_library_<x>`` directory token or a ``../grc_library_<x>``
# path) is a cross-repo reference. ``grc_library_private`` is matched before the
# bare short names so the longest name wins.
_SIBLING_FULL = {
    "grc_library_ref": "ref",
    "grc_library_scratch": "scratch",
    "grc_library_private": "private",
}
CROSS_REPO_TOKEN = re.compile(
    r"(?:\.\./)?(grc_library_(?:ref|scratch|private))(/[^\s`)\]\"']*)?"
)

# Sibling short names whose pointers are the two the public repo legitimately
# references (the reference base and the worker-exchange). A ``private`` pointer is
# flagged for over-exposure review instead.
_INTENDED_SIBLINGS = frozenset({"ref", "scratch"})


def iter_text_files(root: Path) -> list[Path]:
    """Every UTF-8-readable file under ``root``, minus SCAN_EXEMPT_DIRS.

    Non-text (binary) files are dropped by the read step, not here; this returns
    the candidate path list in sorted order for deterministic output.
    """
    out: list[Path] = []
    for f in sorted(root.rglob("*")):
        if not f.is_file():
            continue
        if any(part in SCAN_EXEMPT_DIRS for part in f.relative_to(root).parts):
            continue
        out.append(f)
    return out


def classify_link(target: str, source: Path, root: Path) -> tuple[str, str]:
    """Classify a single (non-external, non-cross-repo) markdown link target.

    Returns ``(bucket, detail)`` where bucket is ``in-repo-exists``,
    ``in-repo-missing``, or ``ambiguous``. Resolution mirrors gate 3's
    ``resolve_link``: strip the ``#anchor``, resolve relative to the source
    file's directory, then require the result to be inside ``root`` and to exist.
    A pure-anchor link (no path) is treated as in-repo-exists (it targets the
    source file itself, which exists).
    """
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return "in-repo-exists", "(pure anchor)"
    resolved = (source.parent / target_no_anchor).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return "ambiguous", f"{target} (resolves outside repo)"
    if resolved.exists():
        return "in-repo-exists", target
    return "in-repo-missing", target


def classify_cross_repo(
    match: re.Match[str],
    source_rel_parts: tuple[str, ...],
    *,
    sibling_resolver=_default_resolve_sibling,
) -> tuple[str, str]:
    """Classify a cross-repo pointer match into ``(sub_flag, detail)``.

    ``sub_flag`` is ``intended-minimal`` (a ref/scratch pointer) or
    ``review-over-exposure`` (a ``_private`` pointer from a public-tree file; a
    pointer that itself lives under ``.working``/``.claude`` is treated as
    intended-minimal, since those trees are maintainer/AI operational state, not
    public corpus). When the named sibling RESOLVES (is present), a pointed-to
    sub-path is existence-checked in the sibling; when it does NOT resolve, that
    check NO-OPS and the detail records ``sibling-absent`` (the section-1.19.2
    portable-clone degradation, distinguishing an expected placeholder None).
    """
    full = match.group(1)
    name = _SIBLING_FULL[full]
    subpath = (match.group(2) or "").lstrip("/")
    in_operational_tree = bool({".working", ".claude"} & set(source_rel_parts))
    if name in _INTENDED_SIBLINGS or in_operational_tree:
        sub_flag = "intended-minimal"
    else:
        sub_flag = "review-over-exposure"

    # Sibling-reaching existence check (no-ops when the sibling is absent).
    sibling = sibling_resolver(name)
    if sibling is None:
        expected = sibling_placeholder_present(name)
        note = "sibling-absent, placeholder present" if expected else "sibling-absent"
        existence = f"{note} (existence not verified)"
    elif subpath:
        exists = (sibling / subpath).exists()
        existence = "target exists in sibling" if exists else "target MISSING in sibling"
    else:
        existence = "sibling present (bare pointer, no sub-path to check)"
    detail = f"{full}/{subpath}" if subpath else full
    return sub_flag, f"{detail} [{existence}]"


def audit_tree(
    root: Path, *, sibling_resolver=_default_resolve_sibling
) -> tuple[list[tuple[str, int, str, str, str]], Counter]:
    """Audit every text file under ``root``. Returns (findings, counts).

    Each finding is ``(rel_path, lineno, bucket, sub_or_detail, detail)``.
    ``counts`` is a Counter over the four top-level buckets plus the two cross-repo
    sub-flags. Markdown links are resolved for the in-repo buckets on ``.md`` files
    (link-existence is a markdown concern, exactly gate 3's scope); cross-repo
    tokens are scanned in EVERY text file (a ``_private`` mention in a ``.py`` or a
    ``.working`` note matters as much as one in a corpus doc).
    """
    findings: list[tuple[str, int, str, str, str]] = []
    counts: Counter = Counter()
    for path in iter_text_files(root):
        text = read_text_safe(path)
        if text is None:
            continue  # binary or non-UTF-8: skip
        rel = path.relative_to(root).as_posix()
        rel_parts = path.relative_to(root).parts
        is_md = path.suffix == ".md"
        in_code = False
        for lineno, raw in enumerate(text.splitlines(), start=1):
            line = raw.rstrip("\n")
            # Fenced-code skipping applies to markdown link extraction only
            # (a code fence in a .md documents link syntax, not a live link);
            # cross-repo token scanning runs on every line regardless.
            if is_md and is_fence_line(line):
                in_code = not in_code
                # A fence line itself carries no link/token of interest.
                continue

            # Cross-repo pointers (all files, all lines).
            for m in CROSS_REPO_TOKEN.finditer(line):
                sub_flag, detail = classify_cross_repo(
                    m, rel_parts, sibling_resolver=sibling_resolver
                )
                findings.append((rel, lineno, "cross-repo", sub_flag, detail))
                counts["cross-repo"] += 1
                counts[sub_flag] += 1

            # In-repo / ambiguous markdown links (.md, outside code fences).
            if is_md and not in_code:
                for m in LINK_RE.finditer(line):
                    target = m.group(1)
                    if EXTERNAL.match(target):
                        continue
                    if CROSS_REPO_TOKEN.search(target):
                        continue  # already counted as a cross-repo pointer
                    bucket, detail = classify_link(target, path, root)
                    findings.append((rel, lineno, bucket, "", detail))
                    counts[bucket] += 1
    return findings, counts


def _print_report(findings, counts, root: Path) -> None:
    print(f"Cross-repo / in-repo reference audit (advisory) for {root}")
    print("-" * 60)
    for bucket in ("in-repo-exists", "in-repo-missing", "cross-repo", "ambiguous"):
        print(f"  {bucket:<16} {counts.get(bucket, 0)}")
    print(f"    cross-repo intended-minimal      {counts.get('intended-minimal', 0)}")
    print(f"    cross-repo review-over-exposure  {counts.get('review-over-exposure', 0)}")
    # The actionable buckets get per-item detail; in-repo-exists is count-only
    # (it is the healthy majority and would drown the report).
    actionable = [f for f in findings if f[2] in ("in-repo-missing", "ambiguous")
                  or (f[2] == "cross-repo" and f[3] == "review-over-exposure")]
    if actionable:
        print("\nActionable items (dangling, ambiguous, or over-exposure review):")
        for rel, lineno, bucket, sub, detail in actionable:
            tag = f"{bucket}/{sub}" if sub else bucket
            print(f"  {rel}:{lineno}  [{tag}]  {detail}")
    else:
        print("\n(no dangling, ambiguous, or over-exposure-review items)")


def self_test() -> int:
    """Inline unit tests (kept behind --self-test, out of tests/, so the gate-36
    regression runner does not adopt this advisory tool as a gated test)."""
    import tempfile
    import unittest

    class AuditTests(unittest.TestCase):
        def _tree(self, td: str):
            root = Path(td)
            (root / "governance").mkdir(parents=True)
            # a real target so an in-repo link resolves
            (root / "governance" / "real.md").write_text("x", encoding="utf-8")
            return root

        def test_in_repo_exists_and_missing(self):
            with tempfile.TemporaryDirectory() as td:
                root = self._tree(td)
                (root / "governance" / "doc.md").write_text(
                    "See [real](real.md) and [gone](nope.md).\n", encoding="utf-8"
                )
                findings, counts = audit_tree(root, sibling_resolver=lambda n: None)
                self.assertEqual(counts.get("in-repo-exists", 0), 1)
                self.assertEqual(counts.get("in-repo-missing", 0), 1)
                self.assertTrue(
                    any(b == "in-repo-missing" and "nope.md" in d
                        for _, _, b, _, d in findings)
                )

        def test_cross_repo_pointer_and_over_exposure(self):
            with tempfile.TemporaryDirectory() as td:
                root = self._tree(td)
                # a public-tree file pointing at _private = over-exposure review;
                # a ref pointer = intended-minimal.
                (root / "governance" / "doc.md").write_text(
                    "prep in `grc_library_private/x.md`; base ../grc_library_ref/catalogue.yml\n",
                    encoding="utf-8",
                )
                findings, counts = audit_tree(root, sibling_resolver=lambda n: None)
                self.assertEqual(counts.get("cross-repo", 0), 2)
                self.assertEqual(counts.get("review-over-exposure", 0), 1)
                self.assertEqual(counts.get("intended-minimal", 0), 1)

        def test_sibling_absent_no_op(self):
            # The sibling-reaching existence check must NO-OP (not raise) when the
            # sibling resolver returns None (the portable-clone / adopter case).
            with tempfile.TemporaryDirectory() as td:
                root = self._tree(td)
                (root / "governance" / "doc.md").write_text(
                    "base ../grc_library_ref/catalogue.yml\n", encoding="utf-8"
                )
                findings, counts = audit_tree(root, sibling_resolver=lambda n: None)
                self.assertEqual(counts.get("cross-repo", 0), 1)
                self.assertTrue(
                    any("sibling-absent" in d for _, _, b, _, d in findings
                        if b == "cross-repo")
                )

        def test_sibling_present_existence_check(self):
            # When the sibling resolves, a pointed-to sub-path is existence-checked.
            with tempfile.TemporaryDirectory() as td:
                root = self._tree(td)
                sib = Path(td) / "sibling_ref"
                (sib / "sub").mkdir(parents=True)
                (sib / "sub" / "here.md").write_text("y", encoding="utf-8")
                (root / "governance" / "doc.md").write_text(
                    "a ../grc_library_ref/sub/here.md and ../grc_library_ref/sub/gone.md\n",
                    encoding="utf-8",
                )
                findings, _ = audit_tree(root, sibling_resolver=lambda n: sib)
                details = [d for _, _, b, _, d in findings if b == "cross-repo"]
                self.assertTrue(any("target exists in sibling" in d for d in details))
                self.assertTrue(any("target MISSING in sibling" in d for d in details))

        def test_external_and_fenced_skipped(self):
            with tempfile.TemporaryDirectory() as td:
                root = self._tree(td)
                (root / "governance" / "doc.md").write_text(
                    "[ext](https://github.com)\n```\n[fenced](nope.md)\n```\n",
                    encoding="utf-8",
                )
                _, counts = audit_tree(root, sibling_resolver=lambda n: None)
                # external skipped; the fenced dangling link skipped.
                self.assertEqual(counts.get("in-repo-missing", 0), 0)
                self.assertEqual(counts.get("in-repo-exists", 0), 0)

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AuditTests)
    )
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(REPO_ROOT),
                    help="repository root to audit (default: this repo)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline unit tests and exit")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    root = Path(args.root).resolve()
    findings, counts = audit_tree(root)
    _print_report(findings, counts, root)
    # Advisory: always exit 0. The counts are informational; this tool never
    # fails a build (it spans gate-exempt trees and is not a CI gate).
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
