#!/usr/bin/env python3
"""Delta gate D10: CLAUDE.md size ratchet (TODO 3.139.2).

`.claude/CLAUDE.md` is loaded EVERY turn, so its length is a per-turn token +
performance tax. Phase 1 (3.139.1) cut it from 1971 to 1506 lines by relocating
the PR-lifecycle prose to `references/pr-lifecycle.md`. This gate LOCKS IN that
gain and prevents regrowth: it FAILS when CLAUDE.md exceeds a hand-maintained
ceiling constant.

The ceiling is a DOWNWARD RATCHET: the maintainer only ever LOWERS it. Every
future relocation PR that shrinks CLAUDE.md also lowers CEILING in the same PR,
marching toward the ~800-900 goal and making each gain permanent. The gate never
fails on a decrease; it fails on any increase past the constant, which forces new
content to relocate to references/ rather than swell the every-turn load.

FAIL (not WARN) is deliberate: a size WARN is the advisory shape that gets skimmed
past, and the whole purpose is to FORCE relocation instead of regrowth. Blocking a
large addition until it is trimmed or relocated is exactly the desired behaviour.

Reads the working-tree file by explicit path (the `.claude/` exempt-dir walk does
not apply to an explicit-path read), so like D8 it needs no merge base.

Exit: 0 = at or under ceiling; 1 = over ceiling; 2 = file missing / error.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO_ROOT / ".claude" / "CLAUDE.md"

# Downward ratchet. LOWER this (never raise it) as CLAUDE.md shrinks. Current
# size at adoption (3.139.2): 1506 lines; ~3% headroom absorbs this PR's own
# lean-checklist edits and normal small changes while blocking ~50-line regrowth.
CEILING = 1550


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def evaluate(count: int, ceiling: int) -> tuple[int, str]:
    """Pure decision: (exit_code, message). Testable without the filesystem."""
    if count > ceiling:
        return (
            1,
            f"FAIL: .claude/CLAUDE.md is {count} lines, over the {ceiling}-line "
            f"ceiling (D10 size ratchet). Relocate content to references/ (read at "
            f"its activity boundary) rather than growing the every-turn load; do NOT "
            f"raise CEILING in tools/check-claude-md-size.py (it only ratchets down).",
        )
    return (
        0,
        f"D10 OK: .claude/CLAUDE.md is {count} lines (ceiling {ceiling}).",
    )


def run() -> int:
    if not CLAUDE_MD.is_file():
        print(f"ERROR: {CLAUDE_MD} not found", file=sys.stderr)
        return 2
    try:
        count = line_count(CLAUDE_MD)
    except OSError as exc:
        print(f"ERROR: cannot read {CLAUDE_MD}: {exc}", file=sys.stderr)
        return 2
    code, msg = evaluate(count, CEILING)
    print(msg, file=sys.stderr if code else sys.stdout)
    return code


def _self_test() -> int:
    import unittest

    class D10Tests(unittest.TestCase):
        def test_under_ceiling_passes(self):
            self.assertEqual(evaluate(1506, 1550)[0], 0)

        def test_at_ceiling_passes(self):
            self.assertEqual(evaluate(1550, 1550)[0], 0)

        def test_over_ceiling_fails(self):
            code, msg = evaluate(1551, 1550)
            self.assertEqual(code, 1)
            self.assertIn("1551", msg)
            self.assertIn("ceiling", msg)

        def test_message_names_the_ratchet_direction(self):
            self.assertIn("ratchet", evaluate(2000, 1550)[1].lower())

    suite = unittest.TestLoader().loadTestsFromTestCase(D10Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="D10: CLAUDE.md size ratchet")
    ap.add_argument("--self-test", action="store_true", help="run inline unit tests")
    args = ap.parse_args(argv)
    if args.self_test:
        return _self_test()
    return run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
