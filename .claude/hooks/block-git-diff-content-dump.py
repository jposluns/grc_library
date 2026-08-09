#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse a command that puts a +/- unified diff of file CONTENT on the CONSOLE.

PR1b ACTIVATION CANDIDATE, hardened 2026-08-09 against the seed deep review
(`inbox/deliveries/seed-review-pr1b-codex.md`). Wiring: install as
`.claude/hooks/block-git-diff-content-dump.py`, matcher `"Bash"`, command
`python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/block-git-diff-content-dump.py`.

WHY THIS EXISTS. The rule is maintainer-directed 2026-07-26, after repeated violations, and it is
stated as a hard one in `.claude/CLAUDE.md`: "NEVER run a command whose output is a +/- unified diff
of file content: no `git diff` / `git show <commit>` without `--stat` or `--name-only`". The console
is the maintainer's live window onto the run; a wall of added/removed lines pushes what they
actually need to read off the screen, and it has scrolled a real issue out of view more than once.
Running the diff "to inspect a change" is exactly how the wall keeps reaching the console, so the
prose control has been tried and has failed. This is its mechanical backstop.

THE MODEL, and it is the reviewable part. The guard answers ONE question per command: does a +/-
content body reach the CONSOLE? That is three separate sub-questions, and the seed conflated them:

  0. WHICH TEXT IS EVEN A COMMAND (heredoc data vs
     program, quoting, command substitution)              -> `_strip_heredocs_local`,
                                                             `_split_substitutions`, `_segments`
  1. WHAT COMMAND runs (grammar and indirection)          -> `_command_index`, `_git_invocation`
  2. WHETHER GIT WILL EMIT A PATCH BODY (git option mode) -> `_git_prints_content`
  3. WHETHER THAT BODY REACHES THE CONSOLE (redirect,
     pipeline consumer, command substitution)             -> `_reaches_console`

GIT OUTPUT MODE (question 2) is resolved by OPTION ORDER against git's real grammar, not by an
"exemption anywhere" scan. The model was verified empirically against git 2.53.0 on the pinned
library repository (output counted with `wc -l` / `grep -c`, never printed):

    output_format starts empty.
      * a PATCH flag  (-p, -u, --patch, -U<n>, --unified=<n>, --patch-with-stat,
                       --patch-with-raw, --cc, and post-subcommand -c)  -> patch ON  (explicit)
      * a SUMMARY flag (--stat, --numstat, --shortstat, --dirstat, --summary,
                        --compact-summary, --raw)                       -> format SET, patch UNCHANGED
      * -s / --no-patch                                                 -> format SET, patch OFF
      * --name-only, --name-status, --quiet, --check                    -> HARD suppress, order-free
    content = (not hard_suppress) and (explicit_patch or (format never set and the subcommand
                                       prints a patch by default))

    Verified consequences, all of which the seed got WRONG:
      git diff --stat -p / -p --stat   -> 230 content rows   (summary NEVER beats an explicit -p)
      git diff --no-patch --patch      -> 230 content rows   (order-sensitive: later wins)
      git diff --patch --no-patch      ->   0 content rows
      git diff -sp / -ps               -> 230 / 0            (clustered shorts obey the same order)
      git show -s -p HEAD              -> 230 content rows
      git log -pU1                     -> 230 content rows   (clustered short with an inline value)
      git log -c / --cc                -> 230 content rows   (-c implies -p for log)
      git diff --name-only -p          ->   0 content rows   (NAME/NAME-STATUS strip the patch bit)
      git diff --check -p              ->   0 content rows
      git diff --quiet -p              ->   0 content rows
      git log --full-diff              ->   0 content rows   (the seed listed it as a PATCH flag;
                                                              it only WIDENS an existing patch, and
                                                              the seed therefore false-blocked it)

CONSOLE REACHABILITY (question 3). A content body is only a violation if the maintainer sees it:
  * stdout redirected to a QUIET destination            -> allowed (see ALLOW_FILE_REDIRECT)
  * stdout redirected to a CONSOLE-FACING destination   -> BLOCKED. /dev/tty, /dev/console,
    /dev/stdout, /dev/stderr, /dev/fd/1|2, /proc/<pid|self>/fd/1|2, /dev/pts/<n>, `>&1`, `>&2`,
    and process substitution `> >(cat)` all relay to the screen. The seed treated every `>` as safe.
  * quiet redirect spellings `&>`, `&>>`, `>|`, `1>` are recognised; `2>` is stderr and does not
    exempt; `2>&1` does not steal the classification from an earlier `> file`; `--output=<file>` is
    a git-native redirect and is classified the same way.
  * a pipeline whose downstream stage CONSUMES rather than relays (`| wc -l`, `| grep -c`,
    `| md5sum`, `| sha256sum`) puts a COUNT on the console, not a wall -> allowed.
    `| head`, `| tail`, `| cat`, `| less`, `| tee`, `| grep <pat>` RELAY -> still blocked.
  * a command substitution captured by an ASSIGNMENT or a test (`x=$(git diff)`,
    `if [ -n "$(git diff)" ]`) prints nothing -> allowed. A substitution whose value flows into a
    printing command (`echo $(git diff)`, ``echo `git diff` ``) -> BLOCKED.

ACTIVATION CLAIM, deliberately NARROW and stated so it can be checked. This hook has a MECHANICAL
backstop for exactly these reach-forms, each covered by a self-test fixture:
    plain segments; `;` `&&` `||` `|` `&` lists; subshells `( ... )`; brace groups `{ ... }`;
    shell reserved words (`if/then/else/elif/fi/while/until/do/done/for/case/esac`); `!` negation;
    leading VAR=value assignments; wrapper words (sudo, env, doas, nohup, command, exec, time,
    timeout, stdbuf, nice, ionice, setsid, script, xargs) INCLUDING their separate-value options
    (`env -u FOO git diff`, `timeout -k 5 30 git diff`, `sudo -u root git diff`);
    `$( ... )` and backtick command substitution, nested, quote-aware;
    process substitution `<( ... )` and `>( ... )`;
    shell-interpreter bodies `sh|bash|zsh|dash|ksh|ash -c '<program>'` and `eval '<program>'`;
    command-local git aliases `git -c alias.d=diff d`, including `!shell` alias bodies;
    clustered short options per git's grammar (`-pU1`, `-sp`, `-ps`, `-U1` value consumption);
    heredoc bodies (`<<EOF`, `<<'EOF'`, `<<-EOF`), resolved DATA-vs-PROGRAM before segmentation.

RESIDUE -- NO mechanical backstop, prose rule only. This is the narrower, honest claim chosen over a
wider one the parser cannot keep. Stated here rather than implied:
  * a PERSISTENT git alias (`~/.gitconfig` `[alias] d = diff`), a shell function, or a script this
    hook cannot read. Only the command-local `-c alias.<name>=` form is parsed.
  * a NON-shell interpreter body (`python3 -c 'os.system("git diff")'`, perl, ruby, node), and the
    same body delivered as a heredoc (`python3 <<'EOF'`). This is the documented
    `_hookutil.NON_SHELL_INTERPRETERS` position: shell text inside a python string is not shell, and
    scanning it is a category error that produced a real false catch before.
  * a heredoc body whose DATA is written to a file but reaches the guard as a live substitution:
    `cat > f <<EOF` with `$(git diff)` in the body is BLOCKED even though the wall lands in `f`.
    An UNQUOTED tag really does run the substitution, and proving where its stdout lands would mean
    threading the heredoc's own destination into the substitution classifier. The conservative side
    was chosen for a guardrail, the cost is one false block, and the remedy is one quote character:
    `<<'EOF'` is inert and is ALLOWED. Asserted as a fixture so the behaviour is visible, not
    discovered.
  * `ssh host git diff`. The remote emits the wall onto this console, but ssh's option grammar plus
    a remote command is a second parser; out of scope by choice.
  * git reached through a variable (`G=git; $G diff`), `eval` of a string built at runtime, or any
    base64 / printf-constructed command.
  * `cat` of a diff previously redirected to a file with a NON-patch suffix
    (`git diff > /tmp/d.txt; cat /tmp/d.txt`). The `.diff` / `.patch` suffix case IS covered, see
    COVER_PATCH_FILE_DUMP.
  * a tokenizer failure FAILS OPEN (see the exit protocol). Unbalanced quotes normally fail in the
    shell too, so this is not a demonstrated live bypass, but every future parser change needs a
    regression fixture here; seven are present.

SCOPE, relative to the `.claude/CLAUDE.md` "no diff, no patch dump" sentence. The seed excluded
non-git diff tooling entirely, which left the hook narrower than the rule it backstops. This version
CLOSES that gap where the tool actually renders a wall:
  * `diff` / `colordiff` / `sdiff` / `icdiff`   -> BLOCK unless `-q` / `--brief` / `--help`
  * `git difftool`                              -> BLOCK unless `--help` / `--tool-help`
  * `git format-patch`                          -> BLOCK only with `--stdout`. Without it,
                                                   format-patch WRITES FILES and prints file names.
  * `cat|bat|less|more|most|view|tac|nl <f>.diff|.patch`  -> BLOCK (COVER_PATCH_FILE_DUMP). This
    also closes the seed's acknowledged `git diff > /tmp/d.diff; cat /tmp/d.diff` loop.
    BOUNDED readers (`head`, `tail`, `sed -n`, `grep`) are the sanctioned alternative and stay ALLOWED.
  * `patch -p1 < f` stays OUT of scope, and the reason is not an omission: `patch` APPLIES a patch
    and prints status lines. It does not render one.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds stderr
back to the model as the reason. FAIL-OPEN on any tokenizer or parse failure: a guardrail against
one known mistake, not a security boundary, and a hook that could block all Bash on a malformed
command would be worse than the mistake it prevents.

Severity: `BLOCK_SEVERITY = True` (exit 2). The rule is maintainer-directed, was restated as a HARD
rule after repeated violations, and the allowed alternatives are one flag away, so the friction of a
block is close to zero. Flip to False for WARN-only (exit 0, message still printed, header reads
WARNING and never BLOCKED).

JUDGEMENT CALLS left visible as module constants, each asserted on BOTH settings by the self-test:
  ALLOW_FILE_REDIRECT (True)             -- a quiet redirect is not the wall the rule forbids.
  REQUIRE_LITERAL_REDIRECT_TARGET (True) -- `git diff > "$OUT"` is NOT exempt. An exemption has to
      be provable from the command text; an unexpanded destination could be /dev/tty. It costs a
      false block on a legitimate `> "$TMP/d.diff"`; the remedy is to write a literal path.
  COVER_NON_GIT_DIFF (True), COVER_PATCH_FILE_DUMP (True) -- see SCOPE above.

REGISTER. Each fire appends one row to `/home/grc/grc_working/guard-fires.tsv` (four columns, the
shipped self-QA hook's format) so PR1b has ONE calibration stream across all of its guards.
Best-effort: `log_fire()` returns False rather than raising, and the caller ignores the result, so a
logging failure can never cost a block. The `_hook_state.record_block()` integration is preserved
alongside it; that records recent block-loop state, which is a different observable.

DOCUMENTATION COLLISIONS -- ORCHESTRATOR MUST RESOLVE IN THIS PR (carried forward from the review):
  1. `.claude/CLAUDE.md:796` still recommends bare `git diff` as a read-back. It collides with
     `.claude/CLAUDE.md:868` and with this hook.
  2. `references/pr-lifecycle.md:55-59` directs shared-tree verifiers to bare `git diff`; the same
     text is copied into `guardrails/governance/ai-assistant-workflow-disciplines.md:245-247`,
     `guardrails/governance/validate-inference-before-action.md:117-125`,
     `guardrails/skills/validate-inference/SKILL.md:45-48`, and
     `guardrails/skills/validation-sweep-pr-scoped/SKILL.md:47-53`.
  3. The PR-scoped validation skill genuinely needs CONTENT review, so substituting `--stat` loses
     the evidence. The sanctioned non-console mechanism is `git diff > /tmp/<id>.diff` followed by a
     BOUNDED read (`sed -n`, `grep -n | cut -c1-120`) -- both of which this hook allows by design.

Self-test: `python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/block-git-diff-content-dump.py --self-test`
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path

# BLOCK (exit 2) on a content-producing form. False downgrades to WARN-only (exit 0 + stderr).
BLOCK_SEVERITY = True

# A segment whose stdout goes to a QUIET destination prints nothing to the console.
ALLOW_FILE_REDIRECT = True

# An exemption must be PROVABLE from the command text: `> $OUT` could expand to /dev/tty.
REQUIRE_LITERAL_REDIRECT_TARGET = True

# Non-git diff renderers, and dumps of a saved patch file. See SCOPE in the docstring.
COVER_NON_GIT_DIFF = True
COVER_PATCH_FILE_DUMP = True

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working"))
FIRE_LOG = WORKING_ROOT / "guard-fires.tsv"

# Set by --self-test so the fixtures never touch the real register or block-loop state.
SELF_TEST_MODE = False

# Shell operators that END a command segment, as produced by shlex(punctuation_chars=True).
# Redirect operators are deliberately NOT here: they belong to the segment they modify.
SEPARATORS = {";", ";;", "&&", "||", "|", "&", "|&", "(", ")", "\n"}

# Reserved words and grouping tokens that may PRECEDE the real command word in valid shell.
NOISE_WORDS = {"{", "}", "!", "if", "then", "else", "elif", "fi", "while", "until", "do", "done",
               "for", "select", "case", "esac", "in", "function", "[[", "]]", "((", "))"}

# --------------------------------------------------------------------------------------------
# Layer -1: heredoc bodies are DATA, not commands
# --------------------------------------------------------------------------------------------
# This runs BEFORE segmentation, and it has to, because `_segments` splits on newlines and would
# otherwise read every body line of `cat > note.md <<'EOF' / git diff / EOF` as a command word.
# That was a real FALSE BLOCK: the body is text being written to a file, and the guard refused it.
#
# The implementation below is a STANDALONE copy of `_hookutil.strip_heredocs`, kept in-file on
# purpose. The previous fallback was `return command`, a no-op, so the hook silently lost heredoc
# semantics whenever the shared module was not importable -- which is exactly the condition under
# which this file is reviewed and self-tested as a single fenced block. A guard whose verdict
# depends on whether a sibling import resolved is not reviewable. The shared module is still
# PREFERRED when present (one implementation, per the PR #1441 de-duplication), and the self-test
# asserts PARITY between the two so the copy cannot drift.

# A heredoc INTRODUCER. Three angle brackets is a herestring and `a << b` is a shift: both are
# excluded by rejecting a third bracket and requiring a shell-word tag. `<<-` is the tab-stripping
# form and its terminator may be indented, which the `.strip()` comparison below already accepts.
_HEREDOC_RE = re.compile(r"<<-?(?!<)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")

# Command words whose heredoc BODY is a shell PROGRAM rather than data. Stripping one of these
# would hide real commands from the guard -- `bash <<'EOF' / git diff / EOF` runs the diff -- so
# those bodies are KEPT and scanned. Mirrors `_hookutil.SHELL_INTERPRETERS`.
_HEREDOC_BODY_IS_SHELL = {
    "bash", "sh", "zsh", "dash", "ksh", "csh", "tcsh", "fish",
    "ssh", "sudo", "doas", "su", "docker", "podman", "kubectl", "nsenter", "chroot",
    "env", "nohup", "timeout", "xargs", "eval", "script",
}

# Wrapper words that PRECEDE the real command word. Same set as `_hookutil.WRAPPERS`; used by the
# standalone command-word resolver and as the WRAPPERS fallback when the import fails.
_FALLBACK_WRAPPERS = {"sudo", "doas", "env", "nohup", "command", "exec", "time", "timeout",
                      "stdbuf", "nice", "ionice", "setsid", "script", "xargs"}


def _fallback_command_word(line: str) -> str:
    """The effective command word of one line, skipping assignments, wrappers and their arguments."""
    try:
        tokens = shlex.split(line, comments=False)
    except ValueError:
        tokens = line.split()
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if _ASSIGN_RE.fullmatch(tok):
            i += 1
            continue
        base = os.path.basename(tok)
        if base in _FALLBACK_WRAPPERS:
            i += 1
            while i < len(tokens) and (tokens[i].startswith("-")
                                       or re.fullmatch(r"[\d.]+[smhd]?", tokens[i])):
                i += 1
            continue
        return base
    return ""


def _strip_heredocs_local(command: str) -> str:
    """Remove heredoc BODIES that are DATA; keep bodies that are PROGRAMS.

    Three properties, each of which a naive strip gets wrong and each of which has a fixture:

    1. A body introduced by an interpreter or a remote shell IS EXECUTED. `bash <<'EOF' /
       git diff / EOF` really runs the diff, so stripping it would be a live WEAKENING, not a
       theoretical one. Those bodies are KEPT and scanned.
    2. An UNQUOTED tag EXPANDS the body, so `<<EOF` containing `$(git diff)` really runs the
       substitution. Only a quoted tag (`<<'EOF'`, `<<"EOF"`) is inert. Unquoted bodies are KEPT.
    3. A false introducer with NO matching terminator must remove NOTHING. Swallowing the
       remainder of the command would be a universal bypass for every check downstream.

    A NON-shell interpreter body (`python3 <<'EOF'`) is stripped rather than scanned: shell text
    inside a python program is not a shell command, and scanning it produced a real false catch.
    That is the documented `_hookutil.NON_SHELL_INTERPRETERS` position and it is RESIDUE, stated
    in the module docstring rather than claimed away.
    """
    lines = command.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        cw = _fallback_command_word(line)
        for quote, tag in _HEREDOC_RE.findall(line):
            end = None
            for j in range(i, len(lines)):
                if lines[j].strip() == tag:              # `<<-` may indent its terminator
                    end = j
                    break
            if end is None:
                continue                                 # property 3: remove NOTHING
            if bool(quote) and cw not in _HEREDOC_BODY_IS_SHELL:
                i = end + 1                              # inert DATA: drop body and terminator
            else:
                out.extend(lines[i:end + 1])             # properties 1 and 2: keep and scan
                i = end + 1
    return "\n".join(out)


try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _hookutil import WRAPPERS, strip_heredocs
    _HEREDOC_IMPL = "_hookutil"
except Exception:                                        # pragma: no cover - standalone fallback
    WRAPPERS = set(_FALLBACK_WRAPPERS)
    strip_heredocs = _strip_heredocs_local
    _HEREDOC_IMPL = "in-file"

# Wrapper options that consume a SEPARATE following value. Without this table `env -u FOO git diff`
# loses the command word at `FOO` and the whole invocation goes unseen (review HIGH-2).
WRAPPER_VALUE_OPTS = {
    "env":     {"-u", "--unset", "-S", "--split-string", "-C", "--chdir"},
    "timeout": {"-s", "--signal", "-k", "--kill-after"},
    "xargs":   {"-n", "--max-args", "-I", "-i", "--replace", "-d", "--delimiter", "-P",
                "--max-procs", "-L", "-s", "--max-chars", "-E", "-a", "--arg-file"},
    "nice":    {"-n", "--adjustment"},
    "ionice":  {"-c", "--class", "-n", "--classdata", "-p", "--pid"},
    "stdbuf":  {"-i", "--input", "-o", "--output", "-e", "--error"},
    "sudo":    {"-u", "--user", "-g", "--group", "-C", "-p", "--prompt", "-r", "--role",
                "-t", "--type", "-D", "--chdir"},
    "doas":    {"-u", "-C"},
    "script":  {"-c", "--command", "-f", "-t", "--timing"},
    "exec":    {"-a"},
    "time":    {"-f", "--format", "-o", "--output"},
}

# Shell interpreters whose `-c` body is a shell PROGRAM and is therefore parsed recursively.
SHELL_INTERPRETERS = {"sh", "bash", "zsh", "dash", "ksh", "mksh", "ash"}

# git's own global options, which sit BEFORE the subcommand.
_GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path",
                        "--super-prefix", "--config-env", "--attr-source"}

# Subcommands whose DEFAULT output format is a patch.
ALWAYS_CONTENT = {"diff", "show", "range-diff"}

# Subcommands that emit a patch ONLY when an explicit patch flag is present.
CONTENT_IF_PATCH = {"log", "diff-tree", "diff-index", "diff-files", "whatchanged", "stash"}

# Long flags that SET the output format without touching the patch bit (verified additive).
SUMMARY_LONG = {"--stat", "--numstat", "--shortstat", "--dirstat", "--summary",
                "--compact-summary", "--raw", "--cumulative", "--stat-width", "--stat-name-width",
                "--stat-count"}

# Long flags that suppress the body regardless of ORDER (verified: they beat a later -p).
HARD_SUPPRESS_LONG = {"--name-only", "--name-status", "--quiet", "--check"}

# Long flags that turn the patch body ON.
PATCH_LONG = {"--patch", "--patch-with-stat", "--patch-with-raw", "--cc", "--unified"}

# Order-sensitive suppressor: sets the format (so no default patch) and clears an earlier patch.
NO_PATCH_LONG = {"--no-patch"}

# git options taking a SEPARATE value whose value could otherwise be misread as a flag.
GIT_LONG_VALUE_OPTS = {"--output", "--pretty", "--format", "--grep", "--author", "--committer",
                       "--since", "--until", "--before", "--after", "--max-count", "--skip",
                       "--diff-filter", "--find-object", "--anchored", "--src-prefix",
                       "--dst-prefix", "--line-prefix", "--word-diff-regex", "--ignore-submodules",
                       "-S", "-G", "-O", "-L", "-n"}

# Short-option letters that consume the REST of their cluster (or the next token) as a value.
# Verified: `git log -U1p` errors with "--unified expects a numerical value", so `p` really is
# swallowed by `U` and a cluster parser must stop there.
_SHORT_VALUE_LETTERS = set("SGOlIUxX")

# Stdout redirect operators. `2>` arrives as the two tokens `2` and `>`; the fd check handles it.
REDIR_STDOUT_OPS = {">", ">>", ">|", "&>", "&>>", ">&"}

# Destinations that relay to the maintainer's screen. A redirect to one of these is NOT an exemption.
CONSOLE_TARGETS = {"/dev/tty", "/dev/console", "/dev/stdout", "/dev/stderr", "/dev/ptmx"}
_CONSOLE_FD_RE = re.compile(
    r"^(?:/dev/fd/[12]|/proc/(?:self|thread-self|\d+)/fd/[12]|/dev/pts/\d+)$")

# Pipeline stages that CONSUME rather than relay: their console output is a count or a digest.
NON_RELAYING = {"wc", "md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum",
                "shasum", "b2sum", "cksum", "sum", "true", ":"}

# grep only consumes when it is counting or testing.
_GREP_COMMANDS = {"grep", "egrep", "fgrep", "rg", "ggrep"}
_GREP_QUIET_FLAGS = {"-c", "--count", "-q", "--quiet", "--silent", "-l", "-L",
                     "--files-with-matches", "--files-without-match"}

# Words whose enclosing context CAPTURES a command substitution instead of printing it.
CAPTURING_WORDS = {"[", "[[", "test", "local", "export", "declare", "readonly", "typeset", "let",
                   "if", "while", "until", "elif", "return", "exit"}

# Non-git renderers of the same wall (COVER_NON_GIT_DIFF).
DIFF_COMMANDS = {"diff", "colordiff", "sdiff", "icdiff"}
DIFF_QUIET_FLAGS = {"-q", "--brief", "-h", "--help", "--version", "--report-identical-files"}

# Unbounded dumpers of a saved patch (COVER_PATCH_FILE_DUMP). Bounded readers stay allowed.
DUMP_COMMANDS = {"cat", "bat", "batcat", "less", "more", "most", "view", "tac", "nl"}
PATCH_SUFFIXES = (".diff", ".patch")

_ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*", re.DOTALL)
_SUBST_PLACEHOLDER = "__GRC_SUBST__"
_MAX_DEPTH = 5


# --------------------------------------------------------------------------------------------
# Layer 0: quote-aware extraction of command substitutions
# --------------------------------------------------------------------------------------------

def _match_paren(text: str, open_idx: int) -> int:
    """Index of the `)` matching the `(` at open_idx, or -1. Quoted parens do not count."""
    depth = 0
    i = open_idx
    n = len(text)
    in_single = False
    in_double = False
    while i < n:
        ch = text[i]
        if in_single:
            if ch == "'":
                in_single = False
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "'" and not in_double:
            in_single = True
        elif ch == '"':
            in_double = not in_double
        elif not in_double:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def _match_backtick(text: str, start: int) -> int:
    i = start
    n = len(text)
    while i < n:
        if text[i] == "\\" and i + 1 < n:
            i += 2
            continue
        if text[i] == "`":
            return i
        i += 1
    return -1


def _is_capturing_context(prefix: str) -> bool:
    """True when the substitution's stdout is swallowed by its context rather than printed.

    This is the difference between `x=$(git diff)` (prints nothing, allowed) and
    `echo $(git diff)` (prints the wall, blocked). Heuristic by design; see RESIDUE.
    """
    words = prefix.split()
    if not words:
        return False
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=[\"']?", words[-1]):
        return True                                      # x=$( ... )
    for w in words:
        if os.path.basename(w.strip("\"'")) in CAPTURING_WORDS:
            return True
    return False


def _split_substitutions(text: str):
    """(outer_text, [(inner_text, captured), ...]) for `$(...)`, backticks and `<(...)`/`>(...)`.

    Quote-aware: a substitution inside SINGLE quotes is inert and left alone; one inside DOUBLE
    quotes is live and IS extracted, which is why `echo "$(git diff)"` is caught. `$(( ))` is
    arithmetic, not a command, and is replaced without recursion. Raises on unbalanced input, which
    the caller turns into a fail-open ALLOW.
    """
    out = []
    inner = []
    i = 0
    n = len(text)
    in_single = False
    in_double = False
    last_break = 0                                       # start of the current shell word run
    while i < n:
        ch = text[i]
        if in_single:
            if ch == "'":
                in_single = False
            out.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            out.append(text[i:i + 2])
            i += 2
            continue
        if ch == "'" and not in_double:
            in_single = True
            out.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = not in_double
            out.append(ch)
            i += 1
            continue
        if not in_double and ch in ";&|\n(){}":
            out.append(ch)
            i += 1
            last_break = len(out)
            continue
        if ch == "`":
            end = _match_backtick(text, i + 1)
            if end < 0:
                raise ValueError("unterminated backtick")
            inner.append((text[i + 1:end], _is_capturing_context("".join(out[last_break:]))))
            out.append(_SUBST_PLACEHOLDER)
            i = end + 1
            continue
        if text.startswith("$((", i):
            end = _match_paren(text, i + 1)              # arithmetic: opaque, no recursion
            if end < 0:
                raise ValueError("unterminated arithmetic expansion")
            out.append(_SUBST_PLACEHOLDER)
            i = end + 2                                  # skip the second `)` of `))`
            continue
        if text.startswith("$(", i):
            end = _match_paren(text, i + 1)
            if end < 0:
                raise ValueError("unterminated command substitution")
            inner.append((text[i + 2:end], _is_capturing_context("".join(out[last_break:]))))
            out.append(_SUBST_PLACEHOLDER)
            i = end + 1
            continue
        if ch in "<>" and not in_double and text.startswith("(", i + 1):
            end = _match_paren(text, i + 1)
            if end < 0:
                raise ValueError("unterminated process substitution")
            # A process-substitution body is NOT captured: `cat <(git diff)` and `> >(cat)` both
            # relay. The `>(` marker is preserved so the redirect classifier can see it.
            inner.append((text[i + 2:end], False))
            out.append(ch + "(" + _SUBST_PLACEHOLDER + ")")
            i = end + 1
            continue
        out.append(ch)
        i += 1
    if in_single or in_double:
        raise ValueError("unbalanced quote")
    return "".join(out), inner


# --------------------------------------------------------------------------------------------
# Layer 1: segmentation
# --------------------------------------------------------------------------------------------

def _tokenize(line: str):
    """Operator-aware, QUOTE-aware token list for one line. Raises on an unbalanced quote."""
    lex = shlex.shlex(line, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    return list(lex)


def _segments(text: str):
    """[(tokens, operator_that_followed), ...].

    Newlines are split FIRST, because shlex treats a newline as ordinary whitespace and would
    otherwise fuse two lines into one segment, letting a `--stat` on line 1 exempt a bare
    `git diff` on line 2.
    """
    out = []
    for line in text.split("\n"):
        if not line.strip():
            continue
        current = []
        for tok in _tokenize(line):
            if tok in SEPARATORS:
                if current:
                    out.append((current, tok))
                current = []
            else:
                current.append(tok)
        if current:
            out.append((current, "\n"))
    return out


# --------------------------------------------------------------------------------------------
# Layer 2: which command is this segment actually running
# --------------------------------------------------------------------------------------------

def _skip_wrapper_args(tokens, i: int, wrapper: str) -> int:
    vals = WRAPPER_VALUE_OPTS.get(wrapper, set())
    while i < len(tokens):
        tok = tokens[i]
        if _ASSIGN_RE.fullmatch(tok):
            i += 1                                       # env FOO=1 git diff
            continue
        if tok in vals:
            i += 2                                       # the option and its separate value
            continue
        if tok.startswith("--") and tok.split("=", 1)[0] in vals:
            i += 1
            continue
        if tok.startswith("-") and len(tok) > 1:
            i += 1
            continue
        if re.fullmatch(r"[\d.]+[smhd]?", tok):
            i += 1                                       # timeout's duration
            continue
        break
    return i


def _command_index(tokens) -> int:
    """Index of the effective command word, or -1. Skips reserved words, assignments, wrappers."""
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in NOISE_WORDS or _ASSIGN_RE.fullmatch(tok):
            i += 1
            continue
        base = os.path.basename(tok)
        if base in WRAPPERS:
            i = _skip_wrapper_args(tokens, i + 1, base)
            continue
        return i
    return -1


def _strip_redirects(tokens):
    """Option tokens only: redirect operators and their destinations are not command options."""
    out = []
    skip = False
    for i, tok in enumerate(tokens):
        if skip:
            skip = False
            continue
        if tok in REDIR_STDOUT_OPS or tok in ("<", "<<", "<<<", "2>", "2>>"):
            skip = True
            continue
        if tok.isdigit() and i + 1 < len(tokens) and tokens[i + 1] in REDIR_STDOUT_OPS:
            continue                                     # the fd of `2> f` / `1> f`
        out.append(tok)
    return out


def _git_invocation(tokens, depth: int = 0):
    """(subcommand, arg_tokens, shell_alias_body), or (None, None, None) when this is not git.

    Resolves git's global options including `-c <key>=<value>`; a `-c alias.<name>=<body>` whose
    name matches the subcommand is EXPANDED, because `git -c alias.d=diff d` is a live bypass
    inside the very command grammar this hook claims to parse (review HIGH-2).
    """
    idx = _command_index(tokens)
    if idx < 0 or os.path.basename(tokens[idx]) not in ("git", "git.exe"):
        return None, None, None
    i = idx + 1
    config = {}
    while i < len(tokens):
        tok = tokens[i]
        if tok == "--":
            i += 1
            break
        if not tok.startswith("-"):
            break
        if tok in _GIT_OPTS_WITH_VALUE:
            if tok in ("-c", "--config-env") and i + 1 < len(tokens) and "=" in tokens[i + 1]:
                key, _, value = tokens[i + 1].partition("=")
                config[key] = value
            i += 2
            continue
        if tok.startswith("--") and "=" in tok:
            head, _, value = tok.partition("=")
            if head in _GIT_OPTS_WITH_VALUE:
                config[head] = value
            i += 1
            continue
        i += 1
    if i >= len(tokens):
        return None, None, None
    sub = tokens[i]
    args = tokens[i + 1:]
    alias = config.get("alias." + sub)
    if alias is not None and depth < _MAX_DEPTH:
        body = alias.strip()
        if body.startswith("!"):
            return None, None, (body[1:] + " " + " ".join(args)).strip()
        try:
            expanded = ["git"] + shlex.split(body) + args
        except ValueError:
            return None, None, None
        return _git_invocation(expanded, depth + 1)
    return sub, args, None


# --------------------------------------------------------------------------------------------
# Layer 3: will git emit a patch body (option ORDER, per git's grammar)
# --------------------------------------------------------------------------------------------

def _apply_short_cluster(tok: str, state: dict) -> bool:
    """Apply one clustered short-option token IN ORDER. True when it consumed the next token.

    git's grammar: `-pU1` is -p then -U1; `-sp` is -s then -p (patch WINS); `-ps` is the reverse; a
    value-taking letter swallows the REST of the cluster (`-U1p` is `--unified=1p`, an error).
    """
    body = tok[1:]
    j = 0
    while j < len(body):
        ch = body[j]
        if ch.isdigit():
            return False                                 # `-3` style count: the rest is a number
        if ch in ("p", "u"):
            state["patch"] = True
            state["format_set"] = True
        elif ch == "s":
            state["patch"] = False
            state["format_set"] = True
        elif ch == "c":
            state["patch"] = True                        # log/show -c implies -p (verified)
            state["format_set"] = True
        elif ch in _SHORT_VALUE_LETTERS:
            if ch == "U":
                state["patch"] = True
                state["format_set"] = True
            return j == len(body) - 1                    # value is the next token when none trails
        elif ch in ("M", "C", "B"):
            j += 1
            while j < len(body) and (body[j].isdigit() or body[j] == "%"):
                j += 1
            continue
        j += 1
    return False


def _git_prints_content(sub: str, args) -> bool:
    """True when this git invocation puts a +/- content body on stdout."""
    if sub == "format-patch":
        return "--stdout" in args
    if sub == "difftool":
        return not any(t in ("-h", "--help", "--tool-help") for t in args)
    if sub not in ALWAYS_CONTENT and sub not in CONTENT_IF_PATCH:
        return False
    state = {"patch": False, "format_set": False, "hard": False}
    skip = False
    for tok in args:
        if skip:
            skip = False
            continue
        if tok == "--":
            break                                        # pathspecs from here on
        if not tok.startswith("-") or tok == "-":
            continue
        head = tok.split("=", 1)[0]
        if head in HARD_SUPPRESS_LONG:
            state["hard"] = True
        elif head in NO_PATCH_LONG:
            state["patch"] = False
            state["format_set"] = True
        elif head in PATCH_LONG:
            state["patch"] = True
            state["format_set"] = True
        elif head in SUMMARY_LONG:
            state["format_set"] = True
        elif head in GIT_LONG_VALUE_OPTS and "=" not in tok:
            skip = True
        elif tok.startswith("--"):
            continue
        else:
            skip = _apply_short_cluster(tok, state)
    if state["hard"]:
        return False
    return state["patch"] or (not state["format_set"] and sub in ALWAYS_CONTENT)


def _git_output_file(args):
    """git's own stdout redirect: `--output=<f>` / `--output <f>`, or None."""
    for i, tok in enumerate(args):
        if tok.startswith("--output="):
            return tok.split("=", 1)[1]
        if tok == "--output" and i + 1 < len(args):
            return args[i + 1]
    return None


# --------------------------------------------------------------------------------------------
# Layer 4: does the body reach the console
# --------------------------------------------------------------------------------------------

def _target_is_quiet(kind: str, target: str) -> bool:
    """True when a redirect destination genuinely keeps the body off the maintainer's screen."""
    if kind == "dup":
        return target not in ("1", "2")                  # `>&1` / `>&2` relay; `>& file` does not
    if not target:
        return False
    if target.startswith(">(") or target.startswith("<("):
        return False                                     # process substitution relays
    if "$" in target or "`" in target or _SUBST_PLACEHOLDER in target:
        return not REQUIRE_LITERAL_REDIRECT_TARGET
    norm = target.rstrip("/")
    if norm in CONSOLE_TARGETS or _CONSOLE_FD_RE.match(norm):
        return False
    return True


def _stdout_is_quiet(tokens) -> bool:
    """True when this segment's stdout is redirected somewhere the maintainer cannot see.

    The LAST stdout redirect wins, matching the shell. `2>` and `2>&1` are stderr and never exempt,
    and `2>&1` must not steal the classification from an earlier `> file`.
    """
    found = None
    for i, tok in enumerate(tokens):
        if tok not in REDIR_STDOUT_OPS:
            continue
        prev = tokens[i - 1] if i else ""
        if prev.isdigit() and prev != "1":
            continue                                     # 2> / 3> / 2>&1 : not stdout
        target = tokens[i + 1] if i + 1 < len(tokens) else ""
        found = ("dup" if tok == ">&" else "file", target)
    if found is None:
        return False
    return ALLOW_FILE_REDIRECT and _target_is_quiet(found[0], found[1])


def _consumes_rather_than_relays(tokens) -> bool:
    """True when this pipeline stage prints a count or a digest rather than the body it received."""
    idx = _command_index(tokens)
    if idx < 0:
        return False
    base = os.path.basename(tokens[idx])
    if base in NON_RELAYING:
        return True
    if base in _GREP_COMMANDS:
        for tok in tokens[idx + 1:]:
            if tok in _GREP_QUIET_FLAGS:
                return True
            if re.fullmatch(r"-[a-zA-Z]*[cqlL][a-zA-Z]*", tok):
                return True
    return False


def _reaches_console(segments, index: int) -> bool:
    """Walk the pipeline downstream of segments[index] and decide whether the body hits the screen."""
    if _stdout_is_quiet(segments[index][0]):
        return False
    i = index
    while segments[i][1] in ("|", "|&") and i + 1 < len(segments):
        i += 1
        stage = segments[i][0]
        if _consumes_rather_than_relays(stage) or _stdout_is_quiet(stage):
            return False                                 # a count reaches the console, not a wall
    return True


# --------------------------------------------------------------------------------------------
# Layer 5: the decision
# --------------------------------------------------------------------------------------------

def _shell_body(tokens, idx: int):
    """The shell PROGRAM text this segment carries (`sh -c '...'`, `eval '...'`), else None."""
    base = os.path.basename(tokens[idx])
    if base == "eval":
        return " ".join(tokens[idx + 1:]) or None
    if base in SHELL_INTERPRETERS:
        for j in range(idx + 1, len(tokens)):
            tok = tokens[j]
            if re.fullmatch(r"-[a-zA-Z]*c", tok) and j + 1 < len(tokens):
                return tokens[j + 1]
            if tok.startswith("-c") and len(tok) > 2 and not tok.startswith("--"):
                return tok[2:]
    return None


def _segment_dumps_content(tokens, segments, index: int, depth: int):
    """The display string when this segment renders a content diff on the console, else None."""
    opts = _strip_redirects(tokens)
    idx = _command_index(opts)
    if idx < 0:
        return None

    body = _shell_body(opts, idx)
    if body is not None and depth < _MAX_DEPTH:
        return _scan_command(body, captured=not _reaches_console(segments, index), depth=depth + 1)

    base = os.path.basename(opts[idx])

    if base in ("git", "git.exe"):
        sub, args, alias_shell = _git_invocation(opts)
        if alias_shell and depth < _MAX_DEPTH:
            return _scan_command(alias_shell,
                                 captured=not _reaches_console(segments, index), depth=depth + 1)
        if sub is None or not _git_prints_content(sub, args):
            return None
        out_file = _git_output_file(args)
        if out_file is not None and ALLOW_FILE_REDIRECT and _target_is_quiet("file", out_file):
            return None
    elif COVER_NON_GIT_DIFF and base in DIFF_COMMANDS:
        if any(t in DIFF_QUIET_FLAGS for t in opts[idx + 1:]):
            return None
    elif COVER_PATCH_FILE_DUMP and base in DUMP_COMMANDS:
        if not any(t.endswith(PATCH_SUFFIXES) for t in opts[idx + 1:]):
            return None
    else:
        return None

    if not _reaches_console(segments, index):
        return None
    # The internal substitution placeholder must never surface in the maintainer-facing message.
    return " ".join(tokens).replace(_SUBST_PLACEHOLDER, "...")


def _scan_command(text: str, captured: bool = False, depth: int = 0):
    """The first console-reaching content dump in this shell text, as a display string, or None."""
    if depth > _MAX_DEPTH or not isinstance(text, str) or not text.strip():
        return None
    outer, subs = _split_substitutions(strip_heredocs(text))
    if not captured:
        segments = _segments(outer)
        for index in range(len(segments)):
            try:
                hit = _segment_dumps_content(segments[index][0], segments, index, depth)
            except Exception:
                continue
            if hit:
                return hit
    for inner, inner_captured in subs:
        hit = _scan_command(inner, captured or inner_captured, depth + 1)
        if hit:
            return hit
    return None


def offending_segment(command: str):
    """The first console-reaching content-dumping segment (display string), or None. Never raises."""
    if not isinstance(command, str) or not command.strip():
        return None
    try:
        return _scan_command(command)
    except Exception:
        return None                                      # fail-open on parse ambiguity


# --------------------------------------------------------------------------------------------
# Message, register, protocol
# --------------------------------------------------------------------------------------------

def log_fire(event: str, detail: str) -> bool:
    """Append one row to the shared fire register. True on a written row, False on any failure.

    Row: <utc-iso-Z> TAB <event> TAB <hook> TAB <detail>, the four-column shape already used by the
    shipped self-QA hook. The CALLER ignores the result: a logging failure must never cost a block.
    """
    try:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row = "\t".join([stamp, event, "block-git-diff-content-dump",
                         " ".join(str(detail).split())]) + "\n"
        with FIRE_LOG.open("a", encoding="utf-8") as fh:
            fh.write(row)
        return True
    except Exception:
        return False


def _message(segment: str, blocking=None) -> str:
    if blocking is None:
        blocking = BLOCK_SEVERITY
    head = "BLOCKED" if blocking else "WARNING"
    tail = ("The call has been refused."
            if blocking else "This is a WARNING and the call proceeds; do not send the next one.")
    return (
        head + " (console diff-wall guardrail): this command puts a +/- unified diff of file "
        "content on the console.\n"
        "  offending segment: " + segment[:160] + "\n"
        "\n"
        "WHY: the maintainer's hard rule (2026-07-26, restated after repeated violations) is that "
        "no command's console output may be a content diff. The console is their live window onto "
        "the run, and a wall of add/remove lines scrolls the signal they actually need off the "
        "screen; it has hidden a real issue more than once. " + tail + "\n"
        "\n"
        "CONSIDER-INSTEAD:\n"
        "    git diff --stat                  # file names + churn counts, no content\n"
        "    git diff --name-only             # file names only\n"
        "    git status --short               # the staged-vs-working check\n"
        "    sed -n '<a>,<b>p' <file>         # or a targeted Read of the specific lines\n"
        "    grep -n <pat> <file> | cut -c1-120\n"
        "    git diff | wc -l                 # measure it without printing it\n"
        "    git diff > /tmp/<id>.diff        # capture it quietly, then read it BOUNDED\n"
        "\n"
        "  If you are confirming an edit you just made: the Edit tool already showed what changed, "
        "so re-diffing it is redundant as well as refused."
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload.get("tool_input", {}).get("command", "")
    except Exception:
        return 0                                         # fail-open on a malformed payload
    try:
        segment = offending_segment(command)
    except Exception:
        return 0                                         # fail-open on anything unexpected
    if segment is None:
        return 0
    if not SELF_TEST_MODE:
        try:
            from _hook_state import record_block
            record_block(command, "git-diff-content-dump")
        except Exception:
            pass
    log_fire("BLOCK" if BLOCK_SEVERITY else "WARN-ALLOWED", "segment=" + segment[:160])
    sys.stderr.write(_message(segment) + "\n")
    return 2 if BLOCK_SEVERITY else 0


# --------------------------------------------------------------------------------------------
# Fixtures. Every adversarial example from the seed deep review is present and tagged.
# --------------------------------------------------------------------------------------------

BLOCKED_CASES = [
    # --- seed baseline ------------------------------------------------------------------------
    "git diff",
    "git diff HEAD~1",
    "git diff main..feature",
    "git diff -- tools/",
    "git show HEAD",
    "git show a9aaf8b3",
    "git show HEAD:tools/exec-dispatch.py",
    "git log -p",
    "git log -p -3 tools/",
    "git log --patch",
    "git log -U5",
    "git log --unified=3",
    "git range-diff main...topic",
    "git diff-tree -p HEAD",
    "git diff-index -p HEAD",
    "git -C /home/grc/grc_library diff",
    "git -c color.ui=false diff",
    "git --no-pager diff",
    "sudo git diff",
    "cd /home/grc/grc_library && git diff",
    "git status --short; git diff",
    "git diff | head -50",
    "git diff | tail -20",
    "echo start; git show HEAD; echo done",
    "(cd /repo && git show HEAD)",
    "git diff --stat\ngit diff",
    "git diff 2> /tmp/err.log",
    "GIT_PAGER=cat git diff",
    "git diff --pretty=full",
    "git show --oneline HEAD",
    "git stash show -p",
    # --- review HIGH-1: a summary flag must NOT beat an explicit patch flag ---------------------
    "git diff --stat -p",
    "git diff -p --stat",
    "git log --stat -p",
    "git show -s -p HEAD",
    "git diff --no-patch --patch",
    "git show --no-patch --patch HEAD",
    "git diff --numstat -p",
    "git diff --raw -p",
    "git diff --summary -p",
    "git diff --compact-summary -p",
    "git diff --shortstat -p",
    "git diff --dirstat -p",
    "git log -1 --patch-with-stat",
    "git log -c -1",
    "git log --cc -1",
    # --- review HIGH-2: grammar and indirection --------------------------------------------------
    "{ git diff; }",
    "if true; then git diff; fi",
    "! git diff",
    "echo `git diff`",
    "sh -c 'git diff'",
    "bash -lc 'git diff'",
    "env -u FOO git diff",
    "env FOO=1 git diff",
    "git -c alias.d=diff d",
    "git -c alias.d='diff --stat -p' d",
    "git -c alias.sh='!git diff' sh",
    "eval 'git diff'",
    "timeout -k 5 30 git diff",
    "sudo -u root git diff",
    "while git diff; do :; done",
    "for f in a b; do git diff; done",
    "cat <(git diff)",
    'echo "$(git diff)"',
    "echo $(git show HEAD)",
    # --- review HIGH-3: a console-facing redirect is not a quiet redirect ------------------------
    "git diff > /dev/tty",
    "git diff > /dev/stderr",
    "git diff > /dev/stdout",
    "git diff > /proc/self/fd/1",
    "git diff > /dev/fd/2",
    "git diff > /dev/pts/3",
    "git diff > >(cat)",
    "git diff >&1",
    'git diff > "$OUT"',
    # --- review MED-4: clustered short options ----------------------------------------------------
    "git log -pU1",
    "git diff -sp",
    "git log -1 -sp",
    "git log -pM90",
    # --- review MED-6: the rest of the CLAUDE.md:868 command set ------------------------------------
    "diff -u a.txt b.txt",
    "diff -r old/ new/",
    "colordiff a.txt b.txt",
    "git difftool",
    "git format-patch -1 --stdout",
    "cat /tmp/x.patch",
    "less /tmp/change.diff",
    "git diff > /tmp/d.diff && cat /tmp/d.diff",
    # --- pipelines that still relay ------------------------------------------------------------------
    "git diff | cat",
    "git diff | tee /tmp/d.diff",
    "git diff | grep '^+'",
    "git diff | wc -l | cat; git show HEAD",
    # --- heredocs must not become a bypass. Each of these is a way the strip could go wrong. -------
    "bash <<'EOF'\ngit diff\nEOF",                             # interpreter body IS a program
    "sh <<'EOF'\ngit diff\nEOF",
    "sudo bash <<'EOF'\ngit diff\nEOF",                        # wrapper before the interpreter
    "cat <<EOF\n$(git diff)\nEOF",                             # unquoted tag: the subst RUNS
    "cat > /tmp/note.md <<EOF\n$(git diff)\nEOF",              # deliberately conservative, see RESIDUE
    "cat > /tmp/note.md <<'EOF'\nnothing here\nEOF\ngit diff",  # text AFTER the body still scanned
    "cat > /tmp/note.md <<'NOEND'\ngit diff",                  # no terminator: strip NOTHING
    "grep 'x' <<< 'data'\ngit diff",                           # `<<<` is a herestring, not a heredoc
    "cat > /tmp/note.md <<'EOF'\nnotes\nEOF\ncat /tmp/x.patch",  # non-git dumper after a body
]

ALLOWED_CASES = [
    # --- seed baseline ------------------------------------------------------------------------
    "git diff --stat",
    "git diff --stat=200",
    "git diff --numstat",
    "git diff --raw",
    "git log --oneline --graph -10",
    "git diff --shortstat",
    "git diff --name-only",
    "git diff --name-status",
    "git diff --compact-summary",
    "git show --stat HEAD",
    "git show -s --format=%H HEAD",
    "git show --name-only HEAD",
    "git log --oneline -5",
    "git log --oneline | head -5",
    "git log --stat -3",
    "git log",
    "git status",
    "git status --short",
    "git diff-tree --stat HEAD",
    "git diff-tree HEAD",
    "git -C /home/grc/grc_library diff --name-only",
    "git add -A && git commit -m 'x'",
    "git format-patch -1",
    "git blame tools/exec-dispatch.py | head -5",
    "python3 /home/grc/grc_library/tools/run_all_audits.py",
    "grep -rn 'git diff' .claude/CLAUDE.md | cut -c1-120",
    "git commit -m 'never run git diff without --stat'",
    'echo "git diff is forbidden"',
    'git commit -m "fix (git diff) wall"',
    # --- heredoc bodies are DATA: the body is written to a file, it is not a command run ---------
    "cat > /tmp/note.md <<'EOF'\ngit diff\nEOF",
    "cat > /tmp/note.md <<'EOF'\ngit diff --stat is fine, bare git diff is not\nEOF",
    "cat > /tmp/note.md <<-'EOF'\n\tgit diff\n\tEOF",          # tab-stripping form
    'cat > /tmp/note.md <<"EOF"\ngit diff\nEOF',               # double-quoted tag, also inert
    "tee /tmp/note.md <<'EOF'\ngit show HEAD\nEOF",
    "cat > /tmp/note.md <<'EOF'\n$(git diff)\nEOF",            # quoted tag: the subst is LITERAL
    "cat > /tmp/note.md <<EOF\nsee the notes above\nEOF",      # unquoted body kept, nothing in it
    "python3 <<'EOF'\nprint('git diff')\nEOF",                 # non-shell body: stated RESIDUE
    "git diff > /tmp/d.diff",
    "git diff >> /tmp/d.diff",
    "git show HEAD 1> /tmp/d.diff",
    "git diff --name-only\ngit diff --stat",
    "ls -la",
    # --- review HIGH-1 counterparts: order-sensitive suppression really suppresses ---------------
    "git diff --patch --no-patch",
    "git diff -ps",
    "git log -1 -ps",
    "git diff --name-only -p",
    "git diff --name-status -p",
    "git diff --check -p",
    "git diff --quiet -p",
    "git log --full-diff",
    # --- review HIGH-3: the quiet redirect spellings the seed false-blocked -----------------------
    "git diff &> /tmp/d.diff",
    "git diff &>> /tmp/d.diff",
    "git diff >| /tmp/d.diff",
    "git diff > /dev/null",
    "git diff > /tmp/d.diff 2>&1",
    "git diff --output=/tmp/d.diff",
    "git diff --output /tmp/d.diff",
    # --- review MED-5: false blocks the seed produced ----------------------------------------------
    "git diff --quiet",
    "git diff --check",
    "git diff | wc -l",
    "git diff | wc",
    "git diff | md5sum",
    "git diff | sha256sum",
    "git diff | grep -c '^+'",
    "git diff | grep -q 'TODO'",
    "git diff | head -50 | wc -l",
    "x=$(git diff)",
    "COUNT=$(git diff | wc -l)",
    'if [ -n "$(git diff)" ]; then echo dirty; fi',
    # --- review MED-6 counterparts: the bounded readers stay allowed --------------------------------
    "diff -q a.txt b.txt",
    "diff --brief old/ new/",
    "head -20 /tmp/x.patch",
    "tail -5 /tmp/x.patch",
    "sed -n '1,40p' /tmp/x.patch",
    "grep -n '^+++' /tmp/x.patch | cut -c1-120",
    "git difftool --help",
    "patch -p1 < /tmp/x.patch",
    # --- STATED RESIDUE, asserted so the gap is visible rather than claimed away --------------------
    "python3 -c 'import os; os.system(\"git diff\")'",
    "G=git; $G diff",
]

# Malformed shell. The contract is FAIL-OPEN: allow, exit 0, never raise.
FAIL_OPEN_CASES = [
    "git diff 'unbalanced",
    'git show "open',
    "git diff $((1+",
    "git diff `open",
    "git diff $(",
    "git diff <(",
    "git diff --unmatched-quote'",
]


def _run_main(command: str):
    """(exit_code, stderr, stdout) from an ACTUAL main() call.

    The review asked for protocol assertions, not only `offending_segment()` unit calls.
    """
    import io
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    saved = (sys.stdin, sys.stdout, sys.stderr)
    sys.stdin, sys.stdout, sys.stderr = io.StringIO(payload), io.StringIO(), io.StringIO()
    try:
        code = main()
        return code, sys.stderr.getvalue(), sys.stdout.getvalue()
    finally:
        sys.stdin, sys.stdout, sys.stderr = saved


def self_test() -> int:
    import tempfile
    global SELF_TEST_MODE, FIRE_LOG, ALLOW_FILE_REDIRECT, BLOCK_SEVERITY, \
        REQUIRE_LITERAL_REDIRECT_TARGET, COVER_NON_GIT_DIFF, COVER_PATCH_FILE_DUMP
    SELF_TEST_MODE = True
    saved_log = FIRE_LOG
    root = Path(tempfile.mkdtemp())
    FIRE_LOG = root / "guard-fires.tsv"
    bad = 0
    protocol = 0
    extra = 0

    for cmd in BLOCKED_CASES:
        if offending_segment(cmd) is None:
            bad += 1
            print("FAIL should BLOCK: " + repr(cmd))
            continue
        code, err, out = _run_main(cmd)                  # end-to-end protocol assertion
        protocol += 1
        if code != 2 or not err.strip() or out:
            bad += 1
            print("FAIL protocol on BLOCK %r: exit=%d stderr=%d stdout=%d"
                  % (cmd, code, len(err), len(out)))

    for cmd in ALLOWED_CASES:
        seg = offending_segment(cmd)
        if seg is not None:
            bad += 1
            print("FAIL should ALLOW: " + repr(cmd) + "  (segment: " + seg + ")")
            continue
        code, err, out = _run_main(cmd)
        protocol += 1
        if code != 0 or err or out:
            bad += 1
            print("FAIL protocol on ALLOW %r: exit=%d stderr=%r" % (cmd, code, err[:80]))

    # Fail-open contract: a tokenizer failure must ALLOW, exit 0, and never raise.
    for broken in FAIL_OPEN_CASES:
        extra += 1
        try:
            if offending_segment(broken) is not None:
                bad += 1
                print("FAIL: malformed input must fail OPEN: " + repr(broken))
        except Exception as exc:
            bad += 1
            print("FAIL: did not fail open on " + repr(broken) + ": " + repr(exc))
        if _run_main(broken)[0] != 0:
            bad += 1
            print("FAIL: malformed input must exit 0: " + repr(broken))
        protocol += 1

    # A malformed PAYLOAD must also fail open.
    extra += 1
    import io
    saved = (sys.stdin, sys.stdout, sys.stderr)
    sys.stdin, sys.stdout, sys.stderr = io.StringIO("not json"), io.StringIO(), io.StringIO()
    try:
        if main() != 0:
            bad += 1
            print("FAIL: a malformed payload must exit 0")
    finally:
        sys.stdin, sys.stdout, sys.stderr = saved

    # The message must carry the three headers and name the sanctioned alternatives: a block that
    # does not say what to do instead is the shape that gets retried verbatim.
    msg = _message("git diff", blocking=True)
    for needle in ("BLOCKED", "WHY:", "CONSIDER-INSTEAD:", "--stat", "--name-only",
                   "git status --short", "sed -n", "| wc -l"):
        extra += 1
        if needle not in msg:
            bad += 1
            print("FAIL: block message omits " + needle)
    extra += 2
    if "BLOCKED" in _message("git diff", blocking=False):
        bad += 1
        print("FAIL: WARN mode must never say BLOCKED")
    if "WARNING" not in _message("git diff", blocking=False):
        bad += 1
        print("FAIL: WARN mode must say WARNING")

    # Every judgement-call constant is asserted on BOTH of its settings.
    extra += 4
    ALLOW_FILE_REDIRECT = False
    if offending_segment("git diff > /tmp/d.diff") is None:
        bad += 1
        print("FAIL: ALLOW_FILE_REDIRECT=False must block a redirected diff")
    ALLOW_FILE_REDIRECT = True

    REQUIRE_LITERAL_REDIRECT_TARGET = False
    if offending_segment('git diff > "$OUT"') is not None:
        bad += 1
        print("FAIL: REQUIRE_LITERAL_REDIRECT_TARGET=False must allow an expanded destination")
    REQUIRE_LITERAL_REDIRECT_TARGET = True

    COVER_NON_GIT_DIFF = False
    if offending_segment("diff -u a.txt b.txt") is not None:
        bad += 1
        print("FAIL: COVER_NON_GIT_DIFF=False must allow non-git diff")
    COVER_NON_GIT_DIFF = True

    COVER_PATCH_FILE_DUMP = False
    if offending_segment("cat /tmp/x.patch") is not None:
        bad += 1
        print("FAIL: COVER_PATCH_FILE_DUMP=False must allow a patch-file dump")
    COVER_PATCH_FILE_DUMP = True

    extra += 1
    BLOCK_SEVERITY = False
    code, err, _out = _run_main("git diff")
    if code != 0 or "WARNING" not in err or "BLOCKED" in err:
        bad += 1
        print("FAIL: BLOCK_SEVERITY=False must exit 0 with a WARNING on stderr")
    BLOCK_SEVERITY = True

    # The register must accept a row, and must never cost a block when it cannot.
    extra += 3
    if not log_fire("BLOCK", "detail  with   spaces\nand a newline"):
        bad += 1
        print("FAIL: log_fire could not write the register")
    else:
        row = FIRE_LOG.read_text(encoding="utf-8").strip().split("\n")[-1]
        if len(row.split("\t")) != 4 or "block-git-diff-content-dump" not in row:
            bad += 1
            print("FAIL: register row is not the four-column shared format")
    FIRE_LOG = root / "no-such-dir" / "guard-fires.tsv"
    if log_fire("BLOCK", "x"):
        bad += 1
        print("FAIL: log_fire must report False when it cannot write")
    if _run_main("git diff")[0] != 2:
        bad += 1
        print("FAIL: a register failure must never cost a block")

    # The internal placeholder must never reach the maintainer-facing message.
    extra += 1
    if _SUBST_PLACEHOLDER in (offending_segment("git diff > >(cat)") or ""):
        bad += 1
        print("FAIL: the substitution placeholder leaked into the reported segment")

    # The heredoc layer, asserted directly rather than only through the command fixtures. Each row
    # is (command, does PAYLOAD survive the strip). A body that survives is scanned as a program.
    heredoc_cases = [
        ("cat > f <<'EOF'\nPAYLOAD\nEOF",        False),  # quoted tag: inert DATA
        ('cat > f <<"EOF"\nPAYLOAD\nEOF',        False),
        ("cat > f <<-'EOF'\n\tPAYLOAD\n\tEOF",   False),  # tab-stripping form
        ("cat > f <<EOF\nPAYLOAD\nEOF",          True),   # unquoted tag EXPANDS the body
        ("bash <<'EOF'\nPAYLOAD\nEOF",           True),   # interpreter body is a PROGRAM
        ("sh <<'EOF'\nPAYLOAD\nEOF",             True),
        ("ssh host <<'EOF'\nPAYLOAD\nEOF",       True),
        ("sudo sh <<'EOF'\nPAYLOAD\nEOF",        True),
        ("python3 <<'EOF'\nPAYLOAD\nEOF",        False),  # not shell: category error, see RESIDUE
        ("cat > f <<'NOEND'\nPAYLOAD\n",         True),   # no terminator: strip NOTHING
        ("echo a <<< 'PAYLOAD'",                 True),   # herestring, not a heredoc
        ("echo a << b\nPAYLOAD",                 True),   # `<<` with no shell-word tag
    ]
    for impl_name, impl in (("effective", strip_heredocs), ("in-file", _strip_heredocs_local)):
        for command, must_survive in heredoc_cases:
            extra += 1
            if ("PAYLOAD" in impl(command)) != must_survive:
                bad += 1
                print("FAIL heredoc (%s impl): %r want survive=%s"
                      % (impl_name, command, must_survive))
        # Text after a stripped body must survive: swallowing it is a universal bypass.
        extra += 1
        if "AFTERWARDS" not in impl("cat > f <<'EOF'\nPAYLOAD\nEOF\nAFTERWARDS"):
            bad += 1
            print("FAIL heredoc (%s impl): text after a stripped body did not survive" % impl_name)

    # PARITY. The in-file copy exists so this hook is standalone; it must not drift from the shared
    # module when that module is the one actually in use.
    extra += 1
    if _HEREDOC_IMPL == "_hookutil":
        drift = [c for c, _ in heredoc_cases if strip_heredocs(c) != _strip_heredocs_local(c)]
        if drift:
            bad += 1
            print("FAIL: in-file strip_heredocs has drifted from _hookutil on " + repr(drift))

    FIRE_LOG = saved_log
    SELF_TEST_MODE = False

    print("hook self-test %s (%d block cases, %d allow cases, %d fail-open + contract checks, "
          "%d main() protocol assertions, %d bad)"
          % ("OK" if not bad else "FAILED", len(BLOCKED_CASES), len(ALLOWED_CASES), extra,
             protocol, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(self_test())
    sys.exit(main())
