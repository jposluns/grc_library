#!/usr/bin/env python3
"""Run the reviewed store-dependent subset of gate 36 (pre-push, every push).

CI has no private store (GRC_STORE / <repo-parent>/private), no
grc_library_private sibling and no grc_library_ref sibling, so the gate-36
tests that skip or silently no-op without them never execute on the merge
path. The reviewed list tests/store-dependent-tests.txt names that subset
(one test id per line, with the reason); the pre-push guard runs this tool
on every push, so those tests execute, where their inputs exist, before
every merge. tests/test_store_dependent_list.py keeps the list honest: its
static scan of the suite must name exactly the listed tests.

List format: one entry per line, ``<test id> -- <reason>``, where the test
id is the dotted unittest name of ONE test method
(``tests.<module>.<Class>.<test_method>``). Blank lines and lines starting
with ``#`` are comments.

Fail closed (exit 2): a missing, unreadable or empty list, a malformed or
duplicate line, a listed id that is not a tests.* method id, a listed test
whose module, class or method cannot be loaded (unittest loader errors are
refusals, never skips), or a loaded entry that is not exactly the one named
test. Exit 1 when a listed test fails or errors; 0 on green. A listed test
that SKIPS here (this clone has no store or sibling either) is unittest's
ordinary skip, reported and green: the list run enforces that the tests are
RUN WHERE THEIR INPUTS EXIST (the maintainer's clone), and that the list
itself stays sound everywhere.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIST_PATH = REPO_ROOT / "tests" / "store-dependent-tests.txt"


def parse_list(text: str) -> list[str] | str:
    """The listed test ids in list order, or a string naming the refusal."""
    entries: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        test_id, sep, reason = line.partition(" -- ")
        test_id = test_id.strip()
        if not sep or not reason.strip():
            return ("line %d is not '<test id> -- <reason>': %r"
                    % (lineno, line))
        parts = test_id.split(".")
        if (len(parts) != 4 or parts[0] != "tests"
                or not all(part.isidentifier() for part in parts)):
            return ("line %d names %r, not a tests.<module>.<Class>."
                    "<test_method> id" % (lineno, test_id))
        if test_id in entries:
            return "line %d repeats %r" % (lineno, test_id)
        entries.append(test_id)
    if not entries:
        return "the list holds no test id"
    return entries


def main() -> int:
    try:
        text = LIST_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print("REFUSED: cannot read %s: %s (the reviewed store-dependent "
              "list is required on every push)"
              % (LIST_PATH.relative_to(REPO_ROOT), exc), file=sys.stderr)
        return 2
    entries = parse_list(text)
    if isinstance(entries, str):
        print("REFUSED: %s: %s"
              % (LIST_PATH.relative_to(REPO_ROOT), entries), file=sys.stderr)
        return 2
    if str(REPO_ROOT) not in sys.path:
        # Appended, not inserted: the repo root must not shadow the
        # standard library under python3 -I (gate 103).
        sys.path.append(str(REPO_ROOT))
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test_id in entries:
        loaded = loader.loadTestsFromName(test_id)
        if loader.errors:
            print("REFUSED: listed test %s cannot be loaded (a missing "
                  "listed test fails the push):\n%s"
                  % (test_id, "\n".join(loader.errors)), file=sys.stderr)
            return 2
        cases = list(loaded) if isinstance(loaded, unittest.TestSuite) else [loaded]
        if len(cases) != 1 or not isinstance(cases[0], unittest.TestCase) \
                or cases[0].id() != test_id:
            print("REFUSED: listed id %s did not load as exactly that one "
                  "test method (loaded %r)" % (test_id, cases),
                  file=sys.stderr)
            return 2
        suite.addTest(cases[0])
    print("Running %d store-dependent test(s) from %s:"
          % (len(entries), LIST_PATH.relative_to(REPO_ROOT)))
    for test_id in entries:
        print("  " + test_id)
    sys.stdout.flush()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stderr)
    result = runner.run(suite)
    if result.testsRun != len(entries):
        print("REFUSED: %d listed test(s), %d run; the list run must start "
              "every listed test" % (len(entries), result.testsRun),
              file=sys.stderr)
        return 2
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
