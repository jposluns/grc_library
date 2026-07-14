#!/usr/bin/env python3
"""Advisory length check for root ``CHANGELOG.md`` entry summaries
(maintainer-flagged 2026-07-14; shipped by the CHANGELOG-compact-reformat PR).

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID, not an audit gate.
The root ``CHANGELOG.md`` carries one COMPACT one-line summary per change
(``**YYYY-MM-DD | X.Y.Z | PR #N** - <one-sentence summary>``); the full
maintainer-grade detail lives in the detailed mirror
``.working/changelog-details/CHANGELOG-detailed.md`` and in git history (the
change-tracking governance rule's current-week / compact-root-form model). The
recurring drift this tool guards against: root summaries creep back into long
multi-sentence paragraphs (the #887-#901 reversion, 109-262 words, reformatted
to compact form in the PR that shipped this tool), which defeats the point of a
scannable root file. No existing gate enforces one-line compactness: gate 59
(mirror-header-parity) checks only that the root and mirror HEADERS match, not
the summary length. This tool produces that missing signal.

WHAT IT CHECKS. For each root entry line matching the compact-form header, it
counts the words in the summary portion (everything after ``** - ``) and WARNS
on any entry whose summary exceeds ``--word-warn`` words (default 130). The
threshold is deliberately generous: legitimate compact-but-multi-item entries
run up to ~104 words (a batch PR closing several small findings), while the
drift this catches ran 150-262; 130 clears the legitimate ceiling with margin
so the check is a low-false-positive signal, not noise. It is a COARSE signal
(word count cannot perfectly separate a 104-word legit entry from a 110-word
early drift), which is exactly why it is advisory: it flags clear drift for the
orchestrator to compress, it does not block a build.

It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the
four-surface parity gate 35, the regression suite gate 36) does NOT
auto-discover it, and it is NOT wired into ``run_all_audits.sh`` /
``quality.yml`` / ``.pre-commit-config.yaml``. It always exits 0: its findings
are compress-queue candidates for the orchestrator, never workflow failures.
Making it a blocking gate would be a decorative gate (gate-discipline rule):
the compact/long boundary is a judgement call (a legit batch entry can be
long), so a hard threshold would either false-positive on legit entries or be
set so high it never fires. Its self-test lives behind ``--self-test`` (inline
unittest on the parser) rather than in ``tests/`` so the gate-36 regression
runner does not adopt it as a gated test.

Usage:
  python3 tools/audit-changelog-entry-length.py [--changelog PATH]
                                                [--word-warn N] [--self-test]
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


def scan(text):
    """Return a list of (pr_number, word_count, summary) for every compact-form
    root entry line in ``text``, in file order."""
    results = []
    for line in text.splitlines():
        m = ENTRY_RE.match(line.rstrip())
        if not m:
            continue
        pr = int(m.group(1))
        summary = m.group(2).strip()
        word_count = len(summary.split())
        results.append((pr, word_count, summary))
    return results


def report(entries, word_warn, stream=sys.stdout):
    """Print the advisory report to ``stream``. Returns the count of entries
    over the threshold (informational; the caller still exits 0)."""
    over = [(pr, wc) for pr, wc, _ in entries if wc > word_warn]
    if not entries:
        print("audit-changelog-entry-length: no compact-form root entries "
              "found (nothing to check).", file=stream)
        return 0
    longest_pr, longest_wc, _ = max(entries, key=lambda e: e[1])
    print(f"audit-changelog-entry-length: scanned {len(entries)} root "
          f"entries; word-warn threshold {word_warn}.", file=stream)
    print(f"  longest: PR #{longest_pr} at {longest_wc} words.", file=stream)
    if over:
        print(f"  ADVISORY: {len(over)} entr{'y' if len(over) == 1 else 'ies'} "
              f"over {word_warn} words (compress toward the one-line form; "
              f"full detail belongs in the detailed mirror):", file=stream)
        for pr, wc in sorted(over, key=lambda x: -x[1]):
            print(f"    PR #{pr}: {wc} words", file=stream)
    else:
        print(f"  all entries within the compact-form budget "
              f"(<= {word_warn} words).", file=stream)
    return len(over)


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

        def test_over_threshold_detected(self):
            summary = " ".join(["word"] * 140)
            txt = f"**2026-07-14 | 2026.07.395 | PR #907** - {summary}"
            n = report(scan(txt), DEFAULT_WORD_WARN, stream=open("/dev/null", "w"))
            self.assertEqual(n, 1)

        def test_under_threshold_clean(self):
            summary = " ".join(["word"] * 50)
            txt = f"**2026-07-14 | 2026.07.395 | PR #907** - {summary}"
            n = report(scan(txt), DEFAULT_WORD_WARN, stream=open("/dev/null", "w"))
            self.assertEqual(n, 0)

        def test_empty_corpus(self):
            n = report([], DEFAULT_WORD_WARN, stream=open("/dev/null", "w"))
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
                    help=f"warn on entries over N words (default: {DEFAULT_WORD_WARN})")
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
    report(entries, args.word_warn)
    # Advisory: always exit 0. Findings are compress-queue candidates, not
    # build failures (see the module docstring).
    return 0


if __name__ == "__main__":
    sys.exit(main())
