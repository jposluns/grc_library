#!/usr/bin/env python3
"""CHANGELOG-hygiene first-commit pre-flight aid (TODO P4.14).

A gating helper run BEFORE the first commit of any PR that edits the
CHANGELOG, as:

    python3 tools/preflight-changelog.py && git commit ...

It exits non-zero (so the ``&&`` chain will not fire) when the working-tree
additions to the root [`CHANGELOG.md`] or its detailed mirror
[`.working/changelog-details/CHANGELOG-detailed.md`] contain either:

  - an em-dash or en-dash in prose (the no-dash convention: delta gate D3
    enforces this PR-time on the root file, and gate 51 enforces it on the
    ``.working/`` mirror, but NEITHER fires on the first local commit), or
  - a path-shaped backtick code span that is not wrapped in a markdown link
    (the link-coverage convention that ``lint-changelog-link-coverage.py``
    enforces post-commit on the root file).

This is a developer AID, not a new audit gate. The authoritative gates
(D3, gate 51, the link-coverage gate) remain and run in CI and
``run_all_audits.sh`` / ``run-pr-time-checks.sh``; this aid only moves their
diagnosis earlier, to before the first commit, closing the recurring
commit-then-amend loop (improvement-log #341/#347/#349/#355). Because no
pre-commit git hook fires on commits in this environment, a standalone
helper invoked in an ``&&`` chain is the form that actually gates the
commit; a pre-commit hook would not run.

The check is scoped to the lines a PR ADDS (``git diff`` against HEAD), so
historical entries that predate the conventions never false-alarm. Dash
detection strips inline code spans first (a regex character class or a
quoted format literal may legitimately contain a dash), matching gate 51.

Known limitation: because the aid scans the added diff-lines in isolation,
it does NOT track fenced (```` ``` ````) code-block state the way the
authoritative link-coverage gate does (that gate skips path-shaped spans
inside fenced blocks). A path-shaped span added inside a fenced block in a
CHANGELOG entry would therefore make this aid exit 1 (over-block) where the
gate exits 0. The divergence fails safe (it over-blocks the author's own
commit; it never lets a defect through) and is latent (CHANGELOG entries do
not currently use fenced blocks), so full fenced-block tracking is left
unimplemented; if a CHANGELOG entry ever needs a fenced path-span, run the
commit without the aid and rely on the authoritative gate.

Usage:
    python3 tools/preflight-changelog.py            # working tree vs HEAD
    python3 tools/preflight-changelog.py --staged   # staged diff only

Exit codes:
    0   no dash or unlinked-reference issue in the added CHANGELOG lines
    1   one or more issues (do not commit until fixed)
    2   git invocation error
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CHANGELOG_FILES = (
    "CHANGELOG.md",
    ".working/changelog-details/CHANGELOG-detailed.md",
)

EM_DASH = "—"
EN_DASH = "–"

# Inline code-span stripper: a run of N backticks, the shortest content, then
# a closing run of N backticks (the standard CommonMark code-span shape). Same
# approach as gate 51 (lint-working-prose-hygiene.py), so a dash that is
# legitimately inside a code span (a regex character class, a quoted format
# literal) is treated as content, not prose.
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")

# --- File-reference recognition, mirrored from lint-changelog-link-coverage.py ---
# Kept in step with that gate (the authoritative post-commit check); this aid
# only surfaces the same class earlier. If the gate's logic changes, update
# this block to match.
FILE_EXTENSIONS = (
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".cff",
    ".toml",
)
TOP_LEVEL_FILES = {
    "README.md",
    "CHANGELOG.md",
    "NOTICE.md",
    "LICENSE",
    "CITATION.cff",
    "AUTHORS.md",
    "TODO.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "taxonomy.yml",
    ".pre-commit-config.yaml",
    "specification-ingestion.md",
    "specification-master-project.md",
}


def looks_like_file_reference(text: str) -> bool:
    if "/" in text and text.endswith(FILE_EXTENSIONS):
        return True
    if text in TOP_LEVEL_FILES:
        return True
    if "/" not in text and text.endswith(FILE_EXTENSIONS):
        base = text[: text.rindex(".")]
        if base and re.match(r"^\.?[A-Za-z0-9][A-Za-z0-9_\-.]*$", base):
            return True
    return False


def unlinked_refs_in_line(line: str) -> list[str]:
    """Return path-shaped backtick spans on a line that are NOT wrapped in a
    markdown link. Mirrors the per-line walk in lint-changelog-link-coverage.py."""
    findings: list[str] = []
    i = 0
    while i < len(line):
        # Skip an already-linked reference: [`...`](...)
        if line[i] == "[" and i + 1 < len(line) and line[i + 1] == "`":
            close = line.find("](", i + 2)
            if close != -1:
                paren_close = line.find(")", close + 2)
                if paren_close != -1:
                    i = paren_close + 1
                    continue
        if line[i] != "`":
            i += 1
            continue
        end = line.find("`", i + 1)
        if end == -1:
            break
        inner = line[i + 1 : end]
        if looks_like_file_reference(inner):
            findings.append(inner)
        i = end + 1
    return findings


def added_lines(staged: bool) -> list[tuple[str, str]]:
    """Return (file, added-line-text) for every line the working tree (or the
    staged diff) adds to a CHANGELOG file relative to HEAD."""
    cmd = ["git", "diff", "--unified=0"]
    if staged:
        cmd.append("--cached")
    cmd += ["HEAD", "--", *CHANGELOG_FILES]
    out = subprocess.check_output(cmd, text=True, cwd=str(REPO_ROOT))
    results: list[tuple[str, str]] = []
    current: str | None = None
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            current = line[len("+++ b/") :]
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+") and current is not None:
            results.append((current, line[1:]))
    return results


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Pre-commit aid: fail when added CHANGELOG lines carry an em/en "
            "dash in prose or an unlinked path-shaped reference."
        )
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Check only the staged diff (default: full working tree vs HEAD).",
    )
    args = parser.parse_args(argv[1:])

    try:
        lines = added_lines(args.staged)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, str]] = []
    for path, text in lines:
        stripped = CODE_SPAN_RE.sub("", text)
        if EM_DASH in stripped or EN_DASH in stripped:
            findings.append((path, "em/en dash in prose", text.strip()))
        for ref in unlinked_refs_in_line(text):
            findings.append((path, f"unlinked file reference `{ref}`", text.strip()))

    if not findings:
        scope = "staged" if args.staged else "working-tree"
        print(
            f"OK: {len(lines)} added CHANGELOG line(s) ({scope}) are dash-free "
            f"and every path-shaped reference is a markdown link."
        )
        return 0

    for path, issue, evidence in findings:
        print(f"FAIL {path}: {issue}\n    {evidence}", file=sys.stderr)
    print(
        f"\n{len(findings)} CHANGELOG-hygiene issue(s) in the added lines. Fix "
        f"before committing: remove em/en dashes from prose (use commas, "
        f"colons, or parentheses), and wrap path-shaped references as "
        f"[`path`](path). This aid mirrors delta gate D3, gate 51, and the "
        f"link-coverage gate, surfaced before the first commit.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
