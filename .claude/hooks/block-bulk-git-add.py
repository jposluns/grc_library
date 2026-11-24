#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse a stage-the-tree git command; require enumerated paths.

Command-text residual: this hook inspects tool_input.command, not execution.
Commands inside a script file, a heredoc fed to a shell, or a subprocess are
not generally visible. Recognizing selected shell or heredoc forms does not
provide recursive inspection of the programs they execute. See
.claude/skills/corpus-management/docs/guide-command-text-hooks.md for each hook's
limits and the independent staged-path pre-commit check.

Why: a tree-sweep stage can put a finished, unrelated change into a commit whose message
describes only a corpus-document edit, so the commit says one thing and ships another. The sweep forms stage the TREE rather than the CHANGE,
so the author's scope lives only in the commit message while the artefact inherits whatever the
tree happened to hold.

An earlier version of this hook had several high-severity bypasses. The bypass shapes, and
what this version does about each:

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

Fails OPEN on a malformed payload or an internal error. Fails CLOSED on a command whose
heredocs cannot be read with certainty (an introducer with no terminator line, raised by
_hookutil.strip_heredocs as UnreadableCommand, in the command or in an ``sh -c`` body) when
that command could reach git at all (see could_reach_git): it is refused, the escape
included, because neither reading of it is safe. An unreadable command with no word that
could be git stages nothing under either reading, so it is allowed, as before the rule.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys


def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and the root itself, .claude, .claude/hooks, the hook, the helper folder and the
    helper file must not be symlinks. The folders between .claude and a helper folder
    under .claude/skills are not checked one by one; a symlink there that leads anywhere
    else fails the real-path comparison. Only then are real paths compared, requiring
    the hook's and the helper's real locations to sit at exactly their expected places
    under the real repository root (ancestors ABOVE the root may be symlinks: both sides
    of each comparison resolve them identically). Any violation is REFUSED fail-closed:
    exit 2 with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        # A launch path holding a newline or a terminal escape is shown escaped, so the refusal
        # stays one line (each character that is neither printable nor a space separator
        # becomes its ascii() escape).
        import unicodedata
        why = "".join(char if char.isprintable() or unicodedata.category(char) == "Zs"
                      else ascii(char)[1:-1] for char in why)
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = ((".claude", "hooks") if name.startswith("_")
             else (".claude", "skills", "corpus-management", "tools"))
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


_hookutil = _load_sibling("_hookutil")
WRAPPERS = _hookutil.WRAPPERS
strip_heredocs = _hookutil.strip_heredocs
UnreadableCommand = _hookutil.UnreadableCommand

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
            return ("`git add " + sweep + "` stages the TREE without an explicit bounded pathspec; "
                    "`git add " + sweep + " -- <dir>/` is the bounded form.")
        if not sweep and paths and not real:
            return ("`git add " + paths[0] + "` is a tree root, so it stages everything. "
                    "The pathspec does not enumerate the intended files.")
        interactive = any(a in {"-p", "--patch", "-i", "--interactive", "-e", "--edit"}
                          for a in args)
        if not sweep and not paths and not interactive:
            # F-4: an interactive add presents each hunk for a decision, so the scope IS stated,
            # one hunk at a time. Blocking it would push the author toward the sweep instead.
            return "`git add` has no pathspec identifying the intended files."
    if sub == "commit":
        for a in args:
            if a == "--all" or (a.startswith("-") and not a.startswith("--")
                                and re.fullmatch(r"-[A-Za-z]+", a) and "a" in a[1:]):
                return ("`git commit " + a + "` commits every tracked modification, bypassing "
                        "staging and its explicit file selection.")
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


_GIT_WORD_BREAKS = re.compile(r"[\s;&|()<>`$={},!#*?\[\]]+")


def could_reach_git(command: str) -> bool:
    """True when any word of the RAW command could be git; never reads heredocs.

    Used only for a command strip_heredocs cannot read, so it decides nothing from
    quoting or heredoc structure. A backslash-newline is joined, every quote and
    backslash is dropped (so g'i't, "git" and an ``sh -c`` body all show their words),
    and the text is cut at whitespace and at each character _GIT_WORD_BREAKS splits on,
    which are exactly these: ; & | ( ) < > ` $ = { } , ! # * ? [ ]
    No other character cuts a word (: - % and / do not). A word that is git or ends in
    /git could be the tool, which is a superset
    of what segments() treats as a call (a token whose basename is git, after a wrapper,
    an assignment or inside ``sh -c``). Residue, stated: a name built at
    run time (a variable, an alias, $'\\x67it') is not seen here, and segments() does not
    see it either.
    """
    text = command.replace("\\\n", "")
    for ch in "'\"\\":
        text = text.replace(ch, "")
    return any(word == "git" or word.endswith("/git")
               for word in _GIT_WORD_BREAKS.split(text))


def refusal(command: str) -> str | None:
    """The block message for a command, or None when it may run.

    A command strip_heredocs cannot read with certainty is refused before the escape is
    considered, so no unclosed tail can be taken as either code or data to get past it,
    whenever any word of it could be git. With no such word it stages nothing under
    either reading, so it is allowed (a here-string or an unrelated command).
    """
    try:
        if escaped(command):
            return None
        problems = [p for p in (violation(t) for t in segments(command)) if p]
    except UnreadableCommand as exc:
        if not could_reach_git(command):
            return None
        return ("BLOCKED (bulk-git-add): a command this hook cannot read with certainty.\nWHY: "
                + str(exc) + ". A heredoc introducer with no terminator may be real or may "
                "sit in quotes or a comment, and the two readings stage different things.\n"
                "CONSIDER INSTEAD: close every here-document with its terminator line, or "
                "run the parts as separate commands. The introducer is matched as text, even "
                "inside quotes or a comment, so quoting the text that holds it does not help: "
                "write that text to a file and pass the file instead (for a commit message, "
                "git commit -F <file>).")
    if not problems:
        return None
    return ("BLOCKED (bulk-git-add): a git stage/commit with tree-wide or unspecified scope.\nWHY: " + problems[0] + "\n"
            "A tree-sweep stage makes the commit message the only record of\n"
            "scope, and that message is the half that is never verified.\n"
            "CONSIDER INSTEAD: stage the files you mean by naming their paths, then commit; "
            "when using a sweep flag, bound it with the `-- <dir>/` form above. "
            "For a genuinely intended tree sweep, lead the command with " + ESCAPE + "=1.")


def main() -> int:
    try:
        if os.environ.get(ESCAPE) == "1":
            return 0
        payload = json.load(sys.stdin)
        if payload.get("tool_name") != "Bash":
            return 0
        command = payload.get("tool_input", {}).get("command", "") or ""
        problem = refusal(command)
        if problem:
            print(problem, file=sys.stderr)
            return 2
    except Exception:
        return 0
    return 0


_G = "git"
_AND = "&& "
# The reviewed quoted-introducer escape, before its git word.
_QUOTED_ESCAPE = "echo \"<<NOEND\"\ncat > f <<'EOF'\n" + ESCAPE + "=1\nEOF\n"
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
    (_G + " -C /r add .claude/skills/corpus-management/tools/x.py", False),
    (_G + " add -A -- executive/", False),
    (_G + " add -p", False),
    (_G + " commit -m 'a message that mentions " + ESCAPE + "=1 in passing'", False),
    (_G + " commit --amend --no-edit", False),
    (_G + " status --short", False),
    (ESCAPE + "=1 " + _G + " add -A", False),     # M2: a real leading assignment escapes
    ("echo '" + ESCAPE + "=1' " + _AND + _G + " add -A", True),   # M2: a mention does NOT
    ("cat > f <<'EOF'\n" + _G + " add -A\nEOF", False),           # inert heredoc: data
    ("bash <<'EOF'\n" + _G + " add -A\nEOF", True),               # H7: interpreter body is a program
    ("cat > f <<NOEND <<'EOF'\n$(" + _G + " add -A)\nEOF", True),  # unterminated tag: its body expands
    # An introducer with no terminator is refused, so no unclosed tail reaches the escape.
    ("cat > f <<'NOEND' <<'EOF'\n" + _G + " add -A\nEOF", True),     # two tags, first unterminated
    ("echo \"<<NOEND\"\ncat > f <<'EOF'\n" + ESCAPE + "=1\nEOF\n" + _G + " add -A", True),   # in quotes
    ("# <<NOEND\ncat > f <<'EOF'\n" + ESCAPE + "=1\nEOF\n" + _G + " add -A", True),          # in a comment
    ("echo \"<<NOEND\"; cat > f <<'EOF'\n" + ESCAPE + "=1\nEOF\n" + _G + " add -A", True),  # joined by ;
    (ESCAPE + "=1 " + _G + " add -A <<NOEND", True),          # the escape itself is not read
    ("cat > f <<'EOF'\n" + ESCAPE + "=1\nEOF\n" + _G + " add -A", True),   # closed body is data
    ("cat > f <<'EOF'\nx\nEOF\n" + _G + " add a.md", False),           # closed heredoc still read
    # The fail-closed rule is scoped: an unreadable command with no word that could be git
    # stages nothing, so it is allowed; any word that could be git keeps it refused.
    ("cat <<< x", False),                                       # herestring, not an introducer
    ("echo \"<<NOEND\"; ls", False),                             # unpaired, no git word
    ("printf %s x | wc -c", False),
    ("echo \"<<NOEND\"\n" + _G + " status", True),                # unpaired, a git word
    (_QUOTED_ESCAPE + "/usr/bin/" + _G + " add -A", True),           # a path to git
    (_QUOTED_ESCAPE + "g'i't add -A", True),                        # quotes split the word
    (_QUOTED_ESCAPE + "sh -c 'g\"i\"t add -A'", True),                # inside sh -c
    (_QUOTED_ESCAPE + "gi\\\nt add -A", True),                      # backslash-newline
    (_QUOTED_ESCAPE + "{" + _G + ",add} -A", True),                  # brace expansion
    ("cat <<< x\ncat > f <<'EOF'\n" + ESCAPE + "=1\nEOF\n" + _G + " add -A", True),
    ("cat <<< x\n" + _G + " add a.md", False),                     # herestring: still read
]


def self_test() -> int:
    bad = 0
    for command, should_block in SELF_TEST:
        got = refusal(command) is not None
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
