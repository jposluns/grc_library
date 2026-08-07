#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse a stage-the-tree git command; require enumerated paths.

Shipped 2026-08-07 after ORCHESTRATOR-MISTAKES entry 43: a tree-sweep stage put a finished,
unrelated delta gate into a commit whose message described only a corpus-document edit, so the
commit said one thing and shipped another. The sweep forms stage the TREE rather than the CHANGE,
so the author's scope lives only in the commit message while the artefact inherits whatever the
tree happened to hold.

REBUILT the same day after a dual-family review of the first version found nine high-severity
bypasses. What that review established, and what this version does about it:

  * A tree-root pathspec is a sweep, not an enumeration. ``add -- .``, ``add :/``, ``add ./`` and
    a repo-root argument all stage everything while satisfying a naive "was a path given" test.
  * A sweep flag is only bounded when its pathspec is explicit AND is not a tree root, so a sweep
    flag now requires a ``--`` boundary with a real path after it.
  * Short flags bundle: ``-Av`` and ``-uf`` carry a sweep the first version did not see.
  * Any command word before ``git`` defeated detection: ``sudo git``, ``env git``, ``timeout 5
    git``, ``xargs git``. Wrappers are skipped now, and ``sh -c "..."`` is scanned inside.
  * The escape was an unanchored substring, so merely MENTIONING it disabled the guard. It must
    now be a real leading assignment.

GUARD-INPUT RESIDUE, stated at the point of use: this reads the command STRING. It establishes
that paths were enumerated; it does NOT establish that the enumerated set matches the scope the
commit message claims, and it cannot. Its value is forcing the set to be stated so a mismatch is
visible while it is authored. A DIRECTORY argument is treated as enumeration, which is a bounded
sweep rather than an unbounded one and is a deliberate, stated limit. Staging by any route other
than a git command in a Bash tool call is invisible to it.

Fails OPEN on a malformed payload or an internal error.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hookutil import WRAPPERS, strip_heredocs  # noqa: E402

SWEEP_LONG = {"-A", "--all", "-u", "--update", "--no-ignore-removal"}
TREE_ROOTS = {".", "./", ":/", ":", "*", ":/.", "..", "../"}
ESCAPE = "GRC_ALLOW_BULK_ADD"
_SEPARATORS = re.compile(r"&&|\|\||[;\n|&]|\$\(|\)|`")


def _tokenise(raw: str) -> list[str]:
    try:
        return shlex.split(raw)
    except ValueError:
        return []


def segments(command: str) -> list[list[str]]:
    """Every git invocation in the command, wrappers skipped, `sh -c` bodies scanned."""
    found = []
    for raw in _SEPARATORS.split(strip_heredocs(command)):
        raw = raw.strip()
        if not raw:
            continue
        tokens = _tokenise(raw)
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tok):
                i += 1
                continue
            base = os.path.basename(tok)
            if base in WRAPPERS:
                i += 1
                while i < len(tokens) and (tokens[i].startswith("-")
                                           or re.fullmatch(r"[\d.]+[smhd]?", tokens[i])):
                    i += 1
                continue
            if base in {"sh", "bash", "zsh", "dash"} and "-c" in tokens[i:]:
                j = tokens.index("-c", i)
                if j + 1 < len(tokens):
                    found.extend(segments(tokens[j + 1]))   # scan the inner program
                break
            if base == "git":
                found.append(tokens[i:])
            break
    return found


def body(tokens: list[str]) -> tuple[str | None, list[str]]:
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


def has_sweep_flag(args: list[str]) -> str | None:
    for a in args:
        if a in SWEEP_LONG:
            return a
        if a.startswith("-") and not a.startswith("--") and re.fullmatch(r"-[A-Za-z]+", a):
            for ch in a[1:]:
                if ch in "Au":
                    return a                                # bundled short flags
    return None


def violation(tokens: list[str]) -> str | None:
    sub, args = body(tokens)
    if sub == "add":
        after = args[args.index("--") + 1:] if "--" in args else []
        before = [a for a in (args[:args.index("--")] if "--" in args else args)
                  if not a.startswith("-")]
        paths = [p for p in (after + before)]
        real = [p for p in paths if p.rstrip("/") not in {r.rstrip("/") for r in TREE_ROOTS}]
        sweep = has_sweep_flag(args)
        if sweep and not (after and real):
            return ("`git add " + sweep + "` stages the TREE. Bound it explicitly: "
                    "`git add " + sweep + " -- <dir>/`, or name the files.")
        if not sweep and paths and not real:
            return ("`git add " + paths[0] + "` is a tree root, so it stages everything. "
                    "Name the files instead.")
        interactive = any(a in {"-p", "--patch", "-i", "--interactive", "-e", "--edit"}
                          for a in args)
        if not sweep and not paths and not interactive:
            # F-4: an interactive add presents each hunk for a decision, so the scope IS stated,
            # one hunk at a time. Blocking it would push the author toward the sweep instead.
            return "`git add` with no pathspec. Name the files."
    if sub == "commit":
        for a in args:
            if a == "--all" or (a.startswith("-") and not a.startswith("--")
                                and re.fullmatch(r"-[A-Za-z]+", a) and "a" in a[1:]):
                return ("`git commit " + a + "` commits every tracked modification, bypassing "
                        "staging. Stage the files you mean, then commit.")
    return None


def escaped(command: str) -> bool:
    """The escape must be a real leading assignment, not a mention anywhere in the text."""
    for raw in re.split(r"&&|\|\||[;\n]", strip_heredocs(command)):
        for tok in _tokenise(raw.strip()):
            if tok == ESCAPE + "=1":
                return True
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tok):
                break
    return False


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
        for tokens in segments(command):
            problem = violation(tokens)
            if problem:
                print("BLOCKED (bulk-stage guard): " + problem + "\n\n"
                      "  Why: entry 43 in ORCHESTRATOR-MISTAKES.md. A tree-sweep stage makes the\n"
                      "  commit message the only record of scope, and the message is the half that\n"
                      "  is never verified. Enumerate, or lead the command with "
                      + ESCAPE + "=1.", file=sys.stderr)
                return 2
    except Exception:
        return 0
    return 0


_G = "git"
_AND = "&& "
SELF_TEST = [
    (_G + " add -A", True), (_G + " add --all", True), (_G + " add .", True),
    (_G + " add -u", True), (_G + " add", True),
    (_G + " add -- .", True),            # H1: tree root after the boundary
    (_G + " add -A -- .", True),         # H1
    (_G + " add :/", True),              # H3: repo-root magic pathspec
    (_G + " add ./", True),              # H3
    (_G + " add -Av", True),             # H4: bundled short flags
    (_G + " add -uf", True),             # H4
    (_G + " add -A a.md", True),         # H2: a sweep flag needs an explicit -- boundary
    ("sudo " + _G + " add -A", True),    # H5: wrapper prefix
    ("env " + _G + " add -A", True),     # H5
    ("timeout 5 " + _G + " add -A", True),  # H5
    ("sh -c '" + _G + " add -A'", True),    # H6: inner program
    (_G + " add -A &", True),               # H6: backgrounded sweep
    ("echo hi " + _AND + _G + " add -A", True),
    (_G + " commit -am 'x'", True), (_G + " commit -a", True), (_G + " commit --all", True),
    (_G + " add a.md b.md", False),
    (_G + " -C /r add tools/x.py", False),
    (_G + " add -A -- executive/", False),
    (_G + " add -p", False),
    (_G + " commit -m 'a message that mentions " + ESCAPE + "=1 in passing'", False),
    (_G + " commit --amend --no-edit", False),
    (_G + " status --short", False),
    (ESCAPE + "=1 " + _G + " add -A", False),     # M2: a real leading assignment escapes
    ("echo '" + ESCAPE + "=1' " + _AND + _G + " add -A", True),   # M2: a mention does NOT
    ("cat > f <<'EOF'\n" + _G + " add -A\nEOF", False),           # inert heredoc: data
    ("bash <<'EOF'\n" + _G + " add -A\nEOF", True),               # H7: interpreter body is a program
]


def self_test() -> int:
    bad = 0
    for command, should_block in SELF_TEST:
        got = any(violation(t) for t in segments(command)) and not escaped(command)
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
