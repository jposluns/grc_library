#!/usr/bin/env python3
"""Verify a pull request's newly-added root CHANGELOG.md entries stay short (delta gate D8).

This is a CI-only PR-time delta gate (D8), not part of the corpus audit
programme. The corpus gates check repository state at HEAD; this script compares
HEAD to the PR's merge-base and inspects only the compact root CHANGELOG.md
ENTRY lines the PR ADDS, failing if any added entry's summary exceeds a length
ceiling.

WHY THIS GATE EXISTS (maintainer-directed 2026-07-17). The root CHANGELOG.md
carries one COMPACT one-line summary per change
(``**YYYY-MM-DD | X.Y.Z | PR #N** - <short summary>``); the full maintainer-grade
detail lives in the detailed mirror
(.working/changelog-details/CHANGELOG-detailed.md) and in git history. Root
summaries have drifted back into long, dense, run-on paragraphs THREE times
(#887-901, #902-914, #919-986), each time reformatted by hand and each time
recurring, because the readability check that flags the drift
(tools/audit-changelog-entry-length.py) is ADVISORY ONLY (wired into no gate),
so nothing fails CI when an entry drifts long and the orchestrator simply forgot
to run the advisory. This gate is the enforcement that stops the recurrence: a
NEWLY-ADDED root entry that exceeds the ceiling fails the PR, so a long entry
cannot merge. History is left untouched (the drift there is remediated by a
separate compression pass); only added entries are checked, exactly as the D3
dash gate leaves historical dashes alone and enforces the convention going
forward.

WHAT IT CHECKS. For each added line matching the compact-entry header form, it
measures the summary portion (everything after ``** - ``) two ways and FAILS if
EITHER exceeds its ceiling:
  1. TOTAL LENGTH: total summary words > --word-max (default 100).
  2. DENSE RUN-ON: the longest single sentence > --sentence-max (default 45).
The two ceilings are deliberately set to pass a genuinely-compact entry (a
single-purpose entry runs ~40-50 words; a legitimate multi-item batch entry runs
~90-100 with plain short sentences) and fail the paragraph-length / dense-chain
drift (the historical drift ran 122-262 words with 50-95-word sentences).

The compact-entry regex and the sentence split mirror
tools/audit-changelog-entry-length.py (the full-file advisory); the two
definitions are kept identical by convention (both measure the same thing, one
over history advisorily, one over added lines enforcingly). If you change one,
change the other.

Scope: root CHANGELOG.md only. The detailed mirror
(.working/changelog-details/CHANGELOG-detailed.md) is maintainer working state,
exempt from the corpus gates, and carries the full structured detail, so it is
not checked here.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-changelog-length-on-pr.py
    # Locally, comparing HEAD to a specific base:
    python3 tools/check-changelog-length-on-pr.py origin/main
    python3 tools/check-changelog-length-on-pr.py origin/main HEAD
    # Self-test:
    python3 tools/check-changelog-length-on-pr.py --self-test

Exit codes:
    0 : all added CHANGELOG.md entries are within the ceilings, or the diff does
        not add any compact entry line.
    1 : one or more added CHANGELOG.md entries exceed a length ceiling.
    2 : invocation or environment error (cannot determine base/head, git failure).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

CHANGELOG_PATH = "CHANGELOG.md"
DEFAULT_WORD_MAX = 100
DEFAULT_SENTENCE_MAX = 45

# Mirrors tools/audit-changelog-entry-length.py ENTRY_RE / _SENTENCE_SPLIT_RE.
# Keep the two definitions identical (see module docstring).
ENTRY_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2} \| [^|]+ \| PR #(\d+)\*\* - (.+)$")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.?!)\"'])\s+")


def sentence_word_counts(summary: str) -> list[int]:
    """Word count of each sentence in a summary (crude splitter; under-splits on
    internal periods like ``e.g.``, which only shortens a measured sentence, so a
    false positive is impossible from the splitter, only a false negative)."""
    parts = [p for p in _SENTENCE_SPLIT_RE.split(summary.strip()) if p.strip()]
    return [len(p.split()) for p in parts]


def measure(summary: str) -> tuple[int, int]:
    """Return (total_words, longest_sentence_words) for a summary."""
    total = len(summary.split())
    counts = sentence_word_counts(summary)
    return total, (max(counts) if counts else 0)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def added_entries_from_diff(diff: str) -> list[tuple[str, str]]:
    """Return (pr, summary) for every added compact-entry line in a unified diff."""
    out: list[tuple[str, str]] = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            m = ENTRY_RE.match(line[1:])
            if m:
                out.append((m.group(1), m.group(2)))
    return out


def evaluate(
    entries: list[tuple[str, str]], word_max: int, sentence_max: int
) -> list[str]:
    """Return a human-readable line per offending entry (empty list if all pass)."""
    offending: list[str] = []
    for pr, summary in entries:
        total, longest = measure(summary)
        reasons = []
        if total > word_max:
            reasons.append(f"{total} words > {word_max}")
        if longest > sentence_max:
            reasons.append(f"longest sentence {longest} > {sentence_max}")
        if reasons:
            offending.append(f"PR #{pr}: {'; '.join(reasons)}")
    return offending


def run_git_mode(base: str | None, head: str, word_max: int, sentence_max: int) -> int:
    if not base:
        github_base = os.environ.get("GITHUB_BASE_REF")
        if not github_base:
            print(
                "ERROR: base ref not provided and GITHUB_BASE_REF is unset. Pass a "
                "base ref as the first positional argument when running locally "
                "(e.g. origin/main).",
                file=sys.stderr,
            )
            return 2
        base = f"origin/{github_base}"

    try:
        merge_base = git("merge-base", base, head)
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: could not determine merge-base of {base}..{head}: {exc}. In "
            f"GitHub Actions, ensure that actions/checkout uses fetch-depth: 0.",
            file=sys.stderr,
        )
        return 2

    try:
        diff = git("diff", "--unified=0", merge_base, head, "--", CHANGELOG_PATH)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not diff:
        print(f"OK: {CHANGELOG_PATH} not modified between {merge_base[:8]} and {head}.")
        return 0

    entries = added_entries_from_diff(diff)
    if not entries:
        print(f"OK: no compact root {CHANGELOG_PATH} entry added in this PR.")
        return 0

    offending = evaluate(entries, word_max, sentence_max)
    if not offending:
        print(
            f"OK: {len(entries)} added {CHANGELOG_PATH} entr(y/ies) within the "
            f"length ceiling ({word_max} words / {sentence_max}-word sentence)."
        )
        return 0

    print(
        f"FAIL: {len(offending)} newly-added {CHANGELOG_PATH} entr(y/ies) exceed the "
        f"length ceiling. The root CHANGELOG carries a SHORT one-line summary per "
        f"change; move the detail to the detailed mirror "
        f"(.working/changelog-details/CHANGELOG-detailed.md) and compress the root "
        f"summary to <= {word_max} words with no sentence over {sentence_max} words:",
        file=sys.stderr,
    )
    for row in offending:
        print(f"  {row}", file=sys.stderr)
    return 1


def _self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def test_short_entry_passes(self):
            e = [("988", "Adds one comparator row. Batches the prior QA. No other content changed.")]
            self.assertEqual(evaluate(e, DEFAULT_WORD_MAX, DEFAULT_SENTENCE_MAX), [])

        def test_over_word_ceiling_fails(self):
            long = " ".join(["word"] * 120) + "."
            e = [("999", long)]
            out = evaluate(e, DEFAULT_WORD_MAX, DEFAULT_SENTENCE_MAX)
            self.assertEqual(len(out), 1)
            self.assertIn("120 words", out[0])

        def test_dense_run_on_under_word_ceiling_fails(self):
            # 60-word single sentence, under the 100-word total ceiling.
            run_on = " ".join(["clause"] * 60) + "."
            total, longest = measure(run_on)
            self.assertLessEqual(total, DEFAULT_WORD_MAX)
            out = evaluate([("999", run_on)], DEFAULT_WORD_MAX, DEFAULT_SENTENCE_MAX)
            self.assertEqual(len(out), 1)
            self.assertIn("longest sentence", out[0])

        def test_added_entries_parsed_from_diff(self):
            diff = (
                "+++ b/CHANGELOG.md\n"
                "+**2026-07-17 | 2026.07.476 | PR #988** - A short summary.\n"
                "+not an entry line\n"
                "-**2026-01-01 | 1.0.0 | PR #1** - removed line ignored.\n"
            )
            got = added_entries_from_diff(diff)
            self.assertEqual(got, [("988", "A short summary.")])

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a pull request's newly-added root CHANGELOG.md entries "
            "stay within the compact-form length ceiling (D8 delta gate)."
        ),
    )
    parser.add_argument("base", nargs="?", help="Base ref (default: origin/$GITHUB_BASE_REF).")
    parser.add_argument("head", nargs="?", default="HEAD", help="Head ref (default: HEAD).")
    parser.add_argument("--word-max", type=int, default=DEFAULT_WORD_MAX)
    parser.add_argument("--sentence-max", type=int, default=DEFAULT_SENTENCE_MAX)
    parser.add_argument("--self-test", action="store_true", help="Run the inline unit tests and exit.")
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return _self_test()

    return run_git_mode(args.base, args.head, args.word_max, args.sentence_max)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
