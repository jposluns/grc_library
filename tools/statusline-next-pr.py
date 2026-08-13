#!/usr/bin/env python3
"""Statusline `next:` segment (private-aware).

Reads the Claude Code statusline JSON on stdin, locates the private
``grc_library_private/P-TODO.md`` via ``resolve_sibling``, parses its
``## Up next`` ordered work queue (the single source of truth for what the
orchestrator works on next; see that section's own header), and prints
``next: 1) <title>; 2) <title>; 3) <title>`` for the top three items,
truncated near 120 characters.

This replaced the retired ``next-prs.txt`` queue file: the ``## Up next``
section at the top of ``P-TODO.md`` is now the durable control surface, so
the statusline reads it directly rather than a separate mirror file. The
trailing ``[tags]`` on each queue line are stripped for the console.

Fails soft: any error (no private sibling on an adopter clone, no queue
section, a parse problem) prints a plain ``next:`` note and exits 0, so the
statusline never breaks the prompt.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
_DEFAULT_ROOT = Path(__file__).resolve().parent.parent

_ITEM_RE = re.compile(r"^(\d+)\)\s*(.+)$")
_TAGS_RE = re.compile(r"\s*\[[^\]]*\]\s*$")


def _repo_root(data: dict) -> Path:
    d = ""
    if isinstance(data, dict):
        ws = data.get("workspace")
        if isinstance(ws, dict):
            d = ws.get("project_dir") or ""
    return Path(d) if d else _DEFAULT_ROOT


def _resolve_queue(root: Path) -> Path | None:
    """Locate the private ``P-TODO.md`` holding the ``## Up next`` queue.

    Prefers ``resolve_sibling("private")`` (the canonical sibling-repo
    helper); falls back to ``<root>/../grc_library_private/P-TODO.md`` when
    ``lint_common`` is not importable. Returns ``None`` when no private
    sibling exists (an adopter clone), so the caller no-ops fail-soft.
    """
    if _TOOLS_DIR not in sys.path:
        sys.path.insert(0, _TOOLS_DIR)
    try:
        from lint_common import resolve_sibling
        sib = resolve_sibling("private")
        if sib is not None:
            cand = sib / "P-TODO.md"
            return cand if cand.is_file() else None
    except Exception:
        pass
    cand = root.parent / "grc_library_private" / "P-TODO.md"
    return cand if cand.is_file() else None


def _top_items(text: str, limit: int = 3) -> list[str]:
    """Return the first ``limit`` ``N)`` item titles under ``## Up next``.

    The section ends at the next ``## `` header, a ``# then`` line, or a
    ``---`` rule. Each item's trailing ``[tags]`` bracket is stripped.
    """
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("## Up next"):
            start = i + 1
            break
    if start is None:
        return []
    items: list[str] = []
    for ln in lines[start:]:
        s = ln.strip()
        if s.startswith("## ") or s.startswith("# then") or s == "---":
            break
        m = _ITEM_RE.match(s)
        if m:
            title = _TAGS_RE.sub("", m.group(2)).strip()
            if title:
                items.append(title)
                if len(items) >= limit:
                    break
    return items


def _segment(f: Path | None) -> str:
    if f is None or not f.is_file():
        return "next: (queue file missing)"
    text = f.read_text(encoding="utf-8", errors="replace")
    if "## Up next" not in text:
        return "next: (no queue section)"
    items = _top_items(text)
    if not items:
        return "next: (queue empty)"
    seg = "next: " + "; ".join(f"{i + 1}) {t}" for i, t in enumerate(items))
    if len(seg) > 120:
        seg = seg[:117].rstrip() + "..."
    return seg


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
    top = _top_items

    _QUEUE = (
        "## Up next (the single ordered work queue; top = do next)\n"
        "\n"
        "Position IS priority; the top item is next.\n"
        "\n"
        "1) First item title [integrity, priv]\n"
        "2) Second item title (with a paren note) [content, priv]\n"
        "3) Third item title\n"
        "4) Fourth item title\n"
        "5) Fifth item title\n"
        "\n"
        "# then: the migration cutover is blocked\n"
        "\n"
        "---\n"
        "\n"
        "## Triage disposition\n"
    )

    class T(unittest.TestCase):
        def test_missing(self):
            with tempfile.TemporaryDirectory() as td:
                self.assertIn("missing", seg(Path(td) / "nope.md"))

        def test_top_three_rendered(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "P-TODO.md"
                p.write_text(_QUEUE, encoding="utf-8")
                self.assertEqual(
                    seg(p),
                    "next: 1) First item title; "
                    "2) Second item title (with a paren note); "
                    "3) Third item title",
                )

        def test_tags_stripped(self):
            self.assertEqual(
                top("## Up next\n1) Title here [integrity, priv]\n")[0],
                "Title here",
            )

        def test_no_section(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "P-TODO.md"
                p.write_text("## Backlog\n1) not the up-next section\n", encoding="utf-8")
                self.assertIn("no queue section", seg(p))

        def test_empty_section(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "P-TODO.md"
                p.write_text("## Up next\n\nprose only, no numbered items\n\n## Next\n", encoding="utf-8")
                self.assertIn("empty", seg(p))

        def test_stops_at_then_line(self):
            # Items after a `# then:` line are NOT part of the queue.
            self.assertEqual(
                len(top("## Up next\n1) a\n2) b\n# then: 3) not counted\n4) also not\n")),
                2,
            )

        def test_truncates_near_120(self):
            long_items = "## Up next\n" + "".join(
                f"{i}) {'x' * 80}\n" for i in range(1, 4)
            )
            out = seg_from_text(long_items)
            self.assertLessEqual(len(out), 120)
            self.assertTrue(out.endswith("..."))

    def seg_from_text(text: str) -> str:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "P-TODO.md"
            p.write_text(text, encoding="utf-8")
            return seg(p)

    res = unittest.TextTestRunner(verbosity=1).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
