#!/usr/bin/env python3
"""Answer "is X held in grc_library_ref?" from the AUTHORITATIVE index, not a partial grep.

Forcing-function orchestrator aid (advisory, NOT an audit gate). A held / not-held claim
about the reference base MUST quote this tool's output, never a bare filename grep. The
2026-07-17 lesson that motivated it: a partial ``grep -rlE '27002' ... | head -1`` grabbed
a vendor publication and wrongly concluded "ISO/IEC 27002:2022 is not held", when the ref
index lists the standard plainly. This is the `evidence-grounded-completion`
"inventory/absence claims require the index, not a partial look" corollary, mechanized the
same way ``audit-delivery-status.py`` mechanized delivery-status claims: run it, quote it.

WHAT IT DOES. It searches the reference base's OWN index files (``INDEX.md`` and
``catalogue.yml``; ``SECTION-INDEX.md`` / ``COVERAGE-MAP.md`` if present) for the query as a
case-insensitive substring over titles, ids, and paths, and reports every match (with the
held path and, where the catalogue records it, the version / checked-edition) as HELD, or
reports NOT-FOUND-IN-INDEX. A not-found result means "absent from the index", and the index
is the authority for what is held; it does not license a from-memory assertion, and if the
index itself may be stale that is a separate check (the reference-version-currency SOP).

Usage:
  python3 tools/ref-holds.py "27002"
  python3 tools/ref-holds.py "ISO/IEC 27002:2022"
  python3 tools/ref-holds.py "MITRE ATT&CK"
  python3 tools/ref-holds.py --ref-root /path/to/grc_library_ref "CSF 2.0"
  python3 tools/ref-holds.py --self-test

Exit codes:
  0  at least one index match (HELD)
  1  no index match (NOT-FOUND-IN-INDEX)
  2  the ref index could not be read (locate grc_library_ref, or pass --ref-root)
Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Default: grc_library_ref is a sibling of the repo containing this tool.
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REF_ROOT = REPO_ROOT.parent / "grc_library_ref"

INDEX_FILES = ("INDEX.md", "catalogue.yml", "SECTION-INDEX.md", "COVERAGE-MAP.md")


def find_ref_root(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        return p if (p / "INDEX.md").exists() or (p / "catalogue.yml").exists() else None
    if (DEFAULT_REF_ROOT / "INDEX.md").exists() or (DEFAULT_REF_ROOT / "catalogue.yml").exists():
        return DEFAULT_REF_ROOT
    return None


def search_index(ref_root: Path, query: str) -> list[tuple[str, int, str]]:
    """Return (index_file, line_no, line) for every line matching the query (case-insensitive)."""
    q = query.lower()
    hits: list[tuple[str, int, str]] = []
    for name in INDEX_FILES:
        f = ref_root / name
        if not f.exists():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if q in line.lower():
                hits.append((name, i, line.strip()))
    return hits


def run(ref_root: Path, query: str, stream=sys.stdout) -> int:
    hits = search_index(ref_root, query)
    if not hits:
        print(
            f"NOT-FOUND-IN-INDEX: no entry matching {query!r} in the grc_library_ref index "
            f"({', '.join(n for n in INDEX_FILES if (ref_root / n).exists())}). "
            f"The index is the authority for what is held: 'not found' means not-in-the-index, "
            f"NOT a from-memory not-held claim. If the standard/framework is load-bearing, follow "
            f"the missing-reference SOP (attempt acquire / pause), and confirm the index itself is "
            f"current before relying on the negative.",
            file=stream,
        )
        return 1
    print(f"HELD: {len(hits)} index match(es) for {query!r} in grc_library_ref:", file=stream)
    # De-dupe identical lines across index files while preserving provenance of the first hit.
    seen: set[str] = set()
    for name, lineno, line in hits:
        key = line
        if key in seen:
            continue
        seen.add(key)
        print(f"  [{name}:{lineno}] {line[:240]}", file=stream)
    return 0


def _self_test() -> int:
    import io
    import tempfile
    import unittest

    class T(unittest.TestCase):
        def _mk(self, index_body: str) -> Path:
            d = Path(tempfile.mkdtemp())
            (d / "INDEX.md").write_text(index_body, encoding="utf-8")
            return d

        def test_held_match(self):
            d = self._mk(
                "- _[standards]_ ISO/IEC 27002:2022, Information security controls "
                "(`standards/ISO/ISO-IEC-27002-2022--full-text.md`)\n"
            )
            buf = io.StringIO()
            rc = run(d, "27002", stream=buf)
            self.assertEqual(rc, 0)
            self.assertIn("HELD", buf.getvalue())
            self.assertIn("27002", buf.getvalue())

        def test_not_found(self):
            d = self._mk("- _[standards]_ ISO/IEC 27001:2022 (`standards/ISO/x.md`)\n")
            buf = io.StringIO()
            rc = run(d, "NONESUCH-99999", stream=buf)
            self.assertEqual(rc, 1)
            self.assertIn("NOT-FOUND-IN-INDEX", buf.getvalue())

        def test_case_insensitive(self):
            d = self._mk("- MITRE ATT&CK Enterprise (`frameworks/MITRE/x.md`)\n")
            self.assertEqual(run(d, "mitre att&ck", stream=io.StringIO()), 0)

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description="Answer held/not-held for grc_library_ref from its index (forcing-function; quote the output).",
    )
    p.add_argument("query", nargs="?", help="Substring to search (title, id, or path).")
    p.add_argument("--ref-root", default=None, help="Path to grc_library_ref (default: sibling of this repo).")
    p.add_argument("--self-test", action="store_true", help="Run inline unit tests and exit.")
    a = p.parse_args(argv[1:])

    if a.self_test:
        return _self_test()
    if not a.query:
        print("ERROR: provide a query (or --self-test). Example: ref-holds.py \"27002\"", file=sys.stderr)
        return 2

    ref_root = find_ref_root(a.ref_root)
    if ref_root is None:
        print(
            "ERROR: could not locate the grc_library_ref index. Pass --ref-root /path/to/grc_library_ref "
            f"(looked for {DEFAULT_REF_ROOT}).",
            file=sys.stderr,
        )
        return 2
    return run(ref_root, a.query)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
