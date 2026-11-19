#!/usr/bin/env python3
"""Verify a pull request's added or changed weekly and monthly .working/CHANGELOG.md paragraphs stay short (delta gate D7).

This is a PR-time delta gate (D7), not part of the corpus audit
programme. The corpus gates check repository state at HEAD; this script compares
HEAD to the PR's merge-base and judges each weekly or monthly paragraph of the public
.working/CHANGELOG.md that the PR adds or changes, failing if one exceeds a length ceiling.

THE WEEKLY PUBLIC RECORD. The public .working/CHANGELOG.md carries weekly summaries only
(maintainer-directed 2026-11-13): one paragraph per completed ISO week, headed
``**Week of YYYY-MM-DD (PRs #FIRST-#LAST)**``, and, for periods older than 3 months, one per
calendar month, headed ``**YYYY-MM (PRs #FIRST-#LAST)**``, each an accomplishments summary of
at most 4 sentences. Each change's own entry lives in the private per-change record; D1
refuses a per-change entry in the public file, so D7 does not measure one.

WHAT IT CHECKS. A paragraph is its heading and every line below it up to the next heading of
any kind (``changelog_diff.public_line_kind``); its body is the text of those lines joined by
spaces, so a second paragraph under one heading counts toward the same ceiling. A paragraph is
judged when the PR adds any of its lines (its heading or a body line), and it is judged whole.
It FAILS if any of these exceeds its ceiling:
  1. SENTENCES: more than --sentence-count-max sentences (default 4, the weekly summary's own
     shape).
  2. TOTAL LENGTH: more than --word-max words (default 140).
  3. DENSE RUN-ON: a sentence of more than --sentence-max words (default 45).
Why 140 words: 4 sentences of about 35 words each, the length a plain-language summary
sentence keeps to; the 45-word sentence ceiling is the one the per-change summaries used,
which the earlier repository's drift (50 to 95-word sentences) was measured against. A
paragraph of 4 sentences at the ceilings passes; a fifth sentence, a 141st word or a 46th word
in one sentence fails.

HOW IT READS THE DIFF. The added lines come from the pinned ``git diff`` and hunk-count parser
shared in ``.claude/skills/corpus-management/tools/changelog_diff.py``
(``added_line_diff``, ``parse_numbered_added_lines``), with their line numbers in the head
file; the head file itself is read from the head commit (``git show``) and split on LF only,
then again at every ``str.splitlines()`` boundary inside a line (CR, U+2028, U+0085 and the
rest), so a heading or body after such a boundary is read and a body runs to the end of its
section. A diff the parser cannot read exactly, or a head file that is not UTF-8, is exit 2,
not a pass. The diff names ``:(top).working/CHANGELOG.md``, so a run from a subdirectory reads
the root file.

NOT COVERED: the legacy ``## Week of YYYY-MM-DD`` sections written before the per-change
record moved out of the public file (their bullets are history and are not re-measured), a
paragraph the PR does not touch, and sentence boundaries the crude splitter misses (an internal
period such as ``e.g.`` under-splits, which can only shorten a counted sentence or lower the
sentence count). The authoring preflight (``preflight-changelog.py``) imports
``judged_paragraphs`` and ``evaluate_paragraphs`` with the three ceilings, so the two never
drift.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 .claude/skills/corpus-management/tools/check-changelog-length-on-pr.py
    # Locally, comparing HEAD to a specific base:
    python3 .claude/skills/corpus-management/tools/check-changelog-length-on-pr.py origin/main
    python3 .claude/skills/corpus-management/tools/check-changelog-length-on-pr.py origin/main HEAD
    # Self-test:
    python3 .claude/skills/corpus-management/tools/check-changelog-length-on-pr.py --self-test

Exit codes:
    0 : every added or changed weekly or monthly paragraph is within the ceilings, or the PR
        adds no line to one.
    1 : one or more added or changed paragraphs exceed a ceiling.
    2 : invocation or environment error (cannot determine base/head, git failure,
        a diff the shared parser cannot read exactly, a head file that is not UTF-8, a
        .working/CHANGELOG.md that is a symbolic link or a submodule in the head or the diff,
        or git selecting another repository or work tree than it finds by itself), or
        CANNOT-EVALUATE: base and head resolve to the same commit (a collapsed,
        empty range), so nothing was evaluated.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/skills/corpus-management/tools/ on sys.path
from lint_common import PrRangeError, resolve_pr_range  # noqa: E402  # grc-config/store, stays local
from changelog_diff import (  # noqa: E402  # shared added-line diff reader and public line shapes
    STRUCTURAL_KINDS, ChangelogDiffUnreadable, GitQueryFailed, GitSelectsAnotherTree,
    added_line_diff, check_git_selects_root, parse_numbered_added_lines, public_line_kind,
    public_line_parts, read_blob, refuse_links)

CHANGELOG_PATH = ".working/CHANGELOG.md"
# The weekly and monthly paragraph ceilings (see the module docstring for why).
PARAGRAPH_WORD_MAX = 140
PARAGRAPH_SENTENCE_MAX = 45
PARAGRAPH_SENTENCE_COUNT_MAX = 4

# Authoritative sentence-boundary definition. The authoring preflight imports this module so its
# signal stays in lock-step with these ceilings.
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


def period_paragraphs(text: str) -> list[tuple[str, set[int], str]]:
    """(label, LF line numbers, body) for each weekly or monthly paragraph of ``text``, the
    public file. The label is the heading without its bold markers; the line numbers are the
    heading's and every line's up to the next heading of any kind; the body is the text of
    those lines after the heading, joined by spaces."""
    out: list[tuple[str, set[int], str]] = []
    current: tuple[str, set[int], list[str]] | None = None
    for number, part in public_line_parts(text):
        kind = public_line_kind(part)
        if kind in ("weekly", "monthly"):
            if current is not None:
                out.append((current[0], current[1], " ".join(current[2])))
            current = (part.strip("*"), {number}, [])
        elif kind in STRUCTURAL_KINDS:
            if current is not None:
                out.append((current[0], current[1], " ".join(current[2])))
            current = None
        elif current is not None:
            current[1].add(number)
            if part.strip():
                current[2].append(part.strip())
    if current is not None:
        out.append((current[0], current[1], " ".join(current[2])))
    return out


def evaluate_paragraphs(paragraphs: list[tuple[str, str]], word_max: int, sentence_max: int,
                        count_max: int) -> list[str]:
    """Return a human-readable line per offending (label, body) paragraph."""
    offending: list[str] = []
    for label, body in paragraphs:
        total, longest = measure(body)
        count = len(sentence_word_counts(body))
        reasons = []
        if count > count_max:
            reasons.append(f"{count} sentences > {count_max}")
        if total > word_max:
            reasons.append(f"{total} words > {word_max}")
        if longest > sentence_max:
            reasons.append(f"longest sentence {longest} > {sentence_max}")
        if reasons:
            offending.append(f"{label}: {'; '.join(reasons)}")
    return offending


def judged_paragraphs(added: set[int], head_text: str) -> list[tuple[str, str]]:
    """(label, body) of each paragraph of ``head_text`` holding a line numbered in ``added``."""
    return [(label, body) for label, numbers, body in period_paragraphs(head_text)
            if numbers & added]


def run_git_mode(base: str | None, head: str, word_max: int, sentence_max: int,
                 count_max: int) -> int:
    # git must select the repository it finds by itself (a sibling GIT_DIR printed "not
    # modified"), and the head's .working/CHANGELOG.md must be a regular file even when the diff does not
    # show it. Selection is checked BEFORE range resolution: a sibling GIT_DIR usually also
    # collapses the range, and the precise wrong-repository diagnosis must win over the generic
    # collapsed-range refusal.
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
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: git failed: {exc}", file=sys.stderr)
        return 2

    try:
        merge_base, head = resolve_pr_range(base, head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        # ":(top)" names the root .working/CHANGELOG.md from any subdirectory; the runner drops
        # GIT_LITERAL_PATHSPECS, under which git read it as a file name.
        diff = added_line_diff([merge_base, head], [":(top)" + CHANGELOG_PATH])
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not diff:
        print(f"OK: {CHANGELOG_PATH} not modified between {merge_base[:8]} and {head}.")
        return 0

    try:
        added = {number for path, number, _ in parse_numbered_added_lines(diff)
                 if path == CHANGELOG_PATH}
    except ChangelogDiffUnreadable as exc:
        print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: {exc}", file=sys.stderr)
        return 2

    paragraphs: list[tuple[str, str]] = []
    if added:
        try:
            head_text = read_blob(head, CHANGELOG_PATH).decode("utf-8")
        except GitQueryFailed as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        except OSError as exc:
            print(f"ERROR: git show failed: {exc}", file=sys.stderr)
            return 2
        except UnicodeDecodeError as exc:
            print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: the head file is not "
                  f"UTF-8 ({exc})", file=sys.stderr)
            return 2
        paragraphs = judged_paragraphs(added, head_text)
    if not paragraphs:
        print(f"OK: no weekly or monthly paragraph added or changed in {CHANGELOG_PATH}.")
        return 0

    offending = evaluate_paragraphs(paragraphs, word_max, sentence_max, count_max)
    if not offending:
        print(
            f"OK: {len(paragraphs)} added or changed {CHANGELOG_PATH} paragraph(s) within the "
            f"ceilings ({count_max} sentences / {word_max} words / {sentence_max}-word sentence)."
        )
        return 0

    print(
        f"FAIL: {len(offending)} added or changed {CHANGELOG_PATH} paragraph(s) exceed the "
        f"length ceiling. A weekly or monthly summary is at most {count_max} sentences and "
        f"{word_max} words, with no sentence over {sentence_max} words; the detail belongs in "
        f"the private per-change record:",
        file=sys.stderr,
    )
    for row in offending:
        print(f"  {row}", file=sys.stderr)
    return 1


def _self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        HEADER = "**Week of 2026-07-13 (PRs #980-#988)**"

        def test_short_paragraph_passes(self):
            p = [("Week", "Adds one comparator row. Batches the prior QA. No other content changed.")]
            self.assertEqual(evaluate_paragraphs(p, PARAGRAPH_WORD_MAX, PARAGRAPH_SENTENCE_MAX,
                                                 PARAGRAPH_SENTENCE_COUNT_MAX), [])

        def test_over_word_ceiling_fails(self):
            long = " ".join(["word"] * 150) + "."
            out = evaluate_paragraphs([("Week", long)], PARAGRAPH_WORD_MAX,
                                      PARAGRAPH_SENTENCE_MAX, PARAGRAPH_SENTENCE_COUNT_MAX)
            self.assertEqual(len(out), 1)
            self.assertIn("150 words > 140", out[0])

        def test_fifth_sentence_fails(self):
            out = evaluate_paragraphs([("Week", "A. B. C. D. E.")], PARAGRAPH_WORD_MAX,
                                      PARAGRAPH_SENTENCE_MAX, PARAGRAPH_SENTENCE_COUNT_MAX)
            self.assertEqual(out, ["Week: 5 sentences > 4"])

        def test_paragraphs_read_to_the_next_heading(self):
            text = (f"# Changelog\n\nIntro.\n\n{self.HEADER}\n\nOne.\n\nTwo.\n\n"
                    "## Week of 2026-07-06\n\n- Old.\n")
            got = period_paragraphs(text)
            self.assertEqual(got, [("Week of 2026-07-13 (PRs #980-#988)", {5, 6, 7, 8, 9, 10},
                                    "One. Two.")])

        def test_a_heading_after_a_line_break_is_read(self):
            for sep in ("\r", " ", "\u0085"):
                got = period_paragraphs("Lead." + sep + self.HEADER + sep + "Body.\n")
                self.assertEqual(got, [("Week of 2026-07-13 (PRs #980-#988)", {1}, "Body.")])

        def test_a_per_change_entry_is_not_a_paragraph(self):
            long = " ".join(["word"] * 120) + "."
            text = "# Changelog\n\n**2026-07-17 | 1.0.0 | PR #9** - " + long + "\n"
            self.assertEqual(period_paragraphs(text), [])

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a pull request's added or changed weekly and monthly "
            ".working/CHANGELOG.md paragraphs stay within the length ceiling (D7 delta gate)."
        ),
    )
    parser.add_argument("base", nargs="?", help="Base ref (default: origin/$GITHUB_BASE_REF).")
    parser.add_argument("head", nargs="?", default="HEAD", help="Head ref (default: HEAD).")
    parser.add_argument("--word-max", type=int, default=PARAGRAPH_WORD_MAX)
    parser.add_argument("--sentence-max", type=int, default=PARAGRAPH_SENTENCE_MAX)
    parser.add_argument("--sentence-count-max", type=int, default=PARAGRAPH_SENTENCE_COUNT_MAX)
    parser.add_argument("--self-test", action="store_true", help="Run the inline unit tests and exit.")
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return _self_test()

    return run_git_mode(args.base, args.head, args.word_max, args.sentence_max,
                        args.sentence_count_max)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
