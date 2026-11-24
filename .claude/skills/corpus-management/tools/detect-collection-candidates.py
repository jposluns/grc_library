#!/usr/bin/env python3
"""Collection-candidate detector, exploratory tool, not a gate.

Companion to gate 41 (Collection-enumeration consistency audit). Gate 41
enforces drift discipline on a hard-coded list of "collections" (each
collection: a canonical source-of-truth directory paired with the
enumeration locations in the corpus that should match it). This tool
surfaces NEW candidate collections by heuristic scan, so the maintainer
can triage them one-by-one and add approved candidates to gate 41's
configuration.

Approach (heuristic):

1. Walk the candidate-source roots in ``CANDIDATE_ROOTS``:
   ``.claude/aiqt/rules/``, ``.claude/skills/``, and all 12 domain directories.
   Every direct subdirectory of a root with at least 3 items is treated as
   a candidate canonical source.

2. For each candidate canonical, list its items (file basenames stripped
   of ``.md``; subdirectory names as-is).

3. Walk the markdown corpus. For each file, count how many of the
   candidate's items appear as backticked path-shaped tokens. Files
   whose match exceeds the configured threshold (60% by default) are
   recorded as putative enumeration locations.

4. Subtract collections / enumeration-location pairs already declared
   in ``.claude/skills/corpus-management/tools/lint-collection-enumeration-consistency.py``. The
   remainder is surfaced.

5. Output: one candidate per cluster, with the canonical source path,
   the suggested collection name, the files that look like enumerations,
   the per-file match coverage, and a one-line rationale.

This is an exploratory tool. It runs on demand:

    python3 .claude/skills/corpus-management/tools/detect-collection-candidates.py

It is NOT part of the audit programme, has no §6 inventory number, and
does not fail on candidates. Scan OSError/ValueError failures and unreadable PR
diff inputs return 2. Candidates require a maintainer's decision; the heuristic
does not approve them.

Stdlib-only Python 3.14. Exit 0 reports candidates or a PR with no pack
changes (and --help); exit 2 refuses invalid arguments, unavailable PR diff
inputs, unreadable in-scope Markdown (including invalid UTF-8), and reported
scan filesystem errors. Unexpected exceptions remain uncaught (normally exit 1).
Directory traversal errors propagate to the incomplete-scan report, naming the
unreadable directory instead of reporting a complete negative result.
``--on-pr`` uses GITHUB_EVENT_PATH, GITHUB_EVENT_NAME and GITHUB_SHA.
The quality workflow pins that command as a non-gate informational step.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/skills/corpus-management/tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import is_default_exempt_root, REPO_ROOT, has_exempt_part, PROJECT_DOCUMENT_DIRS, PROJECT_DOCUMENT_FILES  # noqa: E402  # grc-config/store, stays local


# Candidate canonical source roots. Each direct subdirectory of these
# roots with ≥ MIN_ITEMS items is a candidate canonical source.
CANDIDATE_ROOTS: tuple[str, ...] = (
    ".claude/aiqt/rules",
    ".claude/skills",
    "governance",
    "compliance",
    "crypto",
    "ai",
    "privacy",
    "security",
    "operations",
    "dev-security",
    "supply-chain",
    "resilience",
    "risk",
    "architecture",
)

# Minimum number of items a directory must contain to be considered a
# candidate canonical source.
MIN_ITEMS = 3

# Match coverage threshold: a file qualifies as a putative enumeration
# location if at least this fraction of the candidate's items appear in it.
COVERAGE_THRESHOLD = 0.60

# Already-tracked collections (mirror of gate 41's configuration).
# When a candidate matches one of these source-dir paths, it is suppressed
# from the output unless the detected enumeration files extend the
# already-tracked set.
TRACKED_COLLECTIONS: dict[str, tuple[str, ...]] = {
    ".claude/aiqt/rules/aiqt": (".claude/CLAUDE.md",),
    ".claude/aiqt/rules/security": (".claude/CLAUDE.md",),
}

# PRs changing the retained pack surfaces trigger the advisory scan.
PR_SOURCE_ROOTS = (".claude/aiqt/", ".claude/skills/", ".claude/rules/")


def pr_changes_sources() -> bool:
    """Read GitHub's PR event and diff its base against the checked-out merge SHA.

    Missing inputs, malformed SHAs and a failed diff are errors, never a quiet
    skip. NUL separation preserves path boundaries even for unusual filenames.
    Disabling rename detection includes both the old and new paths of a move.
    """
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        raise ValueError("--on-pr requires a pull_request event")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    base = event["pull_request"]["base"]["sha"]
    head = os.environ["GITHUB_SHA"]
    if not all(isinstance(ref, str) and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", ref)
               for ref in (base, head)):
        raise ValueError("PR base and head must be full commit SHAs")
    # Keep Git invocations on the required Bash command route.
    # shlex.join quotes every argv element; validated SHAs cannot become shell code.
    command = shlex.join(["git", "-C", str(REPO_ROOT), "diff", "--name-only", "--no-renames", "-z", base, head, "--"])
    result = subprocess.run(["bash", "-c", command], capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise ValueError("git diff failed: " + result.stderr.strip())
    return any(path.startswith(PR_SOURCE_ROOTS) for path in result.stdout.split("\0"))


# Files and directories to skip when walking the corpus for enumeration
# matches.
WALK_SKIP_DIRS: frozenset[str] = frozenset(
    {".git", "node_modules", "__pycache__", ".claude"}
)

# Generated artefacts and the CHANGELOG are not enumeration locations of
# interest; skip them when scoring files.
WALK_SKIP_FILES: frozenset[str] = frozenset(
    {
        ".working/CHANGELOG.md",
        ".claude/skills/corpus-management/data/taxonomy.yml",
        ".claude/skills/corpus-management/data/narrative.yml",
        "governance/portal.md",
        "governance/maturity-scorecard.md",
    }
)


@dataclass(frozen=True)
class Candidate:
    canonical: str
    suggested_name: str
    items: tuple[str, ...]
    enumeration_files: tuple[tuple[str, int, int], ...]  # (path, matched, total)


def list_candidate_items(source_dir: Path) -> list[str]:
    """Return the basenames (md stripped) / dirnames of items in ``source_dir``.

    Items: markdown files (basename without .md) or subdirectories
    (dirname as-is). Items beginning with ``.`` are excluded.
    """
    items: list[str] = []
    for entry in source_dir.iterdir():
        if entry.name.startswith("."):
            continue
        if entry.is_file() and entry.name.endswith(".md"):
            items.append(entry.name[:-3])
        elif entry.is_dir():
            items.append(entry.name)
    return sorted(items)


def file_mentions_items(text: str, items: list[str]) -> int:
    """Count how many items from ``items`` appear in ``text`` as path-shaped
    tokens.

    Heuristic: an item is considered "mentioned" if its name appears in
    the text either as ``item-name.md`` (with .md suffix) or as
    ``item-name/`` (with trailing slash, signaling directory) or as a
    backticked / markdown-linked path containing the item name with a
    contextual separator (``/``).
    """
    count = 0
    for item in items:
        # Use word-boundary-ish regex to avoid partial substring matches.
        pattern = re.compile(
            r"\b" + re.escape(item) + r"(?:\.md|/SKILL\.md|/)"
        )
        if pattern.search(text):
            count += 1
    return count


def iter_corpus_markdown() -> list[Path]:
    """Yield markdown files in the corpus, minus the skip set."""
    out: list[Path] = []
    def traversal_error(exc: OSError) -> None:
        raise exc

    for directory, _, filenames in os.walk(REPO_ROOT, onerror=traversal_error):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            path = Path(directory) / filename
            if is_default_exempt_root(path, repo_root=REPO_ROOT):
                continue
            try:
                rel = path.relative_to(REPO_ROOT).as_posix()
                parts = path.relative_to(REPO_ROOT).parts
            except ValueError:
                continue
            if has_exempt_part(parts, WALK_SKIP_DIRS, admitted_roots=(
                    *PROJECT_DOCUMENT_DIRS, *PROJECT_DOCUMENT_FILES, ".claude/CLAUDE.md")):
                continue
            if rel in WALK_SKIP_FILES:
                continue
            out.append(path)
    return out


def find_candidates() -> list[Candidate]:
    """Walk candidate roots, score each candidate, return surviving."""
    corpus = iter_corpus_markdown()
    corpus_texts: dict[Path, str] = {}
    for path in corpus:
        text = read_text_safe(path)
        if text is None:
            raise ValueError(f"Cannot read Markdown: {path.relative_to(REPO_ROOT).as_posix()}")
        corpus_texts[path] = text

    candidates: list[Candidate] = []
    for root_rel in CANDIDATE_ROOTS:
        root_path = REPO_ROOT / root_rel
        if not root_path.is_dir():
            continue
        for sub in sorted(root_path.iterdir()):
            if not sub.is_dir() or sub.name.startswith("."):
                continue
            sub_rel = sub.relative_to(REPO_ROOT).as_posix()
            items = list_candidate_items(sub)
            if len(items) < MIN_ITEMS:
                continue
            # Score each corpus file for coverage of this candidate's items.
            matches: list[tuple[str, int, int]] = []
            for path, text in corpus_texts.items():
                # Skip files that are inside the candidate's own source dir.
                try:
                    if path.relative_to(sub).parts:
                        continue
                except ValueError:
                    pass
                matched = file_mentions_items(text, items)
                if matched / len(items) >= COVERAGE_THRESHOLD:
                    rel = path.relative_to(REPO_ROOT).as_posix()
                    matches.append((rel, matched, len(items)))
            if not matches:
                continue
            # Filter against already-tracked enumeration locations.
            tracked_locs = TRACKED_COLLECTIONS.get(sub_rel, ())
            new_matches = tuple(m for m in matches if m[0] not in tracked_locs)
            if not new_matches:
                continue
            candidates.append(
                Candidate(
                    canonical=sub_rel,
                    suggested_name=sub.name,
                    items=tuple(items),
                    enumeration_files=tuple(new_matches),
                )
            )
    return candidates


def main(argv: list[str]) -> int:
    try:
        candidates = find_candidates()
    except (OSError, ValueError) as exc:
        print(f"Collection scan incomplete: {exc}", file=sys.stderr)
        return 2
    print(
        f"Collection-candidate detector: scanned {len(CANDIDATE_ROOTS)} root(s); "
        f"{len(candidates)} candidate collection(s) surfaced.\n"
    )
    if not candidates:
        print("No new candidates detected. Either every plausible collection is")
        print("already declared in .claude/skills/corpus-management/tools/lint-collection-enumeration-consistency.py,")
        print("or no directory met the heuristic thresholds (≥ {} items, ≥ {:.0%}"
              " coverage in an enumeration file).".format(MIN_ITEMS, COVERAGE_THRESHOLD))
        return 0

    for i, c in enumerate(candidates, start=1):
        print(f"--- Candidate {i} of {len(candidates)} ---")
        print(f"  Canonical source: {c.canonical}")
        print(f"  Suggested collection name: {c.suggested_name}")
        print(f"  Items ({len(c.items)}): {', '.join(c.items)}")
        print(f"  Files that look like enumerations of this collection:")
        for rel, matched, total in c.enumeration_files:
            pct = matched / total * 100
            print(f"    {rel}: {matched}/{total} items ({pct:.0f}% coverage)")
        already = TRACKED_COLLECTIONS.get(c.canonical)
        if already:
            print(
                f"  Note: this canonical is already tracked by gate 41 with "
                f"{len(already)} enumeration location(s); the file(s) above "
                f"would extend the tracked set."
            )
        else:
            print(
                f"  Note: this canonical is not yet tracked by gate 41. "
                f"Triage: add it as a new collection, or dismiss as not a "
                f"meaningful collection."
            )
        print()
    print(
        f"To add a candidate to gate 41, edit the COLLECTIONS tuple in "
        f".claude/skills/corpus-management/tools/lint-collection-enumeration-consistency.py with the candidate's "
        f"source_dir, source_glob, source_normaliser, and a list of "
        f"EnumerationLocation entries each declaring its section_start_regex / "
        f"section_end_regex / item_regex. Re-run gate 41 to verify the "
        f"new collection is consistent."
    )
    return 0


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--on-pr", action="store_true", help="scan only PRs changing retained pack paths")
    args = parser.parse_args()
    if args.on_pr:
        try:
            changed = pr_changes_sources()
        except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
            print(f"::error::Cannot determine collection-source changes: {exc}", file=sys.stderr)
            return 2
        if not changed:
            print("No pack changes in this PR. Skipping detector.")
            return 0
        print("Pack changes detected. Running collection-candidate detector...")
    return main(sys.argv)


if __name__ == "__main__":
    sys.exit(cli())
