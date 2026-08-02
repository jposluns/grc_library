#!/usr/bin/env python3
"""Gate: no Unicode em/en dashes on the OPERATIONAL surfaces lint-language.py does not scan.

`lint-language.py` enforces the no-em/en-dash house style on the CORPUS (`.md` domain docs) and
on generator-source emitted prose, but it does NOT scan the project's operational surfaces:
`tools/*.py` and `tools/*.sh` (tool comments and docstrings), `.claude/` (CLAUDE.md, commands, hooks, the loaded
rule copies), and `references/` (the activity playbooks). PR #1314 swept those surfaces clean of
59 dash code points across 48 lines; this gate prevents re-drift (decision-2, the widen-the-gate
half; the sweep was the other half).

Scope: `tools/*.py` and `tools/*.sh`, everything under `.claude/`, everything under `references/`.

Exemptions (each principled, not a drive-by allow-list):
  - `.claude/rules/external/` : the THIRD-PARTY overlay (addyosmani / kariedo / tikitribe, each
    under its own MIT licence and PROVENANCE.md). It is refreshed FROM SOURCE, never hand-edited to
    conform to this project's house style, so its em-dashes are legitimate external content.
  - A glyph inside a markdown INLINE-CODE backtick span (`` `X` ``) or a fenced code block: the
    DELIBERATE illustration / functional form. This is exactly how the language-convention section
    of `.claude/CLAUDE.md` DEFINES the rule (it quotes the forbidden glyphs in backticks), and how a
    code example legitimately shows a dash. A dash used AS a dash in prose (outside code) is what
    re-drift looks like, and that is what this gate catches.
  - The standard exempt dirs (`.git`, `__pycache__`) and non-text artefacts.

The FUNCTIONAL dash literals in the linters themselves (regex patterns, sentinels) were converted to
Unicode escapes by #1314, so they are not literal glyphs and never match here.
"""
import re
import sys
from pathlib import Path

from lint_common import CODE_SPAN_RE, REPO_ROOT

DASH = re.compile("[\u2014\u2013]")
# Inline-code span: a run of N backticks, shortest content, closing run of N backticks.
INLINE_CODE = CODE_SPAN_RE
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")

EXEMPT_DIR_PARTS = {".git", "__pycache__", "node_modules"}
# The third-party overlay, exempt as external-licensed content (see docstring).
EXTERNAL_OVERLAY = REPO_ROOT / ".claude" / "rules" / "external"
TEXT_SUFFIXES = {".py", ".md", ".sh", ".yml", ".yaml", ".json", ".txt", ".toml"}


def _targets():
    """The files in scope: tools/*.py, .claude/**, references/**."""
    out = []
    # tools/ operational SCRIPTS (.py and .sh) carry prose comments/docstrings; the tool config
    # data files (.json) are not prose and are not scanned here.
    for pat in ("*.py", "*.sh"):
        for f in sorted((REPO_ROOT / "tools").glob(pat)):
            out.append(f)
    for base in (".claude", "references"):
        root = REPO_ROOT / base
        if not root.is_dir():
            continue
        for f in sorted(root.rglob("*")):
            if not f.is_file():
                continue
            if any(part in EXEMPT_DIR_PARTS for part in f.parts):
                continue
            if EXTERNAL_OVERLAY in f.parents:
                continue
            if f.suffix.lower() not in TEXT_SUFFIXES:
                continue
            out.append(f)
    return out


def strip_code(line: str) -> str:
    """Blank out inline-code backtick spans so a glyph INSIDE one is not flagged (the illustration
    / code-example form)."""
    return INLINE_CODE.sub(lambda m: "`" + " " * len(m.group(2)) + "`", line)


def scan_text(text: str, is_md: bool):
    """Yield (lineno, stripped_line) for each line carrying a dash outside code. PURE.

    For markdown, inline-code backtick spans and fenced code blocks are exempt (a glyph there is an
    illustration or a code example). For non-markdown (a `.py` comment or docstring), there are no
    backtick code spans, so a literal glyph is prose and stays flagged; the functional dash literals
    are Unicode-escaped (per #1314) and so are not literal glyphs."""
    in_fence = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        if is_md and FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        probe = strip_code(raw) if is_md else raw
        if DASH.search(probe):
            yield lineno, raw.strip()


def scan_file(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return list(scan_text(text, path.suffix.lower() == ".md"))


def _self_test() -> int:
    checks = []
    def c(name, cond):
        checks.append((name, cond))
    c("md-prose-dash-flagged", list(scan_text("a \u2014 b\n", True)) == [(1, "a \u2014 b")])
    c("md-inline-code-exempt", list(scan_text("Em-dashes (`\u2014`) are forbidden.\n", True)) == [])
    c("md-en-dash-flagged", list(scan_text("range 1\u20132\n", True)) == [(1, "range 1\u20132")])
    c("md-fence-exempt", list(scan_text("```\nx \u2014 y\n```\n", True)) == [])
    c("md-clean", list(scan_text("no dashes here, just commas.\n", True)) == [])
    c("py-comment-dash-flagged", list(scan_text("# a \u2014 b\n", False)) == [(1, "# a \u2014 b")])
    c("py-escaped-literal-clean", list(scan_text('P = "[\\\\u2014\\\\u2013]"\n', False)) == [])
    c("py-inline-code-not-stripped", len(list(scan_text("x = `\u2014`\n", False))) == 1)
    # _targets() scope (the logic that hid the tools/*.sh gap from unit tests; dual-family finding):
    # tools/ scripts .py AND .sh are in scope; the third-party overlay is excluded.
    tgt = _targets()
    c("targets-includes-sh", any(t.name == "pre-push-guard.sh" for t in tgt))
    c("targets-includes-py", any(t.name == "lint-ungated-dashes.py" for t in tgt))
    c("targets-excludes-external", not any("rules" in t.parts and "external" in t.parts for t in tgt))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"lint-ungated-dashes self-test: FAIL {bad}")
        return 1
    print(f"lint-ungated-dashes self-test: OK ({len(checks)} checks)")
    return 0


def main(argv) -> int:
    if "--self-test" in argv:
        return _self_test()
    findings = []
    for path in _targets():
        for lineno, line in scan_file(path):
            findings.append((path.relative_to(REPO_ROOT), lineno, line))
    if findings:
        print(f"FAIL: {len(findings)} Unicode em/en dash(es) on operational surfaces "
              f"(tools/*.py, tools/*.sh, .claude/, references/) that lint-language.py does not scan. Replace with "
              f"a comma, colon, or parentheses; a glyph that must appear (an illustration, a code "
              f"example) belongs inside a backtick code span; the third-party overlay under "
              f".claude/rules/external/ is exempt.")
        for rel, lineno, line in findings:
            print(f"  {rel}:{lineno}: {line[:110]}")
        return 1
    print("OK: no Unicode em/en dashes on the operational surfaces (tools/*.py, tools/*.sh, .claude/, references/); "
          "the third-party .claude/rules/external/ overlay and backtick-quoted glyphs are exempt.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
