#!/usr/bin/env python3
"""Web-to-corpus link-target integrity (egress-free).

Reads the committed web corpus-link manifest (``.web/corpus-link-manifest.md``,
a generated artefact like ``taxonomy.yml`` / ``docs/portal.md``) and verifies
that every corpus-relative target it lists resolves to a file inside the
repository. It does NOT fetch any URL: it checks repository-internal targets
only, so it runs in CI and pre-commit with no network. It catches a corpus
document renamed or deleted without the website (and its manifest) being
regenerated, the class the taxonomy-derived page links and the curated
``llms.txt`` map both silently 404 on.

Manifest freshness (the committed manifest matching a fresh build) is a
separate concern, covered by ``.web/build.py --check`` and the website
paired-surface discipline; this gate only checks that what the manifest lists
still exists in the repo.

Usage:
    python3 tools/lint-web-corpus-links.py [--manifest PATH] [--self-test]

Exit codes: 0 clean; 1 on findings (or a usage/self-test failure).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lint_common import REPO_ROOT

DEFAULT_MANIFEST = REPO_ROOT / ".web" / "corpus-link-manifest.md"


def parse_manifest(text: str) -> list[tuple[int, str, str, str]]:
    """Return ``(row_no, target, location, link_text)`` for each data row of the
    manifest's Markdown table. Skips the header row, the ``|---|`` separator, and
    any non-table line. A data row is a pipe-delimited line with at least three
    cells whose first cell is a non-empty corpus-relative path."""
    rows: list[tuple[int, str, str, str]] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        target, location, link_text = cells[0], cells[1], cells[2]
        # Skip the header row and the separator row.
        if target.lower() in ("corpus target", "target"):
            continue
        if target and set(target) <= set("-: "):
            continue
        if not target:
            continue
        rows.append((lineno, target, location, link_text))
    return rows


def check(manifest_path: Path) -> list[tuple[int, str, str]]:
    """Return ``(row_no, target, reason)`` findings for every manifest target that
    does not resolve to an existing file inside the repository."""
    findings: list[tuple[int, str, str]] = []
    if not manifest_path.exists():
        return [(0, str(manifest_path), "manifest file missing")]
    text = manifest_path.read_text(encoding="utf-8")
    for row_no, target, location, _link_text in parse_manifest(text):
        resolved = (REPO_ROOT / target).resolve()
        try:
            resolved.relative_to(REPO_ROOT)
        except ValueError:
            findings.append((row_no, target, "resolves outside repo"))
            continue
        if not resolved.exists():
            findings.append((row_no, target, f"target does not exist (web location {location})"))
    return findings


def _self_test() -> int:
    """Inline cases: a resolving target passes, a missing target fails, and a
    ``../``-escape target fails. Uses real repo paths so no fixture files are
    written; the manifest text is built in memory and written to a temp file."""
    import tempfile

    manifest = (
        "| Corpus target | Website location | Link text |\n"
        "| --- | --- | --- |\n"
        "| taxonomy.yml | llms.txt | taxonomy.yml |\n"
        "| ai/does-not-exist-xyz.md | /ai/ | Missing doc |\n"
        "| ../../../etc/passwd | /ai/ | Escaped |\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(manifest)
        tmp = Path(fh.name)
    try:
        findings = check(tmp)
        reasons = {t: r for _, t, r in findings}
        ok = True
        if "taxonomy.yml" in reasons:
            print("FAIL self-test: a resolving target was flagged"); ok = False
        if "ai/does-not-exist-xyz.md" not in reasons:
            print("FAIL self-test: a missing target was not flagged"); ok = False
        if "../../../etc/passwd" not in reasons:
            print("FAIL self-test: an escaped target was not flagged"); ok = False
        if ok:
            print("self-test OK (3 cases: resolve passes, missing fails, escape fails)")
            return 0
        return 1
    finally:
        tmp.unlink()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=None,
                    help=f"manifest path (default: {DEFAULT_MANIFEST.relative_to(REPO_ROOT)})")
    ap.add_argument("--self-test", action="store_true", help="run inline cases and exit")
    args = ap.parse_args(argv[1:])

    if args.self_test:
        return _self_test()

    manifest_path = Path(args.manifest).resolve() if args.manifest else DEFAULT_MANIFEST
    findings = check(manifest_path)
    if not findings:
        print("OK: every web-to-corpus link target resolves.")
        return 0
    print(f"=== {manifest_path} ===")
    for row_no, target, reason in findings:
        print(f"  row {row_no} -> {target}  ({reason})")
    print(f"\nFAIL: {len(findings)} unresolved web-to-corpus target(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
