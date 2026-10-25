#!/usr/bin/env python3
"""Verify a pull request's newly-added root CHANGELOG.md entries stay short (delta gate D7).

This is a PR-time delta gate (D7), not part of the corpus audit
programme. The corpus gates check repository state at HEAD; this script compares
HEAD to the PR's merge-base and inspects only the compact root CHANGELOG.md
ENTRY lines the PR ADDS, failing if any added entry's summary exceeds a length
ceiling.

WHY THIS GATE EXISTS (maintainer-directed 2026-07-17). The root CHANGELOG.md
carries one COMPACT one-line summary per change
(``**YYYY-MM-DD | X.Y.Z | PR #N** - <short summary>``); the full maintainer-grade
detail lives in the maintainer-grade detailed mirror (in the operational store) and in git history. Root
summaries have drifted back into long, dense, run-on paragraphs THREE times
(#887-901, #902-914, #919-986), each time reformatted by hand and each time
recurring while the earlier whole-file readability check was advisory only, so
nothing failed CI when an entry drifted long. This gate is the enforcement that
stops the recurrence: a NEWLY-ADDED root entry that exceeds the ceiling fails the
PR, so a long entry cannot merge. History is left untouched; only added entries
are checked, exactly as the D3 dash gate leaves historical dashes alone and
enforces the convention going forward.

WHAT IT CHECKS. For each added line matching the compact-entry header form, it
measures the summary portion (everything after ``** - ``) two ways and FAILS if
EITHER exceeds its ceiling:
  1. TOTAL LENGTH: total summary words > --word-max (default 100).
  2. DENSE RUN-ON: the longest single sentence > --sentence-max (default 45).
The two ceilings are deliberately set to pass a genuinely-compact entry (a
single-purpose entry runs ~40-50 words; a legitimate multi-item batch entry runs
~90-100 with plain short sentences) and fail the paragraph-length / dense-chain
drift (the historical drift ran 122-262 words with 50-95-word sentences).

HOW IT READS THE DIFF (3b399). The added lines come from the pinned ``git diff``
and hunk-count parser that tools/preflight-changelog.py uses (3b236), shared in
``tools/changelog_diff.py`` (``added_line_diff``, ``parse_added_lines``). It read the diff
with splitlines() and skipped every line starting "+++", so a CR, U+2028 or
U+0085 inside an added entry cut its summary short and the rest escaped the
ceiling. Each added line is now read whole, split on LF only, and an entry that
starts after any ``str.splitlines()`` boundary inside it (CR, U+2028, U+0085 and
the rest) is checked too. A diff the parser cannot read exactly is exit 2, not a
pass. The diff names ``:(top)CHANGELOG.md``, so a run from a subdirectory reads
the root file (3b399 round 3).

The compact-entry regex and sentence split are the authoritative definitions
for this defect class. The authoring preflight calls ``entries_in_added_line``
and ``evaluate`` rather than duplicating the length logic.

Scope: root CHANGELOG.md only. The maintainer-grade detailed mirror is maintainer working state,
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
    2 : invocation or environment error (cannot determine base/head, git failure,
        a diff the shared parser cannot read exactly, a CHANGELOG.md that is a
        symbolic link or a submodule in the head or the diff, or git selecting
        another repository or work tree than it finds by itself), or
        CANNOT-EVALUATE: base and head resolve to the same commit (a collapsed,
        empty range), so nothing was evaluated.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import PrRangeError, resolve_pr_range  # noqa: E402  # grc-config/store, stays local
from changelog_diff import (  # noqa: E402  # shared added-line diff reader (3b399)
    ChangelogDiffUnreadable, GitQueryFailed, GitSelectsAnotherTree, added_line_diff,
    check_git_selects_root, parse_added_lines, refuse_links)

CHANGELOG_PATH = "CHANGELOG.md"
DEFAULT_WORD_MAX = 100
DEFAULT_SENTENCE_MAX = 45

# Authoritative compact-entry and sentence-boundary definitions. The authoring
# preflight imports this module so its earlier signal stays in lock-step with D7.
ENTRY_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2} \| [^|]+ \| PR #(\d+)\*\* - (.+)$")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.?!)\"'])\s+")

# Tiered-public-CHANGELOG note (1.19.10 (closing PR #1037)): ENTRY_RE matches ONLY the
# per-PR compact header. In the tiered model the older weeks collapse to weekly
# (``**Week of YYYY-MM-DD (PRs #N-#M)**``) and monthly (``**YYYY-MM (PRs ...)**``)
# paragraph headers, which do NOT match ENTRY_RE, so those tiers are already out
# of this gate's scope and only the CURRENT-WEEK per-PR tier is length-gated.
# That is the intended behaviour; the model needs no change to this gate (the
# projection is built by tools/build-public-changelog.py).


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


def entries_in_added_line(text: str) -> list[tuple[str, str]]:
    """Return (pr, summary) for every compact entry in one added line.

    The line is whole (3b399): a CR, U+2028 or U+0085 inside it does not end it, so an entry
    whose summary runs past such a character is measured to the end of the line. An entry may
    also START after one of them (a CR is a markdown line ending, and splitlines() readers see
    a new line there), so ENTRY_RE is tried at the start of the line and after every
    splitlines() boundary; each match runs to the end of the added line. An entry followed by
    another in the same added line is therefore measured with the later one included, which
    can only over-count."""
    out: list[tuple[str, str]] = []
    start = 0
    for part in text.splitlines(keepends=True):
        m = ENTRY_RE.match(text[start:])
        if m:
            out.append((m.group(1), m.group(2)))
        start += len(part)
    return out


def added_entries_from_diff(diff: bytes) -> list[tuple[str, str]]:
    """Return (pr, summary) for every compact entry in the added lines of a ``git diff``'s
    bytes, read by ``changelog_diff.parse_added_lines`` (3b399): hunks by their line counts, bytes
    split on LF only, so an added line whose text starts with "++" is read, and a diff it
    cannot read exactly raises ChangelogDiffUnreadable."""
    out: list[tuple[str, str]] = []
    for _path, text in parse_added_lines(diff):
        out.extend(entries_in_added_line(text))
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
    # git must select the repository it finds by itself (a sibling GIT_DIR printed "not
    # modified"), and the head's CHANGELOG.md must be a regular file even when the diff does not
    # show it (3b399 round 5). Selection is checked BEFORE range resolution (3b530): a sibling
    # GIT_DIR usually also collapses the range, and the precise wrong-repository diagnosis must
    # win over the generic collapsed-range refusal.
    try:
        check_git_selects_root()
        refuse_links([CHANGELOG_PATH], head)
    except GitSelectsAnotherTree as exc:
        print(f"ERROR: {exc}; unset GIT_DIR or GIT_WORK_TREE and rerun.", file=sys.stderr)
        return 2
    except GitQueryFailed as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except ChangelogDiffUnreadable as exc:
        print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: {exc}", file=sys.stderr)
        return 2

    try:
        merge_base, head = resolve_pr_range(base, head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        # ":(top)" names the root CHANGELOG.md from any subdirectory (3b399 round 3); the runner
        # drops GIT_LITERAL_PATHSPECS, which made git read it as a file name (round 4).
        diff = added_line_diff([merge_base, head], [":(top)" + CHANGELOG_PATH])
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not diff:
        print(f"OK: {CHANGELOG_PATH} not modified between {merge_base[:8]} and {head}.")
        return 0

    try:
        entries = added_entries_from_diff(diff)
    except ChangelogDiffUnreadable as exc:
        print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: {exc}", file=sys.stderr)
        return 2
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
        f"change; move the detail to the maintainer-grade detailed mirror "
        f"and compress the root "
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
                "@@ -3 +3,2 @@\n"
                "+**2026-07-17 | 2026.07.476 | PR #988** - A short summary.\n"
                "+not an entry line\n"
                "-**2026-01-01 | 1.0.0 | PR #1** - removed line ignored.\n"
            ).encode("utf-8")
            got = added_entries_from_diff(diff)
            self.assertEqual(got, [("988", "A short summary.")])

        def test_an_entry_across_a_line_break_is_measured_whole(self):
            # 3b399: an entry before or after a CR, U+2028 or U+0085 is measured to the end of
            # the added line, so no fragment of it escapes the ceiling.
            long = " ".join(["word"] * 120) + "."
            for sep in ("\r", "\u2028", "\u0085"):
                for text in ("**2026-07-17 | 1.0.0 | PR #9** - Short." + sep + long,
                             "Lead." + sep + "**2026-07-17 | 1.0.0 | PR #9** - " + long):
                    got = entries_in_added_line(text)
                    self.assertEqual(len(got), 1)
                    self.assertEqual(
                        len(evaluate(got, DEFAULT_WORD_MAX, DEFAULT_SENTENCE_MAX)), 1)

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a pull request's newly-added root CHANGELOG.md entries "
            "stay within the compact-form length ceiling (D7 delta gate)."
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
