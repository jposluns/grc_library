#!/usr/bin/env python3
"""Advisory readability check for root ``CHANGELOG.md`` entry summaries
(maintainer-flagged 2026-07-14; shipped by the CHANGELOG-compact-reformat PR,
strengthened by the P1 §1.2 reformat PR).

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID, not an audit gate.
The root ``CHANGELOG.md`` carries one COMPACT one-line summary per change
(``**YYYY-MM-DD | X.Y.Z | PR #N** - <one-sentence summary>``); the full
maintainer-grade detail lives in the detailed mirror
``.working/changelog-details/CHANGELOG-detailed.md`` and in git history (the
change-tracking governance rule's current-week / compact-root-form model). The
recurring drift this tool guards against: root summaries creep back into long,
dense, semicolon-chained run-on sentences that a general reader cannot follow
(the #887-#901 reversion of 109-262 words, reformatted in the PR that shipped
this tool; and the #902-#914 reversion of 74-147-word semicolon-chains,
reformatted in the PR that strengthened it). No existing gate enforces
one-line compactness or readability: gate 59 (mirror-header-parity) checks only
that the root and mirror HEADERS match, not the summary. This tool produces
that missing signal.

WHAT IT CHECKS (two complementary signals). For each root entry matching the
compact-form header it measures the summary portion (everything after
``** - ``) two ways and WARNS if EITHER fires:

  1. TOTAL LENGTH: total summary words exceed ``--word-warn`` (default 130).
     The threshold is deliberately generous: a legitimate compact-but-multi-item
     batch entry runs ~100 words, while the paragraph-length drift ran 150-262.

  2. DENSE RUN-ON: the longest single SENTENCE exceeds ``--sentence-warn``
     (default 65) words. This is the signal the word-count alone MISSED: the
     #902-#914 drift was one 74-147-word semicolon-and-colon-chained sentence,
     under the 130-word total ceiling yet unreadable, whereas a compact entry is
     two plain sentences of ~40 words each. Sentence length, not total length,
     is what separates "a reader can follow this" from "a run-on". Sentences are
     split on a period-then-space boundary (a crude splitter that never
     OVER-flags: it can only under-split on ``e.g.``-style internal periods,
     which shortens a measured sentence, so a false positive is not possible
     from the splitter, only a false negative).

Both thresholds are advisory ceilings, not hard boundaries: the compact/dense
boundary is a judgement call, so the tool flags clear drift for the
orchestrator to compress and never blocks a build.

It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the four-surface
parity gate 35, the regression suite gate 36) does NOT auto-discover it, and it
is NOT wired into ``run_all_audits.sh`` / ``quality.yml`` /
``.pre-commit-config.yaml``. It always exits 0: its findings are compress-queue
candidates for the orchestrator, never workflow failures. Making it a blocking
gate would be a decorative gate (gate-discipline rule): the compact/dense
boundary is a judgement call, so a hard threshold would either false-positive on
a legitimate long batch entry or be set so high it never fires. Its self-test
lives behind ``--self-test`` (inline unittest on the parser) rather than in
``tests/`` so the gate-36 regression runner does not adopt it as a gated test.

Usage:
  python3 tools/audit-changelog-entry-length.py [--changelog PATH]
                                                [--word-warn N]
                                                [--sentence-warn N]
                                                [--self-test]
"""

import argparse
import re
import sys
from pathlib import Path

# Compact-form root entry header: "**YYYY-MM-DD | X.Y.Z | PR #N** - summary".
# The separator after the closing "**" is a plain " - " (hyphen), per the
# adopted compact root-entry form (no em/en dash anywhere in the corpus).
ENTRY_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2} \| [^|]+ \| PR #(\d+)\*\* - (.+)$")

DEFAULT_WORD_WARN = 130
DEFAULT_SENTENCE_WARN = 65

# A sentence boundary is a period (optionally closing a parenthesis/quote)
# followed by whitespace. Crude by design: it can only UNDER-split (on an
# internal "e.g." period), which shortens a measured sentence and so can only
# cause a false NEGATIVE, never a false positive.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.)\"'])\s+")


def sentence_word_counts(summary):
    """Return the list of word counts for each sentence in ``summary``."""
    parts = [p for p in _SENTENCE_SPLIT_RE.split(summary.strip()) if p.strip()]
    if not parts:
        return [0]
    return [len(p.split()) for p in parts]


def scan(text):
    """Return a list of (pr_number, word_count, max_sentence_words, summary) for
    every compact-form root entry line in ``text``, in file order."""
    results = []
    for line in text.splitlines():
        m = ENTRY_RE.match(line.rstrip())
        if not m:
            continue
        pr = int(m.group(1))
        summary = m.group(2).strip()
        word_count = len(summary.split())
        max_sentence = max(sentence_word_counts(summary))
        results.append((pr, word_count, max_sentence, summary))
    return results


def report(entries, word_warn, sentence_warn, stream=sys.stdout):
    """Print the advisory report to ``stream``. Returns the count of entries
    flagged by EITHER signal (informational; the caller still exits 0)."""
    if not entries:
        print("audit-changelog-entry-length: no compact-form root entries "
              "found (nothing to check).", file=stream)
        return 0
    over_words = [(pr, wc) for pr, wc, _, _ in entries if wc > word_warn]
    over_sentence = [(pr, ms) for pr, _, ms, _ in entries if ms > sentence_warn]
    flagged = {pr for pr, _ in over_words} | {pr for pr, _ in over_sentence}
    longest_pr, longest_wc, _, _ = max(entries, key=lambda e: e[1])
    densest_pr, _, densest_ms, _ = max(entries, key=lambda e: e[2])
    print(f"audit-changelog-entry-length: scanned {len(entries)} root "
          f"entries; word-warn {word_warn}, sentence-warn {sentence_warn}.",
          file=stream)
    print(f"  longest entry: PR #{longest_pr} at {longest_wc} words; "
          f"densest sentence: PR #{densest_pr} at {densest_ms} words.",
          file=stream)
    if over_words:
        print(f"  ADVISORY (total length): {len(over_words)} "
              f"entr{'y' if len(over_words) == 1 else 'ies'} over {word_warn} "
              f"words (compress toward the one-line form; full detail belongs "
              f"in the detailed mirror):", file=stream)
        for pr, wc in sorted(over_words, key=lambda x: -x[1]):
            print(f"    PR #{pr}: {wc} words", file=stream)
    if over_sentence:
        print(f"  ADVISORY (dense run-on): {len(over_sentence)} "
              f"entr{'y' if len(over_sentence) == 1 else 'ies'} with a single "
              f"sentence over {sentence_warn} words (split into shorter plain "
              f"sentences; a semicolon-chained run-on is the drift this "
              f"catches):", file=stream)
        for pr, ms in sorted(over_sentence, key=lambda x: -x[1]):
            print(f"    PR #{pr}: longest sentence {ms} words", file=stream)
    if not flagged:
        print(f"  all entries within the compact-form budget "
              f"(<= {word_warn} words total, <= {sentence_warn} words per "
              f"sentence).", file=stream)
    return len(flagged)


def _self_test():
    import unittest

    class T(unittest.TestCase):
        def test_parses_compact_entry(self):
            txt = "**2026-07-14 | 2026.07.395 | PR #907** - one two three four."
            r = scan(txt)
            self.assertEqual(len(r), 1)
            self.assertEqual(r[0][0], 907)
            self.assertEqual(r[0][1], 4)

        def test_ignores_non_entry_lines(self):
            txt = ("# Changelog\n\nSome prose about the file.\n"
                   "**2026-07-14 | 2026.07.395 | PR #907** - a b c\n")
            r = scan(txt)
            self.assertEqual(len(r), 1)

        def test_over_word_threshold_detected(self):
            summary = ". ".join(" ".join(["word"] * 20) for _ in range(7)) + "."
            txt = f"**2026-07-14 | 2026.07.395 | PR #907** - {summary}"
            n = report(scan(txt), DEFAULT_WORD_WARN, DEFAULT_SENTENCE_WARN,
                       stream=open("/dev/null", "w"))
            self.assertEqual(n, 1)  # 140 words total > 130

        def test_dense_run_on_under_word_ceiling_detected(self):
            # One 90-word sentence: under 130 total, but a dense run-on.
            summary = " ".join(["word"] * 90) + "."
            txt = f"**2026-07-14 | 2026.07.395 | PR #907** - {summary}"
            entries = scan(txt)
            self.assertEqual(entries[0][1], 90)      # total under 130
            self.assertEqual(entries[0][2], 90)      # longest sentence 90
            n = report(entries, DEFAULT_WORD_WARN, DEFAULT_SENTENCE_WARN,
                       stream=open("/dev/null", "w"))
            self.assertEqual(n, 1)  # caught by the sentence signal

        def test_two_short_sentences_clean(self):
            # 80 words total but split into two ~40-word sentences: readable.
            s1 = " ".join(["word"] * 40)
            s2 = " ".join(["word"] * 40)
            summary = f"{s1}. {s2}."
            txt = f"**2026-07-14 | 2026.07.395 | PR #907** - {summary}"
            entries = scan(txt)
            self.assertEqual(entries[0][2], 40)  # longest sentence 40
            n = report(entries, DEFAULT_WORD_WARN, DEFAULT_SENTENCE_WARN,
                       stream=open("/dev/null", "w"))
            self.assertEqual(n, 0)

        def test_empty_corpus(self):
            n = report([], DEFAULT_WORD_WARN, DEFAULT_SENTENCE_WARN,
                       stream=open("/dev/null", "w"))
            self.assertEqual(n, 0)

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--changelog", default="CHANGELOG.md",
                    help="path to the root CHANGELOG.md (default: CHANGELOG.md)")
    ap.add_argument("--word-warn", type=int, default=DEFAULT_WORD_WARN,
                    help=f"warn on entries over N words total (default: {DEFAULT_WORD_WARN})")
    ap.add_argument("--sentence-warn", type=int, default=DEFAULT_SENTENCE_WARN,
                    help=f"warn on entries whose longest sentence exceeds N words "
                         f"(default: {DEFAULT_SENTENCE_WARN})")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline parser self-test and exit")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    path = Path(args.changelog)
    if not path.is_file():
        print(f"audit-changelog-entry-length: {path} not found; nothing to "
              f"check (advisory, exit 0).")
        return 0

    entries = scan(path.read_text(encoding="utf-8"))
    report(entries, args.word_warn, args.sentence_warn)
    # Advisory: always exit 0. Findings are compress-queue candidates, not
    # build failures (see the module docstring).
    return 0


if __name__ == "__main__":
    sys.exit(main())
