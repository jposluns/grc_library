#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse a PR-writing gh command carrying Claude/Anthropic attribution.

Maintainer directive (2026-08-17, re-confirmed 2026-09-24): NO Claude/Anthropic attribution on
any commit, push, or PR; author identity is the maintainer only. Commits are protected by the
local commit-msg strip hook, but PR bodies were not: every PR body from #1622 to #2533 shipped
the harness-suggested "Generated with [Claude Code](...)" line (plus Co-Authored-By trailers and
bare claude.ai/code session links) because each session's harness reminder asks for it and no
guard refused it. This hook is the mechanical half of the fix; the CLAUDE.md directive is the
prose half. The harness's own attribution reminder defers to project instructions, so this
guard enforces a directive the harness explicitly permits to win.

WHAT IT BLOCKS: a Bash command that (a) invokes, at command position, a PR-WRITING gh
subcommand (`gh pr create|edit|comment|review|merge|close`), or a `gh api` call that
names a pulls/issues endpoint with a write indicator (-X/--method POST|PATCH|PUT, or a
field/input flag), AND (b) carries an attribution pattern in the command text (heredoc and
quoted bodies included; they are exactly the data to scan, so no heredoc stripping) or in a
local file passed via --body-file/--input/-F. The patterns are strict attribution shapes
(a Co-Authored-By trailer naming Claude/Anthropic, "Generated with ... Claude", claude.ai/code
and claude.com/claude-code links, noreply@anthropic.com); ordinary prose mentioning the Claude
model family ("claude SHIP", "CLAUDE.md", "the Claude-family verifier") passes.

GUARD-INPUT RESIDUE, stated at the point of use: this reads the command STRING plus any local
body FILE it names. A body read from STDIN (`--body-file -` or `-F -`) is always REFUSED, because
a piped body is invisible to this guard and ignorance must refuse rather than permit (pass a
heredoc through `--body "$(cat <<'EOF' ... EOF)"` instead, whose text is scanned). An unreadable
body-file path is skipped: in the common case gh cannot read it either, but a file materialized
mid-command from a non-literal source is a stated miss. Also not seen: a
gh api GraphQL mutation that never says pulls/issues; gh global flags between `gh` and the
subcommand (`gh -R o/r pr create`); or a PR written by any route other than a gh command in a
Bash tool call. The attribution scan is whole-command and quote-blind by design, so a command
that both writes a PR and QUOTES an attribution pattern in an unrelated argument blocks (split
the command, or use the escape). A relative body-file path is resolved against the payload's
cwd; a later `cd` inside the same command is not followed.

ESCAPE: lead the WHOLE command with GRC_ALLOW_PR_ATTRIBUTION=1 (a real leading assignment,
read quote-aware; a mention in a quoted argument or a heredoc line does not count). The escape
is an audited speed bump, not a security boundary, and it does not bypass the CI check. The standing directive is absolute, so using the escape requires express maintainer
authorization, recorded where the exception is made.

BEST-EFFORT EARLY WARNING, NOT THE AUTHORITY (maintainer ruling 2026-09-24): recognizing every
shell shape that can write a PR body is an open-ended class, so this hook catches the common
shapes only. The authoritative check is `tools/check-pr-attribution.py`, run by
`.github/workflows/pr-attribution.yml` on every PR open, edit, and push; it reads the stored PR
title and body from the event payload and fails the PR, so a shape this hook misses still fails
CI (unless the same PR also weakens the checker, a change visible in its diff under review). Do not grow this hook to chase further shell shapes; fix the CI check instead.

Fails OPEN on a malformed payload or an internal error.
Self-test: `python3 .claude/hooks/block-claude-attribution.py --self-test`.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys

ESCAPE = "GRC_ALLOW_PR_ATTRIBUTION"

# Strict attribution shapes. Each is an attribution LINE pattern, not a model-family mention:
# "claude SHIP", "CLAUDE.md", "claude-attribution" must all pass.
# The patterns run over THREE views of the text (the text is normalized, never the patterns widened
# per delimiter): the raw text; Markdown formatting characters replaced by spaces (so '[Claude][1]'
# and 'Claude_Code' keep their word boundaries); and the same characters deleted (so in-word
# formatting such as 'C**laud**e' or a bold '**Co-Authored-By**:' label rejoins). Newlines survive
# every view, so a match is reported as its line of the ORIGINAL text. Threat model, stated: this
# catches accidental or harness-added attribution in its ordinary Markdown shapes; deliberate
# obfuscation is a visible integrity breach in the PR text, not a parsing target.
MARKDOWN_FORMATTING = str.maketrans("*_`[]", "     ")
MARKDOWN_DELETE = str.maketrans("", "", "*_`[]")
# Emphasis and code markers deleted (they split a word), underscores and brackets spaced (they
# separate words): 'C**laud**e_Code' reads 'Claude Code'.
MARKDOWN_MIXED = str.maketrans({"*": None, "`": None, "_": " ", "[": " ", "]": " "})
# Link syntax reduced to its visible text first, so a destination or reference label never sits
# between (or glues onto) the words: '[Generated with](url) Claude' and '[CLAUDE.md][1]'.
_INLINE_LINK = re.compile(r"\]\([^)\n]*\)")
_REF_LINK = re.compile(r"\]\[[^\]\n]*\]")


def text_views(text: str) -> tuple[str, ...]:
    plain = _REF_LINK.sub("]", _INLINE_LINK.sub("]", text))
    views = [text]
    for base in (text, plain):
        views += [base.translate(MARKDOWN_FORMATTING), base.translate(MARKDOWN_DELETE),
                  base.translate(MARKDOWN_MIXED)]
    return tuple(views)

ATTRIBUTION = (
    ("a Co-Authored-By trailer naming Claude/Anthropic",
     re.compile(r"(?i)co-authored-by[ \t]*:[^\n]*\b(?:claude|anthropic)\b")),
    ("a 'Generated with/by ... Claude' attribution line",
     re.compile(r"(?i)\bgenerated\s+(?:with|by|using|via)\s+(?:(?:the\s+)?(?:help|assistance|aid)\s+of\s+)?"
                r"(?:the\s+)?(?:claude|anthropic)(?![a-z0-9]|\.md)")),
    ("a claude.ai/code link",
     re.compile(r"(?i)\bclaude\.ai/code")),
    ("a claude.com/claude-code link",
     re.compile(r"(?i)\bclaude\.com/claude-code")),
    ("the noreply@anthropic.com trailer address",
     re.compile(r"(?i)\bnoreply@anthropic\.com")),
)

# The gh invocation must sit at COMMAND POSITION in its segment (same anchor family as
# block-verification-pipes): a commit message or echo that merely MENTIONS "gh pr create"
# mid-string does not trigger. Quote-blind on newlines by design (a newline inside a quoted
# body can fabricate a command position; strict-safe direction).
_CMD_POS = r"(?:^|[;&|\n(]\s*|&&\s*|\|\|\s*|\{\s+|\$\(\s*|`\s*)"
_ASSIGN = r"(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
_RUNNER = r"(?:sudo\s+|env\s+|command\s+|nohup\s+|timeout\s+[\w.]+\s+)?"
WRITE_CMD = re.compile(
    _CMD_POS + _ASSIGN + _RUNNER
    + r"gh\s+pr\s+(?:create|edit|comment|review|merge|close)\b",
    re.MULTILINE)
API_CMD = re.compile(_CMD_POS + _ASSIGN + _RUNNER + r"gh\s+api\s", re.MULTILINE)
API_TARGET = re.compile(r"\b(?:pulls|issues)\b")
API_WRITE = re.compile(
    r"(?:^|\s)(?:-X|--method)[= ]\s*(?:POST|PATCH|PUT)\b"
    r"|(?:^|\s)(?:-f|-F|--field|--raw-field|--input)\b")


def _api_segment(command: str, start: int) -> str:
    """The gh api invocation's own segment: from its match to the next pipe, list operator, or
    newline, so a flag belonging to a later command (`| grep -F x`) is not read as a gh api
    field flag."""
    return re.split(r"\|\||&&|[|;&\n]", command[start:], maxsplit=1)[0]


def writes_pr_surface(command: str) -> bool:
    if WRITE_CMD.search(command):
        return True
    for m in API_CMD.finditer(command):
        seg = _api_segment(command, m.end() - 1)
        if API_TARGET.search(seg) and API_WRITE.search(seg):
            return True
    return False


def body_file_paths(command: str) -> list[str]:
    """Local files whose content ships as the PR body: --body-file/--input X (or =X), and a
    gh-pr -F X (a gh api -F is a key=value field, excluded by the '=' test)."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []
    paths = []
    for i, tok in enumerate(tokens):
        if tok in ("--body-file", "--input") and i + 1 < len(tokens):
            paths.append(tokens[i + 1])
        elif tok.startswith("--body-file=") or tok.startswith("--input="):
            paths.append(tok.split("=", 1)[1])
        elif tok == "-F" and i + 1 < len(tokens) and "=" not in tokens[i + 1]:
            paths.append(tokens[i + 1])
        elif tok.startswith("-F") and len(tok) > 2 and "=" not in tok:
            paths.append(tok[2:])
        elif tok in ("-F", "--field") and i + 1 < len(tokens) and "=@" in tokens[i + 1]:
            paths.append(tokens[i + 1].split("=@", 1)[1])  # gh api key=@file reads the file
        elif (tok.startswith("--field=") or (tok.startswith("-F") and len(tok) > 2)) and "=@" in tok:
            paths.append(tok.split("=@", 1)[1])
    return [p for p in paths if p]


def _read_body_file(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(262144)
    except OSError:
        return None


def _snippet(s: str) -> str:
    """The matched attribution text, made safe for the refusal contract: no em/en dashes and
    no contract-marker substrings, truncated."""
    s = s.replace(chr(0x2014), "-").replace(chr(0x2013), "-")
    for marker in ("BLOCKED (", "WHY:", "CONSIDER INSTEAD:"):
        s = s.replace(marker, "")
    s = s.strip()
    return s[:117] + "..." if len(s) > 120 else s


def find_attribution(text: str):
    raw_lines = text.split("\n")
    for view in text_views(text):
        for label, rx in ATTRIBUTION:
            m = rx.search(view)
            if m:
                return label, _snippet(raw_lines[view.count("\n", 0, m.start())])
    return None


def decide(command: str, read_file=None, cwd: str | None = None) -> str | None:
    """Pure decision: the full refusal message, or None to allow. The observer half (payload
    parse, env escape, file reads) stays in main/_read_body_file so both halves are testable."""
    if not isinstance(command, str) or not command:
        return None
    if not writes_pr_surface(command):
        return None
    reader = read_file or _read_body_file
    texts = [("the command text", command)]
    paths = body_file_paths(command)
    if "-" in paths:
        return (
            "BLOCKED (claude-attribution): this gh command writes a PR surface with its body read "
            "from stdin, which this guard cannot inspect.\n"
            "WHY: the maintainer directive (2026-08-17) forbids Claude/Anthropic attribution on any "
            "PR, and a piped body is invisible here, so it is refused rather than passed unchecked.\n"
            "CONSIDER INSTEAD: rewrite the command to pass the body with --body-file <path> (a file "
            "this guard can read) or an inline --body, then resubmit.")
    for path in paths:
        if path == "-":
            continue
        if cwd and not os.path.isabs(path):
            path = os.path.join(cwd, path)
        content = reader(path)
        if content is not None:
            texts.append(("the body file " + path, content))
    for origin, text in texts:
        hit = find_attribution(text)
        if hit:
            label, snippet = hit
            return (
                "BLOCKED (claude-attribution): this gh command writes a PR/issue surface and "
                + origin + " carries " + label + ": `" + snippet + "`\n"
                "WHY: the maintainer directive (2026-08-17) forbids Claude/Anthropic "
                "attribution on any commit, push, or PR; author identity is the maintainer "
                "only, and the harness's per-session attribution reminder defers to this "
                "project instruction (PR bodies #1622 to #2533 shipped the line before this "
                "guard existed).\n"
                "CONSIDER INSTEAD: rewrite the title/body/comment without the attribution "
                "line (drop 'Generated with', 'Co-Authored-By', claude.ai/code, "
                "claude.com/claude-code, and noreply@anthropic.com lines), then resubmit; a "
                "maintainer-authorized exception leads the command with " + ESCAPE + "=1.")
    return None


ESCAPE_RE = re.compile(r"\A\s*(?:[A-Za-z_][A-Za-z0-9_]*=[^\s'\"\\]*\s+)*" + ESCAPE + r"=1(?:\s|\Z)")


def escaped(command: str) -> bool:
    """The escape must be a real LEADING assignment of the whole command, matched on the RAW
    text: an unquoted name at the start, optionally after other simple unquoted assignments. A
    quoted word (a command name, not an assignment), a mention in an argument, or a heredoc line
    never counts; an earlier assignment whose value is quoted also disqualifies (refuse on doubt)."""
    return bool(ESCAPE_RE.match(command))


def main() -> int:
    try:
        if os.environ.get(ESCAPE) == "1":
            return 0
        payload = json.load(sys.stdin)
        if payload.get("tool_name") != "Bash":
            return 0
        command = payload.get("tool_input", {}).get("command", "") or ""
        if escaped(command):
            return 0
        cwd = payload.get("cwd")
        reason = decide(command, cwd=cwd if isinstance(cwd, str) else None)
        if reason:
            try:
                from _hook_state import record_block
                record_block(command, "claude-attribution")
            except Exception:
                pass
            print(reason, file=sys.stderr)
            return 2
    except Exception:
        return 0
    return 0


_GEN = "\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)"
_COA = "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
SELF_TEST = [
    # blocked: every PR-writing gh verb, every attribution shape
    ('gh pr create --title "t" --body "Change.\n\n' + _GEN + '"', True),
    ("gh pr create -t x -b '" + _COA + "'", True),
    ('gh pr edit 12 --body "Done. Generated with Claude Code"', True),
    ('gh pr comment 12 --body "see https://claude.ai/code/session_abc123"', True),
    ('gh pr review 12 --approve --body "' + _GEN + '"', True),
    ('gh pr merge 12 --squash --subject "x" --body "co-authored-by: Claude <noreply@anthropic.com>"', True),
    ('gh pr close 12 --comment "wontfix. ' + _GEN + '"', True),
    ('gh issue comment 7 --body "' + _COA + '"', False),  # scope: PR writes only
    ("printf 'x' | gh pr create --title t --body-file -", True),  # stdin body refused
    ("gh pr create --title t --body-file - <<'EOF'\nClean body.\nEOF", True),  # stdin always refused
    ("gh pr create --title t --body \"$(cat <<'EOF'\nBody.\n" + _GEN + "\nEOF\n)\"", True),
    ("gh api repos/o/r/pulls -f title=t -f body='Generated with Claude Code'", True),
    ("gh api -X PATCH repos/o/r/pulls/9 -f body='x " + _COA + "'", True),
    ("cd /x && gh pr create -b '" + _GEN + "'", True),
    ("GH_TOKEN=x gh pr create -b 'Generated with Claude Code'", True),
    # a body that carries attribution AND merely mentions the escape still blocks
    ("gh pr create -b 'lead with " + ESCAPE + "=1. " + _GEN + "'", True),
    # allowed: clean writes, reads, model-family prose, non-gh carriers, the real escape
    ('gh pr create --title "tooling: attribution guard" --body "Adds the claude-attribution hook."', False),
    ('gh pr comment 12 --body "QA verdicts: claude SHIP, codex SHIP, gemini SHIP"', False),
    ('gh pr create --body "Updates CLAUDE.md and the gate-count prose"', False),
    ("gh pr view 2533 --json body --jq .body | grep -n 'Generated with'", False),
    ("gh pr list --limit 5", False),
    ("gh api repos/o/r/pulls/2533 --jq .body | grep 'Generated with Claude'", False),
    ("git commit -m 'docs: strip Co-Authored-By: Claude trailers from gh pr create bodies'", False),
    ("echo 'gh pr create must never carry " + _COA + "'", False),
    ("gh pr merge 2534 --squash --admin", False),
    (ESCAPE + "=1 gh pr create -b '" + _GEN + "'", False),
    # 2026-09-24 cheap fixes (best-effort scope)
    ("printf x | gh pr create --title t --body-file - && echo '<<'", True),  # '<<' is not a heredoc
    ("gh pr create --title t --body-file - <<'EOF'\n" + ESCAPE + "=1\n" + _GEN + "\nEOF", True),
    ("gh pr create -b \"" + ESCAPE + "=1 " + _GEN + "\"", True),  # quoted mention, not an escape
    ("gh api repos/o/r/pulls/9 | grep -F 'Generated with Claude'", False),  # grep's -F
    ("gh api repos/o/r/pulls/9 --jq .body; grep -f pats x", False),
    ("cat body.md | gh pr create --title '<<EOF' --body-file -", True),  # quoted '<<EOF' is not a heredoc
    ("gh api repos/o/r/pulls/9 & grep -F 'Generated with Claude'", False),  # background '&'
    ("gh pr create -b 'Generated by Claude Code'", True),
    ("gh pr create -b 'Generated with CLAUDE.md as the fixture'", False),
    ("'" + ESCAPE + "=1'; gh pr create --body '" + _GEN + "'", True),  # quoted word is not an escape
    ("X=1 " + ESCAPE + "=1 gh pr create -b '" + _GEN + "'", False),
]


def self_test() -> int:
    bad = 0
    for command, should_block in SELF_TEST:
        got = decide(command) is not None and not escaped(command)
        if got != should_block:
            bad += 1
            print("FAIL want=" + ("BLOCK" if should_block else "allow") + " got="
                  + ("BLOCK" if got else "allow") + ": " + repr(command))
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write("Body.\n\n" + _GEN + "\n")
        dirty = fh.name
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write("A clean body about the claude-attribution guard.\n")
        clean = fh.name
    try:
        cases = [("gh pr create --title t --body-file " + dirty, True),
                 ("gh pr create --title t -F " + dirty, True),
                 ("gh pr create --title t --body-file " + clean, False),
                 ("gh pr create --title t --body-file /nonexistent/x.md", False),
                 ("gh pr create --title t -F" + dirty, True),
                 ("gh api repos/o/r/pulls -F body=@" + dirty, True),
                 ("gh api repos/o/r/pulls --field body=@" + dirty, True)]
        base, name = os.path.split(dirty)
        for command, should_block, cwd in [(c, b, None) for c, b in cases] + [
                ("gh pr create --title t --body-file " + name, True, base),
                ("gh pr create --title t --body-file " + name, False, "/nonexistent")]:
            got = decide(command, cwd=cwd) is not None
            if got != should_block:
                bad += 1
                print("FAIL (body-file) want=" + str(should_block) + ": " + repr(command))
    finally:
        for p in (dirty, clean):
            try:
                os.unlink(p)
            except OSError:
                pass
    total = len(SELF_TEST) + 9
    print(str(total - bad) + "/" + str(total) + " self-test cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
