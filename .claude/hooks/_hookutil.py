"""Shared helpers for the PreToolUse Bash hooks. Not a hook itself.

The heredoc-stripping code lives here rather than in each hook, so the hooks that need it share
one implementation and one set of fixtures instead of duplicated copies that can drift apart.
"""

from __future__ import annotations

import os
import re
import shlex

# A heredoc INTRODUCER. Three angle brackets is a herestring, not a heredoc, and `a << b` is a
# shift: both are meant to be excluded by rejecting a bracket on either side of the pair and
# requiring a shell-word tag. A bracket before the pair matters: without that check the
# pattern matched the last two brackets of `<<< word`. The exclusion is still textual: a
# shift by a name, or `<<` in quotes or a comment, can match. Such a match with no
# terminator line is unreadable (UnreadableCommand), and each consumer decides whether that
# command can matter to it.
_HEREDOC = re.compile(r"(?<!<)<<-?(?!<)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")

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


class UnreadableCommand(Exception):
    """strip_heredocs cannot read the command with certainty, and each consumer decides.

    Raised when a heredoc introducer has no terminator line. The introducer may be real, so
    the rest of the command is its unclosed body, or false (inside quotes or a comment), so
    bash reads no heredoc there and a later quoted body is still data. The text alone does
    not tell the two apart, and each reading hides something the other shows, so neither is
    chosen. The bulk-add hook (block-bulk-git-add.py) refuses such a command only when the
    command could reach git (its could_reach_git rule); one with no word that could be git
    stages nothing under either reading, so that hook allows it. Deliberately not a
    ValueError, so no tokeniser fallback can swallow it.
    """


def strip_heredocs(command: str) -> str:
    """Remove heredoc BODIES that are DATA; keep bodies that are PROGRAMS.

    Three properties the first version got wrong, each proved by a verifier probe:

    1. A body introduced by an interpreter or a remote shell IS executed. Stripping it hid real
       mutating commands from the guards, a live weakening rather than a theoretical one. Those
       bodies are KEPT.
    2. An UNQUOTED tag expands command substitutions in the body, so a substitution written there
       runs. Only a quoted tag is inert. Unquoted bodies are KEPT.
    3. An introducer with no matching terminator cannot be read with certainty. Swallowing the
       remainder of the command was a universal bypass for every guard downstream. Keeping
       the remainder whole is right only when the introducer is real: a false one (quoted,
       or in a comment) is not a heredoc to bash, so a later quoted body is data, and
       keeping it let that data satisfy an escape check. Neither guess is safe, so this
       raises UnreadableCommand and each consumer decides. The bulk-add hook refuses the
       command (fails closed) only when it could reach git (see could_reach_git in
       block-bulk-git-add.py); with no word that could be git, that hook allows it.

    A stripped body keeps its terminator line as well as its introducer: dropping the
    terminator left an unclosed introducer, so a later reader of the stripped text could take
    the lines after it as here-document body.
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
            if end is None:                                 # property 3
                raise UnreadableCommand("heredoc tag " + tag + " has no terminator line, so "
                                        "the command cannot be read with certainty")
            inert = bool(quote) and cw not in SHELL_INTERPRETERS  # properties 1 and 2
            if inert:
                out.append(lines[end])                      # keep the terminator
                i = end + 1
            else:
                out.extend(lines[i:end + 1])
                i = end + 1
    return "\n".join(out)


SELF_TEST = [
    ("cat > f <<'EOF'\nPAYLOAD\nEOF",                       False),
    ("cat > f <<EOF\nPAYLOAD\nEOF",                         True),
    ("bash <<'EOF'\nPAYLOAD\nEOF",                          True),
    ("sh <<'EOF'\nPAYLOAD\nEOF",                            True),
    ("ssh host <<'EOF'\nPAYLOAD\nEOF",                      True),
    ("sudo sh <<'EOF'\nPAYLOAD\nEOF",                       True),
    ("python3 <<'EOF'\nPAYLOAD\nEOF",                       False),  # not shell: category error
]

# An introducer with no terminator: strip_heredocs must raise UnreadableCommand, never return.
SELF_TEST_UNREADABLE = [
    "cat > f <<'NOEND'\nPAYLOAD\n",
    "cat > f <<'NOEND' <<'EOF'\nPAYLOAD\nEOF",               # unterminated tag first
    "cat > f <<NOEND <<'EOF'\nPAYLOAD\nEOF",                 # and its body expands
    "cat > f <<'NOEND'\nPAYLOAD\ncat > g <<'EOF'\nBODY\nEOF",
    "echo \"<<NOEND\"\ncat > f <<'EOF'\nPAYLOAD\nEOF",           # false introducer in quotes
    "# <<NOEND\ncat > f <<'EOF'\nPAYLOAD\nEOF",                # false introducer in a comment
    "echo \"<<NOEND\"; cat > f <<'EOF'\nPAYLOAD\nEOF",          # quoted, joined by ; on one line
]

# EXACT stripped output. A stripped body keeps its introducer AND its terminator, so a later
# reader of the stripped text still sees a closed here-document and never takes the lines
# after it as body. Every tag here is terminated, so each is read exactly as before.
SELF_TEST_EXACT = [
    ("cat > f <<'EOF'\nPAYLOAD\nEOF\nAFTERWARDS",            "cat > f <<'EOF'\nEOF\nAFTERWARDS"),
    ("cat > f <<'EOF'\nPAYLOAD\nEOF",                        "cat > f <<'EOF'\nEOF"),
    ("cat > f <<'EOF'\nPAYLOAD\nEOF\ncat > g <<'END'\nBODY\nEND",
     "cat > f <<'EOF'\nEOF\ncat > g <<'END'\nEND"),
    ("cat > f <<-'EOF'\n\tPAYLOAD\n\tEOF",                  "cat > f <<-'EOF'\n\tEOF"),
    ("cat > f <<EOF\nPAYLOAD\nEOF",                          "cat > f <<EOF\nPAYLOAD\nEOF"),
    ("echo a <<< 'PAYLOAD'",                                  "echo a <<< 'PAYLOAD'"),  # herestring
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
    for command, want in SELF_TEST_EXACT:
        got = strip_heredocs(command)
        if got != want:
            bad += 1
            print("FAIL " + repr(command) + ": got=" + repr(got) + " want=" + repr(want))
    for command in SELF_TEST_UNREADABLE:
        try:
            got = strip_heredocs(command)
        except UnreadableCommand:
            continue
        bad += 1
        print("FAIL " + repr(command) + ": read as " + repr(got) + ", want UnreadableCommand")
    total = len(SELF_TEST) + 1 + len(SELF_TEST_EXACT) + len(SELF_TEST_UNREADABLE)
    print(str(total - bad) + "/" + str(total) + " heredoc cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
