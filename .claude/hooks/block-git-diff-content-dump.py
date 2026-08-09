#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse a command that puts a +/- unified diff of file CONTENT on the CONSOLE.

PR1b ACTIVATION CANDIDATE, hardened 2026-08-09 against the seed deep review
(`inbox/deliveries/seed-review-pr1b-codex.md`), then REVISED 2026-08-09 against the dual-family
validation of commit 22df0be2 (`inbox/deliveries/vpr-1472-codex.md` findings 1-6,
`inbox/deliveries/vpr-1472-claude.md` F1/F2/F4/F5). What that revision changed, each with a fixture:

    FALSE BLOCKS removed (the hook was refusing a SAFE command)
      * a heredoc BODY is DATA whether or not its tag is quoted. Only the LIVE EXPANSIONS of an
        unquoted body are commands; its literal text is not.        -> `_live_expansions`
      * `> >(wc -l)`: a process-substitution CONSUMER is classified with the same relay-vs-consume
        test already used for a pipeline stage.                     -> `_procsub_consumer_is_quiet`
      * a construct that legitimately SPANS a newline (a multi-line quoted string, a backslash
        line continuation) no longer defeats the tokenizer, and a tokenizer failure now fails open
        for THAT LINE only rather than for the whole command.       -> `_join_continuations`,
                                                                       `_logical_lines`, `_segments`
    EVASIONS closed (the hook was allowing a real console wall)
      * `--binary` and `--remerge-diff` are patch-enabling, and `--quiet` does NOT suppress a
        patch for `log` / `show`.                                   -> `_git_prints_content`
      * console paths spelled with redundant separators (`/dev//tty`, `/dev/./stderr`,
        `//dev/stdout`, `/proc/self//fd/1`) are normalised before the console test, and the
        numbered virtual consoles are console targets.  -> `_normalise_path`, `_CONSOLE_FD_RE`
      * a reserved word or an ordinary English word in the prefix no longer masquerades as a
        capturing context: the CONSUMER decides.                    -> `_is_capturing_context`
      * a redirect to an already-open descriptor (`1>&3`) or a csh-style `>& word` is classified
        as CONSOLE, not quiet.                                      -> `_target_is_quiet`

Wiring: install as
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
                       --patch-with-raw, --cc, --binary, and post-subcommand -c) -> patch ON
      * a WEAK patch flag (--remerge-diff)                              -> patch on ONLY if nothing
                        else sets the format (verified: --stat, --no-patch, --name-only, --check
                        and --quiet all beat it, in EITHER order)
      * a SUMMARY flag (--stat, --numstat, --shortstat, --dirstat, --summary,
                        --compact-summary, --raw)                       -> format SET, patch UNCHANGED
      * -s / --no-patch                                                 -> format SET, patch OFF
      * --name-only, --name-status, --check                             -> HARD suppress, order-free
      * --quiet -> HARD suppress for the diff-* family; for `log` / `show` it only SETS the format
                   (it clears a default or weak patch and NOT an explicit one)
    content = (not hard_suppress) and (explicit_patch or weak_patch_with_no_other_format or
                                       (format never set and the subcommand prints a patch by
                                        default))

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
      git diff --quiet -p              ->   0 content rows   (diff-* family: --quiet IS hard)
      git log --full-diff              ->   0 content rows   (the seed listed it as a PATCH flag;
                                                              it only WIDENS an existing patch, and
                                                              the seed therefore false-blocked it)

    Re-measured 2026-08-09 on git 2.53.0 for the vpr-1472 revision, counted the same way:
      git log --binary -1              -> 2380 content rows  (codex#1: --binary implies --patch)
      git log --no-patch --binary      -> 2380 content rows  (it is order-sensitive like -p)
      git log --binary --no-patch      ->    0 content rows
      git log --remerge-diff -1        -> 2380 content rows  (weak: --stat / --no-patch / --quiet /
      git log --quiet --remerge-diff   ->    0 content rows   --name-only beat it in EITHER order)
      git log  --quiet -p              -> 2380 content rows  (found while verifying codex#1: the
      git show --quiet -p HEAD         -> 2380 content rows   22df0be2 model called these 0 and
                                                              therefore ALLOWED a real wall)
      git diff --quiet --binary        ->    0 content rows  (the diff-* family is unaffected)
      git show --quiet HEAD            ->    0 content rows  (it does clear the DEFAULT patch)

CONSOLE REACHABILITY (question 3). A content body is only a violation if the maintainer sees it:
  * stdout redirected to a QUIET destination            -> allowed (see ALLOW_FILE_REDIRECT)
  * stdout redirected to a CONSOLE-FACING destination   -> BLOCKED. /dev/tty, /dev/console,
    /dev/stdout, /dev/stderr, /dev/fd/1|2, /proc/<pid|self>/fd/1|2, /dev/pts/<n>, /dev/tty<n>,
    /dev/ttyS<n>, `>&1`, `>&2` and process substitution `> >(cat)` all relay to the screen. The
    seed treated every `>` as safe. A device path is NORMALISED first, so `/dev//tty`,
    `/dev/./stderr`, `//dev/stdout` and `/proc/self//fd/1` are the same target as their plain
    spelling (codex#2); an ordinary output path normalises too and stays quiet.
  * a redirect to an ALREADY-OPEN descriptor (`1>&3`, `>&4`) is CONSOLE, not quiet: within one
    segment the hook cannot prove where fd 3 points, and `3>&1 1>&3` is the standard way to spell
    "back to stdout" (codex#4). `>& word` with a non-numeric word is the csh form that sends BOTH
    streams to that word, so it is classified as a PATH, which makes `>& /dev/tty` a block and
    `>& /tmp/d.diff` an allow (claude F2).
  * quiet redirect spellings `&>`, `&>>`, `>|`, `1>` are recognised; `2>` is stderr and does not
    exempt; `2>&1` does not steal the classification from an earlier `> file`; `--output=<file>` is
    a git-native redirect and is classified the same way.
  * a pipeline whose downstream stage CONSUMES rather than relays (`| wc -l`, `| grep -c`,
    `| md5sum`, `| sha256sum`) puts a COUNT on the console, not a wall -> allowed.
    `| head`, `| tail`, `| cat`, `| less`, `| tee`, `| grep <pat>` RELAY -> still blocked.
    The SAME test decides a process-substitution consumer: `> >(wc -l)` is a count and is allowed,
    `> >(cat)` relays and is blocked (codex#6).
  * a command substitution captured by an ASSIGNMENT or a test (`x=$(git diff)`,
    `if [ -n "$(git diff)" ]`) prints nothing -> allowed. A substitution whose value flows into a
    printing command (`echo $(git diff)`, ``echo `git diff` ``) -> BLOCKED. The decision reads the
    CONSUMER word, not any word in the prefix: `if` and `while` are transparent, so
    `if echo "$(git diff)"` is a BLOCK (codex#3), and prose is transparent too, so
    `echo "exit code: $(git diff)"` is a BLOCK rather than an allow (claude F4).

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
    heredoc bodies (`<<EOF`, `<<'EOF'`, `<<-EOF`), resolved DATA-vs-PROGRAM before segmentation;
    a backslash line continuation, and a quoted string that spans a newline.

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
    discovered. NOTE the 2026-08-09 narrowing: this residue is now the LIVE EXPANSION only. The
    literal TEXT of an unquoted body is data like any other body text, so
    `cat > note.md <<EOF / git diff / EOF` is ALLOWED, where 22df0be2 refused it (codex#5,
    claude F5).
  * CAPTURE-THEN-PRINT. `x=$(git diff)` is allowed by design and the block message actively
    recommends capturing, so `x=$(git diff); echo "$x"` is the obvious next move and it is NOT
    blocked: the wall reaches the console through a variable the hook does not track. Stated here
    because it was found and left, not because it was missed (claude F6).
  * `ssh host git diff`. The remote emits the wall onto this console, but ssh's option grammar plus
    a remote command is a second parser; out of scope by choice.
  * git reached through a variable (`G=git; $G diff`), `eval` of a string built at runtime, or any
    base64 / printf-constructed command.
  * `cat` of a diff previously redirected to a file with a NON-patch suffix
    (`git diff > /tmp/d.txt; cat /tmp/d.txt`). The `.diff` / `.patch` suffix case IS covered, see
    COVER_PATCH_FILE_DUMP.
  * a tokenizer failure FAILS OPEN (see the exit protocol), and that is now a PER-LINE fail-open:
    a line the tokenizer cannot read is skipped, the other lines of the command are still scanned.
    ACCEPTED MISS, and the accepted part is bounded. The two ordinary spellings claude F1 named are
    now PARSED, not skipped -- a backslash line continuation is joined the way the shell joins it
    (`_join_continuations`) and a quoted string that spans a newline is regrouped into one logical
    line (`_logical_lines`) -- each with a block fixture. What remains is text that is unbalanced
    from the hook's point of view no matter how the lines are grouped: an exotic shell grammar the
    tokenizer does not model (`$'...'` with an embedded quote, a `case` pattern list, an unbalanced
    quote closed by a later construct the lexer does not know). Those are UNBOUNDED, and the
    maintainer decision of 2026-08-09 is to accept them: this hook is a backstop for a chat-hygiene
    rule, not an airtight sandbox, and failing OPEN on an exotic construct costs a MISS, never a
    false block. Seven fail-open fixtures assert the direction, and the two F1 spellings are
    asserted as BLOCKS so the fix cannot silently regress into the fail-open path.

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
  1. CORRECTED 2026-08-09 (claude F7). The 22df0be2 text asserted that `.claude/CLAUDE.md:796`
     recommends a bare `git diff` read-back. It does not: at 22df0be2 that line is the
     "intent is not action" bullet, and the file's only `git diff` is the RULE itself at :868.
     There is no collision inside `.claude/CLAUDE.md`; a MUST-RESOLVE item pointing at the wrong
     line gets closed as resolved without anything being checked, so it is withdrawn rather than
     re-aimed. Items 2 and 3 stand.
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
import posixpath
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


def _live_expansions(body: str):
    """The `$( ... )` / backtick fragments of a heredoc DATA body, in order, as separate lines.

    THE FALSE BLOCK THIS FIXES (vpr-1472 codex#5, claude F5). A heredoc body is TEXT being written
    somewhere, and the 22df0be2 rule "an unquoted body is KEPT and scanned as a program" therefore
    refused

        cat > note.md <<EOF
        git diff is forbidden here
        EOF

    which prints nothing and runs nothing. The reason the body was kept is still true and is still
    honoured: an UNQUOTED tag really does expand a substitution written inside the body, so
    `<<EOF` containing `$(git diff)` really does run the diff. Only the EXPANSIONS are commands.
    Keeping just those keeps the live case blocked and lets the literal case through.

    The fragment is returned WHOLE, `$( ... )` markers included, so the ordinary substitution layer
    re-parses it with its own quote-aware matcher rather than a second, divergent one. A fragment
    the matcher cannot close is dropped: unclosable text is not a provable command, and the
    fail-open direction is the one this hook takes everywhere else.
    """
    out = []
    i, n = 0, len(body)
    while i < n:
        ch = body[i]
        if ch == "\\" and i + 1 < n:
            i += 2                                       # `\$(...)` is literal even unquoted
            continue
        if body.startswith("$((", i):
            end = _match_paren(body, i + 1)              # arithmetic: not a command
            i = end + 2 if end >= 0 else n
            continue
        if body.startswith("$(", i):
            end = _match_paren(body, i + 1)
            if end < 0:
                break
            out.append(body[i:end + 1])
            i = end + 1
            continue
        if ch == "`":
            end = _match_backtick(body, i + 1)
            if end < 0:
                break
            out.append(body[i:end + 1])
            i = end + 1
            continue
        i += 1
    return out


def _strip_heredocs_local(command: str) -> str:
    """Remove heredoc BODIES that are DATA; keep bodies that are PROGRAMS.

    Three properties, each of which a naive strip gets wrong and each of which has a fixture:

    1. A body introduced by an interpreter or a remote shell, or PIPED into one, IS EXECUTED.
       `bash <<'EOF' / git diff / EOF` really runs the diff, so stripping it would be a live
       WEAKENING, not a theoretical one. Those bodies are KEPT WHOLE and scanned.
    2. An UNQUOTED tag EXPANDS the body, so `<<EOF` containing `$(git diff)` really runs the
       substitution. Only a quoted tag (`<<'EOF'`, `<<"EOF"`) is inert. The EXPANSIONS of an
       unquoted body are therefore kept; its literal TEXT is data like any other body text and is
       dropped, which is what removes the vpr-1472 codex#5 / claude F5 false block.
    3. A false introducer with NO matching terminator must remove NOTHING. Swallowing the
       remainder of the command would be a universal bypass for every check downstream.

    A NON-shell interpreter body (`python3 <<'EOF'`) is stripped rather than scanned: shell text
    inside a python program is not a shell command, and scanning it produced a real false catch.
    That is the documented `_hookutil.NON_SHELL_INTERPRETERS` position and it is RESIDUE, stated
    in the module docstring rather than claimed away.

    Property 2 is NARROWER here than in `_hookutil`, deliberately: an unquoted body keeps only its
    LIVE EXPANSIONS, not its literal text. See `_live_expansions` and DIVERGENCE below.
    """
    lines = command.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        # The body is a PROGRAM when ANY stage of this line is an interpreter, not only the first
        # word: `cat <<EOF | bash` feeds the body to a shell just as surely as `bash <<EOF` does.
        # 22df0be2 read the first word only, so the piped form was already stripped for a quoted
        # tag; narrowing the unquoted case without this would have widened that miss instead of
        # leaving it where it was.
        stage_words = {_fallback_command_word(part)
                       for part in re.split(r"\|\|?|&&|;", line)}
        body_is_program = bool(stage_words & _HEREDOC_BODY_IS_SHELL)
        for quote, tag in _HEREDOC_RE.findall(line):
            end = None
            for j in range(i, len(lines)):
                if lines[j].strip() == tag:              # `<<-` may indent its terminator
                    end = j
                    break
            if end is None:
                continue                                 # property 3: remove NOTHING
            body = lines[i:end]
            i = end + 1
            if body_is_program:
                out.extend(body + [lines[end]])          # property 1: a PROGRAM, keep and scan
            elif not quote:
                out.extend(_live_expansions("\n".join(body)))   # property 2: expansions only
            # a QUOTED tag on a non-interpreter is inert DATA: drop the body and the terminator
    return "\n".join(out)


try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _hookutil import WRAPPERS
    from _hookutil import strip_heredocs as _shared_strip_heredocs
    _HEREDOC_IMPL = "_hookutil-present"
except Exception:                                        # pragma: no cover - standalone fallback
    WRAPPERS = set(_FALLBACK_WRAPPERS)
    _shared_strip_heredocs = None
    _HEREDOC_IMPL = "standalone"

# DIVERGENCE, deliberate and asserted rather than drift. The shared module keeps an UNQUOTED body
# WHOLE (PR #1441 property 2) and every hook that reads a body for MUTATING commands needs it that
# way. This hook's observable is different: it asks whether a +/- body reaches the CONSOLE, and a
# line of note text that merely BEGINS with `git diff` neither prints nor runs. Keeping the shared
# call would have re-introduced the false block the moment the import resolved -- which is exactly
# the condition under review, since 22df0be2 was self-tested standalone and shipped alongside
# `_hookutil`. So the in-file implementation is AUTHORITATIVE for this hook, and the self-test
# asserts the two agree everywhere EXCEPT the one documented refinement. The de-duplication this
# splits is real; the follow-up is to lift `_live_expansions` into `_hookutil` behind a flag, which
# changes other hooks' behaviour and is therefore not this fix's to make.
strip_heredocs = _strip_heredocs_local

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
# `--quiet` is NOT here: it is order-free for the diff-* family only. See _QUIET_SOFT_SUBS.
HARD_SUPPRESS_LONG = {"--name-only", "--name-status", "--check"}

# Subcommands where `--quiet` only SETS the format instead of hard-suppressing. Verified on
# git 2.53.0: `git log --quiet -p` and `git show --quiet -p HEAD` each print a full patch, while
# `git show --quiet HEAD` prints none, so it clears the DEFAULT patch and not an explicit one.
# 22df0be2 treated `--quiet` as order-free everywhere and therefore ALLOWED both walls.
_QUIET_SOFT_SUBS = {"log", "show", "whatchanged"}

# Long flags that turn the patch body ON. `--binary` implies --patch and is order-sensitive in
# exactly the way -p is (`--no-patch --binary` prints, `--binary --no-patch` does not): vpr-1472
# codex#1, verified by count on git 2.53.0.
PATCH_LONG = {"--patch", "--patch-with-stat", "--patch-with-raw", "--cc", "--unified", "--binary"}

# WEAK patch flags: they print a body on their own, but ANY other format flag beats them in EITHER
# order (verified: --stat, --no-patch, --name-only, --check and --quiet each take
# `git log --remerge-diff -1` from 2380 content rows to 0). Modelling them as PATCH_LONG would have
# false-blocked `--no-patch --remerge-diff`, which prints nothing.
WEAK_PATCH_LONG = {"--remerge-diff"}

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
# The target is NORMALISED (`_normalise_path`) before either test, so a redundant separator is not a
# different destination: `/dev//tty`, `/dev/./stderr` and `//dev/stdout` are the console (codex#2).
CONSOLE_TARGETS = {"/dev/tty", "/dev/console", "/dev/stdout", "/dev/stderr", "/dev/ptmx"}
_CONSOLE_FD_RE = re.compile(
    r"^(?:/dev/fd/[12]|/proc/(?:self|thread-self|\d+)/fd/[12]|/dev/pts/\d+"
    r"|/dev/tty\d+|/dev/ttyS\d+)$")

# Pipeline stages that CONSUME rather than relay: their console output is a count or a digest.
NON_RELAYING = {"wc", "md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum",
                "shasum", "b2sum", "cksum", "sum", "true", ":"}

# grep only consumes when it is counting or testing.
_GREP_COMMANDS = {"grep", "egrep", "fgrep", "rg", "ggrep"}
_GREP_QUIET_FLAGS = {"-c", "--count", "-q", "--quiet", "--silent", "-l", "-L",
                     "--files-with-matches", "--files-without-match"}

# Words whose enclosing context CAPTURES a command substitution instead of printing it. These are
# CONSUMERS: the word that actually receives the substitution's value.
CAPTURING_WORDS = {"[", "[[", "test", "local", "export", "declare", "readonly", "typeset", "let",
                   "return", "exit"}

# Reserved words that may sit in front of the consumer without being it. `if` and `while` were in
# CAPTURING_WORDS at 22df0be2, which made `if echo "$(git diff)"; then :; fi` read as captured
# (vpr-1472 codex#3). They are TRANSPARENT: skip them and keep looking for the real consumer.
CAPTURE_TRANSPARENT = {"if", "then", "elif", "else", "while", "until", "do", "done", "fi",
                       "for", "select", "case", "esac", "in", "function", "!", "{", "}",
                       "((", "))", "time"}

# Non-git renderers of the same wall (COVER_NON_GIT_DIFF).
DIFF_COMMANDS = {"diff", "colordiff", "sdiff", "icdiff"}
DIFF_QUIET_FLAGS = {"-q", "--brief", "-h", "--help", "--version", "--report-identical-files"}

# Unbounded dumpers of a saved patch (COVER_PATCH_FILE_DUMP). Bounded readers stay allowed.
DUMP_COMMANDS = {"cat", "bat", "batcat", "less", "more", "most", "view", "tac", "nl"}
PATCH_SUFFIXES = (".diff", ".patch")

_ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*", re.DOTALL)
_MAX_DEPTH = 5

# A substitution is lifted out of the outer text and replaced by a NUMBERED placeholder, and the
# body is kept in a registry beside it. The number is what lets a redirect classifier ask what a
# process substitution actually runs: `git diff > >(wc -l)` needs the consumer word `wc` to decide
# that a COUNT reaches the console rather than the body (vpr-1472 codex#6), and at 22df0be2 the
# placeholder was a single opaque string, so the consumer was unrecoverable and every `>(...)` was
# classified as relaying. The registry is process-local and one hook process handles ONE command;
# `offending_segment()` clears it so a long-lived caller (the self-test) cannot grow it without
# bound or read a stale body.
_SUBST_PREFIX = "__GRC_SUBST_"
_SUBST_RE = re.compile(r"__GRC_SUBST_\d+__")
_SUBST_BODIES = []


def _new_placeholder(inner: str) -> str:
    _SUBST_BODIES.append(inner)
    return "%s%d__" % (_SUBST_PREFIX, len(_SUBST_BODIES) - 1)


def _placeholder_body(token: str):
    """The registered body of a placeholder TOKEN, or None when the token is not one."""
    token = token.strip()
    if not _SUBST_RE.fullmatch(token):
        return None
    index = int(token[len(_SUBST_PREFIX):-2])
    return _SUBST_BODIES[index] if index < len(_SUBST_BODIES) else None


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

    The decision reads the CONSUMER -- the first word of the prefix that is not an assignment, a
    wrapper or a transparent reserved word -- and not, as at 22df0be2, ANY word anywhere in the
    prefix. That older scan had two live consequences, both fixed here and both fixtured:

      * `if echo "$(git diff)"; then :; fi` was read as captured because `if` was in the set. It is
        not: `echo` is the condition command and it prints the wall (vpr-1472 codex#3).
      * so was `echo "exit code: $(git diff)"`, because the ENGLISH word `exit` was in the set. One
        extra word in a string defeated the guard (vpr-1472 claude F4).

    A prefix that reduces to reserved words alone (`if $(git diff); then`) returns False, the same
    answer an EMPTY prefix already gave: the conservative side, and unchanged from 22df0be2.
    """
    words = prefix.split()
    if not words:
        return False
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=[\"']?", words[-1]):
        return True                                      # x=$( ... )
    for word in words:
        bare = os.path.basename(word.strip("\"'"))
        if not bare:
            continue
        if bare in CAPTURING_WORDS:
            return True
        if bare in CAPTURE_TRANSPARENT or _ASSIGN_RE.fullmatch(bare) or bare in WRAPPERS:
            continue
        return False                                     # the consumer is a PRINTING command
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
            out.append(_new_placeholder(text[i + 1:end]))
            i = end + 1
            continue
        if text.startswith("$((", i):
            end = _match_paren(text, i + 1)              # arithmetic: opaque, no recursion
            if end < 0:
                raise ValueError("unterminated arithmetic expansion")
            out.append(_new_placeholder(""))
            i = end + 2                                  # skip the second `)` of `))`
            continue
        if text.startswith("$(", i):
            end = _match_paren(text, i + 1)
            if end < 0:
                raise ValueError("unterminated command substitution")
            inner.append((text[i + 2:end], _is_capturing_context("".join(out[last_break:]))))
            out.append(_new_placeholder(text[i + 2:end]))
            i = end + 1
            continue
        if ch in "<>" and not in_double and text.startswith("(", i + 1):
            end = _match_paren(text, i + 1)
            if end < 0:
                raise ValueError("unterminated process substitution")
            # A process-substitution body is NOT captured: `cat <(git diff)` and `> >(cat)` both
            # relay. The `>(` marker is preserved so the redirect classifier can see it.
            inner.append((text[i + 2:end], False))
            out.append(ch + "(" + _new_placeholder(text[i + 2:end]) + ")")
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


def _join_continuations(text: str) -> str:
    """Remove a backslash-newline OUTSIDE single quotes, which is what the shell does before it
    parses.

    `git diff --stat \\` + newline + `-p` is ONE command and prints a full patch. Splitting it on
    the newline handed the tokenizer a trailing backslash, which raised, which failed the WHOLE
    command open (vpr-1472 claude F1, the sharper of its two spellings). The pair is removed rather
    than replaced with a space, matching the shell: `--st\\` + newline + `at` is `--stat`.

    Inside SINGLE quotes a backslash is literal and the pair is left alone. Inside double quotes it
    IS a continuation, which is why only the single-quote state is tracked.
    """
    out = []
    i, n = 0, len(text)
    in_single = False
    while i < n:
        ch = text[i]
        if in_single:
            if ch == "'":
                in_single = False
            out.append(ch)
            i += 1
            continue
        if ch == "'":
            in_single = True
            out.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            if text[i + 1] == "\n":
                i += 2                                   # the shell removes the PAIR
                continue
            out.append(text[i:i + 2])                    # `\\` and friends: consume the escape
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _logical_lines(text: str):
    """Physical lines regrouped so a quoted string that SPANS a newline stays ONE logical line.

    The other half of vpr-1472 claude F1. A newline inside a quoted argument is ordinary shell:

        git commit -m "Title
        <blank line>
        Body"
        git diff

    Splitting on the newline first left `git commit -m "Title` for the tokenizer, which raised
    `No closing quotation`; the raise escaped past the per-segment guard and allowed the WHOLE
    command, including the `git diff` on the last line. Joining forward until the text tokenizes
    keeps the commit as one segment and leaves the `git diff` as its own, which is a BLOCK.

    A buffer that never balances is emitted as it stands and `_segments` fails that ONE line open.
    That is the accepted residue, and it is now a line rather than a whole command.
    """
    out, buf = [], None
    for line in text.split("\n"):
        candidate = line if buf is None else buf + "\n" + line
        try:
            _tokenize(candidate)
        except ValueError:
            buf = candidate
            continue
        out.append(candidate)
        buf = None
    if buf is not None:
        out.append(buf)
    return out


def _segments(text: str):
    """[(tokens, operator_that_followed), ...].

    Newlines are split FIRST, because shlex treats a newline as ordinary whitespace and would
    otherwise fuse two lines into one segment, letting a `--stat` on line 1 exempt a bare
    `git diff` on line 2. `_logical_lines` is what stops that split from cutting a quoted string
    in half.
    """
    out = []
    for line in _logical_lines(text):
        if not line.strip():
            continue
        try:
            tokens = _tokenize(line)
        except ValueError:
            continue                                     # per-LINE fail-open, never whole-command
        current = []
        for tok in tokens:
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
    state = {"patch": False, "format_set": False, "hard": False, "weak": False}
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
        if head == "--quiet":
            # Subcommand-dependent, measured rather than assumed: for the diff-* family `--quiet`
            # beats a patch flag in either order, but `git log --quiet -p` and
            # `git show --quiet -p HEAD` each print a full patch. 22df0be2 called `--quiet`
            # order-free everywhere and therefore allowed both of those walls.
            if sub in _QUIET_SOFT_SUBS:
                state["format_set"] = True
            else:
                state["hard"] = True
        elif head in WEAK_PATCH_LONG:
            state["weak"] = True                         # deliberately does NOT set format_set
        elif head in HARD_SUPPRESS_LONG:
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
    if state["patch"]:
        return True
    if state["weak"] and not state["format_set"]:
        return True                                      # `--remerge-diff` with nothing beating it
    return not state["format_set"] and sub in ALWAYS_CONTENT


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

def _normalise_path(target: str) -> str:
    """Collapse redundant separators and `.` segments before a destination is compared.

    `/dev//tty`, `/dev/./stderr`, `//dev/stdout` and `/proc/self//fd/1` are the console under any
    spelling; at 22df0be2 only a TRAILING slash was removed, so each of those evaded the console
    test and reached the screen through a redirect the hook believed was quiet (vpr-1472 codex#2).

    This is a LEXICAL normalisation of the command text, not a resolution of the file system: no
    symlink is followed and no path is touched, so it cannot change what an ordinary output file
    means and it cannot depend on machine state at hook time.
    """
    if not target:
        return target
    return re.sub(r"^/{2,}", "/", posixpath.normpath(target))


def _target_is_quiet(kind: str, target: str) -> bool:
    """True when a redirect destination genuinely keeps the body off the maintainer's screen."""
    if kind == "dup":
        if not target or target.isdigit():
            # `>&1` / `>&2` obviously relay. An ALREADY-OPEN descriptor (`1>&3` after `3>&1`, the
            # standard "back to stdout" spelling) cannot be proved quiet from one segment, and
            # 22df0be2 called every fd other than 1 and 2 quiet, which allowed a real wall
            # (vpr-1472 codex#4). Unprovable is treated as CONSOLE.
            return False
        kind = "file"                                    # csh-style `>& word`: BOTH streams to a
        #                                                  PATH, so classify the path (claude F2)
    if not target:
        return False
    if target.startswith(">(") or target.startswith("<("):
        return False                                     # bare marker: see _stdout_is_quiet
    if "$" in target or "`" in target or _SUBST_RE.search(target):
        return not REQUIRE_LITERAL_REDIRECT_TARGET
    norm = _normalise_path(target)
    if norm in CONSOLE_TARGETS or _CONSOLE_FD_RE.match(norm):
        return False
    return True


def _procsub_consumer_is_quiet(tokens, start: int) -> bool:
    """True when a `> >( ... )` CONSUMER prints a count or a digest rather than the body it is fed.

    22df0be2 classified every process-substitution target as relaying, so the sanctioned bounded
    shape `git diff > >(wc -l)` -- which puts ONE number on the console -- was refused
    (vpr-1472 codex#6). The consumer is now read with the SAME test a pipeline stage gets, which is
    also why `> >(cat)` and `> >(tee f)` stay blocked: those relay the wall.
    """
    body = None
    i = start
    while i < len(tokens) and tokens[i] != ")":
        registered = _placeholder_body(tokens[i])
        if registered is not None:
            body = registered
        i += 1
    if body is None:
        return False
    try:
        inner = _tokenize(body)
    except ValueError:
        return False                                     # unreadable consumer: assume it relays
    return _consumes_rather_than_relays(inner) or _stdout_is_quiet(inner)


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
        if target in (">(", "<("):
            found = ("procsub", i + 2)                   # the consumer decides, not the marker
        else:
            found = ("dup" if tok == ">&" else "file", target)
    if found is None or not ALLOW_FILE_REDIRECT:
        return False
    if found[0] == "procsub":
        return _procsub_consumer_is_quiet(tokens, found[1])
    return _target_is_quiet(found[0], found[1])


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
    return _SUBST_RE.sub("...", " ".join(tokens))


def _scan_command(text: str, captured: bool = False, depth: int = 0):
    """The first console-reaching content dump in this shell text, as a display string, or None."""
    if depth > _MAX_DEPTH or not isinstance(text, str) or not text.strip():
        return None
    outer, subs = _split_substitutions(_join_continuations(strip_heredocs(text)))
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
    del _SUBST_BODIES[:]                                 # one process, one command: no stale bodies
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
    # --- vpr-1472 codex#1: patch-enabling flags the 22df0be2 model did not recognise -------------
    "git log --binary -1 --format=",                           # codex#1's exact failing input
    "git log --binary",
    "git diff --binary",
    "git log --no-patch --binary",                             # order-sensitive, like -p
    "git log --stat --binary",
    "git show --binary HEAD",
    "git log --remerge-diff -1",                               # weak patch, nothing beating it
    "git diff --remerge-diff",
    # --- extra, found while verifying codex#1: --quiet is not order-free for log / show -----------
    "git log --quiet -p",
    "git log -p --quiet",
    "git show --quiet -p HEAD",
    "git log --quiet --binary",
    # --- vpr-1472 codex#2: a console path spelled with redundant separators ----------------------
    "git diff > /dev//tty",
    "git diff > /dev/./stderr",
    "git diff > //dev/stdout",
    "git diff > /proc/self//fd/1",
    "git diff > /dev/pts//3",
    "git diff > /dev/tty/",
    "git diff --output=/dev//tty",
    # --- extra, same class as codex#2: the numbered virtual consoles (claude F8) -----------------
    "git diff > /dev/tty1",
    "git diff > /dev/ttyS0",
    # --- vpr-1472 codex#3: a reserved word must not make a PRINTING consumer look captured -------
    "if echo \"$(git diff)\"; then :; fi",                     # codex#3's exact failing input
    "while echo \"$(git diff)\"; do break; done",
    "until echo $(git show HEAD); do break; done",
    # --- vpr-1472 codex#4 / claude F2: a console fd and the csh-style `>&` spelling --------------
    "git diff HEAD^ HEAD -- README.md 3>&1 1>&3",              # codex#4's exact failing input
    "git diff >&3",
    "git diff 1>&4",
    "git diff >& /dev/tty",                                    # claude F2, all three spellings
    "git diff >&/dev/tty",
    "git diff >& /dev/pts/2",
    "git diff >& /dev/stdout",
    # --- vpr-1472 claude F4: an ENGLISH word in the prefix must not defeat the capture test ------
    "echo test $(git diff)",
    'echo "test output: $(git diff)"',
    'echo "if you look: $(git diff)"',
    'echo "exit code: $(git diff)"',
    'printf "%s" "$(git diff)"',
    # --- vpr-1472 claude F1: a construct that spans a newline is PARSED, not failed open ---------
    'git commit -m "Title\n\nBody"\ngit diff',                 # F1 spelling 1
    "git diff --stat \\\n-p",                                  # F1 spelling 2, prints 230 rows
    "git log \\\n-p",
    "git commit -m 'one\ntwo'\ngit show HEAD",
    "git diff \\\n--patch",
    # --- a heredoc body piped INTO an interpreter is still a PROGRAM ----------------------------
    "cat <<EOF | bash\ngit diff\nEOF",
    "cat <<'EOF' | sh\ngit diff\nEOF",
    # --- a process substitution that RELAYS is still a wall (the codex#6 counterpart) ------------
    "git diff > >(tee /tmp/d.diff)",
    "git diff > >(grep '^+')",
    "git diff > >(head -20)",
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
    # --- vpr-1472 codex#5 / claude F5: an UNQUOTED heredoc body is DATA, like a quoted one ---------
    "cat > /tmp/note.md <<EOF\ngit diff\nEOF",                 # codex#5's exact failing input
    "cat > /tmp/note.md <<EOF\ngit diff is forbidden here\nEOF",
    "cat > /tmp/note.md <<EOF\ncat report.patch to read it\nEOF",
    "cat > /tmp/note.md <<EOF\ngit show HEAD:file.py is refused too\nEOF",
    "cat > /tmp/note.md <<-EOF\n\tgit diff\n\tEOF",            # tab-stripping, unquoted
    "tee /tmp/note.md <<EOF\ndiff -u a b renders a wall\nEOF",
    # --- vpr-1472 codex#6: a process-substitution CONSUMER that counts is not a wall ---------------
    "git diff > >(wc -l)",                                     # codex#6's exact failing input
    "git diff > >(md5sum)",
    "git diff > >(grep -c '^+')",
    "git diff > >(sha256sum)",
    "git diff > >(cat > /tmp/d.diff)",                         # the consumer's own stdout is quiet
    # --- vpr-1472 claude F2 counterpart: `>& path` is the csh form and a file is still quiet -------
    "git diff >& /tmp/d.diff",
    "git diff >& /dev/null",
    "git diff >&/tmp/d.diff",
    # --- vpr-1472 codex#2 counterpart: normalisation must not turn an ordinary path into a console -
    "git diff > /tmp//d.diff",
    "git diff > /tmp/./d.diff",
    "git diff > /tmp/dev/tty",
    "git diff > /tmp/d.diff/",
    # --- vpr-1472 codex#1 counterpart: the weak patch flag really is beaten, in either order -------
    "git log --remerge-diff --no-patch",
    "git log --no-patch --remerge-diff",
    "git log --stat --remerge-diff -1",
    "git log --quiet --remerge-diff -1",
    "git log --remerge-diff --name-only",
    "git log --binary --no-patch",
    "git diff --quiet --binary",
    "git show --quiet HEAD",
    # --- vpr-1472 codex#3 / claude F4 counterpart: a real capturing CONSUMER still captures --------
    'while [ -n "$(git diff)" ]; do break; done',
    'if [[ -n "$(git diff)" ]]; then echo dirty; fi',
    'test -n "$(git diff)"',
    'if test -n "$(git diff)"; then echo dirty; fi',
    "export SUMMARY=$(git diff)",
    "local x=$(git diff)",
    'if sudo test -n "$(git diff)"; then echo dirty; fi',
    # --- vpr-1472 claude F1 counterpart: the multi-line command itself is not a diff ---------------
    'git commit -m "Title\n\nBody"',
    "git diff --stat \\\n--name-only",
    'git commit -m "line one\nline two" && git diff --stat',
    # --- STATED RESIDUE, asserted so the gap is visible rather than claimed away --------------------
    "python3 -c 'import os; os.system(\"git diff\")'",
    "G=git; $G diff",
    "x=$(git diff)\necho \"$x\"",                              # capture-then-print, claude F6
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
    # ACCEPTED MISS (vpr-1472 claude F1). Text that never balances however the lines are grouped
    # still fails open. `_logical_lines` joins forward first, so the two ORDINARY spellings F1
    # named are parsed and blocked; what is left is exotic, and fail-open costs a miss, not a
    # false block. Asserted here so the direction can never silently invert.
    "git diff 'unbalanced\ngit show HEAD",
    'git show "open\ngit diff',
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
    if _SUBST_RE.search(offending_segment("git diff > >(cat)") or ""):
        bad += 1
        print("FAIL: the substitution placeholder leaked into the reported segment")

    # Layer contracts for the vpr-1472 fixes, asserted directly and not only through a fixture, so
    # a future refactor breaks HERE with a name attached rather than in a command far downstream.
    for target, want in (("/dev//tty", "/dev/tty"), ("/dev/./stderr", "/dev/stderr"),
                         ("//dev/stdout", "/dev/stdout"), ("/proc/self//fd/1", "/proc/self/fd/1"),
                         ("/dev/tty/", "/dev/tty"), ("/tmp//d.diff", "/tmp/d.diff"),
                         ("/tmp/dev/tty", "/tmp/dev/tty"), ("", "")):
        extra += 1
        if _normalise_path(target) != want:              # codex#2
            bad += 1
            print("FAIL normalise: %r -> %r want %r" % (target, _normalise_path(target), want))

    for body, want in (("git diff", []),
                       ("git diff is forbidden here", []),
                       ("$(git diff)", ["$(git diff)"]),
                       ("see $(git diff) below", ["$(git diff)"]),
                       ("`git diff`", ["`git diff`"]),
                       ("cost is $((1 + 2)) units", []),
                       ("\\$(git diff)", []),
                       ("$(git diff", [])):
        extra += 1
        if _live_expansions(body) != want:               # codex#5 / claude F5
            bad += 1
            print("FAIL live-expansions: %r -> %r want %r"
                  % (body, _live_expansions(body), want))

    for prefix, want in (("x=", True), ("echo ", False), ("if ", False), ("if [ -n \"", True),
                         ("if [[ -n \"", True), ("if echo \"", False), ("echo test ", False),
                         ("echo \"exit code: ", False), ("test -n \"", True),
                         ("sudo test -n \"", True), ("export FOO=", True), ("", False)):
        extra += 1
        if _is_capturing_context(prefix) != want:        # codex#3 / claude F4
            bad += 1
            print("FAIL capture-context: %r -> %s want %s"
                  % (prefix, _is_capturing_context(prefix), want))

    for text, want in (("a \\\nb", "a b"), ("a\\\nb", "ab"), ("a \\\\\nb", "a \\\\\nb"),
                       ("'a \\\nb'", "'a \\\nb'"), ("a b", "a b")):
        extra += 1
        if _join_continuations(text) != want:            # claude F1
            bad += 1
            print("FAIL join-continuations: %r -> %r want %r"
                  % (text, _join_continuations(text), want))

    extra += 2
    if len(_logical_lines('git commit -m "a\n\nb"\ngit diff')) != 2:
        bad += 1
        print("FAIL logical-lines: a multi-line quoted string must regroup into one line")
    if len(_logical_lines("git diff --stat\ngit diff")) != 2:
        bad += 1
        print("FAIL logical-lines: two balanced lines must stay two lines")

    # The heredoc layer, asserted directly rather than only through the command fixtures. Each row
    # is (command, does PAYLOAD survive the strip). A body that survives is scanned as a program.
    # Rows are (command, does PAYLOAD survive the strip, is this row a DELIBERATE divergence from
    # `_hookutil.strip_heredocs`). A body that survives is scanned as a program.
    heredoc_cases = [
        ("cat > f <<'EOF'\nPAYLOAD\nEOF",        False, False),  # quoted tag: inert DATA
        ('cat > f <<"EOF"\nPAYLOAD\nEOF',        False, False),
        ("cat > f <<-'EOF'\n\tPAYLOAD\n\tEOF",   False, False),  # tab-stripping form
        ("cat > f <<EOF\nPAYLOAD\nEOF",          False, True),   # codex#5: literal text is DATA
        ("cat > f <<-EOF\n\tPAYLOAD\n\tEOF",     False, True),
        ("cat > f <<EOF\n$(PAYLOAD)\nEOF",       True,  True),   # a LIVE EXPANSION is a command
        ("cat > f <<EOF\n`PAYLOAD`\nEOF",        True,  True),
        ("bash <<'EOF'\nPAYLOAD\nEOF",           True,  False),  # interpreter body is a PROGRAM
        ("sh <<'EOF'\nPAYLOAD\nEOF",             True,  False),
        ("ssh host <<'EOF'\nPAYLOAD\nEOF",       True,  False),
        ("sudo sh <<'EOF'\nPAYLOAD\nEOF",        True,  False),
        ("bash <<EOF\nPAYLOAD\nEOF",             True,  False),  # unquoted INTERPRETER body: kept
        ("cat <<'EOF' | bash\nPAYLOAD\nEOF",     True,  True),   # piped INTO a shell: a PROGRAM
        ("cat <<EOF | bash\nPAYLOAD\nEOF",       True,  False),
        ("python3 <<'EOF'\nPAYLOAD\nEOF",        False, False),  # not shell: see RESIDUE
        ("cat > f <<'NOEND'\nPAYLOAD\n",         True,  False),  # no terminator: strip NOTHING
        ("echo a <<< 'PAYLOAD'",                 True,  False),  # herestring, not a heredoc
        ("echo a << b\nPAYLOAD",                 True,  False),  # `<<` with no shell-word tag
    ]
    for command, must_survive, _diverges in heredoc_cases:
        extra += 1
        if ("PAYLOAD" in strip_heredocs(command)) != must_survive:
            bad += 1
            print("FAIL heredoc: %r want survive=%s" % (command, must_survive))
    # Text after a stripped body must survive: swallowing it is a universal bypass.
    extra += 1
    if "AFTERWARDS" not in strip_heredocs("cat > f <<'EOF'\nPAYLOAD\nEOF\nAFTERWARDS"):
        bad += 1
        print("FAIL heredoc: text after a stripped body did not survive")
    extra += 1
    if "AFTERWARDS" not in strip_heredocs("cat > f <<EOF\nPAYLOAD\nEOF\nAFTERWARDS"):
        bad += 1
        print("FAIL heredoc: text after an unquoted body did not survive")

    # DIVERGENCE from `_hookutil.strip_heredocs`, asserted so it stays INTENDED and BOUNDED rather
    # than becoming drift. The shared module keeps an unquoted DATA body whole; this hook keeps
    # only its live expansions (codex#5 / claude F5). Every other row must still agree byte for
    # byte, and the shared module must still exhibit the wider behaviour -- if it is ever narrowed
    # the same way, this whole local implementation should be deleted in favour of it.
    if _HEREDOC_IMPL == "_hookutil-present":
        extra += 2
        drift = [c for c, _s, diverges in heredoc_cases
                 if not diverges and _shared_strip_heredocs(c) != _strip_heredocs_local(c)]
        if drift:
            bad += 1
            print("FAIL: unintended divergence from _hookutil on " + repr(drift))
        if "PAYLOAD" not in _shared_strip_heredocs("cat > f <<EOF\nPAYLOAD\nEOF"):
            bad += 1
            print("FAIL: _hookutil no longer keeps an unquoted body; drop the in-file copy")

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