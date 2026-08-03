#!/usr/bin/env python3
"""Class-completeness pre-commit aid (P-1.5): surface every corpus occurrence of a
distinctive string BEFORE committing, so a fix applied to ONE instance is applied (or
routed) at the WIDTH OF THE CLASS, not just the one file the change started in.

The dual-family ``/validate-pr`` repeatedly caught the SAME defect surviving in OTHER
files after one instance was fixed (#1296 single-file install, #1297 register-column
overclaim): the fix-at-class-width discipline was applied REACTIVELY. This aid applies it
PROACTIVELY. When a change fixes a distinctive factual phrase or claim in one document,
run this with that phrase (or its distinctive bare token) and it prints the occurrences it
can find across the corpus, so each is fixed or routed in the SAME change and the sweep
finds none.

It is an ADVISORY aid, NOT a gate: the matches include the intended fix and legitimate
unrelated senses (it is FP-aware), so it REPORTS for human triage and its reporting path
ALWAYS exits 0. The author supplies the distinctive string; identifying WHICH phrase is
distinctive is left to the author, deliberately, rather than guessed from a diff (which
mis-fires on ordinary edited prose).

Honest completeness residue (this is a grep-class aid, not an oracle): matching is
substring- and LINE-scoped, so a distinctive phrase that WRAPS across a line break, or
that differs only by Unicode normalization, is not matched; and a file that cannot be read
as UTF-8 is reported as SKIPPED (named on stderr), never silently dropped. Pass the shorter
distinctive bare token if a phrase might wrap.

Usage:
    python3 tools/check-class-completeness.py "distinctive phrase"
    python3 tools/check-class-completeness.py -i "phrase"           # case-insensitive
    python3 tools/check-class-completeness.py "phrase A" "phrase B" # several at once
    python3 tools/check-class-completeness.py --self-test

Exit codes: the advisory reporting path is 0 always (it reports; it never blocks a commit);
2 on a usage error (no string given); 1 only from ``--self-test`` on a self-test failure
(which is how the wired regression test detects rot).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT, is_markdown_target  # noqa: E402


def corpus_files(root: Path = REPO_ROOT) -> list[Path]:
    """Every scannable corpus markdown FILE, via the shared ``is_markdown_target`` +
    ``DEFAULT_EXEMPT_DIRS`` primitive (``.git`` / ``.claude`` / ``.working`` /
    ``node_modules`` / ``references`` excluded), requiring a real file (``is_file``) so a
    directory that happens to end ``.md`` is not returned. This is deliberately BROADER than
    any single content linter's per-tool scan (it includes the generated ``docs/`` artefacts,
    the pack under ``guardrails/``, and ``.project-governance/``): broader is
    the SAFE direction for a class-completeness sweep, which wants to surface every occurrence
    it can read."""
    return sorted(p for p in root.rglob("*.md") if p.is_file() and is_markdown_target(p))


def find_occurrences(
    strings: list[str], files: list[Path], ignore_case: bool = False,
    root: Path = REPO_ROOT,
) -> tuple[dict[str, list[tuple[str, int, str]]], list[str]]:
    """Return ``(occurrences, skipped)``: ``occurrences`` is ``{string: [(relpath, lineno,
    line_text), ...]}``; ``skipped`` is the relpaths of files that could NOT be read (non-UTF-8
    or unreadable). Skipped files are RETURNED rather than silently dropped, so a caller can
    warn that the sweep is incomplete for them (the no-silent-caps discipline: a completeness
    aid must not hide a hole). Matching is substring- and line-scoped. Pure: no I/O beyond
    reading the given files, so it is directly unit-testable."""
    out: dict[str, list[tuple[str, int, str]]] = {s: [] for s in strings}
    skipped: list[str] = []
    needles = [(s, s.lower() if ignore_case else s) for s in strings]
    for f in files:
        try:
            rel = str(f.relative_to(root))
        except ValueError:
            rel = str(f)
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            skipped.append(rel)
            continue
        for lineno, raw in enumerate(text.splitlines(), 1):
            hay = raw.lower() if ignore_case else raw
            for s, needle in needles:
                if needle and needle in hay:
                    out[s].append((rel, lineno, raw.strip()))
    return out, skipped


def _self_test() -> int:
    import tempfile
    checks = []
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "a.md").write_text("The retention is 7 years here.\nUnrelated line.\n", encoding="utf-8")
        (root / "b.md").write_text("Also 7 years elsewhere.\nAND Seven Years spelled out.\n", encoding="utf-8")
        (root / "c.txt").write_text("7 years in a non-md file (out of scope).\n", encoding="utf-8")
        (root / "dir.md").mkdir()  # a DIRECTORY ending .md must NOT be treated as a file
        files = corpus_files(root)
        checks.append(("md-only-discovery", all(f.suffix == ".md" for f in files) and len(files) == 2))
        checks.append(("dir-named-md-excluded", not any(f.name == "dir.md" for f in files)))
        occ, skipped0 = find_occurrences(["7 years"], files, root=root)
        checks.append(("finds-both-md-instances", len(occ["7 years"]) == 2))
        checks.append(("reports-relpath-and-line", occ["7 years"][0][0] in ("a.md", "b.md") and occ["7 years"][0][1] >= 1))
        checks.append(("no-skips-on-readable", skipped0 == []))
        ci = find_occurrences(["seven years"], files, ignore_case=True, root=root)[0]
        cs = find_occurrences(["seven years"], files, ignore_case=False, root=root)[0]
        checks.append(("case-insensitive-matches", len(ci["seven years"]) == 1 and len(cs["seven years"]) == 0))
        multi = find_occurrences(["7 years", "Unrelated"], files, root=root)[0]
        checks.append(("multi-string-keys", set(multi) == {"7 years", "Unrelated"} and len(multi["Unrelated"]) == 1))
        checks.append(("empty-needle-safe", find_occurrences([""], files, root=root)[0][""] == []))
        # an unreadable (non-UTF-8) file is REPORTED as skipped, not silently dropped
        (root / "bad.md").write_bytes(b"\xff\xfe not utf-8 \x80\x81")
        _, skipped = find_occurrences(["7 years"], corpus_files(root), root=root)
        checks.append(("unreadable-file-reported-skipped", skipped == ["bad.md"]))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"check-class-completeness self-test: FAIL {bad}")
        return 1
    print(f"check-class-completeness self-test: OK ({len(checks)} checks)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("strings", nargs="*", help="distinctive string(s) to locate across the corpus")
    ap.add_argument("-i", "--ignore-case", action="store_true", help="case-insensitive match")
    ap.add_argument("--self-test", action="store_true", help="run the built-in self-test")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    if not args.strings:
        ap.print_usage(sys.stderr)
        print("ERROR: give at least one distinctive string (or --self-test).", file=sys.stderr)
        return 2
    files = corpus_files()
    occ, skipped = find_occurrences(args.strings, files, ignore_case=args.ignore_case)
    total = 0
    for s in args.strings:
        hits = occ[s]
        total += len(hits)
        print(f"\n=== {len(hits)} occurrence(s) of {s!r} ===")
        for rel, lineno, line in hits:
            print(f"  {rel}:{lineno}: {line[:120]}")
    if skipped:
        shown = ", ".join(skipped[:20]) + (" ..." if len(skipped) > 20 else "")
        print(
            f"\nWARNING: {len(skipped)} file(s) could not be read (non-UTF-8 or unreadable) and were "
            f"NOT searched, so the sweep is INCOMPLETE for them: {shown}",
            file=sys.stderr,
        )
    print(
        f"\nADVISORY: {total} occurrence(s) across {len(files) - len(skipped)} searched corpus "
        f"file(s)" + (f" ({len(skipped)} unreadable, see the WARNING)" if skipped else "") + ". "
        f"Confirm every instance is fixed or routed in this change (fix at the width of the class), "
        f"not only the one you started in. Matching is substring- and line-scoped, so a phrase that "
        f"wraps a line break is not matched. This aid never blocks; it surfaces the class."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
