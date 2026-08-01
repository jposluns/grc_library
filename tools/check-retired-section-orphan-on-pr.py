#!/usr/bin/env python3
"""Delta gate D9: retired-section-orphan check (roadmap C phase 2, #1250).

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

Four FP guards:
1. RENUMBER/REWORD: an id is retired only if it is NOT a heading in TODO.md at
   HEAD (an in-place reword/split/reorder keeps the id, so references stay valid).
2. HISTORICAL NARRATION: each hit is classified (shared lint_common.classify);
   only LIVE hits are violations. NOTE (dual-family verify, #1250): for D9's
   current scan set this guard is SCOPE-MOOT defence-in-depth, because
   operational_files() never yields a LEDGER (CHANGELOG.md / .working/history)
   or frozen-record path, so classify() always returns LIVE here; the historical
   ledgers are excluded by SCOPE, not by this filter. It is retained (harmless)
   so a future scan-set expansion into .working/ inherits the exemption. A
   genuine historical `§N.M` note that DOES land on an operational surface is
   handled by the SectionRef opt-out or by rewording it to cite the closing PR
   (the permanence rule), which is the correct disposition anyway.
3. IN-PR TEACHING: a `SectionRef: <reason>` commit trailer opts out (for the rare
   PR that legitimately adds a live `§N.M` teaching citation in the same change).
4. PUBLIC/PRIVATE MIGRATION: when a PR MOVES a numbered section from the public
   TODO.md to the private P-TODO.md (keeping its number, so the id stays LIVE but
   in a list this gate cannot read in public CI), the `SectionRef:` opt-out is the
   INTENDED mechanism (maintainer decision 2026-08-01, closing the two-list-
   awareness backlog item won't-fix-the-CI-way). P-TODO.md lives in the private
   sibling, which is never checked out in public GitHub CI, so this gate running in
   CI cannot see the migration destination; a `resolve_sibling`-based two-list read
   is a no-op in CI while working locally (a local-pass/CI-fail split, why that fix
   was reverted). The opt-out, with a reason naming the migration, is correct.

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
HEADING_RE = re.compile(r"^#{3,6}\s+(?:§\s*)?(\d+(?:\.\d+){1,3})\b")


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
    # Only the FOUR documented, UNAMBIGUOUS forms (each carries a §/P/section
    # marker). Bare `TODO N.M` (no §) is deliberately EXCLUDED: it is ambiguous
    # with an ordinary `# TODO 3.1 fix this` code comment, so it stays convention.
    # The right-guard `(?![\w.])` rejects a following word char OR dot, so `§3.1`
    # never matches inside `§3.10`, `§3.1.2`, or a suffix id like `P3.1x`.
    return re.compile(
        r"(?:"
        r"§\s*" + esc + r"|"                    # §N.M
        r"\bP" + esc + r"|"                     # PN.M
        r"\bTODO\s+§\s*" + esc + r"|"         # TODO §N.M
        r"\bTODO\s+section\s+" + esc +        # TODO section N.M
        r")(?![\w.])"
    )


def find_orphans(section_ids: set[str], files: list[tuple[str, str]]) -> list[tuple[str, int, str]]:
    """Return (relpath, lineno, line) for each LIVE surviving anchored reference.

    PURE given (relpath, text) pairs. FP guard #2 (classify) is applied here
    (scope-moot for D9's current surfaces; see the module docstring).
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


def in_scope(rel: str) -> bool:
    """PURE: is repo-relative `rel` one of D9's operational-complement surfaces?

    This is the FP-safety-critical scope decision, isolated so it is directly
    testable. IN scope: anything under `.claude/` or `references/`; `tools/*.py`
    and `tools/*.sh`; a root-level `*.sh`; `.github/**/*.yml|*.yaml`; `TODO.md`.
    OUT of scope (owned by other gates): the corpus `.md` (18/62/65) and the pack
    subtree `dev-security/claude-rules/` (lint-positional-backlog-tokens); `.git/`.
    """
    if rel.startswith(".git/") or rel.startswith("dev-security/claude-rules/"):
        return False
    if rel == "TODO.md":
        return True
    if rel.startswith(".claude/") or rel.startswith("references/"):
        return True
    if rel.startswith("tools/") and (rel.endswith(".py") or rel.endswith(".sh")):
        return True
    if "/" not in rel and rel.endswith(".sh"):  # root-level shell script
        return True
    if rel.startswith(".github/") and (rel.endswith(".yml") or rel.endswith(".yaml")):
        return True
    return False


def operational_files() -> list[tuple[str, str]]:
    """The operational-complement surface set, as (relpath, text) at HEAD.

    Collects candidates from the in-scope roots, then filters through the pure
    `in_scope` predicate (the single source of truth for scope).
    """
    cand: list[Path] = []
    for r in (".claude", "references", ".github"):
        d = REPO_ROOT / r
        if d.is_dir():
            cand += [p for p in d.rglob("*") if p.is_file()]
    cand += list((REPO_ROOT / "tools").glob("*"))
    cand += list(REPO_ROOT.glob("*.sh"))
    todo = REPO_ROOT / "TODO.md"
    if todo.is_file():
        cand.append(todo)
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for p in cand:
        rel = p.relative_to(REPO_ROOT).as_posix()
        if rel in seen or not in_scope(rel):
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
    # Require a non-empty reason: a bare `SectionRef:` (or `SectionRef: `) must
    # NOT disable the gate wholesale (a guard with a costless bypass is no guard).
    for line in log.splitlines():
        s = line.strip()
        if s.lower().startswith("sectionref:") and s[len("sectionref:"):].strip():
            return True
    return False


def run(base: str | None, head: str) -> int:
    # A provided base (the runner passes `${BASE_REF:-origin/main}`, a branch
    # TIP) is merge-based against head before diffing, exactly as the sibling
    # delta gates do: diffing a raw tip on a behind-main branch would show
    # main-added headings as `-` lines and mis-derive them as retired (a real
    # FP vector, dual-family-caught). Argless default honours GITHUB_BASE_REF
    # (the PR's target branch) like the other gates, falling back to origin/main.
    import os
    if base is None:
        target = os.environ.get("GITHUB_BASE_REF", "").strip() or "main"
        base = f"origin/{target}"
    try:
        merge_base = git("merge-base", base, head).strip()
        todo_diff = git("diff", merge_base, head, "--", "TODO.md")
        head_todo = git("show", f"{head}:TODO.md")
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git failed (base={base}, head={head}): {exc}", file=sys.stderr)
        return 2
    base = merge_base
    # NOTE: retired ids + TODO.md come from the `head` git object, but the orphan
    # scan reads the WORKING TREE (operational_files reads files from disk). In
    # the pre-push guard and CI, HEAD IS the checked-out working tree, so the two
    # agree; D9 assumes head == working tree and is not meant for an arbitrary
    # non-checked-out head ref.
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

    class D9Tests(unittest.TestCase):
        # --- retired-id derivation (FP guard #1: renumber) ---
        def test_retired_id_derivation(self):
            diff = "-### 3.9 old thing\n+### 3.10 new thing\n"
            self.assertEqual(retired_ids(diff, "### 3.10 new thing\n"), {"3.9"})

        def test_renumber_in_place_not_retired(self):
            diff = "-### 3.9 reworded\n+### 3.9 reworded better\n"
            self.assertEqual(retired_ids(diff, "### 3.9 reworded better\n"), set())

        def test_heading_needs_three_hashes(self):
            # a level-2 `## 3.9` is not a TODO item heading
            self.assertEqual(ids_in_headings("## 3.9 not an item\n"), set())
            self.assertEqual(ids_in_headings("### 3.9 an item\n"), {"3.9"})

        # --- anchored-pattern precision (FP guards) ---
        def test_live_orphan_flagged(self):
            self.assertEqual(len(find_orphans({"3.9"}, [(CLAUDE, "see §3.9 for detail")])), 1)

        def test_substring_not_matched(self):
            # right-guard: §3.6 must not match inside §3.60
            self.assertIsNone(anchored_patterns("3.6").search("see §3.60 here"))

        def test_child_decimal_not_matched(self):
            # right-guard rejects a following dot: §3.6 must not match §3.6.1
            self.assertIsNone(anchored_patterns("3.6").search("see §3.6.1 here"))

        def test_letter_suffix_not_matched(self):
            # right-guard rejects a following letter: 3.1 must not match P3.1x
            self.assertIsNone(anchored_patterns("3.1").search("per P3.1x above"))

        def test_bare_todo_not_matched(self):
            # § is REQUIRED; ambiguous bare `TODO 3.1` (a code comment) is not a match
            self.assertIsNone(anchored_patterns("3.1").search("# TODO 3.1 fix this later"))

        def test_bare_number_not_matched(self):
            self.assertIsNone(anchored_patterns("3.9").search("version 3.9 shipped"))

        def test_todo_section_and_P_forms_matched(self):
            self.assertTrue(anchored_patterns("3.9").search("per P3.9 above"))
            self.assertTrue(anchored_patterns("3.9").search("TODO section 3.9 detail"))
            self.assertTrue(anchored_patterns("3.9").search("TODO §3.9 detail"))

        # --- scope (the FP-safety-critical in_scope predicate) ---
        def test_in_scope_excludes_corpus_and_pack(self):
            self.assertFalse(in_scope("ai/some-doc.md"))          # corpus
            self.assertFalse(in_scope("compliance/matrix.md"))    # corpus
            self.assertFalse(in_scope("dev-security/claude-rules/governance/x.md"))  # pack
            self.assertFalse(in_scope("tools/foo.md"))            # tools but not .py/.sh
            self.assertFalse(in_scope(".github/x.md"))            # .github but not yaml

        def test_in_scope_includes_operational(self):
            self.assertTrue(in_scope(".claude/CLAUDE.md"))
            self.assertTrue(in_scope("references/pr-lifecycle.md"))
            self.assertTrue(in_scope("tools/check-x.py"))
            self.assertTrue(in_scope("tools/run.sh"))
            self.assertTrue(in_scope("run.sh"))
            self.assertTrue(in_scope(".github/workflows/quality.yml"))
            self.assertTrue(in_scope("TODO.md"))

        # --- classify (currently scope-moot defence-in-depth; still validate the branch) ---
        def test_ledger_narration_not_flagged(self):
            self.assertEqual(find_orphans({"3.9"}, [(LEDGER, "§3.9 closed in #814")]), [])

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
