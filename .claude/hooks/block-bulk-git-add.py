#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse a stage-the-tree git command; require enumerated paths.

Shipped 2026-08-07 after ORCHESTRATOR-MISTAKES entry 43: a tree-sweep stage put a finished,
unrelated delta gate (six files) into a commit whose message described only a corpus-document
edit, so the commit said one thing and shipped another. The mechanism is that the sweep forms
stage the TREE rather than the CHANGE, so the author's scope lives only in the commit message
while the artefact inherits whatever the tree happened to hold. That is the intent-versus-
artefact gap the ``evidence-grounded-completion`` rule names, at the staging boundary, and it
defeats the split-when-in-doubt discipline silently: nothing about a bundled commit looks wrong.

What it does: reads the PreToolUse JSON payload on stdin and BLOCKS (exit 2) any git command
that stages or commits by tree-sweep rather than by enumeration: the add sweep flags
(-A / --all / -u / --update) or a bare "." with no limiting pathspec, and the commit-all forms
(-a / -am / --all), which bypass staging entirely.

ALLOWED, because each states its scope: an add with enumerated paths, a sweep bounded by a
pathspec after "--", an interactive patch add, and every non-staging git verb.

Escape hatch, deliberately visible: set GRC_ALLOW_BULK_ADD=1 in the command's environment. A
guard with no escape gets removed; a guard whose escape must be typed leaves a record of the
choice in the command string itself.

GUARD-INPUT RESIDUE (stated at the point of use, per validate-inference-before-action's
guard-input discipline): this hook reads the command STRING. It therefore establishes that the
author enumerated paths; it does NOT and cannot establish that the enumerated set matches the
scope the commit message claims. Its whole value is forcing the set to be stated, so a mismatch
is visible while it is authored rather than after it merges. It is blind to staging done by any
route other than a git command in a Bash tool call.

It also strips heredoc bodies before parsing, because a heredoc body is DATA: text that quotes
a forbidden command (a docstring, a test fixture, a log entry) must not be read as invoking one.
Omitting that strip is a live defect in a sibling hook and cost a whole command on the day this
one was written.

Fails OPEN on a malformed payload or an internal error: a guard that blocks all work when it
itself breaks is a guard that gets switched off.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys

BULK_ADD_FLAGS = {"-A", "--all", "-u", "--update", "--no-ignore-removal"}
_SEPARATORS = re.compile(r"&&|\|\||[;\n|]")
_HEREDOC_START = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def strip_heredocs(command: str) -> str:
    """Drop heredoc BODIES, keeping the command lines that introduce them."""
    out, lines, i = [], command.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        starts = _HEREDOC_START.findall(line)
        i += 1
        for _quote, tag in starts:
            while i < len(lines) and lines[i].strip() != tag:
                i += 1
            i += 1  # consume the terminator
    return "\n".join(out)


def segments(command: str) -> list[list[str]]:
    """Tokenised segments whose command word is git."""
    found = []
    for raw in _SEPARATORS.split(strip_heredocs(command)):
        raw = raw.strip()
        if not raw:
            continue
        try:
            tokens = shlex.split(raw)
        except ValueError:
            continue  # unbalanced quotes: not parseable, so not judgeable
        while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
            tokens.pop(0)
        if tokens and os.path.basename(tokens[0]) == "git":
            found.append(tokens)
    return found


def git_body(tokens: list[str]) -> tuple[str | None, list[str]]:
    """Return (subcommand, args-after-it), skipping git's own pre-verb options."""
    i = 1
    while i < len(tokens):
        tok = tokens[i]
        if tok in {"-C", "--git-dir", "--work-tree", "--namespace", "-c"}:
            i += 2
            continue
        if tok.startswith("-"):
            i += 1
            continue
        return tok, tokens[i + 1:]
    return None, []


def violation(tokens: list[str]) -> str | None:
    sub, args = git_body(tokens)
    if sub == "add":
        ddash = args.index("--") if "--" in args else None
        bounded = ddash is not None and len(args) > ddash + 1
        named = [a for a in args if not a.startswith("-") and a not in {"--", "."}]
        sweep = [a for a in args if a in BULK_ADD_FLAGS] + (["."] if "." in args else [])
        if sweep and not (bounded or named):
            return (
                "an add sweep (" + sweep[0] + ") stages the TREE, not the change. Name the "
                "files, or bound the sweep with a pathspec after --."
            )
    if sub == "commit":
        for a in args:
            if a == "--all" or (a.startswith("-") and not a.startswith("--") and "a" in a[1:]):
                return (
                    "commit " + a + " commits every tracked modification, bypassing staging. "
                    "Stage the files you mean, then commit."
                )
    return None


def main() -> int:
    if os.environ.get("GRC_ALLOW_BULK_ADD") == "1":
        return 0
    try:
        payload = json.load(sys.stdin)
        if payload.get("tool_name") != "Bash":
            return 0
        command = payload.get("tool_input", {}).get("command", "") or ""
        if "GRC_ALLOW_BULK_ADD=1" in command:
            return 0
        for tokens in segments(command):
            problem = violation(tokens)
            if problem:
                print(
                    "BLOCKED (bulk-stage guard): " + problem + "\n\n"
                    "  Why: entry 43 in ORCHESTRATOR-MISTAKES.md. A tree-sweep stage makes the\n"
                    "  commit message the only record of scope, and the message is the half that\n"
                    "  is never verified. Enumerate the paths, or set GRC_ALLOW_BULK_ADD=1.",
                    file=sys.stderr,
                )
                return 2
    except Exception:
        return 0  # fail open, deliberately
    return 0


_G = "git"
_AND = "&& "
SELF_TEST = [
    (_G + " -C /r add -A", True),
    (_G + " add --all", True),
    (_G + " add .", True),
    (_G + " add -u", True),
    (_G + " commit -am 'x'", True),
    (_G + " commit -a", True),
    ("cd /r " + _AND + _G + " add -A", True),
    ("echo hi " + _AND + _G + " -C /r add -A " + _AND + "echo done", True),
    (_G + " add a.md b.md", False),
    (_G + " -C /r add tools/x.py", False),
    (_G + " add -A -- executive/", False),
    (_G + " add -p", False),
    (_G + " commit -m 'message mentioning an add sweep'", False),
    (_G + " commit --amend --no-edit", False),
    (_G + " commit -m x --author='A B'", False),
    (_G + " status --short", False),
    (_G + " log --oneline -5", False),
    ("cat > f <<'EOF'\n" + _G + " add -A\nEOF", False),   # heredoc body is data
    ("python3 t.py --note 'an add sweep'", False),
    (_G + " stash push -- a.md", False),
]


def self_test() -> int:
    bad = 0
    for command, should_block in SELF_TEST:
        got = any(violation(t) for t in segments(command))
        if got != should_block:
            bad += 1
            print("FAIL want=" + ("BLOCK" if should_block else "allow") + " got="
                  + ("BLOCK" if got else "allow") + ": " + repr(command))
    print(str(len(SELF_TEST) - bad) + "/" + str(len(SELF_TEST)) + " self-test cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
