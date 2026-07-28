#!/usr/bin/env python3
"""Statusline `next:` segment (private-aware).

Reads the Claude Code statusline JSON on stdin, resolves the next-PR queue file
via ``resolve_working`` (private sibling preferred, in-repo fallback), and prints
``next: <first queue line>``. The queue file's first line carries the whole
``1) ...; 2) ...; 3) ...`` item list (per the project's next-prs.txt format); the
console surfaces only that line and truncates it near 120 characters, so this
wrapper emits it verbatim rather than parsing individual items.

Kept as a wrapper (not inline bash) so the ``.working/next-prs.txt`` -> private
sibling migration is a one-line resolver change here rather than a ``settings.json``
edit. Fails soft: any error prints a plain ``next:`` note and exits 0, so the
statusline never breaks the prompt.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
_DEFAULT_ROOT = Path(__file__).resolve().parent.parent


def _repo_root(data: dict) -> Path:
    d = ""
    if isinstance(data, dict):
        ws = data.get("workspace")
        if isinstance(ws, dict):
            d = ws.get("project_dir") or ""
    return Path(d) if d else _DEFAULT_ROOT


def _resolve_queue(root: Path) -> Path | None:
    if _TOOLS_DIR not in sys.path:
        sys.path.insert(0, _TOOLS_DIR)
    try:
        from lint_common import resolve_working
        return resolve_working("next-prs.txt", repo_root=root)
    except Exception:
        cand = root / ".working" / "next-prs.txt"
        return cand if cand.exists() else None


def _segment(f: Path | None) -> str:
    if f is None or not f.is_file():
        return "next: (queue file missing)"
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.match(r"^[0-9]", ln):
            return "next: " + ln.strip()
    return "next: (queue empty)"


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return _self_test()
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    root = _repo_root(data if isinstance(data, dict) else {})
    sys.stdout.write(_segment(_resolve_queue(root)))
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    seg = _segment

    class T(unittest.TestCase):
        def test_missing(self):
            with tempfile.TemporaryDirectory() as td:
                self.assertIn("missing", seg(Path(td) / "nope.txt"))

        def test_first_line_verbatim(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "q.txt"
                p.write_text("1) a; 2) b; 3) c\n# then: more detail\n", encoding="utf-8")
                self.assertEqual(seg(p), "next: 1) a; 2) b; 3) c")

        def test_skips_leading_comment(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "q.txt"
                p.write_text("# header\n1) only item\n", encoding="utf-8")
                self.assertEqual(seg(p), "next: 1) only item")

        def test_empty(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "q.txt"
                p.write_text("# then: only a comment\n", encoding="utf-8")
                self.assertIn("empty", seg(p))

    res = unittest.TextTestRunner(verbosity=1).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
