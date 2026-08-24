"""Shared helpers for the PreToolUse Bash hooks. Not a hook itself.

Extracted 2026-08-07 after a dual-family review of PR #1441 found the same heredoc-stripping code
duplicated byte-for-byte in two hooks and wrong in three ways in both copies. One implementation,
one set of fixtures.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
import shlex

# A heredoc INTRODUCER. Three angle brackets is a herestring, not a heredoc, and `a << b` is a
# shift: both are excluded by rejecting a third bracket and requiring a shell-word tag.
_HEREDOC = re.compile(r"<<-?(?!<)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")

# Command words whose heredoc BODY is a program rather than data. Stripping one of those hides
# real commands: an interpreter or a remote shell EXECUTES what sits between the markers, and the
# guards demonstrably caught mutating version-control commands inside exactly that shape before
# the strip was introduced.
SHELL_INTERPRETERS = {
    "bash", "sh", "zsh", "dash", "ksh", "csh", "tcsh", "fish",
    "ssh", "sudo", "doas", "su", "docker", "podman", "kubectl", "nsenter", "chroot",
    "env", "nohup", "timeout", "xargs", "eval", "script",
}

# A body handed to a NON-shell interpreter is a program in another language, so scanning it for
# shell commands is a category error: the text of a shell command inside a python string is not a
# shell command. Those bodies are stripped. RESIDUE, stated because it is a real gap: such a body
# can still invoke a subprocess, and this observer cannot see that. It is not the observable this
# guard family reads. Discovered as a FALSE CATCH the same day the interpreter rule was added,
# when a python heredoc containing a guard's own error strings tripped the guard.
NON_SHELL_INTERPRETERS = {"python", "python2", "python3", "perl", "ruby", "node", "php"}

INTERPRETERS = SHELL_INTERPRETERS | NON_SHELL_INTERPRETERS

# Wrapper words that PRECEDE the real command word and must be skipped to find it.
WRAPPERS = {"sudo", "doas", "env", "nohup", "command", "exec", "time", "timeout", "stdbuf",
            "nice", "ionice", "setsid", "script", "xargs"}


def command_word(line: str) -> str:
    """The effective command word of a line, skipping assignments, wrappers and their arguments."""
    try:
        tokens = shlex.split(line, comments=False)
    except ValueError:
        tokens = line.split()
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
        return base
    return ""


def strip_heredocs(command: str) -> str:
    """Remove heredoc BODIES that are DATA; keep bodies that are PROGRAMS.

    Three properties the first version got wrong, each proved by a verifier probe:

    1. A body introduced by an interpreter or a remote shell IS executed. Stripping it hid real
       mutating commands from the guards, a live weakening rather than a theoretical one. Those
       bodies are KEPT.
    2. An UNQUOTED tag expands command substitutions in the body, so a substitution written there
       runs. Only a quoted tag is inert. Unquoted bodies are KEPT.
    3. A false introducer with no matching terminator used to swallow the whole remainder of the
       command, a universal bypass for every guard downstream. With no terminator, NOTHING is
       removed.
    """
    lines = command.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        cw = command_word(line)
        for quote, tag in _HEREDOC.findall(line):
            end = None
            for j in range(i, len(lines)):
                if lines[j].strip() == tag:
                    end = j
                    break
            if end is None:
                continue                                    # property 3
            inert = bool(quote) and cw not in SHELL_INTERPRETERS  # properties 1 and 2
            if inert:
                i = end + 1
            else:
                out.extend(lines[i:end + 1])
                i = end + 1
    return "\n".join(out)


# --- session identity ------------------------------------------------------
# The shared `orch` worker broker launches each dispatched Claude worker with
# CLAUDE_CONFIG_DIR pointed at an EPHEMERAL credential copy it creates as
# `mktemp -d "<tmpbase>/orch-worker.XXXXXX"`. The orchestrator's own value is a stable
# pooled-account path. Defined here, not in each hook, so the guards that need it
# cannot drift apart.
#
# WHAT THIS MARKER IS, STATED HONESTLY. It is a LEXICAL check on caller-controlled
# text. It does NOT establish broker provenance: it proves only that the environment
# variable has that prefix, not that the broker set it, that the path exists, that it
# is a directory, or who owns it. An orchestrator that constructs a matching directory
# by hand is classified as a worker. That residual forgeability is ACCEPTED, on the
# same footing as this guard family's deliberate one-shot sentinel escape: the only
# actor positioned to forge it is the orchestrator whose own discipline the guard
# encodes, so it is a guardrail, not a security boundary.
#
# The ACCIDENTAL case, which mattered more, is closed at the source: `orch` reserves
# the `orch-worker.` label prefix (`valid_label()`, plus an explicit die on the
# `--account` path), so no orchestrator account can be labelled into a masquerade.
# An unforgeable signal (a distinct worker UID, or a root-owned marker) requires a
# privileged step the dispatch path does not currently have; it is designed as a
# deliberate lab_infra follow-up, and when it lands this function becomes a single
# ownership or UID check and this caveat goes away.
WORKER_CONFIG_DIR_PREFIX = "orch-worker."


def is_worker_session() -> bool:
    """True when CLAUDE_CONFIG_DIR's BASENAME begins with the broker's worker prefix.

    That is the whole test, and the name of this function claims more than the test
    delivers, so read the module comment above before relying on it.

    WHAT IT CHECKS: a lexical prefix on the basename. It does NOT stat the path, so a
    NONEXISTENT or UNREADABLE path bearing the prefix returns True. An earlier version
    of this docstring claimed those cases fell closed; that claim was FALSE and is
    corrected here (found by a cross-family verifier on PR #1648, which measured
    `/root/orch-worker.fake` and `/definitely/missing/orch-worker.fake` both returning
    True).

    WHAT DOES FALL CLOSED: an unset or empty variable, a path whose basename lacks the
    prefix, the prefix appearing only in a PARENT component, and any exception while
    reading the environment. In each of those a caller keeps its orchestrator behaviour,
    which is the safe direction: the worst case of a miss is the status quo.

    SCOPE: Claude-specific by construction, which is the scope that matters, since Codex
    and Gemini workers do not run Claude Code hooks at all.
    """
    try:
        config_dir = os.environ.get("CLAUDE_CONFIG_DIR", "")
        if not config_dir:
            return False
        return Path(config_dir).name.startswith(WORKER_CONFIG_DIR_PREFIX)
    except Exception:
        return False


SELF_TEST = [
    ("cat > f <<'EOF'\nPAYLOAD\nEOF",                       False),
    ("cat > f <<EOF\nPAYLOAD\nEOF",                         True),
    ("bash <<'EOF'\nPAYLOAD\nEOF",                          True),
    ("sh <<'EOF'\nPAYLOAD\nEOF",                            True),
    ("ssh host <<'EOF'\nPAYLOAD\nEOF",                      True),
    ("sudo sh <<'EOF'\nPAYLOAD\nEOF",                       True),
    ("python3 <<'EOF'\nPAYLOAD\nEOF",                       False),  # not shell: category error
    ("cat > f <<'NOEND'\nPAYLOAD\n",                        True),
    ("echo a <<< 'PAYLOAD'",                                True),
]


def _self_test() -> int:
    bad = 0
    for command, must_survive in SELF_TEST:
        survived = "PAYLOAD" in strip_heredocs(command)
        if survived != must_survive:
            bad += 1
            print("FAIL " + repr(command) + ": survived=" + str(survived)
                  + " want=" + str(must_survive))
    tail = strip_heredocs("cat > f <<'EOF'\nPAYLOAD\nEOF\nAFTERWARDS")
    if "AFTERWARDS" not in tail:
        bad += 1
        print("FAIL: text after a stripped heredoc did not survive")
    print(str(len(SELF_TEST) + 1 - bad) + "/" + str(len(SELF_TEST) + 1) + " heredoc cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
