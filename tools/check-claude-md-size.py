#!/usr/bin/env python3
"""Delta gate D10: CLAUDE.md size ratchet (roadmap C phase 2, #1250).

`.claude/CLAUDE.md` is loaded EVERY turn, so its length is a per-turn token +
performance tax. Phase 1 (3.139.1) cut it from 1971 to 1506 lines by relocating
the PR-lifecycle prose to `.claude/playbooks/pr-lifecycle.md`. This gate LOCKS IN that
gain and prevents regrowth: it FAILS when CLAUDE.md exceeds a hand-maintained
ceiling constant.

The ceiling is a DOWNWARD RATCHET BY DEFAULT: the maintainer lowers it as CLAUDE.md
shrinks, and raises it only by explicit authorization for an intentional canonical
addition (as for the #1482 Five Rules of AIQT). Every
future relocation PR that shrinks CLAUDE.md also lowers CEILING in the same PR,
marching toward the ~800-900 goal and making each gain permanent. The gate never
fails on a decrease; it fails on any increase past the constant, which forces new
content to relocate to references/ rather than swell the every-turn load.

FAIL (not WARN) is deliberate: a size WARN is the advisory shape that gets skimmed
past, and the whole purpose is to FORCE relocation instead of regrowth. Blocking a
large addition until it is trimmed or relocated is exactly the desired behaviour.

Reads the working-tree file by explicit path (the `.claude/` exempt-dir walk does
not apply to an explicit-path read), so like D8 it needs no merge base.

The startup census also enforces Unicode characters, independently of line count.
It includes unscoped non-Markdown provenance and reports all CLAUDE files separately.

PROXY NOTE (dual-family verify, #1250): LINE COUNT remains a proxy for
the every-turn TOKEN load. Content packed into fewer, longer lines could evade the
ratchet while preserving token load; in practice added prose adds lines, so the
proxy tracks the load well enough. The ceiling itself is a CONVENTION the maintainer
maintains (lowering it as CLAUDE.md shrinks): the gate enforces the current ceiling,
and a change that RAISES the constant is a visible, reviewed diff, not a gate-enforced
invariant.

Exit: 0 = at or under ceiling; 1 = over ceiling; 2 = file missing / error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO_ROOT / ".claude" / "CLAUDE.md"

# Downward ratchet BY DEFAULT. LOWER this as CLAUDE.md shrinks; raise it ONLY by explicit
# maintainer authorization for an intentional canonical addition (see the #1482 note below). Current
# size at #1250 adoption: 1506 lines (CEILING then 1550). Roadmap C parts 2-4
# (#1278-1284) + the TODO-split #1301 brought CLAUDE.md to 918, but the ceiling
# was left at its adoption value (~630 lines of slack, so the gains were NOT
# locked in); #1302 lowers it to 945 (~3% headroom over 918) to ratchet the gain
# in, per the downward-ratchet discipline the maintainer set.
# #1482 raises 945 -> 962 for the maintainer-directed verbatim authoring of the
# canonical Five Rules of AIQT into the PRIMORDIAL RULE section (2026-08-11); a deliberate
# one-time upward bump for a locked canonical addition, not drift. The downward-ratchet
# convention resumes from here.
# #1775 raises 962 -> 1023 for the maintainer-authorized (AskUser, 2026-08-28) adoption of the
# no-manufactured-winddown interim rule (fleet share); an intentional canonical
# behavioural addition, reconciles when the guardrails/AIQT pack ships.
# #2365 relocates the block-on-open-findings mechanics to references/hook-open-findings-guard.md
# (batch-3 CLAUDE.md-D10 decision) and adds the guard's mis-filed second condition; net ratchet
# 1023 -> 1022. Downward-ratchet convention resumes.
# 3b177-c relocates the addyosmani overlay from .claude/rules/external/ to five
# .claude/skills/addyosmani-<name>/ skill directories and condenses the external-overlay
# paragraph to ten lines; net ratchet 1022 -> 1021. Downward-ratchet convention resumes.
# 3b177-d lowers 1021 -> 781 (skills/playbook relocation + SUPERSEDED deletion); downward ratchet resumes.
# 3b177-e lowers 781 -> 468 and the startup character ceiling 288490 -> 245289 (set from the draft's
# 458 lines + 10 and 244289 + 1000; restored clauses since then still fit); downward ratchet continues.
CEILING = 468
STARTUP_CHARACTER_CEILING = 245289  # 3b177-e; final backlog goal remains 150000



# Accepted frontmatter is deliberately a small, explicit YAML subset. Unknown
# keys or syntax fail closed: they cannot make a large rule disappear from D10.
SCALAR_METADATA = {"corpus-id", "origin", "family", "facet", "slug"}
LIST_METADATA = {"secondary"} | {
    f"map-{framework}-{strength}"
    for framework in (
        "atlas", "csa-aicm", "csa-ccm", "cwe", "iso-23894", "iso-42001",
        "nist-80053", "nist-airmf", "nist-ssdf", "owasp-api", "owasp-asi",
        "owasp-asvs", "owasp-cheatsheet", "owasp-llm", "owasp-mcp",
        "owasp-proactive", "owasp-web",
    )
    for strength in ("tight", "broad")
}


def string_scalar(value: str, *, path: bool = False) -> str:
    """Read an explicit string or a conservative, unambiguous plain scalar."""
    if value.startswith('"'):
        parsed = json.loads(value)
    elif value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise ValueError("invalid quoted string")
        parsed = value[1:-1].replace("''", "'")
    else:
        pattern = r"[A-Za-z_./][A-Za-z0-9_./*?-]*" if path else r"[A-Za-z0-9_][A-Za-z0-9_./&() -]*"
        if (not re.fullmatch(pattern, value)
                or value.lower() in {"true", "false", "null", "yes", "no", "on", "off", ".nan", ".inf"}
                or (path and re.fullmatch(r"[+-]?[0-9.]+", value))):
            raise ValueError("unsupported or non-string scalar")
        parsed = value
    if not isinstance(parsed, str) or not parsed.strip():
        raise ValueError("empty or non-string scalar")
    return parsed


def scoped(text: str) -> bool:
    """Accept only recognized scope metadata; reject everything ambiguous."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unterminated frontmatter") from exc
    keys = set()
    paths = None
    block_paths = False
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            m = re.fullmatch(r"  - (.+)", line)
            if not block_paths or not m:
                raise ValueError("unsupported frontmatter continuation")
            paths.append(string_scalar(m[1], path=True))
            continue
        m = re.fullmatch(r"([\w-]+):(?: +(.*))?", line)
        if not m or m[1] in keys:
            raise ValueError("invalid or duplicate frontmatter key")
        key, value = m[1], m[2] or ""
        keys.add(key)
        block_paths = key == "paths" and not value
        if key == "paths":
            paths = json.loads(value) if value else []
            if not isinstance(paths, list) or any(not isinstance(x, str) or not x.strip() for x in paths):
                raise ValueError("paths must be a string list")
        elif key in SCALAR_METADATA:
            string_scalar(value)
        elif key in LIST_METADATA:
            if not value.startswith("[") or not value.endswith("]"):
                raise ValueError("metadata must be a flat flow list")
            if value != "[]":
                for item in value[1:-1].split(","):
                    string_scalar(item.strip())
        elif key == "apex" and value in {"true", "false"}:
            pass
        elif key == "tier" and value in {"10", "20", "30", "40"}:
            pass
        else:
            raise ValueError("unrecognized frontmatter metadata: " + key)
    if paths == []:
        raise ValueError("empty paths is ambiguous")
    return paths is not None


def census(root: Path) -> dict:
    paths = [root / ".claude/CLAUDE.md"]
    rule_dir = root / ".claude/rules"
    if not rule_dir.is_dir():
        raise ValueError("missing rules directory")
    def unreadable(exc):
        raise exc
    for directory, dirs, files in os.walk(rule_dir, onerror=unreadable):
        for name in sorted(dirs + files):
            p = Path(directory) / name
            p.stat()  # do not let a disappearing or inaccessible entry silently vanish
            if p.is_symlink():
                raise ValueError(f"symlink in rule tree: {p}")
            if name in files:
                try:
                    unscoped = not scoped(p.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, ValueError) as exc:
                    exc.add_note(p.relative_to(root).as_posix())
                    raise
                if unscoped:
                    paths.append(p)
    def count(selected):
        data = [p.read_bytes() for p in selected]
        return dict(files=len(data), bytes=sum(map(len, data)),
                    characters=sum(len(b.decode("utf-8")) for b in data))
    tracked = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0")
    claudes = [root / p for p in tracked if p and Path(p).name == "CLAUDE.md"]
    return dict(startup=count(paths), all_claude=count(claudes),
                startup_plus_other_claude=count(paths + [p for p in claudes if p not in paths]),
                startup_paths=[p.relative_to(root).as_posix() for p in paths])


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
            f"raise CEILING to force a pass (it ratchets DOWN by default; a raise needs "
            f"explicit maintainer authorization for an intentional canonical addition).",
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
        totals = census(REPO_ROOT)
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: D10 census failed: {exc} {getattr(exc, '__notes__', [])}", file=sys.stderr)
        return 2
    code, msg = evaluate(count, CEILING)
    print(msg, file=sys.stderr if code else sys.stdout)
    print(json.dumps(totals, sort_keys=True))
    if totals["startup"]["characters"] > STARTUP_CHARACTER_CEILING:
        print(f"FAIL: startup character ceiling {STARTUP_CHARACTER_CEILING} exceeded")
        code = 1
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
