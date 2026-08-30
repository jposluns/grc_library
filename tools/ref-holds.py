#!/usr/bin/env python3
"""Answer "is X held in grc_library_ref?" from the AUTHORITATIVE index, not a partial grep.

Forcing-function orchestrator aid (advisory, NOT an audit gate). A held / not-held claim
about the reference base MUST quote this tool's output, never a bare filename grep. The
2026-07-17 lesson that motivated it: a partial ``grep -rlE '27002' ... | head -1`` grabbed
a vendor publication and wrongly concluded "ISO/IEC 27002:2022 is not held", when the ref
index lists the standard plainly. This is the `evidence-grounded-completion`
"inventory/absence claims require the index, not a partial look" corollary, mechanized the
same executed-not-narrated way: run it, quote it, never narrate from memory.

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
  0  at least one index match (HELD); OR, on an adopter clone with the reference
     sibling absent, a clean advisory no-op (nothing to report), per the #1792 degrade
  1  no index match (NOT-FOUND-IN-INDEX)
  2  the ref index could not be read (locate grc_library_ref, or pass --ref-root)
Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lint_common import REPO_ROOT, resolve_sibling

# Default: grc_library_ref is a sibling of the repo containing this tool.
DEFAULT_REF_ROOT = REPO_ROOT.parent / "grc_library_ref"

INDEX_FILES = ("INDEX.md", "catalogue.yml", "SECTION-INDEX.md", "COVERAGE-MAP.md")


def find_ref_root(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        return p if (p / "INDEX.md").exists() or (p / "catalogue.yml").exists() else None
    # Default: the real grc_library_ref sibling, located via the shared resolver
    # (1.19.2 (closing PR #996)). None on a portable clone that has no sibling.
    sibling = resolve_sibling("ref")
    if sibling is not None and (
        (sibling / "INDEX.md").exists() or (sibling / "catalogue.yml").exists()
    ):
        return sibling
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


def _identity_is_adopter(identity: dict) -> bool:
    """PURE decision over a detect-env ``probe_identity`` result: an operator is an
    adopter ONLY on a SUCCESSFULLY-READ, non-maintainer origin. A None/absent
    ``origin_url`` is NOT treated as adopter -- detect-env swallows a git-origin
    probe FAILURE (e.g. a subprocess timeout, rc 124) into a None origin, which
    ``probe_identity`` then classifies as ``adopter``; keying on that classification
    alone would let a MAINTAINER's transient git timeout silently no-op the
    missing-grc_library_ref HALT. Fail SAFE: only a positively-read fork/private
    origin degrades; a None origin, a maintainer origin, or any missing field ->
    False (loud). Pure + injectable so the fail-safe is regression-locked (the
    guard-input pure-decision-behind-a-thin-observer discipline)."""
    origin_url = identity.get("origin_url")
    # Degrade ONLY on a fully-formed non-maintainer identity: a non-empty STRING
    # origin_url AND the maintainer flag EXACTLY False. isinstance-guarding the url
    # (probe_identity yields str|None) and requiring `is False` make the decision
    # monotonically fail-safe: any None/empty/non-str origin, or any non-exactly-
    # False flag, -> False (loud). This TRUSTS probe_identity to produce a (url,
    # flag) pair consistent with each other (the flag is derived from the url); a
    # dict whose flag CONTRADICTS its url is non-producible by that observer, and
    # re-deriving maintainer-ness from the url here would duplicate detect-env's
    # canonical origin check (forbidden by the guard-input single-source rule).
    return isinstance(origin_url, str) and bool(origin_url) and identity.get("origin_is_maintainer_repo") is False


def _operator_is_adopter() -> bool:
    """True ONLY if the operator has a positively-read, non-maintainer origin (see
    _identity_is_adopter). Maintainer / maintainer-fresh-machine / undetermined /
    absent-or-unreadable origin / any error -> False, so a maintainer's
    genuinely-missing grc_library_ref stays a LOUD exit-2 failure (the 1.19.7
    (closing PR #1007) loud gate that /orch relies on). Reuses the SINGLE canonical
    identity source (detect-env.py) via importlib (the file is hyphenated, so not
    import-able by name) rather than duplicating the origin check here (the
    guard-input single-source discipline). Only reached on the rare absent-ref
    branch, so the probe cost is not on any hot path."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "detect_env", str(Path(__file__).resolve().parent / "detect-env.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return _identity_is_adopter(mod.probe_identity(mod.probe_siblings()))
    except Exception:
        return False


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
        # A GENUINELY ABSENT default sibling on an ADOPTER clone degrades to an
        # advisory no-op (exit 0), per 1.19.2 (closing PR #996): ref-holds is a
        # maintainer-only forcing-function tool, and an adopter clone that never
        # fetched grc_library_ref has nothing to answer against. The branch is
        # gated on the detect-env OPERATOR IDENTITY (adopter -> graceful; a
        # maintainer / undetermined identity stays a LOUD exit 2, the 1.19.7 loud
        # gate /orch relies on), NOT on the committed .ref placeholder, which is
        # NOT shipped by default (a fresh adopter clone has no .ref, so the old
        # placeholder gate errored spuriously -- deep-assessment 3.183(3)). It is
        # further gated on resolve_sibling("ref") is None (the real sibling dir
        # truly absent), NOT merely on find_ref_root being None: a real
        # grc_library_ref dir that EXISTS but lacks its index (a corrupt/partial
        # checkout) still errors (exit 2), so a broken ref is surfaced, not masked.
        # An EXPLICIT --ref-root that did not resolve likewise stays the operator's
        # mistake to surface (exit 2).
        if (
            a.ref_root is None
            and resolve_sibling("ref") is None
            and _operator_is_adopter()
        ):
            print(
                "advisory: grc_library_ref sibling absent (adopter clone); "
                "ref-holds is a maintainer-only advisory, nothing to report."
            )
            return 0
        print(
            "ERROR: could not locate the grc_library_ref index. Pass --ref-root /path/to/grc_library_ref "
            f"(looked for {DEFAULT_REF_ROOT}).",
            file=sys.stderr,
        )
        return 2
    return run(ref_root, a.query)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
