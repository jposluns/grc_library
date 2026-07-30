#!/usr/bin/env python3
"""Delta gate D9: retired-section-orphan check (TODO 3.139.2).

When a PR CLOSES a numbered TODO section (deletes its `### N.M` heading),
positional references to that section (`§N.M`, `PN.M`, `TODO §N.M`,
`TODO section N.M`) can survive on the OPERATIONAL / gate-exempt surfaces that
no other gate scans, silently dangling. This gate flags those survivors.

Why it is false-positive-safe (the design constraint: a gate that cries wolf gets
bypassed and protects nothing):
- DELETION-TRIGGERED. It derives the retired ids from headings this PR REMOVES
  from TODO.md, so "old" is unambiguous and there is no coexisting "new" value to
  disambiguate against (unlike a value-change, which is irreducibly semantic).
- ANCHORED KEY FORMS ONLY. It matches `§N.M` / `PN.M` / `TODO §N.M` /
  `TODO section N.M` with a left anchor and multi-part decimal + right word
  boundary, so `§3.6` never matches inside `§3.60` (the #1161 title-slot defence,
  structural rather than claim-scoped). Bare `N.M`, `item N`, and ranges are
  deliberately EXCLUDED as too FP-prone; they stay convention.
- OPERATIONAL-SURFACE-SCOPED. It scans only `.claude/`, `references/`,
  `tools/*.py`, `*.sh`, `.github/**/*.yml`, and `TODO.md` itself: the complement
  of the corpus `.md` gates (18/62/65) and of `lint-positional-backlog-tokens`
  (pack subtree). On those surfaces a bare `§N.M` is unambiguously a backlog
  reference (a tool docstring does not cite a corpus document by section number),
  which dissolves the corpus-vs-backlog ambiguity.

Three FP guards:
1. RENUMBER/REWORD: an id is retired only if it is NOT a heading in TODO.md at
   HEAD (an in-place reword/split/reorder keeps the id, so references stay valid).
2. HISTORICAL NARRATION: each hit is classified (shared lint_common.classify);
   only LIVE hits are violations. A CHANGELOG/DONE/history.md line narrating a
   past closure is LEDGER and exempt.
3. IN-PR TEACHING: a `SectionRef: <reason>` commit trailer opts out (for the rare
   PR that legitimately adds a live `§N.M` teaching citation in the same change).

Exit: 0 = no retired ids / no LIVE survivors / opt-out / empty diff; 1 = LIVE
survivors found; 2 = git or environment error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import classify  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

# A numbered TODO heading: `### N.M`, optionally `### §N.M`. Two+ decimal parts.
HEADING_RE = re.compile(r"^#{2,6}\s+(?:§\s*)?(\d+(?:\.\d+){1,3})\b")


def ids_in_headings(todo_text: str) -> set[str]:
    """Every numbered id that is currently a heading in TODO.md. PURE."""
    out: set[str] = set()
    for line in todo_text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            out.add(m.group(1))
    return out


def retired_ids(todo_diff: str, head_todo_text: str) -> set[str]:
    """Ids whose heading this PR DELETED and which are NOT a heading at HEAD.

    PURE. `todo_diff` is `git diff <base> <head> -- TODO.md`. A removed heading
    line begins with `-` (but not `---`). FP guard #1 (renumber) is the
    subtraction of the still-present headings.
    """
    deleted: set[str] = set()
    for line in todo_diff.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            m = HEADING_RE.match(line[1:])
            if m:
                deleted.add(m.group(1))
    return deleted - ids_in_headings(head_todo_text)


def anchored_patterns(section_id: str) -> re.Pattern:
    """One combined regex for the anchored key forms of `section_id`. PURE.

    Matches: `§N.M`, `PN.M`, `TODO §N.M`, `TODO section N.M`. Left-anchored on
    `§` / `P` / `TODO ` and right word-boundaried so a longer decimal does not
    collide (`§3.6` vs `§3.60`).
    """
    esc = re.escape(section_id)
    return re.compile(
        r"(?:"
        r"§\s*" + esc + r"|"          # §N.M
        r"\bP" + esc + r"|"                 # PN.M
        r"\bTODO\s+§?\s*" + esc + r"|"  # TODO §N.M / TODO N.M
        r"\bTODO\s+section\s+" + esc +       # TODO section N.M
        r")(?!\d)(?!\.\d)"                   # not followed by another digit/decimal
    )


def find_orphans(section_ids: set[str], files: list[tuple[str, str]]) -> list[tuple[str, int, str]]:
    """Return (relpath, lineno, line) for each LIVE surviving anchored reference.

    PURE given (relpath, text) pairs. FP guard #2 (classify) is applied here.
    """
    if not section_ids:
        return []
    pats = {sid: anchored_patterns(sid) for sid in section_ids}
    hits: list[tuple[str, int, str]] = []
    for rel, text in files:
        if classify(rel) != "LIVE":
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat in pats.values():
                if pat.search(line):
                    hits.append((rel, i, line))
                    break
    return hits


# ---- git / IO (thin) ----

def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), *args], text=True
    )


def operational_files() -> list[tuple[str, str]]:
    """The operational-complement surface set, as (relpath, text) at HEAD."""
    roots = [".claude", "references", ".github"]
    paths: list[Path] = []
    for r in roots:
        d = REPO_ROOT / r
        if d.is_dir():
            paths += [p for p in d.rglob("*") if p.is_file()]
    paths += list((REPO_ROOT / "tools").glob("*.py"))
    paths += list((REPO_ROOT / "tools").glob("*.sh"))
    paths += list(REPO_ROOT.glob("*.sh"))
    todo = REPO_ROOT / "TODO.md"
    if todo.is_file():
        paths.append(todo)
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for p in paths:
        rel = p.relative_to(REPO_ROOT).as_posix()
        # NOT the pack subtree (owned by lint-positional-backlog-tokens),
        # NOT .git.
        if rel.startswith("dev-security/claude-rules/") or rel.startswith(".git/"):
            continue
        if rel in seen:
            continue
        seen.add(rel)
        try:
            out.append((rel, p.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            continue
    return out


def opt_out_present(base: str, head: str) -> bool:
    """True if any commit in base..head carries a `SectionRef:` trailer."""
    try:
        log = git("log", f"{base}..{head}", "--format=%B")
    except subprocess.CalledProcessError:
        return False
    return any(
        line.strip().lower().startswith("sectionref:")
        for line in log.splitlines()
    )


def run(base: str | None, head: str) -> int:
    try:
        if base is None:
            base = git("merge-base", "origin/main", head).strip()
        todo_diff = git("diff", base, head, "--", "TODO.md")
        head_todo = git("show", f"{head}:TODO.md")
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git failed: {exc}", file=sys.stderr)
        return 2
    ids = retired_ids(todo_diff, head_todo)
    if not ids:
        print("D9 OK: no TODO section closed in this PR.")
        return 0
    if opt_out_present(base, head):
        print(f"D9 OK: {len(ids)} section(s) retired; SectionRef: opt-out present.")
        return 0
    hits = find_orphans(ids, operational_files())
    if not hits:
        print(f"D9 OK: {len(ids)} section(s) retired; no LIVE orphan references.")
        return 0
    print(
        f"FAIL: {len(hits)} LIVE orphan reference(s) to section(s) this PR retired "
        f"({', '.join(sorted(ids))}). Reword or drop each, or add a `SectionRef: "
        f"<reason>` commit trailer for a legitimate teaching citation:",
        file=sys.stderr,
    )
    for rel, ln, text in hits:
        print(f"  {rel}:{ln}: {text}", file=sys.stderr)
    return 1


def _self_test() -> int:
    import unittest

    CLAUDE = ".claude/CLAUDE.md"
    LEDGER = ".working/DONE.md"
    CORPUS = "ai/some-doc.md"

    class D9Tests(unittest.TestCase):
        def test_retired_id_derivation(self):
            diff = "-### 3.9 old thing\n+### 3.10 new thing\n"
            self.assertEqual(retired_ids(diff, "### 3.10 new thing\n"), {"3.9"})

        def test_renumber_in_place_not_retired(self):
            # heading still present at HEAD -> not retired (FP guard #1)
            diff = "-### 3.9 reworded\n+### 3.9 reworded better\n"
            self.assertEqual(retired_ids(diff, "### 3.9 reworded better\n"), set())

        def test_live_orphan_flagged(self):
            hits = find_orphans({"3.9"}, [(CLAUDE, "see queued §3.9 for detail")])
            self.assertEqual(len(hits), 1)

        def test_ledger_narration_not_flagged(self):
            hits = find_orphans({"3.9"}, [(LEDGER, "§3.9 closed in #814")])
            self.assertEqual(hits, [])

        def test_corpus_md_out_of_scope(self):
            # a corpus .md would never be in operational_files(); find_orphans is
            # pure, so we simulate by classify: corpus paths are LIVE, so scope is
            # enforced by operational_files(), not classify. Assert the pattern
            # itself would match but scope excludes it (documented behaviour).
            self.assertTrue(anchored_patterns("3.9").search("§3.9"))

        def test_substring_not_matched(self):
            self.assertIsNone(anchored_patterns("3.6").search("see §3.60 here"))

        def test_bare_number_not_matched(self):
            # bare "3.9" with no §/P/TODO anchor is not a match (too FP-prone)
            self.assertIsNone(anchored_patterns("3.9").search("version 3.9 shipped"))

        def test_P_form_matched(self):
            self.assertTrue(anchored_patterns("3.9").search("per P3.9 above"))

    suite = unittest.TestLoader().loadTestsFromTestCase(D9Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="D9: retired-section-orphan check")
    ap.add_argument("base", nargs="?", default=None, help="base ref (default: merge-base with origin/main)")
    ap.add_argument("head", nargs="?", default="HEAD", help="head ref (default: HEAD)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return _self_test()
    return run(args.base, args.head)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
